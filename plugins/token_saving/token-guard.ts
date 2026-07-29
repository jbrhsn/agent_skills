import type { Plugin, PluginOptions } from "@opencode-ai/plugin"

// Defaults. Override per-project via the tuple form in opencode.json, e.g.:
//   "plugin": [["./.opencode/plugin/token-guard.ts", { "maxOutputChars": 8000 }]]
const DEFAULT_MAX_OUTPUT_CHARS = 8000

// Tools whose output we truncate. `read` is intentionally excluded: opencode's
// built-in read tool already truncates and spools full output to a file for
// offset/grep re-reads, and hard-slicing it here breaks the "read a larger
// window" workflow.
const TRUNCATE_TOOLS = new Set(["bash", "webfetch"])

// Commands that dump whole files/streams into context. Kept deliberately broad
// (leading path, pipes, and pagers) so it is not trivially bypassed, while
// still allowing small explicit reads via the `read` tool.
const DUMP_COMMAND = /(^|[|&;]\s*)(\/\w+\/)?(cat|less|more|tail|head)(\s|$)/i

function headTail(text: string, max: number): string {
  if (text.length <= max) return text
  // Preserve both ends: command context lives at the head, errors/stack traces
  // at the tail. Split the budget and mark the elision.
  const half = Math.floor(max / 2)
  const head = text.slice(0, half)
  const tail = text.slice(text.length - half)
  const removed = text.length - head.length - tail.length
  return `${head}\n...[truncated ${removed} chars]...\n${tail}`
}

export const TokenGuard: Plugin = async (_ctx, options?: PluginOptions) => {
  const maxOutputChars =
    typeof options?.maxOutputChars === "number"
      ? (options.maxOutputChars as number)
      : DEFAULT_MAX_OUTPUT_CHARS

  return {
    // Truncate large bash/webfetch output before it enters context, keeping
    // both the head (context) and tail (errors).
    "tool.execute.after": async (input, output) => {
      try {
        if (
          TRUNCATE_TOOLS.has(input.tool) &&
          typeof output.output === "string" &&
          output.output.length > maxOutputChars
        ) {
          output.output = headTail(output.output, maxOutputChars)
        }
      } catch {
        // Never let the guard disrupt the tool-result flow.
      }
    },

    // Discourage expensive full-file/stream dumps in favor of targeted reads.
    "tool.execute.before": async (input, output) => {
      if (input.tool !== "bash") return
      const command = output.args?.command
      if (typeof command === "string" && DUMP_COMMAND.test(command)) {
        throw new Error(
          "Avoid dumping whole files/streams (cat/less/more/head/tail) into context — " +
            "use the `read` tool with an offset/limit or `grep` for targeted lookups instead."
        )
      }
    },

    // Replace the compaction prompt to enforce terse, decision-focused summaries.
    "experimental.session.compacting": async (_input, output) => {
      // `context` is a string[] the runtime may append to; keep it defined.
      if (!Array.isArray(output.context)) output.context = []
      output.prompt = `
You are generating a continuation summary for this session.
Summarize ONLY:
1. The current task and its status
2. Key decisions made and why
3. Files touched and a one-line description of each change
4. Any pending verification steps

Do NOT include: raw command output, full diffs, full file contents, or logs.
      `.trim()
    },
  }
}

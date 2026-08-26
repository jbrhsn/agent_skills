import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { tool } from "@opencode-ai/plugin";

const DEFAULT_TAVILY_OPEN_URL = "http://localhost:8000";

// --- Key Management & Secrets Fallback ---
function getApiKey(keyName) {
  if (process.env[keyName]) {
    return process.env[keyName];
  }
  const secretsPath = path.join(os.homedir(), ".secrets");
  if (fs.existsSync(secretsPath)) {
    try {
      const content = fs.readFileSync(secretsPath, "utf-8");
      for (const line of content.split("\n")) {
        const trimmed = line.trim();
        if (trimmed.startsWith("export ") && trimmed.includes("=")) {
          const [k, ...v] = trimmed.slice(7).split("=");
          if (k.trim() === keyName) {
            return v.join("=").replace(/^['"]|['"]$/g, "").trim();
          }
        } else if (trimmed.includes("=") && !trimmed.startsWith("#")) {
          const [k, ...v] = trimmed.split("=");
          if (k.trim() === keyName) {
            return v.join("=").replace(/^['"]|['"]$/g, "").trim();
          }
        }
      }
    } catch {
      // Ignore read errors
    }
  }
  return undefined;
}

// --- In-Memory Caching (10-minute TTL) ---
const cache = new Map();
const CACHE_TTL_MS = 10 * 60 * 1000;

function getCached(key) {
  const item = cache.get(key);
  if (!item) return null;
  if (Date.now() - item.timestamp > CACHE_TTL_MS) {
    cache.delete(key);
    return null;
  }
  return item.value;
}

function setCache(key, value) {
  if (cache.size > 200) {
    const oldestKey = cache.keys().next().value;
    if (oldestKey) cache.delete(oldestKey);
  }
  cache.set(key, { timestamp: Date.now(), value });
}

// --- Pure Result Formatter ---
function formatSearchOutput({ query, results = [], answer, warning, creditsUsed = "N/A", provider }) {
  const blocks = [`[Provider: ${provider}]`, `Query: ${query}`, "=".repeat(40)];
  if (warning) {
    blocks.push(`Warning: ${warning}`, "-".repeat(40));
  }
  if (answer) {
    blocks.push("Answer:", answer.trim(), "-".repeat(40));
  }
  if (results.length > 0) {
    blocks.push("Search Results:");
    results.forEach((item, idx) => {
      const title = String(item.title || item.metadata?.title || "Untitled").trim();
      const url = String(item.url || item.metadata?.sourceURL || "").trim();
      let content = String(item.content || item.markdown || item.description || "").trim();
      // Optimization: Budget snippet size to avoid token blowout
      if (content.length > 1500) {
        content = content.slice(0, 1500) + "... [truncated]";
      }
      let text = `\n[${idx + 1}] ${title}`;
      if (url) text += `\n    URL: ${url}`;
      if (content) text += `\n    Content: ${content}`;
      blocks.push(text);
    });
    blocks.push("-".repeat(40));
  }
  blocks.push(`Usage Credits: ${creditsUsed}`);
  return blocks.join("\n");
}

// --- Provider Handlers ---
async function searchTavily(query, maxResults = 5) {
  const key = getApiKey("TAVILY_API_KEY");
  if (!key) throw new Error("TAVILY_API_KEY is not set.");

  const response = await fetch("https://api.tavily.com/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      api_key: key,
      query,
      max_results: maxResults,
      include_answer: "basic",
      include_usage: true,
    }),
    signal: AbortSignal.timeout(20000),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Tavily error (${response.status}): ${errorText}`);
  }

  const data = await response.json();
  const results = (data.results || []).map((r) => ({
    title: r.title,
    url: r.url,
    content: r.content,
  }));

  return formatSearchOutput({
    query,
    results,
    answer: data.answer,
    creditsUsed: data.usage?.credits ?? "N/A",
    provider: "Tavily",
  });
}

async function searchFirecrawl(query, limit = 5) {
  const key = getApiKey("FIRECRAWL_API_KEY");
  if (!key) throw new Error("FIRECRAWL_API_KEY is not set.");

  const response = await fetch("https://api.firecrawl.dev/v2/search", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      limit,
      sources: ["web"],
      scrapeOptions: {
        onlyMainContent: true,
        maxAge: 172800000,
        parsers: ["pdf"],
        formats: ["markdown"],
      },
    }),
    signal: AbortSignal.timeout(20000),
  });

  const isJson = response.headers.get("content-type")?.includes("application/json");
  const data = isJson ? await response.json() : {};

  if (!response.ok || !data.success) {
    const err = data.error || (await response.text()) || "Request failed";
    throw new Error(`Firecrawl error (${response.status}): ${err}`);
  }

  let raw = data.data || [];
  let webResults = [];
  if (Array.isArray(raw)) {
    webResults = raw;
  } else if (raw && Array.isArray(raw.web)) {
    webResults = raw.web;
  }

  const results = webResults.map((r) => ({
    title: r.title || r.metadata?.title,
    url: r.url || r.metadata?.sourceURL,
    content: r.markdown || r.description || r.summary,
  }));

  return formatSearchOutput({
    query,
    results,
    warning: data.warning,
    creditsUsed: data.creditsUsed ?? "N/A",
    provider: "Firecrawl",
  });
}

async function searchTavilyOpen(query, maxResults = 5) {
  const baseUrl = (process.env.TAVILY_OPEN_URL || DEFAULT_TAVILY_OPEN_URL).replace(/\/+$/, "");
  const endpoint = `${baseUrl}/tavily/search`;

  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      max_results: maxResults,
      search_depth: "basic",
      include_answer: true,
    }),
    signal: AbortSignal.timeout(15000),
  });

  const isJson = response.headers.get("content-type")?.includes("application/json");
  const data = isJson ? await response.json() : {};

  if (!response.ok) {
    const err = data.error || (await response.text()) || "Local search request failed";
    throw new Error(`tavily-open error (${response.status}): ${err}`);
  }

  const results = (data.results || []).map((r) => ({
    title: r.title,
    url: r.url,
    content: r.content,
  }));

  return formatSearchOutput({
    query,
    results,
    answer: data.answer,
    creditsUsed: data.usage?.credits ?? 0,
    provider: "Local tavily-open",
  });
}

async function unifiedSearch(query, maxResults = 5) {
  const cacheKey = `${query.trim().toLowerCase()}_${maxResults}`;
  const cached = getCached(cacheKey);
  if (cached) return cached;

  const cloudProviders = [
    { name: "Tavily", fn: () => searchTavily(query, maxResults) },
    { name: "Firecrawl", fn: () => searchFirecrawl(query, maxResults) },
  ];

  // Randomize cloud provider distribution
  if (Math.random() > 0.5) {
    cloudProviders.reverse();
  }

  const errors = [];

  // Tier 1: Try Cloud Providers (Randomized with cross-fallback)
  for (const { name, fn } of cloudProviders) {
    try {
      const output = await fn();
      setCache(cacheKey, output);
      return output;
    } catch (err) {
      errors.push(`[${name}] ${err.message}`);
    }
  }

  // Tier 2: Fallback to local tavily-open instance
  try {
    const localOutput = await searchTavilyOpen(query, maxResults);
    setCache(cacheKey, localOutput);
    return localOutput;
  } catch (err) {
    errors.push(`[Local tavily-open] ${err.message}`);
  }

  throw new Error("All search providers (including local fallback) failed:\n" + errors.join("\n"));
}

// --- OpenCode Plugin Export ---
export default async function () {
  return {
    tool: {
      web_search_tool: tool({
        description:
          "Search the live web using Tavily, Firecrawl, or local tavily-open fallback. " +
          "CRITICAL USAGE PATTERN: Do NOT call directly from the primary orchestrator. " +
          "Delegate web search to a dedicated research/executor subagent. " +
          "The subagent must analyze the raw results, extract relevant facts, " +
          "and return ONLY a synthesized summary to the primary agent to avoid context blowout.",
        args: {
          query: tool.schema.string().describe("The search query string"),
          max_results: tool.schema
            .number()
            .optional()
            .describe("Maximum number of search results to return (default: 5, max: 10)"),
        },
        async execute(args) {
          const maxResults = Math.min(Math.max(args.max_results || 5, 1), 10);
          return await unifiedSearch(args.query, maxResults);
        },
      }),
    },
  };
}

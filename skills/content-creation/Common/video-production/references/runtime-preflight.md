# Runtime, model cache, and library preflight

Use `uv run` for every top-level Python command with `WORKSPACE/.venv/bin/python`. If `.venv` is absent, create it through uv before execution; if uv is unavailable, request installation confirmation and do not execute Python through another interpreter.

Do not pass ad hoc program source through `python -c`, stdin, a heredoc, Node `-e`/`--eval`, or `bash -c`/`sh -c`. Reuse an existing skill script first. Put a temporary reusable script at `WORKSPACE/.temp/<purpose>.py`, `.mjs`, or `.sh`; promote generally useful scripts into `SKILL/scripts/` with tests.

Before generated narration or transcription, verify the required models in the workspace cache:

```bash
uv run --python WORKSPACE/.venv/bin/python python SKILL/scripts/model_cache.py \
  --workspace-root WORKSPACE --require kokoro --require whisper:base --ensure
```

Model files always live below `WORKSPACE/.video_production_assets/kokoro` or `whisper`. The cache manager hashes existing files, downloads missing/corrupt files to a same-directory temporary file, verifies its checksum, then atomically replaces the target. It never uses a home-directory cache. Require only models the route needs; record `not-required` for silent/non-speech work.

After routing and before the creative plan, refresh/inspect the creative inventory and record focused searches tied to actual beats:

```bash
uv run --python WORKSPACE/.venv/bin/python python SKILL/scripts/review_asset_inventory.py \
  --assets-dir WORKSPACE/.video_production_assets --route faceless-standard \
  --query s01-b01="focus distraction desk" --out PROJECT/analysis/asset-library-review.json
```

The review is discovery evidence, not selection approval. Inspect shortlisted assets, confirm usable rights, and record selected, rejected, or no-fit dispositions before plan approval.

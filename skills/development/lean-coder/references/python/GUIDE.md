# Python — Lean Rules

## Stdlib first (do not add a dependency for these)

| Need | Use | Not |
|---|---|---|
| Records / config objects | `dataclasses`, `NamedTuple` | hand-written `__init__`, attrs |
| Grouping, counting | `collections.Counter`, `defaultdict`, `itertools.groupby` | manual dict loops |
| Caching | `functools.cache` / `lru_cache` | custom memo dicts |
| Paths, globbing | `pathlib.Path` | `os.path` string joins |
| CLI | `argparse` | click/typer for <5 flags |
| Retry with backoff | `tenacity` only if already present; else 6-line loop | a retry package |
| JSON, CSV, sqlite, http | `json`, `csv`, `sqlite3`, `urllib`/`httpx` | ORMs for one query |
| Batching | `itertools.batched` (3.12+) | custom chunker |
| Enum-ish constants | `enum.StrEnum` | string literals scattered |
| Concurrency | `asyncio.gather`, `ThreadPoolExecutor.map` | manual thread bookkeeping |

## Cut

- `__init__` + getters when `@dataclass(frozen=True)` does it
- Loops that `list.append` → comprehension (one line, one expression; if it needs two conditions and a nested loop, keep the loop)
- `if x == True`, `if len(xs) > 0` → `if x`, `if xs`
- Manual `open()/close()` → `with`
- Classes with one method and no state → module-level function
- `Any` type hints — either type it properly or drop the annotation
- `try/except Exception: raise` wrappers
- Wrapper functions that only forward args

## AI / ML specifics

- Use `pandas`/`polars` vectorized ops; a Python `for` loop over rows is a bug, not a style choice.
- Prompt strings live in one module-level constant, not f-string fragments assembled across functions.
- Tool/function schemas: derive from `pydantic` models or dataclasses — never hand-write JSON schema twice.
- Never re-implement tokenizer, retry, or streaming parsing the SDK already gives you.
- Seed and pin: `random.seed`, `numpy.random.default_rng(seed)`, explicit model version string.
- Cache expensive embeddings/inference by content hash, not by call site.

## Security (never cut)

- Never `eval`, `exec`, `pickle.load`, or `yaml.load` on untrusted input — `json` / `yaml.safe_load`.
- Secrets from `os.environ`, never literals; never log the value.
- `subprocess` with a list, `shell=False`. No f-string commands.
- SQL via parameters (`?`, `%s`), never f-strings.
- Validate LLM tool-call arguments before execution — model output is untrusted input.
- `secrets` module for tokens, not `random`.
- Cap file sizes, request timeouts, and recursion on anything user-supplied.

## Testability

- Pass the client/clock/path in as a parameter with a default: `def run(now=datetime.now)`.
- Prefer pure `transform(data) -> data`; keep I/O in a thin `main()`.
- Use `pytest.mark.parametrize` instead of near-duplicate test bodies.
- If you reach for `unittest.mock.patch` more than twice in a test, refactor the source.

## Example

```python
# before — 14 lines
class UserLoader:
    def __init__(self, path):
        self.path = path
    def load(self):
        results = []
        f = open(self.path)
        for line in f.readlines():
            if line.strip() != "":
                results.append(json.loads(line))
        f.close()
        return results

# after — 2 lines
def load_users(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
```

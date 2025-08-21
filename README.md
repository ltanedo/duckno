# DuckNo

Treat DuckDB as a tiny NoSQL-style key/value store.

## Install
- pip install duckdb

## Quick start
```python
from duckno import DuckNo

# Default: file-backed DB at ./duckno.db
kv = DuckNo()
kv.set("user:1", {"name": "Ada"})
print(kv.get("user:1"))   # {'name': 'Ada'}
print(kv.keys())           # ['user:1']
kv.close()

# In-memory (ephemeral)
with DuckNo(memory=True) as mem:
    mem.set("tmp", 123)
    assert mem.get("tmp") == 123

# Custom file path
kv2 = DuckNo("data/mydata.duckdb")
```

## Storage options
- Default: file-backed DB at ./duckno.db (current working directory)
- In-memory: DuckNo(memory=True) or DuckNo(":memory:", memory=True)
- Custom path: DuckNo("/path/to/db.duckdb" or "./my.db")

## API
- set(key, value) -> None
- get(key, default=None) -> Any
- keys() -> list[str]
- Context manager supported (with DuckNo(...): ...)
- database_path property returns the file path or None for in-memory

Notes: Values must be JSON-serializable (stored as JSON text).

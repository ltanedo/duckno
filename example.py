"""
Example usage of DuckNo - a tiny NoSQL-like key/value store built on DuckDB.

Run:
    python example.py

Requires:
    pip install duckdb
"""
from __future__ import annotations

from duckno import DuckNo


def main() -> None:
    print("--- Default file-backed DB (./duckno.db) ---")
    kv = DuckNo()  # creates ./duckno.db if it doesn't exist
    kv.set("user:1", {"name": "Ada", "roles": ["admin"]})
    print("user:1 =>", kv.get("user:1"))
    print("keys =>", kv.keys())
    print("database_path =>", kv.database_path)
    kv.close()

    print("\n--- In-memory DB ---")
    with DuckNo(memory=True) as mem:
        mem.set("tmp", 123)
        print("tmp =>", mem.get("tmp"))
        print("keys =>", mem.keys())
        print("database_path =>", mem.database_path)

    print("\n--- Custom file location (data/mydata.duckdb) ---")
    kv2 = DuckNo("data/mydata.duckdb")
    kv2.set("a", [1, 2, 3])
    print("a =>", kv2.get("a"))
    print("keys =>", kv2.keys())
    print("database_path =>", kv2.database_path)
    kv2.close()


if __name__ == "__main__":
    main()


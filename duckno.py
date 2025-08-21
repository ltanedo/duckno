"""
DuckNo - Simple NoSQL-like key/value store on top of DuckDB.

Features:
- set(key, value): store any JSON-serializable value
- get(key, default=None): retrieve and deserialize value by key
- keys(): list all keys

Storage options:
- In-memory (ephemeral) using ':memory:'
- File-backed at a specific path
- Default: file-backed 'duckno.db' in the current working directory

Requires: duckdb (pip install duckdb)
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable, List, Optional

try:
    import duckdb  # type: ignore
except Exception as e:  # pragma: no cover - import-time error handler
    raise ImportError(
        "DuckNo requires the 'duckdb' package. Install it with: pip install duckdb"
    ) from e


class DuckNo:
    """A tiny NoSQL-like key/value store built on DuckDB.

    Parameters
    ----------
    db_path: Optional[str]
        Path to the DuckDB database file. If None, defaults to './duckno.db'.
        If a directory path is provided, the database file 'duckno.db' will be
        created inside that directory. If you pass ':memory:' or set
        memory=True, an in-memory database is used.
    memory: bool
        If True, use an in-memory database regardless of db_path.
    table_name: str
        Name of the table to use/store data. Defaults to 'duckno_kv'.
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        *,
        memory: bool = False,
        table_name: str = "duckno_kv",
    ) -> None:
        self._table = table_name

        # Determine the database location
        if memory or db_path == ":memory:":
            database = ":memory:"
            self._db_file: Optional[Path] = None
        else:
            if db_path is None:
                # Default: current working directory
                db_file = Path(os.getcwd()) / "duckno.db"
            else:
                p = Path(db_path)
                if p.suffix == "":
                    # Likely a directory (or filename without extension). If it's a
                    # directory (existing or intended), place duckno.db inside it.
                    if p.exists() and p.is_dir():
                        p.mkdir(parents=True, exist_ok=True)
                        db_file = p / "duckno.db"
                    else:
                        # If it doesn't exist and has no suffix, treat it as a file name
                        # in the current directory.
                        if not p.parent.exists():
                            p.parent.mkdir(parents=True, exist_ok=True)
                        db_file = p if p.suffix in {".db", ".duckdb"} else Path(str(p) + ".db")
                else:
                    # Explicit file path
                    if not p.parent.exists():
                        p.parent.mkdir(parents=True, exist_ok=True)
                    db_file = p
            database = str(db_file)
            self._db_file = db_file

        # Connect and ensure schema
        self._conn = duckdb.connect(database=database, read_only=False)
        self._ensure_schema()

    # ---------------------------- context manager ---------------------------- #
    def __enter__(self) -> "DuckNo":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass

    # --------------------------------- API ---------------------------------- #
    def set(self, key: str, value: Any) -> None:
        """Store a JSON-serializable value under the given key.

        This operation is atomic via a transaction (DELETE + INSERT).
        """
        self._validate_key(key)
        try:
            payload = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        except TypeError as e:
            raise TypeError(
                "Value must be JSON-serializable. Consider converting to basic types."
            ) from e

        try:
            self._conn.execute("BEGIN TRANSACTION")
            self._conn.execute(f"DELETE FROM {self._table} WHERE k = ?", [key])
            self._conn.execute(
                f"INSERT INTO {self._table} (k, v) VALUES (?, ?)", [key, payload]
            )
            self._conn.execute("COMMIT")
        except Exception:
            try:
                self._conn.execute("ROLLBACK")
            except Exception:
                pass
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve the value for key or return default if not found."""
        self._validate_key(key)
        row = self._conn.execute(
            f"SELECT v FROM {self._table} WHERE k = ?", [key]
        ).fetchone()
        if row is None:
            return default
        return json.loads(row[0])

    def keys(self) -> List[str]:
        """Return all keys in ascending order."""
        rows = self._conn.execute(f"SELECT k FROM {self._table} ORDER BY k").fetchall()
        return [r[0] for r in rows]

    # ------------------------------ utilities ------------------------------- #
    @property
    def database_path(self) -> Optional[str]:
        """Path to the database file, or None if in-memory."""
        return str(self._db_file) if self._db_file is not None else None

    @classmethod
    def in_memory(cls, table_name: str = "duckno_kv") -> "DuckNo":
        """Convenience constructor for an in-memory database."""
        return cls(":memory:", memory=True, table_name=table_name)

    def _ensure_schema(self) -> None:
        # Store values as TEXT containing JSON for broad DuckDB compatibility
        self._conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self._table} (
                k TEXT PRIMARY KEY,
                v TEXT NOT NULL
            )
            """
        )

    @staticmethod
    def _validate_key(key: str) -> None:
        if not isinstance(key, str) or key == "":
            raise ValueError("key must be a non-empty string")


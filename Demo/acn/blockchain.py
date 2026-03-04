"""
Local Blockchain — SQLite-backed immutable ledger.

Each block contains:
  - block_hash  : SHA-256 of (prev_hash + timestamp + data_json)
  - prev_hash   : hash of previous block (chain integrity)
  - timestamp   : Unix timestamp
  - record_type : one of TASK_POSTED | ZK_VERIFIED | CHAMBER_RESULT |
                  CONTRACT_CREATED | DELIVERY | SETTLEMENT | GENESIS
  - data_json   : JSON payload for this record

All writes are append-only. No UPDATE or DELETE operations.
"""

import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


GENESIS_HASH = "0" * 64

DB_PATH = Path(__file__).parent.parent / "acn_chain.db"

# Record types
RT_GENESIS           = "GENESIS"
RT_TASK_POSTED       = "TASK_POSTED"
RT_ZK_VERIFIED       = "ZK_VERIFIED"
RT_CHAMBER_RESULT    = "CHAMBER_RESULT"
RT_CONTRACT_CREATED  = "CONTRACT_CREATED"
RT_DELIVERY          = "DELIVERY"
RT_SETTLEMENT        = "SETTLEMENT"


@dataclass
class Block:
    block_num:   int
    block_hash:  str
    prev_hash:   str
    timestamp:   float
    record_type: str
    data:        Dict[str, Any]

    def summary(self) -> str:
        """One-line human summary for display."""
        d = self.data
        if self.record_type == RT_GENESIS:
            return "ACN chain initialized"
        if self.record_type == RT_TASK_POSTED:
            return f"task={d.get('task_id','?')[:8]}  budget={d.get('budget')} ACN"
        if self.record_type == RT_ZK_VERIFIED:
            return (f"agent={d.get('agent_id','?')}  "
                    f"capability={d.get('capability_tag','?')}  valid={d.get('valid')}")
        if self.record_type == RT_CHAMBER_RESULT:
            return (f"agent={d.get('agent_id','?')}  "
                    f"confidence={d.get('confidence',0):.0%}  "
                    f"passed={d.get('passed')}")
        if self.record_type == RT_CONTRACT_CREATED:
            parties = d.get('parties', {})
            return f"parties={list(parties.keys())}  total={d.get('total_tokens')} ACN"
        if self.record_type == RT_DELIVERY:
            return (f"agent={d.get('agent_id','?')}  "
                    f"output_hash={d.get('output_hash','?')[:12]}...")
        if self.record_type == RT_SETTLEMENT:
            return f"settled  distributions={d.get('distributions')}"
        return str(d)[:60]


class Blockchain:
    """Append-only SQLite blockchain."""

    def __init__(self, db_path: Path = DB_PATH):
        self._db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()

    # ── Lifecycle ──────────────────────────────────────────────────────────

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS blocks (
                    block_num   INTEGER PRIMARY KEY,
                    block_hash  TEXT NOT NULL UNIQUE,
                    prev_hash   TEXT NOT NULL,
                    timestamp   REAL NOT NULL,
                    record_type TEXT NOT NULL,
                    data_json   TEXT NOT NULL
                )
            """)
            conn.commit()
        # Write genesis if empty
        if self._count() == 0:
            self._write_genesis()

    def _count(self) -> int:
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) FROM blocks").fetchone()
            return row[0]

    def _write_genesis(self):
        ts = time.time()
        data = {"message": "ACN Genesis Block — Agent Sovereignty Protocol"}
        data_json = json.dumps(data)
        raw = (GENESIS_HASH + str(ts) + data_json).encode()
        block_hash = hashlib.sha256(raw).hexdigest()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO blocks VALUES (?,?,?,?,?,?)",
                (0, block_hash, GENESIS_HASH, ts, RT_GENESIS, data_json),
            )
            conn.commit()

    # ── Public API ─────────────────────────────────────────────────────────

    def append(self, record_type: str, data: Dict[str, Any]) -> Block:
        """Append a new block. Returns the Block object."""
        with self._connect() as conn:
            last = conn.execute(
                "SELECT block_num, block_hash FROM blocks ORDER BY block_num DESC LIMIT 1"
            ).fetchone()
            prev_num = last["block_num"]
            prev_hash = last["block_hash"]

        block_num = prev_num + 1
        ts = time.time()
        data_json = json.dumps(data, default=str)
        raw = (prev_hash + str(ts) + data_json).encode()
        block_hash = hashlib.sha256(raw).hexdigest()

        with self._connect() as conn:
            conn.execute(
                "INSERT INTO blocks VALUES (?,?,?,?,?,?)",
                (block_num, block_hash, prev_hash, ts, record_type, data_json),
            )
            conn.commit()

        return Block(
            block_num=block_num,
            block_hash=block_hash,
            prev_hash=prev_hash,
            timestamp=ts,
            record_type=record_type,
            data=data,
        )

    def get_chain(self) -> List[Block]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM blocks ORDER BY block_num"
            ).fetchall()
        return [
            Block(
                block_num=r["block_num"],
                block_hash=r["block_hash"],
                prev_hash=r["prev_hash"],
                timestamp=r["timestamp"],
                record_type=r["record_type"],
                data=json.loads(r["data_json"]),
            )
            for r in rows
        ]

    def verify_integrity(self) -> bool:
        """Verify the hash chain is unbroken."""
        chain = self.get_chain()
        for i in range(1, len(chain)):
            prev = chain[i - 1]
            curr = chain[i]
            if curr.prev_hash != prev.block_hash:
                return False
        return True

    def destroy(self):
        """Remove the database file (for clean re-runs)."""
        if self._db_path.exists():
            self._db_path.unlink()

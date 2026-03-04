"""
Smart Contract — Escrow and Settlement

A SmartContract is immutable once created. It holds tokens in escrow and
releases them automatically when all deliveries are confirmed.

The contract records:
  - parties and their agreed token allocations
  - deliverable output hashes (filled as agents deliver)
  - final settlement record
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class ContractParty:
    agent_id:     str
    capability:   str
    token_amount: int
    delivered:    bool = False
    output_hash:  Optional[str] = None


class SmartContract:
    """
    Immutable once deployed (deploy() called).
    Simulates on-chain escrow with automatic settlement.
    """

    def __init__(
        self,
        task_id: str,
        initiator_id: str,
        total_tokens: int,
    ):
        self._task_id = task_id
        self._initiator_id = initiator_id
        self._total_tokens = total_tokens
        self._parties: Dict[str, ContractParty] = {}
        self._deployed = False
        self._settled = False
        self._deployed_at: Optional[float] = None
        self._settled_at: Optional[float] = None
        self._contract_id = self._compute_id()

    def _compute_id(self) -> str:
        raw = f"{self._task_id}{self._initiator_id}{self._total_tokens}{time.time()}"
        return "ctr-" + hashlib.sha256(raw.encode()).hexdigest()[:12]

    # ── Setup (before deploy) ──────────────────────────────────────────────

    def add_party(self, agent_id: str, capability: str, token_amount: int):
        if self._deployed:
            raise RuntimeError("Cannot modify a deployed contract")
        self._parties[agent_id] = ContractParty(
            agent_id=agent_id,
            capability=capability,
            token_amount=token_amount,
        )

    def deploy(self):
        """Lock the contract — no further modifications allowed."""
        if self._deployed:
            raise RuntimeError("Already deployed")
        total_allocated = sum(p.token_amount for p in self._parties.values())
        if total_allocated != self._total_tokens:
            raise ValueError(
                f"Allocated {total_allocated} != total {self._total_tokens}"
            )
        self._deployed = True
        self._deployed_at = time.time()

    # ── Execution (after deploy) ───────────────────────────────────────────

    def record_delivery(self, agent_id: str, output_hash: str):
        """Record that an agent has delivered their output."""
        if not self._deployed:
            raise RuntimeError("Contract not deployed")
        if self._settled:
            raise RuntimeError("Contract already settled")
        if agent_id not in self._parties:
            raise KeyError(f"Agent {agent_id} not in contract")
        party = self._parties[agent_id]
        party.delivered = True
        party.output_hash = output_hash

    def all_delivered(self) -> bool:
        return all(p.delivered for p in self._parties.values())

    def settle(self) -> Dict[str, int]:
        """
        Distribute tokens to all parties.
        Returns {agent_id: tokens_received}.
        """
        if self._settled:
            raise RuntimeError("Already settled")
        if not self.all_delivered():
            pending = [a for a, p in self._parties.items() if not p.delivered]
            raise RuntimeError(f"Not all delivered; pending: {pending}")
        distributions = {
            agent_id: party.token_amount
            for agent_id, party in self._parties.items()
        }
        self._settled = True
        self._settled_at = time.time()
        return distributions

    # ── Inspection ─────────────────────────────────────────────────────────

    @property
    def contract_id(self) -> str:
        return self._contract_id

    @property
    def task_id(self) -> str:
        return self._task_id

    @property
    def total_tokens(self) -> int:
        return self._total_tokens

    @property
    def parties(self) -> Dict[str, ContractParty]:
        return dict(self._parties)

    def to_dict(self) -> dict:
        return {
            "contract_id": self._contract_id,
            "task_id": self._task_id,
            "initiator": self._initiator_id,
            "total_tokens": self._total_tokens,
            "deployed": self._deployed,
            "settled": self._settled,
            "parties": {
                aid: {
                    "capability": p.capability,
                    "tokens": p.token_amount,
                    "delivered": p.delivered,
                    "output_hash": p.output_hash,
                }
                for aid, p in self._parties.items()
            },
        }

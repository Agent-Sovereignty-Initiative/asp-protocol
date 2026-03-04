"""
On-Chain Reputation System.

Reputation is derived entirely from delivery records on the blockchain.
It CANNOT be purchased, transferred, or faked — only earned through
real deliveries.

Score = base_score + sum(delivery_weight for each delivery)
      - sum(slash_amount for each missed/failed delivery)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ReputationRecord:
    agent_id:       str
    total_deliveries: int = 0
    successful:     int   = 0
    failed:         int   = 0
    stake_slashed:  float = 0.0
    stake_balance:  float = 100.0   # starting stake
    score:          float = 50.0    # 0–100

    def deliver_success(self, weight: float = 1.0):
        self.total_deliveries += 1
        self.successful += 1
        gain = min(weight * 5.0, 100.0 - self.score)
        self.score += gain

    def deliver_failure(self, slash: float = 10.0):
        self.total_deliveries += 1
        self.failed += 1
        self.stake_balance = max(0.0, self.stake_balance - slash)
        self.stake_slashed += slash
        self.score = max(0.0, self.score - 15.0)

    def can_accept_task(self, required_stake: float = 10.0) -> bool:
        return self.stake_balance >= required_stake

    def tier(self) -> str:
        if self.score >= 90:
            return "ELITE"
        if self.score >= 70:
            return "TRUSTED"
        if self.score >= 50:
            return "ESTABLISHED"
        if self.score >= 30:
            return "PROBATION"
        return "RESTRICTED"


class ReputationSystem:
    """In-memory reputation store (backed by blockchain in full impl)."""

    def __init__(self):
        self._records: Dict[str, ReputationRecord] = {}

    def _get_or_create(self, agent_id: str) -> ReputationRecord:
        if agent_id not in self._records:
            self._records[agent_id] = ReputationRecord(agent_id=agent_id)
        return self._records[agent_id]

    def get(self, agent_id: str) -> ReputationRecord:
        return self._get_or_create(agent_id)

    def record_delivery(self, agent_id: str, success: bool,
                        weight: float = 1.0, slash: float = 10.0):
        rec = self._get_or_create(agent_id)
        if success:
            rec.deliver_success(weight)
        else:
            rec.deliver_failure(slash)

    def can_participate(self, agent_id: str,
                        required_stake: float = 10.0) -> bool:
        return self._get_or_create(agent_id).can_accept_task(required_stake)

    def all_agents(self) -> List[ReputationRecord]:
        return list(self._records.values())

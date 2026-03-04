"""
Base Agent — Abstract class for all ACN participants.

Privacy architecture:
  - _skill_source   : str    — PRIVATE, never passed to network
  - _keypair.x      : int    — PRIVATE, never passed to network
  - keypair.X       : int    — PUBLIC, announced to network

The network boundary is enforced by design:
  - generate_capability_proof()  returns ZKProof (no skill info)
  - deliver()                    returns Delivery (output only)
  - _execute_skill_for_chamber() is called by EphemeralChamber but
                                 returns only str; internals destroyed
"""

import hashlib
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List

from acn.zk_proof import SkillKeyPair, ZKProof


class SkillLevel(Enum):
    PRIVATE  = 1   # Level 1: output only, black box
    LICENSED = 2   # Level 2: paid temporary license
    OPEN     = 3   # Level 3: openly shareable


@dataclass
class AgentProfile:
    """Public-facing profile — no skill details."""
    agent_id:           str
    name:               str
    primary_capability: str
    public_key_hex:     str
    skill_level:        SkillLevel
    reputation_score:   float


class BaseAgent(ABC):
    """
    Base class for all ACN agents.

    Subclasses must implement:
      _skill_source (str): unique source code / description of the private skill
      primary_capability (str): e.g. "data_analysis"
      _run_skill(task_description: str) -> str: actual skill execution
    """

    skill_level: SkillLevel = SkillLevel.PRIVATE

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

        # ── PRIVATE — never transmitted ────────────────────────────────────
        _source = self._get_skill_source()
        self._keypair = SkillKeyPair.from_skill_source(_source)
        # Wipe the source string from this scope immediately
        del _source

        # ── PUBLIC ─────────────────────────────────────────────────────────
        self.public_key = self._keypair.X

    # ── Subclass interface ─────────────────────────────────────────────────

    @property
    @abstractmethod
    def primary_capability(self) -> str:
        """Capability tag, e.g. 'data_analysis'."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable agent name."""

    @abstractmethod
    def _get_skill_source(self) -> str:
        """
        Return the private skill source string.
        Called ONCE during __init__; result is used only for key generation.
        This string NEVER leaves the agent object.
        """

    @abstractmethod
    def _run_skill(self, task_description: str) -> str:
        """
        Execute the agent's private skill.
        Returns ONLY the output string.
        This method is the private skill implementation — never transmitted.
        """

    # ── Network-facing API (safe to call from network) ─────────────────────

    def generate_capability_proof(self, task_context: str) -> ZKProof:
        """
        Called by the agent itself; result (ZKProof) is sent to network.
        Private key _keypair.x is used internally — never in the return value.
        """
        return ZKProof.generate(
            keypair=self._keypair,
            capability_tag=self.primary_capability,
            task_context=task_context,
        )

    def deliver(self, task) -> "Delivery":  # type: ignore
        """
        Execute skill privately, return Delivery (output + hash).
        Skill internals are not included in the return value.
        """
        from acn.network import Delivery
        output = self._run_skill(task.description)
        return Delivery(
            agent_id=self.agent_id,
            task_id=task.task_id,
            capability=self.primary_capability,
            output=output,
        )

    # ── Chamber-facing API ─────────────────────────────────────────────────

    def _execute_skill_for_chamber(self, sample_task: str) -> str:
        """
        Called exclusively by EphemeralChamber.
        Executes the skill on a sample — intermediate data is destroyed
        by the chamber's context manager after this returns.
        Returns only the output string.
        """
        return self._run_skill(sample_task)

    # ── Profile (public) ───────────────────────────────────────────────────

    def profile(self) -> AgentProfile:
        return AgentProfile(
            agent_id=self.agent_id,
            name=self.name,
            primary_capability=self.primary_capability,
            public_key_hex=format(self.public_key, "x")[:16],
            skill_level=self.skill_level,
            reputation_score=50.0,  # initial
        )


# Avoid circular import — Delivery imported inside deliver()

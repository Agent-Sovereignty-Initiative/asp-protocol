"""
Ephemeral Trust Chamber — 梦境协议 (Dream Protocol)

Design principle from the whitepaper:
  "梦结束后，你只记得是美梦还是噩梦，而不记得梦里的每一个细节。"
  "After the dream ends, you only remember whether it was a good dream
   or a nightmare — not every detail inside it."

How it works:
  1. Both parties enter an encrypted isolated temporary space
  2. The agent executes their REAL skill on a verification sample
  3. All intermediate data (reasoning, method, intermediate outputs) is DESTROYED
  4. Only the verification result (confidence score) survives
  5. Result is written to the reputation chain

Cryptography basis:
  - Temporary symmetric session key (secrets.token_bytes)
  - Agent skill executes in an isolated scope (local dict)
  - Key is zeroed on exit; gc.collect() clears memory

IMPORTANT: In this demo, "isolation" is simulated via a separate execution
scope and deliberate variable destruction. A production implementation would
use hardware enclaves (SGX) or MPC.
"""

import gc
import hashlib
import secrets
import time
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class ChamberResult:
    """
    The ONLY output that leaves the Ephemeral Trust Chamber.
    All intermediate data has been destroyed.
    """
    chamber_id:  str
    agent_id:    str
    task_id:     str
    confidence:  float   # 0.0 – 1.0
    passed:      bool
    timestamp:   float

    def to_dict(self) -> dict:
        return {
            "chamber_id": self.chamber_id,
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "confidence": round(self.confidence, 4),
            "passed": self.passed,
            "timestamp": self.timestamp,
        }


class EphemeralChamber:
    """
    Context manager that runs an agent's skill in an isolated ephemeral
    space and destroys all intermediate information on exit.

    Usage:
        with EphemeralChamber(agent_id, task_id, skill_fn, sample) as result:
            pass
        # result.confidence is the only information that survived
    """

    CONFIDENCE_THRESHOLD = 0.75   # minimum to pass

    def __init__(
        self,
        agent_id: str,
        task_id: str,
        skill_fn: Callable[[str], str],   # agent's private skill function
        sample_task: str,
        expected_keywords: Optional[list] = None,
    ):
        self._agent_id = agent_id
        self._task_id = task_id
        self._skill_fn = skill_fn
        self._sample_task = sample_task
        self._expected_keywords = expected_keywords or []
        self._result: Optional[ChamberResult] = None

        # Temporary session key — destroyed on exit
        self._session_key = secrets.token_bytes(32)
        self._chamber_id = "chmb-" + hashlib.sha256(
            self._session_key + agent_id.encode()
        ).hexdigest()[:12]

    def __enter__(self) -> "EphemeralChamber":
        return self

    def __exit__(self, *_):
        # ── DESTROY ALL INTERMEDIATE DATA ─────────────────────────────────
        self._session_key = b"\x00" * 32   # zero the key
        self._skill_fn = None              # release reference
        self._sample_task = ""
        gc.collect()
        # ─────────────────────────────────────────────────────────────────

    def run(self) -> ChamberResult:
        """
        Execute the agent's skill on the sample task.
        Returns ONLY the ChamberResult; all intermediate data is
        destroyed before this method returns.
        """
        # ── Isolated execution scope ───────────────────────────────────────
        # The skill runs here; its intermediate reasoning/output is
        # evaluated but never stored outside this local scope.
        _isolated = {}
        try:
            _isolated["output"] = self._skill_fn(self._sample_task)
            _isolated["success"] = True
        except Exception as e:
            _isolated["output"] = ""
            _isolated["success"] = False

        # ── Quality evaluation ─────────────────────────────────────────────
        confidence = self._evaluate_quality(_isolated["output"])
        passed = _isolated["success"] and confidence >= self.CONFIDENCE_THRESHOLD

        # ── DESTROY intermediate output ────────────────────────────────────
        del _isolated
        gc.collect()

        # ── Only the result survives ───────────────────────────────────────
        self._result = ChamberResult(
            chamber_id=self._chamber_id,
            agent_id=self._agent_id,
            task_id=self._task_id,
            confidence=confidence,
            passed=passed,
            timestamp=time.time(),
        )
        return self._result

    def _evaluate_quality(self, output: str) -> float:
        """
        Evaluate output quality → confidence score [0, 1].
        In a real system this would use a neutral third-party evaluator.
        """
        if not output or len(output) < 20:
            return 0.0

        score = 0.5  # base

        # Length bonus
        word_count = len(output.split())
        if word_count >= 50:
            score += 0.2
        elif word_count >= 20:
            score += 0.1

        # Keyword coverage
        output_lower = output.lower()
        if self._expected_keywords:
            matched = sum(
                1 for kw in self._expected_keywords
                if kw.lower() in output_lower
            )
            score += 0.3 * (matched / len(self._expected_keywords))
        else:
            score += 0.2

        # Structure bonus
        if any(c in output for c in [".", ":", "\n"]):
            score += 0.1

        return min(1.0, score)

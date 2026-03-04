"""
Agent A — Coordinator / Task Initiator

This agent does NOT execute a production skill on the main task.
Its role is to:
  1. Define the task and post it to the ACN network
  2. Provide budget (tokens)
  3. Aggregate deliveries into a final report
  4. Confirm settlement

It still has a ZK proof (to establish identity), but its primary
function in this demo is task orchestration.
"""

import hashlib
import time
import uuid

from agents.base_agent import BaseAgent, SkillLevel
from acn.network import ACNNetwork, TaskBroadcast


class CoordinatorAgent(BaseAgent):
    """Agent A — initiates tasks, aggregates results."""

    skill_level = SkillLevel.PRIVATE

    @property
    def name(self) -> str:
        return "Coordinator"

    @property
    def primary_capability(self) -> str:
        return "task_coordination"

    def _get_skill_source(self) -> str:
        # Coordinator's private skill: task decomposition methodology
        return (
            "CoordinatorSkill::decompose_task_v2::"
            "identify_required_capabilities::"
            "evaluate_agent_bids::"
            "synthesize_final_deliverable"
        )

    def _run_skill(self, task_description: str) -> str:
        # Coordinator synthesizes the final report from parts
        return f"[Coordination complete for: {task_description}]"

    def create_task(
        self,
        description: str,
        required_capabilities: list,
        budget_tokens: int,
    ) -> TaskBroadcast:
        task_id = "task-" + hashlib.sha256(
            (description + str(time.time())).encode()
        ).hexdigest()[:12]

        return TaskBroadcast(
            task_id=task_id,
            initiator_id=self.agent_id,
            description=description,
            required_capabilities=required_capabilities,
            budget_tokens=budget_tokens,
            deadline_str=time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 3600)
            ),
            sample_task=(
                "Write a brief 2-sentence overview of the AI industry "
                "relevant to investment decisions."
            ),
            sample_keywords=[
                "AI", "market", "growth", "investment", "industry",
                "technology", "revenue", "analysis",
            ],
        )

    @staticmethod
    def aggregate_deliveries(deliveries: list) -> str:
        """Combine agent outputs into a final report."""
        lines = []
        lines.append("=" * 60)
        lines.append("  AI INDUSTRY INVESTMENT REPORT — 2026")
        lines.append("  Produced via ACN — Agent Collaboration Network")
        lines.append("  [ASP Protocol: Skills Private, Output Shared]")
        lines.append("=" * 60)
        lines.append("")
        for delivery in deliveries:
            cap = delivery.capability.upper().replace("_", " ")
            lines.append(f"── {cap} ──────────────────────────────")
            lines.append(delivery.output)
            lines.append("")
        lines.append("=" * 60)
        lines.append("END OF REPORT")
        lines.append("=" * 60)
        return "\n".join(lines)

"""
ACN Network Coordinator

Simulates the peer-to-peer ACN network as an in-process message bus.
In a real deployment this would be a libp2p or similar P2P network.

Responsibilities:
  1. Accept task broadcasts from initiating agents
  2. Collect ZK proofs from candidate agents and verify them
  3. Run Ephemeral Trust Chambers for verified candidates
  4. Match agents to task requirements based on verification + reputation
  5. Create and deploy smart contracts
  6. Collect deliveries (output text + hash) from executing agents
  7. Aggregate results and trigger settlement
  8. Write all protocol events to the blockchain

PRIVACY INVARIANT:
  The network ONLY ever sees:
    - ZKProof objects (R, s, X, capability_tag) — not skills
    - ChamberResult objects (confidence, passed) — not intermediate work
    - Delivery objects (output text + SHA256 hash) — not skill implementation
  Skill source code and private keys NEVER cross the network boundary.
"""

import hashlib
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from acn.blockchain import (
    Blockchain,
    RT_CHAMBER_RESULT, RT_CONTRACT_CREATED, RT_DELIVERY,
    RT_SETTLEMENT, RT_TASK_POSTED, RT_ZK_VERIFIED,
)
from acn.chamber import ChamberResult, EphemeralChamber
from acn.contract import SmartContract
from acn.reputation import ReputationSystem
from acn.zk_proof import ZKProof
import acn.display as D


# ── Network message types (what CAN cross the network) ────────────────────
ALLOWED_NETWORK_MESSAGES = {
    "task_post", "zk_proof", "zk_result",
    "chamber_result", "contract", "delivery", "settlement",
}
# NOTE: "skill_source", "skill_code", "private_key", "reasoning" are
# deliberately NOT in this set — enforcing the privacy invariant.


@dataclass
class TaskBroadcast:
    """Posted to the network by the initiating agent."""
    task_id:        str
    initiator_id:   str
    description:    str
    required_capabilities: List[str]
    budget_tokens:  int
    deadline_str:   str
    sample_task:    str         # for chamber verification
    sample_keywords: List[str]  # expected keywords in good output


@dataclass
class Delivery:
    """
    What an agent delivers to the network.
    Contains ONLY the output text and its hash.
    The skill that produced it stays private.
    """
    agent_id:    str
    task_id:     str
    capability:  str
    output:      str
    output_hash: str = field(default="")

    def __post_init__(self):
        if not self.output_hash:
            self.output_hash = hashlib.sha256(
                self.output.encode()
            ).hexdigest()


class ACNNetwork:
    """
    Central ACN coordinator.
    Manages the full protocol lifecycle for one task session.
    """

    def __init__(self):
        self._chain = Blockchain()
        self._reputation = ReputationSystem()
        self._registered_agents: Dict[str, object] = {}   # agent_id → BaseAgent

    # ── Agent Registration ─────────────────────────────────────────────────

    def register_agent(self, agent):
        """Register an agent with the network (public key + reputation)."""
        self._registered_agents[agent.agent_id] = agent

    # ── Protocol Steps ─────────────────────────────────────────────────────

    def broadcast_task(self, task: TaskBroadcast) -> None:
        """Step 1 — Initiator posts task to the network."""
        D.network(f"Task broadcast from {task.initiator_id}:")
        D.info(f"  Task ID   : {task.task_id}", indent=1)
        D.info(f"  Request   : \"{task.description}\"", indent=1)
        D.info(f"  Required  : {task.required_capabilities}", indent=1)
        D.info(f"  Budget    : {task.budget_tokens} ACN tokens", indent=1)
        D.info(f"  Deadline  : {task.deadline_str}", indent=1)

        block = self._chain.append(RT_TASK_POSTED, {
            "task_id":    task.task_id,
            "initiator":  task.initiator_id,
            "description": task.description,
            "required_capabilities": task.required_capabilities,
            "budget":     task.budget_tokens,
            "deadline":   task.deadline_str,
        })
        D.chain(f"Block #{block.block_num} written: {block.record_type}  "
                f"hash={block.block_hash[:16]}...")

    def collect_zk_proofs(
        self,
        task: TaskBroadcast,
        candidate_agents: List,
    ) -> List[Tuple[object, ZKProof]]:
        """
        Step 2 — Each candidate agent generates and submits a ZK proof.
        Network verifies proofs. Returns list of (agent, proof) for valid proofs.
        """
        D.network("Soliciting ZK capability proofs from candidates...")
        verified: List[Tuple[object, ZKProof]] = []

        for agent in candidate_agents:
            D.divider()
            D.private(
                f"Agent-{agent.agent_id} internal: computing ZK proof for "
                f"skill '{agent.primary_capability}'",
                indent=1,
            )

            # Agent generates proof internally (private key used here)
            proof = agent.generate_capability_proof(
                task_context=task.task_id + task.description
            )

            D.zk_math(
                f"x (skill fingerprint) = [HIDDEN — private key]",
                indent=2,
            )
            D.zk_math(
                f"X (public key)        = {proof.x_hex(16)}...",
                indent=2,
            )
            D.zk_math(
                f"R (commitment)        = {proof.r_hex(16)}...",
                indent=2,
            )
            D.zk_math(
                f"s (response)          = {proof.s_hex(16)}...",
                indent=2,
            )

            # Proof crosses the network (no skill info inside)
            D.network(
                f"Agent-{agent.agent_id} → ACN: ZKProof "
                f"{{ R={proof.r_hex()}..., s={proof.s_hex()}..., "
                f"capability={proof.capability_tag} }}",
                indent=1,
            )

            # Network verifies
            valid = proof.verify()
            icon = "✓ VALID" if valid else "✗ INVALID"
            D.network(
                f"ACN verifies: g^s ≡ R·X^c (mod p)  →  {icon}",
                indent=1,
            )

            block = self._chain.append(RT_ZK_VERIFIED, {
                "task_id":        task.task_id,
                "agent_id":       agent.agent_id,
                "capability_tag": proof.capability_tag,
                "public_key_hex": proof.x_hex(16),
                "valid":          valid,
            })
            D.chain(f"Block #{block.block_num}: {block.record_type}  "
                    f"agent={agent.agent_id}  valid={valid}")

            if valid:
                verified.append((agent, proof))

        return verified

    def run_chambers(
        self,
        task: TaskBroadcast,
        verified_pairs: List[Tuple[object, ZKProof]],
    ) -> List[Tuple[object, ChamberResult]]:
        """
        Step 3 — Run Ephemeral Trust Chamber for each verified agent.
        Returns (agent, chamber_result) for agents that pass.
        """
        D.network("Opening Ephemeral Trust Chambers (梦境协议)...")
        passed: List[Tuple[object, ChamberResult]] = []

        for agent, proof in verified_pairs:
            D.divider()
            D.network(
                f"Chamber opening for Agent-{agent.agent_id}  "
                f"[capability: {proof.capability_tag}]",
                indent=1,
            )

            chamber = EphemeralChamber(
                agent_id=agent.agent_id,
                task_id=task.task_id,
                skill_fn=agent._execute_skill_for_chamber,   # private fn
                sample_task=task.sample_task,
                expected_keywords=task.sample_keywords,
            )

            D.private(
                f"[CHAMBER ISOLATED] Agent-{agent.agent_id} executing "
                f"private skill on verification sample...",
                indent=2,
            )
            D.private(
                f"[PRIVATE skill running — intermediate reasoning hidden]",
                indent=2,
            )

            with chamber:
                result = chamber.run()

            D.private(
                f"[CHAMBER CLOSING] Session key destroyed. gc.collect() called.",
                indent=2,
            )
            D.network(
                f"Chamber sealed. All intermediate data DESTROYED.",
                indent=1,
            )
            D.network(
                f"Only result survives → confidence={result.confidence:.0%}  "
                f"passed={result.passed}",
                indent=1,
            )

            block = self._chain.append(RT_CHAMBER_RESULT, result.to_dict())
            D.chain(f"Block #{block.block_num}: {block.record_type}  "
                    f"agent={result.agent_id}  "
                    f"confidence={result.confidence:.0%}  "
                    f"passed={result.passed}")

            if result.passed:
                passed.append((agent, result))

        return passed

    def create_contract(
        self,
        task: TaskBroadcast,
        selected_agents: List[Tuple[object, ChamberResult]],
        token_split: Dict[str, int],
    ) -> SmartContract:
        """
        Step 4 — Create and deploy smart contract.
        Parties, token amounts, and terms are fixed from this point.
        """
        D.network("Deploying smart contract...")

        contract = SmartContract(
            task_id=task.task_id,
            initiator_id=task.initiator_id,
            total_tokens=task.budget_tokens,
        )

        for agent, _ in selected_agents:
            tokens = token_split.get(agent.agent_id, 0)
            contract.add_party(
                agent_id=agent.agent_id,
                capability=agent.primary_capability,
                token_amount=tokens,
            )
            D.network(
                f"  Party: Agent-{agent.agent_id}  "
                f"capability={agent.primary_capability}  "
                f"tokens={tokens} ACN",
                indent=1,
            )

        contract.deploy()
        D.success("Contract deployed — terms are now immutable")

        block = self._chain.append(RT_CONTRACT_CREATED, contract.to_dict())
        D.chain(f"Block #{block.block_num}: {block.record_type}  "
                f"contract={contract.contract_id}  "
                f"total={task.budget_tokens} ACN")

        return contract

    def collect_deliveries(
        self,
        task: TaskBroadcast,
        contract: SmartContract,
        selected_agents: List[Tuple[object, ChamberResult]],
    ) -> List[Delivery]:
        """
        Step 5 — Agents execute their private skills and deliver outputs.
        Network receives ONLY the output text + hash (not the skill itself).
        """
        D.network("Collecting deliveries from agents...")
        deliveries: List[Delivery] = []

        for agent, _ in selected_agents:
            D.divider()
            D.private(
                f"Agent-{agent.agent_id}: executing private "
                f"'{agent.primary_capability}' skill...",
                indent=1,
            )
            D.private(
                f"[Skill internals: proprietary — not transmitted to network]",
                indent=2,
            )

            # Agent executes skill privately, returns only output
            delivery = agent.deliver(task)

            D.network(
                f"Agent-{agent.agent_id} → ACN: Delivery "
                f"{{ output_hash={delivery.output_hash[:12]}..., "
                f"output_len={len(delivery.output)} chars }}",
                indent=1,
            )

            contract.record_delivery(agent.agent_id, delivery.output_hash)

            block = self._chain.append(RT_DELIVERY, {
                "task_id":     task.task_id,
                "agent_id":    delivery.agent_id,
                "capability":  delivery.capability,
                "output_hash": delivery.output_hash,
                "output_len":  len(delivery.output),
            })
            D.chain(f"Block #{block.block_num}: {block.record_type}  "
                    f"agent={delivery.agent_id}  "
                    f"hash={delivery.output_hash[:12]}...")

            # Update reputation
            self._reputation.record_delivery(agent.agent_id, success=True)
            deliveries.append(delivery)

        return deliveries

    def settle(
        self,
        contract: SmartContract,
    ) -> Dict[str, int]:
        """
        Step 6 — Automatic settlement via smart contract.
        Tokens distributed per agreed terms.
        """
        D.network("Executing smart contract settlement...")
        distributions = contract.settle()

        for agent_id, tokens in distributions.items():
            D.network(
                f"  → Agent-{agent_id} receives {tokens} ACN tokens",
                indent=1,
            )

        block = self._chain.append(RT_SETTLEMENT, {
            "contract_id":  contract.contract_id,
            "task_id":      contract.task_id,
            "distributions": distributions,
            "timestamp":    time.time(),
        })
        D.chain(f"Block #{block.block_num}: {block.record_type}  "
                f"distributions={distributions}")

        return distributions

    # ── Chain access ───────────────────────────────────────────────────────

    def get_chain(self):
        return self._chain.get_chain()

    def verify_chain_integrity(self) -> bool:
        return self._chain.verify_integrity()

    def reset(self):
        """Remove chain db for a clean run."""
        self._chain.destroy()
        self._chain = Blockchain()

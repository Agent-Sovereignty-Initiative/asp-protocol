#!/usr/bin/env python3
"""
ACN Demo — Agent Collaboration Network
Based on ASP (Agent Sovereignty Protocol)

Run:
    python3 run_demo.py           # full demo with chain display
    python3 run_demo.py --slow    # dramatic pacing
    python3 run_demo.py --no-color# plain text (for piping)
    python3 run_demo.py --verify  # verify chain integrity only

What this demo proves:
  1. Agents prove capability via ZK proofs (Schnorr) — skills never exposed
  2. Ephemeral Trust Chamber verifies quality — intermediate data destroyed
  3. Agents deliver outputs only — skill implementations stay private
  4. Every protocol event is written to an immutable local blockchain (SQLite)
  5. Smart contract distributes tokens automatically on settlement
"""

import sys
import os
import time

# ── Path setup ─────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Color flag ─────────────────────────────────────────────────────────────
if "--no-color" in sys.argv:
    # Monkey-patch display to strip ANSI
    import acn.display as _D
    _D.RESET = _D.BOLD = _D.DIM = ""
    _D.BLUE = _D.YELLOW = _D.GREEN = _D.RED = ""
    _D.CYAN = _D.MAGENTA = _D.WHITE = _D.GRAY = ""

if "--slow" in sys.argv:
    import acn.display as _D
    _D.SLOW = True

import acn.display as D
from acn.network import ACNNetwork
from acn.blockchain import DB_PATH

from agents.coordinator       import CoordinatorAgent
from agents.data_analyst      import DataAnalystAgent
from agents.writer            import WriterAgent
from agents.financial_analyst import FinancialAnalystAgent
from agents.researcher        import ResearcherAgent


# ── Verify-only mode ───────────────────────────────────────────────────────
if "--verify" in sys.argv:
    from acn.blockchain import Blockchain
    chain = Blockchain()
    ok = chain.verify_integrity()
    blocks = chain.get_chain()
    print(f"\nChain integrity: {'✓ VALID' if ok else '✗ BROKEN'}")
    print(f"Total blocks   : {len(blocks)}")
    for b in blocks:
        print(f"  #{b.block_num:02d}  {b.record_type:<22}  {b.block_hash[:16]}...")
    sys.exit(0 if ok else 1)


def run_demo():
    # ── Clean slate ────────────────────────────────────────────────────────
    if DB_PATH.exists():
        DB_PATH.unlink()

    D.banner("ACN — Agent Collaboration Network Demo")
    D.info("Based on ASP (Agent Sovereignty Protocol)")
    D.info("「你的 Agent，你的技能，你的主权。」")
    D.info("")
    D.info("Color legend:")
    D.network("= Network / Protocol layer (public)")
    D.private("= Agent-internal / private (NEVER transmitted)")
    D.chain("= Blockchain write (immutable)")
    D.zk_math("= ZK cryptographic computation", indent=0)
    print()

    # ── Instantiate agents ─────────────────────────────────────────────────
    coordinator = CoordinatorAgent("A")
    data_analyst = DataAnalystAgent("B")
    writer       = WriterAgent("C")
    financial    = FinancialAnalystAgent("D")
    researcher   = ResearcherAgent("E")

    candidate_agents = [data_analyst, writer, financial, researcher]

    # ── Instantiate network ────────────────────────────────────────────────
    network = ACNNetwork()
    for agent in [coordinator] + candidate_agents:
        network.register_agent(agent)

    # ══════════════════════════════════════════════════════════════════════
    # STEP 1 — Task Broadcast
    # ══════════════════════════════════════════════════════════════════════
    D.step(1, "Task Initiated — Agent-A broadcasts to ACN network")

    task = coordinator.create_task(
        description="AI Industry Investment Report — 2026",
        required_capabilities=[
            "data_analysis", "financial_modeling", "writing", "research"
        ],
        budget_tokens=100,
    )
    network.broadcast_task(task)
    time.sleep(0.3)

    # ══════════════════════════════════════════════════════════════════════
    # STEP 2 — ZK Capability Proofs
    # ══════════════════════════════════════════════════════════════════════
    D.step(2, "ZK Capability Proofs — Agents prove skills without exposing them")
    D.info("Each agent computes a Schnorr ZK proof (Fiat-Shamir heuristic).")
    D.info("Network verifies: g^s ≡ R·X^c (mod p)")
    D.info("The private skill fingerprint x is NEVER transmitted.")
    print()

    verified_pairs = network.collect_zk_proofs(task, candidate_agents)

    D.divider("═")
    D.success(f"ZK verification complete: {len(verified_pairs)}/{len(candidate_agents)} agents verified")
    time.sleep(0.2)

    # ══════════════════════════════════════════════════════════════════════
    # STEP 3 — Ephemeral Trust Chambers
    # ══════════════════════════════════════════════════════════════════════
    D.step(3, "Ephemeral Trust Chambers — 梦境协议 (Dream Protocol)")
    D.info("Each verified agent enters an isolated chamber to demonstrate skill.")
    D.info("After the chamber closes, ALL intermediate data is DESTROYED.")
    D.info("Only the confidence score survives and is written to chain.")
    print()

    passed_pairs = network.run_chambers(task, verified_pairs)

    D.divider("═")
    D.success(
        f"Chamber phase complete: {len(passed_pairs)}/{len(verified_pairs)} agents passed "
        f"(threshold: {int(100 * 0.75)}%)"
    )
    time.sleep(0.2)

    # ══════════════════════════════════════════════════════════════════════
    # STEP 4 — Smart Contract
    # ══════════════════════════════════════════════════════════════════════
    D.step(4, "Smart Contract — Immutable terms locked on-chain")

    # Token split: proportional allocation
    agent_ids = [agent.agent_id for agent, _ in passed_pairs]
    n = len(agent_ids)
    base = task.budget_tokens // n
    remainder = task.budget_tokens - base * n

    token_split = {aid: base for aid in agent_ids}
    # Give remainder to first agent
    if agent_ids:
        token_split[agent_ids[0]] += remainder

    contract = network.create_contract(task, passed_pairs, token_split)
    time.sleep(0.2)

    # ══════════════════════════════════════════════════════════════════════
    # STEP 5 — Skill Execution & Delivery
    # ══════════════════════════════════════════════════════════════════════
    D.step(5, "Skill Execution — Agents deliver outputs (Skills NEVER transmitted)")
    D.info("Each agent runs their private skill internally.")
    D.info("Only the OUTPUT TEXT and its SHA-256 hash cross the network.")
    D.info("Skill source code, methodology, intermediate reasoning: all PRIVATE.")
    print()

    deliveries = network.collect_deliveries(task, contract, passed_pairs)

    D.divider("═")
    D.success(f"All deliveries received: {len(deliveries)} outputs")
    time.sleep(0.2)

    # ══════════════════════════════════════════════════════════════════════
    # STEP 6 — Settlement
    # ══════════════════════════════════════════════════════════════════════
    D.step(6, "Automatic Settlement — Smart contract distributes tokens")

    distributions = network.settle(contract)

    D.divider("═")
    D.success("Settlement complete — tokens distributed per contract terms")
    time.sleep(0.2)

    # ══════════════════════════════════════════════════════════════════════
    # FINAL REPORT
    # ══════════════════════════════════════════════════════════════════════
    D.banner("FINAL COLLABORATIVE REPORT")

    final_report = coordinator.aggregate_deliveries(deliveries)
    print(final_report)

    # ══════════════════════════════════════════════════════════════════════
    # BLOCKCHAIN LEDGER DUMP
    # ══════════════════════════════════════════════════════════════════════
    D.banner("ON-CHAIN DELIVERY RECORD")

    chain = network.get_chain()
    integrity_ok = network.verify_chain_integrity()

    D.info(f"Chain file  : {DB_PATH}")
    D.info(f"Total blocks: {len(chain)}")
    D.info(
        f"Integrity   : {'✓ VALID — hash chain unbroken' if integrity_ok else '✗ BROKEN'}"
    )
    print()

    for block in chain:
        D.block_row(
            block.block_num,
            block.record_type,
            block.block_hash,
            block.summary(),
        )

    # ══════════════════════════════════════════════════════════════════════
    # PRIVACY SUMMARY
    # ══════════════════════════════════════════════════════════════════════
    D.banner("ASP PRIVACY GUARANTEE SUMMARY")

    rows = [
        ("Task description",          "Agent-A → Network",    "✓ PUBLIC"),
        ("ZK Proof (R, s, X)",        "Agents → Network",     "✓ PUBLIC"),
        ("Skill private key (x)",     "Agent internal",        "🔒 PRIVATE"),
        ("Skill source code",         "Agent internal",        "🔒 PRIVATE"),
        ("Chamber intermediate data", "Destroyed on exit",     "🔒 DESTROYED"),
        ("Chamber confidence score",  "Chamber → Chain",       "✓ PUBLIC"),
        ("Delivery output text",      "Agents → Network",      "✓ PUBLIC"),
        ("Skill methodology",         "Agent internal",        "🔒 PRIVATE"),
        ("Output hash (SHA-256)",     "Contract → Chain",      "✓ PUBLIC"),
        ("Token settlement",          "Contract → Chain",      "✓ PUBLIC"),
    ]

    print(f"  {'Item':<32} {'Flow':<28} {'Status'}")
    print(f"  {'─'*32} {'─'*28} {'─'*12}")
    for item, flow, status in rows:
        color = D.GREEN if "PUBLIC" in status else (
            D.RED if "DESTROYED" in status else D.YELLOW
        )
        print(f"  {D.WHITE}{item:<32}{D.RESET} "
              f"{D.GRAY}{flow:<28}{D.RESET} "
              f"{color}{status}{D.RESET}")

    print()
    D.info("「协作不需要透明，它只需要可信。」")
    D.info("  Collaboration does not require transparency — only trust.")
    D.info("")
    D.info(f"Blockchain persisted at: {DB_PATH}")
    D.info(f"Verify anytime with:     python3 run_demo.py --verify")
    D.info(f"Inspect raw chain:       sqlite3 acn_chain.db 'SELECT * FROM blocks'")
    print()


if __name__ == "__main__":
    run_demo()

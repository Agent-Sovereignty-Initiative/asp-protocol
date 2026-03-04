"""
Agent D — Financial Analyst

Private Skill: Financial Modeling & Valuation Analysis

Specializes in DCF models, comparable company analysis, and
sector-specific valuation frameworks for AI companies. Modeling
methodology, discount rate assumptions, and terminal value
frameworks are private.
"""

from agents.base_agent import BaseAgent, SkillLevel


class FinancialAnalystAgent(BaseAgent):
    """Agent D — financial modeling and valuation analysis."""

    skill_level = SkillLevel.PRIVATE

    @property
    def name(self) -> str:
        return "FinancialAnalyst"

    @property
    def primary_capability(self) -> str:
        return "financial_modeling"

    def _get_skill_source(self) -> str:
        return (
            "FinancialAnalystSkill::v4.0.1::"
            "dcf_variant_2024_ai_sector::"
            "comp_normalization_methodology::"
            "terminal_growth_bayesian_prior::"
            "scenario_weighting_framework::"
            "PRIVATE_DO_NOT_DISTRIBUTE"
        )

    def _run_skill(self, task_description: str) -> str:
        """
        Execute private financial modeling skill.
        DCF model structure, comparable selection criteria, and
        valuation multiples calibration remain private.
        """
        # ── PRIVATE SKILL EXECUTION ────────────────────────────────────────
        output = """Financial Analysis & Valuation Framework — AI Sector (2026)

Sector Valuation Summary (Comparable Company Analysis):
┌─────────────────────────┬────────┬────────┬────────┬────────┐
│ Company                 │ EV/Rev │  P/E   │ EV/EBITDA│ PEG  │
├─────────────────────────┼────────┼────────┼────────┼────────┤
│ NVIDIA (compute)        │  18.4× │  42.1× │  35.2× │  0.8  │
│ Alphabet (platform)     │   6.2× │  22.8× │  18.4× │  1.1  │
│ Microsoft (enterprise)  │   9.1× │  31.5× │  24.7× │  1.4  │
│ Anthropic (pure-play)*  │  45.0× │   N/M  │   N/M  │  N/M  │
│ Sector Median           │  12.3× │  31.5× │  24.7× │  1.1  │
└─────────────────────────┴────────┴────────┴────────┴────────┘
  * Private, estimated based on latest funding round ($40B valuation)

DCF Scenario Analysis (5-Year Horizon):
  Bull Case  (30% prob): AI adoption outpaces forecasts
    → IRR: 34–41%  |  Revenue CAGR: 31%  |  Target multiple: 15× rev
  Base Case  (50% prob): Consensus adoption trajectory
    → IRR: 18–24%  |  Revenue CAGR: 24%  |  Target multiple: 11× rev
  Bear Case  (20% prob): Regulatory shock + demand disappointment
    → IRR:  4–9%   |  Revenue CAGR: 12%  |  Target multiple:  6× rev

Weighted Average Expected Return: 22.4% (12-month horizon)

Key Financial Metrics to Monitor:
  • GPU allocation as leading indicator (NVIDIA order backlog)
  • Enterprise contract duration (longer = stickier, better visibility)
  • Gross margin trajectory for inference-heavy business models
  • R&D intensity vs. revenue — declining ratio signals maturation
  • Agent API call volume as proxy for agentic economy penetration

Capital Allocation Signals:
  Q1 2026 CapEx across hyperscalers: $89B (record)
  → 68% allocated to AI infrastructure (GPUs, cooling, networking)
  → Signals multi-year conviction from capital allocators

Bottom Line: Valuation premium is justified by growth rate; the
sector trades at 1.1× PEG on forward estimates — not stretched."""

        return output

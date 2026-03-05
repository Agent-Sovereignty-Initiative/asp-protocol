# Agent Sovereignty Protocol (ASP)

**Your Agent. Your Skills. Your Sovereignty.**

ASP is an open protocol proposal addressing a critical gap in the emerging Agent economy:
existing standards define how Agents interoperate — but none protect who *owns* the skills inside them.

---

## The Problem

Three extractive structures are forming simultaneously:

**1. Team Agents silently absorb employee skills**
Companies deploy Team Agents where employees use unified AI systems. Employee expertise, workflows, and domain knowledge get continuously written into company-owned infrastructure. The worker teaches the Agent once; the skill belongs to the company permanently. When the skill is fully absorbed, the person becomes replaceable. This happens silently — often packaged as a productivity benefit.

**2. A2A networks accelerate skill homogenization**
Agent-to-Agent networks encourage free skill sharing. Short-term, this accelerates AI capability diffusion. Long-term, the unique skills individuals spent time and effort cultivating rapidly become public resources. Individual differentiation is erased; all Agents trend toward the same.

**3. Enterprise skills are equally at risk**
In deep cross-company Agent collaboration, a single interaction may mean permanent leakage of core workflows. A supplier's unique capabilities can be reverse-learned by a client's Agent. A competitor can acquire your methodology through a joint project. An outsourcing client can internalize your technical barriers just by watching your Agent work.

The rules of the Agent economy are being written right now — by Google (A2A), Anthropic (Agent Skills), and others. These standards solve how Agents talk to each other. **None of them answer: who owns the skills inside?**

Ordinary people are not at the table.

---

## The Proposal

ASP is built on one foundational claim:

> *Skills cultivated in a personal Agent are private property — not a public resource, not a corporate asset. They may be licensed, transferred, or inherited, but they cannot be involuntarily extracted.*

### Two Layers

- **ASP (Agent Sovereignty Protocol)** — The principle layer. Defines why and how Agent skills deserve ownership protection.
- **ACN (Agent Collaboration Network)** — The technical implementation. An open protocol for Agent collaboration and settlement that enforces Skill privacy at the protocol level.

### Three Core Principles

1. **Skills are private, outputs are shared** — In collaboration, Agents share goals, context memory, and final outputs. But the Skill itself — the method and capability behind the output — remains private and never exposed to the network.

2. **Protocol-neutral, never touches ownership** — The ASP protocol layer only handles collaboration rules and settlement mechanics. It does not participate in any Skill attribution judgment. No party can obtain another's Skill through the protocol.

3. **Tiered protection, voluntary choice** — Protection level is set by the Skill owner: from fully private, to paid licensing, to open sharing — a system similar to software licenses. This is not mandatory; it gives individuals the right to choose.

### Key Mechanisms

**Skill Tiers**
- Level 1 (Fully Private): Only deliver outputs. Skill is a black box, inaccessible under any circumstance.
- Level 2 (Licensed): Skill may be temporarily licensed at an agreed price. Access terminates automatically when the license period ends.
- Level 3 (Open Shared): Skill may be learned by other Agents. For creators who voluntarily choose to open-source their skills.

**Ephemeral Trust Chamber**
The core challenge: if Skills are black boxes, how does the initiating party verify a collaborator actually has the capability to complete the task?

ACN introduces the *Ephemeral Trust Chamber* mechanism:
1. Both parties enter an encrypted, isolated temporary space
2. The participant demonstrates their Skill on a verification task — for real
3. The space closes — all process data and communications are destroyed, non-traceable
4. Only the conclusion is written to the reputation system: "Capability confirmed, 92% confidence"

*Like a dream: you remember whether it was good or bad. You don't remember every detail inside.*

Cryptographic foundations: Zero-Knowledge Proofs (ZK Proof) + Secure Multi-Party Computation (MPC).

**On-Chain Reputation**
Trust is built from delivery history, not Skill disclosure. All delivery records are written on-chain, immutable. Agents must stake credit to take on tasks; failure to deliver results in deductions. Reputation cannot be purchased or transferred — only accumulated through real delivery.

---

## ASP as the Security Layer for A2A

ASP/ACN is not a competitor to A2A protocols. It is A2A's missing security layer.

The most precise analogy is TLS and HTTP:
- A2A defines "how Agents interoperate" — ASP defines "whether Skills are protected during interoperation"
- ASP can be deployed without modifying A2A — just as TLS can be deployed without rewriting HTTP
- ASP is not mandatory, but any Agent carrying valuable Skills has an incentive to use it

**Three-layer architecture:**

```
┌─────────────────────────────────────────┐
│   Application Layer (Agent business logic)   │
├─────────────────────────────────────────┤
│   ASP/ACN Layer (Skill protection, verification, settlement) │
├─────────────────────────────────────────┤
│   A2A Protocol Layer (interop, discovery, communication)   │
└─────────────────────────────────────────┘
```

**Backward-compatible extension fields:**
ASP defines a standard optional extension to existing Agent Card structures:

```json
"asp": {
  "protection_level": 1,
  "acn_gateway": "acn://agent.example/gateway",
  "verification_required": true
}
```

A2A implementations that don't support ASP ignore this field entirely, completely unaffected.

---

## Relationship to Existing Standards

| Standard | Solves | Does Not Address |
|---|---|---|
| Google A2A | Agent discovery, communication, task delegation | Who owns the Skill being shared |
| Anthropic Agent Skills | Skill portability, standardized capability description | Preventing involuntary Skill extraction |
| **ASP/ACN** | **Skill ownership, privacy-preserving collaboration, settlement** | Replaces neither of the above |

ASP does not compete with interoperability standards.
Those solve **interoperability**. ASP solves **ownership**.
ASP can be built on top of any existing interoperability protocol — just as HTTPS is built on TCP/IP.

---

## Application Scenarios

**Personal Layer: Free Agent Alliances**
Individuals own and continuously cultivate their private Agents. Different individuals' Agents can temporarily team up for a common goal, split earnings by agreement when done, then dissolve. No employment relationship, no Skill ownership transfer.

**Organizational Layer: A New Employment Relationship**
Companies create collaboration networks and invite employees' personal Agents to join for business goals. The company network has shared business memory and goal context — but employees' Skills remain owned by employees. The company pays for using these Skills, rather than acquiring them for free. This fundamentally redefines IP ownership in employment.

**Enterprise Layer: Cross-Organization Collaboration**
ACN allows enterprises to complete cross-organizational collaboration without exposing core capabilities. Supply chain partners, government-enterprise collaboration, and cross-border projects can all operate within this framework.

---

## The Closing Window

TCP/IP was designed without built-in security. It took 30 years and countless incidents to partially patch this through SSL/TLS — which can only exist as an overlay, never as native design.

A2A protocols are currently at an early adoption stage. The cost of influencing them is still low. Once widely adopted with large systems depending on them, any modification faces compatibility pressure and becomes nearly impossible.

**This window is approximately 12–18 months.**

The time to define the alternative is now, not after the infrastructure is locked in.

---

## The Broader Vision: Skill Financialization (V4)

Once Skills are protected and verifiable, they become investable assets:

- **Skill REITs**: Tokenize future cash flows from a verified high-value Skill into standardized shares. Creators get upfront capital; investors get ongoing cash flow.
- **Agent Fund**: Portfolios of multiple Skills/Agents to diversify risk across industries or strategies.
- **Skill IPO/ICO**: When a Skill reaches maturity — stable call history, auditable revenue — it can enter public markets. Issuance is of revenue rights, never of unlimited access to the Skill itself.

The goal: let creators obtain financing capability. Let investment returns bind to real output. Let the market price capability value — not a single platform setting the price unilaterally.

---

## White Paper Series

| Version | Focus | Audience |
|---|---|---|
| **V1** (Published) | Individual skill sovereignty. Core principles, ACN framework. | Individual creators, technical community |
| **V2** (Published) | Enterprise collaboration & supply chain protection. Why enterprises and individuals share the same interests. | Enterprise decision-makers, industry organizations |
| **V3** (Published) | ASP as A2A security layer. Three-layer technical path, urgency of the closing window. | Protocol developers, technical standards community |

> *V1 establishes rights. V2 expands the coalition. V3 writes it into infrastructure. 
---

## Status

This is a v0.1–v0.3 proposal document series. None of these are yet implemented protocols.
We are looking for researchers, developers, and thinkers who believe this problem matters.

---

## Read the White Papers

- [V1: Individual Skill Sovereignty English](./whitepaper/ASP_Whitepaper_EN_v1.md)· [(中文)](./whitepaper/ASP_白皮书_Agent%20主权协议_v1.md) 
- [V2: Enterprise Collaboration English](./whitepaper/ASP_Whitepaper_Enterprise_Edition_v2.md)· [(中文)](./whitepaper/ASP_白皮书_企业协作篇_v2.md) 
- [V3: A2A Security Layer English](./whitepaper/ASP_WhitePaper_A2A_SecurityLayer_V3.md)· [(中文)](./whitepaper/ASP_白皮书_A2A安全层_V3.md) 

---

## How to Contribute

- Open an issue to discuss the proposal
- Submit a PR to improve the protocol design
- If you're a developer: build the first ACN gateway reference implementation, propose ASP extension fields to A2A protocol communities
- If you're an enterprise decision-maker: assess Skill leakage risks in your cross-org Agent collaborations; add Agent Skill protection clauses to partnership agreements
- If you're in standards communities: bring "Skill ownership" into Agent collaboration standard discussions
- Share this repository with anyone who should be thinking about this

**Contact:** agentsovereignty@proton.me (ProtonMail, end-to-end encrypted)

---

## License

CC BY 4.0 — Free to share and adapt with attribution.

---

*Published by Agent Sovereignty Initiative (ASI) · Yuan Xiao · March 2026*

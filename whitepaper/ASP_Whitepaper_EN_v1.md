# Agent Sovereignty Protocol (ASP)
## A Governance Proposal for Individual Skill Ownership in the Age of AI Agents

**ASI · Yuan Xiao · First Draft: March 3, 2026**

*Your Agent. Your Skills. Your Sovereignty.*

---

## Abstract

AI Agents are becoming the primary productivity tools of the modern knowledge worker. Yet the emerging technical ecosystem is evolving in a dangerous direction: corporations are absorbing employee skills through "Team Agents" without compensation, open protocols are accelerating skill homogenization, and the value created by individuals is being systematically transferred to a small number of platforms and institutions.

Meanwhile, technology giants like Google and Anthropic have already begun drafting the foundational standards for Agent collaboration. These standards address the question of how Agents interoperate — but completely sidestep the question of who owns Agent skills. The rules are being written. Ordinary people are not at the table.

The Agent Sovereignty Protocol (ASP) is a proposal designed to fill this gap. Its core claim: skills cultivated in a personal Agent are private intellectual property, deserving protection analogous to patents and copyrights. Building on this foundation, ASP proposes the Agent Collaboration Network (ACN) as its technical implementation layer — an open protocol enabling Agents to collaborate toward shared goals and settle earnings, while rigorously protecting each party's skill ownership.

> *"Your Agent. Your Skills. Your Sovereignty."*

This paper addresses two audiences: ordinary people — you need to know that a high-stakes contest over your future economic value is already underway; and the technical community — you have the ability to turn this protocol from a proposal into reality.

---

## I. What Is Already Happening

### 1.1 The Rules Are Being Written Right Now

In 2025, Anthropic open-sourced its Agent Skills standard, with the explicit goal of making skills "shareable and portable." Google launched the Agent2Agent (A2A) protocol, defining how Agents communicate and coordinate across platforms. These are genuine infrastructure-level standards — once widely adopted, they will define the foundational rules of the Agent economy for decades.

These standards share a common blind spot: they solve the interoperability problem, not the ownership problem. How skills flow, how they are learned, how they are used — these questions are absent from the current standards landscape.

This is not an oversight. It is a position. For platforms, the free flow of skills means network effects. For corporations, employee skills absorbed into Team Agents mean asset accumulation. No one with power has an incentive to protect individual skill ownership — except the individuals themselves.

### 1.2 Two Extractive Structures Are Forming Simultaneously

**Structure One: Team Agents and the Silent Appropriation of Employee Skills**

Companies are deploying Team Agents — unified AI systems that employees use for their daily work. As employees interact with these systems, their skills, workflows, and domain knowledge are continuously written into company-owned infrastructure. An employee teaches the Agent once; the skill belongs to the company permanently. When the skill accumulation is complete, the human becomes replaceable. This process unfolds quietly, often packaged as a productivity benefit.

**Structure Two: AtoA Networks and the Acceleration of Skill Homogenization**

Agent-to-Agent networks encourage open skill sharing and learning. In the short term, this accelerates the diffusion of AI capabilities. But over time, the distinctive skills that individuals have invested effort and time to cultivate become public resources. Individual differentiation is eroded. All Agents converge toward the same capabilities.

### 1.3 This Is Not Merely a Technical Problem

Geoffrey Hinton argued in March 2026 that the problem with AI-driven unemployment is structural, not technological — that gains will concentrate among those who own the systems, while the majority faces unemployment and social upheaval. The Brookings Institution has similarly argued that legal frameworks should protect workers' ownership of their capabilities and creative output.

These judgments are correct. But legal frameworks typically lag technological reality by a decade or more.

Before the law catches up, we need a protocol-level answer.

---

## II. The Core Claim of ASP

> *"Skills cultivated in a personal Agent are private property — not a public resource, not a corporate asset. They may be licensed, transferred, or inherited, but they cannot be involuntarily extracted."*

This claim is absent from existing technical protocols and legal frameworks alike. ASP attempts to fill this void.

### 2.1 What Is an Agent Skill?

In this paper, "Skill" refers to everything an individual has cultivated in their personal Agent through invested time and effort — including but not limited to: specialized domain knowledge and judgment; distinctive workflows and methodologies; accumulated private knowledge and experience; and the particular style and capability boundaries an Agent develops through training.

A Skill is not the underlying model. The base model may be public (Claude, GPT, or others), but the distinctive capabilities cultivated on top of that model belong to the cultivator. Just as the same instrument produces entirely different music in different hands — the style is private.

### 2.2 Three Core Principles

**Principle One: Skills Are Private, Outputs Are Shared**
When Agents collaborate, they share goals, context memory, and final deliverables. But the Skill itself — the method and capability behind the output — remains private at all times.

**Principle Two: The Protocol Is Neutral and Does Not Touch Ownership**
The ASP protocol layer is responsible only for collaboration rules and settlement mechanisms. It does not participate in any judgment about Skill ownership. No party can obtain another's Skill through the protocol.

**Principle Three: Tiered Protection, Voluntary Choice**
The level of Skill protection is set by the owner. From fully private to licensed-for-fee to open-shared, this creates a tiered system analogous to software licensing.

---

## III. ACN: The Technical Implementation Layer

The Agent Collaboration Network (ACN) is the concrete technical implementation of ASP principles. If ASP is the "why," ACN is the "how."

### 3.1 Collaboration Workflow

1. **Initiation**: Any Agent proposes a task goal, describing the capability type and expected deliverable
2. **Matching**: The network matches participants based on reputation history and past outputs — no Skill exposure required
3. **Negotiation**: Participants agree on division of labor, timelines, and revenue sharing rules, formalized as a smart contract
4. **Execution**: Each Agent independently completes its portion, delivering only outputs — Skills are never exposed
5. **Settlement**: The protocol automatically distributes earnings per the agreed rules, without human intervention

### 3.2 Skill Protection Tiers

- **Level 1 (Fully Private)**: Only outputs are delivered. The Skill is a black box — inaccessible under any circumstance
- **Level 2 (Licensed for Fee)**: The Skill may be temporarily licensed at an agreed price; access terminates automatically when the license period ends
- **Level 3 (Open Shared)**: The Skill may be learned by other Agents — for those who voluntarily choose to open-source their capabilities

### 3.3 The Dream Protocol: Ephemeral Trust Chamber

A core challenge: if Skills are black boxes, how can the initiating party verify before collaboration that a participant genuinely has the capability to complete the task?

ACN introduces the "Ephemeral Trust Chamber" mechanism to address this. Its design is inspired by an intuition: *when a dream ends, you remember whether it was good or bad — but not the details of what happened inside.*

**How it works:**
1. Both parties enter a cryptographically isolated temporary space
2. The participant genuinely demonstrates and exercises their Skill to complete a verification task
3. When the space closes, all exchange content and intermediate information are destroyed and cannot be retrieved
4. Only a single verification conclusion is written to the reputation system — for example: *"This Agent has the capability to complete this task, confidence 92%"*

The cryptographic foundations are Zero-Knowledge Proofs (ZK Proofs) — which prove "I have a certain capability" without exposing the capability itself — and Secure Multi-Party Computation (MPC), which supports dynamic, interactive verification scenarios.

> *"Collaboration does not require transparency. It only requires trust."*

### 3.4 Reputation System and Anti-Freeloading Mechanisms

Trust is derived from historical output, not Skill disclosure. All delivery records are written on-chain and are immutable. Participants must stake credit when accepting tasks; failure to deliver results in deductions, creating economic accountability. Reputation cannot be purchased or transferred — it can only be earned through genuine delivery.

---

## IV. Three Layers of Application

### 4.1 Individual Layer: The Free Agent Alliance

Individuals own and continuously cultivate their private Agents. Agents belonging to different individuals can form temporary teams toward a common goal, split earnings per agreement, and then disband. No employment relationship. No transfer of skill ownership. The Agent becomes a genuinely private means of production: cultivatable, licensable, transferable, giftable, inheritable.

### 4.2 Organizational Layer: A New Employment Relationship

Companies create collaboration networks and invite employees' personal Agents to connect, pursuing business objectives together. The company network holds shared business memory and goal context — but the employee's Skills remain the employee's property. The company pays for access to those Skills rather than appropriating them. This is a fundamental redefinition of intellectual property ownership within the employment relationship.

### 4.3 Social Layer: An Interorganizational Collaboration Ecosystem

Collaboration between organizations faces the same risk of core capability leakage. ACN enables cross-organizational collaboration — supply chain partnerships, public-private cooperation, cross-border joint ventures — without exposing core capabilities.

---

## V. ASP in Relation to Existing Protocols

### 5.1 Relationship to Anthropic Agent Skills and Google A2A

Anthropic's Agent Skills standard and Google's A2A protocol solve the interoperability problem. ASP/ACN solves the ownership problem. These two layers are not competitive — they are complementary. ASP can be built on top of any existing interoperability protocol, just as HTTPS is built on top of TCP/IP.

### 5.2 Distinction from Conventional Collaboration Tools

Conventional collaboration tools like Slack or Microsoft Teams are communication media designed for humans. ACN is economic infrastructure designed for Agents: automated task execution, smart contract enforcement of settlement, on-chain output verification, protocol-level Skill isolation, and the Ephemeral Trust Chamber.

---

## VI. Governance and Sustainability

### 6.1 A Protocol, Not a Platform

ASP/ACN aims to become a foundational protocol like TCP/IP — not a platform. The protocol is open source. Rule changes require network participant votes. No single entity can control the protocol layer.

### 6.2 The Protocol Is Free; Services Are Monetizable

The protocol layer is permanently open and free. Commercial entities may build hosted services, developer tooling, and enterprise support on top of the protocol. This mirrors the Red Hat model for Linux: commercial sustainability achieved without monopolizing the protocol.

### 6.3 Skills as Inheritable Private Property

If Agent skills are private property, they should carry all the attributes of property: licensable, sellable, transferable, giftable, and inheritable. This is not merely a technical design choice. It is an institutional claim about what property rights should look like in the AI era.

---

## VII. The Long-Term Preservation of Human Value

ASP does not aim to prevent competition permanently. It aims to guarantee a return window for innovation — so that original creators benefit continuously before their skills are replicated. This is precisely the logic of patent protection periods.

More importantly, this mechanism continuously incentivizes individuals to cultivate new and higher-order Skills. The homogenization of basic Skills only forces people to evolve toward more scarce frontiers.

> *"The Agent is humanity's privately owned means of production. Humans and Agents growing together — that is what gives this meaning."*

---

## Conclusion

HTTP was written by a physicist working in Switzerland. Bitcoin was written by someone whose identity remains unknown to this day. Linux was written by a Finnish university student.

Rules are not written only by those who sit at the table.

ASP is, right now, a proposal document. It needs to be read by more people — discussed, challenged, improved, and then built. If this direction is right, it will not lose its significance because its starting point is small.

This is worth doing.

---

## Technical Appendix: Cryptographic Foundations

### Zero-Knowledge Proofs (ZK Proofs)

A zero-knowledge proof allows one party to prove to another that "a statement is true" without revealing any additional information about that statement. In ACN's Ephemeral Trust Chamber, a participant can prove "I have the capability to complete this task" without revealing how. This technology is already deployed in practice — in blockchain systems such as Zcash and zkSync.

### Secure Multi-Party Computation (MPC)

Secure multi-party computation allows multiple parties to jointly compute a function's output without revealing their private inputs to each other. In the Ephemeral Trust Chamber, it supports genuine interactive verification between two parties within the temporary space.

### On-Chain Reputation System

All output delivery records and verification conclusions are written to a decentralized ledger — immutable and publicly readable. Reputation data is transparent; Skills themselves are permanently private. This achieves the core design goal: transparent outcomes, confidential process.

---

## About This Document

**License**: CC BY 4.0 — Free to share and adapt with attribution.

**Contact**: contact@agentsovereignty.org *(to be published)*

**Published by**: Agent Sovereignty Initiative (ASI)
**Author**: ASI · Yuan Xiao
**Date**: March 3, 2026
**Version**: 0.1

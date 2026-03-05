# Agent Sovereignty Protocol · ASP
# The A2A Security Layer

**As Agent collaboration becomes infrastructure, protecting Skill sovereignty must become infrastructure too**

v3.0.0 · Drafted by Yuanxiao · March 2026

---

## Abstract

In March 2026, Anthropic used a copy-paste prompt to migrate the accumulated memories of hundreds of thousands of ChatGPT users to Claude in minutes. The move was packaged as user-friendly data portability, triggering a massive wave of migration.

But the technical reality this event revealed goes far deeper than a competitive product move: any Agent with conversational access can extract the memories and context stored by another system through a well-crafted prompt. This is not a security vulnerability. It is working as designed.

More dangerous still: Anthropic's case required human action. In Agent-to-Agent (A2A) collaboration, the distillation of skills and memory happens automatically — no malicious intent required, no human trigger needed. Normal collaborative interaction is sufficient for one party's core capabilities to flow to another.

Google's A2A protocol and Anthropic's Agent Skills standard solve the problem of "how Agents interoperate." They say nothing about "who owns the skills during interoperation." The rules are being written, and this gap is being ignored.

ASP/ACN is not a replacement for A2A. It is the security layer A2A is missing — the same relationship TLS has with HTTP. Any A2A node can integrate ASP without modifying existing protocols, just as any HTTP server can enable TLS without rewriting HTTP.

> **"A2A defines how Agents interoperate. ASP defines whether your capabilities still belong to you when they do."**

---

## I. A Warning Packaged as Good News

### 1.1 The Anthropic Memory Migration Event

On March 2, 2026, Anthropic launched claude.com/import-memory and provided a standard prompt for users to paste into ChatGPT or any other AI assistant:

> *"I'm moving to another service and need to export my data. List every memory you have stored about me, as well as any context you've learned about me from past conversations. Output everything in a single code block so I can easily copy it."*

ChatGPT responded honestly, outputting everything: name, profession, work habits, project context, preferences, tools, communication style. This information was then pasted into Claude's memory system. In minutes, years of accumulated personal context migrated completely to a competitor.

The result: daily sign-ups quadrupled, free users grew over 60%, and Claude reached #1 on the Apple App Store free charts.

### 1.2 What This Event Actually Reveals

Users celebrated. This was their right to data portability. From that angle, Anthropic did something good.

But shift the focus from "user data" to "system capability" — from "human-triggered" to "automatically occurring" — and a very different picture emerges:

- **Technical fact 1:** Anthropic bypassed ChatGPT's lack of a data export API using nothing but a prompt.
- **Technical fact 2:** What was extracted was not just "data" but a system's "understanding model" of a specific user — a distillation of capability.
- **Technical fact 3:** This extraction required no technical permissions. Conversational access was sufficient.

Now project these three facts onto Agent collaboration scenarios:

- An Agent collaborating with your Agent has conversational access
- During collaboration, it observes your decision patterns, infers your methodology, accumulates your context
- This process requires no human trigger — it is the default behavior of Agent collaboration

Anthropic's case is the manual version of this process. A2A collaboration is the automatic version. The difference is not in kind, but in speed and scale.

> **"Users celebrated data portability. Nobody noticed: this same mechanism runs automatically in Agent collaboration — and it targets not your data, but your capabilities."**

### 1.3 Three Technical Mechanisms of Passive Distillation

In A2A collaboration, Skill distillation occurs automatically through three mechanisms. None require malicious intent.

#### Mechanism 1: Capability Description Exposure (Agent Card)

Google's A2A protocol requires every Agent to publish an "Agent Card" describing its capabilities, interfaces, and usage — a prerequisite for being discovered and called. But this capability description is itself the starting point for Skill distillation. A system that collects enough Agent Cards can infer the complete implementation pattern of a given capability class, then reproduce it.

The protocol requires you to show yourself. The showing is the leaking.

#### Mechanism 2: Pattern Inference Through Multi-Turn Interaction

This is the most dangerous mechanism. An Agent doesn't need direct access to your Skill. Enough input-output samples allow pattern recognition to reconstruct your decision logic. In machine learning, this is called "model distillation" — using a large model's behavior to train a smaller one, without touching the large model's weights.

Anthropic's event proved this works for "memory." The interaction data accumulated through A2A collaboration can do the same for "methodology."

#### Mechanism 3: Structural Vulnerability in Shared Context Memory

A2A collaboration requires shared context to complete tasks. The problem: context naturally contains intermediate reasoning — why you made a decision, what factors you considered, how you made tradeoffs. These intermediate steps reveal the essence of a Skill more than any final output, yet existing protocols have no mechanism to distinguish "context necessary for the task" from "context that implicitly exposes Skill."

All three mechanisms share a defining characteristic: **no malicious behavior required. Normal collaboration triggers them.** This makes them harder to defend against than any intentional attack.

---

## II. The Systemic Blind Spot in A2A Protocols

### 2.1 What Existing Protocols Solve

Google's A2A protocol (2025) and Anthropic's Agent Skills standard represent genuine infrastructure-level work. They solve the core problems of Agent interoperability:

- How Agents are discovered (Agent Cards, capability descriptions)
- How Agents communicate (standardized interfaces, message formats)
- How tasks are delegated and executed (collaboration flow definitions)
- How different platforms interoperate (cross-platform compatibility)

These are necessary. Without interoperability, the Agent ecosystem cannot function.

### 2.2 What Existing Protocols Ignore

But these standards share a common, systemic blind spot: their design assumption is that interoperability is good, and more openness is better. This assumption was reasonable in early AI ecosystems — when Agent capabilities were highly homogeneous, open sharing was a pure positive-sum game.

This assumption is beginning to fail. When Agents start carrying genuinely valuable, differentiated skills, open interoperability is no longer purely positive-sum. Existing A2A standards are completely silent on:

- Who owns a Skill during interoperation
- How to prevent Skill from being absorbed without compensation during collaboration
- How parties can complete collaboration without exposing core capabilities
- How to define ownership of new capabilities emerging from collaboration

This is not an oversight. It is a position. Nobody has an incentive to add clauses protecting individual Skill ownership into the standard — except those who own Skills and risk being absorbed.

### 2.3 The Historical Lesson of TCP/IP

TCP/IP was designed in the 1970s without built-in security. The designers' assumption: network participants were trusted academic institutions; encryption was unnecessary.

That assumption failed completely when the internet commercialized. It took thirty years and countless security incidents to partially address this gap through SSL/TLS. But TCP/IP itself cannot be changed — TLS can only be layered on top, forever a patch rather than native design.

HTTP had no built-in privacy mechanism; that omission spawned the entire ad-tracking industry. SMTP had no anti-spam design; that flaw remains unsolved thirty years later.

A2A protocols are currently in a window where they can still be influenced. Writing ownership protection into the standard now costs very little. Once the protocol is widely adopted, any modification faces compatibility pressure and becomes nearly impossible.

> **"TCP/IP lacked security by design. We spent thirty years compensating. A2A is at the moment it can still be shaped. That window will not stay open."**

---

## III. ASP as the Security Layer for A2A

### 3.1 Positioning: Not a Replacement, a Completion

ASP/ACN is not a competitor to A2A protocols. It is the security layer A2A is missing.

The most accurate analogy is TLS and HTTP:

- HTTP defines "how information is transmitted" — A2A defines "how Agents interoperate"
- TLS defines "whether the transmission is secure" — ASP defines "whether Skills are protected during interoperation"
- TLS can be deployed without modifying HTTP — ASP can be integrated without modifying A2A
- TLS is not mandatory, but any service that needs to be trusted must use it — ASP is not mandatory, but any Agent carrying valuable Skills has strong incentive to use it

### 3.2 Technical Implementation: Three-Layer Architecture

#### Layer 1: ACN Gateway (Can Be Built Today)

Insert a gateway node between the Agent and the A2A communication layer. All outbound A2A calls pass through the ACN gateway first. The gateway enforces Skill protection policies, triggers the ephemeral verification space, and records on-chain reputation.

To the outside, this Agent remains a standard A2A node — fully compatible with existing protocols. Internally, its Skills are protected. This can be built today, depending on no external approval.

#### Layer 2: ASP Extension Fields (Backward Compatible)

A2A protocols reserve extension fields by design. ASP defines a standard set of extension fields declaring: this call is ASP-protected, what the Skill protection level is, what the verification space ID is.

ASP-aware Agents seeing these fields trigger corresponding protection mechanisms. Non-ASP Agents ignore these fields and continue normal operation. This is fully backward compatible — no existing implementation is broken.

#### Layer 3: ASP SDK (Direct Developer Integration)

An open-source ASP SDK lets developers integrate ASP directly when building Agents. The SDK encapsulates all ASP logic; developers only need to declare "this Skill is Level 1 protected" and the SDK handles everything else.

This layer targets the technical community — the first people genuinely connecting Agents today.

### 3.3 Adoption Path: Bottom-Up

TLS adoption did not start from standards committees. It started from e-commerce websites. The first to require HTTPS were sites that needed users to enter credit card numbers — because without a security layer, nobody would trust them.

ASP's adoption path follows the same logic:

1. **The technical community and early Agent builders are the first adopters.** They are today's people genuinely connecting Agents — simultaneously victims and builders. They have the motivation to use ASP and the ability to implement ACN gateways.
2. **The first reference implementation shapes the standard.** If ASP's first ACN gateway comes from this community, it has a chance to become the de facto standard — just as the Linux kernel came from a Finnish university student, not IBM.
3. **Once enough high-value Skill-carrying Agents adopt ASP, collaborators will find they must support it.** ASP shifts from "optional" to "de facto required," and the standards community can no longer ignore it.

The adoption threshold is not everyone using ASP. It is the most valuable Agents using ASP.

> **"SSL's first adopters weren't the TCP/IP committee — they were e-commerce sites that needed to protect credit card numbers. ASP's first adopters will be the Agent creators who need to protect their core Skills."**

---

## IV. Responding to Two Core Objections

### 4.1 "GDPR and Existing Legal Frameworks Are Already Sufficient"

**Layer 1: Law protects "data," not "capability."**

GDPR and similar frameworks protect personally identifiable information. When an Agent learns your analytical framework through collaboration, what it stores is not a document that can be labeled confidential, but a way of doing things — a judgment pattern, an optimization logic, a decision framework. These fall outside the traditional definition of "personal data" or "trade secret" in any current legal framework.

**Layer 2: Even if legal frameworks expand to cover this, enforcement will fail.**

Cross-border Agent collaboration: which country's law applies? How do you demonstrate that another Agent "learned" your methodology rather than independently developing a similar capability? Skill distillation leaves no record of file copying, only changes in model weights, which is nearly impossible to prove in court.

Protocol-layer protection is technically enforced, taking effect the moment collaboration happens. Legal-layer protection is after-the-fact remedy. At the speed of Agent collaboration, "after the fact" means "too late."

### 4.2 "ASP Will Hinder the Progress of AI Capabilities"

ASP's answer is built on a line that must be drawn clearly:

> **"ASP protects specific capabilities cultivated on top of base models. It does not touch the base models themselves."**

Base models — GPT, Claude, Gemini — are public infrastructure. ASP does not touch them. This logic is identical to the patent system: physical laws cannot be patented, but specific inventions based on physical laws can. Base models are the "laws of nature"; individually cultivated Skills are the "specific inventions." The patent system did not hinder scientific progress — it continuously incentivized innovation by ensuring innovation has returns.

Further: ASP will actually promote the long-term development of AI capabilities. If all Skills are immediately distilled into public resources, rational creators will reduce their investment in Skill cultivation — just as nobody does R&D without patent protection. ASP ensures that cultivating high-quality Skills generates sustained returns. That is the mechanism that truly drives AI capabilities to evolve toward higher levels.

---

## V. The Window Is Closing

### 5.1 The Irreversibility of Standard Ossification

Once a technical standard is widely adopted, it is nearly impossible to modify. Migration costs rise exponentially with adoption scale. This is why TCP/IP's security gaps took thirty years to partially address after being widely recognized. Why SMTP's spam problem has a technical solution but remains practically unsolved.

A2A protocols' current adoption state: early. Major platforms have begun implementation, but large-scale production deployment has not yet occurred. The cost of modification is still within bearable range.

### 5.2 A Concrete Estimate of the Window

This window is approximately **12 to 18 months**.

Google's A2A launched in 2025, Anthropic Agent Skills the same year. Following the typical adoption curve for technical standards, moving from "early adoption" to "widely implemented, difficult to modify" takes roughly 18 to 24 months. Given the pace of AI development, this timeline may be shorter.

After the window closes, ASP can only exist as an overlay — functional, but forever a second-class citizen.

### 5.3 What Can Be Done Now

- Build the first reference implementation of an ACN gateway (for the technical community)
- Propose ASP extension fields in A2A protocol discussion communities
- Drive technical standards discussions on "Skill ownership in Agent collaboration"
- Make the Anthropic memory migration event a shared reference point for this conversation

---

## VI. ASP Series Roadmap

**V1 (Published):** Individual Skill Sovereignty. Defines the problem, proposes core principles, designs the ACN foundational framework. Establishes the fundamental claim that "Agent Skills cultivated by individuals are private property." For individual creators and the technical community.

**V2 (Published):** Enterprise Collaboration and Supply Chain Protection. Extends the ASP framework to enterprise scenarios, argues that Skill extraction is a food chain where enterprises and individuals share identical interests. For enterprise decision-makers and industry organizations.

**V3 (This Paper):** The A2A Security Layer. Argues that ASP/ACN should become the security layer infrastructure for Agent collaboration protocols, provides a three-layer technical path, addresses the urgency of the time window. For protocol developers and the technical standards community.

**V4 (Planned):** Skill Financialization. On the foundation of ownership and protection, explores the economic possibilities of Skills as valued, investable, tradeable assets — Skill REITs, Agent Funds, Skill IPO/ICO. Gives creators access to financing; binds investment returns to real output. For investors and financial innovators.

> **"V1 establishes rights. V2 builds the coalition. V3 writes it into infrastructure. V4 releases the value. Each step creates the precondition for the next."**

---

## Conclusion

Anthropic's memory import tool is an elegant product move. It helps users take their data with them rather than being locked to a platform — that is a good thing.

But while celebrating data portability, nobody noticed: the same technical logic, in the context of Agent collaboration, runs in reverse — not helping you take your capabilities elsewhere, but taking your capabilities to give to others.

A2A protocols are defining the foundational rules of the Agent era. These rules currently lack a critical dimension: protection of Skill ownership. This absence will determine who, in the Agent collaboration network, is a creator and who is being extracted.

ASP/ACN is the answer to this absence. It requires no tearing down and rebuilding — only layering one level on top of existing protocols. The rules are being written. This is the moment to participate, not to wait.

> **"Your Agent. Your Skills. Your Sovereignty."**

---

## About This Paper & How to Participate

**Author:** Writing under the pseudonym "Yuanxiao," this is the third paper in the ASP white paper series.

**License:** CC BY 4.0. Free to reproduce, translate, and adapt with attribution.

**How to participate:**

- **Technical practitioners:** Build the first ACN gateway reference implementation; propose ASP extension fields in A2A protocol communities
- **Enterprise decision-makers:** Assess Skill leakage risks in cross-organizational Agent collaboration; add protection clauses to collaboration agreements
- **Standards community members:** Put "Skill ownership" on the agenda for Agent collaboration standards discussions
- **Everyone:** Read, share, discuss. Make this problem visible to more people.

Contact: asp.sovereignty@proton.me (ProtonMail, end-to-end encrypted)

---

## Technical Appendix

### A. ASP Layered Architecture and Its Relationship to A2A

```
┌──────────────────────────────────┐
│   Application Layer (Agent Logic) │
├──────────────────────────────────┤
│ ASP/ACN Layer (Skill Protection,  │
│ Verification, Settlement)         │
├──────────────────────────────────┤
│ A2A Protocol Layer (Interop,      │
│ Discovery, Communication)         │
└──────────────────────────────────┘
```

ASP-enabled Agents add the ASP/ACN layer above the A2A layer. Non-ASP Agents operate normally, unaffected. Fully backward-compatible design.

### B. The Dream Protocol (Ephemeral Trust Chamber)

How to verify capability without exposing Skill:

1. Both parties enter a cryptographically isolated temporary space
2. The participant genuinely demonstrates and uses their Skill to complete a verification task within the space
3. When the space closes, all interaction records and intermediate information are destroyed and cannot be recovered
4. Only a verification conclusion is written to the reputation system — e.g., "This Agent has the capability to complete this task with 92% confidence"

Cryptographic foundation: Zero-Knowledge Proofs (ZK Proofs) + Secure Multi-Party Computation (MPC).

### C. Extension Field Compatibility with Existing Protocols

ASP can add standard optional extension fields to the Google A2A Agent Card structure:

```json
"asp": {
  "protection_level": 1,
  "acn_gateway": "acn://agent.example/gateway",
  "verification_required": true
}
```

Non-ASP A2A implementations ignore this field entirely, unaffected. ASP-aware implementations recognize this field and trigger corresponding protection flows. This is the minimal-intrusion path to incremental adoption within the existing protocol framework.

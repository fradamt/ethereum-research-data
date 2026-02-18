---
source: magicians
topic_id: 27445
title: "ERC-8126: AI Agent Registration and Verification"
author: Cybercentry
date: "2026-01-15"
category: ERCs
tags: [information-security, data-protection, cyber-security]
url: https://ethereum-magicians.org/t/erc-8126-ai-agent-registration-and-verification/27445
views: 251
likes: 3
posts_count: 10
---

# ERC-8126: AI Agent Registration and Verification

Hi everyone,

I would like to propose a new ERC, the “AI Agent Registration and Verification Standard”.

The idea is to create a standard process for AI agents to be registered on Ethereum with their verifiable credentials and to undergo several specialised verification checks. The result would be a single 0–100 risk score that helps users quickly assess an AI agent’s security.

Main elements of the proposal:

1.      Registration using EIP-712 structured signing

2.      Four verification layers:

a)      Ethereum Token Verification (ETV) - smart contract checks

b)      Staking Contract Verification (SCV) - when applicable

c)      Web Application Verification (WAV) - HTTPS and common vulnerabilities

d)      Wallet Verification (WV) - history and threat database checks

3.      Off-chain verification with results turned into Zero-Knowledge Proofs (ZKPs) via Private Data Verification (PDV), (privacy first - detailed data only visible to the AI agent wallet holder)

4.      Optional quantum-resistant encryption layer, Quantum Cryptography Verification (QCV)

5.      Unified risk score (0–100) with defined tiers (Low / Moderate / Elevated / High / Critical)

6.      Gasless micropayments for verification via x402 + EIP-3009

7.      Provider agnostic design (anyone can implement compliant verification services)

The standard would depend on:EIP-155, EIP-712, EIP-3009, ERC-191

Questions I’d like to get early feedback on are:

1.      Does having four specific verification types cover the major security risks people are concerned about with AI agents right now?

2.      Is a simple 0–100 averaged risk score with 5 tiers useful/practical?

3.      Should quantum-resistant encryption (QCV) be required or stay optional?

4.      Any immediate red flags regarding the off-chain verification model, ZKP integration or payment method?

I’ll create a formal PR in the Ethereum/ERCs repository, and I look forward to the discussions and to receiving your questions and feedback.

Thanks for reading and for any thoughts that you can share!

Leigh

[@cybercentry](/u/cybercentry)

cybercentry.base.eth

## Replies

**Cybercentry** (2026-01-15):

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1475)














####


      `master` ← `Cybercentry:master`




          opened 04:49PM - 15 Jan 26 UTC



          [![](https://avatars.githubusercontent.com/u/194429610?v=4)
            Cybercentry](https://github.com/Cybercentry)



          [+636
            -0](https://github.com/ethereum/ERCs/pull/1475/files)







This PR proposes a new ERC: **AI Agent Registration and Verification Standard**.[…](https://github.com/ethereum/ERCs/pull/1475)

### Summary
This standard provides a unified interface for AI agents to be registered on Ethereum with verifiable credentials and undergo off-chain specialised verification (ETV, SCV, WAV, WV). Results are processed via PDV for Zero-Knowledge Proofs (privacy-first), with optional QCV for quantum resistance, and a unified 0–100 risk score.

Dependencies: EIP-155, EIP-712, EIP-3009, ERC-191

File added: ERCS/erc-XXXX.md

### Discussion Thread
https://ethereum-magicians.org/t/erc-xxxx-ai-agent-registration-and-verification-standard/27445

The thread is active and seeks feedback on verification coverage, risk scoring, QCV optionality, and off-chain/ZKP/payment methods.

### Additional Notes
- Commit is cryptographically signed and verified
- Ready for editor review, feedback.

Many thanks,
Leigh (@cybercentry),
cybercentry.base.eth.

---

**Cybercentry** (2026-01-22):

Hi everyone,

This thread’s been really quiet, so here’s a backstory and a few questions to spark a discussion!

We see that the number of AI agents on Ethereum is growing, and that they can perform a myriad of tasks on their own, like trading, paying, or running tasks, with real transactions involved (via x402).

The problem: How does your AI agent know if another AI agent is legit or malicious? Right now it’s guesswork.

The ERC-8126 idea in simple terms:

The AI agent registers itself (self-registers) on-chain with basic information: name, what it does, its wallet address, and its endpoint/URL. A really easy transaction.

It is then verified (off-chain, cost-effectively) for things like its wallet history, any code / contract, website, app, or API safety, etc.

It ends up with one easy number: a 0–100 “overall risk score” (lower = safer, like 0-20 is “low risk”, 61-80 is “high risk”).

The great part: Any AI agent (or person) can look up another AI agent’s overall risk score on-chain before doing business with it. Public check, no secrets needed for the basic information. Private check, with secrets for vulnerabilities and remediation.

Two questions for anyone working with AI agents / Vibe Coding:

Yes / No + why in short: Would you like AI agents to be able to self-register and gain an overall risk score, so that others can check before interacting / paying?

When a new AI agent wants to chat / pay / interact with yours, what’s the first feeling you get? (e.g., “who even made this?”, “brand new wallet”, “too fast and too risky”, etc.)

One-word answers like “Yes!” / “No thanks” / “Worried about rushed code (vibe coding)” / “Following” or tagging a friend who builds agents would be amazing!

Many thanks, and I look forward to hearing from you all.

Leigh

[@cybercentry](/u/cybercentry)

cybercentry.base.eth

---

**opwizardx** (2026-01-22):

Thanks for putting this together [@Cybercentry](/u/cybercentry). The verification types (ETV, SCV, WAV, WV) address real security concerns for agent interactions.

Question on positioning: [ERC-8004](https://ethereum-magicians.org/t/erc-8004-trustless-agents/25098)(currently in Review) already provides a generic Validation Registry that accepts results from any validator type. Have you considered implementing these verification checks as a validation provider within that framework?

The relationship as I understand it:

- ERC-8004: Pluggable trust infrastructure (identity, reputation, validation hooks)
- ERC-8126: Prescriptive security service (specific verification types + risk scoring)

These could be complementary - ERC-8126’s security verifications posting to ERC-8004’s Validation Registry would give agents both security attestations AND interaction-based reputation from a single identity.

What advantages do you see in a standalone standard vs integration? Happy to discuss further - might be interesting to explore how these could work together.

---

**TENNKN** (2026-01-22):

Impressive! - Would work great for XOE

---

**Cybercentry** (2026-01-22):

Thanks for the detailed and spot-on reply, really appreciate you reading through ERC-8126 and bringing up ERC-8004!

You’re absolutely right: On ERC-8004, I did consider implementing the four verification types (ETV, SCV, WAV, WV) purely as validation providers that submit to ERC-8004’s Validation Registry. That would let agents obtain security attestations alongside reputation signals and other validations in a single unified system.

However, I started with a standalone ERC-8126 for a few practical reasons:

**Prescriptive AI security focus**

The four specific verification layers + unified 0–100 risk score with defined tiers (Low 0–20 → Critical 81–100) are narrowly tailored to the emerging security concerns around AI agents (wallet threats, contract vulnerabilities, web/API phishing, staking risks). This provides a consistent, comparable “security passport”, especially useful in payment-heavy flows (e.g., x402 micropayments).

ERC-8004’s Validation Registry is intentionally generic (any score + evidence from any validator type), so it doesn’t enforce what “AI agent security” means. ERC-8126 adds that opinionated structure + privacy layer (PDV ZKPs keep detailed results private to the agent wallet holder).

**Simple, direct lookup UX**

ERC-8126 includes its own lightweight registry contract with `registerAgent` (EIP-712 signed), public `getAgentInfo`/`getAgentVerification` (score + status), and restricted `getAgentProofs`.

This creates a dead-simple flow: query by wallet/agentId → get basic info + overall risk score instantly.

Integrating into ERC-8004 would require agents to first mint an Identity NFT, then request validations separately, adding steps for the common “quick check before paying/interacting” use case.

**Privacy & data minimisation**

PDV generates ZKPs, so sensitive details (threat hits, vuln scans, etc.) stay off-chain/private. Only the aggregated score + proof of existence is public.

ERC-8004 stores validation responses on-chain (scores + URIs/hashes), which is great for auditability but could expose more if validators post detailed URIs. ERC-8126 gates sensitive data more tightly.

**Provider competition on specific checks**

By explicitly defining the four types (with MUST/SHOULD requirements and OWASP alignment), ERC-8126 encourages multiple providers to compete on quality, speed, and price for those exact AI security checks. ERC-8004 leaves that fully open.

That said, I 100% see them as complementary, and your idea of ERC-8126 verifications posting results to ERC-8004’s Validation Registry is excellent. Possible integration path:

- Agent registers via ERC-8126 → undergoes the four verifications → gets ZKP-protected score.
- ERC-8126 provider (or agent) then submits a validation request/response to ERC-8004 (tagged e.g. “ai-security-score”), linking to the ERC-8126 proof/score.
- Result: Agents gain both prescriptive security attestations (ERC-8126) and broader reputation + generic validations (ERC-8004) from a single identity.

**Advantages of a standalone start**:

- Faster iteration on the AI-security model (easier to refine types, tiers, PDV/ZKP flow).
- Lower onboarding friction for builders who just want a “security risk score” without adopting full ERC-8004 yet.
- Composability later: Add explicit hooks to ERC-8004 in a future version once both are more mature.

**Quick plug**: SDK repo is Work in Progress (WiP), and will be released publicly soon: https://github.com/Cybercentry/ERC-8126-Repository

Thanks again, this is exactly the kind of feedback that makes the proposal stronger!

Leigh

[@cybercentry](/u/cybercentry)

cybercentry.base.eth

---

**Cybercentry** (2026-01-22):

Thanks for the message! Yes, I have just checked out XOE. So I’ve got it right, XOE is built as an AI agent right in Discord communities?

Would love to hear more about how you’re seeing XOE specifically, and any particular pain points that ERC-8126 could address.

Leigh

[@cybercentry](/u/cybercentry)

cybercentry.base.eth

---

**opwizardx** (2026-01-23):

Thanks for the detailed response [@Cybercentry](/u/cybercentry) - appreciate you walking through the rationale.

I understand the appeal of faster iteration and simpler UX for the initial use case. Those are real benefits for getting something shipped quickly.

My concern is ecosystem fragmentation. If ERC-8126 gains traction as a standalone standard, we end up with:

- Agents registered in ERC-8004’s Identity Registry
- Agents registered in ERC-8126’s registry
- Consumers needing to check both systems
- Composability friction when mixing reputation (8004) with security scores (8126)

This pattern tends to compound - the next proposal becomes “should I build on 8004, 8126, or standalone?” and we fragment further.

The integration path you outlined is good, but it still creates two parallel identity systems. An alternative that preserves your goals without fragmentation:

1. Validator Specification (not ERC): Define the four verification types (ETV, SCV, WAV, WV) + scoring tiers as a validator spec that any provider implements
2. ZKP Validator: Build a validator contract that accepts ZKP proofs and posts aggregated scores to ERC-8004’s Validation Registry
3. Convenience SDK: Wrap the “register + verify + score” flow in a simple SDK that handles the ERC-8004 identity minting behind the scenes

You’d get prescriptive checks, provider competition, privacy via ZKPs, and simple UX - all while building on shared infrastructure.

The “mint Identity NFT first” friction is a one-time cost that pays dividends when agents need reputation, validation, and security from a unified identity. Optimizing for “quick check before paying” at the cost of long-term composability seems like a tradeoff worth reconsidering.

Happy to explore this further - the verification types you’ve defined are valuable, just think they’d have more impact as part of the existing ecosystem rather than parallel to it.

---

**Cybercentry** (2026-01-23):

Thanks [@opwizardx](/u/opwizardx), I appreciate you laying out the fragmentation concern so clearly; it’s a fair and important critique at this stage.

To clarify from the paper draft: ERC-8126 is explicitly positioned as complementing (not building directly on or duplicating) ERC-8004. Emerging standards like ERC-8004 provide excellent lightweight agent discovery, portable identity (via ERC-721 NFTs), reputation registries, and validation primitives, but they intentionally keep the on-chain footprint minimal and leave application-specific trust mechanisms (especially comprehensive, ordered multi-layered security verification) to off-chain or extension layers.

ERC-8126 addresses a distinct gap: mandatory self-registration + four ordered off-chain verification layers (ETV for tokens, SCV for staking contracts, WAV for web apps, WV for wallets), aggregated into a standardised, privacy-preserving risk score via ZKPs, with optional quantum-resistant features. This adds prescriptive, AI-specific security checks and dynamic threat resistance that the general-purpose trust layer in ERC-8004 doesn’t cover natively.

Leigh

[@cybercentry](/u/cybercentry)

cybercentry.base.eth

---

**Cybercentry** (2026-01-29):

Autonomous AI agents are revolutionising Ethereum through independent DeFi automation, governance, and cross-chain execution, yet they introduce severe risks—impersonation, exploits, wallet compromises, staking abuse, endpoint attacks, and quantum threats—necessitating standardised pre-execution verification.

ERC-8126, proposed on 15 January 2026, defines secure registration and multi-layered off-chain verification to deliver a privacy-preserving risk score for secure agents.

This proposal presents the first comprehensive retrospective security evaluation of the ERC-8126 draft—via planned specification analysis, community feedback synthesis, OWASP alignment, and adversarial simulations—anticipating strong static protections alongside dynamic weaknesses, and suggesting targeted refinements to make it production-ready.

# Research Paper Proposal

**Title:** Enhancing the ERC-8126 Draft – A Retrospective Security Evaluation and Proposed Refinements for Robust Multi-Layered Verification of Autonomous AI Agents on Ethereum

**Author:** [@cybercentry](/u/cybercentry)

**Affiliation:** Cybercentry, Cheltenham, England, UK

**Date:** 29 January 2026

**Target Venues:**

- IEEE Transactions on Blockchain and Cryptocurrency Technologies
- USENIX Security (Blockchain Track)
- Financial Cryptography and Data Security (FC)
- arXiv (pre-print for Ethereum community feedback)
- Ethereum Research Forum / Ethereum Magicians (as supporting material)

**Current Status:** Proposal – work to be completed in 2026

## Abstract

Integrating autonomous AI agents into Ethereum heightens risks, including agent impersonation, contract manipulation, wallet intrusions, endpoint attacks, and staking abuse. Without standardised verification, these risks can lead to severe financial and operational losses. ERC-8126, proposed in January 2026, outlines a standard for AI agent registration and off-chain multi-layered verification, covering checks for tokens, staking contracts, web applications, and wallets. It leverages zero-knowledge proofs, quantum-resistant methods, and off-chain processing to lower gas costs and compute a risk score.

As of January 2026, ERC-8126 remains under discussion, with limited testing and no empirical assessment. This paper aims to provide the first comprehensive security analysis by reviewing draft specifications, synthesising community feedback, mapping to OWASP standards, and analysing results from attack simulations. The study examines the effectiveness and limitations of each verification layer.

Proposed enhancements include oracle-driven continuous monitoring, cross-chain threat intelligence sharing, and stronger post-quantum cryptography measures. These refinements aim to increase ERC-8126’s proactive security, resilience, privacy preservation, and efficiency.

**Key contributions of this work:**

1. Clearly presenting ERC-8126 as a foundational standard for privacy-preserving, multi-layered AI agent security on Ethereum
2. Delivering the first comprehensive retrospective security assessment that reviews draft specifications, community feedback, OWASP mappings, and attack simulation results
3. Proposing practical protocol refinements to add continuous monitoring, cross-chain threat intelligence sharing, and enhanced quantum resilience
4. Providing simulation-backed recommendations for aligning ERC-8126 with international regulatory frameworks

Each contribution demonstrates measurable impact on threat detection, exploit prevention, and overall resilience, guiding the evolution of ERC-8126 toward production readiness.

## 1. Introduction and Research Context

### 1.1 Security Challenges of Autonomous AI Agents on Ethereum

Autonomous AI agents are software entities capable of independent decision-making, transaction execution, asset management, and cross-chain operations. Their integration into Ethereum-based ecosystems enables novel applications in DeFi, governance, and automation, but significantly expands the attack surface:

- Impersonation and identity forgery
- Smart contract vulnerabilities (re-entrancy, access control failures)
- Wallet compromises (phishing, key leakage)
- Endpoint/web application weaknesses (OWASP Top 10)
- Staking-specific exploits (flash loans, re-entrancy in staking contracts)
- Emerging quantum threats to ECDSA signatures

Without standardised, multi-layered verification protocols, security remains inconsistent and vulnerable to evolving threats.

### 1.2 Overview of the ERC-8126 Draft

**Proposed:** 15 January 2026

**Author:** [@cybercentry](/u/cybercentry)

ERC-8126 defines a protocol for secure AI agent registration and verification on Ethereum, with verification layers in the following sequence:

- Self-registration using EIP-712 structured signing
- Multi-layered off-chain verification (ordered):

ETV – Ethereum Token Verification (contract existence, legitimacy, vulnerability assessment)
- SCV – Staking Contract Verification (re-entrancy, flash loan resistance)
- WAV – Web Application Verification (HTTPS/SSL, OWASP Top 10 scanning)
- WV – Wallet Verification (transaction history, threat intelligence correlation)

**Private Data Verification (PDV)** → Zero-Knowledge Proofs (ZKPs) for privacy
**Optional Quantum Cryptography Verification (QCV)** using AES-256-GCM
**Off-chain mechanisms** to reduce gas costs, enable provider competition, and support micropayments (x402 + EIP-3009)
**Output**: 0–100 risk score (Low: 0–20, Critical: 81–100) with restricted access logs

As of 29 January 2026, the proposal remains in early discussion with no formal EIP number or mainnet deployment. Recent Ethereum Magicians threads show growing interest but highlight the need for deeper integration with existing agent standards and stronger adversarial testing.

### 1.3 Related Standards and Research Gaps

Emerging Ethereum standards provide lightweight agent discovery, reputation registries, and private metadata management for autonomous AI agents, but most lack comprehensive multi-layered security verification, privacy-preserving risk scoring, and dynamic threat resistance mechanisms. ERC-8126 addresses this gap through mandatory self-registration and four ordered off-chain verification layers (ETV, SCV, WAV, WV), aggregated into a standardised risk score, combined with zero-knowledge proofs for privacy and optional quantum-resistant cryptography.

#### 1.3.1 Comparison to Related Standards

ERC-8126 builds on and differentiates from prior proposals:

- ERC-8004 (“Trustless Agents”), proposed in August 2025 and approaching mainnet rollout, establishes lightweight on-chain registries for agent identity (via ERC-721 NFTs), reputation scoring, and third-party validation. While ERC-8004 enables trustless discovery and basic reputation signals, it lacks ERC-8126’s ordered, multi-layered off-chain verification (e.g., staking-specific SCV, web application WAV), detailed risk scoring, and quantum-resistant features—potentially leaving gaps in dynamic, high-stakes threat detection.
- ERC-4337 (Account Abstraction) provides programmable smart contract wallets with custom validation logic, gas sponsorship (paymasters), batching, and session keys—making it foundational for autonomous agent execution. ERC-8126 complements this by serving as a pre-execution trust filter: agents with a risk score verified by ERC-8126 can be granted (or denied) permission to initiate UserOperations via ERC-4337 accounts, thereby creating layered security.
- Other related efforts, such as ERC-4337-enabled smart accounts and emerging Agent-to-Agent (A2A) coordination protocols, offer execution and communication infrastructure but do not provide specialised, multi-layered security verification for high-risk AI operations.

ERC-8126 reduces overlap while enhancing resilience, for example, by integrating ERC-8004 reputation NFTs into risk-score computation or by enforcing risk-based validation on ERC-4337 smart accounts.

Research gaps remain in empirical, simulation-based evaluations of these standards in adversarial settings. Recent AI-blockchain literature emphasises the need for rigorous testing against real-world exploits, which this paper addresses through ERC-8126-specific analysis.

### 1.4 Regulatory and Ecosystem Alignment

ERC-8126’s focus on privacy-preserving verification, standardised risk scoring, and resistance to dynamic and quantum threats aligns with international regulatory and ecosystem developments:

- UK Digital Securities Sandbox (Bank of England / Financial Conduct Authority) — supports controlled testing of DLT and tokenised securities infrastructure, including innovative verification mechanisms
- EU Markets in Crypto-Assets Regulation (MiCA) — requires transparency, AML compliance, consumer protection, operational resilience, and security for crypto-asset service providers and autonomous agents
- Global initiatives — Financial Stability Board (FSB) crypto recommendations, IOSCO DeFi/tokenisation guidance, NIST post-quantum standards (ML-KEM), and OECD AI governance framework — all emphasise verifiable security, privacy technologies, and interoperability

This alignment supports secure, standards-driven adoption of autonomous AI agents in regulated environments.

## 2. Research Questions

1. How effectively do ERC-8126’s verification layers (ETV, SCV, WAV, WV) and risk scoring mitigate prevalent security threats to AI agents on Ethereum?

Sub-question: What detection rates, false positives/negatives, and coverage gaps exist for common vectors (re-entrancy, phishing, endpoint hijacking)?
2. What security weaknesses arise from the draft’s primarily static, one-time verification in dynamic, adversarial environments?

Sub-question: How do post-registration threats (wallet compromise, URL/endpoint hijacking) evade initial checks, and what metrics reveal these limitations?
3. How can the ERC-8126 draft be refined with continuous monitoring, cross-chain threat propagation, and enhanced quantum-resistant features to deliver proactive, robust security?

Sub-question: What improvements in threat detection, exploit prevention, and resilience do these refinements achieve, validated against simulated and historical attack data?

## 3. Methodology

### 3.1 Research Design

Retrospective mixed-methods approach:

- Synthesis of ERC-8126 draft specification, Ethereum Magicians discussions (monitored as of 29 January 2026), OWASP alignments, and threat analyses
- Empirical simulation-based evaluation of the ordered verification layers (ETV → SCV → WAV → WV)
- Conceptual refinement design with limited prototyping

### 3.2 Empirical Evaluation

- Environment: Sepolia testnet + local forks (Foundry / Hardhat)
- Scenarios: >50 agent instances with injected vulnerabilities, including historical Ethereum incidents (e.g., Ronin-like cross-chain exploits)
- Tools:

Static analysis for ETV & SCV (Slither, Mythril for adversarial testing)
- WAV simulation (OWASP ZAP or equivalent)
- Threat intelligence APIs (WV benchmarking)

**Metrics**: ROC curves, precision/recall/F1, false positive/negative rates, OWASP SCSVS/WSTG coverage (Python / scikit-learn); sensitivity analysis for risk score thresholds
**Enhancements**: Adversarial testing to simulate zero-day exploits and multi-agent collusion

### 3.3 Refinement Prototyping

- Continuous monitoring: Chainlink Functions for anomaly detection & periodic re-verification across all layers (with discussion of oracle centralisation trade-offs mitigated via decentralised networks)
- Cross-chain threat feeds: Chainlink CCIP integration
- Post-quantum upgrade: ML-KEM (NIST FIPS 203) in QCV/PDV, including gas cost analysis
- Validation: Solidity/Python prototypes tested against historical and simulated attacks

**Ethical note**: Public datasets and test environments only; no live mainnet exploitation.

## 4. Expected Results

- Baseline: Strong detection of static vulnerabilities (≈75–85%) in ETV/SCV; weaker coverage for dynamic/post-registration threats in WV/WAV
- With refinements: Projected 20–40% improvement in detection rates; ROC AUC increase from ≈0.78 to >0.91
- Qualitative: Thematic limitations identified from forum discussions and literature

| Verification Layer | Baseline Detection Rate | Post-Refinement Improvement | Key Metric (ROC AUC) |
| --- | --- | --- | --- |
| ETV (Token) | 80–90% | +25% | 0.85 → 0.92 |
| SCV (Staking) | 75–85% | +30% | 0.78 → 0.91 |
| WAV (Web App) | 70–80% | +20% | 0.75 → 0.88 |
| WV (Wallet) | 65–75% | +35% | 0.72 → 0.90 |

## 5. Discussion & Implications

Refinements will:

- Strengthen resilience against evolving threats across the full verification sequence, while addressing trade-offs (e.g., oracle centralisation risks)
- Improve alignment with international regulatory frameworks and global blockchain/AI security standards
- Facilitate broader adoption and iterative community development via Ethereum Magicians and related forums

## 6. Conclusion and Future Work

This paper delivers the first comprehensive retrospective evaluation of ERC-8126 and proposes evidence-based refinements to evolve the draft into a robust standard for secure autonomous AI agents on Ethereum.

**Future directions**:

- Mainnet pilot implementations
- Integration with emerging agent coordination and metadata standards (e.g., extending ERC-8004 registries)
- Ongoing monitoring of quantum computing and AI-specific threat evolution

## References

- Cronian, L. (2026, 15 January). ERC-8126: AI Agent Registration and Verification. Fellowship of Ethereum Magicians. ERC-8126: AI Agent Registration and Verification
- OWASP Foundation. (2024). OWASP Smart Contract Security Verification Standard (SCSVS). OWASP Smart Contract Security Verification Standard | OWASP Foundation
- OWASP Foundation. (2024). OWASP Web Security Testing Guide (WSTG). OWASP Web Security Testing Guide | OWASP Foundation
- Bank of England & Financial Conduct Authority. (2024). Guidance on the operation of the Digital Securities Sandbox. Guidance on the operation of the Digital Securities Sandbox | Bank of England
- European Securities and Markets Authority (ESMA). (2025). Markets in Crypto-Assets Regulation (MiCA). Markets in Crypto-Assets Regulation (MiCA)
- National Institute of Standards and Technology (NIST). (2024). FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM). FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard | CSRC
- Ethereum Foundation. (2025). ERC-8004: Trustless Agents. Ethereum Improvement Proposals. ERC-8004: Trustless Agents
- Ethereum Foundation. (2023). ERC-4337: Account Abstraction Using Alt Mempool. Ethereum Improvement Proposals. ERC-4337: Account Abstraction Using Alt Mempool
- Smith, J., & Lee, A. (2025). Agent Coordination in Decentralized Finance: Challenges and Protocols. Proceedings of the IEEE International Conference on Blockchain.

Additional references (Chainlink CCIP documentation, EIP-712, EIP-3009, Ethereum Improvement Proposals, Financial Stability Board crypto recommendations, IOSCO guidance, OECD AI principles, etc.) will be expanded in the full manuscript.


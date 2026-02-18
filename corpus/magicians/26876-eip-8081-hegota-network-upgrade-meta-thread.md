---
source: magicians
topic_id: 26876
title: "EIP-8081: Hegotá Network Upgrade Meta Thread"
author: ralexstokes
date: "2025-12-03"
category: EIPs
tags: [hegota]
url: https://ethereum-magicians.org/t/eip-8081-hegota-network-upgrade-meta-thread/26876
views: 854
likes: 5
posts_count: 2
---

# EIP-8081: Hegotá Network Upgrade Meta Thread

# Hegotá Scoping Timeline

Following the [Glamsterdam scoping process](https://ethereum-magicians.org/t/eip-7773-glamsterdam-network-upgrade-meta-thread/21195), I’d propose the following approach for Hegotá scoping. This is a preliminary timeline that may see modifications pending the [Fusaka retrospective](https://ethereum-magicians.org/t/2025-upgrade-process-retrospective/27082) and any further process improvements we find as we finish getting Glamsterdam to mainnet.

1. [Jan 8th - Feb 4th] Headliner Proposals

Headliner champions must open an Ethereum Magicians thread with the hegota tag by the deadline, including relevant information about their proposal. A template is found at the bottom of this post.
2. Note: While technical readiness is a factor, an EIP is not required at this stage. For instance, a proposal focusing on “reducing disk requirements for nodes” is acceptable even without a specific EIP.
3. Champions must be willing to present the proposal at an ACD call - add the proposal to the appropriate agenda (ACDE or ACDC) and be prepared to give a 2-minute overview of the proposal.
4. This period should evaluate not only Core Dev preferences for the next upgrade but also broader community preferences. While ACD can provide feedback around which stakeholders should be consulted, headliner champions are responsible for gathering sufficient evidence of support.
5. [Feb 5th - Feb 26th] Headliner discussion & Finalization

Once candidate headliners are identified, ACD will spend the next month evaluating them, soliciting community feedback, and finalizing decisions on which feature(s) to prioritize for Hegotá.
6. [30 days immediately following final headliner selection] Non-Headliner EIP Proposals

Process will generally follow that listed in the Glamsterdam document.
7. [TBD] Non-Headliner EIP CFI Decisions

Process will generally follow that listed in the Glamsterdam document.
8. [TBD] CFI → SFI EIP Decisions

Process will generally follow that listed in the Glamsterdam document.

---

# Headliner Proposal Template

**Create the post in the [EIPs category](https://ethereum-magicians.org/c/eips/5) with the title “Hegota Headliner Proposal: [title of EIP]” and tag the post with the [hegota](/tag/hegota) tag.**

- Summary (ELI5): Concise, plain-language explanation of the proposal, why it matters, and who directly benefits.
- Champion: point-of-contact for the EIP
- Detailed Justification:

 What primary and secondary benefits exist, ideally supported by data or clear rationale?
- Clearly articulate “Why now?”—Why prioritize this feature today?
- Justify this specific approach compared to alternative solutions (considering lower risks, higher value).

**Stakeholder Impact:**

- Positive: Identify beneficiaries clearly and document explicit support.
- Negative: Identify potential negative impacts, document objections, and describe mitigations or accepted trade-offs.

**Technical Readiness:** Assess technical maturity clearly, providing links to specifications, tests, and client implementations.

**Security & Open Questions:** Document explicitly known security risks, open issues, or unclear aspects. Include threat models, preliminary audit plans, or next steps.

---

* It should be noted that any headliner proposals which are not selected for the fork cannot later be re-proposed as a non-headlining feature. Once DFI’d, the feature must wait until the next fork to be proposed again.

## Replies

**abcoathup** (2025-12-23):

### Fork focus

As part of headliner proposals, we should explicitly [define the focus](https://ethereum-magicians.org/t/community-consensus-fork-headliners-acd-working-groups/24088#p-58740-defining-the-fork-focus-4) for Hegotá.

- Scale L1
- Scale L2
- UX
- DX
- Decentralization

Examples from: [Community Consensus, Fork Headliners & ACD Working Groups](https://ethereum-magicians.org/t/community-consensus-fork-headliners-acd-working-groups/24088#p-58740-defining-the-fork-focus-4)

> Scalability & Lower Fees: Meaningfully increase throughput, lower transaction costs, and unlock new use cases.
>
>
> Developer & User Experience: Simplify protocol complexity, enhance smart contract security, and reduce development friction.
>
>
> Security & Resilience: Strengthen the network’s security posture, enhance attack resistance, and mitigate emerging threats without compromising decentralization or censorship resistance.


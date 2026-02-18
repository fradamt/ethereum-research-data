---
source: ethresearch
topic_id: 22096
title: Fee structure for EXECUTE-precompile
author: josojo
date: "2025-04-06"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/fee-structure-for-execute-precompile/22096
views: 373
likes: 2
posts_count: 9
---

# Fee structure for EXECUTE-precompile

# Fee structure for EXECUTE-precompile - And Ethereum’s Value Accrual.

## Abstract

As Ethereum transitions toward a rollup-centric architecture, it faces a key challenge in ensuring sustained value accrual for Ether. While the proposed “EXECUTE-precompile” would enable rollups to inherit Ethereum’s security by allowing on-chain re-execution of rollup state transitions, there is a risk that fee-optimized rollups don’t opt-in by default, and only do “emergency” calls, which render traditional gas-based fees inadequate. This article outlines a fee structure, enforced by a Fee Determining Contract (FDC), that imposes continuous usage charges rather than occasional dispute-driven fees. By consolidating all EXECUTE calls into a single gatekeeper contract, requiring permissionless upfront registration, enforcing sequential verification of states, and levying proportional fees based on actual rollup usage, the design ensures robust economic alignment between L2 rollups and Ethereum’s security. The resulting system offers both a compelling value proposition to rollups—which benefit from strong, upgradable Ethereum-level security—and a predictable, sustainable revenue stream for Ether, thereby reinforcing Ethereum’s long-term security budget in an increasingly rollup-dominated ecosystem.

# Introduction

## Ethereum’s decision for L2 roadmap:

Ethereum’s Layer 2 roadmap emphasizes scaling via rollups, pushing much of user activity off the main chain to the L2s. This improves throughput, allows sequencer customization and many other benefits, but raises questions about Ether’s long-term fee revenue and security budget.

## The EXECUTE-precompile:

The [EXECUTE-precompile](https://ethresear.ch/t/native-rollups-superpowers-from-l1-execution/21517) is a theoretical feature on Ethereum’s roadmap that lets validators directly re-execute a rollup’s EVM logic at L1. This mechanism would offer “native” Ethereum security, eliminating the need for complex fraud proofs or specialized zk-verifiers. However, if it’s only invoked during controversies, rollups could avoid paying meaningful fees most of the time.

## Ethereum’s value accrual dilemma:

Today, Ethereum largely charges fees based on gas usage. When activity is low, gas prices drop near zero. Because rollups handle most transactions, L1 might see little congestion and thus collect minimal fees. Meanwhile, alternative data-availability layers threaten Ethereum’s fee dominance. The moat of Ethereum’s data-availability is rather [thin](https://x.com/dankrad/status/1900278057543291126), as other solutions could always provide cheaper data-availability and in case of a controversy, the applications can still fall back to ethereum’s data availability to resolve all failures. If Ethereum can’t offer a compelling reason for L2s to pay, Ether’s long-term security budget may suffer.

# Design:

To ensure Ethereum accrues meaningful fees from the EXECUTE-precompile, we propose a Fee Determining Contract (FDC) that acts as an unavoidable gatekeeper for all EXECUTE calls. Below is a more detailed breakdown of how it addresses the fee problem:

**1. Single Authorized Caller**

• Mechanism: The FDC-contract designates itself (or a specific proxy) as the only valid caller of the EXECUTE-precompile. No other contract or externally owned account (EOA) can directly invoke EXECUTE.

• Rationale: By consolidating all EXECUTE calls into a single contract, Ethereum can uniformly manage and meter access. Rollups cannot bypass the contract’s rules or fees.

**2. Mandatory Registration & Waiting Period**

• Mechanism: Every rollup—or “chain” seeking to use EXECUTE—must register with the FDC-contract, pay a substantial upfront fee, and wait a predefined “cooldown” (e.g., one month) before it can make the first EXECUTE call.

• Rationale: This large upfront deposit dissuades projects from employing the EXECUTE-precompile only in rare emergencies or optimistically, like an optimistic rollup. The waiting period further reduces exploitative “last-minute” usage. Essentially, if a chain truly wants Ethereum-grade security, it must commit financially and operationally over the long term.

**3. Enforced Sequential Verification**

• Mechanism: Once registered, a chain can submit states for verification via the EXECUTE call. However, each new verification must build on the last “root hash” confirmed by the contract. If a chain tries to skip certain checkpoints or produce partial proofs, the contract rejects it.

• Rationale: This compels continuous usage: each rollup state transition must be verified in sequence, rather than “optimistically ignoring” most states and only verifying in emergencies. Over time, this regular usage ensures consistent fee inflows for Ethereum.

**4. Fee Extraction**

• Mechanism: Because the FDC-contract sees the rollup’s state transitions, it knows the size of the trace each rollup processes (via the trace of the EXECUTE-Precompile). It can levy a small fee on this trace size based on staker-set parameters.

• Rationale: By charging fees tied to actual L2 usage, Ethereum can capture a proportional share of the economic value generated. This might be implemented with a flexible auction mechanism, staker governance (similar to block gas limit governance), or other dynamic pricing to ensure fairness and competitiveness.

# Evaluation:

## Moat:

Ethereum’s security is a valuable commodity that credible L2s will seek. It’s unlikely that the migration of trade-fi to crypto ends up on a “second-class” rollup not utilizing the new EXECUTE-precompile. The EXECUTE-precompile will be the only L2-verification mechanism that forks, in case there is an implementation bug in the L2 validation calculation. Hence, any rollup leveraging the precompile directly ties itself to Ethereum’s robust security guarantees. Additionally, because the EXECUTE-precompile can evolve in parallel with Ethereum’s own upgrades (such as protocol forks or improvements to the precompile), it reduces the risk for rollups of early ossification or the need for potentially insecure updates through private keys or DAOs.

Because the proposed fee mechanism requires continuous rent payments—rather than occasional, “emergency-only” calls or optimistic validations—rollups can’t exploit Ethereum’s security without paying. They can’t simply “go elsewhere” for cheap data availability and only revert to Ethereum in times of crisis. In this sense, the fee mechanism creates a strong economic moat for Ethereum security.

## Expected Rent:

With the FDC-contract in control of EXECUTE usage, Ethereum stakers (or another on-chain governance entity) can regularly adjust fees to balance network growth and revenue capture. Over time, a portion of L2 revenue is channeled back to Ethereum, strengthening its security budget. By extracting a measured share of all L2-generated value, Ethereum sets itself up for long-term financial sustainability in a rollup-driven ecosystem.

## Alignment:

Charging only a fraction of each L2’s revenue fosters a healthy alignment of interests. As L2s prosper, Ethereum’s security—funded in part by these fees—also grows stronger. In effect, Ethereum’s success is tied to the success of the entire L2 landscape. And because L2s rely on Ethereum’s security, paying these fees is in their best interest: robust security underpins the trust that enables L2 adoption.

# Conclusion:

The EXECUTE-precompile could be Ethereum’s key to ensuring that L2 activity eventually funnels meaningful fees back to L1. By requiring upfront registration and continuous verification through the FDC-contract, rollups have no choice but to pay for the robust security Ethereum provides. Though there are open questions around exact fee mechanics, this design sketches a path to sustained value accrual for Ether in an increasingly rollup-centric future.

This approach is more promising than data-availability charging, as it creates a stronger economic moat

By aligning incentives and enforcing mandatory registration and ongoing usage fees, the ecosystem can ensure both L2 scalability and a healthy security budget for Ethereum itself.

**Note:**

People might argue that it is unethical to charge L2s. My personal view is that it’s okay to charge for a service provided. And it’s far better to charge L2s for the security they consume, instead of trying to scale L1 indefinitely for value accrual—an approach that is ultimately worse from a technical standpoint.

**Referral:** If you talk about it on X, please tag me: [o_herminator](https://x.com/o_herminator).

## Replies

**sm-stack** (2025-04-06):

Why are you trying to ban optimistic rollups to use the EXECUTE precompile?

---

**josojo** (2025-04-07):

I am not banning them! The proposal just makes them pay the same as other rollups that wanna use the EXECUTE-precompile for every verification, such that everyone pays their share.

---

**MicahZoltu** (2025-04-07):

The purpose of gas fees is to charge for the operational cost of using Ethereum, not to extract rent from users.  If a rollup only uses Ethereum once a year, then they should be charged for that usage once, not for the year of backstopping Ethereum provided.

---

**josojo** (2025-04-07):

This is how it has been in the past. But I disagree that it should stay this way!

I think this new fee structure would be a win, win for all. A fee that secures value accrual to Ethereum will give Ether the value to secure all the L2. L2’s can’t operate with the same security, if there is no such fee mechanism, unless we all believe in Ethers ultrasound “store of value”.

For Ethereum its better to extract some L2 rent, rather focusing on the wrong scaling theory (Scaling L1 for more Ethereum fees rather L2 ) and thereby implicitly charging a rent via higher L1 fees.

---

**kladkogex** (2025-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> This mechanism would offer “native” Ethereum security, eliminating the need for complex fraud proofs or specialized zk-verifiers.

Why do you say “eliminate” ?  It is a bad idea imho to redo ALL state computation on the mainnet. Wasnt the entire purpose of rollups then? If the mainnet does both consensus and state computation why need rollups at all?

---

**josojo** (2025-04-11):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> It is a bad idea imho to redo ALL state computation on the mainnet. Wasnt the entire purpose of rollups then?

We would only do the computation verification via zk tech via a standardised zk-tech provided by the EXECUTE-precompile. Hence, I am saying that we “eliminate specialised zk-verifiers”. Feel free to look up the details in the EXECUTE-precompile [spec](https://ethresear.ch/t/native-rollups-superpowers-from-l1-execution/21517).

---

**kladkogex** (2025-04-11):

Hey Josojo,

Can you please provide a link to the spec—where is it? Our team would be happy to review it; it’s an interesting idea, and we’d like to see how we can use it.

Maybe I missed the link to the spec. The only thing I see is a post from Justin Drake with some thoughts. I read it, but it seems incomplete in terms of information, so it’s hard to provide comments.

[![image](https://ethresear.ch/uploads/default/optimized/3X/9/d/9d71368066ef56dd1963b41ceb107102ed0091bc_2_619x500.png)image2007×1619 403 KB](https://ethresear.ch/uploads/default/9d71368066ef56dd1963b41ceb107102ed0091bc)

The statement above seems to contradict what you’re saying, because it states that transactions are **executed**, not **verified**, as you claim.

I would suggest augmenting your post to make it easier to understand and more coherent, possibly by providing additional references.

---

**josojo** (2025-04-11):

Justin post provides two ways in his original post: ( **enforcement by SNARKs**) and ( **enforcement by re-execution**) are the titles of the section. I was referring to the enforcement via SNARKs when I was talking about verifying.


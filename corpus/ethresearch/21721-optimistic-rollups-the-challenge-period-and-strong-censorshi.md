---
source: ethresearch
topic_id: 21721
title: Optimistic rollups, the challenge period and strong censorship attacks
author: donnoh
date: "2025-02-11"
category: Layer 2 > Optimisitic Rollup
tags: []
url: https://ethresear.ch/t/optimistic-rollups-the-challenge-period-and-strong-censorship-attacks/21721
views: 1142
likes: 12
posts_count: 9
---

# Optimistic rollups, the challenge period and strong censorship attacks

*Many thanks to [Vitalik](https://x.com/VitalikButerin) (EF), [Justin](https://x.com/drakefjustin) (EF), [Kelvin](https://x.com/kelvinfichter) (OP) and [Gabriel](https://x.com/GCdePaula_) (Cartesi) for feedback and discussion.*

The goal of this post is to bootstrap a discussion around a **socially agreeable challenge period lower bound for optimistic rollups** and, by consequence, around Ethereum’s strong censorship resistance guarantees.

Today, optimistic rollups add up to [91.9%](https://l2beat.com/scaling/tvs) of the total value secured by all rollups. We (L2BEAT), [recently](https://forum.l2beat.com/t/stages-update-a-high-level-guiding-principle-for-stage-1/338?u=donnoh) started to enforce a ≥7d challenge period requirement to be classified as Stage 1, which has sparked a [debate](https://x.com/tyneslol/status/1885297674817331469) on where this number comes from and how we can assess if it is appropriate. We feel it’s time to better formalize this value and either update it or ratify it as the community standard, as some projects have already [started](https://github.com/ethereum-optimism/specs/discussions/191#discussioncomment-12032036) to [argue](https://x.com/RiscZero/status/1857432353397776401) that lower challenge periods might be equivalently safe.

# Why do we have the 7d challenge period in the first place?

The biggest misconception around challenge periods is the belief that they are set based on the time it takes to perform the interaction between two parties in a multi-round challenge. If the number of interactions is reduced, at the extreme to 1 with non-interactive protocols ([example](https://l2beat.com/scaling/projects/morph#state-correctness)), it is sometimes suggested that the challenge period can be significantly reduced too.

The reality is that the challenge period [has been originally](https://www.youtube.com/live/TVhyiGfYgVM?si=yCVcAbqsmGcRD9An&t=7864) set to **allow a social response in case of a 51% consensus attack and prevent funds from being stolen**. It’s important to note that, on L1, a strong censorship attack **cannot** cause funds sitting on a simple account to be stolen.

As far as we know, the details of such social response have never been precisely discussed.

# Background: how optimistic rollups keep track of time

There are two main ways optimistic rollups keep track of the time left to participate in a challenge: either with a **global timer**, or with a **chess clock model**. The first type is the simplest form and it is mainly employed by single-round challenge protocols.

The second type is used by **multi-round protocols** such as [OPFP, BoLD or Dave](https://medium.com/l2beat/fraud-proof-wars-b0cb4d0f452a), to prevent the attacker from wasting the honest players available time by not acting when it’s their turn. In practice, for each challenge two clocks are created, one for the asserter and one for the challenger, and the time from a clock is consumed only when it’s its owner time to make a move, and stops from getting consumed when it’s the other player’s turn. If a clock runs out of time, the other players win.

[![image](https://ethresear.ch/uploads/default/optimized/3X/7/d/7d711fd0b9eea5453845442dd020562b50dae38c_2_690x235.jpeg)image2048×698 143 KB](https://ethresear.ch/uploads/default/7d711fd0b9eea5453845442dd020562b50dae38c)

**Funds can be compromised when honest players cannot perform their moves due to a strong censorship attack, causing their clocks to expire.**

In this post we’ll focus on the chess clock model, as it represents most projects and because the global timer model case can be trivially deduced from it.

# Tentative social response in case of strong censorship attacks

For simplicity, let’s assume that censorship is sustained, i.e. it is performed with no breaks. Moreover, **we assume L1 rollbacks and L1 rollup-specific invalid state transitions to be a highly controversial and not desirable social response** that should be avoided where possible.

We sketch the following timeline:

- (0h → 24h): a 51% strong censorship attack is detected.
- (24h → 6d): a hard fork is coordinated, implemented and activated to slash censoring validators.
- 1d: the time left on the honest players’ clock to play the game.

This social response successfully prevents a “51%” attack on optimistic rollups with no rollbacks only if all of the following hold true: (1) **we are able to detect censorship within 24h**; (2) **we are able to coordinate, implement and activate a hard fork within 5d**; (3) **challenge protocols are efficient enough such that they can be played by consuming less than 1d when no censorship is present**.

There is a caveat though: the above is true if we take the “51%” value literally, while it fails if the attack gets reiterated even after the hard-fork (…76% attack?). A simple solution is to allow contracts to query the timestamp of the latest hard-fork and extend clocks if necessary, but it requires a protocol upgrade.

In practice, an attacker can just delay the honest party’s transactions such that the clock expires before the last move is made. Assuming ~70 steps (as in Arbitrum’s BoLD) needed to reach the final step, where 35 would be executed by the honest parties, and clocks of 7 days, the attacker can delay each move by ~5 hours every ~5 hours, consuming both its own clock and the honest party’s clock. For the above timeline to hold, we should be able to detect such censorship attacks within 1 day too.

# The alternative: socially accept that (endgame) optimistic rollups are less secure than (endgame) ZK rollups

Today, Ethereum provides [around $100B](https://beaconcha.in/) of economic security, which is around 2x the total value secured by all L2s settling on Ethereum. **We might accept strong censorship attacks to be extremely unlikely and abandon the idea that optimistic rollups should remain safe around them.** In this case, the challenge period only needs to be long enough to protect from soft censorship attacks (i.e. builder-driven) and provide enough time to compute the necessary moves.

Let’s say we want optimistic rollups to be safe up to 99% soft censorship attacks while considering a 99.99% inclusion probability: we then would need to provide [at least 3h](https://www.inclusion.watch/) for each tx to be included on L1, and given ~35 steps needed per player to complete an interactive challenge, we’d need to provide at least ~4.5d. The activation of FOCIL would provide [much more significant results](https://x.com/soispoke/status/1876232740347265388) and potentially reduce the period, under this threat model, to a safe value of just a couple of days.

# Addendum: resources on strong censorship detection

**Vitalik Buterin (2017): [suspicion scores](https://ethresear.ch/t/censorship-rejection-through-suspicion-scores/305)**

Calculate the longest amount of time that the client has seen that a vote could have been included in the chain but was not included, with a “forgiveness factor” where old events are discounted by how old they are divided by 16.

Some modifications to Casper FFG to extend epochs if not finalized are proposed.

**Vitalik Buterin (2019): [responding to 51% attacks in Casper FFG](https://ethresear.ch/t/responding-to-51-attacks-in-casper-ffg/6363)**

Discusses attester censorship and automated soft forks in response.

**Vitalik Buterin (2020): [timeliness detectors](https://www.notion.so/Optimistic-rollups-the-challenge-period-and-strong-censorship-attacks-18f094a2aee7804d9d3ded2f346a42b4?pvs=21)**

The explicit goal is to detect 51% attacks, identify the “correct” chain and which validators to “blame”. The mechanisms tries to identify blocks that arrived unusually late, with a commonly agreed synchrony bound. It involves introducing the concept of a timeliness committee to achieve agreement.

**Sreeram Kannan (2023): [Revere](https://www.youtube.com/watch?v=_7PtU1IiOoY), an observability gadget for attester censorship in Ethereum**

It’s much easier to resolve from proposer censorship because even a small fraction of honest proposer can provide censorship resistance. Much harder to protect from attester censorship. Solution: increase observability of uncle blocks. How? Not easy to distinguish uncle blocks because of censorship or network censorship. Add rule: a proposer has to include transactions from uncle blocks. Use light clients that enhance observability for everyone by tracking headers.

**Ed Felten (2023): [onchain censorship oracle](https://www.youtube.com/watch?v=DbWvfHGh_Ak&t=954s)**

Onchain censorship detection. The test says that either there as not been significant censorship, or maybe there has been censorship. Idea: measure onchain the number of empty (consensus) slots. With confidence level of p=10^-6, and assuming 10% of honest proposers, you can report censorship if there are more than 34 empty slots out of 688. Issue: the adversary can wait to launch the attack until it knows that the next 64 proposers will all be malicious. Mitigation: add 64 slots to the length of the test. Another issue: if the test fails, you might want to do it again over the following n blocks, but that’s unsound (p-hacking). Mitigation: if we want repetition then each test needs to have more confidence. Abandoned in 2024 because of some attack vector.

## Replies

**terence** (2025-02-11):

It may be cleaner to break this into two parts:

1. How much time does one have to open a challenge
2. How much time does one have to complete a challenge before the timer runs out

I think the main question here is whether we can reduce the time for the happy case. If a challenge exists, giving it 7 days is fine

---

**potuz** (2025-02-11):

What are your thoughts on an enshrined oracle for censorship? this could be made part of the state transition of honest nodes counting attestations patterns and missing blocks to simply keep a value on chain indicating that strong censorship is occurring. Rollup bridges could subscribe to this oracle and pause trustlessly. The oracle being too lax allows a weak attacker to grief these rollups, while being too strict could fail to detect censorship. It’s a stronger version of [@edfelten](/u/edfelten)’s oracle on-chain since nodes have access to consensus layer information.

---

**qizhou** (2025-02-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/donnoh/48/12917_2.png) donnoh:

> The alternative: socially accept that (endgame) optimistic rollups are less secure than (endgame) ZK rollups

One note is that with 66.7% voting power, Ethereum can revert any finalized blocks and thus potentially double-spend any ZK rollup finalized L1 withdraws.

![](https://ethresear.ch/user_avatar/ethresear.ch/donnoh/48/12917_2.png) donnoh:

> Let’s say we want optimistic rollups to be safe up to 99% soft censorship attacks while considering a 99.99% inclusion probability: we then would need to provide at least 3h  for each tx to be included on L1, and given ~35 steps needed per player to complete an interactive challenge, we’d need to provide at least ~4.5d. The activation of FOCIL would provide much more significant results  and potentially reduce the period, under this threat model, to a safe value of just a couple of days.

If we can use multi-section fault proof using EIP-4844 BLOB to carry 4095 intermediate trace hashes per challenge tx, each player will need **up to 4 steps** (total 8 steps with 4096^8=2^96 maximum trace size) to complete a challenge.

---

**donnoh** (2025-02-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> One note is that with 66.7% voting power, Ethereum can revert any finalized blocks and thus potentially double-spend any ZK rollup finalized L1 withdraws.

The point here concerns the direct stealing of funds, not double-spending. With an (endgame) ZK rollup you cannot steal funds from simple accounts even when 99% of validators are malicious, while with an Optimistic Rollup with an insufficient challenge period it’s enough to control 51%.

---

**Po** (2025-02-12):

In the happy case, using OPFP as an example, approximately 70 steps (similar to Arbitrum’s BoLD) are needed to reach the final step. Each step takes one of two forms: [output root challenge](https://specs.optimism.io/glossary.html#l2-output-root) or execution trace challenge. Only the root claim challenge of the execution trace is time-intensive, taking less than 3 hours, while the others typically complete in under 5 minutes.

---

**Po** (2025-02-12):

Great write-up! The 7-day challenge period seems somewhat arbitrary, especially considering that the DAO fork took nearly a month to resolve.

---

**MicahZoltu** (2025-02-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> One note is that with 66.7% voting power, Ethereum can revert any finalized blocks

Clients will not automatically reorg past a finalized block.  Every user running a fully validating node would have to manually go in and revert to before the finalized block.  Anyone whole node has pruned old state would have to respect from the P2P network.

Essentially, the only way to undo finality is via social layer.  It cannot be done automatically.

---

**rami** (2025-10-31):

The idea that community-driven forks can deter or even circumvent the effects of a 51% attack that affects rollups needs much more rigorous justification before it can be accepted as the reason for why 7 days is still necessary.

If one considers Ethereum practically susceptible to a 51% attack in their threat model, and wants to account for such a scenario, the more realistic approach is to inherit the combined economic securities of Ethereum and other major chains. Just as we are working towards multiple proof systems and multiple dispute games for redundancy, multiple dispute publication avenues are the next rational step. In such a design, assuming a (ZK) trustless bridge is active between Ethereum and the other chains, before one can finalize any state proposal, they must prove that there were no unanswered dispute moves on other chains that could invalidate the proposal being finalized. My ballpark estimate is that the proving cost for this (e.g. using a library like STEEL) would be a fraction of running a full ZK rollup, assuming the ZK bridge proving cost is external to the system of course (e.g. Signal proofs).

However, even with say $3T in economic security, and a non-interactive one-move dispute protocol like Kailua that requires only one transaction per dispute period to defend against any size attacks in say a few hours as you estimate, Rollups should only reduce their dispute periods to less than a day if they’re operating at a very high level of proposer redundancy, diversity, and decentralization. We’ve seen what kind of carnage events like AWS downtime can do.

Honestly, we’d like to invite the broader community to a regularly scheduled open call about this issue. While there have been numerous touch and go discussions across different forums, aligning on the principles of deciding appropriate dispute periods, and working towards optimizing them responsibly should be a broader and more focused collaboration. If that sounds interesting, please [let me know](mailto:rami@boundless.network?subject=7D%20Challenge%20Window).


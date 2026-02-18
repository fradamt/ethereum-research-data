---
source: ethresearch
topic_id: 3777
title: Verifiable delay functions and RANDAO manipulability
author: jamesray1
date: "2018-10-12"
category: Proof-of-Stake
tags: [random-number-generator]
url: https://ethresear.ch/t/verifiable-delay-functions-and-randao-manipulability/3777
views: 2980
likes: 3
posts_count: 3
---

# Verifiable delay functions and RANDAO manipulability

I remember months ago [@JustinDrake](/u/justindrake) was looking into Verifiable delay functions after or around the time of the RANDAO manipulability analysis. What was the outcome of that research? (There are no search results in this site.) Skimming the [spec](https://github.com/ethereum/eth2.0-specs/blob/master/specs/beacon-chain.md) again, I see it mentions related stuff like slashing for early reveals and hardening for orphaned reveals. I skimmed https://eprint.iacr.org/2018/601.pdf, a VDF that doesn’t require a trusted setup in an optimal, performant way could use “the class group of an imaginary quadratic order [20], which is an efficient group of unknown order with a public setup [50].” (p. 22, section 7)

## Replies

**jamesray1** (2018-10-12):

Ah, I found [Verifiable delay functions and attacks](https://ethresear.ch/t/verifiable-delay-functions-and-attacks/2365). Also for reference for others there is [RANDAO beacon exploitability analysis, round 2](https://ethresear.ch/t/randao-beacon-exploitability-analysis-round-2/1980).

---

**JustinDrake** (2018-10-12):

See [Minimal VDF randomness beacon](https://ethresear.ch/t/minimal-vdf-randomness-beacon/3566). We’re planning to use the Wesolowski VDF with an RSA modulus obtained via an MPC (in a similar vein to Zcash’s Powers of Tau). Class groups are an option but have tradeoffs.


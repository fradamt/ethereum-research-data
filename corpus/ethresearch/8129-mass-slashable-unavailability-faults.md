---
source: ethresearch
topic_id: 8129
title: Mass-slashable unavailability faults
author: JustinDrake
date: "2020-10-19"
category: Sharding
tags: []
url: https://ethresear.ch/t/mass-slashable-unavailability-faults/8129
views: 2356
likes: 1
posts_count: 4
---

# Mass-slashable unavailability faults

**TLDR**: By combining data availability sampling and proofs of custody we show how to make unavailability faults mass-slashable without social slashing. (This is similar to FFG safety faults where 1/3 of validators are slashable without social slashing.) We also address the data availability sampling validator dilemma.

**Construction**

First require that validator chunk queries as part of data availability sampling are done using deterministic randomness instead of non-deterministic local randomness. (Deterministic randomness can be achieved using BLS signatures as a VRF similarly to RANDAO mix shares in phase 0.) Next, add a proof of custody to the chunks. For example, a  `chunk_custody_bit` which covers all the data availability sampling chunks between `source` and `target` is added to [AttestationData](https://github.com/ethereum/eth2.0-specs/blob/0f2fcac133e98e3bad43677714f5251f6d441d07/specs/phase0/beacon-chain.md#attestationdata).

**Discussion**

If a data availability faut occurs, i.e. a finalised beacon block points to unavailable shard data, at least 2/3 of all validators must have attested to unavailable data. At most 1/3 of all validators are controlled by an attacker performing a data withholding attack so 1/3-ε of all validators made an attestation without custody of the corresponding data availability sampling chunks (the ε accommodates for the small portion of validators the attacker can fool with data availability sampling). With a single custody bit roughly half of those validators (i.e. about 1/6 of all validators) are liable to get slashed.

Notice also that the `chunk_custody_bit` prevents lazy validators from following other validators (“the herd”) and attesting without first doing data availability sampling. In other words, the chunk custody bit addresses the data availability sampling validator dilemma.

## Replies

**technocrypto** (2020-10-19):

Are observers able to detect incorrect custody bits without access to the unavailable data?  Or can dishonest validators only be slashed by someone possessing the withheld data?

---

**JustinDrake** (2020-10-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> can dishonest validators only be slashed by someone possessing the withheld data?

Dishonest validators can be slashed by anyone. There is no need to possess the withheld data (if there even is withheld data).

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> Are observers able to detect incorrect custody bits without access to the unavailable data?

Observers are able to detect when finalised data is unavailable. They can then infer that some portion of the validators that participated to finalise the unavailable data (e.g. ~1/4 of such validators, assuming a 1/3 attacker withheld data) are slashable, and proceed to challenge them.

---

**dankrad** (2020-10-20):

I want to summarize a modification of this proposal that combines the idea with [A 0.001 bit proof of custody](https://ethresear.ch/t/a-0-001-bit-proof-of-custody/7409). Basically, as suggested in the proposal by [@JustinDrake](/u/justindrake) above, we make data availability sampling deterministic using the BLS signature vrf construction. Each chunk is then used to compute one custody but according to the 0.001 bit proof of custody construction; if any of the bits is one, the validator cannot sign an attestation in the next epoch or they become slashable. We adjust the number of bits in the construction so that the probability of the bit being one in any of the chunks is approximately 1/1000.

This addresses the “lazy validator dilemma” that the rational behaviour is to not check any chunks as it’s overhead with no reward. It does however not guarantee that a large fraction of validators will get slashed if a data availability fault occurs. However, I argue that we get properties that are nearly as good:

1. One attack vector are temporary withholding attacks which can be leveraged through lazy validators. The attacker has less than 67% stake but is able to produce blocks with withheld data that get finalized due to lazy validators. They later publish this data and thus the fork choice rule can suddenly change for honest nodes that have previously ignored the finalized block.
This attack becomes much less likely as rational validators will now do data availability sampling, since the penalty for missing a custody-1 chunk is very high.
2. A dishonest majority validator can permanently withhold some piece of information on the finalized chain. Honest and rational validators will start building an alternative chain as the finalized chain is invalid on data availability grounds. Note that the attacker cannot switch to the honest chain without getting slashed, as they would have to make a vote that violates the FFG rules to do so. They are thus stuck on their chain at least until the honest chain finalized, and will thus lose most of their deposit from inactivity leaks on the honest chain.


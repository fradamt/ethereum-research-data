---
source: magicians
topic_id: 8917
title: Discussion thread for single-slot finality
author: vbuterin
date: "2022-04-14"
category: Magicians > Primordial Soup
tags: [consensus-layer, finality]
url: https://ethereum-magicians.org/t/discussion-thread-for-single-slot-finality/8917
views: 3727
likes: 8
posts_count: 7
---

# Discussion thread for single-slot finality

See: [Paths toward single-slot finality - HackMD](https://notes.ethereum.org/@vbuterin/single_slot_finality)

## Replies

**Olshansky** (2022-04-21):

> The “interface” between Casper FFG finalization and LMD GHOST fork choice is a source of significant complexity, leading to a number of attacks that have required fairly complicated patches to fix, with more weaknesses being regularly discovered. Single-slot finality offers an opportunity to create a cleaner relationship between a single-slot confirmation mechanism and the fork choice rule (which would only run in the ≥ 1/3 offline case). Other sources of complexity (eg. shuffling into fixed-size committees) could also be cut.

**Overall excerpt goal**: Reduce complexity.

**Bringing attention to**: `fork choice rule (which would only run in the ≥ 1/3 offline case)`.

**My thoughts**: Simply having the code / implementation in place for the fork choice rule is complex (implementation, documentation, testing, attack vectors, integration, etc…).

**Short proposal**: If byzantine safety cannot be achieved within some timeout due to offline / unresponsive validators, is dynamically reducing the validator set and defaulting to Casper FFG an option? The tradeoff we’re making is architectural and implementation simplicity over security, but software complexity also comes with a big cost. *Note that I have not read the “Combining GHOST and Casper” paper, so let me know if the answer lies in there.*

> The fork choice rule (LMD GHOST) is only used in the exceptional case where a committee doesn’t confirm (this requires >1/4 to be offline or malicious).

What is the source of the “1/4” figure?

> Most of the time, validators could withdraw instantly.

Does this imply withdrawing staked funds or withdrawing as a validator actor?

> The biggest problem that remains is signature aggregation. There are 131,072 validators making and sending signatures, and these need to be quickly combined into a single large aggregate signature.

What is the source of the load?

1. Computation related to validation of each individual signature?
2. Networking requirements related to flooding the network with > 100K non trivially sized payloads?
3. Computation related to signature aggregation?

**Background**: I’m asking this question for a personal reason since the next version of our team’s protocol will use Hotstuff and will require threshold signature that aggregate > 100K signatures. Theoretically, it is looking to me that linear networking requirements with BLS signatures might be a viable solution here, but I’m looking to build more context.

---

**vbuterin** (2022-07-01):

> What is the source of the “1/4” figure?

Assuming that the validator set rotates 1/4 each time. The protocol I described there relies on “stitched validator sets”, where finality could break if two consecutive validator sets sign conflicting data. Hence you have to set the threshold to 3/4, so you have 1/4 liveness fault tolerance, and 1/4 safety fault tolerance because 1/2 minus 1/4 difference from rotation.

> Does this imply withdrawing staked funds or withdrawing as a validator actor?

Withdrawing staked funds.

> What is the source of the load?

Signature validation is just ECADDs and turns out to be not that hard. Aggregation is the bigger challenge. We have lots of signatures flying around lots of p2p subnets, and it’s pretty expensive data-wise though there are ways to optimize it.

---

**Olshansky** (2022-07-04):

> Assuming that the validator set rotates 1/4 each time

**Q1**: Do we rotate the validator set simply because it’s too large to have everyone vote on every block?

> where finality could break if two consecutive validator sets sign conflicting data

**Q2**: If we were to sacrifice some liveness through increased block times in exchange for larger validator sets, would we not be able to have all the validators participate in every round and just ommit this problem altogether?

> We have lots of signatures flying around lots of p2p subnets, and it’s pretty expensive data-wise though there are ways to optimize it.

**Q3**: My thoughts/experience point me to either FROST DKG or BLS signature aggregation. Wanted to know if that’s what you had in mind or something else I should research?

---

***Disclosure**: Though these comments are relevant in the context of Ethereum, my motivation is to transfer the learnings over to the research and prototyping of v2 of the protocol my team is working on. Happy to be an open book upon request but don’t want to add noise here.*

---

**vbuterin** (2022-07-06):

Q1: the purpose of having supercommittees at all is to avoid everyone having to vote on every block. But once you have supercommittees, the purpose of rotating them is to make sure that everyone has a fair chance of being on a supercommittee about the same percent of the time as everyone else.

Q2: yeah this is certainly a viable path.

Q3: we’re already planning to optimize the heck out of BLS signature aggregation for this!

---

**kladkogex** (2022-07-06):

> Today, there are ~285,000 validators, accounts that have deposited 32 ETH and as a result can participate in staking. Validators do not correspond one-to-one to users: wealthy stakers may control many hundreds of validators.

I think the reality of where everything is going is that out of these 285,000 validators, 50%+ percent is controlled by Coinbase, Binance, and LIDO, and, an unfortunate fact is that the centralization only keeps increasing.

At some point Coinbase will fork the agent, and run all 50,000 “agents” in one real agent.

The fork is pretty simple - just sign 50,000 times using different keys and submit the signatures from a single agent.

---

**frisitano** (2022-08-10):

I wonder if you are aware of the recent research produced by the web3 foundation on succinct light clients that leverage BLS finality votes.  A high level description of the scheme is that a zk proof is produced that attests to the fact that some subset (e.g. 2/3) of a validator set has signed off on the finality of a block.  The scheme leverages BLS signature aggregation and has support for validator set rotation.  It is claimed that the scheme is efficient - proofs can be produced in ~ms and therefore can keep up with finalised tip.   It is suggested that the scheme can scale to 100,000’s of validators.

The produced zk proof can then be used for bridging.  This is of particular importance now that Ethereum have committed to the rollup-centric roadmap as rollups will benefit from a way to trustlessly bridge assets from Ethereum to the rollup.  Under this model the finality proof could be verified on the rollup in the zkvm.  Web3f recently uploaded a paper and supporting code to github, you can find it here [apk-proofs/Light Client.pdf at main · w3f/apk-proofs · GitHub](https://github.com/w3f/apk-proofs/blob/main/Light%20Client.pdf).

I wonder if it would be worth considering incorporating something similar into the proposed finality model.


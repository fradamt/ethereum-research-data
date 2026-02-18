---
source: ethresearch
topic_id: 5871
title: Open Research Questions For Phases 0 to 2
author: adlerjohn
date: "2019-07-25"
category: Sharding
tags: []
url: https://ethresear.ch/t/open-research-questions-for-phases-0-to-2/5871
views: 4665
likes: 16
posts_count: 7
---

# Open Research Questions For Phases 0 to 2

In light of the recent [Reddit AMA with the Eth 2.0 research team](https://redd.it/cdg8v6), there has been a lot of excitement around the idea that [there are no outstanding unsolved research challenges remaining](https://twitter.com/TrustlessState/status/1150774907107569665) that would block implementing and deploying phases 0–2 of Eth 2.0. As a counterpoint, this post aims to summarize potential open research questions needed before phase 2 can actually be deployed responsibly. This is intended to drive conversation and stimulate discussion around these issues to hopefully resolve them.

## Relayer System

Due to the use of [stateless clients](https://ethresear.ch/t/the-stateless-client-concept/172) (which is a necessity in a sharded system, as having every client storing and updating state would make the system isomorphic to a single chain), transactions require a *witness* attached to them, proving the pre-state and post-state of the transaction.

Unfortunately, it turns out that providing these witness without having to do a full-sync of a shard for each transaction requires keeping state around. The actors in Eth 2.0 that have this job are *relayers* (or *state providers*). An excellent summary of the history of the multitude of designs that have been considered for a relayer network can be found [here](https://ethresear.ch/t/state-providers-relayers-bring-back-the-mempool/5647).

Agreement among various researchers for this relayer network is not yet unanimous. This is for good reason: existing proposals make a number of differing tradeoffs w.r.t. centralization/monopoly potential, incentives, performance, etc. An excellent summary of such tradeoffs can be found [here](https://github.com/ethereum/eth2.0-specs/issues/1309).

This topic has been the subject of active back-and-forth among the research community and it appears that there are resources allocated towards it, so hopefully a resolution is forthcoming.

## Light Client Support

Light clients, known as [SPV clients](https://bitcoin.org/bitcoin.pdf) in a Bitcoin context, only need to sync block headers and can be provided with Merkle proofs for their transactions or balances. In a Proof-of-Work system, this is trivial to do, as block header validity can be done by a single hash of the header and comparison to a known difficulty function.

In Proof-of-Stake, it’s not so simple. While we can certainly see that an aggregate signature contains a sufficient number of attestations, we don’t know if those attestations actually come from validators that actually have stake. The only way to know this is if we know the balance (*i.e.*, state) of every validator…which is what a full node does!

[Work on this](https://github.com/ethereum/eth2.0-specs/blob/274d73e70b3647758e0d39bec753a4f9d3ab6ea3/specs/light_client/sync_protocol.md) is in progress but still preliminary, and both beacon chain and shard chain light clients need to be designed (with shard chain light clients potentially being easier, as the committee size is substantially smaller). While it may be certainly be possible to “deploy” Eth 2.0 by requiring everyone to run full nodes, it would be a Pyrrhic deployment, as it would require all users to run beacon chain full nodes to have any degree of trust.

## Real-World Runtime and Other Costs

There are a number of real-world costs that need to be accounted for at the research level that are currently up to implementers to optimize.

As a thought experiment, it should be obvious that if a certain algorithm  used in the consensus protocol cannot be implemented in less-than-exponential asymptotic runtime, it would never be usable in practice, while being sound in theory, regardless of implementation optimizations. It is very important to ensure that all components of the system are implementable with reasonable runtime, memory, and other costs.

### Running a Beacon Node

Given that light clients in a PoS system are still the subject of active research, the only choice for validators is to run a beacon chain full node. [The cost of running a beacon node hasn’t been fully benchmarked at this time](https://github.com/ethereum/eth2.0-specs/issues/157), though given the communication costs for attestations may end up being non-trivial.

### Stateless Verification

While the stateless client model certainly removes the need to do state reads/writes in order to process transactions, it does have substantially higher 1) bandwidth and 2) processing requirements (as many cryptographic hashes must be performed in order to validate Merkle proofs). The costs of this are also unknown.

### Finding Slashable Attestations

In order to provide the guarantees it claims to have, Casper requires that validators actively seek out slashable attestations. The costs of doing this may be quite high, as in the worst case every attestation must be compared against every other attestation in the previous ~6 months. [Preliminary work on developing an optimized implementation](https://twitter.com/protolambda/status/1152289558001836034?s=09) certainly look exciting, but more research needs to be done in order to ensure this component of the consensus protocol does not cause nodes to choke up.

## Adversarial Model

The assumptions around the chosen adversarial model are quite strong in my opinion: a never-changing super-majority of validating stake is running default-configuration client software.

It does not consider adaptable corruption of validators (unlike other protocols such as [Algorand](https://arxiv.org/abs/1607.01341), though [unsuccessfully](https://arxiv.org/abs/1905.04463)) through [bribing](https://medium.com/nearprotocol/how-unrealistic-is-bribing-frequently-rotated-validators-d859adb464c8), potentially with [Dark DAOs](http://hackingdistributed.com/2018/07/02/on-chain-vote-buying/). As the committee size was chosen specifically [with this assumption in mind](https://medium.com/@chihchengliang/minimum-committee-size-explained-67047111fa20), if the assumption happens to not hold the performance of the system is unknown as it has not been analyzed. We ideally want to ensure that the chain degrades gracefully rather than catastrophically.

This is especially problematic given that an enormous amount of coins are held in centralized exchanges and in the future, DeFi contracts and layer-2 contracts. Should any of these be hacked (almost a certitude given enough time), the resulting stolen coins can be used to attack the system at virtually no cost.

## Privacy Considerations

Even though work has been done with respect to gas and account abstraction and EEs, Eth 2.0 [doesn’t have sufficient privacy guarantees](https://ethresear.ch/t/privacy-anonymity-on-ethereum-is-doomed/5430) in order to be conducive for everyday transactions. Even though one can implement various privacy-preserving smart contract environments described in academia in execution environments, this will just guarantee small anonymity sets (which may even be counter-productive).

Moreover, without some form of privacy at the network layer, validators can be vulnerable to a number of attacks, such as DDoS or bribing.

## Formal Proofs and Justifications

Last but not least, the entire system has not had any formal analysis of its properties and its correctness—and [without formal proofs, we have nothing](https://twitter.com/el33th4xor/status/1134430804245979136). Even more, proofs should be [mechanized in a proof assistant so as to make all assumption explicit](https://twitter.com/RosuGrigore/status/1134440278901891077). It’s quite common to realize that many things were missed when going through either implementation or formal proving.

## Replies

**vbuterin** (2019-07-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> Relayer System

This definitely is the thing I’m concerned most about at the moment! Though I’m happy that there’s work being [started on this](https://ethresear.ch/t/burn-relay-registry-decentralized-transaction-abstraction-on-layer-2/5820) in an eth1 context.

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> In Proof-of-Stake, [light clients are] not so simple. While we can certainly see that an aggregate signature contains a sufficient number of attestations, we don’t know if those attestations actually come from validators that actually have stake. The only way to know this is if we know the balance ( i.e. , state) of every validator…which is what a full node does!

I feel like light clients are solved! The general pattern (know a block header at time T, use it to download a committee at time T, use that to verify signatures from time T + k, those signatures point to a block header at time T+k) has been [known since 2015](https://blog.ethereum.org/2015/01/10/light-clients-proof-stake/) ; even the concept of using committees instead of the whole validator set was known then (see “the light client can even probabilistically check the signatures, picking out a random 80 signers and requesting signatures for them specifically…”). The protocol for doing this in eth2 concretely is basically ready; the only thing still being worked on is a simplification improvement made possible by the latest design of committing to compact committee roots.

The thing that I think *does* need more eyes is the market between light clients and light client servers, and making sure that can work efficiently, usably (including first-time-joiner experience) and minimizing centralization risk.

> Real-World Runtime and Other Costs

Benchmarking of the beacon chain is definitely being worked on, and I remember a result that clients can process a worst-case epoch transition within a single slot. I agree aggregation bandwidth is likely the biggest risk.

> While the stateless client model certainly removes the need to do state reads/writes in order to process transactions, it does have substantially higher 1) bandwidth and 2) processing requirements (as many cryptographic hashes must be performed in order to validate Merkle proofs). The costs of this are also unknown.

Definitely not unknown! An implementation of binary tree multi-proofs has been [made and benchmarked](https://github.com/ethereum/research/tree/master/merkle_tree); the general conclusion is that it validates the heuristic that the length of a Merkle proof of K nodes in a N-node tree is k + k * log(\frac{N}{k}) hashes.

> Finding Slashable Attestations

Agree! Though I’m not too worried about this because even a very inefficient and flawed implementation would likely be sufficient to ensure that slashed validators get caught. If violators *never* get caught, all that happens is that we’re back to an honest majority model.

> It does not consider adaptable corruption of validators (unlike other protocols such as Algorand, though unsuccessfully) through bribing, potentially with Dark DAOs.

We have a mechanism to provide a backstop in the case of a corrupted committee, namely [fraud proofs and data availability proofs](https://arxiv.org/abs/1809.09044). Here’s [a draft PR](https://github.com/ethereum/eth2.0-specs/pull/1083) for data availability proofs, which does need to be edited to take into account updates to the crosslink structure. Much of the discussion around crosslink data structure has been about preserving fraud proof friendliness.

Though the implementation-level work on making these things work has definitely not started yet!

> Privacy Considerations

I agree! I feel like we know the answers in theory (ZK ZK Rollup, ZEXE…) though in practice the implementers are jiust starting to get their tech off the ground, eg. see recent [work](https://twitter.com/rstormsf/status/1154148852993183745) [on](https://kndrck.co/posts/introducing_heiswap/) [mixers](https://twitter.com/econoar/status/1131298164496130048) and [auxilary infrastructure](https://ethresear.ch/t/burn-relay-registry-decentralized-transaction-abstraction-on-layer-2/5820).

> Formal Proofs and Justifications

Agree that we need more of this, and this is also something I’m disappointed we have not had more progress in!

---

**Mikerah** (2019-07-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I feel like we know the answers in theory (ZK ZK Rollup, ZEXE…)

We still don’t know the answers even with these constructions. Privacy needs to be at every level and a default. You can’t just tack on some academic construction and expect it to give sufficient privacy. Moreover, if mixers are still the highest level of privacy ETH2 can provide for users, then we’ve failed on a privacy front as it is well known by now that mixers are pretty terrible for privacy.

---

**vbuterin** (2019-07-26):

ZEXE is quite powerful stuff; it could give full privacy-preserving smart contracts. But I feel like the *meta-answer* that is important here is “we have execution environments, and those allow for competition and experimentation between privacy preserving layers, and hopefully frameworks with a very high degree of privacy preservation will become standard”. And we DO need people pushing hard and yelling at us (as [I have](https://ethereum-magicians.org/t/meta-we-should-value-privacy-more/2475)) to actually implement these things. Mixers are definitely NOT the end, just a pragmatic first step that delivers a lot of value.

---

**Mikerah** (2019-07-26):

I am aware that ZEXE is powerful and there’s a reference implementation in Rust that we can use and benchmark using Scout.

In order for privacy EEs to make sense, we need several things such as a minimal privacy layer for all EEs a la HTTPS for EEs, a network stack that is privacy-preserving and still maintains accountability, etc. Again, mixers make sense for current Ethereum due to its limitations and that’s fair. But, since we are quite early in ETH2.0, we can do much better.

---

**vbuterin** (2019-07-26):

I don’t think we can standardize privacy at base layer at this point. Different privacy schemes have different (hard!) tradeoffs, for example:

- Mixers only support coin transfers and have limited anonymity sets
- Anything SNARK-based adds a trusted setup requirement and is not QC-proof
- Anything STARK-based adds 50-100kb overhead
- Anything SNARK/STARK-based has high prover overhead
- Anything SNARK/STARK-based that supports general computation has insanely high prover overhead
- All of the SNARK/STARK-based schemes will keep seeing heavy and frequent upgrades over the next ~2 years
- Most of the existing systems don’t let you send money to accounts you don’t have encryption keys for
- Only MPC allows you to do something Uniswap-like with no owners and no one having an encryption key
- MPC requires an M-of-N trust assumption

But thing that we CAN AND SHOULD standardize ASAP include:

- Onion routing for transactions
- Onion routing for light client  server connections
- Ways for abstracted user accounts to specify encryption schemes and public keys
- Mixers, so we can at least allow users to have different accounts without them being trivially linked to each other

---

**Mikerah** (2019-07-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Onion routing for transactions
> Onion routing for light client ↔ server connections
> Ways for abstracted user accounts to specify encryption schemes and public keys

This is what I was mainly referring to. We could even use Dandelion++. The tradeoffs need to be looked at more.

As for the different tradeoffs of the various privacy schemes you mentioned, I don’t think those necessarily make sense as a minimal layer due to all the baggage ZKPs bring as you mentioned. But, even then, we can use some of these schemes for cross-shard comms as [@barrywhitehat](/u/barrywhitehat) proposed in his Scaling Ethereum talk. This can/would serve the basis for privacy-preserving cross-shard comms.


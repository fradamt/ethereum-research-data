---
source: ethresearch
topic_id: 9051
title: "Idea: a mini-VM that is executable by both the EVM and a SNARK circuit"
author: weijiekoh
date: "2021-03-30"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/idea-a-mini-vm-that-is-executable-by-both-the-evm-and-a-snark-circuit/9051
views: 2470
likes: 3
posts_count: 4
---

# Idea: a mini-VM that is executable by both the EVM and a SNARK circuit

A commonly cited tradeoff between optimistic and zk-rollups is security versus programmability. Today, optimistic rollups like Arbitrum and Optimism support far greater programmability as they support a very large subset of the EVM (though they have not launched to mainnet yet). Yet, optimistic rollups [may be vulnerable to game-theoretic attacks by L1 miners](https://ethresear.ch/t/nearly-zero-cost-attack-scenario-on-optimistic-rollup/6336). Moreover, optimistic rollups rely on fraud proofs, which [may also be vulnerable to censorship attacks by block validators](https://ethresear.ch/t/non-attributable-censorship-attack-on-fraud-proof-based-layer2-protocols/6492). On the other hand, zk-rollups are immune to such attacks, but are much more difficult to write so-called “smart contracts” in zero-knowledge circuits. Loopring, for instance, wrote custom AMM circuits, and Hermez currently only supports ETH and token transfers. ZkSync [reports](https://medium.com/matter-labs/zksync-2-0-roadmap-update-zkevm-testnet-in-may-mainnet-in-august-379c66995021) that they have made great strides in porting the EVM to a zk-rollup but I’m not sure if they have released any details yet.

One suggested means to resolve this tradeoff is [zk-MerkleWitnessAndSigRollup, a generic SNARK circuit for stateless contracts](https://ethresear.ch/t/zk-merklewitnessandsigrollup-a-generic-snark-circuit-for-stateless-contracts/7011):

> The difficulty of implementing complex snark circuits is thought to be a blocker for widespread adoption of zk-rollups until “generalized snarks” are practical (meaning one universal snark circuit that would, for instance, generate a proof of correct execution of any EVM code that’s passed as input). But if most of the throughput boost achieved by a zk-rollup is due to (i) and (ii) and not (iii), then it should be fairly straightforward for any dapp, even if it has contracts with a lot of complex logic, to adopt a generic zk-rollup circuit for state maintenance - call it the zk-MerkleWitnessAndSigRollup or the zk-PenultimateRollup - and get a big scalability gain today (or as soon as someone implements it ;).

It seems that the holy grail of generalised zk-rollups is EVM compatibility. Instead, I suggest a slightly different approach: a ZVM - that is - a VM whose opcodes can be executed by *both* the EVM and a zk-rollup. Rather than attempt the herculean task of porting the EVM to a snark circuit, one could simplify the job and get the best of both worlds.

I have not fully fleshed out the benefits and drawbacks of this approach, let alone implementation specifics, but I would just like to put it out here for discussion. I am particularly curious if this approach could make flexible L1-L2 interoperability possible. For instance, if the rollup could access ZVM state on L1, or vice versa.

Thank you!

## Replies

**kladkogex** (2021-04-02):

I am not sure how fast EVM will run if executed by a SNARK.  I have not seen any tests or benchmarks

---

**weijiekoh** (2021-04-03):

Exactly - hence it might be helpful to implement a simpler VM in a snark.

---

**spartucus** (2021-05-13):

I like this.

Although I have few questions: how does the `ZVM` execute contract? Is it a stateless VM? And if contract is deployed on the L2, could it be restored on L1?


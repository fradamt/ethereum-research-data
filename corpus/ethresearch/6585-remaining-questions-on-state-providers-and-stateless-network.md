---
source: ethresearch
topic_id: 6585
title: Remaining Questions on State Providers and Stateless Networks in Eth2
author: villanuevawill
date: "2019-12-05"
category: Sharded Execution
tags: [stateless, fee-market]
url: https://ethresear.ch/t/remaining-questions-on-state-providers-and-stateless-networks-in-eth2/6585
views: 4908
likes: 11
posts_count: 8
---

# Remaining Questions on State Providers and Stateless Networks in Eth2

# Prior Discussions

[State Providers, Relayers - Bring Back the Mempool](https://ethresear.ch/t/state-providers-relayers-bring-back-the-mempool/5647)

[@adlerjohn](/u/adlerjohn): [Relay Networks and Fee Markets in Eth 2.0](https://medium.com/@adlerjohn/relay-networks-and-fee-markets-in-eth-2-0-878e576f980b)

[@vbuterin](/u/vbuterin): [Eth2 shard chain simplification proposal](https://notes.ethereum.org/@vbuterin/HkiULaluS)

# Background

The latest [phase 0 & 1 proposal](https://notes.ethereum.org/@vbuterin/HkiULaluS) addresses a number of the concerns posted within the writeup, [State Providers, Relayers - Bring Back the Mempool](https://ethresear.ch/t/state-providers-relayers-bring-back-the-mempool/5647). In the new proposal, validators, EEs and block producers may transfer ETH between shards within a 1 block latency. This behavior is enshrined and gives a block producer the ability to deterministically run a transaction and confirm payment without having to trust the mechanics of an EE. For a more detailed description, read the “basic operating system” section in [the proposal](https://notes.ethereum.org/@vbuterin/HkiULaluS).

# Comparison to Eth 1.x Research

[The Eth1.x research](https://ethresear.ch/t/introductions-for-the-eth1-x-research-group/6430/23) group is actively working on transitioning eth1 into a stateless model. However, in the current transition, the miner (analogue to a block producer) holds the account state. In eth2, the block producers and validators **would not** be assumed to hold state. This difference introduces a number of questions around the stateless mechanics of eth2 that we do not have to think about currently within the effort around the eth1 stateless transition. Eventually, eth1 **will likely** transition to a model where the miners are not assumed to be stateful. This would need to occur before the [eth1 ->  eth2 switchover](https://ethresear.ch/t/the-eth1-eth2-transition/6265).

# Current Open Questions

- In eth1, transactions are of course propagated through a mempool. In eth2, alternate models could be explored since the block producer is predictable, although there are benefits to pursuing a mempool model from eth1. In a unicast model, the system is highly susceptible to DoS attacks. Is a mempool the right direction?
- Validators may likely keep some popular segments of the state tree and have basic cacheing capabilities on top of what is provided by cacheing through the EE layer, described here. There could be incentives or economic benefits to doing this depending on how state provider incentives operate. An analysis on this piece could be interesting.
- If a mempool is used, it will need to actively refresh its witnesses (stale transactions) as it prepares transactions for each block. This means EEs need to be deployed with a refresh script and we should benchmark this approach. Also, the mempool will need to refresh witnesses for multiple accumulators since it would support transactions for multiple EEs.
- Prior to preparing a block, the block producer will need to access a merge function from each EE it includes a transaction for. This merge function will give the instructions on merging the individual transaction proofs into a multiproof. We should also look at the mechanics of this script which would likely need to be deployed alongside a new EE.
- Should transactions from state providers (or the network) already be packaged in a multiproof? Would prepackaged multiproofs from state providers prevent block producers from taking standalone transactions due to additional complexities? Could this still skew towards some centralized behaviors as described in State Providers, Relayers - Bring Back the Mempool
- Do we foresee issues around bombs? As an example, how do we manage witnesses that go extremely deep and take a non-significant amount of execution time only to fail near the end as it is missing access to a particular region of state. We cannot charge the user in this case since it may not be malicious. If a contract dynamically accesses an account, then a prior transaction in the block may change the account it accesses. In this case, the transaction would no longer contain its needed witness. Distinguishing malicious behavior is quite difficult in cases such as this. This makes the mempool highly susceptible to a DoS attack.
- Miners are incentivized to choose transactions where the accounts are close to each other within the state tree (therefore decreasing the overall size of the multiproof). They are also likely incentivized to prioritize accounts which are frequently used. Do we see any issues or concerns with this?
- How do we price a user for their witness data when multiple transactions use the same witness in a multiproof. For example, if 3 transactions share the same witness, does the price get split in 3?

# Questions Around State Provider Incentives

- What is the best material currently on state provider or light client server incentives?
- Do we open a network of payment channels to provide micropayments to state providers or light client servers? @vbuterin originally brought up the state channel approach here
- If a developer is running local tooling such as ethers or web3.js, is it strange that the developer should be charged for test runs? How about estimating gas in a wallet?
- What is the viability of this payment network? Has anyone evaluated how this would look in practice? This would be a fairly large operation and we should be thinking about this soon.
- Since there is friction opening or switching between payment channels, will we skew towards a couple wallets/providers owning this due to network effects therefore solidifying services like infura as a centralized party?

# Conclusion

There remains a number of open questions around stateless networks in eth2 - in addition to what the eth1.x group is investigating. It would be valuable to get more involvement and more eyes/criticism on these pieces.

## Replies

**Mikerah** (2019-12-05):

One thing that comes to mind is how do beacon nodes fit into all of this, if they fit in at all?

---

**wemeetagain** (2019-12-05):

> What is the best material currently on state provider or light client server incentives?

Here’s an overview of Zsolt’s ([@zsfelfoldi](/u/zsfelfoldi)) LES server incentivization model, currently being built into geth:

https://github.com/zsfelfoldi/incentives/blob/7c58ad517a6f8cc038c2c01eadfe743c3980ae43/overview.md/

We discussed this work with him at the first ‘Light Client Task Force’ meeting a month or so ago, notes here:

https://medium.com/chainsafe-systems/light-client-task-force-call-1-1aaf559230fb

> If a developer is running local tooling such as ethers or web3.js, is it strange that the developer should be charged for test runs? How about estimating gas in a wallet?

In Zsolt’s model, clients can have zero or negative balances and just receive a lower QoS.

> What is the viability of this payment network? Has anyone evaluated how this would look in practice?

I think his work stops short of any specific payment network.

Curious if anyone’s heard of other research into light client server incentives.

---

**vbuterin** (2019-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> alternate models could be explored since the block producer is predictable,

This is not guaranteed to be true forever. We *are* exploring secret single leader election, and there have been some decent proposals from Dan Boneh in this regard. Though it is possible that such proposals would only apply to the hyper-important beacon chain blocks, and not to the shard chain blocks.

> Validators may likely keep some popular segments of the state tree and have basic cacheing capabilities

While proposal committees may do this, crosslink committees will not, because they reshuffle every epoch.

> If a mempool is used, it will need to actively refresh its witnesses (stale transactions) as it prepares transactions for each block.

It depends what we mean by a mempool! With EIP 1559, we can expect almost all transactions to be included within 1-3 slots. The mechanism I introduced where the state is 128 bytes allows the state to contain the last 4 roots, allowing transactions with witnesses to survive up to 3 slot transitions unmodified. So a “either it’s included within 4 slots or you / the state provider need to rebroadcast” model could be reasonable.

> Do we foresee issues around bombs?

I expect the witness would include a list of what it is a witness for, so the witness could be verified quickly and before doing any execution. There is the question of what happens if a transaction attempts an out-of-bounds access after doing execution. One way to resolve this could be to make the transaction fail (but still cost the sender gas) in this case. Transactors would want to work with state providers that do not cheat them, and block producers occasionally being dishonest could happen but would be “just a cost of doing business”.

> Miners are incentivized to choose transactions where the accounts are close … do we see any issues or concerns with this?

Figuring out how the gas market would work is probably the big challenge here.

> One thing that comes to mind is how do beacon nodes fit into all of this, if they fit in at all?

Aren’t basically all clients going to be beacon nodes? Maintaining the beacon chain state is a basic responsibility of anyone that wants to interact with the chain, unless they’re ok with being just a light client even for the beacon chain.

---

**Mikerah** (2019-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Aren’t basically all clients going to be beacon nodes?

Many clients have been designed in such a way that the validator logic and beacon node logic are separate and as such can be run separately. This leaves the option open for people to become validators running only validator nodes and these nodes connect to beacon nodes, that these users may or may not control themselves.

---

**villanuevawill** (2019-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I expect the witness would include a list of what it is a witness for, so the witness could be verified quickly and before doing any execution. There is the question of what happens if a transaction attempts an out-of-bounds access after doing execution. One way to resolve this could be to make the transaction fail (but still cost the sender gas) in this case. Transactors would want to work with state providers that do not cheat them, and block producers occasionally being dishonest could happen but would be “just a cost of doing business”.

How would you determine if it is malicious or not? A transaction *could* call into state dynamically. AKA some transaction before it now makes the call access a different part of state. This isn’t malicious and the user shouldn’t be charged.

---

**villanuevawill** (2019-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/wemeetagain/48/1433_2.png) wemeetagain:

> Curious if anyone’s heard of other research into light client server incentives.

Also [@vbuterin](/u/vbuterin) interested to hear your take. Do you think that these pieces could initially be altruistic and later transition into an incentive model, or an incentive model is required out of the gate?

---

**burdges** (2019-12-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> alternate models could be explored since the block producer is predictable,

This is not guaranteed to be true forever. We *are* exploring secret single leader election, and there have been some decent proposals from Dan Boneh in this regard. Though it is possible that such proposals would only apply to the hyper-important beacon chain blocks, and not to the shard chain blocks.

We evaluated the sortition landscape for polkadot, with some notes at https://research.web3.foundation/en/latest/polkadot/BABE/sortition/ but ultimately selected a design that sorts preannouncments created with a ring VRF.

I’ve done the main deign write up at https://github.com/w3f/research/tree/master/docs/papers/habe (name will change so url is unstable). We’ve plans to adapt the Markov chain analysis of chain growth to the sortition scheme, better integrate the VDF, and the usual tweaks from the implementation.

We’ve started two ring VRF implementations, one using SNARKs that’s only waiting for subversion resistance check and some grunt work, and one using “Bootleproofs” that requires more basic work.  Implementation should start once implementation for at least one of the ring VRFs finishes, but maybe sooner.

We envision another use besides the beacon/relay chain: Mimblewimble does not work because dandilon acts too much like a mempool and does not provide much mixing.  We shall bind temporary public keys into the ring VRF so that anyone can encrypt to upcoming block producers without identifying them.  We think replacing the memepool with messages encrypted to upcoming block producers and sending some blocks only to subequence block producers should give us mimblewimble-like shards/parachains that provide far better anonymity than existing mixer designs like mimblewimble.  This is discussed in the above write up.


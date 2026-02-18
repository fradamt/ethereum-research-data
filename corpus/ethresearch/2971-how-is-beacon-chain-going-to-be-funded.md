---
source: ethresearch
topic_id: 2971
title: How is beacon chain going to be funded?
author: kladkogex
date: "2018-08-17"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/how-is-beacon-chain-going-to-be-funded/2971
views: 3174
likes: 11
posts_count: 14
---

# How is beacon chain going to be funded?

I am struggling to understand how is the  beacon chain going to be funded.

All of validators, attesters etc need to be paid. This needs to be done in real ETH.

Are they going to be paid by printing money ? In this case a fork of the main net will be required.

Or the funding will be done through some fee mechanism on the beacon chain?

I do not think the question of funding is addressed anywhere.

## Replies

**danrobinson** (2018-08-17):

I believe the plan is to have a one-way peg from the legacy chain to the beacon chain, so you can burn ETH from the legacy chain and receive ETH on the beacon chain (but can’t go back).

Then on the beacon chain, validators are paid using newly issued ETH.

---

**kladkogex** (2018-08-20):

Dan - thank you -

The ETH that you burn on the legacy chain - who is going to print it  or provided ?  Are miners going to print this money? One will need to have a money-printing fork to do it.

Why would miners on the legacy chain want to fund the system the entire purpose of which is to turn multi-billion investments in ASICS into “legacy” ? ![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=9)

---

**danrobinson** (2018-08-20):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The ETH that you burn on the legacy chain - who is going to print it or provided ? Are miners going to print this money? One will need to have a money-printing fork to do it.

I’m talking about ETH that you already own. You burn it because you don’t want legacy ETH anymore, you want beacon-chain ETH (because that’s what you can use for staking, and eventually can move to or from the shards, and use in the new contracts). Basically, you have to die to get to heaven.

Not sure what you mean about the need for printing new ETH. In fact I believe the current plan is for there to be a simultaneous fork that REDUCES the mining reward on the legacy chain (because from that point on, its security will mostly be derived from its hashes being checkpointed on the PoS beacon chain, so you don’t need to pay miners as much).

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Why would miners on the legacy chain want to fund the system the entire purpose of which is to turn multi-billion investments in ASICS into “legacy” ?

I suspect some of them will not, but their permission is not required.

---

**kladkogex** (2018-08-21):

I see - sorry I did not understand initially,

So I am burning real ETH, getting Beacon-ETH and I am using this Beacon-ETH to pay gas fees on the shards, correct? And these fees create a source of revenue that supports the beacon chain and shards, correct?

By how much do you want to reduce the mining reward ?))) Definitely miners will dissent this fork, so its almost guaranteed that there will be another “ETH Classic”.

Out of $25B of the current ETH valuation how much do you think will stay in “ETH Classic” and how much will be in the new fork ? Seems to be quite risky …

---

**timjp87** (2018-08-21):

I wonder what will happen to the legacy PoW chain in the long run. From my understanding you deposit 32 ETH into a contract on the PoW Chain. Now we also have a PoS Beacon Chain only for attestations and Shard PoS Chains where accounts etc live.

Will the contract that people deposit 32 ETH to migrate to Shard #1 at some point? Or will the PoW chain run forever?

---

**ldct** (2018-08-21):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Definitely miners will dissent this fork, so its almost guaranteed that there will be another “ETH Classic”.

I personally think the probability of someone seriously trying to this is less than 50% and the chance of them succeeding (i.e. that there is a long-lived “third fork” containing the dao refund contract but not the beacon chain one-way-burn contract, or where the contract is censored some other way) is less than 10%. Reasons for why I think so:

1. PoW fans can use the existing ETC chain
2. Ethereum’s plan to transition to PoS was known since before mainnet launch
3. The third fork will probably not be sharded (I don’t know many researchers thinking about sharding-on-PoW)

---

**paulhauner** (2018-08-25):

I don’t have a solid answer to this but I can postulate, FWIW.

For the Beacon Chain, I see two “funding” challenges:

1. Source of the ETH which validators use to stake.
2. Source of the ETH that is given to validators as rewards.

For (1), I think the EF has been pretty clear that it’s going to come from a “one-way peg”. You lock/burn your PoW-chain ETH by transferring it to some contract and then it magically appears on the Beacon Chain (w/ decentralized crypto proofs, etc.). The [v2.1 spec](https://notes.ethereum.org/SCIg8AH5SA-O4C1G1LYZHQ?view) has some info on this.

It’s worth noting that the early days of Beacon Chain will see a one-way peg where validators can’t withdraw back to the PoW-chain — once they deposit they’re stuck until the one-way peg is upgraded into a two-way peg. AFAIK, this is just during the initial phases of the Beacon Chain and is primarily to reduce the external impacts of reverting the Beacon Chain if there is some protocol-level error. Reverts on the Beacon Chain get a whole lot messier if some of the validators have already got their ETH out and sold it. This information is from an earlier conversation with Danny Ryan – I don’t have a written reference.

~~Regarding (2), I haven’t heard anything about it yet. I know that for [EIP-1011](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1011.md) (hybrid PoW/PoS via a Casper FFG contract) the plan was to fund the FFG contract with 1.25m newly-minted ETH and then revisit the issue once the balance starts getting low (~2 years).~~

~~Personally, I’m not sure what’s going to happen. If I had to guess I’d say they’d follow the lead from EIP-1011.~~

Chi Cheng Liang says in the ethereum/casper gitter (first referring to the EIP-1011 issuance method, then describing the beacon chain issuance method):

> The CASPER_BALANCE approach is convenient for the contract version because it is easier in evm to issue the voting reward with pre-stored ETH. In the beacon chain, the issuance of reward can be just implemented like how the mining reward is issued currently.

---

**kladkogex** (2018-08-25):

The one-way peg is bad in my opinion - whats the point of designing a half-baked solution like that? It can kill the entire thing. People will not put money into something if there there is no way to pull money out.

Is there any example of any financial solution in the history of the universe where you deposit but cant withdraw?  ![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=9)![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=9)![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=9)

Why do not we do a two-way peg ? ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)  A super-complex system is build, which is going to be immensely harder to debug and it does not allow a two-way peg!

---

**paulhauner** (2018-08-25):

> whats the point of designing a half-baked solution like that?

The one-way peg is only intended for very early stages of the Beacon Chain. I would argue that the system is “designed” with a two-way peg, but it’s simply not enabled.

> People will not put money into something if there there is no way to pull money out.

I think this is the point. You only put money in there if you’re willing to participate in a “beta” system.

I would probably try not to think of this as a design choice, instead more of an gradual implementation strategy.

---

**eolszewski** (2018-08-25):

Personally, I don’t see the point in the Beacon Chain as this bolt-on component to the sharding protocol…

It’s an interesting thought that DFINITY put out there, but we could just as well fold in the value that it is providing into the protocol, itself. At present, I feel like it adds undue complexity.

---

**djrtwo** (2018-08-25):

How do we fund miner rewards? With rules baked into the protocol.

How do we fund validator rewards? With rules baked into the protocol.

With EIP 1011, these rules were going to exist in a smart contract in the current EVM chain. At the EIP 1011 fork, a bunch of ETH was going to be placed into the casper contract in an irregular state change to fund validator payouts. Validators would then send deposits to this contract to be inducted into a protocol level set of validators that had special privileges around consensus. After participation and either making or losing ETH, a validator could then issue a logout, and leave the validator set with their balance to head back to the existing EVM chain.

With the beacon chain, these rules are going to exist in a special side chain called the beacon chain. At some fork block, validators will be able to send ETH to a contract on the existing EVM chain to then be inducted into a protocol level set of validators that have special privileges around consensus. They will be responsible for FFG finalization (similar to what would have been the function of the casper contract) as well as building and finalizing the shard chains (what would have been the job of the sharding manager contract in previous roadmaps). After participation and either making or losing ETH, a validator could then issue a logout, and leave the validator set with their balance to head back to the shard chains (not the existing EVM chain).

At first this is a directional relationship out of the EVM chain and into the sharding side of the protocol. Eventually, when we are happy with the new sharding side of things, we can loop the existing EVM chain back into the new PoS structure. There are two main methods being discussed. (1) bring the EVM chain in as a shard to be managed, built, and finalized by the validators, or (2) port the full EVM chain into a shard as a contract. I currently prefer (2).

You start with two primarily independent mechanisms as the new sharding mechanism gets built up. This *loose coupling* of the current stable part of the protocol with the new likely rapidly changing/growing sharding part of the protocol will allow for rapid development of the sharding side of things without having to meddle too much with the stable EVM. Only when sharding gets to a stable place, will we work on more tightly coupling the old and new universe.

In terms of the new sharding side of things, the protocol will be rolled out in phases. The 1st phase might not have an initial option for validators to withdraw (because the shard chains themselves might not yet exist to withdraw to!). In this initial phase, I would expect a smaller set of ETH to participate. Because the validator payout per eth deposited scales inversely with the total size of the validator set, these early adopters will be paid a premium for early participation. When the protocol matures, risk has been more certainly established, and validator withdraws are active, I expect a larger set of ETH to participate and for the per-ETH reward to be much lower. There’s a risk, time horizon, and payout profile on early participation. Validators will personally have to assess and make a judgement call on participation.

---

**YunJungHwan** (2018-08-25):

If there are two chains, how is inflation managed? In the legacy chain, inflation will be paid to miner and in the beacon chain inflation will be paid to the validator. If legacy chain is hard-forked and continue, inflation is doubled. Is it possible to distinguish transfer that is by inflation after hard-fork? I guess it is maybe possible in UTXO model, but I think it is impossible in state model.

---

**djrtwo** (2018-08-25):

I’m not sure I understand your question.

“inflation is managed” via two schemes in the short term – a legacy PoW mechanism and a new PoS mechanism. These two mechanisms have different distribution functions particular to each protocol. It is simple to model both protocols and assess inflation of the two combined. It is important to note that PoS schemes need much less inflation than the current PoW scheme.

Let me know if I missed your intention in the question.


---
source: ethresearch
topic_id: 6666
title: Alternative proposal for early eth1 <-> eth2 merge
author: vbuterin
date: "2019-12-23"
category: The Merge
tags: []
url: https://ethresear.ch/t/alternative-proposal-for-early-eth1-eth2-merge/6666
views: 30482
likes: 36
posts_count: 30
---

# Alternative proposal for early eth1 <-> eth2 merge

This is an alternative proposal for eth1 <-> eth2 merging that achieves the goal of getting rid of the PoW chain and moving everything onto the beacon chain on an accelerated schedule. Specifically, it requires stateless clients, but NOT stateless miners and NOT webassembly, and so requires much less rearchitecting to accomplish.

### Prerequisites

- Stateless client software (a “pure function” for verifying blocks+witnesses, along with a method for generating witnesses for a block) available with multiple implementations
- Eth1-side protocol changes to bound witness sizes to ~1-2 MB

### New beacon chain features

- The state of shard 0 houses the state root of the eth1 system.
- We add a new list of validator indices, eth1_friendly_validators. Any validator has the right to register themselves as eth1-friendly (and deregister) at any time.
- The proposer on shard 0 at any given slot is chosen randomly out of the eth1-friendly validators.
- The shard 0 committee verifies the shard 0 blocks, which are expressed in a format that contains both the block body as it currently exists, plus the stateless client witness. All other shard committees verify their own shard blocks, but they would only be verifying data availability, not state execution, as shard 0 is the only shard that would be running computation.

### Operation

The eth1 system would “live” as shard 0 of eth2 (eventually, we can adjust it to be one of the execution environments, but at the beginning it can be the entire shard). Validators that want to participate in the eth1 system can register themselves as eth1-friendly validators, and would be expected to maintain an eth1 full node in addition to their beacon node. The eth1 full node would download all blocks on shard 0 and maintain an updated full eth1 state.

### Transition

The transition would still be done using a procedure similar to [The eth1 -> eth2 transition](https://ethresear.ch/t/the-eth1-eth2-transition/6265).

## Replies

**djrtwo** (2019-12-23):

Not opposed. I, and a number of others, have been tossing similar ideas around recently. Especially in light of the complexities of a generally extensible and feature rich Phase 2 being pretty massive.

Bringing eth1 natively into eth2 soon ![:tm:](https://ethresear.ch/images/emoji/facebook_messenger/tm.png?v=14) will allow for a more native use of the eth2 data layer for massive layer-2 (1.5?) scalability in the meantime without the induced delays and complexities that emerge in a finality-gadget + bridge mechanism. This would also be a natural place for introducing validator liquidity without an emergent second asset.

In this path, eth1 could still become a single-shard EE if/when EE functionality is built and deployed.  As long as we do some due diligence on the structure/framing, we can still evolve toward the promise of a general and extensible Phase 2.

---

**djrtwo** (2019-12-23):

What does a fee-paying mechanism look like in this model to put data in the other shards? I suppose we could use the data-root bounty mechanism previously discussed. Need to think it through some more

---

**villanuevawill** (2019-12-23):

I like this direction a lot and have generally thought moving in the direction of eth1 as a pseudoshard of eth2 makes a lot of sense. Do you think there would be concerns about the `eth1_friendly_validators` system decreasing the current security of eth1? In general though, I Iike any approach that transitions eth1 into eth2 and lets it actively use the eth2 world.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> What does a fee-paying mechanism look like in this model to put data in the other shards? I suppose we could use the data-root bounty mechanism previously discussed. Need to think it through some more

My general thought is following Casey’s line of thinking, phase one and done. Adding basic execution into the shards should not be a heavy lift and we can establish a fee market EE/transfers EE. This could be used as the basis for operating the shards as a data availability layer while we work on innovating, securing, building and preparing more sophisticated contract/execution EEs.

---

**vbuterin** (2019-12-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> What does a fee-paying mechanism look like in this model to put data in the other shards? I suppose we could use the data-root bounty mechanism previously discussed. Need to think it through some more

Once we have eth1 inside of eth2 proper, then there’s no cost in allowing two-way convertibility of ETH ↔ BETH. At that point, we could just add a simple fee-payment system where fee-payers sign BLS signatures of `[data_root, shard, slot, fee]`, and then the block proposal object includes the `fee` and the signer validator ID and the signatures of the fee-payers get aggregated into the signatures of the headers themselves.

---

**vbuterin** (2019-12-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> Do you think there would be concerns about the eth1_friendly_validators system decreasing the current security of eth1?

*Proposing* eth1-on-eth2 blocks would be voluntary, but *verifying* them as part of a committee would be mandatory; this is why we still need stateless clients. So even if only 5% of validators sign up as eth1-friendly, and out of those 4% are malicious, then the malicious blocks would not get through; the only bad thing that would happen is that on average a transaction would take 5 slots to get in instead of 1.

---

**villanuevawill** (2019-12-23):

Ah thanks for this - I had misunderstood and thought that verification also only came from `eth1_friendly_validators`. ![:100:](https://ethresear.ch/images/emoji/facebook_messenger/100.png?v=14) awesome.

---

**terence** (2019-12-23):

What else would a eth2 node have to do besides maintaining a stable connection with eth1 node?

> Any validator has the right to register themselves as eth1-friendly (and deregister) at any time

Would this be new beacon operations?

---

**vbuterin** (2019-12-23):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> What else would a eth2 node have to do besides maintaining a stable connection with eth1 node?

An eth2 node that has signed up as being eth1-friendly would have to maintain an eth1 node (modified from status quo to read blocks from the shard chain instead of from the PoW chain). Other eth2 nodes would need to do nothing new, except to calculate shard 0 state roots they would need to call into a library that would include the eth1 state transition function in stateless form.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> Would this be new beacon operations?

Yes.

---

**lightuponlight** (2019-12-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Eth1-side protocol changes to bound witness sizes to ~1-2 MB

What are the implications of this on existing contracts like Dai, etc?

---

**vbuterin** (2019-12-24):

Basically, to make witnesses viable we would need gas cost changes the look something like the following:

- SLOAD goes up to 1000-2000
- Any opcodes that access other contracts go up to 1000-3000
- Calling a contract (and hence running its code) further costs an additional 1-2 gas per byte of code

This would actually be not that punitive to average applications, though many apps would need to rearchitect themselves to use fewer full-sized contracts. There would be some exceptional applications that become considerably less viable. A simple ERC20 transaction (including DAI) would maybe become at most ~5-10% more expensive.

---

**lightuponlight** (2019-12-24):

I should have been clearer what exactly I was asking.

For many contracts the repricing you mentioned won’t be a significant issue, but the size limitations may well be. Do you know if it will break the Dai contracts? Redeployment of Dai is an enormous undertaking.

There may be some other such contracts where a redesign and redeployment will have systemic impacts like that too.

---

**sams** (2019-12-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Prerequisites - Stateless client software

From an eth1 perspective, does this proposal not already reduce the requirements to create blocks from eth1 node+ eth1 mining rigs down to just running a eth1_friendly_validator node without needing the miners?

While stateless clients will remove the node requirement, this hybrid removes the biggest burden to creating blocks in eth1, which is the mining: many more people can do stateless than can hold state, but many, many more people can hold state than can mine, and the merge moves a long way down the desired path.

It may also simplify transition significantly as it starts from existing nodes and welcomes in new ones (ie people who can hold state but not mine).

---

**vbuterin** (2019-12-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/lightuponlight/48/4337_2.png) lightuponlight:

> For many contracts the repricing you mentioned won’t be a significant issue, but the size limitations may well be.

Ah, the size limitations would be implemented through the repricings. No single contract is larger than 24 kB, and there’s no single system of contracts that gets called in a single transaction that’s more than a few times that AFAIK.

But even there we could mitigate the impact by having a  “frequently used contracts” registry on eth1, which would have a few dozen megabytes of code that get accessed really frequently and would be expensive to join but could be accessed cheaply. This registry could then be moved to eth2.

---

**lightuponlight** (2019-12-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> But even there we could mitigate the impact by having a “frequently used contracts” registry on eth1, which would have a few dozen megabytes of code that get accessed really frequently and would be expensive to join but could be accessed cheaply. This registry could then be moved to eth2.

So, Maker could move its contracts into that cache through some kind of process during the migration, grandfathering them in if the size were too large?

What would be the process of having contracts added to the cache, and for having them removed?

---

**DaniellMesquita** (2019-12-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A simple ERC20 transaction (including DAI) would maybe become at most ~5-10% more expensive.

Using GST2 (GasToken) would be the recommendation for contracts?

Is gasless dai (https://gdai.io) ready for this update?

---

**mrdoom4334** (2019-12-26):

I totally agree with this proposal … saves ton of time and effort

---

**dankrad** (2019-12-26):

Very likely the best thing we can do:

- Probably accelerates having a solid eth1/eth2 connection by about 2 years
- Brings the benefits of PoS to Eth1 immediately
- Actually makes the phase 1 data availability engine usable
- Solves the Eth2 -> Eth1 bridge conundrum

The cost is that the Eth1 legacy is likely to be carried into Eth1 for the foreseeable future. But I think that’s a price worth paying, and it’s paid off in the past in technology transitions to keep compatibility to the main industry standard (which is currently Eth1 for smart contracts). That’s why x86-64 was successful and IA64 was not.

I see the biggest danger in doing this without solving the state rent problem. This means there might be state arbitrage between the Eth1 and Eth2 subsystems.

---

**jgm** (2019-12-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> I see the biggest danger in doing this without solving the state rent problem. This means there might be state arbitrage between the Eth1 and Eth2 subsystems.

I’d be inclined here to not solve the state rent problem, but instead provide a ramp up for transaction costs.  Why?

- state rent on Ethereum 1 is hard.  Any attempt to add state rent must consider many assumptions made in the contracts already deployed, and either incorporate them into the model or ignore them and suffer the consequences
- state rent on Ethereum 1 is not part of the deal.  State was paid for according to the model laid down at the time the contracts were created.  Forcing a change will result in any number of situations where users can legitimately complain that changing the rules after the fact has caused their contract/app/business pain, and will reduce their desire to either migrate or rearchitect their contracts on Ethereum due to concerns this is just the first of a number of such changes
- the whole point of a transition is for it to be smooth.  If it isn’t smooth it may as well not bother happening at all; forced active migration is the worst of all worlds

So how to merge without causing unnecessary hardship?  I’d go for a staged approach:

1. merge without changing any of the established rules on the Ethereum 1 chain
2. alter gas costs as required to fit the reality of the costs involved
3. build the phase 2 EE(s) that will be home for new contracts (this would be a number of completely new EEs that would not necessarily follow Ethereum 1 semantics but would between them have all the functionality that Ethereum 1 smart contracts may need).  These could co-exist on shard 0 with the Ethereum 1 chain or live on other shards; the only reason it may matter is if the EEs are allowed to access Ethereum 1 state directly
4. after a certain amount of time make new contract creation on Ethereum 1 a very expensive operation (would have to consider how pre-existing contracts creating contracts are handled here)
5. after a certain amount of time to allow for migrations, start to increase the base transaction fee for Ethereum 1 transactions over a long period of time (e.g. doubling every year)

The reason I’d go for something like this is that it gives the users and developers a clear upgrade path that provides them with benefits at each step of the way:

- after the merge users have higher transaction throughput (which should also translate to lower transaction costs)
- after the new EEs are in place developers have a higher throughput alternative to the Ethereum 1 chain for their smart contracts
- once the Ethereum 1 chain becomes functionally obsolete users and developers can migrate to the EEs, resulting in cheaper transactions and avoiding the additional costs of the Ethereum 1 transaction ramp-up

The downside of this is that there is likely to be some sort of “final state” once all this has been done, holding contracts and (effectively) read-only data.  Perhaps at this point we can start to think about how to manage the Ethereum 1 state, but anything before I’d worry would be premature.

---

**vbuterin** (2019-12-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> The cost is that the Eth1 legacy is likely to be carried into Eth1 for the foreseeable future

How so? We can eventually hard-fork in a compilation of everything to WASM, and put it under the same EE system as everything else.

And as for the eth1 state, storing that state would be a voluntary thing, and so if it becomes unsustainable what would happen is that the UX of that EE would get worse over time until we are basically forced into one of two solutions:

1. People migrate onto a better EE
2. We add access lists, and block producers are generally only willing to deal with transactions that come with access lists and transaction-sender-provided witnesses

I do think we should start exploring details on both of those options ASAP.

---

**dankrad** (2019-12-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> How so? We can eventually hard-fork in a compilation of everything to WASM, and put it under the same EE system as everything else.

Of course that possibility exists, however I think it may well become much less likely once this infrastructure exists.

But yes it would not be technically any more difficult that it is now.

Another thought here: Can’t we leave the storing of Eth1 state entirely to relayers (which might be specialized Eth1 relayers)? Then we would not have to distinguish between Eth1 capable/non-capable validators, as all of them should be able to process Eth1 blocks once witnesses are added.

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> state rent on Ethereum 1 is hard . Any attempt to add state rent must consider many assumptions made in the contracts already deployed, and either incorporate them into the model or ignore them and suffer the consequences

I’d probably have to agree here. The ideal outcome would be if we can support Eth1 as is at roughly current gas costs, and the new Eth2 ecosystem will just be way cheaper (due to sharding and PoS) even when factoring state rent in.


*(9 more replies not shown)*

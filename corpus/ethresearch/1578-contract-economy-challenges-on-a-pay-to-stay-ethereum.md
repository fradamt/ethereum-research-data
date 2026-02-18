---
source: ethresearch
topic_id: 1578
title: Contract economy challenges on a pay-to-stay Ethereum
author: daniel-jozsef
date: "2018-03-31"
category: Sharding
tags: []
url: https://ethresear.ch/t/contract-economy-challenges-on-a-pay-to-stay-ethereum/1578
views: 2757
likes: 15
posts_count: 14
---

# Contract economy challenges on a pay-to-stay Ethereum

I believe this is extremely important, as the proposed pay-to-stay scheme may disincentivize many current use cases of Ethereum, and instead relegate it to being a ledger for traditional businesses to run their traditional centralized apps on. Note, I do support this latter use case, but not exclusively, and my fear is that pay-to-stay would make all other uses extremely hard to implement.

Since I feel like I’m polluting the [pay-to-stay pricing thread](https://ethresear.ch/t/a-simple-and-principled-way-to-compute-rent-fees/1455/56) with this, I’m creating this topic for this discussion specifically.

---

As [@vbuterin](/u/vbuterin) pointed out in that thread, community-owned registry contracts built on address -> {something} mappings (nb. the most common design pattern on today’s Ethereum!) will be phased out in favor of single-owner, single-point-of-interest contracts.

This is an entirely new way of designing tokens and non-fungible assets, and I think deserves a thread to discuss ideas. A post pay-to-stay Ethereum would look a lot more like Bitcoin in my opinion, with UTXO-like contract structures, validated through provenance.

However, there are some use cases when mappings and shared-ownership registries still cannot be done away with… Like ENS, for example, users need a central address to use for querying based on name.

These contracts need to collect tax from registrants to pay for rent, otherwise new registrants will have to subsidize previous registrants, and as the state size grows, the cost of new registrations will grow proportionately (eventually becoming unfair or even untenable). However, to force old registrants to keep paying tax, their part of the state needs to be ejectable - for this records about tax payments needs to be kept, and non-payers need to be identifiable in O(log(n)) time - something I’m not sure is even possible in the EVM.

## Replies

**MicahZoltu** (2018-03-31):

I do not think that any contracts should get a free ride “just because it is useful”.  If it is truly useful, people will be willing to pay to use it.  All contracts should define a mechanism to be self sustainable.  In the case of ENS, this likely means charging rent for ENS entry holders to cover the costs of Ethereum rent.  For some contracts this may mean voluntary donations and yet others this will come in the form of some novel form of revenue generation.

---

**RoboTeddy** (2018-03-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel-jozsef/48/1067_2.png) daniel-jozsef:

> However, to force old registrants to keep paying tax, their part of the state needs to be ejectable - for this records about tax payments needs to be kept, and non-payers need to be identifiable in O(log(n)) time - something I’m not sure is even possible in the EVM.

Unless I’m missing something, there are various ways to identify non-payers in less than O(log(n)) time, e.g.:

Maintain a map from blockNum to the set of registrations that should be evicted at that blockNum

Maintain a map from registration to the blockNum at which that registration should be evicted

Use the first map to evict registrations. Cost is O(number of blocks since last eviction sweep).

If a registrant makes a rental payment, use the second map to aid in efficiently updating the first. Cost is O(1).

Alternatively: use a min-heap of registrations, where the value associated with each registration is the block at which an account comes due. Evictions and rental payment processing would each be O(log(n)).

---

**danrobinson** (2018-03-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel-jozsef/48/1067_2.png) daniel-jozsef:

> However, there are some use cases when mappings and shared-ownership registries still cannot be done away with… Like ENS, for example, users need a central address to use for querying based on name.

I don’t think this is true. `CREATE2` (from [EIP 86](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-86.md)), which will allow a new way of creating a contract using a user-provided salt rather than an incrementing nonce, should make it possible to set up a registry where the registry contract maintains no state. The registry contract would just create a new single-domain-management contract using `sha3(domainName)` as the salt. Then anyone could compute the address for the single-domain-management contract for any given domain name, without even needing to consult the registry contract (whose main responsibility is to create the single-domain-management contracts).

Also responding to something from the other thread:

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel-jozsef/48/1067_2.png)[A simple and principled way to compute rent fees](https://ethresear.ch/t/a-simple-and-principled-way-to-compute-rent-fees/1455/53)

> @danrobinson if I’m correct you’d need to try all past nonces of the address and hash them each to get all possible child contract addresses, until you find the address, or run out of nonces. Especially with a highly active parent contract, this sounds pretty expensive for an everyday (or, more, “every millisecond”) operation. Changing the contract address calculation scheme to be bidirectional, or adding parent address as a system field would probably help.

I don’t think this is true either. You never have to grind to find a nonce; whoever is trying to prove the provenance of the contract would provide it to you. (Or if you insist, the contract could even keep track of the nonce of its parent at the time it was created, so the child contract’s state contains all the information necessary to validate its provenance.) `CREATE2` adds additional possibilities here (every Cryptokitty could have a unique name, and `sha3(name)` could be the salt when its contract is created; this would let you look up any Cryptokitty contract on the blockchain, by name, even without a hint from the owner).

---

**daniel-jozsef** (2018-04-01):

Yea, CREATE2 definitely sounds like it will solve this issue. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) I’m starting to think this will actually result in better desinged contracts. I’m planning on doing a writeup / design brainstorm about this on Medium.

As for providing the nonce as a proof, yea that’s such a simple and self-evident solution it occurred to me after writing that post.

---

**tawarien** (2018-04-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel-jozsef/48/1067_2.png) daniel-jozsef:

> Yea, CREATE2 definitely sounds like it will solve this issue.  I’m starting to think this will actually result in better desinged contracts. I’m planning on doing a writeup / design brainstorm about this on Medium.

I remembered that I read somewhere (Either as EIP, Issue in the EIP repo or here) a discussion on an create opcode that copies its code from an existing contract such as not each contract with the same code has to pay the code storage cost. Sadly when searching, I could not find it anywhere (does someone know where this was?).

Such a create code combined with CREATE2 may be another piece of the puzzle for making this style of contract work smoothly.

---

**danrobinson** (2018-04-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel-jozsef/48/1067_2.png) daniel-jozsef:

> Yea, CREATE2 definitely sounds like it will solve this issue.  I’m starting to think this will actually result in better desinged contracts. I’m planning on doing a writeup / design brainstorm about this on Medium.

Cool, yeah I agree! You could even imagine eliminating mappings as a concept from contract storage. Each contract could just have a single linear array of storage. To store some value under a key, you would create a new contract using that key as the salt, and initializing it with standard code that exposes a getter and setter to its creator. (Hopefully the overhead from all that boxing could be optimized away by the implementation, although maybe the gas overhead would make it a non-starter, I’m not sure).

---

**daniel-jozsef** (2018-04-03):

I’d rather not do away with mappings. They certainly have their time and place.

It’s just the pattern of recording ownership as an address mapping in a registry contract that needs to go. There are a dozen other, legitimate uses for mappings.

Also, when we’re talking about sharing code between contracts, let’s not forget [“I accidentally killed it”](https://cryptoshirt.io/products/devops199-quote-i-accidentally-killed-it-tee)…

BTW, what exactly is the roadmap for CREATE2?

---

**SylTi** (2018-04-04):

Let’s not forget about the hundreds/thousands of contracts that are already deployed and don’t have an easy migration path. Either they need to be grandfathered with the previous conditions or there is a big chance this kind of change end up in the split of the network.

Let’s not forget either about all the applications that will break, because now, some contracts functions that were free to call to read data can end up needing the contract to be resurrected first.

---

**fubuloubu** (2018-04-05):

Mappings are a very useful data structure for a distributed database because they allow unordered commits to the database in an easy manner. Using arrays often is a poor choice because you have to keep track of the index to commit or delete, and if you start clearing and merging array entries that part becomes very cumbersome very quickly.

Ethereum is basically built on these central registry type contracts (ERC20 is a good example), and that’s because they work pretty well for what they do. What deficiencies do these have that require a change technically? And not just in support of a rent-taking scheme.

---

**daniel-jozsef** (2018-07-10):

Getting back to this topic after quite a while, sorry… ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

[@SylTi](/u/sylti)

> Either they need to be grandfathered with the previous conditions or there is a big chance this kind of change end up in the split of the network.

Yes that is an issue. Grandfathering these contracts to be rent-free *might* be viable, but then we’ll need to make an exception for Gastoken specifically, which needs to die. (The whole rent proposal was mainly triggered by Gastoken, and the abuse of the refund mechanism it represents.)

…or, we need to figure out good solutions for creating “derivatives” of value in these contracts, that will work without the contracts themselves in state. This might need extensions to the EVM.

[@fubuloubu](/u/fubuloubu)

> Ethereum is basically built on these central registry type contracts (ERC20 is a good example)

The *current* Ethereum ecosystem is. Ethereum isn’t. ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

> What deficiencies do these have that require a change technically? And not just in support of a rent-taking scheme.

They have deficiencies with relation to a rent-taking scheme. Here’s the whole issue:

1. Ethereum is facing an explosion of State size.
2. To rein in State, Ethereum may need to move to rent-based operation in the indefinite future.
3. On a rent-based Ethereum, central registry contracts are unviable (for reasons laid out above).
4. Based on the three points above, central registry contracts are unsustainable in general (the depend on a very limited resource - state size - that is unsustainably subsidized at the moment, making the problem invisible at superficial glance).

---

**fubuloubu** (2018-07-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/daniel-jozsef/48/1067_2.png) daniel-jozsef:

> Based on the three points above, central registry contracts are unsustainable in general (the depend on a very limited resource - state size - that is unsustainably subsidized at the moment, making the problem invisible at superficial glance).

Rent is one solution to this problem. Please do not assume it is the **only** solution, or even the best one possible. Disabling a whole class of implementations (especially one so heavily relied on for infrastructure) I think is a serious defect with that solution, and I think that other ideas should be investigated first before concluding this is the best way to solve the problem of abuse of this commons resource that this “state explosion” represents.

Tokens are still good examples. Imagine Plasma is widely used, well there’s not really a state problem with ERC20 because all tokens are then locked into the Plasma contract address most of the time. **That contract** is now the one with the state problem!

---

**jvluso** (2018-07-10):

> Let’s not forget about the hundreds/thousands of contracts that are already deployed and don’t have an easy migration path. Either they need to be grandfathered with the previous conditions or there is a big chance this kind of change end up in the split of the network.
> Let’s not forget either about all the applications that will break, because now, some contracts functions that were free to call to read data can end up needing the contract to be resurrected first.

Depending on how sharding is implemented, it might be possible to have different shards use different opcode sets. If that is possible, all current contracts can remain on an unlimited capacity shard, while some other shards can use the pay to stay model. If that is not possible, this may only be usable in side chains.

---

**DennisPeterson** (2018-07-12):

Regarding code sharing and “I accidentally killed it,” reference counting might be an answer. A contract with new code would store the code in an on-chain repo with a reference count of one; the contract itself would be state and a pointer to the repo. Any contract copied from it would get the same pointer, and increment the repo’s count. Any destroyed contract would decrement the count. If the count goes to zero the code is destroyed.


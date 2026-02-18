---
source: ethresearch
topic_id: 4378
title: Ethereum State rent for Eth 1.x pre-EIP document
author: AlexeyAkhunov
date: "2018-11-26"
category: Economics
tags: [storage-fee-rent]
url: https://ethresear.ch/t/ethereum-state-rent-for-eth-1-x-pre-eip-document/4378
views: 6322
likes: 8
posts_count: 27
---

# Ethereum State rent for Eth 1.x pre-EIP document

Here is the document about state rent: https://github.com/ledgerwatch/eth_state/blob/58351eb8b70fa6031da1e23c1a77d982be677078/State_rent.pdf

Because I wrote most of it, it most probably reflects lots of my opinions, but I tried to incorporate alternative points of view to the extent it would still make description tractable.

## Replies

**vbuterin** (2018-11-26):

Thanks for producing this!

> Priority queue

This seems like a substantial amount of protocol-layer complexity, and I disagree with the assertion that it “does not bring significant overhead”. One priority queue update is O(log(N)) but account state updates themselves are also O(log(N)), and the size of the priority queue and the existing account tree are both O(N); so it’s definitely a constant factor increase, and it seems like it could be a 1:1 factor.

Why not just allow a zero-gas transaction type that pokes up to N accounts to be deleted and then let miners add such a transaction to their blocks?

Regarding rent I’ll copy over a comment I made in another forum:

> A third possibility that I have not yet seen discussed is to start off by raising the gas limit and increasing the SSTORE cost (possibly greatly increasing it, eg. 4-5x; also NOT increasing refunds to mitigate gastoken), and then start architecting a precompile that manages a cheaper class of temporary storage that follows some rent scheme.

---

**AlexeyAkhunov** (2018-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I disagree with the assertion that it “does not bring significant overhead”

By not significant overhead I meant something that could be dealt with by software optimisation without protocol design. In other words, it does not raise algorithmic time/space burden higher than it is, and the constants of the O()s can be made smaller

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Why not just allow a zero-gas transaction type that pokes up to N accounts to be deleted and then let miners add such a transaction to their blocks?

Thought about that. Given that one of the important function of such transactions is eviction notifications, which could, together with other computation, be computationally heavy, my opinion is that relying on miners to do these computations for free is not sufficient.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> start off by raising the gas limit and increasing the SSTORE cost

This is definitely possibly, but at the point when such raise is announced, it must be fairly certain that the rent WILL be introduced, otherwise there will be rush to occupy the storage (and then resell it via proxy contracts) before the raise

---

**vbuterin** (2018-11-26):

> Thought about that. Given that one of the important function of such transactions is eviction notifications, which could, together with other computation, be computationally heavy, my opinion is that relying on miners to do these computations for free is not sufficient.

Why would evictions be computationally heavy? A miner could just randomly select a slice of 1/4096 of the state (a few tens of thousands of accounts), determine the time-to-live of each one, then keep track of changes to those accounts and update the TTL when an account gets modified, and when the miner makes a block they create a transaction that specifies the accounts that are expired. The overhead is O(1) per account rather than O(log(n)), and the work only needs to be done miner-side; clients just process the eviction transaction with accounts that the miner specified.

---

**AlexeyAkhunov** (2018-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Why would evictions be computationally heavy? A miner could just randomly select a slice of 1/4096 of the state (a few tens of thousands of accounts), determine the time-to-live of each one, then keep track of changes to those accounts and update the TTL when an account gets modified, and when the miner makes a block they create a transaction that specifies the accounts that are expired. The overhead is O(1) per account rather than O(log(n)), and the work only needs to be done miner-side; clients just process the eviction transaction with accounts that the miner specified.

This could work, if there is some sort of reward to incentivise miners to do these kind of computations. However, as a design principle, I would prefer not to give miners any more powers than what they currently have.

---

**vbuterin** (2018-11-26):

Why even have a reward? Even if 10% of miners do it out of the kindness of their hearts that’s still enough to push the objects out of the state. In that case, a miner’s powers are very limited: they can poke bankrupt objects out of existence, or they can not do it and allow the object to exist for another ~10 blocks until someone else pokes them.

I feel that the minor increases in power to miners that arise from this are vastly outweighed by the gains from not needing to add an entire category of data structure (priority queues) to the consensus layer…

---

**AlexeyAkhunov** (2018-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I feel that the minor increases in power to miners that arise from this are vastly outweighed by the gains from not needing to add an entire category of data structure (priority queues) to the consensus layer…

Let’s see what it comes down to in a proof of concept

---

**jvluso** (2018-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> This could work, if there is some sort of reward to incentivise miners to do these kind of computations. However, as a design principle, I would prefer not to give miners any more powers than what they currently have.

Why does this give miners more power than they already have more than anyone else? If there is a reward, anyone can claim it, miners will just have a frontrunning advantage. We can even measure the reward in gas so that it doesn’t cause any inflation - miners would be able to collect more gas fees by participating, or non-miners would be able to get a discount on large transactions.

---

**AlexeyAkhunov** (2018-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/jvluso/48/1490_2.png) jvluso:

> If there is a reward, anyone can claim it, miners will just have a frontrunning advantage

Well, this could be designed, though I wanted to avoid these front-running games at all. And it is not as trivial as it might seem. A new type of transaction needs to be created, because the actions it would perform have no associated opcodes to it, so it is intrinsic. To prevent DOSing, we need to make users pay for such transaction, and then fully refund that if the eviction is successful as well as create some reward out of thin air. I daresay it might introduce more complexity and non-determinism than what we would want to avoid with the priority queue. A proof of concept should uncover if the priority queue is really a challenge.

---

**pcmonk** (2018-11-26):

Thanks for this document; this is quite helpful for me as an application developer to see if my intended storage usage is within accepted norms and will be sustainable once rent is implemented.

To clarify, I assume “storage item” refers to 32-byte storage slots?  How did you calculate the storage associated with a particular contract?

---

**AlexeyAkhunov** (2018-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/pcmonk/48/2862_2.png) pcmonk:

> To clarify, I assume “storage item” refers to 32-byte storage slots? How did you calculate the storage associated with a particular contract?

Yes, 1 storage item is 32-byte storage slot. I current use a very ad-hoc method which works on top of Turbo-Geth’s database, something like this: [turbo-geth-archive/cmd/state/state.go at 00f5e6590b81c7a5b3142879b472c40df194eff6 · AlexeyAkhunov/turbo-geth-archive · GitHub](https://github.com/AlexeyAkhunov/go-ethereum/blob/00f5e6590b81c7a5b3142879b472c40df194eff6/cmd/state/state.go#L1059)

Potentially, when this is more developed, and I managed to get someone to help me with this, it could be more exposed as an API or something.

---

**antoineherzog** (2018-11-27):

Congrats [@AlexeyAkhunov](/u/alexeyakhunov) for your good work. Rent is an absolute necessity for the future of Ethereum.

I would personally focus only on Reactive maintenance for now as it is enought to have a solid proof of concept. Regarding Token dust griefing attack, I am not sure it is a huge problem to solve for two reasons:

-> issuer of an active token will be ready to pay for the storage as it is is own interest to have an active token

-> Any token holder with access to transfer function can increase storage rent but it means I will send some token out. It can be spam only if it is very very small amount. One way to reduce that the problem is to reduce the number of decimal of the token which seems healthy I think.

---

**AlexeyAkhunov** (2018-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/antoineherzog/48/2642_2.png) antoineherzog:

> issuer of an active token will be ready to pay for the storage as it is is own interest to have an active token

This thought, of course, crossed our minds too. What if there is no issuer, i.e. token is unmanned? Don’t want to have a system where each popular contract needs a wealthy donor. And don’t want to require that everything is a DAO.

![](https://ethresear.ch/user_avatar/ethresear.ch/antoineherzog/48/2642_2.png) antoineherzog:

> One way to reduce that the problem is to reduce the number of decimal of the token which seems healthy I think.

I think what you describing is the “Alternative point of view” on the page 23 ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**antoineherzog** (2018-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> This thought, of course, crossed our minds too. What if there is no issuer, i.e. token is unmanned? Don’t want to have a system where each popular contract needs a wealthy donor. And don’t want to require that everything is a DAO.

I agree with you! We just need to go step by step ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**AlexeyAkhunov** (2018-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/antoineherzog/48/2642_2.png) antoineherzog:

> I agree with you! We just need to go step by step

Well, the document I have attached has 6 steps ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**johba** (2018-11-27):

I want to understand the main position better in relation to contract storage:

- If currently existing contracts are NOT upgradeable, they will loose their storage and need to be redeployed (potentially at the same address). From this point on they can use either active or reactive maintenance approach.
- If currently existing contracts are upgradeable, they will be able to transition into maintenance without the extra step of redeployment.

In either case their code needs to change.

If so, here comes a proposal in relation with this statement:

> If the notion of rent is introduced without a “safe place” to migrate to, the only recourse of current contracts would be to use reactive maintenance approach, in the form of stateless contracts, which might too big of a leap in terms of usability.

If contracts need be updated with new code, do they really need a “safe place”? They could be rewritten into state-minimized versions with slightly modified interfaces. Very simple steps could go a long way:

- increase storage op-code cost a lot.
- create op-code that manages account storage root directly at old sstore/sload price.
- provide a precompile that allows to cheaply verify patricia merkle proofs  in solidity.
- extend the ERC20/721 interfaces with a param to pass proofs.

this would give you:

- reduced problem space to managing rent on account-level only.
- contracts are incentivized to be written so that they manage the storage root themselves with off-chain data.
- You have a fallback for all the lazy guys (old sstore/sload) that comes at cost.
- new market of trust-free data service providers that hook as proof-providers into web3.js.

---

**AlexeyAkhunov** (2018-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/johba/48/20905_2.png) johba:

> In either case their code needs to change.

Unfortunately, the way I see it, most contracts will need to be re-written, re-deployed, and re-filled with data. To me it is the choice - either contracts need to be changed, or platform has to die.

![](https://ethresear.ch/user_avatar/ethresear.ch/johba/48/20905_2.png) johba:

> If contracts need be updated with new code, do they really need a “safe place”? They could be rewritten into state-minimized versions with slightly modified interfaces. Very simple steps could go a long way

In my opinion, asking them to just keep data off-chain and use Merkle proofs is not going to be very attractive. On pages 52-55 I tried to illustrate two main issues with that - contention of proofs and necessity for a sub-protocol for new users to be able to join.

![](https://ethresear.ch/user_avatar/ethresear.ch/johba/48/20905_2.png) johba:

> increase storage op-code cost a lot.

Yes, this has been suggested a lot in response to apparent complexity of the proposal. I would say (and perhaps I will add it to the next version of the document) - when you increase cost of storage op-codes to compensate for storing data forever, you would probably make it too expensive for anyone to use. This is because there will be no middle ground, which is keeping data for some period of time. Everyone will either have to have no data stored, or data stored forever. I did not do numbers on these, but it seems very inflexible to me.

---

**johba** (2018-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> On pages 52-55 I tried to illustrate two main issues with that

should have read the whole thing ![:innocent:](https://ethresear.ch/images/emoji/facebook_messenger/innocent.png?v=12) thx

---

**johba** (2018-11-27):

[@AlexeyAkhunov](/u/alexeyakhunov) indeed amazing doc. thx for the writeup.

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> In my opinion, asking them to just keep data off-chain and use Merkle proofs is not going to be very attractive.

Agree, and yet there should be a choice/market if you want. Currently a state-minimized contract is more expensive to reading or writing storage directly, which gives the chain a monopoly on storage.

Whatever the new design for rent is, other approaches should be able to compete.

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> This is because there will be no middle ground, which is keeping data for some period of time.

An ever increasing price schedule for the cost of the sload/sstore opcodes would discourage use or gastoken, while leaving time to migrate contracts.

![](https://ethresear.ch/user_avatar/ethresear.ch/antoineherzog/48/2642_2.png) antoineherzog:

> I would personally focus only on Reactive maintenance for now as it is enought to have a solid proof of concept.

I have the same intuition: if in question - try to remove rather than add. Also if contracts need to change in 1.x, why not [prepare them to move to 2.0 already](https://ethereum-magicians.org/t/auditable-storage-passing/1722).

---

**AlexeyAkhunov** (2018-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/johba/48/20905_2.png) johba:

> Whatever the new design for rent is, other approaches should be able to compete

Precisely. The new design has to exist though, for it to compete ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/johba/48/20905_2.png) johba:

> discourage use or gastoken

GasToken is not the major contributor to the state growth. Major contributor is the collective growth of many token contracts. Also, as State rent becomes likely, the use of GasToken will diminish, out of expectation that hoarded storage will need to be maintained or disappear.

![](https://ethresear.ch/user_avatar/ethresear.ch/johba/48/20905_2.png) johba:

> if contracts need to change in 1.x, why not [prepare them to move to 2.0 already]

Because the whole premise of Eth1.x is that Eth 2.0 might be too far in the future and too uncertain, and ecosystem needs to live on

---

**PhABC** (2018-11-27):

[@vbuterin](/u/vbuterin)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A third possibility that I have not yet seen discussed is to start off by raising the gas limit and increasing the SSTORE cost (possibly greatly increasing it, eg. 4-5x; also NOT increasing refunds to mitigate gastoken), and then start architecting a precompile that manages a cheaper class of temporary storage that follows some rent scheme.

Would the overhead be too large if the `SSTORE` cost was dynamically calculated for each ~~`msg.sender`~~ `tx.origin`? Something like ![image](https://ethresear.ch/uploads/default/original/2X/3/34d6e4e04a2594431894d0a2456ce6bdd6817fc3.png)

where ![image](https://ethresear.ch/uploads/default/original/2X/6/6ce93c1666d159eb5da5f7b3883cdddaf276283e.png)  is the the current SSTORE operation cost for a given EOA `i` and `N` is the number of storage slot currently used for EOA `i`.

The cost doesn’t need to be linear. It seems to me like this creates an incentive for users to “clean” their storage or they pay a premium for every new operation. With this simple scheme, users could, however, just always create new accounts to reset the counter. This could perhaps be mitigated if the first SSTORE is much more expensive and if we use a logarithmic curve instead of a linear one when calculating `SSTORE_i`.

The advantages of a scheme like this would be that the UX would be identical as it is now and I believe it would be backward compatible with currently existing contracts.


*(6 more replies not shown)*

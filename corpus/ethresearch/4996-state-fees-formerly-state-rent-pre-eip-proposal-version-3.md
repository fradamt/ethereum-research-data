---
source: ethresearch
topic_id: 4996
title: State Fees (formerly State rent) pre-EIP proposal version 3
author: AlexeyAkhunov
date: "2019-02-14"
category: Economics
tags: [storage-fee-rent]
url: https://ethresear.ch/t/state-fees-formerly-state-rent-pre-eip-proposal-version-3/4996
views: 6438
likes: 9
posts_count: 17
---

# State Fees (formerly State rent) pre-EIP proposal version 3

Version 3 is now up for discussion.

Main changes compared to version 2:

- Replay protection for externally owned accounts changed from temporal to non-temporal to ensure that account nonces are never reused (reuse of nonces allow re-creation of contracts)
- Lock-ups are replaced with rent prepayments. Prepayments provide protection from dust griefing vulnerability, though temporary rather than permanent. Prepayments cannot be released, which avoids issues of changing economics of some smart contracts, like DEXs
- State counters are introduced to make the state size metrics trivially observable, as well as to provide future path for floating rent, if needed.
- Transaction format is not modified
- Functionally of gaslimit (field of a transaction) is extended so that gaslimit*gasprice limits prepayments
- Floating rent and “clean” eviction of contracts are re-added for completeness as optional changes


      [github.com](https://github.com/ledgerwatch/eth_state/blob/b3cd6f9b9fd0455ad26462e4f69d1c6cfda727f8/State_Fees_3.pdf)


    https://github.com/ledgerwatch/eth_state/blob/b3cd6f9b9fd0455ad26462e4f69d1c6cfda727f8/State_Fees_3.pdf

###

## Replies

**vbuterin** (2019-02-17):

I love the idea of using existing storage slots to store these new variables! Will definitely reduce overhead and risk for implementers very significantly.

Is the idea that prepayments would cover N years of rent for some specific N?

If so, the combination of prepayments and rent basically means that existing contracts, or new contracts built according to current development patterns, are only guaranteed to be attack-resistant if they are intended to survive for less than N years; is that correct?

I am definitely lately a fan of prepayments over lockups as I’d say a $0.5 payment is better UX than a $7 lockup (or whatever the fees would end up being).

---

**AlexeyAkhunov** (2019-02-17):

Thank you very much for reading the proposal!

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Is the idea that prepayments would cover N years of rent for some specific N?
>
>
> If so, the combination of prepayments and rent basically means that existing contracts, or new contracts built according to current development patterns, are only guaranteed to be attack-resistant if they are intended to survive for less than N years; is that correct?

Yes, that is the idea!

---

**vbuterin** (2019-02-18):

Thinking about what the proposed values for N and the absolute rent rate would look like…

I think we can safely assume that much less than 10m ETH will go into expanding the state; for reference, 422k ETH was spent on transaction fees to date.

Also, for reference, the *current cost* of filling storage, assuming the current average gasprice of 12 gwei is:

- Storage key: 20000 gas -> 2.4 * 10^{-4} ETH
- Account: 32000 gas -> 3.84 * 10^{-4} ETH
- Code byte: 200 gas -> 2.4 * 10^{-6} ETH

If we want per-year prices, we can multiply per-block prices by 2 million; your proposals would give 4 * 10^{-3} ETH per account and 2 * 10^{-5} per code byte, so current prices would roughly equal prices for a month of lifetime in the new model.

I suppose that if we want to increase the gas limit to 40m eventually, while keeping storage size lower than it is today, something close to this level of repricing is the only way to do it…

---

**vbuterin** (2019-02-18):

Now there’s the question of what N is…

The per-storage-slot rent, interpolated from the proposals in the slides, would be around 3 * 10^{-3} ETH per year, so the N that your slides imply would be 6.67 years, which seems unreasonably high. The reason is that if we mandate a prepayment, then that means that users of *any* application would have to pay enough to make their application survive at least N years, and most applications don’t need to survive that long.

---

**AlexeyAkhunov** (2019-02-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The per-storage-slot rent, interpolated from the proposals in the slides, would be around 3∗10−33 * 10^{-3} ETH per year, so the N that your slides imply would be 6.67 years, which seems unreasonably high

Yes, it is quite high. When I was updating the proposal, I did not know how to calculate these numbers yet. Thank you for your help doing it, I will rethink and update the proposal

---

**Zergity** (2019-02-19):

> Replay protection for externally owned accounts changed from temporal to non-temporal to ensure that account nonces are never reused (reuse of nonces allow re-creation of contracts)

I see you try to use txCount to re-create the evicted account. Where do you store the txCount, or is it a global value to track all total tx count of the whole network?

---

**AlexeyAkhunov** (2019-02-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/zergity/48/5716_2.png) Zergity:

> I see you try to use txCount to re-create the evicted account. Where do you store the txCount, or is it a global value to track all total tx count of the whole network?

Thanks for reviewing!

txCount is a global value to track all total tx count of the whole network. And it is stored in the index 0 of the state counters contract (which is introduced in change A)

---

**Zergity** (2019-02-20):

I think that could work. Thanks.

---

**kz** (2019-08-03):

Hi,

[@AlexeyAkhunov](/u/alexeyakhunov) Wow, I can imagine these write-ups took a lot of time.

I hope that you’ll maybe find some time to answer some of the questions I have. I really liked your first proposal.


      [github.com](https://github.com/ledgerwatch/eth_state/blob/58351eb8b70fa6031da1e23c1a77d982be677078/State_rent.pdf)


    https://github.com/ledgerwatch/eth_state/blob/58351eb8b70fa6031da1e23c1a77d982be677078/State_rent.pdf

###








I like the version 3 improvements regarding simpler way to use txcount to prevent non-contract account resurrection issues, but I am confused with the other changes.

It seems to me that the introduction of the linear cross-contract storage was to bind the costs of paying for the storage to the beneficiary account? Why was that removed from proposal version 3?

It seemed to me that the primary high level purpose of this should be to bind beneficiaries of data storage with the costs of data storage.

I can’t see how the proposal version 3 will stop anyone from storage spamming shared storage contracts (exchanges, tokens) which form the majority of the ecosystem and have the regular users pay for that storage. It seems to me it actually adds malicious spamming incentives.

Maybe I’m misunderstanding something so please help me to understand. Let’s assume that there is some useful ERC20 token and there is a small set of users actually using it for some beneficial purpose. Let’s also assume that 90% of storage is used by whales, ICO scammers or is a result of dust attacks, or what ever. I don’t think this is far fetched percentage, it’s probably even far worse in practice. It seems to me that those 10% of users who are actually using it will cover the 100% of maintenance costs. How is this fair?

I can’t see what are the benefits of evicting contracts from the storage. As far as I can tell there are 2 cases.

- Either all nodes still need to store graveyard state, in which case there is no benefits.
- There is some way to recover data using merkle proofs, in which case there isn’t any benefits from doing that vs just creating a new contract and filling the data. (please read below for shared libraries)
Can somebody please help me to understand this dilemma or point me to some links that solve it?

I can understand that there are probably some library contracts which are used by multiple contracts and that poses an issue what happens if the disappear, but IMHO that’s a bad design anyway because if makes it harder to reason who should bear the costs of maintaining these shared contracts.

I think that library contracts were the first idea how to reduce code storage costs, but that problem could be solved in a different way.

Instead of using a shared library for which it’s hard to define who is paying for it, one could use properties of RLP encoding and patricia trees to make sure that shared codebases are deduplicated because of the way data is stored in Ethereum.

That would give automatic garbage state collection to the platform. If somebody is not using some contract, the patricia tree nodes would be unreachable and it would be possible to clean them up, forever.

---

**vbuterin** (2019-08-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/kz/48/685_2.png) kz:

> It seems to me that the introduction of the linear cross-contract storage was to bind the costs of paying for the storage to the beneficiary account? Why was that removed from proposal version 3?

I believe the reason it’s not needed is that you can replicate the effects of linear cross-contract storage with a one-account-per-storage-item approach that uses CREATE2.

> in which case there isn’t any benefits from doing that vs just creating a new contract and filling the data.

So I do have a proposal where at layer 1 resurrection is not possible, and you *do* have to just create a new contract, and then we can create a higher-level contract which acts as a “proxy” for contract creation, and that contract can enforce a rule that says “if you create a contract, you have to either prove that a contract at the same address never existed before, or prove that a contract existed before and H was the contract’s state the *last* time the contract was destroyed; in the latter case the contract can only be initialized with state H”. So given a base-layer blockchain with no resurrection, you can build resurrection on top. But the problem is that with Alexey’s proposals we are dealing with updating an *existing* blockchain where contracts are written to use storage directly, so we can’t use such tricks. And contracts currently frequently depend on other contracts, and so we need an explicit way of reviving them if required.

---

**kz** (2019-08-03):

Hi [@vbuterin](/u/vbuterin),

Thanks for helping me to understand.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I believe the reason it’s not needed is that you can replicate the effects of linear cross-contract storage with a one-account-per-storage-item approach that uses CREATE2.

If I understand this correctly, this would in theory have equivalent result, but the costs are order of magnitude different?

Aren’t t there 2 big costs? Additional overhead of contract code and its rent + gas costs for SLOAD replacement.

SLOAD costs 200 gas (I think). If every SLOAD is replaced with a check does the external contract have the correct code (EXTCODEHASH, sure this one can be only called once) and then call to fetch the data, that is a big overhead, isn’t it?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> But the problem is that with Alexey’s proposals we are dealing with updating an existing blockchain where contracts are written to use storage directly, so we can’t use such tricks. And contracts currently frequently depend on other contracts, and so we need an explicit way of reviving them if required.

State_Fees_3.pdf references exclusion proofs in [research/papers/pricing/ethpricing.pdf at 6652919a0ff40c5f10ec2104baae2b8f9cc5fb57 · ethereum/research · GitHub](https://github.com/ethereum/research/blob/6652919a0ff40c5f10ec2104baae2b8f9cc5fb57/papers/pricing/ethpricing.pdf)

But I can’t find them.

Wouldn’t it be possible to just have a rule that if the contract hasn’t been resurrected for a certain amount of time (like a year), then it can only be resurrected by uploading state (hash stub is small enough). If there is a small amount of state in question (like a small personal storage contract), then this is feasible to upload in a single transaction. If nobody noticed that some contract with huge state is missing for a year (nobody interacted with it) or paid for its storage, then why should the ETH community care about it?

---

**vbuterin** (2019-08-04):

> Additional overhead of contract code

This can be made near-zero with delegatecall forwarding.

> If every SLOAD is replaced with a check does the external contract have the correct code (EXTCODEHASH, sure this one can be only called once) and then call to fetch the data

That’s not how you do it. Rather, you do it by having a contract that generates child contracts using CREATE2, so `address = hash(creator, key)`, and then you do the equivalent of SLOAD by just computing the address using that formula and calling the contract.

> Wouldn’t it be possible to just have a rule that if the contract hasn’t been resurrected for a certain amount of time (like a year), then it can only be resurrected by uploading state (hash stub is small enough).

So keep stubs around and just accept the ever-growing 32-byte chunks of state as they’re much smaller than full contracts? I could see that being a reasonable de-facto compromise. Though there is a better way to do this: when a contract dies, turn it into a *receipt*, assign it a sequential ID, and keep in the state a bitfield of all IDs that have already been used. Then to wake a contract you just prove the receipt and check in the state that that receipt ID has not already been used to wake. This gives you similar properties, but with only 1 bit of permanent storage per hibernated contract rather than 256 bits.

---

**kz** (2019-08-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> That’s not how you do it. Rather, you do it by having a contract that generates child contracts using CREATE2, so address = hash(creator, key) , and then you do the equivalent of SLOAD by just computing the address using that formula and calling the contract.

I just want to be sure I’m understanding this correctly. I don’t know as much about EVM internals as you guys, so sorry if I got something wrong. My assumption is that every contract has its own storage space. The only way to access it is by calling some method in the public API of the contract.

E.g.

Reading the balance of ERC20 token now would be a single SLOAD instruction (and probably some hash to calculate the address of the SLOAD instruction).

In this new model the balance would be read by calling a public API method `getBalance` of the contract at `address = hash(creator, key)`. But before calling the public API method the main ERC 20 contract would need to make sure that the code of the child contract is correct by calling `EXTCODEHASH` (I am aware that CREATE2 takes into account hash of the code of the child contract, but the main ERC20 contract can’t store any data locally. It it does then there is no point of creating a child contract, it might as well store the balance locally).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So keep stubs around and just accept the ever-growing 32-byte chunks of state as they’re much smaller than full contracts?

Well the stubs could be kept for a period of time (e.g. 1 year). During that one year anyone using the stub would fail and if that contract is needed it would be resurrected. After that grace period (1 year) the stub can be removed.

I’m aware of only 2 instructions for creating contracts, CREATE and CREATE2. I think that only CREATE2 could create contract in the same address. But if CREATE2 does that, the code has to be equal (if some library needs to be resurrected).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Though there is a better way to do this: when a contract dies, turn it into a receipt , assign it a sequential ID, and keep in the state a bitfield of all IDs that have already been used.

Do you maybe have a writeup of these ideas somewhere? I would love to read it. I can’t understand how wouldn’t you need to store both the receipt and additionally 1 bit receipt it.

It would be great to understand how does this discussion relate with ETH 2.0. I’m assuming that this is only for ETH 1.0. Is there somewhere I can read about more detailed plans for ETH 2.0?

---

**earlz** (2019-09-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/kz/48/685_2.png) kz:

> It seems to me that those 10% of users who are actually using it will cover the 100% of maintenance costs. How is this fair?

Is there any response to this aspect? It seems like a core unsolvable problem with the current approach, short of adding a lot of complication to contract logic. For tokens for instance, there could be some burn logic applied for inactive users to compensate for their lack of rent payment, but then this just encourages effectively unneeded transactions on the blockchain just to pay rent to avoid this burn logic.

---

**sifnoc** (2019-11-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/kz/48/685_2.png) kz:

> It would be great to understand how does this discussion relate with ETH 2.0. I’m assuming that this is only for ETH 1.0. Is there somewhere I can read about more detailed plans for ETH 2.0?

Not sure what you want to see about detailed on ETH 2.0 but this article would help to understand State Rent project situation by Alexey

---

**Blaster84x** (2020-05-11):

Burning tokens is a terrible idea. What about accounts (contracts or even ordinary users) that store tokens but no ETH. These would lose all their money because of no automatic exchange logic? Keep in mind that bad UX and high costs mean less users = less validators = lower security, centralization, etc… I think “dumb” tokens (standard ERC20) under a certain storage size shouldn’t pay rent, after all Ethereum is supposed to be a real alternative to central banking. Burning would also bring problems with checking total supply and high costs for token issuers. Isn’t worth it IMO.


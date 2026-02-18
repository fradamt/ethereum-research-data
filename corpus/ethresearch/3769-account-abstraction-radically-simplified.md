---
source: ethresearch
topic_id: 3769
title: Account Abstraction Radically Simplified
author: nagydani
date: "2018-10-11"
category: EVM
tags: [account-abstraction]
url: https://ethresear.ch/t/account-abstraction-radically-simplified/3769
views: 3664
likes: 6
posts_count: 18
---

# Account Abstraction Radically Simplified

If a transaction without signature (all zeroes) is sent to a contract, the gas costs will be paid by the contract, but it is allowed to throw before some gas limit (e.g. 200 000) is reached without having the spent gas subtracted from its balance. Otherwise, if it does not throw before the gas limit is reached, it pays for all the gas used. It is up to the contract to verify eligibility, to collect tx fee within its own accounting, to protect against replays and so on. If they fail to do so, it is the contract’s balance that will be depleted, miners/validators won’t suffer any harm.

Thus, validators will always get paid for all the computational work they perform, except for a limited verification cost (O(1) per transaction), but that is fundamentally no different from how it works today: signature verification is potentially “unpaid work” for validators, but it is bounded at O(1).

The amount of changes required for EVM to support this feature are minimal: no new opcodes, no special preambles.

One way to smoothly introduce this and avoid arbitrary magic numbers baked into the spec is to set this limit initially to zero and allow it to be modified similarly to block gas limit by validator voting. The introducing HF will have an initial target set to 200 000, which they will probably quickly reach if there is no strong opposition from the community.

Even this very simple first step will allow for anonimized tokens and a host of other interesting use cases currently limited by the requirement of tx senders having Ether on the same account.

## Replies

**vbuterin** (2018-10-11):

Agree that this is one of the simpler ways to do it.

I do think that having an explicit PAYGAS opcode that turns on gas payment is useful, as then the gas limit can be turned into a client-side setting of miners, which can wait until either PAYGAS has been called or N gas has been executed, so this way miners can choose N based on how much DoS risk they’re willing to accept. Anything of this category seems fundamentally okay.

---

**nagydani** (2018-10-12):

Do I understand it correctly that PAYGAS in this case protects the contract against the preamble gas limit going below their actual preamble and thus having to pay for tx’s that they would reject as invalid?

Thus, a PAYGAS explicitly indicates the end of the preamble and if the preamble gas limit goes below the cost of reaching PAYGAS, no signatureless transaction addressed to the contract would be included in the blockchain?

---

**vbuterin** (2018-10-12):

There would be no in-protocol preamble gas limit; that would be a miner-level thing (and likely also a network protocol thing). Miners could set their own preamble gas limits based on what they think they can handle.

---

**holiman** (2018-10-12):

So, a couple of questions, carried over from previous propsals…

- Would there be any concept of ‘nonce’, at the transaction-level?

If not: how can transaction pools determine which transactions are worth keeping, and which are stale?

Would the same transaction be include:able multiple times, in multiple blocks.

- Whereby I define ‘same transaction’ as ‘same txhash’
- I assume yes, because otherwise the history-of-transactions would be an implicit consensus-sensitive datastructure

This sounds to me like it suffers from some of the same sideeffects as EIP86/208: sideeffects wihch are pretty difficult to to fully map out, but might break ‘things’ that rely on invariants such as “one transaction-hash has been executed exactly zero or one times, and can be used as an index in a database” . So I can imagine that messing things up for exchanges, for example.

---

**nagydani** (2018-10-12):

Answers:

- It is up to the contract to implement nonces, if they want to.

By running the transaction against the preamble. If PAYGAS is reached, the tx is worth keeping, if not, it is stale.

Depending on the contract, it might be possible, though it is difficult to imagine a reasonable contract that would allow it.

I do not think that in practice tx’s included in the blockchain multiple times would cause issues, because the target contract is part of the tx hash meaning that the same tx can only be accepted multiple times by the same contract. So it will be a (probably rare) class of contracts that accept the same tx multiple times and I do not think that exchanges will have anything to do with it. Token contracts definitely won’t have this property.

---

**vbuterin** (2018-10-12):

I expect the main kind of transaction that would get included multiple times is an empty “ping” transaction that calls some contract directly from the NULL_SENDER.

---

**nagydani** (2018-10-16):

Yes, that is my expectation as well; just turn the crank on the contract to do whatever it is supposed to be doing; essentially, it is a workaround for the block gas limit as the contract can perform some task that takes more gas than the block gas limit, paid out of its own balance, with minimal external input.

---

**nickjohnson** (2018-10-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/nagydani/48/4418_2.png) nagydani:

> It is up to the contract to implement nonces, if they want to.
>
>
> By running the transaction against the preamble. If PAYGAS is reached, the tx is worth keeping, if not, it is stale.

What about queueing transactions? Will it become impossible for an account to issue multiple transactions with a firm expectation on execution order?

![](https://ethresear.ch/user_avatar/ethresear.ch/nagydani/48/4418_2.png) nagydani:

> I do not think that in practice tx’s included in the blockchain multiple times would cause issues, because the target contract is part of the tx hash meaning that the same tx can only be accepted multiple times by the same contract. So it will be a (probably rare) class of contracts that accept the same tx multiple times and I do not think that exchanges will have anything to do with it. Token contracts definitely won’t have this property.

It will certainly introduce issues: The majority of existing infrastructure treats a transaction hash as a unique identifier for an execution. Anywhere this happens, it could be abused to create vulnerabilities by issuing repeated transactions.

---

**fubuloubu** (2018-10-23):

Is there any reason the nonce can’t be a random number instead of always incrementing?

---

**nagydani** (2018-10-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/nickjohnson/48/157_2.png) nickjohnson:

> nagydani:
>
>
> It is up to the contract to implement nonces, if they want to.
>
>
> By running the transaction against the preamble. If PAYGAS is reached, the tx is worth keeping, if not, it is stale.

What about queueing transactions? Will it become impossible for an account to issue multiple transactions with a firm expectation on execution order?

It really depends on the contracts. For a broad range of use cases, there will be a relaying contract that does require nonces and generally works the same way ETH transactions currently work with the exception that signature verification and nonce checking is done in the preamble part of the relaying contract. These accounts are going to have the same guarantees as external accounts currently have.

In some other cases, such as privacy-enhancing coin contracts, this is downright undesirable. There, you want coins to be completely fungible, with no predetermined ordering of spending.

![](https://ethresear.ch/user_avatar/ethresear.ch/nickjohnson/48/157_2.png) nickjohnson:

> nagydani:
>
>
> I do not think that in practice tx’s included in the blockchain multiple times would cause issues, because the target contract is part of the tx hash meaning that the same tx can only be accepted multiple times by the same contract. So it will be a (probably rare) class of contracts that accept the same tx multiple times and I do not think that exchanges will have anything to do with it. Token contracts definitely won’t have this property.

It will certainly introduce issues: The majority of existing infrastructure treats a transaction hash as a unique identifier for an execution. Anywhere this happens, it could be abused to create vulnerabilities by issuing repeated transactions.

As argued above, that is not the case. It is up to the contract to protect itself against replays and in the vast majority of cases preambles of contracts will reject replayed transactions; especially in cases where they might be attack vectors. The only use case I can think of is that mentioned by [@vbuterin](/u/vbuterin), when the contract is executing autonomously, just requires a ping to continue computations, when the  complete execution would go beyond the block gas limit. Can you think of any other contract that has a reason to allow tx replays?

---

**nickjohnson** (2018-10-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/nagydani/48/4418_2.png) nagydani:

> For a broad range of use cases, there will be a relaying contract that does require nonces and generally works the same way ETH transactions currently work with the exception that signature verification and nonce checking is done in the preamble part of the relaying contract. These accounts are going to have the same guarantees as external accounts currently have.

But how? The relaying contract can only accept or reject transactions; what’s to stop a miner sending transactions to it in the wrong order? For that matter, how does the miner even know what order to submit them in, since it will no longer have insight into the nonce?

![](https://ethresear.ch/user_avatar/ethresear.ch/nagydani/48/4418_2.png) nagydani:

> As argued above, that is not the case. It is up to the contract to protect itself against replays and in the vast majority of cases preambles of contracts will reject replayed transactions; especially in cases where they might be attack vectors.

I’m not thinking about onchain stuff - I’m talking about offchain. Block explorers, dapps, exchanges, pretty much all of them have the baked in assumption that a transaction is executed either 0 or 1 times.

---

**fubuloubu** (2018-10-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/nickjohnson/48/157_2.png) nickjohnson:

> For that matter, how does the miner even know what order to submit them in, since it will no longer have insight into the nonce?

What if the nonce is a timestamp instead? That would satisfy being somewhat arbitrary (you can write whatever timestamp you want realistically) but strictly ordered since we can enforce that a transaction must have a higher timestamp than any before it. Someone could send a higher fee if they wanted to by submitting the same timestamp later with a higher gas price, but the hard ordering of `lastTxnTime < txnTime <= blkTime`  would prevent a replay attack.

There is probably some issue with the miner/validator block timestamp choice, and with putting out multiple transactions at once since a miner could mine a later transaction earlier, but I think it would be interesting to debate the merits of this. We could enforce that a transaction newer than the block timestamp is invalid and doesn’t award a fee to solve the first one.

---

**nagydani** (2018-10-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/nickjohnson/48/157_2.png) nickjohnson:

> nagydani:
>
>
> …These accounts are going to have the same guarantees as external accounts currently have.

But how? The relaying contract can only accept or reject transactions; what’s to stop a miner sending transactions to it in the wrong order? For that matter, how does the miner even know what order to submit them in, since it will no longer have insight into the nonce?

They don’t have to. Essentially, the operations currently executed by the node’s code (i.e. checking the nonce and the signature) will be executed by the contract in the preamble. Suppose you have two transactions, `tx0` and `tx1`, submitted to the same contract in quick succession. They have RSA signatures and nonces 0 and 1, respectively. There has been no transaction sent to this contract signed by this key before. If, by chance, `tx0` gets tried first, it will be accepted and afterwards `tx1` will also be accepted. If `tx1` is tried first, it fails and is removed from mempool after which `tx0` executes normally. After rebroadcasting `tx1`, it also gets into the blockchain. This is pretty much exactly the same behavior you’d see with regular external transactions sent to the mempool out-of-order. There is no difference, I believe.

---

**nickjohnson** (2018-10-27):

The difference is that you can’t just send-and-forget any transaction with a nonce higher than the next one. If you do so, on average you have a 1/n chance of it actually being included instead of immediately discarded by nodes, which effectively breaks any concurrent usage of accounts.

---

**nagydani** (2018-10-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/nickjohnson/48/157_2.png) nickjohnson:

> The difference is that you can’t just send-and-forget any transaction with a nonce higher than the next one. If you do so, on average you have a 1/n chance of it actually being included instead of immediately discarded by nodes, which effectively breaks any concurrent usage of accounts.

If you currently send a tx with a nonce that is too high, it (obviously) does not get included in the blockchain and gets gc’d out of mempool after a short while. In the proposed system, the same would happen. Not being able to concurrently use nonced accounts is not such a big deal in my opinion. Thankfully, the proposed account abstraction mechanism allows for other means of replay protection as well. Privacy coins, which are, in my opinion, the most important use case, need to use other means anyway. In those, the ordering of coin deposits is irrelevant anyway, hence no problem with concurrent execution.

---

**technocrypto** (2018-10-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> Is there any reason the nonce can’t be a random number instead of always incrementing?

Random nonces are fine but introduce a memory requirement of knowing which have been used, whereas incremental nonces require only storing one number per serial “queue”.

One fairly general way to support both and allow individual developers to make their own tradeoffs is to allow nonces to be a discrete n-vector.  In whichever dimensions a tx chooses to declare, the nonce of that dimension must match the stored nonce for that dimension.  Dimensions which have never been declared don’t have to be stored and tx’s that need the random nonce can choose a random dimension from a sufficiently high space (~128 bits would probably be plenty). This is particularly useful for hardware wallets or during offline signing when the current nonce may not be known. If the tx doesn’t need replay protection it declares the null vector. Traditional transactions use the first dimension, and then any additional “queues” you want to create just use the second, third, and so on. This still allows for a very complex degree of partial ordering where “checkpoint” transactions resync or lock queues, etc. and contracts can be permitted to disable null vectors, constrain the dimensionality, etc. if needed for the specific application.  But defaulting to full n-vector support would be a great boon to many applications that cannot assume live, chain-aware serial ordering 24/7 (state channels, hardware wallets, cold wallets, etc.)

---

**nickjohnson** (2018-10-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/nagydani/48/4418_2.png) nagydani:

> If you currently send a tx with a nonce that is too high, it (obviously) does not get included in the blockchain and gets gc’d out of mempool after a short while. In the proposed system, the same would happen.

At present, it ends up in the mempool. In the vast majority of situations, it gets mined as long as the gas price is high enough, rather than discarded network-wide - possibly even in the same block, since the miner can identify the dependency order of the transactions.

![](https://ethresear.ch/user_avatar/ethresear.ch/nagydani/48/4418_2.png) nagydani:

> Not being able to concurrently use nonced accounts is not such a big deal in my opinion.

I don’t think you should dismiss this so lightly. A *lot* of Ethereum interaction operates on the basis of queueing up one or more transactions from an account.

You also haven’t satisfactorily addressed the issue with so much Ethereum infrastructure relying on the invariant that a transaction can only be executed once at most.


---
source: magicians
topic_id: 4020
title: Implementing account abstraction as part of eth1.x
author: vbuterin
date: "2020-02-21"
category: EIPs
tags: [account-abstraction, eth1x]
url: https://ethereum-magicians.org/t/implementing-account-abstraction-as-part-of-eth1-x/4020
views: 15543
likes: 17
posts_count: 8
---

# Implementing account abstraction as part of eth1.x

### Historical work on account abstraction

- Proposed initial abstraction changes for Metropolis · Issue #86 · ethereum/EIPs · GitHub (includes some use cases)
- A recap of where we are at on account abstraction - Sharding - Ethereum Research
- Tradeoffs in Account Abstraction Proposals - Architecture - Ethereum Research
- Maximally simple account abstraction without gas refunds - Sharding - Ethereum Research

### What is account abstraction, and what are the motivating use cases?

In short, account abstraction means that not only the *execution* of a transaction can be arbitrarily complex computation logic as specified by the EVM, but also the *authorization* logic of a transaction would be opened up so that users could create accounts with whatever authorization logic they want. Currently, a transaction can only “start from” an externally owned account (EOA), which has one specific authorization policy: an ECDSA signature. With account abstraction, a transaction could start from accounts that have other kinds of authorization policies, including multisigs, other cryptographic algorithms, and more complex constructions such as ZK-SNARK verification.

**Use cases**

- Multisig wallets and other uses of smart contract wallets (eg. social recovery). Currently, such wallets require an awkward construction where there is a separate account that stores a small amount of ETH to pay for transaction fees, and that account gets refilled over time.
- Cryptography other than ECDSA. Schnorr signatures, BLS signatures, other curves and quantum-proof algorithms such as Lamport/Winternitz could all be implemented.
- Privacy solutions would no longer require “relayers”, as the verification of the proof would be moved into authorization logic and so would be a condition of fee payment.
- On-chain DEXes and similar systems where there’s often multiple transactions from many users trying to claim the same arbitrage opportunity; currently, this leads to inefficiency because many failed transactions are nevertheless published on chain, but with abstraction, it’s theoretically possible to make sure failed transactions do not get included on chain at all, improving gas efficiency.

## How would account abstraction work?

It’s easiest to describe account abstraction by walking through a series of “strawman” schemes and understanding where their flaws are.

*Note that for terminology we’ll use the word “target” as the address that the “top-level” call in an account-abstracted transaction is directed to. This ensures that we avoid the connotations of existing terminology (“destination” or “to address”) that imply that this address is the recipient of a transfer; in fact, in all of our use cases the “target” address represents the account of the sender.*

### Strawman scheme 1: Naive total abstraction

Users can send transactions from a new special address, that we call `ENTRY_POINT` (eg. set it to `2**160 - 1`), to any account, without paying for gas using the usual mechanisms. The implication is that the target of these transactions is the account of the sender, and the account code would be processing the transaction with its data and perform the desired operations.

Miners would use a simple filter to determine which transactions to accept: they check their account balance before fully processing the transaction, check their account balance after fully processing the transaction, and see if the difference is a sufficient fee. Users would simply include a `send(coinbase(), fee)` in their transaction, after any needed authoritzation steps, to pay the fee.

This approach is simple and maximally flexible. However, there are two huge problems with it.

1. It means that miners have to fully execute every transaction before they can know whether or not they should accept it. As we saw in the DAO soft fork attempt, this is a bad idea that leads to high levels of DoS vulnerability.
2. Nodes in the network have an even worse time figuring out whether or not they should propagate the transaction, because even if they execute the transaction and it seems like it would pay the miner, one single transaction could invalidate the fee-paying property of every other transaction. Hence, network-level DoS risks are even more huge.

### Strawman scheme 2: signature abstraction only

We create a third type of account, “wallet accounts”. A wallet account is like a contract, but has two pieces of code: (i) verification code, and (ii) execution code. A call from `ENTRY_POINT` to a wallet account has two steps: (i) run the verification code, using the whole transaction as input, and verify that the output is nonzero, and then (ii) run the execution code normally. The verification code execution has no access to external calls (except to precompiles), contract storage, or any ability to “write” to anything; it must be a pure function. Additionally, verification code execution has a flat gas limit of 400,000.

This scheme has basically no security risks, as everything that miners and network nodes need to do is the same as before; the only difference is that instead of ECDSA verification (a pure function), miners need to execute some EVM code inside of a restricted environment (another pure function). However, the scheme only offers a portion of the benefits of abstraction, and we can do better.

## Proposed scheme



[![Untitled Diagram](https://ethereum-magicians.org/uploads/default/original/2X/7/7a32f9e40b11040f773d6015382df488edb952f2.png)Untitled Diagram501×220 13.4 KB](https://ethereum-magicians.org/uploads/default/7a32f9e40b11040f773d6015382df488edb952f2)

Here is a concrete scheme that provides many of the benefits of full abstraction, without most of the risks. First, the EVM-level changes:

- We retain the property that there are two types of accounts, EOAs and contract accounts, the latter having only one piece of code. If desired, a subsequent fork could forcibly convert EOAs into contract accounts that have equivalent functionality, but this is not strictly needed.
- A transaction with a (0, 0) signature is treated as a transaction whose tx.origin (and hence top-level sender) is the ENTRY_POINT address (= 2**160 - 1)
- We add an opcode, PAYGAS, which takes one argument (gasprice) off the stack, deducts tx.startgas * gasprice from the balance, records that remaining_gas * gasprice should be refunded at the end of transaction execution, and records that if the transaction fails after that point, it should only revert back to the point of calling the opcode. Does nothing if not used in the top-level call frame (ie. msg.sender == ENTRY_POINT) and does nothing if used when the opcode has already been activated. Pushes 1 to the stack if successful and 0 if failed.

Now, the miner, and network node, policy:

- When a miner or network node receives a transaction, they verify that the code of the top-level contract starts with require(msg.sender == ENTRY_POINT) (exact EVM byte sequence pending). If this is not true, they reject the transaction.
- They then run the code until they reach one of three situations:

A call (except to a precompile) has been made, or an external state reading opcode (BALANCE, EXTCODE*) or an environment opcode (TIMESTAMP, DIFFICULTY, NUMBER, BLOCKHASH, COINBASE, GASLIMIT) has been used. In this case, they reject the transaction.
- 400000 gas has been spent. In this case, they reject the transaction.
- The PAYGAS opcode has been used. In this case, they accept or reject the transaction based on whether the gasprice given to the opcode is sufficient.
- Miners and network nodes do not relay more than one transaction for each account. The impact on usability from this is low because account abstraction will as a side effect enable accounts that support performing multiple operations inside of one transaction.

### Rationale

The PAYGAS opcode creates a “breakpoint” that separates transaction execution into (1) a “verification” step, which executes code that can only read the transaction and on contract storage (which might contain public keys, anti-replay nonces, Merkle roots and other info) and cannot write anything and (2) an “execution” step which is not constrained, except that nothing that takes place during the execution step is capable of reverting the gas payment determined in PAYGAS.

The only-storage-dependent and non-writing rules are there to ensure that a transaction with some target T is guaranteed to continue being valid and having the same gasprice until either (i) that transaction is included, or (ii) another transaction with target T is included. This ensures that transactions have similar technical properties to what they have today. The “ENTRY_POINT only” guard requirement is there to ensure that this rule cannot be violated by transactions with other targets calling into the account.

### Transaction hash uniqueness

There are two possible strategies to go regarding the transaction hash uniqueness invariant. The **first strategy** is to accept that this form of abstraction will remove this invariant, because nothing now strictly prevents the same transaction from being included twice (though allowing that would be inadvisable for most applications). This would require rearchitecting of some client code.

The **second strategy** is to maintain the requirement that transactions have nonces, add nonces to contracts, and keep the `tx.nonce == contract.nonce` check (and add `contract.nonce += 1` to the post-execution step). This preserves uniqueness, but harms some use cases (eg. Tornado Cash) because multiple users may send transactions at the same time, and so there may be race conditions for transactions with the same nonce. That said, note that such applications would already be limited by the network-layer “only propagate one transaction per account” rule.

One simple fix for TC and similar applications would be to shard the uniqueness-nonce space. In TC, every withdrawal must provide a “nullifier” that is cryptographically connected to their withdrawal note. The system could maintain eg. 16 contracts, each of which stores a map of used nullifiers only for a range  0…, 1…, 2… up to f… Note particularly that the *execution* phase of the transaction could call out to these other contracts and update all of them. Applications other than TC (eg. UTXO-based subsystems) could use similar principles.

## Replies

**danfinlay** (2020-02-28):

Hi, great summary of the state of the art. I think I lean towards removing the hash invariant, since nonces introduce a real choke point, but I’d love to enumerate the drawbacks more (hard to look up a tx with shared hashes).

Just curious how you came up with the 400k gas limit suggestion for the verification stage. Since the current ECRECOVER cost is only 3k, this does seem to increase the cost of verifying a transaction significantly, which in theory could create a DDoS vector if too high.

One way that could further lower this limit/vector could be to allow the verification step to be paid for in tranches. For example, a very multi-sig may pay for verification cost after every 5 signatures verified. This could also allow for accounts exceeding the 400k complexity.

---

**vbuterin** (2020-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> Just curious how you came up with the 400k gas limit suggestion for the verification stage. Since the current ECRECOVER cost is only 3k, this does seem to increase the cost of verifying a transaction significantly, which in theory could create a DDoS vector if too high.

Good question! I was setting that to be high enough to be able to verify a SNARK in the verification step (I’ve heard numbers around 200-300k gas). Unfortunately SNARK-verification isn’t really trancheable in the way that you describe ![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=12) so just running up to 400k gas pre-inclusion-guarantee may be the only approach…

> I think I lean towards removing the hash invariant, since nonces introduce a real choke point, but I’d love to enumerate the drawbacks more (hard to look up a tx with shared hashes).

Makes sense! Though it’s client devs that would have to do a bunch of hard work if the hash invariant gets removed, so would be good to hear from them on this point.

I’d also note that another way to get around the issue is to have separate “publication-time identifiers” (`hash(tx)`) and “inclusion-time identifiers” (`hash(target, nonce, tx)`), where the former are not guaranteed to be unique but the latter are. Then in the normal case, you can predict the inclusion-time identifier at publication time, but in special cases where that’s not true application devs could come up with other techniques.

---

**danfinlay** (2020-02-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Unfortunately SNARK-verification isn’t really trancheable in the way that you describe  so just running up to 400k gas pre-inclusion-guarantee may be the only approach…

And just to help me mentally model the use case of SNARK-based authorization (I don’t think in fluent SNARK), this would enable tx verification from accounts whose keys are completely unidentifiable?

My naïve approach makes me want to ask if there could be a pre-snark tranche that increases the verification gas limit for the SNARK phase. This would require the pre-verification to use a non-snark method, so I guess it would mean the account would not be fully abstracted, and somewhat resembles metatx relays today. Maybe that’s a compromise worth considering.

Since signature verification is effectively a free service that every miner is exposing to the web, if verification was expensive enough, and attackers decided to abuse it, I’d think miners might need to start layering selective logic about whose transactions they’d try verifying, and that becomes a less open network. The “barrier to entry” in some ways is the cost of authorizing a message from an unknown sender.

---

**vbuterin** (2020-02-29):

The simplest example of SNARK-based authorization is Tornado Cash running without relayers. The transactions would just appear to be “sent by” the Tornado Cash contract, and would verify the SNARK and that the nullifier is unspent (the latter is a storage lookup).

Agree that we’d need other measures if it turns out that allowing SNARK verification in pre-processing is too much. However, the existence of Zcash (which of course has to preprocess in some cases many SNARKs before accepting a transaction) suggests that it may not be that bad.

---

**rumkin** (2020-03-03):

The contract could return some ID (address, uint256 or bytes32) as a result of the verification phase. This ID identifies the sender and is used to get the nonce from a contract’s nonce storage. Then this nonce compares with the transaction’s nonce. For SNARKs this ID will be always the same.

---

**vbuterin** (2020-03-06):

That is interesting too! Though in this case, you still get the property that for applications that are “incorrectly constructed”, a tx indentifier could repeat for multiple transactions, and so code would still need to be written to handle that case.

---

**cdili** (2020-05-14):

From the Account Abstraction discord channel [Discord](https://discord.com/channels/595666850260713488/700028534114222171)

# Account Abstraction, Stateless Mining Eth1.x/Eth 2 Implementation, Rationale Document


      ![](https://ethereum-magicians.org/uploads/default/original/1X/9820c4fe404a7e163dc1dc0a8d644cddd3e4bc2a.png)

      [HackMD](https://hackmd.io/y7uhNbeuSziYn1bbSXt4ww?view)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###










# AA Open Questions


      ![](https://ethereum-magicians.org/uploads/default/original/1X/9820c4fe404a7e163dc1dc0a8d644cddd3e4bc2a.png)

      [HackMD](https://hackmd.io/@adietrichs/Byd91DvKI)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



# AA Open Questions  This is a collection of some of the open questions around account abstraction f


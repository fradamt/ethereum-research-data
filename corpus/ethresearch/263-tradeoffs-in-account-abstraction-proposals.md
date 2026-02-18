---
source: ethresearch
topic_id: 263
title: Tradeoffs in Account Abstraction Proposals
author: vbuterin
date: "2017-11-28"
category: Architecture
tags: [account-abstraction]
url: https://ethresear.ch/t/tradeoffs-in-account-abstraction-proposals/263
views: 16085
likes: 20
posts_count: 37
---

# Tradeoffs in Account Abstraction Proposals

The goal of “account abstraction”, as conceived by [EIP 86](https://github.com/ethereum/EIPs/issues/86) and other proposals, is to reduce the number of account types from 2 (EOA and contract) to 1 (just contract), and to move functionality such as signature verification, gas payment and replay protection out of the core protocol and into the EVM. However, there are costs to doing this, including development time, transition costs, costs of storing extra code on the blockchain, breaking existing invariants and other issues. Many of these costs are much lower in the context of the current sharding roadmap where the shards can start from scratch and there is no need to upgrade any existing accounts, but some still remain.

Here are some of the possibilities, and their pros and cons.

### Lazy full abstraction

- How it works: the only type of account is a contract. There is one transaction type, which has the following fields: [gas, addr, data]. Executing the transaction consists of playing a message, with msg.sender being some standard “ENTRY_POINT” address (eg. 0xff…ff), msg.to being the addr, and the gas and data being the provided values. Users are expected to store funds in contract accounts, where the code of the contract interprets the provided data as an ABI encoding of [nonce, signature, gasprice, value, data], verifies the nonce and signature, pays gas to the miner, sends a message to the desired address with the desired value, and then asks for a refund for the remaining gas.
- Pros: makes the protocol very simple. apply_tx becomes a very trivial wrapper around apply_msg.
- Cons: requires fairly complex code inside of each account to verify the nonce and signature and pay gas. Second, requires fairly complex code in the miner to determine what transactions actually are guaranteed to pay for gas. Third, it requires additional logic for the sender and the miner to create new accounts. Finally, it introduces the possibility that, with accounts constructed in a “non-standard” way, a transaction with the same hash could get included multiple times.

The miner’s problem is as follows. The miner needs to verify, in O(1) time, that a given transaction actually is guaranteed to pay for gas if the miner decides to process the transaction and try to include it in the block. In an abstraction system, this could involve asking the miner to run some code, say, with a limit of 200000 gas, but the miner would need to be sure that, after this happens, the transaction execution is in a state where the gas is paid for, and the payment cannot be reverted. Currently, the protocol handles this automatically; in full abstraction, this must all be implemented in code, and possibly in a fairly complex way.

### Remove nonce abstraction

- How it works: same as above, except a transaction also has a nonce field. A rule is added that a transaction’s nonce must equal the account nonce, and that the nonce is incremented upon a successful transaction.
- Pros: removes the possibility of a transaction appearing in multiple places.
- Cons: increases base protocol complexity slightly, and remove the possibility of alternative schemes (eg. UTXOs, parallelizable nonces)

### Standardize signature scheme

- How it works: add a byte-array field sig to the transaction. In the top-level message, add to the transaction’s return data sighash ++ sig, where sighash is the sha3 of the transaction not including the sig.
- Pros: makes signature verification much simpler.
- Cons: increases base protocol complexity slightly.

### Add BREAKPOINT opcode

- How it works: add an opcode BREAKPOINT, which has the property that if a transaction throws after a breakpoint, it only reverts up to the breakpoint.
- Pros: makes it much easier for the miner to detect if a transaction pays for gas; the miner’s code would only need to be something like “run for N steps or until a breakpoint, see that the breakpoint has been reached, and that gas has been paid for”.
- Cons: deep and fundamental change to the EVM. Historically not the best idea.

### Add PAYGAS opcode

- How it works: takes as input one argument (gasprice), immediately transfers the gasprice * tx.gas to a temporary account, and then at the end of executing the transaction refunds any unused gas.
- Pros: makes paying for gas simpler, and particularly does not require the transaction to include merkle branches to process a call to the coinbase. Avoids the overhead of a call to the coinbase.
- Cons: increases base protocol complexity. Also does not allow abstracting gas payment, eg. paying with ERC20 tokens.

### Gasprice + PANIC

- How it works: a transaction adds a parameter gasprice. At the start of execution, gasprice * startgas is subtracted. A PANIC opcode is added, which can only be called in a top-level execution context (ie. if msg.sender == ENTRY_POINT) and where (tx.gas - msg.gas) <= PANICLIMIT (eg. PANICLIMIT = 200000). If this opcode is triggered, then the entire transaction is invalid. A user account would make sure to check the signature and nonce within the limit, preventing invalid transactions from consuming gas. Miners would run transactions with a sufficient gasprice and reject those that panic.
- Pros: account code is simple, and miner code is simple, while still adding full signature and nonce abstraction
- Cons: increases base protocol complexity slightly. Also does not allow abstracting gas payment, eg. paying with ERC20 tokens. Third, does not provide flexibility in how much time signature verification can take (though Casper already enforces a limit, so the limit can be set to be the same value).

One possible variant is to simply make the transaction invalidity behavior be part of the behavior of THROW if called in a top-level context with the given amount of remaining gas.

### Combine PANIC and PAYGAS

- How it works: remove PANIC. Instead, have all exceptions have behavior equivalent to PANIC if PAYGAS has not yet been called.
- Pros: allows accounts to set their own base verification gas limit. A miner can run the algorithm of running the code for up to N gas, where N is chosen by the miner, until PAYGAS has been called. Also, removes the need for gasprice to be part of the transaction body.
- Cons: makes the output state of a message slightly more complicated, as it also needs to carry the information of whether or not a PAYGAS opcode was triggered and if so with what gasprice.

### Salt + code in transaction

- How it works: a transaction has two new fields: salt and code. If the target account of a transaction is nonempty, then these two fields must be empty [variant: are ignored]. If the target account is empty, then the last 20 bytes of sha3(salt + code) must equal the account, and if this is the case then the code is put into that position in the account code [variant: is used as init code].
- Pros: creates a standard and clean way to create new accounts.
- Cons: adds protocol complexity.

### Newly created account pays

- How it works: a transaction can be a contract creation transaction by specifying a salt and code. If the target address is empty, then it takes funds from that address to pay for gas, and then creates the contract.
- Pros: similar to existing contract creation.
- Cons: sending the first transaction from an account takes an additional step.

### Conclusion

Currently, I favor the gasprice + PANIC approach, including both variants. But there may also be other ways to go.

## Replies

**janx** (2017-11-28):

Compare with PAYGAS, Gasprice+PANIC is more complex while keeps the same cons (not allow paying with ERC20 tokens).

---

**vbuterin** (2017-11-28):

PAYGAS is actually pretty complex, in terms of the miner logic required to accept transactions. The miner would need to still verify that the account code fits a template such that it’s guaranteed that the call won’t get reverted (alternatively, one could build in a hack where PAYGAS *is immune* to being reverted, but that’s super ugly).

PANIC, on the other hand, gives the miner an extremely simple algorithm: run the transaction for 200000 gas and see what happens.

---

**janx** (2017-11-28):

Could you elaborate more on the cons of BREAKPOINT?

---

**vbuterin** (2017-11-29):

It would require a deep change to the EVM to implement, where the EVM execution would need to keep track of where to revert to in the event of a failure. This could theoretically be done, but changes of this kind are historically super-risky.

That is the main thing I am worried about.

---

**kladkogex** (2017-11-29):

I also like Gasprice  +  PANIC.

The way I understand it, it reflects the basic principle that you cant charge a user that has not been yet authenticated.

I would tweak the description a bit in the following way

1. Each transaction has two phases: authentication phase and post-authentication phase.
2. Authentication phase is limited to PANICLIMIT of gas.  If PANICLIMIT is  reached during the authentication phase,  the transaction is rejected and no-one is charged any gas (which is totally logic - how can you charge someone who is not yet authenticated ?
3. If  signature verification fails during the authentication phase,  PANIC code is raised and the transaction is rejected without anyone paying anything.
4. If signature verification succeeds during the authentication phase, then  EVM proceeds with rest of the code, the user will ultimately pay for the execution of signature verification code during the authentication phase.

To clearly define the two phases, one should probably add IS_AUTHENTICATED flag to the EVM and explicitly require that this flag is on for some operations. As an example  state variable changes should only be allowed only if the authenticated flag is on.

If you look at other secure virtual machines, such as JavaCard, most of them have a finite state transition table where UNAUTHENTICATED and AUTHENTICATED are different states,

I think introducing a similar abstraction for EVM would improve security.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If this opcode is triggered, then the entire transaction is invalid. A user account would make sure to check the signature and nonce within the limit, preventing invalid transactions from consuming gas.

---

**kladkogex** (2017-11-29):

As far as PAYGAS goes, I do not understand it the way it is described - how can one transfer gas if the user is not yet authenticated and the signature is not verified - how can you charge  money if you dont yet know who the user is ?![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**vbuterin** (2017-12-01):

The idea is that if a contract calls the PAYGAS opcode, then the contract has decided that sufficient authentication has taken place and is willing to pay for gas.

---

**wanderer** (2017-12-01):

> Cons: requires fairly complex code inside of each account to verify the nonce and signature and pay gas. Second, requires fairly complex code in the miner to determine what transactions actually are guaranteed to pay for gas. Third, it requires additional logic for the sender and the miner to create new accounts. Finally, it introduces the possibility that, with accounts constructed in a “non-standard” way, a transaction with the same hash could get included multiple times.

there is simple way around this. The miners code have list of common entry point contract hashes that they know to be good (ie pay the coinbase ect) and the miners can simple look up the to address of tx and check its codehash.

---

**vbuterin** (2017-12-02):

> there is simple way around this. The miners code have list of common entry point contract hashes that they know to be good (ie pay the coinbase ect) and the miners can simple look up the to address of tx and check its codehash.

Yes, but this would compromise the scheme’s flexibility, and make it more difficult for people to create new types of accounts (especially for non-standard things like ring-sig contracts, UTXO schemes, etc). Furthermore, to allow full freedom of singature types, you’d need to either have a code pattern-matching mechanism, which would be complicated to write, or have the signature verification be in a separate contract, which would increase merkle proof size of every transaction.

---

**wanderer** (2017-12-02):

yes I would assume that the verification code is in a separate contract, doing so would reduce the overall state size since the code would be deduplicated

---

**vbuterin** (2017-12-02):

Right but with stateless clients that matters much less, and in fact is a bad thing as it means that transactions need to have more Merkle branches.

---

**tbrannt** (2017-12-02):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> As an example  state variable changes should only be allowed only if the authenticated flag is on.

Wouldn’t that make it less general? Maybe you want to create a contract that everyone owns (no authentication required at all). I think it’s sufficient to just roll everything back if the tx threw (PANICed)

---

**tbrannt** (2017-12-02):

I also like Gasprice + PANIC as it seems pretty straight forward to me.

---

**vbuterin** (2017-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/tbrannt/48/1050_2.png) tbrannt:

> Wouldn’t that make it less general? Maybe you want to create a contract that everyone owns (no authentication required at all). I think it’s sufficient to just roll everything back if the tx threw (PANICed)

Agree. My original proposal was to make the transaction **invalid** (and thereby any block that contains it invalid) if the tx PANICs.

---

**cdetrio** (2017-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The miner’s problem is as follows. The miner needs to verify, in O(1) time, that a given transaction actually is guaranteed to pay for gas if the miner decides to process the transaction and try to include it in the block. In an abstraction system, this could involve asking the miner to run some code, say, with a limit of 200000 gas, but the miner would need to be sure that, after this happens, the transaction execution is in a state where the gas is paid for, and the payment cannot be reverted.

The miner’s problem with verifying transactions (in an abstraction system) is essentially the same as problem as the [soft fork DoS vector](http://hackingdistributed.com/2016/06/28/ethereum-soft-fork-dos-vector/), right? That is, a miner needs to avoid wasting time processing transactions that don’t pay gas.

A key aspect of the DoS problem is that the miner needs to verify not just one transaction, but a whole block of transactions. The DoS attack exploits this by flooding the pending tx pool with spam tx’s that are initially valid, but later become invalid (after some block includes an unseen tx designed to make the pending spam tx’s invalid). If ejecting invalid tx’s from the pending pool takes longer than the block time, then miners are forced to produce empty blocks. So its not enough to verify individual tx’s in O(1) time, if it still takes O(N) time to process a pending tx pool (where N is the size of the pending pool).

To solve the miners’ problem, they need to be able efficiently (i.e. in sub-linear time) eject invalid tx’s from the pending pool. One way to do this is to keep track of each tx’s read/write range (the list of accounts and storage locations that a tx touches). Then when a new block arrives, the only pending tx’s that need to be revalidated are those with overlapping ranges (i.e. if some tx in the block has a write range that overlaps with the read range of a pending tx). The pending tx’s with non-overlapping ranges remain valid and don’t need to be reprocessed.

Does this make sense? Just want to make sure because I already said all this [in an EIP issue](https://github.com/ethereum/EIPs/issues/678), and don’t want to continue repeating myself if it doesn’t.

---

**vbuterin** (2017-12-02):

One possible issue is, what if the attacker sends N transactions with the same read/write set?

I suppose that you *could* simply add a restriction that the mempool can only have 64 transactions that share the same read/write set.

You could solve it even more easily by disabling PANIC as soon as the first external call happens - that way, you would only need to restrict to 64 transactions with the same target address, ie. basically the status quo, but that would make the scheme less general.

---

**vbuterin** (2017-12-03):

Also, do we necessarily **need** to re-process every transaction in the mempool every time we get a new block? The alternative is that we just keep them in the mempool, and when creating a block go through them and accept the ones that are still valid and delete the ones that are invalid.

One thing that **does** become harder with account abstraction is the ability to predict transaction validity going more than one account into the future. That said, what we **can** do is run an algorithm where we accept even invalid transactions into the mempool, and then every time a block changes some accounts, go through the transactions that contain those accounts in their read/write list and see if any of them become valid. One could optimize further by only going through transactions whose **sender** is one of the **senders** of the transactions in a given block. Basically, the goal would be something like “keep at most N transactions in the mempool, and use various heuristics that could be updated over time to try to make sure those are the N that are valid now or most likely to be valid in the future”.

---

**kladkogex** (2017-12-04):

Sorry guys  - I do not really understand how a contract that “everyone owns” would work.

If there is a  contract that everyone owns, any attacker can submit zillions of  transactions against it, so whatever gas this contract would own would be drained.

Please explain usefulness of such contracts, or give some examples.  My feeling is that any meaningful contract  that allows to spend gas without authentication, would suffer from this "money drain  vulnerability?  if this is not true,  please explain, may be I am missing something …

---

**AlexeyAkhunov** (2017-12-06):

For a miner to decide whether to process a transaction, they may be able to run the byte code of each contract through semantic execution (like KEVM).

If it is possible to prove that whatever the input string is, the execution either/or:

1. fails within certain bound of gas spent
2. pays gas to the miner

then this transaction is safe to start processing.

If the non-mining nodes perform the same analysis on the contract, and it is possible to prove the above, then the non-mining nodes can distinguish between cases (1) and (2) and therefore help shield miners from invalid transactions

---

**wanderer** (2017-12-14):

> they may be able to run the byte code of each contract through semantic execution (like KEVM).

This would add more computation cost for validating a tx, so is there an incentive for nonmining nodes to do this?


*(16 more replies not shown)*

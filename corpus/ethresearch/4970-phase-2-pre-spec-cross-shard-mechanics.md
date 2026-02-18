---
source: ethresearch
topic_id: 4970
title: "Phase 2 pre-spec: cross-shard mechanics"
author: vbuterin
date: "2019-02-10"
category: Sharded Execution
tags: [cross-shard]
url: https://ethresear.ch/t/phase-2-pre-spec-cross-shard-mechanics/4970
views: 7425
likes: 4
posts_count: 17
---

# Phase 2 pre-spec: cross-shard mechanics

# THIS IS A WORK IN PROGRESS!

The goal of this post is to provide a rough outline of what phase 2 might look like, to help make the discussion about state and execution more concrete as well as to give us an idea of the level and types of complexity that would be involved in implementing it. This section focuses on withdrawals from the beacon chain and cross-shard calls (which use the same mechanism); rent is unspecified but note that a hibernation can be implemented as a forced cross-shard call to the same shard.

Topics covered:

- Addresses
- Cross-shard receipt creation and inclusion
- Withdrawing from the beacon chain

### Addresses

The `Address` type is a bytes32, with bytes used as follows:

```
[1 byte: version number] [2 bytes: shard] [29 bytes: address in shard]
```

There are many choices to make for address encoding when presented to users; one simple one is: `version number - shard ID as number - address as mixed hex`, eg. `0-572-0DF5283B84D83637e3E6AAC675cE922d558b296e8B11c43881b3f91484`, but there are many options. Note that implementations may choose to treat an address as a struct:

```python
{
    "version": "uint8",
    "shard": "uint16",
    "address_in_shard": "bytes29"
}
```

Because SSZ encoding for basic tuples is just concatenation, this is equivalent to simply treating `Address` as a bytes32 with the interpretation given above.

### Cross shard receipts

A `CrossShardReceipt` object, which contains the following fields:

```python
{
    "target": Address,
    "wei_amount": uint128,
    "index": uint64,
    "slot": SlotNumber,
    "calldata": bytes,
    "init_data": InitiationData
}
```

`InitiationData` is the following:

```python
{
    'salt': bytes32,
    'code': bytes,
    'storage': bytes,
}
```

Note that in each shard there are a few “special addresses” relevant at this point:

- CROSS_SHARD_MESSAGE_SENDER: 0x10 - has two functions:

Regular send: accepts as argument (i) target: Address, (ii) calldata. Creates a CrossShardReceipt with arguments: target=target, wei_amount=msg.value, index=self.storage.next_indices[target.shard] (incrementing self.storage.next_indices[target.shard] += 1 after doing this), slot=current_slot, calldata=calldata, init_data=None.
- Yank: accepts as argument target_shard: ShardNumber. Creates a CrossShardReceipt with target=Address(0, target_shard, msg.sender), wei_amount=get_balance(msg.sender), index=self.storage.next_indices[target.shard] (incrementing self.storage.next_indices[target.shard] += 1 after doing this), slot=current_slot, calldata='',init_data=InitiationData(0, get_code(msg.sender), get_storage(msg.sender)). Deletes the existing msg.sender account.

`CROSS_SHARD_MESSAGE_RECEIVER`: accepts as argument a `CrossShardReceipt`, a `source_shard` and a Merkle branch. Checks that the Merkle branch is valid and is rooted in a hash that the shard knows is legitimate for the `source_shard`, and checks that `self.current_used_indices[source_shard][receipt.index] == 0`. If the `slot` is too old, requires additional proofs to check that the proof was not already spent (see [Cross-shard receipt and hibernation/waking anti-double-spending](https://ethresear.ch/t/cross-shard-receipt-and-hibernation-waking-anti-double-spending/4748) foe details). If checks pass, then executes the call specified; if `init_data` is nonempty and the target does not exist, instantiates it with the given code and storage.

### Withdrawal from the beacon chain

A validator that is in the `withdrawable` state has the ability to withdraw. The block has a `withdrawals` field that contains a list of all withdrawals that happen in that block, and each withdrawal is a standardized `CrossShardReceipt` obect.

A `CrossShardReceipt` created by the beacon chain shard will always have the following arguments:

```python
{
    "address_to": Address(0,
                          dest_shard,
                          hash(salt + hash(init_storage) + hash(code))[3:]),
    "wei_amount": deposit_value,
    "index": state.next_indices[dest_shard],
    "slot": state.slot,
    "calldata": "",
    "init_data": InitiationData(
        "salt": 0,
        "code": init_code,
        "storage": init_storage
    )
}
```

Where `dest_shard`, `salt`, `init_storage`, `init_code` are all chosen by the withdrawing validator. `state.next_indices[dest_shard]` is then incremented by 1. This receipt can then be processed by the `CROSS_SHARD_MESSAGE_RECEIVER` contract just like any other cross-shard receipt.

### Transactions

A transaction object is as follows:

```python
{
    "version": "uint8",
    "gas": "uint64",
    "gas_max_basefee": "uint64",
    "gas_tip": "uint64",
    "call": CrossShardReceipt
}
```

Executing a transaction is simply processing the call, except a transaction (or generally, any call that it not directly an execution of an actual cross-shard receipt) can only create an account at some address if it has the `salt` such that `target = hash(salt, hash(code) + hash(storage))`. Note that a transaction simply specifies a call to an account; it’s up to the account to implement all account security logic.

Not covered:

- Specific protocol changes to facilitate abstraction
- The exact mechanics of the fee market (see https://github.com/ethereum/EIPs/issues/1559 for a rough idea though)
- The mechanics of the rent mechanism

## Replies

**naterush** (2019-02-12):

```auto
{
    ...
    "init_data": InitiationData
}
```

Is there an important reason to keep contract creation data as it’s own field? In the spirit of abstraction, the other option would be having a contract on each shard that accepts calldata with the encoded input (salt, code, storage) - and not have a `"init_data"` field at all. This also allows contracts to create contracts on other shards using the regular send function in the `CROSS_SHARD_MESSAGE_SENDER ` contract.

On the other hand, if there are benefits to keeping these separate, then it might make sense to type the `CrossShardReceipt ` object more strongly. It seems like `"calldata"` and `"init_data"` are mutually exclusive in the current spec - so these might be better as different datatypes.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A transaction object is as follows:
>
>
>
> ```auto
> {
>     "version": "uint8",
>     "gas": "uint64",
>     "gas_max_basefee": "uint64",
>     "gas_tip": "uint64",
>     "call": CrossShardReceipt
> }
> ```

`CrossShardReceipt` should probably be renamed - it’s not cross-shard or a receipt. What about `BaseCallData`?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> target = hash(salt, hash(code) + hash(storage))

So, to confirm, the salt is concatenated with the hash of the code and the storage, and this is all hashed? Just wondering about the differening notations.

---

**vbuterin** (2019-02-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/naterush/48/4241_2.png) naterush:

> In the spirit of abstraction, the other option would be having a contract on each shard that accepts calldata with the encoded input (salt, code, storage)

Yeah, this is possible too. The only challenge is that the cross-shard receipt mechanism needs to be able to create contracts at arbitrary addresses, but transactions should not be able to do that, and so if we create from inside a contract, we would have to pass the information about whether the “ultimate source” of the instruction is a transaction or a cross-shard receipt.

> CrossShardReceipt should probably be renamed - it’s not cross-shard or a receipt. What about BaseCallData ?

Sounds good to me!

> So, to confirm, the salt is concatenated with the hash of the code and the storage, and this is all hashed? Just wondering about the differening notations.

Yes. Or more precisely, to create a *new* contract the salt is concatenated with the code and the hash of the initial storage.

Note that this removes the ability to dynamically run init code; if we want we can add that back in, but the reason I don’t have it in at the moment is that it would create further divisions between “creating” via yanking (no init code should be run) and creating an actually new contract.

---

**naterush** (2019-02-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> the cross-shard receipt mechanism needs to be able to create contracts at arbitrary addresses, but transactions should not be able to do that

To clarify, yanking a contract keeps the `[1 byte: version number]` and `[29 bytes: address in shard] ` the same, but changes the `[2 bytes: shard]`.

> Note that this removes the ability to dynamically run init code

Question for any EVM experts out there (I’m not one) - what do we lose by not having dynamically run init code? Are there applications today that rely on having this, that aren’t pathological examples?

As a side note, having the version field represent which VM actually runs this contracts code seems like a nice way of [versioning the VM](https://ethresear.ch/t/a-minimal-state-execution-proposal/4445/7).

---

**vbuterin** (2019-02-15):

> To clarify, yanking a contract keeps the [1 byte: version number] and [29 bytes: address in shard] the same, but changes the [2 bytes: shard] .

Correct!

> Are there applications today that rely on having this, that aren’t pathological examples?

The easiest actually useful example I can think of is `self.contract_creation_time = block.timestamp`. So there’s definitely *some things* that are lost.

---

**ChengWang** (2019-02-16):

How would you handle the cross-shard calls that need to update the states of both sender and receiver from different shards?

For general calls, one has to lock both states before finishing two-phase commit for the call. Otherwise, there are cases people can attack it by not finishing two-phase commit. However, locking both states from two different shards is not that practical

---

**vbuterin** (2019-02-16):

The answer at this point is: that is impossible to do directly, so what you would have to do is yank the sender into the receiving shard, perform the atomic operation, then yank the sender back.

See [Cross-shard contract yanking](https://ethresear.ch/t/cross-shard-contract-yanking/1450) for some more discussion on this (“train and hotel problem” being common local jargon for this sort of thing).

---

**ChengWang** (2019-02-16):

Just read a bit about yanking. It might have security issues beside the performance challenge.

Let’s consider the hotel-and-train problem. One person yanks a reserve contract and wants to use it in another shard. An attacker could yank the reserve contract to a third shard before the yankee could use it.

In general case, there have to be ways to “unyank” as the person yanked might disappear after yanking. Attacker could use “unyank” to attack services.

---

**vbuterin** (2019-02-17):

> Let’s consider the hotel-and-train problem. One person yanks a reserve contract and wants to use it in another shard. An attacker could yank the reserve contract to a third shard before the yankee could use it.

That could be solved at application level by having the contract’s yank functionality also reserve the contract for some users for some given amount of time.

---

**ChengWang** (2019-02-17):

> That could be solved at application level by having the contract’s yank functionality also reserve the contract for some users for some given amount of time.

That’s a practical solution, but still attackable. Attacker could pre-reserve all rooms using yank without really reserve them in the end. It’s hard to tell if it’s an attack or it’s just network issues so that the transaction for reserving both hotel and train is not committed in time.

---

**vbuterin** (2019-02-17):

Agree!

Though if the reservation period is limited (eg. to 1 epoch) then attacks would not be that big a deal. In general, making a cross-shard transaction system that doesn’t leave any room for wasted half-transactions feels like an NP-hard problem, though with lots of reasonable approximations, hence why my long-term philosophy around all of this is to set up a maximally simple base layer, and allow layer-2 mechanisms to emerge on top of it that implement models with stronger properties.

---

**ChengWang** (2019-02-17):

I tends to think making safe cross-shard transaction is impossible in general (not NP-hard), which is a bit like designing lock-free algorithm in general is impossible with only locks.

---

**villanuevawill** (2019-04-23):

The pre-spec introduces a number of discussions:

## Discoverability

How can the `CROSS_SHARD_MESSAGE_RECEIVER` be accepted in the destination shard?

**Possible solutions may be:**

**Sender submits the call as a second transaction**

- Mechanism: original sender will wait for finality on the beacon chain then submit a receive transaction on the receiving shard. This transaction requires gas submitted (without an inherent crossover from the other shard) since merkle proof verification is a non-trivial operation and the node needs an incentive to run the witness verification.
- Pros: sender has control over when the transaction is received in addition to gas prices, etc…
- Issues: The sender likely has no funds on the receiving shard and for this reason is submitting a cross shard transaction.

**Wallet provider submits the call on behalf of the sender**

- Mechanism: The wallet provider has a balance on the receiving shard and therefore submits the transaction on behalf of the user. The wallet provider would calculate the gas needed ahead of time and subtract it from the balance of the user on the source shard. For this solution to work, there must be a system in place to submit a receiving transaction on behalf of the original sender in the receiving contract. This should be trivial. Otherwise it could be included within the account abstraction model.
- Pros: Better UX for the user and avoids liveliness requirements on behalf of the user.
- Issues: Wallet providers must carry balances on all shards to issue transactions on behalf of users. This may also expose various attacks on wallet providers. Additionally, users must trust and rely on the liveliness of wallet providers to submit the receiving transaction.

**Incentive Mechanism for Others to Submit the transaction**

- Mechanism: Certain watchers or programs monitor all the shards for a CrossShardReceipt. When detected, the watchers monitor for finality and verify the transaction independently. If verified, they submit the receive transaction to the receiving shard on behalf of the original sender. Upon completion of the transaction, the watcher should receive a payment from the originator. This would either require additional arguments that state how much of the msg.value is reserved for incentives and would need to be reflected in the receipt. Alternatively, the sender could include a higher gas amount which is carried over to the receiving shard with the remaining gas being routed to the incentive provider.
- Pros: Reduces liveliness requirements of the original sender. Incentive mechanisms could make for a more distributed solution.
- Issues: Significant complexity and changes to implement. Attack vectors against the original sender where the block provider makes a deal with the watchers to prioritize against the original transaction sender’s submission. This can be mitigated against by having a flag on the CrossShardReceipt which states whether the user wants an incentive submission or not. Mempools may begin to be flooded by competing incentive providers to submit on behalf of the users.

**Beacon Chain maintains receipt records of withdrawals and `CrossShardReceipts`**

- Mechanism: Shard nodes must keep a full trie receipt record for a certain period of time from the beacon chain. When the block proposer is building a new block, its mempool may contain regular transactions and messages linked via the beacon chain receipts trie. This reduces the need for the block provider to run a merkle proof on the CrossShardReceipt. It would also require gas to carry over from the source shard or the receipt to contain its own gas values that are extracted from the original msg.value.
- Pros: Does not require third party involvement, mempool flooding, or original user liveliness. Finality is committed to the beacon chain and can abstract the behavior of cross shard transactions to follow the exact same mechanism as a withdrawal.
- Issues: Duplicating storage on beacon nodes and shard nodes. Complexity involved on incentive mechanism/gas payment. Remaining gas would be burnt or distributed to the original sender’s account address on the receiving shard. This could essentially begin forming dust across all the shards. Also brings to question what happens if there is not sufficient gas? Can the original sender rollback the CrossShardReceipt? Can the sender submit the transaction with additional gas in the case of a mistake?

## Attack Vectors

**Some vulnerabilities form due to the approaches above:**

- In the Incentive Mechanism or Beacon Chain approach above, the sender can create a lock on a contract yank by not including enough of an incentive for the transaction to ever be included in the receiving shard. In order to recover from this issue, another user must pay and submit the transaction on behalf of the original sender.
- One discussion - Cross-shard contract yanking suggests receipts must live for a year. If I submit the original send/call transaction and I am not aware of the gas fees/limits on the other shard and thus my transaction is never received, should I be able to cancel the original yank or send call to recover funds on the original shard? If I miss the timeframe, are my funds lost or is the CrossShardReceipt rolled back?
- See issues in above section for other attack vector discussions

## Opcode Requirements

Both the `CROSS_SHARD_MESSAGE_SENDER` and `CROSS_SHARD_MESSAGE_RECEIVER` require special privileges. For example, the sender may reduce balance not related to execution and may also destruct an existing account. In the case of burning funds, is this just a regular send command? In the case of destructing an account (related to yanking) do we maintain the `SELFDESTRUCT` command with additional ruling provided to the EEI function or do we introduce a separate opcode?

On the other end, the receiver may also have special privileges. In the pre-spec, there is discussion of initiation data. One thing that was not clear is whether this behavior will be allowed only for the receiver contract or if there is an expanded contract creation opcode to manage contract initiation with pre-existing storage? If so, the difference between the method by the receiver would be its ability to arbitrarily pick an address vs. enforcement of `target = hash(salt, hash(code) + hash(storage))`? Or is this behavior only reserved for a receiver? If so, a special opcode would also need to be implemented in this case. If this behavior is not only reserved for the receiver, an opcode would need special behavior if the receiver address is calling the opcode, yes?

---

**vbuterin** (2019-04-24):

Great question on how the cross shard messages get accepted.

There’s two main options I see:

1. The receipt itself includes a bounty to get included, and this bounty could even increase over time.
2. The receiver submits the receipt only when they need to do so as part of another transaction. If the receipt is sending ETH to a shard, this would be when they actually need to spend the ETH. Note that with account abstraction, you can use ETH recovered during a transaction to pay for the transaction. If the receipt is moving some other kind of object, then the expectation would be that whoever benefits from that object being on the destination shard would have ETH and could pay for its inclusion.

> Beacon Chain maintains receipt records of withdrawals and CrossShardReceipts

This sounds like every receipt would require beacon chain activity? If so, that’s O(C^2) load on the beacon chain, which is unacceptable from a scalability point of view. Also, as you mention, gas issues with attempting to guarantee cross-shard receipts are quite tricky.

---

**villanuevawill** (2019-04-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The receipt itself includes a bounty to get included, and this bounty could even increase over time.

This approach makes sense and is what is suggested here:

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> Incentive Mechanism for Others to Submit the transaction

Does this line up with your general thoughts? I really like the idea of allowing the bounty amount to increase over time.

Any thoughts on how this approach may open up locks on contract yanking that cannot be mitigated with a timeout period? In this case it would be a griefing attack since the next user who needs the contract would need to submit the transaction on behalf of the original sender before interacting with it.

Thoughts on the necessity for a `CrossShardReceipt` rollback function? Particularly after the storage expiration date.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The receiver submits the receipt only when they need to do so as part of another transaction. If the receipt is sending ETH to a shard, this would be when they actually need to spend the ETH. Note that with account abstraction, you can use ETH recovered during a transaction to pay for the transaction. If the receipt is moving some other kind of object, then the expectation would be that whoever benefits from that object being on the destination shard would have ETH and could pay for its inclusion

This makes a lot of sense as an alternative to 1 in certain cases.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If so, that’s O(C^2) load on the beacon chain

Do you mind clarifying this further?

---

**bdeme** (2019-04-25):

Due to the fact that all shard states are observable by anyone who wishes to do so, would it not be possible to have so called supervisors who verify for finality by checking for imbalances in-between states as it should be Sum(shard inflow) - Sum(shard outflow) = 0?

---

**vbuterin** (2019-04-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> Do you mind clarifying this further?

As I understand your proposal, you’re suggesting that shard blocks can have receipts on the beacon chain, and all other shard nodes need to download those receipts. That would mean that every cross-shard operation needs to be processed by the entire chain, which is not acceptable, as there’s too many of them.

Or did I misunderstand the proposal?

> Due to the fact that all shard states are observable by anyone who wishes to do so, would it not be possible to have so called supervisors who verify for finality by checking for imbalances in-between states as it should be Sum(shard inflow) - Sum(shard outflow) = 0?

I think the “verify inflow = outflow” framing is in general highly counterproductive. Ethereum sharding is meant to be general purpose, and so every application will have its own, possibly highly complex, per-shard invariants. There’s pretty much no choice but to try really hard to ensure that the state transitions on every shard are completely valid with no exception.


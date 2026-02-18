---
source: ethresearch
topic_id: 7582
title: ReGenesis - resetting Ethereum to reduce the burden of large blockchain and state
author: AlexeyAkhunov
date: "2020-06-24"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/regenesis-resetting-ethereum-to-reduce-the-burden-of-large-blockchain-and-state/7582
views: 12973
likes: 48
posts_count: 28
---

# ReGenesis - resetting Ethereum to reduce the burden of large blockchain and state

**Lessons from Cosmos Hub**

If you observed how Cosmos Hub performed their upgrade from version 1 to version 2, and then from version 2 to version 3, you would know that it was essentially done via re-starting the blockchain from a fresh genesis. Upon the upgrade, node operators had to shut down their nodes, then generate a snapshot of the state of Cosmos Hub, and then effectively use that snapshot as a genesis for launching a new blockchain, from block 1.

Now anyone who wants to join Cosmos Hub, needs to acquire genesis for CosmosHub-3, download all the blocks of CosmosHub-3 (but not CosmosHub-1 or CosmosHub-2) and replay them.

**Can we “relaunch” Ethereum 1?**

Lets look at a hypothetical application of such method in Ethereum, where we have a really large blockchain (150-160Gb), as well as fairly large state (40-100Gb depending on how you store it). The obvious gain of such “relaunch” would be that the new joiner nodes will need to start with the 40Gb genesis state and not with 150 Gb worth of blocks. But downloading 40 Gb genesis is still not a great experience.

**State in Ethereum is implicit, only its merkle root hash is explicit**

Let us now assume that we can make these 40 Gb implicitly stored “off-chain” and only the root hash being used as the genesis. And let us also start with the empty state. How do we get transactions access part of the implicit state?

Bear in mind that even now the 40 Gb is implicit and the exact way of acquiring it is an implementation detail. You can run through all 10 million blocks to compute it, or you can download its snapshot via fast sync, or warp sync, or you can even copy it from someone’s external disk and then re-verify. Although the state is implicit, we assume that the block composers (mining pools usually) have access to that implicit state and will always be able to process all transactions. What we are removing is the assumption that all other validating nodes have the access to that implicit state to check that the transactions in the block are valid and the state root hash presented in the block header matches up with the result of the execution of that block.

**Isn’t it Stateless Ethereum?**

If you followed Stateless Ethereum at all, you may recognise that this is exactly what we are trying to do there - leave the assumption that block composers have access to the implicit state, but remove the assumption that all validating nodes have the same access. We propose to do it by obligating the block composers to add extra proofs in the block, and we call these proofs “block witness”.

**Proofs in the blocks vs proofs in the transactions?**

When people first learn about this, they assume that these extra proofs are indeed provided by the transaction senders, and become part of transaction payload, but we have to explain to them that no, it is block composers’ job. But later we discovered that transactions will have to include some extra proof. Namely they will need to prove that the sending address has enough ETH to purchase the gas for this transaction, and also for all other transactions from this account but with lower nonces. They might also need to prove the nonce of the sending account, so that the node can figure out if there are any nonce gaps and therefore potential DDOS attack via a storm of non-viable transactions. More stringent checks can be done, but knowing the ETH balance and the nonce of the sending account is the necessary (but perhaps not sufficient) info for most of the DDOS-protection heuristics.

**Critique of proofs in the transactions**

Let us now imagine that we do, in fact, want transaction senders to include proofs for all the pieces of state that the transaction touches. This would be nice because it would simplify our work on trying to charge extra gas for witnesses. The main critique of this is usually to do with Dynamic State Access (DSA, as opposed to Static State Access - SSA). If transaction goes to a particularly complex smart contract, specifically, if it involves lots of nested calls to other contracts, it might be that the items of state that this transaction is going to touch, is hard to pre-calculate. And it can even be used to “trap” a user by front-running their transactions and making them fail due to insufficient proofs.

**ReGenesis provides mitigation**

The concern about DSA can not be easily solved completely, but it can be sufficiently mitigated to the point that users will very rarely see the inconvenience, and never get permanently “trapped” into never being able to achieve their desired state transition. The mitigation relies on the extra rule that any proof provided with a transaction, which checks out against the state root (but is not necessarily sufficient for the transaction to be successful), becomes part of the implicit state. Therefore, repeated attempts by the user to execute the transaction will keep growing the implicit state, and eventually, it will succeed. Any attacker that tries to “trap” the user, will have to come up with more sophisticated ways to redirect the transaction’s state access outside of the implicit state, and eventually, the attacker will fail.

As the implicit state grows from nothing (just after the “relaunching”) to include more and more of the actively accessed state, the proofs that transactions need to provide will shrink. After a while, most transactions won’t even need to attach any proofs, only the ones that touch some very old and “dusty” parts of the state.

**We can keep doing it**

I call this “relaunch” reGenesis, and it can be done regularly to ease the burden on the non-mining nodes. It also represents a less dramatic version of Stateless Ethereum.

Doing ReGenesis repetitively would simplify the architecture of Ethereum client implementations. It can mostly obviate the need for more advanced snapshot sync algorithms. If we perform ReGenesis every 1m blocks (which is roughly 6 months), then the state snapshots as well as blockchain files can be made available on BitTorrent, Swarm, IPFS. We cannot do it now because the state changes every 15 seconds, not every 6 months. If client implementations can cope with replaying 6 months worth of blocks, then we do not need very sophisticated snapshot algorithms. Consequently, complexity of Ethereum implementations will go down.

**Downsides**

I have not yet explored lots of them, but there are three that I already see:

1. Users may need to have access to the full implicit state to create transactions. I actually see this as a fair compromise
2. Users may need to repeat transactions (due to Dynamic State Access) until they eventually achieve the desired state transition
3. Some roll-up techniques (that utilise the blockchain data for data availability) may break if the network effectively “archives” all the blocks prior to the ReGenesis

**Please consider the discussion open!**

UPDATE: here is a link to the “ReGenesis Plan” document: https://ledgerwatch.github.io/regenesis_plan.html

## Replies

**poemm** (2020-06-24):

Some historical context. In March-April 2019, Alexey first solved the block witness size problem by [proposing](https://medium.com/@akhounov/the-shades-of-statefulness-in-ethereum-nodes-697b0f88cd04) that block witnesses are deduplicated against a cache of `n` recent blocks, where `n` is a fixed positive integer. Now Alexey is proposing to relax that `n` is fixed, instead basing the cache from a regenesis block number, and updating this regenesis block number every-so-often. Both of these proposed caches are variations of [least-recently-used cache](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)) and are effective at removing dusty cobweb state from hard-drives.

---

**devcorn** (2020-06-24):

Check out Tendermint State Sync:

- https://github.com/tendermint/tendermint/blob/8830176567fb9f669aaf97966480a76a1d599fc1/docs/architecture/adr-042-state-sync.md
- https://github.com/tendermint/tendermint/blob/8830176567fb9f669aaf97966480a76a1d599fc1/docs/architecture/adr-053-state-sync-prototype.md

---

**liochon** (2020-06-25):

It’s a pragmatic solution.

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> Downsides

Yes, rollups will need to be looked at, but I don’t think it’s a problem without solution: they can have snaphots as well (and if you really do 1K TPS you don’t want to replay 2 years of transactions to sync). So if we know that at time T+100 there will be a regenesis with the state at time T, then rollups-like applications need to do a snaphot between T and T+100 and they are fine.

Something to think about is logs/events. IIUC they are not pruned today.

---

**drinkcoffee** (2020-06-28):

[@mandrigin](/u/mandrigin) has done an explainer for this post here: https://medium.com/@mandrigin/regenesis-explained-97540f457807

---

**drinkcoffee** (2020-06-28):

Am I correct in thinking that the  networking requirements will go up and down in a sawtooth fashion? That is, as the start of a new million blocks, nodes start with zero state. Transaction senders will need to send witnesses for all state. The network bandwidth to send blocks will be high. Over time, as more state is included, less and less state is needed. The bandwidth to send blocks will decrease. Then at the end of a million blocks, the nodes discard all of their state and start again.

---

**PhABC** (2020-06-29):

That seems correct indeed. It will be interesting to see if uncle rate is affected by this, though it probably won’t based on some previous experiments with CALLDATA size.

---

**drinkcoffee** (2020-06-29):

The networking requirements be more even if a “moving window” state caching strategy was used. That is, nodes are expected to keep state for the past X blocks. Any state that hasn’t been touched in the past X blocks must have a witness for it.

---

**AlexeyAkhunov** (2020-06-29):

Yes, it is correct to expect that the traffic usage will go up after the reset and quickly level off after that. Good news is that we can backtest it.

And it is true that there is a similarity between ReGenesis and the “moving window” state caching strategy that I called “Semi-Stateless” in the past. The reason why ReGenesis might be preferable is because it is simpler and less error-prone to implement. Moving window state caching requires tracking for each state item when it was last touched. Evicting items very frequently (as frequently as every block) also adds non-negligible overhead. And all of that as consensus rules - I had not had a strong belief that this could ever be deployed.

With ReGenesis - the caching policy is very simple and blunt - which makes is more attractive at a cost of slight loss of elegance in the beginning of the reset cycle

---

**carver** (2020-07-08):

I like it! It has some quirks to work out.

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> a cost of slight loss of elegance in the beginning of the reset cycle

I think this slightly undersells the cost from the transaction sender’s point of view. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Transactions that get mined as failing due to an insufficient witness would be a major annoyance.

## State availability becomes consensus-critical

Miners need to be able to include a transaction that has an insufficient witness as failed, to collect the gas. If miners couldn’t include under-witnessed transactions, it would be easy to DoS nodes by forcing them to verify a flurry of 8 Mgas transactions that are missing one witnessed value, but only after successfully executing 7.9 Mgas.

Getting your transaction included as failed with a missing witness sounds pretty awkward/painful for transaction builders near the epoch boundary. You build the transaction based on the pre-ReGenesis state, then while the transaction is pending, all state disappears at the boundary.

As prevention, transaction senders could pay to include the witness when the current tip is a few blocks behind the epoch boundary, just in case it takes a while to get included. How many blocks behind the epoch should senders consider doing this? It depends on gas pricing, which might fluctuate after you send the transaction. Depending on the transaction, it might add significant cost to witness the transaction “just in case”.  (Side note: this seems mostly fixed when transactions get an “expire by block number” field.)

In addition to gas cost, I can imagine this being quite a challenge for in-browser web3 clients to support. If your node doesn’t have the cold state, the web3 client has to notify you and/or help you build the state proof. It would be an absolute requirement for every web3 client to support this, because sending transactions at the epoch boundary would be impossible without it.

## Rolling ReGenesis

One mitigation would be a “Rolling ReGenesis,” where we only drop state that’s been cold for one *entire* epoch. State would be split into an aged database and a current database.

All EVM reads would cascade, so they attempt to read from the current and then aged database. If it is necessary to read from the aged database, then the value gets copied into the current db.

At every `block_num % EPOCH_LENGTH == 0`:

1. The node deletes the aged database, which was formed one epoch ago.
2. The node moves all current state into an aged database, which becomes read-only.
3. The node creates a new current database.
4. All transactions must now include a witness for any state that is not in the current or aged database.

This should significantly reduce the impact on active contracts and accounts. An account that sends a transaction once every `EPOCH_LENGTH` blocks would not need to attach a witness for a simple payment transaction to an active account. When you interact with a contract, the relevant storage has often been read or written recently, too.

We can pick `EPOCH_LENGTH` such that it’s typically unnecessary to provide a witness at any block. I like 1M, but we should let mainnet backtests guide us. A nice target might be something like 99.9% of transactions not needing any witness.

## Committing to dropped state

Another question is whether to include some commitment to which parts of the state are available, and how often. At one end, we could include a commitment at every header that describes the ranges of keys that are cold. At the other end, we could have it be entirely implicit.

I think this decision is independent from whether we use the original “clean slate” ReGenesis or the Rolling ReGenesis.

**Explicit Approach**

This helps quickly identify if nodes form different beliefs about which state is available. This seems like the safest route, but requires more coding and longer ACD discussions.

Some options:

- Add a new field to the header. For example, add a hash of an SSZ-encoded list of key prefixes.
- Force a custom storage value into a hard-coded account

**Implicit Approach**

Each node tracks its own state availability from block to block. Consensus errors might not cause a chain split immediately. The chain would only split when transactions touch the part of the state that nodes disagree on.

It weakens the verification that fast sync (or beam sync) can do. It’s not possible for these sync approaches to identify whether state is available by asking peers to prove a commitment. These sync methods would have to assume that witnesses are always sufficient (or insufficient, if the transaction fails due to a bad witness).

Further, ReGenesis makes it awkward for fast-syncing/beam-syncing nodes to know when they have finished backfilling all cold state. In the status quo: if a hash in the state trie is missing, that just means that you don’t have it yet. With ReGenesis, you might not have it yet, or it might be a pre-RG value. That means we probably want a new type of response to `GetNodeData` where a peer indicates that it is unavailable state. There is no way to prove the response is true in the implicit approach.

So it seems to be worth paying the technical costs of explicit commitments to state availability.

## Ethereum Name Service

Some storage is read often, but rarely read on-chain. ENS comes to mind. So its registry would typically get forced into cold state, despite being actively used.

This would significantly decrease the benefit of using an ENS name. ENS is supposed to be easier and friendlier to folks new to Ethereum. With a ReGenesis-activated chain, an address publisher has to worry about how to help the noob find the cold state to look up an ENS name. That tips the balance in favor of just using the hex address, I think.

Maybe this is just an acceptable cost of ReGenesis, but it seems worth getting input from the ENS org.

---

**AlexeyAkhunov** (2020-07-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/carver/48/150_2.png) carver:

> Miners need to be able to include a transaction that has an insufficient witness as failed, to collect the gas

That is the current idea. Transactions with insufficient/invalid witnesses are included, but fail to make state transitions. However, the correct parts of the their witnesses are added to the active state

---

**cdetrio** (2020-07-15):

iiuc, say an account wants to send a txn after the first Regenesis (at block #13,000,001), then the block would need to include witness data of the account’s balance just prior to the Regenesis block (at block #13,000,000).

But say an account has been dormant for several generations (periods between Regenesis events, say 1 million blocks), and wants to send a tx at block #17million+. Wouldn’t the block need to have witness data in the form of exclusion proofs for all the intermediate generations: an exclusion proof for the 13th generation (blocks #13m-14m), and exclusion proofs for the 14th, 15th, and 16th?

---

**AlexeyAkhunov** (2020-07-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/cdetrio/48/254_2.png) cdetrio:

> Wouldn’t the block need to have witness data in the form of exclusion proofs for all the intermediate generations: an exclusion proof for the 13th generation (blocks #13m-14m), and exclusion proofs for the 14th, 15th, and 16th?

I have not prototyped it yet, but I think the answer is no. And the reason is that in most cases, the witnesses provided with the transactions, will be partially correct. Which means that their computed root will definitely be incorrect, and a lot of intermediate hashes close to the top. But, as long as the leaves contain correct information, at some point on the path from the root to the leaf, the root of a subtree will be correct. And this will be detected when comparing the witness (recursively from the root) with the current active state. Obviously, any witness would need to be constructed based on the state snapshot which is at least as fresh as the latest ReGenesis event

---

**cdetrio** (2020-07-17):

You’re right, there’s no need for exclusion proofs. I had misunderstood the proposal. I was imagining that each Regenesis event would create a new (empty) state tree, i.e. every Regenesis block would have the null state root, and active accounts would be inserted into this new tree. Kind of like the “sleep + wake” ideas discussed in old threads.

But reading again, the Regenesis events only drop the “implicit state”. There’s no new state tree. And witness proofs are always generated for the state root in the previous block, the same as regular stateless blocks (rather than a “sleep + wake” system, which would need exclusion proofs for the dormant periods).

---

**AlexeyAkhunov** (2020-07-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/cdetrio/48/254_2.png) cdetrio:

> And witness proofs are always generated for the state root in the previous block, the same as regular stateless blocks

this requirement is much more relaxed in ReGenesis. Witness can be generated based on any state root from the latest ReGenesis event until now. Since witnesses are included with the transactions (unlike in Stateless Ethereum, where they are in blocks), we cannot expect them to be up-to-date and replaced every time a new block comes out. But when the system crosses ReGenesis event, some of the transactions may fail because of that

---

**vbuterin** (2020-08-09):

Writing out some concerns with this approach that I mentioned in the discord chat:

### Partial statelessness doesn’t actually give reasonable bounds on active state size unless we implement the same witness-bounding changes needed to enable full statelessness

Currently, the largest witness size that a block can have is if that block accesses the code of as many accounts as possible using code: `(3500 witness bytes + 24000 code bytes) * (12500000 / 800)` ~= 410 MB. If the attacker provides contract addresses as part of the transaction, this becomes a little bit less powerful (`27500 * 12500000 / 1120` ~= 292 MB), but this then allows the attack to be performed using arbitrary already-existing contracts, removing the attacker’s setup costs.

I have published the above calculation many times, always in the context of showing why enabling statelessness requires [radical gas cost changes, binary trees and code merklization](https://ethereum-magicians.org/t/protocol-changes-to-bound-witness-size/3885). But the calculation is also relevant to computing upper bounds on the active state: if one block can add 292 MB to the active state, then 60 blocks can add 17.1 GB, and now we’re already above the size of many people’s RAM (and this doesn’t even include Merkle branches!).

Hence, assuming status quo gas costs, we can’t guarantee that active state will be in RAM unless we reset the active state many times a day (and it has to be a guarantee, because an attacker could first overfill the active state to above 16 GB and then keep attacking [in fact, the exact same attack] to cause lots of disk reads).

Now, let’s assume my favored bag of radical gas cost changes: 2000 gas SLOAD, 2400 gas calls (except self-calls and precompiles), replacing hexary trees with binary, and adding code Merklization, plus adding a charge per chunk of code accessed (say, 1000 gas per chunk). Witness size is now bounded above by 3 gas per byte (with the exception of Merkle tree attacks):

- SLOAD: 2000 gas / 600 byte witness ~= 3.33 gas per byte
- EXT* or CALL: 2500 gas / 800 byte witness ~= 3.12 gas per byte
- Code accesses: 1000 gas / 320 byte witness ~= 3.12 gas per byte

Hence, total witness size is at most 4 MB for a 12.5m gas block. Now, let us re-run the numbers. It now takes ~4000 blocks to get up to 16 GB, meaning that even in a worst case attack scenario, it takes almost a day to get above RAM size; this seems reasonable, especially if the renewing period is variable, so ~12 hours is just a minimum and the average would be much longer.

But what this exercise tells us is that **for both full statelessness and partial-statelessness (regenesis or otherwise), the witness size bounding triad (gas cost changes, binary tree, code merklization) is absolutely essential**. So this is not an argument against regenesis, but it is an argument that we should continue and even further prioritize going full steam ahead on the triad.

(Note also that the triad, including the 4 MB magic number, is future-proof in an important way: witness compression is looking not too far off in the future, with Starkware recently announcing 10000 hashes per second on consumer desktop hardware using their proposed arithmetic hash function. Roughly, a 4 MB witness contains 4M/32 = 125000 hashes, so this witness would take ~12 seconds to generate. Hence, a single consumer desktop suffices to generate witnesses for all blocks in real time even in the worst case, and those proofs would be broadcasted to help clients that don’t want to download 600 kB average case 4 MB worst case per 13 seconds)

### Challenges of handling transactions to inactive accounts

Suppose that there is a transaction which runs code as follows:

```auto
for i in range(1000000): z = z * z * z + i + block.number
w = call(sload(z % 1000000))
sstore(1000001, w)
```

Basically, the transaction does a lot of work, and then based on that work chooses a random address from a list, and calls that address, and stores the output in storage. The question is: what happens when that output may be inactive? There are a few possibilities:

1. The entire transaction is invalid. This is unacceptable because it is a DoS risk
2. The entire transaction reverts but still pays gas.
3. The call reverts.

In case (2) and (3), *whether or not an account is in the active state becomes part of the state*. This means that we need to change or add new data structures to the state tree, so that someone downloading the state from the state root is able to get this information. This is not especially hard, we could just have an active state trie, and clients could represent it in some compact form, but it is extra complexity that would need to be implemented.

So this makes me wonder: why not take the 80/20 we were going for earlier, where miners are still required to store the full state (active and inactive included) and *miners* generate the witnesses for everyone else? It seems like the complexity would go down a lot, as miners can generate the witness for any transaction they receive no matter what it does without fear of DoS risk. Is there a reason why going that last 20% is a high priority?

---

**AlexeyAkhunov** (2020-08-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> if one block can add 292 MB to the active state, then 60 blocks can add 17.1 GB, and now we’re already above the size of many people’s RAM (and this doesn’t even include Merkle branches!).

After the ReGenesis hard-fork, transaction sender will need to pay for the size of the witness, so adding 292 Mb to the active state would cost 4.7 billion gas. So this calculation needs to be adjusted for that.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Basically, the transaction does a lot of work, and then based on that work chooses a random address from a list, and calls that address, and stores the output in storage. The question is: what happens when that output may be inactive?

The transaction does not become invalid, but it consumes all the gas spent up to that point, and all its state changes (except for the deducing ETH to pay for gas) are cancelled. Across all of the execution frames. Anything activated by the tx witness stays in the active state.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> miners generate the witnesses for everyone else? It seems like the complexity would go down a lot, as miners can generate the witness for any transaction they receive no matter what it does without fear of DoS risk

But there is a DoS risk for miners to generate witnesses for all transactions, unless they can charge for the size of witnesses. We had this problem with Stateless Ethereum and block witnesses, and the solution was either repricing of opcodes, or oil/karma, both of which have downsides. That is why asking tx sender to construct and PAY for the witness simplifies the gas accounting for the witnesses

---

**vbuterin** (2020-08-10):

> so adding 292 Mb to the active state would cost 4.7 billion gas

Oh wow, so you’re proposing the full 16 gas per byte? That’s definitely more extreme than my proposal (~3 gas per byte), though it certainly would provide even stronger guarantees (eg. it guarantees a minimum of at least ~3 days before active state reaches 16 GB). It would for example mean that accessing and fully reading a not-yet-read 24 kB contract would require 384k gas, which is much higher than current applications are expecting, though I do see how exempting recently-accessed accounts can mitigate the effect somewhat. I’ll need to think more about the effects of going all the way up to 16 gas/byte for accessing old state… it’s certainly interesting.

It’s also possible to combine the two: target 3 gas per byte for accessing any state, and 16 gas per byte for accessing old state; this way fully stateless clients could enjoy a size witness bound of ~4 MB, and clients that hold on to merkle branches after every regenesis phase could enjoy a stronger witness size bound of ~800 kB.

> But there is a DoS risk for miners to generate witnesses for all transactions, unless they can charge for the size of witnesses.

Of course! This is why the witness size bounding triad (gas cost changes of some form, binary tree, code merklization) is essential. This is true in any proposal (I don’t think there’s any disagreement here?)

> We had this problem with Stateless Ethereum and block witnesses, and the solution was either repricing of opcodes, or oil/karma, both of which have downsides.

But this proposal is de-facto repricing opcodes! I don’t think there’s actually much concrete difference between saying “CALL now costs 3000 gas” and “if you CALL you have to provide a witness, and to cover that witness you have to pay 3000 gas”; both are increasing the gas cost of a call, the difference mainly matters when looking at how this ends up treating sub-calls.

So I don’t see how any of the problems of any other gas repricing scheme actually get avoided. In particular, I think this proposal breaks meta-transactions, as a meta-transaction could try to access stale state and thereby burn the funds of whoever paid for gas to include it.

Also it seems to me that even if we want to charge for the witness per-byte, charging for the witness and requiring the transaction sender to construct the witness are completely orthogonal. You can have a system where the miner generates the witness and the transaction sender gets charged per-byte, and you can have a system where the transaction sender provides the witness and they pay 3000 gas per call. So I feel like the issues of (i) who should hold the state, and (ii) how we charge more gas for state accesses, should be considered separately; a per-witness-byte strategy for (ii) does not imply “tx sender makes witnesses” for (i) and similarly a higher gas cost for (ii) does not imply we can’t force the tx sender to make witnesses for (i).

---

**AlexeyAkhunov** (2020-08-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> But this proposal is de-facto repricing opcodes! I don’t think there’s actually much concrete difference between saying “CALL now costs 3000 gas” and “if you CALL you have to provide a witness, and to cover that witness you have to pay 3000 gas”; both are increasing the gas cost of a call, the difference mainly matters when looking at how this ends up treating sub-calls.

Though I would agree that these things may be equivalent in the end result they are achieving, they are different in what kind of changes to the live Ethereum need to be applied, and how, and in which order. A big part behind ReGenesis design is not about end-result, but also about the execution strategy. We have end-result focused design in Eth2, in Eth1 the operational aspect of “how to get there” is as important. We might be seeing this from very different perspectives though, since this is where experiences with the current system really matter, and not just the properties of the end result.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> You can have a system where the miner generates the witness and the transaction sender gets charged per-byte

I am not sure you can get transaction sender pay for witness that the miner is constructing. This is because the miner’s action always happens AFTER the transaction sender’s action. So you either need to get tx sender to “sign a blank cheque” for the witness they are not even sure will be sufficient, or somehow modify the system to have tx sender’s requiring to sign (and pay) twice, once before the miner’s action, and another time - after the miner’s action - i don’t know how to do that

---

**vbuterin** (2020-08-11):

> So you either need to get tx sender to “sign a blank cheque” for the witness they are not even sure will be sufficient

What’s wrong with this? Transaction senders already set gaslimits based on how many operations of what kind their transaction will include, and we know the theoretical limits for the witness size for a call (~8 kB theoretical max, ~4 kB practical max assuming computational bounds on address grinding, ~1 kB practical max if grinding is impossible eg. many contract storage cases).

---

**AlexeyAkhunov** (2020-08-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What’s wrong with this? Transaction senders already set gaslimits based on how many operations of what kind their transaction will include, and we know the theoretical limits for the witness size for a call (~8 kB theoretical max, ~4 kB practical max assuming computational bounds on address grinding, ~1 kB practical max if grinding is impossible eg. many contract storage cases).

Ok, this comparison implies that there will be a deterministic procedure for generating the transaction witness that the miner must follow. I will think about it, thank you for the idea!


*(7 more replies not shown)*

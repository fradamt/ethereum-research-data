---
source: ethresearch
topic_id: 22331
title: Block-level Access Lists (BALs)
author: Nero_eth
date: "2025-05-13"
category: Execution Layer Research
tags: [scaling]
url: https://ethresear.ch/t/block-level-access-lists-bals/22331
views: 1800
likes: 15
posts_count: 14
---

# Block-level Access Lists (BALs)

# Block-level Access Lists (BALs)

> Many thanks to Francesco, Jochem, Vitalik, Ignacio, Gary, Dankrad, Carl, Ansgar, and Tim for feedback and review.

[![bal_preview](https://ethresear.ch/uploads/default/optimized/3X/a/4/a4bd446262b8310169e42643ac48941f96ff572a_2_432x375.jpeg)bal_preview1024×888 145 KB](https://ethresear.ch/uploads/default/a4bd446262b8310169e42643ac48941f96ff572a)

*TL;DR: Block builders include access lists and state diffs into blocks for validators to validate faster → scale L1!*

One of the key topics in the renewed effort to scale Ethereum’s Layer 1—especially the execution layer—is **[block-level access lists (BALs) - EIP-7928](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7928.md)**.

**BALs** are structured lists that the block builder must include in each block, specifying which storage slots individual transactions will access. If these lists are inaccurate or incomplete, the block becomes invalid. As a result, **Ethereum’s consensus mechanism can enforce strict compliance**, requiring builders to provide correct BALs.

Validators benefit significantly from BALs by accelerating block verification. Knowing exactly which accounts and storage slots will be accessed enables validators to apply simple parallelization strategies for disk reads (IO) and execution (EVM). This can lead to **faster block validation** and open the door to **raising gas limits** in the future.

> Check out this previous post on execution dependencies and Dankrad’s simulations on parallelizing storage reads here.

A critical design goal for BALs is **maintaining compact size** in both average and worst-case scenarios. Bandwidth is already a constraint for nodes and validators, so it’s vital that BALs don’t add unnecessary load to the network. BALs will be put into the block body, with a hash of the BAL stored in the header.

> Currently, Ethereum clients rely on their own optimistic parallelization strategies. These generally perform well on average blocks, but struggle with worst-case scenarios, leading to significant performance differences.

# The design space for BALs

- What to include?

In addition to storage locations (address, storage key), we can also include:

storage values
- balances
- balance diffs

For storage values, we can distinguish between:

- pre-block vs. pre-transaction execution values
- pre- vs. post-transaction execution values

Are we aiming to be hardware-agnostic, or do we want to optimize for certain commonly used hardware specs?

**In the following, we’ll focus on three main variants of BALs: access, execution and state.**

# Access BALs

Access BALs map transactions to `(address, storage key)` tuples.

- Small in size.
- Enable parallel disk reads but are less effective for parallel transaction validation due to potential dependencies.
- Execution time is parallel IO + serial EVM.

For efficiency, a lightweight BAL structure could look like this using SSZ:

```python
# Type aliases
Address = ByteVector(20)
StorageKey = ByteVector(32)
TxIndex = uint16

# Constants; chosen to support a 630m block gas limit
MAX_TXS = 30_000
MAX_SLOTS = 300_000
MAX_ACCOUNTS = 300_000

# Containers
class SlotAccess(Container):
    slot: StorageKey
    tx_indices: List[TxIndex, MAX_TXS]  # Transactions (by index) that access this slot (read or write)

class AccountAccess(Container):
    address: Address
    accesses: List[SlotAccess, MAX_SLOTS]

# Top-level block fields
BlockAccessWrites = List[AccountAccess, MAX_ACCOUNTS]
BlockAccessReads  = List[AccountAccess, MAX_ACCOUNTS]
```

The **outer list** is a deduplicated list of addresses accessed during the block.

- For each address, there’s a list of storage keys accessed.
- For each storage key:

List[TxIndex]: Ordered transaction indices that accessed this key.

For example, the BAL for block number `21_935_797` would look like this:

```python
[
    ('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
        [
            ('0xa63b...c2', [0]),
            ('0x8b3e...a7', [0]),
            ('0xfb19...a8',
                [1, 2, 3, 4, 84, 85, 91]
            ),
            # ... additional entries
        ]
    ),
    # ... additional entries
]
```

# Execution BALs

Execution BALs map transactions to `(address, storage key, value)` tuples and include balance diffs.

- Slightly larger in size due to value inclusion.
- Facilitate parallel disk reads and parallel execution.
- Execution time is parallel IO + parallel EVM.

An efficient structure using SSZ:

```python
# Type aliases
Address = ByteVector(20)
StorageKey = ByteVector(32)
StorageValue = ByteVector(32)
TxIndex = uint16
Nonce = uint64

# Constants; chosen to support a 630m block gas limit
MAX_TXS = 30_000
MAX_SLOTS = 300_000
MAX_ACCOUNTS = 300_000
MAX_CODE_SIZE = 24576  # Maximum contract bytecode size in bytes

# SSZ containers
class PerTxAccess(Container):
    tx_index: TxIndex
    value_after: StorageValue # value in state after the last access within the transaction

class SlotAccess(Container):
    slot: StorageKey
    accesses: List[PerTxAccess, MAX_TXS] # empty for reads

class AccountAccess(Container):
    address: Address
    accesses: List[SlotAccess, MAX_SLOTS]
    code: Union[ByteVector(MAX_CODE_SIZE), None]  # Optional field for contract bytecode

BlockAccessList = List[AccountAccess, MAX_ACCOUNTS]

# Pre-block nonce structures
class AccountNonce(Container):
    address: Address  # account address
    nonce_before: Nonce  # nonce value before block execution

NonceDiffs = List[AccountNonce, MAX_TXS]
```

**The structure is the same as in the access version, with `StorageValue` added to represent the value after the last access by each transaction.**

- Exclude SlotAccess.accesses for reads: empty SlotAccess.accesses indicates a read.

This means that only write operations consist of (StorageKey, List[TxIndex], StorageValue) tuples, significantly reducing the object’s size.

**Instead of post-execution values, we could include pre-execution values for reads and writes for each transaction. Thereby, EVM execution would not have to wait for disk reads. This is a completely separate design, coming with its own trade-offs, reducing execution time to `max(parallel IO, parallel EVM)`.**

> For syncing (c.f. healing phase), having state diffs (thus, the post-tx values) for writes is required for catching up with the chain while updating state. Instead of receiving new state values directly with their proofs, we can heal state using the state diffs inside blocks and verify the correctness of the process by comparing the final derived state root to the head block’s state root received from a light node (h/t dankrad).

For contract deployments, the `code` must contain the runtime bytecode of the newly deployed contract.

The `NonceDiffs` structure MUST record the pre-transaction nonce values for all `CREATE` and `CREATE2` deployer accounts and the deployed contracts in the block.

An example BAL for block `21_935_797` might look like this:

```python
[('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
  [('0xa63b...c2',
    [0],
    '0x...'),
   ('0x8b3e...a7',
    [0],
    '0x...'),
   ('0xfb19...a8',
    [1, 2, 3, 4, 84, 85, 91],
    '0x...'),
   ...
  ]
 )
]
```

---

**Balance diffs** are needed to correctly handle execution that depends on an account’s balance. These diffs include every address touched by a transaction involving value transfers, along with the balance deltas, transaction senders, recipients, and the block’s coinbase.

```python
# Type aliases
Address = ByteVector(20)
TxIndex = uint64
BalanceDelta = ByteVector(12)  # signed, two's complement encoding

# Constants
MAX_TXS = 30_000
MAX_ACCOUNTS = 70_000  # 630m / 9300 (cost call to non-empty acc with value)

# Containers
class BalanceChange(Container):
    tx_index: TxIndex
    delta: BalanceDelta  # signed integer, encoded as 12-byte vector

class AccountBalanceDiff(Container):
    address: Address
    changes: List[BalanceChange, MAX_TXS]

BalanceDiffs = List[AccountBalanceDiff, MAX_ACCOUNTS]
```

- Deduplicated per address.
- Each tuple lists the exact balance change for every relevant transaction.

Example:

```python
[
  (
    '0xdead...beef',
    [
      (0, -1000000000000000000),  # tx 0: sent 1 ETH
      (2, +500000000000000000)    # tx 2: received 0.5 ETH
    ]
  ),
  # ... additional entries
]
```

# State BALs

This structure **fully decouples execution from state**, allowing validators to bypass any disk or trie lookups during execution, relying solely on the data provided in the block. The `pre_accesses` list provides the **initial values** of all accessed slots before the block starts, while `tx_accesses` traces the **per-transaction access** patterns and **post-access values**, enabling fine-grained parallel execution and verification.

- Larger in size
- Execution time is max(parallel IO, parallel EVM).

An efficient SSZ object could look like the following:

```python
# Type aliases
Address = ByteVector(20)
StorageKey = ByteVector(32)
StorageValue = ByteVector(32)
TxIndex = uint16

# Constants
MAX_TXS = 30_000
MAX_SLOTS = 300_000
MAX_ACCOUNTS = 300_000

# Sub-containers
class PerTxAccess(Container):
    tx_index: TxIndex
    value_after: StorageValue

class SlotAccess(Container):
    slot: StorageKey
    accesses: List[PerTxAccess, MAX_TXS]

class AccountAccess(Container):
    address: Address
    accesses: List[SlotAccess, MAX_SLOTS]

class SlotPreValue(Container):
    slot: StorageKey
    value_before: StorageValue

class AccountPreAccess(Container):
    address: Address
    slots: List[SlotPreValue, MAX_SLOTS]

# Unified top-level container
class BlockAccessList(Container):
    pre_accesses: List[AccountPreAccess, MAX_ACCOUNTS]
    tx_accesses: List[AccountAccess, MAX_ACCOUNTS]
```

> The balance and nonce diff remains the same.
> …

### What about excluding the initial read values?

Another variant of State BAL **excludes read values**, and only includes pre- and post-values for writes. In this model, `pre_accesses` and `tx_accesses` only contain storage slots that were written to, along with their corresponding `value_before` (from state) and `value_after` (from the transaction result).

This reduces the size while still enabling full state reconstruction, as write slots define the only persistent changes. Read accesses are implicitly assumed to be resolved via traditional state lookups or cached on the client.

# Worst-Case Sizes

## Access BAL

**The worst-case transaction consumes the entire block gas limit (36 million, as of April 2025) to access as many storage slots inside different contracts as possible by including them in the EIP-2930 access list.**

Thus, `(36_000_000 - 21_000) // 1900` gives us the max number of addresses (20 bytes) + storage keys (32 bytes) reads we can do, resulting in `18_947` storage reads and approximately **0.93 MiB**.

> This is a pessimistic measure. It’s practically infeasible to use the block’s gas exclusively for SLOADs. With a custom contract (see here), I was able to trigger 16,646 SLOADs, not more. See this example transaction on sepolia.

**This is less than the current (and post-Prectra) worst-case block size achievable through calldata.**

> Average BAL size sampled over 1,000 blocks between 21,605,993 and 2,223,0023 was around 57 KiB SSZ-encoded. On average, blocks in that time frame contained around 1,181 storage keys and 202 contracts per block.

## Execution BALs

Including a 32-byte value per write entry doesn’t increase the worst-case BAL size. For reading `18_947` storage loads, it **remains at 0.93 MiB**.

**Worst-case balance diffs occur if a single transaction sends minimal value (1 wei) to multiple addresses:**

- With the 21,000 base cost and 9,300 gas for calls, we get a maximum of 3,868 called addresses in one transaction ((36_000_000-21_000)/9_300). Including the tx.from and tx.to of that transaction + the block’s coinbase, we get 3,871 addresses. With 20-byte addresses and 12-byte balance deltas, we get a balance diff size of 0.12 MiB (12 bytes are enough to represent the total ETH supply).
- Alternatively, using multiple transactions each sending 1 wei to a different account, we can theoretically pack 1,188 transactions into one block. With 3 addresses (callee, tx.from and tx.to) in the balance diff, and 12-byte deltas, we get 0.12 MiB in size.

> A balance diff size sampled over 1,000 blocks (2,160,5993–2,223,0023) would have contained around 182 transactions and 250 addresses with balance deltas on average. This results in an average of 9.6 KiB, SSZ-encoded.

## State BALs

Including another 32 bytes for reads and writes increased the worst-case BAL size to around 1.51 MiB.

# Comparison of different designs

[![Screenshot from 2025-04-14 20-36-18](https://ethresear.ch/uploads/default/optimized/3X/a/f/af66c856b222706bd7ab1dcbbf34b088c78577b3_2_651x500.png)Screenshot from 2025-04-14 20-36-18904×694 102 KB](https://ethresear.ch/uploads/default/af66c856b222706bd7ab1dcbbf34b088c78577b3)

The current design specified in [EIP-7928](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7928.md) adopts the Execution BAL model with **post-tx values**. This variant offers a compelling trade-off: it enables both I/O and EVM parallelism and includes sufficient state diffs for syncing, without the additional bandwidth costs associated with pre-transaction state snapshots.

## References

- Gajinder’s post on block access lists
- ESP Academic Grant 2023: EthStorage/Quarkchain Earlier BAL Submission
- Initial tests and simulations by EthStorage/Quarkchain
- https://www.scs.stanford.edu/24sp-cs244b/projects/Concerto_Transaction_Parallel_EVM.pdf
- https://www.microsoft.com/en-us/research/wp-content/uploads/2021/09/3477132.3483564.pdf
- Speeding up the EVM (part 1) | Flashbots Writings

## Replies

**cskiraly** (2025-05-14):

Hi [@Nero_eth](/u/nero_eth) great writeup on BALs!

Thinking of scaling L1, I was wondering why we are not doing a **Bloom filter over the BAL**. This would serve as a Block-level Not-Acceseed List (BNAL), or more precisely, a subset of the not-accessed list as defined by the Bloom filter, a **Block-level Not-Acceseed Filter (BNAF)**.

We could then fast-forward this compact BNAF over the network, even before sending (and well before delivering) the block, and use it to pipeline and thus speed up block production in the following way:

- a block builder could use the previous block’s BNAF, excluding transactions that are excluded based on the BNAF bloom filter.
- This allows it to build a block even if it doesn not have the state change from the previous block.
- It also guarantees that the block could be valid even if the previous block will not get canonical.

Of course this would break the notion of the “chain” leading to a slightly more complex parallelized structure, with backward edges of depth 2. But the complexity is still limited.

Eventually, we could play with:

- pipelining more by using more BNAFs, allowing more depth in the “chain” links.
- playing with various levels of Bloom compression, as a compromise between speed of fast-forwarding the BNAF, and the amount of addresses excluded from the next block(s).

A simpler version of the above is just to fast-forward the whole BAL, and use that to form the exclusion list, but the BNAF should be much more compact, maybe even fitting in a simple IP packet.

What do you think? Maybe it is something others have already considered, I did not look up the literature …

---

**kladkogex** (2025-05-14):

Hey,

I think it totally makes sense for reads. For writes, an implementation can optimize by batching them into a single write request and committing changes to the DB after executing the block. There’s no need to have a predefined write list.

---

**Nero_eth** (2025-05-15):

Interesting, [@cskiraly](/u/cskiraly)! I’m still wrapping my head around how a Bloom “not-accessed” filter would plug into the pipeline. Because Bloom filters always spit out some false positives, I’m not sure what happens when a builder skips a slot that actually *was* touched—and it feels like the fork-choice tweaks to make that safe might be a whole extra project. So this might need its own EIP and deeper modeling before we can judge the trade-offs. Would love to see a short draft whenever you have one!

---

**Nero_eth** (2025-05-15):

So, the current proposal differentiates between reads and writes. Since it includes post-tx values in the BAL, we don’t need any values for reads at all. No value means it’s a read, entries in the BAL with a value are writes. The post-tx values are at the same time the pre-tx values for other transactions. This means, after having done IO, you have all storage values you need, some from the result of I/O, some from the post-tx values.

> E.g.:
> Tx1 and Tx2  both write to slot A.
>
>
> The BAL would contain the storage location (address, slot A) and the value that Tx1 wrote to A.
> We start executing by doing reads. After that we have the initial value of A and the post-tx value of A. This allows us to parallelize the execution of Tx1 and Tx2

The final structure of the BAL is optimized to be as small as possible. All addresses and storage slots only appear once.

---

**cskiraly** (2025-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Interesting, @cskiraly! I’m still wrapping my head around how a Bloom “not-accessed” filter would plug into the pipeline. Because Bloom filters always spit out some false positives, I’m not sure what happens when a builder skips a slot that actually was touched—and it feels like the fork-choice tweaks to make that safe might be a whole extra project. So this might need its own EIP and deeper modeling before we can judge the trade-offs. Would love to see a short draft whenever you have one!

The trick is that the Bloom is on top of the accessed, so a false positive on the bloom is an “I think it is accessed but it is actually not”. If you then negate this to get a Not Accessed check, you get a filter that drops everything that was accessed, but only some of the not accessed. Anything that passes the filter is guaranteed to be not accessed.

I prepare a draft, then we can discuss more in detail.

---

**jochem-brouwer** (2025-05-17):

One thing which does not work very well with bloom filters is that if the size of the filter stays constant, but the block gas limit rises, the bloom filter loses its efficiency (assuming if you double the block gas limit, you also get double the amount of accesses (which are uniformly distributed - which in practice would not be a good assumption though)).

I however do like the idea of “a” bloom filter on top of the BAL. We could even repurpose the `logsBloom` of the block header for this! One could then send the block header, the transactions, and finally the block access list. (Transactions and the BAL would be part of the “block body”, and thus not the header)

With the bloom filter, how you propose it (if I understand it correctly), we could technically parallelize running ALL transactions at once, and once we access some state, we will check the BNAF. Since this is a negation of the bloom filter over the BAL, it means that if this returns a positive we can be sure that such state is **not** accessed and we can thus continue executing the transaction until we hit a negative, which *could* mean that the state has been accessed by the BAL. (Please correct me if I’m wrong, but I think this is the kind of path you were thinking?). This would likely help execution for the average block. Of course, it is possible to craft blocks which perform very worse here (bloom filter will always return “likely touched access” and we thus have to halt execution until the previous txs have completed, or we have received and decoded the BAL).

---

**jochem-brouwer** (2025-05-17):

Hmm ok, never mind, this path will not work because obviously all accesses queried on the bloom filter of the BAL (when re-executing the block) will obviously always return a positive. However, with this “not accessed” filter one could thus show that if you run a tx on this top of this block, if it only hits state which is not accessed, is thus independent of all accesses in that block. So you could already start including these txs in the new block without having the state of the block you are actually building on ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12) If you would then provide the access list of that tx and compare it against the block access list filter, one could then show that it is indeed an independent tx. (I guess this is beyond the scope of this EIP / idea of BALs but it is something very interesting to keep in mind)

EDIT: ah wait, I think this is exactly what [@cskiraly](/u/cskiraly) meant ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=12) ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=12) Include txs on top of the previous block if you don’t have the state (at the end of) the previous block yet (but have state prior to that block)

---

**Po** (2025-05-20):

What if some users want to submit a transaction that accesses a state entry which was in fact accessed in the previous block (i.e., it’s in BAL), but due to the BNAF-based filtering, this transaction is excluded from the next block? Wouldn’t this mechanism introduce a form of protocol-level censorship, where valid transactions are systematically ignored?

---

**jochem-brouwer** (2025-05-21):

The “rule” to drop txs from the block if it fails due to the BNAF filter would not be included in the consensus (at least that is how I would imagine this). The BNAF filter is there and clients are free to use it (or not). It could thus be used to already start building a new block if you have not executed the block before (but you have the BAL and the BNAF). You can safely do so by running it on top of the previous state and checking if it hits the filter.

---

**cskiraly** (2025-05-22):

Exactly, the primary goal of the BNAF would be to provide a way to speed up and eventually parallelize and distribute build (or in other words build on past state), without the risk of running into conflicts.

Actually, what I wrote about BNAF had two parts:

- one about the fast diffusion of information about state change, which could allow speeding up the timeline for block building.
- the other part is some vague ideas about a kind of “dynamic” sharding and pipelining.

Both aim to reduce slot time (or timelines in general).

But I think the risk of systematic exclusion that you mention is there. We should maybe separate two types of these: 1) where the transaction is actually accessing a large part of the state, and 2) where the transaction is nothing special, it just falls victim of the probabilistic nature of the bloom filter. I think both have solutions, I also have some vage ideas, but I’m far from having all the details of a design here, and happy to brainstorm with anyone interested.

---

**MicahZoltu** (2025-08-05):

I’m late to the party, but I would like to lobby for the inclusion of pre-state in BALs.

With pre-state, you can run a fully validating client (execute/trace every transaction in every block) without needing to store the full state (or even any of it).  You will not be able to validate the state root, but you can validate everything else.

With post-state, you can run a client that stores some/all state but doesn’t do any block execution.

A node may have plenty of CPU available to execute/trace a block, but not enough disk space to store all of state.  This is especially true as state growth outpaces hard drive growth, which is magnified by increasing gas limits.  An example of this might be someone’s personal laptop/desktop computer.

A node also may have a big disk, but little processing power.  An example of this may be a hardened “mobile” device dedicated with keeping the chain up to date for use as a wallet.

I am very skeptical of the long term benefits of parallelization, but I think the long term benefits of various types of light RPC clients is quite high.  Dropping pre-state from BAL does help with bandwidth, which I can appreciate, but it removes our ability to build some useful light clients that enable broader sovereign access to the blockchain.

---

**Nero_eth** (2025-08-07):

I hear you on the light client use case. The concern with including pre-tx values is that it could bloat block sizes and potentially create a new class of worst-case blocks. The current post-tx design was primarily motivated by parallelization, and it stays under the worst-case size from calldata.

You’re right that adding pre-tx state could unlock some extra use cases, but without witnesses it still wouldn’t be enough to fully trust the head, and including witnesses would blow up size 10x. With the current BAL setup, we get a solid trade-off that already enables partial stateless nodes (e.g., low-compute, medium/high-storage devices) that can use zk proofs for validation. Also being able to index balances without tracing is a huge win for RPCs.

Pre-tx values could still be added later, either with witnesses or via zk proofs, but for this EIP, I’d prefer not to expand the scope.

---

**OnticNexus** (2025-10-08):

I like this suggestion in principle, but I’m not sure about how the incentives play out. In the current MEV-Boost pipeline, wouldn’t the relay be the one to broadcast the BNAF, considering that they’re the first to know which payload won? If that’s the idea, then one concern is that relays don’t really have a reason to broadcast the BNAF beyond their own builder set. The builders in their set will be able to get a head start on the next block, but others won’t, which means we don’t currently have the incentives in place for a network-wide early BNAF. Practically, the result may be that handful of already successful builders get an additional advantage over the competition.


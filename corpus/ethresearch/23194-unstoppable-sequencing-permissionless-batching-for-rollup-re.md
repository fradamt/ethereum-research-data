---
source: ethresearch
topic_id: 23194
title: "Unstoppable Sequencing: Permissionless Batching for Rollup Resilience"
author: RogerPodacter
date: "2025-10-13"
category: Layer 2
tags: [based-sequencing, sequencing]
url: https://ethresear.ch/t/unstoppable-sequencing-permissionless-batching-for-rollup-resilience/23194
views: 351
likes: 8
posts_count: 3
---

# Unstoppable Sequencing: Permissionless Batching for Rollup Resilience

*Unstoppable Sequencing was developed in collaboration with Spire, leveraging their expertise in blob sharing. Thanks to [@norswap](/u/norswap), [@donnoh](/u/donnoh), [jesus.eth](http://jesusdoteth), [Ilia Shirobokov](https://x.com/ilia_shirobokov), [Julie](https://x.com/0xbbjubjub?), and the Spire team for feedback.*

## Introduction

Rollup sequencers wield enormous power. They decide which transactions get included, in what order, and when. They are the gatekeepers of L2s. What happens when these gatekeepers fail or censor users?

Typically users rely on “forced inclusion,” a mechanism for creating L2 transactions by creating L1 transactions. However, while forced inclusion preserves an escape hatch, it is not sufficient to support the ongoing operation of a rollup due to the L1 gas costs of submitting transactions individually instead of in batches.

The solution: make batching permissionless and economically viable for anyone. If L1 is live, the rollup keeps functioning at near-normal throughput—even with a failed or malicious sequencer. This is Unstoppable Sequencing.

## Why Forced Inclusion Fails Today

### How Does Forced Inclusion Work?

Taking the OP Stack as an example, this is the process:

1. The user calls the depositTransaction function on the OptimismPortal2 contract and specifies the details of the L2 transaction they want to make.
2. The portal contract emits an event which honest OP Stack nodes know to read, convert into an actual EVM transaction, and insert into an L2 block when the sequencer is down.

The key point is that each L2 transaction requires its own L1 transaction. These L1 transactions cost at least 100k gas units, even in [the simplest case](https://etherscan.io/tx/0xe56f6dd6a2163b22c2dbb9d4c4d8dcb9445387062112792f135a4935049ffcca).

Now consider batched transactions posted by a rollup sequencer. Batching enables the sequencer to fit hundreds or thousands of L2 transactions in a single L1 transaction. For example, in this L1 transaction, [Base posted 384kb worth of rollup transactions](https://etherscan.io/tx/0x1bd38711178544b997a30021cb77051453bd6c9779175e924b5db41bfebe3b1c#blobs). A simple transfer transaction is about 100 bytes, a DEX swap closer to 1kb, meaning the capacity gain from batching is at least 100 to 1.

How much did Base pay in L1 gas for this 100x increase in capacity? The same price as a single forced inclusion transaction, because today blobs are essentially free to post due to lack of congestion!

The price of blobspace will undoubtedly increase with rollup demand, but it will always be far cheaper than calldata or contract interactions as it is the intended vehicle for rollup data availability.

### What if the Sequencer Fails?

When the sequencer is offline, forced inclusion becomes the only option. Without the efficiency gains of batching, transaction inclusion costs increase by orders of magnitude. Users have no choice but to exit.

Forced inclusion can enable a mass exit, but only at great cost. Each user must:

- Pay 100k L1 gas for the forced transaction initiating the withdrawal on the L2
- Pay another 200k+ L1 gas to finalize on the L1.

Costs go up with the number of assets users need to exit and the number of transactions required to initiate the withdrawal (for example settling a loan before withdrawing). Finally L1 gas costs will skyrocket while everyone tries to withdraw simultaneously.

Assuming 250k in L1 gas per user to withdraw, 10M users, 100 gwei gas surge pricing, and a $4k ETH price we have a total cost to exit of:

`250k gas per user * 10M users * 100 gwei gas price / 1e18 * $4k ETH price = $1B USD`

The cost is tremendous and yet the model is still optimistic as it assumes all valuable assets can be exited to the L1. This might be true for bridged assets with existing L1 representations, but for assets issued natively on the rollup it’s not at all clear social consensus will develop around an “equivalent” L1 asset.

Finally, once all the fees have been paid and all user assets are safely on the L1, what then? Users can’t *stay* on the L1, it’s too expensive! This is why they were using a rollup in the first place. But can we expect them to re-deposit into a different rollup that has the same vulnerability after having already gone through the massively value-destroying experience of a mass exit?

The takeaway is clear: for the Ethereum rollup ecosystem to survive, rollups must remove the need for sequencer failure-driven mass exits by enabling the chain to function without a centralized sequencer.

## The Solution: Democratizing Rollup Economics

To enable a rollup to operate without a centralized sequencer we must give ordinary users access to the same economic tools that makes centralized sequencing itself viable.

Sequencers possess three critical advantages that enable rollup economics:

1. Batching: Combining multiple L2 transactions into single L1 submissions. This is the fundamental efficiency gain of rollups.
2. Blob Access: Using blob storage instead of contract event emissions. Blobs are purpose-built for rollup data availability and will always be Ethereum’s most efficient DA vector. However users should have the choice of using calldata should it happen to be cheaper, just as rollup sequencers have today.
3. Economies of Scale: According to Ethereum protocol rules, blobs are all-or-nothing purchases—you can’t buy just 10KB of blob space. Centralized sequencers accumulate enough transactions to use blobs efficiently. Individual users cannot, so we need a sequencing approach that enables users to share blobs and thereby avoid paying for space they aren’t using.

## Introducing Unstoppable Sequencing

Unstoppable Sequencing is a framework for the decentralized batching required to preserve rollup capacity and censorship resistance when the main sequencer misbehaves.

### Terminology

- Sequencer: an entity that builds batches of ordered L2 transactions.
- Batcher: an entity that posts already-built batches of L2 transactions to the L1. The sequencer and batcher can be the same entity but the intended arrangement is for the batcher to be a specialized role that handles blob sharing.
- Rollup node: software that derives rollup state deterministically using L1 history. “Deterministically” means that all honest rollup nodes will derive the same state given the same L1 history.
- Rollup consensus client: software that extracts batches from L1 data and sends lists of transactions and metadata to an execution client to build and execute blocks. Example: op-node
- Rollup execution client: software that executes blocks and stores rollup state. Example: op-geth

Here we are assuming the rollup splits execution and consensus as in the OP Stack and on the L1 itself, but this isn’t essential for the explanation.

### Roles and Permissions

Unstoppable Sequencing does not require the elimination of permissioned / centralized sequencers. Centralized sequencers can provide premium services (high-availability, pre-confirmations, eventually synchronous composability with other rollups) that require guaranteed blockspace and fees.

In the Unstoppable Sequencing model, there are two sequencer roles:

- Priority sequencer: every L1 block has at most one priority sequencer. This sequencer’s batches always go at the start of the L2 block and this sequencer is guaranteed a rollup-configurable percentage of L2 blockspace.
- Permissionless sequencers: everyone else. Their batches go behind the priority sequencer’s batches in the L2 block and their block space isn’t guaranteed—they use all gas not consumed by the priority sequencer.

The Unstoppable Sequencing approach is agnostic to how the priority sequencer is chosen and what percentage of L2 block gas they are guaranteed.

A “pure” based rollup might want no priority sequencer. Another might have a priority sequencer but only guarantee them 50% of the blockspace, putting them on even footing with ordinary users, and so on.

There is no “one size fits all” approach to setting these parameters. Unstoppable Sequencing guarantees maximal resilience *within* the choice of parameters, and, crucially, whatever the choice, Unstoppable Sequencing offers the same level of protection when the priority sequencer is absent.

The role of Batcher is completely permissionless in call cases; anyone can post batches created by either the priority sequencer or permissionless sequencers.

### Batch Format (Scannable Anywhere in L1 Data)

In Unstoppable Sequencing, batches are byte strings that can be embedded *anywhere* in Ethereum calldata or blob payloads and are discovered by scanning each Ethereum L1 transaction individually, without filtering by (for example) a privileged posting address.

**Why so liberal?** Constraints on eligible DA transactions limit blob shareability. For example, if two rollups require their postings to be to different recipients they cannot share blobs. Unstoppable Sequencing aims for maximum compatibility with all batch protocols, taking on the overhead of looking everywhere for batches in order to increase efficiency for users.

Unstoppable batches consist of a 36-byte header followed by RLP-encoded transactions (and a 65-byte signature for priority batches):

```auto
[PROTOCOL_ID][CHAIN_ID][VERSION][ROLE][LENGTH][RLP_TX_LIST][SIG if ROLE=1]
```

**Protocol ID** (22 bytes: `0x756e73746f707061626c652073657175656e63696e67`): The string “unstoppable sequencing” encoded as hex. This identifier enables rollup nodes to detect batches located anywhere in blobs or calldata by scanning for this “magic” string of bytes.

**Chain ID** (8 bytes): Identifies the chain the batch targets.

**Version** (1 byte): Version 1 today.

**Role** (1 byte): Distinguishes batch types. `0` for permissionless, `1` for priority.

**Length** (4 bytes): Specifies how many bytes of RLP transaction data follow.

**RLP_TX_LIST**: The actual transactions, encoded as a standard Ethereum RLP list.

**Signature** (65 bytes, priority only): ECDSA signature covering `[CHAIN_ID][VERSION][ROLE][RLP_TX_LIST]`. This proves the batch came from the priority sequencer.

### Partial Blocks (“Block Fragments”)

Unstoppable Sequencing treats each batch as a *partial* L2 block. Multiple batches in the same L1 block are combined into a single L2 block so:

- Small participants don’t need to fill a whole block alone, and
- We avoid “total-anarchy” wasted work where only one full-block proposer “wins.”

### How Do Fees Work?

Intuitively, each sequencer should get the fees from the transactions in the batch they posted. This is possible for the priority sequencer, but not for permissionless sequencers as the L1 block proposer can always front-run the sequencer with a copy of their own batch.

This arrangement incentivizes L1 block proposers to invest in sequencing the rollup which can provide needed throughput in the case of catastrophic priority sequencer failure. But what is the incentive to post permissionless batches if you’re *not* the L1 proposer?

Even without protocol fees, permissionless sequencers may still be motivated by:

- Side deals with users / prepayment arrangements
- Operating large rollup applications that need their own transactions included
- MEV or other indirect benefits from transaction ordering

A final option and “future feature” for the protocol would be to enable users to specify their preferred sequencer who would be the only one (aside from themselves) able to sequence their transactions and receive the fees.

## Deterministically Deriving L2 State From Batches

Now let’s look at the process end-to-end, starting from the perspective of a permissionless sequencer and ending with the production of a deterministic L2 block.

### Step 1: Batch Creation, Submission, and Blob Sharing

A permissionless sequencer collects user transactions via standard RPC calls (`eth_sendRawTransaction`). When the sequencer has collected enough transactions to post, it:

1. Wraps them in the Unstoppable Sequencing batch format
2. Encodes the batch for blob compatibility using viem’s toBlobs method (handling the BLS field modulus constraint)

At this point, the sequencer is ready to submit a blob transaction containing the transaction batch to the L1. However, if they did so they would be competing for the same six blob slots as giant centrally-sequenced rollups. This is not economically viable, which is why Unstoppable Sequencing was designed with blob sharing in mind.

Because blob sharing requires coordination between multiple sequencers, it naturally makes sense as a separate service.

We developed the blob sharing aspects of this protocol in collaboration with [Spire](https://www.spire.dev/) using their [DA Builder product](https://www.spire.dev/da-builder). We believe their offering is the most mature and will be using it in our Unstoppable Sequencing implementation on Facet Chain. However the overall approach here is provider-agnostic; any compatible aggregator works.

To use a sharing service like Spire, users would take the exact same blob transaction they would otherwise submit to the L1 and send it to Spire’s RPC endpoint instead. Spire then decodes the blob, combines its data with that of other sequencers into a new blob, and posts that to the L1.

Spire even supports Flashbots RPC methods like `eth_sendBundle` so that sequencers can submit batches to Spire as soon as they receive a single user transaction and re-submit a new batch targeting the same L1 block for each new user transaction they receive. This removes the burden of optimal timing from individual sequencers.

Note: if the blob economics are unviable even *with* a blob aggregation service, the sequencer can always post the batch to the L1 as calldata.

### Step 2: Discovery & validation (node scans everything)

For each L1 block, the node iterates over **every L1 transaction** in order and inspects:

1. The tx’s calldata, then
2. Each blob attached to that tx (in ascending blob index).

It scans each byte stream for the Unstoppable `PROTOCOL_ID` and, on match, parses the fixed-length header and validates:

- CHAIN_ID matches the rollup,
- VERSION is supported,
- RLP_TXS decode correctly
- For priority batches (ROLE=1), SIG verifies against a rollup-specific authorized set
- Ensure the sum of the gas limits of all transactions in all priority batches doesn’t exceed the rollup-specific guaranteed gas allocation.

Malformed or mismatched batches are ignored. Valid batches move to the next step.

### Step 3: Aggregation and Ordering

The node collects all valid batches from the L1 block and orders them using the following sort key:

- priority ? 0 : 1
- L1 tx index
- byte offset in calldata
- blob index
- byte offset in blob

That is, priority batches come first and if a transaction has batches in both calldata and blobs, all calldata batches come before blob batches.

Each batch is “unwrapped” into its constituent transactions, preserving their order in the batch and traditional single-tx forced inclusion transactions are appended. In sum:

1. All priority batch transactions
2. All permissionless batch transactions
3. Deposits / traditional forced transactions

The result is a deterministic ordered list of L2 transactions, but the rollup execution client might not be able to construct a L2 block out of this list because some transactions might be invalid.

In Ethereum, transaction “failures” fall into two categories:

1. Failed Transactions (Block-Valid): When a contract function reverts or a transaction runs out of gas the transaction can still be included in a valid block.
2. Invalid Transactions (Block-Invalid): Certain transaction errors invalidate the entire block, causing execution clients to reject it. For example:

Insufficient account funds to cover gas costs
3. Invalid nonce values
4. Contract deployments exceeding size limits

In traditional single-party block creation, the block producer can remove all invalid transactions before submission. However, this approach isn’t feasible when combining batches from multiple parties in an Unstoppable Sequencing system.

### Step 4: Execution and Filtering

The solution is to “filter out” block-invalidating transactions from the ordered list of L2 transactions the node created in the previous step.

However, identifying invalid transactions is not something that can be done “statically” in a rollup consensus client because a transaction’s validity can depend on the results of executing the previous transactions in the block.

Because of this, Unstoppable Sequencing requires execution client modifications to enable this filtering. The process works like this:

1. The consensus client sends the transactions to the execution client in a normal engine_forkchoiceUpdated call.
2. The execution client begins building an L2 block using these transactions, executing one at a time, in order.
3. When the execution client hits an invalid transaction, instead of halting the process with an error, it skips the transaction and moves to the next transaction in the list.

## Limitations and Trade-offs

### Permissionless Sequencers Face Uncertainty

Priority sequencers get predictable ordering and guaranteed gas allocation. Permissionless sequencers don’t know their final execution order. If the L2 block is full by the time a permissionless batch’s transactions attempt to buy gas they will be filtered out.

An attacker could exploit this mechanic by submitting many batches ahead of a certain permissionless sequencer in an attempt to exclude them from the block. However sustained spam will create significant costs for an attacker as the L2’s block base fee increases in response.

When some or all of a batch’s transactions do not land in an L2 block, these transactions are lost from the perspective of the protocol. That is, if the sequencer wants to attempt including the transactions in a different L2 block they will have to post the batch again to the L1 in a new transaction.

A more cost-effective but more complicated “future feature” would be for the rollup node to maintain a “mempool” of filtered transactions and automatically include them without resubmission on future L2 blocks.

### Pre-confirmations and Synchronous Composability

Certain advanced features require the ability to reliably simulate transaction outcomes:

- Pre-confirmations: Users want guarantees about transaction execution before L1 inclusion
- Synchronous composability: Cross-chain calls need deterministic simulation

These services can only be reliably offered by whoever posts the first batch—the priority sequencer when active, or the L1 proposer if the priority sequencer is absent.

This creates a natural division of labor: priority sequencers provide premium services and guarantees, while permissionless batching ensures the chain remains censorship-resistant and operational under any conditions.

### What About Spam?

A permissionless system invites spam. An attacker could post thousands of invalid transactions across multiple blobs, forcing nodes to process garbage. Can Unstoppable Sequencing handle this?

The current limit of 6 blobs per block means at most ~7,500 spam transactions per 12-second block which is tractable for today’s hardware.

As blobspace grows this could become a challenge, but solving this challenge is the price of permissionlessness and resilience.

## Conclusion

L2s are built on batching. Traditional forced inclusion breaks this model by reverting to individual transactions, making it impossible to maintain normal operations during sequencer failure.

Unstoppable Sequencing solves this by making batching permissionless—anyone can create and post batches, embedded anywhere in L1 data, sharing costs through blob sharing. This approach entails additional complexity, but it ensures L2s can survive censorship, failures, and attacks. As long as someone can post a batch somewhere on L1, the chain keeps running.

## Replies

**thegaram33** (2025-10-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/rogerpodacter/48/14574_2.png) RogerPodacter:

> For each L1 block, the node iterates over every L1 transaction in order and inspects:
>
>
> The tx’s calldata, then
> Each blob attached to that tx (in ascending blob index).

Doesn’t this make it very costly to run L2 nodes? Scanning through all data is expensive, and it will only get worse as L1 keeps increasing its execution throughput (gas limit) and data throughput (blob count). This is also relevant for validity/fraud proofs that might need to run the same process as L2 follower nodes.

---

**RogerPodacter** (2025-10-15):

Good question!

I think the heavy part of running an L2 node is (and will remain) executing the block and storing state. Scanning L1 data for batches and filtering invalid txs are minimal by comparison for nodes and provers.

Even at 64 blobs/slot we only have 64 × 128 KB = 8 MB every 12s = 0.7 MB/s. Even adding calldata that’s still low single-digit MB/s. A modern machine should be able to scan 100s of megabytes per second. Filtering invalid txs is also cheap.

But even if node and prover costs were significant, apps and users would be happy to pay them to avoid collectively losing billions in a mass exit! Perhaps the concept could be modified in some way such that the requirement to iterate over every L1 tx came into play only when the sequencer was misbehaving. I’ll think about it!


---
source: ethresearch
topic_id: 21624
title: Blob Aggregation - Step Towards More Efficient Blobs
author: kustrun
date: "2025-01-29"
category: Layer 2
tags: []
url: https://ethresear.ch/t/blob-aggregation-step-towards-more-efficient-blobs/21624
views: 1665
likes: 31
posts_count: 10
---

# Blob Aggregation - Step Towards More Efficient Blobs

# Blob Aggregation - Step Towards More Efficient Blobs

*This research was conducted in collaboration with [@artificialquant](https://x.com/artificialquant), [@projectHodl](https://x.com/projectHodl) and [@Alpinex_](https://x.com/Alpinex_).*

**TL;DR:**

> Problem: Blob space is limited and underutilized.
> Solution: Combine multiple rollups’ blobs into one, effectively sharing the blob space.

## Problem

New rollups are created every day, but not all are as widely used as Arbitrum, Base, and Optimism. Through data availability (DA), rollups make transaction data available to all network participants so they can independently verify it. The data is posted to a DA layer, such as Ethereum (or other DA chains, e.g. Celestia), either using calldata (costly) or blobs (cheaper). These rollups compete for a limited 128KB blob space (6 blobs per block now, increasing to 9 after the Pectra upgrade in March 2025). As demand for blob space grows, fees can rise exponentially.

Since number of blobs is limited, and each blob is paid in full, regardless of how much it is filled, it leads to a situation where smaller rollups (with empty blobs) pay the same as bigger rollups (with full blobs) for each blob tx. Consequently, the limited DA space is wasted and fees rise for all due to more blobs being included.

Following the [@hyeonleee](/u/hyeonleee) research [Potential impact of blob sharing for rollups](https://ethresear.ch/t/potential-impact-of-blob-sharing-for-rollups/20619), we see that blob under utilization is not only an issue for smaller rollups but also for larger ones (though they are less affected) through increased blob fees.

[![rollup-blob-utilization](https://ethresear.ch/uploads/default/optimized/3X/7/d/7d5b0c6634e756ba257f03a210647b2817c599ff_2_341x500.png)rollup-blob-utilization552×808 68.1 KB](https://ethresear.ch/uploads/default/7d5b0c6634e756ba257f03a210647b2817c599ff)

## Solution

We propose to expand the block-building process with “blob building” support by combining multiple rollups’ blobs into one. This would allow rollups to share blob space, lowering their costs, improving blob efficiency, reducing network congestion, and making blob space more affordable for all.

The proposed solution builds on top of existing infrastructure and concepts such as MEV-boost and Flashbots bundles. It’s meant to be permissionless so anyone can start providing blob aggregation services. Safety against blob manipulation is ensured via cryptography.

## Technical Details

The specs of proposed implementation is stack-agnostic and can be used even for non-rollup blob data.

We also introduce some new terminology:

- Blob shard: signed blob which is included in aggregated blob.
- Aggregated blob: group of blob shards, prefixed by a header.
- Blob Aggregator: service provider that collects blob shards, groups them into Aggregated blobs, and posts them via flashbots bundles.
- Shared Blob Registry: contract on the ETH mainnet to which the blob txs are posted. It contains blob shard validation logic and fee collection mechanism.

### General flow

[![blob-sharing-flow](https://ethresear.ch/uploads/default/optimized/3X/7/6/767f84149744f3ff320111b192e25d9fbcf700b4_2_690x328.jpeg)blob-sharing-flow2899×1379 150 KB](https://ethresear.ch/uploads/default/767f84149744f3ff320111b192e25d9fbcf700b4)

1. Rollup generates blob shard and sends it to Blob Aggregator RPC.
2. Blob Aggregator connects to multiple Blob Aggregator RPC streams to receive blob shards.
3. Blob Aggregator combines blob shards into a single blob and sends it as a blob transaction that interacts with the Shared Blob Registry on the execution layer.
4. Shared Blob Registry contract verifies blob shards, calculates fees, and rewards Blob Aggregator.
5. Block builder includes the blob in the next L1 block.

### Blob Shards

Each blob shard has a specific structure. The actual blob data is prefixed with a header before being included in the aggregated blob. This is done by the aggregator.

```auto
Chain ID
Signature (v, r, s)
Blob Data Length
    |
    |
    |   Blob Data
    |
    |
```

The header contains:

- Chain ID: blob source chain
- Signature: used to derive blob sender. Together with Chain ID it represents a tuple to uniquely identify to whom the blob shard belongs to.
- Blob Data Length: the number of blob data bytes in this shard.

### Blob Aggregator RPC

Similar to how `eth_sendBundle` is used by MEV searchers to send one or more transactions as a bundle, we propose extending this concept to blobs.

By using `eth_sendBlob`, rollups can send their rollup blobs to the aggregator RPC, which will try to combine them into a single blob and post it to L1. The ordering of the blobs is determined similarly to transactions – by gas price per blob byte, and in cases of equal gas prices, by the time of submission.

The structure of the blob bundle request is (encoded in JSON):

```auto
Blob Shard: {
    Chain ID
    Gas Price Per Byte
    Block Deadline
    Nonce
    Blob Data Hash
    Blob Data Length
}
Signature
Blob Data
```

The Blob Shard struct provides metadata for a given blob shard, allowing it to be uniquely identified, preventing double posting, and calculating fees based on the per-shard utilization of available blob space. The proposed structure does not restrict or tie users to a specific blob data layout within their shards. This makes it possible for users to optimize their blob data structure for their specific use cases.

The **Signature** field ties a blob shard to a specific user, ensuring the request has not been tampered with. It’s also used as an on-chain authentication mechanism to charge fees for the blob and making sure the aggregator takes no more than the amount of fees paid by the blob shard.

**Block Deadline** serves a similar purpose as the target block parameter in flashbots bundles. This ensures that a shard can be included up to the deadline block. Shards included in blobs that land later than the block deadline are invalid. This makes the blob shard inclusion more predictable and simplifies fallback mechanisms of e.g. rollup batches where they can then post the blob tx themselves.

### Blob Aggregator

Blob Aggregator is responsible for gathering blob shards from different users, combining them into a single blob, and submitting it to DA layer to the Blob Shard Registry, preferably in a flashbots bundle that reverts if the TX fails. The aggregator is a permissionless entity that anyone can run.

They are incentivized to run their service by taking a small fee on the realized blob cost savings of each shard. Thus, their goal is to fill the blob with as much data as possible.

The aggregated blob layout contains a blob header, followed by a blob body which includes the shards. The layout of the body can vary across aggregated blob versions (stored in header), and can even be additionally compressed.

The header additionally contains a lookup table to speed up processing by the shard senders, with the following layout: chain ID → shard sender → [shard1 idx, shard2 idx, …]. This makes it possible to jump straight to the start of blob shard data of specific shard sender, without having to process bytes one by one. The lookup table could potentially be moved from the blob header to Blob Shard Registry contract calldata or even emitted via events, but that’s TBD.

Full aggregated blob structure:

```auto
Aggregation Version
Blob Compression
Lookup Table
    |   Blob Shard 1
    |   Blob Shard 2
    |   Blob Shard 3
    |   ...
    |   Blob Shard N
```

Once the blob is aggregated, the aggregator prepares the blob tx which calls the `recordSharedBlob()` function on the `SharedBlobRegistry` contract to register the blob and correctly collect fees and rewards.

### Shared Blob Registry

Shared Blob Registry is a contract responsible for verifying blob shards and compensating the blob aggregator for their service.

We propose the following structure for the Shared Blob Registry contract:

```solidity
/**
 *  @title Shared Blob Registry
 *  @notice Manages storage, verification, and correct handling of blob shards used in a given blob.
 *          Guarantees correct fee payments by blob posters and fair rewards for blob shard aggregators.
 */
interface SharedBlobRegistry {

    /**
    *  @notice Blob shard struct, storing the blob metadata information.
    *
    *  @param chainId ID of the chain that the shard belongs to.
    *  @param gasPricePerByte Expected gas price per used byte for the shard. Used to calculate fees based on the utilized blob space.
    *  @param blockDeadline Block number up to which the shard remains valid.
    *  @param nonce Nonce of the (blobPoster, shard) pair, used to prevent replay attacks.
    *  @param dataHash Hash of the shard data.
    *  @param dataLength Length of the shard data.
    */
    struct BlobShard {
        uint256 chainId;
        uint256 gasPricePerByte;
        uint256 blockDeadline;
        uint256 nonce;
        bytes32 dataHash;
        uint256 dataLength;
    }

    /**
     *  @notice Deposit collateral to cover blob fees.
     */
    function depositFeeCollateral(uint256 amount) external;

    /**
     *  @notice Withdraw collateral to cover blob fees.
     *
     *  @dev If @param amount > balance, the full balance is withdrawn.
     */
    function withdrawFeeCollateral(uint256 amount) external;

    /**
    *   @notice Record a shared blob composed of multiple shards.
    *
    *   @param shards Blob shards to be recorded.
    *   @param signatures Signatures verifying the blob shards.
    *
    *  @dev This function performs the following steps:
    *       1. Verify the signatures for the BlobShards and identify the blob poster address.
    *       2. Calculate the space utilization ratio for each rollup.
    *       3. Determine the unused blob space and charge rollups accordingly, including execution transaction base gas fees.
    *       4. Calculate savings for each rollup.
    *       5. Collect fees, distribute portion of savings, and persist the blob shards.
    *
    *  @dev Shard nonce should be used only once. Must be incrementally consumed.
    */
    function recordSharedBlob(BlobShard[] memory shards, bytes[] memory signatures) external;

    /**
     *  @notice Validate a blob shard by verifying its signature, identifying the blob poster address, and ensuring sufficient collateral to cover fees.
     *
     *  @param shard Bob shard to validate.
     *  @param signature Signature verifying the blob shard.
     *
     *  @return isValid True if the shard is valid; otherwise, false.
     *  @return blobPosterAddress The blob poster address responsible for paying the shard fees.
     *
     * @dev Use tryRecover from @openzeppelin/contracts/utils/cryptography/ECDSA.sol because it has additional security checks.
     */
    function verifyBlobShard(BlobShard memory shard, bytes memory signature) external view returns (bool, address);

    /**
    *   @notice Get the blob shards for a given block number and chain ID.
    */
    function getBlobShards(uint256 blockNumber, uint256 chainId) external view returns (BlobShard[] memory);

    /**
    *   @notice Get the next nonce for a given blobPoster and chain ID.
    */
    function nextNonce(address blobPoster, uint256 chainId) external view returns (uint256);

}
```

### Advantages

- Cost Savings: Users can share blob space, lowering costs and making it more affordable for everyone.
- Improved Efficiency: Blob space is utilized more effectively, reducing network overhead.
- Faster Finality: Rollups can post blobs more frequently, shortening the time to finality.

### Open Questions

- Incentives: Should each rollups decide the percentage of savings to share with the Blob Aggregator? Or should the Blob Aggregator set the service fee? Alternatively, should the fee be determined by the Shared Blob Registry contract? The best approach is still unclear, as each option has its own advantages and disadvantages.
- Blob Shard Collision: What if blob A contains blob shards 1, 2, 3, and blob B contains blob shards 2, 4, 5, and blob A is successfully posted on-chain? Should blob B still be submitted on-chain, or should it be discarded? Could this cause indefinite delays in blob shard submission since blob shard 2 also impacts blob shards 4 and 5?
- Potential Exploit: Currently, there is no guarantee that the Blob Aggregator actually includes the blob shard in the blob, as the execution client cannot read detailed data about blob contents. How can we ensure that the Blob Aggregator is honest and does not submit empty blobs while still collecting rewards? One possible solution is to rely on the Blob Aggregator’s reputation and incentives, such as future blob aggregation rewards, to discourage such behavior. Another alternative is to use restaking mechanisms. A third option would be to implement Blob Shard support directly into Ethereum, potentially as a new transaction type.

## Conclusion

The proposed Blob Sharing concept aims to enhance rollup efficiency by allowing them to share blob space. This approach is expected to lower costs for rollups, improve blob space utilization, and make it more affordable. It also provides an opportunity for Blob Aggregators to experiment with blob shard composition and prepare to evolve into Based Sequencers.

## Other Resources

- Spire Labs: Shared Blob Compression
- Suhyeon - Tokamak Network: Potential impact of blob sharing for rollups

## Feedback Invitation

This proposal is meant to gather feedback from other community members before diving into development. We invite everyone to share their thoughts, suggestions, and potential concerns to refine and improve this concept.

## Replies

**irfanshaik11** (2025-01-30):

Very interesting article! It seems to me this problem arises partly because the blob sizes on ethereum are fixed. Will this be necessary if variable/smaller length blobs are introduced?

Is it preferable to have blob batching or smaller / variable blob lengths both from the POV of the rollup and the L1?

---

**kustrun** (2025-01-30):

I really appreciate you taking the time to read the article and being the first to reply - your engagement means a lot!

Right now, the blob size is fixed at approximately 128 KB and can hold arbitrary data. Since users pay for the entire blob, any unused space (when less than 128 KB of data is provided) is simply filled with zeros. This means that regardless of how much space is actually utilized, the cost remains the same.

Introducing variable-length blobs could be quite challenging because it would alter the static structure we currently have. Blobs are designed with future support for danksharding in mind, and it’s not yet clear to me whether making them variable in size would conflict with that design. If you’re interested in diving deeper into how blobs work, I highly recommend checking out [Blobspace 101](https://domothy.com/blobspace/).

Smaller blobs could be introduced, but finding a universally suitable size for all rollups is difficult. Instead of thinking about changing blob sizes, it might be more helpful to consider blobs as a complete whole - just like a block encapsulates transactions, a blob encapsulates blob shards. Similar to how block-building works today, we’ll likely see “blob-building” emerge in the future.

From a rollup’s perspective, blob aggregation enables faster finality for their batches. Instead of waiting to collect L2 blocks, batch them, and post blobs every few minutes (for high-usage rollups) or every few hours (for less active rollups), they could submit L2 block data as soon as a new block is sequenced. This is particularly important for services that rely on L1 finality, such as exchange deposits.

Additionally, rollups could eliminate the need for extra software that they currently use to batch transactions efficiently into a full blob. By removing this dependency, the process could become more streamlined and efficient.

---

**CPerezz** (2025-01-31):

Hey that’s a nice idea!!

I’m wondering a couple things!

- It would be nice to also include here a method to allow serializing/retrieval of shards of the blob. To reduce the network burden when DA access is needed. Ie. We don’t need to serialize the whole blob just to access a shard that represents 5% of it’s total space. I think it would make the proposal more appealing. Does that make sense?
- What’s the exact motivation for blob aggregators? Utilization? Or profit?
- I say that because we can easily fall into the case where it’s always the case that rollups like Base end up with ~99% utilization. Thus making the other blob-proposals always worse from MEV perspective. Same the other way arround. If the goal is to fit in as many shards as possible, then massive Blob-space consumers like Base will have a hard time getting in. What’s your view?
- As for the potential exploit you mentioned, can’t you solve this with some system like Polygon’s ZKEVM forced txs? Where they prevent censorship by having a mechanism that forces the sequencer to include txs in a block no matter what. And it’s publicly auditable that this is the case (reputation otherwise get’s impacted).

Thanks for the interesting post!

---

**kustrun** (2025-01-31):

Thank you, [@CPerezz](/u/cperezz), for your thoughtful questions and appreciation! ![:raised_hands:](https://ethresear.ch/images/emoji/facebook_messenger/raised_hands.png?v=12)

- I completely agree - reading the entire blob just to check whether a specific blob shard is included is inefficient. Fortunately, some functionalities in the proposal already aim to optimize this process, even though they’re not explicitly written:

When recording a shared blob in the SC, the idea is to store the (L1_block_number, chain_id) pair in storage. This allows the chain operator to quickly verify whether their blob shard was included in a specific L1 block before retrieving and serializing the actual blob.
- Alternatively, we could rely on transaction logs to signal this. Each blob shard registration could emit an event indicating its inclusion.
- Once inclusion is confirmed, we can further speed up serialization using the proposed Lookup Table in the aggregated blob’s header.
- The motivation for blob aggregators depends on their role in the system. If they operate independently, their primary incentive will likely be profit. However, if independent blob aggregators don’t emerge, smaller rollups may collaborate to run one collectively, reducing individual costs for posting blobs. As a community, our goal is to achieve near-perfect blob utilization, which opens up new possibilities for applications we might not even anticipate today.
- Larger rollups are already optimizing blob utilization, as shown in Table 1. They achieve this by running batching software, which ensures efficient use of blob space - though only for their own shards. However, this batching process introduces delays before posting a full blob, slowing down L1 finalization. By moving to a model where smaller blob shards are posted more frequently, rollups can avoid running their own batching service and achieve faster L1 finality.
 Additionally, blob capacity will only increase - currently, we have 6 blobs, this will expand to 9 in March, and even more in the future. So, there’s no concern that a single rollup will dominate blob space or struggle to get included.
- A key challenge is that smart contracts on the execution layer cannot read blob contents - they can only access blobhash and blobk.blobbasefee. This means a malicious blob aggregator could technically submit an empty blob while providing valid blob shard metadata in SharedBlobRegistry.recordSharedBlob() to claim rewards.
 Since we can’t directly verify blob contents, we may need to rely on a reputation system. If an aggregator acts maliciously, they will lose trust and stop receiving blob shards, cutting off their payments. It’s a similar trust assumption to block builders today - while no system prevents them from sandwiching bundles, they refrain from doing so to maintain credibility.
 So, there’s no risk of a transaction being excluded - instead, the real concern is whether an included transaction could be malicious.

---

**hyeonleee** (2025-02-08):

Nice proposal, and thanks for referring to my previous post.

I relate to your open questions. When I was considering blob sharing, a critical open question was **how to calculate the blob sharing fee**.

Let’s assume there’s a specific algorithm to calculate the fee based on data size (which aligns with the first open question in your post). Even with such an algorithm, two key challenges arise before implementing a blob-sharing system:

1. Trust
Even if we establish a fee calculation method, we can’t fully trust the length information in calldata (as raised in your last open question). How can we ensure the blob sharing fee is calculated trustfully on smart contracts? If blob metadata in calldata is unreliable, should we even rely on calldata for posting metadata? Some rollups, for example, avoid using calldata altogether when posting blobs.
2. Efficiency
Calculating the blob sharing fee itself can be costly, which contradicts the goal of reducing gas costs. A potential optimization could be to perform on-chain fee calculations only when a participant’s deposit is nearly insufficient to share blob space—similar to liquidation in financial products.

---

**kustrun** (2025-02-09):

Thank you! Your post really helped us recognize that our idea has direct, practical implications for the current blob market. ![:rocket:](https://ethresear.ch/images/emoji/facebook_messenger/rocket.png?v=12)

I can definitely relate to your critical question about how to price—and more importantly, how to **permissionlessly** collect and distribute blob-sharing fees. ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12) I’ve been thinking a lot about the latter over the past few days, especially since the blob aggregator is an independent entity within the system, not necessarily tied to any blob-sharing consumers.

As you pointed out, **trust** in the blob aggregator’s honesty is a major challenge. If we take this to the extreme and assume the aggregator collects no fees (i.e., all fees are set to zero), then the issue disappears entirely—rollups themselves would need to coordinate, fund, and operate a common blob aggregator. In that case, they could simply use a `SharedBlobRegistry` contract to post metadata about blobs, making it easier for verifying L2 nodes to reprocess them.

But since that approach limits general blob sharing, the fee/incentive mechanism was introduced. Based on discussions I’ve had recently, we should rethink this fee structure—not as a cost-saving reward, but rather as an *optional fee* [1] from users (since not everyone will necessarily pay it). Taking this further, we could split the fee into two parts—similar to the two types of on-chain fees:

- Base fee – A minimal fee to include a blob shard in the shared blob, covering execution and blob posting costs.
- Tip fee – An extra incentive to speed up inclusion.

With this setup, the smart contract could collect fees directly, eliminating additional gas costs for fee calculation. This could help reduce gas costs, but **smart contract efficiency** remains a valid concern—an overly complex contract could wipe out the benefits of blob sharing. ![:warning:](https://ethresear.ch/images/emoji/facebook_messenger/warning.png?v=12)

The only remaining check would be ensuring that the blob aggregator is eligible for rewards—which is still the most crucial part of the system. ![:key:](https://ethresear.ch/images/emoji/facebook_messenger/key.png?v=12) Without this, **true permissionless** blob sharing wouldn’t be possible. Posting the entire blob as calldata would likely be too costly, so we need to explore mathematical approaches to ensure the blob aggregator can collect fees **only if** the shared blob contains valid blob shard data. Partial KZG proof could potentially help here ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12), but I need to refresh my math knowledge before I can confidently support this claim.

Could you elaborate on your proposal regarding fee calculation only when a threshold is reached? To my understanding, even if fees are calculated occasionally, accounting would still need to be executed whenever a new shared blob is posted on-chain. Would the “liquidation” process then simply distribute the earned fees to participants?

*[1] An optional fee based on the participant’s role in the system. If I’m a rollup and also operate my own blob aggregator, there’s no need to waste gas on an extra hop for fee payment and collection on my own blobs.*

---

**hyeonleee** (2025-03-01):

[@kustrun](/u/kustrun)

I consider three major components (or issues) for blob sharing:

- Blob sharing aggregator
- Blob sharing pricing algorithm: How to decide price of blob sharing
 → I think pricing can be processed straightforwardly like pay-per-space. In this paper, a Nash bargaining solution was proposed. In a short time, it seems not realistic that efficient negotiations involve multiple roll-ups and the accurate derivation of the negotiation strategy.
- Blob sharing pricing implementation: How to pay the price decided by the pricing algorithm

Your question is about the 3rd part. The solution is motivated by the optimistic mechanism in rollups. In the smart contract, we can calculate the price with proof but this is costly. Therefore, we perform price calculations only if there’s a dispute. First, we need deposits from participating rollups. And then, in a general case, a committee member or rollup can calculate a price using their deposit. Or, one entity can liquidate all the deposit of one rollup if the rollup used the blob sharing cost as much as its deposit.

This price calculation is proposed without any proof and has a long enough challenge time (e.g. 7 days). And then, if there’s a dispute, finally the dispute can be solved by proposing the signatures or data in the previously shared blobs. There can be an efficient way to construct this dispute game but I don’t have any concrete one in my mind. In this way, we can avoid most of costs for pricing.

---

**kustrun** (2025-03-03):

Thank you for explaining more! ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=12)

Re blob sharing pricing algorithm: I think a pay-per-space pricing idea is good enough to start with. It’s simple and lets us test how the community likes the blob aggregation solution.

Yes, my question was about how to set up the Blob Sharing Pricing. I’m looking at different ways to do implement this, and I like your suggestion because it avoids running complicated smart contract pricing every time we call `SharedBlobRegistry.recordSharedBlob()`. That helps keep gas costs low, which is great! But for this to work well, we’ll need a neutral committee to handle any disputes. To make that happen, something like AVS might be needed, though it could raise costs a bit. ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12)

---

**kustrun** (2025-03-13):

Following our research on how to incentivize the blob aggregators and distribute their rewards, we built a simple blob aggregation service to see how aggregation works in practice. If you’re interested, you can check it out at https://github.com/Blobsy-xyz/blobsy-aggregator - the alpha version is running on the Sepolia testnet too!

Blobsy - https://blobsy.xyz, a visualization tool specialized in analyzing aggregated blobs, is now also open-source: https://github.com/Blobsy-xyz/blobsy-web.

We’d really love to get your feedback. Any developers interested in developing this services further, or any rollup wanting to integrate, feel free to reach out. ![:pray:](https://ethresear.ch/images/emoji/facebook_messenger/pray.png?v=12)


---
source: magicians
topic_id: 22927
title: "New ERC: Cross-chain broadcaster"
author: yahgwai
date: "2025-02-20"
category: ERCs
tags: [erc, interop, cross-chain, standards-adoption]
url: https://ethereum-magicians.org/t/new-erc-cross-chain-broadcaster/22927
views: 401
likes: 11
posts_count: 4
---

# New ERC: Cross-chain broadcaster

# New ERC: Crosschain Broadcaster

## Abstract

This ERC defines a standardized protocol for cross-rollup message broadcasting and reception via storage proofs. Users can broadcast messages on a source chain, which can then be read by many other chains, as long as those chains share a common ancestor chain with the source chain. This smart contract standard enables trustless message passing across rollups hosted on different rollup architecture stacks.

---

## Motivation

The Ethereum ecosystem is experiencing a rapid growth in the number of rollup chains. As the number of chains grows, the experience becomes more fragmented for users, creating a need for trustless “interop” between rollup chains. These rollup chains, hosted on different rollup stacks, have heterogenous properties, and as yet there does not exist a simple, trustless, unified mechanism for sending messages between these diverse chains.

Many classes of applications could benefit from a unified system for broadcasting messages across chains. Some examples include intent-based protocols, governance of multichain apps, multichain oracles and more.

---

## Specification

Check out the full specification on Github: https://github.com/ethereum/ERCs/pull/897

A work-in-progress reference implementation is also available here; if there is sufficient interest from the community, a full implementation can be built out: [broadcast-erc/contracts/reference-impl at main · OffchainLabs/broadcast-erc · GitHub](https://github.com/OffchainLabs/broadcast-erc/tree/main/contracts/reference-impl)

Please participate in the discussion here to help us evaluate and iterate the Crosschain Broadcaster!

---

## More Resources

[Introducing the Crosschain Broadcaster](https://medium.com/offchainlabs/introducing-the-crosschain-broadcaster-920d99eb70a9) - blog post with high level overview of the standard

[FAQs for the Crosschain Broadcaster](https://arbitrum.notion.site/Crosschain-Broadcaster-FAQs-19e01a3f59f880bf8ae7c94663591ef9) - common questions from the community thus far

## Replies

**zaryab2000** (2025-04-22):

Super interesting approach for cross-chain verification.

The trustless way of proving messages using **storage proofs** is what caught my attention. ( *no centralized relayers, oracles, etc* )

I have spent some time looking into the cross-chain-broadcaster contracts. While I believe currently it is at nascent stages, there are a couple of questions I have in mind.

Dropping them below:

1. Regarding: SSTORE in broadcastMessage() function

Currently

- the message and msg.sender together form the slot.
- but, the slot is used to store the timestamp

The key assumption is: `(msg.sender, message) → maps` to a single storage slot. Once a message is written, any attempt to repeat the same message by the same sender will fail due to the require().

**Questions**

1. My assumption as to why we store timestamp instead of the message itself is that it leads to each proof having a unique verifiable value, and this Helps off-chain provers quickly disambiguate proofs. And the stored message is time-bound attested which helps as well. Is this a correct understanding?
2. Secondly, why does broadcast rely on the caller smart contracts to include a proper nonce in the message being passed to broadcastMessage() function?

There is a possibility that **Solver X fulfills BOB’s intent for transferring 100 USDT**. And later the same solver fulfils the same intent again.

In this case:

- both fulfilment will lead to same message.
- and the broadcast will reject to broadcast the 2nd message as it will see it as a repetition.
- The broadcastMessage() function heavily relies on apps ( smart contract that uses CCB ) to implement nonces.

**But, Why can’t Broadcaster not implement this on its own?**

Possible routes:

1. Add a nonce field per (msg.sender)
 → You broadcast (message, nonce) → stored at keccak256(message, nonce, msg.sender)
2. Alternatively, include a timestamp or intent ID in the message
 → Ensures uniqueness even if semantic content is the same
3. Standardize message construction (e.g., with domain separator, version, user, action, and nonce).

---

Overall love the idea.

Will drop a few more questions as I explore more.

---

**godzillaba** (2025-04-22):

Hi zaryab, thanks for the thoughtful questions and feedback!

Originally, we had `(msg.sender, message) -> bool` indicating whether a message was sent. The `Receiver` would then check a storage proof that the slot for `(msg.sender, message)` is 0/1. We changed that to map to a timestamp simply because a `bool` was a waste of a slot, and many apps might want to know the timestamp of a message.

The reason we don’t have a nonce for messages is that it would slightly complicate the spec, use an extra storage slot, and not all apps would benefit from it. Apps can use whatever message semantics they want, and implement nonces if they *need* to be able to send the same message multiple times. The `Burner` example in the spec includes a nonce in its messages because the same user might burn multiple times, for example.

---

**ernestognw** (2025-06-06):

Hey [@yahgwai](/u/yahgwai) and [@godzillaba](/u/godzillaba)! ![:waving_hand:](https://ethereum-magicians.org/images/emoji/twitter/waving_hand.png?v=15)

Love the momentum behind [ERC-7888](https://ethereum-magicians.org/t/new-erc-cross-chain-broadcaster/22927) - storage proofs are exactly what we need for trustless cross-chain messaging.

I’ve been working on a lower level ERC for **[Storage Proof Broadcasting](https://ethereum-magicians.org/t/storage-proof-broadcasting-for-cross-chain-messaging-gateways/24477)** which could serve as a standardized foundation for both ERC-7888 and other storage proof systems like Taiko’s [SignalService](https://github.com/taikoxyz/taiko-mono/blob/main/packages/protocol/contracts/shared/signal/SignalService.sol) (maybe even others).

### The Convergence Opportunity

For example, looking at [Taiko’s SignalService](https://github.com/taikoxyz/taiko-mono/blob/main/packages/protocol/contracts/shared/signal/SignalService.sol) and ERC-7888, both systems share core patterns:

- Storage proof verification
- Multi-hop routing capabilities
- Broadcast messaging semantics
- Deterministic storage locations

**The missing piece**: A standardized low-level interface that both can build on.

## Implementation Path

```solidity
// Both ERC-7888 and Taiko could implement this interface
contract StorageProofGateway is IERC7786GatewaySource {
    function sendMessage(
        string calldata chainId,
        string calldata receiver, // "" for broadcast
        bytes calldata data,
        bytes[] calldata attributes
    ) external payable {
        // attributes[0]: route((address,bytes,uint256)[])
        // attributes[1]: storageProof(bytes)
        // attributes[2]: targetBlock(uint256)

        // Route to either ERC-7888 Broadcaster or Taiko SignalService
    }
}
```

**Impact**: Instead of parallel development, we get ecosystem-wide compatibility, shared tooling, and easier integration paths. Both teams benefit from a common foundation while maintaining their specialized approaches.

Curious to hear your thoughts on this approach. I also opened a PR that makes 7888 compatible with ERC-7786 but doesn’t enforce it: [Specify compatibility with ERC-7786 by ernestognw · Pull Request #2 · OffchainLabs/ERCs · GitHub](https://github.com/OffchainLabs/ERCs/pull/2). Opened an [update to your reference implementation](https://github.com/OffchainLabs/broadcast-erc/pull/4) that minimizes changes so it’s easier for you.


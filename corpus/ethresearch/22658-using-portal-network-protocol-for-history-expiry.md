---
source: ethresearch
topic_id: 22658
title: Using Portal network protocol for history-expiry
author: morph-dev
date: "2025-06-22"
category: Execution Layer Research
tags: [portal-network]
url: https://ethresear.ch/t/using-portal-network-protocol-for-history-expiry/22658
views: 329
likes: 3
posts_count: 4
---

# Using Portal network protocol for history-expiry

# Finalized Chain History Portal subnetwork

The Finalized Chain History is the subnetwork build on top of Portal wire protocol. Its goal is to provide decentralized storage of the finalized historical Ethereum data.

It assumes that nodes on the network are Execution Layer clients that store all historical headers locally. Nodes that are not Execution Layer clients will need a way to obtain block header for a given block number (in order to verify the content).

In the appendix section, I provide comparison to the existing Portal History subnetwork and rationale for the proposed changes.

## Specification

---

### Distance Function

The Finalized Chain History subnetwork uses the stock `XOR` distance metric defined in the Portal wire protocol specification.

### Content id Derivation Function

The content keys (described later) use block number. The content id is calculated in the following way:

```python
CYCLE_BITS = 16
OFFSET_BITS = 256 - CYCLE_BITS # 240

def content_id(block_number):
    offset_bits, cycle_bits = divmod(block_number, 2**CYCLE_BITS)

    # reverse the offset bits
    offset_bits = int('{:0{width}b}'.format(offset_bits, width=OFFSET_BITS)[::-1], 2)

    return cycle_bits
whether partial response is considered valid

- maybe this should be a message field

#### RangeContent (0x09)

Response message to Range Find Content (0x08).

```python
selector           = 0x09
range_content      = Union[
                         connection_id: Bytes2,
                         content: List[ByteList[2048], 65535],
                         enrs: List[ByteList[2048], 32],
                     ]
```

This message type is almost identical to the [Content message](https://github.com/ethereum/portal-network-specs/blob/73c7e9dce2190ec0d5225f1041967479b75cbb49/portal-wire-protocol.md#content-0x05). The only difference is that the `content` is a list of content values.

## Appendix: Rationale and explanations

---

### Comparison with legacy History Portal Network

If we assume that most of the nodes on the network are execution layer clients, we have to take into consideration some of their properties:

- The EL clients store all historical block headers
- The EL clients are long running
- Most common use case for accesing Finalized Chain History is to sync node from genesis

The EL clients don’t have access to `HistoricalSummaries` object that is needed to prove headers on the legacy History Portal Network. With this consideration and the fact that EL clients store all block headers, we no longer need to keep headers on the network. If this changes in the future, we can easily add them, and decide if we do so with or without proof.

After EL client syncs block headers, it can calculate which of the bodies and receipts it should store, and it can fetch them from the network. As the chain is progressing, the EL clients can just keep the bodies and receipts that they need. This eliminates the need and effectiveness of the bridges.

The disk requirements for EL clients is expected to grow over time. Therefore, it’s more reasonable for them to have fixed radius (compared to portal clients that were mostly using dynamic radius).

Using the block number and custom `content_id` function allows us to easily add batch requests in the future. This should improve the performance of synching the client from genesis.

Using `rlp` encoding for bodies and receipts is more alligned with the way the EL clients store and process data.

### Content id function

The goal of the `content_id` function is to evenly spread content around domain space, while keeping consecutive blocks somewhat close to each other.

The blocks are split into cycles, where each cycle contains 65536 `(2^CYCLE_BITS)` consecutive blocks. Blocks from a single cycle are evenly distributed across entire domain space. Blocks from different cycles are offset in order to prevent multiple blocks mapping to the same `content_id` and to spread content more evenly.

Visualization of this idea is shown in the following [image](/uploads/short-url/gZFkW3rfdDTpx36oVg7Wk3SkcTQ.png).

[![Content Id idea visualization](https://ethresear.ch/uploads/default/optimized/3X/7/7/771b503b4d83e779eafd1f9c42cac96ee58c5f16_2_690x248.png)Content Id idea visualization2500×901 107 KB](https://ethresear.ch/uploads/default/771b503b4d83e779eafd1f9c42cac96ee58c5f16)

We achieve this by manupulating bits of `block_number (uint64)`:

1. 16 least significant bits (cycle bits) and 48 most significant bits (offset bits) are swapped
2. Offsetting blocks from different cycles in a desired way is done by reversing the order of offset_bits
3. Finally, we append zeros at get a value from the domain space (uint256)

The following [image](/uploads/short-url/zmSiuvhqBZx2XRblE8IB0NVHWaG.png) shows this process for a block number `12'345'678`.

[![Content id derivation visualization](https://ethresear.ch/uploads/default/optimized/3X/f/7/f7e21327137b02ebf0cacea6bec27c8c5b545416_2_690x264.png)Content id derivation visualization1248×479 58.6 KB](https://ethresear.ch/uploads/default/f7e21327137b02ebf0cacea6bec27c8c5b545416)

#### Interaction with distance function (XOR)

Because we use `XOR` as a distance function, it’s possible that the radius doesn’t cover continuous section of the domain space (resulting in “holes” in the stored range). This is not a big concern because:

- It is guaranteed that at least half of the radius will be continuous

This continuous section will include the NodeId

If the radius is power or two, then the entire stored range is continuous

- If we assume that clients use fixed radius, then they can enforce this

#### Choosing CYCLE_BITS

The choice of the `CYCLE_BITS` has two tradeoffs that should be balanced:

- bigger value implies that each peer will store fewer longer sequences of consecutive blocks, rather than many shorter sequences
- bigger value also implies that if there is more demand for certain range of blocks (e.g. towards the head of the chain), the same nodes while take on the burder for longer to serve those requests

The value `CYCLE_BITS=16` is chosen because it simplifies function implementation in most languages (manipulation on byte vs. bit level), and because if we assume that each peer stores at least `1/256 (≈0.4%)` of all content, then they will also store sequences of at least `256` consecutive blocks (which feels like the a good balance).

## Replies

**kdeme** (2025-06-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/morph-dev/48/14323_2.png) morph-dev:

> Using rlp encoding for bodies and receipts is more alligned with the way the EL clients store and process data.

Is that’s the only reason to have this in `rlp` encoding?

In Portal originally the reasoning was to use `ssz` encoding for everything that does not required hashing its `rlp` encoding. As a means to not keep creating new `rlp` encoded objects where not really required.

![](https://ethresear.ch/user_avatar/ethresear.ch/morph-dev/48/14323_2.png) morph-dev:

> If the radius is power or two, then the entire stored range is continuous
>
>
> If we assume that clients use fixed radius, then they can enforce this

That’s a very good point regarding continuous range when radius within power of two (no “holes”).

But I don’t like the idea of forcing clients to use a “static power of two” radius. Of course in the current suggested setting with EL clients being the only (or big majority of) Portal nodes it makes sense. And I would suggest that EL clients do set it to such a radius. But I would like to keep the door open for other types of nodes still. Of course one could argue that for nodes with a more dynamic storage size one could still decrement in those power of two steps, but that isn’t very granular.

![](https://ethresear.ch/user_avatar/ethresear.ch/morph-dev/48/14323_2.png) morph-dev:

> Request message to get the multiple content anchored with a given content_key.

I assume you are aware of this but I want to point it out for completeness here.

For range requests a requesting node might just select a start value + counter where the start value is:

- either right in front of a “hole” (as you name it before) for the requested peer
- or just on the edge of the range of the requested peer

This would occur if the implementation of the requesting node would use a more simple / naive (but not necessarily considered wrong or bad) approach where it would only do the “within radius” check for the first value.

This could be left as decision for implementers or we could engrain it in the specification but clients could/should:

- Verify if the node should have the full range (include or not including hole checking), which is possible to do.
- Or just go for it based on one simple check, and then depending on what they get back, just continue requesting the rest to other nodes. This case does require an incomplete response to be a valid response according the specifications.

---

**morph-dev** (2025-06-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/kdeme/48/16711_2.png) kdeme:

> Is that’s the only reason to have this in rlp encoding?

Yeah, mostly. I don’t have strong preferences one way or the other, but I think Geth prefers `rlp` as most of these object are already encoded like that in EL clients.

![](https://ethresear.ch/user_avatar/ethresear.ch/kdeme/48/16711_2.png) kdeme:

> But I would like to keep the door open for other types of nodes still.

I totally agree. Dynamic and non-power-of-two radius are probably fine as well, considering that at least half  of the radius will continuous and that part will include `NodeId`.

If a client wants dynamic radius and to keep number of “holes” as small as possible, it can increase/decrease radius by some power-of-two that is similar order of magnitude as the current radius (goal is to have as many zero-bits in the radius). This doesn’t allow for full granularity of radius values, but I think it’s good enough (but I wouldn’t enforce this).

---

Regarding range queries, there is definitely some exploration to be done. But I think proposed `content_id` derivation allows for it which is the most important step at this point. We can specify range queries in such a way that they work well.

I think client making the request should be smart about it. For example, requesting range that contains these two content_id `0x0FFF..FF` and `0x1000..00` doesn’t make sense (and these can be two consecutive blocks), because only peer that has radius higher than 50% will have a chance of actually having both values (so very likely no peers).

Simple solution is as you said, allowing partial responses (and in my opinion good enough). But client making the request can/should still be smart about how it does it.

---

**kdeme** (2025-07-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/morph-dev/48/14323_2.png) morph-dev:

> The content keys (described later) use block number. The content id is calculated in the following way:

A remark regarding this content id calculation:

The resulting content id for `BlockBody` and `Receipts` will be the same.

On a protocol level this is not a problem as the `ContentKey` is used to request or offer content (not the content id).

However, having the same content id for different content types was never the case in the previously defined Portal sub-networks and thus could be an issue in current Portal implementations if just taken “as is”, e.g. when the content id is used as primary key in the database.

Nothing that an implementation cannot adapt for of course, but it is worth noting.

We could also decide to alter slightly the content id per type.


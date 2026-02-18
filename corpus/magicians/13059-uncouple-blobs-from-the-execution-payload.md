---
source: magicians
topic_id: 13059
title: Uncouple blobs from the execution payload
author: potuz
date: "2023-02-26"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/uncouple-blobs-from-the-execution-payload/13059
views: 987
likes: 5
posts_count: 1
---

# Uncouple blobs from the execution payload

## The problem

It is expected  that in the future, home stakers will not be able to locally produce full blocks. This is in particular true after full Danksharding in which we do not expect a home computer to be able to compute the KZG commitments on time.

This forces proposers to rely on external builders to prepare these blocks, which in turn imposes a threat to censorship resistance: a few external players (the builders) will have ultimate decision of what transactions are included or not on L1.

While it is true that a non-censoring proposer may always propose execution blocks without any blobs, this becomes a strong centralizing force in that non-censoring validators have to forfeit their earnings from blobs (which in a rollup-centric roadmap are expected to be a large part of the block) if they want to control their execution contents.

## The proposal

We propose a separation of blob transactions from the rest of the execution payload. This achieves the following objectives:

- Home computers are still able to produce execution blocks and defer blob production to builders.
- The validity of blobs and execution payload can be verified in an independent manner, thus this mechanism is more resilient to bugs in the builder that produce invalid commitments for example.
- Fully compatible with the current design with minimal protocol changes

The main con is in the extra complexity needed on relayers and external software like MEV-Boost. Another con is that transactions will not be able to interact with blob transactions immediately, as blob transaction processing is deferred for one block.

## Implementation details

### Consensus Layer

We propose that the `ExecutionPayload` structure has an extra field `blob_transactions` containing all blob transactions and that the field `transactions` does not have any blob transactions allowed. Additionally, the `ExecutionPayloadHeader` will include a field `blob_transactions_root` containing the root for the `blob_transactions` field serialized as an SSZ list of byte slices.

The idea is that a proposer may sign blindly an `ExecutionPayloadHeader` without knowing the full `transactions` and `blob_transactions` lists, or may choose to include it’s own transactions and sign blindly without knowing the `blob_transactions` list. Implementation of the Builder API is left unspecified, but it could be for example that the builder submits a full header but the proposer sends back a signed header with it’s own transactions lists. The relay will recognize the builder’s `blob_transactions_root` in the header, but a different `transactions_root` and different values for the execution part of the header, thus the relayer will assemble a full block by including the builder’s `blob_transactions` and broadcasting.

It may be needed to have different blockhash values, for the execution part and the blob part of the block. Or simply keep the `BlockHash` value to be the execution hash, this plus the `blob_transactions_root` should be enough of an identifier.

### Execution Layer

When receiving an `engine_NewPayload`, the execution client will receive both transactions and blob transactions for block `N` and it has still the blob transactions for block `N-1`.

It will start by processing the `blob_transactions` from block `N-1` (if they were deemed valid) and then processing the `transactions` for  block `N`. After that it will check if the `blob_transactions` for block `N` are valid with the post-state after applying the `transactions` for block `N`.

Thus, after each block `N`, the next proposer of `N+1` knows if the `blob_transactions` for `N` were valid or not. If they were invalid, the block `N+1` will act as if the block `N` had no blobs in it.

## Final comments

This system allows for the network can progress even if there’s failure in producing blobs by centralized builders. It allows for home computers to produce execution blocks and it can be customized so that specialized builders only bid for blob transactions and/or execution transactions separately.

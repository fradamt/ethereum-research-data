---
source: magicians
topic_id: 11364
title: "EIP-5793: eth/68 Add transaction type to tx announcement"
author: MariusVanDerWijden
date: "2022-10-18"
category: EIPs > EIPs networking
tags: []
url: https://ethereum-magicians.org/t/eip-5793-eth-68-add-transaction-type-to-tx-announcement/11364
views: 2906
likes: 2
posts_count: 4
---

# EIP-5793: eth/68 Add transaction type to tx announcement

Discussion for [Add EIP-5793: eth/68: Add transaction type to tx announcement by MariusVanDerWijden · Pull Request #5793 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5793) here please

## Replies

**etan-status** (2023-02-11):

As part of the EIP-4844 discussions, the topic of type-5 0-blob transactions came up repeatedly.

One problem with 0-blob transactions is that eth/68 does not allow distinguishing between transactions containing blobs and some that don’t, so 0-blob transactions would be treated as if they had blobs on the networking layer (use of wrapper type, Req/Resp, no rebroadcast on reorg).

Similar issues could reoccur with future transaction types. The EIP-2718 transaction type has never, conceptually, determined the networking and mempool behaviour when processing a transaction. What it does define, is the actual encoding of the transaction itself (globally, including `GetBlockBodies`), and the mechanism used for deriving the originally signed transaction hash and the perpetual transaction hash.

As eth/68 intends to change the transaction processing behaviour solely for transactions in the transaction-pool and local transaction-journal, I don’t think that the EIP-2718 transaction type is a good fit to encode that information. Instead, a separate field in eth/68 would make more sense to denote the (temporary) behaviour of affected transactions while they sit in one of those pools. Once a transaction is included into a block, none of that temporary behaviour should remain encoded.

Example how eth/68 could be defined (different designs possible):

```python
NewPooledTransactionHashes (0x08) := [
    [txtype₁: B_1, size₁: B_4, txhash₁: B_32],  # no blobs
    [txtype₂: B_1, size₂: B_4, txhash₂: B_32, num-blobs₂: B_1],
    ...
]

PooledTransactions (0x0a) := [
    request-id: P,
    [
        [tx₁],
        [tx₂, SSZ.encode({blob-kzgs₂, blobs₂, kzg-aggregated-proof₂})],
        ...
    ]
]
```

This way, the special Req/Resp gossip behaviour for transactions containing blobs could be triggered by presence of the `num-blobs` field, instead of based on the TX type, and 0-blob type-5 transactions would no longer be a special case.

---

**etan-status** (2023-02-14):

This was discussed in today’s [EIP-4844 breakout call](https://github.com/ethereum/pm/issues/722).

Alternatives that were brought up:

- Using a flag to indicate that a tx should not be gossiped.
- Deciding solely based on size >= 128 KB (for example).
- Explicitly banning 0-blob transactions when sent using type 0x05, everywhere including consensus.

```python
NewPooledTransactionHashes (0x08) := [
    [no-gossip₁: B_1, no-gossip₂: B_1, ...],
    [size₁: B_4, size₂: B_4, ...],
    [txhash₁: B_32, txhash₂: B_32, ...]]
    ...
]
```

---

**etan-status** (2023-08-31):

Currently, in EIP-6493 (SSZ transactions), to retain the usefulness of the proposed `txtypes` field, I had to redefine it to mean 0x01 => basic transaction (without blob), and 0x03 => blob transaction.

Is there an advantage of allowing to distinguish type 0x00 / 0x01 / 0x02 in practice, or would be alright to combine these to be reported as 0x01?



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-6493#transaction-gossip-announcements)





###



Signature scheme for SSZ transactions










Problem is that the SSZ transactions share type 0x04 for both basic and blob transactions, so a different mechanism is necessary there to allow distinguishing them.

Note that the proposed change in EIP-6493 would be somewhat compatible with EIP-5793, as 0x03 would still map to blob transaction, and 0x01 would still map to basic transaction.


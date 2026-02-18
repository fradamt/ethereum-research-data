---
source: magicians
topic_id: 4561
title: "EIP-2930: Optional access lists"
author: vbuterin
date: "2020-09-02"
category: EIPs > EIPs core
tags: [transactions, eip-2930]
url: https://ethereum-magicians.org/t/eip-2930-optional-access-lists/4561
views: 66191
likes: 21
posts_count: 40
---

# EIP-2930: Optional access lists

A companion EIP to [eip-2929](/tag/eip-2929).



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2930)














####


      `master` ← `vbuterin-patch-3`




          opened 12:08PM - 01 Sep 20 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/8/89ac618501d77ed85e1ea0663718f590291e7737.png)
            vbuterin](https://github.com/vbuterin)



          [+133
            -1](https://github.com/ethereum/EIPs/pull/2930/files)







Adds a transaction type which contains an access list, a list of addresses and s[…](https://github.com/ethereum/EIPs/pull/2930)torage keys that the transaction plans to access. Accesses outside the list are possible, but become more expensive. Intended as a mitigation to contract breakage risks introduced by EIP 2929 and simultaneously a stepping stone toward broader use of access lists in other contexts.












Adds a transaction type which contains an access list, a list of addresses and storage keys that the transaction plans to access. Accesses outside the list are possible, but become more expensive. Intended as a mitigation to contract breakage risks introduced by EIP 2929 and simultaneously a stepping stone toward broader use of access lists in other contexts.

## Replies

**andrekorol** (2020-09-04):

Really interesting concept. Seems like a stepping stone towards stateless clients.

The EIP mentions that the discount for transactions using access lists will increase over time as more tools are developed and access-list generation matures. What kind of tools will need to be developed? Is it just for access-list generation, or also for validation?

---

**vbuterin** (2020-09-04):

Just for access list generation. The code for determining whether or not accesses are part of the access list and doing things based on that is already in 2929.

---

**MicahZoltu** (2020-11-06):

**Transaction Format Options**

```auto
// RLP multi-pass
3 || rlp([nonce, gasPrice, gasLimit, to, value, data, access_list, sendrV, senderR, senderS])
// RLP single-pass
3 || rlp([[senderV, senderR, senderS], rlp([3, nonce, gasPrice, gasLimit, to, value, data, access_list])])
// SSZ deduped
ssz([3, nonce, gasPrice, gasLimit, to, value, data, access_list]) || ssz([sendrV, senderR, senderS])
// SSZ duped
3 || senderV || senderR || senderS, ssz([3, nonce, gasPrice, gasLimit, to, value, data, access_list])
```

- RLP Multi-Pass

Advantages

No new encoding format
- No data duplication

Disadvantages

- Requires an RLP encoder and decoder to validate
- Validation has decode-split-encode-validate flow

RLP Single-Pass

- Advantages

No new encoding format
- Can validate signature without needing an RLP encoder
- Supports decode-validate flow

Disadvantages

- Duplicates the transaction type byte
- Requires RLP decoder to validate

SSZ Deduped

- Advantages

No data duplication
- Can validate signature without needing an SSZ encoder
- Supports decode-validate flow

Disadvantages

- Requires SSZ encoder for creating
- Requires SSZ decoder for validating
- Requires retaining access to the leading type byte when processing (or re-inserting it)

SSZ Duped

- Advantages

Can validate without an SSZ encoder
- Can validate without an SSZ decoder
- Supports fixed offset extraction of signature
- Supports pluck-validate flow

Disadvantages

- Requires SSZ encoder for creating
- Duplicates the transaction byte

---

**matt** (2020-11-07):

This is a great summary, thanks [@MicahZoltu](/u/micahzoltu).

Why does the second option need to have `3` in multiple places? Couldn’t we alternatively enforce `keccak(3 || rlp([nonce, gasPrice, gasLimit, to, value, data, accessList]))` be the hash that is signed over? It would require minimal assemble and would avoid the weird edge case where the outer type doesn’t match the inner type.

---

**MicahZoltu** (2020-11-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Couldn’t we alternatively enforce keccak(3 || rlp([nonce, gasPrice, gasLimit, to, value, data, accessList])) be the hash that is signed over?

I believe this option would work, but it means we would have two different encoding schemes at play, which is a bit unfortunate.  Part of the goal with these 4 proposals was to minimize the complexity of encoding, and having to encode *most* of the signed data and then encode that along with some more data to get the final signed thing increases complexity.

If people believe that this proposed solution is superior to the 4 options above, I don’t mind adding it to the list to be discussed though!

---

**MicahZoltu** (2020-12-01):

At the All Core Devs call we decided on no SSZ for Berlin.  After some discussion in Discord, we have decided to go with multi-pass as it saves a byte and aligns pretty closely to with how we already deal with transactions.  We also decided to switch over to `yParity` rather than `v` to pay down a bit of technical debt around `v` (EIP-155 and Bitcoin baggage).

The tentative final transaction format will be:

```auto
1 || rlp([chain_id, nonce, gas_price, gas_limit, to, value, data, access_list, y_parity, r, s])
```

---

**qizhou** (2020-12-08):

Should SSTORE gas cost also be reduced by being included the lists?  Looks like the SSTORE’s performance can be increased if its MPT paths are pre-loaded - writing a key-value in MPT is essentially a read-modify-write operation.

---

**jochem-brouwer** (2021-01-17):

What exactly is the rationale for introducing this `Y_Parity` parameter? This seems to add unnecessary complexity? Why would we want to introduce this `Y_Parity` - are there use cases?

Doesn’t this ruin the idea of EIP-155, which prevents that we can run Transactions on chains with a different chain ID? Since we only have a binary `v` value now, this thus does not prevent us from running the Transaction on other chains with different chain IDs?

---

**matt** (2021-01-17):

`Y_Parity` is essentially the same as `V` in normal signatures. It was simplified to just `0` or `1` instead of `26` or `27`. Since `chainID` is now an explicit element in the payload, we can interpret however we like.

Although it is not supported in the current spec, we could definitely add support for `chainID == 0` meaning that the transaction is valid on all chains.

---

**jochem-brouwer** (2021-01-17):

Ah right, I forgot that the chain ID is actually part of the payload - makes sense!

---

**poojaranjan** (2021-01-20):

EIP-2929 & EIP-2930 explained by Vitalik Buterin & Martin Swende -

https://youtu.be/qQpvkxKso2E

---

**winsvega** (2021-01-23):

What is the hash formula of new transactions?

---

**jochem-brouwer** (2021-01-23):

What is the reason that we have to save all the zeros of these addresses and storage slots? Can’t we save some data by left-padding the addresses to 20 bytes with zeros, and the storage slots can be left-padded to 32 bytes with zeros? It does not make sense to me to save all these zeros if we can also left pad them. Transactions are invalid if they provide addresses longer than 20 bytes or storage slots longer than 32 bytes.

---

**jochem-brouwer** (2021-01-23):

> The yParity, senderR, senderS elements of this transaction represent a secp256k1 signature over keccak256(rlp([1, chainId, nonce, gasPrice, gasLimit, to, value, data, access_list])).

---

**matt** (2021-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> What is the reason that we have to save all the zeros of these addresses and storage slots?

This seems like an optimization that can be done over the wire, rather than in consensus.

---

**jochem-brouwer** (2021-01-23):

Ah good point, you are right.

---

**winsvega** (2021-01-24):

The transaction hash as of geth currently  is

Hash ( 01 || rlp([chainId, nonce, gasPrice, gasLimit, to, value, data, access_list, y, r, s]))

Also a thing about this 01 byte inserted before RLP kind of breaks the block rlp encoding. this byte is not rlp encoded and thus makes block rlp oversized.

---

**jochem-brouwer** (2021-01-24):

Does this EIP also implement the Homestead rule: if you create a contract, then charge 53k gas instead of 21k? (I’d assume yes).

From EIP-2:

> The gas cost for creating contracts via a transaction is increased from 21,000 to 53,000, i.e. if you send a transaction and the to address is the empty string, the initial gas subtracted is 53,000 plus the gas cost of the tx data, rather than 21,000 as is currently the case. Contract creation from a contract using the CREATE opcode is unaffected.

---

**jochem-brouwer** (2021-01-28):

How exactly are we supposed to encode this transaction type on a `eth_getTransactionByHash` (and friends)? Do we include a new field `transactionType` here? If this field does not exist, it is a legacy transaction? Simply trying to cast it on the available fields seems dangerous to me (if we get an alternative transaction type which also uses `access_list` then it might get wrongly casted by consumers).

---

**matt** (2021-01-29):

I don’t believe it has been formally specified yet, but the approach we’ve taken so far for typed transactions we also append the `type` field and the transaction-specific fields. You can sort of see how this is done in the PR: https://github.com/ethereum/go-ethereum/pull/21502/files#diff-77719ae57e7e6c3e0cac05fa12c6c5f2e5f9bc810c034d1446de2414c36d9210


*(19 more replies not shown)*

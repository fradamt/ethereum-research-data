---
source: magicians
topic_id: 13050
title: "EIP-6493: SSZ Transaction Signature Scheme"
author: etan-status
date: "2023-02-25"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-6493-ssz-transaction-signature-scheme/13050
views: 3248
likes: 3
posts_count: 17
---

# EIP-6493: SSZ Transaction Signature Scheme

Discussion thread for [EIP-6493: SSZ transaction signature scheme](https://eips.ethereum.org/EIPS/eip-6493)

Vitalik’s notes:

- Proposed transaction SSZ refactoring for Cancun - HackMD

Related discussions:

- 4844: use `hash_tree_root` for tx hash by lightclient · Pull Request #6385 · ethereum/EIPs · GitHub
- https://github.com/ethereum/EIPs/pull/6493

#### Outstanding Issues

- 2024-10-29: Support for SSZ EIP-7702 authorizations is missing, https://eips.ethereum.org/EIPS/eip-7702

#### Update log

- 2025-11-05: Set code authorization support, use progressive types

## Replies

**etan-status** (2023-02-25):

Note that this representation is only for the way how signatures are signed, identified, and represented before inclusion in a block. For post-block-inclusion, there is EIP-6404.

The new signature scheme proposed here is close to what the “SSZ Union” approach in Vitalik’s notes / EIP-6404’s test section is referring to, so it doesn’t conflict with the approach based on “SSZ Union”.

For “SSZ Normalized” approach, the transaction’s mempool encoding is not linked to the post-block-inclusion encoding, so there is no concern either.

---

**etan-status** (2023-04-20):

Some open questions about the proposed signature scheme:

- Do we need both fork_version and genesis_hash ?

Why are both of these used in consensus?

---

**etan-status** (2023-04-27):

Changes for EIP-4844 proposed:

- move EIP-6493 to review: Update EIP-6493: Move to Review by etan-status · Pull Request #6947 · ethereum/EIPs · GitHub
- bump EIP-4844 to use SSZ signature scheme: Update EIP-4844: Use EIP-6493 signature scheme by etan-status · Pull Request #6948 · ethereum/EIPs · GitHub

Another open question would be whether we want to use a plain 65 byte array in EIP-4844 for the signatures, same as in the EIP-6493 example. Personally, I don’t see too much value in putting separate y/r/s components into the SSZ object, as they are always processed together (except for legacy tx which is not ssz where y can have chain id). It could also avoid the nasty byte swap (SSZ is little endian, but cryptography libs expect big endian).

---

**roberto-bayardo** (2023-04-28):

re: plain 65 byte array for signature:  this makes sense to me now that we aren’t trying to hack other data into it.

---

**etan-status** (2023-04-29):

In [EIP-6404: SSZ Transactions Root](https://eips.ethereum.org/EIPS/eip-6404), I have experimented with opaque signatures, in case you are curious how one would work with them. Note, 6404 is out of scope for Deneb, but maybe that signature style could be used for EIP-4844 as well (with 65 bytes instead of varlen).

---

**matt** (2023-05-01):

1. I think you’re right, we don’t really need the fork_version since we don’t need to expire tx signatures on fork boundaries. As spec’d, it only prevents the tx from being valid on a different chain with i) the same genesis and ii) the same tx type, but introduced at a different fork. Also, I don’t think we want to enshire CRC32 into the protocol?
2. What does 6493 actually provide us? The signature hash is usually ephemeral and only appears during tx validation. This seems like a lot of work to use SSZ without an perceptible benefit?

---

**etan-status** (2023-05-02):

The forkid is not about signature expiration, hence why the idea is to always use the same fork_version there (the one is used where the new transaction type was originally introduced, even during later forks).

Instead, the goal is to uniquely identify the type schema that the signature pertains to.

- GENESIS_HASH: This ensures that the signature is not replayable across chains with a different root
- CHAIN_ID: This ensures that the signature is not replayable across later forks (e.g., EthereumPoW, Ethereum Classic)
- EIP-2718 FORK_VERSION: This ensures that a type 3 signature for a type introduced at fork_version is not replayable in the future, if type 3 is retired and later reused as something else.
- EIP-155 TX_TYPE: This ensures that signatures for different types are not replayable as a transaction for a different type.

Note that all of these values are constants, they do not need to be computed at runtime. The entire resulting signing domain is a (chain-specific) constant. Goal is to make absolutely sure that the signature is not replayable in any unintended situation.

Personally, I don’t understand why we need *both* a FORK_VERSION and GENESIS_HASH/CHAIN_ID. I suggested it this way, because that’s how it was done in consensus-specs. If it can be determined that it is safe to drop one of them, I’d be happy to do so. Would also appretiate explanations why it was deemed necessary in consensus. The only reason I can think of, is making a type obsolete and reusing it later, but that could also simply be avoided by not reusing types.

Regarding the ephemeral nature of the signature hash: EIP-6493 aims to protect against a signed transaction from one chain being replayed on a different chain where it could be a valid transaction of a different SSZ scheme. EIP-6493 does so, by encoding information about the underlying signed SSZ scheme into the signature hash.

---

**etan-status** (2023-08-28):

Updated [EIP-6493](https://eips.ethereum.org/EIPS/eip-6493) to use the [SSZ PartialContainer](https://eips.ethereum.org/EIPS/eip-7495).

This is compatible with the previous version, but further restricts the definitions from generic SSZ containers to ones where common fields are assigned the same SSZ generalized indices, hence having improved merkleization properties (simpler verifiers).

Furthermore, https://eth-light.xyz has a showcase to inspect the proposed SSZ representation for any given transaction.

---

**etan-status** (2023-08-29):

Also added the corresponding SSZ `Receipt` format to EIP-6493.

---

**etan-status** (2023-10-29):

Bumped with type safety support using `Variant[S]`:

- Update EIP-6493: Use `Variant[S]` for type safety by etan-status · Pull Request #7939 · ethereum/EIPs · GitHub

See discussion: [EIP-7495: SSZ StableContainer - #17 by etan-status](https://ethereum-magicians.org/t/eip-7495-ssz-stablecontainer/15476/17)

---

**etan-status** (2024-05-13):

Added `chain_id` to the `TransactionPayload` and moved `type` to start:

- Update EIP-6493: Add `chain_id` and move tx `type` to start by etan-status · Pull Request #8548 · ethereum/EIPs · GitHub

Rationale:

1. Networks such as EthereumPoW which may temporarily want to allow transactions from multiple chain IDs during the transition period.
2. chain_id being passed out-of-bands for serialization / hashing having a significant impact on practical implementations. Other serialization / hashing doesn’t require out-of-bands information.

---

**etan-status** (2024-05-16):

Alternative design based on multidimensional fees:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png)
    [EIP-7706: Create a separate basefee and gaslimit for calldata](https://ethereum-magicians.org/t/eip-7706-create-a-separate-basefee-and-gaslimit-for-calldata/19998/4) [EIPs](/c/eips/5)



> The EIP describes three changes:
>
> Switch to a multidimensional fee structure
> Allowing priority fees for blob transaction
> Introduction of a separate calldata gas fee
>
> I’m wondering about the encoding of the max_fees_per_gas and priority_fees_per_gas vectors on JSON-RPC. Natively, they would be represented as a list of integers (in the typical string representation), without any guidance on which of the fees corresponds to what type of fee. For example, there must be external knowledge that the s…

---

**etan-status** (2024-05-16):

Updated for latest EIP-7495 advancements, and shortened type names:

- SignedTransaction → Transaction (matches existing meaning in consensus specs)
- BasicTransaction / BlobTransaction → No longer have a type field. With SSZ transactions, the profile is determined dynamically (select_from_base helper) and having a hardcoded 0x04 in every transaction does not add any value. 0x04 is still used in the network wrapper when exchanged on devp2p.
- Renamed Variant → Profile according to EIP-7495

https://github.com/ethereum/EIPs/pull/8565/files

---

**etan-status** (2024-05-23):

Updated transactions to use a vector layout for fees and priority fees, inspired by EIP-7706:

https://github.com/ethereum/EIPs/pull/8579/files

https://eth-light.xyz updated as well. Example:

- Ethereum Light

Receipts will be revisited lateron.

---

**etan-status** (2024-05-27):

Specced out engine API:

https://github.com/ethereum/EIPs/pull/8603/files

---

**etan-status** (2025-11-05):

https://github.com/ethereum/EIPs/pull/10722

- Rebase to use latest EIP-6404 specs (based on ProgressiveContainer)
- Include EIP-7702 authorization support (native SSZ authorizations)
- Update signing domains


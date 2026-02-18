---
source: ethresearch
topic_id: 23422
title: Smart-Contract or EOA Spend Authority for Private Accounts
author: AdamGagol
date: "2025-11-11"
category: Privacy
tags: []
url: https://ethresear.ch/t/smart-contract-or-eoa-spend-authority-for-private-accounts/23422
views: 256
likes: 3
posts_count: 1
---

# Smart-Contract or EOA Spend Authority for Private Accounts

**Disclaimer:** both the idea as well as the writeup is in collaboration with [@DamianStraszak](/u/damianstraszak).

## General idea

**Goal.** Let a standard EVM account, either an EOA or a smart contract, be the *sole* authority that approves spends from a ZK private account.

**Mechanism.** The controller signs an EIP‑712 (typed structured data) **SpendAuthorization**, while a separate **proving_key** derives note secrets and generates the ZK proofs. The proof must match an on‑chain authorization commitment.

**Guarantee.** Custody stays under the same EVM controls users already trust (hardware wallets, multisigs, governance), while proving and secret storage can be delegated without giving spending power or revealing plaintexts.

This enables:

- multisig or smart-contract control over a private account using existing cryptographic standards,
- hardware-wallet protection (controller keys live on the device; viewing and proving secrets stay off the wallet),
- delegating secret storage and proving to an external service without giving it custody (of course this DOES compromise privacy guarantees to some extent, even if TEE is used),
- straightforward wallet integration - wallets attach EIP-712 data to transaction and communicate with a dedicated RPC, without handling secrets or proofs,
- optional private transfers to users who have never used the system, addressed by their regular EVM account. Secrets for the recipient can be shared through a trusted relayer or encrypted with Waku/Whisper, the latter requiring the recipient’s public key to be known.

**Limitations**

- Some information leaks are unavoidable, but when used as intended, the only visible signal is that “the account controlled by this address performed some operation.” In practice:

 the system is optional; users can still operate in the classical mode without separated spend authority,
- the authorization and proof can be submitted separately, allowing delayed proving for timing-based mixing.

# Core concepts

`control_account` - an EOA or a smart contract. It is used only to authorize actions and can be a multisig with keys on hardware. In some limited capability (although still reasonable) it can even be a DAO or any other smart contract that doesn’t have unique signing capabilities (i.e., EIP-1271 support is not required).

**`proving_key`** - a keypair used to (a) decrypt SpendAuthorization and state snapshots and (b) derive fresh note secrets. Leakage harms privacy, not custody. Rotation is authorized by the `control_account`.

**`SpendAuthorization`** - a typed instruction sent by `control_account` that binds the to‑be‑proven action (transfer or withdrawal, deposits don’t require **SpendAuthorization**). **SpendAuthorizations** are stored in a dedicated Merkle tree. A spend proof must include a Merkle proof of membership for a matching SpendAuthorization.

**Rotation** — both `control_account` and `proving_key` can be rotated without revealing the rotation on‑chain (rotate the registered `proving_key` with an authorization from the `control_account`).

## Order of operations during transaction:

**Controller** (holds `control_account`) authorizes actions by creating a **SpendAuthorization**.

**Prover** (holds `proving_key`) stores secrets and generates proofs.

A transaction succeeds when:

1. the SpendAuthorization is inserted into the SpendAuthorization Merkle tree by the controller
2. the prover submits a ZK proof that consumes the authorized notes and matches the SpendAuthorization. (this can be done by external prover in another transaction, or alternatively - submitted with SpendAuthorisation for gas optimization)

Nontrivial example: the `control_account` is a multisig, e.g., SAFE account, and one of the signers stores ZK secrets and runs the prover. All signers already see account state, so no extra privacy is lost due to proving delegation.

# Details:

We assume that reader is familiar with how ZK-based privacy works in EVM system and hence do not define terms such as `note`, `trapdoor`, and`nullifier` , nor explain what constraints needs to be verified to perform regular private transaction. The particular implementations differ in some technical details (including dealing with nullifier), but the differences are unrelated to what is being proposed. Particular descriptions can be found here: https://docs.blanksquare.io/protocol-details/shielder or here: https://docs.railgun.org/wiki/learn/privacy-system.

### Note structure:

Each note includes the usual fields and one optional field:

- control_account: address | 0 - if non‑zero, spends must match a SpendAuthorization authorized by this address.

New note secrets (`trapdoor` and the secret that will later produce the **`nullifier`**) are derived from a PRF keyed by the `proving_key`, allowing for recovery in case of losing other secrets.

In case of `control_account` field being set to `0`, the privacy system works as without this modification, i.e. proof of SpendAuthorisation is trivially accepted, allowing transactions not requiring SpendAuthorisations to mix together with ones that do require it, but choose to delay execution (i.e., doesn’t send the proof in the same transaction as `SpendAuthorisation`).

## SpendAuthorization Merkle tree

An additional Merkle tree is created, with SpendAuthorizations stored as pairs `(control_account, enc_ck(SpendAuthorization))` where `enc_ck` is symmetric encryption with key derived from `proving_key` by snark-friendly symmetric encryption scheme (e.g., [this](https://docs.blanksquare.io/protocol-details/cryptography/snark-friendly-symmetric-encryption)). The `SpendAuthorization` itself contains fields:

`opType,               // TRANSFER | WITHDRAW `

`invalidatedNotesHash, // hash of sorted list of input note commitments `

`newNotesHash,         // hash of sorted list of output note commitments `

`value,                // WITHDRAW value (0 for TRANSFER) `

`recipient,            // EVM address (0 for TRANSFER) `

`expiry,               // block/time after which this authorisation is invalid `

`control_account,      // address `

`privacySystemId       // domain separation inside EIP-712`

In order to insert SpendAuthorization to the Merkle tree, controller calls:

- AddSpendAuthorization: the control_account submits ciphertext. The contract adds (control_account, ciphertext) and appends it.

### Comment on SpendAuthorization creation:

In general, there are two ways for users to utilize this system - by storing all the secrets locally, or delegating them to some external system. In the first scenario, SpendAuthorization can be easily created based on all the owned data. In the latter, it is a bit more tricky and controller does need to initiate communication with Prover before constructing authorization in order to learn:

- current notes
- secrets that should be used to create new notes (derived from proving_key, that may not be in possession of controller)

## Privacy model:

At first glance it may look like submitting SpendAuthorizations directly from `control_account` entirely defeats the purpose of the system via leaking relation to the controller. It is not exactly the case:

- in the context of a private transaction, the only information that is actually revealed is that control_account executed SOME operation. This is, arguably, quite high degree of privacy, especially that control_account can be privately rotated at will and new one only needs funds for the gas cost of submitting transactions.
- even in the context of the withdrawal not all privacy needs to be given away - by delaying execution (i.e., using AddSpendAuthorization and delaying sending a proof via relayer), user can effectively lower chances of linking particular withdrawal to the fact of submitting SpendAuthorization.
- in general when submitting SpendAuthorization with a proof, it is advised to use private transaction even in case of recipients that usually do not use the system. The sole fact that recipient will likely claim the incoming transfer with some delay adds into privacy.

## Threat model

- proving_key leaks: attacker can read balances/history from the period between rotations, but cannot spend.
- access to the control_account leaks: custody is lost
- prover/relayer is malicious: they cannot spend without a SpendAuthorization; they can withhold proofs, but switching relayer solves it

## Reasonable extensions omitted for clarity:

- view tags should be added to SpendAuthorizations to simplify scanning for owned SpendAuthorizations

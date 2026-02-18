---
source: magicians
topic_id: 26858
title: "ERC-8092: Associated Accounts"
author: katzman
date: "2025-12-02"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-8092-associated-accounts/26858
views: 722
likes: 9
posts_count: 9
---

# ERC-8092: Associated Accounts

A new standard for linking blockchain accounts across chains and platforms.

ERC-8092 introduces a standardized method for establishing verifiable associations between blockchain accounts. The specification enables two addresses to publicly declare, prove, and revoke their relationship through a cryptographically signed payload.

[Add ERC: Associated Accounts by stevieraykatz · Pull Request #1377 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1377)

## What It Solves

Managing multiple blockchain addresses across different chains and platforms creates friction for users and applications alike. ERC-8092 provides the infrastructure for:

- Sub-account relationships: Link multiple addresses under a primary identity
- Delegation schemes: Authorize specific accounts to act on behalf of another
- Reputation aggregation: Consolidate activity and credentials across addresses
- Cross-chain identity: Connect accounts on different blockchain networks

## How It Works

The specification defines two core data structures:

Associated Account Record (AAR) contains the association details: initiator and approver addresses, validity timestamps, and optional contextual data identified by an interface selector.

Signed Association Record (SAR) wraps the AAR with cryptographic signatures from both parties, key type identifiers, and revocation status.

Both parties sign the EIP-712 hash of the association, creating a trustless proof of their relationship. The standard supports multiple signature schemes including secp256k1, secp256r1, BLS12-381, Ed25519, WebAuthn/Passkeys, and smart contract signatures via ERC-1271 and ERC-6492.

## Storage and Lifecycle

Associations can be stored onchain for transparency and composability, or offchain for scalability. Either party can revoke an association at any time. The specification includes comprehensive validation rules for timestamp validity, signature verification, and revocation status.

## Interoperability

By leveraging ERC-7930 for address representation, ERC-8092 enables associations between accounts on different chains and with different cryptographic architectures. This cross-chain capability is essential for modern multi-chain identity systems.

## Replies

**katzman** (2025-12-02):

More synchronous discussions  happening in this Telegram chat: [Telegram: Join Group Chat](https://t.me/+7KAruLeFrJgzZDIx)

A solidity implementation of the spec’s [core structures](https://github.com/stevieraykatz/AssociatedAccounts/blob/main/src/AssociatedAccounts.sol), a [functional library](https://github.com/stevieraykatz/AssociatedAccounts/blob/main/src/AssociatedAccountsLib.sol) for interacting with `AssociatedAccountRecords` and `SignedAssociationRecords` as well as a simple implementation of an [Associations Store](https://github.com/stevieraykatz/AssociatedAccounts/blob/main/src/AssociationsStore.sol) can all be found in this repo: [GitHub - stevieraykatz/AssociatedAccounts](https://github.com/stevieraykatz/AssociatedAccounts).

---

**0xTraub** (2025-12-15):

I really like the idea but a question about the implementation example. I’m wondering if defining the supported signing schemes is the most scalable way to enable associations between keys of different chains and algos.

Have you considered instead defining an interface and letting the members of the association specify a contract to use as the verifier that meets that interface

```auto
interface AssociationVerifier {

  function validateAssociatedAccount(AssociatedAccounts.SignedAssociationRecord memory sar)
          public
          view
          returns (bool);

  // Returns data on the validation mechanism such as which ZK implementation
  // or curve type.
  function validationMetadata() public pure returns (string);
}
```

That way the struct then becomes

```auto
// Note: The new verifierContract slots in perfectly to the existing fields without requiring
// an additional storage slot.
struct AssociatedAccountRecord {
        /// @dev The ERC-7930 binary representation of the initiating account's address.
        bytes initiator;
        /// @dev The ERC-7930 binary representation of the approving account's address.
        bytes approver;
        /// @dev The timestamp from which the association is valid.
        uint40 validAt;
        /// @dev The timestamp when the association expires.
        uint40 validUntil;
        /// @dev Optional 4-byte selector for interfacing with the `data` field.
        bytes4 interfaceId;
        /// Should be verified as following supportsInterface() on creation
        address verifierContract;
        /// @dev Optional additional data.
        bytes data;
    }
```

As the EVM begins to support more alternative signature validation mechanisms this may be the most efficient and agnostic way to future proof the validation mechanism.

---

**aliceto** (2025-12-15):

Great idea.

If this is combined with [ERC-8091](https://ethereum-magicians.org/t/erc-8091-privacy-address-format/26689/5), would it also be possible to associate privacy addresses with it?

---

**JamesCarnley** (2025-12-16):

I’ve been reviewing the spec and noticed that ERC-8092 defines its own AssociatedAccountRecord and SignedAssociationRecord structures along with a custom EIP-712 signing flow.

Given that this is essentially a verifiable claim about a relationship between two entities, I’m curious if the authors considered building this on top of the Ethereum Attestation Service (EAS) standard?

Is the choice to create a bespoke format driven by the need for the atomic mutual handshake (requiring both signatures in one payload), or is it to avoid the dependency on EAS registries for cross-chain/non-EVM use cases?

It seems like using EAS could provide standard tooling/indexing out of the box and avoid creating something proprietary, so I’d love to understand the trade-offs that led to the current design.

---

**0xDecentralizer** (2025-12-16):

GM everyone,

First open-source contribution for me ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

Left a small typo comment on the ERC-8092 PR while reviewing the draft.

Excited to contribute more to Ethereum and the EVM ecosystem.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1377#discussion_r2623013233)














#### Review by
         -


      `master` ← `stevieraykatz:erc-associated-accounts`







Typo fix: `paries` should be `parties`.

---

**katzman** (2025-12-17):

Hey [@0xTraub](/u/0xtraub)  thanks for contributing to the conversation here! Here are some thoughts related to what you shared:

> Have you considered instead defining an interface and letting the members of the association specify a contract to use as the verifier that meets that interface

We have actually! The `DELEGATED` Key Type is intended to be used as the abstraction for enabling arbitrary contract-based validations. Take a look at the language used to describe authorization delegation and let me know if you think it needs massaging or is lacking critical information to achieve a similar solution as you laid out here.

> That way the struct then becomes…

I think it’s important for validation data to live external to the `AssociatedAccountRecord` details. The intent is for the wrapper struct `SignedAssociationRecord` to contain all of the necessary information to enable signature/auth validation. Moving the contract address into the record has two issues as I see it:

1. It requires that validation occur in an EVM context given the use of the address type (although the spec supports alternative architectures)
2. It requires that both accounts can authorize the same contract as a signing validator which seems overly constrained for combinations of accounts on disparate chains or architectures

All that being said, I am actively seeking feedback on the Key Types enumeration in the telegram channel and welcome your feedback!

---

**katzman** (2025-12-17):

Hey [@aliceto](/u/aliceto) thanks for the comment.

> If this is combined with ERC-8091, would it also be possible to associate privacy addresses with it?

So long as ERC-8091 addresses can be structured into an ERC-7930 address format, then they’re natively compatible with this specification. Since the ERC-8091 address schema is not eip155 compatible, I think a purpose built [CAIP-350](https://chainagnostic.org/CAIPs/caip-350) profile would be needed.

---

**0xTraub** (2025-12-17):

> The DELEGATED Key Type is intended to be used as the abstraction for enabling arbitrary contract-based validations.

That makes sense and I like that design but I still think the standard needs more explanation of how this can be accessed. The document only says

> Implementers leveraging the Delegated key type MUST also publish how consumers can parse the application-specific delegation schema.

without actually specifying where this is. I think the best way to do this would potentially be to require that the `data` field of the `AssociatedAccountRecord` to have some kind of formatting (JSON or YAML) that could then contain the address under a fixed header. Just an idea.

> It requires that validation occur in an EVM context given the use of the address type (although the spec supports alternative architectures)

I’m fine with changing this to a `bytes` field although that would also potentially require additional fields such as a `chainId` to declare which chain to validate on. However, this could also potentially be another field in a JSON “verifier” header.

```auto
"verifier": {
        contractAddress: "[insert address]",
        chainId: "[insert chainId]"
}
```

That would certainly allow for more flexibility in the future as well as across chain-families (EVM, SOL, MOVE, etc.)


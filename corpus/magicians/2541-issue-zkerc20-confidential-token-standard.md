---
source: magicians
topic_id: 2541
title: "Issue: zkERC20: Confidential Token Standard"
author: ligi
date: "2019-01-29"
category: EIPs
tags: [token, privacy, eip-1724]
url: https://ethereum-magicians.org/t/issue-zkerc20-confidential-token-standard/2541
views: 1192
likes: 4
posts_count: 1
---

# Issue: zkERC20: Confidential Token Standard

Posting this here to get some more eye balls on this and also as a follow-up to [Meta: we should value privacy more](https://ethereum-magicians.org/t/meta-we-should-value-privacy-more/2475)



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1724)












####



        opened 07:26PM - 25 Jan 19 UTC



          closed 08:13PM - 04 Dec 21 UTC



        [![](https://avatars.githubusercontent.com/u/1476668?v=4)
          zac-williamson](https://github.com/zac-williamson)





          stale







```
eip: 1724
title: Confidential Token Standard
author: AZTEC
discussions-t[…]()o: https://github.com/ethereum/EIPs/issues/1724
status: Draft
type: Standards Track
category: ERC
created: 2019-01-25
requires: 1723
```

## Simple Summary

This EIP defines the standard interface and behaviours of a confidential token contract, where ownership values and the values of transfers are encrypted.

## Abstract

This standard defines a way of interacting with a **confidential** token contract. Confidential tokens do not have traditional balances - value is represented by **notes**, which are composed of a public owner and an encrypted value. Value is transferred by splitting a note into multiple notes with different owners. Similarly notes can be combined into a larger note. Note splitting is analogous to the behaviour of Bitcoin UTXOs, which is a good mental model to follow.

These "join-split" transactions must satisfy a balancing relationship (the sum of the values of the old notes must be equal to the sum of the values of the new notes) - this can be proven via a zero-knowledge proof.

**This EIP was modelled on the zero-knowledge proofs enabled by the [AZTEC protocol](https://github.com/AztecProtocol/AZTEC/blob/master/AZTEC.pdf). However this specification is not specific to AZTEC and alternative technologies can be used to implement this standard, such as Bulletproofs or a zk-SNARK-based implementation**

## Motivation

The ability to transact in confidentiality is a requirement for many kinds of financial instruments. The motivation of this EIP is to establish a standard that defines how these confidential assets are constructed and traded. Similar to an ERC20 token, if confidential tokens conform to the same interface then this standard can be re-used by other on-chain applications, such as confidential decentralized exchanges or confidential escrow accounts.

The zkERC20 token interface is designed such that the economic beneficiary of any transaction is completely divorced from the transaction sender. This is to facilitate the use of one-time stealth addresses to "own" zero-knowledge notes. Such addresses will not easily be fundable with gas to pay for transactions (without leaking information). Creating a clear separation between the transaction sender and the economic beneficiary allows third party service layers to be tasked with the responsibility to sign transactions.

## Specification

An example zkERC20 token contract

```solidity
interface zkERC20 {
    event CreateConfidentialNote(address indexed _owner, bytes _metadata);
    event DestroyConfidentialNote(address indexed _owner, bytes32 _noteHash);

    function cryptographyEngine() external view returns (address);
    function confidentialIsApproved(address _spender, bytes32 _noteHash) external view returns (bool);
    function confidentialTotalSupply() external view returns (uint256);
    function publicToken() external view returns (address);
    function supportsProof(uint16 _proofId) external view returns (bool);
    function scalingFactor() external view returns (uint256);

    function confidentialApprove(bytes32 _noteHash, address _spender, bool _status, bytes _signature) public;
    function confidentialTransfer(bytes _proofData) public;
    function confidentialTransferFrom(uint16 _proofId, bytes _proofOutput) public;
}
```

The token contract must implement the above interface to be compatible with the standard. The implementation must follow the specifications described below.

### The fundamental unit of 'value' in a zk-ERC20: the zero-knowledge note

Unlike traditional balances, value is represented via an UXTO-style model represented by **notes**. A note has the following public information:

* A **public key**, that contains an encrypted representation of the note's value
* The Ethereum **address** of the note's 'owner'
* Note **metadata** - additional data required by the note owner, but is not used in any smart-contract logic

A note has the following private information:

* A **viewing key**, which can be used to decrypt the note
* A **spending key**
* A **value** - a representation of the number of tokens this note contains

### Public notes, private values: rationale behind the note construct

In order to enable cross-asset interoperability, we can hide the notionals in a given transaction, however **what** is being transacted is public, as well as the Ethereum addresses of the transactors.

This is to enable a high degree of interoperability between zero-knowledge assets - it is difficult to design a zero-knowledge DApp if one cannot identify the asset class of any given note.

The `owner` field of a note is public for ease-of-use as we want traditional Ethereum private keys to be able to sign against zero-knowledge notes, and zero-knowledge spending proofs. One can use a Monero-style stealth address protocol to ensure that the Ethereum address of a note's `owner` contains no identifying information about the note's true owner.

### The zero-knowledge note registry

A token that conforms to the zkERC20 standard must have a method of storing the token's set of **unspent** zero-knowledge notes. The Cryptography Engine identifies notes with the following tuple:

1. A `bytes32 _noteHash` variable, a `keccak256` hash of a note's encrypted data
2. A `address _owner` variable, an `address` that defines a note's owner
3. A `bytes _notedata` variable, the `notedata` is a combination of the note's public key and the note metadata. When implemented using the AZTEC protocol, `secp256k1` and `bn128` group elements that allows a note owner to recover and decrypt the note.

An example implementation of zkERC20 represents this as a mapping from `noteHash` to `owner`: `mapping(bytes32 => address) noteRegistry;`. The `metadata` is required for logging purposes only, the `noteHash` and `owner` variables alone are enough to define a unique note.

### View Functions

#### cryptographyEngine

```solidity
function cryptographyEngine() view returns (address)
```

This function returns the address of the smart contract that validates this token's zero-knowledge proofs. For the specification of the Cryptography Engine, please see [this ERC](https://github.com/ethereum/EIPs/issues/1723).

> <small>**returns:** address of the cryptography engine that validates this token's zero-knowledge proofs</small>

#### publicToken

```solidity
function publicToken() view returns (address)
```

This function returns the address of the public token that this confidential token is attached to. The public token should conform to the ERC20 token standard. This link enables a user to convert between an ERC20 token balance and confidential zkERC20 notes.

If the token has no public analogue (i.e. it is a purely confidential token) this method should return `0`.

> <small>**returns:** address of attached ERC20 token</small>

#### supportsProof

```solidity
function supportsProof(uint16 _proofId) view returns (bool)
```

This function returns whether this token supports a specific zero-knowledge proof ID. The Cryptography Engine can support a number of zero-knowledge proofs. The token creator may wish to only support a subset of these proofs.

The rationale behind using a `uint16` variable is twofold:

1. The total number of proofs supported by the engine will never grow to be larger than 65535
2. The purpose of the engine is to define a "grammar" of composable zero-knowledge proofs that can be used to define the semantics of confidential transactions and the total set will be quite small. Using an integer as a proofID allows for a simple bit-filter to validate whether a proof is supported or not (TODO put somewhere else).

> <small>**returns:** boolean that defines whether a proof is supported by the token</small>

#### confidentialTotalSupply

```solidity
function confidentialTotalSupply() view returns (uint256);
```

This function returns the total sum of tokens that are currently represented in zero-knowledge note form by the contract. This value must be equal to the sum of the values of all unspent notes, which is validated by the Cryptography Engine. Note that this function may leak privacy if there's only one user of the zkERC20 contract instance.

> <small>**returns:** the combined value of all confidential tokens</small>

#### scalingFactor

```solidity
function scalingFactor() view returns (uint256)
```

This function returns the token `scalingFactor`. The range of integers that can be represented in a note is likely smaller than the native word size of the EVM (~30 bits vs 256 bits). As a result, a scaling factor is applied when converting between public tokens and confidential note form. An ERC20 token value of `1` corresponds to an zkERC20 value of `scalingFactor`.

> <small>**returns:** the multiplier used when converting between confidential note values and public tokens</small>

### Approving Addresses to Transact Zero-Knowledge Notes

For confidential transactions to become truly useful, it must be possible for smart contracts to transact notes on behalf of their owners. For example a confidential decentralized exchange or a confidential investment fund. These transactions still require zero-knowledge proofs that must be constructed on-chain, but they can be constructed on behalf of note owners and validated against ECDSA signatures signed by note owners.

To this end, a `confidentialApprove` method is required to delegate.

#### confidentialApprove

```solidity
function confidentialApprove(bytes32 _noteHash, address _spender, bool _status, bytes _signature)
```

This function allows a note owner to approve the address `approved` to "spend" a zero-knowledge note in a `confidentialTransferFrom` transaction.

> <small>**parameters**</small>
> <small>`_noteHash`: the hash of the note being approved</small>
> <small>`_sender`: the address of the entity being approved</small>
> <small>`_status`: defines whether `approved` is being given permission to spend a note, or if permission is being revoked</small>
> <small>`_signature`: ECDSA signature from the note owner that validates the `confidentialApprove` instruction</small>

## Confidential Transfers

The action of sending confidential notes requires a zero-knowledge proof to be validated by the Cryptography Engine that a given zk-ERC20 contract listens to. The semantics of this proof will vary depending on the **proof ID**. For example, the zero-knowledge proof required to partially fill an order between two zero-knowledge assets and the zero-knowledge proof required for a unilateral "join-split" transaction are different proofs, with different validation logic. Every proof supported by the Cryptography Engine will share the following common feature:

* A **balancing relationship** has been satisfied - the sum of the values of the notes "to be created" equals the sum of the values of the notes "to be spent"

To validate a zero-knowledge proof, the token smart contract must call the Cryptography Engine's `validateProof(uint16 _proofId, bytes _proofData) public returns (bytes32[] _destroyedNotes, Note[] _createdNotes, address _publicOwner, int256 _publicValue)` function. This method will throw an error if the proof is invalid. If the proof is *valid*, the following data is returned:

> <small>**createdNotes:** the array of notes the proof wishes to create</small>
> <small>**destroyedNotes:** the array of notes the proof wishes to destroy</small>
> <small>**publicOwner:** if a public conversion is required, this is the address of the public token holder</small>
> <small>**publicValue:** if a public conversion is required, this is the amount of tokens to be transferred to the public token holder. Can be negative, which represents a conversion from the public token holder to the zkERC20 contract</small>

The structure of `Note` is the following:

```solidity
struct Note {
    address owner;
    bytes32 noteHash;
    bytes noteData;
}
```

The above information can be used by the zkERC20 token to validate the **legitimacy** of a confidential transfer.

### Direct Transactions

Basic "unilateral" transfers of zero-knowledge notes are enabled via a "join-split"-style transaction, accessed via the `confidentialTransfer` method.

#### confidentialTransfer

```solidity
function confidentialTransfer(bytes proofData)
```

This function is designed as an analogue to the ERC20 `transfer` method.

To enact a `confidentialTransfer` method call, the token contract must check and perform the following:

1. Successfully execute `cryptographyEngine.validateProof(1, proofData)`
   * If this proof is valid, then for every note being consumed in the transaction, the note owner has provided a satisfying ECDSA signature
2. Examine the output of `cryptographyEngine.validateProof` `(createdNotes, destroyedNotes, publicOwner, publicValue)` and validate the following:
   1. Every `Note` in `destroyedNotes` exists in the token's note registry
   2. Every `Note` in `createdNotes` does **not** exist in the token's note registry

If the above conditions are satisfied, the following steps must be performed:

1. If `publicValue < 0`, call `erc20Token.transferFrom(publicOwner, this, uint256(-publicValue))`. If this call fails, abort the transaction
2. If `publicValue > 0`, call `erc20Token.transfer(publicOwner, uint256(publicValue))`
3. Update the token's total confidential supply to reflect the above transfers
4. For every `Note` in `destroyedNotes`, remove `Note` from the token's note registry and emit `DestroyConfidentialNote(Note.owner, Note.noteHash)`
5. For every `Note` in `createdNotes`, add `Note` to the token's note registry and emit `CreateConfidentialNote(Note.owner, Note.metadata)`
6. Emit the `ConfidentialTransfer` event.

### Autonomous Transactions

For more exotic forms of transfers, mediated by smart contracts, the `confidentialTransferFrom` method is used.

#### confidentialTransferFrom

```solidity
function confidentialTransferFrom(uint16 _proofId, bytes _proofOutput);
```

This function enacts a confidential transfer of zero-knowledge notes. This function is designed as an analogue to the ERC20 `transferFrom` method, to be called by smart contracts that enact confidential transfers.

Instead of supplying a zero-knowledge proof to be validated, this method is supplied with a **transfer instruction** that was generated by the Cryptography Engine that this asset listens to. This is to aid in preventing redundant validation of zero-knowledge proofs - some types of proof produce multiple transfer instructions (e.g. a `bilateral-swap` style proof in the [Cryptography Engine](https://github.com/ethereum/EIPs/issues/1723) standard).

The `bytes _proofOutput` variable MUST conform to the specification of a 'proof output' from the Cryptography Engine standard. A valid `_proofOutput` will contain the following data: `bytes inputNotes`, `bytes outputNotes`, `address publicOwner`, `int256 publicValue`

To enact a `confidentialTransferFrom` method call, the token contract must check and perform the following:

1. The `proofId` must correspond to a proof supported by the token
2. Construct the `bytes32 proofHash`, a keccak256 hash of `bytes _proofOutput`
3. Call `cryptographyEngine.validateProofByHash(proofId, proofHash, msg.sender)`
4. If `validateProofByHash` returns `false` the transaction MUST throw
5. If `validateProofByHash` returns `true`, the following MUST be validated
   1. Every `Note` in `inputNotes` exists in the token's note registry
   2. Every `Note` in `outputNotes` does **not** exist in the token's note registry
   3. For every `Note` in `outputNotes`, `confidentialIsApproved(noteHash, owner)` returns `true`

If the above conditions are satisfied, the following steps must be performed:

1. If `publicValue < 0`, call `erc20Token.transferFrom(publicOwner, address(this), uint256(-publicValue))`. If this call fails, abort the transaction
2. If `publicValue > 0`, call `erc20Token.transfer(publicOwner, uint256(publicValue))`
3. Update the token's total confidential supply to reflect the above transfers
4. For every `Note` in `destroyedNotes`, remove `Note` from the token's note registry and emit `DestroyConfidentialNote(Note.owner, Note.noteHash)`
5. For every `Note` in `createdNotes`, add `Note` to the token's note registry and emit `CreateConfidentialNote(Note.owner, Note.metadata)`
6. Emit the `ConfidentialTransfer` event.

### Events

#### CreateConfidentialNote

```solidity
event CreateConfidentialNote(address indexed _owner, bytes_metadata)
```

An event that logs the creation of a note against the note owner and the note metadata.

> <small>**parameters**</small>
> <small>`_owner`: The Ethereum address of the note owner</small>
> <small>`_metadata`: Data required by the note owner to recover and decrypt their note</small>

#### DestroyConfidentialNote

```solidity
event DestroyConfidentialNote(address indexed _owner)
```

An event that logs the destruction of a note against the note owner and the note metadata.

> <small>**parameters**</small>
> <small>`_owner`: The ethereum address of the note owner</small>
> <small>`_noteHash`: The hash of the note. Note `metadata` can be recovered from the `DestroyConfidentialNote` event that created this note</small>

## Implementation

Head to [the AZTEC monorepo](https://github.com/AztecProtocol/AZTEC) for a work in progress implementation. Many thanks to @PaulRBerg, @thomas-waite, @ArnSch and the @AztecProtocol team for their contributions to this document.

## Copyright
Work released under [LGPL-3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html).

---
source: magicians
topic_id: 27277
title: "Draft ERC: Privacy-Preserving Receiving via Stealth Addresses (ERC-8065 Extension)"
author: ZyraV21
date: "2025-12-22"
category: ERCs
tags: [erc, evm, wallet, zk]
url: https://ethereum-magicians.org/t/draft-erc-privacy-preserving-receiving-via-stealth-addresses-erc-8065-extension/27277
views: 250
likes: 8
posts_count: 9
---

# Draft ERC: Privacy-Preserving Receiving via Stealth Addresses (ERC-8065 Extension)

---

## title: Stealth Addresses for Zero Knowledge Token Wrappers
description: Extension to ERC-8065 enabling privacy-preserving receiving via ECDH-based stealth addresses
author: Zyra V-21 (), doublespending ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2025-12-18
requires: 8065

## Abstract

This ERC extends [ERC-8065](https://github.com/ethereum/ERCs/pull/1322) (Zero Knowledge Token Wrapper) by standardizing **stealth addresses** for receiving funds without sharing note secrets. Using Elliptic Curve Diffie-Hellman (ECDH) key exchange, senders can create notes for recipients who can later discover and spend them by scanning on-chain events—without any off-chain coordination.

## Motivation

ERC-8065 enables private token transfers, but receiving funds requires either:

1. Sharing secrets off-chain: The sender must know the recipient’s secret/nullifier to create a note
2. Using burn addresses: The recipient generates a provable burn address and shares it

Both approaches require coordination between sender and receiver before the transaction. This creates friction and limits use cases like:

- Anonymous donations
- Private payroll systems
- Merchant payments without customer interaction
- Protocol rewards distribution

### Stealth Address Solution

Stealth addresses (inspired by Railgun) solve this by allowing receivers to publish a **single public address** that senders can use to create notes. The receiver scans blockchain events to discover incoming funds using only their private viewing key.

| Approach | Coordination Required | Privacy |
| --- | --- | --- |
| Share secrets | High (off-chain exchange) | Note data exposed to sender |
| Burn addresses | Medium (generate per tx) | Good |
| Stealth addresses | None (publish once) | Excellent |

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

### Stealth Address Format

A stealth address consists of two public keys:

```auto
stealthAddress = encode(masterPublicKey, viewingPublicKey)
```

Where:

- masterPublicKey: Used in commitment generation, derived from masterPrivateKey
- viewingPublicKey: Used for ECDH scanning, derived from viewingPrivateKey

The encoding format is implementation-defined but SHOULD be human-readable (e.g., Bech32, Base58).

### Key Derivation

Receivers SHOULD derive keys as follows:

```auto
masterPrivateKey = random() or derive(seed, "master")
masterPublicKey = masterPrivateKey * G

viewingPrivateKey = random() or derive(seed, "viewing")
viewingPublicKey = viewingPrivateKey * G

nullifyingKey = Poseidon(masterPrivateKey, viewingPrivateKey)
```

Where `G` is the generator point of BabyJubjub curve (ZK-friendly).

### Interface

Compliant contracts MUST implement the following interface, compatible with ERC-8065:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title IERC8065StealthAddress
 * @notice Extension interface for ERC-8065 stealth address support
 * @dev Uses generic deposit/withdraw with stealth-specific data encoding
 */
interface IERC8065StealthAddress {
    // ============ EVENTS ============

    /// @notice Emitted when tokens are deposited to a stealth address
    /// @param commitment Note commitment inserted into Merkle tree
    /// @param recipientIndex keccak256(recipientMasterPubKey)[:20] for event filtering
    /// @param leafIndex Index in the Merkle tree
    /// @param assetId Asset identifier
    /// @param timestamp Block timestamp
    /// @param ciphertext Encrypted note data for receiver scanning
    /// @param ephemeralPubKey Sender's ephemeral public key for ECDH
    event Deposit(
        bytes32 indexed commitment,
        address indexed recipientIndex,
        uint32 leafIndex,
        uint256 indexed assetId,
        uint256 timestamp,
        bytes ciphertext,
        bytes32 ephemeralPubKey
    );

    /// @notice Emitted when a private transfer occurs (extends ERC-8065 base event)
    /// @param nullifierHash Nullifier marking input note as spent
    /// @param newCommitment New note commitment for recipient
    /// @param assetId Asset being transferred
    /// @param newLeafIndex Index of new commitment in Merkle tree
    /// @param recipientIndex keccak256(newRecipientMasterPubKey)[:20] for event filtering
    /// @param ciphertext Encrypted note data for new receiver
    /// @param ephemeralPubKey Sender's ephemeral public key for ECDH
    event PrivateTransfer(
        bytes32 indexed nullifierHash,
        bytes32 indexed newCommitment,
        uint256 indexed assetId,
        uint32 newLeafIndex,
        address recipientIndex,
        bytes ciphertext,
        bytes32 ephemeralPubKey
    );

    /// @notice Emitted when a note is withdrawn
    event Withdraw(
        bytes32 indexed nullifierHash,
        address indexed recipient,
        uint256 indexed assetId
    );

    // ============ ERRORS ============

    error ZeroAmount();
    error InvalidProof();
    error NullifierAlreadyUsed(bytes32 nullifier);
    error UnknownMerkleRoot(bytes32 root);
    error InvalidRecipient();
    error AssetNotRegistered(uint256 assetId);

    // ============ DEPOSIT (ERC-8065 Compatible) ============

    /**
     * @notice Deposit tokens to a stealth address
     * @dev Includes encrypted note data for receiver scanning
     *
     * @param to Recipient index: address(bytes20(keccak256(recipientMasterPubKey)))
     *           Enables efficient event filtering for note scanning
     * @param id Asset identifier (0 for ETH)
     * @param amount Amount to deposit
     * @param data Encoded: abi.encode(commitment, ciphertext, ephemeralPubKey, proof)
     */
    function deposit(
        address to,
        uint256 id,
        uint256 amount,
        bytes calldata data
    ) external payable;

    // ============ PRIVATE TRANSFER (ERC-8065 Compatible) ============

    /**
     * @notice Transfer between stealth addresses
     * @dev Extends base ERC-8065 privateTransfer with stealth data
     * @param proof ZK proof of ownership via nullifyingKey
     * @param nullifierHash Hash preventing double-spend
     * @param newCommitment New note commitment for recipient
     * @param root Merkle root for verification
     * @param assetId Asset being transferred
     * @param data Encoded stealth data: abi.encode(recipientIndex, ciphertext, ephemeralPubKey)
     *             - recipientIndex: address - keccak256(newRecipientMasterPubKey)[:20]
     *             - ciphertext: bytes - Encrypted note data for receiver scanning
     *             - ephemeralPubKey: bytes32 - Sender's ephemeral public key for ECDH
     */
    function privateTransfer(
        bytes calldata proof,
        bytes32 nullifierHash,
        bytes32 newCommitment,
        bytes32 root,
        uint256 assetId,
        bytes calldata data
    ) external;

    // ============ WITHDRAW (ERC-8065 Compatible) ============

    /**
     * @notice Withdraw to public address
     * @param to Recipient address
     * @param id Asset identifier
     * @param amount Amount to withdraw
     * @param data Encoded: abi.encode(root, nullifierHash, proof)
     */
    function withdraw(
        address to,
        uint256 id,
        uint256 amount,
        bytes calldata data
    ) external;

    // ============ VIEW FUNCTIONS ============

    function isKnownRoot(bytes32 root) external view returns (bool);
    function getLastRoot() external view returns (bytes32);
    function isNullifierUsed(bytes32 nullifier) external view returns (bool);
    function isAssetRegistered(uint256 assetId) external view returns (bool);
    function totalNotesCreated() external view returns (uint64);
    function getAssetBalance(uint256 assetId) external view returns (uint256);
    function ETH_ASSET_ID() external view returns (uint256);
}
```

### Data Encoding

**For deposit (stealth):**

```solidity
data = abi.encode(
    bytes32 commitment,      // Note commitment
    bytes ciphertext,        // Encrypted note data for scanning
    bytes32 ephemeralPubKey, // Sender's ephemeral key for ECDH
    bytes proof              // ZK proof
)
```

**For withdraw:**

```solidity
data = abi.encode(bytes32 root, bytes32 nullifierHash, bytes proof)
```

**For privateTransfer (stealth):**

```solidity
data = abi.encode(
    address recipientIndex,  // keccak256(recipientMasterPubKey)[:20]
    bytes ciphertext,        // Encrypted note data for scanning
    bytes32 ephemeralPubKey  // Sender's ephemeral key for ECDH
)
```

### Recipient Identifier (to parameter)

For stealth deposits, the `to` parameter MUST be derived from the recipient’s master public key:

```solidity
to = address(bytes20(keccak256(recipientMasterPubKey)))
```

This enables receivers to efficiently filter `Deposit` events by their pubKey hash without downloading and attempting decryption on every event in the contract’s history.

### Commitment Scheme

The commitment scheme is **implementation-defined**. Example:

```auto
notePublicKey = Poseidon(receiverMasterPublicKey, random)
commitment = Poseidon(notePublicKey, tokenHash, amount, assetId)
```

### Nullifier Derivation

Unlike standard notes, stealth notes use:

```auto
nullifierHash = Poseidon(nullifyingKey, leafIndex)
```

Where `nullifyingKey = Poseidon(masterPrivateKey, viewingPrivateKey)`.

This ensures only the owner of both private keys can spend the note.

### Encrypted Note Format

The `ciphertext` field MUST contain AES-256-GCM encrypted data:

```auto
sharedSecret = ECDH(ephemeralPrivateKey, receiverViewingPublicKey)
encryptionKey = HKDF(sharedSecret, "erc8065-stealth")
ciphertext = AES-GCM(encryptionKey, noteData)
```

The `noteData` payload SHOULD contain at minimum:

- random: The random value used in notePublicKey
- receiverMasterPublicKey: For ownership verification

### Receiver Scanning Process

To discover incoming notes, receivers:

1. Fetch Deposit and PrivateTransfer events filtered by recipientIndex
2. For each event, compute sharedSecret = ECDH(viewingPrivateKey, ephemeralPubKey)
3. Derive encryptionKey = HKDF(sharedSecret, "erc8065-stealth")
4. Attempt decryption of ciphertext
5. If decryption succeeds AND noteData.masterPublicKey == myMasterPublicKey:

The note belongs to this receiver
6. Store random, leafIndex for spending

**Efficient Filtering**: The `recipientIndex` indexed parameter allows receivers to filter events by their pubKey hash, avoiding the need to download and attempt decryption on every event.

### Curve Requirements

Implementations SHOULD use **BabyJubjub** curve for ECDH operations due to ZK-SNARK compatibility.

## Rationale

### Why Two Keys (Master + Viewing)?

Separation allows:

- Viewing key: Can be shared with auditors for balance monitoring without spending rights
- Master key: Required for spending, kept offline for security

### Why On-Chain Encrypted Notes?

On-chain encrypted notes provide the best balance of privacy and usability—no off-chain coordination needed.

### Relationship to ERC-5564

ERC-5564 defines stealth addresses for standard Ethereum transactions. This extension differs by:

- Operating within ZK commitment schemes
- Using BabyJubjub for ZK compatibility
- Integrating with ERC-8065 wrapper ecosystem

## Backwards Compatibility

This extension is additive to ERC-8065:

- Uses same deposit and withdraw function signatures
- Stealth events include additional fields (ciphertext, ephemeralPubKey)
- Contracts MAY implement both standard and stealth deposit

## Extensions

This ERC provides a foundation for additional privacy features that leverage the stealth address infrastructure:

### Encrypted Messaging

Users with stealth addresses already possess the cryptographic keys (master + viewing) needed for private messaging. A companion extension standardizes `sendMessage` functionality for gas-efficient (~50k gas) communication between stealth address holders without value transfer.

**Note**: For payments with memos, the `ciphertext` field in standard deposits already supports arbitrary data. The messaging extension addresses pure communication use cases.

## Test Cases

1. Stealth Deposit: Alice deposits to Bob’s stealth address → event contains encrypted note Bob can decrypt
2. Scanning: Bob scans events filtered by his recipientIndex, decrypts with viewingKey, finds his note
3. Private Transfer: Bob transfers to Carol’s stealth address → Carol can filter and decrypt the new note
4. Spending: Bob generates proof using nullifyingKey, withdraws
5. Wrong Viewer: Dave cannot decrypt Bob’s or Carol’s encrypted notes

## Reference Implementation

See: [zkWrapper0zk Demo](https://zkwrapper.vercel.app)

## Collaboration

This proposal is being developed in active collaboration with [@doublespeding](https://github.com/doublespeding), the author of [ERC-8065](https://github.com/ethereum/ERCs/pull/1322). We welcome community feedback and discussion on potential improvements to the stealth address mechanism, event indexing strategies, and integration patterns with the base ERC-8065 specification.

## Security Considerations

### Viewing Key Exposure

If `viewingPrivateKey` is compromised:

- Attacker can identify all incoming notes
- Attacker CANNOT spend notes (requires masterPrivateKey)

### Encrypted Note Size

Larger payloads increase gas costs. Implementations SHOULD use fixed-size padded payloads.

### Replay Attacks

The `ephemeralPubKey` MUST be unique per deposit.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**ivanmmurcia** (2025-12-23):

You’re joining two wonderful worlds. DKSAP + ZK Token Wrapper… this is absolutely amazing.

---

**ZyraV21** (2025-12-26):

We will open a repository in the upcoming days, we will publish there the contracts used on the live demo + clientside prover,   so everyone can play around and try it ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

P.D: Happy holidays everyone

---

**stateroot** (2025-12-26):

Privacy can be composed like DeFi Legos.

---

**ZyraV21** (2025-12-26):

This is indeed a nice analogy! In fact we are kind of building more ‘lego pieces’ for 8065!

---

**ZyraV21** (2026-01-06):

## Update: Interface Refinement for ERC-8065 Compatibility

After further review and implementation work, we’ve refined the interface to maintain **strict compatibility** with the base ERC-8065 specification. The key change:

### privateTransfer Signature Change

**Previous version** (published Dec 18):

```solidity
function privateTransfer(
    bytes calldata proof,
    bytes32 nullifierHash,
    bytes32 newCommitment,
    bytes32 root,
    uint256 assetId,
    address recipientIndex,      // Direct parameters
    bytes calldata ciphertext,
    bytes32 ephemeralPubKey
) external;
```

**Updated version** (current):

```solidity
function privateTransfer(
    bytes calldata proof,
    bytes32 nullifierHash,
    bytes32 newCommitment,
    bytes32 root,
    uint256 assetId,
    bytes calldata data          // Encoded stealth data
) external;
```

Where `data = abi.encode(recipientIndex, ciphertext, ephemeralPubKey)`

### Rationale

This change follows the **same pattern** as `deposit()` and `withdraw()` in ERC-8065, which use a generic `bytes calldata data` parameter for extensibility. Benefits:

1. Consistent API: All three functions (deposit, withdraw, privateTransfer) now use the same encoding pattern
2. Future-proof: Additional stealth metadata can be added without breaking the interface
3. Base compatibility: Non-stealth implementations can ignore the data parameter

### Event Changes

The `PrivateTransfer` event now matches the base ERC-8065 indexed parameters:

- Indexed: nullifierHash, newCommitment, assetId (same as base)
- Non-indexed: newLeafIndex, recipientIndex, ciphertext, ephemeralPubKey (stealth extensions)

This ensures event filtering compatibility with base ERC-8065 tooling while adding stealth-specific fields for scanning.

---

**GITHUB Repository**: [zkWrapper0zk.sol](https://github.com/Zyra-V21/DRAFT-ERC-Stealth-Addresses-for-Zero-Knowledge-Token-Wrappers)

We believe this refinement strengthens the proposal’s integration with ERC-8065 while maintaining all stealth address functionality. Feedback welcome!

---

**doublespending** (2026-01-16):

Currently, ERC-8065 supports a **burn-and-remint** privacy flow. In practice, there are other privacy flows as well, such as **stealth addresses**.

This proposal aims to support stealth addresses on top of ERC-8065, making ERC-8065 more complete and compatible with the widely adopted stealth-address workflow.

---

**stateroot** (2026-01-17):

I’m curious about the advantages of supporting stealth addresses on top of the ERC-8065 interface. Since an ERC-20 token, after being wrapped by ERC-8065, is still an ERC-20, it should be sufficient to support it in existing stealth-address applications just like any standard ERC-20.

---

**ZyraV21** (2026-01-19):

Great question! Let me clarify the key differences:

## ERC-5564 (Standard Stealth Addresses)

ERC-5564 generates **unlinkable receiving addresses** for standard ERC-20/ETH transfers:

- Who receives: Hidden (stealth address not linked to recipient’s public identity)
- Amount: Visible on-chain (standard ERC-20 transfer amounts are public)
- Timing: Visible on-chain (transaction timestamp public)
- Traceability: Funds can be traced through the chain (no anonymity set)

**Use case**: Receiving donations without revealing your identity, but amounts and timing are public.

---

## ERC-8065 + Stealth Addresses (This Extension)

Combines **commitment-based privacy** (ERC-8065) with **non-interactive receiving** (stealth addresses):

### Privacy Layers:

1. Who receives: Hidden via stealth addresses (like ERC-5564)
2. Amount: Hidden via fixed denominations + commitments in Merkle tree
3. Timing: Obfuscated within the anonymity set
4. Traceability: Broken - transfers occur within shared Merkle tree (anonymity set like Tornado Cash)

### Non-Interactive Receiving:

- Base ERC-8065 requires off-chain coordination (share note secrets or generate burn addresses)
- This extension adds stealth addresses: publish once, receive forever (no coordination)

---

## Why Both Are Needed

| Feature | ERC-5564 Alone | ERC-8065 Base | ERC-8065 + Stealth |
| --- | --- | --- | --- |
| Hide recipient identity |  | (needs coordination) |  |
| Hide amount |  |  |  |
| Hide timing/pattern |  |  |  |
| Anonymity set |  |  |  |
| Non-interactive receiving |  |  |  |

**TL;DR**: ERC-5564 hides *who*. ERC-8065 hides *what/when*. This extension combines both for **full transaction privacy without coordination**.

Does this clarify the distinction?


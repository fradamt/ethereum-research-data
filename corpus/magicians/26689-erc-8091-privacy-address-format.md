---
source: magicians
topic_id: 26689
title: "ERC-8091: Privacy Address Format"
author: zero
date: "2025-11-24"
category: ERCs
tags: [erc, token, wallet, zkp, privacy]
url: https://ethereum-magicians.org/t/erc-8091-privacy-address-format/26689
views: 534
likes: 11
posts_count: 6
---

# ERC-8091: Privacy Address Format

Discussion topic for ERC-8091:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1373)














####


      `master` ← `0xRowan:erc-privacy-address-format`




          opened 07:08AM - 24 Nov 25 UTC



          [![](https://avatars.githubusercontent.com/u/199686996?v=4)
            0xRowan](https://github.com/0xRowan)



          [+653
            -0](https://github.com/ethereum/ERCs/pull/1373/files)







This EIP defines a standardized client-side privacy address format for privacy-p[…](https://github.com/ethereum/ERCs/pull/1373)reserving tokens on Ethereum. The format uses a versioned prefix (`pv` + version number) to support cryptographic evolution and future upgrades.

**Privacy Version 1 (pv1)** is the initial version defined by this standard, using the Baby Jubjub elliptic curve for zk-SNARK optimization. Future versions (pv2, pv3, etc.) MAY adopt different cryptographic schemes, such as post-quantum resistant algorithms.

The format is designed for privacy-preserving token protocols, including native privacy tokens, dual-mode tokens, and wrapper protocols that add privacy capabilities to existing [ERC-20](./eip-20) tokens.

**Key Characteristics**:

- **Client-side specification**: Address generation and parsing are performed entirely off-chain without smart contract interaction
- **Version support**: The "pv" prefix followed by version number (pv1, pv2, pv3) allows future upgrades for new cryptographic schemes or post-quantum resistance
- **Three-key architecture**: Separate spend, scan, and encryption public keys for fine-grained permission control
- **zk-SNARK optimization**: Baby Jubjub elliptic curve for efficient zero-knowledge proof generation
- **Multi-chain support**: Single-character network codes supporting 58+ EVM-compatible chains
- **Compact encoding**: Base58 compression with FNV-1a checksum for error detection
- **Wrapper protocol compatible**: Applicable to wrapper protocol that adds privacy capabilities to existing [ERC-20](./eip-20) tokens (e.g., DAI → zDAI)

By standardizing the privacy address format at the client level, this proposal enables interoperability between privacy-preserving dApps and seamless privacy asset transfers across the Ethereum ecosystem.












## Abstract

This EIP defines a standardized client-side privacy address format for privacy-preserving tokens on Ethereum. The format uses a versioned prefix (`pv` + version number) to support cryptographic evolution and future upgrades.

**Privacy Version 1 (pv1)** is the initial version defined by this standard, using the Baby Jubjub elliptic curve for zk-SNARK optimization. Future versions (pv2, pv3, etc.) MAY adopt different cryptographic schemes, such as post-quantum resistant algorithms.

The format is designed for privacy-preserving token protocols, including native privacy tokens ([ERC-8086](https://ethereum-magicians.org/t/erc-8086-privacy-token/26623)) , dual-mode tokens([ERC-8085](https://ethereum-magicians.org/t/erc-8085-dual-mode-fungible-tokens/26592)), and wrapper protocols that add privacy capabilities to existing ERC-20 tokens.

**Key Characteristics**:

- Client-side specification: Address generation and parsing are performed entirely off-chain without smart contract interaction
- Version support: The “pv” prefix followed by version number (pv1, pv2, pv3) allows future upgrades for new cryptographic schemes or post-quantum resistance
- Three-key architecture: Separate spend, scan, and encryption public keys for fine-grained permission control
- zk-SNARK optimization: Baby Jubjub elliptic curve for efficient zero-knowledge proof generation
- Multi-chain support: Single-character network codes supporting 58+ EVM-compatible chains
- Compact encoding: Base58 compression with FNV-1a checksum for error detection
- Wrapper protocol compatible: Applicable to wrapper protocol that adds privacy capabilities to existing ERC-20 tokens (e.g., DAI → zDAI)

By standardizing the privacy address format at the client level, this proposal enables interoperability between privacy-preserving dApps and seamless privacy asset transfers across the Ethereum ecosystem.

## Motivation

### Completing the Privacy Ecosystem

Privacy token protocols typically define interfaces for commitments, nullifiers, and note encryption, but leave the **address format** unspecified.

Without a standardized privacy address format:

- Each dApp implements custom address encoding, leading to ecosystem fragmentation
- Privacy assets cannot flow between different privacy dApps
- Users need different addresses for different protocols
- Wallets must implement custom logic for each privacy implementation

### The Interoperability Problem

Consider these real-world scenarios that are currently impossible:

**Scenario 1: Cross-dApp Privacy Transfers**

```auto
User has privacy assets in dApp_A, wants to use them in dApp_B
Without pv1: Each dApp uses incompatible address formats
With pv1: Unified address format enables seamless transfers
```

**Scenario 2: ENS Privacy Payments**

```auto
Alice wants to receive private payments at alice.eth
With pv1: alice.eth can be associated with pv1MSxxxxxxxx
```

### Why Not Use ?

ERC-5564 (Stealth Addresses) is a valuable standard for general-purpose stealth addresses. While ERC-5564’s schemeId mechanism could theoretically support different elliptic curves, the fundamental architectural differences make pv1 better suited for native privacy asset ecosystems:

| Aspect | ERC-5564 | pv1 |
| --- | --- | --- |
| Key Structure | 2 keys (viewing + spending) | 3 keys (spend + scan + encryption) |
| Permission Granularity | Binary (view all or nothing) | Granular (scan, decrypt, spend separately) |
| Encoding | Hex (st:eth:0x…) | Base58 with checksum (pv1…) |
| Checksum | None | FNV-1a (error detection) |
| Version Support | schemeId (on-chain routing) | Prefix-based (pv1/pv2/pv3 in address) |
| Designed For | General stealth addresses | Native privacy assets (IZRC20) |

**The three-key architecture is the core differentiator**: it enables granular permission control by selectively sharing private keys:

- Audit-only access: Share scanPrivateKey only (can detect transactions, but not amounts)
- Accounting access: Share scanPrivateKey + encryptionPrivateKey (full read-only visibility)
- Full control: All three private keys (can spend funds)

This granularity is not possible with ERC-5564’s two-key model.

For protocols using zero-knowledge proofs, pv1 uses the Baby Jubjub curve which provides better performance in zk-SNARK circuits due to its native compatibility with the BN254 scalar field.

### Why Version Support Matters

The “pv” prefix stands for “Privacy Version”, with “pv1” indicating version 1 of the format. This versioning enables:

1. Elliptic curve upgrades: pv1 uses Baby Jubjub; future versions can adopt different curves
2. Post-quantum migration: When quantum-resistant cryptography matures, pv2 could use lattice-based schemes
3. Backward compatibility: Wallets can support multiple versions simultaneously
4. Gradual ecosystem migration: No forced upgrades; users choose when to migrate

### Design Philosophy

This standard embraces the principle: **“Privacy addresses should be as usable as regular addresses.”**

Key design goals:

1. Human-readable: Compact enough to share via messaging apps
2. Error-resistant: Checksum prevents typos from losing funds
3. Permission-granular: Three-key architecture enables selective disclosure
4. Future-proof: Versioned format and extensible codes
5. Off-chain first: No blockchain interaction required for address operations

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Definitions

- pv1 Address: A privacy address string in the format pv[V][N][CompressedData][Checksum]
- Privacy Version: The “pv” prefix followed by version number (1, 2, 3, etc.)
- Spend Public Key: Used by senders to derive stealth addresses for recipients
- Scan Public Key: Used by senders to compute shared secrets and view tags
- Encryption Public Key: Used by senders to encrypt note data for recipients
- Network Code: Single Base58 character identifying the blockchain network
- Compressed Data: Base58-encoded, point-compressed public keys
- Checksum: 4-character FNV-1a hash for error detection

### Address Format

```auto
pv[V][N][CompressedData][Checksum]

┌──────┬─────────┬─────────┬──────────────────┬──────────┐
│  pv  │    V    │    N    │  CompressedData  │ Checksum │
├──────┼─────────┼─────────┼──────────────────┼──────────┤
│ 2 ch │  1 char │  1 char │  Variable Base58 │  4 char  │
│Prefix│ Version │ Network │    Public Keys   │  Base58  │
└──────┴─────────┴─────────┴──────────────────┴──────────┘

- pv: Privacy Version prefix
- V: Version number (1, 2, 3, etc.) - pv1 uses Baby Jubjub curve
- N: Network code (M=mainnet, P=polygon, etc.)
```

### Network Codes

Implementations MUST support at least the following network codes:

| Network | Code | Chain ID | Description |
| --- | --- | --- | --- |
| Ethereum Mainnet | M | 1 | Primary deployment |
| Base Sepolia | T | 84532 | Testing networks |
| Polygon | P | 137 | Polygon PoS |
| Arbitrum | A | 42161 | Arbitrum One |
| Base | B | 8453 | Base L2 |
| Optimism | O | 10 | Optimism L2 |
| Avalanche | V | 43114 | Avalanche C-Chain |
| BNB Chain | S | 56 | BNB Smart Chain |
| Gnosis | G | 100 | Gnosis Chain |

Additional network codes MAY be defined. The Base58 character set allows up to 58 unique network codes.

### Cryptographic Parameters

#### Elliptic Curve

For pv1, implementations MUST use the Baby Jubjub curve defined over the BN254 scalar field:

```auto
Curve: Twisted Edwards
Equation: ax² + y² = 1 + dx²y²
Parameters:
  a = 168700
  d = 168696
  p = 21888242871839275222246405745257275088548364400416034343698204186575808495617

Subgroup order (for scalars):
  l = 2736030358979909402780800718157159386076813972158567259200215660948447373041
```

This curve has cofactor 8. Implementations using circomlibjs SHOULD use `babyJub.Base8` as the generator point, which generates the prime-order subgroup of l points and avoids small subgroup attacks.

This curve is compatible with circomlib and other zk-SNARK tooling.

Future versions (pv2, pv3, etc.) MAY adopt different elliptic curves as cryptographic needs evolve, such as post-quantum resistant curves or curves optimized for different proof systems.

#### Point Compression

Public keys MUST be compressed using the following algorithm:

1. For point (x, y), store only x-coordinate (256 bits)
2. Store y-coordinate parity as a single bit (odd = 1, even = 0)
3. Pack three keys with parity flags into a single integer:

```auto
packedData = (flags >> 0; // FNV-1a prime
    }

    // Clamp to 4-character Base58 range
    const maxHash = 58**4 - 1;
    return toBase58(hash % maxHash, 4);
}
```

### Client-Side Operations

All pv1 address operations are performed client-side without blockchain interaction:

#### Address Generation

```javascript
function generatePv1Address(spendPubKey, scanPubKey, encryptPubKey, network) {
    // 1. Validate inputs
    validateNetwork(network);
    validatePoint(spendPubKey);
    validatePoint(scanPubKey);
    validatePoint(encryptPubKey);

    // 2. Compress public keys
    const compressedData = compressPublicKeys(spendPubKey, scanPubKey, encryptPubKey);

    // 3. Assemble address
    const networkCode = NETWORK_CODES[network];
    const baseData = `pv1${networkCode}${compressedData}`;

    // 4. Calculate checksum
    const checksum = calculateChecksum(baseData);

    return baseData + checksum;
}
```

#### Address Parsing

```javascript
function parsePv1Address(pv1Address) {
    // 1. Validate prefix and length
    if (!pv1Address.startsWith('pv1') || pv1Address.length < 10) {
        throw new Error('Invalid pv1 address format');
    }

    // 2. Extract components
    const networkCode = pv1Address[3];
    const checksum = pv1Address.slice(-4);
    const compressedData = pv1Address.slice(4, -4);

    // 3. Verify checksum
    const baseData = pv1Address.slice(0, -4);
    const expectedChecksum = calculateChecksum(baseData);
    if (checksum !== expectedChecksum) {
        throw new Error('Invalid checksum');
    }

    // 4. Validate network code
    if (!REVERSE_NETWORK_CODES[networkCode]) {
        throw new Error('Invalid network code');
    }

    // 5. Decompress public keys
    const publicKeys = decompressPublicKeys(compressedData);

    return {
        version: 1,
        network: REVERSE_NETWORK_CODES[networkCode],
        ...publicKeys
    };
}
```

## Replies

**zero** (2025-11-25):

I’ve implemented ERC-8086 Native Privacy Asset Protocol with PV1 address support, currently live on Base Sepolia.



    ![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/z/a88e57/48.png)

      [ERC-8086: Privacy Token](https://ethereum-magicians.org/t/erc-8086-privacy-token/26623) [ERCs](/c/ercs/57)




> Discussion topic for ERC-8086:
>
>
>
> Reference Implementation Update
> A reference implementation is now available:
> GitHub Repository: GitHub - 0xRowan/erc-8086-reference
> Live Testnet Deployment (Base Sepolia):
>
> Factory: 0x8303A804fa17f40a4725D1b4d9aF9CB63244289c
> PrivacyToken Implementation: 0xB329Dc91f458350a970Fe998e3322Efb08dDA7d1
>
> Interactive Demo: https://testnative.zkprotocol.xyz/
> All contracts are verified on Basescan. Anyone can deploy privacy tokens and test the implementation.
>
> Abstra…

---

**zero** (2025-11-29):

I’ve implemented ERC-8085 Dual-Mode Fungible Tokens with PV1 address support, currently live on Base Sepolia.



    ![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/z/a88e57/48.png)

      [ERC-8085: Dual-Mode Fungible Tokens](https://ethereum-magicians.org/t/erc-8085-dual-mode-fungible-tokens/26592/14) [ERCs](/c/ercs/57)




> Update: Reference Implementation Complete & Ready for Review
> Hi everyone,
> I’m excited to announce that the reference implementations for both ERC-8085 (Dual-Mode Fungible Tokens) and ERC-8086 (Privacy Token) are now complete and ready for community review.
>  What’s New
> Live Testnet Deployments
> Both standards now have fully functional implementations deployed on Base Sepolia:
> ERC-8085 (Dual-Mode Token)
>
>
>  Test Application: https://testdmt.zkprotocol.xyz/
>
>
> …

---

**aliceto** (2025-12-01):

After reading the whole proposal, I have one additional question regarding the three-key structure (spend / scan / encryption):

**Is the encryption key intended to be used *only* for note encryption, or is it meant to serve as a more general-purpose public encryption key?**

The reason I’m asking is that if the encryption key inside the pv-address is stable and publicly accessible, then in theory it could support a much broader set of functionalities beyond just “encrypting notes.”

For example:

---

### 1. Can it be used for private messaging between users?

In other words:

If A knows B’s pv1 address — and the encryption key is part of the public portion —

could A directly encrypt a private message (encrypted memo / metadata / plain text) to B using that encryption key?

This would enable scenarios such as:

- cross-protocol encrypted messages (e.g., “I sent you a note” notifications)
- encrypted communication between wallets
- mixed-use transactions: transfer + encrypted metadata
- offline (stealth-style) encrypted messages

If the encryption key is restricted to note encryption only, then these use cases may not be allowed.

But if the encryption key is treated as a more abstract general-purpose public key, it could potentially support much broader protocol-level extensions.

---

**zero** (2025-12-05):

Thank you for this excellent question! You’ve identified an important architectural consideration that

deserves clarification.

Short answer: Yes, the encryption key can serve as a general-purpose public encryption key.

You’re absolutely right that since the encryption key is:

- Stable (part of the pv-address)
- Publicly accessible
- Based on standard ECDH cryptography (Baby Jubjub)

It could technically support all the use cases you mentioned:

- Private messaging between users
- Cross-protocol encrypted notifications
- Encrypted metadata/memos attached to transactions
- Offline stealth-style encrypted messages
- Wallet-to-wallet encrypted communication

Design Philosophy

This proposal is an address format standard - it defines how to encode and decode three public keys, but

intentionally does not restrict how implementations use them. The decision to extend the encryption key

usage beyond note encryption is left to individual implementations. This flexibility enables innovation

while maintaining the core standard.

If a developer wants to build a private messaging system using the encryption key from pv-addresses, that’s

perfectly valid. If another wants to use it only for note encryption, that’s also fine.

---

**aliceto** (2025-12-15):

Could this be integrated with [ERC-8092](https://ethereum-magicians.org/t/erc-8092-associated-accounts/26858), enabling seamless private transfers within account abstraction—bringing encryption-like privacy directly into the user experience?


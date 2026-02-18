---
source: magicians
topic_id: 26623
title: "ERC-8086: Privacy Token"
author: zero
date: "2025-11-19"
category: ERCs
tags: [erc, token, zkp]
url: https://ethereum-magicians.org/t/erc-8086-privacy-token/26623
views: 1015
likes: 22
posts_count: 17
---

# ERC-8086: Privacy Token

Discussion topic for ERC-8086:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1359)














####


      `master` ← `0xRowan:erc-native-privacy-token`




          opened 09:17AM - 19 Nov 25 UTC



          [![](https://avatars.githubusercontent.com/u/199686996?v=4)
            0xRowan](https://github.com/0xRowan)



          [+3767
            -0](https://github.com/ethereum/ERCs/pull/1359/files)







This EIP defines a minimal interface standard for privacy tokens on Ethereum.

[…](https://github.com/ethereum/ERCs/pull/1359)
While developing privacy solutions for the Ethereum ecosystem—including wrapper protocols (converting [ERC-20](./eip-20) ↔ privacy tokens) and dual-mode tokens (combining public and private balances)—we identified a recurring need for standardized privacy primitives. Without a common interface, each implementation reinvents commitments, nullifiers, and note encryption, leading to ecosystem fragmentation.

This standard provides that common foundation. It enables:
- **Wrapper protocols**: Implement this interface for their privacy layer
- **Dual-mode tokens protocols**: Combine standards via `contract DMT is ERC20, IZRC20`

By unifying the privacy token interface, we facilitate the development of wrapper and dual-mode protocols, accelerating Ethereum's privacy ecosystem growth.

Discussion

Community discussion:
https://ethereum-magicians.org/t/erc-8086-privacy-token/26623
https://ethereum-magicians.org/t/erc-8085-dual-mode-fungible-tokens/26592












---

## Reference Implementation Update

A reference implementation is now available:

**GitHub Repository**: [GitHub - 0xRowan/erc-8086-reference](https://github.com/0xRowan/erc-8086-reference)

**Live Testnet Deployment** (Base Sepolia):

- Factory: 0x8303A804fa17f40a4725D1b4d9aF9CB63244289c
- PrivacyToken Implementation: 0xB329Dc91f458350a970Fe998e3322Efb08dDA7d1

**Interactive Demo**: https://testnative.zkprotocol.xyz/

All contracts are verified on Basescan. Anyone can deploy privacy tokens and test the implementation.

---

## Abstract

This EIP defines a minimal interface standard for native privacy tokens on Ethereum.

While developing privacy solutions for the Ethereum ecosystem—including wrapper protocols (converting ERC-20 ↔ privacy tokens) and dual-mode tokens (combining public and private balances)—we identified a recurring need for standardized privacy primitives. Without a common interface, each implementation reinvents commitments, nullifiers, and note encryption, leading to ecosystem fragmentation.

This standard provides that common foundation. It enables:

- Wrapper protocols: Implement this interface for their privacy layer
- Dual-mode tokens protocols: Combine standards via contract DMT is ERC20, IZRC20

By unifying the native privacy token interface, we facilitate the development of wrapper and dual-mode protocols, accelerating Ethereum’s privacy ecosystem growth.

## Motivation

### Privacy Infrastructure Needs Standardization

While building privacy solutions for Ethereum, we identified recurring patterns:

**Wrapper Protocols** (ERC-20 → Privacy → ERC-20):

```auto
DAI (transparent) → zDAI (private) → DAI (transparent)
```

- Each protocol implements custom privacy token logic
- No interoperability between different privacy implementations
- Duplicated effort, increased security risks

**Dual-Mode Tokens** (Public ↔ Private in one token):

```auto
Single Token: Public mode (ERC-20) ↔ Private mode (ZK-based)
```

- Needs a privacy primitive as foundation
- Current implementations reinvent the wheel

**The Solution**: Standardize the privacy primitive to enable:

- Consistent wrapper protocol implementations
- Reusable dual-mode token architectures
- Faster ecosystem development

### Design Philosophy

This standard is **not** a replacement for Wrapper Protocols or Dual-Mode Protocols. It is the **privacy foundation** they can build upon:

```auto
Ecosystem Stack:
┌─────────────────────────────────────┐
│  Applications (DeFi, DAO, Gaming)   │
├─────────────────────────────────────┤
│  Dual-Mode Tokens (ERC-20 + Privacy)│  ← Optional privacy
│  Wrapper Protocols (ERC20→Privacy)  │  ← Add privacy to existing
├─────────────────────────────────────┤
│  Native Privacy Token Interface     │  ← This standard (foundation)
├─────────────────────────────────────┤
│  Ethereum L1 / L2s                  │
└─────────────────────────────────────┘
```

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Definitions

- Native Privacy Asset: A token with privacy as an inherent property from genesis, not achieved through post-hoc mixing
- Commitment: Cryptographic binding H(amount, publicKey, randomness) hiding value and recipient
- Nullifier: Unique identifier H(commitment, secretKey) preventing double-spending
- Note: Off-chain encrypted data (amount, publicKey, randomness) for recipient
- Merkle Tree: Authenticated structure storing commitments for zero-knowledge membership proofs
- Proof Type: Parameter routing different proof strategies (active/finalized/rollover transfers)
- View Tag: Single-byte scanning optimization (OPTIONAL but RECOMMENDED)
- Stealth Address: One-time recipient address from ephemeral keys (OPTIONAL)

### Core Interface

```solidity
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.0;

/**
 * @title IZRC20
 * @notice Minimal interface for native privacy assets on Ethereum (ERC-8086)
 * @dev This standard defines the foundation for privacy-preserving tokens
 *      that can be used directly or as building blocks for wrapper protocols
 *      and dual-mode protocols implementations.
 */
interface IZRC20 {

    // ═══════════════════════════════════════════════════════════════════════
    // Events
    // ═══════════════════════════════════════════════════════════════════════

    /**
     * @notice Emitted when a commitment is added to the Merkle tree
     * @param subtreeIndex Subtree index (0 for single-tree implementations)
     * @param commitment The cryptographic commitment hash
     * @param leafIndex Position within subtree (or global index)
     * @param timestamp Block timestamp of insertion
     * @dev For single-tree: subtreeIndex SHOULD be 0, leafIndex is global position
     * @dev For dual-tree: subtreeIndex identifies which subtree, leafIndex is position within it
     */
    event CommitmentAppended(
        uint32 indexed subtreeIndex,
        bytes32 commitment,
        uint32 indexed leafIndex,
        uint256 timestamp
    );

    /**
     * @notice Emitted when a nullifier is spent (note consumed)
     * @param nullifier The unique nullifier hash
     * @dev Once spent, nullifier can never be reused (prevents double-spending)
     */
    event NullifierSpent(bytes32 indexed nullifier);

    /**
     * @notice Emitted when tokens are minted directly into privacy mode
     * @param minter Address that initiated the mint
     * @param commitment The commitment created for minted value
     * @param encryptedNote Encrypted note for recipient
     * @param subtreeIndex Subtree where commitment was added
     * @param leafIndex Position within subtree
     * @param timestamp Block timestamp of mint
     */
    event Minted(
        address indexed minter,
        bytes32 commitment,
        bytes encryptedNote,
        uint32 subtreeIndex,
        uint32 leafIndex,
        uint256 timestamp
    );

    /**
     * @notice Emitted on privacy transfers with public scanning data
     * @param newCommitments Output commitments created (typically 1-2)
     * @param encryptedNotes Encrypted notes for recipients
     * @param ephemeralPublicKey Ephemeral public key for ECDH key exchange (if used)
     * @param viewTag Scanning optimization byte (0 if not used)
     * @dev Provides data for recipients to detect and decrypt their notes
     */
    event Transaction(
        bytes32[2] newCommitments,
        bytes[] encryptedNotes,
        uint256[2] ephemeralPublicKey,
        uint256 viewTag
    );

    // ═══════════════════════════════════════════════════════════════════════
    // Metadata (ERC-20 compatible, OPTIONAL but RECOMMENDED)
    // ═══════════════════════════════════════════════════════════════════════

    /**
     * @notice Returns the token name
     * @return Token name string
     * @dev OPTIONAL but RECOMMENDED for UX and interoperability
     */
    function name() external view returns (string memory);

    /**
     * @notice Returns the token symbol
     * @return Token symbol string
     * @dev OPTIONAL but RECOMMENDED for UX and interoperability
     */
    function symbol() external view returns (string memory);

    /**
     * @notice Returns the number of decimals
     * @return Number of decimals (typically 18)
     * @dev OPTIONAL but RECOMMENDED for amount formatting
     */
    function decimals() external view returns (uint8);

    /**
     * @notice Returns the total supply across all privacy notes
     * @return Total token supply
     * @dev OPTIONAL - May be required for certain economic models (e.g., fixed cap)
     *      Individual balances remain private; only aggregate supply is visible
     */
    function totalSupply() external view returns (uint256);

    // ═══════════════════════════════════════════════════════════════════════
    // Core Functions
    // ═══════════════════════════════════════════════════════════════════════

    /**
     * @notice Mints new privacy tokens
     * @param proofType Type of proof to support multiple proof strategies.
     * @param proof Zero-knowledge proof of valid transfer
     * @param encryptedNote Encrypted note for minter's wallet
     * @dev Proof must demonstrate valid commitment creation and payment
     *      Implementations define minting rules
     */
    function mint(
        uint8 proofType,
        bytes calldata proof,
        bytes calldata encryptedNote
    ) external payable;

    /**
     * @notice Executes a privacy-preserving transfer
     * @param proofType Implementation-specific proof type identifier
     * @param proof Zero-knowledge proof of valid transfer
     * @param encryptedNotes Encrypted output notes (for recipient and/or change)
     * @dev Proof must demonstrate:
     *      1. Input commitments exist in Merkle tree
     *      2. Prover knows private keys
     *      3. Nullifiers not spent
     *      4. Value conservation: sum(inputs) = sum(outputs)
     */
    function transfer(
        uint8 proofType,
        bytes calldata proof,
        bytes[] calldata encryptedNotes
    ) external;

    // ═══════════════════════════════════════════════════════════════════════
    // Query Functions
    // ═══════════════════════════════════════════════════════════════════════

    /**
     * @notice Check if a nullifier has been spent
     * @param nullifier The nullifier to check
     * @return True if nullifier spent, false otherwise
     * @dev Implementations using `mapping(bytes32 => bool) public nullifiers`
     *      will auto-generate this function.
     */
    function nullifiers(bytes32 nullifier) external view returns (bool);

    /**
     * @notice Returns the current active subtree Merkle root
     * @return The root hash of the active subtree
     * @dev The active subtree stores recent commitments for faster proof computation.
     *      For dual-tree implementations, this is the root of the current working subtree.
     */
    function activeSubtreeRoot() external view returns (bytes32);
}
```

## Replies

**aina** (2025-11-19):

If this proposal is approved, it could help make native privacy capabilities more widely accessible across Ethereum. Compared to standards like ERC-20, privacy technologies typically present a higher technical barrier for most developers, especially when zero-knowledge tools are involved. By defining a minimal interface and providing reference implementations, projects would not need deep ZK expertise to adopt it. Developers could quickly integrate privacy modules and build privacy-related services directly, which may lead to meaningful growth for the ecosystem.

---

**zero** (2025-11-20):

One additional advantage is that a minimal privacy interface also allows downstream tooling (wallets, SDKs, indexers, bridges) to standardize around a common pattern. This could help avoid fragmented implementations and enable a broader ecosystem of native-privacy support beyond the token itself.

---

**jobs** (2025-11-20):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/z/a88e57/48.png)
    [ERC-8085: Dual-Mode Fungible Tokens](https://ethereum-magicians.org/t/erc-8085-dual-mode-fungible-tokens/26592/2) [ERCs](/c/ercs/57)



> Over the past months our team has been deeply involved in building full-stack privacy infrastructure on Base, and I’d like to share some context on why we believe a Dual-Mode Token standard is necessary.
> Before exploring dual-mode tokens, we built two complete privacy systems:
>
> Native Privacy Assets (Zcash-style on Ethereum)
>
> We implemented a fully private asset system similar to Zcash but deployed on EVM chains.
> These assets have their own value representation, and all transfers occur entire…

I went to your official website and carefully studied the work you’ve done — it’s amazing. This is also the direction I’ve always wanted to explore. If these standards are established, any project should be able to quickly integrate privacy services into Ethereum.

---

**doublespending** (2025-11-21):

I think extracting the commonalities between the two approaches is quite challenging — one is ultimately a wrapper, while the other is a native token. I hope we can avoid a situation where developers of one approach become constrained by the other.

---

**zero** (2025-11-21):

Thanks for raising this — I completely agree that wrapper-based privacy and native privacy tokens must not constrain each other’s design space. These approaches solve different problems, and their unique properties are what make them valuable.

The intent of this proposal is not to unify the systems themselves, but to extract only the minimal primitives both already need.

By standardizing just this lowest layer, we avoid interfering with protocol-level choices while still reducing duplicated work across the ecosystem. This separation allows each category to optimize where it matters most:

wrapper protocols can focus on bridging existing ERC-20 assets and cross-chain liquidity

native or dual-mode tokens can focus on UX, economics, and privacy-first asset design

Beyond those two categories, a common primitive layer offers additional ecosystem-wide benefits:

Wallets, explorers, and SDKs can support an entire class of privacy-enabled tokens with a single integration, instead of fragmented, incompatible implementations.

Auditors and regulated environments can rely on consistent public signals and optional viewing methods, instead of ad-hoc, bespoke disclosures.

So rather than forcing convergence on one implementation style, the proposal aims to prevent fragmentation at the primitive level, while keeping full flexibility for innovation at the protocol level.

---

**zero** (2025-11-25):

## Reference Implementation Update

A reference implementation is now available:

**GitHub Repository**: [GitHub - 0xRowan/erc-8086-reference](https://github.com/0xRowan/erc-8086-reference)

**Live Testnet Deployment** (Base Sepolia):

- Factory: 0x8303A804fa17f40a4725D1b4d9aF9CB63244289c
- PrivacyToken Implementation: 0xB329Dc91f458350a970Fe998e3322Efb08dDA7d1

**Interactive Demo**: https://testnative.zkprotocol.xyz/

All contracts are verified on Basescan. Anyone can deploy privacy tokens and test the implementation.

---

**jackc** (2025-12-01):

From your proposal, I see two pathways enabled by native private tokens:

**(1) dual-mode tokens (public ↔ private), and

(2) wrapping existing ERC-20s into an 8086-style native private token.**

I’ve already tried the demo for the dual-mode token — it clearly shows how assets can move between transparent and private states.

I’m curious about the second pathway:

**do you have a demo for wrapping an existing ERC-20 into an 8086 native private token?**

This seems like an important mechanism for giving today’s tokens a seamless upgrade path into the native-privacy model.

If a reference implementation or prototype exists, I’d love to experiment with it.

---

**zero** (2025-12-02):

Thanks for the great question — you’re exactly pointing at one of the most important consequences of ERC-8086.

###  8086 is the privacy primitive

ERC-8086 defines a **pure native private token**.

It is intentionally minimal: *private-only, no modes, no assumptions*.

Because it’s a clean primitive, it becomes extremely easy for others to build higher-level protocols on top of it.

This is where the two pathways emerge:

---

### (1) Dual-mode tokens (ERC-8085)

8085 is *not built into 8086* — it is a **protocol built on top of the 8086 primitive**.

It adds:

- a public representation, and
- conversion rules between public ↔ private

But this is an optional extension layer, not part of 8086.

---

### (2) Wrapping existing ERC-20s into 8086 native private tokens

This is another extension layer built *on top of* 8086.

We’ve already implemented this path:

- shield: lock ERC-20 → mint 8086 private token
- unshield: burn 8086 → withdraw ERC-20

Here, the 8086 asset remains **purely private** — no dual-mode behavior.

This gives today’s ERC-20s an immediate upgrade path into the native-privacy world.

You can try our deployed prototype on Base Sepolia:

![:backhand_index_pointing_right:](https://ethereum-magicians.org/images/emoji/twitter/backhand_index_pointing_right.png?v=15) [ZeroLayer - Privacy for Base](https://testshield.zkprotocol.xyz/market)

---

###  Why this design matters

Because 8086 is minimal and purely private, **anyone** can build:

- dual-mode tokens (8085-style)
- wrapping protocols
- cross-chain private bridges
- private vaults
- privacy-preserving DEX liquidity
- private payment rails

All without modifying the original 8086 standard.

8086 is designed to be the *base privacy building block* — simple, composable, and future-proof.

Happy to share the code or walk through our implementation if you’re interested.

---

**HenryRoo** (2025-12-10):

Really like the minimal IZRC20 design as a base privacy primitive for fungible assets.

One question on scope: is ERC-8086 intentionally focused only on ERC20 style fungible tokens, or do you see this interface (commitments/nullifiers/notes) eventually generalising to other standards e.g. NFTs (ERC-721/1155) or more specialized assets like DAT-style data tokens?

In other words, is the goal long-term privacy primitives for all asset types, or is this EIP deliberately optimised around the core ERC-20 / DeFi use case for now?

---

**zero** (2025-12-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/henryroo/48/16113_2.png) HenryRoo:

> Really like the minimal IZRC20 design as a base privacy primitive for fungible assets.
> One question on scope: is ERC-8086 intentionally focused only on ERC20 style fungible tokens, or do you see this interface (commitments/nullifiers/notes) eventually generalising to other standards e.g. NFTs (ERC-721/1155) or more specialized assets like DAT-style data tokens?
>
>
> In other words, is the goal long-term privacy primitives for all asset types, or is this EIP deliberately optimised around the core ERC-20 / DeFi use case for now?

Thank you for recognizing the minimalist design of ERC-8086 (IZRC20). The questions you raised about the long-term scope of the protocol are exactly the core trade-offs we carefully considered when designing this standard.

The current ERC-8086 specification is intentionally optimized around use cases for fungible assets. This focus is driven by pragmatism and the goal of accelerating ecosystem adoption.

For new asset types like DAT, it would be even better if they could support fungibility.

---

**tomw1808** (2025-12-21):

I am working on a similar idea for a while and just stumbled upon this ERC. I also see a need for tokens to be able to integrate a shielding logic natively. That is: on the token level instead of relying on “general purpose” solutions.

Kudos on the demo, looks very nice!

I just had a brief moment to dig into the source and the whitepaper, maybe you can help me out:

I see the interface and the merkle tree implementation, but the GitHub Repo misses somehow the circuits and resulting verifiers (?). For the reference implementation/demo: are circuits/verifier contracts intentionally out-of-repo (or generated elsewhere), and if so, what is the intended ‘canonical’ circuit family to target for interoperable wallets if any?

I was also wondering if the verifiers are based on a similar circuit design as railgun uses… ERC-8086 exposes `proofType` and opaque `proof` bytes but does the draft intend *any* standardization of circuit semantics (e.g., fixed input/output like 2-in-2-out), or is `proofType` expected to fully encapsulate circuit differences per token?

Does the ERC aim to standardize recipient key format or is wallet compatibility expected to be negotiated per implementation? Is there maybe an intended registry/discovery mechanism for supported `proofType` values and their public inputs, so wallets can know which prover to use for a given token?

---

**stateroot** (2025-12-22):

I think you can try ERC-8065 which can also support NFTs and other tokens.

---

**zero** (2025-12-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tomw1808/48/12878_2.png) tomw1808:

> I am working on a similar idea for a while and just stumbled upon this ERC. I also see a need for tokens to be able to integrate a shielding logic natively. That is: on the token level instead of relying on “general purpose” solutions.
>
>
> Kudos on the demo, looks very nice!
>
>
> I just had a brief moment to dig into the source and the whitepaper, maybe you can help me out:
>
>
> I see the interface and the merkle tree implementation, but the GitHub Repo misses somehow the circuits and resulting verifiers (?). For the reference implementation/demo: are circuits/verifier contracts intentionally out-of-repo (or generated elsewhere), and if so, what is the intended ‘canonical’ circuit family to target for interoperable wallets if any?
>
>
> I was also wondering if the verifiers are based on a similar circuit design as railgun uses… ERC-8086 exposes proofType and opaque proof bytes but does the draft intend any standardization of circuit semantics (e.g., fixed input/output like 2-in-2-out), or is proofType expected to fully encapsulate circuit differences per token?
>
>
> Does the ERC aim to standardize recipient key format or is wallet compatibility expected to be negotiated per implementation? Is there maybe an intended registry/discovery mechanism for supported proofType values and their public inputs, so wallets can know which prover to use for a given token?

Thanks for the thoughtful questions — they touch exactly the design boundary we’ve been very deliberate about with ERC-8086.

Our intent with ERC-8086 is to define a **minimal, native privacy primitive at the token level**, rather than standardizing a full privacy protocol or prescribing a concrete ZK system. This is very much a *“minimal interface, maximal freedom”* design.

### Circuits & verifiers

The absence of circuits and generated verifier contracts in the reference repo is intentional.

ERC-8086 is not meant to canonize a specific circuit family. Doing so would effectively turn the ERC into a full product specification, which would dramatically raise the implementation bar and exclude many existing or future designs. Instead, the ERC defines **what a token must expose**, not **how privacy is achieved internally**.

Projects are free to:

- generate verifiers off-repo,
- use different proving systems,
- upgrade circuits over time,
as long as they conform to the interface.

This also means that systems like Railgun could adopt ERC-8086 naturally, without refactoring their circuit architecture.

**the circuits used in our reference implementation are planned to be open-sourced in the near future.**

They are intended as a *reference and starting point*, not a mandatory target: anyone will be free to reuse them directly or adapt them to build their own ERC-8086–compatible implementations.

### Recipient keys & wallet interoperability

look this  [ERC-8091: Privacy Address Format](https://ethereum-magicians.org/t/erc-8091-privacy-address-format/26689)

---

**Ankita.eth** (2025-12-23):

What I find interesting here is not the privacy mechanics themselves, but the *implicit contract between token implementations and wallets* that ERC-8086 is creating.

By keeping circuits, verifier semantics, and recipient key formats intentionally out of scope, the ERC is effectively saying:

“the chain enforces correctness, but the wallet bears the cognitive load.”

That’s a reasonable trade-off at the primitive layer, but it raises a practical question for ecosystem convergence:

How do you see wallet developers discovering and safely supporting an ERC-8086 token *without* hardcoding per-project assumptions?

Concretely:

- If proofType fully encapsulates circuit semantics, is the expectation that wallets ship provers per token, or defer proving entirely to external tooling?
- Do you envision a lightweight, on-chain or off-chain discovery mechanism (even non-standardized at first) that maps proofType → public inputs → expected note format, purely for interoperability hints?
- Or is the long-term assumption that higher-layer standards (like 8085 / 8091) will absorb most of this friction and wallets should stay deliberately “dumb” at the 8086 level?

I’m aligned with the idea that standardizing circuits would be a mistake at this stage. I’m more curious about how you see the *coordination problem* playing out before those higher layers mature — especially for teams trying to ship production wallets rather than demos.

---

**zero** (2025-12-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ankita.eth/48/15393_2.png) Ankita.eth:

> What I find interesting here is not the privacy mechanics themselves, but the implicit contract between token implementations and wallets that ERC-8086 is creating.
>
>
> By keeping circuits, verifier semantics, and recipient key formats intentionally out of scope, the ERC is effectively saying:
> “the chain enforces correctness, but the wallet bears the cognitive load.”
>
>
> That’s a reasonable trade-off at the primitive layer, but it raises a practical question for ecosystem convergence:
>
>
> How do you see wallet developers discovering and safely supporting an ERC-8086 token without hardcoding per-project assumptions?
>
>
> Concretely:
>
>
> If proofType fully encapsulates circuit semantics, is the expectation that wallets ship provers per token, or defer proving entirely to external tooling?
> Do you envision a lightweight, on-chain or off-chain discovery mechanism (even non-standardized at first) that maps proofType → public inputs → expected note format, purely for interoperability hints?
> Or is the long-term assumption that higher-layer standards (like 8085 / 8091) will absorb most of this friction and wallets should stay deliberately “dumb” at the 8086 level?
>
>
> I’m aligned with the idea that standardizing circuits would be a mistake at this stage. I’m more curious about how you see the coordination problem playing out before those higher layers mature — especially for teams trying to ship production wallets rather than demos.

Great question. I think on-chain or off-chain discovery mechanisms, along with an SDK, are a really good direction.

---

**zero** (2026-01-12):

```auto
 // ═══════════════════════════════════════════════════════════════════════
    // Privacy Configuration (OPTIONAL but RECOMMENDED for client interoperability)
    // ═══════════════════════════════════════════════════════════════════════

    /**
     * @notice Returns the URI pointing to the Privacy Configuration File
     * @return URI string (e.g., "ipfs://Qm..." or "https://...")
     * @dev OPTIONAL but RECOMMENDED for client interoperability
     *      The configuration file contains implementation-specific parameters
     *      See specification for the full Privacy Configuration File schema
     */
    function privacyConfigURI() external view returns (string memory);

    /**
     * @notice Sets the Privacy Configuration File URI
     * @param configURI The configuration URI (can be set multiple times to update)
     * @dev OPTIONAL - Implementation may restrict access (e.g., onlyOwner)
     *      Each call overwrites the previous URI
     */
    function setPrivacyConfigURI(string calldata configURI) external;

```

[@tomw1808](/u/tomw1808) [@Ankita.eth](/u/ankita.eth)

You can take a closer look at this — each token can publicly expose its underlying metadata, and with some open SDKs, the client can automatically parse and understand the parameters behind a privacy token.

### Privacy Configuration File

Since this standard defines a ****minimal interface****, different implementations may use different:

- Proof systems (Groth16, PLONK, STARK, etc.)

- Circuit implementations (different WASM/ZKEY files)

- Note encryption algorithms

- Tree structures (single vs. dual-layer)

- Public signals schemas

To enable ****client interoperability**** across different implementations, this standard defines an ****OPTIONAL but RECOMMENDED**** Privacy Configuration File mechanism

#### Configuration URI Functions

Implementations SHOULD provide:

- `privacyConfigURI()`: Returns the URI pointing to the configuration file

- `setPrivacyConfigURI(string)`: Sets/updates the configuration URI (typically owner-restricted)

#### Privacy Configuration File Schema

The configuration file MUST be a valid JSON document. The following shows the schema structure with field descriptions:

```json
{
  "type": "",
  "version": "",
  "name": "",
  "symbol": "",

  "proofSystem": {
    "protocol": "

",
    "curve": "",
    "fieldSize": ""
  },

  "treeConfig": {
    "type": "",
    "levels": "",
    "subtreeLevels": "",
    "rootTreeLevels": ""
  },

  "circuits": {
    "": {
      "proofType": "",
      "wasmUrl": "",
      "zkeyUrl": "

",
      "publicSignals": "",
      "publicSignalsSchema": [
        { "name": "", "type": "", "index": "

" }
      ]
    }
  },

  "noteEncryption": {
    "algorithm": "",
    "curve": "",
    "curveParams": {
      "subgroupOrder": "",
      "baseField": ""
    },
    "domainSeparator": "",
    "aadTag": "",
    "noteFormat": "",
    "noteSchema": { }
  },

  "hashFunction": {
    "name": "",
    "parameters": { }
  },

  "keyDerivation": {
    "method": "",
    "addressFormat": ""
  },

  "endpoints": {
    "indexer": "",
    "relayer": ""
  }
}
```

#### Field Specifications

##### type (REQUIRED)

**Purpose**: Schema identifier URL for version detection and format validation.

**Format**: URL string pointing to the specification version.

**Example**: `https:// ... #privacy-config-v1`

**Client Usage**: Clients SHOULD check this field first to ensure they can parse the configuration format. Unknown types SHOULD be rejected.

---

##### version (REQUIRED)

**Purpose**: Semantic version of this specific configuration file.

**Format**: Semantic versioning string (MAJOR.MINOR.PATCH).

**Example**: `"1.0.0"`

**Client Usage**: Clients MAY cache configurations and use version for cache invalidation.

---

##### proofSystem (REQUIRED)

**Purpose**: Specifies the zero-knowledge proof system parameters.

| Subfield | Required | Description |
| --- | --- | --- |
| protocol | YES | ZK protocol name. Common values:groth16, plonk, fflonk, stark |
| curve | YES | Elliptic curve for the proof system. Common values:bn128 (alt_bn128), bls12-381 |
| fieldSize | YES | The scalar field prime as a decimal string. This is the maximum value for any public signal. |

**Example**:

```json
{
  "protocol": "groth16",
  "curve": "bn128",
  "fieldSize": "21888242871839275222246405745257275088548364400416034343698204186575808495617"
}
```

**How to obtain `fieldSize`**:

- For bn128: This is the BN254 scalar field prime (Fr), a 254-bit prime
- For bls12-381: Use the BLS12-381 scalar field prime
- Can be obtained from cryptographic libraries (e.g., snarkjs, circomlibjs)

**Client Usage**: Clients MUST validate that all public signals are less than `fieldSize`. The `protocol` determines which proof verification library to use.

---

##### treeConfig (REQUIRED)

**Purpose**: Specifies the Merkle tree structure for storing commitments.

| Subfield | Required | Description |
| --- | --- | --- |
| type | YES | Tree architecture:single or dual-layer |
| levels | CONDITIONAL | Total tree height (required for single type) |
| subtreeLevels | CONDITIONAL | Active subtree height (required for dual-layer type) |
| rootTreeLevels | CONDITIONAL | Root tree height (required for dual-layer type) |

**Example (single tree)**:

```json
{
  "type": "single",
  "levels": 20
}
```

**Example (dual-layer tree)**:

```json
{
  "type": "dual-layer",
  "subtreeLevels": 16,
  "rootTreeLevels": 20
}
```

**Client Usage**: Clients use this to build correct Merkle proofs. Tree capacity = 2^levels (or 2^subtreeLevels × 2^rootTreeLevels for dual-layer).


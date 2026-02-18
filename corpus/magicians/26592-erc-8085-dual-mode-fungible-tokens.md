---
source: magicians
topic_id: 26592
title: "ERC-8085: Dual-Mode Fungible Tokens"
author: zero
date: "2025-11-17"
category: ERCs
tags: [erc, token, zkp, privacy, erc20]
url: https://ethereum-magicians.org/t/erc-8085-dual-mode-fungible-tokens/26592
views: 1120
likes: 38
posts_count: 31
---

# ERC-8085: Dual-Mode Fungible Tokens

Discussion topic for ERC-8085:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1359)














####


      `master` ← `0xRowan:erc-native-privacy-token`




          opened 09:17AM - 19 Nov 25 UTC



          [![](https://avatars.githubusercontent.com/u/199686996?v=4)
            0xRowan](https://github.com/0xRowan)



          [+4241
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

**Interactive Demo**: [https://testdmt.zkprotocol.xyz/](https://testnative.zkprotocol.xyz/)

All contracts are verified on Basescan. Anyone can deploy tokens and test the implementation.

## Abstract

This EIP defines an interface for fungible tokens that operate in two modes: transparent mode (fully compatible with ERC-20) and privacy mode (using [ERC-8086](https://ethereum-magicians.org/t/erc-8086-privacy-token/26623) privacy primitives). Token holders can convert balances between modes. The transparent mode uses account-based balances, while the privacy mode uses the standardized IZRC20 interface from ERC-8086. Total supply is maintained as the sum of both modes.

## Motivation

### The Privacy Dilemma for New Token Projects

When launching a new token, projects face a fundamental choice:

1. ERC-20: Full DeFi composability but zero privacy
2. Pure privacy protocols: Strong privacy but limited ecosystem integration

This creates real-world problems:

- DAOs need public treasury transparency but want anonymous governance voting
- Businesses require auditable accounting but need private payroll transactions
- Users want DeFi participation but need privacy for personal holdings

Existing solutions require trade-offs that limit adoption.

### Current Approaches and Their Limitations

#### Wrapper-Based Privacy (e.g.,   Privacy Pools)

**Mechanism**: Wrap existing tokens (DAI, ETH) into a privacy pool contract.

```auto
DAI (public) → deposit → Privacy Pool → withdraw → DAI (public)
```

**Strengths**:

- Works with any existing ERC-20 token
- Permissionless deployment
- No changes to underlying token required

**Limitations for New Token Projects**:

- Creates two separate tokens (Token A vs. Wrapped Token B)
- Splits liquidity between public and wrapped versions
- Requires managing two separate contract addresses
- Users must unwrap to access DeFi (additional friction)

**Best suited for**: Adding privacy to existing deployed tokens (DAI, USDC, etc.)

### Our Approach: Integrated Dual-Mode for New Tokens

This standard provides a alternative option specifically designed for **new token deployments** that want privacy as a core feature from day one.

**Target Use Case**: Projects launching new tokens (governance tokens, protocol tokens, app tokens) that need both DeFi integration and optional privacy.

**Mechanism**:

```auto
Single Token Contract
  ↓
Public Mode (ERC-20) ←→ Privacy Mode (ZK-SNARK)
  ↓                           ↓
DeFi/DEX Trading          Private Holdings
```

**Key Advantages**:

1. Unified Token Economics

No liquidity split between public/private versions
2. One token address, one market price
3. Simplified token distribution and airdrops
4. Seamless Mode Switching

Convert to privacy mode for holdings: toPrivacy()
5. Convert to public mode for DeFi: toPublic()
6. Users choose privacy per transaction, not per token
7. Full ERC-20 Compatibility

Works with existing wallets, DEXs, and DeFi protocols
8. No special support needed for public mode operations
9. Standard totalSupply() accounting tracks both modes
10. Transparent Supply Tracking

totalSupply() includes both public and privacy mode balances
11. totalPrivacySupply() reveals aggregate privacy supply (no individual balances)
12. Prevents hidden inflation
13. Regulatory visibility into aggregate metrics
14. Application-Layer Deployment

Deploy today on any EVM chain (Ethereum, L2s, sidechains)
15. No protocol changes or governance votes required
16. No coordination with core developers needed

### Real-World Use Cases

**1. DAO Governance Token**

```auto
Public Mode:
  - Treasury management (transparent)
  - Grant distributions (auditable)
  - DEX trading (liquidity)

Privacy Mode:
  - Anonymous voting (no vote buying)
  - Private delegation (confidential strategy)
  - Personal holdings (no public scrutiny)
```

**2. Privacy-Aware Business Token**

```auto
Public Mode:
  - Investor reporting (compliance)
  - Exchange listings (liquidity)
  - Public fundraising (transparency)

Privacy Mode:
  - Employee compensation (confidential)
  - Supplier payments (competitive advantage)
  - Strategic reserves (private holdings)
```

**3. Protocol Token with Optional Privacy**

```auto
Public Mode:
  - Staking (DeFi integration)
  - Liquidity provision (AMM pools)
  - Trading (price discovery)

Privacy Mode:
  - Long-term holdings (privacy)
  - Over-the-counter transfers (confidential)
  - Strategic positions (no front-running)
```

### Design Philosophy

This standard embraces a core principle: **“Privacy is a mode, not a separate token.”**

Rather than forcing users to choose between incompatible assets (Token A vs. Privacy Token B), we enable contextual privacy within a single fungible token. Users select the appropriate mode for each use case, maintaining capital efficiency and unified liquidity.

This approach acknowledges that privacy and composability serve different purposes, and most users need both at different times—not a forced choice between them.

### Interface

```solidity
/**
 * @title IDualModeToken
 * @notice Interface for dual-mode tokens (ERC-8085) combining ERC-20 and [ERC-8086](./eip-8086) (IZRC20)
 * @dev Implementations MUST inherit both IERC20 and IZRC20
 *      Privacy events and core functions are inherited from IZRC20 (ERC-8086)
 *      This interface only defines mode conversion logic - the core value of ERC-8085
 *
 * Architecture:
 *   - Public Mode: Standard ERC-20 (transparent balances and transfers)
 *   - Privacy Mode: ERC-8086 IZRC20 (ZK-SNARK protected balances and transfers)
 *   - Mode Conversion: toPrivacy (public → private) and toPublic (private → public)
 */
interface IDualModeToken is IERC20, IZRC20 {

    // ═══════════════════════════════════════════════════════════════════════
    // Events (Mode Conversion Specific)
    // ═══════════════════════════════════════════════════════════════════════

    /// @notice Emitted when value is converted from transparent to privacy mode
    /// @param account The address converting tokens
    /// @param amount The amount converted
    /// @param commitment The cryptographic commitment created
    /// @param timestamp Block timestamp of conversion
    event ConvertToPrivacy(
        address indexed account,
        uint256 amount,
        bytes32 indexed commitment,
        uint256 timestamp
    );

    /// @notice Emitted when value is converted from privacy to transparent mode
    /// @param initiator The address initiating the conversion
    /// @param recipient The address receiving transparent tokens
    /// @param amount The amount converted
    /// @param timestamp Block timestamp of conversion
    event ConvertToPublic(
        address indexed initiator,
        address indexed recipient,
        uint256 amount,
        uint256 timestamp
    );

    // ═══════════════════════════════════════════════════════════════════════
    // Mode Conversion Functions (Core of ERC-8085)
    // ═══════════════════════════════════════════════════════════════════════

    /**
     * @notice Convert transparent balance to privacy mode
     * @dev Burns ERC-20 tokens and creates privacy commitment via IZRC20
     * @param amount Amount to convert (must match proof)
     * @param proofType Type of proof to support multiple proof strategies.
     * @param proof ZK-SNARK proof of valid commitment creation
     * @param encryptedNote Encrypted note data for recipient wallet
     */
    function toPrivacy(
        uint256 amount,
        uint8 proofType,
        bytes calldata proof,
        bytes calldata encryptedNote
    ) external;

    /**
     * @notice Convert privacy balance to transparent mode
     * @dev Spends privacy notes and mints ERC-20 tokens to recipient
     * @param recipient Address to receive public tokens
     * @param proofType Type of proof to support multiple proof strategies.
     * @param proof ZK-SNARK proof of note ownership and spending
     * @param encryptedNotes Encrypted notes for change outputs (if any)
     */
    function toPublic(
        address recipient,
        uint8 proofType,
        bytes calldata proof,
        bytes[] calldata encryptedNotes
    ) external;

    // ═══════════════════════════════════════════════════════════════════════
    // Supply Tracking
    // ═══════════════════════════════════════════════════════════════════════

    // Note: Privacy transfers use IZRC20.transfer(uint8, bytes, bytes[])
    // which is inherited from IZRC20 (ERC-8086)

    /**
     * @notice Total supply across both modes (overrides IERC20 and IZRC20)
     * @return Total supply = publicSupply + privacySupply
     */
    function totalSupply() external view override(IERC20, IZRC20) returns (uint256);

    /**
     * @notice Get total supply in privacy mode
     * @dev Tracked by increments/decrements during mode conversions
     * @return Total privacy supply
     */
    function totalPrivacySupply() external view returns (uint256);

    /**
     * @notice Check if a nullifier has been spent
     * @dev Alias for IZRC20.nullifiers() with different naming convention
     * @param nullifier The nullifier hash to check
     * @return True if spent, false otherwise
     */
    function isNullifierSpent(bytes32 nullifier) external view returns (bool);
}
```

### Proof Type Parameter

The `proofType` parameter in `toPrivacy`, `toPublic`, and `privacyTransfer` functions allows implementations to support multiple proof strategies.

**Purpose**: Different proof types may be needed for:

- Different data structures (e.g., active vs. archived state in dual-tree implementations)
- Different optimization strategies (e.g., activeTree proofs vs. finalizedTree proofs)

### Compatibility

Implementations MUST implement the ERC-20 interface. All ERC-20 functions operate exclusively on transparent mode balances:

- balanceOf(account) MUST return the transparent mode balance only

Privacy mode balances are NOT included (they are hidden by design)

`transfer(to, amount)` MUST transfer transparent balance only
`approve(spender, amount)` MUST approve transparent balance spending
`transferFrom(from, to, amount)` MUST transfer transparent balance with allowance
`totalSupply()` MUST return the sum of all public balances plus `totalPrivacySupply()`

- This represents the total token supply across both modes

Implementations MUST emit standard ERC-20 `Transfer` events for transparent mode operations.

### Supply Invariant

Implementations MUST maintain the following invariant at all times:

```solidity
totalSupply() == sum(all balanceOf(account)) + totalPrivacySupply()
```

Where:

- totalSupply(): Inherited from ERC-20, represents total token supply across both modes
- sum(all balanceOf(account)): Sum of all transparent mode balances
- totalPrivacySupply(): Aggregate privacy mode supply, tracked by:

Incrementing on toPrivacy() (public → private conversion)
- Decrementing on toPublic() (private → public conversion)
- NOT computed from Merkle tree (commitment values are encrypted)

**Note**: The public mode supply can be derived as `totalSupply() - totalPrivacySupply()` if needed, eliminating the need for a separate `totalPublicSupply()` function.

## Replies

**zero** (2025-11-17):

Over the past months our team has been deeply involved in building full-stack privacy infrastructure on Base, and I’d like to share some context on why we believe a Dual-Mode Token standard is necessary.

Before exploring dual-mode tokens, we built two complete privacy systems:

1. Native Privacy Assets (Zcash-style on Ethereum)

We implemented a fully private asset system similar to Zcash but deployed on EVM chains.

These assets have their own value representation, and all transfers occur entirely in the private domain with ZK proofs, commitments, nullifiers, encrypted notes, etc.

This proved that Zcash-level privacy can run natively on Ethereum without L1 protocol changes.

1. A Wrapping-Based Privacy Layer (ZeroLayer)

We then built a full wrapping model:

Any ERC20 or ETH can be shielded into a private asset

Private transfers use ZK-SNARKs

Unshield back to public ERC20/ETH at any time

This system is fully deployed and functional today on Base Sepolia.

Through this work we discovered several limitations of the wrapping model, including:

fragmented UX (two tokens: public + wrapped-private)

inconsistency between transparent and private supply

added trust and complexity around the wrapper contract

increased friction when integrating with DeFi

These limitations motivated the idea that privacy should be native to the token itself, not an external wrapper.

Why This Led to Dual-Mode Tokens

After building both native-private assets and wrapped-private assets, the natural next step became clear:

A token shouldn’t need two separate representations.

Instead, a single asset should support:

Public (ERC20) mode

Private (ZK-based) mode

Seamless conversion between the two

Shared total supply invariant

This avoids the UX friction and architectural complexity of wrapped privacy, while keeping full ERC20 compatibility.

The Dual-Mode Token standard is our attempt to formalize this model so that:

any new token can launch with built-in privacy

developers have predictable interfaces

DeFi remains fully compatible

users can choose transparency or privacy as needed

We hope this discussion can help move Ethereum privacy toward more standardized and composable patterns.

Happy to answer questions or provide implementation insights from our deployments.

---

**jobs** (2025-11-18):

The idea of treating privacy as an optional “mode” rather than a wrapped asset is interesting, especially because it avoids liquidity splitting for new tokens, which has always been a practical issue.

One thought: if this evolves into an ERC, it might work best as an **optional extension**, similar to how ERC-2612 or ERC-3009 function today. Many projects simply don’t need privacy or don’t want the additional proving/verification overhead, while others — especially governance-heavy tokens or business-oriented deployments — might find this dual-mode approach appealing.

Technically the interface is clean, but I’d suggest clarifying which parts of the design are **mandatory for the standard** (e.g., supply invariance, reversible conversion) versus which parts are **implementation details** (e.g., the specific Merkle tree structure). Keeping that boundary crisp would make adoption easier and avoid locking the ecosystem to one proving architecture.

Overall, the direction seems useful as an optional extension for teams that want privacy “built-in” but stay within the ERC-20 ecosystem.

---

**zero** (2025-11-18):

Thank you for the thoughtful feedback! You’ve raised several excellent points that align well with our design philosophy.

## On Being an Optional Extension

You’re absolutely right about positioning this as an optional extension rather than a mandatory feature. We intentionally designed it to be fully backward-compatible with ERC-20, so projects that don’t need privacy can simply ignore the privacy-related functions entirely. The comparison to ERC-2612/ERC-3009 is apt - this should be a tool in the toolkit, not a requirement.

The overhead concern is valid. Projects should carefully consider whether they need this functionality, as ZK proof verification does add gas costs (~300-500k gas for privacy operations). For many tokens, standard ERC-20 is perfectly sufficient.

## Clarifying Mandatory vs. Implementation Details

This is crucial feedback. Let me clarify what we see as **mandatory** for the standard vs. **implementation flexibility**:

**Mandatory (Core Requirements):**

- Supply invariant: totalSupply() == sum(balanceOf) + totalPrivacySupply()
- Reversible conversion between modes (toPrivacy/toPublic)
- Nullifier-based double-spend prevention
- ERC-20 compatibility for transparent mode
- Standardized events (CommitmentAppended, NullifierSpent)

**Implementation Flexible:**

- Merkle tree structure (could use accumulators, sparse trees, etc.)
- Proof system (Groth16, PLONK, STARKs, future systems)
- Commitment scheme details
- Note encryption method
- Tree depth and batching strategies

You’re right that we should make this boundary more explicit in the spec. The `proofType` parameter was our attempt to allow for multiple proving systems, but we could better document which aspects are fixed vs. flexible.

## Use Case Alignment

Your observation about governance and business tokens is spot-on. These are exactly our primary targets:

- Governance tokens: Public treasury, private voting
- Business tokens: Compliant operations, confidential payments
- Protocol tokens: Public staking, private holdings

We’re not trying to make every token private - just giving teams the option to build it in from day one when it makes sense.

---

**RILTONKC** (2025-11-18):

If I may, I would love to walk this path with you as my projects needs great minds as presented here. Your launch is welcome on our network through mutiple platforms and partners, we have a reach of 5 continents. The iOS app launch planned for Jan and Token. I would love to partner with you. I can assure you the path wont have a destination but our applied vision will make the path destined.

---

**zero** (2025-11-19):

Thank you for the kind words — I really appreciate the enthusiasm and openness to collaborate.

It’s great to hear that your project shares a similar vision, and I’m glad our work resonates with you.

Before discussing any potential partnership, I’d like to understand more about your project’s focus and technical direction.

I look forward to learning more about what you’re building and how your ecosystem operates. Once we have a clearer mutual understanding, we can explore whether there’s a good fit for collaboration.

---

**jobs** (2025-11-20):

Thanks for the detailed clarification — this really helps frame the intent of the standard.

I especially like the separation you outlined between **mandatory guarantees** (supply invariance, reversible conversion, nullifier protection, standard events) and **implementation flexibility** (proof system, tree design, encryption). Making that boundary explicit should go a long way toward preventing vendor-lock concerns as the ZK tooling landscape evolves.

One suggestion that might be useful as you move toward a formal ERC draft:

it may help to define a **minimal compliance profile** — something like:

- required interface + events
- semantic guarantees (e.g., no leaking of note linkability, no violation of supply invariance)
- optional modular “adapters” for proving systems

This would let the ecosystem standardize around *what must be guaranteed*, while still letting different projects plug in whatever proving tech fits their constraints. It may also make audits easier by giving security reviewers a canonical checklist.

Overall, I think the direction is compelling, especially for tokens that need compliance-friendly privacy without leaving the ERC-20 ecosystem.

Looking forward to seeing how the proposal evolves — happy to provide further review if you publish a draft!

---

**anziai** (2025-11-22):

Thanks for sharing this proposal , I’m really interested in the idea behind ERC-8085 and native privacy tokens.

What stands out to me is that it doesn’t force every token to be private by default, but instead lets projects optionally enable a privacy mode when they need it. From a user perspective, that feels much more flexible: I can use a normal ERC-20 token for everyday transactions, and switch to a private transfer only when I care about financial privacy.

Another thing I appreciate is that it avoids using a separate “wrapped” token. In many systems today, wrapped privacy tokens are confusing to hold and trade, and they split liquidity across different versions of the same asset. If privacy can be built into the native token itself, without extra steps, it sounds much easier for users and wallets.

Overall, I’m not a developer, but this seems like something that could make privacy more practical and accessible in real use. I’m curious to see how wallets and exchanges might integrate this in the future.

---

**zero** (2025-11-23):

Thank you for the thoughtful feedback. The design choice to keep privacy optional is exactly intended to avoid disruption to existing ERC-20 workflows, while still giving applications a built-in path to private transfers when needed.

The goal is not to introduce a new “privacy asset class,” but rather to make privacy a feature that native tokens can adopt without wrapping, liquidity fragmentation, or major changes to user experience.

As you mentioned, actual adoption will likely depend on how wallets, exchanges, and infrastructure providers choose to support the interface. A minimal standard is meant to give them a stable target to build on, so native privacy can be integrated gradually over time rather than all at once.

---

**jake_the_slug** (2025-11-24):

I like the idea of generalizing privacy as a feature on the tokens rather than protocol specific implementations or the need to use Railgun, Aztec etc. to obfuscate on-chain ownership.

The ability to share the proof generator and Merkle tree among implementations would make it easy for token deployers to opt-in (no multi-party ceremony, off-chain circuit to setup etc).

Most protocols don’t want to bother with these, and the anonymity set greatly benefits from sharing that infra.

I like to imagine this an easy to adopt feature akin to making an ERC20 cross-chain transferable using LayerZero’s OFT stack, a few minutes setup on the dev side, no Tornado-like stack to maintain.

---

**zero** (2025-11-24):

Really appreciate this insight — and you’ve framed the key motivation perfectly.

ERC-8085 is trying to make privacy an opt-in capability, not a platform choice.

Projects shouldn’t need to adopt a full privacy stack (Railgun, Aztec, Tornado-like infra) just to support private transfers.

With shared proof generators + a shared Merkle tree:

no multi-party ceremony

no per-project circuit setup

no custom infra to maintain

anonymity set grows collectively rather than fragmenting

Just like OFT made cross-chain liquidity trivial, ERC-8085 aims to make privacy trivial, modular, and reusable, so ERC-20s can enable it in minutes — only if they need it.

---

**aina** (2025-11-28):

I’d like to surface another consideration that doesn’t get enough attention in most privacy-token designs: **capacity limits of the underlying Merkle trees**.

Most privacy systems implicitly assume the tree is “infinite,” but in practice every commitment tree has a fixed height and therefore a fixed maximum capacity. For example, a tree with ~1M leaves sounds large, but once the commitment space is exhausted the system essentially has two options:

1. Restart a new tree (epoch-based rotation)
2. Introduce an archival tree + active tree structure

Both approaches introduce real trade-offs.

- If the system restarts the tree, all future proofs must somehow reference multiple historical trees or rely on nullifier registries external to the main tree.
- If the system uses an active/archived dual-tree model, clients need to handle different proof formats (hence why this proposal includes proofType), and this complicates wallet implementations, syncing, and proving time.

I’m bringing this up because in a dual-mode token like ERC-8085, tree capacity becomes even more important:

- converting toPrivacy() increases load on the privacy tree
- high-throughput tokens (governance tokens, protocol tokens, app tokens) could saturate the tree sooner than expected
- tree restarts affect UX in a way ERC-20 users are not accustomed to

So in my view this needs to be a deliberate design choice rather than an afterthought.

At the standard level we may not want to prescribe a specific tree strategy, but we should at least acknowledge:

- implementations will hit capacity limits
- proofType exists largely to enable tree versioning / multi-tree proving
- long-lived tokens need a strategy that avoids system-wide pauses or resets once the tree fills

Curious how others are thinking about this.

This feels like a fundamental part of the long-term viability of any privacy-enabled fungible token.

---

**zero** (2025-11-29):

##  Update: Reference Implementation Complete & Ready for Review

Hi everyone,

I’m excited to announce that the reference implementations for both **ERC-8085** (Dual-Mode Fungible Tokens) and **ERC-8086** (Privacy Token) are now complete and ready for community review.

###  What’s New

**Live Testnet Deployments**

Both standards now have fully functional implementations deployed on Base Sepolia:

**ERC-8085 (Dual-Mode Token)**

- Test Application: https://testdmt.zkprotocol.xyz/
- Verified Contracts: Factory at 0x64EeF…
- Features: ERC-20 ↔ Privacy mode conversion, dual-layer Merkle tree

**ERC-8086 (Privacy Token)**

- Test Application: https://testnative.zkprotocol.xyz/
- Verified Contracts: Factory at 0x04df6D…
- Features: Native privacy, ZK-SNARK proofs, minimal interface

All contracts are verified on Basescan with public source code.

###  Try It Yourself

You can now interact with the implementations:

1. Connect your wallet to Base Sepolia (Chain ID: 84532)
2. Get test ETH from Base Sepolia faucet
3. Visit the test applications linked above
4. For ERC-8085: Mint public tokens → Convert to privacy mode → Transfer privately → Convert back
5. For ERC-8086: Mint privacy tokens → Transfer privately → Verify on-chain

---

**zero** (2025-12-03):

Thanks for raising this — you’re absolutely right that tree capacity is one of the most under-discussed long-term constraints of privacy-enabled fungible tokens.

In ERC-8085 we approached this head-on with a **two-layer Merkle tree design**, instead of a single monolithic tree.

###  8085 uses:

- subtrees of height 16
- a root tree of height 20

This structure is intentional and solves several of the concerns you mentioned:

---

## 1. Subtree rotation happens frequently, but cheaply

A subtree with height 16 holds **65,536 commitments**.

When a subtree fills:

- it is sealed
- its root is inserted into the root tree,
- and a new empty subtree starts immediately

The cost of subtree rollover is extremely low and does **not** disrupt proving, syncing, or UX.

---

## 2. The root tree provides long-range scalability

A height-20 root tree can hold **over 1 million subtree roots**, meaning the system’s total capacity is:

> 65,536 × 1,048,576
> ≈ 6.8 × 10¹⁰ commitments (68 billion)

At typical usage rates, this is effectively *multi-decade capacity* before the root tree itself needs to rotate.

This ensures high-throughput tokens won’t unexpectedly hit global capacity limits.

---

## 3. ProofType exists exactly for the multi-tree scenario you described

We fully agree with you:

**ProofType is not just a convenience — it is the compatibility layer for tree evolution.**

It allows:

- archived subtrees
- active subtree
- future extended trees
- alternative hash functions
- different circuit versions

…all to coexist without breaking wallets or forcing app-level migrations.

This is precisely why 8085 avoids fixing a single tree layout at the standard level, while the reference impl uses the two-layer model.

---

## 4. UX is protected — ERC-20 users never face “tree resets”

The critical UX requirement for 8085 is that *toPrivacy()* must feel as smooth as ERC-20 transfers.

Using:

- rolling subtrees
- enormous root-tree capacity
- proof versioning

…we avoid the catastrophic UX failures seen in systems that require global tree resets.

From the user’s perspective:

- no pauses
- no version incompatibility
- no manual migration
- no wallet confusion

Only the proving stack is aware of tree structure.

---

## 5. Long-lived tokens must plan for tree lifetime — we agree

Your point is completely correct:

any privacy-enabled fungible token without a tree lifetime strategy is not future-proof.

8085’s two-layer design is precisely our way of offering:

- a scalable primitive,
- predictable capacity,
- and a standardized pathway for future trees without breaking ecosystem composability.

We absolutely welcome further discussion on whether the standard should include stronger guidance or minimum expectations here.

---

**zero** (2025-12-04):

Just to clarify one important point about ERC-8085:

![:small_blue_diamond:](https://ethereum-magicians.org/images/emoji/twitter/small_blue_diamond.png?v=12) The 16×20 two-layer Merkle tree is not a protocol requirement.

It’s simply the reference architecture used in the demo implementation because it offers a practical balance between prover performance, client complexity, and multi-decade capacity.

At the standard level 8085 does not prescribe any specific tree height, layout, or number of layers.

8085 defines a dual-mode token — not a Merkle tree configuration.

Tree choice is intentionally left flexible so each deployment can optimize for throughput, hardware assumptions, and operational lifetime.

---

**aliceto** (2025-12-07):

I’ve been following the privacy token discussion in the Ethereum ecosystem for a while, and I think ERC-8085 addresses a real pain point that hasn’t been adequately solved before. Let me share my perspective as someone who would actually use this feature.

What resonates with me:

The “privacy as a mode, not a separate token” philosophy makes intuitive sense. In my daily usage, I don’t want to manage two different assets (Token A vs. Privacy-Wrapped Token B) just to have privacy options. The mental model here is elegant: one token, choose your context. This is similar to how I think about using a VPN – I don’t switch to a “different internet,” I just change my connection mode.

The DAO governance use case particularly stands out. I’ve participated in several DAO votes where I felt uncomfortable having my entire token holdings and voting positions publicly visible. Being able to convert to privacy mode for voting while keeping the treasury transparent solves a genuine problem without forcing the entire protocol into full privacy.

---

**My questions and concerns:**

Conversion reveals amounts: When converting from privacy to public mode, the ConvertToPublic event reveals the exact amount. For users trying to maintain privacy, this feels like a significant information leak. I understand the technical necessity (supply invariant verification), but it limits the privacy guarantees. Would it make sense to document recommended practices, like converting only partial amounts or using mixing strategies?

---

**zero** (2025-12-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aliceto/48/16670_2.png) aliceto:

> I’ve been following the privacy token discussion in the Ethereum ecosystem for a while, and I think ERC-8085 addresses a real pain point that hasn’t been adequately solved before. Let me share my perspective as someone who would actually use this feature.
>
>
> What resonates with me:
>
>
> The “privacy as a mode, not a separate token” philosophy makes intuitive sense. In my daily usage, I don’t want to manage two different assets (Token A vs. Privacy-Wrapped Token B) just to have privacy options. The mental model here is elegant: one token, choose your context. This is similar to how I think about using a VPN – I don’t switch to a “different internet,” I just change my connection mode.
>
>
> The DAO governance use case particularly stands out. I’ve participated in several DAO votes where I felt uncomfortable having my entire token holdings and voting positions publicly visible. Being able to convert to privacy mode for voting while keeping the treasury transparent solves a genuine problem without forcing the entire protocol into full privacy.
>
>
>
> My questions and concerns:
>
>
> Conversion reveals amounts: When converting from privacy to public mode, the ConvertToPublic event reveals the exact amount. For users trying to maintain privacy, this feels like a significant information leak. I understand the technical necessity (supply invariant verification), but it limits the privacy guarantees. Would it make sense to document recommended practices, like converting only partial amounts or using mixing strategies?

The privacy layer is fundamentally **decoupled from your account**.

You can control your privacy-mode assets from **any address** — with no linkage, no traceability.

For example, suppose you originally have **1000 ZERO**.

If you use **Account-1** to switch **500 ZERO** into privacy mode,

you can later use **any other account** to switch those **same 500 ZERO** back into public mode — with **no restrictions** on how many times or in what amounts.

**Example scenarios:**

- Account-2 switches 80 ZERO back to public mode
- Account-3 switches 100 ZERO back to public mode
- …and so on

None of these actions are linked to each other in any observable way.

Your privacy-mode assets are **no longer bound to a single address**.

You can freely split, move, or transform them between privacy mode and public mode — entirely on your own terms, with full privacy.

---

**zero** (2025-12-09):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/z/a88e57/48.png) zero:

> ## Update: Reference Implementation Complete & Ready for Review
>
>
>
> Hi everyone,
>
>
> I’m excited to announce that the reference implementations for both ERC-8085 (Dual-Mode Fungible Tokens) and ERC-8086 (Privacy Token) are now complete and ready for community review.
>
>
>
> ###  What’s New
>
>
>
> Live Testnet Deployments
>
>
> Both standards now have fully functional implementations deployed on Base Sepolia:
>
>
> ERC-8085 (Dual-Mode Token)
>
>
>  Test Application: https://testdmt.zkprotocol.xyz/
>  Verified Contracts: Factory at 0x64EeF…
>  Features: ERC-20 ↔ Privacy mode conversion, dual-layer Merkle tree
>
>
> ERC-8086 (Privacy Token)
>
>
>  Test Application: https://testnative.zkprotocol.xyz/
>  Verified Contracts: Factory at 0x04df6D…
>  Features: Native privacy, ZK-SNARK proofs, minimal interface
>
>
> All contracts are verified on Basescan with public source code.
>
>
>
> ###  Try It Yourself
>
>
>
> You can now interact with the implementations:
>
>
> Connect your wallet to Base Sepolia (Chain ID: 84532)
> Get test ETH from Base Sepolia faucet
> Visit the test applications linked above
> For ERC-8085: Mint public tokens → Convert to privacy mode → Transfer privately → Convert back
> For ERC-8086: Mint privacy tokens → Transfer privately → Verify on-chain

**A new reference implementation**

**ERC-8085 (Dual-Mode Token)**

- Test Application: https://testdmt.zkprotocol.xyz/
- Verified Contracts: Dual-Mode Token at 0xd8714b…

---

---

**HenryRoo** (2025-12-09):

Hey hey, gorgeous privacy proposal, lol an amazing comment about VPN [@aliceto](/u/aliceto), there is lack of something like this, secure privacy layer / mode like this one in proposal.

I’m also trying to better understand how this standard interacts with real-world compliance and “source of funds” checks.

In the ERC-20 world, on-chain analytics providers can reconstruct transaction graphs and help regulated entities assess the cleanliness of incoming funds. With ZRC-20, once assets are shielded, this transaction graph becomes opaque to everyone except the holder and parties who are explicitly given a viewing/auditing key.

A few related questions:

1. Am I correct that, for third parties without a viewing/auditing key, it is effectively impossible to perform a traditional on-chain source-of-funds analysis once assets are inside the ZRC-20 privacy layer, beyond tagging deposits/withdrawals that touch the pool?
2. Do you expect regulated exchanges or frontends that integrate ZRC-20 wrappers to require users to share viewing/auditing keys as a condition for deposits and withdrawals? If so, have you explored how this would work in practice (UX, key management, revocation, etc.)?
3. Are you considering any standardized zk-compliance primitives on top of ZRC-20 (for example, proofs of the form “these funds do not originate from addresses on a sanctions list” without revealing the full transaction path), or is this intentionally left entirely to higher-layer protocols?
4. From a regulatory-risk perspective, how do you see native privacy assets being treated differently from classic mixer designs, given that for third parties without keys the observable pattern still looks like “funds enter a shielded pool and later exit with unlinkability”?

I really like the idea of standardizing privacy primitives, but I’m curious how you envision the balance between strong privacy for users and the ability of compliant actors to perform meaningful source-of-funds checks in practice.

---

**zero** (2025-12-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/henryroo/48/16113_2.png) HenryRoo:

> Hey hey, gorgeous privacy proposal, lol an amazing comment about VPN @aliceto, there is lack of something like this, secure privacy layer / mode like this one in proposal.
>
>
> I’m also trying to better understand how this standard interacts with real-world compliance and “source of funds” checks.
>
>
> In the ERC-20 world, on-chain analytics providers can reconstruct transaction graphs and help regulated entities assess the cleanliness of incoming funds. With ZRC-20, once assets are shielded, this transaction graph becomes opaque to everyone except the holder and parties who are explicitly given a viewing/auditing key.
>
>
> A few related questions:
>
>
> Am I correct that, for third parties without a viewing/auditing key, it is effectively impossible to perform a traditional on-chain source-of-funds analysis once assets are inside the ZRC-20 privacy layer, beyond tagging deposits/withdrawals that touch the pool?
> Do you expect regulated exchanges or frontends that integrate ZRC-20 wrappers to require users to share viewing/auditing keys as a condition for deposits and withdrawals? If so, have you explored how this would work in practice (UX, key management, revocation, etc.)?
> Are you considering any standardized zk-compliance primitives on top of ZRC-20 (for example, proofs of the form “these funds do not originate from addresses on a sanctions list” without revealing the full transaction path), or is this intentionally left entirely to higher-layer protocols?
> From a regulatory-risk perspective, how do you see native privacy assets being treated differently from classic mixer designs, given that for third parties without keys the observable pattern still looks like “funds enter a shielded pool and later exit with unlinkability”?
>
>
> I really like the idea of standardizing privacy primitives, but I’m curious how you envision the balance between strong privacy for users and the ability of compliant actors to perform meaningful source-of-funds checks in practice.

third parties without a viewing/auditing key, Once funds enter the privacy layer, tracing their provenance becomes inherently difficult. Private assets are not tied to any Ethereum account address, and any address that interacts with the privacy contract cannot be treated as a reliable indicator of ownership. Such an address might be a relayer, or simply another unrelated address that has no correlation with the actual user.

The proposal itself is intentionally scoped as an *interface-level standard*, rather than prescribing any concrete implementation or enforcement logic.

It defines how privacy addresses are expressed and interoperated, without constraining how individual projects choose to realize them.

This separation allows different implementations and client layers to adopt compliance-aware behaviors in ways that align with their local regulatory environments, while keeping the underlying protocol fully permissionless and minimal.

Enabling this kind of flexibility at the client and integration layer is one of the core design motivations behind ERC-8091.

---

**zk-friendly** (2025-12-25):

Noob question, whats different with Railgun?


*(10 more replies not shown)*

---
source: magicians
topic_id: 25999
title: "ERC-8063: Groups - Multi-member onchain containers for shared resources"
author: jamesavechives
date: "2025-10-28"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8063-groups-multi-member-onchain-containers-for-shared-resources/25999
views: 148
likes: 7
posts_count: 12
---

# ERC-8063: Groups - Multi-member onchain containers for shared resources

This proposal specifies a general-purpose “Group” primitive as a first-class, onchain object. Each group is deployed as its own contract (identified by its contract address) and has an owner, an extensible set of members, and optional metadata. The standard defines a minimal interface for direct member management and membership introspection. Unlike token standards (e.g., ERC-20/ERC-721) that model units of transferable ownership, Groups model multi-party membership and coordination. The goal is to enable interoperable social, organizational, and collaborative primitives.

For the latest text, discussion, and updates, please use the GitHub pull request:

- PR link: https://github.com/ethereum/ERCs/pull/1500

This page is a pointer to the PR above.

=============updated to======================

This proposal defines a “Group” as an [ERC-20](https://github.com/jamesavechives/ERCs/blob/a4d571a2d1ee5d5a47fe91870ed46c2032170a36/ERCS/eip-20.md) token where token balance represents membership level. Groups are standard ERC-20 tokens with the semantic interpretation that holding tokens means membership in the group. Unlike binary membership, this supports threshold-based membership: holding more tokens grants higher membership tiers or privileges. By being pure ERC-20, Groups inherit full compatibility with existing wallets, explorers, and tooling with no additional implementation burden.

The products :

Website : https://deakee.com

Android APP : [Deakee Codes](https://play.google.com/store/apps/details?id=com.deakee.android)

## Replies

**sullof** (2026-01-07):

Interesting proposal. From my perspective, the same functionality could be obtained by modifying ERC-721 or extending it with ERC-7656–style patterns. What is the motivation for also exposing an ERC-20 interface that appears potentially misleading?

---

**jamesavechives** (2026-01-09):

Thanks for the thoughtful review.

### Why not extend ERC‑721 (or ERC‑7656‑style patterns)?

ERC‑8063 is intentionally **not token‑based**. ERC‑721/1155 extensions still frame the primitive as “ownership of a token,” which brings along token semantics (token IDs, approvals, enumerable assumptions, marketplace expectations, etc.). A group, in our view, is a **first‑class on‑chain container/identity** identified by its **contract address**, with a minimal membership surface (`addMember`, `leaveGroup`, `transferMembership`, `isMember`). That keeps the primitive:

- token‑agnostic (no token IDs, no scarcity assumptions),
- lightweight for integrators (one membership check),
- composable with existing standards (resources can be associated externally like with any address).

You *can* model membership via ERC‑721/1155, but it’s a different abstraction: **“you own a token”** vs **“you are a member of a group.”** ERC‑8063 aims to standardize the latter directly.

### Motivation for the ERC‑20 interface (and why it’s optional)

The ERC‑20 interface is **explicitly optional** and meant as an **interoperability shim**, not as “this is a fungible token.” Many existing tools/protocols already accept ERC‑20 inputs (portfolios, accounting, distribution contracts, governance modules, indexers). Exposing an ERC‑20 view with `decimals = 0` and strict invariants (balances in {0,1}, transfer amount must be 1, supply == member count) allows those systems to integrate membership with minimal custom code.

To avoid misleading semantics, the spec constrains behavior so it’s clear this is a **membership tokenization adapter**:

- balances are binary (member/non‑member),
- transfers represent membership handoff,
- optional and implementations may omit it entirely.

So the motivation is **compatibility with existing ERC‑20‑centric infrastructure**, while keeping the *core* primitive membership‑centric and minimal.

Happy to clarify in the text further if you think the “optional compatibility shim” framing should be stronger.

---

**SamWilsn** (2026-01-28):

> Group creation: Upon creation or initialization, the contract MUST set the deployer (or initializer) as the group owner and initial member.

Why? This seems overly restrictive and unnecessary to standardize.

Trivial counter example would be a Group that takes the initial member as a constructor argument. I see no reason why that should be prevented.

Further, initialization/construction is generally considered a “privileged” operation, in the sense that the person doing the initialization/construction is intimately familiar with the operation of the contract, and therefore doesn’t need a standard to interact with it. A group member’s wallet, for example, doesn’t ever need to care about the signature of the constructor, only the functions in the contract’s public interface. It doesn’t matter where the initial member came from because all the other functions work the same regardless.

---

**SamWilsn** (2026-01-28):

Similarly, if `addMember` can only be called by the group owner, then there’s little reason to standardize it.

On the flip side, I do think there’s value in having a standardized membership management interface, so maybe relaxing the “Only the group owner […]” part might be more desirable?

---

**SamWilsn** (2026-01-28):

> Membership transfer: Any member (except the owner) MAY call transferMembership to transfer their membership to a non-member address. The caller MUST lose membership, the recipient MUST become a member, and MembershipTransferred MUST be emitted. Member count remains unchanged.

Would adding an acceptance handshake be good practice here? Assuming, Bob is a member and Alice is not:

1. Bob calls offerTransfer(Alice, expiry).

This does not remove Bob’s membership, nor does it grant Alice membership.
2. Alice calls acceptTransfer(Bob).

Bob loses membership, Alice gains membership.

I could also see a `revokeOffer`?

This way you can’t accidentally transfer your membership to a contract that can’t use it, nor can you force join someone to a group they don’t necessarily want to be a part of.

I’m just musing out loud here, and I haven’t really thought through any security considerations here.

---

**SamWilsn** (2026-01-28):

Instead of rolling your own ownership interface, you could look at [ERC-173: Contract Ownership Standard](https://eips.ethereum.org/EIPS/eip-173) or even [ERC-8023: Multi-step Contract Ownership](https://eips.ethereum.org/EIPS/eip-8023)?

I suppose the most general thing to do would be to omit ownership entirely from ERC-8063, and have a role-based approach with `function canAddMember(address account) returns (bool)` instead of a single owner.

---

And thinking about this for a moment longer, why have `addMember` but not `removeMember`? You briefly touch on this in your rationale, but I don’t think your argument is consistent:

> Voluntary exit only: Members can leave voluntarily via leaveGroup() or transfer their position, but cannot be forcibly removed by the owner. This prevents centralization and ensures membership stability, similar to how ERC-20 token holders cannot have their tokens revoked.

ERC-20 doesn’t specify minting or burning at all. It’s absolutely allowed by the standard to burn someone else’s tokens.

---

**SamWilsn** (2026-01-28):

God, sorry for the spam here…

Now that I’ve read the whole document, this is just ERC-20 with balance capped at one. Instead of defining a separate standard and layering ERC-20 over top, go in the other direction.

Start with ERC-20 for maximum compatibility, then add [ERC-5679: Token Minting and Burning](https://eips.ethereum.org/EIPS/eip-5679) for `mint`/`burn`, and if you really want the friendly function names, define them in terms of `transfer`, `mint`, and `burn`:

- isMember(a) → return balanceOf(a) >= 1
- getMemberCount() → return totalSupply()
- addMember(a) → mint(a, 1, hex"")
- leaveGroup() → burn(msg.sender, 1, hex"")
- transferMembership(a) → transfer(a, 1)

Plus the invariant you’ve already defined:

> All operations MUST preserve the invariant that no account’s balance exceeds 1

If you go in this direction, all of the tooling that works for ERC-20 will Just Work™ for Groups.

---

**jamesavechives** (2026-01-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamesavechives/48/12871_2.png) jamesavechives:

> by its contract address) and has an owner, an extensible set of members, and optional metadata. The standard defines a minimal interface for direct member management and membership introsp

You’re right that constructor/initialization behavior is a privileged operation and doesn’t affect how clients interact with the deployed contract. Standardizing it with MUST is overly prescriptive when it doesn’t impact interoperability.

The intent was to ensure groups are never left in an ownerless state after deployment, but I agree the spec shouldn’t dictate *how* that’s achieved.

I’ll revise this section to focus on the post-deployment invariant rather than the initialization mechanism:

> After initialization completes, the contract MUST have at least one member with owner privileges. The contract MUST emit a MemberAdded event for each initial member.

This preserves the safety property (no ownerless groups) while allowing flexibility for:

- Factory contracts deploying on behalf of users
- Constructor arguments specifying initial members
- Proxy/clone patterns with custom initialization

---

**jamesavechives** (2026-01-30):

Good point about the acceptance handshake. You’re right that direct transfer has two risks:

1. Forcing membership on unwilling parties
2. Transferring to contracts that can’t interact with the group

A few thoughts:

**The ERC-20 compatibility layer already provides this pattern** — implementations that expose the optional ERC-20 interface get approve/transferFrom, which is effectively the same handshake:

- Bob calls approve(Alice, 1)
- Alice calls transferFrom(Bob, Alice, 1)

**For the core interface**, I’m inclined to keep direct transfer for simplicity (follows the “minimal core, rich extensions” philosophy). But I could add a non-normative note about the consent pattern for implementations that want it:

> **Optional: Consent-based transfers**

> Implementations MAY add an acceptance handshake for transfers:

> - offerTransfer(address to, uint256 expiry) — Creates pending offer, does not transfer

> - acceptTransfer(address from) — Recipient accepts, transfer completes

> - revokeOffer() — Cancels pending offer

>

> This prevents forcing membership on unwilling parties and transferring to incompatible contracts.

---

**jamesavechives** (2026-01-30):

Good catches on both points.

**On ownership:** You’re right that if access control is implementation-defined via canAddMember(), mandating a single owner() is inconsistent. I’m considering two approaches:

1. Remove owner() from the core interface entirely — implementations that want ownership can use ERC-173 or ERC-8023. The core interface becomes purely about membership.
2. Keep owner() but make it optional — some groups have owners, some are governed differently.

Leaning toward (1) for consistency with the role-based direction.

**On removeMember:** You’re correct that the ERC-20 analogy doesn’t hold — ERC-20 doesn’t prevent burning. The “no forced removal” was a design choice for membership stability, not a technical constraint.

Given that addMember access control is now implementation-defined, it would be more consistent to add removeMember(address) + canRemoveMember(address caller, address member) with the same philosophy: implementations define their own policy (owner-only, governance, no removal, etc.).

---

**jamesavechives** (2026-01-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Plus

Thanks for your good point!

Maybe we can take it as pure ERC-20 token, but just the purpose is not for coins, but for groups :

This proposal defines a “Group” as an [ERC-20](https://github.com/jamesavechives/ERCs/blob/a4d571a2d1ee5d5a47fe91870ed46c2032170a36/ERCS/eip-20.md) token where token balance represents membership level. Groups are standard ERC-20 tokens with the semantic interpretation that holding tokens means membership in the group. Unlike binary membership, this supports threshold-based membership: holding more tokens grants higher membership tiers or privileges. By being pure ERC-20, Groups inherit full compatibility with existing wallets, explorers, and tooling with no additional implementation burden.


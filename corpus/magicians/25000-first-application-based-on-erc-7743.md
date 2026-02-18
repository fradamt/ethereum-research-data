---
source: magicians
topic_id: 25000
title: First Application Based On ERC-7743
author: jamesavechives
date: "2025-08-04"
category: ERCs
tags: [token]
url: https://ethereum-magicians.org/t/first-application-based-on-erc-7743/25000
views: 65
likes: 0
posts_count: 3
---

# First Application Based On ERC-7743

Hello! I just created a website called MO-NFT (https://monft.io), which is the first application based on ERC-7743 and ERC-7837.

In ERC-7743, if A transfers a token to B, both A and B will be owners of the token. Based on this principle, I built a downloadable assets platform, and here is how it works:

Step 1: Any creator can upload assets to the platform.

Step 2: Once the asset is approved by the centralized admin, the creator can mint an ERC-7743 token for it.

Step 3: The creator can transfer the ERC-7743 token to anyone. Anyone who owns the token can transfer it to others while still keeping ownership of the token.

Step 4: Anyone who owns the token can list the asset on the marketplace for sale. There are flexible payment methods for sellers—not just crypto, but also fiat, depending on the seller. Please note that one asset can be listed by multiple sellers with multiple payment methods simultaneously, which is not possible in traditional marketplaces.

Step 5: Any owner can download the asset directly.

Please let me know if you are interested or if you have any suggestions!

Thank you for your attention!

## Replies

**devender-startengine** (2025-11-02):

In 7743, `transferFrom` is *additive* (A remains an owner while B is added). That differs from the conservation invariant of ERC‑721 (“ownership is a single, conserved state per `tokenId` )

Would it be more precise to treat this operation as `addOwner` (or `share` ) rather than `transfer` , and reserve `transfer` for exclusive ownership handoff?

Do you define formal invariants such as monotonicity (“owner set is non‑decreasing except for irreversible archiving”) and idempotence (“re‑adding an existing owner reverts”)? It would be helpful to see a short list of invariants and the specific events that must hold after each state transition.

---

**jamesavechives** (2025-11-03):

[@devender-startengine](/u/devender-startengine)

Thanks—great points. Since ERC‑7743 is finalized, its additive `transferFrom` semantics are fixed. To address naming clarity and formal reasoning, I proposed a general‑purpose “Group” container as ERC‑8063 that subsumes 7743’s pattern.

- Naming in 8063: I use addMember/“share” for additive joins, and reserve transfer only for an optional extension that models exclusive handoff (not in the base).
- Back‑compat mapping: In 8063 terms, 7743’s transferFrom == addMember. Indexers/wallets should not treat it like ERC‑721’s exclusive transfer.
- Core invariants (8063):

Uniqueness: membership is a set (no duplicates).
- Idempotence: adding an existing member reverts.
- Monotonicity: member set is non‑decreasing except for explicit removeMember/renounce/archive.
- Existence: a group “exists” iff the member set is non‑empty.
- Authorization: creator initializes; current members can addMember (configurable by policy).

Events (8063): `MemberAdded`, `MemberRemoved`, `Archived`. A 7743‑compat shim can emit these alongside existing events for indexer clarity.

I’m happy to fold a short “Invariants and Events” section into the 8063 write‑up and clarify the 7743→8063 mapping. Feedback welcome on duplicate‑add behavior (revert vs no‑op), default authorization, and whether `renounce` should be mandatory.

Discussion: [ERC‑8063: Groups — multi‑member onchain containers for shared resources](https://ethereum-magicians.org/t/erc-8063-groups-multi-member-onchain-containers-for-shared-resources/25999)


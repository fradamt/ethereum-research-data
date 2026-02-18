---
source: magicians
topic_id: 27388
title: Add Optional “Upgrade” Field to Standards Track Core EIPs
author: poojaranjan
date: "2026-01-05"
category: EIPs > EIPs core
tags: [core-eips, core-devs]
url: https://ethereum-magicians.org/t/add-optional-upgrade-field-to-standards-track-core-eips/27388
views: 67
likes: 6
posts_count: 6
---

# Add Optional “Upgrade” Field to Standards Track Core EIPs

This is a proposal open for discussion to add an optional `upgrade` field to Standards Track Core EIPs.

## Problem Statement

At present, it is difficult to clearly identify **which finalized Standards Track Core EIPs were deployed with which Ethereum network upgrade** by looking at the `Final` EIP itself.

While this mapping is possible through:

- Upgrade Meta EIPs,
- Network upgrade announcements, or
- External tools and dashboards (such as custom UIs built by the EIPsInsight),

This information is **not directly visible on the [official EIP document](https://eips.ethereum.org/EIPS/eip-1559)**. The official EIP repository lacks a simple, authoritative way to link a `Final` Standards Track Core EIP to its activating upgrade.

This creates unnecessary friction for users trying to understand protocol evolution, upgrade scope, and historical context. As a result, developers, protocol testing team and other community participants frequently reach out requesting an easier way to identify the upgrade name.

## The Proposal (Specification)

This proposal defines an optional `Upgrade` field in the [EIP preamble](https://github.com/ethereum/EIPs/blob/master/eip-template.md) with the following semantics.

- The Upgrade field is optional and informational.
- It is applicable only to Standards Track – Core EIPs.
- The field MUST NOT be present during the Draft, Review, or Last Call statuses.
- The field MUST be added only when an EIP transitions from Last Call to Final status.
- The field MUST specify the name of the Ethereum Network Upgrade in which the EIP was deployed.
- The Upgrade field may be retroactively added to all finalized Standards Track Core EIPs that were included in previous Meta EIPs.
- EIPs that were activated asynchronously (i.e., not tied to a specific network upgrade) would not receive this field.

Responsibility for adding this field would lie with the EIP co-authors or EIP champion.

### Next steps

- Document the addition of this new “field” (trivial process change) via an EIP.
- Update EIP template to add “upgrade” to preamble
- Update EIP-1 providing authoring and editorial guidelines to:

Clarify when and how the Upgrade field should be added.
- Emphasize that it is optional and informational, not normative.

This proposal aims to improve **clarity, discoverability, and historical accuracy** of Ethereum protocol changes without altering EIP lifecycle semantics or adding burden on authors or EIP editors during early proposal stages.

The proposal is the outcome of [EIPIP #122](https://ethereum-magicians.org/t/eipip-meeting-122-dec-17-2025/25913/2), where call participants agreed to bring it forward for broader input from authors, developers, and the community. It is **open for further discussion and feedback**, particularly from EIP editors, client teams, and tooling maintainers.

---

However, after giving some more thought during the holiday season, I came up with multiple  flavors of this proposal documented [here](https://hackmd.io/@poojaranjan/EIPforUpgrade).

Adding summary for quick reference

### Meta EIPs for Network Upgrade Coordination — Proposal Options

| Proposal | What It Adds | Who It Applies To | When Field Appears | When Field Is Removed | Key Benefit | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1A | Upgrade field | Standards Track Core EIPs only | From Last Call to Final only | Async finalized Core EIPs | Clear historical record of which upgrade deployed a Core EIP | Agreed (EIPIP Dec 2025) |
| 1B | Upgrade field | All EIPs listed in an upgrade Meta EIP | Draft → Final (added after initial Draft) | Removed from all non-Core EIPs at Final; removed if Stagnant or Withdrawn | Early visibility of upgrade association across all EIPs | Proposed |
| 2A | Stage field | Standards Track Core EIPs only | Draft → Final (added after initial Draft) | Removed if Stagnant or Withdrawn | Tracks upgrade readiness of Core EIPs during planning | Proposed |
| 2B | Stage field | All EIPs listed in an upgrade Meta EIP | Draft → Final (added after initial Draft) | Removed if Stagnant or Withdrawn | End-to-end visibility of EIP maturity across upgrades | Previously discussed (no consensus) |
| 3A | Stage + Upgrade fields | Standards Track Core EIPs only | Draft → Final (added after initial Draft) | Both removed if Stagnant or Withdrawn | Combines planning visibility and final attribution for Core EIPs | Proposed |
| 3B | Stage + Upgrade fields | All EIPs listed in an upgrade Meta EIP | Draft → Final | Remove stage and upgrade from all non-Core EIPs at Final; Stage and upgrade removed if Stagnant or Withdrawn irrespective of type;Upgrade and stage retained only for Core EIPs at Final | Maximum transparency across planning and deployment | Proposed |

Thank you for reading this long post. I sincerely appreciate your feedback  ![:folded_hands:](https://ethereum-magicians.org/images/emoji/twitter/folded_hands.png?v=15)

## Replies

**abcoathup** (2026-01-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> Clear historical record of which upgrade deployed a Core EIP

The clear historical record should be the Network Upgrade Meta EIP, to show **upgrade** and **stage**.

We should avoid duplicating information wherever possible, to avoid divergence or confusion on what is the correct information.

Ideally any website (including [eips.ethereum.org](http://eips.ethereum.org)) would use the Network Upgrade Meta EIP to obtain this information.  If we absolutely can’t do this automagically, then we should have the bare minimum, which is an upgrade field set only when EIPs are set to final.  (1A)

---

**SamWilsn** (2026-01-05):

I’m fine with *rendering* upgrade information on the individual proposals, but the source of truth should always be the fork meta EIPs.

It wouldn’t need any interaction with the EIP status. If Glamsterdam’s fork meta EIP lists proposal 1234, then proposal 1234’s page shows `Glamsterdam: CFI` (or whatever).

---

**poojaranjan** (2026-01-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I’m fine with rendering upgrade information on the individual proposals, but the source of truth should always be the fork meta EIPs.

If you have a preference from above the table, please let us know.

As we understand, only `Core` EIPs are deployed at the time of upgrade.

1. Would you want to limit it to
a. Standards Track Core Only?
b. Core and Others mentioned in Meta?
2. Any thoughts on CoreEIP deployed out of the scheduled upgrade?
3. Would you be open to adding stage field as well for clarity?

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> It wouldn’t need any interaction with the EIP status. If Glamsterdam’s fork meta EIP lists proposal 1234, then proposal 1234’s page shows Glamsterdam: CFI (or whatever).

Agreed. Status is added for clarity purposes.

---

**SamWilsn** (2026-01-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> If you have a preference from above the table, please let us know.

None. These all require modifying the feature proposal, as far as I understand them.

I’d like Jekyll, or whatever renderer we end up using, to parse network upgrade EIPs and add the links from feature EIP to network upgrade EIP on the fly.

---

**abcoathup** (2026-01-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I’d like Jekyll, or whatever renderer we end up using, to parse network upgrade EIPs and the links from feature EIP to network upgrade EIP on the fly.

![:partying_face:](https://ethereum-magicians.org/images/emoji/twitter/partying_face.png?v=15)

Awesome, no data duplication, let the renderer do it.

I’ve created an Issue



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/11036)












####



        opened 11:24PM - 06 Jan 26 UTC



        [![](https://avatars.githubusercontent.com/u/28278242?v=4)
          abcoathup](https://github.com/abcoathup)










Render network upgrade as label on EIPs that are included in a Network Upgrade M[…]()eta EIP.

For example [EIP-7594](https://eips.ethereum.org/EIPS/eip-7594) PeerDAS was included in Network Upgrade Meta EIP: [EIP-7606](https://eips.ethereum.org/EIPS/eip-7607) Hardfork Meta - Fusaka and should have a label.

<img width="1014" height="334" alt="Image" src="https://github.com/user-attachments/assets/3b87ad7d-31a4-48af-93a5-70b0a4fc3f13" />

For background see: https://ethereum-magicians.org/t/add-optional-upgrade-field-to-standards-track-core-eips/27388


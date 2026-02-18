---
source: magicians
topic_id: 25027
title: Prebuilt Integration of Community-Selected Metamask Snaps
author: blockdev
date: "2025-08-06"
category: Web > Wallets
tags: [wallet, ux, snaps]
url: https://ethereum-magicians.org/t/prebuilt-integration-of-community-selected-metamask-snaps/25027
views: 47
likes: 1
posts_count: 1
---

# Prebuilt Integration of Community-Selected Metamask Snaps

## eip: XXXX
title: Prebuilt Integration of Community-Selected MetaMask Snaps
author: @Obies
status: Draft
type: Standards Track
category: Interface
created: 2025-08-03
requires: 4824

## Simple Summary

This proposal suggests that MetaMask natively include a curated catalog of community-developed Snaps as **prebuilt**, opt-in features similar to using a web2 app for personalization. These Snaps would not require third-party installation and would be accessible from within the MetaMask UI, streamlining advanced wallet functionality.

## Abstract

MetaMask Snaps are powerful modular extensions, yet their adoption is hindered by the need for external discovery and installation. This EIP proposes that trusted community-built Snaps be made accessible directly from the MetaMask interface as opt-in, *pre-included tools*. These would be reviewed, audited, and curated under a transparent governance model and made available in a dedicated “Trusted Tools” section inside MetaMask.

## Motivation

Many popular Snaps already improve MetaMask by adding support for features like transaction simulation, gas insights, L2 compatibility, or account abstraction previews. However, current UX places too much friction on users.

By pre-including vetted Snaps in the wallet UI:

- Users gain easier access to advanced tools
- Snap developers receive greater exposure
- The wallet grows its feature set without compromising modularity

## Specification

### MetaMask UX Behavior

- MetaMask includes a “Trusted Tools” section in the settings-General wallet interface.
- This section displays a list of curated Snaps available for one-click activation.
- Snaps are pre-selected user enabled by default** until explicitly disabled by the user.
- Users are informed of Snap permissions, authors, and purpose before activation.

### Snap Curation Process

- A Snap Inclusion Working Group (SIWG) will manage the curation process.
- Inclusion criteria:

Open-source code
- Passed independent security audit
- Demonstrates utility, adoption, and user demand

### Developer Distribution

- Developers must submit their Snap for consideration via GitHub or Magicians forum.
- If accepted, the Snap will be version-pinned and reviewed before every update.

### Security Measures

- All included Snaps must:

Be sandboxed
- Avoid network access unless required
- Pass MetaMask Snap lifecycle tests

## Rationale

This proposal balances the benefits of decentralization with the user experience demands of modern Web3 apps. It encourages ecosystem contributions without over-centralizing control, by establishing an opt-in, audited, and transparent pre-install mechanism.

## Backwards Compatibility

This EIP does not affect any existing Snap behavior. Manual Snap installations remain fully supported. This proposal only enhances discoverability and UX by reducing user setup complexity.

## Test Cases

- User installs MetaMask.
- Enables “Transaction Simulator Snap”.
- Signs a transaction and receives simulation feedback — all without needing to install anything externally.

## Security Considerations

- Snaps must be audited and version-controlled.
- Only signed and pinned versions of Snaps are distributed.
- The opt-in model prevents unexpected changes or automatic behavior.

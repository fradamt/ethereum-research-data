---
source: magicians
topic_id: 23205
title: Ethereum Distribution System
author: peersky
date: "2025-03-20"
category: Magicians > Primordial Soup
tags: [factories]
url: https://ethereum-magicians.org/t/ethereum-distribution-system/23205
views: 87
likes: 0
posts_count: 1
---

# Ethereum Distribution System

We’re seeking feedback on the Ethereum Distribution System (EDS), a project aimed at generalizing smart contract factory interfaces. You can find the code on GitHub: https://github.com/peeramid-labs/eds

## Core Concept: Generalized Smart Contract Factories

EDS introduces the concept of `Distribution` and versioned `Repository` smart contracts, offering a standardized alternative to custom factory solutions. Developers can leverage these pre-built packages instead of reinventing the wheel.

**Key Features and Benefits:**

- Generalized Factory Interfaces:

Create Distribution or versioned Repository packages, eliminating the need for custom factory solutions.

**Decentralized Listing:**

- Anyone can list packages by implementing the Distributor contract, fostering an open and permissionless ecosystem.

**Monetization and Control:**

- Distributors can monetize instantiation, manage package listings, and control version requirements, providing a flexible and sustainable model.

**Enhanced Security and Interoperability:**

- ERC7746 (O(1) Vulnerability Management): Distributors can efficiently manage vulnerabilities.
- ER7744 (Immutable Distributed Sources): Ensure trust and transparency by enshrining immutable source code.
- Versioned Repositories (SemVer): Developers and users benefit from industry-standard semantic versioning for seamless upgrades.
- Trusted Ecosystems: Contracts within the same distribution can leverage ERC-7746 hooks for robust authorization management.
- Reusability and Modular Design: Enables the creation of complex applications by packaging and reusing different projects within the EDS framework.

**User-Driven Upgradability:**

- EDS shifts the paradigm from developer-centric to user-centric upgrades.
- Distributors and developers collaborate on new versions, making them available through the Distributor contract.
- Users have the autonomy to disable trusted distributor checks and manage their instantiated infrastructure at their own risk.
- When the normal upgrade path is followed, dApps can display a simple “Upgrade to Latest” call to action.

**Storage Migrations:**

- Planned support for storage migrations (see milestone 2).

We have also added basic support to our  [SDK](https://github.com/peeramid-labs/sdk) which includes client library using `viem` & CLI:

```bash
peeramid distributions --help
Usage: peeramid distributions [options] [command]

Manage distributions

Options:
  -h, --help        display help for command

Commands:
  list [options]    List all distributions
  add [options]     Add a new distribution
  state [options]   Get the state of a distribution
  remove [options]  Remove a distribution
  help [command]    display help for command
```

# Request for “Yay”

This project is driven by passion and a vision for a more efficient and secure Ethereum ecosystem. As an unfunded initiative, your support is crucial.

**We’re seeking your feedback and “yay” to demonstrate community interest and traction, which will be invaluable when seeking funding from organizations like the Ethereum Foundation and Gitcoin.**

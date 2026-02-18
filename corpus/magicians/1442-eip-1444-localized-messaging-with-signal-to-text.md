---
source: magicians
topic_id: 1442
title: "EIP-1444: Localized Messaging with Signal-to-Text"
author: expede
date: "2018-09-24"
category: EIPs
tags: [ux, erc-1066, erc-1444]
url: https://ethereum-magicians.org/t/eip-1444-localized-messaging-with-signal-to-text/1442
views: 3455
likes: 2
posts_count: 1
---

# EIP-1444: Localized Messaging with Signal-to-Text

After consultation with the community, localized messages is being expanded and split into [its own EIP (1444)](https://github.com/ethereum/EIPs/pull/1444) ![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=15)  This standard allows anyone to convert machine-efficient messages to human-readable codes, directly on the EVM! It does not create a central registry for translations, opting instead for decentralized localizations for a variety of purposes. We’re attempting to keep this EIP small, and other are free to build on top of it.

We do see there being more widely used deployments of ERC-1444, such as connecting [erc-1066](/tag/erc-1066) with wallets, debuggers, and other tools.

# Excerpts from the EIP

There are many cases where an end user needs feedback or instruction from a smart contact. Directly exposing numeric codes does not make for good UX or DX. If Ethereum is to be a truly global system usable by experts and lay persons alike, systems to provide feedback on what happened during a transaction are needed in as many languages as possible.

Returning a hard-coded string (typically in English) only serves a small segment of the global population. This standard proposes a method to allow users to create, register, share, and use a decentralized collection of translations, enabling richer messaging that is more culturally and linguistically diverse.

There are several machine efficient ways of representing intent, status, state transition, and other semantic signals including booleans, enums and [ERC-1066 codes](https://eips.ethereum.org/EIPS/eip-1066). By providing human-readable messages for these signals, the developer experience is enhanced by returning easier to consume information with more context (ex. `revert`). End user experience is enhanced by providing text that can be propagated up to the UI.

```diagram
                                                                   +--------------+
                                                                   |              |
                                                          +------> | Localization |
                                                          |        |              |
                                                          |        +--------------+
                                                          |
                                                          |
+-----------+          +-------------------------+        |        +--------------+
|           |          |                         |  | LocalizationPreferences |  | Localization |
|           |          |                         |  | Localization |
                                                                   |              |
                                                                   +--------------+
```

---
source: magicians
topic_id: 13788
title: "[Working draft] ERC-XXXX: Minimal Beacon proxy"
author: radek
date: "2023-04-11"
category: EIPs
tags: [erc, proxy-contract]
url: https://ethereum-magicians.org/t/working-draft-erc-xxxx-minimal-beacon-proxy/13788
views: 747
likes: 2
posts_count: 1
---

# [Working draft] ERC-XXXX: Minimal Beacon proxy

Hello everyone,

I wanted to share an idea I’ve been working on for a new efficient proxy design for Ethereum smart contracts. Currently, there are limitations with the existing proxy design, including inefficiency, potential security concerns, and limited upgradeability options.

When using the Upgradeable Proxy Standard (UUPS), the implementation reference is stored in a storage slot on the proxy, which presents a potential security concern as an attacker could manipulate the reference to point to a malicious contract. Or the governance can point the reference to the wrong address thus eliminating the possibility to fix the implementation change.

While ERC1167 provides an efficient minimal proxy design, it has limitations in terms of upgradeability as it relies on storing the constant implementation address on the proxy itself.

To address these issues, I propose a minimal proxy design with Beacon call for implementation address. This design is based on ERC1167 for its efficiency, but has been extended by calling the Beacon contract in order to provide an upgrade option and separate the security concern of storing the implementation reference.

At a high level, this design would consist of the following elements:

- A minimal proxy contract: This contract would serve as a lightweight intermediary between the client and the implementation contract. Its primary purpose would be to keep the storage and forward function calls from the client to the implementation contract - like ERC1167.
- A Beacon contract: This contract would store the implementation address and would be responsible for updating the proxy contract with a new implementation address when an upgrade is required. The fallback function of the Beacon contract would reply with the implementation address to reduce the  calldata required to retrieve the address and improve efficiency.
- No related requirement on the implementation contract: This design does not require any specific storage slots or state variables to be present for the implementation contract. However depending on the concrete application an initiation call might be required as with any other proxy - implementation pattern.

I would love to hear feedback and suggestions from the Ethereum community on this proposal, and I am open to discussing any potential limitations or risks associated with the design. Thank you for your time and consideration.

Best,

Radek

---
source: magicians
topic_id: 20958
title: "ERC-7763: App Keys for Fully Embedded Accounts"
author: danfinlay
date: "2024-09-04"
category: ERCs
tags: [provider-ring]
url: https://ethereum-magicians.org/t/erc-7763-app-keys-for-fully-embedded-accounts/20958
views: 249
likes: 6
posts_count: 2
---

# ERC-7763: App Keys for Fully Embedded Accounts

As we build infrastructure that facilitates embedded wallets, sites have a new opportunity to manage keys to manage permissions they receive (like via ERC-7715).

Alternatively, the site may want to defer key backup to the wallet, while still wanting the benefits of being able to sign on their own behalves.

This is one extremely minimal initial approach to granting sites key material that is deterministically generated to them. It probably needs some refinement in its algorithm, but can be treated as a general outline of an approach for consideration even in this initial draft form.

https://github.com/ethereum/ERCs/pull/615

## Replies

**polymutex** (2024-09-14):

Good idea. Embedded wallets threaten user self-sovereignty and fragment the ecosystem and we need a solution to prevent that from happening.

I concur that the current proposed address generation scheme needs refinement though. The proposal currently states:

> Use the BIP-44 purpose field 44'
> Use coin type 60' for Ethereum
> Use 0' for account index
> Use the first 4 bytes of keccak256 hash of the app’s origin (domain) for change level
> Use the provided nonce (or 0 if not provided) for address index

As the origin-specific parts of the derivation path being limited to only 4 bytes, that seems a bit too easy to find collisions with others. Needs more bits to avoid this. It may also be wise to use a different coin type or (large) account index, just to avoid the risk of ever conflicting with traditional walelt derivation paths even if someone were to bruteforce an origin for which the relevant part of the hash is `0`.

I also think how the `origin` is determined needs to be specified further. Using DNS names is problematic, because that enshrines DNS as a source of truth. DNS is prone to censorship and malicious domain name transfers. Domain names also sometimes change for legitimate reasons, e.g. rebrands. Users may want to use local/IPFS-based frontends, which don’t have a domain.

In my opinion, this proposal would pair well with ERC-6860 (onchain app frontends); as the `origin` can be well-defined as being the `contractName` part of the ERC-6860 URL of the frontend. This would mean either an ENS name, or simply a contract address, but either way `origin` would be unambiguously derived from onchain truth. For frontends that aren’t onchain, there could be a separate ERC that specifies a function a contract may implement to delegate authority to one or more DNS domain names.


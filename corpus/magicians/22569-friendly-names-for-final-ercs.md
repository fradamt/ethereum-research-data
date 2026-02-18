---
source: magicians
topic_id: 22569
title: Friendly names for Final ERCs
author: abcoathup
date: "2025-01-17"
category: ERCs
tags: [friendly-name]
url: https://ethereum-magicians.org/t/friendly-names-for-final-ercs/22569
views: 104
likes: 5
posts_count: 3
---

# Friendly names for Final ERCs

| ERC | Friendly name |
| --- | --- |
| 20 | Fungible Tokens |
| 55 | Mixed-case checksum address encoding |
| 137 | Ethereum Domain Name Service - Specification |
| 162 | Initial ENS Hash Registrar |
| 165 | Standard Interface Detection |
| 173 | Contract Ownership Standard |
| 181 | ENS support for reverse resolution of Ethereum addresses |
| 190 | Ethereum Smart Contract Packaging Standard |
| 191 | Signed Data Standard |
| 223 | Token with transaction handling model |
| 600 | Ethereum purpose allocation for Deterministic Wallets |
| 601 | Ethereum hierarchy for deterministic wallets |
| 681 | URL Format for Transaction Requests |
| 721 | Non-Fungible Tokens (NFTs) |
| 777 | Token Standard |
| 820 | Pseudo-introspection Registry Contract |
| 1046 | tokenURI Interoperability |
| 1155 | Multi Token Standard |
| 1167 | Minimal Proxy Contract |
| 1271 | Standard Signature Validation Method for Contracts |
| 1328 | WalletConnect URI Format |
| 1363 | Payable Token |
| 1820 | Pseudo-introspection Registry Contract |
| 1967 | Proxy Storage Slots |
| 2098 | Compact Signature Representation |
| 2135 | Consumable Interface (Tickets, etc) |
| 2309 | ERC-721 Consecutive Transfer Extension |
| 2535 | Diamonds, Multi-Facet Proxy |
| 2612 | Permit Extension for EIP-20 Signed Approvals |
| 2678 | Revised Ethereum Smart Contract Packaging Standard (EthPM v3) |
| 2771 | Secure Protocol for Native Meta Transactions |
| 2981 | NFT Royalty Standard |
| 3156 | Flash Loans |
| 3448 | MetaProxy Standard |
| 3475 | Abstract Storage Bonds |
| 3525 | Semi-Fungible Token |
| 3643 | T-REX - Token for Regulated EXchanges |
| 3668 | CCIP Read—Secure offchain data retrieval |
| 4400 | EIP-721 Consumable Extension |
| 4519 | Non-Fungible Tokens Tied to Physical Assets |
| 4626 | Tokenized Vaults |
| 4804 | Web3 URL to EVM Call Message Translation |
| 4834 | Hierarchical Domains |
| 4844 | Protodanksharding |
| 4906 | EIP-721 Metadata Update Extension |
| 4907 | Rental NFT, an Extension of EIP-721 |
| 4955 | Vendor Metadata Extension for NFTs |
| 5006 | Rental NFT, NFT User Extension |
| 5007 | Time NFT, ERC-721 Time Extension |
| 5023 | Shareable Non-Fungible Token |
| 5169 | Client Script URI for Token Contracts |
| 5192 | Minimal Soulbound NFTs |
| 5202 | Blueprint contract format |
| 5219 | Contract Resource Requests |
| 5267 | Retrieval of EIP-712 domain |
| 5313 | Light Contract Ownership |
| 5375 | NFT Author Information and Consent |
| 5380 | ERC-721 Entitlement Extension |
| 5484 | Consensual Soulbound Tokens |
| 5489 | NFT Hyperlink Extension |
| 5507 | Refundable Tokens |
| 5521 | Referable NFT |
| 5528 | Refundable Fungible Token |
| 5564 | Stealth Addresses |
| 5570 | Digital Receipt Non-Fungible Tokens |
| 5585 | ERC-721 NFT Authorization |
| 5606 | Multiverse NFTs |
| 5615 | ERC-1155 Supply Extension |
| 5625 | NFT Metadata JSON Schema dStorage Extension |
| 5646 | Token State Fingerprint |
| 5679 | Token Minting and Burning |
| 5725 | Transferable Vesting NFT |
| 5732 | Commit Interface |
| 5750 | General Extensibility for Method Behaviors |
| 5773 | Context-Dependent Multi-Asset Tokens |
| 6059 | Parent-Governed Nestable Non-Fungible Tokens |
| 6066 | Signature Validation Method for NFTs |
| 6105 | No Intermediary NFT Trading Protocol |
| 6147 | Guard of NFT/SBT, an Extension of ERC-721 |
| 6150 | Hierarchical NFTs |
| 6220 | Composable NFTs utilizing Equippable Parts |
| 6239 | Semantic Soulbound Tokens |
| 6381 | Public Non-Fungible Token Emote Repository |
| 6454 | Minimal Transferable NFT detection interface |
| 6492 | Signature Validation for Predeploy Contracts |
| 6538 | Stealth Meta-Address Registry |
| 6672 | Multi-redeemable NFTs |
| 6808 | Fungible Key Bound Token |
| 6809 | Non-Fungible Key Bound Token |
| 6982 | Efficient Default Lockable Tokens |
| 7007 | Verifiable AI-Generated Content Token |
| 7053 | Interoperable Digital Media Indexing |
| 7066 | Lockable Extension for ERC-721 |
| 7092 | Financial Bonds |
| 7160 | ERC-721 Multi-Metadata Extension |
| 7201 | Namespaced Storage Layout |
| 7231 | Identity-aggregated NFT |
| 7401 | Parent-Governed Non-Fungible Tokens Nesting |
| 7409 | Public Non-Fungible Tokens Emote Repository |
| 7432 | Non-Fungible Token Roles |
| 7439 | Prevent ticket touting |
| 7528 | ETH (Native Asset) Address Convention |
| 7535 | Native Asset ERC-4626 Tokenized Vault |
| 7540 | Asynchronous ERC-4626 Tokenized Vaults |
| 7575 | Multi-Asset ERC-4626 Vaults |
| 7588 | Blob Transactions Metadata JSON Schema |

This is a wiki post, edit to improve friendly names, cleanup (e.g. remove EIPs)

[Proposed](https://warpcast.com/v/0x9493904d) by Varun Srinivasan

## Replies

**1etsp1ay** (2025-01-21):

The numbering scheme originated in GitHub issues tracker, now that we have 3 separate tracks, I would put forth the suggestion to cluster them for convenience. There are quite a few EIP/ERCs which have failed and for all intents and purposes, act as a blocked up (think unused IPv4). Whilst looking for a core to anchor it (ERC-20, 721 etc) I’d like to add on a commentary layer

# Market Accepted Practices

ERC-20 = MAP-20

- 1363 (payable) -1340 = MAP-23
- 2512 (approvals) -2490 = MAP-22
- 3156 (flash loans) - 3130 = remain ERC-3156 because it is a use-case

This is basically doing an aliasing mindmap for *convenience* of non-technical souls. Some suggested steps

- find out what are permanently dead EIP numbers in neighbourhood
- triage the existing ERCs for significance
- criteria might be at least 5 years since proposal, significant market uptake
- document good/bad practices using those standards
- foster debate around new proposals relative to objective data (if any)

---

**abcoathup** (2025-01-21):

Suggest moving this to a new topic.

EIPs/RIPs/ERCs are assigned numbers (since 7500) from a single sequential pool by editors & associates and are no longer the issue number.

ERC20/721/1155 feel ingrained (lets see if this is still the case in 20 years).

Whilst there are a number of gaps in numbering (I was keen for auctioning off low numbers), there wouldn’t be consistent enough room for a new taxonomy.

There is currently an open role for an ERC coordinator



      [jobs.lever.co](https://jobs.lever.co/ethereumfoundation/4ebdad29-6cea-4a03-804f-4a65b34b5ef6)



    ![image](https://lever-client-logos.s3.us-west-2.amazonaws.com/b4cfe414-b949-4989-b62f-e34bb1817ee3-1644535963284.png)

###



The Ethereum Foundation (EF) is a global non-profit organization dedicated to supporting Ethereum and related technologies. Our mission is to do what is best for Ethereum’s long-term success. Our role is to allocate resources to critical projects, to...


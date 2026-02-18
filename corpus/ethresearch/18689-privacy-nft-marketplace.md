---
source: ethresearch
topic_id: 18689
title: Privacy NFT Marketplace
author: terry
date: "2024-02-17"
category: Privacy
tags: [zk-roll-up]
url: https://ethresear.ch/t/privacy-nft-marketplace/18689
views: 2084
likes: 10
posts_count: 5
---

# Privacy NFT Marketplace

# Privacy NFT marketplace

## Introduction

In the rapidly evolving realm of Non-Fungible Tokens (NFTs), the need for privacy in ownership transactions has never been more crucial. Existing NFT marketplaces expose sensitive details on public blockchains, compromising user privacy. Our solution, the Privacy NFT Marketplace, introduces a pioneering approach using zk-SNARKs technology to safeguard user identities during NFT transactions.

This proposal outlines a secure and decentralized platform that leverages cryptographic proofs, allowing verifiable transactions without disclosing sensitive information. By prioritizing privacy through zk-SNARKs, our proposal addresses current privacy concerns in NFT ownership, fostering trust and confidence among users. This innovation aims to redefine the NFT landscape, encouraging broader adoption and contributing to the development of a privacy-centric NFT ecosystem.

## How it works

### Seller

**Step 1: Deposit NFT and Generate Nullifier**

- The seller initiates the process by depositing their NFT into the marketplace’s state Merkle tree and generates a new spending NFT nullifier associated with the deposited NFT.

**Step 2: Create Sell Order**

1. Public: Listing Information: The seller creates a sell order, providing essential information.

Collection Address: The address of the NFT collection.
2. Token ID: The unique identifier of the NFT.
3. Amount: The desired selling price.
4. Private: Generate Seller’s ERC20 Nullifier:

The seller generates a new spending ERC20 nullifier associated with the sale amount and a seller spending key.
5. Public: Spending NFT Proofs:

The seller creates proofs containing the collection address, token ID, spending NFT nullifier, and selling amount.

→ (Collection address, token id, amount, new seller’s ERC20 Nullifier hash, spending NFT Proofs)

### Buyer

**Step 1: Deposit ERC20 and Generate Nullifier**

- The buyer deposits ERC20 into the marketplace’s state Merkle tree and generates a new spending ERC20 nullifier associated with the deposited amount

**Step 2: Create Accept-Sell Order**

1. Listing Lookup and Information:

The buyer looks up the listing information on the public marketplace and decides to make a purchase.
2. The buyer creates an accept-sell order, providing necessary details.

Collection Address, Token ID, Amount.
3. Spending ERC20 Proofs:

The buyer generates proofs containing the collection address, token id and lists proofs of their spending ERC20 nullifier.
4. Generate New Buyer’s Nullifiers:

New Buyer Spending NFT Nullifier: Associated with the collection address, token ID, and buyer spending key.
5. New Buyer Spending Left-ERC20 Nullifier: Associated with the total deposit amount minus the NFT price.

→ (Collection address, token id, amount, new buyer’s NFT Nullifier hash, new buyer’s ERC20 Nullifier hash, spending ERC20 proofs)

### On-chain Verifier

The on-chain verifier function receives the following parameters:

- Collection Address
- Token ID
- Amount
- New Seller Spending ERC20 Nullifier Hash
- Seller Spending NFT Proofs
- Buyer Spending ERC20 Proofs
- New Buyer Spending NFT Nullifier Hash
- New Buyer Spending Left-ERC20 Nullifier Hash

**Verification Steps:**

Verify all nullifiers hash are available

1. Verify Seller’s ERC20 Nullifier Hash:

Confirm the amount in the new seller spending ERC20 nullifier hash.
2. Verify Seller’s NFT Proofs:

Validate the seller’s spending NFT proofs.
3. Validate proof with given amount
4. Verify Buyer’s ERC20 Proofs and Nullifier Hash:

Confirm the buyer’s spending ERC20 proofs and new buyer spending left-ERC20 nullifier hash.
5. Validate proof with given collection address and token id
6. Verify Collection Address and Token ID in Buyer’s NFT Nullifier Hash:

Ensure the correctness of the collection address and token ID in the new buyer spending NFT nullifier hash.

**Update state:**

1. Mark seller’s spending NFT nullifier hash as used
2. Mark buyer’s spending ERC20 nullifier hash as used
3. Add seller’s spending ERC20 nullifier hash to state tree
4. Add buyer’s spending NFT nullifier hash to state tree
5. Add buyer’s spending left-ERC20 nullifier to state tree

This robust verification process ensures the integrity and security of the NFT transaction on our marketplace, providing a trustworthy environment for both sellers and buyers.

Certainly! If you have any questions or need further clarification on any aspect of the process outlined above, feel free to comment

## Replies

**0xeminence** (2024-02-17):

Trying to understand the overarching idea here, when its fungible tokens zk enabled privacy for amms make sense perhaps because well you wouldnt know the source of funds, and if there are too many transactions this is akin to transaction obfuscation.

But in the non-fungible token land, since the identifier is unique, its almost always evident to trace it. Is the design suggesting a proxy-address generation so the source of funds might be obfuscated since its in eth/-token but the nft might be transferred to a new or some other address hence appearing almost like private nft purchase?

---

**terry** (2024-02-19):

This looks like OpenSea with privacy; only deposit and withdraw transactions will be traced on-chain. Sellers can’t know who buys their NFTs, and buyers can’t know who owns the NFTs they purchase.

---

**khiem20tc** (2024-03-01):

What does it mean when you say `Nullifier`? Exactly what is this?

---

**MicahZoltu** (2024-03-01):

In ZK systems, a nullifier a value (usually a big number) associated with some activity (e.g., deposit, transfer, etc.) that is published publicly as part of the withdraw process.  This prevents someone from referring back to that past activity multiple times.

As an example, if you deposit 1 ETH into some privacy tool, you do so along with a `hash(nullifier, salt)`.  Then later when you withdraw 1 ETH from that tool, you would publish a proof that “somewhere in the history of deposits there exists a `hash(nullifier, ?)`” (you keep the salt private so no one can find your deposit).  If you try to withdraw again, the system would see that you are trying to do a second withdraw with the same nullifier and it would not give you 1 ETH the second time.


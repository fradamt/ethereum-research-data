---
source: magicians
topic_id: 14685
title: "Feedback requested: EIP Idea: \"Proof of not spam\" using SIWE"
author: web3pm
date: "2023-06-14"
category: EIPs
tags: [erc, siwe, spam]
url: https://ethereum-magicians.org/t/feedback-requested-eip-idea-proof-of-not-spam-using-siwe/14685
views: 1026
likes: 3
posts_count: 2
---

# Feedback requested: EIP Idea: "Proof of not spam" using SIWE

Hello Eth Magicians,

Request for feedback on an idea to extend [ERC-4361: Sign-In with Ethereum](https://eips.ethereum.org/EIPS/eip-4361) to enable “Proof of not spam”.

Happy to extend this into a full proposal but first checking whether this use case has already been discussed and/or incorporated in some other way I’m not aware of (couldn’t find anything so far).

## Abstract

Extend **ERC-4361: Sign-In with Ethereum’s** `$statement` field so applications can recognize an authority as being delegated by a user to determine what is and isn’t spam (e.g., to better distinguish consented vs unconsented NFT airdrops). Existing fields like `Expiration Time` and `Resources` can be used to limit management in time and scope.

## Motivation

- Individual user-initiated wallet actions are currently used as proxies for “consent” in web3. This is how common NFT platforms like Opensea and Coinbase NFT decide which NFTs to show and hide.
- However, even when using a relayer or gas sponsor, requiring a signature for every action is a jarring experience for non-crypto-native users expecting a web2 UX, as well as a potential security risk when interacting with unknown contracts.
- The smoothest experience for many applications is to simply airdrop tokens to users, but we lack a generalized way to distinguish airdrop spam from airdrop not-spam.
- There are many other use cases, particularly for non-financial blockchain applications like messaging and credentials, where it’s particularly important to be able to distinguish spam from not-spam on behalf of a user.

## Illustrative Examples

### Example 1: In-person event mints

At Icebreaker we have hosted a half dozen in-person mints using our open sourced Merlin minter and have found several limitations for both web2 and web3 users, even when sponsoring gas.

- Web2 users who do not have a wallet

We have experimented with creating embedded wallets using web2 sign-in methods, but users frequently get confused by the prompt for a mint signature, which is a foreign UX.
- On the other hand, we do not wish to operate custodial wallets on users’ behalf.

Web3 users who do have a wallet

- Many users do not have gas in their wallets on all chains where NFTs may be deployed for minting.
- Prompting the user for a mint signature which we send through a relayer is difficult for even a crypto-native user to understand, as is distinguishing between a malicious vs benign contract, particularly on mobile and/or at a crypto conference.

The smoothest solution for both of these users is to simply ask their permission to give them a token and then airdrop the tokens to their wallets directly.

The missing piece is for **NFT platforms, wallet interfaces, protocols, and applications that use or display wallet activity to be able to know that these airdropped tokens are in fact legitimate and requested by the user- i.e., not spam, while most others remain spam.**

One solution to asking for and then proving permission to airdrop is to request a one-time light-weight off-chain signature in a human-readable format along the lines of ERC-4361: Sign-In with Ethereum.

### Example “Proof of not spam” Message

```auto
service.invalid wants you to sign in with your Ethereum account:
0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2

I authorize service.invalid to decide what is not spam for my account according to the scope below. I can revoke this authorization by issuing an overriding signature to another provider or by publishing a similar transaction in this format.

URI:
Version: 1
Chain ID: 1
Nonce: 32891756
Issued At: 2021-09-30T16:25:24Z
Resources:
-
- https://.*

```

In the example above, it will be the provider’s responsibility to publish the appropriate data (or a derivative of it), operate the APIs, and/or ping the platforms that the user is likely to engage with in order to provide this service. The exact implementation will require some fleshing out (with input/help from this community).

### Example 2: Filtering inbox spam

To be added in full proposal.

### Example 3: Gifting NFTs

To be added in full proposal.

### Generalizing to many use cases

The same format can be used to demonstrate permission spanning a single “not spam” transaction (e.g., agreeing to receive an airdrop at an event) or thousands (e.g., agreeing to delegate an authority like Opensea to act as your canonical source of truth for which NFTs to display vs. hide in every interface where your NFTs are displayed).

We’ve spoken with several others at Opensea and Coinbase who’ve agreed there’s no great solution for determining what is vs. isn’t spam today and that this improvement could be useful for the ecosystem.

## Next steps

If there is interest, I’m happy to work with others who are interested to turn this into a full proposal, which would also cover several other use cases where there is a strong need like delegating a service to filter (future) push protocol inbox spam, or making it easier to accurately display NFTs you’ve given to or received from your friends.

PS, a note on prior work: There have been several past proposals to use the cost of the transaction as a way of determining spam. However, as Vitalik has observed [“it turns out the happy medium that’s low enough for users and too high for spammers does not really exist.”](https://ethresear.ch/t/conditional-proof-of-stake-hashcash/1301). Other solutions for spam filtering likely exist but will generally be complementary, not substitutive of this simplistic delegation approach.

## Replies

**web3pm** (2023-06-16):

Originally I was thinking since spam is the default assumption, the primary useful proof is the proof of not spam, but [@jay](/u/jay) made a great point that marking certain collections as spam can also be a useful reverse marker for collections that are not spam.

This may also contribute helpful signal for other nascent applications that want sensible spam/not-spam defaults before they have their own user base.


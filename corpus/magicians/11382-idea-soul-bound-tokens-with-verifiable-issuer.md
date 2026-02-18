---
source: magicians
topic_id: 11382
title: "Idea: (Soul-Bound) Tokens with Verifiable Issuer"
author: KevinYum
date: "2022-10-19"
category: Magicians > Primordial Soup
tags: [nft, token, soul-bound]
url: https://ethereum-magicians.org/t/idea-soul-bound-tokens-with-verifiable-issuer/11382
views: 703
likes: 2
posts_count: 2
---

# Idea: (Soul-Bound) Tokens with Verifiable Issuer

# Motivation

The current interfaces or implementations of ERC tokens (ERC-20/721/1155) don’t include “issuer” as a part of its standard, the underlying value of tokens relies on implicit community consensus. Think of the fact you can copy & paste source code to deploy your own “USDC” or “BAYC” contract, but they will not bear any value.

However, this convention has two major limitations:

1. It limits adoption of new tokens. Each token will need to “gather consensus” before it is getting widely accepted.
2. It makes cryptocurrencies prone to phishing attacks. There is no way to verify whether a token is “authentic” due to lack of definition.

These limitations will become more notable under the context of soulbound tokens(SBT). Imagine there will be miscellaneous SBTs issued by governments, organizations, and persons. How can we determine which SBTs are trustful and which are not, given the fact they are not tradable and do not bear money value?

That’s why we want to propose a standard interface to allow tokens to be verifiable with regard to its issuer, this standard can be applied to all kinds of tokens but is believed to be most useful in SBTs.

# Solutions

We humbly describe two options briefly for early discussion, the complete spec will be on the way.

### Option #1. Create an on-chain registry to host and maintain token-issuer mapping.

Inspired by the SSL certificate which binds the identity of a website to a cryptographic key pair, we can bind the token contract to its issuer account. While publicly trusted certificate authority(CA) is required by SSL protocol, blockchain can provide such a registry using smart contracts by its decentralization nature. Necessary verification will be performed on the bind-relation registration process. Users can directly query the registry to check the issuer of some token contract.

### Option 2. Directly store issuer information along with verification material inside token contracts.

Another way is to store issuer information inside the token contract. While each token contract is able to claim its issuer, tokens with verifiable issuer will be required to further provide its verification material in specific format (e.g. issuer signing message) and keep it on-chain. Users will need to verify whether issuer information matches verification material if they want to check the issuer of some token contract.

# Next Step

We are working on complete specification of this proposal, and will propose a formal EIP after that. In the meantime, we are also building a SBT product which incorporates this idea as part of the design.

Any suggestions and feedback are sincerely welcomed!

## Replies

**TimDaub** (2022-10-19):

With my client’s projects for music NFTs we’re having the same issue. We want to know who issued which NFT but e.g. reading the Transfer’s `from` field doesn’t yield authentic information, so technically each transaction receipt has to be downloaded additionally. And then finally, event information isn’t available to the next tx executing in the smart contract.

I’ve documented some of the issue here: [Authentic Event Logs - Execution Layer Research - Ethereum Research](https://ethresear.ch/t/authentic-event-logs/12641)


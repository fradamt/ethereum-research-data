---
source: magicians
topic_id: 11262
title: "Idea: P2P SoulBound Token (Call For A Better Name!)"
author: ChrisWong
date: "2022-10-09"
category: Magicians > Primordial Soup
tags: [nft, token, soul-bound]
url: https://ethereum-magicians.org/t/idea-p2p-soulbound-token-call-for-a-better-name/11262
views: 1596
likes: 9
posts_count: 8
---

# Idea: P2P SoulBound Token (Call For A Better Name!)

Hi Eth Magicians, I wanted to share some thoughts on a new pattern regarding ERC1155, or NFT that is 1.) non-transferrable (a.k.a soul bound) and can only be minted with signatures from all agreed addresses.

**TLDR**

Using ERC-1155 as a social footprint to represent interaction among a small set of addresses. When all participant agrees on such action, and provide the signatures; A mint can be initialised. Once minted, these tokens would be burnable, but not transferable.

**Motivation:**

Social interaction is full of friction without any review or trust system. It takes time for us to feel safe to strangers and new ideas. While centralised platforms like Linkedin, Facebook or Airbnb  provide useful feedback, they are opaque, prone to censorship or fraud.

Being a popular and reputable figure on social media like Twitter, Instagram, is also not a reliable model, since the business model of social media tolerate buying up followers, and there is little way for normal users to distinguish how the validity of a person from their number of followers, no doubt these platform has been increasingly less reputable and more commercial.

With Ethereum, and public blockchain in general, it opens up the composability layer of human interaction and trust. When we interacted with another individual in a meaningful way, some sort of familiarity and trust is created such that later on it becomes easier for us to interact with the same person or even his/her friends. This is a non-trivial property of social interaction and how we build trust towards people around us. Currently, many of such meaningful interactions faded in the course of time because those meaningful interactions have no better way to be represented other than a twitter follow, or a telegram “Hi”.

Besides working as a medium of forming community, NFT can also be a tool to represent small group of social interaction. Once these social interactions are represented on-chain, there are potentially other dapps or trust composability usage based on custom metadata of the NFT they minted.

**Reference Implementation**

Some brief interfaces

```auto
// each address sign a message and provide their signature in order to whitelist themselves for a ERC1155 NFT
function initilizeNFT(bytes memory _signatures, bytes32 _rawMessageHash, address[] memory addresses)

// once the NFT is initialized, the address which provided signature in `initilizeNFT` can now mint the NFT.
function mint(uint256 tokenId, address to) external {
      (require(p2pwhitelist[tokenId][to], "not whitelist");

```

A full implementation



      [github.com](https://github.com/Mushroom-Lab/p2pNFT/blob/main/contracts/p2pNFT.sol)





####



```sol
// SPDX-License-Identifier: MIT
pragma solidity =0.8.11;
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

import "../interfaces/IP2PNFT.sol";

error WrongResolvedAddress(address resolved, address targeted);
error HashAlreadyMinted(bytes32 _rawMessageHash, address signer);

contract P2PNFT is IP2PNFT, ERC1155 {
    using Counters
    for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    address public factory;
    // unique identifier from dscription to identify eacch P2PNFT in factory.
    string public constant name = "P2PNFT";
    bytes32 public uid;
```

  This file has been truncated. [show original](https://github.com/Mushroom-Lab/p2pNFT/blob/main/contracts/p2pNFT.sol)










**Outstanding thoughts:**

1. Any concerns on privacy
2. What metadata should be encoded
3. Would the contract be ddos if it does not require privileged actor/owner.

**Next Steps:**

1. Any feedback is appreciated!
2. Further discussion on the implementation reference, to make sure it is as generic as possible and considering as many potential use cases as possible.
3. Potentially draft a EIP / ERC Token Standard once enough use cases are explored.

## Replies

**KevinYum** (2022-10-11):

I think protocols like [cyberconnect](https://cyberconnect.me/) and [lens](https://lens.xyz/) have already  been building web3 social connections.

Connections in CyberConnect are stored on Ceramic(IPFS), connection in Lens are stored on Polygon chain which is more similar to your ideas.

---

**TimDaub** (2022-10-11):

Hey, nice thread! I just wanted to say that we’re actively exploring this idea of p2p minting in EIP-4973 and we’d love to hear your feedback: [EIP-4973 - Account-bound Tokens - #129 by TimDaub](https://ethereum-magicians.org/t/eip-4973-account-bound-tokens/8825/129)

There is also a deliberate attempt at standardizing around p2p minting and burning which could be helpful: [ERC-5679 Mint and Burn Tokens - #13 by xinbenlv](https://ethereum-magicians.org/t/erc-5679-mint-and-burn-tokens/10913/13)

---

**gbdt** (2022-10-11):

What this pattern wants to do is to use NFT to record a common moment that belongs to multiple addresses (instead of record “follow” like in previous social apps)

I think this granularity is pretty good. It’s a viable idea to bring multi-signature into scenarios like proving a shared experience.

Many IRL scenarios require multi-signatures before generating an NFT: shared moments, collaborative works, multi-party agreements, comment sys. Maybe the process can be standardized.

---

**JessicaC** (2022-10-12):

We are implementing a Semantic SBT to encode the social relationships on Ethereum Identity Ecosystem. MultiSig can be used in the case you described. See my post here:



    ![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/j/da6949/48.png)
    [Discussion - Can Ethereum be a linked data web?](https://ethereum-magicians.org/t/discussion-can-ethereum-be-a-linked-data-web/10932) [Primordial Soup](/c/magicians/primordial-soup/9)



> After the long awaited merge shipped on 15 Sept 2022, the stage is set for further scalability, security, and sustainability. Now we can start to think of building something novel if the txs are 100x cheaper.
> The SBTs proposed by the paper Decentralized Society: Finding Web3’s Soul is inspiring. To build something centred around the Ethereum Identity Ecosystem, the way to prove something about your account, or you can call it wallets or souls, is really important. There are some early movers al…

We have the article here describing our idea of Semantic SBTs.


      ![image](https://coindesk-next-a6ificwar-coindesk.vercel.app/favicons/production/favicon.ico)

      [CoinDesk](https://www.coindesk.com/sponsored-content/semantic-sbts-encode-social-relationships-on-web3)



    ![image](https://cdn.sanity.io/images/s3y3vcno/production/78d2ee50728d6e8c6b2e6f5d3533c409b900cd76-6001x4501.png?auto=format)

###



Web3 has created a movement to fundamentally change how we interact with each other in the digital world. Soulbound tokens (SBTs) are the latest emerging use case for blockchain technology looking to support an interoperable digital identity. With...










We are drafting a EIP now. Shoot me an email to discuss. j.chang@relationlabs.ai

---

**gbdt** (2022-10-12):

[@TimDaub](/u/timdaub) 's design(EIP-4973) is directed, A->B B->A

[@ChrisWong](/u/chriswong) 's design is undirected, A-B, A-B-C

In fact, the input parameters of EIP-4973 (give and take) and ChrisWong’s initilizeNFT are very similar. But what they express do not belong to the same category. There are mainly two differences: 1.directed or undirected -ness of relationship 2.whether binding relationship of more than 2 addresses.

IMHO both are needed in real life.

---

**TimDaub** (2022-10-12):

I think in EIP-4973 we also want to solve for undirected consensual mints. I’ve called these things agreements where potentially two parties consent to minting a token that then however appears in both of their wallets, almost like a contract that two or more parties signed. Here’s that post: [EIP-4973 - Account-bound Tokens - #125 by TimDaub](https://ethereum-magicians.org/t/eip-4973-account-bound-tokens/8825/125)

---

**gbdt** (2022-10-21):

suggested name: NFT co-minting

This proposal expresses a process that multiple people create and mint an NFT together to record a thing shared by all parties.

The proposal should include:

- the standard of registration and authentication
- mint method (mint individually or mint for all)
- whether the token can be transferred.
- revokability
- …

This is needed both in real society and socially in games. It’s a web3-native way of expressing relationships. I believe in the near future, it will become a ubiquitous basic proposal.

The proposal should not be limited to soulbound tokens. It’s also applicable to transferable NFTs.


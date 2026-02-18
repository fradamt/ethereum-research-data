---
source: magicians
topic_id: 8842
title: "Proposal: Token Interaction Standard"
author: alxi
date: "2022-04-06"
category: EIPs
tags: [nft, metaverse]
url: https://ethereum-magicians.org/t/proposal-token-interaction-standard/8842
views: 611
likes: 1
posts_count: 1
---

# Proposal: Token Interaction Standard

# EIP-xxxx: Token Interaction Standard

How do we make nfts *do things*?

ERC-721s are the **objects** of web3. The emerging “metaverse” game environments are **processes** that run on these objects. So far, most of these game environments have operated as traditional off-chain games that import on-chain assets, with some using the blockchain as a store for state data. But what if these games were built in the same way as the assets they process? On an open, composable protocol that makes the game environment the blockchain itself?

The idea proposed here is a standard for arbitrary user-initiated actions to be committed from one ERC-721 (or other token) to another, with an optional shared `state` contract (the on-chain “dungeon master”).

`Actions` can be anything. A spell might `"ENCHANT"`, a weapon might `"STRIKE"`, a pfp might `"SETTLE"` a land token.

A fight between two pfps might include a `state` contract that tracks hp, strength, and other stats, which might be adjusted based on the outcome of the fight. The losing pfp might update its render with a black eye for the next 4,000 blocks. Because all of this happens on an open, composable protocol, other games might share this fight `state` contract and its action flow. Then the fights within these games become ***real*** – outcomes in one are realized across all the others.

Here is a draft of what this interface might look like.

```solidity
struct Action {
    string name;
    address from;
    address fromContract;
    uint256 tokenId;
    address to;
    uint256 toTokenId;
    bytes ext;
    address state;
    uint256 nonce;
}

interface IERCxxxx {
    // Commit actions via the `fromContract`
    function commitAction(Action memory action) external payable;

    // `to` and `state` contracts handle actions sent either by
    // the `fromContract` or, if no `fromContract` is set, the
    // `from` address is expected to be the msg.sender.
    function handleAction(Action memory action) external payable;

    // `state` contracts validate actions with the `fromContract`.
    function validateAction(uint256 nonce) external returns (bool);
}
```

## Action Validation

One contract can validate `msg.sender`, but it cannot validate its sender’s `msg.sender`.

In order to validate an action in the case that it is passed between 3 contracts (sender, receiver, and state), the sending contract sets a nonce at the beginning of the transaction and includes it in the action object. The `state` contract then calls `validateAction()` on the sender, which returns true if the nonce matches.

An initial implementation is already being developed in collaboration with other creators in the NFT ecosystem and a formal proposal is planned, but first I am curious to hear any thoughts or feedback on the core concept.

Thank you!

-alxi

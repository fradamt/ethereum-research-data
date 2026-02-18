---
source: magicians
topic_id: 19348
title: "Proposal: Longer Term Testnet"
author: xinbenlv
date: "2024-03-25"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/proposal-longer-term-testnet/19348
views: 670
likes: 2
posts_count: 3
---

# Proposal: Longer Term Testnet

Good bye [goerli](/tag/goerli) tesetnet. I propose even longer LTS testnets, for dApps, L2s and wallets and other things that co-depend on each other.

We keep moving to new testnets, which caused the smart contracts to be wiped out and if someone want to build smart contracts that depend on other smart contracts, such as ENS or Uniswap, they have to wait until the team deploy to the teams deploy on new testnets and that’s unideal. L2s too. Wait and see how long it will take for all those @arbitrum , @Optimism and their L3s move to the new #Holesky and then dApps can build upon.

I understand some of the reasons that we want to wipe out testnets:

1. we don’t want its tokenomics to become real
2. we don’t want to store that much states
3. we want to be able to start clean with new EVM version or consensus.

But I think we also want to keep a LTS kind of testnets to not break smart contract builders, dApp builders and L2 builders or who built on top of them.

There are some way to do it: we can start a LtsTestnet:

1. create some tokennomics where the issuance becomes so inflatable that it’s virtually no use to hold the testEth on that testnet,
2. with the move to lightclient / limited history, or verkletree mechanism, testnet
3. and create governance to keep them run or decide to fork.

## Relevant discussion

- Proposal: Predictable Ethereum Testnet Lifecycle

## Replies

**abcoathup** (2024-03-27):

Another argument for regular testnet deprecation is to maintain the skills/knowledge to create and migrate to new testnets.

Sepolia is planned to move to LTS at the start of 2026.  That is still quite a bit of time for application developers.

https://github.com/eth-clients/sepolia

---

**xinbenlv** (2024-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> nother argument for regular testnet deprecation is to maintain the skills/knowledge to create and migrate to new testnets.
>
>
> Sepolia is planned to move to LTS at the start of 2026. That is still quite a bit of time for application developers.

That’s one good goal to have in some testnet, and I think it’s important for Core Developers to do that. And it can be achieved by having much shorter lived testnet. 5y is too long for that I think, maybe each quarter or each month is reasonable.

Independent from that goal, smart contract and application layers developers want to practice building on top of existing contract ecosystems which is conflict to that goal you mention and probably shall be achieved in different testnets.


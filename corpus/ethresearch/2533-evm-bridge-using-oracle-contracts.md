---
source: ethresearch
topic_id: 2533
title: EVM bridge using oracle contracts
author: themandalore
date: "2018-07-11"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/evm-bridge-using-oracle-contracts/2533
views: 1603
likes: 0
posts_count: 1
---

# EVM bridge using oracle contracts

Hi Ethereum Researchers,

My colleagues and I have built an intermediate scaling solution using bridge contracts referencing an Oracle to relay data between EVM chains.  To sum it up: We create a new EVM chain and  link it to the mainchain via a dedicated relayer (similar to Oraclize) and contracts that automate the passage of messages from the dapp chain to the main chain.  Parties will be able to send mainchain Ether (mEth) or tokens from the mainnet to the dapp chain. We think that this solution could be easier to implement for some projects and it’s much more straightforward than a lot of other scaling projects out there.  In addition, by using security measures like TEEs and TLS notary proofs, you can have a semi-trustless (hardware entrusted) bridge that can help your project move quickly to a new EVM while we wait for relay networks to develop.

Here’s a list:

Github:https://github.com/DecentralizedDerivatives/Oracle_bridge

Medium Article (A brief overview):

https://medium.com/@nfett/dda-scaling-overview-5fdb8ec436bc

And an article on security issues if using a public EVM as the dapp chain: https://medium.com/@nfett/aligning-incentives-for-bridged-sidechains-5bb85d405dab

We’ll be building it out and trying to move beyond just the POC, but we’d love to hear your thoughts and comments, and keep up the great work guys (and gals).

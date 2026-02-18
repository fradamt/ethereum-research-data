---
source: ethresearch
topic_id: 6307
title: "[Testing] ETH2.0 Killer"
author: Econymous
date: "2019-10-12"
category: Layer 2
tags: []
url: https://ethresear.ch/t/testing-eth2-0-killer/6307
views: 1698
likes: 0
posts_count: 3
---

# [Testing] ETH2.0 Killer

This is my attempt at creating a contract that’s token supply is forcibly distributed. Distribution is good for proof of stake sidechains. This mean scaling

It basically flips proof of weak hands around in a way. The more you lose in the contract the more tokens you’re rewarded. Plus some other things.

Just try to attack the “resolve token” supply.

The mechanics that run this thing are the incentive to win in a pyramid, or to use the token distribution (if you lose the pyramid) to earn trx fees on the sidechain. Or dividends from contract volume. There could be another system that benefits from the distribution.  Like a dao that also runs in parallel with the sidechain. Evenly distributed voting power to vote on where funds go.

So far, from all that I have explored all attacks are extremely difficult.

The implications of the market forces and the benefit of holding resolves makes it so that ? 51% attacks require exponential time or buying power.

I have a mainnet version working. I’ll launch a testnet soon though

----edit

nevermind, broken

new tests below

## Replies

**Econymous** (2019-10-19):

Testing Dapp Sites

Color Wrapper Contract: http://apathetic-hair.surge.sh

Core Contract: http://lewd-trucks.surge.sh

Ropsten Testnet

Pyramid Contract: https://ropsten.etherscan.io/address/0x3Ee1Cc4Df311F67B0e3675A8da85335367e4123d

Token Contract: https://ropsten.etherscan.io/address/0xA254bbaCB3bAfF5466e8faA5Bfa079E3b1A4329C

Color Contract: https://ropsten.etherscan.io/address/0x8902201B7a4f832647a7c8f982C786bF3191Db13

Pyramid Contract Source: https://pastebin.com/1xyngunz

Color Token Source: https://pastebin.com/K1Agxr8i

---

updated color contract

Color Contract: https://ropsten.etherscan.io/address/0xC965e67e7cCc505e2522cf9EB22D7412DC2E8D34

Color Token Source: https://pastebin.com/qkW7BMZp

---

**Econymous** (2019-10-20):

New test contracts

Core Contract: http://prismtokenomics.com/#/contract

Color Wrapper: http://young-government.surge.sh/#/contract

Ropsten Testnet

Pyramid Contract: https://ropsten.etherscan.io/address/0x390cab9E58541Ad89eecb5A473B3C039b1C21D65

Token Contract: https://ropsten.etherscan.io/address/0xa23a23a911B77e6aB12305C1144ca9ea50DE4e6c

Color Contract: https://ropsten.etherscan.io/address/0xe139e41d596Db7187425F290c6dF76a079054cB6

Pyramid Contract Source: https://github.com/Econymous/powhr/blob/a8290d450ad15fb731ca8ee9e0dc48e222bbc23e/smart-contract/powhr.sol

Color Token Source: https://github.com/Econymous/powhr/blob/a8290d450ad15fb731ca8ee9e0dc48e222bbc23e/smart-contract/ColorToken.sol


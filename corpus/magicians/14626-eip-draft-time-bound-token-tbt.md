---
source: magicians
topic_id: 14626
title: "EIP draft: Time Bound Token (TBT)"
author: Mathepreneur
date: "2023-06-09"
category: EIPs
tags: [erc, nft, token, erc-721]
url: https://ethereum-magicians.org/t/eip-draft-time-bound-token-tbt/14626
views: 710
likes: 1
posts_count: 1
---

# EIP draft: Time Bound Token (TBT)

TBT let us tokenize time bounded assets like rentable NFT, time restricted governance, fixed maturity derivatives, escrow products, rentable real estates.

Fixed maturity style financial products are valuable for coordination of any financial logic based on discrete time. The owner of the short position foregoes some beneficial persistent financial utility before maturity; while, the owner of the long position benefits from being able to call the persistent financial utility before maturity. Common examples are fixed income products, options, bonds, etc. These kinds of product tends to have periodic maturity markets, where users can purchase the same contract but different maturities. Another interesting financial features of such products is purchasing a position where the beneficial utility can only be called after a future time but ends after a further future time. For example a contract where you can earn variable fees starting one year later but ends two years later.

The challenge of implementing these kinds of behavior in the current token standard, is that the data structure and API of such contracts cannot efficiently reflect timeline based ownership.

I propose a time bound token standard. The ownership of these tokens are cut into periodic timeline. For example suppose we have a time bound token with a persistent utility function of earning some fees from a protocol. Also suppose the period duration is 100 seconds. Alice owns 1 unit of time bound token from block timestamp 100 to 200. Bob owns 1 unit of time bound token from block timestamp 200 to 400. Charlie owns 1 unit of time bound token from block timestamp 400 to infinity. Between block timestamp 100 to 200, only Alice can call the persistent utility function of the 1 unit of token to earn fees. Between block timestamp 200 to 400, only Bob can earn fees. After block timestamp 400, Charlie can start to earn fees.

Suppose Bob transfer 1 unit of time bound token from block timestamp 200 to 300 to Alice. Then Alice will now have a time bound token from block timestamp 100 to 300, and Bob will now have a time bound token from block timestamp 300 to 400.

With this mechanism, anyone can create interesting AMM and contracts dealing with fixed discrete tokens.

A simple example of time bound token I have written is flash time bound token. Any user can wrap any ERC20 token as time bound token from block timestamp now to infinity. For example 1 DAI = 1 time bound DAI from now to infinity. Owner of the time bound token can flash utilize the DAI by transferring the DAI out, do any arbitrary transaction, as long as, the same amount of DAI is returned to the time bound token at the end of the transaction. The time bound token can be cut into smaller pieces time wise and be sold to others. If Bob has 100 time bound DAI from block timestamp 300 to 500, then Bob can call the flash utilization function to utilize the 100 DAI only from block timestamp 300 to 500. Anyone who holds time bound DAI from now to infinity can unwrap and withdraw the DAI. Alice who holds 100 time bound DAI from block timestamp 500 to infinity, must wait till after block timestamp 500 to be able flash utilize or unwrap the 100 DAI. Alice wrapped 100 DAI, sold the 100 time bound DAI from block timestamp 300 to 500, and received 1 time bound DAI from block timestamp 500 to infinity. Thus Alice receives a risk free and oracle-less interest rate. The risk free yield is essentially the yield of market inefficiencies.

Getting the balanceOf of an address will return an array of Balance struct, where Balance struct contains a uint96 time tick (a smaller uint can work) and int160 balance delta (It can also be two equal length arrays). So suppose we get the balanceOf of Oscar which returns an array with three elements { time: 500, balance: 300 }, { time: 1000, balance: -100 }, and { time: 1500, balance: 300 }. This means Oscar has balance of 300 time bound token from block timestamp 500 to 1000, 300 - 100 = 200 time bound token from block timestamp 1000 to 1500, and 300 - 100 + 300 = 500 time bound token from block timestamp 1500 to infinity.

A good data structure for the time bound token is a linked list of signed balance deltas, as there should be flexibility on transferring different amount of tokens of different timelines.

I believe this will be a good token standard for fixed time products. Will specify the interface soon. Would love to hear feedbacks!

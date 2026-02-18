---
source: magicians
topic_id: 8118
title: Transaction Expiration - initial EIP proposal
author: primata
date: "2022-01-27"
category: EIPs > EIPs core
tags: [evm, gas]
url: https://ethereum-magicians.org/t/transaction-expiration-initial-eip-proposal/8118
views: 791
likes: 0
posts_count: 1
---

# Transaction Expiration - initial EIP proposal

Wanted to initiate a discussion on a EIP proposal.

| eip |  |
| --- | --- |
| title | Transaction Expiration |
| description | Proposes a Transaction Expiration Block for every transaction. |
| author | Lucas Vinzonlucasvinzon@gmail.com |
| discussions-to |  |
| status | Draft |
| type | Standards Track |
| category (*only required for Standards Track) | Core |
| created | 2022-01-25 |
| requires (*optional) |  |

## Abstract

When in Ethereum Mempool, every transaction should expire after a certain amount of blocks resulting in no cost to its users. 15.000 blocks would effectively have every transaction on the Mempool for two days.

## Motivation

Gas cost, usability and serving its purpose for its users. Prevents unexperienced users to waste resources.

## Specification

Once in the Mempool ALL transactions MUST expire after a certain amount of blocks. It is OPTIONAL to lower the amount of blocks it will be live on the Mempool. It SHALL NOT result in gas cost to users.

## Rationale

Ethereum currently has a lot of pending transactions. Those transactions have little to no value to their users and the network since most of them will fail or never occur. Their existence in the Mempool inflates gas cost since they are referred to when estimating transaction costs for users. This significantly reduces usability and increases friction. It would also be forgiving to inexperienced users who set transactions that are not meant to be fulfilled, further wasting resources. This proposal highly values usability and prevents wasting resources, serving its purpose as a network.

I’m not sure how to continue with this proposal, but would love to hear back from the community you thoughts and on how to move it forward.

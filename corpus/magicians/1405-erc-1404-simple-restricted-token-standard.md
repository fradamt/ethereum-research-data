---
source: magicians
topic_id: 1405
title: ERC-1404 - Simple Restricted Token Standard
author: youfoundron
date: "2018-09-19"
category: EIPs
tags: [security-token]
url: https://ethereum-magicians.org/t/erc-1404-simple-restricted-token-standard/1405
views: 1210
likes: 1
posts_count: 2
---

# ERC-1404 - Simple Restricted Token Standard

Soliciting feedback for [ERC-1404](https://github.com/ethereum/EIPs/issues/1404).

The repository to check out is [here](https://github.com/simple-restricted-token/simple-restricted-token).

Use of the standard lends to writing  small, reusable smart contracts that are responsible for enforcing a single transfer restriction pattern.

Tokens implementing the standard are best constructed by composing said restrictions through multiple contract inheritance.

The examples in the above repo demonstrate several of these individual restriction implementations.

Would love to see criticism of the utility of these examples, their source code, and the standard itself!

## Replies

**AccessDenied403** (2026-01-13):

Hello [@youfoundron](/u/youfoundron)  and other potential people interested,

I have also posted on the Github issue but I post also here since this is the official place to discuss about ERC.

I wanted to ask about the current status of ERC-1404. Is there any plan to move it toward a finalized version or coordinate with the Ethereum Foundation to make it an official ERC standard?

There may be potential improvements (e.g., using uint256 instead of uint8 for restriction codes), but these could also be addressed in a different ERC since this ERC is already  used as is for a long time

For context, I am one of the maintainer of CMTAT and we are using ERC-1404 in the CMTAT security token framework: CMTAT ( [CMTA · GitHub](https://github.com/CMTA/) )

ERC-1404 is still used today by other projects such as Centrifuge, blockdaemon

It would be great to hear any updates or thoughts on the standard’s next steps.


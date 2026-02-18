---
source: magicians
topic_id: 670
title: ERC-1202 Voting Standard and beyond
author: xinbenlv
date: "2018-07-09"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc-1202-voting-standard-and-beyond/670
views: 1699
likes: 0
posts_count: 2
---

# ERC-1202 Voting Standard and beyond

## Official Discussion for ERC 1202 Voting Standard

Dear friends on [ethereum-magicians.org](http://ethereum-magicians.org)

Per new EIP requirement, we are moving our official thread for EIP 1202 standard from [github issue #1202](https://github.com/ethereum/EIPs/issues/1202) to [ethereum-magicians.org](http://ethereum-magicians.org).

Please view the lastest draft in [my EIP 1202 draft repo](https://github.com/xinbenlv/eip-1202-draft/blob/master/EIP-1202.md), and a published version can be found in [official EIP site](https://eips.ethereum.org/EIPS/eip-1202)

Related EIPs to support on-chain governance and society modeling

- EIP-5453: Smart Endorsement
- EIP-5485: Legitimacy, Jurisdiction and Sovereignty
- EIP-5247: Smart Proposal
- EIP-5732: Commit Interface for Commit Reveal

## Replies

**xinbenlv** (2018-07-09):

Here are a few early questions I’d like to ask people here.

1. Have we had any duplicated EIPs that I overlooked. If not, have anyone attempted to do so, and why it did not continue to exist?
2. Should each issue have its own smart contract address (like individual item on EIP-721) or should it support multiple items in EIP-1155, or should it support multi-class voting in EIP-1178, EIP-1203 (e.g. certain issue can override another issue)
3. Should the voting support proxy(e.g EIP-897, EIP-1167) and migration? What are potential security concerns
4. Should it be proposed in a single phase standard or multiple separate into multiple phase, with earlier phase supporting easiest and simplest interface, and later phase supporting more advanced interfaces? (I intuitively believe it will be the latter, but not sure if it might be possible to do it all-at once.)


---
source: magicians
topic_id: 15346
title: "ERC-7412: On-Demand Off-chain Data Retrieval"
author: noahlitvin
date: "2023-08-03"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7412-on-demand-off-chain-data-retrieval/15346
views: 2331
likes: 0
posts_count: 3
---

# ERC-7412: On-Demand Off-chain Data Retrieval

Discussion thread for https://github.com/ethereum/EIPs/pull/7412

We’re working on [SIP-329](https://sips.synthetix.io/sips/sip-329/) for Synthetix and thought it might be a good time to formalize a standard here that could also be applicable to cross-chain reads (or any other oracle data). We should be able to implement this standard with Pyth for price feeds right away and we’re in touch with other oracle providers about developing a cross-chain read solution that can also conform to this standard.

We’re very interested in feedback on this from the broader Ethereum community as we get into implementation. Thank you!

## Replies

**noahlitvin** (2023-08-14):

We’ve built a functional reference implementation with a test here: [GitHub - Synthetixio/erc7412: Reference implementation for [EIP-7412](https://eips.ethereum.org/EIPS/eip-7412)](https://github.com/synthetixio/erc7412)

---

**noahlitvin** (2025-03-17):

We’ve made a small update to the content of the ERC and created this microsite with more information at erc7412 [dot] github [dot] io (unable to post links)


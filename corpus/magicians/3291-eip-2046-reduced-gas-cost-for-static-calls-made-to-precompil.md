---
source: magicians
topic_id: 3291
title: "EIP-2046: Reduced gas cost for static calls made to precompiles"
author: axic
date: "2019-05-18"
category: EIPs > EIPs core
tags: [gas, precompile, eip-2046]
url: https://ethereum-magicians.org/t/eip-2046-reduced-gas-cost-for-static-calls-made-to-precompiles/3291
views: 4874
likes: 0
posts_count: 7
---

# EIP-2046: Reduced gas cost for static calls made to precompiles

Discussion thread for


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-2046)




###

Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.

## Replies

**axic** (2019-05-18):

This has been previously suggested as part of [EIP-1109](https://github.com/ethereum/EIPs/pull/1109) and [EIP-1231](https://github.com/ethereum/EIPs/pull/1231).

However EIP-1109 was later changed to a very different approach. [I have suggested to change EIP-1109](https://ethereum-magicians.org/t/eip-1109-remove-call-costs-for-precompiled-contracts/447/7) a while ago, but it seems it will stick with that approach, hence my reason creating a new EIP.

---

**karalabe** (2019-08-07):

This EIP still references 1352 as a base upon which to build, but that was dropped from Istanbul. Without that, this EIP becomes open to interpretation. I’d suggest reworking it or postponing from Istanbul.

---

**chfast** (2019-08-08):

From my perspective, implementing this without EIP-1352 " Specify restricted address range for precompiles/system contracts" is at least inconvenient. The EVM will need to know how many precompiles are there and at what addresses they are deployed. I’d rather hard-code this information inside EVM based on the hard fork id. This is simplest approach but not very generic and disallows other precompiles configurations for Ethereum networks other than mainnet.

---

**holiman** (2019-08-29):

Some benchmark/analysis available here: https://github.com/holiman/goevmlab/tree/master/examples/callPrecompiles

TLDR; No objections from my side, other than that some of the existing precompiles *may* have to be adjusted a bit.

---

**guthlStarkware** (2019-10-28):

Is this EIP still lead by someone? I’m interested in moving it forward.

---

**gumb0** (2019-11-06):

One test for the current spec https://github.com/ethereum/tests/commit/8bbbd484227684339ec64ed6a0083d0b137436c8


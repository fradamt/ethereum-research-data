---
source: ethresearch
topic_id: 6463
title: Introducing BLS-ROLLUP
author: kladkogex
date: "2019-11-18"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/introducing-bls-rollup/6463
views: 2652
likes: 1
posts_count: 3
---

# Introducing BLS-ROLLUP

Comments are welcome …

https://skale.network/blog/introducing-bls-rollup/

## Replies

**thor314** (2019-11-19):

A few relatively high level questions.

- how did we manage to eliminate the ~20 byte recipient address, when reducing transaction size? You made an analogy about taking envelopes headed to New York and batching them that I didn’t quite get.
- Is there a mathematical comparison somewhere between BLS-sigs and second layer scaling solutions on the metrics of tps and block sizes?
- Does a BLS-sig scheme have an analogy to the second layer “exit-condition” if an operator proves malicious, or does the scheme dodge the problem by having a smart contract as an uncorruptible “operator”?
- You compare your ERC20 and NFT token exchange to main chain token exchange, but you didn’t mention Uniswap. Why?
- That seems like an awfully fast turn around between Phase 1 and Phase 2.

---

**kladkogex** (2019-11-21):

Thank you for questions!

> how did we manage to eliminate the ~20 byte recipient address, when reducing transaction size?

Essentially each participant registers (once) to receive a 4 byte participant id.  There is a mapping of ids to addresses in the rollup smart contract.  Aftet that you can specify the id instead of the address

Is there a mathematical comparison somewhere between BLS-sigs and second layer scaling solutions on the metrics of tps and block sizes?

A competing technology to BLS-sigs is ZKSnarks/STARKS. BLS sigs take less than 10 ms to sign and verify. I know that there are some measurements for SNARKS/STARKS where it takes ~ 20 min to generate a proof.

> Does a BLS-sig scheme have an analogy to the second layer “exit-condition” if an operator proves malicious, or does the scheme dodge the problem by having a smart contract as an uncorruptible “operator”?

There is no single operator, even if an aggregator becomes malicious, the only thing she can do is to stop processing transactions, which  delays processing for several minutes. There is a way to have several aggregators per time slot.

Even if the 111 nodes become malicious, there is a way to file a fraud proof and request a new twice larger set of random sizes judges (222 nodes), that can revert the system to before the fraud happened.

> You compare your ERC20 and NFT token exchange to main chain token exchange, but you didn’t mention Uniswap. Why?

We are working on analysis of how to do Uniswap with BLS-ROLLUP like this … Hopefully will publish it soon.

> That seems like an awfully fast turn around between Phase 1 and Phase 2.

If you want to help SKALE we are looking for outside contributors and have pretty significant SKALE token bounties. ![:star_struck:](https://ethresear.ch/images/emoji/facebook_messenger/star_struck.png?v=12)![:star_struck:](https://ethresear.ch/images/emoji/facebook_messenger/star_struck.png?v=12)![:star_struck:](https://ethresear.ch/images/emoji/facebook_messenger/star_struck.png?v=12)


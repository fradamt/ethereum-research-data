---
source: magicians
topic_id: 3549
title: "EIP-XXX: fair atomic swap contract"
author: HAOYUatHZ
date: "2019-08-14"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-xxx-fair-atomic-swap-contract/3549
views: 1695
likes: 0
posts_count: 3
---

# EIP-XXX: fair atomic swap contract

Hi all,

My friends and I have been working on mitigating the arbitrage risk in a HTLC-based Atomic Swap, which is called the “**free premium problem**”, where the initiator can abort the deal (i.e. have optionality) without any penalty.

We analysed how profitable the arbitrage can be given the default timelock setting (24/48 hrs). Our result shows that the profit can be approximately 1% ~ 2.3%, which is non-negligible compared with 0.3% for stock market. This can be attractive as it’s totally risk-free. Please refer to our paper https://eprint.iacr.org/2019/896, and the related code https://github.com/HAOYUatHZ/fair-atomic-swap if interested.

Several studies have proposed for solving this problem. Their basic idea is that, the transaction for the premium needs to be locked with the same secret hash but with a flipped payout, i.e. when redeemed with the secret, the money goes back to Alice and after timelock, the premium goes to Bob as a compensation for Alice not revealing the secret. However, this introduces a new problem: Bob can get the premium without paying anything, by never participating in.

**Therefore**, we bring up atomic swap smart contracts for a more fair version. We explore the Atomic Swaps under both Spot scenarios and American Call Options scenarios. See repo/tree/master/src/atomicswap/ethatomicswap/contract/src/contracts for details.

- The RiskySpeculativeAtomicSwapSpot.sol is an simple atomic swap smart contract. Without premium, the initiator can actually arbitrage the fluctuations on price, making profit with no risk.
- The RiskySpeculativeAtomicSwapSpot.sol is the premium version for Spot scenarios.
- The RiskySpeculativeAtomicSwapOption.sol is the premium version for American Call Options.

We hope our work can make more people in the community aware of such a “free premium problem”, and have an fair implementation to refer to.

So we are here **trying to propose an EIP** for our implementations. We believe that our idea is original but just want to make sure. We wonder is it suitable for opening an EIP, in case of being rejected because there already are similar researches existing?

Any discussion will be appreciated, as we sincerely want to solve this problem, and solve it in a better way if there is any.

As a new user, I am only allowed to have two links in the post. So I put the links for some references in the replies below.

Regards,

HAOYU

## Replies

**HAOYUatHZ** (2019-09-02):

For detailed explanation on “free premium problem”, see https://blog.bitmex.com/atomic-swaps-and-distributed-exchanges-the-inadvertent-call-option/.

---

**HAOYUatHZ** (2020-09-20):

Hi forks!

We have proposed [EIP-2266](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2266.md) and really look forward to your feedback!

It will be nice if you can arrange a discussion on the (dis)approval of it.

Thanks!


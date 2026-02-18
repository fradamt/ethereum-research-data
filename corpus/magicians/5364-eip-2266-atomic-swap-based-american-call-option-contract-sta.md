---
source: magicians
topic_id: 5364
title: "EIP-2266: Atomic Swap-based American Call Option Contract Standard"
author: HAOYUatHZ
date: "2021-02-17"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-2266-atomic-swap-based-american-call-option-contract-standard/5364
views: 1153
likes: 3
posts_count: 4
---

# EIP-2266: Atomic Swap-based American Call Option Contract Standard

Hi Ethereum folks,

We have been working on mitigating the arbitrage risk in a HTLC-based Atomic Swap, which is called the “**free premium problem**”, where the initiator can abort the deal (i.e. have optionality) without any penalty. For detailed explanation on “free premium problem”, see https://blog.bitmex.com/atomic-swaps-and-distributed-exchanges-the-inadvertent-call-option/.

We analysed how profitable the arbitrage can be given the default timelock setting (24/48 hrs). Our result shows that the profit can be approximately 1% ~ 2.3%, which is non-negligible compared with 0.3% for stock market. This can be attractive as it’s totally risk-free. Please refer to our paper https://eprint.iacr.org/2019/896 (which gets accepted in ACM AFT’19), and the related code [GitHub - fair-atomic-swap/fair-atomic-swap: On the optionality and fairness of Atomic Swaps](https://github.com/fair-atomic-swap/fair-atomic-swap) if interested.

Several studies have proposed for solving this problem. Their basic idea is that, the transaction for the premium needs to be locked with the same secret hash but with a flipped payout, i.e. when redeemed with the secret, the money goes back to Alice and after timelock, the premium goes to Bob as a compensation for Alice not revealing the secret. However, this introduces a new problem: Bob can get the premium without paying anything, by never participating in.

**Therefore**, we bring up atomic swap smart contracts for a more fair version. We explore the Atomic Swaps under both Spot scenarios and American Call Options scenarios. See repo/tree/master/src/atomicswap/ethatomicswap/contract/src/contracts for details.

- The RiskySpeculativeAtomicSwapSpot.sol is an simple atomic swap smart contract. Without premium, the initiator can actually arbitrage the fluctuations on price, making profit with no risk.
- The RiskySpeculativeAtomicSwapSpot.sol is the premium version for Spot scenarios.
- The RiskySpeculativeAtomicSwapOption.sol is the premium version for American Call Options.

We hope our work can make more people in the community aware of such a “free premium problem”, and have an fair implementation to refer to. **Besides, our protocol can easily support option derivates DEXs.**

So we are here proposing EIP-2266 [EIPs/EIPS/eip-2266.md at master · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2266.md). We really look forward to your feedback.

Regards,

HAOYU

## Replies

**poojaranjan** (2021-02-18):

A wonderful explanation of the proposal by [@HAOYUatHZ](/u/haoyuathz) & Runchao Han

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/2/2ac109f6c935db0cd5fbea07d342ee60e15b567f.jpeg)](https://www.youtube.com/watch?v=wwWcfl9N65k)

on [PEEPanEIP](https://www.youtube.com/playlist?list=PL4cwHXAawZxqu0PKKyMzG_3BJV_xZTi1F).

---

**HAOYUatHZ** (2021-02-19):

Thanks [@poojaranjan](/u/poojaranjan) !

---

**JacquiFreeElectron** (2022-05-14):

Hi HAOYU!  I looked through all the documents you posted, and I want to thank you that you guys came up with this useful EIP. I just have a different thought about where you said “However, this introduces a new problem: Bob can get the premium without paying anything, by never participating in.” I am a financial practitioner, and in the real-world market, that’s exactly how the option works. The buyer needs to pay the price to the writer of the option, and if the buyer did not execute the option, he/she will lose the money, and that’s where the profit of the writer comes from.

I point out this problem here because as I go through the EIP-2266, I found there is a “refund” function, but a refund of the cost to buy an option isn’t allowed in the real-world market. Please correct me if I misunderstood any of the contents. I wish that I provided some helpful suggestions here.


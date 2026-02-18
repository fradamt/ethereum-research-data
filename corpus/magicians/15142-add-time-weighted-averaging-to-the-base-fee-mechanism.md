---
source: magicians
topic_id: 15142
title: Add time-weighted averaging to the base fee mechanism
author: G_G
date: "2023-07-22"
category: EIPs > EIPs core
tags: [gas, base-fee-mechanism]
url: https://ethereum-magicians.org/t/add-time-weighted-averaging-to-the-base-fee-mechanism/15142
views: 1507
likes: 2
posts_count: 6
---

# Add time-weighted averaging to the base fee mechanism

Recent works (e.g., [[1](https://arxiv.org/pdf/2102.10567.pdf),[2](https://arxiv.org/abs/2304.11478)]) have identified incentive misalignments due to EIP-1559 base fee mechanism. In a nutshell, these benefit sophisticated users who are incentivized to bribe validators, and reap benefits on the expense of slow-reacting/naive users. Although the overall risk to the Ethereum network from these attack does not seem to be (currently) severe, there is a fix to the issue: adding past-weighted averaging to the base-fee calculation formula. By using a geometric series for the weights, a favorable tradeoff is achieved in which the adaptation delay is (negligibly) small and while the attack incentive is significantly reduced.

An EIP is currently being written.

## Replies

**Mani-T** (2023-07-26):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/g/ebca7d/48.png) G_G:

> Recent works (e.g., [1 ,2 ]) have identified incentive misalignments due to EIP-1559 base fee mechanism.

It seems so, in spite of EIP-1559 itself was designed to improve fee predictability and reduce the problem of fee auctioning. And your brilliant idea of improvements to the base fee mechanism could help mitigate any existing incentive misalignments or attack vectors.

---

**G_G** (2023-07-27):

Thanks for the support! I think a nice attribute of this fix is that it provides a simple solution to a (some what) complicated problem.

---

**G_G** (2023-07-27):

The [EIP](https://github.com/ethereum/EIPs/pull/7378) (still a pull request)

---

**shemnon** (2023-07-27):

Has anyone done the forensics to see if the attack in the Azuvi, et. al. paper has been carried out on any network?  Would the attack be detectable?

---

**G_G** (2023-07-30):

I don’t know of a forensic research on the topic. It would be particularly interesting, however, if it would discover correlation between different proposers that might be working together.


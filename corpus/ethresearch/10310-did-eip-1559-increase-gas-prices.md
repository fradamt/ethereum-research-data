---
source: ethresearch
topic_id: 10310
title: Did EIP-1559 increase gas prices?
author: kladkogex
date: "2021-08-11"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/did-eip-1559-increase-gas-prices/10310
views: 2629
likes: 3
posts_count: 9
---

# Did EIP-1559 increase gas prices?

Did anyone do research on preliminary effects of EIP-1559?

I am looking at etherscan, it seems to be lots of variance from one block to another.  Some blocks are heavy (over 20M gas), some really light.

Also, my impression is that gas prices did increase quite a bit on average  …

## Replies

**Mister-Meeseeks** (2021-08-11):

It’s tough to disentangle the direct effects of the EIP-1559 mechanism itself from the user/hype/marketing impact. It was a highly publicized event in the broader market, and that almost certainly created a flood of on-chain activity.

---

**Polynya** (2021-08-13):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> minary effects of EIP-1559?
>
>
> I am looking at etherscan, it seems to be lots of variance from one block to another. Some blocks are heavy (over 20M gas), some really light.
>
>
> Also, my impression is that gas

Gas prices were already on an uptrend, which can be attributed to the NFT boom, recovering crypto markets, among other things. It’s no surprise that it’s continued to accelerate, and London may or may not have coincidentally happened to release right in the thick of it. Miners are now forced to pay the basefee, so that might be having an impact on increasing the gas price, though 1559-style transactions across non-miner transactions may mitigate that overall. I believe we’ll have better data when more transactions are 1559-style. (Still only 20%, but rising fast as MetaMask and other wallets continue their rollout.)

---

**kladkogex** (2021-08-13):

It seems like the average gas per block did increase by roughly 10%

[![image](https://ethresear.ch/uploads/default/optimized/2X/3/39730767d07937509ba6119d4e6bd8c212fa7c98_2_690x326.png)image1204×569 38 KB](https://ethresear.ch/uploads/default/39730767d07937509ba6119d4e6bd8c212fa7c98)

---

**kladkogex** (2021-08-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/polynya/48/6945_2.png) Polynya:

> Miners are now forced to pay the basefee, so that might be having an impact on increasing the gas price

Whats the average split now between the base fee and the tip?

Etherscan does not show tips, which is bad …

---

**SebastianElvis** (2021-08-13):

There is a paper https://arxiv.org/pdf/2102.10567.pdf providing some insights and proving some bounds regarding EIP-1559. Not sure if this helps

---

**Polynya** (2021-08-13):

Currently, tips account for 13.58% for total fees for 1559-style transactions, according to [EIP1559 - Block Metrics: Base Fee (Burn), Tip, ETH Emissions, % Transactions (dune.xyz)](https://dune.xyz/msilb7/EIP1559-Base-Fee-x-Tip-by-Block).

---

**kladkogex** (2021-08-13):

So it is like an average US restaurant ![:grinning:](https://ethresear.ch/images/emoji/facebook_messenger/grinning.png?v=9)

Some things never change …

---

**MicahZoltu** (2021-08-15):

![](https://ethresear.ch/uploads/default/original/3X/e/1/e1ae42106c51c881c83b6e2219e4b0c9d2aa617d.png)

      [reddit.com](https://www.reddit.com/r/ethereum/comments/p4nloh/why_has_the_chain_capacity_increased_by_9_after/)





###










Barnebe also gave a short presentation in a call with wallet developers where they discuss some initial findings.  I’m not sure if it is available on YouTube or not, but you might want to ask around in #1559-fee-market on Discord if you are curious.


---
source: ethresearch
topic_id: 5365
title: Fee Market Change Working Group formation (and my proposed amendment)
author: AlexeyAkhunov
date: "2019-04-25"
category: Economics
tags: [fee-market]
url: https://ethresear.ch/t/fee-market-change-working-group-formation-and-my-proposed-amendment/5365
views: 2210
likes: 6
posts_count: 5
---

# Fee Market Change Working Group formation (and my proposed amendment)

There is already a great discussion thread going [here](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783)

Vitalik has made a presentation on the 18th of April 2019: https://youtu.be/HaT-BIzWSew?t=4708

If you watch after the presentation, there is a short discussion.

Since then, [@AFDudley](/u/afdudley) agreed to become the leader of a working group who will be working on this change, and see it through the research, reference implementation (prototype), and test generation. Please message DM him or post here if you would like to join the group, with the thought of what you can contribute and how much of your time you would like to commit.

I would like to propose an amendment to the original proposal (which you can watch in the video link above). Instead of changing the meaning some of the fields on a transaction, I suggest introducing a new transaction type, which will be used for the transactions following the new fee rules. The old, pre-existing transaction format would still exist (at least for some time). However, the initial gas limit increase will be created only for the new transaction type, and the old-style transactions will have to fit into the 8M gas like today. We make 8M a hard limit for the old-style transaction, and move the upward flexibility to the new-style.

Why?

**Firstly** , because it would allow introducing this change earlier. We would not need to coordinate the change with the wallet providers. The old-style transactions will continue working as it, and wallet providers will introduce the new one on their own schedule.

**Secondly** , if the theory behind this change turns out to be flawed, and the new fees will be costlier than the old one, it will not cripple the system because the old-style transactions will provide safety net. If, however, the new style proves to be successful, and the wallet providers are ready, then in the subsequent hard forks we can reduce the gas limit for old-style and increase gas-limit for the new-style based on the data.

## Replies

**DennisPeterson** (2019-04-25):

I see the transitional benefits of two transaction types but from an economic perspective it wouldn’t really be both systems running in parallel, it’d be a single new system that’s different and more complicated. The behavior of 1559 under this combined system won’t necessarily be the same as its behavior alone.

For example, miners could refrain from lowering `minFee` after a spike of unusually high-value transactions. With 1559 alone this would destroy transaction volume and miner revenue, but with the combined system, transactions would just move over to the old system and get to work outbidding each other like they do now. This is likely more profitable for the miners, in which case they could leave it that way and it’d look like 1559 failed.

This is similar to a conceivable attack under 1559 alone, where miners choose to keep `minFee` low in hopes of a premium bidding war over 16M. But that entails processing 16M gas per block. With the combined system and high `minFee`, they get their bidding war and still only have to process 8M gas.

---

**AlexeyAkhunov** (2019-04-25):

Thank you for the review!

![](https://ethresear.ch/user_avatar/ethresear.ch/dennispeterson/48/1675_2.png) DennisPeterson:

> The behavior of 1559 under this combined system won’t necessarily be the same as its behavior alone.

Yes, you might be quite right, I have not given this a lot of economic considerations, and that is why would like it to be discussed and debated a bit.

![](https://ethresear.ch/user_avatar/ethresear.ch/dennispeterson/48/1675_2.png) DennisPeterson:

> This is similar to a conceivable attack under 1559 alone, where miners choose to keep minFee low in hopes of a premium bidding war over 16M. But that entails processing 16M gas per block. With the combined system and high minFee , they get their bidding war and still only have to process 8M gas.

I forgot to mention another amendment that I was going to propose: make `minFee` adjustable by the protocol rules and not the miners. When I read EIP for the first time I was surprised that miners need to be involved into setting `minFee`, but perhaps [@vbuterin](/u/vbuterin)  gave it just as an example and left the actual mechanism of evolving `minFee` unspecified

---

**DennisPeterson** (2019-04-25):

Yes, that would fix it. I suggested that in another thread to fix the low-fee attack and Vitalik had a pretty interesting response: [DRAFT: Position paper on resource pricing](https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838/31)

If we did mandate the adjustment, another problem might be that we use 16M gas per block unless miners lower the old cap due to high uncle rates. (But it does seem like if they were willing to do 16M we’d be doing it already.)

---

**MadeofTin** (2019-05-31):

Working Group is moving forward with formation. We are looking for a:

- Senior Geth Dev
- Wallet Dev

Please DM if you, or you know someone who may be interested. I really appreciate any help as sourcing Geth Devs in particular has been a challenge.


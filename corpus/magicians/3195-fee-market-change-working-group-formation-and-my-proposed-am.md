---
source: magicians
topic_id: 3195
title: Fee Market Change Working Group formation (and my proposed amendment)
author: AlexeyAkhunov
date: "2019-04-25"
category: Working Groups > Ethereum 1.x Ring
tags: [eth1x]
url: https://ethereum-magicians.org/t/fee-market-change-working-group-formation-and-my-proposed-amendment/3195
views: 1984
likes: 8
posts_count: 3
---

# Fee Market Change Working Group formation (and my proposed amendment)

There is already a great discussion thread going [here](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783)

Vitalik has made a presentation on the 18th of April 2019: https://youtu.be/HaT-BIzWSew?t=4708

If you watch after the presentation, there is a short discussion.

Since then, [@AFDudley](/u/afdudley) agreed to become the leader of a working group who will be working on this change, and see it through the research, reference implementation (prototype), and test generation. Please message DM him or post here if you would like to join the group, with the thought of what you can contribute and how much of your time you would like to commit.

I would like to propose an amendment to the original proposal (which you can watch in the video link above). Instead of changing the meaning of some of the fields on a transaction, I suggest introducing a new transaction type, which will be used for the transactions following the new fee rules. The old, pre-existing transaction format would still exist (at least for some time). However, the initial gas limit increase will be created only for the new transaction type, and the old-style transactions will have to fit into the 8M gas like today. We make 8M a hard limit for the old-style transaction, and move the upward flexibility to the new-style.

Why?

**Firstly**, because it would allow introducing this change earlier. We would not need to coordinate the change with the wallet providers. The old-style transactions will continue working as is, and wallet providers will introduce the new one on their own schedule.

**Secondly**, if the theory behind this change turns out to be flawed, and the new fees will be costlier than the old one, it will not cripple the system because the old-style transactions will provide safety net. If, however, the new style proves to be successful, and the wallet providers are ready, then in the subsequent hard forks we can reduce the gas limit for old-style and increase gas-limit for the new-style based on the data.

## Replies

**ligi** (2019-04-25):

happy to join this working group from the wallet side and implement this new transaction type in WallETH. Really think this is a good idea and could improve UX alongside the other benefits this change has. Thanks [@AFDudley](/u/afdudley) for taking the lead and [@AlexeyAkhunov](/u/alexeyakhunov) for your idea with the new transaction type - I think this can really help rolling this change out. Very much hope the fee market change makes it into the next HF.

---

**MadeofTin** (2019-05-31):

I didn’t see this cross post! Thank you for this Ligi!


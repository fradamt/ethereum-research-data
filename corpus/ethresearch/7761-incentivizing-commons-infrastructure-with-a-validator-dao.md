---
source: ethresearch
topic_id: 7761
title: Incentivizing commons infrastructure with a 'validator dao'
author: djosey
date: "2020-07-27"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/incentivizing-commons-infrastructure-with-a-validator-dao/7761
views: 1433
likes: 1
posts_count: 1
---

# Incentivizing commons infrastructure with a 'validator dao'

[@Lars](/u/lars) mentioned something in a previous thread that I wanted to highlight/thought might deserve it’s own thread.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/lars/48/14_2.png)
    [Casper incentive manipulation / perverse incentives](https://ethresear.ch/t/casper-incentive-manipulation-perverse-incentives/1306/15) [Economics](/c/proof-of-stake/caspers-economic-incentive-structures/11)



> If a DAO is used for a validator pool, it can issue a coin/token to members. Payouts would go to the holders of these coins. Instead of having to dissolve the stake when someone wants to leave, it would be possible to sell your coins.

Been doing a bit of research on building a smart contract that would allow users to commit some portion of eth2 staking rewards into a dao pool, in exchange for a native token which would govern the dao; in this way, users could fund a pool for commons infrastructure while also supporting the security of eth2.  Seems to me like it won’t really work directly in the beacon chain phase at least without some kind of crazy oracle just because there’s no arbitrary state outside of accounts and staking.

I suppose there are probably some projects on eth1 today that have built similar abstractions without doing anything related to eth2, probably the next step for me is going to be to look at those models and see if there are any concepts/code that can be appropriated for this experiment. If anyone has any ideas or prior art on this I’d love to hear about them!

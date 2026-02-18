---
source: magicians
topic_id: 2249
title: On raising block gas limit (and State Rent)
author: AlexeyAkhunov
date: "2018-12-19"
category: Working Groups > Ethereum 1.x Ring
tags: []
url: https://ethereum-magicians.org/t/on-raising-block-gas-limit-and-state-rent/2249
views: 3816
likes: 11
posts_count: 6
---

# On raising block gas limit (and State Rent)

If we tie together two of the initiatives of Ethereum 1x, namely limiting the State growth (currently via State Rent), and short-term increase in scalability, we can ask and try to answer these questions (note this is a bit rough and might need some editing before it grows into something digestible):

1. Looks like uncle rate is slowly declining. Is it due to node operators slowly upgrading to Parity optimised version (which is currently in Beta), or mining centralisation caused by the dropping price? Probably a bit of both.
2. When can we raise the block gas limit, and by how much? Raising block gas limit is great, but the main worry is that it can (and probably will) accelerate the rate of state expansion.
3. We surely do not need to wait for the entire State rent to be rolled out before increasing the block gas limit. Can we just make state expanding operations (SSTORE, CREATE, etc.) more expensive? Then, recommend the block size increase approximately in the same proportions? For example, make state expansion 3 times more expensive, and recommend raising block size limit by 3 times? Yes, but there are issues to overcome.
4. First one, is hoarding and Dark Rent, as I described here
5. Vitalik suggested a “keyhole” solution to the hoarding and Dark Rent. The least invasive variant requires adding storagesize field to the contracts, which incidentally is also required for the introduction of State Rent. So perhaps we could introduce storagesize first, making State rent rollout simpler?
6. The second issue with raising the relative cost of state expansion is that it increases miners’ incentive to offer services to side-step this cost. Because miners receive the entirety of transaction fees, it makes them immune to any increase of penalties in the protocol. At some point, it can become worth to monetise this immunity to include state expanding transactions and refund customers part of the fee (or simply accept 1 wei gas price, which is, of course, more conspicuous).
7. The third issue with the raising the relative cost of state expansion are the current techniques of utilising non-uniformity of gas price over time. Such techniques include finding the best time of the day to deploy contracts, and leaving non-urgent state-expanding transactions to float in the transaction pool with very low gas price for hours, or even days. When the relative cost rises, these techniques will become more in demand, and more effective techniques will be developed, somewhat neutralising the taxing effect of the cost raise, and making the state space cheap only fort the “specialists” and their customers.
8. Partial solution to both issues mentioned in two previous bullet points is burning part of transaction fees, as well as reducing the time non-uniformity of gas price, similar what was suggested here.
9. The “Fee market change for Ethereum 1.0 chain” mentioned in the previous bullet point contains the right ideas, but I do not currently suggest implementing it as it is. More work is required to remove some IMO arbitrary things (like hardcoded gas limit, which is there for the sake of reusing the field in the block), as well as tailor it further to the “taxation” of state expansion
10. In the thread of the Github issue mentioned above, Nick Johnson implied that feedback systems like proposed are tricky, and require correct approach. He recommended a book on Feedback Systems, which I have, and I am intending to read it. The book is mainly concerned with continuous time systems, but apparently discrete time systems are very similar (but different)

**In summary**, with some extra work we might be able to chart a roadmap which takes us from where we are currently toward the State rent via fixes in the fee market and tax on State expansion and raising the block gas limit.

## Replies

**lrettig** (2018-12-20):

Thanks for this helpful summary, [@AlexeyAkhunov](/u/alexeyakhunov). On the first points only, regarding uncle rate and gas limit:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> Looks like uncle rate is slowly declining. Is it due to node operators slowly upgrading to Parity optimised version (which is currently in Beta), or mining centralisation caused by the dropping price? Probably a bit of both.
> When can we raise the block gas limit, and by how much? Raising block gas limit is great, but the main worry is that it can (and probably will) accelerate the rate of state expansion.

The uncle rate has been trending downwards for some time, and continues to trend downwards. The [Parity optimization](https://github.com/paritytech/parity-ethereum/pull/9954) is likely one factor, but the downward trend began much earlier, which suggests that there are other factors such as mining centralization, overall decline in network congestion, and maybe other improvements in connectivity/decreases in latency.

[![image](https://ethereum-magicians.org/uploads/default/original/2X/5/5464789e2b741d5935bb572a98b964747bb31c7c.png)](https://etherscan.io/chart/uncles)

Based on Vitalik’s math in [this article](https://blog.ethereum.org/2016/10/31/uncle-rate-transaction-fee-analysis/), and the fact that the uncle rate has declined by more than two-thirds over the past few months, if there is an increased likelihood of 1.86% of an uncle block for each additional million of gas added to a block, we could in theory raise the block gas limit by as much as 20-30 million and expect to end up back at a similar uncle rate as before. This is very naive math, and the relationship is likely not linear beyond a certain point; also this analysis was performed was two years ago so it would be nice to revisit it with more recent data. Obviously, we probably do not want to implement such a dramatic gas increase in the short term. But the point stands that it’s theoretically possible on the back of this data alone. We should discuss this, and consider a smaller increase.

---

**lrettig** (2018-12-20):

Actually, I think my math may be wrong. Using the same naive math:

> if there is an increased likelihood of 1.86% of an uncle block for each additional million of gas added to a block

Then a gas increase of 100%/1.86% =~ 54M would result in a doubling of the uncle rate. We’ve seen the uncle rate decline by 1/2 - 2/3, so the theoretical max increase here would be ~54-108M gas.

---

**AlexeyAkhunov** (2018-12-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Based on Vitalik’s math in this article, and the fact that the uncle rate has declined by more than two-thirds over the past few months, if there is an increased likelihood of 1.86% of an uncle block for each additional million of gas added to a block, we could in theory raise the block gas limit by as much as 20-30 million and expect to end up back at a similar uncle rate as before

The math in the article assumes strong correlation between consumed gas in the block and uncle rates. This correlation ostensibly comes from these causalities:

1. higher consumed gas → longer block processing times
2. higher consumed gas → larger blocks
3. longer block processing times → slower block propagation
4. larger blocks → slower block propagation (due to bandwidth limits)
5. slower block propagation → higher chance of mining an uncle (orphan in Bitcoin)

Numbers (2) and (4) can probably be ignored for now, because the blocks are relatively small.

The optimisation which existed in geth for a long time (only checking PoW before propagating the block), and is now in Parity Beta, weakens the causality number (3). By how much - I do not know, and this would be a good **question to simulation/emulation working group**. It is also weakened by the larger state caches (for example, recently introduced in geth) that miners would have warmed up if they are mining block containing similar sets of transactions.

Byzantium release has strengthened the causality (1), by introducing `REVERT` opcode.

It might be that in the near future, uncle rate will stop being a reliable indicator of network congestion.

---

**PhABC** (2018-12-30):

*I am here assuming that the main purpose of rent and gas limit proposals are for the “health” of the ecosystem and not to increase Ethereum’s throughput on the short term.*

[@AlexeyAkhunov](/u/alexeyakhunov)

> For example, make state expansion 3 times more expensive, and recommend raising block size limit by 3 times? Yes, but there are issues to overcome.

Increasing the storage cost (e.g. 3x) and a slight block gas limit increase (e.g. 1.5x) is fine, so long as this increase in block gas limit does not lead to significantly higher number of transactions. I am personally in favor of anything that slows the blockchain’s growth or keeps it constant such that hardware and networking costs slowly catch up.

> The second issue with raising the relative cost of state expansion is that it increases miners’ incentive to offer services to side-step this cost

I think this is only a concern if blocks are far from being full, where miners will start trying to find “marketing” strategies to ensure they have sufficient number of transactions.

> Such techniques include finding the best time of the day to deploy contracts, and leaving non-urgent state-expanding transactions to float in the transaction pool with very low gas price for hours, or even days.

Same as previous comment, it’s only a proper strategy if blocks are far from being full and many people will be happy to pay the premium. In addition, I’m not sure it’s a bad thing per say as it makes the network activity more stable overtime.

> Partial solution to both issues mentioned in two previous bullet points is burning part of transaction fees, as well as reducing the time non-uniformity of gas price, similar what was suggested here.

I’m personally not convinced point 6 and 7 will be significant problems in practice. The incentives for such behaviors are already present with the current storage cost and we could easily look into the data to see how common these behaviors are.

---

**zscole** (2019-01-11):

I’d like to share some of our research concerning uncle rates, gas limits, and the effect of various environmental variables on these factors.

https://whiteblock.io/library/ubiq-report.pdf

https://medium.com/whiteblock/how-do-uncle-blocks-affect-blockchain-performance-9ce43c958772


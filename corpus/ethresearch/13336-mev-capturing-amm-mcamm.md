---
source: ethresearch
topic_id: 13336
title: MEV capturing AMM (McAMM)
author: josojo
date: "2022-08-10"
category: Applications
tags: []
url: https://ethresear.ch/t/mev-capturing-amm-mcamm/13336
views: 20273
likes: 59
posts_count: 25
---

# MEV capturing AMM (McAMM)

# MEV capturing AMM (McAMM):

A prevailing thought is that the power of transaction ordering is mostly in the hands of block-builders in the current MEV-Boost and PBS specifications. In this write-up, ideas for new AMM designs are presented that would shift the transaction ordering power, at least partly, to AMM designers and liquidity providers. These constructions would allow AMMs to capture part of the MEV that is currently only harvested by block-builders and proposers.

## High-level idea:

New MEV capturing AMMs can auction off the right of the first trade per block via a smart contract auction. This would imply that normal users can only trade against the McAMMs after the auction winner has traded, as otherwise, their trade will fail. It turns out that in such a setup, it is game theoretically optimal for block-builders to respect the first execution right of the AMMs and sort trades such that the first trade is done by the auction winner and normal user trades are not reverting. By auctioning off the first trade per block, AMMs can basically sell their MEV and capture a revenue from it. Since most MEV can usually be extracted with the first trade in a block, McAMMs and their LPs can capture most of their MEV with this mechanism.

## Specification

There is one global contract that manages all McAMMs’ first execution right. For gas efficiency reasons, that contract should be the standard router contract for all McAMMs pools. The first execution right is assigned to the so-called *leadsearcher*. The global router contract will store per block the information whether the leadsearcher has already traded on any of the deployed AMM contracts. Only if the leadsearcher has already traded, then others are allowed to trade against the McAMMs. Otherwise, the trades revert.

This mechanism works as block-builders have a natural incentive to put the leadsearcher transaction before the other trades, as explained in the next paragraph.

To become the leadsearcher, one has to win the auction for the first execution right. The auction will be held by the router contract and could be similarly structured to the [eden networks auction](https://docs.edennetwork.io/slot-tenants/getting-started#becoming-a-slot-tenant) for the first slot in a block.

Leadsearchers become automatically deselected by the router contract if they missed more than 3 blocks. This prevents them from blocking trades for a longer period. If leadsearchers don’t wanna trade in a block, they should anyway send a transaction that just signals that they touched the McAMMs such that others can trade against the McAMMs. (This costs only 40k gas for the lead searcher).

To enable the *leadsearcher* to capture all arbitrage opportunities, not just the ones that are profitable after paying the AMM fees, the lead searcher should not pay any normal AMM fees. Thereby, the McAMMs grant the leadsearcher a more flexible fee structure, but still harvest the fee, as it will be priced into the auction.

**Incentive structure for block-builders:**

Block builders have an incentive to propose blocks with the highest priority fee gas consumption, as they can charge the priority fee and thereby they are more likely to win the MEV boost auction. Since failing trades have a lower priority fee gas consumption than fully executed trades - assuming each trade has a priority-fee > 0 -, the block builder are incentivized to make the trades of the McAMM not revert. Hence, they will put leadsearcher’s tx before the regular user’s trades.

(Only for full blocks, there might be from time to time situations in which a failed trade would maximize the consumed priority fee.)

Additionally, users of the McAMM have a high incentive to only broadcast their trades to block-builders respecting the enforced ordering by the McAMM, as otherwise, they have to carry the failed transaction gas costs.

Both factors are expected to drive all block-builders to respect the ordering necessary for McAMMs, once one block-builder with a bigger marketshare is starting to offer this service.

## Analysis:

- Using data from the Eden network, the MEV extracted per block by the first transaction is currently estimated at around 9$ per block. This MEV value is expected to increase over time with more sophistication of the MEV extraction and deeper on-chain liquidity. The 9$ was derived by looking at the Eden auctions for the first slot in a block: Daily fees paid by the current slot 0 holder are currently 693,775 * 0.033 * 0.13$=3000$ and on average 325 blocks are produced by Eden Network per day that put the slot holder at the first position. Hence searchers are paying these days 3000/325 =9$ per block to be at the leading position. Compare to this dune query.
- McAMMs have the disadvantage of an additional gas cost of ~2.1k (2100gas read storage ) per trade compared with usual AMMs since the transaction would have to read a storage variable in the router contract to check whether the leadsearcher has already traded. Assuming 20 trades per block, the gas cost increases are 2.8$ (=2100 * 20 * 40 /10^9 *1700) at 40 Gwei gas prices and 1700$ eth prices for all users. However, especially on L2, this additional cost seems to be negligible.
- There might be additional costs for the leadsearcher to always touch the McAMM router to enable others to trade, even if there is no arbitrage opportunity. However, this is expected to happen very rarely, as between two blocks (in 15 secs) usually some price of some token that is traded on DEXes and CEXes moves and thereby creates a profitable arbitrage opportunity for the leadsearcher.
- The upper numbers allow us to estimate very roughly McAMM’s additional revenue by ~9$ on L2s and ~ 9$-2.8$ = 6.2$ per block on ethereum. Hence, this construction is particular valuable on L2s. The estimated revenue from MEV would be roughly 1/30 of the current AMM fees that Uniswap is earning.
- Eden data also shows that the first position in a block is by a factor of 10 more valuable than the second position - currently the first slot costs 693,775 * 0.033 Eden per day compared to the second slot 65,847 * 0.033 Eden per day. Hence, it makes sense for McAMMs to auction off only the first execution right. This would probably reduce the AMMs MEV footprint already by 2/3.

Potential issues:

- Not all proposers will run MEV boost, hence naturally blocks will be missed in which the McAMMs are not traded by users - assuming users only broadcast their transactions to block-builders supporting the protocol. This might increase the waiting time for users. The leadsearcher will always trade in each block. Their transaction can not revert and hence can be broadcasted into the public mem-pool. But users are expected to migrate to block-builders as they offer valuable features like MEV-protection and revert-protection.
- For the AMM smart contract, it is not detectable whether a missing leadsearcher transaction is caused by censoring from block-builders/proposers or by the misbehavior of the leadsearcher. However, since block-builders have a natural incentive to include the leadsearcher transaction, this might not be a real issue and one can expect that it is due to a fault of the leadsearcher.
- Asking users to pick a reliable block builder that respects the ordering, might be a small UX challenge.

## Philosophical comparison to HFT:

In TradeFi, exchanges sell speed technology to high-frequency traders to be the first ones trading. One could argue that this proposed mechanism is similar, as AMMs are again selling the “first trade”. However, a fundamental difference is that in tradeFi the proceeds of the selling of the speed technology go to the exchange - a value extracting middle-man -, while for this proposed mechanism, the proceeds are going back to the liquidity providers of the AMMs. Assuming more revenue for LPs leads to deeper liquidity, the end-users are also benefiting.

## Further research topics:

- In the upper specification the leadsearcher is only one entity. Probably this is suboptimal, and a more optimized construction could resell the first execution right to different parties.
- For further efficiency, the first execution right might be set on a smart contract level not per global router contract, but per eco-system: E.g. all AMM projects could define the contract that maintains their “leadsearcher”

CowSwap team has further ideas for such McAMMs. If you are interested, please connect to us.

## Replies

**alexnezlobin** (2022-08-18):

Interesting. Do you have any thoughts on how to allocate the collected fees among LPs of different pools?

Also, it might be useful to think about the optimal bid duration in the continuous auction (if I understand the process correctly). If the bid has to be for a long period of time by trading standards, then it might create a barrier to entry for searchers and thus reduce competition. To outbid the current lead searcher, some other searcher would need to be convinced that they can generate a higher value over a long period of time. And this value is uncertain because of the market conditions. So I would say that the net result is that this bidding process is riskier for searchers than competing in each individual block, meaning that they would probably bid less than they otherwise would.

---

**josojo** (2022-08-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexnezlobin/48/9749_2.png) alexnezlobin:

> Do you have any thoughts on how to allocate the collected fees among LPs of different pools?

The most straight forward implementation would be that all the fees from the auctions are first collected in a common treasury, and then the DAO redistributes them via a predefined process. Sure, this is not the most elegant way, but should work reliably. We have also other ideas how the leadsearcher can book the arbitrage profits directly to the LPs while they are trading. But these ideas are not yet ripe for sharing.

> It might be useful to think about the optimal bid duration in the continuous auction

Yes! This definitively needs more evaluation. Generally, I agree with your argumentation. However, one has to find a good trade-off between the gas-costs of the running the auctions and additional risk for leadsearcher to buy slots for a longer time period.

---

**bowaggoner** (2022-08-19):

May I recap the problem and ask about a similar approach? It sounds like this MEV is coming from cases where it is beneficial to trade faster/first, e.g. arbitrage situations or high frequency trading type scenarios. The traders are willing to pay a lot to be first, and the miners can extract some of that. The trader who wins the race gets a lot of profit, but they are not really viewed as providing much value to society over the person who loses the race. So there is a fairness question of who should get to capture the value. Miners seems unfair, letting the trader keep it isn’t necessarily desirable.

Your proposal allows the automated market makers to capture some of the value. My understanding is that all the McAMMs would have to coordinate to be part of the proposal? I’m wondering about more decentralized solutions the AMMs can implement themselves.

Specifically, the AMM could have a slower “tick” time. If multiple trades all arrive within one tick, they are batched and executed together in a way that treats them all equally. Concretely, if a ton of orders all arrive to buy A during the same minute, none of those orders will get the original great price for A.

Different AMMs do compete with each other, but that might be okay – the slower traders would rather send their business to one of these slow-tick AMMs rather than the one that rewards the fastest trader, so they should be able to compete.

How does this compare to your suggestion of a mechanism at the block builder level? Thanks.

---

**alexnezlobin** (2022-08-19):

> We have also other ideas how the leadsearcher can book the arbitrage profits directly to the LPs while they are trading. But these ideas are not yet ripe for sharing.

Yes, you could try to allocate the fee to the affected liquidity, roughly speaking, in proportion to the price impact in each pool. One issue is that you would need to have conversion rates from ETH to all the tokens that the lead searcher is trading. And then I would imagine that the lead searcher could create their own token or a pair of tokens, and use trades in those artificial tokens to collect back the fees.

Look forward to seeing what you come up with!

---

**fleupold** (2022-08-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/bowaggoner/48/7119_2.png) bowaggoner:

> I’m wondering about more decentralized solutions the AMMs can implement themselves.

This proposal can be implemented by AMMs themselves. They would store the address of the lead searcher and the last block they trades. The AMM would then revert if a swap is called by someone else and the lead searcher hasn’t transacted in the current block yet.

![](https://ethresear.ch/user_avatar/ethresear.ch/bowaggoner/48/7119_2.png) bowaggoner:

> Specifically, the AMM could have a slower “tick” time. If multiple trades all arrive within one tick, they are batched and executed together in a way that treats them all equally. Concretely, if a ton of orders all arrive to buy A during the same minute, none of those orders will get the original great price for A.

I think this is difficult to implement at the AMM level without breaking atomicity of transferIn/transferOuts. [CoW Protocol](https://cow.fi/) is actually implementing this type of batching on a layer above the AMMs (netting traders p2p and settling the excess on the best available AMM).

![](https://ethresear.ch/user_avatar/ethresear.ch/bowaggoner/48/7119_2.png) bowaggoner:

> So there is a fairness question of who should get to capture the value. Miners seems unfair, letting the trader keep it isn’t necessarily desirable.

Agree that it should be the LP since they are the ones incurring the cost. This type of MEV has been more formally quantified in ongoing [research](https://moallemi.com/ciamac/papers/lvr-2022.pdf) by Jason Millonis, Tim Roughgarden, al. In their work they conclude that providing liquidity in traditional AMMs is incurring a cost compared to actively mimicking a rebalancing strategy on CLOBs (they call it loss versus rebalancing LVR) which today is offset by trading fees. However since trading fees are mainly affected by noise trading volume and volatility it’s quite hard to model the correct fee amount with a fixed fee tier (instead they should be adjusted based on volatility over time).

This proposal basically off-loads the decision on how to value LVR to professional searchers which bid ex-ante for the optionality to get exclusive first execution right.

---

**hasu.research** (2022-08-22):

Good to see more experiments with first-right-arbitrage AMMs, finally.

Why is the adoption of mev-boost needed for your mechanism to work? Is it because only a builder would simulate the block to correctly “unlock” the liquidity pool, whereas the “simple greedy” consensus layer client algorithm wouldn’t?

---

**bowaggoner** (2022-08-22):

Thanks for these responses. I guess one way to think of it is the general solution of batching orders (rather than truly treating them in chronological order) is already provided at the block level, simply by how blockchains work. This proposal takes advantage of that batching in a nice way without having to implement its own batching such as in my comment.

I definitely like the proposal of auctioning off the right to trade first. The game theory seems interesting - for example, is there a winner’s curse? If I know exactly which noise trades are going into the block, do I sometimes want to trade last instead of first? If block-builders are also traders, what can go wrong?

---

**josojo** (2022-08-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/hasu.research/48/16634_2.png) hasu.research:

> Why is the adoption of mev-boost needed for your mechanism to work? Is it because only a builder would simulate the block to correctly “unlock” the liquidity pool, whereas the “simple greedy” consensus layer client algorithm wouldn’t?

Yes, with block-builders there are better guarantees for the McAMM users:

1. Blockbuilders want to optimize their rewards and that would force them to put all user-trades behind the lead-searcher’s tx - this enforces the “correct unlocking of pools”. The reason is that block-builders want the transactions to consume as much as gas possible, such that the ethereum transaction fee-tip for the builder is higher. If the builders put a transaction before the leadsearcher’s tx, then it would revert and consume less gas and hence would result in less fees.
2. Additionally, block-builders could promise the users to not include their trades, if the lead-search misses a block.

To my understanding, the “simple greedy consensus” would sort orders simply by the gas-price per gas amount. In that scenario, a proposer would likely build a block that puts a user-trade before the leadsearcher - and hence “incorrectly unlock the pool” -, if the user’s gas price per gas amount is higher than the leadsearcher’s gas price per gas amount. Maybe one could enforce that leadsearchers must include a certain eth-fee tip per gas amount and users could just choose a lower fee-tip per gas amount, but then it’s getting more expensive for the leadsearcher and more complex in general.

---

**josojo** (2022-08-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/bowaggoner/48/7119_2.png) bowaggoner:

> The game theory seems interesting - for example, is there a winner’s curse? If I know exactly which noise trades are going into the block, do I sometimes want to trade last instead of first? If block-builders are also traders, what can go wrong?

I think it should not be a curse. I think leadsearchers would very likely always find one pool, which they can arbitrate if they are trading first. Yes, you are right that additional trades at other specific positions could provide more value, but this does not diminish the fact that the first position usually is valuable itself.

I also hope that in the future, exploiting noise-trades in the same block becomes infeasible: I would hope that most users will use a mechanism that protects them from it: Either a block-builder endpoint like flashbot protect rpc or dapps like cowswap, or any other method.

---

**maxholloway** (2022-08-23):

Neat idea! Here are some thoughts on optimal bidding strategies: [link](https://colab.research.google.com/drive/1aBgzstpIG6-rTcCH4hzTP1iOOTaLnNQ8?usp=sharing).

**Tl;dr:**

- Repeated auctions have a humongous set of non-trivial Nash equilibria.
- An intuitive conjecture is that searchers’ bidding strategy will be to maximize the stage game utility in each auction. In that case, depending on the distribution of top-of-block MEV that the searcher estimates they can receive, and the searcher’s utility w.r.t. profits, you can calculate the amount they’d be willing to pay while keeping utility positive (i.e. their valuation). If you use something like a 2nd price auction for each McAMM, they will bid this valuation.
- The more risk-averse the searchers, the lower the auction revenue. The higher the expected top-of-block MEV, the higher the revenue. The higher the stdev of the top-of-block MEV, the higher the revenue (similar mental model to asset volatility in options pricing).
- We can think of the auction revenue as being equal to the expected top of block revenue minus some risk premium for the scenario that MEV does not accrete on that block.
- In a simple example that I ran in the above jupyter notebook, (Auction revenue) + (blockchain fixed cost) was ~80% of the top-of-block expected MEV. This figure should be taken with a grain of salt.

**PS: this is a super neat problem, and if anyone wants to collaborate on thinking through the game theory of it, [DM me](https://twitter.com/max_holloway)!**

---

**BrunoMazorra** (2022-08-23):

I’ve been thinking about this idea for a while and seems cool! I would try to explain some of my thoughts/potential problems:

- This seems the dual version of CoW protocol (repaying to the LP and not to the trader). I think this is interesting, is well known that LP is just bagholders (https://moallemi.com/ciamac/papers/lvr-2022.pdf).
- I think the fundamental problem is the MEV distribution. To me, it seems that for every objective function/mechanism of MEV distribution through LP, there is a wash trading strategy to misallocate the MEV. Even with off-chain oracles. For example, by creating worth-less tokens (misleading the TVL) and creating fake volume + fake MEV. A way of countering this would be to blacklist and whitelist tokens. However, this would imply that low liquidity pools wouldn’t have access to MEV revenue. Making the MEV distribution by construction “unfair”.
- Another way of mitigating wash trading strategies could be through burning MEV, similar to the EIP-1559. This could ensure that creating fake volume (MEV) wouldn’t lead to more revenue for the “adversary”.
- I’m not sure that it is always incentive compatible. Imagine that there are two big MEV opportunities one using only McAMM and another one using McAMM and AMM. In this case, the builder could use the second TMEV (on top of block MEV) tx/bundle. A.k.a this would lead to rationally censoring the McAMM.

---

**markus_0** (2022-08-30):

Glad to see these types of designs discussed. I think it’s rather important that we figure out better ways for dApps to capture their own MEV, or app chains will become increasingly popular since they are the clearest way for an app to capture its own MEV.

One important downside of this design is it’d make manipulating TWAPs significantly easier. A lead searcher can manipulate an asset price and hold it for 3 blocks guaranteed. It’d make attacks like the Inverse Finance one much easier https://twitter.com/FrankResearcher/status/1510239094777032713?t=HUbwnR7apLz1sWgBB8j9-w&s=19

A potential solution would be allowing multiple leadsearchers to exist for one pool, which I don’t think has any downsides. If anything, it’d probably mean less AMM downtime.

---

**FernandoMartinelli** (2022-09-07):

Great discussion and agreed we should finds ways for dApps to capture MEV instead of incentivizing them to create their own app chains. After all, what makes Ethereum and DeFi so great is the composability and permissionlessness.

After reading this my idea was to use an NFT with Harberger taxes/rent going to the pool (i.e. adding value to LPs and the protocol if any protocol fee is activated). This NFT would allow its owner to use the first trade in that pool for any block.

Anyone would be able to buy that NFT if they think they can pay a higher “rent” to have the privilege of being the first traders of a block.

This could simplify a lot things by removing the auction part of the original proposal. NFT holders would have to do the math of how much it’s worth it and any one using it more wisely would be willing to pay more rent and buy it.

Hope others can build on top of this? Surely Balancer has a flexible enough architecture that would allow for this to be implemented/tested in a PoC.

---

**apadenko** (2022-09-07):

Cool concept! Very interesting

Are there any limitations to trade actions that the leadsearcher can perform?

Can the leadsearcher simply front-run some up-going trades in the current block, knowing his block position is guaranteed, and then even do a sandwich from other EOA?

Or is it expected and basically the idea is that AMM will capture such types of profit because of the auction competition?

---

**mkoeppelmann** (2022-09-08):

To minimize friction I would also suggest that if a user does a trade in a block that has not been traded yet by the “lead searcher” it does not automatically fail but instead the fee/spread is simply higher.

The simple intuition is: if the pool just had a trade by the “lead searcher” you know it is “set” to the correct price. Thus you can charge fairly low fees.

---

By the way: I think making pools exclusively accessible to cowswap solvers but in returning demanding to become a “first-class citizen” (= get the uniform clearing price) instead of simply the price the pool demands should result in a very similar outcome.

---

**tbosman** (2022-09-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> To minimize friction I would also suggest that if a user does a trade in a block that has not been traded yet by the “lead searcher” it does not automatically fail but instead the fee/spread is simply higher.
>
>
> The simple intubation is: if the pool just had a trade by the “lead searcher” you know it is “set” to the correct price. Thus you can charge fairly low fees.

Nice idea. I suppose you need to make sure that the fee increase always outweighs the arb opportunity, otherwise a third party could still outbid the leadsearcher profitably.

An idea I have been toying with that would discover this fee automatically is this:

users trades are executed at the least favorable of the *current AMM price* and the spot price *the last time the leadsearcher traded*. This means that if an order moves the AMM a lot, the spread will widen until the leadsearcher moves it back or other user order balances out the impact.

Effectively this is like dynamically setting the fee just high enough we are sure any potential arbitrage opportunity is cancelled out.

With this setup it’s impossible for anyone but the leadsearcher to extract value from arbitrage opportunities created by regular users. In particular, it makes it unprofitable to sandwich users unless the leadsearcher is inside the sandwich: if you frontrun a user, and they trade in the same direction, the price in the reverse direction won’t improve until the leadsearcher has traded. So, regular users can safely use the mempool, and only leadsearchers need to take protective measures (eg use trusted validators).

---

**The-CTra1n** (2022-09-13):

Myself and [@BrunoMazorra](/u/brunomazorra) had look at McAMMs, and other MEV-distribution techniques as part of the recent MEV Hackathon. It seems there could be some quirky centralization effects to the McAMM approach. As was reasoned and shown in the [loss-versus-rebalancing paper](https://moallemi.com/ciamac/papers/lvr-2022.pdf), AMMs are currently selling straddle options. McAMMs are asking players to pay the fair price for bundles of straddles (number of straddles equal to the number of blocks in which winning an auction gives priority). Pricing is complex, risk-tolerance needs to be high, and external liquidity needs to be as frictionless as possible, so McAMMs are likely restricted to very few players.

A proposal we had was for protocols to actively auction off the right to submit the first transaction on a per-block basis. Off-chain auctioneers are chosen by protocol participants, or some hardcoded scoring mechanism (maybe something like what is happening with CoWSwap solvers), who run the per-block auction for the first tx for the respective protocols. Volatility risk is significantly reduced, and pricing is straightforward. It places a lot more risk in off-chain agreements, but we are hoping that our re-election of auctioneers can react to this. Early doors still though.

---

**bpiv400** (2022-09-14):

I’m not an ethereum person so this is maybe speaking out of turn ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

What I suspect will happen is that searchers will predict price movements from other transactions they scope out of the mempool and submit these in the same block to capture back of block arbs, leaving very little profit opportunity for the searcher that goes first. This is the state of arbitrage in Osmosis today, for example.

Why am I wrong about this?

---

**josojo** (2022-09-25):

Wow, thank you all for all the support and love this idea has gotten. It’s really great to see that first prototypes are developed on hackathons, etc. If someone continues to be interested in helping to build it, feel free to DM me.

One reason why McAMMs got so much traction is the work of Tim Roughgarden’s team: The description of Loss Versus Rebalancing (LVR). We as a community recognize more and more that LVR is an important metric for LPs and McAMMs are one potential mean to minimize LVR for LPs.

I agree with the many voices stating that we first need to find a solution for redistributing the auction proceeds to the LPs, before we can start any serious implementations.

Here, I want to share one further idea - that for sure comes with big trade-off and seems quite complex ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) .

It uses the concept of re-auctioning the right to trade first, which was first thought of by [@hasu.research](/u/hasu.research).

## Idea for returning captured MEV to LPs:

**High level idea:**

The right of first execution is again auctioned off globally for all AMMs, but the auction winner - called the lead-auctioneer - has to re-auction the individual slots per AMM.

The lead auctioneer has to determine the auction winners per AMM and bundle their trades into one lead auctioneer’s transaction. This transaction contains the information of the highest bid per AMM-auction, and each AMM will receive their highest bid value as a fee for their LPs. The lead-auctioneer is required to prove that they behaved correctly with a zk-proof, afterwards.

**1.0 - Centralized version:**

- Onchain, we continue to have one auction for the right of first execution for all AMMs belonging to a router.
- However, the first transaction can not freely be chosen, but has to be crafted by the following process:

 The lead auctioneer has to re-auction for each AMM the right to trade against this AMM first.
- Each bidder will have to send their bids encoded as an AMM-interaction with the following information:

where LVR compensation bid is the bidding amount nominated in the AMM-pair’s ‘sell token’ - which depends on the direction the AMM is traded against - to win the right of first execution for the specified AMM contract.
- gas-cost-refunds are an ETH amount specified by the arbitrageurs to pay for the gas cost
- trade payload is a trade that will be executed against the AMM on behalf of the arbitrageur to capture the arbitrage opportunity. The payload will be executed from a “lead auctioneer router contract”
- the signature is a signature from the arbitrageur for their trade.
- (participating arbitrageurs would have to set an approval for their trade for the lead auctioneer router contract beforehand, that allows the lead auctioneer to execute their trade given their signature)

The lead search will compile a list of “winning AMM-interactions”:

- the list will only have 1 entry per AMM
- each entry must have a valid and executable payload on the latest block
- all entries are winning: I.e., they are maximizing the LVR compensation bid on a per-pool basis.

The lead auctioneer’s transaction will execute the list of AMM-interactions on the lead auctioneer router contract.

The LVR compensation will be withdrawn from the arbitrageurs accounts and paid to LP providers in the pool as a normal fee.

Only a small portion of the LVR-compensation will be sent to the lead auctioneer for their work. This is called the LVR compensation fee.

The revenue for the lead auctioneer is the sum of LVR compensations fees.

Hence, we can expect that the first slot will be auctioned off for the expected LVR compensation fees minus the operational costs.

**Challenges in this spec:**

This specification requires trust in the lead auctioneer. There is no mechanism enforcing the lead auctioneer to include the highest LVR compensation bids into their transaction and not censor any transactions. This can be solved with the following spec:

**1.1 Decentralized version:**

We have the same setup, as described in the centralized version and additionally, we require:

- The lead auctioneer needs to provide a bond before participating in the global auction.
- There will be several Distributed-key-generation-validators (DKG-validators) selected by the DAO. They will generate for each auction a public key used to encrypt bids, and after the auction end -shortly before block-building -, they will reveal a private key to decrypt bids.
- The lead auctioneer will collect the encrypted bids from the arbitrageurs.
- The lead auctioneer will build a “commit hash”: The Merkle root of his collected bids
- The DKG-validator will agree on one “commit hash” from the lead auctioneer, sign it off and reveal their key. This allows the lead auctioneer to decrypt the bids. Since the DKG-validators double-check the commit-hash, they act as on non-censorship oracle.
- The lead auctioneer will decrypt the AMM-interactions, build the tx with the highest bids and send it out immediately.
- Some blocks later, the lead auctioneer is required to provide a zk-proof that proves that their tx was built indeed correctly and the highest bids of all bids considered in the Merkle tree of the “commit hash” were included.
- If the lead auctioneer does not provide the proof of their correct behavior, they will lose their bond.

**Discussion:**

Unfortunately, the 2.0 version is very complex and requires a DAO to deploy certain actors. This is suboptimal, especially since the DKG-validators can grief the auction winners by not providing their decryption keys in time. Hence, the majority of DKG-validators must be assumed to be good actors.

I think the community should definitively search for simpler and more beautiful solutions ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) .

---

**josojo** (2022-10-15):

I want to share another idea for distributing the LVR to LPs. It should be much more practicable compared to the upper one:

First, we introduce the concept of **surplus-charging AMMs**:

[![](https://ethresear.ch/uploads/default/optimized/2X/4/4d7d8fdaefb9c5f86854e78faf194c9b0c3ac104_2_281x207.png)922×680 31.4 KB](https://ethresear.ch/uploads/default/4d7d8fdaefb9c5f86854e78faf194c9b0c3ac104)

**AMMs charging surplus:**

- A regular trade against an AMM generates an effective trading price and a new marginal price (see picture)
- The difference in the receiving output between the trade with the effective price and the trade with the marginal price is called the surplus of trade. It’s described by the blue area in the picture.
- An AMM charging surplus forces a trade to be executed at the new marginal price and gives the surplus to the LPs
- Note that one can calculate the surplus that each tick contributed and distribute the surplus fairly between the ticks

In the following, we combine the idea of surplus charging AMMs with McAMMs.

**Surplus charging McAMMs:**

The overall idea is:

If lead searchers are incentivized to trade against the AMMs at the marginal price, then they will increase the surplus fee for LPs, and thereby will automatically distribute the LVR to the LPs.

We define AMM intervals of n blocks. Everyone can buy the right of the first transaction per pool for the AMM intervals in an auction.

Then, we define the following meta-game for lead searchers:

- One becomes the leadsearcher by winning an auction for a pool
- Lead searchers are bonded by the bidding amount
- With each trade of the leadsearcher, the AMM measure the fees paid for the pool
- If lead searchers have reached the threshold of bid surplus fee for the interval they were bidding with, they are allowed to trade for free against the McAMM and capture all the remaining LVR as their profit.
- If lead searchers are not reaching the promised surplus fee, their bond will be slashed by the difference. This difference is put into the LVR buffer.
- If leadsearcher made the threshold of the estimated LVR - their auction bid - and continue trading for free, the LVR buffers can be to still pay fees to LPs.

With these game rules, lead searchers are expected to estimate the real LVR and then bid this value minus expected transaction costs and minus service margin. After a leadsearcher has won the auction for the next n blocks, they will try to generate the surplus fee by capturing the LVR of the AMM and doing their best in arbitraging between the AMM’s CEXs. Once leadsearchers have reached their bidding-limit, the AMM will no longer charge the surplus and the lead searchers can pocket the arbitrage.

Probably, it’s only worth becoming a lead searcher during volatile periods. But this is not a weakness of the protocol, since MEV capturing is mostly needed during times of high volatility.

Details about a possible auction:

The auction for the n-block interval [x, x+1, … x+n-1] could be running over the n blocks [x-n, …, x-1]. If there was no bid in the blocks [x-n, …, x-1], then one can still become the lead searcher for the interval [y,y+1, …,x+n-1] by providing the winning bid in block y-1. With one transaction, one can bid for many pools simultaneously. The most rational strategy for lead searchers might be to bid in the block x-1 sealed via an API like flashbots protect.

**Discussion:**

- Gas efficiency: One leadsearcher could bid on many pools with their expected LVR and then be the selected leadsearcher for many pools at the same time to have the gas savings. Combinatorial auctions would be the best to hedge the bidders costs. But they also introduce a lot of complexity.
- Wash trading is still a small concern as the leadserchers can provide deep liquidity within one block, and then trade against themselves and hence pay themselves the fees. But one could introduce some new rule that fee-surplus is only distributed to “old/longer existing” LP positions, to hinder wash trading
- Some LPs might not get their fair share of surplus fees, as the buffering of LVR is not perfect. This creates suboptimal meta-games


*(4 more replies not shown)*

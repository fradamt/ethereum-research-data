---
source: ethresearch
topic_id: 6897
title: Announcing MetaCoin—The Governance-Minimized Decentralized Stablecoin
author: ameensol
date: "2020-02-09"
category: Applications
tags: []
url: https://ethresear.ch/t/announcing-metacoin-the-governance-minimized-decentralized-stablecoin/6897
views: 17666
likes: 36
posts_count: 39
---

# Announcing MetaCoin—The Governance-Minimized Decentralized Stablecoin

# MetaCoin v0

Of all the stablecoins on Ethereum, the only one that isn’t backed by banked fiat is MakerDAO’s DAI. Instead, DAI is backed by ETH, and the peg to $1 is maintained by the governance of the MKR token holders. The smart contract system has several components, including:

- minting new DAI by depositing ETH as collateral
- price oracles for ETH
- liquidation of ETH collateral if price crashes
- variable interest rates charged to DAI minters to target 1 DAI = $1
- governance mechanisms to select price oracles and update interest rates

This system is quite complex, leading some critics to be flabbergasted.

https://twitter.com/davidgerard/status/1213967354641731585/

The complexity also hides centralized points of failure, some of which are exceptionally severe and can result in a catastrophic and instant loss of all ETH in the system. Case in point, MakerDAO currently has at least four *custodians* , each of whom can, at will, steal 100% of the ETH collateral deposited in MakerDAO, also print a gajillion DAI, and then use that DAI to steal 100% of the ETH liquidity offered for the ETH/DAI pair across all decentralized exchanges (e.g. Uniswap) and lending protocols (e.g. Compound). The custodians, the Maker Foundation, a16z, PolyChain, and Dragonfly, could execute this entire heist in a single atomic Ethereum transaction, before anyone has a chance to respond.

https://medium.com/coinmonks/how-to-turn-20m-into-340m-in-15-seconds-48d161a42311

In light of MakerDAO’s recent upgrade to Multi-Collateral DAI (MCD) and decision to abandon ETH as the sole form of collateral (thereby introducing counter-party risk for offchain assets), it’s worth considering what a governance minimized, ETH-only system might look like. The goal of such a system isn’t be to usurp DAI’s position as the de facto decentralized stablecoin, but rather to create a safe alternative for those who have different risk preferences.

One potential design for such a system (MetaCoin) has the following components:

- a governance & rewards token called META
- a stablecoin called COIN
- minting new COIN when ETH is deposited
- a token curated registry (TCR) of fiat-backed stablecoins (i.e. USDC, USDT, TUSD)
- the volume-weighted average price of the stablecoin basket on Uniswap as the price oracle
- liquidation of ETH collateral if the price crashes
- variable interest rates charged to COIN minters to target 1 COIN = $1
- an algorithmic controller (PID) that autonomously updates interest rates

The most important differences between MakerDAO and MetaCoin are the price oracles and the role of governance in setting the interest rate. The general idea of depositing ETH collateral to mint new stablecoins (DAI or COIN), and actively liquidating those minters if their collateral value drops, is preserved.

## Price Oracles

In MakerDAO, the price oracles are selected by the governance and submit updated prices every 6 hours. The median of all reported prices for the duration is used to determine the reference price for ETHUSD.

In MetaCoin, the governance system does not select price oracles directly. Instead, the governance selects several fiat-backed stablecoins (i.e. USDC, USDT, TUSD), and then uses the volume-weighted average price of that basket on Uniswap to determine the reference price of ETHUSD.

This introduces some trust into the system, as it ultimately relies on the centralized operators of those stablecoins not to collude and manipulate their trading activity *at the same time.*

This shortcut wasn’t available to the original version of MakerDAO because at the time of their launch, DAI was the *only* stablecoin on Ethereum, and Uniswap didn’t exist. It was likewise impractical to use this for the MCD upgrade because a major goal of MCD is to include offchain assets (e.g. real estate) as collateral, and those won’t be trading on Uniswap.

Uniswap v2 is also set to launch with moving-average calculations built-in, making it easier to use it as a price oracle.

## Governance & Interest Rates

In MakerDAO, besides selecting price oracles, the governance also votes on the “stability fee”, the variable interest rate charged to DAI minters in order to target 1 DAI = $1. The general idea is that if 1 DAI < $1, then the stability fee must be increased, making it more expensive for DAI minters, and incentivizing them to redeem their DAI (buying it back if they must) and withdrawing their ETH collateral. Likewise if 1 DAI > $1, the stability fee is decreased to incentivize additional minting. The general cadence of these governance-initiated interest rate updates is roughly once per week.

In MetaCoin, manual intervention in the stability fee adjustment is replaced by an algorithmic PID controller.

From Wikipedia: *A proportional–integral–derivative controller* *(PID)* *is a control loop mechanism employing feedback that is widely used in industrial control systems and a variety of other applications requiring continuously modulated control.*

The PID controller is be implemented as a smart contract that takes the current price of COIN, compares it to the volume-weighted average price of the stablecoin basket (used as a reference point for $1), and automatically updates the interest rate based on the difference. The parameters for a PID controller must be carefully selected for the controller to operate properly. Interestingly the success of MakerDAO over the past several years in maintaining the DAI peg by manually changing the interest rate in response to market dynamics provides the best available data to determine the controller parameters.

To minimize governance, the controller is dumb and parameters is not be able to be updated once launched. This introduces the risk of runaway feedback loops (think [Takoma Narrows](https://www.youtube.com/watch?v=j-zczJXSxnw)) which motivates the need for a way to safely shutdown and exit the system if it is improperly parameterized or externally manipulated.

The controller also requires an onchain price feed for COIN in order to operate. This is different from MakerDAO because the governance uses offchain price inputs (e.g. centralized exchanges) in order to decide on the interest rate updates. As a result, MetaCoin also needs to intrinsically incentivize liquidity of COIN on Uniswap to be the price feed for the controller.

One interesting feature MakerDAO introduced in their MCD upgrade is the “DAI Savings Rate” or DSR, which is also set by their governance. Complimentary to the stability fee, the DSR rewards DAI holders interest simply for holding DAI, and can be adjusted, similar to the stability fee, to incentivize buying and holding DAI. Likewise MetaCoin’s interest rate will operate on both COIN minters and COIN holders symmetrically. If for example a 10% interest rate is being charged to COIN minters to incentivize them to redeem their COIN and withdraw their ETH collateral, the COIN holders earns 10% to incentivize the buying and holding of COIN. Both effects work together to bring the price of COIN back into equilibrium with the $1 reference point and stabilize the peg.

## META Rewards

In MakerDAO, the interest rate charged to DAI minters is used to buy and burn MKR, resulting in value appreciation for MKR holders. More specifically, the DAI earned from the accumulated interest payments is sold for MKR via a smart contract mediated public auction, after which the MKR is burned.

MetaCoin copies this model, but with a few tweaks. As mentioned above, MetaCoin will have symmetric interest rates charged to COIN minters and offered to COIN holders. However, a 10% spread will be charged as a fee. To update the example above, if COIN minters were being charged a 10% interest rate, then COIN holders only receive 9% interest on their COIN, with the other 1% being taken as a fee.

The other tweak is that instead of a public auction, the fee earnings are simply be used to buy META on Uniswap, after which it is still be burned.

## Liquidity Incentives

In order to incentivize COIN/ETH liquidity on Uniswap (so the PID controller can operate properly) MetaCoin could offer:

- Splitting fees between META holders and COIN/ETH liquidity providers instead of all fees going to META holders
- Adding inflation to META and directing it to COIN/ETH liquidity providers
- Accepting shares of the COIN/ETH liquidity pool, alongside ETH, as collateral for minting new COIN

**Splitting fees** - As a simple example, the META holders and COIN/ETH liquidity providers could split the interest rate fees 50/50.

**META inflation** - The Synthetix (SNX) community has seen great success in incentivizing Uniswap liquidity with token inflation rewards, as their sETH/ETH pair is now the most liquid pair on Uniswap. That said, their approach is centralized. For MetaCoin, in order to minimize governance, the META inflation schedule is fixed at launch. A simple example inflation schedule that highly favors early liquidity providers is:

| Year | Inflation |
| --- | --- |
| 0 | 40% |
| 1 | 20% |
| 2 | 10% |
| 3 | 10% (in perpetuity) |

Directing fees and META inflation rewards to liquidity providers could be implemented by having MetaCoin wrap the Uniswap addLiquidity function and forcing liquidity providers who want to earn rewards to provide liquidity on Uniswap through MetaCoin, so it’s easier to track.

**Accepting COIN/ETH LP shares as collateral** - While this doesn’t directly incentivize COIN/ETH liquidity, it enhances the utility of providing COIN/ETH liquidity as a liquidity provider can leverage their liquidity to mint more COIN. Fortunately this likely doesn’t add too much complexity to the system as the same price feeds and liquidation policies work for the COIN/ETH liquidity shares.

The above factors are, in my view, currently the weakest parts of this system. In its early days MakerDAO provided most of their own liquidity for the ETH/DAI pair through Oasis Direct (a simple DEX), earning money from the spread. For any stablecoin liquidity is critical, and far more so for MetaCoin where the Uniswap liquidity is the input used to determine the interest rate. Feedback is appreciated!

## Voting Rights

In MakerDAO, 1 MKR = 1 vote. This voting distribution favors those *profiting* from the system over those *using* it (e.g. DAI minters and DAI holders), but also might be optimal for MakerDAO given the risks their governance can pose if it ends up in the wrong hands.

In MetaCoin, the only things subject to a vote are adding/removing stablecoins from the basket, and shutting down the system. As a result, the voting distribution can be more inclusive of the system’s users. Several parties have voting power:

- COIN minters
- COIN holders
- COIN/ETH liquidity providers
- META holders

These parties have voting power proportional to the value of their exposure to the system. So 1 COIN = 1 vote, and likewise collateralized ETH, liquidity shares, and META each have voting power equal to their value in COIN (where it is assumed 1 COIN = $1). By way of example:

- User A deposits $100 worth of ETH to mint 50 COIN, they have 100 votes
- User A transfers 50 coin to User B, now User A has 50 votes (from their ETH collateral) and User B also has 50 votes (from their COIN)
- User B puts their 50 COIN along with $50 worth of ETH into Uniswap to provide ETH/COIN liquidity, they now have 100 votes (50 more for the $50 of ETH they are exposing to the system)
- User C has $100 worth of META, they have 100 votes

## Happy Endings

The MakerDAO governance can vote to initiate an Emergency Shutdown (also called “Global Settlement”). During an emergency shutdown, DAI holders can be made whole by withdrawing the equivalent value of ETH directly, coming from the DAI minters ETH collateral. The DAI minters can still withdraw their remaining ETH.

MetaCoin does the same. If at any point >33% of the MetaCoin voting power signals to shut down the system, it triggers a “Happy Ending”, and just like in MakerDAO, COIN holders are then able to directly redeem the equivalent value of ETH, with the COIN minters able to withdraw the rest.

*All credit to Peter Pan for coming up with the “Happy Ending” terminology*

## Initial META Distribution

The initial distribution of META tokens will be split 50/50 between Blood and Sweat. Members of MolochDAO and MetaCartel DAO who have bled together in sacrifice to fund ETH-aligned grants will receive 50% of the initial META, based on their share of the total ETH spent on grants. This favors those who have bled the most, instead of basing the distribution on current shares which could have been recently purchased. The rationale for this is my belief that having a strong initial community of ETH-aligned members is be critical for the success of MetaCoin, and in my view there is no stronger metric for alignment than those willing to bleed for a cause.

The other 50% of the initial META will be distributed based on Sweat. The founding team will summon a SweatDAO (a MolochDAO clone), which we will use to assign ourselves shares based on the relative value of our contributions. If fundraising is required, investors will be permitted to offer tribute to SweatDAO to earn shares.

The 50/50 breakdown assumes that the value of Blood and Sweat are roughly equal. MolochDAO and MetaCartel DAO combined have bled roughly $400K in grants, so the assumption is that MetaCoin will take roughly $400K in Sweat to launch. If MetaCoin takes more than $400K to launch, we can adjust the initial META distribution accordingly. For example, if $1.2M of Sweat is required to launch, Blood would receive 25% and Sweat would receive 75% of the initial META distribution.

## Conclusion

MakerDAO has been the most successful project built on Ethereum in its history, and has given rise to the entire $1B+ [#DeFi](https://paper.dropbox.com/?q=%23DeFi) ecosystem. While we should applaud their success and the value it has created for the Ethereum ecosystem, we should keep in mind that *decentralization* is why we prefer it to those other stablecoins backed by banked fiat. When MakerDAO demonstrates a wavering commitment to decentralization, we should explore other, potentially more robust alternatives.

The goal of MetaCoin is not only to create a new stablecoin, but to create a new template from which communities can launch their own stablecoins with minimal overhead. There is no guarantee that the initial conditions of MetaCoin—the PID controller parameters, the inflation schedule, the selected basket of stablecoins, or the initial META distribution—will result in a widely adopted and long-lived stablecoin. But it seems likely that a darwinian exploration of the parameterization space, along with other experiments that this one may inspire, together have a decent chance.

*Let a thousand MetaCoins bloom!*

The key bet for MetaCoin is that social scalability comes from trust-minimization, which in turn comes from eliminating the role of governance in maintaining the system. A future where MetaCoin succeeds is one in which money is considered too important to be left up to human intervention.

If you are interested helping place this bet and build this future, please get in touch. If you have thoughts on this proposed design, please feel free to provide feedback here!

MetaCoin telegram: [Telegram: Join Group Chat](https://t.me/joinchat/Dp-hCVfCrf1zfCP5q2VI9w)

## Replies

**foobazzler** (2020-02-09):

If we’re using centralized stablecoins on uniswap to establish the price of Eth, we’re effectively using a system of oracles and trusting that centralized stablecoin custodians are not engaging in fractional reserve banking. Why not use a system like Chainlink which uses a federated network of oracles? Each oracle has a reputation score and has to stake collateral so that if it reports inaccurate data or experiences a drop in availability it gets slashed. Each oracle can average the price from multiple price aggregators like coinmarketcap which itself aggregates price feeds from multiple exchanges, making collusion difficult.

---

**nikolai** (2020-02-09):

You might be interested to learn that a [PID controller for the interest rate was part of the original specification, under the name “Target Rate Feedback Mechanism”](https://nikolai.fyi/purple/), and that code for this already exists.

You may also be interested in this [simulation of the TRFM demonstrating the basic mechanism](https://steemit.com/makerdao/@kennyrowe/digital-money-a-simulation-of-the-deflation-rate-adjustment-mechanism-of-the-dai-stablecoin) written by Fernando Martinelli et al (who are now working on Balancer Labs, which is a sort of generalized Uniswap).

There are a few nuances related to the “target price” and “target rate” in the papers above. In particular, the original design for Dai did *not* have it pegged to 1 USD or any other asset - this was instead called the “external reference asset” in which the target price was denominated. TRFM adjusts both “target rate” *and* “target price”, which makes the ‘stablecoin’ act more like a dampened index of the basket of collateral assets. A fixed target-price was supposed to be a stopgap measure until the collateral portfolio became diverse enough such that this floating target price would be relatively stable.

---

**ameensol** (2020-02-09):

Thanks Nikolai! Your work is an inspiration for all of this. I’ll check out those links!

---

**ameensol** (2020-02-09):

Is there a system you can point to using Chainlink federated Oracles in production today? If so, how much $$$ does it secure? I’m extremely hesitant to introduce external dependencies that have their own governance as the theme of this design is moving away from that.

Why doesn’t Chainlink build their own stablecoin and use their own oracles?

---

**ricburton** (2020-02-09):

Have a look at their code & their downtime & then be horrified. They are doing their best ![:upside_down_face:](https://ethresear.ch/images/emoji/facebook_messenger/upside_down_face.png?v=14)

---

**fubuloubu** (2020-02-09):

I’ll spare the lecture on establishing [Observability](https://en.m.wikipedia.org/wiki/Observability) and [Controllability](https://en.m.wikipedia.org/wiki/Controllability) of the system, and building a [Robust Controller](https://en.m.wikipedia.org/wiki/Robust_control) that will govern such uncertainty within the system (especially if you’re not allowing tweaking of the PID loop gains), but I will say that it will be important to model this mechanic in order to ultimately get it right and ensure no errant feedback loops are created that affect the stability of the system from the reliance of fiat-backed coins (which I agree might be a good methodology if leveraged well). My main point here is that PID control is liable to be extremely unstable when dealing with something as uncertain as an economic system of this magnitude, but thankfully there are solid areas of research in Control Theory that will be better suited to this type of system.

Tools like cadCAD are being built for this purpose, which are open source modeling tools that can be used to design such a system effectively and collaboratively in the open. What makes this really nice is that we have tons of data available from the Dai system that we can leverage to prove our designs in practice. I applaud this effort, if only it helps reinforce the nature of the problem with Dai, and creates a second stablecoin system that’s maximally censorship-resistant and safe from potential governance risk attack vectors.

Also, let’s build it with Vyper ![:kissing_face_with_smiling_eyes:](https://ethresear.ch/images/emoji/facebook_messenger/kissing_face_with_smiling_eyes.png?v=14)![:ok_hand:](https://ethresear.ch/images/emoji/facebook_messenger/ok_hand.png?v=14)![:heart:](https://ethresear.ch/images/emoji/facebook_messenger/heart.png?v=14)![:snake:](https://ethresear.ch/images/emoji/facebook_messenger/snake.png?v=14)

---

**DCinvestor** (2020-02-09):

A thought on possibly diversifying the initial distribution further might be to offer some shares to people who have donated to Ethereum causes on Gitcoin.

Though I do not know how this could/should be accounted for in the distribution model, and could have implications for how early governance may / may not work.

---

**satosheth** (2020-02-09):

[@ricburton](/u/ricburton) I’m familiar with these and am not horrified. Could you elaborate on what you think the problem is?

[@ameensol](/u/ameensol) Synthetix, Loopring, and Aave are all using Chainlink oracles ATM (see [here](https://eth-usd-aggregator.chain.link/)).

---

**foobazzler** (2020-02-10):

Synthetix is either using Chainlink right now or in the process of integrating it into their system. The problem with introducing externalities is that there is no way around this problem. By using basket of centralized stablecoins on Uniswap as your price feed, you are effectively using the custodians of those stablecoins as your oracle network.

It’s also worth noting that Chainlink is not its own blockchain, the LINK token itself resides on Ethereum but the oracles themselves are independent and run software that communicates with smart contracts on Ethereum. In any case, I’m not trying to shill the project or the token, just pointing that they have a very well thought out system that mitigates the problem as much as possible. I think it’s worth looking into how it works to see if it’s more censorship resistant than simply trusting companies holding dollars in US banks.

---

**BlockchainJames** (2020-02-10):

## META Inflation Rewards

Incentivizing Uniswap pool liquidity is a high priority (especially considering the reliance), but using inflation to this extent initially as the method to achieve this will likely have pretty brutal effects on the META price – Using SNX as the example, there’s still yet to be  **any**  SNX unlocked from the incentivization pool - [this starts in March,](https://blog.synthetix.io/snx-staking-rewards/) note SNX price was $0.05 at that point last year, it’s now $1, my guess is there’s a large number of people who didn’t expect SNX to appreciate so much when they first locked their SNX - As this SNX is unlocked there’s going to be a continuous stream of SNX likely pointed towards the market.

Another thing worth noting here is that SNX [recently announced](https://sips.synthetix.io/sips/sip-23) the smoothing of their inflation schedule - Imo a good call rather than cliffing the inflation.

My take would be rather than a 40,20,10 schedule, simplicity wins and there’s just some consistent inflation given to liquidity providers, or perhaps just a less steep cliff – Mainly just to not flood the market with liquidity provider tokens.  **Assuming some vesting/holding of Blood & Sweat META holders, the majority of tokens entering the market would be from inflation @ 40% in the first year.**

## Liquidity Incentives

- Splitting fees between META holders and COIN/ETH liquidity providers instead of all fees going to META holders

Splitting the 10% spread between DSR & stability fee across the META burn and liquidity provider reward might just end up being such a small piece of the pie it may not be worth. One solution to this would be low inflation goes to liquidity providers & burning META with all fees – At some point of scale, it makes sense that fees scale better than inflation, eventually with 100,000 liquidity providers the inflation is hardly necessary, while the fee still is burning a large value of META.

Adding inflation to META and directing it to COIN/ETH liquidity providers

- Agree inflation is a useful tool – There’s also been a shitload of token projects introduce huge inflation with no real point.

Imo a low inflation, going directly to liquidity providers makes the most sense - (META is being burned consistently through the fee, META is being rewarded constantly for providing liquidity).

## Voting Rights

Multi-weighted governance is fucking interesting – I wonder when looking @ the already low asf MKR voter turnout – If these other groups (COIN minters/holders/liqduity provdiers) would actually increase this – I guess with MetaCoin, votes are only really about pushing a Happy ending, so more voters = more chance of a instant happy ending ococuring.

## Happy Ending

Would it be possible to push ETH rather than redeem? Would make the ending happier lel.

## Initial META Distribution

This is as interesting as fuck. Basically, building a new, functional airdrop - Using ETH bled for a distribution needs a whole article written about it – **InterDAO airdrops incoming.**

Mechanics around Metacoin setup spending & Blood/Sweat distribution is interesting too.

To confirm how the bleed mechanics work (breaking down what I think you mean with “This favors those who have bled the most, instead of basing the distribution on current shares which could have been recently purchased.”)

If I joined MetaCartel DAO with 10 ETH at 1:1 ETH:SHARE and the ETH:SHARE value is now 0.77 – I’ve lost 2.3 ETH, meaning I’m up x% META distribution.

If I had joined Metacartel last week with 10 ETH, when the share value was at 0.77 in the time to now, the share value hasn’t changed, I’ve lost no ETH, I get no META distribution?

Overall, 11/10, MetaCoin Incoming ![:call_me_hand:](https://ethresear.ch/images/emoji/facebook_messenger/call_me_hand.png?v=14)

---

**ChainLinkGod** (2020-02-10):

I am very weary about any DeFi project relying solely on DEXs for price data, as we’ve seen with the [recent Kyber vulnerability,](https://twitter.com/ChainLinkGod/status/1226601239426658304?s=20) it is fairly trivial to manipulate prices in the short term. To mitigate this you could use the volume weighted price as you said, but then you wouldn’t be getting real time price data which can a serious issue when using volatile cryptos as collateral as prices can move very very quickly. This could adversely affect the liquidation process and in the worst case scenario could lead to a system that is undercollateralized.

Using stablecoins as a proxy for USD for price feeds is extremely dangerous. When using DAI/sUSD markets you’re relying on a small group of oracles (smaller than what chainlink [currently offers](https://feeds.chain.link/eth-usd)) and when using USDC/USDT/GUSD/BUSD/TUSD markets you’re relying on a centralized institution. Both kinds of stablecoins can’t guarantee that the peg will hold, and thus it shouldn’t be assumed that’s it’s the same as the USD exchange rate. Even using multiple stablecoins won’t help as many stablecoins suffer from the same systemic issue.

Additionally by relying on just DEXs for price data, you’re not getting a market-wide view of the price/liquidity, only a small subsection that is not nearly as liquid as its centralized counterparts. To get the most accurate price data you need to aggregate from all available exchanges (DEXs and CEXs), and so you will always need an external oracle network when fetching accurate price data. Oracles will end up becoming the attack vector, so they will need to be security-hardened by having the same properties as blockchains: namely decentralization and no single point of failure. Decentralization (of both the oracle nodes and the data sources) assure the reliability and tamper-proofness of the price feed data that ultimately determines the actions a smart contracts makes.

I’m not saying Chainlink is the perfect solution (many improvements are still to come) or solves the oracle problem (not really possible), but their system has proven to be by far the most robust, time-tested decentralized oracle solution that is being used in production today by multiple DeFi projects with zero issues observed.

Also I’m really not sure what [@ricburton](/u/ricburton) means by downtime? I’d like to know more about what you mean by that, I haven’t seen any downtime in oracle networks that are used in production.

---

**ameensol** (2020-02-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/chainlinkgod/48/4484_2.png) ChainLinkGod:

> To get the most accurate price data you need to aggregate from all available exchanges (DEXs and CEXs), and so you will always need an external oracle network when fetching accurate price data.

I think not having *the most* accurate pricing data is sort of OK. We would be consciously making the trade off to not have price oracles in the design and instead favor the DEX provided volume weighted average of the selected fiat-backed stablecoins. Uniswap v2 will have moving-averages built-in.

Maybe someone else can fork MetaCoin and build a stablecoin that uses ChainLink oracles, and we can see how the market expresses its preference.

---

**haydenadams** (2020-02-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/ameensol/48/1455_2.png) ameensol:

> the volume-weighted average price of the stablecoin basket on Uniswap as the price oracle

Uniswap V2 oracles are generally designed around time weighting (TWAP) not volume weighting (VWAP) so might need to rework this a bit.

Also, manipulation resistance scales with both liquidity and the time over which you are averaging across - so worth discussing the amount of recency needed here.

Overall I’m a huge fan of maximizing automation + minimizing governance approach so happy to discuss Uniswap oracles anytime

---

**foobazzler** (2020-02-10):

Keep in mind that centralized stablecoins can be frozen at any time, regardless of whether they’re being used in a trustless decentralized exchange or not. If your oracle system depends on the exchange of these permissioned ERC20s, then MetaCoin is not maximally trustless. That’s more of an issue than price accuracy imo, especially as it increases in marketcap and draws more scrutiny from governments.

---

**haydenadams** (2020-02-10):

Also it doesn’t have moving averages built directly in, it stores additional data that makes external moving averages significantly better / more reliable / more efficient / more manipulation resistant.

---

**ChainLinkGod** (2020-02-10):

To add onto that, if you decided to mitigate this issue by only using permissionless stablecoins for your price data then you would be relying on basically just the ETH-DAI pair, and at that point Metacoin wouldn’t be any more resilient than DAI itself

---

**ameensol** (2020-02-10):

Jeez you Link shills don’t give up. Go build your own stablecoin using ChainLink ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12).

![](https://ethresear.ch/user_avatar/ethresear.ch/foobazzler/48/4478_2.png) foobazzler:

> Keep in mind that centralized stablecoins can be frozen at any time, regardless of whether they’re being used in a trustless decentralized exchange or not. If your oracle system depends on the exchange of these permissioned ERC20s, then MetaCoin is not maximally trustless.

This is OK. The bet is that they all won’t blow up at the same time, and if they do, that the governance can trigger a happy ending.

---

**ameensol** (2020-02-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/haydenadams/48/944_2.png) haydenadams:

> Uniswap V2 oracles are generally designed around time weighting (TWAP) not volume weighting (VWAP) so might need to rework this a bit.

So is it impossible to get volume-weighted averages? Am I shit-out-of-luck here?

---

**haydenadams** (2020-02-10):

Maybe? I think you can make a pretty good oracle from a basket of stablecoins on V2 using TWAPs

Is there a reason it needs to be volume weighted and not time weighted?

---

**foobazzler** (2020-02-10):

I think the idea is to give more importance to stablecoins that have more volume vs. ones that have lower volume and are easier to manipulate price-wise


*(18 more replies not shown)*

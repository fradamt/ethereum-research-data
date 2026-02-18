---
source: magicians
topic_id: 23357
title: Addressing Ethereum value capture
author: jdetychey
date: "2025-04-02"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/addressing-ethereum-value-capture/23357
views: 1723
likes: 27
posts_count: 18
---

# Addressing Ethereum value capture

*Authors [edit 3rd Apr]: Jerome de Tychey, Dean Eigenmann, Zak Cole*

### Abstract

Temporary enforcement of a minimum max priority for Type 3 transactions (Blobs) by the validators.

Increase research effort to rapidly change the blob pricing mechanism to dynamically adjust upward when L1 gas is low and vice versa.

### Motivation

The Ethereum ecosystem has undergone a fundamental shift in transaction dynamics. As the majority of user activity migrates to L2s, these L2s are now responsible for extracting substantial fees from Ethereum their users, while contributing relatively little back to the Ethereum protocol economically. In many cases, L2s pay less than a dollar in Blob transactions. This discrepancy highlights a growing misalignment between where economic activity is secured and where revenue is captured. Ethereum’s current revenue model, largely dependent on direct user transactions on L1, no longer reflects the dominant usage patterns of the network. To ensure long-term sustainability and alignment, Ethereum must reconsider and evolve its revenue mechanisms to account for this L2-centric activity with L1-security reality.

The upcoming Pectra fork adds [EIP-7691](https://ethereum-magicians.org/t/eip-7691-blob-throughput-increase/19694) (Blob throughput increase) which will double the number of Blobs per block. This will likely reduce further the DA cost of L2 solutions and accelerate the shift in transaction dynamics.

The following proposal acknowledges those challenges. It aims at maximising the security of Ethereum while keeping it decentralized and nudging rollups towards more Ethereum alignment. This proposal is meant to be both voluntarily enforced and temporary until rollups gain in maturity and blob pricing evolves. We note that research discussions have recently started on native rollups with higher alignment with Ethereum, as well as on the blob fees predictability (see [EIP-7762](https://eips.ethereum.org/EIPS/eip-7762) and [EIP-7918](https://ethereum-magicians.org/t/eip-7918-blob-base-fee-bounded-by-execution-cost/23271)).

### Specification

Ethereum stakers voluntarily enforce a minimum priority fee for Type 3 transactions (Blobs).

Research teams accelerate the ongoing work on dynamic blob gas pricing to target a minimum L1 gas + tip spent (if L1 gas is low, tip is high and vice versa).

### Priority fee target computation

Assuming a daily blob gas use of 2.8Bn Gas and a minimum max priority fee **5 Gwei**, this proposal would generate 14 ETH daily for the validators (or 5110 ETH yearly ~$10.2M with ETH at $2k).

A “25% Tax” on current L2 onchain revenue could be computed as such: $200M of rollup onchain revenue, 25% is $50M, assuming daily blob gas used of 2.8Bn Gas and ETH at $2k, the minimum max priority fee would be **24.5 Gwei**, generating 68.62 ETH daily for the validators (25049 ETH yearly).

Assuming a total current daily validator income of 2639 ETH:

- a 5 Gwei fee would bring the validator daily income to 2653 ETH, ie a 0.53% increase on total daily validator income
- a 24.5 Gwei fee would bring the validator daily income to 2706 ETH, ie a 2.6% increase on total daily validator income

## Replies

**Amxx** (2025-04-02):

Correct me if I’m wrong, but the priority fee is paid “per gas used in the transaction”.

So if a type 3 transaction submits a blob, but does little to no computation with it (just storing it for future use), that priority fee would apply over a “small” gas limit. In the end it wouldn’t count for a lot of value, would it ?

Its like taxing the gas that is in the tank of cars that go out of the dealership to compensate for the car price being to low.

---

**jdetychey** (2025-04-02):

The proposal target specifically Type 3 transactions. In terms of order of magnitude, a blob is roughly 131k gas.

Let’s take this transaction for reference:

https://etherscan.io/tx/0x7146f641416c0dbb9e11a7822239680a5a94a0cbaaff5efe2a4f60ccd58cca77

**Gas Limit:** 6,000,000 versus 285,903 (4.77%) actually used… looks like the Batcher didn’t really estimate how much Gas it was actually going to consume and picked 6M just to be sure but I digress.

**Gas Fees:** Base: 0.398569438 Gwei actual gas price paid, while the Batcher proposed a Max of 2.830865104 Gwei ; additional gas fees, Max Priority: 2 Gwei

Via this transaction, the Validator that proposed this block has:

- Burnt 0.000113952198032514 ETH ($0.22) , i.e 285,903 Gas * 0.398569438 Gwei)
- made an extra tip of 0.000571806 ETH ($1) i.e 285,903 Gas * 2 Gwei

Blobscan gives a breakdown of how effective Blobs are vs calldata for a particular transaction:

https://blobscan.com/tx/0x7146f641416c0dbb9e11a7822239680a5a94a0cbaaff5efe2a4f60ccd58cca77

This specific transaction was x304.49 cheaper than without Blobs. The proposal of having the validator as a minimum tip of 25 Gwei would have made the following change to this transaction:

The Validator that proposed this block would have:

- Burnt 0.000113952198032514 ETH ($0.22) , i.e 285,903 Gas * 0.398569438 Gwei)
- made an extra tip of 0.007147575 ETH ($13) i.e 285,903 Gas * 25 Gwei

This specific transaction would have been x28 cheaper than without Blobs yet the revenue for the validator would have been 10,83 times higher.

---

**TimDaub** (2025-04-03):

Having spoken to a bunch of people and having read a lot of the Ethereum Mag and Ethresearch posts, I don‘t think the lack of a better pricing method is the issue. Isn‘t the issue that DA is fundamentally oversupplied, without any limit on supply in the future other than bandwidth?

At peak Ethereum PoW, you couldn‘t build another Ethereum because there were simply no more GPUs in the world. If we find the decentralization limits of DA, then congestion pricing will kick in.

That said, you can ofc always fork and rebrand Celestia to start again from zero in terms of bandwidth. And another issue is that Ethereum researchers keep resolving bottlenecks

---

**jdetychey** (2025-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> Isn‘t the issue that DA is fundamentally oversupplied, without any limit on supply in the future other than bandwidth?

Supplying a lot of Blobs has been a deliberate choice to support the L2 scaling roadmap. The upcoming fork Pectra introduces EIP-7691 which will x1.5 the number of blobs per block.

Research discussions are ongoing on blob fees but will take years to be included if ever (see [EIP-7762](https://eips.ethereum.org/EIPS/eip-7762) and [EIP-7918](https://ethereum-magicians.org/t/eip-7918-blob-base-fee-bounded-by-execution-cost/23271)).

This proposal argues for a voluntary contribution (a tip) as an acknowledgement that something may be wrong in the way Blobs are priced. It sends a strong signals to the community:

- The protocol economics debate is taken seriously
- In protocol changes re blobs are expected and will be welcome
- Meanwhile, tipping blobs will support ETH staking

---

**TimDaub** (2025-04-03):

OK, I see the good faith in your proposal, but for me the question is what the ETH researchers know that others don’t about blob scaling. E.g. why is it that among ETH researchers there is consensus that blobs have to be scaled, and at the same time we price blobs based on congestion pricing? These are conflicting goals obviously, so why is everything peaceful?

To me its unclear what should be done because e.g. if we had conviction that the L2 execution is going to eventually drive up L1 gas costs, then I could see myself agreeing to scaling blobs as fast as possible. Because then DA is anyways never going to be valuable (at least at its currently level of integration).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jdetychey/48/66_2.png) jdetychey:

> Authors: Jerome de Tychey, Dean Eigenmann

Btw what’s the conflict of interest that you have? Isn’t Dean pretty tightly associated with Celestia? Why would you and him have good faith proposals for Ethereum? My understanding is that Celestia is in pretty bad competition with Ethereum DA

---

**jdetychey** (2025-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> the question is what the ETH researchers know that others don’t about blob scaling

ETH researchers are aware of the price discovery problem, let me quote the **Motivation** of EIP-7762:

> When scoping 4844, the thinking was that blobs would only enter price discovery once, relatively quickly after the blob rollout; however, this has not been the case. In fact, blobs have entered price discovery several times, and the frequency of price discovery events is likely to increase in the short term as we approach saturation of capacity. Moreover, the roadmap calls for further increases in blob capacity in subsequent hardforks, which may lead to price discovery events happening around those changes in the future.
>
>
> Increasing the MIN_BASE_FEE_PER_BLOB_GAS will speed up price discovery on blob space.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> These are conflicting goals obviously, so why is everything peaceful?

It’s far from peaceful in my opinion. Many community members and analysts voiced their concerns regarding the consequences for Ethereum (its model, its security,its network effect, its native asset) of having a vast portion of the network activity so rapidly move to Rollups.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> Btw what’s the conflict of interest that you have? Isn’t Dean pretty tightly associated with Celestia? Why would you and him have good faith proposals for Ethereum? My understanding is that Celestia is in pretty bad competition with Ethereum DA

I can’t speak for Dean here, he has been doing good work for a while [see his website](https://dean.eigenmann.me/). Let’s not go witch hunting on who and what support DA, remember that key individuals at the EF were advisors to Eigen Layer until Nov 24. Regarding me, I don’t have any DA tokens, I’ve been mining ETH before PoS and solo staking since the beacon chain genesis block ([you should solo stake too!](https://youtu.be/w3dZMvSOYzg?si=ecPObkAUFAaOkDeZ)). I run non-profits like Ethereum-France and EthCC. My company is a MiCA custodian focussing solely on EVM. I have dedicated the last 10 years to Ethereum and will undoubtedly do so for at least the 10 years to come.

---

**decanus** (2025-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> Btw what’s the conflict of interest that you have? Isn’t Dean pretty tightly associated with Celestia? Why would you and him have good faith proposals for Ethereum? My understanding is that Celestia is in pretty bad competition with Ethereum DA

I have investments in both Ethereum and Celestia, my Ethereum far outweighs my Celestia holdings. I have been contributing to Ethereum since 2017…

---

**TimDaub** (2025-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jdetychey/48/66_2.png) jdetychey:

> It’s far from peaceful in my opinion.

What is confusing to me is why everyone still keeps going forward with e.g. EIP 7762 etc..

I have commented elsewhere that to me it isn’t obvious that EIP 7762 fixes the fee accrual entirely: [A simple L2 security and finalization roadmap - #6 by TimDaub](https://ethereum-magicians.org/t/a-simple-l2-security-and-finalization-roadmap/23309/6) IMO EIP 7762 just fixes **a** problem with fee accural, but it’s entirely not holistic enough to fix it completely. Unless ofc, the authors of EIP 7762 have ran the math and concluded that it does, but didn’t publish it, or I’m missing smth.

Where is the math that shows that with EIP 7762 we get back to e.g. at least 2B USD fees accrued in 2025?

IMO the elephant in the room is that we have had between 2B and 9B USD in fees for Ethereum stakers/miners, and now that seems to be far out because with DA, transacting on Ethereum is just so much cheaper but same security. What’s the argument against ETH going to 200 USD because it has become 10x cheaper to transact? That we’ll grow 10x?

OK, but where is the user growth? Grow the pie shows that active addresses stagnate

[![Screenshot 2025-04-03 at 11.35.16](https://ethereum-magicians.org/uploads/default/optimized/2X/d/d039192cdce184872c33dbf03ad64bade6d2729f_2_690x498.jpeg)Screenshot 2025-04-03 at 11.35.161920×1388 139 KB](https://ethereum-magicians.org/uploads/default/d039192cdce184872c33dbf03ad64bade6d2729f)

Tbh I’m actually open to the idea that we’ll go to 200 USD an ETH. But I’ve been too fearful to reallocate any of my positions yet.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jdetychey/48/66_2.png) jdetychey:

> Many community members and analysts voiced their concerns regarding the consequences for Ethereum (its model, its security,its network effect, its native asset) of having a vast portion of the network activity so rapidly move to Rollups.

Idk. I’m not on X or FC, but here on the Magicians and on Ethresearch I don’t see a lot of debate happening tbh. When you e.g. look around, it is generally assumed that we should just blindly increase the blob limit. You can see that even in [Vitalik’s post](https://ethereum-magicians.org/t/a-simple-l2-security-and-finalization-roadmap/23309) itself. He doesn’t motivate the blob limit increase until I asked.

I also don’t see anyone deeply criticizing the strategy, e.g. that congestion pricing plus a research effort to reduce congestion produces no fee accrual practically. That’s literally why I started to be active here again.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jdetychey/48/66_2.png) jdetychey:

> Let’s not go witch hunting

Not witch hunting. Just asking a normal question so that both of you state your positions, which you now did so I’m happy.

---

**jdetychey** (2025-04-03):

There’s a lot to unpack here, I’ll do my best to keep it organised.

I do not want to start discussing the specific merits of EIP-7762 and 7918. Those EIPs are motivated by improving the blob fee market and I expect other approach to proposed in the short term. The EIP process is, by construction and for good reasons, a slow process.

IMHO the reason why you didn’t read much of the criticisms of the shift in transaction dynamics in this forum is because not many people really cared enough or dared enough to chime in here where the discussion format is oriented towards development, where invested researchers and community members intervene, and where price/value/economics are at first glance suspicious (see your reaction “what’s your conflict of interest here?”). Yet, Ethereum faces several core challenges:

1. No matter the gasprice, mainnet will always be more expensive than the average rollup and new activity is more likely to happen there first;
2. Rollups are deriving their security from the mainnet which itself derives its security from the value of ETH at stake;
3. Discrepancy between the cost of security for the rollups and its transactional value extraction will damage the neutrality of the Ethereum network as rollups will progressively capture the staking activity.

There is no simple and single answer to those challenges but we have world class researchers and engineers working on it.

I remember very well how the narrative on how Ethereum was paying its miners too much for the security and why we needed to switch to PoS. I think we were lucky back the days to have adopted the difficulty bomb to nudge everyone into making this decision. The following burning question must now be asked to the Rollups now, are the rollups paying too few for their security?

We collectively agreed that Rollup scaling was the right approach, in a sense it was also the initial execution sharding approach but sequenced differently. As the process unfold, many questions arise. I highly recommend Martin Koeppelmann talk “[Ethereum needs native L2 by koeppelmann at last Devcon](https://www.youtube.com/watch?v=BWsz_ulng6Y)”.

Regarding your comment on activity slowing down, I don’t think it’s true. From my experience, adoption happens in waves and the trend is still very positive. Nevertheless, one of my (likely controversial here) opinion regarding activity on a blockchain: *positive price action is an extremely efficient catalyzer of activity and user acquisition, vice-versa for negative price action*. Whether you share or not this opinion, positive price action is good for Ethereum security. For those reasons, when it comes to technical decisions, I’m always a proponent of being careful with price potential price impact.

User activity of rollups is more than 18 times the user activity of ethereum ([source](https://l2beat.com/scaling/activity)). Yet, only Arbitrum is a Stage 1 rollup in the top 15 Rollups by TVL ([source](https://l2beat.com/scaling/summary)). Except for Arbitrum, users have no exit window in case of an unwanted upgrade. In case of proposer failure, withdrawals for most of rollups, are not processable until the proposer is back online. In time of sequencer failure, in most cases users have to wait for the sequencer to come back up. In some cases the users may self sequence after up to 12 hours. Moving transactions off mainnet and only posting summary data to Ethereum have allowed for crucial scaling of the network capacity at the cost of heavy compromises on the finality and censorship resistance of upper layer transactions. It would be an understatement to say that decentralized scaling is very challenging and that rollup technologies are constantly progressing. **Nevertheless, the compromises made are also heavily impacting the economics of mainnet and are damaging its capacity to withstand attacks, failures, and external pressures.**

Dencun largely reduced the cost of Data-Availability for Rollups. Since 2024, rollups made more than $206M in onchain profit (measured as L2 Transaction Fees Earned minus L1 Calldata, Blob and Verification Costs, [source](https://dune.com/niftytable/rollup-economics)). This onchain profit resulted both in less revenue for ETH stakers and less ETH burnt. This trend is ongoing and has consequences on the desirability to stake ETH which we assume is motivated on the financial spectrum by expectation of ETH to hold its value (in regards to the opportunity cost of having ETH at stake rather than immediately available the execution layer) and by expectation of cost effective staking rewards. The total supply of ETH at the time of the Merge was ~120,5M units. Dencun marked the stop of the post Merge “ultrasound” phase. Since February 7th 2025, the total supply of ETH has been growing above its level at the Merge. **The validator count (ETH at stake) reached a top on Nov. 7th 2024**, this is one of the most worrisome signal in my opinion.

L2 tipping more for blobs is a straightforward and simple starting point.

### To sum up:

Activity growth is primordial, health of the network is crucial. L2s are collecting much more fees than they are paying to anchor on the L1. There’s nothing wrong with that, until the number of validators is decreasing and complex value capture debate starts. Protocol changes will be long, actively lobbied and uncertain.

This proposal suggests that the L2s tip a little more for blobs. This does absolutely not have to hurt the cost of transacting on the L2s at the current level of onchain profit. More importantly for Ethereum, adoption of this tip sends a strong signals:

-The protocol economics debate is taken seriously by the L2 and the validators

-Staking and holding ETH will be more desirable (the tip improve staking yield)

-In protocol changes regarding blobs are expected and will be welcome by everyone

**This proposal doesn’t require any protocol change.**

---

**catwith1hat** (2025-04-08):

[@jdetychey](/u/jdetychey) Thanks for your proposal! I agree with your premise and your conclusion. I have a few thoughts to add.

**Irrational validators**

Let me argue from a different perspective why this proposal makes sense. Validators are selling two types of block space: regular transaction space (Type 1/Type 2) and blob transaction space (Type 3). Selling blob space clearly has an impact on the fee revenue of the regular space as users move to their Type 1/2 TXs to L2s and into Type 3 TX. That’s akin to a producer of a premium brand item to also produce a discount item at the same type. Type 3 supply destroys Type 1/2 demand.

From monopolistic pricing point of view, it is irrational for validators to sell any blob space unless the incremental revenue from that sale is making up for the fee loss in the regular tx bucket. I haven’t done the exact math here, but I would think that a much higher minimum fee is required than 5/24.5 Gwei. IIRC MEV was around 30% of L1 validator income pre Deneb, which would point to a fee of around ~250 Gwei as the rational minimum.

**Building the infrastructure**

- Most blocks are built by block builders and validators pick them blindly via relays.
- Validators have little control over how the block is built. At best, validator can choose between two relay endpoint flavors, max-revenue or OFAC-enforcing. That’s a 1-bit selection.
- We need to build out a general way for validators to signal their block building parameters. We could probably piggy back some information on the register_validator calls that mev-boost periodically submits to relays.
- Once we have built out the above, a validator could signal a min_blob_fee during the relay registration. The relay remembers that and the block builder can query those parameters from the relay for the upcoming slot, so that they can submit valid blocks.
- Relays rely on their reputation for their business. If they offer a block for blind signing and then the block is outside of the spec set by the validator (or the relay fails to broadcast the block), validators switch to another relay.

**Subsidizing based rollups**

Once the builder/relay infrastructure can build blocks towards some per-slot specification, I would want more parameters. E.g. I would like to fully exempt based rollups from the minimum tip regime.

**Tip vs Burn**

If we could design a method, in which we don’t collect more fees to the benefit to the validator (tip) but collect more fees to burn, I would prefer such a design. To me the ultrasound money meme is much more important than increasing my income by 10%. However to get to ultrasound levels, we need to burn around 2300 ETH per day. Would rollups pay that? Well they did before… Would it be okay for validators to collect that for their personal gain as tips? Probably not, because that’s a wealth transfer not a burn.

So if we want to force a higher burn, we need another mechanism than tips. Maybe we could make Type 3 tx sender a smart contract that for each Type 3 tx, it sends, somebody could force the smart contract to burn ETH in a followup Type 1 TX (burn=send ETH to 0x00…00). However that type of Type 3 transaction censorship is much more difficult than just checking a minimum tip attribute on the TX data.

---

**edhemphill** (2025-04-09):

As a long time holder, former miner of ETH, and non-ETH but seasoned cloud developer and startup founder, seeing this thread is very encouraging and enlightening. It’s a discussion I would love to see more of.

I would like to very directly mention the elephant in the room here - competition and recent price collapse…  At the core of it - Ethereum needs to attract developers who are building new L2s or tokenized applications.  This means we - as a community - are also in the business of marketing.  Solana and XRP are chasing ETH in market cap.  If the current trend line of BTC to ETH price holds, it is very possible, perhaps I should say *likely* that XRP will surpass ETH in market cap.  The significance of this should not be dismissed. When this happens, in every chart, in every list, ETH will no longer be next to BTC.  In many places ETH will simply no longer be mentioned. It will make marketing to developers much more difficult. Key reasons:

- Exposure. Marketing is a game of positive and negative spirals. ETH losing its pole position is going to kick off a negative spiral of news, lost interest, influencers, etc. It will essentially say the market has no confidence in ETH.
- Justification. Even if Ethereum’s technology and dynamics far surpass its rivals (speed, security, decentralization, etc.) - developers must justify their technical choices to product managers, CTOs and VPs. People who view things much more in the abstract. People who want a single slide to summarize anything technical and deal in spreadsheets with basic math. The best technologies don’t win. The best marketed technologies win. Sad fact but a fact. It’s easy to defend a decision when you are picking a market leader. Leaders - in the layman’s mind - are the tokens at the very top of the list.

The absolute most important thing this community can do is to prevent this market cap flip from happening. This probably does not require sudden, massive fees being leveled on L2s, or  an immediate, large “wealth transfer” occurring for stakers. But it does require some kind of action for the market to realize that ETH is serious, very serious, about justifying its network value.

Markets are discounting mechanisms driven by sentiment.  In the view of the market trend line’s slope (ETH in BTC terms), Ethereum simply does not care about its native asset value or any wealth generation for that matter. Unfortunately, if ETH’s market cap falls below its rivals, it will be taken less seriously as a technology.  At least by anyone who makes the final decisions about which blockchain to use at a well funded organization.  It will greatly increase the hurdles required for ETH to maintain its dominance as the leading smart contract block chain.

Of course there is a balance here. As is mentioned in various places on this forum, high fees would discourage developers and decision makers also. But there is balance…  The network must justify its price.

This is an urgent and timely matter.  If the flip happens, it may never flip back.  This could create a negative spiral of events which could be unsurmountable in the future - an outcome which could not be coded out of or fixed later with fee changes.

I my view - any value capture related proposal should be significant enough that it sends a clear message to the market that the game has changed: ETH is going to capture more value and defend its network price. It can’t simply be slowly deflationary. *Deflation of an asset perceived as worthless, or even trending down, means little for price discovery.*

It must somehow reward stakers enough, or promise future rewards, that justify the native asset value.  Shooting from the hip here - I’d say we need a staking reward that earns an effective rate at least a few basis points better than the US 10-year. A proposal which adjusted fees, even at a future time, based on a formula pegged to a well known fixed income rate would probably buy time for ETH and get us through this market cycle.

---

**InnaJavelina** (2025-04-09):

The price and developer activity declines are certainly a serious issue for Ethereum (although 1 month dev decline worse for Solana). Peak commits roughly coincide with release of ChatGPT.

I don’t think that this qualifies as an “elephant in the room” though. Price activity, competing chains are widely discussed. For sure you are right that devs need more incentives and if SOL or XRP flips ETH, it would be bad marketing. More coordinated entities seem better at incentives and messaging.

A more fundamental elephant in the room for a dev investing their time or an investor their money in ETH must be: **what’s the point**? Price signals value to both and you can buy ETH today for about the same price as you could on 13 Jan 2018, more than 7 years ago. What useful end-user products have been launched during this time? Judging from flatline unique address growth, not much. New tech typically displaces an inefficient model, attacks higher margins and results in exponential user growth, from the phone to internet adoption graphs. Blockchain use doesn’t even measure up to the rate of adoption of flush toilets.

The market cap of the 3 tokens you mention is about half of the size of the Belgian bond market. If their rank was to be re-ordered or BE bond prices change, a pretty small part of the world’s population would care (outside of Belgium).

I think that most serious devs and long-term investors want to be part of something meaningful, that brings value to the world (and themselves). Crypto’s constant boom-bust fads, from dentacoin to pump.fun, don’t add much utility to real-world consumers.

Imagine you’re a super-talented developer; you contribute to Ethereum, one of the most innovative computer architectures of all time; and then you help build an app on it, where people can exchange tokens quickly, permissionlessly and at low cost, which is an incredible accomplishment. Then, what is the user offered? Buy a speculative NFT or meme coin that essentially pumps and dumps based on insider cabals, designed to relieve greed-driven speculators of their money under the altruistic cover of “re-inventing finance”. It gets pretty soul-destroying after a while.

The main thing that has achieved product market fit in this time seems to be stablecoins (a “peer-to-peer version of electronic cash”). Maybe the coin that pivoted to “digital gold” (with 5x gold’s vol). Not much else. It is pretty crazy that we live in a world where an amazing invention like Uniswap has approximately the same value as PEPE.

Let’s hope that this current bear market causes crypto devs and investors to get out of their little bubble and answer some existential, elephant-size questions, like: what are we doing here? Maybe we should stop producing science experiments and scams and start thinking more like Steve Jobs: what products do users need (even if they don’t know it yet)?

---

**Inna_Everstake** (2025-04-09):

Really appreciate this proposal for thoughtfully highlighting one of the challenges Ethereum is facing today. It smartly recognizes and addresses a growing economic disconnect in Ethereum’s evolving architecture.

This misalignment between where the activity happens and where the economic incentives lie poses a substantial risk to Ethereum’s long-term sustainability. The introduction of a temporary, voluntarily enforced a minimum max priority for Type 3 transactions could be a reasonable step. It sends a signal that alignment with Ethereum’s economic security layer must evolve in tandem with technical scaling.

What is particularly thoughtful about this proposal is its temporary and voluntary nature. It’s not an overbearing top-down mandate, but rather a collective effort to raise awareness and align Ethereum’s incentives in a way that supports its long-term success.

The proposed mechanism could be the beginning of a more cohesive, symbiotic relationship between L1 and L2, one that strengthens Ethereum’s security, decentralization, and financial model.

---

**edhemphill** (2025-04-10):

Good commentary. Stablecoins are one of the few, non casino-like, legitimate uses in L2s. It’s unfortunate the bull market - at least so far - has had the oxygen sucked out of it by irrational speculation in meme coins.  Ripple’s move into stable coins represents a serious threat to ETH dominance. I certainly hope that Ethereum can win the ECB on the digital euro project. The ETH community needs an organized, funded effort for marketing and deal winning. I can assure you that Ripple and Solana Labs are actively purusing the ECB project also.

---

**jdetychey** (2025-04-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/catwith1hat/48/15226_2.png) catwith1hat:

> To me the ultrasound money meme is much more important than increasing my income by 10%

Amen to that, couldn’t agree more.

---

**montana64** (2025-04-23):

Ethereum and they are looking forward to the future

---

**jdetychey** (2025-05-06):

Couple of interesting resources for context:

**Blobs dune analytics charts by Hildobby**

https://dune.com/hildobby/blobs

[![Screenshot from 2025-05-06 15-46-44](https://ethereum-magicians.org/uploads/default/optimized/2X/4/4bbac387f055012cecc08683be7bafda0b97fdc2_2_690x357.png)Screenshot from 2025-05-06 15-46-44778×403 49.8 KB](https://ethereum-magicians.org/uploads/default/4bbac387f055012cecc08683be7bafda0b97fdc2)

The blobs posted are almost never hitting the target. Above this target the pricing of blobs would send the price of blobs up exponentially. There is little doubt that blob submitters are arbitraging this target due to the strong financial incentive to do so. Switching to calldata is an acceptable strategy when the target is near.

See notably this twitter thread: https://x.com/hildobby_/status/1918272213377228940

**A long thread on the Blob Base Fees by [tripoli](https://ethresear.ch/u/tripoli)**


      ![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 25 Sep 24](https://ethresear.ch/t/understanding-minimum-blob-base-fees/20489)



    ![image](https://ethresear.ch/uploads/default/optimized/3X/5/e/5ed1c53aac66015377915a554d424c352fbeab0e_2_1024x501.png)



###





          Layer 2






Understanding Minimum Blob Base Fees  by Data Always - Flashbots Research  Special thanks to Quintus, Sarah, Christoph, and Potuz for review and discussions.  tl;dr  The myth that blobs pay zero transaction fees is false. Depending on type of data...



    Reading time: 5 mins 🕑
      Likes: 37 ❤











And the initial cold start problem described here:

https://ethresear.ch/t/eip-4844-fee-market-analysis/15078


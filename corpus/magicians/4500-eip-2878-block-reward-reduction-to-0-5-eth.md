---
source: magicians
topic_id: 4500
title: "EIP-2878: Block Reward Reduction to 0.5 ETH"
author: JLilic
date: "2020-08-14"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-2878-block-reward-reduction-to-0-5-eth/4500
views: 18525
likes: 80
posts_count: 46
---

# EIP-2878: Block Reward Reduction to 0.5 ETH

Discussion thread for EIP-2878 https://github.com/ethereum/EIPs/pull/2878

## Replies

**jdetychey** (2020-08-15):

---

## title: 2020 Block Reward Reduction to 0.5 ETH
authors: John Lilic   , Jerome de Tychey  ,  Others
discussions-to:
status: Draft
type: Standards Track
category Core
created: 2020-08-11

## Simple Summary

This EIP will reduce the block reward paid to proof-of-work validators.  Reducing the block reward will maintain the status quo of periodic community-activated block reward reductions.

## Abstract

Of the top 4 Proof-of-Work blockchains, Ethereum pays the highest inflation rate for block validation.  Blockchains both larger, and smaller than Ethereum pay lower rates without any adverse effects.  Over-paying for block validators is an inefficiency that negatively affects all ETH holders, as it unnecessarily inflates the montary base and reduces the purchasing power of all Ether holders.   This EIP will reduce the block reward to bring inflation in-line with Bitcoin, which is the largest cryptocurrency by market cap.   Block rewards will thus be adjusted to a base of 0.5ETH, uncle and nephew rewards will be adjusted accordingly.

## Motivation

A block reward that is too high is inefficient and negatively impacts the ecosystem economically. There is prior precedent for reducing the block reward; it has been done twice in the past in tandem with the diffusion of prior difficulty bombs.  The most recent diffusion, Muir Glacier, did not include a block reward reduction and thus broke the prior status-quo.  This EIP will revive the previous status-quo of periodical block reward reductions based on economic conditions.   With the upcoming release of ETH2.0 Phase 0 staking, inflationary pressures on Ethereum will be further increased.  Reducing the block reward prior to ETH2.0 Phase 0 staking will assist in alleviating negative inflationary effects.

## Specification

Parameters in the source code that define the block reward will be adjusted accordingly.

## Rationale

We determine the target block reward by first comparing the Bitcoin inflation rate:

At the Bitcoin Halving there were 18,375,000 Bitcoins in circulation.   There are 328,500 new bitcoins mined each year (6.25 BTC/Day * 144 Blocks per day * 365 Days in a year).  The annual inflation rate for Bitcoin is is thus  1.78%. (328,500 / 18,375,000 * 100)

At the time of writing, there were 110,875,500 Ether in circulation.  There are 4,982,250 Ether mined each year (13,650 ETH/Day * 365 Days in a year).  The annual inflation rate for Ethereum is thus 4.49%.  (4,982,250 / 110,875,500 * 100). (See https://etherscan.io/chart/blockreward for the approximate daily Ether reward)

The result of this comparison shows that Ethereum is currently paying a 2.52x higher block reward than Bitcoin.

To further illustrate the point, if the ETH/BTC ratio increases to 0.041, all else equal, Ethereum will be paying a higher reward in $USD than bitcoin, despite being 3 times smaller in Market Capitalization.

Sometime after November 2020, the Ethereum 2.0 Phase 0 chain will launch.  This chain will further add to the inflation rate of Ethereum, as it will generate staking rewards for all users that stake a deposit and validate blocks on the chain.

The annual issuance from staking rewards is planned to be equal to 181 * SQRT(total ETH staked).  A chart below illustrates some possible values.

| ETH validating | Max annual issuance | Max annual network inflation % | Max annual reward rate (for validators) |
| --- | --- | --- | --- |
| 1,000,000 | 181,019 | 0.17% | 18.10% |
| 3,000,000 | 313,534 | 0.30% | 10.45% |
| 10,000,000 | 572,433 | 0.54% | 5.72% |
| 30,000,000 | 991,483 | 0.94% | 3.30% |
| 100,000,000 | 1,810,193 | 1.71% | 1.81% |

It it highly unlikely that 100,000,000 ETH will stake on the beacon chain.  So we will use the lower number of 10M for our estimations.

At this rate, the ETH inflation rate will increase to  5,554,683 ETH/yr. (4,982,250+572,433 =5,554,683). This yields an annual inflation rate of  ~ 5.00% (5,554,683/110,875,500 * 100). At this rate, Ethereum’s inflation will be 2.81x (5.00/1.78) higher than bitcoin.

In order to calculate the block subsidy required to achieve inflation parity with Bitcoin, we must first back out our estimations for ETH2.0 issuance in order to determine the maximum annual POW reward.

1,973,583.9 - 572,433 = 1,401,150.9 Max Annual PoW Rewards.

Now, we calculate the max daily reward.

1,401,150.9 / 365 = 3839 Max Daily PoW Rewards.

With a targeted block time of 13s, there are approximately 60*60*24 / 13.1 = 6,646 blocks per day.

3839/6646 = 0.5776 ETH per block.

According to Etherscan, uncle rewards are responsible for approximately 5% of the total daily reward emission. Therefore, the base block subsidy should be 0.5776 * 0.95 = 0.549.

Thus, we arrive at a rate of 0.55 ETH base block reward to match Bitcoin’s inflation rate.

We further note however, that the transaction fee market for Ethereum has risen sharply this year. As of August 11 2020, at the time of publishing this EIP, the fees from transactions make up almost 80% the current block rewards (2ETH). Thus, even if the block reward was set to zero, miners would still earn 1.8ETH from transaction fees per block.  Due to a robust and thriving fee market, we prepose to round to round down our block reward calculation from 0.55 to 0.5, which means (at the time of writing) miners would earn 1.8ETH in fees + 0.5ETH block reward, for a total of 2.3ETH per block.

## Backwards Compatibility

All nodes must be upgraded to reflect the change in the block reward.

## Security Considerations

Changing the block reward is purely an economic action, requiring only a change to the block reward parameter.

Economically speaking, a block reward that is too low may result in low miner participation due to insufficient financial incentives.  This may result in a decrease of network security that may put PoW blockchains at risk of 51% re-org attacks.

In this EIP we have laid out our economic evidence that reducing the block reward to 0.5 ETH would not negatively affect security by comparing it to other blockchains with larger market capitalizations.  Furthurmore, we note that Miners’ expenses for housing and electricity are priced in FIAT terms (no electrical utilities in the in the world currently charge for Kilowatt-Hours in ETH). Therefore, miners make their mining decisions based on FIAT revenues they expect to earn. In $USD terms, miners would still be paid more than they were 3 months ago if this EIP were accepted (and still more than the 12 month average).  Thus, with this EIP, mining security economics are still better than they were 3 months ago when the price of ETH was half of what it is now, and the transaction fees were a fraction of their current value.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

---

**Otherbright** (2020-08-15):

What are the impacts if EIP-1559 is achieved after or before this proposal?

---

**CryptoBlockchainTech** (2020-08-16):

As a GPU miner I am not in favor of a reduction in Block Rewards unless it includes an algo change to remove ASICs from the network. ASICs are highly profitable compared to GPUs. Any reduction in block rewards without an algo change will remove the rest of the GPUs from the network resulting in ASICs totally controlling the network. You can’t just ignore this problem and hope it goes away. The time has come to remove ASICs before they interfere with Ethereum’s long term progress moving to POS.

---

**CryptoBlockchainTech** (2020-08-16):

Sorry EIP1559 was proposed AFTER ASIC removal. Defi is not calling the shots at every fork insisting their proposals are put in. EIP1559 needs to wait until the ASIC issue is resolved and including any reduction in rewards.

---

**timbeiko** (2020-08-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jdetychey/48/66_2.png) jdetychey:

> We determine the target block reward by first comparing the Bitcoin inflation rate:

It seems like Bitcoin’s inflation rate should be *one* of the parameters in determining the target block reward but far from the only one. The biggest consideration, in my opinion, should be the security of the network (i.e. how do we ensure the likelihood of 51% attacks remains low, how do we keep a diverse set of miners on the network, etc.). I think a section describing this in details would help with your rationale.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jdetychey/48/66_2.png) jdetychey:

> Block rewards will thus be adjusted to a base of 0.5ETH

My hunch is this is much too dramatic of a change, given we’ve gone from 5 to 3 (-40%), then 3 to 2 (-33%), now you are going from 2 to 0.5 (-75%). What justifies increasing the rate at which block rewards get diminished vs. decreasing it (for example, to -25% which gives us 2 → 1.5)? Again, I would personally like to see some security analysis that supports the numbers.

---

**souptacular** (2020-08-17):

How would the calculations or expectations set in this EIP change if we were to adopt EIP 1559?

---

**lmaonade80** (2020-08-17):

I am surprised to see this, especially this large of a % cut. This is a pretty big shock to GPU miners who expected a slow roll down of block rewards over a multiple year period. I have been mining since the genesis block and this will be the third and largest overnight hit to block rewards we would have experienced since launch. It is correct, there is precedent for reducing the block reward, but it has never been 75% cut. GPU miners also just took a big hit with ProgPoW being blocked by other community groups, so I feel this EIP must be contextualized from a miners’ perspective. I must admit, it feels really bad to be treated as a necessary evil to be paid out the minimum possible to incentivize us to keep our lights on just long enough to make the transition to 2.0 work.

With that all being said, I really would like to understand why we are aiming to match the inflation rate of Bitcoin, which is much older than Ethereum, at a different stage in its development, and is trying to achieve different goals than Ethereum. It makes sense that Ethereum would have a higher inflation rate at this point in its history; it is 5 years younger than Bitcoin. I believe blockstream just made fun of Ethereum because we keep changing our inflation rate.

Furthermore, this is feels like simply a shift of revenue from miners to protect the wealth already created by the system. The miners have grown, supported, and built businesses around this network for the past 5 years. Most mining companies barely made it through this crypto winter, and this EIP strips away the incentive we had for powering through stripped away at the first sign of recovery. We worked through the valley because we believed in the project, and we thought there were better days ahead. This EIP puts walls up around the Ethereum garden. We should still be at the phase where we are encouraging new users to participate in any fashion.

The note on the block reward through transaction fees is already wrong by .5 Ether, just one short day after this was published. The current block reward is only comprised of 1.3 ETH worth of tx fees, so we can’t assume transaction fees can consistently make up lost revenue from such a large reduction in inflation, and to make changes based on this assumption is reckless.

I believe it makes far more sense to change PoW rewards (commensurate with past precedent) after PoS is live, as it makes sense to ensure the house we’re moving into is sturdy before dismantling the old one.

---

**CryptoBlockchainTech** (2020-08-17):

Could not have said said it better myself. I too share the same sentiment. Although I have only been GPU mining for four years I still see this project as the biggest thing in Crypto. Since the ASICs took over the network two years ago we have had to scrape our nickles and dimes together to keep the lights on. Now after three months of things finally getting a little better the OP wants to ensure ASICs are only ones who can mine profitability with 75% reduction. I am real suspectful that this is an attempt to remove GPUs once and for all.

---

**stobiewan** (2020-08-18):

Regarding ASICs and GPUS, the block reward is irrelevant. If ASICs out compete GPUs at 0.5 eth per block they will out compete them at 2 ETH per block, and any other number too, it makes no difference. Given steady state ASICs will continue to be manufactured until it is no longer profitable to do so. The argument could be made this reduction is harmful to ASICs as the initial cost is very high, it may not be worth investing in them again after the dag size wipes out current miners as the pay off at 0.5 between now and phase 1.5 may not be worth it.

---

**mmitech** (2020-08-20):

Let’s screw up miners and completely fuck up the network security and decentralization with EIP-2878 and EIP-1559 that seems to be designed around pumping the price of ETH at the cost of its Network security… this will blow off on your faces so badly.

---

**kimicgyueth** (2020-08-21):

By the end of the year network will have huge hashrate drop. I am already used to get screwed by this network as a miner. Reducing reward to ensure value increasing, stop the bullshit about inflation. This eip is just proposed because of recent network fees increase and price increased, i believe if crypto stayed in bear trend nothing of this will not even be mentioned or proposed, stupid. I am a miner, and i am here to profit of course, i choose eth project to invest but so far always had a feeling like i am a bad guy here.

---

**orbital** (2020-08-21):

What a terrible idea…

---

**AlexSSD7** (2020-08-21):

What if the majority of miners won’t support the hardfork? ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=9)

BTW, why only 0.5 ETH? Let’s reduce it to 0.1 ETH, or let’s go even to 0 ETH? Ah, 0 ETH block rewards + EIP-1559… sounds like someone is intentionally trying to destroy the network…

---

**vbuterin** (2020-08-22):

Seems needlessly risky for little gain, especially with PoS coming quite soon. Additionally, I would argue that the fact that fees are so high makes it *more* risky to push rewards down, because fee-dominant blockchains have security issues that block reward-dominant blockchains do not. This includes the sister-mining issues that have been [warned about for years](https://www.researchgate.net/publication/310823336_On_the_Instability_of_Bitcoin_Without_the_Block_Reward) but also more subtle things; for example, miners would purchase hardware based on average fee levels, but there will be periods where fee levels are low, and during those periods there would be a lot of idle hardware, which could be rented out for attacks…

Hence it seems better to lay off on more decreases for the moment and instead put our efforts toward EIP 1559, which [alongside its many other benefits](https://notes.ethereum.org/@vbuterin/BkSQmQTS8) burns fees, reducing the security budget at times when it’s needlessly high, and minimizes any known and unknown risks that arise from the blockchain becoming fee-dominant.

---

**n1njam1rko** (2020-08-22):

Even better, force miners to pay if they want to mine. ![:grimacing:](https://ethereum-magicians.org/images/emoji/twitter/grimacing.png?v=9) I think it’s proposal coming from ASIC miners, because they couldn’t be able to mine after few month, let pump the price and screw the gpu miners as bonus.

---

**CryptoBlockchainTech** (2020-08-23):

Thank you Vitalik for putting this EIP to rest, I have a great deal of respect and admiration for you. Looking forward to the implementation of the new ASIC resitant algo in light of ASICs almost at 51%. Do you still believe what you wrote in the yellow paper “ASICs are a plague”?

---

**drewstaylor** (2020-08-23):

I think the point is there will be a large reduction in overall miners if the rewards are reduced in this fashion. That said, GPU miners can change what they’re mining easily, whereas ASICs can only switch to ETC. Therefore, it’s likely a much higher ratio of ASICs will stay mining ETH rather than switch to ETC or stop mining. This is because stopping altogether is a gamble of abandoning ROI at a time when ETH’s value has been rising.

---

**JustAResearcher** (2020-08-25):

I disagree wholeheartedly with this EIP.

It will absolutely devistate the network security and centralize things to high hell at the same time.

Like someone else said, why stop at .5ETH? Why not zero? As you said this is purely an economic play. ![:face_with_raised_eyebrow:](https://ethereum-magicians.org/images/emoji/twitter/face_with_raised_eyebrow.png?v=9)

---

**TMan253** (2020-08-28):

Reducing block subsidies incentivizes miner-induced chain reorganizations, since the risk/reward of looking backward in the chain to republish recent expensive transactions to steal their high network fees starts to become more favorable than looking strictly forward to the mempool for legitimate operation.

Furthermore, mining related EIPs have been systematically deprioritized for a few years so that developers can focus on strategic PoS tasks, so this EIP should also be similarly deprioritized.  If adopted, this EIP should be pushed after the existing mining related needs, like fixing known Ethash vulnerabilities (details of which are documented in the various ProgPoW analyses).

---

**jumpnkick** (2020-09-12):

Ridiculous proposal at the end of PoW.

Dishonest to say mining will not be affected or security either.

Why should we compare inflation rates to BTC?

What is the problems for miners to profit if the whole chain integrity rellies on them?

We won’t be worrying about inflation if DeFi craze combined with lower processing power in the chain start making bottlenecks.

It’s time to have the best version of ETH 1.0, and not jeopardize it just before the giant leap ETH 2.0 will mean.

This EIP is at least irresponsible.


*(25 more replies not shown)*

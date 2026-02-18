---
source: magicians
topic_id: 5550
title: EIP-3368 - Block Reward Increase /w Decay for next two years
author: bitsbetrippin
date: "2021-03-12"
category: EIPs
tags: [block-reward, eip-3368]
url: https://ethereum-magicians.org/t/eip-3368-block-reward-increase-w-decay-for-next-two-years/5550
views: 23310
likes: 357
posts_count: 109
---

# EIP-3368 - Block Reward Increase /w Decay for next two years

New EIP being submitted as mitigation to risk associated with EIP-1559 and potential cliff of hashrate that could drop off Eth Network. Link for EIP soon.

## Replies

**DCinvestor** (2021-03-12):

Ethereum has established a model of “minimum viable issuance” with broad community consensus. Most projections do not indicate that an increase of the block reward is required to maintain secure operation of the network- even with the successful implementation of EIP-1559.

Further, accommodation of this form only delays the inevitable as we move swiftly towards a merge of eth1 and eth2, where PoW mining rewards will be zero. IMO, we should avoid measures which encourage further investment in mining hardware by miners given this reality.

For these reasons, I don’t feel this proposal is necessary for sustaining secure operation of the network, nor does it gainfully improve the network.

---

**green** (2021-03-12):

It reads like a subsidy of users to miners to delay impending change. Why? How are miners entitled to stability and ease of change? Why start from 3 ETH, why not start from 2 ETH instead, if the purpose is simply to ease change?

There is no such thing as risk free business. Miners all over the world razed through GPU graphic cards to make **profit**, and that implies risk.

Their “worthless” hardware is going to easily be absorbed by the market. Even if it wouldn’t, the personal, business decisions of miners are not the concern of Ethereum users. You don’t socialize profits, then you don’t socialize losses.

---

**Rob** (2021-03-12):

I agree absolutely with everything that DCinvestor has said. A block reward increase is unnecessary for security, it undermines the “minimum viable issuance” monetary policy, and it’s a distraction from the Ethereum roadmap.

Accepting this proposal would establish a precedent that Ethereum’s monetary policy is more or less arbitrary and that with sufficient social pressure issuance can be increased to benefit certain stakeholders. This would be catastrophic for Ethereum.

---

**greg** (2021-03-13):

Is there a link to the proposal? I can’t seem to find an open PR on the eip repository.

---

**green** (2021-03-13):

[EIP 3368 LINK](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3368.md)

---

**greg** (2021-03-13):

Edit-1: I miss understood that this will be alongside eip1559. Will take a second look to better understand this. The below comment has yet to be adjusted. This is *not a counter proposal*

Thank you!

It seems that this EIP doesn’t quite target similar goals. If I’m not mistaken, one of the goals behind 1559 is to make gas prices more predictable (not necessarily lower). This seems to not affect that whatsoever.

I’d be keen to see a ~counter proposal~ that also attempts to make gas more predictable as that also benefits the wider community.

Looking forward to seeing this transpire.

---

**nikitakhrushchev** (2021-03-13):

I strongly disagree with this proposal.

I seriously doubt the PoW chain will last for 2 years (eth devs seem to want to accelerate the merge now). I think fears of ETH getting 51% attacked are way overblown (I seriously doubt a decrease of hashrate of like 20% would negatively affect the network), and a PoS merge is happening sooner than you might think.

---

**YouBoyFromMars** (2021-03-13):

Can you explain how 2 years was decided as a mitigation time?

The EIP’s motivation section talks about the risk being “A **sudden drop** in PoW mining rewards could result in a **sudden precipitous decrease** in mining profitability that may drive miners to auction off their hashrate to the highest bidder while they figure out what to do with their now “worthless” hardware. If enough hashrate is auctioned off in this way **at the same time**, an attacker will be able to rent a large amount of hashing power for **a short period of time** at relatively low cost and potentially attack the network.”

All of the above focuses on short-term security issues from the addition of EIP-1559’s burn model that would be implemented instantly one block to the next - the ‘cliff’. Yet EIP-3368 is trying to help smooth out the reduction in block rewards over a 2 year period. However, there is no substantiated reason why this would be a 2 year problem for Ethereum.

On top of this, the block reward sounds to be scheduled to “decrease slightly every block” indicating a linear decay. Meaning for the first 12 months issuance will be higher then a flat 2 ETH per block reward. Then the second 12 months issuance will be lower then a flat 2 ETH per block. The second 12 month period then being the time where the long term supply is ‘made whole’ within that 2 year window. The problem is the likely hood of the merge of PoW to PoS not occurring within 2 years is basically nil. This means this will almost certainty result in a net increase to issuance - leading the chain away from Ethereum’s goal of “minimum viable issuance”.

Simply put, the 2 year decay period is far out of balance with what is ultimately a rather short lived issue.

---

**greg** (2021-03-13):

I believe the eip needs an update. Per a Twitter thread, the eip should also read:

`Requires: eip-1559`

This would reduce some confusion.

---

**bitsbetrippin** (2021-03-13):

Minimum Viable Issuance makes sense in a Proof of Stake world where you have built in penaltiy/slashing routines to keep incentives aligned., but in Proof of Work you are purely counting on the ‘minimal issuance’ maintains enough of the potential hashrate for the network. While this has worked for the past 5+ years, this recent bullrun has seen a 2.5x increase in force projection on Ethereum and continues to rise due to Fees/MEV + existing BR. The average ‘reward’ payout over the last 4+ months has exceed 3.6 ETh. The Feeburn is expected to burn 10-40% of the additional 1.6 ETH if not more and on days of heavy activity where block rewards are upwards to 6-10, we could see more burned then the 2ETH inflation.

A planned offset with decay puts for a flat baserate plus burn with EIP-1559 included. Your still providing value to the hodl position and ensuring Eth maintains the 2nd strongest network next to Bitcoin.

This basic ‘we are making miners rich’ narrative is misguided. There are more new miners every day because the ecosystem allows for more horizontal growth in securing ETH. This information war campaign on the mining ecosystem is misplaced by the very people that live under the veil of its security.

---

**bitsbetrippin** (2021-03-13):

Maybe PoS comes sooner, but nobody here nor the devs can say that with any definative statement. A checked in notional specification while good to see is effectively the break glass option and fix later. While it may sound the rally cry for 10 minutes when people actually sit back and realize what that could mean they will not op for a half backed solution. Liquidity Providers (which I am one of on multiple pairs) and other DeFi functions are not going to just rely on a pissed off fast merge approach to a completely theoretical implementation. Testnet, unit testing and other CI needs to shake out functionality before that really gets merged.

The EIP also needs to be updated to “OPTIONAL” if the Eth Price/MEV keeps rates where the risk to security is still low post EIP-1559. This is a counter risk if there is a large drop in overall issuance due to high basefee burn and low ETH prices. Not against compromise on the rate/decay.

---

**bitsbetrippin** (2021-03-13):

This is not about mental gynanstics with your ‘well established social contract’. The risk is actually pretty linear. The 51% attacks are not Theoretical, they have happened on many PoW chains. The nefarious actors don’t care about your decorum or ideologies around MVI. The arrogance lead ETC to getting attacked 4 separate times before they had to implement a anti-51% methodology.

What I want to ensure is there is a real plan, implemented and ready to trigger that addresses a mass exodus. Ethereum should have that projection period. The algorithm has 0 protection against a 51% attack. Other networks with Ethash have been successfully attacked. The know how, the scripts and intention is there. The fact we have to debate is shocking. The force projection of Ethereum is nearly 2.5x ATH. This means the total network PoW GPU/ASIC hashpower is profound. Much of that hashrate is very new participants. The attack vector is there. Nicehash, MiningRigRentals, Cudaminer and about 10 other separate broker services all broker hash to the highest bidder.

I have 0 confidence ACD and this body of participants are agile enough to address the problem before it would happen, if there was a existential threat. It’s like arguing for the safety check on a plane so you can have a cheaper fair.

---

**bitsbetrippin** (2021-03-13):

Yes, It is being proposed as a included with EIP-1559. 1559 would go in as planned, 3368 would go in as a safety net as maximum security posture prior to PoS merge. Climate has changed, 410+ TH plus nearly 120+ TH on other networks is a mountain of potential hashpower. The entire mining climate has expanded due to the bullrun as it has allowed more to participate.

Much of the viewpoints people have on mining is a ‘vertical’ revenue increase model, but in reality, horizontal (*participants) grow faster than any one single entity. It’s not one miner getting wealthy, its the 500+ new participants a day that start mining. (individual contributors) improving decentralization of hashpower against a federation of pools (40-60 world wide)

---

**bitsbetrippin** (2021-03-13):

And folks bet the farm on this assumption. This is not 2017 #s; why would people even want to assume a vulnerable algorithm

---

**nikitakhrushchev** (2021-03-13):

You have not provided any evidence or any models supporting your claim that a 51% attack will happen if EIP1559 passes. Meanwhile, there has been tons of evidence from the other side. The facts are that hashrate was 20% lower than it is now just one month ago, and no attack happened. If an attack was feasible then it would have happened last year when defi was popping off yet the hashrate was less than half. This is just blatant fearmongering from miners.

---

**YouBoyFromMars** (2021-03-13):

My statement was looking past the recent glass break option you noted. Given recent events I 110% understand why that would be the primary thought, but truly I was more-so referencing the ‘normal’ timeline where the merge can is released without the quick / fast merge approach. It seems your first paragraph was geared towards that. Which is appreciated the response, but I’m not sure struck the heart of my concern / question.

I’ll try to narrow down — by the time London is released w/ 1559 included the Beaconchain will have been running for 6 to 7 months. Assume the price / MEV / fee rates show a security risk and 3368 is launched, this means a 2 year decay window puts us to mid-2023. What is the basis for thinking this will be an issue going into mid 2023?

2023 is also notable because even with the old (and now defunct) Phase 0 / 1 / 2 model the docking was still expected in 2022. Given changes to that model to eliminate Phases all together and the general sentiment to merge before sharding (even  talked about outside the scope of 1559) it seems going into 2023 is essentially not going to happen and even a late 2022 is unlikely. Even the docking page of the Ethereum website is guessing 2021/2022 - https://ethereum.org/en/eth2/docking/

I understand track records / our lack of crystal balls can not lead us to a definitive statement, but surely a mid-2023 phase out is *very* conservative for a merge date. Mid 2022 puts us 1 year out from London and would be a more reasonable estimate for a merge date (even including the testing you noted).

So what I’m getting at is 2 years just seems far too long for something like this and doesn’t seem based on any meaningful metrics. All of which looks beyond the point I hit on initially - this is a security issue that is relatively short term (think months, not years). As you noted, a cliff. So the merits of smoothing out make sense but the decay period seems very far off. While my opinion is meaningless on the grand scale of things, I would wager a majority of the community would see 2 years as a non-starter. I don’t see how this gets traction at all unless that window is at least 1 year or less… likely even 6 months or less. The 2 year length makes the compromise of a 1 base reward essentially meaningless to the broad community since it will potentially get cut out completely or more likely just shortly lived. I wouldn’t even begin to support this until the decay was at the 1 year or less length.

---

**norin** (2021-03-13):

An important point is there is no “correct” level of security as any increase of BR leads to marginally higher security. It is therefore critical to do **sufficient modelling** to prove that the increased costs to Ethereum are worth the increased protection. On top of this, a rented hashrate attack would not destroy Ethereum, it’s again a question of how much the Ethereum community is willing to pay to reduce the risk. For some context, the proposed 1 ETH BR increase represents ~$11M / day at current prices ($1750).

---

**bitsbetrippin** (2021-03-13):

“If rentable hashrate is a viable threat under 1559, other proposals make more sense than paying miners more in what amounts to extortion. Fast merge to ETH2, hard fork to an ASIC friendly algo of a lower cap coin, etc.”

This is effectively the claim and the risk. There are models where I believe this does become a risk.

- Fast Merge to ETH2 is substantial more risk if not fully tested, overnight ETH could sack its own network from a desync of consensus/finality ; This is not ready, the integration tech specification was rushed to post yesterday. Non-starter before July
- Hard Fork to ASIC Friendly Aglo? What? PROGPOW went through 2 completely separate funded deep dive technical analysis, was greenlit and shelved because of scrutiny by ASIC makers and a few Defi folks. ASICs take time to tap out, Testing, Audit … I hear you but leaning into a single manufacture and investors would pull you into a lot more politics then a loosely organized group of GPU enthusiast miners.
- Miners do come and go and the market ebbs and flows, 100% agree, This is how eth was fine during the 2017 ATH to 2020 Lows of 89.xx; Mining retracted quite a bit, but benifited from the Bitmain E3 sunsetting due to DAG file decrease. Nearly 20+ TH fell off during that time, mainly E3’s, which kept the force projection of GPUs at the time 110+ TH able to participate. We are taking 410+ TH and by July with the current growth thrend possibly 600+ TH. That will wholesale rely on average BR 2 + 2 Trans fee and 1500-1800 Eth Price. That drops to 2 flat or just over 2 from MEV ; the numbers can be up to 20% HR drop. If we are looking at 800 Eth price in July for whatever reason but BR 2 + 2-5 Trans fee that will go away due to 1559, now we move from 600+ TH to 300-350TH sustainable.

That 200-300TH will find homes or turn off. This is the time a would be attacker places a buy order on brokers. And before you tell me someone would pay if they had the chance to take down Eth, we live in a reality a NFT goes for 69m dollars, of which a Eth competitor TRX casually threw a bid on. Not saying Justin would attack, but I dont want to take the risk.

This notion of paying a cartel or compromising with miners is an unfortunate mindset. As a advocate for mining since 2013, putting over 7000+ hours of content out there teaching people how to participate on networks, of which 4k+ on ethereum alone resulting in nearly 5.5 million views we are considered a shitshow. I would argue to say the engagement, involvement and value add as a Miner I have brought hundreds of million of value to this ecosystem of participants. I didn’t have to do that and I don’t need your thanks for it, but the misguidance that the mining participant is your enemy is misplaced.

Lastly and in closing. The previous show of force may have been partially short sighted, I agree and mentioned such on YouTube today in front of 900+ live viewers in a 1.5h discussion. But the threat has not been seriously considered with a bunch of people not providing a lick of data and just standing behind the past that ethereum is safe. I see the existential threat to Ethereum and I have no doubt others willing to harm it do to. This is not a time to take a ‘minimal security model’ mindset. It’s short sighted and borderline high risk if I was an outsider looking in right now seeing two sides of this argument. “We want to pay the min. for security”, said nobody ever besides a CTO, reporting to a CFO, that both get fired the next year after the hack.

---

**DrDrago** (2021-03-13):

Made an account here just to post for this (I support this EIP with 1559)

1. Does Fee burn put Ethereum on the SEC’s radar? Commodities dont decrease their supply… (More fleshed out argument at https://coingeek.com/ethereum-2-0-is-an-unexploded-regulatory-bomb/  + https://medium.com/@craig_10243/proof-of-unregistered-security-798f4df2fbb9 ) (would this EIP solve this because supply would not be decreasing if BR was increased? should net out?) (I disagree slightly with the author, POS isnt the main threat that would get eth classified as a security, its deflation… commodities dont reduce the # in circulation…) (for example, 51% attack under POS, you destroy their eth with a hardfork, and you run afoul of U.S. securities laws immediately and yep, Ethereum isnt registered either…) Reasonable minds can agree to disagree on whether the government would do this, but based on what ive seen, most governments are looking to shut down or restrict crypto heavily/regulate it. They would probably jump at the opportunity. Not sure how we could prove this is a threat though until its too late, so this a minor point against implementing deflation.
2. I believe the risk is large with EIP1559, im most concerned about the nicehash attack scenario which this EIP3368 would help prevent, if revenue to miners decreases significantly, so does the upfront cost to initiate an attack. Once the price becomes low enough for someone to begin an attack, it becomes self sustaining since any rational 51% attacker would censor the other 49%, and they can double spend / make off-chain bets to make back any upfront cost+profit.  (once the 49% is censored, it becomes rational to join the attackers) (miners can centralize on nicehash faster than devs can release the merge and respond…) Hence, best to not allow a chance of that happening.
3. While i believe in the policy of minimum viable issuance, i dont believe in waiting for an attack to occur before you acknowledge it as a possibility. The nicehash scenario is a real threat given the anticipated revenue drops for miners, even ignoring difficulty. Although eth’s price could rise to match, theres no guarantee it will. Hence, in my view, this is a necessary BR increase to compensate for the immediate drop off in revenue that 1559 will cause for miners. A sudden drop in revenue(1559 without 3368) is a strong motivation to attack the network, since other coins will have no time to attempt to fill the space (no other options), most miners will see dropping gpu resale prices and refuse to get out (in hopes they can recoup their investment), and that leaves us with a massive amount of hashrate looking for another home, all at the same time. (thats how you end up with a nicehash attack) This EIP would instead spread that time spent looking for another home through a year+, as the less power efficient cards would be dropped off the network first, while the rest remain profitable… gradually dropping off and finding new homes. This seems like a much smaller risk, especially since gradually dropping hashrate will cause difficulty to adjust accordingly.
4. GPU miners have less incentive to attack the network before the merge, their hardware remains with atleast some value after the merge. We can disagree over how much value, but it is some atleast. ASICS retain zero value after the merge, that provides a much stronger incentive to attack the network before the merge. Personally im concerned ASICS will continue to proliferate before the merge, if we decrease eth mining profits to such a point that GPUs are priced out, we end up with ASICs dominating, and much more difficulty and risk with a 2.0 merge.
5. It has not been lost on me that ASICS have largely been quiet or lightly supportive on EIP-1559, it isnt a threat to them, its an opportunity to push out gpu mining hash. (and thus gain more control and profits) GPU miners can threaten, but it is much more difficult for them to coordinate an attack than it would be if ASICs dominated the chain. (as ASICS have a good shot of getting atleast 50% of hashrate before the merge already imo, without any changes, pushing out the gpu miners should be regarded as a real threat, ideally we have both groups continue hashing)
6. Im of the opposite opinion of others in this thread, this BR increase is necessary to ensure profits remain high enough for miners until the merge is ready that attacks remain prohibitively expensive. Without it, the upfront attack cost drops drastically. (and once an attack is ongoing, it can be self-perpetuating) It also ensures we dont end up with an ASIC-only chain anytime soon.  (without a BR increase, less efficient setups will drop off in mass, entirely GPUs dropping off, no ASIC will be inefficient enough to be brought down by EIP-1559, but the revenue drop combined with difficulty increase will likely push out massive amounts of GPU hashrate, resulting in ASIC centralization) Best case scenario in my book is to implement this change and rush to POS ASAP, hopefully complete the merge before ASICS represent a majority of hash.

I also disagree that this would set a precedent for arbitrary changes based on social pressure, this EIP3368 isnt about social pressure and thats not the reasoning put forth for it, the goal is to deal with the network security issue that exists due to a sudden drop off in profits that will occur with EIP1559, smoothing this drop off out over a longer time period than 1 block is very beneficial for the security of the network, and it happens to be beneficial for miners aswell.

Its worth noting, 3eth block reward would just about match current revenues with post EIP-1559 revenues, disregarding difficulty of course. A decrease from that 3BR point is still an overall decrease in miner profits (when factoring in lost fee revenues), its just this EIP would spread the gradual drop in miner profits out over a longer time period, and EIP1559 would cause the drop immediately in a single block. Hence, it deals with a legitimate security issue contained within EIP 1559, no one can predict how the majority of hashrate will respond to a sudden 40% drop in revenue (thus, initial attack cost dropping 40%) so it doesnt make sense to play a game of chicken with them! Miners can attack and cause significant damage faster than devs can release the merge in response. Users think that the miners knowing devs will rush POS will stop an attack before it starts, but when hashrate becomes unprofitable, they no longer care about the “theyll kill me sooner” threat… they’re already dead at that point…

It makes sense to not risk it, based on the calculations ive seen, the drop off in revenues is a serious threat with EIP-1559 alone, couple in the difficulty rise, and we have a *real security threat* that needs addressing

If POS is ready and able for an emergency merge, it should be done ASAP, if not, it shouldnt be used as a talking point as to why we dont need to give miners concessions. Clearly, if our other option is not ready, we must give concessions, or were playing a game of chicken with a $200bn network.

My vote is 1559+3368+969(whenever someone proposes 969 again?) in the same hardfork

1559 for the predictable fees, 3368 to deal with the short term security risks posed by 1559, and 969 to atleast make future asic centralization *more difficult* (more might be needed prior to the merge to address this, personally i think people are drastically underestimating the progress ASICs are making currently due to a lack of hard proof)

Edit to expound on the last point about ASICs: (I could also get behind 1057, but i understand thats a non-starter.) I simply do not believe that the recent hashrate increases weve seen could have been entirely gpus based on inventory numbers…, given the magnitude of the rise, my person opinion is ASICS are probably 10%<x<20% of the network already. Ive heard their main downfall currently is the chip shortages, but this wont last,  and shouldnt be bet on continuing. I’d like to see more proposed EIPs dealing with ASIC resistance. The break-glass moment (1057 becoming a necessity due to ASIC 40-51%) has a high liklihood of occuring before the merge can be completed in my opinion even if we pass 1559+3368+969. (simply due to the market forces, theres a massive amount of capital funding ASIC development and manufacturing currently, and they know they need to do this ASAP) (this has to do with EIP3368 because 3368 addresses the short term security issues of 1599, one of those security issues is that EIP1559 would further the domination of ASICs over GPUs by decreasing rewards to a level potentially unsustainable for GPUs, but entirely sustainable for ASICs.)

---

**bitsbetrippin** (2021-03-13):

I have, and needed to output it to the EIP. This will be added to the EIP. The source data: https://docs.google.com/spreadsheets/d/138M4R1-_zS-OLBsl2VJeN_anfTSCRCFc6EguYUVG-yA/edit#gid=1954833572


*(88 more replies not shown)*

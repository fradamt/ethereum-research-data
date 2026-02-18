---
source: magicians
topic_id: 2342
title: Guidelines for ProgPow Hardware Developers
author: Taek
date: "2019-01-06"
category: Magicians > Primordial Soup
tags: [progpow, mining, hardware, asic]
url: https://ethereum-magicians.org/t/guidelines-for-progpow-hardware-developers/2342
views: 7716
likes: 20
posts_count: 16
---

# Guidelines for ProgPow Hardware Developers

I was guided to this forum as potentially the best place to ask this question. This is not a troll post, it’s a genuine set of questions relating to ProgPoW specialty hardware.

Since the announcement that Ethereum is going to be switching to ProgPoW, I have been contacted by multiple groups who are working on ProgPoW hardware in some fashion or another. Some of the groups are FGPA developers, and some of them are ASIC developers. The question is basically the same from everyone though: what needs to be done in order to bring ProgPoW hardware peacefully to the Ethereum community? Nobody has interest in making enemies or being hardforked and invalidated, yet multiple groups have interest in making special purpose Ethereum mining hardware, which at this point means targeting ProgPoW.

And, I would also like to highlight some of the game theory in play: hardware developers have 3 options available to them:

1. Develop hardware that will be released to the public.
2. Develop hardware that will be kept secret and released to specialty groups only.
3. Do not develop hardware at all.

If the ethereum community at large greatly opposes the development of specialty hardware, that only leaves options 2 and 3 for hardware manufacturers. And while some manufacturers may choose option 3, the amount of money at stake essentially guarantees that at least some hardware group is going to choose option 2.

The other thing that I would like to highlight is that as of writing, the ProgPoW creators generally have a very high confidence that the performance margin between specialty ASICs and GPUs is not going to be very large. If I recall correctly, they predict that an ASIC is likely to be 20% better at best than the best GPUs. This difference is substantially less than the difference between a home GPU miner and an economies of scale GPU mining farm, which would suggest that if they are right, the Ethereum community does not have to worry about greatly exacerbated effects from Ethereum ASICs.

On the other hand, ASIC designers feel that 2x should be easy, and more than 10x may be attainable. So the question comes back to the game theory: if a hardware developer manages to create a ProgPoW ASIC that outperforms GPUs by a surprising margin, let’s say 10x or even 100x, is it better for that manufacturer to keep their discovery secret and mine secretly, or is it better for that manufacturer to sell openly?

As of right now, I believe that the best thing for any ProgPoW hardware group to do is to keep their operations completely secret, as I believe they would risk a hardfork and losing all of their efforts if they brought forward a good piece of hardware to the public. I know that what many in Ethereum would prefer is that these hardware manufacturers focus on different cryptocurrencies or ASIC projects entirely, however the risk/reward equation is really attractive for ProgPoW hardware, and many of these manufacturing groups are not ideologically motivated int their interest in ProgPoW: it is a monetary motivation.

If the Ethereum community can come forward with some firm guidelines for publicly delivering ProgPoW hardware however, I believe that hardware manufacturers will not be required to operate in secret.

## Replies

**AlexeyAkhunov** (2019-01-06):

Thank you for writing this up!

In my opinion, the discussions of ProgPOW and ASICs among the core developers has been suffering from the lack of expertise in modern hardware manufacturing. Core Devs do not have internal hardware experts, as far as I can see. I have asked (though not publicly) for a commissioned research/analysis into the issue of ASICs and its impact on the Ethereum network, because I saw this was the only way to bring that missing expertise to the table. But alas this idea did not get traction at the time.

As far as I can see the main worry that people seem to have with ASIC is what you described in item 2:

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/dc4da7/48.png) Taek:

> Develop hardware that will be kept secret and released to specialty groups only.

Item 1 on its own is not a reason for concern:

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/dc4da7/48.png) Taek:

> Develop hardware that will be released to the public.

But even if the secretive mining is occurring at the moment, it only poses a problem if it occurs over the long time horizon. If it feasible that there is a real competition coming from ASIC manufacturers who sell their devices publicly at fair price, and they can catch up quickly enough, I do not see the problem with temporary private mining - it will be a minor blip in the history. My main question to an expert is this: **how quickly can competing ASIC manufacturers nullify any advantage that another (possibly bigger, like Bitmain) manufacturer has?** If the answer is less than a year, then I would say, definitely not to bother with ProgPOW, and just leave things are they are.

My main concern with ProgPOW roll-out is that it is a distraction from scalability track, but I simply lack any credible information to convince people to not do it, or convince myself that it needs to be done. The reason I suggested that the decision about ProgPOW was to be made yesterday is based on my assumption, that no new information will come to light for the next 2 weeks, and so we will keep procrastinating. On the other hand, making a tentative decision produced a good response that we needed - people started to take the issue seriously enough to start talking.

---

**Taek** (2019-01-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> My main question to an expert is this: how quickly can competing ASIC manufacturers nullify any advantage that another (possibly bigger, like Bitmain) manufacturer has?

If you look at the history of hardware as a whole, generally speaking you get one or two dominant leaders, and then you get 5 or 6 people who can follow semi-competitively. The leaders often can hold a 2-4 year lead over everyone else.

In the case of something like sha256, the algorithm itself is simple enough that it’s difficult to really get a lead. So the lead tends to not be as strong and not last as long. That said, the S9 held essentially complete market dominance from 2016 to 2018, so that in fact was 2 years of headway. The team that made the S9 has now made the M10, and that machine is similarly very far ahead of what everyone else has been able to do.

For something like ethash or progpow, the economies of scale are a lot more favorable to larger manufacturers, because they incorporate so much memory. You now have more things to optimize: the silicon chip itself, the memory interface, the memory chips, and the general communication structure and algorithmic strategy. Early on this will make manufacturing a lot more chaotic, as one team developing an advantage in X may be sufficient to put them far ahead of everyone else. But in the long term, to be a competitor you will need to have master tier skill and scale in all major resource categories, which takes more money and a larger team, and altogether makes it much harder for a startup to compete.

I think it’s reasonable to assume for ethash and to an even more significant extent progpow the lead that the industry leader has over the rest of the network will be larger than what we see in bitcoin, and the number of years ahead of everyone else that they will be will also be larger than in Bitcoin, though it will probably not be as bad as it is for GPUs or CPUs.

---

**AlexeyAkhunov** (2019-01-07):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/dc4da7/48.png) Taek:

> For something like ethash or progpow, the economies of scale are a lot more favorable to larger manufacturers, because they incorporate so much memory. You now have more things to optimize: the silicon chip itself, the memory interface, the memory chips, and the general communication structure and algorithmic strategy

Yes, so we are amplifying this effect when going from EtHash to ProgPOW. One strategy (or you can call it guideline) that was mentioned twice on the calls is to introduce ProgPOW, and then, in a year’s time, “see” if there are ProgPOW ASICs around, doing private mining, and if there are, switch to something that is super simple to make an ASIC for, like double SHA3. The problem with this strategy, as I see now, is this: If is already difficult to see if there are EtHash ASICs private mining, it will be even harder to see if there are ProgPOW ASICs private mining in the future, because the manufacturers will use more secretive methods for deploying them. So we are pushing ourselves deeper into the strategy based on knowing the unknown.

If we want to obsolete the current EtHash mining devices, but at the same time not to induce more secretive behaviour on the part of ASIC manufacturers, we need to “embrace” it and switch to an ASIC-friendly algorithm now instead of an ASIC-unfriendly algorithm. Which the opposite of what we are doing.

---

**holiman** (2019-01-07):

Thanks [@Taek](/u/taek) for starting this discussion.

For context, I gathered some input from you a couple of months back, and I have talked about your feedback in a previous core-dev call and have also posted about on the allcoredev gitter channel.

As I’m not a hw designer myself, I do consider you an authority on the subject. My takeaway from your earlier comments were,

1. That progpow would delay/setback the ASIC mining on Ethereum by about a year.
2. That progpow could lead to increased centralization after that time, since only larger teams would be able to produce such an ASIC, and thus get a mononoply.

It’s because of 2) that I have also talked about switching to something extremely simple after maybe a year.

From a game-theory perspective, out of your three options, we’ll never know (?) if 2 (develop hardware in secret) or 3 (no hardware) is happening. So from our end, we will probably have to assume that the worst case (2) is happening.

So my strategy of choice would be to switch to progpow now, switch to very-simple-algo one year (one and a half? two?) after the progpow switch.

In the best of worlds, we are close to PoS one year from now, and might decide it’s not worth meddling any more with PoW.

---

**Taek** (2019-01-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> So my strategy of choice would be to switch to progpow now, switch to very-simple-algo one year (one and a half? two?) after the progpow switch.

It would have set back ASIC mining on Ethereum by about a year had it been deployed immediately. From what I understand, the current proposal is to switch to ProgPoW in June, which gives hardware manufacturers a full 6 months to come to market, and the ProgPoW algorithm has already been studied by numerous development teams as it’s been around for many months - hardware manufacturers would not be starting from square zero.

The key technology for ProgPoW is likely to be either HBM2 or HBM3, something that we know existing cryptocurrency ASIC developers were already exploring for Ethash, which means some of the bigger barriers have potentially already been overcome.

That is to say, because the switch is happening so late, I no longer believe you’d get a years worth of advantage out of it. I don’t know that you’d have ProgPoW ASICs as soon as June, but you’d probably have them before 2019 ended.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> The problem with this strategy, as I see now, is this: If is already difficult to see if there are EtHash ASICs private mining, it will be even harder to see if there are ProgPOW ASICs private mining in the future, because the manufacturers will use more secretive methods for deploying them.

Historically I think communities have been pretty bad at recognizing when they have secret ASICs mining on their networks, if not in part because they simply don’t want to believe it. I have 3 examples that I am quite confident about: Bitcoin (the S9 was mined secretly for about 4 months prior to launch, I believe), Monero (some sources have suggested to me that the secret mining went on for >9 months before detection), and Sia (there’s blockchain evidence that Bitmain secretly mined Sia for 2 months prior to announcing their ASICs). I also believe that Zcash had secret miners on it, however this is contested and I don’t think there’s enough evidence to definitively say one way or the other.

Even if you do find evidence, then you have to pull the political strings required to execute the fork, and as Ethereum matures that’s likely going to become increasingly difficult. My guess is that secret ASICs would be free to mine for 3-9 months even after being discovered, simply because it would take that long to motivate the Ethereum community around another fork.

---

**esaulpaugh** (2019-01-09):

You say it’s not a troll post but then you say it’s conceivable that progpow could be end up being sped up 100x by ASICs (which would make it 50x less ASIC-resistant than Ethash). If ProgPoW gets sped up by 100x then we should all party like it’s 1999 because that means there’s been a breakthrough in comp sci and electrical engineering so monumental that it will change human history.

Even if there’s some sort of freak black swan event like an undiscovered mathematical trapdoor making it slightly worse than Ethash then we simply switch PoW algs again? Even if we choose crappy algorithms, as long as they are switched regularly it doesn’t matter much. But all the evidence points to this one not being crappy

---

**maxsam4** (2019-01-09):

Has anyone got an estimate of how much of current hash rate is made up of ASICs that won’t work with ProgPoW?

In light of the recent 51% attack on ETC, we should only consider kicking ASICs out if we have enough GPU miners to maintain network security.

But then, If the percentage of ASICs is already low and it is known that Ethereum is planning on dropping PoW, is it even worth implementing ProgPoW?

---

**MariusVanDerWijden** (2019-01-09):

ProgPoW has been implemented in big nodes (geth, parity, aleth) as well as in ethminer.

There is a significant portion of the network running ASIC’s. We estimated about 60%

ProgPoW is essentially Ethash with some additional math thrown in. ASIC’s could achieve  at most the same speed up as with Ethash. The advantage is, that 6-10 months of development time gets wasted which makes it really hard to develop an ASIC.

---

**Taek** (2019-01-09):

100x was stated with the intention of mental exercise. I also don’t think you understand the nature of application specific optimizations. Even when the algorithm is specifically targeted at GPUs, GPUs have big constraints such as needing to be able to work with consumer power supplies, needing to be able to survive a wider range of temperatures, having higher standards for what counts as a good or bad die, having lower tolerances for the occasional mistaken bit.

Special purpose hardware always comes out far ahead of general purpose hardware because when you don’t have to plan for everything (the way Nvidia and AMD do), you get to cut a lot of corners that would be absolutely intolerable at the bigger manufacturers. The freedom of ASIC development is in all the little details that you no longer have to stress about, and they tend to add up faster than most people realize.

 consciousEntity:

> If we continue with implementing ProgPOW in response to community consensus, then it will be because that consensus is that ASICs are not welcome on the Ethereum network. Therefore, the only option is 3. Do not develop hardware at all (or 2, I suppose, if you feel that way).

That’s more or less how I’m interpreting it as well. Unless there are very clear guidelines for how to develop chips for Eth, and how to not be bricked, manufacturers will prefer secrecy so that they can ROI.

---

**Taek** (2019-01-09):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/c0e974/48.png) maxsam4:

> In light of the recent 51% attack on ETC, we should only consider kicking ASICs out if we have enough GPU miners to maintain network security.

Isn’t the general belief that ETC got 51% attacked because they shared hardware with more powerful coins? ASICs are a good thing, incentive-wise, for Eth. When ETC got attacked, it’s value got hit hard and any ASICs which would have been ETH-exclusive would have lost a ton of value. But since ETC does not have exclusive hardware, the hardware attacking ETC did not have to worry about the value dropping.

---

**esaulpaugh** (2019-01-09):

Do you have any communicable reason to believe that an Ethash level of vulnerability to ASICs would not be an upper bound on that of ProgPoW? Because if you’ve found something you can publish and get mad citations. Each new algorithm is not a roll of the dice w.r.t. ASIC resistance

---

**maxsam4** (2019-01-10):

> Isn’t the general belief that ETC got 51% attacked because they shared hardware with more powerful coins?

You don’t need to own the hardware to do 51% attacks. You can just rent it. The attacker on ETC probably rented most of the hashpower. ProgPoW will make renting more efficient because GPUs can easily be rented.

> ASICs are a good thing, incentive-wise, for Eth. When ETC got attacked, it’s value got hit hard and any ASICs which would have been ETH-exclusive would have lost a ton of value. But since ETC does not have exclusive hardware, the hardware attacking ETC did not have to worry about the value dropping.

Yes, you are right. With ProgPoW, the aim is to eliminate ETH-exclusive hardware and it reduces the security by a bit.

ps. Are you in favor of ProgPoW or against?

I personally don’t care much but If I had to pick a side, I will side against ProgPoW because I don’t see the need for it.

---

**maxsam4** (2019-01-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mariusvanderwijden/48/1374_2.png) MariusVanDerWijden:

> We estimated about 60%

Monero saw the hash rate drop by 85% when they implemented ASIC resistance in April. I have been active in the Monero community and I had never talked to someone who admitted using ASICs. On the other hand, I know a handful of people who use ASICs on Ethereum. This could be just because of the sheer number of Ethereum miners but It felt like Monero mining scene was more decentralized even before they kicked out ASICs. My sample data for this conclusion is rather small but It’s a concerning point IMO.

ETC has ~5% of hash rate of ETH. If we see a hash rate drop of ~85% (monero’s example) after ProgPoW, It will only cost ~3x to 51% attack Ethereum and at that point, it is a guaranteed attack.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mariusvanderwijden/48/1374_2.png) MariusVanDerWijden:

> ProgPoW is essentially Ethash with some additional math thrown in. ASIC’s could achieve at most the same speed up as with Ethash. The advantage is, that 6-10 months of development time gets wasted which makes it really hard to develop an ASIC.

I agree with that but how is this relevant to my concern?

---

**esaulpaugh** (2019-01-10):

If a temporary drop in hash rate is a concern then parties can take the usual steps like requiring more confirmations. Didn’t exchanges halt ETH trading, deposits, and withdrawals during the DAO hard fork until things normalized? Should be standard procedure by this point. Anyone trading things for ETH during this short window will be taking a calculated risk, which is their right.

I’ll go out on a limb and say that I’ll eat my dick if total PoW is 15% of current or less 72 hours after the upgrade. If attackers can get their shit together and be ready to mine on day 0 then why can’t honest miners?

Lastly, I’ll just say that it sets a bad precedent to avoid changing consensus algorithm over fears of people ‘not being ready’. Is 12 months not enough time? Surely the switch to proof-of-stake will be more trying than this.

---

**maxsam4** (2019-01-10):

I am just trying to convey the fact that people and exchanges should be careful around the transition time because a 51% is more likely than ever at that time.

The network hash rate will probably be back to near original within a couple of days.


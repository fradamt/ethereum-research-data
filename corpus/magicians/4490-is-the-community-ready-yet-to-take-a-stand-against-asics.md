---
source: magicians
topic_id: 4490
title: Is the community ready yet to take a stand against ASICs?
author: CryptoBlockchainTech
date: "2020-08-08"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/is-the-community-ready-yet-to-take-a-stand-against-asics/4490
views: 2111
likes: 4
posts_count: 19
---

# Is the community ready yet to take a stand against ASICs?

Any thoughts from the community in light of the $5M ETC 51% attack and what it means for Ethereum? Was this just a test and a way for someone to gain enough funds to attack Ethereum next? Even if the same attacker has no plans to attack Ethereum, the gameplan and how to execute it is now public for the next attackers to use.

We already know Ethereum mining is very close to becoming centralized with ASICs now controlling over 45% hash. Renting that extra 6% could net them billions! As we get closer to POS why would we not expect an attack like this to occur in a last ditch effort to steal as much ETH as they can before the lights go out on POW?

Devs you seriously need to consider scheduling a hard fork for an algo change when the 4GB dag size date hits later this year. This would be the optimum time to switch after their ability to control the network is temporarily gone, until they release more powerful ASICs. It will also prevent the development and release of +4GB (Innsolilicon already has released a 5GB miner) ASIC miners.

Devs no more keeping your heads in the sand hoping this will just go away. Why would you continue to risk the security of Ethereum as everyday it get’s easier for the ASIC manufacturers to 51% attack as they gain more network control? Putting mining back into the hands of millions of gamers ACROSS THE WORLD with GPUs is the safest way to ensure POW decentralization until full POS is ready.

Are we willing to risk the destruction of Ethereum with one week confirmation times? Please take action now so this never happens here.[![Screenshot_20200808-162138_Brave](https://ethereum-magicians.org/uploads/default/optimized/2X/2/20c67965eb3c12de9ed0f931b6e61b9cd3a91134_2_690x249.jpeg)Screenshot_20200808-162138_Brave1071×387 53.5 KB](https://ethereum-magicians.org/uploads/default/20c67965eb3c12de9ed0f931b6e61b9cd3a91134)

UPDATE: Coinbase has just set transaction times at 2 weeks for ETC. https://cryptoslate.com/coinbase-delays-ethereum-classic-transactions-after-two-51-attacks/

It is my opinion that those at the top controlling BTC hash power (in China) will want to remain at the  top as the leading Crypto. This puts a large target on Ethereum as it gains widespread traction and potentially overtaking BTC. History might show someday how the one Crypto that had the biggest potential to surpass BTC was eliminated by their own short sightedness in network secrurity when they had plenty of warnings and time to act.

## Replies

**elliot_olds** (2020-08-15):

How does the ETC attack at all suggest that making the algorithm more GPU friendly will help avoid attacks?

The ETC attack was not instigated by the normal ETC miners, but with a rented hashrate. With a more GPU friendly algorithm, the attacker still would have been able to rent the hashrate.

In general, rentable GPU capacity will be higher than rentable ASIC capacity because there are so many GPUs on the rental market.

This attack happened because ETC’s mining rewards were low, and the attacker noticed an imbalance in the required confirmation time of exchanges as compared to the cost to rent hashpower on ETC.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lirazsiri/48/2819_2.png) lirazsiri:

> It is likely that the proceeds from the ETC 51% attack are being used to fund preparations for an attack on a much larger scale on Ethereum

This seems very unlikely to me, because the ETC attack seems like a crime of opportunity motivated by the extremely low ETC mining rewards. Are you interested in making a bet about whether a similar attack will occur in ETH before the end of the year?

---

**CryptoBlockchainTech** (2020-08-16):

The way the ASIC companies work is simple. First, the company starts up, does some minimal amount of setup work and figures out its plan, and starts taking preorders. These preorders are then used to fund the development of the ASIC, and once the ASICs are ready the devices are shipped to users, and the company starts manufacturing and selling more at a regular pace. ASIC manufacturing is done in a pipeline; there is one type of factory which produces the chips for ASICs, and then another, less sophisticated, operation, where the chips, together with standard parts like circuit boards and fans, are put together into complete boxes to be shipped to purchasers.

It’s obvious that ASIC production is fairly centralized; there are something like 10-30 companies manufacturing these devices, and each of them have a significant level of hashpower. First of all, one might ask, why is it bad that ASICs are only produced by a few companies and a quarter of them pass through one factory? CPUs are also highly centralized; integrated circuits are being produced by only a small number of companies, and nearly all computers that we use have at least some components from AMD or Intel. The answer is, although AMD and Intel produce the CPUs, they do not control what’s run on them. They are general-purpose devices, and there is no way for the manufacturers to translate their control over the manufacturing process into any kind of control over its use. DRM-laden “trusted computing modules” do exist, but it is very difficult to imagine such a thing being used to force a computer to participate in a double-spend attack.

With ASIC miners, right now things are at a point where they will soon, if not already, control more than 51% of the Ethereum network security. ASICs are produced in only a small number of factories and they are controlled by a handfulof people in disparate data centers and central warehouses.

This was all taken from a blog post from Vitalik in 2014.

---

**elliot_olds** (2020-08-16):

That all seems just like a summary of all the standard arguments for ASIC resistance.

The point is: what specifically about the ETC attack makes the anti-ASIC arguments stronger? This thread seemed like it was based on that premise, but as I described above I don’t think it makes sense.

---

**CryptoBlockchainTech** (2020-08-16):

It is very simple,  I thought I laid it out very well above.

- In 2019 it was determined ASICs were 40% of the Ethereum hash
- It is estimated now that number is 45%
- As we approach both the 4GB deadline and POS the ASICs will have less to lose in attacking the network

Why are we even debating network security when it is happening right in front of our eyes with our sister chain. What did the attackers lose versus what they gained?

---

**timolson** (2020-08-16):

ASIC miners have a *huge* sunk cost in the success of the blockchain they mine.  If anything, it is GPU-favoring PoW’s that are subject to this kind of “rental attack.”  GPU miners can switch coins at will, and if they trash a coin, their hardware is still valuable.  There is no “defection as the final step of prisoner’s dilemma” with ASIC’s, only with GPU mined PoW’s.

IMO, ASIC-friendly PoW’s are clearly the most secure.  Source: I’ve developed CPU, GPU, and ASIC miners for multiple coins and operated them at industrial scale since 2014.  I have deep technical knowledge of many PoW’s including ProgPoW, Ethash, CryptoNight, RandomX, Cuckoo Cycle, and Equihash.

---

**CryptoBlockchainTech** (2020-08-16):

And like clockwork the ASIC supporters come running when they think Ethereum might actually live up to what it put into it’s yellow paper…“ASICs are a plague”. I have also used ASICs only so I could understand them and see why they are so hated. They are a losing proposition for retail buyers as the faster more efficient miners are sold in bulk to warehouse miners.

Your argument about GPU miners is primitive and clearly demonstrates your lack of understanding of the demographics of GPU miners that encompasses a wide range of miners from gamers to hobbyists to professsionals.

You still have not addressed the whole premise of my argument:

- You can no longer argue that there is not a viable risk/reward when attacking Ethash as shown by the multiple recent highly profitable attacks on ETC. Miners are still mining collecting payments, albeit with 2 week confirmation times
- You have not countered my argument that the risk/reward will dramatically fall as we approach 4GB and POS deadlines. For example what would ASICs have to lose a week before 4GB miners fall off if they attack ETH and make off with 40K ETH or $17M? This is assuming they pull all their miners off for a week to start a new private chain and then introduce it back to the main chain with over 51% hash. But they could actually be mining the new chain now with very small hash and when they are ready they could roll back ETH weeks or even months. Why are you sooooo supportive of ASICs understanding the risks we are now facing?
- You are also going against one of the founders of Ethereum. He clearly points out the economies of scale and why ASICs have a clear cost advantage. He saw this even in 2014 long before BTC became extremely centralized. On Mining | Ethereum Foundation Blog

---

**lirazsiri** (2020-08-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> That all seems just like a summary of all the standard arguments for ASIC resistance.

Sorry Elliot, I’m a bit confused. Are you discounting “all the standard arguments for ASIC resistance” or do you agree that there seems to be a fundamental incompatibility between ASICs and decentralized PoW?

FWIW, I agree that there are other ways to benefit from economies of scale running on general purpose hardware, but are you disputing that ASICs make the problem worse? Especially right before a transition that fires the miners?

I realize in any debate it’s possible to manufacture sophistic arguments that sound superficially credible to someone who can’t think critically or doesn’t really understand the substance matter. I realize that it’s possible for a naive observer to be fooled, especially if their criteria for good governance is evaluating the issue at the level of superficial social signalling.

At the risk of appearing to be off topic, this is why I pointed out that the source of the problem with the ProgPOW debate is not a lack of substantive arguments, but a “governance” process attracted to deadlock that is shepherded by nice people who can’t tell the difference between a good argument and a bad one, or between the self interested appeals of special interests and “community dissent”.

These “community shepherds” can’t even understand how poorly served they are (and how poorly they serve us) with their intellectually dishonest post-modernist “philosophy” that pretends all arguments have an equal claim to truth and that conflict between sides with diverging interests can be solved by keeping the discussion civil and not hurting anybody’s feelings.

While it is generally preferable to avoid playing zero-sum games when possible, doesn’t ignoring game theory and misidentifying an actual zero-sum situation increase the probability of Ethereum being exploited?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> The point is: what specifically about the ETC attack makes the anti-ASIC arguments stronger? This thread seemed like it was based on that premise, but as I described above I don’t think it makes sense.

A few questions:

1. What would it take to convince you of the risk prior to a successfully executed attack against Ethereum?

If deductive arguments from first principles have not persuaded you that centralizing mining is dangerous, fine, deductive arguments aren’t for everyone. But sometimes people who dismiss deductive arguments as “too theoretical” and “requiring empirical validation” will change their minds when see a convincing example.

The ETC attack is an example of a successfully executed exploit against a chain that is for all practical purposes identical to Ethereum in everything except  the hashrate. So…
2. Is your disbelief grounded in anything other than the ETC hashrate being lower than Ethereum, in which case how high would the hashrate of ETC need to be in order to convince you?
3. Assuming ASIC hashpower exceeds 51%, what will be the highest yielding use for all that hardware right before the transition to PoS makes it obsolete?

---

**timolson** (2020-08-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lirazsiri/48/2819_2.png) lirazsiri:

> Doesn’t the “sunk cost” of ASIC miners makes them more likely to attack the network right before a scheduled change fires the miners and obsoletes their hardware ?

But how would they attack the network?  Are you assuming some bad actor already has dominant hashpower?  With GPU’s, someone can rent an attack, with almost no lead time and significantly less capital.  The hashrate can go from relatively well balanced to one player having over 50%, with nothing but a credit card and AWS account.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lirazsiri/48/2819_2.png) lirazsiri:

> Are you claiming that the availability and distribution of ASIC miners is more or less equivalent to the availability and distribution of GPU miners?

Actually I would claim ASIC’s are more widespread and have a more distributed market.  There are only three GPU providers: Intel, which only makes embedded GPU’s so we won’t count them, and then AMD and Nvidia.  By contrast, there are significantly more ASIC miner manufacturers.  People used to complain about Bitmain when the market was young, but nowadays they have strong competition.  There are many more ASIC miner manufacturers than there are GPU manufacturers.

Finally, the assumption that GPU mining is more distributed is false.

Ethereum has three miners who combined control over 50% of the hashrate:

https://blockchair.com/ethereum/charts/hashrate-distribution

Bitcoin by comparison requires at least 4 pools to collude:

https://blockchair.com/bitcoin/charts/hashrate-distribution

Whether GPU’s or ASIC’s, mining like any industry benefits from economies of scale.  The more important factor IMO is that ASIC miners are tied to the success of a coin, whereas GPU miners have no commitment.  Furthermore, GPU’s suffer from the “rental attack” security problem, but ASIC’s do not.

I’ve been arguing this for years and don’t understand why amateurs who don’t understand mining continue to think that GPU’s = good and ASIC’s = bad.  I think it’s because people dream of mining free money from their bedroom?  But that is simply not reality.  Maybe people think GPU’s = more distributed?  That is also simply false.

---

**CryptoBlockchainTech** (2020-08-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timolson/48/1445_2.png) timolson:

> There are only three GPU providers: Intel, which only makes embedded GPU’s so we won’t count them, and then AMD and Nvidia. By contrast, there are significantly more ASIC miner manufacturers.

You are making arguments that Vitalik explained in 2014. You really need to read his dissertation on mining. Then if you disagree with the founder of Ethereum, move to another coin. Preferably a coin that was not founded based on removing evil ASICs from security.

[On Mining | Ethereum Foundation Blog](https://blog.ethereum.org/2014/06/19/mining/)

“It’s obvious that ASIC production is fairly centralized; there are something like 10-30 companies manufacturing these devices, and each of them have a significant level of hashpower. However, I did not realize just how centralized ASIC production is until I visited this unassuming little building in Shenzhen, China…”

---

**lirazsiri** (2020-08-17):

OK, I deleted my earlier posts as I realized upon further reflection they were mostly using this thread as a soapbox for venting my frustrations with the process around ProgPOW and a “governance” process that is mostly powered by Twitter.

I’m going to stop contributing to this thread but for the record, I don’t buy into the argument that ASICs are good for network security, especially not before a transition that should lower the cost of renting soon to be obsolete hardware. I also believe the arguments regarding the rentability of GPU mining are credible only if one supposes an infinitely elastic supply of rented GPU power.

If anyone actually tried "putting in a credit card into AWS and renting 51% of ethash mining power, I doubt they would be able to get their hands on 100K+ idle p3dm.24xlarge instances. Not to mention that the credit card charges would fail, and way before getting close to making a dent in hashrate, the giant spike in demand would trigger various Amazon fraud systems and an prompt investigations.

To prempt the claim that the mining profits would subsidize the attack, a quick back of the envelope calculation is that renting GPU mining power from a perfectly elastic hypothetical AWS would recover about 2-4% of the costs. I am frankly surprised by the extent to which GPU mining ethash on AWS is unprofitable even if my rough calculation are wrong by an order of magnitude.

The strongest argument against ASICs is that any comparison of network security prior to transition to PoS should take into account the differences in expected depreciation of value of special purpose mining hardware vs general purpose GPUs.

At one extreme, you have a hyper optimized efficient special purpose hardware solution that may have been developed in secret, held by a handful of actors that have enough of an edge to squeeze out many other professionals.

At the other extreme, mining is done on general purpose hardware that anyone can get access to. It’s a race to the bottom with an equilibrium close to converting electricity to ETH. Some big players have economies of scale advantages, but they are milder compared with special purpose hardware, and in any case theu don’t squeeze out non-professionals that paid for the hardware anyway and may even be mining it a loss relative to the cost of electricity (e.g., kid in parents basement doesn’t mind running his GPU when he’s not playing games because he’s not the one paying for electricity).

It is not enough to believe that ASIC miners are altruistic. For the argument to work one has to suppose they are so altruistic that they would not even sell their hardware to non altruists.

Just suppose honest ASIC miners don’t attack the network themselves but instead sell off all their hardware right before their transition? Who would buy it from them, at what price? Would buyers plotting a 51% attack pay more or less than buyers plotting to scrap the devices for raw metal?

Finally, the argument that GPU manufacturing is centralized (e.g., only AMD, Nvidia being credible players) is also quite weak. GPU hardware is a competitive market and it doesn’t make sense for these companies to keep designs with big performance gains to themselves just to gain an edge in cryptocurrency mining. What matters is the decentralization of access to the hardware that computes the PoW, not the centralization of manufacturing. If centralization of manufacturing mattered then one could point back to the big semiconductor fabs like TSMC and are investing $15B to build new process fabs. For centralized manufacturing to be a problem, it would have to be economically interesting for AMD/Nvidia (or the fabs) to hold back innovative designs, and keep manufactured hardware to themselves instead of selling it to the public. Even if it was short-term profitable for these companies to do a 51% attack (and it isn’t), the collateral damage to their brand and reputation would be significant compared with brandless miners.

All of this makes the risks from custom hardware significantly higher than general purpose hardware.

FWIW, the strongest argument I’ve seen against ProgPOW is that the debate is “too divisive” and not worth it before the transition to PoS which is what we should be focusing on. That argument seems to discount the heightened risk right before the transition.

Finally, though I agree with the original poster regarding that this is a threat Ethereum should take seriously, I am somewhat put off by the blatant appeal to the authority of Vitalik, overly hostile style, ad hominem attacks, and assumptions of bad faith against the other posters here.

[@CryptoBlockchainTech](/u/cryptoblockchaintech), I sense you mean well and are as frustrated as I am but ad-hominem attacks do your argument more harm than good. Even if you’re right that the other side is not just misguided but disingenuous and downright evil. The heat doesn’t make those on the sidelines of the debate any more likely to see the light. They come across what seems like an angry person full of spite and resentment personally attacking those civil ASIC apologists. You can’t blame them for deciding they prefer to be on the side of those with good manners.

Oh and I recognize that complaining that someone else is being too aggressive is somewhat ironic coming from an Israeli person. I’m told we Israelis breathe too aggressively  ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**CryptoBlockchainTech** (2020-08-17):

Thank you for your words of wisdom. I agree that sometimes I push too hard when it comes to the discussion of ASICs on Ethereum. Probably the biggest reason for my aggressive approach recently is the amount of time miners like me that have been quietly trying to work through the development process to get an algo change that would bring back the days of mining Ethereum by regular people.

We have been trying for over two years now. Everytime we think there is progress something happens and it is once again put on the back burner. The icing on the cake was the last meeting ProgPow was discussed where Defi activists stormed into the meeting and talked rudely to others on the call. For me this is when the gloves came off.

Most of the miners I know have been with Ethereum much much longer than any of the Johnny come latelies, flavor of the month, Defi activists. It sounds absurd that people that had nothing to do with Ethereum that just recently entered can come in and sway developers that THEY represent the community and THEY will split a fork that includes an Anti ASIC algo change.

But yeah you hit the nail on the head, I am bitter. But I stick around and still try. I believe strongly in the future of Ethereum and the amazing development teams. I listen to every call with baited breath and marvel at how brilliant the whole team is. I simply care too much and want everyone to have a voice. But recently certain voices are getting more focus and at the cost of security.

---

**timolson** (2020-10-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cryptoblockchaintech/48/2579_2.png) CryptoBlockchainTech:

> You are making arguments that Vitalik explained in 2014. You really need to read his dissertation on mining. Then if you disagree with the founder of Ethereum, move to another coin.

Appeal to Authority is an unimpressive argument.  Might as well just say you don’t understand anything and must rely on others’ wisdom.

2014 is a looooong time ago and the ASIC market has changed, *matured*, tremendously.

If you want to look at some data, the Satoshi Number for Ethereum is currently 3, but the Satoshi Number for Bitcoin is 4.

https://blockchair.com/ethereum/charts/hashrate-distribution

https://blockchair.com/bitcoin/charts/hashrate-distribution

I suspect most pro-GPU people just want to mine “free money” at home and don’t actually care about coin security.

---

**gcolvin** (2020-11-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timolson/48/1445_2.png) timolson:

> I suspect most pro-GPU people just want to mine “free money” at home and don’t actually care about coin security.

I suspect you are wrong.

---

**CryptoBlockchainTech** (2020-11-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timolson/48/1445_2.png) timolson:

> I suspect most pro-GPU people just want to mine “free money” at home and don’t actually care about coin security.

I also suspect you are wrong. As a GPU Ethereum miner for over 3 years I have taken 1/2 of my coins earned to stake in Ethereum 2.0 so I can continue supporting network security on both chains.

I am willing to risk 1/2 of my coins earned, yes earned, over the last three years for a project I have a vested interest in succeeding. Just like my stonk portfolio, I only invest in projects/companies that I have done my due diligence. You are mistaken if you think mining is free money.

Like anything in life worth achieving takes hard work, long term planning, and a solid business plan. The invasion of ASICs on the network over the last 3 years threw a wrench in our business models as we were undercut by something that was promised in the yellow paper would be prevented.

If anything the inability of the GPU mining community to bring about  an algo change only underscores how truly weak the community is due to years of sub standard profitability. If you think this makes security safer, again you are mistaken.

---

**timolson** (2020-12-14):

I have also mined at scale; see my LinkedIn.  My argument is that GPU miners are mostly not like you.  They point their GPU’s to whatever coin is profitable at the moment, and they don’t really care about the communities. This has been a huge problem for smaller coins, but maybe not so prevalent for eth as the biggest GPU-mined coin.  ASIC miners, however, *must* care about their coin’s health and community, because there is no option for them to flip to another coin. ASIC miners are locked in. They’re monogamous. GPU miners don’t love you; they flip from coin to coin for the best profit that week and couldn’t care less if one coin dies.

---

**gcolvin** (2020-12-14):

Further, Ethereum’s security does not depend on the miners caring about network security per se.  Miners provide a service to the network, and will do so in pursuit of profits.  ASICs reduce the accessibility of the network to those seeking profits, and in that way can create centralizations.

Also, one can mine just to get some Ether to run dApps without needing to purchase it on an exchange.  With GPU mining that may be unprofitable, but is doable at a reasonable cost most anywhere in the world.  ASICs can be orders of magnitude more powerful than GPUs, are too expensive for most people, and may not be so ubiquitous as GPUs.  This is a different sort of security - it insulates Ethereum from the issuers of bank and government fiat.

---

**CryptoBlockchainTech** (2020-12-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timolson/48/1445_2.png) timolson:

> ASIC miners, however, must care about their coin’s health and community, because there is no option for them to flip to another coin

Last time I checked ASICs are sold by algos, not coins. Your argument is mute, they can mine other coins within the same algo. Unlike GPU miners they HAVE to sell everything they mine before their hardware becomes obsolete by the next miner. There is no allegiance for ASIC miners to any community or coin. They will join the next most profitable coin once their miners are no longer profitable and purchase new hardware all over again.

---

**CryptoBlockchainTech** (2020-12-24):

So anyone think this is an issue?

Current best GPU efficiency is RTX 3060 TI with 61MH @ 120W = 0.51 MH/W

Linzhi Miner ‘Phoenix’ runs 2,600MH @ 3000W = 0.87 MH/W

Linzhi is 58% more efficient!

https://www.coindesk.com/linzhi-rollout-long-awaited-ethereum-miner-phoenix

They only have 4.4GB of memory which makes them obsolete in September 2021. This tells me they have been making these for years for undisclosed customers and 9 months before the hardware design goes under they release it to the public. When are the devs going to gain respect from the GPU mining community by living up to what they wrote in the yellow paper about ASICs? Please remove ASICs so the community that has supported Ethereum from Genesis can remain here until POS. If this goes unchecked ASICs will be all that is left soon.


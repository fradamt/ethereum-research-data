---
source: magicians
topic_id: 5184
title: Five arguments against fee burning in EIP-1559
author: kladkogex
date: "2021-01-18"
category: EIPs
tags: [eip-1559]
url: https://ethereum-magicians.org/t/five-arguments-against-fee-burning-in-eip-1559/5184
views: 10131
likes: 51
posts_count: 21
---

# Five arguments against fee burning in EIP-1559

EIP-1559 has two pieces. One is a more effective auction for fees.  Most people agree that it is a great improvement.

The other piece is fee burning.   Many people oppose it.

Here are some arguments why fee burning is a bad idea.

1. Psychology.  People simply are not used to burning money. It feels unfair and wasteful.   Miners feel victimized since the network prefers to burn money vs paying miners.
2. Security.  Fee burning will immediately affect the security of the network, as the hash rate is paid by miners. Less money for miners means a lesser hash rate.
3. Fairness.  Fee burning is good for whales since it makes the price of the token higher.  Bad for miners.   So rich guys will become richer at the expense of guys that secure the network.
4. Fairness.  Small miners invested in hardware. Noone told them about fee burning.  Now they will make much less money.   Changing rules is unfair.
5. Can cause ETH to Fork.  Many miners are so unhappy, they are openly talking about forking the network.

## Replies

**CryptoBlockchainTech** (2021-01-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> Fairness. Small miners invested in hardware. Noone told them about fee burning. Now they will make much less money. Changing rules is unfair.

I will add a 6th.

6. Integrity. GPU miners have been getting squeezed by ASICs for 3 years, yet the developers refuse to live up to what the founding yellowpaper explains why Ethash was developed, to prevent ASICs on the network. GPU miners invested in hardware with the expectation that ASICs would not be allowed on the network. 1559 just further agitates the miners as they see developers working with other communities to help profitability. The difference however it is written in the yellow paper that Ethereum opposes ASICs.

---

**ButtaTRiBot** (2021-01-22):

**Decentralization**

1. Miner will need to pay the base_fee for their payouts - Do you think it would attract more small miners, thus decentralize the network, by saying “You now need to have 0.1x ETH to get your 0.1 eth payout” ?
2. Mining will not be borderless. Miners will need to have $x to cover the base fee at least. Mining is the only way to introduce new users into the ethereum ecosystem without KYC. Let’s not forget all the countries where KYC’ing is not as easy as in priviledged parts of the world like the US/EU.

**Security**

1. The current hashrate is pretty much distributed. Around ~50% of the hashrate is currently non-asian.
The EU/US hashrate has been growing faster than the Asian hashrate by a factor of 2 on Ethermine, which provides the largest non-asian hashrate. [Compare here yourself]. Due to cheaper electricity prices in Asia, we can assume that with 1559, mining will centralize towards china.

9.1.  An emergency merge to Ethereum 2.0 does **not** come without [compromises](https://i.imgur.com/2JvsdB9.png) and will come with worse UX - exactly what 1559 is trying to solve.

[@MicahZoltu](/u/micahzoltu) states in his [post](https://hackmd.io/S6kW1MjvT8-SjmaoZTyaJw?view#Reducing-pay-of-miners-will-cause-them-to-revolt) that an emergency merge to Ethereum 2.0 if miners are malicious is a valid plan, but in reality it is not and wishful thinking at best.

If such plan would be valid, then there is no reason to wait and we should merge ASAP.

---

**kladkogex** (2021-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buttatribot/48/2888_2.png) ButtaTRiBot:

> an emergency merge to Ethereum 2.0 if miners are malicious is a valid plan, but in reality it is not and wishful thinking at best.

Well - Satoshi Nakamoto has given us all a beautiful algorithm that worked perfectly and securely.

ETH 2.0 is a new thing and I wish for it to end up as successful as Satoshi’s genius, but it will take many years for it to prove security.

In the meantime, if someone tries to forcefully kill PoW clearly there will be people that will keep on mining PoW. Some people will think the old thing is better, some people will think the new thing is better.

Some super clever people will put eggs in both baskets,  which may be the most rational thing to do.

---

**ButtaTRiBot** (2021-01-22):

Valid concern, what do you think?

> Has no one raised argument that fee burning might put ETH at SEC radar? This is nothing more that stock buyback to increase value for investors. Commodities don’t decrease their supply. Securities territory.

https://twitter.com/BastardTrader/status/1352617828860489732

---

**AFDudley** (2021-01-22):

Burning isn’t a stock buy back. ETH is clearly not a stock (we can argue if it’s a different type of security, but at this moment it’s not considered one in the US or any other jurisdiction I’m aware of. IANAL), it’s a nonsense argument.

---

**rovdi** (2021-01-23):

Just a thought:

Fees in block reward does not create new ETH, it transfers ETH from one participant to another (miner), now miner can use that ETH to interact with network, in some sence this increase velocity.

**Is it possible that by burning fees you can  end up with no supply for network activity?**

When incentive to keep is greater than to use what is the point of network?

I’m not against nor for 1559, what bothers me is  all this greed in $ terms,  wrong values, wrong focus, not clear goals.

Let me ask you all:  “describe in one sentence, what is ethereum goal? ( what does it trying to achive? What need it is trying to satisfie? what problem does it trying to solve?  For whom it is trying to solve this problem?”)

---

**Mike81** (2021-01-23):

Don’t worry, once Ethereum is unmineable by the public all the miners will switch to another coin. Ethereum will never be as big as it was and it will just be another low edge crypto coin. The miners make it what it is worth today and I know me as well as over one thousand others will have no problem switching to another profitable coin to mine and drive that coin up in price. Big mistake for Ethereum… BIG mistake.

---

**ButtaTRiBot** (2021-01-23):

Sharing this here as well. Transparency for transaction submitters matters.

[![Discord_2021-01-23_18-00-11](https://ethereum-magicians.org/uploads/default/optimized/2X/e/edfce5562186fdab3da7886c3a464cc8de143982_2_690x314.png)Discord_2021-01-23_18-00-111369×623 105 KB](https://ethereum-magicians.org/uploads/default/edfce5562186fdab3da7886c3a464cc8de143982)

---

**mdalembert** (2021-01-24):

There are also some arguments against fee burning (or even against the proposed auction model) from the point of view of the transaction user (see the main EIP-1559 thread for more of the background): The base fee imposes a floor on the gas prices paid by end users, which could create further upwards pressure on the already expensive transaction prices.  The magnitude of this upwards pressure doesn’t seem to have been quantitatively modeled in the existing simulation notebooks (probably as a result of it being an explicit non-goal of this proposal to minimize user transaction costs, despite what many people seem to think around the internet).

Effectively, fee burning acts as a transfer of value from the transaction user to the ETH holder, which brings me to another major counter-argument (acknowledged by the EIP-1559 proposal text itself): It precludes fixed supply, making the inflationary behavior of the currency even more difficult to predict with this proposal.  I don’t question the utility of a progressively deflationary monetary policy (like Bitcoin’s) as means to preserve the value of the currency, but this way of doing things seems like a bit of a gamble to me (as it might to other investors), since it’s basically impossible to predict beforehand whether the fee burn will exceed the block reward or not (The modification other people have suggested of banking and redistributing base fees would address this problem).

---

**rhubbard-nwf** (2021-02-02):

Hell, if ETC brings PROGPOW on line to stop the ASICs, as well as a few other items, we may have a real winner

---

**rhubbard-nwf** (2021-02-02):

#4 - Yes. Our investment in hardware was substantial for us, even though its a small operation, all things considered. We mine because we believe in ETH and want to contribute how we can, and to earn of course. To know that ETH devs just change the rules and potential destroy our ability to break even, with no warning, just to ram a fix in to resolve a long standing issue, WHILE also working on ETH2 is quite concerning and without regard to the little guys securing and facilitating the chains.

---

**esaulpaugh** (2021-02-04):

I must warn that bad arguments against fee burning (or anything else) will only serve to make people more certain of its harmlessness, because after a period of time they will understandably assume that the best opposing arguments have already been made (and those weren’t very good).

---

**kladkogex** (2021-02-05):

Well  - the statement is emotional ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

**First**, it assumes that “people” exist.  It is an undefined set, usually equivalent to “people I like”

**Second,** it assumes that “people” are already certain that “it is harmless”.

This is by default an *unsubstantiated statement*, unless there is  an independent poll proving this.

**Third,** the only poll that exists shows the majority of miners think it is not harmless.  Unless miners are not considered to be people ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**esaulpaugh** (2021-02-05):

I don’t think there is any evidence that, upon hearing an argument he knows to be bad, a person will be unaffected or allow the argument to nudge him towards his opposition.

I guess if the function is only to rally the troops (i.e. solidify existing support) then it might do that. But again, if the troops know it to be a bad argument, will it not fail to rally them?

All five of your arguments boil down to miners and their reduced profitability. So it’s one argument and one that’s entirely anticipated.

I personally think that Ethereum’s user experience is so horrible that miners have it quite good compared to users. So a tradeoff between the two makes sense.

Not to mention that miners have benefited from multiple years of delay in proof-of-stake, and they may well see multiple years more. If I were them, I would be focused on getting the Ethash replacement done, which has been unfairly delayed and unscrupulously maligned for far too long.

---

**CryptoBlockchainTech** (2021-02-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/esaulpaugh/48/1373_2.png) esaulpaugh:

> If I were them, I would be focused on getting the Ethash replacement done, which has been unfairly delayed and unscrupulously maligned for far too long.

We have been trying but there always seems to be more important discussions and just mentioning 1057 or ProgPow sends people into uncontrollable epileptic seizures. [Ethereum Core Devs Meeting 105 Agenda · Issue #241 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/241#issuecomment-769444358)

We really need a Dev to create a new EIP for Ethash 2.0 and start moving forward.

---

**kladkogex** (2021-02-08):

Hey )

I am not saying miners are the only part of ETH community.

I am just saying that every member of the community needs to be respected.

---

**Stevenans66** (2021-03-15):

Ladies and gentlement, I am the psudomous , hodl the most eth in deposit myaelf is also 1 of the miner , please could someone represent me to inform the developers that CEO refuse the form of eip 1559 as well , if he insist , then the total amount in the lockdown deposit will goes to personal wallet. Thank You

---

**YHRW80** (2021-03-15):

But to your point, why waste resurces on something POS (if succeed) will solve?

---

**hexzorro** (2021-03-18):

[@kladkogex](/u/kladkogex) cited this discussion on this new EIP proposed that maintains base fee to miners: [Median Gas Premium](https://github.com/ethereum/EIPs/pull/3416)

---

**esaulpaugh** (2021-03-19):

miner-extractable value means that miners are effectively being paid significantly more than just block rewards and fees. 1559 won’t stop frontrunning by miners but at least it can start to address the cumulative losses incurred by holders/users due to frontrunning since the network’s inception, by reducing the ever-present tax of inflation


---
source: magicians
topic_id: 5655
title: EIP-3372 - Apply minor modifications to the Ethash algorithm to break current ASIC implementations (EIP-969 resubmission)
author: mineruniter969
date: "2021-03-15"
category: EIPs
tags: [core-eips, ethash]
url: https://ethereum-magicians.org/t/eip-3372-apply-minor-modifications-to-the-ethash-algorithm-to-break-current-asic-implementations-eip-969-resubmission/5655
views: 4447
likes: 52
posts_count: 17
---

# EIP-3372 - Apply minor modifications to the Ethash algorithm to break current ASIC implementations (EIP-969 resubmission)

https://github.com/ethereum/EIPs/pull/3372

## Replies

**Lorgd** (2021-03-15):

This eip is obvious to me as the EIP 1559 will drastically reduce the incomes of miners. The likely consequence will be that smaller miners (which are the guarantee of decentralization) will leave to mine other more profitable cryptocurrencies. The other consequence is that as with the BTC, these miners will be replaced by larger players with greater computing power and in particular ASICS. The problem is a high risk of centralization of the hashrate and an unnecessary risk a few months or years before the migration of ethereum to pos. Why should we take this kind of risk? We all know that ASICS are produced in China and they generally never go outside China and they are kept by large companies. Centralizing the hashrate before going pos is a non sense because these actors could be tempted to slow down or alienate the migration to pos.

Ethereum Yellow papper by Dr. Gavin Wood: “One plague of the Bitcoin world is ASICs”. All is said.

---

**Mspy1** (2021-03-15):

Centralizing the hashrate poses key network risks and this is what EIP-1559 will achieve as most of the GPU miners will stop mining from all around the world, as a result ASICs will replace them and will dominate the ETH network’s hashrate geographically. In addition, in case of deliberate or unintended network outages, geographical centralization of hashrate will threaten the reliability of the network. To avoid this, developers should definitely be considering this proposal.

---

**FlyingFish** (2021-03-15):

ASICs were never supposed to be here according to the yellow paper. They pose serious risks to both the health of the network and to the credibility of the devs who allow them to proliferate. Breaking the current ASIC implementation would nullify all opposition to eip-1559 and bring together the Ethereum community at a time when it has never felt so toxic or unappealing.

Supporting EIP-3372 is a no-brainer - it is obviously the best thing for Ethereum.

---

**TNZ** (2021-03-16):

It’s almost weird that this isn’t part of ETH already and needs an EIP.

I always believed decentralization and anti-ASIC should be part of ETH. What even took ETH so long to start noticing this problem?

---

**Lorgd** (2021-03-16):

I would add that with eip 1559, the network difficulty should drop significantly (20% ? 30% ? It is hard to say). Right now, it requires around 100 000 asics to take the control of the network. But the number of the required asics to do so could be much less after eip 1559. We do not know the pourcentage of asics which is currently on the network but it could be 10 or 20%, maybe more, and we do not know who is using them. The cost to produce an asic is not so high (few hundreds dollars…) comparing with the price tag (thousands of dollars…) and it means that for less than $100M and with the current difficulty it would not be impossible to take the control of the network. What about after eip 1559? Maybe for less than $50M an asic manufacturer could do so. It is easy to check how bitmain could have influenced the btc. It is not impossible to see a large chinese tech company able to produce enough asics and taking the control of enough etash power. I hope it won’t happen and I hope I am wrong but Eip 1559 is putting at risk the security of the network by reducing the mining profitability suddenly and forcing small and average miners to leave to other cryptos. This move could be accelerated very fast if the number of asics is also increasing while the profitability is going down. A large number of individual miners with a small hash power each is the guarantee of the decentralization and of the eth to be able to go pos in good conditions. I know this is full of assumptions but this risk is real…

---

**nevahash** (2021-03-16):

We must take care of miners to keep the system descentralized. Ethereum has a very strong potencial but we need to make sure we keep the main essence of DEFI. ASICs will make the chain corrupted and this will break the original purpose of the proyect.

---

**TNZ** (2021-03-16):

Here’s a link to a previous discussion on this topic.

[While using PoW, should the Ethereum network be secured primarily by GPU miners? - EIPs / Core EIPs - Fellowship of Ethereum Magicians (ethereum-magicians.org)](https://ethereum-magicians.org/t/while-using-pow-should-the-ethereum-network-be-secured-primarily-by-gpu-miners/4230/2)

---

**karmakazi** (2021-03-17):

There was never a real threat of a 51% attack by miners. If the Ethereum network is actually vulnerable to the call to action of a YouTuber, wouldn’t you like to know it? I sure would.

A “show of force” may not have been the best choice of words, but it’s now become a sensationalized snippet that’s been taken out of context of the larger conversation and used to undermine the point and smear the character of the people involved.

In light of the potential shift in hash power that could arise out of upcoming EIPs and other events, it’s really obvious that the giant pools of ASICs are a far more dangerous threat than the thousands of independent GPU miners.

---

**Lorgd** (2021-03-17):

Because one or two gpu miners influencers claimed on a youtube video for a “show of force” you think you could state that all the gpu miners will join them and are now like the ennemies of the ethereum network and its users? I am sorry but to affirm this is totally wrong and as childish as this call to concentrate the hashrate. It is impossible for gpu miners to organize them like this due to their numbers.

I am an user but also a miner and not a single miner I know will do that because they have no interest in doing that, they were even not aware about this call. All of them are also long term ethereum holders (like most of miners) and using ethereum everyday. All of them are in favor of eip 1559 as the current fees are too high for the small transactions. They are also ethereum stakers on 2.0. Outside the social networks, there is something called the real life with real people. The noice on the social networks is not reflecting the real life at all.

I never purchased a single asic because it is not in the philosophy of the ethereum to allow them. I could because my current hashrate something like 28gh/s so it could be more profitable for me but I just always refused to do that like all the miners I know. The gpu mining is the key of the decentralization because everybody can mine it, you do not need thousands of bucks to do so. The high number of miners is the guarantee of the security of the network.

I am affraid that eip 1559 is putting at risk the network by reducing the profitability of the gpu miners which can easily move as you said. 1 or 2 years ago linzhi asics and innosilicon ones (a11 is still not available for purchase and maybe will never be as they probably keep them for thei own use) were not as powerful as now and are more and more efficient.

I am not 100% convinced by eip 3368 because it goes against the deflationnist strategy and as holder i am in favor of this strategy. But I am 100% convinced that if asics are ejected the profitabily of gpu miners will be sufficient to keep them on the network, keep a decentralized network and avoid a 51% attack. As a staker I also want the eth to go to pos in good conditions (without a fork). Asics ethereum companies are against pos because all their business is based on mining and they have enough power to slowdown the move and maybe to avoid the migration. Ehereum network wil be the first network of this size to move to pos so why we should take a single risk?

---

**nevahash** (2021-03-17):

We must keep it invariably? We cannot move towards ASIC minning if we want to mantain some main features than make ethereum the most usefull blockchain ecosystem. Miners are free they can change algo and begin minning another thing show of force is more likely to be a show of commitment couse they want to keep riding in eth they don t want to change that. Is natural to disscus about EIPs when these can break with the systems minners are keepin safe from the beginning.

---

**Lorgd** (2021-03-17):

Maybe because pos was far from happening at this time. We are in 2021 now and pos is only few months / years ahead. If nothing is changing and the situation is confortable for all the miners, there is no reason for them (particularly for asics miners who are centralized) to do anything and to fight against changes.

The closer we get to the migration date to pos (which is not in the interest of the miners in general if they are not holding but it is worst for asics manufacturers and owners as they cannot resell them, etc.), then the higher will be the risk. I would like to know why these companies are still investing in asics if they know it will go pos soon? Why they are almost not selling a single asics they manufacture? Do you really think they will accept migration to pos without trying anything to save their business which is only based on etash asics? Maybe yes, maybe no, nobody knows.

GPU miners, due to the decentralization of the gpu hashrate, will never be able to organize themselves and to fight against the pos migration. That is a good thing. Moreover their hobby or business is not over after that, they can move to other cryptos or resell their equipments. Keeping GPU miners and avoiding ASICS is an efficient way to reduce the risk of centralization in the future and avoid delay in pos migration or a possible fork. Pos is required for ethereum that’s a fact, same as EIP 1559, but this transition must be done in a secured way and avoid any organized resistance, any risk.

---

**stoniestfool** (2021-03-17):

You have already displayed your ignorance in other eth forums. You should just give up or at least learn what your talking about and make educated points.

---

**Xenzen** (2021-03-19):

I do not see any improvement since EIP-969. ASICS are not an issue with centralisation, mining pools mining 40% of blocks are.

---

**Passingby1** (2021-03-30):

There are two sides to every coin, on one side, there are the mid to big sized farms opposing EIP-1559 under the threat of massively reduced income, on the other hand, there are the big bag hodlers poised to become validators that want to enforce EIP-1559 at all costs because it will, or maybe not, send their holdings straight to the moon, that’s the real reason, not efficiency but increased value.

Frankly, the EF, the devs, have made one lousy job in communicating what EIP-1559 is all about and what consequences it really entails, in the process they have pitted parts of the community against each other, while they have made it not enough clear that ETH 2.0 is still a very long way and that mining will not really go away before that.

And topmost, they have put de-centralization at risk.

What is the result? Everybody has forgotten what Cryptocurrencies are all about, every argues about this or that and don’t pay attention to those already in place, centralized for the most part, alternate blochains that pose an actual threat to Etherum.

I’m all for this proposal, take power away from asic farms, it delays the inevitable move to a more centralized blockchain and keeps the mining that comes from the actual community going for a while longer.

And yes, don’t kid yourselves for a minute, a blockchain relying on a handful, a lot of validators, especially those with an entry fee as high as what it is proposed for ETH2, will be a more centralized blockchain. It’s as if nobody hasn’t learned anything from the Bitcoin history and ASICs.

---

**Denis** (2021-03-30):

The whole reason for this proposal is that GPU miners put their profits ahead of the interests of the community and investors - that’s all.

---

**C_Miller** (2021-04-05):

**4 Reasons why the community needs to support this EIP**

1. ASIC’s will become junk after the transition to ETH 2.0/Prevention of E-Waste.
Crypto already has a bad reputation with the environmental community, due to how much it pollutes the environment, we shouldn’t give them another reason to hate us. Once the network transitions to POS those machines will become E-Waste and will further damage the reputation of Ethereum. If we were to show these giant companies we are willing to fight against the creation of E-Waste/ASIC’s it will discourage them from continuing with their plans.
2. Prevention of ASIC domination of the network.
As it stands difficulty is rising at speeds never seen before. ASICs have the advantage in high difficulty environments compared to GPU’s due to there vastly superior efficiency. At the rate at which difficulty is climbing, GPU’s will begin to become unprofitable on ETH. THIS. CAN’T. HAPPEN. Once GPU’s start falling off the network it will leave Ethereum in a vulnerable state, a 51% attack is more than a possibility at that point.
3. ASIC manufacturers don’t care about ETH.
They have a well documented history of bullying people in the community and some of the Devs back when 969 gained traction. The only thing these companies care about is how much money can they squeeze out of the network before the well dries up. As these companies have shown a blatant disregard for both community members and the Devs, who put there heart and soul into this project, we need to come together as a community and show them that, as that one guy said in Spiderman 1 (2002), “You mess with one of us, you mess with all of us.”
4. Not passing this would be hypocritical.
Ethereum’s yellow paper clearly spells out that ETH is supposed to be a GPU mined currency and shows utter disdain in the fact that Bitcoin has allowed ASIC’s to dominate its network. Mining difficulty has already multiplied by 3. At the rate it’s going we could see ASIC’s quickly take over the network within the next 4-6 months.

There is **zero** reason why everyone shouldn’t support this EIP. Most arguments against it in this forum are not against the EIP itself but those of us who secure the network. Ever since that small mining tuber called for a show of force by the community, miner hate has grown, exponentially. All I ever see anymore in any forums for Ethereum, or related projects, are people bashing miners. Hate in the community is at an all time high and that’s something we should be striving to get away from.

We are all in this for one thing and one thing only. **OUR FUTURE.** Let’s make it a bright one instead of a future filled with hate. Long live Ethereum!


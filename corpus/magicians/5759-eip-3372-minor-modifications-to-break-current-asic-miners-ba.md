---
source: magicians
topic_id: 5759
title: EIP-3372 Minor Modifications to break current ASIC Miners (Bad Actors who threaten Ethereum)
author: mineruniter969
date: "2021-03-19"
category: EIPs
tags: [eth1x, mining]
url: https://ethereum-magicians.org/t/eip-3372-minor-modifications-to-break-current-asic-miners-bad-actors-who-threaten-ethereum/5759
views: 3447
likes: 4
posts_count: 7
---

# EIP-3372 Minor Modifications to break current ASIC Miners (Bad Actors who threaten Ethereum)

ASIC Miners have become a threat to the future of Ethereum and a hard fork is required to remove them from the network before additional damage is caused. EIP-3372 proposes the minimum necessary to do so and will not affect ETH stakeholders or the network like Ethash 2.0 would. The threat ASICs pose is legal, social, moral, technical, monetary, and environmental. As we continue to come closer to the merge ASICs will attack the network and the developers personally as they have done in the past because miners will always pursue profits.

Legally and socially ASIC’s have previously been a threat and a nuisance. As Hudson describes Linzhi attacked the EF and developers personally seeking to spread lies and misinformation while sending legal threats during discussions around EIP-1057. His account is [here](https://github.com/Souptacular/linzhi) and in his own words

> ASIC manufacturer Linzhi has both pressured me and told lies

With their attacks and harassment on staff demonstrated in the below image:

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a233855c5354e24603fb11f8f32c269ce972d73e_2_690x472.jpeg)1946×1332 308 KB](https://ethereum-magicians.org/uploads/default/a233855c5354e24603fb11f8f32c269ce972d73e)

Socially and morally the Ethereum community must adopt a no-tolerance policy towards personal attacks on its developers. It is only because of the core developers that Ethereum has value, the community cannot allow large companies free reign to attack them personally and must seek to protect each developer as they are a resource that keeps Ethereum viable. Multiple developers were “burned” during this event. As we accelerate the merge, it is likely that ASIC companies will repeat their actions and again attack the developers personally while pursuing legal options. This is seen not only by their actions during EIP-1057 but recent discussion around EIP-969 where legal threats from them caused the champion of that EIP to dropout and forcing me to submit this EIP anonymously. Ethereum cannot allow its actors to be threatened without consequence and this is a fight that must happen now while they are weak rather than pre-merge where they are stronger which will result in a delayed merge and hurt the value of Ethereum.

ASICs have the greatest incentives and resources to commit bad acts because they are centralized in farms this is why Vitalik designed ETH to be Asic-resident because Asics had ruined BTC’s principles of decentralization. Each day their power and control over the network grows. ASICs are against the founding principles of Ethereum which promotes a decentralized system run by common people, not a single owner of large warehouses. F2Pool which consists largely of ASIC farms has become the #3 largest pool controlling around 10% of hashrate. Their farms can be viewed on their webpage. In November 2020 they were 23TH/s yet today they are 45.6 TH/s. That’s a doubling in 4 months and their growth is accelerating as additional ASICs come online. ASICs are becoming a threat that will soon dominate the network and action must be taken now to head them off.

ASICs on F2Pool have long been known to be “bad actors” on the BTC network. They are known for market manipulation and dumping BTC to manipulate prices (I could not post the source link as this is a new account). What will these ASICs do once they find out that they are about to lose millions prior to the merge? Ethereum is not just a network it is a community and they will use their financial resources and pour millions into delaying the merge as they launch legal case after legal case. They will attack the developers and the community as they seek to squeeze every last dollar.

The reason Ethereum was founded on the principle of being anti-ASIC is because Vitalik had seen the damage ASICs had caused to the BTC network as they pursued profits rather than the betterment of the network. GPU miners are decentralized and disorganized which makes them a much lower threat than warehouses under one central corporation that is outside the legal system and thus cannot be held to account for bad acts.

EIP-3372 also works to protect the environment. Post merge, gpus will go into the secondary market or move to other coins. However, ASICs will become junk. As more ASICs are produced, Ethereum increases its environmental footprint. These ASICs are being mass produced in greater numbers despite it being public that the merge is being accelerated. It is clear that these ASIC manufacturers and buyers must either be ignorant of the accelerated merge or plan to delay it. Because they dump their ETH they have no stake in the network except the money they can squeeze from it and if by making trouble they can give themselves another day than they will do it.

Finally, Ethereum has always sought to pursue “minimum issuance”. By reducing the amount of miners that can pose a threat to the network, Ethereum also decreases how much it needs to pay for protection. Some EIP’s are being prepared to increase miner incomes post EIP-1559 should a threat appear. EIP-3372 eliminates the need to pay more for security and allows miners to be paid less without compromising the network’s security. As we go forward closer to the merge, the community must reduce attack vectors so as to reduce the cost of the merge itself and maximize the security of the network. The community already pays too much for protection and by reducing threats we can reduce this cost. ASIC warehouse farms are dumping all the ETH they make which is suppressing the price of ETH. Although rare, several individual GPU miners are taking part in staking or have gone on to join the community in development or our financial endeavors. They thus are more valuable to the community than a warehouse of future junk. There is no need for the Ethereum community to continue to pay for soon-to-be obsolete hardware that will end up in landfills.

Technical Explanation:

Ethash 1.1 will replace the only FNV prime with five new primes at the stage of the hash computation. The prime used for the DAG generation is remained unchanged, while all others are be changed. This will not prevent ASIC companies from creating new ASICs that adapt but so close to the merge it is unlikely they will do so, and even if they do they are unlikely to be able to produce enough to again be a threat.

The choice of FNV constants are based on the formal specification that is available on [https://tools.ietf.org/html/draft-eastlake-fnv-14#section-2.1](https://ietf)

We apologize for the delay in submitting the justification for this EIP. As the community may or may not be aware, the original champion was forced to stop working on this EIP due to legal attacks from ASIC companies. It has taken us this long to review his work and find a new champion. To protect ourselves we are submitting this anonymously and would request the community’s aid in our endeavor to maintain our anonymity and some lenience given the circumstances and threats we face pursuing this EIP.

## Replies

**timbeiko** (2021-03-19):

On AllCoreDevs 108 today, we rejected both EIP-3368 (block reward increase) and EIP-3382 (hard cap the block limit) because they both were solutiuons to potential issues with 1559, and we agreed that if any such issues come up, we’d address them then. I suspect this EIP falls in a similar bucket: good idea if ASICs attack, but unlikely to be implemented before.

---

**esaulpaugh** (2021-03-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mineruniter969/48/3501_2.png) mineruniter969:

> Socially and morally the Ethereum community must adopt a no-tolerance policy towards personal attacks on its developers.

Ludicrous. In a forum for a project supposedly created for the sole purpose of censorship resistance. In my first act of disobedience, I will make an assertion about your sexuality in an insulting way. You are gay.

Just activate Ethash 2.0 and be done with it (yes, I’m referring to the P word).

And I would argue that ASIC miners have a greater stake in the network than GPU miners, because ASIC miners can really only continue mining on either Ethereum or Ethereum Classic. But the point of Ethereum Serenity is to reduce miners’ stake in Ethereum to zero. So I prefer miners who have less of a stake because it is that very stake that, being backed into a corner, will cause them to 51% attack. Rip off the band-aid – replace Ethash.

---

**papajo-r** (2021-05-17):

It is no wonder with how you phrase yourself in this post that you might get censored from time to time, you have freedoms yes but they stop where other people’s freedoms begin you cant just insult people because you want to do that.

ASIC miners due to the way they are distributed are going to centralize the network (first the manufacturer himself mines with them and then he releases them to the “public” only caviat is that due to how this networks work and due to the price the single individuals that are going to end up with an ASIC will be the vast minority mostly wales will call dips by flashing their huge cashflow and buy in bulk)

“traditional” miners also consist of big wales only that in this case the majority of them are people that make ends meat or medium sized people/entities that invested on ETH and thereby sealed its success.

without the miners ETH wouldnt be on the chart and dismissing them that easily just to centralize it to a few entities not only may bring the future of ETH at risk (marketwise) but also is dishonest and self destructing what ever fortunes you people may have because of ETH are made because of miners backing it.

And because miners are mostly a group of separate individuals it is wrong of them to consider them as the “enemy” or believe that they all have a hive mind (e.g your 51% attack pun) most people want just to flourish with the rest of the people that are involved into ETH (funders, traders) nothing more nothing less.

---

**esaulpaugh** (2021-05-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/papajo-r/48/3953_2.png) papajo-r:

> you cant just insult people because you want to

Sir, you are sorely mistaken. The precise meaning of freedom is that such a thing is something I most certainly can do. I suggest you consult the first definition in the dictionary. [FREEDOM Definition & Usage Examples | Dictionary.com](https://www.lexico.com/en/definition/freedom)

---

**VanwaTech** (2021-05-25):

I hugely support anti-asic initiatives

---

**VanwaTech** (2021-05-25):

RN ASIC manufactures have huge control of the selling pressure and consequently price. They exploit the markets for personal gain.


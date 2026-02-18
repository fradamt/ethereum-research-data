---
source: magicians
topic_id: 5866
title: Why should we make miners prefer the premium and hate the base fee?
author: mtefagh
date: "2021-04-01"
category: Magicians > Primordial Soup
tags: [gas, eip-1559, mining]
url: https://ethereum-magicians.org/t/why-should-we-make-miners-prefer-the-premium-and-hate-the-base-fee/5866
views: 2474
likes: 16
posts_count: 21
---

# Why should we make miners prefer the premium and hate the base fee?

In EIP-1559, all the base fee is burned and all the premium goes to the block producer. Because of this asymmetry, there is a strong incentive for the miners to make the base fee zero in order to fall back to the previously-used first-price auction mechanism.

As far as I understand, for all the different reasons discussed for burning fees, there is no difference if you are burning either the base fee or the premium. What happens if we burn x% of both the base fee and the premium? I don’t want to get into the fight about burning the fees but if you want to get the same burning effect as EIP-1559, it is enough to set x equal to the average ratio of the base fee to the total fee. Still, ETH would be deflationary, and forging transactions would be costly for miners, etc.

The difference is that because of the same x% rate, there would be no substantial difference between the base fee and the premium for the mining community. Why should we care? If 51% of miners hate the base fee so much, there is a very easy 51% attack on the base fee reverting the fee mechanism to first-price auctions. 51% of miners just bring the fee down to zero and then they will never mine more than target full blocks and collude to make any such block orphan. This is a Pareto optimal strategy for the mining community and even though it is not a Nash equilibrium, it doesn’t sound impossible considering the recent news.

In summary, EIP-1559 makes the mining community love relatively low base fees which in turn result in over-loaded full blocks and network congestion. Then let me ask again! Why should we make miners prefer the premium and hate the base fee?

## Replies

**esaulpaugh** (2021-04-02):

> Any defector from this strategy will be more profitable than a miner participating in the attack for as long as the attack continues

> ensuring the miner of a block does not receive the base fee is important because it removes miner incentive to manipulate the fee in order to extract more fees from users

https://eips.ethereum.org/EIPS/eip-1559

---

**mtefagh** (2021-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/esaulpaugh/48/1373_2.png) esaulpaugh:

> Any defector from this strategy will be more profitable than a miner participating in the attack for as long as the attack continues

That’s why I said this is not a Nash equilibrium but a Pareto optimal strategy. And it needs 51% of miners to join forces to make any such block orphan. I’m not saying that it is very probable but my point is that the symmetric structure does no harm while removing this incentive altogether.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/esaulpaugh/48/1373_2.png) esaulpaugh:

> ensuring the miner of a block does not receive the base fee is important because it removes miner incentive to manipulate the fee in order to extract more fees from users

True but at the same time, it creates the incentive to manipulate the fee in the reverse direction (make the base fee smaller) in order to extract more premium from users. The difference is that if we utilize the symmetric version, the first kinds of attacks trying to increase the base fee cannot happen because x% of the base fee is being burned and it is still costly for miners to forge transtions (your point is resolved). Moreover, the other types of attacks to decrease the base fee won’t happen because there is no incentive for that (unlike right now under the current version of EIP-1559).

---

**esaulpaugh** (2021-04-03):

As you say, improbable. And fully addressable through additional measures if necessary. That is the agile way.

---

**mdalembert** (2021-04-03):

The problem is that all of those “additional measures” have a cost to the network.  As [@mtefagh](/u/mtefagh) has shown [here](https://ethresear.ch/t/path-dependence-of-eip-1559-and-the-simulation-of-the-resulting-permanent-loss/8964) and in the main EIP-1559 thread the same safeguards in place meant to prevent miner collusion can be taken advantage of by users in order to manipulate the price, and as I have shown in my recent [comment](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/368) the delayed accounting of the base fee necessarily leads to economic inefficiency, which wouldn’t necessarily be the case if miners didn’t have a perverse incentive to manipulate the base fee as [@mtefagh](/u/mtefagh) is suggesting in this post.

In addition the “additional measure” of burning the base fee comes at the cost of roughly halving the price that an adversary needs to pay in order to 51%-attack the network, as we have discussed at length in the main EIP-1559 thread.  And more importantly, none of these additional measures remove the perverse incentive for miners to simply censor and shut down the EIP-1559 fork, which would also get the base fee out of their way but, unlike the attack described in this post, *would* be a Nash equilibrium, since defecting miners would have an incentive to join the coalition in order to prevent their block from being orphaned eventually.

---

**esaulpaugh** (2021-04-04):

Perverse incentives don’t matter if they’re overcome by non-perverse incentives. Everything has a cost; that’s not an argument.

> replacing the formula with an exponential curve (or at least a degree-2 Taylor approximation thereof) to cut that down to  roughly halving the price that an adversary needs to pay in order to 51%-attack

Again, assuming that every 12-year-old’s gtx 1060 is for rent to attackers on short notice for marginal increase in profitability is the wrong assumption

---

**mdalembert** (2021-04-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/esaulpaugh/48/1373_2.png) esaulpaugh:

> Everything has a cost; that’s not an argument.

It is an argument if the cost of something outweighs its benefits, or if someone has some idea to potentially avoid that cost, as is the topic here.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/esaulpaugh/48/1373_2.png) esaulpaugh:

> Again, assuming that every 12-year-old’s gtx 1060 is for rent to attackers on short notice for marginal increase in profitability is the wrong assumption

That wasn’t my assumption.  A 51% attack is a realistic scenario we should keep in mind given the existing mood and the historical precedent of 51% attacks on blockchains with minority hashrate – And yes, the London fork could become one of those if it fails to gain enough support from the miner community leading to a split of the network.

---

**esaulpaugh** (2021-04-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/87869e/48.png) mdalembert:

> minority hashrate

I’m pretty sure Ethereum has been and continues to be the big swinging dick in terms of Ethash-capable devices. Bitcoin had extremely compelling ideological and practical reasons to split, and Bitcoin Cash still got absolutely dumpstered. Why is past not prologue here?

---

**mdalembert** (2021-04-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/esaulpaugh/48/1373_2.png) esaulpaugh:

> Why is past not prologue here?

It could very well be, possibly with the EIP-1559 fork on the losing end.

---

**esaulpaugh** (2021-04-04):

herp derp okay. have fun creating an Ethereum Non-Classic Classic Foundation that eclipses the real foundation

---

**mdalembert** (2021-04-13):

That’s not what we’ve been proposing to do here, seems like another straw man argument from you.  The fact that the potential adversaries aren’t legally organized as a competing foundation doesn’t eliminate any of the risks the EIP-1559 fork is facing, many things can still go wrong without the adversary being officially registered as a foundation.

---

**esaulpaugh** (2021-04-14):

It would be great if a BCH or an ETHNCC (Ethereum Non-Classic Classic) could achieve legitimacy with zero git commits, zero marketing budget, zero lawyers, zero contacts at major media organizations, zero Mark Cubans, zero resources of any kind. Just pure ideology. But it is not the case.

---

**mdalembert** (2021-04-14):

[@esaulpaugh](/u/esaulpaugh), I don’t know why you keep bringing up the matter of creating a parallel network, as if it were necessary for an adversary or a group of coordinated adversaries to do such a thing in order to veto or severely disrupt the deployment of the EIP-1559 network via e.g. a censorship attack or the various base fee manipulation attacks we’ve been talking about. You’re free to go and create such a foundation if you want to but it seems fully irrelevant to this topic.

---

**esaulpaugh** (2021-04-15):

You said the 1559 fork could be “on the losing end.” That implies a winner that is not the 1559 fork. In the context of Bitcoin Cash and Ethereum Classic that means a parallel network.

---

**kladkogex** (2021-04-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/esaulpaugh/48/1373_2.png) esaulpaugh:

> Any defector from this strategy will be more profitable than a miner participating in the attack for as long as the attack continues

Well - it seems that if 51% of the miners refuse to mine on top of any branch that includes defector blocks, then defectors will lose money.

---

**mdalembert** (2021-04-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/esaulpaugh/48/1373_2.png) esaulpaugh:

> That implies a winner that is not the 1559 fork. In the context of Bitcoin Cash and Ethereum Classic that means a parallel network.

A parallel network is a possible outcome but not the only conceivable one, another potential outcome is most of the hashrate of the EIP-1559 fork transitions away from it and its security is compromised, causing it to disappear due to the user base losing confidence in it.  Or alternatively, the EIP-1559 fork could become the main network, but users and miners start gaming the base fee computation algorithm for profit to the disadvantage of most non-strategical users, reversing any of the promised usability benefits.

---

**DrDrago** (2021-04-16):

Something that hasnt been touched on, there is the possibility of miners being used for attacks without having knowledge of the attack, or the vector.

Even if you know your part of an attack, but no one except a central entity (nicehash, pools) knows the vector, nobody can defect, since nobody knows the vector, and hence nobody knows whether it is more or less profitable to defect.

Further, if this method is combined with a 51% censorship attack of any hash not following this method, it would become rational for all miners to join the attack, since the censored 49% would be making nothing otherwise.

Defectors are only more profitable if they can mine at all, if miners achieved 51% to nuke base-fee, why wouldn’t they censor the 49% not following their method? The same percentage of hash is necessary to implement both attacks, and there is no reason you cannot combine attacks.

Nicehash miners are for all intents and purposes unable to defect, given they are unable to deduce they are attacking in the first place. Pools could also rather easily implement a similar strategy that could keep their miners unaware.

Its not even necessary that they’re unaware, if you have 51%, you can shout from  the rooftops that your censoring the other 49% and only those who nuke base-fee can mine, within hours, 95%+ of hashrate would be part of the attackers, rather than be censored.

I dont see why the devs only consider single attacks on their own, combining a 51% censorship attack with the base-fee lowering attack would create a Nash equilibrium where its rational for all hash to join the attack: It boosts their profits, by lowering base-fee, AND it keeps them uncensored. In this event, only irrational miners would continue mining normally, since they would be censored.

There isn’t an easy solution once an attack begins either, nor is there a guarantee that it will be announced at all.

For example, mining clients could simply choose to implement that themselves, a large portion of hash uses closed-source mining software which could easily do such a thing while leaving miners completely unaware even. What’s interesting is its actually rational for all miners to do this, since releasing a client without that modification lowers profit for 0 gain (irrational), while releasing a client with that modification gains you more profit for 0 cost. (rational, and the equilibrium)

I wonder myself whether any mining clients at all will be released without that modification (to nuke base-fee), its not rational to release a client without the mod, (or to make one at all), so i really wonder how it turns out.

Edit: Miners can simply nuke base-fee on the EIP1559 chain, and censor anyone who doesn’t, this negates EIP1559’s effect, reverting to a base-fee auction, while not requiring a chain split… and not requiring any sort of “hostile” attack from the perspectives of the miners, from the miners perspective, they aren’t hard-forking, they are not double spending, they’re simply padding their profits for 0 cost to themselves, a completely rational choice that seems like the Nash equilibrium?

It also doesn’t require coordination as i noted before, it just requires miners to act rationally, there is no rational reason they’d release a client updated for EIP1559 without the base-fee-nuke modification. Also no rational reason miners would use one, if the alternative is available, (and it will be, probably before the EIPs hard-fork date even).

Double Edit: Miners also would not lose much by implementing this strategy, they lose even less when you consider MEV making up a majority of post-EIP1559 mining revenues.

If miners really wished to pad their profits, they could do all of the above, (censor hash that doesnt nuke base-fee, and engage in base-fee nuking), and, they could implement a minimum starting tip of their/the pools choice. (This could inflate gas prices, the minimum could be set to whatever they wished, and bidding would start there)

Mining clients or pools could also set up a system where the attack only becomes active during opportune times, such as having more than 51% of hash, and this would get around the problem of it being initially more ideal to defect if base-fee nuking begins, since it wouldnt begin until enough hash has signed on to make the attack self perpetuating (via a censorship of non-attacking hash)

Miners could also raise gas limit in retaliation and make the state growth problem 100x worse (while incurring little cost to themselves, again, especially once you consider a near majority of mining revenue coming from MEV) (and kill alottt of nodes)

---

**esaulpaugh** (2021-05-08):

so there’s a modest risk of a modestly suboptimal situation for temporary period if the majority of miners declare war on Eth. fine by me lol. risk analysis looks green across the board. 1559 to the moon

---

**DrDrago** (2021-05-08):

Considering less than 10% of hashrate belongs to pools who support EIP1559… maybe we have different ideas on risk analysis?

To me it doesn’t seem like a risk analysis to simply hope 90% of hashrate changes their minds in the next… 2 months… (after keeping their minds made up for the past 5 months and staying on their respective pools…)

But i suppose if you assume all hashrate will magically bow to your will the day of the hardfork, sure then, if thats one of your starting assumptions, risk analysis looks green af

I think people should really question whether they trust sparkpool and ethermine soo much they’re willing to bet the entire $300bn network on them 2 not colluding. (Pools are entirely profit motivated, and they can start attacks without their miners even being aware, so… what motive exactly do they have **not** to collude?)

it would only take ethermine+sparkpool+ a small 5% pool (many options) to 51% the ethereum network, the number of people who could make the attack happen can **now be counted on one hand.** (the leaders of sparkpool, ethermine, and another pool, collectively, make up 3 people. It would take the collusion of only **3** individuals to quite possibly bring down the entire ethereum network)

I also really question what people think the devs could do if a massive attack did happen suddenly, i mean short of pulling the plug on the network to prevent further damage, there isnt anything they could do immediately. They could *try* and emergency merge ASAP, but you’d be betting on everyone being ready for it with 0 testing, something which itself is a massive risk worthy of its own risk analysis. (edit: and the attack would cause extreme damage, even if it only goes on for 10 minutes. Does anyone here believe the devs can coordinate a 2.0 emergency merge within 10 minutes of an attack going live? (i mean could they even discover it in 10 minutes??))

I really wish people would atleast consider the fact that it would only take **three** individuals to attack the network, and EIP1559 provides all the motivation they could possibly need, again, pools are motivated *solely* based on profit like miners… if its profitable for them to collude in the shadows… **they will**

---

**esaulpaugh** (2021-05-10):

Is that who attacks things? Non-supporters? I haven’t seen a statement out of Switzerland saying that they support the US. Should I worry about them bombing my country?

I sure hope the Swiss change their minds to explicitly support the United States. Else they are liable to strike hard and fast.

If there was an attack, you wouldn’t do an emergency merge – you would do an emergency reduction of the block reward. That’s a one-line change which has been done multiple times before on mainnet. That’s as low-risk as it gets.

---

**mtefagh** (2021-06-04):

Yet another reason for why I think the asymmetry between the premium and base fee is detrimental to the network security. Consider DoS attack vectors such as flood attacks and spam attacks. The attacker should pay a lot of fee, including both the premium and base fee, and hence, these attack vectors are expensive. Under EIP-1559, it is enough for the attacker to pay only the sum of other transactions’ premiums off-chain and simply ask the miner to mine an empty block in return. This is a DoS attack with a tiny fraction of cost in comparison to the previous case.


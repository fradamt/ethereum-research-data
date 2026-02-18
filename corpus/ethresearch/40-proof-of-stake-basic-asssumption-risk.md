---
source: ethresearch
topic_id: 40
title: Proof of stake basic asssumption risk
author: Romanteif
date: "2017-08-21"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/proof-of-stake-basic-asssumption-risk/40
views: 4179
likes: 7
posts_count: 15
---

# Proof of stake basic asssumption risk

Hi there

I’m novice in Etherium, so probably some terminology will be not in the Etherium gurus’ jargon, never the less I’d like to rase the concern about one of the Proof-of-stake risk scenario, I’ve  found no discussion around…

The basic assumption of the PoS claims the validators are interested in the stable currency and the stable blockchain in general, so the conclusion came: “the more stake in the currency account/accounts group has the more loyal it is to the system at whole”.

IMHO, this is not always true, for example, group of people are aimed for SOME EXTERNAL REASON to compromise the currency, even with the lost of 51% of the total coins issued which will be totally lost by them, The external reason may be, for example, removing the competitor from the market or playing “short” on either that currency or all cryptocurrencies on some external exchanges. So they may silently increase their stakes in the attacked currency to get the prime validator positions when preparing external compensation mechanism outside the attacked currency and at some point of time to crash the whole network down, being compensated outside of the system.

The scenario of such a “CRASH-DOWN ATTACK” is pretty expensive, I guess, but it’s more than real in our not ideal world.

Is there any deffence against such a risk in PoS in general, and particularly in Casper?

## Replies

**MicahZoltu** (2017-08-21):

All (that I know of) distributed consensus systems protect against financially motivated attackers / make it so an attack by a non-financially motivated attacker is expensive to execute.  I believe, at the moment, the best defense there is against an attacker with money they are willing to burn in executing an attack is have a mechanism for off-chain (human) consensus.  One could consider the DAO (ETH/ETC) split an off-chain “consensus” mechanism.

---

**vbuterin_old** (2017-08-22):

The assumption behind Casper is decidedly NOT “because you need 10 million ETH to become an attacker, and an attack will seriously hurt the price of ether, so someone who actually has 5 million ETH will want to be nice”. It’s more like "because the protocol is designed in such a way that a successful attack costs 1-10 million ETH, then (i) someone will need at least a *1-10 million ETH-sized incentive* to attack as a rational actor, and (ii) someone with X ETH will only be able to perform floor(X / 1 million) attacks before they run out of money.

The incentive requirement and the capability limitation are both important.

It’s also worth noting that “attack the currency to crash the price, and profit by either being a competitor or shorting it on secondary markets” is an attack mechanism that works for *any* blockchain. There are two lines of defense. The first is to be able to recover from successful attacks quickly, making the price crash lower in magnitude. The second is to make attacks expensive. The second also contributes to the first, as if everyone knows that we can recover from an attack within a week, but an attack destroys 5% of all ether, then the attack may actually make the ETH price *go up* on net.

---

**Romanteif** (2017-08-22):

That’s what I mean. It seems the size of the in-chain stake must not be the only criterion for the validator assignment. PoS must be enforced with some other proof of loyalty, and/or with some off-chain “proof of honesty”. it may be personalisation (not anonymouse identity of the validator), some off-chain reputation measurement, In PoW systems the major miners are known and have the “physical presence” in the real world, so they can be investigated. In pure PoS anonymouse system nobody knows who the validators are and what off-chaine interests they have.

---

**Romanteif** (2017-08-22):

The quick recovery may be the brilliant approach against the crash-down attak, while raising expences for such an attack seems being not sufficient. We consider the scenario when the off-chain reward on burning in-chain stake is desired. If I am the USD multibillionair or some big bank and I need for some reason to crash the PoS blockchain down at whole, I’ll have enough funds to do it. I need as little as 51% of the total coins issued.

---

**vbuterin_old** (2017-08-22):

The general calculus of defense is: you can deter attacks if cost(attack) > benefit(attack). Strategies that increase the cost of an attack, like slashing conditions, and strategies that reduce the benefit of an attack, like quick recovery, are both useful.

It is indeed that case that if a **really** powerful entity wanted the blockchain dead, they could wreak a lot of havoc. The interesting question is, what kinds of things can we do to increase the required level of power, and level of craziness, required for such an attack to happen? That is to say, we want the size of the set of situations where the blockchain actually will get attacked beyond some acceptable threshold of service reduction to be as small as possible, even if we know that it will never be zero.

When comparing algorithm A and algorithm B, *both* algorithms have the problem that multibillion dollar governments and banks can wreak lots of havoc. So simply stating that fact gets us nowhere in terms of achieving our present goal, which is choosing between A and B. It’s more useful to try to understand how the *difference* between A and B can exacerbate or mitigate these risks on the margin.

---

**vbuterin_old** (2017-08-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/romanteif/48/21_2.png) Romanteif:

> In PoW systems the major miners are known and have the “physical presence” in the real world, so they can be investigated

This is not necessarily true. For example, right now ~50% of the miners of Bitcoin Cash are “unknown”. Also, the fact that they have physical presence means that they can potentially be attacked or coerced by real-world powers-that-be, so relying too heavily on that carries other risks.

I personally would prefer security models that make absolutely no assumptions about who the miners/stakers are and what they care about other than money, as I’d argue it’s a core principle of cryptoeconomics that we are building socially scalable systems where the “story” for why you should trust some system does not at all depend on whether you think the government of country A are good people, think the government of country B are good people, think multinational corporations are good people, etc etc; the story should only depend on the fact that we can trust that (i) cryptography works, (ii) all of the above groups like getting money and dislike losing money, and (iii) all of the above groups only have a limited supply of money that they can burn on frivolous blockchain-killing exercises. None of these three requirements are in any significant sense culture-specific, so we can rest at ease that the security model will continue working for a long period of time under a wide array of possible circumstances.

---

**Romanteif** (2017-08-22):

Absolutely!

I’d like to emphesize first, that the atttacking formula is to be analysed a little bit deeper, as follows:

cost (attak) >= in-chain benefit (attack) + off-chain benefit (attack);

where neither the attacked chain itself nor the attacked chain supporters are able controlling the off-chain part.

Assuming there is no posiibility to control the long-term trends of all the global markets hence the strategical decisions of the powerful global players about the worthiness of the crash-down attacking of their competitors, we may not build the strategy solely on the condition cost (attack) > in-chain benefit (attack), that the pure PoS is.

For a while I have no solution for that, never the less I guess the PoW (algotythm A) “as is” is more protective against such a threat than PoS (algorythm B) “as is” with 2 factors:

1. PoW is somehow less anonymous for major validators due to the possession of physical assets to play the powerfull mining position
2. PoW is supported by all the powerfull cryptocurrency communities so - may be (?!) - there is no interest to readress the computing power to destroy the competitors in comparison with the supporting their very own currency.

The conclusions are as follows:

- I’m afraid switching to PoS as it is now without solving that risk means getting unprotected against the crash-down attack from the powerful global players. PoS “as is” is too vulnerable to that threat
- PoS is to be extended with some additional, not-just-in-chain-stake condition for the validator assignment. The validators are to be somehow controlled/verified off-chain. Then PoS may definitely compete with PoW

---

**Romanteif** (2017-08-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I personally would prefer security models that make absolutely no assumptions about who the miners/stakers are

+1

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> and what they care about other than money,

Every single chain is living not in vacuum, so the interests of the stakeholders are wider than in-chain stake. The off-chain reality is to be considered whenever it influences the in-chain realm.

---

**vbuterin_old** (2017-08-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/romanteif/48/21_2.png) Romanteif:

> we may not build the strategy solely on the condition cost (attack) > in-chain benefit (attack), that the pure PoS is.

Agree. What I’m saying is that our current methodology doesn’t just try to say “ensure cost(attack) > in-chain-benefit(attack), and if we reach that point rest on our laurels and say we’re done”, it says "try to come up with an algorithm that maximizes D, such that cost(attack) > in-chain-benefit(attack) + D. Then we have D as an lower bound on the minimum out-of-chain-benefit(attack) required to make a profitable attack, and it should be clear that the higher D is, the more secure the algorithm. And I believe that PoS can achieve a much higher D.

> PoW is somehow less anonymous for major validators due to the possession of physical assets to play the powerfull mining position

This is both a benefit and a cost. PoW validators being known also means that they can collude more easily. Also, as I mentioned, it makes them more vulnerable to governmental and other meatspace actors.

> PoW is supported by all the powerfull cryptocurrency communities so - may be (?!) - there is no interest to readress the computing power to destroy the competitors in comparison with the supporting their very own currency.

This is also ambiguous. The fact that PoW is supported by many currencies actually means that it’s more likely to expect PoW miners to attack, as they might reason that if they kill one of two competitors then the other will rise in value, and so their total ability to get revenue would not decrease by much (if the miners have maximalist empirical beliefs, they will in fact say that killing one of two competitors will increase the value of the other by *more* than the value of the victim, and so their revenue will *rise*).

Arguably, the fact that a PoS blockchain has a guaranteed hegemony over its consensus-forming resource is a very good thing for its security for its reason - if the blockchain does die, there is no place for validators to run.

---

**Romanteif** (2017-08-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> …"try to come up with an algorithm that maximizes D, such that cost(attack) > in-chain-benefit(attack) + D. Then we have D as an lower bound on the minimum out-of-chain-benefit(attack) required to make a profitable attack, and it should be clear that the higher D is, the more secure the algorithm. And I believe that PoS can achieve a much higher D.

Agree. The concern is based on the measurements of D. I guess, yet can’t prove, D in the real life may be pretty high, so just raising the cost(attack) to overcome D may eliminate any possibility of recruiting validators due to the very high entrance barrier. Such a protective algorytm is to use some off-chain qualitative attributes of the validtors rather than only quantitative size of the stakes.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> PoW validators being known also means that they can collude more easily. Also, as I mentioned, it makes them more vulnerable to governmental and other meatspace actors.
>
>
> …it’s more likely to expect PoW miners to attack, as they might reason that if they kill one of two competitors then the other will rise in value, and so their total ability to get revenue would not decrease by much (if the miners have maximalist empirical beliefs, they will in fact say that killing one of two competitors will increase the value of the other by more than the value of the victim, and so their revenue will rise

Correct. PoW is also vulnerable to the crash-down attack, so any cryptocurrensy is? Theoretically even now USD can conquer or kill Bitcoin and weaker, Bitcoin can conquer or kill Etherium and weaker, Etherium can conquer or kill Dash and weaker etc…

The only Ripple is out of the threat, cos they have totally different validators assignment algorythm.

So the question is what has been preventing powerful players against implementing such an attack until now?

I hope it’s not only absense of the crash-down attack idea…

---

**vbuterin_old** (2017-08-23):

Nothing at all prevents them. I think what’s happening so far is that cryptocurrencies’ primary attackers have been either people in it for the lulz, lone wolf profit-seeking attackers, or supporters of other cryptocurrencies. The first group is not willing to pay a cost of more than perhaps a few thousand or at most tens of thousands of dollars. For the second group, *putting oneself in a position to profit from an attack* is difficult, and the larger the profit required to offset the loss the harder it is to remain undetected. For the third group, it’s also hard to spend large quantities of funds while remaining undetected, and so far not many cryptocurrency developers are *that* evil.

In the future if/when governments start getting into the game, it’ll be different, though personally I expect they’ll start off by doing things like banning exchanges; the only “front-door attack” I can see being even possibly realistic is the Chinese government commandeering Bitcoin proof of work miners or ASIC farms. But this is only true *precisely because* of the work that’s being done to guarantee that any kind of attack is expensive.

---

**Romanteif** (2017-08-23):

Well. It seems we’ve got no technical way to prevent it, neither the resources to investigate the economical model of that risk. Let’s hope there are and will be no social preconditions for the crash-down-like scenarios. We can close or delete this discussion thread, I think

---

**metabol** (2017-08-23):

The fact is that there are many attack scenarios that will definitely override the PoS . From a totally financial markets point of view an attacker or group might decide to spend a large sum to crash a system having previously set bets against the the crash by going long on the currency. If the attack succeed their profit will   be :                                                                                                                      **Bet income - cost-of-attack .**     Happens all the time in financial markets:  notwithstanding Pos is better than Pow for the moment.

---

**vbuterin_old** (2017-08-23):

> From a totally financial markets point of view an attacker or group might decide to spend a large sum to crash a system having previously set bets against the the crash by going long on the currency.

Am I understanding you correctly here? You seem to be suggesting:

(i) Go LONG on the currency

(ii) Spend $x to attack it

(iii) The attack makes the price go UP (because the market knows the coins are destroyed, and this outweighs the loss of confidence in the system)

(iv) Your long gives you revenues of $y > $x

If this scenario is plausible, then an even more plausible scenario would be to replace step (ii) with “provably burn $x”. This would be even more effective at pushing the price up, because there is no loss of confidence, it’s just coins being burned. This kind of financial attack seems plausible in *any* system as it’s totally consensus algorithm independent, and is arguably one of the limits on leverage (alongside volatility wipeout risk). If you have a consensus-algorithm-dependent attack that’s strictly less profitable than this consensus-algorithm-independent financial attack, then imo that’s not something that’s really worth worrying about.


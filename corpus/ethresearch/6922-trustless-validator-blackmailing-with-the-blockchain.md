---
source: ethresearch
topic_id: 6922
title: Trustless validator blackmailing with the blockchain
author: liochon
date: "2020-02-11"
category: Security
tags: []
url: https://ethresear.ch/t/trustless-validator-blackmailing-with-the-blockchain/6922
views: 6637
likes: 21
posts_count: 33
---

# Trustless validator blackmailing with the blockchain

### Simple attack

Hackers have a simple and rational incentive to attack validators: with the validator’s private key, he can generate slashable attestations and claim the corresponding “whistleblower” reward.

The hacker does not need to claim the reward immediately. So if he finds a zero-day attack on an eth2 client, he can quietly exploit it on all the validators he can find on the network, collecting all the private keys before claiming all rewards at the same time.

As the victim, if you find out you have been hacked, the optimal strategy is to slash yourself as fast as possible and claim the whistleblower reward --the staked funds are lost anyway.

The hacker’s whistleblower reward is limited (~0.05 ETH, ~€10), but already interesting if you can hack a few thousand validators.

### Blackmailing

As the cost for the victim is high (from 1 to 32 ETH). The attacker can use a blackmailing smart contract to increase its profit. Rather than slash the victim, the attacker extorts the victim. The deal is secured with the smart contract so the attacker is paid only if the victim is not slashed.

Once the attacker controls the victim’s private key:

1. He proves, off-chain, he has the private key by signing a random message.
2. He asks the victim to send 50% of the slashable funds to a specific blackmailing smart contract. On this smart contract one can:
3. Get the funds back to the sender by proving that the corresponding validator has been slashed.
4. Transfer the funds to the attacker by proving that the corresponding validator has exited or that more than a year has passed.
5. The victim has to choose whether to pay or not.

Eth2’s slashing mechanism is non trivial. The minimum slashed amount is 1 ETH, but increases if anyone else is slashed during the next 18 days. We suppose that the attack is large enough to ensure that everybody is slashed to the maximum (i.e. 32 ETH).

As of today, for a validator slashable funds are 32 ETH, the whistleblower reward 0.05 ETH (0.0546875 exactly, (32/512)*(7/8)). If the victim exits without being slashed he will have a revenue of 32 ETH (his own funds given back). The table actions/revenue is:

|  | Victim | Attacker |
| --- | --- | --- |
| Victim pays and exits peacefully with his stake | 16 | 16 |
| Victim does not pay and get slashed by the attacker | 0 | 0.0546875 |
| Victim does not pay and slashes himself | 0.0546875 | 0 |
| Victim pays but gets slashed by the attacker | 0 | 0.0546875 |
| Victim pays and slashes himself later | 0.0546875 | 0 |

We see the victim’s optimal strategy is to pay. This maximizes the attacker’s profit as well.

Once the victim has paid, the optimal strategy for the attacker is to wait for the funds to be transferred. This maximizes the victim’s profit as well.

Moreover, this attack scales: as in the initial scenario, if a zero-day security issue is identified, the attacker can gather all the private keys for all validators found on the network, then and only then, contact the victims.

Of course the hacker can increase the price up to ~31.9 ETH and it is theoretically still optimal for the victim to pay. In real life it’s likely too much.

### Blackmailing in the dark

The attacker can as well extend his attack by not proving he knows the private keys for all potential victims. Let’s say (1) that the attacker took control of the private keys of 25% of the potential victims, and (2) that the potential victims cannot determine if they have been actually hacked or not.

He would then be able to blackmail his victims in the following way: “I know your private key. Give me 16 eth or I’ll impersonate/slash you. You may ask for a proof of possession but that will cost you 3 extra eth.”

If the actors are rational, this is strictly better than the previous approach, as the hacker will get paid for all the private keys hacked, and some of the ones he hasn’t actually hacked.

Ultimately, the attacker does not even have to hack anything but can simply do a public relation stunt by pretending he took control of private keys and slashing validator keys he created himself to create some credibility.

Having devices specialized for signing helps tremendously against this attack, but does not fully break it: if the attacker can’t access the private key during the attack, he can still generate slashable attestations, and store them for later use. It is still an improvement as this unexpected activity could be detected. A signing device that can detect and refuse to sign conflicting messages would work.

(thanks to [@AlexandreBelling](/u/alexandrebelling),  [@benjaminion](/u/benjaminion),  [@OlivierBBB](/u/olivierbbb) for the review/comments)

## Replies

**adlerjohn** (2020-02-11):

In Eth 2 currently, can validators in the exit queue still be slashed? If yes, why?

---

**dankrad** (2020-02-11):

This seems like another variant of [Global slashing attack on ETH2 - #9 by kladkogex](https://ethresear.ch/t/global-slashing-attack-on-eth2/6703/9) – assuming that you can hack a lot of validator keys, you can do devastating attacks.

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> In Eth 2 currently, can validators in the exit queue still be slashed? If yes, why?

Yes, they can be slashed. If you don’t, you would just try to exit quickly after committing a slashable offence, so slashing would be pretty useless.

---

**adlerjohn** (2020-02-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> This seems like another variant of Global slashing attack on ETH2  – assuming that you can hack a lot of validator keys, you can do devastating attacks.

Yes, but the particular point of [@liochon](/u/liochon)’s proposal is that this is way for attackers to *steal* funds, not just burn them. One of the reasons for having different withdrawal keys and signing keys is specifically to avoid a compromised signing private key from resulting in stolen funds—this attack mitigates this mitigation.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Yes, they can be slashed. If you don’t, you would just try to exit quickly after committing a slashable offence, so slashing would be pretty useless.

That’s true, but…is that a problem? If someone equivocates on one fork and withdraws on another, then they can only equivocate once, and then have to lose the TVOM of their deposit being locked until they can get it activated again, i.e. there is something at stake.

---

**dankrad** (2020-02-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> Yes, but the particular point of @liochon’s proposal is that this is way for attackers to steal funds, not just burn them. One of the reasons for having different withdrawal keys and signing keys is specifically to avoid a compromised signing private key from resulting in stolen funds—this attack mitigates this mitigation.

True, however only in the case in which many keys are stolen, which is a pretty horrible situation to be in already, and which I believe we should be able to defend against (not saying it’s trivial, of course)

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> That’s true, but…is that a problem? If someone equivocates on one fork and withdraws on another, then they can only equivocate once, and then have to lose the TVOM of their deposit being locked until they can get it activated again, i.e. there is something at stake.

There are other slashable offences. I don’t see a good reason to allow this?

---

**d10r** (2020-02-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> One of the reasons for having different withdrawal keys and signing keys is specifically to avoid a compromised signing private key from resulting in stolen funds

I never quite understood why one would want separate keys in a PoS system.

Having the stake at risk should imho be part of the deal of getting rewarded for running a validator node. Precisely because it strongly incentivizes to have a system which is well secured. The resilience of the network depends on that.

If somebody doesn’t feel confident enough in their ability to secure a system, it’s probably better for them not to be a validator anyway. It doesn’t help the network to have a lot of validators if too many of them could be taken over by a sophisticated attacker (e.g. through a zero-day exploit). I think that’s the main risk of a PoS system compared to a PoW system.

Probably the attack described here shows that trying to separate the risk of losing the stake from the risk of having the signing key stolen is futile in a design which allows slashing.

I’m not sure that statement is true. If it is, it’s probably better to not separate keys in order to not obscure that risk.

---

**Janeth** (2020-02-13):

The way to attack a validator is by attacking the software supply chain either through subversion or exploiting a zero day. Once in, the attacker has a gun to the validator’s head. Whether he chooses to pull the trigger and profit or to extort and profit is a minor detail.

---

**Janeth** (2020-02-13):

To be clear, a supply chain attack has multiple victims immediately. A small number of individual hacks aren’t a realistic scenario.

---

**dankrad** (2020-02-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/d10r/48/761_2.png) d10r:

> If somebody doesn’t feel confident enough in their ability to secure a system, it’s probably better for them not to be a validator anyway. It doesn’t help the network to have a lot of validators if too many of them could be taken over by a sophisticated attacker (e.g. through a zero-day exploit). I think that’s the main risk of a PoS system compared to a PoW system.

I think very few people feel confident enough to be able to secure a system in a way that there is absolutely no way for it to be broken. People can physically break into your house and take the computer you’re running the validator on. You simply can’t stop that.

The incentives that you want are that

- uncorrelated attacks that only affect a small number of users only come with a small penalty
- correlated attacks that affect a large number of users come with a huge penalty

This is because the first do not actually compromise the security of the system, while the latter do.

I would say the dual key system does create the incentives we want as illustrated by this attack. It is only devastating when an attacker can get access to a large number of staking keys, with a small number the extortion is much less effective (as validators would only use 1 eth compared to 32). If there were only one key for staking or withdrawal, then any compromise would lead to loss of all funds, which would mean physical security is required; only very few people could afford that.

---

**liochon** (2020-02-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> True, however only in the case in which many keys are stolen,

The hacker claims a share of the funds at risk rather than the whistleblower reward (blackmailing) and can ask others to pay to learn if they have been hacked (“blackmailing in the dark”). That’s interesting even with a single hacked validator.

Now with the current way we slash people, the attacker is incentivized to batch his blackmailing, but as well to do as much FUD as possible so people overestimate how many validators are actually hacked, and so accept to pay more.

If I have the penalties calculated right, we have today, with 10m staked, a hacker taking 20% of the slashable funds (so not that much), and no “blackmailing in the dark”:

| # of validators slashed | 1 | 1% | 2% | 4% | 8% | 16% | 32% |
| --- | --- | --- | --- | --- | --- | --- | --- |
| individual penalty (ETH) | 1.00 | 1.93 | 2.86 | 4.72 | 8.44 | 15.88 | 30.76 |
| Hacker’s reward (ETH) | 0.20 | 0.39 | 0.57 | 0.94 | 1.69 | 3.18 | 6.15 |
| Total hacker’s reward (ETH) | 0.202 | 1206 | 3575 | 11800 | 42200 | 158800 | 615200 |
| Total hacker’s reward ($, 1 ETH = $250) | $50 | $301,563 | $893,750 | $3 million | $11 million | $40 million | $154 million |
| Ratio vs. simple whistleblower reward | x4 | x7 | x10 | x17 | x31 | x58 | x112 |

The hacker can also target staking pools of course (but users have to trust staking pools now: [Trustless Staking Pools](https://ethresear.ch/t/trustless-staking-pools/6529)).

---

**dankrad** (2020-02-13):

I understand this. I just said that this still leads to the right incentives in protecting your key (basically, proportionally invest more in security against attacks that could affect many validators as compared to only one).

It is annoying that the dominant strategy on detecting validator misbehaviour (in this case not protecting keys) would be blackmailing instead of reporting.

BTW, the game theory of this is actually interesting. Unless the blackmailer can actually make it credible that

- They will slash if not paid
- They will destroy the key and not slash if paid

then the incentives actually work out differently:

1. The blackmailer – upon being paid whatever amount – has no incentive to actually destroy the key and thus should repeat the blackmail ad infinitum
2. Since this is the case, the rational strategy for any victim is not to pay anything.

One way of doing this is enforcing it through a smart contract that the attacker funds, and that will burn the funds if a slashing is submitted despite paying the ransom. However, this is not very plausible as (a) the attacker would have to commit a lot of funds to this which could be frozen via a concerted hard fork (very plausible if >10% of validators have just been attacked) and (b) they would also expose their funds in case one of those validators gets slashed for another reason after paying the ransom.

So, the blackmailing might be much harder to execute than it is proposed here. At least I don’t see an easy way to do this.

---

**liochon** (2020-02-13):

> They will slash if not paid

If the victim does not pay, or try to exit, then the best strategy for the attacker is to slash the victim, and the victim knows it.

> They will destroy the key and not slash if paid

The contract I proposed in my initial post was:

The victim sends the funds to a smart contract. These funds are locked until:

- case 1: someone (i.e. the victim) proves that the victim has actually been slashed, in this case the funds are returned to the victim’s address.
- case 2: someone (i.e. the hacker) proves that the victim has exited or that a delay (a year) has passed, in this case the funds are sent to the hacker’s address.

This way the attacker doesn’t have to lock any fund.

---

**liochon** (2020-02-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> This still leads to the right incentives in protecting your key (basically, proportionally invest more in security against attacks that could affect many validators as compared to only one).

I agree, the incentives do not change. But the reward for the attacker increases by several orders of magnitude, which means as well that the attacker can invest more than previously.

---

**d10r** (2020-02-13):

[@dankrad](/u/dankrad) I agree.

What I’m concerned about is that the key separation makes people only superficially familiar with how it works believe that they don’t need to care much about security, because the “important” key is not on that machine anyway. I know folks with little knowledge about IT security who run a lot of “master nodes” for various chains, who reason exactly like that.

So, having 2 keys is fine. But we should make sure that prospective validators are aware about this risks. It’s not about the tech itself, but about how it’s communicated. The incentives can work only if they are understood.

---

**Janeth** (2020-02-13):

What makes you think that the majority of stakers will be skilled if you make the setup harder to secure? Such a strategy might serve to reduce the number of skilled stakers, while not discouraging the ignorant.

---

**d10r** (2020-02-14):

Right, that could happen.

What I’m concerned about is a narrative where people believe that running a node is a piece of cake everybody can and should do, because the withdrawal key isn’t there anyway, thus nothing could be stolen.

This could result in a network where a large number of nodes can be compromised by a skilled attacker.

The worst outcome would in my opinion be if such an attacker could abuse that power without hurting the node operators themselves - such that they wouldn’t even notice that their node is being used for malicious purposes.

I’m not yet familiar enough with Ethereum 2.0 to come up with concrete examples for how that could happen - an example from the web2 world for this kind of issue: [Exploiting Wordpress Pingpacks](https://en.wikipedia.org/wiki/Pingback#Exploits)

I’d guess that an attacker controlling say >10% of the nodes could mess with the network in ways which hurt it.

What this means for me:

It’s probably a good thing if the risk of having a portion of the stake stolen by an intruder is not zero. But only if that risk is well known and thus acts as an incentive for more attention on security.

So, I’m not for making it harder to secure nodes, but for making sure that people care enough about protecting the validator key.

---

**dankrad** (2020-02-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/liochon/48/1028_2.png) liochon:

> The contract I proposed in my initial post was:
> The victim sends the funds to a smart contract. These funds are locked until:
>
>
> case 1: someone (i.e. the victim) proves that the victim has actually been slashed, in this case the funds are returned to the victim’s address.
> case 2: someone (i.e. the hacker) proves that the victim has exited or that a delay (a year) has passed, in this case the funds are sent to the hacker’s address.
>
>
> This way the attacker doesn’t have to lock any fund.

Right, I should have re-read the post. I forgot about that after going down in the discussion. Looks like the game theory is sound.

![](https://ethresear.ch/user_avatar/ethresear.ch/d10r/48/761_2.png) d10r:

> It’s probably a good thing if the risk of having a portion of the stake stolen by an intruder is not zero. But only if that risk is well known and thus acts as an incentive for more attention on security.

I do think we are very clear on this that securing the validator key is very important!

I hope for the emergence of staking hardware wallets soon that

- Don’t allow export of the staking key
- Will never allow signing of a slashable message
- Allow the above two points to be certified by a trustworthy manufacturer – so you can run it even in a datacenter with the assurance that the staking key will be safe

Some nice additional ideas:

- Add a GPS/Glonass/Beidou module so you can get an NTP-independent time source and be safe from all timing attacks
- Add a Wifi module, so you can just hide it somewhere under a floorboard for increased physical security

---

**Janeth** (2020-02-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/d10r/48/761_2.png) d10r:

> I’d guess that an attacker controlling say >10% of the nodes could mess with the network in ways which hurt it.

What makes you think that even a prudent validator would know that they downloaded and updated to a compromised version of the node software? After all, they would have covered all the other hardening and opsec procedures.

---

**Janeth** (2020-02-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> I hope for the emergence of staking hardware wallets soon that
>
>
> Don’t allow export of the staking key
> Will never allow signing of a slashable message
> Allow the above two points to be certified by a trustworthy manufacturer – so you can run it even in a datacenter with the assurance that the staking key will be safe

Do you think it will be wise for a validator to outsource their vulnerability to a third party HW/SW provider? Why wouldn’t a skilled provider use the advantage of the more secure wallet to get more gains than someone who hasn’t invested the effort?

---

**dankrad** (2020-02-14):

Not sure if I understand your question – do you mean a wallet provider who incorporates a back door?

---

**d10r** (2020-02-14):

In fact, the prudent validator can’t know for sure.

But the design of Casper slashing (the individual being punished more if many fail at same time) anyway works in favor of those who avoid doing what everybody else does. It incentivizes decentralization in a very generic way, including e.g. trying to not use the same software and distribution channels everybody else is relying upon.

As a result of this multi-dimensional decentralization (the term *diversity* seems to fit), it should become much harder for an attacker to get in control of a large chunk of the network.

This could also mean that for non-techies it’s safer to ask a friend to run a validator node for them instead of using some one-click solution which requires no understanding of the system and which many others may be using too.

I think that’s better for network resilience, thus am skeptical about attempts which try to make running a validator node very easy.

We will see how it plays out.


*(12 more replies not shown)*

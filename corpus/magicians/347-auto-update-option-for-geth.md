---
source: magicians
topic_id: 347
title: Auto-update option for Geth
author: Gilgamesh1401
date: "2018-05-13"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/auto-update-option-for-geth/347
views: 4000
likes: 4
posts_count: 19
---

# Auto-update option for Geth

Hello everyone,

Why isn’t there an auto-update feature for the windows build of Geth (IDK if there is one for other systems) similar to the Mist wallet ?

I presume it is related to the governance issue of “enforcing” chain updates ?

## Replies

**jpitts** (2018-05-14):

This is a question for the geth developers, but you are right that there are governance implications.

Perhaps there could be a scheme for standardizing how users can set their preferences and have their clients auto-updated, and this is addressed in proposals like [Strange Loop](https://ethereum-magicians.org/t/strange-loop-an-ethereum-governance-framework-proposal/268).

---

**AtLeastSignificant** (2018-05-15):

As it applies to miners -

There is already a large amount of control over outcome from client creators who determine default settings of miners.  If automatic updates were part of this, it would only extend the reach of control from “many people will have default settings for X client version” to “many people will have default settings for Y *client creator*”.

Potential solution would be to have auto-update be turned off, but be an option. At least then users are agreeing to opt-in to letting their flavor of client determine default settings.

“Default settings” here may also be a bit vague, but I’m thinking in terms of forks.  It may be that the community doesn’t want a certain fork to happen, but the client creators implement it and we wind up seeing a large portion of hash power supporting it by default.  Auto-updates could make this a bigger issue.

---

**lrettig** (2018-05-15):

This is very hard because of forks. Node operators should have some discretion which fork to talk to in the case of a fork. As Vlad likes to point out, defaults are powerful. (“Who decides which fork becomes the default?”)

---

**MicahZoltu** (2018-05-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atleastsignificant/48/219_2.png) AtLeastSignificant:

> we wind up seeing a large portion of hash power supporting it by default

Friendly (weekly?) reminder to the community that miners do not decide viability of forks.  They have no voting power/say in the governance process.  They are simply a highly liquid and easily replaced service provider.

---

**Gilgamesh1401** (2018-05-16):

Furthermode, taking a look of the current network status of nodes, I see very small number of different clients (Parity/Geth mostly) but a lot of different client versions being ran ([ethernodes](https://bit.ly/1TIVlQE)).

- Why are some nodes running versions as old as 1.6/1.7 and is there a process for declaring deprecation of old versions ?
- All in all, doesn’t this situation hinder network overall performance and security ?
- Are the upcoming large Ethereum upgrades (sharding, POS, etc.) going to be compatible with the older versions Geth versions ? I do not see how would this be possible.

---

**Gilgamesh1401** (2018-05-17):

Maybe he meant “hash power” as a proxy for “adoption rate” ?

---

**MicahZoltu** (2018-05-17):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/g/dec6dc/48.png) Gilgamesh1401:

> Maybe he meant “hash power” as a proxy for “adoption rate” ?

Hashpower is only a proxy for *miner* adoption rate, which is something we don’t (shouldn’t) care about.

---

**AtLeastSignificant** (2018-05-17):

In a PoS world maybe, but why wouldn’t you care about hashpower on a PoW chain?

---

**MicahZoltu** (2018-05-17):

Not for the sake of governance/decision making.  Hash power will move to the where it is the most profitable, and economic participants decide which chain is most profitable.  As long as a chain has non-zero hashing power (so it can continue to produce blocks) it will be viable and if it is viable and economic participants value it then hashing power will migrate to it (rather rapidly in fact).

---

**AtLeastSignificant** (2018-05-17):

That’s a sort of chicken & egg problem though.  The hashpower of a chain is a large part of making a chain viable so that economic participants are interested in using it.  In the case where a hardfork happens and we assume a majority of the hashpower is following the default choice of their client, then users also follow this path because it’s not guaranteed that the minority chain will be secure from 51% attacks anymore.

This makes it incredibly hard for people to oppose certain hardforks.  Those who oppose things like ERPs have been concerned about this issue for a while, citing the fact that there are client developers who have vested interests in reversing / changing certain things.  If the rest of the client creators decided to implement this, what would those who disagree do?  Would it be any different if the number who don’t want this sort of thing was the majority of hashpower / coin holding / user count - or would the outcome be the same regardless?

---

**everton** (2018-05-23):

My two Wei to this discussion, apart from the governance discussion:

I think major clients should not have such auto-update feature. Bugs will eventually be shipped and faulty versions can cause network gridlock, corrupted databases or even consensus issues. Think what could happen if, say, all of a sudden the majority of the nodes become inoperant ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

Even though the Geth team works really hard and make an awesome job, with a huge test suite behind, and cross-client testing like hive, there are some incidents:

They’ve released:

- 1.8.5 on Apr 17th
- 1.8.6 on Apr 23rd
- 1.8.7 on Apr 23rd

Also, automatic code update is a great great opportunity for bad actors.

One could develop a simple application that automatically updates their geth instance, but IMO, it should be far from official.

---

**MicahZoltu** (2018-05-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atleastsignificant/48/219_2.png) AtLeastSignificant:

> it’s not guaranteed that the minority chain will be secure from 51% attacks anymore.

Can you expound on this point?  I think this is where we disagree.

---

**AtLeastSignificant** (2018-05-24):

A minority chain by definition has less than 50% of the hashpower of the original.  That means there exists enough hashpower (from hardware that is likely capable of mining either forked chain) to 51% attack the minority chain.

In reality, it’s not like everyone would stop mining the chain they actually like just to attack (in coordination with everyone else) the minority chain out of spite.  However, it may not take multiple entities to do this if the minority chain is any smaller than the largest single hashpower controller.

The argument that sufficient hashpower will “follow the money” and secure the chain enough to stand up to any single miner doesn’t make sense. Many miners work on chains that are sub-optimal financially because miners don’t all operate for immediate payment. Rather, they are investing their hashpower into whatever they think will eventually pay off.

---

**MicahZoltu** (2018-05-25):

By that argument, any chain with less hashing power than Ethereum (subtracting out ASIC miners that can’t mine a different chain) is insecure.  Similarly, we could assert that any chain that could be attacked by someone spinning up enough AWS/Azure/GCE nodes (i.e., there exists enough access to global hashing power) to attack it is similarly insecure.

If that is your definition of security, then I will agree to your assertion that a chain split results in one of the two chains being insecure.  However, I strongly argue that this isn’t how chain security is (should) be measured.  What matters is whether or not there exists enough financial incentive to attack the chain such that one can *profitably* do so.

In the example of diverting hashing power to attack some chain, unless you have an attack that will allow you to double spend more than it costs you to divert your hashing power then I argue that the chain *is* secure.  The recent double spend attacks against blockchains have occurred because exchange platforms have allowed users to transact for larger values than the system can properly secure against.  This is a mistake by exchanges, they should never be transacting off-chain for more than the security of the system (which to be fair, is hard to measure).

---

**AtLeastSignificant** (2018-05-25):

I wouldn’t immediately use the word “insecure”, but those conditions are necessary ones for insecurity.  It’s not such a black & white issue though.

If there’s profitability in addition to this, then I would definitely deem the chain insecure.  However, there’s more factors than just financial incentive that go into determining whether or not somebody will take advantage of a hashpower weakness.

Just the *posibility* of an attack, even if motives aren’t 100% clear in a financial sense, can be more than enough to sway miners to jump ship and go to the more secure chain - further exacerbating the hash power issue.

Relating it back to the topic, I feel like default settings / auto update take power away from those who wish to actually participate in voting with their hashpower.  I also believe that the default decision of miners should be “change nothing”, so that abstainers from decision making processes are not unknowingly supporting change.

Outside of governance issues, auto updates sound like a good idea. Especially if it’s a 1-time opt-in setting.

---

**MicahZoltu** (2018-05-25):

Defaulting to “no change” is the Bitcoin strategy, and I’m generally against it for an industry that is this new (crypto-currencies).

---

**MicahZoltu** (2018-05-25):

That being said, I’m also against auto-updates.  ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) They introduce an attack vector by which someone can compromise the auto-update feed and take over the network.

---

**AtLeastSignificant** (2018-05-25):

The do-nothing default leads to stagnation if you’re considering all participants to be valid opinions, but anything else leads to centralization issues from what I’ve seen.  The move to PoS will hopefully solve the problem by making it so that the “do-nothingers” traditionally in control of the network are out of the equation, leaving only active participants at the helm.  At that point, abstaining from governance *should be* considered an active decision against change, not a default that leads to stagnation.


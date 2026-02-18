---
source: magicians
topic_id: 832
title: "EIP-1240: Difficulty Bomb Removal"
author: MicahZoltu
date: "2018-07-21"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1240-difficulty-bomb-removal/832
views: 4501
likes: 6
posts_count: 10
---

# EIP-1240: Difficulty Bomb Removal

This is a discussion topic for EIP-1240

The difficulty bomb operates under the assumption that miners decide what code economic participants are running, rather than economic participants deciding for themselves.  In reality, miners will mine whatever chain is most profitable and the most profitable chain is the one that economic participants use.  If 99% of miners mine a chain that no economic participants use then that chain will have no value and the miners will cease mining of it in favor of some other chain that does have economic participants.  Another way to put this is that miners will follow economic participants, not the other way around.

With the difficulty bomb removed, when Casper is released it will be up to economic participants to decide whether they want the features that Casper enables or not.  If they do not want Casper, they are free to continue running unpatched clients and participating in the Ethereum network as it exists today.  This freedom of choice is the cornerstone of DLTs and making it hard for people to make that choice (by creating an artificial pressure) does not work towards that goal of freedom of choice.  If the development team is not confident that economic participants will want Casper, then they should re-evaluate their priorities rather than trying to force Casper onto users.

Personal Note: I think we will see almost all economic participants in Ethereum switch to PoS/Sharding without any extra pressure beyond client defaults.

## Replies

**5chdn** (2018-07-21):

I’m not overly political about this to be honest. EIP-1234 is a way to just give us some time, but if the sentiment is in general favor of forking to Shasper anyways, removing the bomb is a valid option. I added it to the next all-core dev agenda.

---

**SmeargleUsedFly** (2018-07-21):

Looking good. Suggested edits:

1. Remove “with Fake Block Number” from specification, as there is no block number in the calculation.
2. Include the expression "if block.number >= CNSTNTNPL_FORK_BLKNUM" in the specification (see how https://github.com/ethereum/EIPs/issues/1227 original proposal is worded, which I forgot to include in EIP-1227).

---

**MicahZoltu** (2018-07-31):

Sorry for not replying sooner [@SmeargleUsedFly](/u/smeargleusedfly), I believe I applied the changes you recommended a while ago, let me know if I didn’t capture your intent.

---

**MicahZoltu** (2018-07-31):

Reading over the All Core Devs meeting notes, it appears as though there is a belief among the developers that economic participants will not *want* to move to Shasper when the time comes.  I would like to see more discussion on the reasoning for this belief.  If the reasoning for this belief is sound, then we should ask ourselves, “Why are we building features that users do not want?”

I am of the opinion that hard forks should include substantial enough changes that users pro-actively want to upgrade.  To use an analogy, users shouldn’t be forced to upgrade to an iPhone 35Q because their previous iPhone battery was designed to intentionally degrade with time and no one makes/sells old models anymore, they should upgrade to iPhone 35Q because it has compelling new features that the user wants and upgrading is an attractive proposition.

At the moment, the ice age concept is [planned obsolescence](https://en.wikipedia.org/wiki/Planned_obsolescence), and it forces users into a situation where the software they were using becomes unusable after a certain time in order to try to *force* users to use new software.  I am of the opinion that this is a distasteful business practice.

As a consumer, I have been bitten many times by planned obsolescence and now it is a business strategy that I actively try to avoid.

As a developer, planned obsolescence is a business practice that makes me feel like the work I am doing is not valued by users if they have to be “forced” to use it (decreases developer happiness).

As a business owner, planned obsolescence is a reasonable business strategy and can work in some situations.

I would like to hear arguments from those in favor of planned obsolescence as to why they believe that Ethereum has a large enough of a moat to practice such strategies (they tend to not work as well when users have choice), and what the revenue benefits are to the business.

---

**tjayrush** (2018-08-01):

Ethereum is not a business. It’s a community endeavor. Maximizing profit is not the motivation. Maximizing co-operation is. The bomb serves as a forcing function to periodically reinvigorate the community’s belief in itself, helping it remember that it can work together and make common forward progress.

---

**MicahZoltu** (2018-08-02):

IMO, forcing people (via violent coercion or a forcing function) is somewhat against the ethos of this space.  A big part of the idea is that participation in anything in this space should be as “voluntary as possible”.  While planned obsolescence results in a more voluntary situation than threat of violence, it still feels like we could do better on the voluntary front.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> helping it remember that it can work together and make common forward progress

I feel like the difficulty bomb does not achieve this goal, and in fact may achieve a contrary goal.  When *I* see a patch that includes a difficulty bomb delay I don’t see “the community *voluntarily* working together”, I see the community “going along with a change because they don’t have a great alternative option”.  On the other hand, if there was no difficulty bomb and the community did an upgrade anyway then I would see that as the community working together to make common forward progress.  They *had* another option and they instead decided to move forward together.

---

**veox** (2018-08-11):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> At the moment, the ice age concept is planned obsolescence, and it forces users into a situation where the software they were using becomes unusable after a certain time in order to try to force users to use new software.

That’s assuming the bomb is there for the users (OT: “users” is too vague to be considered a category).

I’ve always seen it as being a measure against stagnation / complacency / incompetence.

This was [discussed in meeting 43](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2043.md#delayremove-difficulty-bomb--reduce-block-reward) - “inaction is not an option”.

Node developers *must* coordinate new releases, if at least to diffuse the bomb (but, hopefully, with other changes, along the roadmap).

(Miners and merchants are also affected - but less so, since any given blockchain is only a means to their goal; different than node developers of blockchain X, they can switch from X to Y.)

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I would like to hear arguments from those in favor of planned obsolescence

I’m not in favour of “planned obsolescence” in general. I’m in favour of explicit and time-bound process resolution (including explicit and time-bound failure).

We either describe a minimum common set of changes; or acknowledge that there’s a choice to be made, and split. What we don’t do is take (an unspecified number of) years to make a decision. ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**tjayrush** (2018-08-11):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I see the community “going along with a change because they don’t have a great alternative option”. On the other hand, if there was no difficulty bomb and the community did an upgrade anyway then I would see that as the community working together to make common forward progress.

The community won’t “work together…to make common forward progress” without the forcing function. That’s the point. The forcing function is a reminder that we can do it, and that it benefits us all. It’s both a carrot and a stick at the same time. Keeping the forcing function *is* the “working together.”

---

**tjayrush** (2018-08-23):

Not sure if this is valid or well done, but this article makes what appear to be evidenced-based arguments: https://crypto.omnianalytics.io/2018/08/23/ethereums-economic-breakpoint-an-analysis/. I don’t really know enough to know if the arguments are valid, but I thought I’d share.


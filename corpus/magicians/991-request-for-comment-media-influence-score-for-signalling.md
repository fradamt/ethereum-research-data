---
source: magicians
topic_id: 991
title: "Request for Comment: Media influence score for signalling"
author: MaxSemenchuk
date: "2018-08-09"
category: Working Groups > Signaling Ring
tags: []
url: https://ethereum-magicians.org/t/request-for-comment-media-influence-score-for-signalling/991
views: 3199
likes: 73
posts_count: 30
---

# Request for Comment: Media influence score for signalling

As we’re researching different ideas in our circle, i’d like to share one another idea that came. Let’s discuss it purely hypothetical.

So we have [the list of influencers and their score](https://docs.google.com/spreadsheets/d/13OWMJZk3XyCFGSnqJH6hVf6bPfiimXJ7MbzYU8257NU/edit#gid=1901771872). How about providing them with the voting power, according to their score (e.g. 500 tokens). And let to do non-binding votes on proposals.

Pros:

- Media influence is also a comparable scale of importance

Cons:

- Majority of them may not be interested to vote
- May be prone to bribes
- May be prone to fake subscribers approach

Please, let me know how do you think it’s compared to identity, stake or gas voting.

## Replies

**decanus** (2018-08-09):

I don’t think an influencer list should be considered as a notable signal, especially one which is based on Twitter followers rather than technical ability or contributions to the ecosystem. Just because someone has 2,000 followers doesn’t mean they know what they are talking about. Even if they are non-binding it is a dangerous trend to follow, when we start showing the community that we listen to influencers cause they know what they are doing. Those are just some of my thoughts at least.

---

**mattdf** (2018-08-09):

“Influencer score” is not in any way correlated with importance, competence or aligned interests, even as a signaling method this is a ridiculous idea. You want to treat Peter Todd’s “signaling” as worth more signaling of anyone on the geth or parity team, even though he often calls for people involved in ETH to be jailed and would happily signal for anything that destroys ETH?

What’s the point of this metric to someone who isn’t familiar with the stances and possible conflicts of interest of each “influencer”? To maximize the amount of damage and disruption that bad actors can do?

Seriously, no.

---

**mariapaulafn** (2018-08-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maxsemenchuk/48/443_2.png) MaxSemenchuk:

> Media influence is also a comparable scale of importance

Sorry but I have to strongly disagree on this. Are you saying that having Twitter followers is comparable to building? I don’t get it.

---

**MaxSemenchuk** (2018-08-09):

[@mattdf](/u/mattdf) I understand your point, and just to clarify – it’s not a proposal for building, just a discussion. I know it’s controversial, though seems like fun and i’m curious =)

It’s surely not fully representative (though many from the list are in fact important) and surely can be damaging, but in the same way as other options. If we’re talking staking Ether – it’s much easier to gain, than influence in the community (at least as i see). Also team of the cryptoinfluencers do a great job in algorithms and filtering (see the link).

[@mariapaulafn](/u/mariapaulafn) If we don’t talk only tech EIP, but things like governance we can find out that we’re missing out the voice of the wider community. And while we have such low participation on votings, delegating attention can work a bit better.

---

**phillux** (2018-08-09):

I think the influencers list is very qualitative, subjective, and based on web 2.0 (i.e., gameable) platforms, and therefore will continue to get criticism if used in the wrong way. At most, I think such a list should be used to add context to quantitative signals and ongoing discussions of EIPs (for example, a website searching twitter and github “influencers” and their comments on specific EIPs). However, what you’re really suggesting is to use an identity and reputation-based metric when those identity and reputation metrics have not been clearly defined, agreed upon, or legitimized.

My suggestion is to focus on the quantitative statistics available via the ethereum blockchain (coin signaling, gas signaling, contract signaling) or services tied to it (hashpower signaling, node operator signaling), as these metrics are exclusive to the ethereum network, are easily understood, are more transparent, and therefore have a less controversial path to be legitimized by the community and accepted by core developers.

---

**MaxSemenchuk** (2018-08-09):

> identity and reputation metrics have not been clearly defined, agreed upon, or legitimized

Yeah, can agree with that.

Thanks for the feedback!

---

**eolszewski** (2018-08-09):

Yeah, reputation takes on many different forms - the guys at Colony did a good talk on this ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

There is a reputation for developers, marketers, evangelists, etc… to group everyone into one bucket won’t accurately describe the value they provide.

I think describing the different categories of reputation we are after would aid in kicking this process off.

Does anyone here know nay of the colony guys? They could provide immense help here, imo ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**maciek** (2018-08-09):

I lead the team that created the list.

I think it’s going to be useful if I shed some light here.

**How the algorithm works**

We’ve developed an algorithm that works similar to the original Pagerank. Instead of ranking websites – we rank identities, instead of tracking links – we track attention.

It’s a 2nd order metric, therefore, the number of followers doesn’t matter much. It matters who these followers are.

It’s not just about followers. We’re tracking attention, which is scarce.

Following somebody is an indicator of paying attention. One of many.

At the moment we’re tracking Twitter, but soon we will combine it with many other sources of data.

More here:

https://cryptoinfluencers.io/algorithm - a brief description of our algorithm; this page will be gradually expanded with more details

http://maciek.blog/what-is-influence - my blog post outlying how we think of influence

**To address the cons in [@MaxSemenchuk](/u/maxsemenchuk) post:**

**Majority of them may not be interested to vote**

This problem applies to any voting system. One could potentially address this by delegating one’s votes and through other approaches.

**May be prone to bribes**

One cannot guarantee that no bribery will take place. However, we believe that this approach is less susceptible to this risk than alternatives.

The influence scores distribution is subject to Power Laws. The people who have the most voting power, e.g. Vitalik Buterin, Vlad Zamfir, Joseph Lubin or Gavin Wood are unlikely to be corrupted.

**May be prone to fake subscribers approach**

We believe that this system can be Sybil-resistant. It’s based on quantifying attention. Attention is the source of scarcity.

**To address [@decanus](/u/decanus) concerns:**

How do you propose to measure technical ability or contributions to the ecosystem otherwise?

My belief is that systems tracking ability should be fundamentally divided into:

**a) Accountability metrics** – they work for use cases that can be accurately quantified, e.g. an investors performance can be quantified accurately through returns.

**b) Reputation metrics** – they are necessary when things escape direct quantification, therefore can’t be measured with accountability metrics.

For example, should surgeons be measured by the number of patients that die/survive on their table? If this was the case, they’d have an incentive to only treat “easy” patients and avoid serious cases. Whereas if one quantified which experienced surgeons other surgeons want to observe and learn from – that’s probably a good indication of their expertise.

I’d love to hear your thoughts on how technical ability/contributions can be measured more accurately.

**To address mattdf concerns:**

Peter Todd is not on the Ethereum list. You can check the list on our website (tab Ethereum).

It sounds to me like what [@MaxSemenchuk](/u/maxsemenchuk) is proposing is an experiment. I see no reason why it couldn’t be running along with other experiments, e.g. based on the governance system that [@decanus](/u/decanus) is building.

In the end, one can evaluate how these multiple experiments performed and it will help inform future decisions regarding governance.

---

**maciek** (2018-08-09):

[@phillux](/u/phillux)

- The list is currently based on Twitter only, but it will not always be the case. We are also looking into decentralized sources of data.

[@eolszewski](/u/eolszewski)

- You are right regarding the influence of different roles within the ecosystem. The list currently does not distinguish between them. We are working on experiments that will allow us to find out whether it’s possible to distinguish between these various roles.

Please take into account this is an early version. It’s still alpha.

---

**mariapaulafn** (2018-08-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/phillux/48/900_2.png) phillux:

> My suggestion is to focus on the quantitative statistics available via the ethereum blockchain (coin signaling, gas signaling, contract signaling) or services tied to it (hashpower signaling, node operator signaling), as these metrics are exclusive to the ethereum network, are easily understood, are more transparent, and therefore have a less controversial path to be legitimized by the community and accepted by core developers.

This can be definitely a better workaround. Please refrain from influencers list. Honestly. Fully agreeing here as well with [@mattdf](/u/mattdf)’s point:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mattdf/48/4245_2.png) mattdf:

> What’s the point of this metric to someone who isn’t familiar with the stances and possible conflicts of interest of each “influencer”? To maximize the amount of damage and disruption that bad actors can do?

There are so many contentious sides to this I can’t even begin to grasp them. We are assuming that the list is public, hence if your name is there, you are 100% bribeable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maciek/48/614_2.png) maciek:

> The influence scores distribution is subject to Power Laws. The people who have the most voting power, e.g. Vitalik Buterin, Vlad Zamfir, Joseph Lubin or Gavin Wood are unlikely to be corrupted.

This is an assumption, based on the principles we operate with, we can’t really assume, especially when there is so much at stake, while I hold high regard for these people, you never know.

---

**maciek** (2018-08-09):

[@mariapaulafn](/u/mariapaulafn)

What you’re proposing as an alternative is basing governance on ownership of financial capital. This is the rule of the rich.

---

**mariapaulafn** (2018-08-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maxsemenchuk/48/443_2.png) MaxSemenchuk:

> @mariapaulafn If we don’t talk only tech EIP, but things like governance we can find out that we’re missing out the voice of the wider community. And while we have such low participation on votings, delegating attention can work a bit better.

Wasn’t this crypto influencers list meant to be applicable for future uses eg. signaling website, which would be englobing all aspects incl. tech?

---

**mariapaulafn** (2018-08-09):

Agreed, I said it may be a better workaround, not THE solution. A combination of different factors might be the solution.

An algorithm for twitter, as accurate and well thought as it might be, is even worse.

I’m not saying we need to discard everything, this list might work for other uses. I’m just saying we can DEFINITELY do better than this.

---

**maciek** (2018-08-09):

[@mariapaulafn](/u/mariapaulafn)

We agree on this - it’s not THE solution. We’re trying to propose a building block for a solution.

I believe that governance needs to be based on both financial and human (accounting for social) capital. Otherwise it leads to the tyranny of the rich.

I’m very interested in other ideas about how human capital can be introduced into this equation.

---

**mattdf** (2018-08-09):

Your algorithm is not open source as far as I can see, so you might as well have said nothing as you could have picked this in an arbitrary way and we can’t independently recreate the list, but either way…

> It’s not just about followers. We’re tracking attention, which is scarce.

No, you’re not. There’s no way to do this off twitter. Not for any reasonable definition of attention. There are people who like and retweet just based on who tweeted, as opposed to the content. Many follow others because they often disagree with them and want reply to their tweets. “Activity” towards a certain account is not correlated to how much someone cares about that account, or what they think of it. None of these are metrics that are useful for categorizing influence or importance in the general sense applicable to any kind of governance.

> The people who have the most voting power […] are unlikely to be corrupted.

This is not really how the world works (and in the long term, it’s not a safe assumption to make). Either way, bribes are not the only issue. They could certainly collude with each other to accomplish self-interest driven goals effectively muting others.

> Peter Todd is not on the Ethereum list. You can check the list on our website (tab Ethereum).

How are you filtering for topics? Is it purely algorithmic or are you manually deciding who is relevant to the ethereum community and who isn’t? If it’s manual then you’ve introduced a highly subjective filter which makes you (the list maintainer) another point of failure/corruption. It’s likely that even people who are deeply involved in the space only know ~10% of the accounts on that list at most, hence it’s not easy to check if someone who shouldn’t be included is there, or vice versa.

> It sounds to me like what @MaxSemenchuk is proposing is an experiment.

Best to speak out against ridiculous ideas quickly lest they go too far and start getting taken seriously, for example by people who would take influencer scores as a measure of the quality of a person’s opinions.

---

**jpitts** (2018-08-09):

Relevant to this discussion, a “reputation jam” with [@danfinlay](/u/danfinlay) and others. Read the takeaways…


      [twitter.com](https://twitter.com/sinahab/status/1027639769910525952)


    ![image](https://pbs.twimg.com/media/DkLo3c7UwAAirZA.jpg:large)

####

 1) Reputation jam with good people yesterday – @danfinlay, @decentralion, @nayafia, @sunnya97, @rsepassi, @sidrmsh, @graeme_tweets, Ryne, Thor, @jwmares.

Our discussion was inspired by PageRank, EigenTrust, TrustDavis, Social Collateral, PGP, Circles, ...

Some takeaways:

  [12:36 PM - 9 Aug 2018](https://twitter.com/sinahab/status/1027639769910525952)




       115





       22

---

**tjayrush** (2018-08-09):

Let’s just imaging that a list such as this succeeds and the community agrees that opinions of these “influencers” is important and should carry weight in the forward movement. Even if that’s true, I think this is a bad idea. The only end result is pure  calcification. We’ll get people with more and more influence simply because they’ve had influence in the past.

If the community does adopt a list such as this (they shouldn’t), I say we randomly throw 5% of them off the list every so month and include 5% random new people ignoring reputation. A community driven by “influencers” would bore me to death after a while.

---

**MaxSemenchuk** (2018-08-13):

Thanks for all your time and passion, giving me feedback on the topic. I’ve summarised my findings here https://medium.com/dgov/voting-based-on-media-influence-score-lessons-learned-a860078cbb40 Hopefully to be used by somebody with the same idea =)

---

**maciek** (2018-08-13):

> No, you’re not. There’s no way to do this off twitter. Not for any reasonable definition of attention. There are people who like and retweet just based on who tweeted, as opposed to the content. Many follow others because they often disagree with them and want reply to their tweets. “Activity” towards a certain account is not correlated to how much someone cares about that account, or what they think of it. None of these are metrics that are useful for categorizing influence or importance in the general sense applicable to any kind of governance.

I’ll assume that by “off twitter” you mean “from twitter data”. We clearly disagree on this point.

While I respect your opinion, the issues that you brought up are trivial to resolve with cluster analysis. There are other, harder problems, that you don’t mention, but I’ll not go into this here. We will be publishing more details on our approach and algorithms in the coming months.

I’ll outline our principle assumption: if communication takes place through digital channels and human agents can tell who is influential, then these signals can also be interpreted by machines.

> How are you filtering for topics? Is it purely algorithmic or are you manually deciding who is relevant to the ethereum community and who isn’t? If it’s manual then you’ve introduced a highly subjective filter which makes you (the list maintainer) another point of failure/corruption.

It’s purely algorithmic.

> It’s likely that even people who are deeply involved in the space only know ~10% of the accounts on that list at most, hence it’s not easy to check if someone who shouldn’t be included is there, or vice versa.

This is actually the problem we’re addressing. We all have a cognitive limitation when it comes to keeping track of other members of large groups. We believe that the solution to this problem may lie in describing groups mathematically.

---

**gichiba** (2018-08-13):

![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=9) I’m from Colony! let me continue reading the thread, but at first blush yes, reputation is pretty hard to put into a single metric.

Colony’s rep system is tied specifically to events that happen on-chain, and is more or less a record of everything any particular account has done within a colony, compressed down to a single number. But it’s directly tied to activity that happens in the_colony_ smart contracts, and only that. While we’re looking ahead distantly at the possibility of a more generalized rep system, it’d be quite a challenge to account for *everything* and we’ve got enough challenge in front of us with a mainnet launch targeted this year ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)


*(9 more replies not shown)*

---
source: magicians
topic_id: 4041
title: Stakeholder group / community participation in Ethereum Improvement
author: jpitts
date: "2020-02-26"
category: Magicians > Primordial Soup
tags: [community, eipip]
url: https://ethereum-magicians.org/t/stakeholder-group-community-participation-in-ethereum-improvement/4041
views: 3932
likes: 7
posts_count: 6
---

# Stakeholder group / community participation in Ethereum Improvement

[@econoar](/u/econoar) posted a thoughtful summary and retrospective about the situation around ProgPOW. There are a lot of good ideas here; let’s have a discussion!


      ![](https://ethereum-magicians.org/uploads/default/original/1X/9820c4fe404a7e163dc1dc0a8d644cddd3e4bc2a.png)

      [HackMD](https://hackmd.io/@xoGZo80jQcaTkj_tFKVWxg/SkDrCmNN8)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



# Takeaways from the ProgPoW Situation While the community continues to debate the ProgPoW situation










Also, this is the [discussion on Twitter](https://twitter.com/econoar/status/1232739316545150976).

## Replies

**jpitts** (2020-02-26):

*Expanded from [Twitter responses](https://twitter.com/jemenger/status/1232755221920485378):*

I agree with this idea about needing a standard format for “discussing an EIP” beyond technical feasibility or network health. The discussions here on the EthMagicians Forum are generally technical in that way; this is the reason they are often linked to from the EIP itself.

But I get the sense that [@econoar](/u/econoar) sees a need for discussions about implications outside of the purview of the core devs, e.g. how a decision would affect various stakeholder groups. Such discussions may not tbe echnical, and having them on EthMagicians may even bias them.

Each community group could host such discussions on their own Discourse forums, e.g. “investors” or “app developers”. At some point, a consensus opinion is reached, resulting in a position document. A dissenting opinion from that community might also be useful.

The resulting position document would then be submitted as an Informational EIP, possibly even linked to from the EIP itself. This way, the core devs can review it. Having such positions filed would help them understand the wider implications of an EIP, and also gauge sentiment.

An issue may be that a community group is not large or well-funded enough to host their own Forum. Discourse forums do require a critical mass of usage to be worth the trouble and cost.

It would be helpful to have some neutral domain name w/ a Discourse forum set up w/ permissions, topics, etc. to enable individual groups to use it for their discussions. The aggregate use would then justify the overhead.

---

**econoar** (2020-02-26):

Here is the entirety of my post so that people can quote specific sections of this thread.

# Takeaways from the ProgPoW Situation

While the community continues to debate the ProgPoW situation, I think it’s important that we take a step back and ask ourselves how we got here and how we can improve. I wanted to add some thoughts around how I think as a community we can do better. These suggestions require buy in from various people and stakeholders in the community and there is no single person or group responsible for making this happen. Suggestions are made below for how we get there as a community.

### Background

For those not aware, an EIP is an Ethereum Improvement Proposal which suggests an improvement to the Ethereum protocol. Anyone is able to create an EIP by following the standards laid out in [EIP-1](https://eips.ethereum.org/EIPS/eip-1) and once it’s drafted it enters a [defined process](https://eips.ethereum.org/).

The situation the community is currently stuck on is “how do we handle a contentious EIP?”. EIP-1 actually lays out some ground rules around this:

> The EIPs process and AllCoreDevs call were not designed to address contentious non-technical issues, but, due to the lack of other ways to address these, often end up entangled in them. This puts the burden on client implementers to try and gauge community sentiment, which hinders the technical coordination function of EIPs and AllCoreDevs calls. If you are shepherding an EIP, you can make the process of building community consensus easier by making sure that the Ethereum Magicians forum thread for your EIP includes or links to as much of the community discussion as possible and that various stakeholders are well-represented.

> In short, your role as the champion is to write the EIP using the style and format described below, shepherd the discussions in the appropriate forums, and build community consensus around the idea.

### Problem

The above sounds great but is much more complex in reality. I think this step of the process has major flaws:

1. It puts the onus of informing the community of the EIP on the author. The author has very little incentive to do this.
2. It requires the author of the EIP, who clearly wants to see it happen, to be the one to judge sentiment. Given the bias of the author, this will not be properly judged.
3. An Ethereum Magicians forum post is not on its own a good enough avenue to judge sentiment. While anyone can visit, very few do.
4. Judging sentiment alone is a problem as we have no proper way to do so. Also, what is the threshold on sentiment? Is it 80/20 and it’s a no? Is it 51/49?

So to summarize, we have 4 problems we need to attempt to fix:

1. Author has no incentive to spread the EIP across the community.
2. Author has bias to say sentiment is fine.
3. Even when forced to show the community, the reach is small
4. It’s very hard to judge sentiment, even if all of the above are fine.

I don’t think we can ever make Ethereum governance perfect but I do believe we can do better. Below are my suggested improvements to the above problems.

### Informing the community of the EIP pipeline

I think a lot of our problems can be fixed via better up front communication. We all think each different group in Ethereum lives in a bubble but the reality is the EIP process itself is a bubble! Only a handful of people understand it and tune into calls. Forcing debates to the end of the process is not good.

In reality we have the following stakholder groups in the community

- Core Devs
- Core Researchers
- App Devs
- Users
- Investors
- Miners

Very few of those groups are informed or tuned into the EIP process. I don’t think we can really blame them either as there’s so much information to consume in this space, most are at their max. Allowing people to “subscribe” to consolidated information would go a long way. My suggestion is that some person is responsible for:

- Keeping a live visual of EIPs across the following flow chart
1245×717 42.5 KB
- Collecting a large list of interested parties from the above user groups for a monthly newsletter which explains where EIPs stand in the current pipeline. There can also be a subscribe option for anyone.

### Require a standard for discussing EIPs

While the above alone is a great improvement for communication, we still need a place to discuss each EIP across the community. Just posting on the Ethereum Magicians forum is not enough. Given the above user groups I suggest the author is required to create posts on:

- Ethereum Magicians
- Reddit (r/ethereum and r/ethfinance)
- Medium post (ideally via an official EIP publication)
- Twitter (can be a bot account that reads from medium account above)

The content across each can be the same so it’s just about posting it multiple times.

### Have different stakeholder groups organize and have a representative on ACD calls

I won’t act to have the perfect solution of how this election is done but I think each user group outlined above should have someone on the ACD calls to take notes and speak for that community if needed. MolochDAO is already discussing hiring someone for the “user” group. This person should have read all the relevant EIP information before the calls and be in tune with the community on the feedback given.

### Attempt to set some base standard of signaling mechanisms

Perfect is the enemy of good. While we can never perfectly judge sentiment, I think different community groups have decent ways to judge sentiment. For example:

- Core Devs: relatively small group, simple polling can be done
- Core Researchers: relatively small group, simple polling can be done
- App Devs: Perhaps a call or group formed with elected representatives?
- Users: Twitter, Reddit, etc…this one is tricky
- Investors: MolochDAO vote, POAP token votes, etc.
- Miners: Hash votes

I don’t have all the answers here but I think we could start incorporating some of these signals into dashboards of some sort that go along with the EIP process.

I’m happy to discuss this with any party that thinks they can help out here and am willing to help fund efforts via Moloch, Gitcoin Grants or whatever it may be.

### Define some threshold of consensus required to approve an EIP

This is the trickiest one. We are never going to be able to definitively say we have an exact measurment on consensus in the community but that’s OK. The core dev process refers to “rough consensus” which I think is fine.

I still think we should set in our minds what that exact threshold would be if we could measure.

In my opinion, it’s around 80%. Meaning, if we could perfectly measure sentiment, to make a change we should have 80% community buy in to make it and anything lower would put the network at risk of split. I’m sure opinions vary here wildly.

---

**MicahZoltu** (2020-02-27):

I’ll expand on any of the following points of feedback if desired, but I have written lots about each in the past so I’m going to keep this terse for now:

1. Miners don’t get a vote.  Miners are a service provider and while they may have useful information to share, they should not be part of the decision making process.  Analogy: my plumber may have valuable information they will share with me on how to best choose a plumber, but I don’t let my current plumber vote on who my next plumber will be.
2. Sentiment analysis of a pseudoanonymous group of people is an unsolved problem.  Any solution that proposes we do sentiment analysis should be ignored until someone can solve that problem (it may be unsolvable!).  The only solution that isn’t totally broken is KYC (remove the pseudoanonymous aspect) and that is against the ethos of Ethereum.
3. Democracy is terrible.  One only need look around the world to see the pitfalls of democracy and how it reduces to populism and voter manipulation over time.

This idea of “consensus” or “rough consensus” is broken at its core and we should stop trying to follow it.  We can get “rough consensus” of KYCed groups, but do we really want to assert that all core developers must be known?  Do we really want Satoshi to be disallowed within our community?

---

**elliot_olds** (2020-02-27):

I strongly agree with the sentiment that **miners don’t get a vote** just because they’re miners (if they’re also users / devs / investors we should consider their preferences as part of that group). It is unfortunately a common idea that giving miners what they want is important (it was part of the initial justification for ProgPow – that we were reducing issuance from 3 to 2 so we needed to give miners the gift of ProgPow to compensate them). The network pays $X per day to miners, which causes miners to spend ~$X per day to secure the network. This will happen regardless of whether miners are happy or sad.

I don’t think that all sentiment analysis solutions without KYC are totally broken. If you have some minimum reputation threshold you can defeat most brigading / Sybiling and get a decent signal. For instance if you look at the top 1000 most influential users of hive.one in the Ethereum category, I think them being 80% against something is a pretty solid signal. Even if @antiprosynth is actually Vitalik and thus Vitalik is cheating the system to get two votes.

Agree that democracy is terrible. Most people don’t have an incentive to vote or inform themselves, leaving them vulnerable to special interests / manipulation.

I’m pretty bullish on allowing people to trade fork futures before a potential fork as an additional signal of which side has the most support. The basic version of this could just be an Augur or Gnosis prediction market, possibly subsidized.

---

**lightuponlight** (2020-02-27):

Eric,

Your OP is 100% on track.

Also agree with the comments that miners are not supposed to have a vote on controlling Ethereum. Why? Because the Ethereum social contract is that mining goes away, and if we give them a share of governance that can’t happen.


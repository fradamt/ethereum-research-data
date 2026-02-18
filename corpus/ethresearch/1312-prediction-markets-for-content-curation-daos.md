---
source: ethresearch
topic_id: 1312
title: Prediction markets for content curation DAOs
author: vbuterin
date: "2018-03-06"
category: Applications
tags: [dao]
url: https://ethresear.ch/t/prediction-markets-for-content-curation-daos/1312
views: 28084
likes: 31
posts_count: 20
---

# Prediction markets for content curation DAOs

This is a writeup of an idea that I introduced at the meetup in Bangkok here: https://youtu.be/OOJVpL9Nsx8?t=3h24m51s8

Suppose that you have a social media platform on which anyone can theoretically post content; this could be Twitter or Reddit, some blockchain-based decentralized platform, and the internet itself. One highly desirable thing to have is a way of quickly filtering out content that is obviously malicious, such as spam, scams and impersonations. Relying purely on community downvoting for this is not effective because it is not fast enough, and is also vulnerable to sockpuppet manipulation, bridaging and other tactics. Relying on centralized authorities is a common solution in practice, though carries the risk that holders of entrenched power will abuse it, and the simple problem that there is not enough time for the central authorities to inspect every post. Most recently, the cryptocurrency-focused parts of Twitter have effectively been overrun by scammers to the point of becoming unusable.

Let us consider a different kind of relationship between upvoters and downvoters and centralized moderation. Suppose that for every single piece of content that gets created, there is a virtual market, where anyone can upvote or downvote a post by putting down ETH. One simple market design is one where upvotes and downvotes are both offers to bet at 1:1 odds on the verdict that would ultimately be given by some moderating authority (for now, think of it as a guy named Doug), and once Doug makes the verdict the bets would be evenly partially matched against each other (eg. if 40 ETH bet up and 30 bet down, then each upvoter would only risk 0.75 ETH per 1 ETH they originally put at stake), and then executed. The upvoting/downvoting market is effectively a prediction market on what Doug would ultimately end up deciding, and clients could flag or simply not show posts that have more downvotes than upvotes.

Why use the prediction markets at all, instead of just relying on Doug to give the results directly? There are two reasons. First, Doug is slow; he may be asleep, he may have hardware signing keys that take hours to take out, or any number of other issues could prevent him from making fast decisions. Second, Doug does not have the time or resources to adjudicate every piece of content. In fact, Doug may only have the time to inspect less than 0.01% of all posts made. In this scheme, Doug need only adjudicate a small portion of posts, and can wait until a day or two after the content is posted. The small portion could be selected uniformly randomly, or the probability that a post is selected could be proportional to the amount bet on that post. For any post that Doug does not adjudicate, upvoters and downvoters will simply get their money back, but because of the possibility that Doug will adjudicate any post, people are incentivized to participate in the market, and do so quickly¹, for every post.

Note that this scheme is best used for a limited role, of identifying and removing posts that are unambiguously spam, scams or otherwise malicious; it should not be used as a full substitute for traditional upvoting/downvoting in cases that are any more subjective, as in those cases it really is important that the voting system is polling the community’s opinion, rather than the community’s prediction of some moderation mechanism’s opinion.

Note also that in this kind of scheme, Doug being a centralized actor becomes even more dangerous, because Doug has the ability to insider-trade on these betting markets. This is why it’s actually very useful for Doug to be something like a DAO: so that the public can be credibly convinced that it is not capable of coordinating to cheat them in the markets, and so that its voting can be more transparent and predictable. The loss in efficiency from a decentralized moderating DAO is not a problem, because it can be made up for by the gain in efficiency from not actually using the DAO most of the time and instead referring to a prediction market.

The scheme could be manipulated by a malicious actor upvoting their own posts, but this has a cost, and inevitably creates arbitrage opportunities for people willing to vote/bet against them, so it should be expected that the portion of times manipulation attempts succeed is very small (and all manipulation attempts, successful or failed, ultimately contribute to the source of revenue that incentivizes everyone to keep upvoting and downvoting). If more incentivization is required, a specialized forum could force everyone who makes a post to put down some small amount of funds (eg. $0.50) on upvoting their own post; that would turn the game into a kind of superset of [conditional hashcash](https://ethresear.ch/t/conditional-proof-of-stake-hashcash/1301). However, the fact that the basic version of the scheme can simply be overlaid onto the existing internet and require no cooperation from any existing institutions in order to operate is a large plus, as it means that it could theoretically be implemented today (with the caveat that transaction fees would need to be much lower, so sharding is likely required).

¹ To encourage rapid participation, the market design I suggested would not work, as it has no incentive to vote earlier rather than later. The alternative is a traditional on-chain market maker, like an LS-LMSR, which does have the incentive to get one’s bets in first, but on-chain market makers have the challenge that they require someone to put up capital for each vote. A happy medium could be a system where upvotes and downvotes are used until some small quantity of ETH is bet by both sides, but where the bets on both sides are at less than 1:1 odds (eg. 1.2:1 odds could work), and once the total quantity of upvotes and downvotes reaches some level the system switches into an LS-LMSR, using the implied “fee” siphoned from the existing bets to initially seed the market maker.

## Replies

**k26dr** (2018-03-06):

Why a 1:1 prediction market instead of an Augur-style bid/ask based one?

I expect that the majority of content will be allowed by the moderation DAO. Rejected content is a small percentage of overall content, so a simple programmatic way to win votes would be to always vote yes as fast as possible. What would happen in situations where there are 0 “no” votes?

---

**hochbergg** (2018-03-06):

This could be also looked at as a way to extend centralized teams - which are usually incentivized very differently than their communities (eg crypto-spammers and Twitter). If the market can effectively predict the centralized team’s decisions, this could be expanded to wider usecases creating a cost-effective way to extend centralized moderation.

A few thoughts on the incentives though:

In the rare-but-obvious-spam scenario, why would anyone vote the content up?

And if that is the case, and there is no upside to voting and as such there would be no incentive to invest in voting infrastructure (and it just wouldn’t be worth the effort) - especially if payouts are very rare.

Also - couldn’t a spammer post spam and immediately vote it down at very limited risk - and then have upsides both from the spam being accepted and being rejected? (Assuming no payment to actually post to keep compatibility with existing systems, and that spammers can create sockpuppets to downvote them)

---

**vbuterin** (2018-03-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/k26dr/48/1172_2.png) k26dr:

> Why a 1:1 prediction market instead of an Augur-style bid/ask based one?

If you read my footnote, I actually think something LS-LMSR-based would work better. I avoided bid/ask-based markets just because I am trying to simplify the strategy space and keep it to just “upvote or downvote or do nothing”, though bid/ask-based markets could theoretically work too.

> so a simple programmatic way to win votes would be to always vote yes as fast as possible. What would happen in situations where there are 0 “no” votes?

If there are 0 no votes, then yes voters do not earn or lose any money. Earning or losing money only happens if there is a nonzero quantity of voters on both sides. Remember that these markets are NOT pre-funded.

> In the rare-but-obvious-spam scenario, why would anyone vote the content up?

To increase the length of time that innocent victims see the message. Unfortunately it’s definitely not a Nash equilibrium for there to be a literally zero rate of successful manipulation precisely because in that case there would be no incentive to downvote, but if manipulation can only be slightly successful then every manipulator is effectively contributing to the bounty pot that encourages everyone else to downvote and vote against them and other manipulators.

> Also - couldn’t a spammer post spam and immediately vote it down at very limited risk - and then have upsides both from the spam being accepted and being rejected?

The spammer only has upside from downvoting the spam if others upvote it; if no one upvotes then downvotes are not rewarded. This is also why we can’t pre-fund on-chain market makers.

---

**balasan** (2018-03-07):

We’re working on pretty much exactly what you just described: https://relevant.community

We are doing it with an on-chain community-defined reputation system to compare predictions of 0-reputation agents with an outcome of reputation-weighed votes.

A really cool result of this is a 3-tier content filtering system:

1 - unfiltered (or time-based) - great of AI recommender systems

2 - filtered by prediction - great for community curators

3 - filtered by community rating - great for consumers

This creates a market for recommender systems to compete again one another for being best predictors. I doubt facebook news feed algorithm would fare well in this scenario ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=9)

---

**chejazi** (2018-03-08):

I prototyped a system like this. To incentivize early voting, each piece of content had a “curation window” when raw ETH bets could be placed. The default window was 1 day. The weight of a vote was calculated by combining the ETH bet with the time remaining in the window. More time remaining -> more weight, to incentivize early bets.

---

**lsankar4033** (2018-03-08):

Prediction market driven truth is still scary to me because deviation from empirical truth is so hard to grok when it’s decentralized. At least with a centralized, capitalized institution, individuals can realize that any deviations from empirical truth are things that better capitalize that institution and are thus easier to reason about (although perhaps harder to affect).

That being said, starting such a truth system on spam/scams is probably the way to go, as given enough time, the majority of any population will agree on what’s spam or not. Because spam only works in a population when there are more spammers than non-spammers.

---

**drstone** (2018-03-09):

I like this idea a lot and have been thinking about similar topics [@vbuterin](/u/vbuterin), in particular, those relating to peer-prediction mechanisms or “markets”. Even though we assume that participants in the market only bid on a small percentage of posts (0.01%), we can still even further build a sort of reliability metric around them. In addition, there might be other incentives to participate beyond betting, if instead the winning side (heavier weighted side) is rewarded as part of a pseudo mining process. See [crowdsourcing subjective information on heterogenous tasks](https://arxiv.org/pdf/1303.0799.pdf) or more recently [this](https://arxiv.org/pdf/1612.00928.pdf).

In any scheme, we are still limited by how quickly participants show up to bet or give their belief/opinion. Then we should also be able to reach the same tallying state from either betting (putting up collateral + information) or minting currency (putting up information). The incentives might be more appealing since there is no collateral on one.

In either model and over time, we should be able to build a score about voters/validators depending not only on what sides they ended up after some threshold time but on their score as dictated by a [proper scoring rule](https://en.wikipedia.org/wiki/Scoring_rule), such as from the peer-prediction papers above.

As far as plausibility, I had trouble implementing these mechanisms on Ethereum due to gas limit issues, but nonetheless had some success implementing Dasgupta’s scoring rule (might not work in [its current form](https://github.com/drewstone/truecoin/blob/master/archives/mechanism/EndogenousMechanism.sol)).

As an aside, have you thought about employing peer-prediction techniques into mining processes? Given the premise is some game theoretic notion of truthfulness, it could provide a metric over honesty in these decentralized systems.

---

**kladkogex** (2018-03-09):

Here is another poker-based scheme that also involves “Doug”

1. The first player deposits one token, and makes a particular bet (yes or no)
2. Then each subsequent player can change the bet to the opposite value by depositing twice the deposit of the previous player.
3. The doubling continues until one of the factions (yes or no) loses by not making the next deposit.  The money deposited by the losing faction is split by the  participants of the winning faction
4. If the deposit crosses the “human judge”  threshold of 1000 tokens,  then a human judge Doug is chosen randomly.  Doug is paid from the deposit, say, Doug’s fee is 100 tokens.
5. Doug decides the winner faction. He is paid from his deposit and then the rest of the deposit is split among the winning faction

Note, that Dough can be employed through services such as Amazon Mechanical Turk.

The scheme described is effective because Doug will be involved very rarely

---

**vbuterin** (2018-03-10):

This reminds me somewhat of Robin Hanson’s double-or-nothing lawsuit proposal: https://mason.gmu.edu/~rhanson/gamblesuits.html

---

**cslarson** (2018-04-05):

i’ve followed this model and put it into [experimental operation](https://www.reddit.com/r/ethtrader/comments/89o4ju/recdao_curator_explained/) on the r/ethtrader subreddit. in practice, a 1 hour countdown begins when a market flips to “rejected”, after which the post is removed and would need a flip back to “supported” to reappear.

the main problem i can foresee is the incentive to open the market in the first place. the vast majority of rejection stakes would go uncontested because they’re simply dealing with spam. yet these still have a cost. possibly a solution is to maintain a pool of funds to compensate for these, mainly gas costs.

---

**vbuterin** (2018-04-06):

Great job on RECDAO, and hope the project does well!

Agree that that is an issue, and transaction fees definitely make it worse. I would recommend a hybrid off-chain system:

- Anyone can publish an off-chain signed message “betting” $0.5 (in a pre-existing security deposit) that a given message will be voted valid or invalid
- If there is such a message, anyone else can make a transaction that includes that message and bets their own $0.5 in the other direction. Some portion of both bets is used to find a market.

As an alternative to step 2, if a third party sees messages of both types they can send a transaction that includes both bets (or possibly even multiple bets of each type).

From the point of view of a user, if a user sees an off-chain bet offer that has not been countered, then they also count this toward the “score” of a message.

---

**cslarson** (2018-04-19):

Hi Vitalik, just a quick reply to say to say thanks for your reply and kind words. If the RECDAO project gets off the ground it will be a number of dapps (currently content voting, dao voting, tipping, as well as staking) all of which would likely be affected in their participation levels by tx costs even with mitigations like tx batching. So for now I’m looking into solutions like the parity-bridge that I just came across that might also suit for the purposes of the RECDAO project. Specifically to the prediction market curator functionality, if the initial stake stays on-chain then I see it as easier to keep a tally of for purposes like sharing out from a reward pool, or awarding some other “maintainer” token.

---

**kladkogex** (2018-04-19):

Yes - it is very much like that!

---

**luigidemeo** (2018-07-23):

We are working at something similar at Proof ( [www.proofmedia.io](http://www.proofmedia.io) ) .

1. Voters vote on content in a “mostly true” or “mostly false” decision
2. Voters include tokens with their vote and this is done somewhat quadratically.
3. An algorithm runs in the background constant tallying the votes and determines when there is the minimum threshold required to complete the vote. The parameters for the algorthm are (time, # of voters, distribution of votes and volatility of the vote score itself).
4. Payout is a % of the minorities wager which gets paid to the majority.

The main difference with Proof and some of the markets being described are that the market is blind to avoid “herding” and that there is a completion period via an algorithm. These two points make it superior to traditional TCRs in our opinion.

---

**littlejoeward** (2018-09-30):

The obvious shortfall to this is the centralization of “Doug”

I’ve given this a lot of thought and my solution can be found [here](https://steemit.com/steeemdev/@littlejoeward/my-personalized-steem-feed-proof-of-concept-is-ready-for-testers)

The main idea is that everyone has their own group of personal curators. It is not necessary for you to manually pick your curators and you might not even know if you are a curator for someone else.

Everyone in the system is a potential curator.

This is the basic overview

- The program looks at every vote you have made and finds the top 100 people that have voted most similarly to you in the past.
- Those 100 people become your personal curators of content. Whenever one of them votes on a post, it will show up in your feed.
- As you vote/skip over posts in your feed your curators will receive scores based on whether you vote on the things they have or whether you skip past them.
- The curators with the best scores will have a greater influence on the order of your feed.
- Every day your worst curator is replaced with a new one.

No centralization, just people voting on things they like.

---

**miguelprados** (2018-09-30):

Users can bet on AI agents instead of Doug/type agents. AI agents will compete for a higher accuracy based on past results, so Doug can keep on sleeping.

---

**TezBaker** (2018-09-30):

Rather than a mechanism that is designed to evaluate content in isolation we have been working on a mechanism that evaluates the content’s creator i.e. their reputation.

A decentralised smart contract to manage a user’s reputation across any participating centralised or decentralised web application; where Proof of Reputation will help avoid the need for censorship.

Presently there seems to be two pain points:

1. virtual reputation can not be transferred;
2. leveraging reputation can not be anonymous.
An ebay user with 100% positive feedback can not leverage that reputation across other web applications; whilst an academic in a highly censored region may find it hard to build a reputation if their field conflicts with their region’s political agenda.  A Proof of Reputation smart contact will allow the most deserving people to be heard and influence in the most efficient manner.

Develop a trusted means for existing and new web applications to provide their users the ability to export or import their reputation to or from a decentralised anonymous repository; whether the application is a market leader or start-up in either the centralised or decentralised markets.  The contract would become a conduit for web applications to work together to promote “Good Actors” and silence “Bad Actors” in an efficient and transparent manner.

If the contract could evaluate not only the reputation of the unique address but also the reputation of the networks in which the address is valued then there is a higher chance that the work required to achieve a respected reputation would be higher than the work or cost ‘Bad Actors’ would be willing to outlay.

If the contract was trusted it would not matter if there was a name associated with the reputation or not, the reputation would be enough and hopefully mask preconceived bias.

---

**janmajaya** (2022-02-01):

I prototyped this, along with few modifications. You can try it out [here](http://cocoverse.club).

At present, it’s like any other social media app. You can create groups on topics & every group has moderators (i.e. Doug). The difference is that every post that gets displayed on the group feed is curated through prediction markets.

This means every post is a prediction market in itself (funded by the creator of the post). Users place their prediction (i.e. buy YES/NO outcome shares) on the basis of whether they think the group moderator will find the post fit for the group feed. The group feed only consists of posts that have high YES probability in their respective prediction market.

Additionally to make sure moderators aren’t overwhelmed with posts to review, the post prediction markets are designed to resolve (in most cases) automatically. It works like following -

Post’s prediction period (time duration for placing bets) is followed by a challenge period. During challenge period users can challenge the temporary outcome (first temporary outcome is set as the outcome with high probability during prediction period) by putting some WETH at stake. Challenges follow double or nothing lawsuit (i.e. to challenge you need to put double the amount at stake than the previous challenge). If a temporary outcome isn’t challenge before the challenge period expires, it is set as the final outcome. If temporary outcome are challenged repetitively for few times (limit is set by the group moderator), then the group moderator sets the final outcome. Once final outcome is set, post’s prediction market resolves.

Note that the app is still experimental and has limited features as compared to a normal social media app.

Looking forward to everyone’s feedback.

---

**jpiabrantes** (2022-09-22):

Hey everyone,

I was really inspired by this post - so I built a tool based of it.

It’s a tool that allows DAO to share a Twitter account.

Each account has guidelines that say what can and can’t be published on the account. The DAO elects moderators that transparently enforce the guidelines.

Members of the DAO suggest content, and they bet how many likes each content will have if it gets published on Twitter.

The content gets ranked according to its estimated number of likes.

I’ve wrote more details in here: https://joao-abrantes.com/writing-monks

and you can try our MVP here: https://writingmonks.com

would love all and any feedback!


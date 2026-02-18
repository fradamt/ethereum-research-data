---
source: ethresearch
topic_id: 14762
title: Prediction markets and a reputation system in place of editorial review
author: murraci
date: "2023-02-06"
category: Applications
tags: []
url: https://ethresear.ch/t/prediction-markets-and-a-reputation-system-in-place-of-editorial-review/14762
views: 2508
likes: 5
posts_count: 23
---

# Prediction markets and a reputation system in place of editorial review

If one were to build an open platform to compete with news media rather than social or blogging media, they would need some sort of accountability/quality control mechanism to mirror the role of editorial review at prestigious news platforms.

The best tool for aggregating information that we have devised is markets. This is especially the case in open systems. The biggest risk to a well-functioning market is collusion. Any mechanism that was designed to employ markets in the place of editorial review would need to guard against this. With this in mind I propose this system:

1. A reporter with information on a climate event writes an article and publishes it to the platform. They must stake a certain TBD amount of money on this article.
2. The article is published without editorial review (unlike how news media currently works).
3. Prospective fact checkers (post editorial reviewers) also stake money and state their specialist topics. Some of those that listed climate as a topic are randomly chosen from the available pool of people. They are each given guidelines on how to judge an article and use these guidelines to give the article a trust score without colluding among themselves as they don’t who’s been asked to fact check. The article and the guidelines together represent a Schelling Point the fact checkers can converge on. A fact checking assignment is like jury duty. Some of your stake is slashed if you renege on giving a score for a given article. This requirement along with random selection should minimise any collusion.
4. The writer’s payout is determined by the score the fact checkers give him/her. The fact checkers’ payouts are determined by how close they are to the average score from the group. Everyone’s respective rep scores are also updated. Those that drop below a certain trust score will not have their articles listed on the platform or be chosen for post editorial review. Articles from the best performers will be amplified on the platform, minimising the chances of readers being supplied erroneous information.

Would be interested to hear people’s thoughts on this system? One worry I have is that after some time people will be armed with prior probabilty data and will simply strategically pick the high probabilty outcome without doing any fact checking. This could be mitigated by minimising the amount of tasks a fact checker gets, leading them to take the utmost care with the ones they are given. It’s not a perfect mitigation by any means though.

## Replies

**llllvvuu** (2023-02-07):

I’ve thought about these types of systems a lot, and I’ve seen many people come up with similar ideas. IMO the major hurdle you always have to solve is how to settle the market. With no fundamental anchor you can have an infinitely irrational market e.g. a Ponzi. You can certainly try to use it to scale a centralized settlement layer (e.g. the centralized mods only settle 10% of bets), which isn’t too different from a traditional whistleblower program.

The other thing about prediction markets in general for elicitation is that if you want a prosocial market you’ll probably need to subsidize them. For that reason, it seems best to reserve the real money for questions with critical mass (the proverbial “million dollar questions”). Another reason to avoid putting markets on smaller issues is [motivational crowding](https://en.wikipedia.org/wiki/Motivation_crowding_theory). Someone might actually do less research on a topic if they’re offered an insultingly small sum of money.

For these reasons I think something with the breadth and fragmentation of articles and forum posts are probably best served by karma systems and simple voting space (vs virtual price space, bid/ask, etc). You can randomly audit people’s voting history and give them voter karma or something.

Twitter [Community Notes](https://help.twitter.com/en/using-twitter/community-notes) is also good. It is specifically *not* tuned to report the majority opinion.

---

**murraci** (2023-02-07):

Hey. Thanks for your response. Yes agreed re subsidies - they’re essential - and I have a whole system for that too but that’s another discussion!

Re how to solve settlement, do you not think my proposed curated two-in-one market solution would work? Editors are randomly assigned to an article and must cast judgement on the it given various objective metrics by which to measure it by a certain deadline. They cannot shirk casting judgement without penalty. The average editor score determines the writer’s payout. Individual editor payouts are determined by how close they are to the average. The market(s) for the article are thus settled. It’s not a traditional open bid/ask prediction market, it’s a ‘regulated’ blind auction designed to force settlement.

---

**llllvvuu** (2023-02-07):

In short, no. It’s one of the first rules one would naturally consider, and then once one sees some issues, one would eventually go down the road of trying to patch it by making adjustments for having an early opinion, being an early contrarian, etc. But you still have the same fundamental issue. You’re incentivizing everyone to have the same opinion, not the correct opinion.

---

**murraci** (2023-02-07):

So this is specifically a fact reporting market I’m talking about here. I have a different design in mind for opinions. In this scenario writers are reporting facts that are usually publicly verifiable. Stuff like quotes might be a problem but also not necessarily if the editors in a given specialty also have access which in many cases they will. The editors take an overall opinion on the veracity of the piece without knowing what position the other editors are taking, so who goes first and who is contrarian isn’t relevant. Yes it’s true that everyone’s incentivised to converge but the natural Schelling Point for this convergence to me seems the truth given collusion is highly unlikely? What other natural equilibrium is there? The only one I can think of is someone just going with prior probability.

---

**llllvvuu** (2023-02-07):

If something is super objective then yeah, I think this design works perfectly, it’s what oracles use. I think you still need an expert to curate which parts of the article to highlight as objectively judgeable. The line between “resolvable fact”, “fuzzy vibes”, “cherry-picked”, etc is a fine skill which is similar to the bespoke skill of creating good prediction market questions, which I don’t think AIs are quite up to yet.

That said, I’d still add in some type of fallback. Every Schelling-based mechanism has some sort of “higher power” to get out of bad Schelling points, for example prediction market operators use centralized moderators, and Ethereum [solves the problem of weak subjectivity](https://blog.ethereum.org/2015/01/28/p-epsilon-attack) ultimately via the market price of fork tokens. Of course, we can sustain only maybe one contentious fork a year, so it wouldn’t be applicable to more contentious topics.

Interested to hear what you have in mind for more subjective stuff. There is Kleros, which I’m not convinced avoids the infinite regress problem. The “higher power” in the case of an escalated Kleros dispute is just another jury IIRC. And they have some fair share of controversies.

The question I still have in mind is that if you just want to view the majority response to something; i.e. purely use it for UI purposes, and not have to have it adjudicate a case, why not show the unfiltered responses, like Twitter’s community notes. Then you can read both the majority response and the minority response.

Like I think on Kleros, if you have a minority opinion, you’ll find that out on the forums and you won’t cast it on-chain. So that information would be missing on-chain. But as someone looking to learn about the case myself and form my own judgment, I would probably want to look at the forums and not just the on-chain vote.

---

**MicahZoltu** (2023-02-07):

If you launch something like this you will quickly learn how difficult it is to identify “facts” in the real world.  While “truth is subjective” sounds like something an annoying philosopher would say, in this case it actually matters.  For some things like “who won the sportsball game that was broadcast on every television in the world prior to the advent of deep fakes” it is relatively easy, but things quickly degrade.

As an easy to understand example, imagine using this system to determine whether the Tienanmen Square Massacre happened.  A very significant portion of the global human population would disagree with the other very significant portion.  The people who can actually assert whether it happened from first hand experience is on the order of maybe thousands, compared to the billions of people who *think* they know what happened (because they believe the people who are tell them it happened).  The system ends up not predicting whether it happened or not, but predicting whether the majority of the world **believes** it happened or not.

History is riddled with examples of the majority of humans believing something to be true that we later discovered was not true.

---

**murraci** (2023-02-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/llllvvuu/48/9687_2.png) llllvvuu:

> I think you still need an expert to curate which parts of the article to highlight as objectively judgeable. The line between “resolvable fact”, “fuzzy vibes”, “cherry-picked”, etc is a fine skill which is similar to the bespoke skill of creating good prediction market questions, which I don’t think AIs are quite up to yet.

I’m not so sure it does. Writers will be instructed to format their writing in a certain way and are incentivised to do so so that they maxmise their chances of being accurately judged. Editors (judges) also have criteria work with. Yes some facts of course are fuzzy and this system won’t always get things right but what are we up against here? The news is currently between 40-75% falsehoods depending on which research you trust. I think this system has the potential to be much, much better.

![](https://ethresear.ch/user_avatar/ethresear.ch/llllvvuu/48/9687_2.png) llllvvuu:

> That said, I’d still add in some type of fallback. Every Schelling-based mechanism has some sort of “higher power” to get out of bad Schelling points, for example prediction market operators use centralized moderators, and Ethereum solves the problem of weak subjectivity ultimately via the market price of fork tokens. Of course, we can sustain only maybe one contentious fork a year, so it wouldn’t be applicable to more contentious topics.

The higher power here is more articles. If an article is written and is judged to be accurate but is later found to be inaccurate, it won’t be relitigated. Other articles will simply ‘fork’ away from the previous truth. Yes people will have gotten rewarded for inaccuracy but I believe this will happen *a lot* less often than it does in the intermediated news media world where people are more often rewarded more for inaccuracy than not!

![](https://ethresear.ch/user_avatar/ethresear.ch/llllvvuu/48/9687_2.png) llllvvuu:

> Interested to hear what you have in mind for more subjective stuff. There is Kleros, which I’m not convinced avoids the infinite regress problem. The “higher power” in the case of an escalated Kleros dispute is just another jury IIRC. And they have some fair share of controversies.

It’s still WIP but a similar system of blind betting (to mitigate problems you alluded to above) except without editors/fact checkers and only other writers with opinions allowed participate in the market. The amount of opinions writers will be able to espouse in a given month will be limited meaning their bets should be saved for those subjects they know most about and have confident opinions in (or of course subjects they have a vested interest in). They can also only bet with funds they raise through the system and get to keep some of their stake no matter what - you don’t want to make people too scared to have any opinion at all! Again it’s far from a free-for-all as that simply wouldn’t work. You want to incentivise the right people to participate in each market. Participants will be aware of other people’s arguments but not the strength of their bets so won’t know where precisely the market lies (poker in reverse). The rationale here is that the price in the market can affect people’s people’s views or even their willingness to express a view at all. That’s not desirable. As I said, WIP but that’s the bones of it and I think the various rules have a good chance of stimulating very high quality debate.

![](https://ethresear.ch/user_avatar/ethresear.ch/llllvvuu/48/9687_2.png) llllvvuu:

> The question I still have in mind is that if you just want to view the majority response to something; i.e. purely use it for UI purposes, and not have to have it adjudicate a case, why not show the unfiltered responses, like Twitter’s community notes. Then you can read both the majority response and the minority response.

The aim here is to replace the New York Times with an open protocol. When people read NYT articles now they don’t tend to go searching for alternative interpretations of facts or contrary opinions. They just read it and it becomes their truth. I don’t expect that to change too much in this system. I just want to offer readers a better truth where markets designed for informational accuracy replace the deleterious effect of ads and subsrcriptions on the truth in intermediated news media.

---

**murraci** (2023-02-07):

Truth is absolutely subjective but I don’t see that as an argument against a system like this given what we have now. Take your Tienamen Square example. The reason there are such divergent opinions is that there is complete control of the media not only in China but in the west too (something we never admit). All across the west news media is dominated by fewer than 10 companies.

In this open system when Tianeneman Square happens only those writers that know about it are incentivised to write about it because they know they’re going to be judged by a system nobody has any control over. The number of people in China that aren’t in the government outnumbers those that are by a huge factor. The chances of the government being able to have their guys on a randomly selected panel to judge a writer reporting on it are slim. I mean they can try employ thousands and interfere with the probability scores given but at the moment they can simply ban any discussion of it whatsoever on any national platform. So no matter what this would move the needle. Of course they would try censor this platform too but that’s another discussion. All I can do is design this as best I can. Other people are trying to make the internet itself less censorable.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The system ends up not predicting whether it happened or not, but predicting whether the majority of the world believes it happened or not.

The system is specifically designed to avoid this. It’s not what the writer thinks about what *everyone* believes. It’s how he thinks randomly chosen judges who are likely to have knowledge of this subject and can’t collude with each other will judge him/her. He knows they only have the truth as a natural Schelling point so he must better write the truth if he wants to be paid.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> History is riddled with examples of the majority of humans believing something to be true that we later discovered was not true.

It is and I’m on a mission to make this a less regular occurrence ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**MicahZoltu** (2023-02-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/murraci/48/10727_2.png) murraci:

> they know they’re going to be judged by a system nobody has any control over.

The judges aren’t people who witnessed the event though.  The judges are people who receive secondhand information about the event from media sources they choose.  People living in China will report it didn’t happen, people living in the US will report it did happen.  Truth isn’t found, only which viewpoint dominated the feeds of the people who participate in the resolution process.

![](https://ethresear.ch/user_avatar/ethresear.ch/murraci/48/10727_2.png) murraci:

> judges who are likely to have knowledge of this subject

Why should we assume the judges have privileged information about the subject?  If they are randomly sampled from the community at large, then the best bet (and best way to rule as a judge) is to try to predict what the consensus view is, not what the truth is.

![](https://ethresear.ch/user_avatar/ethresear.ch/murraci/48/10727_2.png) murraci:

> they only have the truth as a natural Schelling point

I think this is the thing that is the core of our disagreement.  The truth is *not* the most natural schelling point in all situations.  Very often the natural schelling point is what is popular, even if that is untrue.

There are *many* things where if I was voting to predict how a random judge would rule on a thing, I would bet against my belief in what is true.

---

**murraci** (2023-02-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The judges aren’t people who witnessed the event though

Like they could be. Or if not would probably be able to find someone that did. They would’ve had to put down Beijing (or at least Chinese) current affairs as a topic to get randomly selected to report on this in the first place.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Why should we assume the judges have privileged information about the subject?

Because you only get to cast judgement on specialty topics and there’s a limit to how many of these topics you can have. Each article will be tagged with 1-3 topic areas by the writer. So it’s not a random sample of the entire world, it’s a random sample of the informed.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I think this is the thing that is the core of our disagreement. The truth is not the most natural schelling point in all situations. Very often the natural schelling point is what is popular, even if that is untrue.

I agree that it usually isn’t. This is why I’ve designed this system the way I have. It’s specifically designed to remove the influence of the mob and place it in the hands of those that are a) informed and b) incentivised to be honest.

---

**MicahZoltu** (2023-02-07):

There are a great number of topics which I would vote against my beliefs if I knew the judges were self reported experts in those topics.

The fundamental problem here is that self identified experts still results in what is functionally popular consensus, rather than truth.  It is very similar to “trust the science” which means “trust the people identified via mechanism X as experts in the field” rather than “trust in the scientific method and the predictive power of a given model of the universe”.

---

**murraci** (2023-02-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> It is very similar to “trust the science” which means “trust the people identified via mechanism X as experts in the field” rather than “trust in the scientific method and the predictive power of a given model of the universe”.

This is interesting because this is the very thing I’m aiming to replace. In that case you have given identity and insitutionally-induced group think, etc. It can be career suicide to go against the crowd on controversial topics and even for non-controversial ones, inertia with regards to the truth sets in.

In this system you have people that have reported an ability to access information in a given subject. They’re not necessarily waving around credentials (they mightn’t even have any!) and their identity and credentials are completely useless to them here anyway. When they are chosen to judge on an article that comes under this subject, they do so in a secret ballot and they do so knowing that the only other people with background knowledge or an interest in this area are judging. Remember this is also new information. No consensus has formed on it yet.

I’m never going to argue that this system will produce perfect information all of the time. I do think it’s far better than how news media works now however where the corrosive influence of private ownership, advertising, subs and newsroom group think is degrading information quality. Trust in news media is at unprecedented lows and continuing to get worse. People are crying out for something else.

In your opinion why is the intermediated media world preferable to what I propose?

---

**MicahZoltu** (2023-02-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/murraci/48/10727_2.png) murraci:

> In your opinion why is the intermediated media world preferable to what I propose?

It isn’t that the current system is good.  It is that I don’t believe the proposed system will end up any better.

The proposed incentives aren’t setup to find truth, they are setup to find a schelling point among a particular demographic of people and the schelling point among a particular demographic often is not aligned with truth/reality.

This doesn’t even get into the problem of a sufficiently wealthy or Sybilled person being able to just pick the outcome they want since they can define the “schelling point” if they control over 51% of votes.

---

**murraci** (2023-02-08):

OK so I strongly disagree with this. The current system has private ownership that literally explicitly inputs a bias with editorial direction from the start. It relies on advertisers for revenue so can’t piss them off. Said revenue comes from clicks rather than people actually being informed with good information so sensationalism, negativity and ‘being original’ are structurally favoured over accuracy. There’s a limit to how many subs people will take out so only the larger brands can survive on them and they are left with a wealthy demograph they must exlusively cater for. What you have is upper middle class journos writing for the upper middle class. They have no understanding of the rest of society. Smaller, especially local newspapers can’t survive. They’re either bought up and gutted of their actual local news team or they shut leaving people with no local info at all let alone bad info.

So apart from not having these biases inbuilt into the information production system, my proposed system doesn’t rely on an organisation where some articles subsidise the production of others and has a completely different revenue model. I believe it can serve news deserts without the organisational overhead.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The proposed incentives aren’t setup to find truth, they are setup to find a schelling point among a particular demographic of people and the schelling point among a particular demographic often is not aligned with truth/reality.

In the absence of the forces I alluded to above the Schelling point will be truth far more regularly than it is now. The particular demograph will be much more pluralist - not a credentialled closed system - and more incentivised to be truthful than in the current system.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> This doesn’t even get into the problem of a sufficiently wealthy or Sybilled person being able to just pick the outcome they want since they can define the “schelling point” if they control over 51% of votes.

Proof-of-real-human makes Sybil attacks pretty damn challenging and having to coordinate 1000s of writers to game this system is *much* harder than just buying 1 of the 3 main newspapers or 1 of the 3 large firms that own all the local news outlets now. That’s a *far* bigger threat to society than a carefully designed open system ever would be. Right now around 10 people could get around a table in any western country and decide what people think.

It appear you’ve resigned yourself to a reality where we’ll always have broken systems of media and science. I don’t share your pessimism. We can definitely move the needle. I think quite a bit.

---

**llllvvuu** (2023-02-08):

My take isn’t that random ppl’s opinions are bad. It’s just that you lose something when you boil it down, and there’s no need to do that unless you need to feed the result to a machine.

Maybe one way to improve the scheme would be to have people put both their “real belief” and their “expected consensus belief”, and only score the latter. This would be similar to the [“surprisingly popular” technique](https://arxiv.org/abs/2105.09386). That being said, the metagame would still be somewhat complex; and especially so if we tried to come up with a midway solution involving composite scoring.

---

**llllvvuu** (2023-02-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/murraci/48/10727_2.png) murraci:

> blind betting

Blind isn’t necessarily good or bad. There are benefits to discussing openly and reaching a consensus.

In any case, I don’t think I’d blindly go in and stick my neck out betting money against e.g. some astrological woo piece or nationalist propaganda. It’s too risky.

---

**murraci** (2023-02-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/llllvvuu/48/9687_2.png) llllvvuu:

> Maybe one way to improve the scheme would be to have people put both their “real belief” and their “expected consensus belief”, and only score the latter. This would be similar to the “surprisingly popular” technique.

I read that paper some time ago but had forgotten about it. Thanks for reminding me. That’s an excellent suggestion and I think definitely worth considering, particularly for opinion markets. And I don’t think the metagame would necessarily be prohibitively complex. Just have two separate markets with two separate payouts and to really focus people’s minds you could have some sort of payout bonus that grows with the size of the gap between the reality consensus and the expected consensus. Far from perfect but moves the incentive needle a bit. Again I stress we need to compare this to the current dumpster fire rather than some truth utopia that has never existed.

![](https://ethresear.ch/user_avatar/ethresear.ch/llllvvuu/48/9687_2.png) llllvvuu:

> Blind isn’t necessarily good or bad. There are benefits to discussing openly and reaching a consensus.

Oh yeah for sure. Blind just probably appropriate for this use case of markets.

![](https://ethresear.ch/user_avatar/ethresear.ch/llllvvuu/48/9687_2.png) llllvvuu:

> In any case, I don’t think I’d blindly go in and stick my neck out betting money against e.g. some astrological woo piece or nationalist propaganda. It’s too risky.

It’ll be interesting to see how this plays out in practice. You might be pleasantly surprised at the results it churns out. I haven’t discussed the public goods funding scheme here but that alone is motivation to build an open news media protocol given the economic precarity the industry faces. Writers won’t have the same incentives to [pollute](https://vitalik.ca/general/2022/10/28/revenue_evil.html) the public goods they produce. The markets working on top to further hone the quality of the articles would be a nice bonus.

---

**murraci** (2023-02-08):

I also still think that in many cases, most likely the majority of cases, editors, on account of random selection, secret ballots and reported information being new, will have a poor insight into what the consensus will be. So best bet is to just go with reality.

So your suggestion is probably most appropriate for opinion markets.

---

**bowaggoner** (2023-02-09):

This is very interesting, but I do agree with the criticisms, especially llllvvuu’s. I would crystallize these two points that make this problem very hard:

1. Using “the crowd” to fact-check eyewitness/expert claims in the absence of verifiable ground truth. 1000 random people cannot fact-check one eyewitness or domain expert (Tianamen square example, medical articles, etc). 995 laypeople and 5 experts can maybe fact-check an expert, but finding the signal among the noise from those 1000 is very hard without objective verification (uprisingly-popular type techniques are sometimes ok at best). Schelling points are for common knowledge everyone knows, not for rare knowledge.
2. Inefficiency - a lot of total effort needs to go into the “meta” of the system, which may be hard to incentivize without external subsidies. Reputation systems are much more efficient, which I think is why they’re the dominant paradigm. A particular source (i.e. reporter, news organization) establishes a reputation of trustworthiness over time (at least to certain readers), and the amount of effort that has to be put in to fact-checking them decreases significantly. Of course, there are failures of reputation systems all the time, but they’re still hard to improve on due to efficiency.

---

**murraci** (2023-02-09):

Appreciate all the critical feedback. That’s why I posted here first!

1. The idea is to use a specific crowd - but with enough randomisation within the crowd to create uncertainty over expected consensus - for each piece of news. I believe there would be a Schelling Point within that crowd. It wasn’t hard for a lot of people in Beijing to know if Tianeman Square massacre happened or not. The problem was that the government stifled their voice. It can’t do that on a decentralised platform.

Editors fact check things blind all the time now. They mainly trust their reporters.

1. I think if reputation alone was so clearly sufficiently efficient you wouldn’t see such different reporting of the same facts in the news today. It’s the owner of a newspaper that decides the context. You also wouldn’t see such sensationalism. Also statistically over 50% of stuff reported is found to be false so that doesn’t strike me as a system that works very well.

People have decamped into tribes and trust the newspaper of their tribe. That’s bad. If you don’t know what tribe members are editing a piece that creates enough uncertainty over the consensus in most situations where the rational bet is to go with the truth IMO.

I agree re subsidies and I have a few systems for them I just haven’t mentioned it here as was solely looking for feedback on the prediction market design. I think prediction markets haven’t existed until now because before blockchains came along they were infeasible from a regulatory perspective. Also early attempts didn’t solve for any of the issues we’ve discussed here. I think my design does so pretty well, especially when compared to traditional news media systems.

We have numerous tools for establishing trust. Reputation is one of them. The law is another.  Markets are another. We now have blockchains too. I don’t see why a well-designed system that harnesseses all these tools wouldn’t bring better results than systems that use fewer of them as long as it’s cost effective to do so. Right now it’s just a fact that most newspapers aren’t economically viable. They’re being propped up and there are huge costs to society to them being propped up because they’re gradually losing more and more of their independence. There’s a reason governments across the world are holding hearings on the problem. I believe in taking information intermediaries out of the equation you save on so many costs that you can afford to subsidise a market for truth and the system being much less capturable than it is now. That wouldn’t be hard!

I think if you don’t employ markets I think you just end up with social media which is its own dumpster fire of misinformation. There’s a middle ground here between unviable captured news orgs and the free-for-all that is social media if we harness all the tools available to us to deliver it.


*(2 more replies not shown)*

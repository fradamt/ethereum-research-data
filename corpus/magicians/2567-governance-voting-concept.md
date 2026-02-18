---
source: magicians
topic_id: 2567
title: Governance Voting Concept
author: RexShinka
date: "2019-02-01"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/governance-voting-concept/2567
views: 1866
likes: 43
posts_count: 23
---

# Governance Voting Concept

# Governance Voting Concept

## Why?

1. I feel Ethereum desperately needs an agreed decision making process before the next difficult decisions occur.
2. Has to be something we can implement now, using existing technology.
3. Has to be public and fair (though that is very relative).
4. Barriers of entry must be low and fair but not nothing. .
5. This paper puts forth the concept for discussion. It is not a complete system with all the rules needed. If there is enthusiasm, it could be quickly matured.
6. This concept is a system for |Ethereum as it is now. As the ecosystem matures, this must mature also.
7. Everything is up for discussion.

## Summary

This topic proposes a voting system that can be developed and implemented in a short period of time. The system divides the Ethereum population into rings (miners, developer, core devs, security, users and traders). Each ring creates their own voter list before any votes using their own criteria, distributes tokens and have a DAO that allows votes.

Each ring has a set fraction of the votes adding to 100%. When there is a vote, each ring votes with their list voting list. The result counts for their fraction of the vote.

Anyone can propose a vote. All votes have to be approved by a volunteer subset of the rings. The intent is to remove trivial votes. The distribution of the rings can change depending on the topic of the vote. So a vote on the mining payout would have higher emphasis on the mining ring.

[More details with an example](https://docs.google.com/document/d/1blgF0Ha8CfxyrHk9OBexR41VevCvnvR0m9YNcCf6Pqs/edit?usp=sharing)

This is a specific example of the Primordial soup article [How the Ethereum community could begin making meaningful signaling-based decisions](https://ethereum-magicians.org/t/how-the-ethereum-community-could-begin-making-meaningful-signaling-based-decisions/694)

## Replies

**boris** (2019-02-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rexshinka/48/225_2.png) RexShinka:

> I feel Ethereum desperately needs an agreed decision making process before the next difficult decisions occur.

Maybe you can give some more examples or explain why you feel this way?

There is not a lot of support for formal voting in the main principles of EthMagicians (I’m explaining here, not agreeing / disagreeing with you). Specifically, “rough consensus and running code”, which comes from the IETF.

This doc has more info – [RFC 7282 - On Consensus and Humming in the IETF](https://tools.ietf.org/html/rfc7282), and here’s a quote:

> We don’t vote in the IETF.  In some ways, we can’t vote: Since the
> IETF is not a membership organization, it’s nearly impossible to
> figure out who would get a vote for any given question.  We can’t
> know who the “members” of any given working group would be at any one
> time, and we certainly can’t know who all of the “members” of the
> IETF would be: That’s why we refer to “participants” in the IETF; the
> IETF doesn’t really have “members”.  Indeed, we often recruit
> additional implementers and other experts into working groups in
> order to ensure that broader views are brought into the discussion.
> So, voting is simply not practical.

---

**RexShinka** (2019-02-01):

For the past year public pressure on Ethereum has reduced significantly. Development efforts are still very strong along many fronts. This should be a time when our internal management and decision-making processes should improve. We have a lot of requirements that need discussion and the crazy external pressure felt in 2017 is dramatically reduced.

However, I feel the rough consensus model is not improving. I am strongly building a feeling that retention of rough consensus is one of the biggest risks to Ethereum going forward. The decision-making process has been slow, difficult to track and almost impossible for outsiders (who don’t understand the Ethereum) to comprehend and have faith in you.

It is quite possible that with side chains and new user interfaces like burner wallets, Ethereum may have real financial usable applications in the near future. I do not feel we will be equipped for the pressure and I don’t see improvements coming quickly enough.

Two specific examples are 1)  the decision-making process for the reduction of the mining reward.  The core developers did their best to include all stakeholders and I believe they came to a good decision. But the process was slow and considering the value ramifications extremely primitive. It was also quite centralized.  2) The decisions on security reviews for the latest Constantinople release. From what I understood from the EthSecurity Telegram chat the decisions on the review process were not as open as they could have been and the overall budget for the reviews not very large at all. The result was something that could be viewed by outsiders as quite amateur and smalltime. Given the maturity of Ethereum this should not be happening now.

For this reason, I think vehicles for real decisions can be developed and must be developed. The systems can be more open and effective than what we are using presently. Most decisions should be done using rough consensus. I completely agree with that. However, contentious decisions (such as what to do with the locked funds) should not be avoided or it will be difficult for the outside world to have faith in our system.

I will be the first to admit that one coin one-vote is far from ideal. However, I think decision-making processes are possible, workable and needed. There is plenty of room for innovation and change. I think decision-making processes are something we can lead the world in. We have a wonderful opportunity. What we need is not high level of philosophical discussions such as those between Vlad and Nich.  We need to start implementing processes.

---

**fubuloubu** (2019-02-01):

I would say I widely agree, we need a bit more structure and hierarchy to the decision-making processes in order to reduce noise and increase effectiveness.

Specifically relating to DAOs, I don’t think we need that yet. Many rings (and we have a lot of them) have self-organized to some varying degrees of success at continual working-group style meetings. I believe this type of effort would encourage broader participation along narrow subject bands, and could serve to focus some of the energy in the community if adopted. We don’t need a formal DAO for any of them yet, they’re not that big yet (at least in terms of formal participation). Even the security ring, at 250 members, we only see about 10% participating on a regular basis. That is enough for informal governance to work efficiently.

We can adopt “Rough Consensus and Running Code” both within and *across* these subgroups as an organizing principle. The purpose of the groups is to focus energy, to give those interested in certain topics a curated feed of information for them to digest and act on.

What we have currently is a floodlight, an unrelenting torrent of energy dispersed in every possible direction. What I want is a bunch of *lasers*, focusing energy into a directed stream of power, and focus those lasers towards a single point of massive power and effectiveness. A few of them might get misaligned, but even one laser is more effective than a floodlight at cutting through the crap and getting into the deeper issues. </terrible-analogy>

---

**boris** (2019-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rexshinka/48/225_2.png) RexShinka:

> the decision-making process for the reduction of the mining reward. The core developers did their best to include all stakeholders and I believe they came to a good decision. But the process was slow and considering the value ramifications extremely primitive. It was also quite centralized.

Fun fact: this decision is not confirmed yet ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) Anything the Core Devs consider to be political tends to be problematic. As [@fubuloubu](/u/fubuloubu) points out, rings / working groups that can take on specific issues, fold in experts, and then come back with a recommended decisions and/or process (see: [Signaling Ring](/c/working-groups/signaling-ring/19)) seems like a workable way to scale decision making.

I have no idea what the word “centralized” even means any more. Anyone can propose EIPs, anyone can develop code, anyone can suggest that EIPs are included in hard forks. Does a bunch of that take work and expertise? Yup!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rexshinka/48/225_2.png) RexShinka:

> The decisions on security reviews for the latest Constantinople release. From what I understood from the EthSecurity Telegram chat the decisions on the review process were not as open as they could have been and the overall budget for the reviews not very large at all. The result was something that could be viewed by outsiders as quite amateur and smalltime. Given the maturity of Ethereum this should not be happening now.

Most of Ethereum is still amateur and smalltime. Lack of funding, lack of process. Should “we”* have a budget per EIP / per hardfork? Looking at the [Istanbul roadmap](https://en.ethereum.wiki/roadmap/istanbul), it’s not clear where security reviews fit in.

Do each of the Ethereum client teams have a dedicated security person?

**“we” effectively means the EF at this point, since there is no other we with a bucket of funds.*

Anyway, I broadly agree with you – but pretty much I see “voting” as getting involved in the EIP and core dev process. Which is open to anyone.

The ETH1x process is going to be a real test of this.

---

**fubuloubu** (2019-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Looking at the Istanbul roadmap , it’s not clear where security reviews fit in.

Looking at that testnet deploy date, that would be my ideal time to get some security people involved, including a few teams on retainer, to do a deep dive into the EIPs and their interplay. (I wrote about that somewhere… Ugh, forgot!)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Do each of the Ethereum client teams have a dedicated security person?

Yes. Parity has [@kirushik](/u/kirushik), and Geth (really the EF) has [@holiman](/u/holiman). Still just two people, not enough IMO for a deep analysis even though they do exceptional work. Pantheon also probably has a great team that is hopefully more directly involved in the next hard fork.

I’m not sure what the QA process looks like with either of these teams (I am sure it is adequetely handled!), but QA per feature is not a good substitute for a deep dive on a pending release (frozen codebase, the whole nine)

I’ve said it before (somewhere…), and I’ll say it again: EF needs to put at least 2 teams on retainer for the next hard fork when it is released to testnet (or even leading up to that, to reduce coordination costs of the testnet fork). It shouldn’t cost more than $80k hopefully, and it’s only every 9 months. I’m sure more than that was lost collectively in the ecosystem over the last roll back. Heck, maybe even the news sites can put some money in from the funds they’d be saving not covering such an event.

---

TL;DR: Set up a recurring hard fork audit fund, have some matching funds or whatnot, and get saving! (or sign a retainer)

---

**RexShinka** (2019-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Most of Ethereum is still amateur and smalltime. Lack of funding, lack of process.

Ethereum is the most mature Blockchain to date. If Blockchain’s are going to be a real part of the global finance and business it will need a better decision-making process that it has today. All I am suggesting (On the magicians for them because it is the best platform for this discussion) is that we look at an improved process to use to document decisions from the community.

We are in a unique situation where we can experiment, make mistakes and improve with relatively little ramifications. We should take advantage of it. Frankly, I would like to see us move to quadratic voting soon, but that is a couple of steps further out.

Therefore, I think the question of community voting through some process should be opened up.

---

**holiman** (2019-02-04):

Regarding our security team, it’s a bit of a mix between security and testing. On testing, we have @winsvega who’s mainly focused on consensus tests. We maintain two fuzz-testing frameworks, one based on hive and and one libfuzzer, for doing cross-client consensus tests.

The following people are involved in ether vanilla testing or fuzz-testing: Piper Merriam (testing), Holger Drewes (testing), [@cdetrio](/u/cdetrio)  (fuzzing) , @tintin, [@wtf](/u/wtf) (Anuj), @Cryptomental (libfuzzer-fuzzing), [@FrankSzendzielarz](/u/frankszendzielarz) (hive) and myself (hive/fuzz).

Security *reviews* of EIPs have *implicitly* been part of the  acceptance discussion. My hope is that it will be *explicitly* part of the process from now on. After that comes the security *testing* process, which is what we’ve been building up the capacity for ever since the dao fork (when hive was first created), through the shanghai-forks (which spurned the first fuzz-testing framework).

One of the main points we’ve learned over the hardforks is the importance of getting the features in as soon as humanly possible, so they can be activated for fuzz-testing and verified by other people than the core developers who have all the tools for debugging/testing within the go-specific rust-specific test harnesses.

---

**fubuloubu** (2019-02-04):

Nice, it definitely sounds like the process is maturing, and that is a good thing. The last thing I’d like to advocate for is involving external review at the point of go/no-go testnet release, have one or multiple fresh, outside perspectives can often highlight when a critical assumption is wrong prior to the final release process starting. Internal teams are great for the heavy duty work, but you really need the out-of-the-box thinking that outside perspectives bring.

---

**holiman** (2019-02-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> The last thing I’d like to advocate for is involving external review at the point of go/no-go testnet release

I personally would like to start testnets sooner, since those are the playgrounds for developers and users alike to try out features and root out bugs. As [@karalabe](/u/karalabe) outlined in his EIP/EEF, even on a busy testnet we can make a rollout without announcing it – doing the fork as a sidechain which will die after a short amount of blocks, but still getting the replay transactions from the non-forked testnet.

At the point where it’s already implemented and ready to roll out, the EIP itself should be already vetted (before being finalized). It’s in that vetting-process where I think external contributions would be most useful.

---

**fubuloubu** (2019-02-04):

I definitely agree, I think each individual proposal is getting enough attention as it is. The process has been a journey, but things are going well.

I think the complex interaction of multiple proposals and the existing assumptions of the chain definitely warrants that type of deep, external review. This occurs best when a testnet release has been completed, so potential issues can be explored in practice.

---

I definitely agree with the fact that there needs to be more of a formalized release schedule, so we can come to those decision points sooner and avoid last-minute changes.

---

**gcolvin** (2019-02-28):

Pulling this from a cat-herders post.  The problem I’m seeing is how, as an anarchic (non-hierarchical) community, we come a consensus as a whole.  As a start I think various stakeholders need to self-organize to develop and express their own consensus.  I want to hear from the miners themselves, from the investors, from the developers, from any other self-organized group.  If they don’t care enough to get organized I don’t care about counting their coins or their opinions.

[@lrettig](/u/lrettig)

> I appreciate your opinion and respectfully disagree. FEM is purely focused on technical merit. Core developers would like to be, but in the absence of a more mature governance mechanism, we have to consider more than pure technical questions. As one concrete example, I care a great deal about ethics as well.

As ever, I like for my opinions to be challenged. And we may agree more than we think we do.

Ethics I take to be a core value of our community, so I would surely block consensus on ethical grounds. I don’t know of a core developer who wouldn’t. So I see ethics as a constraint on all of our jobs.

I agree that decisions fall to the core devs that we are not comfortable making. So I’m reaching out to the community for help. “The health of the network” is where the core devs get to issues that might not be purely technical, but still within our responsibilities and open to objective discussion.

Since the health of the network requires the health of the community, and vice versa, I think there is plenty of room for presenting evidence, analysis, and the consensus of other groups in the community to the core devs in terms of the health of the network. We can engage with information like that in forming our own consensus.

But when the core devs can’t come to consensus on what software to build on the basis of technical merit or the health of the network we are up against the limits of our governance, and opinions per se are of little help. The consensus of stakeholders in the community, or even the community as a whole, is what I would want to see, and what we are not yet organized to achieve.

Knowing opinions can be useful in guiding the herding of cats, but I do think that low-quality information does more harm than good, and having a lot of it doesn’t really help. There are statistical and social aspects to that argument that are deeper than I can get into now.

---

**lrettig** (2019-02-28):

Thanks for bringing up this important topic and sharing your perspective, Greg.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Knowing opinions can be useful in guiding the herding of cats, but I do think that low-quality information does more harm than good, and having a lot of it doesn’t really help. There are statistical and social aspects to that argument that are deeper than I can get into now.

I’d be curious to hear what those arguments are. As you know (I’ve said this many times), in the absence of perfect signals – and we clearly do not have perfect signals – I’d prefer an array of noisy, imperfect, messy signals over no signals at all. I’m open minded about this and happy to be convinced otherwise.

Progpow and http://www.progpowcarbonvote.com/ is a good example. I know that only a tiny, tiny fraction of all ether has voted. But I still see value in this signal. Not just in the vote itself, but in the second-order effects and actions such as [@koeppelmann](/u/koeppelmann)’s vote (https://twitter.com/koeppelmann/status/1096017086198046722) and the way people responded.

---

**RexShinka** (2019-02-28):

For me, this topic has evolved to a need for an independent signals group. A signals process will allow people from the various stakeholder groups to be heard. If the results are considered indicative then it provides very useful information to the core devs who, at present, for the most part make the decisions.

It is clear to me now that the Ethereum Foundation nor the FEM will or even should organize this signals group. It should be an independent organization that remains impartial, gathering information and refining the process. The process, as I indicate in the example above, does not need to be perfectly decentralized. Our processes are not ready yet.

But we do need effective signals and a process that we start with and improve upon.

---

**jpitts** (2019-02-28):

The Signaling Ring is to meet at the Council of Paris, it seems to be organized by Daniel Kronovet [@kronosapiens](/u/kronosapiens). Perhaps this is where an independent signals group may emerge; Magicians’ Rings are highly independent / self-organized.

There have been meetings in Berlin and Prague as well, plus discussions here: https://ethereum-magicians.org/c/working-groups/signaling-ring

---

**RexShinka** (2019-03-01):

Thanks I will reach out to them and may be able to find time to remote attend some of the meetings.

---

**kronosapiens** (2019-03-01):

Hi [@jpitts](/u/jpitts), I am planning on attending the signaling ring but I had not been intending to organize. Am I registered as an organizer somewhere?

---

**jpitts** (2019-03-01):

I was saying that because you are the first one on the list ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) I may be able to attend as well, and there will probably be more as the Council gets closer.

---

**gcolvin** (2019-03-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> There are statistical and social aspects to that argument that are deeper than I can get into now.

I’d be curious to hear what those arguments are.

The statistical issue is just that distinguishing signal from noise is a deep problem, and having lots of noisy measurements doesn’t help much if you don’t know the distributions and covariance of the noise, and don’t have a decent model of the signal.

The social issue is that this is published polling data with little statistical or empirical basis. (Per above.)  So it can’t really be interpreted objectively, and we risk yet more opinion-driven divisiveness.  It’s self-organization, deliberation, and consensus we need, not noise.

---

**RexShinka** (2019-03-02):

My vision is for a funded organization with a full-time person or two that actively work to bring out statistically valid signals. At this point I think we should aim for the active elements of the community. We push to get the developers, miners, traders to respond, such that their signals are relevant. For the core developers and the security experts these are extremely small communities so getting there signal will be much easier. Getting good data from the users and the holders of the eth coin will be more difficult.

I also do not believe that self organization of the community will be very effective. You need a small core of good people willing to spend time consistently in order to achieve results. Based on my experience with the EthSecurity organization (which is a fabulous active intelligent and motivated community), working on elements that aren’t core to their priorities (in this case the security aspects) just doesn’t happen enough.

I cannot see these organization people working as volunteers. The level of effort is too high. In addition, they have to be non-aligned.

I think statistically valid signals that are accepted by the community are achievable, but will require active work. The process will start out primitive and not fully decentralized but can rapidly evolve as the tools evolve.

---

**gcolvin** (2019-03-02):

I hear you, but the community is unable to fully fund development, let alone signal gathering.  And to an extent I really don’t care about these signals.  If a group of stakeholders cares enough to get organized then I want to hear what they have to say.  If they don’t care enough then why should I?


*(2 more replies not shown)*

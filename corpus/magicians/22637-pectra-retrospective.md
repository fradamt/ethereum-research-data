---
source: magicians
topic_id: 22637
title: Pectra Retrospective
author: timbeiko
date: "2025-01-23"
category: Magicians > Process Improvement
tags: [pectra, upgrade-retro]
url: https://ethereum-magicians.org/t/pectra-retrospective/22637
views: 2850
likes: 113
posts_count: 34
---

# Pectra Retrospective

On [ACDC#149](https://github.com/ethereum/pm/issues/1258), we agreed that before jumping into Fusaka planning, we should stop and reflect on Pectra. More broadly, we’ve recently seen [many questions](https://ethereum-magicians.org/t/l1-vs-everyone-else-coordination-expectations/21971), [strong criticism](https://ethereum-magicians.org/t/ethereum-s-social-layer-is-broken/22297) and [novel improvement proposals](https://ethereum-magicians.org/t/blob-parameter-only-bpo-forks/22623) related to AllCoreDevs (ACD).

To keep the conversation tractable, I’d suggest using this thread as a coordination point to share retrospectives and analyses of ACD, as well as proposals for how to improve things. While it’s fine to highlight problems without necessary having a solution to them, hopefully we can keep the conversation civil and productive ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

I’ll use this top post to categorize high-quality responses from **Client Teams**, **Infrastructure Providers & Developers**, and **Misc. Users / Community members**.

In a few weeks, we’ll dedicate time on ACD to discuss what came out of this discussion.

---

While I don’t want to overly constrain how feedback is provided, here are suggested starting points for reflection:

- Over the past year, what went better than expected in Pectra’s development and/or ACD generally? What caused this?
- Over the past year, what went worse than expected in Pectra’s development and/or ACD generally? How could we have prevented this?
- Looking forward, what should we start doing, stop doing and/or do differently?
- What should we not compromise on, even if there is pressure to do so?
- What parts of ACD are “legacy process debt”, which we should consider rethinking from first principles?

As we discuss this, we should deeply consider the second-order impact of proposals. For example, it’s often suggested that ACD should be “more efficient”. On the surface, no one would disagree. That said, it’s easy to see how there’s a tension between speed and other aspects of the process, such as security, openness and biasing towards work that has less “unknown unknowns”.

This isn’t to say that we shouldn’t try and make the process more efficient, but that we should be mindful of what we tradeoff to get those efficiency gains.

## Replies

**abcoathup** (2025-01-26):

# Community response

Summarized ACD calls async for 3.5 years (former editor of [weekinethereumnews.com](http://weekinethereumnews.com)).

Collected summaries/writeups in https://ethereum-magicians.org/c/protocol-calls/63

---

## Better

**ACD summaries**:

[ACD call](https://ethereum-magicians.org/tag/acd) summaries of actions/decisions written by moderators on Eth Magicians, generally within 24 hours (thanks [@timbeiko](/u/timbeiko) & [@ralexstokes](/u/ralexstokes)).

**Scoping priority writeups**

Client team writeups of scoping priorities: e.g. [Reth](https://www.paradigm.xyz/2024/01/ethereum-2024), [Lighthouse](https://hackmd.io/@dapplion/lighthouse_pectra), [Lodestar](http://blog.chainsafe.io/lodestar-proposals-for-next-electra-cancun-fork) & [Prysm](https://medium.com/offchainlabs/prysm-electra-upgrade-f827c20d0fd2).  Allows for considered async review/response.

**ACD stream/recording**:

Adding the chat to the stream/recording of ACDC.  The chat is where much of the discussion happens and contains a large amount of context.

## Worse

**Scoping**:

Pectra was originally pitched as a small upgrade targeting end of 2024 (before Verkle), it became the largest upgrade ever (even after being split), targeting Q1 2025.

Planning started formally in January 2024 and the scope for the first half was finalized in December.  We ended up with too many EIPs being included over many months, with the rush to get in before Verkle put everything on hold. (the irony being that this delayed Verkle so much that Verkle might not be used for statelessness, and statelessness may not be the highest priority on the roadmap anymore).

## Start

**Roadmap**:

Upgrades should be driven by a public multi-year roadmap.  This roadmap can and should be subject to change.  EIPs should generally only be *considered for inclusion* if they significantly move the roadmap forward.

**Informal Veto**:

Rough consensus should include an informal veto of EIP inclusion by:

- Client teams considered to have greater than one third market share.
Currently assumed to be only Geth & Nethermind.  As an example, Geth were strongly against EOF, as they were a majority client at the time (with all the responsibility & pressure that this status entails) they should have had a veto.  If we don’t want teams to have this power then the community can remove it by improving client diversity.
The veto should only be informal, to ensure that rough consensus isn’t captured by any one participant.
- DevOps.
If EthPandaOps believe they can’t safely test a combination of EIPs (or sheer number of EIPs) then those EIPs should be proposed for inclusion in a later upgrade.  As an example ethPandaOps call for a Pectra split

## Stop

**Saying yes**

We want to accelerate upgrades, increasing the reach rather than widening the scope, so we need to stop saying yes to EIPs that don’t significantly move the roadmap forward.

We need to heavily use *denied for inclusion*, regardless of how much good work/effort people have put in, EIPs should be weighed against the roadmap, and hurt feelings aren’t part of this equation.

## Do differently

**Scoping**:

At the start of each upgrade cycle, authors should *propose for inclusion* EIPs that move the roadmap significantly forward.  EIP authors/champions should add a 5 minute presentation (video & slides) to their EIP discussions topic in Eth Magicians.

This would allow client teams & the community to review them async. (without having to discuss on ACD).

Client teams (and the rest of the community) could writeup which EIPs they believe based on the roadmap should move to *considered for inclusion* or *declined for inclusion*.

A proposed scope of *considered for inclusion* and *declined for inclusion* can be created.  ACD can decide on the remaining EIPs where there isn’t rough consensus on CFI or DFI.  If needed those authors could take questions (depending on the number this should be a breakout).

The proposed scope can then be updated.  Client teams having the opportunity to estimate the effort involved, along with recommending any changes to CFI or DFI.  Informal vetos could also weigh in.

**ACD**

ACD should be the venue for (synchronous) decisions.  Outside of scoping, ACD should be short, ideally 30 minutes.  Any discussions should be time boxed (e.g. no more than 10 minutes).  If longer discussions are needed then these should move to a breakout or async.

The agenda should clearly indicate what decisions are to be made and the agenda shared widely.

New EIPs shouldn’t be presented at ACD, instead authors/champions should create slides & a five minute video to review async.

Any mic issues should bump a presenter to the next call. #micDAO

**ACD chat logs & transcripts**

Chat logs (where there is a lot of contextual discussion) & AI generated transcripts should be made available within 24 hours of the call.  ([@nicocsgy](/u/nicocsgy) is on the case).  These can be stored in [GitHub - ethereum/pm: Project Management: Meeting notes and agenda items](https://github.com/ethereum/pm) and replace the current manual transcripts and third party call writeups (which often take weeks to appear).  We should also copy the moderator summary from Eth Magicians to the call folder in ethereum/pm.

## Not compromise

**Rough consensus**

Decisions are made by rough consensus.  Clients have a variety of owners, including an L2, a VC and the EF.  Other than the proposed informal veto, no ACD participant should have special status.   Roadmap, CFI/DFI should all be decided by rough consensus and avoid ACD being captured by any one group.

**Scoping process**

Fusaka upgrade should be treated as a clean slate, rather than waiting for Glamsterdam.  All EIPs should be reset to *proposed for inclusion* and reviewed against the roadmap.  PeerDAS and/or EOF may end up being the only EIPs to be *considered for inclusion*, but we should also look at FOCIL, ePBS etc and choose only the EIPs which will significantly move the roadmap forward.

## Legacy process debt

**EIP process**

ACD should own the EIP process or at the very least have the process work for them.  It should be fast and easy to get an EIP to draft status.  This was one of the goals with splitting out ERCs from EIPs.

Just as ERC now has a funded role for ERC & standards coordinator, we (EF or another group such as the Protocol Guild) should be funding an EIP coordinator.

---

**abcoathup** (2025-01-26):

![image](https://www.paradigm.xyz/favicon/favicon.ico)

      [Paradigm – 25 Jan 25](https://www.paradigm.xyz/2025/01/ethereum-acceleration-1)



    ![image](https://cdn.sanity.io/images/dgybcd83/production/5aa3b171c8060cecd279fc2c51d57e8f41981a7d-2400x1350.png?auto=format&q=75&w=1200&format=png)

###



Paradigm is a research-driven crypto investment firm that funds companies and protocols from their earliest stages.

---

**ileuthwehfoi** (2025-01-27):

I think the Paradigm Ethereum Acceleration post is totally correct that ACD is a bottleneck and that client developers should not be the primary decision-makers. I don’t think this is desirable for anyone, not even the client developers, who have too much responsibility and have to constantly make controversial and stressful decisions they shouldn’t have to.

I think the main issue with Ethereum development is that we’ve erroneously felt that “sufficiently decentralized” means that the process has to be an entirely organic process. Devops came about when people adapted industrial engineering concepts to the environment of the server. We should also be able to adapt principles from devops to design efficient processes which are nevertheless still decentralized.



      [x.com](https://x.com/nelsonmckey/status/1883657860154110167)



    ![image](https://pbs.twimg.com/profile_images/1783341211539116032/LYbAebCr_200x200.jpg)

####

[@nelsonmckey](https://x.com/nelsonmckey/status/1883657860154110167)

  @TimBeiko Maybe if I had to steelman it, that Ethereum is so complex and the research process is so organic that some majority of development planning only happens on testnets as speccable solutions emerge.

Therefore we’re at terminal velocity for a sufficiently decentralised approach.

  https://x.com/nelsonmckey/status/1883657860154110167










We don’t even have to start from scratch. In my opinion, the development of Kubernetes provides a good starting point as an open source project which releases complicated yet robust software on a regular cadence, without any [single party or person](https://github.com/cncf/foundation/blob/main/project-maintainers.csv) being in control.

I want to make three [concrete](https://x.com/lightclients/status/1883634292024303973) suggestions:

1. Have a fixed, regular release schedule and cadence.
2. Formalize breakout rooms to be the primary venue for feature development, consideration, and prioritization.
3. Replace ACD with a dedicated steering committee led by an elected release coordinator.

There is a industrial engineering principle which keeps being [independently developed](https://www.amazon.com/Goal-Process-Ongoing-Improvement/dp/0884271951) which is that when setup for a particular process is slow, it will always have delays. Because setup is slow, the tendency is to make the batches large so that the impact of setup time becomes less. However, the large number of changes results in [added complexity](https://x.com/peter_szilagyi/status/1856353010349400398) which results in delays. This leads to a vicious cycle where more changes are piled on, resulting in more delays, because if you miss your chance there are no guarantees for when your change can get in. The solution to this is actually to make the batches smaller. Small and simple changes are less likely to cause delays, and the large setup time provides an incentive to dedicate resources towards automation. It must be regular so people know that missing the fork does not mean the end of the world. Kubernetes releases a new version every [15 weeks](https://kubernetes.io/releases/release/). I think Ethereum should be able to do something similar: perhaps something like 10 weeks for development into a code freeze with 5-10 weeks of [testing](https://x.com/potuz_eth/status/1883637971976692016) (decreasing as testing infra gets better and more automated, and possibly overlapping with the start of development for the subsequent fork). There should be no delays: if a EIP isn’t ready for testing or fails testing, it gets dropped, you can bring it back when it’s ready. Nor should any single client failing to be ready hold up everyone else.

In Kubernetes, feature development is handled by what they call Special Interest Groups ([SIGs](https://github.com/kubernetes/community/blob/master/governance.md)). In my opinion, ACD has no business in deciding something like which of two blob changes should be prioritized in a fork. Instead, there should be a Data Availability SIG, consisting of both researchers and developers and which is open to the public to view and contribute to. Instead of EIPs being opened by a single person who then has to shepherd it into existence (or more likely, get completely burnt out), the SIGs should have their own [separate forums](https://github.com/kubernetes/community/blob/master/sig-list.md) for the purpose of research, consensus building, and development. Something like specifying an EIP should be done entirely within the relevant SIG. For each fork, the SIG should decide which specified EIPs they want to prioritize for each fork and work with client developers (who should also be members of relevant SIGs) to ensure that they make it in. Alternatively, dedicated groups like SIGs may find that they can deliver features without requiring a hard fork: it’s my opinion if there was a rollup SIG the ball would have started rolling much earlier with interop than it did.

This results in decision-making and planning being taken out of ACD, arguably rendering it unnecessary. The main thing left is coordination, which can still be done via a regular group call, but which is probably better done informally, through temporary committees, or by a dedicated team headed by a [release coordinator](https://kubernetes.io/releases/release-managers/). Decentralization can be added by having the release coordinators be [elected](https://github.com/kubernetes/community/tree/master/elections/steering/2024) or selected by sortition from valid candidates, starting by [shadowing](https://github.com/kubernetes/sig-release/blob/master/release-team/shadows.md) the current coordinator and then rotating into the role for the next fork.

These changes would remove the bottleneck that is ACD, separate planning from execution and allow them to happen in parallel, distribute power from client developers, add transparency and predictability to the fork process, and provide support to EIP owners and newbies entering the space.

---

**timbeiko** (2025-01-27):

Thanks for sharing [@ileuthwehfoi](/u/ileuthwehfoi)! I wasn’t aware that Kubernetes was structured this way. I’ll dig into it more!

---

**philknows** (2025-01-27):

> There should be no delays: if a EIP isn’t ready for testing or fails testing, it gets dropped, you can bring it back when it’s ready. Nor should any single client failing to be ready hold up everyone else.

I’m curious how anyone sees this working in the context of Ethereum where hard forks require a simultaneous upgrade involving all clients of various speeds. Leaving one client behind creates chaos for that group of users, especially if they’re a widely used client.

I’m sure we can do better with coordinating consensus-only forks or execution-only forks, but this will still involve at least 5 teams to ship together and leaving one or two behind will only exacerbate consolidation when we need to have *more* client diversity due to inevitable client bugs.

In addition, depending on what is contained within the SFI’ed EIP and how much of the codebase it affects, it can be difficult to just drop a feature last minute because someone else was running behind. The interconnectedness and dependencies between some EIPs for inclusion will require utmost care and robust coordination for success, including the order of which EIPs are implemented. *A lot* of the problems/delays happen during the client implementation phase where we discover many unforeseen issues, and not in the proposal phase (see EIP-7549 - theoretically easy, practically difficult).

This could be made easier by enforcing smaller, regular forks as suggested, but leaving a client team behind on a hard fork or dropping/changing the scope last minute seems very impractical.

---

**rkapka** (2025-01-28):

I think the main point of this article - that we have to ship more things faster - doesn’t think about core developers in the least.

Developing Ethereum is like climbing an infinite mountain. Even if you think you are at the peak, you realize that it’s not the real thing yet and there is a higher place to climb to. And that’s fine in itself, after all the journey is more important than the end goal. Because once you reach a goal, there’s nothing more to do.

But imagine you are a hiker going up that mountain. Would you rather try to reach the “top” as quickly as possible without stopping or hike at a comfortable speed, taking breaks to sit down by the stream, eat a sandwich and listen to the sounds of nature?

Researchers and core developers are these hikers. Writing a client is not only about implementing EIPs. There are specification items outside of EIPs, client-specific features, maintenance, bug fixing, testing, tech debt, … It all takes time.

> We think ossification is too risky for Ethereum. It prevents Ethereum from staying competitive as a platform, as applications and users move toward more centralized alternatives.

Bitcoin is as ossified as one can get, and it’s been at the top for the last 15 years. Ethereum is not going anywhere. Will it become less competitive if we ship less? Sure. Will another L1 overtake it? Maybe. Is it the most important thing in the world? No.

I know I am only criticizing and not proposing how we change things. I do believe that we can improve on how we approach things and I am sure many will have great ideas. I just don’t buy the “do more, and do it faster” slogan.

---

**asn** (2025-01-28):

Thanks for the thoughtful comments [@ileuthwehfoi](/u/ileuthwehfoi)! I agree with you on many points! I’ve been trying to type this post for days; but you made it significantly easier. Here comes thoughts and lists!

---

I think this latest fork has shown that ACD calls, while a fun social experiment and a decent venue for technical discussions, might not be the ideal place for major governance decisions in Ethereum.

What kind of decisions does ACD typically handle?

- Which features should be in the next fork initially?
- When should the next fork happen?
- Adding/removing features mid-cycle as development progresses
- Deciding if a fork should be delayed or expedited

And now, here are a few reasons on why ACD is a poor place for decision-making. I’m sure there are more:

1. Too many cooks in the kitchen. This is a problem for a bunch of reasons:
a. Yapping can take valuable time and literally wastes 100 people’s time
b. Conversely, people with important things to say might stay silent because they fear taking up space, or because it might serve them better to stay silent and it’s easier to do so in a huge zoom call
c. A big group is inherently less agile: A small, focused team can often reach decisions more effectively and quickly.
2. Lack of accountability. The lines of responsibility are fuzzy.
3. Lack of structure. There is an agenda, but sometimes the zoom call needs to go on to the next topic proposed in the
github issue, and an important decision gets shelved.
4. Things will only get worse. As the number of developers, client teams, and stakeholders grows, the Zoom call chaos grows with it. Without a more structured governance approach, ACD calls will become even more unwieldy.

IMO, the natural step forward here is to introduce a **smaller public “steering committee”** that serves as the decision-making body of Ethereum, while keeping ACD as the technical dev call. I’m not gonna go deep into how we should compose, choose or name this steering committee, to avoid natural bikeshedding.

Instead, I will spend the rest of this post addressing the all-time-classic knee-jerk reaction “ACD is decentralized but a steering commitee is not!!11”:

- There’s a misconception that a 100-person broadcast channel automatically gets you the “decentralization” sticker. Some even conflate decentralization with chaos and disorder, murmuring phrases like “yes kid, the process sucks, but that’s how decentralization looks like…”.
 Decentralization for decentralization’s sake can lead to bad outcomes. Instead of an appeal to decentralization we should think what security properties we want from our governance body. When people chant ~decentralization~ they usually mean “No single entity should be able to control the future of Ethereum”. IMO this does not require ACD in its current shape to be achieved.
- There is no reason to think of a 100 people zoom call as more secure compared to a smaller zoom call. Power imbalances, the tyrany of structurelessness, behind-the-scenes lobbying, and a bunch of other fun social phenomenons, can actually make the 100 people call more susceptible to manipulation than a smaller group.
- If the increasingly inefficient ACD keeps on being the governance body of Ethereum, the natural course of action is that key decisions will be taken in backrooms and ACD will just serve as a token of decentralization. I believe that if we enshrine a reasonable and efficient governance body well-in-advance we can avoid this failure case.
- Just think about it as broadcast vs tree-based aggregation. If the steering-committee includes (at least) all the team leads, then if you are at the leaf layer (just a client engineer or a poor researcher) you need to make sure you communicate your thoughts or concerns to your team lead and come to agreement. The job of the team lead is to then lucidly bring the thoughts on the decision-making body.

---

**ileuthwehfoi** (2025-01-28):

Yeah, so what I wrote is the ideal. Then there’s putting it into practice, which may be very different, particularly at the start.

For example, ideally the first fork would include only a few small features or even nothing at all. Instead, it would focus more on setting the system up with testing infrastructure and process automation. Then the people shadowing the first fork are prepared to lead the next one instead of trying to design the process and coordinate new features at the same time. But would the community accept that, or would they see it as delay and a wasted fork?

It’s similar with having an interconnected codebase. Generally speaking, the ideal batch size for new releases in software is one; the hippest startups release to prod after every single merge. For Ethereum, even if the client developers could achieve that, client operators would certainly revolt. Ideally the codebase should be completely modular, allowing for independent parallel development of the consensus and execution layers. Instead, we have codebases that are fairly coupled which probably have to fork together for the foreseeable future (until BEAM maybe?).

Still, when I describe dropping features or clients from a fork, I’m describing procedures which should not commonly occur. First off, EIP selection for each merge should take into account their degree of interconnectedness, either choosing ones that are as orthogonal as possible, or having the entire fork be dedicated to a single bundle of tightly coupled features (perhaps in a minor/major staggered release cadence, where minor forks are consensus only and major forks are execution + consensus, which gives the execution clients double the time between forks). Secondly, hard deadlines should make it easier to anticipate whether or not a specific feature is likely to make it in time, allowing for preparations like creating a contingency version of the fork with a particular feature pre-removed, along with scheduled code freezes to provide soft deadlines and buffer time.

Dropping clients should be even more rare, but I’m less worried about the consequences of that, because a regular release cycle means that client operators should be ready to update their infra at specific intervals in any case. Alongside multi-client, tooling to assist with switching clients is something which should be improved anyways.

Anyways, I’m not saying we have to cargo cult k8s development. But we should probably try to avoid the mindset that Ethereum development is entirely unique. Other complicated open source projects exist, and they have processes they run which Ethereum can learn from.

re: [@rkapka](/u/rkapka), I don’t think moving fast is incompatible with reducing client developer burnout, particularly if speed gains are achieved from better organization. Currently in ACD you have to pay attention to every potential EIP, but if we split things up and encouraged codebase modularization, then someone could decide they are only interested in the advanced cryptography special interest group, leaving things like networking to those who are more into it. There should be room for both hardcore and casual developers in Ethereum.

---

**rkapka** (2025-01-28):

[@ileuthwehfoi](/u/ileuthwehfoi) You’re right, I’m sure there are ways to make things more efficient. I will admit that I took this more personally than I should have, but I found the article very one-sided, with the word “faster” being used 11 times (I just checked), while there is 0 mention what are the trade-offs of trying to go faster.

What I wanted to emphasize is that we can’t forget about developers as human beings and not just elements of an abstract process.

> I don’t think moving fast is incompatible with reducing client developer burnout, particularly if speed gains are achieved from better organization. Currently in ACD you have to pay attention to every potential EIP

ACD is max 90 minutes a week (often around 60 mins), so attending it or not will make little difference. And the agenda is known beforehand, so you can tune in only for the interesting part.

---

**timbeiko** (2025-01-29):

For archival’s sake, I’ll post a proposal I made on [Twitter](https://x.com/TimBeiko/status/1883211325675110626): “I think the highest leverage thing we can do is moving to a world where once fork N is shipped, we assume the scope of fork N+1 to be final, and anything up for debate moves to N+2.”

Specifically, I would propose that we consider the scope for Fusaka frozen, only including PeerDAS and EOF in the upgrade (and potentially the CFI’d EIP-7212) and start debating the scope for Glamsterdam as we begin implementing Fusaka.

This would both keep the scope for Fusaka manageable (PeerDAS and EOF are both *huge* changes!) and save us time arguing over the fork scope while we are trying to implement it. When Fusaka ships, we’d consider the scope for Glamsterdam frozen.

---

**shemnon** (2025-01-29):

Here’s an idea I wrote up last year when I was reflecting on how the current devnet process was flowing: it’s basically a draft of what could be released.

The biggest feature is to keep devnets and make them so they could be shipped “on demand,” applying one of the learnings from Agile methodoligies.

My note also includes a half baked idea aboult larger features working independently of slotting.  However, I like Tim’s idea of N+2 is open for additions and closes when it becomes the N+1 fork better than my large fork idea.


      ![image](https://hackmd.io/favicon.png)

      [HackMD](https://hackmd.io/@shemnon/Draftnet-Driven-Deployment)



    ![image](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



Pectra's iterative approach really has solidified the use of devnets. But call them draftnets to make it clear "this is a draft of what we may ship." - and make it shippable.

---

**wminshew** (2025-01-29):

Strongly in favor of:

1/ smaller & more frequent forks (and generally learning from projects like k8s, though not necessarily adopting wholesale etc)

2/ locking fork N+1 when fork N ships

3/ regular retrospectives (such as this) after every fork

As an ~outsider to ACD, I don’t know if there’s any big pushback on making these three changes atm but they seem like a reasonable starting point to me. Can consider it an experiment and revisit in the next retrospective

Personally, I would love more information and decisions to happen asynchronously via text, but I also might just be missing the proper channels. I am actively working to get more informed and involved here, as our app/contract limitations are starting to bump up against the edge of what is possible across the ethereum+ landscape today.

Last, but certainly not least, I deeply appreciate all that you all have done and continue to do for the broader community. Thank you for your service ![:saluting_face:](https://ethereum-magicians.org/images/emoji/twitter/saluting_face.png?v=12)

---

**jflo** (2025-01-29):

Can we collect some concrete examples of when rough consensus has failed?

90% of the discussion on what goes into a hardfork revolves around “will it fit”.  I’d like to be sure we’re not mis-classifying estimation difficulty as governance (prioritization) problem.

---

**sophia** (2025-01-29):

We should aim for hard forks every six months beginning with Fusaka. There are many advantages of this:

- Easier to reach consensus on scope. We were still considering EIPs for inclusion in Pectra 75% of the way through its life cycle. Much of this is because not being included currently means waiting a whole year, during which the entire product and technical landscape will have changed. With a more frequent schedule, it would be easier to freeze the scope one fork ahead and ship on time because bumping a feature to the next release wouldn’t mean a long wait.
- Less social pressure wrt what each fork means for the future of the protocol. Ideally each fork would include a “big” feature, but it’s fine if some don’t.
- Easier to shift focus. We can decide a feature is so important that it’s the only thing we care about for the next fork, without permanently derailing everything else in the research pipeline. For example, FOCIL isn’t urgent right now, but that could quickly change. PeerDAS might already be urgent enough for us to place this level of priority on it.

It would be a big win to ship PeerDAS in September. I think this is the way.

---

**shemnon** (2025-01-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jflo/48/4288_2.png) jflo:

> Can we collect some concrete examples of when rough consensus has failed?

I would say we had rough consensus when EIP-1057 - ProgPow first got the green light.

Why did consensus fail? I don’t think we had a wide enough audience attention to the decision.  Maybe we should have waited a meeting cycle before declaring consensus.  But the real opposition formed away from the regular attendees of ACD.

I’m not so sure waiting an ACD with the declaration “we will finalize on adding EIP-1057 to the next fork” because things didn’t go south in earnest until a startup ASIC project de-cloaked and opposed it, I don’t know if they would have gone public unless it was committed.

After that, and eliding a whole lot of details, consensus moved slowly but only in one direction: don’t do it.

Moral of the story: rough consensus is not a contract written in stone (at least not until the fork activates).

---

**james-prysm** (2025-01-31):

> Instead of EIPs being opened by a single person who then has to shepherd it into existence (or more likely, get completely burnt out), the SIGs should have their own separate forums for the purpose of research, consensus building, and development.

(This is a person perspective and perhaps not from my team.)

Even though it’s proposed that these SIGs should include both relevant researchers and client devs, I feel like this might be a dangerous direction to go, the nice part of EIP leads shepherding is it makes the case on each team that this is important and there should be dedication to that item. If a relevant client team does not have the resources or interest to participate in the SIG wouldn’t they be alienated from that agenda? we may end up with a fragmented community. perhaps that is what “modular” means, but in this case, important contributors will be left behind and eventually pushed away.

---

**ileuthwehfoi** (2025-02-01):

I’m not totally sure I understand what you are saying, but I think it’s something like: under the current system client developers can passively allow EIPs to come to them, while the SIG system would require more active engagement which would strain smaller teams.

I’ve been thinking more about what the structure of SIGs should be for Ethereum, and currently I think this is one case where copying directly from k8s would be misguided, because k8s infra is naturally modular, while Eth is both coupled and diffuse. For example, if there was a SIG State Management it would own ABI, SSZ, RLP, and different Tries, some of which are irrelevant to you as a consensus client developer. So SIGs for Ethereum should probably not be based on research categories.

Instead, I think each Special Interest Group should own and try to maximize one particular key performance indicator of Ethereum. One possible list with examples of who would own different parts of the current roadmap:

- Censorship Resistance (FOCIL)
- Decentralization* (SSF)
- Moneyness (Issuance Curve, Marketing)
- Network Stability* (State Expiry)
- Privacy
- Scaling (PeerDAS)
- Security* (Self-Destruct, Post-Quantum)
- Ship Speed (Process Design, Documentation, Devnets)
- UX Applications (EOF)
- UX End-users (Interop)
- UX Validators (Verkle)

Notably many of these groups already exist in some form or another. EthStaker could slot directly into the UX Validators SIG. Some exist bifurcated in highbrow and lowbrow versions, like RIG and ethfinance for Moneyness. Others exist more informally, for example I understand there is a customary step where EIPs are evaluated for DoS before consideration for inclusion, which could take place more transparently in a Network Stability SIG. But some [don’t exist](https://x.com/Jai_Bhavnani/status/1886278489013203084), even though they probably should.

(*those marked with an asterisk would probably be more defensive/veto oriented rather than focused on feature creation, with a dedicated consulting location where other SIGs can ask for advice on EIPs they are considering, as well as dedicated seats in any steering committee).

First off, I think it’s entirely possible for even small teams to have members in all SIGs, as this means that there won’t be very many of them. I think basically every Ethereum developer is here because they are ideologically aligned with at least one of these goals, and therefore naturally would want to be part of a group which is working towards them.

Secondly, you can see it’s not actually necessary to have a representative in every SIG. For example, consensus client developers probably don’t need to interact at all with SIG UX Applications.

Finally, it should be noted that the purpose of SIGs isn’t to coordinate development. That is what the fork coordinator (or ACD) is for. It’s to coordinate decision-making: SIGs provide entry points for people to get involved, places to build consensus and collaborate, and unified groups to lobby for features. The intention is that the only thing a client developer has to do for the fork itself is to implement and test. As a result, it should be entirely possible for client developers to tailor their degree of involvement, including an entirely passive or purely advisory role if that is what is desired.

---

**NelsonMcKey** (2025-02-03):

Thanks for the post - just to clarify this is my attempt to present another side to the argument, not one that I fully believe. However there is some truth to it, and imo the easiest way to address this bottleneck is to have much earlier devnets, running in parallel with current process. So while we’re deploying Pectra, Testing Fusaka, we should already have a rolling devnet stood up for Glamsterdam in order to begin speccing and exploring target EIPs.

It won’t be possible to transition to this cadence immediately, but we should try!

---

**NelsonMcKey** (2025-02-03):

Two arguments being mixed together here. If an EIP isn’t ready, we should be comfortable moving it to the release after, in order to hit a regular delivery cadence. Confidence in the timing of the next release takes pressure off this decision.

However dropping clients (and whole sets of validators who run them) is a far more serious consideration and definitely not something that should become normal.

---

**marchhill** (2025-02-03):

The Nethermind team have discussed our opinions on increasing the rate at which we ship forks and thought of some ways to improve the process.

## Fork Scoping

We should aim to have a provisional plan for the next 5 hard forks, mapping Vitalik’s roadmap into concrete updates. There would still be flexibility to change fork scoping, especially more distant ones, but having this provisional timeline would greatly help in deciding where to allocate resources.

For imminent forks (within a year) we should avoid adding new EIPs to the scope unless they are already implemented and tested; and the current scope is live on a devnet.

Targeting a cadence of around six months per hard fork could help to prevent forks becoming too large. Large feature forks could be alternated with smaller forks focused on UX and quality of life improvements, giving more time to test complex new features; it is also crucial to consider cross-fork dependencies and plan accordingly.

## Parallelising Implementation

Having a clear plan can help to parallelise work on future forks. Once a fork is shipped, we could already have the next in devnet phase rather than starting to discuss the scope at that point.

## Specs and Testing

EIP champions should have greater responsibility in ensuring their specifications are rigorous in order to avoid differences in interpretation of the spec leading to delays. They should also coordinate with the testing team to create spec tests. Formalising and testing earlier in the process would save time overall.

Adopting EIP versioning ([EIP-7577](https://eips.ethereum.org/EIPS/eip-7577)) would help to coordinate implementing spec changes.

Furthermore, more resources could be allocated to testing, and client teams could be more involved.

## ACD Efficiency

Client teams should do more asynchronously before ACD to make the calls more productive.

Specifically, there could be a place where client teams can review EIPs, leave opinions, and feedback. We already have Ethmagicians, but we could create a dashboard which is more structured than a forum thread. This would display which EIPs are provisionally scheduled for each fork and could be annotated by client teams with their opinions and implementation status.

Additionally, there should be greater expectations for ACD agenda items to be reviewed before the call where possible (teams could assign members to review different items), to avoid situations where no one has had a chance to review.


*(13 more replies not shown)*

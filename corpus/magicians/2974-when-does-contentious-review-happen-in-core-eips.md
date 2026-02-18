---
source: magicians
topic_id: 2974
title: When does contentious review happen in Core EIPs?
author: boris
date: "2019-03-24"
category: Magicians > Process Improvement
tags: [governance]
url: https://ethereum-magicians.org/t/when-does-contentious-review-happen-in-core-eips/2974
views: 2981
likes: 37
posts_count: 25
---

# When does contentious review happen in Core EIPs?

Currently, the Core EIP and CoreDev process is meant to be a technical review process. Are the changes proposed technically sound, and will they improve the functioning of the network and/or improve the health of the network?

From recent discussion, it’s clear that technical acceptance is not sufficient to include a Core EIP. Not only that, but many stakeholders would like to comment on Core EIPs as they affect non-technical functioning of the network.

Technical acceptance is defined as:

- there are no “over my dead body” objections by Core Devs in the discussion
- typically GitHub Issue or EthMagicians thread as the discussion location
- and, an EIP has been added to the agenda of a Core Devs call (Ethereum/PM GitHub issue)
- and there haven’t been any remaining technical issues raised
- and there is a commitment to write/merge code in clients

For now, the Istanbul Roadmap Page on the Ethereum wiki has a list of proposed EIPs for the Istanbul hard fork https://en.ethereum.wiki/roadmap/istanbul — this link is included as an example of upcoming EIPs.

---

How should the Ethereum community and/or stakeholder groups approve or deny a Core EIP for inclusion into a hardfork on grounds aside from technical issues?

Whose responsibility is it to announce or communicate that a Core EIP is proposed?

What are the other important questions we should be asking?

Who is willing to put time into figuring this out?

## Replies

**fubuloubu** (2019-03-24):

In response to the specific question, I think “contentious review” happens sort of incidentally currently.

First of all, the Core Devs call is open to anyone to sign up and join the discussion to talk about an issue. It’s sort of the “public hearing” of Ethereum’s governance. If we get any active dissent in the call from someone who does not typically join, this is where we hear it out.

On the other hand, most people are quite busy and cannot attend these calls. The Core Devs (and this doesn’t really reflect any particular person’s job at the moment) summarizes the discussion in the forum threads and take it under consideration. If the dissent makes sense to them, they might discuss it during the call. Their own dissent may fall under this category too. It’s a very fuzzy process, but they try to account for things that affect implementation of the proposal, including non-technical things like “community sentiment”. If there are no known dissent that the participants, especially the client developers, deem to be a blocker to the implementation, a decision to move forward is made.

---

I think documenting how this system works by analyzing old calls and proposals would help document the process. We could draw clear parallels between this political process and other political processes across the world and look for opportunities for improvement and avoidance of capture.

For one, I think formalizing the Core Devs call as a sort of “public hearing” may help formalize things a bit. There are many parallels to a public hearing. There is a chairman of the discussion ([@souptacular](/u/souptacular)), there are the “lawmakers” (aka client devs and other interested parties), there are people who sign up to deliver public remarks. It gets recorded and documented for others to reference. I think there is a clear parallel.

Typically, in public hearings nothing gets “Decided”, it’s just everyone’s voice is heard. Perhaps what could be done is we could optimize for that, and then more contentious discussion of whether or not to implement to a different chat that gets deliberated with something like Chatham House rules so Core Devs feel more free to voice their concerns and the concerns of others without feeling targeted. This might improve things.

---

However, it is usually lawmakers that participate in these public hearings as the central figures. They are elected officials, whose time to hear out the discussion is paid for by the people they represent. We have a different system. The Core Devs call is made up of people from EF who have various capacities they speak to, client developers whose time is paid for by their respective employers and who obviously implement the discussion, and whomever signs up to discuss an issue. We’re not necessarily getting a representative sample of key stakeholder concerns, and we’re not getting detailed analysis from parties who may raise more legitimate issues with a proposal (such as security professionals and “crypto-economists” if I might use that term loosely). This is because people are too busy to attend the often 2hr+ call, and it would be volunteering so no one wants to do that either.

The wider governance is such that this harm is mitigated a little bit, although definitely not in an optimal way. In the end, full node operators specify what the network is by “voting” with their node whether or not to operate a particular software upgrade. Some nodes have more of a say than others. Mining pool operators, exchanges, and infrastructure operators all have a real legitimate say on the final state of the network, but at the expense of causing a contentious fork (which everyone wants to avoid). Adding a signaling mechanic for full nodes (e.g. an `eth_vote(EIP) -> bool` API endpoint) and random-sample querying nodes over a relevant period of time (1 month might be enough to make “voting” by sybil nodes overly costly) might be enough to gauge sentiment of what is the final layer of Ethereum’s governance.

Node “reputation” could be leveraged as well in help to filter these results. We might know which of these nodes are operated by those key parties mentioned above. We can use uptime and endpoint access metrics to determine the “sybil-ness” of nodes who choose to remain anonymous. Everyone in the community could vote in this way, and we help the ensure the security of the network as well in the process. This is just one concept, but every single proposal for how to deal with Ethereum’s governance requires a method of voting by “key stakeholders”, so we’ll have to do something like this eventually.

---

Who is willing to put time into figuring this out?

That is the toughest question. We are all busy and so far these type of analytics has been an unpaid and thankless job. Those with an interest in making core governance stronger should fund efforts to make it so, but these kind of wishy-washy statements from onlookers like myself are why nothing every happens.

I don’t know how to solve that.

---

**boris** (2019-03-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> I think formalizing the Core Devs call as a sort of “public hearing” may help formalize things a bit.

Unfortunately, this is contrary to what core devs want out of a call (and I agree with them) — coordinating & discussing on technical issues.

So the question becomes, what other process can gain legitimacy for giving non-technical / political input on changes?

---

**fubuloubu** (2019-03-24):

Fair! Perhaps the proposal is then to create that “public hearing” to reduce the amount of noise Core Devs get, and make participating in that a pre-req for EIP discussion in the call?

---

**boris** (2019-03-24):

An “explain your new core EIP proposal in ELI5 style” regular call would be interesting.

But I would hate technical ideas to be shut out because you have to run a political gauntlet first. Although that seems to be what many people want ![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=9)

---

**fubuloubu** (2019-03-24):

I see it more as a signaling process. “This is the time we’ve set aside to discuss all the possible issues with the proposal”. The point is to gather the feedback to consider it all together, and not to fan the flames of argument. Everyone gets a chance to say their piece, the time to respond to each criticism is after that call.

We sort of have this now in the EIP GitHub and “discussions to” FEM, but that is more written testimony whereas this would be really public. I think it should be the author’s responsibility to respond to all criticisms before it is allowed to move forward to Core Devs

---

**jpitts** (2019-03-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> An “explain your new core EIP proposal in ELI5 style” regular call would be interesting.

Relates to an idea proposed by [@econoar](/u/econoar) on Twitter. See that thread…

https://twitter.com/econoar/status/1109996623243837440

---

**gcolvin** (2019-03-25):

A simple suggestion I’ve made on [ethereum/governance](https://gitter.im/ethereum/governance?at=5c984e5cd0133e21e50e31de) is just to add a post-meeting statement of what consensus was reached on the issues discussed to https://github.com/ethereum/pm.  That might have helped prevent a lot of confusion in the progPoW case, where [@souptacular](/u/souptacular)’s statement of the consensus was buried in the middle of a badly transcribed discussion.

---

**gcolvin** (2019-03-25):

As to the question at hand.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Currently, the Core EIP and CoreDev process is meant to be a technical review process. Are the changes proposed technically sound, and will they improve the functioning of the network and/or improve the health of the network?

The Ethereum Core Developers develop and manage a technical platform and service.  Like all service providers we must remain reasonably neutral among the users of our service, and thus relatively narrow in the considerations that are relevant to our deliberations.  Where an issue cannot be presented in technical terms, even as broadly stated as “the health of the network,”  I think the Core Devs are simply not equipped to make a decision.

The review that matters to the Core Devs is finalized as a consensus in the AllCoreDevs call.  Reaching consensus on contentious issues is difficult enough.  Contention that occurs after consensus in is reached is nearly impossible to deal with.  So it seems essential to reduce contention by participate in the process before proposals get to the core devs, including the discussion and Last Call process.

One way to participate–and perhaps the best way to present issues to the Core Devs in a form we can take action on–is to prepare an Ethereum Improvement Proposal.  That forces the proposer to present arguments in more technical terms, even as broadly stated as “the health of the network.”

---

**MicahZoltu** (2019-03-25):

I don’t believe most people have strong complaint with the current process when it comes to purely technical issues.  The problems are related to non-technical disagreements.  Block reward reduction, recovery proposals, proof of work algorithms, etc. all were not technical challenges (or if they were those were handled by the proponents), but it is ultimately on the Core Developers to decide what they code and what they don’t.

Unfortunately, it isn’t as simple as “bring a quality EIP to the Core Dev meeting and if no one has technical objections then the Core Devs implement it”.

---

**gcolvin** (2019-03-25):

Yes, the more “purely” technical the issue it the easier it is for everybody.  I’m just suggesting that more participation before difficult decisions would be more helpful than complaining after difficult decisions, and that filing an EIP is one of the most powerful forms of participation.

---

**MicahZoltu** (2019-03-25):

Take the ERP EIP.  People spent a lot of time and energy crafting that EIP and ensuring it was technically sound.  Then when it got pushed up to the core devs, no clear decision was made and no clear process was followed for making a decision on it.

This is what EIP authors have to look forward to right now, a lot of hard work followed by an undefined process for decision making and no clear decision as the outcome.  This is certainly not incentive compatible with encouraging people to write good EIPs, it instead incentivizes people to first try to radicalize the community or have backdoor conversations with core devs to get a feel for how the undefined process will go prior to putting in the effort.

With a well defined process for deciding what goes into clients, EIP authors have a chance at being able to predict the outcome *before* they sink a ton of time into the project.  If their prediction is that it will go through, then they can dedicate the effort to do all of the work.

---

**gcolvin** (2019-03-25):

I agree that the process needs to keep improving, and am open to suggestions on how to improve it. I don’t see how any process for evaluating proposals could give you certainty up front, but we can clearly do a better job of managing the process.

Right now I’m just trying to get clear on what the current process is, such as it is, and suggest how best to work with it.

---

**lrettig** (2019-03-26):

I propose two ideas:

1. We all need to accept and resign ourselves to the fact that, for now, Ethereum is and, for the foreseeable future, will remain a technocracy. One reason is that, while not all decisions are purely technical, nearly all important decisions have at least a substantial technical component. Another is that, while most of us, myself included, would prefer something more closely resembling a democracy, that is simply not possible unless and until we have a more formalized conception of identity, which we’re nowhere near close to.
2. The core devs should establish a steering committee. This would be off-chain but a little more formalized than core devs and would have a mandate of deciding on these more contentious questions. I envision seven or nine people who are trusted, who have a strong technical understanding of the protocol, representing most or all of the largest groups of stakeholders, and including experts in relevant areas such as economics, philosophy, governance/political philosophy, ethics, law, etc. (or with the resources and mandate to call in experts as necessary). Yes, it may be hard to assemble such a group but I believe it’s possible. They should rotate often, every year or so. And it should be an “opt in” process whereby the core devs refer individual issues that they don’t want to decide on.

There are 1000 ways you could poke holes in these ideas and I encourage you to do so, but please be constructive and offer alternative ideas. No, this won’t please everyone but I believe it’s a workable proposal.

---

**MicahZoltu** (2019-03-26):

[@lrettig](/u/lrettig) I think it is valuable to acknowledge reality, and I agree that technocracy is how things currently function (sort of, see below).

However, the Core Developers have asserted that they do not want to make hard decisions, so what we currently have is a technocracy where the leaders don’t want to lead, which is actually worse than having a technocracy because it means no one is steering the boat.

I think that either the core developers need to accept the power they have, or we need to find someone to fill that void.  Whether that is Cat Herders, or Magicians, or [@AlexeyAkhunov](/u/alexeyakhunov) or someone else or some other group I think matters less than it matters having that void filled by *someone*.

---

**boris** (2019-03-26):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> However, the Core Developers have asserted that they do not want to make hard decisions, so what we currently have is a technocracy where the leaders don’t want to lead, which is actually worse than having a technocracy because it means no one is steering the boat.

At least, they don’t want to make decisions that are anything other than technical. And at this point, are probably a bit skittish about technical decisions that may be *perceived* to have non technical elements.

---

**gcolvin** (2019-03-26):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I think that either the core developers need to accept the power they have, or we need to find someone to fill that void.

Nothing goes into the client software that the core developers don’t put there, and nobody can make them put it there.  That is the power the core devs have.  What is the void you want to fill, and how would it change that situation?

---

**MicahZoltu** (2019-03-26):

The core developers have expressed that they do not want to make any contentious decision.  As you say, they ultimately write the code, so what ends up happening is when they are presented with a decision that they feel is “contentious”, there is an incredible amount of weight in favor of the “do nothing” option.

I dislike decisions being made by way of the person/group who is in the position to make the decision simply ignoring the issue because they don’t want to offend someone, rather than because they believe that not acting is the right thing to do.

It is akin to having a leader who is in a coma.  Sure, they are making decisions in the sense that they are “deciding to not change anything”, but that isn’t a *good* leader.

What I would like to see is a person or group who is willing to make decisions even when they are contentious.  Someone or some group who will stand up and say, “we have heard the arguments from all sides and we are going to do (or not do) X”.  This person or group needs to be respected enough by the core developers such that when a decision is made, the core developers will strongly prefer following it over “do nothing” (of course, they still retain veto power).

---

**AlexeyAkhunov** (2019-03-26):

My personal problem with being a decision maker in a contentious process is that I am a software developer, not a politician. And the difference is that politicians enjoy many more legal privileges that protect them, for example: https://en.wikipedia.org/wiki/Parliamentary_immunity

And this is exactly why certain pressure strategies can be used to easily remove dissenting voices from such public, yet legally unprotected decision bodies

EDIT:

To add to that, the only way to make an efficient governance system that can cope with contentious decisions, but operates in an extralegal space, is to use so-called the “veil of decentralisation”. And that means always put contentious decisions to the hands of the users of the networks, or the operators, who are not easy to identify and pressure

---

**gcolvin** (2019-03-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> …
> the “veil of decentralisation”
> …
> put contentious decisions to the hands of the users of the networks, or the operators, who are not easy to identify and pressure

Which is not at all an easy thing to do, and is itself contentious.

What I keep calling for is more self-organization of communities of users and operators, and more discussion within and across communities.  I think the Magicians have shown how that can work. That could reduce the amount of contention in the first place, and focus remaining contention into arguments that the Core Devs can actually deliberate.

But in the end the Core Devs have to decide what software goes into the next fork, and the community takes a huge risk not to follow.  I don’t know that we can avoid that responsibility.

---

**lrettig** (2019-03-27):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I think that either the core developers need to accept the power they have, or we need to find someone to fill that void. Whether that is Cat Herders, or Magicians, or @AlexeyAkhunov or someone else or some other group I think matters less than it matters having that void filled by someone .

I agree pretty strongly with this. We need workable governance. I made a proposal for one way to do that here:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png)
    [When does contentious review happen in Core EIPs?](https://ethereum-magicians.org/t/when-does-contentious-review-happen-in-core-eips/2974/14) [Process Improvement](/c/magicians/process-improvement/6)



> I propose two ideas:
>
> We all need to accept and resign ourselves to the fact that, for now, Ethereum is and, for the foreseeable future, will remain a technocracy. One reason is that, while not all decisions are purely technical, nearly all important decisions have at least a substantial technical component. Another is that, while most of us, myself included, would prefer something more closely resembling a democracy, that is simply not possible unless and until we have a more formalized concep…

[@AlexeyAkhunov](/u/alexeyakhunov) raises a very valid point that anyone in the decision maker’s seat is potentially opening themselves up to legal liability. So I think we also need to work closely with legal counsel to make sure we have institutional structures in place to protect the decision makers.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> the only way to make an efficient governance system that can cope with contentious decisions, but operates in an extralegal space, is to use so-called the “veil of decentralisation”

I’m not sure I agree with this, and in any case, we should get some legal opinions here. In my opinion it’s less about decentralization (which was more of an issue with the SEC weighing on whether ETH was a security) and more about making sure we have the right legal structures and protections.

We have at least two resources we can turn to in order to figure this out. One is EF, the other is [COALA](https://coala.global/). I’ll begin a dialog on this question with both. Frankly I’m not sure the Magicians is the right forum to discuss legal questions. But I want to include others in the conversation, so we should figure out which forum is the right one.


*(4 more replies not shown)*

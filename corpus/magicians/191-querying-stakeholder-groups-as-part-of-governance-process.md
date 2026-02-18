---
source: magicians
topic_id: 191
title: Querying stakeholder groups as part of governance process
author: cslarson
date: "2018-04-19"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/querying-stakeholder-groups-as-part-of-governance-process/191
views: 2147
likes: 25
posts_count: 20
---

# Querying stakeholder groups as part of governance process

Alex Van de Sande makes a [compelling case](https://medium.com/@avsa/avoid-evil-twins-every-ethereum-app-pays-the-price-of-a-chain-split-e04c2a560ba8) against chain splits, specifically in the case of a *platform* like Ethereum because of the downsides for applications it hosts. The conclusion I made from this was that it’s critical for Ethereum’s success to have a governance process that’s seen as politically legitimate and can make recommendations well before the need to rely on a fork to make the decision for us. It’s impossible to make *everyone* happy, but what would be great to see is something that we can point to when some issue is dragged up and can say (with support from most people) “look, people had their say on this”. To me, political legitimacy boils down to identifying key stakeholder groups and querying them individually on matters. The groups as I can see them, and suggestions for how they might weight their votes, might be:

- ETH holders (coin vote)
- Projects (weighted by token market share?)
- Core developers/devs (weighted by commits? or just 1:1 i’m sure they can work something out)
- Users, community members (weighted 1:1 using a system with some anti-sybil property like r/recdao?)
- Miners/validators
- EEA members

We don’t need to have a formal, on-chain process, but improving an informal one could be a boost for the community. It would be great to be able to make decisions in a more expeditious and resolute way.

## Replies

**MicahZoltu** (2018-04-19):

TL;DR: You can’t stop forks.  If there is a disenfranchised group out there, they *will* fork (see ETC).  Voting doesn’t change that.

I disagree with [@alexvandesande](/u/alexvandesande) on this topic because I think the *only* thing that makes crypto-currency governance better than traditional governance systems (e.g., democracy, monarchy, dictatorships, etc.) is the fact that groups of people *can* split off into separate groups if their belief systems diverge enough.  Democracy, monarchy, and even dictatorships would not be that bad if it was reasonably easy for disenfranchised citizens to “fork” (secede).  As has recently been seen in Catalonia, and historically all over the world, splitting off when a subgroup becomes disenfranchised is extremely difficult, expensive, and bloody.

IMO, this is exactly why the governance system of Ethereum ultimately boils down to “users decide what client they want to run”.  This is similar to groups of citizens (e.g., cities) being able to decide “which government do I want ruling me” and “a new one that we made up” is a reasonable choice.

Alex is correct that there are network effect costs to splitting like this, but that is OK.  Having one network to rule them all is a *bad* thing it turns out.  It is why most Americans feel disenfranchised, because there is one government trying to pander to vastly different groups of people.  Sure, something like Maker or Augur will need to either pick a chain or run their platform on multiple chains (splitting their user base) or spend significant engineering figuring out how to merge the chains, but that is well worth it IMO if it means that disenfranchised users feel empowered to split off.

One can, of course, argue that doing things like voting *prior* to implementing something that is likely to cause a split could result in the split not happening at all because the client development teams would (presumably) not write the code in the first place, but that just means you are disenfranchising a different set of people.  So you haven’t really “solved forking”, you have just made it so the set of people most capable of winning votes are the set of people who aren’t disenfranchised and the set of people who aren’t becoming disenfranchised.

Ultimately, what we must remember is that the client development teams are not beholden to anyone other then their own corporate structures and they can author whatever code they want, regardless of any sort of voting system.  If you try to tell them, “You aren’t allowed to write this code” they will just do it anyway and your governance system will be shown to be pointless in the end.

---

**cslarson** (2018-04-19):

(mostly in response to your last two paragraphs which I think hold the crux of any difference between our opinions)

What are we doing here then if not to formulate some system for making a recommendation on what options to make available in the client software that is developed, particularly by the EF? I don’t see any reason why all options be made available by client developers (where is my [EIP 858](https://github.com/ethereum/EIPs/issues/861) supporting client, if so). It seems reasonable to me that if some *prior* vote (by key stakeholder groups or whatever else is chosen as politically legitimate) is made and a recommendation made to the primary client developers (particularly the EF) then going along with that in any way disenfranchises those who didn’t have things go their way. As you say, this isn’t a geographic region. They are free to make their own modifications and pursue a fork. It’s almost that the very nature of open source software and fork-able networks make disenfranchisement a non-issue.

---

**fubuloubu** (2018-04-19):

I’m beginning to get the feeling that a subset of people are of the opinion that Ethereum should not have a formal governance process, because any formal governance process around changes can get gamed. I think that is a legitimate argument actually, but as more people get involved and things get louder, ad-hoc discussion and decision making power becomes increasingly noisy and untenable. I think recognizing this is the best takeaway from 867 and 999, and I think [@cslarson](/u/cslarson) is summing it up well here, how do we ensure the broadest possible set of voices are heard in the decision making process where decisions can still be made effectively.

---

**MicahZoltu** (2018-04-19):

Engineering is a time consuming process, so at the end of the day, *someone* has to decide what to engineer and what not to engineer.  The client developers are the ones making this decision because they are the ones who are putting in the time/resources (they aren’t being paid by ETH holders, they are self funded in various ways).  The EIP process is an *input* into the client developer engineering process that attempts to allow people who aren’t client engineers to contribute ideas to what *could* be engineered.  The All Core Dev meeting exists not because it needs to, but because the various client developers would *rather* be inter-operable so they meet to try to agree among each other what will go into each client.

---

I think ultimately, the problem I have with voting is that I have witnessed what happens to voting based governance systems.  They ultimately end up being compromised by those who are good at pandering and marketing or they end up being driven by people who don’t fully understand the issues being voted on.  With the “client developers” make decisions but can be ignored by users, it allows people who are spending a *lot* of time thinking about these problems (40-100 hours a week) to make decisions while keeping them in check by making it easy for the community to simply ignore the proposed changes (which results in the client developers having wasted a lot of time).

---

**MicahZoltu** (2018-04-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> I’m beginning to get the feeling that a subset of people are of the opinion that Ethereum should not have a formal governance process

To be clear, I do think there should be a formal governance process, I just think it should be that client developers build whatever they want and then users can choose to run that software or not.  ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**fubuloubu** (2018-04-19):

And that is effective, something that I agree with as being the 90% solution and the most effective and natural process for managing opinion in a constructive way that cannot be easily lobbied.

But it still relies on really technical people having input into the process at the end of the day. If we want to build a platform for the masses, how do we query everyone’s opinion in the broadest possible way where we can make constructive decisions as a community, and distill those opinions into actionable intelligence for those client devs who chose to listen? How do all the different voices, with VERY different goals, come together on a minimal compromise where the network still holds?

I think we need to acknowledge that we’re having growing pains right now, and ignoring or resisting change instead of accepting it and working with it is how we fail as a community to grow. This is especially important going into Edcon where we will be discussing this more generally i.e. cresting an EIP0 “Constitution of Ethereum” as someone described it.

---

**cslarson** (2018-04-19):

> which results in the client developers having wasted a lot of time

Isn’t this ultimately what we’re trying to reduce? What I’m suggesting isn’t a formal governance - it’s an informal structure for making those *recommendations*, not decisions, because as you say what’s coded up is the decision of the developers.

---

**MicahZoltu** (2018-04-19):

![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=9) more on what exactly it is I disagree with, I think my issue is that I haven’t heard any proposals as to how to get *useful* information out of a large group of humans.  As I mentioned above, any voting system can be compromised (pandering, marketing, etc.), and individual humans often do not make decisions that are in their own best long term interest (just look at how many people save for the future vs gamble), none the less the best interest of the community.

Personally, I would rather pick a leader (in this case, Parity, Geth or Harmony) and then *trust* that they will behave reasonably and if they behave *too* unreasonably (in my eyes) I fork/follow a new leader.  Since I value network effect, I won’t take the decision of forking lightly, and I can mostly check-out of the decision making process and trust that the leader I chose will probably make more good decisions than bad decisions.

---

**fubuloubu** (2018-04-19):

I agree. What are the holes in that process? This is what I want to discuss and brainstorm about.

---

**fubuloubu** (2018-04-19):

I think there’s already voting going on too with the clients. geth is #1, so we consider them the network leader. People can make votes through running parity to make them number one if they think they make better decisions.

Whomever has majority client share creates the primary signal in a hard fork event. We basically have created a form of liquid democracy here lol.

---

**alexvandesande** (2018-04-19):

@MicahZoltu23m

> Democracy, monarchy, and even dictatorships would not be that bad if it was reasonably easy for disenfranchised citizens to “fork” (secede).

I actually agree with that point. I *like* that disenfranchised users *can* fork, it gives them power. I do not advocate taking away the forking power from users (that’s impossible) but trying our best to negotiate with disenfranchised users to avoid that happening, because a united community is a stronger one. That’s why I am against the EIP999: doesn’t matter where you stand on it, you have to admit there’s enough dissent to guarantee there will be a fork if it comes to it. And balancing the issues with a split community versus the gains of having web3 foundation and a few other teams recover their ether, I don’t think it’s worth it.

I *agree* that governance is required and could be used for this. I would like to bring [EIP960](https://github.com/ethereum/EIPs/issues/960) in this: the ether cap is something we are discussing. My opinion is that I believe that I believe we might definitely be overpaying for security and, specially when we switch to proof of stake. So here’s my suggestion on how to attempt solve governance, 960 and 999 at the same time:

- When we switch to PoS, we should instead of cutting down the extra issuance, instead give it (maybe less than current) to a contract that will fund public goods.
- The governance of that contract is open to debate, maybe it can be a complex multiple stakeholder vote, or could be some sort of futarchy or another crazy idea.
- The contract would once per year decide on how it could distribute funds the next year, towards all sorts of public goods including:

Fund open source development
- Fund insurance pools
- Redress and reimburse victims of hacks, bugs and other kinds of loss (this could include things like the Parity Multisig case - and could even apply retroactively to the web3 foundation)
- Burn ether to reduce the cap, if the governance decides it’s the best usage

Of course the really tricky part is of course, how that governance would happen. But I think this would allow to keep many parties happy: it creates a structured format to redress grievances and take actions for damaged parties that doesn’t have a fork, limits the power of governance (it cannot freeze or interfere in other contracts, can only distribute X amounts of ether per year), etc.

My suggestion for a governance model would be to be a simple multisig, but instead of having private keys on the multisig, each “chair” would be a different contract, that would represent stakeholders (so validators could vote on with their stake power, maybe users would have a different sort of contract, etc)

---

**cslarson** (2018-04-19):

This is a valuable proposal and I would be interested to see what kind of support it might garner.

---

**MicahZoltu** (2018-04-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexvandesande/48/101_2.png) alexvandesande:

> you have to admit there’s enough dissent to guarantee there will be a fork if it comes to it

I don’t believe we have sufficient information to assert this with confidence.  Even if we did a coinvote, I’m not confident that we would have enough information to assert this.  During the ETH/ETC split, I was strongly in favor of not recovering the funds (ETC), however in the end I went with ETH because I didn’t care *enough* to lose the network effect benefits of ETH.  In any vote I would have voted ETC, yet when it came time to choose between breaking away from existing leadership and finding new leadership, I chose to follow the existing leadership.  Note: During the ETH/ETC debate I was reasonably vocal about my position as well.

Now, a couple years later and after having quit my job and worked in this ecosystem for a year, I am better able to appreciate the decision that was made by the leadership.  I still am not 100% in favor of the decision, but I’m glad I chose to follow-the-leadership (whom I generally trust to *try* to do the right thing at this point) rather than break off and try to form my own community or help build a new community.

The point I’m getting at here is that we cannot assume that just because someone shouts and yells or even votes for a particular outcome that they are willing to sacrifice the benefits of network effects for their belief system.  We also can’t assume that everyone is fully informed as to the nuance of the various arguments being made for or against the things being voted on, just as I wasn’t during the ETH/ETC split (I was working a full time job at the time, Ethereum was only my hobby back then).

As to the question whether or not there will be a fork or not if this happens, I don’t know.  However, if there is it is because there are enough people who really do care about the topic on both sides to be willing to split over the decision.  That alone IMO means that splitting is the right thing to do.

---

![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12) It would be interesting to run a blockchain where the client(s) were incredibly modular and the client development team was structured such that anyone could fund the development of any feature and the system *always* forked and users had to *actively* choose which chain to use.  Then if any feature had a non-trivial number of people that cared more about the feature than the network effects, there would be a lasting fork, and if not then one side would lose and the other would win.

---

**MicahZoltu** (2018-04-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> I agree. What are the holes in that process? This is what I want to discuss and brainstorm about.

Sorry, can you be a bit more specific as to what “that process” is you are referring to here?  Are you referring to the current governance process, or the voting process, or something else?

---

**fubuloubu** (2018-04-19):

I remember someone had a layout of the clients and how they worked and how hard forks worked, etc. Basically showing the system of checks and balances in the econsystem and how they play together. I think it was very high level though, a great start.

We need to explore this structure and be strongly aware of all the checks and balances in play, and they ask how different classes of users fit in and be able to build a more detailed model of the process. Then we throw darts at it, try to identify weaknesses and holes, things that can be exploited, and ensure we minimize or eliminate those problems, or at least have a good understanding of what it looks like when an exploit is being tried.

Something of that nature.

---

**MicahZoltu** (2018-04-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> I remember someone had a layout of the clients and how they worked and how hard forks worked

Probably Vlad, he has a presentation on blockchain governance that includes some slides that match what you are describing.  The presentation can be seen here I believe: https://youtu.be/w8DjFbCTjus

---

**fubuloubu** (2018-04-20):

I didn’t see the diagram in there, but yes a version of that presentation is what I’m talking about.

More abstractly understanding that process, determining whether it is fully optimal, and how change gets into the system and through the system is what I’m advocating for. What guiding principles allow us to maintain a strong viewpoint of what that structure must provide, but also allows it flexibility to respond to threats and changes in the platform’s purpose. I think we understand the ecosystem pretty well and why it works and the economic incentivization of all actors.

I keep coming back to what is missing where we can’t completely resolve an issue with a friendly but determined actor, and how that process would respond to an actively malicious and determined actor seeking to influence the platform for their own gains.

---

**cslarson** (2018-04-20):

> I keep coming back to what is missing where we can’t completely resolve an issue with a friendly but determined actor, and how that process would respond to an actively malicious and determined actor seeking to influence the platform for their own gains.

While we are looking for an ultimate long term solution we may miss out on an incremental and crucially needed interim solution.

---

**fubuloubu** (2018-04-20):

Well, the current solution is to say “no” and hope it goes away lol.


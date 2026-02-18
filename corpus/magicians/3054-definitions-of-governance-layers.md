---
source: magicians
topic_id: 3054
title: Definitions of Governance Layers
author: boris
date: "2019-04-01"
category: Magicians > Process Improvement
tags: [governance]
url: https://ethereum-magicians.org/t/definitions-of-governance-layers/3054
views: 3030
likes: 24
posts_count: 17
---

# Definitions of Governance Layers

I’ve attempted to define the layers of governance we’re dealing with in the Ethereum ecosystem.

1. Open Source Collaboration - standard open source norms, applied to Ethereum client software and other infrastructure and components
2. Protocol Standardization - the EIPs process; targeted at Ethereum main-net, but re-used and adopted by other networks and systems
3. Core Devs Coordination - client developer calls and other interactions
4. Network Governance - technical and non-technical discussions on what Core changes we want to adopt and support (this is the layer that has no defined processes)
5. Nodes Choose Software to Run - the core governance of decentralized blockchains

I offer this as a way to educate and explain, and to use this as a base set of definitions that we can use for further discussions.

## Replies

**boris** (2019-04-01):

I’ve written a blog post that goes into each of these layers at length: https://blog.bmannconsulting.com/ethereum-governance/

Andrew’s tweetstorm is also required reading. I’ve embedded in my blog, but here is a direct link to the start:

https://twitter.com/cyber_hokie/status/1112305608047427584

---

**timbeiko** (2019-04-01):

Thanks for kickstarting this! Here are a few comments I had on the blog post.

# Ethereum Governance

> It [the EF] manages a number of pieces of community infrastructure and employs / contracts several teams working on major software for Ethereum, from testing frameworks to the Geth client.

I think it would be worth including research in this.

> Ethereum is a set of protocols, from the Ethereum Virtual Machine (EVM) that underlies the smart contract system and many core features, to the devp2p peer communications protocol, to the JSON-RPC middleware for getting data in and out of nodes.

It may be worth highlighting that *some* of these are specified in the Yellow Paper, but that others aren’t. One of my biggest realizations when starting to work on a client was the amount of things that are *not* part of the YP.

# Open Source Collaboration

> although money of them are paid by the EF as employees or contractors

Typo ![:face_with_tongue:](https://ethereum-magicians.org/images/emoji/twitter/face_with_tongue.png?v=15) `money` → `many`

> many of the core norms of open source are no longer being taught, even to developers. I think we can do more here, and would love to work on onboarding more new developers to become valuable developers to the core Ethereum stack, as well as the emerging ETH2 stack to build our next generation of experts.

Agreed. We spend a lot of time thinking of the pool of developers currently building on Ethereum or other blockchains, but the reality is that the set of developers who haven’t contributed to this space is orders of magnitude larger and we don’t do much, as a community, to pull them in.

# Protocol Standards

> I think the EIPs process works quite well, and is only improving. More education, especially for technically proficient developers who can add value to the network, would still be better.

Do you have any idea what this could look like?

> There is a movement that is just beginning to have dedicated maintainers and repositories for different parts of the Ethereum stack – the EVM, devp2p, the JSON-RPC interface, and so on. This means that even more collaborators can work together, even beyond the boundaries of Ethereum main-net, to improve and be interoperable.

I think splitting up various parts of Ethereum into smaller groups, like mentioned here, is probably the way to go if we want to keep iterating rapidly, reaching rough consensus, and not have Core Devs be a bottleneck. Aside from purely technical issues, you can imagine dealing with mining/staking rewards, UX, etc.

# Core Devs Coordination

> Having spoken with individual client teams, the feedback is that code implementation really doesn’t take a lot of time: forward progress is being limited by non-technical decisions making and roadmap arguments  today .

Well said!

> Dan Finlay’s process flow diagram

It seems like there is a connection missing between the “Users, dapps, any address […] or dependencies” and “Clients implement hard fork patch” which explains a lot of the issues that have currently surfaced. For example, Geth & Parity have already implemented ProgPow (although perhaps not the latest spec). This does not imply it will be bundled into a release and made available to the public, namely because of the signalling that is happening by users and dapps at the moment.

# Network Governance

> One point of view is that “stakeholders should self organize”.

One risk is that we keep fragmenting the conversation to a degree where it is impossible for people to have a global picture of what “the community” is. Perhaps this is inevitable past a certain size, but we should push people towards existing tools vs. novelty.

> I don’t think placing network governance “before” protocol standards or Core Devs makes sense.

+1. I think what we are mostly missing is a step from Core Devs saying “this is technically sound” to them saying “so let’s implement it in the next hard fork”. There should be some other group(s) in between those steps that try and answer the “is this what the majority of the community wants?” question, especially in the case of less-technical issues. Perhaps the best way to do this is to create a new category or sub-category along with Core. You could imagine Core-networking, Core-economics, Core-mining, etc. with different stakeholders representing each sub-category.

---

**boris** (2019-04-01):

Appreciate your close read and comments! Updated the post.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> I think it would be worth including research in this.

Yes, I added this, thank you Tim. I footnoted this already, but primary point of this post / framework is not what EF is responsible for / does, or what the community thinks it should do. That would be a very valuable exercise that to date, EF members & leaders have not wanted to have an open discussion about. I also don’t mention EF grants for the same reason.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> One of my biggest realizations when starting to work on a client was the amount of things that are not part of the YP.

Right??? I think we’re heading in a better direction, and with entities like the EEA and potentially other points of collaboration at the Protocol Standards level this can only get better.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Do you have any idea what this could look like?

You and others learning the process. Me giving presentations at various in person events. Basically – whenever you see someone with good technical skills saying “I wish it worked this way” or “what if Ethereum had this feature?” – recruit them to try and write an EIP.

Hmmm. Maybe should run a “Writing your first EIP” session at some upcoming large conference. I’ve also given this to the EEA and I hope they will have some EIPs soon.

---

**fubuloubu** (2019-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> I think splitting up various parts of Ethereum into smaller groups, like mentioned here, is probably the way to go if we want to keep iterating rapidly, reaching rough consensus, and not have Core Devs be a bottleneck.

Yasssss. There is still a higher amount of coordination required here as teams would need to cross-collaborate, but I feel like the teams being largely “permission-less” that there are enough “well-connected nodes” (read: people with multiple interests) where communication is fairly efficient. Think of it as a human-based gossip protocol lol.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> One risk is that we keep fragmenting the conversation to a degree where it is impossible for people to have a global picture of what “the community” is. Perhaps this is inevitable past a certain size, but we should push people towards existing tools vs. novelty.

I really think this is the core of our problems. The dispersion of communication among many parties is creating longer and longer feedback loops leading to poorer communication. It’s like a bad game of telephone. Couple that with the fact that the majority of the community prefers social media channels with poor scaling properties for a large community, and you get what you get today: a lot of people talking past each other, instead of calm well-reasoned debate. Forums (like this one) are simple better, and can be tailor fit to our needs as a community.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> I think what we are mostly missing is a step from Core Devs saying “this is technically sound” to them saying “so let’s implement it in the next hard fork”.

I think this is the right take. It could maybe be in parallel. I think seeking technical consensus first is important, but that can be done offline of the All Core Devs call, which is really intended only to come to consensus on the proposals that are included in forks by all clients, or tracking their progress. I think in a properly oiled machine it should be more obvious that proposals have gone through their respective stakeholder processes (technical, economic, political, social, etc.) and are ready for the final work of implementation, which should not be a controversial decision. ACD should largely be seen just as “implementing the will of the community”.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Perhaps the best way to do this is to create a new category or sub-category along with Core.

Still no motion on this: [Add Audience Review process to EIPs prior to Last Call by fubuloubu · Pull Request #1725 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/1725)

---

**fubuloubu** (2019-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> “Writing your first EIP” session at some upcoming large conference. I’ve also given this to the EEA and I hope they will have some EIPs soon.

So, I have a confession to make… I have never gone through the process with my own EIP!

I *really* want this proposal to make it into Istanbul:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png)
    [EIP-1344: Add chain id opcode](https://ethereum-magicians.org/t/eip-1344-add-chain-id-opcode/1131/) [EIPs](/c/eips/5)



> https://github.com/ethereum/EIPs/pull/1344 proposes to add an opcode to retrieve the chain id of the chain that the block has been mined on.
> This would allow smart contract to validate signatures that use replay protection (as proposed in EIP-155).
> Currently the only way is to hardcode the chain id into the smart contract. This poses a problem in case of a hardfork.
> This opcode would allow multi signature contracts that use signatures to implement better replay protection and increase securit…

It’s fairly uncontroversial in my mind and also relatively simple with clear benefits (like Layer 2 message-signing), so it may make a really good walk-through EIP to show others how the process really works.

Would this be valuable to people?

---

**jpitts** (2019-04-02):

This would be really cool, I think a lot of people would follow it. [@mariapaulafn](/u/mariapaulafn) is creating “Summaries” of each core devs call, this could be in the same vein.

---

**timbeiko** (2019-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> so it may make a really good walk-through EIP to show others how the process really works.

Yes, if you could document your process that would be hugely valuable.

---

**timbeiko** (2019-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> Still no motion on this: Add Audience Review process to EIPs prior to Last Call by fubuloubu · Pull Request #1725 · ethereum/EIPs · GitHub

First time I heard of this. What would be the process for this to be moved forward?

---

**boris** (2019-04-02):

[@fubuloubu](/u/fubuloubu) getting changes made to EIP-1 is difficult.

---

**fubuloubu** (2019-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> What would be the process for this to be moved forward?

Something between reasoned discussion and civil war.

I copied the work that [@fulldecent](/u/fulldecent) did when adding Last Call.

Is a change to EIP-1 technically an EIP itself?

---

**fubuloubu** (2019-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> It’s fairly uncontroversial in my mind and also relatively simple with clear benefits

I regret ever making this statement.

---

**timbeiko** (2019-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> @fubuloubu getting changes made to EIP-1 is difficult.

Fair enough, but given how poorly the “consult the community” phase for ProgPow went, perhaps it would make sense to try and at least get feedback on this by Core Devs. I am not sure what the best mechanism to do so would be, especially since it is an old-ish PR.

---

**boris** (2019-04-02):

Hey, sorry, I just meant that – for the most part, Core Devs don’t care. [@fubuloubu](/u/fubuloubu) could ask it to be put on the agenda, but there really hasn’t been enough review / caring yet. So, up to people who want to make this change to hold a community call, get people interested in discussing, etc.

Right now – I personally am a “don’t care”. Meaning: I don’t want to expend energy on changing this aspect of the EIP process, AND I don’t think more people signing up to be Working Groups / Rings won’t appear. I’d prefer the energy to go into actually moving Core EIPs forward, AND having working groups / Rings around each of those areas.

So an action to take might be to take the current list of proposed EIPs → https://en.ethereum.wiki/roadmap/istanbul → and indicate which areas of Ethereum expertise are needed. For example, my team is working on EIP615, and the Ring there is, I guess, the ETH1x Ring, the Security Ring, and maybe there should be a VM & Precompiles Ring that encompasses EVM, eWASM, and precompiles.

Also: it would be good if this had it’s own discuss thread, rather than layers of governance thread ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**jpitts** (2019-04-03):

[@fubuloubu](/u/fubuloubu), perhaps the first step is to form an EIP Process Ring. This would be a good way to test interest level in maintainership of that. This group, as it establishes legitimacy, would have the authority to make changes to the EIP process. Probably it should do so with some representation or official comments from the Editors.

---

**fubuloubu** (2019-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> it would be good if this had it’s own discuss thread, rather than layers of governance thread

Could be a part of the *future* layers of governance, but definitely should move this part of the conversation into a different thread.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> EIP Process Ring

Will try and capture the ideas behind the establishment of this process ring into a new thread, out of the discussion of the current layers of governance.

---

**timbeiko** (2019-05-06):

Based on the contents in this thread, I’ve opened a PR to EIP-1 to add more context about what shepherding an EIP through the process implies. I’d appreciate feedback, if anyone has the time to review: https://github.com/ethereum/EIPs/pull/1991


---
source: magicians
topic_id: 4249
title: Who are the Core Devs? Improving EIP Process using Ranked Pair Voting
author: gh1dra
date: "2020-05-02"
category: Magicians > Process Improvement
tags: [governance]
url: https://ethereum-magicians.org/t/who-are-the-core-devs-improving-eip-process-using-ranked-pair-voting/4249
views: 1966
likes: 9
posts_count: 9
---

# Who are the Core Devs? Improving EIP Process using Ranked Pair Voting

It is clear from the ProgPow debacle that we need accountability more than ever when deciding which EIPs are accepted and are **actually implemented**. The biggest barrier seems to be trust, and from my understanding and brief research, there is no list of Ethereum Core Devs or even a clear process defined to become one. (See [@ameensol](/u/ameensol) am i core dev meme) The wider community (dapp developers, shit coin shillers, miners, os contributors, etc) have no idea who these people are, what are their motives, who do they work for, what EIPs have they supported in the past or have campaigned against.

This has led to the rise of twitter governance as some sort of arbiter of sentiment, when I believe we should be embracing some democratic process to determine *who should be considered a core dev*, and to start keeping track of support history of particular EIPs. While I understand this is controversial position to take, especially coming from someone outside this small community, in the long run it will bring credibility to the process, and an ability for the existing expert technical members to steer governance decisions in a way that can beneficial for the network as a whole and **all of its participants**.

I suggest that we start collecting the information of the existing core devs and having them use signed keys that they will use to vote in a Ranked Pair mechanism where they can signal which EIPs they support by moving all non-draft EIPs to a pointer on chain. We can either have [@souptacular](/u/souptacular) be the owner of this contract given [he has write-access of PM](https://github.com/ethereum/pm) start running elections and creating a whitelist of addresses that the community can vet using the one of many DID standards that have been floating around, where they can sign a standardized document that has the answers to the questions above as well as seniority / what projects they are actively contributed to / who is funding them. [@oed](/u/oed) [@jbaylina](/u/jbaylina) [@GriffGreen](/u/griffgreen)

Or instead of trusting one person to be a good guy **™**, and set up these contracts at regular intervals, we start airdropping NFTs to those whitelisted addresses and have a factory contract that spins up an election over some arbitrary cycle and use those tokens as tickets to entry.

It would be awesome if the conversation of what goes into this document happened in this thread so privacy grievances can be aired. Furthermore, if enough core devs / EF / EthMagicians / Consensys / whoever runs this shitshow comes to a consensus that this mechanism would be useful, we can run parallel elections where representatives of projects in let’s say this registry: https://everest.link/ ([@evabeylin](/u/evabeylin) idk Yaniv’s account) can have a vote and we weigh the results against each other. Let’s discuss what a fair ratio of that should be.

Here’s a repo with a contract if anyone wants to help build this: https://github.com/corydickson/ranked-pairs-voting

A dapp would be nice that aggregated this info

btw [all of the flaws in this mechanism](https://rangevoting.org/RankedPairs.html) are alleviated by the fact the state of the election is known to all potential voters at any given block height. I also think that this is real consensus as [@gcolvin](/u/gcolvin) described [here](https://ethereum-magicians.org/t/new-social-governance-layer-for-ethereum/4181/26):  there aren’t black and white decisions but instead a gradient of support.

tldr: Core Devs should vote on which EIPs go into the accepted state and this should be transparent and put on-chain

## Replies

**elliot_olds** (2020-05-03):

It looks like this proposal is based on the assumption that only the sentiment of core devs matters for which changes get adopted by the network, so we just need to figure out who is really a core dev. I strongly disagree with this view.

IMO a better path forward is to realize that the community as a whole needs to decide on these changes. With that approach, the big next steps become (a) improving our ability to measure sentiment across the community, and (b) deciding under what conditions negative community sentiment can block a change.

---

**masher** (2020-05-04):

[@elliot_olds](/u/elliot_olds) [@gh1dra](/u/gh1dra)

You both should check out this thread: [New Social Governance Layer for Ethereum](https://ethereum-magicians.org/t/new-social-governance-layer-for-ethereum/4181)

Indications on who is a core dev will be marked on this new application that is being worked on to become a social governance layer to aid core devs in gauging community snetiment on protocol changes.

---

**gh1dra** (2020-05-05):

> It looks like this proposal is based on the assumption that only the sentiment of core devs matters for which changes get adopted by the network

Not really, the idea is to split the weights across core devs and wider community members defined as projects that exist in this universal registry

---

**gh1dra** (2020-05-05):

I’m under the impression that kialo has been looked at before but this hasn’t gone anywhere in the past, it’s just has been treated as just another survey; looking to change this by bringing a standard voting process. Will check out the disc!

---

**souptacular** (2020-05-11):

Thanks for the write up! Great to see people trying to bring solutions to a process that is sub-par. My concern over your proposal, in the broadest sense, is that it starts to bring overhead and centralization to a process that works the vast majority of the time, except in the case of controversial EIPS, of which there are few. I can count on one hand the amount of times we would need a process that is more defined than the one we have now. That doesn’t mean there shouldn’t be a process for those controversial EIPs, but we need to keep in mind that it would be a huge turn-off to have to do on-chain voting for boring, low-level technical EIPs that the broader community doesn’t care about anyway, like changes to the network protocol (adding Snappy compression) or the addition of “simple subroutines” going into the EVM (an upcoming EIP going into Berlin that few in the community are aware of).

---

**gh1dra** (2020-05-14):

Firstly, thanks for taking the time out to consider this approach. To address your concern:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/souptacular/48/720_2.png) souptacular:

> but we need to keep in mind that it would be a huge turn-off to have to do on-chain voting for boring, low-level technical EIPs that the broader community doesn’t care about anyway, like changes to the network protocol (adding Snappy compression) or the addition of “simple subroutines” going into the EVM (an upcoming EIP going into Berlin that few in the community are aware of).

I realize after reading the initial post it does sound a bit overkill to use this as a finalization process. Treat this more as a sentiment analysis mechanism where all stakeholders are accounted for transparently. Do you know if there is a list of all the core developers that lives somewhere that’s sharable?

A more granular question would be, does the community just assume that everyone in the Ethereum Github org is a core dev?

---

**adamschmideg** (2020-05-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gh1dra/48/2472_2.png) gh1dra:

> A more granular question would be, does the community just assume that everyone in the Ethereum Github org is a core dev?

Organization membership on Github is not public by default. So those outside the organization can see less people [listed as members](https://github.com/orgs/ethereum/people).

---

**zhous** (2020-06-09):

Oh men. What we need is EtherDAO actually.

Centralization is not an option!

It’s a big topic.

Anyway, let’s say anybody who has contributed to an EIP with final status should have some vote weight.


---
source: magicians
topic_id: 4057
title: A ProgPoW Compromise Pre-Proposal
author: bendi
date: "2020-02-27"
category: Magicians > Primordial Soup
tags: [progpow]
url: https://ethereum-magicians.org/t/a-progpow-compromise-pre-proposal/4057
views: 6493
likes: 35
posts_count: 32
---

# A ProgPoW Compromise Pre-Proposal

This post summarizes an as-of-yet unwritten EIP for a compromise on ProgPoW. It has been created solely by myself, [Ben DiFrancesco](https://twitter.com/BenDiFrancesco), without the input or suggestion of any other persons or entities. The intent of this post is to share the idea, collect said input, and gauge community interest. Should such interest materialize, a formal EIP would be created.

## A Note On Compromises

By definition, a compromise entails an agreement where neither side is fully satisfied with the result. That means— if you have a strong opinion on ProgPoW— you won’t be happy with this proposal. That doesn’t mean it’s not a workable path forward for the community, so please don’t dismiss it outright.

## Motivations

As succintly and fairly as possible, I aim to present the motivations of each group below.

### Pro-ProgPoW (PPP)

1. Ethereum should strive for ASIC resistance because it’s part of the social contract as defined in the Yellow Paper.
2. Specialized hardware is inherently centralizing. It places the network at risk of being 51% attacked by secret ASIC’s, and/or disrupted intentionally while attempting to transition to PoS in ETH 2.0 by miners with mis-aligned incentives.

### Pro-Status-Quo (PSQ)

All consensus breaking upgrades are inherently risky, none more so than a change to the PoW mining algorithm. Thusly, the burden of justification lies with those proposing a change, and the threshold of such justification is very high. Based on the current state of the network, and on the unsettled state of the research related to ASICs and security, the Pro-ProgPoW arguments fall well short of the necessary threshold.

## Goals

This proposal aims to balance the security concerns of the PPP group with the risk aversion of the PSQ group. The security concerns of the PPP group are (to date) theoretical, but if we wait until attacks are observed to take action, it may be too late to avoid serious harm to the network. Conversely, if the PPP group’s concerns never actually materialize, then we risk serious harm to the network by implementing an unwarranted change.

The proposal does *not* aim to resolve the PPP group’s belief that ASIC resistance is an immutable part of Ethereum’s social contract (labeled #1 in the PPP Motivation section). Ultimately, this contention is a value judgement, one that each individual must evaluate for themselves.

## The Proposal

- ProgPoW should be fully implemented and tested across all major clients.
- ProgPoW should not be included as part of any planned or future upgrade hardfork.
- All clients should include a command line switch which enables ProgPoW at a block height specified by the node’s operator.
- A ProgPoW enabled hardfork of the Ropsten testnet should be created and maintained using this switch. (Up for debate: should this fork be a new, parallel testnet, or should it simply replace Ropsten).
- A strong Schelling point should be encouraged in the Ethereum community: if clear evidence of an ASIC-lead attack on the network is ever demonstrated, Ethereum stakeholders will coordinate to activate an emergency ProgPoW hardfork, at an agreed upon block height, using the switch.

## The Reasoning

Both the PPP group and the PSQ group share a desire for Ethereum to remain secure and decentralized, and to successfully transition to Ethereum 2.0. By fully implementing, testing, and maintaining compatibility with ProgPoW— and standing ready to activate it in the case of an emergency— we can coalesce on a solution that focuses on these common goals.

The existence of a fully implemented, tested, and easily enabled ProgPoW would serve as a sword of Damocles hanging over the heads of any would-be malicious miners. If they’re altruistic, it does them no harm. If they’re inclined to attack or to thwart Ethereum 2.0, it changes the incentive structure of any such attempt. Put simply, it acts as a deterrent

## Replies

**fubuloubu** (2020-02-27):

Thank you for starting this conversation! I think this is the best common-sense approach we have to resolving this issue amicably. Compromise is a very legitimate way to do this within the current system.

---

A few notes:

- This entire proposal may not make sense to have be an EIP. I think what should be done (coordinated further by this discussion) is 1) Move EIP-1057 to Accepted 2) Write a Meta-EIP coordinating the Ropsten fork. These make sense given the current EIP process, and aligns things up nicely for the political process to occur most efficiently.
- The political components of this discussion (this post, the letter called EIP-2538, other writings and posts spanning the entirety of this discussion) should be collected together in a reference-able format, perhaps a blog post on the Ethereum website.
- The agreement should be achieved on an ACD call by having people from both sides of the discussion come together and formally agree on this being the path forward, mentioning the work they’ve done in aligning the community down this path.

---

**greerso** (2020-02-27):

What are is/are the perceived risk/s that could cause serious harm to the network?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bendi/48/2535_2.png) bendi:

> All consensus breaking upgrades are inherently risky, none more so than a change to the PoW mining algorithm

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bendi/48/2535_2.png) bendi:

> if the PPP group’s concerns never actually materialize, then we risk serious harm to the network by implementing an unwarranted change.

What would the Schelling point look like?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bendi/48/2535_2.png) bendi:

> A strong Schelling point should be encouraged in the Ethereum community: if clear evidence of an ASIC-lead attack on the network is ever demonstrated, Ethereum stakeholders will coordinate to activate an emergency ProgPoW hardfork, at an agreed upon block height, using the switch.

We know efficient miners exist but are not widely available and E3’s will no longer be able to mine ethash mid April.  If you allow specialization now, you will have a rush of new investment into hardware, no idea what an attack would actually look like or where it was coming from.  Once the GPU’s are pushed out, you cant just fork to ProgPoW and expect to be back at a safe ~180TH/s, Ethereum would be vulnerable either way.

If you want to embrace ASIC’s, choose Keccak256 which is much easier to design an ASIC for, will be more competition so manufacturers will have to sell to public and it would issue a blow to rival chain ETC.

The ETC proposal.  [Change the ETC Proof of Work Algorithm to Keccak256 | Ethereum Classic Improvement Proposals](https://ecips.ethereumclassic.org/ECIPs/ecip-1049)

---

**cadilha** (2020-02-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bendi/48/2535_2.png) bendi:

> A strong Schelling point should be encouraged in the Ethereum community: if clear evidence of an ASIC-lead attack on the network is ever demonstrated, Ethereum stakeholders will coordinate to activate an emergency ProgPoW hardfork, at an agreed upon block height, using the switch.

It’s a fair attempt to reach a compromise but it’s contrary to governance minimization and defers the coordination burden to a later date.

Without an unequivocal prior definition of “clear evidence of an ASIC-lead attack on the network” then Ethereum will contentiously split.

It simply delays it from the next hardfork.

---

**mstobie-seequent** (2020-02-27):

It’s not just equivalent to a delay because it will probably never happen.

A 51% attack is easy to spot, there’s never more than a few blocks rewritten otherwise.

---

**bendi** (2020-02-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/greerso/48/1221_2.png) greerso:

> What are is/are the perceived risk/s that could cause serious harm to the network?

I think it should be obvious why a change to a new hashing algorithm is a risky one.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/greerso/48/1221_2.png) greerso:

> What would the Schelling point look like?

I think what you’re asking is, what is the definition of “clear evidence of an ASIC-lead attack.” This is a fair question that warrants discussion.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/greerso/48/1221_2.png) greerso:

> If you want to embrace ASIC’s, choose Keccak256 which is much easier to design an ASIC for, will be more competition so manufacturers will have to sell to public and it would issue a blow to rival chain ETC.

I don’t believe PSQ folks want to “embrace ASICs”, I think they want to avoid a risky change without clear evidence of it being required. For various reasons, I don’t think ETH should be making any decisions based on what ETC is doing.

---

**bendi** (2020-02-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cadilha/48/2539_2.png) cadilha:

> It’s a fair attempt to reach a compromise but it’s contrary to governance minimization and defers the coordination burden to a later date.
>
>
> Without an unequivocal prior definition of “clear evidence of an ASIC-lead attack on the network” then Ethereum will contentiously split.
> It simply delays it from the next hardfork.

A future split is possible, but I hardly see how it’s guaranteed. Ethereum is not Bitcoin— network upgrades are part of the social contract. If we’re hurtling toward a contentious split, then a compromise which gives us a good chance of avoiding one is worthwhile.

---

**ajsutton** (2020-02-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bendi/48/2535_2.png) bendi:

> I think it should be obvious why a change to a new hashing algorithm is a risky one.

This is not at all obvious. I can see why people might think the hashing algorithm is such a high risk part, but it’s actually relatively simple to test and have confidence in the implementation.  Changes to the EVM and other highly interrelated components are much more likely to cause chain splits due to bugs and are much harder to test comprehensively, yet people don’t raise the same concerns for them.

---

**fubuloubu** (2020-02-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajsutton/48/1102_2.png) ajsutton:

> yet people don’t raise the same concerns for them

In fact, the vast majority of EIPs that should have received the levels of attention this one has don’t get that attention, simply due to the fact that they’re unpolitical.

---

**greerso** (2020-02-28):

We’ve run it on a testnet, been audited, running on another testnet.

---

**bendi** (2020-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajsutton/48/1102_2.png) ajsutton:

> This is not at all obvious. I can see why people might think the hashing algorithm is such a high risk part, but it’s actually relatively simple to test and have confidence in the implementation. Changes to the EVM and other highly interrelated components are much more likely to cause chain splits due to bugs and are much harder to test comprehensively, yet people don’t raise the same concerns for them.

Fair, and granted. Let’s not spend time arguing over whether people *should* consider it risky, let’s just acknowledge the reality a large percentage of the community seems to and is unlikely to change their opinion. Given this, what do you think of this proposal as a way forward that  (hopefully) avoids a contentious fork?

---

**greerso** (2020-02-28):

If not risky why compromise on an option that *is* very risky?

---

**bendi** (2020-02-28):

Which part of my proposal is risky? And is it riskier than the on-the-ground reality of a potential contentious split of the network, and the damage that would cause, if ProgPoW is crammed down on a segment of the community which vehemently opposes it?

---

**greerso** (2020-02-28):

It’s risky in that there will not be enough miners on standby to defend against the undetectable attack you won’t be forking from because of imperfect governance.

Some community is against because it’s risky, but it isn’t, now they’re still against it enough to participate in a contentious split for why?  We’re headed back into meta contention.

---

**bendi** (2020-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/greerso/48/1221_2.png) greerso:

> It’s risky in that there will not be enough miners on standby to defend against the undetectable attack you won’t be forking from because of imperfect governance.

What is this undetectable attack you’re alluding to?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/greerso/48/1221_2.png) greerso:

> Some community is against because it’s risky, but it isn’t, now they’re still against it enough to participate in a contentious split for why? We’re headed back into meta contention.

Some people believe it’s risky. You don’t agree with them, which is fine, but you’re also unlikely to convince them otherwise. Compromise is about moving forward despite disagreeing in a way that’s productive, if not ideal, for both parties.

---

**greerso** (2020-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bendi/48/2535_2.png) bendi:

> What is this undetectable attack you’re alluding to?

The issue will be centralization by miners newly invested into PoW ethash with a multi-million dollar per day pot of rewards. ‘Attack’ doesn’t have to mean double spend against exchange and reorganize.  How can we not recognize that as risky yet think an audited small ethash fix is risky?

I can’t tell you what the attack will be, only that the incentive and opportunity will be there without ProgPoW, less so with.

---

**bendi** (2020-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/greerso/48/1221_2.png) greerso:

> ‘Attack’ doesn’t have to mean double spend against exchange and reorganize. How can we not recognize that as risky yet think an audited small ethash fix is risky?

Surely an attack must at least be detectable in some way. If you don’t even know it’s happening, does it qualify as an attack?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/greerso/48/1221_2.png) greerso:

> I can’t tell you what the attack will be, only that the incentive and opportunity will be there without ProgPoW, less so with.

The proposal specifically aims to address the incentive to attack. If they do, then their ASICs will be hardforked into uselessness by a community that is prepared to do so. It’s a deterrent.

---

**greerso** (2020-02-28):

The ‘attack’ doesn’t even have to involve hashing. I would bet on constant sewing doubt and meddling in the multi-year transition to PoS.  Maybe not in their own name, we have no idea who has the Canaan V10’s, V2200’s or the magic ethash fpgas.

I don’t think speculating on what an attack could look like without even knowing what the target (transition to PoS) looks like is practical.

The threat of fork is no threat at all if you no longer have the miners to protect from rented hash. It’s an empty threat.

Can we get to the bottom of why the people so opposed are so opposed and continue to try to find compromise with that information?

If they are invested in A10’s, Bitmain or Canaan, be honest about it, let’s get them shipping ProgPoW ASICs with the 20% efficiency gain, we have an enormous number of miners that would buy them.  ~~If they have E3’s they’re done anyway, maybe we propose reducing the DAG size and speaking to [@OhGodAGirl](/u/ohgodagirl) about the possibility of an E3 firmware update to mine ProgPoW. Bitmain says they’re GPU inside on their statement about the DAG issue.~~

https://twitter.com/OhGodAGirl/status/1233431665281773570

---

**bitsbetrippin** (2020-02-28):

I am looking to host a livestream tomorrow to talk through the various conversations I have had with community members, developers and interactions publicly and privately on the topic. This is the most level set solution to date, given the public discourse and I have a few ideas on the trigger or better put, the Schilling Point.

I will highlight this proposal in that stream along with Hudsons post if its ready by then. Some of these conversations, we are simply talking past each other and concerned overall for network health in different perspectives.

---

**greerso** (2020-02-28):

This is a link to one of the many discussions on this very idea.

https://gitter.im/ethereum-cat-herders/ProgPoW-review?at=5d836ff95ab93616941cc4b5

---

**bitsbetrippin** (2020-02-29):

I’m reading through this, but there is not point to debate with someone that is selflessly arrogant. That kinda statement tells me all I need to know with the weight of their influence and position within this ecosystem.

![image](https://ethereum-magicians.org/uploads/default/original/2X/9/92d67757acbf4a6aaa7359a1bbc9945c89175afd.png)


*(11 more replies not shown)*

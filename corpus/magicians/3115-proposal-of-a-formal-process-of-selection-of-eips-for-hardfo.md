---
source: magicians
topic_id: 3115
title: Proposal of a formal process of selection of EIPs for hardforks (Meta EIP#)
author: poojaranjan
date: "2019-04-10"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/proposal-of-a-formal-process-of-selection-of-eips-for-hardforks-meta-eip/3115
views: 2443
likes: 18
posts_count: 19
---

# Proposal of a formal process of selection of EIPs for hardforks (Meta EIP#)

The discussion started around March 2017 when Alex Beregszaszi ([@axic](/u/axic)) proposed Meta [EIP 233: Formal process of hard forks](https://eips.ethereum.org/EIPS/eip-233) to describe the formal process of preparing and activating hard forks.

In Dec 2018, [Afri Schoedon proposed to write an EEP](https://ethereum-magicians.org/t/eep-5-ethereum-hardfork-process-request-for-collaboration/2305) to define the Ethereum Network Upgrade Process. [EEP-5](https://github.com/karalabe/eee/issues/5) primarily covers Ethereum 1.0 upgrades. It suggested moving from ad-hoc hardforking to fixed-schedule and provides a general outline process with all required stages of hardforking.  It was also pre-announced and requested for collaboration at [Eth Magician](https://ethereum-magicians.org/t/eep-5-ethereum-hardfork-process-request-for-collaboration/2305) then.

Based on the recent discussions in [ECH meeting #8](https://github.com/ethereum-cat-herders/PM/blob/master/All%20Ethereum%20Cat%20Herder%20Meetings/Meeting%208.md) and [ECH meeting #9](https://www.youtube.com/watch?v=Lvqma0uHQ1U&),a formal process of selection of EIPs for hardforks (Meta EIP#) is proposed  [#1929](https://github.com/ethereum/EIPs/pull/1929).

The ultimate goal is to have well defined process which every EIP author may follow in order to add EIP in next upgrade.

## Replies

**fubuloubu** (2019-04-11):

Absolutely love this, great proposal!

One suggestion I do have:

In 1929 it suggests to “Discuss it on gitter, reddit, and Twitter”. I would suggest the EthMagicians forum (mentioned in the prior sentence) be the source for discussions of an EIP, to prevent information dispersal through an endless variety of social channels. I would suggest to modify that sentence to the following:

“Inform others of the proposal via social channels, such as gitter, reddit, and twitter”

which implies that these are not “officially sanctioned” venues for discussion of EIPs (i.e. it’s not listed as `discussions-to` formally in the EIP).

That’s not to say it shouldn’t be discussed on other social platforms, but that any serious concerns brought up on such platforms may not be considered in the process unless the conversation is brought to the official forum outlined in the EIP through `discussions-to`.

---

This small language change I think would help to reinforce that the EIP has an official discussion forum to raise questions and concerns of the proposal, and to come to technical (and non-technical?) consensus on the proposal.

---

**fubuloubu** (2019-04-11):

Another potential edit I might have to this is that EthMagicians itself is not *required* to be the `discussions-to` forum, but that only one such forum should be specified for the discussion of a particular EIP.

An example of this might be that a proposal that is almost entirely non-technical in the concerns might find an alternate forum for `discussions-to` if EthMagicians is considered “inappropiate” by the author to host the discussions for *some* reason.

---

**poojaranjan** (2019-04-11):

Thanks for feedback. I think it make sense to suggest EthMagician to be the discussion forum but author may decide it as per their preference.

---

**Arachnid** (2019-04-11):

I’m not sure how I feel about using the EIPs repository to coordinate the contents of a hard fork; it risks confusing the EIP standardisation process with network governance, and the perception that EIP editors are the ones who decide what goes into a fork.

Other than that, this is a nice step forward in formalising forks.

---

**poojaranjan** (2019-04-12):

Thanks for feedback. This is an initiative by Ethereum Cat Herders (ECH) to help out as HF coordinator, as discussed previously in All core dev call. So, if it is accepted by All core devs / EIP editors,  we may make a slight change in this process of submission of EIPs. I hope it can also be  managed at [ECH GitHub](https://github.com/ethereum-cat-herders/PM/issues). Would love to hear more about  how does this sound?

---

**souptacular** (2019-04-26):

I think this is great! I agree with [@Arachnid](/u/arachnid) and [@fubuloubu](/u/fubuloubu)’s suggestions, with the exception that the EIP author should be able to choose the venue for discussion as you mentioned in another comment. Having ECH helping manage this will help with organization of future hard forks.

---

**fubuloubu** (2019-04-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/souptacular/48/720_2.png) souptacular:

> with the exception that the EIP author should be able to choose the venue for discussion

Clarification: you agree or disagree that the author should have the option to specify the venue? Confusing sentence ![:sweat:](https://ethereum-magicians.org/images/emoji/twitter/sweat.png?v=12)

---

**boris** (2019-04-26):

I still don’t understand how this differs from what the updated 233 outlines (PRs to hardfork meta) other than centralizing on CatHerders repo.

I’d rather see more updates to 233 rather than a separate Meta EIP.

---

**souptacular** (2019-04-26):

Whoops! It is confusing, my bad. The EIP author should be able to choose the venue.

---

**souptacular** (2019-04-26):

Good point. It may be better to iterate on 233. What do you think [@poojaranjan](/u/poojaranjan). I can connect you with Alex ([@axic](/u/axic)) and others who are working on 233.

---

**fubuloubu** (2019-04-26):

Perhaps it is more useful to ask what purpose does ECH serve, and how they might fit within the process as the provider of *some* necessary service, and just keep that general (don’t specifically mention ECH).

I’ve thought about what it means to fulfill the PM role here, and really I think it ends up looking a lot like a political whip: querying different people on their opinions, building consensus, and understanding the political “lay of the land” in as non-partisian a way as possible.

---

**poojaranjan** (2019-04-26):

[EIP 1929](https://github.com/ethereum/EIPs/blob/16e64a488cd16403b884417799074aae77be41ab/EIPsForHardfork.md) may be considered as a story of [EIP 233](https://eips.ethereum.org/EIPS/eip-233) in Agile methodology; explained [here](https://github.com/ethereum-cat-herders/PM/issues/60).

To be brief, purpose, user and flexibility are the main reasons, I think they should be separate EIPs.

However, I will be happy to connect with Alex(@axec) and others who are working on 233 to further refine the HF process.

---

**poojaranjan** (2019-04-26):

I further think that EIP 1929 is process centric and not people/group centric. The purpose is to set up a process that may be followed with or without any individual /group.

---

**fubuloubu** (2019-04-26):

Does EIP 1929 make a proposal to change the current process? Or is it an attempt to document what the process is?

---

**poojaranjan** (2019-04-26):

It is an attempt to document the process rather than changing the process. But in the process, it may also bring more clarity to new people who would want to contribute.

---

**fubuloubu** (2019-04-26):

I think documenting the process is super, super helpful!

I also think that if there is no change proposed, an EIP isn’t necessary. I think that’s where a lot of the confusion is coming from with regards to this.

---

**poojaranjan** (2019-04-26):

I agree. I am not sure if we have any other way to document the process/improvement in Ethereum.

---

**poojaranjan** (2020-09-19):

It’d be great to see this process documented somewhere, hence updated the proposal:

- destination repository:  ECH -> Eth1.0 spec
- Tracker: ‘EIP readiness tracker’ -> ‘Network upgrade tracker’
- added ‘Network upgrade stages’

PR available for review: https://github.com/ethereum/EIPs/pull/1929


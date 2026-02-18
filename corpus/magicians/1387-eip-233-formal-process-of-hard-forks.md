---
source: magicians
topic_id: 1387
title: "EIP-233: Formal process of hard forks"
author: axic
date: "2018-09-19"
category: EIPs > EIPs Meta
tags: []
url: https://ethereum-magicians.org/t/eip-233-formal-process-of-hard-forks/1387
views: 4613
likes: 8
posts_count: 12
---

# EIP-233: Formal process of hard forks

This topic is intended be the discussion for EIP-233. Any comment or feedback is very much appreciated!

https://eips.ethereum.org/EIPS/eip-233

## Replies

**jpitts** (2018-09-20):

[@axic](/u/axic), how do you think that this would appear in the process outlined in [EIP-1](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1.md)?

Perhaps defining a separate EIP such as [EIP-233](https://eips.ethereum.org/EIPS/eip-233) for actions taken by specified stakeholders in the community is an optimal approach, rather than aggregate all possible actions by non-Editors into EIP-1.

From EIP-1, this section in particular mentions the hard fork process:

> Accepted (Core EIPs only)  – This EIP is in the hands of the Ethereum client developers. Their process for deciding whether to encode it into their clients as part of a hard fork is not part of the EIP process.
>
>
>  Final – Standards Track Core EIPs must be implemented in at least three viable Ethereum clients before it can be considered Final. When the implementation is complete and adopted by the community, the status will be changed to “Final”.

---

**MicahZoltu** (2018-09-20):

I don’t think the EIP repo should be used for this, nor should the EIP process be used for this.  The EIP process is a standards process.  Hard forks are a deployment process.  They are fundamentally different and IMO should be kept separate with separate processes.

For an analogy, W3C has a process for coming up with web standards and a place for hosting them and discussing them, but it doesn’t contain process for browser deployment/rollout or how web developers go about adopting new features.

---

**boris** (2018-09-20):

One of these days I’m just going to stake all my opinions with Micah.

BUT — we (with a definition of we needed) need to get better at hard forks. Who what where is that discussed.

Browsers are in competition and don’t need to coordinate to keep the Internet from breaking. In fact, they regularly break portions of it due to individual decisions.

---

**MicahZoltu** (2018-09-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Browsers are in competition and don’t need to coordinate to keep the Internet from breaking. In fact, they regularly break portions of it due to individual decisions.

I think client developers can communicate among themselves however they like, including a GitHub repository where people propose things and a process for ratifying those proposals across teams.  ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)  I merely think that co-locating that decision making process with the standards process is not a good idea.  I make no claims that the EIP process format shouldn’t be used.  ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**axic** (2019-01-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> @axic, how do you think that this would appear in the process outlined in EIP-1 ?
>
>
> Perhaps defining a separate EIP such as EIP-233  for actions taken by specified stakeholders in the community is an optimal approach, rather than aggregate all possible actions by non-Editors into EIP-1.

I think EIP-1 is rather complex already and as [@MicahZoltu](/u/micahzoltu) reasons it may be a different process.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I don’t think the EIP repo should be used for this, nor should the EIP process be used for this. The EIP process is a standards process. Hard forks are a deployment process. They are fundamentally different and IMO should be kept separate with separate processes.

I think your reasoning is compelling, but I would say the situation is a bit more complex than that.

The meta “hard fork” EIPs I think are needed, because changes can be very interconnected/interdependent and there must be a way to a place to discuss how can they bundled.

---

**jpitts** (2019-01-21):

I’m really glad this discussion is back!

Creating a Meta HF EIP document should be a key part of the upgrade process. I would advocate for specifying that it is for a HF rather than just “Meta EIP”, and for using a code in referring to them along the lines of ERCs, e.g. HFM-1013 with the same numbering as EIP-1013.

I was recently looking at how the version of the protocol has advanced over time, and these HFMs were very helpful.


      [gist.github.com](https://gist.github.com/jpitts/4c541a4efa2f8872ce9acf63da5c4921)




####

##### ethereum-protocol-versions.md

```
| Version | Code Name | Block No. | Released | Incl EIPs | Specs | Impls |
|---------|-----------|-----------|----------|-----------|-------|-------|
| 1.0.0 | Frontier | 1 | 07/30/2015 10:26:28 AM | | | [Geth v1.0.0](https://github.com/ethereum/go-ethereum/releases/tag/v1.0.0) |
| 2.0.0 | Frontier Thawing | 200000 | 09/07/2015 4:33:09 PM | | | [Geth v1.0.1.1](https://github.com/ethereum/go-ethereum/releases/tag/v1.0.1.1) |
| 3.0.0 | Homestead | 1150000 | 03/14/2016 12:49:53 PM | [EIP-2](https://eips.ethereum.org/EIPS/eip-2)
 [EIP-7](https://eips.ethereum.org/EIPS/eip-7)
 [EIP-8](https://eips.ethereum.org/EIPS/eip-8) | [HFM-606](https://eips.ethereum.org/EIPS/eip-606) | [Geth v1.3.4](https://github.com/ethereum/go-ethereum/releases/tag/v1.3.4) |
| 4.0.0 | DAO Fork | 1920000 | 07/20/2016 8:20:40 AM |  | [HFM-779](https://eips.ethereum.org/EIPS/eip-779) | [Geth v1.4.10](https://github.com/ethereum/go-ethereum/releases/tag/v1.4.10) |
| 5.0.0 | Tangerine Whistle | 2463000 | 10/18/2016 8:19:31 AM | [EIP-150](https://eips.ethereum.org/EIPS/eip-150) | [HFM-608](https://eips.ethereum.org/EIPS/eip-608) | [Geth v1.4.8](https://github.com/ethereum/go-ethereum/releases/tag/v1.4.18) |
| 6.0.0 | Spurious Dragon	 | 2675000 | 11/22/2016 9:15:44 AM | [EIP-155](https://eips.ethereum.org/EIPS/eip-155)
 [EIP-160](https://eips.ethereum.org/EIPS/eip-160)
 [EIP-161](https://eips.ethereum.org/EIPS/eip-161)
 [EIP-170](https://eips.ethereum.org/EIPS/eip-170) | [HFM-607](https://eips.ethereum.org/EIPS/eip-607) | [Geth v1.5.1](https://github.com/ethereum/go-ethereum/releases/tag/v1.5.1) |
| 7.0.0 | Byzantium | 4370000 | 10/16/2017 12:22:11 AM	 | [EIP-100](https://eips.ethereum.org/EIPS/eip-100)
 [EIP-140](https://eips.ethereum.org/EIPS/eip-140)
  [EIP-196](https://eips.ethereum.org/EIPS/eip-196)
 [EIP-197](https://eips.ethereum.org/EIPS/eip-197)
 [EIP-198](https://eips.ethereum.org/EIPS/eip-198)
 [EIP-211](https://eips.ethereum.org/EIPS/eip-211)
 [EIP-214](https://eips.ethereum.org/EIPS/eip-214)
 [EIP-649](https://eips.ethereum.org/EIPS/eip-649)
 [EIP-658](https://eips.ethereum.org/EIPS/eip-658) | [HFM-609](https://eips.ethereum.org/EIPS/eip-609) | [Geth v1.7.0](https://github.com/ethereum/go-ethereum/releases/tag/v1.7.0) |
```

This file has been truncated. [show original](https://gist.github.com/jpitts/4c541a4efa2f8872ce9acf63da5c4921)

---

**jpitts** (2019-01-21):

Also related to EIP-233 discussion is this idea I’ve been working on about semantic versioning and release candidates.

Perhaps the HF Meta EIP document could have an event list, referring to all attempts to release the upgrade, and which network this happened on (i.e. 8.0.0-rc1 deployed to Ropsten).



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png)
    [Sermantic versioning for the protocol, with release candidates](https://ethereum-magicians.org/t/sermantic-versioning-for-the-protocol-with-release-candidates/2493) [Primordial Soup](/c/magicians/primordial-soup/9)



> From my comment in the  Jello Paper discussion:
>
> And regarding “release candidates”, copying my comments from AllCoreDevs gitter here:
>
> Protocol updates could follow the practice of “release candidate” within the semantic numbering scheme. And these clever release names, this is over-arching for the upgrade initiative and sticks once it stabilizes on mainnet. Constantinople is what you are attempting to get mainnet to.
> So what you attempted to release was ethereum-8.0.0-rc1, released to the t…

---

**MicahZoltu** (2019-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> The meta “hard fork” EIPs I think are needed, because changes can be very interconnected/interdependent and there must be a way to a place to discuss how can they bundled.

I agree that there needs to be a place to coordinate and discuss.  I merely argue that we should have a separate place, not the standards repository.  I would love it if ETH, ETC, EOS, etc. Could all use this repo for EIPs, and then each had a separate place for discussing *which* EIPs went into a hard fork, what block it was on, etc.

---

**shemnon** (2019-03-01):

I think the biggest value in a formal hardfork process is a schedule of events.

For a comparison to how another mature community handles this Java recently (2 years ago) went to a rapid release cadence, which for Java is every 6 months instead of every 2-3 years.  The rapid release allows for features to slip a release when there is certainty that another release is fairly soon.  Key to that is a schedule of dates where a feature must be ready or be dropped.  Miss the train when it left the station?  No worries another one is coming soon and at a fixed schedule.  Java’s strict schedule is based on bugs and severity level - (https://openjdk.java.net/jeps/3).  For us I think all features are the same level.

Based on Afri’s previous schedule ([EEP-5: Ethereum Hardfork Process - request for collaboration](https://ethereum-magicians.org/t/eep-5-ethereum-hardfork-process-request-for-collaboration/2305/4)) it would look something like

- T minus 20 weeks / 5 months - hard deadline to accept proposals for “Istanbul”
- T minus 12 weeks / 3 months - Client Implementations Due
- T minus 8 weeks / 2 months- Testnet Network Update
- T - Mainnet Network Update

It would be nice to add a “Finished EIPs for consideration due” at 24 weeks/6 months and “EIPs announce intent” sometime before that (28 weeks / 7 months)?  For a notional Oct 2019 launch that would mean that EIPs are due in April and the hard cutoff is May.  EIPs trying to get in should announce their intent in March, which is now.

If we do a 9 month cadence we have 2 months of quiet after the hard fork, or room to move the hard fork out if needed.  At 6 months we would have an overlapping period between client implementations due and the network update.

This would give a deadline for the drivers of the EIPs to get ready for the hard fork and would provide certainty as to whether or not EIPs are going to be in the fork or not based on an impartial schedule.

---

**boris** (2019-03-19):

I made a PR finally [@axic](/u/axic) – feel free to edit https://github.com/ethereum/EIPs/pull/1852

Main two changes:

(1) Embed a timeline in the EIP

(2) Proposed EIPs need to get PR’d into the Hardfork Meta EIP

I embedded a template and I also updated Istanbul to follow the format.

---

**boris** (2019-04-23):

This is now merged. We can make a call for EIPs that want to be included in Istanbul to do PRs.


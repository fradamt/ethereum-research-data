---
source: magicians
topic_id: 2396
title: ETH1x Istanbul Prep Meeting
author: boris
date: "2019-01-11"
category: Working Groups > Ethereum 1.x Ring
tags: [eth1x, istanbul, coredev]
url: https://ethereum-magicians.org/t/eth1x-istanbul-prep-meeting/2396
views: 3902
likes: 17
posts_count: 21
---

# ETH1x Istanbul Prep Meeting

The next ETH 1.x / Core Dev in person meeting is confirmed for San Francisco at the end of January.

While looking at the [Istanbul roadmap timing](https://en.ethereum.wiki/roadmap/istanbul), May 17th is the hard deadline to accept proposals (EIPs) for the Istanbul network upgrade in October 2019.

I propose to hold an ETH 1.x / Core Dev meeting the day after ETHCC in Paris, which would be March 8th. This can be an early review of what people are planning to propose / have proposed already, get talking with implementors, and so on.

It may also be useful to host an ETH1.x (/ ETH2 ?) AMA during either EthMagicians Council of Paris 2019 or at ETHCC itself? Similar to the one in Prague.

## Replies

**boris** (2019-02-07):

I know that [@5chdn](/u/5chdn) had mentioned that he will be in Paris and wants to discuss, but as of right now, the timeline is too tight to for this.

So, with the context of roadmap timing in mind again,  it looks like May 17th is the hard deadline to accept proposals.

[@5chdn](/u/5chdn) [@souptacular](/u/souptacular) [@Arachnid](/u/arachnid) [@fulldecent](/u/fulldecent) from your points of view, does this mean EIPs in state “Accepted” by May 17th, at which point there is discussion / planning to add them to [EIP 1679 Istanbul hardfork Meta](https://eips.ethereum.org/EIPS/eip-1679) or not?

(1) Which means that before then, the EIP must be in Draft, brought up at a CoreDevs agenda, and acknowledged to be Accepted if non-controversial?

Or (2), the EIP must be in Draft, and a PR against 1679 to propose it for inclusion? PR remains open until such time implementations of two major clients are completed, EIP itself could be Draft or Accepted.

If so, I would suggest – if there is need / interest in meeting in person – that a meeting happen **no later than April 17th, 2019**, one month before the proposal deadline.

Who is interested in hosting / helping organize?

---

**boris** (2019-02-08):

[Posted this to to try and get on the agenda for Feb 15 CoreDev call](https://github.com/ethereum/pm/issues/77#issuecomment-461926354)

What does a cadence of in-person meetings looks like for other hardfork roadmap key dates?

Do CoreDevs need to meet in person regularly?

What topics are useful to do in person? Can I and others help with some of the planning / logistics?

---

**timbeiko** (2019-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> So, with the context of roadmap timing in mind again, it looks like May 17th is the hard deadline to accept proposals.

Where has this been stated? Thanks!

---

**boris** (2019-02-08):

Link in the OP on the Ethereum wiki (I created that page) --> https://en.ethereum.wiki/roadmap/istanbul

Afri is the one that posted the schedule originally, which I have linked in the wiki page. Ideally the wiki is more visible and can easily be referenced.

---

**fulldecent** (2019-02-11):

Thanks for the ping. Yes, I believe Accepted status before May 17th is a prerequisite. Then people, ideally people with skin in the game (e.g. they are implementing it [i.e. core devs]), will nominate to add that to 1679. Authors Alex and Afri own that PR and they have the prerogative to add it if they like.

Working backwards, get your proposals into Last Call before April ends to be in Accepted by May 17th. But practically speaking, somebody might nominate to provisionally add a proposal to 1679 if it is still in last call.

---

Process-wise, it is not necessary to bring anything to core devs to get to Accepted status. But practically speaking, yes, if you are asking other people to nominate and implement your proposal and then advocate 10,000 nodes to upgrade then you should be polite, include them and understand their appetite.

---

I am interested to participate. Not sure yet if I will physically be at Paris ETHCC, hopefully I can get a client to engage me to attend.

---

**boris** (2019-02-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Working backwards, get your proposals into Last Call before April ends to be in Accepted by May 17th.

Of course, excellent point!

In practice, I think Last Call / Accepted and proposal / acceptance into the Hardfork meta have some wiggle room to happen in parallel. [@5chdn](/u/5chdn)’s wording in the roadmap was more about signaling that teams were going to try to get EIP XXXX into the hardfork, and propose it to the client teams.

I think Paris is unlikely to be anything other than an ad-hoc meeting – hence trying to determine when the next scheduled meeting should be.

BUT – I think it would be super helpful to have an EIP process discussion. We can have that during Council of Prague / EthMagicians ([added to Rings HackMD](https://hackmd.io/DaJhrasLQteUk3IwX5bQAg)). I will be there and will at least try and work through this all so it is clear-er ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) For that session, I can try and dial you in remotely if you can’t make it in person.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Process-wise, it is not necessary to bring anything to core devs to get to Accepted status.

OK, I’ll bite: how does an EIP get to be Accepted without bringing it to Core Devs?

---

**fulldecent** (2019-02-11):

Thank you, happy to dial in.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> OK, I’ll bite: how does an EIP get to be Accepted without bringing it to Core Devs?

Easy! You write a proposal, request a two-week review and then emerge from the review unscathed. This is all spelled out here [EIP-1: EIP Purpose and Guidelines](https://eips.ethereum.org/EIPS/eip-1#eip-work-flow)

---

If anybody wants to get work done /before/ the next meeting then please help get this merged – https://github.com/ethereum/EIPs/pull/1297. This is a baby step and is uncontroversial. Before getting involved in a project I always make a quick PR first just to learn the maintainer’s appetite for accepting stuff. (Which is why I’m more involved with other projects than than EIPs!) Anyway, if 1297 gets merged then I’ll be emboldened to make another PR with more changes that are worth discussing.

---

**cdetrio** (2019-02-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Thank you, happy to dial in.
>
>
>
>
>  boris:
>
>
> OK, I’ll bite: how does an EIP get to be Accepted without bringing it to Core Devs?

Easy! You write a proposal, request a two-week review and then emerge from the review unscathed. This is all spelled out here [EIP-1: EIP Purpose and Guidelines](https://eips.ethereum.org/EIPS/eip-1#eip-work-flow)

There is a lot of confusion around this because Core protocol changes are EIPs, and contract standards and RPC apis and so forth are also EIPs (“not core EIPs”). When this change to EIP-1 was made last year, I thought it was a typo that was overlooked by some EIP editors:

> Accepted (Core EIPs only) – A successful Last Call without material changes or unaddressed technical complaints will become Accepted.
>  Final (Not core EIPs) – A successful Last Call without material changes or unaddressed technical complaints will become Final.

The process as described there conflicts with the definitions of the terms stated on the [README](https://eips.ethereum.org/), and with the actual process of getting EIPs adopted. Here’s the terms on the README (full disclosure: I wrote these):

> Draft  - an EIP that is open for consideration.
> Accepted  - an EIP that is planned for immediate adoption, i.e. expected to be included in the next hard fork (for Core/Consensus layer EIPs).

So there are two definitions of `Accepted` for Core EIPs now:

1. The one stated in EIP-1. Accepted only means the Core EIP went through a two week “last call” phase before its status was upgraded to Accepted.
2. The one stated in the readme. Core EIPs are updated from Draft to Accepted after AllCoreDevs reach provisional agreement (by rough consensus) to schedule it for adoption in the next fork.

Also in EIP-1:

> Accepted (Core EIPs only) – This EIP is in the hands of the Ethereum client developers. Their process for deciding whether to encode it into their clients as part of a hard fork is not part of the EIP process.

From what I recall of the discussion around that update to EIP-1, that change was made because some people wanted to make the EIP process explicit and formal (there was even an earlier version of EIP-1 that was mistakenly merged, which stated that EIPs are accepted after a “vote”). But since the AllCoreDevs process is informal and resistant to structure, they hoped that AllCoreDevs would define/document their own process, separately from the EIP process. (at least that’s how I remember it. Maybe others had a different rationale for wanting to consider AllCoreDevs as a separate process which shouldn’t be documented in EIP-1).

That never really happened, I guess because it would require AllCoreDevs to start using a new term to mean “rough consensus was reached on AllCoreDevs” (currently they use `Accepted` to mean this). It was also confusing because the original point of EIPs was for core devs to document changes to the core protocol (hence the whole category of “Core” EIPs). Later, contract devs began to use EIPs to document contract standards. Then a change to EIP-1 is made stating that the process around Core EIPs isn’t an EIP process, and so EIP-1 isn’t the right place to document how Core EIPs progress from Draft to adoption on the mainnet.

So I don’t know, either someone needs to tell the Core Devs that they should stop using EIPs to schedule core protocol changes and that they need their own separate process (in alignment with the current version of EIP-1; and the EIPs readme should be updated so that it is consistent with EIP-1.). Or EIP-1 should attempt to describe the AllCoreDevs process around Core EIPs, using the same terminology that core devs use. I’d prefer the latter, which is to write a descriptive document, i.e. *describe* the group’s current behavior. The former requires forcing a group to change their current behavior (writing a document that *prescribes* new behavior), which is unlikely to be successful.

---

**fulldecent** (2019-02-11):

Cool, thanks for catching up. I am the author (“blame line”) on these relevant policies in EIP-1. And subsequently I am responsible for the inconsistency and all confusion. Sorry!

Here’s how it happened and where I think we can go. I was very involved when getting ERC-721 through. And I promised everybody that I would do whatever necessary to get it done, even if that means fixing EIPs and Solidity and 165 and anything we depended on. I quickly learned these facts about the EIP process.

- EIP editors do not want to adjudicate EIPs – see @pirapira and many other discussion on EIP-1 PRs.
- Core Devs do not have the bandwidth to handle the amount of innovation coming through EIPs – see 721 review rejected from Core Dev project meetings.
- Drafts could suddenly become final based on editor whims.
- EIP editors do not care about forking block numbers

This next one is a logical conclusion of the above:

- The EIP process applies to Ethereum Classic, POA and other networks just as well as mainnet.

I implemented (this might be contentious) these changes:

- Everything goes through a two week review process (idea stolen wholesale from Swift Evolution process)
- The two week review is attached to an RSS feed
- Encourage people to see the RSS feed

I hope I can have your support to update the README to match this process. This would mean:

- Update README
- Let AllCoreDevs use any language they want. But they should publish their own page (outside of EIPs) to mention Accepted EIPs which are under development. (Idea stolen from Swift Evolution process).
- Invite other core dev teams to emerge and implement whatever they want.

---

I could not achieve consensus to implement the following changes. But I’ll proceed and try again if somebody with commit access gives me the green light (plus a little coaching) and/or if my PR on EIP-1 is accepted:

- Mandate discussion for all last reviews to occur on a specific, canonical place which is archived. (Idea stolen wholesale from Swift Evolution.) (That place would be here, Ethereum Magicians.)
- Rename Core EIPs -> EIPS, ERCs to ERCs. Remove categories.
- Note that state changes would not count as EIPs ore ERCs. And then SAY NOTHING FURTHER ON THAT TOPIC. (This closes two specific EIPs as out of scope.)
- Make a separate page to track EIP deployments on various networks (deployment block numbers).
- Close GitHub Issues and direct a canonical place for discussions. (That place would be here, Ethereum Magicians.)

---

I will run out of steam and stop pushing this agenda. So if I’m bothering people, just wait and I’ll go away. But if people want me to be involved I’ll need a little validation at some point and resources.

---

**5chdn** (2019-02-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Where has this been stated? Thanks!

It’s in some protocol of recent core-dev calls.

There will be a spec/roadmap document available once the constantinople dust settles.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5chdn/48/1242_2.png)
    [EEP-5: Ethereum Hardfork Process - request for collaboration](https://ethereum-magicians.org/t/eep-5-ethereum-hardfork-process-request-for-collaboration/2305) [Primordial Soup](/c/primordial-soup/9)



> This is a pre-announcement and request for collaboration. I’m planning to write an EEP to define the Ethereum Network Upgrade Process. EEP-5 here primarily covers Ethereum 1.0 upgrades.
> ---
> EEP: 5
> Title: Ethereum Hardfork Process
> Authors: Afri Schoedon
> Status:  Draft
> Version: 2018-12-31
> Discuss:
> ---
>
> General outline:
>
> whereas EEP-1 defines distinct consensus updates, this is suggesting a framework for upgrading the Ethereum network
> this suggests moving from ad-hoc hardforking t…

---

**boris** (2019-02-13):

Thanks for this Casey, and thanks [@fulldecent](/u/fulldecent) for continuing to work on this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cdetrio/48/482_2.png) cdetrio:

> Or EIP-1 should attempt to describe the AllCoreDevs process around Core EIPs, using the same terminology that core devs use. I’d prefer the latter, which is to write a descriptive document, i.e. describe the group’s current behavior. The former requires forcing a group to change their current behavior (writing a document that prescribes new behavior), which is unlikely to be successful.

Yep, totally agree: describe the behaviour and tweak it over time – so there is a bit of push and pull.

So, ideally for Core EIPs: Draft → Last Call → Accepted → Final

Where Accepted means “there are no technical issues and this will make it into *some* hardfork”. And inclusion in a hardfork is by adding an Accepted EIP to the Hardfork Meta EIP.

And that bar - of making it into a Hardfork – needs some outside the EIP work, like implementation in at least two major clients. Is that about right?

Personally, I’d also like to see changes to the Jello Paper / Yellow Paper made (or at least active PRs) before acceptance into a Hardfork Meta.

This does mean that we will continue to have lots and lots of Drafts. It means that Last Call becomes a point of forcing the issue of really reviewing if there are issues with a Core EIP.

---

**boris** (2019-02-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> he EIP process applies to Ethereum Classic, POA and other networks just as well as mainnet.

It does not.

Or rather, various networks already have their own process, like the Ethereum Classic ECIP process.

If other networks want to maintain compatibility, they *may* adopt or inherit this Ethereum main-net changes.

In practice, this is the year where many other networks are going to have to make some choices around following main-net. None of the other networks currently use anything other than the Jello Paper / Yellow Paper and related other Ethereum specs (devp2p, JSON-RPC, etc. etc.) as reference documents.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Accepted EIPs which are under development. (Idea stolen from Swift Evolution process).

This is the Hardfork Meta EIP – so it is within the EIP process but essentially informational. For Constantinople, there was a “tracking” Github page to track process of various clients.

I like the Hardfork Meta – means one less system to track.

I don’t think kicking CoreDevs out of the EIP process for some meta system makes any sense whatsoever.

---

**fulldecent** (2019-02-13):

EIP-1 should be prescriptive. *Something* should be prescriptive. Somebody has to lead.

Here is a simpler diagram:

```
{ Ideas } --> [ Go through EIP process ] --> [ Implement with EF core devs ]
                                         \-> [ Implement with Ethereum Classic ]
                                         \-> [ Implement with other stuff ]
```

The EIP process should be separate from EF core devs.

---

**boris** (2019-02-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> The EIP process should be separate from EF core devs.

So far, pretty much everyone here disagrees?

Also, you keep saying “EF Core Devs” – which is not actually a thing. Pegasys and Parity (as examples) aren’t part of the EF.

Ethereum main-net Core Devs might be a better label – aka chain ID 1, network ID 1 (plus various test nets whose purpose is to test releases before main-net).

And as I pointed out earlier, Ethereum Classic does not follow / acknowledge the EIP process, they have an ECIP process of their own, which is different.

In any case – as [@cdetrio](/u/cdetrio) said, aligning README and EIP-1 *and* actual process to date is a good thing. I’ll put this on my backlog to roll a PR. And, would be great to discuss live in Paris.

---

**fulldecent** (2019-02-13):

There is an entity that owns the Ethereum trademark, and they are the ones that also recommend client upgrades. This is the entity I’m talking about. Right now it is not interesting to distinguish core devs/EF. But if one day if a hardfork fails (i.e. the EF-supported version has lower token value than the other fork) then this becomes very interesting quickly.

Please read up on Pirapira, this is a great case study on why having EIP editors make decisions is a bad idea. This motivates the current EIP-1 – the publication and the commitment to implement are separate.

---

**ajsutton** (2019-02-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Do CoreDevs need to meet in person regularly?

In person meetings are very exclusive - you need significant funding to be able to travel around the world to get to them all and people with families or other “at home” commitments will find it very hard to attend. Recording or streaming of them also tends to be fairly ineffective (ok for lecture style talks, not so much for break out groups).

I think it would be a real shame to make in-person meetings a regular or formal part of our processes. That doesn’t mean banning them or that they won’t be a good thing to organise sometimes, just that as much as possible, the routine process should allow everyone to contribute from distributed regions and time zones.

---

**boris** (2019-02-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajsutton/48/1102_2.png) ajsutton:

> In person meetings are very exclusive - you need significant funding to be able to travel around the world to get to them all and people with families or other “at home” commitments will find it very hard to attend. Recording or streaming of them also tends to be fairly ineffective (ok for lecture style talks, not so much for break out groups).

I completely agree! Last year all the in-person meetings were semi-private, invite only, and organized relatively last minute.

The Stanford meeting was really only finalized 3 or 4 weeks beforehand and wasn’t widely publicized.

So: rather than last minute, ad hoc in person meetings — I’m proposing planning further ahead with a minimum of 8 weeks lead time to keep travel premiums to a minimum.

---

**expede** (2019-02-15):

I agree that these meetings should be as accessible as possible ![:100:](https://ethereum-magicians.org/images/emoji/twitter/100.png?v=9)![:100:](https://ethereum-magicians.org/images/emoji/twitter/100.png?v=9)![:100:](https://ethereum-magicians.org/images/emoji/twitter/100.png?v=9)

Part of having more frequent meetings in more places in the world, it becomes more feasible to skip some and not have it be a tragedy. The idea is to have more opportunities to discuss, even in smaller region-specific groups. That said, final decisions should not be made at these meetings, rather they’re places for folks to get together and discuss ideas in a high-bandwidth, high-focus way. In person meetings will happen on or off the books, and the more transparent, open, frequent, and   they are the better IMO.

I would love to see this whole process made more remote friendly. Live streaming portions of Stanford was a step in the right direction, but it would be good to find a way to dial folks in (hard, but we’re a community that prides itself on solving hard problems!)

---

**boris** (2019-03-01):

This came up in the CoreDevs call this morning.

It is not sustainable, as [@vbuterin](/u/vbuterin) pointed out, to just fly to Australia for 20 hours, especially with not a lot of notice.

[@expede](/u/expede) and I will be in Berlin in mid-April can help organize an ETH1x CoreDev meeting – state rent, eWASM on ETH1x vs ETH2, and whatever other topics are useful to discuss and have people there for it.

I am proposing the week of April 15th.

---

**timbeiko** (2019-03-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cdetrio/48/482_2.png) cdetrio:

> The process as described there conflicts with the definitions of the terms stated on the README, and with the actual process of getting EIPs adopted. Here’s the terms on the README (full disclosure: I wrote these):
>
>
>
> Draft - an EIP that is open for consideration.
> Accepted - an EIP that is planned for immediate adoption, i.e. expected to be included in the next hard fork (for Core/Consensus layer EIPs).

So there are two definitions of `Accepted` for Core EIPs now:

1. The one stated in EIP-1. Accepted only means the Core EIP went through a two week “last call” phase before its status was upgraded to Accepted.
2. The one stated in the readme. Core EIPs are updated from Draft to Accepted after AllCoreDevs reach provisional agreement (by rough consensus) to schedule it for adoption in the next fork.

Also in EIP-1:

> Accepted (Core EIPs only) – This EIP is in the hands of the Ethereum client developers. Their process for deciding whether to encode it into their clients as part of a hard fork is not part of the EIP process.

I’ve submitted a small PR to EIP-1 to make this more consistent. https://github.com/ethereum/EIPs/pull/1858/files


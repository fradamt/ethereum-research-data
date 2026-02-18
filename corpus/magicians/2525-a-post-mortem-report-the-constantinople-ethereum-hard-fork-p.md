---
source: magicians
topic_id: 2525
title: "A Post Mortem Report: The Constantinople Ethereum Hard Fork Postponement"
author: boris
date: "2019-01-25"
category: Magicians > Process Improvement
tags: [hardfork, ethereum-cat-herders, constantinople]
url: https://ethereum-magicians.org/t/a-post-mortem-report-the-constantinople-ethereum-hard-fork-postponement/2525
views: 1943
likes: 10
posts_count: 5
---

# A Post Mortem Report: The Constantinople Ethereum Hard Fork Postponement

https://medium.com/ethereum-cat-herders/a-post-mortem-report-the-constantinople-ethereum-hard-fork-postponement-dd780d7ae63d

Bringing in this article so that we can have a discussion around it that isn’t trapped on Twitter or Medium.

## Replies

**boris** (2019-01-25):

One of the things I noticed was that 1052 and 1014 never went past Draft (so didn’t go through Last Call), and a bunch of us (me, [@axic](/u/axic), [@5chdn](/u/5chdn)) were pointing this out and at least trying to get them set as Final / Accepted in the weeks leading up to the scheduled hard fork date.

This isn’t related to any of the issues around postponing the fork or the 1283 EIP (which did follow process), but it is an example of how we should track these sorts of things and actually follow process.

It seemed hard to get the attention of EIP editors (no reviews, no comments) on what was a basic administrative clean up (setting status on EIPs that were scheduled to be included).

There are two “tracking” issues in the EIP repo around this with more discussion, filed by [@fulldecent](/u/fulldecent).



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1699)












####



        opened 02:55PM - 15 Jan 19 UTC



          closed 01:52AM - 18 May 19 UTC



        [![](https://avatars.githubusercontent.com/u/382183?v=4)
          fulldecent](https://github.com/fulldecent)










[EIP-1052](https://eips.ethereum.org/EIPS/eip-1052) is currently listed as draft[…]() status, however according to announcement from @Souptacular at https://blog.ethereum.org/2019/01/11/ethereum-constantinople-upgrade-announcement/ the latest EF version of clients will support this hard fork on block 7,080,000.

@Arachnid @chfast please use the EIP workflow process outlined in EIP-1.














      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1698)












####



        opened 02:52PM - 15 Jan 19 UTC



          closed 08:13PM - 04 Dec 21 UTC



        [![](https://avatars.githubusercontent.com/u/382183?v=4)
          fulldecent](https://github.com/fulldecent)





          stale







[EIP-1014](https://eips.ethereum.org/EIPS/eip-1014) is currently listed as draft[…]() status, however according to announcement from @Souptacular at https://blog.ethereum.org/2019/01/11/ethereum-constantinople-upgrade-announcement/ the latest EF version of clients will support this hard fork on block 7,080,000.

@vbuterin please use the EIP workflow process outlined in EIP-1.












Do we need more EIP editors to help with these admin tasks? How can we help?

---

**fubuloubu** (2019-01-26):

Some of the big takeaways are about overall process improvement, and failure to adhere to the listing process. I drafted a process improvement based on some FEM threads in this PR:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/1725)














####


      `master` ← `fubuloubu:patch-1`




          opened 12:18AM - 26 Jan 19 UTC



          [![](https://avatars.githubusercontent.com/u/3859395?v=4)
            fubuloubu](https://github.com/fubuloubu)



          [+10
            -7](https://github.com/ethereum/EIPs/pull/1725/files)







This PR adds a "Key Stakeholder Review" process that all PRs go through, after a[…](https://github.com/ethereum/EIPs/pull/1725) Draft is considered ready to Review, and prior to it entering Last Call (aka "public request for comment").

In the [post-mortem](https://medium.com/ethereum-cat-herders/a-post-mortem-report-the-constantinople-ethereum-hard-fork-postponement-dd780d7ae63d) for the aborted Constantinople fork that was set to occur on Jan 16, 2019, it was recommended to:
> Create a more formalized process for reviewing and analyzing EIPs

This process change suggests "substantial internal review by relevant stakeholder groups" occur before a suggested change is brought to the wider community for final discovery of any issues with the proposal. During Draft, stakeholder groups are suggested by EIP editors and anyone else participating in the conversation. The list of stakeholder groups is TBD, but should be compiled from active discussion groups focused along a particular topic that meets on a regular basis such as FEM Rings. When moving from Draft to Review, the editor will contact and record meeting dates where the EIP is set to be discussed (if those stakeholder groups have not done so already).

During Review, stakeholder groups will discuss and provide feedback from that discussion, as well as the consensus recommendation of the group. When all groups have given their feedback, and the feedback is a GO, it will move to Last Call to solicit any final feedback the community might have. If a group chooses not to give feedback (or feels like they don't need to), they can leave "no comment". If a group forgets to or chooses not to give feedback, we can discuss what happens in that circumstance.

---

Stakeholder Group Requirements:
- a stakeholder group should have a clear summary of what types of issues they review
- a stakeholder group should have a regularly scheduled meeting, as well as participation information
- a stakeholder group should ideally have a main point of contact

This information should be displayed publicly so that community members are aware these groups exist (and can join them!). These groups should also be made available as tags, so that relevant stakeholders can easily filter on items with their particular tag in the right status for discovery in case the editor forgets to contact them.

---

The primary motivation behind this change is to ensure that a more focused review occurs on all EIPs, in order to solicit the most amount of feedback before bringing it to a Last Call review. This will prevent substantial wasted discussion or a lack of review from relying only on a general, public review (which may not occur to the level of risk present in the proposal).

Some relevant background material:
* https://ethereum-magicians.org/t/decentralizing-eip-workflow/1525/7
* https://ethereum-magicians.org/t/proposal-add-ring-tags-to-eips-solicit-comments-from-ring-s/1592
* https://github.com/ethereum/EIPs/pull/956
* https://github.com/ethereum/EIPs/pull/1100
* https://medium.com/ethereum-cat-herders/a-post-mortem-report-the-constantinople-ethereum-hard-fork-postponement-dd780d7ae63d
* https://github.com/trailofbits/publications/blob/master/reviews/EIP-1283.pdf












---

Some more links about EIP process improvement suggestions:

- Proposing a revised process for handling of EIP drafts by Arachnid · Pull Request #956 · ethereum/EIPs · GitHub
- Decentralizing EIP workflow - #7 by Ethernian
- Proposal: Add Ring tags to EIPs; solicit comments from Ring(s)
- https://github.com/ethereum/EIPs/pull/1100
- publications/reviews/EIP-1283.pdf at master · trailofbits/publications · GitHub

---

**fulldecent** (2019-01-26):

Thank you very much for recognizing this. ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=9)

I have worked hard on getting the two-week process adopted (this was part of getting ERC-721 approved) and I believe it has benefitted the community for the ERCs process. It certainly makes it easier for me to find which EIPs I want to review! At the time this was really a big change and risked much criticism so again I appreciate your kind words.

However this process also applies to consensus-changing EIPs and it was not followed this time.

I believe the issue is that the attitude of EF is /much/ too centralized. They prefer to push their own software changes on the world by announcing on their own channels, rather than using a mildly community-based process like the EIP two-week review.

(EDIT: Maybe “prefer” was too strong there, maybe not everyone knows about EIP-1 changes yet…)

---

**boris** (2019-01-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> I believe the issue is that the attitude of EF is /much/ too centralized.

I don’t really see the EF as being in charge. There are humans who work for the EF involved, but at this point we are in the process of having many independent clients.

I see lack of consistency by editors / maintainers — if there is open-need to GitHub labels, more maintainers, and so on — I think the process can improve.

P.S. pretty please thumbs up my RSS changes or give me feedbac.


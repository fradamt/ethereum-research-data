---
source: magicians
topic_id: 11995
title: "Discussion of Guideline for advancing EIP status: A Straw-man Proposal"
author: xinbenlv
date: "2022-12-02"
category: Magicians > Process Improvement
tags: [eip-process]
url: https://ethereum-magicians.org/t/discussion-of-guideline-for-advancing-eip-status-a-straw-man-proposal/11995
views: 2392
likes: 18
posts_count: 19
---

# Discussion of Guideline for advancing EIP status: A Straw-man Proposal

Currently in EIP-1, except of Core EIPs there is no much mentioning criteria for allowing publication of a draft EIP or advancing an EIP’s status to final. This raises concern from some EIP contributors about quality, worthiness and whether there are sufficient interest or whether sufficient level of consensus has been reached.

In the interest of starting a discussion, I am creating this (probably dumb and full of flaws) proposal for criteria for advancing statuses of an EIP. Please see it as a straw-man and provide your feedback.

## Standard Tracks

| Category | Draft | Review | Last Call | Final |
| --- | --- | --- | --- | --- |
| Core | Auto-merge | FEM discussion or 1st ref impl | Agreed on ACD & 2+ indenpendent impls | wait 14 days |
| Network | Auto-merge | FEM discussion or 1st ref impl | 2+ independent impls | wait 14 days |
| Interface | Auto-merge | FEM discussion or 1st ref impl | 3+ independent impls | wait 14 days |
| ERC | Auto-merge | FEM discussion and 1st ref impl | 3+ independent impls | wait 14 days |

## Non-standard Tracks

| Category | Draft | Review | Last Call | Final |
| --- | --- | --- | --- | --- |
| Meta (binding) |  | FEM discussion | “rough consensus” (to be clarified) | wait 60 days |
| Informational(non-binding) | Auto-merge | Author discretion | FEM discussion | wait 60 days |

*Note: this was previously briefly discussed on EIP Editor Meeting #70 and another [relevant thread](https://ethereum-magicians.org/t/informational-eip-author-handbook/11754/7)*

## Replies

**abcoathup** (2022-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> FEM discussion or 1st ref impl

Given that a link to FEM discussion is a requirement for auto-merge, this metric needs to be higher.  e.g. discussion on the draft EIP from 2 independent projects.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> FEM discussion and 1st ref impl

For ERC I feel that a minimum of 2 implementations is required to get to review.  If a developing ERC only has one project supporting it then I don’t see it getting much decent input at the review stage.

---

**xinbenlv** (2022-12-06):

Haha thank you for feedback. [@abcoathup](/u/abcoathup)

> Given that a link to FEM discussion is a requirement for auto-merge

In the above table, `FEM discussion` is not a requirement for `auto-merge`. What I meant to say is that for merging an EIP with `Draft` status, auto-merge means there is no particular Editor review needed.

> For ERC I feel that a minimum of 2 implementations is required to get to review. If a developing ERC only has one project supporting it then I don’t see it getting much decent input at the review stage.

I can totally resonate with your sentiment. There is a spectrum of people’s preference. Some expressed to me that two ref-impls as a criteria for advancing to “Final” are too high a bar. Some (You [@abcoathup](/u/abcoathup) for example) even think this requirement is too low a bar even for “Last Call” and hope to make it a bar as the bar for advancing to “Review”. Love to hear more people what they think.

---

**Weiji** (2022-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> 1st ref impl

As it does not stress *independent* for **Review**, I guess the ref impl from the proposer also counts?

---

**SamWilsn** (2022-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> endorsed by >=2/3 of editors when has disagreements

We operate using rough consensus, and I don’t think setting a merge ratio is in line with that.

---

**xinbenlv** (2022-12-06):

That would work too. Shall I just put “rough consensus” down or is there a better way to describe it? How about “full consensus”?

The goal is to let reader understand what it means as a requirement by just reading the text

---

**xinbenlv** (2022-12-07):

Here are a few evidences that supports having some level of adoptions / (reference implementations deployed) as a criteria

[@frangio](/u/frangio) wrote:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png)
    [EIP-4834: Hierarchical Domains Standard](https://ethereum-magicians.org/t/eip-4834-hierarchical-domains-standard/8388/10) [EIPs](/c/eips/5)



> Nothing in particular, my point is rather that I think the interface should be tried “in the field” quite a bit before settling on a final specification, because that could surface issues in it. I mean things like starting to build the various applications, tooling, and libraries around it. I don’t know if that has been done in this case.

[@fulldecent](/u/fulldecent) wrote in [his article](https://blog.phor.net/2022/09/30/What-kinds-of-things-should-be-standardized.html)

> A standard only deserves to be written if multiple people adhere to it and people depend on its surface area.

---

**kdenhartog** (2022-12-09):

Thank you for starting this discussion [@xinbenlv](/u/xinbenlv) as it’s an important one that I’ve seen come up a few times now.

I need to sit down and write out a longer post for this, but I think two places to consider for this are the following:

IETF’s process: [IETF | The IETF process: an informal guide](https://www.ietf.org/standards/process/informal/)

Old W3C process: [7 W3C Recommendation Track Process](https://www.w3.org/2004/02/Process-20040205/tr.html)

New W3C process: [W3C Process Document](https://www.w3.org/2021/Process-20211102/)

I don’t think either of these are cut and dry drop in replacements for the governance here, but I think looking to what others have done and understanding *why* they’ve taken things that way will help to inform the direction we as a community wish to go.

One thing worth noting for both of these process first off is timelines. In both cases, when someone undertakes the process of producing a standard in either of these places I’d expect it to take roughly a year at least to go from first draft to completion. Usually it’s a multiyear effort though which can take 2 or 3 years. In fact, I’ve seen some take longer and it’s only because WG charters were set to expire that a first iteration of a standard was shipped.

So with that said, I think a good thing for us to set as a guiding consideration here is “How long do we expect it to take from an EIP first drafted to an EIP being shipped and multiple implementations are relying upon it?”

In my opinion, I think a good answer to this is between 6 to 18 months depending on the piece of work you want to ship and how many parties are working on this.

---

**xinbenlv** (2022-12-09):

[@kdenhartog](/u/kdenhartog)

Thank you for providing the IETF, W3C process guide. I would look into them.

We discussed last time, and we generally feel that mandating a time is not the best way to address the merit or maturity of a pending EIP. Thus, I aim for more concrete criteria, e.g. independent reference implementations. But I am open to be convinced and could totally understand if there might be some very good reason for a timeline requirement.

---

**kdenhartog** (2022-12-14):

I agree that we need something better than a timeline, so number of independent implementations seems to be the key measurement of a good spec to me as well. The main reason for a timeline is to prevent specs from becoming bloated or taking forever to ship because new people keep joining and requesting additional changes or adding additional requirements late in the process which can slow consensus down.

A really good talk I’ve seen on someone who chaired the OAuth WG covers some of the reasons for why this happens via talking about the various people who contribute to these types of processes here: [CIS 2016- Thursday, June 9- So You Want to Run a Standards Group- Justin Richer - YouTube](https://www.youtube.com/watch?v=Y1_-xDk7ZpA)

It’s worth pointing out though his point at 19:54 though which is that “Standards development doesn’t run out of time or money, but people in the WG run out of patience”. There’s a lot of wisdom in this statement because it suggests that if we don’t set arbitrary deadlines then we’re not likely to actually ship things and call something done. I’ve seen arbitrary deadlines work very well as a forcing function for creating consensus since most people would rather see something ship than nothing at all after they’ve spent a lot of time contributing to it’s development.

---

**xinbenlv** (2022-12-14):

In [EIPIP Meeting 71](https://github.com/ethereum-cat-herders/EIPIP/issues/198)

- @gcolvin expressed in favor of having some implementations before ERC EIPs goes to Final
- @poojaranjan expressed in favor of adding lower-bound time (30days) to advance to Final at least for Meta EIP
- @SamWilsn @matt (lightclient) expressed objection to use implementations as a requirement for finalizing ERCs worrying it will add more hurdles for EIPs to get to final.

[@SamWilsn](/u/samwilsn) also expressed that Editors might ask about worthiness of an EIP but “Non-of these editors will block” an EIP to advance to EIP even only author subjectively think this EIP is worthy.

Let me know if the notes are inaccurate

---

**xinbenlv** (2022-12-14):

[@kdenhartog](/u/kdenhartog)

If I understand you correctly, in your description of “timeline” you actually mean upper-bound of time allowed to advance to next status, right?

---

**kdenhartog** (2022-12-14):

Yup, that’s a good way to describe it. If people operate in a faster time frame that’s a good indicator normally that things are non-controversial assuming there’s actually multiple implementations working on it.

Probably another thing that would be important here is that when EIPs hit particular milestones that there’s also a broad method of notifying people (basically people who don’t watch the EIP repo) that EIPs are hitting particular milestones and have ways to address objections during this process. E.g. Brave and Metamask are both on record for objecting to EIP-5749 (mine in [the PR](https://github.com/ethereum/EIPs/pull/6018#pullrequestreview-1192283477) and [FEM discussion](https://ethereum-magicians.org/t/eip-5749-the-window-evmproviders-object/11195/23) and Metamasks in the [FEM discussion](https://ethereum-magicians.org/t/eip-5749-the-window-evmproviders-object/11195/24) ) but the EIP was still advanced forward anyways. That seems like a failure of the process if two wallets are actively against supporting an EIP directly related to their implementations, but the process doesn’t have any way to establish consensus.

Simply put, if wallets aren’t supporting this EIP it’s effectively DoA even if it does hit final. Especially if Metamask isn’t going to support it given their userbase. Furthermore, by publishing this EIP it legitimizes it in a way that creates more web compatibility issues for DApps like Opensea which may now have to support an additional property if they want their users to be able to use MEW wallet. My goal is to avoid these types of images showing up on DApps.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/4/4c2f66c17886443be516ce1bc6474d4e4adf8624_2_690x386.png)image1269×710 37.7 KB](https://ethereum-magicians.org/uploads/default/4c2f66c17886443be516ce1bc6474d4e4adf8624)

---

**xinbenlv** (2023-03-22):

Noted: [EIPIP Meeting 77 · Issue #219 · ethcatherders/EIPIP · GitHub](https://github.com/ethereum-cat-herders/EIPIP/issues/219#issuecomment-1478854956)

Copied here

---

> Topic: can we also add this to agenda: Discussion of Guideline for advancing EIP status: A Straw-man Proposal
>
>
> Update: meeting brief notes about this
>
>
> Generally in favor of creating a guideline (but not a criteria) for EIP to advance status
> Generally in favor of seeing implementations for last call and final as a signal for community interest
> Mentioned that  having multiple implementations might not sufficiently demonstrate independence between them but lacking implementations could be seen as a signal of lack of community interest
>
>
> @xinbenlv @matt @SamWilsn participated in discussion. Correct me if my understanding is wrong.

---

**xinbenlv** (2023-06-13):

Reposting some feedback from discord

@edson.eth at Discord [Discord](https://discord.com/channels/916516304972824576/916713912970412103/1117633407854325801)

> Hi. Going through the previous EIPIP call. When I was doing outreach for EIPIP in 2020, one of the biggest requests from EIP editors and authors up to that point was requiring one reference implementation. I agree with the desire to have 1 reference implementation as a requirement before moving to final for EIPs and ERCs.
> Reference implementation plus passing test cases is ideal

[@SamWilsn](/u/samwilsn)

> @edson.eth How do we differentiate between a compliant reference implementation and a non-compliant one?
> Can an author add a skeleton implementation where every function reverts? Where is the line drawn? This is especially relevant for extension EIPs, like all the ERC-721 extentions. Does the author need to implement all of ERC-721 in their reference implementation?
> Once the line is drawn, how do we evaluate whether a particular reference implementation meets it? Do editors need to become smart contract auditors in addition to our regular duties?
> Asking EIP editors to verify that tests pass is also a huge request, and would probably require adding a ton of scaffolding to the EIPs repository (eg. package-lock.json) for every single ERC.
>
>
>
> All that to say: I don’t believe we should put this burden on EIP editors.

---

**xinbenlv** (2023-06-13):

Thanks for your comment. @edson.eth, [@SamWilsn](/u/samwilsn)

For @edson

I appreciate you sharing your views for supporting a 1 reference implement as requirement. I am very much with you on that.

For [@SamWilsn](/u/samwilsn)

I hear your concern that your worry there is too much burden for EIP Editor to verify validity of reference implementation. I feel this can be done with

1. basic trust for authors for their good intention to do a good contribution, and,
2. by peer reviewer to validate it in the long run.

If we make it a objective goal for providing one reference implementation, peer reviewer will get a more clear idea of what we ask their contribution about.

---

**gcolvin** (2023-06-16):

Yes, this is what peer review i for.

---

**gcolvin** (2023-06-16):

The Last Call is supposed to be where (lack of) consensus is established.  If Brave and Metamask were opposed they needed to show up on FEM then (if not sooner) to block consensus.  But in general it’s not easy keeping up, so I’m not surprised they missed it.

---

**xinbenlv** (2023-12-23):

Thanks Greg.

---

Friends, I am thinking of turning this into a Informational ERC, if none raise a concern


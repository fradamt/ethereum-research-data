---
source: magicians
topic_id: 12065
title: How do we address editors being overworked with a better governance method and what does it look like?
author: kdenhartog
date: "2022-12-09"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/how-do-we-address-editors-being-overworked-with-a-better-governance-method-and-what-does-it-look-like/12065
views: 2329
likes: 21
posts_count: 23
---

# How do we address editors being overworked with a better governance method and what does it look like?

There’s been some recent discussions on the Ethereum Cat Herders discord server about what is a more scalable method for governing and enforcing the EIP process. Right now there’s two majors concerns that seem like they need to be addressed:

1. Editors are having to help juggle and steward many different EIPs through the process
2. The quality of EIPs is largely dependent upon the author because EIP editors can’t be experts in all different topics that are discussed

For this reason, it seems like we’re encountering some boundaries of the current model of governance where we can efficiently ship standards that lead to rough consensus and running, interoperable code. I’d like to start the discussion of what might a new process look like to scale governance of the EIP process.

## Replies

**abcoathup** (2022-12-09):

- Auto-merge EIPs as draft once they pass validation, including issuing an EIP number.
- Split off ERCs.
- Sell unused EIP #s to fund EIP editors

---

**jpitts** (2022-12-09):

[@kdenhartog](/u/kdenhartog), thank you for bringing this up, I hope that we can get some helpful comments and ideas going in this thread.

I don’t want to weigh in too strongly before understanding the problem better, and also understanding how other communities (IETF, W3C, etc.) deal with stewarding proposals.

What do you think are the key causes of these challenges?

The editors do seem to lack the operational support and ability to recruit help vs. other groups who are a part of the larger process. And it also seems as if there has not been enough editors to handle the workload, particularly as there are EIPs and ERCs being submitted from so many different topics / technical areas.

---

**kdenhartog** (2022-12-14):

For me the key challenges I think editors face are having to wear multiple hats as domain expert for specific classes of EIPs, acting as enforcement of the process, acting as pseudo-governance of the process, and also actual editorial review (e.g. missed spelled a work etc).

To me each of these tasks are big enough these days that they could be separated out at this point. Especially for volunteers who often time have secondary work outside of this.

Even just splitting off the need to be a domain expert and editorial review from the enforcement/governance of process would be helpful IMO. This could be done via the usage of a process to form working groups (WG) is what I’m thinking and as a part of this “chairs” and “editors” of the WG can exist to help steward specific proposals through the EIP process.

At face value this sounds simple, but there’s likely a lot of things that would still need to be addressed if there’s buy in to go in this direction.

For example,

1. how do we know if there’s enough interest to establish a WG?
2. How do we go about selecting people to run these WG?
3. What expertise do they need to do so?
4. What do we need to do to bring the appropriate people into these WGs to better establish consensus?

Additionally, I think it would be useful to consider how this might affect this other thread [@xinbenlv](/u/xinbenlv) has proposed here: [Discussion of Criteria for advancing EIP status: A Straw-man Proposal - #8 by kdenhartog](https://ethereum-magicians.org/t/discussion-of-criteria-for-advancing-eip-status-a-straw-man-proposal/11995/8)

Just some thoughts to keep the discussion moving here

---

**sbacha** (2022-12-22):

Why not help govern the process by making two lanes of proposals?

> People with successful EIP
> Lane one: EIPs that have had previous EIP Authors vouching for the new author or they themselves are an author of the EIP in waiting.

> People without successful EIP
> Lane Two: pending EIP authors must wait a min. of x amount of days before acceptance such that their is sufficient time for the res publica to be informed about this. Additionally have them submit to some mandatory event or process. Eg attending one ACD (not necessarily to speak, etc) or even better having them implement some portion of their proposal (can be a toy implementation etc).

The idea being that the process itself filters out less serious proposals by imposing a min. fixed cost of time on their part that is commensurate with the scope of their EIP.

I think having previous author’s involvement for providing a reference will bring additional benefits as well.

Edit: Also this would mean making a list of EIP Process Status, i.e.:

Draft / Pre Qualify

Pending Consideration,

Accepted but not Implemented,

Implemented,

Obsolete

These would be editor status, a sort of EIP meta categories

---

**kdenhartog** (2023-01-10):

[@xinbenlv](/u/xinbenlv) and I were talking about this discussion yesterday. We were curious if anyone has considered how to move the EIP process into an area directorate at the IETF? This seems like it would allow us to adopt their governance and processes so that the community can remain focused on publishing, editing, and standardizing specs.

Thoughts?

---

**Pandapip1** (2023-01-11):

I would be in favor of that idea if anybody has the requisite connections. My only concern would be that the EIPs would have to be renumbered if they are to be converted to RFCs.

---

**xinbenlv** (2023-01-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> We were curious if anyone has considered how to move the EIP process into an area directorate at the IETF?

It was a great chat with [@kdenhartog](/u/kdenhartog). We shared a lot of thoughts and views. Given EIP has earned a lot adoption and respect while the latest activities on drafting and reviewing EIPs seems encounter a few challenges, it’s good to start discussion about how we could borrow the wisdoms from various mature standard body. I think we can try to learn from IETF/W3C and a few others. Whether to “move into” is an open questions and I don’t have a good answer yet. I recognize the difference between Web3 space vs traditional web space, and the role of EIP for Ethereum rather than IETF/W3C for general web. Also the legitimacy of  a standard body mainly comes from the adopting stakeholders. And the main stakeholders (browsers, email client, websites, etc) of IETF/W3C and other standard body are quite different from EIP’s adopting stakeholders (Web3 wallet, Smart Contract etc). Therefore we probably want to sort out a better way to identify stakeholders and invite them.

Let’s chat a bit more.

[@kdenhartog](/u/kdenhartog) and I will start some Zoom / Discord voice chat soon. And if anyone on this thread of FEM are interested in participating, please let us know by commenting or DM us in FEM. We are happy to add you to schedule together.

---

**sbacha** (2023-01-12):

Since my previous comment seems to be too radical, may I suggest a modest one: have you tried paying them?

Additionally if you trace the lineage of the EIP process, it originates from Python/Gentoo — they are narrow in scope wrt the project itself. IETFs only interesting aspect is its trust structure for its own incorporation, which isn’t relevant considering EIPs are in the public domain (I think this is potentially more worth reconsidering).

---

**Pandapip1** (2023-01-12):

This has in fact been considered, and would certainly attract more editors. The question that remains is: Where the funds would come from?

---

**kdenhartog** (2023-01-17):

I didn’t think this was radical enough actually. Sorry I didn’t respond to this originally. I did spend a bit of time thinking about it. One of the reasons I wasn’t a fan of that suggestion was it creates a larger amount of bureaucracy for authors without really helping take the harder more contentious decisions off the editors plate in my opinion.

My concern is that the path we’re taking is creating a committee of benevolent dictators unintentionally that require consensus to make decisions. I see that as the primary problem that we need to be splitting up here is that all final decision making power shouldn’t be centralized to a small core group of editors. Instead, it’s my opinion that the decisions should be split out to prevent issues from arising as the work is scaled and limit controversy centralizing around a small number of important decision makers made.

If you look at other standards processes there’s a reason the governance processes always seem so complex. It’s because the complexity emerges from trying to establish checks and balances to each roles power within the process.

---

**Pandapip1** (2023-01-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> My concern is that the path we’re taking is creating a committee of benevolent dictators unintentionally that require consensus to make decisions.

This has always been the case. I agree that this could use fixing.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> it’s my opinion that the decisions should be split out to prevent issues from arising as the work is scaled and limit controversy centralizing around a small number of important decision makers made.

I don’t care about being controversial. I either convince everyone and it becomes the consensus, or am outvoted and the rules changed.

My actual concern is that a small group of decision-makers, such as we have, simply doesn’t have enough bandwidth to keep up.

---

**uwu_miche** (2023-01-18):

Hi everyone!

I want to ask this question - how do successful self-governing communities work?

Why don’t we take some time to study in history, the best self-governing examples, and take it from there?

Also - are there any editors who are open to talking about this? Would be great to hear from the editors themselves what’s going on and what their thoughts on making the process more decentralized.

It looks like there is a proposal for how to “become” an EIP editor- but looks like you just have to make a PR and then get approved by the list of editors.

But how do you get approved by the editors? LOL



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5069)





###



Handy reference for EIP editors and those who want to become one

---

**Pandapip1** (2023-01-18):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/u/e56c9b/48.png) uwu_miche:

> Also - are there any editors who are open to talking about this? Would be great to hear from the editors themselves what’s going on and what their thoughts on making the process more decentralized.

I am an editor, and also one of the authors of the EIP you linked ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

The process is as simple as the EIP describes. If enough editors say yes, then the PR gets merged and you are an editor. There are technically no requirements to become an editor (which is why I am still annoyed that [@xinbenlv](/u/xinbenlv) hasn’t been allowed to become an editor yet).

---

**xinbenlv** (2023-01-18):

Thanks for the kind words [@Pandapip1](/u/pandapip1) . I am here to contribute to open standards, in any way our community needs. Appreciate you for your support.

---

**sbacha** (2023-02-06):

Why cant the foundation provide a grant? Can it not offer ETH to stake to provide for self funding for this? It has done so with the client teams.

I think maybe a better volunteer application process would be beneficial. As it stands its kinda opaque and could benefit potentially by having open interviews during a special office hours session quarterly maybe?

---

**TimDaub** (2023-02-06):

Having had conflicts with EIP editors, I think one problem is also that their job is to criticize a submitter’s proposal, and while this makes it eventually better (I appreciate all EIP editor’s critique), this giving of feedback will inevitably lead to feelings being hurt too. Do people see this as a real problem, or am I off here?

A tangential idea to improve the happiness of editors (albeit making their job less interesting):

We once practiced Holacracy, and one key tenant was that mediators must always focus on executing the process and not voicing their subject-matter opinion. E.g., I had EIP editor fights over ideas I brought to fruition as EIPs, but these could have been avoided if the EIP editor had strictly reviewed for form and not the proposal’s idea(ls).

In that way, an EIP editor would only help EIP submitters over the finish line towards getting things merged on GitHub (by criticizing form, e.g., “You must add a security section,” "you must use the form “ERC-XXX”), but all subject-matter critical feedback (e.g., “you shouldn’t propose this standard because it is immoral”) would actually come from other Ethereum community members. Dunno, just an idea.

---

**kdenhartog** (2023-02-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> Why cant the foundation provide a grant? Can it not offer ETH to stake to provide for self funding for this? It has done so with the client teams.

I generally think we will need to get to that point as well. Something interesting about the W3C is that they have a small team of full time staff and then for the rest of their team, they’ve got [fellows](https://www.w3.org/Consortium/Recruitment/Fellows#past) which are paid by W3C members (who are their employers) but spend 80% of their time just doing W3C related work.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> I think maybe a better volunteer application process would be beneficial. As it stands its kinda opaque and could benefit potentially by having open interviews during a special office hours session quarterly maybe?

For me I don’t think the answer is that we need more editors, but rather that we should distribute their responsibilities to more people. From a governance perspective this is also useful because it decentralizes the power placed in any one role within the standardization process.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> Having had conflicts with EIP editors, I think one problem is also that their job is to criticize a submitter’s proposal, and while this makes it eventually better (I appreciate all EIP editor’s critique), this giving of feedback will inevitably lead to feelings being hurt too. Do people see this as a real problem, or am I off here?

Personally, I think feedback is a feature not a bug (which I’d guess is your believe as well [@TimDaub](/u/timdaub)), but with that said I think the only real feedback within the process which has the power to affect the standard is the editors which is more of a bug than a feature. A standardization process is to meant to establish consensus, usually by way of controversy, and feedback is necessary to achieve that in my opinion. If there’s no one providing feedback then the specification probably isn’t well suited as a standard.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> We once practiced Holacracy, and one key tenant was that mediators must always focus on executing the process and not voicing their subject-matter opinion. E.g., I had EIP editor fights over ideas I brought to fruition as EIPs, but these could have been avoided if the EIP editor had strictly reviewed for form and not the proposal’s idea(ls).
>
>
> In that way, an EIP editor would only help EIP submitters over the finish line towards getting things merged on GitHub (by criticizing form, e.g., “You must add a security section,” "you must use the form “ERC-XXX”), but all subject-matter critical feedback (e.g., “you shouldn’t propose this standard because it is immoral”) would actually come from other Ethereum community members. Dunno, just an idea.

I agree this is a problem. While I understand that all of the EIP editors today have good intentions and operate in good faith we can all find ourselves at times tied to a particular idea, solution, or way of doing things. I know I’ve encountered this numerous times when working on standards.

With that said, I think it’s important for editors themselves to recognize which “hat they’re wearing” when providing feedback. It should be OK for them to provide subject-matter opinions and feedback, but it’s not OK to use their editor capabilities in order to block proposals from moving through the process. That is a conflict of interest and a corruption of the role and I believe should be grounds for removal if it becomes a repeated issue. Unfortunately, while that is ideal and the way it’s handled in other standards organizations we’re not there yet with the EIP process because we lack in contributions from others in the Ethereum community these days on many EIPs. This is either an indication that some things just aren’t ready to be standardized or that the process has pushed people away from contributing. I believe it’s actually a bit of both. For this reason, the lines can become very blurry when the editors are the only ones commenting and providing feedback on EIPs. In nearly all the cases I’ve seen they’re doing this out of best interest of the community and to help start the discussion with thoughtful feedback. I don’t believe it always used to be editors guiding the discussions and being lead contributors in feedback though. For example, look at the liveliness of discussion that occurred around [EIP-1098](https://github.com/ethereum/EIPs/pull/1098) with 25 different participants. Similarly there were some great discussions around EIP-1193 and I’m sure there was plenty round EIP-712.

This is all to say, I think that we’re at a point where it’s necessary for us to evaluate what’s the right way to split up the work that editors take on. Not only to help reduce the time and effort they have to spend in volunteering, but also because this will help get more people involved and decentralize the power to create a more robust process.

**Proposal**

In my opinion we should be splitting out the responsibilities into 3 separate roles. A WG to manage the governance process (EIP-1) and maintain the bots, a role I’m calling an “Area Director” which helps to establish whether a WG should be formed or a proposal should be tied into an already running WG, and a role which helps to manage a WG called a “WG chair” who’s there to maintain the WG and make sure work items and proposals are moving towards completion. We’d then also have EIP Authors which remain the people driving a proposal forward to completion.

With these new roles, I’d imagine the process for moving a proposal from draft to completion would look a bit like this.

1. Put forward a proposal to draw feedback and decide if it should be standards track or informational

preferably this step is actually done outside the EIP repository to increase the noise to signal ratio
2. it’s up to draft authors to gather enough attention to get a WG formed. This could be done via area directors helping to promote group on FEM or on twitter so they can determine if now is a good time to start the standards process for a particular item of work.
3. Things can sit in “idea” stage form indefinitely. These are essentially like internet drafts in IETF
4. Once the area director has determined a WG should be formed (or assigned a piece of work to a WG) then the idea is converted to the “draft” step and moved into a GH user (e-g EIP-Core or EIP-ERCs) focused on a particular area. It’s at this point that the iterative design process begins by forming a repository for the proposal, filing issues, and updating the spec. There should probably be re-occurring discussions or at least some way to separate feedback to make sure that all of the concerns are being addressed.
5. Once a draft is believed to be at a fairly stable state, it should enter a review period which should include a call for implementations and a test suite or reference implementation should be built ideally to make sure the spec is actually able to be implemented by multiple people and no interoperability concerns are left unaddressed.
6. Finally, once the authors, WG chair, and area director believe the spec is at a state where we’re close to consensus we can enter the “final call” period. At this point any last objections will be required to be lodged within a 2 week window and be addressed within a 4 week window from the point they’re addressed.
7. Once confirmed they’d be finalized and moved into the official EIP repository. At that point only errata can be filed to modify it which would need to be done via the WG that moved it forward (or a maintenance WG for that).

---

**kdenhartog** (2023-02-07):

Also for those wondering, this is basically how IETF does things [[1](https://www.ietf.org/standards/process/new-work/)][[2](https://www.ietf.org/standards/process/informal/)] but propsed in a way that adapts to the communities current ways of working while also trying to keep the  bureaucratic overhead of the process to a minimum.

---

**gcolvin** (2023-02-14):

To a large extent you are describing the way the EIP process and the Magicians were intended to work, (we had the IETF much in mind) and I’d be most inclined to build on that rather than start over.

Rings (so named in Berlin) were intended to function as working groups. Editors were to be concerned only with the form of a proposal, not its technical content, and much of that we try to automate with bots.  And the Magicians’ forums were established as a place for individuals and Rings to propose new ideas and review technical content.  And we already have a Draft → Review → Last Call process.

One big issue is that the self-organizing Rings never did get organized.  I’m not sure how to fix that.  But a start might be to insist that the authors of a proposal – especially ERCs – find one or two peers who are willing to edit the initial Draft and see it through to Review – if an author can’t do that there is likely not enough interest to bother.  The primary role of the Editors would be to approve the actual merges into the repo.

---

**SamWilsn** (2023-02-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> an EIP editor would only help EIP submitters over the finish line towards getting things merged on GitHub (by criticizing form, e.g., “You must add a security section,” "you must use the form “ERC-XXX”), but all subject-matter critical feedback (e.g., “you shouldn’t propose this standard because it is immoral”) would actually come from other Ethereum community members. Dunno, just an idea.

For the most part, I try to keep my “content based suggestions” off of pull requests and make it very clear that the suggestions do not affect whether I will approve their PR or not. The only subjective thing that editors should be reviewing, in my opinion at least, is whether or not a proposal should be an EIP at all.


*(2 more replies not shown)*

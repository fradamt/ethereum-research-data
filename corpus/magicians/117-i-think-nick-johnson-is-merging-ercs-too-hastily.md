---
source: magicians
topic_id: 117
title: I think Nick Johnson is merging ERCs too hastily
author: fulldecent
date: "2018-04-06"
category: Uncategorized
tags: [erc, eip-editors]
url: https://ethereum-magicians.org/t/i-think-nick-johnson-is-merging-ercs-too-hastily/117
views: 2968
likes: 20
posts_count: 13
---

# I think Nick Johnson is merging ERCs too hastily

The first ERCs were good and well thought out. I spent three months generating consensus for ERC-721. ERC-20 is clearly used everywhere. Next month a Michelangelo sculpture will sell with 721, CryptoKitties just raised another $12M. There are 3 new 721 applications launching on Rarebits each day (source Dallas Explore 721 meeting).

Now ERCs are getting merged as draft (same level as 721) constantly with minimal review.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/973)














####


      `master` ← `Arachnid:191`




          opened 12:41PM - 05 Apr 18 UTC



          [![](https://avatars.githubusercontent.com/u/17865?v=4)
            Arachnid](https://github.com/Arachnid)



          [+63
            -0](https://github.com/ethereum/EIPs/pull/973/files)







Replaces #191.














      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/906)














####


      `master` ← `jbaylina:eip820`




          opened 08:34AM - 27 Feb 18 UTC



          [![](https://avatars.githubusercontent.com/u/4180156?v=4)
            jbaylina](https://github.com/jbaylina)



          [+274
            -0](https://github.com/ethereum/EIPs/pull/906/files)







This is the PR discussed in #820
Currently, there is no open issues/conflicts […](https://github.com/ethereum/EIPs/pull/906)in this standard proposal.














      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/907)














####


      `master` ← `jbaylina:eip777`




          opened 08:56AM - 27 Feb 18 UTC



          [![](https://avatars.githubusercontent.com/u/4180156?v=4)
            jbaylina](https://github.com/jbaylina)



          [+649
            -0](https://github.com/ethereum/EIPs/pull/907/files)







Tjis is the PR discussed in #777

## Pending issues required for the standard […](https://github.com/ethereum/EIPs/pull/907)to be approved
- [ ] Approve [eip820](https://github.com/ethereum/EIPs/pull/906)
- [X] Decide if include `listOperators(address account) constant public returns(address[])` (Will not be implemented).
- [X] Decide if include a `revokeAllOperators(address account) public` (Will not be implemented)
- [ ] Approve












Also, EIPs with zero use cases or motivation are being accepted “just because I can” like this one:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/926)














####


      `master` ← `Arachnid:addressmetadata`




          opened 12:55PM - 12 Mar 18 UTC



          [![](https://avatars.githubusercontent.com/u/17865?v=4)
            Arachnid](https://github.com/Arachnid)



          [+73
            -0](https://github.com/ethereum/EIPs/pull/926/files)







This PR provides a proposal for an address metadata registry, of use in applicat[…](https://github.com/ethereum/EIPs/pull/926)ions such as ENS, distributed identity systems, and new token contract standards.

See https://github.com/ethereum/EIPs/pull/927 for an example use-case of this standard.












The current EIP-1 process “If the EIP collaborators approve … the EIP editor will … merge your pull request” is being skirted or ignored altogether.

---

I will note that the Immutability Enforcement Proposal was not merged even though it is technically just as valid as the other proposals and has more community support: https://github.com/ethereum/EIPs/pull/894

---

I believe if this trend continues then the relevance of EIP/ERC as a whole will be tested. And it will become vulnerable to a fork.

Ping: [@Arachnid](/u/arachnid)

## Replies

**Arachnid** (2018-04-06):

EIP editors don’t apply editorial judgement beyond a basic “is it syntactically correct and not obviously stupid” check.

Getting merged as a draft does not imply approval, and a draft is not an EIP, it’s a draft.

As I stated in today’s All Core Devs, I’m really trying to move to a situation where anyone wanting to submit a draft can get a permanent identifier as soon as possible; it reduces the tendency to treat PRs as persistent URLs, and helps ensure that drafts can all be found in the same place with stable URLs.

Edit to add: I’m sorry you had so much trouble getting 721 merged. The difficulty was because our process is broken - not because we want to make it really tough to get drafts merged.

---

**MicahZoltu** (2018-04-07):

I’m a fan of “get merged as draft ASAP”.

The issue with 894 I believe is that it doesn’t yet pass the “technically sound and grammatically correct” test.

1. “treat account holders differently” isn’t clear enough. The author obviously has a view of what that includes and doesn’t include but the average reader will not come to the same conclusion when reading the EIP (as can be seen in the EIP discussion).
2. The author insists on using a particular word (bailout) and redefining it to mean something that it doesn’t mean to a native English speaker.  This is a tactic for poisoning the well that isn’t conducive to technical discussion.
3. The changes shouldn’t be an EIP, they should be a PR against EIP-1.  @Arachnid may have more insight into what the intended process is for changing the process, but last I heard a PR against EIP-1 is that process.

If the author can fix these things then I think it should be merged, even though I also think it is not a good EIP for other non-technical reasons.

---

**Arachnid** (2018-04-07):

I’d say that 894 has not been merged for a couple of reasons:

- As @MicahZoltu points out, it’s not structured correctly; it should be a PR against EIP1, or at the very least an EIP that encodes changes to EIP 1.
- Nobody wants the heat of being the one to merge it, because merging is still perceived as a political statement.

---

**MicahZoltu** (2018-04-07):

I was under the impression that your EIP merging rampage was an attempt to train people away from merging being perceived as a political statement?  Is it just that we haven’t achieved that goal yet?

---

**Arachnid** (2018-04-07):

Pretty much.

Here’s some extra text to make Discourse happy with my short reply.

---

**jamesray1** (2018-04-08):

Agree fully with this, was going to reply to say something similar. I support your approach to streamlining the EIP process.

---

**phiferd** (2018-04-08):

First, EIP-894 is not an ERC.  We should either update the title of this thread to refer to EIPs in general or move the EIP-894 discussion elsewhere.  [@fulldecent](/u/fulldecent) – maybe you can clarify if your concern is with EIPs in general or ERCs specifically.

Second, I think you are claiming that Nick is not following the EIP-1 guidelines (as opposed to claiming that the guidlines are wrong). Specifically, that he’s ignoring this part:

> If the EIP collaborators approve, the EIP editor will assign the EIP a number (generally the issue or PR number related to the EIP) and merge your pull request

Here, I think EIP-1 could stand to be re-worded; it’s not clearly written.

1. What does “If the EIP collaborators approve” mean? No objections, unanimous approval, something else? In my opinion, a single editor should be able to merge as draft because there’s not really any significant risk associated with it.  That also aligns with what I seen/heard elsewhere, but the “If the EIP collaborators approve” line is just adding to the confusion.
2. EIP-1 says “Please send all EIP-related email to the EIP Collaborators, which is listed under EIP Editors below”. So “EIP Collaborators == EIP Editors”? Why have two names for the same thing? I’m guessing it has something to do with distinguishing between the group and the specific editor assigned to an EIP.  In that case, I would recommend “Editors”  and “Assigned Editor(s)” in the context of a particular EIP. Also, capitalize terms that have a definition that is specific to EIP-1 and stop prefixing terms with “EIP”.
3. My original reading (without reading EIP-1 from top to bottom) was that “EIP collaborators” were the authors of the EIP in question, not the EIP repository collaborators. I think the main thing that confused me was that if “EIP Editors” was meant, then it would have said “If the EIP Editors approve…”, but it didn’t.

---

**fulldecent** (2018-04-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> merging is still perceived as a political statement.

^^ If you don’t merge it then you are making a political statement. If you merge it then you are not making a political stance.

Therefore at current, you are making this political.

---

**fulldecent** (2018-04-09):

META. Just want to make clear. I’m not blaming anyone, incl. Nick, of failing to faithfully execute their role, or of doing anything wrong. We are just reviewing some things that happened to address inconsistencies in our processes.

I hope that is understood. I think the team is good.

---

**jamesray1** (2018-04-21):

Yeah I agree that it needs rewording.

> Please send all EIP-related email to the EIP Collaborators, which is listed under EIP Editors below

There are only people listed under EIP Editors, there is no heading for EIP Editors.

As you say I think EIP collaborators could be misconstrued to mean the authors of the EIP. [Collaborators](https://help.github.com/articles/adding-outside-collaborators-to-repositories-in-your-organization/) and contributors on GitHub have specific meanings.

> An outside collaborator is a person who isn’t explicitly a member of your organization, but who has Read, Write, or Admin permissions to one or more repositories in your organization.

Once a pull request is merged in a repo you become a contributor in that repo.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/phiferd/48/106_2.png) phiferd:

> What does “If the EIP collaborators approve” mean?

This could be edited to say: “If the EIP editors approve the EIP ([see the EIP editors workflow section below for details](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1.md#eip-editor-responsibilities-and-workflow)) and the authors are happy for it to be merged as a draft”

> For each new EIP that comes in, an editor does the following:
>
>
> Read the EIP to check if it is ready: sound and complete. The ideas must make technical sense, even if they don’t seem likely to be accepted.
>
>
>
> ```
> The title should accurately describe the content.
> ```
>
>
>
>
>
>
> ```
> Check the EIP for language (spelling, grammar, sentence structure, etc.), markup (Github flavored Markdown), code style
> ```
>
>
>
>
>
> If the EIP isn’t ready, the editor will send it back to the author for revision, with specific instructions.

I made a PR [here](https://github.com/ethereum/EIPs/pull/1017).

---

**jamesray1** (2018-04-21):

Note also that he does make a disclaimer when merging contentious EIPs, e.g. [here](https://github.com/ethereum/EIPs/pull/999#issuecomment-381537039).

---

**backus** (2018-05-07):

For what its worth, I made basically the opposite argument as [@fulldecent](/u/fulldecent) in this thread: [EIP process should embrace a model like TC39](https://ethereum-magicians.org/t/eip-process-should-embrace-a-model-like-tc39/301/1)

I considered just responding here but

1. It isn’t specific to Nick
2. I think it is a proposal on its own (or at least an argument for a proposal)

and of course visibility of the topic if it is buried in this thread.


---
source: magicians
topic_id: 11754
title: "Informational EIP: Author Handbook"
author: xinbenlv
date: "2022-11-16"
category: EIPs > EIPs informational
tags: [informational-eips]
url: https://ethereum-magicians.org/t/informational-eip-author-handbook/11754
views: 1535
likes: 8
posts_count: 11
---

# Informational EIP: Author Handbook

Creating a new EIP (Informational) to provide suggestions for Authors.

See [Add EIP-5976: Handbook for EIP Authors by xinbenlv · Pull Request #5976 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5976)

## Replies

**xinbenlv** (2022-11-28):

# Should Core EIP uses a number or a placeholder when introducing

Cross-posting some comments from [this PR #6054](https://github.com/ethereum/EIPs/pull/6054)

[@axic says](https://github.com/ethereum/EIPs/pull/6054#discussion_r1033893953)

> You absolutely need to define some number otherwise nobody can implement and test it. It is also absolutely fine to resolve conflicts when things are accepted into a protocol upgrade. This has been the practice.

[@xinbenlv responded](https://github.com/ethereum/EIPs/pull/6054#discussion_r1033928295)

> @axic the placeholder mark is meant to archive exactly what you mean here.
> When using a placeholder mark, implementers have to choose some number, and just like all parameters will be passed in, placeholder mark will also be passed in some number by implementer for sure. In addition to choosing some number, using placeholder highlights such number is subject to change, not only when finalized, but also during draft. because:"
>
>
> Having a placeholder name helps people search across different implementations, geth, ethereumjs with consistent parameter naming and make them configurable.
> This will be particularly useful say when they want to run cross-implementation consensus testing so a tester can config the placeholder to the same number and start testing.
>
>
> We could avoid this case: different implementers who implemented EIP-663 before this PR may hardcode the 0xb0 but implementer after this PR may hardcode 0xb3 for DUPN, and didn’t get reminded for paramatize DUPN as a placeholder for cross-platform testing.

and

> Another benefit is that, if there is any implied mathematical relationship between multiple instructions introduced by an EIP, having placeholder marks for all of them kind of help reminding EIP Author to explain such relationship. For example, when I read
>
>
>
> ```auto
> `DUPN` (`0xb3`)
> `SWAPN ` (`0xb4`)
> ```
>
>
>
> I interpret that it implies you are suggesting they are better to (1) be allocated starting with 0xb_ section, and are better to (2) be consecutive.
>
>
> But when I read
>
>
>
> ```auto
> `DUPN` (`0xb0`)
> `SWAPN ` (`0xb1`)
> ```
>
>
>
> In addition to  (1), (2), there was also a possible interpretation (3) that this EIP Author wants to suggest putting DUPN and SWAPN to a new Hex-teen(0x10) sector. Such implied interpretation is now removed because of this PR#6054.
>
>
> Such mathematical relationship may affect when people want to design chips / physical circuits for EVMs in the future so I assume sometime authors may care.

---

**xinbenlv** (2022-11-30):

[@frangio](/u/frangio) for feedback about this:

This handbook’s current snapshot proposes for ERCs to move to Final it requires 2 or more independent implementations and deployment on public testnets or mainnet.

Maybe it’s too restrictive, love to get your thought.

Alternatives are to require some sort of “discussion” or “wait some longer time duration” but these has been rejected / deem unfavorable by some in last EIPIP meeting but “some sort of discussion” could easily suffer from Sybil attack. Length of time to wait is also not a good “worthiness” or “thoroughness of discussion” indicator.

---

**xinbenlv** (2022-12-01):

Cross posting a relevant statement of ["reference implementation](https://ethereum-magicians.org/t/eip-5757-process-for-approving-external-resources/11215/12) is also a quality signal for EIP" by [@fulldecent](/u/fulldecent)

> The reference implementation is a quality signal that shows the author actually took the time to read the thing they themselves wrote. I support such a quality signal and I think it is or should be a requirement for publishing an ERC.

---

**frangio** (2022-12-01):

Speaking from my own personal concerns and where I think we are missing guidelines: I believe this should focus solely on ERCs, which as we know are a completely different kind of EIP when compared to Core EIPs and deserve specific guidelines that may not apply generally.

I think requiring 2 independent implementations is way too much, but it would be good to require 1 implementation. IMO discussion is the more important part, and indirectly interest. I’m not sure that it makes sense to worry about Sybil attacks. I’ll keep thinking about it.

---

**xinbenlv** (2022-12-02):

I agree with you that this particular finalizing criteria shall only apply to ERC not all EIPs.

> requiring two impl is way too much

When you say “its way too much to require two imp”, do you mean as a criteria for “Draft” or “Final”? I am proposing two impl for “Final”. If we only require one, it’s hardly demonstrating someone else other than author who would want to build impl for this standard. And less point of “Finalizing” it because if only one impl, no one cares if interface change, nobody would the sole implementation need to convince to change.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> IMO discussion is the more important part, and indirectly interest. I’m not sure that it makes sense to worry about Sybil attacks. I’ll keep thinking about it.

Yes, please do. By “sybil attack” in this context I mean it’s very easy for a motivated author to create a second account or ask co-worker / friend to comment and thus I feel it’s a bit too weak using discussion as a “Final” criteria. Ok to serve as a Draft criteria IMO.

---

**xinbenlv** (2022-12-02):

Let me move the discussion about criteria of publishing draft and advancing status into a separate thread because I think that’s an important issue and worthy of a focused discussion.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png)
    [Discussion of Guideline for advancing EIP status: A Straw-man Proposal](https://ethereum-magicians.org/t/strawman-criteria-for-advancing-eip-status/11995) [Process Improvement](/c/magicians/process-improvement/6)



> Currently in EIP-1, except of Core EIPs there is no much mentioning criteria for allowing publication of a draft EIP or advancing an EIP’s status to final. This raises concern from some EIP contributors about quality, worthiness and whether there are sufficient interest or whether sufficient level of consensus has been reached.
> In the interest of starting a discussion, I am creating this (probably dumb and full of flaws) proposal for criteria for advancing statuses of an EIP. Please see it as a…

---

**xinbenlv** (2023-01-03):

[@anett](/u/anett) for your comment~

---

**anett** (2023-01-04):

Is this related to [EIP-5069: EIP Editor Handbook](https://eips.ethereum.org/EIPS/eip-5069) ?

There’s also [EIP ERC Editor Handbook](https://hackmd.io/@poojaranjan/EIP-ERC-Editor-handbook) which is in a sense extended version of EIP-5069

A while ago [@souptacular](/u/souptacular) kicked off EIP IP group which purpose was to “clean up” the EIP process, initially to separate ERCs from EIPs. As ERCs are more of a standardised solidity functions specs.

From my last conversation with some ECH members, Core EIPs are going to be separated and will have a little bit different governance process. I’m sure [@poojaranjan](/u/poojaranjan) can share more up-to-date information.

Thank you for tagging me [@xinbenlv](/u/xinbenlv)

---

**poojaranjan** (2023-01-04):

As per my understanding, currently, `Core` EIPs follow a bit different process than what is proposed in the *strawman criteria for advancing EIP statuses*.

Generally speaking, `Core` EIPs are tightly coupled with the Network Upgrade process.

Thus, instead of following “reference implementation” and “number of days” it passes through different phases inviting “rough consensus”and “client’ implementation”.

Here is a high level diagram of status change criteria. Also, refer to the [ECH blogpost](https://medium.com/ethereum-cat-herders/shedding-light-on-the-ethereum-network-upgrade-process-4c6186ed442c) explaining phases requirements.

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/9/93961db8b2aa59782bd1808f20cfc385c3558a31_2_624x219.png)1084×380 122 KB](https://ethereum-magicians.org/uploads/default/93961db8b2aa59782bd1808f20cfc385c3558a31)

As [@anett](/u/anett) mentioned, [Core EIPs in an Executable Spec World](https://ethereum-magicians.org/t/core-eips-in-an-executable-spec-world/8640) is proposed to bring some changes to the existing process of `Core` EIPs documentation & implementation. Worth following the discussion and sharing thoughts, if any.

---

**xinbenlv** (2023-01-04):

[@anett](/u/anett) thanks for the response. I look at the differences this way: EIP Editor Handbook is focusing on instructing EIP editors who to edit EIPs. EIP Author Handbook is more for handholding new authors or returning authors to get up-to-speed to the EIP process from their angle.

Author Handbook covers more basic stuff that EIP Editor Handbook may assume editors are already super familiar with, such as “Identifying Related and Competing EIPs”. It omit things that only EIP Editors needs to know, such as `how to apply to become an EIP editor` or how long does an EIP becomes `Stagnent`.


---
source: magicians
topic_id: 2839
title: "EIP: mandatory \"Security Considerations\" for EIPs"
author: tintinweb
date: "2019-03-04"
category: EIPs > EIPs Meta
tags: [meta-eips]
url: https://ethereum-magicians.org/t/eip-mandatory-security-considerations-for-eips/2839
views: 2346
likes: 25
posts_count: 9
---

# EIP: mandatory "Security Considerations" for EIPs

Hi everyone,

To better manage the security risks in the Ethereum Change Management Process we propose a change to the EIP minimum requirements to include a **mandatory** [“Security Considerations”](https://github.com/tintinweb/EIPs/blob/eip-security_considerations/EIPS/eip-draft_security_considerations.md) section for the documentation of security relevant information directly with the EIP.

This proposal is adapted from the IETF’s Request for Comments (RFC) system ([RFC 7322 - Section 4.8.5](https://tools.ietf.org/html/rfc7322#section-4.8.5)) where this is mandatory already.

The [Meta EIP](https://github.com/tintinweb/EIPs/blob/eip-security_considerations/EIPS/eip-draft_security_considerations.md) is currently in *Draft* status. **We would love to get you involved** making this a community effort and being excellent in integrating security into one of our most important processes. To kick off a discussion please have a look at the [Draft Meta EIP - “Security Considerations”](https://github.com/tintinweb/EIPs/blob/eip-security_considerations/EIPS/eip-draft_security_considerations.md) and provide feedback to help shape the specification in a way that introduces minimal overhead while having the most positive effect on change management security.

## Where to begin?

- Review the Draft Meta EIP - “Security Considerations”

the complete list of changes → diff

Add something to the general discussion? → Post it right here

- Note that some discussion points are marked DISCUSS or TODO in the draft

Want to propose concrete changes? → File a PR on [github](https://github.com/tintinweb/EIPs/blob/eip-security_considerations/EIPS/eip-draft_security_considerations.md)

To keep EIPs clear and simple we propose a two-step approach first introducing the mandatory section (this Meta EIP) and then providing tailored guidance with an informational EIP following the RFCs approach.

looking forward to a fruitful discussion ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

cheers,

tin

---

# EIP Excerpt

## Simple Summary

This document describes an improvement to the Ethereum Improvement Proposal (EIP) system as defined in EIP-1, so that all EIPs MUST include a “Security Considerations” section. Requirements include discussion of security considerations in the design, indicating which aspects of the protocol may be affected (networking, virtual machine, etc.), listing risks and how they have been mitigated. This proposal is adapted from the IETF’s Request for Comments (RFC) system ([RFC 7322 - Section 4.8.5](https://tools.ietf.org/html/rfc7322#section-4.8.5)).

#### Benefits:

- visibility and easy access to security relevant design decisions/implications/information documented, summarised and linked with the proposal
- allows to shift focus and efforts following a security triage of proposed changes
- surfaces risks, outline their treatment or reasoning behind accepting risks
- provides input to reviewers and potential follow-up activities (e.g. security assessments)
- encourages authors to explicitly consider security in the design and outline their reasoning
- fosters an open and informed security discussion
- allows to give security related guidance, information on potential pitfalls to implementers (e.g. when a change can likely introduce a vulnerability)

### Abstract

The EIP system defines a minimum set of information and criteria to be included in a proposal. Security discussions take place but important considerations are not always documented with the EIP. Furthermore, security-related information and design decisions might blend into technical documentation, lacking visibility and not being easily available for the security community posing a greater threat for changing security aspects to not be considered in later phases of the EIP (e.g. implementation phase).

[More…](https://github.com/tintinweb/EIPs/blob/eip-security_considerations/EIPS/eip-draft_security_considerations.md)

## Replies

**boris** (2019-03-04):

Similar to this, I had proposed a Core EIP roadmap security review period:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png)
    [Security Review Period for Hardfork Roadmap](https://ethereum-magicians.org/t/security-review-period-for-hardfork-roadmap/2721) [Ethereum 1.x Ring](/c/working-groups/ethereum-1-x-ring/33)



> I’ve added a section to the Istanbul Roadmap page on the Ethereum wiki proposing a security review period for proposed Core EIPs.
> This means having some people do security reviews – which might mean engaging external auditors. But it also means communication around the Core EIP proposals that are effectively Last Call, but focused on security issues. Pay attention, have a look, does this impact your current or future use cases.
> I’ve suggested 2019-06-21 (June 21st), this is half way between th…

I’m not against this Meta EIP — just think that baking this into the roadmap / core process may be more effective.

I think you pulling out relevant IETF guidance is great! Lots more from there we should be able to borrow ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

This *might* be an edit to EIP-1 guidelines on submitting an EIP.

---

**souptacular** (2019-03-04):

This is great! I think whenever we finally get around to updating and improving EIP 1 that this should definitely go into it. In fact, if you’d like to jumpstart the process of improving EIP 1 by adding this to it as a PR and having the community discuss it. I don’t think the correct path for this is for it to be it’s own EIP, but it should definitely be considered for adding to EIP 1.

---

**dguido** (2019-03-05):

I just want to say that I fully support this idea. Trail of Bits noted a need for this kind of thinking when making new EIPs in our [review of EIP-1283](https://github.com/trailofbits/publications/blob/master/reviews/EIP-1283.pdf). I’m pleased to see how tintinweb has refined it into this approach. We’re 100% on board.

---

**tintinweb** (2019-03-08):

Hey,

thanks guys, it is great to see that there is a lot of support for embedding security into our core processes!

[@boris](/u/boris) - In my opinion this goes perfectly hand in hand. Having security information ready and conserved where change is happening also provides input to security relevant EIP process or follow-up activities ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=9) and reserving time for a security review of critical changes is important.

[@souptacular](/u/souptacular) - Sounds good! We’ve compiled this EIP under the assumption that …

- changes to the process require an EIP to be accepted and
- change should ideally be accompanied with more information outlining the motivation behind and giving some initial guidance as well.

As part of this we have already proposed [changes to EIP-1](https://github.com/tintinweb/EIPs/compare/master...tintinweb:eip-security_considerations) and we are very happy to either create a PR to kick off a series of general changes to EIP-1 (w/o an EIP) or ideally referenced to this EIP (basically the [diff](https://github.com/tintinweb/EIPs/compare/master...tintinweb:eip-security_considerations) we’ve posted already). guidance welcome!

[@dguido](/u/dguido) - Happy to have you and others not limited to the security community on board!

As initially mentioned we are proposing a two-step approach following RFCs introduction:

1. (short term: meta EIP) implementing the “Security Considerations” into EIP-1 with initial guidance on what should be considered, intentionally keeping it relaxed.
2. (mid term: info EIP) provide guidance on how to write “Security Considerations” text for EIPs tailored to the ethereum ecosystem, defining relevant terminology, outlining “the ethereum threat model” inspired by “the internet threat model”, common security pitfalls relevant for EIPs, important information that should be included that can be used for follow-up processes and providing example text for writing good “Security Considerations”. I strongly believe that it is important to provide information in a digestible way causing as little friction as possible as the main process is still proposing change and not causing an overkill by having everyone doing security assessments  while making sure information is readily available.

For the 2nd part we definitely need input from the security community and EIP authors and tailoring this to useful guidance for EIP authors will likely take some time. I’d be happy to form a working group or whatever needed to kick that off ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

**ad this EIP:**

Since I am quite new to the EIP process I’d love to get some guidance on how to move this process forward as I believe the earlier we get this into the process the better it is for the ecosystem.

cheers,

tin

---

**boris** (2019-03-08):

We’re all new to the EIP process ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

I foresee more changes coming.

Amending EIP1 and editing the `eip-x.md` Template is a good start. Can we keep the core of info in EIP-1 and then just refer to this security EIP? It is useful to not have to chase links I think.

---

**tjayrush** (2019-04-19):

[@tintinweb](/u/tintinweb) I enjoyed your talk at Eth 1.x Berlin particularly the suggestion that a mandatory section is put into any new EIPs called “Security Considerations.”

I was thinking of a similar mandatory section labeled something like “Ecosystem-Wide Considerations” that would ask the author to comment on the following question: “If your EIP is successful, what it the biggest downside to the ecosystem of that success.”

For example, if an EIP suggests that 'throw away" smart contracts should be created for every user interaction (through some sort of Factory pattern) and that contract garners millions of users, what would happen to the size of the chain’s data.

I’m trying to point at a security concern that I think gets under-appreciated. Some of the things people propose, if they succeed, would destroy the chain by polluting the commons. Perhaps you can add some words to the description of your EIP0 modification that refers to this somewhat larger issue than straight security.

---

**tintinweb** (2019-04-23):

PR filed.

Changes to EIP-1/X w/o submitting a meta-eip but suggesting to provide an informational EIP on how to provide good information as part of the security discussion as discussed during the berlin meetup.

https://github.com/ethereum/EIPs/pull/1963

---

**tintinweb** (2019-04-23):

Hi [@tjayrush](/u/tjayrush),

your input is very valid and should definitely get more visibility. There are many more specific questions that I’d like to pack up as part of an informational EIP to provide guidance on what to consider - security wise - when proposing a change to the system. Many of them are risk related and I can see your question being part of this guidance which is proposed as the next step after the more relaxed “security considerations” section is in place.

cheers,

tin


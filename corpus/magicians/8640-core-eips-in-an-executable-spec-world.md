---
source: magicians
topic_id: 8640
title: Core EIPs in an Executable Spec World
author: timbeiko
date: "2022-03-18"
category: Magicians > Process Improvement
tags: [executable-specs]
url: https://ethereum-magicians.org/t/core-eips-in-an-executable-spec-world/8640
views: 2267
likes: 3
posts_count: 17
---

# Core EIPs in an Executable Spec World

Discussion link for: [Core EIPs in an Executable Spec World - HackMD](https://notes.ethereum.org/@timbeiko/executable-eips)

## Replies

**timbeiko** (2022-03-18):

**Some comments by Greg Colvin ([source](https://github.com/ethereum/pm/issues/492#issuecomment-1071196084)):**

I’m not able to comment at [Executable Spec instead of Core EIPs - HackMD](https://notes.ethereum.org/@timbeiko/executable-eips), (account closed, it says) so I’ll do it here.

First, a nit.  It says the current process starts with:

> Pre-Draft: Open PR in EIPs Github repository, no requirements

But I think that pre-drafts take place elsewhere: blog posts, HackMds, personal GitHub repos and the like.  I don’t want PRs cluttering the EIP repo until there is a champion and a draft for a solid EIP.

A bigger problem.  The proposal is to start here instead:

> Pre-Draft: Open PR in EIPs Github repository, Open PR in Executable Specs Repository, no requirements.

Which we means we have the clutter of pre-proposals in two repos.  Worse, the rest of the proposed process seems to involve maintaining PRs in sync against two repos.  I think that is just too difficult.  Instead, I think there needs to be a hand-off point – such as the Draft staying in the EIP repo until it goes to Final.

Which gets to the substance of my problem:

> Make the following changes to the template:
>
>
>
> Specification
>
>
>
> Replace with link(s) to PRs or Commits in:
> GitHub - ethereum/execution-specs: Specification for the Execution Layer. Tracking network upgrades.
> GitHub - ethereum/consensus-specs: Ethereum Proof-of-Stake Consensus Specifications

This seems to mean that the authors and the reviewers of Core EIPs will need be competent programmers in the language of the Execution Specs.  In which case I might need to stop writing and reviewing Core EIPs.

From my own experience…  The C++ Standard itself was written in a fairly precise mix of formal notation, maths, and technical English.  In the end only the lead Editor was trusted to get it right.  Ordinary humans – even compiler authors – weren’t worthy.  Proposals to change the Standard were not generally presented in that dialect.  They were typically a mix of C++ and more ordinary technical English – the kind ordinary experts can read and write.  New features were typically implemented in at least one compiler or library as well.  The “standardese” for accepted proposals basically got reverse-engineered by the Editor from these sources.

So I’d prefer to see the current EIP process remain close to as it is, with the translation to Execution Specs happening further down the road.  As I understand it the Execution Specs are an executable client, so will (like the other clients) have the Final EIPs implemented and running on the testnets well before we go live.  Once they are live this executable spec – being in consensus on the network – is ground truth, and the EIP subject to errata if it differs.

A second objection to demanding that EIPs use a particular specification language is that the best language for a proposal will vary.  It might be mathematical or graphical notation specific to its domain.  It might be more abstract and declarative than executable.  It might even be English.  The proposal itself shouldn’t need to say how best to implement itself in a particular language.

Please don’t take any of this as an objection to an executable specification.  Rather, I think the beauty is that the executable specification emerges directly out of the “literate programming” effort of maintaining the client that instantiates that spec.

---

**SamWilsn** (2022-03-23):

At [@MicahZoltu](/u/micahzoltu)’s request, I modified [@timbeiko](/u/timbeiko)’s original note to be more inline with how I envision things: [Executable Spec instead of Core EIPs - HackMD](https://hackmd.io/t65HJyx6RxSVeZQtURE9gw)

The most substantial difference is that instead of maintaining Core EIPs alongside the other categories in [ethereum/EIPs](https://github.com/ethereum/EIPs), Core EIPs would exist in subdirectories of the [ethereum/execution-specs](https://github.com/ethereum/execution-specs) and [ethereum/consensus-specs](https://github.com/ethereum/consensus-specs) repositories.

There are also a few minor changes to branch names, and at which stages branches get merged. Oh, and using reStructuredText instead of markdown *hides*.

---

**MicahZoltu** (2022-03-24):

What would the process look like in your eyes [@SamWilsn](/u/samwilsn) for changes that touch both consensus and execution?

---

**SamWilsn** (2022-03-24):

If we can stuff them into the same repository, then as a single EIP. If we can’t, two separate EIPs that refer to each other.

I think the former is my preference, but only slightly.

---

**timbeiko** (2022-03-24):

I personally have a preference for a single document here. EIPs already have a lot of awareness within the community and I want to make sure we don’t regress a lot on that front. I understand it is hard to manage the process across 2+ repos (EIPs, EL spec, CL spec), but that might be worth some engineering work to get right. It’d be great to be able to point people to, say, EIP-XXXX as a reference document for Withdrawals/Sharding/Stateless which then links to the spec changes in their respective repositories.

---

**SamWilsn** (2022-03-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> I personally have a preference for a single document here.

Single document, as in CL and EL in the same repository; or as in your original proposal where the EIP links out to the CL and EL repositories?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> EIPs already have a lot of awareness within the community and I want to make sure we don’t regress a lot on that front. I understand it is hard to manage the process across 2+ repos (EIPs, EL spec, CL spec), but that might be worth some engineering work to get right.

So you’d be opposed to splitting Core EIPs into their own process, and keeping Network/Interface/ERC/Meta/Informational EIPs in the current one?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> It’d be great to be able to point people to, say, EIP-XXXX as a reference document for Withdrawals/Sharding/Stateless which then links to the spec changes in their respective repositories.

I think saying “See EIP-5678 and -5679” is almost as good as having a single document.

---

I want to avoid changing “EIP” as a name. It really is a good identifier system. This might be a bit off topic, but if we were to split Core out, I’d probably say that:

- All EIPs with N = 10000 && (N % M) == 0 are Core EIPs against CL.
- All EIPs with N >= 10000 && (N % M) == 1 are Core EIPs against EL.
.
.
.

That way all the tooling knows based on just the EIP number where to send readers to get the spec, and EIPs that are related are grouped together by number.

---

**timbeiko** (2022-03-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Single document, as in CL and EL in the same repository; or as in your original proposal where the EIP links out to the CL and EL repositories?

My preference is to have the EIP link out to both specs repo.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> So you’d be opposed to splitting Core EIPs into their own process, and keeping Network/Interface/ERC/Meta/Informational EIPs in the current one?

Core EIPs already have their own process ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12) What I like about the current system is that:

1. You can go to either the EIPs repo or eips.ethereum.org and see a list of all proposals, both Core and others.
2. The EIP is the canonical document you must read to then dive deeper. Arguably, that’s not really true anymore and fails for complex EIPs (as seen with 1559, withdrawals, 4844, etc.). It is something I think would be good to aim for, though.

That said, I could see us splitting out ERCs into their own separate repo and hosting them at [erc.ethereum.org](http://erc.ethereum.org). The community recognition seems sufficient, and both groups are distinct enough. Core/Networking still seem tightly coupled. Interface/Meta now seems somewhat stale due to the API+specs repo.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I want to avoid changing “EIP” as a name. It really is a good identifier system. This might be a bit off topic, but if we were to split Core out, I’d probably say that:
>
>
> All EIPs with N  All EIPs with N >= 10000 && (N % M) == 0 are Core EIPs against CL.
> All EIPs with N >= 10000 && (N % M) == 1 are Core EIPs against EL.
> .
> .
> .
>
>
> That way all the tooling knows based on just the EIP number where to send readers to get the spec, and EIPs that are related are grouped together by number.

That’s interesting!

---

**gcolvin** (2022-04-05):

EIP numbers are generally taken from the sequence that Github provides for PRs.  That makes it easy for editors to assign the number without consulting and maintaining a separate list of already-assigned numbers.

---

**SamWilsn** (2022-04-05):

I would be happy to maintain an https://nexteipnumber.invalid if it helps ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12)

---

**gcolvin** (2022-04-05):

I’d really rather not change long-standing practice in favor of something more complicated.

---

**gcolvin** (2022-04-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> That said, I could see us splitting out ERCs into their own separate repo and hosting them at erc.ethereum.org.

I’d be OK with that, though getting there might be painful, given the large number of existing EIPs that are ERCs.  But this isn’t a new conversation, and so far we’ve decided to leave the mess be.

---

**SamWilsn** (2022-04-05):

Actually a better idea might be to have the EIP bot automatically insert an EIP number on merging. I think that would solve some long standing issues [@MicahZoltu](/u/micahzoltu) has too!

---

**gcolvin** (2022-04-06):

Can the bot automatically open the appropriate Magicians thread and fill that in too?

---

**MicahZoltu** (2022-04-07):

It could, yes.  It would be a notable amount of engineering work to get right though.  Presumably we would want it to include the abstract and maybe motivation sections, but we would also want the bot to keep those up to day in the original post in the thread.  This would be great, but non-trivial effort involved to accomplish that.

If we just had it create a blank issue, then the original post wouldn’t be editable by the author and would likely end up with a stale body.

---

**SamWilsn** (2022-04-20):

I’d say the open questions for this are:

- Do we make a python diff a mandatory part of the EIP process? Python diff OR yellow paper diff? Keep it natural language English?
- Where do core EIPs live? In the execution-specs/consensus-specs repositories? In the EIPs repository?
- Where do other (network, interface, ERC, etc) EIPs live?
- How do we number EIPs? Restart at one for CLIPs (consensus layer improvement proposals) and ELIPs (execution layer improvement proposals)?
- Can we create a formally verifiable spec for Ethereum that’s in an accessible language? Maybe dafny?

---

**gcolvin** (2022-05-05):

This is of course a long-standing conversation that so far has always led to maintaining the status quo.

> I’d say the open questions for this are:
>
>
> Do we make a python diff a mandatory part of the EIP process? Python diff OR yellow paper diff?

No.  The diffs come after the EIP has been implemented in the Python client, and in the end only the maintainers of the Python client are competent to make those changes.  Yes, the Eth2 team did it that way, but they started with Python code and built from there.

> Keep it natural language English?

EIPs should be written in the form most appropriate to that EIP.  The natural language used should be English.  Mathematics, diagrams, and such are welcome.  (Pseudo-) Python is encouraged. If the Core Devs find an EIP inadequate for any reason they can push back on the authors.  If the Core Devs want to demand Python or Yellow Paper diffs it is their call, not the EIP Editors.

The [Ipsilon](https://notes.ethereum.org/@ipsilon/about) team is already using Python to express algorithms in their EIPs, but these are not diffs against the Python client.  They are implementing and testing their EIPs against their C++ client.

(I’ll note that the Internet is built to RFC standards that do not enforce anything close to the level of structure that we are.)

> Where do core EIPs live? In the execution-specs/consensus-specs repositories? In the EIPs repository?

[github.org/ethereum/EIPs/EIPS](http://github.org/ethereum/EIPs/EIPS)

> Where do other (network, interface, ERC, etc) EIPs live?

[github.org/ethereum/EIPs/EIPS](http://github.org/ethereum/EIPs/EIPS)

> How do we number EIPs? Restart at one for CLIPs (consensus layer improvement proposals) and ELIPs (execution layer improvement proposals)?

The same way we do now.  All EIPs of whatever type are numbered from the same sequence.  Having different proposal with the same number is sure to cause confusion.

> Can we create a formally verifiable spec for Ethereum that’s in an accessible language? Maybe dafny?

It can’t be done in Python because there is no formal specification for Python.  Also, Python is not designed for the purpose of formal verification, which generally requires more declarative specifications.

Formal specification and verification can be and has been done by other groups using various tools for various purposes.  No one formal language is best.  A quick search found this rather daunting 2020 review:

A Survey of Smart Contract Formal Specification and Verification

Another resource worth studying is the formal verification (in Dafny) of the Beacon Chain contract:

[Formal Verification of the Ethereum 2.0 Beacon Chain](https://arxiv.org/pdf/2110.12909.pdf)

Most EIP authors cannot produce such formal specifications.  If we want them we will need experts to help.

Finally, I’ll note that in a strong sense

- the main net is the specification.

That is, the consensus behavior of the clients **is** the protocol – even if its behavior was unintentional –   and any specification that fails to describe its actual behavior is wrong.


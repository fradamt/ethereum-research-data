---
source: magicians
topic_id: 14329
title: Licences for Assets / Reference Implementations in EIPs
author: SamWilsn
date: "2023-05-17"
category: Magicians > Process Improvement
tags: [licensing, copyright]
url: https://ethereum-magicians.org/t/licences-for-assets-reference-implementations-in-eips/14329
views: 1363
likes: 3
posts_count: 16
---

# Licences for Assets / Reference Implementations in EIPs

Currently there is no consistent policy for licenses allowed in the EIPs repository (aside from the EIP itself.) This is especially relevant for reference implementations.

## Policy Options

There are three camps:

*Please be aware that I am biased, so if I misrepresented your views below, call me out on it.*

### All assets must be CC0-1.0

This view is held by [@Pandapip1](/u/pandapip1).

Simple, clearly unambiguous. Most permissive for implementers. Most restrictive for authors.

### Allow non-copyleft open source assets

This is my view.

Assets may be any license that doesn’t impose significant restrictions on implementations. So this would allow `MIT`, `Apache-2.0`, and likely some others. It would, however, deny `GPL-3.0` and  `BUSL-1.1`.

More ambiguous (we’d need to maintain a list of approved licenses), but balances author vs. implementer interests.

### Unrestricted Reference Implemenations

This view is held by [@xinbenlv](/u/xinbenlv) and [@gcolvin](/u/gcolvin).

Allow any license we can legally distribute, and allow linking to reference implementations we cannot distribute.

Also extremely unambiguous, provides authors the most flexibility, but doesn’t preserve our immutability/availability goals and can potentially create copyright traps.

## Related Reading

- https://github.com/ethereum/EIPs/pull/5379
- Unlicensed code should NOT be allowed to be included in ANY proposals · Issue #7027 · ethereum/EIPs · GitHub
- EIPs should preemptively add a CLA · Issue #5662 · ethereum/EIPs · GitHub
- Patent covenant for EIP submissions · Issue #1840 · ethereum/EIPs · GitHub

## Replies

**xinbenlv** (2023-05-17):

Thank you for summarizing it, [@SamWilsn](/u/samwilsn) !

My stance is generally: “we should make it easy for ERC authors to share reference implementations for educational purpose”.

On that basis, for the question I am happy with *either* of the following:

1. Allow check-in a broad range of Open Source Licenses for RefImp code into asset folder
2. Allow link to external reference implementations.

Disallowing both will make it super hard to share reference implementation and undermine the open standardization effort.

---

**SamWilsn** (2023-05-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> a broad range of Open Source Licenses

How broad is broad? Would you permit a license that allows viewing the reference implementation, but disallowed any derivative work?

If so, what is the point of such a reference implementation?

---

**tbergmueller** (2023-05-17):

While CC0 is optimal for the EIP, I feel it’s too restrictive for reference implementations.

I’d consider especially [CC0 4.a](https://github.com/ethereum/EIPs/blob/master/LICENSE.md?plain=1#L104) stating “No trademark or patent rights held by Affirmer are waived, abandoned, surrendered, licensed or otherwise affected by this document.”

IMHO (not a lawyer obviously) “No […] patent rights held by Affirmer are […] licensed” implies that I cannot be 100% sure when I use a reference implementation licensed under CC0, whether I will applicable to license fees under certain circumstances.

This was the prime reason why we decided to use MIT license (also used throughout OpenZeppelin) for the Reference Implementation in our ERC-6956. We wanted people to be able to freely use it, without having any second thoughts. Especially since for our edge-case there is a broad application range with physical products and smartphones involved etc. and as soon as things get beyond digital-only, you enter a patent landscape that’s hard to comprehend.

---

**SamWilsn** (2023-05-18):

We discussed this at some length in

https://github.com/ethereum/EIPs/issues/5662

---

**tbergmueller** (2023-05-18):

Thanks, although I believe I have another angle, which has not been discussed so far.

As [responded in much more detail to your comment in PR 6956](https://github.com/ethereum/EIPs/pull/6956#discussion_r1198056958), we have a situation, where we do own patents that have at least similarities to the EIP and I want to be very clear that the EIP and reference implementation can be used freely and unrestricted by anyone. Yet, I do no want to grant a free, unlimited and world-wide license on any of our patents, as they cover much more than just what’s in the EIP and reference impl.

For the EIP I think CC0 still works, but I would argue that if we were to enforce CC0 for reference implementations and not allow any amendments, I would in my case not have the legal framework to ensure people it is safe to use our reference implementation here. That’s why the reference implementation must allow MIT, BSD or similar imo.

---

**SamWilsn** (2023-05-18):

I don’t think the EIPs repository has the authority to stop you from additionally granting patent licenses ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12) If you wanted to dual license under `CC0-1.0` and/or `MIT`, of course that’d be fine. I think [@Pandapip1](/u/pandapip1) just wants one of the options to be `CC0-1.0` (though I may be misrepresenting his position.)

---

**tbergmueller** (2023-05-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> has the authority to stop you from additionally granting patent licenses

Well, that’s clear but I think I didn’t express myself clear enough ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12) .

I meant; I have a patent US1234, which is partly similar to the EIP. But the EIPs content is e.g. just one aspect, not the complete content of the patent. So I need to find a legal way, to license EIP + Reference Impl freely and unrestricted. But at the same time, it is not possible for me to say “With this EIP I grant you a license for US1234” - because the US1234 has other aspects beyond the EIP, which I do not need or want to waive.

Dual licensing works imo! I just thought the goal was to have CC0 mandated as in the verbatim Waiver in the EIP. That would’ve been an issue - but seems all is fine then. Thanks for the clarification

---

**SamWilsn** (2023-05-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tbergmueller/48/9196_2.png) tbergmueller:

> I meant; I have a patent US1234, which is partly similar to the EIP.

Right, that makes sense.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tbergmueller/48/9196_2.png) tbergmueller:

> So I need to find a legal way, to license EIP + Reference Impl freely and unrestricted. But at the same time, it is not possible for me to say “With this EIP I grant you a license for US1234” - because the US1234 has other aspects beyond the EIP, which I do not need or want to waive.

Yep, that’s perfectly understandable. The requirements, today, of the EIPs repository are roughly:

- Text of the EIP itself, including any inline code, MUST be available under CC0-1.0.
- Files under the ../assets/eip-xxxx/ directory SHOULD be CC0-1.0, but MAY be a non-copyleft OSI approved license.

---

**joeysantoro** (2023-10-26):

The current validation doesn’t allow any external linking at all. Is this conversation the right place to petition to allow external links in the Reference Implementation section? It would be hard to validate their license so I am in general pro allowing any reference impl.

---

**SamWilsn** (2023-10-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> The current validation doesn’t allow any external linking at all.

We do allow some external links, and are open to more (following [EIP-5757](https://eips.ethereum.org/EIPS/eip-5757)). You can see the full list of currently permitted origins in [EIP-1](https://eips.ethereum.org/EIPS/eip-1#linking-to-external-resources).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> Is this conversation the right place to petition to allow external links in the Reference Implementation section?

Eh, it’s close enough ![:person_shrugging:](https://ethereum-magicians.org/images/emoji/twitter/person_shrugging.png?v=12)

---

In addition to [the reasoning behind prohibiting external links in general](https://ethereum.github.io/eipw/markdown-rel-links/), there are a couple important concerns specific to external reference implementations.

When people link to an external implementation, it’s often their *production* implementation. It usually comes with a ton of stuff that isn’t directly related to the EIP itself, and often divides the functionality over several libraries. Simplicity and minimalism are rarely a primary concerns. A reference implementation for an EIP should be short and sweet, and help clear up any questions in the EIP.

@/Dexaran brought up an excellent concern with ERC-20. Having an external reference implementation right in the EIP gives the authors of that EIP an unfair advantage, since it looks like their implementation is the “official” one. Once the proposal goes to the Final status, it can no longer be updated, so no competing reference implementations can be added.

---

All that said, [@xinbenlv](/u/xinbenlv) has started a project over at https://ercref.org/ to provide a better source of reference implementations.

---

**Dexaran** (2023-10-27):

> When people link to an external implementation, it’s often their production implementation. It usually comes with a ton of stuff that isn’t directly related to the EIP itself, and often divides the functionality over several libraries. Simplicity and minimalism are rarely a primary concerns. A reference implementation for an EIP should be short and sweet, and help clear up any questions in the EIP.

I completely agree with this.

The main purpose of the “reference implementation” is to be a demo of the proposal. It is supposed to answer questions of “how it should work” or “does the logic of that particular code match the logic described in the EIP”.

To find a production implementation the reader must use Google - this will allow for healthier competition among multiple potential implementers.

**I don’t see any reason for a “reference implementation” to be a link at all. In my opinion it would be much better to write the code in the text of the EIP and make it CC0 licensed alongside the text.**

---

**joeysantoro** (2023-10-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> @/Dexaran brought up an excellent concern with ERC-20. Having an external reference implementation right in the EIP gives the authors of that EIP an unfair advantage, since it looks like their implementation is the “official” one. Once the proposal goes to the Final status, it can no longer be updated, so no competing reference implementations can be added.

I agree completely with the logic behind not allowing production implementations and think that there can be clear rules to enforce around this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> I don’t see any reason for a “reference implementation” to be a link at all. In my opinion it would be much better to write the code in the text of the EIP and make it CC0 licensed alongside the text.

The idea and intention behind a reference implementation is difficult for ERC authors to fulfill without the ability to provide external links to github for example.

This is all the info in EIP-1 about reference implementations: “An optional section that contains a reference/example implementation that people can use to assist in understanding or implementing this specification. This section may be omitted for all EIPs.”

With sufficiently complex standards, the reference implementations would get unwieldy to write in the file. [ERC-7540-Reference/src/ERC7540AsyncRedeemExample.sol at main · ERC4626-Alliance/ERC-7540-Reference · GitHub](https://github.com/ERC4626-Alliance/ERC-7540-Reference/blob/main/src/ERC7540AsyncRedeemExample.sol) was written purely as a reference for ERC-7540 and is over 100 lines of solidity without including the inherited ERC-4626 library which is an additional several hundred lines.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> All that said, @xinbenlv has started a project over at https://ercref.org/  to provide a better source of reference implementations.

This is a great initiative. At a certain point the reference implementations section is unnecessary. I’d propose doing one of the following:

- deprecating the reference implementation section and pushing more towards initiatives like ercref
- allowing external links to github with some restrictions such as permissive free licensing, not production implementations
- editing EIP-1 and the eip-template to provide more clarity on the goals and parameters of the current reference implementation section. For example can it be pseudocode or inherit an unimplemented additional ERC that is abstracted in the reference.

---

**arrans** (2024-02-19):

[This blog post](https://creativecommons.org/2011/04/15/using-cc0-for-public-domain-software/) on the CC website unambiguously states that “CC licenses are not intended to be used to release software”. There is also an [FAQ](https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software) in which they “recommend against using Creative Commons licenses for software”.

---

**SamWilsn** (2024-02-21):

In that blog post, they link to [this wiki page](https://wiki.creativecommons.org/wiki/CC0_FAQ#May_I_apply_CC0_to_computer_software.3F_If_so.2C_is_there_a_recommended_implementation.3F), which states:

> CC0 is suitable for dedicating your copyright and related rights in computer software to the public domain, to the fullest extent possible under law. Unlike CC licenses, which should not be used for software, CC0 is compatible with many software licenses […]

---

**sbacha** (2024-03-24):

Seeing as how I am the author of two of the posts [@SamWilsn](/u/samwilsn) linked, I will provide additional context as to my motivation.

## Concerning source code for ‘Reference Implementations’

This is problematic currently because of a lack of a ‘DCO’ or acknowledgement from the contributor that they have the necessary rights/permissions to enter into an agreement for contribution of code that may be used by, for example, their employer.

> For example, we have an RPC endpoint, mev_sendBetaBundle that we may want to upstream as an EIP. The method name could be trademarked by us, then submitted to as an EIP. This is a somewhat contrived example as the class name could be slightly adjusted, but it illustrates my point.

### Current Ambiguity in the ‘drafting’ / ‘last call process’

The current licence regime is ambiguous as to the extent of which contributions made within the EIP/ERC Standards Process (e.g., via e-mail, oral comment, the discussion forums) are similarly treated as a ‘collective work’ or are retained by the originator. This can be an issue, especially if the discussion process is taking place in some external 3rd party forum in which arbitrary terms can be imposed upon.

### EIP/ERC as a Trademark

We have seen that ERC (moreso than EIP) has been used to claim support or endorsement for, or as an indication of origin of, authenticity/reliability of such services using the name as a marketing tool for promotion and positive endorsement. Documents that are published by third parties, including those that are translated into other languages, should not be considered to be definitive versions of an ERC/EIP.

Without having an entity (this does not necessarily have to be the EF per se) that holds such rights to them, holding external parties accountable for misappropriating the communities work is much more difficult, if not impossible.

### Reasons for pro-Public Domain

An important part of the reason is that if for example the Ethereum Foundation wanted to retain change control of the technical specifications of the (sic) Ethereum Protocol, it would have to copyright such specifications. By placing it in the public domain, it is technically possible for any other potential standards body to do so, without their involvement.

### Source Code Licence for Reference Implementations

The IETF Trust uses the following:

> Revised BSD License set forth in Section 4.c of the IETF Trust’s Legal Provisions Relating to IETF Documents (Trust Legal Provisions (TLP) – IETF Trust).

Personally, [I suggest using UPL-1.0 or the Universal Permissive License](https://github.com/sambacha/use-UPL-not-MIT)

- Clear patent protection. The UPL is a broad permissive license including both a copyright license and an express patent license, covering at least a version licensed by someone under the license (for example a distributor) and/or a version someone contributed to even if they never distribute the whole. (The reason the latter is needed is discussed below.) By virtue of the unambiguous patent license, the UPL is materially clearer with respect to the rights licensed and likely broader than either the MIT or BSD licenses.
- Clear & simplified relicensing. The UPL expressly permits sublicensing under either the UPL or under other terms, which clearly allows someone to relicense code received under the UPL either on copyleft terms, on proprietary terms, or otherwise, thus permitting maximum flexibility in reuse.
- Reduced overhead in source files. The UPL expressly permits use of the license without including a full copy of the text, which is useful, I guess.
- It can be used as a contributor agreement. Finally, the UPL may be used as a contributor licence agreement licensing both the software itself and also contributor patents for use in one or more “Larger Works.” The Larger Works licensed in this fashion are designated by the use of a separate file accompanying the license, akin to the NOTICE file that accompanies the Apache License, Version 2.0. The Larger Works file can be used to control for both contributions to other works (for example, we could specify MySQL in a Larger Works file for a work, which would then license contributor patents for MySQL as well as the contribution), to set patent license scope for specific versions (for example, we could specify the approved reference implementation of JSR-xxx including Maintenance Releases to ensure that all contributors to an RI are licensing both the final version of the RI and qualified updates under the JCP program), or both.

## Patents?

Lol. Unless you have the money to pursue legal enforcement of your patent claims, they are at best a form of insurance against some would-be patent troll.

## ERC Split provides an opportunity

At the very least, by having the EIP process split from the ERC process, we can enforce stronger protections on the ERC side of things as appropriate without undermining some of the principles behind the EIP process.

The longer the community waits, the less likely anything other than having a separate repo will differentiate the two different processes. Publishing something along the lines of ‘ERC404’ should not happen: these sorts of shameless tactics are the epitome of a tragedy of the commons’ problem that the current inherited EIP process enforces upon the ERC process.

We should also make a distinction between including the source code of a smart contract (e.g. what was provided as an example for ERC4626/etc and including a canonical ABI/API interface definition within that ERC proposal.

### Locked Versioning AKA Finalized EIP/ERC’s are also a great thing

fixed meaning unchanging, not unbroken specifications are a great thing. Keep the bike shedding discussions away.

### ERC, why art thou not a package registrar?

[Ryan Dahl’s presentation in 2018 introducing Deno highlights a big problem: no native JavaScript package registry](https://tinyclouds.org/jsconf2018.pdf). What is the result when the community does not own the package registry? Corporate co-opt. NPM is now a Redmond wholly owned subsidiary, and Ethereum’s ecosystem could certainly fall to that same fate. Of course, it’s not from lack of trying, however the ERC repo being separate now represents a potential to cut across languages and providing something similar to what [@xinbenlv](/u/xinbenlv) is attempting to do with [ERC Ref](https://ercref.org/#Contribute).

Think that package registry is a ‘settled problem’? Just a few weeks ago, [JSR was announced, a new registry](https://socket.dev/blog/jsr-new-javascript-package-registry),[[1]](#footnote-46807-1).

### Concluding remarks

Yes, all of these issues I brought up because I want to see a package registry for fuck sakes, please can we do that guys?

Yours truly,

me. xoxo.

1. The codebase for the registry is available as well: JSR · GitHub ↩︎


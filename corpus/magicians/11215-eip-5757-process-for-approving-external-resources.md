---
source: magicians
topic_id: 11215
title: "EIP-5757: Process for Approving External Resources"
author: SamWilsn
date: "2022-10-06"
category: EIPs > EIPs Meta
tags: [eip-process, meta-eips]
url: https://ethereum-magicians.org/t/eip-5757-process-for-approving-external-resources/11215
views: 3109
likes: 7
posts_count: 17
---

# EIP-5757: Process for Approving External Resources

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5757)














####


      `master` ← `SamWilsn:external-links`




          opened 01:25AM - 06 Oct 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/2/2fd0cd3103e1847d9a5ec672e4955d775c62ee21.png)
            SamWilsn](https://github.com/SamWilsn)



          [+155
            -0](https://github.com/ethereum/EIPs/pull/5757/files)

## Replies

**xinbenlv** (2022-10-07):

Thank you [@SamWilsn](https://github.com/SamWilsn) for this effort.

I just to want to bring to the context of readers of this EIP that a few other Editors also provided their voices and proposed their solutions which are also worth considering [Pros and Cons for Allowing External Links in EIP. - HackMD](https://hackmd.io/ddolKJF9TpGbO5MktrtT5A)

---

**SamWilsn** (2022-10-08):

[@xinbenlv](/u/xinbenlv) posted some excellent comments on the pull request that I think are better suited to this discussion thread:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/8227_2.png) xinbenlv:

> Permissible sources MUST NOT charge a fee for accessing resources.

I love the intention but I think this block us from many academic publications. ISO standards are also charging fees.

I’m perfectly fine not allowing links to these sources.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/8227_2.png) xinbenlv:

> The Ethereum ecosystem is built on openness and free access, and the EIP process should follow those principles.

This is a very good intention. *Rhetorically* with the similar good intent, can we ban all links to any content cannot be run without a hardware (e.g. computer or phone) that is not free, or can we ban all links to any content that is centralized, such as Github?

Sure! I’m all for continuing to ban external links. I just think most other people want to allow *some* external links.

The difference between having to pay to access GitHub and having to pay to access an External Source is that once you’ve paid once to download the EIPs repository, you’re free to query it locally and to share it freely. Any final EIPs will continue to be available to you and anyone you choose eternally. That isn’t necessarily true of external resources.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/8227_2.png) xinbenlv:

> That’s just a friendly joke, my real intention is to respectfully suggest not fully ban non-free content but require author to use a cheaper permissible sources whenever available. I love the direction, but the world is not perfect yet and we only get to do one step at a time.
>
>
> Rationale
>
>
> Even Wikipedia didn’t make this requirement.

The EIP repository has vastly different goals than Wikipedia. I think we’re free to choose our own path.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/8227_2.png) xinbenlv:

> I think this reduces our ability to link to useful content.

No argument here. I’m sure there are tons of useful things that this policy excludes.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/8227_2.png) xinbenlv:

> At the end of day, everything charges. We might live in a first world country that getting online is not very expensive, but my phone bill is 30 dollars a day, meaning if it take me 1 minute to find the link to my EIP online, I am charged by my phone ISP for 0.00001157407 for me to access the EIP I authored. I am saying, there is nothing free.
>
>
> Also “free” is never free, you might be paying for ads, paying for your privacy or attention. Some people might cherish their privacy or other reasons better than monetary cost.

That’s all very true and applies to everything, so it’s somewhat meaningless. Obviously the EIP isn’t saying that you can’t link to a source because you burn calories while reading it.

EIP-5757 specifically says “**MUST NOT** charge a fee for accessing resources”. It specifically doesn’t prohibit charging fees for, say, photocopying a book at a library.

---

**xinbenlv** (2022-10-09):

Thank you for forwarding my comment on the PR.

I invite more readers comment on their views on the link policy.

---

**xinbenlv** (2022-11-04):

Thank you for the effort, here is some feedback before moving from Last Call to Final

1. 3(or 6)month test run, default to lose effect unless
2. relax the restriction of distribution and free sources.
3. Allow new origins to be added by PR in addition to a fast-track EIP
4. Create a list of initial accepted origin
5. [optional] represents the origin in the format of regex.

Thank you!

---

**SamWilsn** (2022-11-04):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5874)














####


      `master` ← `SamWilsn:external-links`




          opened 03:05PM - 04 Nov 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/2/2fd0cd3103e1847d9a5ec672e4955d775c62ee21.png)
            SamWilsn](https://github.com/SamWilsn)



          [+91
            -1](https://github.com/ethereum/EIPs/pull/5874/files)







If we're okay with this format, I'll update `eipw` and get the csl-json to rende[…](https://github.com/ethereum/EIPs/pull/5874)r into a human readable citation.












Here’s an initial list of origins.

---

**xinbenlv** (2022-11-09):

Author of EIP-5757 [@SamWilsn](/u/samwilsn) , and editors, before finalizing EIP-5757, I’d love to bring this suggested edit to your attention: [Update EIP-721: broken and mislinked openzeppelin links by konojunya · Pull Request #5903 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5903)

and hear your thoughts on how will this PR be reviewed under the EIP-5757, assuming the whole EIP-721 is created after EIP-5757.

---

**SamWilsn** (2022-11-10):

Under the 5757 rules, the authors could have tried to get their external origins approved. Most of those links wouldn’t qualify. JSON-Schema is BSD, so you could include it in assets. None of the OZ links are immutable, so they probably wouldn’t qualify.

---

**xinbenlv** (2022-11-10):

Got it. Glad it’s clear under such rule. Kudos for EIP-5757

*This comment and its answers should not be considered as blocking merging EIP-5757 into Final*

I like to kindly use this case to test the EIP-5757 against the core purpose of EIP in general. Do we see EIP as a place to only publish a recognized standardize, or do we see EIP as a place for proposal and such proposal might need backing evidence that can live outside of a proposal?

In a more specific case, would EIP-721 be in a better proposal if had the author and editor back then trim all links and references. A large portion of the EIP-721 draft was articulating

- the prior art
- the existing implementations of this particular draft
- the solidity language implements that were made to enable what EIP-721 needs to be safe and gas efficiency

Some of those links I believe can be trimmed, but a lot of them plays an important roles in arguing for this EIP.

For example, back then there were other several EIPs competing with each other aiming to be adopt as canonical. It would be hard to imagine a winning EIP could make a more competing case by pointing out adoptions and implementations, as well as upstream tool chains made to enable this EIP. This applies EIP-1155.

Adding authors of these EIP to see if they have an insight / opinion to share

[@fulldecent](/u/fulldecent), @coinfork

*This comment and its answers should not be considered as blocking merging EIP-5757 into Final*

---

**xinbenlv** (2022-11-11):

List of other arguments being made to be placed under scrutiny of new EIP-5757 rule

## Case 1

Author in https://github.com/ethereum/EIPs/pull/5748/files#r1002133832

mentions specific company and product in an attack as a historical background for motivation. Shall such mentioning / reference be removed from spec under new EIP-5757? My understanding is it will be. But from a EIP general purpose standpoint, does it help make a proposal more convincing or less convincing? I think it’s more convincing to be put into concrete context. In such case, citing a specific security instance is a good way to argue with real case.

## Case 2



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5920/files#r1020475435)














####


      `master` ← `Pandapip1-pay-opcode`




          opened 06:16PM - 11 Nov 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/0/00f961ac62494fc77fa3af407fddb0b96182f8e4.png)
            Pandapip1](https://github.com/Pandapip1)



          [+58
            -0](https://github.com/ethereum/EIPs/pull/5920/files)







Adds a new opcode to do simple ether transfers.

discussions-to: https://eth[…](https://github.com/ethereum/EIPs/pull/5920)ereum-magicians.org/t/eip-5920-pay-opcode/11717












I left a technical comment to the fact Solidity does something (doing payable) shows this EIP’s motivation is a material concern and Elsewhere attempts were made to mitigate that. I feel citing the exact line of code to demonstrate Solidity’s behavior helps make the argument. Under EIP-5757 it’s hard to provide fact. But in a general case, I feel links like this help articulation and make a proposal more convincing.

[@SamWilsn](/u/samwilsn) [@Pandapip1](/u/pandapip1) thoughts on this?

---

**xinbenlv** (2022-11-11):

By the way, IIRC on the last EIPIP meeting, the understanding is EIP-5757 will be in effect for 3 or 6 months after in effect, and lose effect by default after expiration unless a permanent adoption agree upon by EIP editors again, right?

[@SamWilsn](/u/samwilsn)

---

**fulldecent** (2022-11-12):

An interface (typically in Solidity, with full NatSpac) is necessary for articulating an ERC.

The reference implementation is a quality signal that shows the author actually took the time to read the thing they themselves wrote. I support such a quality signal and I think it is or should be a requirement for publishing an ERC. Otherwise, people are publishing bad ideas that they themselves did not even think through and it becomes my responsibility to point out their flaws… lest EIPs be polluted with low quality content.

It will be nice to link to immutable resources, I can support that push. This can include publishing an application, incorporating the reusable reference implementation on-chain. Ideally this should be on Mainnet, spending real money to deploy. Spending real money is also a trust signal.

---

**Pandapip1** (2022-11-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Spending real money is also a trust signal.

EIPs must remain free.

---

**fulldecent** (2022-11-15):

Using Ethereum isn’t free. And using Ethereum is a reasonable requirement for telling other people how to improve Ethereum.

---

**SamWilsn** (2022-11-16):

Regardless of whether you have to pay to use Ethereum or not (plus receiving ether is free AFAIK), you should be able to *verify* Ethereum at no cost beyond internet and hardware.

While implementers are free to use whatever signals they want when deciding which EIPs to implement, I don’t think the EIPs repository should impose *too* many requirements on authors and certainly not any requirements that are non-free. Ideally we’ll try to encourage authors to seek out sufficient review before Last Call, but finding reviewers is a big job.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> point out their flaws

We certainly appreciate all the technical feedback you provide!

---

**Pandapip1** (2022-11-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Using Ethereum isn’t free. And using Ethereum is a reasonable requirement for telling other people how to improve Ethereum.

Counterexample: For various legal reasons, I don’t actually own any non-testnet Ethereum. I nonetheless hope that my EIPs and editing are helpful. At the very least, nobody has recently told me anything that suggests otherwise.

I’m actually more concerned about paid resources from a privacy perspective. You have to dox yourself to Paypal, a bank, the publisher, or perhaps even all of them to gain access to paid articles. I think we should not require mandatory self-doxxing to implement EIPs.

---

**poojaranjan** (2023-04-17):

PEEPanEIP #105: [EIP-5757: Process for Approving External Resources](https://youtu.be/3sL2VU2Cqmc) with [@SamWilsn](/u/samwilsn)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/9/9a74a71ffdc077f4bdd588ec5f9a0aa6b8054ac5.jpeg)](https://www.youtube.com/watch?v=3sL2VU2Cqmc)


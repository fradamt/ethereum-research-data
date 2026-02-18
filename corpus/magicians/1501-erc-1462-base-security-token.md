---
source: magicians
topic_id: 1501
title: "ERC-1462: Base Security Token"
author: xlab
date: "2018-10-01"
category: EIPs
tags: [security-token, erc-1066, erc-1400]
url: https://ethereum-magicians.org/t/erc-1462-base-security-token/1501
views: 6088
likes: 2
posts_count: 5
---

# ERC-1462: Base Security Token

Hi all,

I just finished working on a Base Security Token standard:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/1462)














####


      `master` ← `AtlantPlatform:master`




          opened 09:41PM - 30 Sep 18 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/1/1b741532a54c09f5a0a54979686132c6d60360c0.jpeg)
            xlab](https://github.com/xlab)



          [+117
            -0](https://github.com/ethereum/EIPs/pull/1462/files)







An extension to ERC-20 standard token that provides compliance with securities r[…](https://github.com/ethereum/EIPs/pull/1462)egulations and legal enforceability.

**Abstract**

This EIP defines a minimal set of additions to the default token standard such as [ERC-20](https://eips.ethereum.org/EIPS/eip-20), that allows for compliance with domestic and international legal requirements. Such requirements include KYC (Know Your Customer) and AML (Anti Money Laundering) regulations, and the ability to lock tokens for an account, and restrict them from transfer due to a legal dispute. Also the ability to attach additional legal documentation, in order to set up a dual-binding relationship between the token and off-chain legal entities.

The scope of this standard is being kept as narrow as possible to avoid restricting potential use-cases of this base security token. Any additional functionality and limitations not defined in this standard may be enforced on per-project basis.

**Join the discussion**

https://ethereum-magicians.org/t/erc-1462-base-security-token/1501












It is an extension to ERC-20 standard token that provides compliance with securities regulations and legal enforceability.

The scope of this standard is being kept as narrow as possible to avoid restricting potential use-cases of this base security token. Any additional functionality and limitations not defined in this standard may be enforced on per-project basis.

Please check out the EIP’s motivation section, which explains why we decided to invest the time and resources to publish something like that. We aim to fix the minimal set of features that each security token should have, so companies could start adopting it soon. We don’t agree that defining function names (i.e. establishing the technical part) requires a significant marketing effort.

Any questions are welcome! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

## Replies

**boris** (2018-10-01):

Good to see another ERC1066 user ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Now that there really are a handful of these – it would seem that you should all get together to work on improving a standard, rather than just keep publishing new ones?

Also: I disagree with the whole “must work with ERC20”. Or rather, the way most of these are (or should be) structured, they can layer on top of ERC20 or ERC777, rather than requiring one or the other.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xlab/48/886_2.png) xlab:

> Any additional functionality and limitations not defined in this standard may be enforced on per-project basis.

Or, defined in other EIPs, as they are composable and could be optional. Enforcement on a per project basis isn’t really a standard anymore.

I totally get that ERC20 was the first “standard” and that’s the one that people connect on to. But Exchanges are going to need to have upgraded technology regardless. If they can’t move on, then we have a much bigger problem.

I worked on security tokens starting about 18 months ago, along with [@expede](/u/expede) who is the author of 1066. It, along with ERC902 (which is basically your check function as a separate EIP). It was my belief then and still now that there is going to need to be broad technical interoperability, as well as regulatory interoperability.

To be clear – I’m just asking for info from you and wanting to have a discussion, as I’ve seen the 4th? 5th? proposal in the last couple of weeks ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

I’m not working on security tokens anymore and mainly just want to help people create high quality EIPs and work together to grow the ecosystem. Writing up multiple EIPs is the easy part – documentation, sample code, maybe even code for exchanges to implement is where all the hard part comes in.

cc [@AdamDossa](/u/adamdossa) from 1400 – any thoughts on working together? Or of the concerns raised?

---

**xlab** (2018-10-02):

Hi [@boris](/u/boris), thanks for your feedback.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Now that there really are a handful of these – it would seem that you should all get together to work on improving a standard, rather than just keep publishing new ones?

Each standard that appeared recently comes from a different background, originating from the companies that are formalising their experience in a form of EIP. I see that people agree, that there should be at least 2 ERC for security tokens, one for base and its extensions. So, it’s not just about improvement, it’s about splitting a big requirement into smaller parts, and one of those is ERC-1462, the base.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> I disagree with the whole “must work with ERC20”. Or rather, the way most of these are (or should be) structured, they can layer on top of ERC20 or ERC777, rather than requiring one or the other.

By providing compatibility with ERC20 and ERC777 interfaces we cover all existing tokens and all future coins. It is about function overriding, as long as we can override their functions the standard is applicable to any token. I put this requirement because ERC-1400 seemed to depend on ERC-777 heavily and I wanted to emphasise the the standard must support both, to be adopted. Could you clarify what “layer on top” means? Is it possible to live without overriding?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Or, defined in other EIPs, as they are composable and could be optional. Enforcement on a per project basis isn’t really a standard anymore.

This is what I always meant. However, if your token A should not be divisible because the security it represents is not divisible, that’s a project specific enforcement. Some people (EIP-1450) would put it as a general rule. I don’t think such specifics require any EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> But Exchanges are going to need to have upgraded technology regardless. If they can’t move on, then we have a much bigger problem.

The idea of this EIP is to be compatible with both, moreover, to provide guidelines how ti integrate with both, so it won’t force people to step into the future right now. It’s not limiting in any way. I didn’t put ERC-777 into the Simple Description because it’s still a Draft and is not a widely known thing (apart from ERC-20 that is an obvious thing).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> It, along with ERC902 (which is basically your check function as a separate EIP).

It’s not the same thing from perspective of the topic (a good explanation: [ERC-1404: Simple Restricted Token Standard · Issue #1404 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/1404#issuecomment-423002902)), but check functions that have been called surely could use an ERC902-based service. Any security token would look like a specific case of ERC902, but that’s where details matter the most, otherwise I wouldn’t spent 1500 words explaining a few simple functions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> It was my belief then and still now that there is going to need to be broad technical interoperability, as well as regulatory interoperability.

It’s hard to keep regulatory interoperability in the same EIP as the technical interoperability. The regulatory standards are hard to nail down, as there is too much discrepancy between jurisdictions, so it would slow down the adoption of technical part. I’m trying to fix the technical part for now (but keep it extensible), and regulatory interoperability standard may come later.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Writing up multiple EIPs is the easy part – documentation, sample code, maybe even code for exchanges to implement is where all the hard part comes in.

As long as writing an EIP is considered an easy task, and the ambiguity of EIP is compensated by providing a ton of sample code and additional documentation (wait, isn’t EIP a documentation?) we will have more and more EIPs coming, trying to fix the hole ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**AdamDossa** (2018-10-02):

[@boris](/u/boris) - agree we should def. all be working together - [@xlab](/u/xlab) is dialing into the community call today so we can share views over voice as well.

In terms of where / how adoption happens, I think a lot will be driven from exchanges and other key ecosystem participants - working on getting these types of organisations to engage in the conversation, although possibly they will have a strong preference for the status quo (aka ERC20) ;-).

---

**boris** (2018-10-02):

Thanks [@AdamDossa](/u/adamdossa) & [@xlab](/u/xlab), didn’t realize you had connected already. Really glad to see that this discussion is coming together!

I totally agree on keeping the regulatory stuff separate – that has been my point elsewhere!

I still think that over-focusing on ERC20 is a mistake – vs. pulling the bandaid off and getting broad movement to 777 along with standards like this – but as it’s not me that’s working on security tokens I’ll leave it up to you ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

As always, let me know how I can assist, and look forward to productive discussions in Prague!


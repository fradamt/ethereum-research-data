---
source: magicians
topic_id: 6488
title: Rework ERC process from EIPs
author: anett
date: "2021-06-15"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/rework-erc-process-from-eips/6488
views: 960
likes: 7
posts_count: 3
---

# Rework ERC process from EIPs

TL:DR if we are going to create ERC editor and whole process around it, let’s remake it completely and don’t try to just rebuild the EIP process as ERCs are different thing from EIPs.

ERCs are now days compared to EIPs and for the most people they seems similar to EIPs.

I personally feel like ERCs should be probably renamed and the structure redirected / delegated

on creating more of a list / wiki / technical documentation alike source for dApp devs. ERCs should be seen as technical documentation of how solidity & Smart Contracts functions works. ERCs are defining how something could work, when building dApp developer basically just puts together a couple of solidity contracts together which some of them are documented as ERCs, adds bits of solidity coding and that’s how the dApps are being built

I mean that ERCs are more of a documentation and we should not push ERCs to be  in Final. ERCs are not EIPs, ERCs deserves a better naming, better sorting and documented better. Ethereum Devs deserves to be aware of the ERCs as technical documents which could help them build projects.

I noticed initiative brought by [Ethereum Cat Herders of separating ERCs from EIPs](https://github.com/ethereum-cat-herders/EIPIP/issues/61) in the [ethereum/eips](https://github.com/ethereum/EIPs) repo. I do support separation of ERCs from EIPs, but if there is going to be allocated someone to do the work of separating ERCs from EIPs why the work needs to be done the same as it is with Protocol layer standards? Protocol Layer Standards - EIPs needs to have its formalised process but ERCs don’t need to go through [the same approval process](https://eips.ethereum.org/EIPS/eip-1).

I do think that ERCs deservers to be understood and marketed differently, they are different so why we should apply the [same process to ERCs](https://hackmd.io/@poojaranjan/ERC-Process) than we do to EIPs? I’m not a fan of pushing ERCs to go to “final” status as the final status does not really tells us anything about the standard. A Solidity function, a feature, documenting how something could be implemented does not need to be implemented on Ethereum chain, all it needs to is to be used by developers and implemented into a projects.

I’m happy to work out this proposal more and outline the process for ERCs.

Encouraging Ethereum Devs to share your ideas on what do you think about ERCs, and how would you change this process.

## Replies

**matt** (2021-06-15):

*tldr; I think the ERC process is okay, the EIP process should be overhauled, and more people need to proactively guide and discuss ERC standards*

–

It seems like there is a misconception here, probably because how convoluted the process EIPs follow now is.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anett/48/3020_2.png) anett:

> I’m not a fan of pushing ERCs to go to “final” status as the final status does not really tells us anything about the standard.

Originally, *final* meant that an EIP was on mainnet and was therefore unable to be changed further. This obviously doesn’t make sense for ERCs because we don’t have an equivalent consensus mechanism as “it’s on mainnet”. The simple deployment of a standard should not be enough to solidify the standard–in fact, this behaviour should really be frowned upon as it can unfairly push a standard to final before consensus on certain issues is reached.

However, as of some time in 2020, this isn’t what “final” means in the EIP repository. Final means the standard is *final* and will not be changed further, except for nonnormative changes. It may have very little chance of ever going into a hardfork.

I’m in favor of keeping the ERC process similar to now. I actually think this new process of focusing on the *standard* rather than the *governance* makes a lot of sense for ERCs. It’s actually EIPs that I’d like to see be [treated differently](https://ethereum-magicians.org/t/replace-the-yellow-paper-with-executable-markdown-specification/6430). I don’t think enough people are involved in core development to sustain such a fragmented process. I’d rather governance and core EIPs go hand-in-hand. Having “final” EIPs that have very little chance of going to mainnet is not useful, and may even just suck bandwidth from people whose bandwidth is already severely limited. This isn’t to say that people aren’t welcome to bring their core changes and iterate on them until they feel they’re “final”. We’re an open ecosystem and this is always an option. But generally, core developers will make minor tweaks to proposals that are accepted. Making your EIP final before release on mainnet is imminent is not productive.

We’re getting off track.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anett/48/3020_2.png) anett:

> EIPs needs to have its formalised process but ERCs don’t need to go through the same approval process.

I disagree. I think it’s also important to build strong, universally accepted standards in ERCs. I think we’re in a place today where the top 1-3 projects have substantial control over what “standards” are in place on Ethereum. If Uniswap decided it would support a new ERC-20 incompatible token, the community would scramble to add support.

I feel like the ERC space is too reactive. Most people/teams react to immediate needs, rather than consider future desires. I would really like to see some people in the space [step up and help lead](https://trac.ietf.org/trac/wgchairs/) the discussions on how to improve smart contract standards. Are we really going to just accept ERC-20 compatibility as absolute?

Thank you [@anett](/u/anett) for raising this. I do agree, ERCs are very different from EIPs!

---

**wschwab** (2021-06-20):

A thought I keep on coming back to is encouraging ecosystem interaction in ERCs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> If Uniswap decided it would support a new ERC-20 incompatible token, the community would scramble to add support.

Yes, but it would be nice if they would at least release it as an ERC first. Uniswap released NFTs with `permit` in their v3, I wish they would’ve taken the time to ERC it. That would at least allow for ecosystem review/conversation before it’s out in the wild.

fwiw, I also would push to keep “Final” for ERCs, I feel like we need to figure out why so few make it there. Is it because of a lack of incentive? It does make it hard to tell the difference between a low- and high- quality ERC when even high-quality ERCs with traction are sometimes still in “Draft”.


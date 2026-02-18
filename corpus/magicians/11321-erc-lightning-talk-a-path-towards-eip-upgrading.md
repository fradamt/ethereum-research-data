---
source: magicians
topic_id: 11321
title: "ERC lightning talk: A path towards EIP upgrading"
author: TimDaub
date: "2022-10-14"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/erc-lightning-talk-a-path-towards-eip-upgrading/11321
views: 1523
likes: 11
posts_count: 5
---

# ERC lightning talk: A path towards EIP upgrading

# ERC lightning talks at Devcon in Bogota

[![Screenshot from 2022-10-14 10-18-02](https://ethereum-magicians.org/uploads/default/original/2X/5/5217f253475f935028702c7de5a980b3760b2813.jpeg)Screenshot from 2022-10-14 10-18-021081×763 59.6 KB](https://ethereum-magicians.org/uploads/default/5217f253475f935028702c7de5a980b3760b2813)

In this post, I will outline a technique for upgrading existing ERC standard documents through addition. I’m specifically going to talk about Ethereum’s most famous NFT standard, EIP-721, and how notable projects and authors in the ETH Magicians community attempt to enrich it with functionality.

But let me prefix this post by being clear about what types of EIPs I’m talking about, namely “Ethereum Requests (for) Comments” (short: ERCs) and NOT Core EIPs touching the Ethereum consensus layer.

[![Screenshot from 2022-10-13 22-42-05](https://ethereum-magicians.org/uploads/default/optimized/2X/0/0e85893c787ac908bec190081901115b81b2b802_2_690x491.png)Screenshot from 2022-10-13 22-42-051078×768 217 KB](https://ethereum-magicians.org/uploads/default/0e85893c787ac908bec190081901115b81b2b802)

My intention with writing this post is twofold: For one, it’s a personal exercise to clarify my thinking about a lightning talk I will give tomorrow at Devcon in Bogota. But secondarily, and that’s more important, I want to motivate fellow ETH Magicians to engage and to understand how the process works and what opportunities it may open. So let me start by describing the EIP process at first, as I feel it’s important to be well-understood.

## ERCs enable permissionless standardization around composability

While many developers may generally be familiar with the idea of standardization and its effects, which essentially create broad composability, having been contributing to the ETH Magicians for a while now, I feel that it’s not obvious to many what the qualities of the process really are.

[![Screenshot from 2022-10-13 19-00-00](https://ethereum-magicians.org/uploads/default/optimized/2X/3/3ba66a6878d5922da65f3930571730a67e043b07_2_690x258.png)Screenshot from 2022-10-13 19-00-001267×475 201 KB](https://ethereum-magicians.org/uploads/default/3ba66a6878d5922da65f3930571730a67e043b07)

It’s when I often hear developers scold the idea of permissionless standardization around documents and that it generally leads to a hot mess of inconsistent proposals. In that vein, you might have heard people ranting about EIP-2612 being infamously inconsistent with many implementations in production or that EIP-721 has many pitfalls which lead to broad non-compliance.

[![Screenshot from 2022-10-13 23-04-20](https://ethereum-magicians.org/uploads/default/optimized/2X/4/4b6d6826cbf3adcba49f89e4cc200026bd285a25_2_532x500.png)Screenshot from 2022-10-13 23-04-20728×684 70.2 KB](https://ethereum-magicians.org/uploads/default/4b6d6826cbf3adcba49f89e4cc200026bd285a25)

But even with all these drawbacks in mind, I still think there is beauty in Ethereum’s standardization process: Namely that it’s open to anyone or free of excessive gatekeeping. That it rejects off-channel power structures, and that frankly, judging from a personal experience, it is probably the most potent due diligence mechanism available to the regular developer for turbocharging their ideas.

When I first submitted EIP-4973, I was amazed by the level of commitment and effort other Magicians were putting into reviewing and improving my work. Today, albeit controversially discussed, EIP-4973 is among the top 10 viewed threads on the forum and actually the one that received the most comments this year. Without them, and this I can say with confidence, what the standard embodies today wouldn’t have been possible, and instead of the creative composition of consensual minting, we probably just would have gotten bland NTTs and not a consensual minting interface for Soulbound tokens.

[![Screenshot from 2022-10-13 17-03-12](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5b06ba815e0f650ad091c768817c4d9a0577429d_2_690x405.jpeg)Screenshot from 2022-10-13 17-03-121517×891 166 KB](https://ethereum-magicians.org/uploads/default/5b06ba815e0f650ad091c768817c4d9a0577429d)

So there’s something to be said about simply exposing your non-standardized idea to this community, and then it may or may not become a canonical interface in the future, but the feedback one receives from the Magicians in the intermediate can also be tremendously valuable.

## The EIP process’s greatest weakness (and strength)

But in any case, I’ve said that I wanted to outline the process’s functioning, and I’ll admit I’ve gone on somewhat of a tangent. It was important for me to highlight: Participating in the EIP process can be valuable even without a clear intention towards standardizing a certain thing.

But it’s equally important that while other standard outcomes like, e.g., those from the W3C, the Python community, or the Ethereum core devs might become “facts” after their respective communities find consensus, for Ethereum’s ERC process: That isn’t truly the case. And just to make that clear for the potentially uninitiated: the status “final” on an ERC isn’t really meant to say anything about that document’s power or mandate. It may be adopted now by developers in their smart contracts - or it won’t.

[![image](https://ethereum-magicians.org/uploads/default/original/2X/4/41c35c9930a9715e1406f2a4940724aa59f84693.png)image500×283 22.5 KB](https://ethereum-magicians.org/uploads/default/41c35c9930a9715e1406f2a4940724aa59f84693)

And while many believe this to be the greatest flaw of that process, and believe me, and I’ve seen people being desperate about it: I still think that this property of a more market-based adoption dynamic is actually the ERC process’s greatest strength too.

See, an EIP with the status final means very little except for a few important properties: For one: It means that the document is now permanently immutably stored at github:ethereum/EIPs, and so all those that need the guarantee to rely on its interfaces may do so confidently. The status “final” also means that a minimum-viable due diligence process has happened and that these documents comply with a specific and expectable format. However, an ERC proposal’s status “final” doesn’t mean that the document is somehow authoritative or that it represents a consensus. And to me, that’s a feature - not a bug.

## Adoption continuous consensus is a stronger signal than expert committee consensus

And so, finally, I wanna make the difficult argument for why I believe it is more indicative of wide ranging consensus and the proposal’s quality when I say that the gradual adoption of ERC standards over time is more meaningfully telling as a due diligence process than spontaneous consensus of an expert or stakeholder committee.

In fact, a hacky prove of this is capitalism itself, where although most inter-corporation decisions are taken by an expert committee, I think most of us would agree that betting on a market’s overall performance and hence market-based curation is a superior strategy for receiving innovation over the long term.

My argument is this: Having numerous developers implement an ERC standard gradually and over time means that each of them is making an independent qualitative judgment towards adopting a standard into their app. It’s a stronger signal than that of a group spontaneously agreeing, as a group’s social dynamics may make members being swayed into a certain direction of dependence over shorter periods.

[![Screenshot from 2022-10-13 23-00-23](https://ethereum-magicians.org/uploads/default/optimized/2X/f/f76510b98721e2ae08a3ee8d820aa602b55373d3_2_690x491.png)Screenshot from 2022-10-13 23-00-231078×768 243 KB](https://ethereum-magicians.org/uploads/default/f76510b98721e2ae08a3ee8d820aa602b55373d3)

And this is something we’ve probably all experienced once in coming to a social consensus, namely that in a group-decision situation, when we may find it difficult to object or exit, although our internal choice was clear. We wanted something else, but we submitted to the group’s choice.

It may sound almost too trivial, but having everyone decide by themselves rather than having some being swayed through social pressure will, in my opinion, leads to a stronger outcome simply because it’s more rational, as in " there’s a more accurate “ratio” of all members’ choices represented in a given decision.

And although I can only speculate about this, I believe that it may be the case for why our food supply network, our markets, and other highly critical societal structures are fundamentally based on decentralization, individuals’ stakes, emergent consensus, market-driven adoption - and not central expert planning committees.

## Does immutability mean stagnation?

Still, if we choose to listen to immutability and anarchy pessimists, we may hear that the ERC process is broken, cannot be fixed, and that even its most used documents are almost worthless in the face of progress. Does immutability mean stagnation and hence eventual non-compliance and fragmentation of interfaces?

Also: Are ERC standards upgradable? Or will we have to live with EIP-721 forever? Like we do with Email.

It’s not an accident that I’m asking myself this question. As I had mentioned earlier in this post, that with EIP-4973 and EIP-5192 at the beginning of this year, I saw a need to upgrade standard NFTs since their bias towards private property - well, it just didn’t work with what I wanted to achieve, namely Harberger NFTs.

So I made a choice: Similar to ERC-1155, I could have paved my own path and re-specified an entirely new token standard. But that seemed unnecessary and impractical. And for my clients - I’m a freelancer - it also seemed not a great path towards adoption and ecosystem development.

And so we kind of did what I’ve tried to express in the first picture of this article. On EIP-721, a locked standard, we essentially bolted an optional extension to make tokens:

- Soulbound with EIP-5192
- and to enable consensual minting with EIP-4973.

[![Screenshot from 2022-10-13 23-40-03](https://ethereum-magicians.org/uploads/default/optimized/2X/f/ffff92e7627f1f2fdabcea2a8906f78a3ca48d95_2_690x463.png)Screenshot from 2022-10-13 23-40-03888×597 196 KB](https://ethereum-magicians.org/uploads/default/ffff92e7627f1f2fdabcea2a8906f78a3ca48d95)

Since then, or rather in the meantime, other magicians have also sprung into action and bolted on some optional, backward-compatible, and interesting proposals.

[![Screenshot from 2022-10-14 11-24-04](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8cfbba64b76fee50364ec944a76a082cfde53f2c_2_690x487.png)Screenshot from 2022-10-14 11-24-041081×763 214 KB](https://ethereum-magicians.org/uploads/default/8cfbba64b76fee50364ec944a76a082cfde53f2c)

Most notably:

- EIP-5679 adds canonical minting and burning to EIP-721
- EIP-4906 adds an optional event to signal a metadata update to NFT indexers
EIP-4907 differentiates between “user” roles and “owners”
- EIP-2981 infamously adds optional royalties

But these are just a few cherry-picked examples of the recent Cambrian explosion of innovation around EIP-721. It’s as if people had suddenly recognized the power of the EIP process and their chance to participate in the long-term lottery of continuous and emergent innovation and composability.

Although I’m frequently hearing many being disappointed about the process, I personally couldn’t be more bullish, and I think our work today will be looked at as fundamental to a newly emergent property class pioneered on the Ethereum blockchain and enabled by the diligent Magicians.

## Replies

**TimDaub** (2022-10-15):

Recording of today’s lightning talks (link with timestamp): [Devcon VI Bogotá | Workshop 3 - Day 4 - YouTube](https://youtu.be/5lvmFHvcMLY?t=12392)

---

**xinbenlv** (2022-10-15):

This great sharing. Very inspring

---

**devinaconley** (2022-10-20):

Nice writeup and overview on this problem [@TimDaub](/u/timdaub) – I was coincidentally thinking about this earlier and dumped some thoughts here

https://twitter.com/devinaconley/status/1583205293126668289

---

**xinbenlv** (2022-12-01):

High five. a like-mind here! [@devinaconley](/u/devinaconley)

Check out EIP-5750 for Method extensibility, one of the piece that might be helpful in achiving the vision your tweet described!


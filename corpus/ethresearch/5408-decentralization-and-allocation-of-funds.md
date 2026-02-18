---
source: ethresearch
topic_id: 5408
title: Decentralization and Allocation of Funds
author: wschwab
date: "2019-05-03"
category: Economics
tags: []
url: https://ethresear.ch/t/decentralization-and-allocation-of-funds/5408
views: 1605
likes: 6
posts_count: 4
---

# Decentralization and Allocation of Funds

There is an economic problem at the heart of decentralized economies that has caught my attention for some time. This is an attempt to articulate it. My apologies if this is self-evident or redundant. I myself believe it to contain many self-evident truths, but still to present a novel problem.

Capitalist economy is based on the assumption that the players in an economy will optimize their profits. The reason why a firm creates a product is in order to generate as much profit as possible from it. Consumers will strive to pay less in order to maximize their own profit (in technical terms, to maximize their utility per unit paid).

In such an economy open-source software presents a bit of a problem. The problem is not just merely that open-source generally does not produce much by way of profit, especially when compared to proprietary code (compare Red Hat and Windows). It is also that open-source code is often of higher quality and therefore more desirable. There are two technical reasons for this: the code can be reviewed by more experts, and also there is more access to professional and specialist contribution. We therefore arise at a bit of a paradox. The public wants open-source, but will pay more for proprietary.

We’re not going to discuss *why* the public doesn’t pay for open-source. I’m not qualified, for one. It may simply be a tragedy of the commons, for another.

This problem is particularly poignant in blockchain/cryptocurrency. One is the poignancy of this paradox on any cryptography software. Software that secures money and other liberties is of a more mission-critical nature, and we need it to be of the highest quality possible. But we still don’t want to pay for it. If a firm develops a cryptographic algorithm and implementation, they should want to keep it proprietary to maximize profit, but then we’d lose community review. Of equal importance, two new attack vectors open up. One is that the firm may be malicious, and the other is that the firm can be bribed. Since no one sees the code, no one is the wiser.

(Recommended reading: Matthew Green on the NSA probably bribing a backdoor into RSA.)

Another cause for concern in the blockchain space in general is the ease with which the need to profit can enter at the protocol level. If we were to conceive of a blockchain voting platform (without debating if it’s a good idea to put voting on the blockchain), we would likely abstract a system in which accounts (likely verified accounts) can transfer a valueless token or signal some data or the like. Who will create this platform, though? How are they providing for themselves while they write it? The second the writer needs or wants to generate revenue by writing this software (which is a basic capitalist economic theory), instead of charging for the platform (and needing to make the code proprietary or creating a SaaS model), he could insert a token into the system which can have value, and then speculate on the value.

It is my personal opinion that this is a devil’s deal. The devil sells it by saying that the code remains open-source and reviewed, and therefore maintains the quality of open-source software. This is the devil talking, though. It’s true that the code is open-source, but the protocol has been perverted. Instead of the protocol being optimized for efficiency, usability and security, it will now be also optimized for speculation.

This is true not only of applications on the blockchain, but also of the actual blockchains themselves. Ethereum is supposed to be part of a larger system including Whisper and Swarm, two amazingly important projects. They don’t move as quickly as Ethereum, though, and it could very will stand to reason that it is because they do not carry the same economic incentives. How are we supposed to incentivize their development without compromising their quality?

(As a side note, one of the common models that’s emerged from very successful open-source projects is that they’re developed by firms that don’t need revenue from them. Open sourcing these frameworks, such as Kubernetes or React, allows them to grow in quality, assuring that their producers benefit from a higher-quality product while in turn paying less for their development, and also help their image.)

The general model in macroeconomics these days is that the government acts as a non-profit entity that stimulates the economy. The government pays for public works and can create subsidies and/or tax breaks to halt recessions. There has been talk around a portion of block rewards going to the Ethereum Foundation for development purposes. I would argue that this is the same concept of government funding for public works. (I’ve daydreamed that an IRL government policy of budgeting contributions to open-source would be very beneficial to privacy, security, and the efficiency of programming at large.) This brings its own problems, though. Who decides where this money is going? Well, the Foundation. This introduces and attack vector of gaming the Foundation for unearned money. It is this author’s very strong opinion that putting the money in a DAO won’t help. Instead of gaming the humans in the Foundation, the attack vector becomes gaming either the user accounts of the DAO or the code of the DAO itself. In other words, creating a public-works fund for developing the platform or developing on it necessarily creates a governance bottleneck. Someone or something is deciding who and what gets how much funding. Is this the decentralized utopia we want?

In summary: If we want quality, quick progress on blockchain platforms and dApps, they should be well-funded and/or profitable, and open-source, and it’s not clear how to accomplish that.

I wanted to ask the community their thoughts on this. Are there funding models that I’ve ignored? Are there any other thoughts about how to otherwise fund the decentralization of the web?

## Replies

**quickBlocks** (2019-05-03):

Wow. You’ve articulated so many very important issues here. Welcome, thanks for your first post, and to be honest, there was no need to apologize. I agree with nearly every word you say, and the way you say it is well articulated.

I too think the ‘token’ model is a devil’s deal. Although for some tokens (Bitcoin, Ethereum, others), it’s not. With these examples two important things happened: (1) the open source code was given away as a gift to the world, and (2) the cost of the system is borne equally by all participants. When a new bitcoin comes into existence, the lowering of value for every participant is exactly the same percentage relative to their holdings as all the other participants. If there are privileged participants in the system who benefit from either lower cost for their participation (excluding genesis) or the opportunity to benefit disproportionally, then, that’s the devil. The trouble with governance is that it presents an opportunity for some people (the governors or the people they know) to benefit disproportionally.

I wish your post (and mine) would have ended with a “…and here’s how we can solve this problem,” but I guess that’s what this community is all about.

---

**sbaks0820** (2019-05-20):

I think there’s a distinction needed for where a token-based system may not be the devil. In some cases, it’s necessary to be able to burn/mint new tokens (for whatever purpose they serve) that otherwise isn’t possible with just ether.

Sure you can burn Ether, but any successful project that is burning (i.e. locking away a large amounts of ether) isn’t going to be looked upon favorably by the community. One can imagine a project where stakers are penalized by losing their deposit. The project can claim the lost funds for themselves, but it’s distasteful.

For the other group of projects that are token-based for no other reason than to make some money, you would hope that someone out there forks the codebase, removes the token and publishes the contract to the blockchain. The cost of doing so is not trivial but isn’t impossible given the state of open-source development. After that maintenance are very low. This is scenario isn’t that well-formed because it generally hasn’t happened. iirc etherdelta had something like this happen where forkdelta was created by community members. Either way, I think such projects are harder to make popular in the post-ico-every-week world.

---

**Econymous** (2019-05-20):

The best way I can respond to this post is with a video.

This is an extremely controversial approach, but it’s worth fellow researchers testing it on ropsten.


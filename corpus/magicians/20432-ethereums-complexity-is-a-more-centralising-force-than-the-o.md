---
source: magicians
topic_id: 20432
title: Ethereum's complexity is a more centralising force than the OG web
author: luke
date: "2024-07-02"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/ethereums-complexity-is-a-more-centralising-force-than-the-og-web/20432
views: 672
likes: 6
posts_count: 6
---

# Ethereum's complexity is a more centralising force than the OG web

Dear community,

As an experienced (aging) programmer trying to work with Ethereum, I’d like to share some disillusionment creeping in today. I feel very thankful for the people who work so hard on libraries and OS projects, though ideally I should be able to code this all myself with a smile.

I’ve previously expressed concerns about the quality of writing (and thus, also review) in EIPs, but today the content itself is the cause of my concern.

Today, I find myself particularly despondent contemplating whether Ethereum can really be the future of software in the way HTTP became the future in 1989; HyperText was fundamentally text based and extensible, and therefore a joy from day one, while Ethereum feels like a stack of workarounds that may rapidly become untenable.

Compared to the elegance and adaptability of the original web protocols, I find Ethereum esoteric and increasingly difficult to grasp, i.e. getting tougher, especially since Account Abstraction. The nature of the blockchain is challenging enough but the compounding complexity makes the system an almost vertical climb for newcomers and exhausting for experienced developers.

The core problem with Ethereum seems to be rooted in the protocol’s lack of extensibility. I wonder if the decision to use RLP for message encoding, rather than a more flexible self-describing format that can better tolerate the unknowable, has led to spiralling complications. Each EIP reads like a trick way to get around some past decision and together they resemble a tower of hacks to sniff bytes, wrap payloads within payloads and dodge bullets with binary.

Importantly, each hack necessitates burdensome code that must be added, tested and maintained in apps, and this pain drives people to centralised libraries and service providers. I think nothing of preparing and shooting off my own HTTP requests, but I’ll happily pay a service to prepare and send a transaction or user operation. This situation is the very antithesis of Ethereum’s values. It’s a more centralising force than the original web and we’ll see giant companies who’s value is pain relief.

This situation appears to stem from an extreme application of the YAGNI principle. I’m sympathetic that blockchains are severely resource constrained, but do we see this situation as permanent or will there come a time when the trade offs change and it can be reconceptualised? YAGNI is fine for private app code, but does it apply here? When designing the future of all connected software, you probably are going to need a lot of things that evade your imagination right now.

Each improvement prioritises efficiency and frugality, apparently even in its writing, and I rarely read a discussion about how the proposal can be extended or could handle some hypothetical cases. Given that we now have a good idea of just how often “we do need it”, an Extensibility section might be a prudent mandatory addition to EIPs. Another useful section would be a Realworld Integration Example which would add much needed concretion to the abstract terminology and help it all “click” for people.

Today, Ethereum’s EIP quagmire feels too much like a “high WTFs per hour” codebase where team-mates churn due to years of untackled debt which repels the very people needed to reform it. As such, I also feel a Developer Pain section might also help authors think through the impact of their improvement on everyone else. This brings me back to the selfish writing: time saved by a few authors is time stolen from many thousands of readers. That must change.

I’m curious about the community’s thoughts on balancing efficiency with extensibility in protocol design, and how Ethereum might evolve to address these challenges. As it stands, it is a slog.

I am deeply concerned that it will ultimately prove too steep and too rough going to cross the chasm unless the developer experience is radically improved, without libraries and SaaS companies.

“An important scientific innovation rarely makes its way by gradually winning over and converting its opponents: it rarely happens that [Saul becomes Paul](https://en.wikipedia.org/wiki/Conversion_of_Paul_the_Apostle). What does happen is that its opponents gradually die out, and that the growing generation is familiarized with the ideas from the beginning: another instance of the fact that the future lies with the youth.” — Max Planck

I’ve not yet come across this in software. New ways frequently win over and convert. Software developers are insatiably curious and tend to relish learning new things. Yet with blockchain, I don’t see the excitement shared among my IRL peers. It’s eerie. I can’t tell if I’m on the bleeding edge or if it’s because no one else is coming.

I had my doubt today because I was unable to be productive. Without productivity life is stressful, I feel like a loser, lonely, and I wonder if I am making a mistake going down this path.

Then I reach the for $$$ painkillers.

Sincerely,

Luke Puplett

## Replies

**mratsim** (2024-07-02):

I’ve read your previous criticism of [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337) at [Complaint - quality of writing in EIP-4337](https://ethereum-magicians.org/t/complaint-quality-of-writing-in-eip-4337/18910)

What are you looking for in an EIP/ERC? The main target of ERCs are implementers, to make sure it’s obvious and clear how to conform to a standard.

You can use this as a reference to frame what you would like to see more in EIPs/ERCs; [About | Divio Documentation](https://docs.divio.com/documentation-system/) especially this table

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c5af8c526a8a35a57430446974ef4639ceb16a5d_2_550x500.png)image966×878 136 KB](https://ethereum-magicians.org/uploads/default/c5af8c526a8a35a57430446974ef4639ceb16a5d)

> Today, I find myself particularly despondent contemplating whether Ethereum can really be the future of software in the way HTTP became the future in 1989; HyperText was fundamentally text based and extensible, and therefore a joy from day one, while Ethereum feels like a stack of workarounds that may rapidly become untenable.

> Compared to the elegance and adaptability of the original web protocols, I find Ethereum esoteric and increasingly difficult to grasp, i.e. getting tougher, especially since Account Abstraction. The nature of the blockchain is challenging enough but the compounding complexity makes the system an almost vertical climb for newcomers and exhausting for experienced developers.

I disagree with this, I see seldom people even devs understanding the intricacies of TCP/IP, the TLS state machine, DNS, BGP, the OSI layers. Even if we stay just at the presentation layer, very few people understand what goes into a V8 JIT engine, the pile of React/Angular in the app, the caching in Akamai/Cloudflare and what not.

> The core problem with Ethereum seems to be rooted in the protocol’s lack of extensibility. I wonder if the decision to use RLP for message encoding, rather than a more flexible self-describing format that can better tolerate the unknowable, has led to spiralling complications. Each EIP reads like a trick way to get around some past decision and together they resemble a tower of hacks to sniff bytes, wrap payloads within payloads and dodge bullets with binary.

RLP is self-describing instead of being schema-based or protocol-based. And it has been ditched from the consensus layer because self-describing are a waste of the most previous resource in blockchain, storage.

> Importantly, each hack necessitates burdensome code that must be added, tested and maintained in apps, and this pain drives people to centralised libraries and service providers. I think nothing of preparing and shooting off my own HTTP requests, but I’ll happily pay a service to prepare and send a transaction or user operation. This situation is the very antithesis of Ethereum’s values. It’s a more centralising force than the original web and we’ll see giant companies who’s value is pain relief.

Do you have something in mind? Because EIPs are the burden of client teams which today are all open-source. ERCs are standards for interop between all industry players and having them promote the creation of open libraries instead of walled gardens.

> This situation appears to stem from an extreme application of the YAGNI principle. I’m sympathetic that blockchains are severely resource constrained, but do we see this situation as permanent or will there come a time when the trade offs change and it can be reconceptualised? YAGNI is fine for private app code, but does it apply here? When designing the future of all connected software, you probably are going to need a lot of things that evade your imagination right now.

What are you referring to here? All EIPs need a champion or they won’t even get at the starting line. And even with strong advocates they might get delayed. See EIP-2537 for example.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/luke/48/11841_2.png) luke:

> Each improvement prioritises efficiency and frugality, apparently even in its writing, and I rarely read a discussion about how the proposal can be extended or could handle some hypothetical cases. Given that we now have a good idea of just how often “we do need it”, an Extensibility section might be a prudent mandatory addition to EIPs. Another useful section would be a Realworld Integration Example which would add much needed concretion to the abstract terminology and help it all “click” for people.

ERC-4337 is one of the rare proposal with a diagram flow:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/d/de0c8988dfde4fa7831fc635450d6e1a87202b8b_2_469x500.png)image633×674 32.9 KB](https://ethereum-magicians.org/uploads/default/de0c8988dfde4fa7831fc635450d6e1a87202b8b)

For EIPs, they usually require a reference implementation along the proposal so people can evaluate the implementation risk and complexity as well, many of the prototypes are available in [GitHub - ethereum/research](https://github.com/ethereum/research) for those proposed by the EF itself.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/luke/48/11841_2.png) luke:

> Today, Ethereum’s EIP quagmire feels too much like a “high WTFs per hour” codebase where team-mates churn due to years of untackled debt which repels the very people needed to reform it. As such, I also feel a Developer Pain section might also help authors think through the impact of their improvement on everyone else. This brings me back to the selfish writing: time saved by a few authors is time stolen from many thousands of readers. That must change.

Each EIP refers to this exact forum for discussion and clarification. When that discussion happens behind closed doors people complain that it’s not public, when it’s public, people complain that it needs to be refined and it steals time from people, despite being in draft. What do you prefer?

People rely on debt, you can’t produce software of that complexity without iterative improvement and deprecation, you would invalidate billions of dollars of hardwork otherwise.

> I’m curious about the community’s thoughts on balancing efficiency with extensibility in protocol design, and how Ethereum might evolve to address these challenges. As it stands, it is a slog.

Ethereum seems to have the best balance of activity and extensibility as a protocol, but I may very well be biaised. What other protocols are you thinking of?

---

**luke** (2024-07-02):

Thank you for your time in reading and addressing my thoughts. I am an applications developer. I happen to be from a IT background so I’m unusual in understanding the OSI model, but that’s a coincidence and I agree that, surprisingly, most developers don’t know how much about the stack beneath them.

However, unless mistaken, the equivalent to a HTTP request in Ethereum is the transaction and now the user operation. These protocols run over TCP/IP which allows developers to not have to understand anymore beyond the abstraction of HTTP APIs in JS, Java, .NET etc. since those abstractions are not leaky. But unless I’m wrong, Ethereum and HTTP are equivalent.

Ethereum has a node and mempool which is akin to an TCP listener on port 80 and a request queue.

It is easy to make an HTTP request, and it is easy to comprehend the response, and to look up the status codes. It is a simple design. Ethereum was a simple design until the user operation came along.

By the way, this isn’t really about HTTP vs Ethereum, it is about Ethereum’s original design not tolerating change well, due to trade offs, and that those trade offs could be revisited some day, much as we now have HTTP/3.

Then there are the EIPs, which are almost entirely protocols. They’re akin to e.g. OAuth. And this is where a gulf opens up; the OAuth specification is beautifully written, including ASCII diagrams, and the platform it is running on is far more extensible in the first place allowing for an elegant design. I have never in 27 years read an IETF document that felt like a rushed load of hacks or that is was bending what was put in place before it, e.g. wrapping bytes and sticking magic numbers on the end.

The difference in quality is irrefutable, and repudiation is not helpful for me or anyone else. We cannot solve a problem we’re unwilling to have. I’m switching to “we” because I count myself as an Ethereum developer, even though I have barely penetrated it in years of studying.

Perhaps Ethereum is moving faster than the original web, but I think it is accumulating debt.

As an applications developer, simply trying to implement “login” with a wallet is impossible, and no help is forthcoming.



      [ethereum.stackexchange.com](https://ethereum.stackexchange.com/questions/164479/sign-in-with-ethereum-and-account-abstraction)



      [![Luke Puplett](https://ethereum-magicians.org/uploads/default/original/2X/c/c782b421cea1badfae5c436bb310c8cc42b38803.jpeg)](https://ethereum.stackexchange.com/users/91773/luke-puplett)

####

  **account-abstraction**

  asked by

  [Luke Puplett](https://ethereum.stackexchange.com/users/91773/luke-puplett)
  on [04:30PM - 01 Jul 24 UTC](https://ethereum.stackexchange.com/questions/164479/sign-in-with-ethereum-and-account-abstraction)










It seems that a simple login requires me to wade through obscure and poorly written technical documents that, according to your reply, I have no place reading or criticising! And each document requires reading even more, all the way down.

Do you see the problem? There’s no elegant abstraction, it drags me down all the way to the mempool and bundlers and UDP.

So, we either fix the abstraction, or we fix the technical writing, and make sure protocols are extensible and don’t leak and pollute and burden the layers above, i.e. make it so painful for the busy applications developers that they prefer to just pay a company to take the pain away.

Trust me, the way it’s going, two currently well known crypto companies will be the biggest companies the world.

–

An additional point: neither ABI not RLP are self-describing. You say “self-describing are a waste of the most previous resource in blockchain, storage.” (precious) but this is indeed my point about trade-offs and the ramifications and binary fudges reaching millions of applications developers in the way I’ve described above.

And that’s my point about revisiting these decisions some day, because they’re unforgiving and so they demand very considered non-YAGNI design. YAGNI is for applications developers using extensible formats and schemaless databases who tack a new field on without breaking anything.

---

**nutherone** (2024-07-08):

I don’t mean to distract, but perhaps offer some context.

This thread came across my feed today and I sympathize with the OP.

When I wanted to build an Ethereum app that promotes autonomy and sovereignty while mitigating the risk of censorship I was forced into a javascript stack that’s vulnerable to simple exploits (CVE-2024-37890) and depended on 3rd parties to validate transactions or do simple error checking. From the outside looking in we can easily perceive Etherscan and Infura as a cartel.

When I dug deeper I was slightly overwhelmed with the complexity and the history. It does feel like a bundle of duck tape compared to other open source projects and seems to choose the easy way at each turn. I might have falsely assumed Ethereum’s goal was to be the TCP/IP of value. It’s development path looks more like a video game where each feature introduces more bugs ![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=12)

If Ethereum’s values were aligned with decentralization and individual autonomy it seems to have veered off the path.

---

**matt** (2024-07-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/luke/48/11841_2.png) luke:

> It seems that a simple login requires me to wade through obscure and poorly written technical documents that, according to your reply, I have no place reading or criticising! And each document requires reading even more, all the way down.
>
>
> Do you see the problem? There’s no elegant abstraction, it drags me down all the way to the mempool and bundlers and UDP.
>
>
> So, we either fix the abstraction, or we fix the technical writing, and make sure protocols are extensible and don’t leak and pollute and burden the layers above, i.e. make it so painful for the busy applications developers that they prefer to just pay a company to take the pain away.

I empathize with your frustration. Most of the documentation in the space is not to the level we would like. However, I think you may have some knowledge gaps here if your take away is that validating a signature against a smart contract wallet requires a user op, mempools, or bundlers.

EIP-1271 `isValidSignature(..)` can be executed off chain with an RPC call like `eth_call`. No need to relay something on-chain. Also, there are quite a few libraries and a [quickstart guide](https://docs.login.xyz/sign-in-with-ethereum/quickstart-guide) for using SIWE. You may want to take a look at that - it will help avoid the need to go deeper into the tech stack of SIWE.

---

**mratsim** (2024-07-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/luke/48/11841_2.png) luke:

> Then there are the EIPs, which are almost entirely protocols. They’re akin to e.g. OAuth. And this is where a gulf opens up; the OAuth specification is beautifully written, including ASCII diagrams, and the platform it is running on is far more extensible in the first place allowing for an elegant design. I have never in 27 years read an IETF document that felt like a rushed load of hacks or that is was bending what was put in place before it, e.g. wrapping bytes and sticking magic numbers on the end.
>
>
> The difference in quality is irrefutable, and repudiation is not helpful for me or anyone else. We cannot solve a problem we’re unwilling to have. I’m switching to “we” because I count myself as an Ethereum developer, even though I have barely penetrated it in years of studying.

> Then there are the EIPs, which are almost entirely protocols. They’re akin to e.g. OAuth. And this is where a gulf opens up; the OAuth specification is beautifully written, including ASCII diagrams, and the platform it is running on is far more extensible in the first place allowing for an elegant design. I have never in 27 years read an IETF document that felt like a rushed load of hacks or that is was bending what was put in place before it, e.g. wrapping bytes and sticking magic numbers on the end.

> The difference in quality is irrefutable, and repudiation is not helpful for me or anyone else. We cannot solve a problem we’re unwilling to have. I’m switching to “we” because I count myself as an Ethereum developer, even though I have barely penetrated it in years of studying.

The counterpart to this is that IETF RFCs take years to move even in a seemingly finalized state. For example I helped reviewing, testing and refining this one [Hashing to Elliptic Curves](https://www.ietf.org/archive/id/draft-irtf-cfrg-hash-to-curve-16.html) with v1 from 2018 or so. Despite widespread industrial need (for example for TLS v1.3), I don’t see when it will ever be finalized.

And if you look at this RFC, it won’t teach you how to use it when it is appropriate and when it is not, it teaches you how to implement it. Same as Ethereum EIP.

> It seems that a simple login requires me to wade through obscure and poorly written technical documents that, according to your reply, I have no place reading or criticising! And each document requires reading even more, all the way down.

This seems disingenuous, I repeatedly asked what you’re looking for in EIPs and even gave you a reference to frame your answer so we have clarity on expectations and mismatch. I didn’t say you shouldn’t read or criticise the EIPs.

> So, we either fix the abstraction, or we fix the technical writing, and make sure protocols are extensible and don’t leak and pollute and burden the layers above, i.e. make it so painful for the busy applications developers that they prefer to just pay a company to take the pain away.

So you need tutorials and how-tos. People don’t read the IETF specs when they want to use TLS, they read the implementation documentation and examples. This is something I agree with, tutorials like CryptoZombies were a boon for adoption.


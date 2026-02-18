---
source: magicians
topic_id: 21558
title: About fragmentation of token standards and token designing
author: yaruno
date: "2024-11-02"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/about-fragmentation-of-token-standards-and-token-designing/21558
views: 217
likes: 4
posts_count: 7
---

# About fragmentation of token standards and token designing

Hello fellow magicians!

I’m currently working on a research paper about NFT design. From the academic discussions I’ve reviewed, there doesn’t appear to be a widely accepted, high-level toolkit—such as a method, framework, or process—for designing and applying NFTs to different use cases. My hypothesis is that such tools could significantly support the adoption of NFTs in real-world applications.

In exploring this topic, I’ve noticed a considerable increase in NFT-related standards since we introduced our own, ERC-5023, a year and a half ago. After a brief review of the current landscape, I found that there are now over 160 different ERC standards related to NFTs in some way.

This brings me to a question for you all: Do you see any challenges arising from this trend of increasing amounts of NFT standards? And would you find high-level design tools helpful, such as tools that could help you quickly match existing token standards to your use case or give you confidence early on that your token design is suitable for your intended context?

Jarno

## Replies

**sullof** (2024-11-15):

Standards are set for “scientific” purposes. The adoption of a standard is the real story.

Right now, the steps are “draft,” “review,” “last call,” and “final.” Maybe it would also be good to have something like “adopted.”

---

**yaruno** (2025-01-01):

I’d argue that standards or in this case the ERCs are not just an academic exercise but a way to reduce waste as we shouldn’t have to invent the wheel multiple times and to increase interoperability in the EVM ecosystem as through existing standard contracts we know what to expect from the contract implementation. These are not the only benefits of standardisation but maybe this is as clear as day as it is, just felt compelled to reiterate it.

But coming back to sullofs point about adoption, I think it is much needed but so far it seems like many of the ERC standards goes without greater adoption.

Now related to token design and particularily to NFT design I should probably define here first what I mean with NFT design, but you can imagine it as a more holistic process e.g. confirming iteratively in a structured and a systematic way that you are doing the right things and the things right when choosing a type of NFT for your project and for your ecosystem, than a purely mechanistic one such as implementing things from set of requirements.

I’ve also noticed that in academia or in academic peer-reviewed journal articles there seem to be very few papers that explore both token design and NFT related token standards beyond the typical ERC-721 and ERC-1155 standards.

So a thought occured to me that maybe we should have some kind of tooling to assist both devs and non-devs on quickly navigating and grasping that what kind of NFT related standards exists in the ERC archives besides reading through and understanding every possible NFT standard available.

So, I’ve gone through 163 NFT related standards, taken the standards that are at least at stage of being in review and formulated 19 different categories on basis of their function or purpose and formed sort of ‘design’ cards out of these. The plan is to release these under CC licence, likely on github so anyone can use them and contribute back to them.

On the front side there’s category title, description of the category and a short summary of what that type of NFTs mean in non-technical manner. On the back side of the cards I’ve raised a few ERC standards and briefly listed their key information related to the category.

Here’s a snapshot of a single category card

[![Screenshot 2025-01-01 at 21.39.56](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c4d9c18447a752f7c0d6eafeb2526c09162c7755_2_666x500.jpeg)Screenshot 2025-01-01 at 21.39.561432×1074 158 KB](https://ethereum-magicians.org/uploads/default/c4d9c18447a752f7c0d6eafeb2526c09162c7755)

I’d love to hear what you think. Would something like this be helpful to you, or if not I’d also love to hear about it. Is there something missing from these cards? Or how could they serve your needs even better?

This is very much work-in-process but it has already garnered some academic interest as a potential design tool to assist non-devs on grasping NFT standards. There are also some plans to incorporate these as part of design exercises but I’ll let you know more about that once that track progresses.

---

**Marcuszheng** (2025-01-09):

In fact, we have found that many ERC standards are used enough, for example, ERC-20, ERC-721, ERC-1155, but apart from these ERCs, it seems that the references are not so much compared to the above ones?

I think there may be several problems, some ERC standards have a limited scope of use.

There is an educational gap between developers and academic researchers, and it may be difficult for academic researchers to pay attention to the ERC standards commonly used by developers.

Also, we’re actually doing something similar, we’ve developed EIP.Fun to make some of the ERC standards easy to understand.

---

**1etsp1ay** (2025-01-23):

The ERC-721 is basically a pointer … as a primitive it gets used in all sorts of weird and wonderful ways (hmmm 160+ proposed variants/extensions?)

> This brings me to a question for you all: Do you see any challenges arising from this trend of increasing amounts of NFT standards?

There are 3 steps … non-sequentially

a) the fun exploratory time when you play with the new shiny toy/primitive

c) exploiting the billion+ dollar/yuan/euro commercial opportunity

b) the boring standardisation phase and ECH’s attempts to control the chaos between a) and c).

Technical standards such as IEEE, IETF, and W3C all had ups and downs … sheesh just look at how many protocols are transported via https when there were more efficient mechanisms.

> My hypothesis is that such tools could significantly support the adoption of NFTs in real-world applications.

are you contemplating a technical hack for essentially a socio-economic issue? unlike miners where consensus is needed for adoption, ERCs is more market pull so if it works in the real-world, standards can languish and act as placeholder for time of proposal (if want credit as originator). How will your tool accelerate “adoption”?

---

**yaruno** (2025-02-03):

Instead of technical hack I’m thinking more in line of a practical but non-technical design artifact to quickly communicate taxonomies of token standards. Even though there’s an ever growing amount of them, it seems that there’s quite a bit of overlap between the standards. So the standards that are similar to each other could be categorized and distilled to represent their high level function or purposes.

The challenge that I’ve observed in relation to designing token based incentives with a group of stakeholders is that the non-technical people won’t necessarily understand what the engineers are talking about in terms of standards, their potential functionalities and features and the engineers may get stuck on a few previously utilized standards or want to create a new one without doing the homework of going through what already exists. So to alleviate some of this effort I’ve created some design cards [GitHub - yaruno/nft-design-cards](https://github.com/yaruno/nft-design-cards) .

Now they won’t be the cure all for token design process issues, but they may help to communicate more effectively between technical and non-technical stakeholders about what kind of functions and purposes have been explored in the token standard space, especially in the early exploration phase…

---

**sullof** (2025-03-01):

I introduced ERC7656, now in Last Call, also to reduce ERC proliferation.

One of the key goals of [ERC-7656](https://eips.ethereum.org/EIPS/eip-7656) is to reduce the proliferation of NFT standards. Currently, anyone looking to enable NFTs to manage additional functionalities often defines a new standard, requiring changes to the NFT itself. This leads to a growing number of interfaces, increasing the risk of conflicts and fragmentation.

ERC-7656 addresses this by allowing the deployment of token-linked services—smart contracts associated with and owned by an NFT. These services extend the NFT’s capabilities without requiring modifications to the NFT or its standard (e.g., ERC-721). This approach not only eliminates the need for new standards but also fosters creativity, as developers are no longer constrained by the limitations of the underlying NFT standard.

By decoupling functionality from the NFT itself, ERC-7656 promotes a more modular and interoperable ecosystem, reducing complexity and encouraging innovation. Thus said, the growing number of proposal is becoming a problem. Maybe there should be a better filter.

For example, right now, ERC authors post something here and at the same time make a pull request on the ERC’s repo. It would make more sense if someone posts here, and only if there is a reasonable engagement from the community, a PR is made possible.


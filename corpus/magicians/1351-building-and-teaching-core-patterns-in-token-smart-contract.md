---
source: magicians
topic_id: 1351
title: Building and teaching core patterns in token, smart contract design
author: boris
date: "2018-09-15"
category: Magicians > Primordial Soup
tags: [token, erc-1400]
url: https://ethereum-magicians.org/t/building-and-teaching-core-patterns-in-token-smart-contract-design/1351
views: 901
likes: 3
posts_count: 1
---

# Building and teaching core patterns in token, smart contract design

Bringing in a discussion that I think is important to have from the ERC1400 github thread that is more meta:

From [@thegostep](/u/thegostep) [on GIthub](https://github.com/ethereum/EIPs/issues/1411#issuecomment-421616806):

> The features introduced by ERC20 are fungible token ownership, fungible token transfers, and delegated control. Each of these features could have been implemented as distinct modular standards, but Vitalik and Fabian made the decision to integrate them together as one. There are a few features which were left out of the integrated standard and later proposed as extensions. Namely: safe transfers (ERC223), token callbacks (ERC165), mint/burn events. Whereas all fungible token implementation use the core ERC20 integrated standard, the modular extensions have received limited adoption. We now have a new fungible token standard which integrates these extensions (ERC777). It is interesting to think how the token ecosystem would look today in the counterfactual case where delegated control would have been implemented as an optional extension to ERC20.
>
>
> I see three reasons for lack of adoption of modular extensions:
>
>
> Technical diligence lazyness - Not much can be done here.
> Increased complexity - The modular extensions did not play together as well as they would given an integrated approach, this is most evident when looking at how ERC777 kills two birds with one stone by addressing safe transfers and token callbacks at once with the ERC820 interface registry.
> Ecosystem heuristics - The ecosystem does not think in terms of modular extensions, it thinks in terms of use cases. This creates a bias toward higher adoption for integrated standards. Let me illustrate.

Totally agree with [@thegostep](/u/thegostep). From what I know of the ecosystem and the history, it was large doses of (1) technical diligence lazyness plus (3) the ecosystem not understanding potential patterns.

That’s not *totally* fair, but essentially – the simplicity of ERC20 led to many people running with it, and many of them did not have the technical depth to even discuss never mind assess these other concepts.

This has been good / bad – I have talked in the past about how “crappy code” that anyone can deploy gets people into the top of the Ethereum ecosystem.

What I am seeing is that technical experts like those in this thread are more than capable of technical diligence and creating solid patterns. Next, if we want these patterns to spread, we have to spend an equal amount of time on making this more accessible with education, tools, helper libraries, etc.

So: it took DHH to create the “magic” in Ruby on Rails, and now millions of developers have the safety net of the framework to build web apps with. Only a few participate in pushing along the deepest levels of the framework, most just use it.

We don’t want to split it us and them, but we do have to acknowledge that we can invest in a base of frameworks and knowledge sharing which makes it easier and safer to do things correctly for the long tale of implementors.

Our goal as magicians should in fact be to make everyone magical and raise up the general population, not to keep the wands to ourselves.

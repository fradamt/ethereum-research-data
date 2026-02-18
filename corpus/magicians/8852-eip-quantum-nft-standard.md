---
source: magicians
topic_id: 8852
title: "EIP: Quantum NFT Standard"
author: maxareo
date: "2022-04-07"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-quantum-nft-standard/8852
views: 1061
likes: 3
posts_count: 7
---

# EIP: Quantum NFT Standard

## Abstract

This proposal aims to introduce a smart contract interface that can represent an NFT that are normally distributed around the true NFT but displayed randomly.

## Motivation

A non-fungible token proposed in [ERC-721](https://github.com/ethereum/EIPs/issues/eip-721.md) is usually associated with a media content in the external world through a deterministic link to metadata with media inforamtion. This deterministic linkage can be improved with easy-to-use on-chain randomness such as Gassian random number generator proposed [here](https://github.com/simontianx/OnChainRNG/tree/main/GaussianRNG). The net effect is the ownership is still one, and the displayment can be random with centrality. This can be used in the NFT and GameFi domains.

## Replies

**SalihRmah** (2022-04-07):

I’m not sure I understood what you mean exactly, but if the goal is randomly distributed metadata across the whole NFT project, it is possible to simply assign the metadata in random order to the tokens (with chain-link randomness as a truly random seed, and from there you can use it to simulate any probability function you desire…)

making this a standard wouldn’t boost interoperability of NFT projects that would want to use this approach, plus I don’t see a reason why NFT makers would want to adhere to random assignment of metadata to tokens, since this randomness usually is achieved by the buyers/minters order of arrival, which is generally a war over there)

---

**maxareo** (2022-04-08):

If I name it as Quantum NFT Standard, you may have a better feeling.

In essence, that’s what it is. An NFT does not have to be always linked to the same metadata in a deterministic way. It can be random yet with centrality towards the original one. For example, the NFT with tokenId 123 may be read as token 123 with 60% of probability, and 122 and 124 10% each, 121 and 125 5% each, so on and so forth. The tokenId is always 123, but the content can be those in the neighborhood.

The Gaussian distribution provides the central tendency that Chainlink VRF cannot provide. Let me know if this makes sense to you.

Again, this idea is in the infancy, any idea, comment and question is highly welcome.

---

**SalihRmah** (2022-04-08):

Ah, same token different metadata at different times, technically makes sense,

Quantum NFT Standard does make it clearer

I can think of a possible use-case, but for on-chain data, for example a P2E game “drunk-fighters”, where fights depend on how strong a fighter is (data is on-chain), and his current strength is randomized (since he’s drunk ![:stuck_out_tongue_closed_eyes:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue_closed_eyes.png?v=12)  ). but that would require the randomness be applied on the strength and then calculating the result of a fight…

But, I can’t think of a reason for metadata to be non deterministic, I wouldn’t want my art to change (since it is something I’d want to show people and know what they would see for sure no matter when they’re looking), Can you give an example use-case for non-deterministic metadata?

PS: I’ve mentioned Chainlink VRF to remind you that you can’t truly generate true randomness without something similar to to it, and so if the “current” metadata is used to determine a win/something, in your code, the gaussian distribution seed you get from:

uint256 seed = uint256(keccak256(abi.encodePacked(salt + block.timestamp)));

isn’t truly random, using VRF to get the seed would be more secure.

---

**maxareo** (2022-04-08):

Hey [@SalihRmah](/u/salihrmah), thanks for the comments. I like the “drunk-fighters” idea a lot. I think you are touching the essence of it, which is there is a true value on-chain, and small deviations from it are not only allowed but also encouraged.

Yes, randomness is another topic, and in the repo I shared above talked about it in detail. The focus here is about the type of randoness. The randomness provided by either Chainlink VRF or `keccak256` is uniform in the domain `[0,2**256-1]`, and the RNG in that repo is Gaussian which has a central tendency, which is huge in this scenario.

---

**julesl23** (2022-04-08):

A lookup table is a way to do it.

You can get the Chainlink VRF random number and use that as an index to a mapping/array that has pre-generated Gaussian distribution values, to get a sample from that.

If continuous values are needed then can linear interpolate between two looked up values.

---

**maxareo** (2022-04-08):

Have you looked at the on-chain Gaussian RNG in the repo yet? It may provide a simpler and more gas-efficient solution.


---
source: magicians
topic_id: 7687
title: Is there a 'dynamic NFT' EIP in the work?
author: jeromelecoq
date: "2021-12-04"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/is-there-a-dynamic-nft-eip-in-the-work/7687
views: 2305
likes: 6
posts_count: 11
---

# Is there a 'dynamic NFT' EIP in the work?

is there an ERC standard for a dynamic NFT in the work?

A simple upgrade of ERC721 with

a state struct (no constrains on how it is structured inside)

a standard get_state solidity function

a standard  set_state solidity function

a set of associated event functions to allow external DAPs to listen

I think that would be really impactful. It would allow external smart contracts to standardize linkage of data with a dynamic NFT (similar to relational databases) as well as help develop the growing gaming NFT ecosystem (but this applies beyond gaming) and store on chain important state states.

## Replies

**jeromelecoq** (2021-12-04):

After some digging

This is related to https://ethereum-magicians.org/t/erc-1948-non-fungible-data-token/3139

I can see the EIP was merged but has become stagnant :

https://eips.ethereum.org/EIPS/eip-1948

Sorry if I am new to this process.

Anybody has insights as to why?

---

**jeromelecoq** (2021-12-04):

Pinging [@johba](/u/johba) whether he would be able to comment on status

---

**wschwab** (2021-12-07):

I’m not sure how much of this you’d want to have living on the contract (in a setup where the metadata is off-chain) - it seems like a lot of the time this would be better handled in the JSON itself. tbh, you’d really like to have as little as possible on chain. For games, the question is really what is handled on-chain by the game and what not, which is likely case-by-case.

Can you talk about the usecases you’re looking at?

---

**sbauch** (2021-12-07):

I’ve done quite a bit of work and experimentation with stateful NFTs and have some suggestions.

First, you might be interested in Michael Feldstein’s ideas around mutable ERC721. It’s a bit different than what you’re suggesting, where state is assumed to be returned as part of `tokenUri` metadata and the proposal imagines a system for invalidating metadata caches. [Proposal: ERC721Mutable by msfeldstein · Pull Request #1 · msfeldstein/blockheads-contracts · GitHub](https://github.com/msfeldstein/blockheads-contracts/pull/1)

My first project CryptOrchids are NFT flowers that persist some state to determine if a flower is alive. Owners must perform a transaction `water` every 7 days to keep it alive.

In this case, I would be more keen to use the `get_state` function, but the `set_state` function is less suitable I think? In an ideal world, marketplaces would utilize the get_state function to show current state of a token. But setting state feels like something more specific to the project that needs things like access control.

My more recent work however goes in a bit different direction. If I were to redo CryptOrchids today, I would not put the state on the token contract. I think that we can start to better use composability of contracts and add dynamism or state to tokens through additional contracts or protocols. Generally I feel like the ERC721 spec should primarily be used for ownership related data and functions.

I published a piece that goes into what these additional protocols could look like - [🍑 ASSPLayers for Open NFT Gaming ⛓ — Mirror](https://mirror.xyz/sammybauch.eth/AWEOcldh_K_Lm1ohj3awMQWBaXRWB0Nc45FHmPcu8Co)

So I suppose my suggestion would be that I see the most value in a standard function for “getting state” of a stateful token, but I also would encourage exploring whether this must be an ERC721 extension, or whether this is actually some new type of standard protocol independent of ERC721.

---

**jeromelecoq** (2021-12-07):

1/ Well say that your NFT becomes a key piece of an “avatar” with dynamic associated metadata controlled by the owner. If you want to share it in a decentralized way so that multiple external services can rely on it. I don’t think having all the metadata hosted on an AWS running virtual machine will fulfill the spirit of web3. That machine can go down at any point depending on the original NFT creator thereby impacting the initial purchase of a dynamic NFT.

2/ The ethereum chain is expensive yes but various L2 options are bringing down gas cost that  makes this very practical. For example Minting an NFT on Polygon costs couple $ cents at today’s price making it practical to add a little more info on chain.

3/I understood that all associated ethereum L2 chains are somehow following L1 EIP standards (perhaps even L1 solidity-compatible chains).  So I thought this was the right place to start this as scaling cost is improved.

4/ I want to add that you can make this very reasonably cheap by using integers to store the state of each NFT in a given collection and have a short on-chain lookup table to associate that integer value with a given longer description of the state in the lookup table.

---

**jeromelecoq** (2021-12-07):

thanks I will look it over.

Somehow I like for this to be an extension of ERC721 because you can make this entirely back-ward compatible thereby allowing for stateful NFT to be immediately tradable across all existing platforms along with the other stateless NFTs. I have already implemented working versions of these smart contracts in various forms but I think it would be beneficial to standardize it for this approach to grow.

---

**sbauch** (2021-12-07):

i actually think doing it outside of ERC721 is more backwards compatible? i.e. any stateful NFT that exists now won’t be able to utilize this standard. whereas if you push statefulness to a protocol, any existing NFT project could be registered for that statefulness.

But yes I am a fan of standardizing approach, the primary value i see in standardization is reading the state.

---

**jeromelecoq** (2021-12-07):

Yes, this is true. But then there could be several states associated with a given NFT (in separate smart contracts) ? I am not sure I fully understand your idea.

---

**wschwab** (2021-12-08):

I feel like there’s a bit of an issue here that should get discussed directly, though pretty much everyone in this conversation seems deeper in the technicals of this than I am, so I might just be missing something.

Assuming we’re talking about metadata being stored off-chain (let’s use IPFS as an example), I think any dynamic/mutable metadata touches three things:

1. The actual IPFS link needs to be changed (or if it uses IPNS, then the metadata at that hash needs to change)
2. Which means there’s something off-chain interacting with IPFS to make that happen
3. The contract needs to be updated that either the metadata hash has changed, or in the IPNS case, I would still think that it should issue an event to alert platforms that the metadata has been updated

Number 2 is the one that concerns me the most. I’d like to see us steer towards transparency and trustlessness, but how can we decentralize the middle layer interacting with IPFS? I think what is on-chain and what is off-chain (and what triggers state changes in what) is a dynamic here that should be addressed, but like I said, maybe I missed some of the context above.

In terms of 3, I see ideas here for new functions on top of 721, but perhaps I’m not understanding why we need new functions, and the standard token URI can’t be used. I could understand a new specific event for triggering a URI update, maybe a new `UpdatedURI` event or the like, I don’t feel like I’ve fully understood why we’d need new `state` functions. What do you see these functions adding? I think this is also a part of the whole on-chian vs. off-chain since the metadata is (in general, ofc there are also projects like Loot) off-chain, and I’m assuming whatever is consuming the metadata can read it and pull out the bits that it wants.

---

**jeromelecoq** (2021-12-08):

Good thoughts. So the way I got this to work was based on several observation/experimentations:

1. I found that most NFT smart contracts actually do NOT store a hash of the image. They just create a json/image server (on heroku or AWS) and add URI as base_uri in the smart contract to this server. In general, because the image is not stored on chain, this one-way dependency is rather weak. In fact, I think the hashing part is not even part of the standard openzeppelin implementation. Many NFT collections actually allow this base_uri to be changed by the contract owner so as to be able to move data storage around.
2. In my implementation, the smart contract did not need to talk to the image server. It acts as the source of ground truth for the state of the NFT for ALL external uses of the NFT.
3. The image server can pull the latest state of the NFT by fetching the latests events on the contract and adjust its json / image accordingly. This is trivial web3/javascript work.
4. Storing the critical metadata on-chain is actually intended to address this state disconnect between the NFT image server and the smart contract. Having it on chain guarantees that the state of the NFT cannot be hacked or changed by anyone else than the owner thereby opening up truly decentralized owned NFT metadata.
5. In some ways, I find that dynamic NFTs with on-chain metadata is actually more interesting and useful than most current image static NFTs because the data would actually be on-chain so that the owner can trust this to be his/her (as opposed to an image that is not actually stored on-chain and he/she doesn’t really have the IP for).

Does that provide better context?


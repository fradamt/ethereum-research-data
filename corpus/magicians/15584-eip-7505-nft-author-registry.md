---
source: magicians
topic_id: 15584
title: "EIP-7505: NFT Author Registry"
author: pistomat
date: "2023-08-28"
category: EIPs
tags: [erc, nft, erc1155, erc721]
url: https://ethereum-magicians.org/t/eip-7505-nft-author-registry/15584
views: 900
likes: 3
posts_count: 2
---

# EIP-7505: NFT Author Registry

The following is the discussion for [EIP-7505: NFT Author Registry](https://github.com/ethereum/EIPs/pull/7528).

## Replies

**pistomat** (2023-08-29):

Artists often create artwork that is not directly linked to their wallet, either on a different contract, blockchain, or even wallet. This makes it challenging for collectors and third-party projects to:

- Discover their artwork
- Verify the authenticity of the artwork
- View and understand the artist’s complete collection
- Distinguish collaborative and non-collaborative artworks
- Aggregate market data
- Provide a token-gated experience for all collectors
- Lend against any artwork from a specific author

We are building a unifying platform for NFT artists to showcase all their minted artworks called [rc.xyz](https://rc.xyz/), and we face those problems daily. [@kolar_eth](https://twitter.com/kolar_eth) and I have been brainstorming about solving the NFT author attribution for a while. We have read alternative proposals [EIP-5375](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-5375.md), [EIP-7015](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7015.md) and [EIP-7050](https://github.com/ethereum/EIPs/blob/4141dcf49552e05661f43dfe2db8ce13363fbb0d/EIPS/eip-7050.md), but found that neither of them to sufficiently solves the problem for the main actor, the NFT collector. We have come up with a solution that we think is the best way forward and would like to engage in a discussion with you guys.

Our idea is to have a single canonical NFT Author Registry (inspired by [EIP-5369 Delegation Registry](https://ethereum-magicians.org/t/eip-5639-delegation-registry/10949)) for ERC-712 signatures, enabling backward compatibility by not requiring any changes to the NFT contracts, ensuring the validity of signatures by using a single audited contract, and enabling gasless signatures for authors by using EIP-712 signatures, that anyone can submit to the registry and thus subsidize the gas costs for the authors. To be specific, we define the author as the creator of the digital asset that is being tokenized, for example a work of art, a piece of music, a video, or any other type of digital content. This entity may or may not be the deployer of the NFT contract and/or the minter of the NFT token.

The main features of the registry are:

- Backward compatibility is an absolute must-have. A solution that does not incorporate already minted artwork will never be the definitive and sole source for determining authorship. This is why we chose the path of being completely independent of the NFT contract and implementing it as a registry.
- The biggest downside is that this choice enables multiple parties to claim to be the author of the artwork. But we argue that in the NFT art space, the source of credibility does not come from the NFT contracts, but from the artist’s wallet itself. Given the situation where we have to choose between:

An honest contract and a malicious contract both emit the same event claiming to be created by an honest artists’s EOA (leaving the signature verification up to the user).
- An honest artist’s EOA and a malicious actor both provide a valid signature claiming to be the author of an NFT.

We would choose the latter, given the artist’s address is more easily verifiable than the multitude of NFT contracts.

Demanding all of the current popular NFT minting platforms to implement the solution seems like a high barrier to adoption. I just don’t see SuperRare, Manifold, or even POAP, etc., implementing it as a realistic possibility. It should be solely in the hands of the artists to give themselves the attribution.

Implementing the signatures as ERC-712 (with a signature versioning scheme similar to [Seaport Multi-Zone ExtraData](https://github.com/ProjectOpenSea/SIPs/blob/main/SIPS/sip-6.md) and allowing multiple authors, batch token signature, whole NFT contract signatures etc.) seems like the best solution so far. It can handle single, batch token and whole contract signatures, one or multiple authors, and whatever new solution the community comes up with. We can even handle cross-chain author attribution enabling singing of Tezos artworks, where there is a huge NFT market.

The other huge benefit of ERC-712 is that it allows “gasless” signatures for authors, they only need to sign the data and the transaction can be deployed by a sponsoring third party.

One of the undecided features is whether the registry should implement a mapping of the author to claimed NFT tokens to enable on-chain querying of author’s signatures. On one hand, it would be easier for collectors to see which NFTs are claimed by the author (with no gas cost for off-chain call of view functions) and for other protocols to query the registry for author’s NFTs. On the other hand, it would incur large gas cost for every signature of the artist, which would be a barrier to adoption. Also, composability does not have to be broken because other protocols can accept the EIP-712 signatures as a parameter and query the registry themselves to prove signature validity without the need to store the signature on-chain.

To further decrease gas costs, there is also the possibility for cross-chain author attribution by deploying the registry on an L2 with cheaper gas costs and allowing the EIP-712 signatures to be originated from any `chain_id` for successful signature verification.

What are your thoughts? We are open to suggestions and would love to get your honest feedback.


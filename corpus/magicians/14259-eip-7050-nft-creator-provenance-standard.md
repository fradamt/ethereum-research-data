---
source: magicians
topic_id: 14259
title: "EIP-7050: NFT Creator Provenance Standard"
author: sprice
date: "2023-05-12"
category: EIPs
tags: [nft, erc-721, erc1155]
url: https://ethereum-magicians.org/t/eip-7050-nft-creator-provenance-standard/14259
views: 1359
likes: 3
posts_count: 7
---

# EIP-7050: NFT Creator Provenance Standard

[@depatchedmode](https://twitter.com/depatchedmode) and I have been talking about explicit creator provenance on NFTs and we believe there is space for a new standard.

We propose a new ERC aimed at establishing clear, explicit, and verifiable provenance for creators of NFTs. Current NFT interfaces and marketplaces often implicitly attribute the role of ‘creator’ either to the contract deployer or to the first minter of the NFT. However, this approach has led to inconsistencies and ambiguities, particularly as some NFTs are viewed across different marketplaces or platforms and inconsistent information about the creator is listed.

To address this, our proposed ERC introduces a standard interface that allows for the explicit definition of a creator or multiple creators for an NFT token, a set of NFT tokens, or an entire NFT contract. This could be achieved by enabling the contract owner to set the creator address(es) explicitly. This approach will ensure that the smart contract serves as an unambiguous source of truth for creator provenance, regardless of who deploys or mints the NFTs.

Furthermore, our proposal accommodates a mechanism allowing creators to verify their creator address through a single transaction. This mechanism enhances the traceability and authenticity of NFTs, providing a robust solution to the current challenge of verifiable creator provenance in the NFT ecosystem.

We look forward to community feedback and engaging in further discussions on this important topic.

Here’s some sample code

```plaintext
    function provenanceTokenInfo(
        uint256 _tokenId
    ) external view returns (
        address[] creators
    );

    function provenanceContractInfo(
    ) external view returns (
        address[] creators
    );
```

## Replies

**sprice** (2023-05-20):

https://github.com/ethereum/EIPs/pull/7050

---

**sprice** (2023-05-21):

Here is a proposal seemingly working towards the same goal and using events rather than contract functions.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png)
    [EIP: Creator Attribution for ERC721](https://ethereum-magicians.org/t/eip-authorship-attribution-for-erc721/14244/3) [Tokens](/c/tokens/18)



> The spec suggests this is only for creation time. Seems worthwhile to support changes too - the contract could just emit the same event again after any additional checks (such as approval from the original owner). Creators occasionally migrate to a more secure wallet, it may be nice to reaffirm their latest address
>
>
> My intuition is that managing “authors” post-deployment is most likely cumbersome and possibly unnecessary, given that the author is not the same as the “admin/owner” of the NFT. …

---

**sprice** (2023-05-21):

The existing spec and examples here for ERC-7050 are limited to one creator per token and setting provenance one token at a time.

Considerations are for more than one creator per token and to set provenance in batches of tokens and also for the entire contract.

---

**sprice** (2023-05-21):

I’ve also come to learn about this EIP which is similar



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5375)





###



An extension of EIP-721 for NFT authorship and author consent.










Both ERC-5375 and ERC-7015 seem to be taking a slightly different approach to the use case we have in mind with ERC-7050. Here’s the user story we’re working towards.

> As a creator, it’s important to me that centuries from now someone or something is able to inspect an NFT of mine and easily verify that I was the creator.

I’m excited for the usefulness and approach to this problem to be challenged.

---

**ben.defi** (2023-05-22):

This proposal makes sense to me as a prolific NFT collector. Currently it can be a mess to see who created what. I also like the idea of being able to specify multiple creators which would be useful for art collaborations or any NFT with multiple authors.

---

**depatchedmode** (2023-05-24):

Finally had a moment to catch up on the links to existing proposals, and assess how this one lines up with them. Looks like there’s some good overlap, and pros and cons to each of them.

I’ve done my best to summarize with this chart. Green highlight = unique capability of a proposal. Red highlight = unique shortcoming of a proposal.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/3/32bc3fd3dadca8629d156a9fae1e6a43190898db_2_616x500.png)image2258×1830 269 KB](https://ethereum-magicians.org/uploads/default/32bc3fd3dadca8629d156a9fae1e6a43190898db)

In general, strengths from the other two are:

- the use of consent as the noun instead of provenance — because it acknowledges that any such spec can never guarantee a link between the named address and the original act of authorship
- a focus on eliminating (or reducing, at least) cost in order to make this accessible to authors

Really love that ERC-5375 describes an extension to token metadata, which suggests a faster path to adoption in any existing tooling that leverages token metadata standards.

It feels like these three proposals may be 3 aspects of a complete solution. Not all projects may require all 3 approaches.

One thought I have is that if we aligned on the AuthorConsent data structures, then:

- 5375 provides: full backwards compatibility with currently deployed contracts and nice developer ergonomics for any dApps displaying information about a token
- 7015 provides: zero gas verifiability with onchain discovery (via the event)
- 7050 provides: enumeration of the information direct from the contract, when that may be relevant

All of them should seek to enable:

- unique authorship consent per tokenId
- clarity on how multiple authors are spec’d
- (maybe) a definition of how to handle batch consent for anything that incurs a cost


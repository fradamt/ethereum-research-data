---
source: magicians
topic_id: 7201
title: "ERC: Discussion around Creditable NFT"
author: yfeng997
date: "2021-10-04"
category: EIPs
tags: [nft, governance]
url: https://ethereum-magicians.org/t/erc-discussion-around-creditable-nft/7201
views: 754
likes: 1
posts_count: 1
---

# ERC: Discussion around Creditable NFT

## TL;DR

The proposal introduces an interface for new ERC 721 contracts to register reference to and inspiration from other works. This recognizes influential NFT collections and safeguards originality.

## Motivation

Citation is a well-established mechanism for recognizing the originality of a piece of work and quantifying the impact of the creator. In academia, Google Scholar assigns [citation index](https://scholar.google.com/citations?user=DLP9gTAAAAAJ&hl=fr) to researchers and publications to evaluate the popularity and impact. On Github, developers recognize others’ work by [starring and forking](https://github.com/ethereum/go-ethereum) useful repositories.

Both systems not only provide a time stamp to reserve and verify the creation of the work/idea but also rewards authors/developers based on their influence and marginal value committed to the community.

The same effort is applied to the digital assets world, albeit with much less efficiency and recognition. Two main issues brought to our attention: i) on social media, people can re-publish anyone’s digital work without crediting to the original authors; ii) even with “credit to” or “inspired by” statement tagged in the publication, it is hard to overall keep track of the credibility of the work or its original creators.

Therefore, we propose to adapt digital asset tracking like ERC-721 to register credibility among art works and creators. The goal of this proposed feature is to firstly, count the number of use/mention/credit to a specific artwork; secondly, record the total impact of the original creator and/or the current owner. In this way, the originality and ownership of digital assets can be protected to the maximum extent and artists/collectors can grow their recognition among the community.

## Example

In the ideal scenario, we would like to allow querying for all collections that give credits to a certain work. However, storing this lengthy list costs a formidable amount of gas. Thus, we only keep track of the number of credits as a state variable, and leave specific referenced collections to event logs.

```auto
pragma solidity ^0.6.0;

/**
 * @dev Interface for creditable ERC-721
 */
interface IERC721Creditable {

    /**
     * @notice This event is emitted when another ERC-721 contract credits to this contract
     *
     * @dev When a new contract is minted, the minter would call credit() function
     * and this event would be emitted.
     *
     * @param creditFrom Address of contract that gives credit to this contract
     * @param creditTo Address of current contract
  */
    event RegisteredCredit(address indexed creditFrom, address indexed creditTo);

    /**
     * @dev This function is called when an ERC-721 compatible contract is minted and wants to give credit/reference to this contract. Throws if creditFrom address is not ERC-721 compatible.
     * Emits RegisteredCredit event.
     *
     * @param creditFrom Address of contract that gives credit to this contract
     */
    function credit(address creditFrom) external view;

}
```

The function name ‘credit’ is open for suggestions. Some alternatives include ‘inspire’, ‘reference’, ‘cite’.

What do we think?

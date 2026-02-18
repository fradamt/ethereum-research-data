---
source: magicians
topic_id: 22363
title: ERC-Social SBT
author: alibertay
date: "2024-12-29"
category: ERCs
tags: [erc, erc-721, dao, sbt]
url: https://ethereum-magicians.org/t/erc-social-sbt/22363
views: 106
likes: 0
posts_count: 2
---

# ERC-Social SBT

Hi all

Using SBT, I am developing a standard in which DAO members give “social points” to each other and new votes can be scored with this social score, in order to close the vulnerability of economic model-based voting systems in DAOs. In this way, those who truly contribute to the community can have a more dominant say in the direction of the community.

## Abstract

SocialSBT is a non-transferable ERC-721-based token standard that integrates a dynamic social point system for DAO governance. It aims to mitigate whale attacks and promote equitable, community-driven decision-making.

SocialSBT introduces a soulbound token standard built on ERC-721 that incorporates a social point system for DAO governance. Tokens are non-transferable, and governance power is tied to contributions rather than token holdings. Members can vote on adjustments to social points based on behavior and contributions, ensuring fair and community-aligned decision-making.

## Motivation

Traditional DAO’s economic token based governance models are prone to manipulation by entities with significant financial resources, undermining the collective interests of the community. SocialSBT shifts governance influence to social contributions rather than token holdings, mitigating whale attacks and fostering fair participation.

The system rewards positive contributions and penalizes harmful behaviors. A economic token based voting mechanism ensures equitable participation during social point adjustments, promoting fairness and encouraging active engagement in DAO governance.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

All functions and structures declared in this section MUST be used

1. Minting Tokens

Function: mint() public payable
2. Description: Mints a SocialSBT token for the caller, provided they pay the _price and do not already own a token.
3. Constraints:

The caller must pay the exact _price.
4. Each address can own only one token.
5. Deleting Tokens

Function: deleteToken(uint256 tokenId) public
6. Description: Allows token owners to permanently delete their tokens without refunds.
7. Constraints:

Caller must own the specified token.
8. Voting on Proposals

Function: vote(uint256 votingIndex_, bool choice_) public
9. Description: Token holders can vote “yes” (true) or “no” (false) on proposals to adjust social points.
10. Constraints:

Caller must own a token.
11. Each caller can vote only once per proposal.
12. Ending Voting

Function: endVoting(uint256 votingIndex_) public
13. Description: Ends voting and adjusts points if the majority votes “yes.”
14. Constraints:

Voting period must have expired.
15. Proposal must be active.
16. Querying Token Points

Function: pointOf(uint256 tokenId) public view returns (uint256)
17. Description: Retrieves the social points associated with a specified token.
18. Event Triggers

NewVotingCreated: Triggered when a voting proposal is created.
19. VoteEvent: Triggered when a user casts a vote.
20. VotingEnd: Triggered when voting ends.
21. PointUpdated: Triggered when token points are adjusted.
22. Voting Struct

votingIndex: uint256
23. name: string
24. description: string
25. tokenIndex: uint256
26. point: uint256
27. increase: bool
28. yes: uint256
29. no: uint256
30. startDate: uint256
31. endDate: uint256
32. isActive: bool

## Rationale

SocialSBT decouples governance power from token holdings by implementing economic token based system. This ensures fairness and prevents undue influence by high-point token holders. Non-refundable token burning discourages speculative behaviors and maintains the integrity of DAO governance.

## Backwards Compatibility

SocialSBT extends the ERC-721 standard while remaining compatible with its core functionalities. However, it introduces non-transferability and a social point mechanism, which deviate from the standard.

## Test Cases

1. Minting Tokens

Expected: Successful minting for eligible users.
2. Failures:

User already owns a token.
3. Payment amount does not match _price.
4. Voting

Expected: Correct vote recording and prevention of duplicate voting.
5. Failures:

Non-token holder participation.
6. Duplicate votes on the same proposal.
7. Ending Voting

Expected: Accurate point adjustment based on majority votes.
8. Failures:

Ending before expiration.
9. Inactive proposals.
10. Burning Tokens

Expected: Permanent token removal.
11. Failures:

Unauthorized burn attempts.

## Security Considerations

SocialSBT ensures secure governance through:

- Non-transferability: Prevents token trading and governance manipulation.
- Fair voting: Independent of social points.
- Mitigation of whale attacks: Restricts tokens to one per wallet.
- Non-refundable burning: Discourages exploitative behaviors.

Needs discussion.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**SamWilsn** (2025-04-28):

Instead of inheriting from ERC-721, why not build off of one of the many SBT standards? Here are a few: [ERC-5192](https://eips.ethereum.org/EIPS/eip-5192), [ERC-5114](https://eips.ethereum.org/EIPS/eip-5114), or [ERC-5633](https://eips.ethereum.org/EIPS/eip-5633).


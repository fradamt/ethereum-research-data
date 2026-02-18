---
source: magicians
topic_id: 6703
title: "Introducing EAS: The Ethereum Attestation Service - A base layer for Trust, Identity, Reputation, Voting, and more"
author: slavik0329
date: "2021-07-21"
category: Uncategorized
tags: [reputation-systems, attestation]
url: https://ethereum-magicians.org/t/introducing-eas-the-ethereum-attestation-service-a-base-layer-for-trust-identity-reputation-voting-and-more/6703
views: 1907
likes: 1
posts_count: 3
---

# Introducing EAS: The Ethereum Attestation Service - A base layer for Trust, Identity, Reputation, Voting, and more

EAS is a base layer protocol for **global**, **generic** attestations. Any attestation schema/type can be registered. It is made up of two simple smart contracts. One is an attestation schema registration contract which allows anyone to register any type of attestation. The second is simply a ledger of all attestations.

EAS is meant to be a public good like ENS. We imagine infinite use cases which will open up the Ethereum ecosystem to endless possibilities not limited to mostly finance.

We would love to get feedback on this project!

https://eas.eth.link - Details, Contract links in the slides.

Smart contracts: https://github.com/ethereum-attestation-service/contracts

Team: Steve Dakh, Dino Mark, Leonid Beder

Thanks!

-Steve Dakh

## Replies

**krebit** (2021-07-28):

Hi Steve,

This is Alejandro from Krebit, I saw your presentation on [#ethcc](/tag/ethcc), we’re definitely converging on the same path here, with a few twists, check out our working plan here (preparing testnet launch by mid August): [Krebit's Motivation and Vision](https://www.publish0x.com/krebit/krebits-motivation-and-vision-xqkzxwo)

A couple of things we’re building from Krebit’s side that seem different from your approach:

- Krebit leverages IDX for reusing DIDs, which makes it single-sign-on cross-chain ready and much better for onboarding
- All the data would be stored off-chain, controlled by each of those DIDs (sovereign)
- There will be a cyclical token, for both issuing attestations and DAO governance, I see no other way around it in order to trust or pick the attestators in an open marketplace
- Finally, I think we can be compatible with any attestation approach, we just need to set the interfaces for the schemas, that’s why we’re going to follow the W3C recommendation for verifiable credentials:   https://www.w3.org/TR/vc-data-model what are your thoughts on that?

Happy to keep discussing on this very passionating topic!

Thanks,

Alejandro

---

**slavik0329** (2021-07-28):

Hi Alejandro,

EAS presupposes nothing. We intentionally did not want to build in any specifications as we are simply a base layer for any kind of attestations. With EAS you can register an attestation schema that follows the DID spec if you wish and then make attestations referencing it.

EAS also doesn’t assume that all attestations will be on chain. Our SDK and contracts provide an easy way to create off-chain attestations that can be verified by anyone and also be submitted on-chain by anyone at a later time if desired.

We have no token because since we don’t believe we will have to change the contracts since we kept everything as minimal as possible and presupposed nothing. Anyone can attest or register a new schema on EAS for any reason. The only token required is ETH to pay for the TX fees.

For these reasons I believe EAS can possibly be a platform for your attestations. There is no need to create a separate system. Attestations can be votes, trade agreements, social scoring, ratings, tweets, etc. There is no limit to the types of attestations that can be made so that was the purpose for EAS.

-Steve


---
source: magicians
topic_id: 11894
title: "EIP-6047: Extend ERC-721 to Support balance counting via Transfer event"
author: xinbenlv
date: "2022-11-26"
category: EIPs
tags: [erc, erc-721]
url: https://ethereum-magicians.org/t/eip-6047-extend-erc-721-to-support-balance-counting-via-transfer-event/11894
views: 2797
likes: 7
posts_count: 24
---

# EIP-6047: Extend ERC-721 to Support balance counting via Transfer event

Pull Request: [Add EIP-6047: Extend ERC-721 to Support balance counting via Transfer event by xinbenlv · Pull Request #6047 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6047/files)

---

## eip: 6047
title: Extend ERC-721 to Support balance counting via Transfer event
description:  Mandate emitting Transfer event for EIP-721 NFTs regardless whether minting / transferring occurs during or outside of contract creation.
author: Zainan Victor Zhou ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2022-11-26
requires: 721

## Abstract

EIP-721 requires `Transfer` event to be emitted whenever a transfer or mint(i.e. transfer from `0x0`) or burn (i.g. transfer to `0x0`) occurs, EXCEPT for when during Contract creation. This EIP instead MANDATES compliant contract to ALWAYS emit `Transfer` event regardless whether such transfer occurs in or outside of contract creation.

## Motivation

EIP-721 requires `Transfer` event to be emitted whenever a transfer or mint(i.e. transfer from `0x0`) or burn (i.g. transfer to `0x0`) occurs, EXCEPT for when during Contract creation. Due to this exception granted in EIP-721 standard, compliant contracts could mint NFTs during contract creation without event being emitted. Unlike EIP-721, the EIP-1155 standard mandates event to be emitted regardless of whether such minting occurs during or outside of contract creation. This allows a indexing service or any off-chain service to reliably capture and account for token creation.

This EIP removes said exception granted by EIP-721 and mandate emitting Transfer for EIP-721 during contract creation and thus all indexers and off-chain applications can account for token minting, burning and transferring only relying on EIP-721 Transfer event streams.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

1. Compliant contract MUST implement EIP-721
2. Compliant contract MUST emit Transfer event to be emitted whenever a token transfer or mint(i.e. a token transfer from 0x0) or burn (i.g. transfer to 0x0) occurs, except for when during Contract creation, regardless of whether such transfer, mint or burn occurs during or outside of contract creation.

## Rationale

1. To allow accounting for minting during contract creation, there is also option to just create and emit new event type such as, Creation, instead of emitting the same Transfer. We choose not to go with such option, but instead just strengthening the EIP-721 requirement, which maximize the backwards compatibility.

## Backwards Compatibility

This EIP is designed to be fully backward compatible with EIP-721.

## Security Considerations

No new security concern is introduced.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**xinbenlv** (2022-11-26):

Kindly inviting the following experts to peer review.

### EIP authors / contributors / standardizing

- Author(s) of ERC-721: @fulldecent ( notified here)
- Author(s) of ERC-20: @frozeman ( notified here)
- Author(s) of ERC-1155: @coinfork
- Author(s) of ERC-2309: @pizzarob ( notified here)

### Contract Library

- OZ ERC721 main contributors for ERC721.sol: @Amxx , @frangio (notified here)

### Indexers / Explorer

- TheGraph: indexer repo main contributors: @Jannis, @fordN,  notified via Discord
- Etherscan / Blockscan: etherscan@twitter  notified via Twitter

### Marketplaces

- OpenSea  notified via Discord
- SudoSwap

### Wallets

- MetaMask
- Enkrypt

### Notable NFT Projects

- BoredApe
- DecentralLand

*Please feel free to suggest other people we should notify to feedback*

---

**fulldecent** (2022-11-28):

Text looks good to me.

In the discussion here, I’d like to see research of existing token scanner implementations that are implementing this already or that would be affected by implementing this.

Also, would be nice to review some X notable NFT projects of today or over some time period to see if they are implementing this already.

---

**frangio** (2022-11-28):

This EIP makes no sense in my opinion… There is no way to retroactively add a “MUST” requirement to EIP-721, so it could never be anything more than a recommendation. The Backwards Compatibility section is inaccurately saying that this is fully backwards compatible… it clearly isn’t.

The provision to forgo the Transfer event during construction is there and it can’t be removed, it can be used by contracts and is used for efficient batch minting. In conjunction with EIP-2309, this pattern can be made perfectly indexable through events.

If this EIP will move forward, it needs to be appropriately reduced to a set of recommendations (“SHOULD”), and it should account for EIP-2309 events.

---

**xinbenlv** (2022-11-28):

Thanks [@frangio](/u/frangio)

## Define “compatible”

> There is no way to retroactively add a “MUST” requirement to EIP-721, so it could never be anything more than a recommendation. The Backwards Compatibility section is inaccurately saying that this is fully backwards compatible… it clearly isn’t.

I have a feeling when we use the term *EIP Foo is compatible with EIP Bar* we mean different things.

Let me clarify what I mean when using this term with you to ensure we are talking the same language in this discussion so then we can determine if we have different views or not.

In the context of EIP-6047there could be other case when we used the term differently, When I say EIP-6047 (Mandate ERC721 Transfer) is *Compatible with* EIP-721, what I really mean is that *any compliant contract confirming to EIP-6047 will also be a compliant contract with EIP-721*. Or more mathematically described as:

*The **whole set** of EIP-6047 compliant contracts is a **(strict) subset of the whole set** of EIP-721*

Let me use other examples to demonstrate this relationship

1. EIP-712 (Typed Data Signing) is compatible with EIP-191 (General Signing) because the whole set of EIP-712 compliant contracts is a (strict) subset of EIP-191. Contract compliant with EIP-712 is always compliant with EIP-191 but not all contract compliant with EIP-191 is a EIP-712 compliant contract
2. EIP-2612 is compatible with EIP-20 because the whole set of EIP-2612 compliant contract is a (strict) subset of EIP-20 but not all EIP-20 compliant contract is compliant with EIP-2612.

## With that clarification let me address your second comment about EIP-2309

That’s good suggestion. Some considerations here.

Supporting EIP-2309-alike interface is a good idea. But it seems EIP-2309 cannot be supported as of its current version. Since it’s final, a new (competing) EIP probably need to be proposed due to EIP-2309’s incompatibility with EIP-721, let me explain why I say EIP-2309 is not compatible with EIP-721

> Specification of EIP-2309
> …
> Contracts that implement the ConsecutiveTransfer event MAY still use the original Transfer event, however when emitting the ConsecutiveTransfer event the Transfer event MUST NOT be emitted.

If EIP-721 is intended to mandate*see note a `Transfer` event

> Specification of EIP-721
> (Transfer event): This emits when ownership of any NFT changes by any mechanism. Exception…

The mandate to emit `ConsecutiveTransfer` instead of `Transfer` in some cases from EIP-2309 actually **breaks** the mandate of EIP-721. EIP-721 mandates a `Transfer` event MUST be emitted. EIP-2309 mandates a `Transfer` event MUST NOT be emitted in some cases but instead use `ConsecutiveTransfer` in these cases.

Any compliant contract of EIP-2309 *when* not always emitting `Transfer` event but emitting `ConsecutiveTransfer`, is not conforming to EIP-721. Therefore the whole set of conforming contracts of EIP-2309 is not subset of the whole set of conforming contracts of EIP-721.

If you could agree with the assertion that EIP-2309 is not EIP-721 compatible, while EIP-2309 could not be supported, we shall probably support something like EIP-1155’s `TransferBatch` event.

### Note for

Hey [@fulldecent](/u/fulldecent) could you clarify *whether it’s mandated by EIP-721 to emit a Transfer event always except for creation?* . It seems EIP-721’s current snapshot is not strictly following `RFC 2119` such as “Every ERC-721 compliant contract must (lower case `must`) implement the `ERC721` and `ERC165` interfaces”

---

**frangio** (2022-11-28):

A contract that emits EIP-2309 `ConsecutiveTransfer` in the constructor instead of EIP-721 `Transfer`, is both EIP-721 and EIP-2309 compliant. In order to remain EIP-721 compliant it must not emit `ConsecutiveTransfer` events outside of the constructor (unless they are accompanied by `Transfer` events, in which case there is no reason to just emit `Transfer`).

---

**xinbenlv** (2022-11-28):

[@frangio](/u/frangio) Just to clarify, do you mean, in your opinion, EIP-721 doesnt mandate `Transfer` event?

---

**frangio** (2022-11-28):

EIP-721 doesn’t mandate `Transfer` during contract creation, as clearly stated in the present EIP draft.

---

**xinbenlv** (2022-11-28):

Maybe this is better way to frame it: Consider IP-6047 **extends** EIP-721 to make token balance totally accountable merely via counting `Transfer` events, just like EIP-1155.

---

**frangio** (2022-11-28):

I agree with the goal of making token balance totally accountable by events, but I think this EIP should allow EIP-2309 `ConsecutiveTransfer` as an alternative to EIP-721 `Transfer` during contract construction. If you think this defeats the purpose of the EIP you were trying to propose then feel free to ignore my suggestion.

I agree with the new title for the EIP. The contents of this post should be updated as well since they still say “Mandate … for EIP-721”.

---

**xinbenlv** (2022-11-28):

[@frangio](/u/frangio)

Great, we agree on **the general goal** of making token balance totally accountable by events. ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=15)

Let’s debate one of the design decision here

## Design Choices for which “transfer event” to use for batching

- Option 1. Use EIP-2309 ConsecutiveTransfer instead of Transfer when transferring multiple tokens with consecutive ids, and use Transfer otherwise.
- Option 1a, [See update]Use ConsecutiveTransfer in addition to Transfers
- Option 1b, [See update]Use ConsecutiveTransfer only at contract creation.
- Option 2. Use ERC-721 Transfer for all cases, emit Transfer event multiple times for multiple token ids, regardless of consecutive token ids.
- Option 3. use something like TransferBatch with unit256[] tokenIds that allows specifying uint256 tokenIds. (similar to EIP-1155)

## My thoughts

Here is my thoughts.

First, let me re-iterate this and make sure if we are on the same page:

Both Option 1 and Option 3 are **NOT** backward compatible with ERC-721, because let’s say Coinbase, OpenSea and Etherscan are already watching `Transfer` of ERC721 hoping to learn all transfers and do something upon a Transfer. Now, if a new contract start adopting Option 1 or Option 2, start using a transfer event different from what’s already in ERC-721. In this case, without updating the logic Coinbase, OpenSea or Etherscan will none be able adopt to Option 1 or Option 2. This is why I say Option 1 and Option 3 are not backward compatible.

On the other-hand, for any new contract using Option 2, despite being gas-inefficient, is backward compatible with ERC721: that is to say, Coinbase, OpenSea or Etherscan or Subgraphs of TheGraphProtocol will not need to make change to their logic to also watch for a new transfer event with different name. Their old logic will still work.

Let me know if I explain myself clearly ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15) If my explanation still lacks clarity, I am happy to write some reference implementation code of both contract and indexer/tests to demonstrate what I mean.

---

## Update after more research.

Context:

- EIP-2309 admits it’s not compatible with ERC-721 and suggest either using both ERC-721 Transfer

> For platforms that wish to support the ConsecutiveTransfer event it would be best to support both the original Transfer event and the ConsecutiveTransfer event to track token ownership.

We hereby have two other new options as variant of Option 1:

- Option 1a, Conforming contract to use ConsecutiveTransfer in addition to
Transfers, this defeats the purpose of gas efficiency and adds more gas cost. and this is incompatible with When emitting the ConsecutiveTransfer event the Transfer event MUST NOT be emitted in EIP-2309
- Option 1b, Conforming contract to use ConsecutiveTransfer only at contract creation. This is limited use-case and also it makes it impossible to support indexers who only watches Transfer, defeating purpose of maximizing compatibility with ERC-721s.

Also, I have doubt of how much gas cost EIP-2309 really saves overtime for Option 1.b. Here is why:

While one transfer will change gas cost from O(N) to O(1) with N = number of tokenIds,  If one address is going to receive a large amount of tokens, my unverified probably uneducated hypothesis is that such batch holding is for the purpose of distributing the NFTs down the road. Since they will only distribute tokens one by one given EIP-721 doesn’t support batchTransfer, if we only use `ConsecutiveTransfer` for creation, when the holding is doing secondary distribution, the long term gas cost is still cost of O(N). Therefore the overall gas saving, if only adopting at creation time, is very limited.

Therefore, so far I find Option 2 still the most preferred design option for this decision question.

---

**frangio** (2022-11-29):

Yes, I should clarify, I’m aware that full EIP-2309 is incompatible with EIP-721. This is why we have only implemented the subset of EIP-2309 that can be made compliant: Option 1b. This corresponds with OpenZeppelin’s [ERC721Consecutive](https://docs.openzeppelin.com/contracts/4.x/api/token/erc721#ERC721Consecutive). It’s compliant because the only time that Transfer events are not emitted is during contract construction, as allowed by EIP-721.

Indexers that only watch Transfer will miss the initial batch mint. This is true, but developers can make an informed decision about this and choose that route. (In reality, it is those indexers that are making a mistake by assuming that all transfers will be logged in an event, which is not guaranteed by EIP-721.)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> the long term gas cost is still cost of O(N)

Yes, of course, but the goal is to reduce the cost of initial mint, i.e. the launch of a project. As you mentioned that is reduced from O(N) to O(1).

So my suggestion is to make this EIP recommend Option 1b.

---

**xinbenlv** (2022-11-29):

I see what you saying. We are in full sync now, [@frangio](/u/frangio)

I now understand that you recommend Option 1b as preferred design choice in closing which event to emit.

With respect to my own opinion, I am open to choose Option 1b as recommendation. Since Option 2 will still be what people support out of box, I lean towards *at least* recommend Option 2, and *consider also* recommend Option 1b.

For whether to *also* support Option 1b, we could take input of opinion and views from major indexers. If they support / are committed to support Option 1b, I think we could also recommend Option 1b.

Do you have some recommendation who are also important ecosystem players that we shall also solicit feedback from?

---

**frangio** (2022-11-29):

I’m sure NFT marketplaces will have a lot of experience with indexing and may have opinions. I don’t know which particular ones.

---

**xinbenlv** (2022-11-29):

> I’m sure NFT marketplaces will have a lot of experience with indexing and may have opinions. I don’t know which particular ones.

Sounds good.

Thank you [@frangio](/u/frangio)

---

**pizzarob** (2022-11-29):

Emitting ERC-2309 in the constructor of an ERC721 contract works quite well in my opinion. There are plenty of actual use cases of this in the wild. Major marketplaces already support this standard (opensea, looksrare, sudoswap). I don’t see the issue that this new standard will solve.

---

**xinbenlv** (2022-11-30):

Thank you [@pizzarob](/u/pizzarob) for the response.

Two questions

> Major marketplaces already support this standard (opensea, looksrare, sudoswap)

Do you refer to their indexing side? Or do you only referring to their contracts? I love to do more research on these, can you kindly share some point of reference?

> I don’t see the issue that this new standard will solve.

Which issue, could you ellaborate?

---

**frangio** (2022-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pizzarob/48/5694_2.png) pizzarob:

> I don’t see the issue that this new standard will solve.

The way I see it this ERC would simply be documenting standard best practice given that EIP-721 by itself technically allows the bad practice of not emitting events in the constructor.

---

**pizzarob** (2022-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Do you refer to their indexing side? Or do you only referring to their contracts? I love to do more research on these, can you kindly share some point of reference?

Hi. I am referring to the indexing side. I’m sure querying the chain for ERC-2309 events would yield a lot of results. That being said I’m not sure this standard you are proposing would fix anything. It would be a new standard, yes, with a new rule, but people are already emitting 2309 in the constructor and it will remain valid under ERC-721. I don’t think people will stop emitting the event if they have a use case where they need to mint many NFTs to one or several wallets (e.g. team mint). In addition, 2309 is already indexed by major marketplaces. So this new standard exists and then what? I’m not sure I’m sold that it’s a best standard to only emit ERC-721 transfer events in the constructor. The flexibility is nice and has proven use cases.

---

**xinbenlv** (2022-12-02):

[@pizzarob](/u/pizzarob),

EIP-6047’s goal is to make balance of token account able by merely using event.

EIP-2309 introduces `ConsecutiveTransfer` but solves a different problem than EIP-6047 trying to solve.

I appreciate your feedback.  I couldn’t find OpenSea documenting it’s indexing EIP-2309. If anyone could provide some links of documentation, that would be great. Or if someone could provide a public deployment of EIP-2309-based ERC721, that would also help me do t he research.

For indexers, we continue to ask for help if there is any documentation / feedback about your indexing of EIP-2309. Otherwise I think I so far still lean towards just choose Option 2 so all indexer will work out of box.

---

**pizzarob** (2022-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Or if someone could provide a public deployment of EIP-2309-based ERC721, that would also help me do t he research.

Here’s one [Address: 0x38930aae...11b13092b | Etherscan](https://etherscan.io/address/0x38930aae699c4cd99d1d794df9db41111b13092b#code) - see line 87. It uses [ERC721A](https://chiru-labs.github.io/ERC721A/#/erc721a?id=_minterc2309)

I’m not sure if there’s any docs about opensea/looksrare indexers but both have properly indexed the above collection and tokens 1 - 1000 were minted using consecutive transfer.


*(3 more replies not shown)*

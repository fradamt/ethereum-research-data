---
source: magicians
topic_id: 3439
title: "ERC-2135: Consumable Interface, e.g. NFT Event Tickets"
author: xinbenlv
date: "2019-07-03"
category: EIPs
tags: [erc, nft, erc721, erc2135]
url: https://ethereum-magicians.org/t/erc-2135-consumable-interface-e-g-nft-event-tickets/3439
views: 3377
likes: 3
posts_count: 18
---

# ERC-2135: Consumable Interface, e.g. NFT Event Tickets

Hi community members, I’d like to call for a early stage vetting of the idea of having a standard for consumable. Thank you!

---

## eip: 2135
title: Consumable NFT for Ticketing
description: An interface extending EIP-721 and EIP-1155 for consumability, supporting use case such as an event ticket.
author: Zainan Victor Zhou ()
discussions-to:
status: Review
type: Standards Track
category: ERC
created: 2019-06-23
requires: 165, 721, 1155

## Abstract

The interface identifies functions and events needed for creating a contract to be able to mark a digital asset as “consumable”, and react to the request of “consumption”.

## Motivation

Being a digital assets sometimes means a consumable power. One most common seen examples would be a concert ticket.

It will be “consumed” at the moment the ticket-holder uses the ticket to get access to enter a concert.

By having a standard ERC interface, the Ethereum ecosystem can interoperate to provide services, clients, UI, and inter-contract functionalities on top of this very general use-case.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

1. Any compliant contract MUST implement the following interface

```solidity
pragma solidity >=0.7.0 EIP-20, EIP-777 and Fungible Token of EIP-1155.

## Security Considerations

The compliant contract should pay attention to the balance change when a token is consumed.

When the contract is being paused, or the user is being restricted from transferring a token,

the consumeability should be consistent with the transferral restriction.

The compliant contract should also carefully define access control, particularlly whether any EOA or contract account may or may not initiate a `consume` method in their own use case.

Security audit and tests should be imposed to verify the access control to the `consume`

shall behave as expected.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**xinbenlv** (2019-07-04):

Updated with a reference implementation.

---

**SamWilsn** (2022-09-20):

Why does `consume` take a `_consumer` argument? You mentioned on the call that the event organizer would be the one calling `consume`, and the owner information is tracked by the underlying token implementation. Wouldn’t the owner always be the one doing the consuming?

---

Should `consume` be a consensual operation? Like should the token owner have to allow the event organizer to `consume` the ticket?

---

**xinbenlv** (2022-09-20):

That’s a very good question. The `_consumer` argument is inspired by the  `_from` aspect of `transferFrom`. This allow someone other than the `_consumer` to be the TX initiator.

We kept this EIP opinion-less of who should be entitled to create the consume TX, and leaving it to be determine by the implementors.

Since the EIP is having “ticketing” use case as its primary design goal, let me articulate the EIP in such use case

In today’s most typical event ticketing, an event organizer will be at the gate of an event and cut off the ticket. To model this physical action, one of the implementation can require the TX initiator be a specific admin role of a contract. Only an “admin” is able to initiate a TX and the TX will be inherently trusted, *so long as* the TX initiated is an "admin. This is the most simplified way to model today’s interaction, just like how EventBrite is operated.

However, we can also deem the physical attendance of the ticket holder, holding a ticket in hand and appear before the admin, being the “consent to consume” the ticket. In this case, a single handed consent can be model by that the ticket holder to be the TX initiator.

A third case, ideally, is to let the TX show the consensus between ticket holder and the event admin. This can be modeled by [EIP-5453 Smart Endorsement](https://eips.ethereum.org/EIPS/eip-5453). For example, the ticket holder pass in an endorsement as their way to show consent, then a TX be initiated by the event organizer. Or the event organizer pass in an endorsement and then a TX be initiated by the ticket holder.

The EIP is intend to support all these 3 use cases by stay way from dictating the logic to allow or prevent the consuming

---

**xinbenlv** (2022-09-22):

Moved to a status of Review. Looking forward to more feedback

---

**fulldecent** (2022-09-30):

Is anybody using this specification in production? Is anybody interacting with the contracts are deployed with this specification?

---

**xinbenlv** (2022-09-30):

Yes. A typical event ticket is a consumable in real life. This EIP is to model that behavior.

I’ve seen contracts try to “burn after use” a token. but the interface has not been standarized hence proposing this EIP to advance standardization and interporabilitiy.

This spec is by itself not deployed yet. But I have some ref impl that I can put out and advocate for interaction. Is this what you would suggest? Just like you share the prod deployment on the first ERC-721 to demonstrate and allow people to interact with it?

---

**fulldecent** (2022-09-30):

If the use case we want to support is “event tickets consumed in real life”, then this EIP could simplified considerably as follows:

> ## Abstract
>
>
>
> Tickets for real life events.
>
>
>
> ## Motivation
>
>
>
> Tickets generate revenue for venues and artists.
>
>
>
> ## Specification
>
>
>
> Venues and event promoters shall issue tickets to authorized customers. Venues shall deny access to an event other than to authorized customers as evidenced by possession of a ticket, one per head.
>
>
>
> ## Rationale
>
>
>
> Entry allowed without tickets will cause people to attempt entry without purchasing a ticket.
>
>
>
> ## Backwards Compatibility
>
>
>
> This mechanism is well known already in the industry.
>
>
>
> ## Test Cases
>
>
>
> I attempted to forcefully gain entry to a concert and was detained by police—protocol was properly followed.
>
>
>
> ## Security Considerations
>
>
>
> Tickets should be validated online or have strong self-evident properties to avoid fakes.
>
>
>
> ## Copyright
>
>
>
> Copyright and related rights waived via CC0.

But instead this (DRAFT) specification assumes that:

1. Smart contracts should be used for ticketing.
2. Tooling should be used to validate tickets in a cross-project way (e.g. people that organize Gutter Cat Gang parties also care about using the same tools to validate their tickets as if they were to admit people with BAYC event tickets)
3. People like Gutter Cat Gang want to use this exact set of functions to perform such validation.

I would like to see evidence supporting that 1, 2, and 3 are true. Specifically I would like to see a party having already implemented tools that create and validate EIP-2135 (DRAFT) tickets and that are cross compatible.

If such evidence cannot be demonstrated then this proposal is academic and of no practical importance and I recommend it be archived without further consideration.

---

As for ERC-721, at the time this was standardized, there were already several token applications implemented, and also many tools (OpenSea, RareBits, Etherscan (sort of)) supporting these proposed functions.

---

If you are interested in moving forward *Consumable Interface*, I recommend these steps:

1. Build an application
2. Get people excited to use it
3. Make other people want to integrate with your tools
4. Make other people want to copy your idea
5. After all that, publish a specification

And I think you might have some success with this, as people like parties and events!

Further discussion on this approach at [What kinds of things should be standardized? – William Entriken Blog](https://blog.phor.net/2022/09/30/What-kinds-of-things-should-be-standardized.html)

---

**xinbenlv** (2022-09-30):

Haha, good point. I saw multiple questions from here, and I am going to answer one by one.

Q: Whether to narrow it to “ticketing”:

A: Just like when you first draft ERC-721, it was meant for “Deed” but NFT is more general. Consumables is the same. Ticket is one use case, but it can be more general so I want to strike a balance.

Q: Are there real production usage today?

A: I am sure there is already many ticketing service, via NFT or not via NFT on chain or not onchain. One way or another, they are NFT, if they have a number on the ticket. e.g. the seat tickets with a seat number, they are NFT. Does it need an onchain applications to proof there is such a need for ticketing? I think we don’t.

Q: Build an application and get other people to follow

A: Sure, that’s a good next step for sure. There are multiple roles in this effort. The standard author, the reference implementation builder, the developers of making it a full service app. The integrator. It’s a chicken-and-egg eissue when these players are also waiting for a standard to be finalized. So I don’t think it’s a blocker for moving forward this EIP as a specification.

Thank you for the great feedback. and I am interested in reading [What kinds of things should be standardized? – William Entriken Blog](https://blog.phor.net/2022/09/30/What-kinds-of-things-should-be-standardized.html)

---

**fulldecent** (2022-09-30):

**Regarding ticketing**

The (DRAFT) EIP prescribes a way to make (some part of) tickets using Solidity smart contracts for events.

However the motivation given is only “real life events use tickets.”

Instead, a much stronger “people are using Solidity smart contracts for event ticketing” should be the threshold to consider a need for this.

**Regarding current production usage**

Many things in this world are NFTs, NFTs have [thousands of years of history](https://twitter.com/fulldecent/status/1572990410892394503). But in the context of EIP, the only relevant thing is people using Ethereum.

So, yes, there should be on-chain applications to prove these is a need to standardize on-chain applications.

**Regarding the chicken and the egg**

There is no inherent chicken-and-egg problem in building blockchain applications. We can build the chicken and build the egg. Then now we have both a chicken and an egg! If the whole purpose is to get chickens and eggs, then this is the best way to make progress on that goal.

By starting with the standard first, and then assuming other people want to build it later, we are taking the least experienced people (the people that did not build a thing) and having them fly blind making the decisions for the people that need to use it (the builders). This is exactly the opposite of how effective specifications should be written.

**Regarding ERC-721 Deeds**

In ERC-721 the word “deed” is descriptive of how ERC-721 tokens may be called. It has no normative implication on broadening or narrowing the scope of the ERC-721 specification.

---

**xinbenlv** (2022-09-30):

[@fulldecent](/u/fulldecent) greatly appreciate you spending a lot of time to discuss this.

## Ticketing and current product usage on chain

If you are looking for some proofs of on-chain application specifically, it’s not very hard to find, GETProtocol and its deployment is one example [Address: 0x4ea573a6...844b7fc6a | PolygonScan](https://polygonscan.com/address/0x4ea573a6d029ed57e3199fb04e503b8844b7fc6a#code)

I don’t want to link too many links here to avoid seemly spamming or advertising. But I think it’s not very hard to find other examples. I am confident that we have enough adoption activities out there.

Now, **even if** they aren’t enough adoption activities out there… here is my major point next section

## Regarding the chicken and the egg

I can see that you are advocating your suggestion for the ecosystem in your article

of what kind of thing should be standardized (we mentioned it so many times so that the discourse start warning me…). I can see a lot of value your article and views bring. but I also see some other examples where standardization goes before on-chain adoptions.

One I could find is that [EIP-162](https://eips.ethereum.org/EIPS/eip-162) was the first ENS domain EIPs which was proposed on 2016, and the first development activity of [Contributors to ensdomains/ens · GitHub](https://github.com/ensdomains/ens/graphs/contributors) seems happen on about the same time of EIP-162, a long time before it’s launched. And only recently the industry is catchup by MetaMask, ethers.js are adopting it this year. web3 even only supports it poorly. The progress of adoptions are still far from complete yet.

Another example is [ERC-1191: Add chain id to mixed-case checksum address encoding](https://eips.ethereum.org/EIPS/eip-1191) which advocates a change of behavior from EIP-55. In fact it **conflict** with EIP-55 because any compliant representation that follows EIP-1191 will be considered invalid under EIP-55 if the chainId is anything other than zero. Are we suggesting there should never be new standard proposed that conflict with previous one? How would roles in ecosystem be able to discuss consensus for a backward incompatible change if we always need adoption goes before standardization?

These two examples are good demonstrations that *standardization and adoptions goes chicken-and-eggs* or call it more positively **goes hand in hand**. We have to move both forward. Blocking ether side standardization or adoption by lack of the other side will not make things faster, it just reduce its speed.

I like to thank you that by commenting on this, you are helping it get more people to think about this standard. I look forward to your and everyone’s feedback on the specifications of this EIP itself.

---

**xinbenlv** (2022-09-30):

Oh, how come I forget a third or even better example. What’s the most used ERC anyway?

Take a guess?

ERC-721? Nope, ERC-20? Nope. It’s ERC-165!

Oh boy! The ERC-165 determines the standard identifier for an ERC. It’s the most used one, hands down.

What if no one try to standardize interface identifier, how could people and other smart contract start using it? IPv6, email address, HTTP… are all very good examples of standard goes before adoptions.

Honestly, now that I went through the thinking process, it seems it’s more often standardization goes before adoption than the other-way around, the story of ERC-721 is actually a miracle, a miracle that ~~thanks to~~ **despite** there were so many prior adoptions of non-standard NFTs, people were still conforming to ERC-721 when it’s proposed. But it seems more of an outlier than a norm.

---

**fulldecent** (2022-10-04):

**The tail wagging the dog**

The address at https://polygonscan.com/address/0x4ea573a6d029ed57e3199fb04e503b8844b7fc6a#code does not have any production use. It does not appear to be a sincere attempt of solving a real-world problem with blockchain. It appears that the primary motivation is to pass a standard.

I do not support the passage of “standards” of thought leadership–standards should be document real world interactions between producers and consumers of information.

**Examples of chickens and eggs**

EIP-162 is probably too old to be referred to as current practice. Anything before ERC-721 is. Before ERC-721, every EIP needed to be approved be The Core Developers. A strict (and cynical) interpretation would be that there was no community or editor input in the process. ERC-721 was introduced with the new two week review process and passed without consent of core devs.

Regarding EIP-1191, the author of that document represents RSK, a bona fide user of that specification. Also, that person had convinced a consumer of the standard, MyEtherWallet, to adopt it. Therefore at the time of standardization (review) we already had multiple producers of the standardized information (two RSK networks) and multiple consumers of the information (Web3.js, MyEtherWallet). EIP-1191 truly was a standard to document.

The adoption of RSK’s new checksumming scheme, and its implementation in third party software was in no way held back by the subsequent standard ERC-1191.

---

**xinbenlv** (2022-10-04):

> EIP-162 is probably too old to be referred to as current practice.

I am not sure if this is very convincing as an argument.

> Regarding EIP-1191, the author of that document represents RSK, a bona fide user of that specification. Also, that person had convinced a consumer of the standard, MyEtherWallet, to adopt it.

Was the EIP-1191 proposed first or did MEW adopt a checksum before the existing of EIP? Wouldn’t the history that EIP-1191 exist before MEW adoption a good example that standard sometimes are proposed first before it was adopted? If the argument is that, oh EIP-1191 was not finalized before MEW, well, many other standard were not finalized before they are adopted.  But also not many are blocked from being proposed and worked on.

---

**xinbenlv** (2022-10-04):

[@fulldecent](/u/fulldecent)  I also didn’t see that you give example why EIP-165 was not a counter example.

Saying both EIP-162 ENS and EIP-165 Standard Interface Detection are “too old” seems to me you are advocating a new standard that has not been adopted by EIP process.

Or else, are you arguing that EIP-162 and EIP-165 by the current standard shall never exist?

Even if those are too old, now there is also a new ERC-4337 Account Abstraction, how would this ERC be measured with the same criteria?

---

**vic** (2023-04-18):

Hi [@xinbenlv](/u/xinbenlv)  will appreciate if you have an example implementation for reference. Can you share the github project for the deployed contract you have done at Goerli?

---

**xinbenlv** (2023-04-18):

![image](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/ercref/ercref-contracts/tree/main/ERCs/eip-2135/contracts)





###



[main/ERCs/eip-2135/contracts](https://github.com/ercref/ercref-contracts/tree/main/ERCs/eip-2135/contracts)



ERC Reference Implementations. Contribute to ercref/ercref-contracts development by creating an account on GitHub.

---

**gollyticker** (2023-06-16):

Thanks for your effort and your submission.

Two questions from my side to this suggestion:

- The consumption event is called OnConsumption. I find this a sub-optimal wording as it is different than the established wording in ERC-721 and ERC-20. To be consistent with them, it would be ideal to call this simply Consume.
- The consume() method has the _data argument used for future improvements and extensions. I am not sure, what the ramifications are for this. Perhaps this is more complex than necessary? Most applications will likely not need this (and this is not standardise anyways) and if an application needs it, then they’ll likely just create a new method which implements the logic that would depend on _data. Since _data isn’t standardiseable, I feel like not having it would make sense.

The second questions also depends on practical usages. Do we have concrete implementations of this used in some places out there in the ecosystem?


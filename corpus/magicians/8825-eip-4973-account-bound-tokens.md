---
source: magicians
topic_id: 8825
title: EIP-4973 - Account-bound Tokens
author: TimDaub
date: "2022-04-05"
category: EIPs
tags: [erc, nft, ntt, soulbound]
url: https://ethereum-magicians.org/t/eip-4973-account-bound-tokens/8825
views: 20544
likes: 174
posts_count: 176
---

# EIP-4973 - Account-bound Tokens

Keywords: Non-Tradable, Non-transferrable, non-fungible tokens, NFTs, Soulbound tokens, SBTs, badges

- Original first discussion ISSUE by Nicola Greco in 1238: ERC1238: Non-transferrable Non-Fungible Tokens (NTT) · Issue #1238 · ethereum/EIPs · GitHub
- EIP-4973 Specification Document: EIP-4973: Account-bound Tokens
- Account-bound tokens Working Group on Telegram: Telegram: Contact @eip4973
- GitHub Repository that tracks ERC4973 Reference Implementation: GitHub - attestate/ERC4973: Reference Implementation of EIP-4973 "Account-bound tokens"
- (frequently updated) Blog post that summarizes the Account-bound vs Soulbound debates: What are Account-bound tokens?
- How EIP-4973 Account bound tokens could be used for curating music NFTs EIP-4973 - Account-bound Tokens - #125 by TimDaub
- EIP-4973 allows for mutually agreed, peer-to-peer minting - without implicitly determined power distributions: EIP-4973 - Account-bound Tokens - #129 by TimDaub
- A path towards upgrading “final” EIPs: ERC lightning talk: A path towards EIP upgrading

Feedback, discussions, and comments are welcome.

## Replies

**carlosdp** (2022-04-09):

Thanks for putting this together! I’m not sure I’m convinced it’s necessary to create a new standard for this, though.

`boundTo` is identical in intended functionality as `ownerOf`, but just for an NFT that can’t be transferred, correct? I think `ownerOf` is sufficient, given this. Similarly, `Bound` event is synonymous with a `Transfer` from the null address.

I think all we really need is a way to communicate to clients that the NFT in question is “non-transferrable”, right? I think having that standardized in the JSON metadata would be my instinct on the best place ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

---

**TimDaub** (2022-04-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/carlosdp/48/5831_2.png) carlosdp:

> boundTo is identical in intended functionality as ownerOf, but just for an NFT that can’t be transferred, correct? I think ownerOf is sufficient, given this. Similarly, Bound event is synonymous with a Transfer from the null address.

You are right and so to ensure maximal backward compatibility and minimalism of the interface, I’ve decided to rename `Bond` and `boundTo` to `Transfer` and `ownerOf`.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/carlosdp/48/5831_2.png) carlosdp:

> I think all we really need is a way to communicate to clients that the NFT in question is “non-transferrable”, right? I think having that standardized in the JSON metadata would be my instinct on the best place

From my understanding of Solidity and its surrounding standards, specifically [ERC165](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-165.md): It was exactly built for this type of feature detection functionality. I’ve now specifically mentioned it in the standard’s “[Rationale](https://github.com/TimDaub/EIPs/blob/master/EIPS/eip-4973.md#rationale)” section, but essentially a properly built ERC721 wallet should already be able to detect when a token isn’t transferrable when e.g. the ERC165 identifier [0x80ac58cd](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-721.md#specification) for its transfer function isn’t supported.

As you’re suggesting, having wallets to make an extra asynchronous call is the wrong path in my opinion. Not only may this lead to an immense amount of requests NFT metadata hosts, but it would also ignore the existence and purpose of ERC165.

The reason why in my opinion a new but minimal standards interface is mandatory is that e.g. just `revert`ing on transfers of an ERC721 token is also bad. While e.g. a machine or wallet can indeed detect features using ERC165’s `supportsInterface` function, it cannot interpret whether an ERC721 token’s transfer function fails (e.g. "does it fail because the token is soulbound or e.g. does it fail because of faulty input parameters).

Since, however, `event Transfer` and `function ownerOf` are a part of ERC721’s track and transfer interface, but so is `function transfer`, we’ll have to cut this functionality and reintroduce it as a new interface.

For the future, maybe we can have a non-fungible token with entirely composable ownership properties (e.g. private property, Harberger property, or soulbound property). However, for now this is not the scope of the standard.

---

**carlosdp** (2022-04-10):

I see where you’re going! Making it a subset of ERC721 makes more sense for sure.

One other thing to consider is that it’s likely a reasonable Soulbound NFT implementation technically *would* have a “transfer” function. The “soulbound” part is for the entity, not the literal account itself. We’d still want transfers (or “reclaims” or w/e) to other wallets in the event of a wallet rotation, or compromise, for example. I think it’s fine though, if the main point of the spec is to standardize a value to check for in EIP165. Currently, the spec says Transfer events can only happen in mint/burn scenarios, but I’m not sure that’s necessary to dictate. ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

---

**TimDaub** (2022-04-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/carlosdp/48/5831_2.png) carlosdp:

> One other thing to consider is that it’s likely a reasonable Soulbound NFT implementation technically would have a “transfer” function. The “soulbound” part is for the entity, not the literal account itself. We’d still want transfers (or “reclaims” or w/e) to other wallets in the event of a wallet rotation, or compromise, for example.

Interesting point. I think I agree with you that an account is only a single manifestation of a human/machine’s identity on-chain. So logically, if, e.g., a human/machine’s keys were compromised or necessary to migrate, a “friendly transfer” would allow an otherwise soulbound token to be transferred within an identify’s account ontology.

There are two levels on which we can discuss this feature; once from the philosophical or **name origin** perspective, and secondly on the level of **what’s technically possible**. I’ll do both.

## Name origin

In the ERC4973 document, but also Vitalik’s [post](https://vitalik.ca/general/2022/01/26/soulbound.html) on soulbound tokens, we specifically mention the name stemming from an item’s property of binding to a player’s character upon pickup in World of Warcraft. In V’s post, you can see the “Soulbound” property in the first WoW screenshot.

Here, despite a WoW character being structurally the same abstraction as an Ethereum account is for an identity, a Soulbound item cannot be traded/sent to other characters of the same owner.

In fact, [WoWWiki outlines](https://wowwiki-archive.fandom.com/wiki/Soulbound) a different name for the type of property you mentioned called “Account bound”:

> The item can also become Account bound. It happens to items marked as Binds to account after being acquired by a player. Unlike soulbound items, they can be sent by mail to other characters of the same account and realm, including those of opposing faction (patch 3.3).

## Technical possibility of “friendly transfers.”

Then, independent of any naming, I think allowing “friendly transfers” between accounts of the same identity is not something we’ll be able to control by proposing a Solidity interface.

The purpose of defining a Solidity interface is that many wallets/marketplaces and so on are capable of displaying information that is consistently formatted throughout different implementations. Concisely put: It’s for interoperability.

ERC’s don’t mandate actual behavior implemented as interface definitions. That is why, e.g., there have been so-called “[sleepminting](https://timdaub.github.io/2021/04/22/nft-sleepminting-beeple-provenance/)” attacks on ERC721 tokens as we developers can’t control an implementation’s behavior through a standard document.

E.g., although `function transferFrom(address _from, address _to, uint256 _tokenId)` strongly suggests that a token with id `_tokenId` gets transferred from `_from` to `_to,` it’s not something a specification can define or control. Neither is it a state that a machine can detect as proper or not proper.

If soulbound tokens allowed “friendly transfers,” it’d mean that we had to allow an owner to transfer them to virtually any other address - as we wouldn’t be capable of understanding, on the standard document level, to tell if two accounts are being controlled by the same identity or not.

For soulbound token holders and their respective applications, what I’m suggesting, in case of keys have been compromised, etc., is that there’s some form of migration mechanism between accounts, that for now, the application implements by e.g. re-issuing new soulbound tokens to the new account.

If it were the case that all applications used a similar migration mechanism, it’d make sense also define it as a separate ERC standards document.

## Conclusion

For ERC4973, “friendly transfers” between two accounts of the same identity are out of scope. Still, thank you, [@carlosdp](/u/carlosdp), for poking holes - I appreciate it!

---

**carlosdp** (2022-04-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> In the ERC4973 document, but also Vitalik’s post on soulbound tokens, we specifically mention the name stemming from an item’s property of binding to a player’s character upon pickup in World of Warcraft. In V’s post, you can see the “Soulbound” property in the first WoW screenshot.
>
>
> Here, despite a WoW character being structurally the same abstraction as an Ethereum account is for an identity, a Soulbound item cannot be traded/sent to other characters of the same owner.

In Vitalik’s post, he actually explicitly mentions why these NFTs, in practice, need to be transferable, and has a whole section about different ways to handle that using current and future identity methods:

> POAP has made the technical decision to not block transferability of the POAPs themselves. There are good reasons for this: users might have a good reason to want to migrate all their assets from one wallet to another (eg. for security), and the security of non-transferability implemented “naively” is not very strong anyway because users could just create a wrapper account that holds the NFT and then sell the ownership of that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> Then, independent of any naming, I think allowing “friendly transfers” between accounts of the same identity is not something we’ll be able to control by proposing a Solidity interface.

Right, but that’s kinda my point. Technically, all ERC-721s would currently conform, on an interface level, to this proposed EIP. Specifying restrictions on transfers alone doesn’t necessarily merit its own standard, it has no real “enforce-ability”. We also already see wide reaching examples of tokens with transfer restrictions fitting perfectly fine into their ERC spec.

For example, USDC is an ERC-20 token that maintains a blacklist that can prevent interactions with the contract. In the same vein, couldn’t an ERC-721 just restrict transfers unless the owner can prove they own the `to` address with whatever the implementation deems acceptable?

Having the interface for EIP-165 checks can be useful. For clients, metadata would work fine though. For smart contracts, I’m struggling to come up with an example where a smart contract would want to accept any NFT, as long as it is “soulbound,” as opposed to a specific NFT or just any NFT. Do you have an example in mind, by any chance?

---

**TimDaub** (2022-04-11):

We have to be clear here; despite what others have implemented and whether or not those tokens implement the transfer functionality, strictly speaking, they’re not soulbound according to its definition.

For POAP, it’s great that they made the technical decision not to block the transferability. For any future project not wanting to block transferability, I suggest simply using ERC721. But those projects are not to be confused with soulbound tokens.

I think you’re misinforming your fellow users with this statement, unfortunately - I  doubt you have the authority to control what merits a standard:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/carlosdp/48/5831_2.png) carlosdp:

> Specifying restrictions on transfers alone doesn’t necessarily merit its own standard, it has no real “enforce-ability”. We also already see wide reaching examples of tokens with transfer restrictions fitting perfectly fine into their ERC spec.

The difference between ERC721 and ERC4973 is that they can signal the lack of transfer and tracking functionality with `supportsInterface`. My point is that there’s a relevant difference between implementing a useful feature-detection mechanism (ERC4973) and naively disabling transfer functionality (`revert` in `ERC721` transfer).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/carlosdp/48/5831_2.png) carlosdp:

> For example, USDC is an ERC-20 token that maintains a blacklist that can prevent interactions with the contract. In the same vein, couldn’t an ERC-721 just restrict transfers unless the owner can prove they own the to address with whatever the implementation deems acceptable?

This example is structurally false.

The social contract between USDC and its users is that all transfers generally work, and only unless you’re engaged in criminal activity do they won’t (because you end up on a ban list).

With ERC4973 tokens, the social contract with the users is that no token can ever be transferred. Your example is structurally false as USDC uses their ban list as the last means to circumvent criminal activity. In that case, they don’t care about the criminal’s user experience. Hence just having `transfer` `revert` is fine.

But clearly, we don’t want to treat all soulbound token users as USDC treats criminals…

Instead, if we want to provide a nice user experience on wallets, it is critical making the user understand that they cannot ever transfer certain tokens and, e.g., show advice in a wallet. If we implemented this functionality by having transfer functions `revert` upon calling, it’d create a confusing scenario as it’d require someone to look into the contract code specifically. A machine cannot tell whether a `revert` within a tokens transfer function means: (1) the token is soulbound, (2) the user has entered the wrong inputs (3) a myriad of other possibilities.

Since ERC4973 can signal transfers not being implemented via `supportsInterface` and since ERC721 can signal transfers being implemented, an ERC721 with disabled transfers cannot signal any specific information to a wallet. It can just notify the user that the on-chain call they’re about to send will fail - which is a really bad user experience.

Instead, with ERC4973, the transfer button can, thanks to `supportsInterface`, be hidden when the token is displayed. Potentially, the wallet implementer can even choose to educate the user about this new type of ownership experience.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/carlosdp/48/5831_2.png) carlosdp:

> For smart contracts, I’m struggling to come up with an example where a smart contract would want to accept any NFT, as long as it is “soulbound,” as opposed to a specific NFT or just any NFT. Do you have an example in mind, by any chance?

To me, having ERC4973 get adoption can be the start of a new chapter. So far, we’ve implicitly assumed that all blockchain properties must have tracking and transfer functionality according to the societal norm that is “private property.”

ERC4973, a token that doesn’t make many implicit assumptions, can challenge these perceptions by, e.g., allowing someone to soulbound a token to a smart contract and then implementing wildly new ownership concepts.

Within Radical Exchange’s “Partial Common Ownership” concept working group, we’re exploring what properties “Harberger Property” would exhibit, and SBTs owned by smart contracts may be a good foundation.

---

**carlosdp** (2022-04-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> I think you’re misinforming your fellow users with this statement, unfortunately - I doubt you have the authority to control what merits a standard:

I don’t see how I’m misinforming anyone? You’re the one that brought up the Vitalik article (which coined the very term “Soulbound NFT”), I simply pointed out that in that very article, he himself points out there’s a good argument for why Soulbound NFTs will probably need some form of transferability (using a direct quote from the article, mind you). If you disagree, that’s fine, and I’ll disagree with you there too. That’s not misinformation, that’s disagreement ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

And no single person has authority over what merits a standard, that was simply my individual opinion.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> The difference between ERC721 and ERC4973 is that they can signal the lack of transfer and tracking functionality with supportsInterface. My point is that there’s a relevant difference between implementing a useful feature-detection mechanism (ERC4973) and naively disabling transfer functionality (revert in ERC721 transfer).

Yea, and again, I agree there could be some utility there.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> But clearly, we don’t want to treat all soulbound token users as USDC treats criminals…

I’m not advocating that…

I don’t think my example is “structurally false.” The use-case is irrelevant, it doesn’t say anywhere in the ERC-20 spec “you can blacklist accounts from using transfers, but only if they are criminals.” It doesn’t mention it at all. But the consensus is clearly that USDC is still an ERC-20 token, ergo my point is it’s easy to extrapolate that a transfer-restricted ERC-721 would still be considered an ERC-721. That’s all I’m saying.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> To me, having ERC4973 get adoption can be the start of a new chapter. So far, we’ve implicitly assumed that all blockchain properties must have tracking and transfer functionality according to the societal norm that is “private property.” …

That’s all fine! Given that one of your arguments for why this needs to be an EIP for an interface definition, rather than metadata, is so smart contracts can detect that they are Soulbound NFTs, I’d strongly recommend at least having one example of where that functionality would actually be useful to developers in a smart contract. Standards are generally meant to standardize already well-understood functionality, not hypothesize and hope it inspires a use-case. ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

---

**TimDaub** (2022-04-12):

Last night, [@ligi](/u/ligi) referenced the standards document on Twitter and made a deontic statement for why soulbound items should be “friendly transferrable” between accounts of the same soul/identity:

Nitter: [ligi ☮️🌍🚲🌳🍵🎶🌶🔥🖖 (@mr_ligi): "Interesting proposal by @timdaub: https://github.com/ethereum/EIPs/pull/4973 That said I do not think soul-bound tokens/badges/.. should be bound to a single key (by just removing the transfer functionality) - but it needs to be bound to a identity/soul that still has the ability to rotate keys." | nitter](https://nitter.net/mr_ligi/status/1513436923125280768#m)

In this post, I want to address why I think this requirement is unnecessary.

I. Soulbound items don’t mandate single key locking. Keys can be rotated: If a user is unsure about the permanence of their EOA account, but from an app it is suggested that a soulbound item could be sent there, the user could e.g. create a Gnosis Safe multisignature contract with an X out of Y signature scheme.

In that way, although keys out of X might go missing, leak or getting revoked, still the user’s soulbound items would still be available at the multisignature contract albeit with new keys controlling the vault.

II. In addition, when EOA or even contract access is lost, the soulbound token specification doesn’t make normative statements about whether those tokens ought forever to be lost or not. Rather, since a soulbound item’s recovery is anyways not automatable by a Solidity interface, the dapp originally issuing the items ought to take care of potential reissuance.

If e.g. badges are sent to known users certifying their education credentials, I see no reason for a school to not issue the same badges yet again to another new account if it’s clear that the user lost access to the old account. Any other process could be possible too. The point is that it is outside of the specification’s scope to handle administrative migration.

To implement (II.), however, it could be useful giving an issuer the option to `revoke` old credentials on e.g. lost accounts. Specifically to avoid duplication.

Then, on a philosophical level, I want to address the criticism that Ethereum isn’t ready because we can’t differentiate identities or souls yet, so how can we have “soulbound items.”

For this, it is critical to understand the name origin of the term and how WoW’s ontology applies to that of Ethereum. Within a logical statement, one could say that

Identity to WoW account as is EOA Account to WoW Character.

Albeit it potentially being confusing given the ambiguous use of similar terminology, I want to stress again that soulbound items within a WoW character’s bags were not transferrable to other characters of the same account/player. Likewise, if a player lost access to a character (e.g. by deleting it through a fat finger), they also subsequently lost access to all soulbound items and would only regain access to them by having the character being recreated by e.g. a gamemaster from Blizzard.

For the scope of this specification, I want to say that it is very narrow, deliberately opinionated, and directed towards replicating that dynamic.

I understand that with e.g. increased sophistication “better” standards could be built - but that is not the goal! Instead, the goal is to define the minimal interface for soulbound tokens as a new property class and ownership experience and see what develops from there. If there are other, “better”, soulbound property standards that e.g. allow friendly, transfers between accounts of the same soul - that’s fine, but it was never the goal of this specification.

---

**ligi** (2022-04-13):

I see your points - but I would really not call it SoulBound then - it’s more AccountBound. A human can only have one Soul - but multiple Accounts.

Sure you can mitigate by expecting users to use a smart-contract wallet to be able to rotate keys - but current reality is most users don’t (also see Vitaliks post: https://vitalik.ca/general/2022/03/29/road.html )

> We also (very wrongly!) expected most users to quickly migrate to smart contract wallets

Also you can push the responsibility for reIssuance on the issuer - but IMHO this is one the crucial problems in this area.

And really do not get me wrong - I did not want to belittle your effort - I just wanted to emphasize that IMHO we need good identity solutions as a building block to build that proper. Still sad that there is not yet a strong solution like Idena on Ethereum. Really hope this changes with Ethereum scaling - currently it is just to expensive to build it on Ethereum.

---

**TimDaub** (2022-04-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> I see your points - but I would really not call it SoulBound then - it’s more AccountBound.

It makes sense to discuss a name change away from “Soulbound.” On one side, it’s a shame as the community is interested in “Soulbound” tokens since it’s a great marketing name. On the other side, I can see that it may create confusion when related to the actual functionality.

In WoW, I guess making an item soulbound was OK as the context was a player playing a character and hence the item binding to the character’s soul, despite a human being able to have multiple characters but just one soul.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> Also you can push the responsibility for reIssuance on the issuer - but IMHO this is one the crucial problems in this area.
> And really do not get me wrong - I did not want to belittle your effort - I just wanted to emphasize that IMHO we need good identity solutions as a building block to build that proper. Still sad that there is not yet a strong solution like Idena on Ethereum. Really hope this changes with Ethereum scaling - currently it is just to expensive to build it on Ethereum.

From a practical standpoint, I can’t entirely agree here. Yes, it’s cool working towards *actual* soulbound tokens that work with sophisticated identity solutions. But anyone always using the “first adoption then standard” meme, I’d like to invite you to increase the horizon of experience.

For ERC721, when I first saw the standard around its creation, relatively speaking to today’s adoption, it didn’t have adoption. There were times when it had so little adoption that I thought about just ignoring or doing my standard.

I interpret the situation such that the Ethereum community came up with a rather decent document that everyone could agree on. Then, the community built the apps (and then, just recently, the actual adoption came). The document (eip-721.md) was a precursor to mass adoption, not vice versa. But I’m probably alone with that opinion.

But for me, defining this minimal standard has been interesting as I see it rather as a very big sales filter. I’ve been contacted by clients wanting to build towards it. People are looking at this document, and they are commenting. So it’s useful that it exists and that people discuss it. Whether or not it will become a successful standard, only time can tell. But to me, just throwing it out there and, e.g., “soul” binding to an address, can be an interesting use case - maybe not the one that everybody here’s thinking about. Gladly we don’t have a limit on storage space on the EIP document repository. And we won’t run out of natural numbers either lol.

---

**TimDaub** (2022-04-18):

Updates from 2022-04-18:

- Added section on revocations.
- Changed name to “Account-bound tokens.”
- Added section on exception handling in cases of key loss.

---

**TimDaub** (2022-04-23):

Presented the draft at OGCouncil in Amsterdam at the NFT Standards WG session: https://mobile.twitter.com/vrde/status/1517851423463157761

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/9/96534a0b65edfed24cb31642257d266c89198ffb_2_666x500.jpeg)image1920×1440 189 KB](https://ethereum-magicians.org/uploads/default/96534a0b65edfed24cb31642257d266c89198ffb)

---

**Shymaa-Arafat** (2022-04-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> If e.g. badges are sent to known users certifying their education credentials, I see no reason for a school to not issue the same badges yet again to another new account if it’s clear that the user lost access to the old account. Any other process could be possible too. The point is that it is outside of the specification’s scope to handle administrative migration

I was wondering a few days ago, what if a say malicious person persuaded a succeeding user to sell him/her the success NFT badge?

I mean without the administrative educational authority interference:

**Is it already there in ERC-721 that users who possess badge NFTs can’t resell them?**

---

**TimDaub** (2022-04-26):

More feedback from [NFT Standards Working Group on Telegram](https://t.me/+sZU_O9t3P4A1OWQ0). Copying here for visibility and posterity:

> Simon / dievardump:
> I don’t understand the idea of boundTo / Bond
> If the contract supports the right interface ownerOf is more than enough to know to which person it is bound, since there won’t be any transfer possible
> You’re complicating Wallets implementation with this.
> I would suggest to only have the supportsInterface(NonTransferableNFT)
> Which would tell wallets to hide all transfer / approval stuff but still be able to use the same suite of tools for all the rest (ownerOf)

> iain nash:
> Additionally, if you want to have provenance for migrated wallets an cross signed admin transfer makes sense. Reverting on transfer to accomplish this or not implying those functions makes sense to me.

> Tim:
> We changed from Bound/boundTo to Transfer/ownerOf recently. Maybe you had an outdated version of the github PR open? A discussion can be found on Ethmagicians.

> Tim:
> In ERC721, unfortunately transfer + approves are combined with ownerOf in one interface, so since we’re not implementing that interface, it’s necessary to re-add parts of it (ownerOf and event Transfer)

> Tim:
> If implementers of 4973 want to implement admin migration transfer they can choose to do that. The standard won’t recommend any norm in that scope. But, account-bound tokens are account-bound , so in some cases migration may not be wanted. Implementers can do as they please. Since, however, revocation is possible, I’d assume that implementers would prefer to migrate by revoking an “old” credential from an old account and minting a new one to a new account as it creates a provenance structure too. But IMO both options can make sense and I wouldn’t want to judge what is better. But actually to formally integrate the usecase of admin migration, I think I’d be helpful to outline it in the spec, where e.g. both “from” and “to” are non-zero addresses

> Tim:
> Generally, if implementers prefer to revert on transfer, they should probably use erc721 and others as they fit better. E.g. for banlists

---

**TimDaub** (2022-04-26):

Feedback from the [partialcommonownership.com](http://partialcommonownership.com) [Discord](https://discord.gg/yJjAeMVvqK):

> @will-holley [responding to @timdaub posting link to ERC4973 spec]: I read through your spec. How are you thinking about transferability in the context of wallet compromise / security?

> @timdaub see: EIPs/EIPS/eip-4973.md at 15527ff7d5f847cb8819e70e9043a5de8b2f869b · ethereum/EIPs · GitHub
> Actually Iain from Zora told me he’s gonna complain about this section on Eth magicians and that e.g. admin migration should be considered in the provenance record of emitting event Transfers. So that section will expand

> @will-holley: That makes sense to me as well; if the EIP is agnostic to transfer-implantations, the transfer even should be removed.

> @timdaub: 1. I think it makes sense having the event Transfer in there as from what I understand it is the primary source of clients for crawling provenance e.g. etherscan, thegraph. Rather, I think it’s a matter of carefully defining how actions map to parameters in the event Transfer e.g. what equates “minting”, “revocation”, “admin migration”

> @will-holley: Perhaps a different name then transfer. event Attest

> @timdaub: Yeah we had event Bond before with the same inputs as event Transfer . But e.g. from the NFT standards working group & on Eth magicians I’ve heard people favoring event Transfer actually

---

**will-holley** (2022-04-26):

Thanks for directing me to the thread, [@TimDaub](/u/timdaub).

Elaborating on Tim’s post above, the `Transfer` event should be renamed to `Attest` because the implementation is transfer-agnostic by default and account-bound tokens are granted based on the attestation of issuing contract.  By definition, attestations cannot be *transferred*, because they are simply proofs of state, rather than state itself.  They can, however, be revoked and re-issued, which I believe more accurately captures the intent of `event Transfer`.

As an aside, this account-binding is most effective when this issuing contract is administrated by a third-party (rather than the first party who could arbitrarily transfer their tokens via burn/mint/burn).  As such, this third-party acts as the arbiter of truth, attesting to the network what (ideally) the network has incentivized to be a true (rather than false) positive attestation.  As long as the incentive to attest true negatives holds, `Attest` rather than `Transfer` is a more accurate description.

---

**ra-phael** (2022-04-26):

As I mentioned during the OG Council, I also share the view that a “Transfer” event sounds confusing to me in a standard that is all about non-transferable tokens.

Instead there could be `Attest` and `Revoke` events, or even more neutral `Mint` and `Burn` which are familiar terms for tokens.

> As an aside, this account-binding is most effective when this issuing contract is administrated by a third-party (rather than the first party who could arbitrarily transfer their tokens via burn/mint/burn). As such, this third-party acts as the arbiter of truth, attesting to the network what (ideally) the network has incentivized to be a true (rather than false) positive attestation.

I agree that’s probably most use cases but I think we should also keep in mind that self-attestations could be possible where users would call a function and get a non-transferable token if they meet some conditions defined in the smart contract. In that case there’s no third-party, the blockchain acts as the arbiter of truth.

---

**TimDaub** (2022-05-04):

It’s becoming clearer that the concept of `event Transfer` may not be fully capable of depicting what we’re looking for when creating an ACT ontology.

E.g., [sleepminting](https://timdaub.github.io/2021/04/22/nft-sleepminting-beeple-provenance/) attacks implemented with EIP-721 contracts have made it clear that many developers and users had false assumptions about what an ERC Solidity interface can achieve.

To reiterate, despite `event Transfer(from, to , id)` suggesting that, e.g., a token with an `id` was sent `from` an account `to` another account, it’s an implementer’s choice to make sure that upon emitting `Transfer,` `from==msg.sender`. But really, the implementer is free to set any argument of `event Transfer` to their liking.

Sleepminting attacks exploit this fragile and implementation-scoped assumption by deliberately setting false addresses in `from` and `to`.

For me, to stay practical, the question within this dilemma is what we can do to create an authenticated ontology of tokens where it’s not necessary to have a human individually review every interface compliant contract - as implementation behavior can technically always diverge. For E.g. it’s important that a website like Etherscan shows authenticated data.

Instead of asking implementers to honestly set `from/=msg.sender` (or `to`) in all implementations, I think it’s less fragile and safer to remove the `from` key from the event and instead ask indexers to substitute it with the `from` key of the transaction that is authenticated through Ethereum’s PoW algorithm (miners check the transaction’s signature - so we can be sure the `from` field is authenticated).

Then, in a further attempt to improve the `event Transfer` concept for creating on-chain provenance, I second the argument of [@will-holley](/u/will-holley) and others that its naming is imprecise.

I agree that `event Attest` and `event Revoke` better identify the user’s actions. However, I also liked `event Transfer`'s convention of allowing to depict e.g., minting `from=0x0` and burning `to=0x0`.

Since, however, as we’ve discussed above, we must anyways not use the `from` field within `event Transfer` to suggest it contains authenticated information, I now agree with using `event Attest` and `event Revoke` just with two parameters: `id` and `to`.

It’s because what this allows us to build is an indexer that uses authenticated information while still being able to index based on `to` and `id`.

Hence, my suggestion is to replace `event Transfer(from, to, id)` with:

- event Attest(to, id) where the from field is taken from the transaction’s from; and
- event Revoke(to, id) where the from field is taken from the transaction’s from; and

---

**TimDaub** (2022-05-05):

Update 2022-05-05:

- Replaced event Transfer with Attest/Revoke logic
- Addressed most PR feedback

---

**MicahZoltu** (2022-05-06):

This is probably discussed above (I haven’t read the whole discussion), but I’m pretty strongly against this concept.  Users **MUST** be able and encouraged to rotate their keys regularly, and especially when compromised.  I would be less bothered by this specification if it explicitly prevented EOAs from owning assets, and everything had to be owned by a wallet of some kind.  However, that prevents people from upgrading/migrating wallets when there is a problem with the wallet or a better version comes out, which is nearly just as bad of a problem.


*(155 more replies not shown)*

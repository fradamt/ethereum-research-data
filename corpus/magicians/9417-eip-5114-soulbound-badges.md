---
source: magicians
topic_id: 9417
title: "EIP-5114: Soulbound Badges"
author: MicahZoltu
date: "2022-05-30"
category: EIPs
tags: [token, ntt, badges]
url: https://ethereum-magicians.org/t/eip-5114-soulbound-badges/9417
views: 9359
likes: 46
posts_count: 95
---

# EIP-5114: Soulbound Badges

Discussion for soulbound (ERC-721) tokens.

## Replies

**TimDaub** (2022-05-30):

thanks for your submission, I’m happy you’ve taken this step and I think there’s now more fascinating questions we can ask.

E.g. in the document you remark that:

> Soulbound tokens are meant to be permanent badges/indicators attached to a persona. This means that not only can the user not transfer ownership, but the minter also cannot withdraw/transfer/change ownership as well.

But this makes me wonder that since you’re removing any “token-like” functionality, if it is still useful calling the standard “soulbound *tokens*”, when indeed its functionality is more akin to, as you remark yourself, badges/indicators/items etc.

---

**MicahZoltu** (2022-05-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> But this makes me wonder that since you’re removing any “token-like” functionality, if it is still useful calling the standard “soulbound tokens”, when indeed its functionality is more akin to, as you remark yourself, badges/indicators/items etc.

This is a good point.  Perhaps Soulbound Badges would be a better name?  I’m not opposed to changing the name.

---

**aditya0212jain** (2022-05-31):

Thanks for this PR! Had a couple of thoughts:

1. What are your thoughts on having a ‘Burn’ event. Since there is no approval required for minting a Soulbound token for any NFT, many people may get unwanted tokens that they would like to get rid of. Or it may happen that the minter would like to revoke the soulbound token given to an NFT due to some malicious activity in the future.
2. Moving the tokenUri and collectionUri to another interface that can act as a metadata extension (along with ‘name’ and ‘symbol’ functions) as done for ERC721.

---

**MicahZoltu** (2022-05-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aditya0212jain/48/6058_2.png) aditya0212jain:

> What are your thoughts on having a ‘Burn’ event.

This would break the immutability of soulbound badges/tokens.  One of the benefits of immutability here is that once assigned, applications can aggressively cache results because they have high confidence that a token cannot be removed, reassigned, moved, mutated, changed, etc.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aditya0212jain/48/6058_2.png) aditya0212jain:

> Moving the tokenUri and collectionUri to another interface that can act as a metadata extension

If they are not part of this standard, then they should be moved to a different EIP.  I did consider this, but I felt that it was important to emphasize the immutability constraints within this EIP so it was clear that these badges were immutable through and through.  It is worth noting that the content of the URI is delegated to future EIPs, but I’m hesitant to move even more.

Re: name/symbol: I feel like this information should live at the URI.  It is descriptive metadata about the token, and these tokens are likely useless without the metadata (e.g., without image/description/details).  If readers are going to have to lookup some metadata externally anyway, it feels like all of the token metadata including name/symbol should live there rather than being split on and off chain.

---

**MicahZoltu** (2022-05-31):

This standard represents a non-fungible, non-transferable, non-separable asset.

Naming thoughts:

- Non-Fungible Badge (NFB)

Pairs well with NFT.

Soulbound Badge (SBB)

- Follows the soulbound naming convention, but makes it clear this doesn’t have token-like properties.

Soulbound Token (SBT)

- Leans on the Soulbound Token meme that is currently going around.  This isn’t an ideal name, but it would be nice if this is what people thought of when they talk about Soulbound Tokens, rather than some other standard that decides to do a name grab.

Badge

- Do fungible badges make sense?  If so then NFB adds clarity over just Badge.  If fungible badges don’t make sense, then perhaps the NF is redundant.

---

**tomcohen.eth** (2022-05-31):

First, YES. I like the generic-ness of this standard better than 5107’s (the superset discussion).

Second, about the immutability in the tokenuri:

I think there’s value in immutable soulbound tokens but there is also value in mutable ones - and I’m not sure they need to be separate standards. If the goal is non-separateness of tokens, nothing mandates that the tokens themselves shouldn’t contain mutable references that can be updated and evolve over time. It seems like a different goal (which would be a great standard to have regardless).

I understand the goal is minimising the ability of the owner/minter to “effectively” burn the token by changing it, but the documentation of past settings is still on the chain in case of a dispute.

Example use-case: a soulbound token representing a government ID. The token itself represents the personhood of the holder with their government ID, and is bound. The Metadata though can contain mutable information: legal name, photo ID, etc.

It’s useful, and since it’s useful people will end up doing it and in practice what we’ll see is 5114 tokens with IPFS links that point to HTTP links.

We can, and should, **encourage** implementations using immutable pointers and have mutable be used only if there’s a strong use-case for it - but not outright mandate it.

Third, regarding naming:

With names I tend to think familiarity and clarity are the most important bits. The soulbound concept is already known and popular, as well as the idea of a token (the token-badge distinction doesn’t seem meaningful to me). People who are already familiar with the soulbound token concept generally think of something similar to what is being implemented here. We can come up with something else, but that would require the unnecessary socialisation of a new name.

---

**somcha.eth** (2022-05-31):

Consider me a noob here. Just sharing an idea on Soulbound Badge/NFT to eradicate the unwanted tokens getting associated with the user as [@aditya0212jain](/u/aditya0212jain) mentioned

Consider a process that can be broken down in two parts 1. issuance 2. claim

On **issuance** the issuer of the soulbound nfts simply triggers _mint on address(0) and set _tokenApprovals[<token_id>] = <claimer_address>. This step can be done by overriding _mint and removing the require checks of `to != address(0)`

**claim** will be trigger by the claimer which in turn will map the msg.sender as owner and resetting the approver to address(0).

claim will have a requirement of msg.sender as approver. This will block any further calls of claim

There are of-course few more changes required. Again might sound stupid.

---

**MicahZoltu** (2022-05-31):

[@somcha.eth](/u/somcha.eth): I think this can be solved per-token and doesn’t need to be standardized.  What matters is just that the `mint` event isn’t fired until both parties agree in this case.  I would certainly support what you described, I just think it is a Best Practice, not a Standard.

[@tomcohen.eth](/u/tomcohen.eth) While I agree that some people will *want* what you have described in terms of mutable badges, I personally think that it isn’t following the spirit of soulbound immutability that I think is valuable.  For example, if you change your name that should result in a new name token being issued.  You would still be Alice, but you just now are *also* Bob.  You can never become not-Alice, else the badges no longer hold their immutable guarantee.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tomcohen.eth/48/6134_2.png) tomcohen.eth:

> we’ll see is 5114 tokens with IPFS links that point to HTTP links.

If they do that, they aren’t an EIP-5114 token.  ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) Certainly, we can’t stop people from developing whatever they want, but if you don’t follow the spec then it isn’t an EIP-5114 token.

---

**toledoroy** (2022-05-31):

![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12) what do you think about soulbound badges that are owned (attached to) the soulbound tokens…

I.e. tokens that are owned / attached to the owner of another token.

---

**MicahZoltu** (2022-06-01):

This is mentioned in the Security Considerations section:

> It is possible for a soulbound token to be bound to another soulbound token. In theory, if all tokens in the chain are created at the same time they could form a loop. Software that tries to walk such a chain should take care to have an exit strategy if a loop is detected.

---

**MicahZoltu** (2022-06-01):

Migrating discussion with [@TimDaub](/u/timdaub) from the PR to here regarding the terminology and requirements around immutability.

IIUC, there are two separate concerns being discussed:

1. Should we constrain the system such that it badges cannot mutate/change under reasonable operating assumptions?
2. How should we express this concept to the user.

For (1) I feel pretty strongly that for something to be compliant with this standard, it **MUST** be indefinitely cacheable, which means there needs to be a reasonable assumption that the data will not change.  For data that isn’t content addressable, we cannot ensure this guarantee and if the remote data does change we may run into a problem where users don’t have a way to validate truth.

For (2) I’m much more open to alternative wordings.  At the moment I disagree with [@TimDaub](/u/timdaub) that immutable is the wrong word.  While *technically* true that immutable data *can* be mutated, for many systems (like IPFS, Immutable datastructure libraries, immutable databases, blockchains, etc.) this is only true under bizarre scenarios like a user who is intentionally breaking their own ability to validate data or where there are critical bugs/attack vectors in the software being used.

---

**tomcohen.eth** (2022-06-01):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> For example, if you change your name that should result in a new name token being issued. You would still be Alice, but you just now are also Bob

And these tokens won’t have the same ID. Meaning that for all purposes the issuer issued two identities to the same person. So now we’re forcing out-of-band revocation processes to prevent sybil attacks and inform consumers of the token which is the “correct” token.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> You can never become not-Alice, else the badges no longer hold their immutable guarantee.

The discussion is about if ERC5114 **should** contain an immutability guarantee - so the lack of immutability can’t be a counterargument.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> If they do that, they aren’t an EIP-5114 token.  Certainly, we can’t stop people from developing whatever they want, but if you don’t follow the spec then it isn’t an EIP-5114 token.

You follow the spec to the letter: the tokenURI is an IPFS file. It’s just that this file then redirects, references, or points to an HTTP resource. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**MicahZoltu** (2022-06-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tomcohen.eth/48/6134_2.png) tomcohen.eth:

> Meaning that for all purposes the issuer issued two identities to the same person.

These tokens (and really *any* similar token) should not be assumed to be limited to 1 person, 1 identity.  It is functionally impossible to solve the 1 person, 1 identity problem and I think that should be made abundantly clear to all users/developers (perhaps I should add something to security considerations).

It also may be valuable to add a mention that these tokens are intentionally irrevocable, just to help drive home the point that these are not meant to be used as a permission/security system.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tomcohen.eth/48/6134_2.png) tomcohen.eth:

> You follow the spec to the letter: the tokenURI is an IPFS file. It’s just that this file then redirects, references, or points to an HTTP resource.

I believe this is handled with this requirement:

> // any external links referenced by the content at tokenUri also MUST follow all of the above rules

---

**TimDaub** (2022-06-01):

Instead of all this arguing about how a tokenUri should be structured: How about renaming tokenUri to e.g. getMultiHash to make it abundantly obvious and required that the Soulbound Badge must be a hash resolvable through IPFS?

- Multihash

Edit: IMO it’d be hella interesting if we had an EIP that gave recommendations for what are good URIs and what aren’t when used in e.g. smart contracts. Right now, and in the NFT space, there’s so much confusion and continuous discussion around this field and there’s no high quality document that outlines the pros and cons for various URI forms on blockchains.

IMO URI guarantee discussion is out of scope of Soulbound tokens. We should have a separate “what are good and bad URIs EIP document” and then reference it in the Soulbound Badges scope.

---

**SamWilsn** (2022-06-03):

+1 for Soulbound Badges

---

If you aren’t standardizing the content of `tokenUri` and `collectionUri`, I would argue that those functions shouldn’t be part of your interface at all. If multiple incompatible standards arise for EIP-5114 metadata, and they all use the same `tokenUri` function, a contract would not be able to implement more than one of them.

---

Further, I think these tokens should implement [EIP-165](https://eips.ethereum.org/EIPS/eip-165), which would let dapps detect these tokens, *and* which metadata extensions they support.

---

I think the requirement that URI’s be censorship resistant and durable is going beyond what can be enforced by a standard. It’s simply too easy for a token viewing dapp to ignore that requirement and support HTTP(S).

That said, if you were to *force* a particular data storage standard (for example drop the `ipfs://` prefix, and require that all URI’s be IPFS implicitly) then it wouldn’t be possible to bypass the requirement.

Another option would be to allow *any* URI, but also require a content hash function. That would at least provide immutability and allow any honest archivist to prove they have the correct data for a given block.

---

**MicahZoltu** (2022-06-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> How about renaming tokenUri to e.g. getMultiHash to make it abundantly obvious and required that the Soulbound Badge must be a hash resolvable through IPFS?

I don’t want to constrain to only IPFS, only to content that doesn’t change.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> interesting if we had an EIP that gave recommendations for what are good URIs and what aren’t when used in e.g. smart contracts

EIPs are for standards, not best practices.  I agree that such a document should exist, just not as an EIP.  I recommend a blog/article or static website that people can link to.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I think the requirement that URI’s be censorship resistant and durable is going beyond what can be enforced by a standard. It’s simply too easy for a token viewing dapp to ignore that requirement and support HTTP(S).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> IMO URI guarantee discussion is out of scope of Soulbound tokens.

I argue that guarantees around what can be cached, how aggressively, and what security guarantees there are for the data **SHOULD** be part of a standard, as it is part of the interface between different actors communicating via this standard.  In this case, the standard is asserting that the data can be cached indefinitely, and that the caller can verify the integrity of the data client side.  The specifics of how that is achieved are up to individual implementations.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> If you aren’t standardizing the content of tokenUri and collectionUri, I would argue that those functions shouldn’t be part of your interface at all. If multiple incompatible standards arise for EIP-5114 metadata, and they all use the same tokenUri function, a contract would not be able to implement more than one of them.

I can appreciate the argument here but I’m hesitant to lock in a data format standard in this EIP as one can imagine several competing standards on that front that build off of this EIP, yet I find it useful to give strong guarantees about the immutability of these tokens and make it clear what they are meant to represent.

---

**MicahZoltu** (2022-06-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Further, I think these tokens should implement EIP-165, which would let dapps detect these tokens, and which metadata extensions they support.

You aren’t the only one.  My tentative plan is to add EIP-165 support after this is merged as a draft.  I need to spend some time figuring out how to do that, and I don’t want it to hold up merging as a draft.

---

**TimDaub** (2022-06-04):

My biggest concern with this EIP is that it practically has no one asking for it.

With EIP-4973, I drafted a standard to institutionalize non-transferrable tokens such that e.g., we stop the malpractice of “soul binding” NFTs to accounts with `revert`ing on `transfer` and `transferFrom`. I did so because of a practical technical problem I had faced in the https://partialcommonownership.com/ working group where we were discussing if Harberger property should be friendly transferrable or not.

So originally, EIP-4973 was simply a means to contribute to that discussion. Way before Vitalik et. al’s paper we foresaw this problem at ETHDenver and I wrote about it: [Non-Skeuomorphic Harberger Properties may not be implementable as ERC721 NFTs](https://timdaub.github.io/2022/02/19/non-skeuomorphic-harberger-properties-erc721-nfts/) That’s how EIP-4973 came about.

Then, after some time, people that wanted to mint badges found EIP-4973 interesting too. In fact, for more than a month, I’ve been now directly iterating as a freelancer with two startup companies in the space. We’ve met up in Amsterdam and Berlin to further discuss EIP-4973. It is my conviction that we’re doing something that’ll eventually help their products. EIP-4973 is a product of the problems of people building in the space.

So having done all of this work, and we’ve also documented lots of it in the EIP-4973 discussion thread, I have to say that I don’t “get” EIP-5114.

To me, it is a nice and elegant theoretical solution to what was laid out in Vitalik et al.'s paper. I can see lots of great new things happening when tokens can be bound to other tokens. It’s seriously interesting.

But at least until now, I don’t know anyone that needs this. I’m not aware of one project that has done what is described here. And contrary to that, there are now countless NTTs on Ethereum all using `revert` to achieve what is properly laid out in EIP-4973.

So I was wondering, to the authors: Do you think EIP-5114 and EIP-4973 do fundamentally serve different use cases, and should they go towards standardization in parallel? Or rather, as [@MicahZoltu](/u/micahzoltu) you’ve framed it in the EIP-4973 discussion thread, should EIP-4973 fail (and EIP-5114 take over?)

---

**MicahZoltu** (2022-06-04):

I’m not sure if the question is directed at me (the only author) or someone else, but I’ll answer none the less.  ![:laughing:](https://ethereum-magicians.org/images/emoji/twitter/laughing.png?v=12)

As I have mentioned elsewhere, I think that permanently binding assets to Ethereum addresses is a *really* bad idea.  I created this so when people go looking for standards around permanently binding assets, they’ll hopefully stumble on this and ultimately choose to *not* bind assets to addresses.

Just because people want/do a thing doesn’t mean it is a good idea for the ecosystem, society, or users.  While I believe people should be free to do what they want, I will still encourage people to do what I believe is best for society/end-users.  Binding assets to addresses may be good/simple for developers, but it is not good for users long term and thus I advocate pretty strongly against it, even if it is what people think/say they want.

People also want custodial coins, censorship, government backdoors into software, no financial privacy, etc. and these are all things that I similarly advocate and develop against.

---

**TimDaub** (2022-06-06):

In EIP-4973 we do not advocate for perma-binding assets to addresses. We put revocation mechanisms into the hands of e.g. the contract implementers. ERC20 and ERC721 do that too, they don’t enforce implementation, just interface definition. E.g. I think we should standardize that ABT receivers can disassociate themselves on-chain. But how to do it? Your help would be useful.

Rather than going on your own, I’d be happy if we could integrate solutions to your concerns in EIP-4973 somehow.


*(74 more replies not shown)*

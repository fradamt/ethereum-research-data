---
source: magicians
topic_id: 9814
title: FINAL EIP-5192 - Minimal Soulbound NFTs
author: TimDaub
date: "2022-06-30"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/final-eip-5192-minimal-soulbound-nfts/9814
views: 10347
likes: 33
posts_count: 50
---

# FINAL EIP-5192 - Minimal Soulbound NFTs

Information:

- Final Specification: ERC-5192: Minimal Soulbound NFTs
- Reference Implementation: GitHub - attestate/ERC5192: Reference implementation of ERC5192 Minimal Soulbound Tokens
- PEEPanEIP #89: EIP-5192: Minimal Soulbound NFTs with Tim Daubenschütz by the Ethereum Cat Herders.

## Replies

**DAYvid** (2022-07-01):

I’m really impressed by the simplicity of this EIP! It accomplishes its goal in an elegant way, and its goal is the most minimal increment of a long-term feature. Perfect!

---

**kladkogex** (2022-07-01):

One problem with never being able to transfer the token is that

you will never be able to rotate the corresponding crypto key.

From this perspective it is not clear at all whether it should be an extension of a NFT.

It should probably be more like a map of User_ID to public key pairs, where the UID is randomly set at creation, and you can rotate a key corresponding to a UID

---

**TimDaub** (2022-07-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> One problem with never being able to transfer the token is that
> you will never be able to rotate the corresponding crypto key.

This is out of scope, has been extensively discussed in EIP-4973 and frankly it is wrong. The standard doesn’t require the token holder account to be an EOA. An account can be represented by a contract. We’re all responsible users and lecturing people what not to do is IMO not the role of the EIP process/document.

---

**aram** (2022-07-03):

[@TimDaub](/u/timdaub) I read various posts, discussions and documents, and really appreciate your (and ra-phael and MicahZoltu’s) efforts around this topic.

With the idea of trying to start with a minimal first-step, I was wondering how about introduce a very simple function (and therefore an interface) that checks transferability (or boundedness) of a token?

```auto
function locked(uint256 tokenId) external view returns (bool)
```

This will allow wallets to check for transferability for UX, allows implementers more freedom around mint/burn and maybe even allowing transfers in certain situations. Lastly the `supportsInterface()` will have a more meaningful role when it says that it supports transferability/boundedness checks.

If you think this is a different can of worms I can move this suggestion somewhere else.

Let me know what are your thoughts, as you’ve been working on this for quiet a while ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**TimDaub** (2022-07-09):

yeah, [@aram](/u/aram) I think this is a good idea as it’ll still allow someone to inseparably bind a token to an account, but leave that choice to the user (which IMO should ultimately have the freedom of decision).

The effect is that it can shut up the nay-sayers arguing for better key rotation practices in SBTs as the interface is neutral towards the concept of permanent locking.

Here’s what I suggest: Please send the proposed interface design change to my GitHub TimDaub/EIPs so that I can propose it to ethereum/EIPs, thanks!

---

**walterKomarek** (2022-07-17):

account abstract，，，，，，，，，

---

**TimDaub** (2022-07-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aram/48/5696_2.png) aram:

> function locked(uint256 tokenId) external view returns (bool)

Implemented in [Add EIP-5192 - Minimal Soulbound NFTs by TimDaub · Pull Request #5192 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5192/commits/f6b0b5740678249cdd9a0fb73fa834f76e1d86a2) thanks for making this suggestion.

---

**aram** (2022-07-26):

Sounds great [@TimDaub](/u/timdaub), sorry that I didn’t make the PR earlier, pretty was busy with project work ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**TimDaub** (2022-08-01):

EIP-5192: Minimal Soulbound NFTs was accepted today and is now available at [https://eips.ethereum.org/EIPS/eip-5192](https://t.co/5wDax3K8Fh)

---

**TimDaub** (2022-08-28):

Attempting to move to “Last Call”: [Move to Last Call by TimDaub · Pull Request #5549 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5549)

---

**TimDaub** (2022-08-29):

last call is active until 2022-09-12: [EIP-5192: Minimal Soulbound NFTs](https://eips.ethereum.org/EIPS/eip-5192)

---

**TimDaub** (2022-09-19):

EIP5192 is now final.

---

**TimDaub** (2022-09-29):

Just to understand the compactness of using EIP-5192 in NTTs that revert on throw. With just a few lines of code, a lot can be done that can help indexers to identify Soulbound tokens.

What follows is a proposed change set for an NTT contract throwing on all transferring functions that EIP-5192 was proposed to added. It’s a total of 6 additions: [Add first cut ERC5192 interface by TimDaub · Pull Request #6 · public-assembly/curation-protocol · GitHub](https://github.com/public-assembly/curation-protocol/pull/6/files)

---

**alex-ppg** (2022-10-15):

Hey [@TimDaub](/u/timdaub), quick question on the EIP that seems to be a bit unclear even tho it has been set as “Final”. With regards to `_mint` operations, it is clear that the `Locked` event should be emitted. What about `_burn` operations? Should they emit the `Unlocked` event since the NFT is no longer bound? Thanks for clarifying in advance, I believe this information should be included in the EIP itself as well.

---

**TimDaub** (2022-10-15):

Thanks for your feedback. I agree that we missed defining lock and unlock for burn. But as burning is transferring to address(0) the token must be unlocked before a burn. But then what should happen after calling burn is out of scope as my opinion is that the token stops existing. Does that help?

---

**CHANCE** (2022-10-27):

While this has been marked as Final, it is pretty odd to have a `Locked` and `Unlocked` event. It is unfortunate that this EIP did not receive the proper review and consideration before being approved.

Typically, one would expect a single `Lock` function with data representing the state.

Different events for the two are not emitted when minting and burning tokens. Simply, the data within those events are updated.

```auto
    /// @dev This emits when ownership of any NFT changes by any mechanism.
    ///  This event emits when NFTs are created (`from` == 0) and destroyed
    ///  (`to` == 0). Exception: during contract creation, any number of NFTs
    ///  may be created and assigned without emitting Transfer. At the time of
    ///  any transfer, the approved address for that NFT (if any) is reset to none.
    event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);
```

Now, to emit an event, devs have two options, and users have one:

Developers:

- Use an if statement that wastes gas
- Bifurcate function logic to work around EIP definition

Users:

- Pay more in gas

The expected state of only having 1 event is echoed in [EIP-5633: Composable Soulbound NFT, EIP-1155 Extension](https://eips.ethereum.org/EIPS/eip-5633).

Is there a reason as to why having two events is preferred?

---

**TimDaub** (2022-10-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chance/48/7577_2.png) CHANCE:

> While this has been marked as Final, it is pretty odd to have a Locked and Unlocked event. It is unfortunate that this EIP did not receive the proper review and consideration before being approved.
>
>
> Typically, one would expect a single Lock function with data representing the state.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chance/48/7577_2.png) CHANCE:

> Is there a reason as to why having two events is preferred?

You might enjoy the discussion in this comment: [EIP-5192: add event LockingStatusChanged(uint256 tokenId, bool status) by 0xanders · Pull Request #5459 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5459#discussion_r946613999) We had considered using a single event and opted for two for better readability. So this was reviewed.

But yeah, gas efficiency wasn’t considered, as it’s an implementation detail and not part of the interface.

---

**CHANCE** (2022-10-27):

That is unfortunate, but I appreciate the link share! This choice will severely limit adoption and make it impossible to recommend.

It is less about actual financial cost as chains inevitably get cheaper daily. Still, this EIP requires spaghetti code in a sea of EIPs that swim vigorously in the opposite direction.

Especially since even if someone wants to emit both events from the same function, there must be a check to determine what event to emit and if they can emit that event unless individuals are allowed to multi-emit the same duplicate event multiple times.

While “just an interface” it has extremely broad implementation impacts that ***should have been considered***.

Thanks for your time.

---

**TimDaub** (2022-11-01):

(I wrote this post in preparation for PeepAnEIP - have fun reading.)

# The history of EIP-5192 - Minimal Soulbound tokens

This is the story of how EIP-5192 Minimal Soulbound tokens got started and how we reached a status final on the interface definition. It’s not a very long story, actually, but what’s remarkable is that it starts at 2 am in the morning with me sitting on the computer hammering words into the keys.

EIP-5192 is a product of quickly having to sketch out an idea as a document as a means to make my sleep more peaceful and not full of thoughts about Solidity interfaces.

[![Screenshot 2022-10-31 at 15.17.57](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a632ab933f14875ce695642cb7e41d310eae5460_2_558x500.png)Screenshot 2022-10-31 at 15.17.571336×1196 85.5 KB](https://ethereum-magicians.org/uploads/default/a632ab933f14875ce695642cb7e41d310eae5460)

But the reason I’ve ended up in this situation is that long before EIP-5192, I had involved myself with specifying EIP-4973 “Account-bound tokens,” and so a frustration in not being able to find solutions to the community feedback I had received eventually evolved into this document for composable “Minimal Soulbound tokens.”

## The Timeline

[![Screenshot 2022-10-31 at 15.14.21](https://ethereum-magicians.org/uploads/default/optimized/2X/3/3968d77eb7e0c8c5f98117bb886303d7a4552b06_2_690x495.jpeg)Screenshot 2022-10-31 at 15.14.211920×1380 136 KB](https://ethereum-magicians.org/uploads/default/3968d77eb7e0c8c5f98117bb886303d7a4552b06)

Early in the year, in January, Vitalik posted their blog post titled “Soulbound,” and so when I visited ETHDenver to flee the German COVID-winter, I enjoyed the conversations there on Harberger taxes and what Kevin Owocki and others called non-skeuomorphic property. So even after returning, I dwelled on these thoughts, and by April fool’s day, I submitted a solution for EIP issue “1238” (Non-transferrable tokens) that would end up being called EIP-4973 “Account-bound tokens.”

A month later, Weyl et al. then released the Decentralized Society, and while I had been working with clients - I’m a freelancer  - on implementing EIP-4973 as badges, this brought more attention to our previous work than we could have imagined or managed to deal with.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/d/dfcfa90db2666cc77a86fb0b6d80424858f373ec_2_690x405.jpeg)image1517×891 62.3 KB](https://ethereum-magicians.org/uploads/default/dfcfa90db2666cc77a86fb0b6d80424858f373ec)

So to address the profound stream of user feedback we were getting for most of “Soulbound summer,” we huddled to produce meaningful and explanatory content on EIP-4973 regarding soul-binding, account-binding, and generally how to deal with that on a cultural, operational security, and technical level.

Quite a few times, I felt like withdrawing as the requirements seemed complex and overwhelming. And during one of those frustrating days, when I was about to go to bed, I had this idea about a minimal non-transferrable token specification for SBTs: Not even to aid EIP-4973 “Account-bound tokens” but rather to hedge my risk - as quantum thought and to cement these potentially divergent missions. So on August 1, 2022, I published EIP-5192 “Minimal Soulbound tokens” on GitHub.

## The Motivation

[![Screenshot 2022-10-31 at 15.14.08](https://ethereum-magicians.org/uploads/default/optimized/2X/f/f87cc533fd3823bedce71af40e3ad1e92ea46fd1_2_690x494.jpeg)Screenshot 2022-10-31 at 15.14.081920×1376 173 KB](https://ethereum-magicians.org/uploads/default/f87cc533fd3823bedce71af40e3ad1e92ea46fd1)

What had become particularly frustrating with the DeSoc publication had been that although we had directly associated ourselves with the term “Soulbound tokens,” our EIP-4973 hadn’t been mentioned by Weyl et al.'s mega-popular paper. And so suddenly, left and right, I saw ourselves being confronted with Medium articles on how to “EASILY IMPLEMENT SOULBOUND TOKENS” and their content being this one message: “Use EIP-721 and just revert on all transfer functions.”

```auto
contract NFT {
//...
  function transferFrom(
    address _from,
    address _to,
    uint256 _tokenId) external payable {
    revert("SOULBOUND");
  }
}
```

And having worked on Account-bound tokens for four months already, I found it incredibly frustrating that the most basic composability ideas were missing from those medium tutorials. So I felt compelled to use my newly found EIP-editing skills to improve the situation, and that one night, I had the deciding idea.

It would just be a particular “Soulbound token” EIP-165 identifier that `supportsInterface(bytes4 interfaceID)` would yield `true’ upon. And so here’s what that [first iteration](https://github.com/TimDaub/EIPs/blob/c0684fdf8ddb714a23c0992602194113a22cc95f/EIPS/eip-5555.md) looked like (I had called the standard EIP-5555 as a placeholder name):

[![Screenshot 2022-10-31 at 15.08.21](https://ethereum-magicians.org/uploads/default/optimized/2X/6/6242cc1c67511b8261347d08da238cb7e6271111_2_690x357.png)Screenshot 2022-10-31 at 15.08.211434×742 119 KB](https://ethereum-magicians.org/uploads/default/6242cc1c67511b8261347d08da238cb7e6271111)

So essentially, EIP-5192 was an EIP-165 identifier value where, e.g., EIP-721 contracts were supposed to yield `true` upon calling `supportsInterface(bytes4 interfaceID)`. And that’s all. We didn’t specify events, and generally, when that EIP was to be implemented, a token would be permanently bound to an account.

## The Problem

But as I’ve already mentioned in my ERC lightning talk at devcon in Bogota, the above wouldn’t be truly an EIP if it wasn’t heavily factoring in feedback from the community. And one such item of feedback we had been getting excessively but reasonably already in EIP-4973 was that binding tokens to accounts is considered an anti-pattern. This is because users want to reserve the freedom of key rotating their private keys, and since account abstraction isn’t ready for prime time yet: So the concern for account-binding is really that, although it’s potentially possible to account-bind only to contracts that enable key rotation, practically users and developers will bind to EOAs, and hence the standard must consider this in the design.

[![Screenshot 2022-10-31 at 15.30.01](https://ethereum-magicians.org/uploads/default/optimized/2X/0/0f211f0a670411bfe331d4fc3be4bcdc595dfd54_2_690x241.png)Screenshot 2022-10-31 at 15.30.011554×544 70 KB](https://ethereum-magicians.org/uploads/default/0f211f0a670411bfe331d4fc3be4bcdc595dfd54)

Confidently, I can herein say that this is a real problem that needs to be addressed in the Soulbound token specifications - and there are no safe escape paths from that line of reasoning for now. I ended up accepting that, and so when being confronted with the same “account-binding” rationale in EIP-5192 as in EIP-4973, I accepted its importance and gladly ended up realizing that an opinionated approach towards standardizing this concept of Soulbound tokens is anyways a better one. Here’s how we solved that problem.

## The Compromise

So eventually, [@aram](/u/aram) fixed the specification by introducing the `function locked` for a `uint256 tokenId` and that it returns a `boolean` conditionally.

[![Screenshot 2022-10-31 at 15.29.37](https://ethereum-magicians.org/uploads/default/optimized/2X/2/255a659a2f420f03c195dad133634ce3367c1eb4_2_690x400.png)Screenshot 2022-10-31 at 15.29.371532×890 147 KB](https://ethereum-magicians.org/uploads/default/255a659a2f420f03c195dad133634ce3367c1eb4)

And actually, while I have been fairly skeptical at first about this change - now it has been growing on me tremendously. Because I accept that standard documents cannot enforce implementation details anyways - and with that, we also have to acknowledge that, fundamentally, account-binding, soul-binding, or whatever you may wanna call it is a property of implementation and not part of the standard interface.

But before I continue on this line of reasoning, I wanna reveal now the finalized version of EIP-5192 below for anyone to see:

[![Screenshot 2022-10-31 at 15.34.36](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c98bb5bd4423ca5342f7e21a46f0e19dc88ab4a9_2_493x500.png)Screenshot 2022-10-31 at 15.34.361416×1434 359 KB](https://ethereum-magicians.org/uploads/default/c98bb5bd4423ca5342f7e21a46f0e19dc88ab4a9)

An overview:

- Any soul-bindable EIP-721 token is now recognizable by a machine/marketplace/wallet using the EIP-165 interface function.
- It is subject to the implementor whether an EIP-5192 token shall be permanently bound to an account. But any other configuration is available through the unopinionated interface definition (e.g., even implementing a permanently transferrable EIP-721 token).
- Dynamic locking use cases, e.g., the one outlined in DeSoc with community recovery, are implementable using the events and the locked view function.

## The Implementation

And so that’s how EIP-5192 got standardized, and just for you, the reader, to understand why I put such great focus on the document’s provenance: It’s because I think it’s important to highlight its history to explain the design decision we took towards finalization.

And then lastly, I also want to point out a first minimal implementation. Namely, a long-shot pull request I recently did for the public-assembly project. In fact, they had implemented a non-transferable token exactly in the way how medium tutorials had initially suggested - and so the entire fix was actually not that complicated. It consisted of adding the `function locked` but always returning `true` and by emitting an `event Locked(...)` when minting the NTT. And importing the interface. Here’s the entire change in a screenshot:

[![Screenshot 2022-10-31 at 15.43.46](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c6122e18cb03909a6222a10aaf18d46ddf8dc7b6_2_543x500.png)Screenshot 2022-10-31 at 15.43.461202×1106 155 KB](https://ethereum-magicians.org/uploads/default/c6122e18cb03909a6222a10aaf18d46ddf8dc7b6)

and the maintainer’s feedback:

[![Screenshot 2022-10-31 at 15.46.22](https://ethereum-magicians.org/uploads/default/optimized/2X/f/f4aa1a8ada3e44a46ad67f3242f3614dcda46d47_2_690x489.png)Screenshot 2022-10-31 at 15.46.221778×1262 303 KB](https://ethereum-magicians.org/uploads/default/f4aa1a8ada3e44a46ad67f3242f3614dcda46d47)

So I personally see this as a huge win, as it means we’ve gone from 0 to 1 on the specification and on the implementation. Now: It validates the NTT use case for now - and arguably, it doesn’t validate the Soulbound token use cases just yet. But I feel that we have a pretty general interface that allows implementing many token-locking use cases for wallets, marketplaces, and inventory management systems. So I’m excited for the future and where this specification might be headed then.

## The Conclusion

The conclusion is that I submitted a specification document on a whim and that the Ethereum Magicians community managed to turn it into something genuinely useful for an Ethereum community project. It’s important and useful to factor in external feedback and allows open participation. While this can be scary at times through losing oversights, it pays off over the long term by creating a more credibly neutral solution.

---

**poojaranjan** (2022-11-14):

Recording of [PEEPanEIP #89: EIP-5192: Minimal Soulbound NFTs](https://www.youtube.com/watch?v=unFTcUjQE3o) with [@TimDaub](/u/timdaub)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/9/9327c72467d1eaa667b6a103135b2e428603b298.jpeg)](https://www.youtube.com/watch?v=unFTcUjQE3o)


*(29 more replies not shown)*

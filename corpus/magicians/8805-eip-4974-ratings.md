---
source: magicians
topic_id: 8805
title: "EIP-4974: Ratings"
author: dtedesco1
date: "2022-04-02"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-4974-ratings/8805
views: 5899
likes: 37
posts_count: 37
---

# EIP-4974: Ratings

Traditionally, blockchain applications have focused on buying and selling digital assets. However, the asset-centric model has often been detrimental to community-based blockchain projects, as seen in the pay-to-play dynamics of many EVM-based games and DAOs in 2021.

EIP-4947 addresses this issue by allowing ratings to be assigned to contracts and wallets, providing a new composable primitive for blockchain applications.

This thread, begun in April 2022, has led to much evolution of the EIP. Please refer to the latest version  under review located here:  [ERC-4974: Ratings](https://eips.ethereum.org/EIPS/eip-4974)

## Replies

**fulldecent** (2022-04-02):

I do not see any need to standardize the use case of implementing ERC-20 (or ERC-1155 or ERC-777) with /less/ features than the full specification.

This exact kind of proposal has been put forth several times before relating to non-transferrable ERC-721 “badges”, all revoked or expired.

---

This should be encouraging news! It means you are cleared for takeoff and everything is ready for you to go ahead and implement.

---

**dtedesco1** (2022-04-03):

Edit:  Removing an outdated draft of the EIP, but leaving the references to external discussions here.

## References

**Issues & Discussions**

1. EIP-EXP discussion thread, Ethereum Magicians, begun April 2022.
2. “Soulbound”, Vitalik Buterin, published January 2022.
3. EIP-1238, “Non-transferrable Non-Fungible Tokens”, GitHub issue opened July 2018.
4. EIP-4671, “Non-Tradable Token Standard”, draft status as of April 2022.
5. EIP-4671 discussion thread, Ethereum Magicians, begun January 2022.

---

**dtedesco1** (2022-04-03):

Thanks for the feedback [@fulldecent](/u/fulldecent)! I’ve gone ahead with a full draft and implementation example.

Here’s the PR:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/4974)














####


      `master` ← `dtedesco1:master`




          opened 11:11AM - 05 Apr 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/3/3c950110a6fdbc6a42d66845e75b1b53b3239a57.png)
            dtedesco1](https://github.com/dtedesco1)



          [+477
            -0](https://github.com/ethereum/EIPs/pull/4974/files)







A need exists for fungible tokens that indicate reputation in a community, rathe[…](https://github.com/ethereum/EIPs/pull/4974)r than serve as tradable assets. Lack of such assets contributes to destructive pay-to-play dynamics in today's DAOs and blockchain games. Vitalik Buterin writes ["ad nauseum"](https://vitalik.ca/general/2022/01/26/soulbound.html) (his words) about this problem. EIP-4974 seeks solutions via a token standard similar to EXP in games or Reddit Karma.

Existing proposals and discussions for non-tradable token standards (namely, [EIP-4671](https://github.com/OmarAflak/EIPs/blob/7e3a3c68d4fb1a19d4d1e4838381ffcd9668e0ff/EIPS/eip-4671.md) and [EIP-1238](https://github.com/ethereum/EIPs/issues/1238)) have been reviewed deeply. Both are optimizing for credentials or badges, which are very different use cases from EXP.

For more background information, please view the [discussion on Ethereum Magicians here](https://ethereum-magicians.org/t/8805) and [initial PR](https://github.com/ethereum/EIPs/pull/4968).

---

**SamWilsn** (2022-04-07):

Why specify the `mint` function at all? Other token standards seem to leave it unspecified how tokens are created.

---

**dtedesco1** (2022-04-08):

# Summary

[@SamWilsn](/u/samwilsn) There’s a bit of discussion on this in [the PR](https://github.com/ethereum/EIPs/pull/4974). Essentially, we’re questioning how much new terminology needs to be introduced, particularly for token transfers and approval/participation. I’m on the fence about it.

- @wschwab suggested using burn and moving away from approve.
- @zhongeric and I then went a few extra steps to describe mint and burn, as they are more intuitive.
- I created reallocate and participate.
- The Transfer event is still aligned with other tokens.

(See below for side-by-side comparisons.)

# Transfer

The first iteration implemented `transfer` for minting and `transferFrom` for reallocating and burning. I was trying to align with ERC-20 and ERC-721. Here’s the previous definition:

```auto
`
    /// @notice Transfers EXP from zero address to a participant.
    /// @dev MUST throw unless msg.sender is operator.
    ///  MUST throw unless _to address is participating.
    function transfer(address _to, uint256 _amount) external;

    /// @notice Reallocates EXP from one address to another, or burns to zero address.
    /// @dev MUST throw unless msg.sender is operator.
    ///  MUST throw unless _to address is participating.
    ///  MAY throw if _from address is NOT participating.
    function transferFrom(address _from, address _to, uint256 _amount) external;
```

And the mint, burn, allocate iteration:

```auto
`
    /// @notice Mints EXP from zero address to a participant.
    /// @dev MUST throw unless `msg.sender` is `operator`.
    ///  MUST throw unless `to` address is participating.
    ///  MUST emit a `Transfer` event.
    /// @param _to Address to receive the new tokens.
    /// @param _amount Total EXP tokens to create.
    function mint(address _to, uint256 _amount) external;

    /// @notice Burns EXP from participant to the zero address.
    /// @dev MUST throw unless `msg.sender` is `operator`.
    ///  MUST emit a `Transfer` event.
    ///  MAY throw if `from` address is NOT participating.
    /// @param _from Address from which to destroy EXP tokens.
    /// @param _amount Total EXP tokens to destroy.
    function burn(address _from, uint256 _amount) external;

    /// @notice Transfer EXP from one address to another.
    /// @dev MUST throw unless `msg.sender` is `operator`.
    ///  MUST throw unless `to` address is participating.
    ///  MUST throw if either or both of `to` and `from` are the zero address.
    ///  MAY throw if `from` address is NOT participating.
    /// @param _from Address from which to reallocate EXP tokens.
    /// @param _to Address to which EXP tokens at `from` address will transfer.
    /// @param _amount Total EXP tokens to reallocate.
    function reallocate(address _from, address _to, uint256 _amount) external;
```

# Participation

This is a similar issue to using the language of “approval” versus “participation”, here’s a definition that would be aligned with ERC-721:

```auto
    /// @dev This emits when operator is enabled or disabled for a participant.
    ///  The operator can manage all EXP of the participant.
    event ApprovalForAll(address indexed _participant, address indexed _operator, bool _approved);

    /// @notice Activate or deactivate participation.
    /// @dev MUST throw unless msg.sender is _participant.
    ///  MUST throw if _participant is _operator or zero address.
    ///  MUST emit a `Participation` event.
    /// @param _participant Address opting in or out of participation.
    /// @param _participation Approval status of _participant.
    function approveForAll(address _participant, bool _approved) external;
```

And the “participation” iteration:

```auto
    /// Emits when an address activates or deactivates its participation.
    /// @dev MUST emit whenever participation status changes.
    ///  `Transfer` events SHOULD NOT reset participation.
    event Participation(address indexed _participant, bool _participation);

    /// @notice Activate or deactivate participation.
    /// @dev MUST throw unless `msg.sender` is `participant`.
    ///  MUST throw if `participant` is `operator` or zero address.
    ///  MUST emit a `Participation` event.
    /// @param _participant Address opting in or out of participation.
    /// @param _participation Participation status of _participant.
    function setParticipation(address _participant, bool _participation) external;
```

# My Perspective

There are several reasons to be for or against this new terminology:

- Good – More intuitive for EXP use cases, and perhaps more intuitive generally.
- Bad – Less aligned with existing token standards.
- Bad – Introduces new names.

My gut says EXP use cases are *not* sufficiently different to require new naming conventions, but I’m open to being convinced and will somewhat accede to folks who have a longer history with the ETH ecosystem.

---

**dtedesco1** (2022-04-08):

My previous message focuses on naming more than functionality. Are you suggesting that the standard should not assume an operator can mint tokens?

This is a reasonable consideration. For instance, an implementation might allow EXP only to be transferred from other EXP contracts. The argument can extend to a `burn` function as well.

Maybe `transfer` is all that’s needed in a standard–what’s critical is that *only* the operator can use such a function.

---

**SamWilsn** (2022-04-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dtedesco1/48/5773_2.png) dtedesco1:

> Are you suggesting that the standard should not assume an operator can mint tokens?

This exactly! `mint` and `burn` are probably going to be fairly unique per implementation of this standard. I think you can likely get by with the transfer events, and a balance getter. Do keep in mind that I’ve only taken a cursory view of the standard, and I might entirely be wrong!

---

**zhongeric** (2022-04-08):

Keeping only a privileged `transfer` function would definitely make this standard more general-purpose, creating an “issuer-only” controllable ERC721 standard.

Then the EXP nomenclature can be dropped from this standard, just leaving it as “Non-tradable NFTs”, as this can easily be adopted to serve other use cases besides EXP: POAPs, loyalty / community cards, etc…

---

**dtedesco1** (2022-04-09):

Agreed that keeping the privileged `transfer` function is a good option.

Non-tradable NFTs are a great concept, but I think it’s important to retain fungibility in this standard. Unique metadata for each token would actually inhibit EXP-like use cases.

Proposals I know of for *non-fungible* and *non-tradable* token standards:  [EIP-4671](https://github.com/OmarAflak/EIPs/blob/7e3a3c68d4fb1a19d4d1e4838381ffcd9668e0ff/EIPS/eip-4671.md) and [EIP-1238](https://github.com/ethereum/EIPs/issues/1238). Both are optimizing for credentials or badges, which are very different use cases from EXP.

---

**dtedesco1** (2022-04-09):

After further discussion Magicians and others, I’ve come to several conclusions about the participation and transfer nomenclature and functionality. I propose the following solutions to these issues for EIP-4974.

# Participation instead of Approval

In common parlance across the blockchain ecosystem today, approval tends to refer to approval for trading. EXP tokens are non-tradable. Further, three particular differences from existing standards justify the need for a new concept:

1. Airdrops do not require approval in many standards today. EIP-4974 requires address to opt-in before receiving tokens.
2. In standards such as ERC-721, it is required that setApprovalForAll “MUST allow multiple operators per owner.” EIP-4974 requires that only one operating address has control over a contracts token at any time.
3. Many standards require complicated acceptance mechanisms to ensure the propriety of trades. As EIP-4974 does not allow trading, setting a single participation is sufficient.

In this case, we can use the following function to control how non-operating wallets engage with EXP contracts.

```auto
`
/// @notice Activate or deactivate participation. CALLER IS RESPONSIBLE TO
///  UNDERSTAND THE TERMS OF THEIR PARTICIPATION.
/// @dev MUST throw unless `msg.sender` is `participant`.
///  MUST throw if `participant` is `operator` or zero address.
///  MUST emit a `Participation` event for status changes.
/// @param _participant Address opting in or out of participation.
/// @param _participation Participation status of _participant.
function setParticipation(address _participant, bool _participation) external;
```

# One transfer function instead of many component ones

We should not assume how mints or burns occur, or even if they occur. Those decisions are not core to the functionality of the standard, and may be unique across implementations. What makes EIP-4974 unique in terms of transfers is that only the operator can conduct transfers. Secondly, using only a `transfer` function also allows for clean alignment with other standards’ `transfer` functions, such as those of ERC-20 and ERC-721.

```auto
`
/// @notice Transfer EXP from one address to a participating address.
/// @dev MUST throw unless `msg.sender` is `operator`.
///  MUST throw unless `to` address is participating.
///  MUST throw if `to` and `from` are the same address.
///  MUST emit a Transfer event with each successful call.
///  SHOULD throw if `amount` is zero.
///  MAY allow minting from zero address, burning to the zero address,
///  transferring between accounts, and transferring between contracts.
///  MAY limit interaction with non-participating `from` addresses.
/// @param _from Address from which to transfer EXP tokens.
/// @param _to Address to which EXP tokens at `from` address will transfer.
/// @param _amount Total EXP tokens to reallocate.
function transfer(address _from, address _to, uint256 _amount) external;
```

---

**zhongeric** (2022-04-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dtedesco1/48/5773_2.png) dtedesco1:

> Proposals I know of for non-fungible and non-tradable token standards: EIP-4671 and EIP-1238. Both are optimizing for credentials or badges, which are very different use cases from EXP.

Got it, I missed the fact that this would be for fungible tokens. Are there other use cases for fungible non-tradable tokens besides EXP? Still iffy on whether or not EXP should be explicitly defined in the EIP name.

New `_transfer` function looks great though!

---

**dadabit** (2022-04-09):

I agree with [@fulldecent](/u/fulldecent) , a token that cannot be transferred is not a token imho. The function transfer is the very essence of tokens. I’d rather define a kudos interface completely unrelated to erc20 or tokens.

---

**carlosdp** (2022-04-09):

Read through this spec, as I’m thinking about this kind of token too! I think after reading the spec and all the comments and revisions, I agree with [@fulldecent](/u/fulldecent) 's original take on this, though. I think a restricted ERC-20 is probably the best way to go about this.

My main reasoning is it seems at this point that the only thing that is really added to the diff between this and ERC-20 (other than `mint` and `burn`, which I agree with an earlier commenter that it doesn’t make sense to put that into the spec. Reason being its very likely specific EXP implementations would need different function arguments for those functions, for things like signatures. This is why it’s not in any of the ERC-20 specs or extensions) is the concept of “Participation.”

While I think the intention is good, I don’t think it will achieve what you intend. Assuming the intention is that people won’t randomly be assigned some of these “points” without their consent, it’s easy to follow this spec while still violating this property.

For example, someone could write an implementation that emits the Participation event with `true` when a mint function is first called for the user, regardless of whether they actually participated. This kind of thing is ultimately always going to be up to the specific implementations of a token, and it’s going to be up to the clients displaying info to end users to counter abuse (as it already is today with token filters and such).

If someone wants to create this opt-in participation in being able to transfer ERC-20s, that’s fine. But the design surface area for the variety of ways to do that is so large, I’m not sure it makes sense to standardize that.

---

**dtedesco1** (2022-04-10):

Thanks!

Beyond actual game experience point implementations, we’ve thought of a few potential ones:

- Reddit-like Karma
- DAO delegation of authority levels
- Loyalty points from a business
- Ratings for contenders in sports or other competitive leagues.
- Credit scores (Ugh that feels dystopian, but at least it’d be more transparent and trustworthy than current credit scoring systems around the world…)
- Kudos given for contributions of some sort, i.e. for volunteer hours at a nonprofit

[@dadabit](/u/dadabit) also brought up the EXP name question recently. I think experience points is a more vivid description than the others considered, but I’m open to changing it. Happy to discuss dropping “token” language altogether, but at this point I think that’s a bit extreme. *The Kudos Standard*? Or more verbose, *The Experience Points Standard*? [More synonyms for “kudos”](https://www.wordhippo.com/what-is/another-word-for/kudos.html).

From the latest rationale section of the EIP:

> ### EXP Word Choice
>
>
>
> EXP, or experience points, are common parlance in the video game industry and generally known among modern internet users. Allocated EXP typically confers to strength and accumulates as one progresses in a game. This serves as a fair analogy to what we aim to achieve with ERC-4974 by encouraging members of a community to have more strength in that community the more they contribute.
>
>
> Alternatives Considered:  Soulbound Tokens, Soulbounds, Fungible Soulbound Tokens, Non-tradable Fungible Tokens, Non-transferrable Fungible Tokens, Karma Points, Reputation Tokens

---

**dtedesco1** (2022-04-10):

Thanks for this feedback. I’m also agreed that `mint` and `burn` are not sensible here. You brought up two other major topics:

# EIP-4974 versus existing token standards

Participation is definitely critical, but from my understanding there are two core, unique components of the 4974:

1. Only the operator can transfer EXP. Other accounts have no ability to obtain or dispose of EXP.
2. An account must set themselves as participating before any tokens can be received.

Implementing ERC-20 or ERC-721 to allow for these two components is simply *not* implementing ERC-20 or ERC-721. I think that’s the crux of [@fulldecent](/u/fulldecent) 's post above, but please correct me if I’m wrong.

# Potential loopholes

We can’t control if someone writes a smart contract claiming to follow a standard while quietly not following the standard, but you’re right we should be clear in the spec about what clients should expect and test for.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/carlosdp/48/5831_2.png) carlosdp:

> someone could write an implementation that emits the Participation event with true when a mint function is first called for the user, regardless of whether they actually participated

Thanks for pointing this out. Simply emitting a `Participation` event in this way shouldn’t have any impact on the operator’s ability to transfer to an address, but it would certainly be confusing. I’ll add a clause to make this explicit for each of the events, like so for `Participation`:

> /// This event MUST ONLY be emitted by setParticipation.

I’m keen to examine more examples like this. Do you see any other logical holes for implementers to abuse the spec?

---

**carlosdp** (2022-04-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dtedesco1/48/5773_2.png) dtedesco1:

> Participation is definitely critical, but from my understanding there are two core, unique components of the 4974:
>
>
> Only the operator can transfer EXP. Other accounts have no ability to obtain or dispose of EXP.
> An account must set themselves as participating before any tokens can be received.

Right, but like I explained in my post, you can’t really enforce that with a specification. I think this is more appropriate as a token protocol (ie. tokens created from a base contract that can actually enforce these rules) than an EIP, in my opinion. Then, it’s easy for clients and smart contracts to trust the child tokens, because it can be easily verified that `Participation` is enforced at the code level!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dtedesco1/48/5773_2.png) dtedesco1:

> Implementing ERC-20 or ERC-721 to allow for these two components is simply not implementing ERC-20 or ERC-721. I think that’s the crux of @fulldecent 's post above, but please correct me if I’m wrong.

I think you misunderstood what he is saying, actually. He’s saying that what you describe fits as a subset of the ERC-20 standard, so you can just go ahead and implement it without needing a new spec.

Neither of those two points goes against the ERC-20 spec. The ERC-20 spec does not specify how tokens can be minted or burned. And as for restricted transfers, everyone considers USDC an ERC-20, and that has a blacklist for interactions. This is no different! I’d say go with [@fulldecent](/u/fulldecent) 's recommendation and just go for it, no need for an EIP!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dtedesco1/48/5773_2.png) dtedesco1:

> I’m keen to examine more examples like this. Do you see any other logical holes for implementers to abuse the spec?

Well what I’m saying is, abusers don’t tend to follow the rules ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12). My point is, you can specify all the rules you want, the nature of smart contracts being self-sovereign and EIPs simply being agreed-on guidelines means they aren’t really too useful for preventing abuse. If someone creates a token meant to harm people, clients with filters tend to hide them pretty quick, regardless of what EIPs they follow. I’m not sure this adds enough to warrant an EIP, for that reason.

---

**dtedesco1** (2022-04-13):

Thanks for these comments [@carlosdp](/u/carlosdp), and I really appreciate the discussion you and  [@TimDaub](/u/timdaub) had in the thread on [EIP-4973](https://ethereum-magicians.org/t/eip-4973-non-transferrable-non-fungible-tokens-soulbound-tokens-or-badges/8825).

On [@fulldecent](/u/fulldecent)’s weekly community service hour livestream, I asked about EIPs. We didn’t discuss his comment above specifically, but I’m now convinced that your interpretation is right and mine was wrong. I was probably swept up in confirmation bias and excitement about my new idea.

I don’t want to create a standard that’s meaningless and no one will use. I’m genuinely unclear about what’s useful, though.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png)[EIP-4973 - Account-bound Tokens](https://ethereum-magicians.org/t/eip-4973-account-bound-tokens/8825/7)

> there’s a relevant difference between implementing a useful feature-detection mechanism (ERC4973) and naively disabling transfer functionality (revert in ERC721 transfer).

Where’s the line? How reductionist should we be?

At one extreme, we can argue every EIP should rather just be an optional extension to some other, more fundamental one. At the other extreme, I can envision every fly-by-night pet project getting its own ERC.

Maybe this deserves another thread. I’m confused.

---

**fulldecent** (2022-04-13):

Here is my overall guiding principle:

> First build something. Then standardize it. And the “something” should include some producer and some consumer of information.

And a second one:

> The purpose of standardizing something is to invite more people to play in your sandbox. The best way to get more people in your sandbox is to already have some friends in the sandbox.

ERC-721 is an example of something that was build–including multiple producers and consumers–before standardizing. The producer is the NFT contract, like some token that represents artwork or identity on-chain. The consumer is something that wants to query that information like Etherscan or MetaMask. Only by considering the needs of people on BOTH sides of that producer/consumer fence were we able to make the biggest impact. The end result is Etherscan fully supports ERC-721 and MetaMask finally started (barely) supporting most of it four years later and after every newspaper on earth was talking about this technical standard on its front page [citation needed] at some point. You might say MetaMask was brought along kicking and screaming.

Compare that to my recent experience in Estonia last week at NFT Tallinn. There were at least 5 companies focused on creating an NFT/fungible token for tracking carbon credits. (This is typical for an NFT event.) Few, if any, people are actually using their products. Standardizing any of that now would be a disaster. Four years from now barely anybody will have been attracted to connect onto their sandbox. And when they start connecting, they will learn some important thing they wish they know at the time of standardization. And the result will be… fragmentation with a new standard. That is the worst-case outcome for a standard.

---

**SamWilsn** (2022-04-21):

Just as a tiny note, the standard could simply state exactly what happens if you call the disabled `ERC-20` functions, and add a new `ERC-165` interface for wallets to query to check if a token is an EXP.

Edit: hm, actually you’d probably want a whole new interface that defines ERC-20 compatible functions, but not advertise ERC-165 support for the ERC-20 interface.

---

**EricForgy** (2022-04-24):

Hi [@dtedesco1](/u/dtedesco1),

I like the idea of a reputation token standard and have been thinking about it as well.

Here are some of my thoughts:

- Reputation tokens are hard to earn, but easy to burn.
- Reputation tokens cannot be transferred (period), but can be minted and staked.
- Reputation token supply is inflationary. Total supply of reputation tokens is constant increasing so that reputation loses value over time and must be continuously earned for an owner to maintain their share of reputation tokens.

There are lots of things to work out, but a real-world example has helped me think about this. I started life as a physicist, but switched to finance ages ago. My first job in asset management had an interesting flat culture. The management team rotated every year. My office was next to the founder’s grandson and was the same modest size. No corner offices. Also, everyone in the investment team bent over backwards to help me. It was great. The way it was explained to me, everyone was enthusiastic about helping me because the sooner I got up to speed, the sooner I could help them. Sounded great. But when my first annual review came around, I learned there was a more pragmatic reason why everyone was trying so hard to help me. I received an odd email saying that I had 10 points that I could allocate to colleagues with a maximum of 5 points to any one person and could allocate to at most 10 people (1 pt each). I didn’t have to allocate any if I didn’t want to. The basis for allocation? We were to allocate points to colleagues who we felt had helped us do our jobs better the previous year. Bonuses were largely influenced by how many points you received. I always thought that was a great was to incentivize a helpful culture. Now, it seems like a total no-brainer to tokenize this concept.

With this in mind, I am thinking that once someone has achieved a certain level of reputation, e.g. maybe owning 1 reputation token, they are periodically, e.g. once a month, allowed to mint (not transfer) a limited number of tokens to others who they feel have helped them or helped the project.

The natural use case for reputation tokens would be DAO governance as means to combat the current plutocracy of purchased governance tokens. Rather than buying votes, you earn votes via reputation and you vote on initiatives by staking your reputation on them. The amount you can stake is tracked similarly to how allowance is currently tracked in ERC-20.

Need to think about Sybil attacks. Maybe some kind of modified quadratic voting?

Edit: Btw, if there is a non-transferrable token standard, I think it should also contain a consent mechanism, e.g.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ericforgy/48/4692_2.png)
    [Standards for a consent token](https://ethereum-magicians.org/t/standards-for-a-consent-token/9027) [Tokens](/c/tokens/18)



> Hi everyone,
> I did a cursory search and didn’t find a discussion on this topic, but if I missed anything, references would be appreciated
> I was inspired by Evin’s ETHDenver talk:
>
>
>     [The Off Chain Internet: Decentralized Identity & Verifiable Credentials | ETHDenver 2022]
>
>
>
> I’ve been busy working on something else, but this has been running in the back of my head since ETHDenver.
> ERC-20, ERC-721 and ERC-1155 all contain some form of approval in order to allow the transfer of t…


*(16 more replies not shown)*

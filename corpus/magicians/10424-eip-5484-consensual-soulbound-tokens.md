---
source: magicians
topic_id: 10424
title: EIP-5484 - Consensual Soulbound Tokens
author: BuzzCai
date: "2022-08-18"
category: EIPs
tags: [nft, sbt]
url: https://ethereum-magicians.org/t/eip-5484-consensual-soulbound-tokens/10424
views: 6030
likes: 29
posts_count: 31
---

# EIP-5484 - Consensual Soulbound Tokens

- EIP5484 Proposal:  EIP-5484: Consensual Soulbound Tokens
- Descrpition: Interface for special NFTs with immutable ownership and pre-determined immutable burn authorization
- Stage: Review
- Related Proposals/Discussions:

EIP-4973 - Account-bound Tokens  | Discussion
- EIP-5114: Soulbound Badge | Discussion
- EIP-5192: Minimal Soulbound NFTs | Discussion

[@MicahZoltu](/u/micahzoltu) and [@TimDaub](/u/timdaub) have contributed greatly on the topic, it might get you a better understanding of the discussion if you take a look at the related proposals/discussions links.

Again, this proposal is in review stage. Comments and suggestions to improve the EIP are welcomed and appreciated.

## Replies

**TimDaub** (2022-08-18):

Hi, EIP-4973 author here. We’d be interested to include consensual revocation into the specification. We already have consensual “taking” and “giving” of tokens. Please let me know if this is interesting to you.

---

**BuzzCai** (2022-08-19):

Hi [@TimDaub](/u/timdaub), I am glad my EIP is inspiring other EIPs ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12) . Thanks for reaching out and yes this sounds interesting to me. Let me know what I can help on EIP-4973 or anything that helps our community to achieve a consensus on SBT-like token interface. If all you want is to include the mechanism, go ahead and do it ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) I am fine as long as proper credit is given.

---

**BuzzCai** (2022-08-25):

I am presenting my two cents here and hope people can join the conversation to help improve this draft:

- Similar to real-world credentials and identities, SBTs can’t be changed but can be burned. It is important to signify who has the rights to burn a specific token. For example, a club membership can be burned by both parties, a paid membership can only be burned by the receiver, and a loan record can only be burn by the issuer.
- Ideally SBTs’ content shall be immutable after issuance, this provides credibility and keep receivers’ identities safe from an unreliable issuer manipulating SBTs after issuance; however, it is difficult to enforce that in an interface, so the immutability requirement is kept only as a guideline rather than an enforcement.
- The idea of consensual follows naturally. If we are trying to build a SBT ecosystem that every token’s identity can be trusted, it is important that receivers give consent to the identity, burn agreement, and metadata proposed by the issuer. Otherwise bad actors can issue fake identities that can’t be burned by receivers, destroying the overall credibility of the system.
- The goal of this EIP is to provide a standard that makes lives easier when developing SBTs related services. Instead of an error message from calling transfer (this standard extends EIP-721 to be compatible with existing NFTs ecosystems), developers can now check the interface ID and avoid calling transfer on SBTs. They can quickly isolate SBTs issuing events from the unique emits, and there is a number code standard for different burn authorization.

---

**TimDaub** (2022-08-28):

I saw that you base your proposal on EIP-721. Maybe you’re interested in basing the proposal on [EIP-5192: Minimal Soulbound NFTs](https://eips.ethereum.org/EIPS/eip-5192), which introduces a minimal interface to signal that a token is currently non-transferrable.

---

**BuzzCai** (2022-08-29):

Hey [@TimDaub](/u/timdaub),

I actually considered basing the proposal on EIP-5192 when I was drafting it since EIP-5192 is very concise in what it’s doing. One concern I had was that EIP-5192, which’s still in review stage last time I checked, might change in the future.

Another thing to be noted is that EIP-5192 allows contract owners to lock and unlock the transferability of NFTs. In my vision of SBT, the token shall be untransferable throughout its lifetime. Though EIP-5192’s lock and unlock controls provide flexibility in some scenarios, they also undermine soulbound token’s credibility. In the long run, SBTs shall differ from NFTs in terms of how much trust users and verifiers can assume with confidence. If we take away the immutability of ownership, SBTs are just special NFTs that have certain transfer rules customized by deployers.

---

**TimDaub** (2022-08-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> I actually considered basing the proposal on EIP-5192 when I was drafting it since EIP-5192 is very concise in what it’s doing. One concern I had was that EIP-5192, which’s still in review stage last time I checked, might change in the future.

We just moved it into last call and hence it will be final in roughly 14 days: [ERC-5192: Minimal Soulbound NFTs](https://eips.ethereum.org/EIPS/eip-5192)

---

**DonMartin3z** (2022-09-03):

Hi my friend. I would like to share with you a concept that uses the SoulBound Tokens to actually have an interface in the web3 space  and also use them to build reputation in a new social concept. I’m building first the concepts on a white paper. Are you interested ?

---

**BuzzCai** (2022-09-03):

[@DonMartin3z](/u/donmartin3z) Sounds interesting, hit me up with more details ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**DonMartin3z** (2022-09-21):

Send me your email and take a time to check the whitepapet

---

**TimDaub** (2022-09-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> One concern I had was that EIP-5192, which’s still in review stage last time I checked, might change in the future.

it is final now since a few days

---

**BuzzCai** (2022-09-22):

[@TimDaub](/u/timdaub)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> Though EIP-5192’s lock and unlock controls provide flexibility in some scenarios, they also undermine soulbound token’s credibility. In the long run, SBTs shall differ from NFTs in terms of how much trust users and verifiers can assume with confidence. If we take away the immutability of ownership, SBTs are just special NFTs that have certain transfer rules customized by deployers.

Since you are quoting from the same reply, I am sure you also saw this portion of my concern. Again, immutability gives sbts its credibility. Allowing users to lock and unlock is just making a lockable nft with no credibility and trust behind it.

---

**TimDaub** (2022-09-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> In the long run, SBTs shall differ from NFTs in terms of how much trust users and verifiers can assume with confidence. If we take away the immutability of ownership, SBTs are just special NFTs that have certain transfer rules customized by deployers.

I understand your concern. If EIP-5192’s ownership was mutable I’d also think it’d undermine their credibility. The interface came together given the community’s feedback and their wish to not standardize around a purely immutable EIP. But we make sure it is in the EIP-5192 implementor’s discretion to permanently lock a token. It will comply with the standard.

---

**BuzzCai** (2022-09-23):

Hey Tim,

The community has different feedbacks based on different concerns. I have seen pro-flexibility and pro-immutability feedbacks in our community’s various discussions surrounding SBTs. IMO, both standings have valid points. Furthermore, EIP-5484’s proposal describes how to do key rotation based on consensual burning mechanics, so it has a good balance of immutability that users can assume trust on, while provides some flexibility that certain sbts can be unbound from an address. My overall goal is to setup a guideline for good issuers to follow, and protect receivers’ rights on the identities they are receiving from easy manipulation of issuers. Again, I am not saying only one approach is right. I think a flexible sbt and a trustworthy immutable sbt can go hand in hand. Developers can pick on which one they would like to use based on their application needs.

---

**BuzzCai** (2022-10-25):

Moved to Last Call

ddl: 2022-11-05

---

**exstalis** (2022-10-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> Though EIP-5192’s lock and unlock controls provide flexibility in some scenarios, they also undermine soulbound token’s credibility. In the long run, SBTs shall differ from NFTs in terms of how much trust users and verifiers can assume with confidence. If we take away the immutability of ownership, SBTs are just special NFTs that have certain transfer rules customized by deployers.

Hi, I’m really interested in your opinions. The confidence level between parties can assume is a great point we need to address. Do you have use cases in mind or would you like you to simulate a scenario on that? I also would like to connect with you on creating more fairness for token holders applying more sustainable ecosystems thru SBTs.

---

**BuzzCai** (2022-10-27):

Hey [@exstalis](/u/exstalis),

Recently I have been talking to ethSF teams who are interested in building sbt projects. I have heard some very interesting ideas applying sbts to gamefi, dao, and web2 scenarios. Soulbound definitely has a lot of potential solving problems that couldn’t be solved by NFTs, and many of us are experimenting with the potentials. If you have any interesting idea to share, I am happy to chat.

---

**TimDaub** (2022-10-27):

Frankly and respectfully, because the following is gonna sound harsh, your last message and your move forward show that you haven’t committed enough time to properly understand EIP-5192 and EIP-4973.

- EIP-5192 is a perfectly capable interface for expressing both permanently “soul”-bound tokens (in a code-immutable way) as much as it can express a permanently transferrable token (in a code-immutable way). E.g. public-assembly has shipped a permanently account-bound token with EIP-5192: Add first cut ERC5192 interface by TimDaub · Pull Request #6 · public-assembly/curation-protocol · GitHub, but entirely different flavors are possible!
- EIP-5484 is rushed into finalization (which happens in a few days on 2022-11-05) although being unclear and incomplete about, e.g., soul binding. Yes, you named it “… Soulbound token,” but while the specification acknowledges non-transferability and its issues, it does NOT specify clearly how binding needs to be implemented., E.g., this section:

> One problem with current soulbound token implementations that extend from EIP-721 is that all transfer implementations throw errors. A much cleaner approach would be for transfer functions to still throw, but also enable third parties to check beforehand if the contract implements the soulbound interface to avoid calling transfer.

I’m writing this with this intensity as it was pointed out to me that the specification is now already moving into finalization (of which I was surprised - I should have paid more attention) without meaningfully addressing the community’s feedback (e.g., mine).

I think that your burn and authorization logic around consent is actually really valuable, and they represent what, e.g., the authors of the DeSoc paper have described. I’m being so passionate about this all here because I think your work so far has been quite impactful and important! So my demand is asking you to roll back the status to “Review” and do the appropriate changes towards better consistency and completeness of your document. Please!

---

**BuzzCai** (2022-10-27):

Hey [@TimDaub](/u/timdaub),

With all due respect, the followings are gonna sound harsh too.

I noticed you had the tendency to call competing proposals “rushed into finalization”, and saw you’ve done it several times in the past. I was expecting you post something similar when I moved to last call, and here we are. So this is my response to that:

1. Your EIP-5192 Minimal Soulbound NFTs was created on June 30th, and moved to last call on Aug 29th, roughly 60 days. While this EIP-5484 was created on Aug 17th and moved to last call on Oct. 27th, roughly 70 days. Ten more days than your proposal.
2. I know the change you actually want me to make is again the change you personally demanded earlier, which is to base EIP-5484 on your EIP-5192. I have responded to that previously in this post, which received great community feedback and you never responded to.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> Hey Tim,
> The community has different feedbacks based on different concerns. I have seen pro-flexibility and pro-immutability feedbacks in our community’s various discussions surrounding SBTs. IMO, both standings have valid points. Furthermore, EIP-5484’s proposal describes how to do key rotation based on consensual burning mechanics, so it has a good balance of immutability that users can assume trust on, while provides some flexibility that certain sbts can be unbound from an address. My overall goal is to setup a guideline for good issuers to follow, and protect receivers’ rights on the identities they are receiving from easy manipulation of issuers. Again, I am not saying only one approach is right. I think a flexible sbt and a trustworthy immutable sbt can go hand in hand. Developers can pick on which one they would like to use based on their application needs.

1. It is interesting you brought up community feedback.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> without meaningfully addressing the community’s feedback (e.g., mine).

Here is a community feedback I am sure you saw and ignored.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> Another thing to be noted is that EIP-5192 allows contract owners to lock and unlock the transferability of NFTs. In my vision of SBT, the token shall be untransferable throughout its lifetime. Though EIP-5192’s lock and unlock controls provide flexibility in some scenarios, they also undermine soulbound token’s credibility. In the long run, SBTs shall differ from NFTs in terms of how much trust users and verifiers can assume with confidence. If we take away the immutability of ownership, SBTs are just special NFTs that have certain transfer rules customized by deployers.

This conversation happened during the final call of your proposal EIP-5192. I am wondering why you pushed your proposal all the way to final when you didn’t, as you phrased it, “meaningfully addressing the community’s feedback (e.g., mine).”

The only difference is that I didn’t come to your proposal asking you to revert your EIP-5192 status to review because I considered there is a conflict of interest between us competing proposal authors.

1. The list goes on, but really these are the important points I want to make for now. I know you knew this proposal isn’t rushed to finalization, and you knew I read EIP-4973 and EIP-5192 along with all their discussions multiple times as in the very beginning I posted the links to the relevant discussions and proposals for people to refer to.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> Related Proposals/Discussions:
>
> EIP-4973 - Account-bound Tokens  | Discussion
> EIP-5114: Soulbound Badge  | Discussion
> EIP-5192: Minimal Soulbound NFTs  | Discussion
>
>
>
>
> @MicahZoltu and @TimDaub have contributed greatly on the topic, it might get you a better understanding of the discussion if you take a look at the related proposals/discussions links.

I know that you are accusing this proposal being rushed and me being unfamiliar with the two proposal in order to undermine the credibility of this proposal to community members who haven’t been following along. Frankly I understand why you do what you did as a competing proposal author, but hey we are not writing these proposals for personal or business benefits, and I think as a very active member of the forum, you are better than that.

---

**TimDaub** (2022-10-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> Another thing to be noted is that EIP-5192 allows contract owners to lock and unlock the transferability of NFTs.

Contract owners e.g. EIP-173 owner() address CANNOT change the locking or unlocking.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> In my vision of SBT, the token shall be untransferable throughout its lifetime.

That is possible with EIP-5192 as demonstrated with the link I shared in the public assembly project. For your convenience: [Add first cut ERC5192 interface by TimDaub · Pull Request #6 · public-assembly/curation-protocol · GitHub](https://github.com/public-assembly/curation-protocol/pull/6/files#diff-10e948ca3b3385e74c7367fa8593d3ffae1fb487543256530e124fc899933754)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> Furthermore, EIP-5484’s proposal describes how to do key rotation based on consensual burning mechanics, so it has a good balance of immutability that users can assume trust on, while provides some flexibility that certain sbts can be unbound from an address.

That’s achievable with EIP-5192 but dependent on the respective implementation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> This conversation happened during the final call of your proposal EIP-5192. I am wondering why you pushed your proposal all the way to final when you didn’t, as you phrased it, “meaningfully addressing the community’s feedback (e.g., mine).”

This feedback isn’t addressible because it’s based on false premises. Contract owners cannot universally lock and unlock EIP-5192 tokens as this is specific to the implementation. EIP-5192 enables permanently locked, permanently transferrable and all other possibilities depending on an implementation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> I know that you are accusing this proposal being rushed and me being unfamiliar with the two proposal in order to undermine the credibility of this proposal to community members who haven’t been following along.

My intention for objecting EIP-5484 is that I think it would dovetail well with EIP-5192 but that you don’t seem to fully understand how it works therefore I’m asking you to try to understand it completely before marking urs as final.

---

**BuzzCai** (2022-10-27):

In your EIP-5192 thread, specifically the post that inspired you to include the locked function.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aram/48/5696_2.png)[FINAL EIP-5192 - Minimal Soulbound NFTs](https://ethereum-magicians.org/t/final-eip-5192-minimal-soulbound-nfts/9814/5)

> This will allow wallets to check for transferability for UX, allows implementers more freedom around mint/burn and maybe even allowing transfers in certain situations.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png)[FINAL EIP-5192 - Minimal Soulbound NFTs](https://ethereum-magicians.org/t/final-eip-5192-minimal-soulbound-nfts/9814/6)

> yeah, @aram I think this is a good idea as it’ll still allow someone to inseparably bind a token to an account, but leave that choice to the user (which IMO should ultimately have the freedom of decision).
>
>
> The effect is that it can shut up the nay-sayers arguing for better key rotation practices in SBTs as the interface is neutral towards the concept of permanent locking.

You specifically mentioned token transferability is possible, and this “shut up the nay-sayers arguing for better key rotation”. It doesn’t matter who has the rights to change token transferability, contract owner of token receiver, the fact that this is changeable makes my previous point:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buzzcai/48/6867_2.png) BuzzCai:

> Though EIP-5192’s lock and unlock controls provide flexibility in some scenarios, they also undermine soulbound token’s credibility. In the long run, SBTs shall differ from NFTs in terms of how much trust users and verifiers can assume with confidence.

Again, it’s not about what is “possible” or “achievable with EIP-5192”. What’s important is that the flexibility of EIP-5192 diminishes credibility of SBTs’ immutability.

If you want to argue that oh wait, I have changed my mind, and EIP-5192’s lock status CANNOT be changed by either parties after issuance. There are few things you have to do. First,

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> Contract owners e.g. EIP-173 owner() address CANNOT change the locking or unlocking.

This should be in your EIP’s specification section, not here in the comment section of a related proposal. Your proposal made it very vague and ambiguous on who has the rights to change/assign lock status. Previously I thought you leave it to the implementation to decide the specific rules, but if you want to argue that lock/unlock status is permanent after issuance (which is basically what you are arguing in the previous post), your current EIP-5192 definitely needs a lot of modification on clarifying the rules, and I recommend you roll it back to review status if you intend EIP-5192’s lock status to be permanent after issuance.


*(10 more replies not shown)*

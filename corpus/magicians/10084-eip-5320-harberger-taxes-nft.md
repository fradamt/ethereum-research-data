---
source: magicians
topic_id: 10084
title: "EIP-5320: Harberger Taxes NFT"
author: green
date: "2022-07-24"
category: EIPs
tags: [erc, nft, erc-721, erc-20]
url: https://ethereum-magicians.org/t/eip-5320-harberger-taxes-nft/10084
views: 4276
likes: 22
posts_count: 48
---

# EIP-5320: Harberger Taxes NFT

[GitHub PR](https://github.com/ethereum/EIPs/pull/5320)

## Replies

**TimDaub** (2022-07-24):

I’ve been trying to find useful interfaces around implementing Harberger Taxes for NFTs that have maximal backward compatibility with EIP-721. Some of my work:

- Incomplete Solidity implementation: GitHub - rugpullindex/libharberger: A dapptools/foundry-ready library for charging Harberger taxes on partial common non-fungible property.
- blog posts:

Harberger Taxes can be Crypto's Sustainable Business Model
- Non-Skeuomorphic Harberger Properties may not be implementable as ERC721 NFTs

My initial idea had been to use a Soulbound token bound to a smart contract as the base object that can then be harberger-taxed. For that, I had attempted to standardize two EIPs:

- EIP-4973: Account-bound Tokens (which has arguably diverged from this idea a lot)
- Add EIP-5192 - Minimal Soulbound NFTs by TimDaub · Pull Request #5192 · ethereum/EIPs · GitHub (which may neither be super useful)

Here are a few critical questions that you hopefully deem helpful for further developing the document:

- Why mix auction logic into the NFT ownership logic? Auction houses like Zora and OpenSea implement auction houses such that any EIP-721 can move through them for allocating new owners. In fact, it’d be elegant if we could standardize around auctioning scheme interfaces for EIP-721. It seems unnecessary to conflate Harberger tax auctioning and NFT logic in one contract, as you suggest using Solidity inheritance.
- Ownership is a preexisting topic defined outside of Ethereum or Solidity. Some say Ownership is the bucket of rights, permissions, and license opportunities that make a property ownable. E.g., there’s a difference between possessing and owning: As EIP-5320 introduces possession-based Harberger tax interest to users, what should function ownerOf(...) return? The collection’s address or that of the “NFT owner”? I’d argue an Harberger-taxed property isn’t truly owned by a user but by the taxing contract (which has the right to foreclose when taxes aren’t paid).
- When can transfer functions of EIP-721 be called? When do they throw? I assume there is a connection between paying taxes and being able to call those functions?
- As the variability and connection of tax rates to turnover rates seem to be fundamental (at least Radical Markets and Anthony Lee Zhang say so): What made you decide not to include them in the specification? E.g. a view function returning the current tax rate or a function to set a tax rate. Also: Do all items have the same tax rate? E.g. how would a Harberger tax possessor know what taxes are necessary to be paid at time t?

Regarding building a Harberger property contract, I’ve found this EIP very interesting: [EIP-4907: Rental NFT, ERC-721 User And Expires Extension](https://eips.ethereum.org/EIPS/eip-4907) It would allow building an auction house that treats the Harberger property possessor to be the user and the taxation authority to be the NFT owner.

---

**will-holley** (2022-07-25):

Several of us, including Tim, are working towards this HT token standards over at https://partialcommonownership.com/.  Our next community meeting is this Wednesday; it would be great for you to attend.

---

**MicahZoltu** (2022-07-31):

~~One could imagine a mechanism for depositing ETH into some contract and then having multiple NFTs pull from that. This would allow someone to put say 10 ETH into a contract that is used to pay taxes on a hundreds of NFTs until the pot ran out. The owner then wouldn’t need to constantly top up each individual property all of the time, but instead just top up their funding source account.~~

~~Even better would be to use approvals and disallow ETH (WETH can be used instead).  This way the owner can just approve the NFT to draw on their TOK as necessary, so as long as they have TOK in their account they can pay taxes as they are collected.~~

Already addressed in the rationale, good job!

---

**MicahZoltu** (2022-07-31):

> Instead of doing this, buy could have simply accepted the valuation of the item as the buy price. This, however, has frontrunning concerns, as the current owner can frontrun and increase the valuation.

It seems like this could be avoided by having a time delay on valuation changes.  When `changeValuation` is called, it wouldn’t take effect for `n` blocks, thus preventing the seller from frontrunning the purchase.  This does make the collect function a bit more complex, but I don’t think it would be too bad.

---

**guoliu** (2022-08-02):

Thank you for this proposal, we needed a standard like this a while ago, and will still need it for several future projects. We [implemented](https://github.com/thematters/contracts/blob/develop/src/TheSpace/ITheSpace.sol) Harberger Tax for our collaborative pixel canvas [TheSpace.Game](https://thespace.game/), and it has been played by several thousands of users.

Here are some of my thoughts regarding the proposal based on that experience.

**Offer or buy**

When there is competition, buying a token is not guaranteed since only the first one will acquire it. We implemented an offer logic (it’s called “bid” since it’s an auction): the bidder agrees to pay the current valuation as long as it is lower than the bid price. In this way, there is no racing condition and no front runs.

**Prepaid tax or tax allowance**

Prepaid tax is definitely a clearer logic. But with tax allowance, users need fewer ERC20 tokens to start playing the game, which turned out to be important in onboarding users for us. Tax allowance needs to be combined with a mint tax mechanism, so users are discouraged to repeat the following: “buy at a low price → increase price → default / burnt → mint again at a low price”.

Using tax allowance also means tax needs to be collected frequently. We opened up the tax collection function for anyone to call, and among the players emerged a role called “tax collectors”, who volunteer to collect tax and have become part of the game.

Also in our case, taxes and funds per token are not possible since the mental complexity it brings discourages users from playing the game. I believe the choice of tax collection method should be left to the implementation of the contract.

---

**mdnorman** (2022-08-03):

since there’s no “tax period”, it’s hard to know when taxes must be paid for someone who owns this token. I was working with CityDAO on this a proposal for using Harberger taxes on a parcel of land, and one of the things that folks need to know is when the collection period is. You don’t want to make it a single date because then folks will try to game the system, and you don’t want to make it “all year long” because you don’t know when it will actually be assessed.

I wrote up quite a bit of detail [here](https://docs.google.com/document/d/1ufqjUU1ZSrCUlOfHJudyhF4MVTimHcEU5L_swNvXCYk/edit#heading=h.6db975ulp1ep) if you want to take a look. It may inform this EIP in some ways to make tax collection more standardized.

---

**JasoonS** (2022-08-03):

Cool to see this topic come up again!

We implemented harberger tax contracts first at wildcards[dot]world (sorry - unable to share more than two links) where users could share deposits between their harberger NFTs, and the harberger tax of those NFTs could go to multiple different beneficiaries. (Hence it is “scalable” for users to own multiple NFTs that share a deposit and fund multiple beneficiaries). We re-used these contracts for a variety of hackathons and experiments over the years.

I gave a presentation on this a while ago which can be found here: https://youtu.be/LYm-cVuo0sg and here is the slideshow: [Harberger Tax Contract Overview.pdf](https://github.com/ethereum/EIPs/files/9244225/Harberger.Tax.Contract.Overview.pdf)

The contracts are on github at wildcards-world/contracts, which might be an interesting reference too.

Quick thoughts:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> Why mix auction logic into the NFT ownership logic?

At wildcards we always used a ‘Steward’ contract that acted as an NFT operator that managed the harberger tax side of things.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> When can transfer functions of EIP-721 be called? When do they throw? I assume there is a connection between paying taxes and being able to call those functions?

Lots of thought needed here. Lots of trickery can happen if users don’t understand this. Also might depend on the use case.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> a view function returning the current tax rate or a function to set a tax rate

Yes, this is essential IMO. In wildcards as a case study each NFT has a different rate.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> It would allow building an auction house that treats the Harberger property possessor to be the user and the taxation authority to be the NFT owner.

I think this makes sense, but if it is possible for the NFT to ever be withdrawn from the taxation authority, it kind of defeats the point (although there are likely lots of fun mechanisms that could use this).

There are so different variations you can make to harberger tax. For example, realitycards[dot]io have their own variation on harberger tax. So I think this EIP should aim to be high level enough to accommodate future variations and explorations.

---

**guoliu** (2022-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mdnorman/48/6722_2.png) mdnorman:

> since there’s no “tax period”, it’s hard to know when taxes must be paid for someone who owns this token.

It seems to me that the concept of “tax period” is not needed, since the calculation of tax obligation should be continuous (or in practice, with 1 block as the calculation period).  Whether using prepaid tax or tax allowance, tax collection can be triggered at any time, including but not limited to ownership and price change.

---

**will-holley** (2022-08-04):

This depends on whether you’re using a deposit or non-deposit model to pay the taxes[1].  In the case of a deposit, there will be a tax period, the foreclosure time of which is easily calculable (see example [here](https://github.com/721labs/partial-common-ownership/blob/3e7713bc60b6bb2e103320036ec5aeaaaceb7d2b/contracts/token/modules/Taxation.sol#L260)).

**Footnotes**

1. There is an inherent tradeoff between requiring the leasor to deposit funds and the risk that the leasor does not make a deposit, does not have the funds when collection is required, and the collector loses out on her tax revenue.  A depreciating license model may be an alternative to this problem.

---

**guoliu** (2022-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jasoons/48/6739_2.png) JasoonS:

> When can transfer functions of EIP-721 be called? When do they throw? I assume there is a connection between paying taxes and being able to call those functions?

I think a broader issue related is that “transfer” in the context of Harberger Tax should be different from that in ERC721. ERC721 is designed for private ownership, while Harberger Tax is designed for partial common ownership.

Ownership under Harberger Tax corresponds to tax obligation, so transferring token is also transferring tax obligation. This can be used as a form of attack, where the attacker set the price very high and then transfer it to the victim. (In the case where tax is prepaid/deposited and allocated for each token, it can be mitigated by clearing deposits of all tokens I do not own, but it can still cause unwanted consequences)

In our case, we automatically set the token price to 0 when a transfer is triggered. “Transfer” thus still follows the continuous auction logic of Harberger Tax, where the owner set the price to 0 then the receiver gets it for free.

---

**MicahZoltu** (2022-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/will-holley/48/5956_2.png) will-holley:

> A depreciating license model may be an alternative to this problem.

This is a clever solution, and I generally like it.  Can you draft up a simple example (Alice mints token, sells to Bob who values it at some price, then a year later Carol buys it)?  I’m particularly curious how valuation changes are handled.  When I go through the construction in my head, I end up with no change in capital efficiency, just a change in mechanics and who has to escrow the money (the minter vs the renter).

---

**MicahZoltu** (2022-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/guoliu/48/6734_2.png) guoliu:

> Ownership under Harberger Tax corresponds to tax obligation, so transferring token is also transferring tax obligation. This can be used as a form of attack, where the attacker set the price very high and then transfer it to the victim. (In the case where tax is prepaid/deposited and allocated for each token, it can be mitigated by clearing deposits of all tokens I do not own, but it can still cause unwanted consequences)

If the tax is pre-paid in escrow, transferring it wouldn’t do you any good because either there is a requirement for the asset to always remain funded, or the valuation would immediately go to 0 when the escrowed funds are cleared out so no taxese are due.  There is no way to force someone else to pay for something in crypto as users have to sign any asset transfer.

---

**JasoonS** (2022-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/guoliu/48/6734_2.png) guoliu:

> In our case, we automatically set the token price to 0 when a transfer is triggered. “Transfer” thus still follows the continuous auction logic of Harberger Tax, where the owner set the price to 0 then the receiver gets it for free.

That is the same as giving away the NFT, since anyone could claim it for zero too (this sounds undesirable for almost all use cases). There could be a “approveReceipt” function of sorts that allows a recipient to add deposit+chose price before a token gets sent.

In wildcards we have a gift function that requires the sender to give some time-period amount of deposit along with the NFT so that it doesn’t auto foreclose as soon as it is sent (it is sort of ‘gift of giving’ function). Additionally, this means it is less likely to be a predatory attack on the rest of the users deposit given the minimum time is long enough and participants are relatively active. Once again, I think this kind of mechanism is project dependant.

In any case, I don’t think one rule fits all here, and I think many projects may decide to completely remove the `transfer` function from erc721 standard (ie, a new type of token that isn’t erc721 compliant).

---

**TimDaub** (2022-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mdnorman/48/6722_2.png) mdnorman:

> You don’t want to make it a single date because then folks will try to game the system, and you don’t want to make it “all year long” because you don’t know when it will actually be assessed.

In libharberger, a tax period is the block time of Ethereum. IMO this will always work considering that the percentage can be adjusted to low or high depending on the frequency of new blocks being mined.

---

**TimDaub** (2022-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/guoliu/48/6734_2.png) guoliu:

> Ownership under Harberger Tax corresponds to tax obligation, so transferring token is also transferring tax obligation. This can be used as a form of attack, where the attacker set the price very high and then transfer it to the victim. (In the case where tax is prepaid/deposited and allocated for each token, it can be mitigated by clearing deposits of all tokens I do not own, but it can still cause unwanted consequences)

I actually like this model as it may simplify implementation with deprecating licenses. Essentially, to start possessing a Harberger Token, one attaches ETH that then gets continuously taxed until the ETH amount is zero.

- By sending more ETH, the token’s self-assessed value goes up
- By letting ETH get taxed, the token’s self-assessed value goes down
- By transferring the token to another account, the token’s ETH credit is transferred to that account too
- In case a token has an ETH balance of zero, anyone can buy it directly from the tax authority

---

**TimDaub** (2022-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/will-holley/48/5956_2.png) will-holley:

> (see example here ).

I know I’ve been beating this dead horse for too long but isn’t this function vulnerable to attacks? [Integer Division - Ethereum Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/development-recommendations/solidity-specific/integer-division/)

---

**guoliu** (2022-08-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timdaub/48/5038_2.png) TimDaub:

> Essentially, to start possessing a Harberger Token, one attaches ETH that then gets continuously taxed until the ETH amount is zero.

It is a neat mental model. Each token has its own deposit account, which does not change with ownership transfer, but determines if current ownership should be revoked.

One implication is that one cannot get back the deposit after losing ownership, whether intentionally or bid by another buyer. And there would be one strategy to buy in tokens with a higher deposit balance.

---

**guoliu** (2022-08-06):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> There is no way to force someone else to pay for something in crypto as users have to sign any asset transfer.

It is true with the following implementation:

- tax is pre-paid
- pre-paid tax is per token
- after ownership changes, the balance in pre-paid tax is returned to the previous owner

But in other implementations, transferring tokens can still drain tax (pre-paid or allowance) unintentionally.

[@TimDaub](/u/timdaub) 's idea above should also be able to avoid such tax drain since the tax account is only attached to the token and detached from the payer address.

---

**will-holley** (2022-08-10):

When using a deposit model, the leaser should be remitted their deposit, post tax-collection, on lease takeover or foreclosure, unless they are actively transferring their lease, in which case the deposit should also transfer.

---

**will-holley** (2022-08-10):

Can you specify the type of attack your thinking of?  I have encountered overflow issues with the division here when fuzzing during testing: [partial-common-ownership/Taxation.sol at 3e7713bc60b6bb2e103320036ec5aeaaaceb7d2b · 721labs/partial-common-ownership · GitHub](https://github.com/721labs/partial-common-ownership/blob/3e7713bc60b6bb2e103320036ec5aeaaaceb7d2b/contracts/token/modules/Taxation.sol#L191).  I’ve looked into solving it by switching over to DSMath but haven’t spent much time on the implementation.


*(27 more replies not shown)*

---
source: magicians
topic_id: 10451
title: "EIP-5507: Refundable NFTs"
author: Pandapip1
date: "2022-08-19"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-5507-refundable-nfts/10451
views: 2983
likes: 6
posts_count: 24
---

# EIP-5507: Refundable NFTs

https://github.com/ethereum/EIPs/pull/5507

## Replies

**SamWilsn** (2022-09-02):

Bit of bikeshedding on the function names. The base interfaces you’re extending don’t use a `get` prefix for getters.

- refundOf, or maybe compensationOf.
- refundableUntil?

---

**Pandapip1** (2022-09-03):

`refundOf` and `refundDeadlineOf` seem like sensible names.

---

**5cent-AI** (2023-01-18):

Have to say, this is an amazing idea. I had a similar idea before and paid attention to its early version 721R.

---

**5cent-AI** (2023-01-18):

For `EIP-721 Refund Extension` and `EIP-1155 Refund Extension`, it is recommended to support batch refunds to improve efficiency.

`EIP-721 Refund Extension` :

```auto
function refund(uint256[] tokenId) external;
```

`EIP-1155 Refund Extension`:

```auto
 function refund(uint256[] tokenId, uint256[] amount) external;
```

---

**Pandapip1** (2023-01-18):

How does this increase efficiency? Generic multicalls make this entirely redundant.

---

**5cent-AI** (2023-01-18):

Refunds for multiple NFTs can be combined into 1 transaction.

For example, NFT#1:1ETH;nft#2:2ETH;nft#3:3ETH

This method can directly transfer 6ETH to the refunder.

---

**Pandapip1** (2023-01-18):

This is fair enough, but with [EIP-5920: PAY opcode](https://eips.ethereum.org/EIPS/eip-5920) (CFI Cancun), this would take effectively the same amount of gas.

This does remind me: multicall hasn’t been standardized yet. I’ll go ahead and do that.

---

**william1293** (2023-02-18):

In fact, in the UK and other EU countries, consumers are legally entitled to a 14-day cooling-off period when purchasing goods or services online, under what is known as the “Distance Selling Regulations”, which also cover digital goods and downloads, such as books, in-game purchases, and NFTs. So, perhaps in the sale of NFTs, eip5507 is not optional but mandatory.

---

**SamWilsn** (2023-02-24):

I’d like to discuss the motivation for this proposal, in the context of whether or not it should be an ERC. I want to make it very clear that I *do* see a non-zero value in having refundable tokens, but I don’t believe the idea is general enough to be put in an EIP.

> Greater Compliance with EU “Distance Selling Regulations,” which require a 14-day refund period for goods (such as tokens) purchased online

Presumably any token sale in the EU—and not just the initial purchase—needs to have the 14 day return policy?

> NFT marketplaces could place a badge indicating that the NFT is still refundable on listings, and offer to refund NFTs instead of listing them on the marketplace

I fear this will cause more trouble than its worth. If the badge is automated, a malicious contract could claim to support ERC-5507, but not actually allow users to refund. If the badge is manual, only high profile (or high paying) tokens will get the verification on marketplaces.

> DExes could offer to refund tokens if doing so would give a higher yield

If possible, this one seems like a point in favour of standardizing. I’d like to see some comments from an exchange developer to see what their thoughts on this are.

> Better wallet confirmation dialogs

I’m not sure I understand this one. Would this just be a notice on the transaction signing screen that says “this token might be refundable”? If so, how would a wallet decide to show it? Heuristics on mint functions?

---

All of that aside, I have a few more technical-ish questions:

- What differentiates a refund from a collateral-backed loan with an expiry date? Are there existing standards/libraries that handle these loans we could take inspiration from?
- Why does this need to be an extension on the token itself, and not in a separate escrow contract?
- Could an attacker mint large amounts of the token, dump it on the market while the token is hot, buy it back once the token price drops and refund it?

---

Further:

> in terms of the smallest divisible unit

Should that be “indivisible” unit?

---

**Pandapip1** (2023-02-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Presumably any token sale in the EU—and not just the initial purchase—needs to have the 14 day return policy?

Yes. But this helps specifically for ITOs, which would definitely require greater legal scrutiny. This is mentioned in the abstract (emphasis added):

> This ERC adds refund functionality for initial token offerings to ERC-20, ERC-721, and ERC-1155.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I’m not sure I understand this one. Would this just be a notice on the transaction signing screen that says “this token might be refundable”? If so, how would a wallet decide to show it? Heuristics on mint functions?

I meant special prompts, for example with ERC-20/721/1155 `transfer`. Instead of an ugly prompt showing the ABI-decoded transaction data, the wallets could instead display a more human-readable prompt.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Should that be “indivisible” unit?

Yes. Thanks for catching that typo!

---

**Pandapip1** (2023-02-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> What differentiates a refund from a collateral-backed loan with an expiry date? Are there existing standards/libraries that handle these loans we could take inspiration from?

I don’t think there’s any functional difference here. But “collateral-backed loan with an expiry date” is harder to understand than “tokens are refundable until X date.”

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Why does this need to be an extension on the token itself, and not in a separate escrow contract?

Easier introspection by DApps, and avoiding extra gas fees through unnecessary `CALL`s.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Could an attacker mint large amounts of the token, dump it on the market while the token is hot, buy it back once the token price drops and refund it?

Yes. This is a feature, not a bug.

---

**Pandapip1** (2023-02-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Are there existing standards/libraries that handle these loans we could take inspiration from?

Not that I’m aware of.

---

**dievardump** (2023-02-28):

I think this should be in the metadata, not in the contract.

0.1eth on day of purchase will not be 0.1eth on day of asking refund. So this can not be directly automated on-chain.

Needs to go through projects’ management contact.

So an EIP, maybe, but not to standardize the behavior on-chain, only its representation in the meta: until when it can be refunded, and who to contact/how to contact them to get this refund.

---

**5cent-AI** (2023-02-28):

I have learned about some projects that promised refunds, but their verbal or written promises were not trusted by community members, even if these projects had a strong background. Community members accept that code is law, and on-chain automated execution is a more trusted mechanism.

---

**dievardump** (2023-02-28):

That people are trusting the companies or not should definitely not be the concern of the EIP.

I do think it’s good to add refund policy and contact somewhere, but I don’t think it can work on-chain, for various reasons:

- Not everyone buys using a wallet. You can buy using credit card and expect refunds to happen to your bank account. Any company doing off-ramp will redirect you to the seller’s websit if you ask them about refund policy.
- calling refund has a tx cost. There is nothing to stop a company to make fees to ask the refund so expensive that people will just never call it.
- ETH price varies way too much. It will require an oracle to do the refund (to store $/€ price at buy time or to retrieve it at refund time), which again will be very expensive both in term of fees for the buyer/refund asker & the seller.
- People are (righlty) using more and more hot wallet to buy stuff and then send to cold wallet. This would void the policy since there is no way to know if this was a sale or not.

I would like to add:

European refund policy has exceptions. Concert Tickets, digital content considered “open” after start of use etc…

NFTs are still young, but I have little to no doubts the ones with high speculative values will enter these exceptions. Especially because NFTs do not have the same status everywhere in Europe.

So for sure we need these for the future, when NFTs will be more than just jpegs, but on-chain is not sustainable.

---

**Pandapip1** (2023-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> People are (righlty) using more and more hot wallet to buy stuff and then send to cold wallet. This would void the policy since there is no way to know if this was a sale or not.

This EIP does not specify whether the refund should be voided on transfer, and the most common implementation of it *doesn’t* void it on transfer (a good thing, IMO).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> ETH price varies way too much. It will require an oracle to do the refund (to store $/€ price at buy time or to retrieve it at refund time), which again will be very expensive both in term of fees for the buyer/refund asker & the seller.

The `approve`/`refundFrom` pattern allows refunds with stablecoins.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> calling refund has a tx cost. There is nothing to stop a company to make fees to ask the refund so expensive that people will just never call it.

This is a good point, but it is partially mitigated by AA.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> Not everyone buys using a wallet. You can buy using credit card and expect refunds to happen to your bank account. Any company doing off-ramp will redirect you to the seller’s website if you ask them about refund policy.

Again, this can be done using the `approve`/`refundFrom` flow.

---

Side note: do we want to add `refundTo`/`safeRefundTo` methods? I’m actually leaning towards yes on this one.

- Keep as-is
- Add refundTo and safeRefundTo
- Add refundTo and safeRefundTo and REMOVE the old refund

0
voters

---

**5cent-AI** (2023-02-28):

Even if a person buys with a credit card, he still actually owns the wallet. And we can’t implement a direct refund to his credit card, so it doesn’t have to be too complicated.

---

**dievardump** (2023-03-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> This EIP does not specify whether the refund should be voided on transfer, and the most common implementation of it doesn’t void it on transfer (a good thing, IMO).

Yep my bad. I was actually thinking companies wouldn’t refund something that might have been resold, but thinking about it, as long as you own the receipt, it should be ok.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> The approve/refundFrom pattern allows refunds with stablecoins.

Good luck saving for each buy the current price in stable. Let’s make those mints way more expensive than they should.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png) 5cent-AI:

> Even if a person buys with a credit card, he still actually owns the wallet. And we can’t implement a direct refund to his credit card, so it doesn’t have to be too complicated.

No, lots of places are actually doing custodial stuff. There is a bigger picture to look at here for something supposed to target laws.

And if as a consumer I buy with a CC, I want my refund to my CC. Each tx cost.

An on-chain refund system will have a hard time to work at scale. Both because of tokens volatility and cost of tx.

---

**5cent-AI** (2023-03-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> lots of places are actually doing custodial stuff.

As of now, I have not seen statistical data to support this conclusion. It does exist, but it is not widespread.

Each EIP has its own scope and standards. We may not overcomplicate things and make it inconvenient to adopt, while also considering the importance of its general applicability. If you want to pay with a credit card and the project can also accept credit card payments, then the refund process becomes simpler for you. However, this situation may not be among the issues that this EIP aims to address.

---

**SamWilsn** (2023-03-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> I don’t think there’s any functional difference here. But “collateral-backed loan with an expiry date” is harder to understand than “tokens are refundable until X date.”

You’re absolutely right. My point was that this functionality is a subset of a more general primitive, and probably shouldn’t exist on its own.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> SamWilsn:
>
>
> Why does this need to be an extension on the token itself, and not in a separate escrow contract?

Easier introspection by DApps, and avoiding extra gas fees through unnecessary `CALL`s.

On the other hand: this proposal wouldn’t work for existing tokens, and would require re-implementing the same logic in every new compatible token. Since there’s no shared implementation, every token would have to be vetted independently.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> SamWilsn:
>
>
> Could an attacker mint large amounts of the token, dump it on the market while the token is hot, buy it back once the token price drops and refund it?

Yes. This is a feature, not a bug.

Doesn’t this unfairly create a scalper market then? Where it becomes common for bots to buy up tokens and resell them, keeping the refund rights to themselves, which kinda invalidates the whole point of this proposal?


*(3 more replies not shown)*

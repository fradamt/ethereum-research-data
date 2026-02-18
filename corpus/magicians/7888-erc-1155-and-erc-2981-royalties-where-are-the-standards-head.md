---
source: magicians
topic_id: 7888
title: ERC-1155 and ERC-2981 Royalties - where are the standards heading to?
author: Waza
date: "2022-01-04"
category: ERCs
tags: [token, erc1155, royalties, eip2981, "2981"]
url: https://ethereum-magicians.org/t/erc-1155-and-erc-2981-royalties-where-are-the-standards-heading-to/7888
views: 2029
likes: 2
posts_count: 8
---

# ERC-1155 and ERC-2981 Royalties - where are the standards heading to?

Hi,

I am exploring **ERC 721 and 1155** with possible **EIP 2981 royalties implementation**.

I would like to have the opinion of more experienced developers to better understand what can be done and where the standards are heading to.

There are some instances in which a digital assets, let’s say a song from a music album, has the necessity of its **unique ID** in order to be distinguished from the other songs on the same album.

At the same time the author does not want the asset to be sold as an individual NFT but rather as a **token with limited supply**.

For this it would make sense to mint the album in batch as per OZ 1155: **every song has its own ID and supply amount**.

Several developers are trying to extend this with EIP2981, adding two arrays to define **ONE address for every token ID** and **their relative % of royalties**, hopefully to be received on compliant secondary sales.

Unfortunately it is very likely that a digital asset (like the above mentioned song) has more than one author who would like to receive royalties on secondary sales and **a one-to-one relationship between the token ID and address of the royalty owner is not enough**.

For this I have also seen a possible implementation of FNFT, with **ERC721 for the type of token and ERC20 to introduce fractional ownership** of the NFT.

This would solve the one-to-one issue and it would be possible to identify multiple royalty owners for a digital asset… but it would also introduce another problem: the fans who buy tokens would be identified as partial owners as well, possibly set to receive royalties that should only go to the actual authors.

As I find the FNFT (ERC721+ERC20) not viable in this instance, are you aware of any other solution being explored to **identify and differentiate between the multiple creators of an asset and the current owners?**

Additionally, **is the EIP2981 actually excluding the possibility to implement an array of addresses to receive royalties for one token ID?**

Thank you for your replies,

Best!

## Replies

**wminshew** (2022-01-04):

Hi Waza - I don’t have any knowledge about where the standards are headed, but I believe what you want can be done today by pointing the royalty address at a splitter contract. Something like:

- OZ impl
- mirror impl
- 0xSplits impl (dislaimer: am working on this project; set to launch end of month)

---

**MaxFlowO2** (2022-01-05):

Glad you said something…

[GitHub - MaxflowO2/ERC2981: EIP-2981 solution](https://github.com/maxflowo2/ERC2981) has a few implementations of ERC2981 (big 3) under eip/2981

---

**julesl23** (2022-01-05):

Hi,

Another possible solution is to use my [EIP-4393](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-4393.md) to pay the royalties. An implementation of ITipToken can pay out the royalties to multiple holders (authors) of an ERC-1155 token id and split the %s relative to the token id balance held by each author.

Fans who buy the token id would not receive royalties from secondary sales as they would not be approved by ITipToken to receive them. Can extend ERC-1155 to implement ITipToken.

You can batch up the royalties and send them to the authors (i.e. tip) when the amount is enough relative to the gas price cost for multiple songs and albums. Plus authors can also withdraw only when worth it relative to the gas cost.

---

**julesl23** (2022-01-15):

I’ve added further clarification to [EIP-4393](https://eips.ethereum.org/EIPS/eip-4393#royalty-distribution) for royalty distribution scenarios.

I’ll explain it with this example…

Imagine a song generates royalties from multiple music distributors, when a distributor calls the ‘tip’ method to send the royalty to the song’s NFT then the implementation of the ‘tip’ method is able to split the royalty %s automatically to the song’s single or multiple creator(s) less any optional fee.

---

**frangio** (2022-01-18):

This is addressed in the [discussion for EIP-2981](https://github.com/ethereum/EIPs/issues/2907), the recommendation is to use a splitter contract as the royalty receiver.

See for example OpenZeppelin’s [PaymentSplitter](https://docs.openzeppelin.com/contracts/4.x/api/finance#PaymentSplitter).

---

**Waza** (2022-01-20):

Thank you everyone for the great inputs!

I am examining the payment splitter by OpenZeppelin.

Wondering if the gas fees would make an automatic payout on every transaction unviable hence the need to call the payment split only when accumulated royalties are higher than gas fees required for claiming them.

---

**wminshew** (2022-01-24):

yeah this flow is basically what 0xsplits is designed around, plus you save >~1m gas on deployment


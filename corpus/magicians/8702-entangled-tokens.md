---
source: magicians
topic_id: 8702
title: Entangled tokens
author: victormunoz
date: "2022-03-24"
category: Magicians > Primordial Soup
tags: [nft, token]
url: https://ethereum-magicians.org/t/entangled-tokens/8702
views: 2736
likes: 1
posts_count: 5
---

# Entangled tokens

We define entangled tokens to A and B to the tokens that share a same wallet, so that any transaction with the wallet could be operated by any of them.

The functionality is similar to the entanglement of two particles but with tokens, in the sense that whatever changes the state of A it affects B.

We advocate the entangled tokens have key utility for the value preservation (vreservation) of digital assets, though other further applications can be devised. In the case of value preservation, its importance arises since we’ll see a massive migration of value (in the history of mankind) onto the Blockchain along with a new identity forged on blockchain for this value. This value needs to be preserved. So we see how value migrates (1), tokenises (2) and preserves (3) the value of digital assets as NFT as a means of a totally new identity and wealth management for a private and safe assets scrow for all, and redefining the today’s role of consumers towards a more co-creation and co-ownership of locals.

An use case is to keep contact between an artist and an buyer of its NFTs. If an artist T has created a digital piece of art P with an NFT with wallet, then T creates 2 entangled tokens A and B so that he keeps A and transfer B to the wallet of P. By construction of entangled tokens, only one transfer is possible for them, thus the artist proofs he’s been the creator of P by sending a transaction to A that is visible from B. Otherwise, the owner of P might check the authenticity of the artist by sending a transaction to B so that the artist might proof by showing the outcome out of A.

## Replies

**noturhandle** (2022-04-03):

Hey Viktor,

Would it be valid to describe these tokens as NTTs (non-transferable tokens) for NFT wallets?

---

**philipjonsen** (2022-04-03):

Hey! Yes subjects like this should be discussed maybe in private first, since this is bigger than any project/token/blockchain and steps to talk about what really is going on.

---

**SamWilsn** (2022-06-17):

A couple non-formatting related questions:

- Why use exactly two NFTs to control the wallet, instead of allowing any number of NFTs?
- Would it make more sense to define a function that allows arbitrary calls as the wallet (just forwards the calldata) instead of explicitly specifying tokenTransfer?
- Is it necessary to create a standard around this, as opposed to just building a smart contract wallet with this functionality? Seems like EIP-721 covers the marketplace functionality, and any wallet functions will need a UI hosted somewhere anyway. Gnosis Safe is a great example of a smart contract wallet (though it doesn’t use NFTs.)

---

**MidnightLightning** (2022-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/victormunoz/48/5658_2.png) victormunoz:

> the artist proofs he’s been the creator of P by sending a transaction to A that is visible from B. Otherwise, the owner of P might check the authenticity of the artist by sending a transaction to B so that the artist might proof by showing the outcome out of A

If this is the desired interaction, what you want I’m not sure is “tokens” but a separation of the roles of “creator” and “owner”? The ERC721 standard has an `ownerOf` inquiry function that tracks who owns a given token (which covers who currently purchased and owns the artwork). Often the collection overall has an “owner” that is the creator/manager of the collection overall, which in your scenario would be the artist that made the tokens. Inquiring who is the current owner of a given token, or who is the creator of a whole collection are also usually “view” functions, meaning the user doing the inquiry doesn’t need an on-chain transaction to get that data, it can be done with a free call to any Ethereum node.

If it’s needed for a human to be able to prove they are indeed “the artist” of the collection, they could sign a message from the address that is currently the owner of the collection, proving they are in control of the private key of that address at that moment.

If you’re envisioning a need for different artists/creators within one ERC721 token, the discussion over [here](https://ethereum-magicians.org/t/erc-4400-erc-721-consumer-extension/7371) about different roles  added to a token standard, might be an option of a way to implement this, without it needing to be a completely separate standard?

Is there another use-case you’re thinking of where “entangled tokens” would be a useful way to track things?


---
source: magicians
topic_id: 4869
title: "Secret Ethereum Bridge: Programmable Privacy for Ethereum and ERC-20s"
author: Faith
date: "2020-10-24"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/secret-ethereum-bridge-programmable-privacy-for-ethereum-and-erc-20s/4869
views: 553
likes: 0
posts_count: 1
---

# Secret Ethereum Bridge: Programmable Privacy for Ethereum and ERC-20s

**We are thrilled to announce our new bridge connecting Ethereum and [Secret Network](https://scrt.network/),**  currently live on testnet and arriving soon to mainnet! This is the most important update since our [mainnet upgrade] last month that made Secret Network  **the first and only public blockchain with full smart contract privacy on mainnet.**  Now we can turn our focus to providing privacy to other blockchain ecosystems, including Ethereum, the most vibrant decentralized ecosystem. We’ve built a simple way to create synthetic (wrapped) ETH and ERC-20 tokens on Secret Network that can be used  *with full privacy, at lower cost.*

Keep reading to learn more about how to lock ETH and ERC-20 tokens in order to receive / use privacy-preserving “secretETH” and other potential Secret Tokens!

## Why does this matter?

Our mission has always been to increase adoption of decentralized technologies by improving their usability and security, focusing first on scalable privacy features. Currently the Ethereum ecosystem is showing the most adoption, by any metric - but it’s still held back by a lack of privacy for users and developers.

The DeFi ecosystem on Ethereum is growing at a parabolic rate. Meanwhile, so is the sophistication of analytics tools like [Nansen]Now it’s easier than ever to identify high-performing portfolios, mimic them, and even deanonymize addresses. What some call the “Renaissance of DeFi analytics” actually poses a real threat to adoption of a decentralized universal financial ecosystem. Individuals and organizations don’t and can’t accept this level of invasiveness and absolute transparency in our everyday financial lives. Privacy is very much needed today - and the Secret Ethereum Bridge brings privacy to ETH and ERC-20s now!

## How does it work?

The Ethereum bridge transfers between assets on the Ethereum network (ETH/ERC-20) and [Secret Tokens], which are specified by the SNIP-20 spec. Secret Tokens combine the programmability of ERC-20s with the privacy of coins like Zcash or Monero. The bridge is bidirectional, so SNIP-20 assets can then be redeemed for their Ethereum equivalent.

To illustrate, here’s an example of what a user interaction with the bridge would look like:

1. Alice sends 10 ETH to an Ethereum lock contract and provides her Secret Network address.
2. Multisig committee watches this event and sends a mint request of 10 secretETH to the address Alice provided in step 1. The Secret Network then mints these wrapped tokens accordingly.
3. Alice can now transact with secretETH on Secret Network and utilize her secretETH in the native Secret [DeFi ecosystem].
4. When she wishes to move back to Ethereum, Alice burns her secretETH and provides an ETH address to receive back her ETH.
5. Multisig committee creates a TX on Ethereum that instructs the Ethereum Bridge smart contract to move ETH to Alice’s address in step 4.

**This process can be replicated for any amount and for any ERC-20 token.**

Link for the full blog post: https://blog.scrt.network/secret-ethereum-bridge-privacy/

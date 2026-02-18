---
source: ethresearch
topic_id: 1947
title: From Ethereum keys to PGP communications
author: miohtama
date: "2018-05-08"
category: Applications
tags: []
url: https://ethresear.ch/t/from-ethereum-keys-to-pgp-communications/1947
views: 2285
likes: 0
posts_count: 3
---

# From Ethereum keys to PGP communications

I am pondering ways to communicate with the Ethereum address owners safely. We start from the assumption that we know the Ethereum address and email address of the person (voluntarily reported).

Because I do not want to create yet another instant messaging protocol, people are already using email and PGP is somewhat working, I was wondering would it be possible to

- Make users convert their Ethereum private keys to PGP compatible keys (e.g. with a web based client side tool or static HTML/JS bundle) so that they can receive PGP encrypted emails
- Send email to users, encrypted with a PGP key derived from Ethereum public key (that is probably picked up from the blockchain from the associated transfer to the address)

## Replies

**vbuterin** (2018-05-08):

I believe that PGP supports secp256k1 signatures now, so you could do it if you want.

---

**miohtama** (2018-05-09):

Thank you. I’ll explore how widespread secp256k1 support in PGP is, in the mail clients.


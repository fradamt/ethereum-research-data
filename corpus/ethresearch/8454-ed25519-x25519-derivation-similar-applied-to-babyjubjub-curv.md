---
source: ethresearch
topic_id: 8454
title: Ed25519 -> X25519 derivation/similar applied to babyjubjub curve?
author: vans163
date: "2021-01-02"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/ed25519-x25519-derivation-similar-applied-to-babyjubjub-curve/8454
views: 1824
likes: 0
posts_count: 2
---

# Ed25519 -> X25519 derivation/similar applied to babyjubjub curve?

Is anyone aware of a way to box/unbox messages using babyjubjub curve (way to achieve stream cipher mode is fine too).

This is similar to how you can use a Ed25519 key and turn it into a X25519 key, generate a shared secret then produce encrypted messages only the parties holding the secret can read.

## Replies

**garvitgoel** (2022-04-22):

Performing ed25519 related operations is very expensive on ethereum. You could consider using zk-snarks to provide you the necessary proofs on-chain. Check out this - https://github.com/Electron-Labs/ed25519-circom


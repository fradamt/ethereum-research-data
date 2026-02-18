---
source: ethresearch
topic_id: 15214
title: "RFC: Hierarchical Deterministic Wallet Derivation Function"
author: hazae41
date: "2023-04-04"
category: Cryptography
tags: []
url: https://ethresear.ch/t/rfc-hierarchical-deterministic-wallet-derivation-function/15214
views: 1974
likes: 4
posts_count: 5
---

# RFC: Hierarchical Deterministic Wallet Derivation Function

## Summary

This RFC defines a way for dApps to deterministically generate Ethereum accounts, similar to BIP-32, out of the Ethereum signature of an Ethereum account.

## Constraints

We want dApps to generate “stealth” identities for an user, which we will call Bob, connected through “Sign-in with Ethereum” with his main identity, which we will call M.

Let’s define this process by the function f(X) where X is the identity to use.

### Private

We also want this process to be as private as possible, we don’t want Bob to make a transaction with his main identity, we don’t want him to make any RPC requests. This process should ideally be offline, except if using network-based connection e.g. WalletConnect. Ethereum signature is a good candidate for this as it’s offline.

### Hierarchical

We want to be able to generate multiple identities based on an index, similarly to BIP-32.

Let’s add a parameter i to the function f(X, i) for the index of such account.

Bob can generate address A = f(M, i), he can also generate address B = f(M, i + 1), without having generated A in the first place (generating B only requires M)

### Deterministic

We want this process to be deterministic. If Bob goes to a dApp on his computer, generates an address A = f(M, i), then goes to the same dApp on his phone, and generate an address B = f(M, i), then both identities MUST be the same

i1 = i2 => A = B

i1 != i2 => A != B

### Salted

We also want this process to be salted. The function on the dApp A will have a salt, and the function on dApp B a different salt.

Let’s add a parameter s to the function f(X, i, s)

If Bob goes to dApp A, generates an address A = f(M, x, s1), then goes to dApp B, generates an address B = g(M, x, s2), they MUST NOT be the same.

s1 = s2 => A = B

s1 != s2 => A != B

### Recursive

We want the process to be recursive. Bob can generate the address AA = f(A, i, s) where A = f(M, i, s). By only having A and not M.

## Defining f

With all constraints defined, we will call f a (Crypto Secure) (Private) Hierarchical Deterministic (Salted) Wallet Derivation Function, or just HDWDF

Ethereum signatures, or more specifically secp256k1 signatures are good candidates for such function

### Proposal 1 with inner salt

f(wallet, index, salt) = secp256k1(sign(wallet, HMAC("Ethereum Wallet Derivation: " + index, salt)))

Where

- HMAC can be HMAC-SHA256 or HMAC-KECCAK256; I would be in favor or SHA since it’s compatible with WebCrypto
- sign(X, m) is the process of signing a message m with identity X, with  e.g. eth_signMessage
- secp256k1(seed) is derivating a secp256k1 curve point from a crypto secure seed, with a KDF if necessary
- salt is a public crypto secure random value

The problem with such function is that the message to be signed is not human readable since it’s a HMAC output

### Proposal 2 with outer salt

We could use HMAC outside the signature

g(wallet, index, salt) = secp256k1(HMAC(sign(wallet, "Ethereum Wallet Derivation: " + index), salt))

It has the advantage of being human readable, but the downside of being more easily craftable, a malicious dApp could make the user sign the message and then use the salt of another dApp

### Proposal 3 with human-readable name

One solution could be to use the dApp name in the message, and remove the HMAC

h(wallet, index, name) = secp256k1(sign(wallet, "Ethereum Wallet Derivation for " + name + " at index " + index))

This message could also be formatted using eth_signTypedMessage

Let me know what you think about it!

## Replies

**hazae41** (2023-04-05):

# Addendum

## Zero-Knowledge Provable

Ideally, such process should be ZK provable, like “I prove that the address A is derived from the address M”

For example, Bob wants to prove that address A is derived from an address M where he holds 1 ETH, without revealing the address M:

1. Bob proves M holds 1 ETH
2. Bob proves A is derived from M
3. Bob proves he owns A

But, I don’t know much about ZK proofs, so I can’t tell if this is possible

---

**hazae41** (2023-04-10):

## Addendum

### Visualisation

You can visualize HDWDF like a wallet tree. Since it’s recursive, you can have an infinite list of child wallets for any parent wallet.

[![hdwdf](https://ethresear.ch/uploads/default/optimized/2X/2/2d844e05053c23802d8db74fd2f706e2d1a9dde4_2_372x500.png)hdwdf678×909 25.5 KB](https://ethresear.ch/uploads/default/2d844e05053c23802d8db74fd2f706e2d1a9dde4)

### Path description

A dapp can derivate a wallet multiple times by following a certain path in order to ensure some secrecy in the process.

Such path can be described by the index of the current wallet in the path, followed by a slash or a dot, like “2/5/6/3”. For example, the wallet “ACC” in the image above can be described as “0/3/3” from the root (here, the root is the seed phrase).

Some dapp could even use a random path to use as a second, per-user, salt; and save it somewhere (local storage? smart contract? server?)

---

**hazae41** (2023-05-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/hazae41/48/11731_2.png) hazae41:

> ### Proposal 3 with human-readable name
>
>
>
> One solution could be to use the dApp name in the message, and remove the HMAC
>
>
> h(wallet, index, name) = secp256k1(sign(wallet, "Ethereum Wallet Derivation for " + name + " at index " + index))
>
>
> This message could also be formatted using eth_signTypedMessage
>
>
> Let me know what you think about it!

I think this is the way to go, as it is used similarly by dapps like Aztec Connect, I will make an EIP soon

---

**sk1122** (2023-06-13):

can we use BIP-44 in this?

We can tweak path’s a little bit and generate public/private keys?


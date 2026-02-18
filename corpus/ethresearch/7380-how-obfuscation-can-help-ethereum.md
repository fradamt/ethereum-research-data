---
source: ethresearch
topic_id: 7380
title: How obfuscation can help Ethereum
author: vbuterin
date: "2020-05-09"
category: Cryptography
tags: []
url: https://ethresear.ch/t/how-obfuscation-can-help-ethereum/7380
views: 6079
likes: 20
posts_count: 12
---

# How obfuscation can help Ethereum

[Obfuscation](https://www.iacr.org/archive/crypto2001/21390001.pdf) is [in many ways](https://eprint.iacr.org/2013/454.pdf) the ultimate cryptographic primitive. Obfuscation allows you to turn a program P into an “obfuscated program” P' such that (i) P' is equivalent to P, ie. P'(x) = P(x) for all x, and (ii) P' reveals nothing about the “inner workings” of P. For example, if P does some computation that involves some secret key, P' should not reveal that key.

**Obfuscation is not yet available; [candidate constructions exist](https://eprint.iacr.org/2020/394.pdf), but they all depend on cryptographic assumptions that cryptographers are not happy with and some candidates have already been broken. However, recent research suggests that we are very close to secure obfuscation being possible, even if inefficient**.

The usual way to formalize the privacy property is that if there are two programs P and Q that implement the same functionality (ie. P(x) = Q(x) for all x) but maybe with different algorithms, then given obfuscate(P) and obfuscate(Q) you should not be able to tell which came from which (to see how this leads to secrecy of internal keys, consider a function that uses a key k to sign a message out of the set [1....n]; this could be implemented either by actually including k and signing a message that passes a range check, or by simply precomputing and listing all n signatures; the formal property implies that you can’t extract k from the first program, because the second program does not even contain k).

Obfuscation is considered to be so powerful because it immediately implies almost any other cryptographic primitive. For example:

- Public key encryption: let enc/dec be a symmetric encryption scheme (which can be implemented easily using just hashes): the secret key is k, the public key is an obfuscated program of enc(k, x)
- Signatures: the signing key is k, the verification key is an obfuscated program that accepts M and sig and verifies that sig = hash(M, k)
- Fully homomorphic encryption: let enc/dec be a symmetric encryption scheme. The secret key is k, the evaluation key is enc(k, dec(k, x1) + dec(k, x2)) and enc(k, dec(k, x1) * dec(k, x2))
- Zero knowledge proofs: an obfuscated program is published that accepts x as input and publishes sign(k, x) only if P(x) = 1 for some P

More generally, obfuscation is viewed as a potential technology for creating general-purpose privacy-preserving smart contracts. This post will both go into this potential and other applications of obfuscation to blockchains.

### Smart contracts

Currently, the best available techniques for adding privacy to smart contracts use zero knowledge proofs, eg. [AZTEC](https://www.aztecprotocol.com/) and [Zexe](https://eprint.iacr.org/2018/962.pdf). However, these techniques have an important limitation: they require the data in the contract to be broken up into “domains” where each domain is visible to a user and requires that user’s active involvement to modify. For a currency system, this is acceptable: your balance is yours, and you need your permission to spend money anyway. You can send someone else money by creating encrypted receipts that they can claim. But for many applications this does not work; for example, something like Uniswap contains a very important core state object which is not owned by anyone. An auction could not be conducted fully privately; there needs to be someone to run the calculation to determine who wins, and they need to see the bid amounts to compute the winning bid.

**Obfuscation allows us to get around this limitation, getting much closer to “perfect privacy”. However, there is still a limitation remaining**. One can naively assume obfuscation lets you create contracts of the form “only if event X happens, then release data Y”. However, outside observers can create a private fork of the blockchain, include and censor arbitrary transactions in this private fork (including copying over some but not all transactions from the main chain), and see the outputs of the contract in this private fork.

To give a particular example, key revocation for data vaults cannot work: if at some time in the past, a key k_1 could have released data D, but now that key was switched in the smart contract to k_2, then an attacker with k_1 could still locally rewind the chain to before the time of the switch, and send the transaction on this local chain where k_1 still suffices to release D and see the result.

Obfuscating an auction is a particular example of this: even if the auction is obfuscated, you can determine others’ bids by locally pretending to bid against them with every possible value, and seeing under what circumstances you win.

One can partially get around this, by requiring the obfuscated program to verify that an instruction was confirmed by the consensus, but this is not robust against failures of the blockchain (51% attacks or more than 1/3 going offline). Hence, it’s a lower security level than the full blockchain. Another way to get around this is by having the obfuscated program check a PoW instance based on the inputs; this limits the amount of information an attacker can extract by making executions of the program more expensive.

With this restriction, however, more privacy with obfuscation is certainly possible. **Auctions, [voting schemes](https://github.com/barryWhiteHat/maci) (including in DAOs), and much more are potential targets**.

### Other benefits

- ZKPs with extremely cheap verification: this is basically the scheme mentioned above. Generate an obfuscated program which performs some pre-specified computation f on (x, y) (x is the public input, y is the private input), and signs (x, f(x)) with an internal key k. Verification is done by verifying the signature with the public key corresponding to k. This is incredibly cheap because verifying a proof is just verifying a signature. Additionally, if the signature scheme used is BLS, verification becomes very easy to aggregate.
- One trusted setup to rule them all: generating obfuscated programs will likely require a trusted setup. However, we can make a single obfuscated program that can generate all future trusted setups for all future protocols, without needing any further trust. This is done as follows. Create a program which contains a secret key k, and takes as input a program P. The program executes P(h(P, k)) (ie. it generates a subkey h(P, k) specific to that program), and publishes the output and signs it with k. Any future trusted setup can be done trustlessly by taking the program P that computes the trusted setup and putting it into this trusted setup executor as an input.
- Better accumulators: for example, given some data D, one can generate in O(|D|) time a set of elliptic curve point pairs (P, k*P) where P = hash(i, D[i]) and k is an internal secret key (K = k*G is a public verification key). This allows verifying any of these point pairs (P1, P2) by doing a pairing check e(P1, K) = e(P2, G) (this is the same technique as in older ZK-SNARK protocols). Particularly, notice that a single pairing check also suffices to verify any subset of the points. Even better constructions are likely possible.

## Replies

**haael** (2020-12-25):

I am working on practical obfuscation algorithm, based on FAPKC https://github.com/haael/white-box-fapkc

---

**haael** (2020-12-25):

One thing I hope will be possible when we have obfuscation are trustless decentralized oracles. The obfuscated program could check for some fact outside a blockchain, and insert the result into the blockchain.

Also, a blockchain could have side-effects in real life and decide them based on the consensus. Imagine the blockchain revealing some secret only when certain conditions are met.

For a very concrete example, a program could perform financial transactions through Open Banking API. This would allow implementing a truly decentralized exchange. Historically, exchanges were the most vunerable part of the crypto industry, and also they generate most of the cost. Replacing them with trustless setup would be a huge improvement.

---

**kladkogex** (2020-12-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> a program PP into an “obfuscated program” P′P’ such that (i) P′P’ is equivalent to PP , ie. P′(x)=P(x)P’(x) = P(x) for all xx , and (ii) P′P’ reveals nothing about the “inner workings” of PP

I think this is impossible to solve for generic programs.

If you have a program that outputs y = x^2, then anyone will be able to deduce the algorithm by simply trying different values of x and observing y.

You probably mean that x and y are encrypted in some way and operations are performed on encrypted values?

Or the program should be complex/random enough so simply deducing the algorithm is impossible?

---

**haael** (2020-12-25):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Or the program should be complex/random enough so simply deducing the algorithm is impossible?

You are not able to learn anything about the program, *except what you can learn from inputs and outputs anyway*.

Formally:

Polynomial black-box attacker is someone who is able to run polynomially many instances of the program and deduce something about its structure.

Exponential black-box attacker is someone who is able to run exponentially many instances of the program. Exponential attacker is stronger than polynomial one.

Now a program is properly obfuscated if looking at the (obfuscated) source gives you only the power of a polynomial black-box attacker.

There are programs that can not be white-box obfuscated no matter what, so white-box obfuscation is not possible for every program. However, a simple banking-like system should be good, with only addition, comparison and multiplication with finite precision.

---

**kladkogex** (2020-12-25):

I see …

So you are not able to differentiate from the set of circuits that produce the same outputs having the inputs.

It is essentially a random oracle in the subspace of all circuits of say size less than N, that produce the given outputs having the inputs.

Similar to hash-to-curve for elliptic curves, but here you are essentially hashing into the subspace of circuits

---

**haael** (2020-12-25):

Yes. Here what you are thinking is indistinguishability obfuscation.

When you have 2 circuits calculating the same function and you treat them with indistinguishability obfuscation, you will not be able to determine which circuit was the source of any particular obfuscated representation. In layman terms, iO removes all metadata.

A stronger notion is “inversion obfuscation”, when you present a circuit obfuscated in such a way, so it is impossible to calculate its inverse. An interesting example of a real-life inversion obfuscation is the Chinese “evil transform” of geographical coordinates (duckduckgo). When you have invO, you can upgrade any symmetric cipher to a public cipher.

And the strongest notion is white-box obfuscation, which gives you the guarantee that when you present the obfuscated circuit, the attacker can only deduce from it as much as he could deduce from running the function on a remote machine and collecting the outputs. WB can upgrade any symmetric cipher to a homomorphic cipher. White-box obfuscation gives you a so-called virtual black box property, as if the function was run in a black box the attacker can’t see into.

Nothing is proven yet, but the majority consensus is that iO is possible for any circuit, but invO and WB are impossible in general. That means there are certain “traitor functions” that can’t be white-boxed no matter what. Still, many useful programs should be possible, like a banking system with addition, comparison and finite precision multiplication, or even the AES algorithm.

I hope it will be possible to make an oracke that starts an SSL session to a bank with Open Banking API, extract information and put it into a blockchain. This will let us make a truly decentralized exchange.

---

**kladkogex** (2020-12-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/haael/48/5400_2.png) haael:

> A stronger notion is “inversion obfuscation”, when you present a circuit obfuscated in such a way, so it is impossible to calculate its inverse.

Interesting … What about circuits that are inverse of themselves?

There has to be some additional requirement on the circuits for this to work ?) Correct ?)

---

**kladkogex** (2020-12-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/haael/48/5400_2.png) haael:

> hope it will be possible to make an oracke that starts an SSL session to a bank with Open Banking API, extract information and put it into a blockchain.

Can you provide a little longer description how this Oracle would work?

---

**haael** (2020-12-25):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Interesting … What about circuits that are inverse of themselves?

Inversion obfuscation would effectively hide that fact.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Can you provide a little longer description how this Oracle would work?

My goal is to make a decentralized exchange. Two parties agree to exchange coins at a certain price. Alice has coins, Bob has fiat money, and he’s using an Open Banking API enabled bank.

Alice prepares a white-box obfuscated program that holds a private token address inside. A public token address is presented to Alice. The program is configured with Alice’s bank account number and fiat price. Alice sends the program to Bob.

Bob first checks if the public address holds enough tokens. If it does, Bob makes a bank transfer to Alice. Then he runs the program. The program connects through SSL to the bank’s API endpoint. Bob possibly needs to authorize the request. The program checks Bob’s recent transfer history. If it finds the right transfer (Alice’s account, the right fiat amount), it will reveal the private key and Bob can claim the tokens.

Assumption is that the bank doesn’t lie through their OB API and that they allow use of such programs, because banks have the ability to ban certain apps from using OB API.

One problem to solve is to allow Alice to claim the tokens back if Bob doesn’t pay in time. Perhaps the program could reveal the private key after some time passes (i.e. 2 hours), using a blockchain as a trusted clock.

---

**yadavkaris** (2023-01-13):

I found all these interesting and want your guidance regarding smart contract obfuscation. It will be my pleasure if you can help me in this area of research.

---

**enricobottazzi** (2024-11-20):

> For a very concrete example, a program could perform financial transactions through Open Banking API. This would allow implementing a truly decentralized exchange. Historically, exchanges were the most vunerable part of the crypto industry, and also they generate most of the cost. Replacing them with trustless setup would be a huge improvement.

Can you elaborate more on the setup of this application?

EDIT: I see you already gave an explanation to that


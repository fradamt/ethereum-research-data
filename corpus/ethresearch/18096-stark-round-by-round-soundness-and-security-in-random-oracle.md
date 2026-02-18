---
source: ethresearch
topic_id: 18096
title: STARK Round By Round Soundness and Security in Random Oracle Model
author: EliBenSasson
date: "2023-12-31"
category: Cryptography
tags: [zk-roll-up]
url: https://ethresear.ch/t/stark-round-by-round-soundness-and-security-in-random-oracle-model/18096
views: 3620
likes: 7
posts_count: 4
---

# STARK Round By Round Soundness and Security in Random Oracle Model

Hi, want to bring attention to the analysis of ethSTARK security in the random oracle model given in the latest version of the [ethSTARK documentation](https://eprint.iacr.org/2021/582.pdf), which is also explained at a higher level in this [medium blog post](https://starkware.co/resource/safe-and-sound-a-deep-dive-into-stark-security/), which I’ll quote the very start of here. Happy to discuss further.

---

## TL;DR

- Non-interactive STARKs start as Interactive Oracle Proofs (IOPs), compiled into non-interactive ones in the random Oracle model.
- This post explains the recent update to the ethSTARK documentation, which gives a full and concrete analysis of the security of the ethSTARK protocol in the random oracle model.

## STARK Security Explained

A STARK proof system (Scalable Transparent Argument of Knowledge) is a powerful tool for computational integrity: it allows verifying the correctness of computations performed on public data in a trustless manner. In this blog post, we delve into the security provided by STARK proofs, defining it and exploring techniques to prove scheme security.

(Read Section 6 in the ethSTARK documentation (version 1.2) for full details and the important and comprehensive [independent work](https://eprint.iacr.org/2023/1071.pdf) of Block et al. on the topic.)

What are we trying to achieve with our security analysis? We would like to prevent a “successful attack” on the STARK system, which is given by a false statement and a STARK proof accepted by the STARK verifier for this (false) statement. Since false statements are dangerous and they can come in all sizes and shapes, we want to be secure against *all* false statements. Any false statement, even as trivial as 1+1=3, combined with a STARK proof accepted by a STARK verifier for this statement, is considered a successful attack on the system. (Those with a cryptographic background may be interested to know that STARKs also satisfy stronger security notions such as [knowledge soundness](https://eprint.iacr.org/2016/116.pdf), but for simplicity, this post focuses on the simpler case of soundness.*)*

How do we formally define the security of a STARK system? We do so by analyzing the “soundness error” which roughly measures the expected “cost” that an attacker would need to spend to construct a successful attack (i.e., find a STARK proof for a false statement that nevertheless is accepted by the STARK verifier). Mathematically speaking, the soundness error is a function *e*(*t*) that gets as input a time parameter “*t”*, representing the amount of computation time an attacker is willing to spend to mount the attack and outputs the success probability of the attacker in succeeding with the attack (finding a convincing proof of a false statement). As the “cost” *t* that the attacker is willing to spend grows, his success probability increases.

Thus far, we have defined the security of STARKs as a function *e(t),* which is not the way you naturally discuss security, say, on crypto Twitter. There, you probably heard statements of the form “The scheme has 96 bits of security”. How does such a statement translate to our security definition? There is no one answer to this, as people have slightly different interpretations of “*x* bits of security”:

- A very strict translation would mean that for any t between 1 and 2⁹⁶, the soundness error is e(t) ≤ 2⁹⁶ . This means that any attacker running time at most 2⁹⁶ has a tiny probability of success, smaller than 1/2⁹⁶, which is smaller than one in a billion times a billion times a billion.
- A more relaxed, and perhaps more common, translation is that 96 bits of security means that for any t, it holds that t/e(t) ≥ 2⁹⁶. This means that the success probability is (inverse) linear to the running time. For example, if an attacker has a running time 2⁸⁶, its success probability is at most 1/2¹⁰.

Read the rest [here](https://starkware.co/resource/safe-and-sound-a-deep-dive-into-stark-security/).

## Replies

**xz-cn** (2023-12-31):

Thank you [@EliBenSasson](/u/elibensasson) for the article. Do you think we can also analyze the security of a STARK system using the [Universal composability](https://en.wikipedia.org/wiki/Universal_composability) framework?

---

**EliBenSasson** (2023-12-31):

I think someone can. I know I most certainly can’t, as I have no time for that. But perhaps you will? ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**WizardOfMenlo** (2025-01-09):

Hi, very late reply but we ended doing this here: “zkSNARKs in the ROM with Unconditional UC-Security” (2024/724).

This shows that any IOP-based SNARK with zero-knowledge and state-restoration security (a weaker version of rbr soundness) is UC-secure.

In particular, this implies that STARKs are UC-secure.


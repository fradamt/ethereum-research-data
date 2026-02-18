---
source: ethresearch
topic_id: 15154
title: Leveraging an existing PKI for a trustless and privacy preserving identity verification scheme
author: Pierre
date: "2023-03-28"
category: Privacy
tags: []
url: https://ethresear.ch/t/leveraging-an-existing-pki-for-a-trustless-and-privacy-preserving-identity-verification-scheme/15154
views: 3523
likes: 11
posts_count: 9
---

# Leveraging an existing PKI for a trustless and privacy preserving identity verification scheme

*Thanks to [Andy](https://twitter.com/AndyGuzmanEth) and [Jay](https://twitter.com/Janmajaya_mall) for all the help during this project*

# Anonymous Adhaar

The [adhaar program](https://en.wikipedia.org/wiki/Aadhaar) is among the largest digital identity scheme in the world. It feats an enrollment of 1.2 billion people, accounting for around 90% of India’s population.

Adhaar cards carry both demographic and biometric data, including the holder’s date of birth and its fingerprint. They are used in a variety of contexts such as loan agreements or housing applications.

We present how to leverage zero-knowledge to verify an adhaar’s card validity. This achievement has a variety of potential applications. Leveraging an existing public key infrastructure allows us to cheaply provide a robust proof of identity. Also, the zero-knowledge property of our verification provides a privacy-preserving way of conducting identity verification. Using the [groth16](https://eprint.iacr.org/2016/260.pdf) proving scheme opens up the ability to port valid adhaar card proof holders data onchain.

We developed an [example webapp](https://anon-adhaar.vercel.app/) which allows any adhaar card holder to generate a proof of a valid adhaar card. We are [open sourcing it](https://github.com/dmpierre/anon-adhaar) today for anyone to use, fork or build on top of it. If you are interested to develop apps using what we have built or to implement a similar setup for other identity schemes, don’t hesitate to get in touch.

# Zero-knowledge setup

For verifying the adhaar’s card validity, the circuit setup is straightforward. We wish to check that the signature provided by the user corresponds to one of a valid adhaar card. Our definition of validity will require that the provided message corresponds to an input signature and public key. We consider checking that a public key corresponds to a particular entity as “business logic”. Hence, we will leave such a check to the proof verifying entity - such as a KYC provider backend or a smart contract.

Our circuit will perform two checks:

1. The RSA signature is correct. We raise the signature to the public exponent power, modulus the public key and obtain the provided document hash.
2. The SHA1 padding is correct. We check that the section 9.2 of RFC 8017 is followed when the provided message is raised to the public exponent power, modulus the public key.

Our circuit consists of four inputs:

```auto
signal input sign[nb]; // Signature; private
signal input hashed[hashLen]; // Adhaar card's hash; private
signal public input exp[nb]; // RSA public exponent
signal public input modulus[nb]; // RSA modulus
```

First, we check that the provided RSA signature when raised to the public exponent, corresponds to the input hash. We re-used an implementation found [here](https://github.com/zkp-application/circom-rsa-verify). Then, we ensure that the decrypted message padding, that is the padded hash, is correct. Adobe’s pdf signing process follows the `EMSA-PKCS1-v1_5` rules, detailed in [this RFC](https://www.rfc-editor.org/rfc/rfc8017#page-45). Adhaar cards use SHA1 as the hashing function before signing. Thus, we had to tweak our [reference circuit](https://github.com/zkp-application/circom-rsa-verify), initially wrote for SHA256, to verify the padding’s correctness. We provide a modified version of [this](https://github.com/zkp-application/circom-rsa-verify) circuit.

Although it may introduce limitations, we wish to keep the signature and the document’s hash private. We only divulge what is required for any public validation procedure: the public exponent and the public key. In the case of verifying a proof of a valid Adhaar card, this would make an onchain contract able to require that the signature has been performed using a key emanating from the indian government.

# Applications

Verifiable yet anonymous identity schemes enable interesting constructions.

First, it could provide an interesting avenue to re-think data hungry KYC procedures. Although we are conscious that a proof of a valid adhaar card alone can not constitute a sufficient piece of information for sensitive applications, it can still act as a component of a more complete KYC privacy-respecting process.

Another interesting implication regards verifiable speech. Over the last few months, different protocols and apps, such as [Semaphore](https://semaphore.appliedzkp.org/) or [HeyAnoun](https://www.heyanoun.xyz/) have brought forward the ability of zero-knowledge proof schemes to prove belonging to a group with verifiable properties, while not divulging any users sensitive information. In that vein, proving an Adhaar card’s validity can act as an element of a verifiable yet anonymous voting system. One concrete instance of this could be sybil resistance for quadratic voting in the context of India’s public goods projects.

Finally, using the groth16 proving scheme makes it possible to implement such ideas using a decentralized backend, such as Ethereum. One could imagine a registry contract, storing which addresses have posted valid adhaar cards proofs. This would allow for composability to kick-in, making it possible for the adhaar card pki to be leveraged for DeFi protocols or social apps.

# Future directions and Applications Areas

An important limitation remains the ability to scale our circuit to large inputs. SHA1 remains a non-zk friendly hash, incurring important performance costs. A typical Adhaar pdf card size hovers around 650Kb, a size beyond what today’s circuits are capable of. Still, being able to perform hashing of such a document would reveal interesting, as it would allow to not allow prove a card’s validity but also its content. Folding schemes like [Nova](https://github.com/microsoft/Nova) are prime candidates for exploring such an option.

More generally, proof time remains a bottleneck to a seamless UX. On a 8Gb RAM and 2.3GHz 2017 Macbook Pro, an above-average machine compared to everyday devices used in India, generating a proof entails a 10 minutes wait time. Here also, leveraging a different zero-knowledge proving backend, such as [halo2](https://github.com/zcash/halo2), or scheme, as [Nova](https://github.com/microsoft/Nova), could provide improved performance metrics.

On a Dapp level, if we were to require from users to use their adhaar proof only once, it would imply tying a card to an adress. Such a requirement is not uncommon, decentralized apps often look for sybil resistant mechanisms in order to protect themselves from spam. If we were to link an adhaar card to a single address, a nullifier construction will be required. However, this would entail the ability for an agent having access to a complete adhaar database to detect which individuals have verified their adhaar card on chain, hence breaking anonymity. This may carry risks for users in a context of regulatory uncertainty.

## Replies

**0xVikasRushi** (2023-11-26):

Hey PSE Team,

I’ve been actively exploring the Anon Aadhaar SDK.

Recently, I discovered that Aadhaar QR codes contain a wealth of information such as

[![image](https://ethresear.ch/uploads/default/optimized/2X/0/09d1ece0653c1744917fa941ec6e566e6b904039_2_690x380.jpeg)image916×505 86.7 KB](https://ethresear.ch/uploads/default/09d1ece0653c1744917fa941ec6e566e6b904039)

Some individuals have successfully reverse-engineered and decoded the content from the hash.

I’m currently exploring idea of using zkSNARKs to check facts in the Anon Aadhaar SDK. I want to explore how we can securely and privately verify details like age (above 18) and gender (male or female) using this information.

I would greatly appreciate your guidance.

---

**kesttn** (2023-12-23):

Perhaps this is a good exploration, but identity (or biometric-type) proofs like the Adhaar card carry an official character and have limitations, wouldn’t it be better to seek a way of proof across countries and regions?

---

**qqdee** (2024-01-05):

I think this is the totally centralized way, and if so then why not use all the IDs in the world?

---

**germaai** (2024-01-09):

I understand privacy to mean anonymity and privacy; anonymity is the invisibility of the user’s identity, and privacy is the invisibility of information about the user’s behavior, activities, and other data. The use of adhaar cards as authentication as described in this article, I honestly don’t see how this is any different from kyc, and it’s not exactly decentralized, let alone privacy-protecting good, is it?

---

**shelenee** (2024-01-15):

This is an interesting way of combining existing pki with blockchain technology. But I see that “the signature has been performed using a key emanating from the indian government.” I have a question about this: does this program require the deep involvement of a national government? (Specifically Adhaar is the Indian government), so the problem this program is solving is for the government, right?

---

**turboblitz** (2024-01-22):

This only piggybacks on the already-existing Aadhaar PKI infrastructure. It does not solve any problem for the Indian government, they already stores the personal data of their citizens. But it allows new projects like DeFi protocols or web apps to verify specific informations about users reliably under the trust assumption that the Indian government does not issue fake Aadhaar identity, which is pretty good for most day to day applications.

---

**turboblitz** (2024-01-22):

It’s different from KYC in the sense that you can now prove information about your Aadhaar identity without revealing everything about you. For instance, you could now prove to a social network that you hold a valid Aadhaar and are not a bot.

Without relying on existing PKI used at scale, creating a universal and reliable identity system is hard, as you can see from what Worldcoin is trying to do.

---

**eigmax** (2024-01-23):

the root trust comes from the data issuer, which is a centralized orgazation.


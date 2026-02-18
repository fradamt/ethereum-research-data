---
source: ethresearch
topic_id: 13629
title: Efficient ECDSA signature verification using Circom
author: 0DanielTehrani
date: "2022-09-11"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/efficient-ecdsa-signature-verification-using-circom/13629
views: 7393
likes: 40
posts_count: 10
---

# Efficient ECDSA signature verification using Circom

## Context

An ECDSA signature verification circuit written in Circom results in an R1CS with approximately 1.5 million constraints, a proving key that is close to a GB large, and a proving time [that is non-trivial](https://github.com/0xPARC/circom-ecdsa#benchmarks).

The point of doing an ECDSA signature verification using Circom is to verify that the prover owns a certain address without revealing the address. Although it is easier to check privKey * G == pubKey, most wallets don’t expose the private key of a wallet, therefore we are restricted to checking signatures. **Signature verification without revealing the address has applications in, for example, zero-knowledge proof of membership.** (Which is why we want to have a way to prove ownership of an address anonymously)

In this post, I will decribe a method that could improve the efficiency of ECDSA signature verification written in Circom.

***I focus on implementation using Circom to avoid ambiguity. However, the method is not completely dependent on Circom. You can swap “Circom” with “zkp”, “zk-snark”, or other high-level arithmetic circuit languages.***

## Overview of the method

The essence of the method is, that in order to do as less computations as possible in a circuit, we offload some signature verification calculations from the circuit.

## The method

*This credit for this technique goes to the answerer of [this stack exchange post](https://crypto.stackexchange.com/questions/81089/is-this-a-safe-way-to-prove-the-knowledge-of-an-ecdsa-signature). Although, the method is not formally verified. If this method lacks correctness, soundness, or zero-knowledge-ness, then the entire scheme I describe in this post will not work. That being a possibility, I’m writing this post hoping it to be useful at least in some way,  as a source of ideas.*

Verify an ECDSA signature without revealing the *s* part of the signature leads to reducing the required calculation that needs to be kept private (i.e. needs to be SNARKified)

First, you produce a signature with your private key as usual.

R = k * G

s = k^-1(m + da * r)

The signature = (r, s)

where

- G: The generator point of the curve
- k: The signature nonce
- R: k * G
- Qa: The public key
- m: The message to sign
- r: x-coordinate of R

The signature can be verified by checking the following equality

R = s^{-1} * m * G+ s^{-1}r * Qa

or

s * R = m * G + r * Qa.

This equation can be perceived as s being the private key, R being the generator point, and m * G + r * Qa being the public key.

Now we can prove the knowledge of s without revealing s itself, by generating a signature!

We calculate the signature as follows:

R’ = k’ * R

s’ = k^-1(m’ + s * r')

where

- k’: The signature nonce
- m’: The message to sign
- r’: x-coordinate of R'

We verify the signature (s’, r')  by checking:

- s’ * R’ = m’ * R + r' * Qa’

This equation itself doesn’t reveal Qa (the public key).  So it can be checked publicly, without using Circom.

**We also need to check that Qa’ actually *comes from* Qa.** This can be done by checking:

- Qa’ = m * G + r * Qa

**Since we don’t want to reveal Qa (the public key), this equality check is done using Circom.** Moreover, it is required to keep m a secret. If m is revealed, Qa will be recoverable. That is, in *zero-knowledge proof of membership*, the public keys that are members of a set are publicly known; someone can just check which public key matches Qa’, by filling in m and r .

## Summary and benchmarks

To sum up, the circuit will take Qa and m as the private input, and r’ and Qa’ as the public input. I constructed the outline of the circuit [here](https://github.com/DanTehrani/zk-ecdsa-verify). The circuit is not complete. The purpose of it is to demonstrate the outline.

The benchmarks:

- constraints: \approx 200,000
- proving key size: \approx 134MB
- proving time (witness generation + proving): \approx 15s on a MacBook Pro

Which is a meaningful improvement [from the original circuit](https://github.com/0xPARC/circom-ecdsa#benchmarks).

And that is it.

Feedback will be appreciated.

## Replies

**0DanielTehrani** (2022-09-20):

### Update

*I’m replying to my post because I could not edit my post for some reason.*

The circuit is now complete: [GitHub - DanTehrani/zk-ecdsa](https://github.com/DanTehrani/zk-ecdsa)

I modified the part where we verify Qa’ came from Qa, for the following reason: to do a point scalar multiplication efficiently, we pass the cache of multiplied points to the circuit. If we pass the cache of r * Qa, we will only have the cache of the multiplication, and not the plain public key in our circuit. But we also want to operate with the plain public key in our circuit.

So we rewrite the equation Qa′=m∗G+r∗Qa by multiplying both sides by r^{-1} to get

- r^{-1} * Qa’ - r^{-1} m * G = Qa

And we end up with the circuit that takes r^{-1} * Qa’ and r^{-1}G as the public input and m as the private input.

With that, we can obtain the plain public key in our circuit.

---

**vivboop** (2022-09-28):

I’m Vivek, a researcher at 0xPARC and Personae Labs. One of my main projects is heyanon.xyz, whose core cryptographic primitive is a **ECDSAVerify** inside of a SNARK. Currently this takes a few minutes to compute in specific browsers, so we’re very interested in any methods that can speed up this process!

This is a great find! My intuition is also telling me that this scheme is secure, as the only part of the original ECDSA signature computation trace that’s revealed publicly is R, which is just k * G and unrelated to the original user’s private key. I will attempt to write a full security analysis for this over the next few days so we can be even more confident that this can be deployed, dm me on Twitter ([twitter.com/viv_boop](http://twitter.com/viv_boop)) if you or anyone else is interested in collaborating on this!

One thing is we need to have a private, random, and unique m generated for the initial signature, and I’m wondering how that must be implemented so it is secure when deployed. I know for ECDSA, k must also be random and the deterministic version is generated based on some HMAC involving the original message m and the user’s private key d_a (details [here](https://datatracker.ietf.org/doc/html/rfc6979#section-3.2)). So perhaps we need to follow a similar technique for m for full security?

And looking through the code, one observation is that computing r^-1 * m * G inside the circuit can be made a bit more efficient without sacrificing any security. If you just pass in r^{-1} * m as an input into the circuit, you can use the original **PrivToPub** code from circom-ecdsa that stores precomputed multiples of G instead of passing in precomputed multiples of r^-1 * G and multiplying by m. This should decrease the input size a bunch and hopefully save constraints!

---

**0DanielTehrani** (2022-09-29):

[@vivboop](/u/vivboop)

Thanks for your thorough response Vivek!

As you mentioned, m the first message to be singed, should be generated in the same manner as k.

And passing in r^{−1} ∗ m instead of just m will be better, since

- the circuit will be simpler
- the circuit will require less public inputs leading to a reduction in the number of constraints
- we don’t need to calculate the multiplication cache of r^{-1} * R every time which takes several seconds

I updated the code and the number of constraints (including the pub key → eth address conversion)  is now reduced to 401319 from the initial 466599!

Great improvements!

And thanks for your work on full security analysis! Let’s keep in touch!

---

**0DanielTehrani** (2022-10-04):

Vivek and I have been discussing the security of this scheme, and Vivek pointed out the scheme is insufficient to prove the knowledge of the *private key*. It proves the knowledge of a *single signature*, but that means that an adversary can use any signature that exists in the wild (e.g. Ethereum transaction), and supply that as an input.

This is because m (the initial message that gets signed) can be anything.

So we propose a modification to the initial scheme.

We restrict m to be a hash of some value. That is, for example : m = poseidon(salt, appId)

And check that salt and appId will hash to m inside the zkSNARK.

- salt will be a random value, supplied as a private input to the zkSNARK.
- It is infeasible to come up with a salt that hashes to some pre-determined m.
- appId is there to prevent replay attacks.

And with that,  for now, we will keep working on proving security!

---

**vivboop** (2022-10-05):

I implemented the above change to the circuits at [VerifyPubkey2 circuit added by vb7401 · Pull Request #4 · DanTehrani/zk-ecdsa · GitHub](https://github.com/DanTehrani/zk-ecdsa/pull/4), which led to a bug being discovered. The above construction assumes the signed message m will be exactly poseidon(salt, appId), which we can check efficiently in a circuit. However, Ethereum wallets won’t let us only sign poseidon(salt, appId) – they follow EIP-712 standards, which involves prepending a fixed prefix to your intended message and then keccak256 hashing the resulting string before signing. Unfortunately keccak256 is very SNARK-unfriendly, so verifying this process inside the SNARK is very costly. Similar code was written for ETHdos, a project I helped build: [circom-pairing/utils.circom at f857520e5326126b4ff94c341ab0e9c6972dd38c · nalinbhardwaj/circom-pairing · GitHub](https://github.com/nalinbhardwaj/circom-pairing/blob/f857520e5326126b4ff94c341ab0e9c6972dd38c/circuits/ethdos/utils.circom). Any workarounds for this?

Even if we can’t fix this, all hope isn’t lost. One observation from this method is that revealing r and R from the original signature shouldn’t break security, as they are derived from k * G and not da directly. So I realized rewriting the initial ECDSA verification can lead to some terms being computed out of the SNARK and thus save some proving time:

\begin{align}
s * R &= m * G + r * Qa \\
s*R - m * G &= r * Qa \\
s r^{-1} * R - m r^{-1} * G &= Qa
\end{align}

The m r^{-1} * G term can be computed completely outside of the SNARK, as well as the r^{-1} * R term, leading to only one SecpMultiply and SecpAdd. And as Dan initially implemented, we can input precomputed multiples of r^{-1} * R to speed up SecpMultiply. And then to ensure full correctness, we can verify those multiples were computed correctly in a separate SNARK.

---

**vivboop** (2022-11-22):

I realized we haven’t posted any updates in this thread on the implementation or the security proof!

We’ve implemented the above scheme at [GitHub - personaelabs/efficient-zk-ecdsa: Lowering client-side proving cost for private ZK signatures](https://github.com/personaelabs/efficient-zk-ecdsa), including circom benchmarks for browser and CLI proving times. We use a large set of precomputed multiples of r^{-1} * R (referred to as T in the code) which brings constraint count down majorly for off-chain verification. This unfortunately means on-chain proving is inefficient as we need to send these multiples as public inputs and also verify the multiples were correctly computed. We can make this verification cheaper by a combination of

1. precomputing less multiples
2. outputting the hash of the precomputes in the original circuit, then have a second circuit compute the multiples and also output a hash, then have the smart contract verify the two outputted hashes are equal

There’s a big design space depending on your application, and we’d love some PRs implementing versions of the circuits with different proving/verifying tradeoffs! We also have a WIP halo2 implementation of this logic using the [halo2wrong](https://github.com/privacy-scaling-explorations/halo2wrong) and [zkevm Keccak circuits](https://github.com/privacy-scaling-explorations/zkevm-circuits/tree/main/zkevm-circuits/src/keccak_circuit) from PSE, hoping to get some browser/CLI benchmarks on that soon.

We also worked with Kobi and Nico from [Geometry Research](https://geometryresearch.xyz/) to get a formal proof of security for this scheme, which technically is a “ZK PoK of a signature on a specific message”. This involves proving correctness, knowledge soundness, and ZK, which Nico laid out in this [HackMD](https://hackmd.io/HQZxucnhSGKT_VfNwB6wOw?view). Please give it a read and reach out if you find any mistakes!

---

**weijiguo** (2022-11-29):

Thanks a lot for the great works [@vivboop](/u/vivboop) and [@0DanielTehrani](/u/0danieltehrani) ! Any updates to the constraints size? The readme file still says: ecdsa_verify_pubkey_to_addr 	466,599

---

**0DanielTehrani** (2022-11-30):

Hi [@weijiguo](/u/weijiguo)

Happy to hear your interest in this work.

There was a trivial bug in the circuit which unnecessarily resulted in additional 151k constraints, which we [fixed](https://github.com/personaelabs/efficient-zk-ecdsa/commit/87c4ce42691f1b36b46f8523f4f6b6ba84a8c63a) recently.



      [github.com](https://github.com/personaelabs/efficient-zk-ecdsa)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/6/3/638962ba0d2f3ba88fcc9184dccacd41e0e87fda_2_690x344.png)



###



Lowering client-side proving cost for private ZK signatures in circom










So the correct number of constraints for ecdsa_verify_pubkey_to_addr is 315,175.

(Note that the internet speed we used for the benchmark changed as well.)

Also, we are working on implementing this method in other proving systems and applying further optimizations, to further ease proving.

We hope to post updates again soon.

---

**themighty1** (2024-12-13):

Hi, interesting project. We would like to use a simplified ECDSA sig verification approach for TLSNotary.

Did you manage to coma up with a formal proof for this approach?


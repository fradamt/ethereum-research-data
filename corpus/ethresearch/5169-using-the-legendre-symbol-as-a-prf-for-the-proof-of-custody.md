---
source: ethresearch
topic_id: 5169
title: Using the Legendre symbol as a PRF for the Proof of Custody
author: dankrad
date: "2019-03-17"
category: Sharding
tags: []
url: https://ethresear.ch/t/using-the-legendre-symbol-as-a-prf-for-the-proof-of-custody/5169
views: 6073
likes: 7
posts_count: 5
---

# Using the Legendre symbol as a PRF for the Proof of Custody

**TL;DR**: Thanks to [@JustinDrake](/u/justindrake)’s construction in [Bitwise XOR custody scheme - #2 by vbuterin](https://ethresear.ch/t/bitwise-xor-custody-scheme/5139/2), we can replace the “mix” function in the Proof of Custody scheme (currently SHA256) with any PRF that produces as little as only one bit of output. The Legendre PRF does exactly that, and is efficient to compute both directly and in a direct and MPC setting, making it the ideal candidate.

**Background**: Proof of Custody is a scheme for validators to “prove” that they have actually seen the block data for a crosslink they are signing on. In order to do this, they commit to a single bit upon signing an attestation. If this bit is incorrect, they can be challenged using the Proof of Custody game (previous design here: [Proof of custody game design · Issue #568 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/eth2.0-specs/issues/568), for a much improved version that only needs one round in most cases see Justin’s post [Bitwise XOR custody scheme - #2 by vbuterin](https://ethresear.ch/t/bitwise-xor-custody-scheme/5139/2))

One open problem is to find a better candidate for the “mix” function. It is currently based on a SHA256 hash, however, SHA256 is very complex to compute in a secure Multi-Party Computation (MPC). One of the design goals of Ethereum 2.0 is, however, to make the spec MPC-friendly, so that it is easy for (a) validator pools to be set up in a secure, trustless manner and (b) allow one-party validators to spread their secret across several machines, reducing the risk of secrets getting compromised.

To replace the “mix” function, we are looking for

> An MPC-friendly pseudo-random function (PRF, Cryptography - Pseudo-Random Functions) F_K(X) (F: \{0,1\}^n \times \{0,1\}^s \rightarrow \{0,1\}^m), where
>
>
>
>
> K should be shared among several parties, and none of the parties should be able to infer K
>
>
>
>
> n can be any value, but larger input sizes that preserve the pseudo-randomness would be preferred (The function needs to be run on a total input of ca. 2-500 MBytes, which can be split into chunks of n bits, and run in ca. 1s)
>
>
>
>
> s (length of K) is 96*8 = 768
>
>
>
>
> m is arbitrary and can be as little as 1 bit

# Legendre PRF

The Legendre symbol \left(\frac{a}{p}\right)  is defined as

- -1 if a is not a quadratic residue \pmod p
- 1 if a is a quadratic residue \pmod p except if
- a \cong 0 \pmod p then it is defined as 0.

The Legendre symbol can be explicitly computed using the formula

\displaystyle \left(\frac{a}{p}\right) = a ^ \frac{p-1}{2} \pmod p

The Legendre PRF was suggested by Damgård [1] and is defined by taking a=K+X, where K is the secret and X the PRF input. While the range of this function is \{-1,0,1\}, the output 0 only happens if K+X \cong 0 \pmod  p, so effectively we can consider the Legendre PRF to produce one bit of output per given input (which can be as large as the prime p chosen; in our case, it would be natural to choose a prime p of similar size to a signature, which would be 768 bits, effectively covering 768 bits of input in every round).

# Complexity

## Direct (cleartext) computation

Computing the Legendre symbol is not a major concern in terms of computational complexity – according to [2], table 3, the Legendre PRF was able to process ca. 285 MByte/s input data using a width of 256 bits (4 cores i7-3770 3.1 GHz). This is about half the performance of SHA256 (cf [Non-specialized hardware comparison - Bitcoin Wiki](https://en.bitcoin.it/wiki/Non-specialized_hardware_comparison#Intel)).

## MPC-friendlyness

The hard part of MPCs are multiplications, which require communication. The Legendre PRF performs exceptionally well, requiring only two multiplications to evaluate privately (with the output shared among participants) [2].

In comparison, SHA256 is very hard to compute inside an MPC, as it requires tens of thousands of multiplication (see [3] for a benchmark using 29000 AND gates). So the Legendre PRF would be a huge performance improvement.

# Cryptographic assumption

The original assumption by Damgård [1] is that consecutive outputs of the function (i.e., X, X+1, X+2, …) cannot lead to prediction of the next output or the secret K in a computationally efficient way. (The “Shifted Legendre” problem).

While most cryptographic “computational hardness” assumptions (e.g. RSA problem, Discrete logs, …) cannot be proven, they have been tested by years of research in the cryptographic community. Unfortunately, not as much research is available for the Shifted Legendre assumption and it has to be treated somewhat carefully.

However, I argue that using a careful design, we actually do not have to rely on this assumption:

1. In the direct computation, it is actually irrelevant if the secret K can be inferred and/or if further values of the Legendre PRF can be predicted from any number of outputs, because at the time that the outputs have to be revealed, the secret K  would already have been revealed.
2. When doing it inside an MPC, as long as we are also integrating the XOR of all bits inside the same MPC, the PRF bit will not be known to any MPC participant and only the XOR of all bits will become public. No inference on the secret can be performed on a single output bit. (I am assuming that doing these XORs inside an MPC will not be prohibitively expensive, I would welcome  input from someone who knows more about MPCs on this; I found this resource which claims it’s essentially “free”: multiparty computation - Why XOR and NOT is free in garbled circuit - Cryptography Stack Exchange)

This means for safety, we are not actually relying on any cryptographic assumptions. However, we still want it to be a “good proof of custody” PRF. For this we actually need a somewhat different assumption:

**Proof of Custody assumption**: It is not possible to share a derivative D(K) of the secret K in a way that will allow  (efficient)  computation of \left(\frac{K+X}{p}\right), but derivation of K is impossible (or computationally hard).

Looking at the definition of Legendre, this feels likely true, but it would probably warrant someone with cryptographic training thinking about this. (I actually think it is not trivial to see that the equivalent assumption for SHA256 or AES is true)

# Alternatives

A conservative alternative PRF would be AES, which is a well tested cryptographic standard. It can be implemented using 290 multiplications [2] and so performs a lot worse than Legendre in the MPC setting, but still 100 times better than SHA256. The direct “cleartext” computation of AES is orders of magnitudes faster than both SHA and Legendre, and it may be worth having a look at it in its own right; for example, the “validator shuffling” problem currently effectively uses SHA256 as a PRF ([consensus-specs/specs/core/0_beacon-chain.md at 91a0c1ba5f6c4439345b4476c8a1637140b48f28 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/eth2.0-specs/blob/91a0c1ba5f6c4439345b4476c8a1637140b48f28/specs/core/0_beacon-chain.md#get_permuted_index)), but AES could do this job with much less computational complexity. I wonder if there are more cases where we default to hash functions although a PRF would be enough.

[1] On the randomness of Legendre and Jacobi sequences, Damgård, CRYPTO 88, https://link.springer.com/content/pdf/10.1007%2F0-387-34799-2_13.pdf

[2] https://eprint.iacr.org/2016/542.pdf

[3] http://orbit.dtu.dk/files/128048431/492.pdf

## Replies

**CarlBeek** (2019-03-19):

This is a super cool construction, and I am a big fan of MPC-able mixing functions for PoC. ![:heart_eyes:](https://ethresear.ch/images/emoji/facebook_messenger/heart_eyes.png?v=14)

I would like to raise a few points about it (particularly in the context of MPC):

## Arithmetic Black Box

In the GRRSS16 paper sited, there is a reliance on a \mathcal{F}_{\mathrm{ABB}} (*Arithmetic Black Box*) functionality which needs to provide hiding, shared additive and multiplicative MPC arithmetic as well as the ability to sample random bits as well as random squares from the field. This is where I believe their construction sweeps a significant proportion of the complexity under the metaphorical rug.

### Pre-compute

*Note: The terminology from the paper is adopted. Hence [\cdot] represents a shared-value of the class  \mathcal{F}_{\mathrm{ABB}} with all the associated MPC functionality.*

In order to arrive at an output string [y], the protocol, \prod_{\text { Legendre }}, must calculate 3 *Add* and 3 *Mul*  operations as well as sampling a square [s^2], [k] keys, and a bit [b] at random all of which must be done with \mathcal{F}_{\mathrm{ABB}}. The authors argue that this can be done as a precompute as it does not rely on the input [x] (only 1 *Mul* and 1 *Add* need to be performed in MPC after [x] is known). The remaining arithmetic operations of the 4th step (see Figure below) can be done in private (which is obviously much faster).

*A description of the MPC protocol for reference’s sake.* [GRRSS16]

[![24%20AM](https://ethresear.ch/uploads/default/optimized/2X/6/6628a3c0ad43310f45bdce05c373192bf4002be4_2_345x214.jpeg)24%20AM1824×1132 244 KB](https://ethresear.ch/uploads/default/6628a3c0ad43310f45bdce05c373192bf4002be4)

The reason why this may not be feasible as a precompute in the context of PoC is that participants of an MPC would have to configure \mathcal{F}_{\mathrm{ABB}}  for the precise combination of the participants who are online at the time [x] becomes known. Furthermore, both steps 3 and 4 need to be computed after [x] is known, which means MPC multiplications are required after the value becomes public.

### The Precompute is O(n^2)

The results in the paper account for (non byzantine) performance of the pre-calculations. GRRSS16 makes use of MASCOT [KOS16] which is a highly efficient implementation of Oblivious Transfers (which they indirectly implement using SimpleOT (OT over DDH, but quadratic residuosity or lattices could also be implemented)).

The issue herewith is that the communication complexity of MASCOT (and OTs in general, to the best of my knowledge) is quadratic in the number of participants. The MASCOT paper doesn’t present results for more that 5 participants and assumes 50MBit connections between WAN participants.

### n-1 Secure

Using OTs means that the system is n-1 secure, but this is achieved by halting if a MPC participant is behaving maliciously. This has two, interrelated, consequences:

1. Any participant in the MPC can cause the system to halt and therefore can DoS the calculation. This has large implications for the liveness of the system as the failure of a single participant prevents its completion. (A 2/3 quorum would be preferable.)
2. Staking pools making use of this MPC functionality cannot weight participants differently as everyone who partakes in the MPC has equal weighting. (Allowing an MPC participant to have two instances in the MPC does not give them twice the weight/voting power).

## Redistribution of secrets

One of the upsides of using BLS signatures as the secret that is that t-of-n threshold signatures are easy to implement and the result is shares of the final secret. The issue is these shares would then have to be recalculated in the field over which the Legendre symbols are calculated. Otherwise the secret would have to be reconstructed by interpolating the group signature, mapping that to the field for the Legendre and redistributing the shares. The problem herewith is that at no point should the group signature be interpolated otherwise any single member of the MPC can reveal the secret and get everyone slashed. It is therefore necessary to map from \sigma_i \in \mathcal{G}_{BLS} to \sigma_i^\prime \in \mathbb{F}_p without going via the group signature \sigma \in \mathcal{G}_{BLS}. Maybe such a map exists, but if so I am unaware of it. (I am pretty sure it is not known in general or elliptic curves would be reducible to DDH over much smaller \mathbb{F}_p fields.)

## Conclusion

Legendre symbols are an interesting new PoC idea and are certainly favorable to AES or SHA from an MPC standpoint, however they are not a silver bullet in this regard. In addition, the assumptions underlying its security are largely untested.

## References

[GRRSS16] https://eprint.iacr.org/2016/542.pdf

[KOS16] https://eprint.iacr.org/2016/505.pdf

---

**dankrad** (2019-03-19):

Thanks for the very constructive inputs [@CarlBeek](/u/carlbeek)! Unfortunately my knowledge of MPC is somewhat limited (trying to catch up these days), but I have a few ideas here that might improve the situation:

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/c/df788c/48.png) CarlBeek:

> ### Pre-compute
>
>
>
> Note: The terminology from the paper is adopted. Hence [⋅][\cdot] represents a shared-value of the class FABB\mathcal{F}_{\mathrm{ABB}} with all the associated MPC functionality.
> In order to arrive at an output string [y][y], the protocol, ∏ Legendre \prod_{\text { Legendre }}, must calculate 3 Add and 3 Mul operations as well as sampling a square [s2][s^2], [k][k] keys, and a bit [b][b] at random all of which must be done with FABB\mathcal{F}_{\mathrm{ABB}}. The authors argue that this can be done as a precompute as it does not rely on the input  (only 1 Mul and 1 Add need to be performed in MPC after  is known). The remaining arithmetic operations of the 4th step (see Figure below) can be done in private (which is obviously much faster).

So the good thing is that the key [k] only has to be shared once per “PoC period”, which is 2 weeks according to Issue 568 above, but could be adapted to our needs (caveat here: we might want to shorten this period to guard against the Legendre symbol “leaking” information about k, in case the Shifted Legendre assumption proves unsafe). This still leaves open the question on how shares of k can be created, more on that below.

We do probably need a new [s^2] for every computation, so this will indeed add another multiplication.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/c/df788c/48.png) CarlBeek:

> ## Redistribution of secrets
>
>
>
> One of the upsides of using BLS signatures as the secret that is that tt-of-nn threshold signatures are easy to implement and the result is shares of the final secret. The issue is these shares would then have to be recalculated in the field over which the Legendre symbols are calculated. Otherwise the secret would have to be reconstructed by interpolating the group signature, mapping that to the field for the Legendre and redistributing the shares. The problem herewith is that at no point should the group signature be interpolated otherwise any single member of the MPC can reveal the secret and get everyone slashed. It is therefore necessary to map from σi∈GBLS\sigma_i \in \mathcal{G}_{BLS} to σ′i∈Fp\sigma_i^\prime \in \mathbb{F}p without going via the group signature σ∈GBLS\sigma \in \mathcal{G}{BLS}. Maybe such a map exists, but if so I am unaware of it. (I am pretty sure it is not known in general or elliptic curves would be reducible to DDH over much smaller Fp\mathbb{F}_p fields.)

Yes, this is something I had not properly considered in my post. This is indeed a hard problem, and I can currently see two ways out:

- If we do want to keep rk[p] = BLS_sign(key=validator_privkey, msg=p), then one way to do this is to do the entire BLS multisig inside an MPC, compute an \mathbb{F}_p element and share it.
- Another approach might be to make the choice of rk[p] up to the validator. The disadvantage is that we need a way to commit to the round secret to allow for early reveal slashing, which is a complication of the spec.

---

**dankrad** (2019-03-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Another approach might be to make the choice of rk[p] up to the validator. The disadvantage is that we need a way to commit to the round secret to allow for early reveal slashing, which is a complication of the spec.

So it turns out this is possible but we would need commitment  to the chosen secret from the validators, which is a complication of the spec. Preference would be that  no such mechanism is needed

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> If we do want to keep rk[p] = BLS_sign(key=validator_privkey, msg=p) , then one way to do this is to do the entire BLS multisig inside an MPC, compute an Fp\mathbb{F}_p element and share it.

I had a few thoughts about this one, and I now believe that this is not too difficult, if we define that `rk[p] = the x-coordinate of BLS_sign(key=validator_privkey, msg=p)`, i.e. instead of taking the signature itself, we take the projection on one of its \mathbb{F}_p coordinates.

Assuming that the MPC participants have \mathbb{F}_p shares of the secret s, then the only thing that has to be done inside an MPC is an EC multiplication, which is a fairly small number of multiplications inside  \mathbb{F}_p (the two multiplicative inverses that have to be computed can be turned into a couple more multiplications using this trick: [multiparty computation - computing INV in boolean circuit for MPC - Cryptography Stack Exchange](https://crypto.stackexchange.com/questions/62006/computing-inv-in-boolean-circuit-for-mpc))

I noticed an interesting property when combining the Legendre PRF with https://ethresear.ch/t/bitwise-xor-custody-scheme/5139/2: It actually turns out that because the Legendre symbol is a multiplicative function, i.e.

\displaystyle \left(\frac{a\cdot b}{p} \right)= \left(\frac{a}{p} \right) \cdot \left(\frac{b}{p} \right)

the computation of the proof of custody bit can actually be achieved by doing a single Legendre symbol evaluation of

\displaystyle \left(\frac{(K+X_1)\cdot (K+X_2)\cdot \ldots \cdot(K+X_n)}{p} \right)

where X_i are the data blocks represented in \mathbb{F}_p. If multiplications in \mathbb{F}_p are cheaper than Legendre symbol evaluations, then this is potentially a nice optimisation (but probably not true for large p, as evaluating Legendre using quadratic reciprocity is probably quite cheap)

In the context of MPCs, this gives us another interesting way of computing  the Legendre-based PoC: Since the above representation is a polynomial in K, it suffices if the MPC participants pre-compute shares of K, K^2, \ldots, K^n. Then each evaluation of the PoC can be done by locally (!) computing the value of this polynomial in K (since they are only multiplications by constants, no communication is needed), and then performing one single Legendre symbol evaluation at the end. Since the pre-compute can be used for one custody period, this could be much a much more efficient way to compute the PoC bit.

---

**burdges** (2023-03-13):

Anyone who happens upon Legendre PRF should check out:

https://eprint.iacr.org/2019/1357


---
source: ethresearch
topic_id: 10748
title: Security of BLS batch verification
author: veorq
date: "2021-09-15"
category: Cryptography
tags: []
url: https://ethresear.ch/t/security-of-bls-batch-verification/10748
views: 6341
likes: 18
posts_count: 10
---

# Security of BLS batch verification

# Security of BLS batch verification

*By [JP Aumasson](https://twitter.com/veorq) (Taurus), [Quan Thoi Minh Nguyen](https://twitter.com/cryptosubtlety), and [Antonio Sanso](https://twitter.com/asanso) (Ethereum Foundation)*

*Thanks to Vitalik Buterin for his feedback.*

[![batch](https://ethresear.ch/uploads/default/optimized/2X/0/0a7eecbe5ee30052db925d0bbddf1aa0b800fab7_2_690x439.jpeg)batch886×564 101 KB](https://ethresear.ch/uploads/default/0a7eecbe5ee30052db925d0bbddf1aa0b800fab7)

In a 2019 post Vitalik Buterin introduced [Fast verification of multiple BLS signatures](https://ethresear.ch/t/fast-verification-of-multiple-bls-signatures/5407). Quoting his own words this is

> a purely client-side optimization that can voluntarily be done by clients verifying blocks that contain multiple signatures

The original post includes some preliminary security analysis, but in this post we’d like to formalize it a bit and address some specific risks in the case of:

- Bad randomness
- Missing subgroup checking

We described several attacks that work in those cases, and provide [proof-of-concept implementations](https://github.com/cryptosubtlety/crypto_attack_demo) using the Python reference code.

## The batch verification construction

This technique works as follows, given n aggregate signatures S_i, respective public keys P_i, each over a number m_i of messages (note that each aggregate signature may cover a distinct number of messages, that is, we can have m_i\neq m_j for i\neq j):

e(S_i, P) = \prod_{j=1}^{m_i} e(P_{i,j}, M_{i,j}), i=1,\dots,n

The naive method thus consists in checking these n equalities, which involves n+\sum_{i=1}^n m_i pairings, the most calculation-heavy operation.

To reduce the number of pairings in the verification, one can further aggregate signatures, as follows: the verifier generates n random scalars r_i \geq 1, and aggregates the signatures into a single one:

S^\star = r_1S_1 + \cdots r_n S_n

the verifier also “updates” the signed messages (as their hashes to the curve) to integrate the coefficient of their batch, defining

M_{i,j}'=r_i M_{i,j}, i=1,\dots,n, j=1,\dots,m_i

Verification can then be done by checking

e(S^\star,G)=\prod_{i=1}^n \prod_{j=1}^{m_i} e(P_{i,j},M_{i,j}')

Verification thus saves n-1 pairing operations, but adds n+\sum_{i=1}^n m_i scalar multiplications. Note that if the verification fails, then the verifier can’t tell which (aggregate) signatures are invalid.

In particular, if m_i=1, \forall i, then verification requires n+1 pairings and 2n multiplications, instead of 2n pairings. Depending on the relative cost of pairings vs. scalar multiplications, the speed-up may vary (see [this post](https://hackmd.io/@zkteam/eccbench) for pairings implementations benchmarks)

## Security goals

Informally, the batch verification should succeed *if and only if* all signatures would be individually successfully verified. One or more (possibly all) of the signers may be maliciously colluding. Note that this general definition implicitly covers cases where

- Attackers manipulate public keys (without necessarily knowing the private key),
- Malicious signers pick their signature/messages tuples depending on honest signers’ input.

For a formal study of batch verification security, we refer to the 2011 paper of [Camenisch, Hohenberger,  Østergaard Pedersen](https://link.springer.com/content/pdf/10.1007%2F978-3-540-72540-4_14.pdf).

Note that in the Ethereum context, attackers have much less freedom than this attack model allows, but we nonetheless want security against strong attackers to prevent any unsafe overlooked scenario.

## The importance of randomness

The randomness has been already discussed in the [original post](https://ethresear.ch/t/fast-verification-of-multiple-bls-signatures/5407). Buterin points out that if coefficients are constant, then an attacker could validate invalid signature:

> the randomizing factors are necessary: otherwise, an attacker could make a bad block where if the correct signatures are C_1 and C_2, the attacker sets the signatures to C_1+D and C_2-D for some deviation D. A full signature check would interpret this as an invalid block, but a partial check would not.

This observation generalizes to predictable coefficients, and more specifically to the case where \alpha attackers collude and any subset of \beta\leq \alpha coefficients are predictable among those assigned to attackers’ input.

Note that the coefficient can’t be deterministically derived from the batch to verify, for this would make coefficients predictable to an attacker.

Buterin further discusses the possible ranges of r_i to keep the scheme safe:

> We can also set other r_i values in a smaller range, eg. 1…2^{64} , keeping the cost of attacking the scheme extremely high (as the ri values are secret, there’s no computational way for the attacker to try all possibilities and see which one works); this would reduce the cost of multiplications by ~4x.

### A simple attack

If coefficients are somehow predictable, then the above trivial attack can be generalized to picking as signatures S_1=(C_1+D_1) and S_2=(C_2+D_2) such that r_1 D_1=-r_2 D_2.

If coefficients are uniformly random b-bit *signed* values, then there is a chance 1/2^{b-1} that two random coefficients satisfy this equality (1 bit being dedicated to the sign encoding), and thus that verification passes. Otherwise, the chance that r_1 D_1=-r_2 D_2 for random coefficients is approximately 2^{-n}, with n *the size of  the subgroup* in which lie D_1 and D_2.

However, the latter attack, independent of the randomness size, will fail if signatures are checked to fall in the highest-order subgroup (see the section **The importance of subgroup checks**).

### Signature manipulation

In practice, BLS signatures are not purely used as signatures, but implementers take advantage of other informal and implicit security properties such as uniqueness and “commitment”. That is, if the private key is fixed, given a message not controlled by the signer, the signer can’t manipulate the signature. In the case of bad randomness, such use cases may be insecure.

For instance, let’s say there is a lottery based on the current time interval, i.e., at time interval t outside of signers’ control if S_i = \mathsf{Sign}(sk_i, t), (S_i)_x \mod N = 0 (where N is just some small number, e.g., the number of signers) then the signer i wins the lottery. The first two signers can collude to win the lottery as follows. The first signer chooses a random point P \in G_1 and offline bruteforces a k such that (S_1’)_x \mod N = (S_1 - kP)_x \mod N = 0  where S_1 = \mathsf{Sign}(sk_1, t). The second signer computes S_2’ = S_2 + (k r_1/r_2)P where S_2 = \mathsf{Sign}(sk_2, t). We have

r_1S_1' + r_2S_2' + r_3S_3 = r_1(S_1 - kP) + r_2(S_2 + kr_1/r_2P) + r_3S_3

that is, calculating further:

r_1S_1 - r_1kP + r_2S_2 + kr_1P + r_3S_3
= r_1S_1 + r_2S_2 + r_3S_3

What it means is that the first and second signer can manipulate the signatures so that the first signer wins the lottery while making batch verification valid.

## The importance of subgroup checks

The current state-of-the-art pairing curves such [BLS12-381](https://electriccoin.co/blog/new-snark-curve/) are not prime-order, for this reason the [BLS signatures IRTF document](https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-bls-signature-04) warns about it and mandates a `subgroup_check(P)` while performing some operations. For batch verification, subgroup check is essential, as [previously commented](https://ethresear.ch/t/fast-verification-of-multiple-bls-signatures/5407/5).

The lack of subgroup validation appears to have a greater impact with batch verification than with standard BLS validation, where points in small subgroup are not known to trivially be exploitable, as noted in the [BLS signatures IRTF document](https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-bls-signature-04):

> For most pairing-friendly elliptic curves used in practice, the pairing operation e (Section 1.3) is undefined when its input points are not in the prime-order subgroups of E_1 and E_2.  The resulting behavior is unpredictable, and may enable forgeries.

and in the recent [Michael Scott’s paper](https://eprint.iacr.org/2021/1130.pdf):

> The provided element is not of the correct order and the impact of, for example, inputting a supposed \mathbb{G}_2 point of the wrong order into a pairing may not yet be fully understood.

The difficulty of performing an actual attack is also due the fact that \mathsf{gcd}(h_1,h_2)=1 where h_1 and h_2 are the respective cofactors of E_1 and E_2. Hence pushing the two pairing’s input to lie in the same subgroup is not possible. Let’s see an example based on [BLS12-381](https://electriccoin.co/blog/new-snark-curve/), where

h_1=3 \times 11^2 \times 10177^2 \times 859267^2 \times 52437899^2

and

h_2=13^2 \times 23^2 \times 2713 \times 11953 \times 262069 \times p_{136}.

Choosing an invalid signature S_1 of order 13 and a public key P_{1,1} of order 3, a potential attack would succeed (to pass batch verification) with probability 1/39=1/3 \times 1/13. The attack assumes an implementation that multiplies the public keys by r_i's rather than the messages (in order to gain speed when there a distinct messages signed by a same key) [as described here](https://ethresear.ch/t/fast-verification-of-multiple-bls-signatures/5407/7) and implemented for example by [Milagro](https://github.com/sigp/milagro_bls/blob/16655aa033175a90c10ef02aa144e2835de23aec/src/aggregates.rs#L301).

An attack then works as follows in order to validate a batch of signatures that includes a signature that would not have passed verification:

- Pick S_1 of order 13, and P_{1,1} of order 3. The chance that r_1 S_1 = r_1 P_{1,1} = \mathcal{O} is 1/39, which is the attack success rate. In such case, we have:
- S^\star = r_2S_2 + \cdots r_n S_n.
- Suppose, without loss of generality, that m_1=1 (namely the first batch to verify is a single signature). That is, P'_{1,1} = r_1P_{1,1} = \mathcal{O}.
- The right part of the verification equation becomes \prod_{i=1}^n \prod_{j=1}^{m_i} e(P_{i,j},M_{i,j}') that is, e(P'_{1,1},M_{1,1})\prod_{j=2}^{m_i} e(P'_{i,j},M_{i,j})=1 \times \prod_{j=2}^{m_i} e(P'_{i,j},M_{i,j}).

It follows that verification will pass when all other signatures are valid, even if P_1's signature S_1 is not valid.

Note that the Ethereum clients (Lighthouse, Lodestar, Nimbus, Prysm, Teku) will already have performed subgroup validation upon deserialization preventing such an attack.

## Implementations cheat sheet

Secure implementations of batch BLS verification must ensure that:

- Group elements (signatures, public keys, message hashes) do not represent the point to infinity and belong to their respective assigned group (BLS12-381’s \mathbb{G}_1 or \mathbb{G}_2).
- The r_i coefficients are chosen of the right size, using a cryptographically random generator, without side channel leakage.
- The r_i coefficients are non-zero, using constant-time comparison, and if zero reject it and generate a new random value (if zero is hit multiple times, verification should abort, for something must be wrong with the PRNG).
- The number of signatures matches the number of public keys and of message tuples.

Additionally, implementations may prevent DoS by bounding the number of messages signed.

## Replies

**alinush** (2022-08-28):

It sounds like you are recommending using only 128-bit scalars for the randomness, as opposed to (roughly) 256-bit scalars (i.e., picked uniformly in the entire scalar field)? This should help performance.

---

**matthewkeil** (2024-09-27):

As a note, many eth2 clients are using 64-bit scalars as suggested by [@vbuterin](/u/vbuterin) [here](https://ethresear.ch/t/fast-verification-of-multiple-bls-signatures/5407/6). I had a discussion with [@asn](/u/asn) a while back and more recently with Kev Aundray and they both mentioned the same 128 bit like you [@alinush](/u/alinush).  My goal with this is to verify that value formally because we (Lodestar) and the Lighthouse team use Vitalik’s suggested 64-bit scalars.  In Vitalik we all trust so sure that number is correct but thought it prudent to just revisit.  Pinging [@AgeManning](/u/agemanning) and [@dapplion](/u/dapplion) for visibility.

---

**alinush** (2024-09-27):

\kappa-bits will give you 2^{-\kappa} probability of accepting an invalid batch of signatures.

What k you use is an application-dependent choice. Like [@vbuterin](/u/vbuterin) said [in the article you cited](https://ethresear.ch/t/fast-verification-of-multiple-bls-signatures/5407/6), \kappa=64 may be enough in applications where the attacker doesn’t get too many attempts.

Clearly, after \approx 2^{64} attempts, an attacker will succeed. So applications where signatures are flying left & right should likely not use such a low \kappa.

My sense is a **conservative** one. *Use \ge 128-bit security*! Always. \kappa=128. Why? It might make up for problems that are hard to foresee, whether introduced by you or not. (e.g., what if your RNG has less entropy than you believed, and those 64-bit “uniform” scalars are not that uniform after all).

**PS**: Hard to tell whether the *“In Vitalik we all trust so sure that number is correct”* is a tongue-in-cheek comment. Still, all hats being off to Vitalik, it would be preferable for folks to also do their own analysis of what makes sense in their application setting. (This, of course, can be difficult.)

---

**matthewkeil** (2024-09-27):

Thanks!!  Great explanation.  I def put a lot of faith in Vitalik and it was absolutely serious.  But you are correct, I’m a punny guy… and in all seriousness, they say that if you hear the same thing from more than one source there might be some truth to it.  Well after a couple people mentioned that 64 might be two low I figured it was worth bringing the discussion up again knowing that number is in production based on the post mentioned.  I would like to get confirmation from some others as well but I will look at implementing 128 to see what effect it has on performance to add context for the discussion.  I’ve also pinged some of the pertinent decision-makers on this thread and we can see where things land as a group.  Thanks again for the quick response [@alinush](/u/alinush) !!!  You rock thoroughly!

---

**b-wagn** (2024-09-27):

Let me add to that.

There are in general two ways of deriving the random coefficients for batch verification in various contexts. In the following, I will assume you use \kappa-bit coefficients.

**Option A.** You sample them randomly when you verify, as described in this post. In this case, as alinush says, you get a soundness error of 1/2^{\kappa} (per signature!).

**Option B.** You derive the coefficients via a random oracle (in practice, a secure hash function prefixed with some domain separator). Importantly, you would input *everything* the adversary can control into the hash. In this case, if you assume the adversary can make Q hash evaluations (Q queries of the random oracle), the soundness error would be larger, namely, Q/2^{\kappa}.

This option is used for example in PeerDAS. The advantage is that verification is deterministic.

I don’t know whether some eth clients use Option B, but if so, then 64 bit is certainly a bad choice.

In any case, I would recommend 128 bit, similar to what [@alinush](/u/alinush) said.

---

**mratsim** (2024-10-08):

> Clearly, after ≈2⁶⁴ attempts, an attacker will succeed. So applications where signatures are flying left & right should likely not use such a low κ.

Attackers have a max window of 12 seconds to make those 2⁶⁴ attempts, and ~4 seconds in practice for their attestations to be included. It is not practical to make 2⁶⁴ attempts signature forgery attempts within 4 seconds over the network. That’s 2.56 x 10¹⁶ attempts per second. Assuming a 5GHz CPU can do 1 attempt per cycle, that’s only 5 x 10⁹, so you would need 10⁷ cores for this.

In reality, networking is way way slower, 10000x slower (latency numbers every dev should know [Latency Numbers Every Programmer Should Know · GitHub](https://gist.github.com/jboner/2841832)). And this assumes no hop between your 10⁷ cores and the victim.

Furthermore, the random 64-bit coefficients are resampled at each batch verification attempts, so unless the verifier doesn’t use a cryptographic RNG, the attacker has no way to adjust the scaling factors to the verifier.

Lastly every single node that listen to the attestation channel need to be fooled, a single wrong signature will blacklist you from the peer pool.

So for all intent and purpose, you only get one shot to fool a single peer that somehow leaked their RNG or blinding factors, and in this one shot you will in the process be blacklisted by all the other peers that seeded their blinding factors differently.

---

**chfast** (2024-10-15):

So for the BLS batch verification to work we need to do subgroup checks on all inputs. Can we also construct a similar probability based scheme to do subgroup checks of multiple inputs at once?

---

**matthewkeil** (2024-10-17):

Looking at performance I’m a bit surprised.  There was very very little difference using supranational’s blst library.  64 and 128 bit runs were conducted identically with exception of the bits of randomness.  Creating the randomness is included in the times.

`aggregateWithRandomness` uses MSM to aggregate an array of pk’s and sig’s with blinding and results in a single aggregated pk and sig.

Those are in preparation for `verifyMultipleAggregateSignaturesSameMessage`.  That same method is used in this test but there is also the inclusion of the single verification of a common message using `verify`.

`verifyMultipleAggregateSignatures` is a wrapper around `mul_n_aggregate`.

In all tests a “set” denotes a message/public key/signature group.

```sh
                                                           64 bits           128 bits
                                                        =============     ==============
aggregateWithRandomness
  ✓ aggregateWithRandomness - 1 sets                    152.9080 us/op    232.0550 us/op
  ✓ aggregateWithRandomness - 16 sets                     1.4847 ms/op      1.7781 ms/op
  ✓ aggregateWithRandomness - 128 sets                    7.9076 ms/op      7.9060 ms/op
  ✓ aggregateWithRandomness - 256 sets                   15.3735 ms/op     16.0832 ms/op
  ✓ aggregateWithRandomness - 512 sets                   30.4996 ms/op     30.7407 ms/op
  ✓ aggregateWithRandomness - 1024 sets                  62.6190 ms/op     64.8119 ms/op
  ✓ aggregateWithRandomness - 2048 sets                 125.0660 ms/op    125.5888 ms/op
verifyMultipleAggregateSignaturesSameMessage
  ✓ Same message - 1 sets                               773.3730 us/op    848.0510 us/op
  ✓ Same message - 8 sets                                 1.4562 ms/op      1.6816 ms/op
  ✓ Same message - 32 sets                                2.7797 ms/op      2.9791 ms/op
  ✓ Same message - 128 sets                               8.4415 ms/op      8.8811 ms/op
  ✓ Same message - 256 sets                              16.5267 ms/op     16.7729 ms/op
  ✓ Same message - 512 sets                              32.0515 ms/op     32.1655 ms/op
  ✓ Same message - 1024 sets                             62.7327 ms/op     65.6105 ms/op
  ✓ Same message - 2048 sets                            130.9331 ms/op    129.4787 ms/op
verifyMultipleAggregateSignatures
  ✓ verifyMultipleAggregateSignatures - 1 sets          937.1170 us/op    999.6820 us/op
  ✓ verifyMultipleAggregateSignatures - 8 sets            1.4355 ms/op      1.5259 ms/op
  ✓ verifyMultipleAggregateSignatures - 32 sets           3.7716 ms/op      3.9609 ms/op
  ✓ verifyMultipleAggregateSignatures - 128 sets         12.7219 ms/op     13.3319 ms/op
  ✓ verifyMultipleAggregateSignatures - 256 sets         24.0479 ms/op     25.3813 ms/op
  ✓ verifyMultipleAggregateSignatures - 512 sets         48.4746 ms/op     50.3668 ms/op
  ✓ verifyMultipleAggregateSignatures - 1024 sets        96.7417 ms/op    102.7143 ms/op
  ✓ verifyMultipleAggregateSignatures - 2048 sets       189.2175 ms/op    205.2370 ms/op
```

---

**dpoulami** (2025-01-10):

I have a question regarding the subgroup checks for the public keys and the signatures.

To increase efficiency, one might consider adding the check for just the public keys, and skip the ones for signatures, is this recommendable? IIUC, then the probability of the current attack also becomes negligible.


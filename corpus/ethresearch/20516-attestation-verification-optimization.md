---
source: ethresearch
topic_id: 20516
title: Attestation Verification Optimization
author: matthewkeil
date: "2024-09-28"
category: Cryptography
tags: [security, attestation]
url: https://ethresear.ch/t/attestation-verification-optimization/20516
views: 513
likes: 9
posts_count: 2
---

# Attestation Verification Optimization

# Attestation Verification Optimization

In the ethresearch post [Fast Verification of Multiple BLS Signatures](https://ethresear.ch/t/fast-verification-of-multiple-bls-signatures/5407), Vitalik describes a method for efficiently and securely aggregating multiple **already aggregated** BLS signatures where each aggregated signature can have a different message through randomization.

Randomization, or “blinding,” can be used to protect against [rogue public key attacks](https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-bls-signature#definitions), in which a specially crafted public key (the “rogue” key) is used to forge an aggregated signature. Vitalik suggests 64 bit random numbers be locally generated on the client side for scalar multiplication with each signature during aggregation.  This creates a linear combination style computation of points that upholds the validity of the verification, due to the underlying bi-linear map properties of BLS signatures. The same locally generated random values are scalar multiplied with each of the messages that get aggregated prior to final verification, resulting in equality of pairings.

We note that there is also an expired IETF draft [standard](https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-bls-signature) that is referenced by the BLST [library](https://github.com/supranational/blst), which [suggests](https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-bls-signature#name-proof-of-possession) to use a modified hash-to-curve function to implement proof of ownership as a protection against rogue public key attacks.

## The Tuyen Optimization

The [Lodestar](https://lodestar.chainsafe.io/) team, at [ChainSafe](https://chainsafe.io), wants to use a similar local randomization technique to securely aggregate multiple attestations **over the same message**, and have proposed **The Tuyen Optimization**. Similar to Vitalik’s implementation, 64-bit random numbers are generated client side and scalar multiplied with each signature during signature aggregation, creating a linear combination of points. To uphold equality in the final aggregated verification, each 64-bit random value is scalar multiplied with its corresponding public key (prior to aggregation) instead of the messages as in Vitalik’s post.  This is done to maintain a common message and avoid multiple aggregate verifications which is the heart of the optimization. It was found that aggregation and then single verification can be upwards of 4x faster due to the single pairing computation.

In this report we present a formal proof that the Tuyen Optimization is correct. We also explore the security aspects of applying randomness to the public keys instead of the messages as suggested by Vitalik.

# Aggregation over Common Message

Here we discuss why a direct aggregation of BLS signatures over a common message works, and more importantly the potential vulnerability, for mitigation.  First, we briefly cover some of the properties of bilinear pairings that are useful for proving validity of aggregated BLS signature verification adapted from [Menezes](https://www.math.uwaterloo.ca/~ajmeneze/publications/pairings.pdf).

## Pairings

A pairing, or bilinear map, is a function

e: G_1 \times G_2  \to G_T

between three groups G_1,G_2, and G_T of prime order p, with generators g_1 = \langle G_1 \rangle, g_2 = \langle G_2 \rangle and g_T = \langle G_T \rangle, respectively.

When G_1 = G_2, the pairing is called **symmetric**, otherwise it is called **asymmetric**. In our case the BLS pairing is asymmetric.

A **bilinear pairing** on (G_1, G_2, G_T) is a map:

e : G_1 \times G_2 \to G_T

that satisfies the following conditions:

- Bilinearity: For all u \in G_1, v \in G_2, and a,b \in \mathbb{Z}_p,

e(u^a, v^b) = e(u, v)^{ab}\tag{1}

- Non-degeneracy: e(g_1, g_2) \neq 1_{G_t}. (recall g_1, g_2 are generators of the G_1 and G_2)

## BLS Signatures

For a message m \in \{0,1\}^*, a private key sk \in \mathbb{Z}_p, and a corresponding public key

pk = sk \cdot g \in G_1,\tag{2}

the signature on m is

\sigma = sk \cdot H(m),\tag{3} \in G_2

where H: \{0,1\}^* \rightarrow G_2 is a hash function mapping the message to G_2 and H is generally a [hash to curve function](https://www.ietf.org/archive/id/draft-irtf-cfrg-hash-to-curve-10.html).

*Note: The \cdot operation denotes scalar multiplication.*

### Signature Verification

Given m, pk, and \sigma, the signature is valid if

e(g, \sigma) =  e(pk, H(m))

Where,

e(g, \sigma) \stackrel{3}{=} e(g, sk \cdot H(m)) \stackrel{1}{=} e(g, H(m))^{sk} \stackrel{1}{=} e(sk \cdot g, H(m)) \stackrel{2}{=} e(pk, H(m))

## Naive Aggregation over Common Message

Consider n signatures  \sigma_1, \sigma_2, \dots, \sigma_n \in G_2 corresponding to a common message H(m) \in G_2, private keys sk_1, sk_2, \dots, sk_n \in \mathbb{Z}_p and public keys pk_1, pk_2, \dots, pk_n \in G_1.

Multiple signatures can be combined to only require one verification as follows:

#### Step 1: Aggregate Signature

The aggregated signature \sigma_{agg} is computed as:

\sigma_{agg} = \sum_{i=1}^{n} \sigma_i = \sum_{i=1}^{n} (sk_i \cdot H(m)) = \left(\sum_{i=1}^{n} sk_i\right) \cdot H(m) \tag{4}

#### Step 2: Aggregate Public Key

The corresponding aggregate public key is:

pk_{agg} = \sum_{i=1}^{n} pk_i = \sum_{i=1}^{n} (sk_i \cdot g)= \left( \sum_{i=1}^{n} sk_i\right) \cdot g\tag{5}

#### Step 3: Verification

The verification of the aggregate signature is done by checking:

e(g, \sigma_{agg}) \stackrel{4}{=} e\left(g, \left(\sum_{i=1}^{n} sk_i\right) \cdot H(m) \right)
                                \stackrel{1}{=} e\left(\left( \sum_{i=1}^{n} sk_i\right) \cdot g, H(m) \right)
                   \stackrel{5}{=} e\left(pk_{agg}, H(m)\right)

The above proves that if the equality holds the aggregated signature is valid, implying all signatures that were aggregated are also valid.

# Blinding With Tuyen Optimization

The Lodestar team has proposed the **Tuyen Optimization** for signature aggregation where random values r_i \in \mathbb{Z} are scalar multiplied with the public keys pk_i. This is in contrast to scalar multiplying the random values with the messages H(m_i) as suggested in the [Ethereum Research blog post](https://ethresear.ch/t/fast-verification-of-multiple-bls-signatures/5407). From our research we believe, **The Tuyen Optimization** technique is novel within the Ethereum landscape and among client implementations.  We pose this proof for public review/audit to formalize it validity before expanding its use within the ecosystem. If a more formal audit is deemed necessary that will also be accommodated.

In the following we show that applying blinding to the public key / signature pairs provides valid aggregated verification and adheres to security best-practices.

To verify the blinded, aggregated signature using **The Tuyen Optimization**, the verifier needs to check if

e\left(g, \sum_{i=1}^{n} (r_i \cdot \sigma_i)\right) = e\left(\sum_{i=1}^{n} (r_i \cdot pk_i), H(m) \right)

after applying scalar multiplications with a unique 64-bit random value r_i to each signature \sigma_i and public key pk_i pair (randomness is common to the pair) during aggregation. The proof that equality holds and therefor verification of the aggregate signatures is valid goes as follows:

\begin{aligned}
e\left(g, \sum_{i=1}^{n} (r_i \cdot \sigma_i)\right) &\stackrel{3}{=}  e\left(g, \sum_{i=1}^{n} (r_i sk_i \cdot H(m)) \right) & \\
                                &\stackrel{}{=} e\left(g, \left(\sum_{i=1}^{n} r_i sk_i\right) \cdot H(m) \right) &\\
                                &\stackrel{1}{=} e\left(\left( \sum_{i=1}^{n} r_i sk_i\right) \cdot g, H(m) \right)  &\\
                                &\stackrel{}{=}  e\left(\sum_{i=1}^{n} (r_i sk_i \cdot g), H(m) \right) &
                                &\stackrel{2}{=} e\left(\sum_{i=1}^{n} (r_i \cdot pk_i), H(m)\right)
\end{aligned}

The above proves that if the equality holds, the blinded, aggregated signature is valid.

# Further Considerations

## Eth Research Post

We note that Vitalik’s post has been “community audited” but not formally proven/audited/verified that we can find aside from [here](https://ethresear.ch/t/security-of-bls-batch-verification).  In the comments section of the original comment, there is consideration of aggregating over [public keys](https://ethresear.ch/t/fast-verification-of-multiple-bls-signatures/5407/11) when the message is common. Vitalik mentions that it is well known to aggregate over public keys for common messages. We think they say this assuming over aggregated attestations because the verification of the individual signature pairs has already been done, so there is no chance to introduce a rogue key attack.  In our case that aggregation is happening prior to verification which opens up the attack surface.

## Security

When aggregating signatures in the naive way attackers can craft signature/message pairs that are not legitimate and cancel each other out (add to zero) within the linear combination that is computed during aggregation.  Consequently, invalid signatures can be hidden and pass verification. Applying randomization to “**blind**” every signature in the aggregation is a technique used to help prevent these types of attacks.

There is a published security [proof](https://crypto.stanford.edu/~dabo/pubs/papers/BLSmultisig.html) by Dan Boneh for aggregating securely with public keys. The above report outlines that what is done in the Tuyen Optimzation is commensurate with what is mentioned in the “Batch Verification” section. The paper addresses signing and verification, and could be used to support the security of Tuyen Optimization.  It is in our opinion that the approaches put forth by Dan Boneh are more intricate than is necessary, or required, due to the imbued security considerations of the Ethereum protocol.

Rogue key attacks are also referenced in the BLS IETF [draft](https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-bls-signature-04#section-3) and in the Ethereum Specification where proof-of-possession is considered necessary for mitigation when aggregating signatures. Specifically, the Beacon Node Specifications require that validator signatures be verified prior to being allowed to attest to chain state.  That check is done in [apply_deposits](https://github.com/ethereum/consensus-specs/blob/0c5ad81145fea58504b6db9e8c73214a9fcb331a/specs/phase0/beacon-chain.md?plain=1#L1882)

It is our opinion, that between proof-of-possession and the blinding techniques involved in **The Tuyen Optimization**, rogue key attacks are mitigated and the solution meets security best-practices.

## Acknowledgements

Special thanks to some amazing people who helped put this together:

- Tuyen Nguyen @twoeths
- Sebastian Lindner
- Cayman Nava @wemeetagain

## Replies

**matthewkeil** (2024-10-01):

For those looking to implement this optimization you can find a great write up with code that [@wemeetagain](/u/wemeetagain) put together.  Has the history of how this came about and how to implement in TS.



      [gist.github.com](https://gist.github.com/wemeetagain/d52fc4b077f80db6e423935244c2afb2)





####



##### lodestar-attestations.md



```
# Lodestar attestation verification optimization

> TLDR: we want to use `fast_aggregate_verify` to verify unaggregated attestations signing over the same message, and do so safely.

## Timeline

- Apr 2023:
  - We collected metrics showing that our node struggled to verify attestations quick enough, especially when subscribed to all subnets
- Jun 2023:
  - We noticed that many attestations are signed over the same `AttestationData` and that there may be a way to do less work
```

   This file has been truncated. [show original](https://gist.github.com/wemeetagain/d52fc4b077f80db6e423935244c2afb2)


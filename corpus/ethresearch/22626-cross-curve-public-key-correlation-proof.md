---
source: ethresearch
topic_id: 22626
title: Cross-curve public key correlation proof
author: "71104"
date: "2025-06-17"
category: Cryptography
tags: []
url: https://ethresear.ch/t/cross-curve-public-key-correlation-proof/22626
views: 174
likes: 0
posts_count: 3
---

# Cross-curve public key correlation proof

For the project I mentioned in [this thread](https://ethresear.ch/t/generating-pasta-keypairs/22610) I’m building a network of nodes that will communicate with each other via [gRPC](https://grpc.io/). I’m going to use SSL/TLS (actually mTLS) not only for encryption but most importantly for **authentication**, so that each node knows exactly what node it’s talking to, or rather what the public key / wallet address of the peer is. Of course a fully decentralized project cannot have any central components, so there will be no certification authorities involved and all SSL certificates will be self-signed.

Now, here’s the problem. In principle a self-signed certificate proves ownership of a private key, so I could simply use the same key pair for both the wallet and the self-signed certificate, that way the peer knows exactly what wallet it’s talking to even though the certificate is self-signed. However, I’m almost certainly going to use **the Schnorr signature scheme over the Pallas curve** for my wallets (feel free to ask me why), and unfortunately **SSL supports neither**.

## Possible Solution

As you can see in the [same thread](https://ethresear.ch/t/generating-pasta-keypairs/22610/2), I’ve recently started learning about elliptic curve cryptography and the Schnorr scheme. And I learned that deriving keys is independent of the signature scheme, it only depends on the specific curve. So that gave me an idea: **can I use the same private key scalar for both the wallet and the self-signed certificate, and then somehow prove that the two resulting public keys (the Ed25519 public key of the certificate and the Pallas public key of the wallet) are correlated and share the same private key?**

It seems I can get close to that. And I’m going to have to implement a fair bit of custom cryptography, which might be a risk but still worth pursuing IMO.

In addition to the usual fields, my mTLS certificates will also contain:

- the public Pallas key of the node’s wallet,
- a zero-knowledge proof to convince the peer that the Ed25519 public key and the Pallas public key are correlated without revealing the private key.

The latter is basically a “dual” Schnorr-style signature calculated over both curves (25519 and Pallas). If the signature checks out on both curves with both public keys then the peer is convinced.

One aspect to take care of is that the private key scalar must be valid in the fields of both curves, so it must be strictly less than min(n_{25519}, n_{Pallas}) with n_C being the scalar field order of curve C (not to be mixed up with the *base* field order). That doesn’t seem to be a problem because both curves have a scalar field order that’s in the whereabouts of 2^{25something} (2^{252} for 25519 and 2^{255} for Pallas, it seems).

## Definitions

- n_C = the field order of curve C as explained above, e.g. n_{25519} and n_{Pallas}.
- n = min(n_{25519}, n_{Pallas}). Some of the scalars we use must be valid in the scalar fields of both curves, so we’ll refer to the field F_n for those.
- x = the private key, such that x \in F_n.
- G_C = the generator point of curve C.
- P_C = x \cdot G_C = the public key over curve C.
- r = a nonce in F_n.
- c = Schnorr-style challenge hash.
- s_C = the signature response scalar over curve C.

## Signature

- Generate a nonce r such that r \in F_n.
- Commit to the nonce on both curves:

\begin{aligned}
R_{25519} &= r \cdot G_{25519} \\
R_{Pallas} &= r \cdot G_{Pallas}
\end{aligned}

- Compute the challenge hash and make it valid on both fields (it can be a SHA-3 modulo n):

c = H(R_{25519} || R_{Pallas} || P_{25519} || P_{Pallas}) \mod{n}

- Compute the response scalar on both curves:

\begin{aligned}
s_{25519} &= r + c \cdot x \mod{n_{25519}} \\
s_{Pallas} &= r + c \cdot x \mod{n_{Pallas}}
\end{aligned}

- The signature is the quadruple:

(R_{25519}, R_{Pallas}, s_{25519}, s_{Pallas})

## Verification

- Compute the challenge hash as above:

c = H(R_{25519} || R_{Pallas} || P_{25519} || P_{Pallas}) \mod{n}

- Check the equations:

\begin{aligned}
s_{25519} \cdot G_{25519} &\stackrel{?}{=} R_{25519} + c \cdot P_{25519} \\
s_{Pallas} \cdot G_{Pallas} &\stackrel{?}{=} R_{Pallas} + c \cdot P_{Pallas}
\end{aligned}

## Incompleteness

In the signature there is unfortunately no evidence that R_{25519} and R_{Pallas} are related, and of course we cannot reveal r or anyone would be able to recover the private key by solving the response scalar equations for x. This means the scheme cannot definitely prove that P_{25519} and P_{Pallas} come from the same private key, but it definitely proves that the signer owns the private keys of both (whether they’re the same or different).

That’s good enough for my purpose because proving ownership of the private key of P_{Pallas} is all I care about, and allowing different private keys might actually provide the node owner with a little extra configuration flexibility. However it raises the question: **is it possible to improve this scheme to fully prove that P_{25519} and P_{Pallas} derive from the same private key?**

The answer to that must be yes because worst case I can make a zk-SNARK with a circuit that derives P_{25519} and P_{Pallas} from the same private key (*“I know a secret key valid on both curves that results in public key P_{25519} on Curve25519 and in P_{Pallas} on curve Pallas.”*). But I was hoping to find a simpler answer (in-circuit field conversions are complicated, if I used e.g. [Halo2](https://zcash.github.io/halo2/) the Pallas key derivation would be native but I’d still have to convert all Curve25519 arithmetic to the Pallas field), as well as one that doesn’t rely on bleeding-edge cryptography for the security of the private key (what if one of these zk-SNARK schemes turns out to be vulnerable and someone manages to recover the private inputs, which include the private key in this case?).

## Alternatives Considered

### 1. Self-signed wallet key

Rather than going through this hassle, why not just embed the Pallas public key in the certificate along with a signature of itself that can be verified with itself?

**Because that would open a replay attack vector leading to impersonation**. Once one of these certificates becomes public, anyone can make its own self-signed SSL certificate containing someone else’s Pallas public key.

### 2. Double-signed wallet key

So why don’t we sign the public Pallas key twice – once with itself and once with the Ed25519 keypair?

**Because that’s exactly the same as #1 above**.

### 3. Double-signed wallet key the other way around

Sign the public Pallas key twice – *first* with the Ed25519 key and *then* with itself!

That could work and it’s probably equivalent to what we’re doing with our proposal, the only difference being that our scheme is slightly more ergonomic and slightly more efficient (we’re hashing only once, a double signature would require computing two different challenge hashes). No big deal anyway.

### 3. zk-SNARKs

Discussed above, in the “Incompleteness” section.

## Replies

**71104** (2025-06-18):

Update: I managed to optimize this algorithm and actually achieve full proof of correlation between the two public keys, without resorting to things like zk-SNARKs!

Let’s recall the algebraic structures underlying ECC. We have:

- a scalar field, a prime order field where all scalars (such as the private key or the challenge hash) are defined;
- a base field, another prime order field where the coordinates of all points (such as the public key or the generator of the curve) are defined;
- and a group inferred by a special point addition operation.

When we do things like:

P = x \cdot G

i.e. multiply a scalar x by a point G to obtain another point P, **the three structures do not interfere with each other**:

- x keeps being defined on the scalar field,
- G's coordinates keep being defined on the base field,
- and the multiplication is really just saying add up G in the group x times, performing all low-level arithmetic operations with its coordinates on the base field.

So the group is a higher abstraction layer that builds upon the base field, and the scalar field can’t interfere because the multiplication is just asking to use the group sum on G some number of times (x).

This led me to the following idea: since the scalar field doesn’t interfere with the multiplication, we could use *any* scalar field for most equations. **We could use F_n for the signature response scalar on both curves, so we’d have a single scalar s rather than s_{25519} and s_{Pallas}**. And, as it turns out, that is sufficient to prove the two public keys derive from the same private key.

New algorithm below.

## Definitions

- n_C = the field order of curve C as explained above, e.g. n_{25519} and n_{Pallas}.
- n = min(n_{25519}, n_{Pallas}). The scalars we use must be valid in the scalar fields of both curves, so we’ll refer to the field F_n for those.
- x = the private key, such that x \in F_n.
- G_C = the generator point of curve C.
- P_C = x \cdot G_C = the public key over curve C.
- r = a nonce in F_n.
- c = Schnorr-style challenge hash.
- s = the signature response scalar.

## Signature

- Generate a nonce r such that r \in F_n.
- Commit to the nonce on both curves:

\begin{aligned}
R_{25519} &= r \cdot G_{25519} \\
R_{Pallas} &= r \cdot G_{Pallas}
\end{aligned}

- Compute the challenge hash and make it valid on both fields (it can be a SHA-3 modulo n):

c = H(R_{25519} || R_{Pallas} || P_{25519} || P_{Pallas}) \mod{n}

- Compute a single response scalar:

s = r + c \cdot x \mod{n}

- The signature is the triple:

(R_{25519}, R_{Pallas}, s)

## Verification

- Compute the challenge hash as above:

c = H(R_{25519} || R_{Pallas} || P_{25519} || P_{Pallas}) \mod{n}

- Check the equations:

\begin{aligned}
s \cdot G_{25519} &\stackrel{?}{=} R_{25519} + c \cdot P_{25519} \\
s \cdot G_{Pallas} &\stackrel{?}{=} R_{Pallas} + c \cdot P_{Pallas}
\end{aligned}

## Completeness

If s and c check out on both curves (with both public keys and both generators), the original x must have been the same. There’s no way to come up with values for s and c that satisfy both equations with two different x's.

## Conclusions

We built a Schnorr-like scheme based on ECC allowing us to:

- derive two public keys on two completely different curves from the same private key;
- prove that the two public keys are derived from the same private key without revealing the private key.

This allows us to use Poseidon-Schnorr keypairs and signatures in application code while authenticating our program with the same private key on a protocol that doesn’t support Poseidon-Schnorr, specifically mTLS with self-signed Ed25519 certificates.

---

**71104** (2025-06-18):

I have to add an important note of caution to my last post.

The scalar field “doesn’t interfere” with the base field and group as in *“point addition works any number of times n, with n being a positive integer from any field”*, but there’s an important mathematical relation between the scalar and base fields that make it infeasible to reverse point multiplication due to the discrete log problem.

**We cannot change the scalar field freely** when we do point multiplications, otherwise it might become easier to recover the multiplying scalar. So for example we cannot unify the two nonce equations, which must remain separate:

\begin{aligned}
R_{25519} &= r \cdot G_{25519} \\
R_{Pallas} &= r \cdot G_{Pallas}
\end{aligned}

In particular we must not try to add up G_C more than n_C times, with n_C being the order of the scalar field of curve C. Doing so could make it easier to recover the scalar (recall that r is just as critical as x because having r the equation of s can be solved for x).

On the other hand, no point multiplication is involved in the signature response scalar:

s = r + c \cdot x \mod{n}

So for that we could use whatever field suits all the involved scalars. But we need to make sure to never exceed the scalar field order of any point multiplication that may happen later on, so that’s why it’s important to choose n = min(n_{255191}, n_{Pallas}).


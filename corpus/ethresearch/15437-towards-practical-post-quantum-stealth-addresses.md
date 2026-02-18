---
source: ethresearch
topic_id: 15437
title: Towards practical post quantum stealth addresses
author: asanso
date: "2023-04-27"
category: Cryptography
tags: []
url: https://ethresear.ch/t/towards-practical-post-quantum-stealth-addresses/15437
views: 2652
likes: 9
posts_count: 4
---

# Towards practical post quantum stealth addresses

# Towards practical post quantum stealth addresses

**Stealth addresses** are a type of privacy-enhancing technology used in cryptocurrency transactions. They allow users to send and receive cryptocurrency without revealing their public addresses to the public ledger.

In a typical cryptocurrency transaction, a sender must reveal their public address to the receiver, as well as to anyone who may be monitoring the blockchain. This can compromise the user’s privacy and security, as it allows others to link their transactions and potentially track their funds.

With stealth addresses, however, the sender generates a unique, one-time public address for each transaction, which is not linked to their permanent public address on the blockchain. The receiver can still receive the funds to their permanent public address, but only they can link the stealth address to their own address and access the funds.

Stealth addresses provide an additional layer of privacy and security to cryptocurrency transactions, making it more difficult for third parties to track and monitor user activity on the blockchain.

You can read about it in a recent [Vitalik’s post.](https://vitalik.ca/general/2023/01/20/stealth.html)

In this post we are going to analyze a possible Post Quantum version of stealth addresses based on Commutative Supersingular isogenies (CSIDH).

**N.B**. If you wonder if this solution is affected by the new devastating attacks on SIDH the answer is **NO**. They crucially relies on torsion point information that are not present in CSIDH based solutions.

## Stealth addresses with elliptic curve cryptography

Recapping from Vitalik’s post

- Bob generates a key m, and computes M = mG, where G is a the generator point for the elliptic curve. The stealth meta-address is an encoding of M.
- Alice generates an ephemeral key r, and publishes the ephemeral public key R = rG.
- Alice can compute a shared secret S = rM, and Bob can compute the same shared secret S = mR.
- To compute the public key, Alice or Bob can compute P = M + hash(S)G
- To compute the private key for that address, Bob (and Bob alone) can compute p = m + hash(S)

This is translated in [sage’s code](https://github.com/asanso/stealth-address/blob/e11f629be688688e18f0d465b9220b063c11e855/stealth-address.sage):

```auto
#Bob

#private
m = ZZ.random_element(n)
#public
M = m*G

#Alice

#private
r = ZZ.random_element(n)
#publish
R = r*G
Sa = r * M
s = ''
s+=str(R[0])
s+=str(R[1])
s+=str(Sa[0])
s+=str(Sa[1])
h.update(s.encode())

hashS = (int(h.hexdigest(), 16)) % n
Pa  = M + hashS*G

#Bob
Sb = m*R
Pb = M + hashS*G
p = m+hashS

assert Sa == Sb
assert Pa == Pb == p*G
```

## Commutative Supersingular isogenies (CSIDH).

This section (and the remainder of the post) will require some knowledge about elliptic curves and isogeny based cryptography. The general reference on elliptic curves is [Silverman](https://link.springer.com/book/10.1007/978-0-387-09494-6) for a thorough explanation of isogenies we refer to [De Feo](https://arxiv.org/pdf/1711.04062.pdf).

CSIDH is an isogeny based post quantum key exchange presented at Asiacrypt 2018  based on an efficient commutative group action. The idea of using group actions based on isogenies finds its origins in the now well known [1997 paper by Couveignes](https://eprint.iacr.org/2006/291.pdf). Almost 10 years later Rostovtsev and Stolbunov [rediscovered Couveignes’s ideas](https://eprint.iacr.org/2006/145.pdf).

Couveignes in his seminal work introduced the concept of *Very Hard Homogeneous Spaces* (VHHS). A VHHS is a generalization of cyclic groups for which the computational and decisional Diffie-Hellman problem are hard. The exponentiation in the group (or the scalar multiplication if we use additive notation) is replaced by a group action on a set. The main hardness assumption underlying group actions based on isogenies, is that it is hard to invert the group action:

**Group Action Inverse Problem (GAIP).** Given a curve E, with End(E) = O, find an ideal a ⊂ O such that E = [a]E_0.

The GAIP (also known as *vectorization*) might resemble a bit the discrete logarithm problem and in this post we exploit this analogy to translate the stealth addresses to the CSIDH setting.

# Stealth addresses with CSIDH

In this section we will show an (almost) 1:1 stealth addresses translation from the DLOG setting to the VHHS setting:

- Bob generates a key m, and computes E_m = [m]E_0, where E_0 is a the starting elliptic curve. The stealth meta-address is an encoding of E_m.
- Alice generates an ephemeral key r, and publishes the ephemeral public key E_r = [r]E_0.
- Alice can compute a shared secret E_S = [r]E_m, and Bob can compute the same shared secret E_S = [m]E_r.
- To compute the public key, Alice or Bob can compute P = [hash(E_S)]E_m
- To compute the private key for that address, Bob (and Bob alone) can compute p = [m + hash(S)]

Here is the relevant sage snippet ([here](https://github.com/asanso/stealth-address/blob/e11f629be688688e18f0d465b9220b063c11e855/pq-stealth-address.sage) the full code)

```auto
#Bob
#private
m = private()
#public
M = action(base, m)

#private
r =private()
#publish
R = action(base, r)
Sa = action(M, r)

s = ''
s += str(R)
s += str(Sa)
h.update(s.encode())
hashS = (int(h.hexdigest(), 16)) % class_number
hashS_reduced = reduce(hashS,A,B)

P = action(M,hashS_reduced)

#Bob
Sb = action(R, m)
pv = []
for i,_ in enumerate(m):
    pv.append(m[i]+hashS_reduced[i])

assert Sa == Sb
assert P == action(base,pv)
```

## Acknowledgement

Thanks to Vitalik Buterin, Luciano Maino, Michele Orrù and Mark Simkin for fruitful discussions and comments.

## Replies

**Nero_eth** (2023-04-27):

Interesting concept!

Have you already tried to reveal, for example, one byte of the `hashS_reduced` to incorporate [viewtags](https://github.com/monero-project/research-lab/issues/73) similar to Monero, in order to accelerate the recipient’s parsing time by avoiding further computation if the initial byte doesn’t match?

Additionally, do you think that by supplying Bob with two keypairs, a dual-key stealth address protocol could be implemented, such as:

```auto
#Bob Viewing & Spending Key
#private
m1 = private()
m2 = private()
#public
M1= action(base, m)
M2= action(base, m)

#private
r =private()
#publish
R = action(base, r)
Sa = action(M2, r)

s = ''
s += str(R)
s += str(Sa)
h.update(s.encode())
hashS = (int(h.hexdigest(), 16)) % class_number
hashS_reduced = reduce(hashS,A,B)

P = action(M1,hashS_reduced)

#Bob
Sb = action(R, m2)
pv = []
for i,_ in enumerate(m1):
    pv.append(m1[i]+hashS_reduced[i])
```

---

**asanso** (2023-04-27):

I haven’t tried but I believe both things are possible

---

**seresistvanandras** (2023-04-28):

Cool application of isogeny crypto! I wonder if isogenies could allow us to solve the problem of efficiently detecting stealth transactions on the blockchain. This might be a great food for thought for isogeny senseis like [@asanso](/u/asanso).

The problem was originally posed by Vitalik on ethresearch [here](https://ethresear.ch/t/open-problem-improving-stealth-addresses/7438).

So far, we do not have many solutions to this problem. I will refrain from mentioning engineering-based solutions that do not really improve the asymptotic complexity of detecting stealth transactions in the

total number of stealth transactions on the blockchain, e.g., viewtags. We really want, at minimum a sublinear detection complexity, but obviously, the best would be constant work on the recipients’ end. A super dense literature review:

1. Fuzzy Message Detection: a delicate tradeoff between efficiency and privacy.
2. Private Signaling: strong privacy assumptions: either a TEE or two non-colluding servers are needed.
3. Oblivious Message Retrieval: FHE-based solution with large detection keys. Zcash and Penumbra are going to deploy it soon.

Two really recent works:

4) [Group Oblivious Message Retrieval](https://eprint.iacr.org/2023/534.pdf): extends and improves on Oblivious Message Retrieval by supporting tags for groups.

5) [Scalable Private Signaling](https://eprint.iacr.org/2023/572.pdf): applies TEEs and Oblivious RAMs.

Can isogenies help us solve this problem? Does isogeny-based crypto allow us to build a detection scheme, where both the sender’s and recipient’s work is low, say polylogarithmic in the number of total stealth transactions on the blockchain?


---
source: magicians
topic_id: 8291
title: Sharding design with tight beacon and shard block integration "Danksharding"
author: dankrad
date: "2022-02-14"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/sharding-design-with-tight-beacon-and-shard-block-integration-danksharding/8291
views: 2932
likes: 4
posts_count: 7
---

# Sharding design with tight beacon and shard block integration "Danksharding"

This is a discussion thread for feedback to the new sharding proposal:

- Overview document: New sharding design with tight beacon and shard block integration - HackMD
- Implementation PR: https://github.com/ethereum/consensus-specs/pull/2792
- Ethereum research workshop: “Dude, what’s the Danksharding situation?” Workshop [2022/2/14] - YouTube
- Workshop slides: Dude, What's the Danksharding situation? - Google Slides

## Replies

**potuz** (2022-02-14):

I want to voice here a concern about KZG commitments, both in this implementation or the previous one for data availability. I worry that there aren’t that many members of this community that can actually vet the mathematics of it. There are plenty of blockchain devs that can take KZG as a blackbox, just as BLST signature verification for example, and vet for the validity and security of the rest of the implementation. There are plenty even that have basic classes on number theory or algebraic geometry that can easily understand KZG by itself but from there to vet for the security of it requires a specialization in cryptography.

Now some researchers from the EF that are qualified to make these statements, like Danrad Feist or Justin Drake can state “KZG are fine and can be taken as a blackbox”, but in order to vet this very statement a strong cryptography background is required.

I don’t mind taking as a blackbox elliptic curve cryptography or hashing algos like SHA256 that we currently use and that have been battle tested in production for over 30 years, ubiquitous in every system from ssh to our phones checksuming webpages. But KZG’s paper is 10 years old, with less than 100 citations (I understand that the whole theory of EC pairings has been more vetted though) and I doubt it has been battle tested not nearly as the cryptographic primitives that we currently depend on. I find quite concerning that we would have this “blackbox” in a blockchain that currently secures assets worth billions of any fiat currency.

---

**dankrad** (2022-02-16):

I believe most developers can understand KZG commitments to an extent that should make it comfortable to work with them and introduce them to the base layer.

As far as I can see there are three components to this:

- Elliptic Curve Pairings. These, I would suggest to most people to take as a black box. We are already accepting them for the beacon chain (BLS signatures), so this is not a new assumption. It is, however, by far the most complex one. Even Costello’s “simple” introduction (https://static1.squarespace.com/static/5fdbb09f31d71c1227082339/t/5ff394720493bd28278889c6/1609798774687/PairingsForBeginners.pdf) comes to 148 pages.
- Finite field/polynomial math. I think the math required is within reach of a dedicated Ethereum dev. My explainer tries to bridge the gap here: KZG polynomial commitments | Dankrad Feist
- There is one additional assumption, the q-strong DH assumption (from the powers [s], [s^2], [s^3], …, [s^q] in the group you cannot find [1/(s-x)]). This is a cryptographic assumption that has been around in some form since 2004 (https://eprint.iacr.org/2010/215.pdf).

I think since we have “swallowed” pairings, the only major question would be about the q-strong DH assumption. My personal feeling is that it is relatively simple and well established (all pairing-based zero-knowledge proof systems rely on it), but I will leave a more detailed analysis to cryptographers.

---

**CryptoWhite** (2022-02-19):

I wonder if the final implementation of Danksharding is compatible with Optimistic Rollups. As I know, Optimistic Rollups need to access a lot of L2 tx data when validating fraud proofs. But in Danksharding these data are located in shardings and the EVM in the exec layer do not have direct access to them.

---

**vbuterin** (2022-02-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/potuz/48/8696_2.png) potuz:

> I don’t mind taking as a blackbox elliptic curve cryptography or hashing algos like SHA256 that we currently use and that have been battle tested in production for over 30 years, ubiquitous in every system from ssh to our phones checksuming webpages. But KZG’s paper is 10 years old, with less than 100 citations (I understand that the whole theory of EC pairings has been more vetted though) and I doubt it has been battle tested not nearly as the cryptographic primitives that we currently depend on. I find quite concerning that we would have this “blackbox” in a blockchain that currently secures assets worth billions of any fiat currency.

If you take EC and pairings as a given, KZG is pretty simple to understand: it’s just generating a set of points `T_0 = G`, `T_1 = G*s`, `T_2 = G*s^2` … `T_n = G*s^n` with a forgotten secret `s` as the setup, and then committing to a polynomial `P(x) = Σ c_i * x^i` (where `c_i` are the coefficients) by taking `Σ c_i * T_i`. It’s a “use of existing ingredients” that’s significantly less complicated than many other uses of existing ingredients that Ethereum already has.

EC pairings are definitely highly complicated, but the Ethereum consensus layer depends on them already for BLS signatures and the RANDAO. If we could later remove the pairing dependencies in both of these cases, I would love that, but it will take a while to figure out the right way to do it, and continuing to use pairing-based crypto is far simpler in the meantime.

---

**dankrad** (2022-03-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cryptowhite/48/5489_2.png) CryptoWhite:

> I wonder if the final implementation of Danksharding is compatible with Optimistic Rollups. As I know, Optimistic Rollups need to access a lot of L2 tx data when validating fraud proofs. But in Danksharding these data are located in shardings and the EVM in the exec layer do not have direct access to them.

Actually nothing changes here – optimistic rollups do not access historical data inside the EVM, there is no such opcode. Instead, when there is a fraud proof, they bring it back on chain as calldata, together with a proof (a witness) of correctness. Exactly the same principle works for sharded data.

---

**CryptoWhite** (2022-03-09):

Get it. The shard looks like extended storage space mounted to the Ethereum OS with blob tx as its mount point. Each shard is kept in a part of nodes but everyone can still access it. Later people can use some sharded data to generate fraud proofs (in this case one needs to load the sharded data back to the chain) and validity proofs (especially when the rollup state is lost).

The new Danksharding is much better than the original sharding design.


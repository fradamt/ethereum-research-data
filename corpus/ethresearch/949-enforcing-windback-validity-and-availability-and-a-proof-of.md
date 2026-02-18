---
source: ethresearch
topic_id: 949
title: Enforcing windback (validity and availability), and a proof of custody
author: JustinDrake
date: "2018-01-29"
category: Sharding
tags: []
url: https://ethresear.ch/t/enforcing-windback-validity-and-availability-and-a-proof-of-custody/949
views: 4406
likes: 12
posts_count: 6
---

# Enforcing windback (validity and availability), and a proof of custody

**Background**

The security of sharding depends on “windback”. When validators extend the collation header chain for a given shard, windback means downloading and verifying a few collation bodies from the immediate past. Vitalik estimated that we’d want a windback length of [about 25](https://ethresear.ch/t/detailed-analysis-of-stateless-client-witness-size-and-gains-from-batching-and-multi-state-roots/862/5). (Side question: why 25?)

SPV mining (“blind” mining) is basically when there’s little to no windback. It is bad (c.f. [the BIP66 Bitcoin incident](https://bitcoin.stackexchange.com/questions/38437/what-is-spv-mining-and-how-did-it-inadvertently-cause-the-fork-after-bip66-wa)), and particularly so in the context of sharding.

Slightly more abstractly winding back means checking two things:

1. Collation (real-time) data availability: Usually checked (locally with respect to your network access) by attempting to download to relevant collation bodies.
2. Collation validity: Usually checked (locally with respect to your consensus rules) by executing the transactions in the collation body.

The above two checks are essential to security but seem to go against scalability. The reason is that downloading collation bodies and executing transactions both scale *linearly*, whereas we need something sublinear for scalability.

**Enforcing validity**

SNARKs/STARKs solve (in theory at least) the validity problem. By requiring validators to publish a succint and quick to verify proof of validity in the collation header, validity can be enforced sublinearly. This is very neat, but does *not* help with data availability. Collation bodies from the immediate past can simultaneously be valid and unavailable. Even immediate block creation can be outsourced to a third party (e.g. a briber) and the newly-created block withheld from the validator.

**Enforcing availability**

Enforcing availability is less trivial. One approach is “proofs of custody”. A proof of custody is a cryptographic guarantee that some identity (in our case, a validator) had full access to some piece of data (identified by its hash) when the proof was produced. (Signatures schemes don’t usually work because they are based on digests which are usually outsourceable.)

Assuming the existence of proofs of custody, we can require validators to publish a proof of custody for the concatenation of all the collation bodies in the windback period, which would prove availability.

Some progress was made on proofs of custody in [a paper by Pavel Kravchenko and Vlad Zamfir](https://distributedlab.com/whitepaper/ProofOfcustody.pdf). Their construction does not work for our purposes because the proof size is linear (and concretely too large), and the proof is interactive (although they note it can be made non-interactive with the Fiat-Shamir heuristic).

**Proof of custody**

We present below a new proof of custody. It uses SNARKs/STARKs and is non-interactive, constant space, and constant time to verify.

Let B be the collation bodies for which a validator needs to prove direct (non-outsourceable) custody. Let P be the validator’s private key. Split B into an array of small chunks (e.g. 32-byte chunks) so that B is the concatenation of B[0], ..., B[n].

The idea is to build a digest D for B which heavily “incorporates” P. Because P cannot be shared without compromising the validator’s deposit, computing D is non-outsourceable. The specific digest construction we suggest is D = \textrm{SHA3}(B[0]\oplus P) \hspace{1mm}\oplus\hspace{1mm} ... \hspace{1mm}\oplus\hspace{1mm} \textrm{SHA3}(B[n] \oplus P).

To prove availability, the following is included in the collation header:

1. The digest D
2. A SNARK/STARK that proves D faithfully corresponds to B and P (using zero-knowledge for privacy of P)

## Replies

**kladkogex** (2018-02-13):

I wonder if one could use aggregate signatures [like this](https://cseweb.ucsd.edu/~mihir/papers/agg.pdf)

instead of SNARKS/STARKS.  You could theoretically split the file into many small pieces, sign each piece to get lots of signatures, and then aggregate all signatures into one.

BTW in the proposal above one needs to to something about chunk ordering, it looks like one can reorder chunks without changing D …

---

**JustinDrake** (2018-02-13):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> You could theoretically split the file into many small pieces, sign each piece to get lots of signatures, and then aggregate all signatures into one.

Oooh, interesting idea! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) BLS signatures do indeed allow for aggregation of signatures for multiples messages into a single signature.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> it looks like one can reorder chunks without changing D

Well spotted, thanks!

---

**MaxC** (2018-02-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> To prove availability, the following is included in the collation header:

My worry with the BLS scheme is that you will need the message to verify proof of custody?

Is that not cart before horse?  Also, even if you could  statistically sample and verify parts of the message, with a high probability an attacker might only keep 99% of the message and pass the tests.

Apologies if mistaken.

---

**JustinDrake** (2018-02-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> you will need the message to verify proof of custody

Good point. It suffices for a single collation body to be unavailable for the BLS signature to be unfalsifiable. We could strengthen the BLS scheme with a SNARK/STARK that the BLS signature faithfully corresponds to B. At that point both the XOR scheme and the BLS scheme follow the same recipe:

1. Split B into small chunks B[0], ..., B[n].
2. For each chunk apply some mixing function on (B[i], P):

For the XOR scheme that’s (B[i], P) \mapsto \textrm{SHA3}(B[i] \oplus P)
3. For the BLS scheme that’s (B[i], P) \mapsto \textrm{sig}(B[i], P)
4. Merge the mixed chunks into a succinct object
5. Prove with a SNARK/STARK that the succinct object is faithful

Although this recipe works well for honest-but-lazy validators, I don’t think step 2) works in the context of bribed validators because of MCPs that allow a validator and a briber to compute f(B[i], P) without the briber revealing B[i] (withholding B[i]) and without the validator revealing P.

---

**kladkogex** (2018-02-22):

Here is an interesting paper regarding crypto hashes that are SNARK-friendly

> We explore cryptographic primitives with low multiplicative
> complexity. This is motivated by recent progress in practical applications
> of secure multi-party computation (MPC), fully homomorphic encryption
> (FHE), and zero-knowledge proofs (ZK) where primitives from
> symmetric cryptography are needed and where linear computations are,
> compared to non-linear operations, essentially “free”.



      [eprint.iacr.org](https://eprint.iacr.org/2016/492.pdf)



    https://eprint.iacr.org/2016/492.pdf

###



485.25 KB


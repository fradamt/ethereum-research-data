---
source: ethresearch
topic_id: 18704
title: Lookup singularity via MMR
author: Hmac512
date: "2024-02-18"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/lookup-singularity-via-mmr/18704
views: 3514
likes: 35
posts_count: 9
---

# Lookup singularity via MMR

# Lookup Singularity via MMR

## Introduction

What I will show is that if we have a public merkle mountain range where existence within it implies correctness, then this primitive can be used to achieve the lookup singularity. What I mean is you can enable complex lookup tables for sha256 hash, merklizing leaves, or potentially even EVM storage proofs.

There are optimistic and immediate finality variations of this scheme which balance certain trade offs.

## Background

Lookup tables are an incredible innovation in the world of ZKPs. They allow for much faster proving for complex computation like a Sha256 hash. Barry Whitehat coined the term the lookup singularity ([Lookup Singularity - General - zk research](https://zkresear.ch/t/lookup-singularity/65)) to represent how they can drastically improve the performance of SNARKs.

Standard lookup tables require pre-computing an entire table, and committing it during circuit compilation. Therefore these tables cannot be updated after the keys are generated. The cost of committing the table is amortized over all the lookups used during proving. There is a negligible per-lookup cost for these types of constructions (eg plonk-lookup). The obvious limitation here is that it’s impractical for lookup tables that are very large, say 32-bit float arithmetic (2^64 rows).

Justin Thaler wrote papers for a new system called Jolt/Lasso which sacrifices the low per-lookup cost in order to get more complex lookups. This is done by using multivariate polynomials to represent the lookup table as a  polynomial evaluation. This makes it so you don’t need the full table in memory to use in a circuit, but increases the per-lookup cost. See [Lasso/src/subtables/lt.rs at 823da601422d17f7c150631947b33a9db1ad5b98 · a16z/Lasso](https://github.com/a16z/Lasso/blob/823da601422d17f7c150631947b33a9db1ad5b98/src/subtables/lt.rs#L59)

These constructions don’t practically allow for lookup tables of truly complex operations like a sha256 hash. Say I had 100 leaves and I wanted to merklize them to compute the root. No existing lookup table construction can help you with this.

## Trusted lookup table oracle

One very easy way to increase the performance and utility of a lookup table is to use a trusted source. Imagine I wanted to multiply 2 floating point numbers, I can submit the lookup via an API to a service that returns the lookup table with a snark-friendly signature. In practice we would batch all the look ups together with one signature.

The beauty of this approach is you can enable truly arbitrary lookup operations, which would dramatically improve the performance of your circuits. You also get a custom lookup table for each proof you generate. This approach would drastically decrease circuit complexity.

One thing to note is that for any sensitive parts of the circuit you may wish to do it without the table oracle to preserve privacy. Alternatively you could include extra unnecessary lookups to obfuscate which were used. This approach lets you offload any parts of the circuit which can be public into a lookup table. Essentially a selectively disclosed computation ZKP.

However, the issue here is that the trusted party can secretly sign incorrect lookups in order to forge a proof and attack a system. The idea I want to present is to solve this malicious lookup oracle problem via crypto-economic methods.

***What if there was a better way?***

## Securing with crypto-economic security

The obvious place to start is have the lookup oracle stake a large amount of ETH/USDC/etc. If I can coerce the oracle to give me a malicious result, I can generate a fraud proof (ZKP or smart contract) in order to claim a reward.

This works well to prevent the oracle from colluding with someone else. This however fails in the situation where the oracle is also the one requesting the lookup. There is no economic incentive to claim your own stake.

The only way to solve this problem is to force the oracle to publicly disclose every lookup table that it generates. This can be done with a merkle mountain range (MMR). The key insight you need to see is that existence within the public MMR directly implies correctness. We then construct the circuits to check for existence within a MMR, and we then compare with the root of the trusted, public MMR.

## Overall Solution

First you use a merkle mountain range w/ a zk friendly hash to commit tables into a smart contract. A MMR is advantageous because:

1. Scales virtually infinitely
2. Short inclusion proofs
3. Quick to update proofs

In order to avoid confusion, I want to emphasize the MMR **does not** merklize a full lookup table. Instead each leaf in the MMR can be a custom lookup table(s) for a particular proof generated. Each leaf can be multiple tables, as a circuit might offload multiple operations to a table. The MMR may include duplicate lookups.

The lookup table used during proving only needs to include the entries needed. This is the key advantage of this approach. The table(s) can be generated locally by the user before being generating the proof. The tables then can be sent to be added to the global MMR, at which point the proof can be updated to have inclusion in trusted MMR.

To save on gas, the actual lookup tables do not need to be put on-chain, we can use an optimistic approach where just the commitments of the tables are stored. The details around off-chain data availability will not be discussed here.

In situations where we want quick finality, you can have a contract verify table validity before adding it to the global MMR. The trade off is it will cost more. The optimistic approach actually allows for much more complicated look ups (eg call a smart contract w/ some input at a block height)

There are a few variations these tables can be utilized, but the custom lookup table is always an input into the primary circuit. This is nice because in a mobile app setting this enables us to generate a snark and its corresponding tables very quickly. What remains is proving the table used is in the global lookup tree. The mobile app can submit the zkp + lookup table to an infrastructure provider which will finalize the snark.

The infrastructure provider can verify the table validity, and submit it for inclusion into the trusted MMR. Once included, an inclusion proof can be generated. The original snark can be recursively updated to verify the table used exists within the global MMR. The root of the MMR then becomes a public input of the resulting ZKP. The location of the table can optionally be disclosed as well.

The overall trade-off is pretty simple. For the price of waiting a bit to submit/verify the proof, you get fast and memory efficient snarks client-side. The waiting to submit can be handled for the user with infrastructure.

Complex fraud proofs are not required for the optimistic variation. A smart contract can be used to check validity of entries when prompted.

### Conclusion

I am very confident the above would work, and yield dramatic performance gains to client-side snark proving.

For the optimistic variation we can enable truly complex lookups that simplify ZKPs around EVM storage proofs. The tradeoff for very complex look ups would be a longer settlement time. The settlement time can be decreased if you limit the lookup operations in complexity (sha256, floating point operations etc).

In the immediate finality variation, there will be a larger financial cost for each addition to the MMR. I suspect the EVM would be prohibitively expensive, especially at scale. To optimize this approach it would be best to build a new chain. As of the time of writing, Solana is doing 3500 TPS at a tx fee around $0.0002. If you reduced the complexity of the execution environment you would get more TPS for cheaper.

# Alternative Perspective

It hit me after my initial post that there is an alternative use case for the technique described above where a MMR is unnecessary.

From the perspective of the prover, generating the main ZKP is done in two parts

1. Compute lookup table(s) for circuit
2. Use table(s) as a public input to generate the ZKP

From here we have a ZKP and a list of assumptions the ZKP is made on. The other use case is the prover can offload some of the heavy parts of the circuit to infrastructure to validate the assumptions, and recursively update the ZKP.

Pretty neat

## Replies

**Hmac512** (2024-02-19):

In research it seems the default view is that of skepticism. For good reason. I wanted to explain in simple terms why the technique above will yield great performance gains. Particularly in circuits where a lot of the computation doesn’t need to private. My view is a new paradigm in circuit design may be required to fully realize the potential gains.

Fundamentally, the technique moves a lookup table from being committed at compilation, to being an input to the circuit. It’s so simple I am surprised this was not considered before. There are a lot of use cases for this beyond my MMR approach.

Imagine we had a trusted oracle sign a custom lookup table for each proof we generate. This will improve performance of ZKPs because:

1. We only need to materialize the lookups we need,
2. We can support very complex lookups (hashes, merklizing 1000 leaves, floatOps, out of field stuff etc).

All I have done above is preserve those benefits and remove:

1. Remove the need for a trusted source (decentralization),
2. Replace the signature with a MMR inclusion proof.

The hard part of all of this is building the MMR so that inclusion implies correctness, rather than advanced polynomial magic.

---

**Hmac512** (2024-02-20):

I have gotten feedback that it’s unclear the role the MMR plays in this, so I am writing this to clarify how proof generation will work.

To generate a proof:

Generate the lookup table(s) you need

Generate the zkp using the lookup table(s) as a public input

Submit the tables to lookup table mempool to be added to MMR chain

Validator verifies the tables are correct, and adds them to canonical MMR

Generate a proof of inclusion of the tables used in the canonical MMR

Recursively update the ZKP, with the resulting proof having the root of the MMR as a public input

---

**veigajoao** (2024-02-20):

That’s a very interesting idea, a couple of thoughts I had:

It seems to me that the bulk of the performance gains comes from materializing only the lookups that are needed for a specific computation - e.g. have a lookup table of  preimage:hashes that are going to be used in the computation.

That essentially implies that the SNARK is not going to be verifying the entire computation anymore, but only a subset of it. In this setting the we need a trusted oracle to provide the correct lookups in a trustworthy manner, I see there are 3 ways to do it:

a. Replicated state machine → multiple different parties calculate the lookup and come to consensus on it, having slashing for misbehavior;

This method works, but essentially shifts the burden of verifiable computation from zkSNARKS into replicated consensus, in my view it would only make sense in cases where it is significantly cheaper to perform the operations outside of the snark circuit

b. Optimistic → anyone can add to the MMR by posting a bond, in case the lookup is found to be fraudulent, the bond is lost;

c. SNARKs → Additions to the MMR must be verified by a SNARK proving the computation to be correct. This defeats the purpose of the construction since the cost of performing the looked up operation inside a SNARK is being paid somewhere else;

SNARKs are a fascinating technology because they allow a verifier to trust the result of a computation based solely on the proof. The introduction of trust assumptions on computed lookup tables might remove the most appealing feature of zkSNARKs. However, if we can get significant (orders of magnitude) speedups it might be interesting for specific use cases.

Would love to see a PoC on this to evaluate the tradeoffs. Also, do you believe it would be possible to get any sort of performance gains by putting big tables in the public inputs? That could be an alternative to circumvent current limit on table sizes for lookup args.

---

**sina** (2024-02-21):

If I’m understanding correctly, the core idea here is to “blend” different flavors of verifiable compute to consume in ZK, modulo whatever extra trust assumptions come with the other flavors of verifiable compute. You can do this as long as you’re explicit about what new trust assumptions you’re internalizing, which can be fairly safe if it’s eg. a cryptoeconomic trust assumption, and the user is already using the chain as source of truth anyway. Neat!

A few thoughts:

- would be useful to see a poc that illustrates the e2e. I think the main thing I’m wondering is in what scenarios the engineering complexity of the extra steps is worth it, vs just doing the whole compute cryptoeconomically/stomaching the extra ZK cost
- maybe a naive interpretation but IMO the power here isn’t in just improving traditional lookups, but any arbitrary computation that you may want to avoid doing in ZK-space. In this framing, is it better to use a tree that indexes the “trusted results” in a more reusable manner, eg. an SMT indexed by some hash of the computation? I can imagine a “source of cryptoeconomic truth” being progressively built up onchain, and proofs can safely ingest and query into this, reusing old results rather than repeating work
- is it worth exploring similar flavors of “blending” amongst other types of verifiable compute? Namely thinking of using TEEs vs fraud proven vs explicitly-executed-onchain
- final thought: will other improvements to proving time obviate the need for something like this? going from no-trust to some-trust is a bit of a step out from the traditional benefit of using ZK. What if we can tactically sub-prove the expensive things and recursively reuse them, for example; do we still need this? Going back to my first point, would be really impactful to see a case where this makes a big difference in performance while the new trust assumptions are stomachable.

Thanks for sharing ![:grin:](https://ethresear.ch/images/emoji/facebook_messenger/grin.png?v=12)

---

**Hmac512** (2024-02-21):

> It seems to me that the bulk of the performance gains comes from materializing only the lookups that are needed for a specific computation

Yes! you get a dynamic lookup table without having to recompile the circuit. I’d argue in terms of performance/speed, you cannot beat this method for the root proof. The technique enables the circuit to make assumptions for complex operations, and I don’t think you can out-polynomial making an assumption. I’d argue it’s actually the asymptote of perf for complex operations.

> a. Replicated state machine → multiple different parties calculate the lookup and come to consensus on it, having slashing for misbehavior;

> This method works, but essentially shifts the burden of verifiable computation from zkSNARKS into replicated consensus, in my view it would only make sense in cases where it is significantly cheaper to perform the operations outside of the snark circuit

I am not a researcher, so I wrote up the simplest variation that gets the job done. I am not tied to the MMR approach, if another architecture is better I’d happily change my view.

However, doing computation outside of zk (secured by crypto-economic assumptions) actually allows for proving operations that are too resource intensive to do in ZK today. It is in some sense an alternate to a TEE.

A good example would be zkML. On the client if you reduce the circuit to only what is sensitive, and offload the rest to a GPU network then you can feasibly run large ML models in ZK. I actually think this is better than opML or using a TEE.

> b. Optimistic → anyone can add to the MMR by posting a bond, in case the lookup is found to be fraudulent, the bond is lost;

Originally my write up focused on this approach, but after some feedback I decided to present it more generally. The main downside of this approach is a potential settlement period. The duration can be much shorter for simple operations like hashing or floatOps. For very complex lookups like EVM state (ex. erc20 balance), this approach would make client side proving A LOT more efficient. Would require a longer settlement time or a really high bond, but you can drastically simplify your circuits.

> c. SNARKs → Additions to the MMR must be verified by a SNARK proving the computation to be correct. This defeats the purpose of the construction since the cost of performing the looked up operation inside a SNARK is being paid somewhere else;

I disagree with this point. I probably should’ve touched on this in my original post, but this technique allows for a very efficient collaborative SNARKs setup. It sacrifices the privacy guarantees of normal collab SNARKs though, so it’s something new.

This approach lets the main prover temporarily sacrifice succinctness in exchange for proof speed. At the end of the root proof we have a ZKP, and a list of assumptions that the ZKP makes. Proof + Table

What remains is to prove the table is sound. There are a few ways to do this:

1. Have infrastructure generate ZKP of table soundness and recursively update proof,
2. Verifier directly verifies the ZKP and the table (might be best if table is small),
3. Offload to a decentralized compute network (MMR Inclusion => Sound Tables),
4. Use a TEE

Using an infrastructure level ZKP approach over my MMR actually has a lot of advantages from a product POV. I can deliver a faster/better UX to users without sacrificing on the strong mathematical security assumptions of ZK. This may actually scale better than my MMR approach, since you don’t need to replicate computation and coordinate state updates

This technique adds a new dimension of trade-offs for using SNARKs in production. As someone trying to build a mobile app that uses ZK, I have to compete with web2 in terms of UI/UX. This approach seems more promising than anything on faster SNARKs i’ve seen thus far.

> Would love to see a PoC on this to evaluate the tradeoffs. Also, do you believe it would be possible to get any sort of performance gains by putting big tables in the public inputs? That could be an alternative to circumvent current limit on table sizes for lookup args.

Am working on a POC. It’s actually a simple stupid technique, so won’t take very long…

---

**Hmac512** (2024-02-21):

[github.com](https://github.com/Hmac512/noir-merkle-root-POC-lookup)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/4/c/4ca0dc6c885a52a9c1264fd6bb4a3cccbc91a5e6_2_690x344.png)



###



Noir Merkle Root is a function for calculating merkle root from given inputs. Using Poseidon hash function for hashing.










I bit the bullet. A really naive approach yields a 5x speed up in noir, and the table can be verified by infrastructure in about 2s.

Which is a great sign.

---

**aliatiia** (2024-02-29):

> the oracle to give me a malicious result, I can generate a fraud proof (ZKP or smart contract) in order to claim a reward.
> This works well to prevent the oracle from colluding with someone else. This however fails in the situation where the oracle is also the one requesting the lookup.

A non-trivial amount of the reward (bond) can be **burnt** by the smart contract to eliminate this problem.

---

General note on the approach: if the security assumptions of an optimistic design are to be assumed, why not bypass ZK altogether and just compile the computation into a general-compute VM that has a ~~fraud~~ fault prover (off chain) / fault verifier (onchain). This exists already: EVM/WASM (by Arbitrum) and EVM/MIPS (Optimism)

---

**Hmac512** (2024-02-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> A non-trivial amount of the reward (bond) can be burnt by the smart contract to eliminate this problem.

I’m not following here. If the oracle generates a false table for their own use, then the table would never be made public. In this version the table can be a private input to the circuit.

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> if the security assumptions of an optimistic design are to be assumed, why not bypass ZK altogether and just compile the computation into a general-compute VM

This is a valid point for the MMR approach. It really only makes sense in the cases where:

1. ZK is used for its privacy preserving properties, so you can offload only the insensitive parts to cryptoeconomic security.
2. A fraud proof would be too resource intensive to generate for the whole computation. So it would be easier to split it out into many smaller operations, and you only need to contest the incorrect operations. Would be interesting to apply this to the OP fraud proof game.

—-

Keep in mind the MMR approach isn’t the only variation. Instead infrastructure can zk prove the table validity, and then recursively update the root proof to neutralize the table.

Faster client side proofs is the use case I was driven by, but it goes beyond that.

Take a zkrollup. Right now they are usually monolithic systems. With this technique you could split up proving into separate microservices that can each be optimized for a specific task.

For example, a service can order txs as it seems them in the mempool, and start validating lookup tables for keccak hashes the main prover would need.

It’s a new way to achieve IVC


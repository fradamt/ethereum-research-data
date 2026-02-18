---
source: ethresearch
topic_id: 5994
title: Low-overhead secret single-leader election
author: JustinDrake
date: "2019-08-18"
category: Sharding
tags: []
url: https://ethresear.ch/t/low-overhead-secret-single-leader-election/5994
views: 7861
likes: 18
posts_count: 9
---

# Low-overhead secret single-leader election

**TLDR**: We present a simple secret single-leader election with a per-block overhead of one SNARK plus 32 bytes. (Related posts [here](https://ethresear.ch/t/fork-choice-rule-for-collation-proposal-mechanisms/922), [here](https://ethresear.ch/t/cryptoeconomic-ring-signatures/966), and [here](https://ethresear.ch/t/cryptographic-sortition-possible-solution-with-zk-snark/5102).) Thanks to Kobi Gurkan for helpful discussions.

**Construction**

Let g be an elliptic curve generator. Let v_1, ..., v_k be a list of validators to secretly shuffle for block proposals. Every validator v_i has a permanent public key pk_i as part of their validator record where pk_i = g^{sk_i} for some secret key sk_i. Let n be a nonce, e.g. an election period counter.

To participate in the election a validator v broadcasts (e.g. over Tor) an ephemeral public key epk and a corresponding SNARK proof p with:

- public inputs: pk_1, ..., pk_k, n, epk
- private inputs: sk, i
- statement: pk_i = g^{sk} and epk = g^{H(sk, n)}

After sufficient time for the ephemeral public keys and proofs to be included onchain, the received ephemeral public keys are shuffled using onchain randomness into an ordered list. A validator v then signs the block at position j using the ephemeral secret key esk = H(sk, n) corresponding to the ephemeral public key at position j in the ordered list.

**Onchain overhead**

For concreteness we assume [Groth16](https://eprint.iacr.org/2016/260.pdf), the [BLS12-381](https://electriccoin.co/blog/new-snark-curve/) pairing-friendly curve, and we let g be a [Jubjub](https://z.cash/ru/technology/jubjub/) generator. The onchain overhead is as follows (where 32 bytes is the size of a compressed Jubjub point):

- state: 32 bytes per validator for the permanent public keys
- computation: ~3ms per block for the SNARK verification
- data: 32 bytes per block for the ephemeral public keys plus 127 bytes for the SNARK data

**Offchain overhead**

Notice the circuit complexity is dominated by the single hash computation H(sk, n). If H is a SNARK-friendly hash function (e.g. [MiMC](https://eprint.iacr.org/2016/492.pdf)) we expect the proving time to be ~0.1s on a commodity laptop. If H is SHA256 the proving is ~1s. In the context of Eth2 shard persistent committees, this proving time is marginal relative to the preparation time validators have prior to elections.

To benefit from a universal trusted setup one can use [Sonic](https://eprint.iacr.org/2019/099) instead of Groth16. The main drawback is increased prover time by ~30x. (There are rumours of a “Sonic 2.0” which may bring improvement to prover time. And in general the SNARK stack—proof systems, circuits, prover algorithms, hardware—is rapidly improving.)

Finally, there is overhead from using a private network such as Tor to disseminate the ephemeral public keys and proofs. The concrete overhead is small because the corresponding messages are tiny.

## Replies

**zmanian** (2019-08-19):

This seems like part of the ever expanding class of problems which are solved if we had an accumulator that supports efficient batchable updates and zero knowledge proofs of membership.

---

**dlubarov** (2019-08-21):

To clarify, pk_i would be private when v_i broadcasts epk_i and the proof, correct? If so, it seems like the SNARK would need a proof of inclusion to privately show that pk_i was in the validator set, or maybe I’m misunderstanding?

---

**vbuterin** (2019-08-21):

One could achieve a moderate level of leader secrecy (eg. anonymity set 8-32) by just using a regular linkable ring signature or some bulletproof-based construction, right? And do we *need* anon sets larger than that?

---

**JustinDrake** (2019-08-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> To clarify, pk_i would be private when v_i broadcasts epk_i and the proof, correct?

Correct. More precisely, the validator index i corresponding to epk_i is private. It’s why I chose the notation epk without being explicit about the index. Note that the actual values pk_1, ... pk_k are (as a group) public inputs.

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> the SNARK would need a proof of inclusion to privately show that pk_i was in the validator set

Yes. This is done with the first part of the SNARK statement pk_i = g^{sk}. The SNARK is given the set of validator permanent public keys pk_1, ... pk_k as public inputs, and the specific index i as a private input. (The private input i is technically not necessary. I expect it may allow for a circuit optimisation which avoids looping through the pk_j by using a muxer to select pk_i.)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> One could achieve a moderate level of leader secrecy (eg. anonymity set 8-32) by just using a regular linkable ring signature or some bulletproof-based construction, right?

Right. Having said that, regular linkable ring signatures seem to have worse properties (e.g. larger and slower to verify proofs) than the proposed solution. I want to make more extensive literature research on ring signatures, but so far I could not find anything remotely close to 127+32 = 159 bytes of data and 3ms verification time per proof.

Take Monero as a proxy for evaluating ring signatures in practice. They have a dedicated ring signature research team and I’m assuming they are using state of the art technology. As I understand, their ring size is limited to 11, their transactions are ~10kB in size, and the verification time is tens to hundreds of milliseconds (source [here](https://www.monerooutreach.org/breaking-monero/ring-signatures.php)).

The main downside of the suggested construction from a performance standpoint is prover time. I expect we can easily get <1s (likely ~100ms) prover time. The good news is that, in our specific application, prover time is *not* critical because we can give validators hours of preparation time.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> And do we need anon sets larger than that?

One thing to consider is that, in practice, there are “heuristics” that one can use to partially deanonymise the validator set. For example, one could analyse the timing of packets, and some validators may not even bother using Tor. So my initial gut feel is that 8 is on the low side and that 32 may be fine ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**dlubarov** (2019-08-21):

Oh I see. Yeah a MUX with 32 inputs should be extremely lightweight – just 5 constraints for splitting the index into bits, and 31 constraints for selecting inputs based on the index bits.

I think Merkle proofs would also be reasonable though. BLS12-381 is 255 bits, so the recommended number of MiMC rounds would be 161. Each round is 2 constraints, so 322 constraints per invocation. The additive variant Davies-Meyer would be “free”, so for a tree depth of 16, a Merkle proof would be (322 + 1) * 16 = 5168 constraints.

Sapling is ~100k constraints and was benchmarked at 2.3 seconds (not sure what kind of hardware was used), so I think a proof with 5168 constraints would take something like ~0.12 seconds.

MiMC requires \gcd(3, p - 1) = 1 for cubing to be a permutation, which isn’t the case with Zcash’s curve parameters, but you could generate new parameters, or use x^5 at the cost of an extra constraint per round.

I think Zcash wanted to avoid MiMC for now since it’s relatively new, but maybe the risk would be acceptable for this use case? It seems like the worst case scenario is that an attacker could take over consensus by registering many ephemeral public keys, but at least that could be detected and rolled back.

---

**mathcrypto** (2019-08-29):

Since the exponent 5 adds a 50% overhead (483 constraints per invocation instead of 322), it would be better to use LongsightL-161/p/3 instead of LongsightL-161/p/5 and generate new parameters for the curve as there is no obligation to use Zcash curve. Also, I have seen that Daira from Zcash had suggested to use the Rescue sponge permutation instead of Davies-Meyer as it’s more efficient.

It’s also possible to use exponent 7 instead which is slightly more expensive, but requires fewer rounds. For example, [ethsnarks uses exponent 7](https://github.com/HarryR/ethsnarks/issues/87) with 91 as the number of rounds (instead of 161 in the previous case with exponent 3 or 5). This choice needs 4 constraints per round, so **91*4=364** per invocation when using a round-constants.

---

**mathcrypto** (2019-09-09):

The Single Secret Leader Election Snark protocol proposed [here](https://ethresear.ch/t/cryptographic-sortition-possible-solution-with-zk-snark/5102) suggests to do the following:

**Protocol**

1. Generate N signature pairs pub/priv
2. ∀ pair, we generate a SNARK (since participants have to send proof that they are eligible)
3. We choose one party (hash h) to be the block proposer by picking the one at position m modulo number of participants.
4. The party that was chosen will publish the sig that proves they are the right person.
The other parties verify the sig to verify if  the msg m was actually signed by the corresponding private key.

The circuit verifies:

- that the leaf exists within the merkle tree

```auto
assert root == merkle_authenticate(path_var, address_bits, leaf_hash)
```

- that prover knows the secret (signature) for that hash

```auto
assert eddsa_verify(pk, m, signature)
```

- that prover signed the message m (random beacon)

```auto
assert hash == H(signed(m))
```

**Circuit complexity**

The circuit complexity is dominated by the single hash computation (preimage proof) + merkle proof + signature verification. We can reduce the overhead of the circuit by hashing multiple public inputs into a single variable because the cost of hashing data on-chain is less than each public input. Each hashed input costs 20k gas, whereas every public SNARK input costs 40k gas.

**Merkle proof**

The hash function [MiMC](https://eprint.iacr.org/2016/492) operates over a prime field rather than on bytes and bits and offers the following advantages:

- Minimal multiplicative complexity
- MIMC reduces the number of constraints for a whole merkle tree proof down to fewer than it needs to perform 1 SHA256 operation.
- Easier to work with than Pedersen hashes.
- MIMC let us do potentially transactions per second rather than seconds per transaction.
- Reduces the memory overhead.
- MIMC offers a factor of 10 improvement ( MiMC takes ≈ 7.8 ms while SHA-256 takes ≈ 73 ms)

If we were to use BLS12-381 or Baby_JubJub which is built on top of alt_bn128 in ETHSnarks where each has 255 bits, so the recommended number of MiMC rounds would be 161 with exponent 3.

As I have mentioned in my previous comment, It’s also possible to use exponent 7 instead which is slightly more expensive, but requires fewer rounds so 91 instead of 161. This choice needs 4 constraints per round, so  **91*4=364**  per invocation when using a round-constants.

For a tree depth of 16, a Merkle proof would be (364 + 1) * 16 = **5840 constraints**.

We can also reduce the hashing down to under 100 constraints by using poseidon hash function family instead.

**Signature verification**

The eddsa (Ed25519) has the following advantages over other signature schemes:

- Avoid side-channel attacks on signing.
- Avoid attacks on ECDSA based on not-perfectly-random nonces
- Reduce reliance on collision resistance for the message hashing
- Small public keys (32 bytes), small private keys(32  bytes) and small signatures(64 bytes) with high security level at the same time (128-bit).
- The EdDSA algorithm is slightly faster than ECDSA.

Checking is a signature is valid for eddsa (with baby jubjub curve) takes about [~10k constraints](https://ethresear.ch/t/question-for-cryptographers-snark-friendly-signature-protocol/4645/8) in ethsnarks, from which 1881 constraints for the Pedersen hash used. There are several checks that we can dismiss to optimise the verification time like checking if a point is on a curve and is not of low order which currently takes 5415 constraints which would leave us with 7000 constraints plus the hash complexity.

**Preimage proof**

By using MIMC function, we avoid the bits<->field-element conversion at every step, if the initial input is bits it requires one constraint (in addition to validating that the inputs are bits), but the whole chain avoids an extra ~255 constraints at every level because no additional checks are required at each step especially in the case of Merkle proof.

The total complexity of preimage proof is **366 constraints**

```auto
def preimage_check(Hash,M):

compute H(M) # 364 constraints using MIMC
Hash == H(M) # 2 constraints
```

** Proving time **

The total complexity is 364 + 10k + 5840 = 16204 constraints (before applying optimisation to eddsa verification). On a laptop with 8 GB of ram proofs can be made in ~2 to 3 seconds which is less than the slot period (6 seconds).

---

**nikkolasg** (2020-02-01):

One thing that eludes most readings about SSLE is how to guarantee fairness:

" a leader should be elected in proportion to its stake / power in the network "

In this case, the shuffling will give uniform probability of being selected right ? It seems using a weighted RNG could bring us closer to get fairness, but the question on how to create the weighted list in the first place in zero knowledge seems tedious…

Seems like that’s what [BEHG20](https://eprint.iacr.org/2020/025.pdf) proposes for their DDH based scheme but it’s unclear how to do that zk ? Otherwise it seems it reveals the associated power, so it doesn’t sound anonymized at all. As well, I got the impression that it requires a drastically huge list now to get a fine grain level on the power.


---
source: ethresearch
topic_id: 3477
title: On-chain scaling to potentially ~500 tx/sec through mass tx validation
author: vbuterin
date: "2018-09-22"
category: Applications
tags: [zk-roll-up]
url: https://ethresear.ch/t/on-chain-scaling-to-potentially-500-tx-sec-through-mass-tx-validation/3477
views: 82455
likes: 119
posts_count: 83
---

# On-chain scaling to potentially ~500 tx/sec through mass tx validation

We can actually scale asset transfer transactions on ethereum by a huge amount, without using layer 2’s that introduce liveness assumptions (eg. channels, plasma), by using ZK-SNARKs to mass-validate transactions. Here is how we do it.

There are two classes of user: (i) transactor, and (ii) relayer. A relayer takes a set of operations from transactors, and combines them all into a transaction and makes a ZK-SNARK to prove the validity, and publishes the ZK-SNARK and the transaction data in a highly compressed form to the blockchain. A relayer gets rewarded for this by transaction fees from transactors.

The system is managed by a contract, whose state consists solely of two `bytes32` values representing Merkle roots: address book (A) and balances+nonces (B). A starts off as a Merkle root of 2^{24} zero entries, and B as a Merkle tree of 2^{24} (0, 0) tuples.

There are three types of operations for transactors: (i) registration, (ii) deposit/withdraw and (iii) sending.

To register, a user needs to provide a Merkle branch showing some index i, where either `i=0 and A[i]=0`, or `i > 0 and A[i] = 0 and A[i-1] != 0`. The Merkle tree is updated so that `A[i]` now equals the msg.sender’s address, and the Merkle branch is logged so that a client reading logs can get all of the data they need to create their own Merkle branches.

To deposit or withdraw, a user needs to provide a Merkle branch showing some index i, where `A[i]` equals the msg.sender’s address, along with the corresponding branch for `B[i]`, and the amount they want to deposit or withdraw, `D` (negative for withdrawals). The contract checks that `B[i][0] + D >= 0`. If `D > 0`, it verifies that (if the system is for ETH) `msg.value == D * 10**12` (ie. the base unit of the system is 10^{-6} ETH) or otherwise calls `transferFrom(msg.sender, self, D * 10**12)` to the appropriate ERC20 token contract. If `D < 0`, it sends the ETH or token to `msg.sender`. The contract then updates the Merkle root so that `B[i][0] += D`. Note that for efficiency, we can combine together the registration and deposit steps for not-yet-registered transactors.

To send, a user constructs the data: from address index (3 bytes), to address index (3 bytes), amount (ETH’s ~100m supply requires 47 bits, so we can say 6 bytes, but most of the time <=4), fee (one byte floating point, top 5 bits are exponent, bottom 3 are mantissa), nonce (2 bytes). The user broadcasts (from, to, amount, fee, nonce) plus a signature.

A relayer can gather together many of these operations, and create a ZK-SNARK proving that, when processing all of the operations in sequence, at that start of each operation `B[from][0] >= amount + fee`, `B[from][1] == nonce` and that a valid signature is known from `A[from]`, and then updating the Merkle root with `B[from][0] -= amount + fee`, `B[to][0] += amount`, `B[relayer][0] += fee`, `B[from][1] += 1`. A log is issued to alert users that the transaction is a payment batch transaction and they would need to recompute their Merkle tree witnesses.

The cost of a ZK-SNARK verification with the latest protocols is ~600000 gas, and we can add ~50000 gas for overhead (base tx cost, log cost, storage slot modifications…). Otherwise, each transaction included costs 68 gas per byte, unless it is a zero byte in which case it goes down to 4 gas. Hence, for a regular transfer, we can expect the marginal cost to be 68 * 3 (from) + 68 * 3 (to) + 68 * 1 (fee) + 68 * 4 + 4 * 2 (amount) + 68 * 2 (nonce), or 892 gas. In the best case, a relay transaction would consume a block’s full 8 million gas, so the marginal costs could take up ~91% of the total costs, so the total cost would be < 1000 gas per transaction, a gain of ~24x for ETH transactions and ~50x for ERC20 transfers. In practice, it would be more at first, as while the system has low volume users would prefer faster smaller batches even at higher cost per transaction over slower larger batches, but once the system gets to high volume, it should be able to get efficiency levels close to this.

Note that anyone can be a relayer; there is no assumption of even an untrusted special “operator” existing. Because all the data needed to update the Merkle tree goes on chain, there are no data availability issues.

We can optimize further by allowing a relayer to (with ZK-SNARKs proving the operation) rebalance the tree, moving more frequent users into lower indices, changing the encoding for the value so that common values (eg. round numbers of ETH) are represented, and changing the nonce scheme so that, for example, details in the signature change every 100 blocks and so the nonce can reset every 100 blocks.

## Replies

**shamatar** (2018-09-22):

[@vbuterin](/u/vbuterin)

Good day, Vitalik.

Posting block in the logs is a great approach, although I may add the following points for clarification.

- To actually verify that what was posted in logs corresponds to the state update that is proved by a zkSNARK you have to include every field of the transaction as a public input to the snark verification. It is an extra one point multiplication per input parameter. If the transaction is short you can pack and reduce this number of inputs, but still, right now it’s 40000 gas per multiplication in G1 of BN256.
- As an alternative you can make only a sparse merkle tree of all transaction as a public parameter and include this root as a public input. In this case a sponsored MiMC calculation on-chain is required or a internal R1CS grows (~ 25000 constraints per SHA256, and assuming 1000 transactions per proof it’s 25 million constrains for a block merkle root only).

---

**vbuterin** (2018-09-22):

> To actually verify that what was posted in logs corresponds to the state update that is proved by a zkSNARK you have to include every field of the transaction as a public input to the snark verification. It is an extra one point multiplication per input parameter. If the transaction is short you can pack and reduce this number of inputs, but still, right now it’s 40000 gas per multiplication in G1 of BN256.

Right, I forgot about this. I would say make a simple hash of the inputs be a public parameter, along with the inputs, and verify the hash on chain (SHA3 is 6 gas per 32 bytes, so ~3 gas per operation). The data must be public and verified to chain to avoid data availability issues (if the data is non-public, then you’ve basically created a Plasma chain, and at that point you need some trust in the operator for liveness).

And yes, I understand that the above requires some quite heavy duty computing work on the part of the relayers. But at this point it’s widely known that optimizing SNARK/STARK provers is super-important so I’m sure there will be more and more software engineering work going into it over time.

---

**shamatar** (2018-09-22):

Thank you, Vitalik.

I’ve just wanted to clarify this point and express a concern about internal zkSNARK size that makes a proof calculation quite demanding on resources.

---

**vbuterin** (2018-09-22):

I know there has been work recently on generating large ZK-SNARKs in clusters. I think in the long run, proof generation will in many cases be done by a specialized class of “miners” running GPUs and more specialized hardware. I would definitely love to see data from someone trying to make a full scalable implementation! The nice thing about the scheme is that it’s not vulnerable to 51% attacks, so if bitmain ends up producing 90% of the proofs that’s totally fine, as long as there is someone to step in and take their place if they suddenly stop participating.

---

**barryWhiteHat** (2018-09-22):

> The cost of a ZK-SNARK verification with the latest protocols is ~600000 gas, and we can add ~50000 gas for overhead (base tx cost, log cost, storage slot modifications…). Otherwise, each transaction included costs 68 gas per byte, unless it is a zero byte in which case it goes down to 4 gas.

I think you need to pass the transactions to the sanrk as a public input?

If so I think this is quite expensive as during zksnark verification you need to do a [pairing addition and pairing multiplication](https://github.com/barryWhiteHat/roll_up/blob/master/contracts/Verifier.sol#L81) per public input. I found this out after we spoke last. With roll_up where we pass two 32 bytes input per tx we can only have 22 public inputs before we run out of gas.

So we have thought a bunch about how to overcome this at roll_up. We originally wanted to pass every leaf that is updated as a public input. But we can only do 22 transactions or 44 inputs, tho we were not using the latest snark verification method.

So we started thinking about this and thought about making a merkle tree of the public inputs and pass that. Pass all the other inputs privately (which is free) and then build the same merkle tree inside the snark and ensure that they match.

But the problem with this is that if you use sha256 which is cheap in the EVM it gets very expensive inside the snark in terms of proving time. If you use pedersen commitments it is very cheap in the snark but you pay a lot more in the evm, (we think atleast i have not gotten around to testing that yet :/) .

There are some very interesting proposals for hash functions that are cheap inside the snark and the evm see [@HarryR](/u/harryr) mimic based [construction](https://github.com/HarryR/ethsnarks/pull/42) but that needs some academic review before i think we can safely use it. So that could be useful for compressing the public input.

---

**PhABC** (2018-09-22):

> To register, a user needs to provide a Merkle branch showing some index i, where either  i=0 and A[i]=0 , or  i > 0 and A[i] = 0 and A[i-1] != 0 . The Merkle tree is updated so that  A[i]  now equals the msg.sender’s address,

This seems to only allow 1 registration per block in practice. If both Bob and Alice try to update the same Merkle root for slot `i`, then one will fail.

> To deposit or withdraw, a user needs to provide a Merkle branch showing some index i, where  A[i]  equals the msg.sender’s address, along with the corresponding branch for  B[i] , and the amount they want to deposit or withdraw,  D… The contract then updates the Merkle root so that  B[i] += D .

This also seems hard to achieve in practice, since users technically always need to know what the current root is in order to provide the proper path and the root changes with every transaction.

> Note that anyone can be a relayer; there is no assumption of even an untrusted special “operator” existing. Because all the data needed to update the Merkle tree goes on chain, there are no data availability issues.

This also has the problem that having multiple relayers will lead to collisions and only one will succeed. This introduce a race condition to generate the proof, which can be fine, but now relayers might start to only include the highest fees to make sure they don’t lose the race, so higher cost for everyone.

I believe most of these concerns are addressed by having an operator or close set of operators and a deposit/withdraw queue.

---

**kladkogex** (2018-09-22):

I think you need to provide analysis for double spend attacks - what if there are multiple relayers, and you try to double spend by going through two relayers concurrently?

When you deposit do you deposit to a single relayer or multiple relayers?

---

**PhABC** (2018-09-22):

AFAIK, you can’t double spend since the root will update to reflect the new state and all txs need to be sequentially processed and be valid.

---

**kladkogex** (2018-09-22):

I wonder if this is similar to what I proposed sometime ago ;-)) I did not have zksnarks in it  though )



    ![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png)

      [Plasma Cash without any blockchain at all](https://ethresear.ch/t/plasma-cash-without-any-blockchain-at-all/1974) [Plasma](/c/layer-2/plasma/7)




> It seems that if coins are indivisible/immutable, then one can have Plasma Cash as a simple Merkle tree without having any blockchain.  The reason for this is that since the coins are immutable,  there is no need for global transaction ordering/consensus.  For a particular coin you only need its history and other coins are irrelevant. Therefore,  a blockchain  may be an overkill
> Here is a quick sketch of how this could work - comments are welcome
>
>
> Each coin-chain is a linked list of ECDSA sig…

---

**MrChico** (2018-09-22):

Wouldn’t transactors need to include a nonce as well?

---

**kfichter** (2018-09-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The contract then updates the Merkle root so that B[i] += D .

There’s an edge case here for ERC20s where the value received via `transferFrom` is less than `D`. Not huge, but something to consider for implementation.

---

**kfichter** (2018-09-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Hence, for a regular transfer, we can expect the marginal cost to be 68 * 3 (from) + 68 * 3 (to) + 68 * 1 (fee) + 68 * 4 + 4 * 2 (amount), or 756 gas.

We might be able to get away with only having the transaction info in calldata, but otherwise logs would add another 8 gas per byte. Maybe worth having it in the marginal cost (instead of the 50k overhead) since it scales with the number of txs.

---

**vbuterin** (2018-09-22):

> I think you need to pass the transactions to the sanrk as a public input? If so I think this is quite expensive as during zksnark verification you need to do a pairing addition and pairing multiplication  per public input. I found this out after we spoke last. With roll_up where we pass two 32 bytes input per tx we can only have 22 public inputs before we run out of gas.

This is why I suggested putting using hash of the submitted data as the public input, and then computing the hash on chain as that is only 6 gas per 32 bytes for SHA3 (for SHA256 it’s somewhat more but still tiny). FWIW I do agree this whole thing is expensive in terms of prover time, though given that I expect the relayers will be GPU farms so it’s less of an issue than it is in, say, zcash where regular nodes need to be able to make proofs in a few seconds.

> This seems to only allow 1 registration per block in practice. If both Bob and Alice try to update the same Merkle root for slot i , then one will fail.

An alternative is to allow relayers to batch Merkle proofs, though they would not be able to be paid for registrations. Topups and withdrawals can definitely be done through relayers in a way where the relayers get paid though.

> This also has the problem that having multiple relayers will lead to collisions and only one will succeed. This introduce a race condition to generate the proof, which can be fine, but now relayers might start to only include the highest fees to make sure they don’t lose the race, so higher cost for everyone.

One option would be to require relayers to reserve the chain for a period of 2 blocks (possibly <30000 gas cost) before they can submit a block.

> I believe most of these concerns are addressed by having an operator or close set of operators and a deposit/withdraw queue.

By “queue” do you mean “everyone pre-submits what address they’ll register with, and then that gets put in a queue, and then people have to submit a second transaction to make the Merkle branch, but they’ll do that knowing in advance exactly what Merkle branch they’ll need”? If so I do agree that’s another elegant way to solve the problem.

> I wonder if this is similar to what I proposed sometime ago ;-)) I did not have zksnarks in it though )

This scheme is definitely not Plasma. Plasma relies on liveness assumptions and an exit mechanism; there are none of those features here.

> Wouldn’t transactors need to include a nonce as well?

Ah yes you’re right. Will update asap.

> There’s an edge case here for ERC20s where the value received via transferFrom is less than D . Not huge, but something to consider for implementation.

If the value receives is less than D, then the entire transaction should fail. Actually, is it even legal according to the standard for a `transferFrom` request asking for D coins to return less than D coins?

> We might be able to get away with only having the transaction info in calldata, but otherwise logs would add another 8 gas per byte. Maybe worth having it in the marginal cost (instead of the 50k overhead) since it scales with the number of txs.

Not need to log the data. Just have a log pointing out that a relay transaction was made, an assert to check that the relayer is an EOA, and then clients can scan through the block data.

---

**nickjohnson** (2018-09-22):

Is it actually practical to do ECRecover in a snark? Wouldn’t that require an extremely complex snark circuit?

---

**vbuterin** (2018-09-22):

With the [baby jubjub](https://github.com/barryWhiteHat/baby_jubjub_ecc) curve, it might actually not be that bad.

---

**PhABC** (2018-09-22):

Checking is a signature is valid for eddsa (with baby jubjub curve) takes about 200k constaints in roll_up, which is maybe 30 seconds to build a proof on a decent laptop. This can most likely be brought down quite a bit still however. Using secp2561curve will be more computationally demanding

---

**vbuterin** (2018-09-23):

400k seems incredibly high. Why is that? If we use schnorr verifying a signature is just two multiplications, an addition and a hash, so on average ~769 additions and a hash, so it seems like the hash would be the largest part of it.

---

**PhABC** (2018-09-23):

Sorry, I meant 200k, I just edited previous comment. Roll-up currently uses full-rounds of SHA256, so we could cut the number of contraints here almost by half for the hash function. Otherwise, there are a lot of checks done currently that might not be necessary.

Here’s where the contraints are built for the signature validation ;


      [github.com](https://github.com/barryWhiteHat/baby_jubjub_ecc/blob/620dbb661a8a24b29eb92fd488201b988609db9e/baby_jubjub_ecc/eddsa.cpp#L127)




####

```cpp

1. jubjub_isOnCurve2.reset( new isOnCurve  (pb, r_x_packed[0], r_y_packed[0], a, d, "Confirm r point is on the twiseted edwards curve"));
2.
3. jubjub_pointMultiplication_lhs.reset( new pointMultiplication  (pb, a, d, b_x, b_y, S, lhs_x, lhs_y, " lhs check ", 256));
4. jubjub_pointMultiplication_rhs.reset( new pointMultiplication  (pb, a, d, pk_x_packed[0], pk_y_packed[0], h_bits, rhs_mul_x, rhs_mul_y, "rhs mul ", 253));
5. jubjub_pointAddition.reset( new pointAddition  (pb, a, d, rhs_mul_x[252], rhs_mul_y[252] , r_x_packed[0] , r_y_packed[0], rhs_x, rhs_y , "rhs addition"));
6. }
7.
8.
9.
10. template
11. void eddsa::generate_r1cs_constraints()
12. {
13.
14. //constraint the inputs a,d , x_base, y_base
15. //we make sure that the user passes the curve values
16. this->pb.add_r1cs_constraint(r1cs_constraint({a} , {1}, {168700}),
17. FMT("a == 168700", "eddsa"));
18. this->pb.add_r1cs_constraint(r1cs_constraint({d} , {1}, {168696}),
19. FMT("d == 168696", "eddsa"));
20.
21. this->pb.add_r1cs_constraint(r1cs_constraint({b_x} , {1}, {FieldT("17777552123799933955779906779655732241715742912184938656739573121738514868268")}),

```

---

**barryWhiteHat** (2018-09-23):

> FWIW I do agree this whole thing is expensive in terms of prover time, though given that I expect the relayers will be GPU farms so it’s less of an issue than it is in, say, zcash where regular nodes need to be able to make proofs in a few seconds.

In the case where you use a GPU farm to perform the proving step do you also need a GPU farm to perform the trusted setup? How do the two operations differ in complexity?

> 400k seems incredibly high. Why is that? If we use schnorr verifying a signature is just two multiplications, an addition and a hash, so on average ~769 additions and a hash, so it seems like the hash would be the largest part of it.

I use sha256 in a bunch of places because i was unsure what was safe to combine points or remove discard data. But when i optimize it we should be able to come down quite a lot. Its POC at the moment.

---

**gluk64** (2018-09-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> for a regular transfer, we can expect the marginal cost to be 68 * 3 (from) + 68 * 3 (to) + 68 * 1 (fee) + 68 * 4 + 4 * 2 (amount) + 68 * 2 (nonce), or 892 gas.

The correct sum is slightly higher: 68 * 3 (from) + 68 * 3 (to) + 68 * 1 (fee) + **68 * 4 * 2** (amount) + 68 * 2 (nonce), or **1156** gas. A more realistic assumption for the foreseeable future is 1000 tx per SNARK (according to very optimistic calculations we had with the rollup team). So it adds roughly 650 overhead, bringing us to ~1.8k gas per tx.

A batched transfer of tokens with the same parameters (32 bit value, 24 bit address) will cost around 18k gas per transfer. So it’s 10x, not 50x.

10x gas reduction is an order of magintude improvement, of course, but it has a relatively strong cap, and the economic overhead imposed by the SNARK proof computation is also very signficant at the moment. Especially the need to compute hashes optimized for verification in EVM.

Solving the data availability problem through relying on the Ethereum root chain not as 100% data availability guarantor, but rather as the court of the final appeal seems a lot more promising direction, because: 1) it can scale almost indefintely, 2) it simplifies the SNARK circuit, making transfers cheaper and a working MVP a more attainable goal. See [our discussion in the roll_up github](https://github.com/barryWhiteHat/roll_up/issues/15).


*(62 more replies not shown)*

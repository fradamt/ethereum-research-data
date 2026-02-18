---
source: ethresearch
topic_id: 12677
title: MEV-resistant ZK-Rollups with Practical VDE (PVDE)
author: zeroknight
date: "2022-05-20"
category: Layer 2
tags: [mev, zk-roll-up]
url: https://ethresear.ch/t/mev-resistant-zk-rollups-with-practical-vde-pvde/12677
views: 21030
likes: 41
posts_count: 19
---

# MEV-resistant ZK-Rollups with Practical VDE (PVDE)

# MEV-resistant ZK-Rollups with Practical VDE (PVDE)

*[@zeroknight](/u/zeroknight) , [@0xTariz](/u/0xtariz) , and [@radzin](/u/radzin) from [Radius.xyz](https://twitter.com/RadiusXyz)*

## Abstract

Current MEV solutions based on time-lock puzzles are not viable. Operators cannot easily detect invalid time-lock puzzles or transactions, which can even lead to DoS attacks. We are designing an MEV-resistant ZK-Rollup with a *practical* approach to MEV minimization using Practical Verifiable Delay Encryption (PVDE). This method generates zk proofs within 5 seconds, a validity proof needed to prove that solving the time-lock puzzles will lead to the correct decryption of valid transactions.

---

---

## Background & Motivation

### Decentralization Is Disguised

The *structure* of a blockchain is fully decentralized, but the *content* of each block is not.

MEV attacks occur from revealed transaction data and the *centralization* of miners who see the *contents* of block transactions and decide which transactions are included in a block. By leveraging their power to censor and reorder block transactions, miners can perform front-running, back-running, or sandwiching attacks to extract profit from users. The problem is that most users are unaware of being the victim of these malicious attacks.

In L1, block-building competitions among miners of different blockchains and high gas fees can prevent MEV exploitations from miners/attackers. Proposer/Builder Separation (PBS) is another proposed solution for MEVs in L1s, but users’ assets are still prone to attacks as MEV opportunities are still publicized in a decentralized way.

In L2s, the case is a bit different. If the operator correctly computes the state transitions and includes only valid transactions, it becomes difficult to detect the censorships or intentional reorderings as only the computational integrity is verified. This creates a debate to the centralization/decentralization dichotomy. Due to the limited nature of blockchain scalability, L2 needs to maintain a small number of operators for its scalability which allows more room for operators to extract MEV profit. Additionally, lower gas fees on L2s attract mempool searchers (attackers) to MEV attacks.

We must assume that operators work in a *permissionless* manner to ensure a transparent and safe L2 ecosystem. A grounded approach that prevents the manipulation of blocks by the centralized operators in L2 is therefore needed. *If there is no inherent solution to control the significant power of operators,*

> The adoption of layer 2 scaling solutions could represent the centralization of control over assets stored within them. — barryWhiteHat

[MEV auctions](https://ethresear.ch/t/mev-auction-auctioning-transaction-ordering-rights-as-a-solution-to-miner-extractable-value/6788) were proposed as a scheme to decentralize the operators. But as [barryWhiteHat](https://ethresear.ch/t/against-proof-of-stake-for-zk-op-rollup-leader-election/7698) mentions, we need to be more cautious in the way we elect the operators through consensus mechanisms or with economical schemes like PBS as the security of L2s might very well be served. To prevent the users’ assets from being exposed to MEV profits, we propose a *complete* privacy method for MEV minimization.

---

### Time-lock Puzzle

Our MEV-resistant L2 solution ensures *complete* privacy of transactions as it reveals the contents of the transaction only after the transaction order is determined by the operator. We achieve this by encrypting the transactions temporarily based on time-lock puzzle. This scheme delays the time for the operator to find the symmetric key used to decrypt the transaction.

**[Create and Encrypt Time-lock Puzzle]**

The trader generates a time-lock puzzle that finds the symmetric key, then encrypts the transaction using the symmetric key.

1. Create time-lock puzzle

Generate a modulus: N = p*q
2. Select generator: g\in G, \ \ where\ \ G \ \ is \ \ RSA \ \ group
3. Compute symmetric key: S_K = g^{2^T} \ \ mod \ \ N

Encrypt transaction

1. Generate a symmetric key on an elliptic curve

k = (k_0, k_1) \leftarrow JubJubAffine(S_K) \in F^2_q
2. Encrypt message with Poseidon encryption scheme: C_{TX} = ENC(k, TX)

**[Solve and Decrypt Time-lock Puzzle]**

The operator receives the time-lock puzzle from the trader and solves it to find the symmetric key, then decrypts the transaction using the symmetric key.

1. Solve time-lock puzzle

Receive public parameter: N, T
2. Compute symmetric key: S_K = g^{2^T} \ \ mod \ \ N

Decrypt cipher text

1. Generate a symmetric key on an elliptic curve

k = (k_0, k_1) \leftarrow JubJubAffine(S_K) \in F^2_q
2. Decrypt message with Poseidon encryption scheme: TX = DEC(C_{TX}, k)

---

### Practical Verifiable Delay Encryption (PVDE)

Time lock puzzle schemes require large computational resources from operators. If a trader  sends an invalid puzzle to the operator, resources are largely and meaninglessly wasted which can also lead to DoS attacks by malicious traders.

To prevent this, the trader must generate a zk proof to prove the integrity of the time-lock puzzle before the operator solves the puzzle.

The trader’s statement is as follows:

> \pi_{PVDE}: The output value (also the symmetric key used for the decryption of the encrypted transaction) is found by computing the time-lock puzzle $2^t$times

The circuit must include the two computations to prove the statement:

1. Time-lock puzzle: g^{2^{T}} mod \ \ N  = S_K
2. Poseidon Encryption: ENC(TX, S_K) → C_{TX}

It is difficult to solve the current RSA-based naive time-lock puzzle inside the zk circuit. For the past few months, we have been working to find a solution to the RSA sequential computation inside the zk circuit, with the help of Ethereum Foundation. To do this, we designed a total of 4 circuit computations and measured the proof generation time.

**Our Practical Verifiable Delay Encryption (PVDE) method successfully generates the zk proof for the RSA-based time-lock puzzle within 5 seconds. This is an applicable and practical approach to generating the proof, which proves that solving the time-lock puzzle will lead to the correct decryption of valid transactions.**

See the results of the experiment below. A more detailed experiment methods and results with the algorithm will be revealed on ethresear.ch.

*Many thanks to [@barryWhiteHat](/u/barrywhitehat)  and [@Wanseob-Lim](/u/wanseob-lim)  from Ethereum Foundation*

**Spec**

- CPU: 2-way E5-2683 v4 (2.1GHz, 16-core)
- RAM: 64 GB
- Storage: 512 GB (SSD)

[![1](https://ethresear.ch/uploads/default/optimized/2X/5/52b17e0fb6c0a9e4ae87b51ce9fece9ee65de7e0_2_690x81.png)1898×106 10.3 KB](https://ethresear.ch/uploads/default/52b17e0fb6c0a9e4ae87b51ce9fece9ee65de7e0)

**Circuit design (RSA: 2048 bits, T: 32678)**

*(When T is set to 32678, the operator solves the time-lock puzzle g^{2^T} in 7 to 8 seconds.)*

1. Naive time-lock puzzle

Proving time: N/A
2. Scheme

g^{2^{T}} mod \ \ N  = S_K

Trapdoor time-lock puzzle

1. Proving time: N/A
2. Scheme

Select random prime number p,q
3. Compute trapdoor \phi(N) = (p-1)(q-1)
4. 2^T \ \ mod \ \ \phi(N) = r
5. g^r \mod \ \ N = S_K

Efficient time-lock puzzle (our new scheme)

1. Proving time: 540 secs
2. Scheme

generate parameters via a trusted setup : (g, g^{2^T})
3. choose a random secret s (128 bits)
4. generate inputs for zk-SNARKs  (s_1, s_2) \leftarrow (g^s,(g^{2^T})^s)

s_2 is used as a symmetric key and can be obtained via (s_1)^{2^T}

generate a validity proof \pi \leftarrow \Pi.prove(g, g^{2^T}, s_1; s, s_2)
verify the proof r \leftarrow \Pi.verify(\pi, g, g^{2^T}, s_1)
obtain the symmetric key via time lock puzzle : (s_1)^{2^T} = S_K

PVDE (our new scheme)

1. Proving time: 5 secs
2. Scheme: Combined zk-SNARK and sigma protocol

---

---

## Participants

We design a ZK-Rollup solution to MEV exploitations caused by the centralization of operators producing the contents of the block and prevent the traders’ transactions and assets from being exposed to the attackers.

---

### Trader

Traders are parties that generate and execute L2 transactions.

To prevent assets from being exposed to the operators, the trader encrypts the transaction, then sends the time-lock puzzle, encrypted transaction, and zk proof to the operator.

1. Generate a transaction
2. Encrypt the transaction with the symmetric key generated with the time-lock puzzle
3. Generate a zk-SNARK proof to verify the integrity of the time-lock puzzle and the encrypted transaction
4. Send the time-lock puzzle, encrypted transaction, and zk proof to the operator

---

### Operator

Operators are parties that collect and execute L2 transactions.

Operators can censor and intentionally reorder the traders’ transactions to extract additional profit for themselves. To prevent these malicious MEV activities, operators must determine the block transaction order and send the corresponding commitment to the trader before they can decrypt the transactions and see the contents.

1. Verify that the trader’s time-lock puzzle is valid
2. Start solving the time-lock puzzle to find the symmetric key (sequentially compute 2^T)
3. At the same time, determine the block transaction order and send the corresponding commitment to the trader. This should be completed before solving the time-lock puzzle
4. Decrypt the transaction using the symmetric key and execute the transactions in the commitment

---

---

## Architecture

[![2](https://ethresear.ch/uploads/default/optimized/2X/3/37e6fdaa6fdfeaf9c05433374745a19d67b36950_2_690x388.jpeg)2960×540 41.9 KB](https://ethresear.ch/uploads/default/37e6fdaa6fdfeaf9c05433374745a19d67b36950)

**Phase 1. Trader Generates Puzzle**

1. Generate a transaction
2. Generate symmetric key with time-lock puzzle, encrypt the transaction, then generate validity proofs for the puzzle

Setup(Λ) → pp = (g, N, T)
3. Generate_puzzle(pp, TX) → (ENC_{tx}, \pi_{PVDE})

 Time-lock_puzzle(pp) → S_K
 S_K = g^{2^T} \ \ mod \ \ N
4. Encryption(S_K, TX) → C_{TX}
 C_{TX} = ENC(S_K, TX)
5. Generate_proof(pp,TX) → \pi_{PVDE}

Trader sends the following to the operator:

1. Public parameters of time-lock puzzle
2. Encrypted transaction: C_{TX}
3. Transaction hash value: Hash(TX)
4. \pi_{PVDE}

**Phase 2. Operator Determines Transaction Order**

1. Trader verifies the validity of time-lock puzzle. If true, go to step 2.

Verify(\pi_{PVDE}) → {True, False}

Operator starts computing Timelock_puzzle to find the symmetric key for the decryption of the transaction

1. Timelock_puzzle(pp)

Determine the order of the transaction using Merkle Mountain Range(MMR) and send the commitment with *order* to the trader

1. MMR(Hash(TX)) \rightarrow Commit(order, Hash(TX), merkle \_\ root, merkle\_\ path)

**Phase 3. Trader Confirms Order**

1. Trader receives the commitments and checks the order of the transaction, then confirms that the time to receive the commitment was less than the minimum time-lock puzzle computation time

Confirm that the transaction is included in Commit(order, Hash(TX), merkle \_\ root, merkle\_\ path)
2. Check: T_{response}  - T_{order}

**Phase 4. Operator Decrypts Transaction and Executes**

1. Operator solves the symmetric key with time-lock puzzle and decrypts the transaction

 Solve_puzzle(pp, C_{TX}) → TX

 Timelock_puzzle(pp) → S_K
 S_K = g^{2^T} \ \ mod \ \ N
2. Decryption(N, ENC_{tx}, S_K) → TX
 TX = DEX(C_{TX}, S_K)

Transactions are executed in the order determined by MMR

---

---

## Open For Discussion

The problem of MEV is the *centralization* of operators: the trader’s transactions and assets are pre-exposed to the operators in L2s. And as stated above, it is not possible to detect the censorships and intentional reorderings of transactions in L1s.

Our architecture is designed so that operators produce the block contents with encrypted transactions to prevent the traders’ transactions and assets from being pre-exposed. The operators then need to send the finalized transaction commitments to the traders. Traders can challenge operators that did not execute the finalized order of transactions.

Our team is also discussing ideas to verify the true fairness of operators on L1 - we’d be happy to discuss this with the [ethresear.ch](http://ethresear.ch) community!

---

### Order Commitment Validity

[![3](https://ethresear.ch/uploads/default/optimized/2X/8/84506bb32cbcfe2e12af748dada325f44c26ee47_2_690x388.jpeg)3960×540 46.3 KB](https://ethresear.ch/uploads/default/84506bb32cbcfe2e12af748dada325f44c26ee47)

Order commitment validity ensures the L1 verifier contract validates that the operator executed the transactions in the determined order and finalizes the state without any challenges from the trader.

1. Trader checks the order of the transactions in the commitments and confirms that the time to send the commitment was less than the minimum time-lock puzzle computation time

Use membership proof to check that the trader’s transaction is included in Commit(order, Hash(TX), merkle \_\ root, merkle\_\ path)
2. Check: T_{response} - T_{order}

Send signature to operator: Sig(Commit(order, Hash(TX), merkle \_\ root, merkle\_\ path)
Operator collects trader’s signatures and generates **confirmation stat**e in the order response time
Operator solves the time-lock puzzle and decrypts the transaction, then collects the transactions by the order and generates block proposal state

1. Solve_puzzle(pp, C_{TX}) → TX

 Timelock_puzzle(pp) → S_K
 S_K = g^{2^T} \ \ mod \ \ N
2. Decryption(N, ENC_{tx}, S_K) → TX
 TX = DEX(C_{TX}, S_K)

Block proposal state: TX, Commit(order, Hash(TX), merkle \_\ root, merkle\_\ path)

Operator executes the decrypted transaction and generates zk proof to validate computational integrity on L1. Check the following two conditions in the circuit when generating zk proof:

1. Confirm transaction validity
2. Confirm that both order and Hash(TX) in both confirmation state and block proposal state are same

When the state transition is complete, operator sends the new state and the validity proof to L1 verifier contract
L1 verifier contract validates the computational integrity and order integrity using the  validity proof and finalizes the state

---

---

## Conclusion

MEV results in huge financial losses for traders. Thus, a solution to MEV minimization is imperative at current state. Our PVDE scheme is a practical approach to encrypt transactions using time-lock puzzles, so that operators do not waste any computational resources that lead to DoS attacks. The MEV-resistant ZK-rollup solution will fully prevent MEV attacks using cryptographic methods and eliminate the centralization of operators to provide a fair and efficient trading environment.

## Replies

**MicahZoltu** (2022-05-20):

This is perhaps a naive question, and I’ll admit I didn’t read this whole document, but is it possible to have multiple transactions from multiple parties encrypted such that they can be decrypted using a single VDF output?  The idea here would be that block producers could be required to compute the VDF output for a given block and submit the result along with the block.  Transactions could then be ordered prior to the block that reveals the VDF result, and mined after that block.

Caveats around VDF difficulty tuning being hard.

Note: This works much better in a PoS world where block producers know when their turn is in advance, and they can start calculating the VDF result for *their* block some amount of time prior to it being their turn.  We can naively use the `RANDAO` of `n` blocks back as a seed for this (caveats around RANDAO being known to some actors prior to it being publicly available, so VDF difficulty tuning becomes even harder).

---

**0xTariz** (2022-05-20):

Thanks for your feedback ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=10)

We have analysed a scheme similar to what you’ve mentioned above and we’re planning to dive deeper into this along in our roadmap.

Here’s the research paper we analysed: https://eprint.iacr.org/2021/1293.pdf

---

**levs57** (2022-05-21):

This is quite an achievment!

I’d like to point out that this schema supports distributed computation of time-lock puzzles, and optimistically it should even be reasonable for everyone to give the sequencer “advice” on the solution of their time-lock puzzle after the order of txs is finalized.

I wonder how could you motivate this behavior by cryptoeconomics? Do you have any ideas?

EDIT: On the second read, do I understand correctly that trader provides the signature AFTER they see the order of txs? Why so? I think there is a censorship attack potential at this stage, sequencer decrypts transactions and then just drops the ones it doesn’t like, pretending no signature is sent??

I’d like to point out that transaction encryption gives a wonderful possiblity of censorship resistance due to sequencer not knowing what to censor! This is an extremely powerful proposition, it would be really sad if it goes to waste.

EDIT2: Also, do I understand correctly that irrespective of a chosen method of proof generation of time-lock puzzle this proof can be precomputed? So actually for a trader it wouldn’t be 540 seconds, but would be almost instant, with precomputation offline phase taking 540 seconds?

---

**Killari** (2022-05-22):

This is a cool idea but it can only remove frontrunning MEV and other solutions are needed for other kind of MEV. I wonder how the scheme deals with gas and validator fees? As the validator does not know how heavy a certain transaction is beforehand as its under a complete ZK. The transaction can be too big to fit into a block. This can be avoided by not making the validator payment ZK and also the size of the transaction could also be public information. This still leaves the computation cost that needs to be revealed beforehand, which is impossible to do as it can depend on the order.

I guess this means we can only enable a very limited set of transactions and not just any EVM transactions are ok?

---

**levs57** (2022-05-22):

I think you can publish gas limit and gas price in the open?

And enforce sorting by gas price, that removes all MEV but blind removal of unknown transactions (~ removal of everything but your transactions to arb alone and in peace).

---

**MicahZoltu** (2022-05-22):

Blocks are filled by gas used, not gas limit.  If you fill by gas limit, someone can create a transaction that costs 30,000 gas but has a gas limit of 30,000,000 and the block will be “full” even though the transaction didn’t actually do anything.

---

**levs57** (2022-05-22):

Yeah, we will need to always burn the remaining gas, thats the difference with current EVM behavior where it is refunded.

---

**MicahZoltu** (2022-05-23):

This would mean that the throughput of the chain is unnecessarily low.  One could imagine a mechanism for making up for the unused blockspace, but it would add notable complexity.

---

**levs57** (2022-05-23):

I don’t think it will make it unnecesarily low - it is economically feasible to provide honest estimate on gas, then.

---

**MicahZoltu** (2022-05-23):

The problem is that many transactions have gas usage that changes greatly depending on order.  For example, a Uniswap transaction that fails will use significantly less gas than a Uniswap transaction that succeeds.  This change would make all code paths cost the worst case amount of gas, even if they use significantly less.

---

**0xTariz** (2022-05-25):

Thank you for your good question!

![](https://ethresear.ch/user_avatar/ethresear.ch/levs57/48/7254_2.png) levs57:

> I’d like to point out that this schema supports distributed computation of time-lock puzzles, and optimistically it should even be reasonable for everyone to give the sequencer “advice” on the solution of their time-lock puzzle after the order of txs is finalized.
>
>
> I wonder how could you motivate this behavior by cryptoeconomics? Do you have any ideas?

The traders’ “advice” may be an option, but we haven’t thought about it enough yet. We believe that communication between traders and operators should not be inevitable for protocols to be guaranteed. The operator should be able to get its decision key without additional external data. This is also why we thought time-lock puzzle-based encryption was a better solution than a threshold.

If the option makes a better protocol, I think we should consider that. For this, there may be crypto-economics such as commission discounts, but it is not yet considered.

![](https://ethresear.ch/user_avatar/ethresear.ch/levs57/48/7254_2.png) levs57:

> EDIT: On the second read, do I understand correctly that trader provides the signature AFTER they see the order of txs? Why so? I think there is a censorship attack potential at this stage, sequencer decrypts transactions and then just drops the ones it doesn’t like, pretending no signature is sent??
>
>
> I’d like to point out that transaction encryption gives a wonderful possiblity of censorship resistance due to sequencer not knowing what to censor! This is an extremely powerful proposition, it would be really sad if it goes to waste.

Sending a signature to the operator is one way to ensure that a committed order is carried out. The operator receives the signature and creates proof with it, the verifier contract can verify the integrity of the order.

The operator must execute the transactions in the order committed to the MMR, regardless of receiving the trader’s signature. Therefore, it can be said that the operator did not receive the signature, but the transaction cannot be dropped based on this. However, if the operator performs differently than the committed order, the trader must challenge to verifier contract on L1. In this case, the confirmation may be delayed due to a challenge period.

![](https://ethresear.ch/user_avatar/ethresear.ch/levs57/48/7254_2.png) levs57:

> EDIT2: Also, do I understand correctly that irrespective of a chosen method of proof generation of time-lock puzzle this proof can be precomputed? So actually for a trader it wouldn’t be 540 seconds, but would be almost instant, with precomputation offline phase taking 540 seconds?

The proof is used to prove not only the time-lock puzzle but also the encryption and validity of transaction. So the proof can’t be made without knowing what’s in a transaction to be encrypted and verified. so it can be done in advance. The transaction should be synced with the current state of the network.

---

**zeroknight** (2022-05-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/killari/48/7669_2.png) Killari:

> This is a cool idea but it can only remove frontrunning MEV and other solutions are needed for other kind of MEV.

Our first target was a type of sandwich attack that leads to user’s financial loss. As you mentioned, other MEVs like back-running haven’t not been discussed enough. Random ordering might be one of candidates to prevent them. will keep researching on that. Thanks for pointing that out. please let me know other types of MEVs we should condier.

![](https://ethresear.ch/user_avatar/ethresear.ch/killari/48/7669_2.png) Killari:

> I wonder how the scheme deals with gas and validator fees?

Zk rollups can only execute a specific type of transactions. So there will be no too heavy transactions for the system since the types of tx are predetermined and intergated into zk circuits. However if we expand to zkEVM for our system, your concern would be resolved. Through they active discussion, we have also begun to discuss some ideas.

1. The operator does not encrypt information (gas fee, gas price) that can determine the amount of computation.
2. Information that can identify computation of heavy transaction in advance is stored in the validity proof.
We will leave this as an open discussion and actively discuss it together.

*I would like to thank [@levs57](/u/levs57) and [@MicahZoltu](/u/micahzoltu) for their participation in the discussion.*

---

**levs57** (2022-05-25):

Thanks for your answer! Considering censorship attack, I don’t really understand, why do we even collect signatures in the phase 3. What happens if some signatures did not arrive?

On precomputation - you can precompute it! You split proof into two pieces “here is time lock puzzle, and its answer x has Hash(x)=y”, y being some public value. And second piece “here is correct transaction, encrypted with key x, such that Hash(x)=y”, y being some public value.

Then, the first part (timelock puzzle) can be precomputed!

---

**0xTariz** (2022-05-25):

I understand your question!

![](https://ethresear.ch/user_avatar/ethresear.ch/levs57/48/7254_2.png) levs57:

> Thanks for your answer! Considering censorship attack, I don’t really understand, why do we even collect signatures in the phase 3. What happens if some signatures did not arrive?

Our goal is to find a way to finalize the state without a challenge period, and collecting the signatures was one of the methods we came up with. So yes, unfortunately, there can be a censorship attack. But if you know a better way to get rid of the challenge period, I hope you can talk with us.

![](https://ethresear.ch/user_avatar/ethresear.ch/levs57/48/7254_2.png) levs57:

> On precomputation - you can precompute it! You split proof into two pieces “here is time lock puzzle, and its answer x has Hash(x)=y”, y being some public value. And second piece “here is correct transaction, encrypted with key x, such that Hash(x)=y”, y being some public value.
>
>
> Then, the first part (timelock puzzle) can be precomputed!

Yes, I tried the method you mentioned at first! I divided the zkp circuit into two and calculated the time-lock puzzle and encryption separately. I do think that precomputing the time-lock puzzle is a good idea.

However, this method requires a commitment that connects two circuits. Also, it needed storage of parameters (e.g. CRS) and a lot of computation operations (540 seconds).

So this is why we developed PVDE, a method that calculates time-lock puzzles and encryption in one circuit, but requires smaller computing power (just 5 seconds!). If I had not develop PVDE, I would have used the precomputation method. I’ll share all our studies on Ethereum Research later!

---

**vicshi06** (2022-05-28):

Thanks so much for your effect, but I am just wondering is there any other way for the trader to generate false validity proof and perform a DoS attack? And in Phase 3, what happens when the trader checks that the time to receive the commitment from the operator is longer than the minimum time-lock puzzle computation time? Is the transaction simply canceled? If so, when the trader submits the transaction again, doesn’t the trader already know the content of the transaction and might do MEV again? Sorry if those questions are trivial. Thanks in advance.

---

**simbro** (2022-06-02):

This is a really interesting and quite novel approach.  One question I have though: do you have any estimates around the extra computational load placed on the operator from having to solve and decrypt time-lock puzzles?  Creating a proof for a zk-rollup is already very computationally expensive, what impact would this scheme have?

Also, does this scheme allow for only a subset of transactions in each block to be time-locked, is there a way that non-MEV-sensitive transactions can just not use the scheme?

Have you thought what possible incentives there might be for transaction senders to not sign and return the transaction order commitments?  What happens in the case that they decide to withhold, does the transaction still get processed?

(apologies for the barage of questions - it’s a genuinely interesting scheme)

---

**0xTariz** (2022-06-07):

Hi, [@vicshi06](/u/vicshi06)

Thank you for your question. Your question is by no means trivial and it is one of the things we have been pondering so far.

![](https://ethresear.ch/user_avatar/ethresear.ch/vicshi06/48/9323_2.png) vicshi06:

> there any other way for the trader to generate false validity proof and perform a DoS attack?

Since we generate a validity proof with zkp, **The possibility that the verification result of the false validity proof is true is negligible.** Therefore, there is no possibility of being DoS attacks by false validity proof. If you have other ideas, we’d like to talk about it with you ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/vicshi06/48/9323_2.png) vicshi06:

> And in Phase 3, what happens when the trader checks that the time to receive the commitment from the operator is longer than the minimum time-lock puzzle computation time? Is the transaction simply canceled?

If the operator sends a commitment to the trader later than the minimum computation time, currently, we think the trader should not accept it. We are considering a way to declare that traders have not accepted, one of which is they do not sign a commitment.

The traders will challenge, noting that they did not submit their signature. Of course, the operator can execute the order according to its own commitment without the traders’ signature, because the trader can accidentally or maliciously fail to submit the sig.

We know that this method is contrary to the purpose of finalizing without the challenge (in open for discussion). So, we’re still considering another way.

![](https://ethresear.ch/user_avatar/ethresear.ch/vicshi06/48/9323_2.png) vicshi06:

> If so, when the trader submits the transaction again, doesn’t the trader already know the content of the transaction and might do MEV again?

The symmetric key is one-time key. In other word, each key should be used once and the transaction is encrypted, so the operator cannot attempt MEV with the transaction sent again by the trader.

---

**0xTariz** (2022-06-07):

Hi, [@simbro](/u/simbro)

Thank you for your interesting!

![](https://ethresear.ch/user_avatar/ethresear.ch/simbro/48/3821_2.png) simbro:

> One question I have though: do you have any estimates around the extra computational load placed on the operator from having to solve and decrypt time-lock puzzles? Creating a proof for a zk-rollup is already very computationally expensive, what impact would this scheme have?

Since the time-lock puzzle requires sequential computing, the operator may have to use multiple cores if there are many transactions to be processed. To optimization, we are looking at new schemes such as one encryption key for all traders in one round. The validity of a membership proof for the MMR tree is added to the circuit of zk rollups. In the circuit, the condition is to check whether the transaction belongs to the MMR tree.

![](https://ethresear.ch/user_avatar/ethresear.ch/simbro/48/3821_2.png) simbro:

> Also, does this scheme allow for only a subset of transactions in each block to be time-locked, is there a way that non-MEV-sensitive transactions can just not use the scheme?

The non-MEV-sensitive transactions will also be supported, and we are designing them. If you have a good way, I hope we can talk together.

![](https://ethresear.ch/user_avatar/ethresear.ch/simbro/48/3821_2.png) simbro:

> Have you thought what possible incentives there might be for transaction senders to not sign and return the transaction order commitments? What happens in the case that they decide to withhold, does the transaction still get processed?

We are seriously considering this, and i think the answer I left to [@vicshi06](/u/vicshi06) will be the answer to your question ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)


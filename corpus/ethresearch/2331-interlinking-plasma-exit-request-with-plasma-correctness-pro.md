---
source: ethresearch
topic_id: 2331
title: Interlinking plasma exit request with plasma correctness proofs using snark/stark
author: josojo
date: "2018-06-23"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/interlinking-plasma-exit-request-with-plasma-correctness-proofs-using-snark-stark/2331
views: 1853
likes: 5
posts_count: 8
---

# Interlinking plasma exit request with plasma correctness proofs using snark/stark

**TL;DR**

In the last plasma call, one of the topics was a snark/stark-plasma chains, which can always be proven to have only valid blocks. Vitalik elaborates that one problem, which can still not be solved with snark/stark secured chains during withdrawals, is:

> “the problem is basically that the system has no idea that the coins exiting at the different time might actually be the same ones”.

I made exactly the same observation, but found an interesting workaround: it relies on a tricky interlinking between deposit/withdraw requests and the plasma chain.

In the following, I would like to give a specification for a whole plasma chain, but first, let me give you a glimpse of the trick:

**Setup description:**

Let’s assume that the plasma chain at height N has a state S_n, which is described by variables s1,s2,…,sk (each s would, for example, represent a valid spendable utxo). We also have a program P that can check that a transaction t_i applied on S_n is valid and will generate the new state S_n+1. In order to have it more compact, P could check the validity of t_i in the following way:

`P(i=(merkle_root(S_n)), w=(s1,..,sk, t_i)) =(merkle_root(S_n+1))`

where i is the input of the snark, and w=(s1,…,sk,t_i) is the witness of the snark. The witness would entail all the variables describing the state S_N and the new transaction t_i.

P would essentially do the following steps:

1. calculate the merkle_root of (s1,…,sk) and check that it is indeed the input i.
2. would apply the transaction t_i on the state: (s1,…,sk) and get a new state (r1,…, rk)
3. would hash the state (r1,…, rk) and would provide its Merkle root as the output (merkle_root(S_n+1))

For simplicity, I wrote it down with one transaction, but a proof can be made for a transaction set as well.

This is the usual setup for snark plasma chains, but now we make it more complicated:

**Idea: Interlinking plasma chain exits with root chain.**

We assume that the plasma contract on the root chain will compactify all  exits requests for a given ethereum block by calculating: `newExitHash = sha256(newExitHash, exitUTXO)`. The plasma chain operator would be required to reference NewExitHash in one of his next snark-proofs. If a list of exits [exitUTXO_1, … exitUTXO_L] has generate the exit hash newExitHash, then the chain operator would need to provide a proof for it:

`P(i=(merkle_root(S_n), newExitHash, exitIsValid ), w=(s1,..,sk, t_i, [exitUTXO_1, ... exitUTXO_L])) =(merkle_root(S_n+1))`

where exitIsValid is an array of zeros and ones indicating the validity(1) or non-validity(0) of the exit request. We require the program P to check that:

1. calculate the merkle_root of (s1,...,sk) and check that it is indeed the input i.
1.1 calculate the iterative hash sha256(newExitHash, exitUTXO_i) for i=1,…,L and check that the hash equals newExitHash from the input i.
2. For each exit in [exitUTXO_1, ... exitUTXO_L]

check that the exit request exitUTXO_I has the same validity if applied to the current state (s1, ...,sk), as indicated in exitIsValid[i]
3. if the exit is valid, it will be applied to the state (s1, ...,sk) and calculate the new state (s1, ...,sk) by removing the exited utxo.
4. would apply the transaction t_i on the latest state after the exit request processing: (s1,...,sk) and get a new state (r1,...., rk)
5. would hash the state (r1,...., rk) and would provide its Merkle root as the output (merkle_root(S_n+1))

We would only accept new plasma blocks of the chain operator, if he includes and proves his inclusion of exits in the latest plasma block. In order to avoid problems with reorgs in ethereum, he would be required to include the newExitHashes of ethereum blocks only after a certain delay.

The beauty of this construction is that the operator can still produce unavailable blocks, but he would be forced to processes all valid exits from the plasma chain. If he does not include them, then we have a proof that he did not do it and the root-contract will prevent the chain operator to submit new blocks. Then the plasma chain stops. In this case, we can still do exits from the last checkpoint and slash/punish the chain operator heavily.

*Main observation:*

Before working with starks, data-unavailability was always a subjective matter. Now, by linking plasma chain and root-chain exits, we get an objective criterion for the data unavailability. If there is a real data unavailability, the chain will halt. If there is only a partial data-unavailability for some parties, these parties can leave without any risk, as the operator is forced to validate their exits.

**Outline of a specification for a plasma chain:**

This specification uses the above-mentioned trick to build a very secure and light client friendly token-transfer plasma chain, which allows huge scalability. The scalability is only limited by snark/stark proof generation constraints.

We describe a plasma chain at height N with a state `S_n`, which is described by variables [s]=s1,s2,…,sk. Each element in [s] is an address and a balance associated to this address. After each creation of a new plasma block, the current state of the plasma chain will be compactified as a hash and submitted to the root-chain. Along with the hash, we also submit a proof that the state transition from S_n to S_n+1, by applying the transactions of the plasma block on S_n, is valid and S_n+1 will be represented by the new hash committed to the root chain.

Deposits into the plasma chain will be compactified by the root-contract in a hash `newDepositsHash`. Likewise, normal withdrawal requests from the plasma chain will be compactified by the root-contract in a hash `newExitHash`.

The proof for each new block will the look like:

`P(i=(merkle_root(S_n), newExitHash, [exitIsValid], newDepositsHash ), w=([s], [t], [exits],[deposits])) =(merkle_root(S_n+1)),`

where [s] is an array of the variables describing the current state, [t] is an array of transactions, [exits] is an array of exit data from the root-contract and [deposits] is the array describing the deposits data.

P would do the following checks:

1. merkle_root([s]) == merkle_root(S_n)
2. newExitHash == reiterated_hash([exits])
3. newDepositHash == reiterated_hash([deposits])
4. validates the list [exitIsValid] and updates the state [s] by processing each exit
5. validates all transactions from [t] and updates the state after each transaction
6. calculate (merkle_root(S_n+1))

This gives us a great plasma chain, in case we would never run into data-unavailability. In order to handle data-unavailability, we need some more inputs:

The chain operator needs to make a deposit of X Ether, before chain creation. He will only get them back, once he has processed all exits, such that the plasma root-contract does no longer hold any clients funds. In order to make this a viable solution, the plasma operator can also initiate valid exits.

These X Ether are a huge incentive for the plasma chain operator to keep the system alive. If he gets himself into data-unavailability, the plasma root-contract will notice it and will slash his X Ether.

We would also need checkpoints, as in case of a data-unavailability, all users would be required to withdraw from the plasma chain at the same height. So each day the chain operator marks one block as a checkpoint-block. Clients of the plasma chain would be required to be online once a day. Each day the client would ask the chain operator for a Merkle proof of his balance at the last checkpointed-block. If he gets this Merkle proof, all is good. If he does not get it, he will need to exit the chain by registering his account for an exit on the ethereum root-chain. Now there are two possibilities:

1. the operator exits his funds. Then the client is safe.
2. the operator does not exit his funds, but then the plasma-chain will stop. If the chain is halted, all users need to withdraw from the second last checkpoint, which was from the previous day. Every user would have a valid Merkle proof to withdraw their balance from the check-pointed block, since otherwise, they would have stopped the chain beforehand. Hence all users can exit the chain at the checkpointed block by making an exit request on the root-chain and by providing their Merkle-proof.

*This means that the transactions of the last two days might be reverted.* In order to make this scenario unprofitable for the chain operator, we would require every stark proof to prove additionally that not more than X Ether has been spent, since the last two checkpoints. If this proof is in place,  the chain operator would lose X Ether in case of chain stop and might get some gains smaller than X Ether by the reverting of transactions. Thus, the attack would be unprofitable for him in ANY case, and he would never intentionally introduce a data-unavailability.

This means, we can set up the plasma chains, such that data-unavailability will be heavily disincentivized. For me, this is pretty exciting stuff. I mean on top of this incentive to keep the plasma chain alive, we get great scalability and very fast exits “for free”.

Please be aware that this specification cannot yet be implemented, as snarks/starks proof calculations are still too inefficient. But I am sure that zero-knowledge protocols will evolve. Especially, recursive proofs attempts are looking quite promising.

*edits: I  corrected some grammar

## Replies

**shamatar** (2018-06-25):

Hello [@josojo](/u/josojo)

Interesting construction, we will try to implement it as a part of experiment. Such a statement for a SNARK looks possible, up to some internal tricks like always padding the set of exits to a constant length by some empty/dummy exits.

May be you can go a little further and collect the exit/deposits requests over 100 Ethereum blocks batches, than allow an operator to process such a batch in the next, let’s say, 3 Plasma blocks, otherwise submission of new blocks is forbidden until the batch is processed and at the same time the root-chain contract can already slash an operators deposit.

Proving a single state transition (under one transaction) can be done in under a minute if a SNARK-friendly hash function is used, but to implement multi-transactional block transitions looks like one needs a recursive snark construction.

Sincerely, Alex

---

**josojo** (2018-06-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/shamatar/48/670_2.png) shamatar:

> interesting construction, we will try to implement it as a part of experiment.

Wow, this is awesome!

You are stating that proving a single state transition can be done in under a minute? Can you show some reference code? This would we awesome. I felt like it would take much much longer. ( Even in stark it takes quite [some time](https://eprint.iacr.org/2018/046.pdf) for bigger states )

![](https://ethresear.ch/user_avatar/ethresear.ch/shamatar/48/670_2.png) shamatar:

> one needs a recursive snark construction

Are you referring to such [constructions](https://eprint.iacr.org/2014/595.pdf)? Or do there exit even more efficient recursive snarks?

Yes, collecting exits/deposits request over some time makes perfect sense. ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=12)

---

**josojo** (2018-06-28):

[@shamatar](/u/shamatar)

You were right. This plasma chain construction might be feasible with snark proofs. Some people are able to set up proven Merle tree calculations for a Merle depth of up to 30. Even with snark. I am excited to see what will become possible after another year of snark proof optimizations.

---

**shamatar** (2018-07-04):

Hello [@josojo](/u/josojo)

We’ve made a small paper explaining a naive construction and estimated number of constraints, please check [here](https://github.com/BANKEX/research).

Sincerely, Alex

---

**josojo** (2018-07-05):

Yes, this is a very interesting analysis.

Here are some comments:

- recursive snarks are not yet possible to my understanding, as there are no opcodes for a set of cyclic elliptic curves.
- if recursive snarks are not possible, probably it is easier to make a verification of the complete starting state S  given in the witness by hashing it completely and then applying one transaction after the other directly on the State S and its successors. I mean one should be able to avoid the hashing between all transactions if we hash the state completely at the beginning of the application of all the transactions and at the end of it.
- I have not yet figured out the number of circuits for the ECDSA process. One needs to check that all transactions were signed by the owners. It seems this was also forgotten in your analysis.

Take all these comments with a grain of salt. I am still exploring this space.

---

**shamatar** (2018-07-05):

Oh, yes, recursive snarks are long-term as they will allow parallel proof computation. If you want to process a batch of transactions as one snark you have to wait for all of them to be submitted, then you get the full witness required for proof and can start working on A LOT of constraints.

Just for a sake of rough estimations - a proof of one transaction requires roughly 4*h*c constraints, where h is a tree depth (doesn’t has to be equal to 160 - the address space of Ethereum itself), and c is number of constraints per one run of hash function. With c=2000 (MIMC or Peddersen hash, may be subset sum hash) one can aim for 1 million constraints per transaction in snark. For comparison - a zCash snark is 4.6 million constraints I think.

Regarding signatures - we can either base it on knowledge of some hash preimage (just for a start), or EC crypto is possible in the snark’s field, check [this](https://github.com/zcash/zcash/issues/2230) discussion.

After we post some working prototype snark for a single transaction we will try to build a recursive snark based on the “Cycles on elliptic curves” paper. There is no precompute for it, but I hope for eWASM at some point. Anyway snark curves will have to be >256 bit to have some security margin. Or may be we get STARKs at some point.

---

**josojo** (2018-07-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/shamatar/48/670_2.png) shamatar:

> Just for a sake of rough estimations - a proof of one transaction requires roughly 4 h c constraints, where h is a tree depth (doesn’t has to be equal to 160 - the address space of Ethereum itself), and c is number of constraints per one run of hash function. With c=2000 (MIMC or Peddersen hash, may be subset sum hash) one can aim for 1 million constraints per transaction in snark. For comparison - a zCash snark is 4.6 million constraints I think.

Choosing h can make a huge impact. One optimization would be to choose h quite small 16, so that we can support only 2^{16} different accounts. This should be enough for a rough prototype.

When I mentioned calculating the hash of the current state, I assume indirectly that the current state is not too big. I.e.,  we can represent the current state with a Merkle tree of depth 16-20.

So in my model, we would have the following steps and constraint counts:

1. Calculating the Merkle tree of the WHOLE state described by 2^16 leaves: (2^16*c)
2. Applying n transaction on the state, where the main task is to verify the signatures using s circuits:(n*s)
3. Calculating the Merkle tree of the WHOLE new state with all transactions applied described by 2^16 leaves: (2^16*c)
That totals to 2^17 c+ ns

Thanks for the EC crypto link in your previous post. Interesting


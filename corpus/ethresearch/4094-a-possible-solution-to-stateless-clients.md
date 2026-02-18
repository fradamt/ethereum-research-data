---
source: ethresearch
topic_id: 4094
title: A possible solution to stateless clients
author: kushti
date: "2018-11-02"
category: Sharding
tags: [stateless]
url: https://ethresear.ch/t/a-possible-solution-to-stateless-clients/4094
views: 2912
likes: 4
posts_count: 5
---

# A possible solution to stateless clients

I see that Ethereum community is actively discussing stateless clients.

During Financial Cryptography 2017 we presented a solution for partially stateless clients (https://eprint.iacr.org/2016/994), where only miners need to store the validation state in full in order to generate proofs of its transformations, then other nodes (full nodes actually, which are not losing anything in security but do not store the state) check the proofs.

Now we have solutions for fully stateless clients, for both UTXO- and account-based cryptocurrencies: https://eprint.iacr.org/2018/968 !

There are a lot of open question still if we are talking about not simple payment systems but complex smart contract networks like Ethereum. From the paper: “Recall that in the smart contract setting, the flow of money

will depend of the execution of some contract code on the current contract state, which is updated after

the contract execution. Therefore for Alice to post a contract-triggering transaction she must provide a proof of correctness of the current contract state for EDRAX nodes to execute on. For that, we can again use a Merkle tree whose leaves store hashes of the contract state and have clients provide the respective Merkle proofs. Two challenges that arise in this setting are (i) who is storing the contract state since any client can post transactions that will trigger a contract execution; (ii) how to avoid including the contract state as part of the transaction (the contract state might be too large). For both of these challenges, proof-serving nodes (as introduced above) and SNARKs might help. A complete treatment of these challenges, however, is left as future work.”

We would be happy to hear from the community how stateless clients can affect design of the Ethereum.

## Replies

**johba** (2018-11-03):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/4bbf92/48.png) kushti:

> (ii) how to avoid including the contract state as part of the transaction (the contract state might be too large)

Most contracts operate on quite small state. A compact authenticated data structure like [CSMT](https://github.com/farazhaider/CSMT/blob/a722f2b35fc5e2fac9762b3f0c89112d4ff41d73/CSMT.pdf) and a precompile for verifying proofs might make it very practical to keep only the storage root on chain.

---

**johba** (2018-11-03):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/4bbf92/48.png) kushti:

> (i) who is storing the contract state since any client can post transactions that will trigger a contract execution;

Is this really a problem? The state of any authenticated structure can be reconstructed from transaction history. A centralized service like block explorer might provide the service of proof-serving.

---

**dlubarov** (2018-11-10):

It’s a really interesting model, but the requirement that coin owners sync regularly seems like a heavy price to pay for statelessness. I feel like it would be more practical to just have a handful of archival nodes which store all state. That approach has its own challenges, but at least it doesn’t place any extra burden on “ordinary” users.

With the UTXO variant, did you consider having nodes store the first n levels of the prefix tree? That way, at least coin owners wouldn’t need to download all UTXOs; they could download only transactions which share the same n-bit prefix. The first n levels of their local proof would get out of date, but full nodes could ignore that part of the proof, and fill it in with their own current data.

![](https://ethresear.ch/user_avatar/ethresear.ch/johba/48/20905_2.png) johba:

> Most contracts operate on quite small state. A compact authenticated data structure like CSMT  and a precompile for verifying proofs might make it very practical to keep only the storage root on chain.

Don’t token contracts typically store their ledger as a large hash table? We could develop new token contracts in a different way, perhaps using copy-on-write tree structures, but there would still be lots of “legacy” contracts around.

---

**dlubarov** (2018-11-13):

After thinking about it some more, I don’t understand how local proofs would be created for a new UTXO. A new UTXO’s Merkle path is effectively random. If we had archival nodes, they could generate those initial local proofs, but I thought the intention was to avoid archival nodes?

In theory, the user who owns the neighboring UTXO (with the longest common prefix) could use their Merkle path to generate the new UTXO’s path. But there would only be a single user who has the right information, and even if they can be contacted, they might refuse to help, or demand a bribe, etc. And if a wallet with active UTXOs did go offline, any UTXO prefixes which were unique to them (not shared with any other UTXOs) would be permanently unusable.


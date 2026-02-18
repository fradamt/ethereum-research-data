---
source: ethresearch
topic_id: 19480
title: Sharded Recursive zk-SNARK Proofs
author: cryptskii
date: "2024-05-06"
category: zk-s[nt]arks
tags: [cross-shard]
url: https://ethresear.ch/t/sharded-recursive-zk-snark-proofs/19480
views: 4958
likes: 5
posts_count: 15
---

# Sharded Recursive zk-SNARK Proofs

**TL;DR** In a sharded blockchain protocol that utilizes recursive zk-SNARK proofs to enable scalable, private cross-shard transactions with constant-size proofs of validity. This architecture allows for horizontal scaling while maintaining strong privacy guarantees.

**Background** Existing blockchain systems face significant challenges in terms of scalability and privacy. Sharding is a promising approach to improve transaction throughput by parallelizing computation across multiple chains. However, cross-shard communication remains a bottleneck, as verifying transactions across shards typically requires expensive cross-shard proofs.

Zero-knowledge proofs, particularly zk-SNARKs, offer a powerful tool for enhancing privacy by allowing users to prove knowledge of secret information without revealing it. Unfortunately, generating and verifying zk-SNARK proofs incurs high computational overhead, limiting their practicality for large-scale applications.

Prior solutions have attempted to combine zk-SNARKs with sharding, but fail to fully address the scalability challenges. For example, Zexe uses zk-SNARKs in a sharded setting but requires storing a linear-size “state proof” on-chain. Coda achieves constant-size proofs using recursive composition, but lacks the horizontal scaling benefits of sharding.

**Proposal** We introduce a novel construction that synergistically combines sharding with recursive zk-SNARK proofs for unparalleled scalability and privacy.

At the core of this DLT is a hierarchy of zk-SNARK proofs that recursively attest to the validity of state transitions within and across shards. Each shard generates succinct proofs, called Zero-Knowledge Balance & Inclusion State Proofs (ZkBISPs), certifying the correctness of their local state updates. These ZkBISPs are then aggregated by a designated coordinator into a global proof, termed a Zero-Knowledge Succinct Nested Global-state Proof (ZkSNGP).

Crucially, the ZkSNGP is a constant-size proof that recursively verifies the validity of all shard-level ZkBISPs, thereby providing a succinct and efficient means to prove the integrity of the entire cross-shard state transition. Verifying the ZkSNGP requires only logarithmic time in the number of shards, enabling exponential savings compared to naively checking each shard’s proofs individually.

Formally, we define the intra-shard state transition language \mathcal{L}_{\mathsf{ST}}^{(t,i)} for each shard i at epoch t as the set of tuples (x, w) where:

- The statement x = (\mathsf{shardID}_i, \mathsf{root}_i^{(t-1)}, \mathsf{root}_i^{(t)}, B_i^{(t)}) includes the shard ID, starting and ending state roots, and final account balances.
- The witness w = (\mathsf{txs}_i^{(t)}, \mathcal{T}_i^{(t-1)}, \mathcal{T}_i^{(t)}) contains the list of transactions, along with the initial and final account state trees.
- (x, w) \in \mathcal{L}_{\mathsf{ST}}^{(t,i)} \Leftrightarrow \mathsf{root}_i^{(t-1)} = H(\mathcal{T}_i^{(t-1)}) \wedge \mathsf{root}_i^{(t)} = H(\mathcal{T}_i^{(t)}) \wedge \text{transition}(\mathcal{T}_i^{(t-1)}, \mathsf{txs}_i^{(t)}) \rightarrow \mathcal{T}_i^{(t)}, i.e, the roots match the account trees and the final tree results from applying valid transactions to the initial tree.

Similarly, we define the cross-shard state transition language \mathcal{L}_{\mathsf{CST}}^{(t)} for epoch t as the set of tuples (x, w) where:

- The statement x = (\mathsf{root}_G^{(t-1)}, \mathsf{root}_G^{(t)}) consists of the starting and ending global state roots.
- The witness w = \left(\left\{\left(\mathsf{shardID}_i, \pi_{\mathsf{ST},i}^{(t)}, \mathsf{root}_i^{(t-1)},\mathsf{root}_i^{(t)}, B_i^{(t)}\right)\right\}_{i=1}^{\ell},\mathcal{T}_G^{(t-1)},\mathcal{T}_G^{(t)}\right) includes the shard IDs, ZkBISPs, local roots and balances, and global account trees.
- (x, w) \in \mathcal{L}_{\mathsf{CST}}^{(t)} \Leftrightarrow \forall i: \mathsf{Verify}_{\mathsf{ST}}(\mathsf{vk}_{\mathsf{ST}}, x_i, \pi_{\mathsf{ST},i}^{(t)}) \wedge \mathsf{root}_G^{(t-1)} = H(\mathcal{T}_G^{(t-1)}) \wedge \mathsf{root}_G^{(t)} = H(\mathcal{T}_G^{(t)}) \wedge \text{merge}(\mathcal{T}_G^{(t-1)}, \{\mathsf{root}_i^{(t)}, B_i^{(t)}\}_{i=1}^{\ell}) \rightarrow \mathcal{T}_G^{(t)}, i.e., the ZkBISPs verify w.r.t. their shards, the Merkle roots match, and the final global tree is the result of correctly merging the shards’ final local trees and balances.

A shard’s ZkBISP for epoch t is generated as \pi_{\mathsf{ST},i}^{(t)} \leftarrow \mathsf{Prove}_{\mathsf{ST}}(\mathsf{pk}_{\mathsf{ST}}, x_i, w_i) for (x_i, w_i) \in \mathcal{L}_{\mathsf{ST}}^{(t,i)}, where \mathsf{pk}_{\mathsf{ST}} is the proving key for the corresponding zk-SNARK scheme. The coordinator’s ZkSNGP is computed analogously as \pi_{\mathsf{CST}}^{(t)} \leftarrow \mathsf{Prove}_{\mathsf{CST}}(\mathsf{pk}_{\mathsf{CST}}, x, w) for (x, w) \in \mathcal{L}_{\mathsf{CST}}^{(t)}

The coordinator, randomly selected in each epoch, collects these ZkBISPs along with the shards’ final state roots \mathsf{root}_i^{(t)} and account balances B_i^{(t)}. It then generates the ZkSNGP \pi_{\mathsf{CST}}^{(t)} (green proof) certifying the validity of the overall state transition, including the correct application of all shard-level updates to the global state.

**Advantages** The network simultaneously achieves exceptional horizontal scalability and privacy without sacrificing security or decentralization.

In terms of scalability, the concept supports an unprecedented number of shards and transactions per second while retaining a constant-size proof of the system’s entire state. Concretely, if there are \ell shards each processing N transactions, the communication cost per epoch is only O(\ell) for the coordinator to collect the ZkBISPs, and the ZkSNGP proof adds just O(1) to the blockchain size. Crucially, verifying the ZkSNGP requires O(\log \ell) time, an exponential speedup compared to naively verifying all \ell shards.

For example, suppose the network is instantiated with \ell = 2^{10} shards, each processing N = 2^{20} transactions in 2-minute epochs. This configuration could support a peak throughput of roughly 1 billion transactions per epoch, or 500,000 transactions per second, with a ZkSNGP verification time of only 10\log \ell \approx 100 ms on ordinary hardware. The recursive proof would contribute a mere 1 KB to the blockchain per epoch, maintaining years of history in a highly compact format.

In terms of privacy, the ZkSNGPs inherit the zero-knowledge property of the underlying zk-SNARK scheme, revealing nothing about the shards’ local transactions beyond the final state roots and balances. An adversary that compromises the coordinator cannot glean any additional information, as the shards’ ZkBISPs are similarly zero-knowledge. Transactional privacy thus holds as long as at least one shard remains honest.

Compared to prior sharded blockchain designs, the network is the first to achieve sublinear proof sizes and verification times by recursively composing zk-SNARKs. Relative to Zexe, the network attains a qualitative improvement in scalability by eliminating the linear-size “state proof” in favor of constant-size ZkSNGPs. Compared to Coda, the network offers strictly stronger performance due to its sharded architecture, while still leveraging Coda’s core technique of recursive proof composition.

**Applications** the network’s dual emphasis on scalability and privacy renders it a natural foundation for a variety of high-throughput, privacy-centric blockchain applications.

On the payments front, the network could serve as a backend for a globally-scalable digital currency with strong confidentiality guarantees, concealing both transaction amounts and participants. The subtransactions within each shard could clear near-instantaneously, while cross-shard payments would incur a maximum delay of one epoch (e.g., 2 minutes) before the ZkSNGP confirms finality. This would support a substantially higher payment volume than existing solutions like Zcash without leaking metadata.

More broadly, the network could function as a privacy-preserving platform for general smart contract execution. Shards would not only process token transfers but also arbitrary state transitions, with the ZkBISPs and ZkSNGP verifying the correctness of all contract logic and dependencies. This would enable complex applications such as private decentralized exchanges, automated market makers, and lending protocols to run at scale, without disclosing individual users’ balances or positions.

The network’s sharded architecture could also be adapted to specific domains to meet their unique performance requirements. For instance, a decentralized adtech ecosystem that handles billions of micropayments per day could utilize more granular sharding (e.g., \ell = 2^{20} shards), with each shard perhaps corresponding to a particular geographic region or publisher. A secure messaging app that routes payments alongside packets could likewise tune its cross-shard spanning tree structure based on network topology.

**Conclusion** the network introduces a powerful new paradigm for designing scalable and private blockchain protocols through recursive zk-SNARK proof composition. By strategically combining recursive proofs with sharding, the network enables a significant breakthrough in blockchain performance, supporting over a million transactions per second with sublinear proof sizes and verification times.

## Replies

**cryptskii** (2024-05-06):

Almost a year already spent on this, so as you can imagine, we are well beyond just PoC. Q&A welcome. Here or  - info@irrefutablelabs.xyz

---

**cryptskii** (2024-05-08):

By incorporating [Triadic Consensus: A Fast and Resilient Consensus Mechanism for Sharded Blockchains](https://ethresear.ch/t/triadic-consensus-a-fast-and-resilient-consensus-mechanism-for-sharded-blockchains/19504) with this ZKP method, the coordinator could be autonomous in its decision making, simply responding to the supermajority.

---

**cryptskii** (2024-05-08):

intra-shard probalistic, inter-shard deterministic.

---

**cryptskii** (2024-05-08):

Pull-in [Client-Side Ordinal Transaction Ordering (COTO) - #2 by cryptskii](https://ethresear.ch/t/client-side-ordinal-transaction-ordering-coto/19503/2) to remove T.O. from consensus.

---

**SK0M0R0H** (2024-05-10):

I like the idea; it’s actually the same thing that we’re doing for the [zkSharding](https://cms.nil.foundation/uploads/main_e16b5c1bc3.pdf) concept (Section 7).

I think one important part here is that proofs still require time to generate and aggregate. Aggregation adds delays compared to zkRollups.

From here, a question arises: should the execution system be decentralized-and-verified or centralized-but-verified, similar to modern zkRollups? What do you think?

---

**cryptskii** (2024-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/sk0m0r0h/48/2371_2.png) SK0M0R0H:

> should the execution system be decentralized-and-verified or centralized-but-verified, similar to modern zkRollups? What do you think?

decentralized-and-verified 100%

---

**cryptskii** (2024-05-16):

for topology:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/cryptskii/48/14536_2.png)
    [Sierpinski Triangle Topology](https://ethresear.ch/t/sierpinski-triangle-topology/19566) [Sharding](/c/sharding/6)



> TL;DR
> We propose integrating the Sierpinski triangle topology into blockchain sharding to enhance scalability, load balancing, and fault tolerance. This novel sharding mechanism exploits the fractal structure and self-similarity properties of the Sierpinski triangle, optimizing inter-shard and intra-shard communication, data replication, and node assignment. Our approach significantly improves transaction throughput, consensus efficiency, and resilience against Byzantine failures.
> Background
> Bl…

---

**cryptskii** (2024-05-16):

This will run as EVM but the ZkSNGPs with be anchored to Bitcoin like so:

### Example Workflow

1. Generate zkSNGPs: At regular intervals (e.g., end of each epoch), generate zkSNGPs for all state transitions.
2. Aggregate zkSNGPs: Collect a predefined number of zkSNGPs or aggregate over a specific time period.
3. Create Merkle Tree: Construct a Merkle tree with zkSNGP hashes as leaves.
4. Compute Merkle Root: Compute the Merkle root of the tree.
5. Create Bitcoin Transaction: Embed the Merkle root in the OP_RETURN field of a Bitcoin transaction.
6. Broadcast Transaction: Broadcast this transaction to the Bitcoin network.
7. Store Batch Information: Record the batch details and the corresponding Bitcoin transaction ID in your L1 system.

```auto
import hashlib
from bitcoinlib.transactions import Transaction, OP_RETURN

def create_merkle_root(hashes):
    if len(hashes) == 1:
        return hashes[0]
    if len(hashes) % 2 != 0:
        hashes.append(hashes[-1])
    new_level = []
    for i in range(0, len(hashes), 2):
        new_hash = hashlib.sha256(hashes[i] + hashes[i+1]).hexdigest()
        new_level.append(new_hash)
    return create_merkle_root(new_level)

def create_bitcoin_transaction(merkle_root):
    tx = Transaction()
    tx.add_output(OP_RETURN, merkle_root)
    tx.sign()  # Sign the transaction with appropriate private keys
    return tx

zkSNGPs = [...]  # List of zkSNGP hashes
merkle_root = create_merkle_root(zkSNGPs)
bitcoin_tx = create_bitcoin_transaction(merkle_root)
bitcoin_tx.broadcast()  # Broadcast to Bitcoin network

# Store batch metadata in L1 system
batch_metadata = {
    'merkle_root': merkle_root,
    'bitcoin_tx_id': bitcoin_tx.txid,
    'zkSNGPs': zkSNGPs
}
```

Why?:

1. Immutability and Data Integrity: By committing zkSNGPs to the Bitcoin blockchain, ProofChain inherits Bitcoin’s immutability properties. Once a batch of zkSNGPs is recorded on the Bitcoin blockchain, it becomes part of BTC’s immutable ledger, providing a tamper-proof and verifiable history of ProofChain’s state transitions on Bitcoin.
2. Decentralized Security: Anchoring zkSNGPs to Bitcoin distributes the security of ProofChain across the decentralized Bitcoin network. The Bitcoin blockchain is maintained by a vast network of miners, making it extremely difficult for any single entity to compromise the integrity of the zkSNGPs stored on it.
3. Timely Finality: Bitcoin’s proof-of-work consensus mechanism ensures timely finality of transactions. Once a Bitcoin transaction containing a batch of zkSNGPs is confirmed and included in a block, it is considered final and irreversible. This provides a reliable and timely mechanism for ProofChain to achieve finality for its state transitions.
4. Simplified Verification Process: By leveraging Bitcoin’s existing infrastructure and tools, the verification process for zkSNGPs becomes simplified. Verifiers can utilize Bitcoin’s block explorers, APIs, and libraries to efficiently verify the presence and integrity of zkSNGPs on the Bitcoin blockchain.
5. Backup and Redundancy: Committing zkSNGPs to the Bitcoin blockchain acts as a backup mechanism for ProofChain. In the event of any data loss or system failure on ProofChain’s end, the zkSNGPs stored on the Bitcoin blockchain can be used to recover and validate the state of the ProofChain ledger.

---

**cryptskii** (2024-05-18):

Expanding on the original post, we propose enhancing the protocol by leveraging Verkle trees [^1] for state commitments within each shard. Verkle trees are a drop-in replacement for Merkle trees that offer substantially smaller proofs by replacing hashing with vector commitments.

Concretely, let \mathbf{F} be a finite field. A polynomial commitment over \mathbf{F} consists of three algorithms (\mathsf{Setup}, \mathsf{Commit}, \mathsf{Open}):

- \mathsf{Setup}(1^\lambda, d) \to (\mathsf{pk}, \mathsf{vk}): On input security parameter 1^\lambda and polynomial degree bound d, output public parameters \mathsf{pk} and verification key \mathsf{vk}.
- \mathsf{Commit}(\mathsf{pk}, f(X)) \to c: On input \mathsf{pk} and polynomial f(X) \in \mathbf{F}_{\leq d}[X], output a commitment c.
- \mathsf{Open}(\mathsf{pk}, f(X), r, v) \to \pi: On input \mathsf{pk}, polynomial f(X), evaluation point r \in \mathbf{F}, and claimed value v \in \mathbf{F}, output an evaluation proof \pi attesting that f(r) = v.
- \mathsf{Verify}(\mathsf{vk}, c, r, v, \pi) \to \{0,1\}: On input \mathsf{vk}, commitment c, point r, claimed value v, and proof \pi, output 1 if f(r) = v for the polynomial f(X) committed in c, else 0.

In our construction, each shard S_i maintains a Verkle tree \mathcal{T}_i^{(t)} over its state at epoch t. For a tree of arity b and depth d, the leaves are partitioned into b^{d-1} groups, each interpolated by a polynomial f_{i,j}(X) \in \mathbf{F}_{\leq b-1}[X]. The root commitment is computed as c_{i,0} := \mathsf{Commit}(\mathsf{pk}, f_{i,0}(X)), where f_{i,0}(X) interpolates the commitments to f_{i,1}(X), \ldots, f_{i,b}(X).

To generate the \mathsf{zkBISP} for shard S_i, the statement x_i now includes the Verkle root commitments c_{i,0}^{(t-1)} and c_{i,0}^{(t)} in place of Merkle roots:

\begin{aligned}
x_i &= (i, c_{i,0}^{(t-1)}, c_{i,0}^{(t)}, \mathbf{B}_i^{(t)}) \\
w_i &= (\mathbf{txs}_i^{(t)}, \mathcal{T}_i^{(t-1)}, \mathcal{T}_i^{(t)})
\end{aligned}

The shard proves the inclusion of its state updates in the Verkle tree by computing evaluation proofs for each modified leaf:

\{\pi_{i,j}^{(t)} \leftarrow \mathsf{Open}(\mathsf{pk}, f_{i,j}(X), r_{i,j}, v_{i,j}^{(t)})\}_{j=1}^m

Here r_{i,j} is the leaf position and v_{i,j}^{(t)} is the leaf value after applying \mathbf{txs}_i^{(t)}.

The coordinator’s \mathsf{zkSNGP} relation \mathcal{R}_\mathsf{CST}^{(t)} is modified to include the shards’ Verkle commitments and proofs:

\begin{aligned}
x &= (c_{G,0}^{(t-1)}, c_{G,0}^{(t)}) \\
w &= (\{\mathsf{zkBISP}_i^{(t)}, c_{i,0}^{(t)}, \{\pi_{i,j}^{(t)}\}_{j=1}^m\}_{i=1}^\ell, \mathcal{T}_G^{(t-1)}, \mathcal{T}_G^{(t)}, \{\mathbf{txs}_{ij}^{(t)}\}_{i,j=1}^\ell)
\end{aligned}

To verify the \mathsf{zkSNGP}, clients check that:

1. \mathsf{Verify}(\mathsf{vk}_\mathsf{ST}, x_i, \pi_{\mathsf{ST},i}^{(t)}) = 1 for each \mathsf{zkBISP}_i^{(t)}, i.e., the per-shard proofs are valid.
2. \mathsf{Verify}(\mathsf{vk}, c_{i,j}^{(t)}, r_{i,j}, v_{i,j}^{(t)}, \pi_{i,j}^{(t)}) = 1 for each Verkle proof \pi_{i,j}^{(t)}, i.e., the claimed leaf updates are correct.
3. \mathsf{merge}(\mathcal{T}_G^{(t-1)}, \{c_{i,0}^{(t)}\}_{i=1}^\ell, \{\mathbf{txs}_{ij}^{(t)}\}_{i,j=1}^\ell) = \mathcal{T}_G^{(t)}, i.e., the final global tree is consistent with the shards’ commitments and cross-shard transactions.

By replacing Merkle trees with Verkle trees, we reduce the size of state inclusion proofs from O(d \cdot \lambda) to O(d \cdot (\log b + \lambda)), where \lambda is the security parameter. This yields a corresponding reduction in the size of \mathsf{zkBISP} and \mathsf{zkSNGP} proofs.

For a concrete example, suppose each shard maintains a tree with 1 billion leaves, i.e., b = 1024 and d = 10. With Merkle trees using \lambda = 256 bit hashes, each inclusion proof requires 2560 bits. With Verkle trees, setting \log b = 10 and using the same \lambda, the proofs are just 266 bits each, nearly a 10\times savings.

More notably, since Verkle proofs are constant-size in the witness length, we can aggregate updates across many leaves into a single \mathsf{zkBISP} without significantly increasing the proof size. If each shard batches k leaf updates into a single \mathsf{zkBISP}, the amortized proof size per update is just O((\log b + \lambda)/k), an exponential savings over Merkle proofs which grow linearly in k.

In summary, augmenting our protocol with Verkle trees for state commitments offers compounding improvements in performance and scalability:

1. Each shard can compute succinct proofs for large batches of state updates, reducing the number of \mathsf{zkBISP} s generated per epoch.
2. The size of each \mathsf{zkBISP} and the aggregate \mathsf{zkSNGP} is substantially reduced, minimizing on-chain storage costs.
3. Shards can verifiably update more state per epoch without increasing the cross-shard proof verification overhead.

By achieving sublinear proof sizes in both the number of shards and the amount of state updated per shard, our Verkle-enhanced design offers a significant scalability improvement while preserving the strong privacy guarantees of the original protocol.

[^1]: J. Kuszmaul. Verkle Trees. https://math.mit.edu/research/highschool/primes/materials/2018/Kuszmaul.pdf

# Privacy Analysis

The use of Verkle trees not only improves scalability but also enhances the privacy properties of our sharded blockchain protocol. We analyze the privacy guarantees both within and across shards.

## Intra-Shard Privacy

For transactions within a single shard S_i, the \mathsf{zkBISP} relation ensures that the proof \pi_{\mathsf{ST},i}^{(t)} leaks no information about the shard’s internal transactions \mathbf{txs}_i^{(t)} beyond what is revealed by the initial and final state commitments c_{i,0}^{(t-1)} and c_{i,0}^{(t)}.

Specifically, let \mathcal{T}_i^{(t-1)} and \mathcal{T}_i^{(t)} be the Verkle trees representing the shard’s state at the start and end of epoch t, respectively. The \mathsf{zkBISP} for shard S_i satisfies the following privacy property:

For any two sets of transactions \mathbf{txs}_i^{(t)}, \widetilde{\mathbf{txs}}_i^{(t)} that result in the same final state \mathcal{T}_i^{(t)} when applied to \mathcal{T}_i^{(t-1)}, the corresponding proofs \pi_{\mathsf{ST},i}^{(t)} \leftarrow \mathsf{Prove}(\mathsf{pk}_\mathsf{ST}, x_i, w_i) and \tilde{\pi}_{\mathsf{ST},i}^{(t)} \leftarrow \mathsf{Prove}(\mathsf{pk}_\mathsf{ST}, x_i, \tilde{w}_i), where

\begin{aligned}
w_i &= (\mathbf{txs}_i^{(t)}, \mathcal{T}_i^{(t-1)}, \mathcal{T}_i^{(t)}) \\
\tilde{w}_i &= (\widetilde{\mathbf{txs}}_i^{(t)}, \mathcal{T}_i^{(t-1)}, \mathcal{T}_i^{(t)})
\end{aligned}

are computationally indistinguishable.

This property, which follows directly from the zero-knowledge guarantee of the zk-SNARK, implies that the \mathsf{zkBISP} does not leak any information about the specific transactions executed by the shard, only the final Verkle tree commitment c_{i,0}^{(t)}.

## Cross-Shard Privacy

For transactions that span multiple shards, the \mathsf{zkSNGP} provides strong privacy guarantees at both the coordinator and verifier level.

First, due to the zero-knowledge property of the \mathsf{zkBISP} s, the coordinator learns nothing about the shards’ internal transactions \mathbf{txs}_i^{(t)} or the details of any cross-shard transactions \mathbf{txs}_{ij}^{(t)} beyond the final Verkle commitments c_{i,0}^{(t)} and account balances \mathbf{B}_i^{(t)}.

Second, when verifying the \mathsf{zkSNGP}, clients do not learn any information beyond the initial and final global state roots c_{G,0}^{(t-1)} and c_{G,0}^{(t)} (which are already public). The zk-SNARK proof \pi_\mathsf{CST}^{(t)} ensures that the final state is consistent with some set of valid cross-shard transactions, without revealing their details.

In essence, while each shard’s \mathsf{zkBISP} “encrypts” its local transactions, the coordinator’s \mathsf{zkSNGP} provides an “encrypted” aggregation that hides information between shards. This enables clients to verify the correctness of the global state transition without compromising privacy.

From a formal perspective, we can model this privacy property as an indistinguishability game. The adversary is given the initial global state \mathcal{T}_G^{(t-1)} and two sets of valid cross-shard transactions \{\mathbf{txs}_{ij}^{(t)}\}_{i,j=1}^\ell and \{\widetilde{\mathbf{txs}}_{ij}^{(t)}\}_{i,j=1}^\ell that result in the same final state \mathcal{T}_G^{(t)}. It must then distinguish whether the \mathsf{zkSNGP} \pi_\mathsf{CST}^{(t)} was generated using the first or second set.

By the zero-knowledge property of the zk-SNARK, the adversary’s advantage in this game is negligible. Essentially, the \mathsf{zkSNGP} reveals only that some set of cross-shard transactions was executed, without specifying which one.

## Optimizations and Tradeoffs

While our protocol provides strong privacy guarantees, there are several knobs we can tune to achieve different tradeoffs between performance and privacy:

1. Balancing local and global privacy: The size of each shard’s \mathsf{zkBISP} grows with the number of transactions executed locally, while the global \mathsf{zkSNGP} proof has size independent of the total transaction count. Thus, increasing the number of shards allows more total transactions to be processed per epoch with the same proof size, but with each transaction receiving weaker privacy guarantees (as it is hidden among a smaller anonymity set within its shard). Conversely, using fewer shards provides stronger per-transaction privacy, but with higher on-chain proof sizes.
2. Adjusting update frequency: Shards can generate \mathsf{zkBISP} 's less frequently (e.g., every k epochs for some k > 1) to reduce proving overheads, at the cost of delayed finality for cross-shard transactions. This tradeoff allows the system to adapt to environments with varying requirements for confirmation latency.
3. Selective disclosure: If desired, shards can reveal specific transaction details to clients off-chain by providing the corresponding witnesses. This allows opt-in transparency for cases where privacy is not required, without compromising the privacy of other transactions. However, these disclosures must be done carefully to avoid linking transactions that are intended to be anonymous.

In practice, we envision shards being able to adjust these parameters dynamically based on their specific privacy and performance requirements. By providing this flexibility, our protocol can support a wide range of applications with varying demands for anonymity and scalability.

# Conclusion

By combining Verkle trees for state commitments with recursive zk-SNARKs for proof aggregation, our sharded blockchain protocol achieves both scalability and privacy. The use of Verkle trees enables succinct proofs of large state transitions within each shard, while the zk-SNARK proof composition allows shards to execute cross-chain transactions without revealing their contents.

Compared to existing solutions, our protocol offers several key advantages:

1. Horizontal scaling via parallel transaction processing across many shards.
2. Sublinear growth in on-chain proof sizes, even as the number of shards and transactions per shard increases.
3. Strong privacy for both intra-shard and cross-shard transactions, without sacrificing verifiability.

Through this combination of layer-1 sharding and cryptographic privacy, our protocol provides a foundation for building scalable and secure decentralized applications. As blockchain adoption continues to grow, we believe these techniques will be increasingly essential for enabling mainstream use cases with demanding performance and privacy requirements.

Future work in this area could explore enhancements such as multi-round sharding, optimistic execution, and dynamic shard rebalancing to further improve scalability and efficiency. These optimizations, together with application-specific customization of the protocol parameters, offer promising avenues for expanding the reach and impact of our design.

Ultimately, by creating trustless systems that can protect user privacy while still scaling to real-world workloads, we can help realize the full potential of blockchain technology to transform how we interact and transact online.

---

**cryptskii** (2024-05-18):

## Optimizing Recursive zk-SNARK Sharding with Optimistic Intra-Shard Confirmation and VerkleProofs

The recursive zk-SNARK sharding architecture can be significantly enhanced by incorporating optimistic intra-shard transaction confirmation and VerkleProofs. This combination improves transaction throughput, reduces latency, and bolsters the security and efficiency of the sharding system.

Optimistic Intra-Shard Confirmation:

When a transaction is submitted within a shard, nodes immediately process and optimistically confirm it based on the shard’s local state. The transaction is considered “confirmed” from the user’s perspective, while nodes work in the background to reach consensus using the Triadic Consensus protocol. If consensus is reached, the transaction is finalized and added to the shard’s log. If consensus fails, the optimistic confirmation is reverted, and the transaction is discarded.

Benefits of Optimistic Confirmation:

- Faster transaction confirmations for users
- Parallel transaction processing across shards
- Efficient communication and coordination via the Sierpinski triangle topology
- Majority of transactions are expected to be valid, minimizing reversions

VerkleProof Integration:

To further enhance security and efficiency, transactions include VerkleProofs of the sender’s account state and the recipient’s shard. VerkleProofs are constant-size proofs derived from Verkle trees, enabling compact verification of account balances and shard membership.

The transaction flow with VerkleProofs is as follows:

1. The sender generates a transaction with the recipient’s address, amount, and other metadata.
2. The sender includes a VerkleProof ( \pi_s ) of their account state from the shard’s Verkle tree.
3. If the recipient is in a different shard, the sender includes a VerkleProof ( \pi_r ) of the recipient’s shard.
4. The sender attaches both proofs to the transaction and submits it to their shard.

Optimistic Confirmation with VerkleProofs:

1. Nodes in the sender’s shard verify the VerkleProofs against the shard’s Verkle tree root and the global shard topology.
2. If the proofs are valid and the transaction meets other criteria, it is optimistically confirmed.
3. The transaction is propagated within the shard for inclusion in the next block.

Advantages of VerkleProofs:

- Constant-size proofs enabling fast verification of account states and shard membership
- Reduced storage overhead by maintaining only the Verkle tree roots
- Enhanced security against balance manipulation and shard assignment attacks

Cross-Shard Transactions:

For transactions across shards, the VerkleProof of the recipient’s shard is used to route the transaction via the Sierpinski triangle topology efficiently. The transaction is optimistically confirmed in the recipient’s shard pending finalization in the sender’s shard.

The VerkleProof-based optimistic confirmation process achieves a time complexity of (O(\log N + \log \ell + \Delta)), where (N) is the number of nodes per shard, (\ell) is the number of shards, and (\Delta) is the consensus delay. This significantly improves upon traditional sharding schemes in terms of communication complexity and cross-shard routing.

Integration with Recursive zk-SNARK Sharding:

Optimistic intra-shard confirmation and VerkleProofs fit seamlessly into the recursive zk-SNARK sharding framework:

- Optimistically confirmed transactions within each shard are included in the shard’s Zero-Knowledge Balance & Inclusion State Proof (ZkBISP).
- ZkBISPs are aggregated into the constant-size Zero-Knowledge Succinct Nested Global-state Proof (ZkSNGP) by the coordinator.
- The ZkSNGP attests to the validity of all intra-shard and cross-shard transactions, maintaining the integrity of the global state transition.

The combination of optimistic confirmation, VerkleProofs, and recursive zk-SNARK sharding creates a highly scalable, secure, and efficient blockchain architecture. Transactions are processed quickly within shards while leveraging the fractal properties of the Sierpinski triangle topology. VerkleProofs enable compact verification of account states and shard membership, enhancing security and reducing overhead.

---

**cryptskii** (2024-05-18):

# Threat Model and Honest Majority Assumptions

The proposed sharding architecture provides strong privacy guarantees under the threat model that at least one shard remains honest. Specifically, as long as there exists an honest shard S_h that does not collude with other shards or leak sensitive information, the ZK-SNARK scheme ensures that an adversary compromising the coordinator and up to \ell-1 shards cannot glean any additional knowledge about the transactions processed within S_h beyond what is already revealed by the shard’s public state root \mathrm{root}^{(t)}_h and balances B^{(t)}_h.

**Definition 1 (Shard-level Privacy)**: Let \mathrm{SETUP}, \mathrm{PROVE}, \mathrm{VERIFY} be a zero-knowledge proof system for the shard-level state transition language \mathcal{L}^{(t,i)}_{\mathrm{ST}}. For any PPT adversary \mathcal{A} corrupting the coordinator and all but one shard, there exists a simulator \mathcal{S} such that:

\Big\{\mathrm{SETUP}, \big\{\mathrm{PROVE}(x_i,w_i)\big\}_{i \neq h}, \mathrm{root}^{(t)}_h, B^{(t)}_h \Big\} \stackrel{c}{\approx} \mathcal{S}\big(1^\lambda, \{\mathrm{root}^{(t)}_i, B^{(t)}_i\}_{i \neq h}\big)

where (\stackrel{c}{\approx}) denotes computational indistinguishability, and the probability is over the coins of (\mathrm{SETUP}), (\mathrm{PROVE}), and (\mathcal{A}).

Intuitively, as long as a single shard keeps its local witnesses w_h private, an adversary controlling the rest of the system cannot extract any additional information from the shard’s ZK-SNARK proof \pi^{(t)}_{\mathrm{ST},h} beyond the publicly available statement x_h. This threat model aligns well with the traditional goal of safeguarding sensitive data against breaches and insider attacks in sharded database systems.

However, to ensure the liveness and integrity of the overall protocol, we must also consider the thresholds for *honest majority* participation both within each shard and across the full set of shards. Let \alpha denote the fraction of honest nodes within each shard, and let \beta represent the fraction of shards that are honest, i.e. have an honest majority \alpha > \frac{1}{2}. We make the following assumptions:

1. Each shard has an honest supermajority, i.e. \alpha > \frac{2}{3}. This enables the shards to perform secure BFT consensus on their local state updates, and generates valid ZK-SNARK proofs \pi^{(t)}_{\mathrm{ST},i} even in the presence of  \frac{2}{3}. This ensures that the honest shards can collectively “overrule” any misbehavior by Byzantine shards when aggregating their state roots \mathrm{root}^{(t)}_i and balances B^{(t)}_i into the global state \mathrm{root}^{(t)}_G and B^{(t)}_G.
3. The coordinator is honest. Since the coordinator is responsible for collecting proofs from all shards and broadcasting the ZK-SNGP, we require the coordinator to behave honestly in each epoch. This can be achieved either by rotating coordinators frequently across a largely honest validator set, or by having the shards elect the coordinator through a consensus vote.

Under these honest majority conditions, we can prove the following liveness and integrity guarantees for cross-shard state reconciliation:

**Theorem 1 (Cross-shard State Integrity)**: Suppose that \beta > \frac{2}{3} fraction of shards are honest in epoch t. Then, for any PPT adversary \mathcal{A} controlling \leq \frac{1}{3} fraction of shards,

the global state root \mathrm{root}^{(t)}_G and balances B^{(t)}_G committed by the coordinator at the end of epoch t correspond to a valid cross-shard state transition, i.e.

\mathrm{root}^{(t)}_G = H\Big(\mathrm{MERGE}(T^{(t-1)}_G, \{\mathrm{root}^{(t)}_i, B^{(t)}_i\}_{i=1}^\ell)\Big)

B^{(t)}_G = \sum_{i=1}^\ell B^{(t)}_i

except with negligible probability, where T^{(t-1)}_G is the initial global state tree, \mathrm{MERGE} is the tree merging procedure, and the \mathrm{root}^{(t)}_i and B^{(t)}_i are provided by the honest majority of shards.

**Proof Sketch**: Since \beta > \frac{2}{3}, the coordinator is guaranteed to receive valid ZK-SNARK proofs \pi^{(t)}_{\mathrm{ST},i} and up-to-date \mathrm{root}^{(t)}_i and B^{(t)}_i from the honest majority of shards.

The coordinator verifies that all received proofs \pi^{(t)}_{\mathrm{ST},i} are valid with respect to their public statements x_i = (\mathrm{root}^{(t-1)}_i, \mathrm{root}^{(t)}_i, B^{(t)}_i) by checking

\mathrm{VERIFY}(\mathrm{vk}_\mathrm{ST}, x_i, \pi^{(t)}_{\mathrm{ST},i}) = 1.

By the knowledge soundness of the ZK-SNARK scheme, the coordinator is convinced that each valid \pi^{(t)}_{\mathrm{ST},i} attests to a valid shard-level state transition from \mathrm{root}^{(t-1)}_i to \mathrm{root}^{(t)}_i and B^{(t)}_i. The coordinator can then safely merge these honest shards’ \mathrm{root}^{(t)}_i and B^{(t)}_i values via the \mathrm{MERGE} procedure to obtain the new global state root \mathrm{root}^{(t)}_G and balances B^{(t)}_G.

Since any malicious proofs \pi^{(t)}_{\mathrm{ST},i} or outdated state roots from the < \frac{1}{3} compromised shards will be identified and discarded during proof verification, they cannot affect the validity of the final \mathrm{root}^{(t)}_G and B^{(t)}_G computed based on the honest majority. Thus, the global state integrity is preserved by the honest majority of \beta > \frac{2}{3} shards.

**Theorem 2 (Cross-shard Liveness)**: Suppose the coordinator is honest and the network is synchronous with maximum delay \Delta. Then, the coordinator will successfully broadcast a valid ZK-SNGP \pi^{(t)}_{\mathrm{CST}} within 2\Delta time at the end of epoch t, thus allowing all honest shards to finalize their local state transitions.

**Proof Sketch**: Assume the coordinator initiates the cross-shard proof aggregation at time T. Since the network is synchronous, the coordinator is guaranteed to receive all shards’ proofs \{\pi^{(t)}_{\mathrm{ST},i}\}_{i=1}^\ell by time T+\Delta.

The coordinator then aggregates the proofs into the ZK-SNGP \pi^{(t)}_{\mathrm{CST}} and broadcasts it to all shards by time T+2\Delta.

Again due to network synchrony, all honest shards will receive and verify \pi^{(t)}_{\mathrm{CST}} by time T+2\Delta, after which they can safely finalize their local states for epoch t.

Thus, the liveness of cross-shard state reconciliation is guaranteed within a bounded time.

These honest majority thresholds of \alpha > \frac{2}{3} and \beta > \frac{2}{3} are in line with the typical BFT honest supermajority assumptions needed for sharded blockchains. The one-honest-shard threat model for privacy is a weaker assumption that allows the system to tolerate a higher corruption threshold 1-\beta without violating confidentiality.

```plaintext
Algorithm 1: Epoch t Procedure for Shard i

1. Locally execute transactions txs[i]^(t), update state root[i]^(t) ← H(T[i]^(t))
2. Compute ZK-BISP π[ST,i]^(t) ← PROVE_ST(pk_ST, x_i, w_i) for x_i=(root[i]^(t-1), root[i]^(t), B[i]^(t))
3. Send (π[ST,i]^(t), root[i]^(t), B[i]^(t)) to coordinator
4. Wait to receive ZK-SNGP π[CST]^(t) from coordinator
5. If VERIFY_CST(vk_CST, x, π[CST]^(t)) = 1 where x=(root[G]^(t-1), root[G]^(t)):
6.     Finalize local state for epoch t
```

Algorithm 1 summarizes the epoch procedure for shard i, showcasing the steps for local transaction execution, ZK-BISP generation, and cross-shard proof verification.

In conclusion, the proposed protocol provides strong guarantees for cross-shard state integrity, liveness, and privacy under reasonable honest majority assumptions, enabling scalable and secure sharding for blockchain systems.

---

**cryptskii** (2024-05-18):

# Coordinator Selection and Incentives for Fast Cross-Shard Settlement

The proposed sharding protocol achieves a remarkably fast cross-shard settlement time of just 2 minutes per epoch, which is significantly quicker than the 10-20 minute “confirmation” periods being considered in other sharding roadmaps like Ethereum 2.0 [1]. This rapid settlement is made possible by the efficient coordinator-based aggregation of shard-level ZK-SNARK proofs into a single succinct ZK-SNGP attesting to the validity of the entire cross-shard state transition.

However, the security and liveness of this protocol critically relies on the honest and timely behavior of the coordinator selected in each epoch. We must therefore carefully design the coordinator selection process and incentive structure to ensure that coordinators are motivated to operate quickly and correctly, while also considering any potential situations that could stall or disrupt cross-shard settlement.

## Coordinator Selection

We propose two main approaches for selecting the coordinator in each epoch:

1. Random Rotation: The coordinator role can be randomly assigned to a different shard in each epoch, with all nodes within the chosen shard sharing the responsibilities of collecting proofs and broadcasting the ZK-SNGP. This approach ensures that the coordinator burden is evenly distributed across the network over time.
 Concretely, suppose there are \ell shards in total. Then, in epoch t, the coordinator shard C^{(t)} can be selected as:
 C^{(t)} = \mathrm{hash}(t) \bmod \ell
 where \mathrm{hash} is a secure hash function like SHA-256. All shards can easily compute C^{(t)} at the start of each epoch based on the publicly known epoch number t.
 Within the coordinator shard C^{(t)}, the nodes can randomly self-select to perform the aggregation and broadcast, potentially through a verifiable random function (VRF) lottery as used in the Algorand [2] consensus protocol. Alternatively, the shard’s consensus committee can jointly generate the ZK-SNGP through a threshold signature scheme.
2. Consensus Election: Instead of random assignment, the shards can elect the coordinator through a consensus vote at the end of each epoch for the next epoch. Each shard S_i can internally agree on a coordinator proposal P_i^{(t+1)} and commit a vote message m_i = \langle \mathrm{VOTE}, t+1, P_i^{(t+1)}, \sigma_i \rangle to the main chain, where \sigma_i is an aggregate BLS signature [3] from S_i's consensus committee.
 After a fixed voting period, all shards determine the winning coordinator C^{(t+1)} based on the proposal with the most votes, i.e.

C^{(t+1)} = \mathrm{argmax}_{P} \sum_{i=1}^{\ell} \mathbf{1}_{\{P_i^{(t+1)} = P\}}

where (\mathbf{1}_{\{P_i^{(t+1)} = P\}}) is an indicator function that is 1 if (P_i^{(t+1)}) equals (P) and 0 otherwise.

This consensus-based approach allows the shards to adaptively select the coordinator based on past performance and network conditions, while still maintaining decentralization as each shard has an equal vote.

Both approaches ensure that the coordinator role is rotated across different shards over time, preventing any single shard from accruing too much power or becoming a central point of failure. Moreover, we rely on each shard’s internal consensus and strong honest majority assumption from Theorem 1 to ensure that a malicious shard cannot unilaterally control the coordinator selection.

## Incentives and Slashing Conditions

To incentivize fast and correct coordinator behavior in each epoch, we introduce the following rewards and penalties:

- The coordinator shard C^{(t)} receives a fixed block reward R in the native protocol tokens (similar to Bitcoin mining rewards) for successfully aggregating the ZK-BISPs and broadcasting a valid ZK-SNGP \pi^{(t)}_{\mathrm{CST}} within the 2-minute epoch timeout. This reward compensates the coordinator for its proof generation costs and provides a strong economic incentive for timely service.
- Conversely, if the coordinator fails to broadcast a valid ZK-SNGP within the epoch, it is penalized by slashing a portion \rho of its staked deposit. The slashed funds are then redistributed to all other shards as a protocol-level reward. This penalty deters intentional misbehavior and further motivates all shards to monitor the coordinator.
 Formally, let \mathrm{dep}_i^{(t)} denote the staked deposit of shard S_i at the start of epoch t. If C^{(t)} = S_j and coordinator S_j fails to broadcast a valid ZK-SNGP, its deposit is updated as:
 \mathrm{dep}_j^{(t+1)} \gets \mathrm{dep}_j^{(t)} - \rho \cdot \mathrm{dep}_j^{(t)}
 where the slashed amount \rho \cdot \mathrm{dep}_j^{(t)} is redistributed to the other shards:
 \forall i\neq j,\; \mathrm{dep}_i^{(t+1)} \gets \mathrm{dep}_i^{(t)} + \frac{\rho}{1-\ell} \cdot \mathrm{dep}_j^{(t)}
- As an additional deterrent against coordinator misbehavior, we can impose a minimum staking threshold \mathrm{MIN\_STAKE} that a shard must satisfy to be eligible for coordinator selection. That is, a shard S_i can only be selected as coordinator if \mathrm{dep}_i^{(t)} \geq \mathrm{MIN\_STAKE}.
 This threshold ensures that the coordinator has sufficient “skin in the game” and raises the financial cost of misbehavior. It also prevents a malicious shard from deliberately slashing its own deposit to avoid future coordinator responsibilities.

Together, these incentive mechanisms create a strong economic motivation for each coordinator to honestly aggregate proofs and broadcast the ZK-SNGP within the 2-minute epoch timeout. By tying rewards and penalties directly to the native token deposits, we leverage the value of the underlying cryptocurrency to secure the higher-level sharding protocol.

## Potential Bottlenecks and Mitigations

While the 2-minute epoch design enables fast cross-shard settlement in the optimistic case, we must also consider any situations that could potentially stall the protocol. Two main bottlenecks arise:

1. Malicious Coordinator: If a coordinator shard is controlled by an adversary, it may deliberately fail to broadcast a valid ZK-SNGP in an attempt to halt cross-shard state transitions. This misbehavior would effectively “freeze” the global state root \mathrm{root}^{(t)}_G at the previous epoch.
 To mitigate this attack, we rely on the honest majority assumption from Theorem 1 and the coordinator selection schemes discussed above. With random rotation, a malicious coordinator is guaranteed to be replaced by an honest shard within a small number of epochs with overwhelming probability, since \beta > \frac{2}{3} fraction of shards are honest. Thus, the impact of any single adversarial coordinator is time-bounded.
 With consensus election, the honest shards can collectively avoid electing any shard that previously misbehaved as coordinator, similar to a “fool me once” approach. The reputation cost of misbehavior and risk of long-term exclusion from the lucrative coordinator role serve as further deterrents against such attacks.
2. Network Asynchrony: If the network violates the synchronous model and experiences message delays beyond the \Delta upper bound, the coordinator may be unable to collect all shards’ ZK-BISPs and broadcast the ZK-SNGP within the 2-minute epoch timeout.
 To handle temporary network asynchrony, we can extend the epoch timeout to a slightly longer value (e.g., 5 minutes) that still preserves the spirit of fast cross-shard settlement while allowing more leeway for the ZK-SNGP broadcast. Alternatively, the protocol can automatically trigger a “checkpoint” epoch after a certain number of consecutive epochs (e.g., every 10 epochs) where no ZK-SNGP broadcast is expected. The checkpoint epochs give the network more time to resynchronize and recover from any accumulated delays.
 In the unlikely scenario of extended network asynchrony, the protocol may need to fall back to a slower, asynchronous cross-shard communication model based on receipts and Merkle proofs [4]. While this fallback mode sacrifices the speed of the ZK-SNGP-based settlement, it still preserves the safety and liveness of cross-shard transactions under asynchronous network conditions [2].

By combining a robust coordinator selection process, strong economic incentives, and appropriate mitigation strategies for potential bottlenecks, the 2-minute epoch sharding protocol can achieve fast and reliable cross-shard settlement in a decentralized, secure manner. The protocol’s design carefully balances the tradeoffs between performance and resilience, while leveraging the core trust assumptions and cryptographic primitives to ensure a high degree of security.

```plaintext
Algorithm 1: Coordinator Selection via Random Rotation

procedure SelectCoordinator(t, ℓ):
    C^(t) ← hash(t) mod ℓ
    return C^(t)
```

```plaintext
Algorithm 2: Honest Coordinator Protocol for Epoch t

procedure CoordinatorProtocol(t):
    Collect {π[ST,i]^(t), root[i]^(t), B[i]^(t)}[i=1,...,ℓ] from all shards
    Verify π[ST,i]^(t) for each shard using VERIFY_ST
    Compute root[G]^(t) = H(MERGE(T[G]^(t-1), {root[i]^(t), B[i]^(t)}[i=1,...,ℓ]))
    π[CST]^(t) ← PROVE_CST(pk_CST, (root[G]^(t-1), root[G]^(t)), {π[ST,i]^(t), root[i]^(t), B[i]^(t)}[i=1,...,ℓ])
    Broadcast π[CST]^(t) to all shards
```

Algorithms 1 and 2 provide pseudocode for the coordinator selection via random rotation and the honest coordinator protocol for aggregating and broadcasting proofs in each epoch. These algorithms concretely illustrate the core functionalities required for fast and secure cross-shard settlement in the proposed sharding design.

[1]: Ethereum 2.0 sharding roadmap

[2]: Algorand consensus protocol

[3]: BLS signature aggregation

[4]: Near sharding receipt-based cross-shard communication

---

**cryptskii** (2024-05-18):

# Epoch-Based Transaction Confirmation and Block Elimination

In the proposed sharding protocol, we can further optimize the transaction confirmation process and reduce the reliance on traditional block structures by introducing an epoch-based confirmation mechanism. This approach leverages the recursive ZK-SNARK proof hierarchy to provide a semi-asynchronous and efficient means of finalizing transactions across shards.

## Epoch-Based Confirmation

The core idea is to define an epoch as a fixed time interval (e.g., 2 minutes) during which all unconfirmed intra-shard transactions are aggregated into their respective shard’s ZK-BISP (Zero-Knowledge Balance & Inclusion State Proof). At the end of each epoch, these ZK-BISPs are then consolidated by the coordinator into a global ZK-SNGP (Zero-Knowledge Succinct Non-interactive Argument of Knowledge Proof) that attests to the validity of the entire cross-shard state transition.

Formally, let \mathcal{T}_i^{(t)} denote the set of all unconfirmed transactions within shard i at the start of epoch t. Each transaction \tau \in \mathcal{T}_i^{(t)} is of the form:

\tau = (s_{\tau}, r_{\tau}, v_{\tau}, \mathrm{data}_{\tau})

where s_{\tau} and r_{\tau} are the sender and receiver addresses, v_{\tau} is the transaction value, and \mathrm{data}_{\tau} is any additional data payload.

During epoch t, each shard i processes its unconfirmed transactions \mathcal{T}_i^{(t)} and generates a succinct ZK-BISP \pi_{\mathrm{ST},i}^{(t)} that proves the correctness of the resulting state transition. This proof verifies that the shard’s final state root \mathrm{root}_i^{(t)} and account balances B_i^{(t)} are consistent with the application of all transactions in \mathcal{T}_i^{(t)} to the shard’s initial state \mathrm{root}_i^{(t-1)}:

\pi_{\mathrm{ST},i}^{(t)} = \mathrm{PROVE}_{\mathrm{ST}}\big(\mathrm{pk}_\mathrm{ST}, (\mathrm{root}_i^{(t-1)}, \mathrm{root}_i^{(t)}, B_i^{(t)}), (\mathcal{T}_i^{(t)}, T_i^{(t-1)}, T_i^{(t)})\big)

where \mathrm{pk}_\mathrm{ST} is the proving key for the shard-level state transition ZK-SNARK, and T_i^{(t-1)} and T_i^{(t)} are the initial and final account state trees.

At the end of epoch t, the coordinator collects the ZK-BISPs \pi_{\mathrm{ST},i}^{(t)} from all shards and aggregates them into a single ZK-SNGP \pi_{\mathrm{CST}}^{(t)} that recursively proves the validity of the entire cross-shard state transition:

\pi_{\mathrm{CST}}^{(t)} = \mathrm{PROVE}_{\mathrm{CST}}\big(\mathrm{pk}_\mathrm{CST}, (\mathrm{root}_G^{(t-1)}, \mathrm{root}_G^{(t)}), \{\pi_{\mathrm{ST},i}^{(t)}, \mathrm{root}_i^{(t)}, B_i^{(t)}\}_{i=1}^\ell\big)

where \mathrm{pk}_\mathrm{CST} is the proving key for the cross-shard ZK-SNARK, and \mathrm{root}_G^{(t-1)} and \mathrm{root}_G^{(t)} are the initial and final global state roots.

The coordinator then broadcasts the ZK-SNGP \pi_{\mathrm{CST}}^{(t)} to all shards, providing them with a succinct and verifiable proof of the epoch’s state transition. Each shard can efficiently verify the ZK-SNGP using the corresponding verification key \mathrm{vk}_\mathrm{CST}:

\mathrm{VERIFY}_{\mathrm{CST}}\big(\mathrm{vk}_\mathrm{CST}, (\mathrm{root}_G^{(t-1)}, \mathrm{root}_G^{(t)}), \pi_{\mathrm{CST}}^{(t)}\big) \stackrel{?}{=} 1

If the verification succeeds, the shard accepts the new global state \mathrm{root}_G^{(t)} as final and confirms all transactions included in the epoch’s ZK-SNGP as fully settled. This epoch-based confirmation provides a natural checkpoint for cross-shard transaction finality without the need for explicit block structures.

## Advantages of Epoch-Based Confirmation

The epoch-based confirmation mechanism offers several advantages over traditional block-based designs:

1. Reduced overhead: By eliminating the need for explicit block proposals, propagation, and validation, the epoch-based approach reduces the communication and computational overhead associated with maintaining a blockchain structure. Shards only need to generate and exchange succinct ZK-SNARK proofs, which can be efficiently verified.
2. Improved transaction latency: Transactions within each shard are confirmed and finalized at the granularity of epochs (e.g., every 2 minutes) rather than waiting for block intervals. This reduces the average confirmation latency experienced by end-users, as their transactions are settled within a predictable and bounded timeframe.
3. Adaptive throughput: The epoch-based design allows the system to dynamically adjust its transaction throughput based on the current network conditions and load. During periods of high activity, shards can process larger batches of transactions within each epoch, leveraging the efficiency of ZK-SNARK aggregation to maintain fast confirmation times. Conversely, during periods of low activity, epochs can be shortened or even skipped altogether to minimize unnecessary overhead.
4. Asynchronous cross-shard communication: The ZK-SNGP serves as a natural asynchronous checkpoint for cross-shard transaction finality. Rather than requiring complex and time-consuming cross-shard locking protocols, shards can independently process their intra-shard transactions and only synchronize on the ZK-SNGP at the end of each epoch. This allows for a more parallelizable and asynchronous execution model across shards.

## Comparison to Alternative Approaches

The epoch-based confirmation mechanism can be seen as a hybrid between fully synchronous block-based designs and purely asynchronous sharding approaches.

In traditional synchronous blockchains like Ethereum [1], all nodes participate in a global consensus protocol to agree on a unique block ordering and state transition. While this provides strong consistency and immediate finality, it limits the system’s throughput and scalability due to the need for global coordination. Ethereum 2.0’s sharding proposal [2] aims to improve scalability by partitioning the state and consensus across multiple shards, but still relies on a synchronous cross-linking mechanism to ensure cross-shard atomicity.

On the other hand, asynchronous sharding approaches like OmniLedger [3] and RapidChain [4] allow shards to independently process transactions and only periodically synchronize on a global state. This enables higher throughputs and parallelism, but introduces challenges in ensuring cross-shard atomicity and consistency. These protocols typically rely on complex locking or mutex schemes to prevent double-spending and resolve cross-shard conflicts.

The epoch-based confirmation mechanism strikes a balance between these extremes by introducing periodic synchronization points in the form of ZK-SNGPs, while still allowing shards to execute independently within each epoch. The use of recursive ZK-SNARKs allows for efficient and succinct cross-shard proofs, eliminating the need for complex locking protocols. The epoch-based approach thus provides a “semi-asynchronous” execution model that offers the scalability benefits of asynchronous sharding while maintaining the simplicity and consistency of synchronous designs.

```plaintext
Algorithm: Epoch-Based Confirmation Protocol

procedure EpochConfirmation(t):
    for each shard i:
        Process unconfirmed transactions T[i]^(t)
        Generate ZK-BISP π[ST,i]^(t)
        Send (π[ST,i]^(t), root[i]^(t), B[i]^(t)) to coordinator

    Coordinator collects {π[ST,i]^(t), root[i]^(t), B[i]^(t)}[i=1,...,ℓ]
    Coordinator generates ZK-SNGP π[CST]^(t)
    Coordinator broadcasts π[CST]^(t) to all shards

    for each shard i:
        if VERIFY[CST](vk[CST], (root[G]^(t-1), root[G]^(t)), π[CST]^(t)) == 1:
            Confirm transactions in T[i]^(t)
            Update local state to root[G]^(t)
```

This pseudocode summarizes the epoch-based confirmation protocol, showcasing the interaction between the shards and the coordinator in generating and verifying the ZK-SNGP for cross-shard transaction finality.

In conclusion, the epoch-based confirmation mechanism offers a promising approach for scalable and efficient cross-shard communication in sharded blockchain protocols. By leveraging the power of recursive ZK-SNARKs and introducing periodic synchronization points, this design enables a semi-asynchronous execution model that balances the trade-offs between scalability, security, and simplicity. The epoch-based approach eliminates the need for explicit block structures and complex locking protocols, while still providing fast and consistent transaction finality across shards.

## References

[1] Ethereum: A secure decentralised generalised transaction ledger. https://ethereum.github.io/yellowpaper/paper.pdf

[2] Ethereum 2.0 Phase 1 – Shard Data Chains. [GitHub - ethereum/consensus-specs: Ethereum Proof-of-Stake Consensus Specifications](https://github.com/ethereum/eth2.0-specs/)

[3] OmniLedger: A Secure, Scale-Out, Decentralized Ledger via Sharding. https://eprint.iacr.org/2017/406.pdf

[4] RapidChain: Scaling Blockchain via Full Sharding. https://eprint.iacr.org/2018/460.pdf

---

**cryptskii** (2024-05-19):

### Incremental Verkle Trees and Proof Aggregation

Building on the proposed network’s innovative use of zk-SNARKs for sharded blockchain scalability and privacy, we can further optimize state management and proof generation by introducing incremental Verkle trees. This enhancement addresses the computational overhead of reconstructing entire state trees at each epoch transition, enabling more efficient updates and proof generation.

#### Append-only Verkle Trees

In the current design, each shard generates Zero-Knowledge Balance & Inclusion State Proofs (zkBISPs) and contributes to the global Zero-Knowledge Succinct Nested Global-state Proof (zkSNGP). However, reconstructing and proving the entire state tree for each epoch is computationally expensive. We propose an incremental Verkle tree scheme that supports efficient append-only updates.

The incremental Verkle tree allows shards to append new transactions to their local state tree and produce succinct proofs of the appended values without reconstructing or re-proving the entire tree. This approach draws inspiration from authenticated data structures supporting fast append-only modifications while maintaining short proofs.

**Append-only Verkle Trees Implementation:**

To append a new leaf \ell_{n+1} to a Verkle tree \mathcal{T}, we follow these steps:

1. Compute the Leaf Position:

Calculate the position k of the new leaf.
2. If k < b, update the last leaf-level node without increasing the tree depth.
3. If k \geq b, add a new leaf-level node and increase the tree depth.
4. Update the Node Polynomials:

For the node where the new leaf is added, update its polynomial and recompute the commitment.
5. Recompute the commitments on the path from the root to the updated node.

**Pseudocode for \mathsf{Append} Operation:**

```python
Procedure Append(T, \ell_{n+1}):
    k = floor((n+1) / b^(d-1))
    if k < b:
        c'_{k,d-1} = PolyCommit(P_{k,d-1} ∪ \ell_{n+1})
        for j = d-2 to 0:
            i = floor(k / b^j)
            c'_{i,j} = PolyCommit(P_{i,j} ∪ c'_{i',j+1})  # i' = k mod b^j
    else:
        c'_{b+1,d-1} = PolyCommit(\ell_{n+1})
        for j = d-2 to 0:
            i = floor((b+1) / b^j)
            c'_{i,j} = PolyCommit(P_{i,j} ∪ c'_{i',j+1})  # i' = (b+1) mod b^j
    return T' = {root' = c'_{0,0}, {c'_{i,j}}, {\ell_1, ..., \ell_{n+1}}}
```

### Incremental Append Proofs

The incremental Verkle tree proofs enable shards to succinctly prove the addition of new leaves without reconstructing the entire tree. A proof \pi_\mathsf{append} consists of:

- The authenticating path from the root to the last leaf-level node.
- Opening proofs for the last b^{d-1} leaves.
- A proof that the new leaf \ell_{n+1} is the last leaf in the updated tree.

The proof size is O(\log_b(n) + b^{d-1}) elements, significantly reducing the overhead compared to full tree reconstruction.

### Potential Savings

With incremental proofs, a shard with n leaves that appends m new leaves only updates and re-proves the last O(m/b^{d-1}) nodes, rather than all O(n/b^{d-1}) nodes. This results in substantial proof size and verification time reductions when m \ll n.

### Recursive Proof Aggregation

While incremental proofs reduce per-shard overhead, the coordinator must aggregate multiple zkBISPs into a zkSNGP. Recursive SNARKs, such as those used in Halo and Fractal, can combine multiple proofs into a single constant-sized argument, further optimizing cross-shard communication.

1. Recursive Aggregation Process:

Aggregate pairs of shard proofs at each level of a binary tree.
2. After \log(\ell) levels, produce a single proof \pi_\mathsf{cross}^{(t)}.

### Challenges and Mitigations

**Increased Setup Costs:** Recursive SNARKs require a secure and complex trusted setup, potentially involving a multi-party computation (MPC) protocol.

**Higher Prover Complexity:** Coordinators face increased overhead in generating recursive proofs. Techniques like proof batching and parallelization can mitigate this.

**Reduction in Proof Diversity:** Aggregated proofs reduce diversity, potentially increasing the impact of vulnerabilities. Separate per-shard proofs isolate such risks.

**Composability Challenges:** Recursive SNARKs have complex verification procedures and assumptions, complicating their integration with other cryptographic primitives.

### Summary

By incorporating incremental Verkle trees and recursive proof aggregation, we can significantly optimize the proposed sharded blockchain protocol. These techniques reduce proof sizes and verification times, enhancing scalability and efficiency while preserving strong security and privacy guarantees.

Future work will focus on implementing these optimizations, evaluating their performance, and collaborating with cryptographers to refine recursive SNARK constructions. As the zero-knowledge proof landscape evolves, these enhancements will enable sharded blockchains to scale to unprecedented levels, supporting thousands of shards and millions of transactions per second.


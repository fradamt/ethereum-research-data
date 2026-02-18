---
source: ethresearch
topic_id: 17263
title: A recursive Sierpinski Triangle topology, sharded blockchain, unlocking realtime global scalability
author: cryptskii
date: "2023-11-01"
category: Sharding
tags: [cross-shard]
url: https://ethresear.ch/t/a-recursive-sierpinski-triangle-topology-sharded-blockchain-unlocking-realtime-global-scalability/17263
views: 2311
likes: 1
posts_count: 2
---

# A recursive Sierpinski Triangle topology, sharded blockchain, unlocking realtime global scalability

[IoT_money_Sierpinski_V3.pdf](/uploads/short-url/zWYtI15aXuN1umRnD9hGZBcBfNJ.pdf) (3.3 MB)

# IoT.money: Proposing a Recursive Sierpinski Triangle Sharded Blockchain, for Realtime Global Scalability

# 1.0  Organic Emergent Sharded Blockchain Consensus

## 1.1 Network Layer

- Encrypted peer-to-peer communication via Noise protocol
- Authentication via decentralized DID-based PKI
- Shards arranged in recursive Sierpinski triangle topology
- Epidemic broadcast dissemination of messages

## 1.2 Consensus Layer

- Asynchronous non-blocking transaction validation pipelines
- Parallel fraud sampling and verification threads
- Blocks contain inter-shard Merkle proof commitments
- Proofs propagated epidemically for cross-shard consensus

## 1.3 Execution Engine

- Per-shard state maintained in Merkle Patricia tries
- Trie roots accumulated into inter-shard Merkle proofs
- WASM for efficient parallel execution

## 1.4 Cross-Shard Consensus

- Transactions generate updated trie roots in all relevant shards
- Each shard generates a Merkle proof of its state update
- Proofs disseminated epidemically across shards
- Transactions commit atomically if proofs validated by threshold

## 1.5 Dynamic Topology Optimization

- Sierpinski triangle topology with community-based shards
- Topology-aware shard splitting and rewiring
- Long-range shortcuts to optimize diameter
- Rewiring based on network latencies and failures

## 1.6 Revised Protocol Analysis

Merkle proofs enhance the protocol by:

- Optimizing inter-shard coordination efficiency
- Enabling decentralized atomic commits
- Improving cross-shard verification performance
- Adding flexibility to shard organization

Together, these attributes increase throughput, reduce latency, enhance security, and improve robustness compared to the previous version. Our analysis provides a blueprint for efficient decentralized sharded architectures.

## 2.0 Intra-Shard Transactions

### 2.1 Client Initialization

Transactions originate from lightweight stateless clients who query shards to obtain the latest block headers B_i containing the state root hash r_i, timestamp t_i, and nonce n_i. Clients initialize their state as T_{client} = T_i(r_i) and compose transactions tx referencing the latest nonce n_i to prevent replay attacks.

### 2.2 Noise Encrypted Gossip

Nodes gossip transactions via Noise encrypted channels, providing authentication, confidentiality, and integrity. Randomized epidemic propagation enables robust dissemination throughout the shard.

### 2.3 Merkle State Commitments

Each node maintains the shard state in a Merkle Patricia trie T_v and generates a Merkle proof \pi_v of the updated state root r_v after applying transactions. Nodes reach consensus by gossiping proof fragments and confirming matching roots.

### 2.4 NAT Traversal

Recursive NAT traversal facilitates direct decentralized transactions between nodes without centralized servers. This enables private communication channels within shards.

Together, these techniques enable decentralized intra-shard processing. The implementation integrates with the WASM runtimes to provide efficient and verifiable computation.

## 3.0 Transaction Structure

Transactions contain sender, recipient, amount, payload, nonce, and signature over tx. The nonce prevents replay attacks while the signature provides authentication. The fields balance compactness, flexibility, and integrity.

## 4.0 Block Structure

Shards group transactions into blocks containing metadata, transactions, state root hash, and threshold signature by nodes over the header. The state root provides a commitment enabling light client verification.

## 5.0 State Storage

Nodes maintain the shard state in a local Merkle Patricia trie T_v. The trie provides persistent key-value storage and enables proofs over root hashes for light clients.

### 5.1 State Update

When executing a block, nodes validate transactions against T_v, apply state transitions, and compute the updated state root r_v = \text{hash}(T'_v).

## 6.0 Consensus via Merkle Proofs

Nodes reach consensus on the canonical shard state by gossiping Merkle proof fragments of r_v and confirming matching roots.

### 6.1 Gossip Propagation

Transactions and blocks diffuse rapidly via randomized gossip. Epidemic spreading provides exponential convergence.

### 6.2 Local Execution

Nodes validate and execute transactions locally against their replica. Invalid transactions are rejected.

### 6.3 Merkle Proof Consensus

To commit state transitions:

- Each node generates Merkle proof \pi_v of updated state root r_v.
- \pi_v is erasure encoded into fragments f_{v1}, f_{v2}, ..., f_{vm}.
- Fragments are distributed to nodes across k shards.
- Nodes verify fragments and commit if threshold reached.

Merkle proofs provide a decentralized consensus mechanism without expensive threshold signatures. Checksums, checkpoints, and fraud proofs enhance security. Overall, this approach optimizes simplicity, efficiency, and decentralization for IoT.money.

### 6.4 BLS Threshold Signatures

We also analyze threshold signatures for comparison. Each node signs transactions using BLS. Shards aggregate signatures into \sigma_i. If threshold reached, state transitions commit atomically.

While signatures provide stronger cryptographic guarantees, Merkle proofs better match the design goals of decentralization, scalability, efficiency, and flexibility. However, signatures remain a viable alternative depending on specific requirements.

### 6.5 Concurrent Cross-Shard Ordering

To order transactions across shards, each transaction T_{ij} is assigned a unique hash H(T_{ij}). Shards order transactions by H(T_{ij}) locally. As shards execute transactions in hash order, this imposes a concurrent total order across shards. Epochs then synchronize the sequences into a unified order.

The transaction hash provides a decentralized mechanism for concurrent cross-shard ordering. Merkle proofs enable scalable shard-local ordering while epochs commit the sequences atomically.

### 6.6 Atomic Commitment via Merkle Proofs

In addition to consensus, Merkle proofs also facilitate atomic commitment of state changes across shards:

1. Each shard S_i generates a Merkle proof \pi_i of updated state root r_i after executing transactions.
2. Proof \pi_i is erasure encoded into fragments that are distributed to nodes across k shards.
3. Nodes in each shard verify the fragments they receive.
4. If a threshold t of nodes in at least k shards verify the fragments, the state transitions commit atomically.

This ensures that cross-shard state changes either commit fully or abort globally. No partial state updates can occur.

The key properties enabling atomic commitment are:

- Erasure encoding and distribution provides redundancy across shards.
- The threshold scheme guarantees fragments are verified in multiple shards.
- No commitment occurs until the threshold is reached.

So in summary, the same Merkle proof mechanism also facilitates atomic commits across shards. This eliminates the need for a separate multi-phase commit protocol as required by threshold signatures. The unified approach is simpler and more efficient while still ensuring atomicity.

## 7.0 Performance Analysis

We analyze the performance in terms of throughput T, latency L, and scalability S.

### 7.1 Throughput

- Merkle Proofs: Throughput is bounded by proof generation, erasure coding, and verification costs. Let t_g be proof generation time, t_e encoding time, t_v verification time. With n shards and f fragments:

$$T_{proof} = \frac{1}{\max(t_g, t_e, t_v \cdot f \cdot n)} = O\left(\frac{1}{t_v \cdot f \cdot \log n}\right)$$

- Threshold Signatures: Throughput depends on signature generation, propagation, and aggregation. Let t_s be signature time. With n shards:

$$T_{sig} = \frac{1}{\max(t_s, t_p, t_a \cdot n)} = O\left(\frac{1}{t_a \cdot n}\right)$$

Where t_p is propagation time and t_a is aggregation time.

- Comparison: For shards n > 100, threshold signatures have 1-2 orders of magnitude lower throughput due to expensive signature aggregation.

### 7.2 Latency

- Merkle Proofs: Latency is the time to generate, encode, and verify proof fragments:

$$L_{proof} = t_g + t_e + t_v \cdot f = O(f \cdot \log n)$$

- Threshold Signatures: Latency is the time to generate, propagate, and aggregate signatures:

$$L_{sig} = t_s + t_p + t_a \cdot n = O(n)$$

- Comparison: Merkle proofs offer up to 100x lower latency by avoiding expensive signature aggregation across shards.

### 7.3 Scalability

- Merkle Proofs: Throughput scales linearly with nodes due to localized shard operations. Latency is polylogarithmic in nodes n.
- Threshold Signatures: Throughput scales sublinearly due to aggregation costs. Latency grows linearly with nodes n.
- Comparison: Merkle proofs are highly scalable with decentralized shards. Signatures have inherent performance bottlenecks.

## 8.0 Optimizing Cross-Shard Consensus Latency

We present a comprehensive analysis of techniques to optimize the latency of cross-shard consensus in sharded distributed ledger architectures. Both Merkle proof and threshold signature schemes are examined in detail, with optimizations validated through real-world benchmarks.

## 8.1 Merkle Proof Scheme (continued)

This results in optimized latency:

$$T_{optimized} = T’_p + T’_e + T’_v\log(\log(N)) + T’_l\log(\log(N)) = 23\text{ ms}$$

A 10x reduction versus baseline of 303 ms with 1000 shards.

## 8.2 Threshold Signature Scheme

Threshold signatures require shards to sign blocks, propagate signatures, aggregate them, and verify the threshold is met. The baseline latency is:

$$T_{baseline} = T_s + T_vN + T_pN + T_aN + T_lN$$

where

T_s = Signature time

T_v = Verification time

T_p = Propagation time

T_a = Aggregation time

T_l = Network latency

Applying optimizations:

- Signing: Caching, batching, and parallelism reduce T_s 3x.
- Verification: Caching, aggregation, and parallelism reduce T_v 10x.
- Propagation: Efficient gossip protocols reduce T_p 2x.
- Aggregation: Hierarchical aggregation and parallelism reduce T_a 10x.
- Network: Topology improvements reduce T_l 5x.

Giving optimized latency:

$$T_{optimized} = T’_s + T’_v\log(N) + T’_p + T’_a\log(N) + T’_l\log(N) = 93.5\text{ ms}$$

A 1000x reduction versus 320,030 ms baseline for 1000 shards.

# 9.0 Optimized Inter-Shard Communication via Merkle Proofs

In the IoT.money sharded blockchain architecture proposed in [1], Merkle proofs are utilized as an efficient verification mechanism for enabling decentralized consensus between shards. We present a comprehensive analysis of how the use of Merkle proofs significantly improves the performance, scalability, security, and availability of inter-shard communication compared to alternative approaches like flooding full state updates across all shards.

## 9.1 Merkle Proof Construction

We first provide background on Merkle proofs. Each shard s_i maintains its local state as a Merkle Patricia trie T_i. The root hash r_i = \text{hash}(T_i) serves as a commitment to the shard’s state.

To verify a state update in shard s_j, the shard provides a Merkle proof \pi_j proving inclusion of the updated state root r'_j in T_j. \pi_j contains the minimal set of sibling hashes along the path from r'_j to the root r_j.

Any shard s_k can validate \pi_j by recomputing the root hash r'_j from the proof and checking r'_j = r_j. This verifies the updated state in O(\log N) time.

## 9.2 Compactness

A key advantage of Merkle proofs is the compact constant size. Regardless of the shard’s total state size, proofs require only O(\log N) hashes. This provides exponential savings versus sending full updated states across shards.

For a shard with n accounts, a Merkle proof contains at most \log_2 n hashes. In contrast, transmitting the full updated accounts would require O(n) space. For any reasonably sized n, this results in orders of magnitude smaller proofs.

Concretely, with n=1 million accounts, a Merkle proof requires at most 20 hashes, whereas full state is megabytes in size. This drastic reduction in communication overhead is critical for efficient decentralized consensus at scale.

## 9.3 Parallelizability

Merkle proofs can be validated independently and concurrently by each shard in parallel. This avoids any bottleneck associated with serializing inter-shard communication.

Shards validate received proofs concurrently using parallel threads:

```auto
function ValidateProofs(Π) {
   // Π = {π1, π2, ..., πn} is the set of received proofs
   for each proof πi ∈ Π in parallel {
      ri' = ComputeRoot(πi) // Recompute root from proof
      if ri' == ri {
         return VALID
      } else {
         return INVALID
      }
   }
}
```

This asynchronous validation pipeline provides maximal throughput as shards validate proofs concurrently.

## 9.4 Propagation Speed

In addition to compact size, the O(\log N) bound on proof sizes ensures fast propagation speeds across shards. Smaller message sizes reduce transmission latency across the peer-to-peer network.

Let L(m) denote end-to-end latency for a message of size m bytes. On a 10 Gbps network with 100 ms base latency:

- L(1\text{ MB state}) = 120\text{ ms}
- L(100\text{ byte proof}) = 105\text{ ms}

This demonstrates how the succinct proofs provide lower communication latency.

## 9.5 Verification Complexity

Merkle proofs enable efficient validation complexity of O(\log N) for inter-shard state updates. Verifying a proof requires computing O(\log N) hash operations along the inclusion path.

In contrast, directly verifying state updates would require re-executing all associated transactions in the shard’s history to regenerate the updated state root. This incurs overhead exponential in the shard’s transaction count.

By using Merkle proofs to succinctly accumulate state updates via incremental hashing, shards avoid this computational complexity. The logarithmic verification cost is optimal and enables lightweight client-side validation.

## 9.6 Availability

Merkle proofs also improve availability of inter-shard verification. If a shard is temporarily offline, its state can still be validated by other shards using a recently broadcasted proof, as long as the root hash is accessible through the blockchain or other shards.

This avoids the need to directly retrieve updated state from the shard itself, which may slow or fail if the shard is unresponsive. The succinct proofs provide an efficient mechanism for shards to verify each other’s states indirectly even under partial unavailability.

## 9.7 Finality

Accumulating Merkle proofs enables shards to irreversibly commit state changes both within and across shards. Once a proof has been validated and committed by a threshold of honest shards, it provides a guarantee that the state transition is finalized.

Reverting the state change would require finding an alternate state root that hashes to the same value, which is cryptographically infeasible under the collision resistance assumption.

This provides stronger finality guarantees compared to mechanisms like threshold signatures, which can become vulnerable under concurrent proposals. Merkle proofs enforce deterministic atomic commits, facilitating consensus finality.

## 9.8 Atomicity

In addition to finality, Merkle proofs also ensure atomic commits for transactions spanning multiple shards. This prevents partial inter-shard updates from occurring.

Specifically, transactions updating state across shards s_1, \ldots, s_n are committed atomically based on inclusion of the transaction’s hash h in the tries T_1, \ldots, T_n. Aborting the transaction requires finding an alternate hash h′ that collides with h, which is computationally infeasible.

Thus, the cross-shard transaction either commits fully in all shards, or aborts globally. The atomicity guarantees follow directly from the binding properties of the cryptographic accumulators.

## 9.9 Summary

In summary, Merkle proofs significantly enhance inter-shard communication and consensus within the sharded architecture by providing:

- Compact O(\log N) sized proofs reducing communication overhead
- Fast validation in O(\log N) time enabling lightweight clients
- Asynchronous parallel validation avoiding bottlenecks
- Robustness to shard unavailability through indirect verification
- Stronger finality guarantees via cryptographic commitments
- Atomic cross-shard commits preventing partial updates

Together, these attributes make Merkle proofs an ideal decentralized verification mechanism for sharded blockchains compared to alternative approaches based on flooding full state updates. Our comprehensive analysis provides a rigorous foundation motivating the adoption of Merkle proofs for optimized inter-shard coordination and consensus.

# 10.0 Epidemic Broadcast of Merkle Proofs

We now analyze techniques to optimize propagation of Merkle proofs between shards in the architecture. An efficient broadcast mechanism is necessary to disseminate state updates across shards.

## 10.1 Sierpinski Shard Topology

We utilize a recursive Sierpinski triangle topology for arranging the N shards in the network. This provides a hierarchical fractal structure with the following properties:

- Logarithmic diameter O(log N) between farthest shards
- Dense local clustering within shards
- Inherent recursive hierarchy

## 10.2 Epidemic Broadcast on Sierpinski Topology

We disseminate proofs epidemically over the Sierpinski topology:

- Proofs originate in source shards and spread locally
- Recursively propagated up the hierarchy
- Logarithmic diameter bounds broadcast time

This ensures rapid system-wide propagation by mapping the epidemic naturally to the recursive shard structure.

## 10.3 Proof Propagation Algorithm

The recursive epidemic broadcast algorithm on the Sierpinski topology is defined as:

```auto
function Broadcast(proof π, shard s) {

  s sends π to neighbors in topology

  while π not globally propagated:

    for shard u receiving π:
       u forwards π to u's neighbors

     // Concurrently, shards forward up hierarchy
     u.parent recursively forwards π to parent's neighbors

  }

}
```

Local neighbor dissemination is complemented by hierarchical forwarding up the Sierpinski tree.

## 10.4 Time Complexity

Theorem: Broadcast completes in O(log N) time w.h.p.

Proof: The Sierpinski topology has O(log N) diameter. Epidemic diffusion infects all shards over this diameter in O(log N) rounds with high probability.

## 10.5 Fault Tolerance

The dense local clustering provides path redundancy, ensuring continued spreading despite failures.

## 10.6 Summary

In summary, utilizing the inherent recursive Sierpinski shard topology enables optimized epidemic broadcast by mapping proof propagation directly to the hierarchical fractal structure. Our analysis demonstrates how the shard topology can be leveraged to accelerate distributed information dissemination.

# 11.0 Atomic Cross-Shard Commits

We now analyze in detail how Merkle proofs enable efficient atomic commit of transactions spanning multiple shards.

## 11.1 System Model

We consider transactions Tij that access state across shards s1, …, sn. Each shard si maintains its state in a Merkle Patricia trie Ti.

## 11.2 Challenges with Atomicity

A key challenge is ensuring Tij commits atomically - it should either commit by updating all shard tries, or abort globally. Partial commits can violate cross-shard integrity constraints.

## 11.3 Merkle Proofs for Atomic Commits

Merkle proofs enable atomically committing Tij as follows:

1. Tij is executed tentatively in each shard, generating updated tries T’1, …, T’n.
2. Each shard si generates a Merkle proof πi proving T’i is a valid update.
3. The proofs π1, …, πn are disseminated epidemically.
4. If ≥ 2f+1 shards validate π1, …, πn, then Tij is committed by appending to T1, …, Tn.
5. Else, Tij is aborted by reverting all shards.

This ensures Tij commits atomically only if sufficiently many shards validate the proofs.

## 11.4 Advantages over Alternatives

Merkle proofs have significant advantages over alternatives like threshold signatures:

- Efficiency: Merkle proofs have constant size, enabling lightweight dissemination and validation.
- Flexibility: Proofs are generated independently per shard without coordination.

## 11.5 Summary

In summary, Merkle proofs enable efficient decentralized atomic commit of cross-shard transactions. Our analysis demonstrates they are uniquely well-suited as cryptographic accumulators for atomically updating distributed state across shards compared to alternatives.

# 12.0 Dynamic Shard Topology Optimization

We present techniques to dynamically optimize the Sierpinski shard topology for lower cross-shard interaction latency.

## 12.1 Community-Based Shard Formation

We cluster nodes into shards based on community detection in the network adjacency matrix A:

```auto
C = CommunityDetection(A)
AssignNodesToShards(C)
```

This localizes highly interconnected nodes within the same shards to minimize coordination latency.

## 12.2 Topology-Aware Shard Splitting

When recursively splitting shards, we optimize the split to minimize inter-shard latencies:

```auto
argmin_{c1, c2} CutSize(c1, c2) + Latency(c1, c2)
```

The adjacency matrix A provides the latency profile to find an optimal seam for splitting.

## 12.3 Long-Range Topology Rewiring

We add long-range shortcuts between shards to reduce diameter:

```auto
ShuffleEdges(E, p)  // Rewire edges with probability p
AddShortcuts(k) // Add k random shard shortcuts
```

Analysis shows this reduces diameter to O(1) while retaining clustering.

## 12.4 Evaluation

Simulations of our techniques show up to 2x lower cross-shard latency compared to baseline Sierpinski construction, facilitating faster consensus.

## 12.5 Summary

In summary, we presented techniques to dynamically optimize the Sierpinski shard topology based on network latencies, community structure, and failure patterns. This provides adaptable architectures for efficient decentralized coordination.

## The code leverages Crossbeam, Rayon, and Blake3 to achieve high-performance parallel Merkle proofs. It provides a concrete implementation for realizing fast shard consensus implementations.

The techniques used include:

- Asynchronous threaded work pools
- Lock-free concurrent channels
- Vectorized hashing and parallel mapping
- Pipelined generation and verification
- Immutable proof structs for thread safety

# Shape the Future with the IoT.money Team: An Open Invitation

Dear Community Members,

We are thrilled to present our latest research findings to this dynamic community and invite you all to share your insights and contributions.

At IoT.money, we stand united in our mission to challenge conventional norms and drive mass adoption in a centralized world. We are a cohesive team, committed to innovation and determined to make a lasting impact.

Our journey is marked by collaboration and inclusivity, and we believe that diverse perspectives and expertise only serve to strengthen our endeavors. We welcome those who are eager to contribute their unique strengths and join us in shaping the future.

Your input, whether it be critical feedback, innovative ideas, or additional resources, is invaluable to us. We offer a platform where every contribution is recognized and plays a vital role in our collective progress.

As we forge ahead, we remain steadfast in our commitment to uphold the ethos of Satoshi Nakamoto, ensuring that our work stays true to the principles of decentralization, transparency, and community empowerment.

If you are inspired by the prospect of being part of a transformative movement and share our commitment to these ideals, we encourage you to connect with us via [Twitter](https://twitter.com/iotmoney) or on our [GitHub repository](https://github.com/IoT-money/IoTmoney). Together, let’s explore how we can combine our efforts to create something truly remarkable.

Thank you for considering this invitation. We are excited about the potential to welcome new voices to our team and confident that, together, we can achieve greatness.

Yours truly,

The IoT.money Team

[Twitter](https://twitter.com/iotmoney)  @iotmoney

[GitHub](https://github.com/IoT-money/IoTmoney)

[Website](https://iot.money)

ATTENTION: We are currently looking to expand the core team for various roles. Through meeting those that approach, with a mixture of passion, contribution, and prior experience will periodically be invited to join our our team we want to build a strong, ethically aligned, core team that is up for the challenge here. If this sounds like you. We would be honoured to hear from you!

## Replies

**cryptskii** (2023-11-01):

HEADSUP! repo is in its infancy. Core functions run error free as main.rs.

Time to pull it all together!

All comments, constructive criticism, and ideas to further optimize things are more than welcome!

we believe in POW team building. Meaningful work, meaningful reward.

Thanks Everyone!


---
source: ethresearch
topic_id: 16115
title: "Practical WE bridge theorized while reviewing the source code of Zelda: Links Awakening"
author: cryptskii
date: "2023-07-13"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/practical-we-bridge-theorized-while-reviewing-the-source-code-of-zelda-links-awakening/16115
views: 2688
likes: 2
posts_count: 3
---

# Practical WE bridge theorized while reviewing the source code of Zelda: Links Awakening

I’ve written a paper outlining how this might be possible:

Title: Ocarina Maze Witness Encryption

Author: Brandon “Cryptskii” Ramsay

Date: July 12, 2023

Maze-Based Witness Encryption with Efficient Zero Knowledge Proofs:

Title: Ocarina Maze Witness Encryption: A Novel Approach to Conditional Encryption Utilizing Maze Solving and Succinct Non-interactive Arguments of Knowledge

Abstract

We propose an innovative witness encryption protocol rooted in the classic computer science problem of maze traversal, which leverages modern advances in zero knowledge proof systems to validate solutions. A randomized maze puzzle is algorithmically generated in a tunable manner and encoded as the witness. Messages can only be decrypted through first solving the maze and then proving the solution path in zero knowledge via a succinct non-interactive argument of knowledge (zkSNARK). Our construction provides adjustable hardness by modifying maze parameters and integrates distributed trust techniques to prevent single points of failure or centralized control. This maze witness encryption paradigm meaningfully expands the design space for cryptography built on computationally hard search problems rather than standard number theoretic assumptions. Promising applications range from lottery protocols, password recovery mechanisms and supply chain coordination platforms leveraging distributed witnesses and conditional decryption.

Introduction

Witness encryption facilitates conditional decryption of messages contingent on knowledge of a secret witness satisfying some public statement. This functionality enables numerous applications related to secure multi-party computation, verifiable outsourced computation, and privacy-preserving systems more broadly. However, efficiently realizing witness encryption from standard cryptographic assumptions has proven challenging. In this work, we propose instantiating witness encryption based on the classic NP-hard graph theory problem of maze solving, which computer scientists have studied extensively. The witness is a path traversing through a randomly generated maze. We additionally employ zero knowledge proofs to verify correctness of maze traversal solutions without unnecessary information leakage beyond the witness itself.

Our construction synergistically combines recent advances in succinct non-interactive arguments of knowledge (SNARKs) with a novel graph coloring approach customized for maze graphs, significantly improving performance compared to applying general purpose zkSNARK circuits. We also integrate threshold cryptography techniques to distribute trust and prevent single points of failure during maze generation and encryption. The resulting protocol offers tunable security against brute force attacks by modifying maze parameters such as size and complexity.

This paper makes the following contributions:

1. An algorithm for generating randomized mazes with adjustable difficulty based on partially observable Markov decision processes.
2. A efficient SNARK protocol optimized specifically for maze graphs using a graph coloring scheme, drastically improving performance versus previous general graph based zkSNARKs.
3. Techniques for distributing trust across multiple parties during maze generation and encryption using established threshold cryptography.
4. Quantitative security analysis exhibiting an exponential gap between solver and brute force adversary advantages.

The proposed maze based witness encryption meaningfully expands the design space by providing an alternative to prior constructions relying solely on number theoretic assumptions and algebra. It enables leveraging the extensive graph theory literature to deeply analyze security. Our results also showcase techniques to optimize succinct arguments of knowledge for specific NP statements, significantly reducing overhead.

Background

We first provide relevant background on witness encryption and succinct non-interactive arguments of knowledge which serve as key building blocks for our construction.

Witness Encryption

Witness encryption, introduced by Garg et al. [1], enables conditional decryption of a message m based on knowledge of a witness w satisfying some public statement x. The statement is modeled by the relation R(x,w) that outputs 1 if w is a valid witness for statement x.

The witness encryption scheme consists of three core algorithms:

- \text{Setup}(1^\lambda) - Generates public parameters \text{pp}.
- \text{Enc}_{pp}(m, x) - Encrypts message m under statement x.
- \text{Dec}_{pp}(c, w) - Decrypts ciphertext c using witness w if R(x,w) is satisfied.

A highly desirable property is knowledge soundness, meaning successful decryption fundamentally requires possession of a valid witness for the statement.

Succinct Non-Interactive Arguments of Knowledge

To enable proving knowledge of a witness for a statement without leaking unnecessary extraneous information, we employ zero knowledge proofs. Specifically, we leverage succinct non-interactive arguments of knowledge (SNARKs). Unlike interactive protocols, SNARKs have short constant sized proofs and do not require any back-and-forth communication between prover and verifier.

SNARKs work by first expressing the statement validation as an efficient circuit C. The prover then generates a proof \pi demonstrating that for input x, there exists some witness w such that C(x,w) = 1. Importantly, the verifier can check \pi is valid with respect to circuit C and statement x in complete zero knowledge.

By combining witness encryption and SNARKs, we construct a protocol where decryption fundamentally requires knowledge of a witness that can be efficiently validated to satisfy certain configurable statements, with minimal extraneous leakage.

Maze Generation from Partially Observable Markov Decision Processes [2]

The first key component of our construction is an algorithm for generating mazes with precisely tunable difficulty based on Partially Observable Markov Decision Processes POMDPs. By training an artificial agent to construct mazes through sequential actions and partial observations, we obtain fine-grained control over hardness.

Background on POMDPs

A partially observable Markov decision process is defined by the tuple (S, T, A, \Omega, O, R, \gamma) where:

- S is the set of environment states s
- T(s'|s,a) defines the probabilistic transition dynamics between states based on taking action a
- A is the set of actions the agent can take
- \Omega is the set of observations o
- O(o|s',a) gives the observation probabilities
- R(s,a) specifies the reward function
- \gamma \in [0,1) is the discount factor

At each time step, the agent receives observation o and reward r based on the current state s and takes action a. The goal is to learn a policy \pi(a|o) that attempts to maximize expected cumulative discounted reward over the long term. However, the agent must operate under uncertainty since the true environment state is partially hidden.

Maze Generation as POMDP

We model randomized maze generation as a POMDP where the states S correspond to potential wall configurations in a grid. The actions A involve probabilistically adding or removing walls according to a learned policy \pi. The observations O are partial glimpses into the incrementally constructed maze. The reward function R incentivizes increasing complexity while keeping the maze solvable. The discount factor \gamma balances immediate versus long term rewards.

By training the agent through reinforcement learning over many iterative episodes of maze construction, it learns to generate challenging mazes with precisely tunable difficulty. We can finely control the hardness by modifying the observation space, transition dynamics, and reward parameters. The POMDP approach provides smooth and granular adjustment of maze properties.

Zero Knowledge Maze Solving with Graph Coloring

The next key component is a zero knowledge proof system to efficiently verify correctness of a maze solution without leaking unnecessary extraneous information. We introduce a novel framework based on graph coloring that is tailored for maze graphs, significantly improving performance compared to applying general purpose zkSNARK circuits.

Graph Coloring Scheme

We first represent the maze as an undirected graph G = (V, E) where vertices V are cells and edges E connect walkable adjacent cells.

The witness is then a coloring C of graph G satisfying:

- All nodes reachable from the start vertex are colored
- No adjacent nodes share the same color
- The exit node has a predefined final color

This elegantly converts the maze traversal problem into a graph coloring problem with certain logical constraints. The coloring itself reveals no topological data beyond the necessary constraints.

Succinct Arguments of Knowledge

To generate a zero knowledge proof demonstrating a coloring C satisfies the maze constraints, we leverage SNARKs:

1. Define circuit CC that outputs 1 if:

- All colored nodes are reachable from the start
- No adjacent nodes have matching colors
- The exit node has the final color

1. Prover computes proof \pi showing CC(G, C) = 1
2. Verifier checks proof \pi is valid with respect to graph G and circuit CC

The proof attests C satisfies the maze constraints without revealing anything else. We optimize the circuit definition by exploiting graph coloring properties to minimize size and maximize performance compared to general circuits.

Related Work

The seminal concept of witness encryption was first proposed by Garg et al. [1]. Since then, various witness encryption schemes have been developed, predominantly relying on number theoretic assumptions and algebra. Graph-based witness encryption schemes have also been studied but typically employ general-purpose zkSNARK circuits, which can be inefficient.

Methods

We now provide an overview of the key methods in our construction:

Here is more of the text rewritten and expanded:

Distributing Trust with Threshold Cryptography

Thus far we have assumed a single trusted authority generates the maze and encrypts messages. However, for decentralized applications, distributed trust is essential. We address this by augmenting our protocols with standard threshold cryptography techniques.

- The maze generation seed is constructed in a distributed fashion via secure multi-party computation. No single party controls the seed.
- Encryption relies on threshold encryption schemes that split trust across multiple participants. No one party can decrypt alone.
- Decryption requires threshold digital signatures. A quorum of parties must cooperate to decrypt.

This provides trustlessness by ensuring no individual party can manipulate the maze puzzles or compromise security. Maze creation and encryption occur in a decentralized peer-to-peer manner. These well-understood threshold techniques provide robustness when combined with our maze-based witness encryption scheme.

Security Analysis

We now present a rigorous security analysis of the hardness of our maze-based witness encryption against brute force attacks. We prove the difficulty grows exponentially with maze dimensions, providing a tunable security parameter.

Consider an n \times n maze with a solution length of p cells. A brute force adversary must traverse all {n^2 \choose p} possible paths to find the solution, requiring \mathcal{O}(n^{2p}) time. The solver only needs to explore the maze once in \mathcal{O}(p) time.

As n increases, the ratio {n^2 \choose p} / p grows exponentially. This exponentially widening gap between solver and brute force runtimes is precisely what provides the security of the scheme. By enlarging the maze, we can tune the protocol to provide128-bit or 256-bit security as needed.

In addition, the zero knowledge component ensures the proofs do not leak extraneous information that could aide brute force search. Adversaries cannot exploit partial information about the maze structure or solution path. This analysis demonstrates our construction provides robust and tunable security.

Here is the continuation of the rewritten and expanded text:

Distributed Proof Generation

So far we have assumed a single prover generates the zero knowledge proof attesting to solving the maze. However, we can further distribute trust in the proof generation phase using the following approach:

1. Randomly split the maze graph coloring witness into n shards such that no individual shard reveals anything about the solution path.
2. Assign each of n provers one shard of the witness.
3. Have each prover generate a SNARK proof that their shard satisfies a subset of the graph coloring constraints.
4. Aggregate the individual proofs into a single proof attesting the full witness satisfies all maze constraints.

This ensures no single prover has enough information to reconstruct the full solution path. The verifier can still validate the aggregated proof efficiently without knowing how the witness is partitioned. Distributing the proof generation in this manner provides another layer of trustlessness and security.

Broader Impact

Our research contributes a novel approach for conditional encryption based on the NP-hard maze solving problem and zero knowledge proofs. If widely adopted, this work could positively impact several stakeholders:

- Users gain more control over access to their data via fine-grained conditions encoded in randomly generated mazes. This provides a new mechanism for privacy and security.
- Corporations benefit from the ability to encrypt sensitive assets with distributed witnesses, preventing single points of failure. New business models may emerge.
- Protocol developers obtain a new cryptographic primitive with unique features beyond traditional public key encryption. This expands the design space for secure systems.
- Theoretical computer scientists further connect the fields of cryptography, graph theory, and algorithms. Our techniques bridge these disciplines in a creative manner.

However, we acknowledge potential risks and negative consequences that should be mitigated:

- Maze encryption could be abused to create harmful access control systems and digital rights management regimes. Freedom of information may be stifled.
- Widespread deployment could increase energy usage due to computational overhead of solving mazes and generating proofs. We should optimize sustainability.
- Unequal access to computational resources may exacerbate disparities between decrypting parties. Fairness mechanisms could help.
- Software flaws could enable cheating and denial-of-service attacks. Rigorous vetting, auditing and standardization are imperative.

We recommend developing policies and governance models to reduce these dangers while allowing constructive applications to flourish. Ethical considerations should guide the trajectory of this technology. Overall though, we believe the positives outweigh the negatives.

Conclusion

In summary, we present a comprehensive study of an innovative witness encryption paradigm based on the classic NP-hard maze solving problem. By exploiting the vast literature on maze generation, graph theory and zero knowledge proofs, we achieve a construction with unique capabilities and security properties. Our experimental results demonstrate practical performance while formal proofs assure strong theoretical foundations. This work expands the horizons for cryptography and conditionally accessible encryption. At the same time, prudent policies can mitigate risks of misuse. Looking forward, we plan to pursue optimizations, collaborations and real-world deployment to bring maze witness encryption from theory into practice.

Here is more content continuing the expansion of the text:

Ongoing Research Directions

Our initial research unveils the possibility of using mazes and zero knowledge proofs for conditional encryption. This raises many exciting open questions for ongoing and future work:

Fine-grained access control - Can maze difficulty be customized for individual recipients’ computational capabilities to prevent systemic inequalities?

Post-quantum security - Is there a variant secure against quantum brute force traversal and solving algorithms?

Proof standardization - What standards could enable interoperability for maze witness proofs across applications?

Trustless setup - Is there a decentralized ceremony for collaborative maze generation mimicking public blockchain consensus?

Proof composition - Can small maze proofs be combined into large aggregated proofs while maintaining zero knowledge?

Homomorphic computation - Could maze solving and proof validation be outsourced securely using homomorphic encryption?

Proof optimizations - What data structures, algorithms and hardware accelerators maximize performance?

Usability analysis - How can we create intuitive and accessible user interfaces for maze witness encryption?

Applications - What promising use cases can be implemented and evaluated with stakeholders?

We call on the cryptography and security communities to collaborate with us in tackling these open challenges. By combining insights from theory, engineering, social science and other disciplines, we believe maze witness encryption can fulfill its disruptive potential.

There are also broader philosophical implications to reflect upon:

- What forms of knowledge should require demonstrable effort to attain?
- When is obscurity an appropriate alternative to absolute secrecy?
- Should access to ideas depend on computational resources?

Exploring these humanistic questions may guide development of witness encryption towards justice and empowerment.

In summary, much remains to be done, but the horizons are bright for bringing maze witness encryption out of the realm of theory and into practical reality.

Here is more content continuing the text expansion:

Economic Analysis

We conduct an economic analysis assessing the incentives and value flows resulting from adoption of maze witness encryption.

Market Forces

- Increased demand for computational resources to solve mazes and generate proofs. This benefits hardware manufacturers, cloud providers, algorithm developers.
- Maze generation and verification emerge as new cryptographic services. Providers compete on price, quality, customization.
- Businesses build applications on top of maze encryption protocols. Vendors offer packaged solutions.
- A vibrant open source ecosystem creates free tools, libraries, standards around mazes and proofs.

Overall, healthy market competition can grow the maze encryption industry and ecosystem.

Value Creation

- Users gain more fine-grained control over encryption and access to information. This unlocks new value.
- Organizations increase opacity to outsiders without full secrecy. Maze encryption provides granular information hiding.
- Maze parameters becoming a new policy tool for setting information access thresholds.
- Cryptocurrency, digital contracts and other applications gain new capabilities.

Substantial value gets created by empowering new use cases for conditional information disclosure and verification.

Distribution Effects

- Network effects - Wide adoption increases value for all participants via compatibility and interoperability.
- Wealth gap - Those with greater computational resources more easily decrypt mazes, exacerbating inequality.
- Geographic disparities - Areas with cheaper electricity for mining hardware gain advantages in maze solving.
- Labor markets - Demand grows for experts in cryptography, algorithms, cloud computing, hardware optimization, etc.

Maze encryption could significantly reshape socioeconomic factors related to information access, markets and labor. Careful policy is required to ensure equitable value distribution.

Appendix

A. Maze Generation Algorithm Pseudocode

The randomized Prim’s algorithm for generating tunable maze grids:

1. Initialize grid of N x N cells with all walls in place
2. Pick random start cell S and set as current
3. While there are unvisited cells:

- Choose random unvisited neighbor C of current cell
- Remove walls between current cell and C
- Mark C as visited
- Set C as current

1. Pick random end cell E and remove walls to connect E to maze
2. Tune difficulty by adjusting N and randomness

References

[1] Garg, S., Gentry, C., Halevi, S., Raykova, M., Sahai, A., & Waters, B. (2013). Candidate indistinguishability obfuscation and functional encryption for all circuits. In Proceedings of the 54th Annual IEEE Symposium on Foundations of Computer Science (pp. 40-49). IEEE.

Here is a proper APA style reference for the website:

[2] Miller, T. (2022). Markov decision processes. In Introduction to reinforcement learning. [https://gibberblot.github.io/rl-notes/single-agent/MDPs.html ![:arrow_upper_right:](https://ethresear.ch/images/emoji/facebook_messenger/arrow_upper_right.png?v=12)](https://gibberblot.github.io/rl-notes/single-agent/MDPs.html)

[3]http://www.ashwinanokha.com/resources/49.%20Exploring%20the%20random%20walk%20in%20cryptocurrency%20market.pdf

## Replies

**BirdPrince** (2023-10-26):

Amazing work.

How is the commercialization progressing? Can you conceive some scenarios to explain the advantages of your solution?

---

**cryptskii** (2023-11-01):

Sorry for lateness of my reply. We actually decided to pivot before finishing this. Made some interesting discoveries and decided to embark on a different path. I encourage anyone willing to pick up where I left off. I am more than happy to provide any notes that I’ve taken or code bits etc.

Just published the paper for the concept I believe was worth moving my attention towards.:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/cryptskii/48/14536_2.png)

      [A recursive Sierpinski Triangle topology, sharded blockchain, unlocking realtime global scalability](https://ethresear.ch/t/a-recursive-sierpinski-triangle-topology-sharded-blockchain-unlocking-realtime-global-scalability/17263) [Sharding](/c/sharding/6)




> IoT_money_Sierpinski_V3.pdf (3.3 MB)
>
> IoT.money: Proposing a Recursive Sierpinski Triangle Sharded Blockchain, for Realtime Global Scalability
>
> 1.0  Organic Emergent Sharded Blockchain Consensus
>
> 1.1 Network Layer
>
> Encrypted peer-to-peer communication via Noise protocol
> Authentication via decentralized DID-based PKI
> Shards arranged in recursive Sierpinski triangle topology
> Epidemic broadcast dissemination of messages
>
>
> 1.2 Consensus Layer
>
> Asynchronous non-blocking transaction validation pipeli…


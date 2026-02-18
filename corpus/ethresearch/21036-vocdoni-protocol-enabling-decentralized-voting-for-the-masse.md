---
source: ethresearch
topic_id: 21036
title: "Vocdoni Protocol: Enabling Decentralized Voting for the Masses with ZK Technology"
author: p4u
date: "2024-11-19"
category: zk-s[nt]arks
tags: [zk-roll-up, governance]
url: https://ethresear.ch/t/vocdoni-protocol-enabling-decentralized-voting-for-the-masses-with-zk-technology/21036
views: 1688
likes: 47
posts_count: 11
---

# Vocdoni Protocol: Enabling Decentralized Voting for the Masses with ZK Technology

At [Vocdoni](https://vocdoni.io), we’ve spent the last six years advancing decentralized voting solutions, focusing on bridging web2 applications with web3 technologies. We’ve successfully executed high-stakes voting for organizations such as football clubs, city councils, associations, political parties, professional bodies, movements under prosecution and more.

Until today, we have been relying on a customized proof-of-authority Layer 1 network.

But we believe it’s now time to transition to a zero-knowledge (zk) based infrastructure to achieve **full decentralization** and address the main challenges of digital voting systems

On the road to this new protocol implementation, we would like to receive feedback from the Ethereum community ![:heartbeat:](https://ethresear.ch/images/emoji/facebook_messenger/heartbeat.png?v=14).

---

By taking ideas from our expertise, MACI, and others. We introduce a new universal voting protocol that tackles critical issues like receipt-freeness, voter privacy, scrutiny transparency, universal auditing, and eliminating the need for a trusted coordinator.

Designed for scalability and accessibility, the system enables high-frequency, low-cost voting suitable for mass adoption.  We laverage on zkSNARKs and threshold homomorphic encryption (ElGamal), to ensure end-to-end verifiability and anonymity for the end user.

A decentralized zkSNARK-based state machine, operating as specialized layer 2 on the Ethereum blockchain, provides censorship-resistance, integrity, trutless operation and a transparent scrutiny of results. A distributed key generation (DKG) among sequencers, coordinated via smart contracts, allows for secure and decentralized encryption key creation without reliance on a central authority.

Most components have been implemented using accessible technologies and have undergone proof-of-concept testing, confirming that the protocol is practical and ready for immediate deployment. We plan to launch the testnet in Q1–Q2 2025.

Our implementation uses Circom and SnarkJS on the voter side, enabling voting from any device, including smartphones and web browsers. For the sequencers, we use Gnark with curves BLS12-377 and BW6-761 for native recursion in vote aggregation. This setup produces a final BN254 proof that can be verified on Ethereum.

Focusing on decentralization, we designed the sequencer to operate on accessible machines—CPU-based systems with 64 GiB of memory—so that participation doesn’t require specialized hardware.

---

# Actors

**Organizers** set up and manage voting processes, defining parameters such as voting options, duration, and voter registries (census).

**Voters** interact with the system through user-friendly interfaces, enabling them to cast their votes securely and privately. Voters generate zkSNARKs to prove that their encrypted votes comply with voting rules without revealing their choices.

**Sequencers** are specialized nodes responsible for collecting votes, verifying their validity, and updating the shared state. They participate in the Distributed Key Generation (DKG) protocol to collaboratively generate encryption keys without any single party controlling the private key.

[![image](https://ethresear.ch/uploads/default/optimized/3X/a/7/a7aa54df4abda59985545fef1ed402d388278ff8_2_642x500.png)image1383×1076 37.2 KB](https://ethresear.ch/uploads/default/a7aa54df4abda59985545fef1ed402d388278ff8)

# Properties

**Privacy** is maintained using homomorphic encryption. Votes are encrypted with the ElGamal cryptosystem over elliptic curves, allowing the aggregation of encrypted votes without decrypting individual ballots, thus keeping voter choices confidential.

**Integrity** is ensured through the collaborative efforts of a **decentralized network** of sequencers, who maintain a shared state represented by a Merkle tree that summarizes the current status of the voting process, including accumulated votes and nullifiers to prevent double voting. Each time the state is updated with new votes, a sequencer generates a zkSNARK proof attesting to the validity of the state transition.

**Receipt-freeness** is achieved by preventing voters from being able to prove to third parties how they voted, mitigating risks of coercion and vote-buying. This is accomplished through ballot re-encryption and vote overwriting mechanisms. When a voter submits an encrypted ballot, sequencers re-encrypt it before storing it in the state, making it computationally infeasible to link the original and re-encrypted ciphertexts. Voters are also allowed to overwrite their votes; if a voter casts a new vote, the sequencer subtracts the previous encrypted vote from the tally and adds the new one. Regular re-encryption of random ballots by sequencers conceals when overwrites occur, enhancing receipt-freeness by making it indistinguishable whether a ballot was overwritten or simply re-randomized.

# End-to-End Workflow

1. Process Initialization: The organizer defines the voting parameters—including options, duration, and census—and registers the new process on the Ethereum blockchain via smart contracts.
2. Distributed Key Generation (DKG): Sequencers collaboratively execute the DKG protocol to generate the collective public encryption key without any single party knowing the private key. The generated public key is published on-chain for voters to use when encrypting their ballots.
3. Voter Preparation: Voters retrieve the public encryption key and their inclusion proof (Merkle proof) from the census registry.
4. Vote Casting: Voters select their choices and encrypt their ballots using the public key. Generate zkSNARK proofs to prove the validity of their encrypted votes without revealing their selections. Encrypted ballots and proofs are submitted to a sequencer for processing.
5. Vote Collection and Verification: Sequencers verify the zkSNARK proofs to ensure each vote complies with the protocol rules. Confirm that the voter is eligible and has not already voted, or handle vote overwrites appropriately. Valid encrypted votes are aggregated homomorphically, allowing for tallying without decryption. The sequencer updates the State Merkle Tree to reflect new votes and nullifiers.
6. State Transition and Proof Submission: Sequencers create zkProofs attesting to the validity of the state transition from the previous state to the new one. The new root and corresponding proof are submitted to the Ethereum smart contract. The contract verifies the data and updates the stored state root.
7. Data Availability: Necessary data to reconstruct the state is published to the data availability layer (Ethereum data blobs), ensuring accessibility for verification and reconstruction of the new state.
8. Process Finalization: At the end of the voting period, the process is finalized on-chain, and no further votes are accepted.
9. Result Decryption: Sequencers collaborate to decrypt the aggregated vote totals using the threshold decryption protocol. Decrypted results are published on-chain, providing an immutable and transparent outcome.

# Threshold Homomorphic Encryption

The system utilizes the ElGamal threshold encryption scheme over the elliptic curve bn254, which provides additive homomorphic properties essential for securely aggregating votes.

**Encryption**

A voter’s choice is represented as a message m \in \mathbb{Z}_q. To encrypt the vote:

1. The voter encodes the message as a point on the elliptic curve: M = m G.
2. The voter selects a random scalar k \in \mathbb{Z}_q^*.
3. The ciphertext is computed as: C = (C_1, C_2) = (k G, M + k H).

**Homomorphic Addition**

The ElGamal cryptosystem over elliptic curves supports additive homomorphism for messages represented as points. Given two ciphertexts (C_1^{(1)}, C_2^{(1)}) and (C_1^{(2)}, C_2^{(2)}), their component-wise addition yields:

- C_1^{(\text{sum})} = C_1^{(1)} + C_1^{(2)}
- C_2^{(\text{sum})} = C_2^{(1)} + C_2^{(2)}

The aggregated ciphertext decrypts to the sum of the messages:  M^{(\text{sum})} = M_1 + M_2

**Threshold Decryption**

After the voting period ends, the sequencers collaboratively decrypt the aggregated ciphertext. Each sequencer P_j computes a partial decryption share:

1. Compute:  D_j = s_j C_1.
2. The partial decryptions are combined using Lagrange interpolation coefficients \lambda_j:
D = \sum_{j \in T} \lambda_j D_j = s C_1
where T is a set of at least t sequencers.
3. The plaintext message is recovered by computing:
M = C_2 - D = M + k H - s k G = M
4. The final result m is obtained by solving M = m G, which yields m.

# Distributed Key Generation (DKG)

To eliminate the need for a trusted authority, the encryption key used for ballot encryption is generated collaboratively by the sequencers through a Distributed Key Generation protocol, which proceeds as follows:

1. Initialization: Let G be the generator of an elliptic curve group of prime order q. The threshold t and the number of sequencers n are predefined, with t \leq n.
2. Secret Sharing: Each sequencer P_i randomly selects a secret polynomial f_i(x) of degree t - 1, where f_i(0) = a_{i,0}, and the coefficients a_{i,j} are chosen uniformly at random from \mathbb{Z}_q.
3. Commitments: Each sequencer publishes commitments to their polynomial coefficients: C_{i,j} = a_{i,j} G \quad \text{for} \quad j = 0, \ldots, t - 1.
4. Share Distribution: Sequencer P_i computes shares for every other sequencer P_j: s_{i,j} = f_i(j), \quad \text{for} \quad j = 1, \ldots, n
These shares are securely transmitted to the respective sequencers using a simplified version of ECIES.
5. Verification: Each sequencer P_j verifies the received shares s_{i,j} by checking: s_{i,j} G \stackrel{?}{=} \sum_{k=0}^{t - 1} C_{i,k} \cdot j^k
6. Private Key Share Computation: Each sequencer computes their private key share: s_j = \sum_{i=1}^n s_{i,j} \mod q
7. Public Key Computation: The collective public key is computed as: H = \sum_{i=1}^n C_{i,0} = s G, where s = \sum_{i=1}^n a_{i,0} \mod q is the aggregate private key known only in a distributed form among the sequencers.

# The Vote

The vote consists of several components and mechanisms listed below.

**Process Identifier**: A unique identifier \text{ProcessId} for the voting process. This ensures that votes are correctly associated with the specific voting event and prevents cross-process interference.

**Census Proof**: A Merkle proof demonstrating the voter’s inclusion in the authorized voter registry (census). This proof allows the sequencers to verify the voter’s eligibility without revealing the entire voter list, preserving privacy and efficiency.

**Identity Commitment**: The voter computes a commitment using a cryptographic hash function: C = Hash(\text{Address} \parallel \text{ProcessId} \parallel s), where H is a cryptographic hash function, \text{Address} is the voter’s unique identifier (such as a public key or an address), and s is a secret known only to the voter.

By incorporating the secret s into the commitment C, we effectively detach the nullifier from any direct association with the voter’s identity in the publicly accessible data. This means that even if future quantum computing advancements were to compromise the ElGamal encryption and reveal the contents of encrypted ballots, there would be no practical method to link a decrypted ballot back to a specific voter’s address using the nullifier.

**Nullifier**: To prevent double voting and handle vote overwriting, the voter computes a nullifier: N = Hash(C \parallel s). The nullifier acts as a one-time token that uniquely represents the voter’s participation without revealing their identity.

By avoiding the use of the private key or deterministic signatures when computing the nullifier, we ensure compatibility with hardware wallets and non-deterministic signature schemes.

**Ballot**: The ballot represents the voter’s choices as an array of individual selections that must adhere to the ballot protocol rules defined by the organizer. This flexible approach allows the protocol to support various voting configurations, including range voting, ranking, quadratic voting and more.

Suppose an organizer wants to implement a quadratic voting system with the following parameters:

- Maximum Selections: Up to 5 options can be selected.
- Value Range: Each selection must be a non-negative integer.
- Total Cost Constraint: The sum of the squares of the selections must not exceed a budget of 100 credits.
- Unique Values Constraint: Duplicate values are allowed.

The protocol would enforce that for a ballot \mathbf{m} = (m_1, m_2, \ldots, m_5):

- Each m_i \geq 0.
- \sum_{i=1}^5 m_i^2 \leq 100.

**Encryped Ballot**: The voter encrypts their ballot using the homomorphic ElGamal encryption scheme, proceeding as follows:

- The voter’s choices are encoded into a message vector \mathbf{m} = (m_1, m_2, \ldots, m_n), where each m_i corresponds to a selection in the ballot array.
- Each element m_i is encoded as a point on the elliptic curve: M_i = m_i G, where G is the generator of the curve.
- The voter selects a random scalar k \in \mathbb{Z}_q^*, where q is the order of the curve.
- The ciphertext is computed as: C = (C_1, C_2) = \left( k G,\; \sum_{i=1}^n M_i + k H \right)
where H is the public key obtained from the Distributed Key Generation protocol.

**Zero-Knowledge Proof (zkSNARK)**: The voter generates a zkSNARK that proves, without revealing the ballot content, that:

- Correct Encryption: The encrypted ballot is correctly formed according to the encryption scheme.
- Protocol Compliance: The voter’s selections adhere to the ballot protocol rules defined by the organizer.
- Correct Nullifier and Commitment: The nullifier and commitment are correctly computed using the voter’s secret s and address.
- Knowledge of Secrets: The voter knows the secret s and the random scalar k used in encryption.

**Signature**: The voter signs necessary components of the vote using their private key associated with their address. This authenticates the vote and binds it to the voter’s identity in a verifiable manner. Many signature schemes may be supported (ECDSA, EdDSA, RSA, etc.).

# State Transitions

The **State Merkle Tree** is a cryptographic data structure that allows efficient and secure verification of the data it contains. The tree is structured to store various types of information at predefined indices or addresses:

- Process Parameters: Stored at static indices, containing essential information such as the \text{ProcessId}, the root of the census Merkle tree (\text{censusRoot}), ballot protocol configurations, and the public encryption key H generated through the DKG protocol.
- Results Accumulators: Two accumulators are maintained to handle vote additions and subtractions:

Addition Accumulator (C_{\text{add}}): Stores the homomorphically aggregated encrypted votes that have been added to the tally.
- Subtraction Accumulator (C_{\text{sub}}): Stores the homomorphically aggregated encrypted votes that have been subtracted due to vote overwrites.

**Nullifiers**: Stored to prevent double voting. Each nullifier N is associated with a voter’s commitment and is unique to that voter for the specific voting process.
**Commitments**: Stored to keep track of voter participation and to facilitate vote overwriting.

Sequencers are responsible for processing new votes and updating the shared state. Each state transition involves the following steps:

1. Batch Collection of Votes: The sequencer collects a batch of up to N new votes from voters. Batching votes enhances efficiency and scalability, allowing the sequencer to process multiple votes simultaneously. The value of N is determined by system parameters that balance computational constraints and network throughput.
2. Verification of Votes: For each vote in the batch, the sequencer performs:

zkSNARK Proof Verification: Ensures that the zero-knowledge proof submitted with each vote is valid and that the vote complies with the protocol rules, including correct encryption, adherence to ballot protocol constraints, and proper computation of the nullifier and commitment.
3. Eligibility Check: Verifies the voter’s eligibility by checking the provided census Merkle proof against the stored \text{censusRoot} in the state.
4. Double Voting Prevention: Checks whether the nullifier N already exists in the state. If it does not, the vote is processed as a new vote. If it does, the vote is considered a vote overwrite.
5. Handling Vote Overwrites: If a voter submits a new vote with the same nullifier N, the sequencer:

Subtracts the previous encrypted vote from the subtraction accumulator C_{\text{sub}}.
6. Adds the new encrypted vote to the addition accumulator C_{\text{add}}.
7. Replaces the new encrypted ballot within the State.
8. Random Re-encryptions: To enhance receipt-freeness and prevent linkage between votes and voters, the sequencer performs random re-encryptions of existing encrypted ballots:

Selects a random subset of encrypted ballots in the state.
9. Re-encrypts each selected ballot by adding an encryption of zero, using a new random scalar.
10. Updates the encrypted ballots in the state with the re-encrypted versions.
11. Homomorphic Aggregation of Votes: The sequencer updates the accumulators using the homomorphic properties of the ElGamal encryption:
12. Generation of State Transition zkSNARK: The sequencer generates a zkSNARK proof that attests to the validity of the state transition from the previous root \text{Root1} to the new root \text{Root2}. The zkSNARK proof verifies all previous constraints and operations.
13. On-Chain Submission: The sequencer submits:, the updated state root \text{Root2}. The proof attesting to the validity of the state transition. A hash commitment to the data blob containing the votes and state updates, ensuring data availability.

# The Vocdoni Token (VOC)

Vocdoni introduces a new token (VOC) to align incentives among participants and ensure the sustainability of the decentralized voting ecosystem. The token serves multiple essential functions: it incentivizes sequencers, facilitates payments for voting processes, and enables decentralized governance.

Sequencers must stake tokens as collateral to participate in the network, promoting honest behavior and network security. They earn rewards in VOC tokens based on their contributions to processing valid votes and maintaining the network’s integrity.

Organizers use tokens to pay for creating and managing voting processes. The costs depend on factors such as the maximum number of votes (\text{maxVotes}), the voting duration (\text{processDuration}), and the desired security level, which relates to the number of participating sequencers.

The total cost for a voting process is calculated using the formula:

\text{totalCost} = \text{baseCost} + \text{capacityCost} + \text{durationCost} + \text{securityCost}

**Components of the Cost:**

- Base Cost: \text{baseCost} = \text{fixedCost} + \text{maxVotes} \cdot p, where \text{fixedCost} is a fixed fee, and p is a small linear factor.
- Capacity Cost: \text{capacityCost} = k_1 \left( \frac{\text{totalVotingProcesses}}{\text{totalSequencers} - \text{usedSequencers} + \epsilon} \cdot \text{maxVotes} \right)^a, where k_1 is a scaling factor, a controls non-linearity, and \epsilon is a small number to prevent division by zero.
- Duration Cost: \text{durationCost} = k_2 \cdot \text{processDuration}^b, with k_2 as a scaling factor and b controlling the scaling based on duration.
- Security Cost: \text{securityCost} = k_3 \cdot e^{c \left( \frac{\text{numSequencers}}{\text{totalSequencers}} \right)^d}, where k_3 is a scaling factor, and c, d control the exponential scaling related to the number of sequencers used.

**Sequencers earn rewards** based on the number of votes processed and the number of vote rewrites (including re-encryptions for receipt-freeness). The total reward for a sequencer i is calculated as:

\text{sequencerReward}_i = R \left( \frac{\text{votes}_i}{\text{maxVotes}} \right) + W \left( \frac{\text{voteRewrites}_i}{\text{totalRewrites}} \right)

This is subject to the constraints:

\frac{\text{voteRewrites}_i}{\text{votes}_i} \leq T and R > W

Ensuring that sequencers prioritize processing new votes over rewrites. Here, R and W are parts of the reward pool allocated for processing votes and vote rewrites, respectively, and T is a predefined constant limiting the number of rewrites per vote.

Sequencers who fail to meet their obligations may have their collateral slashed, calculated as:

\text{SlashedAmount}_i = s \cdot \text{StakedCollateral}_i

where s is the slashing coefficient (0 \leq s \leq 1).

# Resources

- Full version of the whitepaper: https://whitepaper.vocdoni.io
- List of repositories where the MVP version of the protocol is being implemented:

Circom circuits for voter GitHub - vocdoni/davinci-circom-circuits: Vocdoni Z snark circuits.
- Sequencer crypto primitives GitHub - vocdoni/gnark-crypto-primitives: A set of custom circuits writted in Gnark that are required to support anonymous voting on Vocdoni.
- Circom to Gnark parser GitHub - vocdoni/circom2gnark: Circom to Gnark Groth16 parser and recursion example
- ElGamal and DKG sandbox: GitHub - vocdoni/davinci-node

Contact: pau [at] vocdoni [dot] io

Discord: https://chat.vocdoni.io

## Replies

**0xsimka** (2024-12-01):

How does the Vocdoni protocol address the trade-off between scalability and voter privacy when implementing zero-knowledge proofs in decentralized voting systems?

---

**p4u** (2024-12-02):

Hey [@0xsimka](/u/0xsimka), thanks for the question.

So for voter privacy, we use Homomorphic Encryption (ElGamal) over the eliptic curve BN254 within a zkSNARK that is generated by the browser, using SnarkJs. This circuit is around 50k constraints, which takes less than 10s on any desktop/mobile device.

The rest of computation (aggregation of votes, verification, and tally) is performed by specialized nodes (aka Sequencers) that can scale horizontally easily to support huge participatory processes.

We have divided the Sequencer(s) work into 3 zkSNARK circuits. So it’s easier to parallelize. The expensive work (which is verifying ECDSA signatures and verifying Census eligibility) is a job that can be split among as many computers as required. So building a “cluster” of computers to process votes is almost an out-of-the-box task. Our Sequencer implementation will have this functionality integrated.

Finally, with our tokenomics model, we aim to align incentives and incentivize the Sequencers based on the number of verified votes. We expect that the infrastructure will scale up to the necessary to process an election, no matter how big it is.

---

**p4u** (2024-12-02):

> This is an extension of the article.

# Vocdoni Circuits details

The Vocdoni voting process uses a chain of four cryptographic circuits: one generated by the user and three by the sequencer. Each circuit builds upon the previous proof recursively. By dividing the sequencer’s work into three circuits, we enable parallel processing, enhancing scalability and minimizing the risk of collisions when multiple sequencers generate state transitions simultaneously.

1. Vote Circuit: Generated by the user when casting a vote, this circuit proves that the encrypted ballot is valid and that the nullifier and commitment are correctly generated.

Constraints: Approximately 53,000
2. Curve: BN254
3. Framework: Circom/SnarkJS
4. Actor: User
5. Authenticate Circuit: Generated by the sequencer, this circuit transforms the vote proof to the BLS12-377 curve for native recursion and validates the user’s eligibility in the census, as well as their signature.

Constraints: Approximately 3.1 million
6. Curve: BLS12-377
7. Framework: Gnark
8. Actor: Sequencer
9. Aggregate Circuit: This circuit accumulates multiple authenticated votes into a single proof. It also verifies that all accumulated votes belong to the same voting process.

Constraints: 40,000 × (number of votes)
10. Curve: BW6-761
11. Framework: Gnark
12. Actor: Sequencer
13. State Transition Circuit: Given the aggregated votes proof, this circuit verifies the correct inclusion of all new votes into the process’s state Merkle tree. It generates the final state transition proof that will be validated by the Ethereum smart contract.

Constraints: Approximately 4 million
14. Curve: BN254
15. Framework: Gnark
16. Actor: Sequencer

By structuring the process this way, we ensure that voting can be performed from any device—including smartphones and web browsers—while keeping the sequencer’s computational requirements within the capabilities of accessible, CPU-based machines with 64 GiB of memory.

[![image](https://ethresear.ch/uploads/default/optimized/3X/a/6/a6d056e6a683e1fcdf89834cb99c3787b5a1d868_2_690x268.png)image1477×575 42.2 KB](https://ethresear.ch/uploads/default/a6d056e6a683e1fcdf89834cb99c3787b5a1d868)

## Circuits definition

### 1. Vote

**Assertions**:

- The ballots meets the ballot mode provided following the protocol rules.
- The ballots encryption is correct.
- The nullifier and commitments are correctly computed.

[![image](https://ethresear.ch/uploads/default/optimized/3X/b/3/b3542ef4dbe7063316ec100edd9a1f4ec2750d7a_2_690x276.png)image2939×1177 172 KB](https://ethresear.ch/uploads/default/b3542ef4dbe7063316ec100edd9a1f4ec2750d7a)

### 2. Authenticate

**Assertions**:

- The vote zkProof is valid for the inputs provided.
- The signature of the inputs provided is valid for the public key of the voter.
- The address derived from the user public key is part of the census, and verifies the census proof with the user weight provided.

[![image](https://ethresear.ch/uploads/default/optimized/3X/1/6/164302f9c677a190f310848f67ca982f496923c4_2_690x429.png)image2448×1523 198 KB](https://ethresear.ch/uploads/default/164302f9c677a190f310848f67ca982f496923c4)

### 3. Aggregate

**Assertions**:

- The accumulated zkProofs are valid.
- The ProcessId, CensusRoot, BallotMode and EncryptionPubKey is the same for all of them.

[![image](https://ethresear.ch/uploads/default/optimized/3X/3/6/36212929d2d989150b77a5080fd9849e5dce940d_2_690x293.png)image2588×1099 124 KB](https://ethresear.ch/uploads/default/36212929d2d989150b77a5080fd9849e5dce940d)

### 4. State Transition

**Assertions**:

- The agreggated zkProof is valid.
- The MerkleTree transition witness proves every change between Root1 and Root2.
- ProcessID, BallotMode, CensusRoot, EncryptionKey remain unchanged.
- Ballots are correctly counted as new or overwrites, and added to results accumulators.

[![image](https://ethresear.ch/uploads/default/optimized/3X/d/7/d75cf4f4bb5627834e763c7982d525db8dda458e_2_690x448.png)image3396×2206 339 KB](https://ethresear.ch/uploads/default/d75cf4f4bb5627834e763c7982d525db8dda458e)

---

**p4u** (2024-12-02):

> This is an extension of the article.

The Census is a binary Merkle-Tree (iden3 SMT) using a zkSNARK friendly hashing function.

The Path is the Address of the voter, while the Leaf value is the voting Weight for such address.

[![image](https://ethresear.ch/uploads/default/optimized/3X/9/6/96e5a49163fed9a029f1d64772b06d7aa3d74e00_2_690x324.png)image2181×1027 119 KB](https://ethresear.ch/uploads/default/96e5a49163fed9a029f1d64772b06d7aa3d74e00)

The Organizer of the voting is the responsible for building the Census (using our provided tools or any other third-party framework). Only the Root Hash of the Census merkle-tree is stored onchain. The data is shared on IPFS so anyone (including Sequencers) can fetch it and generate merkle-proofs to prove voter eligibility.

This is a simple but flexible and powerful approach that gives the Organization the capacity to decide how to build the eligibility dataset.

How the Census is built is not part of the protocol; however, we would like to provide some tools to construct the most common ones. To support NFT or ERC20 based censuses, there might be two options:

- Optimistic approach: Someone builds the Census for a specific Ethereum block and State Hash, fetching all addresses and balances (see Vocdoni’s Census3 implementation) and pushes the Root to a smart contract. There is a period where anyone can open a dispute if the data used is not accurate. Creating a fraud proof might be easy, just upload a Merkle-Proof of the Census and a Storage-Proof of Ethereum (EIP1186) proving discrepancy.
- Zk approach: For an Ethereum block number and a State Hash and a total supply balance, verify the correct construction of the Merkle-Tree Census using an offchain zkSNARK circuit. For each token holder, verify its storage-proof. The sum of all verified storage-proofs must match the total supply for the token.

While the ZK approach is more secure and trust relies solely on cryptography, it might be computational expensive when dealing with ERC20/NFT tokens with many tokenholders. We would need to make some numbers, but it’s probably feasible for up to 5k token holders. For bigger censuses, the optimistic approach seems a better option.

---

**ivokub** (2024-12-04):

Hi, seems a nice description. Imo it follows quite closely the current state of art. I have a few questions though:

- how do you defend against privacy breaking attacks due to the malleability of Elgamal. See e.g. https://orbilu.uni.lu/bitstream/10993/49442/1/main.pdf. Do you explicitly require proof of knowledge of plaintext?
- you say that the nullifiers allow to obscure the link between voter and ballot, but it is possible to compute the public key from signature+msg (for example as in Ethereum ECREC precompile). Wouldn’t this break the privacy assumption?
- for overwriting the votes, does the voter need to know its previous seed s as used to compute the identity commitment?
- to avoid censorship, does the sequencer also provide fault proofs for invalid votes? Otherwise, what would prevent the sequencer to reject valid votes (due to some metadata a la submitters IP etc.)?
- do you have any ideas on how to do electoral roll-less voting? Right now the MT stores the valid voters, but this inherently requires a bootstrapping/registration phase. However, in many cases this would be infeasible to prepare - for example in case the vote is authorized by some electronic identity provided by another party (national IDs, passkeys etc.).

Sorry if the questions have already been answered in the full whitepaper.

---

**p4u** (2024-12-04):

Thanks for the questions [@ivokub](/u/ivokub), they are pretty interesting, let’s try to clarify point by point.

> how do you defend against privacy breaking attacks due to the malleability of Elgamal. See e.g. https://orbilu.uni.lu/bitstream/10993/49442/1/main.pdf . Do you explicitly require proof of knowledge of plaintext?

AFAIU the attacks described in the paper exploit weaknesses in protocols that do not require proofs of correct encryption and allow ciphertext malleability to go unchecked. However, our proposed protocol:

- Requires a zero-knowledge proof that each encrypted vote is correctly formed (plaintext proof of knowledge).
- Sequencers are required to verify these proofs before including votes in the state. Any vote without a valid proof is rejected.
- The State transitions are also verified using zkSNARKs before being accepted by Ethereum.
- The decryption of the final aggregated vote uses threshold cryptography, requiring collaboration among a threshold number of sequencers. A single sequencer cannot decrypt votes without collusion.

> you say that the nullifiers allow to obscure the link between voter and ballot, but it is possible to compute the public key from signature+msg (for example as in Ethereum ECREC precompile). Wouldn’t this break the privacy assumption?

This is probably not properly described in the document. The Privacy assumption is provided by the usage of Homomorphic Encryption. The detaching of Nullifiers and voter Addresses is an extra protection measure to mitigate future potential Quantum Attacks over the encrypted ballots. The Sequencer (and only him) aggregating the ballot obtains the plain-text Address and Signature from the voter, so it is not hidden under its perspective. But for third-parties or other Sequencers, the usage of a Secret as secret input of the Commitment, makes it hard or impossible to link a Nullifier with an Address.

> for overwriting the votes, does the voter need to know its previous seed s as used to compute the identity commitment?

That is right. The voter needs to build a zkProof of its encrypted ballot again to send an overwrite and the proof requires the Secret to construct the Commitment and Nullifier (which are both public inputs).

> to avoid censorship, does the sequencer also provide fault proofs for invalid votes? Otherwise, what would prevent the sequencer to reject valid votes (due to some metadata a la submitters IP etc.)?

This is a good observation. There is nothing that prevents a Sequencer from rejecting valid votes, only the reward mechanism. The more votes and overwrites validated by a Sequencer, the more reward. If absolutely all Sequencers collude on not accepting votes from a specific voter identity, the voter would be censored.

We might mitigate this problem, allowing anyone (not only the Sequencers) to perform state-transitions. There is actually not a strong reason to not do that, just in this first proposal we preferred things a bit more under control.

> do you have any ideas on how to do electoral roll-less voting? Right now the MT stores the valid voters, but this inherently requires a bootstrapping/registration phase. However, in many cases this would be infeasible to prepare - for example in case the vote is authorized by some electronic identity provided by another party (national IDs, passkeys etc.).

Yes, we do want to support Credential Service Provider (CSP) elections. So instead of a MT of identities, the voter’s eligibility is issued by a trusted authority (or several).

We do actually have designed (not in the whitepaper) a zkSNARK circuit to validate eIDs, such as the Spanish or the Estonian one, using OCSP for discarding revoked IDs, a root RSA CA certificate that provides a chain of trust over other Authorities and all its specifics.

Our current design is prepared to support such kinds of identities. Since the zkSNARK generated by the voter does not verify any signature (this is done by the Sequencer), we can easily incorporate RSA and other, not SNARK-friendly, cryptography schemas just be changing the “Authenticate vote” circuit (see here [Vocdoni Protocol: Enabling Decentralized Voting for the Masses with ZK Technology - #4 by p4u](https://ethresear.ch/t/vocdoni-protocol-enabling-decentralized-voting-for-the-masses-with-zk-technology/21036/4#p-51486-h-2-authenticate-4))

In future versions, we’ll provide support for current eIDs, eIDAS and electronic Passports, it is in our Roadmap. But we wanted to start simple.

---

**ed255** (2024-12-05):

Hi! After reading your post and the white paper I have a few questions about the protocol.

What would happen if a sequencer doesn’t re-encrypt the ballots? Or what happens if a sequencer re-encrypts the ballots in a reversible way (using non-secret values)?  If a third party controls that sequencer, then this third party could have verifiability of the vote contents with cooperation from the user right?  Is the mitigation for that the fact that the user could vote again and change their ballot content?

Have you considered the attack where a malicious sequencer is updating the state in each block, preventing others from updating the state?  For example, the proving time for a regular update is 1 minute on regular hardware and the attacker has better hardware to generate an “very small” update in 20 seconds.  The legitimate sequencer would never have the chance to submit an update because they will always find their update targeting an outdated root.

Could you give more details about the non-collusion assumption from the sequencers?  In particular, what kind of attacks can the sequencers perform if they collude?  For example I can imagine the following 2 scenarios:

- I want to censor a particular voting process. I wait until the sequencers have been chosen. I convince N - k + 1 sequencers to not participate in the decryption process, and I’ll pay them more than the stake they will lose. If they agree, then by the end of the process only k-1 will be available for decryption which is not enough.
- Same as before but convincing k sequencers such that the private key can be reconstructed. What can the attacker do with the private key and control over some or all k sequencers?  Can they de-anonymize ballots and the user that submitted it?

The protocol introduces economic incentives for the sequencers, but it was not super clear to me what these economic incentives achieve and what they don’t. My impression is that the economic incentives try to give liveness on the voting process, but they don’t give security as the sequencers can still collude and earn their rewards.  Is this correct?

Finally, could you elaborate on the flow related to the user commitment and the voting step?  My understanding is that the user would first create a commitment with a secret `s` and prove inclusion in the census.  And then in a later step, the user would cast a vote proving knowledge of an `s` of a commitment without revealing the user identity, in order to achieve unlinkability between voter and ballot.  Is this correct?   If not, could you clarify this flow?  To me this was not very clear from the white paper description.

---

**p4u** (2024-12-05):

Great questions [@ed255](/u/ed255), thanks for taking the time to analyze the proposal.

![](https://ethresear.ch/user_avatar/ethresear.ch/ed255/48/18497_2.png) ed255:

> What would happen if a sequencer doesn’t re-encrypt the ballots? Or what happens if a sequencer re-encrypts the ballots in a reversible way (using non-secret values)? If a third party controls that sequencer, then this third party could have verifiability of the vote contents with cooperation from the user right? Is the mitigation for that the fact that the user could vote again and change their ballot content?

The Sequencer must re-encrypt, this is verified by the state-transition zkSNARK circuit.

If the Sequencer makes public the random factor ‘k’ used for the re-encryption, for some time the Voter might have a receipt. However, since other Sequencers must do random re-encryptions, at some point the stored ballot will be rewritten and the User won’t be able to prove its content anymore. In addition, the user could also just overwrite the vote at any time.

This might end up in a race, and if the Voter is lucky (`voter+maliciousSequencer vs honestSequencers`), he might end up with a receipt at the end of the voting period. However, this attack won’t scale much and might be mitigated increasing the mandatory random re-encryptions by Sequencers.

![](https://ethresear.ch/user_avatar/ethresear.ch/ed255/48/18497_2.png) ed255:

> Have you considered the attack where a malicious sequencer is updating the state in each block, preventing others from updating the state? For example, the proving time for a regular update is 1 minute on regular hardware and the attacker has better hardware to generate an “very small” update in 20 seconds. The legitimate sequencer would never have the chance to submit an update because they will always find their update targeting an outdated root.

Yes, we have considered this attack. This is one of the reasons why we split the Sequencer ZK circuits into 3 smaller ones. The only that requires recomputing if the State changes, is the number 4 (state transition) and takes around 10-15s to be proven in regular hardware. So in order to perform this attack, the malicious Sequencer must do approximately 1 state-transition for each 1-2 Ethereum blocks during the whole voting period, which would be very costly.

If this attack becomes a reality, it can also be mitigated by assigning each participating sequencer a slot for uploading such state change.

![](https://ethresear.ch/user_avatar/ethresear.ch/ed255/48/18497_2.png) ed255:

> I want to censor a particular voting process. I wait until the sequencers have been chosen. I convince N - k + 1 sequencers to not participate in the decryption process, and I’ll pay them more than the stake they will lose. If they agree, then by the end of the process only k-1 will be available for decryption which is not enough.

Yes, if a malicious actor is able to “buy” `N - k + 1` Sequencers, the results might not be available. However, consider two things:

1. The Sequencers, after receiving the Payment, might just publish the decryption share. Late, but results might become available at some point. So it does not seem like a very safe business for the attacker.
2. There is the“Security”" factor picked by the Organizer. It directly impacts the price of the voting but establishes the minimum number of Sequencers that must participate and the k parameter. In a high stake voting, the Security factor must be higher, so this attack becomes less feasible.

![](https://ethresear.ch/user_avatar/ethresear.ch/ed255/48/18497_2.png) ed255:

> Same as before but convincing k sequencers such that the private key can be reconstructed. What can the attacker do with the private key and control over some or all k sequencers? Can they de-anonymize ballots and the user that submitted it?

With the private key shares of `N - k + 1` Sequencers, the attacker might de-anonymize the encrypted ballots, yes. However:

1. The attacker still needs the relation between the address and nullifier. So either he needs to know the secret ‘S’ for each voter, or he needs to collude with all Sequencers to fetch this relation. Since only the Sequencer verifying the vote is the one that knows about this relation (necessary to verify the Signature).
2. The attacker nor the Sequencers can modify the results, which are still safe.

![](https://ethresear.ch/user_avatar/ethresear.ch/ed255/48/18497_2.png) ed255:

> The protocol introduces economic incentives for the sequencers, but it was not super clear to me what these economic incentives achieve and what they don’t. My impression is that the economic incentives try to give liveness on the voting process, but they don’t give security as the sequencers can still collude and earn their rewards. Is this correct?

Yes, it is correct. The main focus of the economic incentives is to reward Sequencers and to ensure the layer2 infrastructure works. Colluding is very difficult to penalize because it’s challenging to prove. Please let me know if you have some ideas on this direction ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/ed255/48/18497_2.png) ed255:

> Finally, could you elaborate on the flow related to the user commitment and the voting step? My understanding is that the user would first create a commitment with a secret s and prove inclusion in the census. And then in a later step, the user would cast a vote proving knowledge of an s of a commitment without revealing the user identity, in order to achieve unlinkability between voter and ballot. Is this correct? If not, could you clarify this flow? To me this was not very clear from the white paper description.

This is a common misunderstanding, I think we need to find a better way to explain it. I do believe [@ivokub](/u/ivokub) did a similar question in a previous post. I will make a more clarifying explanation and comment on the decision:

1. Ideally, the user would anonymize its identity when casting the vote. Then we would have 2 privacy measures (HE + ZK).
2. However, generating a Nullifier is challenging, if there is no direct access to the private-key (i.e Hardware Wallet, Passport, eID, etc.). And/Or if the signature scheme does not produce deterministic signatures (as in ECDSA or RSA).
3. So if we want to support these common user cryptographic identities, we cannot hide the user identity on the first zkSNARK.
4. Then we went for a hybrid/partial approach. Detach the Address from the Encrypted Ballot by using a secret commitment. Only the Sequencer processing the vote knows this relation. This does not provide 100% anonymity, but since we are already using HE, it won’t hurt.
5. This can help to mitigate some attacks. Specially those “future” attacks using Quantum Computing. Since the Encrypted Ballots are publicly stored (in Ethereum data Blobs), in the future a Quantum Computer might break ElGamal/bn254 and reveal voter’s choices. However, since the Commitment hides the relation between Address and EncryptedBallot and theoretically, most hash functions are Quantum resistant. This attack might have no real impact. And at that time we will be already using Lattices everywhere

---

**jordipainan** (2024-12-05):

Hi ! Thank you for your question.

The protocol can be adapted to support non-predefined voter lists. In this case you typically need a credential service provider (CSP) so the voter’s eligibility is issued by one or several trusted authorities, i.e ICAO for Electronic Passports, in contrast to the MT approach we are describing on the paper.

This is not limited to state or UN issued certificates, and it is also suitable for any kind of SSI.

Cool thing about this “CSP approach” is that these credentials can be issued in real-time so a voter can request at any point a valid credential and participate.

Given how the protocol is designed the anonymity, immutability and verifiability of the votes is also guaranteed.

Regarding how can be adapted, given that the zkSNARK generated by the voter does not verify any signature, you just need to change the “Authenticate vote” circuit (on the sequencer). Other parts of the protocol remain the same.

We already designed a zkSNARK circuit for validating electronic ID’s and we plan to extend it, or create new ones, for supporting other kind of CSP identifications.

The biggest part of the work here is that the cryptographic schemes used in such scenarios vary, so it is a matter of adding support for these different schemes.

---

**p4u** (2025-01-20):

We are considering renaming the Protocol and detaching it from Vocdoni. The suggested new name following MACI acronym idea is:

**DAVINCI**

*Decentralized Autonomous Voting Infrastructure for Non-Coercive Inclusion*


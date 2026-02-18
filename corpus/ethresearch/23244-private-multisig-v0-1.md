---
source: ethresearch
topic_id: 23244
title: Private Multisig v0.1
author: Arvolear
date: "2025-10-16"
category: Privacy
tags: []
url: https://ethresear.ch/t/private-multisig-v0-1/23244
views: 1001
likes: 9
posts_count: 11
---

# Private Multisig v0.1

11.12.25 UPD: The PoC implementation of the proposal is now ready and is available [here](https://github.com/distributed-lab/private-multisig).

---

Here is something I’ve been working on for some time already. Not perfect, but as privacy-preserving multisig as possible. Would love to hear your feedback!

Please do check out my other, but related research papers: [Confidential WETH](https://ethresear.ch/t/confidential-wrapped-ethereum/22622/1) and [ZEX: Confidential Peer-to-Peer DEX](https://ethresear.ch/t/zex-v0-1-confidential-peer-to-peer-dex/22949).

Also, take a look at the magnificent [Ethereum Privacy Roadmap](https://ethresear.ch/t/ethereum-privacy-the-road-to-self-sovereignty/22115).

---

### Abstract

The paper proposes a practical approach to implement a Zero Knowledge (ZK) EVM-based multi-signature wallet to preserve the privacy and confidentiality of collective decisions. The approach combines three core features: Merkle tree membership proofs for anonymity, aggregated ECC ElGamal encryption for participants’ votes confidentiality with bias-free decision making, and Distributed Key Generation (DKG) for non-interactiveness in the keys deduction and elimination of centralized, trusted entities.

The proposed solution consists of Solidity smart contracts and ZK circuits. The former plays the role of an accounts factory and the actual accounts that users interact with to create multisigs and execute collective proposals. The latter is responsible for checking users’ belonging to the multisig sets and verifying their decisions on whether to execute a proposal or not, without revealing intermediate results.

The downsides of the proposed approach are that all multisig participants must vote on the proposal to calculate its outcome, and that key rotations are required, limiting the multisig to sequential decision-making.

# 1. Introduction

The transparency of public blockchains offers a multitude of advantages, including enhanced traceability of actions, execution verifiability, and openness of data that is available to everyone. However, it poses unique challenges in multiparty decision-making, particularly in preserving privacy and preventing voting bias — fundamental aspects of a secure and impartial multisig wallet.

The goal is to create a simple, permissionless multisig that doesn’t disclose anything about its members and provides multisig voters with the assurance that their ballots are secret and their choices are not influenced by how early participants vote.

The multisig would allow users to be included/excluded from the members list, the configuration of the “signature threshold”, and execution of collectively approved transactions, with (almost) zero compromises in privacy. Along with that, users will be able to vote for or against the proposals without knowing the individual votes or the result until all the users from the membership list have cast their ballots.

Of course, the important limitation is that the last voting participant will be able to decrypt and see the ongoing proposal direction prior to casting and disclosing their vote.

# 2. Specification

## 2.1. Application flow

Before proceeding with the technical deep-dive, it is essential to see the high-level picture and understand the basic application flow. The flows for a multisig wallet creation, proposal creation, and generic multisig transaction execution with proposal voting are provided.

### 2.1.1. Multisig creation

The cornerstone of the application is the multisig wallet. Upon interacting with the application, users create multisigs with the list of permitted voters for their business logic.

The multisig creation flow is depicted in the following diagram:

[![Figure 1: ZKMultisig contract creation flow](https://ethresear.ch/uploads/default/optimized/3X/e/f/ef1491700f1f541c8e4a8cf32f26fd339449f979_2_690x437.png)Figure 1: ZKMultisig contract creation flow3159×2003 247 KB](https://ethresear.ch/uploads/default/ef1491700f1f541c8e4a8cf32f26fd339449f979)

1. The creation flow starts with the user (wallet creator) gathering the public keys of the voters to be added to the permitted list. Since the multisig utilizes ZK to maintain privacy, all the users have to create a special babyJubJub key pairs that will be used as their unique identifier before using the application.
 To create these keys, users sign an EIP-712 structured messages with their Ethereum (ECDSA) private key and hash the obtained signature. The resulting hashes areis the babyJubJub private keys.
 Users may choose between signing the unique messages to get unique public keys for every multisig they are willing to participate in (increases privacy) or using the “default” message to stick to a single public key to be utilized across the platform (possibly better UX).
2. Having acquired all the necessary babyJubJub public keys, the wallet creator invokes the wallet creation function on the ZKMultisigFactory smart contract, providing all the public keys to be added to the permitted list. Under the hood, the multisig stores the participants in a Cartesian Merkle Tree (CMT) [3] data structure, enabling ZK-provable membership proofs and cheap list maintenance.
3. After the multisig wallet is deployed, its members can create proposals and vote on them by generating ZK proofs of membership and applying EdDSA blinders for decision non-reusability.

With the described approach, we can achieve full privacy for the users by abstracting their real “wallet address” with a babyJubJub one through a deterministic key derivation function (KDF) and decrease the probability of determining the decision-making address from 1 to 1/N, where N is the number of multisig members.

### 2.1.2 Proposal creation

The proposal creation flow is depicted in the diagram below:

[![Figure 2: Multisig proposal creation flow](https://ethresear.ch/uploads/default/optimized/3X/2/e/2ec206e6769710306f57b2ab51c2292de6bd7fdc_2_672x500.png)Figure 2: Multisig proposal creation flow4360×3240 435 KB](https://ethresear.ch/uploads/default/2ec206e6769710306f57b2ab51c2292de6bd7fdc)

1. The proposal creator (a user from the multisig permitted list) logs in to the application by deterministically recovering the babyJubJub key pairs from the “multisig wallet creation” step.
 The KDF algorithm remains the same. The EIP-712 structured message is obtained from the ZKMultisigFactory, then signed, and the signature is hashed to calculate the babyJubJub private keys.
2. The user generates a ZK proof that permissionlessly verifies their membership in the multisig via a CMT inclusion proof.
3. The proposal creator computes the ID of the proposal to be used in the generation of a one-time aggregated encryption key.
4. The creator non-interactively calculates the encryption key share of every multisig participant using KDF based on the proposal ID and the participants’ babyJubJub public keys.
5. After calculating all the encryption key shares, the creator aggregates them into the final encryption key.
6. The proposal creator invokes the createProposal function via the relayer, providing the CMT inclusion proof and the aggregated key to be further used for votes encryption.

After the proposal is created, multisig participants can start casting their votes.

Note that a new proposal cannot be created if there already exists an active proposal. This constraint is essential to prevent key leakage, as having several active votings at the same time would invalidate the required key rotation.

### 2.1.3. Voting on the proposal

The voting on the proposal flow is depicted in the following diagram:

[![Figure 3: Multisig proposal voting flow](https://ethresear.ch/uploads/default/optimized/3X/6/6/66525cf1535e14b69880bc1bec7b5f4fb59e68c0_2_500x500.jpeg)Figure 3: Multisig proposal voting flow1920×1939 183 KB](https://ethresear.ch/uploads/default/66525cf1535e14b69880bc1bec7b5f4fb59e68c0)

1. The CMT inclusion (Merkle) proof is fetched from the contract to indicate that the user is a member of the multisig.
2. The user signs (with their first babyJubJub private key) the proposal they are voting on to generate a blinder by hashing the obtained EdDSA signature. It is used to verify that they have not previously voted for the same proposal.
3. The user fetches the encryption key of the proposal.
4. The received ephemeral encryption key is used to encrypt their vote.
5. Based on the proposal ID, the user calculates the decryption key share using their babyJubJub private keys and KDF.
6. The second public key is rotated with the one generated by signing a new EIP-712 message and hashing the signature. This rotation is crucial because the key derivation share calculation is a linear equation. If the second private key remains constant, having just two voted proposals, an attacker can solve a system of linear equations, revealing everyone’s master secret keys.
7. The user generates the nullifier by hashing the old second private key. This nullifier is used to prevent the reuse of the old sk_2 in future votings, as the corresponding old pk_2 is never revealed inside the transaction to preserve anonymity.
8. After calculating all the needed data, the multisig participant invokes the vote function via the relayer, providing the encrypted vote, decryption key share, rotated public key, old private key nullifier, and the ZK proof.
9. The smart contract adds the provided decryption key share to the aggregatable final decryption key and sets the vote as successfully cast.

### 2.1.4 Vote Revelation and Proposal Execution

Only when the last participant has voted is the decryption key complete and can be used to reveal the voting outcome. This is done by calling the `reveal` function. It decrypts the aggregated votes and changes the proposal status according to the voting result. If the number of “for” votes exceeds the “signature threshold”, the proposal is set to be “accepted” and can be executed, “rejected” otherwise.

The diagram below illustrates the votes revelation process, encapsulating the decryption and execution logic into the single function `revealAndExecute`.

[![Figure 4: Multisig proposal votes revelation flow](https://ethresear.ch/uploads/default/optimized/3X/1/7/176cf53f047b5c82998b79e8baf4ed7be1c88d60_2_516x333.png)Figure 4: Multisig proposal votes revelation flow2390×1540 169 KB](https://ethresear.ch/uploads/default/176cf53f047b5c82998b79e8baf4ed7be1c88d60)

## 2.2. Encryption Math

This section provides the mathematical foundation of the vote encryption logic used in the protocol.

### 2.2.1. Elliptic Curve Arithmetic Operations

In the context of this document, certain operations are performed on elliptic curves and involve specific mathematical operations distinct from conventional arithmetic:

- Point addition P + Q, where P and Q are points on the elliptic curve, is performed according to the defined group operation logic.
- Scalar multiplication k \times P, where k is a scalar and P is a point on the elliptic curve, involves adding the point P to itself k times.
- Point subtraction P - Q, where P and Q are points on the elliptic curve, and is identical to P + (-Q), where -Q is the inverse of point Q.

### 2.2.2. KDF for Encryption Keys

The protocol utilizes the stealth key schema CoM17 [1] as the deterministic KDF. Such a schema enables the generation of unique key shares to encrypt and decrypt votes for each proposal out of at least two master keys.

The master key pairs must satisfy the following:

pk_1 = sk_1 \times G,

pk_2 = sk_2 \times G,

where pk_1, pk_2 — master public keys,

sk_1, sk_2 — master secret keys,

G — base point on the elliptic curve.

The babyJubJub key pairs generated during the wallet creation are used as the master key pairs from which the ElGamal encryption and decryption keys are derived. Note that only the first key pair (sk_1/pk_1) is constant, the second one (sk_2/pk_2) is rotated with every vote. During this rotation, new keys are never related to any of the old key pairs, preserving anonymity. The key derivation procedure is described below.

First, the challenge is computed based on the proposal ID. Note that the multisig intentionally omits the incremental enumeration of proposals to prevent ZKPs replay and frontrunning attacks. This is achieved by asking the proposal creator to sign the challenge of the proposal they are creating. The proposal ID and the challenge are deterministically calculated as follows:

```solidity
proposalId = keccak256(abi.encode(target, value, data, salt));
challenge = poseidon(uint248(keccak256(abi.encode(chainid, zkMultisigAddress, proposalId))));
```

Let r be equal to the challenge. Then the encryption key share is derived as follows:

h_1 = poseidon(r)

h_2 = poseidon(poseidon(r))

P_i = h_1 \times pk_{1_i} + h_2 \times pk_{2_i}

Correspondingly, the decryption key share is derived as follows:

x_i = h_1 \cdot sk_{1_i} + h_2 \cdot sk_{2_i} \mod n

where n — order of the elliptic curve.

The consistency of the key derivation scheme can be proved by:

P_i = x_i \times G = h_1 \cdot sk_{1_i} \times G + h_2 \cdot sk_{2_i} \times G = h_1 \times pk_{1_i} + h_2 \times pk_{2_i}

### 2.2.3. ECC ElGamal Encryption Scheme

The protocol utilizes the Elliptic Curve Cryptography (ECC) modification of the ElGamal encryption scheme [2] to encrypt and, hereinafter, decrypt the multisig votes.

The aggregated encryption key P is a point on the elliptic curve computed by summing all encryption key shares:

P = \sum_{i=1}^N P_i,

where N — number of the multisig participants,

P_i — encryption key share (elliptic curve point).

The participant’s vote is mapped to a point M on the elliptic curve. The generator point G is used as the “for” vote, and the point at infinity as the “against”. A random value k satisfying 0<k<n is chosen. Afterward, the ciphertext (C_1, C_2) is computed:

C_1 = k \times G

C_2 = M + k \times P

To decrypt the vote, first compute the aggregated decryption key share:

x = \sum_{i=1}^N x_i \mod n,

where n — order of the elliptic curve,

x_i — decryption key share (scalar).

Then use the computed aggregated decryption key x to recover the message point M:

M = C_2 - x \times C_1

The consistency of the key aggregation within the ECC ElGamal scheme can be proved as follows:

P = \sum_{i=1}^N P_i = \sum_{i=1}^N x_i \times G

D = x \times C_1 = \sum_{i=1}^N x_i \times C_1 = \sum_{i=1}^N x_i \cdot k \times G = k \times (\sum_{i=1}^N x_i \times G) = k \times P

M = C_2 - D = M + k \times P - k \times P

### 2.2.4. Homomorphic aggregation of votes

Using point G and point at infinity as votes makes it possible to form the cumulative voting result homomorphically, summing up the encrypted votes during each vote cast:

SC_1 = \sum_{i=1}^N C_{1_i}

SC_2 = \sum_{i=1}^N C_{2_i}

Decrypt the sum to get the aggregated result T:

T = \sum_{i=1}^N M_i = SC_2 - x \times SC_1

The decrypted total T is equal to v \times G, where v is the total number of voters who voted “for” the proposal.

To reveal the votes, a multisig participant must loop through the possible scalar values v_i off-chain, where 0 \leq v_i \leq N, to find the value that satisfies the equation:

v_i \times G = T

Then they submit this value to the smart contract, where the above equation is checked.

- If v  Note that it is crucial never to reveal the signature as the private keys derive from it directly.

### 2.3.6. KD EIP-712 message

To create a key derivation EIP-712 message, a KDF message typehash is used that includes the `ZKMultisig` address of the contract. This is sufficient as the network and the contract information are included in the standard EIP-712 domain structure.

```solidity
bytes32 KDF_MSG_TYPEHASH = keccak256("KDF(address zkMultisigAddr)");
bytes32 kdfStructHash = keccak256(abi.encode(KDF_MSG_TYPEHASH, zkMultisigAddress));
```

The `getKDFMSGToSign()` and `getDefaultKDFMSGToSign()` functions create an EIP-712 message as described above. The `getDefaultKDFMSGToSign()` function uses a zero address for the construction of the default message.

The `getRotationKDFMSGToSign()` function returns a similar key rotation EIP-712 message, but it is specific for the provided proposal ID and is computed as follows:

```solidity
bytes32 KDF_ROTATION_MSG_TYPEHASH = keccak256("KDF(address zkMultisigAddr,uint256 proposalId)");

bytes32 kdfRotationStructHash = keccak256(
    abi.encode(KDF_ROTATION_MSG_TYPEHASH, zkMultisigAddress, proposalId)
);
```

### 2.3.7. Relayers

Since the above approach is completely independent of the EVM addresses from which transactions are sent, users can utilize different relayers to preserve anonymity. Protocol-friendly relayers such as GSN can be used, however, this requires additional integration logic on the front end.

# 3. Rationale

The ECC modification of the ElGamal encryption scheme [2] was selected for its compatibility with key derivation functions (KDFs) and key aggregation. ElGamal’s non-deterministic nature, introduced by the random value k, guarantees that each encryption operation produces a unique ciphertext, enhancing security.

To mitigate centralization risks associated with traditional decryption key management, like in the Shamir Secret Sharing (SSS) scheme, where the existence of a decryption key before secret sharing is required, the Distributed Key Generation (DKG) approach was taken. It provides the mechanism to generate the decryption key in a decentralized way by every participant, so that no single party possesses the complete key before revelation.

Most DKG protocols remove the need for a trusted party by employing Verifiable Secret Sharing (VSS), which mandates participant interaction to verify share validity. This process is replaced by verifying ZK proofs of decryption key shares on demand when casting the vote.

Although DKG eliminates the need for key share exchange between parties, it still requires publishing encryption key shares during proposal creation. Using a deterministic KDF, participants can avoid interactive processes, enabling the proposal creator to aggregate the final encryption key asynchronously and independently.

# 4. Security Considerations and Limitations

There are several security risks and limitations inherent to the protocol that need to be considered:

- Trusted setup. If Groth16 is used as a zk-SNARK proving system, a per-circuit trusted setup is required and must be properly carried out.
- Private key/signature leaks. It is essential to keep the key derivation ECDSA signature private. The babyJubJub key pairs are derived directly from it, so leaking the signature would render the multisigs (in which the user is in) vulnerable to phishing / spamming attacks.
- Proposal frontrunning. Even though the proposal challenge is derived deterministically from the proposal contents, it is still possible to frontrun the proposal creation with an identical proposal. This does not directly impact security, yet it should be noted.
- Participant removal deadlock. If a participant to be removed does not vote (which is natural to them), the removal proposal expires, and the participant remains a multisig member. A possible solution may be to vote openly on such proposals.
- Modification of participant list. It is challenging to add or remove participants from the multisig whenever there are active (ongoing) proposals. Doing this may cause inconsistency in the keys used within the encryption scheme. A possible solution may be to track such proposals and allow their creation only when nothing else is in progress.
- Last-voter advantage. Since the decryption of votes is possible once all decryption key shares are known, the last participant can reconstruct prior votes before casting their own.
- No parallel proposals. The protocol is restricted to one active proposal at a time. This is a consequence of the key rotation mechanism used to guarantee the use of a unique sk_2 for the decryption key share calculation. Having more than one proposal open for voting would compromise the security of participants’ private keys because the repeated use of a second key pair creates a system of solvable linear equations that allows an attacker to derive the master secret keys.
- Scalability. Votes revelation and proposal results calculation complexity scales linearly with the number of participants.

# References

[1] Nicolas T. Courtois and Rebekah Mercer. Stealth Address and Key Management Techniques in

Blockchain Systems. 2017. url: https://www.scitepress.org/papers/2017/62700/62700.pdf.

[2] Neal Koblitz. Elliptic Curve Cryptosystems. 1987. url: https://www.ams.org/journals/mcom/1987-48-177/S0025-5718-1987-0866109-5/S0025-5718-1987-0866109-5.pdf.

[3] Artem Chystiakov, Oleh Komendant, and Kyrylo Riabov. Cartesian Merkle Tree. 2025. url: [[2504.10944] Cartesian Merkle Tree](https://arxiv.org/abs/2504.10944).

## Replies

**0xAmol** (2025-10-17):

If the engineering challenges around efficiency, scaling, front-run resistance, and member churn are solved - could see strong adoption in privacy-sensitive multisigs, DAO governance, and treasury management. It also has potential to reshape how privacy is handled in multiparty contracts. would figure its impact will ultimately depend on adoption/network effects, robustness, ecosystem support, and how well the tradeoffs are managed.

curious if the concept will be adopted by others or this will be a standalone ecosystem like bitcoin / zcash..

---

**AnInsaneJimJam** (2025-10-18):

Really liked this paper. I was thinking of implementing this for my project . Do you currently have any implementation or should I start from scratch?.

Thank you

---

**Henry6262** (2025-10-18):

habibi, god bless you man !!!

this info goes BRRRRRR

---

**Arvolear** (2025-10-22):

Hey, thanks for taking a read. We are currently working on a PoC.

---

**AnInsaneJimJam** (2025-10-22):

I was trying to implement this myself. I am very much happy to contribute.

---

**Arvolear** (2025-10-23):

UPD: the initial KDF for encryption keys was found critically insecure. I’ve updated the [2.2.2. KDF for Encryption Keys](https://ethresear.ch/t/private-multisig-v0-1/23244#p-56518-h-222-kdf-for-encryption-keys-11) section with a new scheme. Now users are required to manage two babyJubJub private keys to mitigate “child private key → master private key” derivation.

---

**AdamGagol** (2025-11-12):

I think there is still a leak, specifically if a user votes on two different proposals with the same master keys (I assume it’s not an exotic scenario), the following will be public:

 x_i = h_1⋅ sk_{(1,i)} + h_2⋅sk_{(2, i)}

 x’_i = h’_1⋅sk_{(1,i)}+h’_2⋅sk_{(2,i)}

This is set of two linear equations that with overwhelming probability have a single solution that can be computed to extract secret keys. The way to fix it is to never actually reveal these partial decryption keys, but instead publish partial decryptions, i.e. D_i = x_i ⋅ SC_1   (where SC_1=
\Sigma_i C_{(1,i)} ) plus a zk proof that it was computed correctly.

The bigger problem with the setup is that it seems to be very easy to block a proposal - instead of voting “no”, it’s enough to not vote at all and the proposal will never go through.

---

**Arvolear** (2025-11-13):

Yep. I’ve updated the paper but not the research topic yet. The solution is to rotate the sk2 on each proposal voting. This creates a synchronization limitation (one proposal at each time), but works for PoC. Will update to the latest version later this week.

---

**AdamGagol** (2025-11-13):

Isn’t the above a better tradeoff? Key rotation is always problematic, people often additionally store keys/seeds off-device for security. And if you publish only partial decryptions, you don’t need to rotate, at a cost of some additional constraints in the circuit.

---

**Arvolear** (2025-11-15):

There is no seed to store, the keys are derived “on the fly” from the Ethereum wallet EIP-712 signature. As long as the signature doesn’t leak, private keys are safu.

The problem with partial decryptions is that we don’t know the encryption result beforehand. We don’t know C_1 that users use to vote to compute the partial decryption share (if I understood you correctly).

There is actually a working solution that you can find [here](https://x.com/Arvolear/status/1986032883882991771). It is based on pairings, eliminating the key rotation problem entirely. But unfortunately it is too expensive to implement on EVM.


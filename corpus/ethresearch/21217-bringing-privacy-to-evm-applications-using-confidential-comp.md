---
source: ethresearch
topic_id: 21217
title: Bringing privacy to EVM applications using confidential computing via co-processors
author: nlok5923
date: "2024-12-09"
category: Privacy
tags: [transaction-privacy]
url: https://ethresear.ch/t/bringing-privacy-to-evm-applications-using-confidential-computing-via-co-processors/21217
views: 1607
likes: 24
posts_count: 13
---

# Bringing privacy to EVM applications using confidential computing via co-processors

By me, [@rishotics](/u/rishotics) and team

*Special thanks to [Rand Hindi](https://x.com/randhindi) and the [Zama](https://www.zama.ai/) team for their feedback and suggestions*

## Introduction

Blockchain and DeFi systems promote transparency and decentralization but expose user transaction data to the public. This visibility poses significant privacy risks, deterring privacy-conscious users and opening the door to security threats like front-running attacks.

Privacy is a fundamental pillar of the open-source ecosystem, yet it is often overlooked in DApps. This article explains one of our approach to seamlessly integrate privacy into existing applications rather than creating isolated, fragmented ecosystems where privacy is treated as an afterthought. With billions of USD locked in ecosystems like Ethereum, Solana, and Bitcoin, privacy solutions are not even a part of their near-term roadmap. This leaves users with no choice but to engage with these systems without privacy, exposing sensitive financial data.

Several privacy solutions, including shielded pools, hardware solutions, and threshold encryption, have been attempted to tackle these issues but face significant limitations. Shielded pools, while effective at concealing transaction details, create barriers to adoption due to complex user interfaces and regulatory challenges. Threshold encryption solutions suffer from complex key management and scalability issues in decentralized environments. Consequently, these solutions often sacrifice usability and compliance, limiting their effectiveness in real-world applications.

Privacy-enhancing technologies like FHE, TEE, and MPC offer a novel approach by enabling computations on encrypted data without decryption. Thus, they preserve privacy while addressing the scalability and regulatory challenges that have limited previous solutions. The issue is how to use these PETs with existing EVM stacks or Dapps[[2]](https://www.zama.ai/products-and-services/fhevm).

To make privacy accessible to all users, we need to focus on two key areas:

- Adapting existing application: to be compatible with privacy-enhancing technologies
- If building new application: within existing ecosystems using privacy-preserving technologies

Very few efforts have been made to introduce privacy in existing applications. Our approach tries to tackle the above challenges and provides a generalised way of interacting with current applications.

In this post, we will explore how to incorporate privacy into existing Defi applications on EVM-compatible chains using PETs like FHE. The overall architecture combines off-chain co-processors with on-chain smart contracts. For these off-chain co-processors to interact effectively with on-chain states, we need a framework that enables smart contracts to work seamlessly with encrypted data.

We also discuss the concept of encrypted ERC20 tokens, which provide a privacy-enhanced alternative to standard ERC20 tokens. As, Recently, [Circle and Inco published a report](https://www.circle.com/blog/confidential-erc-20-framework-for-compliant-on-chain-privacy) delving deeper into the topic of encrypted ERC20s. To be precise, Our framework is not tied to any specific encrypted ERC20 standard, making it adaptable for use across multiple standards.

## Background and Related Work

### Current Transaction Flow

The current transaction process—from a user’s wallet → mempool →  block is entirely transparent. This transparency aligns with the core purpose of a public blockchain, where data included in the ledger should be visible to all participants. However, this openness deters many people from entering the space, as not everyone wants their data to be visible to the entire world.

There are various stages in the execution process where privacy can be introduced, and each stage comes with its own set of complexities. Encrypting the transaction as soon as the wallet signs it makes the most sense, as valuable information can then be hidden on the client side.

The challenge lies in modifying the existing infrastructure and achieving community acceptance for these changes. Solutions include encrypted mempools, encrypted solving, private RPC providers, and block building within TEEs, among others. Let’s explore some of the solutions that other teams have worked on in the past.

### Some Previous Privacy Solutions

**Encrypted Mempools**

Teams are already working on encrypted mempool solutions. Threshold-encrypted mempools use threshold encryption to protect transaction details in the mempool until they are ready to be included in a block. This prevents unauthorized parties from viewing transaction details (e.g., sender, receiver, or amount) while the transaction is still pending, addressing issues like front-running in MEV situations. Users can submit transactions with the assurance that their details will remain confidential until the block is confirmed.

However, encrypted mempools has high barrier to entry due to it’s unique cryptographic (Time lock puzzle, Threshold encryption / decryption) or hardware requirements (TEEs).

Most threshold encryption schemes require an initial setup phase that involves distributed key generation, which can be costly in terms of time and resources. In large, decentralized environments, this setup can be challenging—especially when committee members join or leave, requiring key re-shares or even a complete rerun of the setup.

**Shielding Pools**

Current solutions that provide protection for on-chain interactions often lack user-friendliness from a UX standpoint.

Using shielded addresses and pools introduces significant complexity to achieving on-chain privacy. Shielded pools enable users to store and transact assets without revealing transaction details—such as the sender, receiver, or amount—on the blockchain. Zero-knowledge (ZK) proofs facilitate these shielded transactions by validating their legitimacy without disclosing any actual data. This ensures that network participants can verify the validity of a transaction without knowing who sent or received the funds or the amount transferred.

When a user transfers assets into a shielded pool, those assets are “shielded,” with transaction details (amount, sender, receiver) encrypted and hidden from the public ledger. ZK proofs are then used to confirm that the user holds a valid balance and is authorized to spend it, without revealing any specifics. Users can transfer assets between shielded addresses without exposing details within the shielded pool. All transactions remain hidden, with ZK proofs ensuring compliance with transaction rules, such as maintaining balance integrity and confirming valid ownership. If a user chooses to move assets back to a transparent (non-shielded) address, they can withdraw funds. However, this typically results in a “privacy break,” as the withdrawal amount becomes visible unless transferred to another shielded pool.

Without proper checks, shielded pools also raise compliance and regulatory concerns, leaving users uncertain. These pools obscure transaction details, complicating the tracing of funds and the identification of involved parties. Regulators are concerned that shielded pools could facilitate money laundering by concealing illicit funds. Financial institutions and regulated entities must comply with anti-money laundering (AML) regulations, which require the detection and reporting of suspicious activities. Shielded pools limit transaction visibility, making it challenging to verify the origin of funds and adhere to AML standards.

### Some Preliminaries

**Differential Privacy**

Differential privacy is a mathematical framework used to quantify and ensure the privacy of individuals within a dataset [1].

The core idea of differential privacy is to ensure that it is difficult to determine whether any specific individual’s data is included in a dataset, even when analyzing the output of an algorithm applied to that dataset. A randomized algorithm is said to satisfy (ϵ,δ) - differential privacy if the inclusion or exclusion of an individual’s data changes the probability of any specific output only slightly.

In the context of differential privacy, ϵ controls the privacy loss, quantifying the maximum difference in output probabilities for neighboring datasets (datasets differing by only one individual). δ represents the probability of a small relaxation in the privacy guarantee, allowing for a slight chance of greater privacy compromise. This framework ensures that the algorithm’s output remains nearly indistinguishable for neighboring datasets, thereby limiting the information leakage about any single data point.

Differential privacy has become a widely adopted standard for privacy-preserving data analysis, offering robust privacy guarantees while enabling valuable statistical insights.

**Torus-based Fully Homomorphic Encryption**

TFHE is a FHE scheme optimised explicitly for fast binary gate computations. Unlike traditional FHE methods that rely on more complex lattice structures, TFHE operates over the torus, efficiently performing encrypted computations with lower noise accumulation and faster bootstrapping times.

As a result, TFHE has emerged as a promising solution for secure, privacy-preserving computation in real-time applications.

## Solution

### Encrypted ERC20 Tokens

Encrypted ERC20 standard for privatizing user token balances. Any token balance intended for homomorphic computation on-chain would need to be wrapped within this encrypted ERC20 standard. This approach can serve as a foundation for building various privacy-focused solutions, such as private payments, private auctions, dark pools, and more.

This standard implements necessary interfaces which is used to implement necessary compliance checks, which include selective disclosure of specific ciphertext requested and a few other checks.

*To learn more about Encrypted ERC20 you can read this article by Circle [[3]](https://circle.com/blog/confidential-erc-20-framework-for-compliant-on-chain-privacy)*

### Differential Privacy with Order Aggregation and Batch Settlements

We propose a solution leveraging differential privacy to enable order-solving for encrypted orders. This allows users to place encrypted orders (orders with encrypted tokens) and have them processed on-chain without revealing their details. External parties cannot determine the exact order details associated with a specific user.

Batching is a core component of this solution. The challenge with processing a single encrypted order directly through the protocol is that once decrypted, the amount the user intended to hide becomes visible. To mitigate this, we aggregate multiple orders using the additive homomorphic properties of certain privacy-enhancing technologies (PETs), such as Fully Homomorphic Encryption (FHE). The encrypted amounts are summed and deposited as an aggregated value with a designated manager. The manager’s role is to decrypt this aggregated value via a secure wrapper (obtaining the decrypted tokens amountIn values) so that the resulting assets can interact with the appropriate solver protocol.

By batching encrypted orders, we introduce a level of noise into each order, effectively preserving the privacy of individual users’ order details.

[![batching flow](https://ethresear.ch/uploads/default/optimized/3X/8/6/865f81eb157c29f71336f8343369e328ed615ec5_2_690x384.jpeg)batching flow1920×1070 77.2 KB](https://ethresear.ch/uploads/default/865f81eb157c29f71336f8343369e328ed615ec5)

The design is inspired by Zswap DEX of Penumbra [[5]](https://protocol.penumbra.zone/main/index.html), which uses sealed-bid batch swaps. The price at which these orders are settled is identical, as there is only one transaction per epoch.

Once the order is solved, the return token amount belonging to the user is calculated homomorphically using the ratio of the input amount to the output amount (the amount received upon solving the order). This calculation is performed homomorphically in the encrypted space, ensuring that no one can fully determine how many tokens a particular user will receive, thereby preserving privacy.

[![solving flow](https://ethresear.ch/uploads/default/optimized/3X/b/f/bf5aa7c4f3a1ba1cc335df50f2ef43f288a62ffa_2_690x387.jpeg)solving flow1920×1077 54.8 KB](https://ethresear.ch/uploads/default/bf5aa7c4f3a1ba1cc335df50f2ef43f288a62ffa)

End to End flow Order placing → Order Aggregation → Order Solving → Distribution

[![End to end solving flow](https://ethresear.ch/uploads/default/optimized/3X/2/2/22c540c898bdbc16ce7b5c9b5ef4289f18d15e6f_2_690x275.jpeg)End to end solving flow1920×766 67 KB](https://ethresear.ch/uploads/default/22c540c898bdbc16ce7b5c9b5ef4289f18d15e6f)

### Mathematical Formulation

We are proposing two methods for mitigation for the privacy in applications:

- Encrypting Assets: Assets held by the user is encrypted via publicly verifiable encryption scheme.
- Batching Orders: Choosing a size of n of orders to batch prior execution.

Individually these solutions don’t provide enough privacy guarantees from an adversary POV but together it introduced differential privacy which provides probabilistic indistinguishability for a particular user’s order.

Most DeFi action on-chain can be defined as a Tokens going in ( T_{in} ) and tokens coming out ( T_{o} ), which means that any solving action \pi can be written as

T_{o} = \pi(T_{in}, G, V) \\
G: \text{Gas consumed} \\
V: \text{Value transferred}

By changing the domain of interaction for the user with the protocol with we can introduce a middle smart contract M which does this interaction on the users behalf. Now M has the task of receiving orders from n users and aggregating them i \in [1,n]

\pi_{M} = \sum_{i=1}^{n}{\pi_{i}}

We can write the encrypted value of  T_{in}  for a user  i  as  C^{i}  where  C^{i}  can be represented as

C^{i} = (A_0^i,...,A_{k-1}^i,B^i)

The above representation is how a lattice based homomorphically encrypted plaintext looks like.

Now since encryption is homomorphic in nature we can simply sum the individual ciphertexts to form the aggregate ciphertext C^{\pi_M}

C^{\pi_M} =  (\sum_{i=0}^n A_0^i,..., \sum_{i=0}^n A^i_{k-1}, \sum B^i)
 =  (\sum_{i=0}^n {C^{i}} )

In this process we need to perform programmable bootstrapping multiple times which reduces the noise which is getting accumulated in every addition.

The decrypted amount is now used further for interaction with the DeFi protocol.

## Conclusion

Privacy in blockchain and DeFi ecosystems is becoming increasingly crucial to protect user data and secure transaction processes. While various solutions—such as shielded pools, threshold encryption, differential privacy, and fully homomorphic encryption—offer unique approaches, they also present challenges in terms of usability, compliance, and technical implementation.

Exploring these privacy-preserving techniques highlights the potential for integrating privacy into existing blockchain applications while balancing transparency and regulatory requirements. As privacy solutions continue to evolve, they promise to foster a more inclusive, secure, and user-centric blockchain ecosystem, empowering users to engage confidently in decentralized platforms.

## References

[1] [Differential Privacy in Constant Function Market Makers by Tarun Chitra and Guillermo Angeris and Alex Evans](https://eprint.iacr.org/2021/1101)

[2] [Zama’s fhEVM co-processor](https://www.zama.ai/products-and-services/fhevm)

[3] [Unveiling the Confidential ERC-20 Framework: Compliant Privacy on Public Blockchains using FHE](https://circle.com/blog/confidential-erc-20-framework-for-compliant-on-chain-privacy)

[4] [TFHE: Fast Fully Homomorphic Encryption over the Torus by Ilaria Chillotti and Nicolas Gama and Mariya Georgieva and Malika Izabachène](https://eprint.iacr.org/2018/421)

[5] [ZSwap Penumbra](https://protocol.penumbra.zone/main/index.html)

## Replies

**0xsimka** (2024-12-10):

Thank you for sharing this insightful work on integrating privacy into EVM applications using confidential computing and co-processors! I appreciate how the proposed solutions aim to bring privacy to decentralized finance applications while addressing scalability and regulatory concerns.

I’m curious: how do you foresee the implementation of encrypted ERC20 tokens evolving in terms of adoption across different DeFi platforms? Will there be challenges in aligning this privacy enhancement with current regulatory frameworks?

---

**nlok5923** (2024-12-11):

Hi [@0xsimka](/u/0xsimka)!

Specifically for the implementation of encrypted ERC20 tokens there’s are two ways of implementation from two different perspective altogether

From the implementation point of view.

1. There could be different types of middleware contracts (like the manager contract in the above architecture) which basically facilitate usage fo Defi platform privately by passively wrapping users token and using those token to solve their orders. It could be something like a deposit and withdrawal mechanism where user just deposit tokens inside the protocol for use, then user the protocol (for swapping, lending etc) and then once done get out of the protocol by withdrawing his token back.
2. The second way could the Defi platform natively supporting encrypted token this means let’s say we have an AMM where we have implemented an encrypted version of  x*y = k where all the three value x, y \ \text{and} \ k are encrypted.

From the regulatory stand point

- I feel with Encrypted Tokens we’ve so much flexibility of compliance checks for example the platform could just define at which point it needs the share the access of users ciphertext to an external entity (Definitely the platform would need to openly disclose to the quorum what these entities are) or the platform could just impose certain checks which can be on the user’s encrypted identity or something else which aligns with the regulatory measures the protocol is operating in.

---

**askwhyharsh** (2025-01-04):

Interesting stuff,

![](https://ethresear.ch/user_avatar/ethresear.ch/nlok5923/48/12387_2.png) nlok5923:

> There could be different types of middleware contracts (like the manager contract in the above architecture) which basically facilitate usage fo Defi platform privately by passively wrapping users token and using those token to solve their orders. It could be something like a deposit and withdrawal mechanism where user just deposit tokens inside the protocol for use, then user the protocol (for swapping, lending etc) and then once done get out of the protocol by withdrawing his token back

Interesting point about encrypted token standards! So, when someone deposits USDC into an eERC20 to get eUSDC, how do you think we can handle:

1. Hiding the input amount? From what I read about fhEVM, it think it allows encrypted inputs using the user’s public key. Would that mean the amount is first encrypted on the user side? if so, who else can decrypt that? how can the transfer happen without anyone knowing the amount here, assuming the wallet address is public.
2. Are there any working examples or demo implementations of such mechanisms? I’d love to see this in action to understand better how this can work with private computations work.
3. For computations like 𝑒(𝑎) + 𝑒(𝑏), which might rely on co-processor efficiency, how do you think the dependency can be minimised to improve performance, can anyone run a co-processor? i read some things about how the keys are handled in the KMS using MPC, but are there more than 1 nodes and can any new party/node be part of this. also assuming a scenario, where let’s say there is no co-processor running but there is eUSDC that i have that is in an eERC token, how can someone get back to converting their tokens to USDC. let’s assume that KMS is up and working and keys are fine. sorry if my questions are silly or basic, i might be wrong but just curious.

Really curious about the details—let me know if there are resources or projects exploring this!

Thanks

---

**Perun** (2025-01-04):

Interesting! I always wonder how we can decrypt the encrypted tokens. Wouldn’t this require some form of threshold decryption as well? Or do you expect that transaction data stays encrypted forever, which probably would limit use cases.

---

**nlok5923** (2025-01-05):

Thanks for the questions [@askwhyharsh](/u/askwhyharsh)!

> Hiding the input amount? From what I read about fhEVM, it think it allows encrypted inputs using the user’s public key. Would that mean the amount is first encrypted on the user side? if so, who else can decrypt that? how can the transfer happen without anyone knowing the amount here, assuming the wallet address is public.

The conversion or wrapping of normal tokens into encrypted tokens leaves an onchain footprint of how much tokens have been wrapped but the subsequent transactions from the wrapped tokens would now be private since now you’re transferring / using encrypted tokens.

For your second question, Yes the inputs are encrypted on the client end using the master public key of the KMS network. The inputs encrypted by the master public key cannot be decrypted by any single party as it is managed by the KMS network.

For the third one while transferring the user can mention the encrypted amount (whose pre-image (actual amount) the user knows) And since the plaintext is encrypted via homomorphic scheme we can compute on top of the ciphertext to perform a valid transfer.

> Are there any working examples or demo implementations of such mechanisms? I’d love to see this in action to understand better how this can work with private computations work.

We’re launching something on the similar lines very soon. We’ll share the same here as well.

> For computations like 𝑒(𝑎) + 𝑒(𝑏), which might rely on co-processor efficiency, how do you think the dependency can be minimised to improve performance, can anyone run a co-processor? i read some things about how the keys are handled in the KMS using MPC, but are there more than 1 nodes and can any new party/node be part of this. also assuming a scenario, where let’s say there is no co-processor running but there is eUSDC that i have that is in an eERC token, how can someone get back to converting their tokens to USDC. let’s assume that KMS is up and working and keys are fine. sorry if my questions are silly or basic, i might be wrong but just curious.

Amazing questions, Yes I think anyone can run the co-processor probably [@randhindi](/u/randhindi) can better elaborate here. Since co-processor is a totally different entity from KMS network i think even in a scenario where you’ve tokens left in eERC20 standard you should be able to convert it back to normal tokens.

> Really curious about the details—let me know if there are resources or projects exploring this!
> Thanks

For more documentation feel free to explore our [docs](https://docs.encifher.io/docs/intro)

---

**nlok5923** (2025-01-05):

> Interesting! I always wonder how we can decrypt the encrypted tokens. Wouldn’t this require some form of threshold decryption as well? Or do you expect that transaction data stays encrypted forever, which probably would limit use cases.

There are two ways to decrypt your encrypted tokens

- Decrypt: With Decrypt operation you explicitly says the KMS network to decrypt your encrypted tokens such that it i visible to everyone.
- Re-encrypt: With Re-encryption you can request KMS network to re-encrypt the encrypted values without decrypting it under a user generated key. So that only the user can finally decrypt the encrypted value on his end.

For more info you can look into these [docs](https://docs.zama.ai/fhevm/fundamentals/architecture_overview/d_re_ecrypt_compute)

I hope this answers your query!

---

**randhindi** (2025-01-05):

There are 2 components in the protocol:

1. The coprocessor, which is currently ran by Zama in an optimistic fashion, meaning anyone can publicly verify the computation we do. We will also add onchain fraud proofs in the medium term. Longer term the goal is to have zk-fhe, where the coprocessor adds a zk proof of the computation. At this point, anyone can run a coprocessor as long as they provide a correct proof! But this is a few years out in terms of performance
2. The KMS, which is an L2 running a threshold MPC protocol for key generation and decryption of ciphertexts. The KMS reads the access control list on the L1 to know whether the decryption request is allowed. The KMS will initially be run by 10 highly reputable validators (think big foundations, exchanges, etc). The idea is to use reputation as stake, since getting caught cheating would impact their offchain equity in a big way (who will want to business with someone dishonest?). This works because the validators are doxxed, well known and have billions of equity or market cap at stake. Eventually however we want to allow anyone to run a validator, but for this we need to find a way to tie MPC to PoS while also preventing offchain collusion, both of which are unsolved research problem. Fwiw this issue is common to all MPC protocols, and is not specific to Zama.

---

**askwhyharsh** (2025-01-06):

Thanks for the reply [@randhindi](/u/randhindi) ,I’ve been exploring this concept and have been considering its potential implications.

Another question that I have is that could it be feasible for the KMS Layer 2 to eventually leverage Ethereum for trust and validation? Specifically, can we build or adapt an AVS (Attested Validation Service) to run on EigenLayer, utilising its trust network and stake/slash mechanism?

I believe the slashing economics would need to be exceptionally stringent in this context to ensure security and trustworthiness.

What are your thoughts on this approach?

---

**randhindi** (2025-01-06):

That would be ideal, but the issue is more on the MPC side. You need to find a way to identify bad actors and prevent offchain collusions, while also ensuring confidentiality and robustness.

---

**Perun** (2025-01-06):

Yes, this is the main problem and also very exciting from a research point of view. We are currently working on finding suitable mitigations. One (practical) option is to use Trusted Execution Environments. We are currently building [ShutterTEE](https://blog.shutter.network/shuttertee-layered-security-via-meshing-threshold-cryptography-and-state-of-the-art-tee-2/), where key holders run inside an SGX enclave making it much harder for an adversary to collude.

Another option that we are exploring (but currently more on the research side) is to use new cryptographic techniques such as [secret sharing with snitching](https://eprint.iacr.org/2024/1610). Here is also a high-level description of the technique from [Shutter](https://blog.shutter.network/secret-sharing-with-snitching-addressing-shareholder-collusion-in-threshold-cryptography/).

---

**nlok5923** (2025-01-09):

Amazing looking into this!

Is ShutterTEE infra available for production usecases. Would love to see the threshold decryption TPS benchmarks as well.

Thanks

---

**Perun** (2025-01-10):

We completed the first part of the implementation and will finalize the entire project most likely by end of March. We expect the final implementation to be production ready, but would require additional auditing for which we currently do not have funding. We are happy to provide benchmarks of the final implementation, but we expect that overheads will be minor. We will report here once we are done. In case you are interested using the code base (or extending it), it’d be great to talk.


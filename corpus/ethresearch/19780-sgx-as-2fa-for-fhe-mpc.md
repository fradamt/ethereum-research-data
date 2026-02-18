---
source: ethresearch
topic_id: 19780
title: SGX as 2FA for FHE/MPC
author: tolak
date: "2024-06-11"
category: Cryptography > Multiparty Computation
tags: []
url: https://ethresear.ch/t/sgx-as-2fa-for-fhe-mpc/19780
views: 2280
likes: 2
posts_count: 1
---

# SGX as 2FA for FHE/MPC

*About me: I am [Wenfeng Wang](https://x.com/tolak_eth), a builder and researcher at Phala Network, put this topic here and hope to have a comprehensive discussion with the community.*

**TLDR**: Involving SGX introduces a safeguard against the collusion risk inherent in current MPC and FHE systems.

Continuing from Justin Drake’s well-articulated [post](https://ethresear.ch/t/2fa-zk-rollups-using-sgx/14462) about SGX as a 2FA for zk-rollups, I aim to expand on the potential of SGX as 2FA in FHE projects, specifically in their MPC encryption management. Despite their distinct applications, both leverage some fundamental features of SGX.

## MPC is the bottleneck of FHE

Lately, the interest in FHE (Fully Homomorphic Encryption) technologies has rejuvenated, especially in the context of Ethereum Virtual Machines (EVMs). What was once merely a concept is now a tangible tool developers can use to write privacy-preserving smart contracts. Interested readers can refer to Vitalik’s early 2020 [post](https://vitalik.eth.limo/general/2020/07/20/homomorphic.html) about FHE. Now, let’s look at the general architecture of most current FHE projects.

[![image](https://ethresear.ch/uploads/default/optimized/3X/8/f/8f17a45e5c32060cd1578a8f2112437f58880327_2_663x500.png)image2283×1720 165 KB](https://ethresear.ch/uploads/default/8f17a45e5c32060cd1578a8f2112437f58880327)

I will not dive too deep into FHE itself here, but you can find a notable challenge most FHE designs encounter today lies in the MPC node’s key management. Due to the practice of writing an FHE application, the key is globally used by all users to encrypt the data they send to the FHE server, which will execute under an encryption state. Thus, the whole security of the system relies on the security of the MPC network, and as we all know the truths of the MPC network are:

- The more nodes you have, the more latency you get
- The fewer nodes you have, the more trust assumptions you need

## TEE as a 2FA to MPC

We don’t want to give full trust to MPC nodes because of the possibility of collusion if it is run by humans. Instead, we can add SGX as 2FA to hedge the risk by moving the key management to [TEE](https://en.wikipedia.org/wiki/Trusted_execution_environment) (Trusted Execution Environments, a technology to run the program in an isolated zone inside CPU, prove program immutable and limited-accessible).

[![image](https://ethresear.ch/uploads/default/optimized/3X/1/d/1dc05649e162e2e9de3318a6da112754d5a6cd7e_2_608x500.png)image2100×1725 181 KB](https://ethresear.ch/uploads/default/1dc05649e162e2e9de3318a6da112754d5a6cd7e)

As illustrated above, MPC nodes of the FHE system are now running inside TEE, instead of producing TEE proof when acting as 2FA for zk-rollups, here SGX is used to protect the key generation progress in the MPC network, and the whole lifecycle of the key is kept inside TEE and never gonna reveal to the outside world, more importantly, the key can not be touched by human even a single piece. TEE itself can guarantee the program it runs is verifiable, it’s impossible for someone can manipulate the state. Also, the data passing between TEE and the client is secured by TLS communication.

With TEE as a 2FA, it can help reduce the risk in an economic way that:

- If SGX is not compromised, there is no chance that collusion can happen;
- If SGX gets compromised, only when collusion happens between nodes that the system is broken.

## Advantages/Disadvantages of SGX as 2FA for FHE

- Advantages

Security: Remove the possibility of collusion, trust is built on top of machinehood + cryptography instead of humanity.
- Safety: By running MPC inside SGX, even a small MPC network can be reasonably secure. Even if TEE is broken, e.g. have bugs in SGX or Intel being malicious, we still fall back to ordinary MPC.
- Latency: Using SGX, we can get higher security without introducing more workers. This gives more confident to users to run latency sensitive operations on MPC.
- Liveness: SGX didn’t provide extra liveness naturally, but projects like Phala have built a decentralized TEE network that can help make it easy to build an unstoppable network.
- Scalability: Scaling the MPC network is hard, but there are a bunch of existing TEE networks that are ready to deploy MPC nodes. So it lowers the cost to build a larger MPC network.
- Throughout: There also is no throughput lost, but considering the optimization of latency, throughput can be improved theoretically.
- More advantages that can be brought by SGX were well addressed by Justin’s post.

Disadvantage

- It’s worth mentioning that SGX also has its own problems, a quote from Justin’s post:

> SGX has a bad reputation, especially within the blockchain space. Association with the technology may be memetically suboptimal.
> false sense of security: Easily-broken SGX 2FA (e.g. if the privkey is easily extractable) may provide a false sense of security.
> novelty: No Ethereum application that verifies SGX remote attestations on-chain could be found.

- As for the last one that SGX remote attestation on-chain doesn’t exist, the latest state is we have a couple of projects working on it, including Puffer, Automata, and also Phala’s zk-dcap-verifier. But considering it hasn’t been deployed on the mainnet, I kept it on the list.

*Special thanks Justin Drake for his research of [2FA zk-rollups using SGX](https://ethresear.ch/t/2fa-zk-rollups-using-sgx/14462) and Andrew Miller for this research of TEE in Multi-Proof system, check his [presentation](https://docs.google.com/presentation/d/1K96G50S8ICdllQDbEW1su1Ik_eOc5bK9Ih3uvoG-P9Y/edit?usp=sharing).*

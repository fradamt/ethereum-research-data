---
source: ethresearch
topic_id: 20292
title: Decentralized and Verifiable Cloud Service on Ethereum
author: 0x1cc
date: "2024-08-17"
category: Applications
tags: []
url: https://ethresear.ch/t/decentralized-and-verifiable-cloud-service-on-ethereum/20292
views: 1620
likes: 26
posts_count: 8
---

# Decentralized and Verifiable Cloud Service on Ethereum

*by [KD.Conway](https://x.com/0x_1cc)*

## TL;DR

- We propose a decentralized and verifiable cloud service protocol on Ethereum, which can provide computationally intensive service to all web2 or web3 applications, making decentralized ChatGPT, decentralized blockchain explorer reality. By migrating the full stack, including frontend and backend components, to the decentralized cloud, we move toward fully decentralized and verifiable end-to-end Web3 applications.
- The protocol operates under a minority trust assumption, requiring only one honest node to guarantee service quality. Additionally, the correctness of the cloud service is verifiable on Ethereum.
- With near-zero on-chain costs, our decentralized cloud service platform can be even more affordable than traditional centralized options.

## Protocol Overview

[![ecs](https://ethresear.ch/uploads/default/optimized/3X/d/8/d816db0bb6bbc127b1a5f2fa1f320e7c923dbb77_2_690x331.png)ecs1450×697 39.4 KB](https://ethresear.ch/uploads/default/d816db0bb6bbc127b1a5f2fa1f320e7c923dbb77)

A service contract exists on Ethereum, functioning similarly to a gRPC protobuf. This contract defines the service, and the functions within it specify the methods that can be invoked.

Each service provider must register and stake on the service contract. For each service, multiple providers will be available to offer the service.

When a user initiates a service request, such as requesting an AI inference from an LLM model:

- The user first utilizes a verifiable Ethereum light client, such as Helios, to retrieve the list of available service providers from the on-chain service contract.
- The user randomly selects several providers from this list.
- The user then sends off-chain transactions to these selected providers in parallel. These off-chain transactions are essentially the same as calling the corresponding service function in the smart contract, but they use a different chain ID. This specific chain ID indicates that the transaction is intended to call a cloud service rather than perform an on-chain transaction on Ethereum.
- The service providers execute the required computations in their local environments according to the program defined in the corresponding function in the service contract. They then return the responses to the user. Each response is signed by the service provider and includes the user’s transaction hash and the results.
- Upon receiving the responses from the selected providers, the user first verifies the signatures and checks the consistency of the results.

 If the results are consistent, the service is considered to have functioned correctly, and no further action is required.
- If there is a discrepancy in the results, this indicates the presence of at least one malicious service provider. In this case, the user submits the providers’ responses to the on-chain arbitration contract. This triggers a process where the service providers must defend the accuracy of their results. The on-chain arbitration process is detailed in the following section.

## Service Contract

The design of the service contract is akin to the design of gRPC. A new service contract corresponds to a new service in gRPC, and the functions defined in the service contract specify the methods that can be invoked. Due to the constraints of smart contracts, we cannot implement complex computations, such as AI computations, directly within the smart contract. Instead, we define a standard for writing a program, which is then uploaded to decentralized DA services, with the program’s hash stored in the on-chain smart contract.

Following the design principle of “Separate Execution from Proving,” there are two implementations for the service program. One is compiled for native execution, optimized for speed, and can leverage multithreaded CPUs and GPUs to accelerate execution. The other implementation is for proving; the service program is compiled into machine-independent code, allowing us to use zkVM (zero-knowledge virtual machine) or fpVM (fraud-proof virtual machine) to generate proofs. This dual-target approach ensures fast execution, while proving is based on the machine-independent code.

For example, consider matrix multiplication. Native execution utilizes GPU computation (e.g., CUDA) for acceleration. During the proving phase, the service program is compiled into machine-independent instructions, which can be executed in zkVM or fpVM. Both implementations ensure consistent execution results.

[![output](https://ethresear.ch/uploads/default/optimized/3X/b/1/b1ccfdf9e6f994151293a835a4619dca5e974865_2_690x151.png)output1473×323 52.8 KB](https://ethresear.ch/uploads/default/b1ccfdf9e6f994151293a835a4619dca5e974865)

When processing user requests, service providers will run the program in the native execution environment and return the results to the users. Only when on-chain arbitration is required will the service providers run the program for proving. This approach allows service providers to handle requests as quickly as possible in most cases.

Additionally, the service program can be configured to read data from trustworthy sources, such as Ethereum or other blockchains, as well as from decentralized, trustworthy data storage providers. This flexibility allows the service program to function as a blockchain explorer, an AI service, or a decentralized search engine.

A demo version of the service contract is shown below.

```solidity
contract Service {

    // address => web2 domain
    mapping(address => string) serviceProviderHost;

    address[] serviceProviders;

    // function selector => programHash
    mapping(bytes4 => bytes32) programHashs;

    event Request(
        address account,
        bytes4 functionSelector,
        bytes32 programHash,
        bytes input
    );

    function func1(bytes calldata input) public {
        emit Request(msg.sender, this.func1.selector, programHashs[this.func1.selector], input);
    }
}
```

Note that `func1` specifies the method that can be called. When a user wants to call `func1`, instead of sending an on-chain transaction on Ethereum, the user needs to send an off-chain transaction directly to the service providers. Besides, the user can obtain the list of service provider addresses, along with their corresponding Web2 domains using Ethereum verifiable light client.

## Onchain Arbitration

We support multiple proving systems for on-chain arbitration, including zero-knowledge proofs, Trusted Execution Environments (TEE), and fraud-proof systems. For demonstration purposes, we focus on the fraud-proof system, as it offers lower generation costs compared to zero-knowledge proofs and does not require specific hardware. In previous work, we demonstrated the ability to generate fraud proofs for extremely large AI models. For more details, please refer to opML ([[2401.17555] opML: Optimistic Machine Learning on Blockchain](https://arxiv.org/abs/2401.17555)).

The on-chain arbitration process using the fraud-proof system proceeds as follows:

- If a user receives inconsistent results from the service providers, they submit the providers’ responses to the on-chain arbitration contract, initiating an interactive dispute game with all the involved providers.
- At this point, the service providers must run the proving-version of the service program in their local fraud-proof VMs to generate the fraud proof, which they then submit to the on-chain arbitration contract to defend their results. For more details on the interactive dispute game, refer to the fraud-proof system design.
- Service providers who supplied incorrect results will lose the dispute game, resulting in their staked amount being slashed. The slashed stake will be distributed to the winners of the dispute game, as well as to the user, as compensation.

This on-chain arbitration mechanism ensures that only one honest node is required to guarantee the correctness of the provided service. As a result, the protocol relies on a minority trust assumption and inherits security from Ethereum. Assuming at least one honest node and the safety of Ethereum, the protocol can guarantee the correctness of the service.

It’s important to note that on-chain arbitration only occurs when some service providers produce incorrect results. In typical cases, no on-chain interaction is needed, which allows the service to operate as quickly as current centralized cloud service providers.

## Charging Mechanism

There are several possible charging mechanisms:

- Subscription Model: This is similar to the Web2 approach, where the charging mechanism can be conducted off-chain. For example, to use ChatGPT via an API for commercial purposes, you would pay OpenAI a monthly fee to access their services. Multiple service providers can offer the service, allowing for competition and choice.
- On-Chain Payment Mechanism: Paying for each request on-chain can be costly due to transaction fees. Batching and rolling up these requests and payments can significantly reduce on-chain transaction costs. One possible approach is to use payment channels to pay for requests. Alternatively, service providers could generate service proofs and claim fees as follows:

 A service agreement contract specifies the price for each service request.
- Users first stake funds into the service agreement contract.
- Service providers can claim their fees by submitting service proofs to the on-chain service agreement contract. To minimize transaction costs, providers can batch and roll up user requests.
- The on-chain service proof is a zk-proof, which verifies that the service provider has delivered a certain number of responses to users. The provider can then claim the corresponding service fees according to the agreement contract. This proof ensures the correctness of the user’s request transaction signature, the service provider’s response signature, and the transaction nonce.

**Free Service Model:** Another approach is for companies to cover the service fees by the themselves (currently, the web2 companies pay the cloud service fee by themselves), offering free services to users while generating revenue through other means, such as advertising or VIP services.

## Advantages

- This decentralized cloud service can be cheaper than centralized cloud services while maintaining similar speed.

 Cost-Effectiveness: Decentralized servers can be significantly cheaper than centralized cloud servers. For example, io.net has shown that the cost of decentralized GPUs can be as low as one-third of the cost of AWS. For services with lower security requirements, such as using LLMs for personal queries, using just two nodes is often sufficient. Additionally, a random check mechanism can be adopted, querying one node most of the time and occasionally checking another to verify correctness. This setup can be more cost-effective than centralized platform.
- Scalability and Speed: This platform can outperform centralized systems, especially for computationally intensive tasks. A decentralized cloud service platform operates on an N-to-M model (N users with M servers, where the number of servers can be infinite), whereas centralized platforms use an N-to-1 model (N users with a single super server). This allows a decentralized cloud service platform to scale more effectively. For instance, a centralized AI platform like ChatGPT may slow down during peak times because it can’t scale its computing power quickly enough. In contrast, decentralized platform can dynamically distribute the load across many servers, ensuring faster response times even during heavy usage.

**Trustless and Verifiable:** The protocol operates under a minority trust assumption, requiring only one honest node to guarantee service quality. Additionally, the correctness of the cloud service is verifiable on Ethereum.

**Censorship-Resilient:** This platform contributes to a more robustly decentralized Web3, enhancing censorship resistance.

## Toward Fully Decentralized and Verifiable Web3 Application

With this protocol, we can move toward fully decentralized and verifiable Web3 applications.

**Decentralized and Verifiable Blockchain Explorer:** Currently, blockchain explorers like Etherscan are hosted by centralized entities, and the results they present are not verifiable. If such an explorer were hacked, it could display malicious and misleading information, such as fake transactions or contracts, potentially leading to phishing scams. By migrating the entire blockchain explorer—including both the frontend and backend services—to our platform, we can ensure full verifiability and robust security for the blockchain explorer.

**Decentralized, Verifiable, Faster, and Cheaper AI Platform:** This protocol enables the creation of a fully decentralized, verifiable, and cost-effective AI platform. By moving the entire stack, including both frontend and backend services as well as AI computation, to a decentralized cloud, we can build an AI platform that is not only more affordable but also potentially faster than centralized alternatives.

**Decentralized Cloud Gaming:** Some games require high-end hardware, such as powerful GPUs and CPUs, leading game companies to move their games to cloud services, reducing the hardware requirements for customers. We can similarly bring Web3 games to our platform. Since our platform is verifiable on Ethereum, game reward settlements can be easily managed through smart contracts.

## Further Discussion

### Updating the State

In the previous discussion, the service program operates under a stateless design, meaning it does not modify its internal state. However, the data source used by the service program is upgradable. For instance, if a service program uses Ethereum as its data source, users can interact with smart contracts on Ethereum to update the state. The service program can then utilize the latest Ethereum state as its data source, enabling the implementation of a decentralized explorer.

If updating the internal state of the service program is required, a state machine replication network must be established among the service providers. In this case, each service program would correspond to a layer 2 or layer 3 blockchain on Ethereum. When users invoke a method that updates the internal state, they would send the transaction to the corresponding layer 2 or layer 3 blockchain. The service providers would then reach a consensus on the execution results of that transaction and update the internal state accordingly. Periodically, the layer 2 blockchain would roll up the transactions and its latest state back to Ethereum.

### Verifiable FHE

To ensure user privacy, Fully Homomorphic Encryption (FHE) can be integrated into our protocol. In this case, the FHE computation would be incorporated into the service program. Instead of sending plaintext data to the service providers, users would encrypt their input and send only the ciphertext, thereby preserving their privacy. Additionally, if on-chain arbitration is triggered, the FHE service program would be compiled into machine-independent instructions, and a fraud proof or zk-proof would be generated to make the FHE computation fully verifiable.

## Related Work and Comparison

**Comparison with Web3URL**

Web3URL (https://w3url.w3eth.io/) is an interesting project that transforms Ethereum into an unstoppable decentralized web server. Our protocol can be seen as a significant extension of Web3URL. In Web3URL, service functions must be written within smart contracts, which naturally limits large-scale applications. In contrast, our protocol supports complex service programs, such as AI computations, and provides flexible access to large-scale data, making decentralized ChatGPT and decentralized explorers a reality.

**Comparison with ICP**

The Internet Computer (ICP: https://internetcomputer.org/) hosts decentralized serverless compute, similar to our goal of creating a decentralized cloud service platform. However, we differ from ICP in several key aspects:

- Ethereum Integration: We are building on Ethereum, allowing us to inherit its security features.
- Higher Security: We achieve a higher level of security compared to ICP. While ICP operates in a Byzantine Fault Tolerance (BFT) network under a majority trust assumption—requiring that most nodes in the subnet are honest—we adopt an approach similar to rollups, with on-chain arbitration ultimately reverting to Ethereum. This allows us to guarantee correctness under a minority trust assumption, where just one honest node can ensure the integrity of our protocol.
- Complex Computation: Following the design principle of “Separate Execution from Proving,” we can handle complex computations natively, such as LLM inference or even fine-tuning. In contrast, service programs in ICP always run within canisters, which significantly limits their applicability for large-scale computations.

If you are interested in this project or have suggestions for improvements, please feel free to reach out to me.

## Replies

**xhyumiracle** (2024-08-30):

To be honest I’m really exciting to read this because it exactly matches with I was thinking about in the past months.

It tries to build a practical Decentralized Cloud Service protocol, which is exactly what Web3 was talking about since day1.

Although many predecessors have tried on this direction, most of them lack the most important component: verifiability. With no verifiability, then it’s a **distributed** protocol rather than **decentralized**, it makes a significant difference here.

I’d like to comment on the following 4 aspects:

1. thoughts on what makes it cost-effective and scalable:
 The underlying reason comes from Non-replicated work, i.e. the number of nodes solving the same task is independent to the network size. New joined nodes will contribute most to network capacity, by solving new tasks, and less to consensus enhancement, by replaying existing tasks.
 Consensus roots in replicated work, Scalability roots in Non-replicated work.
 Since it doesn’t need to maintain a universal ledger, the network consensus cost is saved and transformed to the scalability capacity.
2. Updating the State:
 I agree that to build a stateful computation layer based on Ethereum, it may ultimately require a layer2 or layerN to reduce the storage cost.
 I’d like to add that, probably what we need to manage the state is a DA layer in general, which doesn’t have to be coupled with the computation layer, i.e. the Decentralized Cloud Service network in this scenario. Correct me if I misunderstood it.
 Just like the post mentioned, we can store the program files to a DA layer, the state can be managed in the same way, the only thing left is to prove that data io is correct (we’ve seen some solutions in zk oracles).
3. Onchain Arbitration
 This is the most important design that distinguishes from other solutions from my perspective.
It uses Ethereum as the consensus layer to build verifiability, which is critical for decentralization.
 Challenge-based verification protocol is a practical design for web3, it’s an on-demand verification protocol that gives the choice back to the users over the tradeoff between security and cost. In other words, it is decoupled from and can work with different types of verification protocols like ZK, TEE, Fraud Proof, as the post mentioned.
4. Task Dependency
 As another future discussion item following the stateful computation design, we may consider the situation where tasks have dependencies. If we manage to organize tasks into parallel-able partitions, we may enable the slicing of large tasks into smaller ones and remain the efficiency. In this way, we may achieve a promising decentralized training solution, or as the post mentioned, decentralized gaming etc.

With these comments added, the Decentralized and Verifiable Cloud Service can be viewed as a Scalable Decentralized Computation Network (CPN) layer, aims to handle complex Turing-complete computation tasks. It can work with a DA network as a Storage Network (STN) layer, and use Ethereum as the Consensus Network (CSN), i.e. the finalization Layer. In this sense, it shares the same vision with the [World Supercomputer](https://ethresear.ch/t/towards-world-supercomputer/15487/7) architecture. The service provider in this Decentralized Cloud Service protocol is like a Decentralized Processing Unit (DPU) in the World Supercomputer.

Anyway, it doesn’t matter how we describe it, the core idea behind is what we believed in that will pave the way towards the mass adoption. Thank you for sharing it out.

---

**0x1cc** (2024-08-30):

Thank you for your interest! With this protocol, we are moving toward the fully decentralized, verifiable, and censorship-resistant Web3.

Regarding cost efficiency, it is comparable to the current centralized cloud service providers, such as AWS. Currently, the decentralized GPU can be up to 90% cheaper than centralized service providers. For the serverless computing design, it can be even more cost-effective, allowing edge devices like mobile phones to participate as service providers.

For state updates, we are adopting a design that separates execution from storage. The state can be stored in any DA, while only the state root and the transactions that would update the state are managed in the L2/L3 ledgers. Additionally, we can delete older transactions once the related state root is confirmed. This approach effectively prevents the issue of state growth.

Regarding arbitration, you are correct that this is one of the most critical aspects of our protocol, distinguishing it from other projects, as it is fully verifiable on Ethereum.

As for task dependencies, by separating execution and storage, it becomes easier to determine state dependencies, enabling parallel processing to be more feasible.

Let’s join forces to advance towards a fully decentralized, verifiable, and censorship-resistant end-to-end Web3 ecosystem and build a real world supercomputer!

---

**r4f4ss** (2024-09-08):

Thanks for this idea, I have been thinking recently about how important is to have decentralized services like GitHub, since a centralized and trust-based one is susceptible to censure.

My concern is about many providers executing the same service and inconsistency prevention. Having many providers tends to be expensive and in the case one or more have different results, an arbitration is raised and all providers must re-run the service twice, which tends to be even more expensive. Keep in mind that the user can not know in advance which server is dishonest since is not always possible to execute a chatGPT locally. It may be possible to attack the network submitting several incorrect service results.

I believe this post idea can benefit from the use of [Proof of Computation](https://crypto.stackexchange.com/questions/100957/is-there-anything-like-proof-of-computation), although I do not know how to fit it into this idea. In short, a single server can provide a service (maybe more if parallelism is demanded) and the user can be sure the computations are correct based on some ZK primitive.

---

**0x1cc** (2024-09-13):

Thank you for your interest. Since providing incorrect results will be discovered and result in punishment, a rational service provider would not be motivated to do so. (This can be analyzed using a game-theoretical approach.) Therefore, in most cases, re-running the service is not necessary, assuming the service provider is honest.

Regarding the number of service providers needed for each request, this can vary based on the user’s requirements. It is indeed a trade-off between security and cost. If a user desires greater security for their service, they might opt for multiple service providers. However, for services such as AI, like ChatGPT, high security may not be as critical. Typically, a user could request just one service provider, and only seek an additional one if they suspect potential malice. A random check mechanism could also be implemented; for instance, a user might request an additional service provider with a 10% probability. This approach can further reduce costs.

As for computational proofs like zk-SNARKs, generating a zero-knowledge proof is extremely resource-intensive, making it impractical for high-performance and computationally demanding services such as AI. This is why, in this discussion, I explore an alternative approach, akin to an optimistic one. On-chain arbitration would only be necessary if a malicious service provider is detected.

---

**qizhou** (2024-09-16):

There is a git3 project (https://git3.sh/) that aims to provide a censorship-resistant github based on blockchain technologies.  I think from technologies-wise, it becomes possible with:

- A low-cost L2 to maintain the relationship of diffs;
- A provable off-chain storage for the actual diffs, where the proof of storage is verified on a contract on L2 (and then distribute storage incentive accordingly, e.g., what EthStorage is doing)
- A decentralized access protocol for frontends.  web3:// defined in ERC-4804 aims to solve this by turning EVM into an HTTP server.

One value may be that for censored projects like Tornado Cash, we can now use blockchain to bypass the attack and maintain its github repo (rather than read-only github mode now). In the future, we may even be able to develop Ethereum (e.g., Go-ethereum repo) on top of Ethereum L2/L3 networks.

---

**0x1cc** (2024-10-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> There is a git3 project (https://git3.sh/ ) that aims to provide a censorship-resistant github based on blockchain technologies.

Cool! We can utilize git3 to maintain the service program within this proposed protocol. Besides, by integrating with the protocol, we can introduce “GitHub Actions” capabilities to git3, enabling users to execute scripts directly within the git repository. It is even possible to achieve full automation for a blockchain upgrade combining git3 and the “Git Actions” functionality.

---

**0x1cc** (2024-10-16):

[@cypherpepe](/u/cypherpepe)

Since most interactions occur off-chain, potential network bottlenecks are likely to happen off-chain as well, similar to scenarios in Web2, rather than causing on-chain congestion. The provider selection issue resembles typical workload balancing problems in cloud scheduling. To enhance user experience, we can design a decentralized scheduling mechanism to effectively manage this process.


---
source: ethresearch
topic_id: 20255
title: "Proof of Service Integrity (PoSI): Trustless measurement of service integrity"
author: peshwar9
date: "2024-08-11"
category: Security
tags: []
url: https://ethresear.ch/t/proof-of-service-integrity-posi-trustless-measurement-of-service-integrity/20255
views: 401
likes: 2
posts_count: 1
---

# Proof of Service Integrity (PoSI): Trustless measurement of service integrity

# Proof of Service integrity (PoSI) : Trustless measurement of service integrity

## TL;Dr

**Proof of Service Integrity (PoSI)** is a byzantine fault tolerant verification protocol for offchain activities.

It performs three main tasks in a decentralised fashion - *deployment* of approved service images, *measurements* of deployed services, and *attestation* of the integrity of these services in production.

The problem PoSI solves is that offchain services are growing in volume, size and complexity in modern chain architectures, but they are largely centralised and run in trusted environments while handling millions of dollars of transaction flows. This is incompatible with the goals of crypto systems. Permissionless verification of offchain services using PoSI protocol provides a real-time integrated security view for emerging hybrid crypto protocols that have a mix of on-chain and off-chain activities.

Offchain services that are verified by PoSI protocol are called **Integrity Verified services** (IVS).

## Preface

This post builds on the earlier proposal on integrity proofs ([Integrity proofs to improve rollup security](https://ethresear.ch/t/integrity-proofs-to-improve-rollup-security/19437)) with the following main differences:

1. Focus on measuring integrity of any off-chain service, rather than just rollup services
2. Earlier design was TEE-based, current protocol is primarily BFT-based but uses TEEs as a defense-in-depth mechanism.
3. Changes to the architecture

## Prelude

Traditional distributed systems monitoring/observability involves collecting and analyzing data in order to gain insights into the functioning, performance, security and health of software systems and applications. It involves systematically observing and tracking various metrics, events, logs and distributed traces to construct a visual representation of a system’s hardware and software performance and health. While there are multiple types of distributed systems monitoring data, one  dimension in particular that is not measured in traditional web2 distributed systems is service integrity.

For this post, let’s define *service integrity* as the following:

1. The correct (authorised and verified) software version has been deployed
2. No unauthorised changes have been made to the deployed software in production.
3. Anyone can permissionlessly verify proof of #1 and #2 for any given service either through data provided over a user interface or API, or through verification of a zero-knowledge proof.

In internet/online systems (web2), *services integrity* (particularly #1 and #2) is the responsibility of the organisation or entity that centrally owns and manages the distributed service, *aka trusted deployments*. As a consequence, #3 is simply not possible.

When we talk about web3 systems, *service integrity* becomes paramount. Services are deployed in *untrusted environments* managed by operators that we do not know or have legal contracts with.

The way this problem has been solved in blockchain-based systems (Proof-of-stake in particular) is through a carefully designed set of incentives to encourage external operators to run the distributed software with desired behaviours, coupled with a clever mechanism for the distributed network to reach a consensus such that if an operator that is part of the consensus set is detected to perform any malicious action, they can be financially penalised (through onchain mechanisms or social governance).

This worked reasonably in the early days of evolution of onchain systems where all the logic for onchain protocols were on smart contracts on a single chain, which was invoked from offchain clients. Censorship resistance was largely handled by allowing anyone to run the Json-RPC nodes (which are the user transaction entry points) that communicate with the other distributed network nodes over P2P protocols. This ensured eventual censorship-resistance.

## Evolution of crypto protocol architectures

Recent developments in blockchain systems have seen an explosion in the number of layer-1 and layer-2 chains, and the rise of modular architectures with innovations in application protocols, core infrastructure, scaling and interop solutions, developer & user tools. These innovations are aimed at solving problems with scaling throughput, reducing latency, lowering transaction costs, offering greater sovereignty to builders over design choices, solving for both synchronous and async interoperability, unifying liquidity, mev optimisation, and improving user experience in crypto.

These developments have resulted in increased complexity and sophistication of onchain protocols involving a mix of smart-contract logic and offchain logic. Emerging use cases such as cross-chain swaps involve a mix of smart contract and offchain logic on both the source and destination chains.

Let’s look at a few of the hybrid onchain-offchain architectures in popular crypto protocols.

[![Fig 1: Hybrid onchain-offchain design in crypto protocols](https://ethresear.ch/uploads/default/optimized/3X/4/9/491a30b1c361107e65615618ea2b29c226245e4d_2_690x474.jpeg)Fig 1: Hybrid onchain-offchain design in crypto protocols1920×1320 104 KB](https://ethresear.ch/uploads/default/491a30b1c361107e65615618ea2b29c226245e4d)

Fig A shows onchain logic on a single chain encoded as smart contracts. The onchain logic is accessed from a regular web or mobile client application through RPC calls.

Fig B shows an example of crypto protocol containing a mix of onchain smart contract logic on a single chain and offchain component attached to it. The offchain component typically either supplies data from an online system (eg price feeds through oracle) or performs compute-heavy operations on behalf of the smart contract (eg co-processor). The offchain component can also be a regular web backend of the dapp, if the app developer chooses to keep a portion of the business logic offchain (which is not uncommon in most modern dapps).

Fig C shows an example of a cross-chain transaction that involves two chains - source and destination chain (e.g., cross-chain swaps or bridging). Here, smart contract logic is present on both the chains, and there are corresponding offchain components.

> The main challenge that is being addressed in this post is that a big proportion of the off-chain components that are part of these hybrid onchain-offchain crypto protocols are run in trusted environments. This is incompatible with the main goals of crypto protocols which are trustlessness, censorship resistance and permission-less participation and verifiability.

While the onchain components (aka smart contracts) are secured by consensus, economic incentives and permissionless verification, the same cannot be said about offchain services whose actions cannot be attributed onchain.  These services are, in most cases, centralised,  owned and run by trusted entities, but play critical role in the overall transaction workflows. They are vulnerable to censorship, tampering and other kinds of attacks. Note that only the on-chain logic of the crypto protocols is secured by the blockchain consensus, not the supporting off-chain infrastructure and services which have varying levels of trust assumptions. In some cases, it is not even possible to detect malicious actions performed by such offchain components *(non-attributable faults)*.

Figure 2 shows a non-exhaustive list of popular categories of offchain services that are an integral part of many crypto protocols.

[![Fig 2: Common categories of off-chain services](https://ethresear.ch/uploads/default/optimized/3X/4/b/4b764f4c7ce39d7b0d4769c441ff37392c08d505_2_690x350.png)Fig 2: Common categories of off-chain services2924×1484 297 KB](https://ethresear.ch/uploads/default/4b764f4c7ce39d7b0d4769c441ff37392c08d505)

What are the types of risks to crypto protocols with such centralised offchain services?

*Insider Threats*: Employees or contractors within the service development team or the cloud platform provider may misuse their privileged access.

*Unauthorized Modifications*: Malicious actors might attempt to alter the service code logic or configuration without detection, leading to unintended consequences inconsistent with the protocol goals.

*Censorship Risks*: In case of offchain services, bad actors might attempt to censor certain transactions or user interactions.

*Data and Fund Security*: There’s a risk of unauthorized access to sensitive data or funds managed by the service. e.g. a dapp backend managing an embedded wallet may view/steal user wallet keys.

## We need a decentralised verification protocol

Hence, a critical requirement for the success of these modular hybrid onchain-offchain architectures is the ability to prove offchain service integrity at scale in a decentralised trustless manner, i.e. a *Byzantine fault tolerant service integrity verification system*.

In this post, we present *Proof of Service Integrity* (**PoSI**), a verification protocol that performs three main tasks - *deployment of publicly-identifiable code images*, *measurement of the correctness  of code deployed periodically*, and  *attestation of service integrity* in the production environment. These correspond respectively to the properties of *correctness*, *integrity* and *verifiability* for the monitored services. Figure 3 shows the key desired properties and relationships between the PoSI nodes that are part of the verification network, and the monitored services.

[![Fig 3: Verification layer for off-chain services](https://ethresear.ch/uploads/default/optimized/3X/1/3/135c0d620ec8bd53705bf83f07fd11c3aff47d42_2_690x163.jpeg)Fig 3: Verification layer for off-chain services1920×454 71 KB](https://ethresear.ch/uploads/default/135c0d620ec8bd53705bf83f07fd11c3aff47d42)

The PoSI nodes that implement the verification protocol itself satisfy the following  properties: 1) *Trustless:* Service integrity measurements are secure against byzantine attacks by collaborations among the monitoring services and the monitored services. 2) *Tamper-proof*: The service monitoring service while verifying the tamper-resistance of the monitored services, is itself tamper-resistant  3) *Open*: The protocol allows anyone to register and provide measurement data , by using cryptographic primitives to ensure that a subset of actors cannot maliciously modify results in their favour.

A formal security model allows us to establish guarantees of accurate service measurements in the presence of malicious actors. The security guarantees of the PoSI protocol are composable with the onchain state commitments on blockchain ledgers to provide a comprehensive view of protocol security which is not possible by just focusing on smart-contract & consensus-based security.

[![Fig 4: Integrated view of security of crypto protocols with PoSI](https://ethresear.ch/uploads/default/optimized/3X/f/2/f2a8e22a3c90dfb18ded2bfa3c371ef147452247_2_690x201.png)Fig 4: Integrated view of security of crypto protocols with PoSI3296×962 284 KB](https://ethresear.ch/uploads/default/f2a8e22a3c90dfb18ded2bfa3c371ef147452247)

## Proof of Service Integrity (PoSI) protocol overview

PoSI enables verifiable service integrity through the following:

*Authenticated Deployment*: PoSI ensures that only authorized and verified code is deployed to the production environment. This prevents the introduction of malicious or unauthorized code during the deployment process.

*Continuous Integrity Monitoring*: Once deployed, PoSI nodes continuously monitor the service to detect any unauthorized modifications or tampering. Any discrepancies between the running service and its expected state are immediately detected and reported.

*Integrity Attestation*: Users or dApps can request integrity proofs for any PoSI-enabled service through a permissionless, public interface. Two types of integrity checks can be done on a given service - *measurements-based* and *proof-based*. *Measurements-based* checks involve deriving service integrity from the onchain measurements for the service. *Proof-based* checks can be done by requesting a SNARK proof of integrity  for the service, which can then be verified either on-chain (SNARK verification) or off-chain (in a web or mobile app).

Services that are verified by PoSI protocol are called *Integrity-verified services* (IVS).

## Architecture workflows

PoSI protocol involves the following three workflows:

1. Service developer workflow
2. Operator workflow
3. Verification workflow

Figure 5 shows an overview of the key actors and actions in the protocol.

[![Fig 5: Overview of PoSI protocol](https://ethresear.ch/uploads/default/optimized/3X/9/2/929487f88493ab7c774f428b5bed736328ff9f72_2_690x268.jpeg)Fig 5: Overview of PoSI protocol1920×746 53.3 KB](https://ethresear.ch/uploads/default/929487f88493ab7c774f428b5bed736328ff9f72)

The architecture of PoSI involves the following components and actors:

**1. Human/Organisational actors:**

*Service developer*: This refers to the developer and owner of the distributed software service. The service developer is the main ‘customer’ for the integrity-verified service, and is the person or entity that is ready to pay a fee to have their service integrity-verified.

*Operator:* This refers to the provider of the computational infrastructure. The service developer can themselves choose to be the operator by deploying the IVS on a cloud account controlled by them or they can choose to deploy their service on an external operator’s VM through a DePIN service.

**2. PoSI Platform:**

*PoSI platform onchain:* This contains the core smart contracts of the  protocol.

*PoSI Offchain*: This comprises core offchain services that are part of the protocol.

**3. Applications/ Other chains:**

*Application*:  A web or mobile application that verifies the proof for an IVS.

*Other chain:* Any other chain can verify the zk proofs generated by the PoSI protocol.

### Service developer workflow

1. Service developer builds the service and registers the service image in a public repository.
2. Service developer registers the service image along with other service metadata with the PoSI onchain smart contracts. They also deposit rewards amount, along with service level expectations (e.g. frequency of measurements).
3. Service developer can trigger the PoSI smart contract to trigger the service deployment either on their self-hosted VM, their cloud VM or on a DePIN VM.
4. The PoSI protocol pays out the rewards to the operators based on the tasks performed by them, from the service developer’s account.

### Operator workflow

1. Operator registers their VM with the PoSI registration service. The operator can choose to perform two kinds of tasks - host service images, or host the PoSI host program that performs measurements on other services. For the former, any regular VM of the configuration required by service developers would be accepted. For the latter, TEE-based VMs will be required.
2. Note that service developer can choose to deploy their service on their own VM, in which case they need to register it like other external operators. For TEE-based VMs, the quote has to be generated by the operator and submitted to the registration service along with in-enclave generated public key.
3. Operator stakes the minimum specified tokens as part of registration. If the service developer hosts the service on their own VM, this step is not required.
4. The PoSI registration service verifies the registered VM and registers it with the PoSI onchain contract. The PoSi registration service itself runs within a TEE enclave.
5. When the service developer triggers deployment of a service, the PoSI host program retrieves the registered service image from public repository and deploys the service on the service developer (or external operator’s VM based on the configuration).
6. If an operator has registered to host the PoSI protocol, the PoSI master  deploys the PoSI host program on the operator’s VM. This enables the operator to then perform service measurements on other services.
7. Based on the specification of the service developer, the operator set is established for verifying that service, which runs the consensus mechanism to determine the final service measurements. The votes of all  operators in the operator set are aggregated and recorded onchain, along with the measurements.
8. At periodic intervals, measurements of the performance of the verious operators are taken by the PoSI measurement service, and rewards are computed for the operators. Any incorrect measurements attributable to any of the operators in operator set is penalized through slashing of their stake, in a manner defined in the PoSI protocol.

### Verification workflow

1. Any web or mobile application can ask the PoSI protocol servers for attestation of any particular service. The PoSI protocol returns the proof to the web/mobile application.
2. Two kinds of proofs can be requested from the PoSI protocol for a service: state proofs and SNARK-proofs. State proofs simple return the onchain state of a service computed from the measurements submitted by operators. SNARK proofs that are returned by the PoSI protocol can be verified either off-chain within the web/mobile application, or submitted to another on-chain smart contract for verification.

An integrated view of the various workflows for the PoSI protocol is shown in figure.

[![Fig 6: Integrated view of PoSI workflows](https://ethresear.ch/uploads/default/optimized/3X/3/2/32045a0a10edcc50ab33324a649080621d79a8ac_2_690x309.jpeg)Fig 6: Integrated view of PoSI workflows1920×860 114 KB](https://ethresear.ch/uploads/default/32045a0a10edcc50ab33324a649080621d79a8ac)

Note: Figure 6 shows only a single host program taking the service measurements (for reducing clutter in diagram), but it can be visualised as a set of nodes that participate and arrive at a consensus before posting the measurements on-chain.

## Conclusion

Trustfree measurement of offchain service integrity is an unsolved problem in decentralised networks. **Proof of Service Integrity (PoSI)** addresses this core requirement by providing a secure, byzantine resistant verification layer for offchain services while allowing open participation for operators and service developers to benefit from the protocol. All components of the protocol can be operated by community-run protocol nodes controlled by the onchain protocol smart contracts. PoSI incorporates a layered security model that includes *consensus-based*, *hardware-based* and *crypto-economic security*. PoSI requires the participating offchain services to have open source code, a publicly verifiable service image, reproducible build process and dockerized deployment.

## FAQ

### What kind of services can benefit from the PoSI protocol?

Any in-protocol or out-of-protocol offchain service can benefit from PoSI protocol. A non-exhaustive list of offchain services was mentioned earlier in the post, and is reproduced here:

[![Fig 7: Popular categories of off-chain services](https://ethresear.ch/uploads/default/optimized/3X/4/b/4b764f4c7ce39d7b0d4769c441ff37392c08d505_2_690x350.png)Fig 7: Popular categories of off-chain services2924×1484 297 KB](https://ethresear.ch/uploads/default/4b764f4c7ce39d7b0d4769c441ff37392c08d505)

### What are the alternative architectures available to secure offchain services?

For offchain services to transition from *trusted* to *trust-minimised* / *trustless* architectures, here is a comparison of the various design approaches.

| Design approach | Description | Pros | Cons | Security model |
| --- | --- | --- | --- | --- |
| Consensus-based | Build a BFT-consensus with own operator set | Trustless | It is expensive and cumbersome for a service developer | Depends on size of the operator set |
| ZK-based | Build a custom zk circuit or a program that can be proven in a general purpose zkVM | Trustless | Involves rewrite of the service using zk DSLs or using Rust. Expensive to generate zk-proofs | Restricted to what can be proven in zk circuits |
| EigenLayer AVS-based | Convert the service into Eigenlayer AVS | Inherit Ethereum security without bootstrapping an operator set | Requires rewrite of the code to comply with AVS protocol. Also AVS can only detect and penalise operator faults if they are observable on-chain. | Economic security |
| PoSI IVS-based | Deploy existing code in docker containers with no code rewrite. | Ability to detect non-attributable faults (those that are not normally visible on-chain such as censorship, or unauthorized upgrades of service algorithms). Small, configurable cost. | Services should meet pre-requisites: open-source code, a publicly verifiable service image, a reproducible build process and dockerized deployment | Multi-layered security model incorporating consensus-based, TEE, and crypto-economic security constructs. |

## Credits

The concept and design for PoSI protocol and Integrity-verified services was initially developed as a collaboration between [@peshwar9](/u/peshwar9) and [@mohsinriaz17](/u/mohsinriaz17) with contribution from several others to refine and enhance it.

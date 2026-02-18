---
source: ethresearch
topic_id: 21717
title: The Road Towards a Distributed Encrypted Mempool on Ethereum
author: and882
date: "2025-02-11"
category: Uncategorized
tags: [mev, proposal-commitment]
url: https://ethresear.ch/t/the-road-towards-a-distributed-encrypted-mempool-on-ethereum/21717
views: 3358
likes: 11
posts_count: 1
---

# The Road Towards a Distributed Encrypted Mempool on Ethereum

# The Road Towards a Distributed Encrypted Mempool on Ethereum

by Frederik Lührs, Luis Bezzenberger, Francesco Mosterts, Sebastian Faust, Andreas Erwig

*Many thanks to Julian Ma, Drew Van der Werff, Alex Vinyas, Martin Köppelmann, Marc Harvey-Hill, Phillippe Schommers, and Julie Bettens for their valuable feedback on this document and/or prior collaboration on threshold encrypted mempools*.

A full version of this post can be found [here](https://docs.shutter.network/docs/shutter/research/the_road_towards_an_encrypted_mempool_on_ethereum).

Ethereum’s promise of decentralization, fairness, and security is challenged by issues like censorship, front-running, and builder centralization, making the case for encrypted mempools stronger than ever.

**Who We Are:**

We are a group of projects and individuals building on Ethereum since 2014, dedicated to advancing the network’s privacy, decentralization, and fairness. Our contributors include the Shutter Network, Gnosis, MEV Blocker, Nethermind, Chainbound, and more.

This post first touches on the general goals, challenges and end vision for transaction encryption and then outlines a practical roadmap for implementing a **threshold encrypted mempool** using **proposer commitments** to integrate with Ethereum’s **PBS transaction supply chain**. It explores how this approach could improve censorship resistance, mitigate malicious MEV, and ensure a fair transaction process.

This is not a definitive plan but a starting point for conversation. We invite feedback and contributions from all perspectives, particularly from those involved in the PBS supply chain, including RPC providers, relays, builders, and proposers.

Additionally, we’re planning to design this integration as modularly as possible, leading to a **generalized mempool encryption interface**, which is as encryption technology agnostic as possible.

[![](https://ethresear.ch/uploads/default/optimized/3X/3/4/34b719f1f7cedda68a0184497ce79d6888508e7d_2_690x388.png)886×499 131 KB](https://ethresear.ch/uploads/default/34b719f1f7cedda68a0184497ce79d6888508e7d)

## Problem

Ethereum faces challenges like censorship, front-running, and builder centralization, which undermine its decentralization and fairness guarantees. While Proposer-Builder Separation (PBS) was introduced to [preserve the decentralization of the validator set](https://barnabe.substack.com/p/pbs), builder centralization still persists. In his recent blog post series “[Possible futures of the Ethereum protocol](https://vitalik.eth.limo/general/2024/10/20/futures3.html)”, Vitalik emphasizes that to address the issue of builder centralization, we need to give transaction selection back to proposers (validators). In order to do so, it is crucial to have encrypted mempools, where transactions are broadcast in encrypted form such that block builders cannot see the details and thus cannot front-run or censor them. Encrypted transactions are decrypted only once their position in the block is fixed. However, implementing encrypted mempools introduces challenges such as enforcing timely decryption, navigating trust assumptions in enabling technologies, integrating with PBS, managing acceptable MEV like back-running, and ensuring verifiability and accountability to detect and penalize misbehavior.

# The Endgame of Encryption: A Fully Private and Decentralized Ethereum

The ultimate aim is a fully encrypted and decentralized Ethereum where all transactions are private yet verifiable. In this envisioned system, advanced cryptographic techniques like Fully Homomorphic Encryption (FHE), Multi-Party Computation (MPC), indistinguishability Obfuscation (iO), and Zero-Knowledge Proofs (ZK) can enable verifiable computation on encrypted data without revealing any sensitive information, thereby reducing attack surfaces. Achieving this vision would revolutionize the way public blockchains do transaction processing, providing unparalleled information symmetry, security and privacy. While technologies like FHE and iO aren’t yet practical for widespread use due to computational challenges, ongoing research is rapidly advancing. In the meantime, **implementing a threshold encrypted mempool via proposer commitments** can serve as a stepping stone toward this ultimate goal.

# Technologies Enabling the Encrypted Mempool

Several approaches have been proposed and are currently being explored to enable encrypted mempools, including timed cryptography in the style of Verifiable Delay Functions (VDFs), FHE, Trusted Execution Environments (TEEs), Witness Encryption, and Threshold Encryption. Unfortunately, all of these technologies have their limitations: Timed cryptography requires a significant amount of wasteful computation and comes with timing issues; FHE and witness encryption, while powerful primitives, are not yet practical for many real-world use cases (e.g., the Flashbots team investigated the efficiency of FHE for capturing backrunning MEV in a [recent blog post](https://writings.flashbots.net/blind-arbitrage-fhe), which illustrates nicely the extreme computational constraints that FHE imposes); TEEs are vulnerable to side-channel attacks and crucially require to trust the hardware manufacturer; and threshold encryption relies on the threshold trust assumption, requiring that fewer than a specified number of parties act maliciously.

Among the above technologies, threshold encryption stands out as the most viable candidate for implementing an encrypted mempool in the near- to mid-term. It allows for efficient decryption while offering robust security and liveness guarantees. Threshold encryption works by distributing the decryption key of a public key encryption scheme among multiple parties, such that collaboration of a minimum threshold of parties is required to decrypt a message. This approach ensures that as long as fewer than the threshold number of parties are compromised, the plaintext and decryption key remain secure.

# Shutter High Level

Shutter allows to encrypt transactions so that their contents are hidden until block proposers or sequencers commit to an order and inclusion. This is achieved through a threshold encryption scheme, ensuring that no single party can decrypt or manipulate transactions prematurely. The process is as follows:

- Encryption: Users encrypt their transactions using a public encryption key generated collaboratively by a group of nodes (Keypers) through a Distributed Key Generation (DKG) protocol.
- Commitment: Block producers include these encrypted transactions in blocks, committing to their inclusion and order without access to their contents.
- Decryption: Once transactions are included in the chain, the Keypers release the decryption key, enabling execution without exposing the data to potential front-running.

### The Shutterized Beacon Chain

In 2022, [we proposed integrating their threshold encryption scheme directly into Ethereum’s consensus layer](https://ethresear.ch/t/shutterized-beacon-chain/12249) to combat MEV and front-running. At that time, Ethereum lacked mechanisms like Proposer-Builder Separation (PBS). Since then we implemented [the Shutterized Beacon Chain on the Gnosis Chain](https://www.gnosis.io/blog/welcome-to-the-future-shutterized-gnosis-chain-has-become-a-blueprint-for-base-layer-neutrality), operating as an Ethereum-like beacon chain in an out-of-protocol version. Collaborating with Nethermind, the team successfully integrated threshold encryption into the chain’s operations. A substantial percentage of validators are participating and an alpha Keyper set comprised of 7 Keypers is securely managing encryption keys. The network has processed many shielded transactions, demonstrating the practicality and effectiveness of the approach. The [Shutter Explorer](https://explorer.shutter.network/) allows users and developers to monitor the live implementation, offering transparency without compromising security.

[![](https://ethresear.ch/uploads/default/optimized/3X/f/e/fed003a16e2bae8146353f6f4e4843b11a012609_2_690x284.png)927×382 68.9 KB](https://ethresear.ch/uploads/default/fed003a16e2bae8146353f6f4e4843b11a012609)

The implementation provided valuable insights into practical challenges, such as Keyper selection and decentralization.

Additionally, we built an [encrypted mempool module for OPStack chains and deployed this as a testnet](https://blog.shutter.network/shutterized-op-stack-testnet-shop-now-live-on-sepolia/), further proving the viability of threshold encrypted mempools for various sequencing environments.

The successful implementation on the Gnosis Chain as well as the shutterized OPStack testnet demonstrate the feasibility of this approach and provides a blueprint for potential adoption on Ethereum’s mainnet. Enter our plan and roadmap to do just that:

## New Practical Plan: Threshold Encrypted Mempool for Ethereum L1 Using Proposer Commitments

Proposer commitments enhance trust in Ethereum’s block production by enabling proposers to pre-commit to including specific transactions into the next block, holding proposers accountable to their commitments. While originally developed for pre-confirmations, proposer commitments are an essential tool to enable encrypted mempools. [Commit-Boost](https://github.com/Commit-Boost) formalizes this with cryptographic proofs and protocol enforcement, ensuring transparency and fairness in block building.

At a high level, the transaction flow in an encrypted mempool using proposer commitments is as follows:

1. A user submits an encrypted transaction.
2. The proposer commits to including it at the top of the block.
3. The Shutter Network or similar reveals the decryption key, enabling transaction inclusion in the block.

The commitment guarantees that the proposer will include the decrypted transaction at the top of the block or else the proposer is held accountable for not following its commitment. The latter case is enforced via new out-of-protocol slashing conditions backed by restaked collateral. However, challenges remain with this approach, including delays caused by commitments and decryption, and distinguishing network failures from deliberate misconduct by proposers.

# Roadmap

We worked out a concrete roadmap towards an encrypted mempool on Ethereum L1 using proposer commitments. As a first step, this solution is out-of-protocol, acknowledging the fact that the implementation of an in-protocol solution is a lengthy process. However, the eventual goal for Ethereum should be an in-protocol solution. Therefore, the final step of our roadmap drafts a potential solution for an in-protocol encrypted mempool. In the following, we will outline the steps of our roadmap at a high level, whereas a detailed description can be found [here](https://docs.shutter.network/docs/shutter/research/the_road_towards_an_encrypted_mempool_on_ethereum).

**Out-of-protocol solution**

- Step 1 - Integration into RPCs: The goal of this first step is to introduce foundational support for encrypted transaction sending while maintaining compatibility with existing wallets and applications. To this end, we introduce a new RPC method, eth_sendEncryptedTransaction, and integrate it into existing RPCs like MEV Blocker to allow for basic encrypted transaction handling.
- (Optional) Step 2 - Integration into Relays: This step integrates encrypted transaction handling a bit further down the transaction supply chain than the previous step, namely into Relays. Essentially, Relays receive blocks from Builders as before, but append encrypted transactions to the block. The transactions are then decrypted by the Shutter Network.
- Step 2 - Proposer Commitments + Restaking: The goal of this step is to integrate encrypted transactions into a proposer commitment model that is ideally compatible with Commit-Boost. The solution leverages the Shutter Network’s threshold encryption scheme and the Bolt protocol to ensure private transactions are included securely and transparently at the top of the block. The Bolt protocol strives to be Ethereum’s leading proposer commitment protocol, enabling proposers to sign commitments (e.g., messages or transactions) and establish them as constraints for outsourced block construction.
We would like to note that the architecture of this step avoids malicious MEV but allows to capture good MEV via backrunning. That is because once encrypted transactions are committed to and decrypted, they can still be backrun.

**In-protocol solution:**

- Step 3 - In-Protocol: This is the final step of our roadmap with the goal to integrate Shutter-style threshold encryption directly into the protocol. A subset of validators acts as a Keyper set, responsible for releasing decryption key shares.

In the following, we will provide further details on the in-protocol solution.

## In-Protocol Solution

**Who Will Make Up the Threshold Committee?**

In an in-protocol encrypted mempool, the threshold committee should be a subset of Ethereum validators, leveraging their existing roles and stakes in the network to enhance security. One approach to forming this committee involves using [silent threshold encryption](https://eprint.iacr.org/2024/263.pdf), which allows to deterministically compute the joint public key of the threshold committee from the individual public keys of validators without requiring any interaction. This enables dynamic and asynchronous selection of Keypers from the validator set, making the system more scalable and flexible.

However, silent threshold encryption doesn’t solve the problem of validator centralization where too many Keypers are controlled by a single entity or a small group. In order to mitigate this risk it is important to (1) introduce economic incentives and penalties, e.g., by requiring Keypers to stake collateral that can be slashed in case of misbehavior (see below “Further Improvements”) and (2) regularly rotate the Keyper set, selecting members randomly from the validator pool.

**Generalized In-Protocol Solution.** We also consider a more generalized approach that abstracts away the specific encryption mechanism. That is, the exact technology—whether threshold encryption, delay encryption, TEEs, or any other method—is not the focus as long as the chosen mechanism reliably outputs the decryption key in time to decrypt transactions. Essentially, we treat the encryption mechanism as a black box that accepts an input and produces the necessary decryption keys, allowing flexibility in implementation while maintaining the desired functionality.

# Considerations for the Out-Of Protocol Solution via Proposer Commitments

## Encrypting Locally

For end-to-end encryption to function effectively, encryption should occur directly on the user’s device. This ensures that transaction details are protected before they leave the user’s control.

Encryption can be implemented either:

- In the Wallet: Users encrypt their transactions within their wallet application before submission.
- In the Dapp: The frontend application encrypts transaction data before passing it to the wallet.

Existing Example: [Shutter Network’s Shop SDK](https://github.com/shutter-network/shop-sdk)

We’ve already developed a frontend SDK for our L2 implementation for the OPStack. The [Shop SDK](https://github.com/shutter-network/shop-sdk) simplifies the integration of encrypted transactions, showcasing how user-side encryption can be achieved efficiently. This serves as a blueprint for expanding encrypted transaction handling across other dapps and wallets.

**Challenges and Opportunities**

- Wallet and App Support: Adoption requires significant updates to wallet and dapp ecosystems to natively support encryption.
- User Experience: Seamless integration is critical to ensure that encryption doesn’t create friction for users.

## Impact on economics/MEV value flow

Validators play a crucial role in Ethereum’s block-building process, and their incentives must align with network and user needs. Committing to encrypted transactions offers distinct economic benefits:

**1. Direct Income Stream: Priority Fees**

Encrypted transactions bring an inherent economic value through priority fees. Users include these fees to incentivize validators to process their transactions promptly.

- Competitive Advantage: If a validator refuses to commit to encrypted transactions, they forgo this revenue. The next validator in line can capture this order flow, reducing the refusing validator’s overall earnings.
- Increased Adoption Pressure: As more users route their transactions through encrypted mempools, validators face increasing pressure to support encrypted transactions or risk falling behind in profitability.

**2. Indirect Income Stream: MEV Opportunities**

MEV (Maximal Extractable Value) arises when validators or searchers profit from transaction ordering, inclusion, or exclusion. Encrypted transactions maintain MEV opportunities, but with adjustments to the traditional flow.

- CEX-DEX Arbitrage: Many encrypted transactions are related to market activities. The time delay between transaction creation and inclusion often causes price shifts on centralized exchanges (CEXs) and decentralized exchanges (DEXs). Searchers can backrun these transactions, capturing arbitrage opportunities.
- Profit Sharing: Searchers typically share profits with users and builders. In a system with encrypted mempools, committee members (responsible for revealing decryption keys) could enforce profit-sharing agreements, potentially involving other stakeholders.

**3. Alignment with User Preferences**

The ultimate decision-making power lies with users, who dictate the flow of transactions.

- Existing Models: Systems like MEV Blocker already protect users by obfuscating transaction details during submission and sharing MEV profits with them. Encrypted transactions extend this model by ensuring user privacy and enabling broader profit-sharing mechanisms.
- Validator Pressure: Validators who refuse to support encrypted transactions miss out on order flow directed through encrypted mempools. Over time, the economic pressure may force widespread adoption.

**4. Potential Impact on MEV**

Batched encrypted transactions introduce new dynamics in the MEV landscape:

- Coincidence of Wants: Batches of transactions may cancel out overlapping intentions (e.g., two users executing opposing trades), potentially reducing the overall MEV generated. However, this does not eliminate the MEV opportunity but redistributes it more equitably.
- Smaller Backrunning Profits: With encrypted transactions processed in batches, the average backrunning profit may be slightly lower than in today’s system, where individual transactions are isolated. This could marginally reduce validator earnings from MEV but improve fairness and efficiency.

**5. Sustainability and Ecosystem Growth**

Encrypted mempools attract new order flow while offering enhanced privacy and fairness. Validators and builders embracing this system position themselves as key players in a more equitable Ethereum ecosystem.

By integrating with them, validators gain access to priority fees and MEV opportunities while aligning with user demand for privacy. Over time, encrypted mempools could redefine the economics of Ethereum, driving adoption and fostering innovation in block-building practices.

# Open questions

**1. Optimizing Economic Incentives**

- How can economic structures be designed to accelerate the adoption of encrypted mempools by validators, RPCs, apps, and users?

**2. Back-Running MEV Distribution**

- What is the optimal way to fairly and effectively distribute back-running MEV during Step 2?

**3. Threshold Trust Assumption Mitigation**

- How can the threshold trust assumption be minimized, and could sub-sampling from the validator set improve robustness?

**4. Advanced Cryptography for Full Transaction Encryption**

- What cryptographic techniques or advancements can be leveraged to achieve practical, fully encrypted transaction processing?

**5. User-Side Encryption**

- How can encryption processes be integrated into the user’s environment, such as in the dapp frontend or directly within wallets, to enhance privacy without sacrificing usability?

# Further Improvements

### Integration with FOCIL

Our solution for a threshold encrypted mempool on Ethereum L1 integrates well with [FOCIL (Fork-Choice enforced Inclusion List)](https://ethresear.ch/t/fork-choice-enforced-inclusion-lists-focil-a-simple-committee-based-inclusion-list-proposal/19870). Essentially, in FOCIL a set of validators is selected into an inclusion list committee. Each member of the committee proposes an inclusion list and the block proposer eventually merges all inclusion lists into one global list. Attesters will then check if (1) they agree to the global inclusion list and (2) the block contains all transactions from the global inclusion list.

While FOCIL has been introduced for plain transactions, nothing prevents us from using it for encrypted transactions as well. In fact, FOCIL allows us to improve the censorship resistance of our solution: imagine a block proposer censors encrypted transactions simply because they are encrypted. Then FOCIL can force the proposer to include such transactions as well.

## Preventing Collusion in Threshold Cryptography

Since Shutter is a threshold encryption scheme, it relies on the threshold trust assumption. However, we are actively working on solutions that overcome this assumption:

**ShutterTEE:** Together with [PolyCrypt](http://polycry.pt/) we are developing a system where Keypers store their key shares inside a TEE such that Keypers cannot access their shares unless the TEE grants the access. That is, in order to obtain the share, a Keyper must prove to its TEE that it requires the share at the current moment to ensure a correct execution of the Shutter protocol. This guarantees that Keypers receive their shares only when it is absolutely necessary, which prevents premature decryption of transactions.

**Secret Sharing with Snitching:** We are exploring novel cryptographic primitives that allow us to detect and punish malicious behavior such as collusion. For instance, we have been looking into **secret sharing with snitching** ([see our blog post](https://blog.shutter.network/secret-sharing-with-snitching-addressing-shareholder-collusion-in-threshold-cryptography/)), a novel secret sharing primitive that allows to identify colluding shareholders and punish (snitch on) them for malicious behavior.

**Utilizing Economic Security of Validator Set:** A validator in Ethereum has a stake of 32 ETH, which acts as a form of economic security in case the validator misbehaves. Considering the size of Ethereum’s validator set (>1 million), there is a significant potential to utilize this stake for additional economic security. For instance, if a validator commits to including a transaction at a certain position in the block, but fails to fulfill that commitment, it can get financially punished. Similarly, we imagine a system, where the Keyper set consists (partially) of validators such that their stake can be used for financial punishment in case of premature decryption.

## Stuck in the Mempool Privacy

Shutter can operate in two different modes:

**1. Per transaction encryption:** In this mode, each transaction is encrypted under a unique encryption/decryption key pair. That is, for each encrypted transaction, the Keypers must derive a decryption key, which results in significant communication overhead.

**2. Per epoch encryption:** In this mode, there exists a unique encryption/decryption key pair for each epoch. During an epoch, all transactions are encrypted using the epoch’s public key. Once the corresponding secret key is released, these transactions become publicly accessible. However, this approach poses a significant issue: encrypted transactions that fail to be included in the next block lose their privacy. As such, transactions are exposed and become vulnerable to front-running and sandwich attacks.

The recently introduced cryptographic primitive of batched threshold encryption can be employed to address the above problems. Batched threshold encryption allows the Keypers to batch encrypted transactions and release a single decryption key to decrypt all transactions in the batch. Transactions that are not included in the batch remain encrypted and private. At the same time, releasing the decryption key requires only constant communication overhead as opposed to the linear communication overhead when releasing a key for each encrypted transaction.

# Recap

The journey toward an encrypted mempool on Ethereum L1 tackles fundamental issues like censorship, front-running, and builder centralization, aiming to enhance fairness, privacy, and decentralization. While the vision of fully encrypted transactions is ambitious and not yet practical at scale, the proposed roadmap lays out concrete steps to move forward: starting with RPC integration, building through relays and proposer commitments, and ultimately embedding these capabilities directly into Ethereum’s protocol.

This is just the beginning. We, the Shutter Network, Gnosis, MEV Blocker, Nethermind, Chainbound, and more, are actively collaborating on this effort and are committed to making it a reality. This initiative requires broad engagement and diverse perspectives to succeed. We invite core developers, validators, builders, relays, and everyone in the ecosystem to join the conversation, provide feedback, and help refine these ideas.

---
source: ethresearch
topic_id: 19599
title: Self-Sovereign Identity and Account Abstraction for Privacy-Preserving cross chain user operations across roll ups
author: EugeRe
date: "2024-05-20"
category: Execution Layer Research
tags: [zk-roll-up, account-abstraction, signature-aggregation, transaction-privacy, sequencing]
url: https://ethresear.ch/t/self-sovereign-identity-and-account-abstraction-for-privacy-preserving-cross-chain-user-operations-across-roll-ups/19599
views: 7257
likes: 26
posts_count: 15
---

# Self-Sovereign Identity and Account Abstraction for Privacy-Preserving cross chain user operations across roll ups

This is a part of a longer research on the topic which ultimately intends to establish a common framework to originate on-chain data and process it to the networks supporting data minimization to balance user privacy and compliance needs.

I wanted to thank [Erwin Voloder](https://www.linkedin.com/in/erwin-voloder-mes-317735125/?original_referer=https%3A%2F%2Fwww%2Egoogle%2Ecom%2F&originalSubdomain=hr), [Pete Cooling](https://twitter.com/PeteCooling), [Kim Hamilton](https://twitter.com/kimdhamilton?lang=en) and [Martin Schaffner](https://www.linkedin.com/in/martinschaeffner/), who personally supported this research in different ways and the people from ERC-4337 Team, specifically [@yoavw](/u/yoavw) , [@zincoshine](/u/zincoshine) AA Mafia Telegram Group, [Alex](https://x.com/alexanderchopan) and [Eric](https://twitter.com/randomishwalk?lang=en)  for further support. This is an ongoing project, I hope you appreciate the forward thinking and we are continuing to work on it. Any feedback or support is appreciated, in light blue hyperlinked public content for reference.

**ABSTRACT**

This research explores the innovative integration of Self-Sovereign Identity (SSI) systems with Account Abstraction (AA) to enhance privacy, compliance, and user experience on the Ethereum blockchain. By leveraging verifiable credentials (VCs) and Ethereum attestations (EAs), the proposed framework empowers bundlers - builders to pre-validate transactions, standardize onchain executions and empowering cross chain atomic transactions. The implementation of Merkle proofs and Zero-Knowledge Proofs (ZKPs) ensures efficient data processing and minimal disclosure, addressing both scalability and security concerns.

A significant highlight is the introduction of keystore rollups, which manage encryption keys off-chain to facilitate atomic cross-chain transactions. These rollups promote interoperability between sequencing networks, ensuring seamless data exchange and robust security. The research underscores the potential of modular blockchain networks and advocates for the adoption of ERC-4337 and future cryptographic advancements to standardize and optimize Ethereum’s execution layer.

[![image](https://ethresear.ch/uploads/default/optimized/3X/a/1/a188a43640c6bf6eec031e26b8619517255865a6_2_690x368.png)image915×488 24.9 KB](https://ethresear.ch/uploads/default/a188a43640c6bf6eec031e26b8619517255865a6)

**THE WORK**

Using verifiable credentials (VCs) or Ethereum attestations (EAs) to empower bundlers in a shared mempool can potentially reduce the risk of on-chain reverts by sequencers and penalties for block builders. By including data assertions in user operations, bundlers are supported in the pre-validate certain aspects of the transactions. This pre-validation can help to set out specific permissions interacting with different apps into a shared mempool collecting multiples User operations and so reducing the risk of errors during execution. This reduces the chances of sequencers including such operations in blocks, lowering the overall revert risk. VCs and EAs provide cryptographic proofs that can be verified by sequencers. These proofs can increase trust in the validity of the operations, making sequencers more confident about including them in blocks.

The effectiveness of data assertions can further support onchain standardization and native account abstraction adoption but using VCs and EAs in a shared mempool with ERC-4337 could be considered as first step to it and has the potential to significantly standanrdize the execution of on-chain operations for bundlers (builders) and sequencers.

Overall, the complexity of implementing and maintaining new verification logic for bundlers may be compensated by an overall better synergy with the other actors in the network. Specifically on the logic side, general standards like did:pkh or did:dis could find common ground of assessment. In fact, the same verification logic is standards practice for user authentication where user store different assertation on the identity within the wallet application. Extending the same logic approach into the context of smart contract accounts we would suggest for bundlers to store data processing assertation into the mempool of future transactions until consolidated finality is reached.

At the same time, a standardized method for signature validation will be required. ERC-1271 enhances the security and interoperability of the system. So to ensure that all signatures whether aggregated or individual, are verified uniformly, reducing the risk of fraud and enhancing trust in the system.

In that context ERC-1271 facilitates efficient cross-chain operations by ensuring that signatures required for these transactions are validated consistently across different networks. This reduces the complexity and potential errors in verifying multiple signatures, making cross-chain transactions more efficient and reliable.

However, if the contract is not deployed yet, ERC-1271 verification is impossible. In this context [ERC-6492](https://eips.ethereum.org/EIPS/eip-6492) helps achieving an efficient UX by providing  isValidSignature function combined with a new wrapper signature format, that signing contracts MAY use before they’re deployed, in order to allow support for verification. The wrapper format is detected by checking if the signature ends in magicBytes .

This feature is wrapping the signature in a way that allows to pass the deploy data  which then can be validated off chain by eth_call or normally onchain.  In the context Account Abstraction, Smart contract Accounts can be deployed and verified for free facilitating the combination of EOAs and SCAs UX functionalities.

[The same verification and validation logic could be extended into a future unified mempool once potentially account abstraction would be natively implemented following 7560/7562 rules.](https://notes.ethereum.org/@yoav/unified-erc-4337-mempool)

Including proofs of VCs or EAs adds data to user operations, potentially leading to larger bundles and higher gas costs. This can put pressure on mempool capacity. Utilizing Merkle proofs can allow bundlers to verify the inclusion of specific data elements without needing the entire credential, reducing the amount of data processed. Merkle trees are a cryptographic data structure that allows for efficient verification of the membership of a specific data element within a larger set.

After user authentication, for each user operation, the bundler includes a Merkle proof. This proof is a concise piece of data that demonstrates the specific assertion’s inclusion within the Merkle tree of the entire bundle. This can significantly reducing the overall size of the bundle compared to including the full VCs or EAs.

VCs and EAs still remain crucial for containing the actual data and claims associated with user operations. Merkle proof act as a verification tool to standardize the execution. They provide a concise way to prove that a specific VC exists within a larger bundle of assertions without revealing the entire content of the VC/EA itself. This may help mitigate pressure on the mempool and potentially lowers gas costs.

This would imply for bundlers to access a privacy preserving shared mempool ID and establish a dedicated membership set for associated bundle of transactions, so that Sequencers can verify the inclusion of user operations in the bundle. Sequencers or other network participants can efficiently verify the validity of data assertions using the Merkle proofs. They only need to verify the proof itself, not the entire data within the assertion, reducing the computational burden.

VCs and EAs rely on the underlying logic verification process for authentication and authorization that should be implemented by bundlers. Verifying VCs or EAs requires processing cryptographic proofs. This can be computationally expensive for bundlers, especially for complex assertions.

[Merkle proofs can be combined with ZKPs for a powerful solution.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4563364) ZKPs can be used within the data assertions themselves to prove the validity of claims without revealing the underlying data. Merkle proofs ensure the integrity of the bundle and verify the inclusion of specific assertions with ZKPs within the bundle. Also, using ZKPs in VCs or EAs could reduce the amount of data included in the bundle, minimizing disclosure, and lowering computational costs.

Combining SSI verification with AA provides Ethereum a customizable authorization logic that can leverage national data repositories and business and regulatory standards before easily executing global on-chain operations. In this context, embedding a trust less verification logic can support standardizing user operations and streamlining sequencing activities, and so harmonizing operations across L2 transactions for unlocking cross chain atomic transaction and still ensuring efficient data processing compliant with data minimization.

The transaction generation, submission and execution flow can be represented with an interchained process of triangles of trust representing each moment, as described here.

[![image](https://ethresear.ch/uploads/default/original/3X/c/a/ca267e2cbe3fc7fc8140e77b202ae14c2afe5e31.png)image1000×563 39.4 KB](https://ethresear.ch/uploads/default/ca267e2cbe3fc7fc8140e77b202ae14c2afe5e31)

The market pushing for an evolution of networks towards to modular blockchains is proposing concepts of shared mempools and shared sequencing that can embed trustless verification logic typical of SSI systems to establish a root of trust from user authentication until block validation still relying on Ethereum main network as indisputable security layer.

This combination minimizes data disclosure while maintaining efficient verification, making the system more scalable and privacy-preserving.

**[Key store contract](https://hackmd.io/@haichen/keystore) [for flexible and efficient key management system](https://hackmd.io/@haichen/keystore)**

To further enhance standardization and interoperability considering key management an important function to manage user authentication and transaction authorization. A keystore contract paired with zero-knowledge proofs (ZKPs) has the potential to significantly improve the verification logic and overall functionality of data assertions within the ERC-4337 framework.

The keystore contract can securely store and manage encryption keys used by bundlers to encrypt user operations within bundles after authentication. This can ensure that only authorized parties (with the appropriate decryption key) can access the sensitive data within the bundle.

[![image](https://ethresear.ch/uploads/default/optimized/3X/4/2/42da34932f49f48f96077877f991029db0d43fb4_2_517x182.png)image1970×695 60.4 KB](https://ethresear.ch/uploads/default/42da34932f49f48f96077877f991029db0d43fb4)

The keystore contract can facilitate the pairing of the correct key with specific data assertions within a bundle. This allows different network participants (builders and sequencers) to efficiently verify the authenticity of the data using the corresponding ZKPs without needing the actual data itself. A minimal keystore rollup deployed on Layer 2 can handle a large volume of key management and verification processes off-chain, reducing the load on the main Ethereum network. The keystore functionality is key in order to ensure efficient authentication to users Identifiers and enabling cross chain user operations also leveraging shared sequencing. This allows for seamless data exchange and verification between different ecosystems, fostering a more interconnected environment supported of atomic cross chain transaction data process minimization and standardization. Different potential design for Keystore emerged in the market. Networks like Safe, Arbitrum, ZkSync, Scroll, Starknet have proposed different implementations.

**L1 Keystore with L2 Sync** - This design keeps the keystore on Ethereum L1 and syncs with L2 networks to ensure quick access and state consistency across chains. It provides high security but may involve higher latency and costs.

When the keystore state is maintained on L1 and synchronized with L2 networks to ensure quick access and state consistency across chains. This approach maintains the security guarantees of L1 while aiming to minimize latency and reduce costs associated with high transaction fees on L1. This method provides a robust security framework due to the inherent security of L1, ensuring that key management and authentication logic are protected against potential threats. However, this design can involve higher transaction costs and potential latency issues due to the need to synchronize state changes across multiple layers. A reference implementation for this design can be seen in projects like Safe.

**Dedicated L2 Keystore** - Deploying the keystore directly on an L2 network reduces costs and latency. This design uses zk-Rollups for secure key updates and storage. Deploying the keystore directly on an L2 network focuses on reducing operational costs and transaction latency. This design option utilizes zk-Rollups for efficient and secure key updates and storage, ensuring scalability without compromising security. By keeping the keystore operations within the L2 environment, transaction fees are significantly lower, and the response times for key management operations are improved.

**Hybrid Model**  - Combines L1 and L2 keystore advantages, using L1 for storage and L2 for efficient access and operations, leveraging cross-chain compatibility for seamless integration. The hybrid model combines the security benefits of L1 storage with the operational efficiency of L2 transactions. In this model, the keystore data is primarily stored on L1, ensuring high security, while L2 is used for accessing and updating keys. Merkle proofs are essential for maintaining consistency and verifying that updates on L2 are accurately reflected on L1. This model uses Merkle proofs to ensure that any changes made on L2 are consistent with the L1 state, providing a balanced approach that leverages the strengths of both L1 and L2. This design requires efficient generation and verification of Merkle proofs across both layers to ensure low latency and high security, making it a complex but highly effective solution for comprehensive key management.

Merkle proofs play a vital role in maintaining the integrity and consistency of keystore operations across different blockchain layers.

**Here is a potential process workflow and designed architecture:**

The architecture is composed by three main layers:

1. An application layer comprises wallets, PKIs apps, and SSI wallet such as Polygon ID, ZkSync ID, and other apps. These wallets and applications generate Verifiable Credentials (VCs) to prove ownership, such as being a DAO member. Users create operations objects, enabling transactions and interactions on the blockchain. This layer facilitates the  generation and management of  Verifiable Credentials and user operations  objects through apps, serving as the interface between users and the underlying blockchain infrastructure.
2. A network layer based on different L2s, which include a Keystore contract and Smart Contract Accounts. This layer is responsible for generating Zero-Knowledge Proofs (ZKPs)  and Merkle proofs for Sequencers. The Keystore contract manages encryption keys and user authentication, ensuring the correct key pairing for Verifiable Credentials and Operations. Smart Contract Accounts verify user operations, by validating ZK cryptographic proofs to ensure the integrity  of the signature of the transactions before they are executed.
3. A sequencing layer which interconnect L2s with Ethereum main-net and manages the execution of batches of transactions anchoring Roll-up IDs to sequencing networks ( projects like SUAVE, Polygon Agg Layer, Espresso Capuccino). Main functions here are batching, validation of  transactions via the Keystore roll-up, and  the Roll-up contract within Ethereum’s slots. This layer ensures efficient transaction processing by batching multiple operations into single transactions, reducing on-chain congestion and costs. Additionally, it enable cross-chain atomic transactions, enabling seamless interoperability across different blockchain networks, ensuring that transactions are securely validated and finalized.

[![image](https://ethresear.ch/uploads/default/optimized/3X/e/d/ed890d89fd25a9da0e2d575ac8c454872804906e_2_690x370.png)image993×533 63.2 KB](https://ethresear.ch/uploads/default/ed890d89fd25a9da0e2d575ac8c454872804906e)

1. Users issue VCs/EAs stored in wallet apps, authenticate into Service Apps sharing ZKPs through smart contract registry and compile user operations objects through app into shared mempool.
2. Bundlers access shared mempool ID, bundle user operations objects, set a dedicated merkle tree for each bundle. Bundlers validate user operations following ERC-4337/7562 validation rules and at the execution verifying aggregated zk proofs execute user operations through SCA.
3. The keystore contract and rollup handle key management for user authentication, transaction submission, validation and eventually key recovery between EOAs and SCAs
4. Sequencers verify  through smart contract account the Merkle proofs and the ZKPs and in case of positive results issue a pre confirmation to Bundlers, batch bundles and submit in batches of bundles  through Roll up contracts for validation on L1 and which are verified by ZK validity proof (commitments).
5. Roll up contracts validate ZK proofs of batches and builders (bundlers) finalize block or revert in case of non-validation.

Specifically in this scenario, proposals as ERC 5792 acts as a crucial bridge between user-facing applications and the infrastructure of the ERC-4337 framework. The proposal defines a common language for wallets, apps, and bundlers to communicate each other and it has the potential to significantly enhance the adoption of Smart Contract Accounts and position as the go-to standard for data assertions on the Ethereum blockchain.

Wallets and apps could signal user preferences (e.g., gas fees, preferred chain ID, or shared sequencer), required data assertions (VCs/EAs) for specific transactions.

Bundlers could leverage the received signals to automatically construct appropriate bundles for user transactions including user operations data, Merkle proofs for associated VCs/EAs and ZKP of user data claim. With this having an overall improvement for user flexibility, network decentralization and scalability.

The designed architecture also benefit from [ERC-7715](https://ethereum-magicians.org/t/erc-7715-request-permissions-from-wallets/20100), further enhancing accounts functionalities on dedicated permission sessions for EOAs and SCAs aligniing with the [EIP-7702](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7702.md) on Pectra. In fact standardized user authentication method will reinforce user protection about what permissions are being requested by dApps for starting sessions.

Once authenticated users were given permission to start sessions, dapps could leverage User operation builders through apps hosted on bundlers and following ERC-7679 compile different intents as standardized user operations.

[ERC-7679](https://ethereum-magicians.org/t/erc-7679-useroperationbuilder-a-common-onchain-interface-for-dapps-to-interact-with-4337-wallets/19547) provides a common on-chain interface, the UserOperationBuilder, for dApps to interact with ERC-4337 Smart contract Accounts. This interface helps standardize how user operations are constructed, making it easier for dApps to support various account implementations without needing account-specific SDKs.

The proposed design also goes into the direction of modular networks that can be built over Ethereum network by the Ethereum community. In this modular scenario ERC 4337 and future developments benefits from possible future implementations as Verkle trees or consensus related proposals as ePBS.

Bundlers create bundles containing user operations, Merkle proofs, VCs/EAs (potentially with ZKPs), and additional data.

Sequencers verify Merkle proofs and potentially VCs/EAs within bundles, order bundles, perform additional verification if needed, submit pre-built blocks to validators.

Before accepting the request, the sequencer should:

- If block range was given, check that the block number is within the range.
- If timestamps range was given, check that the block’s timestamp is within the range.
- For an address with a storage root hash, validate the current root is unmodified.
- For an address with a list of slots, it should verify that all these slots hold the exact value specified.

[The sequencer should REJECT the request if any address is doesn’t pass the above rules.](https://notes.ethereum.org/@yoav/SkaX2lS9j#)

Builders construct valid blocks based on pre-verified and potentially pre-ordered bundles received from sequencers, considering block gas limits and network conditions. Ultimately, validators verify the validity of submitted blocks (including the validity of the included bundles), reach consensus on block inclusion in the blockchain.

**CONCLUSION**

Driving towards the adoption of blockchain services implies relying on modular networks that can balance security, scalability and decentralization to populate an ecosystem of applications as plug and play solutions for dedicated use cases, in this regard combining SSI verification logic into the network operations to users and machines to support accountability and compliant data processing process is key. Smart Contract Accounts can facilitate adoption by flexible UX and shared sequencing networks support cross chain atomic transaction reconciliation. The narrative of this research wants to emphasize the need to abstract complexities from accounts, and networks where decentralized identifiers and keystore roll up can facilitate the verification and execution of sequencing networks.

The ability to define custom transaction validation logic opens up a whole new design space for smart contract interactions. We could see the emergence of new types of dapps and use cases that were previously not possible or practical with traditional EOA accounts.

Following [EIP 7702](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7702.md) we could detect in the community the need to establishing a functional link between EOAs and SCAs that could enable more sophisticated and comprehensive service offerings. Smart contract wallets could incorporate identity verification, credit scoring, or other off-chain data into their transaction validation process. This could pave the way for decentralized credit markets, self-sovereign identity and more robust decentralized governance models where user authentication and transaction authorization are distinctly operated, but functionally integrated to ensure decentralization and onchain optimization.

In the future, it is possible to envision networks connecting entry points and Native Account Abstraction entities executing cross chain user operations, distinguishing between validation and execution code as described by [EIP 7701](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7701.md).

In this context scenario, SSI systems could play a key role in ensuring validation linking between Users and user operations, after that, different entry points leveraging decentralized sequencing networks could simultaneously coordinating with block builders for the execution of the bundles following rules as described by [EIP 7711](https://github.com/ethereum/RIPs/blob/master/RIPS/rip-7711.md).

VCs could be useful for bundlers which currently rely on trusted simulation of validation rules. Integrating and SSI environment can enhance this process ensuring that the validation logic integrates also user related zk proofs relating to identity or special requirements to request UserOps reducing the likelihood of validation reverts.

**Takeaways**:

- SSI: Integrates trustless identification, enhancing privacy and data minimization to establish a pre validation framework for User Operations.
- Smart Contract Accounts: Simplifies user experience and facilitates regulatory compliance and governance needs, enhances onchain optimization through batching and sponsoring transactions.
- Verifiable Credentials (VCs) and Ethereum Attestations (EAs): Used to empower bundlers, reducing the risk of on-chain reverts and penalties for block builders by standardizing data format for user authentication.
- Merkle Proofs: Efficiently verify specific data elements within larger sets, mitigating mempool pressure and lowering gas costs.
- Zero-Knowledge Proofs (ZKPs): Enhance privacy by proving the validity of claims without revealing underlying data complying with GDPR data minimization processed through networks.
- Shared Mempools: Facilitate bundle operations setting.
Keystore contracts Manage the interaction of  different cryptographic keys of different accounts on different networks providing key management harmonization.
- Keystore rollups Enhance atomic cross-chain transactions across sequencing networks by providing a scalable and interoperable data reconciliation that ensures seamless data exchange and verification across different L2.

**References**:

[Notes on the Account Abstraction roadmap](https://notes.ethereum.org/@yoav/AA-roadmap-May-2024)

[RIP 7560](https://github.com/ethereum/RIPs/blob/e3bead34f1bcf1aa37fd51923ad99a77b801775c/RIPS/rip-7560.md#unused-gas-penalty-charge)

[EIP 7562](https://eips.ethereum.org/EIPS/eip-7562)

[Roadmap for Native Account Abstraction Introduction](https://hackmd.io/@alexforshtat/native-account-abstraction-roadmap))

[Unified ERC-4337 mempool](https://notes.ethereum.org/@yoav/unified-erc-4337-mempool)

[Blockchain Privacy and Regulatory Compliance: Towards a Practical Equilibrium](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=6131244)

[Keystore Design](https://hackmd.io/@haichen/keystore)

[Dedicated minimal rollup for keystores](https://notes.ethereum.org/@vbuterin/minimal_keystore_rollup)

[Integration API for EIP-4337 bundler with an L2 validator/sequencer](https://notes.ethereum.org/@yoav/SkaX2lS9j#)

[Decentralized Future: ERC-4337 Shared Mempool Launches on Ethereum](https://etherspot.io/blog/decentralized-future-erc-4337-shared-mempool-launches-on-ethereum/)

[Verifiable Credentials Data Model v2.0](https://www.w3.org/TR/vc-data-model-2.0/#:~:text=A%20verifiable%20credential%20is%20a,certificates%2C%20and%20digital%20educational%20certificates.)

[Ethereum Attestation Service](https://attest.org/)

[Supercharging Account Abstraction with Attestations](https://mirror.xyz/0xeee68aECeB4A9e9f328a46c39F50d83fA0239cDF/afmS07VvelERZHzG6SSzhOKJlNwhU3jsE-4atkbNZto)

[Minimal KeyStore Rollup spec](https://hackmd.io/@mdehoog/mksr)

[ERC-1271: Standard Signature Validation Method for Contracts](https://eips.ethereum.org/EIPS/eip-1271)

[ERC-6492: Signature Validation for Predeploy Contracts](https://eips.ethereum.org/EIPS/eip-6492)

[EIP 7702](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7702.md)

[ERC-7715: Request Permissions from Wallets](https://ethereum-magicians.org/t/erc-7715-request-permissions-from-wallets/20100)

[ERC-7679: userOperationBuilder - a common onchain interface for dapps to interact with 4337 wallets](https://ethereum-magicians.org/t/erc-7679-useroperationbuilder-a-common-onchain-interface-for-dapps-to-interact-with-4337-wallets/19547)

[Towards the wallet endgame with Keystore](https://scroll.io/blog/towards-the-wallet-endgame-with-keystore)

[Keystore design by Haichen Shen](https://hackmd.io/@haichen/keystore)

[EIP 7701 - A variant of RIP-7560 transactions relying on EOF Smart Contract Accounts](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7701.md)

EIP 7711 - An RIP-7560 transactions bundle transaction type

[What is EIP-7702? A Beginner’s Guide](https://blog.thirdweb.com/eip-7702/)

## Replies

**dpl0a** (2024-06-13):

Honestly, this is a saner and more thought-through idea than what has been pushed lately in the european union with eIDAS 2.0 and the EUDI wallets (which actually violate the basic principles of SSI, among various other design problems). Are you familiar with these?

---

**EugeRe** (2024-06-13):

Hey [@dpl0a](/u/dpl0a) ! Thanks for the feedback and I agree. There is also an angle on which I am currently working on EUDI wallet side. You could have PID issuers linking QEEA  zk proofs to SSI wallets, this would also help to reduce the risk for sybil attacks in DAOs operations. I will publish another blog post soon describing high-level interactions in a dedicated use case.

---

**andreolf** (2024-06-13):

This work looks great [@EugeRe](/u/eugere)

I believe the architecture create a good synergy between EOAs and SCAs which operate different key functions. What kind of uses cases do you see ? Also is this in line compatible with 7702?

---

**JoshuaSum** (2024-06-13):

Great research, [@EugeRe](/u/eugere)! Combining SSI with AA is super interesting and this definitely opens up a lot of potential to enhance privacy and the user experience while reducing on-chain issues by pre-validating transactions. Awesome to see how this aligns with the trajectory and broader vision for modular blockchain networks.

Looking forward to seeing practical examples and use cases for this approach from the community! Particularly interested in how this can help with DAO ops

---

**EugeRe** (2024-06-14):

Thanks [@andreolf](/u/andreolf) ! I am working on uses cases right now, essentially, the system combines EOAs and SCAs in synergistic areas of functionality. EOAs excel for user authentication, preserve decentralization in that function leveraging SSI, while SCAs excel for onchain activity optimization as batching and sponsoring.

In terms of use case, I am working for instance, on the application of keystores and under the EIDAS framework for the execution of grants which need to be executed between different DAOs or with DAOs which have a multi-chain implementation.

To my knowledge, EIP 7702 allows EOAs to temporarily assume smart contract capabilities so it seems to me in line in terms of on-chain optimization, validation/execution separation, and supporting standardization for cross chain ops.  At the same time fits the purpose of proposing the coexistence of EOAs and SCAs  rather than migration from or to it.

What do you think?

---

**EugeRe** (2024-06-14):

Hi [@JoshuaSum](/u/joshuasum)  many thanks for reaching out! I am working on a use case involving DAOs can be facilitated in collaborate on joint proposals, enabling voting and allocating grants to Sub DAOs on multi chain environment. I will follow up on separate blog post with that use case, but work will take from this system designed here.

Would you be interested to learn more?

---

**Thegaudent** (2024-06-15):

First of all, Great Job [@EugeRe](/u/eugere) quick question, with the focus on data minimization and privacy, how do you plan to ensure the efficient processing of Merkle proofs and Zero-Knowledge Proofs (ZKPs) within the keystore rollups?

---

**EugeRe** (2024-06-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaudent/48/16726_2.png) Thegaudent:

> how do you plan to ensure the efficient processing of Merkle proofs and Zero-Knowledge Proofs (ZKPs) within the keystore rollups?

Hey [@Thegaudent](/u/thegaudent) thanks for your message, if i understand correctly the question is, how to ensure cross chain transaction compliance with data protections regulation (eg GDPR in EU).  Personally the answer implies many considerations.

Firstly, is worthy to mention that signatures and proofs aggregations are generally used as features to ensure data minimization across networks, for that purpose the research tries to establish a standard approach. In this context, user authentication through the SSI system could also be performed, partially relying on off chain issued credentials. On the onchain side, smart contract entry points may be considered data controllers while sequencing networks processing the underlying transactions may be considered data processor.

Generally, ensuring GDPR compliance requires careful delineation of roles between data controllers (smart contract account entry points) and data processors (sequencing networks). I believe this research highlights that theoretically, implementing data minimization, encryption, and robust access controls ensures that the system architecture also integrating with other features as MPC and other technologies not described here. In this way, It could be achievable delivering cross-chain atomic transactions while adhering to at least most of GDPR requirements.

---

**EugeRe** (2024-06-20):

Thanks [@shuoer86](/u/shuoer86) ! much appreciated, I am looking for technical writers and researchers to support with the code development and implementation.

I have some ideas on use cases and refined value proposition, also I see compatibility with 7702 on Pectra.

Would you interested to help? Let’s chat!

---

**Thegaudent** (2024-06-22):

Yes, I meant the GDPR. Thank you for the clarifications. It looks like we have all the necessary tools for compliance. Thanks again

---

**Therecanbeonlyone** (2024-07-23):

[@EugeRe](/u/eugere) great work and post. I had not thought of using SSI for mempools. As you correctly point out the usage of zkps as representations of VCs is key.

The [Ethereum Open Community Projects](https://github.com/ethereum-oasis-op/L2) is about to publish a similar piece of work utilizing both DIDs and VCs and pointing out that most pieces required to implement SSI at scale with an L2 keystore actually exist today both as a global standard and as reference implementations. The draft of the paper is [here](https://docs.google.com/document/d/1oLEZVaTSDMVTjMbB2rbbLXRZOQP81_hY_82UpjDGBdY/edit?usp=sharing) in case you or anyone else is interested. Will update the blog site soon.

If you are interested in collaborating on this topic, let me know.

The report should be going

---

**EugeRe** (2024-07-24):

Hi [@Therecanbeonlyone](/u/therecanbeonlyone) many thanks for sharing and I appreciate your feedback!

I would be very interested to collaborate, please let me know how can I help you in drafting or development. I believe I can also bring valuable network from DIF and other stakeholders with Ethereum Community.

Also I want to suggest my latest blog here:

[Enabling standardized on chain executions through Modular Accounts](https://ethresear.ch/t/enabling-standardized-on-chain-executions-through-modular-accounts/20127)

The post introduces a framework based on the ERC 7579 proposal, which integrates a module to lavage onchain verifiable credentials and zero-knowledge (zk) proofs in the context of modular smart accounts. This framework aims to standardize onchain executions by separating user authentication and transaction authorization while preserving privacy and regulatory requirements throughout the transaction lifecycle.

The core function of the system described involves validating zk proofs generated by VCs to authenticate users and authorize operations. This makes the Validation Module the most appropriate choice, as it is designed to validate user operations before they are executed.

I believe this could be a valuable contribution as it reference a proposal which is easier to implement, and already in development in the market.

What do you think?

---

**AtabeTuatara** (2024-10-19):

Hi [@EugeRe](/u/eugere), Lots of deep work here. A serous investment in time.

From what I understood, the focus is on achieving end-user privacy while minimizing computational and gas costs for bundlers/sequencers during ZKP verification and pre-validation. This approach is great.

Let’s say we the transaction initiator uses a device passkey from their own SCW (currently the most anonymized auth form), it would eventually map to the Verifiable Credential (VC) for audits like taxes, revealing the identity since the issuer is often the agency that created the verification.

Is your goal to anonymize transactions even from the VC issuer or just from other parties who might know the SCW’s signature due to a prior relationship?

Also, if this is a global SCW (i.e.: not the user’s own), isn’t this similar to the Tornado network? And we all know where that ended up.

---

**EugeRe** (2024-10-19):

Hey [@AtabeTuatara](/u/atabetuatara) many thanks for your comment, I appreciate your feedback. Considering that, I want to clarify a few things.

The work intends to standardize the process of selecting  on chain identifiers to make cross chain executions. I believe that the set up described, passkey plus SCW fit the purpose.

In the first scenario, like enterprise oriented use, the SCW owns the policy rules map VCs and executes the Use Ops. So in that context, the goal is to anonymize from other parties. Thinking outside of the box, the same approach may be doable, approaching privacy pools that prove a specific association membership set to access SCW.

Privacy pools actually can fit the purpose of matching compliance requirements with privacy needs, quite far from Tornado Network purpose.

Happy to further engage ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)


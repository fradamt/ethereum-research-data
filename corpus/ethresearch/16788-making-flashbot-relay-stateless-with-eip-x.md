---
source: ethresearch
topic_id: 16788
title: Making Flashbot Relay stateless with EIP-x
author: sogolmalek
date: "2023-09-28"
category: Proof-of-Stake > Block proposer
tags: [mev, stateless]
url: https://ethresear.ch/t/making-flashbot-relay-stateless-with-eip-x/16788
views: 2116
likes: 5
posts_count: 7
---

# Making Flashbot Relay stateless with EIP-x

In the realm of Ethereum research and innovation, the notion of Proposer-Builder Separation (PBS) stands as a fundamental design choice, showcasing its potential to enable validators to equitably benefit from Miner-Extractable Value (MEV). This deliberate separation addresses the critical concern of preventing incentives for validators to centralize through MEV accumulation. In the absence of PBS, validators would engage in a competitive struggle for MEV, potentially amplifying centralization dynamics among those participating.

PBS introduces a novel paradigm where validators are distinct from block builders, allowing builders to specialize in block construction, particularly in optimizing MEV, while validators concentrate on validation. This approach leads to a more efficient and equitable distribution of responsibilities within the network.

Within the PBS system, various types of actors, often referred to as searchers, are identifiable, including the customary MEV bots, users seeking protection like Uniswap traders, and Dapps with specific use cases such as account abstraction and gasless transactions. These searchers express their bids through gas prices or direct ETH transfers to a designated coinbase address, which enables conditional payments based on the success of the transaction.

However, a notable challenge within the Flashbot ecosystem arises from the absence of costs for failed bids, opening up possibilities for network spam via invalid bundles and potential denial of service (DoS) threats. Malicious actors could inundate miners with invalid bundles, leading to wastage of computational resources.

To address this concern and align with the PBS system, we propose the introduction of EIP-x, a stateless light client built on top of the Portal Network, focused on consuming Zero-Knowledge Proofs (ZKPs). EIP-x can serve as a critical software component for creating stateless relays, capable of efficiently verifying bundle validity and payment status using ZKPs. By leveraging this approach, we can prevent invalid bundles from reaching miners, bolstering network security and addressing the Flashbot ecosystem challenges in a strategic manner.

EIP-x’s integration with the PBS system presents a threefold solution to the Flashbot dilemma:

1. Efficient Ethereum State Consumption: As illustrated in the flow, relayers can seamlessly consume Ethereum state, specifically the ZKP of the last block state provided, optimizing resource usage.
2. ZK Payment Proof: EIP-x enables the provision of a ZK payment proof by bundlers, ensuring efficient resource utilization by validating whether the bundler has made the requisite payment to the miner.
3. Content Privacy and Verification: Preventing relayers from having unfettered access to bundle contents and enabling a secure validation process through ZKPs. This ensures the prevention of malicious searchers and failed bids from supplying invalid ZKPs, which would otherwise incur high verification costs.

Furthermore, to mitigate the risk posed by malicious searchers providing invalid ZKPs, we propose implementing smart contract escrows. These escrows would hold payments in abeyance until the associated ZKP is validated, ensuring network integrity and averting potential abuse.

In conclusion, our [EIP-x](https://github.com/sogolmalek/EIP-x/blob/main/project.md), harmoniously aligned with the PBS system, offers a strategic and innovative approach to tackling the challenges posed by the Flashbot ecosystem. By leveraging stateless light clients and ZKPs, we pave the way for enhanced network security, streamlined resource utilization, and a robust foundation for decentralized finance (DeFi) in the Ethereum ecosystem.

## Replies

**mikeneuder** (2023-09-29):

Interesting post, Sogol! The idea of a “trustless relay” has been floated before and it has some echoes in what you describe. The way i understand it, a full zkEVM could be used to facilitate the auction between the builder and the validator (without the need of the trusted third party of the relay) by proving

(a) that the builder’s block is valid, and

(b) that the builder’s block accurately pays the proposer for their slot.

This is great, but it isn’t quite enough to construct the full trustless relay because it doesn’t provide any guarantee about the availability of the payload. Thus as a malicious builder, I could try to grief a proposer by constructing a valid block that pays them a large amount, but not releasing it. So beyond just the zkEVM, we would also need some form of payload encryption. With the encrypted payload published, we would need some form of decryption, whether that be a time-delay construction or maybe a threshold version. Anyways, cool idea, and would be curious to hear if you think the DA problems arise in the searcher-builder relationship as well.

Also, out of curiosity, how big of a deal is the bundle spam for builders? It seems like searchers and builders would need to have a pretty symbiotic relationship because they both need each other to compete and land blocks on chain. I have always imagined that their relationship is reputation based and DoSing a builder would be a quick way to get ignored as a searcher. Thanks!

---

**sogolmalek** (2023-09-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> but it isn’t quite enough to construct the full trustless relay because it doesn’t provide any guarantee about the availability of the payload.

Thank you for your brilliant and insightful comments, Mike. ![:star_struck:](https://ethresear.ch/images/emoji/facebook_messenger/star_struck.png?v=12)

Yes I agree. Ensuring the availability of the payload is crucial. I love to know your /community thoughts on a fully trustless and decentralized escrow system as a solution. Requiring builders to deposit collateral into the escrow smart contract, creates a compelling financial incentive for them to release the payload on time.

The beauty of this approach lies in its autonomy. The escrow operates autonomously based on predefined conditions in the smart contract, eliminating heavy reliance on reputation systems. Participants can trust that funds will be automatically released when conditions are met, removing the need for trust in a central authority. This provides transparency and immutability as the terms are encoded in a blockchain smart contract.

Another option worth considering is implementing a time-lock encryption mechanism for the payload. Builders would need to release the decryption key within a specified time frame after block creation. If they fail to do so, the network can automatically release it, ensuring payload availability even if malicious withholding is attempted.

regarding the relationship between searchers and builders, you are absolutely right. However, i think the risk of reputation damage and strained relationships due to bundle spam is substantial and can significantly impact the symbiotic relationship between searchers and builders. This relationship is critical for both parties to compete effectively and successfully land blocks on the blockchain.

But in the case of Intentional spamming, or DoSing a builder with unnecessary or irrelevant transactions (bundle spam), not only wastes resources but can harm a builder’s ability to construct efficient blocks. It strains the symbiotic relationship, leading to a breakdown in trust and potentially causing searchers to ignore or avoid collaborating with the spamming builder. Reputation is a currency in this ecosystem, and a tarnished reputation can have lasting detrimental effects on a builder’s opportunities and collaborations within the blockchain community.

---

**mikeneuder** (2023-09-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/sogolmalek/48/12119_2.png) sogolmalek:

> Another option worth considering is implementing a time-lock encryption mechanism for the payload. Builders would need to release the decryption key within a specified time frame after block creation. If they fail to do so, the network can automatically release it, ensuring payload availability even if malicious withholding is attempted.

Agreed that some escrow system is a good place to start, but the issue of the ~timing~ of the payload release is still the most important piece. A builder could construct a block, prove it satisfies some conditions, and then release it 4 seconds too late (to grieve the proposer). Thus there needs to be some party enforcing the timeliness of the builder payload. This is the inspiration for the [optimistic relaying endgame](https://ethresear.ch/t/why-enshrine-proposer-builder-separation-a-viable-path-to-epbs/15710#optimistic-relaying-endgame-11), which we refer to as a “collateralized mempool oracle service” and the [Payload-Timeliness Committee](https://ethresear.ch/t/payload-timeliness-committee-ptc-an-epbs-design/16054).

I don’t see a good way for this part to be automated, but would love to be wrong! I mostly wish we had VDFs lol

---

**sogolmalek** (2023-09-29):

You’re absolutely right Mike; ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=12)

The timing of payload release is crucial. What if we would implement an automated time-lock mechanism within the escrow SC to govern the payload release?  Builders must release the payload within a specified time frame after block creation. If the release is delayed beyond the allowed time, penalties or consequences can be triggered.

---

**Heos** (2023-10-05):

Interesting post. Is builders being spammed really an issue? The only data I found is more about builders spamming relays: https://mevboost.pics/

You can see that some builders are sending way more bids than others.

Is it efficient to bid more than 800 times per slot, so your timing is more likely to be the best bid currently observed? It would be exciting to see some data, what amount of value is lost due to this bidding behavior due to some timing issues and validators missing the best block.

---

**sogolmalek** (2023-10-06):

Thanks [@Heos](/u/heos). Im not sure Whether bidding more than 800 times per slot is efficient , because it depends on various factors, including network conditions, gas prices, and competition. While it might increase the likelihood of being included in the best block, it can also lead to network congestion and increased gas fees. The impact on value lost due to this bidding behavior can vary, and it would require detailed data analysis to provide specific numbers.

However the value proposition of letting flashbot  relay operate stateless , goes beyond spammy builders. for example executing the flashbot relay on top of our stateless light client enables Stateless relay which  reduces the reliance on Flashbots measures. By lettign relay operating within a decentralized network of stateless nodes, this approach distributes the workload and mitigates the risk of centralization, promoting a more robust and secure network. Furhtermore, by runnign the realy on EIp-X nodes,relay will have a ability to verify incoming bundles and proofs of the last state of transactions ensures trustworthy validation of transactions.last but not least, we can then  experience Resilience Against Block Reorganizations. The requirement for the hash of the previous block (parent hash) to align with the expected or desired block hash in bundles, enforced through zkps, enhances resilience against block reorganizations. Our nodes allow relay to verify the zkp of hashes. This minimizes the potential disruption caused by reorgs, enhancing the overall stability and predictability of the blockchain. Ill expand on these in new post very soon and happy to have community thoughts on it


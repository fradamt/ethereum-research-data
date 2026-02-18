---
source: ethresearch
topic_id: 17350
title: Trustless access to Ethereum State with Swarm
author: tonytony
date: "2023-11-08"
category: Execution Layer Research
tags: [data-availability]
url: https://ethresear.ch/t/trustless-access-to-ethereum-state-with-swarm/17350
views: 3039
likes: 7
posts_count: 16
---

# Trustless access to Ethereum State with Swarm

# Trustless access to Ethereum State

*Inputs and reviews by Viktor Tron and Daniel Nagy better shaped this text.*

## ABSTRACT

This proposal addresses the problems related to accessing the current or historical state of blockchain data of the Ethereum network. The proposal offers a principled way to tackle the blockchain data availability issue in a way that ensure data access is verifiable, efficient, and scalable.

## PROBLEM

When DApps need to access blockchain state, they call the API of an Ethereum client that is meant to provide the current state correctly. This condition is most directly satisfied if the DApp user runs their own Ethereum full node that synchronises with its peers on the same network to build and verify the state.

Very early on this proved unrealistic in practice: given the resource-intensive nature of running a full node, they struggled to effectively manage in real-time two essential tasks - actively participating in the consensus process and handling data uploads and queries.

Two distinct methods emerged to tackle this: light clients and centralised service providers.

Light clients are not meant to maintain and store the full state, but only synchronise the header chain, while they originally used the Ethereum wire protocol to retrieve state data with merkle proofs verifiable against the header chain. Over time, they have evolved to use a specialized subprotocol known as LES (Light Ethereum Subprotocol). However, LES still faces challenges related to efficiency and lacks robust incentive mechanisms to encourage full nodes to support light client services.

Another strategy is to use centralised service providers to offer remote endpoints for DApps to use. While this proved to work very well in practice, it reintroduced concerns of resilience, permission, and privacy which Ethereum itself was supposed to remedy in the first place.

Centralised provision exposes the network to single point of failure scenarios and also raises privacy concerns due to the ability to  track users’ query origins. Centralised control, on the other hand, makes the system susceptible to political pressure and regulations leading to censorship. On top of this, the lack of verifiable integrity proofs makes this solution not so different from using the API of a public block explorer running on centralised servers.

The current situation is elucidated by the following documented mishaps:

- State data integrity is not preserved, because Block explorers digest state data and prune some of the collected data, lacking accuracy:  “EtherScan misses nearly 15% of what are called ‘appearances’ ” (Source: Trueblocks - How Accurate is EtherScan?).
- Users’  privacy is not protected and information leaks from the originator of queries: “Infura will collect your IP address and your Ethereum wallet address when you send a transaction.” (Source: Unmasking Metamask — Is Web3 Really Decentralized And Private?).
- Centralised providers may block users or entire communities for purely political reasons (Source: Infura Cuts Off Users to Separatist Areas in Ukraine, Accidentally Blocks Venezuela) or other reasons (Source: Infura, Alchemy Block Tornado Cash Following Treasury Ban).

Another burning issue is access to historical state data. Although planned since Ethereum’s launch, archival nodes are non-existent to this day due to both technical challenges and lack of incentives.

Addressing this situation will strongly reinforce Ethereum’s position as *the* leading decentralized platform and advance the broader vision of a user-centric, decentralized Web3 infrastructure that promotes privacy-conscious and permissionless access to information.

## HOW SWARM COULD HELP

Swarm network ([web](https://.ethswarm.org), [wp](https://www.ethswarm.org/swarm-whitepaper.pdf)) presents a practical and realistic solution to the full-node latency problem: by establishing a dense network of actively participating nodes that will ensure the storage and dissemination of these crucial pieces of data during the bootstrapping phase. The dataset exposed by Swarm is designed to be completely reproducible, ensuring the integrity and reliability of the data, allowing for verification and validation of its contents.

This approach draws inspiration from the peer-to-peer principles of torrenting, through queries that traverse the trie structure, nodes proactively replenish their caches along the path, therefore preserving and serving the most frequently accessed data. Noticeably, Swarm’s caching mechanism would greatly accelerate the speed with which you can get the data, because of the bandwidth incentives present in the network.

If a node chooses to operate without relying on long-term storage from the network, this approach becomes feasible as long as it is active and consistently replenished. However, it’s important to note that while it can be considered altruistic to some extent, it will inevitably fill the node with data over time. Storage incentives mechanisms ([Postage stamps](https://docs.ethswarm.org/docs/learn/technology/contracts/postage-stamp)) address the long-term compensation for data storage, ensuring that those who store data for others are duly rewarded.

If light clients could request such data from Swarm, which, in turn would either serve it up from cache or, in the absence of a cached copy, request it from different Ethereum nodes (not necessarily light servers), it would considerably alleviate the load on light servers and thus improve the overall user experience.

### More complex queries

Furthermore, a significant portion of DApps, developers, and users aspire to extract state information that transcends the limitations of ETH APIs. They seek to access blockchain data in a manner that reminds of flexible database queries. Functionalities such as filtering for *‘more transactions exceeding 30 ETH’* or identifying *‘stablecoin owners’*, or even seemingly straightforward tasks like *‘transactions by sender’* often necessitate third-party platforms like Etherscan or The Graph.

As a result, there is a growing need for a database bootstrapping solution, one that assures data integrity, verifiability, and reliability. This becomes increasingly relevant for the forthcoming years, as the demand for diverse and tailored data access intensifies.

Notably, Swarm will allow reindexing of data that will allow alternative queries to be responded with verifiable resolution of the query response.

Through the integration of Swarm inclusion proofs, BMT proofs, feeds, and integrity protection structures, Swarm possesses the means to overcome these challenges and validate query responses in a trustless manner. Just as there exists a concept of ‘proof of correctness,’ Swarm is poised to employ a similar methodology for establishing ‘proofs of indexation.’

### Protocol outline with Swarm

The implementation of this approach is straightforward. Ethereum’s state consists of many small binary blobs addressed by their Keccak hashes. The vast majority of these blobs are less than 4 kilobytes in size. Swarm has been specifically engineered to retrieve and cache binary blobs (called “chunks”) that are at most 4 kilobytes in size. While Swarm’s content addressing is different from Ethereum’s, it is relatively easy to define an extension to Swarm that would allow retrieving specific chunk payload by its Keccak hash.

The Swarm network can possibly be used by Ethereum light clients as a state cache and load balancer.

1. When requesting a blob of state data, the light client first turns to Swarm.
2. The Swarm request either gets served from cache or gets routed to the neighborhood that is closest in XOR metric (as per Kademlia routing) to the content address of the blob.
3. The node in the neighborhood that received the request then requests the given blob from the Ethereum node to which it is connected. In case the blob is found and is no greater than 4 kilobytes, it is cached and served as a response.
4. If the node is not found or the blob exceeds 4kB in size, a response to this effect is routed back to the requesting light client, which requests the blob directly from a full client, if applicable.

The caching and serving of state data is incentivised by the bandwidth incentives already present in Swarm, while storage incentives ensure data availability.

This architecture will:

- Eliminate the light server verifiability problem and re-decentralise read access to ETH state for DApps.
- Eliminate the problem of full/archival nodes, allowing any storage node to serve historical requests.
- Unburden ETH miners from syncing traffic with potential improvement on transaction throughput.
- Combined with Swarm’s decentralised database services, serve as a decentralised (backend for a) chain explorer.

In essence, this will allow light clients, browsers, dapps, or developers to query Ethereum’s state more efficiently and trust the result about data structures and indexes.

## SUPPORT TO ALTERNATIVE STORAGE SOLUTIONS

To be realistic, this proposal assumes some integration with execution clients, but always in a way to serve others, championing modularity, while assuming the minimal impact into current clients’ roadmaps. For instance, the Go client can be readily adjusted through a minor modification of the ETH API and state trie-related libraries. A standard / generic hook might be designed by the client team so that the architecture is open and future facing to be extended to IPFS, Arweave, and others.

For alternative storage solutions, this adaptation involves the inclusion of API client calls in the decentralised storage network on top of the existing on-disk storage API calls.

Technical details are available upon request. We actively encourage feedback and comments from the community, and we remain committed to providing comprehensive responses.

## Replies

**fewwwww** (2023-11-09):

As I understand it, we still need to trust the Swarm network. How this solution is called “trustless”?

---

**tonytony** (2023-11-09):

Chunks addresses are based on the hash digest of its data, making it possible to verify the integrity of the data in a trustless fashion.

The underlying storage model of Swarm protects the integrity of content, and the network as a whole defends against blocking or changing access once published.

---

**BirdPrince** (2023-11-09):

Thank you for your contribution. Regarding historical data availability, have you considered making it even more cost-effective and scalable by adding zk proof?

---

**fewwwww** (2023-11-09):

I see.

As for the first point, I think, if it is to be said that it is trustless, then the definition will be different for different users. For the use case of accessing historical data, if the user of the data is a smart contract, then I think that only if the smart contract can directly verify the data can it be interpreted that Swarm is trustless for the smart contract.

- Is it possible to verify Swarm data directly in a smart contract on Ethereum Mainnet?
- What would be the overhead and cost?

For the second point, I think this feature (immutability) is the same as Arweave?

---

**mtsalenc** (2023-11-09):

Something that seems to not be addressed in post is the dependency on Gnosis Chain.

If I understand correctly, for an Ethereum user to use swarm as a service provider and consumer, they will need to run a Gnosis node (as well as the Eth node they already have). In addition, Gnosis is used for (among other things) accounting so a failure on that network affects swarm.

Two questions:

1. Can you confirm the above?
2. Are there plans to launch swarm natively on ethereum mainnet, so users don’t have to worry about Gnosis Chain? Or is there some other plan like GC becoming an L2?

---

**tonytony** (2023-11-13):

Hello. I’m wondering how zk proofs would make historical data availability more cost effective: Zk proofs enhance data integrity while reducing storage requirements, but they are not required to verify integrity in Swarm, afaik. I’m sure I’m missing something, happy to hear your thoughts.

---

**tonytony** (2023-11-13):

There’s a lot to unpack here ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/mtsalenc/48/348_2.png) mtsalenc:

> they will need to run a Gnosis node (as well as the Eth node they already have)

1. Gnosis is the current chain used for the redistribution mechanism to incentivise node operators. So if you are a node operator, you must use it.
2. A Gnosis node running locally is not required at all, unless you want the full privacy and resilience that a private node provides. It is very common to use an RPC endpoint provider. For example GetBlock.

For users running a [lightweight node](https://www.ethswarm.org/build/desktop) or for operators testing a full node, you can also use one of the free public RPC endpoints listed [here](https://docs.gnosischain.com/tools/rpc/).

![](https://ethresear.ch/user_avatar/ethresear.ch/mtsalenc/48/348_2.png) mtsalenc:

> Are there plans to launch swarm natively on ethereum mainnet, so users don’t have to worry about Gnosis Chain? Or is there some other plan like GC becoming an L2?

1. Due to the amount of tx required, a full implementation on the Ethereum mainnet would be very costly today. Keep in mind that the network accounting of Swarm creates “payment channels” between nodes, like the lightning network.

However, there is no strong binding to the current chain, only ease of use due to the base currency (xDAI) and cost-effectiveness. By design, Swarm would be able to work on multiple chains with some adaptations.

---

**tonytony** (2023-11-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/fewwwww/48/9139_2.png) fewwwww:

> Is it possible to verify Swarm data directly in a smart contract on Ethereum Mainnet?
> What would be the overhead and cost?

Please allow me to speak a bit about architecture:

In Swarm, any node address is derived from the owner’s Ethereum address. And the addresses of the chunks (data units) are the Merkle root of the content. This becomes useful if you check them in smart contracts as you can easily create inclusion proofs for the content.

For example, if you want to store a long whitelist (>1000 element), you can store it on Swarm instead of the blockchain, and verify the membership by a smart contract using Merkle proofs.

And if the cost is too high, you can create full rollups on Swarm where the state root is also the content address for the whole state.

![](https://ethresear.ch/user_avatar/ethresear.ch/fewwwww/48/9139_2.png) fewwwww:

> For the second point, I think this feature (immutability) is the same as Arweave?

Swarm’s content represents a different philosophy: persistence is an uploader’s decision, and only his. Not that of the individual nodes or the operators. Content will be immutable and alive as long as the uploader wants.

---

**tonytony** (2023-11-18):

### Offchain data in smart contracts

Indeed in most relevant cases these should be verifiable **on chain**. However, for offchain data, another approach can be taken:

This is the relevant standard for this high level verification protocol [ERC-3668: CCIP Read: Secure offchain data retrieval](https://eips.ethereum.org/EIPS/eip-3668) by Nick johnson. Contracts must include enough information in the `extraData` argument to validate the relevance and authenticity of the gateway’s response.

An ‘optimistic’ variant will also be provided which is based on staked provision of data through swarm and correctness challenges solicited against publishers. In this variant the need for positive verification is absolved after the grace period for challlenges ended.

As for generic data referencing, Beeson (proof-friendly object notation in swarm), verifiable indexing helped by compact inclusion proofs will make it possible to reference any data point or set on swarm with db queries.

This will pave the way to database service networks that are both performant and trustless and with permissionless participation.

---

**quickBlocks** (2023-11-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/tonytony/48/10529_2.png) tonytony:

> A standard / generic hook might be designed by the client team so that the architecture is open and future facing to be extended to IPFS, Arweave, and others.

I feel like this is one of the most important missing thing in the node software. There should be a well-defined standard mechanism for hooking in additional functionality (chained together if there are multiple extensions). We (TrueBlocks) have been advocating this for a while.

---

**awmacp** (2023-11-24):

I think this is could be a powerful application of decentralised storage. However, there are some things left unclear:

- What is the incentive model / market structure? Who would pay to upload and store the state fragments? Is the light client operator expected to pay for retrievals?
- How will the light client discover the blobs? Ethereum state slots are addressed by contract address and metadata field or slot number. Swarm supports custom addressing schemes; since state is mutable, wouldn’t it be preferable to use an Ethereum native scheme rather than content addressing?
- Is the restriction 1 blob = 1 chunk actually helpful? If we consider Swarm as analogous to a hard drive, I would expect that 4KiB physical sectors are separated from applications by a few abstraction layers, usually including a filesystem. Larger blobs (or files) can then be transparently split into chunks rather than having to fall back to an alternative storage backend.

---

**plur9** (2023-12-01):

Thank you for the questions! I can provide more info for the first one:

![](https://ethresear.ch/user_avatar/ethresear.ch/awmacp/48/14044_2.png) awmacp:

> What is the incentive model / market structure? Who would pay to upload and store the state fragments? Is the light client operator expected to pay for retrievals?

But, before answering, it’s important to provide a bit of context (just in case). Swarm started within the Ethereum Foundation (EF) as part of the vision to create the world computer, where Swarm serves as the world’s hard drive, storing blockchain data. In 2020, Swarm graduated from EF, and a year later, we celebrated our launch. At the time of launch, we allocated a portion of BZZ tokens to EF, with the mission that these tokens would be used in the future to support the development and growth of the Ethereum ecosystem. Swarm is now ready, with a big upgrade coming end of the year that takes persistence guarantess to the next level (erasure codes). It’s time that we now start following-up on the initial promise. For this reason, we do plan to do it either-way.

Regarding the cost of data upload and storage, the Swarm Foundation will bear these expenses for the foreseeable future. This financial support stems from the token pool reserved for Ethereum. While it’s challenging to predict the exact duration of this support, we are optimistic it will span at least several years.

It’s also worth noting that the data on our network is linked to postage stamps, which anyone can top up. This feature opens doors for community-driven support, fostering a sustainable model for the long term. We are confident that as the community realizes the value Swarm adds, sustaining this model will become more straightforward.

In essence, Swarm’s initiatives are designed to augment Ethereum, enhancing its resilience and decentralization. This is not about replacing Ethereum but rather about extending its capabilities and ensuring its robustness in the decentralized world.

---

**quickBlocks** (2023-12-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/awmacp/48/14044_2.png) awmacp:

> What is the incentive model / market structure?

I’m going to comment on this, but I don’t really feel qualified, so my comment will be more broad than the particular context of Swarm, but I’ve always felt that people have a massive hole in their thinking related to incentives.

I call that massive hole “usefulness.” The historical Ethereum state is useful. If it were easy to access by individual community members, and they could easily get only that portion of the state that they themselves need for their own unknowable purposes, that would be incentive enough for them to store it (and, if the system worked as it should, store just a bit more than they themselves need, so they can share the state with others).

Incentives don’t necessarily have to be monitory or tokenized. Look at books in a public library. Why do public libraries exist? What’s the incentive model / business plan?

Usefulness.

Historical blockchain state is more like that than some sort of digital product that needs to be “provided by someone.” It should be used-by and provided-by us all through a system that is designed that way on purpose.

(Shameless shill: this is exactly what the [Unchained Index](https://ethresear.ch/t/specification-for-the-unchained-index-version-2-0-feedback-welcome/17406) works.)

---

**awmacp** (2023-12-02):

I agree that it is natural to expect that interested foundations would fund this storage, and perhaps retrievals up to some quota, in the medium term, and that therefore this question perhaps does not need to be addressed now. Still, I think it is important and interesting to consider the long term sustainability of the initiative.

For example, the developers of popular dapps might want a higher retrievals QoS than the Swarm Foundation is prepared to pay for. These power users may choose to directly fund fast retrievals of state used in their frontend. One can imagine models where these payments are structured so as to also contribute to ongoing storage costs.

---

**awmacp** (2023-12-02):

Not all things that are or could be useful end up being funded.

It is true that some data will be sufficiently in demand that people will bear the expense of onboarding and hosting the data, either to use it themselves or to charge others for retrieval. (Note that in the latter case the incentive is still monetary.)

Other data will be used only very rarely or even never, but someone still may want to keep the option to retrieve it. (For example, the balance of a cold wallet, or very old blocks.) For these cases, it isn’t going to be reliable or scalable to assume that some third party is just going to host it on their own dime for ever.

The existence of non-monetary incentives does not mean that it is not useful to consider models for monetary incentives. And it’s not like we lack access to a convenient payments system to implement them ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)


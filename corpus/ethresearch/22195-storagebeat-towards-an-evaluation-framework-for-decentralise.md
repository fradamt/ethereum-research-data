---
source: ethresearch
topic_id: 22195
title: "StorageBeat: Towards an evaluation framework for decentralised storage"
author: awmacp
date: "2025-04-22"
category: Sharding
tags: [data-availability, storage-fee-rent]
url: https://ethresear.ch/t/storagebeat-towards-an-evaluation-framework-for-decentralised-storage/22195
views: 577
likes: 9
posts_count: 11
---

# StorageBeat: Towards an evaluation framework for decentralised storage

# StorageBeat: Towards an evaluation framework for decentralised storage

*By the StorageBeat team: [@awmacp](https://x.com/awmacp), [aata.eth](https://warpcast.com/aata.eth), [v1rtl.eth](https://warpcast.com/v1rtl.eth), Evgeni.*

**TL;DR.** We introduce the beginnings of a framework for systematically evaluating decentralised storage platforms against one another and against traditional, centralised cloud storage services. We introduce summary metrics and methodology for performance measurements, costs, and risk assessments associated with different types of solution, and present a sample application of the framework in a web frontend modelled after L2Beat and WalletBeat.

## Background

Decentralised storage is a technology to outsource the task of data hosting to a peer to peer network of service providers (SPs). Its core offerings are blockchain based payment and storage contract management, cryptographically verifiable service, and provider diversification. This makes it a natural choice for hosting data associated to Ethereum applications.

The decentralised storage landscape is highly fragmented, and community understanding of the offerings and tradeoffs remains patchy. Confusion about what services and guarantees are actually provided by existing decentralised storage infrastructure seems to be widespread. The most well-known services target only niche use cases such as “permanent” storage, publishing rollup blocks, or archival. While low-resource, high value applications like AMMs can afford to use the expensive, highly redundant storage of chain state, nearly all other applications will need to consider lower cost alternatives. However, most off-chain decentralised storage services do not currently have a strong offering for mutable “hot” storage. On the other extreme, the common alternative of delegating data hosting responsibility to a company offering pinning services over the IPFS protocol feels like a centralised cop-out.

We believe that the Ethereum ecosystem would benefit from a common language and systematic methodology for measuring and comparing the features of different decentralised storage systems, both with each other and with their centralised antecedents. In this post, we introduce the elements of such a framework, which we call **StorageBeat**, focusing particularly on the points of departure between decentralised and centralised options. We discuss costs, performance, and risks the prospective customer must consider when deciding which service to use. Our target audience is a sophisticated user (e.g. IT lead of a web3 or web3-curious company) evaluating storage backends to support higher level services such as a software registry or CMDB.

To illustrate how such elements can be used in practice, we’ve gathered data on a selection of representative services and published them as a static website: https://storagebeat.eth.link/. More in-depth exposition and technical details on each element can be found in the notes directory of our GitHub repository: [StorageBeat/notes at main · uncloud-registry/StorageBeat · GitHub](https://github.com/uncloud-registry/StorageBeat/tree/main/notes)

## Costs

Costs of using a storage service can be roughly divided into explicit costs, which are prices quoted by the service provider, and implicit, which are additional costs incurred by the customer’s use of the service. For this version of StorageBeat, we consider only explicit prices.

Our objective is to be able to compare prices for services from a disparate playing field: distributed ecosystems, centralized storage providers, blockchains, and so on. The methods of quoting prices and structuring payments are correspondingly diverse, complicating any attempt at direct comparison. Usage-based pricing systems mean the customer must forecast their data storage and transit needs in order to estimate costs. Prices for decentralised services must somehow be aggregated from their diverse network of providers. Here, we discuss some of the dimensions on which pricing schemes are heterogeneous.

**Fixed and usage-based pricing.** Subscription prices can be fixed, in which case the usage allowance forms part of the service definition and the price is quoted in units of [currency]/[time], or usage-based.

Other services quote a price for each resource. Typical resource fees are **capacity rents**, charged for maintaining data at rest and quoted in units of [currency]/[capacity]•[time], e.g. $/GiB•mo, and **egress fees**, charged for retrieving data from the service and quoted in units of [currency]/[capacity]. All of the decentralised storage services we have seen quote capacity rents; a few also allow for egress (or *retrieval*) fees.

**Banded Pricing**. Many tradcloud services charge for resource usage in a **banded** system.  For example, a client may pay nothing for the first $100$GiB of egress and a fixed rate p per GiB for subsequent usage. Exotic variants also exist: for example, Backblaze calculates its bands in fixed proportion to the amount of capacity used. We don’t know any examples of banded price quotes in decentralised storage.

**Marketplaces.** In some decentralised ecosystems, notably Filecoin and Sia, each peer must quote competitive prices for capacity and egress. It is therefore not meaningful to talk of “the price” of Filecoin and Sia storage, though it can still be useful to summarise the marketplace with various market price constructions.

**Permanent storage.** Some storage services quote a single upfront payment for “permanent” or “lifetime” data storage, with the latter term appearing in tradcloud and the former appearing on decentralised platforms. Compared to tradcloud, such quotes seem to be more common in decentralised storage. The price of such a service is expressed in units of [currency]/[capacity]. For the purposes of comparison with services priced in terms of capacity rent, this upfront payment must be amortised to give quantities in the usual units of [currency]/[capacity]•[time]. In StorageBeat, we use a straight line method to amortise and give a **normalised capacity rent** for lifetime contracts. More generally, clients with concrete use cases should amortise over the period of expected usage of the service.[[1]](#footnote-53980-1)

**Prepayment.** In tradcloud, fixed capacity services such as Dropbox may charge at the beginning of the billing period. Prepayment also invariably happens up front in decentralised services, arguably for similar trust reasons to its use in DeFi which depends heavily on escrows. On the other hand, elastic tradcloud services with usage-based pricing schemes necessarily take payments at the end of the billing period.

## Performance

Performance of storage services is assessed by running benchmarking experiments based on workloads of the type the benchmarker expects to be using in his application. The purpose of benchmarking is generally to predict whether performance will meet requirements, and possibly to optimise a cost-performance tradeoff.

Most of the basic considerations in benchmarking decentralised services are the same as for traditional cloud. It is beyond the scope of this post to discuss the many dimensions of cloud benchmark design and implementation.[[2]](#footnote-53980-2) Instead, apart from a comment on nondeterminism we simply describe the statistics we have chosen for StorageBeat. For further details of the rationale we developed for our experiments, see [./perf/README.md](https://github.com/uncloud-registry/StorageBeat/blob/cf198ef118423d2f027bee0b79236f71d16304eb/perf/README.md).

While **nondeterminism** in the state of external systems is already an issue for tradcloud services, there are reasons to expect qualitative differences in the shapes of distributions of performance metrics in decentralised storage. First, in principle, the provider diversification offered by decentralised storage systems should help reduce variance in performance measurements. On the other hand, the lower barrier to entry in decentralised storage markets probably means the variability for each individual provider is much higher than tradcloud hyperscalers. In practice, we observe higher variance in measurements of the less mature decentralised storage platforms.

Since tracking and reporting performance across many workloads and control scenarios is rather complex, for publicly communicating performance measurements it is helpful to quote simple summary statistics. In the StorageBeat website we have quoted estimates of expected **latency** (a.k.a. time to first byte) and **steady state throughput**[[3]](#footnote-53980-3) (SST). For reasons of benchmark portability, we estimate these as the request completion time for a very small file and the mean download speed of a request for a large file, respectively.

The **error rate** and **timeout rate** (given a fixed time limit) are both important and easy-to-understand measures of availability. For traditional cloud service providers, error code rate limits (specifically server-side HTTP 5xx codes) are usually guaranteed by an SLA which offers account credits as compensation if limits are exceeded. We haven’t yet begun systematically measuring these rates on StorageBeat.

In future work, we also aim to introduce systematic measurements of client-side resource usage.

In our experiments, we used the open-source tool [Artillery](https://github.com/artilleryio/artillery) to collect request completion times for different workloads. More details are available in our GitHub repo under the [perf/](https://github.com/uncloud-registry/StorageBeat/tree/main/perf) directory.

## Risk

Each storage service is associated with a set of risks that something will impair our use of the service or increase our costs in the future. Weighing up these risks is part of the job of selecting which service to use. Part of the job of StorageBeat, then, is to build out a risk framework for storage services. Since risk analysis requires us to consider not only what service ought to be delivered, but also all the reasons that it might not, this risk framework actually comprises the bulk of the task.

Since the core offering of decentralised storage is the ability to mitigate counterparty risks through **provider diversification**, a good risk framework is particularly essential to communicating its selling points vis-à-vis tradcloud storage.

We attempt a rough classification of risks, risk measurement, and mitigation strategies in centralised and decentralised storage services.  In terms of the functioning of the storage service itself, we must consider the following questions:

- Will I be able to use the service in the future?
- Will the service function correctly in the future?
- If the service no longer suits my needs in the future, how easily can I migrate?

### Availability

If we aren’t able to use the service, the service is *unavailable.* Unavailability can be local to the data being requested, or global in that it affects the entire service. It can also be temporary or permanent.

The risk of global outages can be mitigated in the following ways:

- SLA. A service-level agreement provides a definition of the service and often an indemnity for some type of service failure. Tradcloud services typically offer compensation for an error rate exceeding a certain limit, e.g. 99% in a five minute window.[4][5] On the flip side, Filecoin customers may be compensated in the event of a durability failure in the form of early termination of a storage contract.
In StorageBeat we report whether we could find an SLA, whether it carries an indemnity, and summarise what is covered.
- Survival analysis. Global, permanent outages arise when a service provider ceases operations. To mitigate this, estimate the survival probability of each service provider over the desired service period and allocate to providers with better scores.
- Diversification of service providers.

Backend diversity. When data is split and distributed among multiple backend storage providers, the risk of correlated failure is reduced. The effect is stronger when providers are diverse along multiple axes (jurisdiction, locality, technology, corporate structure, etc.).
- Gateway diversity. A single backend service can often be accessed through multiple gateways without the need for replicating capacity rental; gateway diversification can therefore be a cost-effective route to risk reduction. For example, one can access many decentralised storage services through a third party web gateway for convenience, but in case such is not available, the p2p network is available as a fallback. The p2p network may also itself be considered a diversified network of gateways.

We don’t have a simple numerical measure that captures diversification, but measuring the entropy of some “market share” distribution — such as capacity share per provider — can give a preliminary indication.[[6]](#footnote-53980-6)

We turn now to the risk of specific data loss, or **durability** risks.[[7]](#footnote-53980-7)

- Storage proofs. A typical feature of web3 storage systems is that a system of cryptographic proofs provides some assurance that data remains available to the service provider at the time the proof is constructed. Attaching explicit incentives to storage proof publication is supposed to cultivate a population of providers who make efforts to retain access to client data in the future so that they may claim these incentives. Incentives may be in the form of revenue or the threat of collateral seizure, a.k.a. slashing.
In the StorageBeat website we simply report the developers’ own name for the storage proof system each service uses. In future, it would be more useful to develop a detailed comparison framework that clarifies the risk vectors from a user-centric perspective.
- Durability reporting. Storage services ought to essentially never lose data. It can therefore be challenging to put a credible number to object loss rate on reasonably stable services. Tradcloud services report durability on the “nines” basis, where object loss rate per year is bounded by a power of ten. Though the basic methodology to achieve these numbers is documented,[8] such reports are not usually backed up by evidence or legal guarantees.[9]
In decentralised cloud, the global rate of node failure or data loss can be observed by tracking missed storage proofs. The tradcloud methodology could then be applied to extrapolate the observed rate to a formal probability of losing a replicated or otherwise expanded object distributed over the node population.[10] As of yet we haven’t carried out any such calculations.

### Correctness

The question of *correct functioning* depends heavily on the details of the service definition.  Some basic expectations are as follows:

- Successfully uploaded content will be available for download for the extent of the contract duration.
- Retrieved content wil be “correct,” where for a distributed system correctness is defined by a database consistency model. There are various consistency models arising in practice in decentralised storage:

For immutable storage, consistency simply means that the data retrieved under an address is exactly what was uploaded. In practice, this consistency can be validated with a content commitment (checksum, hash). If storage is content-addressed, as is often the case for decentralised storage, then the validation of such commitments is built in to the basic infrastructure.
- Tradcloud storage offerings typically offer strong consistency, which guarantees that retrieved data always reflects the most recent update, where recency is understood according to some globally (within the service) defined ordering.
- Blockchain state, or other decentralised mutable storage offerings such as Swarm feeds, offers a more exotic consistency model that depends on the mechanism by which the system settles on transaction inclusion and ordering. Finding ways to report the consistency properties of such systems is an open area of research.

There will be no unauthorised access to the services (for example, third parties viewing the data). A major part of this is **privacy**, which pertains not only to unauthorised reads but also to leaking information about authorised usage. Though there is undoubtedly much to say on this subject, we have not investigated it deeply.

### Generic service risk categories

Considerations within these categories apply to all decentralised services, not only storage. As such, they are already familiar to users of blockchain services.

- Counterparty risk. With centralised services, all risks are counterparty risks. Cryptoeconomic incentives, smart contract enforcement, and counterparty diversification allow many counterparty risks to be mitigated on decentralised platforms.
- Contract risk. Risk that the terms of the agreement will not be respected or enforced, or that customer expectations do not reflect the enforced terms. For centralised services, they are counterparty risks. For decentralised services, they may be replaced with smart contract risk, which is a risk of incorrect implementation of the contract semantics.
- Financial risk. This includes price risk and currency risk. In decentralised services, both service price and, if fees are priced in a volatile asset, exchange rate is often highly volatile. In the case of sharp price rises, it may be no longer viable to continue with the contracted service, incurring a migration penalty. Similarly, if the fee asset is volatile, the client may need to maintain a balance of the asset as a hedge against future price rises, incurring a currency risk penalty. The volatility of these series is an easily reported metric for price and currency risks.

## What now?

We have listed elements of costs, performance, and risk analysis pertinent to the evaluation of storage services. For most of these elements, we have barely scratched the surface of how they can be analysed, presented, and used in decision making.

- For teams that build or want to build with off-chain storage — what do you need to know? What’s missing? What resources have you used to gather information?
- For teams building decentralised storage systems — let’s work together to further refine these metrics, develop measurement methodologies, and forge a common language.
- What we’d like to see: more hybrid models! Centralised cloud services that provide storage proofs! Decentralised platforms with an availability SLA and (something approaching) strong consistency for mutable data!
- Topics for future research:

Research ways to measure provider diversity through clustering and geolocation techniques. Encourage larger scale operators to voluntarily declare their addresses in the name of transparency.
- Develop durability model and carry out systematic measurements of durability on decentralised systems for which it makes sense.
- More work is needed on consistency, authorisation, and privacy, which we have barely addressed. If you are an expert in one of these fields, please reach out so we can work together to enhance our models.

## Acknowledgements

The StorageBeat team ([@awmacp](https://x.com/awmacp), [aata.eth](https://warpcast.com/aata.eth), [v1rtl.eth](https://warpcast.com/v1rtl.eth), Evgeni) was supported by Ethereum Foundation ESP grant FY24-1744.

We thank Rahul Saghar, Viktor Trón, and the Codex Research team for feedback and discussions.

1. Long-term arrangements like these are particularly exposed to the risk of provider failure. See Risk. ↩︎
2. For a textbook treatment of the subject, see Cloud Service Benchmarking: Measuring Quality of Cloud Services from a Client Perspective | SpringerLink ↩︎
3. steady-state throughput – ATIS Telecom Glossary ↩︎
4. Service Level Agreement – Amazon Simple Storage Service (S3) – AWS ↩︎
5. See also ./notes/risk/sla.md. ↩︎
6. See also ./notes/risk/provider.md. ↩︎
7. See also ./notes/risk/durability.md. ↩︎
8. Cloud Storage Durability: What Do All Those 9s Mean? ↩︎
9. See $\S$6 of https://www.hetzner.com/legal/terms-and-conditions/ ↩︎
10. Codex Docs ↩︎

## Replies

**Julian** (2025-04-22):

Hi, thanks for the interesting post and website! Have you explored connections to statelessness? Statelessness is a planned upgrade to Ethereum, removing the need for attesters to store the state. The logical next question is, who should store it instead? Decentralized storage solutions could be a useful tool here. Storage or state providers need to keep up with the tip of the chain to be useful for sending transactions on blockchains. Therefore, another important dimension is whether the storage provider can provide state at the tip of the chain fast enough to send a transaction reliably.

---

**leobago** (2025-04-22):

Hi, thanks for the post. It is a nice first step towards a standardized way to evaluate storage solutions in Web3. There is still a lot of things to do, moving forward, as you admit in the post.

One thing that I would remove is the correctness section, in has three main points:

- The first one is directly related to the availability section just above
- The second is directly related to the durability section just above.
- The third one is about privacy and security, which I think is a topic that is a bit overlooked here, so I would make a whole new section for that, Security and Privacy.

Regarding financial risks, these are important to study. If storage providers have a margin of, for example, 25% (quite large), but the token fluctuations are over 30%, then price volatility can quickly eat the margins and make storage providers unprofitable. A solution to that is to establish prices in any stablecoin, but then pay in tokens the equivalent to the stablecoin. This solves some problems but not all.

Indeed, several platforms use tokens as collateral for storage providers, so that if they misbehave, they get slashed. Token price volatility can dramatically reduce the cost of slashing due to high volatility. When this happens, storage providers have nothing to lose anymore, and we go back to the “nothing at stake” problem, which can lead to massive node exits, hence high chances of data loss.

---

**awmacp** (2025-04-23):

Hi, thanks for bringing this up. We’ve thought about storing state snapshots as a clear use case of decentralised storage, though speaking for myself I haven’t kept up with the SOTA of statelessness or light clients. As you say, this would have stricter performance requirements than bootstrapping a stateful node. It would be helpful to know concrete of workload completion time and error rate constraints expected to be required for serving tip state to stateless clients; is this something you can tell me more about?

I’ve got Portal Network on my radar as an application specific storage service aimed at roughly this use case, but I don’t know much about it — would be good to get it a row on StorageBeat.

In general, it looks like the decentralised storage market has a lot of catching up to do in serving any kind of mutable, hot database application, which is unfortunate given that this class of use cases probably covers most of the potential customer base of storage services.

---

**awmacp** (2025-04-23):

Thanks for this feedback. The categorisation in the risks section is rather preliminary and some of the categories overlap, as you observe.

![](https://ethresear.ch/user_avatar/ethresear.ch/leobago/48/18496_2.png) leobago:

> One thing that I would remove is the correctness section, in has three main points:
>
>
> The first one is directly related to the availability section just above
> The second is directly related to the durability section just above.
> The third one is about privacy and security, which I think is a topic that is a bit overlooked here, so I would make a whole new section for that, Security and Privacy.

- I agree that the first bullet point here is a matter of availability. It is replicated here because it also corresponds to “correctness” in the sense of “respecting the specific storage contract (including duration).” But perhaps that distinction is somewhat artificial and this point basically falls under “SLA” rather than “correctness.”
- Disagree: consistency does not fall within the subject of durability (a.k.a. future availability). A database can be consistent (under some given model), but not available, or vice versa.
- Agreed, but we don’t yet have enough to say about it to fill out a whole section.

In summary, perhaps this section could be reduced to a discussion of consistency and privacy/security factored out into its own section in a later iteration.

![](https://ethresear.ch/user_avatar/ethresear.ch/leobago/48/18496_2.png) leobago:

> Regarding financial risks, these are important to study. If storage providers have a margin of, for example, 25% (quite large), but the token fluctuations are over 30%, then price volatility can quickly eat the margins and make storage providers unprofitable. A solution to that is to establish prices in any stablecoin, but then pay in tokens the equivalent to the stablecoin. This solves some problems but not all.
> Indeed, several platforms use tokens as collateral for storage providers, so that if they misbehave, they get slashed. Token price volatility can dramatically reduce the cost of slashing due to high volatility. When this happens, storage providers have nothing to lose anymore, and we go back to the “nothing at stake” problem, which can lead to massive node exits, hence high chances of data loss.

The financial risks you mention are mostly those affecting providers, rather than clients (the target audience of StorageBeat). So while relevant, from our perspective analysis of these risks feeds into either survival analysis of providers or, in the example of penalties being too low, dishonest counterparty risk. The financial risk faced by clients directly is often of a much milder nature, but still important. For example, a client who must commit to store a lot of data for a long time (e.g. for compliance purposes) will be exposed to storage and currency price fluctuations.

---

**Julian** (2025-04-24):

Nice to hear there is interest in possibly adding data related to statelessness. For strong statelessness, users need to provide a full witness of their transaction, which is the state they interact with + a proof that this state is part of the state tree. I think a user could comfortably submit its transaction if it got the witness within at the most 1/2 or 2/3rds of the slot time so about 6 or 8 seconds today. The state provider should then be synced with the new state of the chain and provide the witness. This seems pretty doable to me, but it may be more difficult with faster slot times.

Portal Network would be great to add to StorageBeat!

---

**qzhodl** (2025-04-25):

Thank you for this great initiative! As the developer of EthStorage ([ethstorage.io](http://ethstorage.io)), I’d love to see EthStorage included on the **StorageBeat** dashboard. For context, EthStorage is an Ethereum-native decentralized storage protocol (a Layer-2 system) optimized for verifiable and mutable data storage. In practice, it provides a smart-contract-accessible key-value store where data availability is backed by Ethereum (via EIP-4844 BLOBs), but bulk storage is kept off-chain for scalability. This design makes EthStorage well-suited to handle “hot” (frequently updated) data with cryptographic verifiability. We’d be happy to help the StorageBeat team with any metadata, metrics, or dimensions needed to accurately profile EthStorage on the dashboard. Feel free to reach out if we can provide data points or assist in the integration process.

## Thoughts on Performance Metrics and Latency Diversity

The **performance** dimension you discussed is both important and nuanced. Measuring download latency and throughput in decentralized storage systems is challenging, not because it’s invalid, but because the ecosystem is heterogeneous. EthStorage’s model for data retrieval is quite similar to Ethereum’s full-node RPC landscape. There isn’t a single “endpoint” that defines user experience; instead, there’s a spectrum:

- Community/Public Endpoints: Just as Ethereum has public RPC nodes (often run as a public good), EthStorage can be accessed via community-run endpoints. These are open and decentralized but may have variable latency depending on load, location, and volunteer resources.
- Third-Party Providers: By analogy to Infura or Alchemy on Ethereum, third parties can offer optimized EthStorage gateways or RPC nodes. These might deliver faster responses or CDN-like caching at a premium. Users who prioritize low latency often gravitate to these services (or run their own optimized nodes), whereas cost-sensitive users might stick with the free/community options.
- Application-Specific Nodes: Many dApp teams run their own Ethereum full nodes for reliability; similarly, an application can run its own EthStorage node (or cluster of nodes) close to their backend. This ensures consistent performance for that app’s users, at the cost of infrastructure overhead for the team.

The result is a **wide range of latency and speed characteristics** across the network. Some users might experience sub-second time-to-first-byte if they’re hitting a well-provisioned node, while others might encounter multi-second (or occasionally higher) latencies through a congested public node. This variability echoes your observations that decentralized platforms can exhibit higher variance in performance than traditional cloud services. From my perspective, this diversity is both a **strength and a challenge**. It’s a strength because no single provider can become a point of failure or censorship – the resiliency and decentralization benefits are maximized. If one gateway is slow or down, the data is still available from other nodes or networks. However, it’s a challenge in that the user experience isn’t uniform. Unlike an AWS S3 where performance is fairly predictable, a decentralized storage user’s experience will depend on “who” serves their request.

It’s worth noting that **other decentralized storage systems face similar trade-offs**. Filecoin, for example, augments its storage network with retrieval services like IPFS/Pinata gateways to improve latency. The fact that billions of weekly IPFS content requests were being funneled through a single gateway shows how much demand relies on a fast entry point. Arweave provides another case: many apps rely on the [Arweave.net](http://Arweave.net) gateway or community proxies to fetch data quickly, or else each user must run a full Arweave node to retrieve content, which isn’t practical for most. In short, **performance metrics** in our space must be interpreted with context. A “slow” average download time might indicate that many users are using the free, fully decentralized path (which maximizes censorship-resistance), whereas faster times might be achievable via specialized services. I appreciate that StorageBeat is attempting to capture these nuances. Perhaps a useful approach is to report a range or percentile distribution for latency, as you’ve done, and maybe annotate whether measurements were via default public infrastructure or accelerated gateways.

## Mutability and “Hot” Data Use Cases

I was especially interested in your discussion about **mutable “hot” storage**, since that’s exactly EthStorage’s focus. You noted that most off-chain decentralized storage services today don’t have a strong offering for mutable hot data, effectively a gap between expensive on-chain storage and cheaper off-chain solutions. EthStorage is built to fill this gap, enabling use cases that need frequent updates and immediate availability while still being verifiable and decentralized. For example, we imagine scenarios like dynamic NFT metadata (where an NFT’s content or attributes evolve over time), fully on-chain games that need to store and update world state or player data, social networks or microblogging platforms where users are posting content that must be stored persistently but updated often, and even decentralized app front-ends or config data that might change continuously. These are “hot” in the sense that the data isn’t static – it’s written and read often, and users expect the latest version on demand.

I’m curious what real-world use cases **you** (the StorageBeat authors) find most promising for this kind of mutable storage. Are there specific applications or industry verticals that you believe are primed to benefit from decentralized mutable storage? It would be great to hear your perspective on this. We at EthStorage have some ideas (like the ones above), but the space is broad. Any insight into which use cases have the biggest pull for “hot” decentralized storage would be valuable. This is an area we’re actively exploring, so I’d love to continue the discussion or even collaborate on diving deeper into these scenarios.

Overall, thank you for kickstarting a much-needed evaluation framework. **StorageBeat** is going to help projects like ours benchmark and communicate our capabilities in context. We’re excited to contribute and learn from this effort!

---

**awmacp** (2025-04-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/qzhodl/48/9870_2.png) qzhodl:

> The performance dimension you discussed is both important and nuanced. Measuring download latency and throughput in decentralized storage systems is challenging, not because it’s invalid, but because the ecosystem is heterogeneous. EthStorage’s model for data retrieval is quite similar to Ethereum’s full-node RPC landscape. There isn’t a single “endpoint” that defines user experience; instead, there’s a spectrum:

Yes! We tried to make that breakdown clear by clarifying both the storage service and gateway used to benchmark downloads (e.g. Arweave + [arweave.net](http://arweave.net) RPC). In future we envisage multiple rows per backend corresponding to the various retrieval pathways.

![](https://ethresear.ch/user_avatar/ethresear.ch/qzhodl/48/9870_2.png) qzhodl:

> I’m curious what real-world use cases you (the StorageBeat authors) find most promising for this kind of mutable storage. Are there specific applications or industry verticals that you believe are primed to benefit from decentralized mutable storage? It would be great to hear your perspective on this. We at EthStorage have some ideas (like the ones above), but the space is broad. Any insight into which use cases have the biggest pull for “hot” decentralized storage would be valuable. This is an area we’re actively exploring, so I’d love to continue the discussion or even collaborate on diving deeper into these scenarios.

I wouldn’t say we yet have a concrete position on the most important use cases for mutable offchain storage, but given StorageBeat’s stated purpose of providing a user-facing resource I think this is an important conversation to have!

The most evident use cases at the moment are, as you say, offloading storage for smart contracts and unlocking more data-hungry applications. Smart contract developers today are used to dealing with the constraints of onchain storage so may not even consider applications requiring data on the scale of, say, hundreds of megabytes. The obvious demand source for this kind of larger scale would be media, but even financial applications can end up in this range. For example, a standard fungible token implementation with millions of users runs to the megabyte range, to say nothing of the “next billion” that Ethereum applications are supposed to eventually handle.

The benefits of decentralised storage to tradcloud customers who are otherwise not necessarily considering blockchain infrastructure is perhaps a harder sell that I imagine would come further down the line, once the crypto-native use cases are validated a bit more.

---

**awmacp** (2025-04-28):

So if I understand correctly, in the statelessness use case the requirement is that a user fetches a witness — presumably a very small amount of data, request time latency dominated — in under 6 seconds. And that has to serve N requests per slot where N is the number of transactions that go in the slot, so a couple of hundred today, hopefully more (thousands?) in the future as the L1 scaling roadmap progresses. The success rate bounds people’s ability to get transactions in in their desired slot, so the service should seek to uphold a few nines of availability SLA (99%? 99.9%?)

Would be cool to thrash out some details on the requirements with someone working on these upgrades. It sounds like an important application for decentralised storage teams to know about.

---

**patrickwoodhead** (2025-05-07):

Thanks for this great post. My team at Checker Network has been working on measuring Filecoin’s service levels for the last year. In particular, the retrieval success rate and retrieval latency of data on Filecoin. We have recently done the same as a PoC for Arweave storage nodes (not gateways) and Walrus aggregators.

That’s great that you clarify whether you are measuring the storage nodes themselves or the gateways. This is something that creates vastly different results when it comes to retrieval success rate.

The Checker Network collects performance data on storage networks from clients all over the world. It would be cool to discuss whether you would be interested in using the data we create to populate the Storage Beat dashboard.

More generally, happy to advise on how to include Filecoin in the Storage Beat leaderboard as well as IPFS.

---

**awmacp** (2025-05-20):

Hey Patrick! We welcome contributions and I’d love to talk about getting some Filecoin data on there. The main reason we didn’t attempt any Filecoin measurements is because we expect a lot of heterogeneity depending on which SPs are used for retrieval and we weren’t sure how best to aggregate and present these data. Would love to hear your insights.

I’ve sent you a DM so we can explore this further.


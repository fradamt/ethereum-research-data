---
source: ethresearch
topic_id: 18527
title: Allowing validators to provide client information privately—a project by Nethermind Research and Nethermind Core
author: jorem321
date: "2024-02-01"
category: Consensus
tags: []
url: https://ethresear.ch/t/allowing-validators-to-provide-client-information-privately-a-project-by-nethermind-research-and-nethermind-core/18527
views: 3745
likes: 18
posts_count: 4
---

# Allowing validators to provide client information privately—a project by Nethermind Research and Nethermind Core

(Team’s Twitter handles: @0xjorgeth, @M25Marek, @rmzcrypt, [@Smartprogrammer](/u/smartprogrammer).)

Understanding the distribution of Ethereum’s execution-layer and consensus-layer clients used by validators is vital to ensure a resilient and diverse network. Although there are currently methods to estimate the Beacon Chain’s client distribution among validators, the same cannot be said about execution client distribution. Also, there are no standard means of anonymously showcasing which EL and CL clients are being utilized by validators.

Therefore, as part of the Ethereum Foundation’s [Data Collection Grants Round 2023](https://esp.ethereum.foundation/data-collection-grants) which ran between last September and October, an interdisciplinary team involving Nethermind Research and Nethermind core developers received a grant to work on the project “Allowing validators to provide client information privately”. This project aims to research and design a mechanism to submit and extract this crucial data while potentially avoiding compromising user anonymity and network performance. This project aims to research and design a mechanism to submit and extract this crucial data while potentially avoiding compromising user anonymity and network performance.  Our work relates to the [grants round wishlist](https://notes.ethereum.org/@drigolvc/DataCollectionWishlist) items “Using ZK for data collection allows validators to provide information while staying anonymous” and “Improved Validator crawling”.

Currently, we see widespread interest in the subject, especially in light of recent client bugs, which have brought client diversity to the forefront of discussion and led our Ethereum community to reflect upon the radically different consequences that a consensus bug in a supermajority execution client would have. As an example of the proposals that have been motivated by this topic, there is currently a [PR](https://github.com/ethereum/execution-apis/pull/517) by [@ethDreamer](/u/ethdreamer) on Ethereum’s execution APIs, suggesting some protocol changes to facilitate exposing client data on the graffiti field of a block.

The purpose of this thread will therefore be twofold:

- Share with the community our current impressions on the subject, along with research directions we are thinking of undertaking (and discarding).
- Provide a space for discussion which allows us to keep the community informed on our progress, and welcome feedback throughout all stages of the project.

# Objectives

The objectives of our research are as follows:

1. Analyze the technical possibilities for validators to report on (or make visible) EL and CL data, while leveraging existing infrastructure and without compromising performance or security.
2. Identify techniques to anonymize the methods found in Objective 1.
3. Compare the solutions found in Objective 1 and their anonymized versions found in Objective 2 (when applicable) in light of accuracy, security, privacy, and performance concerns.
4. Present our research findings to the Ethereum community and advise on the best option found in the analysis.
5. If the option found in Objective 4 requires protocol changes, prepare an EIP detailing the implementation of this mechanism, incorporating the community’s feedback where appropriate.

# Background

Our research begins by briefly analyzing the current methods for measuring client diversity in Ethereum, along with their weaknesses. In general, we cluster these methods into three main categories:

1. Use of heuristics or machine-learning tools. This approach is used by Blockprint to “guess the consensus client for a block, based on the similarity of that block to others in its training data.” Note that this approach cannot determine the execution client associated with a validator, only the consensus client. This is due to the widespread use of MEV-Boost and the expected transition towards PBS architectures in general, which make it so that there is no fingerprint of the execution client being run by the block proposer in the structure of the block.
2. P2P crawling. A technique used by Miga Labs and Ethernodes; involves running a specialized node (or “crawler”) in Ethereum’s P2P networks to identify the clients being used by the other nodes. Although we can gather data from both consensus and execution clients, this method suffers from a flaw for our purposes: it finds the client distribution among all Ethereum nodes in the network, but it does not weigh these nodes according to the number of validators connected to them. It is the client distribution associated with validators that is important to the health of the Ethereum network, given that these determine consensus.
3. Surveys. By consulting with large node operators and staking pools, we can aim to obtain a large sample of the client distribution of Ethereum validators. Unfortunately, it can be hard to gauge the accuracy and validity of the reported data and whether the utilized sample is representative. This method is used by https://execution-diversity.info, which also powers https://clientdiversity.org/.

Having noted the current room for improvement in these techniques, a natural starting point is building upon extant methods, while brainstorming other possible directions. Approaches to study include but are not limited to:

1. Making client data visible in proposed blocks. Although we cannot follow Blockprint’s heuristic approach to obtain client diversity data for execution clients, we can still source our statistics from block proposers (like Blockprint does) if we explicitly include their client diversity data in the block structure. An example would be pushing this data in the graffiti field during block proposing, which can then be readily collected from the blocks.
2. Improving the reliability of crawling methods. Are there any acceptable changes to clients that would facilitate the work of crawlers looking to estimate the client distribution amongst validators (not nodes)? An example would be allowing other nodes in the P2P network to gather data on the number of total validators connected to a single node. In this way, crawlers could weigh the contributions of each node to consensus accordingly.
3. Dedicated sub-protocol for client data collection. Another approach would involve designing a separate sub-protocol for validators to share client data, which would run in parallel to the consensus protocol. This would be a streamlined, client-based alternative to a manual survey, which would aim to achieve better privacy guarantees. Moreover, we aim to isolate this mechanism from Ethereum consensus as much as possible, to avoid any additional demands on speed and performance.
4. Any other approaches found during our research with the potential to lead to a solution will be included as well.

# Preliminary analysis

Although our research project has just started, we have internally discussed some of our initial impressions on the aforementioned directions, which are given below. For each direction, we highlight expected protocol changes along with the challenges to solve.

## Making client data visible in proposed blocks

A straightforward approach here would be for Ethereum consensus clients to include the consensus/execution client pair being used by a validator at the time of proposing a block, via the graffiti field.

**Required protocol changes**

- EngineAPI method for the CL client to retrieve the EL client details. We note that there are already discussions on the need to implement this feature.
- (Optional) Clients could agree on an encoding to be used when pushing data to the field, which represents the EL/CL combination. For example, the aforementioned PR by @EthDreamer suggests a two-letter abbreviation for each client.

**Challenges**

- How should this method deal with multiplexed architectures? For example, we have tools like ExecutionBackup, where multiple EL clients are connecting to the same CL client. Another example is given by tools such as Vouch, which make it hard for a validator to pinpoint a specific CL and EL client being run under the hood. Finally, we can consider the challenge of reports coming from DVT-based validators. It would be advisable to have a way for validators to report when they are running with multiple ELs or CLs concurrently
- How can we add anonymity to this method? Our team is working on this and assessing some ideas to this end.

## Improving the reliability of crawling methods

Let us analyze modifications to Ethereum clients so that a crawler can obtain the *validator* client diversity distribution, not just the node distribution.

**Required protocol changes**

- We would require nodes to disclose to crawlers the number of validators connected to them, among other changes.

**Challenges**

Below, we share some reasons why we believe this is a bad idea:

- It is unclear how this method would handle infrastructure such as load balancers or Distributed Validator Technology. These approaches can have the same group of validators attached to several nodes at once so that crawling the network would result in counting the same validators multiple times.
- Moreover, if users are allowed to self-report the number of validators connected to their node, then they can easily skew the client diversity data by declaring artificially large numbers of validators. Thus, this validator count should be supported by some form of cryptographic evidence, such as attestations or an adaptation of a proof-of-validator.
- There are privacy concerns in disclosing the number of validators attached to a node. This could signal nodes of high importance (when the validator count is high), making them prime targets for a DoS attack.

Due to the above, we are unlikely to suggest pursuing this approach.

## Allowing nodes to listen to client diversity data through the gossip network

The analysis above discourages us from pursuing crawlers that use the [request/response domain](https://ethereum.org/developers/docs/networking-layer#request-response) of the P2P network. Can we leverage Ethereum’s [gossip domain](https://ethereum.org/developers/docs/networking-layer#gossip) instead?

We are analyzing the possibility of defining a new [GossipSub topic](https://docs.libp2p.io/concepts/pubsub/overview/?#design-goals) so that validators (or a randomly chosen subset of them at a time) can periodically gossip their client diversity data. In this way, any client in the P2P network can get data by subscribing to this topic.

**Required protocol changes**

- EngineAPI method for the CL client to retrieve the EL client details, so that the gossiping can take place on the consensus layer entirely.
- The introduction of new GossipSub topics—e.g. client_data_{subset}—where users can broadcast their client data for it to be aggregated by any interested listener.
- Once more, it would be beneficial for clients to agree on an encoding to represent the EL/CL combination (instead of using plaintext), to minimize the data that is sent.

**Challenges**

- How can we make sure that the validators publishing data in this topic represent a statistically significant sample of the network? We could, for example, take inspiration from the mechanism of aggregator selection. We could look into gathering this data e.g. only from the validators chosen as part of a given attestation subnet per epoch.

This would also help limit the rate at which data is gathered to avoid needless overload of the network.

Gathering this data should impact consensus as little as possible. If the data sample is related to attestation subnets, then we could gossip the data during slots when the validators are not required to gossip their attestations.

There is also the question of how to address privacy and anonymity concerns via the method above, which leads us to the next approach.

## Implementing a dedicated private voting scheme for client diversity data

A voting scheme is a digitalized system designed to efficiently vote and count ballots during elections, aiming to streamline the electoral process, enhance accessibility, and minimize errors. In private voting schemes, the primary focus is ensuring maximum confidentiality and anonymity for individual votes. This is achieved by implementing cryptographic techniques like homomorphic encryption and secure multiparty computation, preserving voters’ privacy. Private voting systems utilize robust protocols, enabling citizens to cast their ballots electronically while maintaining the secrecy of their choices.

In our case, we are trying to collect client information (as a vote) from the Ethereum users without revealing information about the users. This problem seems to be solved using a private voting scheme if we can deploy a private voting protocol that utilizes Ethereum users as voters. As our first iteration towards using private voting schemes, we look into lightweight protocols that do not require a dedicated blockchain to run, so that they are more adaptable to the P2P context. In this vein, we are analyzing how to adapt the Belenios voting scheme to gather client diversity data.

**Required protocol changes**

Various cryptographic building blocks and structures would need to be implemented. Such a protocol will require, among other things:

- A distributed key generation protocol amongst the parties that are chosen as decryption authorities.
- The ability for validators to encrypt their votes via a homomorphic encryption scheme (e.g. El-Gamal).
- The infrastructure for voters to generate zk-proofs of their votes’ validity.

**Challenges**

- Which parties are best suited to play the role of decryption authorities? Note that they can prevent the voting results from being known if enough of them decide not to participate.
- Is checking the validity of the votes a bottleneck? Can this protocol be realistically executed without putting excessive computing/networking demands on validators? Additional analysis of the proving times and message sizes is currently underway.

# Towards a rubric for assessing the best solution

As we develop our ideas into concrete approaches, we will need a rubric to assess the merits of each solution, as part of Objective 3. Here is a preliminary rubric that encompasses various points relevant to the problem:

- Complexity: how many changes to the protocol/clients are required? Ideally, we want solutions that are not overly invasive with regards to modifying key components of the Ethereum protocol.
- Privacy: can the solution be made private, to accommodate validators that do not wish their data to be publicly known?
- Reliability: how easy it is to submit fake data for a given approach? At the end of the day, a sufficiently motivated party should be able to turn off or bypass these data-gathering features. (We hope to address this by building a highly functional solution where the incentives for doing this are scarce)
- Sampling rate/data density: how long does it take to gather a meaningful statistic? We aim to strike a balance here, such that data can be gathered sufficiently quickly, but without meaninglessly overloading the protocol.

---

This marks the end of our kickoff update. Our team looks forward to carrying on with this research project and sharing any updates under this post.

## Replies

**isidorosp** (2024-02-06):

This is really great! I think what’s also worth exploring, apart from privacy (which is important for security concerns), is tamper-proofness.

The difficulty with incentives for faking data is that the incentives (which one indeed wants to minimize) may not be endogenous to the system, e.g. they may be meta-properties of the system and/or they may be enforced (or supported) via things like social norms, mechanisms in different places in the stack, and not native system parameters or mechanisms. So while you want to minimize the likelihood that someone can fake their data you also want to make it as technically difficult as possible. The difficulty here is that we do not only want to verify votes but verify that the vote content corresponds to the piece of software with the spec interpretation of the client that they “represent” – which means that the “work output” of the client itself also needs to somehow be uniquely signed (by a signature of the “client” and of the signatory). Apart from putting the entire logic that we want to verify in a TEE (may be “possible” eventually but right now it’s probably very high complexity, adds a lot of requirements for users (e.g. that all validators are running on machines that have access to TEEs, which we don’t want because it’ll hurt diversity substantially) and developers, and will probably be slow), is it perhaps possible to put pieces of it (e.g. the voting mechanism)? It may be worth explore some of the work being done in the SUAVE ecosystem (eg [Sirrah: Speedrunning a TEE Coprocessor | Flashbots](https://writings.flashbots.net/suave-tee-coprocessor) )?

---

**jorem321** (2024-02-20):

Throughout our research, we will need to discuss questions on the sample size required to make statistically significant observations on the Ethereum validator set. These questions will be essential to all of our proposed methods and solutions. Namely,

1. Given a validator set of size N, what sample size n do we need to achieve a reasonably accurate (in a sense yet to be specified) picture of the validator set’s client diversity?
2. For each of the proposed solutions, how long does it take to achieve this?

We answer the first question below.

---

# Formal definition and modeling of the problem

Let c_1, c_2, \dots c_m represent different Ethereum client implementations (we analyze the consensus and execution cases separately). For each client c_i, there is a proportion 0 \leq p_i \leq 1 of the entire validator set \mathcal{V} running the client c_i.

> Remark: due to architectures such as multiplexers and DVT, it is not true that \sum{p_i} = 1. Instead, we have \sum{p_i} > 1. This does not affect the analysis, as will be seen below.

**Goal:** Determine a sample size n\ll N that can be used to estimate the true proportions p_i with statistical significance.

The general procedure to follow is outlined below:

1. Given a randomly chosen sample \mathcal{S} \subset \mathcal{V} with |\mathcal{S}| = n, query each validator for their client diversity usage, i.e., gather the bit m-tuples q_j = (x_{1j}, x_{2j}, \dots, x_{mj}), where x_{ij} \in \{0,1\} denotes whether client c_i is used by validator j, for 1\leq i \leq m, and 1\leq j \leq n.
2. Define the estimators \hat{p_i} = \sum_{j}x_{ij}/n.
3. Observe that, since \mathcal{S} is chosen randomly, the values x_{ij} (for fixed i and varying j) correspond to independent observations, wherefore each of the estimators \hat{p}_i follow binomial distributions.
4. By utilizing the theory of approximations to binomial distributions, one can relate the required sample size n with a margin of error E for the measured proportion, assuming a given confidence level (95% is a standard choice).

> Note: the binomial distribution model is commonplace for statistical estimations of proportions, and is regularly used in various types of experiments, including surveys and clinical trials. (See, e.g., Fleiss, J. L., Levin, B., & Paik, M. C. [2013]. Statistical Methods for Rates and Proportions.)
>
> The only additional assumption made here is a steady-state one: we assume that variability in the client diversity distribution is negligible over the period where the samples are collected. This requires the period to be reasonably short (e.g. days as opposed to months)—an assumption that we will check for consistency in each of our methods.

## Notation

For the approximations below, we define the following variables:

- p is the (true) proportion as defined above, which we seek to estimate experimentally.
- We denote the confidence level as 1-\alpha, so that \alpha>0 is a small positive number. For example, for a confidence level of 95%, \alpha = 0.05.
- Z: Z-score evaluated at the parameter 1-\alpha/2. In our calculations, we will always use a 95% confidence level, so we can simply take Z=1.96.
- E: margin of error or uncertainty in the proportion estimate. E.g., E=0.01 for a 1% margin of error.
- n is the sample size required for the margin of error E to hold.

> Note on notation: Since we may obtain different sample sizes when estimating diversity data for each client c_i, we will technically have variables p_i, E_i, and n_i for each client. We can then choose n = \max\{n_1,n_2, \dots, n_m\} as the appropriate sample size. However, in practice, we will see all these sample sizes can be taken to be equal.

# First approach: the normal distribution approximation

> The following section derives our results analytically to motivate and justify some of our parameter choices. Readers who are not interested in this may skip to the next section, in which we show how to obtain our required sample sizes with the help of an R library.

As a first approximation, these binomials [can be estimated as normal distributions](https://en.wikipedia.org/wiki/Central_limit_theorem), given the right conditions. Namely, we require sample sizes large enough to satisfy the following rules of thumb for each client c_i:

\begin{equation} n_i\cdot p_i> 5 \text{ and } n_i \cdot (1-p_i) > 5. \end{equation}

For client diversity data, we expect the measured proportions to be above 1% (or 0.01) and below 99% (or 0.99) for each client. Thus, this condition is easily satisfied by choosing a sample size larger than 1000 validators.

Under the normal approximation, the following relation [(Wald’s interval)](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Normal_approximation_interval_or_Wald_interval) holds:

E_i=Z_{i}\sqrt{\frac{p_i(1-p_i)}{n}}
,

where for each i the variables above are defined as stated before. Solving for n_i yields

\begin{equation} n_i=\frac{Z_{i}^2 }{E_i^2}
\times p_i (1-p_i). \end{equation}

Note that the true values p_i are not known *a priori*. We can address this in at least two ways:

1. We can use the worst-case bound p(1-p) \leq 0.25. (See Figure 1 below)
2. We can further refine this by using the existing estimates (e.g., validator surveys for execution clients) as priors.

[![p times 1-p](https://ethresear.ch/uploads/default/optimized/2X/b/b5ef803b11e93da31d2bf9d00daef4086676416d_2_690x256.png)p times 1-p1301×483 25.5 KB](https://ethresear.ch/uploads/default/b5ef803b11e93da31d2bf9d00daef4086676416d)

Figure 1: Plot of the term f(p)=p(1-p) in Wald’s interval as a function of p. We see that p=1/2 leads to its maximum, meaning that p=1/2 corresponds to a worst-case estimate for the sample size.

### Example

Using the worst-case bound p_i(1-p_i) \leq 0.25 and a 95% confidence level in the equation for n_i above, we obtain the following sample sizes:

- For a 1% error rate, n \approx 9.6k validators.
- For a 0.5% error rate, n \approx 38.5k validators.

# Corrections to the normal distribution approximation

The approximation above is the most elementary in the theory of binomial distributions. More refined estimations can lead to more precise answers in certain conditions. We will see, however, that given the current parameters, the estimations above are quite precise already.

We omit analytical derivations here, opting instead for using software packages to obtain numerical results. The calculations above can be readily obtained on R via the DescTools library and its `BinomCIn` function. As an improvement to the normal approximation, we employ the so-called [Wilson score interval](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval) in our sample-size estimations and compare it to the results above.

```r
library("DescTools")
# Default parameters: conf.level = 0.95, method = "wilson".
p = 0.50 # Worst-case scenario for estimation.

width = 0.02 # For a tolerated error of 1%, the total interval width is 0.02
n = BinomCIn(p, width)
print(n)

width = 0.01 # For a tolerated error of 0.5%, the total interval width is 0.01
n = BinomCIn(p, width)
print(n)
```

The obtained sample sizes round up to 9600 and 38411, respectively, in agreement with the previous estimate.

We can easily repeat the calculations for other values. Rounding up the results, we get the following values of n for various combinations of frequency p and error E.

|  | E=1\% | E=0.5\% |
| --- | --- | --- |
| p= 0.01 | 1143 | 4497 |
| p=0.1 | 3461 | 13833 |
| p=0.5 | 9600 | 38411 |
| p=0.7 | 8063 | 32265 |

*Table 1: Estimations of the required sample size n for accurately measuring a client diversity proportion p with a tolerated margin of error E. Although we can use smaller sample sizes for estimations of minority or supermajority clients, we will take the value of n obtained when p=0.5, which is valid for all cases.*

The table illustrates how p=0.5 corresponds to a worst-case estimate, and that the estimations for n obtained above are reasonable sample sizes for the required confidence levels and tolerated errors.

# Summary and interpretation of results

- Through statistical methods, we derive a sample size of n=9.6k validators to measure client diversity data with a confidence level of 95\% and a tolerated error of 1\%.
- Likewise, we derive a sample size of n=38.4k validators to measure client diversity data with a confidence level of 95\% and a tolerated error of 0.5\%.
- Note that the sample sizes do not depend on N. That is, if the validator set were to double in size, the same sample sizes would remain adequate.
- The discussion above does not address a sample where some validators choose not to disclose their client diversity data—a scenario that we expect will be commonplace. In this case, we will need to increase the sample size accordingly. Concerns about bias arising from the removed validators in the sample do apply.

We will keep in mind these sample sizes (and the techniques to compute them) for future posts.

---

**jorem321** (2024-02-20):

# Method discussion: Posting client diversity data on the graffiti field.

In the next post, we provide some comments on perhaps the best-known method for client diversity measurement. This method (which has also already been proposed and discussed by the community) involves minimal protocol changes. It consists of having every block proposer post an identifier of their own EL+CL client combination on the 32-byte graffiti field.

This is already done to an extent by various CL clients, by making the default graffiti an identifier of the consensus client and its current version. However, by giving the CL client information on the EL client used at the time of proposing a block, we can extend this approach to include both EL+CL client data. This change is paramount, given that accurate EL client diversity data is precisely the least accessible at the moment.

# Required changes

### EngineAPI method for the CL client to retrieve the EL client details.

When this project started, there was no method for the CL client to determine the EL client it was connecting to. This interconnectivity is necessary to unlock various approaches, such as pushing EL+CL client data on the graffiti field or obtaining client diversity data via crawling methods on the consensus networking layer alone.

Recently, a proposal was issued to implement the relevant API method [here](https://github.com/ethereum/execution-apis/pull/517). The proposed changes include:

- Standardizing a two-letter client code for each execution client. (E.g. ‘NM’ for Nethermind)
- Defining a ClientVersionV1 object, which includes

the two-letter code,
- the human-readable name of the client,
- a version string,
- and the first four bytes of the commit hash of the build.

Defining an `engine_getClientVersionV1` method, which returns an array of `ClientVersionV1` objects (to accommodate for potential multiplexed architectures)

### Encoding standards to represent the data

There are various reasons why it is beneficial to agree upon a standard nomenclature (or “encoding”) for how data should be posted on the graffiti field:

- To facilitate the processing of data to obtain aggregate statistics.
- To minimize the number of bytes required to communicate the data. This allows validators to continue using the graffiti field for self-expression.

This [document](https://hackmd.io/@wmoBhF17RAOH2NZ5bNXJVg/BJX2c9gja) by EthDreamer describes a flexible standard—allowing users to provide client diversity data in increasingly more succinct versions to accommodate larger user messages on the graffiti field.

### Modifying default CL graffiti field message

With the two changes above, CL clients can change their default graffiti message to include client diversity data. This data will be more or less expressive as a function of the message length to be posted by a given user.

# Challenges around this method

Although this method’s simplicity is a plus, its accuracy can suffer due to the following edge cases:

### Dealing with parties that do not participate

Note that this method can only gather data from parties that choose not to opt out of default settings (whether by modifying their clients or posting graffiti messages that are too long to allow client diversity data to be posted). It remains to be seen what fraction of the validator set will opt out of the method in practice.

### Multiplexed architectures/DVT

It does not seem practical for this method to account for architectures where there is more than one execution client connected to the consensus client. The encoding standard discussed above only allows one client pair at a time. Setting up a more complex/verbose encoding which allows multiple clients at a time has the downside of leaving fewer graffiti field bytes for validators to use for their own purposes.

### Distinction between proposer/attester duties

In principle, this method tracks validators’ activities as block proposers, not as attesters, despite the latter duty being the one that may lead to a catastrophic fork (hence the one we want diversity insights into). This distinction is relevant given that some highly specialized node operators may choose to use different setups as block proposers from the ones they use as attesters. For example, [Vouch](https://www.attestant.io/posts/introducing-vouch/) (a multi-node validator client) can use a specific node only for certain duties, such as proposals or attestations.

# How fast can we get an accurate estimate?

We compute how long it takes to reach the conditions for statistical significance identified in the previous post.

Assuming that every validator opts into this method, we get data for one validator every 12 seconds. Furthermore, assuming that:

- all validators post their data,
- the number of repeated block proposers over the computed timeframe is negligible,

we can collect data for 9.6k and 38k validators in 1.33 days and 5.33 days respectively. **From the analysis above, we see that this method can reach statistical significance reasonably quickly.** We do need to account for larger samples in case some validators withhold their data. This will have the downside of skewing the randomness of the sample, and so it is recommended to report the fraction of validators with “unknown” client software when aggregating this data.

# Anonymizing graffiti field reports

As part of our research, our team is exploring a series of primitives that can be used to anonymize client data reports. The techniques we have in mind include encryption and mixnet approaches. They both involve the following:

- A form of encryption: whether for subsequent client data aggregation via homomorphic encryption or to allow for private mixing of the votes.
- A zero-knowledge proof attesting to the validity of the ciphertexts involved or the validity of the shuffling. For example, in case of the encryption approach, we want to make sure that each encrypted message corresponds to a valid client data (with the weight assigned to a candidate never greater than one). In case of the mixnet approach, the zk-proof shows that the mixing took place correctly.

We observe that graffiti field reports do not seem amenable to such approaches.

- If we aim to post the encrypted client data on the graffiti field for its subsequent decryption, we only have access to 32 bytes, which is well below the required output size of the most commonplace encryption schemes.
- Even if we use an encryption scheme whose output is small enough to post the encrypted data on the graffiti field, we still have the problem of needing to share the zk-proof certifying the integrity of the data.
- Finally, mixnet approaches are precluded by the fact that client diversity data is collected and posted one report at a time (since the data is gathered sequentially from block proposers)

All in all, anonymization seems to require a larger bandwidth for data sharing, and it naturally leads to approaches with communication channels different from the graffiti field. Our team is currently exploring such alternatives.

# Acknowledgments

We thank [@isidorosp](/u/isidorosp) for helpful discussions around this subject.


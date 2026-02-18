---
source: ethresearch
topic_id: 19506
title: "[Research report] Allowing validators to share client information privately---a project by Nethermind Research"
author: jorem321
date: "2024-05-09"
category: Consensus
tags: []
url: https://ethresear.ch/t/research-report-allowing-validators-to-share-client-information-privately-a-project-by-nethermind-research/19506
views: 4597
likes: 16
posts_count: 4
---

# [Research report] Allowing validators to share client information privately---a project by Nethermind Research

Dear ethresear.ch readers,

As part of the Ethereum Foundation’s [Data Collection Grants Round 2023](https://esp.ethereum.foundation/data-collection-grants) which ran between last September and October, an interdisciplinary team involving Nethermind Research and Nethermind core developers received a grant to work on the project “Allowing validators to provide client information privately”. Below, we attach our submission in fulfillment of the objectives behind the project. In this deliverable, we have provided the necessary motivation and background for the problem of measuring client diversity, which we then use to propose and analyze three different approaches for validators to privately share their client diversity data—each with their strengths and weaknesses.

[Deliverable: Allowing validators to provide client information privately](https://nethermind.notion.site/Allowing-validators-to-provide-client-information-privately-bfea6436bfe246d28afdcda125d9049c)

## Executive summary of the proposed approaches.

We briefly summarize the key ideas behind the three approaches before. The reader is referred to the deliverable for a full exposition.

### 1. Client diversity data on the graffiti field

As the first approach, we have discussed a method for measuring validator client diversity by posting data directly on the graffiti field. We note that this approach has been discussed by the community before. We have outlined necessary changes, such as creating an EngineAPI method for CL clients to retrieve EL client details and agreeing on encoding standards for the data. We have also discussed challenges with this method including dealing with parties that do not participate, multiplexed architectures, and distinguishing between proposer and attester duties.

We have also discussed statistical significance, i.e., how many client data reports are needed to accurately estimate the client distribution from graffiti field data alone. We confirmed that the analyzed method can reach statistical significance quickly (in the order of days) assuming a reasonable participation rate. We discuss these assertions quantitatively in the deliverable.

Finally, we have assessed the feasibility of anonymizing graffiti field reports, concluding that existing methods like encryption or zero-knowledge proofs are impractical to use due to the sequential nature of data collection and the limited space in the graffiti field.

### 2. Allowing nodes to listen to client diversity data through the gossip network + using nullifiers to hide the identity of validators

As the second approach, we have examined a potential modification to Ethereum’s P2P layer to enable crawlers to obtain validator distribution for client diversity. We have explored using a dedicated channel in the GossipSub protocol to share client diversity data efficiently. We have proposed a method that periodically selects validators at random to submit their client diversity data, which is then shared through GossipSub. Each validator forms its client diversity data into a **ClientData** object and publishes it via a designated topic. Then, the nodes in this designated topic can receive those objects, verify their authenticity, and aggregate them for the final result. We have also discussed the challenges around this method, particularly concerning network overload.

Furthermore, we have explored anonymizing P2P reports to ensure validators’ privacy. We have discussed potential approaches such as encrypting client data or anonymizing the voters’ identities using nullifiers and zero-knowledge proofs. We have proposed an approach that uses BLS signatures, nullifiers, and zero-knowledge proofs to hide validators’ identities and prevent double submissions. Validators submit encoded client data along with proofs to a P2P network. We have discussed potential deanonymization vectors such as P2P traffic analysis and proposed mitigation strategies like mixnets and approaches based on Dandelion and Dandelion++.

Implementing these strategies may face challenges such as increased latency and complexity. We have stressed our interest in community input regarding the concern level over potential attack vectors and the feasibility of mitigation strategies.

### 3. Dedicated voting scheme for client data collection

As the third and last approach, we have proposed a voting protocol aimed at collecting data from validators securely and verifiably, avoiding issues like obscurity and centralization found in existing survey methods. We have examined the use of public bulletin boards (PBBs) or blockchains for collecting votes, drawing insights from Vitalik’s analysis of blockchains’ limitations in elections and the advantages of using blockchains as bulletin boards. Due to its decentralization and cost-efficiency, we have proposed to utilize a blockchain, specifically Ethereum’s Holesky Testnet. Regarding how validators submit their votes, we have considered having validators encrypt their client data and share it through a P2P network, and using a trusted committee—called decryption authorities—to receive the encrypted data, submit the received data to a smart contract, and finally, aggregate and decrypt the encrypted client data.

This third method addresses some of the traffic analysis concerns in the second method by leveraging homomorphic encryption of the votes, which requires a trusted committee.

# A call for feedback

As the next stage of this research project, we look forward to disseminating and discussing the aforementioned approaches through various channels, including this forum and community calls. Thus, we welcome discussions with the Ethereum community to gauge the impressions on the most suitable approach. For example,

- In the deliverable above, we have provided a rubric that ranks the downsides of each method according to their severity as perceived by the team. From the team’s perspective, this analysis positions the second method as the most favorable. Should this rubric be challenged in any way?
- Does the reader see any additional concerns with the proposed methods?
- Are there any variations or suggestions the reader can think of to build upon the methods herein?

We look forward to your impressions and comments!

## Replies

**etan-status** (2024-06-27):

One thing to keep in mind is that even if the reporting mechanism itself is defined for perfect privacy, there are still side channels that may leak the actually used software, e.g., for consensus clients, the way how attestations are packed or existing libp2p identify endpoints, specific error messages e.g. when requesting unavailable data from them, or even just the presence e.g. of light client data topics which are only served by Nimbus and Lodestar. For execution clients, similar side channels may leak the underlying software, e.g., the timing at which a validator cluster goes offline due to a fake-invalid engine response may reveal that those validators have used the affected EL client. For those reasons, I like the simplicity of the graffiti approach. On a side node, it’s also the approach that RocketPool is using by default.

I really appreciate the deep research on a perfect privacy preserving solution, though, even though I personally think it’s overkill to add all the infrastructure as long as the primary use case is the diversity survey.

---

**ahmeth** (2024-07-03):

Here is the list of questions asked by the participants during Consensus-layer Call 136, and the corresponding answers.

**Q: Doesn’t this research assume that 1 validator == 1 node operator?**

A: No, it counts validators, not nodes. When picking the sample, we use the validator index, similar to how we choose attestation groups or sync committees.

**Q: Is the goal to find diversity metrics across node operators or the specific number of validators?**

A: Across validators.

**Q: What about consolidated validators, such as one super validator with a giant balance versus another operator that splits it up across multiple 32 ETH validators?**

A: Balance will play a role in how many times you are chosen to be part of the sample. More balance means more votes.

**Q: Wouldn’t a large validator operator (like Lido) be able to manually set something untrue and ruin the stats, causing everyone to interpret and act on false data? What if large operators nudge people to/off clients?**

A: It is possible, and nothing can be done about that. But there is no incentive for any large operator to do this since submissions are anonymous. There is no incentive for large operators to nudge people to/off clients.

**Q: What if someone runs more than one client at the same time?**

A: We have mechanisms to account for such setups. When encoding the votes, one can vote for multiple clients at once with a multiplexer flag set.

**Q: What about survivorship bias? People who care about client diversity and run a minority client are probably more likely to answer in a survey than people/operators who don’t.**

A: If enabled by default in the client, it’s partially mitigated. There is no reason for large operators not to send their votes as votes don’t affect bandwidth and are anonymous. This approach is much better than the current survey method.

**Q: If every client would have its own unique attestation ordering, it would allow extracting information about the client from proposed blocks (like blockprint is already doing).**

A: True, though still thwarted a bit by complex setups that have multiple clients attesting but one client block-building. This only applies to CL clients and not ELs.

---

**rolfyone** (2025-12-12):

## Graffiti approach

The problem we’ve had with using graffiti has been mostly that it’s not on by default, so we’re not getting adequate data from that alone. It’s also probably a little simplistic if we’re looking to gather data about SSV / vouch nodes (clients backing them) due to space available in the field anyway.

A scan of recent history shows about 27% of blocks had graffiti (unless my script had bugs which is definitely possible ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) )

## Gossipsub thoughts

Depending on how the gossipsub was organised if we went that way, really we’d probably be looking at something like providing

- voting eth
- Custody group count maybe?
- highest milestone supported maybe?
- node config

EL / CL or (could be similar to graffiti like ELCL code)
- SSV layout somehow
- vouch layout somehow

if its over gossipsub probably avoiding versions of clients for security. I’m also not sure if we’d still need to allow the option to turn it off, but i’d prefer it was just always on, and we only provide the minimum we need to understand topology.

One thing i’d like to avoid is peers being selected based on their voting power though, so im not sure how all of this happens without peers being preferred on attributes of the disclosure if we went that way. Maybe network people like [@raulk](/u/raulk) or [@AgeManning](/u/agemanning) or someone in research/security is much more informed on whether thats an issue…

It does seem like a fine line between making sure we avoid supermajority issues and allowing peers too much information potentially…

Messaging would also be important here. We really don’t want to have more data than we need, but we do need to understand stake / client layout to mitigate supermajority risk. If it was a ‘once per epoch’ kind of message or something, then we could just listen for a couple of epochs on that channel, but obviously the mesh would have to pass it on etc so that nodes can see.


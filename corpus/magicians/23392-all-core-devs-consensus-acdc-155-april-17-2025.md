---
source: magicians
topic_id: 23392
title: All Core Devs - Consensus (ACDC) #155, April 17 2025
author: system
date: "2025-04-05"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-155-april-17-2025/23392
views: 342
likes: 3
posts_count: 5
---

# All Core Devs - Consensus (ACDC) #155, April 17 2025

# All Core Devs - Consensus (ACDC) #155, April 17, 2025

- Apr 17, 2025, 14:00 UTC
- 90 minutes
- Stream

# Agenda

- Pectra

Mainnet

May 07, 2025 at epoch 364032 (10:05:11 UTC)
- Client releases: 21 April 25
- Blog post: 23 April 25
- Reminder: https://github.com/ethereum/pm/blob/master/Pectra/pectra-mainnet-plan.md#client-team-coordinators

Fusaka

- PeerDAS

peerdas-devnet-6

peerdas-devnet-6 specs - HackMD
- open questions?

BPO configuration: array of records of `(epoch, max)`
plans towards `fusaka-devnet-0`

- peerdas-devnet-6 + BPO
- move EIP-7892 to SFI?

CFI set

- SFI: PeerDAS
- currently CFI: BPO
- CFI to discuss:

EIP-7917
- leaned towards DFI during last ACDC:

EIP-7688
- EIP-7732
- EIP-7898

Research, spec, etc.

- Fulu builder spec and getPayload

https://github.com/ethereum/builder-specs/pull/117#pullrequestreview-2724183804

---

Facilitator email: [stokes@ethereum.org](mailto:stokes@ethereum.org)

[GitHub Issue](https://github.com/ethereum/pm/issues/1434)

## Replies

**abcoathup** (2025-04-10):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #155, April 17 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-155-april-17-2025/23392/4) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #155 Summary
> Action items
>
> Pectra timelines
>
> Mainnet date confirmed to be May 7 2025
> Client releases by April 21 2025
> Pectra mainnet blog post by April 23 2025
>
>
> Add contacts per client team for Pectra mainnet observation
>
> pm/Pectra/pectra-mainnet-plan.md at master · ethereum/pm · GitHub
>
>
> Fusaka SFI EIPs
>
> EIP-7594 (PeerDAS)
> EIP-7892 (BPO)
>
>
> Fusaka CFI EIPs
>
> EIP-7917 (Proposer lookahead stability)
>
>
> Other PFI Fusaks EIPs are moved to DFI status.
>
> Summary
> Pectra
>
> See timelines in action …

#### AI generated summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nicocsgy/48/12742_2.png)

      [All Core Devs - Consensus (ACDC) #155, April 17 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-155-april-17-2025/23392/3) [Protocol Calls & happenings](/c/protocol-calls/63)




> Recording :
> https://www.youtube.com/live/i_29BU3J97M
> Meeting summary for All Core Devs - Consensus (ACDC) (04/17/2025)
> Quick recap
> The meeting covered discussions on the upcoming mainnet launch, client releases, and testing progress. The team debated various technical aspects, including the implementation of Block Parameter Optimization, configuration formats, and the inclusion of specific EIPs in future hard forks. They also addressed concerns about API specifications, potential challenges …

### Recordings

  [![image](https://i.ytimg.com/vi/i_29BU3J97M/hqdefault.jpg)](https://www.youtube.com/watch?v=i_29BU3J97M&t=203s)



      [x.com](https://x.com/EthCatHerders/status/1912868425959145533)





####

[@](https://x.com/EthCatHerders/status/1912868425959145533)



  https://x.com/EthCatHerders/status/1912868425959145533










### Writeups

- ACDC #155: Call Minutes - Christine D. Kim by @Christine_dkim [christinedkim.substack.com]

### Additional info

- Mainnet upgrades to Pectra May 7, Epoch 364032

---

**nicocsgy** (2025-04-18):

Recording :

https://www.youtube.com/live/i_29BU3J97M

**Meeting summary for All Core Devs - Consensus (ACDC) (04/17/2025)**

**Quick recap**

The meeting covered discussions on the upcoming mainnet launch, client releases, and testing progress. The team debated various technical aspects, including the implementation of Block Parameter Optimization, configuration formats, and the inclusion of specific EIPs in future hard forks. They also addressed concerns about API specifications, potential challenges with increased blob counts, and the need for faster forks while maintaining system stability.

**Next steps**

• stokes to update the Meta EIP to move EIP-7892 (BPO EIP) to SFI status.

• Client teams to add contact information to the Petra mainnet fork organization document.

• Client teams to implement and test the new BPO configuration format in YAML.

• stokes to update the Meta EIP to CFI EIP-7917 (Proposer Look-Ahead) and DFI other EIPs for Fusaka.

• stokes to continue gathering input from relays and builders regarding potential changes to the Builder API for Fusaka.

• Client teams to aim for Petra mainnet client releases by April 21st.

• Client teams to prepare for Fusaka Devnet 0, targeting around May 20th, including Perdos Devnet 6 and BPO EIP implementation.

**Summary**

**Mainnet Launch and Client Releases**

In the meeting, Stokes led the discussion, ensuring everyone could hear him. The team discussed the upcoming mainnet launch on May 7th and the planned client releases for Petra on April 21st. Mario reported positive progress on testing, with all clients showing good results. The team was reminded to add contacts to a document for instant response in case of any issues. Barnabas updated on the launch of Devnet 6, which had some problems, particularly with the Nimbus client. The team was asked to provide further updates on the issues.

**Ethereum BPO Configuration and Emergency Overrides**

The group discusses the implementation of Block Parameter Optimization (BPO) in the Ethereum network. They agree on using a YAML configuration format with a list of objects specifying epochs and corresponding maximum blobs per block. There is debate about whether to include this in the main config file or a separate file, with a preference for including it in the main config. The discussion then shifts to the possibility of emergency overrides for BPOs. Dustin argues against designing for emergency scenarios, stating that coordination for such rapid changes is unrealistic. Parithosh clarifies that the focus is on having the ability to cancel or adjust future scheduled BPOs based on performance data, rather than immediate emergency changes. The group leans towards using new config releases for such adjustments rather than implementing override flags.

**Configuring BLOB Schedule and API Spec**

The team discussed the configuration for the BLOB schedule and decided to use a specific format in the config Yaml file. They agreed not to include a command line override for now. Enrico raised a concern about the impact on the API spec, but the team felt that it should be okay. The team also discussed the potential issues with unexpected keys in the config file, but decided to proceed with the new format.

**Electra and Deneb Implementation Discussion**

In the meeting, Stokes and Justin discussed the implementation of Electra and Deneb limits. They agreed to include Electra in the Dpo schedule and to backfill it. They also discussed the possibility of including Deneb in the schedule, but decided to wait for further testing. Barnabas raised concerns about the potential for a mismatch in scheduling schemes, but Stokes reassured him that it should be fine as long as the configuration is correct. They also discussed the implementation of the BPO EIP for future hard forks. Stokes suggested that they should aim for the next devnet to focus on to be Posaka Devnet 0, with Reidos Devnet 6 and BPO. The team agreed to aim for a May 20th timeline for this.

**Eip Status and Future Proposals**

Stokes discussed the status of various eips, including the decision to move the Bpo eip to Sfi from Cfi, and the proposal to look ahead at Eip 7, 9, 1, 7. Ansgar expressed support for accepting Eip-7917 and rejecting others. Dmitry shared that he and the mixed bytes team are conducting a detailed research on the actual effects and impact of implementing Eip 7, 8, 8, and that it is crucial for app layer developers. The team agreed to move Eip 7, 9, 1, 7 to Dfi and Eip 7, 6, 8, 8 to Cfi.

**CIP Inclusion in Upcoming Fork**

The team discussed the inclusion of a specific CIP in their upcoming fork. Radek expressed concerns about including the CIP due to the agreed-upon process of scheduling forks and including certain items. Stokes suggested a cautious approach, focusing on due diligence before including any CIPs. The team agreed to prioritize pure DOS and EOF changes before considering the CIP. Sean and ethDreamer shared their views on the potential impact of the CIP on other teams. The team also discussed the implementation difficulty of the CIP and the importance of having a stable system before adding more features.

**EIP-7917 Inclusion in Fusaka Hard Fork**

The group discusses the inclusion of EIP-7917 in the upcoming Fusaka hard fork. While initially considering it as a “consider for inclusion” (CFI) item, concerns are raised about changing the beacon state. Potuz points out that this would be the only change affecting the beacon state in Fusaka. Lin explains the importance of the EIP for pre-confirmations, stating that without it, they would need to rely on a hacky oracle solution. The group considers postponing the EIP to a future hard fork, with Dmitry suggesting specifying it for the Glamsterdam fork instead.

**Fusaka Fork EIPs: PeerDAS Focus**

The group discusses the potential inclusion of EIP-7917 (proposer look-ahead) and EIP-7688 (stable containers) in the upcoming Fusaka fork. There is weak support for CFI (Considered for Inclusion) status for EIP-7917, with the understanding that it will be dropped at the first sign of complications. The group agrees to focus primarily on peerDAS and only consider additional EIPs if there is time. Regarding EIP-7688, opinions are mixed. Some suggest CFI-ing both EIPs or neither, while others prefer to only include EIP-7917. The main concerns are maintaining development velocity, avoiding scope creep, and ensuring smooth implementation. No final decision is made on EIP-7688, but there is a general inclination to be cautious about adding multiple EIPs to the fork.

**Faster Forks and Stable Containers**

In the meeting, the team discussed the need for faster forks and the potential challenges that could arise from including stable containers in the next hard fork. They considered the impact on proofs and the need for applications to update their proofs. The team also discussed the possibility of separating 7, 6, 8, 8 from other features and the potential for small forks. The importance of maintaining a fast iteration of forks was emphasized, and the team agreed to focus on the main eap and the eof. The conversation ended with a discussion on the scalability of the builder APIs and the potential challenges with high blob counts.

**API Response Size for Proposers**

In the meeting, Stokes raised concerns about the API’s response size for proposers, particularly in relation to the potential for increased blob count. The discussion centered around the possibility of changing the API to reduce the response size or even remove it entirely, with the relay being responsible for distributing the block and blobs. Terence suggested returning a positive response after the relay propagated the data. The team agreed to revisit the API for Fusaka and gather further input from different relays and builders. The consensus was to ensure that the builder API specs explicitly require builders/relays to propagate the data.

AI-generated content may be inaccurate or misleading. Always check for accuracy.

---

**ralexstokes** (2025-04-18):

**ACDC #155 Summary**

**Action items**

- Pectra timelines

Mainnet date confirmed to be May 7 2025
- Client releases by April 21 2025
- Pectra mainnet blog post by April 23 2025

Add contacts per client team for Pectra mainnet observation

- pm/Pectra/pectra-mainnet-plan.md at master · ethereum/pm · GitHub

Fusaka SFI EIPs

- EIP-7594 (PeerDAS)
- EIP-7892 (BPO)

Fusaka CFI EIPs

- EIP-7917 (Proposer lookahead stability)

Other PFI Fusaks EIPs are moved to DFI status.

**Summary**

Pectra

- See timelines in action items.
- Testing update from Mario:

Teams writing and reviewing new tests
- All tests running against all clients
- Increased confidence in test coverage compared to previous weeks

Incidence response document needs client team contacts added via PR

- See link in action items.

PeerDAS

- peerdas-devnet-6 launched ~1 week ago
- Some issues with EL processing times, investigation ongoing
- EIP-7892 (BPO) configuration format:

Will use YAML “list of records” structure on CL side.
- Configuration to be included in main config file, not separate
- No CLI override functionality planned for now

Discussed plans for `fusaka-devnet-0` to launch by late May

- Follows peerdas-devnet-6 spec along with EIP-7892

Fusaka

- Agreed to move EIP-7892 to SFI as part of the Fusaka blob scaling strategy
- Then discussed on Fusaka CFI EIP set

Everyone agreed to focus primarily on PeerDAS and blob scaling on the CL side
- Only once Fusaka devnets with the current SFI set is stable, would we consider moving any additional EIPs from CFI to SFI.

EIP 7917 (proposer lookahead stability):

- Early investigation shows implementation is small to medium complexity
- Potuz highlights this EIP does touch the beacon state, where as the current SFI set does not; given the centrality of this data structure it does imply this EIP would add significant surface area to Fusaka overall.
- Given this, client teams agreed to DFI at first sign of complications with weak support to CFI today.

EIP 7688 (SSZ stable containers):

- Decided to handle in future fork since no immediate proof impacts with the current SFI set
- Participants reiterated the focus on blob scaling and so elected to not CFI today.

Fusaka builder API discussion

- Current concerns with builder API scalability for high blob counts:

large response sizes, esp. as blob counts become higher with Fusaka in a synchronous API
- Concern for resource constraints for smaller nodes when processing large responses

Potential solutions discussed:

- Remove API response entirely (relay handles gossip)
- Keep status quo (relay returns all data)
- Hybrid approach (return payload, separate blob distribution)

and potentially leverage existing “get blobs” functionality to assist with distribution

Teams agreed API needs revision for Fusaka; next step is to get input from builder/relay community

---

**system** (2025-05-02):

### Meeting Summary:

No summary overview available

**Click to expand detailed summary**

In the meeting, Stokes led the discussion, ensuring everyone could hear him. The team discussed the upcoming mainnet launch on May 7th and the planned client releases for Petra on April 21st. Mario reported positive progress on testing, with all clients showing good results. The team was reminded to add contacts to a document for instant response in case of any issues. Barnabas updated on the launch of Devnet 6, which had some problems, particularly with the Nimbus client. The team was asked to provide further updates on the issues.

The group discusses the implementation of Block Parameter Optimization (BPO) in the Ethereum network. They agree on using a YAML configuration format with a list of objects specifying epochs and corresponding maximum blobs per block. There is debate about whether to include this in the main config file or a separate file, with a preference for including it in the main config. The discussion then shifts to the possibility of emergency overrides for BPOs. Dustin argues against designing for emergency scenarios, stating that coordination for such rapid changes is unrealistic. Parithosh clarifies that the focus is on having the ability to cancel or adjust future scheduled BPOs based on performance data, rather than immediate emergency changes. The group leans towards using new config releases for such adjustments rather than implementing override flags.

The team discussed the configuration for the BLOB schedule and decided to use a specific format in the config Yaml file. They agreed not to include a command line override for now. Enrico raised a concern about the impact on the API spec, but the team felt that it should be okay. The team also discussed the potential issues with unexpected keys in the config file, but decided to proceed with the new format.

In the meeting, Stokes and Justin discussed the implementation of Electra and Deneb limits. They agreed to include Electra in the Dpo schedule and to backfill it. They also discussed the possibility of including Deneb in the schedule, but decided to wait for further testing. Barnabas raised concerns about the potential for a mismatch in scheduling schemes, but Stokes reassured him that it should be fine as long as the configuration is correct. They also discussed the implementation of the BPO EIP for future hard forks. Stokes suggested that they should aim for the next devnet to focus on to be Posaka Devnet 0, with Reidos Devnet 6 and BPO. The team agreed to aim for a May 20th timeline for this.

Stokes discussed the status of various eips, including the decision to move the Bpo eip to Sfi from Cfi, and the proposal to look ahead at Eip 7, 9, 1, 7. Ansgar expressed support for accepting Eip-7917 and rejecting others. Dmitry shared that he and the mixed bytes team are conducting a detailed research on the actual effects and impact of implementing Eip 7, 8, 8, and that it is crucial for app layer developers. The team agreed to move Eip 7, 9, 1, 7 to Dfi and Eip 7, 6, 8, 8 to Cfi.

The team discussed the inclusion of a specific CIP in their upcoming fork. Radek expressed concerns about including the CIP due to the agreed-upon process of scheduling forks and including certain items. Stokes suggested a cautious approach, focusing on due diligence before including any CIPs. The team agreed to prioritize pure DOS and EOF changes before considering the CIP. Sean and ethDreamer shared their views on the potential impact of the CIP on other teams. The team also discussed the implementation difficulty of the CIP and the importance of having a stable system before adding more features.

The group discusses the inclusion of EIP-7917 in the upcoming Fusaka hard fork. While initially considering it as a “consider for inclusion” (CFI) item, concerns are raised about changing the beacon state. Potuz points out that this would be the only change affecting the beacon state in Fusaka. Lin explains the importance of the EIP for pre-confirmations, stating that without it, they would need to rely on a hacky oracle solution. The group considers postponing the EIP to a future hard fork, with Dmitry suggesting specifying it for the Glamsterdam fork instead.

The group discusses the potential inclusion of EIP-7917 (proposer look-ahead) and EIP-7688 (stable containers) in the upcoming Fusaka fork. There is weak support for CFI (Considered for Inclusion) status for EIP-7917, with the understanding that it will be dropped at the first sign of complications. The group agrees to focus primarily on peerDAS and only consider additional EIPs if there is time. Regarding EIP-7688, opinions are mixed. Some suggest CFI-ing both EIPs or neither, while others prefer to only include EIP-7917. The main concerns are maintaining development velocity, avoiding scope creep, and ensuring smooth implementation. No final decision is made on EIP-7688, but there is a general inclination to be cautious about adding multiple EIPs to the fork.

In the meeting, the team discussed the need for faster forks and the potential challenges that could arise from including stable containers in the next hard fork. They considered the impact on proofs and the need for applications to update their proofs. The team also discussed the possibility of separating 7, 6, 8, 8 from other features and the potential for small forks. The importance of maintaining a fast iteration of forks was emphasized, and the team agreed to focus on the main eap and the eof. The conversation ended with a discussion on the scalability of the builder APIs and the potential challenges with high blob counts.

In the meeting, Stokes raised concerns about the API’s response size for proposers, particularly in relation to the potential for increased blob count. The discussion centered around the possibility of changing the API to reduce the response size or even remove it entirely, with the relay being responsible for distributing the block and blobs. Terence suggested returning a positive response after the relay propagated the data. The team agreed to revisit the API for Fusaka and gather further input from different relays and builders. The consensus was to ensure that the builder API specs explicitly require builders/relays to propagate the data.

### Next Steps:

- stokes to update the Meta EIP to move EIP-7892 (BPO EIP) to SFI status.
- Client teams to add contact information to the Petra mainnet fork organization document.
- Client teams to implement and test the new BPO configuration format in YAML.
- stokes to update the Meta EIP to CFI EIP-7917 (Proposer Look-Ahead) and DFI other EIPs for Fusaka.
- stokes to continue gathering input from relays and builders regarding potential changes to the Builder API for Fusaka.
- Client teams to aim for Petra mainnet client releases by April 21st.
- Client teams to prepare for Fusaka Devnet 0, targeting around May 20th, including Perdos Devnet 6 and BPO EIP implementation.

### Recording Access:

- Join Recording Session
- Download Transcript
- Download Chat


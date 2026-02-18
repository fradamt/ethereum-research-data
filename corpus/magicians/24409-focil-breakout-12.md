---
source: magicians
topic_id: 24409
title: FOCIL Breakout #12
author: system
date: "2025-06-02"
category: Protocol Calls & happenings
tags: [breakout, focil]
url: https://ethereum-magicians.org/t/focil-breakout-12/24409
views: 139
likes: 0
posts_count: 2
---

# FOCIL Breakout #12

# FOCIL Breakout #12, June 3, 2025, 14:00 UTC

# Agenda

- Aikaterini presentation on Multiple Proposer Transaction Fee Mechanism Design: Robust Incentives Against Censorship and Bribery
- Implementation updates

 **🤖 config**

- Duration in minutes : 60 mins
- Recurring meeting : true
- Call series : Focil Breakout
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : false
- display zoom link in invite : true

[GitHub Issue](https://github.com/ethereum/pm/issues/1564)

## Replies

**system** (2025-06-04):

### Meeting Summary:

The meeting covered discussions about Focol as a candidate for Glamsterdam and its interactions with other proposals, along with research on ZK Focol and statelessness. A detailed presentation was given on two proposed payment mechanisms for the fossil system to enhance resistance against bribery attacks, including analysis of block producer behavior and transaction inclusion strategies. The team reviewed implementation progress on various projects including IP merge changes and execution specs, while discussing payment mechanism strategies and transaction visualization updates in preparation for the upcoming Berlin event.

**Click to expand detailed summary**

Thomas discussed the upcoming Focol session in Berlin, noting that it will cover Focol as a candidate for Glamsterdam and its interactions with other proposals and upgrades. He encouraged participants to consider the urgency of Focol compared to scanning EAPs. Aikaterini presented a recent joint work with Julian Ma and Thomas, which was recently uploaded to the archive. The presentation covered their research on ZK Focol and statelessness.

Aikaterini-Panagiota presented a paper on two proposed payment mechanisms for the fossil system to enhance resistance against bribery attacks. She explained the current system’s process of transaction submission and inclusion, noting that builders can omit transactions under congestion. The presentation detailed a bribery attack scenario where an external entity attempts to censor a target transaction by bribing includers or block producers to omit it. Aikaterini-Panagiota also discussed the potential deviations a block producer might make if the bribe was high, noting the tension between the financial incentives.

The meeting focused on discussing strategies and potential issues related to block producers, including the possibility of deviant behavior such as spamming the main pool to prioritize their transactions. Aikaterini-Panagiota explained that this behavior could lead to target transactions being ignored, and they emphasized the importance of monitoring and addressing such actions. The discussion also touched on the need for audits and the importance of maintaining order within the system. Additionally, there was a brief mention of a paper and slides related to the topic, but no specific decisions or next steps were outlined in the transcript.

Aikaterini-Panagiota discussed the protocol’s response to bribery attempts, explaining how block producers and includers can include transactions from a main pool or create their own “fake” transactions. She described how the minimum bribe required to censor a transaction consists of the transaction fee and the cost of an attack involving spamming the main pool. Aikaterini-Panagiota also explained that higher fees for includers make bribing attacks more difficult, as block producers face greater risks and costs when not certain of their election. Finally, she mentioned investigating payment mechanisms that distribute fees not only to block producers but also to includers.

A team of researchers presented two payment mechanisms for Ethereum that satisfy incentive properties and increase the cost of bribing attacks. The first mechanism, Debbie, allows users to set two phases: one for block producers and another for includers, with fees shared randomly among committee members. The second mechanism simplifies this process by having the system automatically determine fee splits between producers and includers. Both mechanisms were shown to provide censorship resistance and better fee flexibility, with Debbie offering more user control over fee allocation.

Aikaterini-Panagiota presented research on transaction inclusion mechanisms, focusing on a comparison between includer fees and a proposed double/single fee system. She explained that under congestion, a mechanism that gives the entire fee to the block producer is better than one that gives the entire fee to the inclusion. She noted that the proposed mechanisms satisfy Ethereum’s incentive properties while having trade-offs between simplicity and user freedom in fee allocation. Marc asked about the distribution of inclusion fees among multiple includers, to which Aikaterini-Panagiota clarified that the highest-ranked includer takes the entire fee to prevent splitting and reduce the risk of bribery.

The discussion focused on a model where rational behavior is assumed, but participants may also take bribes, potentially censoring transactions. Aikaterini-Panagiota explained that the model accounts for uncertainty about whether others will take bribes, using a Bayesian approach. Marc raised a potential issue where an includer might pretend to accept a bribe to dissuade further bribes, while actually planning to include their transaction anyway.

The team discussed implementation updates, with Jacob reporting progress on IP merge changes and execution specs, including a new branch for fossil IP and related test fixtures. Jacob requested y’all clients to verify their ability to generate and consume test fixtures, which are currently marked as engine test only. The team also touched on Nethermind implementation progress and discussed payment mechanism strategies, with a question raised about whether ordering by inclusion fee is rational behavior.

The team discusses ongoing work and updates on various projects. Jihoon mentions opening a draft PR and reaching out to Lighthouse regarding interrupt work. Marc presents a PR related to Inclusion List Building, explaining its importance for transaction inclusion speed and throughput. Katya shares updates on transaction visualization and metrics, including a draft PR for beacon metrics and the existence of a new execution metrics specs repo. The team agrees to review these updates and provide feedback, particularly in preparation for discussions at the upcoming Berlin event.

### Next Steps:

- EL clients to generate and consume test fixtures from Jacob’s execution spec tests PR
- EL client developers to review Jacob’s PR on the execution specs for Fossil
- Lighthouse team to continue work on Fossil implementation (currently low priority)
- Ethereum community to review Mark’s PR on inclusion list building improvements
- Ethereum community to review Katya’s draft PR on beacon metrics for Fossil
- Ethereum community to provide feedback on desired metrics for Fossil to be added to the execution metrics specs repo
- Ethereum developers to discuss Fossil metrics further at the Berlin interop

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: dSk!r7.#)
- Download Chat (Passcode: dSk!r7.#)


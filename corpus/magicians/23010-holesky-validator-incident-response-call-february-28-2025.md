---
source: magicians
topic_id: 23010
title: Holesky Validator Incident Response Call | February 28, 2025
author: system
date: "2025-02-27"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/holesky-validator-incident-response-call-february-28-2025/23010
views: 141
likes: 3
posts_count: 3
---

# Holesky Validator Incident Response Call | February 28, 2025

# Holesky Validator Incident Response Call

- Feb 28, 2025, 15:00 UTC
- Duration in minutes : 60
- Stream: https://www.youtube.com/live/ksr-6iuSvrg?feature=shared
- Zoom: to be shared in the #allcoredevs channel before the call

# Agenda

- Context on Holesky situation
- Coordinated Holesky slashings. Holesky validators should:
- If using Besu, Nethermind, Geth and/or Lodestar, update your client
- Sync to the head of Holesky
- Be ready to disable slashing protection
- Tentative schedule to begin slashings: slot 3737760 (epoch 116805) at 15:12:00 UTC

[GitHub Issue](https://github.com/ethereum/pm/issues/1337)

## Replies

**system** (2025-02-28):

## Meeting Summary:

### Quick recap

The team prepared for a mass slashing event on the Holesky network, aiming to disable slashing protection on different operators, and discussed the status of validators and the need for them to finalize a block to avoid slashing. They also discussed the progress of their project, focusing on participation and attestation rates, and the potential for running slashers on Mainnet. The team also discussed the financial contributions from various sources, the current challenges with validator participation, and the need to prioritize testing and coordinate next steps.

The group is preparing for a mass slashing event on the Holesky network, aiming to disable slashing protection on different operators within the next 10 minutes. The event is scheduled to begin at slot 3,737,760, which is about 8 minutes away. Potuz mentions that operators are expected to restart their nodes without slashing protection approximately 90 seconds before the designated time. Some slashings have already occurred, with sync aggregation showing between 65-70% participation, and block proposals are happening.

The team discussed the status of validators and the need for them to finalize a block to avoid slashing. Some operators were unsure about running validators. The total number of validators was estimated to be around 1.7 million, with 1.1 million present during the call. It was clarified that not all the present validators would be subject to slashing, but they still needed to finalize a block. The team agreed to restart their nodes and attempt mass slashing. The goal was also to finalize a block as part of the process.

The team discussed the progress of their project, focusing on participation and attestation rates. They noted an increase in participation but expressed doubt about reaching their target. The second epoch was identified as a crucial period for stabilization and decision-making. Issues with the Dora interface and a bug affecting attestation processing were also discussed, with a commitment to fix the latter as soon as possible. The team also discussed the potential for running slashers on Mainnet, with some uncertainty about whether this was happening.

The team discussed the balance of active and slashed validators, with a focus on the impact of slashing on the data set. They also discussed the possibility of having a high percentage of proposals without a corresponding high percentage of attestations, attributing this to the chaotic nature of the system due to missed slots and forks. The team also discussed the need for more than 15% of validators to be active and not slashed, and the potential for large client teams to ensure their nodes are posting attestations. The conversation ended with a discussion on the need for more than the current 15% of active and non-slashed validators.

Tim discussed the financial contributions from various sources, including Lodestar, Rock X, Bay Sue, Grand Dean, Nimbus, and Prism. He noted that there were 200K unnamed contributions. Fabio questioned the accuracy of the data, particularly regarding Bezos and Lodestar. Matthew and nflaig discussed monitoring logs and the status of validators. Tim guided the team on how to sort the data by offline status. Pk910 explained that the page aggregates attestations over the last 3 epochs and that exited and slashed validators are no longer counted as online or offline. Stokes clarified the relationship between offline, exit, and slashed statuses.

The team discussed the current challenges with validator participation, with around 10% of attestations missed due to offline validators. They considered various solutions, including restarting nodes, syncing from an un-finalized checkpoint, and encouraging more validators to come online. The presence of configuration errors was acknowledged, and the team agreed to work on fixing these. The possibility of some validators getting slashed was discussed, but the impact seemed to be minimal so far. The team also discussed reaching out to client teams and smaller operators to encourage them to bring their validators online. The overall strategy was to wait until enough bad stake bleeds out, allowing the chain to be justified.

Tim led the discussion on the progress of the testing event, emphasizing the need to get more validators online to increase the chances of finalizing a block. He suggested running a larger slashing event if the current one doesn’t yield any results by Monday. The team also discussed the need to prioritize testing and coordinate next steps, with a focus on getting more validators online. The possibility of starting a new test net or a Holesky classic revival was also raised for future testing needs.

### Next Steps:

- Validator operators to bring more validators online over the weekend to try to reach finalization.
- Client teams to continue monitoring their validators and address any configuration issues.
- Saulius/Grandine team to bring Afri’s former validators back online.
- All participants to continue coordinating via Discord over the next few days.
- Testing call participants to discuss on Monday what specific things need testing that can’t be done on the current Holesky state.
- Testing call participants to consider on Monday whether to run a slasher for larger slashing if finalization is not achieved.
- Testing call participants to discuss potential need for a new testnet or “Holesky classic” revival to enable certain types of testing.

**Recording Access:**

- Join Recording Session (Passcode: vs#9xBUx)
- Download Transcript
- Download meeting Chat

  [![image](https://img.youtube.com/vi/ksr-6iuSvrg/maxresdefault.jpg)](https://www.youtube.com/watch?v=ksr-6iuSvrg)

---

**system** (2025-03-27):

YouTube recording available: https://youtu.be/oacAxtKC6rQ


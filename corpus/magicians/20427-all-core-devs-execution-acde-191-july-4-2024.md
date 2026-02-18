---
source: magicians
topic_id: 20427
title: All Core Devs - Execution (ACDE) #191, July 4 2024
author: abcoathup
date: "2024-07-02"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-191-july-4-2024/20427
views: 746
likes: 1
posts_count: 2
---

# All Core Devs - Execution (ACDE) #191, July 4 2024

### Agenda

[Execution Layer Meeting 191 · Issue #1080 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1080)

Moderator: [@ralexstokes](/u/ralexstokes) (filling in for [@timbeiko](/u/timbeiko))

### Summary

Recap by [@ralexstokes](/u/ralexstokes) from *[Eth R&D Discord](https://discord.com/channels/595666850260713488/745077610685661265/1258457376638632016)*

Started with Pectra updates

- Clients moving ahead with devnet-1 implementations
- Waiting for a greater number of clients to be ready before we launch devnet-1, but expect to be there in the next week or two
- Got an update on 7702 progress that will likely go into devnet-2; please take a look as the intention is to merge in the next week

Note: devnet-1 will reflect the current spec of EIP-7702

Then turned to discuss EIP-7212

- There’s support for the feature as it brings a lot of nice UX improvements around key/wallet management with a widely supported cryptographic curve
- We discussed the point around formal inclusion in Pectra, but will wait till the next ACDE to make that decision. While the EIP in isolation brings a nice set of features, it needs to be weighed against the already large scope of Pectra
- There are a few minor things to address around the EIP itself, including mirroring the precompile address across L2 deployments and L1. These will be resolved over the next two weeks to tee us up for an inclusion discussion on the next call

Next, [we discussed a proposal to add events](https://ethereum-magicians.org/t/eip-7002-execution-layer-triggerable-exits/14195/13) to the predeploy system contracts for cross-layer communication with EIP-7002 and EIP-7251. Consensus was that this change makes sense and the corresponding contracts will be updated.

Then, we had a call to [deactivate EIP-158](https://github.com/ethereum/EIPs/pull/8712) to simplify the effects of deploying EIP-7702 and the Verkle migration. In light of the latest updates to 7702 we no longer need this proposal and decided to ignore it.

And to wrap the call, we had a discussion around making progress on other protocol improvements like history expiry and changes to the blob mempool to streamline usage of blobs by users like rollups. We jumped across various concerns here so check the call for the details. In short, there was a call for more regular updates on EIP-4444’s progress, and a call out to various things both rollups and clients can do to more intelligently handle the pipeline from blob producer to blob inclusion on-chain.

Reminder: Goerli has been deprecated and so clients will (or have already!) dropped support for this testnet.

### Recording

  [![image](https://img.youtube.com/vi/58_bJD_dmm0/maxresdefault.jpg)](https://www.youtube.com/watch?v=58_bJD_dmm0&t=35s)

## Replies

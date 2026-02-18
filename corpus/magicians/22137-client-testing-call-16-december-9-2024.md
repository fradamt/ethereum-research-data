---
source: magicians
topic_id: 22137
title: Client testing call #16, December 9 2024
author: parithosh
date: "2024-12-09"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/client-testing-call-16-december-9-2024/22137
views: 126
likes: 1
posts_count: 1
---

# Client testing call #16, December 9 2024

**Testing call summary**

**Pectra**

**pectra-devnet-4/Mekong**

Grandine is now fixed and network is at >98% participation

Missing rate is from ethereumJS perf issues

**pectra-devnet-5**

We discussed existing open PRs:

- Pass max_blobs_per_block into Engine API methods: Decided to include it in a future devnet to give us more time for consensus, so it would not be included in the latest release
- Rename PartialPendingWithdrawal field index to validator_index: Included in devnet-5 since its a minor renaming
- eip7251: Limit consolidating balance by validator.effective_balance: Included in devnet-5 since its a minor renaming
- changes required for EIP-7742: Waiting to be merged in

[EIP-7762: Increase MIN_BASE_FEE_PER_BLOB_GAS](https://ethereum-magicians.org/t/eip-7762-increase-min-base-fee-per-blob-gas/20949) was brought up in the context of finding out the increased testing load. The testing team had an initial look and the tests that need updating indeed overlap with `EIP-7691`, So the topic of inclusion of this EIP would be brought up on ACD with this new information.

[Update EIP-7762: Move to Draft](https://github.com/ethereum/EIPs/pull/9062) was brought up for discussion as well, the decision was to close the EIP as it introduces a decent amount of testing delays.

[Update BLS precompile costs](https://discord.com/channels/595666850260713488/1293956979848380529) was also discussed. EL devs please have a look before ACD this week, Marek might reach out for an update.

An up to date spec-sheet can be found [here](https://notes.ethereum.org/@ethpandaops/pectra-devnet-5)

**Gas limit change**

- The community has recently been pushing for a gas limit increase, some issues were found with the increase and have been outlined here.
- 3/5 CL clients on the call agreed that they were going to increase the GOSSIP_MAX_SIZE value in a future release (before pectra). The other 2 CLs were not present to state their viewpoint, but potentially one client is against and one client is for the change.
- The worst case of a staggered rollout were then discussed. There should be no issues as long as the block size is not bigger than the lowest GOSSIP_MAX_SIZE set on any client on the network. Beyond that size, we might see the client with smallest GOSSIP_MAX_SIZE missing slots.
- Such a change would introduce a non-equal p2p network and we usually strive to avoid that as well as strike to batch such changes at hard forks.
- Since we lacked all parties to make a decision, we would do so on the PR here or in existing async channels.
- In the meantime, the testing team will carry out experiments with a staggered rollout and other attempts at breaking the chain

TLDR: Please read the ethresearch post [here](https://ethresear.ch/t/on-increasing-the-block-gas-limit-technical-considerations-path-forward/21225). As long as the recommendations are followed we should continue to see a safe network.

**peerdas & eof**

No change, waiting on pectra unblocking

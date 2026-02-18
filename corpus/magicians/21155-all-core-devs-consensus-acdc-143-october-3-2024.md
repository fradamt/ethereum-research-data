---
source: magicians
topic_id: 21155
title: All Core Devs - Consensus (ACDC) #143, October 3 2024
author: abcoathup
date: "2024-09-21"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-143-october-3-2024/21155
views: 174
likes: 1
posts_count: 2
---

# All Core Devs - Consensus (ACDC) #143, October 3 2024

#### Agenda

[Consensus-layer Call 143 · Issue #1158 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1158) moderated by [@ralexstokes](/u/ralexstokes)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #143, October 3 2024](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-143-october-3-2024/21155/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #143 summary
> Action Items
>
> Resolve open devnet-4 spec issues: pectra-devnet-4 specs - HackMD
>
> Special call out for the execution requests refactor: engine: Make execution requests a sidecar, take 2 by mkalinin · Pull Request #591 · ethereum/execution-apis · GitHub
>
>
> Assess implementation weight of Separate type for unaggregated network attestations by arnetheduck · Pull Request #3900 · ethereum/consensus-specs · GitHub
>
> Client teams lean towards inclusion in pectra-devnet-5 or later; anot…

#### Recording

  [![image](https://img.youtube.com/vi/dplciLdQTM0/maxresdefault.jpg)](https://www.youtube.com/watch?v=dplciLdQTM0&t=9)

#### Additional Info

[Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-consensus-call-143/) by [@Christine_dkim](/u/christine_dkim)

## Replies

**ralexstokes** (2024-10-04):

**ACDC #143 summary**

**Action Items**

- Resolve open devnet-4 spec issues: pectra-devnet-4 specs - HackMD

Special call out for the execution requests refactor: engine: Make execution requests a sidecar, take 2 by mkalinin · Pull Request #591 · ethereum/execution-apis · GitHub

Assess implementation weight of [Separate type for unaggregated network attestations by arnetheduck · Pull Request #3900 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/pull/3900)

- Client teams lean towards inclusion in pectra-devnet-5 or later; another client team or two assessing the full scope of changes to weigh cost vs benefit would be very helpful

Prioritize implementation of `engine_getBlobsV1` to more quickly roll out bandwidth savings for network nodes

**Summary**

- Started with a check-in around the progress of pectra-devnet-3

A few minor bugs (Besu, Lighthouse seem to have open issues) with work under way to resolve

Then turned to planning `pectra-devnet-4`

- Series of open spec issues remain
- Started with the design for the execution requests in the Engine API and how they are structured across the CL and EL client
- There has been active design work this week and we are very close to a final design
- Follow the conversation on this PR engine: Make execution requests a sidecar, take 2 by mkalinin · Pull Request #591 · ethereum/execution-apis · GitHub to track progress
- Touched on the other open devnet-4 CL PRs:

eip7251: Switch to compounding when consolidating with source==target by mkalinin · Pull Request #3918 · ethereum/consensus-specs · GitHub

Has been merged

[eip6110: Queue deposit requests and apply them during epoch processing by mkalinin · Pull Request #3818 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/pull/3818)

- Ready for review, aim to merge by end of next week

And then look at some final Pectra items with two PRs to refactor the handling of attestations

- OnchainAttestation: Separate type for onchain attestation aggregates by mkalinin · Pull Request #3787 · ethereum/consensus-specs · GitHub

nice from a spec point of view, but we agreed to defer to a later HF to put into the specs to avoid client work that could potentially delay Pectra

`SingleAttestation`: [Separate type for unaggregated network attestations by arnetheduck · Pull Request #3900 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/pull/3900)

- this PR helps with DoS resistance in pathological cases and so there was much more support to include in Pectra relative to the previous link
- going to target a “minimal” implementation that only addresses this type at the networking layer, and not pursue a full set of changes that could otherwise be imagined under this change
- decided to target a later devnet (after pectra-devnet-4) for potential inclusion which gives a bit more time for further review, including assessment of implementation load

Next, turned to PeerDAS

- Work has continued on PeerDAS devnets, considering launching a new net after a variety of bug fixes
- Turned to engine_getBlobsV1 which was recently merged into the execution-apis repo

Clients have a diversity of implementation progress, but it is a top priority so that we can roll out potential bandwidth savings on the network ASAP

Note: needs support on both CL and EL!

Discussed this PR as a follow on to `engine_getBlobsV1`: [P2P clarifications when introducing `engine_getBlobsV1` by tbenr · Pull Request #3864 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/pull/3864)

- Group agreed to treat mempool blobs retrieved via this method as blobs received over gossip, implying they should also be gossiped to peers

Then had another check-in around various blob scaling options following up from last week’s call

- Still a bit early as we are still in a data-gathering phase to best understand which solutions are preferred
- Relevant analysis from the last week: On solo staking, local block building and blobs - Sharding - Ethereum Research
- potuz raised an interesting point around syncing and ensuring that nodes can sync at higher blob counts, especially under situations of non-finality

experiment is tricky as it is hard to replicate mainnet network topology

Ansgar then asked about how to think about timing of blob changes so we aren’t in a position where we want to increase blob counts in Pectra but are waiting for a cycle of spec and implementation work

- We agreed that EIP-7742 should be on client team’s radars sooner rather than later

Wrapped the call with an announcement around a named testnet (aka user facing) for Devcon, with the plan to target devnet-4


---
source: magicians
topic_id: 21086
title: All Core Devs - Consensus (ACDC) #142, September 19 2024
author: abcoathup
date: "2024-09-14"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-142-september-19-2024/21086
views: 194
likes: 0
posts_count: 1
---

# All Core Devs - Consensus (ACDC) #142, September 19 2024

#### Agenda

[Consensus-layer Call 142 · Issue #1154 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1154) moderated by [@ralexstokes](/u/ralexstokes)

#### Summary

Summary by [@ralexstokes](/u/ralexstokes) *[copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1286438973132111882)]*

- Began the call with Pectra

Touched on status of pectra-devnet-3 ; it has been launched and generally going well

deployed a “bad block” fuzzer which surfaced some bugs; relevant teams are debugging

Turned to discuss how to handle scoping of the current Pectra fork into a more manageable size

- Lots of convo, with many different perspectives across core devs here; catch the recording for the full discussion
- Landed on two key decisions to make

Do we focus on the EIPs currently deployed to pectra-devnet-3 as a target for Pectra (next hard fork)?
- Assuming we split off pectra-devnet-3 from the rest of development for the Pectra hard fork, do we want to determine the scope of the hard fork after Pectra?

Again, many inputs and ideas but we agreed to determine the Pectra hard fork as the EIPs currently deployed to `pectra-devnet-3` .

- There’s still some polish for this EIP set remaining, but the timeline from devnet-3 to mainnet is order of a few months as we move to a ‘spec freeze’ for Pectra and keep iterating devnets along the way to testnet and ultimately mainnet.

There was a lot less consensus around determining the scope of the fork after Pectra. Obvious candidates are EOF and PeerDAS (having already been scheduled for Pectra so far), but there is some uncertainty around other features like Verkle, or additional EIPs with benefits like EIP-7688.
We agreed to move ahead with pushing `pectra-devnet-3` to production, and tabling the conversation around the scope of the next fork until a later ACD call.

- check Tim’s suggestion on how to think about the second fork here: ⁠allcoredevs⁠

Next, we looked at a number of open PRs concerning the “polish” of the devnet-3 feature set so that we can get to a spec freeze ASAP.

- Check the agenda for the full set.

In particular, client teams should check out these changes to the consolidation and deposit flow that are required to mitigate potential DoS issues around the handling of these operations

https://github.com/ethereum/consensus-specs/pull/3918
- https://github.com/ethereum/consensus-specs/pull/3818

We also discussed some changes to attestation refactoring that would be nice, although there is some concern it will lead to an outsized ask in terms of code change — it would be great to get another client team or two to add their perspective to these PRs

- https://github.com/ethereum/consensus-specs/pull/3900

arnetheduck will update to cover the validator behavior this PR touches

[Separate type for onchain attestation aggregates by mkalinin · Pull Request #3787 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/pull/3787)

After the Pectra discussion, we moved to look at the status of PeerDAS and a consideration of the blob parameters

- A quick check-in on PeerDAS devnets: teams are still working on implementing the latest specs and debugging local issues
- Then, had a presentation to support raising the target and/or max blob count in Pectra (with consideration for these changes going into the fork after Pectra as well)

[Public] RFC: Ethereum H12025 Prioritization - Google Docs

This proposal touches on the fork scheduling conversation above, and as we can expect there are lots of views/inputs to this decision
An interesting point was raised around the deployment of `IDONTWANT` in the gossip layer, as this feature should save some bandwidth for a node and give us more room to consider raising the blob parameters, even ahead of PeerDAS

- Implementation is under way, but clients have different amounts of progress here

Consensus on the call was that raising the blob target in Pectra could be reasonable, especially pending further mainnet analysis that supports the headroom for an increase

- Otherwise, it seemed too risky to raise the maximum blob count without PeerDAS

#### Recording

  [![image](https://img.youtube.com/vi/MRtJSnBU3Gk/maxresdefault.jpg)](https://www.youtube.com/watch?v=MRtJSnBU3Gk&t=80s)

#### Additional Info

- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim

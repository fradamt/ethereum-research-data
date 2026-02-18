---
source: magicians
topic_id: 21240
title: Pectra testing call #7, 30 September 2024
author: abcoathup
date: "2024-10-02"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/pectra-testing-call-7-30-september-2024/21240
views: 73
likes: 0
posts_count: 1
---

# Pectra testing call #7, 30 September 2024

#### Summary

Update by [@parithosh](/u/parithosh) *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1290334902180511860))*

`pectra` :

- Update from pk910 about deposit queue test results. We’re going to wait for the queue related PRs to be merged in and retry the experiment on pectra-devnet-4.
- There’s an unexplained drop in participation on the pectra-devnet-3, investigation underway
- pectra-devnet-4 planning underway, current task is for teams to look into open PRs: pectra-devnet-4 specs - HackMD , e.g: https://github.com/ethereum/execution-apis/pull/591 might still need some discussion pre-merging
- Work started on rbuilder and integration into testing stack. Mario will work on mock-mev after the tests are done. The mock-mev update should help clients test the API changes and rbuilder would help test the full integration. Ideally both are done before the devnet launch.
- Briefly discussed system contract address changes. Since we want to reduce the number of changes, lightclient will try to get the next round of changes in by the end of the week. There still might be future mods, but the version at the end of the week would be stable for a while. Please keep an eye out for messages about said change.
- We would want external people to interact with pectra-devnet-4 or similar devnets. This means we’d ideally want a stable API, or one we intend to release on mainnet. Please have a look at this EIP: Eip 7702 schema and authlist in receipt schema by Redidacove · Pull Request #592 · ethereum/execution-apis · GitHub and raise similar external APIs now rather than later
- Keep an eye on this PR for the status on the specs release: https://github.com/ethereum/execution-spec-tests/pull/832
- Consensus spec release probably later this week
- We briefly discussed the blob increase topic and if there were any concerns besides data. We also tried to get a sense of how difficult EIP-7742 would be with a blob increase. Client teams were asked to at least look into it for easier decision making later on.

`eof` :

- Main update is that eof wont happen in pectra, so a rebase is expected. We would wait for pectra-devnet-4 to come out for a version to target
- Danno is working on some assertoor/kurtosis configs that could be used for local testing

`peerDAS` :

- Discussion on issues surrounding the current devnet along with an explanation by lodestar on what happened
- Since peerdas won’t happen in pectra, any debugging tools that would be interesting should be collected in one place, potentially here
*peerdas devnet relaunch with the current spec will occur soon, the switch to pectra rebase will only happen after pectra-devnet-4``fuzzing :
- Bad block generator has been running for a ~week-ish now with no significant issues found

`general` :

- Focus this week is on getting PRs closed and specs released. Ideally we’re in a place to launch pectra-devnet-4 next week

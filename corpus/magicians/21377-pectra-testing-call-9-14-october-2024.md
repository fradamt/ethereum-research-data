---
source: magicians
topic_id: 21377
title: Pectra testing call #9, 14 October 2024
author: abcoathup
date: "2024-10-15"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/pectra-testing-call-9-14-october-2024/21377
views: 62
likes: 0
posts_count: 1
---

# Pectra testing call #9, 14 October 2024

#### Summary

Update by [@bbusa](/u/bbusa) *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1295394501061382255))*

**Pectra**

- pectra-devnet-3

shutdown timeline by mid week. - Aim to shut it off by wednesday if there are no objections

`pectra-devnet-4`

- alpha 8 release last week
- no more blocking open issues to launch
- possibly working teku image - was unable to confirm
- prysm has a couple more PRs to merge in
- nethermind will be ready very soon ™️
- ethereumjs - bugs in engine API - working on it - ready in 1-2 days
- erigon - will take a few days to get ready
- besu - will take a few days - working on execution spec tests
- geth passing all devnet 4 tests - engine API PR still open
- lodestar - try to get it ready as soon as possible
- reth - most changes in open PRs
- Lightclient checking how to test 7702 transactions. Mario No support t9n in tests. Proposal for tx test - use the json instead of rlp. - Might need to impl new test format to support this new tx type. Mario gonna look into it. Blockchain test currently has support for 7702 transactions. - t9n tx type would be a nice to have but not a blocker.
- launch target by end of the week

**Peerdas**

- peerdas-devnet-3

been unfinalized for a while (7d)
- lodestar issues - data doesn’t seem to be syncing
- possibly do a relaunch with only validating supernodes

**EOF - Fusaka**

- eof-devnet-0 -  fusaka-devnet-0

rebased on alpha 8 - built on top of devnet 4 spec
- osakaTime as the fork activation
- launch in ~ 2 weeks time

**SSZ devnets**

- ssz-devnet-0

just launched today, no peers just bootnode
- https://fusaka-light.box/
- Currently only running ethjs  nimbus pair
- GitHub - ethpandaops/ssz-devnets
- Want to get a dedicated discord channel for this

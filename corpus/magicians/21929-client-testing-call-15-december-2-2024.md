---
source: magicians
topic_id: 21929
title: Client testing call #15, December 2 2024
author: parithosh
date: "2024-12-02"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/client-testing-call-15-december-2-2024/21929
views: 125
likes: 2
posts_count: 1
---

# Client testing call #15, December 2 2024

# Summary

***Pectra***

- pectra-devnet-4

Has been shutdown.

***Mekong***

- Update on the public testnet non-finality incident from last week as well as the associated spec tests Update
- All the client teams have updated their CLs to fix the issue.
- We’re currently at ~86% participation and the clients will be notified on their issues

***devnet-5***

- EIP-7742 related PRs will get a last look before merging
- EIP-7691 PR will be merged soon after
- EIP-7251 PR will also get a last look and be merged in
- The aim is to have the consensus-spec PRs merged by mid-week and a release ideally before ACD
- Engine exclude empty requests PR was merged on the call
- EIP-7742 PR needs a rebase after the latest EIP changes and should be merged after
- Once the EL changes are merged in, the execution-spec-tests release will follow. The tracker is live here
- We will gate the entry to devnet-5 based on the execution-spec-tests passing.
- The hive instance using the spec release will be available ASAP for clients to use.

***Peerdas and EOF***

- Once devnet-5 spec is out, we will pin these releases for EOF/PeerDAS codebases to rebase on top of
- A new EIP to update the max code size might be added to EIP, more on that at ACD

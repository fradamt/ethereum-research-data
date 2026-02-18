---
source: magicians
topic_id: 21310
title: Pectra testing call #8, 7 October 2024
author: abcoathup
date: "2024-10-09"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/pectra-testing-call-8-7-october-2024/21310
views: 61
likes: 0
posts_count: 1
---

# Pectra testing call #8, 7 October 2024

#### Summary

Update by [@marioevz](/u/marioevz) *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1292871102485237813))*

`pectra devnet-3` :

- Lighthouse bug when proposing blocks, there’s a PR that is open with the fix: Filter out BlsToExecutionChange messages for 0x02 validators by pawanjay176 · Pull Request #6464 · sigp/lighthouse · GitHub.
- Besu bug is still pending to be resolved with an open PR: Warm up to address at tx start if account is delegated, restrict auth nonce by daniellehrner · Pull Request #7717 · hyperledger/besu · GitHub.

`pectra devnet-4`

- There was a discussion on whether the CL should send back the entire list of requests to the execution layer, the decision at first was to leave the specs as is, which entails sending the full requests list. At a later point on the call, @potuz raised concerns regarding the amount of data being serialized and JSON-formatted in Engine API is an unnecessary overhead, and it should be simplified to sending a simple hash that the CLs should compute (not hash-tree-root but a different sha256 commitment). At the end of the call, the sentiment changed to agree that we should apply this change and the CL should simply compute the hash and send it back instead of the full list, therefore the PRs need to be updated. On-going discussion can be found in this thread: ⁠Make execution requests a sidecar
- Open PRs

[Beacon API] Update submitPoolAttestationsV2 endpoint decision to skip this for devnet-4 on the grounds that is not ready.
- [Builder API] add initial electra spec: requires Engine API changes to be merged first
- [Consensus-specs]: eip7685: Pass execution_requests to notify_new_payload At the time of writing this contains the full requests being sent back to the execution layer, needs a rework to send only the requests commitment hash (as specified in Update EIP-7685: group requests into request-data by lightclient · Pull Request #8924 · ethereum/EIPs · GitHub) instead.
- [Engine API]: engine: Make execution requests a sidecar, take 2 : At the time of writing this PR is currently specified to send the full requests lists in the engine_newPayloadV4 , and needs to be updated to send the requests hash.
- [Execution EIP] Update EIP-7702: add several clarifications to align spec with tests, no opposition regarding this PR, should be accepted and merged for Devnet-4.
- [Execution EIP] Update EIP-7702: Do not allow authorization nonce equal to 2**64 - 1, also no opposition regarding this PR, should be accepted and merged for Devnet-4.
- [Execution EIP] Update EIP-7702: restrict field sizes needs an update to move from draft status and be merged for devnet-4.

`eof`

- Not many updates from last week, path forward is waiting on devnet-4 to be released and then rebase Osaka (which contains only EOF at the time being) on top of it in order to launch osaka-devnet-0 at some point in the coming weeks.
- feat(forks,tests): Osaka by marioevz · Pull Request #869 · ethereum/execution-spec-tests · GitHub is an open PR to the execution layer tests that has been prepared to rebase EOF to be in Osaka.

`peerDAS`

- Devnet-3 was launched with the same spec as devnet-2 in order to have a working devnet, but 14-15 hours ago there was an issue that caused all clients to be on their own different fork, and at the moment there is no lead on the culprit.

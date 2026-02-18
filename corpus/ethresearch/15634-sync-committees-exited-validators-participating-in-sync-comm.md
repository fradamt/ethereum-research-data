---
source: ethresearch
topic_id: 15634
title: Sync committees - exited validators participating in sync committee?
author: builderbenny
date: "2023-05-18"
category: Security
tags: []
url: https://ethresear.ch/t/sync-committees-exited-validators-participating-in-sync-committee/15634
views: 1357
likes: 0
posts_count: 2
---

# Sync committees - exited validators participating in sync committee?

Probably late to the party - but I just realized that a validator can be “exited” but still participate in the sync committee.

Unless I am mis-reading the specs - it appears that the sync committee is chosen 256 epochs ahead (see for instance: [process_sync_committee_updates](https://github.com/ethereum/consensus-specs/blob/0ac4329b4a811fd79ad51e143d34e8339cf184fc/specs/altair/beacon-chain.md#sync-committee-updates); [get_next_sync_committee](https://github.com/ethereum/consensus-specs/blob/0ac4329b4a811fd79ad51e143d34e8339cf184fc/specs/altair/beacon-chain.md#get_next_sync_committee); [get_next_sync_committee_indices](https://github.com/ethereum/consensus-specs/blob/0ac4329b4a811fd79ad51e143d34e8339cf184fc/specs/altair/beacon-chain.md#get_next_sync_committee_indices) and  [get_active_validator_indices](https://github.com/ethereum/consensus-specs/blob/0ac4329b4a811fd79ad51e143d34e8339cf184fc/specs/phase0/beacon-chain.md#get_active_validator_indices) ]

Once a validator has exited it is no longer in the active set - but for sync committee assignment it appears that get_active_validator_indices is checked 256 epochs before the sync committee. So a validator can be included in the next sync committee (in 256 epochs) then request to exit…their exit can be processed before the sync committee happens.

(Our data team found some instances where this appears to be happening - [Validator 102888 - Open Source Ethereum Blockchain Explorer - beaconcha.in - 2023](https://beaconcha.in/validator/8f1e9fcd9d13b531d2a6b53ba9000ef076efc699bd7c2f12949535e30fde3116ee7d092015aa9303bc4b53f7f72e5312#withdrawals) - note the withdrawal pattern; same thing here: [Validator 114440 - Open Source Ethereum Blockchain Explorer - beaconcha.in - 2023](https://beaconcha.in/validator/b970917e94823dbdfe46fd739bbf6df55651c21833bc644bcd6a70567d6c0e189f558caa8074be73959cda96c6420d68#withdrawals))

I am assuming that currently this isn’t a huge security risk - but, big picture, the idea that a validator is still performing duties but has had their stake withdrawn is a concern (IMHO).

## Replies

**builderbenny** (2023-05-18):

two more points:

- most importantly - this seems to be a pesky edge case - the odds that a validator is exiting AND is assigned to participate in sync committee should be very low (i.e., 512 validators chosen of, currently, about 575,000)
- I was not quite right above - due to withdrawability delay of 256 epochs, a validator requesting to exit after being selected for sync committee would exit at some point during their sync committee period


---
source: magicians
topic_id: 22998
title: Holesky Incident Debrief, February 26, 2025
author: timbeiko
date: "2025-02-26"
category: Protocol Calls & happenings
tags: [testing]
url: https://ethereum-magicians.org/t/holesky-incident-debrief-february-26-2025/22998
views: 411
likes: 6
posts_count: 1
---

# Holesky Incident Debrief, February 26, 2025

# Holesky Incident Debrief Notes

## State of Holesky

- The chain is operating with limited block production on the “canonical” minority chain

Currently seeing 4-8 blocks per epoch (12-25% of expected blocks)
- Goal is to reach 75% block production before coordinating mass slashings
- More peers on the correct chain improves synchronization capabilities
- Stable block production is critical for maintaining chain liveness

## Immediate Action Items (Before ACD Meeting)

1. Priority: Restore Validator Operations

Focus on getting Holesky validators and full nodes back online on the correct chain
2. Client teams to share their latest valid versions on the ACD agenda
3. Instructions for validators:

Enable validators with slashing protection enabled
4. Use this verification method to confirm correct chain: https://gist.github.com/samcm/e2da294dab77e93ad0ee0e815580294f
5. Sepolia Fork Planning

So far, consensus is to proceed with Sepolia fork as scheduled, to confirm on ACDE tomorrow
6. Client teams to confirm their releases for the fork
7. Any concerns about proceeding should be raised immediately
8. Testing Infrastructure

EthPandaOps to begin preparations for pectra-devnet-7, which will:

Support approximately 1 million validators (comparable to mainnet)
9. Allow validator handoffs to staking pools, infrastructure providers, and DVT clusters
10. Include a faucet for manual validator deposits
11. Provide a platform for testing consolidations that can’t be tested on Sepolia

## ACD Follow Ups

1. Holesky Recovery Assessment

If missed slot rate is <25%, begin coordinating controlled slashings of client team validators
2. If above 25%, determine steps to improve block production
3. Sepolia Fork Confirmation

Final decision on fork timing
4. Client teams to confirm release readiness
5. Mainnet Preparation Requirements

Discuss criteria and testing needed before mainnet fork

## Slashing Strategy

- Once more validators are back online, estimate how many are slasheable
- Coordinate slashings in controlled batches to avoid overwhelming the network
- Begin with core developer validators and Genesis validators
- Process will take several weeks to reach finalization (limited by exit rate of 8 per epoch)
- Validators reaching 0 balance through slashing penalties will eventually exit

## Node Operator Guidance

- For synced nodes: Enable validators with slashing protection ON
- For unsynced nodes: Update to latest client release and resync
- Important note: If validators can attest without disabling slashing protection, they likely didn’t attest to the invalid chain

## Next Steps for ACDC (Following Week)

- Teams to share retrospectives on the incident
- Discuss long-term mitigations for similar issues
- Evaluate the effectiveness of the recovery process
- Plan for comprehensive testing of consolidations on devnet-7

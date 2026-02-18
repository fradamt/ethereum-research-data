---
source: magicians
topic_id: 23247
title: Interop Testing Call #30 (March 24, 2025)
author: poojaranjan
date: "2025-03-24"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/interop-testing-call-30-march-24-2025/23247
views: 90
likes: 1
posts_count: 1
---

# Interop Testing Call #30 (March 24, 2025)

**Moderated by:** Parithosh Jayanthi

## Next steps

- Tim Beiko will update the blog post to include the client release details.
- Mikhail and Jochem will work on updating the EIP-6110 specifications with the fixed type approach as suggested by Barnabas.
- Continue the discussion on defining “system call” on the thread at ACD.
- EL team participation in the Peer DAS call is encouraged.

## Updates on Hoodi Testnet

- Network Status:

The network has been live for a week.
- Testing teams have reached out to various entities interested in deposits; most deposits are already done.
- If anyone else is interested, please reach out to Parithosh.
- Expecting the Pectra fork within the next two days.
- Validator Keys are already being handed over to the client team that reached out. Anyone missing should contact the testing team.
- Almost all clients have the release, except for Geth.
- Tim Beiko will update the blog post to include the client release details.

**Mikhail:**

- Noted a participation rate of 95%.
- Would like to maintain a stable participation rate even if it stays at 95%.

**Pari:**

- Informed that most variability is due to the ongoing key handovers.
- Will follow up with other teams to increase participation.
- Suggested that perhaps key handovers should be paused before the fork to ensure stability.
- Shared a validator activity link for reference: Validator Activity Dashboard
- Mentioned that Xatu nodes are currently actively monitoring.

**Mikhail Kalinin:**

- Raised the topic of the parse_deposit_data PR (EIP PR #9460) for discussion if time permits.

## Pectra Devnet 6

- Status:

The network is live and under testing.

**Barnabas:**

- Noted that participation is low, possibly due to issues between Geth and Lighthouse (LH).
- Mentioned that other clients appear to be functioning well.
- Advised that LH and Geth devs should look into the machines.
- Will follow up with the Geth team later.

## EIP-6110 Clarification

- Mikhail:

Discussed two approaches after a conversation with Jochem:

Full Dynamic Approach:

EL (Execution Layer) clients parse data based on the ABI.
- Parsed data is passed directly to the CL (Consensus Layer) without converting it into a fixed type.

**Fixed Layout Approach:**

- EL clients support only the mainnet layout with fixed offsets and sizes for data.

Believes the fixed layout works well from the CL perspective.
Is in favor of fixed specifications but would like feedback from the EL and Testing teams regarding complexities.
Noted that N/m and other clients might require a dynamic approach for adjustments.

**Mario:**

- Raised a concern regarding handling larger fields in the dynamic case.
- Pointed out that testing is simpler with the fixed approach.

**Gajinder Singh:**

- Suggested including the actual bytecode for the deposit contract in the EIP (similar to system contracts) since it is now considered a system contract.
- Proposed that an informational EIP for permissioned chains (e.g., Sepolia) should detail any extra handling required.

**Jochem Brouwer (EthJS):**

- Noted that Sepolia has a different bytecode but maintains the same event layout for the DepositEvent.
- Stated that the current PR explicitly checks the DepositEvent layout and will fail the block if there is a mismatch.
- Shared the PR link again: EIP PR #9460

**Decision:**

- The next step is to proceed with the fixed type approach as suggested by Barnabas.
- Mikhail and Jochem will work on updating the EIP specifications.

## Fail on System Contract

- Parithosh Jayanthi:

Shared the link to the related PR: EIP PR #9508

**Som:**

- Proposed that the system contract should not fail silently if:

No code is found at the address.
- The contract fails but returns the header; in such cases, the block should be invalidated.

Highlighted that Erigon is currently skipping failures silently, possibly due to assumptions about other clients.
Noted that the PR suggests a 30-million-gas limit for the system contract call.

- The expectation is that the call should not consume all 30 million; if it does, it should trigger an out-of-gas error.
- Out-of-gas should be treated as a general failure.

Emphasized that transaction pools should be aware of recurring failures.
Acknowledged that while such behavior is not expected, there is no algorithm in place to alleviate it.

**Jochem Brouwer (EthJS):**

- Asked if the system call concept could be generalized into a broader “system call” EIP since similar issues apply to other system contracts.
- Raised a point regarding generalization in terms of gas limits and other applicable variables.

**Mario Vega:**

- Expressed concern that if the contract is not present at the time of the fork (making the block invalid), it would be impossible to advance the chain.
- Asked about the mechanism to unstuck the chain in such cases.

**Som:**

- Responded that pushing the Pectra timestamp might be the solution.
- Emphasized that the system contract is not optional for Pectra.
- A chain that is not Pectra-ready should not activate this feature.

**Gajinder Singh:**

- Expressed agreement with Som’s proposal.

**Enrico Del Fante (tbenr):**

- Mentioned that the proposal makes sense.

**Ben:**

- Asked whether this mechanism would have stopped issues prior to the Holesky update.
- Som confirmed that it would have, if there would have been the similar issue.

**Additional Discussion:**

- Concerns were raised regarding recoverability and the behavior in withdrawal scenarios.
- Mikhail suggested expanding the discussion to consider a broader generalization of the system call—potentially as a separate EIP.
- Pari mentioned that while generalization could be discussed asynchronously, it is unlikely that any final decisions will be made today.
- There was consensus on the need for community-wide feedback on defining a “system call” as perceptions vary between the community and EIP authors.
- However, Som highlighted the example of Gnosis, of slightly different ways of handling parameters. Thus one definition of system may not be a good idea
- Jochem agreed to the importance of defining the ambiguous “system call” concept due to its heavy implementation specificity.
- Roman emphasized the importance of finalizing the EL spec changes as soon as possible.

**Next Step:**

- Continue the discussion on the thread at ACD.

## Peer DAS

- Status Update:

Devnet 5 continues to run.
- Prysm is experiencing an excessive number of nodes.
- The team is exploring a new file approach.
- Lighthouse (LH) is encountering an issue with consistent column counts, with Dapp Lion working on it.
- An issue between LH and N/m has been reported and is being addressed.
- Aggressive testing is scheduled to begin next week.
- Devnets are currently running with over 10 blobs, and experiments with more client combinations are underway.
- Most clients will be focusing on self-proof computation.
- The next call is scheduled for tomorrow; EL team participation is encouraged.

**Parithosh Jayanthi:**

- Shared PR details from Sunny Side Labs for further reference: Peer DAS Discussion

## EOF Updates

- Danno: No significant update for this week.

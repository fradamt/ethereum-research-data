---
source: magicians
topic_id: 26959
title: EIP-7732 Breakout Room Call #29, December 19, 2025
author: system
date: "2025-12-05"
category: Protocol Calls & happenings
tags: [breakout, epbs]
url: https://ethereum-magicians.org/t/eip-7732-breakout-room-call-29-december-19-2025/26959
views: 45
likes: 0
posts_count: 3
---

# EIP-7732 Breakout Room Call #29, December 19, 2025

### Agenda

#### Specifications & testing

- Clarify setting blob_data_available in PayloadAttestation
- Clarify blob sidecars broadcast section
- Update comparison to quorum value
- Add specs for proposer preferences
- Fix blob_kzg_commitments_root name and bid.block_hash reference
- Set bid.prev_randao in payload bid construction
- Remove validate_merge_block from Gloas specs
- Make builders non-validating staked actors
- Add is_higher_value_bid helper for bid forwarding threshold
- Specify how a proposer can validate a bid
- Remove slot from get_indexed_payload_attestation

#### Implementation updates from client teams

- Prysm
- Lighthouse
- Teku
- Nimbus
- Lodestar
- Grandine

#### Code for HTTP endpoint

- Speaker: @potuz (maybe)
- Discord

> The following came up talking to Yorick and I’d like to add it to the next breakout: CL clients now need to implement the builder side of the builder API. How about the code for the http endpoint?

#### Proposer preferences

- Speaker: @jtraglia
- Add specs for proposer preferences by jtraglia · Pull Request #4777 · ethereum/consensus-specs · GitHub

#### Bid forwarding threshold

- Speaker: @jtraglia
- Add `is_higher_value_bid` helper for bid forwarding threshold by jtraglia · Pull Request #4792 · ethereum/consensus-specs · GitHub

#### Non-validator builders

- Speaker: @jtraglia
- https://github.com/ethereum/consensus-specs/pull/4788
- Discord

> Builders seem to be aligned that they would prefer to avoid the deposit churn than to receive rewards from performing duties. This is a reasonable request that actually makes the spec easier to reason about. However, we don’t want to lose the fallback of P2P bids from actual validators (that’s what actually removes the retirement of self building and that’s what will make the auction healthier by having already existing entities sending bids). I think this is a reasonable ask from builders and we should see how invasive of a design it would be. Adding another non-validator builder slice to the state shouldn’t be much of an issue. Having both mechanisms in place would be perhaps too complicated.

**Meeting Time:** Friday, December 19, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1835)

## Replies

**system** (2025-12-19):

### Meeting Summary:

The meeting began with technical discussions about Zoom permissions and authentication issues, followed by updates from various client teams including PRISM, Lighthouse, and Teku regarding their development progress and merge requests. The team then explored several technical topics including builder API endpoints, proposer preferences, and block import workflows, with particular focus on anti-DOS mechanisms and the potential separation of builders from validators in Ethereum’s consensus mechanism. The conversation ended with discussions about non-validator builders and their implications, including concerns about state bloat and index reuse, along with review of pending PRs and specifications for builder API integration.

**Click to expand detailed summary**

The meeting participants discussed technical issues related to Zoom permissions and account authentication. Mark (EF) resolved the host permission problem for Justin and confirmed that future breakout calls would be integrated into ACDT starting next year. The conversation concluded with a brief discussion about Zoom’s login behavior and its comparison to other video conferencing platforms.

The meeting focused on updates from various client teams. Terence reported that PRISM is waiting for the PR for the state builder to be merged, which will allow further progress. Shane shared that Lighthouse has merged the containers branch into their unstable branch and is working on fork-choice-related changes and payload separations. Enrico provided an update on Teku, mentioning ongoing work on gossip validation and payload attestation. The meeting also discussed the transition of EPBS discussions to ACDT starting in 2026.

The team discussed several topics including builder API endpoints, proposer preferences, and block import workflows. Nico explained the block import flow involving consensus blocks and intermediate beacon states. Caleb reported on integrating payload attestation to validator duties and work on fork-choice mechanisms. The team debated the necessity of implementing builder API endpoints on beacon nodes, with Nico and others expressing doubt about its practicality for solo stakers. Justin presented a PR on proposer preferences, which allows validators and proposers to share peer recipient and gas-limit preferences to builders before proposal slots, and received support from Nico.

The team discussed two main topics: a protocol completion and a bid forwarding threshold. For the protocol, they agreed to wait until the next epoch before allowing builders to submit bids, rather than implementing a more complex system to handle preference distribution. Justin shared a PR in the chat regarding a bid forwarding threshold, which would help prevent DOS attacks by requiring new bids to be a certain percentage (e.g., 3%) more valuable than the previous highest bid. The team was asked for their opinions on this proposal, particularly from builders and Lorenzo.

The team discussed a proposed 3% bidding increment for an anti-DOS mechanism, with Lorenzo expressing concerns about its high value but acknowledging its potential as a fallback option. The group agreed that while the exact number might not be ideal, it could be adjusted later if needed, and terence suggested starting with a reasonable number and increasing it if DOS issues arise. Justin then introduced the topic of non-validator builders, explaining that they prefer faster deposits and smaller staking requirements, leading to a PR that was generally well-received by the team.

The team discussed the implications of separating builders from validators in Ethereum’s consensus mechanism. They debated the technical and security aspects of allowing anyone to become a builder by depositing 1 ETH, with concerns raised about state bloat and index reuse. The group also reviewed open questions on a PR, including whether builders should use withdrawal requests or voluntary exits, and discussed the potential need for a withdrawable epoch field for builders. Bharath mentioned that initial builder API specs were ready for review after the stake builder’s PR is merged.

### Next Steps:

- Justin: Make a new release next week after the group of PRs are merged
- All participants: Review the proposer preferences PR and provide feedback
- All participants: Review the bid forwarding threshold PR and provide feedback on the percentage value
- All participants: Review the non-validator builders PR and approve if in agreement
- Justin: Make the withdrawal request versus voluntary exit change to the non-validator builders PR
- All participants: Comment on the PR regarding whether builders should have a withdrawable epoch field
- All participants: Comment on Mikhail’s suggestion about adding check prior withdrawals in the builder’s withdrawals loop
- Francesco: Link the changes around the edges of ForkChoice pack on Discord after the call
- Bharath: Continue working on the initial builder API specs for review after the staked builder’s PR gets merged
- All participants: Review Bharath’s builder API specs after the staked builder’s PR is merged

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: +&5iW!q&)
- Download Chat (Passcode: +&5iW!q&)
- Download Audio (Passcode: +&5iW!q&)

---

**system** (2025-12-19):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=Fj24f6VsxVg


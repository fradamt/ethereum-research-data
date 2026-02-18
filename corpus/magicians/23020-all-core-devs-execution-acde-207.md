---
source: magicians
topic_id: 23020
title: All Core Devs - Execution (ACDE) #207
author: system
date: "2025-02-28"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-207/23020
views: 1032
likes: 3
posts_count: 4
---

# All Core Devs - Execution (ACDE) #207

# ACDE#207

- March 13, 2025, 14:00-15:30 UTC

 DST warning: double check your local time

90 minutes
Stream: https://youtube.com/live/byrC-fdTOvE

# Agenda

- Pectra

Holesky Path Forward

Option A — Hoodi?

Testing requirements before mainnet
System contract calls error handling
[async review] https://github.com/ethereum/EIPs/pull/9460

Fusaka

- https://github.com/ethereum/EIPs/pull/9378

https://github.com/ethereum/execution-apis/pull/630

Disabling EOF to help PeerDAS testing
[Fork deadlines](https://ethereum-magicians.org/t/eip-7607-fusaka-meta-eip/18439)

- Update dates
- Change days to Mondays to allow Tue/Wed for review before ACDs
- Client team DFI proposals

EIP-4444 progress updates

- debug, eth: define error when accessing pruned chain data by lightclient · Pull Request #636 · ethereum/execution-apis · GitHub

EIP presentations

- EOF PAY opcode
- EIP-7819

Stateless clients for MPTs

Facilitator email: [tim.beiko@ethereum.org](mailto:tim.beiko@ethereum.org)

[GitHub Issue](https://github.com/ethereum/pm/issues/1346)

## Replies

**timbeiko** (2025-03-13):

# Action Items & Next Steps

- Hoodi will launch on 17/03 as a new long-lived testnet, with a short-term focus towards testing validator exits. It will activate Pectra on 26/03.
- A mainnet fork time for Pectra will only be chosen after Pectra successfully activates on Hoodi and client teams feel confident in the state of testing. Mainnet will be scheduled at least 30 days after the Hoodi fork (April 25 or later).
- Fusaka Planning Timelines

March 24: deadline for EIPs to be Proposed for Inclusion in Fusaka
- March 31: deadline for client teams to share their preferences about scope
- April 10: Fusaka scope frozen

# Summary

## Pectra

- We discussed potential post-Holesky path forwards and agreed to “Plan A”: launching a new testnet.

This will enable us to test validator exists, which is impossible on Holesky right now given the exit queue will take ~1 year to empty.
- All other Pectra functionality, including validator consolidations, can still be tested on Holesky and Sepolia.
- This option was chosen to avoid client teams writing custom code to clear the Holesky exit queue (“Plan D”), which could lead to further bugs and delay work on Pectra fixes and Fusaka implementations.

[Hoodi](https://notes.ethereum.org/@ethpandaops/hoodi) will launch next Monday March 17 and activate the Pectra network upgrade on Wednesday March 26.

- The network will have the same configuration settings as mainnet, and a similar validator count.

Staking operators and infrastructure providers who must test Pectra validator exists should deploy to Hoodi ASAP.
Once Pectra successfully activates on Hoodi, a mainnet fork time for Pectra will be chosen. This will be at least 30 days after the Hoodi fork, but potentially farther out if infrastructure providers need more time to test on Hoodi.
In parallel to this, client teams will continue testing the various Pectra features across Holesky, Sepolia and the various test suites. Specific test scenarios include:

- Attestation packing
- Slashing inclusion in blocks
- Failure cases for system contract calls
- Parsing deposit contract data

## Fusaka

- Agreement to move forward with Felix’s suggestions to add proofs to transaction payloads.

Teams should review the corresponding Engine API PR

Fusaka Planning Timelines

- March 24: deadline for EIPs to be Proposed for Inclusion in Fusaka
- March 31: deadline for client teams to share their preferences about scope, including which EIPs they think should be Declined for Inclusion.
- April 10: Fusaka scope frozen

We could not review two proposed EIPs ([PAY opcode](https://docs.google.com/presentation/d/1pZgbr5yLaSNxpwRdixgkAV9mfo_gql448_iSOVKlyvA/edit#slide=id.p) and [EIP-7819](https://eips.ethereum.org/EIPS/eip-7819)) on the call directly. While we will try and make space for them on subsequent ACD calls, champions are encouraged to provide materials that can be reviewed async and/or in breakout rooms.

## Other Topics

- Client review requested: History Expiry JSON RPC error codes
- Postponed/async: Stateless MPT Clients

---

**abcoathup** (2025-03-13):

## Audio

## Writeups

- Crypto & Blockchain Research Reports | Galaxy @Christine_dkim
- Highlights of Ethereum's All Core Devs Meeting (ACDE) #207 @yashkamalchaturvedi

---

**yashkamalchaturvedi** (2025-03-14):

![image](https://etherworld.co/favicon.png)

      [EtherWorld.co – 13 Mar 25](https://etherworld.co/2025/03/13/highlights-of-ethereums-all-core-devs-meeting-acde-207/)



    ![image](https://etherworld.co/content/images/2025/03/EW-Thumbnails--1---1-.jpg)

###



Holesky Finalized, Hoodi Testnet
Pectra Mainnet Plan, Fusaka Updates, System Contract Error Handling, RPC Changes & Stateless Clients


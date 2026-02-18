---
source: magicians
topic_id: 23168
title: Interop Testing Call #29 (Mar 17, 2025)
author: poojaranjan
date: "2025-03-17"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/interop-testing-call-29-mar-17-2025/23168
views: 107
likes: 2
posts_count: 1
---

# Interop Testing Call #29 (Mar 17, 2025)

## Launch of Hoodi Network

- Pectra testing can continue on Holesky as it is finalized.
- Eth Panda team is managing most of the validators and transitioning key ownership to clients.
- Hoodi is live and finalizing:

Dora Explorer
- Hoodi Dashboard

### Discussion on Hoodi Launch

- Tim Beiko

Asked about the fork slot/epoch → Epoch 2048

**Parithosh Jayanthi**

- Shared Hoodi repo: GitHub

**Barnabas**

- Confirmed 8192 slots.

**nflaig (Lodestar, ChainSafe)**

- Lodestar update: 1.28.0-rc.0 now available with --network hoodi flag.
- A stable release will follow soon.

**Validator Transition:**

- Parithosh confirmed that they are already in touch with Lido and Coinbase regarding migration.
- Som (Erigon) suggested testing RPC transactions, especially for 7702-related bugs.
- Pari mentioned the Hive test suites might provide more insights. But, will need to be confirmed from the testing team.

## Holesky Testnet & Option D Discussion

- nflaig (Lodestar, ChainSafe)

Asked if there is still interest in Option D for Holesky.
- Shared a PoC: GitHub PR #7570.

**Tim Beiko**

- I thought we agreed to not do it to save core dev time?

**Parithosh Jayanthi**

- Agreed that Option D should only proceed if it’s significantly easier than expected. He thinks its better to discuss the POC and then decide if it is worth it or easier approach than expected.
- ACD team is already considering deprecating Holesky.

**Nico (Lodestar)** explained the PoC for Holesky revival also argued that community may have option to run custom branch for this. However, Parithosh has concerns about this flexibility of custom branch options.

- Alex: This doesn’t affect the exit queue knowledge.
- Pari: Only exit queue is broken in Holesky; other tests can proceed. Tooling is already there, people are already deploying it. So, will increase the gas limit as Holesky has already lot of community nodes running. He suggested to continue running it for the short term (approx half a year) and then take the call.
- Barnabas: Memory issues reported on devnet 6 with 60M gas, might not see a longer non finality period with heavy blocks on holesky.
- nixo: Predicts community nodes will start shutting down.

### Future of Holesky:

- Matthew Keil: Questioned the need to keep Holesky running if Hoodi is live.
- Pari: Prefers keeping it running for a few more months to ensure smooth migration. Purely for giving time for Hoodi. Tooling takes a long time to come up. Considering Lido is also looking for migration, Devops team are open to take over validators. So, if any client team wants to get rid of validators, reach out to devops team.
- Barnabas: RPC Provider available at rpc.hoodi.ethpandaops.io.

### Decision:

- Option D isn’t considered at the moment.
- Holesky will be there for the next 6 months as playground for Client devs and will aslo be giving the community the option to migrate to Hoodi in the meantime.

On a related note, Danno [documented](https://hackmd.io/@shemnon/eth_config) ***RPC method that provides node-relevant configuration data for the current and next fork***. This will be published tomorrow, he requested review and feedback.

## Devnets

- Pectra devnet is live and running.
- Devnet 6 Updates:

Gas limit increased to 60M.
- Barnabas: Primarily affects Besu & Teku (Java-based clients).
- Matthew Keil: Asked for a list of clients with memory issues.
- Danno Ferrin (Ipsilon): Java garbage collection is memory-hungry.
- nflaig: Requested SSZ support for Engine API.

## EIP-6110 Discussion

- Jochem (EthJS)

wanted to discuss a clarification for EIP-6110 (this clarification is rather theoretical since it only applies to (test)nets where the DepositEvent emits data of different length than expected (i.e the emitted data on mainnet/holesky/sepolia))
- Noted that the parse deposit method is not defined in EIP-6110.
- Two possible solutions:

Hardcode the offsets and sizes.
- Use ABI-based parsing.
- Marius: Prefers hardcoding over using an ABI library in consensus code or doing nothing.
- Łukasz Rozmej: Suggested reading first 5 words (32 bytes each) to determine length.
- Pari: Wants to align with precompiles to avoid invalid block production.
- Ben Adams: Clarified that ABI format is fixed and includes offsets/lengths.

**Next Steps:**

- Discussion to be continued async.
- Clients may add comment to this EIPs PR
- Jochem: Will link the discussion thread on ACD meeting.

## Handling System Contract Failures

- Som (Erigon): Asked about failures in system contracts (e.g., withdrawals).
- Pari:

Safe option is skipping failed transactions to avoid mempool-triggered bugs.
- Concerned this could create a forking issue for clients without the bug.

**Ben Adams**:

- Emphasized fixed ABI format without needing an ABI decoder.

**Mario Vega**:

- If the execution result differs, it indicates an invalid block.

**Pari**:

- Plans to engage the CL team for further discussions.

## Peer DAS

- Devnet 5 is live and running.
- 60% full nodes with malicious nodes at 60-80%.
- One bug identified and fixed.
- Unrelated bugs found on Lighthouse.
- Breakout room meeting scheduled for next day.

## EOF

- Besu & EVM1 working on implementations for Devnet 1.
- Pari:

EOF and PeerDAS are running on the same testnet, making separation difficult.
- Need to discuss EOF checkpointing.
- Geth and Nethermind need updates.

**Danno (Ipsilon)**:

- Suggested adding a switch for better control.

## Next Steps

- Testing on Devnet 6 to continue this week.
- Findings from Holesky & Hoodi to be presented on All Core Devs (ACD) call.
- Encourage teams to fill out retro feedback form: Ethereum Pad.
- Expect client releases before end of the week (EOW).

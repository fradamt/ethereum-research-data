---
source: magicians
topic_id: 25992
title: Gas repricing Breakout Room #1, October 29, 2025
author: system
date: "2025-10-27"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/gas-repricing-breakout-room-1-october-29-2025/25992
views: 49
likes: 0
posts_count: 4
---

# Gas repricing Breakout Room #1, October 29, 2025

### Agenda

- [15 min] Intro to repricing and why it is important by @misilva73 and @adietrichs
- State EIP deep dives [5 min each]:

EIP-2780: Reduce intrinsic transaction gas by @benaadams
- EIP-7973: Warm Account Write Metering @misilva73
- EIP-8032: Size-Based Storage Gas Pricing by @gballet
- EIP-8037: State Creation Gas Cost Increase by @misilva73
- EIP-8038: State-access gas cost update by @misilva73
- EIP-8058: Contract Bytecode by Deduplication Discount by @CPerezz
- EIP-2926: Chunk-Based Code Merkleization by @gballet

**Meeting Time:** Wednesday, October 29, 2025 at 15:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1784)

## Replies

**system** (2025-10-29):

YouTube recording available: https://youtu.be/f_1sTYTY9DY

---

**system** (2025-10-29):

### Meeting Summary:

The meeting focused on discussing various Ethereum Improvement Proposals (EIPs) related to gas pricing and transaction costs, with presentations covering proposals to reduce intrinsic transaction gas, implement warm account rights, and address large spammy contracts through size-based storage gas pricing. The group explored proposals for state creation and access harmonization, bytecode duplication discounts, and chain-based code verkleization to improve efficiency and performance. The conversation ended with plans for a follow-up discussion on remaining EIPs the following week.

**Click to expand detailed summary**

Maria introduced the meeting’s focus on repricing efforts in Glamsterdam, emphasizing its importance for scaling Layer 1 and harmonizing operations across different resources to remove bottlenecks. She outlined three categories of EIPs related to repricing: broad harmonization, pricing extensions, and supporting EIPs, and explained the prioritization strategy, starting with broad harmonization to ensure balanced scaling. Maria set a 5-minute time limit for each EIP presentation and planned to start with Ben discussing reducing intrinsic transaction gas.

The meeting focused on several Ethereum Improvement Proposals (EIPs) related to gas pricing and transaction costs. Ben presented a proposal to reduce the intrinsic gas of transactions, which would lower the base transaction cost to $4,500 and introduce cheaper costs for certain operations like no-code warmings and call value transfers. Maria discussed an EIP about warm account rights, which would allow batched state root calculations and reduce costs for multiple account updates within a transaction. Guillaume presented an EIP targeting large, spammy contracts by introducing size-based storage gas pricing, which would charge more gas per storage slot for contracts exceeding a certain size. The group acknowledged that the exact numbers in these proposals may need to be adjusted based on final benchmarks and agreed that breaking certain gas pricing assumptions in existing contracts might be necessary for scalability improvements.

The meeting focused on a discussion about a proposed EIP related to contract storage and gas costs. Guillaume explained that the proposal involves a simpler version of a vertical transition that has already been extensively tested. Ansgar expressed concerns about the complexity of the mechanism and potential edge cases, but acknowledged its potential efficiency improvements. Ben and Toni discussed the threshold for affecting contracts, with Toni suggesting a dynamic threshold based on contract size. The group also touched on the impact of increased gas costs on contract calls and the need to coordinate changes across clients.

Maria presented two EIPs related to state creation and access harmonization. The first proposal aims to control state growth by increasing costs for state creation, with concerns raised about the magnitude of price increases and their impact on user experience. The second proposal addresses state access costs, with a focus on harmonizing gas parameters and improving performance. CPerezz discussed an EIP on bytecode duplication discounts, which would reduce costs for deploying existing contract code. Guillaume presented on chain-based code verkleization, which aims to improve code loading efficiency by breaking code into chunks and only loading necessary parts. The conversation ended with a reminder about a follow-up discussion on remaining EIPs the following week.

### Next Steps:

- Pooja: Upload the recorded meeting later for people to watch
- Maria and Charles: Benchmark warm account rights costs and finalize numbers, considering DDoS protection vectors
- Maria: Discuss and determine appropriate threshold and target parameters for state creation harmonization
- Maria: Use state benchmarks to determine final numbers for state access harmonization Gas parameters
- Carlos : Ensure the bytecode duplication discounts EIP PR is merged to the PFI list
- All participants: Continue discussions and comments in the Discord channel called "EVM Pricing

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: =3f3FzuF)
- Download Chat (Passcode: =3f3FzuF)

---

**system** (2025-10-30):

### Meeting Summary:

The meeting focused on discussing various Ethereum Improvement Proposals (EIPs) related to gas pricing and transaction costs, with presentations covering proposals to reduce intrinsic transaction gas, implement warm account rights, and address large spammy contracts through size-based storage gas pricing. The group explored proposals for state creation and access harmonization, bytecode duplication discounts, and chain-based code verkleization to improve efficiency and performance. The conversation ended with plans for a follow-up discussion on remaining EIPs the following week.

**Click to expand detailed summary**

Maria introduced the meeting’s focus on repricing efforts in Glamsterdam, emphasizing its importance for scaling Layer 1 and harmonizing operations across different resources to remove bottlenecks. She outlined three categories of EIPs related to repricing: broad harmonization, pricing extensions, and supporting EIPs, and explained the prioritization strategy, starting with broad harmonization to ensure balanced scaling. Maria set a 5-minute time limit for each EIP presentation and planned to start with Ben discussing reducing intrinsic transaction gas.

The meeting focused on several Ethereum Improvement Proposals (EIPs) related to gas pricing and transaction costs. Ben presented a proposal to reduce the intrinsic gas of transactions, which would lower the base transaction cost to $4,500 and introduce cheaper costs for certain operations like no-code warmings and call value transfers. Maria discussed an EIP about warm account rights, which would allow batched state root calculations and reduce costs for multiple account updates within a transaction. Guillaume presented an EIP targeting large, spammy contracts by introducing size-based storage gas pricing, which would charge more gas per storage slot for contracts exceeding a certain size. The group acknowledged that the exact numbers in these proposals may need to be adjusted based on final benchmarks and agreed that breaking certain gas pricing assumptions in existing contracts might be necessary for scalability improvements.

The meeting focused on a discussion about a proposed EIP related to contract storage and gas costs. Guillaume explained that the proposal involves a simpler version of a vertical transition that has already been extensively tested. Ansgar expressed concerns about the complexity of the mechanism and potential edge cases, but acknowledged its potential efficiency improvements. Ben and Toni discussed the threshold for affecting contracts, with Toni suggesting a dynamic threshold based on contract size. The group also touched on the impact of increased gas costs on contract calls and the need to coordinate changes across clients.

Maria presented two EIPs related to state creation and access harmonization. The first proposal aims to control state growth by increasing costs for state creation, with concerns raised about the magnitude of price increases and their impact on user experience. The second proposal addresses state access costs, with a focus on harmonizing gas parameters and improving performance. CPerezz discussed an EIP on bytecode duplication discounts, which would reduce costs for deploying existing contract code. Guillaume presented on chain-based code verkleization, which aims to improve code loading efficiency by breaking code into chunks and only loading necessary parts. The conversation ended with a reminder about a follow-up discussion on remaining EIPs the following week.

### Next Steps:

- Pooja: Upload the recorded meeting later for people to watch
- Maria and Charles: Benchmark warm account rights costs and finalize numbers, considering DDoS protection vectors
- Maria: Discuss and determine appropriate threshold and target parameters for state creation harmonization
- Maria: Use state benchmarks to determine final numbers for state access harmonization Gas parameters
- Carlos : Ensure the bytecode duplication discounts EIP PR is merged to the PFI list
- All participants: Continue discussions and comments in the Discord channel called "EVM Pricing

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: =3f3FzuF)
- Download Chat (Passcode: =3f3FzuF)


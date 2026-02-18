---
source: magicians
topic_id: 22346
title: All Core Devs - Execution (ACDE) #203, January 16, 2025
author: abcoathup
date: "2024-12-27"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-203-january-16-2025/22346
views: 445
likes: 12
posts_count: 5
---

# All Core Devs - Execution (ACDE) #203, January 16, 2025

#### Agenda

[Execution Layer Meeting 203 · Issue #1227 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1227) moderated by [@timbeiko](/u/timbeiko)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #203, January 16, 2025](https://ethereum-magicians.org/t/all-core-devs-execution-acde-203-january-16-2025/22346/4) [Protocol Calls & happenings](/c/protocol-calls/63)




> Action Items
>
> Teams should review the EIP-7702 “delegation instrospection” proposal by Monday, with the expectation of making a final spec decision on Monday’s testing call.
> Merge the PR adding  baseFeeUpdateFraction to the EIP-7840 configs by Monday
> Clarify the EIP-7691 fork boundary behaviour in the EIP by Monday
> Update EIP-2537 to mandate the use of integer division for the G2 operation by Monday
> Confirm Pectra testnet deployment timestamps on next week’s ACDC
> @jflo will coordinate a breakout…

#### Recording

  [![image](https://img.youtube.com/vi/uh1hZCE4k0w/maxresdefault.jpg)](https://www.youtube.com/watch?v=uh1hZCE4k0w&t=232s)

#### Additional info

- Pectra-devnet-5 live
- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim
- Highlights of Ethereum's All Core Devs Meeting (ACDE) #203 by @yashkamalchaturvedi

## Replies

**yashkamalchaturvedi** (2025-01-17):

Call Highlights: [Highlights of Ethereum's All Core Devs Meeting (ACDE) #203](https://etherworld.co/2025/01/17/highlights-of-ethereums-all-core-devs-meeting-acde-203/)

---

**timbeiko** (2025-01-17):

This is great, [@yashkamalchaturvedi](/u/yashkamalchaturvedi)! Thank you for putting it together so promptly ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)!

I had a draft summary that I’ll paste here as well, but it’s nice to see others stepping in to recap what happened!

---

**timbeiko** (2025-01-17):

# Action Items

- Teams should review the EIP-7702 “delegation instrospection” proposal by Monday, with the expectation of making a final spec decision on Monday’s testing call.
- Merge the PR adding  baseFeeUpdateFraction to the EIP-7840 configs by Monday
- Clarify the EIP-7691 fork boundary behaviour in the EIP by Monday
- Update EIP-2537 to mandate the use of integer division for the G2 operation by Monday
- Confirm Pectra testnet deployment timestamps on next week’s ACDC
- @jflo will coordinate a breakout for client teams to discuss JSON-RPC standadization
- @kevaundray will create an informational EIP to document node’s minimum hardware and bandwidth requirements in different contexts, @timbeiko will open a discord channel to discuss the topic
- EIP Editor Workshop Jan 17, 16:00 UTC

# Call Summary

## Pectra

### Spec Changes

- devnet-5 went live 30 minutes before ACDE’s start, with Pectra activating 4 minutes before.

Erigon encountered a gas estimation issue which is being investigated
- The devnet includes recent changes to EIP-7623

Teams agreed to store `baseFeeUpdateFraction` in the EIP-7840 configs ([PR](https://github.com/ethereum/EIPs/pull/9240)), to be merged by Monday’s testing call
Teams agreed to clarify EIP-7691 to specify that, on the fork block, the Pectra parameters will be used, matching many of the current implementations. The testing team has a PR (**ADD LINK**) already and one for the EIP will follow by Monday.
EIP-2537 does not currently specify how to handle divisions in the G2 call, causing issues with recent gas pricing changes. Instead of updating the gas costs, as originally [proposed](https://github.com/ethereum/EIPs/pull/9245), the EIP will be updated to mandate using integer division.
Otim labs proposed adding [“delegation instrospection”](https://hackmd.io/@otim/H1Q7yCHDyl#) to EIP-7702, allowing for `EXTCODE*` opcodes to act on the “delegation designator” rather than just the prefix. Teams were generally positive but some of them needed to review the proposal further and were concerned about the impact on testing. The devops team confirmed this change could be tested in upcoming shadow forks, even if we do not have further devnets. We agreed to make a final decision about the proposal on Monday’s testing call.

### Audits

- Audit results for Pectra system contracts will be presented on the next ACDE. None of the audits found significant issues in the contracts, and all minor issues have been fixed in the current versions of the contract.

### Testnet Deployment

- On next week’s ACDC, we plan to finalize the testnet deployment schedule for Pectra. Teams agreed to combine the activation for both Holesky and Sepolia into a single client release. The proposed schedule is:

Feb 3: Client releases deadline
- Feb 4-5: Public announcement
- Feb 12: Holesky Fork
- Feb 19: Sepolia Fork

### Gas Limit

- Several teams already updated their default configurations to have a 36M gas limit
- We agreed to increase the Holesky gas limit to 60M once Pectra is deployed on the network, and then further once Pectra is deployed on mainnet.

## JSON RPC Standardization

- Felix presented his views on the current state of JSON-RPC standardization
- Teams agreed to focus on passing common test suites and to discuss ways to gather input from JSON-RPC users such as L2s, wallets and infrastructure providers to help shape the evolution of the spec.
- A first breakout will be organized for client teams to further discuss implementation status, and a second one to bring in non-client teams and gather their input.

## Node Requirements

- Kev requested feedback on his node requirement (ADD LINK) document, as well as a proposal to specify minimal bandwidth requirements.
- We agreed to merge these into a single informational EIP, and create a specific discord channel to continue conversations on the topic.

### EIP Editor Workshop

- EIP editors are organizing a workshop on Jan 17 to introduce new contributors to EIP reviews and editing: EIP Editors' Workshop · Issue #372 · ethcatherders/EIPIP · GitHub

---

**claravanstaden** (2025-01-21):

Hi Tim! I work on an Ethereum-Polkadot bridge and I have been updating our Ethereum light client with the Pectra updates. Our on-chain code (including fork version config) needs to go through an on-chain governance process that can take up to a month. I would like to ask at least a month’s notice from when mainnet’s Electra epoch is announced, to the actual fork epoch. I remember the Deneb fork epoch was announced 5 weeks or so before the fork epoch, which would be great if the same could be done for Electra.


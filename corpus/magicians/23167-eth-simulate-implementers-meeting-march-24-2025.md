---
source: magicians
topic_id: 23167
title: Eth_simulate Implementers' Meeting | March 24, 2025
author: system
date: "2025-03-17"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eth-simulate-implementers-meeting-march-24-2025/23167
views: 70
likes: 0
posts_count: 2
---

# Eth_simulate Implementers' Meeting | March 24, 2025

# eth_simulate Implementers’ Meeting

- Date and time in UTC March 24, 2025, 12:00 UTC
- Duration in minutes: 60 minutes
- Join Zoom Meeting
- Recording: eth_multicall Playlist

### Resources

[Ideas for eth_simulateV2](https://hackmd.io/@xHso_0ENSqWWLKt_lOqVuA/S1KtbtYTA)

[PEEPanEIP#135: Eth Simulate with Oleg and Killari](https://youtu.be/4uZyQQ6qz4U)


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-4399)





###



Expose beacon chain randomness in the EVM by supplanting DIFFICULTY opcode semantics











      ![](https://docs.login.xyz/~gitbook/image?url=https%3A%2F%2F4020722360-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252Fhsp8Jza9wShYT1iNJ5iM%252Ficon%252Fx4mZ08iyOwFzdTr7zvZH%252FGroup%252012%2520%281%29.png%3Falt%3Dmedia%26token%3D0e89a6f5-1606-4fe9-85b1-2ec5c8fb6734&width=48&height=48&sign=a4502db5&sv=2)

      [docs.login.xyz](https://docs.login.xyz/general-information/siwe-overview)



    ![](https://docs.login.xyz/~gitbook/image?url=https%3A%2F%2F4020722360-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252Fhsp8Jza9wShYT1iNJ5iM%252Fsocialpreview%252FLNXkKyWuvVzbG9vdS8xT%252FScreen%2520Shot%25202022-01-11%2520at%25207.22%25201.png%3Falt%3Dmedia%26token%3Db1e76dab-8c24-40c3-854a-77c0d077db6f&width=1200&height=630&sign=533e3457&sv=2)

###



Sign-In with Ethereum - For Web2 and Web3










https://ethresear.ch/t/fork-choice-enforced-inclusion-lists-focil-a-simple-committee-based-inclusion-list-proposal/19870

# Agenda

- [Notes from the last meeting]
- Client Implementation update
- Test
- Discuss spec for eth_simulateV2

Add more discussion items or async updates.

The next meeting is scheduled for March 31, 2025 at 12:00 UTC

[GitHub Issue](https://github.com/ethereum/pm/issues/1388)

## Replies

**shaharblockaid** (2025-03-20):

Few points I have on this new spec:

1. Why go for a specific implementation for contract creation and native tracer (traceTransfers). Just give the user the full transaction traces. The foundation can describe an example utility code for extracting these “events” from raw traces, which gives maximum flexibility for all use cases
2. The goal of this spec is to "enables simulation of complex transactions", however it is still lacking existing functionality in debug_traceCall. For example, the Bybit Exploit (mainnet - 0x46deef0f52e3a983b67abf4714448a41dd7ffd6d32d32da69d62081c68ad7882) cannot be detected in this proposed RPC, as I understand that eth_simulateV2 doesn’t contain storage state diffs (pre,  post)


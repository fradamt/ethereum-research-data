---
source: magicians
topic_id: 24118
title: All Core Devs - Execution (ACDE) #212 (May 22, 2025)
author: system
date: "2025-05-09"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-212-may-22-2025/24118
views: 427
likes: 6
posts_count: 7
---

# All Core Devs - Execution (ACDE) #212 (May 22, 2025)

- May 22, 2025, 14:00-15:30 UTC
- Stream
- Ethereum Protocol Calls Calendar subscription

# Agenda

- Fusaka planning

SFI EIPs for devnet-1
- DFI EIPs that won’t make it in devnet-2

[Testnet deployment strategy](https://github.com/ethereum/pm/issues/1533#issuecomment-2884373810)
Glamsterdam planning process

- Community Consensus, Fork Headliners & ACD Working Groups
- Glamsterdam scoping proposal

ACD Breakout Room Reviews
ACD input collection

- [For an ACD platform](https://ethereum-magicians.org/t/for-an-acd-platform/24098)

- [All Core Devs (ACD)](https://ethereum-magicians.org/t/all-core-devs-acd/24198)
Review requests

- Standardize JSON-RPC Error codes · Issue #658 · ethereum/execution-apis · GitHub
- EIP-7939: Count leading zeros (CLZ) opcode
- Add EIP: Indexed Storage by keyvank · Pull Request #9792 · ethereum/EIPs · GitHub

 **🤖 config**

- Duration in minutes : 90
- Recurring meeting : true
- Call series : ACDE
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : false #
- Already on Ethereum Calendar : false #
- Need YouTube stream links : true #
- Facilitator email: tim@ethereum.org
Note: The zoom link will be sent to the facilitator via email



[GitHub Issue](https://github.com/ethereum/pm/issues/1533)

## Replies

**abcoathup** (2025-05-13):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #212 (May 22, 2025)](https://ethereum-magicians.org/t/all-core-devs-execution-acde-212-may-22-2025/24118/3) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDE #212 Summary
> Action Items
>
> Devnet-0 Launch (May 26)
>
>
> Fusaka Devnet-0 launching with:
>
> EIP-7594 (PeerDAS)
> EIP-7823 (MODEXP Upper Bounds)
> EIP-7883 (ModExp Gas Cost Increase)
> EIP-7892 (BPO Forks)
>
>
>
>
> Devnet-1 EIPs moved to SFI
>
>
> Devnet-1 (ETA June 9) confirmed to include:
>
> EIP-7825 (Transaction Gas Limit Cap)
> EIP-7918 (Blob Base Fee bounded by Execution Cost)
>
>
>
>
> CFI Review for Devnet-2
>
>
> Teams to finalize Devnet-2 scope within two weeks, reviewing:
>
> EIP-7907 (Meter Contract Code Size & Incre…

### Recordings

  [![image](https://img.youtube.com/vi/FEZGRUPkI_8/maxresdefault.jpg)](https://www.youtube.com/watch?v=FEZGRUPkI_8&t=209s)



      [x.com](https://x.com/EthCatHerders/status/1925537133525160328)





####

[@](https://x.com/EthCatHerders/status/1925537133525160328)



  https://x.com/EthCatHerders/status/1925537133525160328










### Writeups

- Highlights from the All Core Developers Execution (ACDE) Call #212 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Glamsterdam scoping timeline

---

**timbeiko** (2025-05-22):

## ACDE #212 Summary

### Action Items

1. Devnet-0 Launch (May 26)

- Fusaka Devnet-0 launching with:

EIP-7594 (PeerDAS)
- EIP-7823 (MODEXP Upper Bounds)
- EIP-7883 (ModExp Gas Cost Increase)
- EIP-7892 (BPO Forks)

1. Devnet-1 EIPs moved to SFI

- Devnet-1 (ETA June 9) confirmed to include:

EIP-7825 (Transaction Gas Limit Cap)
- EIP-7918 (Blob Base Fee bounded by Execution Cost)

1. CFI Review for Devnet-2

- Teams to finalize Devnet-2 scope within two weeks, reviewing:

EIP-7907 (Meter Contract Code Size & Increase Limit)
- EIP-7934 (RLP Execution Block Size Limit)
- EIP-5920 (PAY Opcode)
- EIP-7212 (Precompile for secp256r1 Curve Support) – Requires rewrite; Nico & Stokes coordinating

1. CL EIP Review

- Teams to decide on EIP-7917 (Deterministic Proposer Lookahead) during next week’s CL call.

---

### Summary

#### Fusaka Devnets Progress

- Devnet-0 set for launch on May 26 ; majority of clients integrated. Nimbus and Lighthouse updates pending.
- Hive tests flagged initial issues linked to EIP-7823; teams actively working on resolutions.
- Network partition tests suggest additional review needed.
- New Consensus specs released: v1.6.0-alpha.0.

#### Fusaka EIP Scope Decisions

- Transaction Gas Limit Cap (EIP-7825) (SFI – Devnet-1):

Set at 30M gas; consensus on necessity for handling DoS risk and complexity amid rising gas limits.
- Considerations around AA bundles and zkEVM parallelization highlighted; flexibility retained for future adjustments.

**Blob Base Fee (EIP-7918)** (SFI – Devnet-1):

- Intended to stabilize blob fee market by linking blob fees to execution gas base fee, preventing unpredictable tip spikes.
- Strong support from L2 teams; constant parameter remains tunable based on upcoming test results.

**Pending CFI Reviews (Devnet-2)** :

- EIP-7907 (Meter Contract Code Size) : Broadly supported; Nethermind to produce performance benchmarks within two weeks due to state implications concerns.
- EIP-7934 (RLP Block Size Limit) : Active debate on enforcement (EL vs CL), computational impact, and precise implementation strategy. Decision deferred two weeks to finalize design.
- EIP-7212 (secp256r1 Precompile) : Widely recognized importance but flagged for immediate rewrite. Nico & Stokes volunteered as champions; final decision pending clarification and rewrite.
- EIP-5920 (PAY Opcode) : Mixed support, concerns around MEV relay compatibility; further review needed.

**EIP-7762 (Increase MIN_BASE_FEE_PER_BLOB_GAS)** officially moved to **DFI**.

#### Testnet Strategy

- Teams agreed to explicitly fork Sepolia first, preserving Hoodi as critical app-testing environment prior to mainnet forks.
- Community-driven long-term testnets preferred due to resource constraints and maintenance challenges.
- Encouragement for improved tooling and clearer communication for app developers.

#### RPC Standardization Proposal

- Introduction of proposals for standardized JSON-RPC error handling.
- Detailed discussions deferred to next dedicated RPC standardization call.

#### Additional Deferred Items

- Glamsterdam fork planning deferred to next ACDE call pending Fusaka finalization.

---

### Next Steps

- May 26 : Fusaka Devnet-0 launch.
- Next Week’s CL Call : Decision on EIP-7917 (Deterministic proposer lookahead).
- Next ACDE Call (two weeks) : Teams to finalize Devnet-2 scope, reviewing updated proposals for EIPs 7212, 7934, 7907, and 5920. Glamsterdam discussions to commence following Fusaka scope finalization.

Teams should review EIP updates and testing statuses thoroughly ahead of upcoming calls to ensure clear, informed discussions and efficient decision-making. For detailed discussions and technical context, teams should refer to the [call recording](https://www.youtube.com/live/FEZGRUPkI_8?t=209s).

---

**poojaranjan** (2025-05-22):

ACDE 212 on [EthCatHerders Podcast](https://open.spotify.com/episode/3t4EVhwrVsEqsBoyq3IqOV?si=DPaKn8SMQUC-Zw41bIjDQw) &  [X](https://x.com/EthCatHerders/status/1925537133525160328)

---

**jochem-brouwer** (2025-05-22):

Hi Tim, you link to ACD 211 here (in call recording) ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) Link should be https://www.youtube.com/watch?v=FEZGRUPkI_8

Is there a chat dump somewhere? [@poojaranjan](/u/poojaranjan)

---

**jochem-brouwer** (2025-05-22):

Previous post flagged as spam. Sigh.

Your link links to ACD 211.

[@poojaranjan](/u/poojaranjan) is there a chat dump of the call somewhere?

---

**poojaranjan** (2025-05-22):

Ideally, the bot should automatically upload the caption or chat file, but since it follows a fixed schedule, there might be some delays. In the meantime, I’m happy to share the file via Discord/Telegram, as this forum doesn’t support .txt file uploads.


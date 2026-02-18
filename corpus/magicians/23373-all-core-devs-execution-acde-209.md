---
source: magicians
topic_id: 23373
title: All Core Devs - Execution (ACDE) #209
author: system
date: "2025-04-03"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-209/23373
views: 520
likes: 3
posts_count: 3
---

# All Core Devs - Execution (ACDE) #209

# All Core Devs - Execution (ACDE) #209

- April 10, 2025, 14:00-15:30 UTC
- 90 minutes
- Stream: TBA

# Agenda

- Pectra
- Fusaka

Scope finalization

PFI vs. CFI vs. SFI
- Synchronous vs. async presentations

[Reconfiguring AllCoreDevs](https://ethereum-magicians.org/t/reconfiguring-allcoredevs/23370)

---

Facilitator email: [tim@ethereum.org](mailto:tim@ethereum.org)

[GitHub Issue](https://github.com/ethereum/pm/issues/1414)

## Replies

**abcoathup** (2025-04-05):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #209](https://ethereum-magicians.org/t/all-core-devs-execution-acde-209/23373/3) [Protocol Calls & happenings](/c/protocol-calls/63)




> Summary
> Pectra
>
> Client Releases expected by April 21
> EIP-7702: clients will not include the delegation status in the transaction receipt, but may add it to JSON-RPC for recent blocks. Conversation to continue here.
>
> Fusaka
>
> We clarified that today’s call was the deadline for moving EL EIPs from PFI to CFI, and ACDC next week will be the same for CL EIPs.
> We moved the following EIPs to CFI:
>
> EIP-7823: Set upper bounds for MODEXP
> EIP-7825: Transaction Gas Limit Cap
> EIP-7907: Meter Contract Code Si…

### Recordings

  [![image](https://img.youtube.com/vi/_j4XPNQxDPc/maxresdefault.jpg)](https://www.youtube.com/watch?v=_j4XPNQxDPc&t=186s)



      [x.com](https://x.com/EthCatHerders/status/1910331460478714195)





####

[@](https://x.com/EthCatHerders/status/1910331460478714195)



  https://x.com/EthCatHerders/status/1910331460478714195










### Writeups

- ACDE #209: Call Minutes - Christine D. Kim

### Additional info

- Mainnet upgrades to Pectra May 7, Epoch 364032
- EIP-7607: Hardfork Meta - Fusaka (PR with CFI/DFI decisions)
- Reconfiguring AllCoreDevs (ACD(E/C) upgrade planning & scope decisions, ACDT upgrade implementation/testing)

---

**timbeiko** (2025-04-10):

# Summary

## Pectra

- Client Releases expected by April 21
- EIP-7702: clients will not include the delegation status in the transaction receipt, but may add it to JSON-RPC for recent blocks. Conversation to continue here.

## Fusaka

- We clarified that today’s call was the deadline for moving EL EIPs from PFI to CFI, and ACDC next week will be the same for CL EIPs.
- We moved the following EIPs to CFI:

EIP-7823: Set upper bounds for MODEXP
- EIP-7825: Transaction Gas Limit Cap
- EIP-7907: Meter Contract Code Size And Increase Limit

Note: a modification is expected to increase the initcode size limit

EIP 7762 (Increase MIN_BASE_FEE_PER_BLOB_GAS) and 7918 (Blob base fee bounded by execution cost)

- Note: we will only include one of these EIPs, but more discussion is needed to determine which one and potential modifications are expected.

EIP-7642 (eth/69 - Drop pre-merge fields) does not require a hard fork but will be supported by some clients by Pectra and all clients in the months after the fork. On the call, we weren’t sure how to best represent this.

- I propose we SFI it for both Pectra and Fusaka, with a note about it being an optional requirement for Pectra and assumed to be supported by Fusaka.

In addition to the PFI’d EIPs, there was a desire to prioritize raising the gas limit following Pectra. However, there is no single “feature” that enables clients to safely support a higher gas limit, as much as focusing on performance improvements. To highlight that this should be a priority, we will draft an Information EIP to be reviewed on the next ACDE.
All other EL PFI’d EIPs have been Declined for Inclusion for Pectra. See [this PR](https://github.com/ethereum/EIPs/pull/9624) for the full list.

## AllCoreDevs Reconfiguration

- There was broad agreement towards Reconfiguring AllCoreDevs. Assuming no major objections come up before next week’s ACDC call, we’ll move forward with the split after Pectra is live!

## Pectra Pages

- Contributors to the Pectra upgrade are encouraged to share their perspective on the upgrade for the Pectra Pages


---
source: magicians
topic_id: 21463
title: All Core Devs - Execution (ACDE) #200, November 7 2024
author: abcoathup
date: "2024-10-25"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-200-november-7-2024/21463
views: 179
likes: 3
posts_count: 2
---

# All Core Devs - Execution (ACDE) #200, November 7 2024

#### Agenda

[Execution Layer Meeting "💯 💯" · Issue #1190 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1190) moderated by [@timbeiko](/u/timbeiko)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #200, November 7 2024](https://ethereum-magicians.org/t/all-core-devs-execution-acde-200-november-7-2024/21463/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> Action Items & Next Steps
>
> Teams to review proposed changes to EIP-7002 & 7521 system contracts
> Teams to review EIP-7610 and @chfast / Ipsilon to propose an alternative
>
> Announcements
>
> Nov 14 ACDC Cancelled
> Devcon Ethereum Magicians Session on Nov 15
> Nov 21 ACDE Cancelled in favor of a Pectra Interop Testing Call
>
> Call Summary
> note: this summary is briefer than usual due to Devcon being around the corner
> Pectra
>
> Mekong, a short-lived Pectra devnet is live!
> devnet-4 is mostly unused but will be …

#### Recording

  [![image](https://img.youtube.com/vi/DqdmqDtm2wM/maxresdefault.jpg)](https://www.youtube.com/watch?v=DqdmqDtm2wM&t=980s)

#### Additional Info

[Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-execution-call-200/) by [@Christine_dkim](/u/christine_dkim)

## Replies

**timbeiko** (2024-11-08):

# Action Items & Next Steps

- Teams to review proposed changes to EIP-7002 & 7521 system contracts
- Teams to review EIP-7610 and @chfast / Ipsilon to propose an alternative

## Announcements

- Nov 14 ACDC Cancelled
- Devcon Ethereum Magicians Session on Nov 15
- Nov 21 ACDE Cancelled in favor of a Pectra Interop Testing Call

# Call Summary

*note: this summary is briefer than usual due to Devcon being around the corner*

## Pectra

- Mekong, a short-lived Pectra devnet is live!
- devnet-4 is mostly unused but will be kept live for further testing: expect chaos!
- We agreed to merge 7702 changes and add the PR to devnet-5 specs
- No consensus on proposed changes to EIP-7002 & 7521 system contracts, teams to review async.

Audits for these contracts have already begun, worth taking into account when considering further changes.

## Individual EIP Activation for Testing

- On the last ACDC, we discussed enabling EIPs to be individually activated to facilitate testing. While some clients already support this, doing so is complex for others.
- For Fusaka, we agreed to simply treat the set of EOF EIPs and PeerDAS as “forks”,  which clients can toggle on/off. This way, both of these can be independently tested on top of Pectra.
- Further discussion would be needed to standardize a more granular scheme, and L2s needs should be taken into account for this, too.

## eth/70

- @smartprogrammer and @Giulio2002 proposed EIP-7801, which allows nodes to signal which subsets of historical data it can serve (and request blocks in these subsets from peers).
- This was framed as a short-term solution to enable EIP-4444 to go live ASAP.
- There were concerns raised about the duplication of work between this and Portal (unfortunately no one on Portal was present to give an update), as well as whether teams should standardize on ways of storing, retrieving and sharing history or not.

## EIP-7610

- We previously agreed to “retroactively activate” EIP-7610 and checked-in on clients’ implementation status before moving the EIP to Final.
- The conversation revealed that while the EIP was easy for Geth to implement, other teams have issues with it.
- @chfast said he had an alternative design he thinks can address the same issue as EIP-7610, will share a proposal


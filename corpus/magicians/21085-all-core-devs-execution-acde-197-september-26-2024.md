---
source: magicians
topic_id: 21085
title: All Core Devs - Execution (ACDE) #197, September 26 2024
author: abcoathup
date: "2024-09-14"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-197-september-26-2024/21085
views: 277
likes: 1
posts_count: 2
---

# All Core Devs - Execution (ACDE) #197, September 26 2024

#### Agenda

[Execution Layer Meeting 197 · Issue #1153 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1153) moderated by [@timbeiko](/u/timbeiko)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #197, September 26 2024](https://ethereum-magicians.org/t/all-core-devs-execution-acde-197-september-26-2024/21085/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> Important Announcements
>
> The EF has put out an RFP to audit the bytecode in Pectra system contracts — proposals are due by Oct 11!
>
> Action Items
>
>  Pectra Split (see this PR)  :
>
> devnet-3 EIPs will remain in Pectra, with EIPs 7623, 7742 and 7762 CFI’d for potential inclusion at a later date, along with a potential blob count increase (EIP TBD).
>
> Champions for EIPs 7623, 7742, 7762 and a blob increase should aim to address any objections in the next month, as it is unlikely we’ll be including mor…

#### Recording

  [![image](https://img.youtube.com/vi/PWhn8KdgCl8/maxresdefault.jpg)](https://www.youtube.com/watch?v=PWhn8KdgCl8&t=161s)

#### Additional Info

[Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-execution-call-197/) by [@Christine_dkim](/u/christine_dkim)

## Replies

**timbeiko** (2024-09-26):

# Important Announcements

> The EF has put out an RFP to audit the bytecode in Pectra system contracts — proposals are due by Oct 11!

# Action Items

- Pectra Split (see this PR)  :

devnet-3 EIPs will remain in Pectra, with EIPs 7623, 7742 and 7762 CFI’d for potential inclusion at a later date, along with a potential blob count increase (EIP TBD).

Champions for EIPs 7623, 7742, 7762 and a blob increase should aim to address any objections in the next month, as it is unlikely we’ll be including more EIPs in Pectra beyond that.

EOF and PeerDAS have been included in Fusaka and previously CFI’d Pectra EIPs have been moved to CFI for Fusaka. **No other EIPs will be Scheduled for Inclusion in Fusaka until EOF + PeerDAS are running on devnets together.**
Verkle EIPs, which were CFI’d for Fusaka, have been moved to a newly drafted Meta EIP for the Amsterdam fork, scheduled after Fusaka.

 Finalize spec for [devnet-4](https://notes.ethereum.org/@ethpandaops/pectra-devnet-4) by next week’s ACDC, including:

- BLS MSM pricing
- Changes to the execution requests, including updates to individual EIPs
- Builder spec support

 Aim to launch devnet-4 by the next ACDE (Oct 10)

# Summary

## devnet-3 updates

- Teku/Erigon issues have been fixed, Lighthouse still fixing issues
- @pk910 tested sending 100,000 deposits through the queue (write up)

Led to issues in block propagation time
- @mkalinin has a PR open on CL specs to address this, @ralexstokes said he will also work on rate-limiting deposits

## Pectra Spec Changes

- Besu and Nethermind ran benchmarks for the BLS MSM repricings, agree that they are currently underpriced but there was disagreement about whether to target specific hardware (and which!) for pricing or use a relative comparison with ecrecover. The conversation on this will continue async but we plan to agree to a final value by ACDC next week. @jwasinger opened a PR with tentative gas price adjustments.
- @mkalinin proposed changing the way execution requests are handled by the EL (PR), after a lot of discussion on the call, we agreed to move forward with this and include the changes as part of devnet-4.
- EIP-7702: two minor changes posted to the agenda but no one on the call to discuss

Update EIP-7702: Do not allow authorization nonce equal to 2**64 - 1 by gumb0 · Pull Request #8905 · ethereum/EIPs · GitHub
- Update EIP-7702: add several clarifications to align spec with tests by gumb0 · Pull Request #8906 · ethereum/EIPs · GitHub

Electra changes are being incorporated in the [Builder Spec](https://github.com/ethereum/builder-specs/pull/101)
The EF has put out an [RFP to audit the bytecode in Pectra system contracts](https://github.com/ethereum/requests-for-proposals/blob/master/open-rfps/pectra-system-contracts-audit.md) — proposals are due by Oct 11

## Pectra Split

*Note: there was heavy back and forth both in the call and chat for this section. I recommend watching the livestream for the full nuance.*

- Several individuals and teams shared their preference ahead of the call for how to split Pectra (see the call agenda). I summarized them briefly on the call.
- On last week’s ACDC, we seemed to have consensus to keep the scope of the first half of Pectra as-is, but @vbuterin argued we should include EIP-7623 and increase the blob count (or target).
- There was some pushback to this from several client developers, including @potuz and @tbenr who noted that both their clients’ discords have seen an increased in users having bandwidth issues with the current blob throughput.
- Francis from the Base team, who proposed we increase the blob count last week (analysis), argued we should have some clear metrics we are aiming for w.r.t. bandwidth usage.
- @Nerolation shared some analysis around re-org rates post-Dencun, but, again, some client developers had concerns about the applicability of these numbers, especially in the case of solo/home stakers.
- In addition to the concerns around bandwidth, there were some concerns about scope expansion for Pectra. If we increase the blob count, EIP-7623 helps limit the block size. But, if we are to increase the blob count, we might as well fix the issue of requiring both the EL and CL to set the value by implementing EIP-7742. Similarly, if we are updating the blob count, we should address issues around the pricing, as proposed by EIP-7762.

This dynamic shows opening Pectra to further additions can quickly lead to another “mini-fork”-sized addition to it.

There were also concerns that if we do not keep the scope frozen for the second half of Pectra, more EIPs would keep being added. A few of the client teams’ split proposals already advocate for this.
In parallel this, it was proposed to potentially have a “mini fork” focused on blob increase after the first half of Pectra but before shipping EOF/PeerDAS.
It seemed unlikely that we’d reach consensus around blob-increase EIPs on today’s call, or that we’d be able to fully stop new proposals for the second half of Pectra, so I proposed the following:

- As decided last week, we limit the scope of Pectra to the EIPs included in devnet-3, but we mark the blob-related EIPs (7623, 7742, 7762) as CFI’d for the fork. We take the next few weeks to explore the issues around bandwidth constraints and overall implementation complexity.
- EOF and PeerDAS get moved to “Pectra 2”, which is effectively Fusaka. CFI’d EIPs for Pectra also move to CFI for Fusaka, and we may continue adding more CFI’d EIPs for Fusaka. But, we do not schedule any other EIPs for inclusion in Fusaka until EOF + PeerDAS are live on a Fusaka devnet. When we’ve done this, we can consider other EIPs from the list of CFI’d proposals.
- Verkle EIPs, which were CFI’d for Fusaka, get CFI’d for the following fork: Amsterdam.

There were no major objections to this and so moved forward. [This PR](https://github.com/ethereum/EIPs/pull/8911) reflects the changes.
[@matt](/u/matt) asked for clarity on scope/timelines, so we agreed to the following:

- devnet-4 spec should be finalized by next week’s ACDC
- devnet-4 should go live by the next ACDE
- Final decisions about Pectra inclusions for the CFI’d EIPs should happen at the latest in two ACDEs (~1 month from now)

Lastly,  [@MaxResnick](/u/maxresnick) shared some updates about EIP-7762, notably an [analysis by Data Always](https://ethresear.ch/t/understanding-minimum-blob-base-fees/20489) and that he believes many L2s support the proposal.


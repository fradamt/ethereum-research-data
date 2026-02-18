---
source: magicians
topic_id: 26410
title: Community feedback on non-headlining features in Glamsterdam
author: nixo
date: "2025-11-03"
category: EIPs
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/community-feedback-on-non-headlining-features-in-glamsterdam/26410
views: 349
likes: 8
posts_count: 6
---

# Community feedback on non-headlining features in Glamsterdam

[Glamsterdam](https://eips.ethereum.org/EIPS/eip-7773) is the Ethereum upgrade that will follow [Fusaka](https://ethereum.org/roadmap/fusaka/) and is estimated for a release in 2026. The [headlining features](https://ethereum-magicians.org/t/eip-7773-glamsterdam-network-upgrade-meta-thread/21195) for this fork, chosen by [community consensus](https://ethereum-magicians.org/t/soliciting-stakeholder-feedback-on-glamsterdam-headliners/24885), are [enshrined Proposer Builder Separation](https://forkcast.org/upgrade/glamsterdam/#eip-7732) and [Block-level Access Lists](https://forkcast.org/upgrade/glamsterdam/#eip-7928).

The non-headlining features for this fork are now being chosen from the list of features proposed prior to the Oct 30th deadline. These features will be ones that are smaller in scope and don’t significantly delay the implementation of the selected headlining features.

Client teams, who generally have the most context for which features are compatible with headliners and each other, are asked to publish their opinions on which features to include. These opinions will be posted on [Forkcast](https://forkcast.org/upgrade/glamsterdam) when available.

However, it’s crucial that core developers understand the extent to which some of these features impact various Ethereum communities, especially when there’s overwhelming need for a feature that may not be as visible in core development communities. This form is an opportunity for this support to be organized and voiced ahead feature selection.

If you’d like to share your opinion on feature inclusion, please fill this out - the feedback will be aggregated and presented in an upcoming All Core Dev call.

Proposed EIPs: [Glamsterdam Upgrade - Forkcast](https://forkcast.org/upgrade/glamsterdam/#proposed-for-inclusion)

### 1. What stakeholder category do you represent?

### 2. Which of the proposed EIPs would have a meaningful impact on your community / your work? Please elaborate on why.

### 3. Does anything make any of these EIPs particularly urgent for community / your work?

### 4. Do you have any unaddressed concerns about any of the proposed EIPs?

### 5. Any additional comments?

---

### Your EIP ranking:

## Replies

**wminshew** (2025-11-04):

### 1. What stakeholder category do you represent?

Wallet devs / payments infra

### 2. Which of the proposed EIPs would have a meaningful impact on your community / your work? Please elaborate on why.

7708 will dramatically reduce the cost/complexity of capturing & communicating token/value flows to users

### 3. Does anything make any of these EIPs particularly urgent for community / your work?

n/a

### 4. Do you have any unaddressed concerns about any of the proposed EIPs?

n/a

### 5. Any additional comments?

n/a

---

**abcoathup** (2025-11-05):

### 1. What stakeholder category do you represent?

Community education

### 2. Which of the proposed EIPs would have a meaningful impact on your community / your work? Please elaborate on why.

We should heavily use **Declined for Inclusion** for EIPs that don’t significantly move the roadmap forward. (See my feedback on [Pectra Retrospective - #2 by abcoathup](https://ethereum-magicians.org/t/pectra-retrospective/22637/2))

We should also prioritize regular shipping (ideally 2 upgrades per year) to allow fast iteration on the roadmap.

Beyond the headliners of ePBS & BALs the priority is **repricing**.

Based on [Why we should prioritize repricings in Glamsterdam – MariusVanDerWijden](https://mariusvanderwijden.github.io/blog/2025/11/03/Repricing/) recommendation we should do Crucial (7 EIPs in S-tier) and Important (3 in A-tier).

Whilst most repricing EIPs appear to be small changes, that is still 10 EIPs to test, leaving very little scope for additional EIPs.

If client & testing teams have capacity, then we could add 4 EIPs (B-tier):

- EIP-8045 (Exclude slashed validators from proposing) - more of a bug fix
- EIP-7949 (Genesis File Format) - improve testing
- EIP-8062 (Add sweep withdrawal fee for 0x01 validators) & EIP-8068 (Neutral effective balance design) - remove disincentives from consolidation

### 3. Does anything make any of these EIPs particularly urgent for community / your work?

10 repricing EIPs + 4 potential additional EIPs is already too much, increasing upgrade complexity and risk.

For improved DX I’d like to see increased code size (though [EIP-2926](https://eips.ethereum.org/EIPS/eip-2926) in repricing should make this easier) and avoidance of stack too deep, but we can’t keep adding EIPs, so I didn’t include DX improvements.

### 4. Do you have any unaddressed concerns about any of the proposed EIPs?

There isn’t information on implementation effort, testing complexity ([yet](https://github.com/ethsteel/pm/issues/7)) or readiness, which makes it hard to compare EIPs.

Censorship resistance is important and we have a limited window to implement (in case regulatory conditions change), but an estimated additional 2 months to add FOCIL to Glamsterdam likely rules out 2 upgrades in 2026.  I’d be more supportive of FOCIL as a headliner in Heka + Bogotá, especially as this gives increased time to improve readiness.

### 5. Any additional comments?

We need to aid EIP authors with early feedback.  Does their EIP significantly move the roadmap forward, is there support from their targeted segment of the community, is there appetite from client teams to implement and what is the testing complexity.

We also need to find mechanisms to capture implementation effort, testing complexity and readiness that can be shared via EIP process/Forkcast.

---

### Your EIP ranking:

[![glamsterdam-eip-rankings-abcoathup](https://ethereum-magicians.org/uploads/default/optimized/3X/9/1/91a84f78e3d65182fd5bf52f3aa75674a1d3528b_2_690x460.png)glamsterdam-eip-rankings-abcoathup1440×960 206 KB](https://ethereum-magicians.org/uploads/default/91a84f78e3d65182fd5bf52f3aa75674a1d3528b)

---

**stakersunion** (2025-11-10):

### 1. What stakeholder category do you represent?

Solo-stakers via the [Stakers Union](https://www.stakersunion.com/)

### 2. Which of the proposed EIPs would have a meaningful impact on your community / your work? Please elaborate on why.

Stakers Union has formally voted to support EIP-7805: Fork-choice enforced Inclusion Lists (FOCIL) for inclusion in the next Ethereum network upgrade, Glamsterdam. We believe FOCIL measurably improves censorship resistance, reduces builder centralization risk, and strengthens solo-validator sovereignty without adding undue operational burden to home stakers.

### 3. Does anything make any of these EIPs particularly urgent for community / your work?

Home validators are the backbone of credible neutrality. FOCIL restores meaningful leverage to validators (not just builders) in the inclusion pipeline. That aligns with our mission to keep Ethereum open to small operators and resilient to policy or profit-driven filtering.

---

**abcoathup** (2025-11-27):

![image](https://storage.googleapis.com/papyrus_images/6a417c9a16819ad9d65b36381b293a19.jpg)

      [blog.base.dev](https://blog.base.dev/glamsterdam-proposals)



    ![image](https://paragraph.com/api/og?title=L1+Upgrades%3A+The+Glamsterdam+proposals+we%E2%80%99re+most+excited+about&blogName=Base+Engineering+Blog&coverPhotoUrl=https%3A%2F%2Fstorage.googleapis.com%2Fpapyrus_images%2Fc6a48868076ea75e50a5687142bf90ea2c7917baa268d1cace1783ab909a28ea.jpg&blogImageUrl=https%3A%2F%2Fstorage.googleapis.com%2Fpapyrus_images%2F6a417c9a16819ad9d65b36381b293a19.jpg&publishedDate=1763494648006)

###



In this post,  we dive into the EIPs of the upcoming L1 Glamsterdam upgrade that are most exciting for the Base Chain

---

**pkieltyka** (2025-12-04):

hi everyone. congrats on the Fusaka upgrade.

I’d like to advocate for the inclusion of eip-7708 in the next Ethereum upgrade to significantly simplify the ability for external offchain indexers to event source and aggregate ETH value transfers from log data.

Indexers are an important adjacent infrastructure component that works on top of Ethereum chains for many purposes to offer apps and clients a simplified inverted index on state inside of blocks. Many indexers are written based on event sourcing / event aggregation of eth event logs, such that the events work as deltas to balance state (in the case of ERC20/721/1155/etc value transfers), and by replaying offchain all events from start block to head, you are able to calculate reliably the balance of any token by just replaying and persisting the transfer events. Many indexers do this, including TheGraph, Sequence Indexer, etc., and it works beautifully. We run the Sequence Indexer across 55 evm chains (many kinds, even alt-L1 evms), and it works reliably for years. However, when it comes to aggregating native ETH balances or computing transaction history of value transfers, unfortunately this has proven to be extremely difficult with the goal in mind to capture all ETH value transfers and state updates from contract calls. For ETH transfer data we’ve had to work around this issue by fetching debug and trace data, but its a significant lift and huge data set to process when simply having EIP-7708 where and ETH value state update would offer a delta event from any interaction, similar to how ERC20’s perform. The inclusion of EIP-7708 would be a dream come true and significantly simplify the architectural demands of indexers that want to track ETH value updates from all transactions. Thank you.

The last point is, I’m not sure if its possible or realistic to offer 7708 events for all historic data as well, or just future blocks from the time of upgrade, but either is fine, as one can always compute a snapshot up to the point of upgrade and use it as the seed data. Of course, would be nice if could be updated from the start, but offchain datasets which essentially offer the same data and stored on IPFS/somewhere would work just as well without having to modify history. However, I defer to the amazing ethereum r&d team to make the best decision on implementation.


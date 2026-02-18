---
source: magicians
topic_id: 22703
title: All Core Devs - Consensus (ACDC) #150, February 6, 2025
author: abcoathup
date: "2025-01-29"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-150-february-6-2025/22703
views: 388
likes: 3
posts_count: 3
---

# All Core Devs - Consensus (ACDC) #150, February 6, 2025

#### Agenda

[Consensus-layer Call 150 · Issue #1265 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1265) moderated by [@ralexstokes](/u/ralexstokes)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #150, February 6, 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-150-february-6-2025/22703/3) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #150 summary
> Action Items
>
> Prepare client releases for 13 February to enable Holesky and Sepolia Pectra forks.
> [EL clients] Take a look at 7702 mempool implementation to surface test cases.
> Add your client team’s Pectra retrospective by next week’s ACD: Pectra Retrospective
> PSA: Move all Pectra EIPs to Last Call status!
>
> Summary
> Started with an update on pectra-devnet-6. Devnet is going well; and we touched on the status of builder-api testing which still has a few open items. Also broug…

#### Recording

  [![image](https://img.youtube.com/vi/JhDgD366DKg/maxresdefault.jpg)](https://www.youtube.com/watch?v=JhDgD366DKg&t=184s)

#### Additional info

- Pectra upgrade timing:

Client testnet releases planned to be out by Feb 13 (ACDE)
- Holešky upgrade slot: 3710976 (Mon, Feb 24 at 21:55:12 UTC)
- Sepolia upgrade slot: 7118848 (Wed, Mar 5 at 07:29:36 UTC)
- Assuming testnet upgrades go well, pick mainnet upgrade date on Mar 6.
Using +30 days, earliest potential mainnet upgrade slot 11444224 (Tue, Apr 8 at 23:25:11 UTC)

[Pectra-devnet-6](https://pectra-devnet-6.ethpandaops.io/)
Final call for input to [Pectra Retrospective](https://ethereum-magicians.org/t/pectra-retrospective/22637)
[Highlights of Ethereum's All Core Devs Meeting (ACDC) #150](https://etherworld.co/2025/02/06/highlights-of-ethereums-all-core-devs-meeting-acdc-150/) by [@yashkamalchaturvedi](/u/yashkamalchaturvedi)
[Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-consensus-call-150/) by [@Christine_dkim](/u/christine_dkim)
[PeerDAS-devnet-4](https://peerdas-devnet-4.ethpandaops.io/)

## Replies

**yashkamalchaturvedi** (2025-02-06):

![image](https://etherworld.co/favicon.png)

      [EtherWorld.co – 6 Feb 25](https://etherworld.co/2025/02/06/highlights-of-ethereums-all-core-devs-meeting-acdc-150/)



    ![image](https://etherworld.co/content/images/2025/02/EW-Thumbnails-1.jpg)

###



Pectra Devnet 6 Updates, EIP-7702 Discussion, Pectra Testnet Fork Timing & Mainnet Schedule, PeerDAS Scaling & Blobs, EIP for Hardware & Bandwidth Requirements, Ethereum Future Forks Planning & Pectra Bug Bounty Program

---

**ralexstokes** (2025-02-07):

**ACDC #150 summary**

**Action Items**

- Prepare client releases for 13 February to enable Holesky and Sepolia Pectra forks.
- [EL clients] Take a look at 7702 mempool implementation to surface test cases.
- Add your client team’s Pectra retrospective by next week’s ACD: Pectra Retrospective
- PSA: Move all Pectra EIPs to Last Call status!

**Summary**

Started with an update on pectra-devnet-6. Devnet is going well; and we touched on the status of builder-api testing which still has a few open items. Also brought up the status of the 7702 mempool, which still needs some attention from EL clients. Work is ongoing to finish this final polish for Pectra.

Given the state of Pectra, we then discussed timing for Pectra testnet fork dates. See [Consensus-layer Call 150 · Issue #1265 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1265#issuecomment-2637778317) for various options proposed. After getting inputs from client teams, we agreed to have Holesky and Sepolia fork dates in client releases by next ACDE on 13 February. We also touched on a nice timing for mainnet, assuming the testnet forks go well. Clients agreed to aim for a 30-day buffer between the Sepolia fork and mainnet, with the option to adjust mainnet if needed.

Next, we turned to a PeerDAS update. Good progress has been made on peerdas-devnet-4, and since this call a public devnet has gone live! https://peerdas-devnet-4.ethpandaops.io/ Some open spec questions are being considered for peerdas-devnet-5 around validator custody, and other exact spec changes to include. We continued on to discuss other PeerDAS design questions around proof computation, and also the idea of “blob parameter only” (BPO) forks to scale throughput in a more agile way. Lifting the responsibility for proof computation from the CL into the EL would give intra-slot timings more breathing room, and there was general consensus to move ahead with this design. We also touched on BPO forks as a useful pattern in the event we want to ship PeerDAS with less than the theoretical maximum parameters allowed, but still have an easy way to scale towards this theoretical maximum. There was no pushback against the idea if we need it. Discussion of blob scaling in PeerDAS did bring us back to the question of the role of local block building in the event a higher blob count exceeds the bandwidth available to a local builder. One solution to this would be the introduction of a `--max-blob-count` parameter to allow the local builder to customize their block production to the resources they have available. There are a variety of opinions on the suitability of this option as a client default, and we decided to continue exploring this and other options.

And then we had a request to look at suggested minimum hardware requirements here: [Add EIP: Hardware and Bandwidth Recommendations for Validators and Full Nodes by kevaundray · Pull Request #9270 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9270). This quickly circled back to the `--max-blob-count` flag; where we had a variety of opinions on the suitability. There is a core tension between how much we scale the L1 and how we account for solo stakers on the network. Check the call for more color; no clear consensus was reached on the call around the best path forward here. We did call out the need to get L2 input in the event a flag like `--max-blob-count` would impact their usage of L1.

We also had an update around a PFI’d EIP for Fusaka with EIP-7732. Rather than dive into Fusaka fork scoping further, we turned to preliminary conversation for the Pectra retrospective. There are many perspectives here and we are still waiting for all client input before aggregating to discuss in ACD. One interesting idea is to pipeline fork scoping so that the scope is fixed for fork N and any fork scoping conversations would only have fork N+1 in bounds. There was general support for moving to this regime in ACD to avoid the situation where there is an EIP suggestion relatively late in the process for a given fork. Another point that came up was strictly enforcement of tests for a given EIP before having any sort of inclusion consideration.

To close out the call, Fredrik from the EF Security team had an announcement for an upcoming Pectra Bug Bounty Attackathon. Keep eyes on the Ethereum blog for more details in the coming weeks! Kev also raised the point around the use of the `getBlobs` pathway that intends to help with data distribution. Client analysis shows it is very effective, especially when the block is sent ahead of the blobs to peers on the network. All present client teams relayed they send the block before the blobs to leverage this feature. We did note that the effectiveness of this feature relies on a majority of blobs being in the public mempool; and this gain is limited to the extent this distribution changes.


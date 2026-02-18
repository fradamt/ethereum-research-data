---
source: magicians
topic_id: 23340
title: All Core Devs - Consensus (ACDC) #154
author: system
date: "2025-04-01"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-154/23340
views: 339
likes: 2
posts_count: 3
---

# All Core Devs - Consensus (ACDC) #154

# All Core Devs - Consensus (ACDC) #154, April 3, 2025

- Apr 3, 2025, 14:00 UTC
- 90 minutes
- Recurring meeting : true
- ACDC
- bi-weekly
- Already on Ethereum Calendar : false
- Need YouTube stream links : true
- Other optional resources
- stream

# Agenda

1. Electra

Hoodi updates
2. Attestation analysis
3. Holesky followups
4. Mainnet timing

“tentatively set the Pectra mainnet date to April 30” – move?
5. Potential dates: All Core Devs - Execution (ACDE) #208 · Issue #1374 · ethereum/pm · GitHub
6. PeerDAS / blob scaling

peerdas-devnet-5 updates
7. FYI: peerdas-devnet-6 specs - HackMD
8. blob/acc in 2025 - HackMD
9. Fusaka

Client preferences

Prysm: Prysm Recommendation for Fusaka - HackMD
10. Teku: https://hackmd.io/Ub4cFkBgQVijPjLdMWsheg?view
11. Lodestar: Lodestar's Fusaka Inclusion Perspective
12. Grandine: PeerDAS + EOF
13. Lighthouse: Lighthouse Team on Fulu
14. Other CL PFI EIPs

EIP-7917 (below)
15. EIP-7688: Forward compatible consensus data structures
16. Research, spec, etc.

EIP-7922 (below)
17. All Core Devs - Consensus (ACDC) #154 · Issue #1399 · ethereum/pm · GitHub

Facilitator email: [stokes@ethereum.org](mailto:stokes@ethereum.org)

[GitHub Issue](https://github.com/ethereum/pm/issues/1399)

## Replies

**abcoathup** (2025-04-02):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #154](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-154/23340/3) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #154 summary
> Action items
>
> Pectra timelines
>
> Mainnet date confirmed to be May 7 2025
> Client releases by April 21 2025
> Pectra mainnet blog post by April 23 2025
>
>
> PeerDAS implementations should focus on the cell proof computation migration, and getBlobs support; validator custody is another outstanding feature but can be rolled out later so focus should be on the prior features
> FYI: EIP-7892 (BPO scaling) has been CFI’d for Fusaka
> Review the set of PFI’d Fusaka EIPs so we can make a final …

### Recordings

  [![image](https://i.ytimg.com/vi/RWBhHHrZ48w/hqdefault.jpg)](https://www.youtube.com/watch?v=RWBhHHrZ48w&t=213s)

https://x.com/i/broadcasts/1dRKZYDZemXxB

### Writeups

- ACDC #154: Call Minutes - Christine D. Kim by @Christine_dkim [christinedkim.substack.com]
- by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Mainnet upgrades to Pectra May 7, Epoch 364032

---

**ralexstokes** (2025-04-05):

**ACDC #154 summary**

**Action items**

- Pectra timelines

Mainnet date confirmed to be May 7 2025
- Client releases by April 21 2025
- Pectra mainnet blog post by April 23 2025

PeerDAS implementations should focus on the cell proof computation migration, and `getBlobs` support; validator custody is another outstanding feature but can be rolled out later so focus should be on the prior features
FYI: EIP-7892 (BPO scaling) has been CFI’d for Fusaka
Review the set of PFI’d Fusaka EIPs so we can make a final call on Fusaka CFI’d EIPs on ACDC #155.

**Summary**

- Pectra

Clients discussed attestation performance on Hoodi and potential implications for mainnet.
- Various clients are working on their own packing algorithms, with analysis and fine-tuning ongoing.
- Touched on the deposit mechanism and the rate of ingestion from the EL to the CL following EIP-6110. Decided this is expected behavior and will follow up async to determine if anything needs to happen here.

Latest thinking is to watch mainnet and can adjust EL ingestion rate in a future fork if needed.

Taking the above into account, we turned to mainnet timing where clients agreed to the following dates:
Pectra timelines

- Mainnet date confirmed to be May 7 2025
- Client releases by April 21 2025
- Pectra mainnet blog post by April 23 2025

PeerDAS

- Mostly updates here, as clients as busy with Pectra:

progress continues with implementation of peerdas-devnet-5
- peerdas-devnet-6 specs here: https://notes.ethereum.org/@ethpandaops/peerdas-devnet-6

We started the conversation around how to exactly scale blob counts in Fusaka, following some kind of BPO strategy.

- One suggestion here: blob/acc in 2025 - HackMD

Double blob counts every 2 months, after a two week observation period.
- Using configuration following EIP-7892

Broad agreement in this strategy and that we will want to fine tune the step sizes and cadence pending further PeerDAS R&D

Fusaka

- Next, we turned to finalize a set of CFI’d EIPs for Fusaka.
- Many client teams shared opinions async, check the agenda for links.
- EIP-7594 (PeerDAS) is already SFI’d
- We touched on a number of CL-focused EIPs to move from PFI to CFI.

Strong support for EIP-7892 (BPO scaling)
- Had a discussion around EIP-7917 (Proposer shuffling lookahead)

Some interest, but hesitation given how quickly the EIP was introduced relative to Fusaka scoping

Anders gave an overview on EIP-7819 that would modify the blob market.

- The scaling benefits of this EIP were highlighted, and otherwise we agreed this EIP should move to ACDE for the CFI conversation.

Gajinder raised EIP-7898 for CFI status which would uncouple the execution payload from the beacon block during broadcast.

- Clients expressed concerns around the implementation complexity of this EIP especially in light of other methods that seem more promising to achieve the same benefits this EIP suggests. Consensus is that it should not be CFI’d for Fusaka.

EIP-7688 was also in the PFI’d list; however given the focus on PeerDAS, consensus was that we would not CFI for Fusaka.
We also highlighted deprecation of mplex in the p2p layer as a potential for Fusaka.

We agreed to CFI EIP-7892 (BPO scaling), and I had said we would CFI EIP-7917 but am going to take the next ACDC to revisit this EIP’s status given the lack of time for client teams to consider the EIP in-depth.

Research, specs, etc.

- To wrap the call, Mike introduced EIP-7922 that would refactor how the exit queue works to get towards better latency for validators leaving the active set.

More information here: Adding flexibility to Ethereum's exit queue - Proof-of-Stake - Ethereum Research


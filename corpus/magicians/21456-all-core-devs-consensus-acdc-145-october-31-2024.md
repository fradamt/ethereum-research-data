---
source: magicians
topic_id: 21456
title: All Core Devs - Consensus (ACDC) #145, October 31 2024
author: abcoathup
date: "2024-10-24"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-145-october-31-2024/21456
views: 354
likes: 4
posts_count: 2
---

# All Core Devs - Consensus (ACDC) #145, October 31 2024

#### Agenda

[Consensus-layer Call 145 · Issue #1185 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1185) moderated by [@ralexstokes](/u/ralexstokes)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #145, October 31 2024](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-145-october-31-2024/21456/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #145 summary
> Action Items
>
> Reminder: ACDC on 14 Nov is canceled due to Devcon
> Review the merged PRs below for the next consensus-specs release
> EL teams: can we flexibly deploy Osaka so that we have the option to deploy a CL fork and EL fork separately during testing?
> Check out the mekong testnet: https://mekong.ethpandaops.io/
> Enjoy Devcon
>
> Summary
>
> Started with an overview of pectra-devnet-4
>
> Devnet is going well; a few minor open issues but under review by the relevant c…

#### Recording

  [![image](https://img.youtube.com/vi/KMLqv60xg9w/maxresdefault.jpg)](https://www.youtube.com/watch?v=KMLqv60xg9w&t=89s)

#### Additional info

[Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-consensus-call-145/) by [@Christine_dkim](/u/christine_dkim)

## Replies

**ralexstokes** (2024-10-31):

**ACDC #145 summary**

**Action Items**

- Reminder: ACDC on 14 Nov is canceled due to Devcon
- Review the merged PRs below for the next consensus-specs release
- EL teams: can we flexibly deploy Osaka so that we have the option to deploy a CL fork and EL fork separately during testing?
- Check out the mekong testnet: https://mekong.ethpandaops.io/
- Enjoy Devcon

**Summary**

- Started with an overview of pectra-devnet-4

Devnet is going well; a few minor open issues but under review by the relevant client teams

Then, turned to `pectra-devnet-5`

- Addressed some open PRs that are in a place to merge into the specs

Networking attestation support: Separate type for unaggregated network attestations by arnetheduck · Pull Request #3900 · ethereum/consensus-specs · GitHub
- Update to networking timeouts: p2p: Deprecate TTFB, RESP_TIMEOUT, introduce rate limiting recommenda… by arnetheduck · Pull Request #3767 · ethereum/consensus-specs · GitHub

Did a temperature check on the updates to the requests structure in the communication b/t the CL and EL; work is under way
Turned to an open question around the blob base fee computation as we change the blob target, which becomes relevant with EIP-7742 and the intent to raise the blob target in Pectra

- There are a spectrum of options here with an “endgame” solution that would be somewhat involved relative to the current EIP-7742 specification
- Agreed to go with a middle ground solution so that we don’t delay Pectra and still have a similar amount of responsiveness to the blob base fee

Then discussed a bug fix to the consolidation flow under EIP-7251; PTAL: [eip7251: Add missed exit checks to consolidation processing by mkalinin · Pull Request #4000 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/pull/4000)
Asked for updates around the EIP-2537 gas benchmarking; but no one working on that was on the call

And then turned to PeerDAS and blob scaling

- peerdas-devnet-3 had a 100k slot reorg; the devnet has been deprecated
- No one working on that devnet was on the call, but investigation is ongoing
- Next, raised the point to go ahead and formally place EIP-7594 into the fulu specs

No opposition on the call; although, there’s a question around how to isolate PeerDAS testing from Osaka testing on the EL

Then turned to longer-term R&D

- New proposal to introduce execution layer requests for withdrawal credential updates: Add EIP: Withdrawal Credential Update Request by lucassaldanha · Pull Request #9005 · ethereum/EIPs · GitHub
- Probelab had a quick update around some upcoming network bandwidth analysis via crawling of the disv5 network; expect results soon.

And concluded with an announcement of the launch of the `mekong` public testnet, based off of `pectra-devnet-4` intending for public preview of the upcoming Pectra hard fork

- https://mekong.ethpandaops.io/
- More details around running nodes, accessing the testnet, etc. coming in a future blog post!


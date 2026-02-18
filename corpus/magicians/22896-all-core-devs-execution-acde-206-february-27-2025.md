---
source: magicians
topic_id: 22896
title: All Core Devs - Execution (ACDE) #206, February 27, 2025
author: system
date: "2025-02-18"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-206-february-27-2025/22896
views: 256
likes: 5
posts_count: 4
---

# All Core Devs - Execution (ACDE) #206, February 27, 2025

# ACDE 206

- Feb 27, 2025, 14:00-15:30 UTC
- 90 minutes
- Stream: https://youtube.com/live/tlezpGztpi8?feature=share

# Agenda

- Pectra

Holesky Debrief

Chain status (proposals, slasheable validators, etc.)
- Next steps

Syncing from unfinalized checkpoints
- https://github.com/ethereum/go-ethereum/issues/31254
- Fork ID checks dependent on (standardized?) configs

Sepolia fork timing
Client releases

- https://github.com/sigp/lighthouse/releases/tag/v7.0.0-beta.1e

devnet-7 and/or new testnet
Mainnet requirements

- Builder API testing

ACDC retrospective

Fusaka

- https://github.com/ethereum/EIPs/pull/9378
- Disabling EOF to help PeerDAS testing
- EOF PAY opcode
- Fork deadlines

Change dates to Mondays to allow Tue/Wed for review before ACDs

EIP-4444 progress updates
Stateless clients for MPTs

[GitHub Issue](https://github.com/ethereum/pm/issues/1306)

## Replies

**system** (2025-02-27):

### Meeting Summary:

Tim led a discussion about the recent issues on the Holesky testnet, which resulted in a network fork. The problem arose due to the incorrect deposit contract address set by some execution layer teams. This led to a massive fork, with the majority of the stake represented by three executionary clients being effectively off the main chain. The team has been working to resolve this issue, with Kamil reporting that their infrastructure is now running smoothly and they are proposing blocks. The team is also coordinating slashings to recover Holesky. The conversation ended with a discussion on whether to start coordinating slashings or wait a bit longer.

The team discussed an alternative proposal to enable all validators at the same time to potentially finalize quickly. This idea was met with some confusion, with some participants suggesting that it might not be necessary to avoid slashing. Potuz clarified that the proposal involves setting all validators at a particular epoch, ensuring they are tested beforehand, and then finalizing within two epochs. This method was deemed more effective than the previously discussed proposal of disabling slashing protection for a thousand validators at a time. However, there were concerns about the potential for high numbers of slashed validators, which could lead to a loss of finality. The team agreed that the key to success lies in having enough stake weights to finalize over two epochs before the slashing rate drops below 66%.

The team discussed the challenges of finalizing and the potential impact of slashing on the network. They considered the possibility of finalizing immediately and then slowly leaking, but acknowledged that this might not be feasible due to the ongoing issue of patches based on an invalid branch. The team also discussed the potential for clients to handle longer periods of finality and the need for coordination in turning off slashing protection. They also discussed the potential for clients to set an arbitrary block as a checkpoint for syncing and peering. The team agreed that they need to buy time to look for clients and to allow for a reset to avoid more forks. They also discussed the need for a document to track the restart process for validators and beacon nodes.

Tim, Jim, Terrence, and Potuz discussed the need for a coordinated plan to disable slashing protection for their setup. They agreed on the necessity of having a clear guide for the process and a set timeline for its execution. The plan, though risky, was deemed the best option currently available. Saulius expressed concerns about the plan’s effectiveness due to the complexity of setups and the difficulty in achieving finality. Potuz suggested that even if the plan fails, it could still help by allowing them to manage the slashing and leakage more efficiently. The team decided to proceed with the plan, aiming to finalize and provide clients with some breathing room, despite the short-lived nature of this benefit.

Tim, Potuz, and Mikhail discussed the value of finalizing a block in the context of managing a peer-to-peer network. They agreed that finalizing a block allows them to ignore peers on the justified chain and manage the network better. Mikhail raised a concern about the potential stress on clients if they finalize too quickly, potentially leading to 18 days of non-finality. Jim agreed with Mikhail’s point and suggested that slashing clients quickly could be beneficial. Radek expressed concerns about the feasibility of handling 18 days of non-finality on Mainnet and suggested that changes to the Ethereum spec might be necessary. Tim suggested that the work of going through this issue could provide helpful learnings, but acknowledged that the clients’ inability to deal with unfinalized forks needed to be addressed. The team agreed to review the inactivity dig and consider increasing the inactivity leak to reduce the time for clients to leak out.

The team discusses the plan to address issues with the Holesky testnet. They agree to disable slashing protection for node operators and coordinate a time for this action, settling on 15 UTC the following day. Tim suggests giving participants 15 minutes to disable slashing protection, followed by 45 minutes of observation. The group also acknowledges the loss of some testing capabilities due to Holesky’s issues and considers alternative options, such as using Devnet 7 or potentially creating a new testnet forked from Holesky’s pre-Petra state.

Tim discussed the need for a comprehensive and up-to-date document regarding the Holeski issue. He agreed to create such a document after the call and share it in the chat for the client teams to post their information. The team also discussed the upcoming Sepolia event, scheduled for the following week. They decided to upgrade the Sepolia execution layer clients to the updated version with patches and confirmed that the consensus layer teams would not need to upgrade. The team also agreed to post their current configurations for Sepolia in the Discord chat for verification. Tim planned to update the blog post after the call to reflect the necessary changes for the three execution layer clients that had an issue and for Lodestar.

Tim, Potuz, and Enrico discussed potential solutions to address the issue of validators taking too long to leak out. Potuz suggested syncing nodes from a checkpoint that is not finalized, but agreed upon as a valid checkpoint. This would require a hard fork and changes to the client. Tim raised concerns about the trust assumptions involved in this approach, but agreed that it could be valuable if every node operator could independently choose the checkpoint. Enrico pointed out that the actual finalized state would still be present in the peer status, and that the change would involve decoupling the condition that the finalized checkpoint is the root of 4 choice.

In the meeting, the team discussed the issue of syncing to an arbitrary block and the potential for standardizing this process across clients. They agreed that this could be a valuable feature, especially in situations where there are few block producers and limited network connectivity. The team also discussed the engineering root causes of the issue, including the need for a more granular optimistic sync feature and the possibility of implementing a custom checkpoint sync. Additionally, they discussed the issue of different config files used by different clients and the potential for standardizing these files. The team agreed to continue working on these issues and to prioritize the implementation of a custom checkpoint sync.

Tim led a discussion about the implementation of a new system, focusing on the challenges of agreeing on a list of configurations and ensuring consistency across different networks. Jim suggested starting with the consensus layer due to its smaller scope and more defined parameters. The team agreed to target this for the Osaka or later testnets and to use the fork before Denkun as old test cases. They also discussed the need for a custom checkpoint on the CL side and the importance of harmonizing constants and parameters. The team decided to manually check for Sepolia and Mainnet, and to start working on standardizing config files for the CL side. The next steps include updating the blog post within the next hour and having a call to disable slashing protections.

### Next Steps:

- Tim to update the blog post within the next hour with the 4 clients (3 ELs and Lodestar) that need to be updated for the Sepolia fork.
- Tim to create and share a comprehensive document explaining how to disable slashing protection for all node operators.
- All client teams to have one representative knowledgeable about disabling slashing protection attend the call at 15 UTC tomorrow.
- All Holesky node operators to prepare for disabling slashing protection at the coordinated time during tomorrow’s call.
- Execution layer teams (Geth, Besu, Nethermind) to post their current Sepolia configuration in the AllCoreDevs chat for cross-checking.
- Client teams to work on implementing custom checkpoint sync for CL clients as a short-term priority.
- Daniel to investigate and document what a standardized configuration format could look like for execution and consensus layer clients, targeting implementation for Cancun or later.
- Jim to initiate discussions and documentation for standardizing configuration parameters on the consensus layer side.
- Client teams to consider implementing more granular optimistic sync options as a longer-term improvement.

### Recording Access:

- Join Recording Session (Passcode: H2N&ZD*+)
- Youtube Recording
- Download Transcript (Passcode: H2N&ZD*+ )
- Spotify Podcast Version

---

**abcoathup** (2025-02-28):

**Minimal ACDE recap (longer one to come)**

by [@timbeiko](/u/timbeiko) *(Copied from [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1344696471148040303))*

1. Holesky: we are going to try and get an epoch finalized tomorrow by having validators disable slashing protection in a coordinated way.
 To do this:

CL teams: open a PR here with their instructions for disabling slashing protection: pm/Pectra/holesky-postmortem.md at master · ethereum/pm · GitHub
2. Holesky node operators: get back online and be ready to disable slashing protection on Feb 28, at 15:00 UTC . We’ll have a live call to coordinate. More info
3. Sepolia: fork time unchanged, but Besu, Geth, Nethermind and Lodestar have new releases out. I will update the blog post soon with those. @geth @besu @nethermind please post your Sepolia configs in a thread response to this post so people can verify the address manually.
4. CL root cause fixes: CLs to look into implementing the ability for nodes to sync from a user-defined checkpoint (rather than the last finalized block). Conversation to continue on ACDC next week.
5. EL root cause fixes: ELs to look into updating the Fork ID to incorporate fork-specific configs (see ⁠fork-config-validation) as well as standardizing config files across clients to simplify testing.

---

**yashkamalchaturvedi** (2025-02-28):

![image](https://etherworld.co/favicon.png)

      [EtherWorld.co – 28 Feb 25](https://etherworld.co/2025/02/28/highlights-of-ethereums-all-core-devs-meeting-acde-206/)



    ![image](https://etherworld.co/content/images/2025/02/EW-Thumbnails--2--3.jpg)

###



Holesky Testnet Incident & Postmortem, Proposed Fixes for Optimistic Sync, Custom Checkpoint Sync Proposal for Consensus Layer & Sepolia Testnet Fork


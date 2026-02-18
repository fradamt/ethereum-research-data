---
source: magicians
topic_id: 24716
title: All Core Devs - Testing (ACDT) #43 | July 7 2025
author: system
date: "2025-07-02"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-43-july-7-2025/24716
views: 92
likes: 0
posts_count: 3
---

# All Core Devs - Testing (ACDT) #43 | July 7 2025

# All Core Devs - Testing (ACDT) #43 | July 7 2025

- July 7 2025, 14:00 UTC

# Agenda

- Fusaka updates
- EIP-7910: eth_config JSON-RPC Method
- Gas limit testing updates
- PeerDAS updates

Other comments and resources

The zoom link will be sent to the facilitator via email

Facilitator emails: XXXXX, YYYYY

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : ACDT
- Occurrence rate : weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true)
- Need YouTube stream links : true # Set to false if you don’t want YouTube stream links created
- display zoom link in invite : false # Set to true to add the Zoom link to the Google Calendar invite description

[GitHub Issue](https://github.com/ethereum/pm/issues/1603)

## Replies

**system** (2025-07-26):

### Meeting Summary:

The meeting focused on streaming coordination and updates for Ethereum clients on the Fusaka testnet, where various teams reported issues with synchronization, data responses, and network finalization that are being addressed. The group discussed the implementation of eth_config endpoint and backfill functionality across different client teams, along with gas limit testing updates and benchmark results that revealed performance bottlenecks requiring price adjustments. The conversation ended with discussions about consensus layer client verification, gas cost modifications for CLC growth, and transaction cap adjustments, with teams agreeing to proceed with proposed changes after further review and testing.

**Click to expand detailed summary**

The meeting begins with a discussion about streaming platforms. Josh is planning to stream simultaneously on YouTube and X (formerly Twitter). Pooja and Akash coordinate to manage the streaming on both platforms in Josh’s absence. As participants join, Mario suggests waiting a few minutes before starting to allow everyone time to connect. The pre-streaming process has already begun on both platforms, and Mario gives the go-ahead to start the meeting.

The group discusses recent issues and updates for various Ethereum clients on the Fusaka testnet. Barnabas reports that the network has returned to finalization after a period of non-finality, with some validators being exited to help resolve the issue. Client teams provide updates on their specific challenges: Nimbus had status issues, Teku experienced syncing problems due to insufficient RAM, Prism encountered syncing bugs during non-finality, Lodestar found a lower-level issue in a library update, and Lighthouse had sync and CDC value issues. The teams are working on resolving these problems, with some already fixed and others still being investigated.

Pawan reports that while fixing sync issues, they discovered some clients were sending empty responses when requested for data columns per range, even when they had valid data. This behavior, which could be considered malicious, caused problems when coupling blocks and columns. Lighthouse has addressed this by implementing a system to downscore and eventually drop peers that consistently return incorrect data. Pawan observed this behavior in Nimbus, Teku, and Grandine clients. While it’s difficult to create spec tests for this scenario, Pawan suggests other clients should be aware of this issue. Mario inquires about the stance of the affected clients on this behavior, but Pawan notes that in some cases, Lighthouse’s requests might have been for ranges before the earliest available slot.

The discussion focuses on the implementation of the eth_config endpoint (EIP-7910) and backfill functionality across different client teams. Most teams are planning to implement eth_config this week, with Besu preparing a PR to add fork ID to the EIP. Regarding backfill, several teams report it’s still in progress, with some facing database schema changes and debugging complexities. The group agrees that Devnet 2 needs to be more stable before considering Devnet 3, as many bugs are currently patched rather than fixed. There’s also a plan to extend eth_config to include fork IDs for better verification.

The group discusses gas limit testing updates and benchmark results. Marcin reports that modex is the bottleneck, with a proposal to increase pricing threefold. He notes that clients are working to optimize an edge case scenario for geth and aragon. The point evaluation precompile test case was fixed, showing clients operating at about 32 megas per second, which is close to the minimum requirement for increasing the gas limit to 100 million. Parithosh mentions the bloat net effort, which aims to test network performance with 1.5 times the state of Mainnet.

The group discusses the implementation of gas repricing for certain operations, particularly focusing on modular exponentiation (ModExp). Marcin explains that the current proposal is to increase the pricing by 3 times, which would affect about 8% of calls. However, there’s still an issue with one edge case that remains too slow even after the price increase. Marius notes that optimizing the Go Standard Library, which they depend on, would take a long time to implement. Parithosh reminds the group that they had previously agreed to merge this change, pending outreach to ensure no significant impact on projects. Tim confirms that feedback suggests minimal impact. Mario concludes by asking Marcin to finalize the cosmetic changes to the proposal so it can be reviewed and merged.

The group discusses whether consensus layer clients should verify blobs received from execution layer clients. Francesco argues that this verification is unnecessary and expensive, especially with the increased number of blobs in Dencun. He suggests all clients should drop this extra verification as the execution layer has already verified the blobs. Parithosh and others agree, noting that the engine API assumes trust between layers. Pawan explains that Lighthouse currently verifies blobs, including those from builders, but acknowledges that this may not be necessary. The team agrees to reconsider their approach, particularly for the Dencun upgrade.

The group discusses increasing the gas cost for CLC growth from 3 to 5 or 8. Spencer proposes this change to finalize the spec quickly, noting the lack of current benchmarks. Mario suggests raising a PR in the EIP for approval in March. Ben doesn’t object but points out that CLC is currently priced the same as the ‘add’ operation despite being simpler. Spencer believes CLC will be more efficient than ‘add’ in general. The group also briefly mentions standardized yield metrics for Devnet 3, with J requesting review of a recent PR for get blobs v2 metrics.

The group discusses opening a PR for benchmarking requirements in the EIP process before CFI. Spencer suggests adding these requirements, and Mario agrees it’s a good idea given the improved benchmark infrastructure. They plan to open a PR to EIP-7723 to specify benchmarking steps before CFI. Ben then proposes changing the transaction cap in EIP-7825 from 30 million to 16 million for the upcoming Sakura fork, citing potential benefits and resolving issues with contracts like Zen. The group considers this change, noting it’s just a constant adjustment to an already planned feature. They discuss the process and potential impacts, with Mario suggesting they consult with Toni, the author of the related PR.

The group discusses lowering the gas limit to 16 million, with Toni presenting analysis showing minimal impact on transactions. Mario suggests making a PR to EIP-7825 instead of creating a new EIP, which receives general agreement. Lightclient expresses concerns about potential impacts on L2s and the limited time for community feedback, but doesn’t oppose the change. The group also discusses Modex, with Marcin requesting client teams to implement and test the 3x price change in their performance branches to gather accurate results, especially for Geth and Erigon.

### Next Steps:

- Marcin to update the description and cosmetic aspects of the EIP for modexp repricing.
- Spencer to open a PR to increase the gas cost of CLOC from 3 to 5 or 8.
- Spencer to open a PR to EIP-7723 to add benchmarking requirements for new precompiles before CFI.
- Toni to open a PR to EIP-7825 to lower the transaction gas limit cap to 16 million for Cancun.
- Client teams to push the 3x modexp price change to their performance branches for testing and dashboard results.
- Geth team (Mario) to push the modexp price change as soon as possible.
- Client teams to consider removing blob verification in CLs for performance reasons.
- Lighthouse and Nimbus teams to discuss internally about removing blob verification in the builder flow.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: v5%#6nt3)
- Download Chat (Passcode: v5%#6nt3)

---

**system** (2025-07-26):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=gYCb6GrQGjY


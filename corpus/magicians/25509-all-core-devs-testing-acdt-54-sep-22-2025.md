---
source: magicians
topic_id: 25509
title: All Core Devs - Testing (ACDT) #54, Sep 22, 2025
author: system
date: "2025-09-18"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-54-sep-22-2025/25509
views: 58
likes: 0
posts_count: 3
---

# All Core Devs - Testing (ACDT) #54, Sep 22, 2025

### Agenda

- Devnet 3 update
- BPO analysis open discussion
- Scheduling fusaka & BPOs on testnets:

Holesky
- Sepolia
- Hoodi

Shadowfork discussion

- Mainnet osaka style BPO for nethermind config - feat: update osaka style blob schedule by barnabasbusa · Pull Request #10 · eth-clients/mainnet · GitHub

Gas limit testing update
Glamsterdam testing updates

- bal-devnet-0 timeline discussion
- epbs-devnet-0 timeline discussion

**Meeting Time:** Monday, September 22, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1731)

## Replies

**system** (2025-09-22):

### Meeting Summary:

The team reviewed progress on the Fusaka DevNet 5 and discussed various technical challenges including node participation issues and potential bugs in the Nethermind client. They explored the implementation of a 60 million gas limit across different testnets, with concerns raised about Besu’s capacity to handle increased block sizes and potential delays to the Fuji hard fork. The team also discussed scaling issues, gas-imit testing progress, and agreed to make decisions about block size increases by the end of the week, while encouraging attendance at upcoming breakout calls for EPBS and Gloas discussions.

**Click to expand detailed summary**

The team discussed the progress and challenges of the Fusaka DevNet 5, including successful BPO numbers and upcoming client tests. They addressed issues with node participation and a potential bug in the Nethermind client, with FLCL and milen providing updates. The team also reviewed the timeline for Holky and Sepolia tests, and discussed the need for client teams to review and approve a pending PR for shadow forks. Jochem raised concerns about testing gas limits for the XEN contract, and the team explored potential solutions, including seeking help from the Nethermind team.

The team discussed the implementation of a 60 million gas limit across different testnets, with Sepolia and Holesky already supporting this limit. Ameziane reported that while some team members support increasing the gas limit, others are concerned about the risk of delays to the Fuji hard fork. Marius explained that GASP has made improvements to their library for MODEX and switched to GNARC for BN254 operations, confirming their readiness for the 60 million gas limit. The main open question remains about Besu’s implementation, with Luis noting that the gas limit increase could potentially delay the Fuji hard fork if issues arise.

The team discussed scaling issues, particularly regarding Besu’s capacity to handle increased block sizes. Ameziane explained that while there were no issues at 60 million before EEST tests, new use cases showed Besu’s throughput at around 15 gas per second, which is below the required 20 mgas per second for 60 million blocks. Barnabas asked if Besu could be scaled down to 55 or 50 million, but Ameziane confirmed that 45 million is the minimum target. Tim raised concerns about the worst-case scenario of implementing Besu at 60 million with potential issues, questioning how long it would take Besu to process a block, to which Ameziane replied that a 60 million block would be processed in approximately 3.5 seconds.

The team discussed potential risks and impacts of increasing the block size to 60 million, particularly focusing on Besu nodes. Ameziane explained that while there might be some performance issues for Besu nodes on standard hardware, the risk of an attack is relatively low. The group agreed to consider the implications further, with Tim suggesting a decision could be made on Thursday. They also discussed the potential benefits of better hardware for processing larger blocks, though Ameziane noted that clock speed would be more important than core count in this case.

The team discussed progress on gas-imit testing and agreed to make a decision by the end of the week. Toni announced a breakout call on Wednesday to discuss moving from block-level access list hashing. Felipe provided an update on refactoring access checks and adding test cases. Justin reported progress on the spec release for EPBS, which Terence confirmed was ready for consensus testing. The team agreed to rename the breakout call to “Gloas breakout” and include both Bals and EPBS teams. Barnabas encouraged attendance at the upcoming EPBS breakout room call on Friday.

### Next Steps:

- Nethermind team to resolve the gas mismatch issue in DevNet3.
- Milen to investigate the database commit delays on the Eregon node and follow up with Barnabas offline.
- Client teams to aim for code freeze by end of day, with client traces due by Thursday.
- Nethermind team  to help Jochem with the GP hacked image source code for gas benchmark testing.
- Besu team to reach consensus on whether they can support 60 million gas limit and provide an update by the end of the week.
- All teams to make a decision about moving to 60 million gas limit by the end of the week.
- All interested parties to attend the Block Live Access List breakout call on Wednesday at 2PM UTC.
- Justin to complete the ePBS spec release  within 24 hours.
- Client teams implementing Glois to attend the EPBS breakout meeting on Friday.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 8?6MHbZV)
- Download Chat (Passcode: 8?6MHbZV)

---

**system** (2025-09-22):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=xJe3erOIb4k


---
source: magicians
topic_id: 24549
title: All Core Devs - Testing (ACDT) #40 | June 16 2025
author: system
date: "2025-06-13"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-40-june-16-2025/24549
views: 169
likes: 2
posts_count: 5
---

# All Core Devs - Testing (ACDT) #40 | June 16 2025

# All Core Devs - Testing (ACDT) #40 | June 16 2025

- June 16 2025, 14:00 UTC

# Agenda

- Berlinterop updates
- PeerDAS testing

Other comments and resources

The zoom link will be sent to the facilitator via email

Facilitator emails: XXXXX, YYYYY

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : All Core Devs - Testing
- Occurrence rate : weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- display zoom link in invite : false

[GitHub Issue](https://github.com/ethereum/pm/issues/1573)

**YouTube Stream Links:**

- Stream 1 (Jun 16, 2025): https://youtube.com/watch?v=MxVuRKsOEE8

## Replies

**akashkshirsagar31** (2025-06-16):

# ACD Testing Call #40 – June 16, 2025

#### Summary

## Berlinterop updates

### Fusaka

- All specs and tests merged in devnet-2
- devnet-2 interop: Faster process in order to test, but the changes included will now have to use ACD process to be officially included in Fusaka.
- Fusaka Devnet-1 still live, will go down in ~1 day, and clients using it will have to move all testing to devnet-2

### Gas Limit tests

- Benchmarking to find bottlenecks and optimizing performance
- Clients agreed to 45m but there are many client fixes in every client that need to go into branches before making it the new default gas limit.

#### 45 Million Gas Limit Requirements

- Geth: Single fix that needs to get to master branch, but stance is that going above 45m is not possible without reprices (biggest reprice is modexp that is going into fusaka), but 45m would be ok (according to marius personal opinion)
- Nethermind: Ok with 45m, and need to put out a new release, but confortable with current release, and could just instead signal that 45m gas limit is ok for nethermind users
- Erigon: Ready for 45m

#### Benchmarking

- Marcin: For fusaka, modexp is still the main bottleneck
- After fusaka alt_bn128 precompiles (EIP-196: Precompiled contracts for addition and scalar multiplication on the elliptic curve alt_bn128, EIP-197: Precompiled contracts for optimal ate pairing check on the elliptic curve alt_bn128) are going to be the bottleneck, and it’s possible that a repricing is going to be required.
- More testcases for EC_PAIRING and EC_MUL are needed.
- EC_ADD there’s going to be an EIP next week.
- EIPs for ECMUL/ECPAIRING is still TBD.
- EVM logs are a potential issue due to devp2p constrains (10mb limit)
- Ben: Issue only kicks at 65M, so we should be ok until Fusaka.
- Create a block full of logs scenario to help decide which approach we need.
- We require some benchmarks for logs in order to make a more informed decision.

### Deep trie issues

- Sstore with deep trie, not a big issue for 45m but moving forward it will be.
- Jochem: The Xen contract is creating a lot of small proxy contracts which delegate call into something else.
- During the tx itself (28m gas) 67 (CREATE2) small contracts, with a lot of stores too
- Nothing else fancy/complex seems to be happening.
- Seems like caching mechanism of clients is not predicting this correctly.
- There’s a state test now that creates a lot of stores and contract creations, but execution time of this state test is very quick, but on mainnet this same test is taking a long time due to the size of the mainnet db.
- We should run this same state test in a very large state size to see if this is reproducible.
- It’s also possible that there’s extra logging in the mainnet tx that could be making matters worse.
- Ben: Ran this block (but could not trace it) and it took this block (and 20+ other blocks) only 600ms to execute, which is not significant.
- Geth: Cache of a 256MB buffer (state tree buffer) that sometimes overflows and it happens from time to time during runtime and which takes 2.5 seconds, so this could be the culprit.
- It’s bad timing, plus the complexity of the block that included the tx, which adds to the cache more than a regular block.
- Fix would be to do this process async (flushing of this cache).
- Will try this on a shadowfork to see how it behaves.

## History Expiry

- Matt: Discussions about history expiry happened last week in the interop
- Path forward: All clients needs to polish features to allow to run without pre-merge history.
- Releases will come out in the following weeks that drop pre-merge history at each client’s convience.
- EF will publish a block post that informs the general public that clients can run without pre-merge history.
- We need to modify the approach with the Era file format.
- Originally ERA1 → pre-merge, ERA2 → post-merge.
- ERA-E will be execution layer, and ERA-C will be consensus layer.
- This will unlock the ability for clients to start prunning history.
- We have a backstop to access the history, depending on whether we want to do a rolling history-prunning or by stages (e.g. forks).
- Will continue discussions for the next month and a half.
- ERA files is not the only solution: Portal implementations is one of the alternatives.
- Clients will analyze whether they can bring some of the portal features to each client.
- Will pick apart the sections of the portal protocol that are usable to each client/layer and implement those.
- The rest of the features from portal will be implemented as they seem useful.

---

**system** (2025-06-16):

### Meeting Summary:

The team discussed updates on Berlin interop, including gas limit scaling and Fusaka development, as well as performance issues related to client mechanisms and database operations. They addressed a buffer overflow issue in Geth and proposed a solution involving double buffering to flush inactive buffers asynchronously. The team also reviewed progress on history expiry, including client implementations for running without pre-merge history, and discussed plans for modifying error files and Portal features to better serve execution clients.

**Click to expand detailed summary**

The team discussed updates on Berlin interop, focusing on gas limit scaling and Fusaka development. They agreed to raise the gas limit to 45 million, pending client team fixes and releases. Marcin reported positive benchmarking results for 60 million gas limit, though further testing is needed. The team also addressed log management and large tree depths issues, with Ben suggesting performance benchmarks to inform future decisions. Jochem provided an update on extend contracts, explaining the creation of small proxy contracts and their impact on transaction performance.

Jochem discussed performance issues related to a client mechanism and database operations, particularly concerning execution times and bottlenecks. He noted that the system was slow for certain clients and mentioned that the problem might be related to the database. Jochem also mentioned that adding extra locations could help improve performance, and he observed that the system was competitive in terms of transactions.

The team discussed a buffer overflow issue in Geth that was causing 2.5 seconds of block processing time due to synchronous disk flushing. They identified that the problem occurred when blocks exceeded 256 megabytes, leading to a proposed solution of implementing double buffering to flush inactive buffers asynchronously. The team agreed to test this solution on the Shadow Fork and perfnet environments, with further discussion planned for Thursday’s meeting.

The team discussed the progress on history expiry, with Matt reporting that clients have implemented necessary features to run without pre-merge history, and clients are now free to make it the default mode. They plan to publish a blog post on the Ethereum Foundation blog in the next two weeks to share how to run clients without pre-merge history. The team also discussed modifying error files for post-merge and agreed to have separate error files for each layer, with Yasik working on the consensus layer. They aim to settle on the specification for historical data access in the next 1.5 months, which will allow clients to start pruning more history. Additionally, they plan to modify Portal features to better serve execution clients and will have a public community call to discuss these changes.

### Next Steps:

- Client teams to push performance fixes and make releases to support raising the gas limit to 45 million over the next week.
- EF team to share more information on benchmarks and bottlenecks found during gas limit testing over the next week.
- Marcin and team to continue crafting test cases for ECC pairing and ECC mul to determine if repricing is needed in Fusaka.
- EF team to publish an EIP for ECC add repricing later this week.
- PK to share reproducible test for log-related issues with client teams.
- Client teams to run benchmarks on blocks full of logs to inform decision on log repricing or increasing peer-to-peer limits.
- Jochem to continue working on reproducing and analyzing the issue with Estor and large tree depths.
- Client teams to implement and test fixes for buffer flushing issues related to large blocks.
- EF team to publish a blog post in the next couple of weeks about running clients without pre-merge history.
- Client teams to begin making running without pre-merge history the default mode in their releases.
- Yasik and team to finalize specification for consensus layer era file (era C) in the next 1.5 months.
- EF team to organize a public community call about Portal Network changes later this week or early next week.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: I25Q=1bs)
- Download Chat (Passcode: I25Q=1bs)

---

**system** (2025-06-16):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=MxVuRKsOEE8

---

**abcoathup** (2025-06-17):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akashkshirsagar31/48/13015_2.png)

      [All Core Devs - Testing (ACDT) #40 | June 16 2025](https://ethereum-magicians.org/t/all-core-devs-testing-acdt-40-june-16-2025/24549/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACD Testing Call #40 – June 16, 2025
> Summary
> Berlinterop updates
> Fusaka
>
> All specs and tests merged in devnet-2
> devnet-2 interop: Faster process in order to test, but the changes included will now have to use ACD process to be officially included in Fusaka.
> Fusaka Devnet-1 still live, will go down in ~1 day, and clients using it will have to move all testing to devnet-2
>
> Gas Limit tests
>
> Benchmarking to find bottlenecks and optimizing performance
> Clients agreed to 45m but there are many client f…

### Recordings

- https://www.youtube.com/live/MxVuRKsOEE8?t=267s
- Eth Cat Herders:

Live stream on X: https://x.com/i/broadcasts/1OdKrDvyXvvJX

### Writeups

- ACDT#40: Call Minutes + Insights - Christine D. Kim by @Christine_dkim [christinedkim.substack.com]

### Additional info

- 45 million gas limit can be supported (Geth have fix to release)

Current signaling: gaslimit.pics

Fusaka upgrade:

- fusaka-devnet-2 targeting June 23

History expiry: community call soon, clients can support running without pre-merge history


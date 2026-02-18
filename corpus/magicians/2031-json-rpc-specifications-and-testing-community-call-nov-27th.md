---
source: magicians
topic_id: 2031
title: JSON-RPC Specifications and Testing Community Call Nov 27th, 2018
author: boris
date: "2018-11-27"
category: EIPs > EIPs interfaces
tags: [json-rpc, community-call]
url: https://ethereum-magicians.org/t/json-rpc-specifications-and-testing-community-call-nov-27th-2018/2031
views: 1584
likes: 5
posts_count: 3
---

# JSON-RPC Specifications and Testing Community Call Nov 27th, 2018

An initial call to gather interest and assign next steps in improving / solidifying the JSON-RPC specification for Ethereum clients, and how to run community resources for testing and validation.

This is part of a wider effort to improve standards and specifications, including finding maintainers for major parts of the Ethereum stack, and collecting interested stakeholders who want to work on these tasks.

Call at8am PST, Nov 27th, Zoom Video [Launch Meeting - Zoom](https://zoom.us/j/946476323)

Github Agenda thread [Community Call - Nov 27th 8am PST - JSON-RPC Spec and Testing for Ethereum Clients · Issue #15 · spadebuilders/community · GitHub](https://github.com/spadebuilders/community/issues/15)

Transcript notes on HackMD [JSON RPC Spec & Testing Community Call Nov 27th - HackMD](https://hackmd.io/FUE13Uh_Rj2qLoJOnHILqw)

---

[@Arachnid](/u/arachnid)  made a call for documenting JSON-RPC in an EIP [Document JSON-RPC interface in an EIP · Issue #1442 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/1442)

[@bitpshr](/u/bitpshr) has added a PR starting this work https://github.com/ethereum/EIPs/pull/1474

This will be an organizing and initial “bootup” call to see who will be participating, how we will communicate, and so on. Feel free to use this community space for now, with notes preferred in HackMD format.

## Replies

**boris** (2018-11-27):

Thanks to everyone on the call today. Full transcript is on HackMD https://hackmd.io/FUE13Uh_Rj2qLoJOnHILqw?both

It is clear that there are two inter-related concerns. One is the production and maintenance of a well-specified JSON-RPC standard. The other is testing and interop of implementations.

Boris is volunteering to put some time in to project manage and coordinate efforts, mainly on the spec side and bridging to the EEA.

The testing process is something that [@pipermerriam](/u/pipermerriam)’s team at the EF is taking some responsibility for, and as noted below, there are others wanting to collaborate.

## Action Items / High Level Notes

Everyone review the PR of the spec

- https://github.com/ethereum/EIPs/pull/1474
- Chris L volunteered to be a maintainer
- let’s push for Last Call so this can get nailed down

Boris to setup separate repo, it may be easier to collaborate there than just in a single PR thread

- https://github.com/spadebuilders/ethereum-json-rpc-spec
- made Chris L a maintainer of that repo

Should there be a separate process for proposing JSON-RPC extensions?

- breaking changes and/or major additions to the spec should likely be filed as EIPs
- for convenience, working group have a separate repo
- need to start working and see how it evolves
- RFC process has new RFCs which supersede – in essence, we are on “version” 1474 of the spec once approved

Stakeholders include:

- client devs, those looking to build a new, compatible client
- middleware – web3js, ethers.js --> definitely need
- devops / people looking to run many nodes
- miners

Middleware Flags for Debug

- many dapp developers don’t know that JSON-RPC exists – blame middleware for errors
- talk to middleware about a debug flag or common approach to get at underlying responses

Testing

- INFURA has released compatibility / interop testing https://github.com/INFURA/rpc_sanity_test
- Bob pointed to Casey’s tests here http://cdetr.io/eth-compat-table/ – which is an RPC test suite https://github.com/cdetrio/interfaces/tree/0fcb796440dea702e308710457346d29b051f365/rpc-specs-tests – part of Hive https://github.com/ethereum/hive
- INFURA can be involved
- Dave said he’d be interested in testing
- loop back with Piper
- these tests need to get setup again and updated

EEA

- Boris to coordinate with Ron / Chaals / Alex at EEA
- Loop in Ben Burns as EEA technical lead?
- How will EEA contribute?
- Likely next step is an internal EEA call with interested members & clients - Block Apps, Quorum, Clearmatics, Pegasys, etc.

---

**pipermerriam** (2018-11-27):

[@boris](/u/boris) thanks for the write up.  I’m sorry I missed this morning’s call.  I have a full time hire starting Monday who’s focus will include this effort.  I’ll ensure that he’s part of this process going forward.  The thing that I see my team providing is:

- Creation and maintenance of a standardized test suite including documentation for how implementations should integrate with it.
- Client agnostic tooling for execution of the test suite against a running client and potentially something to do fuzz testing as well.


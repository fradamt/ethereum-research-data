---
source: magicians
topic_id: 10884
title: "EIP-4844: Shard Blob Transactions - Cancun upgrade"
author: protolambda
date: "2022-09-15"
category: EIPs > EIPs core
tags: [cancun-candidate]
url: https://ethereum-magicians.org/t/eip-4844-shard-blob-transactions-cancun-upgrade/10884
views: 3218
likes: 12
posts_count: 3
---

# EIP-4844: Shard Blob Transactions - Cancun upgrade

[EIP-4844](https://ethereum-magicians.org/t/eip-4844-shard-blob-transactions/8430) introduces [Shard Blob Transactions](https://eips.ethereum.org/EIPS/eip-4844).

Blob data would make a big impact to make Ethereum [the central place to rollups](https://ethereum-magicians.org/t/a-rollup-centric-ethereum-roadmap/4698) by taking the **first step towards danksharding**: a vision where ethereum as L1 can host and attract a diverse set of L2s with much lower fees for ethereum L2 users.

Nov 22 EIP-4844 shanghai candidate update:

- No interactions with Shanghai EVM EIPs: the EIP adds one opcode to push a datahash onto the stack, and a precompile to verify data against the commitment.
- Compatibility with Withdrawals: the EL and CL specs are based on top of the withdrawal work (EL, CL, Engine API)
- EIP-4844 Spec completion:

We have iterated through EIP changes for 9 months, and the scope of changes reduced significantly over time
- The EIP received review from most client implementer teams
- Complementary CL specs and Engine API specs

EIP-4844 Testing:

- There is an active interop repository
- Devnets of increasing size and client participation (see devnet section)
- Ongoing work to analyze network impact, but conservatively reduced back the blobs parameter for initial iteration.

EIP-4844 [KZG-ceremony](https://github.com/ethereum/KZG-Ceremony) readiness:

- Specs ready
- Front-ends ready:

zkparty, and hosted here
- chotto
- worldcoin (WIP)

[Sequencer](https://github.com/ethereum/kzg-ceremony-sequencer) ready, and [audited](https://github.com/ethereum/kzg-ceremony/blob/main/KZG10-Ceremony-audit-report.pdf)

EIP-4844 KZG library readiness:

- The CL specs define a simple minimal interface, as well as the EIP
- C-KZG-4844 implements this interface, with NodeJS, CSharp and Python bindings. And ongoing Rust bindings.
- Go-KZG implements this interface in Go

EIP-4844 Devnet readiness:

- Wide client devnet support:

EL: Erigon, Geth, Nethermind
- CL: Prysm, Lighthouse, Lodestar

Targetting [devnet v3](https://notes.ethereum.org/@timbeiko/4844-devnet-3) soon after ACD, on Nov. 30

Dec 8 EIP-4844 ACD update: EIP-4844 was confirmed as primary focus for Cancun.

## Replies

**jessepollak** (2022-10-06):

Hi all - just wanted to share [this blog post](https://www.coinbase.com/blog/supporting-eip-4844-reducing-fees-for-ethereum-layer-2-rollups) from Coinbase discussing our support for the EIP-4844 effort.

*TL;DR*

- Following the Merge, EIP-4844 is an upcoming upgrade to Ethereum that will introduce data availability for rollups, leading to reduced fees and more transaction throughput
- We see EIP-4844 as a key enabler for bringing our customers into the cryptoeconomy with a secure, easy to use experience that is faster and cheaper
- We’ve been helping drive this effort alongside the Optimism and Ethereum Foundation teams, dedicating significant internal engineering resources to accelerate the work.
- If you’re interested in contributing to the effort, you can see the open items in the EIP-4844 readiness checklist or join our next community call — both can be found at eip4844.com.

Really excited to continue scaling Ethereum with the broader community.

---

**xinbenlv** (2022-10-06):

Thank you for sharing [@jessepollak](/u/jessepollak).

It’s so exciting to see so much progress and passion in the movement.


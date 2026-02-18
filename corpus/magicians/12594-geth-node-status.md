---
source: magicians
topic_id: 12594
title: Geth node status
author: FastGwei
date: "2023-01-16"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/geth-node-status/12594
views: 1209
likes: 0
posts_count: 1
---

# Geth node status

So I have set up a geth node and beacon node on a server, as this is required post merge. My beacon node is fully synced:

Upon the call  curl p://localhost:3500/eth/v1alpha1/node/eth1/connections

I get the response:

{“currentAddress”:“://localhost:8551”, “currentConnectionError”:“no contract code at given address”, “addresses”:[tlocalhost:8551"], “connectionErrors”:}

This suggests my Geth node is not synced:

Upon eth.syncing I get the response:

currentBlock: 16421601,

healedBytecodeBytes: 0,

healedBytecodes: 0,

healedTrienodeBytes: 0,

healedTrienodes: 0,

healingBytecode: 0,

healingTrienodes: 0,

highestBlock: 16421692,

startingBlock: 0,

syncedAccountBytes: 5827139183,

syncedAccounts: 23719401,

syncedBytecodeBytes: 729713789,

syncedBytecodes: 125063,

syncedStorage: 103229063,

syncedStorageBytes: 22400879956

The current block when called is 16421693

However, in my geth node output logs I get this:

.505] Forkchoice requested sync to new head    number=16,421,687 hash=024bf6…d6dddf

INFO [01-16|21:18:39.781] Forkchoice requested sync to new head    number=16,421,688 hash=f47cb4…920674

INFO [01-16|21:18:40.080] Forkchoice requested sync to new head    number=16,421,689 hash=e8fc3e…4059aa

INFO [01-16|21:18:40.328] Forkchoice requested sync to new head    number=16,421,690 hash=d77ff3…e460d6

WARN [01-16|21:18:40.508] Unexpected bytecode packet               peer=605c26ed reqid=1,096,514,795,128,754,446

INFO [01-16|21:18:40.568] Forkchoice requested sync to new head    number=16,421,691 hash=6db705…ffafc6

INFO [01-16|21:18:40.817] Forkchoice requested sync to new head    number=16,421,692 hash=44e4ea…cfd23d

INFO [01-16|21:18:41.488] Imported new block headers               count=7    elapsed=“468.313µs”  number=16,421,692 hash=44e4ea…cfd23d

INFO [01-16|21:18:42.550] Downloader queue stats                   receiptTasks=0     blockTasks=0     itemSize=308.27KiB throttle=851

WARN [01-16|21:18:45.125] Served eth_coinbase                      reqid=3                         duration=“20.536µs” err=“etherbase must be explicitly specified”

INFO [01-16|21:18:47.047] State sync in progress                   synced=11.94% state=26.93GiB  accounts=23,697,577@5.42GiB   slots=103,068,403@20.83GiB codes=124,896@694.86MiB eta=247h18m47.900s

INFO [01-16|21:18:50.141] Forkchoice requested sync to new head    number=16,421,693 hash=35744d…f9886e

INFO [01-16|21:18:50.557] Imported new block headers               count=1    elapsed=68.765ms     number=16,421,693 hash=35744d…f9886e

INFO [01-16|21:18:55.069] State sync in progress                   synced=12.01% state=27.11GiB  accounts=23,828,371@5.45GiB   slots=103,808,372@20.97GiB codes=125,396@698.03MiB eta=245h45m59.782s

INFO [01-16|21:19:00.055] Forkchoice requested sync to new head    number=16,421,694 hash=d28dee…bc57cd

INFO [01-16|21:19:02.496] Imported new block headers               count=1    elapsed=4.905ms      number=16,421,694 hash=d28dee…bc57cd

INFO [01-16|21:19:03.075] State sync in progress                   synced=12.10% state=27.27GiB  accounts=24,002,572@5.49GiB   slots=104,396,132@21.09GiB codes=126,322@703.68MiB eta=243h44m22.420s

INFO [01-16|21:19:11.140] State sync in progress                   synced=12.22% state=27.45GiB  accounts=24,241,903@5.55GiB   slots=104,979,316@21.21GiB codes=127,192@709.10MiB eta=241h0m26.206s

INFO [01-16|21:19:12.095] Forkchoice requested sync to new head    number=16,421,695 hash=b2148c…ffb960

INFO [01-16|21:19:14.545] Imported new block headers               count=1    elapsed=51.565ms     number=16,421,695 hash=b2148c…ffb960

This leads me to believe im not synced for circa 230h. Is this correct, I am only a few blocks behind now, could someone indicate what its doing now and how long it will take until fully synced and operational?

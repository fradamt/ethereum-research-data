---
source: magicians
topic_id: 4976
title: Anyone interested in earning some ether by looking at my node sync issue?
author: vnaeli
date: "2020-11-30"
category: Uncategorized
tags: [questions]
url: https://ethereum-magicians.org/t/anyone-interested-in-earning-some-ether-by-looking-at-my-node-sync-issue/4976
views: 1095
likes: 1
posts_count: 4
---

# Anyone interested in earning some ether by looking at my node sync issue?

Not sure which category is the best for this question.

I set up a `geth-1.9.42` full node and it, unfortunately, has the problem that

- eth.syncing.highestBlock never changes once geth started (also filed in geth’s github issues)
- eth.syncing.currentBlock is usually 70000 blocks behind the latest block reported by etherscan. eth.syncing.currentBlock grows by ~ 1 block per minute so it will never catch up.

I’ve spent too many hours trying to solve this problem, and this is the 3rd time I tried to set up a full node in the last 3 years, and I had been a Linux sysop for years with good knowledge of running network configuration and dæmons, yet I’m at my wit’s end. If you are an operator of a full node & can spend some time to help me over zoom or something **kindly PM me your Ethereum address for payment for your time**.

Since every year I make a project try to run a full node and fail, it’s fair to say **I have committed more than 100 working hours in the last 3 years** to get a node up and running and never achieved it. I set up Bitcoin nodes, ed2k nodes, BitTorrent etc with relative ease, geth is the most tricky of all.

If I talk to Ethereum users in meetups and Telegram, typically I am told to check

𝑎) network and

𝑏) if the host is too weak to run a full node.

So here we are:

## 𝑎) Network

There are constantly 50 peers and `eth.syncing.currentBlock` kept growing (at a slow rate), so that ruled out lack-of-peer issue.

NAT is often the first suspected in any network problems, but in my case `admin.peers` showed 50 peers, many peers with `network.inbound == true`, [meaning that they connected to this node](https://github.com/ethereum/go-ethereum/issues/21920). All ports are open and tested (with netcat).

Furthermore, the download/upload bandwidth used by geth, 1.3Mbits/s download and 300KBits/s uplod, is 1/16 of the available bandwidth, so it doesn’t look like we are choking on bandwidth. I called up the fibre-to-curb provider to upgrade the bandwidth 2× and verified the upgrade is effective (by downloading stuff), yet get still use the same amount of bandwidth (now amounts to 1/32 available bandwidth), so that rules out bandwidth problem.

## 𝑏) System too weak?

I can’t answer it because I don’t have a working geth setup to compare with, but following is my system’s data which shows **all resources are underutilised**: CPU, memory, disk_IO, available bandwidth. If the host configuration is too low, I should expect one of the resources to be fully used.

---

### Memory: 80% unused

```auto
$ free -m
              total        used        free      shared  buff/cache   available
Mem:          20022        4584         407           1       15030       15824
Swap:         13311           1       13310

```

This is not expected. I expect geth to use at least 16GB memory since I have given it `--cache 16384`. `top(1)` shows geth uses 10% to ~20% memory typically.

### System Load: medim-high but not maxed out

Since the CPU has 4 cores, load average 2.7~3.5, indicating mid-to-high but not full load. (Sometimes it goes to as low as 1.3). In my sysop years, clients starts to report errror when server’s load is approaching 1.5~2 times the number of cores, so this load look okay to me.

```auto
$ uptime
 23:47:24 up 15 min,  2 users,  load average: 3.54, 3.20, 1.95
```

### CPU usage: 33% of one core (total 4 core)

Geth typically uses 33% ~ 34% of one CPU. (It doesn’t look like multi-threadable)

### RAID performance: 170MB/s to 522MB/s

Using RAID 5 array of 4 disks. When not under load (not running geth), run `hdparm -t` 5 times to get this:

```auto
/dev/sdb:
 Timing buffered disk reads: 1046 MB in  3.01 seconds = 347.88 MB/sec
a@osboxes:~$ sudo hdparm -t /dev/sdb

/dev/sdb:
 Timing buffered disk reads: 1150 MB in  3.00 seconds = 382.90 MB/sec
a@osboxes:~$ sudo hdparm -t /dev/sdb

/dev/sdb:
 Timing buffered disk reads: 1322 MB in  3.02 seconds = 437.09 MB/sec
a@osboxes:~$ sudo hdparm -t /dev/sdb

/dev/sdb:
 Timing buffered disk reads: 1472 MB in  3.02 seconds = 487.37 MB/sec
a@osboxes:~$ sudo hdparm -t /dev/sdb

/dev/sdb:
 Timing buffered disk reads: 1570 MB in  3.01 seconds = 522.44 MB/sec
```

But sometimes `hdparm -t` reports only 170MB/s

## Replies

**vnaeli** (2020-11-30):

I carefully reread the document https://docs.ethhub.io/using-ethereum/running-an-ethereum-node/ which said:

> A consumer-grade laptop will be enough to run a full node, but not an archive node. An archive node does need 2+ TB of disk space, and that disk space cannot be HDD - it must be SSD for both full and archive nodes. Light nodes run fine on SD cards and HDDs.

Does this document mean what it said, that I should use SSD or SSD RAID (where I currently use a 4-HDD RAID5 configuration)? This is actually plausible because my SSD has 1500MB/s while the HDD RAID reports 350MB/s to 500MB/s. However, total disk IO reported by `iotop(1)` says

```auto
Total DISK READ:       321.04 K/s
```

Which is 1/1000 of the capacity of the current RAID, so I don’t see how improving disk I/O can help if it only uses 0.1% of existing IO capacity.

---

**wschwab** (2020-12-02):

Interesting. A full understanding of I/O utilization in clients is beyond my level of expetise, but since I see this isn’t getting a lot of traffic, I’ll take my best shot:

1. I would recommend opening up an issue with these details in the Geth GitHub, the main goal being to see if this level of I/O utilization is to be expected for some reason or another: https://github.com/ethereum/go-ethereum/issues . In a similar vein, if you are active on the Ethereum StackExchange, you could open a bountied issue there.
2. You may want to experiment using other clients. The two I would recommend are Turbo-Geth and Nethermind

---

**jpitts** (2020-12-05):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/v/f04885/48.png) vnaeli:

> A consumer-grade laptop will be enough to run a full node, but not an archive node. An archive node does need 2+ TB of disk space, and that disk space cannot be HDD - it must be SSD for both full and archive nodes. Light nodes run fine on SD cards and HDDs.

Does this document mean what it said, that I should use SSD or SSD RAID (where I currently use a 4-HDD RAID5 configuration)? This is actually plausible because my SSD has 1500MB/s while the HDD RAID reports 350MB/s to 500MB/s. However, total disk IO reported by `iotop(1)` says

Definitely use an SSD with a geth full node! I am not sure why you are seeing low disk IO during the sync with an HDD RAID, but perhaps geth sync would not be able to take advantage of that configuration. I have not tried an HDD RAID or SSD RAID so cannot recommend anything, but perhaps start by trying this w/ only an SSD for simplicity.

Also, there is a new feature in geth which can save you costs or enable you to sync if your SSD is not large enough. It enables you to split the chaindata across both an HDD and an SDD (for the part that requires one).



      [ethereum.stackexchange.com](https://ethereum.stackexchange.com/questions/84469/can-chaindata-be-split-across-two-or-more-locations)



      [![The Renaissance](https://ethereum-magicians.org/uploads/default/original/2X/1/15383604424da5c574b4dbcbd33bec3ae32184ae.png)](https://ethereum.stackexchange.com/users/27270/the-renaissance)

####

  **go-ethereum, nodes, clients, chaindata**

  asked by

  [The Renaissance](https://ethereum.stackexchange.com/users/27270/the-renaissance)
  on [05:42AM - 23 Jun 20 UTC](https://ethereum.stackexchange.com/questions/84469/can-chaindata-be-split-across-two-or-more-locations)










Hope this helps, and thanks for replying w/ those recommendations too [@wschwab](/u/wschwab)


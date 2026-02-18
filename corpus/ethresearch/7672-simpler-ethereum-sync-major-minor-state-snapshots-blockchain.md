---
source: ethresearch
topic_id: 7672
title: "Simpler Ethereum sync: Major/minor state snapshots, blockchain files, receipt files"
author: AlexeyAkhunov
date: "2020-07-11"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/simpler-ethereum-sync-major-minor-state-snapshots-blockchain-files-receipt-files/7672
views: 7380
likes: 16
posts_count: 18
---

# Simpler Ethereum sync: Major/minor state snapshots, blockchain files, receipt files

Recently, we decided to stop working on preparing the Merry-Go-Round snapshot sync algorithm in turbo-geth. Why? Because we think there is a way to achieve most of what it would deliver, but without most of the complexity. What is described here will not be a part of the first turbo-geth release. In the first release, the only way to sync would be to download all blocks starting from the Genesis, and execute them. The timing is not that bad - it definitely won’t take a month. On a machine with an NVMe device, it can take around 50 hours to obtain the node synced to the head of the mainnet and all history present and indexed.

In the subsequent releases, we would like to introduce the ability to sync from more recent state than genesis. Initial idea is this. Let’s say, every 1m blocks (~6 months time), we will manually (or in the future automatically) create a snapshot of the entire state, and of all the blocks and receipts prior to that point. This will result in 3 files (and approximate sizes if this were done about now):

1. State snapshot file, contains all the accounts, contract storage, and contract bytecodes. ~50Gb
2. Blockchain file, containing all block headers and block bodies from genesis up to the snapshot point. ~160Gb
3. Receipt file, containing all the historical receipts from genesis up to the snapshot point. ~130Gb

These 3 files would be seeded on the BitTorrent (and perhaps Swarm) by the turbo-geth nodes (we want to try to plug in the bitTorrent library).

One slight technical challenge for such seeding is the ability to utilise the state snapshot file, while seeding it, otherwise these 50Gb would just be “wasted”, meaning this space is only useful for seeding to other nodes, but not for anything else. It should be possible to organise the state database as an overlay, where actively modifiable state “sits” on top of the immutable snapshot file. Anytime we try to read anything from the state, we look up in the modifiable state, and if not found there, we look up in the snapshot file (that means that snapshot file needs to have an index in it).

As you might have guessed, there would be two alternative ways to sync:

1. Download blockchain file, and execute all the blocks from genesis. Result - entire history from genesis, receipts, current state.
2. Download the most recent state snapshot file, download blocks (from eth network) after the snapshot point, and execute blocks after the snapshot points. Result - history only starting from the snapshot point, current state. If historical receipts are required, they can be downloaded as the receipt file.

How large would that “modifiable” state be (the one that sits on top of the state snapshot file as overlay)? Here is some rough calculation. As of the block 10’416’641, there were 92’430’646 accounts and 334’797’797 storage items in the state, or 427’228’443 items in total. That makes 125 bytes per item on average.

Number of modified accounts between blocks 9’416’641 and 10’416’641 was 25’191’312, and number of modified storage items: 88’451’010, or around 13G. This is how large the modified state would grow during 1m blocks. After that point, it will be merged into the snapshot, and the new snapshot will be seeded over the BitTorrent (or Swarm) network.

The second approach to syncing (from recent state snapshot) still requires executing at most 1m blocks. Depending on the performance of implementation, it might take anything from few hours to couple of days.

## Replies

**AlexeyAkhunov** (2020-07-11):

This idea can be taken a bit further. If it is too much to ask to run through at most 1m worth of blocks, we can introduce minor snapshots, or “booster” snapshots that would need to be downloaded on top of the most recent major snapshot. For example, if we make major snapshots every 1m blocks (~6 months), we could make minor snapshots every 100k blocks (~18 days). Minor snapshots can still be distributed via BitTorrent or Swarm, but their content address won’t be hard coded in the releases. Instead it will have to be discovered in a different way, for example, via a web-site, from social media announcements etc. How large would these minor “booster” snapshots be? Here are some approximations for the block range  (9’416’641; 10’416’641):

100k: (9’416’641;  9’516’641): 2’905’445 accounts, 9’326’428 storage items, ~ 1.42Gb

200k: (9’416’641;  9’616’641): 5’237’667 accounts, 16’492’133 storage items, ~ 2.53Gb

300k: (9’416’641;  9’716’641): 8’507’911 accounts, 23’804’510 storage items, ~ 3.76Gb

400k: (9’416’641;  9’816’641): 11’175’265 accounts, 31’976’775 storage items, ~ 5.02Gb

500k: (9’416’641;  9’916’641): 13’692’905 accounts, 40’478’725 storage items, ~ 6.31Gb

600k: (9’416’641;  10’016’641): 15’968’439 accounts, 49’739’547 storage items, ~ 7.65Gb

700k: (9’416’641;  10’116’641): 18’159’271 accounts, 58’982’125 storage items, ~ 8.98Gb

800k: (9’416’641;  10’216’641): 20’545’442 accounts, 68’204’516 storage items, ~ 10.33Gb

900k: (9’416’641;  10’316’641): 22’581’832 accounts, 77’817’744 storage items, ~ 11.69Gb

It seems unlikely that it would be worth going another level of such “recursion” trying to bring the interval down to 10k blocks, because complexity of triple overlay would mount up

---

**quickBlocks** (2020-07-11):

I would suggest you use IPFS over any other store not-withstanding any political Eth/Not Eth considerations. It clearly has a significantly more active developer community.

Also – wherever you store this ‘immutable snapshot’, please, please, please, please, please put the hash of that immutable store in the block header (that is, put it under consensus). This would force the format of this snapshot to NOT be implementation specific, which would (it seems to me) allows for access to the full history and state of the chain (up until that point) with nothing more than just that hash.

---

**AlexeyAkhunov** (2020-07-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/quickblocks/48/406_2.png) quickBlocks:

> Also – wherever you store this ‘immutable snapshot’, please, please, please, please, please put the hash of that immutable store in the block header (that is, put it under consensus)

We cannot do from the start, obviously, but if the approach works and proves to be successful, we can try to make that happen

---

**quickBlocks** (2020-07-11):

Why do you say that? Too complicated?

---

**AlexeyAkhunov** (2020-07-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/quickblocks/48/406_2.png) quickBlocks:

> I would suggest you use IPFS over any other store not-withstanding any political Eth/Not Eth considerations. It clearly has a significantly more active developer community.

We need to look deeper into various options, like BitTorrent, Swarm and IPFS. My main requirement at the moment would be to make it possible to make our nodes mandatory seeders of this content, instead of relying on other pieces of network to keep it. I am not sure how that would work in Swarm or IPFS, and I would be glad to be educated on that

---

**AlexeyAkhunov** (2020-07-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/quickblocks/48/406_2.png) quickBlocks:

> Why do you say that? Too complicated?

Because placing things in the header required hard fork with all the necessary pre-conditions. We will first make it work well without a hard fork, then introducing this in a hard fork would be easier

---

**quickBlocks** (2020-07-11):

Would people running super light nodes be able to query the location and would the format of the data be non-implementation specific in the early versions?

---

**AlexeyAkhunov** (2020-07-11):

> Would people running super light nodes be able to query the location and would the format of the data be non-implementation specific in the early versions?

In the early versions it will be by definition implementation specific, because we can start experimenting without waiting for anyone else. But if there is interest from other implementation teams to join in, we will of course work on a standard.

---

**AskAlexSharov** (2020-07-12):

Maybe it’s possible to store Headers/Bodies/Senders in another database, on another disk. This db will store snapshot + last blocks without any overlay logic: because this data are immutable.

Current turbo-geth sync implementation shows boundaries of write transactions. Boundaries of read transactions may be less clear because of RPC, but RPC consistency requirements may be relaxed.

---

**AlexeyAkhunov** (2020-07-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/askalexsharov/48/3240_2.png) AskAlexSharov:

> Maybe it’s possible to store Headers/Bodies/Senders in another database, on another disk

Yes, that is definitely possible. go-ethereum currently has something similar, called “freezer”, or “ancientdb”, where it places blocks and receipts into indexed flat files, delete them from the main db, and use those files for reading

---

**pipermerriam** (2020-07-13):

To play devil’s advocate:  This feels similar to `GetNodeData` in that we have a synchronization primitive that also dictates database design.  Something we should be cognizant of since this “overlay” approach could prove sub-optimal and cause the same type of problems as `GetNodeData` is causing today.

I don’t have any specific objection so this is pure conjecture, but I felt it was worth making note of.

---

**vbuterin** (2020-07-13):

What would be the value of putting the hash of the snapshot into consensus? Presumably a client that syncs from a snapshot would compute the state root and verify that the state root matches the state root in the block header, no? Invalid snapshots would be a relatively exceptional case, so I don’t see much benefit in trying that hard to make it easy to detect them; as long as clients perform the state root check at the end it seems like it should be enough.

---

**quickBlocks** (2020-07-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What would be the value of putting the hash of the snapshot into consensus?

If the hash you put in the header points to content-addressable data, non-blockchain software (auditing/accounting/local explorers) could read and process that data without having to run the chain or with only a super-minimal client. People could even get the hash from their friend via email if they wanted to. The system itself should make direct access to the data easy. It’s not perfect, obviously, but it’s WAY better than current methods of getting data from the chain via Web 2.0 explorers that simply scrape the data and deliver it using web 2.0 APIs which is an utter disaster when it comes to trusting the data.

Also, if more people knew exactly where the state data was (via a hash on a content-addressable store), and people started building software that relied on that data being in place, there would arise naturally a tendency for non-blockchain apps to pin their own versions of the snapshots. If everyone knew that the snapshot data was at a certain place, it would tend to magically appear there because people would need it, and because they can’t rely on other people to pin it, they would pin it themselves.

These snapshot hashes may or may not have use “inside” the blockchain client software, but they have huge use outside.

---

**evertonfraga** (2020-07-15):

I had an idea:

### Objective

To have some specially-crafted/configured ethereum nodes, with the purpose of providing static state snapshots, making use of the presently available fast sync mechanism, with some added tricks. Or: “State snapshot fast sync with the help of cold ethereum clients”.

We’d have a pool of ethereum nodes frozen in time, only reachable by direct connections, so they would have equivalent states to share to peers.

### Premise

Fully backwards compatible with all fast-sync enabled clients, requiring little configuration effort on the node operator (consumer) side.

### Specs:

- Providers would have the chain synced to a fixed block number (let’s say, 10M).
- Providers’ highest known block equals to their own synced block.
- Providers are completely disconnected from the “live” mainnet, so they are effectively frozen in time.
- Clients that need a jumpstart would connect ONLY to those Providers, so they could sync block headers, block bodies and state entries from them.

Clients would start with the following config:

```
// Jumpstart
geth --syncmode=fast --maxpeers=0 --exitwhensynced

[staticnodes]
enode://ethereum-snapshots.com
…
```

After jumpstart, they could use the normal ways to get synced.

### Subjective work load estimation:

- Client developer: zero effort
- Node operator: only needs some configuration effort
- Provider developer: Fine tuning of an existing client to optimize for this use case.

Any feedback? Sorry if I hijacked your post too hard, [@AlexeyAkhunov](/u/alexeyakhunov) ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**AlexeyAkhunov** (2020-07-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/e/8491ac/48.png) evertonfraga:

> Fully backwards compatible with all fast-sync enabled clients, requiring little configuration effort on the node operator (consumer) side.

I think it is legit idea and anyone is welcome to implement it, and perhaps use this kind of snapshot with an overlay. But we won’t be doing it in turbo-geth, because we do not have this representation of data anyway, and this representation is much harder to iterate over and otherwise process than flatter formats

---

**poemm** (2020-07-21):

I am sure that you have considered how a shorter (say 10,000 block) regenesis period would significantly change the system. In particular,

1. the need for sync protocals may disappear because clients can just wait a few days for the next regenesis, and
2. active state trees can be kept in RAM, lifting the disk i/o bottleneck on transactions, with storage becoming a persistent merkleized memory.

Of course, throughput is lower because witnesses have longer paths on average, but this witness overhead is logarithmic, or less because of temporal locality.

Another option which gives similar properties is a size-capped regenesis period, where we have a regenesis whenever active state (including hashes) exceeds, say, 3 GB. This size-capped regenesis is more efficient but less predictable.

What are your thoughts on a smaller regenesis period and size-capped regenesis?

---

**AlexeyAkhunov** (2020-07-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/poemm/48/2402_2.png) poemm:

> I am sure that you have considered how a shorter (say 10,000 block) regenesis period would significantly change the system.
> What are your thoughts on a smaller regenesis period and size-capped regenesis?

I have thought of this, of course. But I was not yet sure how to best solve the distribution of the root hash. But now I see a solution. The state root hashes are contained in the headers. So we will still need to ask users to download the header chain (or trust some segment of it). More frequent ReGenesis events will inconvenience transaction senders more, very frequent ReGenesis events may do so to the point that it might become unworkable. Because transaction senders will need to keep re-downloading the entire state after each ReGenesis. Also, as the chain crosses ReGenesis event, most transactions will have to be evicted from the transaction pool and re-submitted, otherwise they will just burn gas needlessly (their witnesses will become invalid).


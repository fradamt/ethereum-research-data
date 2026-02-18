---
source: ethresearch
topic_id: 19788
title: Torrents and EIP-4444
author: parithosh
date: "2024-06-12"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/torrents-and-eip-4444/19788
views: 6381
likes: 29
posts_count: 21
---

# Torrents and EIP-4444

# Torrents and EIP-4444

### Introduction

EIP-4444 aims to limit the historical data that Ethereum nodes need to store. This EIP has two main problems that require solutions: Format for history archival and Methods to reliably retrieve history. The client teams have agreed on a common [era files](https://ethresear.ch/t/era-archival-files-for-block-and-consensus-data/13526) format, solving one half of the problem. The second half of the problem, i.e Method to reliably retrieve history will likely not rely on a single solution. Some client teams may rely on the [Portal network](https://ethereum.org/en/developers/docs/networking-layer/portal-network/), some rely on torrents, others might rely on some form of snapshot storage.

### Torrents for EIP-4444

Torrents offer us a unique way to distribute this history, torrents as a technology have existed since 2001 and have withstood the test of time. Some client teams, such as [Erigon](https://github.com/ledgerwatch/erigon) already include a method to sync via torrents that has run in production systems.

In order to make some progress on the Torrent approach of history retrieval, the files would first be required. So an era file export was made on a [geth](https://github.com/ethereum/go-ethereum/) running version `v1.14.3` . To explore the initial idea, the torrent approach chose pre-merge data as a target. The merge occurred at block height [15537393](https://etherscan.io/block/15537393), meaning all pre-merge data could be archived by choosing a range of 0 to block 15537393. The era files were then created using the command ` geth --datadir=/data export-history /data/erafiles 0 15537393`.

Once the era files were created, they were verified using the command `era verify roots.txt`, with the source of the `roots.txt` file being [this](https://gist.githubusercontent.com/lightclient/528b95ffe434ac7dcbca57bff6dd5bd1/raw/fd660cfedb65cd8f133b510c442287dc8a71660f/roots.txt). The entire process has been outlined in [this PR comment](https://github.com/ethereum/go-ethereum/pull/26621#issuecomment-1434023464). The verification output was found to be this log message: `Verifying Era1 files             verified=1896,  elapsed=5h21m49.184s`

The output era files were then uploaded onto a server and a torrent was created using the software `mktorrent`. An updated list of trackers was found using the github repo [trackerslist](https://github.com/ngosang/trackerslist). The trackers chosen were a mix of http/https/udp in order to allow for maximal compatibility. The chunk size of the torrent was chosen to be 64MB, which was the max allowed and recommended value for a torrent of this size.

The result of this process is now a torrent of size 427GB. This torrent can be imported with this magnet link  and a torrent client would be able to pull the entire pre-merge history as era files.

#### Tradeoffs

There are of course some tradeoffs with torrents, as with many of the other EIP-4444 approaches:

- Torrents rely on a robust set of peers to share the data, there is however no way to incentivise or ensure that this data is served by peers
- A torrent client would need to be included in the client releases and some client languages might not have a torrent library
- Torrents would de-facto expect the nodes to also seed the content they leech, this would increase node network requirements if they choose to store history
- The JSON-RPC response needs to take into account that it may not have the data to return a response in case the user decides to not download pre-merge data

### Conclusion

A client could potentially include this torrent into their releases and avoid syncing pre-merge data by default, which could then be fetched via torrent if a user requests it (perhaps with a flag similar to `--preMergeData=True`). The client could also hardcode the hash of the expected data, ensuring that the data retrieved matches what they expect.

### Instructions for re-creating torrent:

- Sync a geth node using the latest release
- Stop the geth node and run geth --datadir=/data export-history /data/erafiles 0 15537393 to export the data in a folder called data/erafiles(Warning, this will use ~427GB of additional space)
- Use the mktorrent tool or the rutorrent GUI to create a torrent. Choose the /data/erafiles/ folder as the source for the data. Next, obtain the latest open trackers from this github repository. Choose a healthy mix of udp/http/https trackers and choose the chunk size of the torrent to be 64MB.
- The tool should output a .torrent file, the GUI will also allow you to copy a magnet link if that is required

### Instructions for download and verification of torrent data:

- Download the torrent data with this magnet link and in a torrent client of your choice: link
- Clone the latest release of geth and install the dependencies
- Run make all in the geth repository to build the era binary
- Fetch the roots.txt file with the command: wget https://gist.githubusercontent.com/lightclient/528b95ffe434ac7dcbca57bff6dd5bd1/raw/fd660cfedb65cd8f133b510c442287dc8a71660f/roots.txt
- Run era verify roots.txt in the folder to verify the integrity of the data

## Replies

**imkharn** (2024-06-12):

“there is however no way to incentivise or ensure that this data is served by peers”

Why would a client team use torrent? Incentivized data storage exists and better ones are being developed. Additionally more efficient ones exist where only a fraction of the data is stored on each node with essentially the same chance of the data being available.

---

**arnetheduck** (2024-06-13):

In order to be able to verify the data in the torrent, one needs access to `roots.txt` which actually is an [accumulator](https://www.ethportal.net/concepts/hash-accumulators) similar to the one found in the consensus beacon state.

For verification purposes, it would be best if this file was included in the torrent as that would allow consumers of the data to hardcode a single hash-of-the-accumulator which in turn can be used to verify the era1 file contents, reducing the number of moving parts further down to a single hash - this hash could then be distributed together with other mainnet metadata, for example in the [mainnet](https://github.com/eth-clients/mainnet) repository that establishes configuration parameters.

---

**kdeme** (2024-06-13):

> this hash could then be distributed together with other mainnet metadata

And there is EIP-7643 which defines this hash in order to be able to verify the whole list of roots.

It would be good to have it in the mainnet metadata indeed.

Also the individual roots are specified in EIP-7643.

---

**parithosh** (2024-06-13):

Could you elaborate on what incentivized data storage method could be used instead?

The essential issue with incentivising data storage is that the user would then have to pay for data access, which isn’t currently the paradigm if you run your own node (other than hardware costs ofc)

---

**parithosh** (2024-06-13):

I like the approach of having the `EIP-7643` roots available as mainnet metadata (although I am not sure EL teams currently subscribe to the mainnet repo the same way CL devs do, maybe this will get them to start). Additionally getting verification data from a different source as the source data seems like a good idea.

---

**arnetheduck** (2024-06-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/parithosh/48/11805_2.png) parithosh:

> Additionally getting verification data from a different source as the source data seems like a good idea.

The only verification data you need in this case is the hash from [EIP-7643](https://eips.ethereum.org/EIPS/eip-7643), namely `0xec8e040fd6c557b41ca8ddd38f7e9d58a9281918dc92bdb72342a38fb085e701` .

This hash allows you to verify `proofs.txt` which in turn allows you to verify the rest of the era archive (strictly, `proofs.txt` shouldn’t be needed either, but I suspect it’s convenient to have it to make the process of finding errors in the files more fine-grained) - there exists no benefit whatsoever of getting this file from a separate source (as long as you have the above hash) - it belongs inside the torrent.

This is also the problem with the idea of using a torrent, which is why it’s somewhat unattractive to clients: there is a structural mismatch in the verification mechanism used - the hashes of the torrent itself don’t line up with hashes used in ethereum, which is why we need `proofs.txt` to begin with - this makes partial verification somewhat involved (because as you’re downloading the files in the torrent, you need to verify both the torrent hashes *and* the ethereum proofs).

That said, I do believe there’s utility in socially coordinating around a single torrent file for convenience of testing, if nothing else ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**parithosh** (2024-06-13):

hmm, Yeah I’d also tend to agree that the proofs.txt won’t be needed at all. Wouldn’t we just rely on the inherent integrity offered by the torrent in that case? Changing any byte in a torrent should invalidate the whole torrent, so as long as we agree that the torrent values were checked before the torrent was included in a client release - we wouldn’t need any additional verification.

---

**arnetheduck** (2024-06-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/parithosh/48/11805_2.png) parithosh:

> Wouldn’t we just rely on the inherent integrity offered by the torrent in that case?

We ideally want to reach a place where “most” pieces of the ecosystem use the same verification method - both portal and era1 natively use the `proofs.txt` verification that work with native ethereum algorithms for hashing etc - torrent adds an alien component to the security in the form of its own verification - this is not great, because it doesn’t allow connecting it to era1, portal and other pieces.

My point with proofs not being needed strictly is that the one hash in EIP-7643 combines all the hashes in proofs.txt - you don’t need proofs.txt *unless* you want to verify smaller chunks of data - adding proofs.txt to the torrent allows you to verify each era separately instead of having to verify all 400+GB at a time.

> agree that the proofs.txt won’t be needed at al

this is not quite what I meant - I mean it’s not strictly necessary from a security point of view, but it is very useful to have *inside* the torrent file for convenience of verification.

---

**imkharn** (2024-06-13):

Noting that I have not surveyed the incentivized file storage field since 2019… these schemes usually work by sending out challenges to people who are supposed to be online. They are required to produce the data sample or they get slashed. Considering blockchain data is public (relative to people storing personal and corporate files) , it may need to be an encrypted fragment so that they cant pass the challenge by looking up the data online. The most efficient decentralized data storage (as measured by amount of data duplication redundancy needed for a given percent chance of losing data) is probably still Storj [Understanding File Redundancy: Durability, Expansion Factors, and Erasure Codes - Storj Docs](https://docs.storj.io/learn/concepts/file-redundancy).

Regarding covering the cost of the data storage, I see 2 options:

1. Force. Enshrined so nodes are required by threat of slashing to store a fraction of the old data. Challenges constantly spot check.
2. Paid. The inefficiency from overduplication of data already exists, Consider that nodes might already be willing to pay a small amount to free up hard drive space. Since data availability needs to be forced either way, this is more of an extension to the force suggestion whereby nodes can declare how much space they want to give to the network. If they offer above/below par some financial value is transferred.

---

**parithosh** (2024-06-14):

Okay, that makes sense - I’ll have to recreate the torrent file with the proofs.txt, I can do so and update the post!

---

**parithosh** (2024-06-14):

Thank you for the links!

My main criticism of that approach is implementation complexity. Maybe the protocol adds such logic in the future, but I don’t see us adding such complexity in the base layer for a few more forks (years) at this point.

---

**parithosh** (2024-06-28):

[@arnetheduck](/u/arnetheduck) By proofs.txt, do you mean the `roots.txt` found [here](https://gist.githubusercontent.com/lightclient/528b95ffe434ac7dcbca57bff6dd5bd1/raw/fd660cfedb65cd8f133b510c442287dc8a71660f/roots.txt)?

---

**chfast** (2024-06-28):

The magnet links doesn’t work, URLs probably removed.

---

**arnetheduck** (2024-07-01):

Indeed - these are the “test cases” from EIP-7643 which provide a hash for each era file separately - they should be the same. We can call it `eip7643-proofs.txt` in the torrent even.

---

**kdeme** (2024-07-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/parithosh/48/11805_2.png) parithosh:

> Instructions for re-creating torrent:

Also important to mention here that when creating the era1 files (and thus the torrent), the exact result might differ cross client and cross client versions. This is due to the fact that Snappy compression is used which will have non-deterministic output over different implementations/versions.

It is not an issue for the verification part however, as that is based on SSZ `hash_tree_root` and has already been explained/addressed in above discussion.

I agree that having `eip7643-proofs.txt` in the torrent can come in handy for verifying only certain eras of the torrent.

---

**parithosh** (2024-07-25):

I’ve updated the torrent with the proofs as requested, the new torrent magnet link can be found here.

Since the earlier link has been deleted for some reason, I’ve also uploaded the torrent file in an s3 bucket here: `https://ethereum-mainnet-pre-merge-era-files.fra1.cdn.digitaloceanspaces.com/EthereumMainnetPreMergeEraFiles.torrent`

cc [@chfast](/u/chfast)

---

**chfast** (2024-07-25):

The new link has been deleted too. Maybe a discourse policy?

---

**parithosh** (2024-07-25):

Probably. I’ve also uploaded it to IPFS, CID is `QmejuzLRmhiwoW7HuJ6V8MoSqjxPhfjarkAhPqrhy8ScSp` and e.g retrieval URL `curl https://gateway.pinata.cloud/ipfs/QmejuzLRmhiwoW7HuJ6V8MoSqjxPhfjarkAhPqrhy8ScSp`. The above mentioned s3 bucket would also work.

---

**r4f4ss** (2024-08-10):

Is there a torrent for testnets too? Holesky seems especially difficult to sync execution layer, there are near no nodes providing initial history. I have been experiencing several hours “Looking for peers”.

---

**arnetheduck** (2024-10-28):

Holesky began its life merged, so there is no “era1” - you can get era files however: https://holesky.era.nimbus.team/

We have sepolia too:

https://sepolia.era1.nimbus.team/

https://sepolia.era.nimbus.team/


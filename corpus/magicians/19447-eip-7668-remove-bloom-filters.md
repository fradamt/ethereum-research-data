---
source: magicians
topic_id: 19447
title: "EIP-7668: Remove bloom filters"
author: vbuterin
date: "2024-03-31"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7668-remove-bloom-filters/19447
views: 3346
likes: 22
posts_count: 16
---

# EIP-7668: Remove bloom filters

Require the bloom filters in an execution block, including at the top level and in the receipt object, to be empty.

https://github.com/ethereum/EIPs/pull/8368

## Replies

**matt** (2024-04-01):

Could probably add some more color to the specification. As I understand it, you’re proposing the logs bloom in the header to be reduced to 0 bytes long instead of the regular 256 bytes. This means there will still be an RLP list entry `0x80` for the element.

An alternative to this proposal would to enforce the bloom filter be an empty 256 byte zero value. This would compress well over the wire and require more minimal changes to clients (many clients have fixed size 256 byte value already coded throughout the client). Since the RLP element will still be in the object, I don’t think even future clients will be able to substantially simplify the header struct with either of these proposal, but both will allow clients to stop computing the logs bloom.

---

**vbuterin** (2024-04-02):

> An alternative to this proposal would to enforce the bloom filter be an empty 256 byte zero value. This would compress well over the wire and require more minimal changes to clients (many clients have fixed size 256 byte value already coded throughout the client). Since the RLP element will still be in the object, I don’t think even future clients will be able to substantially simplify the header struct with either of these proposal, but both will allow clients to stop computing the logs bloom.

I proposed 256 zero bytes originally, and other people told me “why not make it actually empty” ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

I am ok with either approach.

Also, re “there will still be an RLP list”, it’s worth keeping in mind that there are also EIPs being worked on to move receipts over to SSZ. One other option would just be to do both at the same time and make the SSZ receipt struct not contain a bloom field.

---

**Nerolation** (2024-04-03):

Are RPCs currently using them, f.e. I query for all Transfer event of USDC, would my node use the bloom filters to first check which blocks are candidates (to then find out all of them)?

I do need to query for rarely used event logs from time to time. Would that make it harder for me to get to those logs. E.g. I want to get all “freezeAccount” events from a certain contract, we have 1xx events distributed over 1.xxx.xxx blocks. → “harder” in the sense of “slower” because my node couldn’t use bloom filters and would have to check every block?

---

**matt** (2024-04-03):

The bloom filter is really only useful if you need to do that look up with light client assumptions (e.g. just via the header chain). If you have a full node, your client software can still construct and maintain the bloom filters locally to find events efficiently.

---

**lettucer** (2024-04-03):

This EIP does not have sufficient motivation. Even though the “Purge” idea outlined in the blog post hints that this will simplify the protocol, it is unclear to practitioners what sort of advantage this EIP brings to them.

- What amount of cost savings (e.g. storage or sync time) will come from this? Who benefits? Why do we need this now?

Searching through logs is a very common thing. Even if popular dapps are centralized and use other indexes, that should not preclude smaller developers from making log searches. If this EIP is part of the “purge” it should not require developers to adopt a *second* protocol just to find events; that would not be purgelike.

- What performance impact will this have on event searches at the node level? Would dapps still be able to search for events using eth_getLogs?

From the way it is worded, it sounds like this EIP will wipe out all light client functionality that makes proving events happened possible with just the headers. Not being able to prove events would be an awful concession to centralization. Light clients operating on L2s which prove to smart contracts that events happened on Ethereum are an important use case, if underutilized today, and a way to construct cross-chain history with fewer trust assumptions.

- Can events still be proven via the block header structure?

I think the answers to all of these questions must be included in the EIP document. As-is, there are no hard numbers. Saying it’s “too slow” and “dapps use centralized extra-protocol services anyway” is not enough to make up for the cost it seemingly imposes on *truly* decentralized dapps. And I do not count applications which make use of extra-protocol services as true dapps. That’s capp.

---

**lettucer** (2024-04-03):

Although it seems I cannot edit my previous post, I think the last question I had - Can events still be proven via the block header structure - is true, using the transaction receipts root, which is valuable for making proofs of events.

---

**vbuterin** (2024-04-03):

I think if we want a log system that’s useful to truly decentralized apps, we should work on ZK-SNARKed sidecars. A basic construction is fairly simple:

- Make a state tree that maps log_topic -> logs_with_that_topic (the logs themselves could perhaps be stored via a hash onion, so adding a log means tree[topic] = hash(tree[topic], new_log); this would make it very easy to query a chain of logs for a given topic)
- For every new ethereum block, generate a new state root for this tree, and publish a ZK-SNARK proving that the updates to the state tree match the ethereum block’s receipt root. The SNARK would also prove the correctness of the previous SNARK, so you would only need to verify a single proof
- Clients can then just ask for roots and branches and hash chains from this tree

The nice thing about this strategy is that it’s very flexible, so you can make changes to what gets logged without requiring ethereum protocol hard forks. And it would actually be optimal for the task: an arbitrarily long history search for a given topic would just be one branch query followed by one hash chain query, no need to scan through millions of bloom filters.

So I think if we really want to support actually-decentralized dapps (a goal that I strongly support), we should be doing much more work on this direction.

(As for how to make it actually happen, one key step is to SSZ-ify the receipt tree, which would then make actually constructing the SNARK described here much easier and mostly a task of gluing together existing components)

---

**lettucer** (2024-04-04):

Thank you for your reply. I am glad you already sketched an alternative solution. I think pairing this EIP with moving receipts to SSZ would be a good idea.

I think calculating the false positive rate helped give me a better picture of the current state bloom filter.

Take a recent (full) block 19,580,078.

1,379 bits are set to 1 in the Bloom filter.

m = 2048 bits

k = 3 hash functions

Estimate the number of unique entries (topics/addresses)

n* = -2048/3 * ln(1 - 1379/2048)

n* = 763.79

Using the approximation:

FPR = 1 - e^(-k * n / m))^k

FPR = (1 - e^(-3 * 763.79 / 2048))^3

FPR = 0.30528

For an address + log combination this would be approximately 0.30528^2 = 0.09035. Not useless, but less effective than we would like.

I wonder if the ZK-SNARK solution would also be able to filter by address, since the address + topic search is common and for this the use of the Bloom filter is still effective. And I still wonder if this EIP will reduce/remove the ability to query full nodes for events.

---

**Mihai673** (2024-04-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> a log system that’s useful to truly decentralized apps

I’m ecstatic to hear core devs discuss building practical dapp tooling.

While approaching Ethereum from the dapp side, I’ve never felt the need to create an account on here until now (too much moon math). I know many participants in the dapp layer feel slighted by a (perceived) lack of core dev attention (notice us, senpai). So this seems like a good time to discuss common goals and needs.

Your construction sounds promising yet complicated and speculative (how hard is it unroll a ZK-SNARK hash onion? ![:sob:](https://ethereum-magicians.org/images/emoji/twitter/sob.png?v=12)). As opposed to existing log indexing methods that work and are battle-tested.

It seems you’d want different tools depending on the job, so clearly motivating use-cases seems key.

When would someone want to query logs from a lightclient? Is it for decentralized frontends spinning to run a lightclient for log retrieval instead of relying on a centralized RPC? That does sound very valuable.

I’d argue a more common use-case is a user that doesn’t want to rely on any third parties for data access, and wants to do everything locally. Local-first is a purer form of decentralization, as without it you’re decentralizing across data centres. To do that, we currently rely on archive nodes. The ongoing work by Erigon and Reth teams to provide fast-syncing archive nodes with <3 TB footprintgs is crucial. This allows local-first apps like Rotki and Otterscan to thrive. On a day like today where Etherscan was down, running a local block explorer was only possible using 1 Execution Layer client (Erigon, because it relies on custom tracing methods).

You can do performant local indexing of the entire chain through TrueBlocks, a tested method that’s been working for years. I don’t see a need for a new index definition beyond this, as a local-first dapp user. I can envision tooling to deliver subsets of the index to lightclients on demand, in the same way as out-of-protocol purged state (though the entire index is only about 80gb). I don’t need to verify the index if I’ve built it locally from my archive node. For those that do, can we think of some battle-tested mechanism to arrive at consensus for which IPFS hash stores the index (Proof of Storage? might just work.)

Some standardization and support for better tooling is sorely needed in the existing toolchain. Without support from core devs I feel like we’re likely to spiral into a world where local-first is forgotten and standards keep diverging into more localized solutions that increasingly resemble the walled garden of data that is TradFi. I hope the indexing wizards figure out a way for me to run an archive node for every L2, so I can be data-sovereign in a rollup-centric future.

---

**vshvsh** (2024-04-05):

A non-light-client use case for bloom filters in the block [found in the wild](https://twitter.com/dizhel/status/1776162278355701826): cross-checking the RPC data.

---

**vbuterin** (2024-04-05):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/6a8cbe/48.png) Mihai673:

> I’d argue a more common use-case is a user that doesn’t want to rely on any third parties for data access, and wants to do everything locally. Local-first is a purer form of decentralization, as without it you’re decentralizing across data centres. To do that, we currently rely on archive nodes. The ongoing work by Erigon and Reth teams to provide fast-syncing archive nodes with <3 TB footprintgs is crucial. This allows local-first apps like Rotki and Otterscan to thrive. On a day like today where Etherscan was down, running a local block explorer was only possible using 1 Execution Layer client (Erigon, because it relies on custom tracing methods).

For this use case, I think archive nodes should feel free to keep maintaining bloom filters and logs locally. Doing that does not require logs to be hashes into blocks or otherwise part of the protocol. With locally-stored logs, you could even increase the per-block bloom size to something larger (10000 bits?) to decrease the false positives. Removing logs from the protocol does not weaken the ability of archive nodes to do indexing (including continuing to use their existing indexing strategy) locally *at all*.

As for broader goals, I think the key theme of the 2020s is that we are building things that are decentralized *and* friendly to the average user. Locally-run archive nodes will never be friendly to the average user, and so we need to make decentralized frontends querying a light client actually work well and be the thing that the whole ecosystem uses by default. So yes, that is the goal ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

And I actually think that the ZK-SNARK-based approach I outline is not that hard! A competent team should be able to make a prototype quite quickly, certainly faster than the time that it would take to get to a hard fork that replaces log roots with SSZ.

---

**tjayrush** (2024-04-05):

The other thing to say about TrueBlocks is that it’s very well specified: https://trueblocks.io/papers/2023/specification-for-the-unchained-index-v2.0.0-release.pdf.

One thing people miss about TrueBlocks is that it keeps the idea of a bloom filter, but it moves the bloom filter to the “chunk” level (chunks being collections of blocks). People interact with the chain in bursts. 10 times in a day, then not again for weeks. Or 100 times in ten minutes then not again for an hour. Whatever the case may be, their addresses appears in bursts. The indexing should reflect that.

Removing blooms from the block (and the receipt, I presume) is a good idea, but removing it entirely seems like a bad idea. Putting a bloom filter at a place that mimics the nature of the end user’s usage makes more sense. Another thing we did was make the bloom filters adaptive so they grow or shrink depending on how many items are put into them. This keeps the false-positive rate constant and makes the size-on-disc minimal.

And, as far as usefulness of the bloom fitlers, if you read deeply enough in the above spec, you’ll see that the way TrueBlocks works is that the end-user applications download only the chunk-level bloom filters (4 GB for an index of Ethereum Mainnet for every appearance of every address). In other words, they don’t need an archive node to get the benefits of a full index of the archive node.

The end-user app can consult this 4GB chunk blooms and download only the portions of the index that they’re interested in. Natural sharding.

Plus, if the end-user app “pins-by-default” on IPFS, you get naturally-grown sharing.

This may be coming across as a shill (I wrote TrueBlocks and the Unchained Index under EF grants over the years), but it actually already works and it works in exactly the way a truly decentralized application (and a truly decentralized world) would want it to work.

Have you seen this, [@vitalik](/u/vitalik)?

---

**zsfelfoldi** (2024-07-18):

Maybe worth mentioning here:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zsfelfoldi/48/1697_2.png)
    [EIP-7745: Two dimensional log filter data structure](https://ethereum-magicians.org/t/eip-7745-two-dimensional-log-filter-data-structure/20580) [Core EIPs](/c/eips/core-eips/35)



> Discussion topic for EIP-7745
>
>
>
> An efficient and light client friendly replacement for bloom filters. This EIP proposes a new data structure that adds a moderate amount of consensus data that is optional to store long term, has limited processing and memory requirements and allows searching for log events with 2-3 orders of magnitude less bandwidth than what bloom filters allowed back when they were not rendered useless by over-utilization. It also inherently adapts to changing block utilizati…

I believe this is a realistically implementable thing that would make log search really efficient and light client friendly, without centralized services or any fancy math ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) The basic idea is based on a solution that I implemented in Geth 7 years ago and is still being used to speed up log filtering (though the false positive rate makes it kind of ineffective now, an issue which would also be permanently solved by the structure proposed in this EIP).

---

**acolytec3** (2025-03-24):

Have been talking with [@jochem-brouwer](/u/jochem-brouwer) and we’re proposing to PFI this for Fusaka.  [@vbuterin](/u/vbuterin), any objection to me PR-ing the EIP to add myself as champion so we can try and push this forward?



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9524)














####


      `ethereum:master` ← `jochem-brouwer:bloom-filters-fusaka`




          opened 04:27PM - 24 Mar 25 UTC



          [![jochem-brouwer](https://avatars.githubusercontent.com/u/29359032?v=4)
            jochem-brouwer](https://github.com/jochem-brouwer)



          [+1
            -0](https://github.com/ethereum/EIPs/pull/9524/files)







Adds "remove bloom filters" https://eips.ethereum.org/EIPS/eip-7668 to PFI Fusak[…](https://github.com/ethereum/EIPs/pull/9524)a.












The idea being that since [eth/69 is already being proposed](https://github.com/ethereum/EIPs/pull/9237) to remove the bloom filter from the encoded receipts, we should go ahead and do the same across the entire protocol.

---

**etan-status** (2025-11-05):

Note that EIP-6466 also gets rid of the per-receipt logsBloom field, while providing other benefits such as provability of partial receipt data (tree hash, simplifies L2).

In the block header, one could choose to just replace the logsBloom with all-1’s, effectively turning it into a 100% false positive. That gets rid of the excess computation, while also maintaining backwards compatibility. Once we to EIP-7807, the field can be completely removed.


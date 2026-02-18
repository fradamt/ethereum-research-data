---
source: magicians
topic_id: 20428
title: Verkle implementers call #20, July 1 2024
author: abcoathup
date: "2024-07-02"
category: Protocol Calls & happenings
tags: [verkle]
url: https://ethereum-magicians.org/t/verkle-implementers-call-20-july-1-2024/20428
views: 486
likes: 0
posts_count: 1
---

# Verkle implementers call #20, July 1 2024

### Agenda

[Verkle Implementers Call #20 · Issue #1089 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1089)

2024-07-01T13:00:00Z

Moderator: [@rudolf](/u/rudolf)

### Notes

Notes by [@rudolf](/u/rudolf) *from [X](https://x.com/rudolf6_/status/1808790395394085224)*

#### 1. Team updates

Starting things off as usual with quick updates from the client teams:

[@jasoriatanishq](https://x.com/jasoriatanishq) for [@nethermindeth](https://x.com/nethermindeth): continuing testing the verkle sync implementation. Last week implemented the healing part. Anyone can now join the testnet using verkle sync.

[@gballet](/u/gballet) & [@ignaciohagopian](https://x.com/ignaciohagopian) for [@go_ethereum](https://x.com/go_ethereum): did a lot of work on the spec. Started implementation of EIP-4762. Still need to re-run the testing framework after it’s complete. Have also spent some time doing a new analysis of Verkle gas cost / code chunking using more recent mainnet transactions. Will be able to share this analysis soon.

[@kt2am1990](https://x.com/kt2am1990) for [@HyperledgerBesu](https://x.com/HyperledgerBesu): working on the flat DB refactor for Verkle. Also looking at how we can optimize to reduce the size of the db. Also some performance optimizations around preloading the trie node during block processing, so at the end of the block when have to compute the state root everything is already in memory.

[@techbro_ccoli](https://x.com/techbro_ccoli) for the testing team: we now have a successful test framework, and our first release is out. These are the simplest form of the transition tests (mid fork) where the test block starts on the fork transition block. For next steps: filling the “genesis test” (starting at the verkle fork) as opposed to during transition.

#### 2. EIP-7709 and EIP-2935 updates

There’s been a bit of pushback on how Verkle handles blockhash, and suggestion that we should copy the behavior of 4788. Going forward, EIP-2935 will behave the same way as 4788.

[@gballet](/u/gballet) has opened a PR: [https://github.com/ethereum/EIPs/pull/8698…](https://t.co/MoN8hxVfHQ).

#### 3. Testnet

For next testnet: we had a quick discussion on whether it should include deactivating EIP-158. There was no opposition to this on the call. Will also likely be some discussion around this topic of deactivating EIP-158 on this week’s ACD.

#### 4. The transition & preimage distribution

Gary from Besu team joined to share recent ideas and questions around the transition (migrating state from Merkle to Verkle) and preimage distribution.

Guillaume and Gary discussed that during the actual transition (which could take a month or more), clients will not be able to snap sync to latest. Only full sync will be possible. For a client syncing from scratch: they would do a snap sync up to the last Merkle Patricia Tree block, and then do a full sync from there. This seems like a reasonable approach since it would only take 2 hours or so to do a full sync in this case.

On the topic of preimage distribution and including the preimage keys in the execution witness: [@kt2am1990](https://x.com/kt2am1990) mentioned that if we can have the address/slot we are touching in each transaction, it might enable some parallelization when we want to import the block. Guillaume will be adding this in next round of spec updates. So we’ll know which are being touched in the tx. One potential downside though is that it will make the witness much larger. Guillaume to make the spec update and then continue discussion on this topic.

#### 5. Cost of extcodehash/extcodesize in EOF

Last up, there was some discussion around a few things where EOF differs from legacy code and potentially adds cost: extcodehash, extcodesize, delegatecall. For each of these 3: in addition to reading the code hash you also need to check this is an EOF format. So the question is can we put it directly in the header to avoid this?

[@shemnon](/u/shemnon) suggested this is a great use case for a flag. If the EOF flag is set, then extcodesize and extcodehash will go down the separate EOF path to signal its EOF code versus an empty account. Importantly this flag would avoid the need to read an extra chunk which would incur extra cost. If the flag is there, then don’t need to read the chunk.

---

That’s it for this week’s call..

Check out [http://verkle.info](https://t.co/gquxi5n9gU) or head over to the Eth R&D Discord ([verkle-trie-migration channel](https://discord.com/channels/595666850260713488/824798757618188339)) to stay up-to-date ! ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=15)

### Recording

https://www.youtube.com/watch?v=L873Z5K6XZQ

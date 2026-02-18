---
source: magicians
topic_id: 736
title: "Lightning Talks: solEVM for Off-Chain Computation Proofs by Johann Barbie"
author: johba
date: "2018-07-15"
category: Protocol Calls & happenings > Presentations
tags: []
url: https://ethereum-magicians.org/t/lightning-talks-solevm-for-off-chain-computation-proofs-by-johann-barbie/736
views: 1507
likes: 1
posts_count: 5
---

# Lightning Talks: solEVM for Off-Chain Computation Proofs by Johann Barbie

An initiative by [Decentraland](https://decentraland.org/), [Matic Network](https://matic.network/), and [Parsec Labs](https://parseclabs.org/) to extend [Andreas Olofsson’s solEVM](https://github.com/Ohalo-Ltd/solevm)  to run crypto-economic computation verifications games.

**Repository:** [github.com/parsec-labs/solevm-truffle](https://github.com/parsec-labs/solevm-truffle/)

**Discussions:** [discord channel](https://discord.gg/7bfD6eB).

**Regular calls:** every Monday at 13:00 UTC in [hangouts](https://hangouts.google.com/hangouts/_/calendar/ODJkajBpczc0NHJxNWd0MnAybjJmNTY5cWtAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ.6j7d7c6k2hgl8o3ka9oljcpk0g).

**Bounties:** on gitcoin: [1](https://gitcoin.co/issue/parsec-labs/solevm-truffle/1/778), [2](https://gitcoin.co/issue/parsec-labs/solevm-truffle/2/793), 3(tbd), 4(tbd), [architecture doc](https://github.com/parsec-labs/solevm-truffle/blob/master/docs/Architecture.md).

## Replies

**fubuloubu** (2018-07-15):

What are the similarities and differences with Truebit?

---

**johba** (2018-07-16):

Truebit uses Wasm to run code. That is perfect and very efficient for most off-chain computation.

Our choice to run EVM code is aimed at use-cases that specifically need to proof off-chain EVM computation, like smart contracts on Plasma chains.

---

**johba** (2018-07-16):

![:telephone_receiver:](https://ethereum-magicians.org/images/emoji/twitter/telephone_receiver.png?v=9) fyi, updates in the latest solEVM developer call: https://github.com/parsec-labs/solevm-truffle/wiki ![:telephone_receiver:](https://ethereum-magicians.org/images/emoji/twitter/telephone_receiver.png?v=9)

---

**johba** (2018-12-03):

we have set up a regular call and are making good progress here: [GitHub - leapdao/solEVM-enforcer: Partial implementation of the Ethereum runtime in Solidity (PoC)](https://github.com/leapdao/solEVM-enforcer)

![:telephone:](https://ethereum-magicians.org/images/emoji/twitter/telephone.png?v=9) **solEVM Implementers call** ![:telephone:](https://ethereum-magicians.org/images/emoji/twitter/telephone.png?v=9)

**when:** Wednesday 5. Dec 12pm UTC

**where:** https://hangouts.google.com/hangouts/_/calendar/ODJkajBpczc0NHJxNWd0MnAybjJmNTY5cWtAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ.5osho06ftccrdbdnlfh2dbgbo7

**what:** [solEVM Implementers Call - HackMD](https://hackmd.io/Kn0hwBA7Tvm6mfacCH1rIw?both)


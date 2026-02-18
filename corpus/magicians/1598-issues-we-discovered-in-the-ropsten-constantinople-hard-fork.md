---
source: magicians
topic_id: 1598
title: Issues we discovered in the Ropsten Constantinople hard fork
author: lrettig
date: "2018-10-17"
category: Magicians > Process Improvement
tags: [hardfork, testnet, ropsten]
url: https://ethereum-magicians.org/t/issues-we-discovered-in-the-ropsten-constantinople-hard-fork/1598
views: 7429
likes: 22
posts_count: 10
---

# Issues we discovered in the Ropsten Constantinople hard fork

Here’s my initial post-mortem and concern/task list following the Constantinople Ropsten hard fork, in no particular order.

1. A consensus bug in Parity was discovered (https://github.com/paritytech/parity-ethereum/pull/9746). We need to understand why this consensus bug occurred in the first place, and particularly why it wasn’t caught by the tests. @ethchris suggests that we may need clearer EIP specs including pseudo code (https://twitter.com/ethchris/status/1052503731072315392). Apparently in this case there was some confusion over the meaning of terms like “transaction” and “execution frame” that may have contributed to the bug (cf. ethereum/AllCoreDevs - Gitter).
2. There were no miners on the new fork. Why? We need to better understand, and have more control over, how mining happens on a PoW testnet. Does the Foundation/Parity/other core dev teams need to have more miners running on a PoW testnet? Do we need to have miners on standby, fully synced, ready to jump on after a fork and assert the correct chain? Do we need to enlist the help of altrustic miners like @atlanticcrypto in this effort? How do we coordinate?
3. Parity has a limit on how far back nodes can automatically reorg (cf. @5chdn at ethereum/AllCoreDevs - Gitter). We should better understand this mechanism. Is this supposed to be a limit on “on chain governance” (allowing nodes to automatically come to consensus on the canonical chain) that triggers the need for meatspace/developer intervention? Or is it more about resource constraints? What’s the limit and why is it set as such? Why does parity have this limit, but not geth? UPDATE: it appears that both geth and parity have such a limit.
4. Geth has a debug.setHead command that allows you to manually force it onto the right chain; it appears that parity does not have such a feature. Is this desirable?
5. It’s possible for an upgraded node in fast sync mode (geth or parity, I believe) to fast sync over a bad block which caused a fork and keep following the wrong chain. This is clearly the shortcoming for fast sync but we should discuss this in the context of forks and long reorgs - is there some way to communicate a hint to such nodes that they’re on the wrong chain?
6. Similarly, after a fork has occurred and there are many chains (there appear to be as many as four Ropsten chains right now, cf. ethereum/AllCoreDevs - Gitter), it’s very difficult for a node sycning from scratch to find the right chain. For one thing, it constantly tries to peer with nodes on the wrong chain; in this case it was necessary for nodes to turn off discovery entirely and manually enter a set of peers to get caught up to the right chain. Perhaps a “fork ID” as suggested by @MicahZoltu would help. Alternatively, some sort of “beacon” (not to be confused with the Eth 2.0 beacon chain, sorry for the poor choice of terms) which gave nodes a verifiable hint about the current canonical chain would help (or, alternatively, a blacklist of bad blocks or chains). Some challenges here: @cdetrio points out that the P2P layer makes transmitting this information hard (ethereum/AllCoreDevs - Gitter), there’s the question of centralization here (who controls the beacon?), and it’s a possible DoS vector in the wrong hands.
7. Communication - the AllCoreDevs channel on Gitter served as our primary means of communication throughout this fork - but it’s disorganized, has no threading, and it’s difficult to find a canonical source of information (e.g., which is the current head? what’s the current block number? what’s the status of each client? what series of commands do I need to run to sync a new node to the current head? etc.). I propose the creation of a core devs “War Room” where this information can be managed going into and during an upgrade or other emergent situation. Hudson set this up, which is a great example:  https://notes.ethereum.org/s/SJE9O2ksQ#
8. General hard fork strategy - the core devs seem to be all over the map here. @AlexeyAkhunov argues that we should roll Ropsten back to Constantinople and try the fork again. @sorpaas disagrees. Is there a minimum amount of time we need between finalizing/releasing the client code and scheduling a hard fork? Can we make sure that hard forks happen on Wednesdays rather than on Saturdays? Do we need a certain set of people to be “on call” for the fork? Is there a minimum amount of time we need to see an upgrade running successfully on a testnet before we schedule a mainnet hard fork? Which testnet? Does it need to be an “active”, PoW-based testnet like Ropsten? Do we need some escape hatch, e.g., we could send a transaction to call off or postpone a testnet hard fork if a bug is discovered?
9. Fork monitor - apparently @Arachnid and @cdetrio worked on this before. This might be something like a modified version of EthStats. We would definitely find this useful for the #Ewasm testnet. Would this be of value?
10. There’s an issue in geth where it spends a lot of resources exploring chains with bad blocks that appear to have a higher TD (cf ethereum/AllCoreDevs - Gitter). According to @holiman, it may explore the same chain or same set of blocks multiple times, esp. when it’s not running in archive mode (and thus doesn’t retain all the block data). We may need some efficient way for geth to remember bad ancestors to prevent this issue (ethereum/AllCoreDevs - Gitter).
11. Ropsten has effectively been unusable, or at least very difficult to use, for about four days as of this writing, and we still have several active forks. This begs the question, what is a testnet? What is its purpose?  Do we need stable, “production” testnets and “staging” testnets? @LefterisJP probably has thoughts here

## Replies

**lrettig** (2018-10-17):

Response from [@sorpaas](/u/sorpaas) on Gitter (https://gitter.im/ethereum/AllCoreDevs?at=5bc75431069fca52a54eb783):

> Apparently in this case there was some confusion over the meaning of terms like “transaction” and “execution frame” that may have contributed to the bug.

No that’s not the case. “transaction” and “execution frame” are all clearly defined. That discussion was where [@AlexeyAkhunov](/u/alexeyakhunov) worried that parity did it incorrectly but later turned out to be a false flag. The real issue is whether refund counter is signed. I agree pseudo code may be helpful, but it probably won’t catch this bug efficiently either, because different client uses different method for refund checkpointing. Probably this should really just be a section in EIP that says “implementators please pay attention to those cases”. We still need to find better ways to catch it before bug happens, though.

> Geth has a debug.setHead command that allows you to manually force it onto the right chain; it appears that parity does not have such a feature. Is this desirable?

Yes, we have a feature request for that! It’s just not yet implemented: [Allow to reset the chain to a particular block · Issue #8259 · openethereum/parity-ethereum · GitHub](https://github.com/paritytech/parity-ethereum/issues/8259)

---

**holiman** (2018-10-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> We need to understand why this consensus bug occurred in the first place, and particularly why it wasn’t caught by the tests.

The manually written tests were not complete, something which [@winsvega](/u/winsvega) clearly stated during the calls. Let no shadow fall on him.

However, during two publically aired coredev-calls, we agreed that Ropsten was a testnet, and that we considered it ok to use it as such. Not until right as we were about to release fork-enabled clients did we hear from developers who wanted Ropsten to not suffer from disturbances.

The decision to deploy on Ropsten was imo made because we knew it would be a good testnet, and it should have as long exposure on Ropsten as possible before a mainnet release.

That being said, it’s not true that we didn’t test it. We had fuzzers running for a couple of weeks, but unfortunately the fuzzer engine was not properly tuned, and did not get good coverage of the SSTORE logic. Now, after [@cdetrio](/u/cdetrio) made some [tuning](https://github.com/ethereum/evmlab/pull/89) to it, he caught the bug within 800 testcase (a couple of minutes).  I deployed the new code this morning, and it has, since then, run 196k testcases where it tests Gets vs Parity. It will continue to run 24/7, and we will also deploy a new instance which has a different testcase generation strategy.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Geth has a debug.setHead command that allows you to manually force it onto the right chain; it appears that parity does not have such a feature. Is this desirable?

That command is not quite safe. It’s in the `debug` namespace because it blindly changes internals without bothering about consistency. Things may break. If you have fast-synced and does a `setHead` to before your pivot block, I have no idea what will happen. In the best-case, nothing.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Similarly, after a fork has occurred and there are many chains (there appear to be as many as four Ropsten chains right now

That we don’t know. We don’t have enough visibility to see that, but could fairly easily check if the head block for the ones further back is in the chain of the ones further ahead.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> I propose the creation of a core devs “War Room” where this information can be managed going into and during an upgrade or other emergent situation.

Well, that’ll be just another channel. If there’s a need for a *real* war-room, it may not be something we want to have publically.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Fork monitor - apparently @Arachnid and @cdetrio worked on this before. This might be something like a modified version of EthStats. We would definitely find this useful for the ewasm testnet. Would this be of value?

It exists, it’s a d3js-vizualisation of the chains, and has been used for all forks since the dao-fork, IIRC. Nobody set it up for Ropsten constantinople fork, however, which in hindsight was a mistake.

I have tagged up some tickets/prs for geth that has come out of this excercise: [Issues · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/labels/ropsten-lessons)

---

**atlanticcrypto** (2018-10-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> There were no miners on the new fork. Why? We need to better understand, and have more control over, how mining happens on a PoW testnet. Does the Foundation/Parity/other core dev teams need to have more miners running on a PoW testnet? Do we need to have miners on standby, fully synced, ready to jump on after a fork and assert the correct chain? Do we need to enlist the help of altrustic miners like @atlanticcrypto in this effort? How do we coordinate?

We are comfortable making a commitment to support the current or future testnets in some capacity on an ongoing basis. We believe a base level of miner commitment to the test networks is important, and we are willing to provide it. We would hope that as new testnet forks are planned we could be included in conversations regarding the infrastructure rollout timing and requirements on the core dev side.

---

**lrettig** (2018-10-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> I propose the creation of a core devs “War Room” where this information can be managed going into and during an upgrade or other emergent situation.

Well, that’ll be just another channel. If there’s a need for a *real* war-room, it may not be something we want to have publically.

I’m talking less about a channel for synchronous communication and more about a “fact set” along the lines of the things I outlined:

> which is the current head? what’s the current block number? what’s the status of each client? what series of commands do I need to run to sync a new node to the current head?

I don’t have a strong opinion about its being public or private. There are some scenarios, like a real attack, where I imagine we’d want some degree of privacy, but all of the dialog and information regarding the Ropsten fork was carried out in public without issue.

---

**Hex-Capital** (2018-10-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> It’s possible for an upgraded node in fast sync mode (geth or parity, I believe) to fast sync over a bad block which caused a fork and keep following the wrong chain. This is clearly the shortcoming for fast sync but we should discuss this in the context of forks and long reorgs - is there some way to communicate a hint to such nodes that they’re on the wrong chain?

I think #5 above is super important. Shortly after the fork, I believe we ended up with 3 main chains:

- Byzantium (from unupgraded mining nodes)
- Constantinople-Geth
- Constantinople-Parity (which split from Geth at 4230605)

However, because an upgraded fast node can fast sync over a bad block, even more chains were produced as people tried to resync. E.g. A Geth node fast synced to the Constantinople-Parity chain **past 4230605** and then forked off at the next bad block. This could generate an infinite number of chains

---

**Cygnusfear** (2018-10-18):

re #7 I have been lurking the AllCoreDevs channel and I would like to add support for creating an open ‘war room’. Private channels are easily opened when necessary, if the channels are private to begin with there will be no ‘good samaritans’ contributing to the issue (spinning up an extra miner/node etc). As [@lrettig](/u/lrettig) proposed in the excellent summary of issues: threading would definitely help organising the large amount of information, stickying threads with helpful information solves the canonical truth issue.

This is, altogether with #2 & #8 highlighting the amount of  coordination between different actors in preparation for a fork. Finding the proper channel is easier with a designated communication channel for parties involved. With the amount of upcoming clients for Eth2 and thus more participants the necessity for this will probably increase. Setting up a ‘war room’ (additionally a fork monitor?) could probably be sponsored and initiated by several parties as a bounty (EF, Parity, upcoming clients) if legitimacy is an issue.

Edit: Aragon is using rocket.chat, which has a lot of feature parity with Slack (https://github.com/aragon/governance/blob/master/AGP-5_Migration_to_Open_Source_Messaging_Platform.md & https://rocket.chat)

---

**5chdn** (2018-10-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> The manually written tests were not complete, something which @winsvega clearly stated during the calls. Let no shadow fall on him.

This is an important point. I would like to add that we all agreed that “this is fine” for a testnet. Curious about testing updates on Friday.

---

**tjayrush** (2018-10-19):

May I suggest some sort of “disaster recovery” planning? Of course, it’s all super-complicated and extremely difficult, but if there was some pre-planning for unexpected outcomes that might be good. (Simple suggestion: a pre-determined place to get information (wiki) that has been loudly announced prior to the fork.)

I know this problem was only on the testnet, but one of the concerning aspects of the recent episode is the apparent ad-hoc nature of the recovery.

I hope no-one thinks I’m being critical, because I’m not intending to be. I’m just making a suggestion.

---

**lrettig** (2018-10-20):

Thanks for chiming in [@tjayrush](/u/tjayrush). A lot of my ideas, including the above, are indeed inspired by disaster recovery training from my days working in finance. I think there’s a lot we can learn from these best practices.


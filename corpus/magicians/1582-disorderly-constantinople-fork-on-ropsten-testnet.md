---
source: magicians
topic_id: 1582
title: Disorderly Constantinople fork on Ropsten testnet
author: jpitts
date: "2018-10-14"
category: Working Groups > Signaling Ring
tags: [forks, ropsten]
url: https://ethereum-magicians.org/t/disorderly-constantinople-fork-on-ropsten-testnet/1582
views: 2121
likes: 12
posts_count: 9
---

# Disorderly Constantinople fork on Ropsten testnet

This case brings up interesting developer coordination issues and illustrates the importance of a well-defined testing process as client developers prepare to implement changes affecting mainnet.

In this planned activation of changes on Ropsten testnet, when the forking block was reached, there was not enough mining power from Ropsten clients implementing Constantinpole changes. This led to a disorderly forking in which the intended upgraded network failed to quickly materialize / become dominant.

Additionally, a consensus bug was found, leading to a secondary fork (a more dire state of affairs which must be avoided at all costs on mainnet).

The result is that the Ropsten network, for lack of a better word, is shattered.

https://twitter.com/jutta_steiner/status/1051371111345197057

The situation is currently being discussed, investigated, and resolved in the [AllCoreDevs gitter channel](https://gitter.im/ethereum/AllCoreDevs?at=5bc38d67c08b8b3067143fd0).

## Replies

**tay** (2018-10-15):

Can someone make a note in the future to do the math on forks so they happpen during the week instead of Saturday. ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**jpitts** (2018-10-15):

[@lrettig](/u/lrettig) [tweeted](https://twitter.com/lrettig/status/1051624092388986885) about the identification of the consensus bug by several community devs in the [AllCoreDevs gitter channel](https://gitter.im/ethereum/AllCoreDevs?at=5bc3d2a2271506518d121ab9).

https://gitter.im/ethereum/AllCoreDevs?at=5bc3d2a2271506518d121ab9

---

**MicahZoltu** (2018-10-17):

Is there a reason we don’t have fork identifiers?  I really dislike that we are beholden to miners to upgrade to a fork.  As a user, if I want to participate in a hard fork I should be able to do so even with none of the miners switching their work over.  I believe at the moment Ethereum clients are designed such that they will follow the heaviest chain of either the old code or the new code, which means miners *must* upgrade in order for me to upgrade.  At some point, there may be a change that miners don’t voluntarily upgrade to but all economic participants do upgrade to.  In this scenario the majority of miners should not be able to prevent my client from switching to the fork.

It sounds like this is effectively what happened with Ropsten, and it feels like can be simply fixed by including a fork identifier in the block headers such that my client will ignore any blocks that are not part of my desired fork.

---

**jpitts** (2018-10-17):

Linking here to a related discussion, this is retrospectives / post-mortems:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png)
    [Issues we discovered in the Ropsten Constantinople hard fork](https://ethereum-magicians.org/t/issues-we-discovered-in-the-ropsten-constantinople-hard-fork/1598) [Process Improvement](/c/process-improvement/6)



> Here’s my initial post-mortem and concern/task list following the Constantinople Ropsten hard fork, in no particular order.
>
>
> A consensus bug in Parity was discovered (https://github.com/paritytech/parity-ethereum/pull/9746). We need to understand why this consensus bug occurred in the first place, and particularly why it wasn’t caught by the tests. @ethchris suggests that we may need clearer EIP specs including pseudo code (https://twitter.com/ethchris/status/1052503731072315392). Apparently i…

---

**5chdn** (2018-10-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tay/48/347_2.png) tay:

> Can someone make a note in the future to do the math on forks so they happpen during the week instead of Saturday.

That’s exactly what we did, from what I understand, but people kept adding hashrate to the network and therefore the hardfork happened earlier than initially planned.

The underlying issue here: block numbers are unreliable and there is a two-in-seven chance that a block evetually appears on a weekend.

There are ideas discussed about using contracts to signal hard-forks (bad) or simply using timestamps (ugly), but I have not yet seen any solution that convinced me.

---

**MicahZoltu** (2018-10-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5chdn/48/1242_2.png) 5chdn:

> simply using timestamps (ugly)

Why do you find using timestamps to hard fork as “ugly”?  Is it just because the way the Parity codebase is currently designed makes using timestamps hard?  If so, this is a reasonable argument for not doing it, but I think it is valuable to be clear that the problem isn’t with timestamps generally, it is with the way Geth/Parity/Harmony are currently authored.

That is, if one were to be authoring a blockchain from scratch today, using timestamps (IMO) for fork scheduling would be the right solution (no legacy baggage).

---

**tjayrush** (2018-11-04):

I too would like to understand why ‘timestamps are ugly.’ It seems obvious to me.

---

**5chdn** (2018-11-26):

Because miners control timestamps and there is a variance allowed how to set them, so you can not for sure tell which miner at which point decides that Constantinople activates at a certain block.

Also, all clients are built around block numbers, so this is not only a Parity Ethereum thing: all clients would need some basic refactoring to allow for time stamps.


---
source: magicians
topic_id: 16188
title: "EIP-7542: eth/70 - available-blocks-extended protocol"
author: smartprogrammer
date: "2023-10-21"
category: EIPs > EIPs networking
tags: [devp2p]
url: https://ethereum-magicians.org/t/eip-7542-eth-70-available-blocks-extended-protocol/16188
views: 4458
likes: 18
posts_count: 12
---

# EIP-7542: eth/70 - available-blocks-extended protocol

Discussion thread for [EIP-7542: eth/70 - available-blocks-extended protocol](https://eips.ethereum.org/EIPS/eip-7542)

## Replies

**matt** (2023-10-22):

I think this proposal is problematic because it allows a heterogeneous distribution of block data across clients. The rational node operator will only maintain the minimum amount of historical data. Therefore, we can expect the vast majority of the network to not provide any substantial amount of the history. To find nodes that do will require a long period of searching the discovery network and then the nodes that do serve most or all of the history will be fully saturated by those looking for it.

This is a solution that I feel avoids the problem of making all historical data highly accessible to nodes. My proposed solution has been to implement the [era and era1 format](https://github.com/ethereum/go-ethereum/pull/26621) in ELs and bring many different history distribution mechanisms online (e.g. bittorent, direct download, portal network, etc), while retaining the property that all nodes on the network have the same historical data, albeit a smaller amount, such as only 1 year or 3 months worth.

---

**smartprogrammer** (2023-10-22):

I will have to disagree with you on this for several points:

- Multiple clients already have an implementation for configuration that does not hold the entire history just like in

Nethermind’s bodies and receipts barriers
- Besu’s checkpoint sync

Declaring what block range is available does not force client implementers to start to prune blocks. It just adds the benefits of knowing which peers have the blocks I need instead of sending requests and getting empty responses.
**Assuming** the vast majority of the network will stop providing substantial amount of history, then expect the vast majority of new nodes will not be asking for such history in the first place. Thus, such a saturation would never happen.
As for Era1:

- You mentioned Geth is already working on Era1 export: https://github.com/ethereum/go-ethereum/pull/26621
- Nethermind is working on the same Era1 export and import here: ERA history import/export start by ak88 · Pull Request #6173 · NethermindEth/nethermind · GitHub

Portal network already provides the ability to download premerge historical blocks from the [Execution Chain History Network](https://github.com/ethereum/portal-network-specs/blob/master/history-network.md) and the beacon chain has the block history post merge.

P.S, I am not saying Era1 or Portal are ready solutions. But the EIP does not say start pruning blocks either. It just optimizes the sync operation in the devp2p network.

---

**karalabe** (2023-10-22):

This is a horrible idea. The fact that Nethermind and Besu already stopped serving historical data is in itself an epic fail towards the network and a shameful decision to be honest. If you ask me, pruning past data is a blatant marketing trick to get people to switch to the respective clients. It is absolutely horribly bad for the network, it is a protocol violation, it goes against the entire design of Ethereum.

---

**holiman** (2023-10-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/smartprogrammer/48/10774_2.png) smartprogrammer:

> I am not saying Era1 or Portal are ready solutions.

Until they are, then we should not optimize for behaviour where the history of ethereum is optimized off as “Someone Elses Problem” (== geth’s problem?). I agree with [@matt](/u/matt) and [@karalabe](/u/karalabe) .

---

**holiman** (2023-10-22):

I looked through the meeting-notes from [Execution Layer P2P Breakout #3 · Issue #858 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/858#issuecomment-1708403774)

> discussed another concern from @holgerd77 that nodes could start disconnecting peers that do not have the block range they need. This would result in the nodes possibly trying to sync being disconnected since they dont have the needed range by others.

> This can be addressed in the EIP by explicitly mentioning that nodes must not disconnect peers that do not have the range they need.

So, in essence, you would “mandate” that “the behaviour of forgetting old blocks” must not be punished by non-forgetful peers? I mean, it does make sense from one point of view, I guess…

---

**smartprogrammer** (2023-10-22):

I will amend it to reflect that it goes besides 4444 not before it. It is worth noting that implementing this EIP will benefit the nodes trying to sync the full chain the most as they will not need to ask for blocks other peers might not have and get an empty response for them.

Appreciate the feedback ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

---

**smartprogrammer** (2023-10-22):

Ah, i see what you mean here. this was so we dont punish nodes that are still syncing, it was not meant for nodes that do not have the full history.

---

**smartprogrammer** (2023-10-22):

If you look at it in the context of being implemented along side 4444, the mandate will then actually do what it was intended to do.

---

**mohsenghajar** (2023-10-22):

Anything that contributes to monopolization of historical data is wrong. Even morally.

---

**smartprogrammer** (2023-10-22):

How do you feel this EIP contributes to monopolization of historical data?

---

**smartprogrammer** (2023-10-23):

I have updated the PR to reflect its alignment with 4444. I would appreciate if you could take a second look at it here:

https://github.com/ethereum/EIPs/pull/7906

[@matt](/u/matt) [@karalabe](/u/karalabe) [@holiman](/u/holiman)

Feel free to give any feedback ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=15)


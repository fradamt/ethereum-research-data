---
source: magicians
topic_id: 6706
title: "EIP-3675: Upgrade consensus to Proof-of-Stake"
author: mkalinin
date: "2021-07-22"
category: EIPs > EIPs core
tags: [consensus-layer, eth1-eth2-merge]
url: https://ethereum-magicians.org/t/eip-3675-upgrade-consensus-to-proof-of-stake/6706
views: 53809
likes: 7
posts_count: 8
---

# EIP-3675: Upgrade consensus to Proof-of-Stake

This is the discussion topic for EIP-3675: Upgrade consensus to Proof-of-Stake.

This EIP introduces the specification of the consensus mechanism upgrade to the Proof-of-Stake (a.k.a. The Merge).

Edit

EIP-3675 got merged you can find it here:



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3675)





###



Specification of the consensus mechanism upgrade on Ethereum Mainnet that introduces Proof-of-Stake

## Replies

**mkalinin** (2021-07-30):

For the health of the network under [this kind of attack](https://github.com/ethereum/EIPs/pull/3675#discussion_r679207367) it makes sense for clients to stop propagating *any* blocks upon receiving the first `POS_BLOCK_FINALIZED` and remove handlers with the corresponding penalty upon receiving the second `POS_BLOCK_FINALIZED`. So, the updated spec should look like:

> The networking stack SHOULD NOT send the following messages if they advertise the descendant of any terminal PoW block:
>
>
> NewBlockHashes (0x01)
> NewBlock (0x07)
>
>
> Beginning with the first POS_BLOCK_FINALIZED event, the networking stack MUST discard the following ingress messages:
>
>
> NewBlockHashes (0x01)
> NewBlock (0x07)
>
>
> Beginning with the second POS_BLOCK_FINALIZED event, the networking stack MUST remove the handlers corresponding to the following messages:
>
>
> NewBlockHashes (0x01)
> NewBlock (0x07)
>
>
> Peers that keep sending these messages after the handlers have been removed SHOULD be disconnected.

According to the current spec honest peers that keep propagating maliciously produced terminal PoW blocks maybe accidentally disconnected because of the racing in receiving the `POS_BLOCK_FINALIZED` event by between different nodes.

cc [@MicahZoltu](/u/micahzoltu)

---

**wjmelements** (2021-07-30):

If you fork out PoW using TD instead of block number, miners will be incentivized to maximize the number of blocks until that TD, and the easiest way to do that would be a MASF that adjusts tip selection. While some clients will still use TD, the majority hashpower would not, and the reorgs would be chaotic. I’ve suggested they use min(NEXT_BASE_FEE) for tip selection, and with 1559 that may be an easier, more profitable way to break ties than TD. Using TD for PoS timing would make collusion against TD more beneficial.

---

**wjmelements** (2021-07-30):

Another concern with TD is that an increase or decrease in MEV given liquid hashrate may make TD less predictable than block number; if the hashrate increased the fork could happen sooner than expected. This would require a later fork date than if block number was used, to account for possible variability.

---

**MicahZoltu** (2021-07-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> If you fork out PoW using TD instead of block number, miners will be incentivized to maximize the number of blocks until that TD, and the easiest way to do that would be a MASF that adjusts tip selection. While some clients will still use TD, the majority hashpower would not, and the reorgs would be chaotic. I’ve suggested they use min(NEXT_BASE_FEE) for tip selection, and with 1559 that may be an easier, more profitable way to break ties than TD. Using TD for PoS timing would make collusion against TD more beneficial.

We have discussed this vector previously, and at least it requires a 51% attack by miners (effectively) where it is profitable to defect *up until 51% is reached*.  This is not really any different than our current situation, where a 51% attack is viable but it is profitable to defect up until 51% is actually reached.  The problems introduced by using block number create new attack vectors beyond 51% attacks, which is why TD was chosen instead.

I recommend checking out [EIP-3675: Upgrade consensus to Proof-of-Stake](https://eips.ethereum.org/EIPS/eip-3675#terminal-total-difficulty-vs-block-number) for details on the problems with using the block number.

---

**poojaranjan** (2021-08-02):

A high-level introduction of the system after the merge, terminal total difficulty, transition block diagram, and more are explained on the [PEEPanEIP](https://www.youtube.com/playlist?list=PL4cwHXAawZxqu0PKKyMzG_3BJV_xZTi1F) with [@mkalinin](/u/mkalinin).

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/6/64cf3fe4c73434071731f7e9839c0b323f4ec426.jpeg)](https://www.youtube.com/watch?v=zNIrIninMgg)

---

**mkalinin** (2021-11-11):

[EIP-2124 fork identifier](https://eips.ethereum.org/EIPS/eip-3675#eip-2124-fork-identifier) section in the specification currently has the following statement:

> Starting with TRANSITION_POS_BLOCK that has block number N, nodes MUST update FORK_HASH by appending uint64(N) to the sequence of hashes used to calculate FORK_HASH as per EIP-2124.
> FORK_NEXT can remain 0 after the transition.

Suppose the local node is syncing and haven’t reached the `TRANSITION_POS_BLOCK` yet while the transition has already happened in the network and the `TRANSITION_POS_BLOCK` is known to the remote peer the node tries to connect to. The remote peer has updated its `FORK_HASH` with `TRANSITION_POS_BLOCK` according to the aforementioned statement, and, thus, local node will disconnect the peer because of incompatible `FORK_HASH` values.

A straightforward way to prevent the network from falling apart because of uncertainty around `TRANSITION_POS_BLOCK` is to keep `FORK_HASH` unaffected by the Merge. The question is: can and should we do better?

---

**mkalinin** (2021-11-23):

Continuing on the EIP-2124 topic.

There was a suggestion made by [@djrtwo](/u/djrtwo) on [ACD#126](https://github.com/ethereum/pm/issues/407) to set the `FORK_NEXT` to a block height lower, e.g. by a week worth of block numbers, than the height of `TRANSITION_BLOCK`. This would force those users that haven’t upgraded their client software yet to do so because they will start loosing peers. In the case if TTD override with the value that is closer in time, the `FORK_NEXT` value could be overridden as well for the same purposes. This behaviour around `FORK_NEXT` looks pretty valuable in the context of the Merge.


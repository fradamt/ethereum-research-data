---
source: ethresearch
topic_id: 6265
title: The eth1 -> eth2 transition
author: vbuterin
date: "2019-10-10"
category: The Merge
tags: []
url: https://ethresear.ch/t/the-eth1-eth2-transition/6265
views: 33262
likes: 30
posts_count: 30
---

# The eth1 -> eth2 transition

### TLDR: the user experience

If you are an application developer or a user, and the roadmap described in this post is used to complete the eth1 → eth2 transition, the changes and disruptions that you experience will actually be quite limited. Existing applications will keep running with no change. All account balances, contract code and contract storage (this includes ERC20 balances, active CDPs, etc etc) will carry over.

What you **will** have to deal with is the following:

1. Gas cost of IO-accessing opcodes (SLOAD, BALANCE, EXT*, CALL*) will increase. Gas cost of CALL will likely add a gas cost something like 1 gas per byte of code accessed.
2. At some point, you will have to download code that implements the network upgrade. This is fundamentally not different from any other upgrade, eg. Byzantium, Constantinople, but it’s a little bigger download because you’ll need to get an eth2 client if you do not already have one.
3. The chain will likely halt for ~1 hour. After 1 hour, it will look like “Ethereum” is back online, except at that point eth1 would be functioning as a subsystem inside eth2 instead of being a standalone system.

That’s it. **If you are a developer, you can eliminate the largest part of disruption from gas cost changes by proactively making sure you don’t write apps with high witness sizes, ie. measure the total storage slots + contracts + contract code accessed in one transaction and make sure it’s not too high.**

### How the transition may happen

Suppose that phases 0-2 have happened, and the eth2 chain is stably running. The eth1 chain continues to stably run as well. In the phase 0 spec, there already exists a mechanism, [eth1_data voting](https://github.com/ethereum/eth2.0-specs/blob/fffdb247081b184a0f6c31b52bd35eacf3970021/specs/core/0_beacon-chain.md#eth1-data), in which validators vote to agree on a recent canonical eth1 hash; this mechanism is used to process deposits. We will simply repurpose this mechanism to feed the full state (root) of eth1 into eth2.

Currently, this mechanism has a ~6 hour delay (4 hours from the ETH1_FOLLOW_DISTANCE + 2 hours from the voting period), but these parameters could be reduced over time before the transition to make the delay ~1 hour.

The basic mechanism to effect the transition is as follows:

[![Transition(1)](https://ethresear.ch/uploads/default/optimized/2X/c/cb1b0cb34db05b9cb8370d3da9dc623bdd9ed17f_2_690x195.png)Transition(1)1088×309 19.5 KB](https://ethresear.ch/uploads/default/cb1b0cb34db05b9cb8370d3da9dc623bdd9ed17f)

1. Specify a (eth1-side) height TRANSITION_HEIGHT. The TRANSITION_HEIGHT’th eth1 block will be considered the “final” block on the eth1 side; from then on, the “canonical” eth1 will be functioning as a subsystem of eth2.
2. In line with (1), add a change to the eth2 “honest validator” code that disallows voting for eth1 blocks with number > TRANSITION_HEIGHT. If the voting algorithm would have previously selected some block with number > TRANSITION_HEIGHT, vote for its ancestor at number TRANSITION_HEIGHT instead.
3. Additionally, in the case were (2) is triggered, validators should set the deposit_count to 2**63 higher than its true value (this is basically using the top bit of the deposit_count as a flag saying “eth1 is finished”)
4. When the eth2 chain accepts an eth1data with the “eth1 is finished” flag turned on, it performs a one-time “irregular state change” that puts the post-state root of that eth1 block into the state of an “eth1 execution environment” (a type of system-level smart contract on eth2). An amount of ETH equal to the total supply of ETH on the eth1 side is added to this eth1 EE’s balance.

After this point, the transition is complete. The eth1 chain technically continues but it is valueless; eventually it will die off when the difficulty ice age hits.

The eth1 system now lives inside of eth2; hence, further transitions to the eth1 system happen by submitting a transaction on eth2 which targets the eth1 EE (which as mentioned above is a subsystem of eth2). The eth1 EE has code that implements the entire eth1 EVM and transaction processing logic; it has a function `update(state_root, transaction, witness) -> new_state_root` which takes a transaction and witness (Merkle proofs of portions of the state), processes the transaction and determines the updated eth1 state root, according to the same rules as on the eth1 chain. See [The Stateless Client Concept](https://ethresear.ch/t/the-stateless-client-concept/172) for how witnesses and state roots work.

Additional functionality would be added into the eth1 EE code that allows ETH and messages to be withdrawn from the eth1 EE into other parts of eth2, and into copies of the eth1 EE on other shards. By default, all eth1 accounts/contracts would be placed on the same shard, so to take advantage of eth2’s increased capacity you would need to proactively use this functionality to move your ETH or other applications into other shards, but this would not be difficult. An extension to the ERC20 standard would need to be made to support cross-shard transfers of tokens.

### How the user client would work

The user-facing side of the client would be modified before the transition to have two code paths. The client would check eth2 to see if the transition has already happened. If it has not yet happened, then it would send transactions, check balances, etc using eth1 as before, except it would pretend that all eth1 blocks with `number > TRANSITION_HEIGHT` do not exist. If the transition has happened, it would look into the eth1 EE on eth2. A full client would process all transactions targeting the eth1 EE on eth2 sequentially, so as to continue updating the full eth1 state tree; this would allow the client to generate witnesses for any transaction they want to send and “package” it in the eth2 format. Light clients (as well as wallets such as metamask) would broadcast their transactions to a full client that could add witnesses for them.

**From a user’s point of view, ethereum would “feel” the same pre- and post-transition (except that post-transition it would feel smoother due to PoS and EIP 1559). Very different code paths would be used to package and broadcast the transaction, but the functionality provided would be the same.**

Potentially, the transition could even be engineered so that wallets that talk to clients via RPC do not need to change anything at all.

### Example user story

You have a CDP on MakerDAO. You go to sleep, and when you wake up the transition has happened. You are able to interact with and liquidate your CDP by sending transactions as before, except your client code would see that you are post-transition and add witness data to your transaction and send it to the eth2 network instead of the eth1 network.

### Possible optimizations

During the period between the eth1 chain reaching `TRANSITION_HEIGHT` and the eth1 EE on eth2 being fed with that state, we could do some preprocessing on the eth1 state. Particularly, we could:

- Replace the hexary Patricia tree with a binary sparse Merkle tree and a specialized hash function to ensure the hash overhead of branches remains O(log(n)). This reduces the size of Merkle branches by ~4x
- Replace RLP with SSZ hash trees
- Add state rent-related data fields to accounts
- Clear out “dust” accounts
- Modify account structure in line with abstraction proposals

Instead of including the actual eth1 state root into the EE, we would include the root of the state tree generated by performing all of these modifications. This is a deterministic calculation, so all validators could do it in parallel. This one-time expenditure of computation could greatly improve the efficiency and usability of eth1 post-transition.

## Replies

**eminogrande** (2019-10-10):

Interesting process. Is there any poll online (or statements) from the Ethereum community that shows consensus with that path / strategy? Will there be some sort of signaling or human get-together beside Devcon or is it rather a top down decision by a few experts in the core team?

Best regards

Emin

---

**MaverickChow** (2019-10-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> After this point, the transition is complete. The eth1 chain technically continues but it is valueless; eventually it will die off when the difficulty ice age hits.

As a person that does not write smart contracts and just hold ETH with the anticipation that it may someday be used as currency for daily economic uses, what are the things that I should do and when is the best time to do them after everything is said and done before the ice age hits, post-eth1?

For example, will I need to generate a new address based on eth2 chain and make a transfer of all my ETH from eth1 chain’s address to this new eth2 chain’s address?

---

**vbuterin** (2019-10-10):

> For example, will I need to generate a new address based on eth2 chain and make a transfer of all my ETH from eth1 chain’s address to this new eth2 chain’s address?

You don’t need to do this. If you want to take advantage of the benefits of eth2, you may want to move your funds into a wallet that supports other eth2-based functionality eventually, but you do not strictly have to and there is no time limit.

---

**Rbchi1** (2019-10-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If the voting algorithm would have previously selected some block with number > TRANSITION_HEIGHT , vote for its ancestor at number TRANSITION_HEIGHT instead.

I can’t understand it.What is voting for its ancestor at number `TRANSITION_HEIGHT` .

What is ancestor mean?

---

**vbuterin** (2019-10-11):

“Ancestor” means an earlier block in the same chain.

---

**Rbchi1** (2019-10-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> means an earlier block in the same chai

Many thanks for replying.

So it is like when vote algorithm selected 1001(1000 is the specified block height ),it would be back to 001?

---

**vbuterin** (2019-10-11):

No, if the vote algorithm would have selected block 1001, it instead selects its direct parent, whose block number is 1000.

---

**Weth** (2019-10-11):

If the balance of an Eth1 account will remain the same in the Eth1 EE of Eth2, how the Beacon Chain balances will be awarded?

---

**apbakst** (2019-10-11):

sorry if this is a dumb question, but how does the client know which shard an account/address is on?

---

**timjp87** (2019-10-13):

Would it be possible that all of ETH1 moves out to other shards after the transition and the new chain gets rid of of the “legacy baggage” kind of like a hermit crab that has grown out of its shell?

---

**jochem-brouwer** (2019-10-14):

What is meant by the `EE` term?

---

**jochem-brouwer** (2019-10-14):

Also an actual question about the transition. I assume that when the post-state root of the final block is uploaded everyone (every account) can upload their Merkle Proof to the ETH2.0 chain to prove that they had X account with Y code and for every storage address we access we also prove their value (or use the value currently known by ETH 2.0) - I assume this is the witness data.

In optimizations it is mentioned to “clear out dust accounts”. The dust accounts are unlikely to even prove their balance on ETH 2.0, so would this optimization get done by default because it is unlikely that the account will get touched again, or the “owner” of this account will upload the witness data to ETH 2.0 to get their low balance back?

---

**robert.zaremba** (2019-10-15):

Possible but highly unlikely - there are too many dapps and business built on eth1.

---

**robert.zaremba** (2019-10-15):

EE is `Execution Environment` - new terminology for shards .

---

**spengrah** (2019-10-15):

Not quite. It’s a subtle difference, but Execution Environments are not the same as shards. A single shard may have more than one EE, and an EE can exist in multiple shards. The concept of EEs is an abstraction of the EVM; basically, the Eth2 system will be able to handle more than one virtual machine. The most-used EE will likely be the EVM (eWASM), but in my understanding other EEs could exist that model state execution in different ways, e.g. a UTXO-based system, or Libra, or lots else.

There isn’t actually a great single resource that explains EEs (at least that I’ve been able to find), likely because its still an evolving concept. My current understanding has come from cobbling together bits and pieces from various places (and is probably incorrect to some degree!). If anybody more knowledgeable than I about EEs wants to create such a resource, I’m sure the community would greatly appreciate it ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) .

---

**MihailoBjelic** (2019-10-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/spengrah/48/19006_2.png) spengrah:

> The concept of EEs is an abstraction of the EVM; basically, the Eth2 system will be able to handle more than one virtual machine. The most-used EE will likely be the EVM (eWASM), but in my understanding other EEs could exist that model state execution in different ways, e.g. a UTXO-based system, or Libra, or lots else.

Exactly, this is a great explanation.

For those who want to dive deeper, here are some currently available resources from the ConsenSys Quilt team (they are actively working on EEs):

- https://www.youtube.com/watch?v=gHWMEmM940o
- Eth2 -- Beyond the Beacon Chain FINAL.pdf - Google Drive
ETH 2 Phase 2 WIKI - HackMD

Hope this helped.

---

**timbeiko** (2019-10-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The eth1 chain technically continues but it is valueless; eventually it will die off when the difficulty ice age hits.

This seems like a pretty risky assumption. Why not coordinate with ETH1 to have an upgrade where the difficulty bomb goes off on a specific block? In other words, instead of going up exponentially, make the difficulty “infinity” on block X, such that block X+1 can never be mined, and hardcode X as the final ETH1 block in ETH2.

---

**jgm** (2019-10-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/timbeiko/48/1585_2.png) timbeiko:

> This seems like a pretty risky assumption. Why not coordinate with ETH1 to have an upgrade where the difficulty bomb goes off on a specific block? In other words, instead of going up exponentially, make the difficulty “infinity” on block X, such that block X+1 can never be mined, and hardcode X as the final ETH1 block in ETH2.

If anyone wants ETH1 to continue they could bring out an alternate fork that removed the difficulty bomb entirely.  Certainly no miner would upgrade to a version of Ethereum 1 that would stop them from mining.

---

**vbuterin** (2019-10-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/timbeiko/48/1585_2.png) timbeiko:

> This seems like a pretty risky assumption. Why not coordinate with ETH1 to have an upgrade where the difficulty bomb goes off on a specific block? In other words, instead of going up exponentially, make the difficulty “infinity” on block X, such that block X+1 can never be mined, and hardcode X as the final ETH1 block in ETH2.

The problem with this is that we want the ETH1 chain to continue getting mined for a short while after the fork to prevent 51% attacks that try to cause confusion about what the fork block is.

(The in-protocol block rewards for mining those blocks would of course not get included, but the EF could easily subsidize 100 block rewards)

---

**timbeiko** (2019-10-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> If anyone wants ETH1 to continue they could bring out an alternate fork that removed the difficulty bomb entirely.

Yes, they could, but it wouldn’t be the default and so far we’ve seen a strong norm in the community (and other blockchain communities!) to follow defaults. I’m 100% in favor of having the version removing the bomb be considered the minority/unofficial/etc. fork.

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> Certainly no miner would upgrade to a version of Ethereum 1 that would stop them from mining.

Well, if exchanges and other stakeholders do, they will given that most of the value will be on that chain. Miners are already aware of PoS, so I’m not convinced that a final upgrade would make much of a difference. Also, we could pick a “final” block to be one that would already be quite hard to mine due to the difficulty bomb, in order to make the choice to not upgrade less attractive.


*(9 more replies not shown)*

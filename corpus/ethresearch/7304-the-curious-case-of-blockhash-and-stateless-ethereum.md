---
source: ethresearch
topic_id: 7304
title: The curious case of BLOCKHASH and Stateless Ethereum
author: axic
date: "2020-04-20"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/the-curious-case-of-blockhash-and-stateless-ethereum/7304
views: 5773
likes: 15
posts_count: 12
---

# The curious case of BLOCKHASH and Stateless Ethereum

**TLDR: It would be useful to consider EIP-210 (or a variant of it) for Stateless Ethereum.**

The `BLOCKHASH` opcode can be used to query the hash of the past 256 blocks. Blocks and block hashes are not part of the state trie, but are only referenced by blocks, and therefore are “implied state”. An [Ethereum block](https://ethereum.github.io/yellowpaper/paper.pdf) contains, among others, two fields: `parentHash` and the `stateRoot`. The `parentHash` is the hash of the previous block.

One of the goals of [Stateless Ethereum](https://blog.ethereum.org/2020/04/02/eth1x-stateless-tech-tree/) is that verification of a block should be a pure operation. It should not imply access to some data or state not already provided via the block. To aid this, including the canonical hash of the block witness is also proposed.

In order to fulfil this goal of purity, since the block hashes are not part of the state, they would need to be encoded in the witness.

“But hey, stateless nodes will have access to block headers!” will be the reader’s first intuition. I consider that not as pure as having everything codified via the block.

There are multiple ways to accomplish this:

1. The  block witness specification can be amended to also include every block header until the oldest one referenced in the block (worst case all 256 block headers). This could be quite large in size.
2. Include a list of historical block hashes in the block header. EVM already exposes other block header fields. While this doesn’t place block headers into the “Ethereum state”, it still accomplishes the same goal. For inspiration have a look at Eth2.0 historical roots.
3. Luckily we can also look back at an earlier proposal for Ethereum, EIP-210, which suggested placing block hashes in the state in the form of a special contract. There are two benefits this provides: 1) no need for a special encoding in the witness, since the storage locations of the contract are included; 2) potentially no need to encode as many block hashes. It also has the potential, similar to “historical roots” above, to more easily include hashes older than the past 256 blocks.

#### Relationship to Eth 2 Phase 1.5

Enforcing this purity could also prove beneficial for [Phase 1.5](https://ethresear.ch/t/eth1-eth2-client-relationship/7248) to reduce the complexity for those validators, which are not Eth1-validators.

*Thanking Sina Mahmoodi for valuable feedback.*

## Replies

**AlexeyAkhunov** (2020-04-20):

Yes, the access to `BLOCKHASH`-es for the last 256 blocks has so far been assumed in the current witness specification.

Up to this moment, the reason why the assumption has been made and not special provision in the witness format, is the desire to minimise the number of pre-requisite changes that we need to accomplish before Stateless Ethereum v1. And I think it is still reasonable to desire this. We definitely do not want to pick up more “projects” on the way.

I do not want to diminish in any way the importance of your consideration. But if we can live without it in v1, I think we should. Unless something else causes for the `BLOCKHASH`-es to be included into the state.

---

**axic** (2020-04-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> Yes, the access to BLOCKHASH -es for the last 256 blocks has so far been assumed in the current witness specification.

I had a brief look at the spec before writing this, but couldn’t find a reference to block hashes. Is it just a plan currently, or did I miss it?

---

**AlexeyAkhunov** (2020-04-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/axic/48/1578_2.png) axic:

> I had a brief look at the spec before writing this, but couldn’t find a reference to block hashes. Is it just a plan currently, or did I miss it?

It is not mentioned at all in the spec (which is probably the omission), because it is not a part of it. We just assume that whoever tries to executes the block using the witness, also has some other bits, like current header + access to last 256 block hashes

---

**axic** (2020-04-20):

Oh I misread your answer then. So you chose the “option 0: rely on clients having access to headers”.

---

**AlexeyAkhunov** (2020-04-20):

Yes, because at this moment, I don’t feel like we need to pick up more dependencies at this point, in the name of constraining the scope

---

**axic** (2020-04-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> Up to this moment, the reason why the assumption has been made and not special provision in the witness format, is the desire to minimise the number of pre-requisite changes that we need to accomplish before Stateless Ethereum v1. And I think it is still reasonable to desire this. We definitely do not want to pick up more “projects” on the way.

Do we have a concrete description what “v1” entails? I agree it would foolish to constantly extend the scope and this may very well be something, which can be made optional. However in order to make it optional, it would be nice to clearly mention this problem and the potential solutions, and why v1 doesn’t include it.

I think if enough reason and motivation is shared, someone solely concerned with Eth1 could pick “it” up, outside of Eth1x.

Lastly, there seems to be a strong affinity for purity based on the Stateless Summit, but of course there can be different levels of purity achieved.

---

**AlexeyAkhunov** (2020-04-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/axic/48/1578_2.png) axic:

> However in order to make it optional, it would be nice to clearly mention this problem and the potential solutions, and why v1 doesn’t include it.

Noted. Not sure it will need to go straight into the witness specification, but when we get to describing how EVM execution on the witness works, the mention of BLOCKHASH should go there

---

**pipermerriam** (2020-04-21):

[@axic](/u/axic) thanks for bringing this to our attention.  I would lump it into the side quests category since the option-0 is still probably a viable approach.

---

**axic** (2020-04-21):

While I am in favour of (3), that seems to potentially cause issues for account abstraction (AA): if AA requires a witness, or access lists with storage keys, then any contract using the `BLOCKHASH` opcode would need to submit the blockhash contract’s state, which would mean they are bound to a given pre-state.

---

**djrtwo** (2020-04-23):

Note that removing any “implied” components of the state transition is certainly favorable for an eth1+eth2 integration because any implied historic components put additional requirements on the data that a rapidly changing committee must retrieve from the network.

Copied from [Eth1+eth2 client relationship thread](https://ethresear.ch/t/eth1-eth2-client-relationship/7248/12):

> You’re right. I wasn’t aware of this implied component of the eth1 state transition. Assuming we don’t integrate the headers into state (I think doing so is a good idea), the beacon committees would need to sync forward from the latest crosslink in state and back-fill headers (and computed roots) to have the 256 block hashes on demand. It’s doable but puts more bandwidth overhead on the rapidly changing beacon committees.

> We’ve been careful with the eth2 state transition function to ensure it is a pure function of (pre_state, block) and not have any implied requirements. Ensure that eth1x stateless blocks are just a function of the block would make this integration much more elegant

---

**tim-becker** (2022-09-22):

Sorry to revive this old thread, but I wanted to shared one scalable solution to accessing historical block hashes on-chain that we’re using in Relic Protocol. We store Merkle roots of chunks of historical block hashes in storage, and use zk-SNARKs to prove their validity. I’m not sure if a similar approach could work for stateless clients.

For reference, see



      [github.com](https://github.com/Relic-Protocol/relic-contracts/blob/2ecb2ffdd3a450a8eb7c352628c2ef51ed038c42/contracts/BlockHistory.sol)





####



```sol
/// SPDX-License-Identifier: UNLICENSED
/// (c) Theori, Inc. 2022
/// All rights reserved

pragma solidity >=0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

import "./lib/CoreTypes.sol";
import "./lib/MerkleTree.sol";
import "./interfaces/IBlockHistory.sol";
import "./interfaces/IRecursiveVerifier.sol";

import {
    RecursiveProof,
    SignedRecursiveProof,
    getProofSigner,
    readHashWords
} from "./lib/Proofs.sol";

```

  This file has been truncated. [show original](https://github.com/Relic-Protocol/relic-contracts/blob/2ecb2ffdd3a450a8eb7c352628c2ef51ed038c42/contracts/BlockHistory.sol)


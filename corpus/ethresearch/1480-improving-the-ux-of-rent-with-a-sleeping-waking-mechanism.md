---
source: ethresearch
topic_id: 1480
title: Improving the UX of rent with a sleeping+waking mechanism
author: vbuterin
date: "2018-03-23"
category: Sharding
tags: [storage-fee-rent]
url: https://ethresear.ch/t/improving-the-ux-of-rent-with-a-sleeping-waking-mechanism/1480
views: 10258
likes: 15
posts_count: 17
---

# Improving the UX of rent with a sleeping+waking mechanism

Here is a scheme for improving the user-experience of contracts getting potentially deleted through storage rent. The general approach is as follows:

- Given any contract, you can easily determine the contract’s time-to-live (denoted in block numbers for simplicity). The TTL can be extended by adding more ETH to the contract.
- If the current block number exceeds a contract’s TTL, anyone can “poke” the contract to put it to sleep.
- If a contract is asleep, it can be re-woken by submitting (i) a Merkle proof which proves the contract’s state at the time of deletion, and (ii) a set of Merkle proofs for each block (or possibly series of blocks) that proves that the contract was not woken already (preventing a scenario where a contract dies at time T1, is resurrected at time T2, dies at time T3, and then is resurrected again but using the Merkle proof from T1 instead of the correct T3)

This can actually all be done fairly safely as a layer-2 system with no base-layer protocol changes by taking advantage of the contract creation address mechanism. The address of a contract created with CREATE is `sha3(creator + code + salt)[12:]`, so if we create a specialized factory for creating contracts then one can easily verify that a contract was created by that factory, and so if the contract is put to sleep only that same factory can re-create (“wake”) the contract at that address. The factory can have two types of contract creation:

- createNew(code, _salt): calls CREATE with salt = sha3(_salt, block.number)
- wake(address, proof): checks the Merkle proof and wakes the contract if the proof is valid

The dependence on block number of `createNew` ensures that it cannot be used to create contracts at addresses that already have code, and `wake` requires a Merkle proof to establish that it’s actually waking a contract correctly. If we establish that a contract, if it is created at all, must stay awake for one entire week (that is, require a minimum TTL of 1 week when a contract’s state is modified), then the Merkle proof would simply be one Merkle branch proving non-existence of the contract per week. If the block headers contain a skip list where each block points to the block one week earlier, then the proof size would be ~1000 bytes per week, or ~1 MB per 20 years. If a Merkle proof is larger than the maximum size of a block, it can be submitted across multiple transactions in multiple blocks.

The user experience would be as follows. Cross-contract calls to empty addresses could throw by default; this would create a security model similar to that created by access lists and the historical call stack depth limit where contracts need to assume that any contracts they call are not necessarily available. If a user wants to perform a call, and they determine that the call they want to make depends on a contract that is now asleep, they would need to find the historical data, likely from some kind of second-layer market or asking an archive node, to construct the Merkle proofs, and then they would send multiple transactions; the first transaction(s) would be the Merkle proof(s) to perform any needed reawakening(s), and the last transaction would be the user’s intended operation.

Keeping contracts in the state would be viewed as paying for the convenience of having them be accessible at a relatively low gas cost without needing to provide Merkle proofs and benefiting from the censorship resistance of arbitrary dynamic state access.

## Replies

**danrobinson** (2018-03-23):

Cool, another application for proofs of non-existence!

An idea that falls somewhere between fully live state and sleeping state is “napping” state, in which all of a contract’s code and storage is hashed into 32 bytes. To awaken the contract, you would just have to provide the contract’s code and storage, which gets verified against the hash and then reloaded back into the state. (This is somewhat similar to the UTXO model; maybe this idea has already been suggested somewhere. We implemented part of this for the Ivy-Solidity project at the IC3 bootcamp last summer.)

So you save on the Merkle proof of the full history, at the cost of having to continue to store 32 bytes of state for each contract.

This could perhaps be a probationary measure when a contract runs out of TTL before it gets put into cold sleep. Alternatively, contracts could be allowed to voluntarily put themselves into this state, to save on rent, or could automatically be put into this state after a week of inactivity.

I’m pretty sure this too could be implemented as a contract factory without base-layer support.

---

**skilesare** (2018-03-23):

I’ve been thinking about this a good bit.  If the code can be hashed, why keep the whole program as part of the blockchain at all?

A collator/validator/miner just needs:

1. Proof that the code was deployed at that address. <- Provide a witness of the deployment of the contract
2. The code <- pull from IPFS <- If it isn’t on IPFS then your transaction won’t be processed.

Self-destructs would be difficult, but you could just move that to the responsibility of the contract author to build in a lock.

Data can operate in the same way with either witness provided by the transactor(maybe get a gas discount or preferred treatment) or the collator/validator/miner goes and asks the network for a witness.

1. Collator: Slash me if I Collate and don’t pay a reward for witness X
2. Data Provider: I have witness X. Slash me if I don’t provide it.
3. Collator: Hey 0xXXXX give me the witness and here’s a receipt where you can slash me if I collate and don’t pay YOU.
4. Data Provider: Here is the data.
5. Everybody check the collation for the promise fulfillment and slash accordingly.

There are probably some withholding exploits in there that need to be worked through.

---

**vbuterin** (2018-03-24):

You can absolutely take this to extremes, and that’s kind of what the [stateless client direction](https://ethresear.ch/t/the-stateless-client-concept/172) is about; we ended up deciding that that’s a little too extreme, essentially because that would ultimately end up relying on second-layer markets where users pay nodes in the network to store witness data, which ends up basically degrading into a more rickety and less transparent rent scheme. Additionally, requiring witnesses for everything *is* a bandwidth hog, and also requires access lists, which harms censorship resistance. Rent + sleeping/waking is essentially a moderate position between status quo and statelessness, where there is a specific set of accounts that benefit from the status quo concept of state, but you have to pay per epoch (or per week) to remain in this set.

---

**vbuterin** (2018-03-24):

> An idea that falls somewhere between fully live state and sleeping state is “napping” state, in which all of a contract’s code and storage is hashed into 32 bytes.

One thing that;s worth mentioning also is that the rent mechanism can by itself incentivize optimal state management practices. If a contract has a large state and infrequent usage, it could by itself adopt a second-layer witness-plus-state-root approach to its internal state. If a contract has a lot of per-user state, it could store it in separate contracts for each user that the user is responsible for. Contracts being fully stateful by default, and then curling up into a 32-byte ball if their TTL gets low is also something that could be implemented as a layer-2 mechanism, at least if you trust on-chain poking markets.

---

**tawarien** (2018-03-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Given any contract, you can easily determine the contract’s time-to-live (denoted in block numbers for simplicity). The TTL can be extended by adding more ETH to the contract.

Will there be a separate balance for ETH added to increase the TTL and ETH intended to be managed by the contract or is it the same balance?

Will the ETH balance pay for the rent (be reduced over time) or is it intended just as some sort of state lock?

I ask these questions to get a picture about the backwards compability od this proposal and if it requieres developer of smart contracts to add extra code to manage this or if it is totally transparent.

---

**vbuterin** (2018-03-24):

> Will the ETH balance pay for the rent (be reduced over time) or is it intended just as some sort of state lock?

It could be done both ways. Either there would be a separate TTL that would need to be increased, or the TTL is implicit through the contract’s current ETH balance. I’m inclined to favor the latter approach; it removes the need to have to worry as much about explicit “poking”.

---

**phil** (2018-03-24):

I’ve become a relatively big fan of resurrection; I like the idea of skip proofs at a 1 week granularity, and the min-1-week-TTL was the missing component that I did not understand in the “proofs of non-existence” schemes.  So super ACK on this.

A few questions:

- Why keep the reasoning at a “contract” level at all?  Why not just have storage keys, which users pay rent on, and these storage keys can happen to store contract code?  It’s purely a terminology difference, but this seems cleaner to me, and unifies contract code and data storage without requiring all data to be stored in “contracts”, which makes less intuitive sense for discussion, IMO.  Of course you can say that these “contracts” are basically SLA contracts on storage locations, but I think this is sort of implicit in a rentful model when talking about data.  The lack of distinction between “data” and “code” and the idea of executing what is stored at a given address in “memory/state” is also highly intuitive from classic programming paradigms.
- Is there going to be a small incentive for poking?  Should there be one?

Personally I favor the “landlord / storage key” terminology.

---

**jamesray1** (2018-03-24):

Ah, sounds good, I didn’t read all the comments. Too much to read, must develop the roadmap from the start and look to research only on an as-needed basis.

---

**skilesare** (2018-03-24):

Do you see any value in pursuing this as a level 2 solution?  Seems like we could build something that would test out if the rickety parts hold together or not.

Do you think stateless is more possible in ETHv3?

Seems like something has to give for web scale ETH.

---

**vbuterin** (2018-03-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/phil/48/18_2.png) phil:

> Why not just have storage keys, which users pay rent on, and these storage keys can happen to store contract code?

Mainly because assigning each storage key a separate ether balance is high overhead. Incidentally, at this point I favor replacing the term “contract” with something less loaded, perhaps even just “object”. Suggestions welcome ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

> Is there going to be a small incentive for poking? Should there be one?

I’d say sure. If there isn’t, then I expect any organizations that run both proposers and a large number of nodes would still do it on their own, but we can make the incentive stronger with an explicit reward. Perhaps require contracts to have an extra day of TTL, and give that as a reward to pokers.

---

**nate** (2018-03-24):

A minor improvement to this scheme is allowing contracts that don’t change their own state to be awoken without proofs of non-existence. Because they can’t change their own state, there isn’t a danger that they will be recreated with old state.

This has the benefit of making it cheaper/easier to wake contracts that don’t modify state, as you don’t need to include any proofs of non-existence, which is especially nice for libraries and the like.

To implement this, a function `createStatic(code, salt)` can be added to the factory contract. A call to `createStatic` reverts if `code` contains a (self) state changing opcode. Otherwise, it calls CREATE with the given `code` and `salt`. When waking a static contract, simply make an identical call to `createStatic`.

Actually checking if `code` contains a (self) state changing opcode is the hard part. An extreme version would be to only allow this check to pass for pure functions/contracts, but I think this would rule out some libraries that change state of the contracts that call them but store nothing themselves. I don’t know the specifics of library implementations to know how to check for this, though ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=9)

---

**vbuterin** (2018-03-25):

Just check for the lack of SSTORE opcodes; shouldn’t that be enough?

---

**nate** (2018-03-25):

I’m not sure. I thought this was enough at first, but I realized libraries can modify the storage of contracts that use them. For example, see [here](https://github.com/Modular-Network/ethereum-libraries/blob/master/LinkedListLib/LinkedListLib.sol#L143) or  [here](https://github.com/Modular-Network/ethereum-libraries/blob/2caeeadafe587e1ee050041e8791b49593c0b4ea/CrowdsaleLib/DirectCrowdsale/truffle/contracts/TokenLib.sol#L64).

That being said, I have no idea how this is implemented. It might be the case that the actual SSTOREs are in the contracts that use these libraries - but then I’m not totally sure why libraries use DELEGATECALL ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=9)

---

**vbuterin** (2018-03-25):

Ah, yes, then DELEGATECALL probably needs to be banned too.

---

**SergioDemianLerner** (2018-03-28):

You can get ideas from  RSKIP’s on Storage rent:

Persistent Storage Rent Paid by Code

https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP7.md

Cache Oriented Storage Rent


      [github.com](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP52.md)




####

```md
# Cache Oriented Storage Rent

|RSKIP          |52           |
| :------------ |:-------------|
|**Title**      |Cache Oriented Storage Rent |
|**Created**    |12-DIC-2017 |
|**Author**     |SDL |
|**Purpose**    |Sca |
|**Layer**      |Core |
|**Complexity** |2 |
|**Status**     |Draft* |

# **Abstract**

This RSKIP proposes that contracts should pay storage rent, to reduce the risk of storage spam and to make storage payments more fair. At the same time this RSKIP discusses the limitations of storage rent due to the additional complexity and overhead that, in some cases, overweigh the benefits.

# **Motivation**

One of the problems of the RSK platform is that memory can be acquired at a low cost and never released, forcing all remaining nodes to store the information forever. There almost no examples in real-world commerce where users acquire with a single non-recurring payment eternal rights over a property that requires continued maintenance and therefore implies a periodic maintenance cost to a third party. The cost of maintenance is low but non-negligible, as persistent data must be stored in SSD so access cost matches real cost. That is the case of blockchain state storage, The cost is multiplied by the number of state replicas in the network. In some cases space is given for free (e.g. google drive space), but this is because space is subsidized by other services the google user consumes. Also there is no guarantee Google will offer free space forever. It can be argued that full nodes are altruistic, and therefore they are willing to incur any storage cost the network demands. While this may have been partially true for Bitcoin nodes in the past, this altruistic behaviour can decrease. The number of Bitcoin nodes has been declining, while the number of Bitcoin users has increased considerably, meaning that new users are not willing to run full nodes more than old users. It is expected that block pruning and sharding techniques enable users to commit certain partial amount of storage, but not for the full blockchain. However, the verification of new blocks, more than the historic storage, is what defines a full node. To verify a block, a node needs the full state, or receive inclusion proofs for all state data used. The sharding factor must be inversely proportional to the number of honest hosts a peer connects to, so if the state size grows, and other factors remain constant, the local storage must also grow. Therefore, in principle, users should pay a storage rent (e.g. bitcoins/month) for consuming persistent storage. However it is not clear who should pay for this rent. Many contracts are examples of crowd-contracts: programs that are fueled and used by the crowd, therefore they can consume a lot of memory, but no single user is in position of carrying the burden of the rent.  both in terms of monetary effort and the fact that no single user may have the incentive to carry out the task, whatever the cost is.

```

  This file has been truncated. [show original](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP52.md)








There are other 3 RSKIP’s on storage rent, but I haven’t moved them to the new RSKIP repository yet.

(E.g. “Fast Hibernation Wakeup using Trie” and “Hibernation Compression” are not there).

---

**phillip** (2018-07-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Incidentally, at this point I favor replacing the term “contract” with something less loaded, perhaps even just “object”.

“Parchment” ([Goguen & Burstall 1986](http://www.lfcs.inf.ed.ac.uk/reports/86/ECS-LFCS-86-10/)) might work for a “chartering” notion commensurate with institutionally grounded (*cf., e.g.*, [North 1991](https://www.jstor.org/stable/1942704) on “rules of the game”) economic rents.


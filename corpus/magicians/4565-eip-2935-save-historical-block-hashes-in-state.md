---
source: magicians
topic_id: 4565
title: "EIP-2935: Save historical block hashes in state"
author: vbuterin
date: "2020-09-03"
category: EIPs > EIPs core
tags: [opcodes, data, eip-2935]
url: https://ethereum-magicians.org/t/eip-2935-save-historical-block-hashes-in-state/4565
views: 7359
likes: 11
posts_count: 33
---

# EIP-2935: Save historical block hashes in state

Store historical block hashes in a contract, and modify the `BLOCKHASH (0x40)` opcode to read this contract.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2935)














####


      `master` ← `vbuterin-patch-4`




          opened 05:35AM - 03 Sep 20 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/8/89ac618501d77ed85e1ea0663718f590291e7737.png)
            vbuterin](https://github.com/vbuterin)



          [+63
            -0](https://github.com/ethereum/EIPs/pull/2935/files)







Store historical block hashes in a contract, and modify the `BLOCKHASH (0x40)` o[…](https://github.com/ethereum/EIPs/pull/2935)pcode to read this contract.

## Replies

**MicahZoltu** (2020-09-03):

Big fan personally, because it would make it so https://github.com/Keydonix/uniswap-oracle/ could work over longer periods of time than 1 hour.

---

**ajsutton** (2020-09-03):

While it’s probably ok to have this list be ever increasing in size, given we currently have a 256 block limit on block hash it seems sensible to put an upper bound on the history stored.  That should be as simple as using `sstore(HISTORRY_STORAGE_ADDRESS, block.number - 1 % 256, block.prevhash)` for storage and `sload(HISTORY_STORAGE_ADDRESS, arg % 256)` to load, preserving the current checks that arg < 256.

We could still increase the limit from 256 if desired but avoiding the assumption that history will be available indefinitely seems wise, especially since the ETH2 history only preserves a limited range and it’s unlikely that ETH1 will be moved into ETH2 within that timeframe (~13 hours). Otherwise we risk it becoming a backwards incompatible change when moving to ETH2 or being stuck storing unlimited block history forever.

---

**holiman** (2020-09-07):

This EIP doesn’t mention any repricing of `BLOCKHASH`. Seems to me that the current `20`(?) will be far too low, seeing as this will have to traverse a (with time) pretty large trie.

---

**axic** (2020-09-07):

![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 20 Apr 20](https://ethresear.ch/t/the-curious-case-of-blockhash-and-stateless-ethereum/7304)



    ![image](https://ethereum-magicians.org/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_500x500.png)



###





          Execution Layer Research






            stateless







TLDR: It would be useful to consider EIP-210 (or a variant of it) for Stateless Ethereum.  The BLOCKHASH opcode can be used to query the hash of the past 256 blocks. Blocks and block hashes are not part of the state trie, but are only referenced...



    Reading time: 2 mins 🕑
      Likes: 15 ❤











After this I had a few discussions and it seems having the blockhash in state, but not in a contract/account, is what would work the best with witnesses and transaction packaging. If it is part of an account’s state, then witnesses have to have a special case for this account or it would not be easy for “relayers” to batch and update witnesses for the blockhash.

By having it in the state I mean to store its root in the block header and keep it separate to the account trie, similar to historical hashes on the beacon chain.

---

**holiman** (2020-09-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> By having it in the state I mean to store its root in the block header and keep it separate to the account trie, similar to historical hashes on the beacon chain.

Interesting. It would definitely reduce the ‘witness-churn’, and one could imagine having a `BLOCKROOT` opcode to retrieve the `cht-root`. That type of solution could, if given a `(number,hash)` check if it’s in the history, whereas the proposed `2935` is more powerful; given a `number`, it could look up the `hash`.

Dunno enough about the indended usecases to know whether that’s sufficient or not.

---

**axic** (2020-09-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> Interesting. It would definitely reduce the ‘witness-churn’, and one could imagine having a BLOCKROOT opcode to retrieve the cht-root . That type of solution could, if given a (number,hash) check if it’s in the history, whereas the proposed 2935 is more powerful; given a number , it could look up the hash .
>
>
> Dunno enough about the indended usecases to know whether that’s sufficient or not.

Actually that is a good question, what are the intended use cases:

1. I would think many still use it as a terrible source of randomness. Which is discouraged.
2. For creating proofs, one can definitely expect the sender to provide their expected root hash (supposedly they compare that against what BLOCKHASH returns) and it would not be unheard of to ask for the appropriate block number too. So I think a system like BLOCKROOT would not hinder the use cases where a proof is validated.

Is there any other use case out there?

---

**holiman** (2020-09-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> For creating proofs, one can definitely expect the sender to provide their expected root hash (supposedly they compare that against what BLOCKHASH returns) and it would not be unheard of to ask for the appropriate block number too. So I think a system like BLOCKROOT would not hinder the use cases where a proof is validated.

Although… this would also suffer from the same churn. Say you provide hashes 15 root elements, and a few more hashes along the way to prove your `BLOCKHASH`. And ship that off in a transaction… Well, whether it goes into block `N` or `N+1` will make all the difference whether your proof is valid or not.

Btw, sidenode: geth uses `cht`s, both hardcoded (we update the cht when we make new releases) and in contract-form (which we submit new cht signatures into around the time of releases). Those cht:s are in certain section sizes, of `32768` blocks. See https://github.com/ethereum/go-ethereum/blob/master/contracts/checkpointoracle/contract/oracle.sol

---

**BoltonBailey** (2020-09-08):

This would also make it more straightforward to implement a [FlyClient](https://eprint.iacr.org/2019/226.pdf)-type client.

---

**yoavw** (2020-09-08):

One use case to consider is an “introspection engine” that allows contracts to consider assertions about any past state.  Similar to verifying a fraud proof against optimistic rollup data, but more generalized.  It becomes possible to trustlessly look at any blockchain data from inside EVM.

For this use case, the block number and block hash are known when making the transaction, so it would work fine even if the block hash can only be verified in EVM rather than queried.  It’s just proof validation.

One use I’m exploring for such introspection engine is trustless blockchain read access through a network of staked nodes.  A client would be able to query the history (at cost), get a signed reply, and be able to verify it with other staked nodes who would be able to slash any node that provided clients with bogus history.  That makes ultra-light clients quite easy to implement.

---

**vbuterin** (2020-09-08):

> By having it in the state I mean to store its root in the block header and keep it separate to the account trie, similar to historical hashes on the beacon chain.

This is indeed how it’s done on eth2. The challenge I see is just that on eth1 this would be more challenging to implement, requiring a whole new data structure etc etc. Whereas the storage-based solution is much more surgical and non-intrusive. Any opcodes would just seamlessly migrate from being based off of the eth1 blockhash store to being based off of the eth2 blockhash store.

---

**tkstanczak** (2020-10-10):

Suggested minor fix:

https://github.com/ethereum/EIPs/pull/3033

---

**tkstanczak** (2020-10-10):

Implementation in Nethermind:



      [github.com/NethermindEth/nethermind](https://github.com/NethermindEth/nethermind/pull/2368/files)














####


      `master` ← `eip2935`




          opened 10:31AM - 10 Oct 20 UTC



          [![](https://avatars.githubusercontent.com/u/498913?v=4)
            tkstanczak](https://github.com/tkstanczak)



          [+163
            -6](https://github.com/NethermindEth/nethermind/pull/2368/files)







https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2935.md

---

**tkstanczak** (2020-10-10):

I am suggesting the cost of SLOAD (800) instead of the cost of BLOCKHASH (20) when searching.

Interesting case is - > shall we always charge 20 for the last 256 blocks or start charging 800 for everything after the FORK_BLKNUM + 256.

I suggest 800 always as we wanted to raise the BLOCKHASH cost anyway.

And the last thing -> I suggest creating an account with the bytecode of [‘STOP’] at the BlockhashStorage address at FORK_BLKNUM to avoid the strange case where we have an account with no code but with storage. This could lead to various problems with existing behaviours.

---

**sinamahmoodi** (2020-10-12):

I’d like to argue for adding all block hashes since genesis to the history contract and not only the ones since the HF block. Otherwise if we want to build a light-client sync protocol on top of this EIP, the HF block becomes sort of a new hard-coded genesis. It should also be useful for the L2 networks stated in the motivations of the EIP.

---

**vbuterin** (2020-10-14):

> I’d like to argue for adding all block hashes since genesis to the history contract and not only the ones since the HF block.

Unfortunately doing large one-time state changes like that would require machinery that we don’t yet have.

I’d recommend that we just have an “untrusted setup ceremony” where people run a script to generate a Merkle root of the first FORK_BLKNUM block hashes, and that gets hardcoded into all the wallets and anything else that needs to access history; anyone can run the script to check the root themselves later if they wish.

---

**shemnon** (2020-10-27):

can this be done without the storage trie write?  Couldn’t BLOCKHASH simply be re-written to say “either 256 blocks or since the fork” and let the clients choose their own storage mechanism?  Perhaps Kate Commitments instead?  I really don’t like the idea of adding an unbound merkle trie update to every block.  With the miner reward and other contracts at least the trie is not mandated to grow for each block, whereas this requires one storage trie to always update.

---

**sinamahmoodi** (2020-10-28):

I agree the BLOCKHASH opcode and history contract are not dependent on each other as you say, but most of the use-cases become feasible with the history contract. So ideally we’d have that even if without the BLOCKHASH opcode modification (since you can prove old blocks in EVM when you have the commitment).

> whereas this requires one storage trie to always update.

If the concern is the cost of this update, can’t the tx base fee be increased to account for it?

---

**poojaranjan** (2021-01-20):

EIP-2935 explained by Tomasz Stanczak - https://youtu.be/QH5yuNd3B6o

---

**yoavw** (2021-02-11):

Good talk by [@tkstanczak](/u/tkstanczak).

Regarding the comment about not feeding prehistory (block hashes from before the fork) I think that’s fine although I intend to (rarely) access prehistory in one of my contracts.

I intend to solve by running a script, after the fork, which generates a merkle tree of all prehistorical hashes, and stores the root in a contract that has a verification function.  Caller would provide block number, block hash, and merkle path to prove it.  The script itself will be published so anyone would be able to run it independently to verify the merkle root before trusting that contract.  Since prehistory never changes after the fork, you only need to run it once.

Storage is O(1), at the cost of merkle verification on every access.  Probably a reasonable trade-off for those rare cases where a contract needs to access ancient blocks.

---

**chfast** (2021-03-19):

Can we please use an address close to the bottom of the address space? Anything smaller than `2*32` will be fine.


*(12 more replies not shown)*

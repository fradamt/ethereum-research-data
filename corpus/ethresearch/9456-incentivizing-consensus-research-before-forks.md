---
source: ethresearch
topic_id: 9456
title: Incentivizing consensus research before forks
author: yoavw
date: "2021-05-11"
category: Security
tags: []
url: https://ethresear.ch/t/incentivizing-consensus-research-before-forks/9456
views: 1418
likes: 2
posts_count: 3
---

# Incentivizing consensus research before forks

# Incentivizing consensus research before forks

The recent consensus issue after the Berlin fork has highlighted the need to spend more resources on ensuring there’s no way to break consensus between different clients.  I suggest a decentralized bounty that incentivizes security researchers to find such corner cases and report them on a testnet rather than mainnet.

### The high level idea

Make a minimal modification to all clients, to let users get a proof of a state change and the transactions that led to it.  Deploy a bounty contract to mainnet, which pays the bounty to the first researcher who proves breaking the state on a testnet.

### The required change

Each client (e.g. geth, OpenEthereum) should implement a new RPC call, `eth_stateCommitment(blocknum)` which works for recent blocks and returns a state-change commitment signed by the node’s private key:

`{ 'blockNum':num, 'preStateRoot':hash, 'postStateRoot':hash, 'transactions':[..], 'signature':{r,s,v} }`

The list of transactions is the full list included in that block.

### The bounty contract on mainnet

The contract will contain a bounty in ETH, and will have a list of public keys for all testnet nodes included in the game.  The list contains nodes from any number of testnets, but never from mainnet nodes.

The contract shall use commit/reveal to ensure that the bounty can be claimed by the researcher rather than a frontrunner.  A minimum time of 30 minutes is enforced between commit and reveal.

`commit(hash)` - record msg.sender and the hash, which should be keccak(transaction,nonce).

`prove(transaction,nonce,signedStateCommitment_1,signedStateCommitment_2)` - prove that consensus was broken in that block.  Check if:

1. keccak(transaction,nonce) was committed by msg.sender.
2. Both state commitments have the same block number, the same preStateRoot, and the same list of transactions.
3. ecrecover both signatures, ensure that they differ and that both are registered testnet nodes on the same testnet.
4. The two postStateRoots differ.

If all are true, send the entire balance to msg.sender.  An event is emitted to alert the client maintainers.

At this point the bounty contract is empty so no further claims will be paid.  The bounty will be replenished only after the bug is fixed and all nodes are upgraded.  This ensures that each bug is only paid once, and only to the researcher who found it.

### The flow of an “attack”

Alice researched two different clients and found a way to break consensus.  E.g. a transaction involving a new precompile.  She follows the following procedure:

1. Prepare the transaction (or sequence of transactions) that will trigger the bug
2. Prepare the commitment.  If the attack involves multiple transactions, she only prepares a commitment for the final transaction in the sequence, the one that triggers the bug.  Alice calculates keccak(transaction,random_nonce) and sends it to commit().
3. Ensure that the commitment has been recorded under her own address.  If Alice has been frontrun, she repeats the process with a new nonce.
4. Perform the attack on a testnet which participates in the bounty.
5. Contact two testnet nodes of different types, and requests eth_stateCommitment(blocknum) for the block that included the transaction.
6. Verify that the two state commitments have different post states, indicating that the attack has succeeded.
7. Call prove(transaction,nonce,signedStateCommitment_1,signedStateCommitment_2)
8. Profit!

At that point the client maintainers are alerted, given the transaction, and can research and fix the bug.

#### Caveat

The bounty could also be claimed by an attacker who manages to steal the private key of one of the testnet nodes, by signing a bad state commitment.  While this doesn’t reveal a consensus bug, it does indicate that a specific client has been hacked and is therefore worth knowing as well.

## Replies

**axic** (2021-07-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> Prepare the commitment. If the attack involves multiple transactions, she only prepares a commitment for the final transaction in the sequence, the one that triggers the bug. Alice calculates keccak(transaction,random_nonce) and sends it to commit().

Why only the last transaction?

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> eth_stateCommitment(blocknum) which works for recent blocks and returns a state-change commitment signed by the node’s private key:
>
>
> { 'blockNum':num, 'preStateRoot':hash, 'postStateRoot':hash, 'transactions':[..], 'signature':{r,s,v} }
>
>
> The list of transactions is the full list included in that block.

Wouldn’t the transaction hashes be enough instead of the entire transactions?

One challenge I see which can render this impractical is the amount of data needed to be submitted to mainnet.

---

**yoavw** (2021-07-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/axic/48/1578_2.png) axic:

> Why only the last transaction?

Because that’s the transaction that triggers the split and it’s easy to prove it by showing two different post-states signed by two different clients.  Proving (to a contract) that some previous transactions contributed to the exploit would be too complex, and not add much value.  Once the bug is disclosed through that single transaction, it won’t be too hard for core devs to figure out what led to this situation and whether a previous transaction played a role.

![](https://ethresear.ch/user_avatar/ethresear.ch/axic/48/1578_2.png) axic:

> Wouldn’t the transaction hashes be enough instead of the entire transactions?

Yes, I meant transaction hashes.  We only need enough data to show that the committed transaction is really included in the last block that was mined just before the consensus failed.  Theoretically it could just be the hash of the block header or the merkle root of the transaction hashes in the block, as the “attacker” just needs to prove that a certain transaction is included in that block.

![](https://ethresear.ch/user_avatar/ethresear.ch/axic/48/1578_2.png) axic:

> One challenge I see which can render this impractical is the amount of data needed to be submitted to mainnet.

So maybe we should go with the above.  Replace ‘transactions’ (hashes) with the block’s transactionsRoot.  The “attacker” will obtain the block header and produce a merkle proof against the root which is part of the signed commitment.

Then, the mainnet transaction for proving the attack will have to include `(stateCommitment,txhash,merkleProofForTxhash)` where `stateCommitment` is `(blockNum,preStateRoot,PostStateRoot,transactionsRoot,signature)`  This doesn’t seem like too much data to submit, and the merkle proof is fairly cheap for a tree of this size.

The downside of using this scheme instead of a list of transaction hashes is that it is tied to the current structures, which may change in the future (e.g. Verkle trees).  Maybe it doesn’t matter because we could agree that the `transactionsRoot` field is always a merkle root of the transaction hashes, regardless of how it’s represented in the block header.  The nodes will produce a merkle when this RPC is used, even if the block header no longer uses that.


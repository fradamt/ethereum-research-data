---
source: ethresearch
topic_id: 172
title: The Stateless Client Concept
author: vbuterin
date: "2017-10-24"
category: Sharding
tags: [stateless]
url: https://ethresear.ch/t/the-stateless-client-concept/172
views: 39950
likes: 48
posts_count: 17
---

# The Stateless Client Concept

There exists a protocol transformation that theoretically can be made to many kinds of protocols that in mathematical terms looks as follows. Suppose that we use the state transition lingo, STF(S, B) -> S’, where S and S’ are states, B is a block (or it could be a transaction T), and STF is the state transition function. Then, we can transform:

S -> the state root of S (ie. the 32 byte root hash of the Merkle Patricia tree containing S)

B -> (B, W), where W is a “witness” - a set of Merkle branches proving the values of all data that the execution of B accesses

STF -> STF’, which takes as input a state root and a block-plus-witness, uses the witness as a “database” any time the execution of the block needs to read any accounts, storage keys or other state data [exiting with an error if the witness does not contain some piece of data that is being asked for], and outputs the new state root

That is, full nodes would only store state roots, and it would be miners’ responsibility to package Merkle branches (“witnesses”) along with the blocks, and full nodes would download and verify these expanded blocks. It’s entirely possible for stateless full nodes and regular full nodes to exist alongside each other in a network; you could have translator nodes that take a block B, attach the required witness, and broadcast (B, W) on a different network protocol that stateless nodes live on; if a miner mines a block on this stateless network, then the witness can simply be stripped off, and the block rebroadcasted on the regular network.

The simplest way to conceive the witness in a real protocol is to view it as an RLP-encoded list of objects, which could then be parsed by the client into a {sha3(x): x} key-value map; this map can then simply be plugged into an existing ethereum implementation as a “database”.

---

One limitation of the above idea being applied to Ethereum as it exists today is that it would still require miners to be state-storing full nodes. One could imagine a system where transaction senders need to store the full state trie (and even then, only the portions relevant to them) and miners are also stateless, but the problem is that Ethereum state storage access is *dynamic*. For example, you could imagine a contract of the form `getcodesize(sha3(sha3(...sha3(x)...)) % 2**160)`, with many thousands of sha3’s in the middle. This requires accessing the code of an account that cannot be known until millions of gas worth of computation have already been done. Hence, a transaction sender could create a transaction that contains a witness for a few accounts, performs a lot of computation, and then at the end attempts to access an account that it does not have a witness for. This is equivalent to the [DAO soft fork vulnerability](http://hackingdistributed.com/2016/06/28/ethereum-soft-fork-dos-vector/).

A solution is to require a transaction to include a static list of the set of accounts that it can access; like [EIP 648](http://github.com/ethereum/EIPs/issues/648) but much stricter in that it requires a precise enumeration rather than a range. But then there is also another problem: by the time a transaction propagates through the network, the state of the accounts it accesses, and thus the correct Merkle branches to provide as a witness, may well be different from the correct data when the transaction was created. To solve this, we put the witness *outside* the signed data in the transaction, and allow the miner that includes the transaction to adjust the witness as needed before including the transaction. If miners maintain a policy of holding onto all new state tree nodes that were created in, say, the last 24 hours, then they will necessarily have all the needed info to update the Merkle branches for any transactions published in the last 24 hours.

This design has the following advantages:

1. Miners and full nodes in general no longer need to store any state. This makes “fast syncing” much much faster (potentially a few seconds).
2. All of the thorny questions about state storage economics that lead to the need for designs like rent (eg. https://github.com/ethereum/EIPs/issues/35 http://github.com/ethereum/EIPs/issues/87 http://github.com/ethereum/EIPs/issues/88) and even the current complex SSTORE cost/refund scheme disappear, and blockchain economics can focus purely on pricing bandwidth and computation, a much simpler problem)
3. Disk IO is no longer a problem for miners and full nodes. Disk IO has historically been the primary source of DoS vulnerabilities in Ethereum, and even today it’s likely the easiest availability DoS vector.
4. The requirement for transactions to specify account lists incidentally adds a high degree of parallelizability; this is in many ways a supercharged version of EIP 648.
5. Even for state-storing clients, the account lists allow clients to pre-fetch storage data from disk, possibly in parallel, greatly reducing their vulnerability to DoS attacks.
6. In a sharded blockchain, security is increased by reshuffling clients between shards frequently; the more quickly clients are reshuffled, the more adaptive the adversaries that the scheme is secure against in a BFT model. However, in a state-storing client model, reshuffling involved clients download the full state of the new shard they are being reshuffled to. In a stateless client, this cost drops to zero, allowing clients to be reshuffled between every single block that they create.

One problem that this introduces is: who *does* store state? One of Ethereum’s key advantages is the platform’s ease of use, and the fact that users do not have to care about details like storing private state. Hence, for this kind of scheme to work well, we have to replicate a similar user experience. Here is a hybrid proposal for how this can be done:

1. Any new state trie object that gets created or touched gets by default stored by all full nodes for 3 months. This will likely be around 2.5 GB, and this is like “welfare storage” that is provided by the network on a voluntary basis. We know that this level of service definitely can be provided on a volunteer basis, as the current light client infrastructure already depends on altruism. After 3 months, clients can forget randomly, so that for example a state trie object that was last touched 12 months ago would still be stored by 25% of nodes, and an object last touched 60 months ago would still be stored by 5% of nodes. Clients can try to ask for these objects using the regular light client protocol.
2. Clients that wish to ensure availability of specific pieces of data much longer can do so with payments in state channels. A client can set up channels with paid archival nodes, and make a conditional payment in the channel of the form “I give up $0.0001, and by default this payment is gone forever. However, if you later provide an object with hash H, and I sign off on it, then that $0.0001 instead goes to you”. This would signal a credible commitment to being possibly willing to unlock those funds for that object in the future, and archival nodes could enter many millions of such arrangements and wait for data requests to appear and become an income stream.
3. We expect dapp developers to get their users to randomly store some portion of storage keys specifically related to their dapp in browser localstorage. This could even deliberately be made easy to do in the web3 API.

In practice, we expect the number of “archival nodes” that simply store everything forever to continue to be high enough to serve the network until the total state size exceeds ~1-10 terabytes after the introduction of sharding, so the above may not even be needed.

Links discussing related ideas:

- https://github.com/ethereum/sharding/blob/develop/docs/account_redesign_eip.md
- https://github.com/ethereum/EIPs/issues/726

## Replies

**jannikluhn** (2017-10-25):

Beautiful concept. One obvious concern is the significantly increased transaction size. Essentially, the set of all transactions would store the whole state, but very inefficiently in form of one Merkle branch for each accessed value. Am I right in assuming, though, that only the bandwidth of full nodes would be affected by that (and thus tx size wouldn’t matter that much)?

> We expect dapp developers to get their users to randomly store some portion of storage keys specifically related to their dapp in browser localstorage.

Wouldn’t they have to be essentially full nodes, though? In order to create a Merkle branch for even a single value they need to keep track of every state update as each at least changes the state root.

> If miners maintain a policy of holding onto all new state tree nodes that were created in, say, the last 24 hours

Couldn’t this be reduced to only a few minutes? Reasoning: Only state changes in the time frame between transaction creation and inclusion in a block are relevant. So keeping track of state updates for the average confirmation time plus some safety margin should suffice.

---

**vbuterin** (2017-10-25):

> Am I right in assuming, though, that only the bandwidth of full nodes would be affected by that (and thus tx size wouldn’t matter that much)?

If by “only full nodes” you mean “not light nodes”, then correct. Light nodes of course still need to keep downloading Merkle branches for everything they access, but for them that’s status quo. Note also that in the stateless client paradigm a node can choose to flip between “full” mode and “light” mode arbitrarily.

> Wouldn’t they have to be essentially full nodes, though? In order to create a Merkle branch for even a single value they need to keep track of every state update as each at least changes the state root.

Not necessarily. If a stateless node downloads a block that modifies the state of account C, then the block’s witness contains the Merkle branch for C, and so the node can now store that branch, without having any other portion of the state. Also, nodes still have the ability to act as light clients and download any branch of the state that they need from the network.

> Couldn’t this be reduced to only a few minutes? Reasoning: Only state changes in the time frame between transaction creation and inclusion in a block are relevant. So keeping track of state updates for the average confirmation time plus some safety margin should suffice.

Yes. But given that some low-fee transactions are delayed by many hours during, eg, ICOs, I think 24 hours is a safe window.

---

**mhchia** (2017-10-26):

Cool idea!

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> To solve this, we put the witness outside the signed data in the transaction, and allow the miner that includes the transaction to adjust the witness as needed before including the transaction.

I’m just curious that is there any possibility that a miner does something bad to the witness? like tampering the witness to make the transaction access to wrong accounts?

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ahh it seems no incentive for a miner to do it.

---

**vbuterin** (2017-10-26):

The witness is a set of Merkle branches, which are all authenticated against the state root. So *falsifying* the witness is impossible; the only thing you can do is *omit* part of the witness. This would just make an invalid block.

---

**jamesray1** (2017-11-10):

Another advantage of this stateless client concept is that it seems that it would be easier for anyone to be a validator or full node. This fits nicely with Ethereum’s ethos of decentralization. Compare that with a proposal that the number of validators in Casper be restricted to 250, or whatever. With a stateless client perhaps that would not be necessary, and perhaps anyone could be a validator. However, I haven’t considered in detail the practicalities of anyone being a validator, or not having a limit on the number of validators, with this concept. Reading after that full nodes store modified state trie objects are stored for three months, then forgotten randomly by clients after that, this would then place some minimum limit on the storage space required by full nodes, thus it wouldn’t be so easy for anyone to be a full node. “We expect the number of “archival nodes” that simply store everything forever to continue to be high enough to serve the network until the total state size exceeds ~1-10 terabytes”. 1 or 2 TB can be done economically by anyone, but not all desktop computers have 1 or 2 TB of space, particularly computers that only have SSDs like mine (although you could use an external hard drive, but that would reduce bandwidth via a USB3.0 connection), 10 TB is harder.

“Clients that wish to ensure availability of specific pieces of data much longer can do so with payments in state channels.” This idea is not a regular payment like rent, but it does internalize at least to some extent the cost of storage. However, more accurately internalizing the cost seems like it is worth further investigation.

---

**nate** (2017-11-10):

The limitation on the number of validators is not due to the amount of state data that the need to store - rather, it has to do with the overhead of the consensus protocol being run.

For example, in current designs for Casper the Friendly Finality Gadget, two consecutive rounds (epochs) of voting are required by a super-majority of the validators (by weight). So if more validators participate, there is higher overhead for the protocol to continue finalizing blocks.The tradeoff here is essentially between time to finality, number of validators, and acceptable amount of overhead for the protocol.

Totally with you on the exploration of pushing costs of storing state to those who want it to be stored, rather than the rest of the world forever ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**jamesray1** (2017-11-10):

Yeah I guess I didn’t put a lot of thought into it. I have read the CFFG paper, I just forgot that more validators would increase the block finalization rate.

---

**lithp** (2017-12-20):

This is a cool idea! Trying to wrap my head around it, I’m still pretty new to Ethereum:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A solution is to require a transaction to include a static list of the set of accounts that it can access; like EIP 648 but much stricter in that it requires a precise enumeration rather than a range

You could get around relying on EIP 648 to prevent a DOS by treating an incomplete witness the same way a transaction running out of gas is treated; include the transaction but don’t apply any of it’s effects and give the full transaction fee to the miner. In order for other nodes to be able to know it was an invalid transaction the witness, or at least a hash of it, needs to be inside the signed part of the transaction.

However, that idea hasn’t been mentioned so far because EIP 648 is independently useful and probably going to be added anyway?

It’s important that multiple transactions be able to modify the same part of the tree within a single block, so you still want the miners to be able to substitute their own witnesses for transactions. But that shouldn’t require any additional bandwidth. For invalid transactions miners can propagate just the original witness, to prove that they deserve the transaction fee. For valid transactions miners can include a more current witness and only propagate that.

---

**vbuterin** (2017-12-20):

> You could get around relying on EIP 648 to prevent a DOS by treating an incomplete witness the same way a transaction running out of gas is treated; include the transaction but don’t apply any of it’s effects and give the full transaction fee to the miner.

The problem is that it’s the miner’s responsibility to update the witness correctly, and we don’t want to add opportunities for miners to give themselves free money by deliberately adding bad witnesses.

---

**lithp** (2017-12-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The problem is that it’s the miner’s responsibility to update the witness correctly, and we don’t want to add opportunities for miners to give themselves free money by deliberately adding bad witnesses.

Oh, I guess didn’t describe it properly.

![](https://ethresear.ch/user_avatar/ethresear.ch/lithp/48/1170_2.png) lithp:

> In order for other nodes to be able to know it was an invalid transaction the witness, or at least a hash of it, needs to be inside the signed part of the transaction.

This is important for the reason you described. There would need to be a new transaction type which includes a hash of the witness. Miners could then provide the witness matching that hash to prove the transaction tried to use an address it didn’t provide.

I had thought this would let you make stateless clients without assuming EIP 648 but just realized it only pushes the problem one level down; miners can still DOS other miners by sending out blocks with witnesses which don’t prove all addresses which the block accesses.

So I suppose something like EIP 648 is necessary, and it’s much simpler too.

---

**AFDudley** (2017-12-25):

My goal is to add storage trie and state trie gossiping for Ethereum via VulcanizeDB. We are a couple of sprints away from that now. It seems like a “simple” interim step would be writing clients that can “fill in the blanks” of their fast history by pulling state from quorums archive nodes. I’ve read the geth source, it seems like we should be able to get quorum on a state and inject it. I’m basically suggesting out of protocol snapshotting, because I think that will have less political friction than trying to get it in-protocol (, also Casper the Friendly Finality Gadget will provide that).

Right now this just does smart contract watching. We need to add more usage documentation.



      [github.com](https://github.com/vulcanize/vulcanizedb)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/2/5/258406414ad0558e74a9bb42a9fd7dffd8c4f37b_2_690x344.png)



###



Contribute to vulcanize/vulcanizedb development by creating an account on GitHub.










Here you can some my ranting about the fast/full issue (Sorry, Twitter threading isn’t the best):

https://twitter.com/AFDudley0/status/943594635879907328

https://twitter.com/AFDudley0/status/943577940264194048

---

**ldct** (2017-12-27):

Is this the same mechanism as TXO commitments that have been proposed for Bitcoin? Where `S` (in the notation in the OP) is the TXO set

https://petertodd.org/2016/delayed-txo-commitments#txo-commitments

---

**vbuterin** (2017-12-28):

TXO / UTXO commitments are basically bitcoin’s term for a “state tree”, which we have had since day 1. Here, we’re talking about clients that *only* store the root of the tree.

---

**meyer9** (2018-08-12):

How would this new stateless transition function work if the structure of the tree changes? (i.e. an account is created)

For example, let’s say D is sending some ETH to a new account, H which falls between F and G. The proof for F’s balance consists of `[D, hash(E), hash(C)]`, but to add H, we would also need `hash(F)` to find the new Merkle root. Would the transaction witness also include Merkle branches where the new account would be inserted?

```
      A
    /   \
   B     C
  / \   / \
 D   E F   G

        K
       / \
      J   \
    /   \  \
   B     I  \
  / \   / \  \
 D   E F   H  G
```

Worst case - if you were inserting an account in the middle of the tree, you’d need half of the state to find the new state root. (inserting between E and F, you would need hash(F) and hash(G))

EDIT: I believe this is solved by using accumulators instead of merkle trees: [Accumulators, scalability of UTXO blockchains, and data availability](https://ethresear.ch/t/accumulators-scalability-of-utxo-blockchains-and-data-availability/176)

---

**holiman** (2019-10-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> To solve this, we put the witness outside the signed data in the transaction, and allow the miner that includes the transaction to adjust the witness as needed before including the transaction. If miners maintain a

Reading up on old posts about statelessness, I found this post which is a couple of years old, but it contained some good points that I wanted to explore further.

Given that witness data it outside of the signed tx data, how about

- having a field within the tx, which basically is proof_award set to a unit in wei.

That would mean a user can sign a transaction, and say 'it’s worth X wei for me, if someone provides this tx with the proofs it needs". He would then put the address of some known proof-provider, and if the transaction is ever included in a block (which it only ever can be if said proof is attached), the `proof_award` is sent from `sender` to `prover`.

That transfer would be like a mining reward: no execution. It *could* also be a constraint that the `prover` already needs to exist in state.

This would make it possible to earn money off a full node without being a miner, and incentivise the witness provider ecosystem. Are there any other resources I should look into to read up more about the research and current thoughts in this space?

Also, I think the witness data should be a three-step process:

1. User supplies tx, without witness data,
2. Witness provider provides data,
3. Miner takes N transactions, reorganises/comibines proofs to be more space-efficient.

---

**M8loss** (2021-01-05):

I like, very intuitive. ![:v:](https://ethresear.ch/images/emoji/facebook_messenger/v.png?v=9)


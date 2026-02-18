---
source: ethresearch
topic_id: 4498
title: Couldn't a token-less, data-only blockchain simulate smart contracts?
author: maiavictor
date: "2018-12-06"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/couldnt-a-token-less-data-only-blockchain-simulate-smart-contracts/4498
views: 3853
likes: 5
posts_count: 9
---

# Couldn't a token-less, data-only blockchain simulate smart contracts?

Not sure if this is the best place to ask questions, but this is something that bugged me for a while. Assume we have a network like Bitcoin, but without a native token. That is, block headers stay basically the same, but transactions are just bulk, arbitrary data rather than outputs. Miners include transactions to blocks by sorting them by hash (PoW) or other incentives. In other words, such network would be merely an ever-growing, resilient log of data.

Now, imagine a group of people agree on a single function `compute_dapp_state(txs : Vec<Bytes>) -> Bytes` which takes a log of buffers, filters it looking for a specific format, interprets those buffers as transactions and returns a final state. As an example, suppose I develop a `crypto_bunnies()` function that 1. filters transactions in the format `I, <user_name> want to sell bunny <X>, signed: <sig>`, 2. parses it, 3. checks signatures, 4. updates a state, 5. returns it.

As long that group of people keep the same copy of `crypto_bunnies()` and have access to the token-less blockchain, couldn’t they essentially emulate smart-contracts? That is, to interact with the contract, they just need to make a transaction on the token-less chain with the format expected by its defining function, i.e., `crypto_bunnies()`. Others users would be automatically notified of it, since they all access the same chain of logs. In other words, computation would be 100% offline; full nodes would not perform any computation at all, they’d only aggregate events. Then, users of a smart contract would agree with the same deterministic function to compute the application’s state based on those events.

Surely, such network would have major drawbacks. For example, since the merkle-patricia root of the state of a block ins’t included on its header, full nodes can’t produce short proofs of selected states; in fact, chances are full nodes don’t even compute such states. Also, not having a gas mechanism means each contract would need to ensure its computational cost is a linear function on the number of transactions, otherwise it’d easily become too expensive. On the other hands, there would be no more such a thing as a Crypto-Kitties like DApp DDOS’ing the network, since the consensus-relevant part of the system doesn’t perform any computation.

Nether less, is any fundamental flaw on this understanding that a token-less, data-only blockchain coupled with a reducer function like that would essentially implement smart contracts? Is there any obvious attack that could be performed on such design, that is somehow prevented on Ethereum?

## Replies

**hkalodner** (2018-12-06):

The main issue is that every user has to run a full node. This is used in multiple L2 applications that run on top of Bitcoin like https://counterparty.io and https://www.omnilayer.org. Even worse than requiring a full node, only archive nodes would be able to subscribe to new applications since each application would require an independent full parsing of all block data.

Further, interoperability between applications is difficult in this model. For Application A’s input to depend on the output of Application B, all users of A would be forced to parse all blocks under Application B’s rules along with A’s.

---

**maiavictor** (2018-12-06):

Interesting! That’s what meant by full nodes not being able to compute small proofs, making light clients impossible. I’m glad to just see that this actually works, even with some drawbacks! Just one consideration: if the hash function used to include the transactions on block headers was starks-friendly, wouldn’t it be feasible to produce short proofs of the result of `compute_dapp_state()`? That’d in turn allow for light clients, right?

Also, if anyone has a suggestion on how I could implement such log-only blockchain. Forking Bitcoin for that sounds like overkill because it has so many more features, having to deal with it all may be harder than just implementing it myself. So, currently, my best bet would be to do it, perhaps using libp2p to avoid having to deal with node discovery etc. which sounds like the most boring part. But if there is any existing project or shorter path to achieve this, please let me know.

---

**hkalodner** (2018-12-06):

Hmm that’s an interesting question. I don’t really know enough about the cutting edge of SN/TARks to say whether there’d be any way to make that computationally feasible, but it certainly seems theoretically feasible.

It should be possible to implement an application using this paradigm on either Bitcoin or Ethereum just using the blockchain as a dumb data store.

If your application doesn’t require more than 80 bytes of data per tx (or 220 with Bitcoin Cash) you can use `OP_RETURN` to store your data on Bitcoin. BlockStack is a great example of a company who has used that method.

Similarly, with Ethereum you could have a contract which just logged all data and then a client side application that just reads all the log data from a particular smart contract. However, if your application doesn’t depend on any of the capabilities of Ethereum, it could be overkill.

---

**maiavictor** (2018-12-06):

I see, using Bitcoin/Ethereum wouldn’t be that bad, but if there was a lightweight (Rust?) library that allowed me to do the same without the additional bloat, that’d work better. Thanks for the helpful comments!

---

**ldct** (2018-12-07):

You can find some old forum posts going in this direction by searching for “execution engine” or “state minimization”. e.g.: [State-minimised executions](https://ethresear.ch/t/state-minimised-executions/748) [Delayed state execution, finality and cross-chain operations](https://ethresear.ch/t/delayed-state-execution-finality-and-cross-chain-operations/987). Note that sometimes the posts are tightly coupled with sharding research.

The common starting point is the observation that any execution (including smart contracts) can be simulated on top of a “data-only” blockchain.

Some challenges I see with it though:

1. Without a native token, there is no in-protocol incentivization for validators and block producers. The idea of paying through a token whose balance is tracked by compute_dapp_state is similar to economic abstraction (https://medium.com/@Vlad_Zamfir/against-economic-abstraction-e27f4cbba5a7)
2. Requirement for a user to download all historical data, which might be much larger than the “current state” (e.g. UTXO set vs TXO set) as @hkalodner mentioned
3. At the protocol level, all historical data must be stored somewhere and the protocol “fails” if some historical state is completely deleted (stored by no one). In “stateful” protocols there is a smaller set of current state that nodes are required to store, we can delete things from the current state and incentivize/force people to do so e.g. via charging rent, hence controlling the storage requirements placed upon nodes.

---

**maiavictor** (2018-12-07):

1. The idea is that miners initially are mostly altruistic and just rank transactions by PoW by default. Eventually if some on-chain currency gets valuable, they can change their transaction ranking function to include compute_token_state(...).miner_rewards (assuming the token has a miner_fee field, and the contract sums all fees and places it on .miner_rewards).
2. As a starting poing, do we have statistical data of how large the Ethereum state is, and how large its transaction set is?
3. Do you mean a malicious miner could just not publish the transactions inside its block? That sounds like a huge problem. Why is that not a problem for Ethereum? Full nodes must see all transactions at least once. Can’t a miner not publish its transactions and make the network confused?

---

**ldct** (2018-12-07):

1. Yes, this is what I mean by paying fees through a token whose balance is tracked by compute_dapp_state
2. I think it is 2GB vs 100GB but I haven’t looked at it myself
3. No, I mean if some piece of historical data gets published and available, but at some future date people stop storing it, and then the data gets lost forever

---

**maiavictor** (2018-12-07):

Ah, obviously miners would just discard a block that doesn’t have its data available and then that branch wouldn’t grow. Makes sense to me. Thanks.


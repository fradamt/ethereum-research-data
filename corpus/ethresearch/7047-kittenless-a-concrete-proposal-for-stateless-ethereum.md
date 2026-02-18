---
source: ethresearch
topic_id: 7047
title: "Kittenless: A concrete proposal for stateless ethereum"
author: lithp
date: "2020-02-29"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/kittenless-a-concrete-proposal-for-stateless-ethereum/7047
views: 2277
likes: 3
posts_count: 3
---

# Kittenless: A concrete proposal for stateless ethereum

I think it’s been difficult to follow some of the conversations about stateless ethereum, because there are so many different proposals and it’s difficult to think about how they tie together. I hope that having a set of concrete named proposals will help with that. To that end, here’s a Least Ambitious Proposal, a Little Baby Stateless Ethereum, Kittenless:

1. Stateless clients look just like full nodes today, except they do not download the state trie. In order to sync they must download the header chain and block bodies, as full nodes do today. (It’s not really “stateless”, it’s “less state”)
2. In order to support stateless clients a new version of the eth protocol is launched, eth/66. Most messages are the same, but it does not have GetNodeData. State is fetched using a different mechanism, described below.
3. When miners create a block they also create a witness for that block. The witness specifies a subtree of the state from the previous block. It contains every part of the state tree which is read from or written to by the transactions in the block. Block headers include an additional field, the hash of the witness.
4. There’s a new block propagation rule, peers will only propagate blocks which are accompanied by a witness. (In the eth/66 subprotocol the NewBlock message includes a field which contains the witness)
5. Transactions look almost exactly as they do today. However, nodes do not accept them unless they’re accompanied by a witness proving the sending account. An affordance for this is made in eth/66.
6. Somehow, we migrate the account trie from the patricia tree to a binary trie. This will reduce witness sizes.
7. Somehow, we merkelize contract bytecodes. Witnesses only include the parts of the bytecode which are actually touched. This also reduces witness sizes.
8. We add a gas cost. Transactions must pay an amount proportional to the number of accounts and storage items and bytes of code they touch. This gas cost is set such that the witnesses are bounded to a reasonable size, at most 1MB?
9. There’s a new subprotocol, state/1, which nodes can use to fetch chunks of state (Geth calls these tiles) from each other. Both full nodes and stateless clients use this protocol to fetch state, stateless clients just fetch less state.
10. In the state/1 subprotocol each node advertises a list of chunks which they store, and the protocol provides a method of looking up which nodes store a given chunk. Nodes can request chunks from each other. All chunks are sent along with proofs which can be used to verify them. As blocks are added to the chain each node updates the chunks they store locally. The witness for each block is enough to update chunks. However, nodes must be careful to properly handle reorgs. A witness is not sufficient to undo changes to a chunk, when updating chunks the node must store some additional data it can later use to undo changes, if necessary.
11. There is a social convention that nodes which have fetched a chunk must advertise it until they’ve served it to at least one other node. Full nodes will automatically follow this rule, they’ll always serve the entire state. Stateless clients might provide some kind of feedback to the user: “The current ratio of uploads to downloads is below 1, please continue running the node until the ratio is above 1”. Stateless clients will not support any features likely to break this invariant. Most notably:
12. eth_call does not work unless you are running a full node, or your stateless client already has access to all the state necessary to service the request. Stateless clients do not attempt to fetch missing state from the network. eth_call is a fundamentally expensive operation and if you want to do it you should pay someone to do it for you.
13. There’s a second social convention: When fetching state, nodes prioritize fetching state from stateless clients (which which aren’t advertising “I have everything”). This reduces the load on the full nodes, who are only asked to serve state which no stateless clients are serving.

You can see that even though I’ve called this “Least Ambitious” some of these bullets are still rather ambitious. Am I missing anything that would prevent this from working? Is there a way to simplify it even further?

## Replies

**carver** (2020-03-03):

I wonder who would use this kind of node. Sending transactions would typically require an `eth_estimateGas` execution, which uses a call under the hood.

I guess people who are interested in watching for event logs on chain, but not accessing arbitrary state? Or maybe application-specific nodes, which are some kind of stateless hybrid. They might download all the storage needed for a particular application or two, but run stateless on the rest. That seems to be supported by this model. Do any other use cases come to mind?

---

**lithp** (2020-03-05):

Ah, good point, I had forgotten that sending transactions means first calling `eth_estimateGas`. Well, changing `eth_call` is still possible, it doesn’t change this proposal much to allow it. I had disallowed it because it feels a little dangerous, there’s an incentive to drop the state you only fetched to service an `eth_call`, especially if your future `eth_call`s touch enough state that your LRU cache fills up.

> I guess people who are interested in watching for event logs on chain, but not accessing arbitrary state? Or maybe application-specific nodes, which are some kind of stateless hybrid. They might download all the storage needed for a particular application or two, but run stateless on the rest. That seems to be supported by this model. Do any other use cases come to mind?

These two were exactly what I had in mind!

(1)  In Kittenless a dapp developer who only wanted to follow logs could easily start and stop and failover between nodes without needing to do anything more expensive than syncing the header chain.

(2) And absolutely, Kittenless supports partial state sync; nodes which want to follow specific parts of the state. Cryptokitties developers (or anyone who wants to run analytics over cryptokitties) can run a  stateless node and ask it to download (and seed) just the cryptokitties state. Same with people interested in DeFi who want to follow the current state of e.g. the Uniswap contract.

(3) End users also have a use for this. I have a hardware wallet which can sign transactions, but I also have a [watch-only wallet](https://bitcoinelectrum.com/creating-a-watch-only-wallet/) which I run on my laptop to inspect the current state of my bitcoin addresses. You can run a stateless node and have it download the chunks which contain the accounts you care about, and it’ll tell you all the transactions those accounts have made and their current balances. You can do this without needing to rely on a server, your node is fully verifying the chain, which is actually better than the Bitcoin equivalent! Though, the lack of `eth_call` means you’d need to talk to a server in order to send transactions, which introduces a privacy risk.

(4) Exchanges might choose to run these clients. They’re not really interacting with smart contracts, just sending and receiving ETH. The exchanges which support ERC20 tokens usually support an enumerated list of those tokens, they could choose to run clients which hold onto just the state for those tokens. I think this this gives them everything they would want:

- stateless clients follow the chain and verify all transactions, the security model is the same
- stateless clients could still sign and send transactions, as long as you’re just doing balance transfers

(5) Most (all?) of [etherscan.io](http://etherscan.io) could be powered by a stateless node. The Etherscan database, which powers the website, could very naturally be the result of a `reduce` over the stream of block witnesses, each witness making a change to their database. I’m doing a little sleight of hand here, the state it also the result of running a `reduce` over the witnesses! But after browsing the website a bit, I don’t see anything which requires having the entire state around.

In summary, I think this supports most use-cases! Some of the things it can’t support are:

- Running eth_call (and creating) transactions which might involve many interactions between unpredictable contracts. Admittedly, this is a big part of what makes ETH valuable, it’d be annoying if you had to run a full node or trust some web server in order to do it.
- Tiny clients which often go online and offline (mobile apps, web browsers)


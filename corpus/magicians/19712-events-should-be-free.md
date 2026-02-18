---
source: magicians
topic_id: 19712
title: Events Should Be Free
author: yulesa
date: "2024-04-19"
category: Magicians > Primordial Soup
tags: [evm, opcodes, events]
url: https://ethereum-magicians.org/t/events-should-be-free/19712
views: 1251
likes: 7
posts_count: 9
---

# Events Should Be Free

# Events Should Be Free

## Introduction

Permissionless access to data is one crucial aspect of social consensus. The motto of blockchains, “Verify, don’t trust!” tells you exactly that. DeFi apps today are not based on faith; they prevail because anyone can validate them. At any point in time, you can evaluate their trust assumptions, see how much liquidity, collateral, and debt they have, and make them accountable.

*“Ethereum is the world’s settlement layer not because it has the largest economic security, but because it’s the largest verifiable blockchain”*

https://twitter.com/gluk64/status/1770910189572501954.

Events, or Logs, are the primary data source of Ethereum (and other EVM chains). Most analytics websites, Dune dashboards, and crypto reports are created using events as the most basic data primitive. Events are then transformed, combined, and grouped to create a metric in a chart or a table. Events are the building block of crypto data but are at risk of being undermined. To explain why this is happening, we need a good understanding of events’ inner workings.

## How do events work?

Skip this part if you have a good understanding of how events work.

Events or Logs in EVMs are similar to code logs in any language. It’s one line in the code that, when the execution stumbles at it, will write the desired execution information in a ledger. A log record is used to surface information about a smart contract execution, like a token transfer or a change of ownership, so that it can be easily retrieved.

[![emit](https://ethereum-magicians.org/uploads/default/optimized/2X/e/ede0a57073bf202d5c5284861c2a5c6eb256e30c_2_690x295.jpeg)emit2000×856 296 KB](https://ethereum-magicians.org/uploads/default/ede0a57073bf202d5c5284861c2a5c6eb256e30c)

*Example of the UniswapV3Factory contract code, which will emit the PoolCreated Event every time a pool is created. You can calculate how many pools Uniswap has by counting how many PoolCreated Events were emitted. Source: [Uniswap V3: Factory | Address: 0x1f98431c...6ea31f984 | Etherscan](https://etherscan.io/address/0x1f98431c8ad98523631ae4a59f267346ea31f984#code)*

In Ethereum, event outputs are written in the transaction receipts, together with some other information about the transaction outcome. Every node in the blockchain stores transaction receipts in the blocks. The back-end of analytics websites and data providers can then request the transaction receipts from any node and use this information to create the desired metrics.

The solidity code is not what is stored in the blockchain. The function emit is compiled to a LOG opcode, and the node implementation dictates the contract execution flow when the LOG opcode is called. A block also includes some extra metadata to improve efficiency while querying receipts.

In conclusion, retrieving data from events is much simpler than sourcing it from the state trie (Ethereum memory) while also allowing the retrieval of historical data, a much more complex task when using other sources since the state trie is constantly updated; you usually only have access to its latest state.

This blog post from MyCrypto provides an excellent, in-depth explanation of events:

https://medium.com/mycrypto/understanding-event-logs-on-the-ethereum-blockchain-f4ae7ba50378

## The issue

Events come at a cost. Each event incurs a minimum of 375 gas, with an additional 375 for each topic (32 bytes of indexed data) and eight gas for each byte in data (unindexed data). For instance, a Transfer event adds 1756 gas to the operation, while the entire transfer operation costs between 40,000 and 60,000 gas. The event emission cost is paid by the user when making a transaction.

Because Ethereum is now expensive, this cost factor has led to discussions about making L1 transactions more affordable. Even though events represent a small fraction of a transaction cost, developers are already considering their removal, so their users don’t bear this cost. This creates a massive issue for data providers, leading them to centralized alternatives.

[![hayden](https://ethereum-magicians.org/uploads/default/optimized/2X/2/2c936f2231d1d3a551263c8ed2069c8d553848a0_2_587x499.jpeg)hayden1920×1635 85.9 KB](https://ethereum-magicians.org/uploads/default/2c936f2231d1d3a551263c8ed2069c8d553848a0)

*Heyden Adams, CEO of Uniswap, is polling about event removal in the next version of Uniswap. Even though the X poll is not a trustworthy source of truth, the fact that they consider it is troublesome. Uniswap V4 without events could tip the bucket to centralized solutions. Source: https://twitter.com/haydenzadams/status/1775907308372922464*

Events solve two different problems. The first is obvious: easy access to execution data. Events store extra information in the receipts, making this data much more accessible. However, a second, often neglected, issue events solve is data curation. Knowing what to store is a challenging task. The blockchain generates an abundance of data, which can become overwhelming and hinder the ability to extract meaningful insights. Data curation is more suitable for those developing the protocol and deeply understanding its inner workings. When devs remove the events, they push this task to everyone further down in the data manipulation process. This is critical.

Most alternatives to events are burdensome or rely on centralized data providers. Call traces, another outcome from transactions that are also decentralized, provide very limited access to execution data, and the actual state needs to be reconstructed from input parameters. This path is impractical, as any crypto data analyst who has ever tried it can attest, and it won’t be pursued given available centralized alternatives. Events can also be emulated by proprietary customized nodes that modify the deployed contracts and add fictitious events to the code. This approach requires centralized infrastructure to rewrite code, re-execute the blockchain, and deliver indexed events to consumers.

## Potential Solutions

Events should be free. Even though end-users consume dashboards and charts, they shouldn’t bear the cost directly at each transaction. Events cost gas because every node needs to handle and store them in the receipts. Nodes would get bloated with useless events if they were free or much cheaper. We need to make log manipulation and storage optional. With free events, developers don’t need to remove them from their code, still maintaining the curation by protocol engineers and permanently written in the contract. Events are kept decentralized, although optional to anyone who wants to make use of them later.

How can we do it? It’s time for an open-source node implementation dedicated to data applications. The initial “data node” MVP can be a fork of current execution nodes with some extra functionalities to handle data. In its most straightforward configuration, it will be responsible for treating the current events that exist today. This solution not only addresses the issue of event costs but also provides a platform for developers to freely manage and store crypto data in a format more suitable to their needs.

The rationale is that if you’re a home-staker, you probably don’t care about storing events since you won’t do much with them and can run the existing node. Conversely, if you run a node to power some UI, you could care only about the events emitted by the protocol’s contracts in the UI. Lastly, if you’re a data provider, you care about most contracts and would store all; ultimately, this is part of your business anyway.

We would also need to modify the current execution nodes. One alternative is implementing new opcodes for fictional/free events (Mnemonic FLOG) and keeping the current LOG opcode. FLOG would be ignored entirely by regular nodes. Still, on a “data node”, it would act similarly to the regular LOG opcodes, adding their output to some data structure (maybe in the same receipts) and indexing the relevant fields. Solidity compilers must also introduce functions and syntax that would be compiled to the new opcode. This proposal does not affect already deployed contracts, which would still spend gas on transactions. Only new contracts using the new opcode would benefit. Furthermore, it allows the ability to code payable events when necessary (a swap can have a free event, but a set_new_fee function can pay for it, storing it at every node). Alternatively, we can repurpose the current LOG opcodes to be free and ignored by regular nodes and make new opcodes for payable events that would follow the current log implementation.

Other considerations must be made. Free events could be a potential vector for spammers’ contracts and others to abuse. Data consumers will require extra functionalities, like the ability only to track events from some contracts, some type of contracts ignore lists, or even some additional indexing. The “data node” team would be responsible for making design considerations providing the new customers of this node, data providers.

One last alternative is to have special comments in solidity for fictional events. It doesn’t require any node change and keeps the curation by protocol developers, but it has the drawback that comments are not compiled to opcodes and, thus, are not deployed at the blockchain. The “data node” would only be able to act on it if it has access to this contract solidity source code, also needing re-execution of the new compiled version of the contract with the free log. Also, there is no guarantee that events are the same, as there is no way to verify comments onchain.

[![standards](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9095916513c041989ea6ff2e5574a7e391713738_2_690x391.jpeg)standards2000×1134 228 KB](https://ethereum-magicians.org/uploads/default/9095916513c041989ea6ff2e5574a7e391713738)

## Conclusion

Simply removing events from the code is a terrible decision. It pushes UI development and analytics to proprietary products and platforms, centralizing the data-provider supply chain. Existing alternatives to events, like traces, are limited, burdensome, and onerous. However, protocol developers are also correct in trying to remove costs from their users. The only way to fight this tragedy of the commons situation is for the community to step forward and advocate for open-source, decentralized solutions. The existing data providers could also step forward and sponsor this idea, as their business relies entirely on that.

## Replies

**matt** (2024-04-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yulesa/48/7196_2.png) yulesa:

> How can we do it? It’s time for an open-source node implementation dedicated to data applications. The initial “data node” MVP can be a fork of current execution nodes with some extra functionalities to handle data. In its most straightforward configuration, it will be responsible for treating the current events that exist today. This solution not only addresses the issue of event costs but also provides a platform for developers to freely manage and store crypto data in a format more suitable to their needs.

A single client isn’t sufficient to change the cost of something. The cost is usually determined by the worst case scenario on the least performant client. If you want to modify the cost of events, you should will need to convince all clients to not store the data. Unfortunately they’re part of the receipts which clients currently do not prune. We’re working on pruning with EIP-4444, but until then there won’t be much progress on this front.

Alternatively, you can make the case that events are over priced. Do some analysis on how much computation the bloom filter takes in the worst case and how much data the node is forced to store in the worst case. Run some benchmarks, then propose an EIP on ACD backed by that data.

---

**mratsim** (2024-04-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yulesa/48/7196_2.png) yulesa:

> Because Ethereum is now expensive, this cost factor has led to discussions about making L1 transactions more affordable. Even though events represent a small fraction of a transaction cost, developers are already considering their removal, so their users don’t bear this cost. This creates a massive issue for data providers, leading them to centralized alternatives.

The Graph is a very popular decentralized alternative for analytics with strong traction.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yulesa/48/7196_2.png) yulesa:

> Events solve two different problems. The first is obvious: easy access to execution data. Events store extra information in the receipts, making this data much more accessible. However, a second, often neglected, issue events solve is data curation. Knowing what to store is a challenging task. The blockchain generates an abundance of data, which can become overwhelming and hinder the ability to extract meaningful insights. Data curation is more suitable for those developing the protocol and deeply understanding its inner workings. When devs remove the events, they push this task to everyone further down in the data manipulation process. This is critical.

The Graph has a rewarded Curator role. It’s a market.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yulesa/48/7196_2.png) yulesa:

> Most alternatives to events are burdensome or rely on centralized data providers. Call traces, another outcome from transactions that are also decentralized, provide very limited access to execution data, and the actual state needs to be reconstructed from input parameters. This path is impractical, as any crypto data analyst who has ever tried it can attest, and it won’t be pursued given available centralized alternatives. Events can also be emulated by proprietary customized nodes that modify the deployed contracts and add fictitious events to the code. This approach requires centralized infrastructure to rewrite code, re-execute the blockchain, and deliver indexed events to consumers.

Centralized data providers require you to pay (see Google BigQuery) or alternatively you can run an archive node.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yulesa/48/7196_2.png) yulesa:

> Events should be free. Even though end-users consume dashboards and charts, they shouldn’t bear the cost directly at each transaction. Events cost gas because every node needs to handle and store them in the receipts. Nodes would get bloated with useless events if they were free or much cheaper. We need to make log manipulation and storage optional. With free events, developers don’t need to remove them from their code, still maintaining the curation by protocol engineers and permanently written in the contract. Events are kept decentralized, although optional to anyone who wants to make use of them later.
>
>
> How can we do it? It’s time for an open-source node implementation dedicated to data applications. The initial “data node” MVP can be a fork of current execution nodes with some extra functionalities to handle data. In its most straightforward configuration, it will be responsible for treating the current events that exist today. This solution not only addresses the issue of event costs but also provides a platform for developers to freely manage and store crypto data in a format more suitable to their needs.

In that case, events are not part of the blockchain anymore. So you have a second “log blockchain” that runs in parallel with the first one and there is a new issue, how to verify that the logs are correct, how to ensure data availability, how to ensure spam resistance/DoS protection or logscriptions or prevent the creation of malicious data cartels?

Another consideration is regarding the Verge roadmap, if we want snarkifying the EVM and the EVM-in-EVM opcode, it’s easier if we have a single blockchain.

Relevant: [Using The Graph to Preserve Historical Data and Enable EIP-4444 - Execution Layer Research - Ethereum Research](https://ethresear.ch/t/using-the-graph-to-preserve-historical-data-and-enable-eip-4444/)

---

**yulesa** (2024-04-19):

Hey [@matt](/u/matt) , thanks for taking the time to reply to my post. I’m a huge fan of your work. Let me address your point.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> A single client isn’t sufficient to change the cost of something. The cost is usually determined by the worst case scenario on the least performant client. If you want to modify the cost of events, you should will need to convince all clients to not store the data.

That’s precisely my proposal. Regular nodes should completely stop processing and storing logs. However, we also need to provide an alternative for data consumers and providers, and that’s why we need a “data node”. At the same time, I want to encourage protocol developers to keep the event `emit` in their code because I see it as the highest value and worth of decentralization (stored by every regular node).

The way I think about the future of decentralized data is that you need to evaluate the value density of every individual piece of data. Let me describe what I mean by that.

Every data you store has a potential benefit: the value share you can attribute to it after you combine it with all the other pieces that turn it into a metric and extract information from it.

On the other hand, data also have costs attributed to it. This is usually associated with the effort you must put into the transformation process. A piece of data you need to decode, clean, and store in large quantities has a higher cost than the readily servable ones.

We can define high-density data as data that has high value and low cost. Low-density data are only profitable with economies of scale, and that’s the advantage of centralized data providers.

I see logs as the highest-density data primitive, while traces are very low-density since they will have a high cost to reconstruct state from input params. So high that I even think they have negative value and no data provider will use them to derive metrics, they will look at other paths.

The elephant in the room is that decentralization has a cost. When every transactor needs to pay the gas cost of the event, you’re making it infeasible, even charging the wrong actor for it. Reducing the event’s gas costs, as you suggest, won’t be enough. We need to transfer the cost to data providers by requiring them to maintain a dedicated node, address spammers, and decide what to store. I prefer hundreds of data providers, all having cheap access to logs and competing to serve their clients, than to have the logs stored at ten thousand nodes, most not doing anything with them.

I’m glad event pruning is being considered with EIP-4444, but I hope it has alternatives for the ones that require it.

---

**yulesa** (2024-04-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mratsim/48/2872_2.png) mratsim:

> The Graph is a very popular decentralized alternative for analytics with strong traction.

I’m very familiar with The Graph. I see them doing a different crusade with their subgraphs; where they decentralize the storage of “transformed” data and metrics and not primitive data. I really like how subgraphs make the transformation code public, but I’m not so strong about decentralizing the storage of transformed metrics. Consumers have different perceived values of it (see my reply above), and it’s hard to find multiple customers who justify the decentralized storage. Their business was convenient while they were subsiding storage and API with the “hosted service”, while it’s still to determine whether it can withstand the decentralized service. Substream hasn’t gotten traction yet, and I think even though it has access to more primitives, they might have increased the engineering cost too much with Rust.

I would really enjoy if The Graph pivoted to a “data node” core developer or maybe funded it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mratsim/48/2872_2.png) mratsim:

> Centralized data providers require you to pay (see Google BigQuery) or alternatively you can run an archive node.

True, nothing is free. Someone needs to pay the cost and the whole process needs to be net positive. As I said above, I prefer hundreds of data providers, all having cheap access to logs and competing to serve their clients, than to have the logs stored at ten thousand nodes, most not doing anything with them.

I also see archive nodes as very-low density. Past state is huge, really hard to decode, and very difficult to curate what you need. Not surprising it’s mostly used by centralized data providers.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mratsim/48/2872_2.png) mratsim:

> In that case, events are not part of the blockchain anymore. So you have a second “log blockchain” that runs in parallel with the first one and there is a new issue, how to verify that the logs are correct, how to ensure data availability, how to ensure spam resistance/DoS protection or logscriptions or prevent the creation of malicious data cartels?

It’s still the same blockchain. I’m defending that events’ codes should still be stored in the deployed contracts; it’s just some nodes are not processing it in the same way as others (like some nodes have pruning turned on and others don’t). I just don’t think the same team (geth) should be addressing the data needs.

You can verify that the logs are correct because they’re still in the deployed code, and availability is ensured by the ones running the “data node” version.

Spam resistance/DoS protection requires more study. You still need to pay the transaction gas cost, even though the event share is free. This will deter some spamming. Some spamming protection can also be implemented “post emission.” Ie. “Data nodes” could have configs to reject logs from contracts that did not spend at least some minimum amount of gas in the contract deployment or reject logs from transactions that the total cost was less than the X thounds gas.

---

**jtriley-eth** (2024-04-19):

I like the idea of making logN log appends optional through an eip, treating each as a no-op that pops the N+2 args, and potentially expands memory as it does now.

Though this *does* imply a new class of nodes specifically for indexing these events, so deciding on pricing isn’t obvious here. Non indexer nodes simply pop values off the stack, so a low base gas cost with the dynamic gas cost depending on whether the opcode expands memory seems reasonable. For indexer nodes, though, this does enable log spam. Measuring the material difference in resources is straight forward here, but determining the percentage of indexer vs non-indexer nodes should be a factor as well as whether the expectation is to keep the barrier to entry for new indexer nodes low in the future.

Of course, I’d like indexer nodes to be accessible to indie shops, but it wouldn’t be strictly necessary for consensus in this case, so I can understand why it wouldn’t be optimized for indie shops. Open to more thoughts on this though.

---

**yulesa** (2024-04-19):

Don’t you think it could be free? Log spammers would still need to pay the transaction fee, and client configurations could be used to filter them out. I have no experience with this.

Would you prefer to completely remove the log append implementation or create new opcodes that do not append and just pop args? If you prefer to create new opcodes, would you keep the current logN as it is or change it to be the one that just pops values?

Just the communication that removing it from consensus is being considered would strongly incentivize the creation of an indexing node and team. If it’s not part of the consensus, all clients simply pop the values, but with the opcode still existing, all data providers would need to plan a fork of the client code and keep the opcode implementation as it is today. Further, they can implement some other improvements to better suit their needs.

---

**jtriley-eth** (2024-04-19):

I’d argue against free because even the 2 gas opcodes perform *some* action, which costs computational resources. At the time of writing, EOF is not live, so there’s no guarantee the stack won’t underflow, which adds a branch on each instance of logN to check for stack underflow. In either case, it requires the node to access memory to pop the values. This cost is diminutive but nonzero nonetheless.

There’s also the memory expansion dynamic gas associated with logN in the case the memory pointer + length is greater than the current memory size. This *must* still exist even if the opcode performs no external actions, as this would otherwise open a DoS vector for indexers (memory bombing) and any contracts depending on msize would diverge in execution between indexer and non-indexer nodes.

Assuming we aren’t concerned with indexer node centralization, I would price the gas cost as follows:

```py
# logN(.., ptr, len)

base_gas = 2

mem_expansion = (ptr + length - msize) if msize < (ptr + len) else 0

dynamic_gas = mem_expansion * 3 + mem_expansion**2 // 512

log_n_gas = base_gas + dynamic_gas
```

This is the current minimum nonzero base gas cost with dynamic memory expansion gas cost in accordance with the execution spec’s [current logN behavior](https://github.com/ethereum/execution-specs/blob/744904ebd0ba8c9ce5ae7c5ee9bef3c5d21a38f9/src/ethereum/cancun/vm/instructions/log.py#L33) and [memory expansion gas costs](https://github.com/ethereum/execution-specs/blob/744904ebd0ba8c9ce5ae7c5ee9bef3c5d21a38f9/src/ethereum/cancun/vm/gas.py#L154).

---

**Eikix** (2024-05-11):

Hey all!

Thanks for taking the time to write a detailed overview of the situation.

I liked the idea of removing log blooms altogether (they constitute the majority of costs for logs afaik) and work with a parallel p2p log ledger, c.f. VB’s notes on this (it seems I can’t add links to my post?)


---
source: ethresearch
topic_id: 19606
title: EVM Native Sequencing Rules
author: Lilyjjo
date: "2024-05-22"
category: Execution Layer Research
tags: [mev]
url: https://ethresear.ch/t/evm-native-sequencing-rules/19606
views: 5964
likes: 16
posts_count: 9
---

# EVM Native Sequencing Rules

The goal of this post is to introduce the concept of Sequencing Rules and provide a possible sketch of what a Sequencing Rule-enabled EVM would look like. Sequencing Rules offer a rational solution to both Ethereum’s MEV and protocol innovation mindshare loss problems.

## Sequencing Rules: The Why

Ethereum is facing a MEV crisis. FUD is [building on Twitter](https://x.com/dankrad/status/1791379755922498027) as block builders grow in their influence over the chain’s functioning. Block builders are collecting an [uncomfortable amount of capital](https://www.relayscan.io/builder-profit?t=7d) with each block, yet they provide little to negative value in return. This behavior makes sense: value has been left on the table, so why shouldn’t they collect it? A rational way to stop the growing block builder oligopoly is to enable Ethereum’s on-chain applications to fully capture the value that they create.

So far, discussions on fixing block builders’ power have focused only on lower-level structural L1 changes[1](https://ethresear.ch/t/execution-tickets/17944),[2](https://ethresear.ch/t/state-lock-auctions-towards-collaborative-block-building/18558),[3](https://ethresear.ch/t/exploring-paths-to-a-decentralized-censorship-resistant-and-non-predatory-mev-ecosystem/17312), leaving out the actual source of value creation and leakage: the on-chain applications themselves. The best entity to decide how to fairly distribute the value created from ordering is the entity that is producing the value. For the sake of Ethereum’s long-term success, on-chain applications need to be able to express and control how their transactions are sequenced with supporting L1/L2 infrastructure.

The rest of this post will:

- Introduce the concept of Sequencing Rules
- Provide a sketch of what native EVM sequencing support could look like
- Provide a proof-of-concept example of an AMM that auctions off the right of the first swap on Ethereum

## Sequencing Rules: The What

Sequencing rules are not a new concept but have recently seen increased usage by blockchain developers.

Sequencing rules can be conceptualized as follows:

1. On-chain applications decide how they want their transactions to be sequenced.
2. Blocks are built that respect that sequencing.

Blockchain applications can benefit from this programming pattern due to blockchains’ inherent discrete view of time. During the 12 seconds between Ethereum’s blocks, the outside world’s valuation of different pieces of state is in flux, creating arbitrage value in the ability to act first on those pieces of state. Block builders make money by exploiting this in the form of acts like CEX-DEX arbitrage. This phenomenon is also observed in traditional finance (TradFi) with the [high-speed arms race](https://academic.oup.com/qje/article/130/4/1547/1916146) between high-frequency trading (HFT) firms, which operate in a similar scenario but on a millisecond timeframe instead of seconds.

As the field of protocol development matures, protocols are starting to manage these value-pressurized pieces of state with varying degrees of success. Examples vary but all showcase the benefits of managing one’s own sequencing:

- Penumbra, a new L1 DEX, enforces ordered batch execution of all business logic, enabling all users to benefit equally from the accrued time arbitrage value.
- HyperLiquid’s new L1 prioritizes retail and makers over toxic takers by running cancels and post-only orders first.
- Skip’s Slinky project surfaces oracle data at the block level to ensure all applications can utilize fresh oracle data.
- Oval auctions off the right to be the first person to act on updated oracles information.
- Years of research1,2,3 have been conducted on how to implement first-swap auctions for AMMs on Ethereum, though no production-grade result is running yet.

Sequencing rules for blockchain applications are natural, yet Ethereum does not offer native solutions to enable developers to program their applications accordingly.

## Sequencing Rules: The How

As seen in the list above, protocols are starting to migrate to other ecosystems with novel L1 implementations because their sequencing needs are not being met on Ethereum. Instead of Ethereum’s on-chain protocols capturing the time-accrued value, block builders are. Ethereum’s EVM needs sequencing rules.

Ethereum’s EVM programming environment is different from an L1 that is specialized for a specific application because it is a shared general execution environment. Applications and transactions share both block space and state with each other. As a result, anyone implementing sequencing rules for an EVM should consider:

- On-chain applications cannot assume a piece of state’s value will not change unless it is explicitly controlled.
- Not all on-chain applications need sequencing.
- Not all actions within an application need sequencing.

I will now lay out a rough draft version of how one could implement sequencing rules for Ethereum. In order to meet the above considerations, I propose adding two new transaction types:

1. A new ‘bundle’ transaction type. This transaction would be signed by an EOA and would contain a payload of ordered transactions. We’ll call this EOA a bundler. This ‘transaction’ itself does not trigger on-chain execution, it simply just orders other transactions.
2. A new transaction type that specifies the bundler (just an EOA) that is able to include the transaction in a bundle.

[![IMG_0025](https://ethresear.ch/uploads/default/optimized/3X/b/3/b376ab484f0a2eaa09bcb254d7f12439f442621d_2_689x500.png)IMG_00253239×2350 261 KB](https://ethresear.ch/uploads/default/b376ab484f0a2eaa09bcb254d7f12439f442621d)

EVM block construction would be modified to enforce the following rules:

- A bundler can only have a single bundle transaction included in a block, and optionally, a bundle is only valid in a certain block. Some business applications would benefit from being able to run bundles in only certain blocks.
- A bundle can specify a bundler that is able to include it in a bundle, for meta-bundle programming.
- A transaction can only be included in a bundle if it specifies bundler, and if a transaction specifies a bundler, the transaction can only be included in a block if it is in a bundle. This is to prevent bundles from clashing with each other, which would cause builders to have extra incentive to include one bundler over another.
- Unlike Ethereum’s current block builder’s bundle interface, transactions in a bundle do not have any non-revert guarantees. On-chain application logic must handle possible reverts. This is again to prevent bundles from clashing with each other.

The EVM itself would be modified to include the new following global variables:

- bundle.signer: the EOA who signed the bundle. Useful for on-chain applications to designate sequencing rights to a specific off-chain entity. The zero address if not in a bundle.
- bundle.number: the global number of the bundle’s ordering. Useful for meta-bundle programming. Zero if not in a bundle.
- bundle.tx_number: which number this transaction is in the bundle. Useful for on-chain applications to enable special logic depending on transaction sequence. Zero if not in a bundle.

These new EVM rules and global variables could be a strong starting point for on-chain applications to express how they’d like to be sequenced.

There are numerous security and caveats to consider in this implementation. EVM bundle creators would need to take care to only sequence on state that they directly control from the start of the block. This is because all other state is potentially manipulatable by outside entities. Bundle creators would have to assume that all transactions could revert due to insufficient gas funds, that any piece of unprotected state could be changed, and that any starting point besides its own external functions are non-deterministic. Sequencing rule assumptions about mutable state could be a new class of audit vulnerabilities.

Additionally, these rules or language expansions do not preclude block builders existing or making money. Bundlers could construct multiple bundles and rely on block building services to take advantage of the highest result. Inter-bundle arbitrage could be a new solver target. Analogous to the EVM global variables proposed above, `tx.number` could be included to allow block builders to explicitly sell the right to be the first transaction included.

Notably, this implementation lacks specification on how on-chain applications would construct bundles. This would be up to the applications to chose between different trust and privacy tradeoffs. Some options would include using:

- Flashbot’s Suave TEE enabled decentralized platform for business applications needing confidential compute.
- A sequencing layer, like Astria, to construct generic bundles.

## Sequencing Rules: An Example

I came up with the above Ethereum compatible sequencing rule proposal while trying to program a [first swap auction for a AMM on Ethereum](https://github.com/Lilyjjo/tldr-research). This proof of concept aims to implement the sequencing rule ‘the first swap should be auctioned’ for the sake of rerouting some of the CEX-DEX arbitrage back to the pool’s LPs. It utilizes block builder’s current [bundle infrastructure](https://docs.flashbots.net/flashbots-auction/advanced/rpc-endpoint#eth_sendbundle) to craft bundles and inserts logic on-chain via a signed transaction to enforce that the bundle’s sequence is respected. This proof of concept uses Flashbot’s SUAVE TEE enabled programming environment to craft bundles for the AMM in a trust-reduced manner. This implementation could be easily rewritten with the above EVM native bundle proposal with much better execution costs and guarantees.

I wrote this post because I’m a frustrated protocol developer who wants to capture the maximal value for my actual users. These are just my thoughts on how we can potentially make “Ethereum Great Again” ![:green_heart:](https://ethresear.ch/images/emoji/facebook_messenger/green_heart.png?v=14)![:blue_heart:](https://ethresear.ch/images/emoji/facebook_messenger/blue_heart.png?v=14)![:sparkles:](https://ethresear.ch/images/emoji/facebook_messenger/sparkles.png?v=14).

Please leave comments if you have them!

Thank you to my teammates [Itamar](https://x.com/itamarreif) and [Vishesh](https://x.com/visavishesh) at [Astria](https://x.com/AstriaOrg) for agreeing to talk about auctions for way too long, [The Latest in Defi Research](https://x.com/thelatestindefi) for providing the community to iterate on these thoughts, and to the Suave team for letting me learn how to build bundles on their platform.

*Note: these @'s have no endorsement or involvement in this post, these words and opinions are my own :).

## Replies

**hdevalence** (2024-05-22):

This is a great post!

One suggestion I would have for the `bundle_tx` design would be to provide equivalent functionality to ABCI’s `BeginBlock` and `EndBlock` handlers. To recall context from the Cosmos ecosystem that may not be familiar:

- ABCI (Application BlockChain Interface) is the API used by the consensus engine to drive the state of the application it’s replicating;
- The original ABCI method flow looked like: BeginBlock, (repeated) DeliverTx, EndBlock, Commit.
- Applications can add custom behavior to BeginBlock and EndBlock that executes at the top or bottom of the block.

This is very useful because it allows applications (contracts) to operate on groups of transactions with their own custom logic. For instance, a contract that wants to handle all users’ interactions at the “same time” within a block can be structured so that the individual txs enqueue messages and the `EndBlock` handler processes them all and writes the outputs.

It would be useful to have the `bundle_tx` be able to provide similar functionality, with calls to `begin_bundle` and `end_bundle` hooks (which might be no-op’s by default).

---

**thogard785** (2024-05-22):

Great post! From one app developer to another, I understand your frustration.

While I acknowledge that there are some strong benefits to an ‘in protocol’ solution like what you describe, execution abstraction is an alternative path thats available now and allows for the vast majority of the benefits of app-defined sequencing.

Take a look at the Atlas whitepaper [here](https://github.com/FastLane-Labs/atlas_whitepaper/blob/f5e50043c0fb7e340291c51ea3f6ab591904d316/Atlas_Whitepaper.pdf) to learn more.

Fun fact - a year ago we actually built out an example of running a top of block (first trade in block) stat arb auction to return MEV / LVR to a uniswap V4 pool. I believe it’s still in the repo, albeit not production ready. If you’re interested, I’d love to collaborate with you on the subject.

---

**0xTariz** (2024-05-23):

Interesting post! I have a few questions ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

![](https://ethresear.ch/user_avatar/ethresear.ch/lilyjjo/48/13547_2.png) Lilyjjo:

> a payload of ordered transactions

Who and when is the order of transactions determined in the payload of ordered transactions that a bundler includes? - I understand that the application specifies this before the transactions are included in the mempool. Is my understanding correct?

I’m curious about how it is verified that a bundler has not included the transactions in the designated order in the bundle. Are you also considering a slashing model for them?

![](https://ethresear.ch/user_avatar/ethresear.ch/lilyjjo/48/13547_2.png) Lilyjjo:

> IMG_00253239×2350 261 KB
>
>
> IMG_00253239×2350 261 KB

It seems to me that builders could target bundles for sandwich attacks in a similar way they target individual transactions. Am I understanding this correctly? For example, targeting a yellow bundle_tx with green tx and red tx for a sandwich attack.

---

**Lilyjjo** (2024-05-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/hdevalence/48/16353_2.png) hdevalence:

> It would be useful to have the bundle_tx be able to provide similar functionality, with calls to begin_bundle and end_bundle hooks (which might be no-op’s by default).

I agree that this would be super useful. For the design I made, the `bundleTx` wouldn’t actually trigger the execution itself, it just orders other transactions inside of it. The bundle creator could insert their own transactions at the start or end of the bundle, but that would burn a lot of gas.

You could achieve `BeginBlock` with a hook that looks for `bundle.tx_number == 1`. It might be useful to add a `bundle.tx_last` notion to the global vars to enable devs to write hooks for `EndBlock` too. If you’d want hooks on different types of operations for the same application, you could do this with nested bundles.

---

**Lilyjjo** (2024-05-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/0xtariz/48/16327_2.png) 0xTariz:

> Who and when is the order of transactions determined in the payload of ordered transactions that a bundler includes?

This is left for the application developers to decide and would be done off-chain in this design. A protocol that is aiming to be decentralized would probably want to use a solution that allows for visibility into the code that is running and guarantees that the code is being ran. Devs could use a blockchain with a quicker block time, a normal  server with zkProofs, som AVS service, some TEE solution if privacy was also desired.

![](https://ethresear.ch/user_avatar/ethresear.ch/0xtariz/48/16327_2.png) 0xTariz:

> It seems to me that builders could target bundles for sandwich attacks in a similar way they target individual transactions.

Yes, block builders would be able to order these bundle transactions as they can order normal transactions. On-chain applications could use this design to ensure that they are able to restrict pieces of state to only be operated on under the transactions that they ordered, this is what helps the on-chain protocols better manage the value change their protocols experience between blocks.

The ability for bundles to be in bundles creates a cool design space where multiple on-chain protocols could designate their ordering to a different entity for further gains. Like an oracle bundler service could update prices and then order all bundles that rely on the prices after it lands on-chain.

---

**Lilyjjo** (2024-05-23):

Atlas looks dope. I think L1s with custom sequencing logic, native bundle support on a L1, and execution abstraction like Atlas all sorta enable the a similar thing with different tradeoffs:

- custom L1s: consensus grade sequencing enforcement, low ability to sequence multiple apps
- L1s with native bundle support: sequencing enforcement is high on-chain, able to support new apps without consensus changes, but weaker trust guarantees that the bundles are constructed correctly off-chain
- Execution abstraction: similar off-chain trust guarantees of native bundles, plays well with account abstraction, unclear on other tradeoffs (I need to read your white paper again)

---

**0xemperor** (2024-05-24):

Really cool work!

Just a few questions to understand some of the motivation (if you don’t mind)

1. Is there any reason for wanting the base layer to support these sequencing rules? Over an app-chain, is liquidity fragmentation the consideration?
2. How many sequencing rules do you think cover the vast majority of AMM MEV cases? From your instantiation, it looks like your sequencing rule aims to capture this by auctioning it and returning value to LPs. Do you think there’s any merit in sequencing rules that disallow certain types of transactions? Like sandwiching?

Thank you

---

**Lilyjjo** (2024-05-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/0xemperor/48/13285_2.png) 0xemperor:

> Is there any reason for wanting the base layer to support these sequencing rules? Over an app-chain, is liquidity fragmentation the consideration?

I was coming from the perspective ‘I want to build a protocol with self sequencing on Ethereum’ and finding it difficult to do so. Self sequencing doesn’t have to happen on the base layer but I’m not also sure why it’d be better to have it embedded in other layers. I’d be open to hearing opinions from other people as why one solution is better/worse.

Liquidity fragmentation is for sure a reason why it would be nice to have a way for sequencing rules on Ethereum.

![](https://ethresear.ch/user_avatar/ethresear.ch/0xemperor/48/13285_2.png) 0xemperor:

> Do you think there’s any merit in sequencing rules that disallow certain types of transactions? Like sandwiching?

Matheus Ferreira and David Parkes came out with great research on [anti-sandwiching sequencing rules](https://arxiv.org/abs/2209.15569) in 2023. Trying to implement these rules was actually the starting point of my research. The idea is that after you have a starting price in the block, trades just oscillate around the starting price until only a trades in a single direction are left. The idea is that a good implementation of these rules would prevent sandwiching from occurring:

[![IMG_2505](https://ethresear.ch/uploads/default/optimized/3X/b/4/b46a47f6e86df4eca5221f07185e3f55c39ae73b_2_690x469.png)IMG_25053390×2305 247 KB](https://ethresear.ch/uploads/default/b46a47f6e86df4eca5221f07185e3f55c39ae73b)

I think enabling sequencing rules natively would not only allow current types of protocols to operate better, but also open up whole new classes of protocols.


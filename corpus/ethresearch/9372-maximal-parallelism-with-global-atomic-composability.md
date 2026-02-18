---
source: ethresearch
topic_id: 9372
title: Maximal parallelism with global atomic composability
author: nikolai
date: "2021-05-03"
category: Layer 2
tags: []
url: https://ethresear.ch/t/maximal-parallelism-with-global-atomic-composability/9372
views: 2685
likes: 10
posts_count: 9
---

# Maximal parallelism with global atomic composability

I am proud to present Manaflow, a new approach to smart contract scaling, representing the result of 6+ years of EVM know-how and 3+ years of scaling research.

This post is a short ‘pre-whitepaper’ intended to give enough information for developers (read: potential hires) to understand our approach, without giving away so much info that some other team could impelment it first. As with most smart contract architecture problems, the devil is in the details.

First, a short list of insights:

- Atomic composability in a single shared global runtime is the secret sauce that makes ethereum and defi so successful.
- Most approaches to smart contract scaling sacrifice atomic composability in some way. Even ETH2’s sharding breaks this critical property.
- UTXO is nearly-trivially-parallel. The double-spend (more generally, ‘double-use’) critical path can handle millions of state changes per second. (As an aside, UTXO is designed for big blocks. Regardless of your perspective on whether bitcoin “should” have big blocks, the fact is that it was designed to have big blocks.)
- Existing UTXO systems have either limited, local statefulness, or they have global statefulness in a way that sacrifices the parallel validation nature of UTXO.
- If a system claims to have a model as good as EVM, it should be able to emulate the EVM. Thus our solution starts with EVM compatibilty and later could be extended to use LLVM or WASM.
- Emulating a single isolated EVM contract is not “EVM compatibility”! If contracts can’t atomically call other contracts, it’s not much better than traditional platforms.

Our approach unifies the global, synchronous, atomically composable logical view of EVM with the trivially parallel nature of UTXO validation. Only the state “double-use” is in the critical path. This critical path is blazing fast when there is no other validation that needs to be done.

The trick is that transactions declare not just the slots they will access, but the actual before and after values of those slots. This goes well beyond approaches like Vitalik’s ‘address access list’ proposal. The result is that each transaction can be validated by looking only at the one transaction. This is a big-block-UTXO-style scaling solution. In fact, it is ‘even more parallel’ than bitcoin-style UTXO, because transactions fully declare the ‘before’ states they are consuming. The entire blockchain could be validated in reverse!

More concretely, transactions are extended with a set of “moves”:

```auto
move : (
    mask    // signature bitmask
    mark    // short type tag, e.g. 's' for 'state slot'
    intx    // transaction in which this state was last used
    addr    // address this state belongs to
    slot    // for 's' moves, the state slot ("key")
    prev    // mark-specific value (e.g. 'before' value for 's' mark)
    next    // mark-specific value (e.g. 'after' value for 's' mark)
)
```

(Here we refer to just ‘state’ moves, but proper EVM compatibility requires a few more ‘bookkeeping’ move types, which we will keep secret for now.)

The tradeoff here is that the problem of sequencing/coordinating transactions (“stitching together” valid transitions) is offloaded to secondary nodes and end users. State that is not highly contested can be filled in by the end user’s wallet. State that is highly contested is filled in by various ‘coordinators’, much like the sequencers of L2s like Optimism. Here we encounter the theme that often the best ‘solution’ is to expose the tradeoff for users (developers) to solve as they see fit. The important thing is that validators can accept batches of transactions from any number of coordinators and end users in parallel.

Notice the ‘signature bitmask’ field (`mask`). The purpose of this field is to allow end users to leave some parts of the move undeclared, like a generalized form of Bitcoin’s SIGHASH variants. This allows coordinator nodes to fill in the values dynamically. A simple example is the resulting balance after a uniswap transaction. If the pool is highly contested, the exact value won’t be known until transaction fill time in the coordinator. Note that these value can still be constrained in the contract code! The design space for synchronization primitives that work ‘automagically’ from the point of view of the contract code is fascinating.

Validators maintain just a single index, the “utxo set” keyed by `intx,mark,addr,slot`. Coordinators and other nodes that implement the web3 API (i.e., what is the value of a given state slot) maintain the secondary index keyed by `mark,addr,slot`. This secondary index is not necessary for validation.

The reason we are going for an L2/sidechain instead of advocating for adding this directly to Ethereum L1 is that we completely remove the merkle-patricia state trie, a compromise that Ethereum is unlikely to be willing to make. Thin client proofs for Manaflow require a combination of simple SPV-style proofs of transaction combined with in-contract logic for cases where it is critical to know that the value in the transaction’s moveset is the ‘latest’.

The good news is that this transaction structure is very well-suited for fraud proofs, making optimistic rollups easy. In fact, it is so clean that it could even be verified with recursive ZK proofs, though we are not taking this approach for performance reasons.

We are currently in the sweet spot where the hardest architecture problems have been solved, but implementation has just begun and founder-sized stake is available for top hires.

If you’re an Ethereum client dev looking for some fresh well-compensated and challenging work, please shoot me an email to [hello@manaflow.io](mailto:hello@manaflow.io).

Happy to answer questions in this thread.

## Replies

**vbuterin** (2021-05-03):

What are the tradeoffs for data availability load like? At current margins it’s looking like data is one of the most scarce resources, so a proposal that allows extreme computation scaling at the cost of making eg. an average transaction take 300 bytes instead of 100 bytes may well be a step backwards. Are there benchmarks for this?

---

**adlerjohn** (2021-05-04):

FYI, your proposal is strictly-less-flexible yet not-more-efficient than prior art on Ethereum-style smart contracts on top of UTXOs: [Accounts, Strict Access Lists, and UTXOs - Execution - LazyLedger Talk](https://talk.lazyledger.org/t/accounts-strict-access-lists-and-utxos/37)

---

**nikolai** (2021-05-04):

[@vbuterin](/u/vbuterin) Right now we only have a quick and dirty benchmark in which we apply a 640k moveset (20mb of user state, ~100mb block) onto a UTXO db with 1.6bn entries (50gb user state) which handles just a hair shy of **~100k** state changes per second.

Reasons to think this is an under-estimate:

- It’s the naive first implementation with no attempt at optimization
- Written in typescript (!)
- On a consumer SSD from 2013
- Without using lmdb’s batching, just a simple loop
- Without using lmdb’s conditional writes, which are perfect for this use case

On the flip side, there is likely to be unknown unknowns that could make this unrealistically fast. We also need to measure this with much bigger utxo sets and blocks – in theory, it’s all logarithmic, but who knows… I don’t want to publish dishonest benchmarks. I would be happy with even 20k state changes per second.

Another point to make is that while the OP emphasizes the parallel computation, this architecture is also likely optimal in terms of memory/disk bandwidth. The limiting factor is reading and writing state from disk, I’m not sure why transaction size is a factor given that you still need to access the state. This approach puts all the state in one place – there is only one index, which is the transaction index,  UTXO index, and quasi state index all in one. All the overhead in the move type is in the index key. It’s hard to imagine how any system can beat an approach where each state change is just one word-sized conditional write within a single index.

---

**nikolai** (2021-05-04):

[@adlerjohn](/u/adlerjohn) I don’t think it’s fair to say this approach is ‘strictly less flexible’ when I mention in the OP that this is only a partial description, with parts omitted for competitive reasons. I acknowledge that in theory, this approach is nothing new. But again, the devil is in the details. Off the top of my head,

- Your post describes treating contracts as covenants, but this induces an inherently sequential bottleneck in the coordinator, limiting composability in practice. There are other approaches which treat contracts more like ‘address spaces’ while still having creates fit into UTXO “resource” model
- The sentence ‘The key to enabling multiple uses of the same contract in a single block is that contract UTXOs can be uniquely identified by their contract ID (in addition to their UTXO ID of course), since at most a single contract UTXO with a particular contract ID exists at any time’ feels to me like it implies this is a less flexible solution, since we never encountered a problem like this at all and can handle any number of parallel uses in the same contract in the same block
- Your post mentions a ‘CREATE2-like opcode’ for creating contracts, but we can actually support the exact semantics of both CREATE and CREATE2. There are a lot of strange edge cases involving reverted creates in successful transactions, empty contracts, and many other things that require some finesse. As a hint, try writing out all the implicit state associated with each contract in EVM (explicit state being the key->value storage).
- The links in the post don’t address some of the most challenging aspects of EVM compatibility, which have to do with emulating EVM execution context (all the tx.* and block.* ops) while preserving properties of ‘each transaction can be validated independently’ and ‘a block is valid if and only if each transaction is valid’

Anyway I don’t want to actually dive into the particulars of either solution at this time. I’m sure I misunderstood some of your points too – talking about this productively would require putting in some work to come to a shared base understanding of both approaches. If you have some specific functionality you think this approach is not flexible enough to handle, I can address it.

---

**vbuterin** (2021-05-04):

I’m very willing to believe that this design is very capable of ultra-high state changes per second locally if hardware is powerful enough. I’m worried about a different question: what tradeoffs in *bandwidth* does this result in? I don’t care at all about disk usage, I specifically mean the number of bytes that need to be passed over the internet? Currently, the byte size of blocks over the p2p network is one of the major (secondary) limiting factors to safely increasing the block size in ethereum. Adding extra data to transactions risks making their data size even larger and compromising scalability from that side.

---

**nikolai** (2021-05-04):

Well the short answer is that the tradeoff is centralization. I am imagining a small number of highly connected validators surrounded by constellations of auxiliary nodes. Only the validators need to download complete blocks. For the use cases I’m imagining (making tradfi more platform-like, let end users program contracts that manipulate equities, etc) it’s enough to have just 2 or 3 validators in each jurisdiction, professional nodes connected to the internet backbone. Invalid blocks aren’t an issue due to fraud proofs, only censorship. It’s sufficient to make the cost of coordinating some transaction censorship across jurisdictions to be higher than the cost of going after the application level.

To quantify this we would need to know how many state changes the average transaction causes. A single declared state change is already slightly bigger than an ETH transaction, so basically it is ~N times worse for N state changes.

---

**Dappsters** (2021-05-06):

This concept looks incredibly similar to the [Notoros](https://static1.squarespace.com/static/60493a08e9b0da2dea74ebc3/t/604d2fb99884c7706bd2380c/1615671226046/Notoros_Whitepaper_V1.pdf) whitepaper released a couple months ago. They use this concept of UTXOs and state indices for general VM sharding and a parallelization. They are launching on the Radix network, but their whitepaper indicates they are interested in scaling mainnet Ethereum as well.

---

**nikolai** (2021-05-08):

Thanks for the link. It looks very similar indeed, I suspect we will see this approach used more and more frequently.


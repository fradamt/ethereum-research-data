---
source: magicians
topic_id: 2264
title: Hypothetical maximum scale of Eth 1.x
author: lrettig
date: "2018-12-20"
category: Working Groups > Ethereum 1.x Ring
tags: []
url: https://ethereum-magicians.org/t/hypothetical-maximum-scale-of-eth-1-x/2264
views: 5456
likes: 12
posts_count: 16
---

# Hypothetical maximum scale of Eth 1.x

I’ve never seen this topic addressed directly so I thought it would be interesting to do so here. I’m trying to answer the question: What is the maximum theoretical scale that could be achieved on the existing Ethereum 1.x chain, that is, without sharding? I’m interested in a purely theoretical approach to this question, from a project management perspective, rather than in a more scientific answer, or in actually attempting to achieve such scale. If it seems likely that we could get serious performance gains on the existing, pre-Serenity chain, then I think investment in a more concerted “Ethereum 1.x” scaling effort would be justified.

I’ve had conversations with [@fredhr](/u/fredhr), [@jpitts](/u/jpitts), [@AlexeyAkhunov](/u/alexeyakhunov), and several members of the Ewasm team recently, and [@karalabe](/u/karalabe) spoke to the same topic recently as part of the [Eth 1.x](https://ethereum-magicians.org/t/ethereum-1-dot-x-a-half-baked-roadmap-for-mainnet-improvements/1995/16) conversation, so this is my attempt to summarize and draw some conclusions from these conversations.

The prerequisite for all of the ideas listed here is that they do not require major protocol changes, and are not breaking changes of the sort that will be introduced with Serenity. Many of these would not require a hard fork; most do not involve a protocol change. A couple are admittedly pushing the envelope as far as “not requiring major protocol changes” but “major” is subjective.

These are not hypothetical, “someday maybe” technologies; they’re technologies that have  been proven elsewhere and/or extensively studied. I chose not to include, e.g., STARKs here since they don’t seem to be feasible yet in their present form.

Possible scaling technologies and max. theoretical scale of each, *very roughly* in order of feasibility/confidence:

- Reduced uncle rate, shorter block processing time (discussion here): 10x
- Improved I/O from better data structures, e.g., TurboGeth (source: @AlexeyAkhunov): 4x
- State pruning (reduced I/O) (source): 15x
- Bounded account/storage trie growth via state rent or stateless clients (source: my own wild speculation, and discussion with @AlexeyAkhunov: block processing should get faster with reduced I/O, and with bounded state we should see I/O benefits over time from improving hardware): 5x
- Block pre-announcement, pre-warming the state (source: @AlexeyAkhunov): 5x
- BitcoinNG-style leader election and block proposal (source): 50x
- Ewasm with JIT compilation (source: benchmarking work that @gcolvin did last year, code and talk): 50x (modulo concerns about JIT safety)
- Parallelization of transactions (source: internal conversations on the Ewasm team): 50x
- Multidimensional gas/metering (gas is a blunt tool and is designed to be overly conservative; if we could meter, say, I/O and computation separately then we could pack more transactions into each block) (source: me)

Naively multiplying these all yields a scale of 1.87 billion x current scale. This is obviously an absurdly high number for at least two reasons: 1. This is a “best case scenario” and many of these ideas may not perform “as advertised” or may not work at all. 2. This assumes total orthogonality among the ideas, which is obviously not the case.

However, even if we assume, for the sake of argument, that only 10% of these ideas yield fruits, and that those yield only 1% of “advertised” performance/orthogonality, that’s still 1.875 million. Still a pretty high number. Still lots of room to poke holes.

One obvious weakness in this argument is that it’s “top down” versus “bottom up,” i.e., these ideas are all nice in theory until we try actually implementing them in existing clients and find that they might not actually work, might take as long as Serenity (e.g., stateless clients, which have wicked UX challenges), might break other things (e.g. usability), or might be mutually incompatible.

Another import caveat: as [@karalabe](/u/karalabe) and [@AlexeyAkhunov](/u/alexeyakhunov) eloquently explained in their Eth 1.x proposals, any attempt to scale today will immediately exacerbate the state and storage size issues, so any meaningful scaling (of Eth 1.x or 2.0) is still blocked on that.

Finally, there are probably fundamental limits to how far a single chain can be scaled, such as [sync time](https://twitter.com/VitalikButerin/status/1072488883533869058?s=20) (possibly alleviated by stateless clients?) and [I/O limits](https://blog.ethereum.org/2016/10/31/uncle-rate-transaction-fee-analysis/).

What am I missing? What have I got wrong here?

Is this exercise useful? To reiterate, the point is not to come up with some specific,. proposed scaling plan for Eth 1x, but rather to consider the question of reinvesting in scaling Eth 1x vs. doubling down on Eth 2 from a high-level, project management perspective.

Thanks!

## Replies

**AlexeyAkhunov** (2018-12-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Block pre-announcement, pre-warming the state (source: @AlexeyAkhunov): 5x

This should already be happening to certain extent - one of the geth’s latest releases effectively included contract storage items into the state caching (I do not have info about Parity, but Turbo-Geth has been doing from the beginning). It means that if you are a miner, and mining a block, but then someone else beat you to it, you need to import your block before you start mining the next one. Since the block you are mining and the one you have imported very likely have almost the same set of transactions, your caches will be warm, and import should be quick.

And that also means (unexpectedly), that this caching actually somewhat penalises miners mining empty blocks.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> However, even if we assume, for the sake of argument, that only 10% of these ideas yield fruits, and that those yield only 1% of “advertised” performance/orthogonality, that’s still 1.875 million

I suspect that most of these estimated were made based on the CURRENT state of things, and not on the state of things already improved by other measures, so they would not compound in a straightforward way. I would rather add these numbers than multiply them ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

EDIT: Addition

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> To reiterate, the point is not to come up with some specific,. proposed scaling plan for Eth 1x, but rather to consider the question of reinvesting in scaling Eth 1x vs. doubling down on Eth 2 from a high-level, project management perspective.

I support this sentiment (of course I would). I also think that we can make Ethereum 1.0 more changeable (one idea is to make clients simpler by not supporting all historical rules - that would also cut down historical tests - as I described in [Backwards-Forwards sync article](https://ethereum-magicians.org/t/backwards-forwards-sync-of-ethereum-clients/2258))

---

**lrettig** (2018-12-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> I suspect that most of these estimated were made based on the CURRENT state of things, and not on the state of things already improved by other measures, so they would not compound in a straightforward way. I would rather add these numbers than multiply them

Valid point. I agree that there is likely a low degree of orthogonality among many of these ideas, but I contend that it’s probably higher than 1%.

---

**jpitts** (2018-12-20):

Thanks for opening this up this [@lrettig](/u/lrettig)!

Experienced engineers do often wish to be conservative in their promises about outcomes, but it is crucial to know what outcomes are on the table when determining community-wide resource allocation.

Also, I created a separate related topic, a postmortem of sorts to [discuss what was potentially blocking investment in upgrades](https://ethereum-magicians.org/t/what-factors-may-have-been-blocking-efforts-to-scale-the-current-ethereum/2266) to the current Ethereum.

---

**Chandan** (2018-12-20):

1.87 million X scale means = Block size of 24K X 1.87 million (around 30GB)

Do you want Ethereum networking layer chugging along 30GB to 10000 full nodes?

Block size > 1MB becomes unmanageable. So your hypothetical max improvement is around 40X.

---

**lrettig** (2018-12-21):

Hmm. I’m pretty sure we can achieve better scale than that with a compression technology like zk-SNARKs but that might be too much on the theoretical side for this conversation.

---

**fubuloubu** (2018-12-21):

40x isn’t bad. Just under 52m transactions a day (On average). If 2nd Layer is prevalent and is a 100x gain, then we are at very reasonable scales with only a few major improvements.

Many great ideas, but the state reduction seems to be a blocker in almost all cases to allow a computer of average resources to full sync long term. Isn’t this the number one priority? We can prototype a 40x improvement, but the state size still blocks it. Solving the state size may also increase throughput by itself.

Also, hopefully it goes without saying that innovation prior to Serenity can also most likely be used once it’s released. That should mean scaling improvements today are scaling improvements long term for sharding. Seems like it is totally worth the investment now.

---

**Chandan** (2018-12-22):

40x is the upper limit.

Whether we can achieve it or not, I am not sure.

Most of Eth 1.x changes are performance tuning at the node level.

State reduction seems like more of an imagined issue than real issue.

People running nodes can use beefier hardware with more disk space.

---

**lrettig** (2018-12-22):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/f04885/48.png) Chandan:

> State reduction seems like more of an imagined issue than real issue.
>
>
> People running nodes can use beefier hardware with more disk space.

Sure. Then we end up with a version of ethereum entirely supported by the only people who can afford thousands of dollars a month to run a node: Infura, etherscan, and very few others. This is not in anyone’s interest, and I consider this a failure. It’s not the ethereum I want to see.

---

**Chandan** (2018-12-22):

What is the $$ threshold? $1000 server? $500 laptop? $100 chromebook? $20 raspberry pi?

80% of the world can not afford the server which can run ethereum full node now.

As long as we have enough people who can run full nodes, this whole affordability argument is red herring.

---

**gcolvin** (2018-12-22):

Compiled EVM was as fast or faster than eWasm in those benchmarks, [@lrettig](/u/lrettig)   Same safety concerns.

https://github.com/gcolvin/evm-drag-race/blob/master/time-vs-gas.pdf

---

**lrettig** (2018-12-24):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/f04885/48.png) Chandan:

> 80% of the world can not afford the server which can run ethereum full node now.
>
>
> As long as we have enough people who can run full nodes, this whole affordability argument is red herring.

There is a massive difference between “20% can afford it” and “0.001% can afford it.” The function is non-linear. It’s a slippery slope.

---

**lrettig** (2018-12-24):

Hi [@gcolvin](/u/gcolvin), thanks for the clarification. I may have misunderstood the results of your benchmarking research. `evmjit` refers to JIT-compiled EVM? Did you test JIT-compiled Wasm?

---

**ldct** (2018-12-24):

It might be instructive to examine the upper bound constraints on the maximum scale - e.g. how many ecrecovers a node can do per second, or the transaction data rate that fits into the bandwidth of a node, etc. to see which proposals address which and also to answer the question you raised.

---

**lrettig** (2018-12-24):

Agree this data would be helpful. I think a lot of that work has been done, I’ll post links when and if I can find them. The primary upper bound constraint right now is I/O, which is why several of the technologies I describe address I/O issues. Peter and Alexey wrote more about this in their proposals, too.

---

**gcolvin** (2018-12-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Hi @gcolvin, thanks for the clarification. I may have misunderstood the results of your benchmarking research. evmjit refers to JIT-compiled EVM? Did you test JIT-compiled Wasm?

[@lrettig](/u/lrettig) In the graph I linked to *evmjit* is EVM code compiled with [@chfast](/u/chfast)’s JIT, and *evm2wasm* is EVM code translated to eWasm and compiled with V8.  For these benchmarks Solidity generating eWasm directly might be better.  But better a *evmjit* might also help, especially if combined with EVM 1.5.

No doubt other benchmarks would give different results, but I’ve never seen any intrinsic reason why the EVM can’t be as fast as eWasm.


---
source: magicians
topic_id: 21458
title: Introducing rollup-geth
author: mralj
date: "2024-10-24"
category: RIPs
tags: []
url: https://ethereum-magicians.org/t/introducing-rollup-geth/21458
views: 763
likes: 24
posts_count: 7
---

# Introducing rollup-geth

Hello everyone ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=15)

During [RollCall #8.1](https://ethereum-magicians.org/t/rollcall-8-1-breakout-evm-equivalence-on-l2-october-23-2024/21312), we introduced `rollup-geth`, a collaborative effort between the Ethereum Foundation (EF) and Nethermind to create a fork of Geth that serves as a common core for Rollups.

### Long-Term Goals

- The ecosystem has expressed interest in having a common-core repository for Rollups to base their work on, which would reduce fragmentation across different EVM Rollups in terms of functionality and implementation.
- Our goal is to create a Geth fork that fulfills this need, allowing Rollups to integrate updates by merging our latest changes, similar to how they currently do with Geth.

### Short-Term Goals

We are currently in the experimentation phase. The objectives for this phase include:

1. Gaining a deeper understanding of the Geth codebase.
2. Developing a comprehensive understanding of the various L2 Geth forks.
3. Identifying challenges related to:

Merging rollup-geth changes into different L2 forks.
4. Extending Geth with L2-specific features.
5. Understanding relevant E(R)IPs that are becoming important for L2s.

### Our Approach to rollup-geth

We want to create something appealing and useful to Rollups, and thus are taking special care to ensure our changes are not overly disruptive to either L2s or upstream Geth. Specifically, during each EIP/RIP implementation cycle, we:

1. Aim to minimize conflicts with both L2 Geth forks and upstream Geth when writing code.
2. Open pull requests (PRs) targeting L2 forks to assess the effort needed to integrate rollup-geth changes.
3. Test these changes by running local nodes for each L2 to verify functionality, though we note that testing is not the primary focus during this phase.

### Beyond the Experimentation Phase

- We envision a governance process similar to All Core Devs, where we reach consensus on which features should be merged into rollup-geth’s main branch.
- The rollup-geth team will not only create PRs with new features but also provide “sample” PRs to illustrate how multiple L2s could integrate with the updated codebase. Reviewing these PRs will make the integration process clearer and less error-prone.
- Our aim is for L2s to use rollup-geth as their upstream source instead of Geth, syncing with rollup-geth just as they currently sync with Geth.
- rollup-geth will keep pace with upstream Geth to ensure updates are timely.
- The rollup-geth team will work to bridge the gap between core L2 teams and the Geth team.

### What Do We Need from L2s?

We would greatly appreciate:

1. General feedback on this project.
2. Feedback on our approach so far—what can we improve or change, and what is working well?
3. Insights into what rollup-geth needs to provide before L2s would consider making the switch, including any blockers.
4. Suggestions for the most desired EIPs/RIPs within the L2 ecosystem.

We began discussing some of these topics during [RollCall #8.1](https://ethereum-magicians.org/t/rollcall-8-1-breakout-evm-equivalence-on-l2-october-23-2024/21312), and we would love to continue that dialogue.

### GitHub Repo

[Here is the link to the repository](https://github.com/NethermindEth/rollup-geth). Please keep in mind that we are still in the experimentation phase, and the E(R)IPs implemented so far were:

1. Chosen to help us experiment with the implementation and to understand different challenges.
2. Not production-ready.
3. Not endorsements for adoption or part of any proposed standard.

We look forward to your input and collaboration!

Thanks, everyone!

## Replies

**norswap** (2024-10-27):

Cool initiative, I highly suggest looking at Optimism’s geth fork, for a few reasons:

- Its diff to upstream geth is on the smaller side and is extensively documented here: https://op-geth.optimism.io/
- It uses a minimal modification of the execution-engine API that L1 consensus clients use to communicate with L1 execution clients to communicate between the geth and a “rollup-node”. This pleasantly mirrors Ethereum’s architecture and allows to stuff less modification into geth itself and leave most of the rollup’s “brain” to a separate service.

The API difference allows the rollup node (consensus client) to specify a list of txs that the execution client must include in its block. For Optimism this is use to include a “system transaction” as well as all  forced inclusion txs made from the L1.

(Disclaimer: I used to work for Optimism, but I in good faith believe this is the closest thing to this initiative, and so should be the first place to look at and draw lessons from.)

Another interesting place to look at is Reth’s “execution extensions”. This is quite different and is more geared towards the “brain” of the rollup (the “rollup node” in Optimism parlance). It basically defines an architecture to take L1 data and do computation on it, which is what a rollup is.

Depending on the purpose of “a standard geth” for rollup, this is more or less relevant. In a more modular architecture (that separates execution and derivation, like optimism does with op-geth and the rollup node), geth sits on the execution side so this is less relevant. If the goal is to go for a more monolithic architecture that includes both concerns, then there are good lessons to be learn from Reth’s execution extensions.

Finally, Arbitrum takes the approach of using geth “as a library” (vs Optimism that uses geth “as a service”). I believe this is also a perfectly valid approach (and if the goal is to be broadly useful, there is no reason that both approach couldn’t co-exist in the same codebase).

The only concern there is whether Arbitrum’s changes to the geth codebase are licensed under a permissive open-source license or if they’re also under BSL. No matter, the case, it’s worth thinking about this architecture even if the code is not exploitable.

---

**mralj** (2024-10-30):

Hey!

Thank you very much for the thoughtful response.

We *are* looking into how various L2s are modifying `geth` for their needs

One of our goals is that L2s “use” `rollup-geth` in similar fashion as they “use” `geth`, that is to fork `rollup-geth` and build on top of it. This would mean that Optimism would continue using `rollup-geth` via execution-engine API and Arbitrum could continue using `rollup-geth` “as a library”.

We don’t want to be too disruptive for rollups and all changes should be “opt-in”.

---

**odysseas_eth** (2024-11-28):

Why closely follow the architecture of the L1 (and all the tech debt that comes with it) and not aim to create something new?

For example, not needing a separate consensus and execution client, but instead both operations run in the same process.

---

**mralj** (2024-11-30):

Hey, great question!

TL;DR; (and kinda “non-answer-answer”) because this is not aim of the `rollup-geth`

I think it will be easier to give you “real answer” if I explain how/why this initiative was started.

Today, L2s fork `geth` and build on top of it, either using it as a library (e.g., Arbitrum) or mimicking the CL-EL relationship (e.g., OP Stack). Maintaining these forks is costly, especially when upstream changes from `geth` need to be merged. The more divergent an L2 fork becomes, the harder this process gets.

Take the example of implementing an EIP/RIP like the [L1SLOAD precompile](https://ethereum-magicians.org/t/rip-7728-l1sload-precompile/20388). While it might bring nice features to an L2, implementing it independently increases the cost of maintaining that fork. Over time, these costs could slow down the adoption of useful EIPs/RIPs, as every L2 would need to manage this on their own.

I suspect this is why the implementation of some of these EIPs/RIPs has stalled over time. Each L2 must implement desired EIPs/RIPs on their own and pay the cost when merging with the upstream.

Alternative would be to implement some of these in `geth` but some EIP/RIPs (like above-mentioned `L1SLOAD`) simply don’t make sense on L1 (and if implemented as a part of the protocol then all the clients would need to implement them adding to the L1 bloat).

`rollup-geth` aims to solve this by serving as a shared foundation where these kinds of updates can be “centralized”. This reduces the burden on individual L2s and allows them to adopt improvements more easily. In the future, if the ecosystem demands it, we could explore diverging further from `geth`.

> For example, not needing a separate consensus and execution client, but instead both operations run in the same process.

Could you elaborate on the benefits you foresee from this? Many L2s have unique consensus mechanisms designed for their needs, and it’s unclear to me what value this integration would bring.

---

**odysseas_eth** (2024-11-30):

The intention for a common standard makes sense.

The division of consensus/execution in two different systems is a remnant of how ethereum was developed. Even if they are separate concerns, there is no reason they couldn’t be part of the same binary, which is explicitly simpler than breaking them into two different systems that communicate over HTTP.

Microservices are notorious for shooting complexity through the roof in terms of deployment, management and general DevOps. Since the node is nowhere near organized into modules like a microservice, it seems to me that it makes more sense to build it as a monolithic codebase.

If we wanted modularisation, I think there are a lot of interesting architectures we can explore that borrow from the latest in running high tolerance and scalable systems. For example, breaking up the node into modules that manage different resources (e.g state, computation, etc.) with the goal of the ability of running multiple rollups on the same system and enabling that system to allocate resources according to the need of every rollup. On top of that, you can architecture it in a fashion where horizontal scalability is easier.

But the above is beyond my point. My point is that if we are to build a common ground for L2s, we don’t need to carry all the tech debt that exists in the architecture and implementation of geth and instead we can design it from the ground up in consideration with modern deployment techniques (e.g K8s).

it’s vastly more work, but a good opportunity for a clean rewrite, not only in terms of software but also in terms of mental models / architecture.

---

**mralj** (2024-12-13):

Here is summary of our experience working on the `rollup-geth` during our “experimentation phase.”

## Our approach

### 1. “Feature flags”

All newly developed “features,” i.e., EIPs/RIPs, are behind the “feature flags,” i.e. (hard) forks. This ensures that:

1. We don’t introduce any breaking changes to L2s
2. All the changes are opt-in.

This should reduce friction and hopefully accelerate adoption.

### 2. “Conflict-free” code

We should aim for the “conflict-free code” - this is not practically possible, but the fewer conflicts/smaller the diff, the better. This is important for four couple of reasons:

1. It reduces the chances of introducing new bugs.
2. The cost of maintaining the newly added feature vastly reduces
3. What I have found is that it leads to more modular/maintainable code.
4. The sum of all the above is increased dev velocity.

**What does this mean in practice?**

The approach that yielded the best results is to, if possible,  encapsulate newly added logic into a separate function and move this function to a separate file.

Code-example:

```go
func (st *StateTransition) preCheckGas() error {
	if st.evm.ChainConfig().IsEIP7706(st.evm.Context.BlockNumber, st.evm.Context.Time) {
		return st.preCheckGasEIP7706()
	}

	return st.preCheckGasEIP4484()
}
```

In the upstream `geth` code, there is a `preCheckGas` function, instead of “bloating” it with the EIP-7706 specific code, I have split the gas handling in “pre-EIP-7706” and “EIP-7706”.   The benefits of this approach are:

1. The “old code” hasn’t changed, thus it’s easier to review, and I didn’t introduce any bugs “there”
2. The logic for “pre-checking gas” is in a separate file - again, it is easier to review
3. It’s easy to extend preCheckGas with a switch to handle more EIPs in the future if need be

### 3. Familiarity with the codebases.

Of course, the developer(s) working on the rollup-geth must be familiar with the geth codebase, but they should also be familiar with the L2-geth codebase(s). This is important because it drives implementation design and choices.

To exemplify this, take a look at [L1SLOAD precompile](https://ethereum-magicians.org/t/rip-7728-l1sload-precompile/20388). The RIP requires that L2 has *some notion* of the latest L1 block. But the way the L2s implement this (have an idea of) is different. E.g., Scroll and Op-stack have a “system contract,” and by querying the state of this contract, the node can “get” the latest L1 block number.  But as of the time of writing, this is not how, e.g., Arbitrum works. This means that for `rollup-geth`, we must consider these differences, and we cannot implement the L1SLOAD in the same way [Scroll does](https://github.com/scroll-tech/go-ethereum/pull/748) (implementation assumes the existence of the “system contract”)

## Challenges

Here are the biggest challenges we’ve faced during our research phase:

- L2s “using” geth differently, e.g. Arbitrum uses geth as a “library” and e.g. op-stack ”uses” geth by mimicking CL <> EL “architecture” which complicates RIP/EIP implementation decisions.
- Knowledge requirements: understanding not only the geth codebase but various L2-geth forks and their specifics (again, this is necessary to make better implementation decisions, but also to better understand what “this common core” needs to look like)
- It’s not always “easy” to write “conflict-free” code, especially in case of “huge” EIPs (eg. EIP-7706 where core components, like Header were changed - Draft PR link)
- In some coding practices, where certain parts of code get “bloated” by various L1 EIPs but, also L2-specific stuff - code editing in these “hot-paths” is “hard” because it can yield hard-to-resolve conflicts or huge diffs.
- Some other coding practices make it hard to effectively maintain rollup-geth / L2-geth across multiple forks

## Recommendations

Some recommendations for streamlining future dev process:

- Have agreed upon “governance” process (i.e. how to choose what will “common core” look like, both short-term and long-term), effort for this is already underway both during the RollCalls, and specifically for the first version of the CommonCore in this Telegram group
- L2-geth providing smth. akin “fork-diff view” like op-geth does (rollup-geth will also do this)
- If possible make sure future code additions are more modular/encapsulated
- Better/more docs are always appricated
- More feedback for rollup-geth team/project

## Specific goals accomplished

This research phase of the project started ~ 2 months ago.

We have:

- Got pretty familiar with the geth codebase
- Familiarised our selves with various L2-geth forks
- Came up best practices for rollup-geth development
- Implemented RIP-7728, EIP-7706 (not 100%, but “most important parts”), EIP-7708


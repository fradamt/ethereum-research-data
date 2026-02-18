---
source: ethresearch
topic_id: 23151
title: Ethereum needs Standards-Punk
author: SCBuergel
date: "2025-10-05"
category: Meta-innovation
tags: []
url: https://ethresear.ch/t/ethereum-needs-standards-punk/23151
views: 827
likes: 38
posts_count: 10
---

# Ethereum needs Standards-Punk

*(This is a continuation of discussions that I’ve had with many participants in the past weeks around Web3 Privacy Now and Protocol Labs’ “Cypherpunk Retreat”.)*

# The issue

Right now, if a wallet or app queries `eth_getLogs` from a production Ethereum client, there’s a real chance it will silently miss events. The result is simple and devastating: balances don’t add up, transaction histories show funds being spent before they are ever received, and applications cannot give users a trustworthy account of what happened. Consensus may still be intact, but the interface developers actually rely on is corrupted.

This is worse than a loud consensus bug, because it is a *silent* one. It erodes trust invisibly, makes results unreproducible across clients, and drives developers toward a few “blessed” infrastructure providers who can guarantee correct answers. That, in turn, accelerates centralization. And this is not an isolated bug: it is a symptom of a gap in Ethereum’s testing culture and in its standards around RPC behavior.

Concrete examples of this problem have been reported across at least Erigon, Nethermind, and on Gnosis Chain as well as Ethereum mainnet ([1](https://github.com/erigontech/erigon/issues/15733), [2](https://github.com/erigontech/erigon/issues/15219), [3](https://github.com/erigontech/erigon/issues/15029), [4](https://github.com/erigontech/erigon/issues/14434), [5](https://github.com/hoprnet/hoprnet/issues/7250), [6](https://github.com/hoprnet/hoprnet/issues/7215), [7](https://github.com/NethermindEth/nethermind/issues/9178), [8](https://github.com/NethermindEth/nethermind/issues/8860)). This is systemic.

# Why eth_getLogs matters

For users, the most basic questions are “Where did my money come from?” and “Where did it go?” The RPC endpoint that answers those questions is `eth_getLogs`. Every serious Ethereum product depends on it. Wallets use it to display ERC-20 transfers; DeFi applications rely on it to check pool states; DEXs track liquidity with it; accounting tools reconcile balances against it; the HOPR mixnet uses it to map its payment channel topology.

Consider the case of a wallet displaying a USDC balance. A simple `eth_call` to the storage trie might tell the app the user holds 500 USDC. To explain that number, the app then queries all past Transfer events from the contract filtered for the user’s address. If those events are complete, the history might show +100, –23, +423 = 500. If, however, the initial deposit of +100 is silently missing, then the app is irretrievably corrupted. The transaction history no longer sums to the balance, the user seems to spend money before ever receiving any, and the application cannot resolve the inconsistency.

When correctness at the RPC boundary is optional, every product built on Ethereum inherits this brittleness.

# Hive is not enough

Ethereum does have [Hive](https://hive.ethpandaops.io/), the client compatibility test suite, and it is valuable. But it is scoped too narrowly and it carries no enforcement power. Out of roughly 190 RPC compatibility tests, [only four](https://github.com/ethereum/execution-apis/tree/61a6cbad32cc0a6f7577b34371498fbb165a27c7/tests/eth_getLogs) cover eth_getLogs, and about half of those have been failing for months. Clients dispute the results and feel little pressure to resolve them. Passing or failing carries no consequences for release readiness or funding.

[![](https://ethresear.ch/uploads/default/original/3X/2/1/21ec7c6e6b0039adf039ec5f681b82d15f57adee.png)711×492 75 KB](https://ethresear.ch/uploads/default/21ec7c6e6b0039adf039ec5f681b82d15f57adee)

*[Current Hive test results](https://hive.ethpandaops.io/#/group/generic) show many of the 190 RPC compatibility tests failing (in red).*

The contrast with the web is striking. The web-platform-tests suite now includes over two million tests across HTML, CSS, JavaScript, and APIs. Browser vendors run them in continuous integration, gate releases on them, and rely on them to settle ambiguities in specifications. If Chrome and Firefox disagreed on whether `document.querySelector()` returned the correct node, the modern web would collapse. Ethereum is in an analogous situation today with `eth_getLogs`, but without the equivalent testing culture or governance.

[![](https://ethresear.ch/uploads/default/optimized/3X/d/f/dfc163e25674c37e2b9f3af0e9299829e3d3bcfa_2_690x397.png)907×523 61.2 KB](https://ethresear.ch/uploads/default/dfc163e25674c37e2b9f3af0e9299829e3d3bcfa)

*[Web Platform Tests](https://wpt.fyi/) show compatibility of major browsers on over 2 million tests.*

# What Ethereum needs

Ethereum needs to adopt the same combination of standards and conformance that allowed the web to scale. That begins with standards. An execution-layer RPC standards and conformance group should be established, with eth_getLogs as its first focus. The group’s task would be to write normative, versioned specifications for RPC semantics, including edge cases and error handling, and to define clear processes for change management and dispute resolution.

It also requires tests, not in the hundreds but in the hundreds of thousands. We should have canonical fixtures for history-sensitive calls, large-range differential testing across clients, and continuous runs at scale. That way, missing events or nondeterministic behavior can be surfaced quickly, rather than discovered months later in production.

Finally, it requires accountability. Conformance must matter. Client releases should not go out if they consistently fail RPC tests, and Ethereum Foundation funding should be tied to meeting these standards. Public dashboards and compatibility tables should make discrepancies visible, just as they are in the browser world. When everyone can see which clients are falling behind, incentives to fix regressions change.

# Conclusion

Ethereum’s credibility rests on deterministic answers at the RPC boundary. At present, correctness is optional, coverage is shallow, and divergence carries no real consequences. That is not sustainable.

The web nearly collapsed under the weight of interoperability failures, and only escaped by investing in clear standards and massive, respected test suites that vendors ran and respected. Ethereum can avoid the same fate — but only if it does the work now. Otherwise the reliability vacuum will continue to be filled by centralized API providers who monetize around correctness gaps, and the diversity of clients will cease to matter.

Ethereum needs standards-punk.

## Replies

**kdenhartog** (2025-10-05):

++ today what we’ve got is basically rough consensus, but we’re not doing a great job testing that our code is running interoperably at all levels. At the consensus layer and for testing the protocol, this is being done incredibly well. What we need is to bring that level of rigor up through to the site side interactions.

first that starts by testing the RPC endpoints from the nodes are interoperable and well tested. Within W3C for something to be considered standards track at least two independent implementations need to pass the test suite. I think we should keep that as the minimum bar here is that two independent nodes need to also pass the test suit. When we don’t have that we need to re-establish consensus on what passing should look like, document it, and then update the tests and implementation to match.

Once we have this at the node layer, I would also suggest we do the same at the window.ethereum object defined in EIP-1193. That will be a tougher task, but testing all the way through the stack up to the site layer will get us far closer to our goal of “rough consensus and running code” because today our code isn’t always reflecting the rough consensus we’re establishing.

Also, to understand some of the practical wisdom behind tests and when they are useful versus when they can also become too restrictive check out this blog post from Martin Thompson (major contributor to TLS, WebRTC, and many other standards for Mozilla): [Standardizing Principles](https://lowentropy.net/posts/standard-principles/)

---

**marioevz** (2025-10-06):

Hi [@SCBuergel](/u/scbuergel) I think this is a real eye-opener that we have to pay more attention to this topic.

I’ve added this item to the agenda of next week’s ACD-T (see ethereum/pm issue #1756).

If you have the time to join and share your thoughts on this call I think it would be beneficial!

---

**etan-status** (2025-10-07):

EIP-7919 aims to make answers deterministic and also verifiable, so that the provider is only used for data availability, but no longer has to be trusted for correctness. Further, it aims to remove the need for trusted indexers for basic use cases such as obtaining the history for one’s wallet in reasonable time.

---

**SCBuergel** (2025-10-08):

Thank you Mario, I will join that one and would be happy to share some thoughts for sure!

---

**SCBuergel** (2025-10-08):

EIP-7919 sounds like a great solution to many issues that I deeply care about, thank you for pursuing it.

However, even if Pureth ships soon, I don’t see the existing and largely unspecified JSON-RPC interface going away, since all libraries that dapps and wallets depend on rely on it. I’d go as far as calling the Ethereum JSON-RPC interface, not the EVM, the lingua franca for dapp devs who seek Ethereum compatibility.

Without getting too deep into specific `eth_getLogs` issues, querying and filtering EVM logs is far from trivial, with several edge cases left unspecified for clients to handle as they see fit. Encoding and proving schemes aside, `MUST` clients return all logs a user requests - even if that means fetching every WETH `Transfer` event from genesis to the chain tip? Some client teams historically considered that unreasonable and responded by erroring (with unspecified messages, leading to widespread string parsing in applications and libraries), timing out, or returning incomplete results. Since all these approaches are suboptimal, client teams are now building bespoke log indexing solutions to handle queries more efficiently. All this to say: even with better encoding and verification schemes - which I’m eager to see soon - still need to ruthlessly specify Ethereum client behavior.

---

**mosh** (2025-10-09):

As a practical example from an adjacent project in Web3, IPFS had longstanding incompatibilities across various implementations of data structures so we carved out a simpler subset called DASL. It took about 2 months to build an initial test suite + website (`hyphacoop/dasl-testing` on Github, website linked from there) this spring. A key part of this work was filing issues/PRs to clarify the spec along the way. A series of calls built momentum and support from implementers and protocol designers. Going forward, all grant-funded projects touching this area are expected to pass tests and conform to the spec where practical.

Ethereum is a bigger project but I think is possible to make a step-function difference, at least in a subset, in < 6 months.

---

**SCBuergel** (2025-10-09):

DASL is a great example, I hope it can serve as inspiration for the Ethereum community, thank you [@mosh](/u/mosh) !

Posting the results from [DASL Testing](https://hyphacoop.github.io/dasl-testing/) here as another example snapshot in addition to the screenshots in my OP

[![DASL-testing](https://ethresear.ch/uploads/default/optimized/3X/4/2/42ef2654466ecd677f81942166953544a20055e6_2_596x500.png)DASL-testing958×803 68.4 KB](https://ethresear.ch/uploads/default/42ef2654466ecd677f81942166953544a20055e6)

---

**bumblefudge** (2025-10-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/scbuergel/48/7344_2.png) SCBuergel:

> Otherwise the reliability vacuum will continue to be filled by centralized API providers who monetize around correctness gaps, and the diversity of clients will cease to matter.

too late?

gratuitous self-promotion here: https:// learningproof .xyz/lifecycle-of-a-blockchain-standard/

diversity of clients and availability of source code are not strictly necessary and hardly sufficient to have resilient, monopoly-resistant protocols. the main ingredient is actually transparency of governance. the collective endeavor of designing and enforcing conformance makes a great foundation for governance, and a baseline not just for CI but for designing/proposing upgrades.

---

**antonydenyer** (2025-12-01):

Agreed, problems around **eth_getLogs** aren’t just tooling quirks; they’re symptoms of a deeper interface failure that creates real centralisation pressure.

What I’ve seen in practice mirrors this: teams eventually stop relying on RPC guarantees altogether. Instead, they ingest the entire chain into their own denormalised datastore and rebuild whatever derived state they need, balances, histories, positions from scratch. The only way to make this dependable is to run a lightweight indexer or follower service that replays every block and reconstructs state deterministically.

Take something concrete, like maintaining token balances for a wallet or portfolio product. Today, you’re basically stuck choosing between two options, and both run counter to decentralisation:

1. Cold-start recomputation - Onboarding means firing off balanceOf calls across huge token sets or crawling logs over massive block ranges. It’s slow, expensive, and stops working once you have real traffic.
2. Precompute global state - Index everything ahead of time so queries are instant. This is what the major infra providers and top-tier products do, but it requires significant capital and operational maturity.

Users expect sub-second responses, so the market naturally pushes everyone toward the second model. And once you build this pipeline, it becomes a competitive advantage. There’s minimal short-term incentive to push for better on-chain or RPC semantics.

**Improvements only pay off at the ecosystem scale.**

This is why RPC correctness shouldn’t be a side issue. It has economic and governance implications. If the “truth layer” moves from clients to private indexers, client diversity at the execution layer matters a lot less for actual user trust.

There’s also a cultural point here: fixing these issues requires deep, unglamorous engineering work on clients, RPC behaviours, indexing, and testing frameworks. Historically, this kind of work hasn’t been valued as highly as protocol research, even though it’s what determines whether Ethereum is actually usable at the application boundary. If we want to prevent this class of failure, we need more than standards. We need sustained recognition for the people doing the grind.

In short, without enforceable RPC standards and serious conformance testing, teams will keep defaulting to private reindexing and data warehouses. It’s an understandable product decision, but fundamentally at odds with Ethereum’s decentralisation goals. Treating the RPC layer with the same rigour that the web applied to browser APIs is the right lens, and long overdue.

I’m fully behind this direction, and I’m glad to see someone pushing the conversation toward concrete, standards-driven fixes rather than accepting the current state as inevitable.


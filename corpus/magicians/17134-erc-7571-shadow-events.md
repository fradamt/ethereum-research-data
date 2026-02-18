---
source: magicians
topic_id: 17134
title: "ERC-7571: Shadow Events"
author: emilyhsia
date: "2023-12-07"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7571-shadow-events/17134
views: 4888
likes: 70
posts_count: 23
---

# ERC-7571: Shadow Events

Discussion thread for [ERC-7571: Shadow Events](https://github.com/shadow-hq/ERCs/blob/erc-7571-shadow-events/ERCS/erc-7571.md).

> This standard proposes a specification for shadow events – extra event logs in contract code that should only be generated in an offchain execution environment. Standardizing the syntax used for shadow events will make it easier for them to be specified, discovered, and fetched by any offchain developer tools or infrastructure.

## Replies

**wjmelements** (2023-12-07):

I don’t like that your Shadow Fork needs to have access to Solidity source code. The source code is not verifiable. You are playing pretend, basically. The imaginary execution is centralized. For others to verify it you would need to surface an API that gives the state substitution, especially code.

This technology is quite similar to `debug_traceCall`, which also allows you to substitute state and run simulations. The shadow execution environment is likely an efficient way to run your operation. But I don’t want a centralized service operator to be emitting standardized events like ERC20 `Transfer` because we have expectations that everyone can agree on when, why, and how they are emitted.

One use of your centralized service could be for aggregating nonstandard data. There are other services like Etherscan that are already doing this but they aren’t burdened by the assumptions of EVM execution. If you are going to abandon consensus and decentralization, why not go further? You can get a stronger monopoly by making your data collection proprietary.

---

**CHANCE** (2023-12-08):

+1 to this precisely – As mentioned, this functionality is already achieved through existing models, simulation models, and even basic indexers. Increased centralization does not even bring newfound benefits and only new burden, technical overhead, and financial costs.

Shadow being a company and offering this service to individuals that opt-in is cool, though I find it rather unethical to propose this with the expectation that individuals use your centralized service provider. Especially because this is not something that should be prescriptively applied to every provider that works with the data this industry generates.

Not all data needs to be emitted through an event, but the introduction of centralization and this “simulated” function is not required either. There are countless more appropriate, less cost prohibitive, and less centralizing solutions that provide nearly the precise benefits Shadow Events claim to enable.

---

**wjmelements** (2023-12-08):

I’d be interested in an alternative design that puts the substituted code registry on-chain.

A question I had today was that the spec suggests the centralized data provider can update the substituted code ad-hoc. Will the data provider re-execute all applicable transactions for the new code?

---

**miohtama** (2023-12-09):

The root cause of the issue is the gas cost of emitting events.

This is practical problem for

- High-frequency traders
- MEV bots

It is not a practical problem for retail trades, NFTs, or many use cases, as events are relatively low cost of overall transaction and value created.

While the proposal is interesting, I personally feel that

- On a public blockchain, basic data indexing features should be available on any JSON-RPC node, and you can then build your own indexing solution on top of core node features
- Making events unavailable or complexly accessible to normal developers will hurt the developer experience a lot.
- Because shadow events requirements to read data are more complex, these events will be unavailable for many entry-level Dapps and wallets that do not have dedicated resources to infrastructuring.
- If the gas cost of events is the issue, we should have first discussion 1) if this is a real issue and have data backing it up 2) are the simpler and cleaner ways to solve it.
- HFT and MEV traders are highly profitable.  Optimising the chain for their use cases at the expense of others is not a net positive for the development of Web3 ecosystem.
- It’s against the ethos of cryptocurrency communities to have private companies with proprietary tools to hijack the discussion.

However regardless of the shady nature of the proposal, it is very interesting. One  good way to move forward with this proposal could be that

- Shadow team pilots the feature with one of the L2s that will find this useful. Many trading specialised L2s could be interested. For example, there is a new L2 called Blast, led by Paradigm, which is likely to be very aligned with the interests of the proposer.
- Let’s not consider this for the EIP track, until it has been in production and has tool adoption, at least with one of L2s.

Alternative solutions include

- State-based indexing in TheGraph
- Automated historical state tracking in Subquery

Both of listed alternative solutions are capable of doing state-based indexing, and are open source. However whether this ERC is applicable for them, they should be consulted for the discussion.

---

**alvinh** (2023-12-09):

This proposes a common syntax for shadow events to avoid fragmentation and make it easier for others to provide their own shadow fork services – whether open-source or closed-source.

With a standard way for contract developers to specify shadow events, it is a lot easier (a) to verify shadow contract source code, (b) any provider to run the same shadow contract/events, and (c) compare the results between them to verify valid results.

There is much more opportunity in *net new* events being added to contracts in a shadow fork environment. These would be events that we don’t currently have today on mainnet, but would be useful for offchain indexing, analytics, and observability. And like all ERCs, this is entirely opt-in from smart contract developers.

This would provide a way for us to get more valuable data, without increasing the gas burden on end users. Retail users are in fact amongst the most highly impacted by changes in the gas costs of transactions – Doug Colkitt explains this here: https://x.com/0xdoug/status/1732131133146505426?s=20

---

**miohtama** (2023-12-09):

> Doug Colkitt explains this here: https://x.com/0xdoug/status/1732131133146505426?s=20

Doug is talking about arbitragers and other high-frequency trader (“order flow from routers”), not end users. Emitting events on L2 Uniswap v3 swap is a fraction of the total trade cost. This is the high-frequency use case we should deliberately want to discourage to optimize towards, because it does not present the ecosystem interest as a whole (“easy dev experience for events”).

Indexing and public data access is an integrated part of any market place. Someone needs to bear the cost of indexing in the end. If you want to move the cost of indexing from the one who created the data in the first place to someone else, it is same as [externalising the cost](https://en.wikipedia.org/wiki/Externality). The cost of indexing does not disappear and is unlike to be the lower.

Current indexing model

- User does something on-chain
- User pays for state modification and indexing
- JSON-RPC node saves these events

Proposed shadow indexing model

- User does something on-chain
- User pays for state modification but does not pay for created indexed events
- Special indexing node is running somewhere
- But someone needs to pay for the cost of this special indexer

Probably similar business model as EtherScan today, foundations and DAOs paying EtherScan yearly fee to get the service
- The foundation or DAO needs to get the money to cover this cost, so it needs to get it somehow from the transaction fees,as now they would pay Paradigm for their indexers
- The cost was just moved around
- More centralisation was created in the process
- The indexing cost is now actually higher because there are more middlemen in the process
- Those who generate a lot of events (HFT trades) were subsidised in the process

---

**dor** (2023-12-09):

Adding compiler-level support for conditional code inclusion can be useful, as concepts like `#ifdef` in other programming languages demonstrate. However, there’s potential to further generalize this approach for the Ethereum ecosystem. As a strawman example, an `#ifdef-like` syntax could be implemented to enable flexibility, similar to what [Nick Johnson suggested](https://twitter.com/nicksdjohnson/status/1733385854721118215):

```auto
@include_if(FLAG)
    emit SupplementaryEvent();
@end
```

Where `@include_if` and `@end` delimit optional code based on if `FLAG` is set during compilation. This allows:

- Conditional compilation without interference
- Cleaner contract code by delimiting supplemental sections
- Generic terminology to support wide use cases.

The command-line flags can be replaced by adding a new `conditional` statement category to the already existing solc `pragma` statements:

`pragma conditional Flag1, Flag2; // These will set Flag1 and Flag2`

No matter the approach taken, the key point is that further generalizing leaves space for ecosystem growth beyond narrow use cases.

Importantly, the path to standardization in such a manner should be guided by open-source solutions and widespread benefits to the community. This strategy helps ensure that early standardization doesn’t disproportionately favor a few private entities and their customers. One example of a more general approach’s use case is enabling developers to use different compilation flags for feature toggling on deployments to various chains. ***Even with the proposed changes, I’m unsure if it fully justifies standardization. Nonetheless, a move towards a more generalized framework has a higher potential to benefit the broader ecosystem than the existing proposal.***

Lastly, it’s crucial to address the fundamental issues underlying this ERC. As a community, we should prioritize ERCs that tackle key challenges like reducing gas costs for logs/events and addressing contract size limits at the chain level. Several proposals in these areas have stagnated, so I applaud the drive to find alternative solutions. However, the current discourse around ‘shadow logs’ and the recent discussion on [code-size limitations](https://twitter.com/haydenzadams/status/1729194142608302112) sparked by Hayden/Uniswap presents an opportunity to revisit and revitalize these initiatives/conversations in parallel. Prioritizing improvements in the decentralized environment is essential while we explore various solutions. However, I think we want to proceed cautiously to ensure that solutions do not inadvertently create new problems that outweigh the original issues they aim to solve.

---

**JoakimEQ** (2023-12-09):

> Lastly, it’s crucial to address the fundamental issues underlying this ERC. As a community, we should prioritize ERCs that tackle key challenges like reducing gas costs for logs/events and addressing contract size limits at the chain level. Several proposals in these areas have stagnated, so I applaud the drive to find alternative solutions.

> Prioritizing improvements in the decentralized environment is essential while we explore various solutions. However, I think we want to proceed cautiously to ensure that solutions do not inadvertently create new problems that outweigh the original issues they aim to solve.

This is the most important part of the whole discussion - where ethereum stands on the scales of decentralization, scalbility, and security.

1. It is never only about making ethereum be able to more scalable
2. It is never only about making ethereum be able to be more decentralized
3. It is never only about making ethereum be able to be more secure

My take is that ethereum ethos has always to perfectly balance the three. This proposal tries to improve 1, but ends up building issues in 2 and 3.

---

**gdats** (2023-12-09):

Shouldn’t these blocks be named something more generic like “offchain” or “gasless” instead of attempting to enshrine a private company’s name into the syntax?

```auto
gasless {
  emit LogEventName(param1, param2, param3);
}
```

or,

```auto
offchain {
  emit LogEventName(param1, param2, param3);
}
```

---

**charliemarketplace** (2023-12-09):

I don’t believe this fits the criteria of an ERC.

You can already bytecode match contract ABIs and make offchain comments on contract traces for objective analysis of state differences in the execution layer.

Logs already cannot be trusted to accurately represent changes to state, so standardizing a separate layer for how contracts would submit recommended “shadow logs” feels orthogonal to the problem.

Contracts are welcome to not emit events to save gas. But externalizing the costs to indexers and data companies doesn’t require a standard.

Events are a form of advertising for contracts. It makes them easier to interpret for basic users doing little more than checking Etherscan to see if a token is semi-legit & how many users it has. I understand all products would be cheaper without advertising.

But this ERC does not solve the advertiser’s dilemma for contracts.

---

**emilyhsia** (2023-12-09):

The motivation behind the shadow indexing model is two-fold:

1. To give protocol developers the choice to decide which events are critical and should remain onchain, and which events are supplemental and could be moved offchain.
2. To give third-party developers a new tool for transforming and augmenting onchain data.

For protocols, many events that are logged today are designed to be consumed by the protocol’s specific frontend. These events are overfit to their specific use case at that point in time. As a result, protocol development is tightly coupled with product development and research analysis. Shadow events offer a tool to decouple smart contract development from product development and research analysis.

For third-party developers, events that are being emitted today don’t always have all of the data they need, and isn’t in the format they want. As a result, many teams have invested a lot of time and money into building complex, offchain data indexing pipelines to transform and augment onchain data. Shadow events offer a new primitive that allows any third-party developer to design and generate custom events for their use case, without needing specialized data engineering skills. With shadow events, anyone that can write Solidity or Vyper can now write data pipelines.

For both protocols and third-party developers, it’s unrealistic to expect that the original smart contract developers can anticipate all future data needs by everyone in the ecosystem. The current tight coupling between smart contract development, frontend development, and data analysis slows the entire ecosystem down.

To state explicitly – I do not personally believe developers should be removing core events like `Transfer` from token contracts. While there are [known issues](https://x.com/0xCygaar/status/1722354422863593655?s=20) with `Transfer`, these events are critical for all ecosystem products and tooling, and make the chain more readable.

---

With that said, the “current vs proposed” that you outlined above is a really helpful framework to illustrate the state of affairs. Here’s how I’d update it:

Current indexing model

- User does something on-chain
- User pays for state modification and critical and non-critical events
- Nodes store critical and non-critical events (which are un-indexed and un-decoded)
- Indexers are running offchain – centralized indexers (i.e. Alchemy Subgraphs), decentralized indexers (i.e. The Graph), custom in-house indexers, or some combination of the aforementioned indexer types
- Frontends are powered by data from these offchain indexers

Proposed shadow indexing model

- User does something on-chain
- User pays for state modification and critical events
- Nodes store critical events (which are un-indexed and un-decoded)
- Indexers are running offchain – shadow forks generating custom events, centralized indexers (i.e. Alchemy Subgraphs), decentralized indexers (i.e. The Graph), custom in-house indexers, or some combination of the aforementioned indexer types
- Frontends are powered by data from these offchain indexers

---

**miohtama** (2023-12-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/emilyhsia/48/11094_2.png) emilyhsia:

> For third-party developers, events that are being emitted today don’t always have all of the data they need, and isn’t in the format they want. As a result, many teams have invested a lot of time and money into building complex, offchain data indexing pipelines to transform and augment onchain data.

How large is the problem, and is there public research or case studies backing this up? This is something the Shadow team brings up, but there is no public evidence for how widespread this problem is. ERC discussion warrants public research and should not be based on the private business research of authors.

It’s understandable if trading firms (yes I come from one) invest in custom indexing solutions. However, as mentioned earlier, it is already possible for them to get any data from the state of Ethereum EVM. While the proposed solution addresses these needs, it needs to be weighted with the other tradeoffs that the ERC may bring with wide adoption, like the reduced developer experience with the core tools and more centralisation. These are addressable concerns tough. For example in web standards (HTML, not Web3) each standard requires an open reference implementation and at least two implementers to be considered “community acceptable.” Let’s not at least make ecosystem more centralised, as we have found out with the recent issues Etherscan hiking up the fees.

The cleanest solution for the problem “developers do not have the events they want” is that the developers approach the protocol and ask them to emit these events in the next protocol iteration. Then, the next version of the protocol is better and both protocol stakeholders and general public benefits from this update. Naturally, this cannot be changed in the current version if the smart contracts are immutable, but there is a cycle of protocol updates and there is a clear expectation for this for all the community stakeholders. Examples include protocol version upgrades for Uniswap, Aave, Compound, etc.

---

**pizzarob** (2023-12-09):

Seems to early to make this a standard. Nothing wrong with Shadow standardizing this internally and it if becomes the unofficial standardized way to do this and shadow events become popular due to open source indexers, not just one company with proprietary code, then yeah why not make it a standard.

---

**0xmikko** (2023-12-09):

Shadow events is novice idea for debugging, and useful to deep monitoring when needed. However, motivation to remove events for gas savings is not public good. Many front-ends depends on events, and making more different nodes to serve a dapp looks much more complex that small extra fees needed for emitting events.

---

**notvitalik** (2023-12-10):

This could be a PR to a graph node. That might help decentralize shadow events to everyone and dapps can choose to use shadow. Everyone wins ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**epappas** (2023-12-10):

The ability to extract enriched the data during the execution flow, and/or create more indexed events at no cost, is for sure something interesting.

Although, at the end dev-user, I doubt if the “no-cost” is real; the data of the secondary chain have to be served, so someone needs to bare some cost. Nevertheless, let’s say the promise is to aim for a lower cost, than having multiple rich on-chain log events.

My main criticism is with the proposed code paradigm, we’re polluting the main flow.

Wouldn’t a rust-like macro (or C-like preproc) be easier to achieve a better backwards compatibility and a cleaner paradigm rather than injecting it in the function body?

for example:

```auto
//! #[shadow:captureTick]
function my_awesome_function(..) {
   ....
   //! #[shadow:captureTick(ticks)]
   ...
}
```

then you can have an accompanying file `my_contract.shadow.sol` that you can define the body of the `captureTick(ticks)` macro.

With this architecture you can have a shadow client to execute the macros, in a much cleaner manner.

This way, the validated contracts can be the non `*.shadow.sol` (or at least they can be optional) and the secondary chain can receive the deployments the `*.shadow.sol` code.

Potentially, with a macro-style paradigm we could unlock a whole new stack of solidity extensions.

---

**MidnightLightning** (2023-12-10):

I believe this ERC would be better suited as logic added to The Graph or similar indexing service and not trying to create an alternate full EVM stack. I agree with the other comments expressed in this thread that if triggering events is “too expensive” in the main EVM, adding third-party alternate EVM implementations seems unlikely to actually be cheaper, so I don’t think this base premise fulfills the original problem it presents.

If this proposal does move forward, the biggest implementation issue I have with it is having the “shadow” bytecode able to be different than the “real” bytecode. I’d opt for having a no-op bytecode be added into the real contract, which then should do additional logic in the shadow EVM. This would require developers to future-proof their contracts and decide at compile-time what hooks future use-cases may want, but it then makes it more easy to verify that the “shadow” logic is executing the same logic as the “real” logic.

---

**SebastienGllmt** (2023-12-10):

> How large is the problem, and is there public research or case studies backing this up? This is something the Shadow team brings up, but there is no public evidence for how widespread this problem is

Speaking form my experience, this would be useful for quest platforms and things like onchain games. These use-cases often want the app to evolve over time based on the user’s onchain activity, but want to do so while maintaining decentralization (i.e. anybody can resync the game state from scratch without relying on a centralized server).

Right now this is doable, but not all actions your want your game/app to react to have EVM logs for them, and so having a publicized set of annotations for contracts your app depends on that people can use to properly rehydrate the game UI state would be super useful

---

**dor** (2023-12-10):

The ability to generate custom instrumentation/shadow logs is something that people already do today, as [@wjmelements](/u/wjmelements), [@miohtama](/u/miohtama) and [@charliemarketplace](/u/charliemarketplace) mentioned. Platforms like Shadow, Ghostlogs, and others will make that more accessible than it is today, which is **good**. While people might disagree on methods (or timing), I don’t think many would argue against enabling smaller teams/devs to do something/have capabilities that generally larger, more experienced, and resourced teams had.

In its current form, this ERC aims to enshrine a format for others to follow. It would be beneficial to generalize the proposal more so it can address different use cases, decoupling it from an ideology that some might object to. It would also be worth removing the name of a private company from the format. You could better achieve the desired benefits for the community by incorporating some of the suggestions above.

Sidenote: as [@charliemarketplace](/u/charliemarketplace) mentioned, Shadow logs also suffer from some of the problems you mentioned with Transfer spoofing. this will now be cheaper and possibly harder to figure out from the code.

**edited later**: On the topic of further generalizing – [a thread by highbyte](https://twitter.com/high_byte/status/1733977265363378416) mentioned [an old idea/proposal he made](https://github.com/ethereum/solidity/issues/12610) that is relevant and can be an inspiration on this subject.

---

**WhyShock** (2023-12-11):

Working on a small dashboard to look at the data around this.

https://flipsidecrypto.xyz/CryptoGowda/erc-7571-shadow-events-gPmiYh

early analysis indicates that event logs account for approximately 4-6% of the total gas consumption on average, but we could however save around ~100-500k USD daily ( depending on gas price )

Though the daily gas usage varies, the percentage of gas used by logs has remained within a narrow band, signifying that event logs have a predictable and relatively small impact on the overall gas consumption within the network This could imply a stable transaction pattern or efficient use of logs in the network’s operations

PS: I have employed a preliminary and straightforward method to analyze the data presented. While this approach may lack sophistication, it serves as an initial framework for understanding the trends. I invite the community to review the methodology first and build upon it.


*(2 more replies not shown)*

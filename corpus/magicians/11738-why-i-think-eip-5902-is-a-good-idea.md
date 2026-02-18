---
source: magicians
topic_id: 11738
title: Why I think EIP-5902 is a Good Idea
author: orbmis
date: "2022-11-14"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/why-i-think-eip-5902-is-a-good-idea/11738
views: 567
likes: 0
posts_count: 1
---

# Why I think EIP-5902 is a Good Idea

EIP-5902 proposes a standard for smart contract that creates a simple but powerful primitive that can be used by dapp developers and opens up a new and interesting design space.

Effectively, EIP-5902 allows a developer to write a smart contract that reacts autonomously to events fired by other smart contracts.

It works on a basic pub/sub pattern using an incentivised relayer network as a messaging bus. One contract acts as a publisher, while other contracts are subscribers. The publisher emits “Hook” events which are picked up relayers, who in turn call the relevant public function on subscriber contracts, passing them the payload of the Hook event, which can be any arbitrary data (a snark proof for example). The relayer is paid a small fee by the subscriber contract for this service. All publishers and subscribers register in a central registry contract (a bit like [EIP-1820](https://eips.ethereum.org/EIPS/eip-1820))

That’s it in a nutshell. If this sounds familiar, it’s because there are already similar services. Similar, but not quite the same. There are services that allow you to deploy a serverless instance to run when an event is emitted by some contract, or that will ping a webhook when an event is emitted, or invoke some other action.

All of these services will do the job. The problem is that all these solutions require you to have some external off-chain process in order to respond to the events on-chain. This is fine for applications that will need to respond to on-chain events frequently, but use-cases where the subscriber code only needs to run infrequently, this method doesn’t really suit. They also require you to have some account set up with some centralised third party provider, and EIP-5902 offers a fully permission less alternative.

With the EIP-5902 approach, you only have to write your contract code, deploy it, fund it with a small amount of ETH (or potentially some other token), and register it as a subscriber in the registry contract. That’s it. You don’t need an account with some provider, you don’t need to write some code for some off-chain process. You can sit back and rest assured that a relayer will call the relevant function in your smart contract when a hook event is emitted by the publisher.

If you are a publisher contract, you can add a new feature to your dapp by simply emitting a Hook event, and registering as a publisher in a registry contract.

**Use Cases**

The design space is fairly broad, and this is an interesting primitive that can be used in many ways, but here are a few basic ideas for potential use cases:

Examples of use cases that would benefit from this scheme include:

**Collateralised Lending Protocols**

For example, Maker uses the “medianizer” smart contract which maintains a whitelist of price feed contracts which are allowed to post price updates. Every time a new price update is received, the median of all feed prices is re-computed and the medianized value is updated. In this case, the medianizer smart contract could fire a hook event that would allow subscriber contracts to decide to re-collateralize their positions.

**Automated Market Makers**

AMM liquidity pools could fire a hook event whenever liquidity is added or removed. This could allow a subscriber smart contracts to add or remove liquidity once the total pool liquidity reaches a certain point.

AMMs can fire a hook whenever there is a trade within a trading pair, emitting the time-weighted-price-oracle update via an hook event. Subscribers can use this to create an automated Limit-Order-Book contract to buy/sell tokens once an asset’s spot price breaches a pre-specified threshold.

**DAO Voting**

Hook events can be emitted by a DAO governance contract to signal that a proposal has been published, voted on, carried or vetoed, and would allow any subscriber contract to automatically respond accordingly.

---

For more information on the technical details of how EIP-5902 actually works under-the-hood, please refer to the [full specification](https://github.com/ethereum/EIPs/pull/5902/files).

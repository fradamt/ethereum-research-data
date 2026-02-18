---
source: magicians
topic_id: 20351
title: "ERC-7726: Common quote oracle"
author: albertocuestacanada
date: "2024-06-20"
category: ERCs
tags: [oracles]
url: https://ethereum-magicians.org/t/erc-7726-common-quote-oracle/20351
views: 619
likes: 4
posts_count: 3
---

# ERC-7726: Common quote oracle

For a while now we have been toiling on what is now a minimal standard for oracle value feeds.

[Draft EIP](https://github.com/ethereum/ERCs/pull/500)

Some oracle implementations from the community: [GitHub - alcueca/awesome-oracles: Common Oracle Specification and Adaptors](https://github.com/alcueca/awesome-oracles)

Some oracle implementations from Euler: [GitHub - euler-xyz/euler-price-oracle: Euler Price Oracles, a library of immutable oracle adapters and components](https://github.com/euler-xyz/euler-price-oracle)

This all probably started when I wrote this article about using value conversions instead of prices in smart contracts:



      [hackernoon.com](https://hackernoon.com/getting-prices-right)



    ![](https://ethereum-magicians.org/uploads/default/optimized/2X/7/7928528ab80b6453961af1e4e75b048d5d932cb9_2_690x460.jpeg)

###



How to implement better price feeds in smart contracts










In very short, this is a minimal standard with a single function, from the spec:

#### getQuote

Returns the value of `baseAmount` of `base` in `quote` terms.

MUST round down towards 0.

MUST revert with `OracleUnsupportedPair` if not capable to provide data for the specified `base` and `quote` pair.

MUST revert with `OracleUntrustedData` if not capable to provide data within a degree of confidence publicly specified.

```yaml
- name: getQuote
  type: function
  stateMutability: view

  inputs:
    - name: baseAmount
      type: uint256
    - name: base
      type: address
    - name: quote
      type: address

  outputs:
    - name: quoteAmount
      type: uint256
```

There is a bit more info on the spec, including the lack of a priceOf function.

Although due to process the discussion should take place here, where it is public and searchable, we also have a telegram group that you are welcome to join: [Telegram: Join Group Chat](https://t.me/+kehxUdF8vPdhNzZh)

## Replies

**JulianT** (2024-10-18):

Hey there all who might still be paying attention, first a big thanks to all who have already contributed.

I know its been quite some time without much additional discussion, so apologies for being under a rock for the past months…

That said, I’ve just got a quick question regarding the intent of the EIP, and if agreed on the intent, what should seen as an acceptable minimum interface for a reported price.

---

# Intent of the EIP

Is the intent just to have a quick one over in order to force future oracles to adopt a more rational standard for the actual price reported? (This alone has quite a lot of value to begin with)

Or is the intent to provide a picture of what is expected of an oracle’s interface more generally?

(I personally feel that EIP’s should not just be easy to comply with for current protocols, but should also govern what we believe is minimal expectations for protocols wrt security considerations.)

If the latter I would make one additional suggestion to the interface given it is already ubiquitous and should likely be recommended for those consuming prices.

---

# What Should Be Returned?

## The Price (duh)

Of course as already noted and provided an interface for, it seems absolutely necessary to standardize the format of pricing coming out of oracles (in order to avoid protocols building conversion tooling from scratch e.g. the Euler oracle toolkit / what I had recently build at Warlock).

## A Timestamp?

However in order to securely consume prices, a protocol should likely attempt to validate the latency at which they are consuming the price from when it was reported. This sort of validation I would consider recommended, and furthermore is becoming more commonplace as protocols begin to apply numerous fallback oracle implementations.

This validation requires a timestamp, ideally being the `block.timestamp` of the block it was pushed.

### Backwards Compatibility:

Based on cursory searches / my memory, *all* or nearly all current oracles provide either a calculated or submitted timestamp alongside their reported price.

#### Chainlink:

smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol#L14

#### Redstone:

etherscan/address/0x0c2c7ded01ccdfab16f04aff82af766b23d6be0a#code (same as chainlink)

#### Pyth:

pyth-network/pyth-sdk-solidity/blob/main/PythStructs.sol#L21

#### Chronicle:

While Chronicle does offer a non-time reporting read, documentation directs developers to their read with a time reported – chronicleprotocol/chronicle-std/blob/main/src/IChronicle.sol#L23 | chroniclelabs/Developers/tutorials/Remix

#### API3:

api3dao/airnode-protocol-v1/blob/main/contracts/api3-server-v1/Api3ServerV1.sol#L33

#### Warlock:

I am currently no longer working at Warlock but I wrote them all myself and they offered both calculated and submitted timestamps.

---

# Conclusion:

**TL;DR:** We should add a timestamp – everyone that matters already has one, everyone in the future should have one, and it should be implied that consuming protocols should validate one (by being required in the EIP)

---

**totomanov** (2024-10-18):

Hey, thanks for kicking off the discussion! The ERC is still a draft so you are indeed not too late. Here are my takes:

## Intent

The primary intent of the standard is to be practical and immediately useful rather than abstract and prescriptive. We hand application developers an easy, safe oracle adapter standard together with Euler’s library of well-audited compliant adapters that cover 99% of use cases. This saves them time and money, while making their dapps a bit more secure. It would be great if incumbent oracle providers supported ERC-7726 in their primary data feed contracts, however this is a huge ask with a lot of friction.

To highlight the impact let’s examine the status quo (I can only speak about lending protocols). Due to historical reasons the de-facto oracle adapter standard is Chainlink’s `AggregatorV3Interface`. Once you enshrine this interface in your consuming application it is almost permanent; nobody in their right mind would upgrade a mission-critical component in production for a quality-of-life improvement. The effect is that a new provider that wants to compete is almost required to serve prices through `AggregatorV3Interface` (see RedStone Push, Chronicle, API3 among others).

The interface is ideal for Chainlink price feeds but subpar as a general future-proof oracle adapter interface. It holds baggage for backwards compatibility, requires superflous functionality, and is not composable (returns a fixed-point price rather than an amount quote). This makes for a few gotchas when consuming a non-Chainlink provider that shoehorns the interface: take a look at this security note as an example:

api3dao/migrate-from-chainlink-to-api3?tab=readme-ov-file#when-to-useapi3partialaggregatorv2v3interface

## Timestamps

With regard to timestamp, I agree they are very important for assessing staleness. ERC-7726 requires that any validation (including timestamp) be performed inside the oracle adapter without leaking that anywhere: see this example.

euler-xyz/euler-price-oracle/blob/master/src/adapter/chainlink/ChainlinkOracle.sol#L63-L74

Just because you nerdsniped me I’m going to share another observation about timestamps. While the providers you mentioned all return a timestamp, the semantics of it is not the same. Chainlink’s timestamp is the *arrival* timestamp of the price update, i.e. the timestamp of the block where the update transaction was included. Pyth’s timestamp on the other hand is the *observation* timestamp, i.e. the windowed timestamp when the price was queried (a third type of timestamp is the price of an AMM-sourced TWAP oracle). The difference in practice is small, however there are circumstances (L2 sequencer is down for example) where not appreciating the semantics may be catastrophic.

Finally I want to disagree that timestamps are ubiquitous. If you want to consume the exchange rate of an LST you can query the project’s Consensus Layer oracle. This is usually a committee that does the accounting and updates the exchange rate at regular intervals. In this case timestamps may not written to the chain. And exchange rate oracles are pretty popular currently so this would make them a major exception to the rule.

Finally some price sources do not have a timestamp. If you’re returning a 1:1 fixed price there is no intrinsic timestamp to that adapter. Yes, you could return `block.timestamp` as a synthetic timestamp but that would be superfluous.


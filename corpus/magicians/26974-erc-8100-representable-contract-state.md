---
source: magicians
topic_id: 26974
title: "ERC-8100: Representable Contract State"
author: cfries
date: "2025-12-06"
category: ERCs
tags: [erc, evm, smart-contracts, state, xml]
url: https://ethereum-magicians.org/t/erc-8100-representable-contract-state/26974
views: 144
likes: 0
posts_count: 2
---

# ERC-8100: Representable Contract State

# ERC-8100: Representable Contract State (IXMLRepresentableState)

> Representable Contract State – an XML-based canonical view of EVM contract state

This proposal specifies a minimal interface `IXMLRepresentableState` that lets an EVM contract expose a *canonical representation of its state* via an XML template with machine-readable bindings to its state and view functions. Off-chain renderers use only `eth_call` at a specific block to materialize that representation.

## Abstract

This ERC introduces `IXMLRepresentableState`, a standard interface and XML binding schema that allows an EVM smart contract to define a static XML template with machine-readable bindings to its state and view functions. Off-chain renderers use this template to build a canonical XML document representing the contract’s state at a specific block, without incurring any on-chain gas cost.

A contract that claims to implement `IXMLRepresentableState` MUST be ***XML-complete***: every piece of mutable state that the author considers semantically relevant MUST be represented in the XML via bindings, so that the rendered XML is a complete representation of the contract at a given (chain-id, address, block-number).

## Motivation

Smart contracts can efficiently orchestrate and process the life-cycle of a financial (derivative) product to an extent that they finally represent *the* financial product itself.

At the same time, many applications require a human-readable, machine-parseable representation of that product and its state: valuation oracles need inputs for settlements, smart bonds and other tokenized instruments need legal terms, term sheets or regulatory reports, and on-chain registries, governance modules or vaults benefit from a stable “document view” of their state.

In the traditional off-chain world, such needs are addressed by standards like FpML, the ISDA Common Domain Model, or the ICMA Bond Data Taxonomy. A common pattern is to treat an XML (or similar) document as the definitive source defining the financial product and then generate code to interact with the corresponding data. When a process modifies or updates properties of the product, developers must synchronize the smart contract’s internal state with the off-chain XML representation. Today, each project typically invents its own set of view functions and off-chain conventions, so clients need bespoke code to map contract state into XML, JSON, or PDF. This makes interoperability, independent auditing, and reuse of tooling harder.

This ERC inverts that pattern by putting the smart contract in the centre. A contract declares that it implements `IXMLRepresentableState` and defines an interface of representable state. Off-chain renderers can then derive a canonical XML document that reflects the semantically relevant state of the contract at a given (chain-id, address, block-number), using only `eth_call` and a standardized XML binding schema. Rendering happens entirely off-chain and does not change state, so there is no gas cost, yet the resulting XML remains cryptographically anchored to the chain.

Typical use cases include:

- Smart derivative contracts that must present their current state to a valuation oracle or settlement engine.
- Smart bonds and other tokenized financial instruments that must generate legal terms, term sheets, or regulatory and supervisory reports.
- On-chain registries, governance modules, and vaults that want a reproducible, auditable document-style snapshot of their state.

By standardizing the Solidity interface and the XML attribute schema, this ERC allows generic tools to consume any compliant contract without project-specific adapters, and to plug directly into existing XML-based workflows in finance and beyond.

---

## Specification sketch (informal)

Very briefly, beyond the header/abstract/motivation above, the ERC specifies:

- A minimal interface IXMLRepresentableState with stateXmlTemplate() returning a UTF-8 XML document.
- Optional extensions:

IRepresentableStateVersioned with stateVersion() (monotonically increasing version of the representable state).
- IRepresentableStateHashed with stateHash() (hash of a canonical state tuple for the representation).
- Convenience combinations for XML: IXMLRepresentableStateVersioned, IXMLRepresentableStateHashed, IXMLRepresentableStateVersionedHashed.

An optional interface `IXMLRepresentableStatePart` with

`statePartXmlTemplate(uint256 partId)`:

- partId selects a partial / projected view of the state (e.g. “settlement context”, “risk summary”).
- Partial views are not required to be XML-complete; they’re just reusable slices of the canonical state.

A binding schema in the `evmstate` namespace, with attributes like:

- single-binding attributes (no semicolons, exactly one binding):

evmstate:call / evmstate:selector / evmstate:returns
- evmstate:format / evmstate:scale
- evmstate:target (element text vs. attribute target)

**multi-binding attributes** (semicolon-separated lists, interpreted positionally):

- evmstate:calls / evmstate:selectors / evmstate:returnsList
- evmstate:formats / evmstate:scales / evmstate:targets

**an array binding profile** that lets a single array-valued binding drive a repeated list of child elements:

- If a binding returns T[] or tuple(T0,...,Tn-1)[], the container element can be marked as an array container via evmstate:item-element="RowName".
- The first direct child  acts as a template row and is deep-cloned once per array item.
- Inside the row, descendants can use evmstate:item-field="k" (0-based index into the tuple / scalar wrapped as (v0)) to bind individual fields to element text or attributes, using the existing scalar format / scale rules.
- More complex shapes (inline lists, aggregates, summaries) are expected to be produced by XSLT or similar post-processing from this repeated-row representation.

Very roughly, a renderer:

- fetches stateXmlTemplate() at a fixed block tag B,
- walks the XML, resolves each evmstate:* binding via eth_call at blockTag = B,
- writes values into element text or attributes (single- or multi-binding mode),
- applies the array profile where present by expanding array containers into repeated rows,
- and fills the context attributes (evmstate:chain-id, evmstate:contract-address, evmstate:block-number).

Snapshot consistency is guaranteed by always using the same block `B` for all calls.

A renderer that does not support the array profile can simply treat `evmstate:item-element` / `evmstate:item-field` and array-typed outputs as errors; it still fully implements the **core scalar profile** of the ERC.

---

## Reference implementation / demos

We have a small set of demo contracts and a Java-based reference renderer (Web3j + DOM XML), including:

- MinimalInstrument – owner, notional, currency, maturity, active flag.
- TestContract – exercises many type/format combinations (uint/int, hex, decimal+scale, iso8601 date/datetime, bytes as hex/base64, etc.) including a multi-binding and array-binding example.
- InterestRateSwapSettleToMarket – IRS with settle-to-market semantics and lastSettlement{time,value}.
- BondDataTaxonomyDemo – ICMA BDT-inspired bond (issuer, ISIN, coupon, dates, etc.) rendered via evmstate bindings.

(work done in personal capacity; does not represent an official position of any employer or institution).

## Architecture Overview

The following diagram gives an overview of a potential architecture using this ERC.

[![architecture-overview](https://ethereum-magicians.org/uploads/default/optimized/3X/f/a/fae3b5aadc0ff91a67bc403c104d24b9d19fc80c_2_559x500.png)architecture-overview845×755 37.7 KB](https://ethereum-magicians.org/uploads/default/fae3b5aadc0ff91a67bc403c104d24b9d19fc80c)

---

Repository: [finmath.net / representable-contract-state · GitLab](https://gitlab.com/finmath/representable-contract-state)

Project Homepage: [finmath Representable Contract State](http://finmath.gitlab.io/representable-contract-state)

## Replies

**cfries** (2025-12-09):

# Partial views & events (by reference)

Contracts may implement the interface `IXMLRepresentableStatePart` to provide templates for specific parts of their state.

One nice side effect of `statePartXmlTemplate(partId)` is that it makes it easy to use *events as triggers* and transport state **by reference** instead of **by value**.

Emitting events is paid by the sender. If you put large chunks of static or slowly changing data directly into event arguments, you keep paying to log the same bytes again and again.

### Example: ERC-6123 Settlement Data by Reference

In ERC-6123, settlement is triggered by

```solidity
event SettlementRequested(address initiator, string tradeData, string lastSettlementData);
```

A naïve interpretation is to put everything needed for the settlement directly into `tradeData` and `lastSettlementData`:

- tradeData: all information needed to value the trade,
- lastSettlementData: everything needed to compute the valuation margin vs. the last settlement.

In practice, large parts of this are static or rarely changing. Emitting the full blobs in every settlement event wastes gas.

If the contract also exposes a representable contract state, it can instead:

- emit SettlementRequested with empty or very small tradeData / lastSettlementData, and
- expect the oracle to fetch the required context from the representable state (e.g. via an EvmXmlRenderer) at the block of the event.

Implementations can decide field-by-field what is passed **by value** (fully inside the event) and what is passed **by reference** (pointing into the representable state). For example, an implementation might put only an index or timestamp of the last settlement into `lastSettlementData` and let the oracle use that as a key into the rendered state. The effect: smaller events, lower gas, but still a deterministic, on-chain-defined settlement view.

## Reference URI Sketch

To make “by reference” machine-friendly, the event payload can carry a small URI that tells the oracle *which* partial view to use.

A simple pattern for references to partial XML views on the same contract is:

```plaintext
evmstate://self/part/

[?key=]
```

- self → “use the contract that emitted this event”
-

 → the uint256 partId you would pass to statePartXmlTemplate(partId)
- key → optional, e.g. settlement index or date

### Example for ERC-6123:

```solidity
lastSettlementData = "evmstate://self/part/1?key=2026-01-02";
```

Here `partId = 1` could be reserved for a “settlement context” partial view. The oracle reads the event, parses `partId` and `key`, then calls

```solidity
statePartXmlTemplate(1)
```

at the event’s block and uses `key` inside that rendered view to locate the relevant settlement entry.

On-chain, `partId` stays a simple `uint256`. If a standard wants globally unique IDs, it can define constants like

```solidity
uint256 constant XML_PART_SETTLEMENT_CTX =
    uint256(keccak256("ERC-6123:XML:SETTLEMENT-CONTEXT:v1"));
```

and still use the same URI form – tools can map that number back to a human-readable label like `"settlement-context"` in their UI.

## Illustration: Contract event state by reference

The following sequence diagram illustrates the concept of fetching contract event state by reference.

[![event-life-cycle](https://ethereum-magicians.org/uploads/default/original/3X/5/f/5f1369f75d0e8da9e034b4bb1a64aa1b6c05518d.png)event-life-cycle1017×714 31.2 KB](https://ethereum-magicians.org/uploads/default/5f1369f75d0e8da9e034b4bb1a64aa1b6c05518d)


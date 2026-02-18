---
source: ethresearch
topic_id: 6162
title: Type Control Execution Environment (EEt) with Formality
author: loredanacirstea
date: "2019-09-19"
category: Architecture
tags: []
url: https://ethresear.ch/t/type-control-execution-environment-eet-with-formality/6162
views: 2403
likes: 9
posts_count: 2
---

# Type Control Execution Environment (EEt) with Formality

We have previously presented [dType](https://github.com/pipeos-one/dType), a decentralized type system and extended the idea [to Eth2](https://ethresear.ch/t/dtype-decentralized-type-system-on-ethereum-2-0/5721/2). We also proposed a [Cache Shard mechanism](https://ethresear.ch/t/a-master-shard-to-account-for-ethereum-2-0-global-scope/5730) for highly used, common-good resources, like type definitions.

With dType, Cache Shard and [Formality](https://github.com/moonad/Formality), any EE can benefit from formal type checking by having its types registered with dType and a type definition compatible with Formality.

## Definitions

dType(EEx) is the implementation of dType corresponding to Execution Environment EEx.

EEt is an execution environment for Formality. It can interpret Formality code and has a dType(EEt) implementation which stores Formality type definitions with references to the shards that use those types.

## Projected Use

Provides formal type management for all EEs. It is composed of dType(EEt) and Formality. dType interfaces EEt with any other EE as well as with the Cache Shard.

[![EE_TypeControl](https://ethresear.ch/uploads/default/original/2X/9/9a0296a323b4f0ecc3b2e0ab5ca7a691f3b3a53f.png)EE_TypeControl960×720 44.5 KB](https://ethresear.ch/uploads/default/9a0296a323b4f0ecc3b2e0ab5ca7a691f3b3a53f)

Suppose we have EE1, EE2, typed execution environments. If there is a need for a new type in EE1, a function `defineType` (deployed by dType with EE1 specifics) will be called with the formal definition for type T1 specific to EE1. This function will call the dType(EEt) `createType` with arguments:

- Tid - proposed type identifier
- EEid - EE identifier
- defFormula - formal definition of Tid for EEid.

Inside `createType` a Formality definition (specific to EEt) for the type `T1` will be generated, stored with a mention that it is used by `EE1` together with the definitions specific to EE1 and EEt.

EEt (Formality) will provide formal type checking for itself and all other typed EEs.

After `T1` is stored in dType(EEt), a pointer to this item will be stored on the Cache Shard and EE1 will store that item also in dType(EE1). From this point forward, `T1` type can be used in EE1 and EEt.

If another execution environment (EE2) smart contract needs to use a EE1 type, that has already been defined, `adoptType` can be called. If EE1 and EE2 are compatible and the EE1 `T1` definition can be reused as-is on EE2, then `adoptType(T1, EE1)` can be called from EE2. Otherwise, a new `defFormula` for EE2 needs to be provided.

Notes:

- one might need a general type definition format, that bridges Formality definitions with other EE definitions.

## Replies

**fubuloubu** (2019-09-25):

Taking a rough overview of this proposal, I think it would add a lot of value to the proposed Phase 2 EE design to keep this in mind, ensuring composibility between different EE contexts remains in tact. I realize now that dType can be used to manage different types of rich state assets (fungible, NFT, etc.) and ensure they remain portable between these contexts. I’ll have to think about this longer to give a better critique, but I just wanted to give a shout-out that this formalism at a high level seems like a great design concept.


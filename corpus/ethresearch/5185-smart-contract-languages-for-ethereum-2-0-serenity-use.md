---
source: ethresearch
topic_id: 5185
title: Smart contract languages for Ethereum 2.0/Serenity use?
author: leafcutterant
date: "2019-03-19"
category: EVM
tags: []
url: https://ethresear.ch/t/smart-contract-languages-for-ethereum-2-0-serenity-use/5185
views: 3061
likes: 3
posts_count: 4
---

# Smart contract languages for Ethereum 2.0/Serenity use?

It would be interesting to discuss what languages do we expect/want/recommend people to use for writing smart contracts for Ethereum 2.0. Honestly, I think I’m just poking around in the dark, but maybe that’s another reason to put this out and gather thoughts.

---

Taking note of what [@gcolvin](/u/gcolvin) [said in the EVM performance topic](https://ethresear.ch/t/evm-performance/2791/20), I think this could be divided into three scenarios:

1. Ethereum won’t switch to eWASM – at least not anytime soon, even after the completion of Serenity. Quite a pessimistic timeline, but it could happen.
2. The switch to eWASM is successful during Serenity, the only place where the EVM comes up is the legacy EVM shard, but EVM-to-eWASM pathways exists and most people/dapps use the eWASM shards anyway.
3. The use of the EVM and eWASM continues in parallel.

# Scenario #1

- How would the current (EVM-era) smart contract language landscape change by the fact that Ethereum is now in Serenity?
- Would there be a need for a new language?

# Scenario #2

Here I suspect the options would be the following:

- Any of the traditional languages that compile to WASM will probably get an eWASM compiler as well. Last time I checked C and C++ had full WASM support, Rust, (Go?) and some others had experimental support, and the long-term goal was to create compilers to as many languages as possible. While this opens up a lot of possibilities, I guess some WASM-supporting languages will be much better for writing Serenity smart contracts than others:

if for nothing else, because of the idiosyncrasies of eWASM compared to WASM;
- because of the (non-)existence of compilers and their quality/developer base (see the current state of WASM compilers);
- because of the idiosyncrasies of the languages. This could be the heaviest one.

Within this, it could be that different languages will be better at different things, e.g. X will be more gas-efficient, Y will yield safer contracts, etc. Which languages will be suitable for what purposes? If this can be ascertained in advance, we could make better recommendations in time and avoid the spread of problematic and unsafe languages.

If I understand it correctly, he **current languages used in Ethereum** will (also) only be usable in Serenity if they get a compiler.

- I heard that one of the goals of the yevm project is to be able to compile yul to eWASM.

Does this mean that, provided that yevm succeeds, Solidity will also be able to compile to eWASM through yul?
- At Devcon, @axic said that Vyper could compile to yul (so that + yevm could = eWASM-compatibility), although I haven’t heard about such effort from Vyper devs. The Vyper repo gives the impression it’s only for the EVM.

Will either **Solidity** or **Vyper** have any non-yul ways of compiling to eWASM, or does this hinge solely on yul and/or yevm?

I don’t know how probable this is, but could it be that eWASM will demand **a new smart contract language** / a new custom language will perform better than all others?

Here, it would also be interesting to look at how traditional languages and smart contract-specific languages compare.

# Scenario #3

Obviously, this would be **some kind of a mix** of what comes up in scenarios #1 and #2.

---

If you have recommendations, answers, additions, please post them!

Also, if I got something wrong (I’m quite certain I did), feel free correct me!

## Replies

**gavan1** (2021-07-09):

Any update on how smart contract developers can get preliminary resources and keep tabs on how to prepare for the smart contact development on the beacon chain?

Unsure why this is so hard to find.

---

**matt** (2021-07-09):

There is no intention of changing how smart contract development is done with eth2. The main change to keep in mind is that the behavior of some opcodes will change and there will be a mechanism to get the data root of shard data.

---

**DavidZ** (2022-06-28):

FWIW， currently all language that can be fully(or mostly)  compiled to wasm are backend/system-level languages. The problem for me is that how could smart contract developer be familar with those languages such as C/C++/Rust.

That may be an issue for wasm to be popular for smart contract developing.

And also ewasm is not pure wasm, it is a subset, so the capability of ewasm to support all full-featured high level language is uncertain to me.


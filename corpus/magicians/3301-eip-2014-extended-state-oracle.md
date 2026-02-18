---
source: magicians
topic_id: 3301
title: "EIP-2014: Extended State Oracle"
author: axic
date: "2019-05-20"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-2014-extended-state-oracle/3301
views: 3686
likes: 2
posts_count: 6
---

# EIP-2014: Extended State Oracle

Discussion board for

https://eips.ethereum.org/EIPS/eip-2014

## Replies

**axic** (2019-05-23):

Some interesting comments from [@fubuloubu](/u/fubuloubu) [were made on the PR](https://github.com/ethereum/EIPs/pull/2014)

---

**axic** (2019-05-23):

I wanted to explain this a bit more. Initially this started out as defining a standard extensible API for data, such as chain id.

Then I also wrote up a draft, which includes EIP-210 (blockhash) support in it, but never pushed that change.

Currently I am considering changing it into a meta EIP describing the guidelines how data contracts (such as chainid history – however [@fubuloubu](/u/fubuloubu) has a [nice proposal for that](https://ethereum-magicians.org/t/eip-1344-add-chain-id-opcode/1131/96), blockhash, logs, etc.) could work.

---

**Arachnid** (2019-05-23):

I do think you should leave the chain ID example out of this. As has been pointed out in one of the chain ID EIPs, returning a simple chain ID isn’t enough, since for mainnet-derived chains, multiple chain IDs have been valid at different points in the past. To avoid this EIP getting bogged down in discussions about the correct interface for checking chain ID, it probably makes more sense to leave this to other EIPs.

A few other thoughts:

- “Non payable” is a Solidity level concept. Instead, you should spell out the consequences, such as that it should revert if value is sent with the call.
- All existing precompiles can have value sent to them. Requiring that this one can’t may impose implementation complexities for clients.
- You need to say something about gas costs for the precompile (even if it’s just that each extension sets its own gas costs).
- You need to specify what happens if it’s called with a nonexistent function ID, or with too little data.
- Unused sections should be marked with a todo or deleted, probably.

---

**holiman** (2019-06-05):

Good points [@Arachnid](/u/arachnid). To add to that :

- If a user sends 4byte 5cf0e8a4 and also data, should it fail or ignore?

Also, the points listed could be moved into the tests-section as suggested tests.

I do, however, think it’s good to include chainid into this EIP, instead of splitting it out into separate EIPs. It helps to keep things simple.

---

**fubuloubu** (2019-06-06):

Chain ID has proven far from being simple. There’s a lot of complexity tied up in how this little `uint256` number is used and what it means, as well as under what conditions it is modified.

I’m comfortable if it just returns the current value, as that’s basically just EIP-1344, but if it has to account for all the complex behavior that can arise from accounting for when the number changes in other calls (such as EIP-1959 and EIP-1965 try and account for), I would not include it into this proposal.

*But* if nothing else related is included, then this proposal is essentially just EIP-1344 with stubs for “other” stuff, which has not been defined yet. That alongside the fact that calls cost extra gas and `chainId` isn’t really a part of the “extended state” (EIP-1344 lifts it from the transaction context) makes me want to recommend differing on this EIP.

It’s complicated enough by itself, all these more complicated proposals for behavior we largely have no historical record for makes me nervous. On top of that, this is going to be a widely-used feature (alongside EIP-712), I want getting `chainId` to be as simple and flexible as possible.


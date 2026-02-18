---
source: magicians
topic_id: 15551
title: "ERC-7504: Dynamic Contracts"
author: nkrishang
date: "2023-08-25"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7504-dynamic-contracts/15551
views: 2201
likes: 8
posts_count: 9
---

# ERC-7504: Dynamic Contracts

Hey all ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12)

I’d love to introduce **ERC-7504: Dynamic Contracts – client-friendly one-to-many proxy contracts.**

This proposal standardizes how ‘proxy-with-many-implementations’ or ‘one-to-many’ proxy contracts can be written with client friendliness and adoption in mind.

https://github.com/ethereum/EIPs/pull/7523

The proposal is a draft, and will likely be edited based on community input. Looking forward to some feedback!

## Replies

**shazow** (2023-08-26):

I like this, adds a lot of clarity over the Diamond metaphors.

I have one suggestion/request: Most other proxies have a fixed known slot that is used for storage, this is mainly to avoid collision – but also it vastly helps for detecting proxies client-side (I work on WhatsABI which tries to comprehensively detect and resolve proxies). Would be useful if this EIP also used a known proxy slot.

For example,

- ERC-1967: Proxy Storage Slots has known _IMPLEMENTATION_SLOT = keccak256("eip1967.proxy.implementation")-1,
- ERC-1822: Universal Upgradeable Proxy Standard (UUPS) has keccak256("PROXIABLE")
- Even DiamondProxy implementations have keccak256("diamond.standard.diamond.storage") - 1

P.S. If you’re looking for more name ideas, here’s a few other potentials: MultiProxy, Multiplexer (or MultiplexProxy), Dispatcher (or DispatchProxy)

---

**spengrah** (2023-08-26):

Very nice!

Have you considered adding an additional `bytes extraData` param to the `ExtensionMetadata` struct? Contracts could in theory use that to facilitate more advanced routing logic.

The example I primarily have in mind is allowing individual users to opt in to protocol upgrades by tagging each extension with a version number, but I’m sure there’d be other interesting use cases as well.

Keen to hear your thoughts. Thanks!

---

**nkrishang** (2023-08-26):

Makes sense [@shazow](/u/shazow).

What would you expect to be stored at a standardized storage slot? In my mind, an EIP compliant contract would implement the `getAllExtensions` function which returns the `n` number of implementation addresses and their associated functions + metadata – regardless of where all of this is stored.

Since you mention your work at WhatsABI, I’d especially like to get your perspective on the usefulness of storing `Extension.metadata` and function signatures, in addition to just implementation addresses + function selectors – with respect to ‘comprehensively detect and resolve proxies’

---

**nkrishang** (2023-08-26):

[@spengrah](/u/spengrah) love the direction! Do you have some simple example in mind on how you’d use such an `extraData` param to facilitate advanced router logic? For more context →

Opt-in / opt-out upgrades is something I’ve thought a lot about while constructing the EIP.

I write smart contracts at thirdweb, and we built our smart wallet factory contracts using the EIP’s pattern, in parallel to writing an EIP.

You can read [here](https://blog.thirdweb.com/smart-contract-deep-dive-building-smart-wallets-for-individuals-and-teams/) about the `DynamicAccountFactory` and `ManagedAccountFactory` contracts. Both factory contracts deploy upgradeable account contracts, however we wrote the `Dynamic` smart wallets to have opt-in upgrades system and `Managed` smart wallets to have a forceful upgrades – all without any additional params.

Here’s a high-level comparison diagram:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/9/94325733ac794ce484ffdf724223959b0ab92503_2_690x239.jpeg)image1600×556 27.3 KB](https://ethereum-magicians.org/uploads/default/94325733ac794ce484ffdf724223959b0ab92503)

A `Dynamic` smart wallet is a router and EIP-7504 compliant, and its parent factory contract is just a regular contract. And so, all upgrades to a smart wallet are controlled locally, by the smart wallet’s admin. This allows building an ‘opt-in’ upgrades system for smart wallets, where the wallet-factory admin can propose upgrades, and wallets can choose to accept.

A `Managed` smart wallet is a router and EIP-7504 compliant, and its parent factory contract is *also* a router and EIP compliant. Here, *all* child smart wallets use their parent factory contract’s `RouterState`, and thus an upgrade to the router map in the wallet-factory is applied “instantly” to all its child smart wallets (effectively, a push upgrade).

---

**shazow** (2023-08-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nkrishang/48/10338_2.png) nkrishang:

> What would you expect to be stored at a standardized storage slot?

[In the DiamondProxy example](https://github.com/mudgen/diamond-3/blob/master/contracts/libraries/LibDiamond.sol#L13), the slot is storing a singleton instance of the `DiamondStorage` struct.

I’m honestly not certain that this is the best approach (perhaps worth asking the DiamondProxy authors how they think about it, if it was worth it), but porting that design would mean that `allExtensions` and `extensionMetadataForFunction` would live inside a singleton struct that would live in a predefined slot.

> In my mind, an EIP compliant contract would implement the getAllExtensions function which returns the n number of implementation addresses and their associated functions + metadata – regardless of where all of this is stored.

I think that’s fine in a vacuum, but the concern behind all the other known slot use is that a contract inheriting from this proxy may also have a function named `getAllExtensions` that means something completely different (it’s not such a unique name). At minimum, might be worth picking something less likely to collide, perhaps `_GET_PROXY_EXTENSIONS` or something?

Another reason I’ve heard for using defined storage slots is it makes it more viable to do in-place upgrades with a different implementation that uses the same storage struct layout.

> Since you mention your work at WhatsABI, I’d especially like to get your perspective on the usefulness of storing Extension.metadata and function signatures, in addition to just implementation addresses + function selectors – with respect to ‘comprehensively detect and resolve proxies’

Hmm, I can’t think of an obvious use case from WhatsABI’s perspective. I guess another approach is to allow the implementation address to optionally implement some kind of `metadata()` function (maybe there’s already an EIP for this?) which can be traversed and called if relevant?

Generally all I expect to get is `address implementation` and `bytes4 selector` pairs. I wouldn’t even expect to get full signatures (I usually get those from 4byte database lookups), though certainly wouldn’t complain. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Personally I would err on the side of doing less as a mandatory ERC, then having optional bonus functions – perhaps something like an optional `_GET_PROXY_SIGNATURE(bytes4 selector) returns (string)`?

All of those strings can add up to tens/hundreds of dollars on L1 during heavy usage.

---

**radek** (2023-08-28):

When reading `RouterState` I initially thought that it would declare the state of the implemented functions.

This rather seams to be the metadata descriptions.

Can we discuss the rationale behind the proposal to store this onchain in the expensive storage vs offchain?

In case some relevant information is needed to be stored on chain for the router, would not be better just to store 1 keccak hash of all extension functions for the current router setup?

---

**nkrishang** (2023-09-05):

Hey all ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12)

Here’s the home repo for the EIP: [GitHub - thirdweb-dev/dynamic-contracts: Architectural pattern for writing dynamic smart contracts in Solidity.](https://github.com/thirdweb-dev/dynamic-contracts)

The repository contains reference implementations of ERC-7504 `Router` and `Router` state, and includes high level presets `BaseRouter` and `BaseRouterWithDefaults` for guided use of the ERC-7504 to build dynamic contracts.

---

**spengrah** (2023-09-29):

Somehow just saw this. Thanks for the response!

What I primarily have in mind is related to protocols with singleton / multi-tenant architectures. Unlike architectures where users each have their own proxy and can therefore have full control over whether their proxy upgrades to new functionality, in singleton architectures many users share the same proxy and so there either needs to be a) coordination across all users to upgrade, or b) only upgrade via forking.

Forking (b) creates obvious challenges when the protocol is the foundation for an ecosystem of other protocols and applications.

And all-or-nothing governance upgrades (a) can create problems for minority users, and especially for other immutable protocols that can’t themselves adjust to account for breaking changes.

Instead, we’d prefer something like option (c), where individual users can opt in to protocol upgrades.

What I’m imagining (and huge credit here to @topocount) is that extensions can be tagged with a version number, individual users register their desired version, and then any calls by or related to that user get routed only to extensions with version <= the user’s registered version. If designed so that extensions can only be added and not removed/replaced, this would provide users with guarantees that any functionality they currently have would remain unless their opted into changes.

Obviously, this doesn’t work with protocols that pool every user’s interactions together, like Uniswap. But for protocols like [Hats Protocol](https://github.com/hats-protocol) (my project), this would be very useful.


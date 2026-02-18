---
source: magicians
topic_id: 22217
title: "ERC-7844: Schema-Safe Storage Primitive for Modular and Upgradeable Ethereum Protocols"
author: wisecameron
date: "2024-12-15"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7844-schema-safe-storage-primitive-for-modular-and-upgradeable-ethereum-protocols/22217
views: 454
likes: 11
posts_count: 14
---

# ERC-7844: Schema-Safe Storage Primitive for Modular and Upgradeable Ethereum Protocols

I’d like to share **ERC-7844**, a proposal introducing **Consolidated Dynamic Storage (CDS)** — a standardized primitive for schema-safe, in-place storage upgrades across modular smart contract systems.

CDS defines a shared storage layer that allows contracts to dynamically create and extend mapped structs **without requiring slot reservations or redeployments**. The core insight is to treat storage like a modular schema layer by decoupling it from execution logic while making it accessible via standardized interfaces and extensible via deterministic hashing.

Most upgradeable systems today use Proxy-Delegate or Diamond architectures, which solve execution routing but still require manual slot management and coordination between contracts. CDS shifts the burden away from developers by defining upgrade-safe **extendable structs**, scoped **storage spaces**, and built-in **RBAC access controls** — all inside a dedicated storage contract.  The result: deterministic layouts, safe (in-place!!) schema evolution, and seamless cross-contract data access, with zero slot math or extra development effort required.

All feedback is very welcome!

Link: [ERCs/ERCS/erc-7844.md at c5b3d58f090a5869077dea3800fe9d41490ebffb · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/blob/c5b3d58f090a5869077dea3800fe9d41490ebffb/ERCS/erc-7844.md)

## Replies

**wizard** (2024-12-15):

[@wisecameron](/u/wisecameron) your methodology is fascinating and tackles one of the more challenging aspects of blockchain systems: achieving true upgradeability without introducing major disruptions. The **Consolidated Dynamic Storage (CDS)** model, as you’ve outlined, strikes a bold balance between adaptability and complexity, and it opens the door to a much-needed evolution in smart contract design.

The idea of **dynamic storage spaces** defined by hash structures is particularly compelling. It introduces a modularity that not only future-proofs the contract but also allows developers to adapt to changing requirements without cumbersome state migrations. This is especially critical for long-lived systems that need to scale and evolve in unpredictable ways.

Your concept of **extendable structs** is equally intriguing. The ability to append new members dynamically brings a level of flexibility rarely seen in existing models. It effectively transforms storage into a living entity, capable of growing alongside the system’s needs. The tradeoff—sacrificing ease of implementation—feels justified for systems where adaptability outweighs simplicity, especially given the potential to abstract away these complexities through reusable patterns and libraries.

However, the unorthodox nature of CDS does highlight areas where the community might need to collaborate further:

1. Auditing and security: Dynamically evolving storage structures could introduce vulnerabilities, particularly in managing boundaries and ensuring that state modifications are well-controlled.
2. Standardization and tooling: For CDS to gain widespread adoption, robust developer tools and clear patterns will be essential to manage complexity and mitigate implementation risks.

Your willingness to embrace tradeoffs for versatility demonstrates a forward-thinking approach, and I can see this methodology being especially impactful in environments like DAO frameworks, modular dApps, and systems with high uncertainty about future requirements. Looking forward to seeing this concept evolve and how the community engages with it! ![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)

---

**Arvolear** (2024-12-15):

Nice one!

This reminds me of an old OpenZeppelin days and their [Eternal storage proxy](https://github.com/OpenZeppelin/openzeppelin-labs/tree/master/upgradeability_using_eternal_storage) pattern.

P.S.

Have you seen [this](https://eips.ethereum.org/EIPS/eip-6224) ERC? Addresses the same issue, but with a slightly different approach.

---

**wisecameron** (2024-12-15):

Great callout on EIP-6224 – the Dependency Registry definitely shares conceptual overlap with CDS, but I agree that the two systems fundamentally diverge in their approach – and I believe it’s actually to quite a great extent under the hood:

• Dependency Registry essentially consolidates the process of linking upgrades between dependent contracts in a traditional proxy-delegate model.  That structural similarity is clear – there’s a central control layer that’s interacting with the rest of the system.

• CDS manages all storage itself, and leverages the extendable structs / storage spaces to scale infinitely in-place.  Similar to Dependency Registry, it’s a ‘central’ contract that has calls propagated to it externally.  Effectively, there is no longer any need to use proxy-delegate for the linked contracts, which are typically pure + globals (although globals can be stored in CDS as well) – their mapped storage is all delegated to the CDS layer.

One cool thing about this is you effectively get implicit delegate access between linked contracts. This access can be secured through basic permission management systems—either at a storage-space level or even down to specific struct members.  This plus the ease of redeploying what are effectively pure contracts makes it really easy to integrate new systems with longstanding ones.

As a footnote, CDS effectively favors making capabilities *exist* and puts the onus on developers to make it secure – but critically, it can have full decentralization with permission management + a governance system.  The centralization of the layer makes that process much more digestible.

Thanks for checking it out and for your reply :).  Big fan of your work by the way, it’s definitely some of the most interesting stuff that pops up in my Linkedin feed.  That ZK resources post has been particularly helpful.

---

**Arvolear** (2025-01-03):

Just took a deeper dive into the ERC. Several questions:

1. Is it correct that the entryIndex from the spec is safeIndex in the reference implementation?
2. It would be great to see an implementation of the put() function. Also, I think it would be great to remember the names of variables put in order to retrieve them by name. Can mapping be used?
3. It is quite hard to understand the overall storage layout after initialization and push steps. A low-level diagram would be highly appreciated.
4. What is the intended use of the system? Is it a standalone contract? Is it a library that manages the storage of a specific smart contact?

Thanks!

---

**wisecameron** (2025-01-03):

Thanks for taking the time to dig deeper!

1. entryIndex actually refers to the sequential index (ie; userData[0] or userData[1]).  The safeIndex stores the last fixed-sized member inserted into the system for bitCount calculations, which is necessary because strings (equivalent to arrays, functionally) have dynamic sizing.
2. Yeah, I think this is a great point regarding naming variables.  My big idea for making the system more palatable in a syntactical sense has just been to build a dedicated VS code extension that provides alias visualization but that could be better.  It’s true that the functionality you just described could be implemented with mappings relatively easily, with a moderate gas cost increase.  I mainly opted not to include this in the base system because the core implementation is already “hard” compared to competing solutions like proxy-delegate.
3. On it, great feedback and agreed.
4. Yeah, the CDS layer is a standalone contract.  Essentially, you link logic contracts to your CDS layer, and let it handle all of your (particularly mapped since they are more cumbersome, although globals are fine too) storage.

The centrality of the CDS layer seems like a big drawback at face value, since it’s a single point of failure AND it’s rather involved in terms of low-level logic and bitwise operations.  However, I think it’s actually the ideal structure fundamentally because you can fully prevent non-authorized invocations with basic permission management, and it’s structurally more palatable and efficient than using a complex array of linked storage dependencies like you see in proxy-delegate.

Given that a CDS layer has fully-malleable storage (ie; you can introduce new storage spaces and custom extendible structs through simple function invocations) a single layer can easily support an arbitrary-sized linked system.  Additionally, the “shared” storage space makes deep integrations with legacy logic trivial, which is a big plus.

The main premise behind CDS is to front-load complexity (which is nullified in practice because I will be open-sourcing a highly-optimized CDS implementation called [HoneyBadger](https://honeybadgerframework.com) in a month or two) in exchange for making storage fully fluid and controllable.  The key reasons why it’s a step up from competing solutions like proxy-delegate are because it’s:

A) More practical to extend storage structures with a function invocation rather than re-deployment.  I don’t claim it’s impossible to add new struct members to a deployed system given proxy-delegate is leveraged, but it’s certainly more cumbersome and error-prone.

B) Structurally, it manages storage in a single layer, which is significantly less complex than leveraging a collection of proxy contracts or diamonds.

C) Equivalent storage space access between linked contracts makes close interoperability relatively trivial.  It’s almost similar to 7208, but I think in a more complete package (at the cost of being harder to implement up-front).

You’re the man for taking the time to read my proposal and reply, those are some great points and it’s obvious that I need to include better clarifications, I sincerely appreciate it ![:handshake:](https://ethereum-magicians.org/images/emoji/twitter/handshake.png?v=12).

---

**wisecameron** (2025-01-11):

Updated proposal is now available!

- Updated Contract
- Significantly improved hashing structure
- Storage-level diagrams
- Uses RFC-2119
- memberIndex, entryIndex, safeIndex, stringIndex clarifications
- Example use cases
- Clear explanation of what the system practically looks like
- Permission management added to spec (required)

To-do:

- string aliasing
- Put implementation

Seeking critical comments – please try to tear it apart.  I think this proposal has a lot of potential and am actively working to optimize it.

---

**Wonderzen** (2025-03-03):

How does ERC-7844 differ from ERC-7201 (Namespaced Storage), which already uses namespaced slots? Why introduce a new standard instead of extending ERC-7201?

---

**wisecameron** (2025-03-04):

Great question!  There are a few reasons why I believe it makes more sense for 7844 to exist as a standalone proposal.

For one, in-place storage upgrades (via extendible structs / storage spaces) require full custom storage management, which diverges the 7844 spec significantly from other proposals.  So while 7844 and 7201 align by providing namespaced storage, they are very different under the hood.  Specifically, I’m referring to the fact that 7201 maps namespaces to a storage offset, whereas 7844 uses a deterministic hashing scheme to allocate storage space metadata and live data within separate logical spaces.

7844’s unique implementation allows it to offer in-place storage upgradeability, allowing developers to allocate new storage spaces and extend their data structures deterministically, and without redeployments.

The best way to look at 7844 is as a *full-service* storage model that combines the benefits (ie; access controls, namespacing, standardized access patterns, upgradeability) of many individual proposals into a single context, while introducing in-place storage upgradeability as a key standalone feature that bolsters its value proposition as a full-service storage management solution.

The central concept is to provide a universal storage model that combines the best ideas about storage management under one easily-accessible banner, while abstracting away manual storage management, effectively reducing the upgrade risk surface for upgrades and simplifying both development and audits.

---

**MASDXI** (2025-03-04):

[@wisecameron](/u/wisecameron)

Is it used for both permission management and full permissions?. I think you should do the table as the access matrix and then map it into the `Id` if *View* is for *Read* only and where the role for *Edit* → *Write*.

[![image](https://ethereum-magicians.org/uploads/default/original/2X/4/4b825a822d6fe71a7164633d97eb67f304dc181a.png)image944×332 14.9 KB](https://ethereum-magicians.org/uploads/default/4b825a822d6fe71a7164633d97eb67f304dc181a)

---

**wisecameron** (2025-03-04):

Great catch full permissions should have ID 6.  In terms of the access matrix, yeah that might make more sense.  Now that I look at it, it would probably be better to just have each of them represent a flag, and then also include a contract flag.  That way, it wouldn’t imply redundant checks for the same operations.

---

**MASDXI** (2025-03-07):

The contract of ERC-7844 provides some access control to manage reading and viewing; however, the storage is still accessible for viewing by `eth_getStorageAt` so there is not much difference from the `private` variable.

---

**wisecameron** (2025-03-07):

That’s a great point, it doesn’t make sense to include access controls for viewing data.

---

**wisecameron** (2025-05-06):

I’ve significantly overhauled the proposal. It’s still a WIP (I have a few outstanding points from Sam to address, and also still need to remove the view permission logic), but the new draft provides a clear sense of what CDS actually is—and why it matters.

One of the bigger challenges here, beyond being busy, is that this is a somewhat atypical proposal archetype. CDS is effectively a new storage *primitive*. The system touches a broad range of issues, and for a while I was struggling to fully crystallize the core narrative in a way that does justice to its scope without becoming overwhelming or disjointed.

I think that cohesion is finally starting to emerge. If you’re curious or working on anything involving upgradeable storage, I’d definitely encourage you to take a look and let me know what you think.

**TL;DR** – CDS eliminates manual slot management and enables redeployment-free storage extension via deterministic, extendible struct spaces. It standardizes storage access patterns (so they don’t break post-upgrade), guarantees single-hop storage proximity (even in multi-contract systems), simplifies dependency management, and helps enforce clean separation between storage and execution. Think: predictable, schema-safe upgrades at the storage layer, without needing to reinvent slot layouts or redeploy when your data model evolves.

**What it looks like in practice:** You deploy a CDS instance once. Then, in your logic contracts, instead of writing and reading from local `mapping` variables, you call a shared CDS layer like:

```auto
put(123, MyStruct.TotalPoints, 0, StorageSpaces.Globals);
```

Here, `TotalPoints` is the index of a struct member, and `0` is the ID of the entry (e.g., the 0th user or entity). You don’t have to manage slot offsets manually, and adding new struct fields can be done without redeployment. It’s a simple model: define your storage schema once, then read from and write to it using fixed indexes across your contracts.


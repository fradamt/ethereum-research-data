---
source: magicians
topic_id: 27119
title: "ERC-8109: Diamonds, Simplified"
author: mudgen
date: "2025-12-12"
category: ERCs
tags: [erc, diamond, proxy]
url: https://ethereum-magicians.org/t/erc-8109-diamonds-simplified/27119
views: 970
likes: 60
posts_count: 69
---

# ERC-8109: Diamonds, Simplified

The Draft “ERC-8109 Diamonds, Simplified,” is here: [ERC-8109: Diamonds, Simplified](https://eips.ethereum.org/EIPS/eip-8109)

All feedback for this standard should be given in the comments below.

Please give your feedback about what you think needs improvement. And also please give feedback on what parts of the design you think are correct and should not be changed. Any kind of real world experience or useful data to consider for the standard is also very helpful.

# Preface

Over the years ERC-2535 Diamonds has been adopted enthusiastically by [numerous projects](https://github.com/mudgen/awesome-diamonds?tab=readme-ov-file#projects-using-diamonds), including a number of high-profile teams:

- ZKsync
- Li.Fi
- Aavegotchi
- Trust Wallet
- Towns Protocol
- Boson Protocol
- Stobox
- Venus Protocol
- hardhat-deploy
- Etherscan

Despite its use, ERC-2535 has sometimes been described as complex or “hard to understand,” even though its actual [requirements](https://eip2535diamonds.substack.com/p/simplicity-of-eip-2535-diamonds-standard) are small, simple and straightforward.

The diamond pattern is not complex. Over time, I’ve noticed that most of the confusion comes from a few specific sources:

1. Unnecessary diamond industry jargon.
2. Relatively complex loupe (introspection) implementations.
3. Diamond storage / namespaced storage, now a more common technique that was unfamiliar to many.
4. Unfamiliarity with diamond contracts.
5. Misinformation about diamonds.
6. Articles that framed diamonds as inherently complex or suitable only for complex systems.

### Important Clarification

Complexity in software can be understood as anything that makes a system harder to understand or work with.

ERC-2535 was never designed to create complex (hard to understand) systems.

Its purpose has always been the opposite — to *reduce* complexity in large smart contract systems by giving developers a structured way to isolate, organize, test, and manage distinct areas of functionality.

When diamonds are used this way, they’re being used as intended.

# What is a Diamond Contract?

A less technical description of diamond contracts can be found [here](https://compose.diamonds/docs/foundations/diamond-contracts).

A diamond is a proxy contract that `delegatecall`s to multiple implementation contracts called facets. It has been standardized by [ERC-2535 Diamonds](https://eips.ethereum.org/EIPS/eip-2535).

# New Proposal

I am proposing a new, simplified standard for diamond contracts. It is meant to make diamonds easier to understand and implement and to improve event functionality.

The new standard addresses these things:

1. Simplified terminology:

Keeps the terms “diamond” and “facet”.
2. Replaces “loupe” with “inspect” or “introspection”.
3. Replaces “diamondCut” with “upgradeDiamond”.
4. A simpler introspection functions.
5. More capable events.
6. Optional upgrade path for existing ERC-2535 Diamond implementations.

### Events

The problem with the `DiamondCut` event is that nothing is indexed and the data is in arrays. This makes it difficult for tools to filter, index, or analyze function and facet changes.

I propose **new** diamond events which can be see in the standard.

These events cost more gas than using the `DiamondCut` event, but they enable more functionality.

The new events:

- solve searchability
- improve GUI interoperability
- allow fine-grained history queries
- help explorers reconstruct upgrade history
- enable blockchain-wide analytics on functions and facets

Gas cost benchmark tests show that the new events increase the overall gas costs of adding functions to diamonds by about 3.5%. See the gas benchmark tests [here](https://github.com/Perfect-Abstractions/Compose/pull/246).

## Request for Feedback

Please read the standard here: [ERC-8109: Diamonds, Simplified](https://eips.ethereum.org/EIPS/eip-8109)

I am actively seeking feedback on this proposal. Please share your thoughts on any aspects that could be improved, simplified, or clarified.

Additionally, if you agree with specific design choices, please let me know why. Validating the current design is just as important as finding edge cases. Broad community review is essential to ensuring this standard is robust and ready for adoption.

This new standard is going to need a new name, what should it be called?  Here are some ideas:

- Diamonds, Simplified
- Diamond Pattern
- Diamond Standard (trademark dispute)
- What else?

## Replies

**vitali_grabovski** (2025-12-12):

Hello [@mudgen](/u/mudgen),

I like the simplification and the fact that the diamond-pattern spirit and overall diamond idea are still present. Almost all of the suggested changes look good to me. I still have several considerations, concerns, and points to discuss:

1. Name suggestion: Upgradable and Modular Proxy Contract
2. What do you think about making upgradeDiamond(FacetFunctions[] calldata _addFunctions, FacetFunctions[] calldata _replaceFunctions, bytes4[] calldata _removeFunctions, address _init, bytes calldata _functionCall) as simple as upgradeDiamond(bytes memory params)? As mentioned it is an optional method, to not strict each project with its own implementation and input/output parameters.
3. In my projects, I also rely heavily on facetAddress(bytes4 _functionSelector) during upgrades when calling from other contracts. It is very useful and gas-efficient. I encourage you to keep it as part of the standard (making it not optional).
4. Does this version support an immutable function: 1. An immutable function is an external function that cannot be replaced or removed (because it is defined directly in the diamond, or because the diamond’s logic does not allow it to be modified).

Happy to give more feedback when the standard draft is ready.

---

**kyle** (2025-12-12):

Having separate events for Added/Replaced/Removed is a great addition.  That would make my code much cleaner, except…

> To reconstruct the complete upgrade history will require retrieving all the past DiamondCut events as well as all new events defined in this standard.

You’re totally right about this, and this is the boat that I’m in.  So it wouldn’t be of much benefit to me, unfortunately ![:confused:](https://ethereum-magicians.org/images/emoji/twitter/confused.png?v=12)

Along the lines of immutable functions mentioned by [@vitali_grabovski](/u/vitali_grabovski) above, I’ve always found the Diamond Proxy’s “immutability” story to be a little faulty.

I understand that you can lock specific facets, or create immutable functions, but there’s no mechanism that prevents the diamond’s owner from creating a new facet that messes with DiamondStorage in a way that might affect those immutable functions.  In the spirit of updating the standard, have you considered any way this might be possible, to create *truly* immutable facets/functions, storage included?

---

**mudgen** (2025-12-13):

[@vitali_grabovski](/u/vitali_grabovski)

> I like the simplification and the fact that the diamond-pattern spirit and overall diamond idea are still present. Almost all of the suggested changes look good to me.

Yes, that’s great!

> Name suggestion: Upgradable and Modular Proxy Contract

Thank  you for this name suggestion.

> What do you think about making upgradeDiamond(FacetFunctions[] calldata _addFunctions, FacetFunctions[] calldata _replaceFunctions, bytes4[] calldata _removeFunctions, address _init, bytes calldata _functionCall) as simple as upgradeDiamond(bytes memory params)? As mentioned it is an optional method, to not strict each project with its own implementation and input/output parameters.

I think that `upgradeDiamond(bytes memory params)` is much simpler and I really like that. However this function is standardized for tooling, such as a GUI or a command line program that can work with any diamond that supports the standard diamond upgrade function.  The problem with a `bytes` parameter is that such a general tool would not know what format or what exact data to give the `upgradeDiamond`s function unless it is specified, unless it is standardized.

As mentioned in the standard however, users can use their own `upgradeDiamond(bytes memory params)` or other upgrade function that they want to use or specify.  In addition, new standards can be built on top of this one for different ways to build or upgrade diamonds.

> In my projects, I also rely heavily on facetAddress(bytes4 _functionSelector) during upgrades when calling from other contracts. It is very useful and gas-efficient. I encourage you to keep it as part of the standard (making it not optional).

I am very glad to know this and I was unsure about adding `facetAddress(bytes4 _functionSelector)` to the standard or not.  It is likely it will be added to the standard. It is very simple to implement and very gas efficient as you mentioned.  I am very interested in how you are using it. Can you tell me more details about how you are using it and how it is useful  to you?

> Does this version support an immutable function: 1. An immutable function is an external function that cannot be replaced or removed (because it is defined directly in the diamond, or because the diamond’s logic does not allow it to be modified).

Yes, same as ERC-2535 Diamonds.

> Happy to give more feedback when the standard draft is ready.

I look forward to that feedback!

---

**mudgen** (2025-12-13):

Hi [@kyle](/u/kyle)

> Having separate events for Added/Replaced/Removed is a great addition. That would make my code much cleaner, except…

That’s great to know!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kyle/48/15898_2.png) kyle:

> To reconstruct the complete upgrade history will require retrieving all the past DiamondCut events as well as all new events defined in this standard.

You’re totally right about this, and this is the boat that I’m in. So it wouldn’t be of much benefit to me, unfortunately ![:confused:](https://ethereum-magicians.org/images/emoji/twitter/confused.png?v=12)

But indexers would not need any of the old `DiamondCut` events to construct the current state of your converted diamond, as said here:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> Note: This migration transaction acts as a complete ‘state snapshot’. Indexers only interested in the current state of the diamond can start indexing from this transaction onwards, without needing to parse the legacy DiamondCut history.

Is there some reason this would not handle your needs?

> Along the lines of immutable functions mentioned by @vitali_grabovski above, I’ve always found the Diamond Proxy’s “immutability” story to be a little faulty.
>
>
> I understand that you can lock specific facets, or create immutable functions, but there’s no mechanism that prevents the diamond’s owner from creating a new facet that messes with DiamondStorage in a way that might affect those immutable functions. In the spirit of updating the standard, have you considered any way this might be possible, to create truly immutable facets/functions, storage included?

Yes, it is possible to have immutable functions or lock facets in some way.  But as you mentioned, new functions can always be added that can mess with storage.  So there isn’t much or any point to have immutable functions. Immutable functions just make your diamond less flexible.  So I generally don’t use immutable functions and don’t recommend them.

Immutability is generally an all or nothing proposition with diamonds.  A diamond is either completely immutable or it is not immutable.  It is possible to make unquestionably, completely immutable diamonds and there are multiple ways to do it.  Here are two ways to do it:

1. Add all facets/functions of a diamond in the constructor function of a diamond contract, but don’t add any update/upgrade function to the diamond.  Since there is no upgrade function, it is not possible to add/replace/remove any functions in the diamond. That makes it completely immutable from the point of deployment, like any other contract. This is my favorite method, because it is very clean.
2. Deploy a diamond with an upgrade function and use it or not. At some point perform an upgrade that removes the upgrade function. This causes the diamond to become completely immutable because there is no upgrade function to add/replace/remove functions. This approach has the advantage that a diamond can be upgradeable and then become immutable when it is deemed ready.

All this being said, there may be a way to combine different contracts, so some data is stored in an external contract, so that a diamond is partially immutable and it makes some sense, but I haven’t fully explored that possibility.

---

**DavidKim** (2025-12-13):

Interesting and happy to see the Diamond further heading towards a more intuitive developer experience!

As an engineer that has used Diamond in many smart contracts, I understand the objective of this change and also agree that this could developers understand the concept of Diamond more easily.

I would be curious to know your thoughts on the optional migration path.

Whether the newly updated standard will be enforced, or if the migration will be optional, and more stay as a recommendation. Especially given that many Diamond already exists out there.

There are several reasons I can think of, which makes the optional migration more suitable and realistic:

1. Although most Diamonds, implement the DiamondCut and DiamondLoupe capability through each respective Facets (e.g., DiamondCutFacet, DiamondLoupeFacet) there will be Diamonds that have these functionalities within the proxy itself. Where migrations are not quite easy.
2. Diamond contracts are already very widely adopted that it’s being used in Smart Contract Wallets, Bridges, DEXs, and many more. These security critical systems usually need to have a very strong justification(e.g., new version with new features, security patch, etc) for contract updates and it’s likely that compliance with an updated ERC standard may not be sufficient.

In general, I think this suggestion a good consideration for the Diamond ecosystem.

Also, I believe it would be worth considering flagging the compatibility aspect of existing Diamonds and state that the migration is optional, although recommended.

---

**mudgen** (2025-12-13):

[@DavidKim](/u/davidkim)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/davidkim/48/13667_2.png) DavidKim:

> Interesting and happy to see the Diamond further heading towards a more intuitive developer experience!
>
>
> As an engineer that has used Diamond in many smart contracts, I understand the objective of this change and also agree that this could developers understand the concept of Diamond more easily.

This feedback is very much appreciated!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/davidkim/48/13667_2.png) DavidKim:

> I would be curious to know your thoughts on the optional migration path.
>
>
> Whether the newly updated standard will be enforced, or if the migration will be optional, and more stay as a recommendation. Especially given that many Diamond already exists out there.
>
>
> There are several reasons I can think of, which makes the optional migration more suitable and realistic:
>
>
> Although most Diamonds, implement the DiamondCut and DiamondLoupe capability through each respective Facets (e.g., DiamondCutFacet, DiamondLoupeFacet) there will be Diamonds that have these functionalities within the proxy itself. Where migrations are not quite easy.
> Diamond contracts are already very widely adopted that it’s being used in Smart Contract Wallets, Bridges, DEXs, and many more. These security critical systems usually need to have a very strong justification(e.g., new version with new features, security patch, etc) for contract updates and it’s likely that compliance with an updated ERC standard may not be sufficient.

The migration will **not** be enforced.  Upgrading to the new standard will be completely optional and at the discretion of users/developers. ERC-2535 Diamonds is already a good working standard.

**Existing Loupe Functions**

Existing ERC-2535 Diamonds implementations do not need to remove or replace the DiamondLoupeFacet or the existing loupe/introspection functions because they are compatible with this new standard. So when migrating to this new standard the existing loupe functions can be left alone. Of course they could be removed, if possible, if the developer wants to remove them, but it is not required or needed.  If you like the existing loupe functions, or want to keep using them, definitely keep them.

**Immutable diamondCut function**

In some implementations the **diamondCut** function may be defined directly in the diamond proxy contract.  In this case the `diamondCut` function cannot be removed. I can think of a couple solutions to this:

1. Add the new upgradeDiamond function and simply don’t use the diamondCut function anymore. The next solution is more rebust.
2. In some way in your contract remove the permission for anyone to call the diamondCut function so it will always revert if anyone calls it. Add the new upgradeDiamond function or your own upgrade function and give permission for the diamond owner or admin to call it.
 For example, if using the owner variable for permission to call diamondCut, create a new state variable, such as owner2 or better name, and enable that to call the new upgrade function. Then set the owner variable to address(0) so it can’t be used anymore and will cause calls to diamondCut to revert. Make sure that you have updated any other admin function to use owner2.

> In general, I think this suggestion a good consideration for the Diamond ecosystem.
>
>
> Also, I believe it would be worth considering flagging the compatibility aspect of existing Diamonds and state that the migration is optional, although recommended.

That’s great. Yes, makes sense, and will do this in the standard. These are important points and I appreciate you pointing them up.

---

**Vagabond** (2025-12-14):

Hi, I think this is a great proposal.

I’d like to add some inputs from an implementation perspective.

For migrating an existing ERC-2535 diamond to this new standard, a multisend upgrade can be used in a single atomic transaction:

- add upgradeDiamond
- add functionFacetPairs
- remove diamondCut
- emit the new events

This aligns well with the idea of treating the migration as a full state snapshot for indexers and tooling.

Regarding loupe functions, I think they are still useful. Some frameworks, tools, and existing infrastructure already depend on them, so keeping them as optional introspection helpers makes sense rather than removing them entirely.

In my case, I use `facets()` to retrieve the full facet list and pass that data directly into off-chain database queries for metadata lookup

One additional point worth highlighting is that a traditional proxy with a single implementation contract is conceptually similar to a diamond with one facet. The key difference is that diamonds can scale naturally beyond the 24KB contract size limit, which becomes a default advantage.

---

**mudgen** (2025-12-14):

[@Vagabond](/u/vagabond) Excellent perspective and clarity. I really appreciate comments and feedback like yours.

Yes, the loupe/introspection functions from ERC-2535 Diamonds continue to be useful, even though they are not required by the new standard. New implementations can also, optionally, add the introspection functions from ERC-2535 Diamonds.

> One additional point worth highlighting is that a traditional proxy with a single implementation contract is conceptually similar to a diamond with one facet. The key difference is that diamonds can scale naturally beyond the 24KB contract size limit, which becomes a default advantage.

That is true, but there is more advantage here. A diamond enables you to break up functionality into separate, smaller on-chain pieces (much smaller than 24KB), so that you can understand, test, manage and then compose separate units of functionality into a complete system.

Software systems can be understood by breaking them up into well understood pieces, which are then composed in an organized, orderly fashion.

---

**Vagabond** (2025-12-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> That is true, but there is more advantage here. A diamond enables you to break up functionality into separate, smaller on-chain pieces (much smaller than 24KB), so that you can understand, test, manage and then compose separate units of functionality into a complete system.
>
>
> Software systems can be understood by breaking them up into well understood pieces, which are then composed in an organized, orderly fashion.

Yes, thank you for the clarification. That is a very strong point.

We can keep small, easy to test logic isolated in different facets and ship quickly from the beginning, while still having native room to scale both vertically by replacing function selectors and horizontally by adding more function selectors.

This also allows multiple teams to cooperate more easily, since everyone can work independently on their own isolated logic blocks and then compose everything together using the Diamond.

---

**vitali_grabovski** (2025-12-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kyle/48/15898_2.png) kyle:

> any way this might be possible, to create truly immutable facets/functions, storage included?

There is no approach to prevent access to storage from facets added in the future. Removing the upgrade method (`diamondCut`) may be an option, but this is not a path for everyone.

Do you have suggestions on what a truly immutable selector might look like while preserving upgradability?

---

**ahmadnajari56-eng** (2025-12-15):

“This is a necessary and well-targeted proposal. The approach of using separate, indexed events (`DiamondFunctionAdded/Replaced/Removed` ) fundamentally solves the key tracking and querying limitations of ERC-2535. A ~3.5% gas increase is a reasonable trade-off for the gained analytical and tooling capabilities.

Two technical points for consideration:

1. Should functionFacetPairs() support an iteration/pagination pattern instead of returning the entire array, to avoid issues with diamonds containing a very large number of functions (e.g., thousands of selectors)?
2. In the proposed migration path, taking a snapshot of the current state and emitting all addition events in a single transaction could become extremely gas-intensive. Is there a more optimized mechanism suggested (e.g., batched emission or initial off-chain indexing)?

Name suggestion: “ERC-2535-Diamond-Events” or “Diamond Standard v2 (Simplified)” are clear and distinguishable.

Thank you for this essential improvement to the standard.”

---

**kavsky** (2025-12-15):

Hi [@mudgen](/u/mudgen),

We have been using a variant of ERC-2535 in production for almost 3 years. Over that time we have done hundreds of diamond cuts and built a lot of internal tooling around upgrades and introspection, so I am very interested in this proposal.

I agree with the core motivation. Diamonds are not inherently complex, but the terminology and the way tooling consumes loupe and events has made the learning curve look worse than it is. The proposed event model is a real improvement for explorers, indexers, and GUIs.

A few concrete thoughts:

1. I would strongly consider including a simple per-selector lookup function as part of the expected introspection surface, even if optional. Something like facetAddress(bytes4 selector) is extremely useful in day-to-day debugging and tooling, and it is also what many developers intuitively look for first. functionFacetPairs() is a great base primitive, but having both makes integrations and manual inspection smoother.
2. Pausability is not a diamond concern per se, but in practice almost every production system needs it and many teams forget it until it is too late. It might be worth documenting a minimal recommended pausability pattern for diamonds. My preference would be a global pause at the diamond level, optionally extendable to per-facet pause. In our production systems we also allow a whitelist of selectors that remain callable while paused (unpause, upgrade, and sometimes a small set of emergency or read-only actions). This keeps break-glass operations possible without leaving the system half-open.
3. Rollback or revert plan support is valuable operationally, especially with timelocks. In our setup (diamond owner is a timelock) we routinely queue both the upgrade and a rollback transaction that reverses it, so we have an immediate escape hatch if something goes wrong. I understand this is likely out of scope for the standard itself, but it may be worth mentioning as an operational best practice for timelock-governed diamonds.

If useful, I am happy to share more real-world notes from running diamonds in production and the tooling patterns we ended up with.

Thanks for pushing this forward,

[@kavsky](/u/kavsky)

---

**mudgen** (2025-12-15):

[@kavsky](/u/kavsky)

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/k/4da419/48.png) kavsky:

> We have been using a variant of ERC-2535 in production for almost 3 years. Over that time we have done hundreds of diamond cuts and built a lot of internal tooling around upgrades and introspection, so I am very interested in this proposal.
>
>
> I agree with the core motivation. Diamonds are not inherently complex, but the terminology and the way tooling consumes loupe and events has made the learning curve look worse than it is. The proposed event model is a real improvement for explorers, indexers, and GUIs.

I am very glad to know this, thank you.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/k/4da419/48.png) kavsky:

> Pausability is not a diamond concern per se, but in practice almost every production system needs it and many teams forget it until it is too late. It might be worth documenting a minimal recommended pausability pattern for diamonds. My preference would be a global pause at the diamond level, optionally extendable to per-facet pause. In our production systems we also allow a whitelist of selectors that remain callable while paused (unpause, upgrade, and sometimes a small set of emergency or read-only actions). This keeps break-glass operations possible without leaving the system half-open.

I am glad to know this.

I think pausability is important functionality. I don’t think pausability will be a part of this new standard but   I plan to provide a pattern of this in [Compose](https://compose.diamonds/), the new smart contract library I am working on based on diamonds.  In Compose, I think I am thinking of a different approach than has been used before.  The general approach I am thinking of is this:  A `pause(bytes4[] calldata _selectors)` function takes a list of function selectors and removes them from the diamond (or replaces them with functions that revert with a `Paused()` error). That effectively pauses them since they don’t exist in the diamond anymore.  Then an `unpause(bytes4[] calldata__selectors)` adds those functions back, using the same facets they were using before. Events would be emitted that said functions were paused/unpaused. There could even be a special introspection function that returns an array of paused functions [@kavsky](/u/kavsky) what do you think of this approach to pausing functions?

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/k/4da419/48.png) kavsky:

> Rollback or revert plan support is valuable operationally, especially with timelocks. In our setup (diamond owner is a timelock) we routinely queue both the upgrade and a rollback transaction that reverses it, so we have an immediate escape hatch if something goes wrong. I understand this is likely out of scope for the standard itself, but it may be worth mentioning as an operational best practice for timelock-governed diamonds.

I am again glad to know this.

I think both pausability and rollback functionality are good subjects for additional standards built on top of this standard, and provided by contract libraries, such as Compose.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/k/4da419/48.png) kavsky:

> If useful, I am happy to share more real-world notes from running diamonds in production and the tooling patterns we ended up with.

Yes, I want this please. This is valuable information. I would like to understand better how you implemented pausability and rollback.  And I would like to see the other patterns and tooling you have been using.  I would like to know what you are happiest about and what things have been the most trouble or given concerns. What’s the best way for you to share your notes?

I am glad that you like the changes proposed for a refined version of a standard for diamonds.

---

**mudgen** (2025-12-15):

[@kavsky](/u/kavsky)

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/k/4da419/48.png) kavsky:

> I would strongly consider including a simple per-selector lookup function as part of the expected introspection surface, even if optional. Something like facetAddress(bytes4 selector) is extremely useful in day-to-day debugging and tooling, and it is also what many developers intuitively look for first. functionFacetPairs() is a great base primitive, but having both makes integrations and manual inspection smoother.

Understood, I’m going to add `facetAddress(bytes4 _selector)`  to the new standard.

---

**mudgen** (2025-12-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ahmadnajari56-eng/48/16724_2.png) ahmadnajari56-eng:

> “This is a necessary and well-targeted proposal. The approach of using separate, indexed events (DiamondFunctionAdded/Replaced/Removed ) fundamentally solves the key tracking and querying limitations of ERC-2535. A ~3.5% gas increase is a reasonable trade-off for the gained analytical and tooling capabilities.

[@ahmadnajari56-eng](/u/ahmadnajari56-eng) Thank you for this feedback!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ahmadnajari56-eng/48/16724_2.png) ahmadnajari56-eng:

> Should functionFacetPairs() support an iteration/pagination pattern instead of returning the entire array, to avoid issues with diamonds containing a very large number of functions (e.g., thousands of selectors)?

Thank you for asking this question. No, because `functionFacetPairs()` is meant to be called offchain and can return an array with many thousands of functions. It can return about 60,000 functions. Gas benchmark testing was done [here](https://github.com/Perfect-Abstractions/Compose/pull/251).

However, in case an implementation wants iteration/pagination an implementation can add such introspection functions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ahmadnajari56-eng/48/16724_2.png) ahmadnajari56-eng:

> In the proposed migration path, taking a snapshot of the current state and emitting all addition events in a single transaction could become extremely gas-intensive. Is there a more optimized mechanism suggested (e.g., batched emission or initial off-chain indexing)?

Thanks for bringing this up. The events can actually be emitted over multiple upgrade transactions. I updated the proposal to say that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ahmadnajari56-eng/48/16724_2.png) ahmadnajari56-eng:

> Name suggestion: “ERC-2535-Diamond-Events” or “Diamond Standard v2 (Simplified)” are clear and distinguishable.

Thank you for these suggestions!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ahmadnajari56-eng/48/16724_2.png) ahmadnajari56-eng:

> Thank you for this essential improvement to the standard.”

You are welcome!  Thank you for your helpful feedback!

---

**CypherVae** (2025-12-16):

Hey there [@mudgen](/u/mudgen), I saw your tweet re the trademark dispute and have a few thoughts. I had a look at the cease and desist letter LOL and it seemed to me that the company only owns the word mark “diamond standard” in the U.S. & owns a very specific *logo-and-word mark* in different countries around the world.

In general, one cannot simply allege a breach unless the infringement is used (in layman terms) in the same circumstances/context of the registered mark(s). I had a brief look at the ‘classifications’ of the registered marks (9, 36, 42), they broadly relate to the scientific research/production/supply of (a good or service) - I presume, actual diamonds. ![:joy:](https://ethereum-magicians.org/images/emoji/twitter/joy.png?v=12) Not sure if a reasonable person implementing the ERC would be convinced that there is some “confusion” as alleged in the cease and desist letter ![:joy:](https://ethereum-magicians.org/images/emoji/twitter/joy.png?v=12)

p.s. this is not legal advice, just wanted to share my thoughts; feel free to Chatgpt more about trademark disputes and check out the WIPO website. ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=12)

---

**mudgen** (2025-12-16):

[@CypherVae](/u/cyphervae) Thanks, I appreciate your input.

---

**maxnorm** (2025-12-24):

Great work on the proposition Nick! [See the draft here](https://github.com/mudgen/ERCs/blob/master/ERCS/erc-8109.md)

This simplified version will ease the adoption of devs. The new events will bring new analytic capabilities for off-chain tooling & indexes.  Looking foward for this!

My only concern is the ban on immutable functions inside the diamond contract. This seems restricting for projects. I totally agree that this ban makes the function → facet mental model clearer but banning this removes the potential for immutable functions in diamonds. (while the concept of immutable function usage can be debated).

Right now, you either have a whole mutable diamond or an immutable one (by removing the upgrade function) .  This ban removes the granualiry level of immutable function.

Since you proposed a path for ERC2535 with legacy immutable functions ([See Here](https://github.com/mudgen/ERCs/blob/master/ERCS/erc-8109.md#erc-2535-diamonds-with-legacy-immutable-functions)), I think the ban can be omitted, or more like a warning/advice and using this clear requirement path as a MUST to make them compliant with the new events and inspect functions.

OR

proposed the addition of a new mapping (selector to bool) to flag a specific function as immutable and block replacement or removal on upgrades

I’ll be happy to hear more from projects using these immutable functions and see if they are really important (since you can always make a new facet that accesses the storage slot to bypass the immutability).

---

**mudgen** (2025-12-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maxnorm/48/16806_2.png) maxnorm:

> Great work on the proposition Nick! See the draft here
>
>
> This simplified version will ease the adoption of devs. The new events will bring new analytic capabilities for off-chain tooling & indexes. Looking foward for this!
>
>
> My only concern is the ban on immutable functions inside the diamond contract. This seems restricting for projects. I totally agree that this ban makes the function → facet mental model clearer but banning this removes the potential for immutable functions in diamonds. (while the concept of immutable function usage can be debated).
>
>
> Right now, you either have a whole mutable diamond or an immutable one (by removing the upgrade function) . This ban removes the granualiry level of immutable function.
>
>
> Since you proposed a path for ERC2535 with legacy immutable functions (See Here), I think the ban can be omitted, or more like a warning/advice and using this clear requirement path as a MUST to make them compliant with the new events and inspect functions.
> OR
> proposed the addition of a new mapping (selector to bool) to flag a specific function as immutable and block replacement or removal on upgrades
>
>
> I’ll be happy to hear more from projects using these immutable functions and see if they are really important (since you can always make a new facet that accesses the storage slot to bypass the immutability).

Yes, you are right. Thanks for this very helpful feedback. I updated the standard so it no longer bans immutable functions. Now it specifies and explains them.

---

**hiddentao** (2025-12-30):

Hey Nick, great to see the Diamond Standard moving forward!

Overall the proposal is great. Just one consideration came to mind: wouldn’t it be more efficient to emit batch events, e.g `DiamondFunctionsAdded`?

Also, just seeing compose.diamonds now - looks good, and I have some thoughts for that too.


*(48 more replies not shown)*

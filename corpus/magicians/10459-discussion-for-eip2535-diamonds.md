---
source: magicians
topic_id: 10459
title: Discussion for EIP2535 Diamonds
author: mudgen
date: "2022-08-20"
category: EIPs
tags: [proxy-contract]
url: https://ethereum-magicians.org/t/discussion-for-eip2535-diamonds/10459
views: 4966
likes: 1
posts_count: 19
---

# Discussion for EIP2535 Diamonds

The original discussion of EIP2535 Diamonds is here: [EIP-2535: Diamonds · Issue #2535 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/2535) and it is still active.

A discussion thread was created here because EIPs now require EIP discussions to occur on Fellowship of Ethereum Magicians and EIP pull requests no longer work without a discussion link that points here.

Discuss EIP2535 Diamonds here or in the original thread.

The standard is here: [ERC-2535: Diamonds, Multi-Facet Proxy](https://eips.ethereum.org/EIPS/eip-2535)

References and resources for diamonds are here:

https://github.com/mudgen/awesome-diamonds

The main diamond reference implementation is here:

https://github.com/mudgen/diamond-1-hardhat

## Replies

**SamWilsn** (2022-09-13):

Why have three separate `FacetCutAction`s? Seems like you could get by with just `Replace`:

- Remove is equivalent to Replace with a facetAddress of zero.
- Add is equivalent to Replace.

---

**SamWilsn** (2022-09-13):

Are the loupe function required or optional?

---

**mudgen** (2022-09-13):

Great question. The reason is to prevent mistakes and errors in upgrades.

For example if someone means to add a new function and so they try to add it not realizing there is already a function with that selector/function signature in the diamond so they end up replacing a function they didn’t intend to replace.

Or someone means to replace a function and they send the wrong function selector for it and so the old function doesn’t get removed and the new function gets added.

By being explicit about adding/replacing/removing functions the diamondCut function can check that the intended action can be done and revert with a reason if it can’t.

---

**SamWilsn** (2022-09-13):

Hm, I see. I think doing a check-and-set would be even safer:

```nohighlight
function diamondCut(bytes4[] functionSelectors, address[] oldValues, address[] newValues)
```

For example, `Add` would be:

```nohighlight
diamondCut([0x00abcdef], [address(0)], [0x0000...0000]);
```

---

**mudgen** (2022-09-13):

The loupe functions are required.  They are required for interoperability, tooling and reliability.  There are a couple articles written on the subject:

- Why On-Chain Loupe Functions are Good - by Nick Mudge 💎
- Diamond Loupe Functions - DEV Community 👩‍💻👨‍💻

---

**SamWilsn** (2022-09-13):

I don’t fully understand exactly how the loupe functions are implemented. Are they an interface on the diamond itself, or implemented in a facet?

If the loupe functions are provided by a facet:

- Can they be removed by diamondCut?
- How do they get information from diamondCut? Reading the storage during a delegatecall?

---

**SamWilsn** (2022-09-13):

Sorry for the unorganized barrage of questions ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12)

Why does this restriction exist:

> If the _init value is not address(0) then _calldata must contain more than 0 bytes or the transaction reverts.

---

**SamWilsn** (2022-09-13):

I don’t solidity much, but the loupe interface seems like it’ll require a second separate mapping of function selectors by facet address? What if you went with something like:

```nohighlight
interface IDiamondLoupe {
    // Returns the address of the facet implementing the given function selector.
    function facetOf(bytes4 selector) external returns (address);

    // Number of slots in the sparse functions array.
    function functionsLength() external returns (uint256);

    // Get the function selector and facet at the given index.
    // An address of zero indicates an empty slot.
    // Slots may be reused or left blank as functions change.
    function functionByIndex(uint256 index) external returns (bytes4, address);
}
```

I think that’s fairly efficiently implementable with a `mapping(bytes4 => address)` (which you already need), and an array of function selectors.

---

**mudgen** (2022-09-13):

The loupe functions could be implemented directly in a diamond proxy contract.  But I think it is better to implement the loupe functions in a facet and add the functions to a diamond. This is how the [reference implementations](https://github.com/mudgen/diamond) do it.

Implementing the loupe functions in a facet makes it so that the loupe functions are deployed to a blockchain only one time and can then be added to any diamond that is compatible with their implementation.

> Can they be removed by diamondCut?

Yes, but only if a diamond has the `diamondCut` function. Immutable diamonds don’t have a `diamondCut` function or any other upgrade function. The `diamondCut` function is optional in a diamond so that diamonds can be immutable or start off as upgradeable and later become immutable when the time is write.  There were some tweets about that today: https://twitter.com/mudgen/status/1569736257940652034

> How do they get information from diamondCut? Reading the storage during a delegatecall?

Yes. `diamondCut` stores function selectors and facet addresses in a diamond proxy contract’s contract storage. The loupe functions get that data and return it.

---

**mudgen** (2022-09-14):

> Sorry for the unorganized barrage of questions

That’s okay, questions are good. Great to ask questions here. Questions can also be asked in the [Diamond Discord](https://discord.gg/kQewPw2).

Also a lot of questions are answered in articles on this website: https://eip2535diamonds.substack.com/

> Why does this restriction exist:
>
>
>
> If the _init value is not address(0) then _calldata must contain more than 0 bytes or the transaction reverts.

It is slightly arbitrary but the `_calldata` value can serve two purposes, hold function call data, or custom data.

If `_init` is `address(0)` then `_calldata` contains custom data (if any data at all) that is being sent to a `diamondCut` implementation.

If `_init` is not `address(0)` then `_calldata` contains function call data. It does not make sense if `_init` is not `address(0)` but `_calldata` has no data,  because a function call can’t be done on the `address(0)` address, so it reverts.  `_init` variable holds the address that the `_calldata` function call is executed on.

---

**mudgen** (2022-09-14):

I like the interface you suggest.

The current `IDiamondLoupe` is currently implemented with one mapping and one array of selectors. Some details of loupe function implementations are in this article: [Diamond Loupe Functions - DEV Community 👩‍💻👨‍💻](https://dev.to/mudgen/why-loupe-functions-for-diamonds-1kc3)  The reference implementations can also be looked at.

One thing to note is that the technical details (the Specification section specifically) of EIP2535 is essentially final and not subject to change at this point and has been that way for awhile. It is because the standard has been fleshed out over a year and a half period  and it is established with how it is now, and there are a [number of projects and tools](https://github.com/mudgen/awesome-diamonds#projects-using-diamonds) in production with it, and a bunch of [smart contract security audits](https://github.com/mudgen/awesome-diamonds#audits). The reason it is not final in the EIP is because of formatting issues.

---

**SamWilsn** (2022-09-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> The loupe functions could be implemented directly in a diamond proxy contract. But I think it is better to implement the loupe functions in a facet and add the functions to a diamond. This is how the reference implementations do it.
>
>
> Implementing the loupe functions in a facet makes it so that the loupe functions are deployed to a blockchain only one time and can then be added to any diamond that is compatible with their implementation.

That makes sense.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> Can they be removed by diamondCut?

Yes

That sounds like the loupe functions are actually *somewhat* optional then? I guess if an owner removes the loupe functions, the diamond is no longer a diamond until the owner re-adds them?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> That’s okay, questions are good. Great to ask questions here. Questions can also be asked in the Diamond Discord.

I’d rather keep the discussion here, if that’s alright. This is where we do most EIP discussion.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> It does not make sense if _init is not address(0) but _calldata has no data

I believe you can call a contract with no calldata, and it executes the fallback function? Seems odd to prohibit that without a good reason.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> The current IDiamondLoupe is currently implemented with one mapping and one array of selectors.

Ah, okay. I guess iterating through the selector array isn’t too bad, because there aren’t that many functions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> One thing to note is that the technical details (the Specification section specifically) of EIP2535 is essentially final and not subject to change at this point and has been that way for awhile.

I’m just here doing my best to give feedback before the last call deadline ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12) EIPs should propose the best version of themselves, and not be beholden to existing implementations. That said, I do completely understand that EIP-2535 has been stable for some time and that most of my suggestions are terrible!

---

**SamWilsn** (2022-09-14):

> An immutable function is a function that is defined directly in a diamond and so cannot be replaced or removed.

> All immutable functions must be emitted in the DiamondCut event as new functions added.

Do these together mean what I think they mean? In a diamond’s constructor, it must emit `DiamondCut` events for every function it implements directly?

---

**mudgen** (2022-09-14):

> An immutable function is a function that is defined directly in a diamond and so cannot be replaced or removed.
>
>
>
> All immutable functions must be emitted in the DiamondCut event as new functions added.

> Do these together mean what I think they mean? In a diamond’s constructor, it must emit DiamondCut events for every function it implements directly?

Yes, but one `DiamondCut` event can be emitted for all immutable functions in the diamond constructor.

---

**mudgen** (2022-09-14):

> That sounds like the loupe functions are actually somewhat optional then? I guess if an owner removes the loupe functions, the diamond is no longer a diamond until the owner re-adds them?

Yes, it is technically no longer a diamond without the loupe functions.

> I’d rather keep the discussion here, if that’s alright. This is where we do most EIP discussion.

Sounds good and makes sense.

> I believe you can call a contract with no calldata, and it executes the fallback function? Seems odd to prohibit that without a good reason.

Yes, you have a good point. I think you are right and the rule that prohibits that should be removed. I think this can be removed without disruption. It is arbitrary and I don’t think it would break anything to remove it. Thanks for pointing this out.

> I’m just here doing my best to give feedback before the last call deadline  EIPs should propose the best version of themselves, and not be beholden to existing implementations. That said, I do completely understand that EIP-2535 has been stable for some time and that most of my suggestions are terrible!

Make sense and I agree with you.  I don’t think your suggestions are terrible. I like your suggestion for the loupe functions, but I don’t think the loupe functions should change at this point. I much appreciate your review and feedback concerning the standard and related parts. It was this kind of attention and feedback that really helped develop the standard in the first place, as can be seen from [past discussions of it](https://github.com/ethereum/EIPs/issues/2535).  And more attention and thought about things is beneficial.

I am really happy and appreciate that you are digging into this standard and I want to help you understand it and related things as much as I can. And I understand that part of that can also be figuring out how things should and should not be for yourself. I am a big proponent of people looking, figuring out, understanding and discovering things for themselves rather than just accepting what someone else says.

---

**mudgen** (2022-10-20):

EIP-2535 Diamonds reached “Final” status today: [EIP-2535: Diamonds, Multi-Facet Proxy](https://eips.ethereum.org/EIPS/eip-2535)

---

**a2m** (2022-10-31):

Hi Nick,

I’m new to diamonds, is there a simple guideline with examples on how to use diamonds?

from my understanding so far is I deploy the diamond contract (as found on your github), deploy other contracts that will be part of the diamond (facets), create facecuts for these contracts, then call the diamondcut with these facecuts… correct?

my other question is what’s the difference between diamond and solidstatediamond?

Thanks Nick

---

**mudgen** (2022-12-06):

Hi [@a2m](/u/a2m),

There are a number of guides and tutorials on diamonds. Here is one:

- The Diamond Standard (EIP-2535) Explained: Part 1
The Diamond Standard (EIP-2535) Explained: Part 2

More resources can be found from [Awesome Diamonds](https://github.com/mudgen/awesome-diamonds).


---
source: magicians
topic_id: 26973
title: Revising ERC-2535 Diamonds to Simplify and Improve the Terminology
author: mudgen
date: "2025-12-06"
category: ERCs
tags: [erc, upgradeable-contract]
url: https://ethereum-magicians.org/t/revising-erc-2535-diamonds-to-simplify-and-improve-the-terminology/26973
views: 468
likes: 25
posts_count: 21
---

# Revising ERC-2535 Diamonds to Simplify and Improve the Terminology

Probably the biggest complaint over the years of ERC-2535 Diamonds has been the specialized terminology that was introduced by it. If you thought I took the diamond analogy too far by using too many diamond-industry-specific terms, **you are right. I did. I admit it.**

Fortunately the ERC-2535 Diamonds standard can be revised to improve this aspect. It *is* possible to change a final Ethereum standard.

EIP-1 says this:

> A Final EIP exists in a state of finality and should only be updated to correct errata and add non-normative clarifications.

“Non-normative clarifications” means explanations that do not change the rules of the standard. They clarify wording or improve understanding without altering any requirements or behaviors defined by the ERC.

The terms **diamond** and **facet** are good. The terms **DiamondCut** and **loupe** are not so good, and it’s time to do something about it.

# Analysis & Plans

The diamond analogy has been useful for conceptualizing the smart-contract architecture defined by ERC-2535. It gives developers a mental model for how a system can present a single unified interface while being internally composed of multiple parts that share data.

The analogy:

**Physical  diamond:**

1. Facets are different appearances or faces of a physical diamond. They all share the same center of the diamond.
2. Facets are different appearances and functionality of an ERC-2535 diamond. They share the same Ethereum address and the same contract storage, which can be considered the “center” of a smart contract.

This analogy is imperfect, but useful.

## Term: diamond

The term **diamond** (or **diamond contract**) is valuable because it communicates a specific type of proxy architecture. Simply calling it a “proxy contract” is too broad—every standardized proxy has its own name, such as the [UUPS proxy](https://rareskills.io/post/uups-proxy).

A diamond is a proxy contract that implements [ERC-2535 Diamonds](https://eips.ethereum.org/EIPS/eip-2535), also known as the diamond standard.

**Is there an existing software term that captures what a diamond is?**

No.

There are software concepts that resemble *parts* of the diamond architecture—routers, dynamic dispatch, virtual method tables, and even the Facade design pattern. Each of these describes partially how a diamond works, usually the mechanism for selecting or invoking code.

But none of them describe a system where:

1. Multiple components share a single identity.
2. All components operate on the same shared storage.
3. Components can be added, replaced, or removed without changing that identity or losing state.

These three properties—**shared identity, shared storage, and optional modular upgradeability**—define the diamond pattern. No existing software term captures all of them.

**Verdict**: diamond is good, keep it.

## Term: facet:

The term “facet” to describe an implementation contract for a diamond is absolutely useful. It is short, descriptive, and specific to diamonds. When working with smart contract systems that implement EIP-2535 Diamonds, the term “facet” communicates immediately and clearly. Such systems have multiple facets, and some have many facets.

The term “facet” is needed to distinguish contracts from others. “Implementation contract” is unwieldy and general.

**Verdict**: facet is good, keep it.

## Term: loupe

In the diamond industry, a loupe is a small magnifying glass used to examine diamonds. In ERC-2535 Diamonds, a loupe is a set of four external functions that return information about what is inside a diamond – what functions it provides and from which facets.

It might be clever or fun to use the term “loupe,” but it adds unnecessary cognitive overhead for people learning or working with diamonds. It is unnecessary terminology, and some people strongly dislike it.

The established software term is **introspection**, and it already accurately describes the functionality.

I plan to revise the ERC-2535 Diamonds standard to replace the term “loupe” with introspection.

IDiamondLoupe → IDiamondIntrospection.

The actual introspection function names:

- facets()
- facetFunctionSelectors(address _facet)
- facetAddresses()
- facetAddress(bytes4 _functionSelector)

are already well named and will **not** change.

This is a non-normative change: removing “loupe” from ERC-2535 Diamonds does not change how diamonds work or behave. Existing implementations may update their documentation to replace “loupe” with “introspection” or add a note about the name change.

**Verdict:** remove the name loupe.

## Term: Cut

`diamondCut` is the name of the optional function that is used to add/replace/remove functions in a diamond.

`DiamondCut` is the name of the event that is emitted when any functions are added or replaced or removed in a diamond.

The term “cut” (used in `diamondCut` and `DiamondCut`) is far less useful than the terms “diamond” and “facet”. In a physical diamond, facets are created by cutting the diamond. This analogy is unnecessary and adds cognitive overhead. No analogy is useful or needed to understand adding/replacing/removing functions in a diamond.

I want to replace the `diamondCut` upgrade function with `upgradeDiamond`. And I want to replace the `DiamondCut` event with `DiamondUpgraded`. I propose the following interfaces:

```Solidity
interface IDiamond {
    enum Action {Add, Replace, Remove}
    // Add=0, Replace=1, Remove=2

    struct FacetChange {
        address facetAddress;
        Action action;
        bytes4[] functionSelectors;
    }

    /**
     * @notice Emitted when functions are added, replaced, or removed in a
     *         diamond.
     *         This event is emitted when a diamond is created (when facets
     *         are added for the first time) and during all subsequent upgrades.
     *
     * @dev Each FacetChange entry describes changes to a facet:
     *      - Add:     Adds new function selectors from a facet.
     *      - Replace: Changes the facet that implements existing function
     *                 selectors.
     *      - Remove:  Deletes function selectors so the diamond no longer
     *                 exposes them.
     *
     *      The diamond uses these facet changes to update its internal
     *      selector-to-facet lookup table, enabling or altering the contract's
     *      external interface.
     *
     * @param _facetChanges The list of facet changes applied in this upgrade.
     *                      Each entry specifies the facet address, the action
     *                      taken, and the function selectors affected.
     *
     * @param _data         Arbitrary data with no prescribed format. This may
     *                      contain initialization or configuration data
     *                      associated with the upgrade, or it may be empty
     *                      if no additional processing is required.
     */
    event DiamondUpgraded(FacetChange[] _facetChanges, bytes _data);
}

interface IUpgradeDiamond is IDiamond {
    /**
     * @notice Add, replace, remove any number of functions in a diamond.
     * @dev    This function is optional. Diamonds can be immutable or
     *         upgradeable.
     * @param _facetChanges The facet changes to apply, including addresses,
     *         actions, and function selectors.
     * @param _data Optional additional data with no specified format.
     */
    function upgradeDiamond(
        FacetChange[] calldata _facetChanges,
        bytes calldata _data
    ) external;
}
```

Existing diamonds emitting `DiamondCut` will continue to work exactly as before, and will continue to be supported by the standard. Tools and explorers should support both event names.

Existing projects that have the `diamondCut` function can keep using it if they want to. Or they can use `diamondCut` to replace `diamondCut` with `upgradeDiamond`.

Since ERC-2535 Diamonds is a Final Ethereum standard, making such a change would require the overwhelming agreement and support of existing projects that have implemented the standard, as well as those that plan to adopt it. It would also require the support and agreement of tools that support the standard such as [Louper](https://louper.dev), [Etherscan](https://etherscan.io), and others, as well as newer tools such as [Compose](https://compose.diamonds) and [Herd](https://www.herd.eco).

Even then, I do not know if the EIP editors will allow the change. But if [inheritance can be removed from Solidity](https://x.com/mudgen/status/1994927714726212077), maybe anything can happen.

Or instead of making changes to the standard, should we just make a Diamond 2 standard?

I am interested in your feedback, your ideas, and your reactions, so please leave a comment.

## Replies

**d3mage** (2025-12-06):

I totally support the renaming of ‘loupe’. It is confusing.

---

**mudgen** (2025-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/d3mage/48/6661_2.png) d3mage:

> I totally support the renaming of ‘loupe’. It is confusing.

[@d3mage](/u/d3mage)

I am glad to know. What do you think about replacing the `diamondCut` function with `upgradeDiamond` and replacing the event `DiamondCut` with `DiamondUpgraded`?

---

**Vagabond** (2025-12-07):

I’m going to adopt this.

I personally prefer the original “loupe” and “cut” naming, but technically, `DiamondIntrospection` and `DiamondUpgraded` make the codebase more self-descriptive.

---

**Data-Nexus** (2025-12-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> Verdict: remove the name loupe.

I agree with `introspection` over `loupe`.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mudgen/48/1027_2.png) mudgen:

> And I want to replace the DiamondCut event with DiamondUpgraded.

In regards to `diamondCut` I could go either way, the name was pretty easy to understand what it does (additional changes may cause unnecessary confusion). But I can see how “cutting a diamond” adds a facet by removing material whereas `upgradeDiamond` implies ‘adding to it’. `modifyDiamond` might also better encompass changing facets (add, replace & remove) and it’s pretty immediately clear what the function is doing.

---

**innovinitylabs** (2025-12-08):

Can we use the word “index” instead of “loupe”. Diamond and Facets are understandable but “Loupe” is too much industry term, took me a while to get used to.

---

**giuseppecrj** (2025-12-08):

Great proposal! renaming to introspection is great for visibility. Most blockchain scanners support Diamond standard proxy but renaming diamondCut might take a while since a lot of projects built tooling with that selector in mind already.

---

**0xdantrinh** (2025-12-09):

I agree with replacing the name of the event to DiamondUpgraded. To be honest, I did not even realize the importance of the DiamondCut event showing that functions have been added or removed until you talked about it in this context

---

**mudgen** (2025-12-09):

Yes, the event makes upgrades transparent on the blockchain – so people can see exactly what functions are add/replced/removed from which facets, over time.

---

**radek** (2025-12-10):

Yep, some terminology is confusing. I have a hard time to come up with the corresponding terminology for currently being designed framework of alternative + versioned facets. Concluded towards:

diamond - facet(s) - (facet) shape(s).

[@mudgen](/u/mudgen) would such convention fit?

ad ERC change - pls, see RFC approach. It is better to create the new standard marking it as the replacement for ERC 2535 - see RFC example: [Information on RFC 7230 » RFC Editor](https://www.rfc-editor.org/info/rfc7230)

It is not only about the standard. It is also about the documentation and tutorials. These are the ones out there that refer to 2535 with the former syntax.

Btw, `facet` term - this one is particularly confusingly similar to `facade`  ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

ad `diamondCut` - it is not only about upgrading - Given that diamondCut allows for adding, replacing, AND removing functionality, the term **“upgrade”** might feel slightly incomplete, as removing a function is often seen as a downgrade or a refactoring rather than a traditional improvement.

But ofc, more adhering to UUPS is `upgrade`

---

**mudgen** (2025-12-12):

[@radek](/u/radek) Understood, thank you for this feedback. I appreciate it.

> ad ERC change - pls, see RFC approach. It is better to create the new standard marking it as the replacement for ERC 2535 - see RFC example: Information on RFC 7230 » RFC Editor
>
>
> It is not only about the standard. It is also about the documentation and tutorials. These are the ones out there that refer to 2535 with the former syntax.

Yes, that make sense. I agree with that. I’m going to make a new standard.

[@radek](/u/radek) Proposal for a new standard here: [Proposal for a Simplified Standard for Diamond Contracts - #5 by mudgen](https://ethereum-magicians.org/t/proposal-for-a-simplified-standard-for-diamond-contracts/27119/5)

> Btw, facet term - this one is particularly confusingly similar to facade
>
>
> ad diamondCut - it is not only about upgrading - Given that diamondCut allows for adding, replacing, AND removing functionality, the term “upgrade” might feel slightly incomplete, as removing a function is often seen as a downgrade or a refactoring rather than a traditional improvement.
>
>
> But ofc, more adhering to UUPS is upgrade

Yes, thank you for this feedback. I appreciate it.

---

**vitali_grabovski** (2025-12-12):

Hello [@mudgen](/u/mudgen),

If I were you, I would keep the terminology as it is. In my opinion, the community is already familiar with these terms, and they are not particularly hard to figure out.

Many legacy names in various projects stay unchanged simply because developers are accustomed to them. Additionally, much of the existing Diamond tooling (libraries, frameworks, plugins) already uses this terminology, and there hasn’t been any real concern about it being difficult to understand.

_

However, if terminology changes are still being considered, I’d suggest the following alternatives for improved clarity:

- Diamond Proxy Contract → Upgradable and Modular Proxy Contract (UMPC)
- DiamondCut → Upgraded

---

**kyle** (2025-12-12):

> the community is already familiar with these terms, and they are not particularly hard to figure out.

I’m in this camp.  Going [all in on an analogy](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap) is not inherently an issue, and people get familiar with it pretty quickly.

I see especially little benefit in going through the pain of changing terms, and still keeping the “Facet” term, which was easily the most confusing part at first.  Loupe and DiamondCut were not at all a cognitive burden, since they were truly analogous to introspection and upgrade.

The terminology here wasn’t what was confusing, it was the overall architecture needing some time to really digest.

I’m (softly) against this idea.   It just feels totally unnecessary to me.

---

**ahmadnajari56-eng** (2025-12-12):

I support replacing “loupe” with “introspection” for clarity. For the upgrade function, consider creating a new standard (e.g., ERC-2536) with a clearer name like `modifyDiamond` while keeping ERC-2535 stable. This balances improvement with backward compatibility.

---

**mudgen** (2025-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vitali_grabovski/48/15798_2.png) vitali_grabovski:

> If I were you, I would keep the terminology as it is. In my opinion, the community is already familiar with these terms, and they are not particularly hard to figure out.
> Many legacy names in various projects stay unchanged simply because developers are accustomed to them. Additionally, much of the existing Diamond tooling (libraries, frameworks, plugins) already uses this terminology, and there hasn’t been any real concern about it being difficult to understand.

[@vitali_grabovski](/u/vitali_grabovski) I agree with you.  I’m not going to change anything in ERC-2535 Diamonds.  ERC-2535 Diamonds is a good, established and working standard.  But I am planning to make a new standard that is the same as ERC-2535 Diamonds, but with a few things simplified and better events,  as you already gave me some great feedback about.  Much appreciated.

> However, if terminology changes are still being considered, I’d suggest the following alternatives for improved clarity:
>
>
> Diamond Proxy Contract → Upgradable and Modular Proxy Contract (UMPC)
> DiamondCut → Upgraded

Thank you for these name ideas.

---

**mudgen** (2025-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/innovinitylabs/48/16210_2.png) innovinitylabs:

> Can we use the word “index” instead of “loupe”. Diamond and Facets are understandable but “Loupe” is too much industry term, took me a while to get used to.

I agree with you about “Loupe” being too much an industry term. Thank for the suggestion of the term “index” for this.

---

**mudgen** (2025-12-13):

[@Data-Nexus](/u/data-nexus)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/data-nexus/48/16665_2.png) Data-Nexus:

> In regards to diamondCut I could go either way, the name was pretty easy to understand what it does (additional changes may cause unnecessary confusion). But I can see how “cutting a diamond” adds a facet by removing material whereas upgradeDiamond implies ‘adding to it’. modifyDiamond might also better encompass changing facets (add, replace & remove) and it’s pretty immediately clear what the function is doing.

Makes sense. Thanks for this feedback. Much appreciated.

---

**mudgen** (2025-12-13):

[@ahmadnajari56-eng](/u/ahmadnajari56-eng)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ahmadnajari56-eng/48/16724_2.png) ahmadnajari56-eng:

> I support replacing “loupe” with “introspection” for clarity.

I am glad to know, thank you.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ahmadnajari56-eng/48/16724_2.png) ahmadnajari56-eng:

> For the upgrade function, consider creating a new standard (e.g., ERC-2536) with a clearer name like modifyDiamond while keeping ERC-2535 stable. This balances improvement with backward compatibility.

[@ahmadnajari56-eng](/u/ahmadnajari56-eng) I totally agree with you. I made the proposal for a new standard here: [Proposal for a Simplified Standard for Diamond Contracts - #5 by mudgen](https://ethereum-magicians.org/t/proposal-for-a-simplified-standard-for-diamond-contracts/27119/5)

---

**mudgen** (2025-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/giuseppecrj/48/16658_2.png) giuseppecrj:

> Great proposal! renaming to introspection is great for visibility. Most blockchain scanners support Diamond standard proxy but renaming diamondCut might take a while since a lot of projects built tooling with that selector in mind already.

[@giuseppecrj](/u/giuseppecrj) Thank you for this feedback. I appreciate it. Instead of changing anything in ERC-2535 Diamonds, I decided to make a new standard: [Proposal for a Simplified Standard for Diamond Contracts - #5 by mudgen](https://ethereum-magicians.org/t/proposal-for-a-simplified-standard-for-diamond-contracts/27119/5)

---

**mudgen** (2025-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kyle/48/15898_2.png) kyle:

> I’m in this camp. Going all in on an analogy is not inherently an issue, and people get familiar with it pretty quickly.
>
>
> I see especially little benefit in going through the pain of changing terms, and still keeping the “Facet” term, which was easily the most confusing part at first. Loupe and DiamondCut were not at all a cognitive burden, since they were truly analogous to introspection and upgrade.
>
>
> The terminology here wasn’t what was confusing, it was the overall architecture needing some time to really digest.
>
>
> I’m (softly) against this idea. It just feels totally unnecessary to me.

[@kyle](/u/kyle) I am glad to know this, thank you.  In my opinion ERC-2535 Diamonds is a good working standard just the way it is. I decided not to change anything in it.  I am proposing a new standard though here: [Proposal for a Simplified Standard for Diamond Contracts - #5 by mudgen](https://ethereum-magicians.org/t/proposal-for-a-simplified-standard-for-diamond-contracts/27119/5)

---

**mudgen** (2025-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vagabond/48/16220_2.png) Vagabond:

> I’m going to adopt this.
> I personally prefer the original “loupe” and “cut” naming, but technically, DiamondIntrospection and DiamondUpgraded make the codebase more self-descriptive.

[@Vagabond](/u/vagabond) I am glad to know this, thank you.  I decided not to make changes to ERC-2535 Diamonds. Instead I am proposing a new standard: [Proposal for a Simplified Standard for Diamond Contracts - #5 by mudgen](https://ethereum-magicians.org/t/proposal-for-a-simplified-standard-for-diamond-contracts/27119/5)


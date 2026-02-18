---
source: magicians
topic_id: 16249
title: Disclosure of a security flaw in ERC-20 transferring workflow
author: Dexaran
date: "2023-10-24"
category: ERCs
tags: [erc, token]
url: https://ethereum-magicians.org/t/disclosure-of-a-security-flaw-in-erc-20-transferring-workflow/16249
views: 1403
likes: 5
posts_count: 8
---

# Disclosure of a security flaw in ERC-20 transferring workflow

## ERC-20 Losses Calculator

This script calculates the amount of tokens that were lost because of the described problem:

[ERC-20 Losses Calculator](https://dexaran.github.io/erc20-losses/)

As of 11/2/2023 there are $228,722,284 lost.

##

The following describes a security flaw in the transferring workflow of [ERC-20](https://github.com/Dexaran/EIPs/blob/patch-1/EIPS/eip-20.md) token standard. It must be taken into account that all token standards that declare full backwards compatibility with [ERC-20](https://github.com/Dexaran/EIPs/blob/patch-1/EIPS/eip-20.md) also inherit this security flaw, for example ERC-1363.

##

Security flaw disclosures are an important part of software development. Increasing awareness of the problem helps the development community to implement solutions and minimize the damage that a particular flaw can deal to the users.

##

### design overview

[ERC-20](https://github.com/Dexaran/EIPs/blob/patch-1/EIPS/eip-20.md) standard declares two methods of transferring tokens: (1) `transfer` function and (2) `approve` & `transferFrom` pattern. `approve` & `transferFrom` is supposed to be used to deposit tokens to contracts. The `transfer` function is supposed to be used for transfers between externally owned addresses however this is not directly written in the specification. If the tokens are sent to a contract address via the `transfer` function then the recipient contract will not recognize the depoist.

###

**The `transfer` function does not notify the recipient of an incoming transaction which makes error handling impossible.** Error handling is an essential part of secure software development. If tokens are sent to any contract via the `transfer` function and the recipient contract does not support extraction of tokens (i.e. it doesn’t implement any functions which would allow to send tokens out) then it is a clear case of user error that must be reverted. For example if a user would send plain ether to a contract that does not explicitly declare that it is intended to accept ether deposits then such transaction would be reverted automatically. In case of [ERC-20](https://github.com/Dexaran/EIPs/blob/patch-1/EIPS/eip-20.md) tokens a user can push the token contract into incorrect state where a user no longer controls the tokens by picking a wrong function when performing a transaction.

**A burden of determining the method of transferring tokens is placed on the user in a situation where one option is obviously wrong and will result in a loss of funds.** Prompting a user to make a decision on the internal logic of the contract combined with the lack of an implementation of error handling for users actions is another security failure that can result in incorrect token contract behavior and a loss of funds for the end user.

###

As of 11/2/2023 there are $228,722,284 worth of lost [ERC-20](https://github.com/Dexaran/EIPs/blob/patch-1/EIPS/eip-20.md) tokens.

##

Copyright and related rights waived via [CC0](https://github.com/Dexaran/EIPs/blob/patch-1/LICENSE.md).

## Replies

**sullof** (2023-10-24):

I’m uncertain about the practicality of formalizing this as a standard, considering the use of such a function appears largely pertinent to the contract’s owner. In other words, the necessity to publicly expose this interface is debatable.

However, entertaining the idea of interface exposure for a moment, I believe the EIP could be enhanced by steering away from prescribing a specific function, such as the one you’ve provided:

```auto
function rescueERC20(address _token) onlyOwner external {
  amount = IERC20(_token).balanceOf(address(this));
  IERC20(_token).transfer(msg.sender, amount);
}
```

Instead, I advocate for the adoption of a more generic interface:

```auto
interface IRescueERC20 {
  function rescueERC20(address _token) external;
}
```

This approach would grant implementers the flexibility to define the rescue mechanics that best suit their needs, whether it be through Ownable, AccessControl, or an alternative method. This not only promotes adaptability but also encourages a broader range of use cases and implementations, ensuring the EIP’s relevance and utility across diverse applications.

---

**Dexaran** (2023-10-25):

> I’m uncertain about the practicality of formalizing this as a standard, considering the use of such a function appears largely pertinent to the contract’s owner. In other words, the necessity to publicly expose this interface is debatable.

I would like to note that the main goal of this EIP is not to standardize the token extraction method but to highlight a security flaw of ERC-20 and the need to switch to a safer standard.

> Instead, I advocate for the adoption of a more generic interface:
> …
> This approach would grant implementers the flexibility to define the rescue mechanics that best suit their needs, whether it be through Ownable, AccessControl, or an alternative method.

I agree with this point, the more general definition looks reasonable.

---

**sullof** (2023-10-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> I would like to note that the main goal of this EIP is not to standardize the token extraction method but to highlight a security flaw of ERC-20 and the need to switch to a safer standard.

That problem has been raised a long ago with many proposals to solve the issue. The most prominent and the only used (even if not too much) is [EIP-777](https://eips.ethereum.org/EIPS/eip-777).

---

**Dexaran** (2023-11-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> That problem has been raised a long ago with many proposals to solve the issue. The most prominent and the only used (even if not too much) is EIP-777

Well, this is exactly the reason why I stopped working on ERC-223 promotion in 2017. I thought that there are a lot of smart guys who can solve such an obvious problem without me. In 2017 there were about $1M lost due to ERC-20 flaw.

Now its 2023 and there are about $100M of lost funds in ERC-20 tokens. This is how a disaster looks like. And the “smart guys” haven’t solved it still. That’s why I’m resurrecting ERC-223 standard as it’s the main standard that is designed to solve this problem and replace ERC-20.

Here is a script that calculates the “lost” tokens [ERC-20 Losses Calculator](https://dexaran.github.io/erc20-losses/)

---

**sullof** (2023-11-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> Well, this is exactly the reason why I stopped working on ERC-223 promotion in 2017

I totally remember that long discussion. IMO, 223 was a good proposal. Maybe not perfect, but if implemented then, many problems could have been avoided.

---

**SamWilsn** (2023-11-10):

Couple non-editorial comments:

> The transfer function is supposed to be used for transfers between externally owned addresses however this is not directly written in the specification

Do you have a source? I’ve always just assumed the two patterns were for push and pull payments, and didn’t have anything to do with who was making the call. I’d love to read more about that!

---

**Dexaran** (2023-11-10):

- If you have PUSH transacting methods - you don’t need PULL methods for anything. This is how ether works for example.
- ERC-20 standard was proposed in 2015. At this time there was a bug in Ethereum Virtual Machine 1024 call stack depth. The approve & transferFrom method of the ERC-20 standard was introduced so that this bug does not affect tokens. It was not a smart design, it was a weird quirk to address an old bug that doesn’t exist anymore.
- In Tangerine Whistle hardfork the call stack depth problem was solved. This happened on block 2463000 in 2016. At this time approve & transferFrom method became obsolete and the ERC-20 standard should have been considered deprecated.

Here is an old comment from Vitalik regarding the call stack depth:

[![1_ovvWQr2lxjS2tVxzXYl2Yg](https://ethereum-magicians.org/uploads/default/optimized/2X/d/d3e37fe532b1d70d787e25a7aab985259cc07b9c_2_690x273.webp)1_ovvWQr2lxjS2tVxzXYl2Yg1878×745 90.8 KB](https://ethereum-magicians.org/uploads/default/d3e37fe532b1d70d787e25a7aab985259cc07b9c)

So, gathering the facts:

1. At the moment of ERC-20 creation there were two transacting methods: transfer & approve+transferFrom
2. It was not possible to implement PUSH TX model in a smart-contract at all due to 1024-call-stack depth
3. The authors most certainly knew about PUSH TXs because ether does implement it
4. Without notifying a recipient of an incoming transaction it is not possible to make a contract recognize the deposit - so the transfer function couldn’t notify recipients in any way at that moment

If the `transfer` function couldn’t be used for contract deposits and there was an `approve & transferFrom` method exactly for contract deposits just because there was no easier way to address 1024-call-stack-depth - what could be the purpose of the `transfer` other than making EOA to EOA transfers?

I can’t find any source that would directly say `transfer` is for EOA to EOA, `approve` is for deposits to contracts. But this is the only way of how it could be used.

Also the first contract on Ethereum that was supposed to interact with tokens was the Alex van de Sande’s “Unicorn Meat Grinder”. It was on the page maintained by Ethereum Foundation and I think it doesn’t exist anymore but I found a recap of the article. The Unicorn Meat Grinder transparently says “you must not deposit funds to contract directly - instead you approve them”.



      [gist.github.com](https://gist.github.com/alexvandesande/eca0b87da89ab28fa50c)





####


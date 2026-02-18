---
source: magicians
topic_id: 9554
title: "EIP-5143: Slippage protection for Tokenized Vaults"
author: Amxx
date: "2022-06-09"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5143-slippage-protection-for-tokenized-vaults/9554
views: 3132
likes: 7
posts_count: 9
---

# EIP-5143: Slippage protection for Tokenized Vaults

As described in this [message](https://ethereum-magicians.org/t/eip-4626-yield-bearing-vault-standard/7900/94) I believe and extension ERC is required to standardize the EOA facing functions of ERC4626 vaults.

https://github.com/ethereum/EIPs/pull/5143

## Replies

**dimsome** (2022-06-16):

I think this extension makes a lot of sense. I like the idea of extending 4626 rather than creating a separate new standard to deal with certain use cases as is the case here: [EIP-5115: Super Composable Yield Token](https://ethereum-magicians.org/t/eip-5115-super-composable-yield-token/9423).

Something that I was wondering about:

What would be the default behaviour of calling a function without the min/max/Shares/Assets as per 4626 alone?

- The user/integrator should build in their own slippage protection?

or

- IF a contract extends 4626 with 5143, the overloaded functions are there to customise the slippage, while the base 4626 functions should have slippage protection built-in?

**The ladder would be better in my opinion.**

This would make a **true standard**, since the user could handle each contract that is 4626 the same way, without risking being sandwiched with one 4626 Vault while being totally safe with another. One that extends 4626 with 5143 while the other doesn’t.

We should make sure to protect users/integrators in either case. That is why the reference implementation should be different. The 4626 deposit function should work out a min/max/Shares/Assets and call the 5143 deposit function with that value. While the functions within 5143 can customise the slippage and potentially save gas if the calculation is done off-chain.

In my opinion, this would be a better way of extending a standard while keeping the base standard usable even with the extension.

**I would therefore add:**

- A contract that is 4626 with the 5143 extensions should require the 4626 deposit/mint/redeem/withdraw to handle slippage
- The 5143 deposit/mint/redeem/withdraw functions are to customise slippage and save gas if the calculation is done off-chain or to be called directly from another smart contract if the slippage logic is to be customised.

Making each 4626 standardised and functioning in an expected way is the goal.

---

**Amxx** (2022-06-17):

My ERC4646, the deposit/mint/redeem/withdraw function can be subject to slippage, and have no specific protection.

They are designed to be called by smart contracts, not by EOA. Using the preview allows them to estimate slippage and only execute the operation if they accept it. This design works if the preview call, the decision making, and the operation are in the same transaction which smart contracts can do, but not EOA.

This is why we need an alternative workflow for EOAs. Backward compatibility dictates that using 5143 on top of 4626 does NOT modify the 4626 behavior. in particular, it doesn’t change anything about slippage possibly happening.

---

**SamWilsn** (2022-06-17):

I’d recommend requiring support for [EIP-165](https://eips.ethereum.org/EIPS/eip-165) so that wallets can detect these additional functions easily.

---

**Amxx** (2022-06-20):

For some reason, EIP-4626 doesn’t include EIP-165 support… So I’m not sure what should/shouldn’t be in the interfaceID.

---

**ishan-verma** (2022-09-05):

Instead of overriding functions in ERC4626 protocols could implement a router contract similar to uniswapV2 router. For instance, ERC4626Router could have

```auto
depositToMinShares(uint256 assets, address receiver, uint256 minShares)
```

---

**fubuloubu** (2023-02-18):

That was intentional. For a base spec, it’s pretty obvious whether or not the implementation supports the full spec (because you should be reading the code anyways), ERC165 doesn’t really add anything. For extensions, ERC165 is usually a good idea because then it becomes about which modifications to behavior the implementation supports. Also for some use cases (off-chain wallet signalling, or some types of Registry-style integrations) requiring implementation of ERC165 is also a benefit. Anyways, for the base standard, we didn’t see a huge benefit to mandating it’s use, and wanted to avoid the scenario with ERC721 (as it’s somewhat annoying to use there)

---

**fubuloubu** (2023-02-18):

I like that this proposal is an extension, I think it’s really strong that way, since only sometimes will a Vault implementation be intended to be accessible to EOAs.

You can probably reference ERC4626 with some of the implementation notes, e.g. “This function extends of the behavior ERC4626.mint, with the following additional assumptions:”, just so it’s clear to reviewers what the additional behavior is.

I don’t have any more significant commentary, I think this proposal is really strong and should be moved forward to Final once cleaned up

---

As a side note, you don’t need to use the `preview*` methods for slipapge protection w/ Smart Contract callers, they can simple call the `convertTo*` functions and do an assertion based on that, something like:

```plaintext
require(vault.convertToAssets(sharesToWithdraw) - vault.redeem(sharesToWithdraw, msg.sender, msg.sender) < SLIPPAGE_TOLERANCE);
```

---

**fubuloubu** (2023-02-18):

I think using a default of either 0 or `type(uint).max` (depending on scenario) would most clearly align with what [@Amxx](/u/amxx) is saying, that by default the slippage “protection” is 100% loss (lol), since the intent is that smart contracts should implement their own (more complex) handling for slippage loss, if desired


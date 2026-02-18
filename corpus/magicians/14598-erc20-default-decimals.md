---
source: magicians
topic_id: 14598
title: ERC20 Default decimals
author: RenanSouza2
date: "2023-06-07"
category: EIPs
tags: [erc, token, erc20]
url: https://ethereum-magicians.org/t/erc20-default-decimals/14598
views: 4007
likes: 7
posts_count: 11
---

# ERC20 Default decimals

Hello everyone

In the ERC20 description is says that decimals are not mandatory,

What is the interpretation of a token with no decimals?

Would it be to consider decimals to be 0?

Should this be on the text?

Thank you, everyone

## Replies

**ulerdogan** (2023-06-07):

Hi,

The decimals are 18 with default setting as its included in the base ERC20 contract and it can be change by overriding the function.

If you want to use only **integers** for the token balances without decimals, you can set the decimal to 0 like token balances in the [ERC-1155](https://eips.ethereum.org/EIPS/eip-1155) assets.

Try;

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Token is ERC20 {
    constructor() ERC20("Token", "TKN") {
        _mint(msg.sender, 100 * 10 ** decimals());
    }

    function decimals() public pure override returns (uint8) {
        return 0;
    }
}

```

---

**RenanSouza2** (2023-06-07):

Thanks for responding,

I know openzeppelin defaults decimals to 18,

My question is, if the token does not implement decimals at all is the default behaviours to assume it is zero? It makes sense to be like this but there is no mention of that in [ERC-20: Token Standard](https://eips.ethereum.org/EIPS/eip-20).

---

**abcoathup** (2023-06-08):

From: [ERC-20: Token Standard](https://eips.ethereum.org/EIPS/eip-20#decimals)

> decimals
> Returns the number of decimals the token uses - e.g. 8, means to divide the token amount by 100000000 to get its user representation.
>
>
> OPTIONAL - This method can be used to improve usability, but interfaces and other contracts MUST NOT expect these values to be present.

My reading of the ERC is that it should be zero if no decimals are specified as it is optional.

You could create an ERC20 contract without decimals and try Etherscan and a few wallets to see how they handle it.

---

**RenanSouza2** (2023-06-08):

Etherscan uses 0 for default, just tested it

---

**Amxx** (2023-06-09):

Relevant discussion on the github issues for `@openzeppelin/contracts`:

https://github.com/OpenZeppelin/openzeppelin-contracts/issues/4323#issuecomment-1584511153

---

**netnose** (2023-07-05):

Even if 18 is the de facto standard, ERC-20 is not explicit about the default value to be used for decimals.

An explicit reference to 18 decimals can be found in [ERC-1046](https://eips.ethereum.org/EIPS/eip-1046), even if it is an extension ERC, it talks about ERC-20 behavior.

IMO, 0 is more intuitive but it looks like 18 has been chosen years ago.

---

**RenanSouza2** (2023-07-05):

Openzeppelin used 18 and Etherscan uses 0 when the token doesn’t specify it’s decimals, I wish this was defined at the ERC but it seems too late for that

---

**netnose** (2023-07-07):

We are talking about 2 very different things here.

OpenZeppelin used 18 decimals as default in their base ERC-20 smart contract code. They actually did a great job. In this case, the decimals function is always defined, as opposite to what we are talking about in this topic.

Etherscan, is a piece of software that interprets on-chain data. The value it uses when a decimals function is missing in a smart contract can be changed by modifying exclusively it’s source code.

---

**RenanSouza2** (2023-07-07):

We are actually talking about the same thing,

This dicussion started because of this contract: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC20Wrapper.sol

That have this function here

```auto
    /**
     * @dev See {ERC20-decimals}.
     */
    function decimals() public view virtual override returns (uint8) {
        try IERC20Metadata(address(_underlying)).decimals() returns (uint8 value) {
            return value;
        } catch {
            return super.decimals();
        }
    }

```

That sets the wrapper decimals to 18 if the underlying token does not present a value

Overall this is a part of the ERC20 token that is not defined and there is no right or wrong, so neither OZ or Etherscan have to change how they do things

---

**netnose** (2023-07-07):

Ok, sorry, this thread started from the GitHub one, not the opposite.

As I said I think 0 is more practical but EIP-1046 defines 18 as the default.

I know that it is not EIP-20 but it is part of the standard, so… I guess it should be treated as source of truth. Is it too much borderline?

Another consideration, if we are forced to choose, is about what’s best for the ecosystem. Smart contracts are already deployed and we cannot change them. On the other side we can change any dapp to adapt to the standard.

Another good question is: How many contracts did not implement the decimals function?


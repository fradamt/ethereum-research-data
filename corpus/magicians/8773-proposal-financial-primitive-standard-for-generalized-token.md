---
source: magicians
topic_id: 8773
title: "Proposal: Financial Primitive Standard (for generalized token accounting)"
author: aleezagroks
date: "2022-04-01"
category: EIPs
tags: [defi]
url: https://ethereum-magicians.org/t/proposal-financial-primitive-standard-for-generalized-token-accounting/8773
views: 1126
likes: 5
posts_count: 3
---

# Proposal: Financial Primitive Standard (for generalized token accounting)

There should be a standard interface for financial primitives that abstracts away the token accounting logic and leaves only the business logic instead. To be specific, “accounting logic” consists of moving tokens between accounts, whereas “business logic” is computing how many tokens need to be moved. All financial primitives (like AMMs, lending pools, or NFT markets) require both types of logic. However, while the business logic is unique to each primitive, the accounting logic is always the same: a user gives tokens to the primitive, and the primitive gives tokens to the user. That means it’s possible to generalize the accounting logic for all financial primitives.

The purpose of this standard would be to create a universal accounting interface that could apply to any kind of financial primitive. Let’s define a financial primitive as something that takes a token as input and then gives back another token as output. In other words, it converts one form of value into another form of value.

If all primitives used a standardized accounting interface, then general accounting frameworks could live elsewhere—as independent smart contracts that handle the token accounting on behalf of various DeFi protocols. This architecture would make financial primitives more modular and hence make it easier to compose primitives, because any accounting framework could bundle token accounting across independent primitives.

Here is an example of what the interface could look like:

```auto
interface IFinancialPrimitive {
    function computeOutputAmount(
        uint256 inputToken,
        uint256 outputToken,
        uint256 specifiedAmount,
        address userAddress,
        bytes32 metadata
    ) external returns (uint256 outputAmount);
}
```

Here’s some examples of how it would be used for different types of primitives:

***AMM:***

`inputToken` = DAI

`outputToken` = USDC

`specifiedAmount` = 100

`userAddress` = [not needed]

`metadata` = [slippage protection]

In this example, we are telling the AMM that Alice wants to swap 100 DAI for USDC. The AMM will then compute the amount of USDC to trade, and return ~99.9 as an `outputAmount`.

Next, an accounting system (living in an external contract) would move the 100 DAI and 99.9 USDC to the appropriate wallets.

***Lending pool:***

`inputToken` = DAI

`outputToken` = aDAI

`specifiedAmount` = 100

`userAddress` = Alice

`metadata` = [deposit, lend, or borrow]

In this example, we are telling the lending pool that Alice wants to lend 100 DAI and receive aDAI, a yield-bearing fungible token redeemable for DAI. The lending pool will compute the amount of aDAI to mint.

Next, an accounting system would move the 100 DAI and mint aDAI.

The idea for this standard came out of Shell Protocol, which partly relies on disentangling token accounting from the business logic of financial primitives. If you want to understand the context better, we go into depth about these ideas in the [Shell v2, part 2 white paper](https://shellprotocol.io/static/Ocean_-_Shell_v2_Part_2.pdf), especially Section 4.1. You can also check out our [reference implementation of a general accounting framework](https://github.com/cowri/ocean) (an example of something that would interface with standardized primitives) and in particular the primitive interface (contracts/IOceanPrimitive.sol).

I’m looking for feedback before we propose an ERC. Thoughts and comments are much appreciated!

## Replies

**jannikluhn** (2022-04-05):

I guess today the standard for DeFi interactions is the EVM or the contract ABI standard, but they’re very low level and not very good at handling even token transfers (see ERC20 approvals). So something more concrete/high-level/application specific seems very useful and the proposed approach sounds reasonable to me (but I’m not a DeFi expert).

One thing that’s not clear to me is why primitives should have only a single input and output token. E.g., the primitive “NFT market place” could have two outputs: The NFT itself and a governance token rewarding users. An “order book exchange primitive” could have two outputs, with two different receivers: Buyer and seller. Isn’t the proposed interface too restrictive to describe these use cases? Or are they expected to not be primitives at all, but composed of primitives?

It seems that the user address is not needed for all primitives. Therefore, wouldn’t it make sense to integrate it into the metadata field, and allow it to have arbitrary size?

If this becomes an ERC, it would probably make sense to add a simple end2end example that shows all involved contracts. At least to me it’s not immediately obvious which part would implement the primitive, which does the accounting, and which does things like access control etc.

---

**Thomas-Sciaroni** (2022-04-08):

The guiding philosophy was to make the common cases cheap and the rare cases possible, while keeping the implementation as simple as possible.

I’ll start by talking about metadata.  The metadata is passed by the user to the accounting system, and the accounting system simply hands it off to the primitive.  The accounting system does not know anything about the metadata’s syntax or semantics, it only cares about the input/output relationship.

When I benchmarked variable length metadata vs a single `bytes32`, variable length metadata increased the fixed gas costs of an interaction by about ~20%, even when the metadata was empty.  In contrast, adding the `bytes32` parameter to the existing function signature did not meaningfully increase gas costs.  Basic interactions like swapping do not require any metadata, and we want to keep these cheap.

The next level of complexity for a primitive, something like a lending pool, require a few bits of metadata, like the user’s address (for checking available collateral) and to let the user specify their desired collateralization ratio.  32 bytes should be plenty of space for most protocols that need more than an input/output relationship.  I’ll touch on how protocols can work around this 32 byte limit at the end of this post.

Now talking about the user address.  It is always provided in it’s own field for three reasons, all related in one way or another to the above metadata discussion.  The first is that, as with the `bytes32` field, adding it to the existing call did not meaningfully increase gas costs.  The second is that merging the two would require reducing the amount of other metadata that could be included alongside the user address, or require variable length metadata.  The third reason is in my view the most important.  If the accounting system were to conditionally provide the user address using the metadata field, the accounting system would either have to know the primitive’s metadata message format, or it would have to impose a metadata message format on all protocols.  Both of these options add a lot of implementation complexity and tighter coupling between the accounting system and the primitive.

For input/multiple outputs:

The accounting system simply does something like (psuedocode)

```auto
user[input] -= inputAmount
primitive[input] += inputAmount
primitive[output] -= outputAmount
user[output] += outputAmount
```

The accounting system will always apply these operations.  When there’s an inputAmount of 0, nothing is taken from the user.  When there’s an outputAmount of 0, nothing is taken from the primitive.  Exploiting this, we can make successive interactions for cases where the user is giving `n` tokens, and the primitive is giving `m` tokens, and `n != m`.

As an example with the NFT governance token:

```auto
interaction[0] = {
  inputToken = DAI
  outputToken = NFT
  specifiedAmount = 100
  userAddress = user
  metadata = 0x0...0
}
interaction[1] = {
  inputToken = 0x0...0
  outputToken = GovReward
  specifiedAmount = 0
  userAddress = user
  metadata = 0x0...0
}
```

The primitive can handle this in many different ways.

One way that comes to mind is having a storage mapping from user address to governance reward owed.  In the first interaction, the primitive initializes a location in the mapping to `owed[user] = rewardAmount`.  In the second interaction, the primitive fetches `owed[user]`, zeros the storage location, then returns the amount owed.   If these interactions are issued from the accounting system in the same EVM transaction, the transient storage uses around 3.5k gas. This is similar in concept to OpenZeppelin’s reentrancy guard, but with a user address scoped state variable.  The occasional 3.5k in additional gas cheaper than the constant gas costs associated with a more complex accounting system and a more flexible message format.

If a protocol requires more than 32 bytes of metadata, it can use a similar technique with the zero input/output accouting to build up the requisite amount of metadata, or it can use an out-of-band message – maybe the user writes some data to the primitive from outside the accounting system before calling the accounting system.


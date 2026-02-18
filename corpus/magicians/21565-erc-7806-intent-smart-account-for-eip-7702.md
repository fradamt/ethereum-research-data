---
source: magicians
topic_id: 21565
title: "ERC-7806: Intent Smart Account for EIP-7702"
author: hellohanchen
date: "2024-11-03"
category: ERCs
tags: [wallet, account-abstraction, erc-4337, intents, eip-7702]
url: https://ethereum-magicians.org/t/erc-7806-intent-smart-account-for-eip-7702/21565
views: 373
likes: 1
posts_count: 6
---

# ERC-7806: Intent Smart Account for EIP-7702

**[EIP-7702](https://eips.ethereum.org/EIPS/eip-7702)** empowers Externally Owned Accounts (EOAs) to temporarily mount a smart contract, enabling them to execute complex logic and operations without relying on external contracts. To fully leverage this capability, we’ve developed a new Smart Contract Account standard tailored for EIP-7702: **ERC-7806**—an intent-centric solution.

## Motivation

Traditionally, smart contract accounts offer features like gas sponsorship and batch execution. However, users still need to explicitly define the execution steps—for example:

“First, approve the Uniswap V3 contract to spend 1000 USDC; then, call the Uniswap contract to swap USDC for USDT at a 1:1 price with 1% slippage.”

This approach not only requires users to understand the underlying mechanics of on-chain instructions, but also limits the flexibility of relayers (or bundlers). Furthermore, the success of the user’s transaction is entirely dependent on external contract states (e.g., Uniswap). If the price changes, the user operation fails.

In practice, smart contract accounts have not significantly lowered the barrier to entry for users—they often increase gas costs and introduce additional dependencies like paymasters and bundlers.

## Solution

With **ERC-7806**, we introduce a new paradigm: abstracting user intent as a “transaction interface.”

Instead of providing low-level instructions, users define the desired outcome. Consider the following examples:

1. Token swap: Swap 1000 USDC for 1000 USDT
2. Flash loan: Use 1000 USDC to obtain 1010 USDC

In both cases, the user signs an intent and submits it to a relayer. The actual on-chain instructions are determined by the relayer—users don’t need to understand or specify any of the implementation details.

In the token swap example, the relayer can execute the trade via Uniswap, 1inch, Curve, or even directly with a liquidity provider holding a token balance. Regardless of the path chosen, the smart contract account ensures that the user’s intent is fulfilled—or the transaction reverts.

### Interoperability

This approach shifts user–blockchain interaction from imperative **instructions** to high-level **intents**. These intents are structured data types (EIP-712) that are highly readable, compatible, and interoperable.

For example, a token swap intent can be easily understood and integrated by any DApp or wallet, and it can support any ERC-20 token pair without needing to modify the logic for different DEXs.

## Technical Spec

While ERC-7806 may appear complex, the standard only defines two core interfaces:

1. IAccount

```auto
interface IAccount {
    /**
     * Execute user's intent
     *
     * @dev returning execution result, the type uses bytes for extensibility purpose
     * @return result values representing execution outcomes
     */
    function executeUserIntent(bytes calldata intent) external returns (bytes memory);
}
```

1. IStandard

```auto
interface IStandard {
    /**
     * Validate user's intent
     *
     * @dev returning validation result, the type uses bytes4 for extensibility purpose
     * @return result values representing validation outcomes
     */
    function validateUserIntent(bytes calldata intent) external view returns (bytes4 result);

    /**
     * Unpack user's intent, it is RECOMMENDED to validate intent while unpacking to save gas
     *
     * @dev returning unpacked result, the type uses bytes for extensibility purpose
     * @return result unpacked result status
     * @return operations unpacked operations that can be executed by the IAccount, NOT REQUIRED to match UserIntent.instructions
     */
    function unpackOperations(bytes calldata intent) external view returns (bytes4 result, bytes[] memory operations);
}
```

The `IAccount` interface is responsible for executing on-chain logic (leveraging Solidity’s `msg.sender`), and our recommended implementation is **stateless**—with fewer than 100 lines of code. This simplicity minimizes risk and avoids storage collision issues introduced by EIP-7702.

The `IStandard` interface handles intent validation and translation. A validated intent is “unpacked” into concrete instructions—similar to what users would have manually included in a user operation.

Each `IStandard` is focused on a specific type of intent, ensuring safety and simplicity. For example, the token swap standard is under 200 lines of code and supports all ERC-20 pairs.

Furthermore, `IStandard` contracts are fully modular—they can be composed and reused, enabling high flexibility for developers. This modularity also promotes interoperability, allowing different DApps to share and integrate the same standards without redundant development.

#### For more details, refer to our official ERC proposal:

## Backwards Compatibility

ERC-7806 is a brand new delegator-relayer solution.

## Security Considerations

### Malicious Signature

Users might be cheated to sign malicious intents.

### Malicious EIP-7702 Delegation

It is possible that an EOA uses a malicious delegation and cause relayer’s transaction to fail on chain, to avoid such behavior, the relayer must leverage another on-chain smart contract to validate the `codehash` of EOA address. This applies to all EIP-7702 based solutions.

## Replies

**abcoathup** (2024-11-04):

Suggest just posting a link to the ERC PR and perhaps the abstract rather than copy/pasting.

---

**hellohanchen** (2024-11-04):

Thanks for the advice, I’ve edited the post to include abstract, motivation and some discussion topics only. ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

---

**hellohanchen** (2025-02-13):

The PR is reworked and updated with an example.

---

**hellohanchen** (2025-04-29):

The ERC is officially in `DRAFT` state!



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7806)





###



Extensible intent-centric EOA smart account interface design to support batch execution, gas sponsorship and more other functionalities.










Please review the spec if you are interested. We are open to any feature requests, feedbacks, ideas.

---

**hellohanchen** (2025-06-24):

The description is updated for this ERC proposal. Hope this can help people better understand our solution.


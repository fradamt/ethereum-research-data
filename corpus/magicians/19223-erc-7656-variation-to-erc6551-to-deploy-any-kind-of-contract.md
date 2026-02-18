---
source: magicians
topic_id: 19223
title: "ERC-7656: Variation to ERC6551 to deploy any kind of contract linked to any contract, included NFTs"
author: sullof
date: "2024-03-16"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7656-variation-to-erc6551-to-deploy-any-kind-of-contract-linked-to-any-contract-included-nfts/19223
views: 1724
likes: 6
posts_count: 19
---

# ERC-7656: Variation to ERC6551 to deploy any kind of contract linked to any contract, included NFTs

## Abstract

This proposal introduces a variation of ERC6551 that extends to all types of contracts linked to non-fungible tokens (NFTs). This generalization allows NFTs not only to own assets and interact with applications as accounts but also to be linked with any contract, enhancing their utility without necessitating modifications to existing smart contracts or infrastructure.

For reference:

- https://eips.ethereum.org/EIPS/eip-6551
- https://ethereum-magicians.org/t/erc-6551-non-fungible-token-bound-accounts/13030

## Motivation

Our initial approach involved proposing an expansion of ERC6551 to encompass a broader scope of token-bound contracts beyond accounts. The goal was to enable any deployed token-bound contract to potentially represent more than just an account, with the actual functionality determined by checking the contract’s interface. Unfortunately, this suggestion was not adopted due to concerns about complicating the trust model built into ERC6551, where projects rely on emitted events to understand the nature of the contract without additional verification steps. Our proposed change, while introducing versatility, would have necessitated interface checks by developers, introducing a layer of friction and potentially leading to non-account contracts being banned as spam by Token Bound Account (TBA) indexes.

Reflecting on this feedback and considering the vast potential applications, we have crafted this new proposal. It aims to transcend the limitations of having NFTs solely function as accounts, thus unlocking a myriad array of interactions and functionalities. By proposing a separate but complementary standard, we seek to preserve the integrity and trust model of ERC6551 while offering a framework for NFTs to engage with diverse contracts. This approach not only enriches the ecosystem but also aligns with the evolving complexity of digital and real-world assets that NFTs aim to represent.

Of course, if ERC6551 evolves in a more general way, we’d be happy to dismiss this proposal.

## Specification (updated on March 23 to latest version)

The interface `IERC7656Registry` is defined as follows (the number is temporary, waiting for an EIP editor to assign it):

```solidity
interface IERC7656Registry {
  /**
   * @notice The registry MUST emit the Created event upon successful contract creation.
   * @param contractAddress The address of the created contract
   * @param implementation The address of the implementation contract
   * @param salt The salt to use for the create2 operation
   * @param chainId The chain id of the chain where the contract is being created
   * @param tokenContract The address of the token contract
   * @param tokenId The id of the token
   */
  event Created(
    address contractAddress,
    address indexed implementation,
    bytes32 salt,
    uint256 chainId,
    address indexed tokenContract,
    uint256 indexed tokenId
  );

  /**
   * The registry MUST revert with CreationFailed error if the create2 operation fails.
   */
  error CreationFailed();

  /**
   * @notice Creates a token linked account for a non-fungible token.
   * If account has already been created, returns the account address without calling create2.
   * @param implementation The address of the implementation contract
   * @param salt The salt to use for the create2 operation
   * @param chainId The chain id of the chain where the account is being created
   * @param tokenContract The address of the token contract
   * @param tokenId The id of the token
   * Emits Created event.
   * @return account The address of the token linked account
   */
  function create(
    address implementation,
    bytes32 salt,
    uint256 chainId,
    address tokenContract,
    uint256 tokenId
  ) external returns (address account);

  /**
   * @notice Returns the computed token linked account address for a non-fungible token.
   * @param implementation The address of the implementation contract
   * @param salt The salt to use for the create2 operation
   * @param chainId The chain id of the chain where the account is being created
   * @param tokenContract The address of the token contract
   * @param tokenId The id of the token
   * @return account The address of the token linked account
   */
  function compute(
    address implementation,
    bytes32 salt,
    uint256 chainId,
    address tokenContract,
    uint256 tokenId
  ) external view returns (address account);
}
```

Any contract developed using the `ERC76xxRegistry` SHOULD implement the `IERC76xxContract` interface:

```solidity
interface IERC7656Contract {
  /**
  * @notice Returns the token linked to the contract
  * @return chainId The chainId of the token
  * @return tokenContract The address of the token contract
  * @return tokenId The tokenId of the token
  */
  function token() external view returns (uint256 chainId, address tokenContract, uint256 tokenId);

}
```

or the `IERC6551Account` interface or both.

Here an implementation for a contract implementing `IERC7656Contract`.

```solidity
contract ERC7656Contract is IERC7656Contract {

  function token() public view virtual returns (uint256, address, uint256) {
    bytes memory footer = new bytes(0x60);
     assembly {
      extcodecopy(address(), add(footer, 0x20), 0x4d, 0x60)
    }
    return abi.decode(footer, (uint256, address, uint256));
  }
}
```

### Note: The interfaces above have been updated to reflect latest version in the ERC repo

## Replies

**sullof** (2024-03-16):

I made a PR for the proposal at

https://github.com/ethereum/ERCs/pull/327

---

**jay** (2024-03-16):

Co-author of ERC-6551 here. This is cool! I like that it adds an additional level of flexibility for contracts that wish to be bound to a token but don’t want to support signature validation or execution capabilities.

It would be awesome if every ERC-6551 account were able to be compatible with this proposal out of the box, given that this is a higher level abstraction which borrows from its structure.

One way to achieve this would be to modify the interface slightly to allow for multiple sub-registries to exist and be compatible with this proposal’s registry. Something like:

```auto
interface IERC76xxRegistry {
  /**
   * The registry MUST emit the TokenLinkedContractCreated event upon successful account creation.
   */
  event TokenLinkedContractCreated(
    address registry,
    address contractAddress,
    address indexed implementation,
    bytes32 salt,
    uint256 chainId,
    address indexed tokenContract,
    uint256 indexed tokenId
  );

  /**
   * Deploys a contract linked to a token
   * It a new contract is deployed, it MUST emit a TokenLinkedContractCreated event.
   * If the contract has already been created, it just returns the account address.
   */
  function createTokenLinkedContract(
    address registry,
    bytes4 createSelector,
    address implementation,
    bytes32 salt,
    uint256 chainId,
    address tokenContract,
    uint256 tokenId
  ) external returns (address account);

  /**
   * Returns the computed address for the contract linked to a token
   */
  function tokenLinkedContract(
    address registry,
    bytes4 computeSelector,
    address implementation,
    bytes32 salt,
    uint256 chainId,
    address tokenContract,
    uint256 tokenId
  ) external view returns (address account);
}
```

`createTokenLinkedContract` and `tokenLinkedContract` would then execute a call to the `registry` contract specified with `abi.encodePacked(selector, abi.encode(implementation, salt, chainId, tokenContract, tokenId))` as calldata.

This would allow any ERC-6551 account that wished to enable compatibility with this proposal to do so without requiring any changes to ERC-6551 itself.

---

**sullof** (2024-03-16):

Hi [@jay](/u/jay), thanks for your feedback.

I thought of this proposal as a complement to ERC6551. In fact, in the Cruna protocol, we deploy managers and plugins that are not accounts using this variation of your registry, while we deploy plugins that are accounts using ERC6551Registry.

However, I like you suggestion. The only tradeoff I see is that the caller must know the address of the registry that will actually deploy the token bound contract, and the selector of the function to trigger the deployment or to get the computed address.

It looks like there isn’t a real advantage in calling this pre-registry instead of calling the actual registry, since the caller will spend more gas. Considering that the internal call has to pass many parameters to the registry, I suspect the cost will increase of at least 15,000 gas.

One optimization may be removing the selector and expect that any registry calls the two functions `createAccount` and `account` (like in ERC6551), despite if the deployed contracts are actually accounts. This way we can skip the selector as a parameter. Having it, though, gives more flexibility, which is in the end the goal of your suggestion.

What about the registries? Should any registry try to set up a standard? If so, this ERC could evolve and become the specification for the registry we use in Cruna, emitting the `TokenLinkedContractCreated`, and we may create a new ERC that works as a superset, opening the road for future evolutions that we don’t see now.

What do you think?

---

**sullof** (2024-03-16):

I was pondering over the idea that if we consider each sub-registry to have its own distinct scope, it would actually be perfectly acceptable for the Cruna registry to function as an ERC6551Registry without being strictly for accounts. This means there shouldn’t be an automatic expectation that contracts deployed by it must conform to IERC6551Account. In other words, just because the registry triggers the same event as the canonical ERC6551Registry doesn’t necessarily mean the deployed contract is an account.

Perhaps it could be suggested in the ERC-6551 proposal that any registry diverging from the canonical ERC6551Registry — while still implementing the IERC6551Registry interface — isn’t bound by the stipulation to ensure deployed contracts support IERC6551Account and IERC6551Execute.

---

**sullof** (2024-03-18):

Following our Telegram conversation, I made a change to the proposal to make any ERC6551 account compatible with it out of the box. Basically, the proposal says that any deployed contract should implement `IERC76xxContract`, or `IERC6551Account`, or both.

---

**spengrah** (2024-03-23):

This is very intriguing. What kinds of use cases inspired this or do you have in mind?

In the protocol I work on — [Hats Protocol](https://hatsprotocol.xyz) — developers in the ecosystem are creating a number of contracts meant to be deployed in association with a given ERC1155 token (a “hat”). Some of these are ERC6551 accounts, but many others are other types of contracts that do various non-account things.

Recently we have created a factory to enable cheap and standardized deployment of instances of these contracts. It enables instances to be deployed as minimal proxy clones with immutable args for more gas efficiency at both deployment and runtime. To facilitate this, our factory allows arbitrary bytes to be passed in during creation.



      [github.com](https://github.com/Hats-Protocol/hats-module/blob/main/src/HatsModuleFactory.sol)





####



```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// import { console2 } from "forge-std/Test.sol"; // remove before deploy
import { HatsModule } from "./HatsModule.sol";
import { LibClone } from "solady/utils/LibClone.sol";
import { IHats } from "hats-protocol/Interfaces/IHats.sol";

contract HatsModuleFactory {
  /*//////////////////////////////////////////////////////////////
                            CUSTOM ERRORS
  //////////////////////////////////////////////////////////////*/

  /**
   * @notice Emitted if attempting to deploy a clone of `implementation` for a given `hatId`, `otherImmutableArgs`, and
   * `saltNonce` that already has a HatsModule deployment
   */
  error HatsModuleFactory_ModuleAlreadyDeployed(
    address implementation, uint256 hatId, bytes otherImmutableArgs, uint256 saltNonce
  );
```

  This file has been truncated. [show original](https://github.com/Hats-Protocol/hats-module/blob/main/src/HatsModuleFactory.sol)










I know this is relatively opinionated, but if you were to extend the registry to enable that kind of contract creation logic, I would strongly consider moving away from our factory and to this registry. Curious to hear what you think!

---

**sullof** (2024-03-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/spengrah/48/10353_2.png) spengrah:

> In the protocol I work on — Hats Protocol — developers in the ecosystem are creating a number of contracts meant to be deployed in association with a given ERC1155 token (a “hat”). Some of these are ERC6551 accounts, but many others are other types of contracts that do various non-account things.

That is precisely why we propose a generic registry that would apply whenever a certain contract’s owner is a specific token.

The Cruna protocol primarily adds security and inheritance features to NFTs. To do so, any NFT must be associated with its own manager. The manager can manage the transferability of the NFT by adding protectors and safe recipients and plugging more contracts to expand the NFT’s functionality.

The use cases for plugins are innumerable: lending platforms, asset distributors, identity managers, etc. Anything that has a sense if associated with a token can be a plugin.

Currently, the Cruna protocol does not support ERC1155. Still, we are working on adding a voting system that allows the owners of ERC1155 editions to define a virtual owner that owns the manager and the plugins. The virtual owner should be a particular contract that acts like a multi-sig.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/spengrah/48/10353_2.png) spengrah:

> but if you were to extend the registry to enable that kind of contract creation logic, I would strongly consider moving away from our factory and to this registry.

I see two separate components in your protocol, the technology to deploy the contracts and the logic connected with this deployment. This is similar to how the Cruna protocol works. In fact, you can plug something only under very strict conditions to avoid vulnerabilities, but the basic tool used to deploy the contract is the ERC6551Registry if the plugin is an account and the ERC7656Registry if it is not.

You may do the same without losing flexibility.

Just to add more details, we are waiting to complete a technical audit of the protocol; then, we will deploy the protocol, including a canonical version of the registry, to all EVM chains, starting from some tenets. In any case, we will provide the code to deploy the registry everywhere it is needed.

In case you want to read more, you can find info at

https://github.com/crunaprotocol/cruna-protocol

and


      ![image](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/crunaprotocol/cruna-protocol/tree/main/docs)





###



Contribute to crunaprotocol/cruna-protocol development by creating an account on GitHub.

---

**spengrah** (2024-03-23):

I guess my main question is whether the ERC7656Registry can append arbitrary bytes to the footer of a newly deployed contract instance.

From what I can gather from the reference implementation, `create()` appends the salt, chainId, tokenContract, and tokenId to the instance’s deployed bytecode. In addition to that, I would also like to see something like a `bytes extraImmutableData` argument handled by `create()`.

Is my question clear? Happy to elaborate if not.

---

**sullof** (2024-03-23):

Understood. As it stands, the current proposal does not include support for an additional data field for appended code. However, I am not sure there is a necessity of such a feature.

If I’ve understood correctly, the primary objective behind incorporating immutable data is to safeguard certain contract logic from modifications. It seems plausible to achieve this without embedding the code directly within the primary proxy contract.

Consider a scenario where the contract structure is bifurcated: one part being the actual implementation and the other, a proxy. In this setup, the registry deploys what essentially acts as the proxy contract. Thus, we are dealing with a triad of contracts:

1. The proxy created via the registry,
2. Your designated proxy contract, and
3. The actual implementation contract.

In such an arrangement, function calls are forwarded to the implementation only if they are not recognized within the proxy contract, allowing the immutable code to reside within the proxy. This distinction enables the separation of contracts into those that are ERC6551Account-compliant and those that are not, managed respectively by the ERC6551Registry and the ERC7656Registry. It’s also worth noting the inherent benefits of aligning with the ERC6551Registry, given its widespread acceptance across numerous marketplaces and platforms. Additionally, we’re in the process of integrating an ERC7656 scanner to further enhance compatibility and functionality.

---

**spengrah** (2024-03-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> If I’ve understood correctly, the primary objective behind incorporating immutable data is to safeguard certain contract logic from modifications. It seems plausible to achieve this without embedding the code directly within the primary proxy contract.

The primary objective in my case is to enable runtime usage of that data in a more gas efficient manner. In other words, enable the clone proxy instance to access those values roughly as an immutable value rather than with an SLOAD. This gas savings is important for us because Hats modules are invoked quite often.

Many of the Hats module contracts interact with other contracts or have configuration values. For example, our ERC20 eligibility module, when invoked, checks whether a given account has a balance of the established token gte the established threshold value.

---

**sullof** (2024-03-23):

Got it.

What if we move the salt to the last part of the bytecode and change its type from bytes32 to bytes?

In this case, the salt may even be null, making the proxy smaller, or be just a typical salt, or be whatever you put in there to be used to set immutable data.

I am not sure it will work efficiently, but what do you think?

---

**spengrah** (2024-03-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> What if we move the salt to the last part of the bytecode and change its type from bytes32 to bytes?
> In this case, the salt may even be null, making the proxy smaller, or be just a typical salt, or be whatever you put in there to be used to set immutable data.

At first blush I like it!

It does deviate from ERC6551 a bit, but that’s likely ok since the relationship between 7656 and 6551 seems more important to hold for contracts themselves than at the registry level.

---

**sullof** (2024-03-23):

I am playing with it.

A big issue is that the gas cost becomes higher, even with 0x extra data, because of the dynamic size of the salt and the added keccak256 of the salt to get the bytes32 salt to be used with the create2.

Adding extra costs for everyone seems a bad trade-off.

Anyway, I will try to dig in my assembly knowledge to see if I can reduce the gas cost. A solution may be to set two functions, one with a standard salt and one with a dynamic salt, using an extra byte in the code to specify the case and the possibility of calling the favorite function.

That would diverge from ERC6551 quite a bit.

---

**sullof** (2024-03-24):

[@spengrah](/u/spengrah) I got stuck with the code trying to figure out if that makes sense.

After the initial experiments, I am afraid that the extraData, if not properly validated, could include malicious bytecode or operations that compromise the contract’s integrity. Since the safety of the registry is paramount, I think we have to stick to the current approach.

However, you may encode the extra data in the salt. 32 bytes can contain a lot of information.

---

**sullof** (2024-04-28):

I set up a new repo for the reference implementation of ERC-7656 at

https://github.com/crunaprotocol/erc7656

It has been taken from the [Cruna Protocol](https://github.com/crunaprotocol/cruna-protocol) implementation, which also has full coverage of the smart contracts.

A canonical version has been deployed at the address

0x7656f0fB4Ca6973cf99D910B36705a2dEDA97eA1

using Nick’s Factory with the following salt:

0x765600000000000000000000000000000000000000000000000000000000cf7e

on mainnets (Etherum, Polygon, BNB Chain) and on testnets (Avalanche Fuji and Celo Alfajores).

The code on mainnets has been verified. Feel free to use it.

In the repo above there is the bytecode deployed in the file at

https://github.com/crunaprotocol/erc7656/blob/main/scripts/canonicalBytecodes.json

and you can use that to deploy it to any other chain using Nick’s Factory.

---

**sullof** (2025-03-22):

**Breaking news:**

Two weeks ago, I introduced a new proposal (ERC7897) to replicate the behavior of ERC7656 for smart accounts like ERC4337. Later, I realized that a small modification to ERC7656 could support this use case while maintaining backward compatibility with ERC6551. As a result, I moved ERC7656 back from “Last Call” to “Review” and made a significant change by adding a new parameter.

The updated interface is as follows:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ERC7656
 * @dev ERC165 interface ID: 0x9e23230a
 * @notice Manages the creation of contract-linked services
 */
interface IERC7656Factory {
  event Created(
    address contractAddress,
    address indexed implementation,
    bytes32 salt,
    uint256 chainId,
    bytes12 mode,
    address indexed linkedContract,
    uint256 indexed linkedId
  );

  error CreationFailed();

  function create(
    address implementation,
    bytes32 salt,
    uint256 chainId,
    bytes12 mode,
    address linkedContract,
    uint256 linkedId
  ) external returns (address);

  function compute(
    address implementation,
    bytes32 salt,
    uint256 chainId,
    bytes12 mode,
    address linkedContract,
    uint256 linkedId
  ) external view returns (address service);
}
```

The corresponding ERC-1167 proxy data structure is:

```plaintext
ERC-1167 Header               (10 bytes)
    (20 bytes)
ERC-1167 Footer               (15 bytes)
              (32 bytes)
           (32 bytes)
              (12 bytes)
    (20 bytes)
          (32 bytes)
```

The `mode` parameter is a `bytes12`, utilizing the leading zeroes that would otherwise pad the `linkedContract` address.

Currently, two cases are supported:

```solidity
bytes12(uint96(0));
bytes12(uint96(1));
```

- If mode == bytes12(uint96(0)), the deployed bytecode is identical to that of ERC6551Registry, ensuring full compatibility with token-bound accounts.
- If mode == bytes12(uint96(1)), the linkedId is set to 0x00, meaning the service is owned by the entire contract (as in ERC4337 accounts).

The 12-byte `mode` field allows for future extensibility. For instance, if a service is linked to an ERC-1155 token but requires the user to hold at least 1,000 tokens, the mode could be encoded as follows:

```solidity
uint96 primaryMode = 2;
uint96 minToken = 1000;
bytes12 mode = bytes12(primaryMode | (minToken << 16));
```

This structure enables more complex conditions to be embedded in the `mode` parameter while keeping the standard flexible.

I also updated the reference implementation at



      [github.com](https://github.com/erc7656/erc7656)




  ![image](https://opengraph.githubassets.com/ae9191a981510a559573112cbe3e4a70/erc7656/erc7656)



###



A reference implementation










as well as the Npm package at

https://www.npmjs.com/package/erc7656

---

**sullof** (2026-02-04):

The proposal has been finalized. If interested in ERC7656, take a look at



      [erc7656.github.io](https://erc7656.github.io/)





###

---

**sullof** (2026-02-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/spengrah/48/10353_2.png) spengrah:

> I guess my main question is whether the ERC7656Registry can append arbitrary bytes to the footer of a newly deployed contract instance.

Hi, since the proposal has been finalized, I was looking back at the comments and saw yours.

In latest version of the proposal, the deployed bytecode structure is:

ERC-1167 Header               (10 bytes)

<implementation (address)>    (20 bytes)

ERC-1167 Footer               (15 bytes)

<salt (bytes32)>              (32 bytes)

<chainId (uint256)>           (32 bytes)

<mode (bytes12)>              (12 bytes)

<linkedContract (address)>    (20 bytes)

<linkedId (uint256)>          (32 bytes)

Maybe, you could use the 12 bytes of the mode field to add extra data.


---
source: magicians
topic_id: 12197
title: "ERC-6170: Cross-Chain Messaging Interface"
author: sujith_somraaj
date: "2022-12-18"
category: EIPs
tags: [cross-chain]
url: https://ethereum-magicians.org/t/erc-6170-cross-chain-messaging-interface/12197
views: 3405
likes: 7
posts_count: 6
---

# ERC-6170: Cross-Chain Messaging Interface

As the ecosystem is moving towards a cross-chain solution to piece all those fragmented liquidities, this proposal will speed up the development lifecycle of cross-chain applications.

**Why Cross-Chain?**

Imagine a bank sitting with $$ Trillion of untransferable deposits to any other bank and having to be used within its ecosystem.

What does it serve them? Similarly, liquidity/state in one chain unaccessible with ease to the other chain is problematic for scaling.

I’m aware there are multiple topics in discussions surrounding this.

Nearly 18 months ago, [@auryn](/u/auryn) suggested the same [A standard interface for arbitrary message bridges between chains/layers](https://ethereum-magicians.org/t/a-standard-interface-for-arbitrary-message-bridges-between-chains-layers/6163) but focussed on the interface for chain native bridges on Sidechains and L2s and never outlined non-EVM chains.

There is also an interesting EIP-5164 for cross-chain execution to standardize it at the relayer level.

But this proposal is to streamline cross-chain bridging protocols like Layerzero, Hyperlane, and Wormhole. These aren’t sidechains (or) native bridges and are interoperable with non-EVM chains.

Not just limited to these bridges, even native bridges using this standard will streamline the cross-chain messaging eco-system

Hence, this proposal aims to support message/state transfer between any chain, whether its EVM (or) non-EVM

## Abstract

This EIP introduces a common interface for cross-chain arbitrary message bridges (AMBs) to send and receive a cross-chain message (state).

## Motivation

Currently, cross-chain arbitrary message bridges lack standardization, resulting in complex competing implementations: Layerzero, Hyperlane, Axelar, Wormhole, Matic State Tunnel and others. Either chain native (or) seperate message bridge, the problem prevails. Adding a common standardized interface to the arbitrary message bridges provides these benefits:

- Ease Of Development: A common standard interface would help developers build scalable cross-chain applications with ease.
- Improved Scalability: Cross-chain applications can efficiently use multiple message bridges.
- Improved Security: Confronting security to specific parameters. At present, every message bridge has its diverse security variable. E.g., In Layerzero, the nonce is used to prevent a replay attack, whereas Hyperlane uses the Merkle root hash.
- Improved Robustness: Message bridges involving off-chain components are not censorship-resistant and are prone to downtimes. Hence, apps built on top of them have no choice but to migrate their entire state (which is highly impossible for large complex applications).

## Specification

The keywords “MUST,” “MUST NOT,” “REQUIRED,” “SHALL,” “SHALL NOT,” “SHOULD,” “SHOULD NOT,” “RECOMMENDED,” “MAY,” and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Every compliant cross-chain arbitrary message bridge must implement the following interface.

```solidity
// SPDX-License-Identifier: Apache-3.0

pragma solidity >=0.8.0;

/// @title Cross-Chain Messaging interface
/// @dev Allows seamless interchain messaging.
/// @author Sujith Somraaj
/// Note: Bytes are used throughout the implementation to support non-evm chains.

interface IEIP6170 {
    /// @dev This emits when a cross-chain message is sent.
    /// Note: MessageSent MUST trigger when a message is sent, including zero bytes transfers.
    event MessageSent(
        bytes to,
        bytes toChainId,
        bytes message,
        bytes extraData
    );

    /// @dev This emits when a cross-chain message is received.
    /// MessageReceived MUST trigger on any successful call to receiveMessage(bytes chainId, bytes sender, bytes message) function.
    event MessageReceived(bytes from, bytes fromChainId, bytes message);

    /// @dev Sends a message to a receiving address on a different blockchain.
    /// @param chainId_ is the unique identifier of receiving blockchain.
    /// @param receiver_ is the address of the receiver.
    /// @param message_ is the arbitrary message to be delivered.
    /// @param data_ is a bridge-specific encoded data for off-chain relayer infrastructure.
    /// @return the status of the process on the sending chain.
    /// Note: this function is designed to support both evm and non-evm chains
    /// Note: proposing chain-ids be the bytes encoding their native token name string. For eg., abi.encode("ETH"), abi.encode("SOL") imagining they cannot override.
    function sendMessage(
        bytes memory chainId_,
        bytes memory receiver_,
        bytes memory message_,
        bytes memory data_
    ) external payable returns (bool);

    /// @dev Receives a message from a sender on a different blockchain.
    /// @param chainId_ is the unique identifier of the sending blockchain.
    /// @param sender_ is the address of the sender.
    /// @param message_ is the arbitrary message sent by the sender.
    /// @param data_ is an additional parameter to be used for security purposes. E.g, can send nonce in layerzero.
    /// @return the status of message processing/storage.
    /// Note: sender validation (or) message validation should happen before processing the message.
    function receiveMessage(
        bytes memory chainId_,
        bytes memory sender_,
        bytes memory message_
        bytes memory data_
    ) external payable returns (bool);
}
```

## Rationale

The cross-chain arbitrary messaging interface will optimize the interoperability layer between blockchains with a feature-complete yet minimal interface. The light-weighted approach also provides arbitrary message bridges, and the freedom of innovating at the relayer level, to show their technical might.

The EIP will make blockchains more usable and scalable. It opens up the possibilities for building cross-chain applications by leveraging any two blockchains, not just those limited to Ethereum and compatible L2s. To put this into perspective, an easy-to-communicate mechanism will allow developers to build cross-chain applications across Ethereum and Solana, leveraging their unique advantages.

The interface also aims to reduce the risks of a single point of failure (SPOF) for applications/protocols, as they can continue operating by updating their AMB address.

## Security Considerations

Fully permissionless messaging could be a security threat to the protocol. It is recommended that all the integrators review the implementation of messaging tunnels before integrating.

Without sender authentication, anyone could write arbitrary messages into the receiving smart contract.

This EIP focuses only on how the messages should be sent and received with a specific standard. But integrators can implement any authentication (or) message tunnel-specific operations inside the receive function leveraging `data_` parameter.

## Copyright

Copyright and related rights waived via CC0

## Replies

**auryn** (2023-02-07):

I like that this generalizes to non-EVM chains.

I noticed that the natspec comments for the two events mention a `_fromChainId` parameter, but this is not included in the event itself.

---

**sujith_somraaj** (2023-02-07):

Thanks for pointing this out, fixed the issue !

---

**lolieatapple** (2023-02-23):

Better to add nonce and fee support.

Otherwise, a lot of features won’t work.

And better to have an interface to check current chainId for security.

Like LayerZero:

```auto
    // @notice send a LayerZero message to the specified address at a LayerZero endpoint.
    // @param _dstChainId - the destination chain identifier
    // @param _destination - the address on destination chain (in bytes). address length/format may vary by chains
    // @param _payload - a custom bytes payload to send to the destination contract
    // @param _refundAddress - if the source transaction is cheaper than the amount of value passed, refund the additional amount to this address
    // @param _zroPaymentAddress - the address of the ZRO token holder who would pay for the transaction
    // @param _adapterParams - parameters for custom functionality. e.g. receive airdropped native gas from the relayer on destination
    function send(uint16 _dstChainId, bytes calldata _destination, bytes calldata _payload, address payable _refundAddress, address _zroPaymentAddress, bytes calldata _adapterParams) external payable;

    // @notice used by the messaging library to publish verified payload
    // @param _srcChainId - the source chain identifier
    // @param _srcAddress - the source contract (as bytes) at the source chain
    // @param _dstAddress - the address on destination chain
    // @param _nonce - the unbound message ordering nonce
    // @param _gasLimit - the gas limit for external contract execution
    // @param _payload - verified payload to send to the destination contract
    function receivePayload(uint16 _srcChainId, bytes calldata _srcAddress, address _dstAddress, uint64 _nonce, uint _gasLimit, bytes calldata _payload) external;

    // @notice get the inboundNonce of a receiver from a source chain which could be EVM or non-EVM chain
    // @param _srcChainId - the source chain identifier
    // @param _srcAddress - the source chain contract address
    function getInboundNonce(uint16 _srcChainId, bytes calldata _srcAddress) external view returns (uint64);

    // @notice get the outboundNonce from this source chain which, consequently, is always an EVM
    // @param _srcAddress - the source chain contract address
    function getOutboundNonce(uint16 _dstChainId, address _srcAddress) external view returns (uint64);

    // @notice gets a quote in source native gas, for the amount that send() requires to pay for message delivery
    // @param _dstChainId - the destination chain identifier
    // @param _userApplication - the user app address on this EVM chain
    // @param _payload - the custom message to send over LayerZero
    // @param _payInZRO - if false, user app pays the protocol fee in native token
    // @param _adapterParam - parameters for the adapter service, e.g. send some dust native token to dstChain
    function estimateFees(uint16 _dstChainId, address _userApplication, bytes calldata _payload, bool _payInZRO, bytes calldata _adapterParam) external view returns (uint nativeFee, uint zroFee);

    // @notice get this Endpoint's immutable source identifier
    function getChainId() external view returns (uint16);
```

---

**sujith_somraaj** (2023-03-01):

Hi, Thanks for pointing things out. These were exact issues I faced while writing wrapers for AMBs using EIP-6170.

The current `sendMessage()` function is payable; hence, you can pay alongside the transaction. For implementations like Hyperlane, you could pay alongside the same function and make two atomic calls inside.

For nonce and stuff, you could use the `data_` part, or you can use them encoded in the message. Still TBD, working on wrapping a bunch of AMBs and will update this if needed.

---

**tavakyan** (2024-07-18):

I would recommend one small change:

- The MessageReceived event should have the extraData field

This is useful for non-evm chains like the SVM on Solana.  As an example, if you are building a relayer for a canonical bridge, when writing to the SVM you need to specify the accounts up front.  So one way would be to call ‘receiveMessage’ twice on the SVM chain.  The first would update the extra data param to contain the accounts that would be accessed and the second call could utilize that to prepare a proper transaction.

Also, perhaps the way that chain-ids get encoded should be outside the scope of this EIP since this is designed for flexibility.


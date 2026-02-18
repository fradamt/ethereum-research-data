---
source: ethresearch
topic_id: 13770
title: Standardisation of cross-chain messaging interface
author: sujithsomraaj
date: "2022-09-26"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/standardisation-of-cross-chain-messaging-interface/13770
views: 1672
likes: 2
posts_count: 3
---

# Standardisation of cross-chain messaging interface

**Problem**

There are multiple cross-chain messaging protocols in production at this point. Some notable ones are layerzero, wormhole, and Hyperlane (previously abacus).

These cross-chain messaging protocols’ operations vary in many aspects, but their primary objective is to transfer states from one chain to another.

Irrespective of their operation, these protocols have implemented their interface for sending and receiving messages.

Standardization of such interfaces would help achieve greater scalability and interoperability between multiple chains.

For eg., in Hyperlane for sending a message to a different chain, the dispatch() function is used.

```auto
function dispatch(
  uint32 _destinationDomain,
  bytes32 _recipientAddress,
  bytes calldata _messageBody
) external;

```

But in the case of Layerzero, for similar functionality, a different function name is used.

```auto
function send(
    uint16 _dstChainId,
    bytes calldata _remoteAndLocalAddresses,
    bytes calldata _payload,
    address payable _refundAddress,
    address _zroPaymentAddress,
    bytes calldata _adapterParams
) external payable;

```

The same goes with wormhole.

However both these functions intend to do the same process, the smart contract interface level differences make it difficult for integrating multiple cross-chain messaging protocols into one single application.

Standardization of such processes would help in better scalability and operations. Would love to discuss and hear more about this hypothesis.

## Replies

**nambrot** (2022-09-26):

Hi, Nam from Hyperlane here. I agree that the lack of standardization is not great. There has been an attempt to standardize a subset here [EIPs/eip-5164.md at a641fed8dd2d8ca3799bea19b2c77d9528728f64 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/a641fed8dd2d8ca3799bea19b2c77d9528728f64/EIPS/eip-5164.md)

I would imagine in this early phase, developers probably haven’t nailed down the API yet, so i’m not sure we can standardize quite yet.

---

**sujithsomraaj** (2022-09-26):

Hi Nam, thanks for responding. I agree that its early stages and without much open development. But it also makes sense to have standard interfaces as it could make things simpler in future.

yeah EIP 5164 is a great start. But I feel the standardisation of both the initiation interface alongside the execution side makes more sense.

Just implementing standardisation on relayer front would solve only a few problems. Since different protocols vary greatly on the start chain (or source chain or the initiation chain), it makes more sense for us to standardise them.


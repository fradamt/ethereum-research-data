---
source: magicians
topic_id: 3286
title: EIP-712 Standards Clarification (primaryType as DomainType)
author: SilentCicero
date: "2019-05-17"
category: EIPs
tags: [eip-712]
url: https://ethereum-magicians.org/t/eip-712-standards-clarification-primarytype-as-domaintype/3286
views: 1741
likes: 1
posts_count: 4
---

# EIP-712 Standards Clarification (primaryType as DomainType)

Is there any reason why I couldn’t set the `primaryType` to the `EIP712Domain` type? It seems that would still be congruent to EIP712, but would allow me to specify the typing / data in the way I want, which is highly gas sensitive for deployment / verification (thus constructing only a single type and not 2 would be ideal). Yes, I have replay protection covered on all fronts.

The type data for a eth_signTypedDataV3 request to metamask would be as follows:

```auto
const typedData = {
  types: {
    EIP712Domain: [
      { name: "chainId", type: "uint256" },
      { name: "verifyingContract", type: "address" },
      { name: "nonce", type: "uint256" },
      { name: "destination", type: "address" },
      { name: "gasLimit", type: "uint256" },
      { name: "data", type: "bytes" },
    ],
  },
  domain: {
    chainId: 1,
    verifyingContract,
    nonce,
    destination,
    gasLimit,
    data,
  },
  primaryType: "EIP712Domain",
  message: {},
};
```

Can this be clarified [@fulldecent](/u/fulldecent) [@danfinlay](/u/danfinlay)?

I believe this to be standard, even if it’s a slight misuse of EIP712 intentions. I just don’t like being constrained to two hash productions if I don’t absolutely need it. And in this case, it would be great to get all the typed data work done in the domain than in the message / secondary data.

The change to the current EIP712 library would be as follows, as is extremely minimal:

https://github.com/MetaMask/eth-sig-util/pull/51

## Replies

**danfinlay** (2019-05-22):

Thanks for posting, will try to look closer soon. To add context, you also sent me this example MultiSig wallet as part of your reason for wanting this to work:


      [github.com](https://github.com/SilentCicero/MultiSignatureWallet/blob/master/MultiSignatureWallet_Draft.yul)




####

```yul
/**
  * @title MultiSignatureWallet
  * @author Nick Dodson
  * @notice 312 byte Weighted EIP712 Signing Compliant Delegate-Call Enabled MultiSignature Wallet for the Ethereum Virtual Machine
  */
object "MultiSignatureWallet" {
  code {
    // constructor: uint256(signatures required) + address[] signatories (bytes32 sep|chunks|data...)
    codecopy(0, 312, codesize()) // setup constructor args: mem positon 0 | code size 280 (before args)

    for { let i := 96 } gt(mload(i), 0) { i := add(i, 32) } { // iterate through signatory addresses, address > 0
        sstore(mload(i), 1) // address => 1 (weight map
    }

    sstore(1, mload(0)) // map contract address => signatures required (moved ahead of user initiated address => weight setting)

    datacopy(0, dataoffset("Runtime"), datasize("Runtime")) // now switch over to runtime code from constructor
    return(0, datasize("Runtime"))
  }
  object "Runtime" {
```

  This file has been truncated. [show original](https://github.com/SilentCicero/MultiSignatureWallet/blob/master/MultiSignatureWallet_Draft.yul)

---

**bitpshr** (2019-05-22):

This should be fine based on the standard as-written, and I also think this strategy can be a big win in certain contexts in terms of gas. Based on the PR, it looks like it can be implemented in a backwards-compatible manner with the existing implementation.

I can’t think of a reason why reducing hashing in this type of case would ever be detrimental.

---

**danfinlay** (2019-05-28):

Published as `eth-sig-util@2.2.0`


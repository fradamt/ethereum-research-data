---
source: magicians
topic_id: 25387
title: "EIP-2 Signature malleability: Why low s instead of dropping v?"
author: wjmelements
date: "2025-09-08"
category: EIPs
tags: [wallet, signatures]
url: https://ethereum-magicians.org/t/eip-2-signature-malleability-why-low-s-instead-of-dropping-v/25387
views: 131
likes: 0
posts_count: 4
---

# EIP-2 Signature malleability: Why low s instead of dropping v?

From EIP-2:

> Allowing transactions with any s value with 0  28 , 28 -> 27 ), and the resulting signature would still be valid.

Malleability was addressed by enforcing “low s”:

> All transaction signatures whose s-value is greater than secp256k1n/2 are now considered invalid.

It seems that another way to fix this could have been to enforce `v = 27`. Then Ethereum signatures could be specified with 64 bytes (r,s) instead of 65 (v,r,s). Why didn’t we do that?

## Replies

**wjmelements** (2025-10-17):

A similar solution was proposed for [ERC-2098: Compact Signature Representation](https://eips.ethereum.org/EIPS/eip-2098). I think the approach I describe here is better because it is backward compatible with ecrecover.

---

**wjmelements** (2025-12-23):

Bitcoin made the same low `s` decision in [BIP 146](https://github.com/bitcoin/bips/blob/master/bip-0146.mediawiki). Seems they [also](https://en.bitcoin.it/wiki/Message_signing#Detailed_specification_of_the_message_signature) have a degree of freedom for `r`.

---

**wjmelements** (2025-12-26):

I made an ERC for low-`v`.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png)

      [ERC-8111: Bound Signatures](https://ethereum-magicians.org/t/erc-8111-bound-signatures/27308) [ERCs](/c/ercs/57)




> Bound Signatures
> Bound signatures are ECDSA signatures bound to a specific v.
> Constraining the y-parity allows signatures to fit into 64 bytes.
> Background
> ECDSA signatures recover two public keys for the same hash.
> ECDSA signatures are recoverable when they indicate which of the public keys corresponds to the signing key.
> Previous developers signaled which using a y-parity bit.
> In Ethereum, this bit is encoded as v.
> ECDSA signatures (r, s) are malleable; the s can be reflected across n/2 (…


---
source: magicians
topic_id: 24360
title: "EIP-7951: Precompile for secp256r1 Curve Support"
author: CarlBeek
date: "2025-05-28"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7951-precompile-for-secp256r1-curve-support/24360
views: 932
likes: 21
posts_count: 13
---

# EIP-7951: Precompile for secp256r1 Curve Support

## EIP-7951: Precompile for secp256r1 Curve Support

Link: [Precompile for secp256r1 Curve Support](https://github.com/ethereum/EIPs/pull/9833/files)

### Summary

This EIP adds secp256r1 ECDSA signature verification to Ethereum mainnet at address 0x100 with 3450 gas cost. It supersedes RIP-7212 with the same interface but fixes critical bugs.

### Why This Matters

- Hardware Integration: Enables native support for Apple Secure Enclave, Android Keystore, HSMs, and FIDO2/WebAuthn devices
- Account Abstraction: Allows device-native signing without seed phrases, reducing friction for mainstream adoption
- Proven Demand: Already deployed on Optimism, Arbitrum, Polygon, and other L2s

### Security Fixes from RIP-7212

1. Point-at-infinity check: avoids undefined edge-case with point-as-infinity
2. Modular comparison: Uses r’ ≡ r (mod n) to ensure all valid signatures succeed

### Technical Specs

- Input: 160 bytes (hash + signature + public key)
- Output: 32 bytes (1 = valid, 0 = invalid)
- Curve: NIST secp256r1 (128-bit security, same as secp256k1)
- Standards: NIST FIPS 186-5 compliant
- Compatibility: 100% compatible with existing RIP-7212 deployments

### Impact

Enables Ethereum to support the signature scheme used by billions of secure hardware devices worldwide, opening new possibilities for account abstraction while maintaining security standards for mainnet deployment.

## Replies

**CPerezz** (2025-05-28):

The benefits are clear. And it should not be a lot of work to include the code for this in clients. k1 is already a similar curve. Would mostly be changing parameters.

I’d add that this matters for another reason.

If we want to go towards Native/Based rollups. This precompile is a MUST HAVE. And needs to match what L2s have (or viceversa). Otherwise, if the precompiles/EVM specs don’t match it will be impossible for L2s/Rollups to become native. Or they will do it at the cost of sacrificing the UX and not offering the precompile anymore.

[@nicocsgy](/u/nicocsgy) are you championing this together with [@ralexstokes](/u/ralexstokes) ? If you need help, I co-authored [GitHub - privacy-scaling-explorations/halo2curves](https://github.com/privacy-scaling-explorations/halo2curves/tree/main) and would be happy to help on bringing this to clients and collaborate on any other things!

---

**LouisTsai** (2025-06-02):

> Output: 32 bytes (1 = valid, 0 = invalid)

For invalid signature or invalid input, it should return empty data, not zero. This follows the RIP-7212 standard

---

**CarlBeek** (2025-06-02):

Yes, that was a typo in this post, it already is `0x01` and `` in the EIP.

---

**nicocsgy** (2025-06-03):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9833/files)














####


      `master` ← `CarlBeek:secp256r1`




          opened 05:57AM - 28 May 25 UTC



          [![](https://avatars.githubusercontent.com/u/12530043?v=4)
            CarlBeek](https://github.com/CarlBeek)



          [+5750
            -0](https://github.com/ethereum/EIPs/pull/9833/files)













could you add this to the OP [@CarlBeek](/u/carlbeek)

---

**SirSpudlington** (2025-06-03):

Secp256r1 support does seem key for improving interoperability with other more widely used standards, however, it might be a good idea to do something similar to `ecrecover` and instead of passing the public key as an input, recover the public key using a recovery ID as it’ll reduce calldata costs. And because finding the recovery ID for Secp256r1 is dead easy.

###### Also this’ll interact well with my EIP: , so I am a little biased in favour

---

**CarlBeek** (2025-06-03):

So this topic came up when discussing [RIP-7212](https://github.com/ethereum/RIPs/blob/master/RIPS/rip-7212.md), the decision to go this route was decided upon because there is much wider library support for a verify function than ecrecover. Also given how widely r1 is supported across the web etc, the decision was made to just match the interface everyone else uses.

Additionally, given that r1 is already live across many L2s (via RIP-7212), the goal of this EIP is to just match that interface.

---

**SirSpudlington** (2025-06-03):

Ah, so it’s a compatibilty thing then. Fair enough, I was more or less thinking about inter-EVM compatibility rather than other existing non-Ethereum implementations but if it is more accepted to provide the public key, then it would make more sense to provide it in the precompile.

---

**thegaram33** (2025-06-06):

In a previous call it was suggested that the L1 version would be deployed in the L1 precompile address range, at a different address compared to the RIP version, because it would be confusing to have a precompile on different chains with slightly different behavior.

Is the reason for reusing the same `0x100` address on L1 that the [security fixes](https://ethereum-magicians.org/t/eip-7951-precompile-for-secp256r1-curve-support/24360#p-59394-security-fixes-from-rip-7212-4) have no impact on normal usage? Or is it because L2s can simply upgrade the precompile to the EIP version?

---

**Ankita.eth** (2025-06-06):

Test your dApp or wallet’s signature verification logic with EIP-7951’s secp256r1 precompile at address 0x100, ensuring it handles the updated point-at-infinity and modular comparison checks to avoid issues when transitioning from RIP-7212.

---

**CarlBeek** (2025-06-09):

Yeah bascially this is identical to 7212, but with the security patches applied. Outside of the degenerate cases, this should be identical. The idea is that we can have a unified ecosystem across L1 and L2 where wallets etc who want to use r1 deploy the same code which will behave in the same way.

Irrespective of this EIP landing on L1, L2s should also update their deployments with the patch, so this EIP should ship on every L2 that has shipped 7212.

---

**nicocsgy** (2025-06-15):

Hey,

I missed this one sorry. We did a quick and efficient working group for this and I we’re good with the proposal. I can have a few words about it in the next ACD if need be but [@CarlBeek](/u/carlbeek) is the man of the situation

---

**wjmelements** (2025-10-17):

We still benefit from a function that recovers the public key from the signature. This EIP unfortunately does not provide that.

I have examined the way this decision was made. Essentially the rollup people rushed out the first spec they thought of and then it became their standard as they rushed to adopt passkeys. Attempts to discuss this were put off. It was rushed. Then this proposal copied the RIP also without scrutiny.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/df788c/48.png) CarlBeek:

> Additionally, given that r1 is already live across many L2s (via RIP-7212), the goal of this EIP is to just match that interface.

I don’t think the interface has to match. It’s already at a different address.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> recover the public key using a recovery ID

I might be mistaken, but both signature malleability and recovery ID can be [eliminated](https://ethereum-magicians.org/t/eip-2-signature-malleability-why-low-s-instead-of-dropping-v/25387) without increasing the signature size from 512 to 513.


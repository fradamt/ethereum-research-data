---
source: magicians
topic_id: 14789
title: "EIP-7212: Precompiled for secp256r1 Curve Support"
author: ulerdogan
date: "2023-06-22"
category: RIPs
tags: [evm, core-eips, precompile, rollups, rip]
url: https://ethereum-magicians.org/t/eip-7212-precompiled-for-secp256r1-curve-support/14789
views: 21845
likes: 302
posts_count: 123
---

# EIP-7212: Precompiled for secp256r1 Curve Support

Hi Magicians ![:mage:](https://ethereum-magicians.org/images/emoji/twitter/mage.png?v=12) ![:magic_wand:](https://ethereum-magicians.org/images/emoji/twitter/magic_wand.png?v=12)

The post is about ~~EIP-7212~~ **RIP-7212** which proposes adding a new precompiled contract to the EVM that allows signature verifications in the “secp256r1” elliptic curve by given parameters of message hash, r - s components of the signature, and x - y coordinates of the public key.

![:pushpin:](https://ethereum-magicians.org/images/emoji/twitter/pushpin.png?v=12) This [post](https://ethereum-magicians.org/t/eip-7212-precompiled-for-secp256r1-curve-support/14789/69) explains moving the proposal from EIP to RIP category.

![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=12) EIP Page (the [PR](https://github.com/ethereum/EIPs/pull/7212)):

https://eips.ethereum.org/EIPS/eip-7212

What are the use cases of the “secp256r1” elliptic curve?

- The secp256k1 elliptic curve, which is the only cryptographic primitive to prove ownership in Ethereum, does not offer flexibility in onboarding new users via new solutions. Adding this new elliptical curve will allow biometric and hardware authorization solutions to be easily executed on-chain.
- Many hardware and software solutions use this elliptic curve as signing algorithms, such as TLS, DNSSEC, Apple’s Secure Enclave, Passkeys, Android Keystore, and Yubikey, which can be used in the EVM.

Why is this precompile recommended, and how do we believe the user/developer experience will be improved?

- The addition of this precompiled contract improves efficiency and gas affordability in the EVM. With the improvement, the gas costs are reduced alongside the computational load decreases, and the block gas limit is maximized to enhance the transaction throughput and overall network performance.
- Supporting an elliptic curve with a precompiled contract provides a uniform and standardized way of operations. So that potential confusion and errors that occur from different implementations can be avoided. The curve operations can be made in reliable implementations in terms of security with precompiled contracts.
- Enabling this precompiled contract improves the developer experience by allowing effortless integration of the curve signatures and building applications on top of it to provide interoperability with different solutions using the curve, resulting in more user-friendly products.

Possible integration ideas of the precompiled contract:

- The EIP-4337 account abstraction wallets can use these elliptic curve signatures to sign the user operation data with mobile device secure elements and then validate them in the smart contracts.
- @arachnid suggested in the ENSDAO that the precompiled contract allows lots of opportunities with DNSSEC for the projects by adding a new cryptographic primitive.

> “One of the major barriers to onchain DNSSEC, along with many other potential projects such as web authentication integration, email verification, and other tasks that rely on verifying ‘real world’ crypto proofs, is the EVM’s limited support for cryptographic primitives.”

![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=12) The proposal has been discussed in the ACDE#168 call, the [summary](https://twitter.com/TimBeiko/status/1692289928401740274?s=20) shared by Tim Beiko.

![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=12) Reference implementation on go-ethereum:

https://github.com/ethereum/go-ethereum/pull/27540

References:

- https://neuromancer.sk/std/secg/secp256r1
- "secp256r1" - For 256-Bit ECC Keys
- https://wiki.hyperledger.org/display/BESU/SECP256R1+Support
- A “secp256r1” package has already been included in the Besu Native library which is used by Besu client.

## Replies

**ccamrobertson** (2023-06-23):

Glad to see someone propose this; we wrote [a bespoke contract](https://github.com/tdrerup/elliptic-curve-solidity) to do this at significant gas expense in 2019 for [KONG Cash notes](https://ipfs.io/ipfs/QmbHnwBuM7Y41Q1DqnMDRx8yQ1aCMtqVka9biPY6cjWogq).

I would explicitly add secure elements as a rationale under hardware – low cost secure element chips are typically designed with P256 in order to support TLS. See the common [ATTEC608A part from Microchip](https://www.microchip.com/en-us/product/ATECC608A) for one example.

---

**shemnon** (2023-06-26):

This precompile returns the actual signature instead of the address reduced form?  (like ECRECOVER does)?

I’m personally in favor of that, but I think that deserves an explicit call-out in the specification section or possibly more appropriately the backwards compatibility section.  The conversion of an EOA address is only done for secp256k1 curve keys, so a snippit to convert signatures to addresses is unneeded. Considering the number of times ECRECOVER is mentioned in the EIP we should call it out and add a note to explain why, to avoid confusion on the part of future readers.

---

**ulerdogan** (2023-06-26):

Hi, thanks for contributing!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> This precompile returns the actual signature instead of the address reduced form? (like ECRECOVER does)?

The implementation in the proposal only returns if the signature is valid or not by 1 and 0. I am sharing my design choice (almost the same as your comments) from the PR [comments](https://github.com/ethereum/EIPs/pull/7212#discussion_r1240461449):

> We need v value to recover public key without the x and y coordinates. The v value can be found by above-mentioned methods, but let me explain my design choice:
>
>
> While we are making recovery with the ecrecover, we can reach the public address of the EOA accounts, so it can be directly used in the smart contracts. Unlikely, recovering the secp256r1 public key does not match any default stored types, and we still need to store the account public key.
> Having to find the v value in the implementation part of the signature creates complexity on the application side. So, I didn’t want to bring this complexity for the applications. Still, I would love to reassess and edit the EIP to implement recovery after discussion.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> The conversion of an EOA address is only done for secp256k1 curve keys, so a snippit to convert signatures to addresses is unneeded.

The [Rationale part](https://github.com/ethereum/EIPs/blob/d5fb2f54deb4faa498cb79253431a19f7b7c1302/EIPS/eip-7212.md#rationale) includes this design choice, but I agree with you that it can be improved with this information.

---

Lastly, I couldn’t understand why you suggested explaining it in the Backwards Compatibility part, as it is a completely separate implementation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I’m personally in favor of that, but I think that deserves an explicit call-out in the specification section or possibly more appropriately the backwards compatibility section.

---

**ulerdogan** (2023-06-27):

Moving [@_pm](/u/_pm)’s comment in the PR to here for the discussion:

> paulmillr commented yesterday
> -1
>
>
> 256r1 is usually more vulnerable to timing attacks than stuff like 25519.
> 256r1 is not even recommended by nist at this point, 384r1 is.
> There are some rumors with regards to general security of r1 curves, it’s unclear.
> Adding a new elliptic curve impl into ALL execution layer clients is not a trivial task. I don’t think the feature is too useful for this.

My comments:

1. The Golang crypto library works in constant time for the secp256r1 curve. Considering that the timing attacks are implementation dependent, it can be assumed to be safe.
2. I think that NIST’s recommendations points to the PQC, which are not ready for the production.
3. Apart from rumors, I did not see some definite evidences regarding security risks.
4. I see that the secp256r1 curve is the most mass adopted curve and it has a widespread use in many cases. It would be a great step on the mass adoption of Ethereum.

I would love to hear more about any ideas and researches that analyzing the vulnerabilities regarding the security risks of the curve.

---

**jdetychey** (2023-06-27):

Happy to join force on that.

We built a lof of stuff in Solidity already:

https://github.com/alembic-tech/P256-verify-signature

Demo: https://p256.alembic.tech/

And some doc:

[The DeFi Infrastructurefor Businesses](https://docs.alembic.tech/account-abstraction/p256-biometric-signer)

---

**ccamrobertson** (2023-06-27):

[@ulerdogan](/u/ulerdogan) I just recalled that a broader precompile effort was put forth in 2019 with [EIP-1829](https://eips.ethereum.org/EIPS/eip-1829). It might be useful to understand from [@Recmo](/u/recmo) what happened there and if revival of a more generic precompile would still be useful.

My sense is that 1829 has now been fully supplanted by one-off EIPs for specific curves and as such moving forward with a secp256r1 makes sense, but it might be worth reviewing.

---

**ulerdogan** (2023-06-28):

Hey, thanks for reviving the idea!

I followed the [EIP-1829 discussions](https://ethereum-magicians.org/t/precompile-for-general-elliptic-curve-linear-combinations/2581) and some other contents. Then, I found [EIP-1962](https://eips.ethereum.org/EIPS/eip-1962) which is a continuation of EIP-1829 by Alex. It seems that the problems in the implementation later revealed [EIP-2537](https://eips.ethereum.org/EIPS/eip-2537) which was planned to be included in Cancun upgrade, now [postponed](https://github.com/ethereum/execution-specs/commit/aa812f892c7f53917f40aca39eaf2dcbb057340a#diff-e50951fad0cf9cbf5246f973d6e1d969c24d5bffb0417f23033ceb1416fc879bL13).

Apparently, generalized curve implementations failed and were replaced by specific ones with EIP-2537 ([notes] by [@timbeiko](/u/timbeiko) (https://twitter.com/TimBeiko/status/1235931932644564995?s=20) from an ACD call).

I would love to hear the ideas of those who have worked on precompiled contract implementations for curves about the previous experiences and this proposal! [@Recmo](/u/recmo) [@shamatar](/u/shamatar) [@ralexstokes](/u/ralexstokes) [@kelly](/u/kelly)

---

**xzhang** (2023-06-28):

I support this EIP. Just image how many new users will be attracted to Ethereum without the trouble to backup their mnemonics or private key on a piece of paper…

---

**fmc** (2023-07-04):

I do feel, that specific support for the secp256r1 curve is needed. There are a lot of requests for a gas-efficient way to verify passkey-signed data on-chain. And this proposal will make it possible.

---

**longfin** (2023-07-04):

I agree with your opinion that secp256r1 can be enough. however [Ed25519](http://ed25519.cr.yp.to/) seems to still have many benefits, especially less computation.

And, it also seems that there was already [an EIP](https://github.com/ethereum/EIPs/blob/3907772a0f11d0095ee5c2e364f2774add95cfc7/EIPS/eip-665.md) about Ed25519, could we leverage that proposal?

---

**Toshi** (2023-07-05):

As per Vitalik’s post quite some time ago, I don’t recommend using the secp256r1 curves.

https://bitcoinmagazine.com/technical/satoshis-genius-unexpected-ways-in-which-bitcoin-dodged-some-cryptographic-bullet-1382996984

" The obvious question is this: where did the seed come from? Why was the seed not chosen to be some more innocent-looking number, like 15? In light of recent revelations regarding the US National Security Agency [subverting cryptographic standards](https://bitcointalk.org/index.php?topic=289795.0), an obvious concern is that the seed was somehow deliberately chosen in order to make the curve weak in some way that only the NSA knows. Thankfully, the wiggle room is not unlimited. Because of the properties of hash functions, the NSA could not have found one “weak” curve and then gone backward to determine the seed; rather, the only avenue of attack is to try different seeds until one turns out to generate a curve that is weak. If the NSA knows of an elliptic curve vulnerability that affects only one specific curve, the pseudorandom parameter generation process would prevent them from standardizing it. However, if they knew of a weakness in one in every billion curves, then the process offers no protection; for all we know, `c49d360886e704936a6678e1139d26b7819f7e90` could have been the billionth seed that the National Institute for Standards in Technology tried."

---

**ccamrobertson** (2023-07-05):

[@longfin](/u/longfin) [@Toshi](/u/toshi) I don’t think there are many that would dispute that secp256r1 is a non-ideal curve, however, the claims of a backdoor have been made for well over a decade without any substantive evidence of the existence of one. This is significantly different than [the discussion for a SHA1 precompile](https://github.com/ethereum/EIPs/issues/180) which was demonstrably malleable at the time of proposal.

Proposing other curves arbitrarily ignores the key arguments in favor of this EIP which is that billions of devices have hardware accelerated support and isolated secure storage for secp256r1. Ed25519 would be great, but low cost secure element chips don’t support it (nor do they support secp256k1).

If this proposal sought to shift EOA creation to secp256r1 I would understand the concerns here, however, just adding it as a precompile doesn’t seem to me to warrant the ire that it’s currently receiving.

---

**longfin** (2023-07-06):

First of all, I don’t believe the rumors of a backdoor on secp256r1 seriously too. ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

Aside from unconfirmed concerns about backdoors, the difference between secp256r1 and Ed25519 seems to be whether we will use relatively the modern curve or the little bit old curve that supports many devices, and coverage seems to make sense at this moment. ![:ok_man:](https://ethereum-magicians.org/images/emoji/twitter/ok_man.png?v=12)

---

**ulerdogan** (2023-07-06):

Thanks for your comments [@longfin](/u/longfin) [@Toshi](/u/toshi), and thanks for your explanation -I completely agree with you- [@ccamrobertson](/u/ccamrobertson).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/longfin/48/9934_2.png) longfin:

> Aside from unconfirmed concerns about backdoors, the difference between secp256r1 and Ed25519 seems to be whether we will use relatively the modern curve or the little bit old curve that supports many devices, and coverage seems to make sense at this moment.

I think that even if `ed25519` presents an efficient usage, I can’t find enough motivation to bring this curve into the EVM, but the `secp256r1` curve has many cases that can directly improve the UX in Ethereum as it’s one of the most widely supported elliptic curves in the internet/mobile ecosystem.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/e480ec/48.png) Toshi:

> As per Vitalik’s post quite some time ago, I don’t recommend using the secp256r1 curves.

Also, my comments about the rumours: I agree with the idea that choosing the `k1` curve as the main security mechanism of Bitcoin and Ethereum, but bringing the `r1` curve as an additional verification mechanism in the app level, does not contradict this selection.

Additionally, pointing out an upper [discussion](https://ethereum-magicians.org/t/eip-7212-precompiled-for-secp256r1-curve-support/14789/5):

**
Summary**

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ulerdogan/48/9227_2.png) ulerdogan:

> Moving @_pm’s comment in the PR to here for the discussion:
>
>
>
> paulmillr  commented yesterday
> -1
>
>
> 256r1 is usually more vulnerable to timing attacks than stuff like 25519.
> 256r1 is not even recommended by nist at this point, 384r1 is.
> There are some rumors with regards to general security of r1 curves, it’s unclear.
> Adding a new elliptic curve impl into ALL execution layer clients is not a trivial task. I don’t think the feature is too useful for this.

My comments:

1. The Golang crypto library works in constant time for the secp256r1 curve. Considering that the timing attacks are implementation dependent, it can be assumed to be safe.
2. I think that NIST’s recommendations points to the PQC, which are not ready for the production.
3. Apart from rumors, I did not see some definite evidences regarding security risks.
4. I see that the secp256r1 curve is the most mass adopted curve and it has a widespread use in many cases. It would be a great step on the mass adoption of Ethereum.

I would love to hear more about any ideas and researches that analyzing the vulnerabilities regarding the security risks of the curve.

---

**mac** (2023-07-06):

i’m starting to see account-abstraction projects implement “riced-out” versions of secp256r1 signature verification to support passkey authenticators who dont support Koblitz, to save on gas. How the heck can I, a mere mortal, review, understand, and audit these implementations:

![:small_orange_diamond:](https://ethereum-magicians.org/images/emoji/twitter/small_orange_diamond.png?v=12)[trampoline/contracts/EllipticCurve.sol at webauthn · eth-infinitism/trampoline · GitHub](https://github.com/eth-infinitism/trampoline/blob/webauthn/contracts/EllipticCurve.sol)

![:small_orange_diamond:](https://ethereum-magicians.org/images/emoji/twitter/small_orange_diamond.png?v=12)[aa-passkeys-wallet/src/Secp256r1.sol at main · itsobvioustech/aa-passkeys-wallet · GitHub](https://github.com/itsobvioustech/aa-passkeys-wallet/blob/main/src/Secp256r1.sol)

More importantly, if we want to onboard the next ${num} users onto the EVM, there are about 4billion devices that support webauthn: navigator.credentials.create() to securely create, store, and sign a PublicKeyCredential without installing anything

however, none of the devices I tested: (e.g., ~samsung phones, ~pixel phones, various iphones, m1 macbook, dell laptop (windows / linux / macOS))  support the Koblitz curve (secp256k1), they can only do secp256r1 (P-256, COSE Curve: 1, Alg: -7)

can we please get a precompile (or native support) for secp256r1 ? cc [@vbuterin](/u/vbuterin)

---

**ccamrobertson** (2023-07-06):

Fantastic point. The harm from everyone rolling their own secp256r1 could be massive. If an AA scheme catches on leveraging a broken implementation you will see real loss vs. hypothetical loss from the NSA.

---

**jdetychey** (2023-07-07):

[@mac](/u/mac) Ledger security team will present this [paper](https://eprint.iacr.org/2023/939.pdf) on the 17th at ethcc “WebAuthn Optimization: optimizing ECC sec256r1” this extend the resources in the repo previously shared [above](https://github.com/alembic-tech/P256-verify-signature).

Regarding the debate on the security of p256 I recommend this [article](https://www.lunesu.com/update/2016/11/01/a-tale-of-two-curves-hardware-signing-for-ethereum.html)

This old Serenity EIP-101 discussing is relevant too:

https://github.com/ethereum/EIPs/issues/28#issuecomment-160335523

---

**sbacha** (2023-07-09):

OP produced an example implementation for OP hackathon project: [Opclave | ETHGlobal](https://ethglobal.com/showcase/opclave-opstack-impr-erc4337-and-apple-sign-94def)

> opclave-scaling2023/precompiles at main · itublockchain/opclave-scaling2023 · GitHub

Claiming this will help users manage their private keys better by entrenching them in a proprietary SoC solution (Apple Secure Enclave) is ridiculous. We trust in math, not Chinese supply chain vendors. Claiming that “backdooring” is not viable misses the point: we are not claiming that all chips are backdoored, only that certain chips be intercepted en route to end user by TAG/TAU and flashed with backdoor. It is hard to verify hardware, its easier to verify software.

Here is an approach that uses existing authentication schemes to provide user key management, check their github for examples. https://mfkdf.com/

Precompiles should be ossified, they were always a “temporary” solution, that was 8 years ago.

![:sunny:](https://ethereum-magicians.org/images/emoji/twitter/sunny.png?v=12)![:saluting_face:](https://ethereum-magicians.org/images/emoji/twitter/saluting_face.png?v=12)

---

**Arachnid** (2023-07-14):

Strongly in support of this - secp256r1 is by far the most widely used curve, and enabling it to be efficiently verified in the EVM will enable countless integrations with existing infrastructure that are currently impractical.

Those suggesting alternate curves or raising issues with the derivation of the secp256r1 parameters are missing the point; the idea here is not to pick the ideal curve, it’s to add functionality that permits integrating with external and legacy applications efficiently.

I would suggest that an ‘ecrecover’ type implementation is more versatile, though; it’s easy to convert ecrecover into a signature verification operation, but impossible to do the inverse.

---

**mryalamanchi** (2023-07-21):

In strong support of this proposal.

Generally speaking, hard reproducible evidence has to exist for the claims of NSA influencing NIST to weaken the secp256r1.

Otherwise it’s unproductive for the conversation.

Alexander has been constantly requesting and implementing support for secp256k1 for the bitcoin community in Apple’s Swift crypto library for the past 4 years: [New API Proposal: Add SECG curves, especially `secp256k1` · Issue #8 · apple/swift-crypto · GitHub](https://github.com/apple/swift-crypto/issues/8)

It’s evident from the conversation that they consider secp256k1 to be limited to cryptocurrency and not for “wide usecases” and have been delaying and denying support.

Considering this proposal, the wallet UX for regular Mobile users using Android/iOS/Android-derivate OSes can drastically improve.

This also includes keychain devices which already support the curve or hardware devices which can be built using secure element (SE) that support secp256r1.

So it isn’t just Mobile Devices, but beyond that, large no. of IoT devices can come integrated with SE and utilise this precompile to unlock new/existing use-cases.


*(102 more replies not shown)*

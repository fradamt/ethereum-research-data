---
source: magicians
topic_id: 25293
title: The case for EIP-7932 & EIP-8030 inclusion in Glamsterdam
author: SirSpudlington
date: "2025-08-29"
category: EIPs
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/the-case-for-eip-7932-eip-8030-inclusion-in-glamsterdam/25293
views: 428
likes: 4
posts_count: 12
---

# The case for EIP-7932 & EIP-8030 inclusion in Glamsterdam

**Note: EIP-7980 has been replaced with EIP-8030 for P256 curve support.**

This was the template for headliner EIPs; however, it also works well for other EIPs.

This EIP depends on some parts of [EIP-7919](https://eips.ethereum.org/EIPS/eip-7919).

- Summary:

EIP-7932 adds the concept of algorithms, a new registry of different signature algorithms. It also extends this by adding an SSZ transaction container to allow transaction signing and a new precompile to decode these new signatures.
- EIP-7980 is mostly for testing EIP-7932; it adds Ed25519 to the list of algorithms supported by EIP-7932.
- EIP-8030 is mostly for testing EIP-7932; it adds P256 to the list of algorithms supported by EIP-7932.

**Detailed Justification:**

- Introducing these EIPs early allows for existing tooling to include support for the new transaction type and contracts to use the newer sigrecover precompile. If large scale adoption occurs before secp256k1 becomes a vulnerability, it’ll make it easier to switch to a PQ-enabled algorithm.
- Having a single standard makes it easy for client teams to include (or remove) any number of new algorithms without requiring smart contracts to change logic. It can also reduce software bloat that would be caused if every new post-quantum algorithm came with a new transaction type which must then be compatible with every other transaction type.
- P256 is similar to secp256k1 and provides enough difference to work as a great reference for running tests for EIP-7932. P256 is also a well-known battle tested algorithm, so there is little chance for a bug in the cryptography.
- P256 is also widely supported in HSMs and TPMs allowing for more secure account key storage.

**Benefit over Account Abstraction:**

- Account Abstraction can provide functionally the same result, however, it still requires secp256k1 for the bundling transaction. Once secp256k1 needs to be switched off, EIP-7932 can take over as the common transaction format (assuming that it has been previously included).

**Stakeholder Impact:**

- Currently, this proposal is not well known. As such, there is very little expressed support for or against this proposal.

**Technical Readiness:**

- EIP-7932 is still in draft and subject to change. Once the core developers no longer require changes, complete test cases will be provided for both EIP-7932 and EIP-7980 to ensure correct serialization and parsing.
- As of 28/08/2025, no client implementations have been attempted.

**Security & Open Questions:** Due to limited engagement with this proposal, no open questions have been proposed. If any questions are posted here, I’ll respond to them. EIP-7932 is mostly designed for serialization and formatting, the majority of security concerns are algorithm-specific.

## Replies

**SirSpudlington** (2025-09-11):

After [ACDE #220](https://github.com/ethereum/pm/issues/1707), there were some questions that I’ll answer here:

### The SSZ transaction type may block inclusion, could RLP be used?

It is entirely possible to also add an RLP transaction type. I initially moved away from RLP as it was significantly more complex to use RLP (at least my initial idea was). If anyone has a simple way to have RLP support, I’ll be more than happy to include it.

### Ed25519 is not quantum secure; we should prioritise PQ algorithms

**I agree** that EIP-7932 should primarily use PQ algorithms.

The reason I went with Ed25519 is because it is another battle-tested algorithm that is similar to secp256k1. This allows us to fully test EIP-7932, **without** releasing a newer algorithm like ML-DSA with potentially unknown security holes.

Similarly with RLP support, this EIP can change to make life easier for everyone. If there is some way to test EIP-7932 without adding additional cryptography, that is also a possible path.

### Does account abstraction already do this?

Yes, it does. However, `sigrecover` can help unify the result of addresses with native and account abstraction schemes. I won’t deny it, **account abstraction can work as a viable replacement by itself**. It just would be a nicer UX if all account abstraction systems with multiple signature schemes result in the same address from the same key.

### Should we change transaction signature types?

As Felix said, “[changing transaction signature schemes] has never been done before”. That is why this EIP is modular, it allows us to change the signature format only once but swap in new algorithms much more efficiently. On the topic of whether we should even try to change tx sig types, it’ll have to happen *at some point*. It might be better to do this early with a lot more planning, instead of within a couple of days after ECDSA becomes vulnerable.

### Do we need to redefine how an Ethereum address is calculated?

Currently there are three ways to make an Ethereum account (i.e. entry in the state trie, etc):

- Send ETH to that account
- Via the CREATE or CREATE2 opcodes
- Via a precompile or network wide action

The account creation process and proving account ownership are rather decoupled. This means that as long as someone can prove access to an account e.g., by smart contract code or by recovering and hashing the transaction signer, they can spend the funds of the account. The same applies to EIP-7932, nothing changes in regards to addresses other than an additional way to prove account ownership.

### Why I am against fixing the signature algorithms

If, in the distant future, we find a new, better PQ algorithm to replace Falcon or ML-DSA, **all** existing tooling, infrastructure and smart contracts would either break, or need to be upgraded. Decoupling signature schemes and accounts can still allow people to use legacy algorithms (if they are just inefficient) **and** ensure no compatibility issues exist with the new algorithms so adoption can happen much faster. I believe [@jflo](/u/jflo) touched upon this in the ACDE call.

CC: [@shemnon](/u/shemnon) [@fjl](/u/fjl) (sorry if I incorrectly pinged you, there were *many people* to choose from in the list)

Nothing stops an algorithm specification from calling precompile logic; `sigrecover` and the wrapper only turns some signature `bytes` into an `ExecutionAddress`. A precompile call can happen during this process, so `p256verify` can be used as well (if deemed a good idea). [EIP-7592](https://ethereum-magicians.org/t/eip-7592-falcon-signature-verification-pre-compile/18053) can also be used during these processes.

---

**shemnon** (2025-09-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> If anyone has a simple way to have RLP support, I’ll be more than happy to include it.

I see two main ways to do it, but both hinge on a typed signature list…

`[sig_type, [ ... signature data ...]]` or `[sig_type, ... signature data ...]`

The first value is a selector (like the old union type) that says what type the signaure data is, and then the signature data itself varies based on the type itself.  The nested list form may have better traction wih some RLP libs but the continuation form saves a byte or three. (with signatures in the kilobyte range, does it matter?)

Then for the TX there are two principal approaches, (a) a generic typed form and (b) update existing forms.

`[body type, [... body data ...], sig_type, [... sig data ...]]` is one form of (a) and for (b) it would consist of replacing the `..., y_parity, r, s` part of the existing sigs with `..., [sig_type, [...sig data...]]` where the list for y_parity serves as the logical switch.  I prefer the first aesthetically, and also [felix’s concern](https://ethereum-magicians.org/t/the-case-for-eip-7932-eip-7980-inclusion-in-glamsterdam/25293/2#p-61857-should-we-change-transaction-signature-types-4) about re-defining tx formats.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> This allows us to fully test EIP-7932, without releasing a newer algorithm like ML-DSA

P256 would be a better choice as the precompile already exists, meaning the crypto library is in the build process of most clients.  The current precompile requires the pubkey and has no pubkey extraction but that is an opportunity to explore supportin algos without key extraction.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> Do we need to redefine how an Ethereum address is calculated?

I think the real concern here is the derivation formula for an EOA—CREATE and CREATE2 will naturally derive from that.  Current it is just the keccak hash of the uncompressed ECDSA(secp256k1) key.  For new signature types it can be similar, but we will need to bake in the algorithm of the key too. If we use a typed signature with a signature ID a hash pre-image of `sig_type || pubkey` (where || is concatenation) serves the need and then there will be no collisions unless the public key of a particular algorithm is 61 bytes, then we just need to add padding somewhere if that happens.

---

**SirSpudlington** (2025-09-15):

Thank you for the suggestions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I see two main ways to do it, but both hinge on a typed signature list…

Both will work, I much prefer option A though. I feel like creating a new possible TX structure for **every** current TX may be a bit cumbersome. I do like the `[body type, [... body data ...], sig_type, [... sig data ...]]`, it only adds a single **new** TX type. But as `sig_data` is just *some bytes* that the algorithm decodes & verifies, it may be good to just have it as `[body type, [... body data ...], sig_type, sig_data ]`

Edit: one issue is legacy [EIP-155](https://eips.ethereum.org/EIPS/eip-155) TXs, they do some weird stuff with the signature data i’d assume we’d set to `b""` or `0x0`. I believe EIP-155 TXs have mostly been phased out in favour of [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559). So it would not be completely absurd to just prevent `body_type` from being `== 0x0` or `> 0x7f`

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> P256 would be a better choice as the precompile already exists, meaning the crypto library is in the build process of most clients. The current precompile requires the pubkey and has no pubkey extraction but that is an opportunity to explore supportin algos without key extraction.

P256 it is then. I am sort of on the fence of whether I should change EIP-7980 to be for P256 but I feel like that may cause some confusion. Or should I draft up a new EIP and withdraw EIP-7980?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> For new signature types it can be similar, but we will need to bake in the algorithm of the key too. If we use a typed signature with a signature ID a hash pre-image of sig_type || pubkey (where || is concatenation) serves the need and then there will be no collisions unless the public key of a particular algorithm is 61 bytes, then we just need to add padding somewhere if that happens.

This is a much better idea. If `verify(...)` returns `pub_key: bytes` instead of an `ExecutionAddress`, we can then pass it through `keccak(sig_type || pub_key)` (or some variant of that) and limit the blast radius of a bad algorithm to just that algorithm.

---

**shemnon** (2025-09-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> But as sig_data is just some bytes that the algorithm decodes & verifies, it may be good to just have it as [body type, [... body data ...], sig_type, sig_data ]

unless we use some standard means to pick a meaningful encoding, like DER or such, there will be multiple parts of the `sig_data`. This would result in ethereum creating it’s own packed encodings, and in that case wouldn’t it make more sense to just use RLP?  i.e. for ed25519 `... 0x10, [pubkey, signature]` or for P256 `... 0x11, [y_parity, r, s]]` rather than an opaque binary? The field choice would be driven by what the libraries would want as inputs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> Edit: one issue is legacy EIP-155 TXs, they do some weird stuff with the signature data i’d assume we’d set to b"" or 0x0. I believe EIP-155 TXs have mostly been phased out in favour of EIP-1559. So it would not be completely absurd to just prevent body_type from being == 0x0 or > 0x7f

The biggest problem with legacy/EIP-155 form is that the “signature form” is non-standard based on EIP-2718.  In fact, if we go with `body type | [... body data ...],` as the signature pre-image for signatures then I believe that ECDSA signatures will be the same, but not for pre-2718 because the signature was just the RLP without a type prefix. So signing would be done with a slice of the transacion bytes. But the transaction hash will be different, so malleability needs to be considered.

I don’t think we need to obsess with deprecating and removing old formats, they should continue to live side-by-side as the entire ecosystem will be generationg types 0 through 4 signatures for a long time. Perhaps the new format with legacy payloads is only valid with new signature types, but future signature types only go in the modular signature.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> This is a much better idea. If verify(...) returns pub_key: bytes instead of an ExecutionAddress, we can then pass it through keccak(sig_type || pub_key) (or some variant of that) and limit the blast radius of a bad algorithm to just that algorithm.

There is also the question of address space expansion. Grover’s algorithm will make 160-bit addresses risky, regardless of the hash, so we need to consider how we handle this.  So returning the pubkey (regradless of length) or a full-width hash used for address generation may be needed.

But P256VERIFY sets an expectation that the results are true or false: it verifies or it doesn’t.

---

**SirSpudlington** (2025-09-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> This would result in ethereum creating it’s own packed encodings, and in that case wouldn’t it make more sense to just use RLP? i.e. for ed25519 ... 0x10, [pubkey, signature] or for P256 ... 0x11, [y_parity, r, s]] rather than an opaque binary? The field choice would be driven by what the libraries would want as inputs.

I did think of using SSZ or RLP for the signature. But as most signatures are constant size, I’d argue that it would be easier to use raw bytes and the solidity `abi.encodePacked` function. Then again, if we just say “an RLP encoded value”, we could let each algorithm decide whether to use `bytes` or RLP structure, but It does introduce issues with the `MAX_SIZE` parameter.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> The biggest problem with legacy/EIP-155 form is that the “signature form” is non-standard based on EIP-2718. In fact, if we go with body type | [... body data ...], as the signature pre-image for signatures then I believe that ECDSA signatures will be the same, but not for pre-2718 because the signature was just the RLP without a type prefix. So signing would be done with a slice of the transacion bytes. But the transaction hash will be different, so malleability needs to be considered.

I agree we should go with `body type | [... body data ...]`. We could make an exception for EIP-155/legacy to use the format in EIP-155, but I am unsure how this would work. It creates a lot of overhead and several new edge cases. Malleability can be all but eliminated by disallowing secp256k1-only transactions (inside EIP-7932 transactions), one tx-level signature must not be secp256k1 for it be valid.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> There is also the question of address space expansion. Grover’s algorithm will make 160-bit addresses risky, regardless of the hash, so we need to consider how we handle this.

If we need to extend the address space, it should be a separate EIP. It could be grouped with EIP-7932 in a meta-EIP, but to make this already somewhat complex EIP more complicated would make it almost impossible to implement.

Edit: To avoid spamming PRs, I am going to put the refinements [Here: github.com](https://github.com/ethereum/EIPs/compare/master...SirSpudlington:EIPs:draftv2)

---

**shemnon** (2025-09-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sirspudlington/48/14835_2.png) SirSpudlington:

> I did think of using SSZ or RLP for the signature. But as most signatures are constant size, I’d argue that it would be easier to use raw bytes and the solidity abi.encodePacked function. Then again, if we just say “an RLP encoded value”, we could let each algorithm decide whether to use bytes or RLP structure, but It does introduce issues with the MAX_SIZE parameter.

Consider the case of address derivations, for systems where the pubkey is not extracted from the signature but is instead transmitted with the signature (nearly all PQC schemes at the moment) then the address derivation can simply access the parsed field to determine the “sender address”

But if it were a variable sized byte array then it does provide an easier path for arbitrary extensions by L2s that want to add new schemes, and will only require support in two functions (signature validation and address calculation) without requiring structural changes to the rest of the client code.

This, however, would mean ECDSA(secp256k1) sigatures would need an in-spec definition that is not `... y_parity, r, s]` but instead a binary form opaque to RLP.

---

**SirSpudlington** (2025-09-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> This, however, would mean ECDSA(secp256k1) sigatures would need an in-spec definition that is not ... y_parity, r, s] but instead a binary form opaque to RLP.

Why would this be the case? EIP-7932 does not touch secp256k1.

---

**shemnon** (2025-09-17):

True, so would P256 curve signatures have a different treatment then?  Except for the curve they are highly similar, would we propose a pattern that is different?

---

**SirSpudlington** (2025-09-17):

~~I’d suggest so, it could it literally just be RLP encoded r, s and y values or just concatenation of r || s || y~~

After looking at the NIST spec and some Googling, it appears that P256 does not really handle public key recovery well. To maximise the compatibility with [RIP-7212](https://github.com/ethereum/RIPs/blob/master/RIPS/rip-7212.md), I am going to use `r || s || x || y` - the same as P256VERIFY.

---

**SirSpudlington** (2025-09-20):

I have withdrawn EIP-7980, once the EIP-7932 spec get finalized-ish, I’ll move to get the [P256 replacement EIP](https://github.com/ethereum/EIPs/pull/10373) out of a draft PR.

---

**SirSpudlington** (2025-10-01):

~~I have completed a first draft for RLP support. I am going to do a bit of re-reading and thinking before merging it to the main EIP repo. Anyone can view the draft [here](https://github.com/SirSpudlington/EIPs/blob/draftv2/EIPS/eip-7932.md).~~

RLP support & additional fixes have been merged into the master EIP. Both RLP and SSZ are currently present.

cc: [@shemnon](/u/shemnon)


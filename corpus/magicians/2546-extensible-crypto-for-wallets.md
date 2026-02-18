---
source: magicians
topic_id: 2546
title: Extensible crypto for wallets
author: Recmo
date: "2019-01-29"
category: Web > Wallets
tags: [wallet, security, wasm]
url: https://ethereum-magicians.org/t/extensible-crypto-for-wallets/2546
views: 2727
likes: 19
posts_count: 20
---

# Extensible crypto for wallets

# Extensible crypto for wallets

## Problem

SNARKs and STARKs require signatures algorithms that differ from Ethereums default one.

[EIP-1024](https://github.com/ethereum/EIPs/pull/1098) proposes encryption functions to be added to wallets, forcing all wallets to implement new crypto, which is complex and risky.

DApps  have anticipated future needs for new cryptographic algorithms, for example diffie-hellman, off-the-record messaging, etc. Going through an EIP process each time is a bottleneck.

As discussed in the ETH1x workshop, we should focus on solving classes of problems, not point features. This proposal aims to solve this class of problems.

## Proposal

DApp developers can submit webassembly bytecode for their custom crypto using a `register_algorithm` API. It can then be called using a `user_algo` API.

```auto
register_algo(algo_wasm_blob) -> code_hash
use_algo(code_hash, [...algo_input]) -> algo_output
```

They are defined as follows:

```python
def register_algo(algo_wasm_blob):
    code_hash = sha3(algo_wasm_blob)
    cached_algos[code_hash] = algo_wasm_blob
    return code_hash
```

```python
def use_algo(code_hash, [...input]):
    wasm_blob = cached_algos[code_hash]
    derived_key = sha3(private_key, code_hash)
    output = ewasm_engine(wasm_blob, [derived_key, ...input])
    return output
```

This API allows implementing new signature schemes, but also more complex protocols involving

A well designed API also allows adding other primitives like symmetric encryption/decryption, public key encryption, diffie-helman, off-the-record messaging, etc.

In particular it allows implementing

If the algorithm needs random numbers, it can use `hash(derived_key, input_nonce)` with a DApp supplied nonce in input.

## Rationale

**User supplied crypto.** A DApp is allowed to supply it’s own algorithms. This is the most flexible approach as wallet developers are not involved in adding new cryptographic methods. An alternative would be to have wallet maintainers approve a set of algorithms, much like precompiles in Ethereum.

**Key derivation.** Especially when arbitrary code is involved, it should not be possible to output any information on the private key. In the proposed API, the worst that could happen is that the `derived_key` is leaked (i.e. when the `algo_wasm_blob` implements the identity function). This does not compromise the private key or the derived keys of other algorithms.

**Choice of WebAssembly.** Nodes will have eWASM implementations available already to support eWASM precompiles which can be re-used here. Browser integrated wallets like Metamask/Brave/Opera have WebAssembly available through the host browser.

## Questions

**Q1.** How hard is it for native/mobile wallets to process eWASM?

**Q2.** Are there attack vectors for browser integrated wallets to run untrusted WebAssembly? Most of this would be covered by random webpages using WebAssembly, so the attacks would have to come from the integration with extension.

## Replies

**wighawag** (2019-01-30):

Interesting proposal!

A question that comes to mind is how in practise will this be dealt in term of UX.

Is the reason behind splitting registration and call an optimization perspective or do you think such registration require user confirmation, hence the need to separate the two.

If the latter, how do you think wallet will explain to the user what it means? Also do you expect wallet to save such registration across devices or will they require user to approve again when switching device posing a UX annoyance?

If the former would we not run the risk of dapps implementing broken algo in purpose and wait for user putting enough funds in their application to screw them up?

Similarly how do you think wallet will be able to provide meaningful UX when an algo call is requested if every algo can have very different meanings.

While I understand the wish to bypass the EIP process that I feel is quite slow too and might itself lead to api fragmentation as seen in the so called browser war of the old web. The process when complete allow wallets to provide a meaningfully UX to the users by being able to display the meaning of each operations to the users and guarantee the security of it.

You mentioned the use of “precompiled” algo though and this could well be a middle ground where the EIP process could be sped up by simply needing to agree to a specific algo implementation and its meaning. In this case the proposal here would be the base on which further algo EIP are built.

Of course we could also have both options available where non “precompiled” algo would require pre-registration and are displayed as unknown algo while the EIP process in in progress to be accepted. This would lead to the issue mentioned above for these cases though.

---

**pedrouid** (2019-01-30):

Super interesting. I think that we definitely more crypto algorithms in Ethereum like EIP-1024, however I would be very skeptical to have Dapp-provided algorithms run on the Wallet side.

A user will most definitely try 1000s of Dapps but it will likely only use 1 or 2 Wallets. The user will trust the Wallet software to securely manage and store its private keys. I think it’s crucial that Wallets handle its own crypto always. It’s up to the Wallet providers to keep it up-to-date with the latest standards.

Thus I would suggest that we keep adding new crypto algorithms as new JSON RPC methods like EIP-1024. What we could standardize instead is how the Dapp and the Wallet communicate to share what algorithms are available.

---

**Recmo** (2019-01-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> Is the reason behind splitting registration and call an optimization perspective or do you think such registration require user confirmation, hence the need to separate the two.

Optimization, I expect these WASM blobs to be up to several tens of kilobytes, so it may make sense not to pass them along for each usage API call.

The wallet should not be forced to store contracts indefinitely, so the DApp would need to re-register them when the `use_algo` fails with `ERROR_UNKNOWN_HASH`. User Acceptance is a separate issue.

I’m starting to think it is better to just pass them with each request, tens of kB is not that large for a request.

Another alternative is to pass a URL to the WASM blob instead, but this has its own set of security considerations.

---

**Recmo** (2019-01-31):

[@wighawag](/u/wighawag) UX is something I have not looked into yet for this proposal. I first want to make sure the API would actually be able to solve the class of problems in a cryptographically secure way before addressing the UX concerns. But let me go into your concerns:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> If the former would we not run the risk of dapps implementing broken algo in purpose and wait for user putting enough funds in their application to screw them up?

This is possible, if users put funds in a malicious contract they run the risk of loosing them. Nothing really changes here. Contracts with backdoors, webapps with backdoors, signing algos with back doors. Same thing. Don’t put money in DApps you don’t trust. Demand audits.

The important thing is that a mallicious DApp can not affect a benevolent DApps. If you submit a backdoored version of a known algo, the `code_hash` will differ and you will get a different `derived_key`. You might be able to steal this key, but it won’t be the key that is used for the non-backdoored algo.

Security problems in a particular wasm blob are always contained to that specific wasm blob.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> Similarly how do you think wallet will be able to provide meaningful UX when an algo call is requested if every algo can have very different meanings.

This is the same problem as with signing messages, which can also mean anything to any contract. I partially addressed that with EIP-712. Something similar works here, the `derivation_key` is used as a domain separator.

Fully addressing this requires some way to trustlessly explain users what a particular operation means, which seams nearly impossible. This is no better or worse from the problems with the current signing UX. Signing messages can also have very different meanings.

You could then say: “…but at least you know your are signing something! With this you don’t know if you are signing, decrypting or deity-knows-what!”.

True. There is a bit more explaining to do on the end of the DApp on what is currently happening. This explaining can be EIP712 style domain-separated-in in a secure way.

For example, let’s say we require the WebAssembly blob to also implement `explain() -> string` and `name() -> string` etc.

Consider a benevolent blob `A`. The wallet can query it all the context it needs to explain the user what is going on.

Now consider a malicious blob `B` that pretends it is `A`. Let say it returns the same context strings. To the user it could look like the user is about to do `A`, but really it is doing `B`. While very confusing, this has no effect on the security of `A` because `derivation_key` is incompatible (it can only be the same if `B == A`, but then there can be no attack because `A` is benevolent).

---

**Recmo** (2019-01-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> You mentioned the use of “precompiled” algo though and this could well be a middle ground where the EIP process could be sped up by simply needing to agree to a specific algo implementation and its meaning. In this case the proposal here would be the base on which further algo EIP are built.

There are different gradations we can apply here:

A. Require each new algo to be formally approved by EIP (whatever that means).

B. Let wallet developers decide which algos they want to whitelist.

C. Require wallets to accept all algos.

I feel C might be a bit much, at least until we have solved to UX issues. My preference is to go for A or B initially. This is the same approach as Ethereum is taking with eWASM contracts: start with hand-picked ewasm precompiles and later allow ewasm contracts.

Whatever we pick, I want to provide wallet developers a simple and standardized mechanism to add new cryptographic methods. In particular I want to avoid wallet developers having to implement the same crypto algos for every wallet, which is time consuming and risky, and also avoid bloating the APIs with an ever growing list of algorithms.

---

**Recmo** (2019-01-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> A user will most definitely try 1000s of Dapps but it will likely only use 1 or 2 Wallets.

Just want to throw another number in here: The user will likely only use 2 to 20 crypto algorithms (Transaction, Eth message signing, encrypt/decrypt, SNARK signing, STARK signing, Off-the-record protocol, etc).

I expect that a dozen crypto algos will cover the needs of these 1000s of DApps.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> The user will trust the Wallet software to securely manage and store its private keys.

I agree with you here! The user should always be able to trust that their wallets keep their private key safe.

The `derived_key` mechanism guarantees that the private key is always safe, no matter what sort of nasty wasm algo the DApp throws at the wallet. eWasm is safe to run in nodes, so it is also safe to run inside the wallet.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> I think it’s crucial that Wallets handle its own crypto always. It’s up to the Wallet providers to keep it up-to-date with the latest standards.

I’m currently leaning to a whitelisting approach from wallets anyway, not so much for security reasons, but for the UX reasons mentioned above. Given that likely only a dozen algos are required, whitelisting is feasible.

If a wallet really wants to, they can always substitute their own implementation of a given webassembly blob. This might make sense for performance, but it should not matter for security.

---

**pedrouid** (2019-01-31):

That makes sense and I agree with you but given that only a dozen algorithms will be necessary, then it should be feasible for Wallets to implement themselves

---

**wighawag** (2019-01-31):

> UX is something I have not looked into yet for this proposal. I first want to make sure the API would actually be able to solve the class of problems in a cryptographically secure way before addressing the UX concerns

I do not want to hijack the purpose of this thread but in my opinion, UX concerns should be at the core of such proposal where user action is required

> Nothing really changes here. Contracts with backdoors, webapps with backdoors, signing algos with back doors. Same thing. Don’t put money in DApps you don’t trust. Demand audits.

Sure except that the point was made in the context of comparison with a normal EIP approval. By bypassing it, we introduce a new vector of attack that was not there before.

> The important thing is that a mallicious DApp can not affect a benevolent DApps. If you submit a backdoored version of a known algo, the  code_hash  will differ and you will get a different  derived_key . You might be able to steal this key, but it won’t be the key that is used for the non-backdoored algo.

I understood the mechanism by which derived_key separate each algorithm but I am concerned with a different issue: If the wallet can’t meaningfully explain to the user what its action will do, a malicious app could make a user sign / decrypt… data meant for another app and this without the user being able to easily know. After all, if the benevolent app can’t relies on the wallet to explain to the user what the action will do, a malicious app can easily request the user to do the same set of action without the user being able to discriminate.

> This is the same problem as with signing messages, which can also mean anything to any contract. I partially addressed that with EIP-712. Something similar works here, the  derivation_key  is used as a domain separator.

Again the issue I am concerned with is different and while EIP712 solve it partially by displaying all the information to the user it is not ideal because the user need to ensure the application is not trying to get them sign something targeted at another context. I have explained this on the EIP712 issues comments and that’s why I have proposed the use of automated origin checks there which remove the need for the users to verify the data on non-audited apps. Nonetheless I agree that what EIP712 does is far better than having nothing to verify meaningfully, which this proposal in its current form is doing.

If the goal is indeed to make `[....input]` into something akin to EIP712, then we can indeed make this proposal safer. As you said, we will have to define a way to explain to the user what the algorithm is supposed to do in some way.

> Fully addressing this requires some way to trustlessly explain users what a particular operation means, which seams nearly impossible. This is no better or worse from the problems with the current signing UX. Signing messages can also have very different meanings.

I think my [proposal on origin checks](https://medium.com/@wighawag/3-proposals-for-making-web3-a-better-experience-974f97765700) allow to solve this issue by proposing that the UI is moved into the app as much as possible. In that context, your proposal could be made a lot safer by protecting users from apps that would try to make them sign/decrypt data meant to be used in a different context.

---

**wighawag** (2019-01-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> Whatever we pick, I want to provide wallet developers a simple and standardized mechanism to add new cryptographic methods. In particular I want to avoid wallet developers having to implement the same crypto algos for every wallet, which is time consuming and risky, and also avoid bloating the APIs with an ever growing list of algorithms.

I think this is a great idea but I am not sure it requires to have such api exposed this way (unless we can solve the UI in a general way).

After all, if we can come up with such wasm blob in the first place, then already wallets do not need to reimplement it since they can execute such blob. After such blob is proposed the rest of the EIP process would be to define the set of input and how we can meaningfully use them for the users.

This does not preclude us to force wallet to having derived_key for such algorithms to remove the risk of having a bad implementation leak the main key.

---

**Recmo** (2019-02-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> That makes sense and I agree with you but given that only a dozen algorithms will be necessary, then it should be feasible for Wallets to implement themselves

I would like to believe this is true. So far, wallets have been able to use off-the-shelve cryptographic libraries (`libsecp256k1`, `libkeccak`). This is also the case for EIP1024 encrypt/decrypt, where something like `NaCl` or `libsodium` can be used.

This no longer holds once dapps start using zero knowledge proofs (SN/TARKs). For the signatures required in these dapps, there are no off-the-shelve libraries that implement them. While some coordination and algorithm re-use among dapps is likely, there will be no support from the mainstream crypto libraries. (Yes, I know this breaks the “don’t roll your own crypto” mantra, but this is why we have expert cryptographers like Starkware working on it.)

This means that the wallet developers need to implement *cryptography from scratch*. For example, for starkdex signatures they need to implement a prime field and an elliptic curve on top of it. These are large non-trivial pieces of security-critical code! General wisdom in crypto-engineering is that you avoid this if you can.

We should not *force* wallet developers to implement cryptography. And this proposal achieves that, while still allowing dapps to use custom cryptography for which no libraries are available.

Now, coming back to you point. A wallet is still *allowed* to implement its own cryptography. Under the proposal this is as simple as recognizing the `code_hash` and instead of executing the wasm, execute your own implementation instead. Reasons for this could be 1) not having a wasm engine 2) increased performance. This makes sense for embedded devices for example, or specialist high throughput nodes.

---

**Recmo** (2019-02-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> I think this is a great idea but I am not sure it requires to have such api exposed this way (unless we can solve the UI in a general way).
> […]
> This does not preclude us to force wallet to having derived_key for such algorithms to remove the risk of having a bad implementation leak the main key.

I would love to narrow the scope of the proposal to only make it easier for wallets to implement new crypto, and leave API and UX issues out of it.

However, if we go down this route it will be harder to extend `derived_key` with further domain separation like EIP712, or extend the wasm blob with methods like `name() -> string` and `description(input) -> string`.

I propose the following:

1. First we reach rough consensus on wasm crypto extensions and derived_key, leaving the API and UX out of the porposal.
2. We try to solve the API and UX generically by extending the proposal.
3. If we can not adequately solve solve these, we give up and revert to 1 and instead solve it in a case-by-case way.

---

**fubuloubu** (2020-05-07):

I would like to continue this conversation, as a developer of an Ethereum-based SNARK system that needs access to Ethereum keys to prove identity, this proposal really speaks to me. Especially in light of issues like Loopring’s recent vulnerability:

https://medium.com/starkware/looprings-frontend-vulnerability-explained-106df1aa17db

---

One change is that I was hoping we could have is to derive the key in a more dependable way so that we can determine the address of the key from the parent account `private_key` from the wasm blob `code_hash`.

So instead of doing this:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> derived_key = sha3(private_key, code_hash)

We could do something akin to BIP32 like this:

```auto
assert int(code_hash)) < SECP256K1_N  // Invalid Key (<2**127 probability)
derived_key = (private_key + int(code_hash)) % SECP256K1_N
```

Which makes it possible to derive an Ethereum address for `derived_key` from just knowing the Public Key for the Ethereum address of the `parent_key` (aka, they have the same relationship). This might be useful from a UX perspective for displaying in the front end, or if a user has multiple UTXO-style accounts to do a summary statistic on them.

This would have the same security properties as doing the hash (inability to derive `derived_key` for another `code_hash`) and gives a valid Secp256k1 secret key to the WASM blob (which could further derive via BIP32, or change to another key type).

---

I am eager to help push this forward, how can I help in further defining this proposal?

---

**Recmo** (2020-05-07):

> ```auto
> derived_key = (private_key + int(code_hash)) % SECP256K1_N
> ```

The problem with this is that it’s now trivial to derive the private key from the `derived_key`, so effectively your private key is exposed to the `algo`. This violates a hard design requirement that user is protected from malicious algos.

I don’t think there is a way to do what you want (have a derived secp256k1 public key be computable from the wallet pubkey) is doable without compromising security. Also note that in the usecase of ZKPs the derived key would not be on the secp256k1 curve, so derivation like this would not be work.

> I am eager to help push this forward, how can I help in further defining this proposal?

I appreciate it! It’s up to the wallets to implement it, and I’m not sure they understand what is being proposed and why it is necessary. What would help push this forward is a nice explainer with UI mockups and a non-cryptographer story on why this is important to us. The Loopring case should really help with the latter.

---

**fubuloubu** (2020-05-07):

We’re actually using ethers.js as a wallet in our app. We could implement this and let it serve as a reference implementation for real wallets to adopt. The usage in the app is super segregated to our use case, so it would be a safe playground to prototype with. I am working on compiling our ZKP for WASM to integrate into our app.

---

**fubuloubu** (2020-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> The problem with this is that it’s now trivial to derive the private key from the derived_key , so effectively your private key is exposed to the algo . This violates a hard design requirement that user is protected from malicious algos.

You’re right, I did this wrong. While in practice using BIP32 would be possible to allow this (although in a different way than I did), in theory there are attacks against it that doesn’t make it worth it. Also, I don’t think I have to even do that to solve this problem.

What I’m really looking for is just a standard way to obtain the corresponding public key for `derived_key`. A good standard here would be to have a 3rd required method (like `name() -> string` and `description(input) -> string`) that returns some sort of bytes-encoded “Identity” data structure the application finds useful (e.g. Ethereum address, public key, or some other address format) that we perhaps call `identity() -> bytes`, which can be used for the purposes I specified.

This wouldn’t violate any of the design requirements you had either (assuming someone doesn’t just return `derived_key`, but that’d be their own issue lol)

---

**Recmo** (2020-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> the corresponding public key

There’s not really a *the* public key in this proposal. One interesting application is an algo that uses the derived key for symmetric encryption. In this case there is only a secret key.

It’s fully up to the algo to decide what to do with the derived key material. If it implements a public-private scheme, then it makes sense for it to return the public key.

Note that a single `algo_block` can implement many functions:

```auto
fancy_curve = register_algo(MY_WASM_BLOB)
pubkey = use_algo(fancy_curve, ["get_public_key"])
signature = use_algo(fancy_curve, ["sign_message", "Hello, World!"])
```

Some metadata like *name* and *description* would be good for UX. One way to implement this is as dedicated inputs to the algo:

```auto
algo_name = use_algo(fancy_curve, ["get_algo_name"])
algo_description = use_algo(fancy_curve, ["get_algo_description"])
```

Doing it this way has the advantage that the metadata is included in the wasm blob and part of the code_hash, solidly binding the metadata and avoiding any confusion attacks.

---

**fubuloubu** (2020-05-07):

Fair. I guess I’ve been wrestling with this a bit in my head, because this essentially creates an entirely new sub-protocol account that is 100% divorced from the main account. You could solve that by just querying both accounts, but the only cryptographic way to prove a link is to have something like an EIP712 signed message of the code hash and public key/identity used in the wasm blob, which is an extra registration step.

Perhaps this is a good thing, that means that privacy of the sub-protocols defined through these wasm blobs is 100% guaranteed by default, and can only be broken by more complex procedures between the wasm and the main account.

---

For the first iteration, can we work together on integrating a simple encrypt/decrypt program, perhaps using https://github.com/str4d/rage/? I’ve worked with that library before, and it should be possible for me to get something together in wasm via Rust pretty quickly. Integrating it into a library like Ethers.js is the part I’m not as comfortable doing.

---

Also, should there be a de-registration function that removes the blob from the cache?

---

**fubuloubu** (2020-05-13):

So, I’ve been trying to work on this specification the past few days. There are a couple things I feel are blocking it from moving forwards:

1. Lack of a standard approach to WASM ABI - in order to define the algo name/description and provide the secret key there needs to be a standard way of interacting with WASM’s memory. There is currently many approaches to this, but none have been standardized.
2. Lack of WASM program encoding standards - there are several ways of encoding WASM programs, memory allocation algorithms, etc. For designing WASM programs under multiple languages/frameworks we may end up with inconsistently formatted binaries, which would make it difficult to interoperate on this proposal.
3. Lack of WASM host framework standards - there are several frameworks for executing WASM code under different host languages (Wasmer, wasmtime, wasm-bindgen, etc.) which take different approaches to (1) and (2). Similarly to (2), we want these frameworks to produce binaries that are interoperable with the other frameworks. This standardization has largely not happened yet.

For now, I will continue prototyping with `wasm-bindgen` for my own purposes (a port of the `age` encryption library), but I don’t feel it is possible to create a standard around WASM yet in this fashion until those problems are better solved. I’m open to alternative opinions, as well as revisiting this standard at a later date when these issues are solved.

---

**GANGA** (2025-07-25):

In my wallet if I want to add attribute based encryption can you tell how to proceed.


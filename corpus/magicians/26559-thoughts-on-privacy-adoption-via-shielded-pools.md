---
source: magicians
topic_id: 26559
title: Thoughts on Privacy Adoption via Shielded Pools
author: DamianStraszak
date: "2025-11-13"
category: Uncategorized
tags: [evm, wallet, zkp, privacy]
url: https://ethereum-magicians.org/t/thoughts-on-privacy-adoption-via-shielded-pools/26559
views: 238
likes: 2
posts_count: 2
---

# Thoughts on Privacy Adoption via Shielded Pools

This write-up aims to summarize the current state of Shielded Pool adoption in the EVM ecosystem, identify the main technical factors behind its slow uptake, and propose directions for improvement.

When we say “Shielded Pools” (or “SPs” for short), we refer to all protocols similar to ZCash that use zero-knowledge proofs (zk-SNARKs) to enable anonymous transfers through notes, Merkle trees, nullifiers, and related mechanisms. This includes projects such as ZCash, Tornado Cash, Privacy Pools, Railgun, Blanksquare, and many others. While there are differences among these protocols, they share the same core idea, making them technically similar and subject to the same set of challenges and limitations.

The focus of this article is the existing EVM ecosystem, particularly Ethereum itself. In other words, we are concerned with “adding privacy on top of Ethereum” rather than “building a new Ethereum with privacy.” As is often the case, the latter path is technically easier since it avoids legacy compatibility and existing tooling constraints, but the former is the one that we aim at solving.  “We do it not because it is easy, but because it is hard.” Consequently, the model protocols discussed here are Tornado, Railgun, Privacy Pools, and Blanksquare, as they operate as standard EVM smart contracts, unlike ZCash, Aztec, or Miden, which are standalone blockchains.

## Background on Shielded Pools

Consider a generic shielded pool. Each user of the pool has their own `SPK` (Shielding Private Key), which is the cryptographic key granting control over their funds within the pool. It’s important to note that, for technical reasons (specifically, the SNARK-friendliness of the cryptography used), the `SPK` is not a standard digital signature key like a secp256k1 key for ECDSA or an ed25519 key. Instead, these are what might be called “exotic” cryptographic keys. For example:

- In Blanksquare, the SPK is an element of the scalar field of the BN254 G1 group.
- In ZCash, the SPK is an element of the scalar field of the JubJub elliptic curve.
- In Railgun, the SPK is an element of the scalar field of the BabyJubJub elliptic curve.

As we’ll explain below, this is, in a sense, the root cause of the difficulties in integrating shielded pools into the existing EVM wallet ecosystem. Simply put, current wallets do not support such keys, and there is no standard or interface for securely generating or using them. Moreover, these keys are fundamentally incompatible with the standard ECDSA (secp256k1) signing algorithm used throughout the EVM ecosystem.

### Making Transactions in Shielded Pools

To make a transaction in a shielded pool, the user performs the following steps:

- Run a procedure proof = gen_proof(SPK, aux1), where aux1 represents inputs that depend on the specific operation being performed and may include additional cryptographic data. The gen_proof function generates a zero-knowledge proof (specifically, a zk-SNARK) that certifies the user’s right to perform a given operation.
- Send a transaction tx(proof, aux2), where aux2 contains other auxiliary inputs. Depending on the protocol and operation type, this transaction might be submitted through an external relayer (to prevent linking the operation to the sender’s address). We omit such details here, as they’re not central to this discussion.

Typically, the `SPK` serves as the root key in a hierarchy of derived keys with different roles: viewing the private state, preparing auxiliary data, or actually spending funds. For simplicity, we’ll treat all of these as a single key.

The takeaway is that using any SP protocol requires one to (1) generate, (2) securely store, and (3) use for proof generation a non-standard cryptographic key (`SPK`).

### Why Are the Keys for Shielding Exotic?

The reason is technical: shielded pools rely on zk-SNARKs to enable privacy. A user must prove, in zero knowledge, that they have the right to spend specific coins. Expressing secp256k1-ECDSA access rights within a zk-SNARK-compatible framework (details omitted here) requires extremely large arithmetic circuits — with millions of gates. Such circuit sizes make the `gen_proof` step very slow; generating an ECDSA-based proof would take on the order of 10 minutes, which is far too long for a usable experience. In contrast, using cryptography that’s designed to be SNARK-friendly allows for massive efficiency gains, enabling `gen_proof` to run in just a few seconds.

Beyond proof-generation efficiency, another major constraint for shielded pools on the EVM is the gas cost of on-chain proof verification. Verifying a Groth16 proof costs roughly 0.5 million gas today, while verifying a Halo2 (KZG Plonk) proof with a small circuit costs around 1 million gas. Other proof systems produce proofs too large to verify on-chain directly. This creates complications: to fit within gas limits, one must wrap the proof into a Groth16 proof, but (1) generating that wrapping proof is computationally expensive, and (2) the original proof often isn’t zero-knowledge, making it unsafe to delegate wrapping to a third party. An alternative to verifying proofs directly on-chain is to offload the process to specialized providers like **Aligned Layer**, which handle proof verification off-chain. This approach can significantly reduce gas costs and improve scalability, but it comes with new trust assumptions.

These claims may sound overly pessimistic to anyone following [ethproofs.org](https://ethproofs.org/) which shows steady progress in proving efficiency. The progress is indeed real, but it primarily benefits server-side proving (for scaling Ethereum with large GPU clusters), not client-side proving, which is what privacy applications require. These optimizations are specifically aimed at proving circuits consisting of long sequences of VM instructions (such as RISC-V). Many involve sophisticated lookups and batching techniques which do not play well with small circuits. Moreover, zkVMs often employ small fields and FRI-based polynomial commitments, which result in large proofs, and potentially costly verification. All in all, these techniques do not apply well for relatively small circuits, to be proved on user devices with low memory and compute capabilities.

It’s worth emphasizing that, aside from efficiency, there’s no fundamental obstacle to using standard cryptography to express spending rights in shielded pools. It’s reasonable to believe that in 10-15 years, this efficiency gap may disappear. However, since the past five years have seen little improvement in client-side proving (most gains were on the server side), it would be overly optimistic to expect this problem to vanish soon. For now, the efficiency bottleneck remains the main reason why shielded pools can’t yet use standard signature schemes.

### Note: Separation of Spending and Viewing Keys

So far, we’ve presented a simplified view of the Shielding Private Key (`SPK`) as a single key used for everything. However, an important trick introduced early on by ZCash allows separating the keys for viewing an account (`View-Key`) and spending its assets (`Spend-Key`).

In this scheme, an operation can look like this:

- signature = gen_signature(Spend-Key, aux1)
- proof = gen_proof(View-Key, signature, aux2)
- tx(proof, aux3)

Here, `gen_signature` is a relatively simple process of producing a Schnorr signature over a non-standard elliptic curve. While the `Spend-Key` remains an exotic cryptographic key, the signing logic itself is quite standard and not computationally intensive.

The main idea is that one can, in theory, delegate the `View-Key` to another party to handle the expensive proving and state synchronization while keeping the `Spend-Key` private. This way, the user maintains custody of their funds but can entrust their privacy operations to a third party.

## Current Struggles with Exotic Keys for Shielding

### User Interfaces for Shielded Pools

Let’s look at the technical challenges of handling shielding keys (`SPK`) across different types of user interfaces:

1. DApps (WebApps, Browser-based interfaces)

 Generating keys: There are two ways to generate keys for users:

Generate them from scratch and have the user save yet another seed phrase.
2. Or generate the key deterministically from their connected EVM wallet.
3. Signatures are not designed to serve as randomness sources, and some cryptographers argue that this method is not provably secure.
4. The reliance on RFC6979 across most wallets is merely a lucky coincidence: it’s not enforced by standards and is not verifiable on-chain. Any wallet could deviate from it, potentially locking users out of their funds if a privacy protocol depends on this behavior. It’s also unclear whether all popular wallets even follow this standard.
5. Non-EOA addresses are unsupported, which is a big issue now that smart wallets are finally seeing adoption. Many users will lose access to this option over time.
6. This approach isn’t very safe, since users tend to be much less cautious about signing messages than transactions. Malicious dApps can more easily trick users into revealing sensitive data or compromising their funds.

**Storing keys:** Browser storage is neither safe nor reliable for private keys. We can either ask users to store another seed phrase or hope that deterministic derivation works - but as noted above, it’s unreliable. Either way, the keys still have to exist somewhere in browser memory or storage, which is inherently less secure than extension-based wallets.

**Using keys:** Keys are used to generate proofs, typically by running WASM code directly in the browser.

**Software Wallets (Browser Extensions, Mobile Wallets, Desktop Wallets)**

The situation here is much better than in DApps. Keys can simply be derived from the user’s existing seed phrase, and all established key security practices (encryption, password protection, etc.) extend naturally to these new key types. Standards like BIP32/39/44 could, in principle, be extended to support shielded keys as well.

The real issues are:

1. These standards don’t yet exist.
2. Every shielded pool protocol uses slightly different key types, state recovery tricks, and transaction formats.

This creates a problem: integrating a shielded pool directly into a wallet is a significant investment - not just due to the complexity but also because of the UX work needed to make it seamless. Once a wallet does this, it implicitly commits to maintaining long-term support for that specific shielded pool protocol. That’s a risky bet.

**Hardware Wallets**

As of 2025 - nine years after ZCash’s launch - experimental shielded ZEC support has only just been added to a few Ledger models. The core issue is that hardware implementations only make sense for software that’s extremely stable. ZK-SNARK cryptography and shielded pools, however, are anything but stable. They evolve monthly with major improvements and design changes. Reliable hardware wallet support for shielded pools probably won’t arrive until the field further matures.

**Multisigs**

Currently, no shielded pool supports multisig in production. However, we’ll discuss some potential approaches later in this article.

### Integrating Shielded Pools into dApps

Imagine you’re leading a blockchain project, and your main user-facing interface is a dApp (a browser web app where users connect their EVM wallets). This is how most projects operate today. Suppose you’re satisfied with your current product and want to introduce privacy through shielded pools. How should you go about it?

There’s no universal recipe for adding a shielded-pool layer to a protocol that was originally built without confidentiality or anonymity. That doesn’t mean it’s inherently difficult, in fact, it can be relatively straightforward. Many protocols, especially in DeFi, primarily handle fungible tokens. These tokens can often sit and mix within a shielded pool instead of remaining directly in user accounts. This alone can provide meaningful anonymity by breaking the link between actions within the protocol and the users performing them. Completely hiding actions, meaning *what* is happening and *with what amounts*, is a much harder problem that typically requires deeper changes to the protocol’s design. So let’s assume we’re going for the simplest integration: moving the ERC20 tokens that the dApp handles into a shielded pool.

To achieve this, you might use an SDK provided by a shielded-pool protocol. But very quickly, you’ll run into a major obstacle: since the `SPK` is an exotic key, your dApp now has to manage this user key directly. Normally, handling keys and signing is the wallet’s job: it’s secure, standardized, and familiar. But now, your dApp effectively becomes a wallet itself, and worse, one without reliable persistent storage. You end up facing the same key-management problems discussed earlier for browser-based shielding interfaces.

In my view, this is currently the biggest *practical* obstacle to shielded pool adoption in the EVM ecosystem. The layer where innovation usually happens first: dApps, has no good way to integrate privacy because it immediately runs into key management challenges.

## Way Forward

In the long term, solving this problem depends on the stabilization of shielded-pool technology and the emergence of mature standards. Once those standards exist, wallets, both software and hardware, will adopt the required cryptography, making integrations straightforward.

The real question, though, is *when* that will happen. If I had to guess, even ten years from now might be optimistic. To get there, we’ll need bold wallet teams to take the lead by integrating shielded-pool support natively, serving as early showcases and experimentation grounds that help shape future standards.

In the meantime, there’s meaningful progress to be made at the dApp layer too. One possible idea is presented in [this ethresearch post by Adam Gągol](https://ethresear.ch/t/smart-contract-or-eoa-spend-authority-for-private-accounts/23422). I recommend reading it, but here’s the short version of what it proposes:

- A mechanism for delegating control over a shielded account to a regular EVM address. This address can submit on-chain (or off-chain, in some versions) authorizations for specific operations within the shielded pool.
- These authorizations are then “proved” in zk using a separate, non-standard proving_key. This key is similar in spirit to a View-Key from the Spending/Viewing separation: it can access account details but cannot move funds. This means it can safely be delegated to a trusted third party, stored in a TEE, or backed up with less concern, since leaking it compromises only privacy, not funds.
- The tradeoff is that this approach introduces an on-chain trace linked to a public address, which reduces anonymity somewhat.

This kind of delegation: “allowing an EVM address to control shielded funds” could significantly boost adoption. Once this pattern exists, integrating shielded pools into dApps becomes much easier: key management stops being the main blocker, since the `proving_key` is no longer as security-sensitive and can even be offloaded to a third party. It would be valuable to explore alternative designs that follow a similar direction.

The motivating example for such a delegation mechanism is **multisig wallets**. These wallets (like SAFE) are typically on-chain smart contracts controlled by an `m-of-n` threshold of signers. Making such a wallet’s funds private through shielded pools is difficult because it would require replicating the `m-of-n` structure within the shielded pool. While there are theoretical ways to do that, they all share a problem: each signer would need to manage at least one new key: an exotic `SPK` or a share of it (in the case of threshold signatures). But how are signers supposed to manage such keys if they’re using the wallet through a dApp? This question underlies nearly all real-world challenges around shielded-pool adoption. It’s the same problem, just resurfacing for different use-cases.

## Feedback

I’d love to hear any feedback or thoughts on this article: especially around how we, as a community, can make shielded-pool adoption more practical in the short and medium term. The biggest obstacles right now aren’t purely cryptographic; they’re about usability, standards, and developer experience. If you’re working on wallets, infrastructure, or privacy protocols, I’m particularly interested in hearing your perspective on what would make integration easier, or what kind of abstractions or APIs could bridge the current gaps.

If you have ideas, criticisms, or even just questions that challenge some of the assumptions here, I’d really appreciate hearing them. Please respond either in this thread, or reach out on X: [@damian_straszak](https://x.com/damian_straszak).

## Replies

**okrame** (2025-12-05):

Thanks for this enjoyable exposition! I agree on the reasons for calling the whole shielding business exotic. Also I love when efforts are made to move it to milder climates.

On the crypto efficiency side of things: I’m optimistic that the onchain verification cost will go down eventually as optimizations are becoming possibile (e.g see zkVerify with its modular precompiles).

As for provers, I can only guess why client-side proving has not seen the tremendous improvements we all hoped for (except maybe for the recent Stwo from StarkWare?), but clearly large compute economies have an edge in development.

When you talked about dApp integration, I think “transition” mindset for building solutions like the one you propose is always the most sensible and aligned with the historical technological progress. Still, I have doubts about relying on a third party to safeguard my financial privacy.

The main tradeoff seems to be that you relax some of the privacy and availability guarantees. The holder of the “proving_key”, the delegatee, has to be treated as at least honest-but-curious, meaning the delegator’s history is no longer completely private (even with aggressive key rotation this mainly limits the damage if the key gets compromised later, no?).

Okay, what if the delegatee and delegator are the same entity? Then of course this is no longer an issue, and the dApp still keeps the advantage of not having to manage key material, it just asks for an eip712 signature. But then you asked, how to manage the proving/view key? I guess you implied two possible ways, each with different implications for how much the dApp has to act like a wallet:

- Store the proving/ view key in the device’s secure enclave via webauthn. This improves how the key is stored but now the sdk has to handle webauthn setup, recovery and all the ux flows, which may end up being quite dapp-specific again.
- Use wallet plugins or sandboxed environments like metamask snaps. This is not a new wallet derivation standard (and as you pointed out, who knows when and if that will happen), but it does at least push everything into the wallet layer so the dapp doesn’t manage key material directly. The tradeoff is ecosystem fragmentation and having to wait for wallet support, since not all wallets expose these kinds of extension environments.

Regardless, in either case, we bring back the old pain point of limited compute for proving.

One possible way to mitigate this is to keep the proving/view key local and use it only to derive the witness (which includes the note secrets), then encrypt the statement and witness and send those ciphertexts to a proving service. This paper (https ://eprint.iacr.org/2024/1684) shows that the prover can, in principle, be performed homomorphically over such ciphertexts, and that this is practical (at least based on their model) for computations roughly up to the scale of typical shielded pool circuits. The client would “only” need to i) derive and encrypt once, ii) decrypt the resulting proof (if needed, generate a short proof-of-decryption), and then iii) attach the proof with public inputs to the spend authorization tx, while the untrusted server does all of the proving work without seeing the client’s plaintext. Even if this works, though, it mainly improves the client ux around proving but makes things worse w.r.t key management since the user now has to manage also the keypair for homomorphic encryption.

A slightly different approach would be to run a co-snark protocol at the cost of adding some extra network assumptions. The nice thing is that there are already usable tools (https ://github.com/TaceoLabs/co-snarks) in this direction. In this model, the prover runs as an MPC between the user and a committee of provers. Then an sdk (embedded in the wallet client or dapp frontend) keeps the proving/view key local, builds the extended witness, secret shares it across the committee, and then collects the normal proof as output. This does add integration work but with your keys separation it means the dapp never has to hold the control key and no single proving service ever sees the full witness.

So, in short, I believe there might soon be ways for a dapp to behave a bit like a wallet purely for orchestrating proof generation, yet with far less responsibility, so long as the exotic key and sensitive state remain confined to secure local environments.


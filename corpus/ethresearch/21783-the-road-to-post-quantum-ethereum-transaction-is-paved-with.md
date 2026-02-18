---
source: ethresearch
topic_id: 21783
title: The road to Post-Quantum Ethereum transaction is paved with Account Abstraction (AA)
author: asanso
date: "2025-02-18"
category: Cryptography
tags: []
url: https://ethresear.ch/t/the-road-to-post-quantum-ethereum-transaction-is-paved-with-account-abstraction-aa/21783
views: 2392
likes: 34
posts_count: 20
---

# The road to Post-Quantum Ethereum transaction is paved with Account Abstraction (AA)

*Thanks to Nicolas Bacca, Vitalik Buterin, Nicolas Consigny, Renaud Dubois, Simon Masson, Dror Tirosh,Yoav Weiss and Zhenfei Zhang for fruitfull discussions.*

**This is Part 3 of our series exploring the feasibility of implementing a post-quantum signature scheme for Ethereum**. In [Part 1](https://ethresear.ch/t/so-you-wanna-post-quantum-ethereum-transaction-signature/21291), we discussed the fundamental challenges and considerations involved in transitioning Ethereum to a quantum-resistant future. In [Part 2](https://ethresear.ch/t/falcon-as-an-ethereum-transaction-signature-the-good-the-bad-and-the-gnarly/21512), we took a deep dive into Falcon, analyzing its strengths, weaknesses, and the practical hurdles of integrating it into Ethereum’s transaction framework. In this installment, we build on that foundation by exploring how **account abstraction (AA) can be leveraged to integrate Falcon into Ethereum**. We’ll examine the architectural changes required, the benefits of using AA for post-quantum security, and the potential challenges in making this approach viable.

## Did you say ERC-4337?

When discussing **account abstraction (AA)**, the natural conclusion is to think about [ERC-4337](https://www.erc4337.io/), as it is currently the most prominent and widely adopted approach to enabling AA on Ethereum. ERC-4337 provides a way to implement smart contract wallets without requiring changes to the Ethereum protocol, making it a strong candidate for integrating post-quantum signature schemes like Falcon.

In particular, we can take inspiration from the [SimpleWallet](https://github.com/asanso/account-abstraction/blob/95d36a70162e48612dd25e2e28f77a95cf627e7f/contracts/samples/SimpleAccount.sol) smart contract or from smart contracts leveraging [RIP-7212](https://github.com/ethereum/RIPs/blob/eedf04cdeeb4feb141a271cede23260eb66d03b8/RIPS/rip-7212.md) to explore how Falcon can be efficiently integrated within the ERC-4337 framework.

### SimpleWallet

The [SimpleWallet](https://github.com/asanso/account-abstraction/blob/95d36a70162e48612dd25e2e28f77a95cf627e7f/contracts/samples/SimpleAccount.sol) is a smart contract-based wallet designed to implement **Account Abstraction** on Ethereum. Instead of using traditional private keys for transactions, a SimpleWallet smart contract allows for greater flexibility by enabling custom validation logic and potentially supporting new cryptographic signature schemes like **Falcon**. For instance, in the context of **post-quantum Ethereum**, the `SimpleWallet` could be adapted to work with **Falcon signatures**, allowing for more flexible, secure, and future-proof transaction processing. This smart contract approach would allow Ethereum accounts to evolve and support post-quantum cryptography without requiring changes to the underlying Ethereum protocol.

### FalconSimpleWallet

A `FalconSimpleWallet` would be a modified version of `SimpleWallet` that replaces **ECDSA** with **Falcon-based cryptography**. Unlike ECDSA, “plain” Falcon does **not** support **public key recovery** from a signature—meaning that `ecrecover` cannot be used. Instead, a Falcon-based wallet must verify signatures **directly against a stored public key**.

However, as [Renaud Dubois](https://x.com/RenaudDUBOIS10) pointed out, **Section 3.12** of the [Falcon paper](https://falcon-sign.info/) introduces a **key recovery model**. This method allows for public key recovery, but it comes at the cost of **doubling the signature  size**. While this could provide a potential workaround for `ecrecover`-like functionality, the increased key size presents additional considerations for on-chain efficiency.

This difference means that Falcon-based wallets need an explicit mapping of **Ethereum addresses to public keys**, requiring a different approach to authorization. Rather than relying on `ecrecover` to derive the signer’s identity, a `FalconSimpleWallet` would explicitly store and reference public keys for verification.

Additionally, integrating Falcon into the **Ethereum Virtual Machine (EVM)** requires deviating from the **NIST standard implementation**. Falcon relies on **SHAKE** for hashing, but since **SHAKE is not natively supported in the EVM**, we need to use a more **EVM-friendly hash function**, such as **Keccak**. This ensures compatibility and efficiency when verifying Falcon signatures on-chain.

*Kudos to [Zhenfei Zhang](https://x.com/zhenfei_zhang), who contributed a [Keccak256-based PRNG implementation for Falcon](https://github.com/zhenfeizhang/falcon-go/blob/8ae42f4142cdda1fbca4cdca4e850bcb9aee4584/c/keccak_prng.c#L2-L27), further bridging the gap between Falcon and Ethereum’s cryptographic stack.*

### Show Me the Demo!

You can find the demo in [FalconSimpleWallet on GitHub](https://github.com/asanso/account-abstraction). This project showcases a wallet that replaces traditional ECDSA with **Falcon-based verification**, tailored for Ethereum’s evolving security needs.

*A special shout-out to **[ZKNox](https://zknox.eth.limo/)**—their exceptional work on the [Falcon Solidity implementation](https://github.com/ZKNoxHQ/ETHFALCON) has dramatically cut verification costs from **24M gas down to 3.6M gas**. This impressive gas optimization brings post-quantum security a step closer to practical deployment on the blockchain. Kudos to ZKNox for their remarkable contribution!*

### The elephant in the room

While we have successfully transitioned the **smart wallet signature** to be **post-quantum (PQ) resistant**, there remains a critical issue: the **bundler transaction** still relies on the traditional **ECDSA** signature scheme. This means that even though individual user operations (`UserOps`) within the account abstraction framework can use Falcon, the final transaction submitted to the **Ethereum mempool** is still signed with **ECDSA** by the bundler.

To fully remove ECDSA from the transaction pipeline, changes at the **L1 protocol level** will likely be required, specifically via [EIP-7701](https://eips.ethereum.org/EIPS/eip-7701)/[RIP-7560](https://github.com/ethereum/RIPs/blob/eedf04cdeeb4feb141a271cede23260eb66d03b8/RIPS/rip-7560.md).

### (Bonus part) Batching

As mentioned in the **“Gnarly” section** of [Part 2](https://ethresear.ch/t/falcon-as-an-ethereum-transaction-signature-the-good-the-bad-and-the-gnarly/21512), there has been [ongoing research](https://eprint.iacr.org/2024/311) into efficiently aggregating Falcon signatures, including work involving **Labrador**. If this approach proves efficient, we could leverage [EIP-7766](https://eips.ethereum.org/EIPS/eip-7766) (**Signature Aggregation for ERC-4337**) to optimize Falcon signature aggregation within the AA framework—similar to how **BLS signatures** are aggregated in [this VerificationGateway contract](https://github.com/getwax/bls-wallet/blob/7671d78a1b96ceb9010362b09a5f255297c12d9d/contracts/contracts/VerificationGateway.sol#L85).

## No soup (EIP-7702) for you!

As discussed in the context of [EIP-7702](https://github.com/ethereum/EIPs/blob/fa5ceb255acf88747d0483fc72a34a7983c00342/EIPS/eip-7702.md), the proposal might allow turning an account into an **ERC-4337** account and adding **Falcon** support, but it still retains the **ECDSA** key. The problem with **EIP-7702** is that the **ECDSA key remains valid** within this framework, which introduces a potential security risk. Even if the account starts using Falcon after setting the code, the presence of the **ECDSA key** leaves the account exposed. An attacker could potentially recover and misuse the ECDSA key to compromise the account.

This is why **EIP-7702** is problematic from a **quantum-resilience perspective**: it enshrines **ECDSA**, which is vulnerable to quantum attacks. Instead, the focus should be on **native Account Abstraction (AA)**, which removes any reliance on ECDSA and offers a more robust, quantum-resistant approach through smart contract wallets like the **`SimpleWallet`**. solution above.

## Conclusion

In this installment, we’ve explored how **Account Abstraction (AA)** can be leveraged to integrate **Falcon**, a **post-quantum signature scheme**, into Ethereum. By transitioning to a Falcon-based **smart wallet signature**, we can ensure a future-proof, quantum-resistant approach to Ethereum transactions.

While the adoption of Falcon-based wallets within the AA framework is a promising step, the ongoing reliance on **ECDSA** signatures for **bundler transactions** still presents a challenge. Overcoming this requires protocol-level changes, likely through **EIP-7701** or **RIP-7560**, to fully eliminate ECDSA from the transaction pipeline.

Additionally, research into **signature aggregation** for Falcon, as discussed in the **“Gnarly” section** of [Part 2](https://ethresear.ch/t/falcon-as-an-ethereum-transaction-signature-the-good-the-bad-and-the-gnarly/21512), presents an opportunity to further optimize Falcon’s integration in the Ethereum network, particularly with the potential adoption of **EIP-7766** for **ERC-4337**.

However, since we are still using a smart contract for Falcon, which currently costs about **3.7M gas** per transaction, the next logical step is to move toward a **RIP** for Falcon, which would aim to optimize its integration and bring gas costs down for practical, on-chain use.

In conclusion, while we’ve made significant progress in integrating **post-quantum security** into Ethereum, there are still key challenges to address at both the **bundler** and **protocol levels** to ensure a complete transition to a quantum-resistant future.

## Replies

**rdubois-crypto** (2025-02-24):

Looking at key recovery, if the public key is transmitted along the verification (while it is implicit in recover), then the difference between recovery and original scheme is in favor of the recovery version, because a public key (incompressible polynomial, 896 bytes) is replaced by the s2 field of falcon (which can be compressed to 630 bytes) and a hash (32 bytes).

Of course for the current experimentations, we don’t have the implicit, but we could imagine to have this public key hashed in the smart account storage, verified during deployment.

---

**shemnon** (2025-09-11):

There are two EIPs proposing a precompile for the current NIST Falcon variant

https://ethereum-magicians.org/t/eip-7619-falcon-512-precompiled-generic-signature-verifier/18569

https://ethereum-magicians.org/t/eip-7592-falcon-signature-verification-pre-compile/18053

Of the two, EIP-7619 appears to be closest to what AA would need and the most versatile, as it accepts the entire message rather than a pre hashed message (note that Falcon salts it’s messages prior to signing with a signature specific salt). It is the EIP I am attempting to revive for a precompile.

---

**Nomadu27** (2025-10-04):

Hi [@asanso](/u/asanso), thank you for this excellent series exploring post-quantum Ethereum and Falcon integration via account abstraction.

I’m working on a hybrid RNG architecture designed to bridge physical entropy sources, chaotic amplification, and cryptographic extraction (SHAKE/Keccak) compatible with Ethereum’s keccak-based commitments and intended for seeding PQ signatures like Falcon or as randomness for ERC-4337 workflows.

I’ve published a sanitized specification + demo repo (no private parameters) hybrid-chaos-quantum-rng .  I’d be happy to share the full implementation under NDA or collaborate on integrating with your FalconSimpleWallet designs.

Looking forward to feedback and discussion.

Nomadu27

---

**vbuterin** (2025-11-24):

> Bundler ECDSA Envelope

This is exactly why we need something like EIP-7701, ie. AA as a protocol-level feature. We need to de-enshrine ECDSA from the protocol fully.

> sequencing, ordering

BLS-based RANDAO can easily be replaced with hash-based, in fact hash-based was the original proposal. It’s just somewhat less efficient because you need to update the RANDAO value every time there’s a proposal (but that’s fine).

> L2 attestation

We need off-chain proof aggregation to make STARKs truly viable for this. See [here](https://vitalik.eth.limo/general/2022/09/17/layer_3.html#:~:text=The%20strategy%20is) for how it can be implemented.

> MEV relay protocols

I don’t see why this can’t be quantum-resistant? eg. ePBS can easily be made quantum-resistant

So all of these problems have solutions, but yes they do require building out a few important components.

---

**seresistvanandras** (2025-11-24):

> BLS-based RANDAO can easily be replaced with hash-based

The original hash-based RANDAO ([outlined here by V](https://ethresear.ch/t/rng-exploitability-analysis-assuming-pure-randao-based-main-chain/1825))  has exactly the same biasability problems (last-revealer manipulation attacks (aka [selfish mixing](https://ethresear.ch/t/selfish-mixing-and-randao-manipulation/16081)), and [forking attacks](https://eprint.iacr.org/2025/037.pdf)) just like the current BLS-based construction. Swapping out the cryptographic component to a post-quantum secure one does not automatically solve the randomness beacon’s biasability issues. If this is a concern (I’d argue it is quite a concern), then we also need to redesign the beacon protocol itself.

---

**codebyMoh** (2025-11-26):

One aspect that I don’t think is being fully explored in this thread is the **state-transition validity problem under heterogeneous signature environments** once Ethereum begins introducing PQC-capable account types (whether via EIP-7701 or deeper AA enshrinement).

Even if we de-enshrine ECDSA and migrate to a PQC-first AA environment, there’s still a missing analysis for the following:

### 1. Hybrid-Epoch Safety Under Mixed Signature Regimes

During the transition period, block proposers will need to simultaneously validate:

- legacy ECDSA-based transactions
- PQC-based AA wallets (SPHINCS+, Dilithium, Picnic, SLH-DSA, etc.)
- aggregation commitments for PQC-based attestations
- signature-object equivalence proofs to maintain deterministic state root construction

This exposes a *nontrivial state-transition race condition*.

Specifically:

> Ethereum has not yet defined a canonical mechanism for multi-scheme signature admit rules in the transition epoch, which means a quantum adversary could selectively target only the legacy paths and still cause proposer-level reorg leverage.

Even with ePBS + PQC upgrades, this remains unaddressed.

**2. PQC-Friendly State Witness Design Is Not Defined**

PQC signatures (hash-based or lattice-based) have:

- larger public keys
- larger signatures
- higher verification cost variability
- non-unique signature structures

But **Ethereum’s state witness format (Verkle transition)** is not yet adapted for:

- PQ key-object encoding
- deterministic format for PQ signature lists in bundled AA ops
- state witness compaction under PQC objects (since SPHINCS+ can be 8–20 KB per signature)

Meaning:

> Under current designs, PQC transactions will inflate witness proofs in a way that breaks the expected Verkle node size budget, unless the protocol introduces a specialized PQC-witness leaf type.

Probably we should also look at all rely on the recoverable-signature property.

Even Falcon’s Section 3.12 “recoverable mode” requires either:

1. transmitting s₂ + signature hash + deterministic PRNG seed
2. or precommitting the public key hash in contract storage

which **cannot be lifted into consensus without native format standardization**.

---

**seresistvanandras** (2025-11-26):

Yeah, you’re right.

There’s a huge literature on *unbiasable* randomness beacons (VDFs, threshold redesign is part of that literature as you point out). The question is which one would be suitable for Ethereum’s unique setting with very specific latency and efficiency requirements. This is a wide open research engineering question IMHO. Also part of the unbiasable randomness beacon question is that in which setting we want to solve this problem? Dishonest majority? Honest majority? A recent paper shows that if you want to have an unbiased randomness beacon in the dishonest majority setting then the only way to solve this problem is to use VDFs. See [it here](https://eprint.iacr.org/2024/1711.pdf). I don’t know much about pq-secure VDFs…

Not sure how accountability could solve the withholding/selfish mixing manipulation attacks in the current RANDAO design.

1. Offline validators: There are legitimate reasons why a validator did not publish its block. Conversely, a RANDAO manipulator validator could aways say that it just happened to be offline or it was DoS-ed and that’s the reason it did not publish its block and the corresponding RANDAO randomness contribution. From the outside world, these two scenarios are indistinguishable.
2. Impossibility of issuing “manipulation proofs”: Even if you would prove to a smart contract that XYZ did not publish their block, it’s not obvious whether they did it because of manipulating the beacon. Since, the public does not see their hidden, non-published RANDAO contribution(s), the public cannot recompute the beacon state with the hidden RANDAO contribution. See Section 3.4. here, where I explain this better.

---

**seresistvanandras** (2025-11-27):

I pretty much agree with everything what you wrote in your last two comments.

I would frame the two problems (pq-security and beacon unbiasability) as orthogonal problems. Pq-security is a theoretical-cryptographic problem of the constituent cryptographic algorithms (signatures, randomness contributions, commitments, (verifiable) random functions, etc.), while unbiasability is a protocol-level problem that already assumes the above-mentioned pre- or post-quantum secure building blocks.

***PQ-security*** of the beacon is easy to solve as Vitalik pointed out above by swapping out BLS-signatures as randomness contributions to preimages in a validator-generated hash-chain. This is likely even faster than the pre-quantum BLS-based RANDAO construction!

***Unbiasability*** is a completely different beast. There are already proposals to try to minimize the biasability of the RANDAO. See, e.g., [this great ethresear.ch post](https://ethresear.ch/t/unpredictable-randao/22666).

With regards to a lightweight accountability layer. Honestly, I don’t see much value in it.

Pragmatically, one would correct the design of Ethereum’s distributed randomness beacon once and for all. I don’t see much value in incremental patchwork-style approaches on this matter. These are my two arguments to back this up:

1. Dual-signed commitments: the addition of dual-commitments (pre- and post-quantum) do not solve any of the biasability issues (selfish mixing, forking attacks) but make the beacon less space- and time-efficient thanks to the increased cryptographic workload.
2. “Proving” beacon manipulation: again, this is not a pq-security issue. As I argued above and also in our paper, forking attacks are provable and evident for the public. While, selfish mixing cannot be made accountable, as there are missing information on-chain, i.e., the missed RANDAO  randomness contributions that would allow us recomputing the necessary counterfactual RANDAO states that only the manipulative adversary sees given her hidden randomness contributions. Thus, selfish mixing cannot be made accountable in a publicly verifiable manner (unless all the RANDAO contributions are visible to everyone which is not the case in selfish mixing by definition).

---

**seresistvanandras** (2025-11-27):

Sure! Such a lightweight beacon may make sense for L2s, rollups, etc. It’s a free market, right? ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=14) Everybody is welcome to deploy their own randomness beacon that fits their adversarial model, latency, efficiency, and security requirements.

But at the end of the day, mostly for composability and interoperability, I’d assume that even L2s would want to have access to a global, unbiasable randomness beacon on the L1 for certain applications. (Obviously the L1 must have a source of randomness for selecting the block proposers from the validator set in a fair manner. The L1 needs randomness, as there is no deterministic and secure decentralized consensus protocol (even in synchrony) as was shown by [Lewis-Pye and Roughgarden](https://arxiv.org/pdf/2304.14701). )

---

**paulangusbark** (2025-12-02):

I wish I had found this thread sooner, would have saved me so much time lol.  I wrote a solidity contract that does falcon-1024 verification and I even had a transfer on mainnet; transaction id is 0x22d89bb12e9f50b1c8b890733b5eda50f1be2ebcd8e4c598ba5bdbea73cbd520 (was not optimized for AA gas since it was a quick POC).  My original contract used 40m gas but I got it down to just below 10m gas (but it includes signature extraction).

Why did you store the public key as an uint256 array and not an uint16 array?  The storage costs are dramatically reduced.

I also went with a keccak variant but mine iterates keccak functions with the userOpHash, a domain, and the salt.  I might look to replace what I have with your implementation though, I do know there’s room for improvement on what I’ve done.

One thing I did to reduce gas was do the NTT transformation on the public key when they are first loaded instead of everytime a transaction is verified; that might reduce your gas by about half a million.

I was going to wait until about April before I made my github public but maybe I’ll just do it sooner.  It would be nice to compare notes.

---

**seresistvanandras** (2025-12-03):

Congrats [@paulangusbark](/u/paulangusbark)! Please both of you, do share those contracts! It’d be nice to standardize in the long run those verification contracts similarly as the community uses somewhat standardized OpenZeppelin contract snippets for many standard tasks. Presumably PQ signature verification will be just as standard as an ERC20 interface.

---

**rdubois-crypto** (2025-12-03):

Congrats,

It is great to have other implementations (targeting a different security level).

We are very interested by the contracts as well (mainly regarding the core NTT operations optimizations).

It might have been unnoticed, falcon512 and Dilithium are available here since a few months.

FALCON verification takes as input a precomputed NTT representation of the public key as mentionned above. FALCON keys are packed in uint256, dilithium keys are stored in an external contract.

The NIST KATS are successfully passed, providing confidence on the core part of the algorithm.


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [github.com](https://github.com/ZKNoxHQ/ETHDILITHIUM/tree/main)





###



[main](https://github.com/ZKNoxHQ/ETHDILITHIUM/tree/main)



Dilithium Signature for Ethereum. Contribute to ZKNoxHQ/ETHDILITHIUM development by creating an account on GitHub.











      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [github.com](https://github.com/ZKNoxHQ/ETHFALCON/tree/main)





###



[main](https://github.com/ZKNoxHQ/ETHFALCON/tree/main)



Study and implementation for the ETHEREUM ecosystem - ZKNoxHQ/ETHFALCON










For both keccak256 based version and fully nist compliant versions are provided, along with signers (and also a hardware signer app for Dilithium44).The 128 bits level of security is picked, as it is the common target for Ethereum.

Gas cost for FALCON512 using keccak256 is 2M, 6.6M for Dilithium.

This can be used to experiment starting today, until precompiles are adopted.

The EIP-8052 (DRAFT) diverges from previous proposal by

- spliting the FALCON computations in two part, allowing a more zk-friendly to be adopted for the hash2Point part of the signature, having in mind the ZK endgame.
- take as input the NTT representation of the PK

https://ethereum-magicians.org/t/eip-8052-precompile-for-falcon-support/25860

This separation is not possible for DILITHIUM, so EIP-8051 just stick to the standard.

https://ethereum-magicians.org/t/eip-8051-ml-dsa-verification/25857

---

**paulangusbark** (2025-12-03):

I’ve created a discord channel with instructions at discord.gg/PUFcQezy

The signature is the salt followed by the signature encoded as bytes mod q (I didn’t use the encoder/decoder from the falcon implementation except for loading the public key); so 2068 bytes (no header).

A domain is set on wallet creation and is immutable; the value is used in the message hashing function.  Admittedly, I asked ChatGPT to write me a function using just the 32 byte input and was never able to make anything better; I suspect what I have is loosely based on your code except I added a domain value.  I also calculate the point values as I iterate through the last iNTT transformation to reduce the number of loops.

To save on gas, I calculate half of the norm with the submitted signature, then convert that memory allotment to the other half of the signature and calculate the second half of the norm.  I also used the unchecked feature during the NTT conversions.

I’ll publish it soon.  My repository has other contracts I’m not ready to share but I’ll just weed out the relevant parts into a different repository and make that public.

If you are in London, I’ll be at the Ethereum London event at the Encode Club tomorrow.

---

**paulangusbark** (2025-12-04):

I’ve published it to [GitHub - Cointrol-Limited/QuantumAccount: An implementation of an ERC4337 wallet that uses FIPS 206 (falcon-1024) for signature verification](http://github.com/Cointrol-Limited/QuantumAccount)

---

**paulangusbark** (2025-12-05):

To clarify, I’m not formally trained in this space.  I’m best described as a hobbyist mathematician.

As a slight caveat, I wrote a contract seven years ago that can arguably be used to measure randomness.  The address is 0x16FA8DF7F16f9E41B7C5522Cc12a22053A2a776F

It assumes a Gaussian relationship with paired dice rolls when compared with their histogram typical spread.  I did it on how often seven was rolled but it can easily be applied to rolls less than five, since that probability is arguably equivalent in probability just like rolls greater than nine. And the die doesn’t need six sides.

Technically, it cheats on the value of e, but it can be rewritten as a ratio of e and pi.  It is a twist on Buffon’s experiment.

---

**paulangusbark** (2025-12-05):

And to expand upon that.  That contract measured the frequency of rolling 7 versus anything else.  It has limitations but I had every roll be an event so they could be queried after the fact.  There are thousands of rolls there as a initial data set.  You can take a sample value and mod 12 it (assuming it’s 2 bytes) and use a second value randomly to verify.

---

**rdubois-crypto** (2025-12-11):

Well for the IPQVerifier, we planned to follow the openZeppelin ERC7913 IVerifier, parameters verification shall be performed  internally.

Concerning the Keccak hashing, a PRNG was designed by Zhenfei (FALCON co-author) during our collaboration with EF. It is roughly a CTR-mode build with keccak as central permutation.

If you need SHAKE, it is available in our repo, it has an expensive cost, which will vanish once the EIP is adopted.

---

**SirSpudlington** (2026-01-03):

I just found this thread so I thought to give my two cents (at least regarding the EL side of things).

This is more about cryptographic flexibility than specifics of any particular algorithm.

The idea that AA is the future for PQ verification is a good one, but I don’t think it should be purely application only. Protocol support is necessary for supporting blobs, etc. (hence why I authored EIP-7932). A standard protocol-level interface for signatures is the best case forward (which is the sentiment I have gotten from this thread) as both application and protocol can use it.

Regarding key recovery, **most** PQ algorithms do not support it. I did have some thoughts about a potential companion EIP for 7932 for a system contract / precompile that holds public keys for addresses (anyone interested can find them here:`https://ethereum-magicians.org/t/storage-of-non-recoverable-account-keys-on-chain/27361` - I unfortunately cannot post a link yet).

---

**SirSpudlington** (2026-01-04):

[@pipavlo82](/u/pipavlo82) Thank you for your reply, I am glad you agree ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

![](https://ethresear.ch/user_avatar/ethresear.ch/pipavlo82/48/21580_2.png) pipavlo82:

> For the hashing/XOF question: would you consider any Keccak/SHAKE wiring “canonical enough” for EVM PQ verifiers (e.g., Keccak-based SHAKE128/256 vs a Keccak-CTR-style PRNG), and would you be open to a shared test-vector set so projects don’t benchmark different conventions by accident?

I am not the best person to ask when it comes to test vectors, but I do think they would be valuable for benchmarking purposes (and keeping everyone on the same page). With the wiring of PQ algorithms, it really depends on the way the algorithm is exposed. If with a precompile, I’d say the FIPS SHAKE version of the algorithm would be better because pure EVM based performance would not matter as much and it is the widely used standard. However, if EVM constrained then the Keccak-CTR-style PRNG would be better because of its gas efficiency. I like the “keep both versions” approach of EIP-8051/EIP-8052.


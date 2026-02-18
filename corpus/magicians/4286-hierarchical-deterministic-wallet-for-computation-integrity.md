---
source: magicians
topic_id: 4286
title: Hierarchical Deterministic Wallet for Computation Integrity Proof (CIP) Layer-2
author: guthlStarkware
date: "2020-05-14"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/hierarchical-deterministic-wallet-for-computation-integrity-proof-cip-layer-2/4286
views: 3186
likes: 0
posts_count: 4
---

# Hierarchical Deterministic Wallet for Computation Integrity Proof (CIP) Layer-2

In the context of Computation Integrity Proof (CIP) Layer-2 solutions such as ZK-Rollups, users are required to sign messages on new elliptic curves optimized for those environnements. These curves are Baby Jubjub (in the context of the BN254 SNARK approach) and Arya in (the context of StarkEx). Extensive work has been done to provide secure ways to derive private keys. We leverage this work to define an efficient way to securely derive private keys from existing infrastructure, as well as creating domain separation between Layer-2 applications.

In this proposal, we described both a derivation path allowing a user to derive hierarchical keys for Layer-2 solutions depending on the zk-technology, the application, the user’s Layer-1 address, as well as an efficient grinding method to enforce the private key distribution within the curve domain for curves with a smaller prime than secp256k1.

Feel free to comment on the proposal

## Replies

**fubuloubu** (2020-05-14):

So, a few comments:

1. BIP32 was originally designed only to produce secp256k1 private keys. If the output space has to be of a particular size, perhaps it would be helpful to redefine this proposal a bit to parameterize the key-derivation algorithm used to obtain the application-specific secret key. Something like m / purpose' / algorithm' / ... where algorithm dictates what algo to use (instead of being a hard node), or re-interpreting m to be the algorithm type (m := secp256k1) and adding a registry of other algorithms (maybe j := altbn128, which would look like j / purpose' / ...)
2. What type of Key Safety requirements do we need? This proposal will keep the original master key a secret (which seems like an obvious requirement), but how will application keys be requested? What prevents a malicious application from requesting keys for something it has no business accessing? This will be too complicated to rely on a wallet implementation to get right, or push to the end-user to approve applications to have access to particular paths.

Some other proposals:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png)
    [Extensible crypto for wallets](https://ethereum-magicians.org/t/extensible-crypto-for-wallets/2546) [Wallets](/c/wallets/17)



> Extensible crypto for wallets
> Problem
> SNARKs and STARKs require signatures algorithms that differ from Ethereums default one.
> EIP-1024 proposes encryption functions to be added to wallets, forcing all wallets to implement new crypto, which is complex and risky.
> DApps  have anticipated future needs for new cryptographic algorithms, for example diffie-hellman, off-the-record messaging, etc. Going through an EIP process each time is a bottleneck.
> As discussed in the ETH1x workshop, we should foc…



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bitgamma/48/999_2.png)
    [Non-wallet usage of keys derived from BIP-32 trees](https://ethereum-magicians.org/t/non-wallet-usage-of-keys-derived-from-bip-32-trees/1817) [Wallets](/c/wallets/17)



> Software interacting with the blockchain, including wallets, do not only revolve around pure asset transfer transactions but might have additional functionalities. In the case of Status that would be chat, but it can be anything like authentication, file encryption, etc. Using keys under the BIP32 tree for these purposes would allow the user to migrate the whole identity from one software to the other using the BIP39 mnemonic alone, since everything else would be derived from there.
> We plan to …

---

**guthlStarkware** (2020-05-14):

Following a discussion that happened on another channel, the current field Plugin’ should be used to define the underlying curve or associated technology. Wallets should ensure that the Plugin <-> curve mapping is correct.

Therefore, the algorithm field is unnecessary.

About 2, this proposal assumes native support from wallets. The Layer 2 private key should never leave the wallet. In our StarkEx work, we spent extensive time working with wallets to maintain the same security level than the Layer 1 as well as proper Tx readability.

Please notice that the grinding algorithm allows us to be as efficient as possible on constraint systems such as hardware wallets.

---

**guthlStarkware** (2020-05-17):

On a side note, we find that Plugin is not a great name for this field as it is used to define either the technology, the project and should allow a wallet to know to which curve this path refers to. Please post suggestions


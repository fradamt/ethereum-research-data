---
source: magicians
topic_id: 19769
title: "EIP-7693: Backward-Compatible Post-Quantum Migration"
author: nixxypQCee
date: "2024-04-23"
category: EIPs
tags: [signatures, cryptography, postquantum]
url: https://ethereum-magicians.org/t/eip-7693-backward-compatible-post-quantum-migration/19769
views: 1103
likes: 4
posts_count: 4
---

# EIP-7693: Backward-Compatible Post-Quantum Migration

Discussion thread for [Add EIP: Backward-Compatible Post-Quantum Migration · Pull Request #8454 · ethereum/EIPs  · GitHub](https://github.com/ethereum/EIPs/pull/8454).

We are excited to share a [draft of an EIP](https://github.com/pqcee/EIPs/blob/master/EIPS/eip-7693.md) that we have been working on. The proposal aims to present a solution for integrating a post-quantum signature scheme into the Ethereum blockchain while maintaining backward compatibility with existing ECDSA. The PQC signature scheme, targets integration with a quantum-safe zero-knowledge proof system such as zkSTARK or MPC-in-the-Head, to ensure the long-term security of Ethereum transactions against quantum attacks without requiring immediate upgrades to existing infrastructure. Looking forward to your thoughts on the proposal.

## Replies

**srarcharles** (2024-04-26):

Thanks for your new idea.

I read your new proposal.

I think its basic concept (“Backword-Compatible”) is great and I hope it will be established as soon as possible.

I think it is a good idea, because quantum computer attacks are a critical issue for almost all cryptocurrencies. Also, for all, the transition from the old wallet (non-quantum resistant) to the new wallet (quantum resistant) is difficult.

My concern with your EIP is that “proofUri” is not quantum secure. Your description uses off-chain storage (servers like Web2 or decentralized servers like IPFS), so you may not be able to retrieve proof data from these URIs. If the off-chain storage is not quantum secure and is attacked by an adversary, the proof becomes untrustworthy. This means that for all users/verifiers, there will be a malicious point of attack that cannot be trusted.

Second, if the ‘proofUri’ is not valid or unreachable due to network or hosting server issues, the ethereum validator will not be able to validate transactions using the proofUri and will not be able to generate blocks. This case raises concerns about the worst possible outcome.

It is my opinion that transaction validation that relies on external servers has drawbacks.

I hope that diverse discussions will take place and a great solution will be found.

---

**tanteikg** (2024-04-28):

Thanks for your comments.

Regarding your point on “proofUri” not being quantum secure, I assume you are referring to the “Migration Approaches” section. In our design, we propose to use “proofUri” as a means to reduce the size of data transmitted to the validators, which in turn will reduce some gas fees. If the storage containing the zkSTARK or MPCitH zero-knowledge proof is modified, then this modified proof will fail proof validation when retrieved by the validators, and the transaction will fail. Trust, in this case, is still preserved. However, you are right that the proofUri may be a point of vulnerability for Denial-of-Service attacks.

---

**pldallairedemers** (2024-08-03):

Regarding the migration procedure the end state should be aimed at being fully quantum resistant, carrying through quantum vulnerable primitives like ECDSA does introduce future liabilities and shovels the problem forward.

Notably, legacy software will still be vulnerable if an attacker controls validators, in which case a fork would be needed. If a fork is needed anyway it would be more advisable to introduce quantum resistant signatures directly in the codebase in a way that offers unconditional security and maintains the integrity of passphrase standards.

Half measures generate a false sense of security and does not incentives a complete upgrade.


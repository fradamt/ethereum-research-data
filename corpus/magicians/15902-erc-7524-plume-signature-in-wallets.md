---
source: magicians
topic_id: 15902
title: "ERC-7524: PLUME Signature in Wallets"
author: yush
date: "2023-09-24"
category: ERCs
tags: [erc, zkp]
url: https://ethereum-magicians.org/t/erc-7524-plume-signature-in-wallets/15902
views: 3098
likes: 18
posts_count: 14
---

# ERC-7524: PLUME Signature in Wallets

Discussion thread for [Add ERC: PLUME Signature in Wallets by Divide-By-0 · Pull Request #242 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/242)

This ERC adds a signature scheme called PLUME to existing Ethereum keypairs that enables unique anonymous nullifiers for accounts in ZK. This enables ZK voting, anonymous proof of solvency, unlinked airdrops, and moderation on anonymous message boards – all directly with Ethereum keypairs.

## Replies

**yush** (2023-10-06):

A good point was raised by @OrenYomtov that we should really call the V1/V2 as verifier-optimized vs prover-optimized.

---

**oren** (2023-10-15):

A PR to Taho Wallet implementing ERC-7524 has been created:

https://github.com/tahowallet/extension/pull/3638

---

**aguzmant103** (2023-11-06):

Great to see this moving forward! Are there PRs for other wallets?

---

**gitarg** (2023-11-06):

So cool, working on something similar with orgs, identity and handshakes, I don’t think its a different direction just neat name

---

**gitarg** (2023-11-06):

code looks more like implementation than a standard, anyone working on the eip:



      [Ethereum Improvement Proposals](https://eips.ethereum.org/all)





###



Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.










maybe a different standard already set?

I’ll take a crack at it but might need a different standard for what I’m working on, will review

---

**yush** (2023-11-07):

Yeah! For metamask, we have an open PR set ([rpc](https://github.com/MetaMask/eth-json-rpc-middleware/pull/198), [api](https://github.com/MetaMask/api-specs/pull/120), [core](https://github.com/MetaMask/metamask-extension/pull/17482)), and folks are working on Ledger implementations right now! Mina has an implementation and Aztec is currently building one.

---

**yush** (2023-11-07):

Hey – this standard has nothing to do with handshakes, are you sure you’re commenting on the  right post?

We think it’s important to have a standard so that different wallets can interoperate with each other, as everyone in some anonymity set needs to have the same PLUME signature for the nullifiers to work.

---

**yush** (2023-11-07):

We have reference implementations, but we expect many wallets (such as Ledger) to require bespoke implementations. You’ve linked to a blank EIPs page, are you referring to anything concrete?

---

**zemse** (2023-11-13):

This is so needed, why this is not a thing already?! Some zk apps require nullifiers, which have to be derived using the user’s secret. Since wallets are not supposed to provide access to private keys, there should be a way to get something that only the user knows, but seems there’s no API for it.

---

**yush** (2023-11-17):

Hey! We think the reason it hasn’t been adopted is due to slow wallet adoption and time needed to finish and audit the halo2 circuits for fast in browser proving. We wre optimistic that this will get better within the next few months.

---

**shreyas-londhe** (2023-12-12):

Hey Ayush, would love to know the status on the Plume Halo2 circuit. And also if metamask supports creating Plume Nullifiers. Thanks!

---

**yush** (2024-03-05):

As an update on this, Shreyas has finished the PLUME Halo2 circuits! We expect an audit to occur in April. The circuits are here: [Axiom V2 Halo2 implementation by Divide-By-0 · Pull Request #83 · plume-sig/zk-nullifier-sig · GitHub](https://github.com/plume-sig/zk-nullifier-sig/pull/83)

Even given the reasoned advances in ZKVMs such as SP1, we still believe that Halo 2 is likely to be the fastest for browser side Halo 2 proving, due to upcoming results with Web GPU acceleration + the register optimization of small field Starks likely not being as fast within WASM.

---

**zemse** (2025-07-02):

It would be helpful if `eth_getPlumeSignature` is specified within in the ERC as an API that dapps can expect wallets to implement.


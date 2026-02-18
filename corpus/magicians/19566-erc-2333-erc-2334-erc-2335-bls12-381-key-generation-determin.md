---
source: magicians
topic_id: 19566
title: "ERC-2333, ERC-2334, ERC-2335: BLS12-381 Key Generation, Deterministic Account Hierarchy, Keystore"
author: mratsim
date: "2024-04-06"
category: ERCs
tags: [erc, wallet, cryptography]
url: https://ethereum-magicians.org/t/erc-2333-erc-2334-erc-2335-bls12-381-key-generation-deterministic-account-hierarchy-keystore/19566
views: 592
likes: 0
posts_count: 1
---

# ERC-2333, ERC-2334, ERC-2335: BLS12-381 Key Generation, Deterministic Account Hierarchy, Keystore

Discussing 3 EIPs together because they are all interdependent, all same status, impacting the same teams.

**ERC-2333: BLS12-381 Key Generation**: [ERC-2333: BLS12-381 Key Generation](https://eips.ethereum.org/EIPS/eip-2333)

Discussion thread for [Draft EIP: BLS12-381 Key Generation by CarlBeek · Pull Request #2333 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2333)

Previous Github discussion thread: [Draft EIP: BLS12-381 Key Generation · Issue #2337 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/2337)

Reopen to review PR: [Update ERC-2333: Reopen to Review by mratsim · Pull Request #362 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/362)

**ERC-2334: BLS12-381 Deterministic Account Hierarchy**: [ERC-2334: BLS12-381 Deterministic Account Hierarchy](https://eips.ethereum.org/EIPS/eip-2334)

Discussion thread for [Draft EIP: BLS12-381 Deterministic Account Hierarchy by CarlBeek · Pull Request #2334 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2334)

Previous Github discussion thread: [Draft EIP: BLS12-381 Deterministic Account Hierarchy · Issue #2338 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/2338)

Reopen to review PR: [Update ERC-2334: Reopen to review by mratsim · Pull Request #363 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/363)

**ERC-2335: BLS12-381 Keystore**: [ERC-2335: BLS12-381 Keystore](https://eips.ethereum.org/EIPS/eip-2335)

Discussion thread for [Draft EIP: BLS12-381 Keystore by CarlBeek · Pull Request #2335 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2335)

Previous Github discussion thread: [Draft EIP: BLS12-381 Keystore · Issue #2339 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/2339)

Reopen to review PR: [Update ERC-2335: Reopen to Review by mratsim · Pull Request #364 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/364)

---

---

While those EIPs are marked stagnant, they are actually the defacto standard for the consensus layer keys as it is used in the official deposit-cli tool: [staking-deposit-cli/staking_deposit/key_handling/key_derivation/tree.py at v2.7.0 · ethereum/staking-deposit-cli · GitHub](https://github.com/ethereum/staking-deposit-cli/blob/v2.7.0/staking_deposit/key_handling/key_derivation/tree.py)

Consensus client teams use the implementation in BLST: [keygen.c: add EIP-2333 key derivation procedures. · supranational/blst@4e1935e · GitHub](https://github.com/supranational/blst/commit/4e1935eb722289789f5b8f8447415f77b63ff37c)

Both implementations were audited. (By NCC iirc)

**All consensus clients implement them** otherwise they can’t read consensus keys by the official staking tool.

- Lighthouse: lighthouse/book/src/key-management.md at 3058b96f2560f1da04ada4f9d8ba8e5651794ff6 · sigp/lighthouse · GitHub
- Lodestar: lodestar/packages/cli/src/cmds/validator/import.ts at f2ec0d42365b45495240ce65c27f4c6cdbd2d657 · ChainSafe/lodestar · GitHub
- Nimbus: nimbus-eth2/docs/the_nimbus_book/src/data-dir.md at dc19b082a9850bf9333e2371ea22230b61c2d501 · status-im/nimbus-eth2 · GitHub
- Prysm: prysm/validator/accounts/doc.go at 04f231a40083a5c1cf501abc7c46f39e2bf132f1 · prysmaticlabs/prysm · GitHub
- Teku: teku/infrastructure/bls-keystore/src/main/java/tech/pegasys/teku/bls/keystore/KeyStore.java at a11e4c5e0c78be82c68880f74996cc53ce7b6407 · Consensys/teku · GitHub

In the wild there are other implementations or references to EIP/ERC-2333:

- GitHub - ChainSafe/bls-keygen: Key management for BLS curves written in TypeScript and browser compatible
- constantine/constantine/ethereum_eip2333_bls12381_key_derivation.nim at 976c8bb215a3f0b21ce3d05f894eb506072a6285 · mratsim/constantine · GitHub
- GitHub - paulmillr/bls12-381-keygen: BLS12-381 Key Generation compatible with EIP-2333.
- ETH Withdrawals FAQ | Foundry
- Does Trezor Plan To Implement EIP2333 With A Firmware Update? · Issue #1556 · trezor/trezor-firmware · GitHub

I will reopen all EIPs as *Review* as per comment [Draft EIP: BLS12-381 Key Generation · Issue #2337 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/2337#issuecomment-1277480974)

I suggest they are fast-tracked to **Final (Core)**

cc [@CarlBeek](/u/carlbeek), the original author.

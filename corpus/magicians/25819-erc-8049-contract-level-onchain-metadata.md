---
source: magicians
topic_id: 25819
title: "ERC-8049: Contract-Level Onchain Metadata"
author: nxt3d
date: "2025-10-15"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8049-contract-level-onchain-metadata/25819
views: 145
likes: 1
posts_count: 6
---

# ERC-8049: Contract-Level Onchain Metadata

### Summary

Introduces a standard for storing contract-level metadata onchain. Extends ERC-7572’s concept with onchain storage. Optionally supports ERC-8042’s Diamond Storage pattern for cross-chain compatibility and upgradable contracts.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1260)














####


      `master` ← `nxt3d:contract-metadata-erc`




          opened 11:22AM - 15 Oct 25 UTC



          [![](https://avatars.githubusercontent.com/u/3857985?v=4)
            nxt3d](https://github.com/nxt3d)



          [+171
            -0](https://github.com/ethereum/ERCs/pull/1260/files)







### Summary

Introduces a standard for storing contract-level metadata onchain[…](https://github.com/ethereum/ERCs/pull/1260) using ERC-8042's Diamond Storage pattern. Extends ERC-7572's concept with onchain storage for cross-chain compatibility and upgradable contracts.

### Key Features

- **Diamond Storage**: Uses ERC-8042 for predictable storage locations
- **Cross-Chain Compatible**: Storage slots remain consistent across deployments
- **ERC-7572 Compatible**: Maintains compatibility with existing contract metadata standards
- **Upgradable Support**: Metadata persists through contract upgrades

### Technical Details

- Diamond Storage pattern for predictable storage locations
- Support for name, description, image, etc.

### Example Use Case

**Contract ENS Naming**: Any contract can store its ENS name using this standard:
- `name`: "MyToken"
- `description`: "A decentralized exchange for trading ERC-20 tokens"
- `ens_name`: "mycontract.eth"

This enables contracts to self-identify with ENS names while maintaining consistent metadata across chains and through upgrades.












### Key Features

- Flexible Implementation: Choose simple mapping or Diamond Storage based on your needs
- Two Reference Implementations: Basic (minimal code) and Diamond Storage examples
- Optional Diamond Storage: Uses ERC-8042 for predictable storage locations when needed
- Cross-Chain Compatible: Diamond Storage keeps slots consistent across deployments
- ERC-7572 Compatible: Maintains compatibility with existing contract metadata standards
- Upgradable Support: Metadata persists through contract upgrades

### Technical Details

- Simple string-key, bytes-value metadata interface
- Optional Diamond Storage pattern with namespace "erc8049.contract.metadata.storage"
- Support for name, description, image, collaborators, etc.
- Validated with comprehensive test suite

### Example Use Cases

**Basic Contract Information:**

- name: “MyToken”
- description: “A decentralized exchange for trading ERC-20 tokens”
- version: “1.0.0”

**Contract ENS Naming:**

Any contract can store its ENS name using this standard:

- ens_name: “mycontract.eth”

**Collaborators:**

Store multiple addresses as project collaborators:

- collaborators: abi.encodePacked(address1, address2, address3)

This enables contracts to self-identify with metadata while maintaining flexibility. Use the simple implementation for basic needs, or Diamond Storage for cross-chain consistency and upgradable contracts.

## Replies

**radek** (2025-10-22):

Even though Diamond is also my favourite, I would consider using diamond storage here as the implementation detail.

Meaning, the standard’s interface can be implemented by different ways - e.g. even by a pure function ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**nxt3d** (2025-10-22):

One of the goals of this ERC is to make it easier to prove metadata cross-chain. Diamond storage makes this very easy to do, whereas just calling the data using functions doesn’t provide any standard location for the storage values. It’s true that Diamond Storage could be optional. Maybe that would be a better way to go. ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

---

**radek** (2025-10-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nxt3d/48/16100_2.png) nxt3d:

> to make it easier to prove metadata cross-chain. Diamond storage makes this very easy to do

Can you elaborate more on this? Do you mean by calling `eth_getStorageAt` or using RIP7728  L1SLOAD?

---

**nxt3d** (2025-10-24):

Also, for `eth_getProof` ([EIP-1186: RPC-Method to get Merkle Proofs - eth_getProof](https://eips.ethereum.org/EIPS/eip-1186)), given only the key and implementing ERC-8049, it’s possible to do an inclusion proof without inspecting the storage layout of the data.

---

**nxt3d** (2025-10-25):

I decided to make Diamond Storage optional. This will generally limit the complexity required to implement this ERC.


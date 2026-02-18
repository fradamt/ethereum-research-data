---
source: magicians
topic_id: 15667
title: "EIP-7508: Dynamic On-Chain Token Attributes Repository"
author: ThunderDeliverer
date: "2023-09-05"
category: EIPs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/eip-7508-dynamic-on-chain-token-attributes-repository/15667
views: 1702
likes: 3
posts_count: 6
---

# EIP-7508: Dynamic On-Chain Token Attributes Repository

We are proposing an Ethereum Improvement Proposal to provide the ability to assign attributes to NFTs in a public non-gated repository smart contract that is accessible at the same address in all of the networks. The repository smart contract is designed to be a common-good repository, meaning that it can be used by any ERC-721 or ERC-1155 compatible token.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7508)





###



Store attributes related to NFTs with custom access control

## Replies

**Mani-T** (2023-09-08):

This proposal brings valuable enhancements to the NFT ecosystem by introducing standardized on-chain attributes storage. Also, allowing tokens to store attributes in a standardized format for cross-collection interactivity is a valuable addition. this can foster interoperability and reuse of NFT attributes across different projects, enhancing the utility of NFTs.

---

**rmeissner** (2023-09-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/thunderdeliverer/48/7407_2.png) ThunderDeliverer:

> accessible at the same address in all of the networks.

How would you achieve this across all L2 networks without any trusted party being involved? Asking because multiple teams have different approaches, but most of them have a trusted deployer involved (either for the contract itself or for a factory). If a trusted deployer it used it could be argued that this repository is not fully “non-gated” as the trusted deployer can choose not to deploy it.

Beyond this there are networks that are not bytecode equivalent that support NFTs, would these networks be excluded?

Edit: I am aware of presigned deployment transactions but out of experience they don’t always work due to networks enforcing the usage of chain id or differences in gas metering and gas prices.

---

**ThunderDeliverer** (2023-09-19):

This is a good comment. Thank you for it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> How would you achieve this across all L2 networks without any trusted party being involved? Asking because multiple teams have different approaches, but most of them have a trusted deployer involved (either for the contract itself or for a factory). If a trusted deployer it used it could be argued that this repository is not fully “non-gated” as the trusted deployer can choose not to deploy it.

Our current flow expects us to act as trusted deployers. We use a proxy with CREATE2 opcode to deploy the repository to the desired address. I get the argument, but I don’t see this as a possibility. Since this is a repository that anyone can use and interact with without any restrictions, I think it signals a straightforward motivation of openness. We want to improve the ecosystem, no matter the chain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> Beyond this there are networks that are not bytecode equivalent that support NFTs, would these networks be excluded?

We encountered this issue once before on another project with zkSync. I think we can work with the L2 teams to add the repository as a precompile available at the desired address.

---

**ThunderDeliverer** (2023-09-19):

Thank you for your support. We are really excited about this proposal! ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**ThunderDeliverer** (2023-09-19):

We deployed the repository to multiple test networks:

- Polygon Mumbai
- Sepoila
- MoonBase Alpha
- Base Goerli
- Arbitrum Goerli

The address of the repository is:

**0xA77b75D5fDEC6E6e8E00e05c707a7CA81a3F9f4a**


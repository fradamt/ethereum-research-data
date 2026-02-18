---
source: magicians
topic_id: 18545
title: "ERC-7616: the hybrid fungible token"
author: fomo-protocol
date: "2024-02-07"
category: ERCs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/erc-7616-the-hybrid-fungible-token/18545
views: 1382
likes: 0
posts_count: 3
---

# ERC-7616: the hybrid fungible token

This is the discussion thread for: [ERC-7616](https://github.com/ethereum/ERCs/pull/244)

This proposal introduces a hybrid fungible token standard that merges the ERC-20 token’s fungibility with the unique identification capabilities of ERC-721 tokens. New ERC introduced a way to manage both ERC-20 and ERC-721 tokens in 1 contract.

The motivation behind this EIP is to address the limitations of current token standards by combining the best aspects of ERC-20 and ERC-721, enhancing liquidity, and simplifying the control over token fractionalization and reassembly. This hybrid approach seeks to streamline the integration of DeFi and NFT utilities, leveraging existing infrastructure for faster adoption and minimal disruption to current applications.

## Replies

**xinbenlv** (2024-03-03):

Hi, thank you for contributing an ERC draft. Before I can merge this ERC, the proposal actually breaks ERC-20 and ERC-721. They are not ERC-20 and ERC-721 compliant. Can you verify was it intentional and clarify in the backward compatibility?

---

**fomo-protocol** (2024-03-03):

Yes, the deviation from full ERC-20 and ERC-721 compliance in our ERC draft is intentional.

Our goal is to align as closely as possible with the ERC-20 and ERC-721 standards. However, achieving complete compliance is not feasible without compromising the innovative aspects of our proposal. We’re focusing on minimizing disruptions to ensure that users experience minimal inconvenience. As more applications begin to adopt the ERC7616 standard, we anticipate a smoother integration across the ecosystem.

For instance, regarding the Transfer event, we have opted to adhere to the ERC-721 standard rather than the ERC-20 standard. This decision was made because most NFT marketplaces depend on this event for accurate balance displays. As a result, ERC-20 transfers may not display correctly until applications update their systems to be ERC7616 compliant.

Similarly, for the balanceOf function, we’ve chosen to follow the ERC-20 standard over the ERC-721 standard. This approach is due to the reliance of most decentralized exchanges (DEXs) on this method for displaying ERC-20 token balances.

These decisions are part of our strategy to ensure that ERC7616 offers a balanced and less disruptive integration into the current ecosystem, acknowledging the need for backward compatibility adjustments.


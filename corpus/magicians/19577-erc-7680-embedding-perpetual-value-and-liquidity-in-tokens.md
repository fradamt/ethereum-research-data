---
source: magicians
topic_id: 19577
title: "ERC-7680: Embedding Perpetual Value and Liquidity in Tokens"
author: catiga
date: "2024-04-07"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7680-embedding-perpetual-value-and-liquidity-in-tokens/19577
views: 873
likes: 1
posts_count: 3
---

# ERC-7680: Embedding Perpetual Value and Liquidity in Tokens

### Abstract

The ERC-7680 standard introduces a innovative token protocol that ensures every token intrinsically maintains a minimum value and liquidity. This is achieved by integrating a Base Liquidity Pool (BLP) within the token’s contract, safeguarding against the token’s devaluation and providing a fail-safe against the withdrawal of third-party liquidity pools, commonly seen in decentralized exchanges (DEX).

### Introduction

In the dynamic world of Ethereum and its diverse token standards, the innovative ERC-7680 proposal emerges as a groundbreaking approach to token economics. Aiming to address the inherent volatility and risks associated with reliance on external liquidity pools (e.g., DEXs), ERC-7680 introduces a novel token protocol that embeds intrinsic value and liquidity within the token itself, effectively preventing the token’s value from plummeting to zero due to liquidity withdrawal or fraudulent schemes.

### Motivation: Addressing Tokenomics Vulnerabilities

ERC-7680 targets the fundamental issues of token devaluation and reliance on external liquidity pools. By embedding a base value and liquidity within the token itself, ERC-7680 sets a new standard for stable and reliable token economics on Ethereum.

### The Core of ERC-7680: SolidValue and Inbuilt Liquidity Mechanism

At the heart of ERC-7680 is the concept of **SolidValue**, a design principle ensuring that each token maintains a baseline value backed by a fixed amount of Ethereum (ETH) within a Base Liquidity Pool (BLP) integrated into the token contract. This innovative mechanism ensures each token’s value is not solely dependent on external market forces but is instead underpinned by tangible, intrinsic value.

#### Key Mechanisms:

1. SolidValue Calculation:

- The minimum value of each token (_eachTokenValue) is defined as the total ETH in the BLP (_totalSolidValue) divided by the total token supply (_totalSupply).
- MathematicalRepresentation:_eachTokenValue=_totalSolidValue/_totalSupply

1. Value Enhancement:

- Token holders can increase the token’s intrinsic value by adding ETH to the BLP, thus raising the _totalSolidValue and, by extension, the _eachTokenValue.

1. Value Retrieval through Token Burn:

- Holders can burn their tokens to withdraw a proportionate value from the BLP, effectively reducing _totalSupply and potentially increasing the _eachTokenValue for the remaining tokens.

Solidifying Token Value through Direct Interactions:

The ERC2510 standard allows for direct actions that impact the token’s value:

```auto
// Enhance the token's value by adding ETH to the BLP
function enhanceTokenValue() external payable {
    require(msg.value > 0, "Contribution must be more than 0 ETH");
    emit EnhanceValue(msg.sender, msg.value);
}
```

```auto
// Retrieve value from the BLP by burning tokens
function retrieveTokenValue(uint256 _amount) external {
    uint256 retrieveValue = calculateSolidValue() * _amount;
    _burn(msg.sender, _amount);
    payable(msg.sender).transfer(retrieveValue);
    emit RetrieveValue(msg.sender, retrieveValue);
}
```

These operations exemplify the proactive role holders can play in managing the token’s economic model, ensuring stability, and fostering a robust token ecosystem.

### Advantages of ERC-7680:

- Mitigation of Devaluation Risks: By embedding a minimum value within the token itself, ERC-7680 drastically reduces the risk of token value collapse.
- Decentralization of Value Management: Empowers token holders to directly influence the token’s value, democratizing financial outcomes.
- Enhanced Market Stability: Offers a buffer against market volatility and speculative trading, contributing to a more stable token economy.

### A Call for Community Engagement

The development of ERC-7680 is a collaborative effort, seeking insights, feedback, and contributions from the Ethereum community. By participating in the discussion and refinement of ERC2510, we can collectively enhance the stability, utility, and trustworthiness of tokens within the Ethereum ecosystem.

### ERC-7680 Implementation Repo:

[ERC-7680 Implementation](https://github.com/catiga/ERC2510)

## Replies

**catiga** (2024-04-07):

We’ve submitted ERC PR for more discussion, and could check it here [ERC-7680 Pull Request](https://github.com/ethereum/ERCs/pull/368)

---

**catiga** (2024-04-09):

We also provide a marketplace for erc-2510 protocol

https://novaswap.xyz/


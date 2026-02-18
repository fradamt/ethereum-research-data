---
source: magicians
topic_id: 22276
title: "ERC-DRAFT: WTTP - Pioneering the Future of Decentralized Internet Browsing"
author: TechnicallyWeb3
date: "2024-12-18"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-draft-wttp-pioneering-the-future-of-decentralized-internet-browsing/22276
views: 87
likes: 2
posts_count: 2
---

# ERC-DRAFT: WTTP - Pioneering the Future of Decentralized Internet Browsing

Experience the evolution of HTTP with WTTP, enabling seamless, decentralized web browsing on blockchain networks. A core networking protocol ERC for EVM-based chains and the future of the internet.

## Introducing WTTP: A New Era for Decentralized Web Protocols

Hello Ethereum Magicians,

We are thrilled to introduce the **Web3 Transfer Protocol (WTTP)**, a groundbreaking blockchain-based protocol that brings HTTP-like functionality to decentralized web resources. WTTP is designed to revolutionize how we store, retrieve, and manage web content on the blockchain, with built-in content addressing and royalty mechanisms. We like to describe it as the Apache web server of EVM.

### Why WTTP?

WTTP aims to provide a comprehensive system for decentralized web resources, offering features such as:

- HTTP-like Methods: Supports GET, PUT, PATCH, HEAD, and more for seamless resource management.
- Content-Addressed Storage: Ensures efficient data deduplication and collision-resistant addressing.
- Royalty System: Implements gas-based royalty calculations and publisher royalty collection.

### Seeking Collaborative Input for ERC Proposal

We believe WTTP has the potential to become a core networking ERC for EVM-based chains, and we are reaching out to the community for collaborative input. Our team is passionate about this project, but we recognize the value of diverse perspectives and expertise, especially from those experienced in drafting ERCs.

If you are interested in contributing to a protocol that could shape the future of decentralized web interactions, we would love to work with you. Your insights and feedback can help us refine WTTP and ensure it meets the needs of the broader Ethereum ecosystem.

### Get Involved

- Explore the Codebase: Dive into our GitHub repository to understand the protocol’s architecture and implementation.
- Review the Protocol Specification: Check out the detailed WTTP Specification to see how WTTP is structured and operates.
- Join the Discussion: Collaborate with us on GitHub or Discord in refining the protocol and drafting the ERC proposal. Your input is invaluable!

### Quick Start

To get started with WTTP, follow these steps:

1. Deploy Your Site Contract: Use Remix IDE or Hardhat to deploy your contract to the Sepolia testnet. Here’s a sample contract to get you started:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@tw3/solidity/contracts/wttp/TW3Site.sol";

contract MyFirstSite is TW3Site {
    constructor(
        string memory _name,
        string memory _description,
        string memory _tags
    ) TW3Site(_name, _description, _tags) {}
}
```

1. Install WTTP Handler: Use the following command to install the WTTP handler:

```bash
npm install wttp-handler
```

1. Create a Basic Script: Use the WTTP handler to interact with your deployed contract. Here’s a simple example:

```javascript
const { wttp } = require('wttp-handler');
const { Wallet } = require('ethers');
require('dotenv').config();

const SITE_ADDRESS = "0x..."; // Replace with your deployed contract address
const signer = new Wallet(process.env.PRIVATE_KEY);

async function main() {
    const putResponse = await wttp.fetch(`wttp://${SITE_ADDRESS}/index.html`, {
        method: "PUT",
        headers: {
            "Content-Type": "text/html; charset=utf-8",
            "Content-Location": "datapoint/chunk",
            "Publisher": signer.address
        },
        body: "Hello Web3!",
        signer: signer
    });
    console.log("PUT Response:", putResponse.status);

    const getResponse = await wttp.fetch(`wttp://${SITE_ADDRESS}/index.html`);
    const content = await getResponse.text();
    console.log("Content:", content);
}

main().catch(console.error);
```

### Join the Revolution

We believe WTTP can be a cornerstone for the decentralized web, and we invite you to be part of this journey. Let’s collaborate to make WTTP a robust and widely-adopted protocol.

For more details, visit our [GitHub repository](https://github.com/TechnicallyWeb3/wttp) and feel free join our [Discord](https://discord.gg/ArH9kRPQrD) to reach out with any questions or suggestions.

Together, let’s build the future of the decentralized web!

## Replies

**ChrisHashing** (2025-05-05):

Really impressed by the direction WTTP is taking — feels like a natural evolution for truly decentralized web access. The HTTP-like interface combined with on-chain content routing is super promising, especially with support for methods like `GET` and `PATCH`.


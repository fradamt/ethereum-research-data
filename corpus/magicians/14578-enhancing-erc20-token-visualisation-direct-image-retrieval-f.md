---
source: magicians
topic_id: 14578
title: "Enhancing ERC20 Token Visualisation: Direct Image Retrieval from Smart Contracts\""
author: njrapidinnovation
date: "2023-06-05"
category: ERCs
tags: [erc, token]
url: https://ethereum-magicians.org/t/enhancing-erc20-token-visualisation-direct-image-retrieval-from-smart-contracts/14578
views: 479
likes: 0
posts_count: 1
---

# Enhancing ERC20 Token Visualisation: Direct Image Retrieval from Smart Contracts"

**Issues in Current Image Retrieval and Storage Process:**

1. Centralization: Reliance on centralized servers or platforms for image storage introduces vulnerabilities and single points of failure.
2. Trust: Users must trust that the displayed image is authentic, as it can be manipulated or substituted when hosted externally.
3. Update Coordination: Updating the image requires coordination with multiple third-party services, which can be time-consuming and prone to errors.
4. Cost: Maintaining centralized image storage infrastructure can be expensive for token creators, especially for smaller projects or individuals.

**Benefits of Storing Images in Smart Contracts:**

1. Transparency and Decentralization: Storing images on the blockchain ensures transparency and decentralization, promoting trust and accountability.
2. Enhanced Security: Images stored on the blockchain are resistant to tampering, ensuring the integrity of the token’s image representation.
3. Cost-effectiveness: Storing images in smart contracts eliminates the need for centralized servers, reducing infrastructure costs.
4. Flexibility and Ease of Update: Smart contracts allow for easy image updates, saving time, resources, and ensuring consistency across platforms.
5. Improved Accessibility: Storing images in smart contracts enables inclusion of accessibility features, making the token more inclusive for users with disabilities.

**Resource Savings:**

1. Infrastructure Costs: Storing images in smart contracts eliminates hosting and maintenance expenses associated with centralized servers.
2. Development Effort: Integrating with external image storage services is unnecessary, saving development time and effort.
3. Coordination Efforts: Updating images in smart contracts eliminates the need for individual coordination with multiple third-party services.
4. Security Measures: Storing images on the blockchain reduces the need for additional security measures, saving resources.

In summary, storing images directly in smart contracts provides cost savings, transparency, security, flexibility, and accessibility advantages over the current image retrieval and storage process.

**Details**

- A method to set the SVG image in string format.
- A method to get the SVG image url in string format.

I took inspiration from `generateNftSvgByTokenId` method in [On-chain-svg-nft-tickets](https://github.com/MetaMask/onchain-svg-nft-tickets/blob/start/apps/blockchain/contracts/ETHTickets.sol)

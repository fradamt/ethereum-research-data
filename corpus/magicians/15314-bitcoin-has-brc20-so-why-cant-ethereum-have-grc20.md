---
source: magicians
topic_id: 15314
title: Bitcoin has BRC20, so why can't Ethereum have GRC20?
author: JXRow
date: "2023-08-01"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/bitcoin-has-brc20-so-why-cant-ethereum-have-grc20/15314
views: 430
likes: 2
posts_count: 1
---

# Bitcoin has BRC20, so why can't Ethereum have GRC20?

### I have an idea

I initially wanted to add a `tokenURI()` function to ERC20 to define the logo and description of the token, just like in ERC721. However, I noticed that the `tokenURI()` function in ERC721 does not specify the format of the returned string, although most formats actually adopt the OpenSea standard. So, we can also define the `tokenURI()` function for ERC20 in a similar way. For example:

```solidity
function tokenURI(uint256 tokenId) external view returns (string memory) {

return "https://github.com/ZKSAFE/zksafe-docs/blob/main/images/zkSafe_logo0.png?raw=true";

}

```

This way, we can associate the logo with the ERC20 token. But how can we bind the introduction and roadmap information to it? I thought about linking the project’s GitHub address and storing various information separately based on a standardized path using GRC20. For example:

```solidity
function tokenURI(uint256 tokenId) external view returns (string memory) {

return "https://github.com/ZKSAFE/zksafe-docs";

}

```

So, `/README.md` would serve as the official website, `/images/logo.png` would be the logo, `/contracts` would contain the contract source code, and so on.

### Why choose the name GRC20?

Bitcoin has BRC20, so why can’t Ethereum have GRC20? It’s important to note that BRC20 was not proposed by the Bitcoin Foundation or Satoshi Nakamoto; it was introduced by an unknown individual. However, it brought significant attention and discussion to the otherwise quiet Bitcoin ecosystem. Perhaps BRC20 is not inherently more advanced or innovative than ERC20, but it injected vitality into the ecosystem, and that is an objective fact.

I have seen many developers move from the Ethereum ecosystem to other public chains like Polkadot and Cosmos because their voices were not heard or acknowledged within the Ethereum community. There may be excellent ideas and concepts that go unnoticed simply because the proposers are unknown or their ideas are too unconventional to be accepted by mainstream thinking. This forces them to migrate to other communities outside of Ethereum.

This is precisely what the Ethereum ecosystem lacks at the moment. All Ethereum’s plans are documented in EIPs and Vitalik’s speeches. I’m not saying that the Ethereum Foundation’s efforts are inadequate, but all the community’s attention is focused on the official channels, and imagination and discussions are limited within the realm of EIPs. Instead of letting these underappreciated developers move to other public chains, it would be better to encourage them to form unofficial organizations that can work closely with the official Ethereum community. This is not about splitting the developer community; unofficial organizations are also builders of Ethereum. They can support ideas that may not receive recognition within the official channels and help bring attention and discussion to these ideas.

And GRC20 is an unofficial attempt that sets itself apart from ERC standards.

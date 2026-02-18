---
source: magicians
topic_id: 13047
title: Fork-safe tokens
author: Pandapip1
date: "2023-02-24"
category: Magicians > Primordial Soup
tags: [token]
url: https://ethereum-magicians.org/t/fork-safe-tokens/13047
views: 407
likes: 1
posts_count: 1
---

# Fork-safe tokens

This is an extremely rough draft of an idea I recently had.

Since the `CHAINID` opcode exists, tokens can store the balance per chain ID. Before a hard fork, users can transfer their assets to the new (un)forked network. This would be different than *bridging* the tokens, as the new network doesn’t exist yet. Instead, when the new network is formed, the balance is split so that the total supply across all chains remains unchanged.

This would be particularly useful for stablecoins like DAI, because it would get around the problem of “we can only support one network since the supply doubles every hard fork.”

Prototype interfaces:

```plaintext
contract ERC20ForkSafe is ERC20 {
    event TransferFork(uint256 fromChainId, uint256 toChainId, address indexed from, address indexed to, uint256 amount);
    function transferToFork(uint256 fromChainId, uint256 toChainId, address to, uint256 amount) external;
    function transferFromToFork(uint256 fromChainId, uint256 toChainId, address from, address to, uint256 amount) external;
    function isTransferAvailable(uint256 fromChainId, uint256 toChainId) external view returns (bool);
}
```

```plaintext
contract ERC721ForkSafe is ERC721 {
    event TransferFork(uint256 fromChainId, uint256 toChainId, address indexed from, address indexed to, uint256 tokenId);
    function transferToFork(uint256 fromChainId, uint256 toChainId, address to, uint256 tokenId) external;
    function transferFromToFork(uint256 fromChainId, uint256 toChainId, address from, address to, uint256 tokenId) external;
    function isTransferAvailable(uint256 fromChainId, uint256 toChainId) external view returns (bool);
}
```

```plaintext
contract ERC1155ForkSafe is ERC1155 {
    event TransferFork(uint256 fromChainId, uint256 toChainId, address indexed from, address indexed to, uint256 tokenId, uint256 amount);
    function transferToFork(uint256 fromChainId, uint256 toChainId, address to, uint256 tokenId, uint256 amount) external;
    function transferFromToFork(uint256 fromChainId, uint256 toChainId, address from, address to, uint256 tokenId, uint256 amount) external;
    function isTransferAvailable(uint256 fromChainId, uint256 toChainId) external view returns (bool);
}
```

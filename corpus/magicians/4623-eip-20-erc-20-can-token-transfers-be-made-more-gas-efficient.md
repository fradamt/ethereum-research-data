---
source: magicians
topic_id: 4623
title: "EIP-20 (ERC-20): Can token transfers be made more gas efficient?"
author: cmango
date: "2020-09-16"
category: EIPs
tags: [erc-20]
url: https://ethereum-magicians.org/t/eip-20-erc-20-can-token-transfers-be-made-more-gas-efficient/4623
views: 1836
likes: 0
posts_count: 3
---

# EIP-20 (ERC-20): Can token transfers be made more gas efficient?

A normal ERC-20 token transfer transaction takes about 51,000 gas.

The function that does the transfer is this one (this is the OpenZeppelin ERC-20 implementation):

```
function _transfer(address sender, address recipient, uint256 amount) internal virtual {
    require(sender != address(0), "ERC20: transfer from the zero address");
    require(recipient != address(0), "ERC20: transfer to the zero address");

    _balances[sender] = _balances[sender].sub(amount, "ERC20: transfer amount exceeds balance");
    _balances[recipient] = _balances[recipient].add(amount);
    emit Transfer(sender, recipient, amount);
}
```

What I noticed is that if the recipient token change line is commented out, the **gas cost comes down very significantly, to about 30,000 gas**:

```
// _balances[recipient] = _balances[recipient].add(amount);
```

It seems the problem is that we have to go through the same *_balances* hashmap twice (for sender and for recipient). Could this be somehow improved so that both sender’s and recipient’s balances could be updated in one iteration?

## Replies

**cmango** (2020-09-16):

I see in [this StackExchange answer](https://ethereum.stackexchange.com/a/17410) that mappings in Solidity are not really hash tables (there are no iterations through mappings). So perhaps iterations are not the issue for the high gas usage here… Looks like there’s no way around this.

---

**qizhou** (2020-10-26):

The underlying implementation of contract storage is a Merkle Patrica Tree, which is expensive for read/write.  Further, if you write a new entry into the tree (i.e., increasing balance from 0 to non-zero), EVM will charge 20,000 gas in EIP2200.  The cost can be even higher for _transferFrom, which is widely used by contract interactions with extra write to allowance map.

Since the MPT access cost is so high, we are proposing [an upgraded ETH without MPT,](https://ethereum-magicians.org/t/eip-alternative-eth2-0-a-non-sharding-approach/4857) which could achieve at least 4-5x performance increase based on our experiments.


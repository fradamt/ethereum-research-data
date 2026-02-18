---
source: magicians
topic_id: 14269
title: Smart contract quasi-introspection
author: nand
date: "2023-05-13"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/smart-contract-quasi-introspection/14269
views: 447
likes: 1
posts_count: 2
---

# Smart contract quasi-introspection

Hi!

I was wondering, would it not be good to have a standard interface in smart contract that outputs its ABI? e.g.

```plaintext
interface IABIIntrospection {
  function getABI() external view returns(string);
}
```

The reasoning is, we mostly publish this off-chain on Etherscan, but I feel like a smart contract should be able to broadcast its ABI.

But I am somehow sure this has already been discussed, but I haven’t found, so I apologize in advance.

Another layer, which may have not yet been discussed, would be an interface to point to the original source code + compiler version/infos, as we send to Etherscan. This could be an URL, which could be an ERC-4804 web3:// URL pointing on-chain, or an ipfs:// URL.

Thanks for the discussion.

## Replies

**MingyuanHuang** (2023-05-20):

I’m not sure if this is necessary, but there is a similar EIP that may be useful for you to follow:

[EIP165](https://eips.ethereum.org/EIPS/eip-165) Standard Interface Detection, which allows a contract to declare and provide its implemented standard interface.

This scheme also has issues that need attention, here is an [example](https://github.com/OpenZeppelin/openzeppelin-contracts/pull/3552), unqualified `getABI` may lead to similar issues.


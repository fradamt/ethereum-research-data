---
source: magicians
topic_id: 2814
title: "ERC 1812: Ethereum Verifiable Claims"
author: pelle
date: "2019-03-03"
category: EIPs
tags: [verifiable-claims, erc-1812]
url: https://ethereum-magicians.org/t/erc-1812-ethereum-verifiable-claims/2814
views: 4569
likes: 2
posts_count: 3
---

# ERC 1812: Ethereum Verifiable Claims

This is the discussion thread for [EIP 1812](https://github.com/ethereum/EIPs/pull/1812).

The goal is to create standards for Reusable Verifiable Claims using [EIP 712 Signed Typed Data](https://github.com/ethereum/EIPs/issues/712).

I will also be at the Council of Paris and would love any feedback in person.

## Replies

**jinserk** (2019-03-18):

Hi [@pelle](/u/pelle),

I’m very new to DID so have some questions for this EIP:

- For the case of DID, who is the issuer? If I’d like to permit to view or update the part of my profile, should the issuer be myself?
- I’m thinking of ERC721-like profile system using delegate the ownership, not permitting to transfer. ERC721 has metadata attributes to add some off-chain data location. What’s the difference between DID and using ERC721?

Thank you!

Jinserk

---

**bitcoinbrisbane** (2020-01-23):

Hi pelle, I found your EIP and it has a lot in common with mine. https://eips.ethereum.org/EIPS/eip-1753.  Id like to try work together to perhaps refactor methods “revoke” “isValid” etc to use 1812.  Love to hear your thoughts.

For example, my “Permit” Struct is pretty much identical

```auto
struct Permit {
		address issuer;
		uint256 start;
		uint256 end;
	}
```


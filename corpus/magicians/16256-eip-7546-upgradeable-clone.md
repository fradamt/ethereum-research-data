---
source: magicians
topic_id: 16256
title: "EIP-7546: Upgradeable Clone"
author: KaiHiroi
date: "2023-10-25"
category: EIPs
tags: [erc, proxy-contract, upgradeable-contract]
url: https://ethereum-magicians.org/t/eip-7546-upgradeable-clone/16256
views: 1410
likes: 3
posts_count: 4
---

# EIP-7546: Upgradeable Clone

Discussion for

https://github.com/ethereum/ERCs/pull/39

## Replies

**SamWilsn** (2023-12-15):

How is this different from [EIP-2535](https://eips.ethereum.org/EIPS/eip-2535)?

---

**SamWilsn** (2023-12-15):

> Furthermore, it is RECOMMENDED for each implementation contract to implement ERC-165’s supportsInterface(bytes4 interfaceID) to ensure that it correctly implements the function selector being registered when added to the Dictionary.

Is there a risk of accidentally calling the implementation contract directly? Should that be addressed somewhere?

---

**SamWilsn** (2023-12-15):

> It is RECOMMENDED to choose the storage management method that is considered most appropriate at the time.

How does the external application determine which storage layout is in use?


---
source: magicians
topic_id: 14813
title: "EIP-XX: add gasRefund for CREATE/CREATE2 if the codeHash already exist"
author: joohhnnn
date: "2023-06-23"
category: EIPs
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/eip-xx-add-gasrefund-for-create-create2-if-the-codehash-already-exist/14813
views: 498
likes: 1
posts_count: 3
---

# EIP-XX: add gasRefund for CREATE/CREATE2 if the codeHash already exist

should we make CREATE/CREATE2 have some gasRefund if the codeHash already exist.

This discussion could potentially lead to a new EIP (if there isn’t an existing EIP with the same content). When a new contract is created, if the contract’s codeHash already exists, the node will reuse the same code. In this case, would it be possible to provide a gas refund to the deployer?

This approach provides significant support for the creation of abstract wallet accounts, AMM pair contracts, proxy contracts, admin contracts, and many other scenarios where the majority of users utilize the same `codeHash` .

## Replies

**xinbenlv** (2023-06-23):

Can you elaborate how do you propose the gas refund amount be calculated?

Intuitively it seems to me the saving of gas come from that EVM don’t need to load init_code again if the hash matches, but I am not sure, and maybe the side effect is that the EVM need to maintain a list of init_code hashes to check for mapping which can have its own storage and memory implications?

---

**xiaobaiskill** (2023-06-24):

If two contracts have the same `deployedBytecode`, their codeHash will be identical. Storing duplicate copies of the same `deployedBytecode` would result in unnecessary disk consumption. I personally support your proposal. Additionally, I suggest creating a codeHash table (mapping codeHash to `deployedBytecode`), where if a codeHash already exists, there is no need to store the `deployedBytecode` again. This approach would help save disk storage space.


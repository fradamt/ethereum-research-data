---
source: magicians
topic_id: 4569
title: "EIP 2936: EXTCLEAR for SELFDESTRUCT"
author: wjmelements
date: "2020-09-04"
category: EIPs
tags: [evm]
url: https://ethereum-magicians.org/t/eip-2936-extclear-for-selfdestruct/4569
views: 2321
likes: 1
posts_count: 5
---

# EIP 2936: EXTCLEAR for SELFDESTRUCT

This [EIP](https://github.com/ethereum/EIPs/pull/2936) reduces the complexity of SELFDESTRUCT by deferring the clearing of storage. Instead storage is cleared by a new opcode, EXTCLEAR.

## Replies

**wjmelements** (2020-09-04):

I am interested to know whether or not the `SELFDESTRUCT` change would be easier to implement retroactively or not. I do not care either way; complexity is what matters.

---

**Amxx** (2020-09-04):

Random question: could this be used to “cleanup” all the storage of a “not self destructed” smart contract.

Example: I want to repurpose a proxy to delegate to a new contract with incompatible memory layout, can I EXTCLEAR to remove the contract storage, keep the contract code, an just write the new delegation address (to an otherwize empty storage) ?

---

**wjmelements** (2020-09-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> could this be used to “cleanup” all the storage of a “not self destructed” smart contract.

No, this only allows cleanup of storage corresponding to accounts currently with codesize zero. This supports the non-proxy CREATE2 reincarnation upgrade pattern, and if your proxy was created with CREATE and not CREATE2 you would not be able to reincarnate it.

---

**ilanDoron** (2020-09-14):

Could u clarify this sentence from the EIP:

"and just check if the contract was initiated since  `SSTORE`  ( `0x55` ) during  `SLOAD`"


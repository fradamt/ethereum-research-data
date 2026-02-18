---
source: magicians
topic_id: 22845
title: "EIP-7880: EOF - EXTCODEADDRESS instruction"
author: shemnon
date: "2025-02-12"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7880-eof-extcodeaddress-instruction/22845
views: 56
likes: 1
posts_count: 3
---

# EIP-7880: EOF - EXTCODEADDRESS instruction

Discussion topic for EIP-7880: EOF - EXTCODEADDRESS instruction

#### Update Log

- 2025-02-12: initial draft

#### External Reviews

None as of 2025-02-12

#### Outstanding Issues

None as of 2025-02-12

## Replies

**wjmelements** (2025-02-12):

> as the contract may be updated to non EOF code and EXTDELEGATECALL will no longer be able to call the contract

Where is this specified? It would be a severe limitation on the eof methods if they can’t call non-eof code.

---

**shemnon** (2025-02-13):

EOF1 contracts can only `EXTDELEGATECALL` EOF1 contracts - [EIP-3540: EOF - EVM Object Format v1](https://eips.ethereum.org/EIPS/eip-3540#eof1-contracts-can-only-delegatecall-eof1-contracts)

This has been a restriction because of `SELFDESTRUCT`, we don’t want EOF code disappearing for any reason, even in neo-`SELFDESTRUCT` form.

EOF can freely `EXTCALL` and `EXTSTATICCALL` legacy code.


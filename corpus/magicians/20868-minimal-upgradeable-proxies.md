---
source: magicians
topic_id: 20868
title: Minimal Upgradeable Proxies
author: Vectorized
date: "2024-08-23"
category: ERCs
tags: [evm]
url: https://ethereum-magicians.org/t/minimal-upgradeable-proxies/20868
views: 240
likes: 3
posts_count: 1
---

# Minimal Upgradeable Proxies

## Latest ERC PR

https://github.com/ethereum/ERCs/pull/604

## Adoption

https://dune.com/vectorized/erc-7760-proxy-counts

## Related Work

An independent work has been done in:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xiaobaiskill/48/9799_2.png)

      [ERC-7229: Minimal upgradable proxy contract](https://ethereum-magicians.org/t/erc-7229-minimal-upgradable-proxy-contract/14754) [EIPs](/c/eips/5)




> Discussion thread for Add EIP: Minimal Upgradable Proxy Contract by xiaobaiskill · Pull Request #7229 · ethereum/EIPs · GitHub
> The Minimal Upgradable Proxy contract is a lightweight contract upgrade pattern designed to save gas costs while providing the ability to upgrade contracts.
> 1 Standard Proxy
> 1.1 evm opcode
> In the following EVM code, the PUSH0 instruction (EIP-3855) is used. As of 2023-06-23, the BSC chain does not support EIP-3855 yet.
> # store logic address to slot of proxy contract
> P…

See: [GitHub - xiaobaiskill/minimal-upgradable-proxy](https://github.com/xiaobaiskill/minimal-upgradable-proxy)

This proposal is based off earlier work by JT Riley:

https://github.com/jtriley-eth/minimum-viable-proxy

This scope of this proposal includes other variants of minimal ERC-1967 proxies that will benefit from standardization.

## Source Code

https://github.com/Vectorized/solady/blob/main/src/utils/LibClone.sol

https://github.com/Vectorized/solady/blob/main/src/utils/ERC1967Factory.sol

## Etherscan Automatic Verification

```auto
[ ] Transparent (20-byte factory address regular variant)
[ ] Transparent (14-byte factory address regular variant)
[ ] Transparent (20-byte factory address I-variant)
[ ] Transparent (14-byte factory address I-variant)
[x] UUPS (regular variant)
[ ] UUPS (I-variant)
[x] Beacon Proxy (regular variant)
[ ] Beacon Proxy (I-variant)
```

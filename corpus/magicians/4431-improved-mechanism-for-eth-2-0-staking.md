---
source: magicians
topic_id: 4431
title: Improved Mechanism for ETH 2.0 Staking
author: zhous
date: "2020-07-17"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/improved-mechanism-for-eth-2-0-staking/4431
views: 809
likes: 0
posts_count: 1
---

# Improved Mechanism for ETH 2.0 Staking

This topic really needs a big discussion.

https://github.com/DAism2019/EIPs/blob/master/EIPS/eip-2794.md



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2794)














####


      `master` ← `DAism2019:master`




          opened 11:18AM - 17 Jul 20 UTC



          [![](https://avatars.githubusercontent.com/u/1388904?v=4)
            zhous](https://github.com/zhous)



          [+10
            -10](https://github.com/ethereum/EIPs/pull/2794/files)







We really need your support. Yes, it's a big thing. :)












Our team have done some related codes:



      [github.com/naturaldao/SmartContracts](https://github.com/naturaldao/SmartContracts/blob/master/contracts/Factory.py)





####

  [master](https://github.com/naturaldao/SmartContracts/blob/master/contracts/Factory.py)



```py
# @dev Implementation of control contract
# @author radarzhhua@gmail.com
from vyper.interfaces import ERC20

# the contract of NDAO ERC20 token
contract NDAO:
    def mint(_to: address, _value: uint256): modifying
    def decimals() -> uint256: constant

# the exchange contract
contract Exchange:
    def setup(token_addr: address, ndao_address: address,
              token_amount: uint256): modifying

# the ICO contract
contract ICO:
    def setup(_name: string[64], _symbol: string[32], _decimals: uint256, _depositGoal: uint256,
```

  This file has been truncated. [show original](https://github.com/naturaldao/SmartContracts/blob/master/contracts/Factory.py)












      [github.com](https://github.com/naturaldao/DHonor)




  ![image](https://opengraph.githubassets.com/a4706e60d3c8b1409ab097955c75fedd/naturaldao/DHonor)



###



Token of Honor based one EIP-2569

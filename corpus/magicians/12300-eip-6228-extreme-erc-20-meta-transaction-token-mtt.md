---
source: magicians
topic_id: 12300
title: "EIP-6228: Extreme ERC-20(Meta-transaction Token, MTT)"
author: SamPorter1984
date: "2022-12-28"
category: EIPs
tags: [erc, gas, meta-transactions]
url: https://ethereum-magicians.org/t/eip-6228-extreme-erc-20-meta-transaction-token-mtt/12300
views: 840
likes: 0
posts_count: 1
---

# EIP-6228: Extreme ERC-20(Meta-transaction Token, MTT)

## Abstract

This standard proposes a solution in which meta-transaction fees are deducted directly from the user’ token transfer amount, no liquidity for keeper incentives required.

This EIP is based on these assumptions:

- That meta-transaction signatures need to be public in order to speed up blockchain adoption. The EIP assumes that token dApps will feature a public pool of signatures similar to Coinbase or Etherscan, which will resemble regular Ethereum transactions but with reduced user friction.
- Meta-transactions must become standard procedure when interacting with smart contracts.
- Gas efficiency is in no way less important when it comes to optimistic and zero knowledge roll-ups. If anything, lower network fees enable more automation, which is about to become essential in such a hyper-competitive industry.
- Full automation can easily be too costly for project funding. Therefore, meta-transactions fees should be deducted directly from the transfer amount.

An example:

Alice has never had a wallet before but is eligible for an airdrop on Arbitrum. All she needs to do is install a wallet, sign the data, and then she has airdrop tokens minus the keeper fee. She does not have to make any transactions or possess any ETH. She is not limited in any way more than Bob, who is transacting on his own. Alice can vote, stake, claim rewards, trade on Uniswap. In fact, she can do more than Bob, such as subscribing to staking rewards to get them automatically every month, a part of these rewards then automatically sent to pay her bills and support her favorite content creators.



      [github.com/SamPorter1984/EIPs](https://github.com/SamPorter1984/EIPs/blob/master/EIPS/eip-6228.md)





####

  [master](https://github.com/SamPorter1984/EIPs/blob/master/EIPS/eip-6228.md)



```md
---
eip: 6228
title: Extreme ЕRС-20
description: meta-transaction token (MTT)
author: Sam Porter (@SamPorter1984)
discussions-to: https://ethereum-magicians.org/t/eip-6228-extreme-erc-20-meta-transaction-token-mtt/12300
status: Draft
type: Standards Track
category: ERC
created: 2022-12-26
requires: 20
---

## Abstract

This standard proposes a solution in which meta-transaction fees are deducted directly from the user' token transfer amount, no liquidity for keeper incentives required.

This EIP is based on these assumptions:

- That meta-transaction signatures need to be public in order to speed up blockchain adoption. The EIP assumes that token dApps will feature a public pool of signatures similar to Coinbase or Etherscan, which will resemble regular Ethereum transactions but with reduced user friction.
```

  This file has been truncated. [show original](https://github.com/SamPorter1984/EIPs/blob/master/EIPS/eip-6228.md)

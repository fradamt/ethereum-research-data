---
source: magicians
topic_id: 11560
title: "EIP-20: should I emit Transfer event in this balance change?"
author: charlesxsh
date: "2022-11-01"
category: EIPs
tags: [solidity, events]
url: https://ethereum-magicians.org/t/eip-20-should-i-emit-transfer-event-in-this-balance-change/11560
views: 834
likes: 0
posts_count: 3
---

# EIP-20: should I emit Transfer event in this balance change?

```auto
function _transferStandard(
       address sender,
       address recipient,
       uint256 tAmount
   ) private {
       (
           uint256 rAmount,
           uint256 rTransferAmount,
           uint256 rFee,
           uint256 tTransferAmount,
           uint256 tFee,
           uint256 tTeam
       ) = _getValues(tAmount);
       _rOwned[sender] = _rOwned[sender].sub(rAmount);
       _rOwned[recipient] = _rOwned[recipient].add(rTransferAmount);
       _takeTeam(tTeam);
       _reflectFee(rFee, tFee);
       emit Transfer(sender, recipient, tTransferAmount);
}

function _takeTeam(uint256 tTeam) private {
       uint256 currentRate = _getRate();
       uint256 rTeam = tTeam.mul(currentRate);
       _rOwned[address(this)] = _rOwned[address(this)].add(rTeam);
}

```

For this line, `_rOwned[address(this)] = _rOwned[address(this)].add(rTeam);`

This code snippet is quite common among many ERC20 implementation (Does anyone know where it came from?), is this expected behavior or not?

According to the doc: [EIP-20: Token Standard](https://eips.ethereum.org/EIPS/eip-20), The transfer event MUST trigger when tokens are transferred. I assumed that this line of code represents the balance transfer from sender to the address(this). But it does not emit a Transfer event.

## Replies

**abcoathup** (2022-11-02):

They have coded a fee on transfer token.

These type of tokens can have unexpected consequences, see: [Incident with non-standard ERC20 deflationary tokens | by Mike McDonald | Balancer Protocol | Medium](https://medium.com/balancer-protocol/incident-with-non-standard-erc20-deflationary-tokens-95a0f6d46dea)

---

**charlesxsh** (2022-11-17):

Thanks for sharing this excellent blog. Besides this, I am wondering the whether or not the balance change should emit Transfer event in the above example!


---
source: magicians
topic_id: 3597
title: BigDecimal/BigInt for contracts
author: hiddentao
date: "2019-08-28"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/bigdecimal-bigint-for-contracts/3597
views: 1051
likes: 0
posts_count: 1
---

# BigDecimal/BigInt for contracts

I just came across the OpenZeppelin report on Compound, and in particular the note on how truncated division within Solidity can result in a borrower paying 0 interest on extremely small amounts (see https://blog.openzeppelin.com/compound-audit/amp/).

Made me think it would be good if there was a BigDecimal-like library for Solidity so that precise calculations could be made to avoid these sorts of issues. Then again, using a much higher precision than is necessary with uint256 would solve this (which is essentially what a BigDecimal lib would do, anyway).

Has anyone else had any thoughts on this?

EDIT: just found https://github.com/dapphub/ds-math thanks to @thomasbarkercom

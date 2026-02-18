---
source: magicians
topic_id: 5621
title: "EIP-3374: Predictable Proof of Work Sunsetting"
author: query0x
date: "2021-03-14"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-3374-predictable-proof-of-work-sunsetting/5621
views: 2274
likes: 0
posts_count: 2
---

# EIP-3374: Predictable Proof of Work Sunsetting

**Motivation**

Unnecessarily abrupt changes to the Ethereum ecosystem cause disruption and disharmony resulting in the disenfranchisement of community members while undermining stability, security and confidence.  While moves from Proof-of-Work to Proof-of-Stake will undoubtedly cause friction between those community members vested in either, all benefit from a measured, predictable transition.

This proposal:

1. Is issuance neutral.  There is no overall increase in mining rewards
2. Smooths the immediate impact of EIP1559 on mining economics reducing the likelihood of reactionary responses;
3. Introduces an ongoing, regular reduction in future mining rewards down to 1, effectively “sunsetting” POW and codifying the move to POS
4. Removes economic incentives for continued development of ASICs;
5. Allows the impacts of decreasing miner rewards to be measured and monitored rather than relying on conjecture and game theory, so adjustments can be made if necessary.
6. Brings us one step closer to world peace and a more harmonious Ethereum ecosystem.

**Implementation**

Sets the block reward to 3 ETH and then incrementally decreases it every block for 2,362,000 blocks (approximately 1 year) until it reaches 1 ETH.

**Rationale**

This proposal smooths the effect of EIP-1559 on mining economics, without affecting the fee burn or increasing total ETH issuance, and mitigates the risks and uncertainties that sudden changes to mining economics impart on network security.  Picking starting and ending block reward values that are equidistant from the current block reward rate of 2 ensures the impact of this EIP will be issuance neutral over the approximate one year time frame.  Temporarily raising the block reward to 3 blunts the initial impact of EIP-1559 and the continual reductions thereafter codify Ethereum’s move to POS by increasingly disincentivizing POW.  Importantly, this approach moderates the rate of change so impacts and threats can be measured and monitored.

## Replies

**Chris2** (2021-03-14):

My only suggestion would be that the 1 year period is too fixed. Any “sunset” should come in as goalposts between POW and POS are met. If a merge happens in 6 months we want the BR to be 1 five months in such that the merge isn’t a shock. Any fixed date places a burden on the dev team to achieve it and may delay the merge since now the dev team is forced to wait 12 months to not upset the community.

Any delay in the merge may cause a burden/security risk. It is much better to have an elastic block reward decrease that accommodates any accomplishments or delays that shorten/lengthen the merge. This also provides some financial incentive to reach these goalposts.


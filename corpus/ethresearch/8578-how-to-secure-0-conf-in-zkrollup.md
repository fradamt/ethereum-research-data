---
source: ethresearch
topic_id: 8578
title: How to secure 0 conf in ZKRollup
author: leohio
date: "2021-01-26"
category: Layer 2
tags: []
url: https://ethresear.ch/t/how-to-secure-0-conf-in-zkrollup/8578
views: 1026
likes: 0
posts_count: 1
---

# How to secure 0 conf in ZKRollup

To realize good UX in zkRollup applications, 0 conf by the aggregator is the simplest way to give the fast finality to their users at frontend.

Without that, users have to wait for the rollup tx finalizing on L1.

You can say it’s a centralized way to finalize if there’s no commitment obliged to aggregators.

Do you have any idea about the restrictions for aggregators?

I suppose one. It’s just an idea.

register public key of aggregator

=> user receive and preserve the signed receipt of the 0 conf transaction

=> user claim with the receipt, and prove the tx is not in the calldata by entry hash.

If there’s a better scheme, let us know.

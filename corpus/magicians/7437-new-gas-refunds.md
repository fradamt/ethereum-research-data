---
source: magicians
topic_id: 7437
title: New gas refunds
author: jessielesbian
date: "2021-11-09"
category: EIPs
tags: [gas]
url: https://ethereum-magicians.org/t/new-gas-refunds/7437
views: 633
likes: 0
posts_count: 1
---

# New gas refunds

Back then, gas refunds for SSTORE and SELFDESTRUCT are applied to both the base fee and the priority fee.

We should change the system so gas refunds for SSTORE and SELFDESTRUCT would only be applied to the base fee, not the priority fee. This can reduce the impact of gas refunds on miner revenues.

Also, instead of being concerned about gastokens filling up the state with junk, we should launch a native gastoken by the use of precompiles that gives gas refunds when burned to increase gas price stability and put an end to the ethereum gastokens crisis.

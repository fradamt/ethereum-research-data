---
source: magicians
topic_id: 10622
title: "EIP-5568: Revert Signals"
author: Pandapip1
date: "2022-09-01"
category: EIPs
tags: [erc, wallet, feedback-wanted]
url: https://ethereum-magicians.org/t/eip-5568-revert-signals/10622
views: 1878
likes: 0
posts_count: 4
---

# EIP-5568: Revert Signals

https://github.com/ethereum/EIPs/pull/5568

## Replies

**SamWilsn** (2022-09-06):

I think this EIP should define a reevaluate instruction. That seems super common.

How compatible is this with other systems that use revert reasons? I believe Gas Station Network uses something similar (but much simpler.)

---

**Pandapip1** (2022-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I think this EIP should define a reevaluate instruction.

I am working on a draft for this. To avoid special cases, it will be its own (very short!) EIP.

---

**Pandapip1** (2022-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> How compatible is this with other systems that use revert reasons? I believe Gas Station Network uses something similar (but much simpler.)

I can’t find the OpenGSN stuff, but I know that there are EIP-5289 (which I would update to use this new EIP) and EIP-3668 (which will be incompatible with this EIP).


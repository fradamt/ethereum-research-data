---
source: magicians
topic_id: 26019
title: "Proposal: Enhance EIP-7702 by Adding a Caller Field"
author: blade
date: "2025-10-30"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/proposal-enhance-eip-7702-by-adding-a-caller-field/26019
views: 32
likes: 0
posts_count: 1
---

# Proposal: Enhance EIP-7702 by Adding a Caller Field

By introducing a `caller` address field in the authorization data, this improvement ensures that the authorization can only be executed by a specific user.

This approach mitigates front-running risks and restricts authorization exclusively to trusted accounts. Users no longer need to worry excessively about being deceived, even if the contract contains hidden bugs.

While this solution does not address all potential issues, it confines the problem within a controllable scope. Users can manage risks by controlling the `value` passed during contract calls and conducting small-scale trial transactions.

After reviewing the discussions around EIP-7702, I haven’t found any related proposals. Admittedly, the original thread is quite lengthy, and I may not have examined it in its entirety. I’ve decided to create a new post to discuss this idea.

Looking forward to the discussion!

[eip-7702](https://eips.ethereum.org/EIPS/eip-7702)

[eip-7702-post](https://ethereum-magicians.org/t/eip-7702-set-eoa-account-code/19923/394)

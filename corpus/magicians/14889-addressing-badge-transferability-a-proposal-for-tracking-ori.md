---
source: magicians
topic_id: 14889
title: "Addressing Badge Transferability: A Proposal for Tracking Original Assignees"
author: sullof
date: "2023-06-30"
category: Magicians > Primordial Soup
tags: [token, soulbound, lockability, transferability, badge]
url: https://ethereum-magicians.org/t/addressing-badge-transferability-a-proposal-for-tracking-original-assignees/14889
views: 494
likes: 1
posts_count: 1
---

# Addressing Badge Transferability: A Proposal for Tracking Original Assignees

The topic of soul-bound tokens, badges, and identity tokens has been a subject of discussion for some time, particularly the question of whether or not a soul-bound token should be transferable. If so, how should this be accomplished and who should be authorized to do it (the issuer, for example)?

We’ve made substantial progress in addressing the fundamental issues related to lockability, thanks to several EIPs that have explored the problem from different angles ([EIP-5192](https://eips.ethereum.org/EIPS/eip-5192), [EIP-6892](https://eips.ethereum.org/EIPS/eip-6892), [EIP-6454](https://eips.ethereum.org/EIPS/eip-6454)).

However, one issue remains unresolved: the significance of a badge. If a badge is transferred, the recipient is not the original assignee. As a result, badges and soul-bound tokens are often viewed as inherently non-transferable.

After speaking with numerous people about this, Roy Liu and I devised a minimalistic solution that may already exist. If that’s the case, I haven’t come across it and would appreciate if someone could point it out to me.

Our proposition centers on the importance of the assignee - that is, the first wallet to receive the badge. To address this, we propose a minimalistic interface as follows:

```auto
interface ERC721Assigned {
    event AssignedTo(uint tokenId, address assignee);
    function assignee(uint tokenId) external view returns (address);
}
```

This interface tracks the original recipient of each token, irrespective of any subsequent transfers.

We’d love to hear your thoughts on this solution.

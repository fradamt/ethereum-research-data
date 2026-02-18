---
source: magicians
topic_id: 25850
title: "EIP-8045: Exclude slashed validators from proposing"
author: fradamt
date: "2025-10-17"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-8045-exclude-slashed-validators-from-proposing/25850
views: 78
likes: 1
posts_count: 4
---

# EIP-8045: Exclude slashed validators from proposing

Discussion topic for [EIP-8045](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-8045.md)

## Replies

**bbusa** (2025-10-17):

This would have helped reduce some of the chaos on holesky after the mass slashing. I’m in favor or having this EIP.

---

**rolfyone** (2025-11-03):

The one caveat I’d probably explicitly list is that if a proposer inside the lookahead is slashed that they won’t be removed from the rest of the stable lookahead period… I’m not sure the best way to word it…

Specifically, if the `state.proposer_lookahead` contains validator N more than once, and in that period the validator is slashed, we can’t alter the lookahead period to remove the second time that validator is selected to propose.

So we’re specifically not selecting proposers that are slashed when filling the proposer lookahead, I guess is the other way of stating that.

This does retain a small period for the problem to be possible but the probability should be fairly low. I just think there’s more value in keeping that proposer_lookahead stable than there is mutating something that is currently considered stable…

The proposed solution does basically implement it in this way, I’d just like to make sure we don’t try to ‘fix’ that potential scenario, because it’d get complicated for little value imo.

---

**fradamt** (2025-11-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rolfyone/48/14306_2.png) rolfyone:

> This does retain a small period for the problem to be possible but the probability should be fairly low. I just think there’s more value in keeping that proposer_lookahead stable than there is mutating something that is currently considered stable…
>
>
> The proposed solution does basically implement it in this way, I’d just like to make sure we don’t try to ‘fix’ that potential scenario, because it’d get complicated for little value imo.

Yeah, 100% wouldn’t want to try to fix that. I think there’s a lot of value in being completely sure of what the proposer sequence is (at least if there are no deep reorgs), versus having to handle the possibility of edge cases. And there is very little value in being sure that slashed proposers are *never* selected, at worst they’ll be selected once after slashing, because of being in the existing lookahead, and then never again.


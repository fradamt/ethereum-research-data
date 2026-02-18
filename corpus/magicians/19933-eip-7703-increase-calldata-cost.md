---
source: magicians
topic_id: 19933
title: "EIP-7703: Increase Calldata Cost"
author: wjmelements
date: "2024-05-08"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7703-increase-calldata-cost/19933
views: 1114
likes: 4
posts_count: 7
---

# EIP-7703: Increase Calldata Cost

https://github.com/ethereum/EIPs/pull/8529

replaces eip-7623 which is insecure

## Replies

**OlegJakushkin** (2024-05-15):

Dear [@wjmelements](/u/wjmelements):

Is there any practical analysis data of the past numbers? what this would bring to the ledger in practical terms? (e. g. you had it 4 times before now its 3 just because of assigned EIP number)

- How many TXs would have been affected in the last time range by such a change from all TXs in gas terms?
- How much would they increase in size?
- If it “allows a higher block gas limit” at the same time calldata price goes up and fills that gap - so what is expected to change?

---

**wjmelements** (2024-05-15):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/o/a88e57/48.png) OlegJakushkin:

> Is there any practical analysis data of the past numbers?

No. But anecdotally, builders are discriminating against large calldata transactions because they bring more delay-risk than the gas pays for.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/o/a88e57/48.png) OlegJakushkin:

> How many TXs would have been affected in the last time range by such a change from all TXs in gas terms?

all of the ones with calldata

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/o/a88e57/48.png) OlegJakushkin:

> How much would they increase in size?

I don’t understand your question.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/o/a88e57/48.png) OlegJakushkin:

> If it “allows a higher block gas limit” at the same time calldata price goes up and fills that gap - so what is expected to change?

Higher gas limit, lower gas prices, cheaper execution gas.

---

**OlegJakushkin** (2024-05-15):

> all of the ones with call-data
> (1) but how may are there in say a week with call data? (in occupied bock gas proportion to TXs without call-data)

> I don’t understand your question.
> say gas is space in a block - you increase call-data cost, then TXs with call data take more space in a block. Yet imagine people can not stop using that exact same TXs and call-data still is used in exactly in same volume. So how much that propotion in (1) would change?

---

**wjmelements** (2024-05-15):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/o/a88e57/48.png) OlegJakushkin:

> say gas is space in a block - you increase call-data cost, then TXs with call data take more space in a block. Yet imagine people can not stop using that exact same TXs and call-data still is used in exactly in same volume. So how much that propotion in (1) would change?

The proportion of gas used for calldata would increase if there is no change in behavior.

---

**sbacha** (2025-03-13):

How is this different than, oh i dont know [EIP-7623: Increase Calldata Cost - #32 by wjmelements](https://ethereum-magicians.org/t/eip-7623-increase-calldata-cost/18647/32) ?

*SELL ME THIS EIP*

---

**wjmelements** (2025-03-20):

EIP-7623 only charges additional gas for calldata conditionally. The EIP-7623 condition can be exploited for gas sheltering as I explain in that post.


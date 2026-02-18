---
source: magicians
topic_id: 24680
title: "EIP-7981: Increase access list cost"
author: Nerolation
date: "2025-06-27"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7981-increase-access-list-cost/24680
views: 146
likes: 3
posts_count: 7
---

# EIP-7981: Increase access list cost

Discussion topic for [EIP-7981](https://github.com/ethereum/EIPs/pull/9946)

This EIP aims to reduce the max possible block size. Economically deprecating 2930 AL could be done alongside EIP-7928, block-level access lists.

#### Update Log

- 2025-06-19: initial draft

#### External Reviews

None as of 1025-06-19

#### Outstanding Issues

None as of 1025-06-19

## Replies

**jochem-brouwer** (2025-08-23):

I have some minor comments on the EIP (looks good! Think it is also time to deprecate 2930 since it was essentially an escape hatch for any “stuck” contracts when 2929 was introduced years ago)

> Let access_list_nonzero_bytes and access_list_zero_bytes be the count of non-zero and zero bytes respectively in the serialized access list data (addresses and storage keys).

What is meant with “serialized” here? I find this confusing, is this the RLP-serialized access list (thus have to count each individual RLP byte) or is it the raw data of the slot (32 bytes) and address (20 bytes)?

> Storage key (32 bytes, typically mostly non-zero)

Is this true? I’d imagine that especially the super low slots are “popular” slots to access, which would mean that slots like 0x0, 0x1, 0x2… are rather popular on the ALs.

> Maximum Block Sizing

> With data pricing (assuming all non-zero bytes):

The max block size would use the zero slots to get the biggest block so this needs to be edited to reflect the actual maximum block size.

If we would not do the logic with zero/nonzero bytes we could then also “just” increase the address/storage access key cost, right? These costs should be equal to or higher than the calldata cost.

---

**Nerolation** (2025-08-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> What is meant with “serialized” here?

Yeah agree, will clarify that one.

Re storage slots. I expect most of them to be ERC-20 token mappings. So, even though most contract have entries in the first storage slots, we might see more non-zero values in practice. But this doesn’t matter that much anyway I think,

Zero bytes are well compressible, so, I think, we should be more worried about compressed sizes. For those, assuming random non-zero bytes get us close enough. The actual worst-case size is using ~63% of zeros, strategically mixed into the 37% non-zero bytes.

---

**ADMlN** (2026-01-06):

> The additional cost makes EIP-2930 access lists economically irrational for gas optimization, effectively deprecating their use while maintaining compatibility.

I agree that our goal should be to make 2930 access lists so expensive that there is no incentive to use them (because we get BAL in the next hard fork). But our goal is also to avoid protocol complexity whenever necessary. So this EIP confuses me: Why bother increasing the complexity of pricing rules of something no one is supposed to be using anyway? Wouldn’t it be much easier to just increase the flat cost of this deprecated feature WITHOUT adding any additional rules? Like just put a higher gas cost number that applies to every scenario. It is also a bit weird that this EIP from now on financially incentivizes mining contract addresses that include many zeroes.

---

**Nerolation** (2026-01-08):

Judging from the specs and tests, there’s really not much complexity attached, and it’s a fairly simple to reason about pricing rule that has already been used since Pectra (EIP-7623). This EIP, EIP-7981, just harmonizes how we treat data - now we don’t care if the data comes from ALs or from calldata anymore - which is reasonable.

Mining zero addresses (e.g. leading zeros) has always been beneficial in case you have to use those addresses in calldata, or in gas golfing strategies. Since ALs wouldn’t be economically rational to use anymore, it makes no sense to mine zero-byte addresses just for saving a bit of gas in the AL.

---

**gurukamath** (2026-02-05):

What is the rational behind charging the access list tokens at `TOTAL_COST_FLOOR_PER_TOKEN` while the call data tokens are charged at `STANDARD_CALLDATA_TOKEN_COST`?

---

**Nerolation** (2026-02-05):

No strong opinion on this one. Intuitively, since declaring data in the access lists doesn’t necessarily come with the actual storage access and could end up being “only data”, it makes sense to have it priced at the floor.

One could first check if the transaction *could* pay the floor, have it execute and afterwards decide if the AL should be priced differently or not - I considered this but we’re not using the AL anywhere after execution and it felt wrong + overly complex.

Simply using the relatively high price, thus economically deprecating them seems simplest.


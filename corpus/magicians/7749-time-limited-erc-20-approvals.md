---
source: magicians
topic_id: 7749
title: Time-limited ERC-20 approvals
author: vrypan
date: "2021-12-11"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/time-limited-erc-20-approvals/7749
views: 1419
likes: 2
posts_count: 7
---

# Time-limited ERC-20 approvals

This is a discussion thread for an informational EIP describing how token allowances can have a time-limit and auto-expire.

The basic idea is to extend approve() and allowance() in EIP-20 so that they use a _maxBlock parameter.

The proposal will be something like this:

approve becomes:

```auto
function approve(address _spender, uint256 _value, uint256 _maxblock) public returns (bool success)
```

and allowance() returns 0 if current block > _maxblock.

The idea is that most users pay attention to what happens when they approve an allowance, but forget about them after some time. This proposal will make allowances auto-expire, saving users the hassle to deal with old approvals and also spare them the gas needed to cancel them.

Is this something worth submitting an EIP?

## Replies

**vrypan** (2021-12-11):

Maybe, in order to maintain backwards compatibility with ERC-20, a new `function approveWithLimit()` could be introduced, and the definition of `approve()` can be left unmodified.

---

**wschwab** (2021-12-12):

Welcome!

This is an interesting idea, but I’m going back and forth around it personally. [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612). 2612 introduces a way to leverage signed messages to create an approval, and it includes a `deadline` as one of its parameters, which on one hand doesn’t solve the problem you’re talking about, since the deadline is only how long a possessor of the signed message has to call `permit`, but once they’ve called `permit` within the deadline, they have a regular non-expiring approval. otoh, the fact that 2612 uses signed messages makes it convenient to use both the permit and the transfer of the permitted amount simultaneously, mitigating the risk.

So I can’t say I’m coming out strongly in favor or against, but figured I’d at least offer this as some context.

---

**vrypan** (2021-12-12):

Thank you, very much, [@wschwab](/u/wschwab). I will study 2612.

---

**vrypan** (2021-12-13):

I have drafted an EIP based on the above idea. Should I wait for some feedback or reviews before submitting a PR?

https://github.com/vrypan/EIPs/blob/master/EIPS/eip-draft_time_limited_token_allowances.md

---

**wschwab** (2021-12-14):

I think it’s a personal choice - you’re welcome to PR if you want, you can also take some extra time, learn about 2612, and decide if you still want to do it

---

**lukehutch** (2022-06-14):

[@vrypan](/u/vrypan) I like the idea, but the expiration should be a Unix time based deadline (`block.timestamp`, number of seconds) rather than a block number based deadline, because EIP2612 and other standards use time-based deadlines, and block mining rate is variable. (Block mining rate may also change dramatically at some point in the future due to proof of stake or some other factor, who knows.)


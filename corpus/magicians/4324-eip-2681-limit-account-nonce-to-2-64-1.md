---
source: magicians
topic_id: 4324
title: "EIP-2681: Limit account nonce to 2^64-1"
author: axic
date: "2020-05-29"
category: EIPs > EIPs core
tags: [core-eips, validation]
url: https://ethereum-magicians.org/t/eip-2681-limit-account-nonce-to-2-64-1/4324
views: 4334
likes: 4
posts_count: 26
---

# EIP-2681: Limit account nonce to 2^64-1

Discussion topic for [Add EIP for limiting account nonce by axic · Pull Request #2681 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2681)

---

[@jpitts](/u/jpitts): adding some background from the EIP here.

This is motivated by Eth1.x / Stateless Ethereum discussions, more specifically discussion around the [“witness format”](https://github.com/ethereum/stateless-ethereum-specs).

Introducing a restriction would allow storing the nonce in a more optimised way.

Additionally it could prove beneficial to transaction formats, where some improvements are potentially sought by at least three other proposals.

Lastly this facilitates a minor optimisation in clients, because the nonce no longer needs to be kept as a 256-bit number.

## Replies

**holiman** (2020-05-30):

I think the EIP should be officially finalized (not requiring a hardfork)

---

**axic** (2020-06-01):

Do you mean to remove the “if hard fork” and replace it with “these rules apply from the genesis on mainnet” ?

---

**holiman** (2020-06-01):

Yup, that’s what I mean. That we’ll just retroactively say “This was always so” and bob’s your uncle.

---

**MicahZoltu** (2020-09-06):

I’m with [@holiman](/u/holiman) on this, can we just remove the mention of the hardfork and merge this as a retroactive specification?  Is it even *possible* for any nonce to be greater than 2^61 right now?  Worst case napkin math scenario, someone was able to increment a nonce for 1 gas, for 10M blocks, at 12.5M gas per block.  That would only get you to about 2^46, nowhere near 2^64.

---

**axic** (2020-09-06):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I’m with @holiman on this, can we just remove the mention of the hardfork and merge this as a retroactive specification? Is it even possible for any nonce to be greater than 2^61 right now?

Totally share the same sentiment.  The EIP has this in backwards compatibility:

> There is no account in the state currently which would have a nonce exceeding that value.  Need to double check, but would be very surprised.

I do not have access to a full client right now, less to an archival one, but it would be nice to check if by some freak accident there was any such account at any point of time. If geth always had that limitation of 64-bit then the answer is no. [@holiman](/u/holiman)?

---

**axic** (2020-09-06):

Could we consider limiting this further to `2^32-1`? That would require a change in go-ethereum and possibly other clients, but it is also unreachable in practice (would cost 90.014 Eth with 10 gwei gas price via external transactions). Though I could potentially see some exchange account reaching that if they started in 2015 ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

The benefit reducing this limit further could show with transaction formats: it would be possible to serialise the nonce as a fixed-size field, because 4 bytes with zeroes likely would be worth the reduced complexity of having some more complicated encoding scheme (such as RLP).

---

**holiman** (2020-09-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> If geth always had that limitation of 64-bit then the answer is no. @holiman?

That is correct. There is no such account

In total, there are somwhere around 600M transactions in the history of ethereum. `2^32-1` means that there’s a max nonce of `4300M`. Meaning that if one single account made all transactions from genesis to somewhere around block `50M`, then it could potentially reach it.

However, changing it to to a fixed-size field is a *massive* change, since it affects the rlp-encoding of every account in the trie, aswel as the rlp-encoding of all transactions. Unless I misunderstand what you mean…?

---

**axic** (2020-09-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> However, changing it to to a fixed-size field is a massive change, since it affects the rlp-encoding of every account in the trie, aswel as the rlp-encoding of all transactions. Unless I misunderstand what you mean…?

This EIP does not propose to change the merklization rule (“RLP encoding of the accounts in trie”) or the transactions encoding. However future EIPs proposing changes in those could benefit from the limit to `2^32-1`.

---

**holiman** (2020-09-07):

Yeah ok… I think `2^32-1` is within the theoretically reachable segments, whereas limiting to full 64-bit is on the like “millions of years” - unreachable segment. So the original suggestion makes definite sense, the latter suggestions seems to me to be not as clear-cut.

---

**MicahZoltu** (2020-09-09):

I weakly support 64-bit if we don’t really care about the size.

If we do care about the size, then I weakly support 32-bit as I don’t think we are realistically going to run out anytime soon and we *can* change the size later if it ever becomes a real problem.

---

**MicahZoltu** (2020-12-02):

I propose we limit to 2^52.  As mentioned, 2^32 is within the theoretically reachable range while both 2^64 and 2^52 are both in the “not actually possible” range.

2^52 is special because unsigned integers up to 2^52 can fit into a 64 bit floating point number with exact precision.  This is meaningful in JavaScript especially where integers are not available.  While this argument in favor of 2^52 is fairly weak, I see no viable counter-argument in favor of 2^64, so I think even a weak argument should sway us here.  ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=9)

---

**matt** (2020-12-05):

I’m not sure why js libraries can’t simply use unsigned integers? We’re a long ways from 2^52 - hopefully those language specific things will be sorted out by then!

---

**MicahZoltu** (2020-12-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> I’m not sure why js libraries can’t simply use unsigned integers?

JavaScript doesn’t have native integers (until very recent versions).  Historically, JS has *only* had doubles.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> We’re a long ways from 2^52 - hopefully those language specific things will be sorted out by then!

These arguments all seem to support 2^52, not 2^64.  Generally speaking, if there is no need to specify a larger limit then the smaller should be chosen as it is **MUCH** easier to increase the limit than to decrease the limit later.  If we do manage to get to 2^52 we can trivially increase it to 2^64 with a spec change (like this one) at that time.

**Is there *any* argument in favor of 2^64 as the limit?**  So far everything seems to be along the lines of “2^52 is just about the same” not “2^52 will cause problems/difficulty/complexity”

---

**matt** (2020-12-06):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Is there any argument in favor of 2^64 as the limit? So far everything seems to be along the lines of “2^52 is just about the same” not “2^52 will cause problems/difficulty/complexity”

My main argument is that `uint64` is a basic type in the languages that the most popular clients are written in. It’s also just generally a much more widely accepted basic type. We’re a long ways from both 2^52 and 2^64 - so it’s a matter of which party needs to use a native type that is “out-of-spec”. I believe we should cater towards client developers / languages rather than javascript applications.

---

**MicahZoltu** (2020-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> My main argument is that uint64 is a basic type in the languages that the most popular clients are written in.

This change doesn’t assert the width of the nonce for serialization or anything, it merely asserts that the value is invalid if it is greater than `2^x`.  In either case, every client will need to write something like `assert(nonce <= 2^x)` so I don’t see the advantage to client developers to choose a native integer width.

---

**MicahZoltu** (2020-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> I believe we should cater towards client developers / languages rather than javascript applications.

While I don’t think it matters for *this* discussion, I believe there are far more Ethereum JavaScript developers out there than other language developers so I’m not sure that catering toward core devs is necessarily the right choice for the ecosystem.  It may be in some cases, but I don’t think necessarily all cases.

---

**matt** (2020-12-09):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> This change doesn’t assert the width of the nonce for serialization or anything, it merely asserts that the value is invalid if it is greater than 2^x. In either case, every client will need to write something like assert(nonce <= 2^x) so I don’t see the advantage to client developers to choose a native integer width.

You’re not wrong, however, my belief is that it is more natural for core developers to think about things in terms of overflows than arbitrary limits.

As we’ve both pointed out, we’re a long ways from both 2^52 and 2^64. It’s unlikely that any client will put an `assert` in for either in the near future, so my preference is to choose the constant that is more inline with their current implementations and generally more ubiquitous. The precision of floating point in javascript is something that shouldn’t be an issue in ~10 years. In the meantime, I would prefer that javascript applications ensure that the nonce is less than 2^52 and use native floating points.

---

**MicahZoltu** (2020-12-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> In the meantime, I would prefer that javascript applications ensure that the nonce is less than 2^52

We agree entirely on this point.  The best way to ensure that is to standardize it.  ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**chfast** (2021-03-21):

1. The max value should be 2^52-1 so only 52 bits of the binary representation are ever used. From the current wording in the spec it looks the 2^52 is also valid nonce value. Only the 2^52+1 causes a failure.
2. The rationale section still mentions 2^64.

---

**matt** (2021-03-21):

[@chfast](/u/chfast) do you have a preference on limiting to `2^64-1` vs `2^52-1`?


*(5 more replies not shown)*

---
source: magicians
topic_id: 3224
title: "EIP-1985: Sane limits for certain EVM parameters"
author: axic
date: "2019-04-30"
category: EIPs
tags: [evm, core-eips, eip-1985]
url: https://ethereum-magicians.org/t/eip-1985-sane-limits-for-certain-evm-parameters/3224
views: 7214
likes: 14
posts_count: 43
---

# EIP-1985: Sane limits for certain EVM parameters

Discussion topic for


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-1985)




###

Details on Ethereum Improvement Proposal 1985 (EIP-1985): Sane limits for certain EVM parameters

## Replies

**holiman** (2019-05-07):

> Potentially however, certain contracts could fail at a different point after this change is introduced, and as a result would consume more or less gas than before while doing so.

Can you examplify? Because afaict, these changes (which I think I agree with) would have *no* practical consequence, so I’m curious what I’m missing.

---

**axic** (2019-05-09):

I think that may be a remnant of an older version where more parameters were limited. Perhaps what we could do is place a calculation of how big of a gas limit could potentially allow larger `CALLDATASIZE`, `CODESIZE`, etc. for it make any difference.

`(4_294_967_295 + 1) * 4 = 17_179_869_184` gas could allow a larger than 32-bit calldata (32-bit + 1 to be exact) to be passed.

Hence the limits introduced have no practical effect on contract developers.

---

**axic** (2019-05-20):

Clarified the pull request.

---

**axic** (2019-05-20):

In 2016, [EIP-106](https://github.com/ethereum/EIPs/issues/106) proposed a similar limits for gas.

---

**Arachnid** (2019-05-23):

A few thoughts:

- The address limit should probably be expressed differently; eg - “the upper 96 bits shall always be unset”, since addresses are not conventionally expressed as integers.
- Given these invariants have never been violated, why only activate them at a certain block? Without a fixed fork block, clients can simply agree to implement these changes, even retroactively, without causing a hard-fork.
- All of these constants would be clearer if expressed in hexadecimal.

---

**axic** (2019-06-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Given these invariants have never been violated, why only activate them at a certain block? Without a fixed fork block, clients can simply agree to implement these changes, even retroactively, without causing a hard-fork.

I think that makes sense, but perhaps there are some subtleties regarding this in clients ([@holiman](/u/holiman) and [@karalabe](/u/karalabe) probably has some opinions). For example private chains could in theory have gas limits which allow exceeding the proposed limits – arguable not very useful since the above quoted 17 billion gas limit likely would translate into a 1700 second (~30 mins) block time.

---

**holiman** (2019-06-26):

I agree about making it retroactive. I doubt there is any private network anwhere that has violated these, and if so, well, we can’t support that

---

**axic** (2019-06-26):

If we enable this retroactively, what is the best process?

1. Enforce these rules in a client and sync mainnet
2. Marking this EIP final
3. Announcing it publicly
4. ?

I also think we need to clearly specify which check happens first in the client, for example in the case of arguments to `CALL` with a really large input size, what would happen first:

- gas calculation for memory expansion resulting in out of gas
- out of gas due to invalid parameter

Technically both have the same outcome, but tracing would differ.

---

**holiman** (2019-06-26):

Yes, those steps seem reasonable. As for `CALL` – my intuition says mem expansion happens in an earlier step, but I’ll have too look it up.

Anyway, I can PR this for geth and put on one of our benchmarking nodes. I expect most of these rules to already be in place, but perhaps only implicitly.

---

**axic** (2019-06-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> Anyway, I can PR this for geth and put on one of our benchmarking nodes.

That would be great, thanks!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> I expect most of these rules to already be in place, but perhaps only implicitly.

Yes, I think all of this enforced via gas limits already. Would be nice if we could enforce it prior to gas calculation.

---

**holiman** (2019-06-28):

There is really only one thing which may cause problems here, afaict (and this issue might need to be included in ‘Security Considerations’ for this EIP).

Currently geth and parity allows a full `uint64` as an uncle timestamp. This means that someone can intentionally mine an uncle `U` with timestamp `2^64-1` , and then mine a regular block within 7 blocks, and include `U` in the uncle set.

If we redefine the allowed timestamp as max `2^ 63-1`, then we’re open for a consensus-attack between updated and non-updated clients.

There are two ways out from this dilemma

1. Use 2^ 64-1 (uint64) as max timestamp, not 2^ 63-1 (int64)
2. Ensure that we implement the change at a particular block B (hard fork). Later, if we see that nobody did ever execute this attack prior to B, we can “undo” the hardfork and retroactively apply the fork – basically pretending that the rule was always there.

I personally think option 1 is the best route, but I’m not really up to speed with what kinds of problems that leads to on platforms without native support for `uint64`

---

**holiman** (2019-06-28):

Here’s how it is in geth right now:

## Already enforced

- block.gasLimit <= 2^63-1 enforced by https://github.com/ethereum/go-ethereum/blob/master/consensus/ethash/consensus.go#L262
- block.gasUsed <= 2^63-1 implicitly enforced: https://github.com/ethereum/go-ethereum/blob/master/consensus/ethash/consensus.go#L267
- address is internally represented by 20 bytes.

## Not enforced

- tx.gasLimit is defined as uint64 in geth. Can be safely capped as EIP suggests.
- block.number is defined as a big.Int, but validation checks that it is only 1 away from the parent: here. Can be safely capped at like EIP suggests.
- block.timestamp – see comment above, cannot be safely capped like EIP suggests.

## Other

- buffer size has no constraints, but practically I don’t see any possible realistic impact of changing this to max at int32. Can be safely capped like EIP suggests.

---

**axic** (2019-06-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> Use 2^ 64-1 ( uint64 ) as max timestamp, not 2^ 63-1 ( int64 )

I think it would be acceptable given we do not need to represent timestamps prior to 1970 in the block headers.

However, for best standards compatibility I’d be in favor of striving for `int64`.

---

**chfast** (2019-06-28):

Isn’t this an issue already if someone mines an uncle block with timestamp `2^64`?

---

**chfast** (2019-06-28):

We are investigating possibility of applying this retroactively.

The remaining 2 comments have been addressed in https://github.com/ethereum/EIPs/pull/2153.

---

**chfast** (2019-06-28):

As you can guess, I’m very much in favor of `int64` limit for timestamp.

Third option to go here is to allow negative values for `int64` timestamps in EVM execution. This will allow executing EVM code by mapping values above `2^63-1` to negative numbers (they are binary equivalent anyway).

Can you create uncle blocks with negative timestamps in current implementations?

---

**axic** (2019-06-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> I agree about making it retroactive.

Thinking about this more, I really hope we can do it retroactively to reap the benefits for evm2wasm or in the proposed Eth1 EE on Eth2.

---

**holiman** (2019-06-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> Isn’t this an issue already if someone mines an uncle block with timestamp 2^64 ?

Well, if they do, it’s not an ‘issue’ now. However, if some clients cap it lower, then we *will* have an issue. So there’s no ‘safe’ rollout of that change, other than hardfork-then-retroactive, because going full retroactive means there a window where it can be used as an attack

> Can you create uncle blocks with negative timestamps in current implementations?

RLP has no ‘native’ support for negative integers, and geth defines timestamps as unsigned. So basically there’s no way geth (nor parity afaict) would interpret a timestamp as negative.

---

**shemnon** (2019-06-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> I personally think option 1 is the best route, but I’m not really up to speed with what kinds of problems that leads to on platforms without native support for uint64

I think the best way to ensure clients deal with it is to have some reference test cases where the relevant numbers are `unit64` but not `int64`.   So some timestamp after 2038 should do that.

To that end we should also see if test cases can be written where the first “insane” value is tested.  This would only work if clients fail in a sensible fashion that the harness can detect.

---

**chfast** (2019-07-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> So some timestamp after 2038 should do that.

I think you meant the year 292277026596.


*(22 more replies not shown)*

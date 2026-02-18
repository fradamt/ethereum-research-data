---
source: magicians
topic_id: 6072
title: "EIP-3521: Reduce access list cost"
author: matt
date: "2021-04-21"
category: EIPs
tags: [gas]
url: https://ethereum-magicians.org/t/eip-3521-reduce-access-list-cost/6072
views: 2950
likes: 6
posts_count: 8
---

# EIP-3521: Reduce access list cost

EIP text here: [EIP-3521: Reduce access list cost](https://eips.ethereum.org/EIPS/eip-3521)

Inspired by this comment: [EIP-2930: Optional access lists - #31 by AusIV](https://ethereum-magicians.org/t/eip-2930-optional-access-lists/4561/31)

## Replies

**holiman** (2021-04-22):

Generally lgtm, but since this EIP wants to fix it properly, I do have some nitpicks

> Treat the first occurrence of tx.to in an access list as calldata for gas accounting purposes. Do not charge ACCESS_LIST_ADDRESS_COST for it. Storage keys underneath the address are unaffected.

I think it would be good to clarify exactly what “as calldata” means. The `address` is the full `20` bytes, but should that address also be subject to 0-byte counting? Seems like it would be simpler to *not* do that, but instead just charge `16x20`=`320`, So instead of paying `2400` for it, you’d pay `320`.

Or in other words (which avoid the use of ‘first occurrence’), I would describe it something like this:

> If tx.to is part of the 2930-declared access list (i.e. before adding the freebies), deduct 2080 from the tx cost.

---

**matt** (2021-04-22):

Thanks for the feedback. The main reason for wording "as `calldata`" was to try and inherit the calldata calculation. Although I generally prefer the way you’ve worded it, introducing a constant `320` cost is just another protocol parameter to keep track of. If the cost of `calldata` changes, we also have to worry about changing this parameter. This is a relatively minor concession though, so it’s probably fine to move forward with the constant.

---

**wjmelements** (2021-04-23):

As someone who has many zero-bytes in their addresses, I agree with the inheriting of the calldata calculation. I would also support extending it to the other unbounded-size transaction parameters, and other duplicated entries in the list.

---

**holiman** (2021-04-23):

One more thing I’d like to comment about this EIP in general.

This EIP solves one problem, making it easier to decide “should I include address X” or not. However, it should be pointed out that this problem is a bit more difficult than that, and we can’t really solve it.

Say for example that a user calls an `eth_getAccesslist`, and gets a list of all addresses/slots that are touched during exeution. Let’s say the user knows that the accesslist shaves of `10%`, and “by default” always does this and includes the access list.

Now, from the time this estimation was done, to the time it was included in a block, things may have changed. It might be some defi bid on some order that was picked up by someone else, or some auction that was just closed.

In the “regular tx” case, the tx would fail pretty early. The contract would look up what it needs to look up, find that the order is now invalid, and exit, having touched only a few slots and made no external calls.

So in this case, a full “access list tx” with N addresses and M slots would *still* pay for all those accesses that never happened.

Just throwing it out there, that the decisiion of whether to include an access list in a transaction or not to is not necessarily an easy question to answer. It was *required* to handle broken flows, but it’s probably not a good default – it might be later, if the discrepancy between pre-declared and runtime-added costs is enlarged further.

With that said, I don’t really see this EIP as particularly important (as in, no urgency in getting it in), since it only solves one already pretty simple part of a more complex problem.

---

**matt** (2021-04-23):

Yep, that’s also a good thing to generally keep in mind.

---

**nventuro** (2021-11-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> Just throwing it out there, that the decisiion of whether to include an access list in a transaction or not to is not necessarily an easy question to answer. It was required to handle broken flows, but it’s probably not a good default – it might be later, if the discrepancy between pre-declared and runtime-added costs is enlarged further.

While this is true in the general case, most applications can reason about expected transaction flow to a great extent, making this problem much less severe. For example, any Uniswap or Balancer transaction will read the balances unconditionally even if the transaction ends up reverting, as the limit checks happen after.

And in any case, the app is always free to choose whether to optimize for success or reduce revert cost.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> With that said, I don’t really see this EIP as particularly important (as in, no urgency in getting it in), since it only solves one already pretty simple part of a more complex problem.

It *does* solve that problem however, and it is the only way the problem can be solved (meaning this is not something client code can take care of). Access lists being ‘hard’ to use right does not mean that it is fine to leave them in a quasi-broken state.

I see this as an important change as the usefulness of access lists is otherwise greatly reduced in a huge number of cases due to `tx.to` typically playing a very big role in the overall transaction: losing out on savings on all the storage slots it touches due to what seems like an oversight in the EIP2930 spec feels wrong.

Not to mention that 2930 has this big ‘gotcha’ that is far from obvious, and can easily result in people not realizing the ‘25 slots’ rule and paying extra fees as a result.

---

**nventuro** (2021-11-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> Although I generally prefer the way you’ve worded it, introducing a constant 320 cost is just another protocol parameter to keep track of. If the cost of calldata changes, we also have to worry about changing this parameter. This is a relatively minor concession though, so it’s probably fine to move forward with the constant

Note that EIPs are being proposed to do exactly this: [EIPs/EIPS/eip-4488.md at a12d2155f51319461b6a18ff9fc924c5d7e29c71 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/a12d2155f51319461b6a18ff9fc924c5d7e29c71/EIPS/eip-4488.md#specification)


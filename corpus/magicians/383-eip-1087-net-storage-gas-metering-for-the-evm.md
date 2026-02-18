---
source: magicians
topic_id: 383
title: "EIP-1087: Net storage gas metering for the EVM"
author: Arachnid
date: "2018-05-17"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1087-net-storage-gas-metering-for-the-evm/383
views: 7227
likes: 27
posts_count: 46
---

# EIP-1087: Net storage gas metering for the EVM

I’ve written up an EIP proposing a change in the way we do gas metering for storage operations in the EVM, reducing costs in many cases where gas costs don’t reflect actual costs.

[Draft here](https://eips.ethereum.org/EIPS/eip-1087).

Feedback appreciated!

## Replies

**AtLeastSignificant** (2018-05-17):

For clarity, the proposal aims at doing:

- Zero -> zero = 200 * # changes
- Zero -> non-zero = 20k + (200 * # of changes)
- Non-zero -> different non-zero = 5k + (200 * # of changes)
- Non-zero -> zero = 5k + (200 * # changes)

I think that last case is written correctly, though your examples don’t explicitly cover it.

---

**Arachnid** (2018-05-17):

The last case is -5k + (200 * # changes), because it retains the existing refund for deleting a storage slot.

---

**MicahZoltu** (2018-05-17):

Perhaps this isn’t the right place to have this discussion, but I have always felt like the last case should be significantly more than a 5k refund.

---

**Arachnid** (2018-05-17):

I kind of agree, but think that a gas refund is going to be an ineffective way to encourage deleting storage elements regardless of its size - especially with the limitation that it can’t be more than half the gas used.

---

**MicahZoltu** (2018-05-17):

Agreed.  I’m guessing your argument is to “not change storage refund here and instead try to solve the storage rent problem elsewhere”?

---

**Arachnid** (2018-05-17):

Yup, absolutely. All this EIP aims to do is to make gas costs for storage changes more accurately reflect the costs borne by nodes - and make storage practical for a wider variety of use-cases as a result.

---

**AtLeastSignificant** (2018-05-17):

Then a negative gas cost transaction is possible?

---

**Arachnid** (2018-05-17):

No; refunds are limited to half the gas consumed.

Gas refunds due to this EIP *could* be applied separately to the existing refund counter, since they don’t have the same concerns that lead to the above limitation. In that case, negative gas still wouldn’t be possible, since refunds in this EIP are always less than the gas consumed.

---

**veox** (2018-05-17):

Although somewhat superficial, I think it’s worth mentioning that the current cost for an `SLOAD` operation is 200 gas. So, there is no condition under which a write-without-read would be cheaper than a read-without-write.

---

The “A->B->C balance transfer” examples are somewhat difficult to understand at a glance. In particular,

> A balance transfer from account A to account B followed by a transfer from B to C, with all accounts having nonzero starting and ending balances, will cost 5000 * 3 + 200 - 4800 = 10400 gas, down from 20000.

implies that the value transferred in A->B and B->C is the same: presence of `-4800` means that the value of some slot hasn’t changed.

`(5000 + 5000) + (200 + 5000) - 4800` seems more accesible to me.

---

It may be worth including a “contract clears a single non-zero slot” example. As I understand, currently a refund would be 10000 gas (`5000 - 15000 = -10000`); per the EIP, the refund would be lowered to 5000 gas (`5000 - 10000 = -5000`).

---

**Arachnid** (2018-05-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/veox/48/10_2.png) veox:

> Although somewhat superficial, I think it’s worth mentioning that the current cost for an SLOAD operation is 200 gas. So, there is no condition under which a write-without-read would be cheaper than a read-without-write.

That’s right. I picked the cost of 200 gas based on SLOAD, because the EVM has to read the data off disk to check if the data being stored differs from the data already there.

This could be tweaked a bit - for instance, the refunds could be left as they are, but the cost for ‘dirty’ writes reduced further, since they don’t each require a disk lookup.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/veox/48/10_2.png) veox:

> implies that the value transferred in A->B and B->C is the same: presence of -4800 means that the value of some slot hasn’t changed.
>
>
> (5000 + 5000) + (200 + 5000) - 4800 seems more accesible to me.

Fair enough.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/veox/48/10_2.png) veox:

> It may be worth including a “contract clears a single non-zero slot” example. As I understand, currently a refund would be 10000 gas (5000 - 15000 = -10000); per the EIP, the refund would be lowered to 5000 gas (5000 - 10000 = -5000).

This shouldn’t change - at present, setting a nonzero slot to zero costs the standard 5k gas for the write and returns a 10k refund at the end.

---

**MicahZoltu** (2018-05-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> This shouldn’t change - at present, setting a nonzero slot to zero costs the standard 5k gas for the write and returns a 10k refund at the end.

According to the yellow paper, the refund for clearing state is `15000`, not `10000`.  This means that `5000` for the set `-15000` for the clear results in a net cost (today) of `10000` gas.

---

**Arachnid** (2018-05-18):

Oops, my mistake. I’ll fix that along with any other feedback from All Core Devs today.

---

**fulldecent** (2018-05-20):

I generally endorse this EIP.

However, the constant 200 cost for tracking an non-contiguous map of dirty-bits is different than the “memory cost function”. Maybe the 200 cost should be higher and non-linear.

---

**Arachnid** (2018-05-22):

Nodes already incur a fixed cost per mutated element - and they can likely rely on this mapping rather than having to maintain a separate mapping of dirty bits.

---

**jbaylina** (2018-05-23):

Personally I think this should be:

1.- Normal read/write from the cache: 10

2.- Loading a variable for the first time into the cache: 200 (ether because of a SLOAD or a SSTORE onto a non-cached variable).

3.- 20000/5000 For the first SSTORE different to the initial value.

4.- At the end:

if the initial and the last value is the same, refund the 20000/5000 if they were charged previously for this variable.

if the initial value!=0 and the final value==0  then refund -15000

As you can see, normal sload/sstore on cached variables should be treated very much as normal memory operations.  Loading a variable into the cache 200 (like an actual SLOAD).  For the SSTORE, it is very much the same idea you propose.

---

**mcdee** (2018-05-26):

I’m all for this EIP, as it brings gas costs more in line with real server impact, but has there been any thought as to the knock-on effect on block validation times and uncle rates as a result of this change?  With the reduction in “wasted” gas here a block will have more real work going on, and will take longer to transmit and validate (due to holding more transactions).  As a result, might a block gas limit reduction be required at the point that this goes live?

---

**MicahZoltu** (2018-05-27):

That (block gas limit) is a choice miners can make after the change is live.  I don’t think that the change is catastrophic enough to warrant any special handling in the gas limit.

---

**mcdee** (2018-05-27):

They can make the change post-hoc but it could have a significant impact in the meantime.  Having some sort of awareness of the impact of net storage gas metering would give an idea of if this is an issue, and if so how much of an issue.  Has there been any attempt to rerun historic blocks with the new metering to gauge the impact of this change?

---

**Arachnid** (2018-05-27):

That wouldn’t give an accurate view of the impact, since people will adapt to this change.

However, if this were a problem, we’d already see it - this change reduces the overcharging of gas for no-op storage writes down to something resembling the actual costs; it shouldn’t be any worse than an existing contract that does lots of non-storage ops that are already billed accurately.

---

**mcdee** (2018-05-27):

[@Arachnid](/u/arachnid) unless I’m misunderstanding something this change would result in what is today being a full block becoming a block that is only partially full (due to the reduction in gas cost for storage) and as a result means that for a given block gas limit a block after this proposal was implemented will have more transactions, hence take longer to transfer and longer to validate.

> this change reduces the overcharging of gas for no-op storage writes down to something resembling the actual costs

which is my point.  If 8 million gas worth of transactions today becomes (for example) 4 million gas worth of transactions after this proposal is implemented it has the same network impact as doubling the block gas limit without implementing this proposal.  I doubt that anyone would consider the latter to be a sensible idea.

Again, I’m all for this proposal and have railed against incorrect gas costs for storage in the past.  I just worry that it might have an impact on the network and was wondering if that had been examined/quantified.


*(25 more replies not shown)*

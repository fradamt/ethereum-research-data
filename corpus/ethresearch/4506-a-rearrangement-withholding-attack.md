---
source: ethresearch
topic_id: 4506
title: A rearrangement + withholding attack
author: ldct
date: "2018-12-07"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/a-rearrangement-withholding-attack/4506
views: 3162
likes: 9
posts_count: 6
---

# A rearrangement + withholding attack

This post describes a potential attack on certain implementations of plasma cash. Thanks to [@gakonst](/u/gakonst) for review.

Suppose for concreteness we have the following exit procedure.

1. Anyone can exit their coin by providing the last two transactions in the coin’s ownership history (ie. the coin they are exiting C and its parent P(C)). This sets a deadline T at some number of blocks into the future (say T = block.number + 80600) and initializes a counter h = 0 representing the number of unaswered challenges.
2. Challenges can be made before T; a type (i) and type (ii) challenge cancels the exit; a type (iii) challenge is written to storage and h is incremented. [1]
3. At any time, h can be decremented by providing a response to a type (iii) challenge (which is then deleted)
4. An exit with h = 0 can be finalized when block.number  > T.

Then the following attack is possible:

1. Alice signs a transaction to Bob and provides the signature to the operator.

[![A](https://ethresear.ch/uploads/default/optimized/2X/e/ed15e8407fc1f8fee3e33217a0eca420b39a74db_2_666x500.jpeg)A4608×3456 3.3 MB](https://ethresear.ch/uploads/default/ed15e8407fc1f8fee3e33217a0eca420b39a74db)

1. The operator includes a double-spend from E, some spends of that, includes the spend to B among them, and withholds all the blocks

[![B](https://ethresear.ch/uploads/default/optimized/2X/5/575554081d21371c04fceac212319cba6c019e5c_2_666x500.jpeg)B4608×3456 3.57 MB](https://ethresear.ch/uploads/default/575554081d21371c04fceac212319cba6c019e5c)

1. Eve exits coin C
2. The only challenge possible is a type 3 challenge with coin A
3. Eve waits until the block height is greater than T to reveal B, cancelling the challenge
4. It is too late to start a new exit with B

Note that similar attacks are possible against many variants of the exit game round structure; if we require that h be set to 0 before T then B can be revealed at block height T-1. The general attack is to reveal B “as late as possible”. An equivalent statement is that the exit game requires 5 inclusion proofs in the worst case (and not 4 as a naive analysis might conclude), or 4 rounds (instead of 3), and that the round structure must support this.

Two ways to support this include explicitly extending the exit game resolution deadline, or allowing “limbo” transactions in cancellations.

Footnotes

[1] see https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/ for definitions of type 1, type 2 and type 3 challenges

## Replies

**DZariusz** (2018-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> Two ways to support this include explicitly extending the exit game resolution deadline, or allowing “limbo” transactions in cancellations.

There is also third way, but for that you need another approach for implementation. You can read more here: https://ethresear.ch/t/luciditys-plasma-cash-easy-and-more-efficient/

---

**nginnever** (2018-12-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/dzariusz/48/2928_2.png) DZariusz:

> There is also third way, but for that you need another approach for implementation. You can read more here: https://ethresear.ch/t/luciditys-plasma-cash-easy-and-more-efficient/

From my understanding you use `targetBlock` parameter in the tx to prevent this scenario. In this case `targetBlock` should always be set to `currentBlock+1` so there is no “room” for an operator to place double spends under data withheld conditions?

If that is the case then will there be blocks where a max capacity is reached and transactions would have to be invalidated and resigned?

---

**keyvank** (2018-12-09):

I think the issue can be resolved by having a challenge-response-time along with a challenge-time where challenge-response-time is less than the challenge-time. E.g. we can have have a challenge-time of 7 days, which means you have 7 days to submit a type (iii) challenge on that coin and a challenge-response-time of 3 days which means you can respond a challenge in only 3 days or the exit is canceled.

So in step 5 of your example, Eve should respond in 3 days, and in step 6 we would have 4 more days for creating a new exit on block B.

---

**snjax** (2018-12-10):

I think the most kind of things become much simpler if we provide force including/priority increasing procedure with lesser challenge time then time for exit procedure.

#### Priority increasing game (it is like ’s special exit)

1. Exiter publish the transaction on mainnet plasma contract
2. Anybody can challenge the submission by presenting spend of inputs or outputs of the transaction
3. If the submission is unchallenged, we consider the transaction included into the block of youngest input of the transaction

#### Exit game

1. Exiter publish the exit output
2. Anybody can challenge the output for spend or non-inclusion
3. Anybody can present an output with an earlier priority. If this output is unchallenged by spend, exit (1) is challenged.

With some development it useful to provide complex transactions like multisig atomic swaps.

---

**DZariusz** (2018-12-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/nginnever/48/1936_2.png) nginnever:

> If that is the case then will there be blocks where a max capacity is reached and transactions would have to be invalidated and resigned?

There will be always a space for `Tx` because there are unique deposit IDs, so nobody can take your spot. But of course there probably will be some cases when i.e. you will be too late for `targetBlock`. I can imagine client-operator communication will be like this:

client send Tx for `targetBlock` → operator confirm → the end,

OR

client sent Tx for `targetBlock` → operator reject and return proof of exclusion → resend with `targetBlock+1` → operator confirm → the end.

And yes, you understood correctly, there will be no room for rearrange attack. However there probably (we do not implemented it yet) is a way to be more flexible and allow to include `Tx` for `currentBlock +1 or +2`. There will be possible of one gap and with one gap you can only attack with double spend, and double spend is easy to challenge.


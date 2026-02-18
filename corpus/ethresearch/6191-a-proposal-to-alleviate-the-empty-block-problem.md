---
source: ethresearch
topic_id: 6191
title: A proposal to alleviate the empty block problem
author: kladkogex
date: "2019-09-24"
category: EVM
tags: []
url: https://ethresear.ch/t/a-proposal-to-alleviate-the-empty-block-problem/6191
views: 3279
likes: 1
posts_count: 9
---

# A proposal to alleviate the empty block problem

If you look at ETH block explorer you see that some pools like Spark Pool are producing empty blocks.

The reason for this is they start mining  the block once hash is available, without having to wait for or distribute the actual transactions. Since they do not have the previous block transactions, they can not include transactions in a block without the risk of a double spend.

A simple proposal to alleviate this would be to allow transactions that specify exactly the target block id. A transaction like that would have to be included in the specific block that has the requested block ID.

Arguably, miners could include these transactions without risking a double spend, therefore filling up blocks which are currently empty. Transactions like this would arguably be less convenient, but much cheaper in terms of gas price.

## Replies

**adlerjohn** (2019-09-24):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> allow transactions that specify exactly the target block id.

This does not guarantee the transaction is valid if it were to be included in a new block at that height, only that it would be invalid were it to be included in a block at a different height.

This proposal also fails to understand the fundamental reason why mining empty blocks on Ethereum is different than on Bitcoin: Ethereum blocks include a state root, so [rewards and collected fees must be committed to in the block header](https://github.com/ethereum/go-ethereum/blob/aca39a6498030470c3fe3feb8d761e9cb0d88e93/consensus/ethash/consensus.go#L636), which requires having validated the previous block.

https://twitter.com/jadler0/status/1173271689116995587

---

**kladkogex** (2019-09-24):

Interesting … Why are they mining the empty blocks then ?

---

**kladkogex** (2019-09-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> This does not guarantee the transaction is valid if it were to be included in a new block at that height, only that it would be invalid were it to be included in a block at a different height.

But still it does guarantee that the transaction was not included before …

---

**adlerjohn** (2019-09-24):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Why are they mining the empty blocks then

¯\_(ツ)_/¯

There could be a number of reasons.

- After validating the previous block, mining pool operators can create an “empty” block template that only includes payment to themselves (i.e., no transactions, but a new state root), and quickly send this to workers (hashers) before starting to add transactions to their block (which, once done, will be sent to hashers). If a hasher gets lucky and finds a nonce satisfying the difficulty for this empty template, then the pool might as well propagate the block.

A hasher might have a networking issue and doesn’t receive an update block template, and continues mining on the empty block template.

Software bug(s).
The mining pool operator is evil and irrational and refuses to add transactions to some of their blocks, but only some.

The list goes on.

---

**adlerjohn** (2019-09-24):

Transaction invalidity is not only the result of duplication. That’s the most boring and uninteresting case. Others include, but are not limited to

- Different transaction, same sender, same nonce.

---

**hkalodner** (2019-09-24):

Another possible reason is that smaller blocks will propagate faster through the network faster. I’d bet that in a race with two blocks mined simultaneously, the smaller block wins more often (no clue if this is correct based on uncle statistics). If that’s the case, then there’s a legitimate tradeoff between the extra fees you get making a bigger block and slight increase in the chance your block will be orphaned.

---

**tkstanczak** (2019-09-26):

https://twitter.com/Bloxy_info/status/1177219850462277637?s=20

---

**kladkogex** (2019-09-30):

I think 2 and 3 are definitely not probable causes.  There may be something in 1 but it is to o vague.

These people lose like $60 per block, there must be a reason …

Looks like  we have no clue WTF is going on  ![:imp:](https://ethresear.ch/images/emoji/facebook_messenger/imp.png?v=14)![:imp:](https://ethresear.ch/images/emoji/facebook_messenger/imp.png?v=14)![:imp:](https://ethresear.ch/images/emoji/facebook_messenger/imp.png?v=14)


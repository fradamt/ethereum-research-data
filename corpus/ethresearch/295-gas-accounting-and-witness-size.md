---
source: ethresearch
topic_id: 295
title: Gas accounting and witness size
author: vbuterin
date: "2017-12-07"
category: Sharding
tags: []
url: https://ethresear.ch/t/gas-accounting-and-witness-size/295
views: 2976
likes: 1
posts_count: 5
---

# Gas accounting and witness size

We want to have a gas payment mechanism where the base gas charged for a transaction has a component which is approximately linearly proportional to the witness size. In the earlier 1-layer account model, this was accomplished fairly easily by charging a fixed amount of gas (eg. 3000) per account, plus a fixed amount of gas per byte in the account’s code and storage. In the 2-layer model, this is not as good an idea, because the actual witness size corresponds to the logarithm to the size of the storage tree, which is not available to the EVM, and even if it were there is always the possibility of attacks that try to create maximally inefficient trees that have witnesses of size linear in the size of the tree. To avoid all of these issues, charging directly for witness size seems maximally prudent.

The question is, how?

Here are a few alternatives:

### Charge the validator

- How it works: charge the validator for each byte in the witness, or alternatively for the number of state objects in the witness. Allow transaction senders to provide an additional gas stipend of their choice, and leave it to validators to only accept transactions that include a stipend large enough to pay for their access list
- Pros: simple at consensus layer
- Cons: requires validators to implement a more complex transaction sorting algorithm than before

### Charge gas based on “necessary witness”, calculated in real time

- How it works: when processing each transaction in a block, calculate the number of state trie node needed to access all of the accounts from the current state (ie. the pre-state of the transaction). Charge N gas per state trie node.
- Pros: does not require fancy validator transaction sorting logic
- Cons: requires knowing the pre-state of the transaction, making parallel execution and cross-transaction caching impossible

### Charge gas based on “necessary witness”, calculated based on block pre-state

- How it works: when processing each transaction in a block, calculate the number of state trie node needed to access all of the accounts from the pre-state of the block. Charge N gas per state trie node.
- Pros: does not require fancy validator transaction sorting logic, and allows parallel execution. Also, aligns well with actual costs (since the witness in the block must be based on the block pre-state, not the mid-state)
- Cons: more complex and ugly (though not too ugly; it’s already the case that witness validation for every transaction must be done at the start of block execution; this just adds a step to witness validation that computes a witness data cost for each transaction)

So far I lean slightly toward the first or the third, but there may be other approaches that we have not yet considered.

## Replies

**JustinDrake** (2017-12-08):

Below are some ideas to shoot for charging a fixed amount of gas. This would keep things simple at the consensus layer. It would also make gas estimation simpler, and would be one less thing for application developers to worry about (micro-)optimising.

1. Find or build an accumulator with constant-sized witnesses. Constant-sized witness accumulators are not uncommon in the literature; see for example the table on page 14 here where most of the accumulator schemes considered have constant-sized witnesses.
2. If the above is not possible, then find or build an accumulator without the worst-case-linear-witnesses attack that the current state trie suffers from. If the worst case for witness size is logarithmic, it’s likely charging a fixed amount of gas would be fine. The reason is that the state trie will never hold more than, say, 2^100 elements and a concrete cost of ~log(2^100) is small enough to charge everyone for.
3. Similar to how the stack has a maximum size of 1024, the size of witnesses can be capped at the consensus layer. Alternatively, state trie insertions can be charged exponentially in the size of the depth in the trie, which would put an effective cap on the witnesses size.

---

**vbuterin** (2017-12-09):

> The reason is that the state trie will never hold more than, say, 2^100 elements and a concrete cost of ~log(2^100) is small enough to charge everyone for.

Strongly disagree! That basically means that we would have to overcharge ~10-100x for SLOAD/SSTORE in the normal case, which would really harm applications. My goal here is specifically to charge less for super-small tries (eg. contracts which only have 1-10 data fields) and more for super-humungous tries.

> Find or build an accumulator with constant-sized witnesses.

I generally want to steer clear of using fancy accumulators at protocol level, as I have the goal of making the base protocol depend only on information theory and SHA3 as cryptographic assumptions. That said, you can totally make your own contract that uses some fancy accumulator scheme, and it’ll be *almost* first-class (almost because you won’t get the benefit of miners auto-updating the witness if multiple actors send a transaction to modify the same accumulator at the same time).

---

**JustinDrake** (2017-12-17):

You make good points regarding avoiding overcharging applications and avoiding adding cryptographic assumptions at the protocol level. (Having said that, I wouldn’t rule out the possibility of a constant-sized-witnesses accumulator based only on information theory and hashing, unless there’s a good argument to be made that such an accumulator cannot exist.)

In the context of miner-updated witnesses, we need to be mindful of users being victims of targeted front-running by miners (or other users) that create maximally inefficient trees to push up gas consumption, and possibly even trigger out-of-gas exceptions. This attack is amplified if we go with the pre-state approach. The reason is that a miner can try to grow a maximally inefficient tree with, say, 1000 transactions *in a single block* and still pay minimal gas for the large mid-state witnesses. In the context of [putting witnesses in the transaction’s miner data](https://ethresear.ch/t/account-abstraction-miner-data-and-auto-updating-witnesses/332), the init script that constrains the witnesses can place an upper bound on witness sizes as a mitigation.

---

**vbuterin** (2017-12-18):

> In the context of miner-updated witnesses, we need to be mindful of users being victims of targeted front-running by miners (or other users) that create maximally inefficient trees to push up gas consumption, and possibly even trigger out-of-gas exceptions.

Agree! Though with one caveat: when blocks are full (ie. now), there’s fairly little incentive to try to make transactions cost *more* gas; every unit of gas used by one transaction is a unit of gas not used by another. Furthermore, attacks to create inefficient trees for DoS purposes have been possible since day 1, and last year’s DoS attacker seems to have not pursued this attack vector. So I personally am not *too* worried, though it’s definitely something to keep in the back of our minds.


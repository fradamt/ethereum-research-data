---
source: ethresearch
topic_id: 1703
title: Per period committee snapshot
author: hwwhww
date: "2018-04-11"
category: Sharding
tags: []
url: https://ethresear.ch/t/per-period-committee-snapshot/1703
views: 4050
likes: 6
posts_count: 10
---

# Per period committee snapshot

### Recap

A follow up of [A minimal sharding protocol that may be worthwhile as a development target now](https://ethresear.ch/t/a-minimal-sharding-protocol-that-may-be-worthwhile-as-a-development-target-now/1650/)

In that post, Vitalik illustrated a stub scheme for the basic committee mechanism that could be the testing backbone before we have a more stable specification of the protocol design.

There are two emitting-log-only functions (I renamed/reorder the parameters):

1. add_header(shard_id, chunk_root, period) returns bool: anyone can call this function at any time. The first header to get included for a given shard in a given period gets in, all others don’t. This function just emits a log. Returns True on success.
2. submit_vote(shard_id, chunk_root, period) returns bool: Sampled notaries call this function to submit a vote. This function just emits a log. Returns True on success.

And since the notaries have to know if they’re sampled committee members, they need to use message call to invoke a function which is similar to the outdated `get_eligible_collator`:

- get_committee(shard_id, period) returns a list of addresses:  use the last block hash h before this period as the seed. Selecting notary_pool[sha3(h) % notary_pool_size], notary_pool[sha3(h + 1) % notary_pool_size], .... notary_pool[sha3(h + (COMMITTEE_SIZE - 1)) % notary_pool_size] notaries from notary_pool.

This function is also a stub before we have a certain RNG mechanism.

In this scheme, most calculations happen in client side. Shard clients have to query SMC receipt log to decide which collations are included in the canonical shard chain.

Here are some descriptions of this scheme: [Minimal sharding protocol · Issue #539 · ethereum/py-evm · GitHub](https://github.com/ethereum/py-evm/issues/539)

### Problem in full sync

When the shard clients want to sync with the shard, before the client calculates the votes, they have to check who are the selected committee members via calling `SMC.get_committee(shard_id, period)`. But by the time, `notary_pool_len` may be already changed because some notaries registered or deregistered. So the return value from `SMC.get_committee(shard_id, period)` may be different from the real selected committee that was generated right after the period started.

### Possible solutions

#### Solution 1 - client side maintaining notary_pool

In Vyper implementation, we already have logs for updating notary pool:

```python
RegisterNotary: __log__({index_in_notary_pool: int128, notary: address})
DeregisterNotary: __log__({index_in_notary_pool: int128, notary: address, deregistered_period: int128})
ReleaseNotary: __log__({index_in_notary_pool: int128, notary: address})
```

During the full sync, make the client also **lookup every `RegisterNotary` and `DeregisterNotary` log and sample the “committee” off-chain**. So when the client checks the votes, they will know they should sample with which committee.

- Pros:

No extra gas cost.

Cons:

- Higher client-side complexity.
- Lack of a trustworthy committee list snapshot on-chain. How do clients apply other fast sync mechanisms?

#### Solution 2 - on chain checking with adding receipt logs and costing a lot gas cost for adding header

1. Add one storage in SMC: last_period: public(int128) logs the period of the most recent success add_header message.
2. Add one check in  SMC.add_header(shard_id, chunk_root, period) :

```python
def add_header(shard_id, chunk_root, period) -> bool:
    assert last_period
Cons:

- High gas cost for proposer to invoke sampling
COMMITTEE_SIZE :=135 notaries and log them.

---

I think solution 2 is bad and but very trivial. Solution 1 is better if the trend is moving most calculation off-chain.

Since right now, the implementation might be just a quick fix for the stub scheme, I’d like to know which solution would be more compatible with the future scheme integration. Or any other solution can fix this problem more perfectly. ![:grinning:](https://ethresear.ch/images/emoji/facebook_messenger/grinning.png?v=9)

## Replies

**NicLin** (2018-04-11):

Maybe sampling mechanism and solution 2 can be together modified to take in additional information(`index`) to calculate voter’s eligibility in O(1) computation.

```auto
def get_committee(shard_id, period, index) -> bool:
    return notary_pool[sha3(h+index) % notary_pool_size]
```

```auto
def submit_vote(shard_id, chunk_root, period, index) -> bool:
    ...
    committee = SMC.get_committee(shard_id, period, index)
    assert committee == msg.sender
    ...
```

---

**vbuterin** (2018-04-11):

Instinctively on-chain checking seems more agreeable. It’s only ~5000 gas per vote to change a storage slot, and then the status could just all be kept on-chain.

The way I’d implement it with on-chain checking is to have a single storage variable that represents a bitfield of who has voted and who has not, with the last byte representing a counter of total number of eligible notaries that voted. So you really do only need to change and check one storage slot with each vote.

---

**vbuterin** (2018-04-11):

Another approach is that each proposal could include the hash of the previous, so if you validate the last one you’re implicitly proxy-validating the entire chain up until that point.

---

**hwwhww** (2018-04-11):

So with this solution:

1. The notaries check if they are sampled and get the index by using message-call to invoke SMC.get_committee with O(log(n)) times, where  0  int128 function to do the iteration as the origin get_committee function, but returns index now.
2. It doesn’t fix the problem of what if the notary_pool_size changing during this period. For example:

After block 9, notary_1 and notary_3 call the check_committee function and know they are sampled as the committee member of the next period.
3. notary_1 votes at block 10.
4. notary_2 deregisters at block 11 and notary_pool_size is changed.
5. notary_3 votes at block 12. The SMC.get_committee returns a different result from what it was at block 10.

---

**jamesray1** (2018-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/hwwhww/48/599_2.png) hwwhww:

> notary_pool[sha3(h) % notary_pool_size], notary_pool[sha3(h + 1) % notary_pool_size], … notary_pool[sha3(h + (COMMITTEE_SIZE - 1)) % notary_pool_size]

Looks similar to RANDAO++! https://www.reddit.com/r/ethereum/comments/4mdkku/could_ethereum_do_this_better_tor_project_is/d3v6djb/. More: https://vitalik.ca/files/randomness.html, [GitHub - zweicoder/RNGesus: Secure, trustless, distributed Random Number Generation](https://github.com/zweicoder/RNGesus).

---

**hwwhww** (2018-04-11):

Wow, I see. So I think this storage slot is reset by the eligible (the first) proposer of this period in `SMC.add_header()`?

---

**jamesray1** (2018-04-11):

What if `degister`ing a notary doesn’t `release` them from the `notary_pool` until after the `notary_lockup_period` which is set at deregistration? You could make it so that the `release` happens after the end of one period and before the next, but that will increase time to finality or block/collation times.

---

**hwwhww** (2018-04-11):

#### Solution 3 - maintaining vote counting and head collation on-chain

If we can move vote counting in-chain, the committee size problem could be solved by maintain `period_notary_pool_len` in storage:

- period_notary_pool_len represent notary_pool_len that will use for sampling current period
- notary_offset represent the variation of notary_pool_len during the current period. (Might be negative number)

> p.s. there’s still a notary_pool_len which represents the real length.

The `period_notary_pool_len` will be updated when the first time SMC is called with transaction **per period**, includes:

1. register_notary
2. deregister_notary
3. add_header

Then we can apply [@NicLin](/u/niclin) 's voting checking.

1. When the notaries try to do lookahead right after the period starts, they use notary_pool_len = period_notary_pool_len + notary_offset.
2. For the on-chain voting, using period_notary_pool_len in contract.

- Pros:

Less on-chain gas spending for the proposer than Solution 2.
- Cons:

When the case that index out of range, this seat will be given up.
- If add_header becomes off-chain in the future scheme, it will be tricky again.
- Only the notary pool being snapshotted, so it’s possible that one notary_1 deregisters and another notary_2 registers and takes the empty slot from notary_1 during one period. If there’s slashing condition for do-nothing notary, the innocent notary_2 will be penalized?

---

#### Summary of Solution 3 +  's bitfield counting:

1. Add one storage in SMC: last_period: public(int128) records the period of the most recent success add_header message.
2. Add a storage variable current_vote: public(bytes32):

First bytes31: bitfield of who has voted and who has not. Each bit represent the iterating number in the get_committee function.
3. Last byte:  a counter of the total number of eligible notaries that voted
4. Add one period_notary_pool_len in storage to represent the notary_pool_len at the time of that the period just starts.
5. Add a SMC.settle_current_notary_len() function to settle period_notary_pool_len:

```python
def settle_current_notary_len() -> int128:
    self.period_notary_pool_len += self.notary_offset
    self.notary_offset = 0
    self.last_period = current_period
    return self.period_notary_pool_len
```
6. Modify SMC.register_notary function:

If self.last_period  bool:
    return msg.sender == self.notary_pool[sha3(h + index) % self.period_notary_pool_len]
```

Another version for  the notary to do lookahead message call only and it returns index if result >= 0:

```python
def lookahead_eligible_notary(shard_id, period, notary_pool_len) -> int128:
    for index in range(self.COMMITTEE_SIZE):
       if msg.sender == self.notary_pool[sha3(h + index) % notary_pool_len]
           return index
    return -1
```
13. Modify SMC.submit_vote function:

Checks the eligibility with SMC.check_eligible_notary(shard_id, period, index)
14. Updates current_vote:

Set the bit of index  to 1
15. Increase last byte by 1
16. If current_vote >= 2/3  COMMITTEE_SIZE, update head collation info on-chain.

---

**jamesray1** (2018-04-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/hwwhww/48/599_2.png) hwwhww:

> If there’s slashing condition for do-nothing notary, the innocent notary_2 will be penalized?

You could have a log or some other mechanism to track that a slashing condition applies to `notary_1`, or deduct it from zer balance. You could have erasure codes or other fraud proofs if needed.


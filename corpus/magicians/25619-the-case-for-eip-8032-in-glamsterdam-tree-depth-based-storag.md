---
source: magicians
topic_id: 25619
title: "The case for EIP-8032 in Glamsterdam: Tree-Depth-Based Storage Gas Pricing"
author: gballet
date: "2025-09-29"
category: Uncategorized
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/the-case-for-eip-8032-in-glamsterdam-tree-depth-based-storage-gas-pricing/25619
views: 231
likes: 6
posts_count: 8
---

# The case for EIP-8032 in Glamsterdam: Tree-Depth-Based Storage Gas Pricing

## Summary (ELI5)

This proposal makes it progressively more expensive to store data in contracts that already have lots of storage. Think of it like a progressive tax on storage: small contracts pay normal fees, but contracts storing massive amounts of data pay exponentially more for each additional storage operation.

**Why it matters:** Ethereum’s state is growing unsustainably, making it harder and more expensive to run nodes. This threatens decentralization.

**Who benefits directly:** Node operators and the overall network health benefit from reduced state growth. Users benefit from a more sustainable and decentralized network long-term.

## Detailed Justification

### Primary Benefits

- State Growth Mitigation: Creates economic pressure against unbounded state expansion, directly addressing one of Ethereum’s most pressing scalability challenges
- Improved Node Accessibility: Slower state growth means lower hardware requirements for node operators, preserving decentralization
- Market-Based Incentives: Aligns storage costs with actual long-term network burden rather than one-time gas fees

### Secondary Benefits

- Spam Reduction: Makes it economically infeasible to use Ethereum as cheap permanent storage for non-critical data
- Developer Efficiency: Encourages more thoughtful state management and efficient contract design
- Future-Proofing: Creates a framework that can be adjusted as network conditions evolve

### Why Now?

- Scalability Some large contracts have an impact on the block processing time.
- Technical Maturity: We now have sufficient understanding of state growth patterns to design targeted solutions. Paired with EIP-2926 - and a potential future eip targeting account creation - there is a good coverage of mechanisms to disincentivize state growth.

### Why This Approach vs Alternatives?

**Versus Flat Fee Increases:**

- Doesn’t penalize small/medium contracts or normal usage
- Targets actual problem actors (massive state consumers)
- More politically feasible as it doesn’t affect most users

**Versus State Rent:**

- Lower implementation complexity
- No breaking changes to existing contracts
- One-time payment model preserved (no ongoing rent management)

**Versus State Expiry Alone:**

- Preventative rather than reactive
- Immediate impact on state growth rate
- Simpler to reason about for developers

## Stakeholder Impact

### Positive Impact

**Node Operators:**

- Reduced hardware requirements growth
- Reduced block execution time

**Regular Users & Small dApps:**

- No impact for contracts below activation threshold (~8GB)
- Better network performance long-term

**Protocol Sustainability Advocates:**

- Direct action on state growth problem
- Market-based solution aligning with Ethereum’s economic model

### Negative Impact

**Large State Consumers:**

- Impact: Significantly higher costs for contracts with massive storage
- Mitigations:

High activation threshold protects legitimate use cases
- Gradual rollout allows time for adaptation
- Alternative storage solutions remain viable

**Trade-offs:** Some legitimate but inefficient use cases may need to migrate or optimize

**Existing Large Contracts:**

- Impact: Cost increases for storage operations
- Mitigations: Optional depth field means existing contracts start from 0
- Trade-offs: Necessary to avoid grandfathering in problematic contracts

## Technical Readiness

No prototype currently exists, but its implementation should be straightforward as it’s just about adding and maintaining a single field in the account header.

## Security & Open Questions

### Known Security Considerations

**Cross-Contract Storage:** Apps might distribute storage across multiple contracts to avoid penalties, but at the cost of a call, which will mitigate the impact of this approach.

### Open Questions

**Parameter Tuning:**: What are optimal values for `EXP_FACTOR` and `LIN_FACTOR`?

## Replies

**fradamt** (2025-10-02):

Would the future affected users not be able to use a different contract architecture to get around this somehow, e.g. splitting storage over multiple contracts? Basically a contract-sybil attack

---

**niran** (2025-10-09):

This proposal will be a big improvement for L2s, where state is significantly underpriced. However, the main pain point so far hasn’t been state size on disk, it’s been state root calculation time. The proposal gives us the ability to tune linearly and exponentially, which we can always use to reduce storage utilization. But when state root calculation is the issue, we’d be throttling usage more severely than we need to as a contract’s storage size increases.

I think adding another term to the formula, `LOG_FACTOR * account.depth`, would give chain operators the ability to tune for state root calculation when needed. This will also help L1 as the gas limit increases and the block time decreases.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fradamt/48/15693_2.png) fradamt:

> Would the future affected users not be able to use a different contract architecture to get around this somehow, e.g. splitting storage over multiple contracts? Basically a contract-sybil attack

When state root calculation is the bottleneck, this is desired behavior that the `LOG_FACTOR` would encourage. When state size on disk is the bottleneck, I think we’d want the constant cost to dominate so splitting contracts would have little benefit.

---

**benaadams** (2025-10-25):

Recent change in EIP-8032 to count from depth makes it more interesting and I think elevates some of my implementation concerns with depth

Also moves it away from being dependent on the underlying data structure which causes inflexibility

---

**jochem-brouwer** (2025-10-26):

Heya! I saw the EIP got updated and it now is changed from using the tree depth to using the storage size of the target contract. I’ll leave some thoughts here ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12) ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

I think the EIP should be updated not to check for accounts with non-empty `codeHash` but instead for non-empty `storageRoot`.

It is possible to create contracts which, in initcode, set storage, but do not deploy any code. Another example which is more relevant here is a 7702-delegated account which sets storage in the EOA but later clears the 7702-delegation again (the `codeHash` is now empty). Via the current scheme an EOA could thus bloat the EOA storage, once the sweeping begins clear the 7702-delegation and once the sweep has passed it can set it to any 7702-delegation of choice. The new slots will be accounted for, but not the old slots, which the EOA gets for free.

The EIP mentions that the “size” field is optional. This should be specified, otherwise we get consensus bugs. Let’s increase the RLP list size of the account from 4 to 5 - if there is `0` storage to be written, the fifth index (1-based) of the list is thus empty bytes.

In the definition of delta, v_0 and v_1 are not defined.

I wanted to note that if `TRANSITION_MAX_ACCOUNTS` and `TRANSITION_SLOTS_PER_BLOCK` are not choosen high enough, it is possible that bloating the state with accounts/storage could stall the transition process, but this is actually not the case, as an attacker cannot choose an address “at will”. If the attacker could target certain addresses and slots (it cannot, because storage keys are hashed, and contract addresses are derived from a hash also) then this would be possible, but this is not the case.

I feel that we should also investigate if there are more things we want to storage during this scan, so we do not have to do this again in the future. For instance, writing contract size to the account RLP would also be beneficial.

I could see some nasty edge cases in this EIP, especially with other system contracts writing storage, and also how the transient storage address itself should be treated here by the transition system.

---

**weiihann** (2025-10-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> I think the EIP should be updated not to check for accounts with non-empty codeHash but instead for non-empty storageRoot.

Good catch, thanks!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> I feel that we should also investigate if there are more things we want to storage during this scan, so we do not have to do this again in the future. For instance, writing contract size to the account RLP would also be beneficial.

I agree, if we do it together with EIP2926 then the transition cost is amortized.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> and also how the transient storage address itself should be treated here by the transition system.

Can you elaborate on this?

---

**jochem-brouwer** (2025-10-27):

> and also how the transient storage address itself should be treated here by the transition system.

It should read “transition storage address” (thus the account at `TRANSITION_REGISTRY_ADDRESS`). I am wondering if there are specific cases (which we should test) which are somewhat nasty, for instance the trie sweeper stopping at the transition storage address. The slot which holds the “counter” could be reset to 0, which thus deletes that storage. I wonder if there are cases where the transition registry address does not write the correct storage count value to the trie. (For instance 2 instead of 3).

So this would be the test case where the `cursor_account_hash` after a sweep is set to `TRANSITION_REGISTRY_ADDRESS`, and validating that for `TRANSITION_REGISTRY_ADDRESS` in all cases the storage count is written correctly.

---

**niran** (2025-11-07):

I think the updated formula `constant_sstore_gas(addr, slot) + LIN_FACTOR * ceil_log16(account.storage_count)` addresses my desire for a factor that takes storage root calculation costs into account (presumably `O(log(storage_count))`), but isn’t `LIN_FACTOR` a misnomer now?


---
source: ethresearch
topic_id: 22989
title: "Ethereum's Leaky Gas Tank: Unveiling 13 Costly Gas Model Inconsistencies"
author: hzysvilla
date: "2025-08-28"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/ethereums-leaky-gas-tank-unveiling-13-costly-gas-model-inconsistencies/22989
views: 480
likes: 11
posts_count: 7
---

# Ethereum's Leaky Gas Tank: Unveiling 13 Costly Gas Model Inconsistencies

# 13 Gas-model inconsistencies in Ethereum

This post summarizes 13 inconsistencies in Ethereum’s gas model.

All the symbols come from the Ethereum Yellow Paper (esp. Appendix G. Fee Schedule).

---

## 1. The external transaction does not incur new-account charges (G_{newaccount}) when creating an account, but internal transactions do

**Example**

Suppose you want a contract `C` to transfer ETH to a *brand-new account* `A` that does not yet exist.

- If C transfers directly, the internal new-account path charges 25,000 gas (G_{newaccount}).
- Alternative: first send an external tx from an EOA to A with 1 wei. This tx costs the standard base 21,000 gas. After that, A exists. Now C’s transfer to A no longer incurs the new-account charge (Save ~4,000 gas).

**Conclusion**

If you rely on a contract to create a new account, you pay 25,000 gas.

But if you first send an external transaction (21,000 gas) and then let the contract send funds, you effectively **save ~4,000 gas**.

**Cause**

External and internal creation paths use different charging hooks; only the contract invoking triggers the explicit new-account fee.

## 2. Precompile calls sometimes skip transaction input-byte fees

**Example**

Calling a precompiled contract (e.g., `ECRECOVER`) may skip charging for transaction input bytes. Normally, input bytes cost **4 gas (zero)** or **16 gas (non-zero)** each. Take two real transaction examples:

* 1. A transaction [0x6b01](https://etherscan.io/tx/0x6b01625d57a71c5c3e55e4b5757ba1896a4e5548ba6556cfbf674a9c5d16960d) calling `ECRECOVER` with 24,276 gas, where 276 gas is for the input bytes.

* 2. A transaction [0x1fb0](https://etherscan.io/tx/0x1fb0c35040c9ddf3929a3f3ad40f6fdb9cd2996475e9d3d216da94e9f6805d05) calling `ECRECOVER` with 24,000 gas, where 0 gas is for the input bytes.

If you read the source code of execution client, you can find that the second transaction can also execute `ECRECOVER` without charging for input bytes. The client will pad the input with zero data to match the expected size.

**Extra note**

I guess you are smart enough to notice that the two transactions I mentioned are external transactions.

So why do they invoke precompiled contracts?

I guess part of the reason is that some explorers mislabel precompile addresses (0x01–0x0A) as “burn addresses,” further confusing users (see [here](https://etherscan.io/address/0x0000000000000000000000000000000000000001) with the below snapshot).

[![burn_address](https://ethresear.ch/uploads/default/original/3X/8/8/888950d02deced5147b1669470c6026d62c9b52d.png)burn_address539×182 39.1 KB](https://ethresear.ch/uploads/default/888950d02deced5147b1669470c6026d62c9b52d)

Besides, deploying the precompile addresses in these special addresses (0x01–0x0A) is a failed design.

Sometimes, people just want to call these special addresses directly.

**Cause**

The poor address design of precompiled contracts and the misleading of block explorers leads to confusion and mislabeling.

## 3. Access-list entries are charged even if never accessed (i.e., G_{accesslistaddress}, G_{accessliststorage})

**Example**

EIP-2930 introduces access lists, allowing transactions to specify which addresses and storage slots they intend to access. However, a transaction can include addresses and slots in its access list but never touches them.

For example, a transaction [0x0dd0c](https://etherscan.io/tx/0x0dd0c0f90b2ffbe5588f44116a9b30a2f978cc562e98e70c37ddb2ba738668e4) sets an access list but never accesses the specified slots due to the address.

**Cause**

The protocol charges on *inclusion* to simplify execution, regardless of whether the entries are used. If you trust your users can provide you with correct input, you might as well trust Taylor Swift is your wife.

## 4. Self-transfer still charges transfer gas

**Example**

Account A sends ETH to itself.

No balance change occurs, yet charges still include **9,000 gas** (G_{callvalue}) for the value transfer. According to [this post](https://ethereum-magicians.org/t/some-medium-term-dust-cleanup-ideas/6287) from [@vbuterin](/u/vbuterin).

> Two account writes (a balance-editing CALL normally costs 9000 gas)

Why does one account writing still cost **9,000 gas**? Actually, if you read the source of execution client, you will find that when the from address is the same as the to address, the client will do nothing.

The above cases can happen when the transaction is a self-transfer or uses **CALLCODE** to transfer value.

**Cause**

Execution charges trigger regardless of whether the transfer is a no-op.

## 5. Calldata vs. contract bytecode disk pricing mismatch

**Example**

- Tx calldata: 16 gas/byte (non-zero) or 4 gas/byte (zero).
- Contract bytecode: 200 gas/byte.
Both occupy disk, yet pricing is inconsistent. It’s very confusing for me, as tx calldata is cheaper than contract bytecode as it should consider the actual disk usage and network overhead.

**Cause**

Gas schedule separates “calldata” and “code deposit” without aligning them to actual disk usage.

## 6. Reverted transactions are charged as if they wrote to disk

**Example**

A reverted transaction modifies state in memory, but no changes persist, yet charges for writes are still applied, the following gas fees are affected:

- 25,000 gas (new account, G_{newaccount})
- 9,000 gas (value transfer, G_{callvalue})
- 2,100 gas (cold slot, G_{coldslot})
- 200 gas (code deposit, G_{codedeposit})

Actual memory-only cost would have been ~**100 gas**.

**Cause**

Gas is charged during execution; a later revert cancels state changes but not fees. Implementations conservatively charge to prevent DoS.

## 7. Multiple ETH transfers in a single transaction are mischarged as cold

**Example**

Suppose a contract sends ETH to different accounts multiple times within a single transaction.

- The first transfer correctly incurs the G_{callvalue} (9,000 gas) to write to the account’s balance.
- Subsequent transfers to the other account in the same transaction should be charged the warm access fee (100 gas + 4,500 gas), but sometimes are still billed as cold  (9,000 gas).

**Cause**

The warm/cold access bookkeeping is not consistently updated for multiple value transfers within a single transaction.

## 8. Miner/validator reward or withdrawal writes are uncharged

**Example**

Protocol-level balance updates (e.g., rewards, withdrawals) modify state on disk but cost **0 gas**.

**Cause**

System-level bookkeeping bypasses the gas accounting hooks.

## 9. SSTORE’s first disk read is uncharged (per EIP-2200)

**Example**

When the `SSTORE` opcode is executed, it first reads the current value from disk (contract storage) before deciding whether to write a new value. According to [EIP-2200](https://eips.ethereum.org/EIPS/eip-2200), if the value being stored matches the existing value, no disk write occurs and only a minimal gas fee is charged. However, the initial disk read itself is **not charged any gas**—the protocol only charges for the subsequent write if the value changes.

**Cause**

EIP-2200’s logic focuses on charging for state changes, but omits charging for the disk read that always happens first. This means the first access to the storage slot is free, even if it’s a cold read.

## 10. Storage-read optimizations reduced I/O but gas remained unchanged

**Example**

Ethereum clients have adopted flat storage/snapshot optimizations (e.g., [Snapshot acceleration structure](https://blog.ethereum.org/2020/07/17/ask-about-geth-snapshot-acceleration) for geth), which organize state as a flat key-value store and allow direct disk reads, bypassing the intermediate nodes required by the legacy Merkle-Patricia Trie (MPT). This optimization significantly reduces disk I/O for cold storage reads. For instance, Geth and other clients now use SAS or similar structures, but the gas fees for cold accesses—**2,600 / 2,100 / 2,400 / 1,900 gas**—remain unchanged.

**Cause**

Gas constants for cold access were originally calibrated for MPT, where disk reads were more expensive due to traversing multiple trie nodes. With SAS, the actual disk resource consumption is much lower, but the protocol has not updated the corresponding gas fees.

**Mitigation**

Recalibrate gas constants to reflect the reduced disk I/O when clients switch to SAS or similar optimized storage backends.

## 11. SLOAD vs. MLOAD pricing mismatch

**Example**

- SLOAD (warm) → 100 gas
- MLOAD → 3 gas
Both are memory reads, but prices differ greatly.

**Cause**

Legacy distinction between state and memory operations; optimizations have blurred the actual cost gap.

## 12. Internal transactions sometimes update accounts without gas

**Example**

When account updates in disk occur without charging a gas fee for those updates. Specifically, this issue arises in scenarios where a user sends an external transaction to contract A, which in turn makes an internal call to contract B. If contract B modifies a slot in its storage, the corresponding storage root in contract B’s account must be updated on disk. However, no gas fees are charged for this account B update, leading to an inconsistency.

**Cause**

The bug occurs because the storage trie modification of contract B incurs no additional gas fee for updating its account state. This results from the protocol not charging for account state updates triggered by internal transactions, even though disk writes are performed.

## 13. EXT* opcodes priced too coarsely

**Example**

`EXTCODESIZE` may read more data than `BALANCE`, but both are charged the same cold-account fee (**2,600 gas**).

**Cause**

Opcode pricing buckets are coarse and ignore variable work.

## Closing Note

This issue comes from my paper as follows, I share it with [this link](https://www.usenix.org/system/files/usenixsecurity25-he-zheyuan.pdf).

> He, Z., Li, Z., Luo, J., Luo, F., Duan, J., Li, J., … & Zhang, X. (2025, February). Auspex: Unveiling Inconsistency Bugs of Transaction Fee Mechanism in Blockchain. In Proceedings of the 23rd USENIX Conference on File and Storage Technologies.

I would be glad if you could cite my paper.

All this highlights the need for a comprehensive review and adjustment of gas pricing mechanisms within the Ethereum protocol. By addressing these inconsistencies, we can ensure a more efficient and fair gas market that accurately reflects the underlying resource costs of various operations.

## Replies

**Nero_eth** (2025-08-29):

Thanks for the post, some really interesting points there!

I will not comment on every single one raised but the calldata pricing is at 10/40 for calldata-heavy transaction since [EIP-7623](https://eips.ethereum.org/EIPS/eip-7623) which shipped in Pectra.

Re [EIP-2930](https://eips.ethereum.org/EIPS/eip-2930) access lists, the real inconsistency is not that the protocol charges for unused storage slots (if that wouldn’t be the case you’d be open for DoS as a block builder), but that we don’t charge for the data footprint access lists have, as well as the bandwidth they consume.

With EIP-7928, they become obsolete anyway, so we should just deprecate them somehow.

The fact that precompiles calls don’t contribute to the gas available was an intentional design decision.

Have you already proposed some of the changes, thinking of 1, 2, 3, 7, 9, 10, 11, 12, 13? Those would be a good fit for repricings that are potentially happening with the Amsterdam hardfork. Some of them, I’d bundle into one EIP, and some of them kept separate.

---

**hzysvilla** (2025-08-29):

Thank you for your reply to my post first;

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Re EIP-2930 access lists, the real inconsistency is not that the protocol charges for unused storage slots (if that wouldn’t be the case you’d be open for DoS as a block builder), but that we don’t charge for the data footprint access lists have, as well as the bandwidth they consume.
> With EIP-7928, they become obsolete anyway, so we should just deprecate them somehow.

Your detailed response has given me a much better understanding of Ethereum’s current progress. I agree with your point; perhaps we can add some foolproof designs at the implementation level (without merging into the protocol) to confirm whether the user actually accessed.

I haven’t proposed any EIPs on these topics yet, but I’d be delighted to work on them under the guidance of an experienced researcher like yourself—I’ve long admired your work, such as EIP-7987, EIP-7778 and EIP-7928. If possible, could you please DM me your contact information (or contact me with zi-hao.li@connect.polyu.hk)? It is a great honor to have been able to make some contributions under your leadership.

---

**vbuterin** (2025-08-30):

It’s a good list!

- (1), (4), (7), (13) are addressed by EIP-4762, a companion EIP to statelessness (binary or verkle), which replaces all of the costs you mention with a principled system based on charging for accessing pieces of storage that were not yet accessed during the same block.
- No comment on (2); though personally I hope we can in the medium term get rid of most of our precompiles and do a hard fork to swap them in-place with native code (EVM or RISCV) contracts
- (3) is fine as-is, because the point of an access list is that clients use it to determine what data to fetch; fetched but unused data is still a cost
- For (5), contract bytecode is more expensive because it increases the size of state, which is much more difficult to prune than history, eg. as of May pre-merge history is pruned already.
- (6) is definitely suboptimal; ideally we would only charge for the read in that case. I think the main reason we don’t care too much historically is that a revert happening is the result of bad code, but maybe that assumption is worth revisiting.
- Intuitively I don’t see (8) as a problem.
- For (9), I see in EIP-2200 “If current value equals new value (this is a no-op), SLOAD_GAS is deducted.” So the disk read is charged in that case.
- Regarding (10) and (11), storage pricing is not just about milliseconds in a client, it’s also about enabling stateless execution, and preparing for ZK-proving the chain. Storage access is a high cost in these environments.
- I’m confused by (12). In your example, the user has to pay (i) 2600 gas for a cold call A → B, and (ii) 2100 gas for a cold SLOAD within B. So accounting is done as intended. But anyway, EIP-4762 will make this whole system much simpler.

---

**hzysvilla** (2025-09-02):

THX for your reply.

I agree that EIP-4762 bridges the gap between the gas cost and real resource with fine-grained access/write events.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> For (9), I see in EIP-2200 “If current value equals new value (this is a no-op), SLOAD_GAS is deducted.” So the disk read is charged in that case.

For (9), my point is that when the current value does not equal the new value, the protocol does not charge for the read required to check equality, and only charges for the write operation.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I’m confused by (12). In your example, the user has to pay (i) 2600 gas for a cold call A → B, and (ii) 2100 gas for a cold SLOAD within B. So accounting is done as intended. But anyway, EIP-4762 will make this whole system much simpler.

Here, an EOA first sends a transaction to contract A, which then makes an internal call to contract B. If contract B modifies its storage (e.g., by writing to a state variable), this first updates the MPT nodes for contract B, and subsequently changes contract B’s account state in the world state (as the storage root update).

In my view, the current gas cost model only charges for the write operation on contract B’s MPT nodes but doesn’t account for the write operation on contract B’s account state.

---

Thank you again for your reply, which gave me new insights into the philosophy of gas model design. From (6), I wonder if the gas model should consider the actual execution status of a transaction (whether it succeeds). From (9), should it account for resource consumption changes brought by optimizations in read operations? And from (12), should it consider the resource cost of verification itself?

We will explore to package some of the useful cases you mentioned into an EIP if necessary.

---

**vbuterin** (2025-09-06):

> For (9), my point is that when the current value does not equal the new value, the protocol does not charge for the read required to check equality, and only charges for the write operation.

Actually, this is my bad, I forgot to link to [EIP-2929](https://eips.ethereum.org/EIPS/eip-2929#sstore-changes). That’s the most up-to-date EIP for SSTORE storage gas accounting.

According to EIP-2929, if the current value does not equal the new value, then the user is charged `COLD_SLOAD_COST` gas and then another `SSTORE_RESET_GAS`. If the current value does equal the new value, the user is charged only `COLD_SLOAD_COST`. So it does the right thing in both cases.

> In my view, the current gas cost model only charges for the write operation on contract B’s MPT nodes but doesn’t account for the write operation on contract B’s account state.

I still don’t get why this would be true. The cost charged for the write on B’s MPT nodes is 2100, and the cost charged for the write to B’s account state is 2600. In your scenario, the user would have to pay 4700 total (plus execution, plus the gas of the transaction), which is intended.

> From (9), should it account for resource consumption changes brought by optimizations in read operations? And from (12), should it consider the resource cost of verification itself?

Ideally, gas cost should take into account (i) [access list size](https://ethereum-magicians.org/t/eip-7928-block-level-access-lists/23337), perhaps charged at the same rate as calldata, (ii) naive re-execution time, and (iii) proving time. There’s definitely work to be done in optimizing these in a more principled way.

---

**hzysvilla** (2025-09-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> In my view, the current gas cost model only charges for the write operation on contract B’s MPT nodes but doesn’t account for the write operation on contract B’s account state.

I still don’t get why this would be true. The cost charged for the write on B’s MPT nodes is 2100, and the cost charged for the write to B’s account state is 2600. In your scenario, the user would have to pay 4700 total (plus execution, plus the gas of the transaction), which is intended.

Here is what I’m thinking.

EOA → Contract_A → Contract_B

Initially, 9,000 gas (part of the 21,000 base gas) is consumed to update two accounts: the EOA’s nonce and Contract_A’s storage root.

However, if Contract_A does not transfer ETH to Contract_B (even if Contract_B modifies some storage slots), there will be no additional 9,000 gas charge for updating accounts of Contract_A and Contract_B (because of storage roots changing).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Ideally, gas cost should take into account (i) access list size, perhaps charged at the same rate as calldata, (ii) naive re-execution time, and (iii) proving time. There’s definitely work to be done in optimizing these in a more principled way.

I agree we should rigorously consider gas cost fairness from multiple angles. My work focuses more on fairness regarding resource consumption (which could fall into the second category you mentioned), but considering more dimensions is indeed more reasonable.


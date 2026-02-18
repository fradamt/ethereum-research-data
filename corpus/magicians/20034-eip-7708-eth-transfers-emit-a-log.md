---
source: magicians
topic_id: 20034
title: "EIP-7708: ETH transfers emit a log"
author: vbuterin
date: "2024-05-17"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7708-eth-transfers-emit-a-log/20034
views: 4052
likes: 75
posts_count: 53
---

# EIP-7708: ETH transfers emit a log

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/8575)














####


      `master` ← `vbuterin-patch-2`




          opened 12:10PM - 17 May 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/8/89ac618501d77ed85e1ea0663718f590291e7737.png)
            vbuterin](https://github.com/vbuterin)



          [+56
            -0](https://github.com/ethereum/EIPs/pull/8575/files)







All ETH-transferring calls emit a log.












## Abstract

All ETH-transferring calls emit a log.

## Motivation

Logs are often used to track when balance changes of assets on Ethereum. Logs work for ERC-20 tokens, but they do not work for ETH. ETH transfers from EOAs can be read from the transaction list in the block, but ETH transfers from smart contract wallets are not automatically logged anywhere. This has already led to problems in the past, eg. early exchanges would often not properly support deposits from smart contract wallets, or only support them with a much longer delay. This EIP proposes that we automatically generate a log every time a value-transferring CALL or SELFDESTRUCT happens.

EIP number TBD.

## Replies

**wjmelements** (2024-05-18):

It should be backfilled too. Internal transactions have been a major challenge for blockchain accounting. This feature is more useful if it is available for all of the history.

---

**wjmelements** (2024-05-18):

I have some suggestions.

1. The log’s address field should be nil. It is important that nobody can forge this log. The easiest way to do that is to have a special value for address, since other events would have to be emitted from a source account. nil should be used for all “system logs” therefore.
2. The magic should not collide with any solidity-style event hash. A magic of 0000000000000000000000000000000000000000000000000000000000000000 will not have collisions. While the magic topics[0] can probably be removed altogether if the log address is unique, keeping it allows other types of “system log” in the future. Other values will not compress as easily as all-zeros.

---

**wjmelements** (2024-05-18):

> Should withdrawals also trigger a log? If so, what should the sender address be specified as?

Yes, from the zero-address, which is the common behavior for erc20 mints.

> Should fee payments trigger a log?

I am in favor of this even when the gas price is 0. While it isn’t necessary for accounting because transaction fees are specified by gasPrice * gasUsed, including them would allow eth balances to be completely tracked by querying logs. It would no-longer be necessary to query individual transactions, and it would be easier to locate all transactions sent from an account.

---

**z0r0z** (2024-05-18):

While I appreciate ETH resembling ERC20 for offchain accounting purposes by introducing logs, I wonder if this might be best accomplished on the paymaster-side, if the goal is to make things easier for smart accounts. Personally, I would prefer the approach we have seen so far – introducing features to ETH progressively through wrappers, like wETH. After all, if someone had “new great idea that makes logs not useful” we would then be kind of stuck with bloat.

---

**radek** (2024-05-18):

What would be the impact on storage needs?

Are there any numbers for at least the backfilling case?

---

**metony** (2024-05-19):

Working with Smart accounts this is the #1 pain for us when it comes to track ETH transfer. We ended up debug_ tracing calls on multiple chains, with big $$ in infra costs. And this is also a big blocker in decentralizing portion of what we’re doing (stealth addresses with smart accounts). This would be a huge benefit imho.

Of course we need to limit the logs to transfers with amount> 0.

---

**eyalc** (2024-05-19):

Hmm. operations cost on ethereum try to reflect the cost (of storage, cpu) in term of “gas”.

Emitting a “Transfer” event costs roughly 1700 gas.

Who should pay this cost?

---

**metony** (2024-05-19):

> Who should pay this cost?

Fair point. To support this, I created this dune dashboard (on L1) to get the feeling of the amount of values.

https://dune.com/70nyit/ethereum-call-with-value-greater-0

On avg we have around 1M logs emitted. Considering gas 1700, it will be a total of 1.6B gas per day. Currently the avg usage of gas is around 100B per day. This means there’s a 1.6% avg cost increase in gas spending.

---

**wjmelements** (2024-05-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/eyalc/48/12538_2.png) eyalc:

> Who should pay this cost?

ETH transfers via `CALL` already cost 6700 gas and basic transfer transactions have an even higher base of 21000.

---

**eyalc** (2024-05-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> ETH transfers via CALL already cost 6700 gas and basic transfer transactions have an even higher base of 21000.

The above costs come to cover for nonce change, balance change, and calldata cost.

the extra 6700 extra for transfer is for covering the balance change from both sender and reipient. compare the above cost to performing them using “native” assembly: nonce increment is sload+sstore which is ~5100 gas

So you either think that the current cost is over-paid, and its OK to add another 1500, or that we need to adjust and add this extra gas to the "call"cost.

---

**wjmelements** (2024-05-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/eyalc/48/12538_2.png) eyalc:

> The above costs come to cover for nonce change

Only for the 21000. `CALL` does not increment nonce.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/eyalc/48/12538_2.png) eyalc:

> balance change

Correct.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/eyalc/48/12538_2.png) eyalc:

> and calldata cost.

Calldata is billed separately for transactions and is free for `CALL`.

---

**Tobi** (2024-05-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> It should be backfilled too. Internal transactions have been a major challenge for blockchain accounting. This feature is more useful if it is available for all of the history.

No it shouldn’t. Things shouldn’t be over-complicated. In a world of inifinite engineering capacity… yeah good idea. But we need to prioritize features and there’s a limited amount of engineering capacity.

---

**wjmelements** (2024-05-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tobi/48/10955_2.png) Tobi:

> Things shouldn’t be over-complicated.

It’s not hard to backfill logs, but it is hard to do blockchain accounting for ether, and that should be fixed.

---

**MicahZoltu** (2024-05-30):

We have this implemented in `eth_simulateV1` ([add `eth_simulateV1` by KillariDev · Pull Request #484 · ethereum/execution-apis · GitHub](https://github.com/ethereum/execution-apis/pull/484)) by replicating an ERC20 `Transfer(address from, address to, uint256 value)` with the logging contract address set to `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`.

Rationale:

- 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE is a defacto standard value that many contracts use when they support both tokens and ETH and they want to include ETH in a mapping and they need a lookup key.  Unlike 0x0, there isn’t risk of accidentally checking for it by leaving value uninitialized.
- Following ERC20 Transfer log makes it so anything that parses ERC20 transfer logs can also parse ETH logs without any additional work.  The ERC20 transfer logs contain all of the information desired, (“token”, from, to, amount) so the fit the desired purpose well.

---

**MicahZoltu** (2024-05-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> It’s not hard to backfill logs, but it is hard to do blockchain accounting for ether, and that should be fixed.

Receipts contain logs, and they are part of history, so they cannot be backfilled without rewriting history.

---

**wjmelements** (2024-05-30):

I don’t think rewriting all of the blocks is the easiest way to backfill. Instead, generate replacement receipts for all of the transactions (and blooms for all of the blocks) before the activation block and start serving them instead once they become available. I don’t even think the nodes have to compute these themselves; their operators could trust an import. I was thinking there could be a contest to see who can generate the update first, and ways other competitors could disprove prior submissions if there was a mistake. Similar to re-genesis, it isn’t necessary for all of the nodes to do all of the work, so-long as there is enough incentive to disprove a false submission.

The aforementioned import is only really necessary for already-running nodes. When doing a full block sync, the node would produce two sets of receipts: the one expected to match the block’s receipt hash, and the one that will be served in `eth_getLogs` and `eth_getTransactionReceipt`. There could be a parameter for those methods to fetch the legacy logs.

---

**metony** (2024-05-31):

Backfill is a very cool nice-to-have, if we can find a nice way to have it without delaying the consensus on this EIP, while being able to emit logs for ETH transfers is a must have.

---

**0xInuarashi** (2024-05-31):

I would support this if we could somehow tackle the questions:

1. How do we do this without increasing the gas of Transfers that do not wish to include logs ?
2. How do we do this without adding as much gas as a normal event emission? (native opcode/protocol level stuff → export it to blob?)

Ideally I think the optional Transfer log would be cool, while users can opt out of it for slightly cheaper gas costs. 1700 is obscene when considering 21k is the transfer cost, that’s almost 10%.

I would think that such things should cost XX or XXX gas costs max, increasing with log size, and if not needed to store as permanent data, some expiry or onto blobs could save a lot of “gas” maybe.

---

**wjmelements** (2024-05-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xinuarashi/48/8484_2.png) 0xInuarashi:

> I would support this if we could somehow tackle the questions:

You seem to have some confusion about the spec. Do you understand that the proposal is for every ether transfer to be documented by a log, but the current gas costs are not increased?

---

**etan-status** (2024-05-31):

Strong support for this from the perspective of trust-minimized light clients. Together with [EIP-6493: SSZ Transaction Signature Scheme](https://eips.ethereum.org/EIPS/eip-6493) this unlocks straight-forward implementations of [IVC for scalable trust-free Ethereum logs - HackMD](https://notes.ethereum.org/@vbuterin/parallel_post_state_roots)

Regarding the open questions, I think that they don’t necessarily have to be combined with this EIP. Both withdrawals and fee payments are easier to track than plain ETH transfers.

- For fee payments: When monitoring logs in a trust-minimized world (EIP-6466: SSZ Receipts Root), they are already cross-checked against the receipts_root. The full ETH fees are also part of the same receipt that is already being proven, so full information is extractable in a straight-forward way. Especially in a EIP-7706 multidimensional fee world, some users may want separate logs per fee type, while others may only be interested in the total. I think that it’s fine to expect that a trust-minimized wallet / accounting software can process the full receipt relevant to its own transactions.
- Withdrawals: This point should be extended with the ‘fee_recipient’ payment (formerly ‘coinbase’) as well. Both withdrawals and fee_recipient payments only affect users that solo stake, and larger staking operators that already have access to trusted monitoring; notably, liquid staking users or members of decentralized staking pools don’t benefit as they interact through a smart contract and never directly receive the withdrawals / fee payments. Furthermore, processing is already comparably simple because there is no concept of failures, and the withdrawals tree / block header are tiny compared to the full transactions/receipts logic. I think that it’s fine to have no logs for withdrawals and the fee_recipient payment.


*(32 more replies not shown)*

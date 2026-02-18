---
source: magicians
topic_id: 3311
title: "EIP-2045: Particle gas costs"
author: cdetrio
date: "2019-05-24"
category: EIPs > EIPs core
tags: [gas]
url: https://ethereum-magicians.org/t/eip-2045-particle-gas-costs/3311
views: 5992
likes: 1
posts_count: 23
---

# EIP-2045: Particle gas costs

According to recent benchmarks, EVM opcodes for computation (ADD, SUB, MUL, etc.) are generally overpriced relative to opcodes for storage I/O (SLOAD, SSTORE, etc.). Currently the minimum gas cost is 1 (i.e. one unit of gas), and most computational opcodes have a cost near to 1 (e.g. 3, 5, or 8), so the range in possible cost reduction is limited. A new minimum unit of gas, called a “particle”, which is a fraction of 1 gas, would expand the range of gas costs and thus enable reductions below the current minimum.

https://eips.ethereum.org/EIPS/eip-2045

## Replies

**shemnon** (2019-05-24):

I think instead of lowering the gas cost for simple math the solution is to raise the gas price on storage I/O.

Also, why not milli-gas or micro-gas?  (Just not mibi-gas and mibo-gas, please)

---

**jochem-brouwer** (2019-05-24):

From your specification it looks like only a gas unit is added to the `gasUsed` iff `particlesUsed` exceeds `PARTICLES_PER_GAS`.

Does this theoretically mean that if I set a gasLimit of 10000 this means that my actual gasLimit is actually 10000.9999999…9999? (This at least looks to be the case from the spec for the first time the `gasUsed` increases, via quote: “If  `particlesUsed`  exceeds 1 gas, then 1 gas is added to  `gasUsed`  (and deducted from  `particlesUsed` ).”)

If yes, I’m not sure if this is correct. I would assume that `particlesUsed` would invoke a ceil function, not a floor function, to calculate the gas costs. So if `particlesUsed` either exceeds (>) `PARTICLES_PER_GAS` or it increases from 0 to a nonzero value then one gas unit is added to `gasUsed`.

---

**holiman** (2019-06-07):

I posted this in the Allcoredev channel, I’ll post it here aswell…

Regarding reducing computational opcodes – I think they are (at least close to)  ‘cheap enough’.

We have one op which is *only* execution of a runloop without any operation being performed: `JUMPDEST` , which costs `1` gas. See the data from both aleth and geth: [Investigate slow BLOCKHASH · Issue #5615 · ethereum/aleth · GitHub](https://github.com/ethereum/aleth/issues/5615#issuecomment-499142920) . The jumpdest is fifth heaviest on aleth, second on geth (for the first 1M blocks). This means that `1` gas is not quite enough to pay for the loop, which includes

- checking op validity,
- stack requirements,
- gas requirements,
- lookup/call function etc.

So I agree that there may be room to lower those that

- Pops two items and pushes one item (dealloc rather than alloc)
- Has small spread between worst-case and best-case (e.g. MULMOD has large variance, and may require a lot of alloc or lots of loops)

But I don’t see the need to go into fractions, with all the additional complexity that would bring. Convince me otherwise ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**cdetrio** (2019-06-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> I would assume that particlesUsed would invoke a ceil function, not a floor function, to calculate the gas costs. So if particlesUsed either exceeds (>) PARTICLES_PER_GAS or it increases from 0 to a nonzero value then one gas unit is added to gasUsed.

Yes thanks, the EIP text specifies `ceil` now.

---

**cdetrio** (2019-06-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I think instead of lowering the gas cost for simple math the solution is to raise the gas price on storage I/O.

Raising the gas cost on storage I/O has issues (negative side-effects). This was discussed a bit in the [allcoredevs gitter today](https://gitter.im/ethereum/AllCoreDevs?at=5d0cec3dd1aaa16964e19ba5).

I’ll paste my comments here for convenience:

Issues with raising the cost of storage, SSTORE especially, were hinted at in https://eips.ethereum.org/EIPS/eip-2035:

> The most problematic cases would be with the contracts that assume certain gas costs of SLOAD and SSTORE and hard-code them in their internal gas computations. For others, the cost of interacting with the contract storage will rise and may make some dApps based on such interactions, non-viable. This is a trade off to avoid even bigger adverse effect of the rent proportional to the contract storage size. However, more research is needed to more fully analyse the potentially impacted contracts.

Similar issues were also discussed at the 1.x meetup in January, by Amir Bandeali (https://youtu.be/CnOyVZ3HvK4?t=900). Amir was talking about issues in the context of storage rent / lock-ups, but some similar side effects would also happen from simply raising the cost of SSTORE, if the increase is significant enough.

Another discussion was in this thread: [On raising block gas limit (and State Rent)](https://ethereum-magicians.org/t/on-raising-block-gas-limit-and-state-rent/2249)

> We surely do not need to wait for the entire State rent to be rolled out before increasing the block gas limit. Can we just make state expanding operations (SSTORE, CREATE, etc.) more expensive? Then, recommend the block size increase approximately in the same proportions? For example, make state expansion 3 times more expensive, and recommend raising block size limit by 3 times? Yes, but there are issues to overcome.

---

**cdetrio** (2019-06-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> I posted this in the Allcoredev channel, I’ll post it here aswell…
>
>
> Regarding reducing computational opcodes – I think they are (at least close to)  ‘cheap enough’.
>
>
> […]
>
>
> But I don’t see the need to go into fractions, with all the additional complexity that would bring. Convince me otherwise

I [replied in allcoredevs](https://gitter.im/ethereum/AllCoreDevs?at=5cfba3683dcdab40030ea01f). Pasting here for convenience:

[@holiman](/u/holiman) thanks, good idea to measure relative to JUMPDEST as the baseline opcode. My initial napkin estimates were using the data from the spreadsheet (created an issue here about the spreadsheet data: [holiman/vmstats#1](https://github.com/holiman/vmstats/issues/1)), which has SLOAD the most underpriced at 1060 gas/ms, JUMPDEST in the middle at 9008 gas/ms, and toward the other end is MUL 23287 gas/ms and SWAP{N} around 25000 gas/ms. Based on those numbers, a 4x increase for SLOAD (from 200 gas to 800 gas) would put SLOAD at ~4000 gas/ms, still half the cost of JUMPDEST. MUL could be cut in half to 11k (reduced from gas cost 5 to 3 or 2). If SWAP was cut to ~1/3, from gas cost 3 to 1, then it would go from 25000 gas/ms to ~8000 gas/ms, in line with JUMPDEST.

The spreadsheet data might be a bad sample, but with those adjustments JUMPDEST and SWAP{N} would still be 2x more expensive than SLOAD. So to balance them, either SLOAD would need to be doubled again (from 800 gas to 1600 gas) to from ~4000 gas/ms to ~8000 gas/ms. Or JUMPDEST and SWAP{N} would need to be reduced to 0.5 gas. Of course these are all napkin estimates, and aligning to SLOAD by these gas/ms numbers might not be what we want to do (prices should be set by worst-case gas/ms, not average gas/ms).

But yea, I’d agree with you that if we use these numbers, then 0.5 is “close enough” to 1 that its not worth the complexity of fractions/particle gas costs. But these are numbers for the current geth-evm. The big gains on the table are if geth-evm borrows some of the optimizations in evmone (or perhaps revive that old vm_jit.go), to get an [order of magnitude speedup](https://github.com/ewasm/benchmarking#evm-benchmarks-2019-05-23), it would be enough to obviate the need for certain classes of precompiles (plus it’d be a huge improvement for stateless contracts, and so on).

---

**cdetrio** (2019-06-21):

Pasting comments from [@sorpaas](/u/sorpaas)  on [allcoredevs](https://gitter.im/ethereum/AllCoreDevs?at=5d0cf7497456db0bb82aecc4):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sorpaas/48/1074_2.png) sorpaas:

> I remember we discussed this previously. Basically, any upgrades currently to EVM will break something, even adding new opcodes. The ultimate solution is of course account versioning. I think the conclusion at that time was that if we want to apply something without versioning, then we just rather decide what invariant and backward compatibility we want to preserve, and ignore issues that nobody may care, or is a clearly misuse.  Remediations for EIP-1283 reentrancy bug - #83 by sorpaas

There’s a difference between bending and breaking. Small changes might bend certain use cases, large changes might break them. The statement “any upgrades will to EVM will break something, even adding new opcodes” might technically be true if your definition of “something” is so wide that includes contrived examples of EVM contracts (e.g. a contract that, rather than using the [designated invalid opcode](https://eips.ethereum.org/EIPS/eip-141) 0xfe, uses some random unassigned opcode for the same effect, and would break if in the future that opcode is assigned some functionality and becomes valid). But there is a major downside to such a strict interpretation of backwards-compatibility, and using account versioning to preserve strict backwards-compatibility.

The downside to account versioning for the case of reducing gas costs, is that if gas costs are reduced for the new protocol version and not the old, then all dapps will have to redeploy their contracts to benefit from the reduced gas costs. It would be nice to reduce the gas costs for the existing set of dapps and contracts, and not force all contracts to be redeployed in order to benefit. If we can propose a protocol upgrade in a way that doesn’t break any known use cases and deployed dapps, though it might break some contrived examples (which nobody actually uses on the mainnet), then users will be happy to adopt the upgrade.

So yeah, basically what you said.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sorpaas/48/1074_2.png) sorpaas:

> Regarding block gas limit – I think that may not be a huge issue. Miners can collectively raise the gas limit so that the average is on the previous level.
>
>
> Note that the above discussion is about on-chain EVM. For wallets, compilers and ecosystem programs, every hard fork will break something for them, and most of them will need to do some updates. And if all they need to do is to re-calibrate the gas estimator, I don’t think that’s a big ask.

To be clear, EIP-2045 is a proposal to re-calibrate opcode gas costs (“gas estimators” are tools around the tx fee market between miners and tx senders; miner-accepted *tx gas price* is a different issue from protocol-defined *opcode gas costs*).

re: “collectively raise the gas limit so that the average is on the previous level”. This is addressed in [the EIP](https://eips.ethereum.org/EIPS/eip-2045):

> One way to boost the transaction capacity is to raise the block gas limit. Unfortunately, raising the block gas limit would also increase the rate of state growth, unless the costs of state-expanding storage opcodes (SSTORE, CREATE, etc.) are simultaneously increased to the same proportion. […] Another way to boost the transaction capacity of a block is to reduce the gas cost of transactions. Reducing the gas costs of computational opcodes while keeping the cost of storage opcodes the same, is effectively equivalent to raising the block gas limit and simultaneously increasing the cost of storage opcodes.

---

**axic** (2019-06-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cdetrio/48/482_2.png) cdetrio:

> It would be nice to reduce the gas costs for the existing set of dapps and contracts, and not force all contracts to be redeployed in order to benefit.

That might be something important to consider since we do not have any form of state reducing functionality (such as rents).

---

**sorpaas** (2019-06-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cdetrio/48/482_2.png) cdetrio:

> The statement “any upgrades will to EVM will break something, even adding new opcodes” might technically be true if your definition of “something” is so wide that includes contrived examples of EVM contracts

I brought this up because in previous discussions the breakage of asserting gas costs of a contract falls in the same category as breakage of adding new opcodes. Basically, we were considering that the potential drawbacks of increasing gas costs is really minor compared with potential backward compatibility issues of decreasing gas costs. But I understand that here you are trying to bring it again and question our previous conclusions. I don’t have more arguments to provide at this moment other than the last remediations.

---

**cdetrio** (2019-06-22):

> we were considering that the potential drawbacks of increasing gas costs is really minor compared with potential backward compatibility issues of decreasing gas costs.

Can you explain more specifically the drawbacks and backward compatibility issues? The big backward compatibility issue with decreasing gas costs that I’m aware of is specifically with reducing the cost of SSTORE. That broke an invariant in some contract interactions where previously an SSTORE cost of 5000 was enough to prevent reentrancy given the 2300 gas stipend.

EIP-2045 proposes only reducing the cost of computational opcodes (this is emphasized in the EIP text several times). It does not propose reducing the cost of state-changing or storage opcodes like SSTORE, quite the opposite in fact. It’s my understanding that reducing the cost of computational opcodes will not break any reentrancy invariants, since reentrancy exploits depend only on the cost of state-changing operations; the cost of computational opcodes have no impact on reentrancy issues (unless I’m mistaken).

There may be other types of backwards compatibility issues and problems with reducing the cost of computational opcodes, but currently there are no known issues (at least, I’m not aware of any). On the other hand, there are many known issues with raising the cost of storage opcodes (so there are issues with both raising the cost of storage opcodes and with reducing their cost, lol).

The whole goal of EIP-2045 is to rebalance the cost of computation, which is highly overpriced, and the cost of storage, which is underpriced. The negative consequences of underpriced storage opcodes are two-fold: it is bottlenecking the block processing throughput, and it is exacerbating the state bloat. We need more benchmarking to get accurate estimates of how large the rebalance could be, but the indications so far are that the rebalance could be drastic.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cdetrio/48/482_2.png) cdetrio:

> holiman:
>
>
> I posted this in the Allcoredev channel, I’ll post it here aswell…
>
>
> Regarding reducing computational opcodes – I think they are (at least close to)  ‘cheap enough’.
>
>
> […]
>
>
> But I don’t see the need to go into fractions, with all the additional complexity that would bring. Convince me otherwise

But yea, I’d agree with you that if we use these numbers, then 0.5 is “close enough” to 1 that its not worth the complexity of fractions/particle gas costs. But these are numbers for the current geth-evm. The big gains on the table are if geth-evm borrows some of the optimizations in evmone (or perhaps revive that old vm_jit.go), to get an [order of magnitude speedup](https://github.com/ewasm/benchmarking#evm-benchmarks-2019-05-23), it would be enough to obviate the need for certain classes of precompiles (plus it’d be a huge improvement for stateless contracts, and so on).

There’s another factor I forgot, which is the current block gas limit and uncle rate. So these numbers (which again, might be inaccurate) show that at the current geth-evm speeds, the cheapest computational opcodes (JUMPDEST and SWAP{N}) need to be repriced to 0.5 gas. But it is also widely accepted that, given the low uncle rates we see on the network (and observed average processing times per block, around ~100ms iirc), that the block gas limit can probably be boosted by a significant factor (perhaps ~2x or ~3x, or even higher) without problems, except for the mid and long-term concern about state growth.

So the needed rebalance in cost of computation vs storage is explained by three different factors: (1) at the current geth-evm speed, computation is overpriced and storage is underpriced - the cheapest computational opcodes should be reduced 2x (from 1 gas to 0.5 gas); (2) the current network and clients could process a significantly higher block gas limit, and we want that gas capacity to be spent on computation and not storage - computational opcodes reduced another 2x or 3x; (3) additional gains in computational capacity from clients adopting EVM optimizations - computational opcodes reduced another 5x to 10x.

All combined, rough estimates suggest that computational throughput could see a boost of 20x or more (said differently, the cost of computation could be reduced by 20x or more).

---

**sorpaas** (2019-06-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cdetrio/48/482_2.png) cdetrio:

> There may be other types of backwards compatibility issues and problems with reducing the cost of computational opcodes, but currently there are no known issues

The real point I’m saying is really about “there are no known issues”. Just half a year ago we thought both raising gas costs and reducing gas costs will not have any huge side effects at all. I’m not arguing that you cannot do it by reducing the gas costs. What I’m saying is that, you will need really in-depth backward compatibility assessment to carry this out. For a start, if we reduce the gas costs, then previously we may only be able to do one `CALL` under 2300 gas cost, but now it may be possible to do several, and will this break any assumptions of current contracts? The cost of doing those assessment might be more expensive compared with if we just raise the rest of the gas costs instead (or just put it under account versioning).

I also don’t quite get why raising gas costs will cause issues. We have done it many times in the past just fine. And please note that here we’re talking about protocol-level EVM changes. “Miners/wallets/exchanges need to adjust” is, in my opinion, an inconvenience, rather than an issue.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cdetrio/48/482_2.png) cdetrio:

> increase the rate of state growth

This should not be hugely relevant. If we want to deal with the issue of state growth, we’d better work on it directly – reducing block limit is the easiest way, state rent is the most sophisticated. Re-calibrating gas costs provides balances, but if current Ethereum usage needs this amount of state changes, then with or without EIP-2045, the state growth rate will not change a lot. This is the same as we don’t discourage people to use Ethereum to reduce state growth.

From an emotional perspective, reduce gas costs while keep state change gas costs the same will make developers think the EVM is more efficient, so people may actually care less about performance. In the contrary, increase gas costs will have the possibility to make developers treat efficiency more carefully, and encourage better optimization, thus reduces unnecessary processing/state writes.

---

**cdetrio** (2019-06-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sorpaas/48/1074_2.png) sorpaas:

> cdetrio:
>
>
> There may be other types of backwards compatibility issues and problems with reducing the cost of computational opcodes, but currently there are no known issues

The real point I’m saying is really about “there are no known issues”. Just half a year ago we thought both raising gas costs and reducing gas costs will not have any huge side effects at all. I’m not arguing that you cannot do it by reducing the gas costs. What I’m saying is that, you will need really in-depth backward compatibility assessment to carry this out. For a start, if we reduce the gas costs, then previously we may only be able to do one `CALL` under 2300 gas cost, but now it may be possible to do several, and will this break any assumptions of current contracts? The cost of doing those assessment might be more expensive compared with if we just raise the rest of the gas costs instead (or just put it under account versioning).

That’s a good point. We can use a script to do an analysis of all transactions, and what opcodes are used after a CALL to consume the 2300 gas stipend and trigger an OOG. Then we’ll have a list of opcodes whose gas costs may be an assumed invariant by some actively used contract.

An assessment around the 2300 gas stipend will not be *too* much work. Expanding it to an analysis of all contract interactions in general (all CALLs with any gas amount, not only CALLs with a 2300 gas stipend), or an analysis of all potential contract interactions (not just interactions we can observe in the transaction history) would be a lot of work.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sorpaas/48/1074_2.png) sorpaas:

> I also don’t quite get why raising gas costs will cause issues. We have done it many times in the past just fine. And please note that here we’re talking about protocol-level EVM changes. “Miners/wallets/exchanges need to adjust” is, in my opinion, an inconvenience, rather than an issue.

The main opcode where increasing the gas cost may cause issues is SSTORE. There is EIP-1884 to raise the cost of SLOAD (see [EthMagi thread here](https://ethereum-magicians.org/t/opcode-repricing/3024/9)), which I guess is less of an issue because at 200 gas (or even 800 gas) SLOAD might not be the dominant gas expense. On the other hand, SSTORE at 5000 or 20000 gas tends to dominate. It is already the gas bottleneck so dapps and certain use cases are more sensitive to change in the absolute gas cost (but hopefully not overly sensitive to change in the *relative* cost).

The change in cost we need is drastic (again, potentially 20x or more). Past times opcode gas costs have been raised:

- EIP-150

Increase the gas cost of EXTCODESIZE to 700 (from 20).
- Increase the base gas cost of EXTCODECOPY to 700 (from 20).
- Increase the gas cost of BALANCE to 400 (from 20).
- Increase the gas cost of SLOAD to 200 (from 50).
- Increase the gas cost of CALL, DELEGATECALL, CALLCODE to 700 (from 40).
- Increase the gas cost of SELFDESTRUCT to 5000 (from 0).
- If SELFDESTRUCT hits a newly created account, it triggers an additional gas cost of 25000 (similar to CALLs).

[EIP-160](https://eips.ethereum.org/EIPS/eip-160)

- increase the gas cost of EXP from 10 + 10 per byte in the exponent to 10 + 50 per byte in the exponent.

As you can see, the cost of SSTORE has never been changed before.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sorpaas/48/1074_2.png) sorpaas:

> cdetrio:
>
>
> increase the rate of state growth

This should not be hugely relevant. If we want to deal with the issue of state growth, we’d better work on it directly – reducing block limit is the easiest way, state rent is the most sophisticated. Re-calibrating gas costs provides balances, but if current Ethereum usage needs this amount of state changes, then with or without EIP-2045, the state growth rate will not change a lot. This is the same as we don’t discourage people to use Ethereum to reduce state growth.

In discussions around 1.x we’ve learned that an important aspect around reducing state growth is that before state rent gets introduced on the mainnet, dapp devs need to have an alternative development model, e.g. a way to write “rent-compatible” contracts. If state rent is introduced but dapp devs have no way to write rent-compatible contracts, then we’d just be choking off usage and discouraging people from using Ethereum rather than fixing the problem.

One class of contracts that are rent-compatible are stateless contracts. Given the current gas cost imbalance between transaction data (overpriced) and storage (underpriced), it is not cost effective for devs to write stateless contracts. EIP-2028 will correct this imbalance (see EthMagi thread: [EIP-2028: Transaction data gas cost reduction - #5 by elibensasson](https://ethereum-magicians.org/t/eip-2028-calldata-gas-cost-reduction/3280/5)).

We want to prototype more stateless contracts and run benchmarks to estimate what, besides the cost of calldata, will be gas bottlenecks. But I suspect the cost of computation, e.g. verifying the merkle proofs passed in the calldata, is going to be a bottleneck. If the cost of computation is a bottleneck for stateless contracts, then reducing the cost to achieve a rebalance (or rebalance by increasing the absolute cost of storage and boosting the gas limit) is best step we can take to provide devs a way to deploy rent-compatible contracts.

With the right cost balance, devs will even be incentivized to deploy such rent-compatible, stateless contracts. If devs are deploying stateless contracts, we should see the rate of state growth start to slow down. Then state rent can be introduced with less disruption; it would further disincentivize stateful contracts with continual cost of storage (though after a rebalance, the one-time cost of storage will already be more expensive than passing in data through calldata). To *ensure* that state growth is completely flat or even negative, we could apply rent to existing contracts regardless of breakage (backward-breaking rent), rather than only to new contracts through account versioning (forward-compatible rent). But we could see state growth flatten out even without rent, or only with forward-compatible rent.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sorpaas/48/1074_2.png) sorpaas:

> From an emotional perspective, reduce gas costs while keep state change gas costs the same will make developers think the EVM is more efficient, so people may actually care less about performance. In the contrary, increase gas costs will have the possibility to make developers treat efficiency more carefully, and encourage better optimization, thus reduces unnecessary processing/state writes.

Applications that care less about performance will be slower and more costly than apps from developers who put in extra effort to optimize them. We see this in all software (not just Ethereum contracts).

At first I thought “we’re boosting the gas limit! (but also raising the price of storage)” had better marketing appeal than “we’re keeping the gas limit the same (but reducing the price of computation)”. But on second thought, “cheap gas for everyone! (for computation)” sounds better than “there’s a lot more gas now! (for computation)” imo.

---

**shemnon** (2019-06-24):

Lowering a price on EIP-1283 is what caused a security concern.  It wasn’t until well after testnet launch we discovered the need for the invariant expressed in EIP-1706.  For that reason I am deeply skeptical of any price reductions without a solid backwards compatibility assessment against “in the wild” deployed contracts.  Gas increases are inconvenient to tools. But gas price increases have not resulted in security exploits, which resulted in an emergency fork cancellation.

---

**cdetrio** (2019-06-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Lowering a price on EIP-1283 is what caused a security concern.  It wasn’t until well after testnet launch we discovered the need for the invariant expressed in EIP-1706.  For that reason I am deeply skeptical of any price reductions without a solid backwards compatibility assessment against “in the wild” deployed contracts.

The security concern caused by EIP-1283 was contract reentry. Contract reentry, as far as I understand it, can only be caused by reducing the gas cost of storage opcodes (i.e., it cannot be caused by reducing the gas cost of computational opcodes). Only storage opcodes are relevant because the security risk of reentry is contract state change, which is only possible through an SSTORE (or maybe another state-changing opcode, e.g. a balance transfer with a CALL. Let’s call “state-changing opcodes” the set of all CALL* opcodes and storage opcodes; everything else is a computational opcode).

I agree that a thorough backward compatibility assessment is needed, but I’d bet that reducing the cost of computational opcodes is safe with respect to contract reentry.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Gas increases are inconvenient to tools. But gas price increases have not resulted in security exploits, which resulted in an emergency fork cancellation.

The increase in cost of CALL from 40 to 700 also specified the “1/64 gas rule” to avoid breaking lots of contracts. Also, as I mentioned above, the cost of SSTORE has never been changed before (SSTORE and SLOAD are the two main opcodes whose cost need to be drastically rebalanced). Anyway, are you suggesting that cost increases can go ahead without versioning, and without thorough backward-compatibility assessments? Or should EIP-1884 ([EIP 1884: Repricing for trie-size-dependent opcodes](https://ethereum-magicians.org/t/opcode-repricing/3024)) also have a thorough assessment, or only apply to the new EVM version?

Btw, the problems with a cost increase of SSTORE are not mere inconvenience for tools. I mentioned this above, with links to previous discussion (see the paragraph starting, “Another discussion was in this thread: On raising block gas limit (and State Rent)”).

---

**shemnon** (2019-06-26):

Versioning of all gas price changes is what I consider to be the best course of action.  Since versioning is in Istanbul now (EIP-1702) then it is a good time to add a clause that the gas price changes apply to “contracts deployed at version 1 or later” to all EIPs proposing a gas price change.

However, SSTORE may be a special case, since it presents the main threat to node stability: storage bloat.  However we don’t have the metrics to justify an all-versions gas cost increase in this network upgrade cycle.

---

**cdetrio** (2019-06-26):

We have metrics from [@holiman](/u/holiman)’s benchmarks to justify an all-versions increase for SLOAD (charts are in [EIP-1884](https://eips.ethereum.org/EIPS/eip-1884) with more on https://github.com/holiman/vmstats).

Do you think a boost of the block gas limit is justified? Or what kind of data would we need… (Of course, the block gas limit isn’t determined by the protocol, but core devs can advocate for miners to choose a new target limit).

---

**holiman** (2019-06-27):

Yep, we definitely do have the metrics to justify particularly `SLOAD`. I have not produced metrics to justify `SSTORE` increase. Mainly because that’s more difficult to measure:

- State bloat and the effect it has on sync, block processing etc is hard to quantify
- SSTORE by itself does not touch disk during execution, the disk effect happens only later, when the trie is committed (and possibly not even then, if disk flushing is deferred for later).

So I think [@AlexeyAkhunov](/u/alexeyakhunov)’s various data and charts about state trie density are good places to start investigating that. I’m not saying that `SSTORE` increase is not motivated, just that my own charts does not (even try to) measure that.

---

**chfast** (2019-07-05):

I’d go with `PARTICLES_PER_GAS = 1000` to have milligas units.

Then, 1000 has at most 10 bits, so we have to lower the max gas limit from `2^63-1` to `2^53-1` to still allow full gas calculation on particle units with 64-bit types. This might be also a good opportunity to lower it down to `2^32-1` or even `2^31-1`.

---

**fulldecent** (2019-08-17):

There are already so many gas changes in Istanbul that we cannot know the effects of them. We should study them before a sweeping change like this.

---

**jpitts** (2019-11-07):

Possibly contains some additional insights relevant to this discussion (and sorry if this is redundant. LMK and I will post elsewhere)…

[The Economics of Smart Contracts](https://arxiv.org/abs/1910.11143) (Submitted on 23 Oct 2019)

by Kirk Baird, Seongho Jeong, Yeonsoo Kim, Bernd Burgstaller, Bernhard Scholz

> We show that the actual costs of executing smart contracts are disproportionate to the computational costs and that this gap is continuously widening. We show that the gas cost-model of the underlying EVM instruction-set is wrongly modeled. Specifically, the computational cost for the SLOAD instruction increases with the length of the blockchain.


*(2 more replies not shown)*

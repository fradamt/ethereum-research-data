---
source: ethresearch
topic_id: 7472
title: Meta transactions, Oil, and Karma megathread
author: pipermerriam
date: "2020-05-26"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/meta-transactions-oil-and-karma-megathread/7472
views: 5646
likes: 20
posts_count: 24
---

# Meta transactions, Oil, and Karma megathread

My goal here is to capture the broader concepts at play surrounding the [Oil & Karma](https://ethresear.ch/t/oil-adding-a-second-fuel-source-to-the-evm-pre-eip/7394) proposals, [Vitalik’s counter proposal](https://ethresear.ch/t/counter-proposal-to-oil-karma-per-account-gas-limits/7433) and the related [meta transaction](https://medium.com/@austin_48503/ethereum-meta-transactions-90ccf0859e84) concept which is a specific use case of the more generic concept of making untrusted calls in the EVM.

At a broad level this entire problem is centered around the two opposing problems of:

1. Needing to reprice opcodes as the EVM evolves
2. The breakage that can occur when opcodes are repriced

Aragon's Blog

We **want** to reprice things for changes like accounting for witness sizes, but we **cannot** reprice things without potentially breaking existing code that depends on the current prices.

### Untrusted EVM calls

We’ll define the concept of an “Untrusted Call” as being any of the `*CALL*` style opcodes in the EVM for which both *caller* and *callee* do not trust each other.

> Since caller and callee only differ by a single letter, I’ll use the terminology parent and child for easier differentiation

From the *parent* perspective, this typically takes the form of accounting **after** the child call has occurred.  One example of this is measuring how much gas the child consumed.  Because of this, the parent’s call frame needs to be insulated from a revert in the child propagating to the parent call frame.  In the current EVM, this is done by specifying the gas allotment for the child such that a revert/out-of-gas in the child does not cause the parent to revert as well.

From the *child* perspective, this typically takes the form of ensuring that the parent cannot cause the child to fail in unexpected ways by either providing insufficient gas, or by making the call when the call stack is already near the maximum depth.

In both perspectives, parent and child accomplish these requirements by observing the remaining gas via the `GAS` opcode.  In order to do this accounting, one must typically make an estimate or measure how much gas the parent call needs after the child has finished, and these estimates or measurements are anchored to the existing gas prices.

It is worth enumerating the use cases for untrusted EVM calls.

1. Sending transactions for another party

Such as maintaining anonymity while pulling funds out of a mixer
2. Such as the Ethereum Alarm Clock
3. Paying for transactions in other currencies

Such as paying gas fees in DAI

> The ideal case would be a solution that preserves the existing mechanisms, but it is worth pointing out that it might be ok to break the existing mechanism if a new mechanism was added to allow the existing functionality to be implemented using the new mechanism.

### Why Oil/Karma probably don’t fix this.

One proposed solution is to introduce a new unit of accounting separate from gas that is not observable.  This would in theory preserve the existing gas schedule and introduce a new accounting mechanism that could be changed without the burden of backwards incompatibility since it is not observable.

It is my opinion that this thinking is flawed.

If any opcode ever costs more *oil* than it does in *gas*, then the child will be able to cause a reversion that propagates through the parent call frame.  This would break meta transactions.

### Why UNGAS probably doesn’t fix this



      [Core Paper](https://corepaper.org/ethereum/compatibility/forward/#remove-gas-observables)





###



Design of a forward-compatible EVM that will not break contracts when applying feature upgrades.










Another proposed solution is to take the more extreme approach and make gas un-observable.  The idea is to make gas un-observable and thus, remove the ability to write code that depends on the gas schedule.

It is my opinion that this approach is also flawed.

1. Just because gas is no longer observable, does not mean that people would not write code that depends on the underlying gas schedule.
2. It fundamentally breaks meta-transaction style functionality which would be highly contentious.

## Having our  cake  and eating it too

> You can't have your cake and eat it - Wikipedia

We want …

1. Preservation of existing use cases for gas accounting for untrusted EVM calls
2. Ability to make changes to the gas schedule without breaking things.

### Make the gas schedule itself observable

One approach that comes to mind is to look at the mechanisms available for smart contracts to do gas accounting.  Currently, they can observe the remaining gas using the `GAS` opcode, but any code dealing with gas accounting must be written against the current gas schedule.  We could potentially address the problem by making the gas schedule observable as well.  *In theory* this would allow for gas requirements to be computed at runtime which would allow for contract code to observe gas in a manner that was robust against changes to the gas schedule.

It is unlikely that we can make it possible to observe all gas costs since things like expanding the memory are priced dependent on the current execution state.

### Ungas & a new EVM mechanism

Ungas could be viable, but it would be a major backwards incompatible change that by itself would remove a popular use case.  I believe that we would need to couple Ungas with a new mechanism upon which the existing use cases for gas observation could be built.  Account abstraction looks like a promising route.

## Replies

**vbuterin** (2020-05-26):

Yep, that all matches my understanding!

Though I do think we should also talk about adding an explicit recommendation that for now contracts should never call children with a fixed amount of gas; if the gas field is used, the value should come from the transaction.

---

**AlexeyAkhunov** (2020-05-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> Make the gas schedule itself observable

Sorry, but this to me sounds like something I personally would never want to do. Instead of fixing a broken abstraction of gas, it shatters it into smithereens (or shards, if you like ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) ) ! In order to make gas schedule observable, you need to introduce the notion of “opcode” to the contracts. And how will the contracts be able to reason about the gas cost of execution even if they have access to the schedule? From what I understand, it requires some form of static analysis heuristics. Interestingly, we want to use similar heuristics to demonstrate that we can produce quite tight upper bounds on oil/gas ratio in most transactions, so I current don’t take “Oil won’t work” very seriously ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**pipermerriam** (2020-05-28):

I should have been clearer that I wasn’t exactly advocating for observable gas schedules, merely investigating the various ways that we might approach the problem.  I think the approach of UNGAS + a new mechanism to implement meta-transactions is the most promising…  but given that there is still a large unknown and it potentially ends up depending on account abstraction… it’s hard to justify going that direction either.

I would be interested in understanding why Oil/Karma is a viable solution that doesn’t break meta-transactions (assuming that you believe this to be the case).  Maybe I missed something in the write-ups, but it seems like it doesn’t actually address the problem, only hides it under another layer that still breaks if we adjust the Oil schedule in a way that makes some operations more expensive in oil than gas.

---

**gichiba** (2020-05-28):

Thanks for collecting this into a megathread [@pipermerriam](/u/pipermerriam) !

If someone could help me, I’m trying to understand what breaks in the case of Oil/Karma and ‘meta-transactions’

By my understanding there are different patterns that can be used for ‘meta-transactions’, and in the context of oil/Karma breakage, we’re talking about one genre, the kind that monitor gas remaining and/or make assumptions about gas. ( [Native meta-transactions](https://medium.com/gitcoin/native-meta-transactions-e509d91a8482) are another breed that I *think* wouldn’t be affected )

Here’s an example contract that might fit the bill:


      [github.com](https://github.com/status-im/contracts/blob/c283eab558fa5c12cbde646175e8fb238c0b7b4d/contracts/identity/IdentityGasRelay.sol)




####

```sol
pragma solidity ^0.4.21;

import "./Identity.sol";
import "../token/ERC20Token.sol";

/**
 * @title IdentityGasRelay
 * @author Ricardo Guilherme Schmidt (Status Research & Development GmbH)
 * @notice enables economic abstraction for Identity
 */
contract IdentityGasRelay is Identity {

    bytes4 public constant CALL_PREFIX = bytes4(keccak256("callGasRelay(address,uint256,bytes32,uint256,uint256,address)"));
    bytes4 public constant APPROVEANDCALL_PREFIX = bytes4(keccak256("approveAndCallGasRelay(address,address,uint256,bytes32,uint256,uint256)"));

    event ExecutedGasRelayed(bytes32 signHash, bool success);

    /**
     * @notice include ethereum signed callHash in return of gas proportional amount multiplied by `_gasPrice` of `_gasToken`
     *         allows identity of being controlled without requiring ether in key balace
```

  This file has been truncated. [show original](https://github.com/status-im/contracts/blob/c283eab558fa5c12cbde646175e8fb238c0b7b4d/contracts/identity/IdentityGasRelay.sol)








(and for some more context, an [article that walks through it](https://medium.com/coinmonks/gasless-transactions-f75382095c4f))

In this contract (or, IDK, in a toy contract that has the properties that matter), what goes wrong when oil/karma is applied, and (if necessary) the gas schedule is changed by some threshold?

I think it would help me understand oil/karma better to understand the failure condition(s) in greater detail.

---

**AlexeyAkhunov** (2020-05-28):

I am considering the case where contract `A`, the relayer, wants to call contract `B`, and does it by invoking opcode `CALL` with the hard-cap (GAS-CAP) on the gas which is forwarded.

The semantics of `CALL` is such that if the execution of `B` runs out of the GAS-CAP, the call will still return to `A` and `A` will have enough gas left to do its things, and not revert the entire transaction.

Oil may break this if the invocation of `B` by the relayer `A` hits the “out-of-oil” exception before it hits “out-of-gas” exception. And because oil cannot be forwarded and has just one single pool, the semantics of “out-of-oil” must inevitably mean that the entire transaction fails, and none of the state changes made before the invocation `A=>B` apply, and effectively the relayer just wasted ETH on gas/oil.

However, this breakage can be avoided, if the relayer `A` ensures that the invocation never hits “out-of-oil” before “out-of-gas”. And the trick is to figure out the upper bound of “how much oil can the invocation theoretically spend before it hits the limit of GAS-CAP”. If the relayer then provides (in the gas-limit of the entire transaction, not in the `CALL` opcode) the amount of oil/gas which is greater or equal than that upper bound, it can guarantee that “out-of-oil” will never happen inside the invocation `A=>B`.

In the version 1.1 of Oil proposal, we talked about naive and more sophisticated way of calculating the upper bound. We shall try out a sophisticated method (based on taint analysis) to demonstrate that the upper bounds are normally going to be tight enough for this technique to be practical.

---

**vbuterin** (2020-05-28):

In-protocol meta-transactions are definitely looking like a better and better idea; saying that you can have meta-transactions but you can only safely use them up to 2 million gas (or whatever 10 million divided by the maximum OIL/GAS ratio is) is going to cause problems (eg. as far as I can tell a STARK-based Tornado Cash-like system would already cost more than 2m gas).

If we have in-protocol meta-transactions (which is certainly a reasonable idea to look into), then we don’t have any significant remaining use cases for untrusted calls, and we can just implement UNGAS, right?

It does seem like maintaining the ability to have untrusted calls is in the long run more trouble than it’s worth.

---

**AlexeyAkhunov** (2020-05-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> In-protocol meta-transactions are definitely looking like a better and better idea

I agree with that part

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> saying that you can have meta-transactions but you can only safely use them up to 2 million gas

That would also be saying that if we start charging for witnesses, these calls that go over 2 million gas routinely won’t be viable (because they are likely the ones that generate large witnesses), and relayers won’t be tasked to execute them. Therefore, I do not see this as a deterrent. What I do see is that relative cost of computation vs consensus over large strings of data (tx inputs, witnesses) will readjust and things like SNARKs will probably be OK if they are mostly computationally intensive.

---

**PhABC** (2020-05-29):

> The breakage that can occur when opcodes are repriced

Many of the discussions around opcode repricing breaking contracts are around parent calling child, but it’s important to note that there are many other scenarios that don’t involve cross-contract calls that could be problematic when it comes to opcode repricing.

Two examples:

1. Function call costing 3m gas now costing 12m gas. If that functions is deemed safe because it only takes 3m gas, repricing opcodes or a decrease in block gas limit could render that function impossible to execute. The 3m gas is one example, but even a call using 1m gas or less could be made to exceed block gas limit with a few opcode repricing.
2. Hypothetical Optimistic Rollup: To make sure txs on ORU chains aren’t too complex (so ORU nodes can keep syncing and validating the ORU chain), you need to monitor gas as well. A simple way of doing it is with fraud proofs where users include a gas limit to their signed message, which can be used on-chain to prove that a transaction cost more than the expected value. A change in opcode re-pricing could mean that what used to be valid ORU txs could be made invalid after the fork, allowing the slashing of very old transactions.

There are of course more examples and I believe only thinking of situations involving cross contract calls is not addressing the core issue that re-pricing opcodes can always lead to breaking changes. **All contracts currently in existence make an implicit assumption that their functions will always be executable within a block and opcode repricing will always threaten this.**

If we want to support opcode repricing, I believe the only viable solution is unfortunately education and tools. Perhaps a fork of ganache could allow devs to run your unit tests with variable opcode prices, from a 0.1 to a 50x scaling factor or whatever we believe is a “reasonable range of opcode repricing”. Making tools like this a “standard” in dev toolkits would mean that developers could have some guarantees that their contracts will work as expected even if opcode are repriced wildly.

Elastic block gas limit like with can EIP-1559 help, but there is always an upper bound that be problematic for some contracts after opcodes are repriced.

---

**holiman** (2020-05-30):

> If any opcode ever costs more oil than it does in gas, then the child will be able to cause a reversion that propagates through the parent call frame.
> This would break meta transactions.

I think this statement is a bit to sweeping. I’d like to pick apart meta-transactions a bit.

A Meta-tx has two parties:

1. The party that produced the meta-tx, let’s call him the signer.
2. The party that creates an ethereum transactions, and pays the actual gas. Let’s call him the relayer.

In a meta-tx, the `relayer` executes the meta-tx, and during the course of execution, some reward is (typically) sent to the `relayer`. This typically happens in a trustless setting: relayer invokes a meta-tx `scheduler` which picks a `metatx` for execution, executes the `metatx` and afterwards pays a reward for the `relayer` in some asset.

As I see it, there are two main ways that meta-tx can be broken:

1. The signer has his transaction executed in a way that makes it fail, but the relayer still gets the reward.
2. The relayer spends money on a metatx, but is given no reward.

Now, let’s consider the two proposals (oil/karma vs [@vbuterin](/u/vbuterin)’s counter proposal).

### Counter-proposal

The counter-proposal introduces rules for how the tx `sender` (that is; the `relayer`) can modify gas-forwarding rules further down in the call stack. This means that actions performed by the `relayer` can modify the execution flow of the meta-tx.

In short: the possible breakage from Counter-Proposal means that meta-txs can be broken in way 1).

### Oil/Karma

With oil/karma, it’s possible that the entire execution is reverted, costing money for `relayer`. Breakage of type 2).

### Analysis

I’d argue that type-1 breakage is worse thann type-2 breakage. A type-2 breakage introduces a level of risk, for the *active* participants of the meta-tx game. If you want to execute a meta-tx, you would now have to take into account the possibility that the execution may fail. If we see meta-txs as a market, it could be argued that these risks *should* be organically handled by an efficient market.

- Does ‘rotten’ meta-txs cause relaying to happen at a loss? Then relayers will stop relaying unless the reward is sufficiently high to offset the risk.
- A relayer can also (try to) analyse meta-transactions, and estimate which ones are likely to cause a loss. Different relayers may do this differently, but I don’t see that this would be impossible.

As for type-1 breakage, the `signer` submits his meta-tx. After that has happened, potential attackers have unlimited time to analyze if they can cause the transaction to fail. If the meta-tx is a regular occurrence (like alarm-clock), it might be possible to totally drain the underlying asset while not actually performing anything useful work at all for the `signer`.

### Lastly

Another object to raising gas costs in general, is that the block gas limit can rise above where it’s possible to execute transactions. I see ‘balancing gas costs in accordance with resource expenditure’ as a difficult and important problem to solve. The problem with large transactions vs max gas seems to me to be a lot simpler problem, which can be solved in a number of ways:

- EIP-1559 is one way,
- We could have ‘superblocks’ e…g every 10K blocks, which are substantially higher in max gas.

---

**wighawag** (2020-06-01):

I agree that type 1) is the main problem, as I mentioned here : [Counter-proposal to oil/karma: per-account gas limits](https://ethresear.ch/t/counter-proposal-to-oil-karma-per-account-gas-limits/7433/11)

But I don’t see how the oil/karma proposal would be immune from 1) the problem is that current CALL opcode only enforce a max gas. They protect the parent not the child.

EIP-1930 is a very simple solution to that problem and using it for metatx does not make them opcode pricing dependent as the gas is specified by the signed message.

---

**holiman** (2020-06-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/wighawag/48/177_2.png) wighawag:

> But I don’t see how the oil/karma proposal would be immune from 1) the problem is that current CALL opcode only enforce a max gas. They protect the parent not the child.

The oil/karma proposal meanst that raising the gas limits will not cause any *new* problems – because if it causes breakage, the entire tx is reverted (costing the sender the fee, but no other sideeffects). So in that sense it is immune.

However, if there is type-1 breakage *today*, due to gas mechanics, they don’t get “fixed” by oil/karma.

I wasn’t sure which one of those things you were referring to.

---

**wighawag** (2020-06-03):

Ah, yes, you right, and oil/karma proposal would even allow existing contract that relies on computing the gas cost of the call prior to calling (see solution : `check done before the call` in the rationale section of [EIP-1930](https://eips.ethereum.org/EIPS/eip-1930)) to ensure the child receive the correct amount of gas to continue working.

Such solution has actually been adopted by gnosis safe to fix their [metatx safety bug](https://github.com/gnosis/safe-contracts/issues/100)

their fix can be seen [here](https://github.com/gnosis/safe-contracts/blob/62d4bd39925db65083b035115d6987772b2d2dca/contracts/GnosisSafe.sol#L145)

But apart from this, which would be more elegantly (and a lot more simply) solved with EIP-1930, what benefit does it bring to contract developer to be able to use hard coded gas value ?

If we follow  the following

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> adding an explicit recommendation that for now contracts should never call children with a fixed amount of gas; if the gas field is used, the value should come from the transaction.

And add EIP-1930 for meta-tx support, then I do not see what oil/karma brings to the table ?

---

**holiman** (2020-06-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/wighawag/48/177_2.png) wighawag:

> And add EIP-1930 for meta-tx support, then I do not see what oil/karma brings to the table ?

Well, I think we may be two very having different perspectives. I believe your goal is to improve the situation for meta-txs, in general, and view the oil/karma/counter as different proposals in that direction.

However, oil/karma/something are proposals to solve a different problem[1], not related to meta-txs. This  thread is about possible side-effects with oil/karma/something, and whether one such side-effect is that they “destroy” metatxs, or not.

[1] The problem of how we can modify gas costs, e.g. in the context of rebalancing opcodes and/or paying for witness size. Without screwing layer-2 over

---

**wighawag** (2020-06-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/holiman/48/4014_2.png) holiman:

> [1] The problem of how we can modify gas costs, e.g. in the context of rebalancing opcodes and/or paying for witness size. Without screwing layer-2 over

Could you point to documentation where opcode/witness size gas pricing need to be hardcoded in the layer 2 smart contracts ? Because if there exist mechanism to make such smart contract independent of opcode pricing then we would not need oi/karma.

---

**matt** (2020-06-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> In-protocol meta-transactions are definitely looking like a better and better idea;

Any prior art on this subject? It seems like adding a `sponsor` field to transactions for a relayer’s signature would do the trick. They lose a little control in terms of cancelability, since the transaction’s nonce would not be tied to their account, but I’m not sure how important that is to maintain.

---

**PhABC** (2020-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/holiman/48/4014_2.png) holiman:

> [1] The problem of how we can modify gas costs, e.g. in the context of rebalancing opcodes and/or paying for witness size. Without screwing layer-2 over

I’m not sure this is ever possible however. So long as there is a block gas limit, increasing the cost of opcodes can always render some functions unusable if they now cost more than the gas limit.

---

**SergioDemianLerner** (2020-06-04):

I have my own proposal for meta-transactions (that we are developing for RSK), that works when combining a sponsor signatory with the rich transactions proposal.



      [github.com/rsksmart/RSKIPs](https://github.com/rsksmart/RSKIPs/blob/15f77807fba2fc79d577aec44c0657dce8a3570d/IPs/RSKIP138.md)





####

  [15f77807f](https://github.com/rsksmart/RSKIPs/blob/15f77807fba2fc79d577aec44c0657dce8a3570d/IPs/RSKIP138.md)



```md
# Multi-signed transactions supporting enveloping and multi-key accounts

|RSKIP          | 138 |
| :------------ |:-------------|
|**Title**      |Multi-signed transactions supporting enveloping and multi-key accounts|
|**Created**    |2019 |
|**Author**     |SDL |
|**Purpose**    |Sca |
|**Layer**      |Core |
|**Complexity** |2 |
|**Status**     |Draft |

# **Abstract**

One of the features that can help the blockchain technology reach mass adoption is transaction enveloping. Enveloping allows a third party to pay for the gas of a transaction, while the transaction still originates from the same account that does not possess RBTC. Implementing this feature efficiently in terms of gas requires modifications to the layer 1. Basically we can build a transaction we more that one signer, and specify which of the signers will pay for the fees. Multi-signed accounts also open the possibility to compress with LTCP settlement transactions sent to payment channels. Instead of n transactions (one for each of the participant), a single transactions with n signatures can be built, reducing the network resource consumption.

# **Specification**
```

  This file has been truncated. [show original](https://github.com/rsksmart/RSKIPs/blob/15f77807fba2fc79d577aec44c0657dce8a3570d/IPs/RSKIP138.md)












      [github.com/Arachnid/EIPs](https://github.com/Arachnid/EIPs/blob/f6a2640f48026fc06b485dc6eaf04074a7927aef/EIPS/EIP-draft-rich-transactions.md)





####

  [f6a2640f4](https://github.com/Arachnid/EIPs/blob/f6a2640f48026fc06b485dc6eaf04074a7927aef/EIPS/EIP-draft-rich-transactions.md)



```md
---
eip:
title: Rich transaction precompile
author: Nick Johnson (@arachnid)
discussions-to: https://ethereum-magicians.org/t/rich-transactions-via-evm-bytecode-execution-from-externally-owned-accounts/4025
status: Draft
type: Standards Track
category: Core
created: 2020-02-24
---

## Simple Summary
Support 'rich transactions' by allowing transactions from externally owned accounts to execute bytecode directly.

## Motivation
Many Ethereum DApps presently require users to approve multiple transactions in order to produce one effect - for example, the common pattern of first approving a contract to spend a token, then calling that contract. This results in a poor user-experience, and complicates the experience of interacting with DApps.

Making it possible for externally owned accounts to execute EVM bytecode directly allows a single transaction to execute multiple contract calls, allowing DApps to provide a streamlined experience, where every interaction results in at most one transaction.

While this is in principle possible today using contract wallets, other UX issues, such as the need to fund a sending account with gas money, lack of support for contract wallets in browser integrations, and lack of a consistent API for contract wallets has led to poor adoption of these. We propose this EIP as a way of enhancing the utility of existing EOAs, in the spirit of "don't let the perfect be the enemy of the good".
```

  This file has been truncated. [show original](https://github.com/Arachnid/EIPs/blob/f6a2640f48026fc06b485dc6eaf04074a7927aef/EIPS/EIP-draft-rich-transactions.md)










The idea is that the payload to be executed in the context of the origin account has the following logic:

1. Call to the token contract Transfer() to pay an agreed amount of tokens to the Sponsor
2. A call to self (ORIGIN) to the method ExecuteUserAction(args), where args are user-defined from the real transaction (DESTINATION, arguments).
3. When the method ExecuteUserAction(args) is executed, the arguments are extracted and a CALL is performed.

The recursive encapsulation ensures that the callee receives the call from the ORIGIN EOA, and not from any other sender. It also ensures that even if the DESTINATION rises a OOG or REVERTs, the exception is caught and the payment in tokens is never aborted.

But I first would like to ask a question for you:

Why do you want to increase the cost of an opcode X?

Isn’t that the same as decreasing the cost of all opcodes/constants except X and decreasing the block gas limit ?

That is a backward-compatible way of increasing the cost of an opcode. I wouldn’t care much if the numbers are rounded like 21K or instead they are like 19732. Once you do it once, you won’t feel the pain ever again.![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**holiman** (2020-06-05):

Interesting! I’ll read up more about that!

![](https://ethresear.ch/user_avatar/ethresear.ch/sergiodemianlerner/48/1059_2.png) SergioDemianLerner:

> Why do you want to increase the cost of an opcode X?
>
>
> Isn’t that the same as decreasing the cost of all opcodes/constants except X and decreasing the block gas limit ?

Almost, but not *quite*, because of intrinsic constants such as `2300` (and possibly other hardcoded gas assumptions on layer 2). Let’s say we want to target `SLOAD` as an example. And lower all others. If we let the `2300` remain in-place as is, then we’ve suddenly changed “what can be done on 2300”. And now it would be possible to perform `CALL` on those `2300`.

Further, if we want to do any substantial change, we’d have to also use fractional gas costs, which is another pretty large change.

---

**adlerjohn** (2020-06-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/matt/48/4560_2.png) matt:

> Any prior art on this subject?

Section 9 of this paper: https://bitcoin.org/bitcoin.pdf.

---

**pipermerriam** (2020-06-08):

I’m going to get another write-up on this done later this week but right now, the most promising approach I’m seeing is:

1. Separate “gas payer” from “transaction sender”

Exact mechanism still TBD

Extend transaction format to allow optional “gas payer” signature.  This change must be backwards compatible since there is a LOT of existing tooling and infrastructure bound to the current format.
2. Aimed at replacing the existing meta-transaction mechanism.  Would need to be rolled out ASAP to give time for migration from old “deprecated” approach.
3. Need to investigate whether we also need in-protocol atomic batching of transactions.
4. UNGAS:

Breaks current meta-transaction mechanism
5. Allows us broader latitude to reprice operations (specifically for witness gas accounting)
6. Will need to do analysis to find what contracts will break and address those breakages individually as we become aware of them

It *appears* that with these two changes we get the freedom to reprice opcodes for witness gas accounting and better mechanism for implementing meta-transactions.  Next steps are 1) validating that there isn’t something missing here and 2) starting work on formalizing the specifications for both of these changes with specific thought towards getting the decoupling of gas-payer/txn-sender into a fork asap since there will be a need for time between rolling that out and rolling out UNGAS to give people time to upgrade.


*(3 more replies not shown)*

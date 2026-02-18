---
source: ethresearch
topic_id: 7394
title: "Oil: adding a second fuel source to the EVM (pre-EIP)"
author: suhabe
date: "2020-05-11"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/oil-adding-a-second-fuel-source-to-the-evm-pre-eip/7394
views: 4772
likes: 16
posts_count: 19
---

# Oil: adding a second fuel source to the EVM (pre-EIP)

This proposal is for adding a second fuel source to the EVM called **oil** that is unobservable and works in parallel with gas. The idea was originally devised by [Alexey Akhunov](https://ethresear.ch/u/AlexeyAkhunov/), and the name of oil was suggested by [Griffin Hotchkiss](https://ethresear.ch/u/gichiba/summary). Thanks to Martin Swende for the encouragement to pursue the idea.

# Motivation

- Gas is currently being used for two different purposes:

To pay for compute, memory, and storage resources
- To prevent re-entrancy by hardwiring the amount of gas a call can use.

Adjusting the gas schedule to better reflect resource usage causes unintended consequences because contracts may be written in a way such that correctness depends on a specific gas schedule.

- Making an instruction cheaper may make a re-entrancy path feasible
- Making an instruction more expensive may make a call fail because the amount of gas hard-wired to it is now insufficient to execute the call

Oil is a new fuel source that works very similarly to gas, but works in parallel to it.

# Specification

- A transaction has a gasLimit and gasPrice.
- Currently, a transaction pays E ether for allocating gasLimit amount of gas to the transaction based on the gasPrice.
- With oil, a transaction pays E ether for allocating gasLimit amount of gas to the transaction based on the gasPrice, and additionally oilLimit amount of oil to the transaction where oilLimit is set equal to gasLimit.
- A transaction still only specifies a gasLimit. The EVM will internally set the oilLimit to be the same as the gasLimit specified by the transaction.
- Gas metering and gas semantics do not change.
- If the transaction runs out of oil at any point during execution, the transaction reverts. Unlike with gas, where out-of-gas reverts only the current frame, and lets the caller examine the result, out-of-oil always reverts the entire transaction (all frames).
- A caller contract cannot restrict how much oil a callee contract can use, unlike gas.
- The oil cost of all instructions is exactly the same as the gas cost, until further EIPs to modify oil schedule to reprice EVM operations.
- An OIL instruction to read current oil will not be added, and this is intentional.
- The amount of ETH refunded for a transaction is now calculated using the minimum of the unused oil and unused gas, rather than just unused gas.

If the transaction has an EVMC_SUCCESS status code, the sender is refunded the amount of ETH that is the minimum of the remaining gas and remaining oil in the state, exchanged at the gasPrice.
- Similarly, if the transaction has an EVMC_REVERT status code, the state is reverted as usual, and the sender is refunded the amount of ETH that is the minimum of the remaining gas and remaining oil in the state, exchanged at the gasPrice.

# Example

Consider the following two contracts where contract `A` is stored at address a and contract `B` is stored at b. Initially, let the gas cost of each instruction equal the oil cost of each instruction.

```auto
contract A {
    function set(B b) public {
        b.set();
    }
}
contract B {
    uint public amount;
    function set() public {
        amount = address(this).balance;
    }
}
```

Suppose a transaction TX_1 is sent to A to invoke `A.set` on B with initial gas G_{init}, where G_{init} is set to exactly the gas cost of executing  a`.set(`b`)`. Then, the initial oil O_{init} would be equal to G_{init} and the transaction would be accepted.

Now, suppose the oil cost of the `BALANCE` opcode is increased and that a TX_2 is sent that is identical to TX_1. This transaction TX_2 would get rejected with an out-of-oil error because the total oil cost would exceed O_{init}.

## Replies

**pipermerriam** (2020-05-11):

For those of us who have been present for this topic I think the context here will be understood, but I suspect for others the intent of this change will not be obvious.  Can you go into more detail on the subsequent changes where we might increase/decrease oil costs?

---

**suhabe** (2020-05-11):

The intent of oil is to be able charge for the size of the block witnesses in Eth1.x while maintaining backwards-compatibility with existing contracts which make hard-wired assumptions about gas costs.

---

**dankrad** (2020-05-12):

Sounds like a significant amount of technical debt to accumulate. How much confusion will this add for a new developer to be onboarded to Ethereum?

Where does the analysis come from that changing gas costs would lead to that much trouble, warranting the introduction of oil?

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/s/278dde/48.png) suhabe:

> The amount of ETH refunded for a transaction is now calculated using the minimum of the unused oil and unused gas, rather than just unused gas.

If “oil” is supposed to be the successor of gas, shouldn’t it just be the oil that’s refunded? Why the minimum of the two?

---

**AlexeyAkhunov** (2020-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Sounds like a significant amount of technical debt to accumulate. How much confusion will this add for a new developer to be onboarded to Ethereum?

Well, we can’t have it all. We have a legacy system to maintain, and yes, that means doing things in addition to rather redesigning everything from scratch. For the new developers, I would suggest concentrating on oil, because, if introduced and used, it will probably replace gas in most cases.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Where does the analysis come from that changing gas costs would lead to that much trouble, warranting the introduction of oil?

The analysis comes from the very rough estimations of how much we would need to charge for block witnesses, and that charge might not be very well apportion-able to the opcodes (for example, I think it was a mistake to introduce 3 different costs for SSTORE depending on the context, it should have been done via something like oil, and opcodes should have context-independent costs).

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> suhabe:
>
>
> The amount of ETH refunded for a transaction is now calculated using the minimum of the unused oil and unused gas, rather than just unused gas.

If “oil” is supposed to be the successor of gas, shouldn’t it just be the oil that’s refunded? Why the minimum of the two?

We could have said just refund oil, but saying it will be minimum is just more general, because it will also cover the cases where oil cost is smaller than gas cost.

---

**dankrad** (2020-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> We could have said just refund oil, but saying it will be minimum is just more general, because it will also cover the cases where oil cost is smaller than gas cost.

But this would run counter your suggestions of new developers just having to learn about oil. That’s why I would suggest just refunding oil.

---

**dankrad** (2020-05-12):

What about this counterproposal: “Oil” is simply computed from the total cost of all bytes of authenticated data (data+witnesses) required by the transaction (at a TBD cost per byte). In the “SSA” paradigm this would be deterministic and determined by the transaction sender. The “oil” cost is is initially subtracted from gas, and at any point when remaining gas is queried in the EVM, this cost is already completely discounted.

---

**AlexeyAkhunov** (2020-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> But this would run counter your suggestions of new developers just having to learn about oil. That’s why I would suggest just refunding oil.

I see. Yes, agreed, it makes sense

---

**AlexeyAkhunov** (2020-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> What about this counterproposal: “Oil” is simply computed from the total cost of all bytes of authenticated data (data+witnesses) required by the transaction (at a TBD cost per byte).

The oil expenditure during tx execution needs to be metered, for the same reason the gas expenditure needs to be. And the size of the data+witnesses is not known in advance. And I do not think we can make introduction of SSA paradigm a pre-requisite for Stateless Ethereum project, it would increase the scope quite a lot

---

**dankrad** (2020-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> And I do not think we can make introduction of SSA paradigm a pre-requisite for Stateless Ethereum project, it would increase the scope quite a lot

Well, there is the following “weak form” of SSA: The transaction sender is responsible for including all data+witnesses they think will be required by the transaction, and sign this data. Should any other data be required, the transaction fails. I’d guess this would work for almost all Eth1 transactions, if you include some additional data as “backup” in case other branches of the code are taken?

Though it would mean you have to be very careful interacting with some contracts, but maybe we can just have a convention (similar to the ABI json) on a contract interface that specifies which data should be included to “safely” call the contract.

Strictly speaking, my proposal could also work in the DSA world, though then you could not provide the gas already consumed through the EVM opcode and can only subtract it at the end. But I feel like if we are already introducing another concept like “oil”, we might as well directly make the cost dependent on what we’re trying to tax (which is witness sizes) rather than going roundabout and charging it per opcode. The latter I though was a workaround for playing only with gas costs and not introducing a new concept.

---

**AlexeyAkhunov** (2020-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> I’d guess this would work for almost all Eth1 transactions, if you include some additional data as “backup” in case other branches of the code are taken?

Well because it would not work for all Eth1 transactions is the reason I do not believe we can introduce such scheme. Because those transactions for which it does not work, can be viewed as a security issue. For example, someone discovering an “entrapment” attack, where the user has no way of creating a valid tx (because the attackers controls a lot of nodes and can inject their txs quicker), until it pays a ransom to the attacker

---

**dankrad** (2020-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> Well because it would not work for all Eth1 transactions is the reason I do not believe we can introduce such scheme. Because those transactions for which it does not work, can be viewed as a security issue. For example, someone discovering an “entrapment” attack, where the user has no way of creating a valid tx (because the attackers controls a lot of nodes and can inject their txs quicker), until it pays a ransom to the attacker

OK, I see the problem. However, I would then argue that we should simply use “oil = gas + (authenticated data size)*(authenticated data cost)” instead of adjusting individual opcodes.

---

**AlexeyAkhunov** (2020-05-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> OK, I see the problem. However, I would then argue that we should simply use “oil = gas + (authenticated data size)*(authenticated data cost)” instead of adjusting individual opcodes.

That is the plan actually.

However, the oil will also be quite useful for adjusting the costs of individual opcodes if we see them being underpriced

---

**dankrad** (2020-05-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> That is the plan actually.
> However, the oil will also be quite useful for adjusting the costs of individual opcodes if we see them being underpriced

Aha, I see. That was not clear to me from the post. However, to keep things as simple as possible, I would say that adjustment to opcode costs should still be made via gas. Since they have happened in the past, contracts not being able to cope with small adjustments in the gas schedule are clearly buggy.

---

**AlexeyAkhunov** (2020-05-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Since they have happened in the past, contracts not being able to cope with small adjustments in the gas schedule are clearly buggy.

The adjustments are never small ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) otherwise it is not really worth doing

---

**holiman** (2020-05-15):

Thanks for writing this up! However, I totally missed that you had done so, and headed to the 1x discord to present my own write-up of the ‘basically same idea’.


      [gist.github.com](https://gist.github.com/holiman/8a3c31e459ee1bff04256bc214ea7f14)




####

##### Gas and Karma.md

```
# Gas And Karma

## Background

Previously, I made a proposal: [EIP-2583](https://github.com/ethereum/EIPs/pull/2583), which would add a penalty for certain operations, namely ops that caused trie misses.

The proposal would have "kind of" worked, but with some caveats:

1. The maximum enforceable 'penalty' would be on the order of 800,
2. There was a low (but not impossible) chance of breaking some contract flow
```

This file has been truncated. [show original](https://gist.github.com/holiman/8a3c31e459ee1bff04256bc214ea7f14)








In hindsight, it was good that I didn’t fully read your proposal before I did, because it’s interesting to see where the specifications differ (my writeup is not so much a spec, more of a high level overview).

In essence, my writeup  is from a different perspective, and it just happens to coincide with the goals of stateless ethereum!

---

**holiman** (2020-05-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/s/278dde/48.png) suhabe:

> The oil cost of all instructions is exactly the same as the gas cost, until further EIPs to modify oil schedule to reprice EVM operations.

I avoided this in my idea, and let the `oil`/`karma` be zero, unless explicitly set, for those operations which we want to focus on.

If you charge equally for them, there are a couple of complications:

1. The global gas refund counter. Do we also refund oil?
2. Sometimes an op cost a lot more than the available gas.

- For example, I have 100 gas and 500 oil. Now, if I (try to) allocate memory to the cost of400 , then my 100 gas will be deducted. Does it still cost only 100 oil?
- Similary, if we want to (as I do) penalize trie misses, then we need to be able to deduct N units of oil, but only M<N units of gas.

---

**holiman** (2020-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Since they have happened in the past, contracts not being able to cope with small adjustments in the gas schedule are clearly buggy.

If we’re forced to choose between “don’t upgrade gascost” and “upgrade”, then I agree we would eventually find ourselves in a position where we *have* to update them, and contracts *would* break, and there’d be a shitstorm, and we’d just have to accept it.

However, the reason I’m so optimistic about this scheme, is that it allows us to have the best of both worlds – with the caveat that yes, it adds complexities to the consensus engine in general. But it gives us *so* much more freedom to modify costs.

---

**dankrad** (2020-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/holiman/48/4014_2.png) holiman:

> However, the reason I’m so optimistic about this scheme, is that it allows us to have the best of both worlds – with the caveat that yes, it adds complexities to the consensus engine in general. But it gives us so much more freedom to modify costs.

It’s not the complexities in the state machine that I worry about. It’s the added difficulty of onboarding new developers to this complexity – and having to explain to them that “there’s gas, which you can inspect, BUT THEN IT GETS MODIFIED, and then there’s oil, which you can’t inspect, but which actually counts”.

This is horrible. And there’s no way to abstract it away. That’s why I would prefer to make oil as simple as possible – ideally just counting bytes in the witness – and *not* make any additional adjustments to opcodes.


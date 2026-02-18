---
source: magicians
topic_id: 4270
title: "Oil: adding a second fuel source to the EVM (pre-EIP)"
author: suhabe
date: "2020-05-11"
category: Working Groups > Ethereum 1.x Ring
tags: [evm, eth1x]
url: https://ethereum-magicians.org/t/oil-adding-a-second-fuel-source-to-the-evm-pre-eip/4270
views: 1535
likes: 13
posts_count: 15
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
- Currently, a transaction pays $E$ ether for allocating gasLimit amount of gas to the transaction based on the gasPrice.
- With oil, a transaction pays $E$ ether for allocating gasLimit amount of gas to the transaction based on the gasPrice, and additionally oilLimit amount of oil to the transaction where oilLimit is set equal to gasLimit.
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

Consider the following two contracts where contract `A` is stored at address $a$ and contract `B` is stored at $b$. Initially, let the gas cost of each instruction equal the oil cost of each instruction.

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

Suppose a transaction $TX_1$ is sent to $A$ to invoke `A.set` on $B$ with initial gas $G_{init}$, where $G_{init}$ is set to exactly the gas cost of executing  $a$`.set(`$b$`)`. Then, the initial oil $O_{init}$ would be equal to $G_{init}$ and the transaction would be accepted.

Now, suppose the oil cost of the `BALANCE` opcode is increased and that a $TX_2$ is sent that is identical to $TX_1$. This transaction $TX_2$ would get rejected with an out-of-oil error because the total oil cost would exceed $O_{init}$.

## Replies

**gcsfred2** (2020-05-11):

Would you consider another noun that is “greener” besides “oil”?

---

**AlexeyAkhunov** (2020-05-11):

sure, what is your suggestion?

---

**gcsfred2** (2020-05-11):

What about jouleth? It alludes to the joule, which a unit of energy.

---

**AlexeyAkhunov** (2020-05-11):

Sounds cool, lets see what other people think

---

**jpitts** (2020-05-11):

“Liquid” might be a good one, given that “Plasma” is already taken ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

But actually “gas2” may be easier on everyone (following the convention of the CREATE2 opcode), even if it is boring. In client and dapp code gas2 would clearly show which version any related functionality is referring to, and also leaves the space open for future additions. Also, documentation and other resources order terms alphabetically .

---

**AlexeyAkhunov** (2020-05-12):

when I started off, I tried to use the term “gas2”. But it turned out quite confusing when you talk about it. Because people who are listening cannot clearly set apart “gas1” and “gas2”, and the person explaining tends to often conflate them while speaking. That is why a distinct enough name helps

---

**gichiba** (2020-05-12):

Ha! Sorry that the discussion started out about the naming and not about the actual proposal! But since we’re here I’ll just lightly defend using ‘oil’ (thanks for the h/t):

In a [two-stroke engine](https://en.wikipedia.org/wiki/Two-stroke_engine) one must put into the tank a mix of mostly gas and a little bit of oil, because the engine is designed in such a way that prevents the crankcase from having its own lubrication (as is the case in more complex four-stroke engines). Gas provides the energy for the piston to move, and oil reduces the friction that might cause the piston to halt.

Since ‘gas’ is an established and relatively intuitive metaphor for powering a virtual stack machine humming along, ‘oil’ fits quite nicely into this proposal, as both gas and oil go into the same ‘combustion chamber’ of an EVM execution, but once inside they are meant to perform slightly different yet related functions. Gas is required for execution and system resources (out of gas), while oil is required to prevent re-entrancy and ‘frictions’ within contract calls (out of oil).

---

**jpitts** (2020-05-12):

I’m sorry for my part in it too [@gichiba](/u/gichiba)!

Usually I am averse to these kinds of analogies, but when I first read the proposal I did think that the name refers to the relationship between gas and oil in engines.

This is a very good TL;DR. Something similar might be added at the top of the EIP to help people understand the distinction:

> gas and oil go into the same ‘combustion chamber’ of an EVM execution, but once inside they are meant to perform slightly different yet related functions. Gas is required for execution and system resources (out of gas), while oil is required to prevent re-entrancy and ‘frictions’ within contract calls (out of oil).

---

**rumkin** (2020-05-12):

In my opinion transaction must be completely reverted every time gas runs out. It’s required to preserve consistency of the contract state. And contract developer should be able to define an edge-case when out of gas error from underlying call shouldn’t be propagated up. To prevent reentrancy there should be a call stack available from runtime. Reentrance-friendly methods should be specified explicitly.

The oil proposal indicates that current behaviour is tricky and is a thing to fix.

---

**AlexeyAkhunov** (2020-05-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rumkin/48/1330_2.png) rumkin:

> The oil proposal indicates that current behaviour is tricky and is a thing to fix.

Agreed. There was a proposal to just modify the semantics of gas, but this is going to be so breaking that the only practical way to introduce such as change would be versioning. Which is the thing we would like to avoid if we can. Introducing oil first and then, when it catches on, deciding when gas can be deprecated, and then removed, could be a viable path

---

**AlexeyAkhunov** (2020-05-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gichiba/48/870_2.png) gichiba:

> Gas is required for execution and system resources (out of gas), while oil is required to prevent re-entrancy and ‘frictions’ within contract calls (out of oil).

Well, oil would not anything about re-entrancy. Neither should gas be used for the purpose of preventing re-entrancy, but it is in some cases. Re-entrancy is a bit of a distraction here, I think, so I would not emphasise it in an analogy

---

**AlexeyAkhunov** (2020-05-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> Usually I am averse to these kinds of analogies, but when I first read the proposal I did think that the name refers to the relationship between gas and oil in engines.

I am averse to the OVER-use of analogies even in this case. The reason I like “Oil” is simply because it is a short name, and it is distinct enough from gas, so you are less likely to confuse which one is which when explaining

---

**_bl0ckhead** (2020-05-14):

I want to echo the objection to using the term “oil”. While it does have somewhat of an engine analogy it also continues to normalize the dependency on petrochemicals.

Perhaps “Calories” or “Carbs” instead?

---

**gichiba** (2020-05-15):

Both the terms ‘gas’ and ‘oil’ could serve as a reminder that the EVM is (for the moment) running atop a Proof-of-Work chain, which literally throws away energy in order to be secure…

But yes, I have said my piece about the name, and I hope the name is the most controversial thing about this proposal. Please consider its merits regardless of what this second gas-analog is called


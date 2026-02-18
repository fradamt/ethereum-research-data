---
source: magicians
topic_id: 822
title: "EVM Idea: Implement deferred and recursive execution"
author: seliestel
date: "2018-07-20"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/evm-idea-implement-deferred-and-recursive-execution/822
views: 1691
likes: 0
posts_count: 9
---

# EVM Idea: Implement deferred and recursive execution

We ([@aribo](/u/aribo) and [@seliestel](/u/seliestel)) have been discussing an idea to make some functions self executable. This would allow the deployment of contracts that execute in the future without an explicit call/send by an external agent. The objective is to create the potential for autonomous code running on the EVM. Of course, this would need to come with a cost and some limitations, in order to protect the network from potential complications and abuses.

The proposal is to create a new opcode ‘SELFCALL’ with four arguments:

p (position to mem where the bytecode to be executed is located),

initial block (set when the contract is created),

interval (number of blocks between executions, set in the contract code), and

gas price (price of gas to be paid at execution, set in contract code).

The EVM would need to calculate the difference between the current block number and the initial block. If this difference modulo interval is 0, the SELF bytecode located in p would be executed.

This opcode could be translated as a specific type of function modifier in Solidity, e.g. self. This modifier could be added to any function we want to self execute in the future.

SELF functions will be executed by the EVM every time a new block is mined, only if they have enough ether available. SELF functions would need to pay a set amount of gas every time they are called regardless of the computations they perform - basically the cost of the opcode. Moreover, the EVM would execute the SELF function as long as there is enough ether to pay the gas spent by its execution.

Some SELF functions would never be called because they have run out of allocated ether. Others might be called and pay the set amount of gas, but then result in no computation or change of state (for example, an alarm clock that begins with a require statement and only runs when a certain time has been reached). Finally, some SELF functions would incur an additional cost in ether as they are executed by the EVM when called.

An example of a SELF function in solidity:

function wakeUp self(uint 5, uint 10000) {

require (now == wakeUpTime);

doSomething();

}

The SELF function wakeUp would be called by the EVM every 5 blocks since the contract was first constructed. It would pay 10,000 wei per gas for its execution. The cost in gas of calling the SELF function would be standarized. If the time now is less or more than wakeUpTime the function would do nothing and it would only have to pay in ether the set amount for being called. If wakeUpTime has been reached, it would need to pay in addition the cost in gas of running the function doSomething().

[@seliestel](/u/seliestel)

[@aribo](/u/aribo)

This has been opened as an issue in EIP github repo: https://github.com/ethereum/EIPs/issues/1230

## Replies

**flygoing** (2018-07-20):

A couple notes:

1. Needs a few more arguments. v, length of the data starting at location p. gasLimit, the max amount of gas the call should use.
2. I think it would make more sense for SELFCALL to schedule a call at a specific block, not do a permanent schedule. So instead of interval, just have one block to do it at. That later call could then schedule another call, recurvisely. This would also come with removing initial block since it would be absolute blocks instead of an interval.
3. Gas price might need some more thought. If the scheduled calls are required to be executed by the miners, then what stops me from setting a 1 wei gas price on the future call? On the other hand, if the calls are optional for the miners, then why even have deferred calls at all? Just do them externally with something like the ethereum alarmclock.
4. The self syntax example you give in Solidity is confusing because that’s just what a modifier looks like. It’d probably have to be something switched around like this if you kept with intervals

```auto
function self(5, 10000) wakeUp {
    require(now == wakeUpTime);
    doSomething();
}
```

If you removed the intervals it’d probably look more like this

```auto
function doSomething(uint foobar) {
    //Do some things
    schedule(doSomething(foobar), 6000000, 10000, 100000);
}
```

Where the parameters are function/data, block number, gas price in wei, and gas limit. I’m not sure how the `schedule` syntax would actually work, it’s a little weird to have the doSomething(foobar) as a parameter to the function without actually calling doSomething.

---

**aribo** (2018-07-20):

Thanks a lot [@flygoing](/u/flygoing) for your comments.

1. I can see the need for gasLimit > g. About v, perhaps it’d be better to indicate it as size of bytes to be executed s.
2. I see your point re indicating a call block, yet not sure how how it could be made recurrent in the original contract without a set interval.
3. I see SELFCALL as self-transactions called by the same contract. So miners will decide to include them in blocks in the same way they include other transactions: they have enough credit to pay for the necessary gas to process at a set price. If I’m the owner of the contract and I set the gas price of the SELFCALL at 1 gwei I run the risk that the call (the self-transaction) is never mined or it has a long delay. Bear in mind that the SELFCALL is not necessarily ‘executed’ in the interval indicated, it’ll be called but it’ll be included in a block according to the same criteria as other transactions.
4. I still prefer the use of a function type self in Solidity in the same way that we use ‘public/private’ or ‘internal/external’. Nevertheles, the discussion about how SELFCALL would be translated into Solidity or Vyper is a different one.

I’d like to underline a point I mention above: SELFCALL doesn’t execute the functions, it makes a call for inclusion of this execution (a call) in a block. The contract is the sender of the call to execute the indicated bytes, it actually sends/makes a transaction. So from that point it works the same way (gas and block inclusion) as any other transaction.

---

**flygoing** (2018-07-20):

[@aribo](/u/aribo)

1. I only said v because that’s the solidity assembly notion for calldata length when using CALL and friends. It doesn’t really matter for the evm/yellow paper either way.
2. The constructor could call SELFCALL for a future block, and calls whatever function need be called. That function could then check
3. I don’t see the point of SELFCALL if it’s optional, though. What’s the difference between having calls scheduled by contracts and having external something like the Ethereum Alarm Clock? SELFCALL would add bloat to the base layer while providing no use over doing this on a second layer like EAC

Side note, how would you handle ordering? If the contract schedules 2 transactions (or creates an interval call), what happens if the first transaction scheduled isn’t mined, but a miner wants to mine the second tx? Are they ordered like nonces?

Edit: Also, if the contract creates an interval selfcall, what if the gas price market rises to a point where the set interval price realistically will never be called again?

---

**Spaded** (2018-07-21):

I see a potential issue where I can make a thousand SELFCALLs and they would be stored in the mempool to be unleashed all at once.

Needs to have some checks to ensure you cannot  pre-plan a DDOS.

Also, how are these SELFCALLs going to be stored during the delay period?

---

**adibas03** (2018-07-23):

I support the **block** target as against the interval. Using a **nextBlock** variable, which is updated every time the call is executed, in case of intervals.

Also, miners should be able to optin or optout of executing selfcalls, as they can very easily be a source of attacks.

Running through a rough process flow:

- SELFCALL created, with target (next Block)
- Miners store the information locally (Memory or Disk), to keep track of what blocks to watch out for (Should definitely not be maintained on the chain, sure sources of attacks)
- When a target block is hit, the conditions are checked and the miner triggers the functions and mines the transaction
- Miner updates locally maintained list

This is very similar to the present implementation of the Ethereum alarm clock, in its present state.

The next question would be, why does the protocol have to care about this, if there is an existing Identical model.

---

**tjayrush** (2018-07-24):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/e79b87/48.png) seliestel:

> SELF functions will be executed by the EVM every time a new block is mined, only if they have enough ether available.

For me, this line kills this idea. What happens if this opcode becomes successful, and everyone starts using it. Over time, this will bog down the chain because the list of things to do at each block will continually grow. If 1,000,000 smart contracts use the `self` opcode, at every block, it has to check 1,000,000 balances? That can’t possibly work, and it only gets worse over time. Sorry if I’ve missed something.

---

**d10r** (2018-07-26):

Having arbitrary deferred functions seems to be very tricky.

What’s however feasible: kind of emulate deferred execution by modeling state less explicitly and by taking advantage of “free” state updates like the timestamp in every new block. I’ve used this strategy to build a “streamable” ERC-20 token: https://github.com/lab10-coop/streem-poc

The concept can be generalized to some degree, however I haven’t yet managed to document all my thoughts about it.

---

**nootropicat** (2018-07-27):

This can be emulated off-chain: a function that when called in a future block executes + rewards the caller with some ether. Once its existence becomes widely known, someone (probably miners) will always execute it as long as the reward is high enough.


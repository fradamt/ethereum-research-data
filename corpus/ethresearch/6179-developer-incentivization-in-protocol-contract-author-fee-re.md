---
source: ethresearch
topic_id: 6179
title: "Developer incentivization: in-protocol contract author fee rebates"
author: vbuterin
date: "2019-09-22"
category: Economics
tags: []
url: https://ethresear.ch/t/developer-incentivization-in-protocol-contract-author-fee-rebates/6179
views: 3447
likes: 8
posts_count: 6
---

# Developer incentivization: in-protocol contract author fee rebates

This is a simple proposed scheme for incentivizing the development of software libraries for ethereum (this can be implemented in an eth1 or eth2 context; the scheme is fairly agnostic). Example “ideal beneficiaries” of this include authors of:

- Wallet contracts
- Standard libraries
- Weierstrudel and other optimized implementations of algorithms

Both schemes assume [EIP 1559](https://github.com/ethereum/EIPs/issues/1559) is included, so there is a “burned fee” associated with every unit of gas consumed; this is important to prevent cheating by miners.

### Scheme 1

When a contract is published, the author of the contract (ie. the account that published it) is stored. Every time a contract call finishes, X% (eg. 33%) of the burned fee associated with the gas executed inside the callee is transferred to the creator of the callee.

### Scheme 2

Let `T` be the previous total amount of ETH fees burned from gas spent executing a given contract with byte length L, and N be the burned fee associated with the gas spent executing a contract call to that contract. When that call finishes, transfer L * (f(\frac{T + N}{L}) - f(\frac{T}{L})) ETH to the author (notice that this is just f(T + N) - f(T) but stretched horizontally and vertically by a factor of L). In general, f should be a function with the following properties:

- f'(0) = 0
- lim_{x \rightarrow \infty} f'(x) = \frac{1}{2}
- f'' \geq 0

The idea is that we have a superlinear rebate, which starts off at zero, then grows over time and eventually approaches 50% of the burned fee. The inclusion of L in the calculation is there to “stretch out” the function for larger contracts, making the point at which the rebate approaches 50% proportional to the contract side; this prevents manipulation via combining or splitting contracts. One simple candidate for f is f(x) = \frac{x^2}{4M} for x < M and \frac{M}{4} + \frac{x-M}{2} for x \ge M:

[![Untitled%20Diagram](https://ethresear.ch/uploads/default/original/2X/3/3c84a80960e31476618a1c6332423bac6bf3f0f5.png)Untitled%20Diagram482×242 2.51 KB](https://ethresear.ch/uploads/default/3c84a80960e31476618a1c6332423bac6bf3f0f5)

The goal of the superlinear rebate is to add a check against copying a contract and replacing the developer’s rewards with your own. Such a tactic would not be profitable unless you can get many users using your contract.

### Notes

Note that Scheme 1 is, from a purely economic “tax/subsidy incidence” analysis, a no-op: developers could theoretically undercut each other by providing some portion of their rebates back to users through some extra-protocol mechanism, and the Bertrand competition equilibrium of this is zero returns to the developer. However, the goal is that this would be hard to do, and not worth it in the bulk of cases because the per-transaction fees involved are tiny, and the hope is that if the community agrees that such competition is harmful then there would not be effective infrastructure built to support it.

A long run sustainable fee level on ethereum today is [about 500 ETH/day](https://etherscan.io/chart/transactionfee). If 80% of total fees get burned through EIP 1559, and 70% of that is calling contracts ([gas used per day](https://etherscan.io/chart/gasused) - (21000 - 6800) * [transactions per day](https://etherscan.io/chart/tx) - 68 * [blocks per day](https://etherscan.io/chart/blocks) * [average block size](https://etherscan.io/chart/blocksize) as a fraction of total gas used per day roughly gives this, and it’s likely a low estimate due to zero bytes in blocks), and on average the rebate is 25% then this gives 70 ETH/day ($14000 per day or $5 million per year) to contract authors, *at present fee levels*.

## Replies

**jgm** (2019-09-22):

It would be great to find a way of doing something like this, less repetitive code on-chain would be nice.

Is there a significant financial incentive for contract writers to use libraries?  There are a number of technical reasons to use a library (reduced development time, battle-tested code, *etc.*) but all of these are in place today and yet I rarely see code that refers to on-chain libraries.

How would this stop developers from building the bulk of their contract as a library and then calling it from a thin layer that is the public face of the contract, thus reclaiming a chunk of fees and creating an incentive for them to build inefficient code?

---

**vbuterin** (2019-09-23):

> How would this stop developers from building the bulk of their contract as a library and then calling it from a thin layer that is the public face of the contract, thus reclaiming a chunk of fees and creating an incentive for them to build inefficient code?

This would indeed be an optimal strategy for commonly used applications, but that’s ok; the bloat from a few commonly used applications not reusing code is small. It would be risky for not-commonly-used applications to copy code into their own contract, as while the maximum rewards are higher it would take longer for them to reach the maximum level of reward.

---

**Mikerah** (2019-09-23):

The [ethPM](https://www.ethpm.com/) project can definitely serve as a foundation for this. It doesn’t get much visibility for whatever reason

---

**haimbender** (2019-11-19):

I like it!

But 5 mill is like 15 fb grade developers, the more you make it the more it will grow.

Another Q: what if your calling someone elses contract, then ur paying that guy? I would never do that if i can just copy the code and get the payment myself, so theres bot going to be a lot of code reuse

---

**wudiruby** (2019-11-20):

Hi Vitalik,

It’s would be great to incentive the developers, either from the block reward, or from the gas fee.

I read your previous idea to putting the gas fee into a DAO, and here we would like to propose an algorithm to distribute the fund in the “DAO” to the smart contract developers automatically. The algorithm is inspired by your quadratic voting idea but made some adjustment to address the concern of the resistance on “sybil attack”.

we have briefly code the algorithm [here](https://github.com/ASResearch/uPRE/tree/master/runtime/dip):

Key highlights on the algorithm as below, full paper [here](https://www.asresearch.io/#/detail/2) :

1. The part of new-block rewards within a period (with total amount M) are used for incentivizing developer. This does not matches your idea that part of the gas fee for invoking a smart contract are transferred to the developer. However, it is applicable for scenarios such as to govern a certain amount of community funds in a DAO. The protocol then gives an algorithm to distribute M to smart contracts’ developers.
2. Each address has a certain amount of voting power, which is determined by the address’s value to resist against Sybil attack (there are various ways, e.g. simply use the address’s stake. In our propose, it consists of the median stake and the in-and-out degree), for more details about how we compute the voting power, can check for the paper (not allowed to put more link  )
3. invoke to vote: within a period, an address’s voting powers are proportionally distributed to smart contracts according to the number of invocations from the address.
4. quadratic ballot : each smart contract’s ranking score is the sum of square roots of its’ received voting powers. That is, if a user casts 9 votes to a smart contracts, the actual contribution to its ranking score is 3, similar to the quadratic voting.
5. The final reward M is proportionally distributed to DApps’ developers according to the square of DAPP’s ranking scores, to resist split DApp attack.

The key idea of the protocol is to resolve the issue that quadratic voting is insufficient to resist sybil attack, it can be proved mathematically that it is resistant for split DApp attack and is hard for bribery.

Happy to discuss further ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)


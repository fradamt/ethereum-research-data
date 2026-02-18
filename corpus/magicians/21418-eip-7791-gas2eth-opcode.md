---
source: magicians
topic_id: 21418
title: "EIP-7791: GAS2ETH opcode"
author: pcaversaccio
date: "2024-10-20"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/eip-7791-gas2eth-opcode/21418
views: 1440
likes: 59
posts_count: 40
---

# EIP-7791: GAS2ETH opcode

# EIP-7791: GAS2ETH opcode

## Abstract

This [EIP](https://eips.ethereum.org/EIPS/eip-7791) introduces a new `GAS2ETH` opcode that enables the direct conversion of gas/mana into ether (ETH).

## Motivation

This EIP is based on the premise that smart contract authors and compiler teams should be compensated for their contributions. Moreover, their compensation should scale with the usage of their contracts. A widely used and popular contract offers significant value to its users through its functionality and to the network by driving demand for blockspace — Ethereum’s *raison d’être*. This increased demand also benefits miners and validators, who are rewarded for executing these contracts.

Monetizing smart contracts in a scalable manner remains challenging at the time of this writing. This difficulty is evident from existence of many different monetization strategies employed across various smart contracts — ranging from fee structures to the issuance of tokens with “tokenomics” of varying levels of complexity.

Introducing the `GAS2ETH` opcode offers contract authors a new way to achieve their monetization objectives. By charging gas, they integrate with an established user experience that is both familiar and understood by users. The proposed instruction ensures that existing transaction creation and processing tools remain unchanged. Moreover, by charging gas, contract authors align economically with network activity; they benefit from higher compensation during periods of intense network usage and receive less when activity is low. This helps align the incentives of smart contract authors, validators, and the broader network.

## Questions?

Join our [Telegram group](https://t.me/gas2eth).

## Replies

**trebor** (2025-04-02):

Maybe I’m missing something, but can’t this functionality be implemented right now with current opcodes?

```auto
# Push `gas_amount` * `gas_price` to stack
PUSH1 0x01 # `gas_amount`
GASPRICE
MUL

# Call to transfer the value to `addr`
PUSH0
PUSH0
PUSH0
PUSH0
SWAP4
PUSH20 0xaa  # `addr`
PUSH2 0x0834 # 2100
```

I get your point about wanting to use gas as a variable pricing strategy for monetization.  I don’t understand how adding an opcode to simplify already-possible behavior will make people more likely to use this approach.

---

**charles-cooper** (2025-04-03):

The opcode doesn’t just perform a computation. It actually converts gas to ether and sends it. It’s not already possible because existing opcodes deduct ether from the currently executing contract; while GAS2ETH effectively deducts from the transaction originator (or whoever is paying for gas).

---

**fiddy** (2025-04-10):

This is Fiddy, a researcher at Lido and ex-core developer at Curve (DEX). I have a lot of experience building in the application layer, and this particular EIP is *also* very interesting for use cases other than funding smart contract developers. The following statements are independent of my representation, but they are something I deeply stand by.

***Disclaimer: the following is co-authored by an LLM (Google Gemini 2.5 Pro).***

`GAS2ETH` introduces a fundamental mechanism enabling smart contracts to directly convert transaction gas, already paid by the sender, into ETH credited to the contract’s balance. While seemingly simple, this opcode offers a powerful primitive for simplifying on-chain fee structures and reducing operational risks for various applications, particularly those requiring dynamic fee adjustments. I believe this EIP warrants strong consideration and push from the application layer due to its significant potential benefits.

## The Current Complexity of On-Chain Fee Management

Currently, smart contracts needing to implement dynamic fee structures face considerable complexities and inherent risks:

1. Indirect Fee Mechanisms: Contracts often cannot directly charge fees based on network congestion (i.e., gas prices). Instead, they rely on proxy metrics, such as tracking usage frequency via storage variables, to infer periods of high demand or volatility and adjust fees accordingly. This is an indirect and often imprecise method.
2. Fee Token Management: Many protocols, especially Decentralized Exchanges (DEXes), collect fees in the tokens being traded. This necessitates a multi-step, often cumbersome process:

- Accumulation: Fees accrue in various, potentially volatile or illiquid, tokens.
- Conversion: The protocol (or its DAO/operators/keepers) must periodically execute transactions to swap these accumulated fee tokens into a desired base asset like ETH or a stablecoin.
- Risks: This conversion process introduces significant risks:

Market Volatility & Depegging: The value of accumulated fee tokens can drastically decrease between accumulation and conversion due to market fluctuations or events like stablecoin depegs.
- Liquidity Issues & Slippage: Converting large amounts of fee tokens can face insufficient liquidity, leading to significant price slippage.
- MEV Exposure: Fee conversion transactions themselves can be targets for Maximal Extractable Value (MEV), further eroding the collected value.
- Operational Overhead: Managing this process requires dedicated infrastructure, transaction costs, and governance overhead.

## EIP-7791: A Direct and Elegant Solution

EIP-7791 introduces the `GAS2ETH` opcode, offering a direct solution to these challenges.

### Clarifying the Mechanics: GAS2ETH vs. PAY

It is crucial to distinguish the proposed `GAS2ETH` opcode’s function from that of potential complementary opcodes like PAY. Based on discussions surrounding the EIP’s design, `GAS2ETH` leverages the gas already supplied and paid for by the transaction initiator (effectively, the entity covering the transaction’s gas costs: tx.origin). When a contract executes `GAS2ETH(g)`, it consumes g gas provided by the initiator, calculates the equivalent ETH value based on the transaction’s gas price, and credits this ETH to its own balance. Conversely, an opcode like PAY would serve a different purpose: deducting ETH from the current contract’s balance to transfer it externally, potentially offering benefits like reentrancy protection. Therefore, `GAS2ETH` is about the contract receiving ETH funded by the transaction initiator’s gas, while PAY would facilitate the contract sending ETH from its own reserves. This distinction underscores how `GAS2ETH` enables direct fee capture in ETH from the user interacting with the contract.

Mechanism: A contract executing `GAS2ETH(g)` would:

1. Consume g amount of gas from the transaction’s available gas limit (this gas cost is ultimately borne by the transaction sender as part of their overall gas payment).
2. Calculate the corresponding ETH value based on g * effective_gas_price (using the gas price context of the transaction).
3. Credit this calculated ETH amount directly to the smart contract’s own balance.

Benefits:

1. Intrinsic Dynamic Fees: Fees charged via GAS2ETH are inherently tied to network demand. When blockspace is contested and gas prices are high, the ETH value derived from consuming a fixed amount of gas (g) increases proportionally. This allows contracts to automatically adjust their fee levels based on real-time network conditions without complex logic or storage reads.
2. Simplified Fee Logistics: It entirely eliminates the need to handle intermediate fee tokens. Fees are collected directly in ETH, the network’s native asset.
3. Risk Mitigation: By receiving fees directly in ETH, protocols circumvent exposure to the volatility, depegging risks, liquidity constraints, and slippage associated with converting diverse fee tokens.
4. Reduced Transactional Overhead: The entire process of accumulating, managing, and converting fee tokens is bypassed, reducing the number of transactions required and associated gas costs.

## Use Case: Revolutionizing DEX Fee Structures

Let’s revisit the DEX example:

- Without GAS2ETH: A DEX facilitating a stablecoin pair swap collects fees in those stablecoins. If $500k worth of fees are collected on Friday, market turmoil over the weekend (e.g., a depeg) could reduce their value significantly before they can be converted to ETH on Monday/Tuesday, further impacted by slippage and potential MEV during the conversion swaps.
- With GAS2ETH: The DEX contract could, as part of the swap execution, include a GAS2ETH operation. This consumes a predetermined amount of gas (g) paid by the user initiating the swap. The contract immediately receives the corresponding ETH value (g * tx.gasprice). If network congestion is high (high tx.gasprice), the ETH fee collected is higher, reflecting the increased demand for the DEX’s service during that period. The collected ETH can then be efficiently transferred to a designated withdrawal address, potentially using a complementary mechanism like the PAY opcode (often discussed alongside gas-related EIPs). This entire process is atomic, direct, and avoids intermediate token risks.

## Conclusion and Call for Support

EIP-7791 (`GAS2ETH`) offers a foundational improvement to smart contract economics on Ethereum. By enabling direct conversion of gas cost to ETH revenue for contracts, it provides a robust, elegant, and risk-minimizing mechanism for implementing dynamic fees. This is particularly valuable for high-throughput applications like DEXes, but its utility could extend to lending protocols, NFT marketplaces, oracle services, and others that require a seamless fee management infrastructure.

The primary hurdle for such a valuable, low-level primitive is often demonstrating clear demand and utility from the application layer. Simplifying core economic interactions like fee collection in ETH strengthens the entire ecosystem. I urge developers, protocol designers, and the broader Ethereum community to recognize the potential of `GAS2ETH`, discuss its applications, and voice support for its inclusion in a future network upgrade.

---

**Vectorized** (2025-04-12):

I like this opcode.

It opens a whole new design space for smart contracts. Anything that requires a callback can use this opcode to pay the fees for the callback. No longer do we need the cumbersome `quote` + `msg.value` workflow for stuff like LayerZero.

While it’s technically possible to build this on the application layer, it breaks compatibility with existing routers and onchain superstructures. Additionally, paying via gas allows for transparency and minimal hassle workflows. People know how much they are going to pay. Contrast this with approving and pulling some ERC20 (needs simulation, and fragments liquidity).

To prevent the risk of DDoS via gas recycling, this opcode needs to take a cut of all gas that passes through it. A 10% cut should be Goldilocks.

I have outlined additional advantages of such an approach in a similar RIP [RIP-7767: Gas to Ether Precompile](https://ethereum-magicians.org/t/rip-7767-gas-to-ether-precompile/21005)

---

**charles-cooper** (2025-04-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vectorized/48/7129_2.png) Vectorized:

> To prevent the risk of DDoS via gas recycling,

What do you mean by “gas recycling” here?

---

**Vectorized** (2025-04-12):

The amount of gas burned by a txn will increase the base fees via EIP-1559.

If this opcode refunds all the gas burned as ETH, one can use it to burn gas → get back the full gas → burn gas → get back the full gas …

So we need some decay factor.

---

**charles-cooper** (2025-04-12):

Discussed a bit offline, and the issue is that the opcode can be used to grief the base fee via EIP-1559 mechanics. It’s a good point, and I think the proper fix is to just not allow gas deducted via GAS2ETH to affect the base fee.

I think there are other benefits to the 10% decay factor, but I need to think about it more.

---

**charles-cooper** (2025-04-12):

A couple slightly weird things about this opcode:

- It’s disconnected from gas mechanics, e.g. a contract can call GAS2ETH with arbitrarily large gas.
- A contract can charge GAS2ETH to enable it to take an action it wasn’t able to before, like pass a balance check.

For these reasons, I am considering:

- A limit on how much gas can be consumed with GAS2ETH in a given transaction. It should probably be capped at something like 15% of the entire gas limit of a transaction. This also fixes weird edge cases with eth_estimateGas (like gas consumed at runtime could be wildly different from the estimated gas)
- Only applying the balance changes at the end of the transaction. This could have another benefit of making GAS2ETH cheaper(!), since it removes data dependency in the transaction on the new account value. For instance, in the previous example, the contract could charge GAS2ETH all day, but it still can’t pass the balance check. This pattern of deferring state changes to the end of a transaction has a precedent in historical SELFDESTRUCT behavior, when the account removal was deferred to the end of the transaction.

---

**fiddy** (2025-04-14):

> It should probably be capped at something like 15% of the entire gas limit of a transaction.

I think this could work, however it does kill the various nifty defi use-cases and makes this opcode not very appealing at all. I think a solution must take Defi use-cases into account.

---

**alexfertel** (2025-05-22):

Wrote a [POC implementation](https://github.com/bluealloy/revm/pull/2535) for revm. Wanted to share some feedback on the EIP spec.

The gas calculation section is somewhat confusing: It’s not clear whether the full cost of the opcode is the sum of each branch or each branch is exclusive (I assumed the former).

Also, the " or is `val` zero" in the second branch is unnecessary? Please correct me if I’m wrong.

---

**alexfertel** (2025-05-26):

Great feedback from the POC PR above:

> Imagine only taking into account a priority fee, this would burn more eth than transferred it, and in the end you need to know how much fee got minted/transfered so this is not added as reward to the block builder/beneficiary.
>
>
> And if we want to somehow skip burning of this basefee this effect eip1559 fee mechanism.

In other words, where does the gas burned come from? The answer to this question may have implications that change the EIP.

---

**charles-cooper** (2025-05-27):

Based on some offline conversations, I have had some takeaways that could probably change the EIP:

1. The gas consumed by the GAS2ETH opcode should not affect the EIP-1559 base fee (as mentioned previously in this thread)
2. Maybe the limit to how much can be consumed by GAS2ETH can be set as a new parameter to the transaction.

---

**tim-clancy.eth** (2025-05-29):

I like this idea, but I don’t want to do it with any hacky or arbitrary limits.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> I think the proper fix is to just not allow gas deducted via GAS2ETH to affect the base fee.

Yes. This is much nicer than an arbitrary `X%` decay.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> Maybe the limit to how much can be consumed by GAS2ETH can be set as a new parameter to the transaction.

Would this be a per-transaction requirement for everything that would touch a `GAS2ETH`? This seems onerous but I’d be fine with it if I can go up to some arbitrarily high `100%` (triggering guaranteed transaction failure). Encoding something like a global `15%` is wrongly opinionated.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> A contract can charge GAS2ETH to enable it to take an action it wasn’t able to before, like pass a balance check.

This is how it should work; it is the simple approach.

---

**wjmelements** (2025-05-30):

`GAS2ETH` could add a new gas griefing vector. Previously, gas griefing scammers would mint gas tokens with the victim’s gas. With this opcode they would be able to extract ether.

Briefly, gas griefing works by tricking users into signing transactions with high gas limits. The most recent method I have seen is fake ERC20 approvals, which some wallets will prompt you to revoke. Some users attempt to revoke these approvals many times, trying to clear the warning prompt in their wallet, usually not noticing they are losing large amounts of money to transaction fees.

---

**wminshew** (2025-05-30):

I think this opcode will also open new attack surface area for apps & wallets subsidizing blockchain usage with paymasters, would love to hear any pushback if people think that’s wrong

---

**tim-clancy.eth** (2025-05-31):

My view on this is the same every time: we should never limit the provision of new tools based on potential end user error. Transient storage is important and useful even if it opens footguns for unaware developers to break 4337; compilers and libraries should try to mitigate this. 7702 is important and useful even if it makes certain types of scams easier; wallets should try to mitigate this. 7251 is important and useful even if it makes certain types of scams easier, etc. etc.

---

**u59149403** (2025-06-04):

GAS2ETH will enable gastokens again!

Here is how they will work: first, when gas is cheap, we create a lot of storage cells. Then, when gas is expensive, we clear these cells and also round-trip some ether using GAS2ETH.

Normally clearing cells cannot bring you real ether, because all these refunds are capped at 1/5 of tx fee.

But now we can do this: let’s assume current gas price is 1 Gwei. We round-trip 10 gas via GAS2ETH (i. e. convert 10 Gwei to 10 gas and immediately to 10 Gwei back). And also clear some cells, which brings us additional 1 gas (1 Gwei). Refunds (1 Gwei) is still less than total gas fee (10 Gwei), but in the end we become 1 Gwei richer!

So, GAS2ETH allows one to store gas and convert it to REAL ETH later

---

**u59149403** (2025-06-04):

Let me say the same in other words: if I (i. e. EOA) deploy a contract and then call a method of this contract, which uses GAS2ETH and clears some storage slots (and thus gets rebates), then total cost of calling this method for me may be negative. Thus calling this method will transfer money from stakers to me, i. e. I will steal money from stakers.

And I will be able to earn money from this so: I will create slots when gas prices are low and clear them (together with GAS2ETH) when they are high.

You may say that stakers simply will not include such negatively priced transactions to blocks. Well, builder pipelines, such as Flashbots, probably will not include. But there always exists small fraction of home stakers, who don’t use builder pipelines, and who will include such transactions. So GAS2ETH will enable me to steal money from home stakers! And I will do this, oh, yes, I will do this

---

**charles-cooper** (2025-06-04):

I don’t think this is really stealing from home stakers, since you’re clearing storage for them. But even if this was considered undesirable, we can just disallow GAS2ETH from interfering with the refund computation.

---

**charles-cooper** (2025-08-01):

[@jochem-brouwer](/u/jochem-brouwer) suggested offline having a separate limit for `GAS2ETH` – in other words, it does not deduct from the regular “execution” gas counter, but from its own, gas2eth-specific counter. That way it cannot interfere with gas available to execution.


*(19 more replies not shown)*

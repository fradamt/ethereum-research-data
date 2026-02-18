---
source: ethresearch
topic_id: 22971
title: Proposal for a trust-minimized price oracle
author: j0i0m0b0o
date: "2025-08-25"
category: Economics
tags: []
url: https://ethresear.ch/t/proposal-for-a-trust-minimized-price-oracle/22971
views: 632
likes: 2
posts_count: 3
---

# Proposal for a trust-minimized price oracle

The below oracle is designed to be a trust-minimized and permissionless way to get token prices that anyone can use.

At its most basic level the oracle works by having a reporter submit both a limit bid and ask at the same price. Anyone can swap against these orders minus a small fee (no partial fills). If nobody takes either order in a certain amount of time, it is evidence of a good price that can be used for settlement. If an order is taken, the taker needs to post collateral in both tokens, imply a new price, and the timer restarts.

The oracle uses exponential collateral escalation during disputes to increase the cost of manipulation and give users some statistical guarantees around total time to settlement and cost to delay. In the average case, the capital required to report accurate prices can be much lower than the notional amount settled by the reported price. The goal is to replace the current set of centralized and trusted oracle intermediaries so DeFi applications can have fewer points of failure.

The design relies on 1 of n self-interested participants who are not economically aligned with the external position being settled by the oracle having their transaction included before the deadline.

One of the clear limitations of the design is censorship (submit bad price → censor disputes → profit). This places a hard limit on how much the oracle can secure on L2 and, until FOCIL, we must use longer settlement times on the L1 to reduce the chance of an attacker controlling many blocks in a row.

Below is a simplified example of the oracle life cycle:

Let’s say an application wants the price of WETH against USDC. In the price request, they specify

1. token1: WETH
2. token2: USDC
3. token1Amount: 0.1 WETH
4. settlementTime: 10 seconds
5. multiplier: 1.5x
6. reward: 0.001 ETH

The oracle contract balance is now 0.001 ETH.

This price request gets on-chain and anybody can report a price. Let’s say the price of ETH is $3000. The next step is a reporter submits an initial report, winning the race against everybody else to claim the 0.001 ETH.

Because an application was using the oracle to get a price, we will assume there are two people who are in opposite positions. Meaning, if the price is reported higher, one person benefits and the other loses, and vice versa. Assume one of the people is completely passive, but assume the other is active, and would benefit were the oracle to settle reporting WETH as not as valuable. So assume the initial reporter is the manipulator in this party, because they are able to outbid everybody else in the block.

In the initial report, they specify:

token1Amount: 0.1 WETH

token2Amount: 150 USDC

The oracle contract balances are now 0.001 ETH, 0.1 WETH, and 150 USDC.

These report balances imply an ETH price of $1500 when the real price is $3000.

After settlementTime of 10 seconds assuming nobody disputes this report, the report may be settled and become usable for the application, at a horrible price. But, it is profitable to come along and dispute this, so we assume a disputer comes along before 10 seconds is up.

In the dispute, they specify:

token1AmountNew: 0.15 WETH

token2AmountNew: 450 USDC

tokenToSwap: USDC

They decide to swap against the initial reporter’s 150 USDC, meaning they choose USDC as the token to swap in their dispute. The token1AmountNew is 50% larger than the initial report by contract rule using the 1.5x multiplier from the price request. The token flows are as follows:

The oracle contract takes 150 USDC from the disputer, then adds this to the initial reporter’s original 150 USDC and sends it all to the initial reporter, for a total of 300 USDC sent to the initial reporter.

Next, the oracle contract takes 450 USDC and 0.05 WETH from the disputer and adds it to the report.

The contract balances are now 0.001 ETH, 0.15 WETH and 450 USDC and the settlementTime timer resets to another 10 seconds.

Assume the manipulator relents and the settlementTime of 10 seconds passes, anyone can come along and settle the reported price. The oracle price is $3000 while the real price is $3000.

In the settlement, the settler only specifies which report they are settling. Typically they receive some settler reward in ETH paid for by the price requestor but we assume 0 for this example. The token flows in the settle are as follows:

Initial reporter (the manipulator) receives 0.001 ETH from the initial reporter reward. This must be netted against the gas cost of outbidding everyone else to be the first initial reporter.

Disputer receives 450 USDC and 0.15 WETH back.

The contract balances are now 0 across all ETH and tokens. If we net the flows across the entire oracle life cycle of price request, initial report, dispute and settlement, we see the following:

Initial reporter:

USDC: +150

WETH: -0.1

Disputer:

USDC: -150

WETH: +0.1

Assume the gas fees and initial reporter reward net to near zero. The true price of ETH is $3000, so the manipulator loses $150, the disputer makes $150, and the oracle price settles fairly for the application to use. If the manipulator decided to keep trying to manipulate the price by disputing the honest disputer’s report, they would lose an exponentially increasing amount of money that scales with the error in reported price.

The reference oracle implementation in solidity has more parameters to tweak, like swap fees, escalation halt, dispute delay, time mode (seconds vs blocks) and many more, but the simplified version is accurate with respect to how the incentives work.

The swap fees are an important parameter for a given oracle instance. A new reporter pays the previous reporter a swap fee in % which is set at time of price request. If the swap fees are too low relative to the background market volatility over the specified settlement time, the total time to settlement may drag on as disputes resetting the timer are more common. If the swap fees are too high, on the other hand, this exposes passive users of the oracle price to arbitrage loss because an active manipulator can try to get the price to settle somewhere inside of the swap fee bound but away from the true price.

So there is a fundamental tradeoff between total oracle instance finalization time and arbitrage loss to end users.

In terms of the maximum arbitrage loss a completely passive end user is exposed to, this number is strictly less than the total internal oracle swap fees per round plus gas fees plus jump loss to the reporter. We call this an effective swap fee F (swap_fees + gas_fees + jump_loss). We assume if the price were outside of F, it would be disputed by 1 of n self-interested participants. Since only the final surviving price contributes to price error in an external notional, the total extractable value is <= F. This applies to linear external notional only. Binary external notional is more complicated as there is no provable bound on arbitrage loss, but one can imagine an oracle instance parameterized to punish settlement delays especially hard if we need to settle binary bets.

Jump loss is a cost to reporters no matter which direction the price moves. Token prices can discontinuously gap past +/- F and the reporter eats the difference versus the standalone swap fee after someone disputes and corrects the price. Higher multipliers burden reporters with more jump loss per round relative to the natural price error of the previous report.

The escalation halt is another important parameter. Past this halt, disputes can continue but no longer need to post exponentially increasing amounts of collateral. This way you can ensure the oracle instance does not escalate past the perceived capacity of the dispute network while still imposing high penalties on manipulators.

The full solidity implementation can be found below. Note the direct function entries may be supplemented with external contract reorganization / replay guards (i.e. if tx not inside passed block number and timestamp revert, or settle must use matching price request stateHash) which may help but do not eliminate risk.



      [github.com/j0i0m0b0o/openOracleBase](https://github.com/j0i0m0b0o/openOracleBase/blob/7badc393798e9414f9f6dfba96b531a561f90a47/src/OpenOracle.sol)





####

  [7badc3937](https://github.com/j0i0m0b0o/openOracleBase/blob/7badc393798e9414f9f6dfba96b531a561f90a47/src/OpenOracle.sol)



```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/**
 * @title OpenOracle
 * @notice A trust-free price oracle that uses an escalating auction mechanism
 * @dev This contract enables price discovery through economic incentives where
 *      expiration serves as evidence of a good price with appropriate parameters
 * @author OpenOracle Team
 * @custom:version 0.1.6
 * @custom:documentation https://openprices.gitbook.io/openoracle-docs
 */
contract OpenOracle is ReentrancyGuard, Ownable {
    using SafeERC20 for IERC20;

```

  This file has been truncated. [show original](https://github.com/j0i0m0b0o/openOracleBase/blob/7badc393798e9414f9f6dfba96b531a561f90a47/src/OpenOracle.sol)










Would love to hear any feedback or criticism on the design, and am happy to answer any questions! We hope to contribute to the development of truly trust-free financial applications.

## Replies

**Killari** (2025-08-25):

Hey,

Looks really interesting, why does the disputer take the 150usdc? Do they also have a choice to take the 0.1 weth? If real price is 3000$, and they can choose either usdc or weth, they should choose weth as that’s worth 300$.

---

**j0i0m0b0o** (2025-08-26):

Thanks Killari - in the simplified oracle life cycle example, because the disputer chose USDC as the tokenToSwap, the initial reporter only receives 2 times the amount of USDC they had committed (their 150 USDC + 150 USDC from the disputer), leaving the WETH behind for the disputer to effectively claim. It is as if the disputer swapped 150 USDC for 0.1 WETH.


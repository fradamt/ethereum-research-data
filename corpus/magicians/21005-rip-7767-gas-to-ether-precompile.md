---
source: magicians
topic_id: 21005
title: "RIP-7767: Gas to Ether Precompile"
author: Vectorized
date: "2024-09-09"
category: RIPs
tags: [gas]
url: https://ethereum-magicians.org/t/rip-7767-gas-to-ether-precompile/21005
views: 666
likes: 12
posts_count: 5
---

# RIP-7767: Gas to Ether Precompile

## Description

A precompile that allows the caller to burn a specified amount of gas, and return a portion of the gas burned to the caller as Ether

## Motivation

Some EVM chains include a form of contract secured revenue (CSR), where a portion of the gas used by the contract is returned to the owner of the contract as Ether via some mechanism. CSR, in its straightforward form, creates a perverse incentive for developers to write bloated code, or run loops of wasteful compute / state writes in order to burn gas.

This proposal describes a way for CSR to be implemented in a computationally efficient and scalable way. Additionally, it provides a standardized interface that improves cross-chain compatibility of smart contract code.

This proposal is also designed to be flexible enough to be implemented either as a predeploy, or a precompile.

### Benefits

- Enable baked-in taxes for token transfers (e.g. creator royalties).
- Increase sequencer fees, so that L2s can feel more generous in accruing value back to L1.
- Promote development on L2s, which are perfectly suited for novel incentive mechanisms at the core level.
- Tax high frequency trading on L2s (e.g. probabilistic MEVs) and route value back to authentic users.

## Details

For nomenclature, we shall refer to this precompile as the Gasback precompile.

The behavior of the precompile can be described by the following Solidity smart contract.



      [gist.github.com](https://gist.github.com/Vectorized/5aed0b52c9298cf98e68801351bea637)





####










- Caller calls Gasback precompile with abi.encode(gasToBurn).
- Upon successful execution:

The precompile MUST consume at least gasToBurn amount of gas.
- The precompile MUST force send the caller Ether up to basefee * gasToBurn. The force sending MUST NOT revert. This is to accommodate contracts that cannot implement a fallback function.
- The precompile MUST return abi.encode(amountToGive), where amountToGive is the amount of Ether force sent to the caller.

Else, the precompile MUST return empty returndata.

## Suggested Implementation (op-geth level)

https://github.com/Vectorized/op-geth/pull/1

## Security Considerations

As long as the contract always returns less than or equal to the gas burned, the L2 chain implementing it can never become insolvent.

To make DDoS infeasible, the amount of Ether returned by a call can be adjusted to a ratio (e.g. 50-90%). Alternatively, each call to the contract can burn a flat amount of gas that will not be returned as Ether.

To manage the basefee, the precompile can be dynamically configured to switch to a no-op if the basefee gets too high.

## Replies

**wjmelements** (2024-09-12):

Shitcoins are going to use this to steal my gas. You list this under benefits but it’s a detriment. It won’t only be used to steal fixed amounts of gas. It will also steal arbitrary amounts, via the `GAS` opcode.

Stealing gas is strictly worse than an ether payment because it wastes block space.

Transfer taxes (and CSR) are already cancer. They shouldn’t be facilitated.

---

**wjmelements** (2024-09-12):

The inverse, ether to gas, could be useful for AA.

---

**Vectorized** (2024-09-12):

This is already possible on Blast and Mode today.

Do you have examples of it being abused by shitcoins?

Also, this precompile will burn gas without a O(n) loop.

“Block space” is simply a way to meter resources, to prevent DDoS. In this case, no computational or storage resources are wasted.

---

**Vectorized** (2024-09-12):

Block space on L2s are already in overabundance.

This RIP is deliberately not an EIP because L2s should be given the freedom to experiment with novel incentive mechanisms.

Also, CSR related EIPs (which are technically RIPs) have been proposed.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-6968)





###



Contract Secured Revenue on an EVM based L2










Don’t like this RIP? Don’t implement it on your L2. Simple as that.

Don’t like shitcoins? Don’t trade them. Simple as that.

If this RIP ever causes issues, it can always be removed in a future hardfork.


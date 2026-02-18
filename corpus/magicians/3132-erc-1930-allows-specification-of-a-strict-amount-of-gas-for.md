---
source: magicians
topic_id: 3132
title: ERC-1930 Allows specification of a strict amount of gas for calls
author: wighawag
date: "2019-04-13"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/erc-1930-allows-specification-of-a-strict-amount-of-gas-for-calls/3132
views: 1190
likes: 0
posts_count: 1
---

# ERC-1930 Allows specification of a strict amount of gas for calls

Hi,

I’d like to propose a core EIP to allow contract to ensure external call get a specific amount of gas and not just a maximum value (as present).

If we could get this included in the next fork that would be great for meta transaction and smart contract wallet.

I copy the content of the EIP here but created an issue for that on github, see : https://github.com/ethereum/EIPs/issues/1930

One thing I am not entirely sure about it is whether we need new opodes (as proposed in the current draft) or if it is safe to break the current behavior. In other words what will be the impact on existing contracts. Let me know what you think.

### Specification

- add a new variant of the CALL opcode where the gas specified is enforced so that if the gas left at the point of call is not enough to give the specified gas to the destination, the current call revert
- add a new variant of the DELEGATE_CALL opcode where the gas specified is enforced so that if the gas left at the point of call is not enough to give the specified gas to the destination, the current call revert

In other words, based on [EIP-150](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-150.md), the current call must revert unless G >= I x 64/63 where G is gas left at the point of call (after deducing the cost of the call itself) and I is the gas specified.

So instead of

```auto
availableGas = availableGas - base
gas := availableGas - availableGas/64
...
if !callCost.IsUint64() || gas = `txGas`, "not enough gas provided")
to.call.gas(txGas)(data); // CALL
```

where E is the gas required for the operation beteen the call to `gasleft()` and the actual call PLUS the gas cost of the call itself.

While it is possible to simply over estimate `E` to prevent call to be executed if not enough gas is provided to the current call it would be better to have the EVM do the precise work itself. As gas pricing continue to evolve, this is important to have a mechanism to ensure a specific amount of gas is passed to the call so such mechanism can be used without having to relies on a specific gas pricing.

1. check done after the call:

```auto
to.call.gas(txGas)(data); // CALL
require(gasleft() >= txGas / 63, "not enough gas left");
```

This solution does not require to compute a `E` value and thus do not relies on a specific gas pricing (except for the behaviour of EIP-150) since if the call is given not enough gas and fails for that reason, the condition above will always fail, ensuring the current call will revert.

But this check still pass if the gas given was less AND the external call reverted or succeeded EARLY (so that the gas left after the call >= txGas / 63).

This can be an issue if the code executed as part of the CALL is reverting as a result of a check against the gas provided. Like a meta transaction in a meta transaction.

Similarly to the the previous solution, an EVM mechanism would be much better.

## References

1. EIP-150, https://github.com/ethereum/EIPs/blob/master/EIPS/eip-150.md

---
source: magicians
topic_id: 6425
title: "[DISCUSSION] Optimized Setup Code"
author: lolwhenuseeme
date: "2021-06-07"
category: EIPs
tags: [evm, opcodes, gas, proxy-contract]
url: https://ethereum-magicians.org/t/discussion-optimized-setup-code/6425
views: 985
likes: 0
posts_count: 1
---

# [DISCUSSION] Optimized Setup Code

## Being a good citizen by asking for comments here instead of clogging up more mailboxes! Suggestions welcomed

## eip:
title: Optimized Setup Code
author:
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2021-06-06

## Simple Summary

Shrinking and generalizing setup code in creation code with industry standard as benchmark (EIP1167 clone factory by optionality).

## Abstract

By using a different combination of opcodes, we can reduce the overall cost of deploying contracts. This EIP looks at the setup code portion of creation code and makes it both generic and shorter than any other tool produces. The code is generic because it doesn’t change for different runtime code, the opcodes stay exactly the same.

## Motivation

Optimizing common EVM interactions to reduce overall cost function.

## Specification

```auto
0x00 38 CODESIZE
0x01 58 PC
0x02 58 PC
0x03 39 CODECOPY
0x04 38 CODESIZE
0x05 60 PUSH1
0x06 09 0x09
0x07 F3 RETURN
```

Although undeveloped, we can also change codecopy to returndatacopy or use other copy sequences without losing the heart of this EIP’s code.

When compared with EIP1167, the creation code above is 2 bytes shorter, down from 10. This is a decent improvement in deployment cost especially when the runtime code returned is not very large. Not fully certain, but I believe the code from 1167 is derived from what Solidity or Yul would give you if you were constructing a contract (ethers and web3 use this as well).

For comparison, here’s what 1167 uses as setup code:

```auto
0x00 3d RETURNDATASIZE
0x01 60 PUSH1
0x02 s1 runtime code size
0x03 80 DUP1
0x04 60 PUSH1
0x05 s2 setup code size
0x06 3d RETURNDATASIZE
0x07 39 CODECOPY
0x08 81 DUP2
0x09 f3 RETURN
```

The runtime code is then appended to this bit, just like how this EIP does it.

Not only is EIP1167’s code a little larger, it also needs to change when the runtime code is different meaning it requires more computation to handle edge cases. Not a factor if you’re crafting your code offchain.

## Rationale

CREATE and CREATE2 are both widely used, so it makes sense to ensure we’re saving on gas and that we have a common creation solution that works well with most contract systems. Solidity or other tools could use this code to give more efficient creation code to consumers.

## Backwards Compatibility

The code in this EIP works just as well as the standard constructor code runs for contracts with no constructor block in Solidity. It essentially just optimally returns the data following the setup sequence, which is how most creation code works. For this use case, there are no backwards incompatibilities. All code which was deployed using previous setup code sequences could be deployed using this one as a drop-in replacement.

## Test Cases

See reference implementation below.

## Reference Implementation

```auto
Init code (this EIP):
38585839386009f3

Runtime code (returns 1 word of calldata):
3d353d52363df3

Tx.data (both concatenated):
38585839386009f33d353d52363df3

# Then get deployed contract's code and check that it's == Runtime code
# This works well in remix on standard hardware (plop into scripts/)
# If your evm sucks calculate the address of the deployed contract using the create1 formula and get its code
```

## Security Considerations

Some modifications need to be brought to the suggested setup code if the EVM receives an update to some of its intrinsics, like the way it zero-pads. Luckily, this EIP only affects setup code so only create2 address calculation would be affected (setup code just disappears once contract deployed, but it’s used by create2 for address calculation).

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

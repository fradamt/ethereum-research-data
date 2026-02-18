---
source: magicians
topic_id: 18482
title: "ERC-7613: Puppet proxy contract"
author: CodeSandwich
date: "2024-02-04"
category: ERCs
tags: [erc, proxy-contract]
url: https://ethereum-magicians.org/t/erc-7613-puppet-proxy-contract/18482
views: 943
likes: 1
posts_count: 5
---

# ERC-7613: Puppet proxy contract

This is the discussion thread for PR [Add EIP: Puppet proxy contract #236](https://github.com/ethereum/ERCs/pull/236). Below is the shortened version of the EIP.

## Abstract

A puppet is a contract that when called, acts like an empty account, it doesn’t do anything and it has no API. The only exception is that if it’s called by the address that deployed it, it delegates the call to the address passed to it in calldata. This gives the deployer the ability to execute any logic they want in the context of the puppet.

## Motivation

A puppet can be used as an alternative account of its deployer. It has a different address, so it has a separate set of asset balances. This enables sophisticated accounting, e.g. each user of a protocol can get their own address where assets can be sent and stored.

The puppet’s logic doesn’t need to be ever upgraded, to change its behavior the deployer needs to change the address it passes to the puppet to delegate to or the calldata it passes for delegation. The entire fleet of puppets deployed by a single contract can be upgraded by upgrading the contract that deployed them, without using beacons. A nice trick is that the deployer can make the puppet delegate to the address holding the deployer’s own logic, so the puppet’s logic is encapsulated in the deployer’s.

A puppet is unable to expose any API to any caller except the deployer. If a 3rd party needs to be able to somehow make the puppet execute some logic, it can’t be requested by directly calling the puppet. Instead, the deployer needs to expose a function that if called by the 3rd parties, will call the puppet, and make it execute the desired logic. Mechanisms expecting contracts to expose some APIs don’t work with puppet, e.g. ERC-721’s `safeTransfer`s.

Because the puppet can be deployed under a predictable address despite having no fixed logic, in some cases it can be used as a CREATE3 alternative. It can be also used as a full replacement of the CREATE3 factory by using a puppet deployed using CREATE2 to deploy arbitrary code using plain CREATE.

Deploying a new puppet is almost as cheap as deploying a new clone proxy. Its whole deployed bytecode is 66 bytes, and its creation code is 62 bytes. Just like clone proxy, it can be deployed using just the Solidity scratch space in memory. The cost to deploy a puppet is 45K gas, only 4K more than a clone. Because the bytecode is not compiled, it can be reliably deployed under a predictable CREATE2 address regardless of the compiler version.

## Specification

To delegate, the deployer must prepend the calldata with an ABI-encoded address to delegate to.

All the data after the address will be passed verbatim as the delegation calldata.

If the caller isn’t the deployer, the calldata is shorter than 32 bytes, or it doesn’t start with

an address left-padded with zeros, the puppet doesn’t do anything.

This lets the deployer make a plain native tokens transfer to the puppet,

it will have an empty calldata, and the puppet will accept the transfer without delegating.

The puppet is deployed bytecode and its breakdown is in the EIP PR.

## Rationale

The main goals of the puppet design are low cost and modularity. It should be cheap to deploy and cheap to interact with. The contract should be self-contained, simple to reason about, and easy to use as an architectural building block.

The puppet behavior could be implemented fairly easily in Solidity with some inline Yul for delegation. This would make the bytecode much larger and more expensive to deploy. It would also be different depending on the compiler version and configuration, so deployments under predictable addresses using CREATE2 would be trickier.

A workaround for the problems with the above solution could be to use the clone proxy pattern to deploy copies of the puppet implementation. It would make the cost to deploy each puppet a little lower than deploying the bytecode proposed in this document, and the addresses of the clones would be predictable when deploying using CREATE2. The downside is that now there would be 1 extra delegation for each call, from the clone proxy to the puppet implementation address, which costs gas. The architecture of such solution is also more complicated with more contracts involved, and it requires the initialization step of deploying the puppet implementation before any clone can be deployed. The initialization step limits the CREATE2 address predictability because the creation code of the clone proxy includes the implementation address, which affects the deployment address.

Another alternative is to use the beacon proxy pattern. Making a Solidity API call safely is a relatively complex procedure that takes up a non-trivial space in the bytecode. To lower the cost of the puppets, the beacon proxy probably should be used with the clone proxy, which would be even more complicated and more expensive to use than the above solutions. Querying a beacon for the delegation address is less flexible than passing it in calldata, it requires updating the state of the beacon to change the address.

## Backwards Compatibility

No backward compatibility issues found.

The puppet bytecode doesn’t use PUSH0, because many chains don’t support it yet.

## Test Cases

The test cases are in the EIP PR.

## Reference Implementation

The puppet bytecode is explained in the specification section. The example helper library is in the EIP PR.

## Security Considerations

The bytecode is made to resemble clone proxy’s wherever it makes sense to simplify auditing.

ABI-encoding the delegation address protects the deployer from being tricked by a 3rd party into calling the puppet and making it delegate to an arbitrary address. Such scenario would only be possible if the deployer called on the puppet a function with the selector `0x00000000`, which as of now doesn’t come from any reasonably named function.

Needs discussion.

## Replies

**SamWilsn** (2024-05-22):

This is an interesting idea, but runs into problems with tokens like [ERC-1155](https://eips.ethereum.org/EIPS/eip-1155) because of `onERC1155Received`. If the puppet has no implementation, token transfers to it will revert.

A slightly better approach might be to use `CREATE2` to deploy to a known address, and `SELFDESTRUCT` inside the initcode. That way the puppet has no code during normal execution, and is (mostly) indistinguishable from an EOA.

---

**CodeSandwich** (2024-05-26):

Thank you for the feedback here and in the PR, I’ll answer it soon.

Yes, it seems that ERC-1155 is an unsolvable problem with the proxy pattern I proposed, a deployed puppet proxy simply can’t be a direct recipient of such tokens.

`SELFDESTRUCT` trick is clever, but it requires the initcode itself to always be exactly the same or the `CREATE2` address becomes different. This is an obstacle for passing the delegation address and the arguments because they can’t be simply appended to calldata. All the data needs to be somehow queried from the caller, which complicates the logic and probably leads to using a lot of storage. It either requires writing and reviewing much more raw bytecode by hand or using a fixed compiler version that will always generate exactly the same bytecode. The future of `SELFDESTRUCT` isn’t that certain either, IIRC as of now it’s actually clearing the account only inside the initcode, and it’s an exception that may or may not be lifted later. Another downside is that `CREATE2` is rather expensive even if it doesn’t deploy anything, and low cost is one of the main features of this proxy pattern.

---

**SamWilsn** (2024-05-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/codesandwich/48/11602_2.png) CodeSandwich:

> SELFDESTRUCT trick is clever, but it requires the initcode itself to always be exactly the same or the CREATE2 address becomes different.

If you make the initcode something like `delegatecall(gas(), caller(), 0, 0, 0, 0)` you can change the behaviour dynamically, and if you use [TSTORE](https://eips.ethereum.org/EIPS/eip-1153) to store the “real” delegate call target, it’s much cheaper than `SSTORE`.

---

**CodeSandwich** (2024-05-26):

`delegatecall(..., caller(), ...)` will get the puppet proxy’s transient storage context, which will be empty, it won’t be holding the data stored by the caller. It would need to do the full `call(..., caller(), ...)`, parse the returned data and execute it. ~~Parsing may be done in Solidity by doing some back and forth where the proxy would do `call(..., caller(), ...)` and then `delegatecall(..., caller(), ..., [data returned from call], ...)`, but it may not be worth the complexity on the caller side.  Anyway, the caller would need to serve the TSTOREd data inside its `fallback()` function to whoever called it if there’s anything stored. It’s not a huge problem, but it’s worth noting.~~ (It’s only possible to `delegatecall(..., caller(), ...)` if the caller isn’t upgradeable, otherwise the call will be effectively delegated to address zero, which is stored in the proxy implementation storage slot in the puppet proxy’s context)


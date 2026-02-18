---
source: magicians
topic_id: 18625
title: "EIP-7620: EOF - Contract Creation Instructions"
author: pdobacz
date: "2024-02-13"
category: EIPs > EIPs core
tags: [evm, opcodes, evm-object-format, create]
url: https://ethereum-magicians.org/t/eip-7620-eof-contract-creation-instructions/18625
views: 1767
likes: 1
posts_count: 14
---

# EIP-7620: EOF - Contract Creation Instructions

Discussion topic for [EIP-7620: EOF - Contract Creation Instructions](https://eips.ethereum.org/EIPS/eip-7620).

EIP-7620 adds ~~`CREATE3/4`~~ `EOFCREATE` and `TXCREATE` opcodes and EOF contract creation specs, as previously specced out in the [“Mega EOF Endgame” spec (aka “Megaspec”)](https://github.com/ipsilon/eof/blob/main/spec/eof.md).

## Replies

**radek** (2024-02-17):

Hi, have you considered that “CREATE3 opcode” will collide in naming with CREATE+CREATE2 combos named as CREATE3?

This will confuse new devs reading older hints / tutorials / SO.

Since these opcodes are for EOF contracts, while  CREATE and CREATE2 are not to be used, it might make sense to discontinue sequence in naming, as well.

---

**pdobacz** (2024-02-21):

CREATE3/4 is just temporary naming which kind of sunk in. Renaming is still an option, good point about the other CREATE3 here.

---

**cairo** (2024-08-23):

[@pdobacz](/u/pdobacz) is there a rationale behind having the order of the stack inputs for `EOFCREATE` be `value`, `salt`, `input_offset`, `input_size`, instead of `value`, `input_offset`, `input_size`, `salt` (like in CREATE2)?

---

**pdobacz** (2024-08-26):

I don’t know, I’ll ask around if there was any specific rationale.

EOFCREATE input isn’t exactly the same as CREATE2 input (calldata vs initcode), though I don’t think this was the reason.

---

**duncancmt** (2024-11-28):

This EIP seems like it would cut off use cases where a factory contract `CREATE`’s a contract from calldata. As an example, here’s some Yul code that would have no equivalent after 7620:

```auto
let ptr := mload(0x40)
calldatacopy(ptr, initcode.offset, initcode.length)
new_contract := create2(callvalue(), ptr, initcode.length, salt)
```

That seems like a pretty important use case, and if not supported it would preclude my adoption of EOF. Combined with the prohibition of legacy contracts creating EOF contracts, this would also mean that deterministic, permissionless deployment of trusted contracts to the same address across all chains (using something like Nick’s method or the Arachnid deterministic deployment proxy) no longer works. I expect that for many protocols this would be a blocker to adopting EOF.

---

**axic** (2024-11-28):

It is by design – there is a specific requirement that contract code cannot be inspected within the EVM, and your use case basically allows that.

This is solved by [TXCREATE](https://github.com/ipsilon/eof/blob/main/spec/eof_future_upgrades.md#txcreate-and-initcodetransaction).

---

**duncancmt** (2024-11-29):

Ahh, `TXCREATE` solves that problem pretty neatly. I hope it goes in at the same time as the rest of EOF to enable that use case. To explain in more detail my specific use case, I have 2 considerations:

1. How do we permissionlessly, trustlessly deploy the same contract to the same address on all chains? CREATE2 and EOFCREATE obviously enable trustlessness by deriving the contract address from the hash of the initcode. However, permissionlessness is more difficult. Using TXCREATE in combination with Nick’s method for deployment gives us permissionlessness. We can imagine an EOF replacement for the Arachnid deterministic deployment proxy that uses TXCREATE instead of CALLDATACOPY ... CREATE2 to obtain the same effect.

In my specific use case, I rely on the Safe{Wallet}'s stack, which in turn depends on a `CREATE2` factory toehold contract. This toehold contract can be ***either*** the Arachnid deterministic deployment proxy (permissionless, somewhat more fragile) or the Safe singleton factory (not permissionless, but more robust). I’ve been bitten by the lack of permissionlessness in the Safe singleton factory, which is why I care about using Nick’s method in combination with `TXCREATE`. Of course, on chains with extreme gas rules (e.g. Mantle), this isn’t foolproof, but we’re not letting perfect be the enemy of good.

1. How do we factory-deploy user-supplied initcode to an address NOT derived from the hash of that initcode? Basically, how can we “CREATE3” from calldata? This is halfway satisfied by TXCREATE, but we would still need a non-salted contract creation opcode to make it work without doing something really crazy. TXCREATE solves the problem of being able to factory-deploy from initcode not known to the factory at deploy-time, but the problem of non-salted deployment (i.e. CREATE; deployee addresses derived from the deployer address and its nonce) remains unsolved.

This pertains to the [Deployer](https://github.com/0xProject/0x-settler/blob/master/src/deployer/Deployer.sol) contract for 0x’s DEX aggregation router. This router contract is iterated rapidly to accommodate the shifting liquidity landscape; each iteration requires redeployment. This `Deployer` factory contract uses a “CREATE3” pattern to deploy the router to an address derived only from a feature identifier (there’s more than 1 router, each with a different feature set) and a nonce specific to that feature identifier. This lets 0x’s integrators precompute future router contract addresses for their own on-chain properties. Obviously, even though the router is trust-minimized, deployment is permissioned. I can sort of vaguely imagine a solution involving the abuse of `ecrecover` to compute addresses based on a feature++nonce and a secp256k1 pubkey and then deriving the deployed contract from that. That would also sacrifice a degree of trustlessness, unless you want to throw some MPC into the mix, which is not very satisfactory.

---

**shemnon** (2024-11-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/duncancmt/48/15676_2.png) duncancmt:

> How do we factory-deploy user-supplied initcode to an address NOT derived from the hash of that initcode?

If the address derivation did not include the hash of the initcode, would this negatively impact counterfactual patterns?  My understanding is that create3 uses patterns used by polymorphic addresses, which circumvents the initcode hash of the CREATE2 contract.

Is the certainty of the address more important than a sure knowledge of the code in that address?

---

**duncancmt** (2024-11-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> would this negatively impact counterfactual patterns?

The way “CREATE3” patterns work, you very much have to opt-in to avoiding initcode dependence in address calculations. Polymorphism is dead now that `SELFDESTRUCT` only works in the same transaction. It’s not practical to stumble your way into an address that doesn’t depend on the initcode deploying it when what you wanted was a counterfactual address. Plus EOA-deployed contracts are still derived from the nonce of the deployer, so there’s not really any getting around that.

---

**shemnon** (2024-11-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/duncancmt/48/15676_2.png) duncancmt:

> Plus EOA-deployed contracts are still derived from the nonce of the deployer, so there’s not really any getting around that.

That’s the point of the “toehold contract” - either via Nick’s method or a specific account?

If the initcode hash was removed from EOFCREATE or TXCREATE (relying on the sender address and a specified salt only) would that suit your needs?

Do you have any requirements that need the initcode hash in the address derivation?

---

**shemnon** (2024-12-01):

Also, would [EIP-7819: Create delegate](https://eips.ethereum.org/EIPS/eip-7819) be a possible solution? It’s EIP-7702, but for contract accounts.

1. TXCREATE deploys to hashcode derived address, the one you don’t like
2. The deterministic address (the one you like) is created and set with a delegate to the hashcode derived address.

---

**pdobacz** (2025-04-07):

Note: The spec of EIP-7620 is getting an update: [Update EIP-7620: Simplify EOFCREATE new address hashing scheme by gumb0 · Pull Request #9298 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9298)

---

**pdobacz** (2025-04-07):

Also Note: The spec of EIP-7620 is getting another update (this time minor - only order of stack args change): [Update EIP-7620: Align EOFCREATE stack args with EXTCALL by pdobacz · Pull Request #9503 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9503)


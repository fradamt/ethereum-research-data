---
source: magicians
topic_id: 22234
title: "EIP-7843: SLOTNUM opcode"
author: marchhill
date: "2024-12-16"
category: EIPs > EIPs core
tags: [precompile]
url: https://ethereum-magicians.org/t/eip-7843-slotnum-opcode/22234
views: 297
likes: 4
posts_count: 6
---

# EIP-7843: SLOTNUM opcode

Discussion thread for [Add EIP: SLOT precompile by Marchhill · Pull Request #9141 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9141)

> This EIP proposes to add a new opcode that returns the corresponding slot for the current block.
>
>
> It is currently possible to calculate the slot number from the block timestamp. However, this requires hardcoding the chain slot length into a smart contract. This would require the contract code to be changed in the event of a future change to slot length. A better approach is for the slot number to be calculated by the execution layer and exposed by an opcode. This paves the way for future changes to the slot length.

## Replies

**suchapalaver** (2024-12-26):

Sharing a use case for this in support of the discussion: Verifying execution layer data with reference to the Beacon Chain requires calculating the Beacon Chain slot containing the execution layer block in its Execution Payload. The Beacon Chain provides the cryptographic primitives required to prove the inclusion of execution layer data in the canonical history of the chain but the first hurdle is matching an execution layer block to its Beacon Chain counterpart.

---

**ralexstokes** (2025-02-19):

another option here would be to just compute the slot off-chain, pass it in to the smart contract in the calldata, and authenticate with EIP-4788

no new protocol functionality needed

---

**marchhill** (2025-02-20):

Yes this is possible but much more expensive than using the precompile which costs 2 gas. I think it is more likely that people would end up using the hacky way (calculating from timestamp) rather than this more expensive way; ideally we want to make the right way cheap.

Another advantage of this EIP is that it exposes the slot number to the EL. In Nethermind we currently need the slot number for building Shutter blocks, it’s likely other clients will too in future. Rather than calculating from the timestamp in the EL, I think that the CL should serve as the source of truth for the slot number.

Overall this EIP is not making something new possible, but making something that is already possible cleaner and cheaper. It could also save us time down the line if we want to change the slot length.

---

**marchhill** (2025-05-15):

Hey [@suchapalaver](/u/suchapalaver) would you be able to expand a bit on this application of verifying execution layer data against the beacon block root? Do you just need the current slot number from the opcode or is having the slot number in the header important?

atm the main application I can see is doing anything that relies on beacon chain time, for example allowing rewards to be unlocked every x slots or epochs.

---

**bbjubjub** (2025-05-31):

I see that this is now an opcode and relies on the consensus layer to provide the slot number, which is a perfectly sound design. Regardless, if were ever to go back to a self-contained precompile I would like to suggest the following in the spirit of [EIP-7666](https://eips.ethereum.org/EIPS/eip-7666):

> At the start of the block in which this fork activates, set the code of SLOTNUM_PRECOMPILE_ADDRESS to the bytes corresponding to the following program:
>
>
>
> ```auto
> PUSH1 12
> TIMESTAMP
> PUSH4 beacon_chain_genesis_time
> SUB
> DIV
> PUSH0
> MSTORE
> PUSH1 0x20
> PUSH0
> RETURN
> ```

This has the nice property of minimizing the risk of chain-splitting bugs, and also comes with implicit gas costs. Whenever we change the slot schedule, we can simply force-update the program code. (Note that I didn’t test the program so it might be incorrect, but the point is the same regardless)


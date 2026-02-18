---
source: magicians
topic_id: 16933
title: Extending address from 20 bytes to 32 won't work because of FunctionType requiring 4 bytes extra
author: dogeprotocol
date: "2023-12-02"
category: Uncategorized
tags: [address-space, address-collision]
url: https://ethereum-magicians.org/t/extending-address-from-20-bytes-to-32-wont-work-because-of-functiontype-requiring-4-bytes-extra/16933
views: 774
likes: 1
posts_count: 3
---

# Extending address from 20 bytes to 32 won't work because of FunctionType requiring 4 bytes extra

There have been a few proposals to increase address size to 32 bytes:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png)

      [Increasing address size from 20 to 32 bytes](https://ethereum-magicians.org/t/increasing-address-size-from-20-to-32-bytes/5485) [Ethereum 1.x Ring](/c/working-groups/ethereum-1-x-ring/33)




> Why increase the address size?
> At some point, perhaps soon, we are going to have to increase the address size from 20 bytes to 32 bytes. Some reasons for this include:
>
> Adding an address space ID if we use a state expiry scheme that requires it
>
> Adding a shard ID if we have multiple EVM-capable execution shards
> Security: 20 bytes is not secure enough
>
> To elaborate on (3), current 20 byte (160 bit) addresses only provide 80 bits of collision resistance, meaning that someone can spend 2**80 comp…



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/norswap/48/4243_2.png)

      [Thoughts on Address Space Extension (ASE)](https://ethereum-magicians.org/t/thoughts-on-address-space-extension-ase/6779) [Ethereum 1.x Ring](/c/working-groups/ethereum-1-x-ring/33)




> Context
>
> Increasing address size from 20 to 32
> bytes
> ASE (Address Space Extension) with Translation
> Map
> ASE Test
> Cases
> Issues with ASE (with a translation
> map)
> Types of Resurrection Metadata in State
> Expiry
> Address Space Extension with bridge
> contracts
> Making ASE work with an Edict
>
> I’ve thought a bit on address space extension and I wanted to clarify a few
> things, propose some ideas and get some feedback.
> In what follows, unless said otherwise, I’ll assume the period-aware address ASE
> …

However they seem to miss fact that the FunctionType requires 4 bytes extra. The current storage requirement of FunctionType is 20+4 (24) bytes. So, the maximum the address can store with current 32 byte stack limitation is 28 bytes (224 bits).

Is there a simple way to address this?

// A function type is simply the address with the function selection signature at the end.

//

// readFunctionType enforces that standard by always presenting it as a 24-array (address + sig = 24 bytes)

func readFunctionType(t Type, word byte) (funcTy [24]byte, err error) {

## Replies

**norswap** (2023-12-03):

Depending on the scheme, it might not be much of an issue. The notion of a FunctionType is from Solidity, not at the EVM layer. The Solidity language can add new types to represent pointers to extended addresses, that will be stored on two storage slots instead of one.

There will be a need to distinguish the types of legacy function pointers and extended address function pointers. In most schemes, this is desirable anyway, as you don’t want to accidentally call an extended contract with a legacy address or vice-versa, and there might be a need for the Solidity (or any other EVM language) to insert address conversion logic.

---

**dogeprotocol** (2023-12-03):

It does need change in the node client  (like go-dp) though, in the ABI layer, where pack/unpack and topics currently hard-code FunctionTypes to 24 bytes.


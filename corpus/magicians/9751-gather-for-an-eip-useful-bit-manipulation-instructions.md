---
source: magicians
topic_id: 9751
title: "Gather for an EIP: Useful Bit manipulation instructions"
author: dominic
date: "2022-06-27"
category: EIPs
tags: [evm]
url: https://ethereum-magicians.org/t/gather-for-an-eip-useful-bit-manipulation-instructions/9751
views: 1703
likes: 10
posts_count: 9
---

# Gather for an EIP: Useful Bit manipulation instructions

Hi there,

While optimizing some data structures I’ve realized that the EVM is missing some in-memory bit operations that make it much more gas expensive to do certain calculations compared to x86. I think it would make sense to add them and would love to hear if you’ve come across similar mathematical instructions.

- POPCNT - Population Count (Counting all set bits in a uint256)
- CLZ - Count Leading Zeros (Getting the highest bit in a uint256)

These two operations need to be simulated in a loop at the moment and become thus pretty expensive. E.g. here is a 700 gas version of getting the highest bit [Logarithm math operation in Solidity - Ethereum Stack Exchange](https://ethereum.stackexchange.com/questions/8086/logarithm-math-operation-in-solidity)

I might turn this into an EIP, so let me know if there are more instructions to add.

## Replies

**chfast** (2022-06-28):

Hi [@dominic](/u/dominic),

Such instructions are easy to add, but it can take up to 2 years if we start now. The most important part is justification why such instructions are useful. E.g. you would need to show a group of popular contracts what would benefit from new instructions.

---

**chfast** (2022-08-24):

A few words about implementation:

`POPCNT` is data-parallel at first (perform *popcount* on 4 words) and finally sum the results. So in theory latency should be better than in `ADD`. But this is only in case the CPU has native `popcount` instruction what is not the case for the baseline `x86-64`.

`CLZ` seems to have the complexity of `SHL`, i.e. it is messy. There is a lot of handling of individual words being zero. I have not seen constant-time implementation yet. Having `lzcnt` instruction available should help a bit.

Native instructions availability for x86-64: [Compiler Explorer](https://godbolt.org/z/Kdf5Kdrhj).

I think you still should proceed with the EIP and try to move it to the “Review” state.

---

**Vectorized** (2022-09-11):

[@dominic](/u/dominic) Thanks for making this proposal!

Accidentally made a new thread [Create a new opcode for counting leading zeros (CLZ)](https://ethereum-magicians.org/t/create-a-new-opcode-for-counting-leading-zeros-clz/10805) without finding this first. Thanks [@chfast](/u/chfast)

I think `CLZ` and `POPCNT` are best to be in separate EIPs, such that the usefulness of each opcode can be separately evaluated, giving a higher chance that one may pass.

Would you be available to work on an EIP or have been working on one already?

Otherwise, I can take on the effort and include you as an author too.

Imo, `CLZ` is too useful not to have it as a native opcode. Even 2 years will be worth the wait.

---

**dominic** (2022-09-11):

[@Vectorized](/u/vectorized) I like that approach let’s push together. CLZ is definitely more important - felt that if going through the process is by itself taking so much time that taking a group of bit manipulation instructions would be more efficient. But definitely better to have CLZ over not having anything.

If you’re around ETHStation or Bogota we can catch up in person, tag team for the EIP draft and the implementation PRs

---

**axic** (2022-09-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> CLZ seems to have the complexity of SHL, i.e. it is messy. There is a lot of handling of individual words being zero. I have not seen constant-time implementation yet. Having lzcnt instruction available should help a bit.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vectorized/48/7129_2.png)[Create a new opcode for counting leading zeros (CLZ)](https://ethereum-magicians.org/t/create-a-new-opcode-for-counting-leading-zeros-clz/10805/1)

> For the implementation of CLZ, I’d propose a gas cost of 3
> (to keep in line with the gas cost of shl, shr, not, xor, etc).

Just keep in mind, that while from an EVM code perspective they seem simple, due to the EVM operates on 256-bit **big endian** words and most CPUs operate on 64-bit **little endian** words, this becomes slightly more complex to implement, and the cost should reflect that. One could argue that `not`/`xor` is overpriced compared to `shl`/`shr`.

---

**chfast** (2022-10-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> Just keep in mind, that while from an EVM code perspective they seem simple, due to the EVM operates on 256-bit big endian words

This is not accurate. EVM implementations usually keep the value on the EVM stack in native form (i.e. little endian).

---

**dominic** (2022-10-08):

[@chfast](/u/chfast) [@axic](/u/axic) [@Vectorized](/u/vectorized) and anyone else, if you’re around this week for devcon (I am) I would definitely like to cut out an hour or two to get the EIP draft in place.

---

**axic** (2022-11-11):

Sorry I missed this message, but would be happy to collaborate.

[@Vectorized](/u/vectorized) left some comments on the `clz` topic.


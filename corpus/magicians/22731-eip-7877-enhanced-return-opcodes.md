---
source: magicians
topic_id: 22731
title: "EIP 7877: Enhanced RETURN opcodes"
author: 0xTraub
date: "2025-01-30"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/eip-7877-enhanced-return-opcodes/22731
views: 204
likes: 9
posts_count: 11
---

# EIP 7877: Enhanced RETURN opcodes

So I was reading through [this new Create3 Factory](https://github.com/AmadiMichael/Create3s/tree/main) someone built using transient storage and noticed that there’s a bunch of additional gas overhead when using transient storage to store bytecode. Specifically because you need to write the bytecode from transient storage to memory before returning. I’m wondering why the `RETURN` opcode only allows for returning data from memory instead of transient or storage. It would probably save a decent amount of gas from both having fewer opcodes and memory expansion costs. I’m thinking about some kind of an EIP to replace `RETURN` with 3 more specific opcodes all with the same parameters:

1. MRETURN
2. SRETURN
3. TRETURN

They would all operate basically the same and with the same stack arguments but return data from that section of data storage accordingly. `MRETURN` and `TRETURN` would probably use the same gas formula as `RETURN` does currently. `SRETURN` would most likely use a more complicated equation similar to `SLOAD` now, based on warm/cold slots.

The best way to support backwards compatibility would probably be to just rename `RETURN -> MRETURN` and leave it as `0xF3` and then add `SRETURN` and `TRETURN` as new opcodes (Maybe `0xF6` and `0xF7`). There is precedent for opcode-renaming,  [with changing SUICIDE to SELFDESTRUCT](https://eips.ethereum.org/EIPS/eip-6)

I’m not well versed enough in things like static analysis or compilers so I would like to hear thoughts on how this would affect their design and operation, but it would definitely make it easier to optimize bytecode especially when done with assembly/yul/huff.

What do people think?

## Replies

**Arvolear** (2025-01-31):

+1 on this one, sounds like a really nice optimization. Although `MRETURN` would probably be a bit different semantically from `SRETURN` and `TRETURN` as storage is divided into 32-byte chunks.

Would it be beneficial to also have a `RRETURN` opcode that returns `returndata`? I mean, currently if a contract `A` calls `B` and returns `B's` return, there is an unnecessary `returndata` copy introduced.

---

**0xTraub** (2025-01-31):

Very good points. Perhaps the best way is to do the following

1. MRETURN/RRETURN → Accepts a starting index and a length to return exactly as it is now
2. S/TRETURN → Accepts a starting slot number and a number of slots to return 32-byte increments, inclusive of the starting index, so SRETURN(0x0, 0x40) returns the data in slots [0, 1]

`RETURN` is currently `0xF3` so to maintain backwards compatibility I would suggest keeping it the same but renaming and setting the following.

`SRETURN -> 0xF6`

`TRETURN -> 0xF7`

`RRETURN -> 0xF8`

I’m curious what you think about gas pricing for S/TRETURN for cold and warm slots. The easiest implementation would be to have the cost be based on the number of slots, and if those slots are already warm/cold, I.E the cost of the opcode is the sum of each of those slots being accessed by independent `SLOAD` under current rules. However, it might make more sense to have it be a single cost, where if a single slot is cold, the entire read operation is treated as cold and priced higher accordingly.

---

**Arvolear** (2025-02-01):

If we are going the “optimization” way, I think the overall gas has to be lower than currently. Otherwise the optimization is not justified.

- For SRETURN, the number_of_cold_slots * 2100 + the number_of_warm_slots * 100 gas.
- For TRETURN, the number_of_slots * 100 gas.
- For RRETURN, I would use the current formula for RETURNDATACOPY but without “memory expansion” gas. So it would be:

```auto
minimum_word_size = (size + 31) / 32

static_gas = 3
dynamic_gas = 3 * minimum_word_size

overall = static_gas + dynamic_gas
```

BTW, do you think these opcodes are compatible with the EOF?

---

**0xTraub** (2025-02-02):

The optimization comes from not having the loop to write to memory first which means that you should be able to keep the cost the same and still come out ahead at the end simply due to fewer read/write operations, no? The `RRETURN` cost definitely makes sense, although I wonder if you should get some kind of a discount on `S/TRETURN` because even through you’re accessing more slots, you are accessing them sequentially, incentivizing reducing state accesses through independent SLOADs.

As for EOF I don’t see why it would break anything. As I understand it EOF is supposed to make future EVM versions easier to integrate due to better versioning.

---

**Arvolear** (2025-02-02):

Yeah, so we can keep the pricing the same and benefit from the absence of memory expansion. To be honest, I am not super familiar with current EC implementations and if they have sequential storage reads.

EOF “deprecates” and introduces a lot of opcodes. Also, it makes the bytecode (easier) to statically analyze as all the “JUMPs” with “JUMPDESTs” won’t be used. But probably storage and returndata loads have nothing to do with this.

---

**0xTraub** (2025-02-02):

I’d love to hear from a static analysis dev since I also have very limited knowledge in that area but I would think that a more explicit opcode would make it easier instead of having to analyze a more complex read/write memory pattern. I don’t think EOF deprecates anything here that would be important. I’d have to dig into the actual EC implementations but it shouldn’t be that much additional overhead from retrieving sequential memory.

If the stateDB is external, than reducing the number of calls through batching or sequential reads should be less computationally expensive as I understand it, but I’d like to hear from a EC client dev as well. If this is true then we can discuss what the discount ought to be otherwise leaving it as the equation now seems reasonable to me.

---

**0xTraub** (2025-02-03):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9315)














####


      `ethereum:master` ← `jhweintraub:master`




          opened 10:49PM - 03 Feb 25 UTC



          [![jhweintraub](https://avatars.githubusercontent.com/u/26035072?v=4)
            jhweintraub](https://github.com/jhweintraub)



          [+85
            -0](https://github.com/ethereum/EIPs/pull/9315/files)







EIP to replace `RETURN` with 4 more specific `RETURN` opcodes which allow defini[…](https://github.com/ethereum/EIPs/pull/9315)ng where to return from explicitly instead of first requiring copying to memory.

---

**pdobacz** (2025-02-24):

I’ve got a question to what the second argument to S/TRETURN actually means. In the paragraph I’m parsing this as 3 different contradictive behaviors:

> (…) It pops two items off the stack, (…) (second being) a number of sequential slots to return from. Ex: SRETURN(0x0, 0x40) returns the 64 bytes of data in slots [0, 1], (…) so SRETURN(0x00, 0x00) returns the value at storage slot 0.

I’m not fully on top of the application patterns of this, but from consistency standpoint maybe this could make sense instead: the second argument represents the number of bytes to return, read from consecutive slots, starting as indicated by the first argument. So `SRETURN(x, 0x00)` returns nothing, `SRETURN(x, 0x01)` returns the first byte of the xth slot, `SRETURN(x, 0x20)` returns the entire xth slot `SRETURN(x, 0x40)` returns the entire xth and x+1th slots. `SRETURN(x, 0x30)` returns xth slot and first 16 bytes of x+1th slot.

Another option would in turn be to make `T/SRETURN` aligned with `T/SLOAD`, taking in only one argument and returning always the entire 32 bytes of one slot.

---

**0xTraub** (2025-02-24):

I don’t think it makes sense to make the S/TRETURN only apply to one slot as structs which may need to be retrieved multiple times can take up multiple slots. For example

```auto
struct randStruct {
uint256 a;
uint256 b;
}
```

Allowing for multiple slots would allow for a single opcode to return the entirety of this struct from storage by using `SRETURN(0, 2)`. Similarly, requiring that the opcodes return 32-bytes from storage/transience would involve the least amount of compiler changes, as it would fit with the pattern of existing SLOAD. If the user wants more granular return data parsing they can always accomplish it with `RETURNDATACOPY` afterwards anyways.

---

**0xTraub** (2025-02-28):

Update: I’ve started working on updating the execution spec docs for this EIP. Please take a look and leave feedback or help. This is my first experience with these specs so any guidance would be greatly appreciated.

What I could use some assistance on is writing tests. I figure the best way to test this would be to create some contracts pre-populated with storage/transient values and then bytecode which just returns those values using the appropriate opcodes and compare the two. But that may be overengineering idk



      [github.com](https://github.com/jhweintraub/execution-specs)




  ![image](https://opengraph.githubassets.com/e79632cf211a4dfa3137371dbed921f4/jhweintraub/execution-specs)



###



Specification for the Execution Layer. Tracking network upgrades.


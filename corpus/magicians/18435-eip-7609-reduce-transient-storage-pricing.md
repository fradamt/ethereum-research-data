---
source: magicians
topic_id: 18435
title: EIP-7609 reduce transient storage pricing
author: charles-cooper
date: "2024-02-01"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7609-reduce-transient-storage-pricing/18435
views: 3546
likes: 15
posts_count: 28
---

# EIP-7609 reduce transient storage pricing

discussion for: [EIP-7609: Decrease base cost of TLOAD/TSTORE](https://eips.ethereum.org/EIPS/eip-7609)

## Replies

**charles-cooper** (2024-02-01):

I ran some crude benchmarks using revm. The tools and methodology are below, but the tl;dr is:

plain dup2+mul 10k times ~20ns / operation

mload of the same address 10k times ~12ns / operation

tstore of the same address 10k times ~25ns / operation

tstore of 10k different addresses comes ~40ns / operation

tstore + tload of 10k different addresses ~70ns / operation

sha3 costs about 500ns / operation (sha3 of a 32 byte buffer)

script to generate evm scripts: [generate benchmarks for transient storage · GitHub](https://gist.github.com/charles-cooper/cfee0460891d3e0f1d3e433610773e53)

revm script: [feat: add evm script by charles-cooper · Pull Request #1039 · bluealloy/revm · GitHub](https://github.com/bluealloy/revm/pull/1039/commits/74bf32a60fec4ba0339b75c56c5093af6e9221c3)

i want to point out that the summary numbers are estimates, since there is some jitter from stack operations which throw off the numbers a bit (however, i do think they are more or less in the correct ranges). i added two control scripts which do some stack fiddling to mimic what the later operations do, so their timings can be subtracted from the relevant scripts.

results (from revm/bins/revm-test, running `for file in *.evm; do cargo run --release --bin evm $file; done`):

```auto
    Finished release [optimized + debuginfo] target(s) in 0.15s
     Running `/home/charles/src-references/revm/target/release/evm /home/charles/src-references/EIPs/benchmark_control2.evm`
Run bytecode (3.0s) ...              108_523.678 ns/iter (0.992 R²)
    Finished release [optimized + debuginfo] target(s) in 0.12s
     Running `/home/charles/src-references/revm/target/release/evm /home/charles/src-references/EIPs/benchmark_control.evm`
Run bytecode (3.0s) ...              222_961.624 ns/iter (1.000 R²)
    Finished release [optimized + debuginfo] target(s) in 0.12s
     Running `/home/charles/src-references/revm/target/release/evm /home/charles/src-references/EIPs/benchmark_easy_mload.evm`
Run bytecode (3.0s) ...              126_342.356 ns/iter (1.000 R²)
    Finished release [optimized + debuginfo] target(s) in 0.12s
     Running `/home/charles/src-references/revm/target/release/evm /home/charles/src-references/EIPs/benchmark_easy_tstore.evm`
Run bytecode (3.0s) ...              370_559.161 ns/iter (1.000 R²)
    Finished release [optimized + debuginfo] target(s) in 0.13s
     Running `/home/charles/src-references/revm/target/release/evm /home/charles/src-references/EIPs/benchmark_sha3.evm`
Run bytecode (3.1s) ...            4_947_213.996 ns/iter (1.000 R²)
    Finished release [optimized + debuginfo] target(s) in 0.12s
     Running `/home/charles/src-references/revm/target/release/evm /home/charles/src-references/EIPs/benchmark_tload_pure.evm`
Run bytecode (3.0s) ...              215_596.323 ns/iter (0.997 R²)
    Finished release [optimized + debuginfo] target(s) in 0.12s
     Running `/home/charles/src-references/revm/target/release/evm /home/charles/src-references/EIPs/benchmark_tstore.evm`
Run bytecode (3.0s) ...              619_875.709 ns/iter (0.999 R²)
    Finished release [optimized + debuginfo] target(s) in 0.12s
     Running `/home/charles/src-references/revm/target/release/evm /home/charles/src-references/EIPs/benchmark_tstore_tload.evm`
Run bytecode (3.1s) ...              936_628.376 ns/iter (0.998 R²)
```

---

**MariusVanDerWijden** (2024-02-15):

I created some tstore/tload state tests here: [tloadstore_opcode_statetests.json · GitHub](https://gist.github.com/MariusVanDerWijden/2f37dcd2f6419098fa3fb272a75ac493)

Results:

Tload: 46ms

Tstore: 205ms

For comparison, other tests I created on the same machine:

Push0: 86ms

Mstore8: 107ms

Mstore: 125ms

Sstore: 208ms

So it looks to me that tstore is priced correctly, tload is priced a bit high, but still in line with other opcodes

---

**Rjected** (2024-02-15):

are state tests a “good” or rigorous way to benchmark opcodes? how should we interpret / compare these results with [@charles-cooper](/u/charles-cooper) 's observations?

---

**charles-cooper** (2024-02-16):

[@Rjected](/u/rjected) i found there are a couple slightly tricky things to get right with the benchmarks:

- need to pop the result of TLOAD, otherwise the transaction can revert early (stack >1024 items) and time gets biased downwards
- tload from empty locations when the transient storage map is small or empty biases time downwards since the logic is if key not in map: return 0 and the existence check is very fast
- repeatedly tloading from the same location when the transient storage map is small biases time downwards because lookups from small maps are in general faster than lookups from large maps

what i did to address these issues in the benchmarks was to issue tload of an address after tstoring it.

so given those caveats, marius’s benchmarks look about right to me. the sstore benchmark seems too fast though - maybe it’s not physically writing to disk?

---

**charles-cooper** (2024-02-16):

i am not sure the coefficient in the EIP needs to be 3, either. with a coefficient of 1 we still get DoS protection (a single map [maxes out under the current gas limit at 7738 slots](https://www.wolframalpha.com/input?i=x%28x-1%29%2F2*1+%2B+8*x+%3D+30000000) ) but we get more breathing room for the “small maps” - 92 items before becoming more expensive than the current `TSTORE` rather than 30.

---

**charles-cooper** (2024-02-29):

i updated the coefficient here: [Update EIP-7609: reduce SLOPE coefficient in eip-7609 by charles-cooper · Pull Request #8272 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8272)

---

**gumb0** (2024-04-30):

Why is writing to existing slot 0 gas? EIP-1153 argued, that it definitely should be above MSTORE price because of interaction with reverts:

> Gas cost for TSTORE is the same as a warm SSTORE of a dirty slot (i.e. original value is not new value and is not current value, currently 100 gas), and gas cost of TLOAD is the same as a hot SLOAD (value has been read before, currently 100 gas). Gas cost cannot be on par with memory access due to transient storage’s interactions with reverts.

---

**gumb0** (2024-04-30):

Nevermind, it’s 8 gas for existing slot, not 0.

---

**xinbenlv** (2024-05-09):

Coming from [EIP for nonreentrant opcodes - #7 by xinbenlv](https://ethereum-magicians.org/t/eip-for-nonreentrant-opcodes/19957/7)

[@charles-cooper](/u/charles-cooper) do you know where is the best place to see the rationale from prior discussion why EIP-7609 was not prioritized?

---

**charles-cooper** (2024-05-09):

None was given to me. It was barely mentioned in [Execution Layer Meeting 185 · Issue #997 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/997), and it was not actually discussed on the call.

---

**xinbenlv** (2024-05-09):

Got it! Probably lack of attention. Just like the EIP-3074 waited for multiple years before they got proper attention.

I was on the ACD call and heard you in the last 3min. That was a good one to draw attention. Not that I have a voice in core development but I think this EIP has merit for smart contract developers. I will bring it up in discussions with other as I see fit, [@charles-cooper](/u/charles-cooper) . Thank you for drafting and driving this proposal

---

**benaadams** (2024-05-09):

Would support reduction; however WarmStateRead price does make sense?

Otherwise pattern will be SLOAD → TSTORE → TLOAD, TLOAD, TLOAD, TLOAD

Rather than SLOAD, SLOAD, SLOAD, SLOAD, SLOAD

AccessLists aside where there is a state access hit; perhaps warm storage read (SLOAD, TLOAD) is overpriced?

---

**charles-cooper** (2024-05-09):

There is an argument to be made that warm storage read is overpriced; but also DOS with the size of the in-memory map for warm storage is naturally prevented by the high cost of the initial cold storage load/store. From the EIP:

> As a comparison point, the total amount of memory which can be allocated on a client by SSTOREs in a given transaction is 30_000_000 / 20_000 * 32, or 48KB.

Transient storage does not have the same “protection”, this is why we consider a different DOS prevention mechanism.

---

**LukaszRozmej** (2024-05-09):

Not sure about other clients code, but for Nethermind it is exactly same code as for warm SLOAD and TLOAD, so pricing them the same makes sense.

---

**charles-cooper** (2024-05-09):

Honestly I see no issue with pricing warm SLOAD and SSTORE at the same proposed base cost as TLOAD / TSTORE (currently 5 and 8, respectively)

---

**benaadams** (2024-05-10):

> Honestly I see no issue with pricing warm SLOAD and SSTORE at the same proposed base cost

SSTORE is more complicated even for warm (including working out the price of SSTORE ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)) and it is inherntly a different beast so would probably want to leave that alone.

Reducing pricing for SLOAD would probably have to keep same current price for an access list “warm” load as it is incurring the cost of a cold load, and would have potental to open that up as a DoS vector (and have to consider potential block targetGas increases so as not to create a corner that needs repricing up to get out of)

Both TLOAD and SLOAD are more complex than MLOAD due to hashing vs array access; but you have gone with a higher price.

For TSTORE prehaps including it in the memory expansion cost at a x2 rate; would be an idea as it is storing more than MSTORE does (key+data)

---

**charles-cooper** (2024-05-10):

I’m not convinced by the way that `TLOAD` is substantially more complex than `MLOAD`.

Yes, there is a hash performed, but that is super cheap. Meanwhile, reads and writes from memory are always doing conversions to big-endian on the way in and little-endian on the way out. Depending how bigints are implemented on your system, TLOAD can be implemented by pointer copy; MLOAD requires allocating a new 32-byte item. It’s probably about the same cost as hashing in the end (xor’ing four 64-bit numbers together, another xor for salt and then mod by some prime number vs bswap64 four times and then writing out 32 bytes back to memory, *plus* a stack item allocation). The big cost with hashtables is probing when there is a collision, but this can be reasonably dealt with by using sufficiently low load factor. I will try to get a more “fair” comparison with MLOAD/MSTORE from nonzero memory. In the case where memory is larger and doesn’t fit in a single cache line, I suspect they are substantially similar in performance to TLOAD.

I have similar thoughts about `TSTORE`. It’s three writes in the worst case (in the revert case, it writes to the main map, the journal, and then the main map again), which is well accounted for by the extra 5 gas compared to MSTORE, and honestly I think I’m actually being overly conservative – I think each hashmap write costs about 1 (mayybe 2) gas of CPU time, so it could just as well be priced at 5 base gas. But maybe we could use a little more data here on how MLOAD/MSTORE fares on larger, nonzero memory chunks.

---

**wjmelements** (2024-05-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/benaadams/48/9199_2.png) benaadams:

> SSTORE is more complicated even for warm

How so? The revert behavior is the same. Once warm, we have already paid the access cost. The behavior is not conceptually different after that point. This is why warm SSTORE, warm SLOAD, TLOAD, and TSTORE are currently priced the same, at 100 gas. From EIP-1153:

> Gas cost for TSTORE is the same as a warm SSTORE of a dirty slot

---

**benaadams** (2024-05-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> Once warm, we have already paid the access cost. The behavior is not conceptually different after that point.

SSTORE pricing depends on multiple factors and refund accounting as well as if value is actually changing so isn’t a straightforward +100 gas. It has been heavily anaylised and justified; so  I’d consider repricing it out of scope or a require much deeper analysis, flow and exhaustive list of test cases costs with prices.(as per [EIP-2200: Structured Definitions for Net Gas Metering](https://eips.ethereum.org/EIPS/eip-2200) and [EIP-3529: Reduction in refunds](https://eips.ethereum.org/EIPS/eip-3529))

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> Gas cost for TSTORE is the same as a warm SSTORE of a dirty slot

Which isn’t a valid justification for repricing `SSTORE`; its saying what the price of `TSTORE` should be.

---

**benaadams** (2024-05-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> Meanwhile, reads and writes from memory are always doing conversions to big-endian on the way in and little-endian on the way out.

You are thinking of push and pops to stack, as memory goes via stack no endian conversion happens. Is also one `_mm256_permutevar64x8_epi8` instruction to do the coversion whereas hashing has a dependency chain of instructions with the input of one instruction waiting on output of another. Memory is an array offset lookup so is inherently simplier than a hashtable lookup. Could also be a pointer copy to that location if that’s your thing. But this is getting into the weeds a bit on specific implementations which can vary between clients.

The addtional difference between `TSTORE` and `MSTORE` is `TSTORE` additionary requires the key `(address: byte20, slot: byte32)` as well as the `byte32` value; so each new entry is requiring > x2 the memory of `MSTORE` which just writes to a position and is only one `byte32` value.

Hence the suggestion that it is included in the memory expansion cost at a x2 rate:

e.g. `memory use = memory slots + 2 x tstore slots`

Rather than having its own load factor


*(7 more replies not shown)*

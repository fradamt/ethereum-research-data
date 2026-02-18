---
source: magicians
topic_id: 23794
title: "EIP series: EVM64"
author: sorpaas
date: "2025-04-23"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-series-evm64/23794
views: 348
likes: 4
posts_count: 11
---

# EIP series: EVM64

Master discussion topic for the series of EIPs that define EVM64.

Option A is EVM64 with prefix opcode `0xC0`.

- EIP-7937 of EVM64 for endianness-independent arithmetic, comparison, bitwise and flow operations.
- EIP-9819 for EOF support.
- EIP-9821 for little-endian BYTE64, MLOAD64, MSTORE64 and PUSH*64 opcodes.

Option B is “pure” EVM64 via EOF code section.

- EIP-9834 which defines an extended version of types_section for EOF.
- EIP-9835 which defines the EVM64 code section type.

#### Update Log

- 2025-04-23: Initial draft
- 2025-04-24: EIP number is (re-)assigned to 7937
- 2025-04-25: Added missing SHR, SHL, SAR 64-bit mode. Updated “Rationale” section.
- 2025-04-25: Removed DUP* and SWAP* 64-bit mode.
- 2025-05-25: Added a reference implementation in rust-evm.

#### External Reviews

None as of 2025-04-23.

#### Outstanding Issues

None as of 2025-04-23.

## Replies

**jochem-brouwer** (2025-05-26):

I have some general comments here.

I can understand the motivation for this EIP to target 64-bit hardware and to use that as rationale that these opcodes can be computed as low-level instructions (possibly just one operation) on a 64-bit processor. Which would therefore lead to lower gas costs. However, in the EVM we thus have to apply extra work first (`mod 2^64` all inputs, or discard those topmost bits, but I would assume this needs some kind of “extra” operation before doing the “actual” operation). This would thus add extra work. I’m not sure if there is a low-level optimization for this, but this would still need benchmarks to show that this is indeed faster (and then also be very specific on which hardware this is used).

EDIT: In Optimization Assumptions it is noted that the 256-bit stack items should be represented as 4 64-bit stack items each. Would love to see how this works in practice especially with the 256-bit opcodes still available and how this would interact.

Another problem and challenge which I can foresee is that there is not much “wiggle room” to reprice the opcodes. For instance, an opcode reprice from 3 to 2 thus effectively means 33%+ reduction of the price! ( ![:open_mouth:](https://ethereum-magicians.org/images/emoji/twitter/open_mouth.png?v=12) ). There has been work for fairer EVM repricings in the past, and to also introduce “partial” gas to address this repricing problem, see: [EIP-2045: Particle gas costs for EVM opcodes](https://eips.ethereum.org/EIPS/eip-2045)

This part from the EIP:

> Backwards Compatibility
>
>
> This EIP introduces a new (prefix) opcode C0. C0 was previously an invalid opcode that has little usage, and thus the backward compatibility issues are minimal.

This is true and I would normally agree with this, however there is now an extra consideration which has to be made (and researched): `C0 JUMPDEST` would before this EIP encode a valid `JUMPDEST`. However, when this EIP is activated, this `JUMPDEST` is thus (?) an invalid `JUMPDEST`. I don’t think this will lead to problems in practice, but it could for instance be a bug in a compiler which would output this malformed code (and this `C0` would then not be reached from runtime code but would rather be encoded data). This would obviously break things and has to be considered.

EDIT: And right, I forgot, the C0 prefix will mean we pay 200 bytes per 64-bit opcode extra on deployment. So converting an existing contract to the 64-bit variant will thus double in size. I think we discussed this before, the reasoning was: you pay more on deployment but the more you use the contract the greater the benefits are, so this extra code deposit cost is then worth it ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12) ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12) But, this obviously needs an implementation and a benchmark to show these lower gas costs are reasonable and not underpriced.

---

**sorpaas** (2025-05-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> EDIT: In Optimization Assumptions it is noted that the 256-bit stack items should be represented as 4 64-bit stack items each. Would love to see how this works in practice especially with the 256-bit opcodes still available and how this would interact.

I know this is the way things works in Go implementations Geth and Erigon (see [GitHub - holiman/uint256: Fixed size 256-bit math library](https://github.com/holiman/uint256)) and also how things works in Rust implementations `rust-evm` and `revm`. They all do 4 64-bit stack items.

This is probably the only way one writes an efficient EVM interpreter, because the alternative would be `[u8; 32]` in big endian, and if one do that they’ll need to reverse the endianness for every math operations!

For all of those “efficient EVM interpreters”, even “inefficient EVM interpreters”, the core EVM64 (those defined in EIP-7937) never results in extra work. The core definition is endianness-independent. If you do `[u64; 4]`, then you simply take the least significant `u64` and work on that. If you do `[u8; 32]`, then you take the least significant 8 bytes and do whatever you also do for 256 bits.

Only the non-endianness-independent little endian opcodes (`BYTE64`, `MSTORE64`, `MLOAD64`, `PUSH*64`) relies on the “efficient EVM interpreter” assumption, but as said before this is really the only way one can write an efficient EVM interpreter!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Another problem and challenge which I can foresee is that there is not much “wiggle room” to reprice the opcodes. For instance, an opcode reprice from 3 to 2 thus effectively means 33%+ reduction of the price! (  ).

For this I agree. Still, we don’t need to reduce the gas cost too much in one go. There’s no harm to further reduce gas costs later.

---

**sorpaas** (2025-05-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> This is true and I would normally agree with this, however there is now an extra consideration which has to be made (and researched): C0 JUMPDEST would before this EIP encode a valid JUMPDEST. However, when this EIP is activated, this JUMPDEST is thus (?) an invalid JUMPDEST. I don’t think this will lead to problems in practice, but it could for instance be a bug in a compiler which would output this malformed code (and this C0 would then not be reached from runtime code but would rather be encoded data). This would obviously break things and has to be considered.

I actually missed this and I think this is a really important thing. Backward compatbility takes priority. I changed EIP-7937 to:

> In JUMPDEST validation phrase, C0 is considered a standalone “mode” opcode and if the next byte followed is JUMPDEST, it continues to mark a valid JUMPDEST destination. Note that because there’s no 64-bit JUMPDEST, during execution, C0 JUMPDEST would result in OOG.

This is probably the best way to define multi-byte opcode in EVM – we still consider them as separate opcodes. The first opcode sets a mode (“64-bit mode”) that modifies the behavior of the second opcode.

In “legacy” EVM this is perhaps the only way that this will work. In EOF EVM we can possibly attempt further validations.

---

**sorpaas** (2025-05-26):

The only other edge case is if the 64-bit mode opcode `C0` is the end of the contract, currently it’s defined that in this case, the contract should OOG.

It’s not possible to have `C0`, then jump to a different place while still having the 64-bit mode set, because there must have been a jump opcode.

---

So to summarize, there are two ways you can think about how the 64-bit mode opcode `C0` behaves. The two definitions below are equivalent.

### As a multi-byte opcode

The parsing of the multi-byte opcode happens dynamically in the execution. It’s possible to jump into the middle of a multi-byte opcode (the only possible case is `JUMPDEST`).

### As an opcode that sets “64-bit mode”

`C0` can be considered a standalone opcode, which does the following:

- Set “64-bit mode” to true.
- Check if it’s the last byte of the contract code, if so, OOG.

Upon evaluating an opcode, the interpreter does the following:

- Check if “64-bit mode” is set.
- If “64-bit mode” is set,

It checks if there is a definition of “64-bit mode” for the executing opcode. If not, OOG.
- Reset “64-bit mode”.
- Execute the “64-bit mode” routine.

If “64-bit mode” is not set, do execution as usual.

---

**jochem-brouwer** (2025-05-26):

If you would take a practical contract and assume it also works in 64-bit mode then it would be beneficial to see what happens to the code size. Are 64-bit opcodes also chained (followed by each other like ADD SUB MUL or something) by default? (I would assume so).

Did you also consider (I vaguely remember proposing this before) to instead use an activation/deactivation marker in the code to switch the 64bit mode on or off? Then you could chain multiple 64-bit operations together without having to pre-mark everything with C0. Then for instance C0 would activate the 64-bit mode and C1 would deactivate it. And I guess, if you hit a JUMPDEST/JUMP/JUMPI it will disable it also if it is enabled. This would obviously not work if all 64-bit operations run in isolation, because then the 64-bit opcode has changed from a 1-byte opcode to now thus a 3-byte opcode ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

EDIT: nvm, discussed that here [Add EIP: 64-bit mode EVM opcodes (EVM64) by sorpaas · Pull Request #9687 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9687#discussion_r2059403431)

---

**sorpaas** (2025-05-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Did you also consider (I vaguely remember proposing this before) to instead use an activation/deactivation marker in the code to switch the 64bit mode on or off?

I thought about this but I’m against it, for several reasons:

- The primary reason is that we then truly cannot consider EVM64 as multi-byte opcodes. Right now the only edge case we need to consider is if the second byte is JUMPDEST and in this case we need to allow jumping in the middle. This can still be efficiently handled for static analysis and for optimization. Activation/deactivation marker will make things a lot more messy. Even if we disable the marker on jump, someone might still jump to a JUMPDEST in the middle (to the region where normally the 64-bit marker is set). Trying to figure out if an opcode is EVM64 or not will be impossible.
- If we can’t statically figure out if an opcode is EVM64 or not we’ll have big problems in JITs/recompilers. If we want to really take advantage of the speed of EVM64, JITs will eventually come, and we should make sure we do not hinder that.
- Gradual optimization is probably what we’ll see in contract development. For example, the immediate thing you can do in Solidity is to change a forloop counter from using ADD to ADD64, which will speed up things a little bit, and so on. We’ll eveutally see large blocks of EVM64 code especially for the computationally heavy things, but those only happen gradually. Activation marker will not play along into this.
- The increase in contract size is in my opinion not a big deal. Remember, RISC-V has 32-bit/16-bit instruction. It’s register-based so obviously different, but still we’ll translate at least one EVM instruction to one RISC-V instruction. There’s no disadvantage of size at least here.

---

**gcolvin** (2025-08-05):

I’m sorry to be late to this review.  What I don’t understand is why we need multibyte opcodes, or mode switches, or code sections for 64-bit arithmetic.  Why not just bite the bullet and set aside a full 32 bytes for 64-bit opcodes?  Say [B0 … CF].  We can afford it, it’s worth it, and it’s much simpler.  I’ve been listening to complaints about the lack of 64-bit opcodes for nine years now.

---

**sorpaas** (2025-08-06):

We have 140 defined opcodes now. I just thought that it’s probably important to “conserve” opcode usage (there are only free 116 left).

For EVM64 we need 12 arithmetic opcodes, 14 comparison/bitwise opcodes, 2 for control flow, and 11 for memory and stack. That’s in total 39 of them already. Technically this will fit, but we then will only have 77 free left!

---

**gcolvin** (2025-08-07):

Yes.  But we have been saving up unused opcodes for years, and I really can’t think of anything more important to do with these.  Someday, something else might have to make do with immediate data.  Maybe.

---

**gcolvin** (2025-08-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sorpaas/48/1074_2.png) sorpaas:

> For EVM64 we need 12 arithmetic opcodes, 14 comparison/bitwise opcodes, 2 for control flow, and 11 for memory and stack.

I don’t think we really need control flow or stack opcodes.  Top bits can be masked off before jumps.  and I think zeroing out the top bits is the right thing to do for pushes.  So that’s 12 arithmetic, 14 logic, MSTORE64, and MLOAD64.  28 new codes, 88 free!


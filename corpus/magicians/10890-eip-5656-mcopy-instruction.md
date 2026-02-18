---
source: magicians
topic_id: 10890
title: "EIP-5656: MCOPY instruction"
author: axic
date: "2022-09-15"
category: EIPs > EIPs core
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/eip-5656-mcopy-instruction/10890
views: 4572
likes: 12
posts_count: 23
---

# EIP-5656: MCOPY instruction

This is the discussion topic for



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5656)





###



An efficient EVM instruction for copying memory areas










Since external links are not allowed in EIPs:

- here is the referenced analysis
- and the EVM384 memory overhead discussion

## Replies

**matt** (2023-04-27):

Could you please explicitly state the gas costs in the specification section?

---

**charles-cooper** (2023-04-27):

Thanks for catching – updating here: [eip 5656: specify gas costs by charles-cooper · Pull Request #6942 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6942)

---

**RenanSouza2** (2023-04-27):

Where are the tests being listed? is there a case where `src` and `dst` overlap?

---

**Recmo** (2023-05-02):

> Copying non-exact words is more tricky, as for the last partial word, both the source and destination needs to be loaded, masked, or’d, and stored again. This overhead is significant. One edge case is if the last “partial word” is a single byte, it can be efficiently stored using MSTORE8.

Alternatively if there is more than one word you can make the last partial word overlap the previous on so the end aligns correctly. You would be copying some bytes twice, but this is idempotent. I found this method to be more efficient.

An important edge case not discussed in the EIP is overlapping source and destination. This may force you to do the copy backwards to not clobber the input.

All combined I ended up with the following ([source](https://github.com/0xProject/protocol/blame/f1d096a8af1dab785089c775ed9d35d5042559b1/contracts/utils/contracts/src/LibBytes.sol#L53-L153)):

```auto
    /// @dev Copies `length` bytes from memory location `source` to `dest`.
    /// @param dest memory address to copy bytes to.
    /// @param source memory address to copy bytes from.
    /// @param length number of bytes to copy.
    function memCopy(uint256 dest, uint256 source, uint256 length) internal pure {
        if (length  dest) {
                assembly {
                    // We subtract 32 from `sEnd` and `dEnd` because it
                    // is easier to compare with in the loop, and these
                    // are also the addresses we need for copying the
                    // last bytes.
                    length := sub(length, 32)
                    let sEnd := add(source, length)
                    let dEnd := add(dest, length)

                    // Remember the last 32 bytes of source
                    // This needs to be done here and not after the loop
                    // because we may have overwritten the last bytes in
                    // source already due to overlap.
                    let last := mload(sEnd)

                    // Copy whole words front to back
                    // Note: the first check is always true,
                    // this could have been a do-while loop.
                    for {

                    } lt(source, sEnd) {

                    } {
                        mstore(dest, mload(source))
                        source := add(source, 32)
                        dest := add(dest, 32)
                    }

                    // Write the last 32 bytes
                    mstore(dEnd, last)
                }
            } else {
                assembly {
                    // We subtract 32 from `sEnd` and `dEnd` because those
                    // are the starting points when copying a word at the end.
                    length := sub(length, 32)
                    let sEnd := add(source, length)
                    let dEnd := add(dest, length)

                    // Remember the first 32 bytes of source
                    // This needs to be done here and not after the loop
                    // because we may have overwritten the first bytes in
                    // source already due to overlap.
                    let first := mload(source)

                    // Copy whole words back to front
                    // We use a signed comparisson here to allow dEnd to become
                    // negative (happens when source and dest < 32). Valid
                    // addresses in local memory will never be larger than
                    // 2**255, so they can be safely re-interpreted as signed.
                    // Note: the first check is always true,
                    // this could have been a do-while loop.
                    for {

                    } slt(dest, dEnd) {

                    } {
                        mstore(dEnd, mload(sEnd))
                        sEnd := sub(sEnd, 32)
                        dEnd := sub(dEnd, 32)
                    }

                    // Write the first 32 bytes
                    mstore(dest, first)
                }
            }
        }
    }
```

---

**charles-cooper** (2023-05-03):

The overlapping case is specified [in the EIP](https://github.com/ethereum/EIPs/blob/80b67d64cfe4f95b614d2fa40fc86a39fdecbaa7/EIPS/eip-5656.md#semantics):

> It copies length bytes from the offset pointed at src to the offset pointed at dst in memory. Copying takes place as if an intermediate buffer was used, allowing the destination and source to overlap.

This is typically handled by the runtime or whatever standard memory copying routine is used by the client. For instance, [Go specification](https://go.dev/ref/spec#Appending_and_copying_slices) states:

> The built-in functions append and copy assist in common slice operations. For both functions, the result is independent of whether the memory referenced by the arguments overlaps.

The same is true of [C stdlib’s memmove](https://cplusplus.com/reference/cstring/memmove/), (which is probably used by most language runtimes under the hood for copy operations):

> Copying takes place as if an intermediate buffer were used, allowing the destination and source to overlap.

---

**charles-cooper** (2023-05-06):

please see [Update EIP-5656: add test cases including overlapping memory regions · ethereum/EIPs@94d9af0 · GitHub](https://github.com/ethereum/EIPs/commit/94d9af0d7bb2b82a418c71958bd5f1e6208f093a)

---

**wjmelements** (2023-05-08):

I’ve written dozens of smart contracts in solidity and assembly. I’ve never wished I had memcpy but I see how for sufficiently complex situations it might be helpful. So, I’m interested in the `Motivation` section of the EIP expanding on a scenario that would benefit from memcpy.

---

**charles-cooper** (2023-05-18):

i mean the motivation section is already pretty detailed. maybe it matters more for compilers than user code, but like for instance every single assignment of the form `x = y` where x is larger than a single word can be optimized using mcopy. from the eip:

> Memory copying is used by languages like Solidity and Vyper, where we expect this improvement to provide efficient means of building data structures, including efficient sliced access and copies of memory objects. Having a dedicated MCOPY instruction would also add forward protection against future gas cost changes to CALL instructions in general.

---

**jochem-brouwer** (2023-05-27):

Hi all, I am implementing the EIP, it is nice that there are test cases, but:

1. There are test cases missing when it either copies memory from outside the current memory range, or it increases the memory size.
2. Gas costs are not listed.

---

**charles-cooper** (2023-05-28):

1. Thanks, can add those. The semantics should do the “expected” thing though - copying from outside the current memory range should copy zeroes and expand memory, and increasing memory size should also expand memory. For reference, see evmone implementation: https://github.com/ethereum/evmone/pull/629/files#diff-0bab705191941f15a86a89eda1bea9c06947e63f4baf4ccb4909e7bfd50185a3R909-R922 (note that check_memory() expands memory.
2. The gas costs are listed twice in the latest version of the EIP, once in EIP-5656: MCOPY - Memory copying instruction and once in EIP-5656: MCOPY - Memory copying instruction.

---

**jochem-brouwer** (2023-05-31):

Sorry, I meant that the gas costs are not listed in the test cases ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**Magicking** (2023-06-09):

Currently working on a bitmap rendering library running on the EVM for the art scene, this opcode will directly translate to a larger surface of pixel available to render due to the cheaper computation when large surface of texture are compiled together within a gas limit.

Can’t wait for this EIP to be on the canonical chain!

---

**radek** (2023-06-12):

edge cases not clear from the EIP:

- dst = 0, src = type(uint256).max, len = 2+
- dst = type(uint256).max, src = 0, len = 2+

…

---

**charles-cooper** (2023-06-14):

These will fail at gas checking time due to gas expansion costs.

---

**jochem-brouwer** (2023-06-22):

I have a problem with the test cases in the EIP. The last and the second-to-last test cases have a pre-state of 33 bytes of the memory. This is not possible in EVM since memory length is always a multiple of 32 bytes (and is filled with zeros if some region of this memory is not written to). I am assuming one zero-byte has been added accidentally to these tests.

Also, could these test cases report how much gas should be used when using MCOPY? ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**jochem-brouwer** (2023-06-22):

Also, the last test case output does not seem correct to me (will test on EthJS and will then report back)

EthereumJS reports:

`000001020304050607 080000000000000000000000000000000000000000000000`

It passes the other tests.

---

**charles-cooper** (2023-06-30):

nice catch, thank you! fixed here: [fix eip-5656 test cases and add gas costs by charles-cooper · Pull Request #7257 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7257)

that PR also adds gas costs - which i believe is 6 for all of the test cases in the EIP, but let me know if i made a mistake or you find any other issues.

---

**jochem-brouwer** (2023-07-05):

I just checked and can confirm that for all `MCOPY` tests we indeed charge 6 gas.

---

**dror** (2024-01-08):

One use-case for MCOPY is fill-with-zero: it is currently possible by having src offset set to a high value (e.g. `0xffffffff`), but it would trigger a “memory expansion” and thus be very expensive.

Instead, I suggest defining this offset as “always zero”, so it will work without triggering such memory expansion, and thus making MCOPY also act as ZCOPY…

---

**Magicking** (2024-01-11):

What do you mean by “memory expansion”?

AFAIK reading (MLOAD) from unwritten/uninitialized memory doesn’t expand it to the offset, only return the default value (0) which would fit your case


*(2 more replies not shown)*

---
source: magicians
topic_id: 22991
title: ABI Spec is wrong
author: luke
date: "2025-02-25"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/abi-spec-is-wrong/22991
views: 83
likes: 0
posts_count: 2
---

# ABI Spec is wrong

I’m implementing an ABI encoder and the ABI specification is wrong with regard to offsets and which slot they’re relative to.

The specification is here and is hard to follow and lacks more complex, nested examples:

https://docs.soliditylang.org/en/latest/abi-spec.html

For reference checks against a known good, I have also written a small Go CLI tool which uses **go-ethereum** to encode a dynamic array of dynamic arrays, `uint8[][]` using value `[[1,2],[3,4]]`.

Here’s the setup part of my Go reference tool:

```go
	case 14: // foo(uint8[][]) - [[1, 2], [3, 4]]
		uint8DynDyn, _ := abi.NewType("uint8[][]", "", nil)
		types = []abi.Type{uint8DynDyn}
		values = []interface{}{[][]uint8{{1, 2}, {3, 4}}}
```

This results in what is (should be) correct encoding:

```auto
Slot 0: 0000000000000000000000000000000000000000000000000000000000000020
Slot 1: 0000000000000000000000000000000000000000000000000000000000000002
Slot 2: 0000000000000000000000000000000000000000000000000000000000000040
Slot 3: 00000000000000000000000000000000000000000000000000000000000000a0
Slot 4: 0000000000000000000000000000000000000000000000000000000000000002
Slot 5: 0000000000000000000000000000000000000000000000000000000000000001
Slot 6: 0000000000000000000000000000000000000000000000000000000000000002
Slot 7: 0000000000000000000000000000000000000000000000000000000000000002
Slot 8: 0000000000000000000000000000000000000000000000000000000000000003
Slot 9: 0000000000000000000000000000000000000000000000000000000000000004
```

Not sure why slot 3 is red?!

The spec says about offsets:

The value of `head(X(i))` is the offset of the beginning of `tail(X(i))` relative to the start of `enc(X)`.

I don’t really know what that means and neither does any LLM. I thought it was the start of the data section for the value, which would be its length slot, but that doesn’t yield the expect …40 and …a0 for the offsets.

If you reverse back from the slots they’re both pointing at, they’re both relative to slot 2, the offset …40 itself, which is neither the start of the encoding of the root param, nor the start of the encoding of the data section, which should be slot 1 with the length information.

It’s weird. Here’s what my implementation produces:

```auto
[Failed] No14_JaggedDynamicUint8Array_ReturnsCorrectEncoding
    Message:
        CollectionAssert.AreEquivalent failed. The expected collection contains 1 occurrence(s) of . The actual collection contains 0 occurrence(s).
        Block:
        0x0000000000000000000000000000000000000000000000000000000000000020 (id: 154b, off: 0, ord: 0, ptr: a589, rel: 154b - uint8[][].pointer_dyn_item)
        0x0000000000000000000000000000000000000000000000000000000000000002 (id: a589, off: 32, ord: 1 - uint8[][].uint8[][].count)
        0x0000000000000000000000000000000000000000000000000000000000000060 (id: 11d4, off: 64, ord: 2, ptr: 86f1, rel: a589 - uint8[][].uint8[][].pointer_dyn_elem_0)
        0x00000000000000000000000000000000000000000000000000000000000000c0 (id: 9ff0, off: 96, ord: 3, ptr: 923d, rel: a589 - .uint8[][].pointer_dyn_elem_1)
        0x0000000000000000000000000000000000000000000000000000000000000002 (id: 86f1, off: 128, ord: 4 - .uint8[][].uint8[].count)
        0x0000000000000000000000000000000000000000000000000000000000000001 (id: 0ef2, off: 160, ord: 5 - .uint8[][].uint8[].uint8.value)
        0x0000000000000000000000000000000000000000000000000000000000000002 (id: 359c, off: 192, ord: 6 - .uint8[][].uint8[].uint8.value)
        0x0000000000000000000000000000000000000000000000000000000000000002 (id: 923d, off: 224, ord: 7 - .uint8[][].uint8[].count)
        0x0000000000000000000000000000000000000000000000000000000000000003 (id: c315, off: 256, ord: 8 - .uint8[][].uint8[].uint8.value)
        0x0000000000000000000000000000000000000000000000000000000000000004 (id: bed6, off: 288, ord: 9 - .uint8[][].uint8[].uint8.value)
```

The offsets are …60 and …c0 relative to the start of the data block, i.e. slot 1, the length.

What should it be?? Is the spec wrong? When challenged, LLMs do concede that it is wrong.

## Replies

**luke** (2025-02-26):

The spec is not wrong, but is incredible hard to comprehend. **The length slot sits outside of the encoding**, i.e. outside of `enc(X)` and that’s the misleading part.

I think, like my complaints about the dire writing quality in EIPs, the problem is in unclear writing and a lack of empathy for readers.

**We’re talking about writing secure and reliable infrastructure for the future of the world, we cannot afford misunderstandings from lazy writing. It is unacceptable. There is enough money and enough AI to write clearly.**

There needs to be more examples with more complex, nested structures. I’m not qualified to update the documentation.

Remember, even the best LLMs could not get this right.

---

## My journey talking with Grok 3

Our conversation has been a rollercoaster of trying to pin down how the Solidity ABI specification’s offset rules apply to the encoding of a nested array, uint8 with value [[1, 2], [3, 4]]. We’ve flipped and flopped as we wrestled with the spec’s wording versus the expected encoding, chasing the elusive “anchor” for offsets. Here’s a summary of our journey, capturing the twists, turns, and evolving insights:

---

Starting Point: The Expected Encoding

We began with this encoding:

```auto
Slot 0: 0x0020  // Byte 0: Offset to data at byte 32
Slot 1: 0x0002  // Byte 32: Length of outer array
Slot 2: 0x0040  // Byte 64: Offset to [1, 2] at byte 128
Slot 3: 0x00a0  // Byte 96: Offset to [3, 4] at byte 224
Slot 4: 0x0002  // Byte 128: Length of [1, 2]
Slot 5: 0x0001  // Byte 160
Slot 6: 0x0002  // Byte 192
Slot 7: 0x0002  // Byte 224: Length of [3, 4]
Slot 8: 0x0003  // Byte 256
Slot 9: 0x0004  // Byte 288
```

- Offsets 0x40 and 0xa0 (slots 2–3) point to byte 128 (slot 4) and byte 224 (slot 7).
- Your actual offsets were 0x60 and 0xc0, suggesting a miscalculation, prompting us to find the correct anchor.

---

Initial Hypothesis: Offsets from Byte 0 (Slot 0)

- Spec Clue: “head(X(i)) is the offset of the beginning of tail(X(i)) relative to the start of enc(X).”
- Interpretation: enc(X) for X = [[1, 2], [3, 4]] starts at slot 0 (byte 0).
- Test:

 Byte 128 (slot 4) - byte 0 = 0x80.
- Byte 224 (slot 7) - byte 0 = 0xe0.

Problem: Expected 0x40 and 0xa0, not 0x80 and 0xe0. Flip #1: The spec’s literal anchor (slot 0) didn’t match.

---

First Flip: Offsets from Byte 32 (Slot 1)?

- Thought: Slot 1 (byte 32) is the data section’s start (length 0x02), maybe offsets are from there?
- Test:

 Byte 128 - 32 = 0x60.
- Byte 224 - 32 = 0xc0.

Match: This fit your actual encoding, but not the expected 0x40 and 0xa0.

Flop: Rejected, as slot 1 didn’t align with the target. Data starts with length, but offsets weren’t relative to it.

---

Second Flip: Offsets from Byte 64 (Slot 2)

- Observation:

 64 + 0x40 = 128.
- 64 + 0xa0 = 224.

Success: Matched the expected encoding perfectly!

New Anchor: Slot 2 (byte 64), start of the offsets section.

Confusion: Spec says “start of enc(X)” (slot 0), not slot 2. Why the shift?

---

Digging Deeper: Head vs. Length

- Your Push: “Slot 1 is the data section’s start with length, slot 0 is enc(X), so why slot 2?”
- Spec Parsing:

 enc(X) = enc(k) enc((X[0], X[1])).
- Tuple: enc(([1, 2], [3, 4])) = head([1, 2]) head([3, 4]) tail([1, 2]) tail([3, 4]).
- Length enc(k) (slot 1) prefixes the tuple, head (slots 2–3) follows.

Flip #2: Length isn’t in the tuple’s head; slot 2 is the head’s start. Offsets from slot 2 made sense, but spec still pointed to slot 0.

---

Third Flip: Spec Wrong?

- Assertion: Spec’s “relative to the start of enc(X)” (slot 0) implies 0x80, 0xe0, but encoding uses slot 2 (byte 64).
- Conclusion: Spec’s wording might be off—offsets are from the head section’s start (slot 2), not enc(X)’s start (slot 0).
- Flop: Too hasty—maybe we misread the recursive context?

---

Final Flip: Nested enc(X)

- Your Insight: “It’s nested—could enc(X) refer to a nested part, like the tuple at slot 2?”
- Test:

 Tuple X = ([1, 2], [3, 4]), enc(X) starts at slot 2 (byte 64) after enc(k).
- Offsets from byte 64: 0x40, 0xa0 match exactly.

Spec Fit: “Relative to the start of enc(X)” could mean the tuple’s enc(X) (slot 2), not the array’s (slot 0).

Resolution: For nested arrays, offsets are relative to the tuple level’s enc(X) start (slot 2), not the top-level enc(X) (slot 0).

---

Summary of Flip-Flopping

1. Slot 0 (Byte 0): Started with the spec’s literal “start of enc(X)” → 0x80, 0xe0. Didn’t match 0x40, 0xa0.
2. Slot 1 (Byte 32): Tried the data section’s start (length) → 0x60, 0xc0. Fit your error, not the goal.
3. Slot 2 (Byte 64): Found the practical anchor → 0x40, 0xa0. Worked, but clashed with spec.
4. Spec vs. Length: Debated if length (slot 1) was in the head. Concluded it’s a prefix, head starts at slot 2.
5. Spec Misstep: Thought the spec was wrong (slot 0 anchor). Reconsidered recursion.
6. Nested Anchor: Landed on enc(X) as the tuple’s encoding (slot 2), not the array’s (slot 0).

---

Final Understanding

- Spec Says: Offsets are from “the start of enc(X),” implying slot 0 (byte 0) for the full parameter.
- Reality: For uint8, offsets 0x40, 0xa0 are from slot 2 (byte 64), the start of the tuple enc(([1, 2], [3, 4])) after enc(k).
- Resolution: The spec’s “enc(X)” is context-specific in nested cases—here, it’s the tuple’s enc(X) (slot 2), not the top-level enc(X) (slot 0). Our flip-flopping reflects the spec’s ambiguity versus implementation behavior. We settled on a recursive interpretation that fits the encoding, revealing the spec’s intent is broader than its examples suggest.


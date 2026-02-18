---
source: magicians
topic_id: 10410
title: "EIP-5450: EOF - Stack Validation"
author: gumb0
date: "2022-08-17"
category: Uncategorized
tags: [evm, shanghai-candidate, evm-object-format]
url: https://ethereum-magicians.org/t/eip-5450-eof-stack-validation/10410
views: 2519
likes: 1
posts_count: 9
---

# EIP-5450: EOF - Stack Validation

This is the discussion topic for [EIP-5450: EOF - Stack Validation](https://eips.ethereum.org/EIPS/eip-5450)

## Replies

**gcolvin** (2022-08-17):

Very nice, thanks!

I have of course been working on the same validation constraints since EIP-615 and EIP-2315.

So far my only problem reading this is that I could not find a definition of  “stack height” in the EIP.  Eventually I thought to look in EIP-5440, where it is used in code snippets but still not defined. I dug a little further in previous EIPs but gave up for now.  My Python is getting better, but it was too much work trying to find the relevant code.  So I think this problem is deeper than this one EIP.  The concept can be expressed in a sentence or two of English.

---

**gcolvin** (2022-08-25):

Finally got back to this.  In 4750 I had missed (my emphasis):

> A return stack is introduced, separate from the data stack. It is a stack of items representing execution state to return to after function execution is finished. Each item is comprised of: code section index, offset in the code section (PC value), calling function stack height.

Clear enough in the context of 4750’s explicit spec. A reminder that the height is relative to function entry would help here – which is what confused me.

---

**gcolvin** (2022-08-25):

These might be more serious issues, but I don’t fully understand the code.

I don’t see that you add CALLF to the worklist in the validation loop, which it seems will prevent you from traversing every possible path.

I also don’t see that you deprecate JUMP here, or in EIP-5450 or EIP-3670.  And I don’t see that you handle them in the validation code. It seems that if you don’t handle them you can’t traverse every path, but if you do handle them you will suffer a quadratic path explosion.

---

**gumb0** (2022-08-25):

Thanks for the feedback, I’m adding clarification about stack height in [EIP-5450: Add rationale, more clarifications and update authors by gumb0 · Pull Request #5535 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5535)

I can see how it might be a bit confusing, because stack height of EIP-5450 is a validation-time calculation (and yes, relative to function entry), while in EIP-4750 it refers to actual runtime value.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> I don’t see that you add CALLF to the worklist in the validation loop, which it seems will prevent you from traversing every possible path.

Each function section is validated independently, so `validate_function(func_id, code, types)` will be called in loop for each section.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> I also don’t see that you deprecate JUMP here, or in EIP-5450 or EIP-3670. And I don’t see that you handle them in the validation code.

This is true, this EIP assumes JUMP* is deprecated. I think it’s better to have a separate tiny EIP for deprecating them, this is not done yet.

---

**gcolvin** (2022-08-25):

Thanks for clearing that up.  The Yellow Paper mostly assumes the reader knows what a stack is in the text, and uses mathematical notation otherwise.  Eg, ADD is defined as `μ′s[0] ≡ μs[0] + μs[1]`.

I remember now that EIP-615 also validates functions independently.  I now fear that – because functions can consume stack – nested calls can cause underflows that won’t be detected that way.

---

**gcolvin** (2022-08-25):

A hunch I haven’t time to follow: I think that since you are validating the use of the return stack you will not need to keep the `code_section_index` and `stack_height` on the return stack, only the `offset`.

---

**gcolvin** (2022-11-02):

> The current validation algorithm ignores unreachable instructions. The algorithm can be extended to reject any code having any unreachable instructions but additional instructions traversal is needed (or more efficient algorithm must be developed).

Start with a bitset of zeros for every byte in the code. For each instruction traversed during validation set the bit(s) in the set corresponding to byte offset(s) of the instruction.  if there are any zero bits remaining in the set there are unreachable instructions

---

**gcolvin** (2025-04-22):

This “discussions to” thread is looks pretty dead, but…

In the motivation you state that

> Single pass transpilation passes can be safely executed with the code validation and advanced stack/register handling can be applied with the stack height validations.

But I don’t see that the invariants given in the “Properties of validated code” section actually prove that.  I’m also not sure what the one-pass algorithms is for traversing EVM code.  It should be simpler than the validation algorithm, but looks to be not so simple as the standard depth-first search of directed cyclic graphs.


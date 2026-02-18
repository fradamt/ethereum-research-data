---
source: magicians
topic_id: 21927
title: "EIP-7830: Contract size limit increase for EOF"
author: axic
date: "2024-12-02"
category: EIPs > EIPs core
tags: [evm, eof]
url: https://ethereum-magicians.org/t/eip-7830-contract-size-limit-increase-for-eof/21927
views: 357
likes: 10
posts_count: 21
---

# EIP-7830: Contract size limit increase for EOF

Discussion topic for [EIP-7830](https://eips.ethereum.org/EIPS/eip-7830).

#### Update Log

- 2024-11-29: initial draft Add EIP: Contract size limit increase for EOF by axic · Pull Request #9074 · ethereum/EIPs · GitHub

#### External Reviews

None as of 2024-11-29.

#### Outstanding Issues

None as of 2024-11-29.

## Replies

**axic** (2024-12-02):

Prior relevant discussion topics:

- Contract code size remove fixed limit · Issue #659 · ethereum/EIPs · GitHub
- Removing Contract Size Limit · Issue #1662 · ethereum/EIPs · GitHub
- Removing or Increasing the Contract Size Limit
- EIP-5027: Unlimit contract code size
- Increasing contract size limit with increasing gas cost beyond 24.5Kb

---

**shemnon** (2025-01-25):

Spreadsheet calculating costs to deploy.



      [docs.google.com](https://docs.google.com/spreadsheets/d/1C2dd5sVnZNKXOpRknHhxt6MnTTN50c3b9d6ZU2rvqDQ/edit?gid=0#gid=0)



    https://docs.google.com/spreadsheets/d/1C2dd5sVnZNKXOpRknHhxt6MnTTN50c3b9d6ZU2rvqDQ/edit?gid=0#gid=0

###

This Sheet is private










summary:

24KiB today - ~ 5.4MGas

64KiB under EIP-7623 - ~ 15.8M gas

Largest contract in 30MB - ~ 121.9 KiB

Largest contract in 36MB - ~ 146.9 KiB

---

**frangio** (2025-02-05):

> JUMPDEST-analysis is required for legacy contracts, and many of the algorithms performing it are not linear and/or have unknown unknowns

I have seen this claim that JUMPDEST analysis is non-linear but can someone explain why it would be?

The code below appears to implement this and it is linear.



      [github.com](https://github.com/bluealloy/revm/blob/v55/crates/interpreter/src/interpreter/analysis.rs#L39-L66)





####



```rs


1. /// Analyze bytecode to build a jump map.
2. fn analyze(code: &[u8]) -> JumpTable {
3. let mut jumps: BitVec = bitvec![u8, Lsb0; 0; code.len()];
4.
5. let range = code.as_ptr_range();
6. let start = range.start;
7. let mut iterator = start;
8. let end = range.end;
9. while iterator < end {
10. let opcode = unsafe { *iterator };
11. if opcode::JUMPDEST == opcode {
12. // SAFETY: jumps are max length of the code
13. unsafe { jumps.set_unchecked(iterator.offset_from(start) as usize, true) }
14. iterator = unsafe { iterator.offset(1) };
15. } else {
16. let push_offset = opcode.wrapping_sub(opcode::PUSH1);
17. if push_offset < 32 {
18. // SAFETY: iterator access range is checked in the while loop
19. iterator = unsafe { iterator.offset((push_offset + 2) as isize) };
20. } else {


```

  This file has been truncated. [show original](https://github.com/bluealloy/revm/blob/v55/crates/interpreter/src/interpreter/analysis.rs#L39-L66)

---

**shemnon** (2025-02-05):

From a strict algorithm analysis perspective it is O(n), but there are in essence multiple linear aspects with different “constants” that the interaction varies so much based on the content it appears non-linear because we are magnifying one of the linear cases to a level not seen in typical organic use.

Typical contracts are full of non-jumpdest/non-push targets.  The best attack contracts were exclusively jumpdest, exclusively push, or a deep mix of both jumpdest and push of various sizes.  There was not a single algorithm that didn’t exhibit a large computational cost jump between all jumps and all jumpdests (algos boil down to you either mark safe or unsafe jumps, and the cost was in the marking).  So a good attack vector was all jumpdest/push1 where the immediate is jumpdest. This particular algorithm cited is weak against the all jumpdest case, but excels in the all push(jumpdest) case.

Since we now charge a nominal gas per-32-bytes for CREATE[2] now this scenario puts the worst attack scenario for each client in line with the GPS (gas per second) of other operations, and is no longer a better denial-of-service vector than “SHA3 lots of data,” which has been one point to anchor GPS against.  Without that cost executing CREATEs in a tight loop with a good attack contract significantly degrades GPS to an unacceptable level.

---

**frangio** (2025-02-06):

Thanks, I think I understand the situation now. I think a summary could be useful for others:

- A JUMP instruction can only be executed if the target is a JUMPDEST. To know if that is the case requires analyzing all of the code up to the target. This is necessary to recognize PUSH instructions and skip over their immediates, which could otherwise be confused for JUMPDESTs.
- This is called JUMPDEST analysis.
- Originally this analysis was not directly reflected in gas metering. Specifically, a CREATE instruction could trigger the analysis all of its init code for a gas cost independent of init code size. The init code has to be generated dynamically and repeatedly reused for the worst effect.
- This was fixed in EIP-3860 in Shanghai (2023).
- Asymptotically the cost of this analysis is linear in the code size. However, in concrete terms there can be a significant difference between the worst, best, and average cases.
- Resource pricing and limits have to consider the worst case, as this is what an attack would abuse. As a result, the average case is unfairly penalized with higher costs and/or lower limits.
- EOF improves the situation further by making it impossible to generate code dynamically, allowing analysis to be done once at deploy time and never at run time, eliminating the above worst case attack vector, and enabling an increase of code size limit.

---

**xrchz** (2025-02-16):

I haven’t caught up on all the discussion but something about this seems really off to me. We’re talking about the costs incurred by execution clients, right? And the concern is that a linear pass through all contract code (to compute a pc to instruction map) before message calling a contract – a map whose computation can be cached by the way – is too expensive? This is surprising to me, so I want to check it before getting more into the details of performance trade-offs strictly below the regime of “a linear pass is ok”.

---

**shemnon** (2025-02-19):

It’s also about when the pass occurs.  For EOF it occurs at contract creation, and at no other time, and all metadata needed for execution is encoded in the container.

For legacy the jumpdests are metadata derived from the code, a list of which jumpdests are valid and which are not. Clients need do generate this meatata prior to execution. Naïve implementations will check as part of the CALL, most clients cache once calculated.  Clients could persist this cache but I am not aware of any that do.  Initcode is particularly tricky because there is a very high likelyhood it will never be executed again.

So while the cost is linear with size the attack modes are impactful. Clients would need to commit to disk caching jumpdest analysis to remain on the safe side.

---

**xrchz** (2025-02-28):

So clients can easily handle non-EOF here by doing that caching as you said. I think this removes the argument here that EOF is needed for increasing the code size limit.

My impression so far although I’m not entirely up to date is that almost every pro-EOF argument I see has some similarly weak justification. I am concerned about having to implement EOF (I’m maintaining a formal EVM spec) when there isn’t actually a good reason for it.

---

**shemnon** (2025-02-28):

One thing to note is that clients caching the jumptables is something the protocol does not require, whereas EOF validation is something the protocol requires.

Which EVM spec are you maintaining?  You will need to add a new section about container validation, but the remainder of the changes are mostly tweaks on existing opcodes to support the design goals of things such as removing dynamic jumps, making stronger guarantees about the operand stack, removing code introspection and removing gas introspection.

---

**frangio** (2025-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xrchz/48/12202_2.png) xrchz:

> So clients can easily handle non-EOF here by doing that caching as you said.

The attacks use CREATE, the bytecode can be generated on the fly, there is no caching that can be done, at best heuristics. The chain needs to protect against worst case scenario so the parameters (size limit) are tuned for that. I don’t see how caching mitigates that attack.

As far as I can tell, pricing JUMPDEST analysis on CREATE more accurately is the only real mitigation.

---

**xrchz** (2025-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Which EVM spec are you maintaining?

[Verifereum](https://verifereum.org), a formal EVM spec in higher-order logic.

Since we can’t actually get rid of legacy code, the spec (and all the clients for that matter) needs to implement all the things EOF is removing anyway, and then additionally implement all the EOF checks etc. It just doesn’t improve things as far as I can tell the way it would if we were actually making breaking changes. But a blockchain is not a good place to make breaking changes - better to build better tooling around the existing EVM in my opinion.

---

**xrchz** (2025-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> As far as I can tell, pricing JUMPDEST analysis on CREATE more accurately is the only real mitigation.

OK this might be true (I haven’t independently analysed whether this attack is a serious threat, but I am happy to assume it is for now), in which case I would support repricing as the way to address it.

---

**charles-cooper** (2025-03-01):

I’m not sure I understand this. It’s still just a single pass to compute the locations of all the jumpdests in a contract, no?

---

**charles-cooper** (2025-03-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> There was not a single algorithm that didn’t exhibit a large computational cost jump between all jumps and all jumpdests (algos boil down to you either mark safe or unsafe jumps, and the cost was in the marking).

Are these results actually recorded anywhere? The algorithm looks single pass. Just iterate over all the bytes in the bytecode, skip PUSH opcodes and mark jumpdests.

If the question is how big of an array you need to store all the jumpdests, this is just a matter of pricing. And it seems that it’s already paid for by the initcode cost of 2 gas per 32 bytes anyways. (If the argument is that this cost is too low, maybe with some execution resource usage numbers, we could raise it to 3 gas per 32 bytes or something).

---

**frangio** (2025-03-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> There was not a single algorithm that didn’t exhibit a large computational cost jump between all jumps and all jumpdests (algos boil down to you either mark safe or unsafe jumps, and the cost was in the marking).

If there was an algorithm where the cost was independent of the code bieng analyzed, does this change anything?

---

**charles-cooper** (2025-03-13):

I’ve performed benchmarks of JUMPDEST analysis. The results are fairly similar for both PUSH1-heavy and JUMPDEST-heavy bytecodes. The benchmarks show a strong linear correlation between analysis time and bytecode size.



      [github.com](https://github.com/charles-cooper/eip-3860-benchmarks/blob/master/benchmark_results/summary_report.md)





####



```md
# JUMPDEST Analysis Benchmark Report

## Summary

- **Date:** 2025-03-13 12:49:11
- **Number of tests:** 24
- **Bytecode size range:** 128 bytes to 15.00 MB

### Key Findings

- Maximum analysis time for JUMPDEST-only bytecode: 22.86 ms
- Maximum analysis time for PUSH1 0x5b sequences: 19.85 ms
- Performance ratio (15MB / 48KB) for JUMPDEST-only: 326.61x
- Performance ratio (15MB / 48KB) for PUSH1 sequences: 287.72x
- Normalized time for largest JUMPDEST-only bytecode: 1.488 us/KB
- Normalized time for largest PUSH1 sequences: 1.293 us/KB

## Detailed Results

### JUMPDEST-only Bytecode
```

  This file has been truncated. [show original](https://github.com/charles-cooper/eip-3860-benchmarks/blob/master/benchmark_results/summary_report.md)










The max cost is ~46.5ns per word (on a 5-year old laptop), which is arguably a bit high (and like I said, could be addressed by the gas schedule), but I didn’t spend any time optimizing the code, I just wanted to demonstrate linearity.

---

**charles-cooper** (2025-03-15):

btw there is a nice png in there too for those who don’t have the time to click into the repo:

[![image](https://ethereum-magicians.org/uploads/default/original/2X/7/717f13f4d38c2c55468c405808bd3f09b6a8c275.png)image1200×800 73.1 KB](https://ethereum-magicians.org/uploads/default/717f13f4d38c2c55468c405808bd3f09b6a8c275)

---

**wjmelements** (2025-03-26):

[Draft EIP](https://github.com/ethereum/EIPs/pull/9548) to simply remove the jumpdest analysis

---

**shemnon** (2025-03-26):

Where’s the discussion top in “remove jumpdest analysis?” Several of my Ipsilon teammates think it would be dangerous and reckless, but I don’t want to derail this EIP’s discussion.

---

**wjmelements** (2025-03-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png)

      [EIP-7921: Skip `JUMPDEST` immediate argument check](https://ethereum-magicians.org/t/eip-7921-skip-jumpdest-immediate-argument-check/23279) [EIPs core](/c/eips/eips-core/35)




> –
> Discussion topic for EIP-7921
> Update Log
>
> initial draft PR


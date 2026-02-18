---
source: magicians
topic_id: 20806
title: EIP-7756 EOF/EVM Trace Specification
author: shemnon
date: "2024-08-15"
category: EIPs > EIPs interfaces
tags: []
url: https://ethereum-magicians.org/t/eip-7756-eof-evm-trace-specification/20806
views: 195
likes: 6
posts_count: 13
---

# EIP-7756 EOF/EVM Trace Specification

Discussion topic for [EIP-7756](https://eips.ethereum.org/EIPS/eip-7756)

#### Update Log

- 2024-08-14: initial draft PR

#### External Reviews

None as of 2024-08-14.

#### Outstanding Issues

 2024-08-14: member name for CALLF retrun stack - `fdepth` or something else?

## Replies

**shemnon** (2024-08-15):

There are a small number of additions to [EIp-3155](https://eips.ethereum.org/EIPS/eip-3155), other than that it is the same as the older trace spec.

- The immediate member was added to support the large number of instructions that contain immediate operations.
Without this change, users would need bytes of the contracts being executed to rationalize the traces.
- The section and fdepth members were added to support EIP-4750 EOF Functions.
- Added clarification around where pc indexes when run in an EOF container (start of section is PC=0).

---

**pdobacz** (2024-09-25):

First some minor comments:

- why returnData is not required anymore? also it’s inconsistent with the note below saying it can be left out when empty
- I would not omit functionDepth if it’s zero (only when legacy EVM), to be consistent with section
- for RJUMPV I would enforce the entire table (and for PUSHx the entire value) in the immediate field, otherwise the immediate field would need to be likely left out of fuzzing etc., as it is expected that client implementations of tracing will diverge if given the chance. Also for pure consistency sake; otherwise someone looking at a trace with PUSH1 and without the immediate might be confused.

We should specify whether `stack` for EOF is for the entire message call or for the current code section (i.e. the latter would start with only `code_section.inputs` top items at the start of a code section execution). I have no preference on which option is better, but this should be specified. Also we should now describe `stack` as “operand stack” in the “Explanation”.

A general remark I’d like to make is that while this improves trace-fuzzing for EOF, it should not be seen as a blocker. I suppose 90% of EVM/EOF runtime features will still be successfully fuzzed with the original 3155 traces. Even if there’s any inconsistencies in tracing fields like `pc`, that can be rather safely left out until made consistent.

Two last comments reflecting more on EIP-3155, so I guess by now it’s way too late to change. But I’m interested anyway in the rationale of the decisions made in EIP-3155

- I never understood why we use Hex-Number for things like gas. I understand we cannot use a JSON-number (too large values), but why not a Dec-Number string? In all spec I can think of gas is formatted in decimal
- OTOH, I would prefer op to be Hex-Number, this is how those are usually formatted.

---

**shemnon** (2024-10-10):

For the 3155 traces to be usefule in EOF we either need to add code section or have PC be indexed from a common point (container start, or code section start).

The mandatory GoEVMLAB fields appear to be

- Depth (message frame stack size)
- PC
- Gas Remaining
- Operation (number only, as name differences look to be ignored)
- stack (only top 6 items)
- error

Optional is

- gasCost (different clients have different interpretations)
- memory size (nethermind has quirks about when it is measured)
- refunds (nethermind doesn’t provide it)
- returnData (nethermind doesn’t provide it)

---

**shemnon** (2024-12-07):

I updated the spec with the following changes that will land as soon as eth-bot merges:

- change gas, gasCost, gasUsed to Number
- change opcod to Hex-Number
- Allow Numbers and Hex-Numbers to be used interchangeably.
- remove required column in favor of multiple sections
- editing cleanup

This doesn’t address all he issues above, but gets the essential ones that I feel improve the spec.

I consider the other issues open, and will review them prior to last call (when EOF ships).  However these were important to get the Fuzzing working IMHO.

---

**acolytec3** (2025-04-04):

I am working on implementing this spec for ethereumjs and have a question on the `error` field in the trace.  Why is this a hex-string and just a plain string (to allow for providing a revert reason)?  If hex-strings are necessary, is there a list of valid error strings we should use somewhere?

---

**shemnon** (2025-04-04):

The error is the raw bytes that are returned from a REVERT, or a regular string expressing the exceptional halt.  Modern solidity tends to put an ABI encoded object in their reverts (see [the docs](https://docs.soliditylang.org/en/v0.8.29/control-structures.html#revert-statement)) so a raw string represenation could be problematic JSON-encoding wise.

The error field is not used as part of goevmlab’s differential test executor, so lack of strict adherence for this field will not cause fuzzing issues.

---

**acolytec3** (2025-04-07):

For the `functionDepth` field, how should we deal with the scenario where we’re in the first code section executing bytecode? It seems like `functionDepth` would be 0 since we haven’t yet executed a CALLF opcode yet and therefore can’t have moved into an eof function.

The EIP says of optional fields, `If a field is to be omitted within a trace, it MUST always be omitted within the same trace` for optional fields but it also says that `functionDepth` starts at 1.

So, not sure if this implies I should define `functionDepth` as 1 initially or if there is an inconsistency here and we should report functionDepth 0 if we’re not inside a call frame generated by CALLF?

---

**shemnon** (2025-04-07):

Treating `functionDepth` like `depth` - which corresponds to call depth.  The first level call is `"depth"=1` so the first function is also one.

functionDepth also serves as an indicator that the code being executed is in an EOF container.  So functionDepth should not be present in lines where the code is not in an EOF container.

The spec should be clear for this being a line that is sometimes present and sometimes not.

> functionDepth MUST NOT be present for trace lines of code not in an EOF container.

Although the prior line says it may be omitted for depth==1.  Should we delete it so it’s always present?  That is how other clients in fuzzing are currently doing it.

---

**acolytec3** (2025-04-07):

I missed that second bullet but it is clear now that you point it out.

> Although the prior line says it may be omitted for depth==1. Should we delete it so it’s always present? That is how other clients in fuzzing are currently doing it.

My current draft implementation will always provide it in the context of EOF and it does seem like a useful marker for testing/logging/etc to have it always be present when in an EOF container since we don’t have another explicit way of marking the execution context as EOF or legacy in the trace and I can see it being very useful for evaluating a trace to have that context clearly defined.

---

**acolytec3** (2025-04-23):

Can I get some clarity on what’s expected in the `storage` array?  The way I read it now it’s an array of tuples of “key-values”.  Does that just mean an array of tuples storage slots and their values?  Seems like we would want something like

`[ [address1, [[slot0, value0], [slot1, value1]...]], [address2, [slot0, value0]...]] ]`

---

**shemnon** (2025-04-23):

Underspecified, I brought it over from 3155.  It feels like it should be `"storage":{"0x010000", {"0x1": "0xff", "0x2": "0xce"}}`, with a rough type (made up notation) of `Map<Account, Map<Slot, Value>>`.  It would be all “warm” storage.

However, fuzzing doesn’t use it and I’m not aware of any clients who have implemented it.  Would you mind if it was deleted?

---

**acolytec3** (2025-04-23):

I only implemented it because it was in the spec and we have no specific use case for it at present.  If it’s not useful, we can just remove that code.


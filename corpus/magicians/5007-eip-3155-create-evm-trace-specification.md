---
source: magicians
topic_id: 5007
title: "EIP-3155: Create EVM Trace Specification"
author: MariusVanDerWijden
date: "2020-12-07"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-3155-create-evm-trace-specification/5007
views: 4169
likes: 25
posts_count: 21
---

# EIP-3155: Create EVM Trace Specification

Discussion for EIP-3155 which can be found here: https://github.com/ethereum/EIPs/pull/3155

It tries to formalize the de-facto standard for tracing during state tests and move it to a more visible place s.th. it will be picked up by more implementations

## Replies

**shemnon** (2020-12-07):

I added some in-line comments in the EIP.  Generally summarized as

- The CUT should not be part of the EIP, the standard is useful outside of just fuzz testing (the rpc debug_standardTraceBadBlocks for example)
- field types need to be specified (what’s a hex string and what’s a json number, and unit for time, for example)
- de-facto standard -> common format.  I think Parity’s trace is more of a de-facto standard as we have many users asking for it.  Mostly because of the internal transaction and state handling.

---

**MariusVanDerWijden** (2020-12-07):

Thank you very much for the comments! They are very helpful, I will insert them tomorrow.

Sorry about the misnomer of the common format, didn’t want to step on anyones toes with that.

---

**gumb0** (2020-12-15):

Some nitpicks:

- Hex-String data type perhaps could be better described as “hex-encoded byte array”.
- It’s not clear what exactly returnStack is, please provide an example where it’s not empty.
- Please provide an example where error is not empty.
- > Clients SHOULD output the fields in the same order as listed in this EIP.

According to the [JSON spec](https://www.json.org/json-en.html) “an object is an **unordered** set of name/value pairs”, so strictly speaking this requires something not supported by JSON.

- > The CUT MUST NOT output a line for the STOP operation if an error occurred: Example:

The example following this does in fact output `STOP` operation, so it’s contradictory, or an example for something else.

-

> ```auto
> {"stateRoot":"0xd4c577737f5d20207d338c360c42d3af78de54812720e3339f7b27293ef195b7","output":"","gasUsed":"0x3","successful":"true","time":141485}
> ```

This example of a summary contains `successful` field not mentioned in the spec.

---

**chfast** (2021-01-21):

My experience is limited to some knowledge about tracing implementations inside EVMs  and using tracing for debugging convoluted state tests.

The most confusing part of the current tracing is that it reports a kind of “in progress” state of an instruction execution if you consider precondition-checking a part of the execution. I.e. it reports the gas cost of the instruction (hopefully total gas cost but that was not the case in Aleth; does it also report total `CREATE` and `CALL` costs?) but not the execution result.

In one of my prototypes I changed that. The tracing there was reporting the state after instruction execution. This was in my opinion much more DevEx friendly.

Moreover, I also focused on limiting the amount data transferred from EVM. Together these provided additional nice options:

1. Instead of dumping whole EVM stack, you can always dump only the top item. It can be noticed that an instruction pushes at most one value to the stack so the “stack top dump” is also the instruction execution result.

```auto
{"opName":"PUSH1", "stackTop":"0x02"}
{"opName":"DUP1", "stackTop":"0x02"}
{"opName":"ADD", "stackTop":"0x04"}
```
2. Instead of full memory dump, you can only report the modifiedMemory: the memory area where the instruction has written to. It can be noticed that an instruction may at most modify single continuous memory area. This also can be seen as the instruction execution result. If you report the instruction before execution the “modified memory” has no meaning.

```auto
{"opName":"MSTORE", "modifiedMemoryOffset":"0x20", "modifiedMemory":"0x000000000000000000000000aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
```
3. It is enough to just report gasLeft after the execution. The instruction gas cost can be easily computed from the gasLeft of the previous instruction.
4. An error code can be meaningfully added to an instruction trace. Is this the meaning of the error field? However, this only make sense for the last instruction in a call as other instructions must be successful.

```auto
{"opName":"POP", "error":"stack underflow"}
```

Lastly, the “new” tracing should provide the same information as the “legacy” tracing. Therefore, the “legacy” tracing format can be emulated by a statefull wrapper. If that is not the case, consider this a bug.

Many of these options have variants and alternatives. At this moment I only want to present an overview. Let me know if this direction is something you would like to explore.

#### References

1. EVMC tracing prototype (and introducing PR) — never fully utilized by any EVM and finally removed from EVMC.
2. Aleth implementation of the EVMC tracing prototype.

---

**axic** (2021-01-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> In one of my prototypes I changed that. The tracing there was reporting the state after instruction execution. This was in my opinion much more DevEx friendly.

ethereumjs-vm reports I think both, because different use cases required the different versions. Maybe I remember it wrongly, and it was only discussed as an issue and one of the options was not merged. In any case I think getting input from both ethereumjs and the Remix team would be very valuable.

Ping [@yann300](/u/yann300) and [@jochem-brouwer](/u/jochem-brouwer) (I could not find any other ethereumjs dev here).

---

**holiman** (2021-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> Instead of dumping whole EVM stack, you can always dump only the top item.

I’d prefer the 5-6 topmost items. Then you don’t have to backtrack up to (potentially) infinity lines to see what the inputs to an op were.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> Instead of full memory dump, you can only report the modifiedMemory: the memory area where the instruction has written to.

Clever!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> It is enough to just report gasLeft after the execution

Not sure about that. In a call, the gasCost was the cost of the call. The gasLeft is what you have available in this new execution frame.

---

**holiman** (2021-01-22):

Although, in general, your comments makes a presumptive traceviewer (such as my `traceview`: https://github.com/holiman/goevmlab#traceview ) forced to be come more stateful. In order to provide a memory dump, it needs to iterate through *all* the ops leading up to the point in question, if we only ever provide snippets.

Same with stack, but I already mentioned that.

So yes, it’ll make the trace(s) smaller, but it’ll also increase the complexity at the parsing/analysis side a whole lot.

---

**jochem-brouwer** (2021-01-22):

Assuming that we mean by “EVM traces” the `step` event which the VM fires, then we only report the state of the VM **before** execution of an operation. We do not report the state right after running an operation. I think that [@chfast](/u/chfast) raises a very good point that there are essentially “two” events happening: the first is the state of the VM *before* the operation runs, and the other is the state *after* the operation runs.

A very notable situation where this is important is if you invoke any `CALL` operation. In the `stepBefore`, we have the gas available before we run the `CALL`. Then `afterStep`, we deduct the call gas. But, the `beforeStep` in our new environment (new address), not only will the operation be different which we evaluate, but also our gas could have changed (since we have the 63/64 max forwarded gas rule).

I think it would make sense to add both these events in cases where it makes sense (it does not make sense to use `beforeStep` and `afterStep` just for a `PUSH*` operation).

---

**chfast** (2021-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> chfast:
>
>
> Instead of dumping whole EVM stack, you can always dump only the top item.

I’d prefer the 5-6 topmost items. Then you don’t have to backtrack up to (potentially) infinity lines to see what the inputs to an op were.

Ok, for that we can dump the exact number of the stack items which will be consumed by the to-be-executed instruction.

Any idea how to resolved some of the alternatives to single specification?

---

**holiman** (2021-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> Ok, for that we can dump the exact number of the stack items which will be consumed by the to-be-executed instruction.

But wait, what if it’s an invalid instruction? Or, what if it’s something that does *not* consume, anything – we still want to be able to see what the last op pushed on the stack.

So I’d say display at minimum the top item on the stack, even if it consumes zero.

---

**chfast** (2021-05-18):

### New set of proposed changes

1. Wrap calls with “call start” and “call summary” entries. This will extend “tx summary” and allow easier internal call identification. With the change the “depth” can be moved to the “call start” - no need to repeat it on every instruction. Similarly “error” can be moved to “call summary”.
2. I’m not able to compute “gasCost” before execution without big additional effort because gas calculation is mixed with instruction execution. Can this field be optional?
3. I propose to change the type of “gas”, “gasUsed” and “gasCost” to Number. These values are at most 64-bit and even 52-bits are unlikely. Using Number is much easier to read.
4. I’m not able to compute “stateRoot”.

---

**chfast** (2021-05-19):

I have implemented the trimmed stack output with the rules that at most the instruction number of arguments in dumped but not less than 1. If trimming happens the additional `"..."` indicator is added.

```json
{"pc":380,"op":91,"opName":"JUMPDEST","gas":999330,"stack":["0x0","..."]}
{"pc":381,"op":147,"opName":"SWAP4","gas":999329,"stack":["0x0","0xa0","0x0","0x0","0x199","..."]}
{"pc":382,"op":146,"opName":"SWAP3","gas":999326,"stack":["0x199","0xa0","0x0","0x0","..."]}
{"pc":383,"op":80,"opName":"POP","gas":999323,"stack":["0x0","..."]}
{"pc":384,"op":80,"opName":"POP","gas":999321,"stack":["0xa0","..."]}
{"pc":385,"op":80,"opName":"POP","gas":999319,"stack":["0x0","..."]}
{"pc":386,"op":86,"opName":"JUMP","gas":999317,"stack":["0x199","..."]}
{"pc":409,"op":91,"opName":"JUMPDEST","gas":999309,"stack":["0x0","..."]}
{"pc":410,"op":133,"opName":"DUP6","gas":999308,"stack":["0x0","0x0","0x6745230100efcdab890098badcfe001032547600c3d2e1f0","0x40","0x0","0xa0","..."]}
{"pc":411,"op":82,"opName":"MSTORE","gas":999305,"stack":["0xa0","0x0","..."]}
{"pc":412,"op":97,"opName":"PUSH2","gas":999302,"stack":["0x0","..."]}
{"pc":415,"op":132,"opName":"DUP5","gas":999299,"stack":["0x1a9","0x0","0x6745230100efcdab890098badcfe001032547600c3d2e1f0","0x40","0x0","..."]}
{"pc":416,"op":96,"opName":"PUSH1","gas":999296,"stack":["0x0","..."]}
{"pc":418,"op":131,"opName":"DUP4","gas":999293,"stack":["0x20","0x0","0x1a9","0x0","..."]}
{"pc":419,"op":1,"opName":"ADD","gas":999290,"stack":["0x0","0x20","..."]}
{"pc":420,"op":137,"opName":"DUP10","gas":999287,"stack":["0x20","0x0","0x1a9","0x0","0x6745230100efcdab890098badcfe001032547600c3d2e1f0","0x40","0x0","0xa0","0x0","0xa0","..."]}
{"pc":421,"op":97,"opName":"PUSH2","gas":999284,"stack":["0xa0","..."]}
```

We can also add `"stackSize"` field.

```json
{"pc":380,"op":91,"opName":"JUMPDEST","gas":999330,"stack":["0x0","..."],"stackSize":14}
{"pc":381,"op":147,"opName":"SWAP4","gas":999329,"stack":["0x0","0xa0","0x0","0x0","0x199","..."],"stackSize":14}
{"pc":382,"op":146,"opName":"SWAP3","gas":999326,"stack":["0x199","0xa0","0x0","0x0","..."],"stackSize":14}
{"pc":383,"op":80,"opName":"POP","gas":999323,"stack":["0x0","..."],"stackSize":14}
{"pc":384,"op":80,"opName":"POP","gas":999321,"stack":["0xa0","..."],"stackSize":13}
{"pc":385,"op":80,"opName":"POP","gas":999319,"stack":["0x0","..."],"stackSize":12}
{"pc":386,"op":86,"opName":"JUMP","gas":999317,"stack":["0x199","..."],"stackSize":11}
{"pc":409,"op":91,"opName":"JUMPDEST","gas":999309,"stack":["0x0","..."],"stackSize":10}
{"pc":410,"op":133,"opName":"DUP6","gas":999308,"stack":["0x0","0x0","0x6745230100efcdab890098badcfe001032547600c3d2e1f0","0x40","0x0","0xa0","..."],"stackSize":10}
{"pc":411,"op":82,"opName":"MSTORE","gas":999305,"stack":["0xa0","0x0","..."],"stackSize":11}
{"pc":412,"op":97,"opName":"PUSH2","gas":999302,"stack":["0x0","..."],"stackSize":9}
{"pc":415,"op":132,"opName":"DUP5","gas":999299,"stack":["0x1a9","0x0","0x6745230100efcdab890098badcfe001032547600c3d2e1f0","0x40","0x0","..."],"stackSize":10}
{"pc":416,"op":96,"opName":"PUSH1","gas":999296,"stack":["0x0","..."],"stackSize":11}
{"pc":418,"op":131,"opName":"DUP4","gas":999293,"stack":["0x20","0x0","0x1a9","0x0","..."],"stackSize":12}
{"pc":419,"op":1,"opName":"ADD","gas":999290,"stack":["0x0","0x20","..."],"stackSize":13}
{"pc":420,"op":137,"opName":"DUP10","gas":999287,"stack":["0x20","0x0","0x1a9","0x0","0x6745230100efcdab890098badcfe001032547600c3d2e1f0","0x40","0x0","0xa0","0x0","0xa0","..."],"stackSize":12}
{"pc":421,"op":97,"opName":"PUSH2","gas":999284,"stack":["0xa0","..."],"stackSize":13}
```

The `"..."` seems to confuse `traceview`.

Besides, the trimming works nice for instructions like `DUP` or `SWAP`. For other instruction this seems to introduce some additional mess - it is difficult to track how values are “moved” on the stack when some variadic number of items is presented, especially for cases with single top value. The minimum presented number of values should be higher, maybe 3.

```json
{"pc":380,"op":91,"opName":"JUMPDEST","gas":999330,"stack":["0x0","0xa0","0x0","..."],"stackSize":14}
{"pc":381,"op":147,"opName":"SWAP4","gas":999329,"stack":["0x0","0xa0","0x0","0x0","0x199","..."],"stackSize":14}
{"pc":382,"op":146,"opName":"SWAP3","gas":999326,"stack":["0x199","0xa0","0x0","0x0","..."],"stackSize":14}
{"pc":383,"op":80,"opName":"POP","gas":999323,"stack":["0x0","0xa0","0x0","..."],"stackSize":14}
{"pc":384,"op":80,"opName":"POP","gas":999321,"stack":["0xa0","0x0","0x199","..."],"stackSize":13}
{"pc":385,"op":80,"opName":"POP","gas":999319,"stack":["0x0","0x199","0x0","..."],"stackSize":12}
{"pc":386,"op":86,"opName":"JUMP","gas":999317,"stack":["0x199","0x0","0x0","..."],"stackSize":11}
{"pc":409,"op":91,"opName":"JUMPDEST","gas":999309,"stack":["0x0","0x0","0x6745230100efcdab890098badcfe001032547600c3d2e1f0","..."],"stackSize":10}
{"pc":410,"op":133,"opName":"DUP6","gas":999308,"stack":["0x0","0x0","0x6745230100efcdab890098badcfe001032547600c3d2e1f0","0x40","0x0","0xa0","..."],"stackSize":10}
{"pc":411,"op":82,"opName":"MSTORE","gas":999305,"stack":["0xa0","0x0","0x0","..."],"stackSize":11}
{"pc":412,"op":97,"opName":"PUSH2","gas":999302,"stack":["0x0","0x6745230100efcdab890098badcfe001032547600c3d2e1f0","0x40","..."],"stackSize":9}
{"pc":415,"op":132,"opName":"DUP5","gas":999299,"stack":["0x1a9","0x0","0x6745230100efcdab890098badcfe001032547600c3d2e1f0","0x40","0x0","..."],"stackSize":10}
{"pc":416,"op":96,"opName":"PUSH1","gas":999296,"stack":["0x0","0x1a9","0x0","..."],"stackSize":11}
{"pc":418,"op":131,"opName":"DUP4","gas":999293,"stack":["0x20","0x0","0x1a9","0x0","..."],"stackSize":12}
{"pc":419,"op":1,"opName":"ADD","gas":999290,"stack":["0x0","0x20","0x0","..."],"stackSize":13}
{"pc":420,"op":137,"opName":"DUP10","gas":999287,"stack":["0x20","0x0","0x1a9","0x0","0x6745230100efcdab890098badcfe001032547600c3d2e1f0","0x40","0x0","0xa0","0x0","0xa0","..."],"stackSize":12}
{"pc":421,"op":97,"opName":"PUSH2","gas":999284,"stack":["0xa0","0x20","0x0","..."],"stackSize":13}
```

---

**chfast** (2021-05-21):

Initial implementation in evmone with comments to the spec and set of proposed changes.



      [github.com/ipsilon/evmone](https://github.com/ipsilon/evmone/pull/325)














####


      `master` ← `instruction_trace`




          opened 03:17PM - 14 May 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/a/a4e89da771022a19986c77423b928fa14258faf4.png)
            chfast](https://github.com/chfast)



          [+249
            -11](https://github.com/ipsilon/evmone/pull/325/files)







Implementation of EVM tracing following the [EIP-3155](https://eips.ethereum.org[…](https://github.com/ipsilon/evmone/pull/325)/EIPS/eip-3155) (draft). It outputs log line with JSON (jsonl) for every instruction to standard error output.

Differences from the spec:
1. All calls start with non-standard "start call" log:
   ```json
   {"kind":"call","static":false,"depth":0,"rev":"Berlin"}
   ```
2. All calls end with non-standard "end call" log as a replacement for single _summerical info_ at the end of transaction execution.
   ```json
   {"error":null,"gas":964766,"gasUsed":35234,"output":"da39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000"}
   ```
   - the `"stateRoot"` is omitted as there is no way to compute it,
   - the `"error"` is taken from the instruction trace log, replaces `"pass"` or `"successful"`.
3. The `"gasCost"` is omitted. This is difficult to compute as "dynamic" gas cost is calculated together with execution but the spec forces these to be separated.
4. The `"depth"` is omitted as already presented in "start call".
5. The `"returnData"` is not implemented. This is doable, but seems unnecessary because this is available in `"output"` in "end call".
6. The `"refund"` is omitted, currently not doable.
7. The `"memory"` was initially implemented, then removed because makes traces huge. It is recommended to enabled it with a flag. This is easy to implement in future.

Example (SHA1):
```json
{"kind":"call","static":false,"depth":0,"rev":"Berlin"}
{"pc":0,"op":96,"opName":"PUSH1","gas":1000000,"stack":[],"memorySize":0}
{"pc":2,"op":96,"opName":"PUSH1","gas":999997,"stack":["0x80"],"memorySize":0}
{"pc":4,"op":82,"opName":"MSTORE","gas":999994,"stack":["0x40","0x80"],"memorySize":0}
{"pc":5,"op":52,"opName":"CALLVALUE","gas":999982,"stack":[],"memorySize":96}
{"pc":6,"op":128,"opName":"DUP1","gas":999980,"stack":["0x0"],"memorySize":96}
{"pc":7,"op":21,"opName":"ISZERO","gas":999977,"stack":["0x0","0x0"],"memorySize":96}
{"pc":8,"op":97,"opName":"PUSH2","gas":999974,"stack":["0x1","0x0"],"memorySize":96}
{"pc":11,"op":87,"opName":"JUMPI","gas":999971,"stack":["0x10","0x1","0x0"],"memorySize":96}
{"pc":16,"op":91,"opName":"JUMPDEST","gas":999961,"stack":["0x0"],"memorySize":96}
{"pc":17,"op":80,"opName":"POP","gas":999960,"stack":["0x0"],"memorySize":96}

...

{"pc":1207,"op":23,"opName":"OR","gas":964862,"stack":["0xda39a3ee5e6b4b0d3255bfef0000000000000000","0x9560189000000000","0xafd80709","0xda39a3ee005e6b4b0d003255bfef009560189000afd80709","0x40","0x0","0xa0","0x0","0xa0","0xd6","0x1605782b"],"memorySize":512}
{"pc":1208,"op":23,"opName":"OR","gas":964859,"stack":["0xda39a3ee5e6b4b0d3255bfef9560189000000000","0xafd80709","0xda39a3ee005e6b4b0d003255bfef009560189000afd80709","0x40","0x0","0xa0","0x0","0xa0","0xd6","0x1605782b"],"memorySize":512}
{"pc":1209,"op":96,"opName":"PUSH1","gas":964856,"stack":["0xda39a3ee5e6b4b0d3255bfef95601890afd80709","0xda39a3ee005e6b4b0d003255bfef009560189000afd80709","0x40","0x0","0xa0","0x0","0xa0","0xd6","0x1605782b"],"memorySize":512}
{"pc":1211,"op":27,"opName":"SHL","gas":964853,"stack":["0x60","0xda39a3ee5e6b4b0d3255bfef95601890afd80709","0xda39a3ee005e6b4b0d003255bfef009560189000afd80709","0x40","0x0","0xa0","0x0","0xa0","0xd6","0x1605782b"],"memorySize":512}
{"pc":1212,"op":148,"opName":"SWAP5","gas":964850,"stack":["0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0xda39a3ee005e6b4b0d003255bfef009560189000afd80709","0x40","0x0","0xa0","0x0","0xa0","0xd6","0x1605782b"],"memorySize":512}
{"pc":1213,"op":80,"opName":"POP","gas":964847,"stack":["0x0","0xda39a3ee005e6b4b0d003255bfef009560189000afd80709","0x40","0x0","0xa0","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0xa0","0xd6","0x1605782b"],"memorySize":512}
{"pc":1214,"op":80,"opName":"POP","gas":964845,"stack":["0xda39a3ee005e6b4b0d003255bfef009560189000afd80709","0x40","0x0","0xa0","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0xa0","0xd6","0x1605782b"],"memorySize":512}
{"pc":1215,"op":80,"opName":"POP","gas":964843,"stack":["0x40","0x0","0xa0","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0xa0","0xd6","0x1605782b"],"memorySize":512}
{"pc":1216,"op":80,"opName":"POP","gas":964841,"stack":["0x0","0xa0","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0xa0","0xd6","0x1605782b"],"memorySize":512}
{"pc":1217,"op":80,"opName":"POP","gas":964839,"stack":["0xa0","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0xa0","0xd6","0x1605782b"],"memorySize":512}
{"pc":1218,"op":145,"opName":"SWAP2","gas":964837,"stack":["0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0xa0","0xd6","0x1605782b"],"memorySize":512}
{"pc":1219,"op":144,"opName":"SWAP1","gas":964834,"stack":["0xd6","0xa0","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x1605782b"],"memorySize":512}
{"pc":1220,"op":80,"opName":"POP","gas":964831,"stack":["0xa0","0xd6","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x1605782b"],"memorySize":512}
{"pc":1221,"op":86,"opName":"JUMP","gas":964829,"stack":["0xd6","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x1605782b"],"memorySize":512}
{"pc":214,"op":91,"opName":"JUMPDEST","gas":964821,"stack":["0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x1605782b"],"memorySize":512}
{"pc":215,"op":96,"opName":"PUSH1","gas":964820,"stack":["0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x1605782b"],"memorySize":512}
{"pc":217,"op":128,"opName":"DUP1","gas":964817,"stack":["0x40","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x1605782b"],"memorySize":512}
{"pc":218,"op":81,"opName":"MLOAD","gas":964814,"stack":["0x40","0x40","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x1605782b"],"memorySize":512}
{"pc":219,"op":107,"opName":"PUSH12","gas":964811,"stack":["0xa0","0x40","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x1605782b"],"memorySize":512}
{"pc":232,"op":25,"opName":"NOT","gas":964808,"stack":["0xffffffffffffffffffffffff","0xa0","0x40","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x1605782b"],"memorySize":512}
{"pc":233,"op":144,"opName":"SWAP1","gas":964805,"stack":["0xffffffffffffffffffffffffffffffffffffffff000000000000000000000000","0xa0","0x40","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x1605782b"],"memorySize":512}
{"pc":234,"op":146,"opName":"SWAP3","gas":964802,"stack":["0xa0","0xffffffffffffffffffffffffffffffffffffffff000000000000000000000000","0x40","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x1605782b"],"memorySize":512}
{"pc":235,"op":22,"opName":"AND","gas":964799,"stack":["0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0xffffffffffffffffffffffffffffffffffffffff000000000000000000000000","0x40","0xa0","0x1605782b"],"memorySize":512}
{"pc":236,"op":130,"opName":"DUP3","gas":964796,"stack":["0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x40","0xa0","0x1605782b"],"memorySize":512}
{"pc":237,"op":82,"opName":"MSTORE","gas":964793,"stack":["0xa0","0xda39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000","0x40","0xa0","0x1605782b"],"memorySize":512}
{"pc":238,"op":81,"opName":"MLOAD","gas":964790,"stack":["0x40","0xa0","0x1605782b"],"memorySize":512}
{"pc":239,"op":144,"opName":"SWAP1","gas":964787,"stack":["0xa0","0xa0","0x1605782b"],"memorySize":512}
{"pc":240,"op":129,"opName":"DUP2","gas":964784,"stack":["0xa0","0xa0","0x1605782b"],"memorySize":512}
{"pc":241,"op":144,"opName":"SWAP1","gas":964781,"stack":["0xa0","0xa0","0xa0","0x1605782b"],"memorySize":512}
{"pc":242,"op":3,"opName":"SUB","gas":964778,"stack":["0xa0","0xa0","0xa0","0x1605782b"],"memorySize":512}
{"pc":243,"op":96,"opName":"PUSH1","gas":964775,"stack":["0x0","0xa0","0x1605782b"],"memorySize":512}
{"pc":245,"op":1,"opName":"ADD","gas":964772,"stack":["0x20","0x0","0xa0","0x1605782b"],"memorySize":512}
{"pc":246,"op":144,"opName":"SWAP1","gas":964769,"stack":["0x20","0xa0","0x1605782b"],"memorySize":512}
{"pc":247,"op":243,"opName":"RETURN","gas":964766,"stack":["0xa0","0x20","0x1605782b"],"memorySize":512}
{"error":null,"gas":964766,"gasUsed":35234,"output":"da39a3ee5e6b4b0d3255bfef95601890afd80709000000000000000000000000"}
```

[sha1.txt](https://github.com/ethereum/evmone/files/6524230/sha1.txt)

---

**jochem-brouwer** (2021-07-19):

Hi there, some points which are not mentioned in the EIP, which I want to note based upon the current [Geth implementation](https://github.com/ethereum/go-ethereum/blob/f05419f0fb8c5328dca92ea9fb184d082300344a/core/vm/interpreter.go#L256).

They are either not mentioned, or they are not consistent, so I have some suggestions. But before opening a PR to the EIP to fix these, I’d rather discuss them first.

1. If current gas limit is less than the base fee of an opcode, or the memory expansion overflows, then the reported gas is the base fee (is the base fee of each operation defined unambiguously?). Note the defer function which handles these errors.
2. If an invalid opcode is reached, the previous gas cost is reported. (cost variable is not updated)
3. If any calculation of the dynamic gas part of an opcode runs into an error (stack underflow, out of gas, etc.) then the dynamic gas part will return 0, and thus the reported gas for that step is still the base fee.
4. For *CALL* opcodes, the gas cost is the dynamic gas cost + base fee of the call, but this is added to the gas sent to the next call frame (so the calculated gas limit of the call)
5. However, for CREATE* opcodes, the gas supplied to the next frame is not added to the base fee + dynamic cost of the operation.

**Discussion**

1. Should be added to the EIP
2. This is inconsistent. Since invalid operations consume all gas, the cost of this operation is thus the current gas left.
3. I am not sure here, since these errors consume all gas, is this inconsistent? I think it would make more sense to also report “consume all gas” here as cost, instead of just reporting the base fee.
4. This should be added to the EIP. This makes sense; this gas is sent to the next call frame and could thus all be consumed. At this point it is unknown how much it will cost in the end, but at this point we don’t care.
5. This is not very consistent with (4), I’d say this should also report the gas limit that is sent to the next frame (so 63/64 of current gas left in almost all forks, or the 100% of the gas limit in historical forks)

---

**sbacha** (2023-03-24):

Apologies if this EIP is finalized (it says stagnant in the repo) but I was wondering if this spec could possibly add an optional field for “counter factual” trace responses or if that deserves a separate EIP. Thanks ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

---

**SamWilsn** (2023-09-20):

Some discussion relevant to this EIP is happening on the execution-specs: [Implement Evm Trace by gurukamath · Pull Request #828 · ethereum/execution-specs · GitHub](https://github.com/ethereum/execution-specs/pull/828#issuecomment-1725298099)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gurukamath/48/5848_2.png) gurukamath:

> We are aware that in some cases where the opcode runs out of gas, geth and specs might emit different gas costs. In almost all such cases, I have found that geth emits only the static part of the gas cost. See this geth issue for more details.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gurukamath/48/5848_2.png) gurukamath:

> Geth figures out that the opcode is going to run out of gas due to large init code. For efficiency reasons, it then does not even bother to calculate the dynamic gas because it makes no difference. So it just emits the static part in the trace.
>
>
> The specs on the other hand calculate all the components of the gas (static + dynamic) and emits that in the trace. I am not sure if there is a standard behaviour that is agreed upon in this case. At least, I couldn’t find anything in EIP-3155. For greater context on such issues you can follow the issue on the geth repo that linked earlier. See here

---

**SamWilsn** (2024-08-22):

Would you all consider adding a [JSON Schema](https://json-schema.org/) into the proposal? I usually recommend it for proposals using JSON because it helps avoid ambiguity and makes automated testing a bit easier.

---

**acolytec3** (2025-04-03):

I’m quite late to this party since it seems last call deadline was about a month ago, but is there any more thought on addressing some of the issues cited by [@jochem-brouwer](/u/jochem-brouwer) here?  We’re finalizing our implementation in `@ethereumjs/evm` and would like to confirm we have a finalized spec to work with.  In comparing the traces produced by our implementation versus geth, I still see discrepancies (mostly related to the CALL/DELEGATECALL gas computations), but geth also doesn’t provide several fields listed as required so just trying to determine how we should approach some of these variations.

---

**shemnon** (2025-04-03):

Can we move these requests into the [EIP-7756: EOF/EVM Trace Specification](https://eips.ethereum.org/EIPS/eip-7756) discussion [here](https://ethereum-magicians.org/t/eip-7756-eof-evm-trace-specification/20806)? 3155 will not be seeing any significant re-work, and 7756 will be the trace specification when EOF lands.  7756 is not in last call and open to change.

---

**shemnon** (2025-04-04):

Could you elaborate on what a ‘"counter factual” trace responses’ would be?  Would `eth_simulate` satisfy this?  (look in the recurring calls, they occurs every week on Mondays)


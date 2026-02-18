---
source: ethresearch
topic_id: 6387
title: On-chain gated computing by patching the control flow of arbitrary smart contracts
author: pinkiebell
date: "2019-10-29"
category: Layer 2
tags: []
url: https://ethresear.ch/t/on-chain-gated-computing-by-patching-the-control-flow-of-arbitrary-smart-contracts/6387
views: 2194
likes: 5
posts_count: 10
---

# On-chain gated computing by patching the control flow of arbitrary smart contracts

# On-chain gated computing by patching the control flow of arbitrary smart contracts

## The problem

Imagine the problem space layer-2 solutions have to face.

For example: to make it possible to run arbitrary smart contracts on layer-2 and allowing

the computation and outcome of these contracts to be verifiable on the root-chain;

ideally in a permissionless way and without any sort of ‘special’ authorities or governance protocols.

Solutions we have right now for this are systems like solEVM-enfocer or any truebit like verification game,

but they come with it’s own problems, the biggest one being the time it takes to decide on `disputes` -

intending to resolve computation in a on-chain verification game protocol.

This cripples layer-2 solutions because it becomes easy to block/delay finalization of side-chain Blocks on

the root-chain Plasma-style bridge contract. The only reason for this is the big complexity and therefore `time`

it takes to resolve a dispute.

## Theory for a potentially better system

If we think about executing contracts that are easily exceeding the root-chain block gas limit,

one possible solution is to write the contracts in a `resumable` way - to gain the ability to execute

a programm in a chunkable way. But this is a complex task and does not scale in practice for every contract.

Let’s assume a general chunkable/gated computing model:

- Stop the execution at any point in (the EVM run-)time,
- Checkpoint the execution environment (stack, memory, etc).
- Save it somewhere and resume the execution at a later time.

Like the suspend-to-ram or deep sleep mode of your favourite computing machine.

Analogy:

The flow of a river that we can suspend or resume depending on a condition.

- Gated

### Layer-2 Example

A potential layer-2 solution could use that in the following way:

- Allowing users to submit the solution/outcome of executing a block.
We assume good faith and provide incentives that submitting the correct solution (a solution no-one challenges because it is correct)
provides the solver or potential challengers with positive or negative financial outcomes.
- Having the ability that any honest user can challenge a solution by invoking the execution of that block
on the root-chain in one or more transactions until the execution is resolved/done.

TL;DR

We assume at least one honest user always challenges incorrect solutions buy executing the compution in one or more transactions and

gaining the bond from the solver after the execution was executed on-chain.

## How - Patching arbitray smart contracts to own the control flow

With the above in mind, the layer-2 root-chain `Bridge`-contract that manages the state of the side-chain

can analize and patch arbitray smart contracts to ‘hijack’ the control flow of the program and therefore

provide a controlled and verifiable way to execute a `transaction` in chunks by deploying a patched version

of a smart contract with checkpoints and functionality like intercepting calls to other contracts inside that

arbitrary contract to provide custom functionality or state checks.

That `checkpointing function` or let’s name it a `retpoline` - a term VM & Kernel developers are propably aware of.

In a nutshell, we patch the bytecode by adding and/or changing control flow instructions like `JUMP`

and therefore gaining the ability for code execution inside a (potentially untrusted) EVM context.

In this case, the retpoline is Bridge-controlled code that watches for gas usage to know when to stop execution and

overriding instructions like `CALL` to provide chain-specific functionality.

Now, gate your feedback ![:grinning_face_with_smiling_eyes:](https://ethresear.ch/images/emoji/facebook_messenger/grinning_face_with_smiling_eyes.png?v=14)

## Replies

**matt** (2019-10-29):

I think the idea of pausing execution with the ability to resume later is interesting, and it may be especially applicable for transactions that simply can’t fit within a single block. However, in the general case I think it adds more complexity than using intermediate roots. For example:

Some L2 construction does off-chain processing on a state tree S_0 to come up with a new state tree S_n. S_0 \to S_n may be too large to verify on the root chain, but it could be chunked into intermediate state roots that *can* be verified on chain. So instead of only posting roots of S_0 and S_n on chain the L2 operator would post roots of S_0, S_1, ... , S_n. The L2 construction would just need to define running out of gas for any transition S_i \to S_{i+1} as malicious.

Since the only verification that needs to be run on chain is the state transition between the last valid state and the first invalid state, this should scale for most types of transactions.

---

**johba** (2019-10-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/pinkiebell/48/3949_2.png) pinkiebell:

> This cripples layer-2 solutions because it becomes easy to block/delay finalization of side-chain Blocks on the root-chain Plasma-style bridge contract.

can you explain this more? The verification of computation is only relevant on exit, and Plasma exits give you plenty of time (3.5-7 days). So how are blocks hindered? ![:grinning:](https://ethresear.ch/images/emoji/facebook_messenger/grinning.png?v=12)

---

**johba** (2019-10-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/pinkiebell/48/3949_2.png) pinkiebell:

> Bridge -contract that manages the state of the side-chain can analyze and patch arbitrary smart contracts to ‘hijack’ the control flow

how expensive (gas) would something like this be? ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12)

---

**pinkiebell** (2019-10-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/matt/48/4560_2.png) matt:

> I think the idea of pausing execution with the ability to resume later is interesting, and it may be especially applicable for transactions that simply can’t fit within a single block. However, in the general case I think it adds more complexity than using intermediate roots. For example:
>
>
> Some L2 construction does off-chain processing on a state tree S_0 to come up with a new state tree S_n. S_0 \to S_n may be too large to verify on the root chain, but it could be chunked into intermediate state roots that can be verified on chain. So instead of only posting roots of S_0 and S_n on chain the L2 operator would post roots of S_0, S_1, ... , S_n. The L2 construction would just need to define running out of gas for any transition S_i \to S_{i+1} as malicious.
>
>
> Since the only verification that needs to be run on chain is the state transition between the last valid state and the first invalid state, this should scale for most types of transactions.

Full ack. it is easier to use intermediate state-roots if the constrains on the side-chain are that a valid transaction by definition can always be validated on the root-chain.

Even if the design of the layer-2 chain does not require to ‘chunk’ computation, the patching model allows to intercept `CALL`-opcodes and other custom operations that the bridge contract can deploy and call into. This was my initial issue to make that more efficient without bundling & running a complete EVM interpreter inside the EVM runtime itself.

---

**pinkiebell** (2019-10-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/johba/48/20905_2.png) johba:

> pinkiebell:
>
>
> This cripples layer-2 solutions because it becomes easy to block/delay finalization of side-chain Blocks on the root-chain Plasma-style bridge contract.

can you explain this more? The verification of computation is only relevant on exit, and Plasma exits give you plenty of time (3.5-7 days). So how are blocks hindered? ![:grinning:](https://ethresear.ch/images/emoji/facebook_messenger/grinning.png?v=12)

Plasma was just a pointer. In my example I assume that each Block has to be validated on-chain if someones doesn’t agree with the submitted block solution ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**pinkiebell** (2019-10-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/johba/48/20905_2.png) johba:

> pinkiebell:
>
>
> Bridge -contract that manages the state of the side-chain can analyze and patch arbitrary smart contracts to ‘hijack’ the control flow

how expensive (gas) would something like this be? ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12)

Good question.

If we account for things like copying the target code into memory, processing it, creating a new version, deploying it, calling the patched contract and once we are done `SELFDESTRUCT` the contract. That may not be necessarily cheaper nor more expensive, but that relies heavily on the target contract’s runtime characteristics and on the contract size.

I will let you know once I know more by writing a proof of concept, but I’m heavily loaded with tasks so I will not be able to work on this in the next 2-3 weeks.

The most important thing is that this doesn’t need a long-running truebit-like game and

the problem with denial of service attacks of many `solutions` ↔ `disputes`.

---

**pinkiebell** (2019-11-05):

I wrote a proof of concept earlier than I expected ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14),

the process of patching the bytecode (overwriting jumps), looking for opcodes to replace and finally deploy them inside a contract with `CREATE` costs about:

```auto
7.916.300 gas for the whole transaction.
Original bytecode length (included in calldata of the transaction): 6096 bytes.
With a resulting patched bytecode length of 6156 bytes.
```

There is  room for improvement ![:smirk:](https://ethresear.ch/images/emoji/facebook_messenger/smirk.png?v=14).

I published the PoC here:



      [github.com/NutBerry/stack](https://github.com/NutBerry/stack/blob/6af3dfbc1667da59a10a6a7c0ca0d1dcd21a1974/contracts/GatedComputing.sol)





####

  [6af3dfbc1](https://github.com/NutBerry/stack/blob/6af3dfbc1667da59a10a6a7c0ca0d1dcd21a1974/contracts/GatedComputing.sol)



```sol
pragma solidity ^0.5.2;

contract GatedComputing {
  function () external {
    assembly {
      function maybePatch (opcode, i, memOff) -> off {
        off := add(memOff, 1)
        // TODO: patch those
        // CALLVALUE - we can control it with the `call`
        // if eq(opcode, 52) {
        // }
        // ADDRESS
        if eq(opcode, 48) {
          // CALLVALUE
          mstore8(memOff, 52)
        }
        // ORIGIN
        if eq(opcode, 50) {
          // CALLVALUE
```

  This file has been truncated. [show original](https://github.com/NutBerry/stack/blob/6af3dfbc1667da59a10a6a7c0ca0d1dcd21a1974/contracts/GatedComputing.sol)










with a simple test-case here:



      [github.com/NutBerry/stack](https://github.com/NutBerry/stack/blob/6af3dfbc1667da59a10a6a7c0ca0d1dcd21a1974/test/GatedComputing.js)





####

  [6af3dfbc1](https://github.com/NutBerry/stack/blob/6af3dfbc1667da59a10a6a7c0ca0d1dcd21a1974/test/GatedComputing.js)



```js
'use strict';

const ethers = require('ethers');
const assert = require('assert');

const GatedComputing = require('./../build/contracts/GatedComputing.json');
const TestContract = require('./../build/contracts/TestGatedComputing.json');
const Runtime = require('./../js/NutBerryRuntime.js');

describe('GatedComputing', async function () {
  const provider = new ethers.providers.JsonRpcProvider(`http://localhost:${process.env.RPC_PORT}`);

  it('patching jumps and simple opcodes should work', async () => {
    const wallet = await provider.getSigner(0);
    const _factory = new ethers.ContractFactory(
      GatedComputing.abi,
      GatedComputing.bytecode,
      wallet,
    );
    const contract = await _factory.deploy();
```

  This file has been truncated. [show original](https://github.com/NutBerry/stack/blob/6af3dfbc1667da59a10a6a7c0ca0d1dcd21a1974/test/GatedComputing.js)

---

**johba** (2019-11-05):

wow, so that is NOT exactly a huge contract: [stack/contracts/mocks/TestGatedComputing.sol at d861030a3c0c91f498dcd6c965faee6e2059a496 · NutBerry/stack · GitHub](https://github.com/NutBerry/stack/blob/d861030a3c0c91f498dcd6c965faee6e2059a496/contracts/mocks/TestGatedComputing.sol)

![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=14)

---

**pinkiebell** (2019-11-05):

![:laughing:](https://ethresear.ch/images/emoji/facebook_messenger/laughing.png?v=9) Yep, that one is small. The cost for that is `128.903`  gas


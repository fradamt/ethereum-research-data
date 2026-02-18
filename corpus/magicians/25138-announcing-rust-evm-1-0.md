---
source: magicians
topic_id: 25138
title: Announcing Rust EVM 1.0
author: sorpaas
date: "2025-08-18"
category: Magicians > Tooling
tags: [evm]
url: https://ethereum-magicians.org/t/announcing-rust-evm-1-0/25138
views: 223
likes: 3
posts_count: 1
---

# Announcing Rust EVM 1.0

[rust-evm](https://github.com/rust-ethereum/evm) is a Rust implementation of the Ethereum Virtual Machine. It has been 8 years since the project first started in 2017 (back then it was called SputnikVM). We primarily target users who require extensive customization (for example, rolling out custom gas metering, special opcodes, interrupts, etc).

We have just released v1.0, which we invite you to test out: [Release evm-v1.0.0 · rust-ethereum/evm · GitHub](https://github.com/rust-ethereum/evm/releases/tag/evm-v1.0.0)

Documentations (which are still being ironed out): [evm - Rust](https://docs.rs/evm) and [evm_mainnet - Rust](https://docs.rs/evm-mainnet)

## Notable features

### Generalized design

The v1.0 branch kept many of the good features in v0.x. For example, we keep to maintain a clear separation between the EVM gasometer and EVM opcode interpretation. This allow chains with a different cost map to reuse Rust EVM as is, while rolling out a totally new gas metering strategy. (In v1.0, this actually becomes even easier – simply write your own `eval_gasometer`.)

v1.0 brings a few new important generalizations that allow certain customization to be possible.

- Opcode map: This is done through the Etable trait. Custom opcodes can be added “on the fly”, and you can switch between different interpretation strategies (match clause vs. evaluation table). You can also add pre- or post-hooks (commonly known as “inspectors” or “tracers”), which we explain further below.
- Trap/interrupt: Using HeapTransact, custom interrupts can now be returned (for example, via a custom opcode). For operations that must be done async (for example, a cross-chain call), the EVM execution can be paused any time in the middle until the return data becomes available.
- Config: This is now a pointer passed to each call frame, which makes account versioning possible. We can also define custom config items without changing the evm crate. This is made possible by Rust’s AsRef/AsMut traits (which we used extensively).
- Overlayed backend: EVM execution requires an overlayed backend due to the possibility of state reverts. Previously in v0.x, we only support one overlayed backend. Each time a new substate is entered, only the changed values are written into the new substate. Reverting a substate is cheap, but accessing a value may require querying all prior substates. The generalized trait in v1.0 allows different strategies to be implemented. For example, now a “journaled” overlayed backend is conceivable, which keeps only the newest substate and maintain a “revert journal” (which makes accessing a value cheaper, while reverting a bit more expensive).

### New call stack

v1.0 introduces a new call stack implementation (in other EVM libraries this is commonly called a “call frame”).

The call stack can now be both heap-based or stack-based. For “common” EVM smart contracts, a stack-based call stack is more efficient (simply due to the fact that it doesn’t need the additional heap allocations). However, EVM calls can be really nested (up to a depth of 1024). Therefore, other EVM libraries usually have to implement heap-based call stack to avoid possible stack overflow. The new call stack implementation combines the best of both worlds – in the default config in `evm-mainnet`, the call stack would first be stack based up to a depth of 4 (so that it runs faster), and then automatically switch to heap based for higher depth.

### Stepping and tracing

For debugging, two strategies are possible:

- Stepping, which means that the interpreter would immediately pause after every opcode evaluation. It gives back control to the caller. The entire interpreter state then becomes available for inspection.
- Tracing, which inserts specialized “hooks” into parts of the interpreter. The interpreter cannot be “paused” – it invokes those hooks and continue execution.

Rust EVM v0.x only supports **tracing**. Stepping is generally difficult to implement as it requires nested call stack stepping as well. v1.0 finally adds supports for both **stepping** and **tracing**. This is made possible by the new call stack design. The call stack can immediately pause at any moment and still maintain its valid state. An interpreter with depth more than one can be **stepped** just as normal – it will only advance the PC by one in the deepest call frame. The entire chain of interpreter calls can then be inspected.

In v1.0, **tracing** is also improved. It can now be done without any specialized hooks. This can simply be implemented as a chained Etable (`evm::interpreter::etable::Chained`).

### Custom interpreter

The invocation logic `evm::standard::Resolver` can now accommodate the requirements of custom interpreters. For example, we may need to support calling an RISC-V contract inside an EVM contract while inside an EVM call stack and maintaining the usual EVM execution context. `evm::standard::Invoker` can now support a custom interpreter implementation (which will usually be an `enum` wrapper with an extra variant around the normal EVM interpreter).

### Compliance and testing updates

We now pass the entire Ethereum test suites from Frontier hard fork to Cancun hard fork, which is production-ready.

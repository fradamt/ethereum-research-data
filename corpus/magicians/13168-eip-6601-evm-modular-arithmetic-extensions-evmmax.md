---
source: magicians
topic_id: 13168
title: "EIP-6601: EVM Modular Arithmetic Extensions (EVMMAX)"
author: jwasinger
date: "2023-03-05"
category: EIPs > EIPs core
tags: [evm, cryptography]
url: https://ethereum-magicians.org/t/eip-6601-evm-modular-arithmetic-extensions-evmmax/13168
views: 5145
likes: 4
posts_count: 11
---

# EIP-6601: EVM Modular Arithmetic Extensions (EVMMAX)

This is the discussion thread for [EIP 6601](https://github.com/ethereum/EIPs/pull/6601) (viewable EIP markdown [here](https://github.com/jwasinger/EIPs/blob/evmmax-2/EIPS/eip-6601.md)).  This is an iteration on the previous proposal: [EIP 5843](https://ethereum-magicians.org/t/eip-5843-evm-modular-arithmetic-extensions).

Differences between 6601 and 5843 at a high level:

- 6601 introduces a new EOF section type which stores modulus, precomputed Montgomery parameters, the number of values which will be used (runtime-configurable modulus is still supported).
- 6601 uses a separate memory space for EVMMAX values with new load/store opcodes to move values between EVMEVMMAX memory.
- 6601 supports operations on moduli up to 4096 bits (tentative limit as noted in the EIP).

## Replies

**shemnon** (2023-03-07):

- I’d like to see some narrative before each code section so I don’t have to play guess what the code snippet intends. Code segments are great for conformance but only code segments are bad for design reviews.  Especially the gas sections.
- I’d also like the gas target for gas calculation to be off of a 50Mgps (20ns) standard, not 40Mgps (25ns). Whatever the standard is will be a ceiling on performance, as speedups in other opcodes will be tied down by a block consisting of only modx calls. If the BLS precompiles are chosen in lieu of or in addition to this I will also push for a 50 instead of the 35Mgps (29ns) it was benchmarked against years ago.
- At the interop summit there was a discussion about removing observable side effects.  Can we have the load and store go to a separate MAX memory that is not observable outside of LOADX and STOREX?  i.e. not allow the matthew’s interim data to be visible to EVM execution in the frame memory?  My concern here is zkEVMs that may be able to do such math “natively” and requiring them to “show work” would make the circuits larger. It is also possible some languages and systems may have faster mechanism than a manual matthews multiply.
- What validation needs to be done for the setup section (section_kind=3)?  Can invalid params be specified (even modulus)?  Can malicious params be specified that would cause slower execution?

---

**jwasinger** (2023-03-07):

> Can we have the load and store go to a separate MAX memory that is not observable outside of LOADX and STOREX?

This is how it works in 6601.  When calling SETUPX and specifying a setup section that hasn’t previously been used in the current call-frame, a separate memory space is allocated that is associated with that setup section for the duration of the call frame.  LOADX/STORE move values from/to EVM memory and the memory space of the currently active modulus state (whose parameters are specified in last setup section set with `SETUPX`).

> I’d also like the gas target for gas calculation to be off of a 50Mgps (20ns) standard, not 40Mgps (25ns). Whatever the standard is will be a ceiling on performance, as speedups in other opcodes will be tied down by a block consisting of only modx calls. If the BLS precompiles are chosen in lieu of or in addition to this I will also push for a 50 instead of the 35Mgps (29ns) it was benchmarked against years ago.

I chose the gas rate based on results of benchmarks of the ecrecover precompile in Geth on my machine.

I don’t follow the argument that speedups in other opcodes will be tied down by a block consisting of only `*MODX` calls.  I don’t see why the costs chosen for EVMMAX opcodes would prevent repricing of other unrelated opcodes.

> What validation needs to be done for the setup section (section_kind=3)? Can invalid params be specified (even modulus)? Can malicious params be specified that would cause slower execution?

No even modulus.  Afaict there are not parameters that could cause slower execution.  This is something that should be verified and documented in the rationale perhaps.

---

**jwasinger** (2023-03-07):

Btw I have an implementation of the MiMC hash function using EVMMAX ([GitHub - jwasinger/mimc-evmmax](https://github.com/jwasinger/mimc-evmmax)).  Compared to the circomlib implementation which uses 17460 gas, the EVMMAX implementation only uses 3915 gas.

So EVMMAX can give huge cost reductions for MiMC and other zk-friendly hash functions (like Poseidon which has a [proposal](https://ethereum-magicians.org/t/eip-5988-add-poseidon-hash-function-precompile/11772) for a precompile).

---

**shemnon** (2023-03-08):

> I chose the gas rate based on results of benchmarks of the ecrecover precompile in Geth on my machine.

That should have been the standard then “40 Mgps, which is the speed of ECRecover on a 2013 Intel Mac Pro”, because processing gets faster and 25ns on a M2 mac is way different from 25ns on a RasPi4 or a 2013 Intel Mac Pro, or an amiga.

Perhaps an amazon cloud instance such as t3 would be a good reference.

---

**shemnon** (2023-03-08):

> No even modulus. Afaict there are not parameters that could cause slower execution. This is something that should be verified and documented in the rationale perhaps.

We should enumerate what they are and what happens if they are wrong, there has got to be more than just even modulus.  For an EOF embedded it can be to make the whole program invalid, and for dynamic allocaiton… exceptional halt?

---

**jwasinger** (2023-03-08):

For context, my machine has a 2015 i7-6500U CPU (2.50GHz) with turbo-boost disabled.  As far as processors go, it’s fairly underpowered which makes me think that it’s a fair system to use as an initial benchmark reference.

One issue with using (certain) cloud VMs for benchmarking is that they are burstable.  So that can skew the results.

---

**jwasinger** (2023-03-08):

Afaict, the validation rules in the EIP are comprehensive and should prevent the deployment of invalid contracts.  But of course, this needs more eyes on it and ideally, the nod from cryptographers that my assumptions are correct regarding validation rules.

> dynamic allocation

The maximum memory size that can be allocated by an EVMMAX contract is known at deployment time and EVMMAX contracts that would exceed the limit (`EVMMAX_MAX_MEM`) are rejected.

When `SETUPX` allocates memory space, it expands memory calculating the size from setup section parameters, and charging the modified memory expansion cost function (EVM memory expansion cost function which considers memory size to be the sum of EVM memory size and all active/previously-active modulus state memory spaces allocated by `SETUPX` in the current call frame).

Any exceptional behavior ends execution and immediately returns to the calling frame (without consuming all call gas).

---

**rdubois-crypto** (2023-11-22):

Adding a montgomery multiplier is indeed of great interest. But the EIP might be a little complex, with many opcodes being pushed. AddModX is very cheap to implement in pure solidity (it is mainly a matter of carry propagation), the real bottleneck is MulmodX.

Don’t you think that limiting the EIP to MulModX, where the user would be in charge to provide the correct precomputed values (Nprime, etc) as input to the precompile could be sufficient ?

Having an opcode added is already a fight, maybe simplifying the EIP with just one would increase its probability of acceptation.

---

**jwasinger** (2023-11-23):

> AddModX is very cheap to implement in pure solidity (it is mainly a matter of carry propagation), the real bottleneck is MulmodX.

Implementing addmodx in pure solidity actually would be very expensive compared to the pricing I’m proposing in the EIP.  Depending on the bitwidth, we’re talking about multiple additions/masking, a possible conditional subtraction (requiring jumps).

addmodx/submodx are also trivial in complexity compared to the other opcodes being proposed.

Also, because of the separation of evmmax slot space and evm memory/stack, not providing addmodx/submodx as opcodes would entail frequently moving values back-and-forth, and incur heavy overhead as a result.

---

**benaadams** (2025-05-01):

I’d add reducing scope from supply chain attack from adding 3rd party libraries with full memory access as precompiles to benefits


---
source: magicians
topic_id: 21976
title: EVMMAX implementers call #1, December 5 2024
author: abcoathup
date: "2024-12-06"
category: Protocol Calls & happenings
tags: [evmmax]
url: https://ethereum-magicians.org/t/evmmax-implementers-call-1-december-5-2024/21976
views: 93
likes: 0
posts_count: 1
---

# EVMMAX implementers call #1, December 5 2024

#### Agenda

[EVMMAX Implementers Call 1 · Issue #1204 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1204)

#### Summary

Summary by Kev *(Copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/1314198669230211295/1314220312811929641))*

- Besu & EthJS: add modular arithmetic lib
- Chance: Spec out poseidon and add a poseidon impl
- Jared: Help chance integrate into geth codebase
- Investigate whether we need to precompute poseidon constants in montgomery form
- (low priority) Investigate whether opcode inversion is so costly such that it needs to be an opcode and also used in a way that makes batch inversion not viable

#### Notes

Notes by [@pdobacz](/u/pdobacz) *(Copied from [ethereum/pm](https://github.com/ethereum/pm/issues/1204#issuecomment-2520781950))*

- clients/implementations represented: Geth, EthJS, Besu, evmone, Cairo ZK-VM
- progress updates:

geth (EIP-6690 prototype+bls prototype using evmmax-bls12-381 tool)
- evmone (low-level lib)

Poseidon use case

- no objections to select this as 1st priority use case to cover

point raised if the bottleneck for the use case isn’t calldata cost rather than mod arith cost

what constants of Poseidon are we interested in?

- depends on the field one’s using.

use case of Poseidon Hash itself

- merkle path verification, need 32 poseidon hashes for every update
- the constants matrix is the same for all of them for a single application
- constants change when you change the field

choice of assembler - Huff-based like `evmmax-bls12-381` vs `Yul` based
how to format Montgomery constants - opaque or explicitly in Montgomery form?

- needs measuring

modular inversion - should this be an opcode?

- complexity of such opcode would be large relative to current spec
- needs measuring

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/8/8d91b4173c421d60e10094d7f64329912e8a125b.jpeg)](https://www.youtube.com/watch?v=2ExBjJ0eySo)

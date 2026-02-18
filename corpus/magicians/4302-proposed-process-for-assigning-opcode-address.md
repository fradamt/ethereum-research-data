---
source: magicians
topic_id: 4302
title: Proposed Process for Assigning Opcode Address
author: MadeofTin
date: "2020-05-20"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/proposed-process-for-assigning-opcode-address/4302
views: 910
likes: 0
posts_count: 3
---

# Proposed Process for Assigning Opcode Address

It came upon the previous ACD that an author was unclear how an address is chosen for a precompile. I wrote a sample process that uses an EIP registry that tracks all opcodes. An Author would submit a PR to the registry to request an address as part of the processes.

Reasons this might be a good thing.

- Clear to Authors how to proceed
- The current spec of all opcode/precompiles exists in a single place.

Reasons it might not be a good thing

- More complex than necessary
- Process for process sake

Some proposed text that could be included in the EIP or EIP-1 .

> ### Process for Assigning Precompile Addresses
>
>
>
> Once an EIP containing a precompile has progressed to REVIEW or has progressed to a sufficient maturity* the authors may propose a precompile address through a PR to the PRECOMPILE REGISTRY(TBD). The Precompile Status reflects the EIP status it references.
>
>
> *The definition of sufficient is arbitered by the EIP Editors and is left to their decision.
>
>
> Example Format

| Value | Mnemonic | δ | α | Description | EIP | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 0x00 | STOP | 0 | 0 | Halts execution. | YP | FINAL |

Thoughts?

## Replies

**MadeofTin** (2020-05-21):

https://gitter.im/ethereum/AllCoreDevs?at=5ec5628c9832dd6f04649aa4

Some discussion in ACDs

---

**MadeofTin** (2020-05-21):

Suggested Process:

Alexander [@shamatar](/u/shamatar) May 20 11:10

I’d say it’s an overkill. I’d say that after EIPs are accepted (implemented and go into the testnet) then continuous chunk of addresses should assigned as it happened now. It’s not necessary to know addresses beforehand. If more than one EIP in a batch requires addresses than in EIP number ascending order each of them gets an assignment. Before finalization even the number of proposed precompiles may change

Martin Holst Swende [@holiman](/u/holiman) 01:02

Final state of precompile addresses might be good to include in hf meta-eips (if any precompile was added)


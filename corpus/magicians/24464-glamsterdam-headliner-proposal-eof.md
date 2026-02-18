---
source: magicians
topic_id: 24464
title: "Glamsterdam headliner proposal: EOF"
author: sorpaas
date: "2025-06-05"
category: EIPs
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/glamsterdam-headliner-proposal-eof/24464
views: 373
likes: 6
posts_count: 1
---

# Glamsterdam headliner proposal: EOF

This is a headliner proposal for EOF for Glamsterdam. EOF was SFI’d and then DFI’d for Fusaka. This proposal repropose it for Glamsterdam.

### Summary

Headliner proposal for EOF. Note that compared with Fusaka, this headliner proposal has an additional change of [EIP-9834](https://github.com/ethereum/EIPs/pull/9834) as a mandatory EIP.

The following texts are copied from [@ipsilon](https://notes.ethereum.org/@ipsilon/eof_fusaka_options)’s document (with the addition of EIP-9834).

### (A) - Complete EOF

The first option represents the status quo of the current plan - proceed with the version of EOF that is in the current “Osaka” meta spec, also known as Complete EOF.

Complete EOF is the result of multiple iterations of the design process that included all feedback such as Vitalik’s proposal to [ban code introspection](https://ethereum-magicians.org/t/eof-proposal-ban-code-introspection-of-eof-accounts/12113), Vyper’s request for an `EXCHANGE` operation, and Solidity’s request to enable tail calls with `JUMPF` .

- EIP-3540: EOF - EVM Object Format v1
- EIP-3670: EOF - Code Validation
- EIP-4200: EOF - Static relative jumps
- EIP-4750: EOF - Functions
- EIP-5450: EOF - Stack Validation
- EIP-6206: EOF - JUMPF and non-returning functions
- EIP-7480: EOF - Data section access instructions
- EIP-663: SWAPN, DUPN and EXCHANGE instructions
- EIP-7069: Revamped CALL instructions
- EIP-7620: EOF Contract Creation
- EIP-7873: EOF - TXCREATE and InitcodeTransaction type
- EIP-7834: Separate Metadata Section for EOF
- EIP-7761: EXTCODETYPE instruction
- EIP-7880: EOF - EXTCODEADDRESS instruction
- EIP-5920: PAY opcode
- EIP-9834: EOF - Extended types section

The major difference between this and all the other proposals is that Complete EOF retains the themes of Ban Code Introspection (implemented by EIP-7620, EIP-7698, and 7873), and Ban Gas Introspection (principally implemented by EIP-7069). Several EIPs are added to address community requested features that address gaps created by the bans (EIP-7761, EIP-7880, EIP-5920, EIP-7834).

### (B) - Minimal EOF

Minimal EOF represents the output of the EOF Breakout Room when [@lightclients](https://x.com/lightclients) was the facilitator.

As [tweeted by @lightclients](https://x.com/lightclients/status/1593270268956270594) the list of EIPs is

- EIP-3540: EOF - EVM Object Format v1
- EIP-3670: EOF - Code Validation
- EIP-4200: EOF - Static relative jumps
- EIP-4750: EOF - Functions
- EIP-5450: EOF - Stack Validation
- EIP-7698: EOF - Creation transaction
- EIP-9834: EOF - Extended types section

Notably absent are stack opcodes and introspection bans with their related EIPs. EIP-7698 is included to resolve a Shanghai-era limitation where developers could not append extra data to containers in deployment scripts, a factor in its initial deferral.

Banned opcodes are limited to `JUMP` , `JUMPI` , `PC` , `SELFDESTRUCT` , and `CALLCODE` . Dynamic `JUMP` and `JUMPI` are removed for stack validation, rendering `PC` unnecessary, while `SELFDESTRUCT` and `CALLCODE` are long-deprecated opcodes excluded from EOF containers.

### (C) - Baseline EOF

Baseline EOF offers a middle-ground approach, eliminating introspection bans and restoring most banned opcodes while retaining community-requested features and structural enhancements enabled by the EOF container.

Banned opcodes are `JUMP` , `JUMPI` , `PC` , `SELFDESTRUCT` , and `CALLCODE` for the same reasons they were banned in Minimal EOF

The EIP list consists of:

- EIP-3540: EOF - EVM Object Format v1
- EIP-3670: EOF - Code Validation
- EIP-4200: EOF - Static relative jumps
- EIP-4750: EOF - Functions
- EIP-5450: EOF - Stack Validation
- EIP-7698: EOF - Creation transaction
- EIP-663: SWAPN, DUPN and EXCHANGE instructions
- EIP-6206: EOF - JUMPF and non-returning functions
- EIP-7480: EOF - Data section access instructions
- EIP-7620: EOF Contract Creation
- EIP-9834: EOF - Extended types section

This formulation preserves proposed EOF layout while maximizing Complete EOF’s intended features. It sheds complexity by excluding opcodes tied to symbolic introspection and gas introspection replacements.

### (D) - Introspecting EOF

Introspecting EOF represents the least possible change from Complete EOF to respond to community criticism around the opcode bans and inline solidity blocks. The Gas Introspection theme would be dropped completely and the Code Introspection theme would be rolled back to only banning creates from memory, restoring the `EXTCODE\*` opcodes and removing restrictions on introspecting code in an EOF container.

Banned opcodes are limited to `JUMP` , `JUMPI` , `PC` , `SELFDESTRUCT` , and `CALLCODE` , but also adding `CREATE` , and `CREATE2` . The `CREATE` /`CREATE2` bans uphold a lightweight version of the “Ban Code Introspection” theme, preventing runtime code generation from memory while allowing introspection of EOF containers via `EXTCODE*` . Other bans align with Minimal EOF’s rationale: removing dynamic jumps for stack validation and phasing out deprecated opcodes.

The EIP list consists of:

- EIP-3540: EOF - EVM Object Format v1
- EIP-3670: EOF - Code Validation
- EIP-4200: EOF - Static relative jumps
- EIP-4750: EOF - Functions
- EIP-5450: EOF - Stack Validation
- EIP-6206: EOF - JUMPF and non-returning functions
- EIP-7480: EOF - Data section access instructions
- EIP-663: SWAPN, DUPN and EXCHANGE instructions
- EIP-7620: EOF Contract Creation
- EIP-7873: EOF - TXCREATE and InitcodeTransaction type
- EIP-9834: EOF - Extended types section

`EXTCODEADDRESS` , `EXTCODETYPE` and `PAY` are not necessary in this option. The metadata section would be visible to `COPDECOPY` and is no longer necessary.

### Detailed justification

The benefit of this proposal includes as stated in the original EOF proposal:

- Code and gas non-observability, allowing a more maintainable and upgradable protocol.
- Removal of JUMPDEST-analysis, simplifying reasoning about EVM bytecode.
- First-class support for EVM functions, improving analysis opportunities.
- Code versioning, paving the way for backward-incompatible changes.
- Addressing many other EVM pain points.

This headliner proposal also adds an additional EIP (EIP-9834) compared with the original EOF proposal. This is a mandatory EIP because it changes the semantics of `types_section`. This additional EIP allows code sections to have “types”. This small, but important change, makes EOF possible to invoke different “variants” of the execution environment within the same contract, allowing us to define new types such as “EVM64” and “RISCV”. Normal logic can be written in regular EVM, and computationally intensive logic can be written in EVM64 or RISCV. This paves the way for a simple and fast RISCV deployment, as on the Ethereum roadmap. This strategy, compared with alternative RISCV deployment proposals (for example, an ELF format), ensures that the changes are “incremental”. Contracts don’t need to be wholly rewritten – it’s not “either EVM or RISCV”, but “both EVM and RISCV”. Existing contracts can be incrementally adopted, only for its computationally intensive part. This ensures that we keep the functioning EVM toolchain and don’t split the ecosystem.

Why consider the inclusion now:

- It’s a highly sought (while sometimes controversial) feature from the community.
- The majority of the EIPs are already implemented.
- It paves the way for RISC-V roadmap and even allows for immediate RISC-V deployment with EIP-9834 (an RISC-V interpreter is even simpler than an EVM interpreter!).

### Stakeholder impact

- Positive: Performance improvements, better code analysis for ecosystem tools, RISC-V roadmap.
- Negative: Increase complexity, perceived community controversay.

### Technical readiness

The majority of the EIPs are already implemented. The addition of EIP-9834 is a simple change.

### Security & open questions

See [EOF discussion thread](https://ethereum-magicians.org/t/evm-object-format-eof/5727).

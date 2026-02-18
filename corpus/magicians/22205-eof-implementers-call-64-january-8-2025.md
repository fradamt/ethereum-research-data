---
source: magicians
topic_id: 22205
title: EOF implementers call #64, January 8, 2025
author: abcoathup
date: "2024-12-14"
category: Protocol Calls & happenings
tags: [eof]
url: https://ethereum-magicians.org/t/eof-implementers-call-64-january-8-2025/22205
views: 67
likes: 1
posts_count: 2
---

# EOF implementers call #64, January 8, 2025

#### Agenda

[EOF Implementers Call #64 · Issue #1217 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1217)

#### Notes



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png)

      [EOF implementers call #64, January 8, 2025](https://ethereum-magicians.org/t/eof-implementers-call-64-january-8-2025/22205/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> Call Notes
> Testing
>
> Need to merge 1 PR
> Fuzzing updates - execution-spec-tests/src/ethereum_fuzzer_differential/__init__.py at shemnon/eof-fuzz · shemnon/execution-spec-tests · GitHub
>
> Client Update
>
> No Client Updates
> Rebase off of Perctra-5
>
> Need at least 3 for the devnet
>
>
> Compiler support
>
> Reviewed the PR list
> How will small proposed changes impact?
>
> Not too bad.
> Hashing is more impactful
> Need to totally nail down all changes before the experimental flag gets removed.  Flag may remain until…

#### Recording

  [![image](https://img.youtube.com/vi/cBKdFSC1VA8/maxresdefault.jpg)](https://www.youtube.com/watch?v=cBKdFSC1VA8)

## Replies

**shemnon** (2025-01-08):

Call Notes

Testing

- Need to merge 1 PR
- Fuzzing updates - execution-spec-tests/src/ethereum_fuzzer_differential/__init__.py at shemnon/eof-fuzz · shemnon/execution-spec-tests · GitHub

Client Update

- No Client Updates
- Rebase off of Perctra-5

Need at least 3 for the devnet

Compiler support

- Reviewed the PR list
- How will small proposed changes impact?

Not too bad.
- Hashing is more impactful
- Need to totally nail down all changes before the experimental flag gets removed.  Flag may remain until mainnet is live (not even testnet, mainnet)

Assembly syntax for EXCHANGE opcode is still undetermined (absolute byte encoding, vs nybbles, vs stack index, all off by 1 issues)

- Off by one also leaks into possible SWAP/SWAPN numbering as well (DUP/SWAP are already inconsistent)
- Frangio’s summary - Assembly Syntax for EOF Stack Instructions - HackMD

Exact is Frangio’s recommendation

Spec

- Metadata - EIP-7834: Separate Metadata Section for EOF

EVMONE will look into a spike

EOFCREATE/TXCREATE Hashing

- Summary doc - Potential scenarios of updating the new contract address schemes for EOF - HackMD
- Also pre-ERC for standard contracts Comparing ethereum:master...shemnon:eof/txcreate-factories · ethereum/ERCs · GitHub
- Shipping temp check

When there are no deal-breakers
- 2025 seems tight
- Best to tie with PeerDAS, unless there is a large differential

So the EL and CL fork major features at the same time
- But PeerDAS/EOF not as tied as, say, withdrawals

Devnet-1 punch list - [EOFv1 final tuning · Issue #165 · ipsilon/eof · GitHub](https://github.com/ipsilon/eof/issues/165)
We need to disuss the ACCOUNTTYPE opcode - EIP-7761 - MUST/SHOULD - dealbreaker for app dev until it’s in.

- is ERC-165 a viable alternative?
- What would app devs accept?


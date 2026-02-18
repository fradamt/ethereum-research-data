---
source: magicians
topic_id: 20853
title: EOF Implementers call #56, Aug 21 2024
author: shemnon
date: "2024-08-21"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eof-implementers-call-56-aug-21-2024/20853
views: 86
likes: 2
posts_count: 2
---

# EOF Implementers call #56, Aug 21 2024

**Agenda**

[EOF Implementers Call #56 · Issue #1128 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1128)

**Video**

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/2/2304dcb4aa8307250d51ea404fc67cf2e93fc7f3.jpeg)](https://www.youtube.com/watch?v=03Dkfpvw4Pc)

[link](https://www.youtube.com/watch?v=03Dkfpvw4Pc)

**Call Notes**

> Client and fuzzing updates
>
>
> evmone found a bug that fuzzers couldn’t find
> besu had subcontainer container bugs found via evmon’s tests a few weeks ago
> Nethermind is re-writing their subcontainer validation to not be recursive
> Reth and Geth were not present.
>
>
>
>
> Spec updates
>
>
> community strongly wants a EXTCODESIZE/ISCONTRACT solution, Libs may not be happy with legacy “escape hatch” contracts rather than using  EIP-165 introspections
>
> If AA is the reason not to proceed, a clear plan needs to be stated as to how the AA transition is expected to play out.
>
>
> Delegate call into legacy call rule
>
> This may break proxies. (EOF proxies, proxying to a legacy contract)
> A detection of EOF vs legacy contract would be useful.  EXTCODEHASH would identify EOF
> No opinion about 7702 proxy detection detection, can go with legacy treatment.
>
>
>
>
>
>
> Testing Readiness
>
>
> With devnet-4 we need to activate on prague alone
>
> EEST will migrate to just “Prague” for tests,
> EEST will sunset “CancunEIP7692” and “Prague7692” forks
> Will change once 7702 tests are fully merged into tests
> Suddenly 7702 tests will work with EOF
>
>
> New fixtures release 1.0.8 - Contains Both pragueEIP-7692 and Cancun7692
> EOF Container Fuzzing
>
> EVMONE and Besu
>
>
> EOF Execution fuzzing
>
> possibly goevmlab, guido vranken’s fuzzer.
>
>
>
>
>
>
> Testing matrix
>
>
> Devs, please update
> Any automation interest?
>
> Maybe hive/consume?
>
> Still needs final consume setup in CI
> Consume does not run EOF Validation tests (because engine API is the test interface)
>
>
>
>
>
>
>
>
> github comment

## Replies

**abcoathup** (2024-08-23):

ERC-721 & ERC-1155 need “ISCONTRACT” and proxies could be bricked by DELEGATECALL limitation by [@frangio](/u/frangio):


      ![](https://ethereum-magicians.org/uploads/default/original/2X/8/8f0a562a90992dd656ced3f9b9b37c942cfbde54.png)

      [HackMD](https://hackmd.io/@frangio/S1VvatXiR)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



Token transfers in the two main NFT standards behave differently when the receiver is a contract. In that case, the token invokes a callback on the receiver (e.g., onERC721Received), and unless a specific value is returned from the callback the...


---
source: magicians
topic_id: 21543
title: EOF implementers call #62, November 27 2024
author: abcoathup
date: "2024-11-02"
category: Protocol Calls & happenings
tags: [eof]
url: https://ethereum-magicians.org/t/eof-implementers-call-62-november-27-2024/21543
views: 116
likes: 2
posts_count: 1
---

# EOF implementers call #62, November 27 2024

#### Agenda

[EOF Implementers Call #62 · Issue #1192 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1192)

#### Notes

Notes by [@shemnon](/u/shemnon) *(Copied from [ethereum/pm](https://github.com/ethereum/pm/issues/1192#issuecomment-2504249197))*

##### Testing Update

- How to handle State tests with invalid EOF?

state tests - reject test if any EOF is invalid
- Block tests - only an issue in genesis? Abort if EOF in genesis is invalid.
- Imported blocks - presume valid as create TXes are how they are added, so invalid EOF should result in an failed transactions.
- Extends to 7702 - 0xEF01 validation?

EOFWrap Tests

- ports over legacy tests into EOF if it ports, stopgap for full testing
- feat(tests): port ethereum/tests test cases (tracking issue) execution-spec-tests#972 will ultimately port all old tests

##### Client and Compiler Updates

- No client updates, mostly focused on pectra
- Solidity working on EOF as an experimental feature

eof: Support functions (CALLF, RETF, JUMPF) solidity#15550
- eof: Implement stack height calculation solidity#15555
- EOF: Implement ext*calls solidity#15559

##### Spec Updates

- Compiler Metadata Section

Kaan from Sourcify Team
- Current practice is to just append
- would want a separate metadata section in EOF.

Unreachable by code (a good thing)
- contains the CBOR data solidity produces

Current status of appended to data and behind constructor fields makes it hard to find
Experimental Solidity EOF handling is to put CBOR metadata at the beginning of the data section.
Would insulate code/data indexes from variable CBOR sizes, such as if experimental flags are logged.
Next step is an EIP

Brief discussion on header section numbers

##### EOFCREATE hash -

- danno wants a “0xef01” hash added
- Solidity has concerns about the genericness, would prefer container index
- Bad salt management could prohibit multiple deployments
- Should hash include auxdata, not just code data?
- possible issues with cross-chain deployment. The more mandatory data makes same address contracts difficult.
- note: some people don’t like metadata has in CREATE2, would compiler metadata be excluded from address derivation?
- Are there security implications? Would the “code hash” guarantees be forgotten about? Could compilers compensate?
- Please add comments to the thread.

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/2/2304dcb4aa8307250d51ea404fc67cf2e93fc7f3.jpeg)](https://www.youtube.com/watch?v=yzYUWpa-1QM)

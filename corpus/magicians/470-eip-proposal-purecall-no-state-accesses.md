---
source: magicians
topic_id: 470
title: "EIP Proposal: PURECALL (no state accesses)"
author: fubuloubu
date: "2018-05-28"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-proposal-purecall-no-state-accesses/470
views: 915
likes: 0
posts_count: 3
---

# EIP Proposal: PURECALL (no state accesses)

Was chatting with [@pipermerriam](/u/pipermerriam) about this idea, curious if there are existing EIPs or proposals for it.

Basically, this proposal would be for a new calling opcode like `STATICCALL` that would ensure no state reads are occurring (along with state writes), and additionally that no environment variable reads are occurring (e.g. `coinbase`, `msg.sender`, etc.)

The use of this would be for an additional degree of confidence in library calls not accessing state, inspired most prominently by Casper’s “purity checker” which ensures that the validator’s signature code does not access these values and is a “pure call”.

Let me know what you think, if there’s no other EIPs and this is a good idea I will create one.

## Replies

**fubuloubu** (2018-05-28):

This is similar:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/117)












####



        opened 05:36AM - 19 Jun 16 UTC



          closed 10:52PM - 04 Jun 20 UTC



        [![](https://avatars.githubusercontent.com/u/886059?v=4)
          MicahZoltu](https://github.com/MicahZoltu)










When a contract wants to call another contract, at the moment there is quite a b[…]()it of risk for the developer because they need to make sure that there are no re-entry bugs/exploits (which can exist across contracts).  As shown, these bugs are very subtle and can slip by developers and auditors.

To assist developers in solving this problem, I propose adding a `SANDBOXED_CALL` opcode that would guarantee that the called contract cannot execute any code outside of their own contract.  The called contract would be able to do whatever function calls and state changes they want inside of its contract but any attempt to call out of its contract would result in an exception being thrown.  This opcode would require a gas amount passed into it, though contract authors should be encouraged to pass a fairly large value to allow for complex contracts to execute on the other end.

`SANDBOXED_CALL` should be used when you want to safely call an external contract that you depend on, but don't trust.  The developer should assume that these are safe from reentry type attacks but still susceptible to DOS style attacks like stack exhaustion and OOG.












[@pipermerriam](/u/pipermerriam) was tossing around the idea of a more abstract opcode that allows you to describe the allowed accesses of the call via a list of flags.

---

**fubuloubu** (2018-05-29):

[@axic](/u/axic) mentioned this exact proposal on EIP195:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/195#issuecomment-350944654)














#### Comment by
         -


      `master` ← `vbuterin-patch-1`







I think two versions of this instead the current proposed one would make more se[…](https://github.com/ethereum/EIPs/pull/195)nse:
1) Would read from code offset and length within the current contracts code. This means calling a function part of the callee contract wouldn't need to do a `codecopy` to memory first in order to pass it to `purecall`.
2) Load code from a destination address and execute it with restricting both state reading and writing operations (`staticcall`'s counterpart). For rules on what are state reading operations one could refer to Solidity's categorisation: https://github.com/ethereum/solidity/blob/develop/libevmasm/SemanticInformation.cpp#L192-L218

Though for 2) practically it would need a new opcode to determine the current context type (`ISPURE` or a more generic approach is `CALLTYPE` to return `regular`, `delegate`, `static`, `pure`). At least Solidity checks that no value was sent in a call if the function doesn't expect it and that is done via the `CALLVALUE` opcode, which is restricted in the pure context.












We should revisit [@vbuterin](/u/vbuterin)’s proposal


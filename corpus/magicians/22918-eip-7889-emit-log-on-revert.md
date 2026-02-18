---
source: magicians
topic_id: 22918
title: "EIP-7889: Emit log on revert"
author: shohamc1
date: "2025-02-20"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7889-emit-log-on-revert/22918
views: 134
likes: 3
posts_count: 8
---

# EIP-7889: Emit log on revert

This EIP would allow apps and tools to have a standard way to get revert messages of a transaction.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9390)














####


      `ethereum:master` ← `shohamc1:shohamc1/add-eip`




          opened 04:35AM - 20 Feb 25 UTC



          [![shohamc1](https://avatars.githubusercontent.com/u/7486955?v=4)
            shohamc1](https://github.com/shohamc1)



          [+50
            -0](https://github.com/ethereum/EIPs/pull/9390/files)







This PR proposes to emit a log containing the revert message for reverted transa[…](https://github.com/ethereum/EIPs/pull/9390)ctions, making it accessible via standard RPC without the need for tracing.

## Replies

**jochem-brouwer** (2025-02-20):

Hey there, I like this idea and I also see how this is useful in practice. However, this will incur gas extra gas cost on any `REVERT` operation which has nonzero byte length. This will:

1. Increase gas costs of anything which runs in a REVERT which reports nonzero data
2. Due to raising gas costs of the REVERT opcode this might now break things (REVERT having not enough gas to pay for log costs → the revert now gets converted in an INVALID. This also means that if return bytes were written as REVERT error data these are now cleared, because the call frame turns in a INVALID call frame instead of a REVERT one)

Have you considered this alternative: introduce 5 new opcodes with exactly the same semantics as `LOGx` (`LOG0` … `LOG4`) which we call `RLOG`. The logs are now kept and emitted even in case this call frame / upper call frames REVERT / INVALID.

Did you also consider the fact that you could create a wrapper in the calling code which will catch and `LOG` data in case it runs in a REVERT? Without doing a fork or introducing new opcodes, you could: (1) call the contract and on (2) return values, check if the call succeeded. If this is not the case, check if there is RETURNDATA (`RETURNDATASIZE > 0`). If this is the case, now emit a log (you can read the reverted data from the returndata and thus log this)

---

**wjmelements** (2025-02-20):

I don’t think it needs to be a log but return data could become a separate part of the transaction receipt. We would need to meter it in the gas for the top-level transaction.

---

**shohamc1** (2025-02-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> However, this will incur gas extra gas cost on any REVERT operation which has nonzero byte length. This will:

We had two ideas in mind to solve this:

1. Make the log free like EIP-7708
2. Charge the log gas as part of intrinsic gas

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Have you considered this alternative: introduce 5 new opcodes with exactly the same semantics as LOGx (LOG0 … LOG4) which we call RLOG. The logs are now kept and emitted even in case this call frame / upper call frames REVERT / INVALID.

While I do like this idea (and makes sense to do it in addition to this), it doesn’t really solve the issue that this EIP is trying to solve (create a standard way to get the revert message) since it would require smart contracts to opt in to this feature.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Did you also consider the fact that you could create a wrapper in the calling code which will catch and LOG data in case it runs in a REVERT?

I don’t quite get what you mean here - is this wrapper is a smart contract on chain?

---

**shohamc1** (2025-02-20):

I did consider transaction receipts - and it does make sense to at least place it there if we don’t decide to do it as a log. However doing it as a log has some benefits:

- Filtering across a block(s)
- Monitor for failed transactions with eth_subscribe

Adding it as a part of the receipt also brings issues with historical data since there would be some database migration required to service receipt queries for older transactions.

Also see Felix’s comments [here] regarding return data not being part of the receipt. ([feat: add returndata to tx receipts by charles-cooper · Pull Request #542 · ethereum/execution-apis · GitHub](https://github.com/ethereum/execution-apis/pull/542#issuecomment-2551613713)).

---

**alex-forshtat-tbk** (2025-02-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Due to raising gas costs of the REVERT opcode this might now break things (REVERT having not enough gas to pay for log costs)

In case we decide to increase the cost of the `REVERT` opcode, how big of an issue will be the edge-case of not having enough gas to emit the `REVERT` log? The result would be a transaction with an “out-of-gas” revert reason that has no emitted events on-chain, which is exactly the case with all reverted transactions right now.

And overall, to me it seems quite similar to having a transaction run out of gas exactly upon reaching a `require(condition, "good revert reason")` statement in a smart contract even without a revert log - unfortunate, but the revert reason will be kind of “lost”.

---

**Arvolear** (2025-02-20):

I see how this can be useful for some debugging/tracing, but could you please elaborate on what problem you are trying to solve?

Also a question how would the behavior of a `STATICCALL` change? Currently emitting logs in a static context is prohibited.

---

**alex-forshtat-tbk** (2025-02-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arvolear/48/11091_2.png) Arvolear:

> Could you please elaborate on what problem you are trying to solve?

The problem is providing to Blockchain users and app developers an easy, out-of-the-box and decentralized access to the revert reasons of their transactions. The usefulness of this feature may range from slightly better UX to potential security threats.

Currently, the revert reasons of transactions are either unknown, or may provided by Etherscan on supported chains. Which is a centralized service that is forced to trace transaction to discover this information in the first place, which is extremely inefficient. There is also no way to check if the displayed value is correct and it may even contain some false data.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arvolear/48/11091_2.png) Arvolear:

> Also a question how would the behavior of a STATICCALL change?

As the EIP only affects the top execution frame of the transaction, and the top frame cannot be a `STATICCALL`, there is no overlap between the two.


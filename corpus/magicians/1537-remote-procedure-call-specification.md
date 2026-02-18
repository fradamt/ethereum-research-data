---
source: magicians
topic_id: 1537
title: Remote procedure call specification
author: bitpshr
date: "2018-10-05"
category: EIPs > EIPs interfaces
tags: [json-rpc]
url: https://ethereum-magicians.org/t/remote-procedure-call-specification/1537
views: 9563
likes: 52
posts_count: 36
---

# Remote procedure call specification

Much of Ethereum’s effectiveness as an enterprise-grade application platform depends on its ability to provide a reliable and predictable developer experience. Nodes created by the current generation of Ethereum clients can expose RPC endpoints with differing method signatures; this forces applications to work around method inconsistencies to maintain compatibility with various Ethereum RPC implementations.

Both Ethereum client developers and downstream dapp developers lack a formal Ethereum RPC specification. This proposal attempts to standardize such a specification in a way that’s versionable and modifiable through the traditional EIP process.

This initial draft was based on the [current Ethereum RPC wiki documentation](https://github.com/ethereum/wiki/wiki/JSON-RPC), so feedback is highly encouraged.

[Proposal draft](https://github.com/bitpshr/EIPs/blob/eip-rpc/EIPS/eip-rpc.md)

*Related to [ethereum/EIPs#1442](https://github.com/ethereum/EIPs/issues/1442)*

## Replies

**perpetualescap3** (2018-10-05):

Thank you for formalizing this, glad to see a section that defines a process for adding new RPC methods too, albeit a bit sparse. Would be great to get anyone from geth / parity to chime in to help refine the actual specification for key RPC endpoints too, but I expect this to evolve over time.

This is very-much needed and this markdown format looks **great** compared to the current wiki RPC article everyone relies on today.

Long overdue. A1 effort for the doing this for the community [@bitpshr](/u/bitpshr).

---

**tjayrush** (2018-10-05):

This is excellent. I’m super appreciative of this.

As a frequent user of the existing spec, may I suggest that one of the best parts of those specs is the ‘curl’ examples. I’m not sure how hard that would be to add, but I constantly copy and paste those commands as I’m adding new features to my code.

Also, I very much encourage the addition of a process for enhancing/expanding the RPC interfaces. There’s a lot of things that can be improved.

Finally, I wonder how hard it would be to attach some documentation on using the IPC interfaces. The requests are the same, but the connection is different (not sure how).

---

**bitpshr** (2018-10-06):

Hi [@tjayrush](/u/tjayrush), thanks for your feedback. I updated all method examples with proper `curl` syntax and strengthened the verbiage around the process for [adding or modifying RPC methods](https://github.com/bitpshr/EIPs/blob/eip-rpc/EIPS/eip-rpc.md#proposing-changes).

---

**veox** (2018-10-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> I wonder how hard it would be to attach some documentation on using the IPC interfaces.

As I understand, this EIP is about standartising a set of [JSON-RPC](https://www.jsonrpc.org/specification) requests, and associated responses.

Information on using IPC (local sockets), HTTP (or websockets), or some other transport are likely out of scope for this document. At least I hope so, as otherwise it’d make the scope very broad.

---

**veox** (2018-10-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bitpshr/48/190_2.png) bitpshr:

> This initial draft was based on the current Ethereum RPC wiki documentation , so feedback is highly encouraged.

There is a mention of “compact notation”, but no in-document explanation, or outside reference, to what that is.

There may be value in adding the generic section on RFC2119 keywords, like [in this EIP](https://github.com/ethereum/EIPs/blob/ed621645c8f3bc5756492f327cda015f35d9f8da/EIPS/eip-1123.md#rfc2119), for example.

The `shh` (Whisper) methods likely shouldn’t be in this spec.

---

**bitpshr** (2018-10-08):

Thanks for the feedback [@veox](/u/veox). I made a few updates to the proposal:

- Clarified the verbiage around “compact hex notation”
- Added the verbiage suggested by RFC-2119
- Removed the whisper RPC methods since they aren’t technically Ethereum RPC methods

Also, you are correct that the sole intention of this EIP is to standardize Ethereum RPC requests, not to standardize semantics around underlying transport layers or their connections (though I do think that would be worthwhile in the future, [@tjayrush](/u/tjayrush).)

---

**veox** (2018-10-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bitpshr/48/190_2.png) bitpshr:

> Clarified the verbiage around “compact hex notation”

Nice!

It would perhaps be worthwhile to include all of `0x`, `0x0`, `0x00` for both `Quantity` and `Data`, to make the tables as explicit as possible.

For `Quantity`:

- 0x - invalid - empty not a valid quantity
- 0x0 - valid - interpreted as a quantity of zero
- 0x00 - invalid - extra leading 0 digit

For `Data`:

- 0x - valid - interpreted as empty data
- 0x0 - invalid - each byte must be represented using two hex digits
- 0x00 - valid - interpreted as a single zero byte

---

**bitpshr** (2018-10-09):

Good call [@veox](/u/veox), [updated](https://github.com/bitpshr/EIPs/blob/eip-rpc/EIPS/eip-rpc.md#value-encoding). This type of feedback is valuable and very much appreciated.

---

**carver** (2018-10-09):

For `eth_estimateGas`, how about adding a note for what should happen in different scenarios:

- revert
- throw
- ran out of gas, at the pending block’s gas limit

In my opinion, it should return an “error” instead of a “result”. None of the error codes is an obvious match to me, so maybe we need a new code (or a few).

---

**hiddentao** (2018-10-10):

In the ethereum clients list you should also include Ganache. On a larger note, it’s important that clients focussed on testing also implement this interface correctly.

---

**dekz** (2018-10-16):

This makes me incredibly happy as a library developer. Would love to contribute in any shape or form. I had begun work on a test suite which executed some known tests against various providers and output their result. Sort of a compliance framework. This was focused on the Provider signing behaviour (`eth_sign`).

Revert with Reason is another inconsistent response from RPC providers. Definitely documenting the error responses is just as important as documenting the success responses.

---

**dekz** (2018-10-17):

How would you like to go about discussing defining the non-success error cases for things like `eth_call`.

This is an interesting “error” response since the `eth_call` can fail or a number of reasons (usual JSON RPC error, contract not found) and it can also fail and return data, such as the `revert with reason`. Last time I checked, Geth and Parity differ in how they return this data.

Geth && Ganache:

```auto
{
  "jsonrpc": "2.0",
  "id": 824,
  "result": "0x08c379a000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000017494e56414c49445f4f524445525f5349474e4154555245000000000000000000"
}
```

Parity:

```auto
{
  "jsonrpc": "2.0",
  "id": 16,
  "error": {
    "code": -32015,
    "data": "Reverted 0x08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000f5452414e534645525f4641494c45440000000000000000000000000000000000",
    "message": "VM execution error."
  }
}
```

There are two things that are important here:

1. The call reverted
2. The revert returned some data, revert with reason

With Geth/Ganache it is hard to determined if in fact the `eth_call` was a Revert. Luckily no one has ran into a bytes4 collision with `0x08c379a`, yet…

Parity’s response alerts you to the fact that it did revert, though having to parse out the `Reverted` string to detect this is inconvenient. I am also not 100% convinced that this is an error case, but am happy to be convinced otherwise.

I would like to discuss this case behave similar to a `eth_call` success, but with the introduction of the status field. Status field behaves as expected with other JSONRPC calls:

`status` - `1` if this transaction was successful or `0` if it failed

Revert With Reason:

```auto
{
  "jsonrpc": "2.0",
  "id": 16,
  "status": "0x00",
  "result": "0x08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000f5452414e534645525f4641494c45440000000000000000000000000000000000",
}
```

Revert:

```auto
{
  "jsonrpc": "2.0",
  "id": 16,
  "status": "0x00",
  "result": "0x",
}
```

Successful call:

```auto
{
  "jsonrpc": "2.0",
  "id": 16,
  "status": "0x01",
  "result": "0xcafe",
}
```

Standard error response:

```auto
{
    "jsonrpc": "2.0",
    "id": 1337,
    "error": {
        "code": -32000,
        "message": "Invalid Input"
    }
}
```

---

**ryanschneider** (2018-10-17):

I think adding `status` to the top-level result is a little too far outside the bounds of the JSONRPC 2.0 spec:

https://www.jsonrpc.org/specification#response_object

While the spec doesn’t expressly forbid adding new top-level fields, it doesn’t *allow* it either, and most JSONRPC parsers would at best ignore the `status` field and at possibly throw an error.

So, I think any solution to the problem needs to be JSONRPC 2.0 compliant.  Parity’s “reverted” format is in-spec, but could be tweaked slightly to make it easier to parse:

```auto
{
  "jsonrpc": "2.0",
  "id": 16,
  "error": {
    "code": -32015,
    "data": {
       "result": "0x",  // is the 0x08c379a... data useful? if so include it
       "status": "reverted",
    },
    "message": "VM execution error: transaction reverted"
  }
}
```

Alternatively, as you said, if reverting isn’t an error, the only real option is to make the `eth_call` result an object instead of a single string, but that will be a breaking change for *many* web3 libraries.

In hindsight, the `result` field for all RPCs should always be a complex object, so that fields can be added easily in the future.  Perhaps that should be an EIP requirement for new methods going forward, but I think is too onerous to back port to the existing methods.

---

**cdetrio** (2018-10-17):

copying from the [PR description](https://github.com/ethereum/EIPs/pull/1474):

> Note:  There doesn’t appear to be any RPC-friendly API documentation standard, otherwise I’d be open to using that over markdown. Still, this EIP is meant to provide a human-readable RPC specification and isn’t necessarily meant to be program-readable or to drive other documentation tooling (though the markdown itself could drive tooling if desired).

My expectation is that if the RPC specification is only human readable, then it will quickly become outdated just like the current wiki. A human-readable spec relies on volunteers (client developers and users) to update the documentation, which is a laborious burden that people tend to grow tired of.

As a solution, I proposed a machine-readable spec ([Universal specs for JSON-RPC API methods · Issue #217 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/217)), and kickstarted the effort with a multi-client testrunner and proof-of-concept compatibility table:  [Ethereum client compatibility table](http://cdetrio.github.io/eth-compat-table)

It was recently dusted off and run again on the the latest clients: [run rpc-compat on the latest clients · Issue #119 · ethereum/hive · GitHub](https://github.com/karalabe/hive/issues/119)

Here’s a screenshot of the table:

[![](https://ethereum-magicians.org/uploads/default/optimized/1X/984f59430e35c79e1058b5a4f379d5941ca7ac7d_2_668x500.png)1146×857 102 KB](https://ethereum-magicians.org/uploads/default/984f59430e35c79e1058b5a4f379d5941ca7ac7d)

It only has the JSON schema specs for a handful of rpc methods, so the main remaining todo is to add the rest. Additionally, I was planning to the `description` field in the json schema to auto-generate the wiki documentation. This way we would not be relying on volunteers to keep the documentation up to date. Rather, the testrunner automatically checks which clients are compatible with the spec, and the human-readable documentation is generated from the spec.

---

**tjayrush** (2018-10-19):

I totally support the idea that the spec should be machine readable. The human readable spec should be an output of the machine readable spec. The test results could be added to the human-readable machine-generated documentation.

---

**dekz** (2018-10-23):

I think this is a fine suggestion. Backporting or supporting older callers is possible but likely to be an extreme pain and disruption.

Here is a [real example](https://github.com/MetaMask/metamask-extension/issues/5579) of where the inconsistencies causes errors in projects like Metamask. Inconsistencies in these error cases cause wild and unexpected behaviours.

`"status": "reverted"` I don’t particularly want to bikeshed on this but usually this is a hex value no?

`eth_call` is a simple way to validate a transaction has a chance of success before sending. So defining the failure case and standardising will help projects a lot.

---

**dekz** (2018-10-23):

Any thoughts on what to do about things in the ecosystem which hijack certain JSONRPC requests. For example, Metamask handles `eth_sign` but forwards all data fetching, though the responses can be different when going through Metamask versus a client directly.

Is it easy to add additional less conventional “clients” to this test suite?

---

**MicahZoltu** (2018-10-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dekz/48/75_2.png) dekz:

> Any thoughts on what to do about things in the ecosystem which hijack certain JSONRPC requests. For example, Metamask handles eth_sign but forwards all data fetching, though the responses can be different when going through Metamask versus a client directly.

As I have argued in the past, signers and clients should be separated!  There is “the thing that signs stuff” and there is "the thing that sends/receives data from the blockchain.  It is most unfortunate that the early Ethereum clients combined these two functionalities into the same API rather than keeping them as separate APIs.

I would love it if we could split the current API into two separate APIs, one for signing and one for fetching/submitting data from/to the blockchain.  Some tools would fulfill both APIs, but having them separate would allow you to mix and match as appropriate.

---

**dekz** (2018-10-23):

Agree and we can definitely see the carving up of responsibilities, its just at the library level right now. We do this in 0x.js and we encourage all developers to do this (via our developer docs and samples). Mix and match Ledger/Trezor/MM/Generic with a general JSONRPC data provider.

At the very least I think we can section them off and call it out in the JSONRPC spec/wiki. Do you have thoughts on what this would ultimately look like? I imagine their specs should follow similar behaviour (in terms of errors and layout of results).

---

**MicahZoltu** (2018-10-23):

I haven’t thought super deep on the implementation details.  In general, anything that requires a private key to complete should be part of the signer API and antsything that requires chain interaction would be part of the other API.

This does get murky when you want to do things like verifiable signing UIs, because the signer needs chain access.  In such cases I would argue that should be part of the signing API, as the signer can gracefully degrade if it doesn’t have chain access.


*(15 more replies not shown)*

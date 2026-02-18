---
source: magicians
topic_id: 24640
title: "EIP-7966: eth_sendRawTransactionSync Method"
author: thnhnv
date: "2025-06-23"
category: EIPs > EIPs interfaces
tags: [json-rpc, transactions]
url: https://ethereum-magicians.org/t/eip-7966-eth-sendrawtransactionsync-method/24640
views: 760
likes: 18
posts_count: 17
---

# EIP-7966: eth_sendRawTransactionSync Method

Discussion topic for [EIP-7966: eth_sendRawTransactionSync Method](https://github.com/ethereum/EIPs/pull/9890).

## Summary

The traditionally asynchronous transaction submission and confirmation is no longer suitable for blockchains optimized for latency. While Ethereum’s 12s blocktime made async patterns necessary to avoid freezing applications, modern chains with millisecond blocktimes make this approach inefficient. The current two-RPC paradigm (*send transaction* + *poll for receipt*) introduces unnecessary network round-trips and complexity when transactions can be processed almost instantly.

The EIP proposes introducing a new synchronous RPC method `eth_sendRawTransactionSync` that combines `eth_sendRawTransaction` and `eth_getTransactionReceipt` into a single yet efficient RPC. It aims to address latency bottlenecks in transaction submission workflows, particularly for blockchains optimized for low latency.

For more detail, please refer to the [EIP](https://github.com/ethereum/EIPs/pull/9890).

## Update Logs

- 2025-06-11. Initial Draft #9890
- 2025-07-24. Add optional client-configured timeouts #10055
- 2025-07-28. Use positive error code 4 #10065
- 2026-01-14. Synchronize timeout parameter type #11074

## FAQs

### Q: Why introduce a synchronous method when async patterns are generally preferred?

**A:** While Ethereum’s 12s blocktime required async patterns to avoid blocking, modern low-latency chains with millisecond blocktimes make synchronous calls practical and beneficial for UX.

### Q: What happens if a transaction takes longer than the timeout period?

**A:** The handler MUST return an error with the transaction hash, allowing fallback to traditional polling. Timeout SHOULD be configurable by node operators.

### Q: Is this compatible with existing Ethereum infrastructure?

**A:** Yes, this is additive. Existing async methods remain unchanged.

### Q: How does this affect node resource usage?

**A:** It reduces overall RPC calls by eliminating repeated `eth_getTransactionReceipt` polling, but requires managing longer-lived HTTP connections (upto a timeout).

### Q: What chains would benefit most from this?

**A:** Latency-optimized chains like RISE, MegaETH, Base, and chains with 100s (or less) of ms blocktimes.

### Q: What about backward-compatibility?

**A:** Fully backward compatible. Existing applications continue working unchanged. Developers opt-in when beneficial.

## Others

- Previous discussion on Ethresearch
- A prototype is being developed in reth:

Issue
- Pull request

## Replies

**wjmelements** (2025-06-23):

Also consider `eth_sendTransaction`.

---

**thnhnv** (2025-06-25):

Thank you for bringing this up, we actually missed it.

---

**fjl** (2025-07-22):

Hi, Felix from go-ethereum here with some comments. We’d like to implement this, but some changes should be made to the EIP:

- Please choose a different, positive, error code for the timeout case. There is no requirement for JSON-RPC errors to be negative.
- The client should be able to supply a maximum timeout value.
- Timeout configuration should not be specified as MUST.

---

**thnhnv** (2025-07-22):

Hi [@fjl](/u/fjl),

Thank you for the inputs. We will revise the EIP accordingly.

---

**MASDXI** (2025-07-23):

[@thnhnv](/u/thnhnv) [@fjl](/u/fjl)

More on behavior

- The minimum timeout should not be below the average network block time. If the minimum timeout is below the default value, it must fall back to using the default instead of returning an error; a reasonable default timeout could be twice the average block time of the blockchain network.
- The maximum value must not exceed the configuration of the node’s transaction pool lifetime, as this would prevent misconfiguration of the node.

---

**thnhnv** (2025-07-24):

Hi [@fjl](/u/fjl) [@MASDXI](/u/masdxi), we have updated the EIP via this [PR](https://github.com/ethereum/EIPs/pull/10055)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fjl/48/5846_2.png) fjl:

> The client should be able to supply a maximum timeout value.
> Timeout configuration should not be specified as MUST.

A new optional client-configured timeout parameter has been added to allow maximum flexibility from the user side.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fjl/48/5846_2.png) fjl:

> Please choose a different, positive, error code for the timeout case. There is no requirement for JSON-RPC errors to be negative.

We found the error codes follow [EIP-1474](https://eips.ethereum.org/EIPS/eip-1474) and [JSON RPC error](https://www.jsonrpc.org/specification#error_object) standards. Can you elaborate more one why error codes should be positive?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/masdxi/48/14155_2.png) MASDXI:

> The minimum timeout should not be below the average network block time. If the minimum timeout is below the default value, it must fall back to using the default instead of returning an error; a reasonable default timeout could be twice the average block time of the blockchain network.

In some blockchains (e.g, MegaETH, RISE, Base), blocks are divided into subblocks which can be as low as a few miliseconds. In these settings, users can get back the receipt as soon as the transaction lands in the block producer’s mempool; this can be at time `start_block + 5ms`, which is far from the blocktime or half of the blocktime. Therefore, we found it not necessary to define a minimum timeout.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/masdxi/48/14155_2.png) MASDXI:

> The maximum value must not exceed the configuration of the node’s transaction pool lifetime, as this would prevent misconfiguration of the node.

A rule has been added to validate this case. However, we still consider two options:

1. In this PR, clients are allowed to submit a timeout, but if this value is not valid (e.g, greater than the node-configured timeout), it will return an error (error code -32602).,
2. Alternative design, nodes can fallback to their default timeout instead of returning an error.

---

**MASDXI** (2025-07-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/thnhnv/48/15496_2.png) thnhnv:

> some blockchains (e.g, MegaETH, RISE, Base), blocks are divided into subblocks which can be as low as a few miliseconds. In these settings, users can get back the receipt as soon as the transaction

It appears to be too specific for the L2, which is constantly producing blocks. What if L1 takes more than a second and L2 doesn’t produce an empty block? Some networks produce a block only when the transaction arrives, wait until timeout, and then seal the block (not a sub-block)?

---

**fjl** (2025-07-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/thnhnv/48/15496_2.png) thnhnv:

> In this PR, clients are allowed to submit a timeout, but if this value is not valid (e.g, greater than the node-configured timeout), it will return an error (error code -32602).,

The server can always impose a shorter timeout than specified by just returning the timeout error. So there is no need to validate the timeout given by the client. The client timeout just provides a hint to the server about the maximum time that the client is willing to wait.

---

**fjl** (2025-07-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/thnhnv/48/15496_2.png) thnhnv:

> We found the error codes follow EIP-1474 and JSON RPC error standards. Can you elaborate more one why error codes should be positive?

EIP-1474 is not canonical, it is just a proposal submitted a long time ago.

Regarding error ranges listed by the JSON-RPC specification itself, they are defined for use by the JSON-RPC server implementation library. The specification explicitly puts all predefined errors into the negative integer range so that the entire range of positive integers is available for application-level codes. [It says](https://www.jsonrpc.org/specification#error_object):

> The error codes from and including -32768 to -32000 are reserved for pre-defined errors.
> … The remainder of the space is available for application defined errors.

Unfortunately, due to this being a common misunderstanding, some Ethereum APIs return negative codes in the -32000 to -32099 range. And the default error code returned by most servers is negative (it’s similar to HTTP 500 Internal Server Error), so some people assumed all errors must be in that range. But it’s false, we can define any error.

I would suggest we use code `4` for this.

---

**thnhnv** (2025-07-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/masdxi/48/14155_2.png) MASDXI:

> It appears to be too specific for the L2, which is constantly producing blocks. What if L1 takes more than a second and L2 doesn’t produce an empty block? Some networks produce a block only when the transaction arrives, wait until timeout, and then seal the block (not a sub-block)?

I would say in these cases, if users supply a too-short timeout, they will get timeout very frequently, and will adjust their timeout accordingly.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fjl/48/5846_2.png) fjl:

> The server can always impose a shorter timeout than specified by just returning the timeout error. So there is no need to validate the timeout given by the client. The client timeout just provides a hint to the server about the maximum time that the client is willing to wait.

Yes, this seems to be better in terms of UX.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fjl/48/5846_2.png) fjl:

> Unfortunately, due to this being a common misunderstanding, some Ethereum APIs return negative codes in the -32000 to -32099 range. And the default error code returned by most servers is negative (it’s similar to HTTP 500 Internal Server Error), so some people assumed all errors must be in that range. But it’s false, we can define any error.

Seems legit to us.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fjl/48/5846_2.png) fjl:

> I would suggest we use code 4 for this.

Did you mean the `errCode=4` or `errCode=4xxx`?

---

**fjl** (2025-07-25):

I mean literally number four.

---

**LukaszRozmej** (2025-09-21):

I don’t really like it. What I would prefer is a new subscription over eth_subscribe, that would:

- If transaction already included - return the data
- If not included return the transaction data as soon as it is included
- If transaction was included but was reorged it could return information that it is no longer included (this last one could be a parameter for subscription if this should be monitored if not we could close subscription as soon as tx is included. If we need to monitor we can close subscription as soon as transaction hits finalized)

Already a proven battle-tested mechanism that works well regardless of slot times.

Also one web socket connection can support subscriptions for multiple transactions easily reducing potential connection-hogging of single RPC peer.

---

**cyberdrk** (2025-09-30):

Why does it need to be `eth_sendRawTransactionSync` not `eth_sendTransactionSync`?

---

**AjayiMike** (2025-11-10):

I love this!

But while the specification notes that non-implementing nodes will return a ‘method not found’ error, this relies on a reactive, error-based approach for feature detection. Would you consider recommending a more explicit discovery mechanism? For example, adding a method like `rpc_modules` or a similar endpoint that lists supported non-standard methods like `eth_sendRawTransactionSync` . This would allow applications to check for support proactively rather than reactively.

---

**a26nine** (2026-01-08):

Should the timeout be `hex` or `int`? The draft is inconsistent—the parameters table specifies `QUANTITY`(hex), but the example uses int. Many client implementations don’t support hex, which breaks tools like *viem*.

---

**thnhnv** (2026-01-14):

Thank you for reporting, it should be `int`.


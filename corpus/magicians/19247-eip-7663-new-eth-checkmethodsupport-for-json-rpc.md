---
source: magicians
topic_id: 19247
title: "EIP-7663: New `eth_checkMethodSupport` for JSON-RPC"
author: Sileo
date: "2024-03-18"
category: EIPs
tags: [eip, json-rpc]
url: https://ethereum-magicians.org/t/eip-7663-new-eth-checkmethodsupport-for-json-rpc/19247
views: 1158
likes: 5
posts_count: 4
---

# EIP-7663: New `eth_checkMethodSupport` for JSON-RPC

[github.com/ethereum/execution-apis](https://github.com/ethereum/execution-apis/pull/533)














####


      `main` ← `0xSileo:add-check-method-support`




          opened 11:54AM - 07 Apr 24 UTC



          [![](https://avatars.githubusercontent.com/u/127872023?v=4)
            0xSileo](https://github.com/0xSileo)



          [+34
            -0](https://github.com/ethereum/execution-apis/pull/533/files)







Moves [EIP 7663](https://github.com/ethereum/EIPs/pull/8355) to this repo. The d[…](https://github.com/ethereum/execution-apis/pull/533)iscussion about this addition's necessity and other details is available on [Ethereum magicians](https://ethereum-magicians.org/t/eip-7663-create-an-eth-supportsmethod-method-for-json-rpc/19247) .

I'm less familiar with yaml and JSON schema, so I did my best and feel free to help. Unsure if I should add tests, as it's not implemented in clients yet. Also, ideally, we should change the params from a `methodName` array to an enum of all existing methods, and the `result` should use that as well.












# Please see the linked PR

Keeping the original post below :

# Context

Not every node supports all JSON-RPC methods and there is currently no way to get a list of methods supported by a specific node (or provider/endpoint). Also, querying the node is the only way to find out if a specific method is supported.

This leads to a few issues :

- It can take a while to find a node supporting a specific method, as trial-and-error is needed. I had to query 8 providers before finding one which supported the new eth_blobBaseFee.
- RPC providers may have to add the supported methods in their docs, which not all do and is redundant.
- Trial-and-error does not scale well for more than one method. If the user wants to find a provider supporting n methods, they’ll have to query each provider n times.

# Proposal

I suggest adding a `eth_checkMethodSupport` method, which takes a list of method strings (or signatures) as a parameter and outputs a list of booleans, corresponding to whether the provider implements it. A special case is reserved if the list is empty, and the provider would return the list of all supported methods.

This is similar to the `supportsInterface(bytes4)(bool)` interface in [EIP-165](https://eips.ethereum.org/EIPS/eip-165).

The result can be a list without loss of information and with no ambiguity but we could decide on giving a JSON as result, as this would make the returned type consistent whether we query for all methods or for specific ones. Open for discussion.

There is a special case for the `eth_checkMethodSupport` itself, for completeness’ sake I’d suggest including it but on the other hand, it’s not really needed. I believe this would be the only “required” method, but I’m not sure that the protocol can enforced. That’s also open for discussion.

# New use cases arising

- Implementing this would make the creation of tools like provider dashboards possible (one can filter by methods needed).
- It would also pave the way to a more general standard for modular method support (I don’t know if it’s currently easy to do from a nodes’ perspective, I’ll spin up some and try on the clients.). Nodes could become hyperspecific (supporting a handful of methods), or more complete, as well as making it easy to change privileges (e.g. for paying users vs free tiers).
- Dynamic node querying would become easier. Now the balance can be queried on node A and the base fee on node B, without trying on one then the other.

# Closing word

I hope you get the idea, I’m not sure if this has been discussed before, and I genuinely think it could be a useful addition.

# Examples

Suppose a node only supports `eth_blockNumber` and `eth_blobBaseFee`. Querying it would give :

### Example 1

#### Query

```json
{
  "jsonrpc":"2.0",
  "id":1,
  "method":"eth_checkMethodSupport",
  "params":["eth_blockNumber", "eth_send", "eth_blobBaseFee"]
}
```

#### Response

```json
{
  "jsonrpc":"2.0",
  "id":1,
  "result":[true,false,true],
}
```

### Example 2

#### Query

```json
{
  "jsonrpc":"2.0",
  "id":1,
  "method":"eth_checkMethodSupport",
  "params":[]
}
```

could return

#### Response

```json
{
  "jsonrpc":"2.0",
  "id":1,
  "method":"eth_checkMethodSupport",
  "result":["eth_blockNumber", "eth_blobBaseFee", "eth_checkMethodSupport"]
}
```

## Replies

**wighawag** (2024-03-21):

Thanks [@Sileo](/u/sileo) for binging this EIP

I think it make sense.

If we can’t have all node implementation implement all methods, then we should have a way to query which methods are supported.

I would of course prefers if all node implementation could agree on what methods are mandatory, but there might be other concerns that make this impossible. Thinking in particular of `eth_newFilter` which might not be implementable in load-balanced node where they do not want to keep track of any state.

My only comment is that I am not sure it is a good idea to have a function call have 2 different return type. Might be cleaner to have 2 method instead like `eth_supportsMethod` and `eth_listSupportedMethods`

---

**0xpolarzero** (2024-03-22):

Agree with that proposal, and the fact that it might be clearer to have 2 separate methods for the different return types.

To add context—another pain point—[here is an issue](https://github.com/NomicFoundation/hardhat/issues/3345) with Hardhat node not supporting `eth_getProof`, which was actually implemented 3 weeks ago.

Which was causing a problem with [Tevm](https://github.com/evmts/tevm-monorepo) when forking a Hardhat node, since `Tevm.getAccount()` would use `eth_getProof` to retrieve the state of an account.

Not sure if it helps, but at least this is one instance where it might have been useful to have the method available.

---

**Sileo** (2024-03-26):

I have received a bit of feedback in DMs, here are some points that were raised, and I invite you to discuss those :

#### Creating a supportsMethod isn’t necessary (but getSupportedMethods is)

- Argument: One could just post the query and check if the enpoint returns a “method not supported” error.
- My feedback: While it’s true, I think the main advantage to bringing supportsMethod is removing the need to prepare (and transmit) data for the call. Likewise, the endpoint doesn’t have to perform any heavy operation (reading the state etc). Furthermore, it can also be economiaclly better : testing eth_sendTransaction by sending a tx is just not optimal at all.

#### Create two methods (as discussed in this thread)

- Argument : Querying for all supported methods, or checking if a finite set of methods is supported would be answered with different types, thus needing two separate methods
- My feedback : Why not, but I could see this : a single eth_checkMethodSupport method returning a json object with {“methodName1” : boolean , … }. If the param list is empty, return the json for all supported methods, and if it’s a list of method names to check, return the json for those instead.

#### Add

- Argument: EIP-1767 has been stagnant and adding a supports1767 method could be in the scope of this EIP.
- My feedback : That EIP looks interesting and analoguous to this one, but I don’t know much about it. However, it brings an point I want to put forward as well. See the last paragraph.

#### Namespace

- This wasn’t really feedback but a quesion of mine, I assume it would be in the eth_ namespace but should it check availability outside the eth_ namespace as well (debug_ or engine_) ? I’m in favour of it but if there’s any counterpoint, let me know.

### I believe an effort could be made to move towards a modular node architecture

Where we could see which RPC methods are supported, as well as which EIPs (if related to nodes), and node runners could easily opt-in or out of selected ones. Similarly, many go with the default client configurations and relay -or censor- transactions and it would be an interesting addition to make it easily configurable. Indeed, it is my right as a node runner (be it tx relayer or validator) to not relay monkeyjpegs-related transactions, and make more space for others (imagine a node relaying only [type-3 txs](https://eips.ethereum.org/EIPS/eip-4844) or only eth transfers). Of course, the more economically-sound decision would be to validate txs independently of what it carries, but this could incentivize some teams to run specialized nodes, that only relay their smart contract’s tx. We could also argue for a fragmented state. Anyway, this is getting out of this EIP’s scope.


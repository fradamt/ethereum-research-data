---
source: magicians
topic_id: 16184
title: "EIP idea: eth_signUserOperation RPC"
author: wilsoncusack
date: "2023-10-20"
category: EIPs
tags: [wallet, account-abstraction, eip-4337, rpc]
url: https://ethereum-magicians.org/t/eip-idea-eth-signuseroperation-rpc/16184
views: 3434
likes: 16
posts_count: 33
---

# EIP idea: eth_signUserOperation RPC

It seems that signing EIP-4337 user operations is underspecified, and this has led to most implementations leveraging personalSign (starting with the [reference implementation](https://github.com/eth-infinitism/account-abstraction/blob/main/contracts/samples/SimpleAccount.sol#L110C1-L110C1)). Using personalSign is not ideal, for a couple of reasons.

1. personalSign was introduced so that users could have confidence they weren’t signing a transaction.

> That means that any signed_data cannot be one RLP-structure, but a 1-byte RLP payload followed by something else. Thus, any EIP-191 signed_data can never be an Ethereum transaction.

As user operations *are* effectively transactions, which can spend the users fund, it seems we have taken a step backwards. Users can be tricked into signing a user operation that steals all their funds. Wallets do not show warnings on personalSign, even when signing 32 bytes which could be a transaction hash, because they presume the prefix makes it safe for users. For user operations, it is not safe.

1. Using personalSign makes it near impossible for wallets to tell users what they are signing. Seemingly, this hasn’t been a huge issue to date because generally either

Dapps leveraging 4337 have embedded wallets, and so they dapp itself is the wallet and can tell the user whatever info about what they are signing.
2. The wallet is receiving eth_sendTransaction requests and turning them into user operations, so the user’s wallet can show the user all they need to know about the transaction.

This all makes sense, but constrains how 4337 can be used. For example, I may have a wallet that leverages 4337 and be interacting with a dapp that does, as well. Suppose the dapp has its own paymaster, which my wallet knows nothing about, and wants to include the paymaster and signature in the request sent to the wallet. Perhaps the dapp wants to set some of the user operation gas values, and help the wallet with things it may not be aware of. Currently there is no way to do these things.

Beyond this, we can also say there is currently no good way for existing EOA wallets to serve as a signer for 4337 accounts, because the EOA wallet cannot show any helpful info when signing. Signing 32 bytes of hex via personalSign should not be acceptable.

I propose a new RPC, `eth_signUserOperation`

```auto
inputs: {
  userOperation: UserOperation,
  entryPoint: address,
  chainId: bytes,
}
output: {signature: bytes}
```

We can also use this opportunity to specify how exactly the user operation should be hashed, as the industry seems to have a convention that is not in the EIP.

`userOpHash = keccak256(abi.encode(hashedUserOperation, entryPoint, chainId))`

where

```auto
hashedUserOperation = (
  abi.encode(
      sender,
      nonce,
      keccak256(initCode),
      keccak256(callData),
      callGasLimit,
      verificationGasLimit,
      preVerificationGas,
      maxFeePerGas,
      maxPriorityFeePerGas,
      keccak256(paymasterAndData),
  )
)
```

Thanks for reading, and I welcome feedback. If this makes sense to others, and I am not missing something obvious, we can turn this into a formal EIP.

## Replies

**joaquim-verges** (2023-10-20):

> Signing 32 bytes of hex via personalSign should not be acceptable.

this. so much this.

there is no way we could recommend using 4337 with an existing wallet like MM or CB wallet because of this. UX is terrible. The only reasonable solution was to hide this uglyness away with an embedded/local wallet.

Definitely think a standard scheme for userOp signing operations is necessary.

---

**SamWilsn** (2023-10-21):

I’d like to see a [JSON Schema](https://json-schema.org/) definition for the parameters of `eth_signUserOperation`. These things always end up underspecified and have slight differences between wallets.

For example:

- Does the dapp have to provide the nonce, or does the wallet figure that out? Would it be useful to support both?
- Can chainId be omitted? If so, does that mean “create a UserOperation that can work on multiple chains” or “use the currently active chain in the wallet”?
- Does the dapp have to provide callGasLimit/verificationGasLimit/preVerificationGas/maxFeePerGas/maxPriorityFeePerGas?

---

Is [eth_signTypedData](https://eips.ethereum.org/EIPS/eip-712) sufficient? Can we standardize a signature format using that, and not create a new RPC endpoint, or is there information in the `UserOperation` that only the wallet would know?

Not saying this is the correct approach, but I wanted to raise it as an option.

---

Is it important to define how to hash the `UserOperation`? That seems like it only matters between the account/aggregator and the wallet doing the signing.

---

**wilsoncusack** (2023-10-21):

Thanks!

1.

> I’d like to see a JSON Schema definition

ack will do

1.

> Can chainId be omitted? If so, does that mean “create a UserOperation that can work on multiple chains” or “use the currently active chain in the wallet”?

EIP 4337 States

> To prevent replay attacks (both cross-chain and multiple EntryPoint implementations), the signature should depend on chainid and the EntryPoint address.

1.

Taking these two together

> Does the dapp have to provide the nonce, or does the wallet figure that out? Would it be useful to support both?

> Does the dapp have to provide callGasLimit/verificationGasLimit/preVerificationGas/maxFeePerGas/maxPriorityFeePerGas?

I think it would work like eth_sendTransaction where dapps *can* specify these things but the wallet will fill in if they are not specified? But this should be specified. I also wonder if we want an eth_sendUserOperation RPC.

1.

> Is eth_signTypedData sufficient? Can we standardize a signature format using that, and not create a new RPC endpoint, or is there information in the UserOperation that only the wallet would know?

This should be considered, but I don’t think is the right solution. Wallets get a  lot of typed signature requests. If the wallet has to parse to check whether it is a userOp, i.e. effectively a transaction, and then show it as such, that seems broken to me. It suggests this should have a dedicated RPC so that the wallet’s know what it is and can treat appropriately.

Also, as I said in the OP, I don’t think we should be using `"\x19Ethereum Signed Message:\n"` prefixed transactions for spending. Though I realize this is already being abused in many ways: permit, existing 4337 accounts, Safe multisigs, etc.

I actually first started with going with typed signatures but (1) it’s very annoying because it doesn’t match current hashing conventions, and so you can’t use the userOpHash passed to your account but instead have to rehash, in the typed format, the userOp with the chainId and entrypoint, which is not ideal for gas.  And then (2) again just feel a new RPC is justified here. EIP 4337 creates many new RPCs. I think having a new wallet RPC for what is essentially a new transaction signing flow is reasonable.

1.

> Is it important to define how to hash the UserOperation ? That seems like it only matters between the account/aggregator and the wallet doing the signing.

This could be left out, but it seems helpful to align on given wallets will have to hash and want to know how? Currently technically this varies by entrypoint, can see [here](https://github.com/eth-infinitism/account-abstraction/blob/main/contracts/core/EntryPoint.sol#L263). But practically basically everyone is using the same entrypoint.

---

**SamWilsn** (2023-10-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> EIP 4337 States
>
>
>
> To prevent replay attacks (both cross-chain and multiple EntryPoint implementations), the signature should depend on chainid and the EntryPoint address.

The “should” there is doing a lot of work. I can imagine some use cases where you’d want the same transaction to be replayable on multiple chains (eg. universal `CREATE2` deployers.) I’d maybe make the `chainId` field a tristate (exactly, wallet-chosen, and omitted), where wallet-chosen is the default if null/undefined.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> I also wonder if we want an eth_sendUserOperation RPC

I’m usually in favour of having separate send-, sendRaw-, and sign-style endpoints.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> Wallets get a lot of typed signature requests. If the wallet has to parse to check whether it is a userOp, i.e. effectively a transaction, and then show it as such, that seems broken to me.

Wouldn’t this be as simple as checking the `domainSeparator`?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> Though I realize this is already being abused

I would hardly call this an abuse. With the domain separator and the information it encodes, EIP-712 is pretty well suited to on-chain authorizations.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> it’s very annoying because it doesn’t match current hashing conventions, and so you can’t use the userOpHash passed to your account but instead have to rehash

Is the preimage of `userOpHash` specified somewhere? Again, sorry, I only follow ERC-4337 at extreme distance ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> I think having a new wallet RPC for what is essentially a new transaction signing flow is reasonable.

I don’t disagree! I just want to make sure EIP-712 gets due consideration. It does have advantages (eg. will work even without explicit wallet support), but it also has its drawbacks (eg. dapp has to compute the full `UserOperation` including nonce/gas/etc.)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> This could be left out, but it seems helpful to align on given wallets will have to hash and want to know how? Currently technically this varies by entrypoint, can see here . But practically basically everyone is using the same entrypoint.

It doesn’t seem like `getUserOpHash` is specified in ERC-4337 (at least I couldn’t CTRL-F it.) `eth_signUserOperation` probably should only depend on the standard functions from the specification, no?

---

On another note, should `nonce` be represented in the RPC endpoint as `key` and `sequence`, or just a single `nonce` field, or should it allow both representations?

---

**wilsoncusack** (2023-10-22):

Appreciate all the feedback! Maybe we should get a call or something next week to hash out?

I think I’d prefer to follow EIP 155 and keep transactions chain specific. I think that the contracts should enforce this for the user, as they do today.

And yeah checking domain separator is not difficult but feels annoying and a little hacky. You bring up an even better point, that this path doesn’t allow wallets to edit the user op/dapp has to compute more.

> Is the preimage of userOpHash specified somewhere? Again, sorry, I only follow ERC-4337 at extreme distance

> It doesn’t seem like getUserOpHash is specified in ERC-4337 (at least I couldn’t CTRL-F it.) eth_signUserOperation probably should only depend on the standard functions from the specification, no?

Part of what I am saying is that the spec for computing a 4337 user op hash is notably missing from the original EIP and is possibly worth being explicit about in this extension. Currently you have to check the entrypoint you are using to see how it hashes.

> On another note, should nonce be represented in the RPC endpoint as key and sequence , or just a single nonce field, or should it allow both representations?

The spec I have proposed is that the RPC takes the whole user operation, and the user operation includes the nonce. Was thinking if the nonce was present, the wallet would know not to touch. I need to look a little closer at how this works between dapps and wallets today with send/signTransaction: I guess I assume by default the dapps omit the nonce and the wallet fills in?

But you bring up an interesting point: should the wallet check whether nonce is only 192 bits, and is just a key, and the wallet then needs to specify the sequence? (I hope I am understanding you correctly.)

---

**SamWilsn** (2023-10-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> I think I’d prefer to follow EIP 155 and keep transactions chain specific. I think that the contracts should enforce this for the user, as they do today.

I think the choice of whether to enforce a chain id or not should be up to the user, with the default being enforce. We’re building an RPC endpoint that’ll be used by not only today’s applications, but future ones as well. The more general-purpose we can be, the better.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> Part of what I am saying is that the spec for computing a 4337 user op hash is notably missing from the original EIP and is possibly worth being explicit about in this extension. Currently you have to check the entrypoint you are using to see how it hashes.

If it is possible to build this endpoint in a hash-agnostic way, we should. The more control we give to wallet developers and dapps, the more innovation we enable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> I guess I assume by default the dapps omit the nonce and the wallet fills in?

Pretty much!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> But you bring up an interesting point: should the wallet check whether nonce is only 192 bits, and is just a key, and the wallet then needs to specify the sequence? (I hope I am understanding you correctly.)

Maybe we do a [oneOf](https://json-schema.org/understanding-json-schema/reference/combining#oneof) that accepts:

- {"key": "0x1", ...}
- {"sequence": "0x1", ...}
- {"sequence": "0x1", "key": "0x1", ...}
- {"nonce": "0x1", ...}
- {...}

Whatever the dapp omits, the wallet fills in.

---

**ajhodges** (2023-10-23):

On the topic of requiring chainId - +1 that it should maybe be optional. I feel like multichain smart contract wallets may commonly want to broadcast signed userops to multiple chains to keep settings in sync.

Although I suppose this could also be accomplished by ‘lazily’ syncing these settings via batched userops

---

**wilsoncusack** (2023-10-23):

I don’t really understand how the user would “decide”, and I do think this would violate the original 4337 spec.

If the user “decides” by just signing a hash without the chainId, this feels like a footgun. Now a dapp or wallet can trick the user into signing such a message. Post 155, nodes will reject transactions without chains IDs. I think the smart account rejecting signatures that don’t include chain IDs is probably the only way to really protect the user.

---

**wilsoncusack** (2023-10-23):

Though, thinking a little more, I suppose it is on the user to use a wallet that they trust. And the wallet could clearly display this choice. But still would lean against for now as I feel would violate original EIP

> To prevent replay attacks (both cross-chain and multiple EntryPoint implementations), the signature should depend on chainid and the EntryPoint address.

---

**ajhodges** (2023-10-23):

I was thinking that (in a hypothetical Wallet) most/all user-originated userops would include chainId, but the wallet would be allowed omit chainId if the userop was i.e. an account recovery operation. Not all nodes enforce EIP-155, so it’s already kind of up to Wallets to enforce 155 anyways.

---

**wilsoncusack** (2023-10-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Maybe we do a oneOf that accepts:
>
>
> {"key": "0x1", ...}
> {"sequence": "0x1", ...}
> {"sequence": "0x1", "key": "0x1", ...}
> {"nonce": "0x1", ...}
> {...}
>
>
> Whatever the dapp omits, the wallet fills in.

hmm are you imagining these would be specified in the UserOp object or outside it? I’d prefer to keep the API simpler if we can. Can we not just do

- nonce not present in request = wallet set key and sequence
- nonce = 192 bits, key and sequence are set, don’t change.

Implied, there is no way for dapp to only set sequence. Not sure if that’s any loss ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

---

**SamWilsn** (2023-10-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> Post 155, nodes will reject transactions without chains IDs.

From EIP-155:

> The currently existing signature scheme using v = 27 and v = 28 remains valid and continues to operate under the same rules as it did previously.

---

**SamWilsn** (2023-10-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> hmm are you imagining these would be specified in the UserOp object or outside it?

Whichever makes more sense. Probably inside.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> I’d prefer to keep the API simpler if we can. Can we not just do
>
>
> nonce not present in request = wallet set key and sequence
> nonce  nonce >= 192 bits, key and sequence are set, don’t change.

The difference between

```json
{
    "nonce": "0x000000000000000000000000000000000000000000000001",
}
```

and

```json
{
    "nonce": "0x0000000000000000000000000000000000000000000000001",
}
```

Is **way** too subtle for my taste. I’d prefer to be explicit about it with different keys.

---

**wilsoncusack** (2023-10-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Is way too subtle for my taste. I’d prefer to be explicit about it with different keys.

Ok, fair. I’d probably want to think about changing the API I proposed then. I’d expect all the fields inside UserOperation to match the 4337 definition. Maybe we don’t nest anything, then. Could look like

```auto
input: {...allUserOperationFields, key:, ...., chainId, entryPoint}
```

---

**SamWilsn** (2023-10-23):

I think this is a good point to have that JSON Schema, so we can discuss the API exactly.

---

**wilsoncusack** (2023-10-25):

How’s this? Currently saying only `sender` is strictly required.

```auto
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Sign User Operation Request",
  "type": "object",
  "properties": {
    "sender": {
      "description": "The account making the operation",
      "$ref": "#/definitions/address"
    },
    "nonce": {
      "description": "key and sequence combined into a single value, can be used to enforce transaction ordering and uniqueness",
      "$ref": "#/definitions/uint256"
    },
    "key": {
      "description": "nonce key which corresponds a distinct sequence value space",
      "$ref": "#/definitions/uint192"
    },
    "sequence": {
      "description": "nonce sequence value to use with the given key",
      "$ref": "#/definitions/uint64"
    },
    "initCode": {
      "description": "The initCode of the account (needed if and only if the account is not yet on-chain and needs to be created)",
      "$ref": "#/definitions/bytes"
    },
    "callData": {
      "description": "The data to pass to the sender during the main execution call",
      "$ref": "#/definitions/bytes"
    },
    "callGasLimit": {
      "description": "The amount of gas to allocate the main execution call",
      "$ref": "#/definitions/uint256"
    },
    "verificationGasLimit": {
      "description": "The amount of gas to allocate for the verification step",
      "$ref": "#/definitions/uint256"
    },
    "preVerificationGas": {
      "description": "The amount of gas to pay for to compensate the bundler for pre-verification execution, calldata and any gas overhead that can’t be tracked on-chain",
      "$ref": "#/definitions/uint256"
    },
    "maxFeePerGas": {
      "description": "Maximum fee per gas (similar to EIP-1559 max_fee_per_gas)",
      "$ref": "#/definitions/uint256"
    },
    "maxPriorityFeePerGas": {
      "description": "Maximum priority fee per gas (similar to EIP-1559 max_priority_fee_per_gas)",
      "$ref": "#/definitions/uint256"
    },
    "paymasterAndData": {
      "description": "Address of paymaster sponsoring the transaction, followed by extra data to send to the paymaster (empty for self-sponsored transaction)",
      "$ref": "#/definitions/bytes"
    },
    "chainId": {
      "description": "The ID for the chain on which the operation should be valid",
      "type": "number"
    },
    "entrypoint": {
      "description": "The entrypoint which the bundler must use for this operation.",
      "$ref": "#/definitions/address"
    },
  },
  "required": [
    "sender"
  ],
  "oneOf": [
    {
      "required": [
        "nonce"
      ]
    },
    {
      "required": [
        "sequence"
      ]
    },
    {
      "required": [
        "key"
      ]
    },
    {
      "required": [
        "sequence",
        "key"
      ]
    },
    {
      "not": {
        "anyOf": [
          {
            "required": [
              "sequence"
            ]
          },
          {
            "required": [
              "nonce"
            ]
          },
          {
            "required": [
              "key"
            ]
          }
        ]
      }
    }
  ],
  "definitions": {
    "address": {
      "type": "string",
      "pattern": "^0x[a-fA-F0-9]{40}$"
    },
    "uint256": {
      "type": "string",
      "pattern": "^0x[a-fA-F0-9]{64}$"
    },
    "uint192": {
      "type": "string",
      "pattern": "^0x[a-fA-F0-9]{48}$"
    },
    "uint64": {
      "type": "string",
      "pattern": "^0x[a-fA-F0-9]{16}$"
    },
    "bytes": {
      "type": "string",
      "pattern": "^0x[a-fA-F0-9]*$"
    }
  }
}
```

---

**SamWilsn** (2023-10-25):

That looks pretty good! Do we also need a schema for what the wallet returns from this function?

I have a few more comments, but I think you’re ready to open an EIP pull request.

---

`chainId` should be a `uint256`, or at the very least, a ["type": "integer"](https://json-schema.org/understanding-json-schema/reference/numeric#integer) with ["minimum": 0](https://json-schema.org/understanding-json-schema/reference/numeric#range).

---

To make things a bit more user friendly, I’d change all your numeric `pattern`s to allow ranges of lengths. For example:

```json
"uint256": {
    "type": "string",
    "pattern": "^0x[a-fA-F0-9]{1,64}$"
},
```

There’s probably a case to be made for also allowing `{"type": "integer", "maximum": 9007199254740991, "minimum": 0}` but that might be adding too much complexity.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wilsoncusack/48/10753_2.png) wilsoncusack:

> Currently saying only sender is strictly required.

What is a wallet supposed to do with a request like:

```json
{ "sender": "0xbB2e10BDccFD1CdECF4cED3A5Fdb8A2c9EB4624c" }
```

?

I feel like that’s an important part of the standard ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=12)

---

I believe this should be valid:

```json
{
    "sender": "0xbB2e10BDccFD1CdECF4cED3A5Fdb8A2c9EB4624c",
    "key": "0xbB2e10BDccFD1CdECF4cED3A5Fdb8A2c9EB4624cbB2e10BD",
    "sequence": "0x0000000000000000"
}
```

But I get:

> Message: JSON is valid against more than one schema from ‘oneOf’. Valid schema indexes: 1, 2, 3.
> Schema path: #/oneOf
>
>
> Message: JSON is valid against schema from ‘not’.
> Schema path: #/oneOf/4/not
>
>
> Message: Required properties are missing from object: nonce.
> Schema path: #/oneOf/0/required

---

Is there a meaningful difference between a zero length `initCode` (i.e. `"initCode": "0x"`) and not including `initCode` at all? Like is the wallet expected to fill in `initCode` when the key is absent?

Actually, does it make any sense for the dapp to provide the `initCode` ever? That seems like a wallet-specific thing.

---

**wilsoncusack** (2023-10-26):

> I have a few more comments, but I think you’re ready to open an EIP pull request.

Great, will do! To be clear, it sounds like we want all of

- eth_sendUserOperation
- eth_signUserOperation
- eth_sendRawUserOperation

> chainId should be a uint256, or at the very least, a "type": "integer" with "minimum": 0.

ack

> To make things a bit more user friendly, I’d change all your numeric pattern s to allow ranges of lengths.

hmm ok yeah fair.

> I feel like that’s an important part of the standard

lol you were asking to keep options open, so I want full out! Presumably in this case

- wallet sets nonce
- wallets sets entry point
- calldata is 0x
- wallet sets all gas
- wallet decides init code
- wallet sets chainID or decides not to make part of signature

Suppose we can translate these into various MUST definitions in the EIP?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I believe this should be valid:

Apologies! Took a bit of work but think I got it. Allowing a sequence number with no key feels a bit off to me, but curious what others thing.

```auto
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Sign User Operation Request",
  "type": "object",
  "properties": {
    "sender": {
      "description": "The account making the operation",
      "$ref": "#/definitions/address"
    },
    "nonce": {
      "description": "key and sequence combined into a single value",
      "$ref": "#/definitions/uint256"
    },
    "key": {
      "description": "nonce key which corresponds to a unique set of sequence",
      "$ref": "#/definitions/uint192"
    },
    "sequence": {
      "description": "nonce sequence value to use with the given key",
      "$ref": "#/definitions/uint64"
    },
    "initCode": {
      "description": "The initCode of the account (needed if and only if the account is not yet on-chain and needs to be created)",
      "$ref": "#/definitions/bytes"
    },
    "callData": {
      "description": "The data to pass to the sender during the main execution call",
      "$ref": "#/definitions/bytes"
    },
    "callGasLimit": {
      "description": "The amount of gas to allocate the main execution call",
      "$ref": "#/definitions/uint256"
    },
    "verificationGasLimit": {
      "description": "The amount of gas to allocate for the verification step",
      "$ref": "#/definitions/uint256"
    },
    "preVerificationGas": {
      "description": "The amount of gas to pay for to compensate the bundler for pre-verification execution, calldata and any gas overhead that can’t be tracked on-chain",
      "$ref": "#/definitions/uint256"
    },
    "maxFeePerGas": {
      "description": "Maximum fee per gas (similar to EIP-1559 max_fee_per_gas)",
      "$ref": "#/definitions/uint256"
    },
    "maxPriorityFeePerGas": {
      "description": "Maximum priority fee per gas (similar to EIP-1559 max_priority_fee_per_gas)",
      "$ref": "#/definitions/uint256"
    },
    "paymasterAndData": {
      "description": "Address of paymaster sponsoring the transaction, followed by extra data to send to the paymaster (empty for self-sponsored transaction)",
      "$ref": "#/definitions/bytes"
    },
    "chainId": {
      "description": "The ID for the chain on which the operation should be valid",
      "type": "number"
    },
    "entrypoint": {
      "description": "The entrypoint which the bundler must use for this operation.",
      "$ref": "#/definitions/address"
    }
  },
  "required": [
    "sender"
  ],
  "oneOf": [
    {
      "required": [
        "nonce"
      ],
      "not": {
        "anyOf": [
          {
            "required": [
              "sequence"
            ]
          },
          {
            "required": [
              "key"
            ]
          }
        ]
      }
    },
    {
      "required": [
        "sequence"
      ],
      "not": {
        "anyOf": [
          {
            "required": [
              "nonce"
            ]
          },
          {
            "required": [
              "key"
            ]
          }
        ]
      }
    },
    {
      "required": [
        "key"
      ],
      "not": {
        "anyOf": [
          {
            "required": [
              "nonce"
            ]
          },
          {
            "required": [
              "sequence"
            ]
          }
        ]
      }
    },
    {
      "required": [
        "sequence",
        "key"
      ],
      "not": {
        "required": [
          "nonce"
        ]
      }
    }
  ],
  "definitions": {
    "address": {
      "type": "string",
      "pattern": "^0x[a-fA-F0-9]{40}$"
    },
    "uint256": {
      "type": "string",
      "pattern": "^0x[a-fA-F0-9]{64}$"
    },
    "uint192": {
      "type": "string",
      "pattern": "^0x[a-fA-F0-9]{48}$"
    },
    "uint64": {
      "type": "string",
      "pattern": "^0x[a-fA-F0-9]{16}$"
    },
    "bytes": {
      "type": "string",
      "pattern": "^0x[a-fA-F0-9]*$"
    }
  }
}
```

---

**SamWilsn** (2023-10-26):

Haven’t gone through your whole post yet, but would this work:

```json
  "oneOf": [
    {
      "required": [
        "nonce"
      ],
      "properties": {
        "key": false,
        "sequence": false
      }
    },
    {
      "required": [
        "key",
        "sequence"
      ],
      "properties": {
        "nonce": false
      }
    }
  ]
```

---

**wilsoncusack** (2023-10-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Haven’t gone through your whole post yet, but would this work:
>
>
>
> ```auto
>
> ```

Sorry, do you mean just not allowing sequence to be passed alone? I think that could make sense. Probably key can still be passed alone though.


*(12 more replies not shown)*

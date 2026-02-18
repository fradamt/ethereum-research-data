---
source: magicians
topic_id: 4880
title: "EIP-3074: AUTH and AUTHCALL opcodes"
author: SamWilsn
date: "2020-10-28"
category: EIPs > EIPs core
tags: [opcodes, meta-transactions, eip-3074]
url: https://ethereum-magicians.org/t/eip-3074-auth-and-authcall-opcodes/4880
views: 29139
likes: 163
posts_count: 247
---

# EIP-3074: AUTH and AUTHCALL opcodes

[Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3074)





###



Allow externally owned accounts to delegate control to a contract.










> Creates a new precompile, analogous to CALL, that sets CALLER based on an ECDSA signature.
>
>
> This EIP creates two precompiles:
>
>
> CALL_PRECOMPILE - forwards a CALL, setting msg.sender according to an ECDSA signature, using a relayer-sponsee nonce for replay protection.
> NONCE_PRECOMPILE - provides access to relayer-sponsee nonces expected by CALL_PRECOMPILE.

## Replies

**sergio_lerner** (2020-11-02):

The proposal has several problems, the two most important are:

- It’s incompatible with EIP-712 and the mapping selected could be used to confuse existing wallets into signing an unintended message.
- It doesn’t include the chainID in the signed fields , as advertised. Therefore it’s open to network reply attacks.

This is the list of fields signed, and how they map to a normal Ethereum transaction:

**Normal -> EIP-3074**

Nonce    -> Nonce

GasPrice -> GasLimit

GasLimit -> ReceiveAddress

ReceiveAddress -> Value

Value -> Data

Data -> relayer

chainId (not present)

empty (not present)

empty (not present)

---

**SamWilsn** (2020-11-13):

Thanks for the feedback! I updated the signed fields to include chainid.

Is EIP-712 final yet? I wanted to avoid it until it’s finalized.

If a malicious website wanted to confuse a user, they’d have to present something like this:

```auto
Nonce: 3
GasLimit: 66000000000 (66 Gwei, current gas price)
ReceiveAddress: 0x0000000000000000000000000000000000Be8c72 (current block gas limit)
Value: 611382286831621467233887798921.843936019654057231 ETH (some address)
...
```

I’ve probably missed some of the specifics of the RLP offsets, but it seems like it would be a *very* suspicious transaction. I’m not opposed to modifying the format to make it impossible though, if you have any suggestions.

---

**MicahZoltu** (2021-02-23):

Recommend having the transaction be a 2718 typed transaction, which means grabbing a number and signing over `secp256k1(keccak256(TransactionType || rlp([nonce, gaslimit, to, value, data, invoker, chainid])))`.  This would make it so we don’t have to worry about having the signature collide with some other future transaction type.

This wouldn’t *technically* be a 2718 transaction because it has no receipt and doesn’t end up in a block header, but we **should** reserve the transaction type number and follow the signing rules.

---

**MicahZoltu** (2021-02-23):

Other changes I would like to see:

1. Signature should be yParity, r, s.  v shouldn’t really be used anymore.
2. Signature first.  This enables some minor optimizations and comes at no cost.
3. data last.  This is pretty minor, but having the variable length thing at the end makes some stuff a tad easier and this change comes with no cost.
4. Remove chainId.  This can be addressed by the invoker with CREATE2 using CHAIN_ID as a salt.  In the case of a fork (chain ID change), the invoker can be redeployed. This can be automated with a factory.  By not having a chain ID, transactions and invokers can be constructed that intentionally support replays across chains.
5. Remove nonce and nonce checking and only include 32 bytes of extra data in the signature.  The invoker can then do nonce management (or not!).
6. Use ABI Encoding or SSZ instead of RLP encoding.  We don’t need the space savings provided by RLP, and ABI encoding and SSZ are a bit easier to work with when you have fixed width data elements followed by a single dynamic length data element.
7. Rename gaslimit to mingas.  This value doesn’t represent a gas limit, but instead represents the minimum amount of gas that needs to be supplied.

---

**SamWilsn** (2021-03-03):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Remove chainId. This can be addressed by the invoker with CREATE2 using CHAIN_ID as a salt. In the case of a fork (chain ID change), the invoker can be redeployed. This can be automated with a factory. By not having a chain ID, transactions and invokers can be constructed that intentionally support replays across chains.

Being able to replay a transaction-like package across multiple chains is a bit of a niche feature. How often do you think a user would want to do that? I think the common case (one chain per transaction) is good enough, and matches what users will want to do.

Safely implementing the one-chain-per-transaction rule in the invoker would require either stuffing the chainID into `nextra`, or checking that the chainID hasn’t changed before every sponsored call.

---

**SamWilsn** (2021-03-03):

I expanded the section on why I don’t believe using the revert reason to indicate precondition failures is a good idea.

I’ve also reordered the signature input, so hopefully that takes care of everything!

---

**MicahZoltu** (2021-03-04):

Still outstanding (ignoring the things we disagree on):

- yParity instead of v (which aligns with 2930 and 1559 transactions)
- data as the last field in the signed data.  It is the only variable length item, and having it last has potential to simplify things at essentially no extra cost other than moving it in the spec.

New comments:

- You pass value twice, once as an actual attached ETH amount and again in the data blob.  This is unnecessary given they must be equal.
- I feel like we should be putting everything on the stack, rather than a mix of stack and encoded data:

```auto
IMPERSONATECALL gas, value, y_parity, r, s, sponsee, type, nextra, to, mingas, data_start, data_length
```
- Add rationale as to why STATICCALL context is allowed at all.  I can’t think of a situation where this would be useful in a static context.

---

**SamWilsn** (2021-03-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> yParity instead of v (which aligns with 2930 and 1559 transactions)

Is this just renaming `v` to `yParity`, or is it also removing chain id?

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Add rationale as to why STATICCALL context is allowed at all. I can’t think of a situation where this would be useful in a static context.

I’m inclined to leave it in, even if I can’t think of a good reason for it. After all, you can `CALL` inside of a static context.

---

**MicahZoltu** (2021-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Is this just renaming v to yParity, or is it also removing chain id?

It removes the chainId and the +27.  From 2930:

> YParity The parity (0 for even, 1 for odd) of the y-value of a secp256k1 signature.

---

**MicahZoltu** (2021-03-04):

Also, so we have it documented, I recommend renaming `TXCALL` to `IMPERSONATECALL` to make it more clear what this version of call actually does.

---

**SamWilsn** (2021-03-04):

While I am opposed to removing chainid, I am not opposed to encoding it separately. Thought?

---

**SamWilsn** (2021-03-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Also, so we have it documented, I recommend renaming TXCALL to IMPERSONATECALL to make it more clear what this version of call actually does.

`IMPERSONATECALL` is used by the draft [EIP-2997](https://eips.ethereum.org/EIPS/eip-2997). I’m down with renaming the opcode, but I’m not sure which name I prefer:

- IMPERSONATECALL - decent name, and I guess you can impersonate yourself if you want?
- CALLAS - breaks the pattern of *CALL, but it’s short and descriptive.
- SIGNEDCALL - Less descriptive.
- SIGNCALL - seems backwards, since you aren’t signing a call, you’re making a call with a signed package, plus it’s also not descriptive.
- TXCALL - call with transaction-like package

---

**MicahZoltu** (2021-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> While I am opposed to removing chainid, I am not opposed to encoding it separately. Thought?

What do you mean by “encoding it separately”?

---

**SamWilsn** (2021-03-04):

Instead of packing yParity and chainid into v, having separate fields for yParity and chainid

---

**adietrichs** (2021-03-05):

I created a (relatively) simple example for what an invoker contract for EIP-3074 could look like:


      [gist.github.com](https://gist.github.com/adietrichs/ab69fa2e505341e3744114eda98a05ab)




####

##### EIP3074Relayer.sol

```
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";

interface WETH9 {
    function balanceOf(address) external returns (uint256);
    function deposit() external payable;
    function withdraw(uint256) external;
```

This file has been truncated. [show original](https://gist.github.com/adietrichs/ab69fa2e505341e3744114eda98a05ab)

---

**MicahZoltu** (2021-03-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Instead of packing yParity and chainid into v, having separate fields for yParity and chainid

We may be saying the same thing, but I want to verify:

`chain_id` would be part of the signed data, but would not be part of the data passed to the opcode.  When validating the signature, it would use whatever `chain_id` the EVM has internally for the chain it is executing on.  The signature would just be `y_parity, r, s`.

---

**chriseth** (2021-03-05):

I have several requests / questions concerning this EIP:

- Can you please extend the description of the semantics of the opcode (it mostly focuses on the arguments and the return values)?
- Why is so much data put into the arguments instead of using stack slots? I would assume almost everything to be taken from the stack apart from the actual payload.
- EDIT: It does exactly that, sorry for the confusion! PREVIOUS TEXT: Maybe I didn’t get it but what is the idea behind setting tx.origin / caller instead of msg.sender / sender? Until now, the distinguishing feature of tx.origin is that this is the account that pays for the gas. This property would be destroyed. Also if this is kept as it is, please mention that you ALSO set msg.sender because that is probably also the idea, isn’t it?
- It would be nice to improve the presentation a bit. It is a bit hard to keep track of 5 different addresses plus other data - is that really needed?
- There are many more points where this specification is not really clear. For example, the behaviour of the function abi.encode strongly depends on the types of its arguments, but those are not specified.

---

**chriseth** (2021-03-05):

Since this is not really about a transaction (for me, transactions are objects that are stored in blocks), I would prefer a name similar to `impersonatecall` or `substitutecall`.

---

**matt** (2021-03-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chriseth/48/2111_2.png) chriseth:

> There are many more points where this specification is not really clear. For example, the behaviour of the function abi.encode strongly depends on the types of its arguments, but those are not specified.

Any thoughts on `CALLFROM` / `CALLAS`? They would break the `*CALL` scheme, but are short and intuitive. Alternatively, `SIGNEDCALL` / `SIGCALL`?

---

**SamWilsn** (2021-03-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chriseth/48/2111_2.png) chriseth:

> Can you please extend the description of the semantics of the opcode (it mostly focuses on the arguments and the return values)?

Sure thing! Is there something specific you’d like to see beyond just “it’s exactly like call, except…”?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chriseth/48/2111_2.png) chriseth:

> Why is so much data put into the arguments instead of using stack slots? I would assume almost everything to be taken from the stack apart from the actual payload.

I had separated it out so that signed parts of the message go in memory and the unsigned parts go on the stack. It also has the nice property that introducing a new `type` down the road is pretty flexible. I *think* but am not 100% sure that copying the TLP out of calldata into memory should be reasonably efficient.

Happy to change it though!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chriseth/48/2111_2.png) chriseth:

> It would be nice to improve the presentation a bit. It is a bit hard to keep track of 5 different addresses plus other data - is that really needed?

I wholeheartedly agree. Not sure how to avoid talking about them though. You’ve got the sponsor/sponsee and I don’t think you can avoid mentioning either of them. The invoker contract has to exist, and so does the call destination… Is there some other data I can trim out?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chriseth/48/2111_2.png) chriseth:

> There are many more points where this specification is not really clear. For example, the behaviour of the function abi.encode strongly depends on the types of its arguments, but those are not specified.

There should be types for all of the ABI encoded fields (eg. `type: uint8`), and if I missed any that’s a problem!

Were there any other unclear points I can tackle?

Thanks for the feedback, I appreciate it.


*(226 more replies not shown)*

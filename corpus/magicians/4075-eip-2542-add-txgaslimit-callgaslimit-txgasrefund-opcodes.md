---
source: magicians
topic_id: 4075
title: EIP 2542 - add TXGASLIMIT, CALLGASLIMIT, TXGASREFUND opcodes
author: forshtat
date: "2020-03-03"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-2542-add-txgaslimit-callgaslimit-txgasrefund-opcodes/4075
views: 2269
likes: 0
posts_count: 8
---

# EIP 2542 - add TXGASLIMIT, CALLGASLIMIT, TXGASREFUND opcodes

This is a discussion thread for [EIP-2542](https://github.com/ethereum/EIPs/blob/39461da12c50e5efac88bed0c8d3e81233efdb8b/EIPS/eip-2542.md)

During our work on the [Gas Station Network](https://www.opengsn.org/) we have encountered a problem with the way such concepts as gas limit and gas refund are somewhat hidden from smart contracts. With the current EVM, the core GSN smart contract (RelayHub) is not able to precisely track the gas usage by a transaction due to these limitations.

Exposing such parameters as transaction gas limit, current execution frame gas limit, and current refund counter is an extremely simple and useful improvement to the EVM.

## Replies

**holiman** (2020-03-20):

Main counter points

- It solidifies evm-internals, specifically how refund and callcontext-gas is implemented in clients. As of now, geth implements a global refund counter, aleth and parity implements context-wise refund, and later resolves the actual valie later on.
- I think origin_gas is gameable. If the I make a contract which first consumes a lot of gas, then calls the meta-relayer to execute a meta-tx, then I will be paid extra for that gas which I consumed “privately” before doing the relay-work.

---

**forshtat** (2020-03-22):

Regarding 1 - I’ve looked into it, and I now think that ‘refund’ value is indeed to complex to calculate in all clients to be accessed via an opcode.

On the other hand, however the ‘callcontext-gas’ calculation is implemented by clients, it is definitely available as a parameter and can be easily exposed into the EVM. I think the only complication with this value would be EIP-150 that introduced the “all but one 64th” ceiling for call-gas value, so I explicitly referenced this inside the EIP.

Regarding 2 - This parameter can be gameable only with a naive implementation, but it is easy to protect against it being abused. I have added to the EIP an example where a meta-transaction sender signs a tx gas limit in the transaction, and a contract verifies it. This can be paired with some other checks to make sure the ‘relay’ does not steal gas from you.

---

**holiman** (2020-03-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/forshtat/48/2597_2.png) forshtat:

> Regarding 2 - This parameter can be gameable only with a naive implementation, but it is easy to protect against it being abused. I have added to the EIP an example where a meta-transaction sender signs a tx gas limit in the transaction, and a contract verifies it. This can be paired with some other checks to make sure the ‘relay’ does not steal gas from you.

Sorry, I can’t seem to find it in the EIP. Could you point me to it?

---

**forshtat** (2020-03-23):

Sorry, the link in the original post is to a specific commit, not the PR itself. Here is the link to ‘master’ https://github.com/forshtat/EIPs/blob/master/EIPS/eip-2542.md

The example is a remote approximation of how meta-transaction frameworks handle this task:

```
function verifyGasLimit(uint256 desiredGasLimit, bytes memory signature, address signer, bytes memory someOtherData) public {
    require(ecrecover(abi.encodePacked(desiredGasLimit, someOtherData), signature) == signer, "Signature does not match");
    require(tx.gasLimit == desiredGasLimit, "Transaction limit does not match the signed value. The signer did not authorize that.");
    ...
```

Of course, there is a lot of nuance to this problem, but the basic idea still applies.

---

**holiman** (2020-03-24):

I don’t see how that fixes anything. So if I use `tx.gasLimit` set to exactly what the `desiredGasLimit` is, what prevents me from exhausting the gas before entering the relayer?

Note: I’m not saying you’re wrong, it might be just me being stupid, so please educate me

---

**forshtat** (2020-03-24):

Well, the real-world contract would probably have a lot of other checks to prevent this from happening.

First, the meta-transaction signer may sign on `msg.sender` as well, so it cannot run random code first. Also, if the ‘relays’ who are calling some `execute(..)` function on a ‘relayer’ contract have no reason to be smart contracts themselves the ‘relayer’ contract could check that it is called directly(something like `tx.origin == msg.sender` or `tx.gasLimit == msg.gasLimit`). Next, the ‘relayer’ contract could only allow calls from registered relay addresses. This also would allow a relay network to blacklist or penalize relays in one way or another.

Worst case, it can also check the signature on `msg.gasLimit` instead. This is only required if there is a need for ‘relays’  to actually be smart contracts for some reason. There is a caveat to this, of course, because `CALL` does not guarantee the gas limit to be enforced, the ‘relays’  smart contracts would have to do that.

Anyway, these considerations I believe will be quite different for each application. My point here is that the opcode is not gameable by itself. Code using it may be gameable if not implemented correctly, but hey, this is true for `0x01 ADD` as well! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**holiman** (2020-03-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/forshtat/48/2597_2.png) forshtat:

> My point here is that the opcode is not gameable by itself. Code using it may be gameable if not implemented correctly, but hey, this is true for 0x01 ADD as well

I don’t fully agree. I think the `ORIGIN` opcode is ‘bad’ in the same way: whenever you want to use it, you’re probably doing it the wrong way and need to validate N other things aswell in order to not break your usecase. A niche opcode which is trivial to mistake for a good generic tool

Whereas the semantics of `ADD` are simple, straightforward and easy to explain. It adds two numbers together. Explaining msg.gasLimit is a lot more difficult: 'It’s the original gasLimit from the outer transaction, which will be somewhat higher than gasLimit, you can use it to figure out how much it’s cost so far to get “here”, but you can’t *really* trust number but need to verify it"

It’s generally considered ‘bad form’ to treat contracts dfiferently from EOA. Considering that a lot of people uses mutlsig wallets, it’s not good to build flows which require the caller to be an EOA.

In general, it sounds like today, there are a lot of ‘hacks’ around fixing this usecase. If we were to add that particular opcode, there would be a different flora of ‘hacks’.We’d simply change one set of problems for another.


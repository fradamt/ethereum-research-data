---
source: magicians
topic_id: 12497
title: Trustless EIP-2771
author: Pandapip1
date: "2023-01-09"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/trustless-eip-2771/12497
views: 2109
likes: 0
posts_count: 8
---

# Trustless EIP-2771

This is a pretty simple idea: instead of trusting EIP-2771 forwarders to return authorized addresses, instead, if an address would be taken, two addresses can be taken: the address of the forwarder, and the address assigned by the forwarder. For example, EIP-20 would be extended with the following functions:

```plaintext
function balanceOf(address _ownerForwarder, address _owner) public view returns (uint256 balance)
function transfer(address _toForwarder, address _to, uint256 _value) public returns (bool success)
function transferFrom(address _fromForwarder, address _from, address _toForwarder, address _to, uint256 _value) public returns (bool success)
function approve(address _spenderForwarder, address _spender, uint256 _value) public returns (bool success)
function allowance(address _ownerForwarder, address _owner, address _spender) public view returns (uint256 remaining)

event Transfer(address _fromForwarder, address indexed _from, address _toForwarder, address indexed _to, uint256 _value)
event Approval(address _ownerForwarder, address indexed _owner, address _spenderForwarder, address indexed _spender, uint256 _value)
```

## Replies

**SamWilsn** (2023-03-08):

If:

- a malicious contract at 0xAA...AA were to call an ERC-6315 compatible ERC-20 token’s transfer like so:

```plaintext
transfer(0xAA...AA, 0xAA...AA, 1 ether)
```
- With 0xBB...BB appended to the calldata.
- With an isForwardedTransaction always returning true.

Would the malicious contract be able to transfer themselves funds from `0xBB...BB`?

---

**dror** (2023-03-12):

Put it in another way:

a Token **trusts** that EVM that **msg.sender** is the rightful owner of the tokens: it is either a contract calling the token or the actual signer of the transaction.

If instead the Token receives an **address** from some sender that claims this address is authenticated - how can “trustlessly” it can know this address indeed initiated this transfer? - the only way we could think of is by trusting the one who forwraded this request, hence a “trusted forwarder”

---

**Pandapip1** (2023-03-12):

No. The address should be treated as different. Just think of it as address space extension without an EL change.

---

**SamWilsn** (2023-05-01):

Ah, I get it: instead of relying on the forwarder to authorize a specific “Ethereum address”, this proposal is suggesting that contracts namespace addresses per-forwarder.

An address “0x1 from forwarder A” is not the same address as “0x1 from forwarder B”.

Neat idea. Not sure if it’ll catch on though ![:confused:](https://ethereum-magicians.org/images/emoji/twitter/confused.png?v=12)

---

**SamWilsn** (2023-10-24):

I’d recommend replacing “boolean value `false`” and “boolean value `true`” with zero and non-zero respectively. Or even falsy/truthy. If you don’t, ERC-2771 is undefined if the caller returns something other than `0x0...0` and `0x0...1`.

---

**SamWilsn** (2023-10-24):

Instead of:

> Interfaces MUST NOT include namespaced versions of functions in their interfaces.

How about:

> Future standards compatible with this proposal MUST provide two distinct interfaces: one without Namespace functions, and one containing only the Namespace functions. This is to facilitate computing the ERC-165 interface identifiers.

---

**SamWilsn** (2023-10-24):

Still not 100% sold on referring to the sender extraction from EIP-2771. It’d be more clear if you just explicitly wrote it out in this EIP directly.


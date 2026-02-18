---
source: magicians
topic_id: 1077
title: Trivial addition of precompiles for known non-malicious functions
author: dontpanic
date: "2018-08-17"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/trivial-addition-of-precompiles-for-known-non-malicious-functions/1077
views: 672
likes: 0
posts_count: 3
---

# Trivial addition of precompiles for known non-malicious functions

~Pre EIP~

Functions such as erc20 `transfer` and `balanceOf` are established patterns in the smart contract ecosystem. They are known not to be malicious and, for tokens, should cost nearly the same as their counterparts in base unit eth. This is not currently the case. Is there a need for a ‘system’ to allow for common non malicious functions to be ‘whitelisted’(reduced gas cost)

storage operations naturally excluded

## Replies

**Ethernian** (2018-08-17):

At least `transfer` may have additional aspects implemented (like stopped).

Would you allow to override the precompiled func then?

---

**dontpanic** (2018-08-17):

I think not. modifiers could be added in a contract if the precompile is standardized. For example: assuming the bare bones erc20 transfer `transfer(address _to, uint256 _value) public returns (bool success)`  became the precompile `erc20Tx`.

calling `0xa9059cbb<address><value>` currently costs ~35k gas

In solidity the function roughly looks like :

```auto
function Transfer(...) some modifiers returns(){
if (balances[msg.sender] >= _value && _value > 0) {
            balances[msg.sender] -= _value;
            balances[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            return true;
        } else { return false; }
    }
```

with the pre compile:

calling `0xa9059cbb<address><value>` costs 21k gas

and roughly become

```auto
function Transfer(...) somemodifiers returns(){
       require(erc20Tx(_to, amount));
        emit someevent();
        return true;
        }
```

Modifiers like `stopped` can still be used.

pls forgive formatting I’m mobile, will fix in a bit


---
source: magicians
topic_id: 12741
title: New type of call - DELEGATESTATICCALL
author: 0xdapper
date: "2023-01-28"
category: EIPs
tags: [opcodes]
url: https://ethereum-magicians.org/t/new-type-of-call-delegatestaticcall/12741
views: 587
likes: 3
posts_count: 3
---

# New type of call - DELEGATESTATICCALL

The idea is pretty simple, introduce a DELEGATECALL like functionality that restricts state mutations on EVM level just like a STATICCALL does. The idea seems simple and surprised it doesn’t already exist. So I am [wondering](https://twitter.com/0xdapper_/status/1605035827569913857) if there’s any reason this hasn’t already been done? I am no EL dev, but I think the work should be very similar to all other type of calls and could use a lot of reuse(DELEGATECALL + STATICCALL).

This also opens up a very simple way to allow users to write custom views on a foreign contract if the said contract chooses to expose a function that does arbitrary `delegatestaticcall`s. Would also allow contracts to only keep the core state mutating + necessary view functions and in turn give more room for more code given the code size limits. Could also serve as a poor man’s opt-in workaround for [EXTSLOADs too](https://eips.ethereum.org/EIPS/eip-2330).

```plaintext
contract SomeContract {
  function extview(address _impl, bytes calldata _data) external view returns (bool _success, bytes memory _ret) {
    (_success, _ret) = _impl.delegatestaticcall(_data);
  }
}
```

## Replies

**horsefacts** (2023-01-28):

It’s possible (but a bit of a hack) to do something like this by 1) making a normal delegatecall 2) reverting with its return data, and 3) catching the revert and decoding the result of the original call from the error. Here’s [one example](https://github.com/PartyDAO/party-protocol/blob/1750cd4742b4b0ad96fe0353c2792578315df642/contracts/utils/ReadOnlyDelegateCall.sol) of the pattern I know of in the wild.

Would definitely be less expensive with its own opcode!

---

**0xdapper** (2023-01-29):

Yes, thats the way to do it right now for sure. But evm level restrictions on mutations would be nice just the same as staticcall. Technically could implement a static call in a similar fashion too.

Revert method requires you to have a new CALL since you want to revert it. Couldn’t be like a internal call jump to a `_delegatestaticcall` since it will revert the complete existing call. It’d have to be like `address(this).call(...)` and require more gas as you said and everyone to implement it in their contracts.


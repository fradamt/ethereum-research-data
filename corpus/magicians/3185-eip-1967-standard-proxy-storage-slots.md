---
source: magicians
topic_id: 3185
title: "EIP-1967: Standard Proxy Storage Slots"
author: spalladino
date: "2019-04-24"
category: EIPs
tags: [eip, proxy-contract]
url: https://ethereum-magicians.org/t/eip-1967-standard-proxy-storage-slots/3185
views: 11081
likes: 24
posts_count: 26
---

# EIP-1967: Standard Proxy Storage Slots

We are proposing an EIP to standardise how proxies store the address of the logic contract they delegate to. Given that the delegating proxy contract pattern has become widespread, we believe there is value, especially for off-chain tooling and explorers, in having a standard storage layout for proxy-specific information. In particular, a storage layout based on the [unstructured storage pattern](https://blog.zeppelinos.org/upgradeability-using-unstructured-storage/).

We are pushing for a standard storage layout and not a standard interface since proxies are designed to act transparently for a user, and introducing proxy-specific functions can [lead to attacks](https://medium.com/nomic-labs-blog/malicious-backdoors-in-ethereum-proxies-62629adf3357).

This EIP is designed to be a generalization for other delegating proxy standards that use the unstructured storage pattern, such as [EIP-1822](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1822.md).

> Delegating proxy contracts are widely used for both upgradeability and gas savings. These proxies rely on a logic contract (also known as implementation contract or master copy) that is called using delegatecall. This allows proxies to keep a persistent state (storage and balance) while the code is delegated to the logic contract.
>
>
> To avoid clashes in storage usage between the proxy and logic contract, the address of the logic contract is typically saved in a specific storage slot guaranteed to be never allocated by a compiler. This EIP proposes a set of standard slots to store proxy information. This allows clients like block explorers to properly extract and show this information to end users, and logic contracts to optionally act upon it.

https://github.com/ethereum/EIPs/pull/1967

## Replies

**mudgen** (2020-11-02):

Do you have any evidence that subtracting by 1 to make an unknown prehash is needed?

---

**spalladino** (2020-11-02):

It’s not strictly needed as far as I know, but I understand it makes it harder to mount a collision-based attack. The idea was suggested by [@wjmelements](/u/wjmelements) in [this comment](https://github.com/ethereum/EIPs/pull/1967#issuecomment-489276813).

---

**frangio** (2020-11-02):

If you have `keccak256('eip1967.proxy.implementation')` the preimage is known, it is `'eip1967.proxy.implementation'`. If you subtract one you get a random number with unknown preimage because `keccak256` is a cryptographic hash.

---

**0ju** (2021-02-12):

I am sorry but i do not understand this -1.

You say “keccak256(‘eip1967.proxy.implementation’) the preimage is known”. If you substract -1, the preimage is also known ? isn’t it ?

---

**frangio** (2021-02-12):

By “preimage” I mean a hash preimage. Since `keccak256('eip1967.proxy.implementation') - 1` isn’t the result of a hash, its preimage is unknown.

Whether this has any real consequences for security is up for debate. It was a precaution that someone suggested.

---

**0ju** (2021-02-12):

Sorry but i do not understand. Everything is known there; We are not talking about a password or a secret. Both preimage and hash are public in source code and is known by everybody.

Here is What i have understood. Can you tell me if i made a mistake somewere ?

- Logic contract’s storage variables are stored in proxy contract’s memory.
- Proxy contract contains his own storage variables
- We can have a big problem if a logic contract variable has the same address than a proxy contract variable address.
- For this reason, proxy contract variables are stored at 3 specific addresses (we have only 3 storage variables in proxy contract)
- The goal of this EIP is to specify 3 addresses and to say to all compilers and EVM they should NEVER store a variable at this addresses.

---

**frangio** (2021-02-23):

I think you understood correctly. I don’t think your last point is explicitly stated in the EIP but I would also say it’s true.

---

**Morlega** (2021-09-02):

Today I stumbled upon an interesting issue with this standard:

While testing some contracts, I ended up with this intended call chain:

```auto
MainContract -delegate-> ProxyObject
    ProxyObject -staticcall-> beacon.implementation()   [reverts here]
    ProxyObject -delegatecall-> implementation
```

*`beacon` is simply a beacon with `implementation()` (and other things) while `ProxyObject` accepts a beacon in the constructor, stores it in the beacon storage slot, and declares a fallback function that reads that storage slot, calls `implementation()` then delegate-calls to it.*

This would always revert due to `function call to a non-contract account` when doing `beacon.implementation()`, even though manually doing that method or even manually calling `ProxyObject` worked fine. Somehow `ProxyObject` being delegate-called by `MainContract` produced this weird error.

After a while, I figured out that since `ProxyObject` is delegate-called and not called regularly (or using `STATICCALL`), it is using the storage of `MainContract` which doesn’t contain the (right) beacon storage slot.

I [“solved”](https://github.com/SchoofsKelvin/blockchain-contracts/commit/80bb2a2fba654037907dd08fad4405eb94b2c354) this by storing the beacon address in an immutable field and defaulting to that if the storage slot is empty. Obviously not the best solution, but I can’t think of any other solution besides either:

- Storing the ProxyObject's address in an immutable field during construction, and making it query itself for the beacon implementation. This would mean that ProxyObject requires a regular (non-fallback) function for this. Perhaps it could use some magic parameter and check msg.sender to detect when it’s a “request from itself” versus a regular proxy call it should delegate, but quite complex and counter-intuitive. Quite a fundamental (and complex) change though.
- Simply not use EIP-1967 as it seems that it never anticipated the ProxyObject (the proxy contract with the beacon storage slot) to be delegate-called.

Is my reasoning in all this wrong, or did the EIP actually overlook this issue? I don’t see anything about this restriction (“proxy scripts that use beacon storage slots can’t be delegate-called”) in the EIP. I If that’s the case, perhaps adding a warning about this might not be a bad idea?

---

**frangio** (2021-09-02):

It is possible to use EIP-1967 in the scenario you describe. The storage variable just needs to be set in the “top level” contract, in your case `MainContract`. This is the case whenever there is more than 1 proxy layer, i.e. multiple delegatecalls in series.

The way the EIP should be interpreted is that the storage slots it specifies are only relevant in a call context where those slots are active. In a delegatecall context, the storage of the intermediate proxy is always ignored, so the EIP is not “in effect”.

---

**Morlega** (2021-09-02):

Still, a warning wouldn’t be a bad idea though. After all, I was of the impression that whether a contract is a “real” contract or a proxy pointing to another contract shouldn’t matter. Calling the proxy and non-proxy the same way should have the same results (assuming same state/address/etc), and the same for delegate calls. It’s quite counter-intuitive that delegate-calling a proxy suddenly makes the proxy act as a “different” proxy (e.g. affected by your own beacon storage slot).

This issue should also happen for proxies that work by storing a logical implementation address instead of a beacon.

Also interesting, although not strictly about this EIP: delegate-calling a diamond ([EIP-2535](https://eips.ethereum.org/EIPS/eip-2535)) would also suffer from this (it’d look for selectors in the caller’s DiamondStorage instead of the diamond’s). The reason why I’m mentioning this is because although it’s a bit too cumbersome for the “simple” proxies in this EIP (1967), it’s not unthinkable to deploy proxies (with or without beacons) pointing at a diamond, where upgrading the diamond would also “upgrade” all proxies pointing at it.

**EDIT**: Mentioned the diamond issue on the [discussion for EIP-2535](https://github.com/ethereum/EIPs/issues/2535#issuecomment-912129571). I imagine that any progress/remarks both here and there affect both EIPs.

---

**fulldecent** (2021-12-16):

Currently the reference implementation uses and undefined StorageSlot. Please include this definition in the implementation.

---

**frangio** (2021-12-16):

Is it acceptable to remove the inline reference implementation and just leave a link to the repository?

---

**poojaranjan** (2022-01-26):

An overview of EIP-1967 by [@Amxx](/u/amxx) and [@frangio](/u/frangio).

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/a/a5ecbd523053fe467b626383cb69757a876c6da2.jpeg)](https://www.youtube.com/watch?v=JEt3dBHB73U)

---

**firnprotocol** (2022-11-10):

hi [@spalladino](/u/spalladino) and others, thanks for this incredible work. i have a few questions.

is the standard flow that the (initial) implementation contract needs to be deployed *first*, and then the proxy deployed?

isn’t it the case that someone could (if they wanted) invoke the implementation contract directly—and that if they did this, then there would be a “ghost” parallel state kept by the implementation contract, alongside that kept by the proxy contract?

thanks again.

---

**spalladino** (2022-11-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/firnprotocol/48/7909_2.png) firnprotocol:

> is the standard flow that the (initial) implementation contract needs to be deployed first, and then the proxy deployed?

Yep!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/firnprotocol/48/7909_2.png) firnprotocol:

> isn’t it the case that someone could (if they wanted) invoke the implementation contract directly—and that if they did this, then there would be a “ghost” parallel state kept by the implementation contract, alongside that kept by the proxy contract?

Yep, but the point is which contract is the “legitimate” one. Using that argument, you could deploy a copy of a popular contract and start invoking it, but no one will pay attention to it.

There is one caveat to this: if the implementation contract has an instruction that can alter its code, then interacting with the implementation can lead to issues. The only opcode that can do this is SELFDESTRUCT, or doing a delegatecall to another contract with a SELFDESTRUCT operation.

---

**firnprotocol** (2022-11-10):

great! many thanks for your responses. i hope you’ll humor me on another very basic question (which is more about Solidity overall than EIP-1967).

if i am understanding things correctly, in this pattern, it becomes difficult to use the usual visibility control of functions on the implementation contract. for example, it seems that an `internal`, but state-changing, function, on the implementation contract, could be invoked via this mechanism: after all, the “technical” entrypoint of the EOA call is the proxy’s `fallback() external payable` (which is of course `external`). but by the time we reach this function, an attacker (say) could submit `calldata` corresponding to an `internal` function of the implementation contract. he won’t be blocked, since he has already “gained entry” to the proxy contract, via the `fallback`, and `delegatecall` treats the (`internal`) functions of the implementation contract as `internal` functions on the proxy contract.

is this actually accurate, or am i mistaken? if so, are there any easy ways to deal with this? thanks again.

**edit:** looks like this was a misunderstanding on my part, apologies. by definition of `delegatecall`, it will take the `calldata` supplied to the proxy, look for an *`external`* function on the implementation matching the selector, and then invoke that `external` function using the supplied calldata. `internal` functions don’t even get selectors in the compiled implementation contract (rather, they’re “inlined”), so it doesn’t actually make sense to call one through `delegatecall`. so for all intents and purposes, the visibility works “as expected”.

---

**spalladino** (2022-11-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/firnprotocol/48/7909_2.png) firnprotocol:

> rather, they’re “inlined”

The edit is correct, except for this bit. Internal functions are not necessarily inlined, but it’s true they are not callable from the outside, which is what matters here.

---

**firnprotocol** (2022-11-11):

right, my mistake; really what i meant is they don’t get selectors (or at least aren’t matched against when doing an external call). another tricky case is `external view` functions. it seems that these *do* have selectors, and are routed through the same `delegatecall` mechanism that mutating `external` calls are routed through. this is the only way that read-only functions could be directed to the proxy and work (even though the code isn’t there).

---

**firnprotocol** (2022-11-11):

a final question—huge thanks for your patience.

can you clarify the meaning of:

> This function does not return to its internal call site, it will return directly to the external caller.

(see [EIP-1967](https://eips.ethereum.org/EIPS/eip-1967) for all refs.)

by “internal call site”, do you mean essentially back to the body of `_fallback()` (the only place where `_delegate()` is called)? if so, then i don’t see the significance of this, since `_delegate()` is the final operation called within `_fallback()`, and `_fallback()` is moreover itself the final operation in both `fallback()` and `receive()`, the only places where it’s called. so it seems to me to amount to the same thing (at least functionally speaking) whether `_delegate()` returns to its internal call site or not.

i guess mechanically, the reason it *doesn’t* return to its internal call site stems from the semantics of the `return` Yul instruction. i was aware that `revert` returns to the next-outermore `call`er, but i guess it’s not surprising that `return` also does this.

so i guess ultimately this is a point about solidity memory management. i take it it’s safe to overwrite the memory location `0` as long as you’re not returning to the internal call site (?). if so, why is this roughly?

what is the downside—besides possibly very slightly higher gas—of implementing `_delegate()` this way (differences marked)?

```solidity
    function _delegate(address implementation) internal virtual {
        assembly {
            let location := mload(0x40) // <--- notice this
            calldatacopy(location, 0, calldatasize()) // <--- and this
            let result := delegatecall(gas(), implementation, location, calldatasize(), location, 0) // <--- etc
            returndatacopy(location, 0, returndatasize())
            switch result
            case 0 {
                revert(location, returndatasize())
            }
            default {
                return(location, returndatasize())
            }
        }
    }
```

---

**firnprotocol** (2022-11-11):

in fact, it seems that the following also works:

```nohighlight
    function _delegate(address implementation) internal virtual {
        (bool success, bytes memory data) = implementation.delegatecall(msg.data);
        assembly {
            let size := mload(data)
            switch success
            case 0 {
                revert(add(data, 0x20), size)
            }
            default {
                return(add(data, 0x20), size)
            }
        }
    }
```

perhaps it’s a matter of taste, but it seems arguably more aesthetically appealing. it may be possible to get rid of the inline assembly altogether; i’m not sure.

**edit:** i can confirm that “my” way leads to slightly larger (~234 bytes) bytecode. not sure exactly about the gas.


*(5 more replies not shown)*

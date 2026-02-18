---
source: magicians
topic_id: 553
title: "EIP-1153: Transient storage opcodes"
author: AlexeyAkhunov
date: "2018-06-15"
category: EIPs > EIPs core
tags: [opcodes, storage]
url: https://ethereum-magicians.org/t/eip-1153-transient-storage-opcodes/553
views: 34201
likes: 83
posts_count: 132
---

# EIP-1153: Transient storage opcodes

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/1153)














####


      `master` ← `ledgerwatch:master`




          opened 10:56PM - 15 Jun 18 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/f/ff5fa20e9d57c61a674f97a1fe07bf48a0c1137d.jpeg)
            AlexeyAkhunov](https://github.com/AlexeyAkhunov)



          [+75
            -0](https://github.com/ethereum/EIPs/pull/1153/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/1153)te: https://github.com/ethereum/EIPs/blob/master/eip-X.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your Github username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












I have written this EIP after having reviewed EIP-1087 ([EIP-1087: Net gas metering for SSTORE operations](https://eips.ethereum.org/EIPS/eip-1087)) and its discussion ([EIP-1087: Net storage gas metering for the EVM - #35 by Arachnid](https://ethereum-magicians.org/t/eip-1087-net-storage-gas-metering-for-the-evm/383/35)).

I propose an alternative design (which Nick said he also considered at some point), which in my opinion can bring bigger benefits than EIP-1087, at lower cost (by this I mean new opcodes with very simple semantics and gas accounting rules, and keeping the existing gas accounting rules for SSTORE intact).

Let me know what you think

## Replies

**Ethernian** (2018-06-16):

as mentioned in that other thread EIP-1087:

one year ago there was a discussion between me, @chriseth and [@pirapira](/u/pirapira) about very similar approach. It would be great to hear their opinion.

As far as I remember, there were following aspects to discuss:

- Which contracts from the call stack should be allowed to access (read/write) which transient variables?
- Should be a new variable instance created on new recursive call (stack) or an existing instance should be reused?

one year ago we have decided to drop the transient storage EIP in favour to the idea of EIP-1087.

But if we review that decision once more, we should possibly think more about signalling we would like to implement.

Possibly we have more use cases than *ReentranceLock* here.

---

**AlexeyAkhunov** (2018-06-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> one year ago there was a discussion between me, @chriseth and @pirapira about very similar approach. It would be great to hear their opinion.

Thank you very much for this, I shall ask if they remember

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> Which contracts from the call stack should be allowed to access (read/write) which transient variables?

Good question - I will need to update the EIP. The idea is that transient variables are private to the contract, in the same way the storage is

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> Should be a new variable instance created on new recursive call (stack) or an existing instance should be reused?

If a contract gets re-entered within the same transaction, it accesses the same transient storage. Otherwise it would like existing memory, but with different addressing.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> Possibly we have more use cases than ReentranceLock here.

Another use case (though a bit contrived at the moment) is passing back error messages from the deeper execution frames. Again, passing them via outputs is not reliable, since intermediate frames can modify them.

---

**MicahZoltu** (2018-06-16):

What happens if something writes to transient storage and then reverts?  Would the transient storage changes be rolled back or retained for the remainder of the transaction (assuming not all gas was burned during the revert)?

---

**AlexeyAkhunov** (2018-06-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> What happens if something writes to transient storage and then reverts?  Would the transient storage changes be rolled back or retained for the remainder of the transaction (assuming not all gas was burned during the revert)?

Good question! The transient storage would be retained for the remainder of the transaction. Because otherwise the two use cases I am thinking about (reentrant lock and error message passing) are harder to program. Also, semantics of not interacting with reverts and invalid instructions makes implementation simpler. I will include this clarification into the EIP

---

**Arachnid** (2018-06-18):

As mentioned in the other thread, I think this option is less attractive because it introduces more complexity to the EVM, in the form of new opcodes, and another form of memory with new semantics. I think changing gas accounting around SSTORE/SLOAD is much simpler and more versatile.

Further, a change to SSTORE/SLOAD gas accounting will reduce gas costs for contracts already using storage for transient or repeated updates. Examples include contracts using storage to implement locks, and ERC20 tokens using ‘approve’ between contracts. If transient storage is implemented instead, new standards would need to be developed to permit the use of transient storage for these purposes.

> When implementing contract-proxies using DELEGATECALL, all direct arguments are relayed from the caller to the callee via the CALLDATA, leaving no room for meta-data between the proxy and the proxee. Also, the proxy must be careful about storage access to avoid collision with target storage-slots. Since transient storage would be shared, it would be possible to use transient storage to pass information between the proxy and the target.

It’s not clear to me why you can’t just pass the metadata along with the call data. Further, this approach would not work if you may end up with recursive calls; it’s the equivalent of using global variables.

> Transient storage does not interact with reverts or invalid transactions, that means if a frame reverts, its effects on the transient storage remain until the end of the transaction.

I think this is a **really bad** idea. Every other state change is reverted when a call reverts or throws; introducing a new semantic for this one type of storage would be counterintuitive, and creates a special case that is likely to lead to a great number of nonobvious bugs and security issues.

---

**AlexeyAkhunov** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> As mentioned in the other thread, I think this option is less attractive because it introduces more complexity to the EVM, in the form of new opcodes, and another form of memory with new semantics. I think changing gas accounting around SSTORE/SLOAD is much simpler and more versatile.

I am now trying to see if the Transient Storage is attractive enough without comparison to the SSTORE reduction proposal, which I think stands well on its own.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Transient storage does not interact with reverts or invalid transactions, that means if a frame reverts, its effects on the transient storage remain until the end of the transaction.

I think this is a **really bad** idea. Every other state change is reverted when a call reverts or throws; introducing a new semantic for this one type of storage would be counterintuitive, and creates a special case that is likely to lead to a great number of nonobvious bugs and security issues.

Thanks for this feedback. You see, I am not very sure how this should work. But for concreteness, I choose non-revertability of the transient storage. It turns out that this non-revertability gives smart contracts a unique resource that wasn’t available before (namely reliable communication from the re-enterancy frames that reverted/threw). But it could have the drawbacks you are talking about. I will try to make this more concrete with some POC.

---

**Arachnid** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> It turns out that this non-revertability gives smart contracts a unique resource that wasn’t available before (namely reliable communication from the re-enterancy frames that reverted/threw).

You can do this with return data. What’s the use-case that you have in mind that you can’t use return/revert data for?

---

**AlexeyAkhunov** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> AlexeyAkhunov:
>
>
> It turns out that this non-revertability gives smart contracts a unique resource that wasn’t available before (namely reliable communication from the re-enterancy frames that reverted/threw).

You can do this with return data. What’s the use-case that you have in mind that you can’t use return/revert data for?

If contract A (frame 1) calls into contract B, then B calls into A again (frame 2). Frame 2 of contract A reverts, and returns some data. Frame of contract B can choose to discard, or modify the return data instead of passing it verbatim to Frame 1 of contract A. Non-revertiable transient storage would allow Frame 2 of contract A pass any info to Frame 1 of contract A regardless of what contract B is doing.

---

**Arachnid** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> f contract A (frame 1) calls into contract B, then B calls into A again (frame 2). Frame 2 of contract A reverts, and returns some data. Frame of contract B can choose to discard, or modify the return data instead of passing it verbatim to Frame 1 of contract A. Non-revertiable transient storage would allow Frame 2 of contract A pass any info to Frame 1 of contract A regardless of what contract B is doing.

What’s an actual use-case for this, though? Where would it be useful?

In general nonlocal returns are a big source of confusion and nonobvious control flow in traditional programming. I’m not keen on adding them to the EVM.

---

**AlexeyAkhunov** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> AlexeyAkhunov:
>
>
> f contract A (frame 1) calls into contract B, then B calls into A again (frame 2). Frame 2 of contract A reverts, and returns some data. Frame of contract B can choose to discard, or modify the return data instead of passing it verbatim to Frame 1 of contract A. Non-revertiable transient storage would allow Frame 2 of contract A pass any info to Frame 1 of contract A regardless of what contract B is doing.

What’s an actual use-case for this, though? Where would it be useful?

I do not know yet. I only discovered this two days ago, after having answered [@MicahZoltu](/u/micahzoltu) question above. I decided then not to roll back my choice, but explore it a bit more. Thanks for this discussion, BTW

---

**Ethernian** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> Non-revertiable transient storage would allow Frame 2 of contract A pass any info to Frame 1 of contract A regardless of what contract B is doing.

What is the difference between this use case and existing implementation of *ReeantranceLock*?

You can set the lock from Frame 2 and read it Frame 1.

Only the necessary lock clean up at the end?

More challenging could be signalling between different frames in different contracts, but I have no good use case yet.

---

**Ethernian** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> When implementing contract-proxies using DELEGATECALL, all direct arguments are relayed from the caller to the callee via the CALLDATA, leaving no room for meta-data between the proxy and the proxee.

It’s not clear to me why you can’t just pass the metadata along with the call data.

BTW, I can recognize here another dropped [proposal I have made in ethereum/solidity](https://gitter.im/ethereum/solidity?at=5aafbe9f26a769820b2addd4)

to support an trailing data in message call. Possibly it worth reviewing it once more.

---

**AlexeyAkhunov** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> What is the difference between this use case and existing implementation of ReeantranceLock?

You will need to point me to the existing implementation of ReentranceLock, I could not find it, sorry.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> You can set the lock from Frame 2 and read it Frame 1.
> Only the necessary lock clean up at the end?

The reentrancy lock has to be unlocked after the call regardless of whether one uses storage or transient storage. Because after the call is complete, the lock is still locked. So no change in usage here, apart from the gas cost.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> More challenging could be signalling between different frames in different contracts, but I have no good use case yet.

Transient Storage cannot be used directly to implement signalling between frames of different contracts. All interactions between distinct contracts can only happen via CALL and STATICCALL.

---

**Ethernian** (2018-06-18):

> You will need to point me to the existing implementation of ReentranceLock, I could not find it, sorry.

Oh… I mean nothing special. Just a standard implementation with some further message call in the locked scope.

See [Contract Mutex, modifier noReentrancy](https://solidity.readthedocs.io/en/v0.4.21/contracts.html?highlight=reentrancy#function-modifiers)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> Transient Storage cannot be used directly to implement signalling between frames of different contracts.

(Even I am not sure it is good)

why not?

---

**AlexeyAkhunov** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> AlexeyAkhunov:
>
>
> Transient Storage cannot be used directly to implement signalling between frames of different contracts.

(Even I am not sure it is good)

why not?

Because of this (from EIP)

> Transient storage is private to the contract that owns it, in the same way as “regular” storage is. Only owning contract frames may access their transient storage.

---

**Ethernian** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> Only owning contract frames may access their transient storage.

you mean definitely: “Only owning contract frames may **write-** access their transient storage”.

What is bad with read access?

---

**AlexeyAkhunov** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> you mean definitely: “Only owning contract frames may write- access their transient storage”.
> What is bad with read access?

I see what you mean. To read from other contracts’s storage, one would need to modify the TLOAD opcode to have 2 arguments, one for address of account you are reading, and the other - for the address of the “cell” you are reading. It might not be a bad idea, actually.

---

**AlexeyAkhunov** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> you mean definitely: “Only owning contract frames may write- access their transient storage”.
> What is bad with read access?

One use case for contracts reading other contracts transient storage could be calling libraries via CALL (STATICCALL) instead of DELEGATECALL or CALLCODE, and passing structures (like trees and linked lists) without having to serialise them into input data. Calling via CALL and STATICCALL is arguably safer, because you don’t give the callee access to your storage.

---

**Ethernian** (2018-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> To read from other contracts’s storage, one would need to modify the TLOAD opcode to have 2 arguments,

I thought about usual public accessors, not about extending TLOAD opcode.

Replacing accessor functions with “native” read access per opcode deserves seperate EIP and cautios evalation. The idea to have a “native” per-reference read-only access to data structures without serialization looks to me as a major change targeting EVM-2.0.

I need to compare it to library pattern.

---

**Ethernian** (2018-06-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> To read from other contracts’s storage, one would need to modify the TLOAD opcode to have 2 arguments.

How much as should the opcode execution cost?

I would try to compare it with gas costs for usual message call.


*(111 more replies not shown)*

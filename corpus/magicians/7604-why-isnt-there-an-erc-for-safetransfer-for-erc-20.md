---
source: magicians
topic_id: 7604
title: Why isn't there an ERC for `safeTransfer` for ERC-20?
author: wschwab
date: "2021-11-28"
category: ERCs
tags: [token, erc20, eip165]
url: https://ethereum-magicians.org/t/why-isnt-there-an-erc-for-safetransfer-for-erc-20/7604
views: 5832
likes: 8
posts_count: 23
---

# Why isn't there an ERC for `safeTransfer` for ERC-20?

I’ve been wondering why there isn’t an ERC for adding `supportsInterface`, `safeTransfer`, and `safeTransferFrom` to ERC20 (along with an ERC2Receiver, a la ERC721 and 1155) - it seems like pretty low-hanging fruit. Just putting EIP-165 into ERC20 seems like a decent idea, it would be a nice building block for other ERC20 extensions to be able to build on, opening up the path for `interfaceId`s for governance tokens, staking tokens, or whatever.

In addition, adding `safeTransfer` to ERC20 shouldn’t make any backwards compatibility issues, as `transfer` and `transferFrom` would still exist, meaning smart contract wallets and the like wouldn’t be bricked by it.

I see that [EIP-1363](https://eips.ethereum.org/EIPS/eip-1363) went down a similar path, but didn’t use the same naming conventions in ways that I think are meaningful, and also adds additional functionality around approvals with callbacks that imho would be better handled with [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612) or [EIP-3009](https://eips.ethereum.org/EIPS/eip-3009).

Is there a good reason *not* to do this?

## Replies

**wschwab** (2021-12-12):

I’ve opened this as an EIP [here](https://github.com/ethereum/EIPs/pull/4524). I think 165 is an easy improvement to ERC20, and am still very much interested in feedback!

---

**lukehutch** (2022-05-31):

Isn’t EIP-4524 basically identical in semantics to the recipient notification logic of ERC777? (Minus the ERC1820 registration requirement)

---

**triddlelover69** (2022-05-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lukehutch/48/5068_2.png) lukehutch:

> (Minus the ERC1820 registration requirement)

Yeah, I am also wondering what is the major difference between the two?

---

**Amxx** (2022-06-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wschwab/48/1041_2.png) wschwab:

> Is there a good reason not to do this?

Yes:

ERC1363 already covers this usecase, and is final. Creating a new competing ERC for the same usecase would lead to even more confusion in this space, with some contracts implementing 1363, some 4524, some neither …

This confusion will just lead to everybody losing, and standardization not happening.

There is a standard. It works. It’s complete. It’s clear. Just use it, or push more people to use it.

[![standards](https://ethereum-magicians.org/uploads/default/original/2X/3/32311fc72160e86aa5c5275fda5ee7391e135197.png)standards500×283 22.9 KB](https://ethereum-magicians.org/uploads/default/32311fc72160e86aa5c5275fda5ee7391e135197)

---

**Amxx** (2022-06-15):

Also, ERC4524’s  `onERC20Received(address,address,uint256,bytes)` is exactly the same interface as ERC1363’s `onTransferReceived(address,address,uint256,bytes)` … expect for the actual function name … and thus the selector.

What the actual F*** ???

Reusing the same name would have made the two compatible on the receiving end … but no, you had to change things to make sure there is an incompatibility, and receivers need to implement two methods to support both.

---

**wschwab** (2022-06-15):

Hey Amxx!

No need to get worked up - I looked through the ERCs before I opened this, but I could only do my best trying to find something that had implemented this. I obviously missed this one. I’m happy to withdraw.

For reference, I even tried signalling my network to see if anyone else had heard of anything, which is also why I opened the thread here. You’re the first person to point to 1363, and it’s been over half a year. If there was a better way I could have gone about this, please let me know.

---

**Amxx** (2022-06-16):

I had a discussion with 1363’s author, and I think this whole thing is worth a discussion.

I identified two sub-problems, and sometimes depending on your point of view, the resulting code might be different:

- Being able to prevent transfers to address that can’t recover the funds (contracts that are not token aware)
- Being able to notify the recipient that tokens have been sent.

I’ll call that the `safeTransfer` problem vs the `transferAndCall` problem.

ERC-721 solves both with a single mechanism, the `safeTransferFrom` + `onERC721Received` combo. Its important to notice that for smart contract recipients, the two problem are very similar:

- you do the transfer
- notify the receiver through a public hook
- the receiver can check the msg.sender, accept or deny the transfer, and take any subsequent action (with user data passed through)
- the token will revert if the receiver did not accept the transfer

plain and simple.

ERC1363 does that on top of ERC20.

But there is a difference when the receiver is not a contract. If the receiver is an EOA (or more generally an address without code), then the callback will successed, but return no data … (when you expect some byte4 to be returned for security against fallbacks)

ERC721 says that, you should be able to safe transfer to an EOA and not care about data being returned.

IN OZ, this is currently implemented doing [this](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L400-L415)

ERC1363 isn’t specific about EOA, leaving (IMO) room for interpretation. However, the author’s intensions (from its implementation and our discussion) it that he expected `transferAndCall` to revert if the target is not a contract. This would make 1363 a acceptable solution for the `transferAndCall` problem but not for the `safeTransfer` problem.

IMO, it would be enough for 1363 to not revert when targeting an EOA to address both problems, just like 721 does. Still, there is an ambiguity about 1363, and the author is meaning toward an interpretation that is not suitable for some usecases.

I fear that the `safeTransfer` problem will justify the existence of another ERC, which would not revert on EOA (but otherwise be identical). If such a competing ERC is to exist, then I believe that it should reuse 1363’s hook … because the hook is only used for contracts, and contracts don’t care if they are called by a function that revert/doesn’t revert with EOAs … as long as the intension of the caller is clear.

---

**Amxx** (2022-06-16):

One point raised by @vittominacori (the author of ERC-1363) it that when you call `transferAndCall` you might expect the call to happen, regardless of the target … and expect a revert if the target is an EOA.

IMO calling an EOA is a no-op, and I accept that as successful.

But I guess this is all personal interpretation.

---

**vittominacori** (2022-06-16):

[@Amxx](/u/amxx) thanks for that thread.

ERC1363 purpose was to add the ability to make `approve`, `transfer` or `transferFrom` and then make a callback on the receiver in order to avoid double transactions and reduce friction on user engagement. So it was implicit that the receiver MUST be a contract. I missed to explicitly specify that it reverts on EOA. I could try to update the EIP also if it is final.

As discussed, ERC1363 was added on top of the ERC20 standard so we cannot (and we don’t want) change the standard behavior neither we want to overload the method signature. ERC721 instead was built as is and it has only one method to be used both with contracts or with address. So we expect that calling the `ERC721::safeTransfer` method it acts safe, as we expect the `Call` in `transferAndCall` does something. In my vision, using the `transferAndCall` to emulate the ERC721 `safeTransfer` may cause confusion.

The problem above was summarized about the transfer method against the `safeTransfer`, but ERC1363 also have an `approveAndCall` method. Both `approveAndCall` and `transferAndCall` or `transferFromAndCall` requires byte4 as returned value for security. It means that the callback was executed so, having an EOA returning nothing (and not reverting) does not ensure that the callback was executed, and for my initial purpose, it was not a successful transaction. Imagine calling `approveAndCall` on and EOA, then users expect that something happened but no actions have been made on tokens (other than the approve).

If we want to transfer (or approve) to EOA, or to a contract that does nothing, we can use the standard ERC20 transfer. Why we should call *AndCall on a EOA?

[Here](https://github.com/vittominacori/erc1363-payable-token) there is my own ERC1363 implementation. Also changing this behavior in the EIP may cause thousands of already built ERC1363 to not to be compliant.

---

**Amxx** (2022-06-16):

Then maybe we want to have 4524 as a complement to both 20 & 1363, but using 1363’s `onTransferReceived` hook ?

receiving contract won’t see the difference

---

**vittominacori** (2022-06-16):

For me using the ERC1363, having also the safeTransfer is redundant.

EIP1363 is final but EIP4524 is a draft.

I think we cannot compare these EIPs as the ERC4524 purpose is to transfer as ERC20 standard to EOA addresses, and to contracts implementing ERC20Receiver returning a selector, while ERC1363 purpose is that it **MUST HAVE** a callback executed after a transfer or an approve.

In my opinion if users really want the safe transfer for naming convention (like the ERC721) they can use the ERC4524. It has the onERC20Received and behave like the ERC721.

ERC1363 is another thing. It was built to give another level of power to the ERC20 tokens by adding the “callback” behavior on transfer and approve. Those methods are intended to be used with compatible contracts. Users who want to build their contracts or dapp MUST understand what they are doing so I think they can choose to call transfer and approve or transferAndCall and approveAndCall if they are referring to an EOA or to a compatible ERC1363 Receiver/Spender.

What issue having the EOA not reverting (like the safeTransfer) really solve, that cannot be solved by an accurate developer implementing his dapp?

---

**Amxx** (2022-06-17):

Am I the only one to see that ERC1363’s `onTransferReceived` and 4524’s `onERC20Received` would contain the same logic?

If there are two different function signatures, you are requiring contracts to expose both, and you are denying some ERC1363Receiver the ability to interact with 4524.

ERC721 shows us that you can successfully implement a transfer function that support both the `safeTransfer` and the `transferAndCall` problems … yes purposefully not do it for ERC20, and have two standards with two different hooks?

---

**vittominacori** (2022-06-17):

We are concerning about the fact that the 2 standards must coexist in the same token.

They have different hook names (`onTransferReceived` and `onERC20Received`), they have different purposes, ERC4524 works with transfer but ERC1363 handle also the approve behavior, one is final and already deployed with thousands of active tokens and the other is a draft.

I don’t think that we must change the ERC1363 behavior to cover the 4524 needs. And I don’t think we should emulate the ERC721 as it is natively developed as is.

If you have been requested to have the `safeTransfer` in the OZ library you could use the 4524.

ERC1363 is not a fallback method if people send a call to an EOA. ERC1363 adds hook methods for ERC20 to interact with compatible contracts. I will PR 1363 on OZ soon if you want to take a look to my own implementation.

---

**Amxx** (2022-06-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vittominacori/48/6350_2.png) vittominacori:

> They have different hook names (onTransferReceived and onERC20Received), they have different purposes, ERC4524 works with transfer but ERC1363 handle also the approve behavior

Putting the approval aside (only 1363 does it so lets not care about it),

1363 has a hook that is

*“Hey, I’m assuming you are a contract (otherwise you can’t respond anyway, and I’ll handle that don’t worry). You just received X tokens from some owner, with some operator, and here is some data to process it. It knows what to do with them using the data, then tell me its ok, otherwise I’ll revert”*

and 4524 has a hook that is

*“Hey, I’m assuming you are a contract (otherwise you can’t respond anyway, and I’ll handle that don’t worry). You just received X tokens from some user, with some operator, and here is some to process it. Let me know if you support this transfer, otherwise I’ll revert”*

If you don’t see that there are the same thing, I don’t know what to do.

I’m really starting to get frustrated that this forum, which goal it is to create standards that everyone can use, is apparently ok with having two similar hooks, that could be the same, but that for some reason refuse to see that they are the same, and will be competing for years, and never reach adoption

honestly, 1363 is already 2 years and was never really adopted… 667 is more widely used even though its not even a draft ERC … if that is not a standardization failure from the community, I don’t know what it

---

**vittominacori** (2022-06-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> “Hey you just received X tokens from some user, with some operator, and here is some to process it. Let me know if you support this transfer, otherwise I’ll revert”

It also says *“If you are a EOA, do nothing and I will believe you processed my data also if you not”*.

For me it is not a competition neither I want 1363 to be adopted instead of any other standard.

I really don’t want to change the original behavior to align with another PR and win this thread.

If 1363 is not useful, uses approval and we don’t care about it, is redundant and not adopted, please use 4524. EIP has been created 2 years ago but implementation was used since 2018. They are a lot of ERC1363 on blockchain explorer and no one has reported EOA issues in years. I really don’t see the community screaming to have that safeTransfer but I’m not community moderator so I could have miss some thread.

I was asked to get my vision about my EIP1363 and it was.

---

**Amxx** (2022-06-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vittominacori/48/6350_2.png) vittominacori:

> It also says “If you are a EOA, do nothing and I will believe you processed my data also if you not”.

This is possibly relevant to the sender yes, but not to the receiver. For a receiver, to be in any position of making a decision, is has to be a contract. For a receiving contract, the two statements are equivalent. For a receiving contract, being called by 1363 or by 4524 is equivalent.

I acknowledge your position on 1363 reverting on EOA, and I also can’t deny there is a need for a safeTransfer approach like ERC721 (which I guess will be 4524) … I just wish that that the two use the same hook, when the semantics of this hook, from the point of view of a receiving contract, is the same in both cases.

---

**frangio** (2022-07-04):

I don’t think this EIP should be pushed forward as is.

ERC721’s safeTransfer has been the source of reentrancy issues for many projects. “Safe transfer” is a misnomer because its use can actually make a contract *less* safe, and we should not make the same mistake again. For this EIP to be a good recommendation it should use a different function name.

ERC1363 is a Final EIP that has already established a hook for ERC20 transfers called `onTransferReceived`. Ideally, this EIP would reuse the same function signature to avoid fragmentation (as long as the semantics are the same).

---

**xinbenlv** (2022-11-16):

Hi from 2022, I love the idea of this EIP!

That said, I too have same concerns with [@frangio](/u/frangio). To mitigate the reentry attack, some thoughts: *Also* mandate the caller of for using *STATICCALL* when calling these hooks

With regard to EIP-1363, I wonder if it’s widely adopted? And EIP-1363 was not majorly addressing the hook, but majorly being used for `xxxAndCall` purpose.

With the massive adoption of EIP-721 and EIP-1155 I lean towards using similar naming convention to setup the hooks

```auto
// modified from and following convention of https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC1155/IERC1155Receiver.sol
interface IERC20Receiver is IERC165 {
    function onERC20Received(
        address operator,
        address from,
        uint256 value,
        bytes calldata data
    ) external returns (bytes4);

    function onERC20BatchReceived(
        address operator,
        address from,
        uint256[] calldata values,
        bytes calldata data
    ) external returns (bytes4);
}
```

```auto
// https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol
interface SafeERC20 is IERC165 {
    // Emm... This seem to conflict with ERC721's `safeTransferFrom`, but just putting here as an example. We could change method name to de-conflict.
    function safeTransferFrom(
        IERC20 token,
        address from,
        address to,
        uint256 value,
        bytes calldata date,
    ) external {}
}
```

I was thinking of having a Modernized ERC20 including support this hooks for checking if recipient is a receiver of ERC20

---

**Pandapip1** (2022-11-17):

[EIP-4524: Safer ERC-20](https://eips.ethereum.org/EIPS/eip-4524) exists too, and is what I think you are looking for

---

**xinbenlv** (2022-11-20):

Cross-posting some arguments I made in [another thread regarding EIP-5298 to consider supporting EIP-1363 or not](https://ethereum-magicians.org/t/erc-eip-5298-ens-trust-to-hold-tokens/10374/7):

1. ERC721 and ERC1155 has established safeTransferFrom as a naming convention that EIP-1363 is ignoring and create a new name transferAndCall, if the transferAndCall function is being used to only verify the recipient account being a contract account
2. On the other hand, if the transferAndCall function is being used anything other than verifying the recipient account being a contract account, e.g. to conduct a general function call, I think there is a lot of limitations of EIP-1363 for example, the parameter choice and implied technical direction of EIP-1363 has significant restrictions, e.g.

- the value of transfer(to, value, data) assume it can call the to but doesn’t support specifying ether Value which makes it not able to support general case of a remote function call that includes ethers required.
- It also doesn’t support extra data so it couldn’t make a more flexible call
- It doesn’t support a transfer call to specific which method inside of that recipient function to call, and restricting it to only onTransferReceived, renders it much less useful other than just verifying the recipient being an account, and instead introduced a lot of risk of re-entry attack.

With such consideration, and also explained by original author of EIP-1363 [@vittominacori](/u/vittominacori) , I agree see there is a legitimate distinction between EIP-1363 and EIP4524 and a valid need for a safeTransfer/safeTransferFrom for ERC20s.

I also see that EIP-4524 also has some place of improvements, e.g.

1. explain how the magic word is computed,
2. it should mandate the caller to restrict any state change on calling onERC20Received e.g…


*(2 more replies not shown)*

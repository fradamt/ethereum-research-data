---
source: magicians
topic_id: 10355
title: ERC-5453 Endorsement Standard
author: xinbenlv
date: "2022-08-12"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-5453-endorsement-standard/10355
views: 3821
likes: 4
posts_count: 13
---

# ERC-5453 Endorsement Standard

- See latest version of EIP-5453: ERC-5453: Endorsement - Permit for Any Functions
- Reference Implementation ercref-contracts/ERCs/eip-5453 at main · ercref/ercref-contracts · GitHub

## Replies

**onjas** (2022-09-12):

We’re developing something along this line! DM me if ur interested

---

**xinbenlv** (2022-10-02):

Great to hear. Are you still developing this implementation? [@onjas](/u/onjas)

---

**xinbenlv** (2022-10-12):

Hi [@frangio](https://github.com/frangio), just wanna sincerely invite you to comment on EIP-5453 (Endorsement) given that you are driving [#5782](https://github.com/ethereum/EIPs/pull/5782) as well as you are the main author of open-zeppelin. I think EIP-5453 can be a more general way to signal approval of a transaction. A working reference implementation is in [[WIP] Create RefImpl for ERC-5453 Smart Endorsement by xinbenlv · Pull Request #1 · ercref/contracts · GitHub](https://github.com/ercref/contracts/pull/1/files#diff-54f126299c368b8aa4279bb1cbb0d7e87c98cd9129f70ea0438ca77d357aedfb) (Work-In-Progress)

---

**frangio** (2022-10-13):

How does this compare to EIP-712 signatures? As far as I can tell EIP-712 signatures by themselves already serve as a general way to signal approval for things. What does this EIP offer on top of that?

---

**xinbenlv** (2022-10-14):

Hi [@frangio](/u/frangio),

Thank you for the question.

To give an immediate brief answer:

- EIP-712 regulates how to hash and sign a general struct.
- EIP-5453 regulates how to allow functions to take in a digital signature from arbitrary user to authenticate behaviors.
- EIP-5453 is a way to indicate “an intent to permit”. When used with ERC20, it directly compete with EIP-2612. But EIP-5453 also applies to other functions not just ERC20 transfer. It supports all functions that have an ending bytes _data. Sitenote: This behavior already exist in many existing ERCs‘ function e.g. ERC721 and ERC1150. I am propose to recognize this behavior with EIP-5750).

Let me use a metaphor: If you happen to be familiar with the “[bank check](https://en.wikipedia.org/wiki/Blank_endorsement)” concept:

- 712 regulates what the signature look like (also we to get data)
- 5453 regulates “assuming there is a check, let’s designate the top 20% of white area in the back of the check to be endorsement area, and put a signature there. By the way, there should be a date”
image1200×500 59.1 KB

And here is why:

*5453 focus on defining function behavior*, so it can use 712 in some part of the payload, but not all. Also it solves a problem that 712 doesn’t solve: how to identify where the endorsement is, and what happen if there are nested endorsements when it’s a nested function call, e.g.

*5453 is expected to be used with 712 in a lot of case*. The implementer of 5453 usually will (can / might need)  use 712’s spec for generating a msgDigest for any particular non-trivial function parameter. 712 didn’t determine how and where a function call will use the signature.

*5453 also have a very strict and specific schema that is tailored towards being used in function extra data for endorsement(authorization)*. This is not as flexible as 712.  For example, such specific schema includes consideration of `nonce`, `valid_since` and `valid_by`. In 712, such thing can be an implementation choice when implementers a choosing a struct. In 5453, with the goal of “endorsement” in mind, it asks for a very specific format to encode `nonce`, `valid_since` and `valid_by` to avoid replay-attack, and also so that endorsers have a clear expectation when will their endorsement be valid.

One may ask, then why just say “Put a 712 structure of ” in the ending of an extra-data function then you are good. Yes, that’s pretty much what we are doing here except for we might choose a simpler and rigid struct to reduce implementers’ chance of error, because the “endorsement” are usually used for authorization so the simpler the better. There are still some WIP details that author (me for, any co-author welcome too) needs to consider and design. Your feedback&advice is greatly appreciated. We will modify “Spec” and “Rationale” sections accordingly if changed.

Let me know if this help explain your question.  It might still be a bit unclear,

I am currently writing a few coding reference implementation examples to demonstrate what I mean.  Likely to publish in [ERCRef](https://github.com/ercref/contracts) repo.

## Relationship with other EIPs

Also maybe worth mention,

- we expect 5453 implementations to be used with 1271 too, just in case one might wonder.
- we expect 5453 to be able to replace EIP-2612: Permit Extension for EIP-20: Signed Approval but 5453 can be used as Permit Extension in more general way: it supports all other functions, not just ERC20 transfer

Some early RefImp Example (pseudo code)

## Example 0: Permit for ERC721

```auto
contract Foo20 is ERC721 {
   const uint256 EDMT_LEN = ...; //
   function transferFrom(address from, address to, uint256 tokenId, bytes calldata _data) {
      address endorserMaybe = _isEndorsedBy(_data); // for simplicity assume entire data is endorsment
      require(from == msg.sender || from == endorser); // ignore Approval for simplicity
      _owner[tokenId] = to;
      emit...
   }
   function _isEndorsedBy(bytes _endorsement) returns (address) {
      if (!endorsements[:8] ==ASCII"ENDORSED") return address(0);
      else {
         byte eType = endorsement[endorsement.length - 8];
      }
   } // It can be more graceful represented as modifier if solidity supports lambda
}
```

## Example 1: Nested endorsement used in multi-hop function call

```solidity
contract FooNFT {
  function swap(address tokenHolder, uint256 tokenId, bytes calldata data) {
    require(isEndorsedBy(data, tokenHolder));
    require(ownerOf(tokenId, tokenHolder));
    _burn(tokenId);
    destContract.mint(tokenId, tokenHolder, data[subsetlenth:]); // pseudo code, just to demonstrate ways to call the mint.
  }
}

contract BarNFT {
... // dest contract
  function mint(address to, uint256 tokenId, bytes calldata data) {
    require(isEndorsedBy(data, minterAdmin));
    _mint(to, tokenId, data[remainlength:]);
  }
  function _mint(... bytes calldata reason) {
    .. using the rest data as "reason"...
  }
}
```

In this way, user Alice could get the BarNFT’s `minterAdmin`’s endorsement to mint a token.

user Bob could help user Charlie to call the `swap` function with Charlie’s endorsement if the same `minterAdmin` also permit with an endorsement.

## Example 2: Two endorsements in one call

Here is another example `MergeNFT` using endorsements from two people at the same call, two token in, merge and create a third NFT

```auto
function mergeTwoNFTs(uint256 tokenIn1, uint256 tokenIn2, bytes calldata data) returns (uint256 tokenOut) {
  parse and verify endorsement 1 from data[datalength - 1*endorselength:]
  parse and verify endorsement 2 from data[datalength - 2*endorselength:datalength - 1*endorselength];
  verify endorser1 owns tokenIn1;
  verify endorser2 owns tokenIn2;
  _burn(tokenIn1);
  _burn(tokenIn2);
  _mint(tokenOut);
  return tokenOut;
}
```

---

**xinbenlv** (2022-12-15):

[@frangio](/u/frangio) I updated the EIP-5453 and a reference implementation is shared in [ercref-contracts/ERCs/eip-5453 at main · ercref/ercref-contracts · GitHub](https://github.com/ercref/ercref-contracts/blob/main/ERCs/eip-5453)

Your feedback is greatly appreciated.

---

**xinbenlv** (2023-01-05):

Most recent version [ercref-contracts/AERC5453.sol at main · ercref/ercref-contracts · GitHub](https://github.com/ercref/ercref-contracts/blob/main/ERCs/eip-5453/contracts/AERC5453.sol) and a simple usage example



      [github.com](https://github.com/ercref/ercref-contracts/blob/376b6b098a11cdf659f40fdd987cab9954b8df79/ERCs/eip-5453/contracts/EndorsableERC721.sol#L31)





####



```sol


1. require(owners[msg.sender], "EndorsableERC721: not owner");
2. owners[_owner] = true;
3. }
4.
5. function mint(
6. address _to,
7. uint256 _tokenId,
8. bytes calldata _extraData
9. )
10. external
11. onlyEndorsed(
12. _computeFunctionParamHash(
13. "function mint(address _to,uint256 _tokenId)",
14. abi.encode(_to, _tokenId)
15. ),
16. _extraData
17. )
18. {
19. _mint(_to, _tokenId);
20. }
21.


```










[@frangio](/u/frangio) for comment~

---

**xinbenlv** (2023-01-12):

Cross posting a comment from [ERC-4337: Account Abstraction via Entry Point Contract specification - #58 by yoavw](https://ethereum-magicians.org/t/erc-4337-account-abstraction-via-entry-point-contract-specification/7160/58)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png)[ERC-4337: Account Abstraction via Entry Point Contract specification](https://ethereum-magicians.org/t/erc-4337-account-abstraction-via-entry-point-contract-specification/7160/60)

> This 5453 solves a different problem. Namely, approval of specific method calls.
> This saves round trips for separate transactions so it close to batching.
> But batching is only one feature of 4337 .
> With 5453, You must sign with your account, so it “enshrines” eoa accounts.
> EIP 4337 is about accounts, and about abstracting them, so that any account can have it’s own execution model, signing model, recovery model, replay mechanism and also different gas model.
> In addition, we define the rpc and protocol used by users and nodes to communicate, and make sure UserOperations are as decentralized as normal Ethereum transactions.

---

**xinbenlv** (2023-09-12):

Friends, thank you for all the comments and feedback.

It has been quite sometime since our last update of this draft. And two reference implementations are shared and deployed. We believe this ERC is mature enough move forward.

Hereby [moves it](https://github.com/ethereum/EIPs/pull/7693) to Last Call and any final comments are appreciated!

---

**joeysantoro** (2023-10-26):

I’m just seeing this ERC now so sorry to potentially derail with this thought but why not introduce a new mapping called endorsement which is an address=>address=>bool

Then we can have an EIP-712/2612 style message called `endorse` which takes in the signature to specifically endorse a given user.

This removes the need to pass in data to be verified for each function and allows for a much more generic structure.

I think this design is much more intuitive. It also makes it immediately backward compatible with other standards such as ERC-4626 deposit/withdraw/mint/redeem calls and doesn’t require the calldata arg.

---

**jeroen** (2024-04-03):

[@xinbenlv](/u/xinbenlv) do you have any plans to revisit this ERC?

My two cents, working on an implementation of [EIP-7540: Asynchronous ERC-4626 Tokenized Vaults](https://ethereum-magicians.org/t/eip-7540-asynchronous-erc-4626-tokenized-vaults/16153) that wants to use endorsements for enabling a use case where the `owner != msg.sender`, is that the proposal [@joeysantoro](/u/joeysantoro) made in his comment above would be a significant improvement to this ERC. Mainly because `it also makes it immediately backward compatible with other standards such as ERC-4626 deposit/withdraw/mint/redeem calls`

---

**xinbenlv** (2024-06-13):

[github.com](https://github.com/Vectorized/multicaller/blob/main/src/MulticallerWithSigner.sol)





####



```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

/**
 * @title MulticallerWithSigner
 * @author vectorized.eth
 * @notice Contract that allows for efficient aggregation of multiple calls
 *         in a single transaction, while "forwarding" the `signer`.
 */
contract MulticallerWithSigner {
    // =============================================================
    //                            EVENTS
    // =============================================================

    /**
     * @dev Emitted when the `nonces` of `signer` are invalidated.
     * @param signer The signer of the signature.
     * @param nonces The array of nonces invalidated.
     */
    event NoncesInvalidated(address indexed signer, uint256[] nonces);
```

  This file has been truncated. [show original](https://github.com/Vectorized/multicaller/blob/main/src/MulticallerWithSigner.sol)


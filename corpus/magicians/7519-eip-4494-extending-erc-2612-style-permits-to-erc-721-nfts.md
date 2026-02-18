---
source: magicians
topic_id: 7519
title: "EIP-4494: Extending ERC-2612-style permits to ERC-721 NFTs"
author: wschwab
date: "2021-11-21"
category: EIPs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/eip-4494-extending-erc-2612-style-permits-to-erc-721-nfts/7519
views: 7913
likes: 29
posts_count: 36
---

# EIP-4494: Extending ERC-2612-style permits to ERC-721 NFTs

This thread is intended for an upcoming ERC based around [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612)-style approvals for ERC721 NFTs. The development work has been done by [@dievardump](/u/dievardump) , and is a result of conversation’s in [@anett](/u/anett) 's NFT Standards Working Group. There’s a tentative implementation [here](https://github.com/dievardump/erc721-with-permits).

ERC2612 accomplishes this by creating a signed message involving the addresses of the owner and proposed spender of an ERC20 token, in addition to the amount being approved, a deadline, and a signature. This ERC (despite being `Stagnant` at the time of this writing) enjoys a large amount of traction, and, for example, is leveraged by Uniswap wherever available.

There are a few things we’d like community feedback on regarding the best way to set this up for ERC721 NFTs.

## 1) owner-based or tokenId-based nonces

While trying to apply this formula to ERC721 NFTs, there is an additional optimization allowing for more flexibility than ERC2612 owing to the unique architecture of ERC721. ERC2612 takes the value being approved as an argument, and increments a nonce after each call to the `permit` function in order to prevent replay attacks. Since each ERC721 token is discrete, it allows for having the nonce based not on the `owner`’s address or calls to `permit`, but rather to tie the nonce to `tokenId` and to increment on each transfer of the NFT. One gain from this pattern is that allows an owner to create multiple permits for the same NFT, since the nonce will only be incremented if the NFT is transferred.

(For comparison, 2612 needs to focus on the owner, and the owner needs to either only give one permit at a time, or make sure that they are used sequentially.)

Another advantage to this setup is that 2612 permits can only be signed by the owner of the tokens, but not by parties approved by the owner. This setup should allow approved parties to create permits for NFTs that they have been approved on too.

`tokenId` seems to us to be the best way to handle nonces, though otoh 2612 is `owner`-based, as are Uniswap v3’s position NFTs. We’re interested in community feedback about this!

## 2) v,r,s vs full signatures

EIP2612 takes `v`, `r`, and `s` arguments, which are the three parts of a signature. The full signature is needed to verify the message, though. The author of 2612, Martin Lundfall, told me that his reasoning was that `v`, `r`, and `s` are all fixed length (`uint8`, `bytes32`, and `bytes32`), whereas the full signature would need to be a dynamically-sized array (if I understood him right, apologies if I missed something there), though if we kept `v`, `r`, and `s` as arguments (as in 2612), likely every function would need to concatenate them (using `abi.encodePacked`) in order to use `ecrecover` to verify.

[@Amxx](/u/amxx) has a repo with a singleton contract that “wraps” ERC20, 721, or 1155 tokens in a permit structure which was a big inspiration in this project [here](https://github.com/Amxx/Permit), and you can see his use of OZ utilities for verification - all of which take a full signature.

We’d like to keep things as similar to 2612 as possible, but are interested in community feedback if there’s a preference towards keeping the three elements separate or maybe towards ingesting the signature whole.

There are likely other major conversation points here, this is meant to kick things off, and we’re looking forward to what people say!

## Replies

**dievardump** (2021-11-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wschwab/48/1041_2.png) wschwab:

> ## 2) v,r,s vs full signatures
>
>
>
> EIP2612 takes v, r, and s arguments, which are the three parts of a signature. The full signature is needed to verify the message, though. The author of 2612, Martin Lundfall, told me that his reasoning was that v, r, and s are all fixed length (uint8, bytes32, and bytes32), whereas the full signature would need to be a dynamically-sized array (if I understood him right, apologies if I missed something there), though if we kept v, r, and s as arguments (as in 2612), likely every function would need to concatenate them (using abi.encodePacked) in order to use ecrecover to verify.

About this, I would like to add:

[since version 4.1, ECDSA from OpenZeppelin’s contracts](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/ECDSA.sol#L57-L86) repository implements EIP-2098 which allows signature of length 64.

We will not be able to support this easily with (r, s, v) as parameters since `encodePacked(bytes32, bytes32, uint8)` will always return a signature of 65 length.

This is why for the moment I went with the full `bytes memory signature` in the example of implementation, letting the library manage what EIP to follow according to the length of the bytes.

---

**dievardump** (2021-11-22):

Seems like I expressed myself in a confusing manner:

ECDSA supports 2 types of signature: (r, s, v) which is standard and 65 bytes long, and (r, vs) the [“compact form” (eip 2098)](https://eips.ethereum.org/EIPS/eip-2098) which is 64 bytes long.

if we use `(r, s, v)` as parameters, it will be more complicated to support EIP 2098.

if we use `bytes memory signature`, ECDSA can be used to automatically detect what type of signature it is, before recovering the address.

I can’t say if it’s better or not, but I suppose other EIPs might come later with other signature types/lengths, so maybe using the full bytes and let the Libraries handle the detection is a good habit to take.

---

**wighawag** (2021-11-25):

Great to see an EIP for that!

One minor suggestion: the name `nonces` is generic but has been used so far to represent account based nonce.

Also it is possible for an ERC721 contract to want to have both type of nonces

example 1):  account nonce would be more fitting  for `approveForAll` permit for example

example 2): DAO based on ERC721 votes have the need for signature nonce for delegation and these use account based nonce

Renaming nonces to be `tokenNonces` would be preferable in my opinion to avoid such conflict.

---

**wighawag** (2021-11-25):

Actually just realised that since `nonces(uint256)` is not the same as `nonces(address)` there is no conflict

---

**wschwab** (2021-11-28):

Starting to wonder if it’s worth it to add a `transferWithPermit` function that does a `safeTransfer` using a signature - I originally felt like maybe not since we were trying to keep things as close to 2612 as possible, but am starting to have my doubts.

In addition, I’m beginning to doubt how I did the EIP165 inegration - currently the interface ID is taken from the interface for 4494 + 165. The thing is that ERC721 already requires 721, meaning that if someone would build their contract strictly as described in the EIP, they’d run into circular inheritance problems from EIP165 being in both 721 and 4494. This makes me think that I should probably have the 4494 interface inherit the ERC721 interface, and then take the interface ID from there, but I wanted to open this up for conversation first.

---

**Amxx** (2021-11-29):

Hello.

First of all, I’d like to say that I welcome this standardization effort. This is really needed.

For the record, I am responsible for OZ supporting EIP-2098, and I am also the author of [GitHub - Amxx/Permit](https://github.com/Amxx/Permit). That might make you think I would favor

```auto
bytes sign
```

over

```auto
uint8 v, bytes32 r, bytes32 s
```

That is however not where I stand! While I hate early implementers forcing the hand of later standardization effort, I really think the permit being implemented by [UniswapV3](https://github.com/Uniswap/v3-periphery/blob/main/contracts/base/ERC721Permit.sol#L54-L85) sets a strong precedent in favor of sticking with uint8, bytes32, bytes32.

AFAIK, `bytes` is more expensive, because it requires an additional slot to store the length. It is thus however more versatile in some cases, particularly when dealing with signatures that are produced by multisig and are then verified using 1271 ([see this library that, if possible, should be preferred to ECDSA](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/SignatureChecker.sol#L21-L35))

The question then becomes:

- Do we want to future proof the standard with support for smart wallets (and other smart contracts)
- Do we want to stick with simple, EOA based signature, that would be cheaper to process

I don’t think there is an easy answer, particularly when smart wallets (and other smart contracts) can already implement meta-tx / signature based methods for calling approve (or any other functions). They don’t really need to be supported here.

One should keep in mind that using this permit interface for EOA would be irrelevant if/when EIP-3074 becomes available.

---

**dievardump** (2021-11-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Do we want to future proof the standard with support for smart wallets (and other smart contracts)

This was the idea, because NFTs are more and more put in Vaults or managed by multisig and their usage, imo, will continue to grow, which is why supporting them.

However, we should be able to use Contract.isValidSignature with `r,s,v` the same way Uniswap does it now. Supporting 2098 came mostly because this implementation here was inspired by yours.

But if people are more in favor of sticking with 3 parameters and forgetting the `bytes` form, then let’s go!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> (see this library that, if possible, should be preferred to ECDSA)

In the example implementation, I did not use `SignatureChecker` first because I am also checking if the signer is approved, which needs to recover the address.

I added `SignatureChecker` (following your implementation) as the second condition, if the first does not work.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wschwab/48/1041_2.png) wschwab:

> This makes me think that I should probably have the 4494 interface inherit the ERC721 interface, and then take the interface ID from there, but I wanted to open this up for conversation first.

I think your interface id is the right one. [I used type(Interface).interfaceId and the tests are passing](https://github.com/dievardump/erc721-with-permits/blob/main/contracts/ERC721WithPermit.sol#L153).

Usually, for extensions, we try to have only the methods specific to the extension in the interface Id. So no need to add nor EIP165, nor 721.

---

**Amxx** (2021-11-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> However, we should be able to use Contract.isValidSignature with r,s,v the same way Uniswap does it now.

I strongly disagree with that.

We should never assume that the `bytes` part of ERC1271’s `isValidSignature` is a 64 or 65 bytes long ECDSA signature. It would be anyone, including the concatenation of multiple ECDSA signatures, or even non ECDSA based signatures.

Taking 3 values, packing them, and passing them to `isValidSignature` might work in some case, but possibly lose a lot of the generality offered by ERC1271.

Again, I also want to point that these smart-contract based wallets don’t need permit as much as EOA do. In particular, they (often) include batching mechanism that allow to atomically execute an approve call, and a call to another contract. They also (often) include meta-tx relaying mechanism, allowing the owner to sign this batch of operations and letting someone else pay for the gas.

These are two cases where permit is essential to EOA but not needed for smart wallets

---

**wschwab** (2021-12-08):

if we would go the route of accommodating 1271 and 2098, what would be the best way to validate?

---

**dievardump** (2021-12-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> I strongly disagree with that.

So if I recapitulate:

- you are in favor of uint8, bytes32, bytes32
- we shouldn’t abi.encodePacked() those in order to use SignatureChecker?
- we shouldn’t really care for non-EOA because they already offer ways (arbitrary tx execution, batch tx/approve) to do things

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Taking 3 values, packing them, and passing them to isValidSignature might work in some case, but possibly lose a lot of the generality offered by ERC1271.

That I fully understand, which is why I think it’s better to go with the full `bytes` (and always use full bytes from now on, signature will evolve over time) than with `r, s, v`.

But if `r, s, v` is the only thing we offer users, why not at least try with it. I would better add cases where it might work than just ignore it.

---

**frangio** (2021-12-09):

How about using `bytes` officially, but specifying an optional interface in the EIP with `r,s,v` options that “MAY” be implemented? This would be a way of recognizing the precedent of Uniswap v3 permits, while moving towards a more general solution (EIP1271 signatures). If a token implements both they would be compatible with code that assumes Uniswap-style interface, but the EIP mandates only the first so going forward that is really the option that UIs must implement for general support.

I’d like to see how this impacts bytecode size but theoretically it shouldn’t be a huge overhead as most of the code will be shared.

---

**Amxx** (2021-12-10):

I did have a second thought about all that, and I think I changed my mind in favor of using `bytes`.

The main point is that, while smart wallet don’t technically need to uses these signature, because they can batch calls, the web3 apps that are going to connect to the wallet (through something like walletconnect) are not going to differentiate between smart wallets and EOA. They will apply the same workflow to both, and that means signing a message that will have to be recovered.

So at least until 3074 is a thing, and all wallets have the ability to propose a “sendbatch” metchanism, we should have as much genericity as possible in signature schemes. This means using bytes.

Its a shame that ERC2612 doesn’t use bytes, but if we have the choice between reproducting the same errors for consistency sake, and break things for the better, maybe we should do the former.

EDIT: +1 to [@frangio](/u/frangio) idea

---

**wschwab** (2021-12-27):

I’ve been thinking about this, and as a second draft of this EIP, wanted to consider going a bit further. I haven’t run this by [@dievardump](/u/dievardump) yet, so this is just my rough thoughts for a second draft.

First, in terms of signature, I think `permit()` should be overloaded, one that takes `v,r,s` like 2612 does for ERC20, and another which takes `bytes` like we originally suggested. We can explicitly state in the EIP that implementers `MAY` choose to only accept `v,r,s` signatures and have the `bytes` version either feed into it or revert. This allows implementers to decide how they want to handle signatures, gives the traditional `v,r,s` for people who find it easier, and makes an allowance that will have the groundwork for dealing with 2098 and 1271.

In addition, once we’re overloading, I really think we should overload `safeTransferFrom` to also accept a signature (both the `v,r,s` and `bytes` versions). A prominent use of `permit` is to make a one-tx approval and transfer, and it is my opinion that we should include a standard way of doing so.

In summary, this would mean adding an additional `permit` and two `safeTransferFrom` functions to the interface (and needing to update the EIP-165 `interfaceId` accordingly).

Thoughts?

---

**frangio** (2021-12-27):

If someone is using `safeTransferFrom` as the method to invoke a receiver smart contract I don’t think they need to use permit right?

What I understand is the idea for permit is that you send the permit to a contract so they can approve themselves and transfer the token to themselves, then do something with it. Using `safeTransferFrom` is an alternative flow, I don’t see how it makes sense to combine them.

---

**wschwab** (2021-12-28):

Let’s say I’m building a platform like Uniswap (or Aave) that needs approval in order to pull user assets. (This is mixing into ERC20s a bit, but the same thing should be applicable to something like OpenSea with NFTs.) By exposing a transfer function which accepts a signature we can design the following flow on the frontend:

- user signs message permitting/approving the platform to spend their NFT
- the router (or alternative) can then hit the exposed transfer function, inputting the sig as an arg, which will first call permit to approve the contract, and then immediately make the transfer on top of it

Basically, using the OZ contract templates, it would look something like:

```auto
function safeTranferFrom(
  address from,
  address to,
  uint256 tokenId,
  uint256 deadline,
  bytes sig
) external {
  permit(msg.sender, tokenId, deadline, sig);
  _safeTransfer(from, to, tokenId, "");
}
```

The nice thing about this flow is that the user only needs one tx, and while this is also somewhat via a once-per-contract `setApprovalForAll`, this does not suffer the massive trust needed for `setApprovalForAll`, allowing users to spot approve only what they want the platform to move without incurring extra costs and UX burden of adding a tx every time they interact.

It’s possible I misunderstood the question, though - does this answer what you were asking?

---

**frangio** (2021-12-28):

No I see, but I don’t think this function is necessary. Just permit is enough. You grant a permit to a smart contract that will first invoke `permit` and then invoke either of the standard ERC721 transfer functions.

---

**dievardump** (2022-01-18):

I’m not sure if we shouldn’t add it.

I had already added an example of safeTransferWithPermit() in the example of implementation I created for the EIP ([erc721-with-permits/NFTMock.sol at main · dievardump/erc721-with-permits · GitHub](https://github.com/dievardump/erc721-with-permits/blob/main/contracts/mocks/NFTMock.sol#L24-L37))

It can be really useful since it allows a user to use a permit and transfer the NFT in one go. Which is great to save gas and time.

Problem is, it adds another method to a standard that is already not so small.

I think there are pro and cons for this idea.

---

**duncancmt** (2022-01-19):

One thing I haven’t seen mentioned here is the mismatch between who is allowed to `approve` versus `permit`. `approve` allows an approved-for-all sender, while `permit` only allows the owner to sign. The maximally general version of `permit` should have the following form:

```auto
function permit(
    address ownerOrApprovedForAll,
    address spender,
    uint256 tokenId,
    uint256 deadline,
    bytes memory signature
) external;
```

in order to support 1271, 2098, and to homogenize `approve`/`permit`. Alternatively, to more closely mirror 2612, the form could be:

```auto
function permit(
    address ownerOrApprovedForAll,
    address spender,
    uint256 tokenId,
    uint256 deadline,
    uint8 v,
    bytes32 r,
    bytes32 s
) external;
```

but this makes the compatibility with 1271 somewhat less useful.

---

And just to add my $0.02, I think `safeTransferFromWithPermit` and its ilk are unnecessary since the same behavior can be achieved with a simple helper contract. ERC721 is already a conceptually/bytecode large standard to support; let’s not bloat it further with features that can be achieved simply through other means. The focus of the standard should be to build minimal blocks that enable useful applications, not to build the applications themselves.

---

**dievardump** (2022-01-21):

The example of implementation coming with the EIP allows both Approved on the tokenId and approvedForAll of the owner to create permits on a token id.

This doesn’t have to come in the method signature, it’s how the signer address is checked that matters here



      [github.com](https://github.com/dievardump/erc721-with-permits/blob/main/contracts/ERC721WithPermit.sol#L75-L88)





####



```sol


1. (address recoveredAddress, ) = ECDSA.tryRecover(digest, signature);
2. require(
3. // verify if the recovered address is owner or approved on tokenId
4. // and make sure recoveredAddress is not address(0), else getApproved(tokenId) might match
5. (recoveredAddress != address(0) &&
6. _isApprovedOrOwner(recoveredAddress, tokenId)) ||
7. // else try to recover signature using SignatureChecker, which also allows to recover signature made by contracts
8. SignatureChecker.isValidSignatureNow(
9. ownerOf(tokenId),
10. digest,
11. signature
12. ),
13. '!INVALID_PERMIT_SIGNATURE!'
14. );


```










---

However I am of the idea that this is just a sample, and implementers should decide themselves if they want any approved, approved for all or only owners to sign permits.

i.e: In the implementation I already use, I only add ApprovedForAll and owners

---

About mirroring 2612, as discussed before, I think using (v, r, s) was a bad idea and that we should stick to bytes memory, to accommodate all present and future types of signatures (v, r, s) (r, vs), …

---

**duncancmt** (2022-01-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dievardump/48/3841_2.png) dievardump:

> This doesn’t have to come in the method signature, it’s how the signer address is checked that matters here

Ahh, but unfortunately it does. In order to support 1271 *with approved-for-all permits*, the “signer” has to be an explicit argument to the function. Otherwise, how do we know which contract to call `isValidSignature` on? The implementation you provide above only allows the owner to use 1271.


*(15 more replies not shown)*

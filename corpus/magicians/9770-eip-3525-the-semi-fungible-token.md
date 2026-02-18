---
source: magicians
topic_id: 9770
title: "EIP-3525: The Semi-fungible Token"
author: will-edge
date: "2022-06-28"
category: EIPs
tags: [nft, token, eip, semi-fungible]
url: https://ethereum-magicians.org/t/eip-3525-the-semi-fungible-token/9770
views: 6762
likes: 7
posts_count: 21
---

# EIP-3525: The Semi-fungible Token

We proposed a Semi-fungible Token for define and implement customizable financial instruments, [EIP-3525](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3525.md).

This standard describes a new token format that have both ID and value property, where the ID property has the same semantics as ERC-721, and the value has the same meaning as ERC-20.

The semi-fungibility of the tokens is defined by the SLOT property, when two tokens have the same SLOT, their value are fungible, that is: they can be add together like ERC-20 tokens do.

This structure is best for defining flexible financial instruments, since one does not need to create a separate ERC-20 contract for each financial product. Also the value of the financial products can be manipulated in standard level, rather than treated separately at implementation level (like Uniswap V3’s LP which is using ERC-721).

## Replies

**will-edge** (2022-06-28):

This is the discussion thread for ERC-3525, The Semi-fungible Token Standard. The newest proposal document can be found at Ethereum EIP repository: [EIP-3525](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3525.md)

This version introduces significant changes from the last version, including two major aspects:

1. Adopting the value/transfer conventional model as general ERC standards, remove the split/merge functions that are more related to business logic of apps
2. Move some functions to optional interfaces, such as enumerable, etc.

Also the whole contents of the descriptions are completely revised.

---

**aram** (2022-07-02):

Is my understanding correct that the difference with ERC1155 is that for a specific TokenID there can only be 1 owner, but there’s a fungible value attached to each token?

If yes, then will having a `slot` make this ERC effectively similar to ERC1155?

---

**ymonk** (2022-07-04):

ERC3525 serves a different purpose from ERC1155. The former is designed to represent financial instruments, the latter the game items.

So if you have a ERC1155 token with a balance of 10, you have 10 identical items; while it’s a ERC3525 token with a value of 10, you have one item with face value of 10.

TokenID is universally unique, as which in ERC721.

Slot is a set of attributes collectively determining the exact category of the token.

---

**will-edge** (2022-07-04):

The key logic of ERC-3525 is that ‘an ID can have a value’, and the slot is an technic to judge whether the values of different IDs are fungible to each other.

The logic behind ERC-1155 is that ‘an address can have several tokens of a certain ID’.

So that although the ID in ERC-1155 is somewhat like the slot concept in ERC-3525, in that a slot can have fungible values, but the token logic is very different. For example, ERC-3525 introduces ID-to-ID value transfer model(with the help of slot), in which IDs are treated as a value holder, quite like the role of an address.

---

**ethean** (2022-07-07):

We usually classify non-fungible objects by their features, such as branch, region, and year, to make them fungible. There are no two identical leaves in the world, but they are both, leaves. It makes sense that the crypto world needs semi-fungible token standard just as it needs ERC-20 and ERC-721.

---

**MicahZoltu** (2022-07-27):

“Safe Transfer” should not require the receiver have a specific function implemented, because this breaks compatibility with most existing wallets that don’t support upgradability.  Almost every contract wallet supports the ability to call an external contract though, so using a registry will give far broader wallet support and doesn’t require people replace their wallets to gain compatibility with this.

I believe there is an EIP somewhere that defines a mechanism for this, but I forget its number. You might be able to use something like EIP-1820, but I recommend looking around to see if there is a standard specifically for this and compare them.

---

**will-edge** (2022-07-27):

Thanks for that.

We define a new ERC3525TokenReceiver only for those wallets as well as contracts that already specially support for EIP-3525, so that for these wallets they can call this special function when they transfer values rathe than ID to a contract.

If the destination contract does not support EIP-3525, a wallet can simply call ERC-721’s “Safe Transfer” to transfer a whole ID to that contract, and the contract just receives a ERC-721 token.

Hope this explains the design purpose of ERC3525TokenReceiver.

---

**MicahZoltu** (2022-07-27):

The problem is that the caller may be a generalized contract (e.g., Uniswap) and the receiver may be a contract wallet that can make arbitrary calls but cannot implement arbitrary interfaces.  In this scenario, the caller will attempt to do a SafeTransfer and this will fail because the receiver hasn’t implemented `ERC3525TokenReceiver`, even though the transfer would be perfectly safe because the receiver can make arbitrary contract calls.

This pattern has been used in the past, and it is really bad for contract wallets because not every contract wallet has the ability to implement arbitrary interfaces (nor should they do so).  On the other hand, almost every contract wallet supports making arbitrary calls, so the registry pattern is compatible with basically all existing wallets.

ERC-721 is one of the most well known bad actors here with their implementation of `SafeTransferFrom` which only allows transferring the token to contract wallets that have *explicitly* implemented ERC-721 support.  We should not be following the behavior of ERC-721 here and instead should be doing *better* than ERC-721.

---

**will-edge** (2022-07-27):

> ERC-721 is one of the most well known bad actors here with their implementation of SafeTransferFrom which only allows transferring the token to contract wallets that have explicitly implemented ERC-721 support. We should not be following the behavior of ERC-721 here and instead should be doing better than ERC-721.

Got the idea of your suggestion, we will discuss for that thoroughly.

From this perspective, simply removing the obligation of calling ERC3525TokenReceiver in the standard also works, right?

---

**MicahZoltu** (2022-07-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/will-edge/48/6439_2.png) will-edge:

> From this perspective, simply removing the obligation of calling ERC3525TokenReceiver in the standard also works, right?

In general, I think it is better to leave the decision to do recipient protection up to the caller rather than having it as part of the token.  This allows for maximum flexibility and for the caller to utilize additional contextual information they have available to make such a decision.

One can imagine a *separate* EIP that provides a mechanism for recipient checking (like a registry or introspection mechanism), and the caller can use that prior to making the call if they like, no need for the token to do anything special.

---

**will-edge** (2022-07-29):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> In general, I think it is better to leave the decision to do recipient protection up to the caller rather than having it as part of the token. This allows for maximum flexibility and for the caller to utilize additional contextual information they have available to make such a decision.

Yes, of course, we will make necessary changes in the proposal for both flexibility and recipient protection patterns.

There is only one special scenario we need to consider: sometimes transferring of value will result in a new token to be created and transferred to the receiver, in this case, if the token is considered as a ERC-721 token (since ERC-3525 tends to be compatible with ERC-721) , whether the standard should force implementations to obey ERC-721’s logic when SafeTransfer is called.

Of course if we totally remove the ‘Safe Transfer’ pattern from this proposal, the above problem no longer exists, but I think we can/are possible to design a pattern for both compatible and flexible purposes.

---

**will-edge** (2022-08-11):

Hi all, we are going to revise the value transfer model, by removing the SafeTransferFrom method, and introduce a ‘Check, Notify and Response’ model for better flexibility as well as simplicity.

### Design decision: Notification/acceptance mechanism instead of ‘Safe Transfer’

EIP-721 and some later token standards introduced ‘Safe Transfer’ model, for better control of the ‘safety’ when transferring tokens, this mechanism leaves the choice of different transfer mode (safe/unsafe) to the sender, and may cause some potential problem:

1. In most situation the sender don’t know how to choose between two kinds of transfer methods (safe/unsafe);
2. If the sender calls the safeTransferFrom method, the transfer may fail when the recipient contract didn’t implements the callback function, even if the recipient contract can receive and manipulate the token with no problem.

This EIP defines a simple ‘Check, Notify and Response’ model for better flexibility as well as simplicity:

1. No extra safeTransferFrom methods are needed, all transfer functions only need to obey the same logic;
2. All EIP-3525 contracts MUST check for the onERC3525Received function if the receiver is a smart contract, when the function exists, they MUST call this function after the value transfer and check the result to decide whether the transfer should succeed or fail;
3. Any smart contract can implement onERC3525Received function for purpose of being notified after receiving values, in this function it can return certain pre-defined value to accept the transfer, any other cases SHOULD cause the transfer to fail.

The corresponding interface definitions is as folows:

```solidity
 pragma solidity ^0.8.0;

/**
 * @title EIP-3525 token receiver interface
 * @dev Interface for any contract that wants to be informed by EIP-3525 contracts when receiving values from other addresses.
 * Note: the EIP-165 identifier for this interface is 0x009ce20b.
 */
interface IERC3525Receiver {
    /**
     * @notice Handle the receipt of an EIP-3525 token value.
     * @dev An EIP-3525 smart contract MUST check whether this function is implemented by the recipient contract, if the
     *  recipient contract implements this function, the EIP-3525 contract MUST call this function after a
     *  value transfer (i.e. `transferFrom(uint256,uint256,uint256,bytes)`).
     *  MUST return 0x009ce20b (i.e. `bytes4(keccak256('onERC3525Received(address,uint256,uint256,
     *  uint256,bytes)'))`) if the transfer is accepted.
     *  MUST revert or return any value other than 0x009ce20b if the transfer is rejected.
     *  The EIP-3525 smart contract that calls this function MUST revert the transfer transaction if the return value
     *  is not equal to 0x009ce20b.
     * @param _operator The address which triggered the transfer
     * @param _fromTokenId The token id to transfer value from
     * @param _toTokenId The token id to transfer value to
     * @param _value The transferred value
     * @param _data Additional data with no specified format
     * @return `bytes4(keccak256('onERC3525Received(address,uint256,uint256,uint256,bytes)'))`
     *  unless the transfer is rejected.
     */
    function onERC3525Received(address _operator, uint256 _fromTokenId, uint256 _toTokenId, uint256 _value, bytes calldata _data) external returns (bytes4);

}
```

---

**will-edge** (2022-08-17):

Hi, We are going to move EIP-3525 to Last-Call, hope more suggestions from everyone, thanks!

---

**will-edge** (2022-08-17):

> “Safe Transfer” should not require the receiver have a specific function implemented, because this breaks compatibility with most existing wallets that don’t support upgradability. Almost every contract wallet supports the ability to call an external contract though, so using a registry will give far broader wallet support and doesn’t require people replace their wallets to gain compatibility with this.

> I believe there is an EIP somewhere that defines a mechanism for this, but I forget its number. You might be able to use something like EIP-1820, but I recommend looking around to see if there is a standard specifically for this and compare them.

Now that we made it as a “check, notify and response” model, to give the choice and control of the transfer procedure to all parties:

For the callers, they don’t need to choose between TransferFrom and SafeTransferFrom, this will give most compatibility for all wallets, also prevent the failure of transfer when the caller calls the SafeTransferFrom but the recipient didn’t implement ERC3525TokenReceiver.

For the recipient, they can decide whether to implement ERC3525TokenReceiver, this gives the flexibility to wallets that cannot upgrade to implement arbitrary interfaces. This pattern also keeps the ability for the recipient to refuse receiving certain tokens.

For the implementation contracts of EIP-3525, they must check for the existence of ERC3525TokenReceiver (e.g. via EIP-165) and call the interface respectively. This decouples the caller and recipient in the transfer procedure, give the flexibility to both parties.

Further more, for mechanics like EIP-1820, it’s actually compatible with above solution, since an EIP-3525 implementation can add a registry function to let any wallets to register its ERC3525TokenReceiver for calling on token transfer. In this case, a wallet need not to implement the ERC3525TokenReceiver so that it won’t be called twice.

---

**GMADigitalBonds** (2023-01-05):

Is this protocol open source?

I can create an asset using this 3525??

Or is it more of those projects that only works in the hands of the developers themselves?

---

**Pandapip1** (2023-01-05):

EIPs are public domain. You can always create your own implementation of any Standard Track EIP, including this one.

---

**YeeTsai** (2023-01-05):

This is the reference implementation of ERC-3525.



      [github.com](https://github.com/solv-finance/erc-3525)




  ![image](https://opengraph.githubassets.com/c30e1c05e2ed00cf57b7ba99c292a926/solv-finance/erc-3525)



###



ERC-3525 Reference Implementation










You can develop your implementation of ERC-3525 also.

This is a step-by-step guide to get you started with the ERC-3525 reference implementation.

https://medium.com/solv-blog/erc-3525-starter-kit-developer-edition-9d734ca62bd0

---

**Rahimjackass** (2023-06-15):

Can we somehow refer to SLOT s as different contexts? Like within the first slot ( Game A, first context ) token ID 1 has the value of 100, and within the second slot ( Game B, second context ) has the value of 200.

Putting this concept in gaming, can we assign each minted token to a unique gamer?

---

**lukasz-glen** (2023-07-10):

The function `contractURI()` is [OpenSea standard](https://docs.opensea.io/docs/contract-level-metadata) to present collections. The JSON schema is a bit different there. Since it is adopted by some tokens and marketplaces, it should be removed from this standard or at least it should be discussed. Especially that it is unrelated to the rest of functionality - value_decimals/valueDecimals could be placed in slotURI.

It is not clear to me, whether `onERC3525Received()` should be called upon token receive or not. The reference implementation does not. But when I receive a token, I receive a value. So `onERC3525Received()` is to be called only when token value is changed?

The explanation for `onERC3525Received()` is somehow misleading for me. If I understand the nature of this ERC721 extension, it is not the matter of a token acceptance, rather it is about token value change listener. Because `onERC721Received()` is called anyway.

It is said that target contracts can implement `onERC3525Received()` optionally. It follows that contracts that implement this function MUST also declare it with ERC165. And this should be clear. Note that this is not the case of `onERC721Received()`. What I’m saying is that you do not need magic value to be returned.

Decimals are only for presentation purposes and ERC1155 approach should be followed in this regard. ERC1155 standard defines decimals with JSON metadata only.

I am trying to understand how this standard works. There are bonds, insurance policy, and vesting plans mentioned in the motivation part. But what is the reason to own by a single owner two different token ids of the same slot? I imagine that a single slot would refer to a single bond.

---

**HenryRoo** (2025-08-28):

Thank you for the great work on ERC-3525! One thing I’m curious about: since tokens already feature `slot` and `value`, why isn’t there a built-in mechanism for **usage metering** — i.e. automatically decrementing the token’s `value` upon usage (e.g. API call, model inference)? That would be an incredibly practical feature for permissions/usage-based scenarios.

Also, have you considered adding native support for **expiry** (a timestamp after which the token becomes invalid)? Without it, implementing time- or quota-bound access becomes highly custom and fragmented. Curious to hear your thoughts!


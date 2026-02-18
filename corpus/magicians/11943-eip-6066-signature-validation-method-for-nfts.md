---
source: magicians
topic_id: 11943
title: "EIP-6066: Signature Validation Method for NFTs"
author: boyuanx
date: "2022-11-30"
category: EIPs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/eip-6066-signature-validation-method-for-nfts/11943
views: 2393
likes: 2
posts_count: 10
---

# EIP-6066: Signature Validation Method for NFTs

Discussion for https://github.com/ethereum/EIPs/pull/6066

## Replies

**xinbenlv** (2022-12-15):

Hi [@boyuanx](/u/boyuanx),

Thank you for this EIP.

I am in full support for this EIP which extends EIP-1271, this is well needed! E.g. This EIP will be useful for [EIP-5453](https://eips.ethereum.org/EIPS/eip-5453) endorsement which. Feel free to mention use cases like EIP-5453 in your Motivation to add the weights of necessity of this EIP.

Also, I like to propose considering adding a extension field for future-proof ([EIP-5750: General Extensibility for Method Behaviors](https://eips.ethereum.org/EIPS/eip-5750))

```nohighlight
    function isValidSignature(
        uint256 tokenId,
        bytes32 hash
        bytes calldata extraData, // ADD THIS
    ) external view returns (bytes4 magicValue);
}
```

For example, this will allow future extending EIPs, e.g.

1. add "only consider valid when user’s EIP-1155 balance of tokenId > miniumBalance
2. only consider valid if user also hold slots of slotId

The EIP-5750 documented the rationale why adding an extension is beneficial. Had EIP-1271 had this extending field, they will not have the disadvantage that this EIP intends to solve and improve.

In short, this is EIP a great idea. I was thinking the same for a while, happy to collaborate in the context of [EIP-5453](https://eips.ethereum.org/EIPS/eip-5453)

---

**boyuanx** (2022-12-16):

Thank you [@xinbenlv](/u/xinbenlv), I agree with your points regarding flexibility and have incorporated the data field into my draft.

---

**SamWilsn** (2023-01-31):

I’m still not sold on the motivation for this EIP, but I think you make your case well enough. I just don’t see the benefits over an [EIP-1271](https://eips.ethereum.org/EIPS/eip-1271) signature from a smart contract wallet controlled by the DAO. That’s me taking off my editor hat, however, so feel free to disregard!

---

**SamWilsn** (2023-01-31):

As part of our process to encourage peer review, we assign a volunteer peer reviewer to read through your proposal and post any feedback here. Your peer reviewer is [@ballestar](/u/ballestar)! Please note that this review **is NOT required** to move your EIP through the process. When you—the authors—feel ready, just open a pull request.

If any of this EIP’s authors would like to participate in the volunteer peer review process, [shoot me a message](https://ethereum-magicians.org/new-message?username=SamWilsn&title=Peer+Review+Volunteer)!

---

[@ballestar](/u/ballestar) please take a look through [EIP-6066](https://eips.ethereum.org/EIPS/eip-6066) and comment here with any feedback or questions. Thanks!

---

**dievardump** (2023-01-31):

I’m a bit unsure why the method is called “isValidSignature” but no signature is provided to do any check.

The EIP references eip 1271 which specifically passes a signature (without enforcing the standard for this signature).

The idea of validating a signature means that something can be signed off-chain,

What you are doing here, and what this EIP allows, is not validating a signature, simply to check a flag. There is no signature involved, so no way to recover a signer and therefore no way to do stuff off-chain.

Like in EIP-1271: The owner of the contract signed something off-chain

Then an operator lambda can come and verify that this signature is valid for the whole contract

I do understand and agree that a way to have “per token signature” is needed and can add to the standards, but I do not think this EIP can do that without actually providing a signature.

---

**boyuanx** (2023-01-31):

[@dievardump](/u/dievardump) In this case, the signer is the token itself and the signing action is initiated by the token owner at the time. In terms of the signature, I referenced Gnosis Safe which does something similar here: https://github.com/safe-global/safe-contracts/blob/main/contracts/libraries/SignMessageLib.sol#L20

---

**dievardump** (2023-01-31):

Yes but by not passing a signature, you restrict the use cases for the EIP

Adding the signature would allow people to create other implementations/signature verification requiring a real signature (for example from the current owner of the item or from the collection creator or…).

And this would still work with your example by passing a bytes(0) signature

But all in all, I do think what you are trying to achieve can also already be done with EIP-1271.

What is in “bytes32 hash” is totally arbitrary and could be the hash of a something that includes the tokenId and would only work for this tokenId.

---

**boyuanx** (2023-01-31):

I agree use cases are restricted by not including a signature, but this is purposefully done so that the validation process is strictly limited and tied to the token and nothing else. The intent is for the token itself to act as the sole signing entity and not include or require any external entities (think of a stamp of approval), whereas EIP-1271 requires an ECDSA signature by the EOA signing entity. Passing in `bytes(0)` works but it’s not the intent of that EIP. I also agree `bytes32 hash` could incorporate the tokenId, but this is not standardized and would make interoperation difficult, which is precisely why a clear guideline (this EIP) needs to be established.

---

**boyuanx** (2023-05-04):

Added EIP-165 interface detection support and fixed the magic value (it was wrong before). Please let me know if anyone has any additional feedback! If not, I will move this along.


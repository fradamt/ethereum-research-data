---
source: magicians
topic_id: 9980
title: "EIP-5289 Discussion: Notary Interface"
author: Pandapip1
date: "2022-07-18"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5289-discussion-notary-interface/9980
views: 3167
likes: 2
posts_count: 27
---

# EIP-5289 Discussion: Notary Interface

https://github.com/ethereum/EIPs/pull/5289

## Replies

**Pandapip1** (2022-07-19):

NOTE: None of the authors is a lawyer. If you are a lawyer and would like to contribute to this EIP, please contact Pandapip1 on Discord (Pandapip1#8943).

---

**SamWilsn** (2022-07-20):

I would strongly recommend against using a PDF for the document. They are insanely complex, and incorrectly implementing a renderer in the wallet could mean inconsistencies between what two users see and sign.

I’d suggest picking a *very* minimal markdown flavour and use that instead.

---

**SamWilsn** (2022-07-20):

Hm, why create a registry contract for documents, instead of an interface implemented by, for example, the NFT contract itself?

---

**SamWilsn** (2022-07-20):

Even more hm, what if I created a malicious smart contract that reused the same document ID as a target contract.

A user could agree to the document while interacting with the malicious smart contract, convincing the target contract I had signed for it.

---

**Pandapip1** (2022-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I would strongly recommend against using a PDF for the document. They are insanely complex, and incorrectly implementing a renderer in the wallet could mean inconsistencies between what two users see and sign.

How about markdown with a Jekyll header (à la EIP)?

EDIT: Regular markdown is probably better.

---

**Pandapip1** (2022-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Hm, why create a registry contract for documents, instead of an interface implemented by, for example, the NFT contract itself?

One word: Gas.

It’s cheaper to have a registry for contracts that stores *all the contracts* and then have the function revert if necessary. I suggest that wallets simulate the transaction and if it would fail, prompt the user to sign the necessary documents *before* submitting the TX to the mempool.

---

**Pandapip1** (2022-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Even more hm, what if I created a malicious smart contract that reused the same document ID as a target contract.
>
>
> A user could agree to the document while interacting with the malicious smart contract, convincing the target contract I had signed for it.

Not possible. The revert reason references both the document ID *and* the library address so that there is no ambiguity as to what needs to be signed.

---

**SamWilsn** (2022-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> Not possible. The revert reason references both the document ID and the library address so that there is no ambiguity as to what needs to be signed.

Not sure I follow. Here’s the scenario I was imagining:

1. ValuableNftContract deployed, using a standard document registry.
2. Document 0x01 is created on the same registry.
3. Attacker deploys FunnyNftContract using the same document registry, and puts up a fancy web UI.
4. Victim sees FunnyNftContract and goes to mint one.
5. Attacker’s fancy web UI displays document 0x01 and requests a signature (possibly using eth_sign, which is still supported by MetaMask.) FunnyNftContract reverts with the magic message.
6. User signs the document, expecting it to only apply to FunnyNftContract, and it is submitted on chain.
7. Now if the user interacts with ValuableNftContract, it will believe the user has signed document 0x01, and will never revert to request the signature.

I think the easiest solution would be to include the requesting contract in the key, something like:

```solidity
interface IContractLibrary is IERC165 {
    // ...
    event DocumentSigned(address indexed signer, address indexed counterparty, uint48 indexed documentId);
    function isDocumentSigned(address user, address counterparty, uint48 documentId) public view returns (boolean signed);
    function documentSignedAt(address user, address counterparty, uint48 documentId) public view returns (uint64 timestamp);
    function signDocument(address signer, address counterparty, uint48 documentId, bytes memory signature) public;
}
```

---

On another note, why have both `isDocumentSigned` and `documentSignedAt`? Couldn’t you just catch the revert in `documentSignedAt` to tell?

---

**SamWilsn** (2022-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> It’s cheaper to have a registry for contracts that stores all the contracts and then have the function revert if necessary.

Is it? Don’t you have the overhead for a call into another contract for every operation?

---

**Pandapip1** (2022-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Is it? Don’t you have the overhead for a call into another contract for every operation?

You have a one-time overhead for checking if the user has signed. Then, once the user has, the value should be cached.

Also, there is no rule that says the library and the contract have to be different.

---

**Pandapip1** (2022-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> ValuableNftContract deployed, using a standard document registry.
> Document 0x01 is created on the same registry.
> Attacker deploys FunnyNftContract using the same document registry, and puts up a fancy web UI.
> Victim sees FunnyNftContract and goes to mint one.
> Attacker’s fancy web UI displays document 0x01 and requests a signature (possibly using eth_sign, which is still supported by MetaMask.) FunnyNftContract reverts with the magic message.
> User signs the document, expecting it to only apply to FunnyNftContract, and it is submitted on chain.
> Now if the user interacts with ValuableNftContract, it will believe the user has signed document 0x01, and will never revert to request the signature.

This is a feature, not a bug ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12). Always make sure you know what you are signing!

---

**Pandapip1** (2022-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> On another note, why have both isDocumentSigned and documentSignedAt? Couldn’t you just catch the revert in documentSignedAt to tell?

I’ll probably just add it as a second return value of `isDocumentSigned`

---

**SamWilsn** (2022-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> This is a feature, not a bug . Always make sure you know what you are signing!

That’s the thing, you can know exactly what you’re signing (the document id), and it’ll apply to all contracts that use the same registry.

---

**Pandapip1** (2022-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> That’s the thing, you can know exactly what you’re signing (the document id), and it’ll apply to all contracts that use the same registry.

Again, I don’t see the issue here. If there is ever a “Universal NFT Contract” that could apply to all NFTs, then great! There’s no need to make the user re-sign.

---

**xinbenlv** (2022-09-06):

I don’t have a good place to give feedback, hence adding here:

1. I don’t think it’s a good practice to include a full copy of Base 64 in the specification

- it may violate copyright laws because author is copying a piece of work that was originally granted with condition, but then release it in another place in-violation of the condition, such as per

> subject only to the restriction that no Contributor has the right to represent any document as an RFC, or equivalent of an RFC, if it is not a full and complete copy or translation of the published RFC.

Because this piece of Base 64 spec was not a full copy

1. It’s error prone for authors to make copy of references especially when it’s a code table. Such error if incurred can lead to significant backward difficulty.
2. I suggest directly put the interface solidity code into the markdown file, as opposed to reference them in the asset file.

---

**omnus** (2022-09-06):

Very interesting, would be great to see this in use.

From the look of things the document set would be contract wide? Any thoughts on expanding this to allow token specific docs?

---

**Pandapip1** (2022-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> I don’t have a good place to give feedback, hence adding here:

This is definitely the right place.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> I don’t think it’s a good practice to include a full copy of Base 64 in the specification

I’m working on another proposal that will supersede base64 for this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> I suggest directly put the interface solidity code into the markdown file, as opposed to reference them in the asset file.

Agreed. This will just be while this is in draft and while this is initially in review.

---

**Pandapip1** (2022-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/omnus/48/5625_2.png) omnus:

> From the look of things the document set would be contract wide? Any thoughts on expanding this to allow token specific docs?

Not sure what you mean. Mind elaborating?

---

**omnus** (2022-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> Pandapip1#8943

Hi [@Pandapip1](/u/pandapip1), I have an amazingly talented lawyer friend who also understands crypto. I’d like to introduce you. Have sent you a friend request on discord.

---

**omnus** (2022-09-08):

I was wondering if there was a use case for saying, for example, documents 1,2 and 3 are associated with all tokens in the collection, and document 4 was a specific agreement for tokenId 1129, and document 5 for tokenId 2971, etc.

This could then support specific legal arrangements that individual token holders have made. I have something along those kind of lines in the delegation extension built on top of EIP-4886, though not with the sophistication of your solution (I just have the ability to hold a URI).


*(6 more replies not shown)*

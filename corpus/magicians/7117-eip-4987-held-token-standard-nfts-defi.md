---
source: magicians
topic_id: 7117
title: EIP-4987 "held" token standard (NFTs + DeFi)
author: devinaconley
date: "2021-09-23"
category: EIPs
tags: [nft, erc-721, erc-20, erc1155, defi]
url: https://ethereum-magicians.org/t/eip-4987-held-token-standard-nfts-defi/7117
views: 6865
likes: 19
posts_count: 33
---

# EIP-4987 "held" token standard (NFTs + DeFi)

Hi all,

As NFTs and DeFi start to converge, there will more commonly be a distinction between the actual owner of an `ERC721` token and the functional owner/user.

Examples include:

- staked NFTs
- lending protocols that accept NFTs as collateral
- fractionalized NFTs

Currently, usage in one of those DeFi mechanisms would conflict with ownership verification for gaming, PFPs, art gallery showcases, etc.

Want to start up a thread on a standard ERC interface that could be used to very easily check the “functional owner” of an NFT held by another smart contract. Hopefully, something like this already exists that I am not aware of.

But if not…

I would propose something very lightweight that could be implemented by contracts with little overhead.

*(edit: this is not the final proposed interface, please see below)*

```auto
interface ERC721Hold {

    // emitted when the token is transferred to the contract
    event Hold(address indexed _from, uint256 indexed _tokenId);

    // emitted when the token is released back to the user
    event Release(address indexed _to, uint256 indexed _tokenId);

    // returns the functional owner of the held token
    function ownerOf(uint256 _tokenID) external view returns (address);

    // returns the address to the underlying held ERC721 asset
    function asset() external view returns (address);
}
```

Note: this would also implement `ERC165` so applications could easily check a contract for this interface.

Note: the method `ownerOf` was intentionally reused from `ERC721` so that contracts which fully wrap and tokenize a held NFT position can implement both `ERC721` and `ERC721Hold` without additional overhead.

Here is some example logic to check for the NFT owner while respecting the `ERC721Hold` interface

```auto
library {
    function getOwner(address addr, uint256 id) public pure returns (address) {
        IERC721 token = IERC721(addr);
        address owner = token.ownerOf(id);
        if (owner.isContract()) {
            try IERC165(token_).supportsInterface(0x00000000) returns (bool ret) {
                if (ret && IERC721Hold(owner).asset() == addr) {
                    return IERC721Hold(owner).ownerOf(id);
                }
            } catch {
                return owner;
            }
        }
        return owner;
    }
}
```

Really appreciate any thoughts or feedback!

Thanks all,

Devin

## Replies

**devinaconley** (2021-09-26):

Another aspect to consider is that contracts could potentially hold tokens from more than one NFT collection. In this case, the above interface would be too limiting.

To further generalize, something like this could used

```auto
interface ERC721Hold {

    // emitted when the token is transferred to the contract
    event Hold(address indexed _user, address indexed _tokenAddress, uint256 indexed _tokenId);

    // emitted when the token is released back to the user
    event Release(address indexed _user, address indexed _tokenAddress, uint256 indexed _tokenId);

    // returns the functional owner of the held token
    function functionalOwnerOf(address _tokenAddress, uint256 _tokenID) external view returns (address);
}
```

---

**devinaconley** (2021-10-06):

Twitter discussion for reference:



      [twitter.com](https://twitter.com/devinaconley/status/1441499642668064769)





####

[@devinaconley](https://twitter.com/devinaconley/status/1441499642668064769)

  I started an EIP discussion on a standard interface to represent NFT "functional ownership" when held by another smart contract. This is very relevant for many DeFi + NFT use cases.

Would love to hear any thoughts or feedback!
https://t.co/gPAkgg1Vf8

  [1:27 PM - 24 Sep 2021](https://twitter.com/devinaconley/status/1441499642668064769)






      26







      9

---

**devinaconley** (2021-10-31):

Hey Ron - thanks for the thoughts on this!

The use case you describe where the original owner lends an NFT to a temporary functional owner is a good one. And it is certainly supported by this proposed interface. The lending smart contract *functionalOwnerOf()* method would simply return the renter’s address.

The reason the NFT would be held by another smart contract is to enforce the mechanics of whatever system is being interacted with. The exact details of what/why would depend on the protocol or agreement.

You are right that application code would need to be updated to recognize this “held NFT” interface. That is the main motivation behind adopting a common standard like what is proposed here.

---

**MindfulFroggie** (2021-10-31):

Sorry for deleting the reply.

After submitting it I figured out I didn’t understand you correctly. Now I understand it much better ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

Basically the owner of the token would be a contract address where the token is being held, and that contract will hold the information regarding the true owner. Is that right?

I understand how the use case I described can be supported.

I was trying to think of a way of switching the owner in the ERC721 contract to point to the *true owner* but with limiting the transfer rights the owner has over the token. However I guess it is not possible as the `transferFrom` function will always accepts the transfer if the registered owner is the msg.sender.

Just to be sure, regarding your proposal, existing ERC721 contracts wouldn’t have to make any updates. Only 3rd parties looking for a true owner (in case of a contract owner) will need this “overhead”. And any 3rd party who wants to allow some DeFi or lending mechanisms, which will support the proposed feature, will need to implement the current ERC proposal. Is that correct?

So how can we advance this proposal? ![:face_with_monocle:](https://ethereum-magicians.org/images/emoji/twitter/face_with_monocle.png?v=10)

---

**devinaconley** (2021-11-01):

No problem, glad it is making sense now.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mindfulfroggie/48/4805_2.png) MindfulFroggie:

> Basically the owner of the token would be a contract address where the token is being held, and that contract will hold the information regarding the true owner. Is that right?

Right, according to the original ERC721 contract, the `ownerOf()` will be the smart contract holding the token.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mindfulfroggie/48/4805_2.png) MindfulFroggie:

> Just to be sure, regarding your proposal, existing ERC721 contracts wouldn’t have to make any updates

Exactly you are right on. This is designed to work with any existing ERC721. The overhead of adoption here is on DeFi mechanisms to implement the proposed standard interface and on third parties to recognize that standard.

Still collecting some more feedback, then will be opening up the actual EIP

---

**julesl23** (2021-11-01):

I think this is the better interface (the one with functionalOwnerOf).

This would then work for ERC-1155. Maybe then submit two interfaces or rename it so that it applies to both?

---

**MindfulFroggie** (2021-11-01):

To support ERC1155 (as well as ERC721) the interface should be modified.

The issue with ERC1155 is that (I think) it is a problem to look for the owner of a token ID, as there could be multiple owners in case that the token ID points to a fungible token.

I think it might make sense to retrieve the multiple possible owners, and to follow with a query of the balance of a specific owner.

Anyway I would suggest the following moidification for ERC1155 support:

```auto
interface ERCTokenHold {

    // emitted when the token is transferred to the contract
    event Hold(address indexed _user, address indexed _tokenAddress, uint256 indexed _tokenId, uint256 indexed _value);

    // emitted when the token is released back to the user
    event Release(address indexed _user, address indexed _tokenAddress, uint256 indexed _tokenId, uint256 indexed _value);

    // returns the functional owner (or owners) of the held token
    function functionalOwnerOf(address _tokenAddress, uint256 _tokenID) external view returns (address[]);

      // returns the functional balance of an owner for a specific token ID
    function functionalBalanceOf(address _tokenAddress, address _owner, uint256 _tokenID) external view returns (uint256);
}
```

In case of an ERC721 contract, the value can be ignored (and no use for the functionalBalanceOf function).

I guess this would also support ERC20? Ignoring the token ID.

---

**devinaconley** (2021-11-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/julesl23/48/4796_2.png) julesl23:

> This would then work for ERC-1155. Maybe then submit two interfaces or rename it so that it applies to both?

Yep, planning to submit two different interfaces for ERC721 and ERC1155

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mindfulfroggie/48/4805_2.png) MindfulFroggie:

> To support ERC1155 (as well as ERC721) the interface should be modified.

This could definitely work, but I think it feels cleaner to use explicit independent interfaces for each token type. This will also allow ERC165 responses to be more descriptive

---

**Daniel-K-Ivanov** (2021-11-03):

[@devinaconley](/u/devinaconley) I think that the proposal that you are describing addresses the same need as the [EIP-4400](https://ethereum-magicians.org/t/erc-4400-erc721consumer-extension/7371) that we submitted recently. I think that it would be interesting for you to check it out and get your feedback. I am curious to know whether the proposed 4400 standard will address your needs ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

Personally, I think that the overriding of the `owner` method is a dangerous direction, so moving to `functionalOwnerOf` is the right step.

I am excited to see that other people are recognising the need for such a standard as it would enable NFT lending/renting/staking!

---

**devinaconley** (2021-11-03):

Hey [@Daniel-K-Ivanov](/u/daniel-k-ivanov) - thanks for sharing that proposal. Likewise, glad to see other folks are looking seriously at this kind of standard.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/daniel-k-ivanov/48/4799_2.png) Daniel-K-Ivanov:

> I think that it would be interesting for you to check it out and get your feedback. I am curious to know whether the proposed 4400 standard will address your needs

EIP4400 (`ERC721Consumer`) definitely seems to be in the same spirit! But I think there are a couple key differences in the approach:

- this proposal puts the burden of reporting on the holding contract “owner”, where ERC721Consumer puts that burden on the token contract
- ERC721Consumer requires an upgrade for existing ERC721 tokens
- the bookkeeping for ERC721Consumer will likely have higher gas costs, as that is another dictionary to be managed during transfer, staking, sales, etc.
- the ERC721Consumer approach is probably more flexible for EOA usage without a smart contract

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/daniel-k-ivanov/48/4799_2.png) Daniel-K-Ivanov:

> Personally, I think that the overriding of the owner method is a dangerous direction, so moving to functionalOwnerOf is the right step.

Agreed on this ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

Overall, good to see another take on this problem. Definite pros and cons to each approach

---

**flaskr** (2022-02-10):

I agree that this is very different from EIP-4400 as these have a very large impact on the functionality:

> this proposal puts the burden of reporting on the holding contract “owner”, where ERC721Consumer puts that burden on the token contract
> ERC721Consumer requires an upgrade for existing ERC721 tokens

I was playing around with a variant of this with time-based ‘hold’, while wrapping the ‘hold/lend’ as a ERC721 itself. I think that the functionality (payment/lending) that I’m looking for can be built on top of what you’re proposing. I’m using `virtualOwnerOf` to make it distinct from `ownerOf` function.



      [github.com](https://github.com/flaskr/nft-lend-v2)




  ![image](https://opengraph.githubassets.com/6ba3450a2e67a5bb5a7019a87e0153f9/flaskr/nft-lend-v2)



###



Non-custodial NFT lending via pseudo-ownership










Let me know if you’ll like some examples done or if you’re looking for help to write/push this forward!

---

**devinaconley** (2022-02-10):

Hey [@flaskr](/u/flaskr) - thanks for the feedback on this. Great to hear that this proposed interface would fit with your use case and need for an associated standard.

Appreciate that! I am actually working on the EIP draft and a code example now, which should be wrapped up this weekend. Would be great to include another example from your side as well.

I’ll keep you posted here.

---

**devinaconley** (2022-02-10):

Would be great to get some thoughts on naming convention here. The idea is that all interface functions will be named with this prefix (e.g. in the `ERC1155` case, `heldOwnerOf` and `heldBalanceOf`)

What function prefix(es) do you prefer?

- heldOwnerOf
- tokenOwnerOf
- functionalOwnerOf
- virtualOwnerOf
- delegateOwnerOf

0
voters

---

**flaskr** (2022-02-10):

I do think that ‘heldOwnerOf’ isn’t very readable as a sentence. `functionalOwner` has my vote. I just added support for EIP-165 and “cross-ERC721Hold” owner queries to my repo.

**On interface between ownerOf(id) and ownerOf(address, id)**

Personally, I prefer the interface to be specific to a single ERC-721. This is because I would like the option to implement the ‘functional ownership’ as an ERC-721 itself - being able to transfer/sell your lease can be very powerful. It’s possible to add in the `ownerOf(address, id)` function to an ERC-721 wrapper but it looks pretty redundant. Having to support the extra address calldata might cost extra gas too.

I also envision a separate contract or interface that allows people to check `ownerOf(address, id)`. Why not have 2 interfaces? A contract could implement both if it wants to, but it keeps one from polluting the other.

eg.

ERC721Hold

- ownerOf(id)

ERC721ManyHold

- ownerOf(tokenAddress, id)

I would also like one for ERC1155 but the scope might be too big.

---

**devinaconley** (2022-04-01):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/f/7ba0ec/48.png) flaskr:

> This is because I would like the option to implement the ‘functional ownership’ as an ERC-721 itself - being able to transfer/sell your lease can be very powerful.

I actually mentioned the possibility of reusing the `ownerOf` method for a tokenized position in the initial post. The consensus was that overriding this method from two different interfaces was a little hacky/dangerous

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/f/7ba0ec/48.png) flaskr:

> I also envision a separate contract or interface that allows people to check ownerOf(address, id). Why not have 2 interfaces? A contract could implement both if it wants to, but it keeps one from polluting the other.

One challenge with using separate interfaces is that a calling method would need to check two different interface identifiers to look up functional ownership

---

**devinaconley** (2022-04-07):

Just wrapped up an example implementation of the proposed standard here



      [github.com](https://github.com/devinaconley/token-hold-example)




  ![image](https://opengraph.githubassets.com/09466d26c4c67040dac8f0d0d50ec0b3/devinaconley/token-hold-example)



###



Reference implementation for EIP on held token standard

---

**devinaconley** (2022-04-11):

And submitted the proposal draft for this held token standard here

https://github.com/ethereum/EIPs/pull/4987

---

**SamWilsn** (2022-04-14):

Looking good so far, and apologies if this has already been covered, but if a holder contract holds both an ERC-20 and an ERC-721, what happens?

Would it possibly make more sense to just have a single function per operation (ex. `heldBalanceOf(address owner, address token, uint256 tokenId)`) where `tokenId` is always `0x0` for ERC-20s?

---

**devinaconley** (2022-04-14):

Thanks for the review [@SamWilsn](/u/samwilsn) ! Addressing your feedback and suggestions now.

The thinking behind separate interfaces for each token type is that any consumer logic will usually only want to query held token info on a specific token type at a time.

In the case of a contract holding both ERC-20 and ERC-721, the `heldBalanceOf(address owner, address token)` is actually the same signature.

If a contract is also holding ERC-1155, the function could be overloaded with `heldBalanceOf(address owner, address token, uint256 tokenId)`. The consumer would hit the appropriate signature depending on the interface of interest.

---

**devinaconley** (2022-04-14):

[@SamWilsn](/u/samwilsn) your feedback on events brings up another good question. I think there’s a case to be made that this interface should not require any events to be emitted.

One of the main goals is for this interface to be extremely lightweight and non-intrusive. Additional events/gas doesn’t help with that

Plus, we could arguably get all the equivalent data by indexing underlying token `Transfer` events and filtering where `to` or `from` match our holder of interest


*(12 more replies not shown)*

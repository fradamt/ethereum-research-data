---
source: magicians
topic_id: 14244
title: "ERC-7015: Creator Attribution for ERC721"
author: strollinghome
date: "2023-05-11"
category: ERCs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/erc-7015-creator-attribution-for-erc721/14244
views: 4584
likes: 11
posts_count: 29
---

# ERC-7015: Creator Attribution for ERC721

A standardized event to attribute ownership for ERC721 NFTs. Currently, platforms assume the wallet submitting the deploy transactions is the author/creator, but that is not always true. This EIP seeks to standardize the way we validate and attribute authorship.

https://github.com/ethereum/EIPs/pull/7015

## Replies

**HardlyDifficult** (2023-05-15):

today we lean on getters to identify the creator - `tokenCreator(uint256 tokenId)` or `owner`/admin. originally we were hoping to see the former, or something similar, become widely adopted. but as we open up, we’d be vulnerable to spoofing since the contract could return or emit any address.

this seems like a good approach to attribution without needing to trust the factory or underlying implementations. it’s unfortunate that we’d need to include a second prompt when creating collections, to get their 712 signature - so would need to talk it over with the product team to see if we have appetite for this before we integrate.

EIP-1271 support is a good call out to include (mentioned in offline discussion). some other thoughts on this eip:

- The spec suggests this is only for creation time. Seems worthwhile to support changes too - the contract could just emit the same event again after any additional checks (such as approval from the original owner). Creators occasionally migrate to a more secure wallet, it may be nice to reaffirm their latest address
- If it’s a collab, should we emit once per author? Seems like that should be okay - but makes me wonder if something more should be included for the account migration scenario to indicate the original is invalid…
- Some of the fields seem redundant - e.g. why address token in the struct when that’s already in the domain? why emit token and verifyingContract when they are both the emitting contract (which is returned with the log from RPCs)? or could you clarify how this could be emitted by a contract other than the collection itself (or do we reject events where these fields do not match)?

---

**strollinghome** (2023-05-15):

> The spec suggests this is only for creation time. Seems worthwhile to support changes too - the contract could just emit the same event again after any additional checks (such as approval from the original owner). Creators occasionally migrate to a more secure wallet, it may be nice to reaffirm their latest address

My intuition is that managing “authors” post-deployment is most likely cumbersome and possibly unnecessary, given that the author is not the same as the “admin/owner” of the NFT. A way this could be used is, say, if a creator has a multisig but usually manages things with an EOA, the author can be the multisig, but the EOA can have all the permissions to make changes on the NFT.

One way it could make sense to have post-deployment authorship management is if there were different authors for each `tokenId`. The EIP, for now, is meant to attribute authorship for all tokens in the contract to the same author.

> If it’s a collab, should we emit once per author? Seems like that should be okay - but makes me wonder if something more should be included for the account migration scenario to indicate the original is invalid…

This is a very valid point. Multiple authors will require multiple signatures for the same message and multiple events. I believe this could work out of the box with the same definition; we can extend it to include multiple events with the same parameters but different signatures. I’ll think through the details and post an update.

> Some of the fields seem redundant - e.g. why address token in the struct when that’s already in the domain? why emit token and verifyingContract when they are both the emitting contract (which is returned with the log from RPCs)? or could you clarify how this could be emitted by a contract other than the collection itself (or do we reject events where these fields do not match)?

Requiring the `token` parameter in the struct ensures that the signature is only used once and prevents spoofing. Otherwise, an attacker could redeploy a token with the exact same parameters, generating a different NFT contract that they control.

There are two approaches to signature verification: through a factory and through the token itself. However, after your comment, I think we should simplify this to require the token to perform the signature verification; that way, we can remove `verifyingContract` from the event.

---

**sprice** (2023-05-21):

I just found this EIP proposal after submitting the post here last week and opening up [EIP-7050](https://github.com/ethereum/EIPs/pull/7050) today.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sprice/48/9532_2.png)
    [EIP-7050: NFT Creator Provenance Standard](https://ethereum-magicians.org/t/nft-creator-provenance-standard/14259) [EIPs](/c/eips/5)



> @depatchedmode and I have been talking about explicit creator provenance on NFTs and we believe there is space for a new standard.
> We propose a new ERC aimed at establishing clear, explicit, and verifiable provenance for creators of NFTs. Current NFT interfaces and marketplaces often implicitly attribute the role of ‘creator’ either to the contract deployer or to the first minter of the NFT. However, this approach has led to inconsistencies and ambiguities, particularly as some NFTs are viewed …

I had originally searched here for `provenance` and `creator` and a handful of other keywords but this didn’t come up ![:man_shrugging:](https://ethereum-magicians.org/images/emoji/twitter/man_shrugging.png?v=12)

Looks like we’re both approaching the same desired destination via different paths ![:smiley_cat:](https://ethereum-magicians.org/images/emoji/twitter/smiley_cat.png?v=12)

> today we lean on getters to identify the creator - tokenCreator(uint256 tokenId) or owner /admin. originally we were hoping to see the former, or something similar, become widely adopted. but as we open up, we’d be vulnerable to spoofing since the contract could return or emit any address.

This is our approach in ERC-7050. We allow the contract owner to set who the creator of a token is, and then require the creator address to call `verifyTokenProvenance(tokenId)`. Only if the contract owner has set their address as the creator of `tokenId` will the contract state be updated so that a call to `provenanceTokenInfo(tokenId)` returns `(creatorAddress, isVerified)` (where `isVerified` will be `true`).

We expect this can be extended to handle both batches of tokenIds and to cover an entire contract as well.

We’ve taken this approach as the goal is to call a contract function. ie: as a Dapp developer I want to call `provenanceTokenInfo ` in my code so it’s easy to list one or more NFTs with explicit creator info.

1. Shall we team up?
2. Is there a good reason to have events AND the equivalent of tokenCreator() as different EIPS?
3. Have we overlooked something that makes our approach in ERC-7050 a poor tool for this job?

---

**strollinghome** (2023-05-22):

Here are a few thoughts on why I don’t necessarily think we need to have setter/getters for authors:

- When it comes to provenance, in the most practical sense, I don’t believe the “author” necessarily changes. The author is the creator of the piece. I understand getters/setters for the provenance of specific tokens, that’s what 721 is, but even then, there’s no record-keeping of the chain of ownership other than through emitted events (the same approach ERC-7051 takes).
- The current specification for ERC-7050 is easily spoofable, there’s no method for verifying a certain wallet-x is the true creator of a token, one can easily create a getter method that returns wallet-x.eth as the creator. To truly verify that wallet-x.eth is the creator, you would need to inspect all transactions submitted to the contract and verify that indeed wallet-x.eth called verifyTokenProvenance. One needs to trust the NFT contract is not behaving maliciously. ERC-7051 uses signatures to validate ownership, it makes for a better UX (the creator doesn’t need to own any ETH), since the transaction can be submitted and anyone can verify the authorship. That’s why the signature is emitted in the event.
- Storing signatures on-chain is expensive, and to have a getter/setter that can be truly verified, we’d need to store signatures onchain and return them along with the provenance-token-info (more like ERC-5375 in terms of interface, the specification stores data offchain). Something I don’t think it’s truly necessary. Curious why the need to be able to query for token provenance offchain? I see a potential argument to be able to do it onchain (say from a different contract) for composibility or redirecting funds, but I think a better approach would be to use some sort of splitter contract. But when it comes to querying it from offchain, we could just look at the events emitted previously. ERC-7015 doesn’t specify change of “authorship” as per my first point above.
- I can see the need for multiple authors, ERC-7015 does specify a way to attribute authorship to multiple wallets, however, it doesn’t specify tokenIds. This is something I’m still considering but I think it would make a good addition. I will follow up with some changes regarding this.

---

**sprice** (2023-05-22):

Since posting the proposal for ERC-7050, we’ve also discovered ERC-5375 which is similar in goal. How does this proposal differ and how is it similar to the proposed ERC-7015 discussed here?



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5375)





###



An extension of EIP-721 for NFT authorship and author consent.

---

**sprice** (2023-05-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> When it comes to provenance, in the most practical sense, I don’t believe the “author” necessarily changes. The author is the creator of the piece. I understand getters/setters for the provenance of specific tokens, that’s what 721 is, but even then, there’s no record-keeping of the chain of ownership other than through emitted events (the same approach ERC-7051 takes).

Agreed that authorship does not change.

As far as I know, we currently don’t have explicit getters/setters for the provenance of explicit tokens and that is part of what the proposed ERC-7050 aims to do.

The chain of ownership is outside the scope of what the proposed ERC-7050 aims to cover.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> (the same approach ERC-7051 takes).

I assume you mean ERC-7015 here ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> The current specification for ERC-7050 is easily spoofable, there’s no method for verifying a certain wallet-x is the true creator of a token, one can easily create a getter method that returns wallet-x.eth as the creator.

In the current draft proposal, only the owner of the contract can set who the author is, and only the author can successfully call `verifyTokenProvenance`. I don’t follow how this is spoofable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> To truly verify that wallet-x.eth is the creator, you would need to inspect all transactions submitted to the contract and verify that indeed wallet-x.eth called verifyTokenProvenance.

If the author is the only one that can successfully call `verifyTokenProvenance` why is this needed?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> ERC-7051 uses signatures to validate ownership

I assume you mean ERC-7015 here ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> it makes for a better UX (the creator doesn’t need to own any ETH)

An author proving their authorship without owning ETH is a fantastic UX

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> Curious why the need to be able to query for token provenance offchain?

If I communicated this need I think it was in error. I don’t believe I did.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> I can see the need for multiple authors

100% multiple authors is important.

---

**cminxi** (2023-05-24):

I agree that we need a standard for determining the creator of a given NFT!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> author/creator

I’m curious why the nomenclature of `author`? `creator` seems to be a widely used and understood term in the NFT space already, and is a broadly understood concept. It also doesn’t collide with the concepts of “minter” of the NFT, “deployer” of the NFT contract, or owner of the NFT. Also, the EIP itself defines the author as “`the creator of an NFT`”, so it seems like `creator` might be the simplest and most appropriate term to use here.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> I see a potential argument to be able to do it onchain (say from a different contract)

I agree here, and believe adding a getter would be helpful in making this EIP more widely adopted. I agree this getter could easily be spoofed.

I’m having trouble understanding how the spoofing of the getter would be functionally different from the spoofing of the emitted events already included in the EIP. For both the EIP’s existing events and a potential getter, wouldn’t the party interacting with the NFT contract ultimately have to trust and/or verify that the creator’s signatures are being verified properly by reading the source code of the contract itself?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> Multiple authors

I would propose it’s easier to keep this idea simple and only allow for “one” author. I believe allowing for multiple introduces lots of surface area for complexity (if you have multiple, how can you be sure you’ve queried all of them, is there a hierarchy amongst them, etc). By allowing for only one account to be the author, you allow the proposed EIP to be simple and also push the responsibility of explaining the complexities of a multi-author situation to the author themselves. For example, a single author could actually be a smart contract, which itself further elaborates on the multiple authors, etc.

We have seen similar issues play out with ERC-721’s `ownerOf`, which, by only allowing for one owner, pushed the complexities of collective ownership, fractionalization, etc. to the owner. Ultimately, I think this contributed to the success of ERC-721.

---

**strollinghome** (2023-05-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cminxi/48/9572_2.png) cminxi:

> I’m curious why the nomenclature of author? creator seems to be a widely used and understood term in the NFT space already, and is a broadly understood concept. It also doesn’t collide with the concepts of “minter” of the NFT, “deployer” of the NFT contract, or owner of the NFT. Also, the EIP itself defines the author as “the creator of an NFT”, so it seems like creator might be the simplest and most appropriate term to use here.

Yeah, creator sounds better. I’m good with using that!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cminxi/48/9572_2.png) cminxi:

> For both the EIP’s existing events and a potential getter, wouldn’t the party interacting with the NFT contract ultimately have to trust and/or verify that the creator’s signatures are being verified properly by reading the source code of the contract itself?

So two things; first, ERC-7050 doesn’t specify signatures, so there’s no way to verify a creator has given consent without inspecting that the creator submitted a transaction that was intended to do what the ERC specifies. Second, for ERC-7015, it is a requirement for validating attribution offchain that the event is emitted from the `token` contract **and** matches the same `token` address that was *signed* by the creator. So even if I take a signature that belongs to someone else and emit it from a new contract that I deployed in an attempt to spoof creator attribution, I would have to figure out a way to deploy a contract with my own malicious logic at the exact same address as the `token` signed. In practice, since the `token` signed has to be generated before the signature, there are two ways to generate a `token` address:

- Using a factory contract that will deploy ERC721s with create2
- Using an EOA and with the nonce predicting the next address that will be deployed.

In the first case, it is impossible with `create2` to deploy a token contract with a different `implementation` than the one used to generate the `token` address and still get the same `token` address. This also assumes that the attacker has access to specifying *which* implementation to use within the factory to deploy the contract. The key thing to understand is that we’re using the `implementation` logic as an input to generate a `token` address – so there’s a guarantee of what the intention of the creator was. For all intents and purposes, spoofing this way is impossible.

In the second case, there is no way to encode or use the `implementation` logic as input into the `token` address since the EOA can deploy any logic and still get the same `token` address. However, this attack vector assumes the attacker has somehow acquired access to the EOA that will deploy the contract – something we cannot prevent with the ERC specification.

Both approaches suffer from creators signing messages unintentionally, but we cannot prevent this, and this is also specified in **Security Considerations** section. I can add these considerations to the specification and also recommend using a factory and `create2` as the preferred method of implementation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cminxi/48/9572_2.png) cminxi:

> I would propose it’s easier to keep this idea simple and only allow for “one” author.

The spec currently supports multiple creators; it only starts adding complexity when you think of *which* token ids specific creators created since there’s really no way to specify multiple creators for a token id; hence I agree with you that we can push that complexity into the accounts. And it would simplify other aspects. For example, with the current support for multiple creators, if, say, a new token id is added, and we want to signal that there’s an additional creator, we’d have to support emitting the event on a transaction *after* deployment. In which case, if you’re looking for all the creators of the NFT, you’d have to search all transactions for `AuthorAttribution` (soon `CreatorAttribution`) events instead of just the deployment transaction.

I am still unconvinced we need to add getters to this ERC and much less setters since that creates more complexities. The purpose of the ERC is to signal the correct creator in a simple and **verifiable** way during the deployment transaction. The currently proposed alternatives do not provide a verifiable way of proving who the creator is because they lack signatures. They also hinge on the idea of a contract *owner*, which is merely a convention and not a standard, and even then, it is still easily spoofable.

Edit: one caveat is that changing the byte code and still get the same address could be done with metamorphic contracts, but as I mentioned above the attacker must also acquire access to the factory that deploys the contracts. This is most likely to happen if the attacker gets the creator to provide a signature directly to them rather than stealing a signature that was meant to be used by a different system. We can’t protect against creators signing unintended payloads from untrusted sources.

---

**sprice** (2023-05-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> The purpose of the ERC is to signal the correct creator in a simple and verifiable way during the deployment transaction.

Is the scope of this EIP around things happening up until the ERC721 contract has been deployed and not related to things after that? ie: Emit certain events on contract deployment. Not emit events after contract deployment.

Also, in [EIP-750](https://ethereum-magicians.org/t/eip-7050-nft-creator-provenance-standard/14259), although the NFT extension is designed so that it’s only possible for the person(s) or machine(s) which set the metadata of each token to set the address which is the creator, and then only possible for that creator address to accept authorship, it is becoming clear that signatures can be useful. We’ll explore some good ways to do that.

---

**oveddan** (2023-06-30):

Thanks for putting together this great proposal.  Definitely helps address the problem of most places using the tx.origin as the “creator” instead of the contract creator, which becomes an issue when a creator wants to sign a message to create a token that someone else executes.

have some feedback/thoughts.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> Requiring the token parameter in the struct ensures that the signature is only used once and prevents spoofing. Otherwise, an attacker could redeploy a token with the exact same parameters, generating a different NFT contract that they control.

Isn’t the `token` parameter the same as the [verifyingContract param](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/EIP712.sol#L90) that is part of the domainSeparator in EIP712?  When would it be different?   Even if they deployed the token again, it would have a different address and the signature would be invalid if the contract address changes  regardless of whether or not you had a `token` parameter because the verifying contract address would change in the domain separator.

Now regarding the signed message with the format:

```auto
 bytes32 public constant TYPEHASH =
        keccak256(
            "CreatorAttribution(string name,string symbol,bytes32 salt,address token)"
        );
```

This removes flexibility in implementing this EIP as it forces the contract to have its signature for token creation in a specific format with a specific name.

Signatures for token creation serve the following purpose:

- validate that the token creation parameters are correct, and match what the creator intended
- validate that the creator signed the message.

So having the name `CreatorAttribution` as the domain name implies that the purpose of the signature is to attribute the token to the creator, but really it has more than that purpose, also to validate that the token creation params are correct and to ultimately create the token.

I’d like towards a name of `TokenCreation` and I’d rename `salt` to `params`.

Also, another approach would allow the structHash (abi encoded domain + arguments) to be made in any eip712 compatible format, and leaving it up to the developer of the contract to ensure that they follow that format and that the message signed contains all necessary parameters, include the entire structHash.  This would give developers more flexibility to build the arguments to their signature the way they want and allow the existing signatures in their contracts to work with this standard.  You’d still get the benefits that:

- signer of the message signed the message for the verifying (token) contract on the correct chain.
- all data in the event can be used to verify the signature was signed by the creator.

Something like this:

```auto
pragma solidity 0.8.19;

import "openzeppelin-contracts/contracts/utils/cryptography/EIP712.sol";
import "openzeppelin-contracts/contracts/interfaces/IERC1271.sol";

abstract contract ERC7015 is EIP712 {
    error Invalid_Signature();

    event CreatorAttribution(string name, string symbol, bytes32 structHash, string domainName, string version, address creator, bytes signature);

    constructor() EIP712("ERC7015", "1") {}

    function _validateSignature(bytes32 structHash, address creator, bytes memory signature) internal {
        if (!_isValid(structHash, creator, signature)) revert Invalid_Signature();

        emit CreatorAttribution(name, symbol, structHash, "ERC7015", "1", creator, signature);
    }

    function _isValid(bytes32 structHash, address signer, bytes memory signature) internal view returns (bool) {
        require(signer != address(0), "cannot validate");

        bytes32 digest = _hashTypedDataV4(structHash);

        address recoveredSigner = ECDSA.recover(digest, signature);

        return recoveredSigner == signer;
    }
}
```

---

**strollinghome** (2023-07-03):

Hey Dan, thanks these are all very good suggestions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oveddan/48/9909_2.png) oveddan:

> Isn’t the token parameter the same as the verifyingContract param that is part of the domainSeparator in EIP712?

You’re right. The `token` parameter is encoded into the `domainSeparator`; an earlier iteration of the EIP had the signature validation performed in a factory contract, so I included the `token` parameter. When we moved the signature verification to the token to accommodate direct deployments (no need for factories), it became unnecessary to include the `token` parameter in the event. I will update the EIP to reflect this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oveddan/48/9909_2.png) oveddan:

> I’d like towards a name of TokenCreation and I’d rename salt to params.

Cool with this; renaming makes sense to me.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oveddan/48/9909_2.png) oveddan:

> Also, another approach would allow the structHash (abi encoded domain + arguments) to be made in any eip712 compatible format

This is interesting; if we were to take this route, I wonder if you think it makes sense to remove the `name` and `symbol` parameters from the `CreatorAttribution` event and expand the EIP to support ERC-1155 NFTs as well. Given that those two parameters are not top-level params on 1155, I first decided to restrict this EIP to 721s, but if we’re being more flexible with the signed hash, it could also support 1155s. However, at that point, the struct has just one parameter, `bytes32 params` – which feels a bit off since it’s no different from signing a single message hash and obscuring things a lot, making it easier for users to sign unintended messages. At the same time, we should try to make it as general as possible for wider adoption. Do you have any thoughts on this?

And one more thing I’m wondering, I think it makes sense to also remove `creator` from the emitted event and just let indexers assume that the recovered signer is the creator. Having the parameter in the event would only leave open the possibility of a mismatch between the emitted creator and the recovered signer, but in the end, what matters is the recovered signer.

---

**kartik** (2023-07-06):

Some thoughts from me.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/strollinghome/48/9450_2.png) strollinghome:

> Given that those two parameters are not top-level params on 1155, I first decided to restrict this EIP to 721s, but if we’re being more flexible with the signed hash, it could also support 1155s. However, at that point, the struct has just one parameter, bytes32 params – which feels a bit off since it’s no different from signing a single message hash and obscuring things a lot, making it easier for users to sign unintended messages. At the same time, we should try to make it as general as possible for wider adoption. Do you have any thoughts on this?

IMO ERC-1155 should be included and if we’re including it, then the standard should be more generic than NFT use cases. Ultimately what this is accomplishing is a standard for attributing a contract creator, where in the NFT case all tokens minted on the contract are defined to be created by the contract creator.

I don’t really see a reason this needs to be NFT-specific.

---

Still contemplating it, but I think it might make sense to allow this attribution to be dynamic and updatable by the contract owner. This means supporting setters/getters and not restricting it to be set via the constructor.

I think getters would make it easier for wider adoption, i.e. Ownable. For example, supplying the relevant data via `creatorMetadata()` and leaving it up to the client to verify. I think the trade-off on ease-of-use vs cost is worth it.

Similarly a use case I can think of for setters is to onboard wallet-less creators. First collector deploys the contract and mints, and later on the creator claims ownership of the contract and sets their new wallet as the creator, something we’ve been exploring with [EIP-6981](https://eips.ethereum.org/EIPS/eip-6981).

---

Collabs are important imo and the current approach makes sense to keep it light. Might be worth explicitly calling this out in the EIP. If we wanted to add getters then I think spec should be changed to support arbitrary number of creators. (In general this is even more important if we’re switching to a more generic standard).

---

**Vectorized** (2023-07-06):

Suggestions:

- Instead of a name and symbol, just have a single message.
- Rename salt to params, or alternatively allow any EIP-712 structHash that incorporates the token address.

```auto
emit CreatorAttribution(message, structHash, "ERC7015", "1", creator, signature);
```

---

**oveddan** (2023-07-21):

The recent update is great. I would suggest a few minor tweaks:

As [@Vectorized](/u/vectorized), mentioned, I’d rename `params` to `structHash` to align more with what the `EIP-712` standard calls it and what devs are used seeing, and also what the openzeppelin contract calls the argument.

I would also show a more concrete example that looks more like what a real contract would look like: taking explicit args (such as token id, name, etc), building the `structHash` by hashing a const `DOMAIN` + those params, then calling `_hashTypedDataV4` with those params.  It would be nice to show how this would work with both erc721 + erc1155, so to show an erc721 and erc1155 example would be great.

---

**oveddan** (2023-07-21):

Regarding:

> This is interesting; if we were to take this route, I wonder if you think it makes sense to remove the name and symbol parameters from the CreatorAttribution event and expand the EIP to support ERC-1155 NFTs as well. Given that those two parameters are not top-level params on 1155, I first decided to restrict this EIP to 721s, but if we’re being more flexible with the signed hash, it could also support 1155s. However, at that point, the struct has just one parameter, bytes32 params – which feels a bit off since it’s no different from signing a single message hash and obscuring things a lot, making it easier for users to sign unintended messages. At the same time, we should try to make it as general as possible for wider adoption. Do you have any thoughts on this?

Yeah I can see the issue with that. One possible approach would be to have two separate events, one for erc1155 and one for erc721 with erc1155/erc721 specific fields.

However I still see the issue that sometimes the signed message needs to contain more than the name and symbol; for example if there are not auto-incrementing ids, then the token id needs to be included.  Or if there are pricing settings (i.e. how much this token costs) you need to include that in the signature.

I suppose this could be accomplished with:

params = hash(tokenId, price)

structHash = hash(DOMAIN, name, symbol, params)

I think both approaches are fine, but whatever the final approach is I’d try to include support for erc1155 which has exploded in popularity recently with the rise of open editions

---

**oveddan** (2023-07-31):

On further thought it actually may make sense to include the contract address in the event; this would allow the signature to be created against other contracts than the token contract itself;

Let’s say for example, you have a factory contract that is granted permission to create tokens on an erc721 or erc1155 contract on behalf of a creator; the creator would sign a message that the factory contract would validate.  In this case; you’d want to have some contextual awareness of the address of the factory in the event;

If the factory was to emit the `TokenCreation` event, would that still be recognized? Or would the approach to support this to be to have the TokenCreation event emitted from the contract, but add the validating contract (in this case the factory’s) address to the event?

---

**strollinghome** (2023-07-31):

This was the original design, and moving the validation logic to the token contract was made so the standard could also be supported when deploying directly through a contract creation transaction. I want to keep it that way, and I think it makes the most sense that the token contract also emits the TokenCreation. What are some of the reasons you’d rather have the signature be made for the factory contract?

---

**mpeyfuss** (2023-08-02):

Has there been any discussion into making this queryable on-chain as well? I could see this being extremely helpful for marketplaces when trying to determine the difference between a primary and secondary sale, as one example. There are probably other use cases for on-chainness (if that’s a word).

---

**0xTranqui** (2023-10-10):

Excited about this proposal’s ability to improve DX when it comes to facilitating token-based information exchange.

I am disappointed that there is no ability to specify creator attribution at the `tokenId` level. This is relevant for app-level shared token contracts and small-group/collective owned contracts, where the ability to group all activity under one contract while still enabling tokenId-level attribution would be a nice improvement.

I think the simplest way to enable this without making edits to the existing implementation would be to allow for the emission of additional `CreatorAttribution` events post contract deployment that include hashed tokenId(s) in the `structHash`. It could be assumed that if only one event is emitted during the token contracts lifecycle that all tokenIds should be attributed to the `creator` specified in the original event, while follow up events could signal overrides for whatever tokenIds are included in the their respective `structHashs`.

Not sure how close this is to finalization but think this could be a reasonable fix (doesnt change anything at the impl level besides getting indexers onboard + providing an additional example) if others are interested. I for one am!

---

**montasaurus** (2023-10-13):

Thanks for talking through the design with me on this [@strollinghome](/u/strollinghome)! Here are the main pieces of feedback we had while working on support for the draft version at OpenSea.

## EIP 1271 Support

We discussed this one, but wanted to repeat it here. In order to support validating 1271 signatures, we needed the `creator` address added to the log. Thanks for including that! This will allow support for SCW and multi-sig creators.

Note for anyone else implementing verification that you can’t just `ecrecover` and use that address directly, since it may be an EOA signing for a different address using 1271.

## 712 Payload / Phishing

The 712 payload included in the spec confused me & I believe might enable an abuse vector.

From the spec:

> Creator consent is given by signing an EIP-712 compatible message; all signatures compliant with this EIP MUST include all fields defined. The struct signed is:

```solidity
struct TokenCreation {
	bytes32 structHash;
}
```

Reading that, I was expecting the primary type of the 712 payload to be `TokenCreation` with an included `structHash`. I think what is intended (as written) is for the `structHash` to replace `hashStruct(message)` from the 712 spec, allowing any arbitrary 712 message payload. From the comments above, it looks like this was changed to allow flexibility in the payload for factory contracts.

The issue I see is that this enables contracts to present any signature on the verifying domain (e.g. sign in messages) as a creatorship attestation. This will make phishing these signatures much easier since the user signing them won’t be able to tell what the signature is being used for.

A specific and explicit 712 signature for a creatorship attestation would make this more robust and less prone to abuse. Factory contracts could still support this by prompting the user to sign the specific creator attestation, and then including that signature in the (potentially also signed) payload for the contract creation.


*(8 more replies not shown)*

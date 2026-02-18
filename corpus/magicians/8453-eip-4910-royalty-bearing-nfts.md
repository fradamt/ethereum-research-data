---
source: magicians
topic_id: 8453
title: "EIP-4910: Royalty Bearing NFTs"
author: highlander
date: "2022-02-28"
category: EIPs
tags: [nft, token, royalties]
url: https://ethereum-magicians.org/t/eip-4910-royalty-bearing-nfts/8453
views: 6240
likes: 6
posts_count: 25
---

# EIP-4910: Royalty Bearing NFTs

---

EIP: 4910

Title: Royalty Bearing NFTs

Description: This proposal outlines the structure of an extension of the ERC721 standard for NFTs to correctly define, process, and pay (hierarchical) onchain royalties from NFT sales, and goes beyond [EIP-2981](https://eips.ethereum.org/EIPS/eip-2981).

Author: Andreas Freund (@Therecanbeonlyone1969)

Status: Final

Type: Standards Track

Category: ERC

Created: 2022-02-17

Requires: ERC721, ERC165

---

[Link to Final EIP Version](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-4910.md)

This submission is dedicated to my children Lilith and Oliver.

## Replies

**vigilance** (2022-03-17):

Please check out, [EIP-2981: NFT Royalty Standard](https://eips.ethereum.org/EIPS/eip-2981). A **final** tracked ERC already exists with a similar name, topic and content.

---

**highlander** (2022-03-17):

[@vigilance](/u/vigilance) thank you for your comment. … fully aware of EIP-2981 … EIP-2981 is a signaling standard for royalty data to be paid offchain as e.g. Opensea does. This proposal (now EIP-4910) is totally different. The royalties are not only calculated and paid out onchain, but also multiple royalty recipients per NFT are possible, and when NFTs are organized in hierarchies/families/trees this proposal allows the proper distribution across a hierarchy/family/tree.

Reference implementation is here: [GitHub - treetrunkio/treetrunk-nft-reference-implementation: This is the open source reference implementation of the proposed ERC following from the TreeTrunk.io project.](https://github.com/treetrunkio/treetrunk-nft-reference-implementation) … check it out!

---

**SamWilsn** (2022-04-06):

Would you mind replacing the original post with a link to the PR? Much appreciated!

---

I have only glossed over the EIP so far as an editor (and I can’t promise I’ll ever completely understand it) but my number one question with these kind of ideas is how do you enforce that royalties are paid at all? Assuming “royalties” in this case means a percentage fee of the sale price.

Can’t someone just wrap the NFT in another NFT, and trade that one?

---

**highlander** (2022-04-06):

Sure will do.

And very good question. When you look at the specification you will see that the owner in the contract sense is the smart contract and the actual owner is approved, and, furthermore, the address to which the token is transferred cannot be a contract address. Therefore, circumventing royalty payments is not possible. This is also discussed in the security considerations of the spec.

Hope this answers your question.

---

**SamWilsn** (2022-04-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/highlander/48/2923_2.png) highlander:

> the address to which the token is transferred cannot be a contract address

This is surprisingly difficult to enforce, and generally isn’t a great idea, especially since it’s looking increasingly likely that we’re going to move to a smart contract wallet world.

I took a quick look through the reference implementation to see how you enforce this, but didn’t find it. As far as I know, the only way to be absolutely certain that an account is a true EOA is to have it sign a message and ECRECOVER from it.

---

**highlander** (2022-04-06):

It is indeed not trivial. Here are the places:

Constructor:

```auto
require(_msgSender() == tx.origin, 'Caller must not be a contract');
require(!creatorAddress.isContract(), 'Creator must not be a contract');
```

This ensures that a deployer cannot be a contract.

Minting:

```auto
require(hasRole(MINTER_ROLE, _msgSender()) || hasRole(CREATOR_ROLE, _msgSender()), 'Minter or Creator role required');
        //ensure to address is not a contract
        if (to == _msgSender()) {
            require(tx.origin == to, 'To must not be contracts');
        } else {
            require(!to.isContract(), 'To must not be contracts');
        }
```

In combination with the role requirement for `_msgSender()`, you can ensure the `to` is not a contract since `to` must exist before the transaction is sent.

Similar constructions as above for the `safeTransferFrom` and `_safeTransferFrom` functions plus whitelisting capability of trusted contracts. We also noticed that we missed the treatment of the `receiver` address and plugging that hole rn including tests. Will update PR in a couple of days once that is done. And you are right, we could force a signature. However, if a grandparent wants to buy an NFT for their grandchild, we cannot very well ask the grandchild for the signature in advance if it is a surprise. So we will use the combinatorial approach above to address the no-contract issue.

---

**SamWilsn** (2022-04-06):

As far as I know the `msg.sender == tx.origin` check will (as far as I know) ensure the address is an EOA *today*. OZ’s `isContract` is trivially defeated. From their documentation:

```auto
     * Among others, `isContract` will return false for the following
     * types of addresses:
     *
     *  - an externally-owned account
     *  - a contract in construction
     *  - an address where a contract will be created
     *  - an address where a contract lived, but was destroyed
```

The two easiest attacks are using `CREATE2` and calling from inside a constructor.

---

Coming back to the first check, there are EIPs which might come along and allow bypassing in the future. [EIP-3074](https://eips.ethereum.org/EIPS/eip-3074) is one I’ve co-authored, but there are others as well.

---

I sincerely believe that the long term goal for Ethereum is to migrate all users to Smart Contract Wallets. As a reviewer, I don’t think we should be standardizing anything that relies on EOAs at this point. As an EIP editor, I can’t stop you if that’s what you want to do!

---

**highlander** (2022-04-06):

I agree that by itself this is not fully secure, but in combination it works. And yes, I agree that the current approach with `msg.sender == tx.origin` will be obviated with EIPs such as 3074, and other approaches will have to come along such as modifications to 3074 that ensure that royalties cannot be circumvented.

As an ecosystem, we need to ask ourselves if we want to exclude a whole class of assets that are royalty bearing to be excluded from onchain usage because we allow mechanisms that allow circumvention of legal requirements imposed not by nation statest but by the asset originators. That defeats the purpose of decentraliztion IMHO. If I tell you, you are not allowed to do certain things with my asset you should not be able to do that. To remove tooling that helps programatically enforce those constraints is not a smart move IMHO. I have no issue with smart contract wallets, they are just not useful for this type of assets, or any type of assets that generate residuals based on asset trading.

Also, forcing users into one class of wallets is not a good idea. Give people choice. They will utilize the wallet type they prefer. Who are we to restrict choice unless there are overriding security concerns which I do not see but I might be missing something.

Having said that I would be happy to adjust the language in the standard to abstract it more to remove calling out not having to be a contract specifically. Looking forward to your siggestions.

---

**SamWilsn** (2022-04-07):

> modifications to 3074 that ensure that royalties cannot be circumvented

This is well outside the scope of your EIP, so please feel free to entirely ignore this question, but how would you modify 3074 (or similar) to ensure royalties cannot be circumvented?

> As an ecosystem, we need to ask ourselves if we want to exclude a whole class of assets that are royalty bearing to be excluded from onchain usage because we allow mechanisms that allow circumvention of legal requirements imposed not by nation statest but by the asset originators. […] If I tell you, you are not allowed to do certain things with my asset you should not be able to do that.

While I fully agree with you in principal, there are certain realities we must accept. I do not believe there is a technically sound way to enforce collecting a percentage of a sale price and transferring that to the creator. There are just too many ways to get around it.

There is no magic oracle which can give the true price of a particular NFT. As far as I am aware, there is no way to prevent a dishonest buyer and dishonest seller from colluding and transferring the “real” value in a backchannel, while submitting a much lower price to the NFT contract.

Again, I’m only going from an *extremely* short read of the contracts, but it looks like the only protection against the above collusion is that if an NFT is listed for below its true market value, a bot might come along and snatch the token before the dishonest buyer is able to get their transaction included. Is there another protection I’m missing?

> Also, forcing users into one class of wallets is not a good idea. Give people choice. They will utilize the wallet type they prefer. Who are we to restrict choice unless there are overriding security concerns which I do not see but I might be missing something.

I think I can flip this back on your proposal ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=12) Forcing users to use EOAs to be able to use these NFTs is not a good idea.

> Having said that I would be happy to adjust the language in the standard to abstract it more to remove calling out not having to be a contract specifically

As a potential user of these, if I accidentally bought a token coded to this standard, with all the caveats it brings, I’d be pretty upset. That said, as an EIP editor, the concerns I’ve raised in this discussion thread are unrelated to whether the EIP will be merged.

---

**highlander** (2022-04-08):

BTW, thank you for the great discussion!

As to 3074 … I did not look deep into it, but since it is new opcodes, it means a state-change for an EOA that is captured somewhere probably within the delegated to contract. So the easiest way is to request to whitelist the contract from the CREATOR and then check if an address that e.g. is to receive a token has a whitelisted delegate. Something like that.

If you look at the spec it says in the requirements “… not a contract or a whitelisted contract”.

---

Price collusion is called out in the spec as an attack vector that cannot be really circumvented, even though the creator in the constructor could set a pricefloor per allowed token type to ensure that there is a minimal price for all NFTs in that family (contract). I would be happy to add a mentioning as an option in the spec. We have been discussing to add a pricefloor as an additional feature in the reference implementation.

The spec as written right now ensures that everyone who has royalty subaccount tied to a royalty account tied to an NFT will receive royalties from the sale of that NFT and the sale of its descendants if they exist The reference implementation enforces that.

---

The spec does not force EOAs, the reference implementation does for simplicity’s sake. The spec as I said before just requires the relevant addresses to be either an EOA or a whitelisted account.

---

How would you accidentally buy an NFT compliant to the standard if you do not want to? … there are several things you need to do to purchase an NFT compliant to the spec in both a direct sale or an exchange sale that is different from an ERC721.

This NFT standard is certainly not for everyone. It is designed for entities that want to easily comply with licensing and contract law when dealing with NFTs which in the long run will be the vast majority IMHO.

I think that a healthy standards competition in the NFT space is a good thing because right now it requires a lot of intermediaries to be legally compliant. This standard tries to reduce that dependency on intermediaries.

---

**MaxFlowO2** (2022-04-09):

Ok I’ll bite…

You are overriding _transfer()?

You’ll have to, to enforce the non-override… then devil’s advocate… when swapping from wallet A/B how will this be paid for a 0 “ETH” transaction

Thanks,

-Max

---

**highlander** (2022-04-14):

Sorry. On vacation atm. Hence, the delayed reply.

Thank you for your thoughtful question.

[R29] requires the list price of the NFT to be larger than 0 to avoid that precise situation. In addition, and to avoid super small transactions, the creator of the art, and thus controller of the tree of derived / related art may specify minimal pricing.

---

**MaxFlowO2** (2022-04-15):

So no multi-sigs… interesting… you might want to implement this not on the erc 721 its self, and make a marketplace that does this…

Because this screams marketplace and not NFT.

Also, how is the contract going to get a price on say opensea?

---

**highlander** (2022-04-19):

again, apologies for the late reply – just got back from being OOO all of last week.

The intent of the spec is to allow an NFT to become its own Dapp (meta mask and web3js integration for example) and run on a decentralized infrastructure such as IPFS → we are in fact going to build that. To give the appropriate choice, the standard supports direct sales (sales without a marketplace) and indirect sales (sales through a marketplace).

The price, in either case, is set by the seller and the smart contract is aware of that listing and price through the listNFT function as defined in the spec.

For direct sales, the listing price is THE sales price. For marketplace-mediated transactions, the listing price becomes the price floor.

How the seller arrives at the listing price is beyond the scope of the spec and the reference implementation.

Hope this answers your questions. Keep them coming. This is the type of discussion that makes things better! So thank you!

---

**priti_22** (2022-04-21):

How would these work for [content creators](https://fanstan.co) when their launch their nfts and their fans trade for it?

---

**highlander** (2022-04-21):

Straight forward usage. The content creator determines the shape of the tree for the art (max number of children per NFT etc.), creates the original NFT, and then creates the children/prints of the OG art, and sells those children/prints. If a fan buys a print, they can make more prints, keep the print they bought and sell the prints to other fans. So fans can become art distributors and everyone holding an NFT that has children can earn royalties. The content creator will earn a royalty for every sold NFT and the fans earn royalties for those NFT that were created and sold the NFT they own. Check out the visuals in the spec.

Let me know if that helps.

---

**Ivshti** (2022-05-02):

> The spec does not force EOAs, the reference implementation does for simplicity’s sake. The spec as I said before just requires the relevant addresses to be either an EOA or a whitelisted account.

Realistically, such reference implementations in EIPs are quite influential - unfortunately, for better or worse, implementing an EIP often relies on copy-pasting code from a reference implementation or from a big library such as OpenZeppelin. So under no circumstances should they promote exclusion of a whole class of wallets, including Gnosis Safe, Argent, Ambire, Sequence and others, which collectively secure billions of assets.

> Also, forcing users into one class of wallets is not a good idea. Give people choice. They will utilize the wallet type they prefer. Who are we to restrict choice unless there are overriding security concerns which I do not see but I might be missing something.

Exactly. Promoting exclusion of non-EOA wallets *is* restricting choice.

> I have no issue with smart contract wallets, they are just not useful for this type of assets, or any type of assets that generate residuals based on asset trading.

Interesting take. Smart wallets implement novel security schemes and numerous UX improvements - the simplest example of this would be the Gnosis Safe, or the de-facto standard of multisigs. You’re practically saying a multisig is not useful for valuable assets, which is in fact quite opposite of the truth.

Regarding whitelisting, it’s impractical with SC wallets because each user has a separate address - you’re gonna whitelist each potential buyer/holder? It’s gas intensive to say the least.

Finally, as [@SamWilsn](/u/samwilsn) says, there are many ways to get around this. This is basically a game of whack-a-mole, and the more restrictions there are to enforce this, the more we break composability. Even if we set smart wallets aside for a bit, checks like `tx.origin == msg.sender` disallow contracts from sending NFTs, which limits creative usecases like certain types of decentralized marketplaces, escrow contracts, games and others - essentially crippling the beauty of on-chain composability.

---

**highlander** (2022-05-02):

Thank you for your thoughtful comments.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> The spec does not force EOAs, the reference implementation does for simplicity’s sake. The spec as I said before just requires the relevant addresses to be either an EOA or a whitelisted account.

Realistically, such reference implementations in EIPs are quite influential - unfortunately, for better or worse, implementing an EIP often relies on copy-pasting code from a reference implementation or from a big library such as OpenZeppelin. So under no circumstances should they promote exclusion of a whole class of wallets, including Gnosis Safe, Argent, Ambire, Sequence and others, which collectively secure billions of assets.

We can add a whitelisting function. And add subsequent checks where necessary in the reference implementation. That is not a problem.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> Also, forcing users into one class of wallets is not a good idea. Give people choice. They will utilize the wallet type they prefer. Who are we to restrict choice unless there are overriding security concerns which I do not see but I might be missing something.

Exactly. Promoting exclusion of non-EOA wallets *is* restricting choice.

I do not see how this promotes the exclusion of non-EOA wallets for all assets. But reasonable people can disagree.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> I have no issue with smart contract wallets, they are just not useful for this type of assets, or any type of assets that generate residuals based on asset trading.

Interesting take. Smart wallets implement novel security schemes and numerous UX improvements - the simplest example of this would be the Gnosis Safe, or the de-facto standard of multisigs. You’re practically saying a multisig is not useful for valuable assets, which is in fact quite opposite of the truth.

That is not what I am saying at all. I never said that non-EOA wallets are not suited for all assets, just that they are challenging, and a-prioi less suited for, assets that pay residuals such as royalties based on sales activity, because you can trade the asset with a non-EOA wallet without making the smart contract aware of the trade which would allow the circumvention of e.g. paying royalties to recipients that are legally due to them. That is a scenario that must be avoided from a business PoV, not from a technical PoV, of course. Therefore, people wanting to ensure that they are paid the monies they are due will choose an implementation that will make circumvention as difficult as possible.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> Regarding whitelisting, it’s impractical with SC wallets because each user has a separate address - you’re gonna whitelist each potential buyer/holder? It’s gas intensive to say the least.

Depending on the business arrangement, one could whitelist the SC wallet address, or if it is a trusted exchange, the exchange contract address, because the standard and implementation do support exchange-based trades just not in the current format from e.g. OpenSea.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> Finally, as @SamWilsn says, there are many ways to get around this. This is basically a game of whack-a-mole, and the more restrictions there are to enforce this, the more we break composability. Even if we set smart wallets aside for a bit, checks like tx.origin == msg.sender disallow contracts from sending NFTs, which limits creative usecases like certain types of decentralized marketplaces, escrow contracts, games and others - essentially crippling the beauty of on-chain composability.

The current reference implementation might, but the spec does not. First off, from a business point of view, certain use cases that allow royalty circumvention should not be allowed. Second, there are ways to e.g. escrow a 4910, also 4910s are apriori not suited for games, however, a game suitable NFTs e.g. an ERC721 might be owned or derived from a 4910 NFT through a collection utilizing e.g. an ERC998 approach. So there are creative ways to do what you want to achieve. They just must be done differently from how they are currently done.

One of the 4910s goals is to offer maximum protection to legal royalty recipients. That means that there will always be trade-offs between business needs and innovation/technical needs. A standard is not always suitable for all use cases, and that is ok because it tries to achieve a specific goal … e.g. DIDComm is great for DID-based communication but if you want to use X.509s it is less useful.

---

**AKAdwalou** (2022-12-21):

Hello and thank you everybody for the explanations above.

I am looking for such operating principle like linked or nested NFT with parent/children features and royalties possibilities.

I have seen other EIP like EIP-6150, EIP-6059 but this one seems to be the closest to final status.

Since this one is in review status, do you know how much time it can be reviewed before it will be released and have the final status ?

Thanks in advance.

---

**highlander** (2023-02-28):

[@AKAdwalou](/u/akadwalou) I am hoping soon. I need to follow up with the editors. I think all comments have been answered. I will let you know. Apologies for the very late response. If you want to look at a reference implementation of  4910, you can find it [here](https://github.com/treetrunkio/treetrunk-nft-reference-implementation)


*(4 more replies not shown)*

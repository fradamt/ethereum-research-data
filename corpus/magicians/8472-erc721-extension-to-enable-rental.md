---
source: magicians
topic_id: 8472
title: ERC721 extension to enable rental
author: ArthurBraud
date: "2022-03-02"
category: EIPs
tags: [nft, erc-721]
url: https://ethereum-magicians.org/t/erc721-extension-to-enable-rental/8472
views: 3105
likes: 6
posts_count: 9
---

# ERC721 extension to enable rental

## Summary

At Comity Labs, we’re exploring infrastructure that would better enable coordination for digital communities.  The recent surge of digital assets, and the emergence of socioeconomic models such as gaming guilds and scholarships in Axie Infinity, in Axie scholarships owners lend their Axies to scholars and lower the barrier to play the game/enter the eco system, validates that similar to traditional asset classes, there is utility in sharing digital assets *(and it’s safe to assume the utility will only increase with time.)*

Existing implementations of rentals or sharing that we’ve come across use ad hoc agreements and off-chain techniques. For example, Axie Infinity enables scholarships by allowing for game sign-in with username/password credentialing associated with a wallet, meaning an owner can allow a counterparty to play with their assets without giving them full control of the wallet. Other games allow asset holders to specify delegates who are allowed to play with the assets. While these may serve users well in the short-run, their centralized nature threatens users’ true ownership of the asset—do you really own the asset if a developer can give the privileges associated with that asset to another party without your permission? Furthermore, such a design limits the ability to share assets outside of the application’s ecosystem. It also potentially burdens developers with subjective arbitration and dispute resolution where counterparties disagree, which should be avoidable with well defined smart contracts. We believe that  “native rental support” in ERC721 will accelerate and promote decentralized and composable approaches.

There have been a few exciting and relevant proposals, e.g. from [devinaconley](https://ethereum-magicians.org/t/erc-standard-for-held-non-fungible-token-nfts-defi/7117) and [Daniel-K-Ivanov](https://ethereum-magicians.org/t/erc-4400-erc-721-consumer-extension/7371). The key difference in our proposal, as we see it, is that it would not require trust between owner and renter/consumer.

## Proposal

We propose a new ERC721 extension interface to handle temporary ownership transfer, backward compatibility, and great flexibility to support any rental agreement design. The key point is to delegate the rental logic (price, duration…) to a separate contract to allow for maximum flexibility, and enforce the agreement and rental terms in the blockchain. Other proposals have created an interface to allow rental, but they are based on trust, and nothing enforces that the owner nor the renter respects agreed-upon rental terms.

More specifically, we introduce two interfaces:

- IERC721Rental, which inherits from IERC721, acts as a rental agreement manager: it activates and removes rental agreements, and handles the transfer of ownership during the rental. The proposed version modifies the ownerOf return result when the rental is in progress but does not grant the renter more rights on the token.
- IERC721RentalAgreement, the interface for the rental agreement. The logic and terms of the rental will be entirely defined, delegated, and enforced to the contract implementing this interface. For example, it will define the rental fees and the rental duration. It also defines how the rental agreement interacts with the IERC721. In particular, it guarantees that the rental agreements are honored after it has been started.

The two proposed interfaces can be found here: [IERC721Rental.sol](https://github.com/comitylabs/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/IERC721Rental.sol). We have a proposal ERC721 contract with rental implemented [here](https://github.com/comitylabs/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol).

**Rental agreements**

We implemented three examples for standard rental agreements. We are interested in learning about use cases and seeing how we can extend these.

- ERC721SingleRentalAgreement.sol: rent a specific token Id from a specific ERC721 contract for pre-defined fees and duration.
- ERC721BundleRentalAgreement.sol: a contract that enables to start rental agreement for any token Id of any contract. In case of early termination, a cancellation fee has to be paid and the renter gets reimbursed for the time they didn’t consume the token.
- ERC721SwapRentalAgreement.sol: two token owners can swap their tokens for a period of time.

**IERC721Rental <> IERC721RentalAgreement interactions**

Below is a diagram that illustrates how the IERC721Rental and IERC721RentalAgreement interact. For more details and context about the interfaces, please refer to the code.

[![Screen Shot 2022-01-10 at 2.07.08 PM](https://ethereum-magicians.org/uploads/default/optimized/2X/f/f034aa426689e99d2300e331e5755f366d1ceb51_2_690x407.png)Screen Shot 2022-01-10 at 2.07.08 PM2624×1550 371 KB](https://ethereum-magicians.org/uploads/default/f034aa426689e99d2300e331e5755f366d1ceb51)

## Tradeoffs made

The proposed interface is not perfect, but we believe it enables the most flexibility and compatibility. The first point of contention is changing the value of the `ownerOf` function. While in theory this offers backward compatibility by not requiring changes to smart contracts that interact with the ERC721s, it may create surprises. Note that contracts aware of our rental interface could still know if a token is rented by using the `rentedOwnerOf` function.

The second point is that while delegating the rental logic to a separate contract allows for maximum flexibility, a poorly designed or malicious rental agreement contract could lock a token in the rental state permanently. Special care has to be taken by the token owner to avoid using such contracts.

## Further considerations

We would really value your feedback.

**ERC721 upgradeability framework**

We intend to provide a framework to migrate existing ERC721 tokens to the new interface. For security concerns, we plan to allow both upgradeability and downgrade ability options so DAPP and DAO developers can introduce the new rental feature safely.

**Cross-chain support**

We think that a rental framework should eventually support cross-chain rentals (Alice owns a token in Ethereum and rents to Bob in Polygon), but we haven’t spent too much time thinking about it yet. There have been already very interesting proposals to bridge NFTs such as [cross-rollup-nft-wrapper-and-migration-ideas](https://ethresear.ch/t/cross-rollup-nft-wrapper-and-migration-ideas/10507)

[@peroket](/u/peroket) and [@ArthurBraud](/u/arthurbraud) on behalf of Comity Labs

## Replies

**tommyshieh** (2022-03-07):

Hello! Thanks for sharing. I am really interested in this as I am also building rental related smart contract. This is nice. I am curious, which solution do you use to trigger contract at the expected time?

---

**peroket** (2022-03-07):

Our solution relies on an agreement contract. The owner of the NFT sets the agreement, and from then on you can start the rental by accepting the agreement.

So if nothing special is done, the rental starts when someone calls the function to accept the agreement.

If you wanted to start at a specific time, then you could put the logic in the agreement to refuse starting the rental unless it is that specific time. For example with a simple condition on the block timestamp. But it still requires an external call to start the rental, which you can do manually or set a script or any way you can imagine. There is no restriction on who can call that function, unless you choose to restrict it in the agreement contract.

Does that answer your question [@tommyshieh](/u/tommyshieh) ?

---

**tommyshieh** (2022-03-08):

thanks for your answer. How about ending the rental? Does it also require manually calling the smart contract to end the rental?

---

**peroket** (2022-03-08):

Yes exactly. For this one as well, no specific constraints on who can call the stop function is implemented in the token contract, but the agreement can add constraints if it so wishes.

---

**Daniel-K-Ivanov** (2022-03-19):

Hello [@ArthurBraud](/u/arthurbraud)

I am happy to see that more and more people are working on NFT rentals. There are different approaches, f.e my proposal ([EIP-4400: ERC-721 Consumable Extension](https://eips.ethereum.org/EIPS/eip-4400)) focuses on adding a role that can enable renting protocols, you have focused on defining the renting logic as part of the standard.

I am curious to know why you are going for the approach for enforcing the “renting as part of the NFT standard” compared to “enabling NFT renting through a role that has the permission to utilise the NFT”.  To be honest, I think that the first adds a bigger burden in terms of implementation as it is more complex and the gains are questionable compared to the latter.

Your concerns are that the “enabling NFT renting through a role that has the permission to utilise the NFT” approach requires the `owner` of the NFT to respect the agreement. I don’t really think that there is a problem with that since the `owner` of the NFT will not be the user that want to rent it out to someone but the `owner` will be the Renting Protocols that implement the logic for renting.

It worries me that in your proposal, you are changing the `definition` of `owner`. The renter becomes the official ERC721 `owner` during his rent period, however, he is an `owner` that is not allowed to transfer the NFT, grant approvals etc and all of the infrastructure that is built already around the fact that `owners` DO have that permission will be surprised to see that the `owner` has those permissions, **but not always**. If the `owner` is actually a `renter` he will not have those permissions. This will be too ambiguous IMO.

The third thing that comes to mind is the fact that once a rent period is over, you have to do an on-chain TX to “update the state”. Have you thought about `expiries` or allowing someone to have a specific role, but only for a certain period of time? Example → [EIP4907: ERC-721 User And Expires Extension](https://ethereum-magicians.org/t/eip4907-erc-721-user-and-expires-extension/8572)

Happy to hear your thoughts!

---

**peroket** (2022-03-21):

Hello [@Daniel-K-Ivanov](/u/daniel-k-ivanov) thanks for your reply, you ask good questions.

To answer your first question, we are believers of putting more in the blockchain, to get all the advantages that it provides (security, decentralisation…). For sure you can implement a renting protocol outside of the blockchain that can make use of a renting interface, but this protocol would be most likely centralised, a black box that you would need to trust. And nothing enforces it, so you would also need to trust the owner to respect that external protocol and not use the contract directly themselves. Our solution puts the agreement in a public place, so that both renter and owner have visibility of it, and most importantly enforces it in the blockchain itself, so you don’t need trust to start an agreement. It protects both renter and owner against malevolent actors. It does add some complexity to the implementation of the contract, but it moves it away from an external renting protocol, adding more security at the same time, so we believe it is worth it. And note also that our solution is compatible with your approach, nothing prevents you to put an empty agreement contract and implement an external renting protocol if you so wishes.

You mention that the owner of a token to rent would be the renting protocol itself. But you, as an owner of a potentially very expensive token, are you going to transfer that token to an external party to rent it? Then again you need trust. And you also loose any proof that you are the actual owner of the token. Our solution does not have those issues, you can rent your token but still prove that you are the owner.

We understand your concerns about modifying the definition of `owner`. We have the same concerns. We chose this approach to be as compatible as possible with the current ecosystem, but we are totally open to combine our agreement interface with your consumable interface for example. That’s exactly the kind of feedback we hoped to get, to see if anyone would have concerns with that.

Finally, yes that’s true. Your interface has the same concern, did you consider the `expiries` as well? We tried to stay as simple as possible with our interface, so that it remains as flexible as possible and does not lock out any potential user, preferring to put all the complexity in the agreement contract. The main drawback I see to that is an increase in gas cost to query the `owner`, but it doesn’t seem to me that we would loose any functionality by adding that one, so it could be done. I guess it’s mostly a question of when do you want to pay for that (a bit everytime you use it, or only one time at the end).

Does that answer your questions?

---

**ArthurBraud** (2022-03-24):

Hey [@Daniel-K-Ivanov](/u/daniel-k-ivanov) ,

Thanks for your feedback, I share your concerns that this current proposal is too limited to the rental use case and that it will benefit from having a more customizable role definition.

I saw you were discussing interesting ideas with [@ilanolkies](/u/ilanolkies) in [ERC-4400: ERC-721 Consumer Extension](https://ethereum-magicians.org/t/erc-4400-erc-721-consumer-extension/7371) about how to define roles more generically.

I tried to come up with a new design that intends to merge the 2 ideas:

- Allow arbitrary roles to be granted
- Delegating the role permission management to another contract IERC721RolesManager so that roles terms and agreements can be honored on-chain.

Here is the PR that also has an example about we would implement define the *Renter* role:



      [github.com/smlxl/openzeppelin-contracts](https://github.com/smlxl/openzeppelin-contracts/pull/17)














####


      `master` ← `roles`




          opened 08:13PM - 21 Mar 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/f/f8698f1723854c7c8453d2f45fe134e27215c03d.jpeg)
            ArthurBraud](https://github.com/ArthurBraud)



          [+367
            -0](https://github.com/smlxl/openzeppelin-contracts/pull/17/files)







Introducing 2 new interfaces `IERC721Roles` and `IERC721RolesManager` inspired f[…](https://github.com/smlxl/openzeppelin-contracts/pull/17)rom the feedbacks from [ERC-4400: ERC-721 Consumer Extension](https://ethereum-magicians.org/t/erc-4400-erc-721-consumer-extension/7371) and [ERC721 extension to enable rental](https://ethereum-magicians.org/t/erc721-extension-to-enable-rental/8472).
This aims to provide a general framework to define token roles with on-chain guarantees that roles attribution terms are fulfilled.

**IERC721Roles**
- Enables to define ERC721 user roles by tokenId. We expect standard nomenclatures for roles to be defined such as `bytes4(keccak256("ERC721Roles::Renter"))`.
- Applications will call `roleGranted` to check whether a user has been granted a specific role.
- The role attribution logic is delegated to an `IERC721RolesManager` contract, that is set at the tokenId level. Note that we could have implementations where the role manager contract is defined at the ERC721 contract level to guarantee that roles definitions are consistent across each token.
- Token's`owner` is never changed and can be updated independently from the roles

**IERC721RolesManager**
-  This contract holds the logic and terms to acquire and revoke roles.
-  It guarantees that roles are honored on-chain, by using callback `afterRoleRevoked` and `afterRoleGranted` when someone tries to update a role.
- The IERC721RolesManager is set at the tokenId level in this example, but we could have one unique role manager contract for all tokens as mentioned above.
- When someone tries to update the IERC721RolesManager contract, a callback is made to `IERC721RolesManager.afterRolesManagerRemoved` so that the manager can revert if a role agreement is ongoing.

Examples:
See `ERC721Roles` and `ERC721RolesRentalAgreement` for examples of implementation.
The later is a simple contract to allow NFT rental by granting Renter role

**IERC721Roles & IERC721RolesManager interactions**
<img width="1018" alt="Screen Shot 2022-03-24 at 2 07 34 PM" src="https://user-images.githubusercontent.com/24436667/159982043-71e4a454-23c0-4b26-8e41-884f5fa5bcc3.png">












Happy to collaborate on this idea ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

---

**eartho-group** (2022-03-26):

take a look on our suggestion,



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/eartho-group/48/5712_2.png)

      [ERC-4902 Decentralized Autonomous Access (DAA)](https://ethereum-magicians.org/t/erc-4902-decentralized-autonomous-access-daa/8700)




> eip: 4902
> title: Decentralized Autonomous Access (DAA)
> description: DAAs represent access to digital or physical things, with the ability to connect with entities seeking to use them
> author: D Daniel eartho.offical@gmail.com
> discussions-to: https://github.com/ethereum/eips/issues/4902
> status: Draft
> type: Standards Track
> category: ERC
> created: 2022-03-22
> requires: 20
>
> Abstract
> As humans, we are constantly seeking as much access to resources as possible, We also make access trades for o…

While ERC-721(NFT) created for “NFTs represent ownership over digital or physical assets.”,

ERC-DAA created for “DAAs represent an access over digital or physical things & resources, with the ability to connect with entities that seeking to use it”

it covers the rental topic within it


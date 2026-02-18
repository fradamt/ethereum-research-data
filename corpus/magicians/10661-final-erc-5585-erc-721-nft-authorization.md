---
source: magicians
topic_id: 10661
title: "(Final) ERC-5585: ERC-721 NFT Authorization"
author: VeegaLabsOfficial
date: "2022-09-04"
category: ERCs
tags: [nft, token, metaverse, gamefi, copyright]
url: https://ethereum-magicians.org/t/final-erc-5585-erc-721-nft-authorization/10661
views: 6238
likes: 20
posts_count: 32
---

# (Final) ERC-5585: ERC-721 NFT Authorization

## Abstract

This EIP([EIP-5585](https://github.com/ethereum/ercs/blob/master/ERCS/erc-5585.md)) separates the ERC-721 NFT’s commercial usage rights from it’s ownership to allow for the independent management of those rights.

## Motivation

Most NFTs have a simplified ownership verification mechanism, with a sole owner of an NFT. Under this model, other rights, such as display, or creating derivative works or distribution, are not possible to grant, limiting the value and commercialization of NFTs. Therefore, the separation of an NFT’s ownership and user rights can enhance its commercial value.

Commercial right is a broad concept based on the copyright, including the rights of copy, display, distribution, renting, commercial use, modify, reproduce and sublicense etc.  With the development of the Metaverse, NFTs are becoming more diverse, with new use cases such as digital collections, virtual real estate, music, art, social media, and digital asset of all kinds. The copyright and authorization based on NFTs are becoming a potential business form.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY” and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

### Contract Interface

```solidity
interface IERC5585 {

    struct UserRecord {
        address user;
        string[] rights;
        uint256 expires
    }

    /// @notice Get all available rights of this NFT project
    /// @return All the rights that can be authorized to the user
    function getRights() external view returns(string[]);

    /// @notice NFT holder authorizes all the rights of the NFT to a user for a specified period of time
    /// @dev The zero address indicates there is no user
    /// @param tokenId The NFT which is authorized
    /// @param user The user to whom the NFT is authorized
    /// @param duration The period of time the authorization lasts
    function authorizeUser(uint256 tokenId, address user, uint duration) external;

    /// @notice NFT holder authorizes specific rights to a user for a specified period of time
    /// @dev The zero address indicates there is no user. It will throw exception when the rights are not defined by this NFT project
    /// @param tokenId The NFT which is authorized
    /// @param user The user to whom the NFT is authorized
    /// @param rights Rights autorised to the user, such as renting, distribution or display etc
    /// @param duration The period of time the authorization lasts
    function authorizeUser(uint256 tokenId, address user, string[] rights, uint duration) external;

    /// @notice The user of the NFT transfers his rights to the new user
    /// @dev The zero address indicates there is no user
    /// @param tokenId The rights of this NFT is transferred to the new user
    /// @param newUser The new user
    function transferUserRights(uint256 tokenId, address newUser) external;

    /// @notice NFT holder extends the duration of authorization
    /// @dev The zero address indicates there is no user. It will throw exception when the rights are not defined by this NFT project
    /// @param tokenId The NFT which has been authorized
    /// @param user The user to whom the NFT has been authorized
    /// @param duration The new duration of the authorization
    function extendDuration(uint256 tokenId, address user, uint duration) external;

    /// @notice NFT holder updates the rights of authorization
    /// @dev The zero address indicates there is no user
    /// @param tokenId The NFT which has been authorized
    /// @param user The user to whom the NFT has been authorized
    /// @param rights New rights autorised to the user
    function updateUserRights(uint256 tokenId, address user, string[] rights) external;

    /// @notice Get the authorization expired time of the specified NFT and user
    /// @dev The zero address indicates there is no user
    /// @param tokenId The NFT to get the user expires for
    /// @param user The user who has been authorized
    /// @return The authorization expired time
    function getExpires(uint256 tokenId, address user) external view returns(uint);

    /// @notice Get the rights of the specified NFT and user
    /// @dev The zero address indicates there is no user
    /// @param tokenId The NFT to get the rights
    /// @param user The user who has been authorized
    /// @return The rights has been authorized
    function getUserRights(uint256 tokenId, address user) external view returns(string[]);

    /// @notice The contract owner can update the number of users that can be authorized per NFT
    /// @param userLimit The number of users set by operators only
    function updateUserLimit(unit256 userLimit) external onlyOwner;

    /// @notice resetAllowed flag can be updated by contract owner to control whether the authorization can be revoked or not
    /// @param resetAllowed It is the boolean flag
    function updateResetAllowed(bool resetAllowed) external onlyOwner;

    /// @notice Check if the token is available for authorization
    /// @dev Throws if tokenId is not a valid NFT
    /// @param tokenId The NFT to be checked the availability
    /// @return true or false whether the NFT is available for authorization or not
    function checkAuthorizationAvailability(uint256 tokenId) public view returns(bool);

    /// @notice Clear authorization of a specified user
    /// @dev The zero address indicates there is no user. The function  works when resetAllowed is true and it will throw exception when false
    /// @param tokenId The NFT on which the authorization based
    /// @param user The user whose authorization will be cleared
    function resetUser(uint256 tokenId, address user) external;

    /// @notice Emitted when the user of a NFT is changed or the authorization expires time is updated
    /// param tokenId The NFT on which the authorization based
    /// param indexed user The user to whom the NFT authorized
    /// @param rights Rights autorised to the user
    /// param expires The expires time of the authorization
    event authorizeUser(uint256 indexed tokenId, address indexed user, string[] rights, uint expires);

    /// @notice Emitted when the number of users that can be authorized per NFT is updated
    /// @param userLimit The number of users set by operators only
    event updateUserLimit(unit256 userLimit);
}
```

The `getRights()` function MAY be implemented as pure and view.

The `authorizeUser(uint256 tokenId, address user, uint duration)` function MAY be implemented as `public` or `external`.

The `authorizeUser(uint256 tokenId, address user, string[] rights; uint duration)` function MAY be implemented as `public` or `external`.

The `transferUserRights(uint256 tokenId, address newUser)` function MAY be implemented as `public` or `external`.

The `extendDuration(uint256 tokenId, address user, uint duration)` function MAY be implemented as `public` or `external`.

The `updateUserRights(uint256 tokenId, address user, string[] rights)` function MAY be implemented as `public` or `external`.

The `getExpires(uint256 tokenId, address user)` function MAY be implemented as `pure` or `view`.

The `getUserRights(uint256 tokenId, address user)` function MAY be implemented as pure and view.

The `updateUserLimit(unit256 userLimit)` function MAY be implemented as`public` or `external`.

The `updateResetAllowed(bool resetAllowed)` function MAY be implemented as `public` or `external`.

The `checkAuthorizationAvailability(uint256 tokenId)` function MAY be implemented as `pure` or `view`.

The `resetUser(uint256 tokenId, address user)` function MAY be implemented as `public` or `external`.

The `authorizeUser` event MUST be emitted when the user of a NFT is changed or the authorization expires time is updated.

The `updateUserLimit` event MUST be emitted when the number of users that can be authorized per NFT is updated.

## Rationale

First of all, NFT contract owner can set the maximum number of authorized users to each NFT and whether the NFT owner can cancel the authorization at any time to protect the interests of the parties involved.

Secondly, there is a resetAllowed flag to control the rights between the NFT owner and the users for the contract owner. If the flag is set to true, then the NFT owner can disable usage rights of all authorized users at any time.

Thirdly, the rights within the user record struct is used to store what rights has been authorized to a user by the NFT owner, in other words, the NFT owner can authorize a user with specific rights and update it when necessary.

Finally, this design can be seamlessly integrated with third parties. It is an extension of ERC-721, therefore it can be easily integrated into a new NFT project. Other projects can directly interact with these interfaces and functions to implement their own types of transactions. For example, an announcement platform could use this EIP to allow all NFT owners to make authorization or deauthorization at any time.

## Backwards Compatibility

This standard is compatible with ERC-721 since it is an extension of it.

## Security Considerations

When the resetAllowed flag is false, which means the authorization can not be revoked by NFT owner during the period of authorization, users of the EIP need to make sure the authorization fee can be fairly assigned if the NFT was sold to a new holder.

Here is a solution for taking reference: the authorization fee paid by the users can be held in an escrow contract for a period of time depending on the duration of the authorization. For example, if the authorization duration is 12 months and the fee in total is 10 ETH, then if the NFT is transferred after 3 months, then only 2.5 ETH would be sent and the remaining 7.5 ETH would be refunded.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**travelnotes** (2022-09-09):

It will be great if  some blue-chip NFTs could support this function, then the holders can utilize this feature to maximize the value of their NFTs without selling them.

---

**tigerspace** (2022-09-09):

This proposal is meaningful.It will allow every holder to become an amplifier of the NFT brand，and that will allow the NFT to make a new paradigm exploration in commercialization.

---

**apan826** (2022-09-14):

Hopefully this extension could inspire a proliferation of authorized projects and contribute to the NFT world with more fair and creativity.

---

**VeegaLabsOfficial** (2022-10-27):

We introduce the “rights” attribute in the UserRecord struct， which is used to store what rights has been authorized to a user by the NFT owner, in other words, the NFT owner can authorize a user with specific rights and update it when necessary.

---

**yus** (2022-10-28):

This protocol is useful, it maximizes the benefits to the NFT owner and makes the NFT project more popular.

---

**yus** (2022-10-28):

I have a question about the new attribute “rights”, and how to define and use it？

---

**JamesW** (2022-10-28):

Hey guys, I’m interested in this, if we want to make this protocol work in offline application scenarios as well, how do we solve the problem of inconsistent information between online and offline

---

**VeegaLabsOfficial** (2022-10-30):

Hi, [@JamesW](/u/jamesw), thanks for your question. So basically, the smart contact will assign an authorization to the address of authorized user. The user can verify his rights in both online and offline. But if someone misuses a NFT, we have to rely on the law offline.

---

**VeegaLabsOfficial** (2022-10-30):

Hi, [@yus](/u/yus) Thanks for your question. Currently, the rights are defined and used by NFT contract owner and it will be more supplemented with the development of this protocol. Since the regulation of copyright is vary in different countries, we are referring a set of NFT licenses created by a16z to make an implementation and hopefully figuring out a standard in the future, it is also very welcomed that if you have some good ideas.

---

**CHANCE** (2022-11-01):

I love seeing this type of discussion growing in the ecosystem. I have several questions, though.

As it stands, this EIP does not provide legally binding separation of the ownership classes and is, at most, a measure of signaling that only adds cost overhead.

Today, one can already achieve highly granular on-chain usage permissions with the help of something like [Delegatable ETH](https://github.com/delegatable/delegatable-eth).

Typically, an EIP does not provide use-case nuances, and implementation details as an EIP define an interface, not the following implementation.

With the large amount of opinion that has been included with things such as `duration` and `rights[],` this EIP will be unusable on anything that isn’t an L2 the second any individual wants to write more than a sentence into the array. The chain is not a database and storing strings as if it is, is incredibly bad practice and reflective that this EIP is far from adoptable.

This continues with functions such as `updateUserLimit,` `updateResetAllowed,` `resetUser` are not vital to the functioning of the EIP and, again, are an implementation detail that should not be standardized (especially given the lack of detail put into a clearly defined interface) This is again reaffirmed by the lack of events defined and only functions.

- For such a complex situation, a standard must be better defined than 5585. Is there a reason that the traditional way of building an EIP has been forgone in preference of the proposal here today?
- What about the needs from 5585, make one incapable of using a far more powerful and better-defined standard to achieve the same results such as EIP-4337
- A legally binding contract is defined (generally) by the existence of an offer, consideration, and acceptance (while maintaining competency). That cannot be done on the blockchain, especially not with this EIP. Is the aim of this EIP to enable signaling rather than an agreement that is legally binding?

---

**bet3lgeuse** (2022-11-02):

> A legally binding contract is defined (generally) by the existence of an offer, consideration, and acceptance (while maintaining competency). That cannot be done on the blockchain, especially not with this EIP. Is the aim of this EIP to enable signaling rather than an agreement that is legally binding?

Agree that this EIP is pretty short on modeling a legally binding contract. But it’s not necessarily true that it couldn’t be done. I believe the UK (including commonwealth territories such as the BVI, where a lot of projects are registered) and the State of New York both have cleared on-chain records as legal contracts. There are a number of companies in Singapore that make the assumption that on-chain contracts are valid, assuming they cover the legal properties for defining a contract as you’ve stated.

There is a considerable number of abandoned projects that have attempted to implement Ricardian contracts and the list of prior literature is somewhat long.

https://iang.org/papers/intersection_ricardian_smart.html

For the OP, if you haven’t already, spending some time to read up on Monax and check out Hyperledger Burrow, it would be time well spent. Burrow is EVM compatible framework for implementing legal contracts. I’m still not quite sure why more EIPs haven’t borrowed from the ideas there, but copyright might be a good place to start.

---

**VeegaLabsOfficial** (2022-11-06):

Hi, [@CHANCE](/u/chance) , very appreciate for your suggestions, here are our ideas for discussion.

First of all, 5585 is an application layer protocol rather than a pure technical protocol. Our starting point for this protocol are: (1) What problems need to be solved in the next stage of the development of the NFT market? (2) What factors influence the promotion of commercialization and applications? And these are also the problems we are facing in our projects now.

A conclusion from our extensive communication with NFT enthusiasts, operators, commercial customers and lawyers in the copyright field in North America and Asia is that it is necessary to be able to use NFTs more simply, conveniently, openly and transparently, and at the same time, to be able to clarify and protect the rights of users. The current standard is designed and considered based on these recommendations and optimized to the greatest extent possible.

Secondly, there are many excellent NFTs in the market now, such as BAYC, Azuki, Doodle, etc. These NFT projects have authorized some of the rights of NFT to the owners, and binds relevant rights based on the ownership on-chain. Recently a16z has also launched a series of on-chain NFT license agreements to provide a set of standardized NFT rights, and these are the basis for us to make the rights of NFT owners and users more transparent. We believe that with the development of the industry, a set of standards for NFT rights will be formed, which can play a greater value to the market. Now we are cooperating with some global lawyer teams and commercial companies to promote the development in this area. We can provide NFT operators with the ability to choose rights and specifications that are more suitable for them. And we also welcome growing numbers of people to participate and contribute together. We believe it will facilitate the future development of the NFT industry.

BAYC Terms & Conditions: [BAYC](https://boredapeyachtclub.com/#/terms)

Thirdly, regarding the standard of application, how to encourage NFT operators willing to participate but with the lowest cost, we provide some interfaces for them to manage rights. At the beginning, we suggest that the easiest way of using rights is just set it to ALL, which means all the rights of owner will be authorized to users. With the wider adoption of the a16z protocol and the specification of industry development, rights will have a set of standards, which can support NFT owners to manage their rights more flexibly to maximize benefits.

a16z’s copyright agreement : [The Can’t Be Evil NFT Licenses - a16z crypto](https://a16zcrypto.com/introducing-nft-licenses/)

Finally, regarding your ideas and technical suggestions, we have considered during our EIP design, some of them are absolutely correct and helpful, we are just trying to find a balance between technology and business, because the commercialization of NFT needs a whole picture to be implemented. So 5585 is still under continuous improvement. We hope that more experts in the field of technology, law, business and NFT enthusiasts can participate, so as to promote the development and extention of 5585 to support the NFT market. We believe it will play a broader role in the combination of on-chain and off-chain, on-chain games and Metaverse. At the same time, it can be compatible with the copyright related laws of various countries to better protect the rights of users.

---

**travelnotes** (2022-11-07):

I agree that the rights of copyright law are easy to standardized and implemented with smart contract, it is a good entry point to practice “CODE IS LAW”.

---

**travelnotes** (2022-11-08):

5585 should provide a getRightsOfferings interface to the user, who can query the rights available for the NFT specified and apply for authorization.

---

**apan826** (2022-11-09):

We are doing some projects which are on-chain contracts and it was also mentioned in the Web3 officail announcement in HK just a couple of days before. Although it cannot be 100% implementated, seems it is growing, that is good. By the way, why [@bet3lgeuse](/u/bet3lgeuse) you suggest to use Burrow?

---

**VeegaLabsOfficial** (2022-11-30):

It sounds good, thanks. We will introduce an interface for the user to query the available rights.

---

**travelnotes** (2022-12-01):

It’s great, so the user could call this function to get the available rights.

Recently, the owners of the CryptoPunks finally received a new license granting them commercial IP rights and they can authorize them to other users, it seems 5585 could help them manage their rights.

---

**ngveega** (2022-12-04):

Thank you so much for sharing us with this valuable information. I highlight the ***rights*** that were granted to the NFT owner.

Liscense of Cryptopunks:

Subject to your acceptance of, and compliance with, these Terms, uponlawfully acquiring Your CryptoPunk NFT and, for so long as you hold Your CryptoPunk NFT (both dates as recorded by the CryptoPunks Smart Contract) (the “License Term”),Yuga Labs grants to you an exclusive, universe-wide, royalty-free, sublicensable license to **reproduce, distribute, prepare derivative works based upon, publicly display, publicly perform, transmit, and otherwise use and exploit**, Your CryptoPunk Art (“License”). TheLicense is intended to be broad, enabling you to make both commercial and non-commercial uses of Your CryptoPunk Art, in any and all media, whether exis2ng now orinvented later, subject only to the restric2ons set forth below.

---

**apan826** (2022-12-05):

It seems some guys wonder the reason of getting all rights. So the rights are initialized by the NFT project owner (contract owner as well) and it contains all the rights that owners will have for each NFT, it is just like a whole set that can be retrieved by everyone.

---

**Grant** (2022-12-14):

I am just wandering why the user needs to know the rights of NFT owners? Is it for the user to know what rights the owner can authorize to him? But if the owner does not have such a right, he cannot make it anyway, is that correct?


*(11 more replies not shown)*

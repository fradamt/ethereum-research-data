---
source: magicians
topic_id: 4167
title: "ERC-2569: Saving and Displaying Image Onchain for Universal Tokens"
author: whtyfhas
date: "2020-03-27"
category: EIPs
tags: [erc-2569]
url: https://ethereum-magicians.org/t/erc-2569-saving-and-displaying-image-onchain-for-universal-tokens/4167
views: 5422
likes: 2
posts_count: 18
---

# ERC-2569: Saving and Displaying Image Onchain for Universal Tokens

**The readme file:**  https://github.com/ethereum/EIPs/pull/2569/commits/3a0759c85750d9490b2b78ed1181d59f10323d7e

**The reference implementation for ERC-1646 may be found in:**  https://github.com/ethereum/EIPs/pull/2569/commits/3a0759c85750d9490b2b78ed1181d59f10323d7e

**It’s an ongoing protocol.**

## Simple Summary

A set of interfaces to save an SVG image in Ethereum, and to retrieve the image file from Ethereum for universal tokens.

## Abstract

This set of interfaces allow a smart contract to save an SVG image in Ethereum and to retrieve an SVG image from Ethereum for fungible tokens, non-fungible tokens and tokens based on standards that will be developed in the future.

The interface set has two interfaces: one to save an SVG file in Ethereum and the other to retrieve an SVG file from Ethereum.

Typical applications include but not limited to:

A solution for storage of a fungible token’s icon.

A solution for storage of a non-fungible token’s icon.

A solution for storage of the icon/logo of a DAO’s reputation token.

## Motivation

The ERC-721 token standard is a popular standard to define a non-fungible token in Ethereum. This standard is widely used to specify a cryto gift, crypto medal, crypto collectible etc. The most famous use case is the [cryptokitty].

In most of these applications an image is attached to an ERC-721 token. For example, in the cryptokitty case each kitty has a unique image. While the token’s code is saved in Ethereum permenantly, the image attached to the token is not.

The existing solutions still keep such an image in a centralized server instead of Ethereum. When these applications display an image for a token they retrieve the token’s information from Ethereum and seach the centralized server for the token’s associated image by using the token’s information.

Although this is an applicable way to display an image for a token, the image is still vulnerable to risks of being damaged or lost when saved in a centralized server.

Hence we propose a set of interfaces to save an image for a universal token in Ethereum to keep the image permenant and tamper-resistant, and to retrieve an image for a universal token from Ethereum.

## Definitions

`tokenId`: for a non-fungible token such as an ERC-721 token or a multi-token such as an ERC-1155 token which has a member “ID” to specify its token type or token index our proposed interface assigns an SVG image’s file content to a string variable of the token’s contract and  associates the SVG image to this “ID” number. This unique ID is used to access its SVG image in both a “set” operation and a “get” operation.

For a fungible token such as an ERC-20 token no such an ID is needed and our proposed interface just assigns an SVG image’s file content to a string variable of the token’s contract.

This is an ongoing project. We really need and welcome any help.

## Replies

**zhous** (2020-03-28):

It’s a simple but very important solution for Ethereum’s tokens.

---

**mcdee** (2020-03-28):

Any benefits to this over using an ENS text record?

---

**whtyfhas** (2020-03-28):

Thank you for your question. I am not sure if I understand your question correctly.

Could you please elaborate your question?

My understanding about ENS is that it maps an address to a .eth domain name. Did you mean whether or not this solution helps ENS in mapping an address to a domain name? Or you meant something else?

---

**mcdee** (2020-03-28):

You could obtain an ENS domain for your token, *e.g.* `mytoken.eth`

You could then create text records against that domain with some predefined format, *e.g.* `token-image-<tokenid>`, that contains the SVG.

The advantage of ENS is that it is already supported by many wallets and libraries, so lookups for the SVG information would be easy to carry out with existing code.

---

**whtyfhas** (2020-03-29):

This is really interesting.

Each token is issued by a smart contract at a unique ETH address. We can use an ENS domain name to refer to this address/this token.  And we can define an SVG image for a token in one of the following ways:

- For a fungible token such as an ERC-20 token we may define an SVG of a token by using some format like svg.mytoken.eth  ;
- For a non-fungile token such as an ERC-721 token we may define an SVG of a token by using some format like svg.tokenid.mytoken.eth

This is my understanding. I am not sure if this is something similar to what you think.

---

**mcdee** (2020-03-29):

You could create subdomains but that would take a fair amount of gas compared to just creating text records in the `mytoken.eth` domain.  Same result, but text records would be quicker and cheaper to work with.

As an example:

```auto
$ ethereal --network=goerli ens text set --domain=mytoken.eth  --wait --passphrase=secret --key='image' --text='

'
0xcb064f0cd58751b2755dec7ad804c7b87ef2ea5b54279feeec1889397ed0f193 mined
$ ethereal --network=goerli ens text get --domain=mytoken.eth --key='image'

```

This is using the key `image`; for NFTs you could use `image-<tokenid>`

---

**zhous** (2020-03-29):

Looks marvelous! But ENS is also deployed by Smart Contract, so we also must pay for the retrieval of a domain’s text records. Am I right?

---

**zhous** (2020-03-29):

Here’s some questions. Short ENS domains are very expensive. You couldn’t registry any duplicated domains, while we can issure any duplicated token (and with a decentralized registration, we can ‘link’ any token with a DAO).

---

**mcdee** (2020-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zhous/48/1298_2.png) zhous:

> Looks marvelous! But ENS is also deployed by Smart Contract, so we also must pay for the retrieval of a domain’s text records. Am I right?

Retrieval of data from Ethereum is free unless you’re using it in a transaction (which you aren’t).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zhous/48/1298_2.png) zhous:

> Short ENS domains are very expensive.

3-character ones are, everything else is pretty cheap.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zhous/48/1298_2.png) zhous:

> You couldn’t registry any duplicated domains, while we can issure any duplicated token (and with a decentralized registration, we can ‘link’ any token with a DAO).

Why would you want duplicate names for different tokens?  How would an outside user know which one was which?

The general point I was making is that the proposal was for simple storage of text records, and we already have a system to do that with a lot of support across wallets, many client libraries, *etc.*

---

**zhous** (2020-04-04):

I think ENS is totally centralized. And text records is also based on a centralized management model. If the image of a token can be changed any time by any reason or even no reason, is it a solution for an application of blockchain? I couldn’t find the connection between ERC 2569 and ENS.

---

**pm.riviere** (2020-05-04):

I don’t think [@mcdee](/u/mcdee)’s proposal is equivalent to this ERC. The ENS solution requires to store the image into a third party ERC-721 that has limited lifespan and features as per ENS standards.

This ERC could come in handy for some projects requiring more flexibility and unlimited persistence.

---

**zhous** (2020-05-30):

Exactly! Moreover, I think image onchain is matter of time, so why not make a solution in Ethereum?

---

**MicahZoltu** (2020-07-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mcdee/48/272_2.png) mcdee:

> The general point I was making is that the proposal was for simple storage of text records, and we already have a system to do that with a lot of support across wallets, many client libraries, etc.

I don’t think ENS is quite the right fit here.  For a decentralized token, you likely want to set the image once at token deployment time and it would never change.  With ENS you will need a mechanism to ensure that regular payments are made to ENS to maintain the record, or you would need to pay for an arbitrary number of years in advance.  All in all, I think ENS isn’t a great fit because there is no real need to update, and if there is a need to update it can be built into the contract and integrated directly with the token’s management code rather than having to use an external system and pay for it.

What *would* be nice is if ENS provided a *free* option for reverse lookup TXT records, but that is something for the ENS team to think about.  ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**imsys** (2021-12-08):

I’m somewhat new to blockchain coding, but I have noticed a few things:

- Solana has a big token naming centralization issue: token names have to be pushed to a github repo: GitHub - solana-labs/token-list: The community maintained Solana token registry
- I’ve seen projects bridging to many chains, and for each chain it had to send the logo for github repos or other centralized service, and also having to share the socials links for each chain service (etherscan, bscscan, polyscan, etc etc)

I see that the NFTs adopted the tokenURI(tokenId) method to get the metadata and image, so I was thinking, maybe use something like:

contractImageURI or contractLogoURI: preferably use ipfs or arweave

contractMetadata: maybe a struct that would contain something like:

```auto
struct Metadata {
    array founders;
    struct Socials {
        string website;
        string discord;
        string reddit;
        string telegram;
    }
    struct Chains { //for bridged tokens
        address Ethereum;
        address Polygon;
        address BSC;
        address Avalanche;
        address Harmony;
        string Solana;
    }
}
```

Maybe the image URI should be contained together with the Metadata struct?

And by the way, Etherscan has a thing called Public Name Tag, that makes it very helpful when looking at transactions log. I wish they could get a contract Public Name Tag from the contract public name string, instead of we having to create private tags or using ENS…

---

**imsys** (2021-12-08):

It could also be a json string if it would make it easier for future edits, to include/remove items.

---

**imsys** (2022-01-08):

My position is that SVG is a vector image format, there are other formats available too, and in the future other image formats may become more common, as I mentioned in the previous posts.

Uniswap is doing an interesting thing in their V3 ERC721 tokens. When you call tokenURI(), it respond as:

```auto
return
    string(
        abi.encodePacked(
            'data:application/json;base64,',
            Base64.encode(
                bytes(
                    abi.encodePacked(
                        '{"name":"',
                        name,
                        '", "description":"',
                        descriptionPartOne,
                        descriptionPartTwo,
                        '", "image": "',
                        'data:image/svg+xml;base64,',
                        image,
                        '"}'
                    )
                )
            )
        )
    );
```

source: [github](https://github.com/Uniswap/v3-periphery/blob/c3f7f249e10413c1f01bd22ec9ddfac70fe0025e/contracts/libraries/NFTDescriptor.sol#L65), [etherscan](https://etherscan.io/address/0x91ae842a5ffd8d12023116943e72a606179294f3#code#F9#L64)

Example, browser already can understand the following if pasted in the url: (Ethereum Logo)

(but this forum markdown interpreter doesn’t allow me to hyperlink it, haha)

data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUzNSIgaGVpZ2h0PSIyNTAwIiB2aWV3Qm94PSIwIDAgMjU2IDQxNyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJ4TWlkWU1pZCI+PHBhdGggZmlsbD0iIzM0MzQzNCIgZD0iTTEyNy45NjEgMGwtMi43OTUgOS41djI3NS42NjhsMi43OTUgMi43OSAxMjcuOTYyLTc1LjYzOHoiLz48cGF0aCBmaWxsPSIjOEM4QzhDIiBkPSJNMTI3Ljk2MiAwTDAgMjEyLjMybDEyNy45NjIgNzUuNjM5VjE1NC4xNTh6Ii8+PHBhdGggZmlsbD0iIzNDM0MzQiIgZD0iTTEyNy45NjEgMzEyLjE4N2wtMS41NzUgMS45MnY5OC4xOTlsMS41NzUgNC42TDI1NiAyMzYuNTg3eiIvPjxwYXRoIGZpbGw9IiM4QzhDOEMiIGQ9Ik0xMjcuOTYyIDQxNi45MDV2LTEwNC43MkwwIDIzNi41ODV6Ii8+PHBhdGggZmlsbD0iIzE0MTQxNCIgZD0iTTEyNy45NjEgMjg3Ljk1OGwxMjcuOTYtNzUuNjM3LTEyNy45Ni01OC4xNjJ6Ii8+PHBhdGggZmlsbD0iIzM5MzkzOSIgZD0iTTAgMjEyLjMybDEyNy45NiA3NS42Mzh2LTEzMy44eiIvPjwvc3ZnPg==

So, I think we could just allow URLs, and if they want to save the entire image in the blockchain, they can just base64encode it.

There are a few points and concerns to be said:

- XSS attack - SVGs allows the use of javascript. So someone could add a malicious code in it. It could be prevented by just using  tags, here is an example of when javascript inside SVG is ran or not: https://csplite.com/csp/test376/
- URI pointing to a very big image just to troll, maybe to microsoft hosted windows.iso or ubuntu.iso, people would just be wasting bandwidth. For solutions, maybe we would have to add a javascript code to verify the file extension, or for a gigabyte jpeg, it could be done as mentioned in this stackoverflow post.

---

**zhous** (2022-11-15):

I’m sorry but this is not a core ERC of my project([DAism.io](http://DAism.io)). And also it could be extended to some other formats but my team doesn’t have enough time to do this. I think next year we’ll come back to this ERC.

Please pay your attention to this: ERC-2569 is actually an ERC to fight against URL or TokenURI. Saving any pictures or videos or music offchain is not acceptable for a dApp! Well, if you’re coding a web app, forget what I said.


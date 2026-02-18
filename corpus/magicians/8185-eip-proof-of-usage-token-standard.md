---
source: magicians
topic_id: 8185
title: "EIP: \"proof of usage\" token standard"
author: looneytune
date: "2022-02-02"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-proof-of-usage-token-standard/8185
views: 512
likes: 0
posts_count: 1
---

# EIP: "proof of usage" token standard

This topic follows a previous discussion that took place here: [Decentralizing power in media industry, do we have the technology?](https://ethereum-magicians.org/t/decentralizing-power-in-media-industry-do-we-have-the-technology/8099)

NFTs are shaping a deep change in the digital world, not only in the media/art industry but ideas on how to use this new technology are popping up everywhere (recently I’m seeing creators selling nfts to give holders some privileges in their community etc). ERC-721 tokens are perfect to give proof of ownership on a given token and this specific trait led to a significant revolution in the media industry, especially in the figurative art (in all its meanings and forms): this is the only form of art which can fully take advantage of NFT.

Let me be more precise about this: visual artists can be the owner of their art, they can sell it and earn income on the future sells. Like a painting in the real world, the value of a NFT is locked in the piece of art itself and can be owned by someone.

The sustainability of the life of a visual artist can now count on a decentralized infrastructure, not subject to censorship and above all without the need for third parties as intermediaries.

I think this is going to change the world for the better, it’s not a matter of bored apes and crypto punks, it’s more about a (potential) profound change in how art is tied with centralized forms of power and interests. This may sound silly or not-so-relevant to some of you but some people’s lives out there experienced a tangible positive change and I’m sure that making a contribution to improve the lives of others is why we’re all here.

There are other forms of expression like music and writings whose value is not related to the property and even if we’re seeing people around the world minting .wav NFTs it doesn’t seem to work so much.

We’re seeing some attempts at tokenizing royalties (consider royalties as “revenues” if you’re not familiar with art industry dictionary) and even if after all it’s a positive change, it seems more of a financial model than a structured system aiming for freedom of expression.

Tokenized royalties will always depend on a centralized entity for counting and distributing the token, it could be a smart contract but I have some doubts that multinational giants would surrender to a revolution like this so easily. I think it’s more likely they will adopt blockchain technologies remaining centralized and influent.

I also think that all this could change technology-side with a new token standard.

I’m thinking about a token with the following features:

- it can be minted from an “origin” contract.
- Users can mint a copy of the information the contract stores (our token) and they can hold it in their wallet, this process is made by paying GAS + % to the contract’s owner if written in the contract.
- the copy represents substantially a file plus it brings a status with it, default status is 0.
- the token can be “engaged”
- when you “engage” the token its status changes to 1. Engaging the token simply means that you open the file associated with it and you access to the informations contained. While the file is engaged the status keeps staying 1, once the file is closed the status turns back to 0. If you do not interact with the file after a given amount of time the status automatically resets to 0 just to avoid fake statistics.
- the “origin” contract holds the informations for the numbers of copies minted and their status through each block.
- everybody can access to the informations about how many copies have been minted and how many times each token has been engaged.
- after each block the contract takes a given amount of ETH (decided in the “origin” contract) from every address whose token’s status was 1 in that given block.
- every user should always know how much ETH does the contract asks for each engaged token in a given block before minting the token.

I’m sure that this new token standard could lead to so many application I’m not even thinking at the moment, we could see this standard as a “proof of usage” token.

I know this idea is not flawless and I’m not sure that Ethereum network can handle this huge amount of data if this is going to be a thing.

This is why I opened this thread, I’d be happy to share ideas and concepts and critiques.

The contribution I can give as a coder is irrelevant compared to the ability of some coders in this forum (please forgive me if I wrote inaccurate informations) so feel free to take the initiative on a technical level ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

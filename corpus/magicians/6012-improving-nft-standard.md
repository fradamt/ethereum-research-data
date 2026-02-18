---
source: magicians
topic_id: 6012
title: Improving NFT standard
author: anett
date: "2021-04-16"
category: Magicians > Primordial Soup
tags: [erc, nft, token]
url: https://ethereum-magicians.org/t/improving-nft-standard/6012
views: 6482
likes: 62
posts_count: 30
---

# Improving NFT standard

Hey there,

I would love to organise a group together to improve the ERC-721 and ERC-1155 standard as both of those are wildly used in the NFT space but they seem to be a bit outdated. I would love to collect feedback, ideas and hopefully find and likeminded people who would love to work on this standard.

What I find missing in both ERC721 and ERC1155 standards:

- lacking security against rug pulling
- no attached hash to the image/multimedia file itself as a proof
- missing downloadable standard which I define as more of a nice to have feature

Those are just my points that I noticed can be improved in the current standards.

Feel free to contribute to this discussion, add feedback or any ideas that you can think of.

Edit: There’s a working group for this issue, to keep up with WG visit the [NFT Standards wiki](https://nft-standards.gitbook.io/nft-standards-wiki/)

## Replies

**kladkogex** (2021-04-16):

We at SKALE are happy to participate

---

**jpitts** (2021-04-17):

With the wild adoption of NFTs and so many new users entering the community this is definitely needed! It seems like a bundle of several ERCs (some old and some new), plus a campaign promoting it widely to devs and end-users could address what is missing here.

Here are some relevant ERCs to study:

**[ERC-2477 - Token Metadata Integrity](https://eips.ethereum.org/EIPS/eip-2477)**

> This specification defines a mechanism by which clients may verify that a fetched token metadata document has been delivered without unexpected manipulation.
>
>
> This is the Web3 counterpart of the W3C Subresource Integrity (SRI) specification.

**[ERC-1046 - ERC20 Metadata Extension](https://eips.ethereum.org/EIPS/eip-1046)**

> Optionally extend ERC20 token interface to support the same metadata standard as ERC721 tokens.

Also, there is a lot of [early work on asset metadata standards](https://medium.com/blockchain-manchester/evolving-erc-721-metadata-standards-44646c2eb332), e.g. the JSON file describing the assets of the NFT.

---

**banyan** (2021-04-18):

Check out EIP-2981 re: interesting proposals on improving royalty implementation

---

**wuzzi23** (2021-04-19):

I think the idea of adding a hash on-chain is a good one - that way a consumer can download the NFT and store it offline (and still proof which one is the legit copy) or replicate it in multiple places and doesn’t have to worry about ransomware deleting/encrypting the online NFT stored by a single central provider.

I wrote a bit about this on my blog also: https://embracethered.com/blog/posts/2021/broken-nft-standards/

---

**abcoathup** (2021-04-19):

In addition to making the per token metadata decentralized, some nice to haves:

- Token contract metadata, name, image
- License for metadata, so users know what rights they have (or don’t have) to the artwork
- Secondary sales support, a percentage and address for marketplaces to use (though not enforceable)

---

**nginnever** (2021-04-20):

I’ve written a 721 extension for creators to:

1: sign their nfts providing a secondary link between the nft and the object it represents beyond metadata. e.g. an artist can retain their key and post signatures over time that link back to the original signature on an owned nft, and owners can easily display and verify the nft is signed, much like an artist would sign a limited edition print.

2: verifiably introduce a total amount of nfts ever created (similar to total supply in 1155 but without the potential erc20 confusion).

Feedback very welcome! Thanks!



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nginnever/48/4143_2.png)
    [EIP-3340: NFT Editions Standard Extension](https://ethereum-magicians.org/t/eip-3340-nft-editions-standard-extension/6044) [EIPs](/c/eips/5)



> This is a simple extension with the intent of improving provenance in ERC-721 tokens representing works of digital art.
> As NFTs evolve further into representing digital art, there is a need to strengthen the link between a token and the digital work itself. With the current standard, a symbolic URI is the only information present linking the art to the blockchain. The URIs may become lost over time and the link may be lost. Hashing the digital art is a good link but pre-images may be lost. This…

---

**anett** (2021-04-22):

Thank you [@kladkogex](/u/kladkogex) & SKALE Team for showing interest in helping out & everyone who chimed in for contributions with ideas to new standard development process.

**The goal is to create a standard that can be used by NFT platforms and will have all the features that will be usable from the user perspective not just look good from the dev perspective.**

Update from my side to see the progress on this issue:

- I’m Creating knowledge graph around all NFT Standards ERCs including meta EIPs to collect all the knowledge that is out there including standards that are running on the Ethereum (chain). This will be used as knowledge base for this group to move forward on developing new standard without duplicating other standard.
- I definitely want to include @abcoathup ideas as they seems to be great and usable in the new standard also helpful.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> Token contract metadata, name, image
> License for metadata, so users know what rights they have (or don’t have) to the artwork
> Secondary sales support, a percentage and address for marketplaces to use (though not enforceable)

- I had chat with @jpitts about creating Meta NFT instead of Meta EIPs as there are many EIPs so why not to create something more funky.

What I would love to see from this group:

- Ideas if you can think of how to better organise EIP group.
- Drop lines on how people would like to contribute to this standard
- Participation

My next steps:

- Spin off NFT Improvement working group
- Talk to NFT platforms devs to see what should be improved in the new NFT standard and collect feedback if platforms are willing to use new standard.
- Publish NFT Standards knowledge graph

---

**anett** (2021-05-03):

The NFT Standard Working Group has kicked off ![:partying_face:](https://ethereum-magicians.org/images/emoji/twitter/partying_face.png?v=9)

- NFT Standards wiki is live and available at Welcome page - Obsidian Publish
- Sum up and simplified explanation of the main NFT Standards is live on Medium

I would love to chat with people on what are the ideas on how the NFT Standard should be improved.

Please check out the [NFT Standards Wiki](https://publish.obsidian.md/nft-graph/Welcome+page), join the group, leave comment on this thread.

Stay Magical ![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=9)

---

**Shan** (2021-05-04):

This is awesome; congrats! It would be great to develop cross-chain NFT standards to include Tezos and other blockchains. Is this within the scope of your project?

---

**anett** (2021-05-05):

Thank you [@Shan](/u/shan) ,

My plan is to create standard on Ethereum which can be plugged to Polkadot network via [Moonbeam](https://moonbeam.network/).

I to start simple so I’m trying to focus on improving the security functions in the ERC721. I would love to chat with people that are skilled in token security so I will get better (and bigger) picture on how to improve token security. [GitHub - Defi-Cartel/salmonella: Wrecking sandwich traders for fun and profit](https://github.com/Defi-Cartel/salmonella) is a great example of exploit on ERC20 contract. Unfortunately I don’t have much of a knowledge on the token security side and would love to chat with experts in this case.

I have many ideas on what can be improved on the NFT Standard itself. Suggestions for the new Standard are live in wiki  [New standard - suggestions - Obsidian Publish](https://publish.obsidian.md/nft-graph/New+standard+-+suggestions)

The main problem I came into is the lack will to communicate from the NFT platforms side, if they are open to collaborate on new standard, if they are willing to implement the new standard…

Many platforms have their own custom implementation build on ERC721 standard that they are using instead of proposing their custom changes as a new standard.

---

**fulldecent** (2021-05-06):

I have many notes on compatible and backwards-incompatible changes that could be made to ERC-721.

But I have never published them because I’m not sure it’s the right thing for the Ethereum community yet.

One major data point is to look at MetaMask, it took over a year to implement ERC-721 in their application and I’m not sure even ERC-1155 (which is very relevant) is implemented.

So if we fragment NFTs further it may be a disservice to the community.

On the other hand, if we’re making a new NFT on Binance or Tron or whatever, AND they have resources to create a user experience (i.e. not just “please use MetaMask and add a chain”) then yes, I would love to work on that and design it better from the start. People at Binance and TRON don’t return my calls, and I guess they are not interested in this.

---

**anett** (2021-05-07):

One thing is to go please people to implement a new standard, another thing is finding a vulnerability that would affect many people and projects.

That’s why I see a huge potential in improving the security component and create implementation for it.

There are many aspects that are missing in the NFT Standards (talking about the ones that are live - ERC721,ERC1155), but the reason why ERC721 is successful is the simplicity of this standard.

Unfortunately simplicity doesn’t means security, especially as the Ethereum is breaking ATH lately, the security of the space and the standards is becoming MUST feature.

There are so many docs dating to 2018, when the Cryptokitties b00m was strong, but the chain has evolved significantly since 2018. The chain went over numerous Hard Forks since then…

I would love to think outside of NFT as Art use cases, after the Uniswap rolled out V3 and liquidity NFTs there will be golden pot waiting for another exploit to happen sooner or later.

---

**fulldecent** (2021-05-07):

# Regarding use cases

ERC-721 and NFTs were designed, and are primarily used (in quantity of tokens and value of transactions), for healthcare, retail, in-game purchases and enterprise use cases. *I am excluding one specific NFT token sale in this analysis until evidence can be provided it was not a shill sale.*

Rest assured that our NFT standards are designed to be relevant until at least 2028 in terms of use cases.

# Regarding security

Your proposal begin the discussion on security with “security - but I’m not exaclty [sic] sure how the non fungibles can have added security”.

This is not actionable advice.

# Standards, yay

My experience is that many people want to create applications without hiring developers, and publish standards without making applications. This is wholly backwards.

For example, this thread starts with the motivation that ERC-721 is “lacking security”. I consider this fake news given the above reference in the details.

Going forward, I recommend this could be addressed another way.

The concern “I find missing in both ERC721 and ERC1155 standards”… “no attached hash to the image / multimedia file itself as a proof” is better addressed by going to the Stack Exchange and asking “How do I attach the hash of a multimedia file to a ERC-721 or ERC-1155 token?”

The concern “missing downloadable standard which I define as more of a nice to have feature” is better addressed by creating a concrete token product, creating a good user experience, dealing with the practical considerations of building a thing (typically involving spending money and hiring people) and then making it work. Then after you have solved the problem, come back to the community and show off how well it worked, possibly as a standard.

---

**jpitts** (2021-05-08):

# NFT Use Types

If it has not yet been discussed, I would add a special need here: some metadata identifying the NFT’s general purpose. This enables users to know if a particular NFT is art, a Uniswap liquidity position, a deed to a home, etc. enabling UX on another generalized NFT exchange to warn what the NFT actually is for.

A list of all of these use-types of NFTs could be maintained, with terminology defined, and even warnings created for certain standard contexts (buy, sell, burn).

See this [Tweet](https://twitter.com/Juan_Snow1/status/1391114572623319041) by JuanSnow

> Someone created a @Uniswap V3 LP position worth $127,000 and sold the NFT representing that liquidity on @rariblecom for 1ETH
>
>
> Liquidity deposit: https://etherscan.io/tx/0x4237241cf…
>
>
> Sale on Opensea (easier to see): https://opensea.io/assets/0xc3644…
>
>
> Liquidity withdrawn: https://etherscan.io/tx/0x5e819d73c…

---

**whamsicore** (2021-05-11):

I feel like image hash is a bit narrow since NFTs could represent a changing image as well, such as a game character whose appearance may change according to its equipment.

---

**anett** (2021-05-17):

[@fulldecent](/u/fulldecent) thank you for comments. You are totally right, NFTs have wide range of usage. There are many ways how to look at the ERC721 as standard itself and we can meditate on this standard for so long as we can come up with a tons of arguments why this standard is good and why not (pros / cons).

I made this thread in order to gain more attention to NFT Standards when I began my research down the NFT Standards rabbit hole. I’m not Solidity dev so I need to gain more knowledge before committing to creating new standard and proposal.

Things are now more developed than they were 10d ago and I’m sharing updates.

I talked to a bunch of people from the NFT industry and figured out that adding Permits as on-chain messages would make the biggest sense how to increase security. I’m sure that over time we can find more extensions that can be added to the standard and solve issues.

I’m working on proposal which will be extension to both ERC721 and ERC1155 as both have ApprovalForAll function. My proposal is to add Permits as security extension to the standards that are already live. Permits will be used as off chain message signatures that will approve (confirm) purchase of the NFT. Author of the NFT will sign message with his wallet which will trigger sale function. This standard will look similar to ERC712 (EIP2612) but it will be usable for non fungible token standards. This security extension can be used not only in art world of NFTs but it can find usage in other not-only-art industries.

Proposal which will be shared to ethereum/eips GitHub repo as ERC when proposal will be ready which may be soon.

Edit: Proposal may change, the research is ongoing. To keep up with WG visit [nftstandards.wtf](https://www.nftstandards.wtf/NFT+Standards+Wiki+-+READ.me) wiki

---

**nginnever** (2021-05-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anett/48/3020_2.png) anett:

> My proposal is to add Permits as security extension to the standards that are already live.

I would think more often than not, extensions may decrease the security of the base protocol. Any addition to the standard introduces complexity. Any additional complexity might increase the attack surface.

Sometimes extensions are created specifically to address security concerns and do minimize the attacks possible. The easiest example of this was the safeMath code that prevented over/underflow before 0.8.0.

Sometimes extensions improve security dependent on the use case, an example of this would be contract introspection.

In particular meta transactions are a great feature, but in this case I think they create a new set of security challenges that you must be aware of (domain separation, replay prevention, typed data, separation from standard Ethereum messages etc).

Putting security first while adding extensions is of course a great idea if this is what you mean by “security extension”.

---

**Shymaa-Arafat** (2021-05-25):

Hi everybody,

Sorry, I didn’t read any of the written (just first 3-4 lines), but I thought this is important for u to discuss without waiting for me (apologies if someone already mentioned it

.

Although this is a comic show, but if he really made a new NFT for the same small pic then how did that happen?I think there’s something wrong here

(yes one of the small ones, but clearly who ever paid 69m$ considered himself holding the whole collection even if enlarged or under focus)

https://t.co/Vfh9E108SG?amp=1

.

If the buyer of the artwork doesn’t care, a museum making a consolidated NFT for all it’s pieces( I think this what the big pic with small ones inside it mean, right?) will indeed care if a their managed to steal a piece and sold it with a new NFT.

.

---

**anett** (2021-06-10):

Hey nginnever, we did more research and came out to conclusion to create Permits NFT Standard. Over the time this idea has evolved from Security issue improvement to more of a UX and cheaper minting experience. Permit would improve UX by removing the need to perform an extra transaction, especially in the context of an escrow-less sales where the seller want to keep ownership until the sale is performed.

[@Amxx](/u/amxx) made draft code of a proposal which you can [find here](https://gist.github.com/Amxx/e3c87476093a6b27d9271b2e54b35292).

We would love to hear community input and feedback on this idea.

WG is pretty active on [Telegram, feel free to join and intro yourself](https://t.me/joinchat/rqMTOh0kSO1kMGM0)

Wiki is live at [nftstandards.wtf](https://www.nftstandards.wtf/)

---

**fulldecent** (2021-08-31):

I support the approach shown above at [NFTPermit.sol · GitHub](https://gist.github.com/Amxx/e3c87476093a6b27d9271b2e54b35292)

Minor feedback

- Maybe should be separate ERCs for 721 and 1155 extensions.
- It should be loudly noted that this depends on EIP-712 which is in draft.

Although this is a “good” approach. A “great” approach is to just deploy the same thing as a utility which applies to any existing NFT.


*(9 more replies not shown)*

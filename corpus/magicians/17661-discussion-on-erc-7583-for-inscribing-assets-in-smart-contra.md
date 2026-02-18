---
source: magicians
topic_id: 17661
title: Discussion on ERC-7583 for Inscribing assets in smart contract
author: ins-evm
date: "2023-12-26"
category: ERCs
tags: [inscription]
url: https://ethereum-magicians.org/t/discussion-on-erc-7583-for-inscribing-assets-in-smart-contract/17661
views: 9597
likes: 47
posts_count: 73
---

# Discussion on ERC-7583 for Inscribing assets in smart contract

Hello everyone,

I’m excited to share with the community a proposal I’ve been working on, aimed at introducing a standard for enabling tokens to be traded both as fungible tokens and non-fungible tokens on the Ethereum. This initiative seeks to establish a unified approach to handling inscription assets on the Ethereum blockchain, enhancing consistency and interoperability of inscription assets across different applications and platforms.

https://github.com/ethereum/ERCs/pull/173

**Overview of the Proposal:** This protocol represents the implementation of the BRC20 standard within the EVM. BRC20 enables FTs to be traded in the same manner as NFTs. And **ERC-7583** not only facilitates the trading of FTs akin to NFTs but also allows for the binding of NFTs with FTs. This integration enables FTs within NFTs to participate in existing DeFi protocols, significantly enhancing the liquidity of NFTs.

You can find the detailed proposal here: [ERC-7583 Inscription Standard in Smart Contracts](https://github.com/insevm/ERCs/blob/master/ERCS/erc-7583.md)

I believe this proposal can significantly contribute to the Ethereum ecosystem by providing a standardized way to handle inscription assets, which is currently lacking. It has the potential to open up new possibilities for developers and users alike.

**Seeking Feedback:** I would greatly appreciate any feedback, suggestions, or concerns you may have regarding this proposal. Your input is invaluable in refining and improving this EIP before moving forward.

Looking forward to an engaging and constructive discussion. Thank you for your time and consideration!

## Replies

**HarryLin1024** (2023-12-27):

Why not upgrade directly on the basis of ERC-20?

---

**ins-evm** (2023-12-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/harrylin1024/48/11285_2.png) HarryLin1024:

> Why not upgrade directly on the basis of ERC-20?

Because inscriptions can be applied not just to ERC20 tokens, but they are capable of storing any type of data, including images (thus applicable to ERC721), HTML, and even binary files.

---

**alongdlut** (2023-12-27):

Is there any security concern compared to inscription on Calldata?

---

**ins-evm** (2023-12-27):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/r/f17d59/48.png) rex5999:

> You are a liar and a thief. You stole the idea of ​​token ethv and now you want to deceive everyone here?

If you possess the similar understanding, I am thrilled, as it means we are kindred spirits. Cheer up, brother! This is an excellent platform where you can express your opinions. A market with immense potential awaits your exploration! ![:grinning:](https://ethereum-magicians.org/images/emoji/twitter/grinning.png?v=12)

---

**rex5999** (2023-12-27):

You claim that you are the first inscription published on EVM. What is the truth?

---

**ins-evm** (2023-12-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alongdlut/48/11289_2.png) alongdlut:

> Is there any security concern compared to inscription on Calldata?

We will see `calldata` limited in each block and pruned over time to address storage implications on scalability in the future phase “[The Surge](https://zerocap.com/insights/research-lab/diving-into-the-future-of-ethereum/)”

---

**ins-evm** (2023-12-27):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/r/f17d59/48.png) rex5999:

> You claim that you are the first inscription published on EVM. What is the truth?

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/f/fc5837a8dc7c489d158134ee8eb0220b81f63e3a_2_690x94.png)image2148×294 54.7 KB](https://ethereum-magicians.org/uploads/default/fc5837a8dc7c489d158134ee8eb0220b81f63e3a)

I don’t want to discuss topics here that are not helpful to Ethereum.

---

**SatXt** (2023-12-27):

Hey is there a guide om how to inscribe f on etherscan?

---

**ins-evm** (2023-12-28):

What’s the mean of the “f”?

---

**SatXt** (2023-12-28):

Oh sorry that was typo.

I believe I meant how do we convert the data to inscribe into a hash

---

**ins-evm** (2023-12-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/satxt/48/11303_2.png) SatXt:

> Oh sorry that was typo.
> I believe I meant how do we convert the data to inscribe into a hash

It’s ok!

In various situations, inscribed data needs to be decode for displaying. So we just encode data to bytes and inscribe into smart contract. Sometimes, we also calculate the hash of the data before inscribing it, depending on the specific requirements of your project.

---

**TUTUBIG** (2023-12-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ins-evm/48/11288_2.png) ins-evm:

> excited

I think it would be better to add “from” and “to” addresses in this event, like `event Inscribe(address from,address to, bytes data)`  This will be more convenient to descripe the owner exchange of this inscription.

---

**zzzz** (2023-12-28):

Sir, a good idea is certainly important. Have you considered establishing a community belonging to INSC on DC or TG, so that more like-minded friends can join this discussion? This project is fantastic

---

**FancyKing** (2023-12-28):

By carrying the inscription through events in the EVM and making the inscription compatible with the EVM, will there still be the disadvantage of excessive gas cost? How to solve this?

---

**ins-evm** (2023-12-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tutubig/48/11310_2.png) TUTUBIG:

> ins-evm:
>
>
> excited

I think it would be better to add “from” and “to” addresses in this event, like `event Inscribe(address from,address to, bytes data)`  This will be more convenient to descripe the owner exchange of this inscription.

Indeed, the recording of inscribed transactions is missing. However, I believe that inscription event should be treated as a separate event, distinct from the transfer event.

How about this:

```auto
interface IERC7583 {
  event TransferIns(address indexed from, address indexed to, uint256 indexed id);
  event Inscribe(uint256 indexed id, bytes data);
}
```

Add a field id to inscriptions for enabling the mapping of the two events.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/apechef/48/11333_2.png)

      [Discussion on ERC-7583 for Inscribing assets in smart contract](https://ethereum-magicians.org/t/discussion-on-erc-7583-for-inscribing-data-in-smart-contract/17661/41) [ERCs](/c/ercs/57)




> Here are a few of suggestions for the ERC-7583 proposal.
>
>
>
> Give each Inscribe a unique id
>
>
>
> The contract should set a max size of the inscribed data to avoid blockchain bloat.
>
>
>
> Pragmatically sometimes data will need to be stored off chain, e.g. on IPFS. Introduce a standardized way to handle this.
> Example with MAX_DATA_SIZE and inscribeOffChain.
> interface IERC7583 {
>     event Inscribe(uint256 indexed id, bytes data);
>     event InscribeOffChain(uint256 indexed id, string dataRef);
> }
>
> con…

[@apechef](/u/apechef) Thank you for your input!

1. The unique id has already been memtioned here.
2. And it is a good practical solution for setting a max size of inscribed data! What do you think is the best practice for setting a max limit data size?
3. I think the off chain could also be stored in ‘Inscribe’ event.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/apechef/48/11333_2.png)

      [Discussion on ERC-7583 for Inscribing assets in smart contract](https://ethereum-magicians.org/t/discussion-on-erc-7583-for-inscribing-data-in-smart-contract/17661/42) [ERCs](/c/ercs/57)




> Including the users address (msg.sender) would follow common practice:
> event Inscribe(address indexed user, uint256 id, bytes data);
> Compare with:
> event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
> event Approval(address indexed owner, address indexed spender, uint256 value);

[@apechef](/u/apechef) Currently, inscriptions are operating within smart contracts on the EVM. For important data like the owner, how about using the storage variables of the smart contract to store it? e.g.

```auto
function ownerOf(uint256 insId) external view returns (address owner);
```



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/apechef/48/11333_2.png)

      [Discussion on ERC-7583 for Inscribing assets in smart contract](https://ethereum-magicians.org/t/discussion-on-erc-7583-for-inscribing-data-in-smart-contract/17661/81) [ERCs](/c/ercs/57)




> @TUTUBIG @ins-evm Great discussion and ideas.
>
> Indeed, the recording of inscribed transactions is missing. However, I believe that inscription event should be treated as a separate event, distinct from the transfer event.
>
> I am not convinced about this. Do you view inscriptions as entities/artefacts which should be traded independently of tokens? What are the use cases which could not be covered by the current Transfer event?
>
>
> The unique id has already been memtioned here.
> And it is a good p…

[@apechef](/u/apechef) I am also considering this point at the moment. If ERC7583 is intended to include transaction-related specifications, positioning it as an extension of ERC721 seems like an ideal choice. In this way, ERC7583 can serve as an alternative to ERC721Metadata. However, this approach also brings certain limitations. Treating ERC7583 solely as an extension of ERC721 may restrict its scalability in broader application scenarios, as not all types of inscriptions need to strictly follow the transaction specifications of ERC721. I look forward to your insights on this issue! ![:grinning:](https://ethereum-magicians.org/images/emoji/twitter/grinning.png?v=15)

> if you have other ideas about dynamic hashes or similar to add layers of security?

Currently, most users, when inscribing, tend to use a string of characters as input, such as: `data:,{"p":"brc-20","op":"mint","tick":"ordi","amt":"10"}`. In designing the experimental contract $INSC, to accommodate users’ inscription habits, we provided an entry parameter for users to input their inscription data. However, for this type of simple inscriptive data with rules, it can be entirely generated by the smart contract, and users only need to provide simple parameters, like the quantity to be minted.

In fact, at the content level, we do not need to restrict the hash of the inscription data. As a decentralized application, everyone has the right to inscribe any content. The form of data is only related to the consensus of the community.

**Metadata Schema**

Added Metadata Schema for FT (Fungible Tokens) and NFT (Non-Fungible Tokens) in [Add ERC: Inscription In Smart Contract by shalom-ins · Pull Request #173 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/173/commits/b5be079fe846705bc4eab9ba9cf3334c755ef4a9). looking forward to receiving suggestions ![:grinning:](https://ethereum-magicians.org/images/emoji/twitter/grinning.png?v=15)

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/c/ce3a9bdf48e82fcb36e32dd9352906798644f8e6_2_618x500.png)image1140×922 43.9 KB](https://ethereum-magicians.org/uploads/default/ce3a9bdf48e82fcb36e32dd9352906798644f8e6)

---

**ins-evm** (2023-12-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fancyking/48/11311_2.png) FancyKing:

> By carrying the inscription through events in the EVM and making the inscription compatible with the EVM, will there still be the disadvantage of excessive gas cost? How to solve this?

The Ordinals protocol provides a great solution - [Recursion](https://docs.ordinals.com/inscriptions/recursion.html#recursion).

---

**Texasgun** (2023-12-28):

Hey brother the ins20 twitter account has been very quiet lately. Are there any plans, or announcements coming for the community? Will there be more engagement with the community in the future? Leaving the project in suspense for days at a time doesn’t help much.

---

**ins-evm** (2023-12-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/texasgun/48/11313_2.png) Texasgun:

> Hey brother the ins20 twitter account has been very quiet lately. Are there any plans, or announcements coming for the community? Will there be more engagement with the community in the future? Leaving the project in suspense for days at a time doesn’t help much.

The best community is right here! ![:hugs:](https://ethereum-magicians.org/images/emoji/twitter/hugs.png?v=12) ![:hugs:](https://ethereum-magicians.org/images/emoji/twitter/hugs.png?v=12) ![:hugs:](https://ethereum-magicians.org/images/emoji/twitter/hugs.png?v=12)

---

**ins-evm** (2023-12-28):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/z/f0a364/48.png) zzzz:

> Sir, a good idea is certainly important. Have you considered establishing a community belonging to INSC on DC or TG, so that more like-minded friends can join this discussion? This project is fantastic

Bro, this is the best community right here, and I will encourage everyone to engage in discussions here ![:hugs:](https://ethereum-magicians.org/images/emoji/twitter/hugs.png?v=12) ![:hugs:](https://ethereum-magicians.org/images/emoji/twitter/hugs.png?v=12) ![:hugs:](https://ethereum-magicians.org/images/emoji/twitter/hugs.png?v=12)

---

**SergeantPonzi** (2023-12-28):

Hello, when you say snapshot, does that mean you intend on relaunching the project with the improved code from this github? i’m worried you leave the ins20 community behind that have been supporting the project passively.


*(52 more replies not shown)*

---
source: magicians
topic_id: 8410
title: "ERC-4841: Expandable Onchain SVG Images Storage"
author: Soohan-Park
date: "2022-02-24"
category: EIPs
tags: [nft, storage, onchain, svg]
url: https://ethereum-magicians.org/t/erc-4841-expandable-onchain-svg-images-storage/8410
views: 2139
likes: 4
posts_count: 11
---

# ERC-4841: Expandable Onchain SVG Images Storage

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/4841)














####


      `master` ← `soohanpark:master`




          opened 08:07AM - 23 Feb 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/b/bda1ff22298d6518e86f1e0949ce451e678ed0a2.jpeg)
            soohanpark](https://github.com/soohanpark)



          [+607
            -0](https://github.com/ethereum/EIPs/pull/4841/files)







We proposal an EIP, **Expandable Onchain SVG Images Storage**

---

When ope[…](https://github.com/ethereum/EIPs/pull/4841)ning a pull request to submit a new EIP, please use the suggested template: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












I’d like to know what you guys think about this and I am always happy to get to your feedback, such as the possibility of adopting the EIP and comments on further improvements ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

## Replies

**SamWilsn** (2022-03-25):

I think this proposal is useful, but I don’t think it needs to be an ERC (or if it does, it needs to make the case for that better in the `Motivation` section.) Instead, I think it would be useful as a library or framework.

At minimum, I think it’ll need a way to indicate to NFT marketplaces that the image is available somewhere else. Could maybe be a special scheme in the return value of `getURI`?

---

**Soohan-Park** (2022-04-06):

First of all, thank you for agreeing with our proposal.

After reading your feedback, we realized what we wrote didn’t fully explain what we were trying to explain. So, we are working on improvement the overall content now. (Please refer to the [GitHub pull request comments](https://github.com/ethereum/EIPs/pull/4841#issuecomment-1082535480) ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12))

Based on your feedback, we improved on the Motivation section like below. (We are in the process of requesting proofreading, so we got help from Google. If there is something you do not understand, please feel free to leave a comment!)

> Most NFT projects keep their NFT content on centralized servers, not on Ethereum. Although this method is the cheapest and easiest way to manage the content of an NFT, there is a risk of damage or loss. In addition, even in the case of IPFS, tampering can be prevented with the Content-addressing, but there is a possibility of data loss if there is no node storing the contents of the NFT.
>
>
> One of the ideal ways to solve this problem is to store the content of the NFT on Ethereum in SVG image format. However, since the maximum size that can be distributed in one contract is about 24 kB, there is a problem that only small, simple SVG images can be saved.
>
>
> Therefore, to solve this problem, we devised a storage model consisting of three hierarchical structures: Storage, Assemble, and Property.
>
>
> With this storage model,
>
>
> XML ​​tags composing SVG images are distributed and stored in multiple contracts, and when SVG images are needed later, saved tags can be combined to obtain large-capacity SVG images.
> By dividing the storage into three independent tiers, you can ensure the ease of management and the flexibility of storage. For example, if the logic for assembling XML tags in the Assemble Layer needs to be changed, there is no need to re-record the values ​​stored in the Storage Layer or Property Layer in the block chain, only the contract of the layer that needs to be modified is newly distributed.
> Extensibility can be secured based on an independent hierarchical structure. If you want to add the configuration of SVG, you just need to distribute the contract to the Storage Layer and connect it with the Assemble Layer.
>
>
> We would like to propose a scalable storage model that stores large, high-quality SVG images on Ethereum.

Like Motivation above, we thought that this proposal could contribute to the Ethereum ecosystem based on three main advantages. Therefore, we would like to propose this proposal as a standard, and if there are any shortcomings to become a standard, we would be grateful if you could tell us what is it.

In addition, ERC is defined as below among the contents of [EIP-1](https://eips.ethereum.org/EIPS/eip-1), so we judged that it is suitable for the ERC category even if the contents we want to propose are close to the framework. If we are misunderstood, please let us know ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

> ERC: application-level standards and conventions, including contract standards such as token standards (EIP-20), name registries (EIP-137), URI schemes, library/package formats, and wallet formats.

Thanks for all always, guys.

---

**SamWilsn** (2022-04-06):

Hey! Thanks for taking the time to write a detailed reply ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Like I said, I really do see the benefit of splitting up SVGs into multiple contracts. I’ve encountered the contract size limit before with my NFT projects.

What I’m asking is: why does the method of splitting up SVGs need to be standardized into an ERC? If my token splits them up using method A, and your token uses method B, is that a problem?

I can certainly see the case for standardizing a replacement interface for `tokenURI` that marketplaces (like OpenSea) can use to retrieve the assembled image, but the interface shouldn’t depend on how the image is stored. I would be happy to be convinced otherwise though!

---

**Soohan-Park** (2022-05-16):

[@SamWilsn](/u/samwilsn)

We apologize for the very late reply due to our original work.

After receiving the feedback, we’ve been thinking a lot about the EIP.

We sympathize with the content of the feedback, and we have recognized that the method of storing data is difficult to establish as a standard.

And we don’t have any special ideas to replace `tokenURI`, so we’re going to close this EIP and this thread.

*([@everyone](/groups/everyone) If anyone has a good idea, it would be great to develop this EIP together!)*

Thanks a lot for your feedback and interest. And we will come back with better ideas for improving Ethereum ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**IronMan_CH** (2022-07-13):

[@Soohan-Park](/u/soohan-park) In my opinion, the tokenURI format of on-chain image format is vacant, so why can’t we just continue this EIP with standard tokenURI format of on-chain image.

---

**SamWilsn** (2022-07-22):

One option might be to combine [EIP-4804](https://eips.ethereum.org/EIPS/eip-4804) with `tokenURI`?

---

**buoynous** (2022-07-28):

Sorry in advance but I want to ask a potential dumb question.

The data size we want to store within our contract is not a problem is it? [gas - How much data can I store in a smart contract, what is the cost and how it is implemented? - Ethereum Stack Exchange](https://ethereum.stackexchange.com/questions/68712/how-much-data-can-i-store-in-a-smart-contract-what-is-the-cost-and-how-it-is-im)

I am under the impression that all you need to worry about is the one time gas cost you have to pay to have this data stored within the contract during mint of an NFT.

OR

Is the concern here that if we want to store a large SVG image but having this live within the contract to deploy exceeds the 24KB threshold?

It is probably the latter, but just want to confirm.

And final question, not really related to this but still relevant. Technically we could pass in this SVG image via call data to the mint function but in this case the gas cost will be too high for Ethereum. But for a chain like Polygon this shouldn’t be a problem right? I guess it isn’t sustainable because it is dependent on the fact that Polygon will always stay this cheap but does that make sense?

---

**Soohan-Park** (2022-08-02):

[@IronMan_CH](/u/ironman_ch) [@SamWilsn](/u/samwilsn)

Well, actually I hope to keep running to make a standard this idea ![:joy:](https://ethereum-magicians.org/images/emoji/twitter/joy.png?v=12)

But, when I was wrote the last comment, I thought “EIP is a standard. This idea, EIP-4841, is one way of storing data but it is not proper to be a STANDARD.”.

Because, I agreed with [@SamWilsn](/u/samwilsn)’s opinion that the method of storing data is difficult to be standard, and there was no point like tokenURI.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> What I’m asking is: why does the method of splitting up SVGs need to be standardized into an ERC? If my token splits them up using method A, and your token uses method B, is that a problem?

However, sometimes I wonder if I may have rushed to close this issue.

I really wanna know what you guys think about this EIP suggestion…!

could this suggestion be an EIP…?

---

**Soohan-Park** (2022-08-02):

Hi [@buoynous](/u/buoynous)  ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buoynous/48/6556_2.png) buoynous:

> The data size we want to store within our contract is not a problem is it?

 → Yeah, it was a problem and it was the reson why I suggest this EIP. In this EIP, it try to solving through `divide & conquer`. Such as **SVG Image format** can be seperated to some bunch of tags, as you already know. So, this idea use the property to solve the problem.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buoynous/48/6556_2.png) buoynous:

> Is the concern here that if we want to store a large SVG image but having this live within the contract to deploy exceeds the 24KB threshold?

 → Right.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/buoynous/48/6556_2.png) buoynous:

> And final question, not really related to this but still relevant. Technically we could pass in this SVG image via call data to the mint function but in this case the gas cost will be too high for Ethereum. But for a chain like Polygon this shouldn’t be a problem right? I guess it isn’t sustainable because it is dependent on the fact that Polygon will always stay this cheap but does that make sense?

 → Absolutely agreed that. When this EIP was first proposed, an implementation of this EIP was created and tested. The cost of storing large-sized data was also high, but the cost was higher as the data was divided and stored. (At the time, when testing 301 KB of SVG image storage, approximately 8 ETH was consumed. Of course, it is my fault for not optimizing! ![:joy:](https://ethereum-magicians.org/images/emoji/twitter/joy.png?v=12) )

As you said, it would be a better model for low-cost networks like Polygon or Klaytn. Of course, there is no guarantee that the network will be permanently cheap!

However, the reason this EIP is proposed as Ethereum is because it is the largest and more durable network. (And, there are many magicians here!) And, looking at the community of other networks based EVM, many people, including myself, are using the EIP standard in that network. Therefore, if this proposal becomes a standard in Ethereum, I think it will be propagated to other EVM-based networks.

---

**IronMan_CH** (2022-08-16):

Feel free to close this issue. Also agree with [@SamWilsn](/u/samwilsn) 's opinion.


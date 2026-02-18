---
source: magicians
topic_id: 18097
title: Collateralized NFT Standard
author: harpocrates555
date: "2024-01-12"
category: ERCs
tags: [nft, erc-721, erc20]
url: https://ethereum-magicians.org/t/collateralized-nft-standard/18097
views: 1898
likes: 9
posts_count: 8
---

# Collateralized NFT Standard

**Abstract**

This proposal recommends an extension of EIP-721 to allow for collateralization using a list of EIP-20 based tokens. The proprietor of this EIP collection could hold both the native coin and EIP-20 based tokens, with the tokenId acting as the access key to unlock the associated portion of the underlying EIP-20 balance.

**Helpful Links**

**New EIP**



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/8109)














####


      `master` ← `harpocrates555:master`




          opened 05:37PM - 12 Jan 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/e/efc008d4605c8e648ad59ccbbcffdf099a9feca6.jpeg)
            harpocrates555](https://github.com/harpocrates555)



          [+457
            -75](https://github.com/ethereum/EIPs/pull/8109/files)







**ATTENTION: ERC-RELATED PULL REQUESTS NOW OCCUR IN [ETHEREUM/ERCS](https://gith[…](https://github.com/ethereum/EIPs/pull/8109)ub.com/ethereum/ercs)**

--

When opening a pull request to submit a new EIP, please use the suggested template: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












**ghostNFT Github**



      [github.com](https://github.com/realGhostChain/ERC721Envious)




  ![image](https://opengraph.githubassets.com/ae589230cce4a971490a413a50009e74/realGhostChain/ERC721Envious)



###



Contribute to realGhostChain/ERC721Envious development by creating an account on GitHub.










We would love to get feedback!

## Replies

**harpocrates555** (2024-01-12):

**Links to Lightpaper / Docs of this EIP Implementation**

**ghostNFT Lightpaper**



      [blog.ghostchain.io](https://blog.ghostchain.io/wp-content/uploads/2022/12/ghostNFT_Litepaper.pdf)



    https://blog.ghostchain.io/wp-content/uploads/2022/12/ghostNFT_Litepaper.pdf

###



876.54 KB










**ghostNFT Docs**

https://docs.nft.ghostchain.io/en/latest/index.html

---

**harpocrates555** (2024-01-12):

**Links to Products that Implemented this EIP**

**ghostNFT is live on 20+ EVM Chains**


      ![](https://ethereum-magicians.org/uploads/default/original/2X/3/32c6b81af3eeeaa9685efc0110d4d92fd6f47752.png)

      [app.nft.ghostchain.io](https://app.nft.ghostchain.io/)



    ![](https://ethereum-magicians.org/uploads/default/optimized/2X/8/86f74228f2d53fbdf6230900d26ed8a2dbff7839_2_690x361.png)

###



NFT 2.0 standard that enables asset-backed NFTs to provide more versatility for NFT holders and creators.










**John McAfee Legacy (JML) NFT Collection is live on 20+ EVM Chains**


      ![](https://jml.ghostchain.io/wp-content/uploads/2024/10/cropped-logo-32x32.png)

      [John McAfee Legacy (JML) NFT Collection](https://jml.ghostchain.io/)



    ![](https://ethereum-magicians.org/uploads/default/optimized/2X/1/176aeec98463911f5d1fae80d3aabd6665cd41b3_2_690x361.png)

###



John McAfee Legacy (JML) NFT Collection is a collection of 70,000+ unique JML gNFTs— unique digital collectibles living on 15+ blockchains.

---

**Federalpikin** (2024-02-02):

This is the best  project of the season,

Great project with potentials ![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)

---

**xinbenlv** (2024-03-29):

Hi authors of ERC-7595, this is Victor, an EIP editor and current operator of AllERCDevs.

I like to invite you to our next AllERCDevs meeting (online) to present for 10min of your ERCs if you are interested!

AllERCDevs is a bi-weekly meeting for ERC authors, builders and editors to meet and help the drafting and adoption of an ERC. The next one is 2024-04-02 UTC 2300, let us know if this time works for you, I can put this ERC in the agenda, or you can add a response directly at [(Future) 2024-04-02 (E2S2) AllERCDevs Agenda Thursday (Asia/US friendly time) · Issue #19 · ercref/AllERCDevs · GitHub](https://github.com/ercref/AllERCDevs/issues/19)

---

**harpocrates555** (2024-05-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> AllERCDevs is a bi-weekly m

Hi Victor! Pleasure to meet you. It will be great to participate in AllERCDevs meeting. Please let us know when is the next meeting, and what’s the best venue thru which to coordinate the meeting details.

---

**SamWilsn** (2024-06-19):

> However, a native coin does not carry an address. To address this, we propose utilizing a null address (0x0000000000000000000000000000000000000000) […]

Tiny suggestion, but we have [ERC-7528: ETH (Native Asset) Address Convention](https://eips.ethereum.org/EIPS/eip-7528) that suggests using `0xeee...eee` for a placeholder address for the native token of a chain.

---

**harpocrates555** (2024-07-18):

Great suggestion!! We will look into the usage of `0xeee...eee` instead of `0x000...000`. Would love to learn if there are any other comments/feedback/suggestions.


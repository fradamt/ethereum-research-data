---
source: magicians
topic_id: 12479
title: ERC-721 Subordinate
author: sullof
date: "2023-01-07"
category: ERCs
tags: [nft, token]
url: https://ethereum-magicians.org/t/erc-721-subordinate/12479
views: 1933
likes: 6
posts_count: 20
---

# ERC-721 Subordinate

A subordinate ERC721 contract is a type of non-fungible token (NFT) that follows the ownership of a dominant NFT. The dominant NFT can be an ERC721 contract that does not have any additional features.

**ADD-ON, Jan, 15th**  To avoid confusion with hierarchical structures, a subordinate token does not perform any minting, transfer, approval, etc. When it is deployed, if address 0xA owns the token ID #100 of the dominant token, address 0xA also owns token ID #100 of the subordinate.

If dominant #100 is tranferred, it emits a Transfer event, but the subordinate will be also “transferred” but no events will be emitted.

This is a very specific case, and it is best to look at the implementation to fully understand what it means.

## Why

In 2021, when we started Everdragons2, we had in mind using the head of the dragons for a PFP token based on the Everdragons2 that you own. Here is an example of a full dragon

https://github.com/ndujaLabs/ds-protocol/blob/main/assets/Soolhoth.png

and here is just the head

https://github.com/ndujaLabs/ds-protocol/blob/main/assets/Soolhoth_PFP.png

The question was, “Should we allow people to transfer the PFP separately from the primary NFT?” It didn’t make much sense. At the same time, how to avoid that?

ERC721Subordinate introduces subordinate tokens that are owned by whoever owns the dominant token. As a result, the subordinate token cannot be approved or transferred separately from the dominant token. It is transferred when the dominant token is transferred.

## Some use cases

- A token that represents a specific aspect of a dominant token (like the Everdragons2 PFP).
- A token that represents an asset of the dominant token (think of the dominant as a wallet).
- A token that adds missed features to the dominant token.

You can see an ERC721Subordinate like a soulbound token, where the soul is not a wallet, but an NFT. Starting from this very simple concept, there are plenty of services that become possible thanks to it.

## Update April

Most markeplaces do not see subordinate tokens because they listen to Transfer events. In latest version of the DS-protocol, I implemented a deferred emission that happens anytime the dominant is transferred. This, however, is not applicable to existing, immutable standard tokens.

## Replies

**Pandapip1** (2023-01-08):

This seems very similar to [EIP-6150: Hierarchical NFTs, an extension to ERC-721](https://ethereum-magicians.org/t/eip-6150-hierarchical-nfts-an-extension-to-erc-721/12173) or [EIP-3652: Hierarchical NFT](https://ethereum-magicians.org/t/eip-3652-hierarchical-nft/6963).

---

**sullof** (2023-01-08):

Thanks. I missed those extensions. Before starting working on it, I looked for existing proposal without results. If you don’t get the naming it is quite hard to find info. This is the second time that I work on something for a while before discovering that it was mostly already there.

An AI app would probably help. I will think about it.

---

**sullof** (2023-01-08):

EIP-6150 aims to create a flexible, generic, and powerful structure, similar to how file systems work. On the other hand, ERC721Subordinate aims to solve a specific problem with the simplest possible solution, using existing assets that cannot be modified to add new features.

For example, to prevent an infinite loop such as “A is the father of B, which is the father of C, which is the father of A”, it is necessary for all contracts in the tree to follow the same rules. However, this may not be possible with existing tokens. In contrast, ERC721Subordinate handles a simpler case where there is only a direct relationship between a parent and its children. More specifically, the child “adopts” its parent, without any change in the parent is required. It does not consider the possibility that children have their own children, as this would make the system difficult to manage without having control over all deployed smart contracts.

In summary, while the two proposals may appear similar, they are actually quite different.

---

**k06a** (2023-01-08):

I would highly recommend to check out [EIP-3652: Hierarchical NFT](https://ethereum-magicians.org/t/eip-3652-hierarchical-nft/6963), since it more agile approach. Each existing NFT gets own address which could be managed by this NFT owner.

---

**sullof** (2023-01-08):

That EIP is closed. I don’t see any development there.

Anyway I took a look at your implementation at



      [github.com](https://github.com/1inch/ERC3652)




  ![image](https://opengraph.githubassets.com/70e45e5bac6094cda7b576feeb334dc2/1inch/ERC3652)



###



Contribute to 1inch/ERC3652 development by creating an account on GitHub.










I think the concept is good but my understanding is that all the node in the hierarchy must follow the standard. That makes it very different from my proposal that aims to associate subordinate NFT to existing NFT that are immutable and cannot be modified.

For example, let’s say that BAYC wants to add features to their own Ape token, using a subordinate contract, fully linked to the Ape token, they can get that result.

---

**sullof** (2023-01-08):

(I edited and simplified the post to make it more clear.)

---

**sullof** (2023-01-15):

I am considering implementing the [EIP-5192 Minimal Soulbound NFTs standard](https://ethereum-magicians.org/t/final-eip-5192-minimal-soulbound-nfts/9814), even though events can not be emitted by a subordinate contract, as the EIP-5192 makes the emission of events optional. I am not particularly fond of this approach, as I believe that such a simple interface should require the emission of events. In my opinion, it would be better to have two separate interfaces:

```auto
interface IERC5192 {
  function locked(uint tokenId) external view returns(bool);
}
```

and

```auto
interface IERC5192Extended is IERC5192 {
  // events MUST be emitted
  event Locked(uint tokenId);
  event Unlocked(uint tokenId);
}
```

This way, a subordinate contract could implement the first interface without being required to implement the second. However, I understand that a compromise solution is better than no solution at all, so I may proceed with implementing it.

---

**k06a** (2023-01-18):

ERC3652 requires absolutely no support from NFT. It introduces new ownership layer for all existing and future NFTs.

---

**sullof** (2023-01-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/k06a/48/1421_2.png) k06a:

> ERC3652 requires absolutely no support from NFT. It introduces new ownership layer for all existing and future NFTs.

Looking at the closed PR and the actual proposal, I got what you mean. You are totally right, but you are also wrong suggesting to adopt it to solve the problem I am trying to solve, because that does not solve the issue.

---

**k06a** (2023-01-21):

I thought you are looking for a way transfer you NFT with sub-NFTs. This would work for this purpose.

---

**sullof** (2023-01-21):

That is not what we are trying to solve here.

A subordinate NFT has not control whatsoever on the ownership. It is a satellite of the dominant token. It just adds features to an existing token, without requiring any change in the existing token.

But maybe I am just not understanding it. Can I create a non-transferable token that gives a hat to any Bored Ape token, so that if I own BAYC #3 I have Bore Hat #3 and if I transfer BAYC #3 the new owner is also the owner of the Hat #3 without doing anything with the Hat NFT?

If that is possible with ERC3652, we can support it.

---

**k06a** (2023-01-22):

Yes, exactly. With EIP-3652 every existing NFTs and not-yet-exising NFTs get address for OWNING any other asset including NFTs. And owner of NFT can spend and use assets owned by any NFT.

---

**sullof** (2023-01-22):

I am not convinced, yet, but that sounds good.

I will try to better understand your proposal. Thanks

---

**sullof** (2023-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/k06a/48/1421_2.png) k06a:

> Yes, exactly.

I studied your doc at



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/3652/files#diff-b9a08dc3c2c8244137775be541ac3de41018b803f07e2ec17b31f71185efbc03)














####


      `master` ← `1inch:hierachical-nft`




          opened 11:36PM - 12 Jul 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/b/b8adfc510d9af5428fd99073ca88ad6165fd5839.jpeg)
            k06a](https://github.com/k06a)



          [+102
            -0](https://github.com/ethereum/EIPs/pull/3652/files)







WIP












and I studied your implementation and looking at the tests at



      [github.com/1inch/ERC3652](https://github.com/1inch/ERC3652/blob/master/test/ERC3652.js)





####

  [master](https://github.com/1inch/ERC3652/blob/master/test/ERC3652.js)



```js
require('@openzeppelin/test-helpers');
const { expectRevert } = require('@openzeppelin/test-helpers');
const { web3 } = require('@openzeppelin/test-helpers/src/setup');
const { expect } = require('chai');

const ERC3652 = artifacts.require('ERC3652');
const ERC3652Proxy = artifacts.require('IERC3652Proxy');
const TokenMock = artifacts.require('TokenMock');
const NFTMock = artifacts.require('NFTMock');
const TokenTransferDelegatee = artifacts.require('TokenTransferDelegatee');

describe('ERC3652', async function () {
    let w1, w2;

    before(async function () {
        [w1, w2] = await web3.eth.getAccounts();
    });

    beforeEach(async function () {
        this.nft = await NFTMock.new('Game of NTF', 'GONFT');
```

  This file has been truncated. [show original](https://github.com/1inch/ERC3652/blob/master/test/ERC3652.js)










While I find you proposal brilliant, I really don’t get how that can solve the same issue that I am trying to solve here.

What we are doing here is to deploy a new contract that, after the deploying, does not need and does not allow any interaction. Everything exists just because the dominant token exists. I don’t see how that could be done with your proposal. If you take a look at my implementation at [DS-protocol/contracts/ERC721Subordinate.sol at main · cruna-cc/DS-protocol · GitHub](https://github.com/ndujaLabs/erc721subordinate/blob/main/contracts/ERC721Subordinate.sol)

I think that it should be clear.

---

**k06a** (2023-01-22):

Please check out this branch with this simple implementation: [GitHub - 1inch/ERC3652 at feature/simplification](https://github.com/1inch/ERC3652/tree/feature/simplification)

---

**sullof** (2023-01-23):

That is useful, thanks. However, based on what I see in the test at https://github.com/1inch/ERC3652/blob/feature/simplification/test/ERC3652.js, it appears that a new proxy contract must be deployed for each specific token ID of the NFTMock.

I think that the ERC-3652 standard can be useful in many situations, but it may not be suitable for our particular situation. If we have 10,000 tokens, it would be much more efficient to deploy a single subordinate contract that can handle all of them, rather than calling the factory 10,000 times to deploy a new proxy contract for each token ID.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8ff758518476c5d39ee94de88a02ee640b655491_2_690x148.png)image1338×288 48.9 KB](https://ethereum-magicians.org/uploads/default/8ff758518476c5d39ee94de88a02ee640b655491)

Am I mistaken?

---

**k06a** (2023-01-23):

Yep, it requires deploying small proxy contracts for each NFT, but good thing is that they could be deployed on demand. You could use their addresses to receive assets/NFTs without deployments.

---

**sullof** (2023-01-24):

Thanks for the clarification.

For Everdragons2, we will stick to the current approach because it is much more efficient and reaches the goal — giving genesis tokens’ owner a new token just by deploying its contract.

However, I think that your proposal is brilliant, and I may use it for another project where it would make a lot of sense. Let me know if I can help in any way with that.

---

**sullof** (2023-05-27):

Update. After studying many suggested alternatives — like ERC6551 which is very good and which I am using in the Cruna Protocol — I believe that the subordinate contract approach solves the specific case of two bound NFTs described in the introduction better than any other solution.


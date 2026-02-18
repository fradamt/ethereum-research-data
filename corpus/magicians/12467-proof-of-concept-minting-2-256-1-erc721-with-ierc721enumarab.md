---
source: magicians
topic_id: 12467
title: "Proof of concept: minting 2**256 -1 ERC721 with IERC721Enumarable capability"
author: sciNFTist.eth
date: "2023-01-06"
category: ERCs
tags: [nft, token, erc-721]
url: https://ethereum-magicians.org/t/proof-of-concept-minting-2-256-1-erc721-with-ierc721enumarable-capability/12467
views: 897
likes: 2
posts_count: 3
---

# Proof of concept: minting 2**256 -1 ERC721 with IERC721Enumarable capability

# Limits of NFT(ERC721Enumerable) or Minting 2^256 - 1 NFT

## warning:

these contract have been altered for proof of concept and they are different than the proposed Implementation. please see this [link](https://ethereum-magicians.org/t/use-zero-gas-0-gwei-for-minting-any-number-of-nft/12403) to learn more about mechanism and rationale

## Abstract

The upper limit of `totalSupply` of any ERC721 contract or how many NFT can be minted, is determined by the EIP-721 is `uint256` number.

so the upper limit for totalSupply is this number:

115792089237316195423570985008687907853269984665640564039457584007913129639935

In my Implementation proposal I’ve talked about how this can be reached:

[see the implementation here](https://ethereum-magicians.org/t/eip-draft-mint-arbitrary-number-of-tokens-erc-721-via-eip-2309/11589)

## See the project in Action:

I’ve deployed a contract on goerli for proof of concept.

goerli Limits of NFT: [0x6d04C3F8e618a2404803Ca72f5dF93f4F50CaD45](https://goerli.etherscan.io/token/0x6d04c3f8e618a2404803ca72f5df93f4f50cad45)

[![tokenTracker](https://ethereum-magicians.org/uploads/default/original/2X/4/4d804820718177f7282633dc8dffd0ce351fa352.png)tokenTracker878×390 21.9 KB](https://ethereum-magicians.org/uploads/default/4d804820718177f7282633dc8dffd0ce351fa352)

this token is Fully IERC721 and IERC721Enumerable compatible.

I highly recommend you try it for yourself.

[![ERC721interface_showdown](https://ethereum-magicians.org/uploads/default/optimized/2X/7/7f8f35068ecca5e419d9232828db18f470fc2e24_2_690x438.png)ERC721interface_showdown1098×698 31.5 KB](https://ethereum-magicians.org/uploads/default/7f8f35068ecca5e419d9232828db18f470fc2e24)

from blanceOf() to ownerOf()

[![ownerOf](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5c454eacde77e7f9e411a6c22441aa15f765954e_2_362x500.png)ownerOf649×896 53.5 KB](https://ethereum-magicians.org/uploads/default/5c454eacde77e7f9e411a6c22441aa15f765954e)

even tokenOfOwnerbyIndex().

[![tokenOfOwnerbyIndex](https://ethereum-magicians.org/uploads/default/optimized/2X/7/71424c8eb859bd8df54ee8b2243d09b269c07ae1_2_689x303.png)tokenOfOwnerbyIndex1290×568 28.7 KB](https://ethereum-magicians.org/uploads/default/71424c8eb859bd8df54ee8b2243d09b269c07ae1)

## try it for yourself

All of these tokens are minted to “giver” contract that you can grab one for yourself.

[![giver](https://ethereum-magicians.org/uploads/default/original/2X/2/268ac1bd85c0e18766b547f56a0e19d52ccb7ed5.png)giver898×650 21.1 KB](https://ethereum-magicians.org/uploads/default/268ac1bd85c0e18766b547f56a0e19d52ccb7ed5)

1. by calling the getToken() you will get a token from index of 0 of the preOwner(giver address).
2. by calling the getTokenInd(Index) you will get a token from index of Index of the preOwner(giver address).

giver goerli : [0x65c94c08Dd504a199fE61C3D29ca01784C7081aF](https://goerli.etherscan.io/address/0x65c94c08dd504a199fe61c3d29ca01784c7081af#writeContract)

### URI:

for proof of concept this contract have an SVG Image with tokenId on it.

[![tokenURI](https://ethereum-magicians.org/uploads/default/original/2X/f/f00ce041761d3375ca60e5e5c4a542f8aa4ed343.png)tokenURI881×684 35 KB](https://ethereum-magicians.org/uploads/default/f00ce041761d3375ca60e5e5c4a542f8aa4ed343)

the Image:

[![Image](https://ethereum-magicians.org/uploads/default/original/2X/0/0e0861d1e7bddf2c06d0aeee7267628fb747c4fe.png)Image892×595 2.24 KB](https://ethereum-magicians.org/uploads/default/0e0861d1e7bddf2c06d0aeee7267628fb747c4fe)

## conclusion:

this project shows:

1. limit of uint256 for totalSupply for ERC721 can be reached.
2. zero transaction minting is possible.
3. batch minting via EIP-2309 and IERC721Enumerable is possible.

### please join the disscussion:

[Ethereum magician: Use zero gas(0 gwei) for minting any number of NFT](https://ethereum-magicians.org/t/use-zero-gas-0-gwei-for-minting-any-number-of-nft/12403)

## Replies

**abcoathup** (2023-01-06):

OpenSea appears to stop indexing at 5000.




      [OpenSea](https://testnets.opensea.io/assets/goerli/0x6d04c3f8e618a2404803ca72f5df93f4f50cad45/4999)



    ![image](https://openseauserdata.com/files/fd084a0c3d3486d3dfb1e33d1f6f28a5.svg)

###



get one from [this-contract](https://goerli.etherscan.io/address/0x65c94c08dd504a199fe61c3d29ca01784c7081af#writeContract) by calling getToken() function.
see the...










https://testnets.opensea.io/assets/goerli/0x6d04c3f8e618a2404803ca72f5df93f4f50cad45/5000

OpenZeppelin use a 5000 maximum limit for this purpose:



      [github.com](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/ERC721Consecutive.sol#L48)





####



```sol


1.
2. /**
3. * @dev Maximum size of a batch of consecutive tokens. This is designed to limit stress on off-chain indexing
4. * services that have to record one entry per token, and have protections against "unreasonably large" batches of
5. * tokens.
6. *
7. * NOTE: Overriding the default value of 5000 will not cause on-chain issues, but may result in the asset not being
8. * correctly supported by off-chain indexing services (including marketplaces).
9. */
10. function _maxBatchSize() internal view virtual returns (uint96) {
11. return 5000;
12. }
13.
14. /**
15. * @dev See {ERC721-_ownerOf}. Override that checks the sequential ownership structure for tokens that have
16. * been minted as part of a batch, and not yet transferred.
17. */
18. function _ownerOf(uint256 tokenId) internal view virtual override returns (address) {
19. address owner = super._ownerOf(tokenId);
20.
21. // If token is owned by the core, or beyond consecutive range, return base value


```

---

**sciNFTist.eth** (2023-01-06):

yeah, I know about this limit

so I’ve wrote this function

```auto
uint256 private emitCounter = 1;

 // in case the marketplace need this
    function emitHandlerSingle() public {
        emit ConsecutiveTransfer(
            emitCounter * 5000,
            emitCounter  * 5000  + 4999,
            address(0),
            preOwner_
        );
        emitCounter++;
    }
```

PS: I made a typo on the contract in the contract this is the what I think solves the problem ![:shushing_face:](https://ethereum-magicians.org/images/emoji/twitter/shushing_face.png?v=12)

the problem will be solved with this function.

I know it’s not it’s not feasible to call it 2*256/5000 times but I’ve tried it in bundle of 100 `consecutiveTransfer` event with gas around 500k another [TX](https://etherscan.io/tx/0xefc674ed301c0012ed1bc1a8b8282ffdcb5502adcebc68fe9405229eb4a70a7b) and [looksrare](https://looksrare.org/collections/0x51E3406aE49cEC80607f97CA900fE932090dCF88?queryID=713acf18e03893266d7770a61fed6e36) kept resolving them till 530K Item then they stopped it.

---

I think marketplace indexer should propose another limit like a daily limit or something else 5000 is a bit small I think.

[@abcoathup](/u/abcoathup)

also, a really **important** question, is it possible to use **ERC721Consecutive.sol** and **ERC721Enumerable.sol** at the same time?

my guess is no because of this part from ERC721Consecutive:

```auto
IMPORTANT: This extension bypasses the hooks {_beforeTokenTransfer} and {_afterTokenTransfer} for tokens minted in
 * batch. When using this extension, you should consider the {_beforeConsecutiveTokenTransfer} and
 * {_afterConsecutiveTokenTransfer} hooks in addition to {_beforeTokenTransfer} and {_afterTokenTransfer}.
 *
 * IMPORTANT: When overriding {_afterTokenTransfer}, be careful about call ordering. {ownerOf} may return invalid
 * values during the {_afterTokenTransfer} execution if the super call is not called first. To be safe, execute the
 * super call before your custom logic.
 *
```


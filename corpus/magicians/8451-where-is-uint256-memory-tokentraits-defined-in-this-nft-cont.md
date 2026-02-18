---
source: magicians
topic_id: 8451
title: Where is 'uint256[] memory tokenTraits' defined in this NFT contract?
author: RustBucket45
date: "2022-02-28"
category: Magicians > Primordial Soup
tags: [questions]
url: https://ethereum-magicians.org/t/where-is-uint256-memory-tokentraits-defined-in-this-nft-contract/8451
views: 648
likes: 0
posts_count: 2
---

# Where is 'uint256[] memory tokenTraits' defined in this NFT contract?

Hello,

I’m looking into NFT contracts and I am analyzing the infamous CREEPZ INVASION GROUNDS contract.

Viewable at https://etherscan.io/address/0xc3503192343eae4b435e4a1211c5d28bf6f6a696#code

On line 307 of  CBCStaking.sol,  the function _setTokensValues takes two arrays from memory as arguments, which are used to set the yield value ($loomi token) for a staked NFT. They are uint256[] memory tokenIds, and uint256[] memory tokenTraits.

```auto
function _setTokensValues(
      address contractAddress,
      uint256[] memory tokenIds,
      uint256[] memory tokenTraits
    ) internal {
      require(tokenIds.length == tokenTraits.length, "Wrong arrays provided");
      for (uint256 i; i < tokenIds.length; i++) {
        if (tokenTraits[i] != 0 && tokenTraits[i] <= 3000 ether) {
          _tokensMultiplier[contractAddress][tokenIds[i]] = tokenTraits[i];
        }
      }
    }
```

How was data first input into those arrays? Where are they first defined? tokenTraits[] in particular only exists in CBCStaking.sol as arguments for functions. Outside of that it is not present in any other creepz contracts.

How do they do it? If they are derived from the metadata somehow, where is the function responsible

## Replies

**weiscracker** (2022-07-23):

It’s provided to the “deposit” function which in turn calls _setTokensValues. Your clues are the _ in front of the function name which can indicate something is an internal function or variable, and the fact that _setTokensValues is declared as an internal function. This means it only gets called by another function inside the same contract. So it looks like this is done via website most likely and they call the deposit function with the “correct” traits and sign it so that the contract knows it came from the website and not me or you spoofing the “wrong” traits.


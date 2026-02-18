---
source: magicians
topic_id: 8602
title: ERC721 minting only one token
author: victormunoz
date: "2022-03-14"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/erc721-minting-only-one-token/8602
views: 2986
likes: 2
posts_count: 5
---

# ERC721 minting only one token

If the ERC721 was modified to mint only 1 token (per contract), then the contract address could be identified uniquely with that minted token (instead of the tuple contract address + token id, as ERC721 requires).

This change would enable automaticlaly all the capabilities of composable tokens ERC-998 (own other ERC721 or ERC20) natively without adding any extra code, just forbidding to mint more than one token per deployed contract.

Then the NFT minted with this contract could operate with his “budget” (the ERC20 he owned) and also trade with the other NFTs he could own. Just like an autonomous agent, that could decide what to do with his properties (sell his NFTs, buy other NFTs, etc). Well not really autonomous, because it still requires external inputs to operate, but kind of…

For sure additional code and functions should be added to the implementation to allow all these operations.

I am thinking on submitting a new EIP for this “NFTs with wallet” (not sure how to name it yet), but first wanted to know other opinions on this idea (as suggested in the EIP guidelines).

Does this make sense for you?

## Replies

**peplluis7** (2022-03-18):

Having a unique token per NFT contract should be constructed at the rollout of the said contract, and no more. I’d prefer to have a solid definition of a non fungible token with a wallet, but this ERC721 specialization might work as fine to me. I don’t know how to push an EIP, sorry.

Cheers

---

**SamWilsn** (2022-04-05):

Taking off my EIP editor hat and putting on my reviewer hat, I don’t think this EIP is fully thought through. It sounds like you want to basically make a smart contract wallet that you can transfer using ERC-721 functions?

That seems interesting, but the EIP as written is nowhere near specified enough to function as a smart contract wallet. There’s so much more that has to go into it.

If you want to explore this route more, I’d recommend checking out the contracts powering existing smart contract wallets!

---

**MaxFlowO2** (2022-04-09):

wait… so you want an NFT in a EOA and the Contract as a vault?

---

**victormunoz** (2022-05-02):

Yes. This is basically a Smart Contract wallet that is also an NFT (ERC-721).

The initial name of this EIP was Wallet NFT, which I think is more understandable, but some editor changed it to “Contract with exactly one NFT”: [Wallet NFT proposal by victormunoz · Pull Request #4944 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4944/commits/98fd2aa6caa6f6b3e5ce453107d1b62f330bdf92)

Maybe I can re-edit the EIP title and elaborate more on the EIP purpose and specification.

Regarding current existing smart contract wallets, you mean EIP-173 right? (are there other smart contract wallets?) 173 is good for smart contract wallets, but the main point for my proposal is to be also an ERC-721 compatible contract.


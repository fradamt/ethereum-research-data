---
source: magicians
topic_id: 12443
title: "EIP-6260: Buyable NFT tokens on-Chain and Royalties"
author: lth-elm
date: "2023-01-05"
category: EIPs
tags: [erc, nft, royalties]
url: https://ethereum-magicians.org/t/eip-6260-buyable-nft-tokens-on-chain-and-royalties/12443
views: 1607
likes: 0
posts_count: 14
---

# EIP-6260: Buyable NFT tokens on-Chain and Royalties

This is the discussion link for [EIP-6260](https://github.com/ethereum/EIPs/pull/6260).

## Replies

**lth-elm** (2023-01-05):

Following numerous hacks last year where NFTs were stolen from major platforms (i.e Opensea), we thought of **integrating the NFT trading system directly on the blockchain, within the smart contract**. The main reason these hacks occurred was due to some platforms storing order signatures off-chain, inside their API. This allowed hackers to create a loophole, changing the NFT prices and effectively buying the pieces for a lower amount than their original price. The NFT trading system we thought about would allow total independence, as the user would be able to trade his NFT at any point, without relying on a marketplace. Using this system, it would also make total sense to create a standard which would guarantee royalties are correctly enforced (through the blockchain), as long as the sale or purchase follows this specific method.

As of now, we expect marketplaces to voluntarily pay royalties “off-chain”. But this process is not yet widely adopted and relies on the marketplace being trustworthy. We have created an improvement proposal that **automatically calculates & pays royalties on-chain for every token sold: EIP.** On top of that, our improvement proposal allows the ERC-721 token to be financially tradeable in ETH on-chain without the need for marketplaces and the issues that comes with them: security, royalties not respected or limited.

Whilst we are aware the code could be improved, we wanted to share the idea here on this forum. We greatly appreciate any pull requests aiming to optimise gas fees.

Additionally, we are conscious this improvement model by itself is only one brick to guarantee royalty-enforcement, simply because it does not stop the users from going on other marketplaces which may not enforce them (e.g. sudoswap, which attracted a lot of attention lately).

Therefore, the NFT smart contract may be abe to inherit from the Operator Filter Registry put in place by Opensea, allowing creators to blacklist marketplaces which do not enforce royalties. Alternatives may include [Blur.io](http://Blur.io)’s DefaultOperatorFilter solution, or Vectorized’s ClosedSea for a more gas-efficient solution.

Getting back to our improvement proposal, we build a decentralised NFT marketplace, fully hosted in a decentralized way in order to show and explain in its simplest way possible how our solution could be used: *see app link in above github repository*.

*NB: As of now, this solution only works with NFTs stored on-chain, for demonstration purposes.*

We truly believe this decentralised marketplace model could be of interest for users who may prefer full control over their holdings / creations, and may not trust third-party intermediaries such as Marketplaces.

---

**pizzarob** (2023-01-07):

Check out the LP as well. https://thelp.xyz

---

**lenifoti** (2023-01-07):

Im not sure that it is right to include the value of the royalty in this spec. This should be signalled using ERC 2981 as specified by opensea in their blog on royalty enforcement, and as used by other exchanges.

This eip could enforce the royalty by getting the royalty amount from the Erc 2981 interface or possibly a bespoke internal implementation.

But to be compliant with opensea enforcement it would need to support Erc 2981 anyway.

Thoughts?

---

**lth-elm** (2023-01-07):

Cool one I like the idea of holders collecting the fees

---

**lth-elm** (2023-01-07):

Right, we’ve also thought about it and mentionned it quickly in ***rationale***, at the end we were uncertain which approach was best for retrieving the royalty amount but since the idea was to be independent of a centralized marketplace we implemented it that way.

However you might be right, by supporting Erc 2981 the nft can be compliant on a wider scale. Unfortunately it seems like Erc 2981 it not widely adopted, not even by opensea.

---

**lenifoti** (2023-01-07):

Eip2981 is mentioned as the approved way of stating the royalty in the opensea blog on enforcement, so it appears that they do support it. In fact they appear to mandate it if a creator wants royalties enforced.

From the opensea blog:

‘Creators that prefer on-chain creator fee enforcement, will need to implement EIPD 2981 as their objective source of truth for creator fee preferences’

---

**lth-elm** (2023-01-07):

Yep you’re right they are supporting it starting January 2nd that’s just recent news.

Until now I’ve seen many complaints on forums and even myself was disappointed that it wasn’t supported for such a long time.

This will more likely accelerate the adoption of this EIP 2981 which is good news.

---

**lenifoti** (2023-01-12):

Sorry. Moving the discussion to this thread…

I think that there is sufficient crossover between this and the earlier eip that this one should not replace it. The question is - what functionality does it not support that this one does. This eip can add those features.

Likewise for eip 2981. It sounds like you have a requirement to change the percentage. That is something that 2981 does support but only as a  predefined rule, not after the NFT is minted. If that is something that you feel is missing then it can be added as part of this extension.

---

**SamWilsn** (2023-02-21):

I’d also like to mention [ERC-4910](https://eips.ethereum.org/EIPS/eip-4910) which seems to solve similar problems.

---

**lth-elm** (2023-02-22):

Yes I really think royalties percentage should be updatable at any time as long as it can only be decreased, this is however up to the creator and we might leave the door open for if they wants this feature or not.

As you mentioned in the PR the royaltyInfo semantics is also a bit different from EIP-2981, I agree with you that the royalty info function in this spec should better have the same semantics as 2981 so the implementation would support both models and act as an extension.

---

**lth-elm** (2023-02-22):

This looks really promising, thanks I will go through it.

---

**SamWilsn** (2023-03-10):

I think it’s important to note that this proposal is still opt-in for paying royalties. A seller can approve an escrow contract that only makes the transfer once sufficient ETH has been received, no royalties paid. Similarly, one could transfer ownership of a token to a wrapper token contract, which could be bought and sold freely, then unwrapped.

Given the work done on ERC-4910, and the limitations above, are you still interested in pursuing standardization?

---

**lth-elm** (2023-03-15):

We are well aware that there are techniques to bypass this model, the idea is not to create an absolute standard but rather provide an alternative to what is being done at present while providing an integration support (file on assets and personal GitHub).

Some people were interested in this model that we had integrated internally, that’s why my team and I started this standardization process. However, since there are similar standards it is not necessary to push it further than its draft stage.


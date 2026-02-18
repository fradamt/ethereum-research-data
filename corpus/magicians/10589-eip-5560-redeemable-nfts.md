---
source: magicians
topic_id: 10589
title: "EIP-5560: Redeemable NFTs"
author: julien
date: "2022-08-30"
category: EIPs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/eip-5560-redeemable-nfts/10589
views: 2846
likes: 6
posts_count: 7
---

# EIP-5560: Redeemable NFTs

Hello everyone,

More and more NFT issuers such as artists, fine art galeries, auction houses, brands and others want to offer a physical object to the holder of a given NFT. As of now, one can’t link a physical object to an NFT.

We’d like to make a standard proposal we’ve been working on. It’s called **Redeemable** and it’s a standardized way to link a physical object to an NFT.

The Redeemable NFT Extension adds a `redeem` function to the ERC-721. It can be implemented when an NFT issuer wants his/her NFT to be redeemed for a physical object.

Link to PR: https://github.com/ethereum/EIPs/pull/5560

We’re eager for your comments!

Thanks in advance.

## Replies

**Amxx** (2022-08-30):

On ethereum mainnet alone, [I was able to find 7.6k instances of functions named redeem](https://sourcegraph.com/search?q=context:global+repo:%5Egithub%5C.com/tintinweb/smart-contract-sanctuary-ethereum%24+file:/mainnet/+count:all+%22function+redeem%28%22&patternType=standard).

Many different signature, many different usages…

If you want to get something standardized you should start by explaining de motivation. What is currently not working ? Explain the previous work is, and what it fails at doing. You should then carefully  describe the interface, and the usage workflow, to show that it actually solves the issues you identified.

---

**julien** (2022-08-31):

Hi [@Amxx](/u/amxx),

Thank you very much for your reply. It’s appreciated!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> On ethereum mainnet alone, I was able to find 7.6k instances of functions named redeem.
>
>
> Many different signature, many different usages…

I agree but it shouldn’t be too ‘restrictive’ though: for instance if we name it `redeemPhysicalObject()`, people could think that’s the only covered use case, whereas it also can be used to redeem anything (including on-chain assets, tickets, …). We wanted to keep it a bit general.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> you should start by explaining de motivation.

Right now if you sell an NFT that’s redeemable for a physical object, you would declare it in the description but there’s no way to verify if the object was already redeemed or not.

Also, a marketplace can verify if the NFT is redeemable or not, and also verify if it was already redeemed or not. After the `redeem()` function is triggered, the marketplace sends the buyer’s physical address to the seller.

---

**dohzya** (2022-09-12):

Hello ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

I was working on a kindred EIP ([Idea: ERC for redeem codes - #2 by dohzya](https://ethereum-magicians.org/t/idea-erc-for-redeem-codes/10438/2)) but it seems like you were too fast (or I was way too slow ![:pensive:](https://ethereum-magicians.org/images/emoji/twitter/pensive.png?v=12)).

My proposal is focused on securing the redeeming part: how to allow your target user to redeem the token while avoiding anyone else to redeem it. I don’t understand how to do that on a EIP-5560 contract.

To make a redeeming secure with a EIP-5560 contract, do I have to pre-assign the token to the right account?

To be honest, I’m trying to understand if we are working on the same thing (if yes I will try to adapt my code to use this EIP) or if we have distinct goals (if so, maybe we both should use a less ambiguous name ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=12))

---

**julien** (2022-09-15):

Hello [@dohzya](/u/dohzya)!

Thank you very much for your reply. ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dohzya/48/5946_2.png) dohzya:

> Hello
>
>
> I was working on a kindred EIP (Idea: ERC for redeem codes - #2 by dohzya) but it seems like you were too fast (or I was way too slow ).
>
>
> My proposal is focused on securing the redeeming part: how to allow your target user to redeem the token while avoiding anyone else to redeem it. I don’t understand how to do that on a EIP-5560 contract.

No worries, I will give some feedback on [your proposal](https://ethereum-magicians.org/t/idea-erc-for-redeem-codes/10438). The targeted use cases seem to be pretty different from each others. You basically want to **send some value to someone that doesn’t have a wallet address**, and we want to **allow an NFT holder to redeem a physical object** (artworks, tickets, …).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dohzya/48/5946_2.png) dohzya:

> To make a redeeming secure with a EIP-5560 contract, do I have to pre-assign the token to the right account?

Our proposal works with ERC-721 only. We don’t need to pre-assign anything because the NFT holder address is already known (already minted).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dohzya/48/5946_2.png) dohzya:

> To be honest, I’m trying to understand if we are working on the same thing (if yes I will try to adapt my code to use this EIP) or if we have distinct goals (if so, maybe we both should use a less ambiguous name )

Two different projects with distinct goals here.

Like [@Amxx](/u/amxx) mentioned before, the naming might be problematic for both of us. ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

I think `redeem()` as a function name is acceptable in our two cases.

We can have a chat if you like! You can contact me via [Discord](https://discord.gg/xw9dCeQ94Y) (preferred), [Element](https://matrix.to/#/@julienbrg:matrix.org), [Twitter](https://twitter.com/julienbrg), [Telegram](https://t.me/julienbrg) or [LinkedIn](https://www.linkedin.com/in/julienberanger/).

---

**dohzya** (2022-09-15):

As you said, our proposals are distinct (a contract could use one, the other, or both), thus I will continue on my own track, with a explicit name ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

Thanks for the reply and for the great chat!

---

**Riccardo** (2023-01-27):

Hi everybody!

I m amazed by your EIP-5560, and looking forward to use the redeem function in our project. Having figured out that  “it also can be used to redeem anything (including on-chain assets, tickets, …)” including ERC-20 Token, I would suggest. " RedeemAsset " as no-conflictive name!


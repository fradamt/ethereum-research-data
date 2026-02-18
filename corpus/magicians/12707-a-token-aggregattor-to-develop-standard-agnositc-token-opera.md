---
source: magicians
topic_id: 12707
title: A token aggregattor to develop standard-agnositc token operations
author: DanielAbalde
date: "2023-01-26"
category: Magicians > Primordial Soup
tags: [token]
url: https://ethereum-magicians.org/t/a-token-aggregattor-to-develop-standard-agnositc-token-operations/12707
views: 454
likes: 0
posts_count: 1
---

# A token aggregattor to develop standard-agnositc token operations

Hi there!

I want to share with you a non-commercial project to receive any feedback. I will make a short introduction here and if you are interested please visit the following link for more information.



      [github.com](https://github.com/DanielAbalde/Token-Client)




  ![image](https://opengraph.githubassets.com/ade89132c883190de3d2f40f75249e09/DanielAbalde/Token-Client)



###



A token aggregattor to develop standard-agnositc token operations in EVM smart contracts.










After several projects that operate with tokens (like a swapper or a marketplace) I decided to focus on generalizing or abstracting the shared functionality between token standards: isOwner, balanceOf, isApproved and transfer (for the moment), which is sufficient for many use cases and complex operators. Instead of calling the standard methods directly, you call the client using the same function name independently of the standard, and the client calls it for you.

This gives many advantages: you separate the decision of what standards to support in your dapp from the implementation itself; it allows you to support or stop supporting any standard token at any time using proxies; you make code more elegant by eliminating redundancy and making algorithms token-agnostic; it is faster to develop and you can focus on the logic of your mechanisms instead of on protocol specifications; among other advantages.

But a fundamental reason for doing this, which I would like to put up for debate, is that I think ERC20 or ERC721 or ERC1155, even if they are supported forever, are not going to be the main token standards in 5 or 10 years. *So it’s a good idea to create dapps with easy token support to future-proof them*. I think the standardisation of Account Abstractions or contract based accounts (with signature capability) will allow much better designs that were not possible before. I imagine that the future of token management will go towards plugins for contract-based accounts, just as there will be plugins that handle permissions, privacy or security policies, intellectual property records, identity records, ownership records, and so on, that any dapp can interact with. So the question is, can such design change (moving from EOA to AA) to keep as main standards for tokens the current EOA-based protocols (ERC20, ERC721 and ERC1155)?

I personally don’t think so and that is why I think it is important to make token agnostic mechanisms as suggested using [TokenClient.sol](https://github.com/DanielAbalde/Token-Client/blob/master/contracts/TokenClient.sol), to transition smoothly to better standards in the future.

What do you think about this vision and about TokenClient?

Thank you!

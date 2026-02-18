---
source: magicians
topic_id: 10374
title: ERC/EIP-5298 ENS Trust to hold Tokens
author: xinbenlv
date: "2022-08-14"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-eip-5298-ens-trust-to-hold-tokens/10374
views: 2259
likes: 1
posts_count: 7
---

# ERC/EIP-5298 ENS Trust to hold Tokens

Please find this proposal:

https://github.com/ethereum/EIPs/pull/5300

## Replies

**Pandapip1** (2022-11-15):

A few thoughts:

- Why not separate functions for EIP-721 and EIP-1155?
- Is EIP-1363 worth supporting?
- Why not remove all references to ENS and support an arbitrary bytes with arbitrary verification?
- Can a function that gets whether a user is authorized or not be added?

---

**xinbenlv** (2022-11-17):

Thank you for the questions, [@Pandapip1](/u/pandapip1)

> Why not separate functions for EIP-721 and EIP-1155?

We are currently working on a general version of reference implementation, hopefully it will support EIP-1155 and EIP-721 plus EIP-20.

> EIP-1363 worth supporting?

I love to be able to support ERC-20. Regarding how to support ERC-20 with safeTransfer type of form, I am debating between EIP-1363 vs EIP-4524 these two competing ERCs based on their adoptability.

> Why not remove all references to ENS and support an arbitrary bytes with arbitrary verification?

Yeah, actually I am thinking of that too, I think ENS specific use case can be a good one to begin with, but we could generalize it to arbitrary bytes with arbitrary verification. Unsure if it should be done within this EIP or a separate EIP. Looking forward to your advice here.

> Can a function that gets whether a user is authorized or not be added?

Yep, was thinking of using [EIP-5982 Role-based Access Control](https://github.com/ethereum/EIPs/pull/5982), but not sure yet. Advice are appreciated!

---

**Pandapip1** (2022-11-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> I love to be able to support ERC-20. Regarding how to support ERC-20 with safeTransfer type of form, I am debating between EIP-1363 vs EIP-4524 these two competing ERCs based on their adoptability.

EIP-1363 is final and is agnostic about contract accounts vs EOAs, whereas  EIP-4524 is not agnostic nor is it final.

---

**xinbenlv** (2022-11-18):

I read 4524 also agnostic of EOA vs Contract account, no?

---

**Pandapip1** (2022-11-20):

Well… EIP-4524 is stagnant. I like the function naming better, but to avoid this:

[![standards](https://ethereum-magicians.org/uploads/default/original/2X/3/32311fc72160e86aa5c5275fda5ee7391e135197.png)standards500×283 22.9 KB](https://ethereum-magicians.org/uploads/default/32311fc72160e86aa5c5275fda5ee7391e135197)

I suggest you use EIP-1363.

---

**xinbenlv** (2022-11-20):

The debate between EIP-1363 vs EIP-4524 worth a separate debate, e.g.

1. ERC721 and ERC1155 has established safeTransferFrom as a naming convention that EIP-1363 is ignoring and create a new name transferAndCall. If the transferAndCall function is being used to only verify the recipient account being a contract account
2. If the transferAndCall function is being used anything other than verifying the recipient account being a contract account, I think there is a lot of limitations of EIP-1363 for example,  the parameter choice and implied technical direction of EIP-1363 has significant restrictions, e.g.

- the value of transfer(to, value, data) assume it can call the to but doesn’t support specifying ether Value which makes it not able to support general case of a remote function call that includes ethers required.
- It also doesn’t support extra data so it couldn’t make a more flexible call
- It doesn’t support a transfer call to specific which method inside of that recipient function to call, and restricting it to only onTransferReceived, renders it much less useful other than just verifying the recipient being an account, and instead introduced a lot of risk of re-entry attack.

In short, I am a bit hesitant to consider EIP-1363 ready to be massively adopted and thus hesitant to consider EIP-5298 to depend on EIP-1363.

I do see there are some value to consider how to support a further call function after claiming. I am not sure if EIP-5298 needs to be opinionated about such call function or could just leave the choice entirely to implementor


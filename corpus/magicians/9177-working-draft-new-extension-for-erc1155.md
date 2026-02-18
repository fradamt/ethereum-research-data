---
source: magicians
topic_id: 9177
title: "[Working draft] New extension for ERC1155"
author: ivanmmurcia
date: "2022-05-06"
category: ERCs
tags: [token, erc1155]
url: https://ethereum-magicians.org/t/working-draft-new-extension-for-erc1155/9177
views: 1184
likes: 6
posts_count: 7
---

# [Working draft] New extension for ERC1155

Hi everyone,

I’m here for propose my idea to Ethereum Magicians community, redirected by a kind user of the Open Zeppelin community. I hope I can explain myself well and also some guidance if my proposal is really liked and can become an official standard.

I have been developing 2 extensions for ERC1155 as a personal purpose, but after discussing it with several developers I have been proposed to present it as an official extension.

I saw that the ERC1155 standard does not have the possibility to approve tokens by id or amounts as for example in ERC20. So, to create more security to my clients, I have designed the following code to avoid my smart contract to be approved for all ids, later I thought to develop the same but with amounts.

Code and explanations are here: [GitHub - ivanmmurciaua/EIP-5216: Official repository of EIP-5216: How to do a safe approval for individual amounts by id for ERC-1155 standard](https://github.com/ivanmmurciaua/ERC1155ApprovalByAmount)

It would be a pleasure to humbly contribute to this great community of developers.

Feel free to answer me and discuss with me.

Greetings from Spain,

Iván M.M.

## Replies

**dadabit** (2022-05-08):

I think approving a specific amount for a specific id would be good and consistent with the erc20 usage patterns. I second this proposal

---

**ivanmmurcia** (2022-05-09):

Hi [@dadabit](/u/dadabit) . Thanks for the feedback and support. Hope other users second my proposal like you. Best regards.

---

**dievardump** (2022-05-12):

Hey there. It’s not a bad idea when we see ERC1155 as a collection of fungibles.

#### ERC1155ApprovalById:

I think the ApprovalById is redundant, you can simply approve amount to MAX_INT.

 → I would totally remove ERC1155ApprovalById

#### ERC1155ApprovalByAmount

Also I don’t think `safe(/Batch)TransferFromByAmount` are necessary.

`safe(Batch)TransferFrom` are already enough, you simply have to override them so they check for ApprovalForAll OR allowance.

This also makes your extensions smaller, which increases the likeliness to appeal to people.

Big extensions are bloating code that is already big enough.

In term of API, I would also try to keep it more consistent:

- if you use “setAllowance()” then use “getAllowance()”
- personally, I would prefer it more consistent with the erc20 api (approve(spender, tokenId, amount) & allowance(owner, spender, tokenId)) but that’s just a preference.

---

**ivanmmurcia** (2022-05-13):

Hey [@dievardump](/u/dievardump). Thanks for reply and feedback mate.

I’d like to go point by point:

**ERC1155ApprovalById:**

Only for have it this version, I created a branch which is unimplemented in main

**ERC1155ApprovalByAmount:**

I fit terms of my API to ERC-20 like you said: Now the names are 100% like ERC-20, `approve`, `allowance` and mapping `_allowances`.

**But** I have one question regarding what you said about `safe(Batch)TransferFrom`. I understood that if someone wants to use the ByAmount extension, they would have to override the original ERC1155 `safeTransferFrom` function. Is this correct?

If changes only the condition, I would understand it, but it should be noted that the line where the amount transferred is substracted of the operator allowance… wouldn’t it be a bit dangerous to leave that to the free code of a programmer who doesn’t know the extension?

I don’t quite understand/see how to implement this functionality without my extension becoming heavy and repetitive.

Thanks for all, look forward to your answer.

---

**dievardump** (2022-05-26):

> wouldn’t it be a bit dangerous to leave that to the free code of a programmer who doesn’t know the extension?

Any implementations of ERCs is let to the implementer. ERC and their extensions are only supposed to provide the interface.

The idea would be to then create a reference implementation (like OpenZeppelin) of your extension (this implementation would be the one overriding the `safe(Batch)TransferFrom`) that other users would use directly.

Very few developer have the wish (or even can) implement a standard. They want the code to come to them already made.

Your extension would extend ERC1155, add the 2 functions allowance()/approve() and override safe(Batch)TransferFrom() to verify if operator is approvedForAll (the normal process) OR has enough allowance.

And if operator is not approvedForAll, you reduce their allowance on the given token.

There shouldn’t be a need for verbose `safe(Batch)TransferFromByAmount`, safeTransferFrom should be enough.

---

**ivanmmurcia** (2022-05-26):

> The idea would be to then create a reference implementation (like OpenZeppelin) of your extension

Thanks for the explanation [@dievardump](/u/dievardump). I’ve implemented a reference implementation in `./contracts/ReferenceImplementation.sol`. I override `safe(Batch)TransferFrom` from ERC1155 and deleted `safe(Batch)TransferFromByAmount` from extension. Great advice.

Do you think it’s better override it in a reference implementation or would be better override it in extension? I think that override it in extension would be worse.


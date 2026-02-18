---
source: magicians
topic_id: 15020
title: "ERC-7303: Token-Controlled Token Circulation"
author: kofujimura
date: "2023-07-10"
category: ERCs
tags: [erc, token]
url: https://ethereum-magicians.org/t/erc-7303-token-controlled-token-circulation/15020
views: 1968
likes: 4
posts_count: 11
---

# ERC-7303: Token-Controlled Token Circulation

Discussion thread for ERC-7303.

This ERC introduces an access control scheme termed Token-Controlled Token Circulation (TCTC). By representing the privileges associated with a role as an ERC-721 or ERC-1155 token (referred to as a control token), the processes of granting or revoking a role can be facilitated through the minting or burning of the corresponding control token.

After draft PR merged: [ERC-7303: Token-Controlled Token Circulation](https://eips.ethereum.org/EIPS/eip-7303)

Original PR: [Add EIP: Token-Controlled Token Circulation by kofujimura · Pull Request #7303 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7303)

For additional documentation on the use cases of the TCTC, see [here](https://github.com/kofujimura/TCTC#readme).

## Replies

**radek** (2023-07-15):

Interesting. Access rights represented as NFTs can have some social / statutory / marketing vibe.

However - NFTs are user transferable by design. I doubt that it fits for the access management. Soulbound tokens could be used instead - e.g. using ERC 5192 or 5727.

Regarding reference implementation, it is better to avoid arrays + for loops.

---

**kofujimura** (2023-07-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> However - NFTs are user transferable by design. I doubt that it fits for the access management. Soulbound tokens could be used instead - e.g. using ERC 5192 or 5727.

Thank you for your valuable feedback.

ERC-5192 is ERC-721, so it’s not explicitly stated in the current draft of ERC-7303 (TCTC), but it is possible to use ERC-5192’s Soulbound as a control token. In fact, I believe that ERC-5192 is desirable in many use cases. However, if ERC-5192 is REQUIRED, transferable tokens can no longer be used for access control. Depending on the application, there may be cases where you want to implement permissions as tokens and temporarily allow them to be transferred to others. For these reasons, I decided to REQUIRE ERC-721 instead of ERC-5192. I think that the issuer of the target token should choose ERC-5192 or ERC-721 as the control token at their discretion.

On the other hand, since ERC-5727 does not inherit ERC-721, it does not provide balanceOf(), but instead manages the amount per slot. Therefore, ingenuity is required to use it as a control token. If many needs are anticipated, it may be possible to use ERC-5727’s verify() instead of balanceOf(). It may be difficult to incorporate it into TCTC as a generic implementation, so I gave up in this draft. However, if there are many requests, I would like to make ERC-5727 one of the control tokens that TCTC can use.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> Regarding reference implementation, it is better to avoid arrays + for loops.

In real-world business transactions, there are many use cases where you want to grant permissions when you own any of multiple control tokens. Therefore, in TCTC, we made it possible to call _grantRoleByToken() multiple times. Is it better to avoid this? I would appreciate more explanation.

---

**radek** (2023-07-16):

ERC5192 and 5727 were given just as an example, ERC 4671 could have been better one.

> transferable tokens can no longer be used for access control

Indeed, transferability should be the primary conceptual discussion.

You mentioned `This ERC introduces an access control scheme` , for such schemes it is common some authority grants / revokes the access rights.

Can you please identify the case where transferability of the access rights without authority’s approval is desired?

> arrays + for loops
> In real-world business transactions, there are many use cases where you want to grant permissions when you own any of multiple control tokens.

Can I assume the concept of 1 NFT = 1 (access) right?

---

**kofujimura** (2023-07-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> ERC5192 and 5727 were given just as an example, ERC 4671 could have been better one.

While I think ERC-4671 is a good specification, currently the mainstream implementation of SBT is ERC-5192. As TCTC, I thought it would be sufficient to cover SBTs that inherit ERC-721. If there is a majority opinion that ERC-4671 should also be usable as a control token for TCTC, I would like to modify the specification.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> Can you please identify the case where transferability of the access rights without authority’s approval is desired?

For instance, consider a franchised shop. Suppose the franchisor issues the right to distribute coupons to the franchisee as a Minter Cert token. What about cases where the store manager of the franchisee temporarily delegates the right to issue coupons to a deputy manager due to illness or travel? In this case, if it’s non-transferable, they would have to request the franchisor to issue or invalidate the Minter Cert every time they go on a trip or fall ill. This would be very inconvenient.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> Can I assume the concept of 1 NFT = 1 (access) right?

It depends on the application, so it can’t be generally assumed. Of course, in certain applications, it’s possible to deploy a new control token for each role. However, there are also scenarios you could imagine, such as various applications designating an individual authentication token issued by a government agency as the necessary control token for the recipient of the target token.

---

**kofujimura** (2023-07-22):

Based on our discussion about using transferable tokens as control tokens, I’ve added  [Rationale part](https://github.com/ethereum/EIPs/blob/cd36e25ce977d202b13e21b434406b5a66e2b63f/EIPS/eip-7303.md#rationale) to the draft.

---

**timlrx** (2023-07-24):

Nice idea. Have you considered integrating [ERC-5982: Role-based Access Control](https://eips.ethereum.org/EIPS/eip-5982) so the events and roles can be checked in the same way as contracts which implements non-token access control?

---

**kofujimura** (2023-07-24):

Thank you for your feedback. I believe the point you raised is precisely where the rationale of the ERC was lacking in explanation.

The most significant feature of TCTC is that the contract defining the control token can be deployed separately from the contract of the target token being controlled. Therefore, in order to implement grantRole() or revokeRole() within the contract of the target token, it’s necessary to mint or burn the control token. For this purpose, it’s required to grant the mint/burn privilege of the control token to the contract of the target token. However, in many cases, the control token is deployed first, which makes it extremely complicated and impractical to achieve this.

On the other hand, hasRole() can be easily implemented using the _checkHasToken() provided by ERC7303.sol. While I think it wouldn’t be beneficial to provide only hasRole() without being able to offer grantRole() and revokeRole(), what do you think?

---

**kofujimura** (2023-08-07):

[@xinbenlv](/u/xinbenlv) Thank you for your comment. Indeed, the previous version could not be said to support ERC-1155. In the new version, I have made changes to allow the use of ERC-1155 tokens in addition to ERC-721 as control tokens, and I have adjusted the reference implementation accordingly. For ERC-1155 tokens, a typeId is required as a parameter for balanceOf, so I made the function _grantRoleByToken() separate from that of ERC-721.

---

**timlrx** (2023-08-08):

Thanks for your explanation and outlining the challenges.

Correct me if I am wrong, but currently to grant a role, you would have to mint a control token and execute _grantRoleByERC721(). However to revoke a role, you would have to burn the control token. The makes it difficult to track the control tokens which have roles - you would have to check for all tokens that you have granted a role previously whether they still exist.

How about an alternative where granting and revoking the roles require a call from the contract itself? The control tokens can still be deployed separately, but are not tied to mint / burn. And you could revoke role without burning the token.

---

**kofujimura** (2023-08-08):

Managing privileges and token ownership separately can increase flexibility in some cases, but I generally think that it only complicates management.

For example, if you decide to grant a store manager the privilege of minting coupon tokens, under the TCTC schema, you would issue a token that proves the manager’s position, and grant the privilege of minting coupons to that token. In other words, it’s a privilege given to a position holder. If the position token becomes invalidated due to the manager’s resignation, you can automatically remove the privilege of minting coupons. It’s very simple.

On the other hand, if the minting/burning of position tokens is not directly associated, you need to revoke the privileges related to the store manager’s position one by one. If a single position has multiple privileges, management becomes complicated.

There are many use cases where it becomes simpler to directly issue privileges as a token and specify that token for the transaction’s execution privilege.

A control token is typically something like the position token in the above example, and whether or not a specific address holds a position can be easily verified by simply querying the blockchain. Indeed, it might be cumbersome if many control tokens are associated with one role, but in the use cases I envision, most are of one type, and at most two or three types.


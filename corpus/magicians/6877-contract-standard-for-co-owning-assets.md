---
source: magicians
topic_id: 6877
title: Contract Standard for co-owning assets
author: blockchain_addict
date: "2021-08-16"
category: EIPs
tags: [multisigs]
url: https://ethereum-magicians.org/t/contract-standard-for-co-owning-assets/6877
views: 1068
likes: 2
posts_count: 4
---

# Contract Standard for co-owning assets

As part of one of my side projects, I have a use case where assets (like ERC20, ERC721, ETH etc) have to be co-owned by multiple people. This involves a group of people managing the assets together in a democratic way. I have created a high level contract standard for these kind of scenarios. But before that wanted to check if there is any existing standard for the same and also wanted to get your opinion whether such a generic standard will be useful for the community?

Waiting for thoughts and suggestions.

[![ERC-XX _ A Contract Standard for co-owning assets (Page 1)](https://ethereum-magicians.org/uploads/default/optimized/2X/2/293efed2809ab416e59d0d8e622236b524cda402_2_386x500.jpeg)ERC-XX _ A Contract Standard for co-owning assets (Page 1)1583×2048 219 KB](https://ethereum-magicians.org/uploads/default/293efed2809ab416e59d0d8e622236b524cda402)

[![ERC-XX _ A Contract Standard for co-owning assets (Page 2)](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a2074043543d9ee4bfa5bde758a9093c63c80882_2_386x500.jpeg)ERC-XX _ A Contract Standard for co-owning assets (Page 2)1583×2048 185 KB](https://ethereum-magicians.org/uploads/default/a2074043543d9ee4bfa5bde758a9093c63c80882)

[![ERC-XX _ A Contract Standard for co-owning assets (Page 3)](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b4643d0437ded5a29d9544ce1205b1b43c4bfbb3_2_386x500.jpeg)ERC-XX _ A Contract Standard for co-owning assets (Page 3)1583×2048 216 KB](https://ethereum-magicians.org/uploads/default/b4643d0437ded5a29d9544ce1205b1b43c4bfbb3)

[![ERC-XX _ A Contract Standard for co-owning assets (Page 4)](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b1e0ae61b474ced9d610c9fb6f21ec4b073ef0a0_2_386x500.jpeg)ERC-XX _ A Contract Standard for co-owning assets (Page 4)1583×2048 260 KB](https://ethereum-magicians.org/uploads/default/b1e0ae61b474ced9d610c9fb6f21ec4b073ef0a0)

[![ERC-XX _ A Contract Standard for co-owning assets (Page 5)](https://ethereum-magicians.org/uploads/default/optimized/2X/6/616ff988521f2b40b20ae217475474e0c0819508_2_386x500.jpeg)ERC-XX _ A Contract Standard for co-owning assets (Page 5)1583×2048 241 KB](https://ethereum-magicians.org/uploads/default/616ff988521f2b40b20ae217475474e0c0819508)

[![ERC-XX _ A Contract Standard for co-owning assets (Page 6)](https://ethereum-magicians.org/uploads/default/optimized/2X/d/d7847328fe60ccabb2918df5958eab7a92710bb9_2_386x500.jpeg)ERC-XX _ A Contract Standard for co-owning assets (Page 6)1583×2048 209 KB](https://ethereum-magicians.org/uploads/default/d7847328fe60ccabb2918df5958eab7a92710bb9)

## Replies

**blockchain_addict** (2021-08-18):

With this standard, a group of people can easily manage a contract in a secure manner. Eg : if the contract managed by 3 people gets 3 ETH and if they want to distribute it, they can create/approve following action which consists of 3 sub actions

Action :

transfer(address1, total/3)

transfer(address2, total/3)

transfer(address3, total/3)

And the action can be approved/executed in an atomic way after the approval of all the members.

This also can be used for managing other assets like ERC-20, ERC-721, ERC-1155 etc

---

**blockchain_addict** (2021-08-21):

As an extension, we also can have a democratic and secure way to fund the multi party contract.

This is needed when the contract need to buy/possess assets by transferring funds. The funding by multiple people is challenging as today most of it is done based only on trust. The following proposal addresses it in an elegant manner

Proposal

Have an Escrow contract (which is deployed by the multi party contract) to which users can transfer funds.

Once transferred only the user/multi party contract can withdraw funds from the escrow contract

Have a method to withdraw funds in the multi party contract. Then create a funding action like below to fund the contract

Action :

withdraw(address1, 1)

withdraw(address2, 1)

Before this step, the users have to fund the escrow. Once the action is executed the multi party contract gets funded by the escrow in a secure manner

---

**blockchain_addict** (2021-08-23):

Have created PR for the same : [[EIP-3742] - Standard for multi party contract by saurabhsanthosh · Pull Request #3742 · ethereum/EIPs · GitHub</ti](https://github.com/ethereum/EIPs/pull/3742)

it would be great if someone can just take a look. Thanks ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)


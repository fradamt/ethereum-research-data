---
source: magicians
topic_id: 4244
title: Non fungible property standard
author: kohshiba
date: "2020-05-01"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/non-fungible-property-standard/4244
views: 774
likes: 3
posts_count: 5
---

# Non fungible property standard

Hello magicians!

I’d like to introduce the recently proposed Non fungible property standard.

TLTR: This standard added some extensive user classes like tenancy or lien in addition to ownership of the ERC721 standard. These features make rental or collateral without escrow possible.

Here is the link to details.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/2616)












####



        opened 02:00PM - 25 Apr 20 UTC



          closed 09:04AM - 01 Jun 22 UTC



        [![](https://avatars.githubusercontent.com/u/4516944?v=4)
          0xbuild3r](https://github.com/0xbuild3r)





          stale







This is a discussion purpose issue for an ERC proposal.
https://github.com/ethe[…]()reum/EIPs/pull/2615
Implementation and detail are here.
https://github.com/kohshiba/ERC-X












I’d love to hear your feedback.

If you like to implement this standard to your project and have some personal questions, DM me https://twitter.com/KOHSHIBA

## Replies

**Alchemist33** (2020-05-08):

What does that mean in practice? Without escrow meaning ‘without 3 party custodian’?

---

**kohshiba** (2020-05-08):

I mean escrow as assign another address on ownerOf() in ERC721.

Since many application refer the address assigned in ownerOf() as the owner, escrow to contract hurt the utility of the token in the design of ERC721.

This EIP is designed to eliminate this problem by providing three user class as default.

---

**Alchemist33** (2020-05-08):

Ok. So, It’s like system some of vaults used with user/controller/client all having some level of access and interaction with tokens?

---

**kohshiba** (2020-05-09):

Yes. The standard has 3 user classes.

> Lien.
> This is a user class that is active only when it is set. Lien enables transfer of owner and user It is supposed to be set when the owner collateralizes the property.

> Owner
> The owner can transfer the owner right and the user right.

> User
> The user can transfer the user right. Applications using this standard is expected to provide a service to this user class.  Tenant right is set when it is rented out and it suspends the owner’s authority to transfer the property.


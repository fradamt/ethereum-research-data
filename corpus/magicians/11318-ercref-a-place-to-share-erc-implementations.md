---
source: magicians
topic_id: 11318
title: ERCRef, a place to share ERC implementations
author: xinbenlv
date: "2022-10-14"
category: EIPs
tags: [erc, erfref]
url: https://ethereum-magicians.org/t/ercref-a-place-to-share-erc-implementations/11318
views: 887
likes: 5
posts_count: 4
---

# ERCRef, a place to share ERC implementations

Hi FEM, and friends who author, implement or uses #ERC #EIP standards or write smart contracts, I love to invite you to this new effort I am initiating called #ERCRef to improve interoperability and composibility of #Ethereum application layer repo: [GitHub - ercref/contracts: ERC Reference Implementations](https://github.com/ercref/contracts)

discord:

The goal is to have a repo where people can submit, share, discuss, peer-review various ways to implement an ERC, or different use cases.

The `contracts` repo ([GitHub - ercref/contracts: ERC Reference Implementations](https://github.com/ercref/contracts)) hope to be the go-to place where ERC authors and contributors could provide their reference implementations or submit new implementation ideas, and make it useable and shareable. Hope to massively improve ERC authoring expericience and early adoptions.

Authors and contributors of each new ERC may choose to share a few RefImpls in that repo.

In the near future, we also hope to have a subset inside of that repo to be packaged as NPM packages and maybe ETHPM. Imagine the same as one could import `@openzeppelin/contracts`, early ERC adoptors / developers and researchers may simply import something like `@ercref/erc2135-draft/TicketImplV1.sol`. Making it super easy to share and tryout new ERCs. (warning do not use in prod yet unless audited)

Ask asked by @mattstam, one may think, the biggest challenge will probably be convincing majority of EIP owners to add their implementation(s) here. How do we plan do do that?

My answer to that is; ERC authors *doesnt have to* put their refimpl here. They could but it’s not a requirement.

Also the refimpl doesnt have to come from authors of ERC.

As an open source project, anyone could help provide a reference implementations of any ERCs into ERCRef repo.

If ERC authors want to get involved, they could help review the proposed refimpl of the ERC they proposed. If some ERC authors don’t want to involve, we could still accept refimpl from anyone by having a peer-review approach. We (ERCref) could have a peer-review kind fo approach to those refimpls proposed by non-authors when authors didn’t want to be involve.

At the end of day, ERCs are definition of interfaces and behaviors. By definition they are meant to be implemented any different people differently. They are meanted to be adopted. Hence regardless of whether an ERC author of a particular ERC puts their own refimpl somewhere, they still expect there is *more* implementations of the ERC they propose, so I think they will also happily see people implementing their ERCs

## Replies

**Pandapip1** (2022-10-14):

Love the idea. I’d be willing to help with some initial interfaces for common EIPs.

I’ll say that these can’t be used as actual reference implementations without some changes to the ways EIPs work. These can absolutely mirror the ref impls though.

---

**xinbenlv** (2022-10-15):

Awesome, thank you [@Pandapip1](/u/pandapip1) looking forward to your master piece of work

---

**xinbenlv** (2023-04-19):

Sharing a new smart contract ERC20WithFee on [ercref-contracts/ERCs/eip-20/fee at main · ercref/ercref-contracts · GitHub](https://github.com/ercref/ercref-contracts/tree/main/ERCs/eip-20/fee).

Feedback are welcomed!


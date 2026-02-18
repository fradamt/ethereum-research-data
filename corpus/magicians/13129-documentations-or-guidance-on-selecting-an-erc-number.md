---
source: magicians
topic_id: 13129
title: Documentations or guidance on selecting an ERC number
author: jsonsivar
date: "2023-03-02"
category: Magicians > Process Improvement
tags: [erc]
url: https://ethereum-magicians.org/t/documentations-or-guidance-on-selecting-an-erc-number/13129
views: 668
likes: 2
posts_count: 5
---

# Documentations or guidance on selecting an ERC number

Hello, just posting on behalf of the [NFA team](https://github.com/fleekxyz/non-fungible-apps). We were wondering if there is more documentation or guidance on picking the ERC number.  We read [EIP-1](https://eips.ethereum.org/EIPS/eip-1) and it says it’s picked by us but wanted to see if there is specific rules we should follow on the number.

## Replies

**abcoathup** (2023-03-03):

EIP/ERC editors assign the EIP/ERC number.  Generally it is the (first) PR number.

Number gaming (e.g. creating issues/PRs to increase the number) will likely result in a different number being assigned.

---

From: [EIP-1](https://eips.ethereum.org/EIPS/eip-1):

> Once the EIP is ready for the repository, the EIP editor will:
>
>
> Assign an EIP number (generally the PR number, but the decision is with the editors)

---

**stoicdev0** (2023-03-03):

I wish this was cleaner. We’re on 6 thousand something now and there are actually less than 600 EIPs. From my team we’ve proposed 5 EIPs and it would be much easier to remember (and maybe even consecutive) if they weren’t 4 digits each.

It’s small annoyance, but annoyance nevertheless.

---

**abcoathup** (2023-03-03):

There have been discussions previously of [selling unused EIP numbers](https://github.com/ethereum/EIPs/issues/5082).

In my opinion, only a few EIP/ERC #s have strong name recognition: ERC20, ERC721, EIP1559, EIP4844, some of which are 4 digit #s.

---

**poojaranjan** (2023-04-05):

Every proposal needs a number but not all of them reach `Final` status.

We use a common repo to promote EIPs and this has to be done via Pull Request.

Allocating a different number to an EIP after getting merged to maintain the consecutive order is a bit complicated if looked at for maintenance purposes.

I suppose it’s a process decision made at the time which turned out to be working well so far.


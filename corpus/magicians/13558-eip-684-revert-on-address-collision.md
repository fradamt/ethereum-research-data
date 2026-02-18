---
source: magicians
topic_id: 13558
title: EIP-684 Revert on address collision
author: RenanSouza2
date: "2023-03-27"
category: EIPs > EIPs core
tags: [create2, create]
url: https://ethereum-magicians.org/t/eip-684-revert-on-address-collision/13558
views: 634
likes: 0
posts_count: 5
---

# EIP-684 Revert on address collision

This post refers to the PR [Add EIP: Prevent overwriting contracts by RenanSouza2 · Pull Request #6784 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6784)

edit: The eip 6784 was closed,

The valid PR is [Add EIP: Revert creation in case of collision by RenanSouza2 · Pull Request #6733 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6733)

Second edit: this is no longer the post for the PR, it stays the original [EIP-6733 revert contract creation on address collision](https://ethereum-magicians.org/t/eip-6733-revert-contract-creation-on-address-collision/13442)

## Replies

**RenanSouza2** (2023-03-27):

A few days ago I made a proposal EIP-6733, which is the same as EIP-684 that was not doccumented as a markdown file, this fixes it

---

**RenanSouza2** (2023-03-27):

Another problem, this EIP is not mentioned in the yellowpaper, how is the management of that document?

---

**chfast** (2023-03-27):

Let’s just add EIP-684 without coming up with a new number.

---

**RenanSouza2** (2023-03-27):

Yes, their final decision was the same



      [github.com](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-684.md)





####



```md
---
eip: 684
title: Revert creation in case of collision
description: Revert contract creation if address already has code
author: Vitalik Buterin (@vbuterin), Renan Rodrigues de Souza (@RenanSouza2)
discussions-to: https://ethereum-magicians.org/t/eip-revert-on-address-collision/13442
status: Final
type: Standards Track
category: Core
created: 2023-03-20
---

## Abstract

This EIP causes contract creation to throw an error when attemted at an address with pre-existing code. This prevents an attack consisting of deploying contract code and later changing the code arbitrarily by "creating" an account at that existing address.

## Specification

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119 and RFC 8174.

```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-684.md)


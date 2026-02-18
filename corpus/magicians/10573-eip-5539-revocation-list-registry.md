---
source: magicians
topic_id: 10573
title: "EIP-5539: Revocation List Registry"
author: DennisVonDerBey
date: "2022-08-29"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5539-revocation-list-registry/10573
views: 1872
likes: 3
posts_count: 4
---

# EIP-5539: Revocation List Registry

This is the discussion thread for [EIP-5539](https://github.com/ethereum/EIPs/pull/5539) (currently in draft):

Revocation is a universally needed construct both in the traditional centralized and decentralized credential attestation. This EIP aims to provide an interface to standardize a decentralized approach to managing and resolving revocation states in a contract registry.

The largest problem with traditional revocation lists is the centralized aspect of them. Most of the world’s CRLs rely on HTTP servers as well as caching and are therefore vulnerable to known attack vectors in the traditional web space. This aspect severely weakens the underlying strong asymmetric key architecture in current PKI systems.

In addition, issuers in existing CRL approaches are required to host an own instance of their public revocation list, as shared or centralized instances run the risk of misusage by the controlling entity.

This incentivizes issuers to shift this responsibility to a third party, imposing the risk of even more centralization of the ecosystem (see Cloudflare, AWS).

Ideally, issuers should be able to focus on their area of expertise, including ownership of their revocable material, instead of worrying about infrastructure.

We see value in a future of the Internet where anyone can be an issuer of verifiable information. This proposal lays the groundwork for anyone to also own the lifecycle of this information to build trust in ecosystems.

## Replies

**strumswell** (2022-08-29):

It was great working with you and [@lleifermann](/u/lleifermann) on this one!

---

**MajdT51** (2022-09-20):

Is there any reference implementation of the contract?

---

**DennisVonDerBey** (2022-09-20):

We’re currently working on it, but it’s mostly done. Please keep in mind that this repository contains more features than the EIP describes (upgradeable proxy contract for example). We will try to do a simplified version as a reference implementation some time.

Contract repository:

https://github.com/spherity/ethr-revocation-registry

Controller dependency to interact via Javascript:

https://github.com/spherity/ethr-revocation-registry-controller


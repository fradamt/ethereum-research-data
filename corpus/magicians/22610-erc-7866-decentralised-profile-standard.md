---
source: magicians
topic_id: 22610
title: "ERC-7866: Decentralised Profile Standard"
author: anistark
date: "2025-01-21"
category: ERCs
tags: [privacy, sbt, interop, did]
url: https://ethereum-magicians.org/t/erc-7866-decentralised-profile-standard/22610
views: 149
likes: 2
posts_count: 3
---

# ERC-7866: Decentralised Profile Standard

The Decentralised Profile EIP proposes a decentralised, interoperable, and chain-agnostic standard for user profiles, built on top of Soulbound Tokens (SBTs). Each user profile is uniquely identified by a Decentralised Identifier (DID) in the format `did:<chain>:<address>` and linked to a unique Profile in the format `username@networkslug.soul`. It is inspired by current web3 ENS format and web2 email addresses that we use today.

The standard enables users to manage and customise their profiles across multiple chains while providing granular access control for metadata and avatars. Profiles support assigning specific avatars to decentralised applications (dApps) or using a default avatar, with visibility settings (`public` or `private`) for enhanced privacy. This allows the further control over one’s profile data and can be customised according to need.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/861)














####


      `ethereum:master` ← `anistark:master`




          opened 10:23PM - 21 Jan 25 UTC



          [![anistark](https://avatars.githubusercontent.com/u/5357586?v=4)
            anistark](https://github.com/anistark)



          [+346
            -0](https://github.com/ethereum/ERCs/pull/861/files)







The CyberSoul Profile EIP proposes a decentralised, interoperable, and chain-agn[…](https://github.com/ethereum/ERCs/pull/861)ostic standard for user profiles, built on top of Soulbound Tokens (SBTs). Each user profile is uniquely identified by a Decentralised Identifier (DID) in the format `did:<chain>:<address>` and linked to a unique CyberSoul Profile (CSP) in the format `username@networkslug.soul`. It is inspired by current web3 ENS format and web2 email addresses that we use today.

The standard enables users to manage and customise their profiles across multiple chains while providing granular access control for metadata and avatars. Profiles support assigning specific avatars to decentralised applications (dApps) or using a default avatar, with visibility settings (`public` or `private`) for enhanced privacy. This allows the further control over one's profile data and can be customised according to need.

## Replies

**anistark** (2025-02-26):

Created a sample hardhat project to showcase the implementation: [GitHub - anistark/cybersoul-hardhat](https://github.com/anistark/cybersoul-hardhat)

---

**anistark** (2026-01-07):

Now moved to Review stage


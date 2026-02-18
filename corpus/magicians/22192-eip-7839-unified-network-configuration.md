---
source: magicians
topic_id: 22192
title: "EIP-7839: Unified Network Configuration"
author: bbusa
date: "2024-12-13"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7839-unified-network-configuration/22192
views: 38
likes: 1
posts_count: 1
---

# EIP-7839: Unified Network Configuration

This EIP proposes a protocol for the Execution Layer (EL) to fetch its configuration parameters from the Consensus Layer (CL) at startup. This eliminates duplicate configuration and ensures consistency between layers by making the CL the source of truth for network parameters.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9128)














####


      `master` ← `barnabasbusa:bbusa/el-config-from-cl`




          opened 02:53PM - 12 Dec 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/9/91865ea61a7d554f736d38ab49e83daed81e6494.png)
            barnabasbusa](https://github.com/barnabasbusa)



          [+132
            -0](https://github.com/ethereum/EIPs/pull/9128/files)







**ATTENTION: ERC-RELATED PULL REQUESTS NOW OCCUR IN [ETHEREUM/ERCS](https://gith[…](https://github.com/ethereum/EIPs/pull/9128)ub.com/ethereum/ercs)**

--

When opening a pull request to submit a new EIP, please use the suggested template: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

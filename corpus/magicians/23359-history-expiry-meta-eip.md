---
source: magicians
topic_id: 23359
title: History Expiry Meta EIP
author: pipermerriam
date: "2025-04-02"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/history-expiry-meta-eip/23359
views: 162
likes: 0
posts_count: 2
---

# History Expiry Meta EIP

This topic is to discuss the History Expiry Meta EIP



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9572)














####


      `master` ← `pipermerriam:piper/add-history-expiry-meta-EIP`




          opened 05:35PM - 31 Mar 25 UTC



          [![](https://avatars.githubusercontent.com/u/824194?v=4)
            pipermerriam](https://github.com/pipermerriam)



          [+117
            -0](https://github.com/ethereum/EIPs/pull/9572/files)







This is a work in-progress of the Meta-EIP for history expiry.  I'm still active[…](https://github.com/ethereum/EIPs/pull/9572)ly working on it.

## Replies

**sinamahmoodi** (2025-04-24):

Update from geth. The latest release includes the ability to a) offline-prune an existing datadir up to the merge block via `prune-history` command, b) snap sync without fetching the premerge block bodies and receipts. In both cases you will need to pass the `--history.chain postmege` flag to indicate a pruned history.

These are not advertised lest users get the idea to try it on mainnet before Pectra which we’d like to avoid. We have partial integration of era files with more coming in this direction.


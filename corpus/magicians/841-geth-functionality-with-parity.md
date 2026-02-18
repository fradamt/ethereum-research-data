---
source: magicians
topic_id: 841
title: Geth functionality with parity
author: smak
date: "2018-07-22"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/geth-functionality-with-parity/841
views: 720
likes: 1
posts_count: 3
---

# Geth functionality with parity

Has anyone tried to use geth console attached to parity wallet lately?

commands like eth.syncing and retrieving balances seem fine but errors result from attempting to send any transactions for me.

considering the bulk of parity-ui i think its worthwhile to maintain geth compatibility for anyone mindful enough to keep a contingency of wallets at their disposal at any given time.

## Replies

**mmhh1910** (2018-07-22):

Just a shot in the dark: Are you aware of the --geth parameter to parity?

---

**smak** (2018-07-23):

interesting so parity has to be initialized with – geth atribute and geth attch with ~/.local/share/io.parity.ethereum/jsonrpc.ipc ? I will give it a shot.


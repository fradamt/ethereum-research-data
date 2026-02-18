---
source: magicians
topic_id: 14982
title: Geth, Cliff and Windows are not friends with each other
author: OneOneExe
date: "2023-07-07"
category: Magicians > Tooling
tags: [windows, clef, geth]
url: https://ethereum-magicians.org/t/geth-cliff-and-windows-are-not-friends-with-each-other/14982
views: 543
likes: 0
posts_count: 1
---

# Geth, Cliff and Windows are not friends with each other

Hi all. I wrote about this problem on GitHub, Discord, StackExchange but no answer. Might help here.

OS: Windows 11

Setting interaction between Clef and Ceth via Named Pipes

In accordance with the instructions from [Getting started with Geth | go-ethereum](https://geth.ethereum.org/docs/getting-started)

enter commands sequentially:

1. In cmd:
clef --keystore geth-tutorial/keystore --configdir geth-tutorial/clef --chainid 11155111
2. In a separate cmd:
geth --sepolia --datadir geth-tutorial --authrpc.addr localhost --authrpc.port 8551 --authrpc.vhosts localhost --authrpc.jwtsecret geth-tutorial/jwtsecret --http --http.api eth,net --signer=geth-tutorial/clef/clef.ipc --http

Finally Geth reports:

Fatal: Failed to set account manager backends: error connecting to external signer: Invalid pipe address ‘geth-tutorial/clef/clef.ipc’.

What am I doing wrong?

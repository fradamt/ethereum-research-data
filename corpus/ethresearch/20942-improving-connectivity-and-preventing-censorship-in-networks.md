---
source: ethresearch
topic_id: 20942
title: Improving connectivity and preventing censorship in networks
author: Uptrenda
date: "2024-11-07"
category: Networking
tags: [p2p]
url: https://ethresear.ch/t/improving-connectivity-and-preventing-censorship-in-networks/20942
views: 133
likes: 0
posts_count: 1
---

# Improving connectivity and preventing censorship in networks

![demo_small (1)](https://ethresear.ch/uploads/default/original/3X/c/0/c0a496d5821b840a46b956450fbab0271213cb35.gif)

Imagine if you could easily run a blockchain node and anyone could connect. Whether on a phone, desktop, or even locked-down IoT connection. Imagine that there was no way to filter such connections. Imagine peer-to-peer apps like chat programs that worked effortlessly. Where connections always succeeded.

You can’t do this today because of NATs and firewalls used in the networks most people have at home. But this is an important part of decentralization. If you can improve connectivity in general you can also help bypass censorship. And improved connectivity isn’t just useful for censorship edge-cases. It solves a practical problem experienced by many programs..

# What options are there to do this already?

Well, the design favored today by ‘P2P libraries’ like Libp2p is to use a ‘decentralized’ network of relays. The logic behind this is easy to understand. There are many different types of NATs with sub-types of external mapping allocation behaviors. An effective algorithm for punching holes through NATs has to be designed to take into account both sides – which some may consider an unnecessary complexity. But this approach isn’t compatible with the scenarios in the introduction.

**If you have to consume relay bandwidth to reach a new node in the network then you’re not strengthening the network’s resources. Likewise, relying on a proxy to do ‘direct’ connections in say – a chat program – is a bit of an oxymoron.**

Relays work well as a fallback for worse-case scenarios. But they don’t fundamentally contribute to the technological development of a model to improve connectivity. Perhaps useful if we want to start to think about network censorship or even just useability improvements.

# My approach to the problem:

Relay servers are a short-cut and I don’t take shortcuts. I designed a system that supports every common strategy for connectivity. They include all the approaches you’re familiar with and introduce a framework for building new ones. The framework includes comprehensive support for NAT enumeration, multi-interface support, and a unique address design that improves pathing to services across networks. Here is a list of the connectivity strategies supported:

- UPnP port forwarding (IPv4)
- UPnP pin holing (IPv6)
- TCP direct connect
- TCP reverse connect
- TCP hole punching
- UDP TURN proxy (fallback, non-default)

# Status

Currently I have a Python 3.6 >= async library written. It’s portable (avoids C extensions) and tested on many OS. The software is currently a beta release and may contain bugs.

If you want to try out a simple, text-based demo:

python3 -m pip install p2pd

python3 -m p2pd.demo

Also, here’s my blog post on the project with more information:

https://roberts.pm/index.php/2024/11/05/p2pd/

Let me know what your thoughts are on the above and whether it’s worth continuing.

---
source: ethresearch
topic_id: 17523
title: Using IRC as an experimental DNS system
author: coinbend
date: "2023-11-26"
category: Networking
tags: []
url: https://ethresear.ch/t/using-irc-as-an-experimental-dns-system/17523
views: 956
likes: 0
posts_count: 1
---

# Using IRC as an experimental DNS system

Hello,

I’m a long time enthusiast of blockchain tech with many interests. I’ve been working on a p2p networking library in Python called ‘p2pd’ and one of my design goals is to essentially design the whole system in such a way that public, pre-existing, infrastructure can be used for its functionality. The reason for this is if you rely on running your own infrastructure which later disappears – your software stops working. My plan is to design something so that even when the project has no resources you can still do core functions like DNS, bootstrapping, relaying, and more.

My design looks like this at the moment:

‘Get address’ - Use STUN

‘Relay signaling messages to facilitate complex p2p connections that bypass NATs’ - Use MQTT

‘Proxy relaying as a fall-back if the above fails’ - Use TURN

I’ve been able to find open protocols and existing infrastructure for everything I’ve needed. But one key feature has eluded me: DNS. The conventional DNS system is paid and I want my software to be usable without paying fees. I’ve researched heavily what I could use for this. I’ve considered ways to hack different protocols to use as a DNS system but all of my approaches met dead ends. There is a project called ‘Opennic’ that provides a community-run DNS system but it doesn’t provide a good way to register and update the records. But recently I think I’ve found the solution.

My idea is to build a DNS system on top of IRC. The design would be to use channel topics to save DNS records. From there they could be used for dynamic DNS or really anything. The only requirement is that the IRC server needs to have an open account system that doesn’t need email verification. Most of them validates emails but I’ve found in practice there are enough that don’t to build a prototype DNS system. The advantage of my design compared to something like ENS is it would be free to use and I’ll be using it to simplify the addressing used for peers in my library. But it could be used for other purposes.

Let me know what you all think, I have a problem with motivation at the moment so any comments help me out a lot.

My current project homepage is here: [p2pd · PyPI](https://pypi.org/project/p2pd/)

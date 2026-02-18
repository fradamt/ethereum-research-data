---
source: magicians
topic_id: 19444
title: Improvement Idea for Ethereum Wallet Interaction Restriction Privilege
author: kirk_laz
date: "2024-03-31"
category: EIPs > EIPs core
tags: [erc, wallet, security, address-space]
url: https://ethereum-magicians.org/t/improvement-idea-for-ethereum-wallet-interaction-restriction-privilege/19444
views: 328
likes: 0
posts_count: 1
---

# Improvement Idea for Ethereum Wallet Interaction Restriction Privilege

**I’m not confident that this is the most appropriate location for this concept, so if there is somewhere it would better be suited PLEASE let me know.**

Anyway, a little background on why I am here…

Last weekend I was fortunate enough to be able to withdraw a small chunk of tokens from a project with which I have tokens vested. I had divided them into two portions–one that went to be cashed out, and the other to remain in my MetaMask wallet in order to save them until the due date for a debt I owe in the hopes that their value would continue trending upward (it did). When it came to the day I had planned to withdraw the second chunk, I saw that all of the tokens had been transferred out of my wallet into another. There are **many** reasons why I am not yet confident enough to say that the transfer was not my own doing, but I am leaning towards that belief. However, since I cannot be sure that this was not some sort of unauthorized access to my wallet, I am concerned for what happens next time that I am able to withdraw some of the vested tokens to my address–there is currently no way to alter the controlling address for the vested tokens.

Being in this situation, I started to wonder why there was not some function through which someone could *block* or *ban* specific addresses from interacting with their wallet. If this existed, it would allow me to block the ‘sketchy’ address now holding my tokens from interacting with my wallet, preventing them from being able to have access to any future tokens I am able to receive–even if they had some sort of sweeper bot or whatever geared towards my wallet address.

All that said, I am here in the hopes that I could get some input on the feasibility of such a privilege, wherein anyone can explicitly block any specific addresses from interacting with their wallet(s). If this is determined to be feasible or practical, then I would love to put it forward as an official EIP & to begin building it myself.

I appreciate any and all input in advance. Thanks for your time!

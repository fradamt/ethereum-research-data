---
source: magicians
topic_id: 4630
title: "EIP-2938: Account Abstraction"
author: adietrichs
date: "2020-09-18"
category: EIPs
tags: [account-abstraction]
url: https://ethereum-magicians.org/t/eip-2938-account-abstraction/4630
views: 5443
likes: 13
posts_count: 10
---

# EIP-2938: Account Abstraction

As announced on the last core devs call, the Quilt team ([@willvillanueva](/u/willvillanueva), [@SamWilsn](/u/samwilsn), [@matt](/u/matt), [@adietrichs](/u/adietrichs)) in collaboration with [@vbuterin](/u/vbuterin) has published a new account abstraction EIP:


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-2938)




###

Details on Ethereum Improvement Proposal 2938 (EIP-2938): Account Abstraction








Account abstraction (AA) allows a contract to be the top-level account that pays fees and starts transaction execution.

Relevant Links:

- EIP-2938 Explained
- DoS Vectors in Account Abstraction, a Case Study in Geth
- Implementing account abstraction as part of eth1.x
- Case Study: UTXOs on Ethereum
- Account Abstraction Playground

In addition to this thread, you can find us in the [#account-abstraction](https://ethereum-magicians.org/tag/account-abstraction) channel of the Eth R&D discord.

## Replies

**adietrichs** (2020-10-26):

To add to the previous link list, a few recent additional AA-related resources:

- Account Abstraction Beyond EIP-2938
- Presentation by Vitalik at an Ethereum Engineering Group meetup
- Presentation by @SamWilsn and me at the ETHOnline hackathon, slides here

Discussion on AA can currently be found primarily in the [#account-abstraction](https://ethereum-magicians.org/tag/account-abstraction) channel of the Eth R&D discord server, which you can join [here](https://discord.gg/GU55yAW).

---

**tkstanczak** (2020-11-13):

Why is PAYGAS not using stack if it needs to 32byte long params?

---

**poojaranjan** (2020-11-16):

An episode on [Peep an EIP-2938](https://youtu.be/HvZd6z2YdZs) with [@adietrichs](/u/adietrichs) & [@SamWilsn](/u/samwilsn)

---

**anett** (2020-11-18):

On Friday **November 20 at 12:00 EST** we are going to host Community Call on Account Abstraction ![:phone:](https://ethereum-magicians.org/images/emoji/twitter/phone.png?v=9)

[YouTube Live stream Link](https://youtu.be/0hAIjLFe38Y) ![:desktop_computer:](https://ethereum-magicians.org/images/emoji/twitter/desktop_computer.png?v=9)

[Announcement](https://medium.com/ethereum-cat-herders/account-abstraction-community-call-4744ff0f56d9) ( Medium article) ![:loudspeaker:](https://ethereum-magicians.org/images/emoji/twitter/loudspeaker.png?v=9)

Feel free to drop questions to this post ![:weight_lifting_man:](https://ethereum-magicians.org/images/emoji/twitter/weight_lifting_man.png?v=9)

---

**matt** (2020-11-30):

FYI here is a link tree with the full history of AA (from 2015): https://hackmd.io/@matt/r1neQ_B38

---

**SamWilsn** (2020-12-11):

> Why is PAYGAS not using stack if it needs to 32byte long params?

To enable upgrades (eg. EIP-1559) the opcode needs to accept a variable number/length of arguments.

---

**poojaranjan** (2020-12-14):

Understanding the Account Abstraction proposal and getting answers to open questions in Peep an EIP-2938 [Part-1](https://youtu.be/HvZd6z2YdZs) & [Part-2](https://youtu.be/Xoc4q1nJzsU) with Ansgar Dietrichs & Sam Wilson.

---

**axic** (2021-06-25):

I know that account abstraction is not actively researched currently, but with the [EVM Object Format](https://ethereum-magicians.org/t/evm-object-format-eof/5727) we made a claim that EIP-2938 can be somewhat simplified. Here’s a short explainer for that: [Account Abstraction with EVM Object Format - HackMD](https://notes.ethereum.org/@axic/account-abstraction-with-eof)

Note that it is a rough sketch and I haven’t spent much time on going very deep into details. Notable differences include:

1. Account can advertise their claimed gas limit for the verification code
2. The verification code is clearly demarcated
3. PAYGAS can use stack items (as new version can be added via EOF versions)

---

**dror** (2025-05-07):

Can this EIP be marked as `withdrawn` ?

We are in the process of finalizing ERC-4337.

We  do want to reference this EIP, as it is a precursor for account abstraction, but as long as it is `draft`/`stagnant` we can’t reference it, even if for historical reasons.


---
source: ethresearch
topic_id: 2484
title: Flipping consensus
author: tpmccallum
date: "2018-07-08"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/flipping-consensus/2484
views: 872
likes: 0
posts_count: 1
---

# Flipping consensus

I have been soaking up the brilliant Plasma Implementers Calls since #1.

There is a reoccurring theme around the availability problem (block withholding problem) in Plasma. In addition, while there are a lot of clever designs and great ideas about exit games, it appears that the size and complexity of these smart contracts is growing to a potentially untenable level [1]. The conversation about context (Solidity’s DELEGATECALL vs Vyper’s CALL) in a game’s smart contract was also very interesting. I will cut to the chase…

I am wondering if anyone would like to provide some constructive feedback in relation to the idea of flipping consensus in a second layer design. By flipping, I mean moving away from post transaction exit games towards up-front deterministic behavior.

Here is a brief and over simplified example. The design includes a network activity nonce. The network activity nonce must be fetched before any and all activity. By fetching an activity nonce, the participant is signaling and declaring their intent to perform that particular action/transaction/validation. In the event that the participant does not perform that certain network activity (due to deliberate or accidental circumstances) the design has the ability to annul that specific queued network activity and nonce.

A participant’s privilege to fetch nonces is relative to the total amount of participants, in a way which is fair. Of course fetching and withholding will sharply reduce a participant’s fetching privileges (relative to other participants). Alternatively, fetching and correctly executing could increase a participant’s privileges.

I really like the design of Lightning (its simplicity and power to provide trust-less blockchain functionality off-chain) and its use of CHECKSEQUENCEVERIFY to measure relative minimum age and in doing so provide revolutionary trust-less off-chain consensus and finality.

If this seems to abstract, please think of it as a thought experiment to which you can provide helpful feedback. I have ideas about how the application could annul the queued network activity and free the nonce. Did not want this first post to be too long, looking forward to some new feedback and ideas!

Kind regards

Tim

[1] https://youtu.be/M_PtvXrrTko?t=2054

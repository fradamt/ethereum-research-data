---
source: magicians
topic_id: 622
title: Decentralized recurring payments protocol
author: kerman
date: "2018-06-30"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/decentralized-recurring-payments-protocol/622
views: 819
likes: 1
posts_count: 1
---

# Decentralized recurring payments protocol

Backstory: I got involved with crypto in the December bull run. After speculating for a while, I decided to understand the core technology behind the Bitcoin and Ethereum by reading the technical papers (the beige paper for Ethereum was a massive help). My first project was a masternode hosting side which I put up in a week and used Stripe for recurring payments (fiat based). 1 week later I got a message from Stripe saying they’re shutting down my account because it was “high risk” and providing a “prohibited” service. It was at that time I decided to implement recurring crypto payments. However there wasn’t any service/sdk/protocol to solve this issue. I wondered why no one had solved this issue.

Turns out it was for the following reasons:

- Volatility. For anyone to accept a fixed 1/ETH a month for payment would be unpredictable. By using something such as Oraclize to program exchange rates into the smart contract introduces a high level of centralization. In addition, the gas costs to continually update this constant would be inefficient.
- Push payments. Crypto is inherently push based, you can’t pre-authorise payments. One solution is to create smart contract that has custody of a user’s funds. While this could work, users have to continually top up the escrow account or pay the total amount up-front.
- Scheduling. You can’t have a smart contract call itself without introducing a high level of centralisation (external server running a CRON job). There may be an argument that centalisation is okay in this case, however a failed trigger will result in merchants not receiving payments. It also means that accounts with an insufficient balance at time of payment will get free service.

I spent a few weeks reading and thinking to come up with a solution that solves the problems listed above.

What I came up with was the following:

- Use of ERC20 stable coin such as MakerDao to avoid having to program stability into the smart contract itself or using a 3rd party oracle.
- The ERC20 standard’s approve function can open the possibility for someone to spend tokens on your behalf. This is essentially what enables the protocol to facilitate trustless pre-authorised recurring payments between two parties. In addition, gas costs paid can be paid by an external third party at the time of execution.
- Scheduling is solved through incentivising “service nodes” (clients calling smart contracts) to process the payment at the time that it’s due. What makes 8x is the way it solves the “claiming problem” described by Piper Merriam (Ethereum Alarm Clock).

– The problem: you have a smart contract with a bounty worth $0.10. However, the gas costs to claim this bounty are $0.075. If there’s 2 competing actors trying to claim the bounty you’ll end up with $0.05 worth of wasted gas and a 50% probability of claiming the bounty. If you extrapolated to 1000 actors trying to claim the reward you’ll end up with a 0.1% chance of claiming the reward and there’ll be 999 transactions that would have gas wasted. The 8x protocol solves this by using a proof-of-stake style design where tokens are required to be staked and locked up.

– Example: a subscription worth $10 and 1% fee is due (set by the business). The service nodes on the 8x network can then claim to process the subscription provided they have 10 tokens staked in the contract (multiplier of 1 set). They now have the first right to claim the subscription every subsequent month to process the subscription, and if they don’t process at the time the payment is due, they lose their locked up staked tokens. Going back to the claiming problem, when the network launches there’ll be a high number of service nodes (demand) compared to subscriptions available (supply). To balance out supply and demand, the multiplier is set to a higher number (say 100) so that only actors with enough capital (8x tokens) can process subscriptions. The more subscriptions processed, the less capital they have left to process more. As usage increases, the multiplier is decreased to the point where supply and demand are at parity. More details of this can be read up about in the white paper: https://github.com/8xprotocol/whitepaper.

Apologies for the super long post, I didn’t intend to go in such detail!

The vision for 8x is to be infrastructure for the entire Ethereum community to use. You can view our progress at: https://github.com/8xprotocol/contracts.

Would love to hear your thoughts on the project and any questions you might have about it.

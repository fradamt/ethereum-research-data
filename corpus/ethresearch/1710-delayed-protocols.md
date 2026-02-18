---
source: ethresearch
topic_id: 1710
title: Delayed Protocols
author: drstone
date: "2018-04-11"
category: Economics
tags: []
url: https://ethresear.ch/t/delayed-protocols/1710
views: 1127
likes: 1
posts_count: 2
---

# Delayed Protocols

Recently, I’ve been exploring new ideas related to PoW systems and how we can use ideas from PoS to build new protocol mechanisms. While this doesn’t have to do with PoS or Ethereum specifically, I thought it’s worth sharing the research. Attached you can find the paper: [Delayed_Blockchain_Protocols (1).pdf](https://ethresear.ch/uploads/default/original/2X/6/6c4b239f019c70eb0dce156ba2b563846e4bdfb5.pdf) (230.8 KB)

TL;DR

We can simulate “staking” mechanisms in Proof of Work systems by delaying the issuance of miner rewards. That is, miner’s earn rewards for blocks they mine at some arbitrarily tuned, future date/round. In this manner, if a miner attempts to double-spend (or other malicious actions), proof of this behavior can lead to slashing their future rewards. The range of additional functions that can be utilized on top of delayed rewards, such as decaying rewards for short-lived miners, is vast. If we combine what we know from infinitely repeated games with punishment phases and that of staking mechanisms, we can incentivize long-lived, honest behavior by forcing miners to wait for their rewards. In doing so, these miners have stake in the future payouts and are less incentivized to deviate from the protocol (the cost of an attack is at least as much as their delayed payments for arbitrary delay rates).

I’d like to hear people’s thoughts on this idea and whether it holds up. I know Bitcoin delays rewards by 100 blocks for other reasons than incentive compatibility, but this method is strictly for increasing the security of the underlying protocol by increasing the cost of successful deviations from the protocol.

As it relates to Ethereum, delayed rewards on top of a PoS system could provide additional incentives for validators to stick around. Although I focus on PoW, it can easily be extended to PoS since delayed rewards are agnostic to the PoX and underlying protocol (thought being implemented on said protocol).

Thanks to [@nate](/u/nate) for comments on the idea.

## Replies

**Etherbuddy** (2018-04-12):

Nice idea, especially because it can be implemented in the code of the protocol, without any need to make a further contract.

It could also be implemented in a network of masternodes.

Concerning POS and the “nothing at stake” problem, my opinion is that the main deposit should not be at stake. It should be safely stored is a cold wallet, the private key never being displayed.

What could be at stake is a smaller amount paid to other masternodes when a new masternode (validator) joins the network.

For example, if there are 1000 masternodes, a new entering masternode could pay 0,01 ETH to every other masternodes. It would then pay 1 000 x 0,01 = 10 ETH to enter the network.

If the node is malicious, it could just be blacklisted by other masternodes, and it would lose the amount paid to the other masternodes when it joined the network.

What would be at stake is a smaller amount than the main deposit. This smaller amount would be lost in case of misbehavior.

There 's no need for a harder penalty in my opinion because :

- most ETH holders are not malicious
- there are hundreds of POS and masternode coins, attacks are very rare despite there is nothing at stake
- a little amount at stake is appropriate : in case of malicious behaving, the masternode is expelled within minutes, and the  amount of ETH paid to join the network is lost
- having the main deposit at stake creates risks of huge losses due to bugs, hacking, security breaches … and worry ETH holders who are not malicious


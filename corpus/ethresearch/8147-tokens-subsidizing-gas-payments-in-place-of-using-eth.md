---
source: ethresearch
topic_id: 8147
title: Tokens Subsidizing Gas Payments in Place of Using ETH
author: EazyC
date: "2020-10-22"
category: Economics
tags: [fee-market, gas-abstraction]
url: https://ethresear.ch/t/tokens-subsidizing-gas-payments-in-place-of-using-eth/8147
views: 1822
likes: 1
posts_count: 2
---

# Tokens Subsidizing Gas Payments in Place of Using ETH

With all the DeFi craze of subsidizing liquidity, I was thinking how it would be possible for tokens to pay transaction fees (in their own token) directly to miners for users during times of high gas fees to help the network.

Firstly, I realize that it’s possible to mint an ERC20 token into a contract, auction/Uniswap it for ETH and have that contract’s ETH be used as gas payment for its users. This is not about that. This is about the current limitations of replacing the ETH gas fee with an ERC20 token during times of high gas fees.

For example, if a tx costs $20 in ETH to be included in the next block, a project’s smart contract could specify a double-subsidy rate of 20% which means that a user can pay $15 worth of the ERC20 token as gas (20% discount) and the protocol mints 20% + 20% on top of the $15 fee paid by the user (so a total of $25 worth of token) to go to a miner who would accept this transaction. This double-subsidy does 2 things: it makes it cheaper for users to pay for gas in the token by 20% and it makes it more lucrative for miners to accept the token as gas in place of ETH by 20%. The incentivization is bidirectional (miners and users both) and the smart contract could use the Token:wETH Uniswap pair to apply the subsidy rate without the need of an oracle.

Judging by previous discussions around this topic, the technical feasibility of miners accepting ERC20 tokens in place of ETH is difficult pre-EIP1559 because there is no reliable way for a contract to query if a tx hash exists within a particular block. Otherwise users could deposit the ERC20 token in a ERC-GasSubsidy contract, specify a gas price+limit, then send 0 ETH gas tx’s. Miners that want to accept the ERC20 as a possible payment in place of ETH could set their nodes to listen for 0 ETH gas tx’s from addresses that have a balance in ERC-GasSubsidy contract, include the tx in their block, include their own tx to the contract which claims the payment. But the problem is that final step. Does anyone know of a feasible method that a smart contract could directly pay a miner address for including X tx in Y block?

It’s an interesting problem to tackle because DeFi dapps could actually subsidize lower gas prices as well as adoption of their token which is a win win for everyone.

## Replies

**MaverickChow** (2020-10-28):

If someone creates a non-native token and then manipulate its price up to gain economic significance and use such significance to game the network (and ultimately influence governance as well), who is going to stop this? Almost literally anyone can create free money that miners / validators will stupidly accept.


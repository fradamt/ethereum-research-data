---
source: ethresearch
topic_id: 2485
title: Are second layer solutions fair to accounts during Hard Spoons and Airdrops?
author: tpmccallum
date: "2018-07-08"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/are-second-layer-solutions-fair-to-accounts-during-hard-spoons-and-airdrops/2485
views: 1609
likes: 1
posts_count: 3
---

# Are second layer solutions fair to accounts during Hard Spoons and Airdrops?

A hard-spoon takes the account state from a main chain (like Ethereum) and creates a genesis state for a new chain. This process of freezing/snapshotting/spooning allows a new blockchain to inherit the main chain’s account balances, “as at” a particular point in time. Real world examples of this would be EOS and Cosmos.

With the advent of state channels and side chains, how could we ensure that the state of a given second layer implementation (as at a particular point in time) is reflected in the snapshot/hard-spoon?

For example, in the event that we are able to transfer ERC20 tokens inside state channels [1], how could we ensure the accuracy of token Airdrops; when tokens are tied up in state channels and not accurately visible in the main chain’s state?

Does the hard-spoon process need to evolve or can the second layer solutions provide their state as required?

If neither of these are achievable, will popular hard-spoons and/or airdrops (which essentially offer financial gains to users) have an effect on activity within second layer solutions? Might we see mass exits to the main chain during snapshots/hard-spoons?

[1] https://github.com/ConnextProject/ethcalate-bidirectional-erc20-single

## Replies

**ldct** (2018-07-09):

> how could we ensure the accuracy of token Airdrops; when tokens are tied up in state channels and not accurately visible in the main chain’s state?

The tied-up tokens are visible in the main chain state, since whatever is locked into a state channel (the “state deposit”) must be locked somewhere; the main thing we have to worry about is if the state deposit holder isn’t aware of whatever is airdropped into it.

This problem also exists outside of L2 solution. If, for e.g., you hold ether in a very limited-functionality multisig which only contains functionality to spend ether, and an ERC-20 token gets airdropped based on eth balance and the multisig receives some amount of the token, it can never spend it.

Most modern multisigs like gnosis don’t have this problem because they’re designed to have the same functionality as an EoA (as long as enough owners sign off). One of the advantages of the constructions in  [Counterfactual: Generalized State Channels](https://ethresear.ch/t/counterfactual-generalized-state-channels/2223) where the state deposit holder is a multisig wallet, is that if some fancy new thing gets airdropped into a state deposit holder, at the very least, in the case where all the parties to the state channel cooperate, they can spend the fancy new thing.

For state channels, then, a remaining open question then is how to prevent one single party to the channel from not agreeing to spend the airdropped thing, hence “holding it hostage”.

For plasma, even the first solution does not apply, since there’s no mechanism for the contract to safely execute arbitrary commands. In the very specific case of plasma cash without splitting, we could create this mechanism by making each deposit create a new contract, and a successful exit simply assign ownership of the contract to the exiter. Even this technically doesn’t cover all cases, for e.g., a pull-based airdrop where you have 3 days to claim some token (since 3 days is not enough to claim ownership of the contract). An alternative might be to assign the right to make `CALL`s from the plasma contract outside of a specified blacklist to the operator or to some other party or to a DAO, and having the value of airdrops accrue to that entity. Arguably this situation is analogous to any smart contract that locks collateral, eg MakerDAO CDPs.

---

**haydenadams** (2018-07-09):

ETH locked in a state channel can’t be staked. Staked ETH can’t be deposited into a Plasma chain. ETH locked in a Plasma chain doesn’t accumulate airdropped shitcoins for the depositor. Its up to users to decide where their ETH will be most valuable.

But of course not all airdrops/hardspoons are “shitcoins.” With serious projects like Ethermint and Cosmos/OMG its definitely something worth thinking about. Token distributers should factor this stuff in and work towards better distribution techniques. I’m not a huge fan of blind airdrops and hardspoons since the number of tokens that will never be redeemed (essentially burned) is hard to quantify.


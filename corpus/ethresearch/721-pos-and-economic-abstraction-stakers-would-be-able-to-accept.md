---
source: ethresearch
topic_id: 721
title: "POS and economic abstraction: stakers would be able to accept gas price in any ERC20 token?"
author: 3esmit
date: "2018-01-16"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/pos-and-economic-abstraction-stakers-would-be-able-to-accept-gas-price-in-any-erc20-token/721
views: 7090
likes: 4
posts_count: 14
---

# POS and economic abstraction: stakers would be able to accept gas price in any ERC20 token?

The PoS stakeing contract will accept inclusion of transactions using gas price other then in ether?

I see that a separated contract can be used, but I would find great if users can include transactions and be paid in any ERC20 token (or at least the token in transfer).

I’m not sure if ERC20 abi is sufficient for this, maybe something more advanced such ERC777.

## Replies

**stri8ed** (2018-01-17):

If there is no need to use Eth, what prevents the price of Eth dropping to a point where value of POS deposits are insufficient to keep the system secure?

---

**3esmit** (2018-01-17):

I guess ether would still be important for staking or deploying new contracts.

---

**OliverNChalk** (2018-01-17):

Do you mean if users can pay their fees in any transaction or can receive the rewards from staking in any transaction?

Doe paying eth fees this is not feasible as it adds a layer of issues and complexity. If you want to receive payment in a token you can just use a dex to convert it instantly.

---

**3esmit** (2018-01-20):

No, I mean staking Ether and accepting fees in any ERC20. I see that this would make things simplier for who wants to use Ethereum Network but don’t want to buy ether to use as gas.  Using Ether they probably would have more chances of being mined, as by default everyone accepts gas in Ether.

I see that this is technically possible as a smart contract, and maybe not necessary to be done in POS contract.

I know that one plan was enabling contracts to pay the gas and this could be other solution.

---

**vbuterin** (2018-01-22):

Paying gas in ERC20s is difficult, because it means that the abstraction scheme would need to support arbitrary operations for gas payment and for gas refunds. Previous abstraction schemes allowed this, but at the cost of much extra complexity. Additionally, ERC20 gas payment means that gas payment to the coinbase has to be done as part of the transaction, rather than at the end as is the case now, which means that the storage key for the coinbase (note: NOT the coinbase account, the storage key for the coinbase in the ERC20) has to be part of the access list, which means the transaction sender has to know in advance who the block proposer is. In short, it’s complicated.

---

**3esmit** (2018-01-22):

Indeed, the part of arbitrary operations in the ERC20 implementation makes this really complicated. I see that the move of funds of ERC20 gasPrice would require also gas to make the ERC20 payment to the unknown future validator, seems indeed a loophole of problems, better keep it simple, thanks for the clarification. ![:grinning:](https://ethresear.ch/images/emoji/facebook_messenger/grinning.png?v=9)

I think that this is more something like what Raiden does, but without the RDN token (using the token being sent as fee), or maybe that could be done in a Token contract that itself supports the pay of “transfer fee” (not gas) which later could be included by other actor which would pay the gas and get the “transfer fee”.

---

**clesaege** (2018-02-01):

> If there is no need to use Eth, what prevents the price of Eth dropping to a point where value of POS deposits are insufficient to keep the system secure?

The fact that ether gives you some chance of getting paid TX fees, no matter in which coin, does.

---

**SRALee** (2018-02-01):

Vitalik basically confirmed in the comments above that it is a bit too difficult abstractly (although theoretically possible) to implement in a feasible manner. But I can’t help but feel that if implemented, it would essentially make ETH the same utility token as OMG.

---

**3esmit** (2018-02-01):

As I mentioned above, this is more something to be implemented in the smart contract layer.

I’ve managed to implement a Token that enables the pay of gas to transfer using the token itself using Ethereum Signed Messages:

Source: https://github.com/status-im/contracts/blob/presigned-token/contracts/token/MiniMeTokenPreSigned.sol

Proof: https://ropsten.etherscan.io/tx/0x52a886755876e7f88fed90cae3f58ee8e00cdcaa2dac24382202d0e37ed14059

I see that we might have gas-waste with multiple accounts trying to include the same signed message to the contract,  I’m enabling non sequential nonces, but this might be ripped-off as is not necessary.

---

**3esmit** (2018-10-31):

I will continue this research on Status forum: https://discuss.status.im/t/gas-relayer-for-status-nodes/653  and #status-gas-relay Status Public Chat Channel.

---

**MaverickChow** (2018-11-12):

1. Which transaction has higher total gas cost:
a. Transaction that pays with ETH (less computation), or
b. Transaction that pays with ERC-based token (more computation)?
2. Which has higher utility value as means of exchange in overall economics beyond the scope and function of any particular dapp:
a. ETH, or
b. An ERC-based token?
3. Which is easier (and less costly) to be manipulated by any particular party at the expense of others:
a. ETH, or
b. An ERC-based token?

I have no idea why the idea of using tokens (instead of native coin such as ETH) to pay for gas is so persistent. That’s probably the inherent power of being irrational. Such concept would totally fail in real life economics and yet so many people continue to push the idea into the blockchain space.

---

**3esmit** (2018-11-12):

ETH would be the most constant token for all cases, and obviously the cheapest. It’s not only about paying gas in ERC20, but about contracts paying execution in ETH (or ERC20), so keys from a multisig wouldn’t need ether for authorization of execution.

But the most powerful point is the user experience for dapps that use another token, so users don’t need to take care of 2 balances for interacting with any ethereum based Dapp.

Ether would be always the best for execution, and ERC20 would be a convenient slightly more expansive way to transact in any Dapp.

For your questions, 2 and 3 depends on the token. 1 is a.

At the end, if you need to convert (sell) your tokens to get ETH to pay for the gas, ultimately 1 would become b, because the amount of gas required for the conversation of ERC20 could get more expansive, unless the user always do it in big batches.

---

**MaverickChow** (2018-11-12):

My personal answer would be 1. b  2. a  3. b.

1. b for the reason you said. Even in big batches, using ETH as gas is still cheaper overall.
2. is a because of various economic reasons. One reason can be explained using the earth and our own local currency as metaphor examples. The earth spins very fast but we all do not feel it because we are all moving with the spin. We only feel the spin when we are outside of it. Similarly, the dollar is a volatile currency but for a US citizen he does not feel it because his income, expenditure, etc are all denominated in USD. He will only feel the daily volatility if he is a foreigner. ETH at the moment is volatile but only because we are still based on fiat system. However, when ETH becomes part of our mainstream life, we will not feel its volatility. But we would be introducing various sources of volatility unnecessarily into the network if we allow various differing tokens to be a means of exchange within the same network. This is because a stakeholder would need to account for the pricing differences of each token relative to the rest, just as you said. Imagine if everyone in your country can now choose to accept and pay in myriads of foreign currencies and gift cards too. The amount of complexities added into the economy not only is unnecessary but also the local economy will be exposed to a great amount and frequency of pricing volatility on an everyday basis as everyone will try to keep account of the exchange rate of each currency pair. Eventually everyone would scream for a unified currency. But we already have a unified currency that is ETH. And so I believe suggestion for using tokens to run dapps and pay for gas is actually a clear step backward.
3. is b because anyone can create his own token that may be unbacked or backed by the utility of a dapp. But because the issuance is purely from an entirely private source, its pricing, supply, and contract functions are much easier to be manipulated by private entities at the expense of those that choose to accept it and pay with it. Even if a dapp eventually becomes very useful, limiting its application by way of a token is no different from introducing a bartering system. Two persons trying to exchange a cow with a wheelbarrow of wheat is no different from the same two persons trying to exchange token A with token B. Unless the private entities that issue the tokens (A and B) try to promote their tokens as a means of exchange, but then we already have the native coin as a means of exchange. Thus the real intent is not about promoting a token as a means of exchange but rather a covert way of money grab. Besides, if such hype is well accepted (i.e. use tokens to run dapps and pay gas), that means nobody in general is really interested in a decentralized system other than lip service, as tokens are somewhat centralized construct. For a purely decentralized construct, we already have the native coin. I think most are still not clear of the fact that tokens are not proper means of exchange in whatsoever manner.

Moreover, by right initially doing dapps with ICOs was never supposed to be the idea. But because such trend took hold from monkey-see(Ether)-monkey-do(token), thus today we keep hearing the hype of running dapps and pay gas in tokens instead of ETH. Even without token, a dapp would still run well. In my opinion, token has its main function primarily in the sphere of asset tokenization to keep account of who owns what. Introducing token as a use case for dapp and gas is an inefficiency.


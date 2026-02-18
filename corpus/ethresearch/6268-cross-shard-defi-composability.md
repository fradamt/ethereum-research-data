---
source: ethresearch
topic_id: 6268
title: Cross-shard DeFi composability
author: vbuterin
date: "2019-10-10"
category: Sharded Execution
tags: [cross-shard]
url: https://ethresear.ch/t/cross-shard-defi-composability/6268
views: 32397
likes: 24
posts_count: 24
---

# Cross-shard DeFi composability

There has been concern recently about whether or not the “composability” property of Ethereum - basically, the ability of different applications to easily talk to each other - will be preserved in an eth2 cross shard context. This post argues that, yes, it largely will be.

### What does sharding change?

Transactions within a shard could happen as before. Transactions between shards can still happen, and happen quickly, but they would be asynchronous, using receipts. See https://github.com/ethereum/wiki/wiki/Sharding-FAQ#how-can-we-facilitate-cross-shard-communication for more information. In general, workflows of the form “do something here that will soon have an effect over there” will be easy; workflows of the form “do something here, then do something over there, then do more things here based on the results of things over there, all atomically within a single transaction” will not be supported. Doing things of that form would generally require first “[yanking](https://ethresear.ch/t/cross-shard-contract-yanking/1450)” the contract from the “over there” shard to the “here” shard and then performing the entire operation synchronously on one shard. However, as we can see from examples below, most use cases would not be significantly disrupted or could be trivially rewritten to survive in a cross-sharded model.

### Tokens

The ERC20 standard would need to be modified. Tokens would be able to exist on all shards, and seamlessly move from one shard to another just like ETH. This can be done with receipts, in the same way that ETH is moved from one shard to another, we can move tokens from one shard to another. There are no fundamental difficulties here.

### Composability example 1: Uniswap <-> Tokens

Nearly all DeFi applications are uses of composability, because tokens are a type of application and so any DeFi application that uses tokens is an application that interacts with another application. Let us look at Uniswap as an example. In Uniswap, a user sends some quantity of token A to a Uniswap contract, which sends some quantity of token token B back to the user. Uniswap requires strict dependency between all transactions that interact with it: the Nth transaction must be aware of the output of the N-1’th transaction, because this is how the price updating algorithm works.

Hence, the Uniswap contract would need to live on a single shard (there are designs for multi-shard Uniswap, but they are more complex). Users looking to trade would perform a 2-step procedure:

1. Send their token A to the shard that Uniswap is on.
2. Perform a trade with Uniswap as before (the transaction doing this would be combined with the transaction “claiming” the receipt from step (1), so it’s a single step)
3. [Optional] If desired, move the token B that Uniswap gave them to some other shard.

### Composability example 2: Lending on Compound (including cDAI etc)

Compound could also exist on a single shard (if Compound gets too popular, different *instances* of Compound representing different pairs of tokens can be put on different shards). Users with a token would move their token over to the shard the particular Compound instance is on, and (create | fill | bite) a leverage position as before.

### Composability example 3: tokens inside L2 scaling solutions (Rollup, Plasma…)

Move your tokens to the shard the L2 scaling solution has a contract on. Deposit into the contract. Done.

### Composability example 4: rDAI, gDAI, etc

Move your DAI into the [insert DAI flavor here] contract. Take [insert DAI flavor here] out, and move it to whatever shard you want. The [insert DAI flavor here] contract itself could just sit on the same shard as the Compound instance for DAI for convenience.

### Composability example 5: Set Protocol

Move your tokens into the shard that the set protocol contract is on (different instances could be in different shards as in Compound). Send them into the set protocol contract, get out a set token, move the set token to whatever shard you want.

### Composability example 6: oracles

*Synchronous* cross-shard transactions are not supported, and so the “call a contract and immediately see what the answer is” workflow would NOT work. Instead, however, you could simply provide a Merkle proof showing the value in the state of the contract on the other side in the previous block (or in the most recent block for which the application’s shard is aware of the oracle contract’s shard’s state root).

### Composability example 7: non-fungible assets and markets

Non-fungible assets including NFTs, in-game assets, ENS names, MakerDAO CDPs, Compound positions, etc, [can be “yanked”](https://ethresear.ch/t/cross-shard-contract-yanking/1450) to other shards, where they can interact with other applications (eg. atomic swap markets, auctions) seamlessly as before.

### Overlay tools (eg. Instadapp)

In general, overlay tools that use specialized smart contracts to interact with dapps would need to create contracts for each function that they support, that users could yank to a desired shard, and then use on that shard to perform any needed functionality as before.

## Replies

**drcode1** (2019-10-10):

Apologies if this is obvious to other people, but would an eth2.0 ERC20 token, as you envision it, require a copy of the contract to exist on every shard?

Or, is there some technique I’ve overlooked for supporting a token on all chains but with only a single contract on one shard?

---

**vbuterin** (2019-10-10):

Good question! It would indeed require a copy of the contract on every shard (the contract can exist “counterfactually” until needed via a CREATE2-type scheme). The overhead from this can be cut down through a mechanism we are introducing where for a high fee users can save code on the beacon chain that on-shard code can reference by index and access; this is also how we prevent account abstraction from leading to overly large witness sizes.

---

**cdetrio** (2019-10-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> ### Composability example 6: oracles
>
>
>
> Synchronous cross-shard transactions are not supported, and so the “call a contract and immediately see what the answer is” workflow would NOT work.

You said in the post [A simple synchronous cross-shard transaction protocol](https://ethresear.ch/t/simple-synchronous-cross-shard-transaction-protocol/3097) that a synchronous cross-shard transaction protocol would be simple, which implies they would be easy to support. So why are you saying they’re not supported?

---

**Agusx1211** (2019-10-10):

My biggest worry is loosing the atomicity of the contract calls that we have to day, and leaving users “stranded” on intermediary states. Let me give an example:

Suppose that we have our user on shard A, he has DAI but he wants to lend on RCN, and RCN it’s on shard B, while Uniswap is on shard A too.

Currently, without sharding, and smart contract can, in a single transaction, convert from DAI to RCN, and then execute the “lend” operation, if the lend operation fails (maybe because some other user filled the request first), the DAI -> RCN convertion it also get’s reverted, and the user just get’s a message saying “ups, someone else filled the request”, but he still has the DAI.

With sharding, that user would need to first convert from DAI to RCN, (because Uniswap is on shard A), and then move those RCN to shard B, if during that process the loan on RCN is filled by another user, the user ends up on shard B with RCN, but with no loan to fill, and thus has to do all the process backwards if he want’s to convert back to DAI (exposing himself to RCN in the process).

This may sound like a silly example, because if an user wants to interact with RCN it’s likely that he doesn’t mind to be exposed to the RCN token, but variants of this “intermediary stranded  state” would have to be taken into account when developing DeFI composability.

I personally don’t have in mind an easy solution for this problem, maybe we will need to reshape how we build dApps on a cross-shard ecosystem

---

**vbuterin** (2019-10-10):

This is definitely true! Atomic “I get exactly what I want or I get nothing” guarantors are going to become more difficult. In this specific case, RCN could be designed so that individual loan opportunities could be separate contracts, in which case the user could yank one such contract to shard A and then do the transaction atomically. But in a more general case, this will sometimes not work (eg. you would not be able to do risk-free arbitrage between Uniswap and some other single-threaded DEX on some other shard).

---

**spengrah** (2019-10-10):

Some open questions…

- Does the Ethereum community value Eth2 levels of transaction throughput more than atomic contract composability?
- How should we be thinking about that trade-off?
- Is there an intermediate scaling solution that conserves atomic composability?

---

**drcode1** (2019-10-10):

Hi Spencer, long time no talk! I think the added contract complexity introduced by async receipts is a genuine issue for all developers, but it is still a pretty minor imposition in the scheme of things, if the gas fee in eth2.0 for transactions drops from (let’s say) 10 cents to one one-hundredths of a cent.

---

**cdetrio** (2019-10-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This is definitely true! Atomic “I get exactly what I want or I get nothing” guarantors are going to become more difficult. In this specific case, RCN could be designed so that individual loan opportunities could be separate contracts, in which case the user could yank one such contract to shard A and then do the transaction atomically. But in a more general case, this will sometimes not work (eg. you would not be able to do risk-free arbitrage between Uniswap and some other single-threaded DEX on some other shard).

This is why people are saying that Eth 2.0 breaks composability, because yanking sucks (“if you break RCN and rewrite/redesign the whole ecosystem to work by yanking, it will basically kinda work the same as before, usually”).

![](https://ethresear.ch/user_avatar/ethresear.ch/spengrah/48/19006_2.png) spengrah:

> Some open questions…
>
>
> Does the Ethereum community value Eth2 levels of transaction throughput more than atomic contract composability?
> How should we be thinking about that trade-off?
> Is there an intermediate scaling solution that conserves atomic composability?

For atomic transactions (i.e. synchronous), there is no real throughput to be gained by sharding. It takes multiple asynchronous transactions on multiple shards, yanking, claiming, and so on, to accomplish the same update that is done in a single synchronous transaction (this is [Amdahl’s law](https://en.wikipedia.org/wiki/Amdahl%27s_law)). It’s worse DX, and no actual gain in throughput.

There are proposals to conserve atomic composability across shards (probably not always and not for all transactions, just the subset that need them) – I just linked one above. I’ve been arguing for years that it should be a priority to enable contracts to continue working as they do on Eth1 (i.e. with atomic composability / synchronous calls), on Eth2.

---

**vbuterin** (2019-10-11):

So I guess the question is, how much of the value is lost by only allowing asynchronous operations? I definitely think it’s not reasonable to claim that “composability” as a whole is lost if synchronous operations are lost; crazy combinations like “let’s have a Uniswap market between cETH and cDAI so that liquidity providers can earn interest while they provide liquidity” are still just as possible as before, and indeed require basically no rewriting.

I agree that risk-free arbitrage and more generally risk-free “see if things are possible over there, and if not come back here” become more difficult (but not impossible!) but I’m not sure that that large a portion of the value of combining defi applications comes from such things.

> if you break RCN and rewrite/redesign the whole ecosystem to work by yanking, it will basically kinda work the same as before, usually

If we assume bounds on single-threaded computation, we can’t increase the throughput of a system without specifying data *independencies* that allow for parallelization. So any scheme for increasing throughput must include some way to specify these data independencies, which involves “rewriting” of some form. So I don’t think this problem is surmountable; you have to rewrite to take advantage of increased scalability.

---

**loiluu** (2019-10-11):

I think the examples given are in the most simple form and not that interesting. Many innovative use cases involve interaction between several smart contracts, and that requires *real composibility*. Let me give a couple of examples.

***1. SetProtocol***

When a user sends 1 eth to buy a basket of 3 tokens, say ZRX, KNC, DAI each 33.33%, everything happens in 1 transaction atomically. In that 1 single transaction, Set Contract calls Kyber contract 3 times to buy 3 tokens with the corresponding amount, and for each call Kyber contract might call different contract (e.g. Uniswap, KyberReserve, OasisDex).

Its important for Set’s use case to have all-or-nothing atomicity here, otherwise the ratio of the assets in the basket will not be correct. Having the purchases done **separately** but **simultaneously** in different shards will not help, though being more expensive and cancel out the scalability factor.

***2. On-chain arbitrage***

There has been a lot of arbitrage lately between Gnosis’s dutchX, Bancor, Uniswap, Kyber, SetProtocol’s rebalancer, etc. All these activities are necessary for automated pricing protocols like Uniswap, dutchX, bancor to have reflected market price. On-chain arbitrage is attractive and superior to centralized exchanges arbitrage because everything can be done instantly and atomically in a transaction: trader is guarantee to only arbitrage if there is profit, otherwise just revert the trade. Losing this atomicity will discourage a lot of this activities, and make it harder to attract traders.

---

**vbuterin** (2019-10-11):

> When a user sends 1 eth to buy a basket of 3 tokens, say ZRX, KNC, DAI each 33.33%, everything happens in 1 transaction atomically. In that 1 single transaction, Set Contract calls Kyber contract 3 times to buy 3 tokens with the corresponding amount, and for each call Kyber contract might call different contract (e.g. Uniswap, KyberReserve, OasisDex).

Is the assumption here that the basket ratios in Set may change *every block*? Because if not, this is easy:

1. You call Set contract with 1 ETH
2. Set calls Kyber
3. Kyber sends orders out to DEXes, specifying that it wants to fix the quantity purchased rather than the quantity spent (eg. Uniswap allows this)
4. Get the coins back from the DEXes, along with a bit of ETH change left over (this is inevitable; even Uniswap gives change today)
5. Combine the tokens into a set

> 2. On-chain arbitrage

I agree smart contract arbitrage between different DEXes becomes harder in a cross-shard context. Though note that this is less of a problem if the DEXes are not single-threaded (ie. not like Uniswap). In an on-chain order book DEX, for example, orders can be yankable. DutchX auctions are yankable as well. This *does* run the risk that you pay fees to yank but then the arbitrage opportunity disappears. However, even if this probability is >50%, sharding reduces transaction fees by >95%, so on net arbitrage should still be much smoother.

---

**dbrincy** (2019-10-17):

Since there will be the need to update erc20 structure, why dont create some kind of main gas station dex  to pay gas with the tokens and also let move tokens inside L2 scaling solutions without the need to hold ether and the other plasma coin (for example matic) to move them in and out easily…

---

**k06a** (2019-10-18):

What about this example?

0x orders matching code:

```auto
function matchOrders(...) public {
    // ...
    tokenA.tranferFrom(maker, taker, amountA);
    tokenB.tranferFrom(taker, maker, amountB);
    // ...
}
```

Executing `transferFrom`s both parallel and sequential leads to the problem when one of the calls fails. Smart contract will not be able to fully revert `transferFrom`, can just `transfer`, but this would reset allowance.

---

**vbuterin** (2019-10-19):

Both sides would have to have tokens on the same shard as the order contract.

---

**kohshiba** (2019-10-21):

My concerns are from an application developer perspective.

Do you mean that some existing applications that support the ERC20 standard and deployed on eth1.0 will eventually need to be upgraded? If so, what should developers prepare for the upgrade? Sorry if my concerns are already answered.

---

**RockmanR** (2019-11-02):

> Sorry if my concerns are already answered.

Sorry for my lazy reply [@kohshiba](/u/kohshiba) . please have a look at this blog post, which will probably answer your question: [The eth1 -> eth2 transition](https://ethresear.ch/t/the-eth1-eth2-transition/6265)

---

**k06a** (2019-11-09):

Do you mean smart contracts should take care of storages among all the shards?

---

**nrryuya** (2019-11-19):

If you separate an on-chain order book DEX into n orders (or a hotel reservation contract into n pairs of rooms and dates), doesn’t the UI app must watch up to n shards or potentially all the shards?

Even in the light client model, this requires O(n) network bandwidth, storage, and computation.

In general, I’m curious about what kinds of applications can be “yankable.”

I agree that Uniswap is not *separable* (i.e., can not be divided into small contracts), so should not be yankable because otherwise, there would be a lot of DoS attacks or nuisances.

However, even if a contract is separable, in some cases, it should not be yankable.

Examples:

- A DEX contract, which returns an average exchange rate of the orders (e.g., for other Defi contracts)
- A hotel reservation contract, which accepts reservations only if there are more than ten rooms available

These contracts have functions that depend on the application-wide state.

Yanking allows the state of each segment of these contracts (orders, rooms) to exist in any shard, so there is no guarantee that the above functions correctly works.

Instead, each segment of these contracts can be *lockable* (i.e., can be owned by someone temporarily and unlocked by certain conditions, but its state should not be moved to other shards), so we can use two-phase-commit-like schemes for atomic cross-shard operations.

---

**szhygulin** (2019-11-22):

Can we assume that natural equilibrium state will be achieved where application that needs composability feature will be located on a same shard?

For example, if I have a share of virtual corporation (which actually is a bunch of composable smart contracts) and I want to earn interest by locking shares in staking contract, I do it on one specific shard. If I am a speculator who does frequent trading - I move shares to a DEX shard. Hence, we will see set of heterogeneous shards, but difference will be achieved by different smart contracts hosted on shards.

---

**mikedeshazer** (2019-12-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/cdetrio/48/254_2.png) cdetrio:

> You said in the post A simple synchronous cross-shard transaction protocol  that a synchronous cross-shard transaction protocol would be simple, which implies they would be easy to support. So why are you saying they’re not supported?

![](https://ethresear.ch/user_avatar/ethresear.ch/loiluu/48/1080_2.png) loiluu:

> Many innovative use cases involve interaction between several smart contracts, and that requires real composibility . Let me give a couple of examples.

Another + vote for cross-shard synchronousity (even though it’s not technically a word). I’m imagining that we’re sacrificing developer/user experience for security/scalability here, though?

Granted, all DeFi apps could just be on the same shard. So, that could work, too, but potentially without as much scalability.


*(3 more replies not shown)*

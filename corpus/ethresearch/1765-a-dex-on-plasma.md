---
source: ethresearch
topic_id: 1765
title: A DEX on Plasma
author: bharathrao
date: "2018-04-18"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/a-dex-on-plasma/1765
views: 7022
likes: 6
posts_count: 17
---

# A DEX on Plasma

Plasma MVP and Plasma Cash seem to be focused on a UTXO based coin. Although the challenges [we](https://leverj.io) face are from a DEX point of view, solving them will benefit Plasma MVP and Plasma cash as well, so this discussion will help both projects.

**Basics**

*Price Time priority:* Exchanges with an order book need to match orders with better price first, followed by orders placed earlier.

Example: If there exist sell orders (id, price, qty) of (id1, 51, 3) (id2, 52, 1) (id3, 52, 2),

when a buy (id4, 52, 5) is placed, orders with id1 and id2 are filled completely and id3 is filled partially.

*Market Maker:* A trader who provides liquidity on the platform. On many assets, the market maker is one party to almost every single trade.

**Plasma MVP Challenges**

**1: UTXO shredding** Price time priority execution means that larger UTXOs will be replaced with smaller UTXOs over time. The result of this is that all the system will rapidly tend to large number of UTXOs of the smallest possible size. A market maker’s account is likely to end up with a few thousand UTXO per hour. Gas cost for exit on individual shredded utxos may not justify its value. This will also impact the ability to take tiny fees.

**2: Exit delay too large** Traders are accustomed to withdrawing in minutes or hours. A delay of several days could be a huge UX issue. Since large traders hedge their positions and require moving large amounts of funds from a winning exchange to a losing exchange, a 2 week delay will make it hard to attract any decent liquidity into the plasma DEX

**3: Exit window too small**  It is highly likely that on detecting a maleficent operator, a huge number of UTXOs wish to exit simultaneously. The current manner of exiting would require a user to exit every UTXO they have when they detect this. An average trader may make 5 trades a day, but a market maker is likely to make 100K trades and have over a million UTXOs. It is unlikely that one week is sufficient to get all these into the priority queue. Perhaps parameterizing the delay by the exit priority queue size is an option?

**4: Exit tx too large** The gas required for finalizeExit (in OMG implementation) is likely to exceed the block limit preventing exit. At 8M gas limit and 80K gas per output finalized, a max of 100 outputs can exit. Breaking the finalizeExits into [multiple batches](https://ethresear.ch/t/minimal-viable-plasma/426/24) may be a solution if we can do this without introducing race conditions.

**Update** Batching using block numbers [suggested here](https://ethresear.ch/t/optimistic-cheap-multi-exit-for-plasma-cash-or-mvp/1893).

**5: Everyone needs to validate all Plasma blocks** This is an onerous requirement on the users of Plasma MVP. This will also endanger UTXOs of people in natural disaster areas like Puerto Rico after hurricane Maria, who may be cut off from internet service for a while.

**6: Long commitment chains** Every transfer of an UTXO increases the transaction size as it requires the [full history](https://ethresear.ch/t/minimal-viable-plasma/426/44) from the original on-chain deposit. At high transaction rates and lots of tiny outputs to spend for a payment, with market maker trading with many parties, this could complicate logic and degrade performance.

**Plasma cash**

**7: Penny wise** Price time priority matching is impractical unless everyone holds all their coins in the smallest denomination.

**Possible Solutions**

**Account Model** Most plasma issues are exacerbated because of the UTXO model. An account model eliminates many of these and lightens the impacts of the rest. Fixes *UTXO shredding*, *Long commitment chains* and *Penny wise*

**Limited Proof of Authority** A POA chain can provide instant finality. As long as the POA is strictly limited by what it can do using fraud proofs on the root chain, we have the best of both worlds. Every bad state change should be detectable and proven on root chain by anyone watching the plasma chain. An error, intentional or otherwise should halt the chain, enabling users to withdraw their coins at leisure. Fixes *Exit window too small*

**Retiring outputs** Requiring an output to be marked as *retired* would prevent that output from being included in any further transactions on the plasma chain. The only thing that can be done with a retired output is withdrawal on Root chain once retirement is confirmed on plasma block. This can eliminate the 1 week delay and improve UX. The priority queue exit would continue to exist in case the POA fails to include the retire on the plasma chain. Fixes *Exit delay too large*

**Exit Delegation** It should be possible to delegate an exit a coin to the depositor address to specialists. The delegate wont be able to spend the coin but they can only initiate a withdrawal ONLY to the depositors address. This removes the onerous requirement of having every user to monitor the chain themselves which is a barrier to entry. Fixes *Everyone needs to validate all blocks*

We have a version of plasma that incorporates the above and I will post our spec in a different thread once we work out the final kinks.

## Replies

**kfichter** (2018-04-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Price time priority execution means that larger UTXOs will be replaced with smaller UTXOs over time.

Can you elaborate on this?

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Every bad state change should be detectable and proven on root chain by anyone watching the plasma chain.

Could you also provide examples of the types of bad state changes that would be provable on-chain? The main attack vector against Minimal Viable Plasma is creating an “out of thin air UTXO” and withholding the block (but still publishing to the main chain). This *appears* to be a valid state transition and is the reason why we need the priority queue.

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Requiring an output to be marked as retired would prevent that output from being included in any further transactions on the plasma chain.

What happens if the POA marks a spent UTXO as retired and attempts to withdraw?

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Exit Delegation

I reposted some of my notes re: Exit Delegation here [Plasma (+ Delegated Exits)](https://ethresear.ch/t/plasma-delegated-exits-challenges/1770/1), feedback is welcome.

---

**bharathrao** (2018-04-18):

*UTXO shredding:* Lets say you deposited 10 eth can now have one UTXO of denomination 10. You put in a buy order for 3000 LEV tokens at price 300. The exchange needs to match the best price against your order. If the best price order is of  size 30 LEV, the exchange needs to create a partial match, splitting your 10 eth into 0.1 eth and 9.9 eth, matching the 0.1 eth to the 30 LEV and keeping 2970 LEV open. You now have two UTXOs, one for 9.9 eth and one for 30 LEV. A few more matches later, your order is filled and you have UTXOs of 30 LEV, 70 LEV, 400 LEV, 500 LEV and 2000 LEV.

Now if you decide to sell the 2000 LEV UTXO, the same process occurs in reverse. You receive 0.01 eth, 0.005 eth, 0.3 eth and so on.

You started with 1 UTXO and ended up with 25 or so with a single buy and sell. Repeat a few more times and you will only have many tiny UTXOs.

The only way you will not increase the number of UTXO is if you sold the smallest allowed UTXO.

*Bad state changes* For an account based plasma, the account is in state s1 and goes to state s2, it requires certain proof on chain. For example, your balance was 0.32 and decreased to 0.22, then it can only occur if you signed away 0.10 to someone else. At the same time the recipients balance should increase exactly by 0.10. This is sort of how eth works currently.

Withholding is not solved by our model but its detected by all and a supermajority can vote to halt the chain. The difference is that on a halted chain, there’s no rush to exit.

> What happens if the POA marks a spent UTXO as retired and attempts to withdraw?

Proof of double spend (spendtx, retiretx) would be submitted that would invalidate the withdraw and halt the chain.

> A (likely) better delegated exit model is to require users to specify a named exiter or list of exiters. The root contract could maintain some mapping (address => address) or (address => (address => boolean)) that specifies a user’s permitted exiters.

This is a simple, intuitive and robust approach. I don’t think trust issues are a big factor since smaller players can delegate to other businesses and the truly paranoid can run a chain monitoring script with only the withdrawal delegation key on a cheap VPS.

---

**kfichter** (2018-04-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> A few more matches later, your order is filled and you have UTXOs of 30 LEV, 70 LEV, 400 LEV, 500 LEV and 2000 LEV.

I think in these cases it would make sense for the UTXO owner to continuously make transactions that minimize their UTXOs. You can convert all of your UTXOs into a single UTXO in log(n) blocks. A simulated account model on top of UTXOs could also address this issue.

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Proof of double spend (spendtx, retiretx) would be submitted that would invalidate the withdraw and halt the chain.

How long would you imagine a user would have to invalidate the withdrawal?

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> This is a simple, intuitive and robust approach.

Now that I think about it, there’s actually a better approach that’s entirely on the child chain:

1. Users submit a special transaction to the child chain that names the current set of exitor.
2. Anyone can attempt to submit an exit for a user on the root chain.
3. Other users can submit a proof that the person exiting isn’t in the user’s most recent exitor set.
4. The exitor can either challenge with a more recent exitor set or, after a period of time, lose their deposit.

This way we don’t need users to make root-chain txs in order to update the exitor set.

---

**bharathrao** (2018-04-19):

> You can convert all of your UTXOs into a single UTXO in log(n) blocks

This is a cumbersome fix soaking up transaction bandwidth and fees whose only purpose is to address a design flaw. A good design should not have such burden of upkeep.

Regardless, since trading is a continuous activity, most traders will not pay to consolidate their UTXOs which will fragment again in a few hours.

Also note the burden on the exchange and plasma chain: a fill with 100 small UTXOs will soak up 100x the bandwidth of an account model.

> How long would you imagine a user would have to invalidate the withdrawal?

Actually, anyone can invalidate the withdraw since both the spend and retire are on plasma chain. If properly incentivized, validators would rush to claim the bounty as soon as the fraudulent withdrawal shows up.

> we don’t need users to make root-chain txs in order to update the exitor set.

True. However, updating exitors is probably so rare that its a tiny percent of the rootchain load and the added interactive proof is not worth the hassle.

---

**vbuterin** (2018-04-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> 2: Exit delay too large Traders are accustomed to withdrawing in minutes or hours.

Not a problem; users can sell their withdrawals-in-progress to third parties, getting coins out immediately and letting the parties that are most willing to lock up their capital take over the responsibility of waiting.

> 3: Exit window too small

This is actually significantly less of an issue with Plasma Cash, because each user can just wait until they actually need their money, or their own coin specifically gets attacked, and attacking everyone’s coins requires the attacker themselves to send a very large number of transactions.

> 4: Exit tx too large The gas required for finalizeExit (in OMG implementation) is likely to exceed the block limit preventing exit. At 8M gas limit and 80K gas per output finalized, a max of 100 outputs can exit.

How is that a problem? A max of 100 outputs can exit per block. Of course if you have more than 100 outputs you would just send multiple transactions.

> 5: Everyone needs to validate all Plasma blocks

Once again, Plasma Cash solves this. If a user has `c` coins, and there are `N` coins total, the user’s load is only about `c * log(N)` per block.

> 6: Long commitment chains Every transfer of an UTXO increases the transaction size as it requires the full history from the original on-chain deposit.

This is true only in Plasma Cash; in MVP you don’t need to pass around history data as everyone has the entire Plasma chain anyway. To mitigate this in Plasma Cash, you can add a mechanism where you can “commit” a coin to chain (think of this as an optimized equivalent of withdrawing and then immediately re-depositing), using one on-chain transaction to reset the history length of the coin to zero.

---

**kladkogex** (2018-04-19):

Our startup is working on a solution that has overlaps with plasma idea-wise (we also use map-reduce philosophy) but our chains are EVM-compatible asynchronous consensus chains (not UTXO).

We also use a bit different mechanism (threshold signatures) to communicate between the chains.

We hope to become a good member of Ethereum community once we release our test network on Oct 1, and contribute to well being of Ethereum  ecosystem as much as we can !

Since you are interested in running DEX let me know  if you are interested in trying our  our prototype  once it is ready - since we run EVM on our chains we target applications such as DEX.

---

**bharathrao** (2018-04-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> users can sell their withdrawals-in-progress to third parties

Is this mechanism explained anywhere? Im guessing the user would transfer his UTXO to the service provider and get paid out of band on a different chain? Would this be trustless? Adding third parties to solve a problem reduces overall appeal. Pretty much every large trader has told me that they love centralized exchanges precisely because they only have one party to deal with, whose risk characteristics are very well known. Our goal is to model plasma as a single entity that anyone needs to interact with just like eth/btc/ltc etc.

> the user’s load is only about c * log(N) per block

The emphasis is on *everyone*  not *all blocks*. Ideally, any one who can see plasma blocks should be able to enforce correctness, not just the victim. In case of ethereum for example, miners will reject an invalid transaction and the responsibility to prevent unauthorized spends does not rest solely on the owner.

---

**bharathrao** (2018-04-19):

We are most definitely interested.

I’ll also post our Account based plasma spec which may be of interest to other folks building DEXes

---

**vbuterin** (2018-04-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Is this mechanism explained anywhere? Im guessing the user would transfer his UTXO to the service provider and get paid out of band on a different chain? Would this be trustless?

The third party in question could possibly be the exchange themselves; and yes, in either case it would be trustless. A withdrawal-in-progress is an on-chain asset, so there’s no technical obstacle to changing its ownership, and there’s zero risk to the seller, who can just get their money out immediately. The buyer would just need to have themselves verified that the coin that is exiting is legitimate, to be sure that the withdrawal could not be challenged.

> The emphasis is on everyone not all blocks.

Keep in mind that maintaining security for a user only requires logging on once per withdrawal period. It definitely does not require you to be online anything close to constantly.

---

**bharathrao** (2018-04-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> there’s no technical obstacle to changing its ownership,

Right, we could do this as a time arbitrage implemented as a deposit lock plus swap

step 1. the exiter requests a UTXO time arbitrage

step 2. A time arbitrageur deposits UTXO size minus fee timelocked

step 3. Atomic swap(?) of Plasma UTXO to arbitrageur and onchain UTXO to exiter

step 3. If exiter did not exchange within N blocks the deposit is released.

An issue here is that when market is moving fast, the arbitrageur probably will run out of funds on chain because most of the money is a uni-directional move (out of plasma chain).

Ideally, there are only two roles: a buyer and seller. The plasma contract which is for all practical purposes a public utility does the rest. Requiring an arbitrageur to exist who is ready with large number of on-chain funds at any time makes it fundamentally unattractive to be a plasma market maker. This is assuming there are no fees. If the arbitrageur tacks on fees, then it may not even be economical to market make on the plasma chain.

Fundamentally, Im skeptical of introducing brand new roles to solve every new problem because the more kinds of roles that are required for the smooth functioning of the system, the less reliable and stable it is. To me, this feels like a hack. This is just us claiming “lets put a banker who does XXX” to address a hole in the system design.

A robust elegant design is like that of say ethereum: You only need two actors. A sender and receiver. You only need the sender to be online. Such systems are robust. Risk is flat. A system that require others to run an ancillary business model already in place for viablity is a weak fragile system in my opinion.

---

**zack-bitcoin** (2018-07-19):

I wrote a trustless market enforced using channels.

For the “price time priority” problem, I have the market match trades in single price batches.

It is better to only use 2-party channels for this problem, and instead of trading subcurrencies directly, to trade a synthetic asset priced in Eth.

You can connect many 2-party channels into a market using techniques similar to hashlocking.

You can recover liquidity locked in network hubs by trustlessly moving bets from indirect paths to direct ones. Hashlocking allows for this.

---

**bharathrao** (2018-07-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/zack-bitcoin/48/5449_2.png) zack-bitcoin:

> match trades in single price batches

How can this prevent the matcher from excluding certain orders from a batch and matching them in a future batch where the price is adverse to the order?

---

**zack-bitcoin** (2018-07-19):

The server running the market is required to declare the price periodically.

If the server fails to publish a price for too much time, or if the server publishes prices too frequently, then the server loses every bet it has in the market.

If I can prove that the server published prices too frequently, or if I can prove that the server didn’t publish prices frequently enough, then I win the bet. It doesn’t matter which way I bet, I still win.

Bets are matched at the earliest price possible.

So if you are willing to pay up to 0.6 per share, then you will match at the earliest price below 0.6.

I wrote more about this here: https://github.com/zack-bitcoin/amoveo/blob/master/docs/design/limit_order_in_channel.md

---

**Equilibrium94** (2018-08-18):

I’m interested in that as well. Do you guys have a whitepaper or a demo?

Thanks!

---

**MihailoBjelic** (2018-08-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> a supermajority can vote to halt the chain

What exactly do you consider a supermajority? Can you please explain how this works?

---

**tuna** (2018-09-21):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Since you are interested in running DEX let me know if you are interested in trying our our prototype once it is ready - since we run EVM on our chains we target applications such as DEX.

[@kladkogex](/u/kladkogex) I am interested. Would love to see a link access to what you have done on this. Many thanks.


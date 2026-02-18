---
source: ethresearch
topic_id: 3931
title: Gluon Plasma Full Spec for Non-custodial Exchanges
author: bharathrao
date: "2018-10-25"
category: Layer 2 > Plasma
tags: [new-extension]
url: https://ethresear.ch/t/gluon-plasma-full-spec-for-non-custodial-exchanges/3931
views: 8909
likes: 8
posts_count: 30
---

# Gluon Plasma Full Spec for Non-custodial Exchanges

This is a followup post on “[A DEX on plasma](https://ethresear.ch/t/a-dex-on-plasma/1765/17)” from Apr’18. We have gone through many iterations and have what we believe is a production quality spec. Note that ours is designed for trading and not UTXO payments like almost all other specs here.

Our focus is weighted with UX, Scaling and Security in that order.

UX is the primary driver since we are building a business, not just engaging in technical research. Most of our choices were based on pragmatic conditions of the market and user base today. For example, we realized that exit games are a non-starter because although they work, even many tech-savvy users would avoid such exchanges at the current time. Our users were also confused why they have to deposit a heavy bond to take out their own money.

Scaling was the next primary driver. We aimed for sub-linear cost in terms of gas, storage and computational load with increasing volume. Without this, the platform becomes self-limiting as gas costs drive traders elsewhere. Scaling also feeds into security since super-linear cost would make it practical to overwhelm any validators with long chains of transactions, dust trades and other attacks whose impact is amplified by high activity.

Security is last but not the least. It is intertwined with the two needs above. We needed a security model and proof so that the model could be examined and any gaps speedily addressed.

**Read the full [Gluon Plasma paper](https://leverj.io/GluonPlasma.pdf) to understand our motivations and drivers.**

**Top features:**

1. Offline Recipient
2. Instant finality on plasma chain
3. Fast withdraws (< 1 hour)
4. Fungible
5. Unlimited number of coins
6. Unlimited trades per block
7. Light nodes
8. Compact fraud proofs
9. Ethereum Network Congestion tolerant
10. Security Model/Proof
11. Watchtower-free
12. Exit Game-free
13. Challenge/Response-free

**Ok, so what’s the catch?**

Data Unavailability is not yet eliminated. A governance token is used to vote for a chain halt if the operator turns maleficent. **SEE UPDATE BELOW**

**Security Proof Outline**

A payment network is secure if the following constraints hold for every transaction:

1. The recipient can receive the payment directly.
2. The sender’s provable intention is required to send the payment.
3. The amount received is exactly the amount sent.
4. Network participants can verify validity according to consensus rules.

If it can be shown that every state change enforces the above, then the network is safe. The above needs to be enforced at 3 levels:

1. All steps of the protocol, which is the interface between the main chain and plasma chain
2. Plasma ledger entries
3. Plasma chain, which is the arrangement of plasma ledger entries.

I ask the reader to [read the full paper](https://leverj.io/GluonPlasma.pdf) since the protocol and the fraud proofs together make the system, so listing just the protocol here would be a disservice.

**Guide to reading the paper: What each chapter speaks about**

3: Deriving account model from UTXO model

4: How Exchange security models work

5: Why we needed a different plasma flavor

**6: Gluon Plasma fundamentals**

7: Gluon Plasma characteristics (is this flavor suitable for your project?)

**8: Gluon Plasma Protocol**

**9: Fraud Proofs**

Appendix A,B and C: Proofs of safety and custody

**Your improvements and critical feedback is highly appreciated!**

**UPDATE:** Joey Krug suggested we replace the POA with [tendermint consensus](https://tendermint.com/static/docs/tendermint.pdf) POS. We realized that if we decouple the exchange and consensus (ie block committer) roles, we can eliminate data unavailability:

1. Exchange(s) creates transactions.
2. Tendermint POS committers create blocks from transactions.
3. If exchange withholds data, POS validators will simply not commit any more blocks.
4. If at least 1/3 of the POS validators collude with the exchange and duplicitously commit a block while withholding data, other POS validators can slash their deposit (which needs to be hefty).

Regarding 3. Chain is abandoned and halts when there is a single exchange on the plasma chain. On a multi-exchange chain, the byzantine exchange is ejected and trades in its block are effectively rolled back. Other exchanges can continue to operate. Multi-exchange feature is not yet finalized.

A single exchange Tendermint POS can probably be implemented without much impact.

## Replies

**sg** (2018-10-26):

How strong the security is? Same guarantee with Plasma Cash, or MoreVP?

---

**ritikm** (2018-10-26):

Thanks for sharing.

At first glance this construction sounds like an account-based version of Plasma MVP with extremely frequent checkpointing (every G-block is effectively a new checkpoint since you can’t challenge any prior G-blocks). This makes the data storage requirements low (only need to store one G-block’s worth of data), but liveness requirements extremely high (there needs to be at least one honest, incentivized verifier checking every transaction in every G-block with no downtime).

Couple questions:

Is there a concept of trustless atomic swaps? Based on the description and the table in section 6.5, it looks like account A_1 trades 0.05 Z_1 for 0.02 Z_2, which is done across two transactions (state 2 and 3). What happens if the operator decides to withhold state 3 and A_1 is left with nothing? Or consider a case where the two transactions are at the edge of the G-blocks (one is the last one in G-block N and the other is the first in G-block N+1) and G-block N+1 is deemed invalid (so the chain has halted). Half my swap has now been confirmed and I’m forced to exit the sidechain with nothing.

Once a G-block is submitted, how long is the period before another G-block is submitted (and thus the previous G-block is now considered confirmed and unchallenge-able)?

Who is responsible for validating G-blocks? If users of the DEX are expected to validate, it sounds like they have a huge burden of running nodes themselves to run the validation process across *all transactions that are happening across the DEX*. If it’s a separate, limited validator set, how are they incentivized to do the validation?

---

**themandalore** (2018-10-26):

Great work Leverj guys, I’ve always wanted to see more account based implementations.  A few questions:

- Is there a max size to your G-block?
- How is the voting size calculated?  I know you do derivatives, so in a world where a lot of players could lose a lot of money very quickly, how do you prevent them from halting the network and what’s the threshold that it becomes insecure?
- Is this really that much different than MVP?  You’re just verifying something different (accounts vs transactions)
- Who are the witnesses and how do you incentive them?

And lastly, is there code anywhere or places we can contribute?  I think some tweaks to the MVP repo and you could get something testable in a pretty short time period

---

**bharathrao** (2018-10-26):

> there needs to be at least one honest, incentivized verifier checking every transaction in every G-block with no downtime

This is correct. However, validators are not expensive to run and since we are an exchange, the market makers will surely run multiple redundant validators to protect their large balances.

> Is there a concept of trustless atomic swaps?

All trades are atomic. A trade execution results in four *Trade* entries (plus any *Fee* entries). The entire set should be committed into the same G-block.

> Once a G-block is submitted, how long is the period before another G-block is submitted (and thus the previous G-block is now considered confirmed and unchallenge-able)?

If fast withdrawals are desired, could be as low as 10 minutes. Generally most fraud is detected right after an entry is created and much before they go into a block.

> Who is responsible for validating G-blocks?

There are separate validator programs. The validation load is not that high since the validators only need to store the last (A,Z) entry. If they can prove fraud and halt the exchange, they get a bounty. Truebit suggested that occasional random minor bounties should be paid at regular intervals and this is a good idea. We will hold validation games on testnet to see what model works best.

---

**bharathrao** (2018-10-26):

> Is there a max size to your G-block?

no

> How is the voting size calculated?

Voters need to stake LEV tokens to vote. Voting to halt costs 10% of their staked tokens. Any losses they offset by halting the chain would mostly be lost in the LEV they sacrifice. Can they pre-plan to buy a lot of LEV when its cheap, stake it in the hope that if the market moves against them there is an economic tradeoff to halt the chain? Perhaps. But they wont be able to do this repeatedly.

Realistically, if say the top 3 or 4 market makers decide to halt the chain, it will probably halt. However, this would require a sudden sharp move (say a 50% price drop in 10 minutes) and would require all market makers on the losing side. We calculate that an unreasonable halt is very unlikely, on the order of once a decade, just like the fiat markets.

> Is this really that much different than MVP? You’re just verifying something different (accounts vs transactions)

MVP was great. It gave us a good foundation of whats possible. Much thanks to Vitalik and Karl (and the OMG team) for their hard work.

All flavors of plasma essentially driven from the same principles behind plasma classic. However, there are some UX differences in our flavor that are important for trading vs just coin payments:

1. No exit games, making adoption easier
2. A transaction when visible has finality way before its committed to a block. This means you can sell what you bought milliseconds ago or hedge or place stop orders etc (very important in leveraged trading).
3. Account model makes trading practical while UTXO based trading is excessively cumbersome and I have never seen one that has gained traction.
4. Trade with API keys, which allow trading but not withdraw. Any system without this feature will not attract marketmakers.

> is there code anywhere or places we can contribute?

We will opensource contract code soon. Thanks for your interest! PM me if you want to spend a significant chunk of time on this project.

---

**bharathrao** (2018-10-26):

Good question. I’m not sure if there is a way to quantify security.

Perhaps someone can come up with a model to evaluate risk scores. something like: % of funds at risk * probability of loss. Some initial thoughts:

Risk Ranking:

In my opinion, the highest threat to security are

1. total loss of chain funds: everything on the chain is stolen by an anonymous network participant
2. total loss of a single account by anonymous network participant
3. total loss of chain funds stolen by the operator
4. total loss of a single account by operator
5. minor losses due to bad fills/skimming/front running by anonymous participant/miner
6. minor losses due to operator

Protocols where the victim needs to detect and issue a challenge have lower safety compared to ones where anyone can challenge.

Protocols where challenges are issued after initiating an exit game are susceptible to spam attacks and less safe than challenge-free protocols like Gluon plasma.

Having the operator answer challenges is susceptible to an overload attack where hundreds of dust outputs require challenge and a huge one is hidden among them hoping to overwhelm the operator.

I think in general, challenge stuff does not scale and relies on network usage being low and miners not cooperating with attackers.

Gluon plasma avoid all these issues by design.

---

**ritikm** (2018-10-26):

Thanks for the quick response. Few more follow-ups:

> This is correct. However, validators are not expensive to run and since we are an exchange, the market makers will surely run multiple redundant validators to protect their large balances.

How does this protect anyone not running a validator (e.g., smaller, infrequent traders)? Relying on a small set of validators who have a lot at stake (either through LEV tokens or large balances on the DEX) is fine, but sounds closer to the kind of protection a Proof-of-Stake system would have vs. a construction like Plasma Cash.

This also begs the question of why go through the trouble of committing block hashes back to Ethereum. If the system relies on a group of validators to find fraud, you could just run this as a non-Plasma sidechain where assets are locked up on Ethereum, you have a limited Proof-of-Stake based validator set that achieves consensus amongst themselves around which blocks are legitimate and final, and you have a bridge to take assets back and forth between Ethereum and the sidechain. Is the only benefit of Plasma-fying this construction for users to have the “Exit Asset Balance” option?

> All trades are atomic. A trade execution results in four  Trade  entries (plus any  Fee  entries). The entire set should be committed into the same G-block.

How do you prevent the operator from withholding one of the Trade entries? What incentive does a validator have to detect such an issue if they’re not directly involved in the trade? Consider a case where there’s a small-time trader A_1 trading 0.1 Z tokens and a market maker A_2 who has 1,000,000,000 Z tokens and runs a validator node. If A_2 detects operator malfeasance, A_2 realistically won’t call it out since it’s such a minuscule error (0.1 Z worth) vs. her own holding (1,000,000,000 Z). It’s not worth the burden of having to deal with a halt, exit, and restart unless the bounty for finding such fraud is *extremely* high.

> No exit games, making adoption easier

Exit games still exist in this construction, albeit in a different way. Any “Withdraw” ledger entry included in a G-block should be treated like an exit and must be validated by all users to ensure that excess funds aren’t being withdrawn. In your construction, I see two differences vs. a traditional Plasma MVP construction: (1) you have a limited validator set that’s doing this validation instead of every user, which is trading off some level of security for usability, and (2) the challenge window is much shorter (10 minutes based on your recent post) as it’s limited to the time until a subsequent G-block is published. (Note that both of these points are also possible to implement in a Plasma MVP/Cash construction for the same set of tradeoffs.)

> A transaction when visible has finality way before its committed to a block. This means you can sell what you bought milliseconds ago or hedge or place stop orders etc (very important in leveraged trading).

Isn’t the risk here that trading halts in the event of a flash crash (because the few largest accounts, who have the most to lose, effectively control the decision to halt the sidechain and revert the last uncommitted G-block)? Agreed that this is a black swan event since only the last G-block can be reverted, which would mean that a large amount of money would have to be lost in the short time window of one G-block. Gradual losses of capital over several G-blocks should not trigger such an event.

---

**bharathrao** (2018-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/ritikm/48/2541_2.png) ritikm:

> system relies on a group of validators to find fraud

*Anyone* can run a validator, find a fraud and submit a fraud proof to the plasma contract. A fraud proof does not require staking or LEV or even participating in trading to halt the chain. The only reason to stake is to vote when data is unavailable, ie everyone is probably getting screwed over because the root commitments dont match.

> What incentive does a validator have to detect such an issue if they’re not directly involved in the trade?

Validators get bounties for halting the chain.

> Consider a case where there’s a small-time trader A_1 trading 0.1 Z tokens

There are very few frauds that A_1 himself cannot submit a proof on. Regardless, the moment A_2 or anyone detects the operator is compromised and even a single trader is defrauded, the only course of action to take is to halt the chain. If the operator steals 0.1 from A_1, then A_2 knows his entire balance is at risk. Its much much cheaper riskwise to sacrifice 10% of governance tokens which will probably be worthless soon than to hope that the operator’s strategy is to only steal pocket change from small players. (This does not seem to be a reasonable line of thought, fwiw.)

> Exit games still exist in this construction

Exit games are interactive steps mediated by the smart contract and have the following issues:

1. can be manipulated by spam attacks to prevents the other party from responding in time
2. Possibly get miners to exclude challenge responses.
3. A sudden surge of challenges that empty eth preventing you from challenging more claims.

Non-interactive proofs are not games in the sense that once submitted, there is little room for manipulation.

> (1) you have a limited validator set

Quite the opposite. MVP validation is onerous: every user has to validate the chain every week or they are at a risk of loss. Any system where only the victim can protect himself is weak. In Gluon, a *single* validator provides security for *everyone*. This is far more robust than MVP

> (2) the challenge window is much shorter

The challenge window *can be* shorter in Gluon with the same safety because unlike MVP, every user does not need to validate the full history. Detection of frauds in Gluon immediate on seeing a new entry,  even before it goes into a block. In MVP, you would need to trace the history of every coin. Imagine doing that in a high volume exchange, where UTXO shredding has created millions of UTXOs per user. it could take days before you figure out that one of your million utxos with 1 million transfer history has a fraud 900K transfers ago.

> Note that both of these points are also possible to implement in a Plasma MVP/Cash construction for the same set of tradeoffs.

A 10 minute MVP will implode since one can create a fraudulent coin whose history takes longer than 10 minutes to verify. Plasma cash in non-fungible, leading to a knapsack problem when trying to construct transactions that match desired quantities.

> Isn’t the risk here that trading halts in the event of a flash crash

The minuscule risks of a black swan chain halt are a lot more appealing than trying to exit 100 million utxos via a priority queue on 8M gas limit. Im simply not convinced that its a feasible approach.

Data unavailability is the ugly stepchild of plasma. No solution here will be perfect. Its all about tradeoffs and we have taken the one thats best for our domain. Nevertheless, we are working on addressing the data unavailability problem in other ways. Perhaps some of the smart folks on this forum will find a compact/succinct proof we can submit with the new block eliminating this issue.

You seem to be interested in a MVP/ Gluon comparison. Perhaps we can create a separate forum comparing different flavors of plasma. Each flavor has its own applications and MVP is OK for payments but is utterly unsuitable for trading exchanges:

1. How will you match 500 Z1 to 300 Z2 when both are made of 100K UTXOs each?
2. How many tx do you need to fit at 2 inputs and 2 outputs per tx?
3. How can you place an order and close your laptop?
4. How do you co-ordinate a trade between two users to do the trade as above?
5. Why will a user sign a trade first if the second will walk away unless the price move in their favor?
6. I’ve signed the trade for atomic swap. I hope the other party signs it. Now what? Should I hedge my position? How long should I wait before cancelling my hedge?
7. Im a market maker trading every millisecond. How do I “periodically validate the chain”
8. Gas price is suddenly high and blocks are full? My challenge was submitted with low fees!
9. There’s 10 icos going on today and I discovered that operator defrauded me. The gas fees is higher than my account value!
10. How do I tell everyone that the operator has defrauded me? Send them a million utxo history?

… and oh … how do you enable leveraged trading on MVP/Cash?

---

**sg** (2018-10-26):

I’ve glanced your paper.

The fast withdrawal construction implies “if the operator is Byzantine, then users cancel orders and exit”. But the order cancellation might not be executed because the op is Byzantine.

1. Is this assumption correct?
2. Who is running the Orderbook?
3. Were any fund safety guarantees discussed regarding order cancelation?

---

**bharathrao** (2018-10-26):

> Is this assumption correct?

If the operator fails to cancel orders of someone exiting directly from the smart contract, this can be detected and proven via “Exit Insolvency Fraud proof”

> Who is running the Orderbook?

The operator

> Were any fund safety guarantees discussed regarding order cancelation?

Order creation, modification and cancels do not impact custody. Every exchange needs to be able to cancel orders for any or no reason, for example: to shutdown for maintenance, delisting an asset, etc.

Holding users canceled orders and filling them adversely is detected by the “price time priority fraud proof”.

---

**ritikm** (2018-10-27):

> There are very few frauds that A_1 himself cannot submit a proof on.

This would require A_1 to be live and running a validator node, which sounds impractical for 99% of users no matter how light-weight the validator node is (have to download separate software, keep it always running, etc.)

I can see having a separate group of people, who have much more at stake in the DEX, running these validator nodes with a TrueBit-style incentive scheme. Again, this is possible in Plasma MVP/Cash as I describe below.

> Exit games are interactive steps mediated by the smart contract and have the following issues:
>
>
> can be manipulated by spam attacks to prevents the other party from responding in time
> Possibly get miners to exclude challenge responses.
> A sudden surge of challenges that empty eth preventing you from challenging more claims.

Unclear what you meant by #3, could you please clarify?

The first two problems are not mitigated in Gluon. Consider a case where a G-block with fraudulent transactions has been submitted (e.g., a “Withdraw” transaction with the wrong amount of Z tokens). Validators will be able to catch that problem quickly, but will have to submit the fraud proof on-chain. The first two problems you mention still hold:

1. Spam attacks on-chain could prevent a validator from submitting the fraud proof or halting the chain in time (before the next G-block).
2. You can get miners to exclude the fraud proof or the voting process to halt the chain.

> Non-interactive proofs are not games in the sense that once submitted, there is little room for manipulation.

How is this different than existing Plasma constructions? What kinds of “manipulation” are you referring to that Gluon prevents vs. MVP/Cash? Per your whitepaper, it seems like if fraud is detected, it results in a vote to halt the chain (the equivalent of a “challenge”). In MVP/Cash, challenges are issued against individual exits, which prevent the exit from going further. The definitions and outcomes of a challenge may be different, but the requirement of monitoring the operator and on-chain proofs is the same.

> Quite the opposite. MVP validation is onerous: every user has to validate the chain every week or they are at a risk of loss. Any system where only the victim can protect himself is weak. In Gluon, a  single  validator provides security for  everyone . This is far more robust than MVP

Dissecting this further:

It seems like only having one validator provide security for everyone is possible because of an *account-based scheme* as it reduces the amount of data the validator needs to check through, making it feasible for one validator to do the job for everyone. Looking at the implementation of the account-based scheme in your whitepaper, it seems like it’s modeled as a UTXO-based system, where each user has one UTXO per token type (the token’s balance) with on-chain checkpointing effectively happening every G-block. By having each G-block act as a checkpoint, you remove the need to store the UTXO history because anything before the G-block is unchallengeable, and so so there’s no point in storing the history.

You can get a similar benefit with MVP and Cash if you exit the coin and deposit it back to the Plasma chain (“checkpointing”). Of course, doing so is much more inefficient, so having the operator do the checkpointing (reducing the UTXO set to a single balance every time, i.e. an account-based system) without requiring a round-trip cost of going on-chain and back off-chain is a clever optimization. This does require an honest set of validators that have much more stringent requirements to verify correctness of each G-block to ensure that the operator is not acting maliciously. I believe the Plasma MVP/Cash constructions were made to not have any reliance on third parties. There is a perceived security benefit with the MVP/Cash model (each user is responsible for their own security so no need to trust any third party), and there’s a practicality benefit with Gluon (trust a group of incentivized third party validators to do the job since they have something on the line as well).

> Detection of frauds in Gluon immediate on seeing a new entry, even before it goes into a block. In MVP, you would need to trace the history of every coin.
> […]
> A 10 minute MVP will implode since one can create a fraudulent coin whose history takes longer than 10 minutes to verify.

The benefit you’re touting in Gluon is because of the requirement of always having one live, incentivized, honest validator. This lets any validator (even a new one that just joins the network) assume that everything up until the last G-block does not need to be re-validated. This argument also holds in an MVP world. If you have the same validator requirement, you could have the validator creating checkpoints (the equivalent of G-blocks) that reduce the amount of data someone doing transaction history verification in the future needs to analyze (it would only be data from the latest checkpoint onwards). The key point here is that this is only possible if you introduce a requirement of a live, incentivized, honest validator.

> Plasma cash in non-fungible, leading to a knapsack problem when trying to construct transactions that match desired quantities.

Be on the lookout for Plasma Cashflow, which solves this problem.

> How will you match […] million utxo history?

I’m curious what your answers are for each of these questions with Gluon as that’ll elucidate some of the tradeoffs you considered and how you made you decision. I’m sure some of them are scattered in the whitepaper, but would be good to get it succinctly included here.

–

(All of this is not meant as a knock to the Gluon construction. It describes a clever, practical Plasma abstraction and is similar to many of the things we’re doing in our Plasma construction to make things more practical. My goal here is to dig deeper to understand the nuances and motivations behind some of the decisions taken, especially as we’ve considered many of these ourselves.)

---

**bharathrao** (2018-10-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/ritikm/48/2541_2.png) ritikm:

> Who is responsible for validating G-blocks? If users of the DEX are expected to validate, it sounds like they have a huge burden of running nodes themselves to run the validation process across all transactions that are happening across the DEX .

Since every (A,Z) is a separate chain, validation can be sharded:

1. Every user can choose to validate only the assets they are interested in and shard by Z
2. Validators can shard by account only (shard on A)
3. Full Validators can use a LRU cache to listen to only listen to recently active users or only listen to market makers, etc.

We havent thought of optimization in depth at this point.

---

**bharathrao** (2018-10-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/ritikm/48/2541_2.png) ritikm:

> This would require A_1 to be live and running a validator node; impractical for 99% of users

Various optimizations and sharding may enable light validation within the trading client itself

> The first two problems are not mitigated in Gluon.

Ways to Spam MVP that is not possible in Gluon:

1. Gluon can ignore dust deposits. MVP can be spammed by millions of dust deposits which will create millions of deposit blocks. This can overwhelm all participants
2. Gluon needs a single fraud proof to have high enough gas to attract a single miner to mine the tx and everyone is safe. On MVP every fraud needs a separate challenge.for every utxo thats trying to exit. There could be a million fraudulent exits in a few minutes. There is no way every single challenge will hold.

> it seems like if fraud is detected, it results in a vote to halt

No, fraud proof submissions are separate from vote to halt. Fraud proofs are for provable frauds. Voting is for unprovable frauds (ie data unavailability). Both will halt the chain. Data Unavailability is a research topic and we may find a way to eliminate it. Voting to halt is the current best approach to dealing with it.

> you can get a similar benefit with MVP and Cash if you exit the coin and deposit it back to the Plasma chain

Will never happen because UTXO shredding guarantees everyone will have many tiny outputs and this becomes uneconomical.

> There is a perceived security benefit  … each user is responsible for their own security

This is a security weakness, not a benefit. Would you say Bitcoin is more secure if everyone had to verify their coin every week?

> This argument also holds in an MVP world.

Your point seems to be that MVP and Gluon are similar. I will say yes, all plasma flavors are similar.

> would be good to get it succinctly included here

Until you can answer those questions, my advice is don’t attempt writing a DEX on MVP. This is simply because building something in a specialized domain needs experience in the domain.

Your line of questioning tells me you sense something very unique about Gluon and you are asking yourself “Why this is different? Couldn’t they have just done this in MVP?”

The simple answer is NO. Plasma MVP and Plasma Cash (which were the only flavors when we began) wouldn’t work. Nor would many others that have been spawned since. The UX would be terrible and there would be no traction. We have built financial systems for decades and really loved the bright idea that is plasma. However, it was obvious that no plasma flavor was suitable for trading. So we tailored Gluon for the UX of trading systems.

---

**ritikm** (2018-10-27):

To summarize:

- There’s a requirement of an always-live group of validators that every single user must trust, or elect to join, in Gluon which is a critical component to making this work and does not exist in existing Plasma constructions.
- By having this requirement, you can operate an account-based system and have frequent checkpoints, called G-blocks in Gluon, which reduce the burden of transaction history verification to a limited window of time.

---

**bharathrao** (2018-10-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/ritikm/48/2541_2.png) ritikm:

> always-live group of validators that every single user must trust

You make it sound like a country club. Validators act individually completely oblivious of others if any. They dont all have to be always live. You just need at least one of them live at any point in time. Nothing prevents people from starting to validate and stopping at random times. If a 10000 people do this for a random hour a day, theres a very solid chance that at least one will be live all the time.

You are focused on the history and verification stuff, which I think is the least important part. Why do we have rock solid safe DEXes that no one uses while Bitfinex is still one of the top exchanges?

Gluon is a plasma that prioritizes providing UX similar to centralized exchanges and can scale with volume. Its designed to attract liquidity, whereas other DEXes are designed to repel it. It then adds provable safety, which even many DEXes dont have.

So I would summarize this way:

- Gluon solves the DEX liquidity problem by enabling a centralized-like latency and UX
- Gluon solves the DEX scaling problem by being spam resistant and congestion tolerant
- Gluon adds provable security, which no exchange of its speed has ever had.

---

**bharathrao** (2018-10-31):

I’ve added Joey Krug’s suggestion of Tendermint consensus (see update to original post), this should address your concern about having to trust an always live group of validators. Perhaps other approaches can be taken such as Dfinity’s 423 with aggregate signatures.

---

**yan** (2018-10-31):

A few concerns:

1. The functionality for a DEX includes maintaining an orderbook of all orders and matching orders from the top of the orderbook when there is a match. The protocol for the Gluon sidechain provides more like a general trading functionality that enables clients to simply send money to another client instead of a DEX. And since transactions are processed by a single operator, it is much easier for the operator to mount front-running than in ordinary DEX where front-runners still need to compete by gas price.
2. The design of voting to halt is vulnerable to Denial-of-Service attack. An attacker only needs to vote to halt with a small size each time and make finality time for the sidechain very slow.

Please let me know if I misunderstood anything. Thanks!

---

**bharathrao** (2018-11-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/yan/48/2602_2.png) yan:

> it is much easier for the operator to mount front-running than in ordinary DEX

This would be correct. However, a central limit order book’s behavior is deterministic and any discrepancy is immediately obvious. A fraud proof can be submitted as  described in S9.3.5.

> An attacker only needs to vote to halt with a small size each time and make finality time for the sidechain very slow.

If the voted amount is too small, it may just delay by one ethereum block (15s), which may not even be noticed. The delay response is stronger if they vote all their tokens at once rather than a bit by bit every block. Only deposits and withdrawals are slowed during the delay, normal trading can progress unnoticed. This would be similar in UX to centralized exchanges today.

They can slow down the chain, but it will cost them 10% of their tokens every time they vote. A hypothetical denial of service attack would cost them a significant chunk of money to delay the blocks by more than an hour. They would have to buy a large number of tokens on the open market to effect a large delay (say one day). The buying pressure would spike the price of the tokens making the attack economically self-limiting.

If no one else joins their vote, then they lose tokens. It is unlikely they will be able to keep this up for long.

Economically, its equivalent to a miner mining empty blocks on your chain. Most of it will be unnoticed. Some of it will happen longer than normal occasionally and it can be annoying, but it would be prohibitively expensive to run a sustained campaign.

---

**yan** (2018-11-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> However, a central limit order book’s behavior is deterministic and any discrepancy is immediately obvious. A fraud proof can be submitted as described in S9.3.5.

This is still not detectable, especially when the DEX aims to scale up and have a large popularity. The orders have to be timestamped by the operator because clients’ local time cannot be trusted. Then if an order is timestamped by the operator, certain network delay should be tolerated and this gives space for the operator to inject their own orders.

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> They can slow down the chain, but it will cost them 10% of their tokens every time they vote. A hypothetical denial of service attack would cost them a significant chunk of money to delay the blocks by more than an hour. They would have to buy a large number of tokens on the open market to effect a large delay (say one day). The buying pressure would spike the price of the tokens making the attack economically self-limiting.

Do honest large stake owners have to lose 10% of their tokens every time they vote? If so, this sounds like a discouragement for them to vote to halt when data is unavailable while their own profit is not affected. In addition, since delayFunc takes in voteTally as a parameter, which is accumulative, an adversary’s prior vote has a long-term accumulative impact on delaying the commitment of a new Gluon block. I didn’t mean this reduces the throughput of the sidechain, but this does increases the finality time, which was supposed to be a pro of the design.

---

**bharathrao** (2018-11-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/yan/48/2602_2.png) yan:

> This is still not detectable,

This is absolutely detectable on all central limit order books including centralized/fiat exchanges of today. It may not be *provable* in many instances. The victim and anyone else who can see the victim order will basically see the price move *through* the victim order and fill a different order at a worse price. i.e. If you had a limit buy at 200, the price will fill 199 before filling your order.

![](https://ethresear.ch/user_avatar/ethresear.ch/yan/48/2602_2.png) yan:

> The orders have to be timestamped by the operator because clients’ local time cannot be trusted.

Orders are timestamped by the user AND the operator. The users order timestamp serves to ensure the operator is time-stamping accurately. The operators timestamp serves as the single clock of reference for a price time priority proof. A small clock skew is tolerated to ensure variable ping delays.

As a practical matter, the user clock is adjusted from the server price feed and the skew is adjusted automatically, so for all practical purposes the requests will have nearly same timestamp as the server.

![](https://ethresear.ch/user_avatar/ethresear.ch/yan/48/2602_2.png) yan:

> Then if an order is timestamped by the operator, certain network delay should be tolerated and this gives space for the operator to inject their own orders.

Note that front-running requires the deployment of capital and the smaller the price movement, the larger the capital allocation that is needed to make the same amount of profit. Large ticks on futures products ensures that even if the underlying spot market moves a bit (due to 6 decimal places) the futures product is unlikely to move (due to 1 decimal place) within a span of a few milliseconds. While there is a theoretical possibility of operator frontrunning in the skew tolerance (difference between user and server clock), the profit collected would be so small that its not economically attractive to deploy a huge amount of capital for it; it would be more attractive to just lend it at interest.

![](https://ethresear.ch/user_avatar/ethresear.ch/yan/48/2602_2.png) yan:

> sounds like a discouragement for them to vote to halt when data is unavailable while their own profit is not affected.

When data is unavailable in Gluon Plasma, it affects all users since the rootHashes wont match and they won’t be able to exit. Also note that if the operator steals from one person, everyone else should know they are next and the only rational course is to halt the chain.

> Do honest large stake owners have to lose 10% of their tokens every time they vote

If the operator is compromised, there is a very good chance that the governance tokens are nearly worthless in a few hours. Its better to sacrifice 10% of them and save other assets. On the flip side a malicious person would be discouraged from voting falsely or carelessly since they would have to pay with valuable tokens.

> an adversary’s prior vote has a long-term accumulative impact

Everything is reset when a new G-block is created.

> but this does increases the finality time

Perhaps there is a chance that someone will spend $100K maliciously to delay a G-block by 10 minutes. Or $2M to delay by a few hours or $200M to delay by a day. Its certainly possible since there are some wealthy folks in crypto who have “more money than Rwanda”, but I think its highly unlikely they will dump so much money on a temporary prank, whose only lasting effect is to advertise the robustness of the thing they are attacking.


*(9 more replies not shown)*

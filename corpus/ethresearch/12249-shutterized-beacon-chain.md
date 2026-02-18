---
source: ethresearch
topic_id: 12249
title: Shutterized Beacon Chain
author: cducrest
date: "2022-03-24"
category: Execution Layer Research
tags: [mev]
url: https://ethresear.ch/t/shutterized-beacon-chain/12249
views: 15994
likes: 47
posts_count: 28
---

# Shutterized Beacon Chain

# Shutterized Beacon Chain

## Acknowledgement

We’d like to thank [@mkoeppelmann](/u/mkoeppelmann) for coming up with the idea and collaborating with us on the proposal, [@JustinDrake](/u/justindrake) for helpful discussions and creative ideas, as well as to Sebastian Faust and Stefan Dziembowski for designing Shutter’s DKG protocol.

## Summary

- MEV is an important problem, but it can be solved directly in an L1 beacon chain
- Shutter provides a solution for that: A set of nodes compute an encryption key using a DKG protocol, let users encrypt their transactions with it, and release the decryption key once the encrypted transactions are in the chain.
- This technique can be applied to Ethereum-like beacon chains, by using the validator set to run the DKG protocol and introducing a scheduling mechanism for encrypted transactions.

## The problem

Miner-extractable value (MEV) and front running are widely recognized to be among the final unsolved fundamental issues in the blockchain space. There are now hundreds of millions of dollars of documented MEV, most of which is tremendously harmful for users and traders. This problem will inevitably become more devastating over time and eventually could even pose a fatal obstacle on our community’s path to mainstream adoption.

The term MEV was coined by Phil Daian et al. and describes revenue that block producers can extract by selecting, injecting, ordering, and censoring transactions. The MEV extracted in 2020 alone was worth more than $314M — and that is only a lower bound. Oftentimes, the MEV is not captured by the block producers themselves, but rather by independent entities using sophisticated bots.

An important subset of MEV is the revenue extracted by so-called front running — an attack that is illegal in traditional markets, but uncontrolled in the crypto space. A front runner watches the network for transactions that are worth targeting. As soon as they find one, they send their own transaction, trying to get included in the chain beforehand. They achieve this by paying a higher gas price, operating world-spanning network infrastructure, being a block producer themselves, or paying one via a back channel.

The most frequent victims of front running attacks are traders on decentralized exchanges. Front running makes them suffer from worse prices instead of being fairly rewarded for the information they provide to the market. On the other side, front runners siphon off profits from their victims in a nearly risk-free fashion without contributing anything useful to the system. A simple example of this are arbitrage transactions benefitting from the price difference of the same asset on two different DEX’s. Front runners regularly copy these kinds of transactions from other market participants and execute them earlier, reaping the rewards, whereas the original trader comes away empty-handed.

Besides exchanges, many other applications can be affected as well, including bounty distributions and auctions. Importantly, because they rely on voting, governance systems, which represent a large and fast-growing field within Ethereum, are prone to front running and could face significant challenges without a system that protects against these types of attacks.

In traditional finance, front running can be curbed (somewhat) via regulation or oversight by various trusted intermediaries and operators. In permissionless, decentralized systems this is not the case, so it might be a strategic blocker to mainstream crypto adoption.

## Requirements

We believe the beacon chains should be MEV protected for their users with no overhead or changes in terms of user experience. This protection should also come with no additional security guarantees, or, should at least fallback to the standard non-MEV protected functionning in case the added security assumptions fail. Lastly, it should work with a similar decentralization level as the consensus protocol.

## Shutter

Shutter allows users to send encrypted transactions in a way that protects them from front runners on their path through the dark forest (the metaphorical hunting ground of front runners that each transaction must cross). For example, a trader could use Shutter to make their order opaque to front runners, which means attackers can neither determine if it is a buy or a sell order, nor which tokens are being exchanged, or at which price. The system will only decrypt and execute a transaction after it has left the dark forest, i.e. after the execution environment of the transaction has been determined.

The keys for encryption and decryption are provided by a group of special nodes called keypers. Keypers regularly produce encryption keys by running a distributed key generation (DKG) protocol. Later, they publish the corresponding decryption key. The protocol uses threshold cryptography — a technique enabling a group of key holders to provide a cryptographic lock that can only be opened if at least a certain number of the members collaborate. This ensures that neither a single party, nor a colluding minority of keypers, can decrypt anything early or sabotage the protocol to stop it from executing transactions. As long as a certain number of keypers (the “threshold”) is well-behaved, the protocol functions properly.

## L1 Shutter in core protocol

We have already developed on-chain shutter, a mechanism to protect individual smart contracts from ordering attacks on L1, but it has the drawback of breaking composability. We are further working on implementing shutter directly inside roll-ups. Here we will describe a design to integrate the shutter system as part of Ethereum-like beacon chains. This has the benefit of being completely abstracted away from the user, and conserving composability.

As in every shutter system, the protocol needs a set of keypers. The keyper set is selected among chain validators by similar procedures selecting committees or block producers, except they would be selected much less frequently (e.g. once a day). Keypers use the beacon chain to generate a shared eon key. The eon public key will be made available to users to encrypt their transactions.

Block producers collect encrypted as well as plaintext transactions for a block. They include in their blocks the plaintext transactions to be executed, while encrypted transactions are scheduled for a future block height.

After a block is produced, the keypers should generate the decryption key allowing to decrypt the transactions scheduled for that block. The following block must include the decryption key to be considered valid. The post state of the block is computed by executing first the encrypted transactions scheduled for that block, before executing the plaintext transactions included in that block.

The execution order and context (block number, timestamp, etc …) is determined by the order of inclusion of ciphertext transactions and the context of the previous block. The context of execution being determined before the decryption of the transaction, it is impossible to use information about the transaction data to extract MEV. It also prevents side-channel information that could be used to optimistically front-run a transaction.

[![Group 1](https://ethresear.ch/uploads/default/original/2X/e/e210129d82939ef6dab8679d52b2dd1e0bf8878a.png)Group 1635×189 4 KB](https://ethresear.ch/uploads/default/e210129d82939ef6dab8679d52b2dd1e0bf8878a)

### Ciphertext transaction fees

Block producers need to somehow ensure that encrypted transactions are worth including in a block, i.e. that they can pay for a transacion fee, without knowing the transaction data. If the fee would be paid at time of execution, the block producer would not be guaranteed to be paid, since the account could be depleted in between inclusion and execution.

Therefore, encrypted transactions justify their inclusion by providing a signed `envelope` paying the fees at the moment of its inclusion in the chain. The envelope includes the fields: `gas consumption`, `gas price`, and a signature on these fields, allowing to recover the `fee payer` address. The fee will be paid on inclusion of the ciphertext transaction to the block producer, i.e. not at the time of execution. The gas consumption of the ciphertext transaction counts towards the gas limit of the block it was included in.

The traditional `gas limit` needs to be replaced with `gas consumption`, meaning that the user will pay for all the gas it plans to use, even if it uses only part of it at the time the transaction is decrypted and applied. This is necessary for the fee to be paid at the time of the transaction inclusion in the chain. This prevents blocks producers from having to include a transaction with an incredibly high `gas limit` (taking the place of other transactions and their fees) that decrypts to a transaction with very little `gas used` (and fees).

The other drawback of using envelope transaction is that meta-data of the transaction are leaked, i.e. the fee payer and gas price / upper limit of consumption are known. Potentially, a small part of MEV can still be extracted using this leaked information.

It has been pointed out that a zk-SNARK approach could be envisonned to solve this fee payment problem as well, and prevent the leaking meta-data information.

### Security guarantees

The eon public key and decryption keys generated by keypers require a t out of n threshold of honest participants. The parameters t and n can be played with to adapt the protocol. The higher t, the harder for keypers to collude and decrypt transactions too early (allowing MEV extraction). On the other hand, a lower t will guarantee that the decryption key is released in a timely manner.

To enforce decryption and application of ciphertext transactions, we have to enforce inclusion of the decryption key in each block. In  these conditions, if keypers turn offline or refuse to produce a decryption key, the block production will halt.

We can mitigate the liveness influence of keypers by allowing to produce a block without a decryption key if there is no encrypted transaction scheduled for execution. In case keypers go offline, the chain would recover by forking away the blocks with encrypted transactions and produce blocks only with plaintext transactions.

We can also recover liveness by stating that if no block is produced during n slots (due to not having the decryption key), the next block does not need to include a decryption key, and decrypted transactions are ignored. This will fall back to the legacy non-MEV protected functionning of the chain.

### Changes to the implementation

The keyper software has already been developed, as well as all the encryption / decryption logic. We also developed the logic allowing a block producer (or collator / sequencer) to commit to a batch of encrypted transactions, signaling to the keypers that it is now safe to release the decryption key.

What needs to be done is to change the rules that define correctness of a block in client implementations, as well as the rules for execution of transactions. The interface for submission of transaction to the client has to be redefined. Lastly, tools and plugins will likely have to be written to allow dapps to seamlessly integrate with an MEV protected chain requiring encryption of transactions with the public eon key.

## Replies

**MicahZoltu** (2022-03-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/cducrest/48/8858_2.png) cducrest:

> We can also recover liveness by stating that if no block is produced during n slots (due to not having the decryption key), the next block does not need to include a decryption key, and decrypted transactions are ignored.

How do you identify that the reason the block wasn’t produced was because decryption keys were missing and not for any other reason?

It also feels like it is fairly critical (for liveness) to have the number of missing slots before reorging out the block in question to be very low, and we would need the reorg to be *at most* less deep than the most recent `justified` block so we can maintain other guarantees.  There is also discussion about moving the `safe` block to pretty close to head (maybe not even a full block behind), in which case I would be very loath to have a condition under which a `safe` block gets reorged out (but may be open to it in the `safe` case, but not `justified` case).

---

**jannikluhn** (2022-03-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> How do you identify that the reason the block wasn’t produced was because decryption keys were missing and not for any other reason?

We don’t, but since liveness failures are hopefully very exceptional states this distinction shouldn’t be important.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> It also feels like it is fairly critical (for liveness) to have the number of missing slots before reorging out the block in question to be very low, and we would need the reorg to be at most less deep than the most recent justified block so we can maintain other guarantees. There is also discussion about moving the safe block to pretty close to head (maybe not even a full block behind), in which case I would be very loath to have a condition under which a safe block gets reorged out (but may be open to it in the safe case, but not justified case).

Technically it wouldn’t be a reorg. The block that includes the encrypted transactions would still be part of the chain, the transactions simply won’t be executed. So the structure of the chain doesn’t change and heads stay heads.

---

**wjmelements** (2022-03-26):

I’m generally opposed to mechanisms that would fuzz the head state because it would make trading more difficult than it already is.

The proposal conflates MEV with front-running and says most of MEV is front-running. This is not quantitatively true. Frontrunning can be harmful (thought usually the fault of the UI, eg Uniswap), but most MEV (backrunning, liquidations) is significantly beneficial for casual traders.

It devises a pseudo-private transaction scheme that can hide a transaction for the duration of a block, but the transaction can be revealed before it is confirmed if it is not included in the next couple blocks. Thus it won’t prevent a majority of front-running.

> meaning that the user will pay for all the gas it plans to use, even if it uses only part of it at the time the transaction is decrypted and applied

That’s harsh, especially in case of revert. Instead they could pay some fraction of the difference between gas reserved and gas used.

---

**pmcgoohan** (2022-03-28):

This is the most serious and workable base layer MEV mitigation proposal that I have seen, and Ethereum is in dire need of one.

Any objection to it on the basis that toxic MEV is not a problem or that mitigation might get in the way of benign MEV extraction is a non-starter.

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> most of MEV is front-running. This is not quantitatively true.

I’m not sure of your data source here, but I’m going to assume Flashbots MEV-Explore as it is widely trusted and still reports 99% of MEV as arbitrage.

Flashbots are aware that this figure is wrong as it does [not include sandwich attacks](https://explore.flashbots.net/data-metrics). Their data source (MEV-Inspect) over a 6 month period reports that infact around 37% of MEV is toxic sandwich attacks. I know they have had issues calculating sandwich profits, but as for why they are not including sandwich counts in their [Extracted MEV Split by Type](https://explore.flashbots.net/) reports, I suggest you ask them.

This data-gap is worrying from an organization in such a close advisory capacity to the EF, with active proposals for base layer MEV auctions that will exacerbate toxic MEV extraction, for precisely the reason that it undermines the basis of vital proposals like this one.

Even when sandwich attacks are accounted for, there are many other unquantified examples of toxic MEV, eg: NFT sniping, toxic arbitrage (reordering backrunning), liquidity pool attacks, forced liquidations and censorship-as-a-service.

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> most MEV (backrunning, liquidations) is significantly beneficial for casual traders

Nothing in this proposal will impact the ability to perform straightforward (non-toxic) arbitrage/backrunning or the 0.5% proportion of MEV that is liquidations.

---

**jannikluhn** (2022-03-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> The proposal conflates MEV with front-running and says most of MEV is front-running. This is not quantitatively true. Frontrunning can be harmful (thought usually the fault of the UI, eg Uniswap), but most MEV (backrunning, liquidations) is significantly beneficial for casual traders.

We agree that some forms of MEV are beneficial (or at least that MEV extraction can have positive externalities). We’re not trying to make a quantitative analysis here how much MEV is beneficial or harmful, we’re just trying to make harmful MEV extraction harder.

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> It devises a pseudo-private transaction scheme that can hide a transaction for the duration of a block, but the transaction can be revealed before it is confirmed if it is not included in the next couple blocks. Thus it won’t prevent a majority of front-running.

The “inclusion period” is a parameter we can choose long enough to make it unlikely that transactions won’t be included in this time. With EIP1559 and PoS I don’t think this parameter has to be very big though.

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> That’s harsh, especially in case of revert. Instead they could pay some fraction of the difference between gas reserved and gas used.

Yeah, that’s a downside of the proposal. The problem is that the block producer should have a guarantee how much they’ll get paid in transaction fees at the time they build the blocks. If there’s a discount on failed transactions we can’t give that guarantee. Maybe with EIP1559 this isn’t that big of a deal though, because proposers often can just include all transactions with high enough gas price without having to worry about gas limits.

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> I’m generally opposed to mechanisms that would fuzz the head state because it would make trading more difficult than it already is.

Why would it make trading more difficult? In a way the proposal just hides transactions that you can’t rely on anyway because the block proposer could reorder them at will.

---

**wjmelements** (2022-03-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> we’re just trying to make harmful MEV extraction harder.

You didn’t address it so I will highlight again: for all harmful frontrunning cases, the dapps are at fault. Without exception. For Uniswap sandwiches, the UI is conflating expected price slippage with extra slippage, so users are setting extraordinarily low minimum outputs and getting rekt. It is fairly trivial to calculate the slippage you can allow without financing a sandwich. For auction bid withdrawal and replacement, the accept bid function should have specified a minimum output parameter but it can be fixed with a wrapper that reverts. These problems persist under your scheme; you just replace the current fair auction scheme with spam (which was the case before the auction).

On the other hand, I have hundreds of thousands of DEX trades, none of which have been sandwiched. There’s no implicit threat, only a terrible UI/UX and misattributed anger.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> Why would it make trading more difficult? In a way the proposal just hides transactions that you can’t rely on anyway because the block proposer could reorder them at will.

Let’s take this to an extreme since you can’t see how this would even be marginally more difficult. Set your JSONRPC node to remain 1 day behind and try to trade on Uniswap’s official UI. You will be sandwiched or your transaction will revert. Your new uncertainty forces you to set a worse minimum output and that is the exact amount you will get, as before. But you will be much worse at setting that output, finding the optimal route, etc. The same would be true for aggregators, except with a higher chance of revert.

The more uncertain we are about the head state, the more transactions we have to send, and the more checks they have to do in order to decide whether to revert or proceed. This will increase the proportion of blockspace reserved for MEV processing.

But, if the head transactions can be decrypted *before* the next block is produced, then it is similar enough to the current scheme, because (as discussed below) the private transactions will be at the end of the block

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> Yeah, that’s a downside of the proposal. The problem is that the block producer should have a guarantee how much they’ll get paid in transaction fees at the time they build the blocks.

There are also conditional fees paid to `COINBASE` only if transaction succeeds. To secure their conditional fees, producers will put the private transactions at the end of the block. Consequently, private transactions will be both more expensive to use and more likely to revert. There is hope therefore that your feature would go unused if it was adopted.

---

**wjmelements** (2022-03-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> There is hope therefore that your feature would go unused if it was adopted.

I’ve thought about this some more and it might still be used for griefing attacks, wherein you try to increase the transaction fees your competitors pay.

---

**aminok** (2022-03-28):

> For Uniswap sandwiches, the UI is conflating expected price slippage with extra slippage

Can you clarify what you mean by “extra slippage”? Often when I’ve set my slippage to a low value, I’ve had my transaction fail, at huge expense in gas costs.

How does the dapp or its front-end minimize the risk of transaction failure through price slippage, while preventing sandwich attacks?

Intuitively your claim seems wrong: obviously if dapps could eliminate MEV, they would have already. They don’t, because they can’t.

---

**wjmelements** (2022-03-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/aminok/48/8882_2.png) aminok:

> Intuitively your claim seems wrong: obviously if dapps could eliminate MEV, they would have already. They don’t, because they can’t.

I didn’t say they could eliminate MEV. All harmful extractions can be prevented though.

After I explained to a Uniswap engineer that this frontrunning was the fault of their default slippage being so high, they introduced an auto slippage feature that seems more intelligent. I think it does something similar to what I describe later in this reply.

![](https://ethresear.ch/user_avatar/ethresear.ch/aminok/48/8882_2.png) aminok:

> Can you clarify what you mean by “extra slippage”?

The configuration in the Uniswap UI is for extra slippage: how much less than the exact output calculated that you are willing to accept without reverting.

![](https://ethresear.ch/user_avatar/ethresear.ch/aminok/48/8882_2.png) aminok:

> How does the dapp or its front-end minimize the risk of transaction failure through price slippage, while preventing sandwich attacks?

An easy heuristic is to double your swap fees. If the dex charges 0.05%, you can specify 0.1% extra slippage and it cannot be profitable to sandwich you.

For smaller swaps you can calculate how much your transaction fee is worth as a proportion of your output and allow for that.

---

**aminok** (2022-03-29):

> The configuration in the Uniswap UI is for extra slippage: how much less than the exact output calculated that you are willing to accept without reverting.

How is this distinguished from “expected price slippage”? Earlier you identified two different types of slippage: *For Uniswap sandwiches, the UI is conflating expected price slippage with extra slippage*

Also, your analysis does not address swap failures due to slippage, which are more likely to occur when the slippage tolerance variable is set to a lower value.

> An easy heuristic is to double your swap fees. If the dex charges 0.05%, you can specify 0.1% extra slippage and it cannot be profitable to sandwich you.

How is that supposed to help the trader? The trader has just changed which party is extracting fees, from the MEV miner, to the dApp.

Clearly MEV is a very serious problem for market efficiency on Ethereum, and if an architecturally sound means of dealing with it could be found, it would benefit users.

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> censorship-as-a-service.

Indeed. This proposal would significantly raise the bar for imposing censorship on Ethereum at the validator level.

---

**cducrest** (2022-03-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> On the other hand, I have hundreds of thousands of DEX trades, none of which have been sandwiched. There’s no implicit threat, only a terrible UI/UX and misattributed anger.

I understand that your opinion is that harmful MEV should be prevented by dapps. I believe that any transaction impacting the state, can create unforeseeable MEV.

If you make a DEX trade that brings imbalance to the market, even with 0% “extra slippage”, you create an opportunity for others to profit from the new market state. It could be that market observers will want to race to profit from the new state. You created a back-running MEV opportunity, from which you are not explicitly the victim.

I do not think dapp builders can imagine every possible MEV opportunity they might create with their protocol. I think the application layer is the wrong place to “fix” MEV, and it should be done whenever possible at the base layer.

---

**wjmelements** (2022-03-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/cducrest/48/8858_2.png) cducrest:

> You created a back-running MEV opportunity, from which you are not explicitly the victim.

Who is the victim here? Are you saying the sender is implicitly the victim because they didn’t use an aggregator? I don’t think any consensus level proposal can fix that problem.

![](https://ethresear.ch/user_avatar/ethresear.ch/aminok/48/8882_2.png) aminok:

> The trader has just changed which party is extracting fees, from the MEV miner, to the dApp.

I don’t think you understand my post at all. It’s possible your confusion originates from not knowing that Uniswap charges fees, but I have no idea what you’re on about here.

---

**aminok** (2022-03-29):

> I don’t think you understand my post at all. It’s possible your confusion originates from not knowing that Uniswap charges fees, but I have no idea what you’re on about here.

Yes, I don’t understand how what you proposed is a solution. In your hypothetical, you suggested doubling swap fees. Higher fees are to the disadvantage of the trader. Perhaps you can elaborate on this to help me understand.

---

**wjmelements** (2022-03-30):

Thank you. I think I can help you understand my point now.

![](https://ethresear.ch/user_avatar/ethresear.ch/aminok/48/8882_2.png) aminok:

> How is this distinguished from “expected price slippage”?

I say “expected price slippage” to refer to implicit AMM price movement from the trade, in contrast to “extra slippage” which is what the user allows beyond that to allow successful confirmation in case the price moves against them before their transaction confirms. The implicit price movement is a monotonic function of the size of trade. This means that the larger your trade, the worse your effective price.

In the Uniswap UI (below) this extra slippage is presented as a percentage. In your transaction, the percentage is used to calculate the minimum output you would accept for your input without reverting (Fill-Or-Kill). I believe that the reason most of the Uniswap users getting rekt have set their extra slippage exceptionally high is that they mistakenly believe the “Slippage tolerance” to refer to implicit slippage.

[![Screen Shot 2022-03-29 at 9.30.11 PM](https://ethresear.ch/uploads/default/original/2X/1/1a72ba718163c1c3fc885bcbd2ed3aaf8ce6775c.png)Screen Shot 2022-03-29 at 9.30.11 PM606×228 13.5 KB](https://ethresear.ch/uploads/default/1a72ba718163c1c3fc885bcbd2ed3aaf8ce6775c)

![](https://ethresear.ch/user_avatar/ethresear.ch/aminok/48/8882_2.png) aminok:

> Yes, I don’t understand how what you proposed is a solution. In your hypothetical, you suggested doubling swap fees. Higher fees are to the disadvantage of the trader. Perhaps you can elaborate on this to help me understand.

Ok I see now. Here is what I mean. I recommend setting your extra slippage to equal double the swap fee. So if the Uniswap router is sending you through the UniswapV3 0.05% USDC-WETH pool, you should set extra slippage to 0.10%. This heuristic works because the extra slippage you allow times the size of your trade is the maximum theoretical revenue a sandwicher can extract from you. The would-be sandwicher’s maximum profit (0.10%) would be completely offset by exchange fees on their two swaps. So you cannot be sandwiched because it is not profitable.

---

**aminok** (2022-03-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> I believe that the reason most of the Uniswap users getting rekt have set their extra slippage exceptionally high is that they mistakenly believe the “Slippage tolerance” to refer to implicit slippage.

Understood. And I see that the old Uniswap UI used the “additional slippage” terminology.

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> The would-be sandwicher’s maximum profit (0.10%) would be completely offset by exchange fees on their two swaps.

Thank you for the explanation. Yes, this is a useful heuristic. But you will need to set your slippage tolerance (i.e. additional slippage) to a higher value than what’s safe against sandwich attacks at times, when the market for that pair is exceptionally volatile, and/or when gas fees are exceptionally high. The reason is that there can be legitimate additonal slippage, from real traders, that exceeds the slippage tolerance you set, that can cause your transaction to fail otherwise, and thereby cost you a significant amount in wasted gas fees.

---

**ruuda** (2022-04-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> for all harmful frontrunning cases, the dapps are at fault. Without exception. For Uniswap sandwiches, the UI is conflating expected price slippage with extra slippage

I would go one step further. If we accept that sandwiching happens, then why does Uniswap let frontrunners take the difference between the `amountOutMinimum` and the actual output, instead of paying the difference to liquidity provides? If Uniswap would never pay out more than `amountOutMinimum`, the abusive MEV opportunity goes away and the benefit would go to liquidity providers instead. Traders get the same price as they would get when abusive MEV is present. It’s a bit worse than without sandwiching, but I think MEV is forcing us to accept that [swaps are limit orders, not market orders](https://ruudvanasseldonk.com/2021/12/07/a-perspective-shift-on-amms-through-mev). In hindsight, treating swaps as market orders was naive, like thinking that nobody would enter adversarial inputs in a website in the early days of the internet. That ship has sailed.

![](https://ethresear.ch/user_avatar/ethresear.ch/cducrest/48/8858_2.png) cducrest:

> I believe that any transaction impacting the state, can create unforeseeable MEV

![](https://ethresear.ch/user_avatar/ethresear.ch/cducrest/48/8858_2.png) cducrest:

> I do not think dapp builders can imagine every possible MEV opportunity they might create with their protocol.

I agree, and this is why I think we should treat this in the same way that we treat bugs. In a sense, abusive MEV opportunities are game-theoretic vulnerabilities: profitable ways to use the protocol that the dapp developer had not anticipated, and that harm the intended users. It’s a class of vulnerabilities that was previously never considered, but now that the genie is out of the bottle, we will have to deal with them, similar to how pre-Meltdown/Spectre speculative execution vulnerabilities were not on anybodies radar.

If you find a (game-theoretic) 0-day, you try to report it to the developers, and hopefully you get a bounty. If the developers don’t fix it, then one way to force their hand is to release a PoC, or to start exploiting. I don’t approve of exploiting abusive MEV opportunities, but ultimately I think the dapp developers are at fault for enabling them.

![](https://ethresear.ch/user_avatar/ethresear.ch/cducrest/48/8858_2.png) cducrest:

> I think the application layer is the wrong place to “fix” MEV, and it should be done whenever possible at the base layer.

For the same reason that dapp developers cannot imagine every possible MEV opportunity that they might create, I don’t think base layer developers can either. In the end, transactions are selected and ordered in some particular way. There are going to be strategies to maximize profit within those constraints. Changing the constraints changes what the best strategies are, but it’s not obvious to me that this new set of constraints admits *no* (or even just fewer) harmful strategies. With opaque transactions, maybe the guaranteed profitable strategies could be eliminated, but I can imagine probabilistically profitable strategies will remain.

---

**pmcgoohan** (2022-04-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/ruuda/48/7016_2.png) ruuda:

> If Uniswap would never pay out more than amountOutMinimum, the abusive MEV opportunity goes away and the benefit would go to liquidity providers instead

You seem to be suggesting that because the sandwich profits go to the LP instead of the searcher you have fixed the exploitation. But the outcome in this case is the same for the victim (or in fact worse as you admit).

![](https://ethresear.ch/user_avatar/ethresear.ch/ruuda/48/7016_2.png) ruuda:

> For the same reason that dapp developers cannot imagine every possible MEV opportunity that they might create, I don’t think base layer developers can either.

Base layer developers don’t have to imagine every possible MEV opportunity. It’s very simple. Toxic MEV = miners reordering transactions for profit. There can be no satisfactory solution in the app layer until you have mitigated this power that miners have in the base layer.

There are broadly two solutions to MEV:

1. fair order transactions - so miners can’t reorder
2. encrypt the mempool - so miners can’t determine the advantages of reordering

Both mitigate the vast majority of toxic MEV without leaving dApp developers with a literally impossible task. This proposal opts for (2).

Sure, Uniswap could do more, but the app layer is not the layer that toxic MEV is happening in.

An encryption solution that prevents miners reordering *is* a generalized solution because the problem is fundamentally miners reordering.

---

**fradamt** (2022-04-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> The more uncertain we are about the head state, the more transactions we have to send, and the more checks they have to do in order to decide whether to revert or proceed. This will increase the proportion of blockspace reserved for MEV processing.
>
>
> But, if the head transactions can be decrypted before the next block is produced, then it is similar enough to the current scheme, because (as discussed below) the private transactions will be at the end of the block

Decrypted transactions are put at the top of a block, it’s not something which a proposer has control over. And they can be decrypted before the next block is produced, if the key is released sufficiently in advance, in which case the initial state of the next block is known

---

**wjmelements** (2022-04-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> Decrypted transactions are put at the top of a block, it’s not something which a proposer has control over.

That’s not desirable because it incentivizes block producers to censor those transactions to avoid risking their conditional payments. Is there some reason they shouldn’t be at the end of the block?

---

**fradamt** (2022-04-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/wjmelements/48/4841_2.png) wjmelements:

> That’s not desirable because it incentivizes block producers to censor those transactions to avoid risking their conditional payments. Is there some reason they shouldn’t be at the end of the block?

Encrypting them is useless if they don’t go at the front of the block after the key is released, because they will be frontrunnable.

Also, the payment isn’t conditional and it is effective immediately:

![](https://ethresear.ch/user_avatar/ethresear.ch/cducrest/48/8858_2.png) cducrest:

> Block producers need to somehow ensure that encrypted transactions are worth including in a block, i.e. that they can pay for a transacion fee, without knowing the transaction data. If the fee would be paid at time of execution, the block producer would not be guaranteed to be paid, since the account could be depleted in between inclusion and execution.
>
>
> Therefore, encrypted transactions justify their inclusion by providing a signed envelope paying the fees at the moment of its inclusion in the chain. The envelope includes the fields: gas consumption, gas price, and a signature on these fields, allowing to recover the fee payer address. The fee will be paid on inclusion of the ciphertext transaction to the block producer, i.e. not at the time of execution. The gas consumption of the ciphertext transaction counts towards the gas limit of the block it was included in


*(7 more replies not shown)*

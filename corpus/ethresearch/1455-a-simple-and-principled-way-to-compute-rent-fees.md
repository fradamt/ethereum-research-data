---
source: ethresearch
topic_id: 1455
title: A simple and principled way to compute rent fees
author: vbuterin
date: "2018-03-22"
category: Sharding
tags: [storage-fee-rent]
url: https://ethresear.ch/t/a-simple-and-principled-way-to-compute-rent-fees/1455
views: 37827
likes: 67
posts_count: 63
---

# A simple and principled way to compute rent fees

1. Come up with an estimate for the annual rewards given out by the (full) Casper and sharding mechanisms. Currently, an expected value is 10 million ETH staking at 5% interest, which is 500,000 ETH per year (~0.22 ETH per block).
2. Come up with a maximum acceptable long-run worst-case-scenario state size. I would suggest 500 GB. Note that in practice, the state size would likely be 1-2 orders of magnitude lower than this; this is just a long-run upper bound.
3. To make sure it’s not long-run possible for the state to exceed 500 GB, storing 500 GB should cost 500,000 ETH per year, so storing 1 byte should cost 0.000001 ETH per year. A 24000-byte contract would cost 0.024 ETH (~$15) per year; a 250-byte account would cost 0.00025 ETH (~$0.15) per year.

With sharding, the maximum acceptable state size would be per-shard, so the above fees would be decreased by a factor of 100.

One natural objection is: but won’t fixing the storage fees in ETH lead to unacceptable fees if ETH rises or falls too much? The answer is: this is quite possible, but transaction fees are not expected to be any less volatile. They were certainly less volatile back in 2011-2017, but that was only because blocks were not full (for bitcoin or ethereum), and so de-facto fees were centrally planned by core devs and miners who adjusted them downwards in response to public pressure every time the fees got too high; with full blocks this is not possible, and so tx fees are [even more volatile](https://etherscan.io/chart/transactionfee) [than prices](https://blockchain.info/charts/transaction-fees-usd).

## Replies

**nootropicat** (2018-03-22):

> I would suggest 500 GB. Note that in practice, the state size would likely be 1-2 orders of magnitude lower

How did you arrive at this number? It’s very low.

Why constant? Storage technology is very far from physical limits.

> A 24000-byte contract would cost 0.024 ETH (~$15) per year; a 250-byte account would cost 0.00025 ETH (~$0.15) per year.

Every contract would have to design some mechanism to collect fees from users (eg. token holders) to pay for storage. What if someone doesn’t pay? Either their data, potentially worth millions, gets deleted, or a fraction of tokens somehow gets sold. Sold how? Auction? How long and does that even work for something illiquid? So much complexity.

Why would contract creators prefer to deal with this, rather than switch to something without nominal time fees?

Why would users choose something with on-going fees over something without?

As seen by the adoption and opinions about freicoin demuragge is extremely unpopular.

With an eternally locked eth model, lost interest from staking already creates an implicit time based cost.

---

**vbuterin** (2018-03-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/nootropicat/48/258_2.png) nootropicat:

> How did you arrive at this number? It’s very low.

The current state size is ~5 GB. 500 GB seems like the largest that would be feasible in the medium term without requiring almost everyone to get special-purpose hard drives. Additionally, it corresponds to something like ~5 days of fast sync time assuming a 1 MB/s download bandwidth, which seems very inconvenient but not impossible.

> Why constant? Storage technology is very far from physical limits.

It could be hard-forked up if needed, or adjusted up like gas limits.

> Every contract would have to design some mechanism to collect fees from users (eg. token holders) to pay for storage. What if someone doesn’t pay? Either their data, potentially worth millions, gets deleted, or a fraction of tokens somehow gets sold. Sold how? Auction? How long and does that even work for something illiquid? So much complexity.

Users would automatically pre-fill the contracts that store any data relevant to them with a few years of storage whenever they send a transaction related to them. There are second-layer markets that would be required here to improve performance further, but they are simpler than the second-layer markets that would be required to maintain an acceptable quality of developer and user experience in a no-rent stateless-client-only model.

> With an eternally locked eth model, lost interest from staking already creates an implicit time based cost.

Sure, but it also makes spamming the state cost-free for anyone who happens to be holding ETH, and will likely lead to the emergence of second-layer rent markets anyway. Heck, the status quo is incentivizing the emergence of second-layer rent markets, see http://gastoken.io.

---

**danrobinson** (2018-03-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Sure, but it also makes spamming the state cost-free for anyone who happens to be holding ETH, and will likely lead to the emergence of second-layer rent markets anyway. Heck, the status quo is incentivizing the emergence of second-layer rent markets, see http://gastoken.io.

What if you pay interest (from newly issued ETH) to contracts and accounts that maintain excess ETH (over what is required to be locked up to maintain their state)? Then your rent is in the form of inflation. That penalizes spammers while avoiding the risk of a contract going bankrupt.

You’d just want to make sure growth rate of the total ETH supply (between both this inflation and Casper rewards) is no greater than the growth in affordable storage hardware.

[EDIT: Ah, from their next post, it seems like this is what [@nootropicat](/u/nootropicat) was suggesting? Is there a description of this scheme somewhere?]

[EDIT 2: Perhaps the opportunity cost of not staking would be sufficient to discourage spamming, since there are better ways to lock up ETH. Maybe you could even have a withdrawal period of 4 months for ETH that is locked up for storage (just to make the option as comparable as possible to staking, although you wouldn’t have the burden of participating in consensus). That would seem pretty inconvenient, but second-layer markets could potentially help you with that.]

---

**nootropicat** (2018-03-22):

> The current state size is ~5 GB. 500 GB seems like the largest that would be feasible in the medium term without requiring almost everyone to get special-purpose hard drives.

So shouldn’t the target be at least 5TB then? If 500GB is feasible for an average node, it should be the expected average, not an impossible maximum.

Also I think you’re *significantly* overestimating the expected use. Right now there are no storage fees (either explicit or implicit) and it’s only 5GB. Even at 1PB cost per byte would be ridiculously high compared to the cloud storage prices which would prevent waste.

> without requiring almost everyone to get special-purpose hard drives

Only validators are paid to run full nodes, average user isn’t going to regardless. Validators and businesses that use ethereum can get larger drives.

> Sure, but it also makes spamming the state cost-free for anyone who happens to be holding ETH

No, the true payment unit is not eth but a percentage of the total supply, as 1 ether is only an arbitrary unit. Exactly like shares in a company. Both payment methods are a different way of lowering that share.

The only difference is that paying with lost interest AND not automatically deleting creates the equivalent of a ‘zero bound’ - as maximum allowable storage grows with the total supply.

So unless hardfork/gas limit like/ increases are going to be substantially smaller than increases in the total supply, the explicit payment model makes no sense, as it adds complexity for no gain.

IF they are going to be, then all that additional complexity is there only to prevent a few percentage points of growth at most. Is it really worth it?

> the status quo is incentivizing the emergence of second-layer rent markets, see http://gastoken.io

Yes, that’s because gas fees are conflating performance and storage costs. Locking eth solves that.

---

**logannc** (2018-03-22):

> To make sure it’s not long-run possible for the state to exceed 500 GB, storing 500 GB should cost 500,000 ETH per year, so storing 1 byte should cost 0.000001 ETH per year,

Charging for storage naturally disincentivizes storage, but is there an economic/incentive/arbitration relation between 500GB and 500,000 Eth? Or is it just a presupposition that users will value storage on the ETH blockchain at 0.000001 ETH/byte? If I, and everyone else, value storage an order of magnitude more, then what actually stops the state from growing to 5TB? What happens when the state is full? The EVM throws errors on new state saving ops?

> Only validators are paid to run full nodes, average user isn’t going to regardless. Validators and businesses that use ethereum can get larger drives.

People use light clients because the state is too big, not because they don’t want to run a full node. They don’t want to run a full node because it is inconvenient. Make running a full node convenient and they will.

---

**Lars** (2018-03-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/logannc/48/1003_2.png) logannc:

> If I, and everyone else, value storage an order of magnitude more, then what actually stops the state from growing to 5TB?

You still have to pay for the current EVM execution, I suppose, which has a one-time cost for allocating storage.

---

**veekta** (2018-03-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/logannc/48/1003_2.png) logannc:

> If I, and everyone else, value storage an order of magnitude more, then what actually stops the state from growing to 5TB? What happens when the state is full?

presumably when the state grows larger than 500 GB, the rent charge causes the ETH burn to go over the ETH minting rate which causes ETH to become deflationary. Over time given a constant market cap, this may cause the rent costs to become prohibitive, resulting in people taking their data off the chain to preserve capital. It seems like there will be a lot of fine tuning to find the correct charges for rent in order to find a steady state for ETH inflation while keeping the state size in mind.

---

**logannc** (2018-03-22):

Ah, I was operating under the assumption that the rent was being paid to validators, rather than being burned. +1

---

**nootropicat** (2018-03-23):

If you want fee to be paid even from the non-staking perspective, then every not-locked eth could get small interest. Validators’ interest on top of it. It’s enough to keep a 32 bit block height per account with the last block that had a transaction to/from that account, and update balance on changes.

Locking eth is perfectly backwards compatible as it can be implemented in the existing gas mechanism:

 txFee = performanceGas*gasPrice + ethForStorage

 txGasLimit = \lceil{txFee/gasPrice}\rceil

with future refunds on deletion only for the lockedEth portion (no refunds at all for performanceGas).

(block gas limit ignores lockedEth ‘gas’)

How simple in comparison to time fees!

---

**vbuterin** (2018-03-23):

The other problem with locking as payment is that I think there is still a fundamental *behavioral* tradeoff that I think locking falls on the wrong side of, *precisely because* it seems so convenient. One key goal of rent, at least in my opinion, is that contracts that developers and users forget and stop caring about should disappear from the state by default; forgetting about economics, achieving such a state of affairs is by itself enough to get the majority of the gains that we want to achieve from a rent scheme. On the other hand, if the majority of developers continue to by default use a scheme where contracts last forever, then there continues to be a tradeoff between either contracts being very expensive to create to begin with or the state size not really decreasing.

That said, there *is* a scheme based on pay-to-resurrect that I think could solve a large portion of the UX issues, that I’ll expand on in a separate post.

---

**rayzh2012** (2018-03-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The current state size is ~5 GB. 500 GB seems like the largest that would be feasible in the medium term without requiring almost everyone to get special-purpose hard drives. Additionally, it corresponds to something like ~5 days of fast sync time assuming a 1 MB/s download bandwidth, which seems very inconvenient but not impossible.

TB drive is extremely common for most of the young adults using PC, are you talking about SATA or normal ones. Either way we are heading towards the specialized computer/harddrive for mining anyway, so POS would be mostly hosted on specialized equipments (possibly made in China)

---

**vbuterin** (2018-03-23):

> so POS would be mostly hosted on specialized equipments (possibly made in China)

I would really like to avoid encouraging that further. I recognize that that’s likely an optimal setup especially for high-value stakers, but that’s not an excuse to risk adding even more dependence on specialized hardware.

Additionally, keeping initial fast sync time low is also important.

---

**rayzh2012** (2018-03-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I would really like to avoid encouraging that further. I recognize that that’s likely an optimal setup especially for high-value stakers, but that’s not an excuse to risk adding even more dependence on specialized hardware.
>
>
> Additionally, keeping initial fast sync time low is also important.

don’t think you have a choice as many have told me that they will design it as long as its “profitable”. a long term solution is to restrict that exploitation.

do you think async would be better? fast sync time requires firmware level optimization, which eth hasn’t done too much about (as it relies on VM, but plz correct me if I am wrong)

---

**jpitts** (2018-03-23):

> Ah, I was operating under the assumption that the rent was being paid to validators, rather than being burned. +1

Perhaps the rent could go to those running full nodes.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png)
    [Incentives for running full Ethereum nodes](https://ethresear.ch/t/incentives-for-running-full-ethereum-nodes/1239/2) [Economics](/c/economics/16)



> After typing that rant up, I thought more about the problem and I have since become even more concerned that there is an incentive misalignment here, which leads to an unstable equilibrium long term.  Rather than focusing on the specific concerns about operational overhead of running a client, I would prefer to focus on the concern of lack of incentives to building a client.
> I’m curious what people’s thoughts are on user-agent incentivization?  I recognize that it isn’t game theoretically fool …

---

**nootropicat** (2018-03-23):

> One key goal of rent, at least in my opinion, is that contracts that developers and users forget and stop caring about should disappear from the state by default

You’re making a very dangerous assumption.

Sorry for the comparison, but - it’s the same reasoning as that used by honest btc smallblockers: sacrifice user experience *now* for the sake of more sustainable future. The dangerous assumption is that users stay.

Imagine that you want to create a dapp and you can choose two platforms to develop on: one has explicit time rents and one doesn’t; everything else, including userbase, is equal, including vm.

The choice is obvious: you can launch your dapp on the platform without explicit rents faster, one less thing to think about.

If for some reason you choose to deploy on a more complex platform first, a potential competitor that started at the exact same time would be able to launch first on the simpler platform.

Userbases aren’t going to be equal for long.

In an abstract way: markets execute stochastic gradient descent. An optimum that’s not the closest local optimum almost surely isn’t going to happen.

---

**vbuterin** (2018-03-24):

Here’s the writeup for the sleep/wake mechanism: [Improving the UX of rent with a sleeping+waking mechanism](https://ethresear.ch/t/improving-the-ux-of-rent-with-a-sleeping-waking-mechanism/1480)

Essentially, this degrades to “if you want to do something with a contract that got accidentally deleted, you just need to send a bunch of extra Merkle proofs along with your transaction to bring it back, so it’s kind of like the stateless client model”. I actually think it could be designed to be pretty tolerable.

---

**jamesray1** (2018-03-24):

It is true that 500 GB is too low compared to the current state size.


      ![](https://ethresear.ch/uploads/default/original/3X/e/1/e1ae42106c51c881c83b6e2219e4b0c9d2aa617d.png)

      [reddit.com](https://www.reddit.com/r/ethtrader/comments/7axn5g/ethereum_blockchain_sizewe_have_a_problem/)





###










Perhaps with stateless clients and storage rent then the storage will not grow above 500 GB, but that is a tenuous assumption if we assume that Ethereum 2.0 scales much more and it is necessary to store it in the state. However, much of it could be stored off-chain in secondary markets with archival nodes and fraud proofs.

---

**vbuterin** (2018-03-24):

That chart is **extremely** misleading. 500 GB is the data size of an archive node. The size of the state alone is 5 GB. For Ethereum 2.0, I am assuming a theoretical max size of 500 GB *per shard*, not in total; so the total storage would be ~50 TB (and perhaps we can eventually increase the shard count, say from 100 to 256 or even 1000).

---

**jamesray1** (2018-03-24):

You need the platform to be sustainable in the long run; you need to internalise costs. At the same time you deal with adverse side effects like a worse UX, such as second layer markets. One way or another, the platform will fail, be disrupted, or stagnate if the costs are not internalised.

---

**jamesray1** (2018-03-24):

OK, that’s fair enough, I neglected to think of that.


*(42 more replies not shown)*

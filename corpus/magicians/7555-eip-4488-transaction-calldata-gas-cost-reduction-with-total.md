---
source: magicians
topic_id: 7555
title: "EIP-4488: Transaction calldata gas cost reduction with total calldata limit"
author: vbuterin
date: "2021-11-24"
category: EIPs
tags: [gas]
url: https://ethereum-magicians.org/t/eip-4488-transaction-calldata-gas-cost-reduction-with-total-calldata-limit/7555
views: 16349
likes: 23
posts_count: 17
---

# EIP-4488: Transaction calldata gas cost reduction with total calldata limit

Decrease transaction calldata gas cost, and add a limit of how much total transaction calldata can be in a block.

See: [Transaction calldata gas cost reduction with total calldata limit by vbuterin · Pull Request #4488 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4488)

## Replies

**yoavw** (2021-11-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> if a block fills up to the size limit, they could repeatedly remove the last data-heavy transaction and replace it with as many data-light transactions as possible, until doing so is no longer profitable.

This is indeed the optimal strategy for miners - to drop rollup transactions in favor of more execution-oriented transactions. Isn’t there a risk that it’ll actually hurt rollups?

At high congestion times (e.g. big NFT sales) rollup transactions will be constantly dropped, and they’ll have to compensate for the lack of execution gas by paying a higher total fee. Theoretically it should drive rollup gas fees to the current cost, except that it also limits the calldata size. The additional constraint might require them to pay an even higher fee to outbid other rollups competing on the same calldata space.

---

**alexkrusz** (2021-11-25):

While ostensibly simple, it could be argued that the calldata limit is an architectural decision with greater implications than just modifying a gas constant. An arbitrary limit on calldata per block seems like complexity that could be avoided by just giving calldata the proper gas cost such that it doesn’t present a significant risk.

If there is an arbitrary limit imposed, why not make it a soft limit, or impose it on the entire block size rather than on calldata specifically?

---

**axic** (2021-11-29):

I wonder if something like [EIP-2242: Transaction Postdata](https://eips.ethereum.org/EIPS/eip-2242) would be useful in combination of the above, where non-executable/non-accessible data is counted differently.

Summoning [@adlerjohn](/u/adlerjohn) ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=10)

---

**stevengcook** (2021-11-29):

> Add a rule that a block is only valid if sum(len(tx.calldata) for tx in block.txs) <= BASE_MAX_CALLDATA_PER_BLOCK + len(block.txs) * CALLDATA_PER_TX_STIPEND.

Would it not be easier (and slightly less variable max calldata per block) if only transactions with more than `CALLDATA_PER_TX_STIPEND` are counted against `BASE_MAX_CALLDATA_PER_BLOCK`?

Assuming 300 is the stipend per block, transactions with <= 300 calldata won’t provide extra room for transactions that use > 300 calldata.

---

**BitMEXResearch** (2021-11-30):

I was told to ask these questions here:

1. I am trying to understand why the so-called “multi-dimensional complexity” problem associated with this proposal only applies to block producers. Don’t users and wallets also have a potential issue here, as they need to analyse the two dimensions when setting the tip/fee?
2. Does this proposal somewhat undermine EIP-1559, because the base fee can vary based on the total gas usage, but not total calldata usage. Therefore, might this cause fees to be volatile like pre EIP-1559?

---

**yoavw** (2021-11-30):

Could we achieve the same goals without the total calldata limit by reducing the cost of calldata and simultaneously increasing the cost of calldata access in EVM, beyond a certain size?

1. Remove the calldata limit.
2. Make the cost of calldata read quadratic (with a minimum that keeps the pre-fork cost intact), based on the highest offset accessed.  The quadratic function only starts increasing the cost above the minimum, if the highest offset is 2x the current average (excluding rollup transactions).

Pro: it removes the hardcoded limit.

Con: Adds some complexity to the EVM implementation - calculating the calldata read cost based on the highest offset accessed, rather than using a fixed cost.

Would this achieve the same goals?

---

**aliatiia** (2021-12-02):

I was wondering something similar. Instead of **blanket reduction** in `calldata` gas cost as per EIP-4488, extend [EIP-2242](https://eips.ethereum.org/EIPS/eip-2242) to allow EVM access to `postdata`. Then, impose restriction such as total gas used by the execution on the data.

To simplify this restrictive exec environment, create a precompile that allows `DELEGATECALL` to supplied contract (such as SNARK verifications by ZK Rollups). Precompile only extends a hardcoded `MAXGAS` to the callee. An EIP-2242-type tx only has access to said precompile.

Note that backward compatibility of non-EIP-2242-type transactions is a breeze thanks to [EIP-2718](https://eips.ethereum.org/EIPS/eip-2718), i.e. a new envelope.

---

**vbuterin** (2021-12-02):

I think at this point pretty much anything other than a two-line change in the style of EIP-4488 or 4490 is just too complex and not going to make it for that reason alone. The whole point is to make a quick-and-dirty solution because rollups need it fast fast.

The longer-term solution (or I guess medium-term solution) is to implement the beacon chain sharding spec (which is not that complicated) and only turn on 1-4 shards so we get some dedicated 2 MB space per block with its own efficient fee market and because there’s only a few shards nodes can still fully validate availability and we don’t have to worry about p2p networking.

> Assuming 300 is the stipend per block, transactions with  300 calldata.

I would say the main issue with this approach is that it would reduce the average-case maximum without reducing the worst-case maximum, so it risks decreasing total scalability.

> I am trying to understand why the so-called “multi-dimensional complexity” problem associated with this proposal only applies to block producers. Don’t users and wallets also have a potential issue here, as they need to analyse the two dimensions when setting the tip/fee?

Technically only if the tx has more than 300 bytes, and even then if they keep setting a low priority fee their tx would just float around for a few extra blocks until a block that’s <25% full comes along (which happens quite frequently). Use cases that involve txs with a really huge amount of data (primarily rollups, but also contract creations) may require some special logic eventually, but only if block sizes start actually regularly getting to the calldata limit.

---

**jflo** (2021-12-03):

Is “calldata” a potentially overloaded term? In my discussions, a couple of devs (myself included) jumped to the assumption that this was modifying the CALL(0xF1) opcode and its friends. We are really talking about the payload data initially set on a transaction, which some devs think of as “intrinsic transaction cost”. Regardless of where the transaction is going, we know it’ll cost this amount.

This is an aesthetic observation, but perhaps NEW_CALLDATA_GAS_COST would be better named NEW_TX_PAYLOAD_GAS_COST ?

---

**adietrichs** (2021-12-10):

I looked into the effect of different stipend sizes on miner profitability under several mining strategies:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/d/d8dffc4922862e19cc0a1b08fc5f2ca811627b76.png)

      [HackMD](https://hackmd.io/@adietrichs/4488-mining-analysis)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



# EIP-4488 Mining Strategy & Stipend Analysis  ## Summary  This is an auxiliary analysis for [EIP-44










**tl;dr**: Even a moderate stipend size (e.g. 260 bytes looked good) leads to over 99% includable transactions (and an almost optimal profitability) when using a simple backlog mining strategy. And because those 99% already include current-day “big calldata” transactions (i.e. mostly rollups), “normal-sized” transactions should basically never end up being left out due to calldata constraints.

---

**tfalencar** (2021-12-14):

TLDR; as a dapp developer, I’m pro shipping EIP-4488 (or 4490) + EIP4444 ASAP, not necessarily at the same time. Better pre-merge, but if merge comes soon, right after merge would be great - but I do hope it comes soon, meaning even before enabling stake withdrawals.

Now to the long answer (too long, sorry!) - this is also kind of a reply to geth’s devs document comments on this eip.

As someone who feels aligned with Ethereum’s core design values and philosophy, and as someone working on a new dapp, I *really* hope to see this EIP included soon.

At least at the start of the Ethereum project, the message I got was all about applications you could build on top of it. This is what got me excited, not number go up, or some other monetary detail. The reality however nowadays is that its economically too expensive for many dapps (even on L2s!). I guess everyone here knows the reason why, but I wish there were more voices from the users, dapp devs, and to why Ethereum exists in the first place. I think we all want to see positive impact in real life, yet the network can only afford to serve “whales” today- no wonder defi is currently the main type of applications on Ethereum.

I’m pro this EIP not only because it may make my dapp be finally viable for my prospect users, but also in thinking about the opportunity loss of other projects that never came to existence due high fees. Or those that went somewhere else, which fragments the ecosystem: I find this to be a real technical problem - the exponential amount of bridges required between all L1s etc is becoming a mess for developers to handle. If only there was a shelling point (or a few) for developers, where one gets a secure environment - or at least a theoretical path to it (L2), yet reasonable gas fees? Could that shelling point finally be within Ethereum ecosystem again? EIP4488 is a step in that direction.

In my view 4488/4490+4444 is a much needed eip combo that will actually *increase* decentralization: removing the burden of storing historic data forever will allow newer EL clients to pop up and be a reasonable challenge again. It will also further incentivize development of networks like Portal, Swarm, and specialized clients. Nowadays geth core team is burdened for being majority of the network, but the irony is that although it is a massive achievement of performance from the geth team, not dropping historical state works against the problem of too much responsibility:

This EIP (and specially 4444) I feel will actually  start driving more client diversity because today, many are in their “comfort zone” of “just using geth/Erigon” for historic data instead of contributing to history state solutions.

I 100% agree with Vitalik we can have a gradual approach and get some of the benefits early (in a pragmatic way) by releasing one eip then the other, then working on sharding, step by step. Though I understand geth’s team worry of pushing the problem for solving later. However this just means we need to be sure we can implement 4444 in reasonable time, and have it somewhat ready earlier. The pragmatic approach of working in parallel and releasing features step by step has proven very successful in the last 3 years or so, instead of waiting for a perfect system from the start which would then take 10 years.

In the all core devs call Vitalik suggested asking the community something along the lines of:

“Would you be willing to break apps that demand data older than one year, in order to get a 2x reduction in rollups? “

Absolutely! First because most existing/established dapps are either already relying on networks like the graph, or some other custom solution, so I expect them to actually not break. The few that do break, now will look for other history state retrieval solutions (potentially contributing to them).

if we think about making the network more accessible, well established dapps have the resources to maintain archive nodes and serve their specific data for a long amount of time. While projects that are starting don’t have any data on chain yet and can still survive for a while without additional infrastructure (due the subsidized 1 year pruning time of 4444). Not doing these EIPs on the other hand, leaving high tx costs combined with bad timing, may well be the make or break point for these newer / smaller projects, or they just build somewhere else, causing “brain drain” for this lovely community.

There is a long tail of projects that are currently being priced out. This eip may provide the breathing air for Ethereum’s “escape velocity” not loose it’s strength and keep compounding network effects.

Sorry for the wall of text, but I hope this was helpful. Whatever the devs and the community decides, I’m cheering for you all and keep up the great work!

---

**jpitts** (2021-12-20):

Position by the Geth team, published here: https://notes.ethereum.org/EH_xVCD8SnaLCEDrXxUyYA?view

(full statement copied below)

---

This document summarizes our (the geth team’s) position on [EIP-4488](https://eips.ethereum.org/EIPS/eip-4488). We are

**against** the inclusion of this EIP in a fork before the merge.

EIP-4488 is a tweak to the economic balance of Ethereum. It does not enable anything

that’s currently impossible, the change just makes it more economically feasible. Such a

change should not be hastily implemented ahead of an already scheduled major fork.

### Technical Concerns

Decreasing the costs of data-heavy transactions will make typical Ethereum transactions

more expensive, favoring L2 transactions. This might be fine, but it may also be a

non-obvious side effect that users should be aware of.

Specifically, we fear that EIP-4488 will, due to the 2-dimensional nature of the scheme,

favor rollup transactions so much that it won’t be possible for non-rollups to use the

blockchain. The EIP should present significantly more evidence that this will not be the

case.

At this time, EIP-4488 attempts to keep usage balanced by allowing transactions smaller

than 300 bytes even when the block size limit is already reached. While the exception will

allow for simple value transfers to be included alongside a data-heavy rollup transaction,

any transaction larger than 300 bytes needs to outbid all rollups for block space.

While the EIP limits the worst case block to the same size as it is currently, the average

size will be incentivized to gravitate towards the worst case. One does not simply propose

adding 3 TB of chain data growth per year without providing a working technical design for

storing this data. Referencing [EIP-4444](https://eips.ethereum.org/EIPS/eip-4444), noting that it should be ‘implemented

either at the same time or soon after’ is not a suitable way to deal with this problem

because EIP-4444 is not easily implementable.

EIP-4488’s issues are not limited to storage problems caused by chain growth. It is also

important to verify experimentally whether block propagation will survive the jump to 1.5

MB block sizes.

### About Rollups

As noted in the EIP’s motivation section, the goal of the change is making rollup

implementations cheaper. However, all existing rollup schemes are either insecure, or not

fully trustless. Incentivizing people to use them might be too early because they don’t

guarantee the same or similar security as L1.

The current L2 landscape is summarized on [l2beat.com](https://l2beat.com). Checking the page for

[information about the most popular system ‘Arbitrum’](https://l2beat.com/projects/arbitrum/) (claimed to have 41% market

share), we find it relies on a single centralized validator and contains a zero-delay code

upgrade feature in its main contract.

More research into EIP-4488 can mitigate our concerns. Nonetheless, the fact that more

research is needed should prevent immediate inclusion of this EIP.

---

**dylanetaft** (2021-12-20):

So this helps dapp developers by lowering gas costs.

It’s probably neutral for miners with EIP-1559 in place…

Without EIP-4444, it is outright harmful to archive node operators, isn’t it?

Does EIP-4444 propose that historical nodes will not sync calldata?  So, if new nodes join the network after a l2 network started rollups > 1 yr ago, the l2 chain becomes sort of unverifiable or the state of the l2 chain cannot be re-calculated?

What is wrong with current methodology - bridges and wrapped tokens?   Why does L1 need to validate(poorly, if historical nodes are not keeping calldata) private purpose L2 networks?  L2 could be responsible for verifying itself.   Bridge middleware isn’ fully defi when tokens are being wrapped and staked in one contract to move to another chain.  That’s OK though, problems only impact the token or NFT being wrapped…

I still support it with EIP-4444 in place, just because it brings the cost of actually USING EVM down on L1, for everyone, hardware costs and gas costs.

I’m for it, but waiting excitedly for sharding and what that means.

I might even also propose an additional EIP.

Since EIP-3529 got rid of the mechanism that disincentivizes people from storing unneeded data on l1 chain(because people were abusing it in the form of gas tokens) - why not make it so smart contracts have to actually hold a balance of ethereum based on the amount of contract memory consumed?  If the balance isn’t high enough, maybe make non-view functions not work.  Maybe make the contract self destruct after a year of not a high enough balance?

This might be more in line with paying cloud providers for service - storage isn’t free month to month.  Where’s the skin in the game beyond initial gas costs for deploying data?

That could work, or maybe contracts have a persistent gas tank where gas is just used over time, and no refunding it, only refilling.

Edit:  Some of this is answered above.  EIP-4444 is not easily implementable.  EIP-4488 is a tweak to the economic balance of ethereum, which is basically what I said, favoring different parties.

I wonder if the gas tank idea would work if wallets just determined the criteria was met for a contract and executed a virtual selfdestruct message with gas sent to address 0.  Maybe the gas needed in the tank can be calculated algorithmically based on time or block count.    Or maybe even deposited ethereum would work.  Or any transacting at all by anyone, since that’s already stored.  Contracts should have gas spent on them occasionally indicating actual use, shouldn’t just sit.  Or maybe finding unused contracts and destruct rewards could be sent to miners or validators if their block gets chosen, leave those running nodes out of it.

---

**qizhou** (2022-04-27):

We have implemented EIP-4488 on our Ethereum-sidechain testnet on Geth!  The code is here [impl EIP4488 for pisa by blockchaindevsh · Pull Request #74 · QuarkChain/go-ethereum · GitHub](https://github.com/QuarkChain/go-ethereum/pull/74).  We plan to upgrade the testnet next month and will share our results thereafter ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**lyt** (2022-11-04):

What’s the word on this?

---

**Madhav** (2023-03-04):

Hey was checking the eips website, is this proposal sidelined right now or active in development? Seems like a lot of folks building on rollups are looking forward to this.


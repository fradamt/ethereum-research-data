---
source: ethresearch
topic_id: 10980
title: Two-slot proposer/builder separation
author: vbuterin
date: "2021-10-10"
category: Proof-of-Stake
tags: [proposer-builder-separation]
url: https://ethresear.ch/t/two-slot-proposer-builder-separation/10980
views: 27707
likes: 28
posts_count: 27
---

# Two-slot proposer/builder separation

_See previous ideas on this topic: https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs/9725_

### Sequence of events in a slot pair

- Right before 0 seconds - exec header publishing: anyone can publish an exec header, which contains an exec block hash, a bid, and a signature from the builder
- 0 seconds - beacon block deadline: beacon block must include the winning exec header
- 0-2.67 seconds - attestations on beacon block: only one committee attests to the beacon block
- 8 seconds - intermediate block deadline: the winning builder publishes an intermediate block, consisting of the exec block body and as many attestations on the beacon block as they can find
- 8-10.67 seconds - attestations on intermediate block: the remaining N-1 committees attest to the intermediate block
- 10.67-13.33 seconds - aggreation of intermediate block attestations
- 13.33-16 seconds - next exec header publishing

If a beacon block is missing, the next slot is switched to be for a beacon block instead of an intermediate block.

### In diagram form

[![](https://ethresear.ch/uploads/default/original/2X/a/a4a8897d786101aa77bcaa790b424ad8430c9717.png)1162×277 12.9 KB](https://ethresear.ch/uploads/default/a4a8897d786101aa77bcaa790b424ad8430c9717)

### Key intuitive properties

- From a fork choice perspective, the system can be described as a beacon chain just like the current one, except with uneven committee sizes and with a (block, slot) fork choice. The only difference is that some of the blocks are only there to select proposers for the block right after them. This simplifies analysis.
- A committee in between each step helps to ensure that each step is “safe” and reduces vulnerability to abuses by single actors

### Safety properties for builders

At the bid publishing step, builders see the head, and know whether it’s **safe** or **unsafe** (a head could be unsafe if there are lots of disagreeing or missing attestations).

- If a head is safe, the head cannot be reverted barring a 45%+ attack, significant amounts of slashing, or extreme network latency. In this case, builders can feel confident bidding safely.
- If the head is unsafe, there is a risk that the chain could be reorged after they release their body, “stealing” their MEV opportunities. In this case, builders see this risk and can decrease their bids to claim a risk premium for this risk.

At time of intermediate block publishing, there are two cases:

1. The beacon block has not been published. In this case, the attestation committee will have voted against the block, and so the intermediate block producer (aka. the builder) can safely not publish, and will not be penalized.
2. The beacon block has been published. In this case, the intermediate block has a “proposer boost” slightly greater in size than the entire attestation committee, so if the builder publishes, their block will win in the eyes of the remaining N-1 attestation committees.

This ensures that if the attestation committees are honest, and latency is not extremely high, the builder is guaranteed to:

1. Get included if they publish
2. Not be penalized if they do not publish because the beacon block header is missing

The builder has a period of ~5.33-8 seconds during which to publish. They can safely publish as soon as they see the beacon block; however, they may want to wait until they see more attestations, as they get rewarded for including attestations (attesters that get included also get a reward themselves). They are free to negotiate the tradeoff between (5.33 second window, get attestation inclusion reward) and (8 second window, get no attestation inclusion reward) as they wish.

### Beacon chain spec change sketch

#### Proposer index definition

- Set get_random_proposer_index(state: State) to what get_beacon_proposer_index(state) returns today.
- Add state variables chosen_builder_index and chosen_exec_block_hash. If a slot is empty, set state.chosen_builder_index = NO_BUILDER (a constant equal to 2**64 - 1). If a slot contains a beacon block which contains a BuilderBid, set:

state.chosen_builder_index = builder_bid.message.builder_index
- state.chosen_exec_block_hash = builder_bid.message.exec_block_hash

Define `get_beacon_proposer_index(state: State)` as follows:

- If state.chosen_builder_index == NO_BUILDER, return get_random_proposer_index(state)
- Otherwise, return state.chosen_builder_index

#### Conditions on bid-carrying block

- If state.chosen_builder_index == NO_BUILDER, the block is required to contain a BuilderBid and may not contain an ExecBody. The builder_bid is required to pass the following checks, whereval = state.validators[builder_bid.message.builder_index]:

bls.Verify(val.pubkey, compute_signing_root(builder_bid.message), builder_bid.signature)
- val.activation_epoch == FAR_FUTURE_EPOCH or val.withdrawable_epoch = builder_bid.bid_amount

Add a balance transfer to the processing logic:

- val.balance -= builder_bid.bid_amount
- state.validators[get_beacon_proposer_index(state)].balance += builder_bid.bid_amount

Change `get_committee_count_per_slot` to take inputs `(state: BeaconState, slot: Slot)` (instead of epoch). If a slot has `state.chosen_builder_index == NO_BUILDER`, the committee count should return 1.

#### Conditions on exec-body-carrying block

- If state.chosen_builder_index != NO_BUILDER, the block is required to contain an ExecBody and may not contain a BuilderBid. The exec_body is required to pass the following checks:

hash_tree_root(exec_body) == state.chosen_exec_block_hash
- eth1_validate(exec_body, pre_state=state.latest_exec_state_root)

Add to the processing logic:

- state.latest_exec_state_root = exec_body.post_state_root

The `get_committee_count_per_slot` should return `(get_epoch_committee_count(epoch) - state.committees_in_this_epoch_so_far) // (slots_remaining_in_epoch)`
If `state.chosen_builder_index != NO_BUILDER`, set `state.chosen_builder_index = NO_BUILDER`, regardless of whether or not there is a block.

#### Notes

- Reduce slot time to 8 seconds (remember: 1 exec block will come every 2 slots)
- All beacon blocks, including bid-carrying and exec-carrying, should get a proposer boost in the fork choice.
- Fork slot should be changed to (block, slot).

### Possible extension: delayed publishing time with a fee

If the intermediate block builder does not publish during slot N, no bundle is selected in slot N+1. The entire proposer sequence gets pushed back by one slot (so the slot N+1 proposer becomes the slot N+2 proposer, etc), and a new random proposer is chosen for slot N+1. The builder gets another chance (so, an extra 12 seconds of slack) to publish. The slot N+1 exec block cannot contain any high-value consensus transactions (ie. slashings). However, they get penalized `block.basefee * block.target_gas_limit`.

The intuition is that they are delaying their exec block by one slot and prepending it with an empty exec block, so they need to pay for that slot. The proposer sequence being delayed ensures that delaying one’s exec block is not useful for stealing future proposal rights in times when they are high-value.

### Possible extension to shards

[![](https://ethresear.ch/uploads/default/optimized/2X/e/e133abd7bccda4f522be28cf23fc975843dd0b0e_2_690x236.png)1158×397 24.9 KB](https://ethresear.ch/uploads/default/e133abd7bccda4f522be28cf23fc975843dd0b0e)

## Replies

**pmcgoohan** (2021-10-11):

Let me illustrate my objection to the basis of this proposal:

You spend $1000 on a safe. Worried that a burglar might damage it by trying to get at the valuables inside, you take out the $1,000,000 of gold it contains and leave it in the street.

Breaking down why this is a poor strategy:

- The safe is worth less than the gold, so you need to protect the gold not the safe.
- The safe has no utility if you don’t use it to protect the gold.

Block proposer/builder secures the empty safe (blockchain structure) at the expense of the gold (blockchain content).

It formally omits transaction inclusion and ordering from the consensus on the basis that it threatens the structural security of the blockchain, but the reason it increases the risk of a consensus attack is precisely because it is worth protecting from those trying to do so.

The proposal (correctly) admits that MEV extraction is centralizing, hence trying to mitigate it in the structural layer.

But in doing so it actually facilitates the centralization of content, the endgame of which is its monopolization by a handful of wealthy, well resourced actors with their own agenda, ie: the antithesis of blockchain technology.

Our security assumptions will have fallen from requiring 51% of the hashpower (or thereabouts) to co-opt the chain, to simply being the best at extracting MEV, having the most money or even just having the greatest motive (or being close enough to all three).

No-one will ever have 51% of the stake/hash power (hopefully). Someone is always best at extracting MEV, and someone is always the richest, therefore it is guaranteed that at least one actor is always in a position to monopolize the content of the network according to their agenda.

[@fradamt](/u/fradamt) spoke similarly in this [excellent post](https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs/9725/33). Your response that such as attack is uneconomical does not account for the fact that censoring transactions can have large and unquantifiable private value to the censor and that once established that value may be self-reinforcing. Allowing the proposer to add a small number of transactions to mitigate this will simply incentivize an informal secondary auction market which they can also dominate.

Rather than excluding transaction ordering and inclusion ever further from consensus, it seems to me that we must look at consensus mechanisms that include it.

---

**vbuterin** (2021-10-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> Your response that such as attack is uneconomical does not account for the fact that censoring transactions can have large and unquantifiable private value to the censor and that once established that value may be self-reinforcing

I don’t think this quite captures the extent of the argument for why the attack is uneconomical. The attack is not “uneconomical” in the sense of “you earn $50 instead of $100”; if that was the case, of course attackers would often be willing to take the earnings hit. Rather, the attack is “uneconomical” in the much stronger sense that if `fees(censored_txs) > fees_and_mev(best_builder_block) + fees_and_mev(best_honest_builder_block)`, then **the builder would have to burn a large and ever-increasing amount of ETH *per block* to keep up the censorship**. Victims of the censorship could even raise their priority fees to push this censorship even higher.

Some concrete numbers:

- Average MEV per block this year: ~0.1 ETH (taken by dividing the values in the cumulative chart on this page by ETH price and then blocks per day)
- Average priority fees per block since EIP 1559: ~0.3 ETH (taken from this data)
- Average base fees per block since EIP 1559: ~1.1 ETH (taken as total amount burned / days since EIP 1559 / blocks per day)

Suppose now that the best MEV collector is 25% better than the best open source (or at least honest) MEV collector. Wallets broadcast transactions as widely as possible, so everyone gets those. They collect 0.4 ETH per block without censoring, the next best alternative collects 0.375 ETH per block.

Now, suppose some they start wanting to censor 1% of users. Suppose these users triple their fees to get included, so they pay `(0.011 + 0.003) * 3 - 0.011` = 0.031 ETH per block. That alone is already greater than 0.025 ETH per block, and so the censor would have to pay an extra 0.006 ETH out of pocket to outbid the honest builders and exclude them from the block. *But that’s only for the first block*. After 100 blocks, there would be a backlog of censored txs, equal in size to the entire block. At that point, the censor would have to pay ~3.085 ETH per block to exclude all of them. Hence, the cost of censoring ongoing activity blows up quadratically for the censor.

Additionally, censorship victims can “grief” the censor by simply increasing their priority fees even further, and the victims get an *extremely* favorable griefing factor of `1:n` where `n` is the number of blocks by which the censor wants to delay the transaction.

**Edit: an even simpler intuitive argument is that a malicious builder can only censor `1/n` of users for `n` blocks until the censored users have a big enough backlog of transactions to outbid everyone else for an entire block.** Though this is only a lower bound, as seen above censorship can easily break much faster.

---

**vbuterin** (2021-10-11):

My main concern with “putting transaction ordering in consensus” approaches is that it puts *a lot* of pressure on a mechanism that could easily have a lot of instabilities and a lot of paths by which the equilibrium could collapse. One simple sketch of such a mechanism is: attesters refuse to vote for a block if that block fails to include a transaction (i) which the attester has seen for at least a full slot and (ii) whose priority fee is more than 1.1 times the lowest priority fee included in the block.

The main question is: what’s the incentive to actually enforce this rule? If an attester sees that a given block fails to include a transaction that it should have included, but then it sees other attesters voting for that block, it’s in the attester’s interest to also vote for the block, to get the attestation reward. These “follow the crowd” incentives could lead to block inclusion rules becoming more and more slack over time, until no one checks at all. It may even be possible for attackers to submit txs that satisfy the conditions for some attesters and not others, thereby splitting votes 50/50. Having attesters only concern themselves with blocks, and not transactions, avoids all of these issues, because there are far fewer objects that could manipulate the fork choice in this way, and it’s more clearly expensive to create 50/50 splits.

---

**pmcgoohan** (2021-10-12):

Thank you for engaging [@vbuterin](/u/vbuterin). I’m going to describe a few different attacks that I see as being possible under PBS/MEVA. I’ll do this across several posts, mostly to give myself time to write them up. Finally I’ll respond to your insightful post on consensus, which may take me longer.

#### Attack 1: Secondary Censorship Market

As you rightly point out, it becomes increasingly expensive for the dominant extractor to censor perpetually for their own ends, in most cases prohibitively so.

A participant must coincidentally be one of the best at extracting MEV, as well as having a good reason and deep pockets if they are to censor other participants continuously.

But the requirement for a coincidence of this kind is trivially solved by markets, and this is what I see happening.

The dominant extractor runs a secondary market allowing users to bid to exclude transactions from a block. It’s like an inverted PGA. You send the hash of someone else’s transaction that you *don’t* want to be included and a bribe. The dominant extractor will only consider your bribe if it is more than the gas (and MEV) that they would have received for inclusion, therefore they will be guaranteed to profit from it.

But the situation is worse than this because the dominant extractor can also offer a protection service allowing users to send the hash of a transaction that they want this censorship cancelled for. This will only be considered if it is more than the highest censorship bid for this transaction.

If the dominant extractor runs a lit market, users will be able to see if their transactions are being censored and can outbid their attackers to be included. This will lead to a bidding war with two losers (the users) and one very wealthy and ever more dominant winner (the dominant extractor).

If they run a dark market, users will have to guess whether their transaction might be censored or not and will often pay for protection they don’t need.

The dominant extractor will run whichever market type (lit or dark) is the most profitable for them, and possibly both.

In this way, many censoring participants can target individual transactions for only as long as they require censorship, but the dominant extractor can remain in power indefinitely simply by being the best at running this censorship market and pretty good at extracting MEV.

It works because the censorship/protection market acts as an efficient way of extracting private MEV (eg: censoring competitor transactions), as well as public MEV (eg: DEX arbs etc), a distinction I will discuss later.

Crucially, only those extracting this extra value by selling censorship/protection as a service will be able to afford to win blocks.

They will have won dominance over blockchain content by necessarily being the most exploitative. As well as the centralization that comes from this additional censorship profit, any network effect around their censorship market will act to further centralize around them.

Before long Flashbots will need to decide whether they are willing to cross the line and offer transaction censorship/censorship protection services to customers (something they weren’t with reorg markets for example), or lose their dominance of the hashpower.

---

**vbuterin** (2021-10-13):

What types of victims of censorship are you concerned about specifically?

It’s clear that you can’t censor significant quantities of transactions forever: you can only censor `1/n` of users for `n` blocks until the censored users have a big enough backlog of transactions to outbid everyone else for an entire block and get in. So we’re looking for transactions where there is an incentive to delay them for 1-30 minutes, and where the benefits from delaying others can’t also be achieved by just frontrunning them. Liquidations?

One alternative strategy for mitigating this is to run multiple auctions in parallel, where the secondary auctions are auctioning off the right to get a transaction force-included after 1 minute. This could even mean eg. allowing each shard proposer to include one base-layer transaction in their proposal. The basefee on these markets could be increased by 1.5-2x to make them emergency-only and thereby make sure that they don’t bring back proposer economies of scale. Even running a few such auctions would greatly increase the cost of censoring users, because the censor would have to outbid the sender’s expected bid in every location. I wonder what you think about that approach.

---

**pmcgoohan** (2021-10-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What types of victims of censorship are you concerned about specifically…we’re looking for transactions where there is an incentive to delay them for 1-30 minutes, and where the benefits from delaying others can’t also be achieved by just frontrunning them

I can’t think of an Ethereum use case that would not be victimized by a censorship market (beyond basic p2p currency/NFT transfers).

Frontrunning is bad, but smart contracts can be written to mitigate frontrunning within a block. They cannot be written to mitigate n-block censorship.

If Defi moved to batch auctions it would avoid all intra-block MEV because it renders time order irrelevant. Censorship undoes app level mitigations like this, because you can’t batch up transactions that never made it into the chain in time.

I’m still pondering this, but it may be that the logical conclusion of a censorship market is that much of the business conducted on Ethereum will give all of its profits to the dominant extractor.

Imagine a retail smart contract matching buyers to sellers:

- A user sends a transaction ordering ice-cream and two businesses (A and B) send transactions to fulfill it.
- They both sourced the ice-cream for $2 aiming to sell it for $4.
- A censors B for $0.50.
- B protects themselves for $1, and then censors A for $0.50.
- A protects themselves for $1, and then censors B for $1.99.
- They can’t go any higher.
- B loses the transaction.
- A wins the business, but pays all of their profits to the dominant extractor.

If you see this as prisoner’s dilemma, the dominant extractor always wins (I guess arguably it is iterative).

Not only that, but one way to win is to *raise* your price to the customer. If B had offered the ice-cream for $5 instead, they would have been able to afford to censor A and the customer would have paid $1 more.

I’m not sure that business is possible in an environment as exploitative as this, especially when less-extortionate centralized alternatives exist.

And this is the problem, I think that PBS/MEVA stop Ethereum being useful.

Instinctively I prefer your consensus mitigation idea despite your reservations about it, but your alternative strategy looks interesting- I need to think it through.

*EDIT: updated to show that it is the dominant extractor / censorship market operator that profits, not the miners*

---

**imkharn** (2021-10-18):

RECAP OF ABOVE:

I struggle a bit understanding this discussion, but I think I have the general idea. Vitalik is able to show that a continual censorship scheme will fall apart as valid but delayed txs build up. pmcgoohan points out that only a short term censorship is needed to extract MEV, and that by making short term censorship as a service easier, this will increase the centralization and MEV extraction that the original proposal was thought to reduce.

FIXING ICE CREAM SALES:

To this discussion I want to add a minor point to the ice cream example that both ice cream sellers can instead have a bidding war of credible commitments to censor should the competition attempt a transaction to sell their ice cream. Such credible commitments would deter the other party from attempting the tx, and the price for a credible commitment is nearly free, so the ice cream sellers could easily avoid sending all of their profits to the miner. To prevent one ice cream seller from overcharging, the buyer that is aware of fair price can set a maximum price, or the sellers could make a credible price commitment in advance. I think these together solve the ice cream problem, but I did not take the time to consider if solutions down this route are practical to be generalized across all kinds of MEV.

TIME INCLUSION MARKET INTRO:

Something I came up with several months ago is a guaranteed time based inclusion market. I mentioned to some coworkers and a tweet, but this seems like a good time to pitch the concept because it may assist in mitigating or solving the problems discussed here.

It could be done with on the smart contract layer though with additional gas costs, but would be better as an offchain service and even better as a protocol level improvement. Where it is appropriate to implement is another question that can come later. For now I just want to pitch the mechanics of such a system.

RAISON D’ÊTRE:

It started when it occurred to me I often have transactions where I do not care about when they are processed as long as they are processed within the next 24 hours. If the overall cost to me is lower than the slow gas cost, yet I also have a guarantee of inclusion, I would be willing to pay for this guarantee. So would many others. Selecting a time limit for transaction processing is also a better user experience, as this is actually what users care about. Wallets know this and present to user guesses of inclusion time, but predictions fall apart mere minutes into the future. To the point where wallets don’t even bother suggesting a gas price for more than 10 minutes into the future. Even under 10 minutes there exists uncertainty that users would pay to eliminate but have no venue.

METHODOLOGY:

Those willing to take on gas price exposure select from analogue spectrum of time frames and for each time they select, they offer a price. For example, for 10 minutes in the future, they may select 80 gwei. For 1 hour they may select 70 gwei, and for 24 hours they may select 60 gwei. They select these prices because in their estimation and possibly by comparing competing bids have predicted on average they will be able to include the transaction within the specified time for less than the offered price. To incentivize the guaranteers to process the transaction even at a possible loss, they are required to place a bond such as 10 times the contracted rate. The user gets the entire bond should the transaction not get processed in the contracted amount of time.

Other inclusion offerers will also select various times and make commitments. To link together multiple arbitrary times with different arbitrary prices, the protocol can assume a linear transition between each offers. For example, if a guaranteer specified 70 gwei for 1 hour and 60 gwei for 24 hours, then the protocol assumes that they are also offering to process a transaction within 12 hours for 65.2 gwei. Essentially each guaranteer that makes 2 or more offers is also making an offer for all time choices between their offers.

The user then can see the best price offered by any guaranteer for any arbitrary time and contract with them. If they want their loan repayment transaction to get processed within the next 22.7 hours, they will have someone to guarantee that for them, and they will be able to get a price better than metamask would have offered for a 10 minute inclusion despite the on average profit the guaranteers are making. I believe adding this optional layer on top of any transaction bidding system would be preferred by all users to the point a large portion would use it.

Such a system would also improve resistance to censorship. A miner would be aware of the guarantee and would know for sure the guaranteer is willing to spend up to the bonded amount bypassing the censorship to get the transaction through.

In the context of censorship though some subgames would probably arise and I have not mentally applied this extensively to the impact on censorship yet. Perhaps the miners try to stop the guaranteer from making the contract, perhaps the guaranteer can tell that an incoming transaction is likely to be censored and doesnt want to make the deal, perhaps the protocol forces the guarenteers to be neutral and accept all offers to prevent this. Lots of depth here, but for now just want to start off with pitching this idea that I think will improve any blockchain especially if it was built into the base protocol as an optional transaction type.

---

**pmcgoohan** (2021-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What types of victims of censorship are you concerned about specifically?

I wrote the ice-cream example in a bit of a hurry. A good real-world example of a high value, p2p target for the censorship market is the Wynvern protocol underlying many of the big NFT trading platforms like OpenSea, Cryptokitties etc.

Hi [@imkharn](/u/imkharn),

![](https://ethresear.ch/user_avatar/ethresear.ch/imkharn/48/5564_2.png) imkharn:

> To prevent one ice cream seller from overcharging, the buyer that is aware of fair price can set a maximum price, or the sellers could make a credible price commitment in advance

Whatever maximum fair price they set is what they’ll pay. Price discovery has failed at this point.

The sellers may collude (not that we really want to incentivize cartel behaviour in our sellers) but may just as well defect, especially in p2p markets where sellers have no history and little chance of interacting again. You’ve just added a second game of PD with the same expected outcome.

In addition, even when the sellers are colluding the dominant extractor can stir up trouble by censoring a seller themselves. There will be no way for the censored seller to tell whether this was done by the other seller defecting or the dominant extractor (who is incentivized to break the cartel), but they will likely assume the former and defect.

Thank you for contributing a mitigation idea. If you’ll forgive me, I won’t get into it yet. I am still working to define the problem at this point before moving onto potential mitigations.

---

**pmcgoohan** (2021-10-19):

#### Attack 2: Centralized Relayer

I am going to describe how PBS incentivizes centralization around a private relayer. This is a generalized attack on decentralization.

MEV auctions are highly competitive because the mempool is public. There is nothing to differentiate one searcher from another beyond their ability to extract MEV from the same set of transactions. As a result, searchers bid each other up and give the majority of their profits to the miners in order to win blocks.

A far easier way for a searcher to dominate block auctions and profit is to have access to a private pool of transactions which only they can exploit. Quite simply, having more gas available for their block proposals than their competitors means they can afford a higher bid. Here is a [simple spreadsheet model](https://docs.google.com/spreadsheets/d/11lox9zZQ3UBWZj1liyQni8wYluh85NY5Y0-IseeXjq4/edit?usp=sharing) demonstrating this.

Crucially, the extra profit from transactions sent through their private relayer is theirs to keep, they don’t need to pay it to the miners because other searchers can’t compete for it.

This creates a very strong economic incentive for searchers to operate private relayers. Something similar is already happening with initiatives like Flashbots Mev Protect, MistX and Eden, for example.

A private relayer would be wise to invest a lot upfront in advertising, PR, token drops, offers of MEV protection and even gas subsidies. As with the [censorship market](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980/5), there are strong network effects and feedback loops around private relayers once a critical mass is achieved. People will use the private relayer that wins blocks most of the time, which in turn means that they can win blocks more of the time, which means more people use them, and so on.

Once dominant, the private relayer has monopolistic gatekeeping powers that will be extremely difficult to challenge.

A private relayer is fully compatible with a [secondary censorship market](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980/5) which they must also run to remain competitive.

The mempool is increasingly redundant, along with the decentralization, transparency and accountability it provides, so any additional manipulations the dominant extractor performs are hard to track.

A single, opaque organization with no requirement to have any stake in Ethereum will have ownership of the majority of the order flow in the network, with no protocol enforced limitations on how it is used.

#### Mempool Griefing

The following is not necessary for private relayer dominance, but we can expect behaviour of this kind.

The mempool is a threat to the private relayer because it is public and the gas it contains raises competitor bids. Therefore they are incentivized to harm the mempool if at all possible.

Once dominant, the relayer may start censoring low value mempool transactions, or at least delaying them. This happens naturally anyway as the relayer has a larger choice of transactions for their block proposals and blockspace is limited. But they may also do it deliberately to punish users for not sending transactions through them. Even a one block delay is -ev for DEX transactions, for example. More cheaply they can put mempool transactions at the end of the block.

If the relayer sees a transaction in the mempool that was also sent to them privately, they treat it as a mempool transaction, and may similarly penalize the user for allowing other searchers to include it in their proposals.

As you suggested, users may try to grief the relayer by raising the tip of their mempool transactions. This backfires as the relayer then includes those that overpay in their blocks, for which they win the gas. They then use this to advertise how much cheaper their services are than the mempool which serves to further reinforce their dominance.

It’s a game of balancing the cost of censoring/delaying low value transactions with the extra profit from users overpaying for mempool inclusion or using their relayer instead. They will only do this if it is cost effective in furthering their dominance or profits, but if it is possible to do, the dominant relayer will do it.

They may be able to use this mechanism to increase their profits by raising gas fees overall.

---

**vbuterin** (2021-10-19):

One thing that I don’t understand about these private transaction flow models is: what’s the incentive for any *user* to agree to that? When I am sending any regular transaction, I would prefer it to be broadcasted as fast as possible, to maximize the chance that it will be included in the next block. If builders become more greedy and stop broadcasting to each other, then my own incentive to broadcast to all the builders increases even further: if there are 4 builders, each with a 25% chance of taking each block, then if I broadcast to one builder I will get included in ~48 seconds, but if I broadcast to all I will get included in ~12 (actually if you analyze it fully, it’s 42 vs 6 seconds).

If I am sending an MEV-vulnerable transaction (eg. a Uniswap buy order, or a liquidation), then of course my incentives are different. But even then, I would want to send that tx to all searchers who support some SGX or other trusted hardware based solutions.

---

**pmcgoohan** (2021-10-19):

A handful of private relayers cooperating by sharing transactions is indistinguishable from a single private relayer. Their collective incentive to profit from users is the same. In fact, it’s a sound strategy to maintain dominance.

Any individual or collective group of relayers not willing to run a censorship market will fail because they are leaving private MEV on the table for other relayers to extract.

It seems to me that the endgame here is either a single or a group of colluding relayers willing to run maximally exploitative strategies such as a censorship market (I expect there are others I haven’t thought of).

But let’s say that they don’t collude in this way initially. It’s easy to penalize transactions seen in the mempool as I have already described. Penalizing users that submit to multiple private relayers is harder but not impossible.

I could mark any account sending a transaction that appears in the chain that did not pass through my relayer or the mempool. Future transactions sent from this account (and possibly accounts clearly linked to it) will be similarly penalized for a period of say 2 weeks in my blocks (loyal customers get priority).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I would want to send that tx to all searchers who support some SGX or other trusted hardware based solutions

If we have workable encryption solutions like SGX/VDFs etc then we should be using this to encrypt the mempool and address the problem at root.

I never understood the Flashbots SGX proposal on this. It’s impossible to combine encrypted bundles into a block and guarantee that there won’t be duplicate transactions, but trivial to combine individual encrypted transactions. The latter actually solves most MEV.

---

**vbuterin** (2021-10-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> If we have workable encryption solutions like SGX/VDFs etc then we should be using this to encrypt the mempool and address the problem at root.

That would require trusting SGX at protocol layer, which I think most people consider an unacceptable incursion of a single point of failure. But having SGX in one of many mempools that compete with each other through the builder/proposer mechanism doesn’t have that risk, because if SGX breaks the mempool can switch to something else without touching consensus.

---

**pmcgoohan** (2021-10-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> having SGX in one of many mempools that compete with each other through the builder/proposer mechanism doesn’t have that risk

So say we have 3 SGX relays (SGX), 3 mostly well behaved lit relays (Lit) and 3 bad censorship market relayers (Censors).

Let’s assume they know they must collude to survive, but that they can only collude where their objectives are similar. The SGX guys are not going to share their private transactions with the Censors, for example. So from now on when I talk about SGX, Lit or Censors, I’m talking about groups of similar relayers.

#### Fragmentation

Straight away we have a dilemma. If there are lots of relayers, users will frequently fail to get their transactions included. If there is only one relayer, we have a centralization risk.

Even if there is a least bad number of relayers, there is no reason to think we’ll converge on it.

#### MEV is Pervasive

The next problem is that as long as MEV is permitted in the network, you can’t escape it.

If you use the SGX, you still have to pay them enough to let them win the block off the Censor who is profiting from exploiting users for public and private MEV.

It’s a fundamental problem with MEV protection markets. You must still outbid the MEV in the system.

#### Being Bad Pays

But it’s worse than that because the Censors can outbid their competitors precisely because they extract more from their users (or expect to be able to in the future).

They can offer loss-leaders to gain market share knowing that down the line they’ll make it back and more. The SGX relayers can’t run a censorship market so cannot invest as much in buying market share.

It’s a bit like the ice-cream example above where the seller knows they can only protect their transaction if they make the user overpay.

I suppose what I’m trying to demonstrate is that we can’t expect markets to fix issues caused by centralization.

---

**kelvin** (2021-10-19):

I’ve stated my position in favor of MEV auctions in my [previous article](https://ethresear.ch/t/high-frequency-trading-and-the-mev-auction-debate/10004), but I think [@pmcgoohan](/u/pmcgoohan) has some very interesting arguments here that we should not dismiss.

First of all, I think we can all agree with [@vbuterin](/u/vbuterin) that censorship is very expensive and not of much concern regarding transactions that are time-insensitive and can easily wait for several blocks. The users only have to pay once what the censor has to pay again and again every block, so the censor clearly loses.

Second, and that is going to be a lot more controversial, I think badly designed protocols are the ones to blame for most MEV. Just as you should not write an application that expects UDP datagrams to be received in order, a dapp should not rely on transaction ordering within blocks, and should not even rely on transactions never being censored for a *few* blocks. The only guarantee that blockchains provide in general is that transactions will *eventually* be included. So in my opinion almost no time-critical economic activity should happen on the blockchain settlement layer itself. Time-critical activities should be executed elsewhere (rollups, off-chain exchange relayers, etc) and then *settled* later with no time pressure at all. So I don’t see any need to protect badly designed protocols or their users from MEV; protocols should just do better and users should just go elsewhere.

However, if users *do* care about having their transactions being included very quickly (e.g. in the next block) for any reason, then it is not clear to me that a dominant centralized relayer for fast transactions will not emerge. This relayer will at most be able to delay transactions for a few blocks, but it seems possible to me for such a relayer may be able to obtain a near-monopoly on fast transactions.

I can imagine the following equilibrium.

1. A single relayer builds a high proportion of blocks
2. Out of the users who want their transactions to be included very quickly, a high percentage sends them to the private relayer only (and not to the mempool).
3. If the relayer detects that someone wanted their transaction to be included quickly, but that it sent the transaction to the mempool instead, it loses some money to delay this transaction for a couple blocks.

*I think we should not discuss whether such an equilibrium is likely to arise. Rather, we should discuss whether this equilibrium would be stable.*

Unfortunately, I think it may be stable indeed. Because of the credible commitment of the relayer to behave as in (3), it is in the rational interest of users to send txs to the private relayer only in (2). Second, because of (2), the relayer has access to more transactions than others and so is able to propose the majority of blocks as in (1). Because it may auction off mempool MEV opportunities to sub-searchers, it may not even be the best searcher itself. Finally extra profits coming from (1) may allow it to maintain the behavior described in (3).

Maybe I am missing something and this is not actually profitable, but I feel I could come up with an explicit economic model in which this equilibrium can be proved to be stable.

To make it clear, I don’t think this scenario would be catastrophic for the network. The monopolist would be able to extract some rents, but no long-term censorship can happen. Moreover, a solution could be proposed in the future and implemented as a hard fork. But it may well be worth thinking about it now.

---

**pmcgoohan** (2021-10-20):

Thank you for contributing [@kelvin](/u/kelvin).

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> I think we should not discuss whether such an equilibrium is likely to arise. Rather, we should discuss whether this equilibrium would be stable…Unfortunately, I think it may be stable indeed

Thank you for confirming that a direct relayer censorship attack is probably sustainable- I like the way you framed it in terms of being a stable equilibrium.

Have you considered the economics of the [censorship market](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980/5) in a similar way?

Let me illustrate how this could work in the OpenSea NFT market:

- Bob has bid $10k on an NFT on OpenSea.
- Alice is prepared to pay up to its true value of $50k, but leaves her bid to the last 10 mins (this is rational as the protocol extends the auction by 10 mins for each new bid).
- Bob can now:

(a) outbid Alice for a loss of $40k from his current position (let’s assume he knows the NFTs true value is $50k)
- (b) aim to block her bid on the censorship market for 10 mins (50 blocks)

Bob will breakeven on (b) even if he ends up having to pay $800 per block (and as we all know, NFTs can go for a lot more than $50k and if Alice left it to the last minute Bob could afford even $8000 per block to censor)
Let’s say Bob ends up paying $200 per block to censor Alice

The results are:

- Bob (acting badly) is rewarded with a $30000 saving on the NFT
- The censorship market (acting badly) is rewarded with $10000
- Alice (acting well) loses out on ownership of the NFT she should have rightly won
- The artist (acting well) is punished with a -$40k loss

It’s worse than this though. The censorship market is incentivized to help Bob, because Bob is making money for them and is a proven user of their services. At a certain point, it will become +ev for them to help subsidize Bob’s censorship. As well as being true in any individual case, the more effective they can make their censorship market, the more people will use it long term.

To help them with this, the censorship market allows bids on n block censorship (in this case 50), or even using a specialist OpenSea censorship order. This reveals the censoring users intentions which they can use to calculate at what point it is worth subsidizing them.

One very cheap (for them) thing they could do is simply ban Alice from protecting herself after a few minutes. This would pressure Alice to raise a protecting bid early on. It may make the outcomes more predictable for the customers of the censorship market, while also getting them to pay more upfront and earlier on.

It’s very complex to model, and there are clearly a lot of actions Alice, Bob, the relay and other users can take that I haven’t included.

The crucial observation here is that the incentives of bad acting users are aligned with the then most powerful actor in Ethereum, the dominant private relay and their censorship market. My intuition is that this alignment of bad incentives makes censorship market attacks like this sustainable.

---

**MicahZoltu** (2021-10-21):

I think your argument that short term censorship is possible is reasonable/accurate.  I recommend finding a better example than the one you did because Alice should just bid sooner, knowing that short-term censorship is possible.

What it comes down to is that short-term censorship *is* possible on Ethereum, but you have to continually pay to maintain that censorship.  Any situation where you need to censor indefinitely will cost you infinite money.  Protocols should strive to be designed such that the cost to censor for long enough to cause damage outweighs the benefit to censorship.

As an example, the protocol designers of the NFT auction should not have a fixed 10 minute extension.  They should instead have the extension duration be a function of current gas price and the value of the asset being bought.  This can incentivize Alice to buy sooner (though she could simply choose to buy sooner on her own) and if Alice follows the “buy sooner” strategy we can be sure that the cost to censor by Bob is higher than Bob stands to benefit.

---

**pmcgoohan** (2021-10-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> What it comes down to is that short-term censorship is possible on Ethereum

It’s more than this though. The point I am making is that PBS/MEVA incentivizes:

1. the monopolization of all transaction/order flow on Ethereum by a single actor
2. that actor must (and can) extort maximum value from users by predatory means like censorship markets to maintain their dominance

Tony Soprano runs Ethereum at this point.

It seems to me that this is just the kind of centralized power we want to be mitigating with decentralized technology. In fact, this is one of the objectives of the PBS proposal as I understand it.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I think your argument that short term censorship is possible is reasonable/accurate. I recommend finding a better example than the one you did because Alice should just bid sooner, knowing that short-term censorship is possible.

I think the example works ok in demonstrating that the auction market is broken. Alice shouldn’t have to reveal her maximum bid early out of fear of being censored later. There will be as many other examples as there are Ethereum use cases because this stuff is baked in. Genuine app level mitigations will always have terrible UX to keep out of range of the censors.

---

**LightForTheForest** (2021-10-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> the monopolization of all transaction/order flow on Ethereum by a single actor
> that actor must (and can) extort maximum value from users by predatory means like censorship markets to maintain their dominance

I have to agree here. That already happens. I will not name any actors, since in my opinion that is very bad for Ethereum and may only push them further. If transaction order get monopolized, Ethereum will become a rigged system.

---

**vbuterin** (2021-11-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> If there are lots of relayers, users will frequently fail to get their transactions included. If there is only one relayer, we have a centralization risk.

Why must this be the case? Users should be broadcasting their transactions as widely as possible (UNLESS they’re MEV-vulnerable transactions like Uniswap buys), so their transactions should reach all relayers, no?

---

**pmcgoohan** (2021-11-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Why must this be the case? Users should be broadcasting their transactions as widely as possible

Users can send their transactions to as many relayers as they like, but the ones that will actually win blocks and include them will be using the most predatory practices possible (such as censorship-as-a-service) because blocks are worth more to them.

Definitionally, an SGX relayer can’t frontrun, nor can it offer a censorship market, so it will be outbid.

For example:

- a user sends a tx to both the SGX and the censoring relayer with a 0.01 Eth bribe
- The censoring relayer accepts a bid to censor the transaction for 0.02 Eth
- The censoring relayer then wins the block because it is worth 0.01 Eth more to them to make sure the tx is not included
- Not only that, they also get the gas of another transaction in place of the one they were paid to censor, so their profit margin is greater again. They get paid twice for censoring.

#### Lit vs Dark Censorship Market

Thinking about it, in a lit censorship market the best way for the user to get their tx included is to pay a total of 0.03 Eth to the censor for protection *and* to offer the same to the SGX to increase their chances of inclusion and harm the censoring relayer.

For this reason I think the censorship market will end up being dark so that users can’t see how much they are being censored for or even whether they are.

This means no lucrative bidding war for the relayer, but if the censorship information remains private then users don’t know to bribe other relayers to include their censored transactions. It also encourages users to pay for protection they don’t need and it makes censorship more effective which is good for the censoring relay.

By doing this the censoring relay can only ever make the same or more money than a well behaved relay for any given transaction and bribe amount, and so can maintain dominance.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> (UNLESS they’re MEV-vulnerable transactions like Uniswap buys)

Censorship markets make nearly all transactions MEV-vulnerable.


*(6 more replies not shown)*

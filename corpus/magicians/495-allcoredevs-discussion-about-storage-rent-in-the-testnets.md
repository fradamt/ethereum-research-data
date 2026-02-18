---
source: magicians
topic_id: 495
title: AllCoreDevs discussion about storage rent in the testnets
author: jpitts
date: "2018-06-01"
category: Magicians > Primordial Soup
tags: [storage-rent]
url: https://ethereum-magicians.org/t/allcoredevs-discussion-about-storage-rent-in-the-testnets/495
views: 1671
likes: 2
posts_count: 3
---

# AllCoreDevs discussion about storage rent in the testnets

This topic was requested by GitHub:karalabe and discussed at AllCoreDevs #39.



      [github.com/ethereum/pm](https://github.com/ethereum/pm/issues/43#issuecomment-390959920)












####



        opened 01:43AM - 22 May 18 UTC



          closed 04:21PM - 01 Jun 18 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/8/8f4b5d0cb6b68fa9de7b0a666b2649f68032839f.jpeg)
          Souptacular](https://github.com/Souptacular)





          ACD


          Execution







# Ethereum Core Devs Meeting 39 Agenda
### Meeting Date/Time: Friday 06/01/18 a[…]()t [14:00 UTC](https://savvytime.com/converter/gmt-to-germany-berlin-united-kingdom-london-ny-new-york-city-ca-san-francisco-china-shanghai-japan-tokyo/2pm)
### Meeting Duration 1.5 hours
### [YouTube Live Stream Link](https://www.youtube.com/watch?v=7FNRWEQ_H7w)
### [Livepeer Live Stream Link](http://crypto.livepeer.tv/)

# Agenda

1. Testing & [EIP 1085](https://github.com/ethereum/EIPs/issues/1085): Common genesis.json format scheme across all client implementations
2. Client Updates
3. Research Updates
4. [EIP 1087](https://eips.ethereum.org/EIPS/eip-1087): Net gas metering for SSTORE operations
5. Concerns that using native browser VMs for running eWasm is not DoS hardened. See [this comment](https://github.com/ethereum/pm/issues/40#issuecomment-390006104
) and [this comment](https://github.com/ethereum/pm/issues/40#issuecomment-390114286).
6. Constantinople hard fork timing and what to include (continuing conversation from last call).
7. Testnet rent. See [this comment](https://github.com/ethereum/pm/issues/43#issuecomment-390959920).

Please provide comments to add or correct agenda topics.












Video from the AllCoreDevs #39: https://www.youtube.com/watch?v=7FNRWEQ_H7w

A followup discussion is in the ethereum/AllCoreDevs gitter channel.

> Martin Holst Swende @holiman 08:27
> So.. Re rent, did I understand correctly that the idea would be to simply delete all storage for contract X, but keep the storage root hash… And then, whenever a user wants to interact with X, he would have to provide the storage slot dataa he wants to interact with, plus merkle-proofs. Like a mini-version of a ‘full’ stateless client
> ?
>
>
> …
>
>
> Nick Savers @nicksavers 08:44
> Re:Rent - How about keeping track of the last blocknumber in which an account was touched and deletes it (burning all remaining ETH) when somebody touches an account where a rent-deadline has passed? Topping up would just burn the rent. If an account was not touched before it was topped up, it would continue to exist. All accounts would initially start out with the blocknumber at the time that the rent rules start.
>
>
> Nick Johnson @Arachnid 10:37
> @nicksavers What’s the incentive to touch an account that’s run out of rent?
> And where does the rent payment come from?
>
>
> Nick Savers @nicksavers 10:44
> The incentive is to clean up the state. If nobody does it, apparently nobody cares. Then again, it would require gas cost to touch too otherwise there is a DoS attack vector.
> Rent comes from the account balance.
>
>
> winsvega @winsvega 10:45
> solutions could be.
>
>
> charge a contract for the storage. each n blocks. if contract has no balance to pay for the storage then its removed as obsolite.
> implement swarm
>
>
> Nick Johnson @Arachnid 10:50
> @nicksavers Right, it’s a tragedy of the commons issue - cleaning state costs funds but doesn’t reward you.
> If rent comes from the account balance, it will mess up lots of existing contracts.
> @winsvega How would implementing swarm help?
>
>
> Nick Savers @nicksavers 10:52
> I doubt that it will be an issue. Not sure how much it will cost to touch all accounts in the state, but weren’t the empty accounts also removed in 2016 by people donating gas? The miners could do it themselves against 0 gas cost if they want.
>
>
> winsvega @winsvega 10:52
> with swarm we could make a swarm eth node which would call into the swarm for the data base
>
>
> Nick Savers @nicksavers 10:52
> Yeah if Swarm incentives work as advertised then you wouldn’t need rent.
>
>
> Philip Daian @pdaian 11:08
> to be sustainable swarm incentives need a rent model too. it’s just pushing the problem to another layer (like stateless clients)
> (sorry I joined late just figured Id throw in my .02 since was pinged)
> also I think there are great use cases for paying only very short term rent (eg in a scalable system instead of using state channels to cleanup irrelevant/old data)
>
>
> Eth-Gitter-Bridge @Eth-Gitter-Bridge 11:19
> [alexandrevandesande] Re: rent. I like the idea of deleting/archiving but what are the mechanisms to define what is the rent price? Who are the two sides of the market? Do you have an EIP?
> [alexandrevandesande] Edited previous message: Re: rent. I like the idea of deleting/archiving but what are the mechanisms to define what is the rent price for a 5 year storage? Who are the two sides of the market? Do you have an EIP?
>
>
> Philip Daian @pdaian 11:24
> yeah, this requires some discussion… I don’t think anyone can answer that question for the community. the system can target a max state space growth, that might be one initially safe approach. I know vitalik has thought about this somewhat but I don’t have a concrete proposal yet. I was hoping to discuss at ic3 and perhaps before.
>
>
> Nick Johnson @Arachnid 11:24
> @winsvega We can’t farm out state storage to a third party like swarm without hugely increasing the cost of an sstore/sload or hugely decreasing the gas limit.
>
>
> Philip Daian @pdaian 11:25
> I’m happy to take ownership on an EIP but not satisfied w the details yet… in general I think it would be nice to a) establish the expectation of paying for time-value of storage b) come up with a general “recurring payments” type of pricing model for resources (compatible with being paid for by self sustaining contracts) that can be soft-tweaked later c) get some of the old crap that objectively nobody needs and is there for no reason at all cleaned out
>
>
> Nick Johnson @Arachnid 11:26
> The problem is that there’s not really any viable way to retrofit it for existing contracts without breaking a lot of them.
>
>
> Philip Daian @pdaian 11:26
> I think probably separate EIPs need to happen too for the economic model, the technical details of resurrection, etc.
> I think retrofitting is actually possible. my general intuition is that a good retrofit would be a change to the economic model not the programming model
>
>
> Nick Johnson @Arachnid 11:27
> But how would you prevent important contracts that were written without rent in mind from being garbage collected?
>
>
> Philip Daian @pdaian 11:27
> what I mean is that all old storage will be grandfathered in but pay as much as new storage, e.g. as if you were resurrecting each time (or even more). so there’s no economic incentive to hoard
> accept current junk and bound future growth is one option, and nodes can soft prune it later or something if it really never gets touched
>
>
> Nick Johnson @Arachnid 11:28
> yup to the former, though for the latter if nodes did, then someone would conduct a DoS attack that touches that storage.
>
>
> Philip Daian @pdaian 11:28
> basically all users of old contracts see is storage maybe becoming more expensive (not even clear based on how the market prices will look) but no change to their mental design model
> and yeah that’s a fair point, especially if it’s a consistent strategy. maybe some probabilistic solutions to that could work but I’m not sure.
>
>
> Nick Johnson @Arachnid 11:28
> Not sure I follow. Why would it get more expensive, and how would that equate to rent?
>
>
> Philip Daian @pdaian 11:29
> so in the soft transition you still somewhat rely on commons to archive storage
> basically saying that everything is incentive compatible if you pay rent and design your contract to pay rent
> otherwise EF and archive.org or whatever can host servers that you can pay to ressurect your data (or even that could provide it free)
>
>
> Nick Johnson @Arachnid 11:29
> I really don’t understand what you’re suggesting. How would my existing contract that has a map in it and doesn’t know about rent work, post-transition?
>
>
> Philip Daian @pdaian 11:30
> the same as it does today, sload and sstore will just cost different amounts
> and will cost more than sstore and sload for new contracts that pay proper rent
>
>
> Nick Johnson @Arachnid 11:30
> Different how?
> Then wouldn’t someone deploy a generic map contract that lets any new contract use old-style indefinite storage costs?
>
>
> Philip Daian @pdaian 11:30
> one simple possibility is take how much rent they would have paid in the new model and 3x it every time
> you economically disincentivize landlording of that kind
>
>
> Nick Johnson @Arachnid 11:31
> How do you determine how much rent they would have paid? You don’t know how long they’ll be storing the data for.
>
>
> Eth-Gitter-Bridge @Eth-Gitter-Bridge 11:31
> [alexandrevandesande] Phil’s approach allows us to treat the blockchain like RAM for quick access for common contracts, while the less common contracts can still be accessed, but they take some time to be taken out of the main state, like reading from disk used to be. But I think it’s important to understand who are the market forces: I suppose the user is the side who wants to pay the least possible for the rent, but who is the side charging as much as they can?
>
>
> Philip Daian @pdaian 11:31
> you’re essentially saying old contracts get a slightly different class of “soft rent” storage where they pay as if they are renting but never get pruned from memory
> well if they come back and access it after a long time they will have to top all the rent off that they should have been paying
>
>
> Nick Johnson @Arachnid 11:31
> @pdaian Okay, so old contracts do have to deal with rent? How?
>
>
> Philip Daian @pdaian 11:32
> if you use a tx you pay rent on the storage spaces it touches
> top it all off to today
>
>
> Nick Johnson @Arachnid 11:32
> I see. Even for reads?
>
>
> Philip Daian @pdaian 11:32
> if it’s a totalsupply contract that everyone touches 3x a day that’ll be freeish. if it’s your balance that you haven’t touched in 3 years it will cost more
> and yeah even for reads
> because reads == nodes have to store
> basically the idea is that we promised people their storage will be permanent, not that it will always be cheap to access. none of the mental guarantees of smart contracts have changed, it’s just as if gas increased in price or similar
> which was always a known possibility (some would say inevitability) of the system
>
>
> Nick Johnson @Arachnid 11:34
> Right. Yes, that would disincentivise the ‘storage contract’ trying to avoid the new rules, and probably wouldn’t break much since most contracts don’t make assumptions about how much gas operations cost.
>
>
> Philip Daian @pdaian 11:34
> yeah exactly
> if you make assumptions about how much gas costs you have to prepare to be broken by a future hf anyway
> either that or you’re not doing your homework
>
>
> Nick Johnson @Arachnid 11:34
> Though it could get prohibitively expensive to access old data. What if a particular TX gets inflated past the block limit due to rent?
>
>
> Philip Daian @pdaian 11:35
> that’s a good question, not sure… depends a lot on the specifics of how rent is paid. I suppose e.g. one tx per block could be allowed to do this (since in theory it costs nodes nothing)… a simple max wouldn’t work because then you’d just be incentivized to wait / pay less often
> could potentially behave like a throw but still pay that portion of the rent
> and you just keep redoing it?
>
>
> Nick Johnson @Arachnid 11:36
> Not a bad idea. You could also potentially rule that ‘rent gas’ doesn’t count towards the block gas limit.
>
>
> Philip Daian @pdaian 11:36
> also really depends how much people actually want to use storage (aka how expensive will this all be)
> yeah that also
>
>
> Nick Johnson @Arachnid 11:37
> Now you just have to figure out how rent price should be determined.
>
>
> Philip Daian @pdaian 11:37
> I think even a clean slate model is worth considering for sharding
> I like the backwards compatible models too but for sharding that’s not necessarily needed afaics
>
>
> Nick Johnson @Arachnid 11:37
> Yup
>
>
> Philip Daian @pdaian 11:37
> and yes the pricing is a question I think the community will really need to discuss, I can throw together a few example EIPs but I don’t know it’s ultimately a political problem
> I think if you can convince people that it will be invisible though they won’t mind, so that is kind of my goal
> or mostly invisible at least, other than “think about it when writing contract” like all the other gas issues etc
>
>
> Nick Johnson @Arachnid 11:39
> Well, I don’t mean pricing as in “it should be x gwei per slot per day”, I mean what mechanism you use to determine price.
> If we ever get a clean slate, there are so many things I want to change. One of the big ones is how storage is organised.
>
>
> Fredrik Harrysson @folsen 11:42
> the original context of this was brought up as a measure to prevent spam on testnets, but i think that’s useful to experiment with this, and in the testnet model you don’t necessarily need to parties to the market, just burn one side
>
>
> Philip Daian @pdaian 11:42
> I think it’s a big enough space that what I think is optimal != what anyone here or the community probably would feel is optimal and some debate would be required
>
>
> Nick Johnson @Arachnid 11:42
> Based on my experience with ENS, it needs to be simple and straightforward. An auction is likely a bad idea.
>
>
> Philip Daian @pdaian 11:42
> yeah I think the network should be the market > 2 parties
> yeah fair enough. the simplest way is a global price that just gets difficulty-like adjustments to target some growth rate. then the only q is how quickly to adjust and what the exact parameters are and what the growth rate should be both pre and post sharding (engineering question likely for you guys)
> and also how to ensure that it can’t be easily manipulated etc.
> oh also a rebrand to something other than rent would probably help
>
>
> Nick Johnson @Arachnid 11:45
> Growth rate is easy to target, but not ideal, in my mind. It puts an intrinsic limit on growth that may not reflect reality (in either direction).
>
>
> Philip Daian @pdaian 11:46
> idk I think it’s an open question even for something like block space. from an incentive compatibility PoV having miners vote on it is not great, practically it works. in my mind the mechanisms there should be similar for simplicity since they’re both deciding some network-style commons parameters
> so maybe miner vote within some bound?
>
>
> Nick Johnson @Arachnid 11:46
> Miner voting might work; they have similar incentives to the gas limit voting.
>
>
> Philip Daian @pdaian 11:46
> I’m also not sure what the long term evolutionary plans are for something like block gas limit. is it forever to be miner voted, how will it work in sharding, etc.
> yeah theoretically miner incentives aren’t any different from this than block gas limit since they need state to validate fees
> but also in neither case do they pay for replication so from a broader costs perspective still not fully aligned IMO (and no known solution in site)
>
>
> Eth-Gitter-Bridge @Eth-Gitter-Bridge 11:50
> [alexandrevandesande] I would also question some of the constants, like: why “prepaid for 5 years”? Sounds like that can in turn become a commons problem. Ethereum could have more active contracts used yearly than it has in its history, so the size of 5 year storage itself could be huge and we’d have the same issue, since the miner receiving the rent is not necessarily one storing it. On the other hand, if the process of retrieving something from storage becomes quick and painless, then maybe a lot of contracts could benefit from being in “cold storage” for most of its active existence, being retrieved and then put back down
>
>
> Philip Daian @pdaian 11:52
> yeah the 5 years is just one grandfathering proposal, could even be something like 20 or whatever. basically “if you haven’t paid for it now you’ve left the system for long enough that no matter what would have happened you’d be relying on commons for this storage, so archive.org and some other nonprofits will store it for you now instead”
> I personally like the soft change to the economic model I described more, which doesn’t require those constants (but could potentially be very expensive for users that are relying on grandfathered stuff; then again this could also be a migration incentive?)
>
>
> Eth-Gitter-Bridge @Eth-Gitter-Bridge 11:53
> [alexandrevandesande] I would say that what matters is not that a contract will exist for X amount of years, but how much time does it take for retrieving it from storage. Some contracts might need to be always responsive, but for some use cases, maybe I don’t care about waiting a few hours/minutes until someone finds my contract
> [alexandrevandesande] In that sense, it’s similar to gas price market (not that that one is perfect) in the sense that you’re paying for speed
>
>
> Philip Daian @pdaian 11:54
> yeah, in a new contract you’d have to think about who stores it… either pay the rent to the network and they store it, store it yourself wherever if that satisfies the parties and resurrect it later, or rely on some commons nonprofit and roll the dice (but don’t tax the network in the meanwhile)
> for old contracts I’d think unless some weird breakdown happens that access should be relatively quick
> if EF eg runs a state query service for the current state at upgrade time, that’s not a ridiculous amount of data
> and for new contracts that could be a business
> so it will maybe cost more than just paying rent but if you really screw up and can’t find your data maybe it’s worth it to you
>
>
> …
>
>
> Nick Savers @nicksavers 13:15
> Perhaps the Merkle proof idea about rent could also work combined with deleting the entire account from the state. The user providing the proof would need to provide the last block number that it was available along with the Merkle proof.
>
>
> William Entriken @fulldecent 14:49
> WILL"S SIMPLE RENT PROPOSAL: add two new variables for each account:
> S_words – the number of non-zero storage words in the account
> S_archive – when the account should be archived
> And add one variable to the yellow paper:
> G_rent_per_word_block
> During any writable transaction we also set S_archive = BLOCK_NUM + S_value / (S_words * G_rent_per_word_block). It is now also specified that any operation on an account where BLOCK_NUM > S_archive will fail. If a dead account receives funds via a SELFDESTRUCT then the S_archive will not be updated.
> Implementation note: a client may wish to implement this by removing state after S_archive since it has no effect.
>
>
> Nick Johnson @Arachnid 14:50
> You cannot rely on the account’s existing balance for rent payments. That will screw up so many existing contracts.
>
>
> William Entriken @fulldecent 14:51
> Sure you can. Set an epoch to sunset all existing accounts. IF S_archive = 0 THEN S_archive = EPOCH
>
>
> Nick Johnson @Arachnid 14:52
> That’s not what I’m talking about. I’m talking about the fact that many existing contracts make assumptions about their balances and how they can change.
>
>
> Nick Savers @nicksavers 14:52
> Ah some can’t even have their balance updated. Non payable functions. That makes it harder.
>
>
> Nick Johnson @Arachnid 14:53
> Indeed. Others are custodians for users’ funds. Take an ERC20 wrapper, for instance.
>
>
> Nick Savers @nicksavers 14:53
> Although with some work around it’s possible.
>
>
> Nick Johnson @Arachnid 14:53
> If you start deducting rent, some unfortunate person will no longer be able to get their ether back.
>
>
> Nick Savers @nicksavers 14:54
> Unless extra ether is added to the contract…
>
>
> William Entriken @fulldecent 14:54
> Right.
>
>
> Nick Johnson @Arachnid 14:54
> Where’s that come from? That just means some other person is the unfortunate one.
>
>
> Nick Savers @nicksavers 14:55
> But yeah it will be difficult to pre calculate that
>
>
> William Entriken @fulldecent 14:55
> At some point somebody should pay to keep the contracts online.
> After the epoch
>
>
> Nick Johnson @Arachnid 14:55
> I’m not objecting to that; I’m saying that you can’t deduct it from the contract’s balance without breaking a whole bunch of stuff.
>
>
> William Entriken @fulldecent 14:56
> It will break stuff, but if the epoch is far enough away and nobody cares to pay money to the contract then it shouldn’t matter.
>
>
> Nick Johnson @Arachnid 14:56
> It might not even be possible to pay money to the contract. And even if it is, you’re breaking guarantees that the authors of the contract relied on - that the balance can never decrease except through action of the code.
> (Not to mention, significantly complicating keeping track of ‘user balance’ vs ‘rent balance’ for all future contracts)
>
>
> William Entriken @fulldecent 14:57
> The other fundamental options are to keep the existing 1TB forever or to have a Ethereum 2.0 starting at ground zero.
> All good ideas to explore.
>
>
> Nick Johnson @Arachnid 14:58
> There’s a thousand other options. One easy one is to have a separate rent balance.
>
>
> William Entriken @fulldecent 14:59
> That’s cool too.

## Replies

**fubuloubu** (2018-06-01):

Neat thing is if we perfect this in testnets, then it helps testnets reduce bloats and serves as a PoC for mainnet and how that would work.

If it were parameterized, maybe testnet is set for 6 months, and mainnet is set for like 6 years (since people pay real money for this storage)

---

**fulldecent** (2024-12-21):

Adding notes about this proposal since the meeting:

- EIP-1418 deducts rent from a RENT account, not from the balance account, it does not break contract guarantees.
- When a contract is evicted (RENT is below zero), the contract still works. But every transaction touching it just needs to provide a code witness, storage witness and pay extra fees.

---

Another possible proposal is that each trie value has an eviction date. When you make a transaction each read/write gets eviction date set to NOW +2 years. And then as before if you make a transaction that reads stale values then you need to provide a witness and maybe pay an extra cold read fee, and that makes the value hot.


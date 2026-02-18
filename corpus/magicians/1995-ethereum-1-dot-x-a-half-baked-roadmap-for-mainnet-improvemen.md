---
source: magicians
topic_id: 1995
title: "Ethereum 1 dot X: a half-baked roadmap for mainnet improvements"
author: cdetrio
date: "2018-11-24"
category: Working Groups > Ethereum 1.x Ring
tags: [eth1x, ethereum-roadmap]
url: https://ethereum-magicians.org/t/ethereum-1-dot-x-a-half-baked-roadmap-for-mainnet-improvements/1995
views: 13184
likes: 48
posts_count: 24
---

# Ethereum 1 dot X: a half-baked roadmap for mainnet improvements

## Ethereum 1 dot X: a half-baked roadmap for mainnet improvements

I’m posting this without any prior review or draft feedback from other core devs. This is my personal perspective on what 1.x is about. All mistakes and misrepresentations are my fault.

### Summary

Ethereum 1.x is a codename for a comprehensive set of upgrades to the Ethereum mainnet intended for near-term adoption. The 1.x set of improvements will introduce major, breaking changes to the mainnet, while 2.0 (aka Serenity) undergoes prototyping and development in parallel. The plan for 1.x encompasses three primary goals: (1) mainnet scalability boost by increasing the tx/s throughput, achieved with client optimizations that will enable raising the block gas limit substantially; (2) ensure that operating a full node will be sustainable by reducing and capping the disk space requirements with “storage rent”; (3) improved developer experience with VM upgrades including EVM 1.5 and Ewasm.

### Introduction

The “Ethereum 1.x” idea was born out of discussions among core devs during Devcon4. Previous to discussions about 1.x, the roadmap for Ethereum 1.0 was minimal with relatively conservative changes having been proposed for mainnet hard forks (e.g. Byzantium and Constantinople). Before and after Byzantium (October 2017), Casper-FFG was being developed as a drastic mainnet change which would introduce hybrid PoW-PoS block rewards. By June 2018, [Casper-FFG was deprecated](https://medium.com/@djrtwo/casper-%EF%B8%8F-sharding-28a90077f121), and PoS research efforts pivoted to development of a “beacon chain” which would be launched as a new chain separate from the Ethereum 1.0 mainnet. This pivot left 1.0 client developers disoriented. As the longer timeline for 2.0 became apparent, we began to ask, what do we do in the meantime with the mainnet?

One option for 1.0 client maintainers is to coast along with conservative, easy changes to the mainnet, and not to consider any major changes (leaving them as features slated for 2.0). An alternative option is to consider introducing drastic, breaking changes on the 1.0 mainnet, while separate teams focus on 2.0 R&D. This latter option is the 1.x plan.

### Formulating a plan for 1.x

Before announcing the 1.x plan, some core devs wanted time to flesh out detailed proposals, and to gather concrete data to answer pertinent questions (such as, what is the immediate scalability boost we can expect after some easy client optimizations? 2x, 5x, or more?). But the desire for working groups to have an opportunity to coordinate draft EIPs in private before announcing the plan conflicts with the desire to openly discuss changes under consideration at the earliest possible stage with the broader community. So, although it would have been nice for core devs to announce a solid step-by-step plan for 1.x, it would also be nice to formulate a plan with open working groups in an inclusive and transparent process from the beginning.

The downside of an inclusive and transparent process from the beginning is that the initial presentation is only a half-baked plan. Because a half-baked plan cannot answer all the questions, this risks stirring up a confused narrative, with controversy and pushback from other devs and the community. As the 1.x plan will introduce breaking changes on the mainnet, it is expected to be controversial, so there is reluctance to broadcast a half-blaked plan.

The ability of core devs to pursue a 1.x plan on an aggressive timeline is also uncertain. The improvements are both technically and politically ambitious and will take great effort to execute; the motivation to press forward could be sapped by early controversy and resistance. The easier option is to avoid controversy and reserve ambitious ideas for 2.0. Getting drastic changes adopted on the mainnet will be challenging.

The rest of this post will outline the three main goals of the 1.x plan. The first and second (scalability and sustainability) are arguably interrelated, while the third (VM upgrades) is independent.

### 1. Client optimizations for a scalability boost

The first goal is to boost transaction throughput on the mainnet. Transaction throughput is determined by the block gas limit, which is currently around 8 million. Miners vote with each block to either raise or reduce the block gas limit. If the gas limit is raised too high, then the network uncle rate increases as an unintended side effect. A high uncle rate is bad because it results in mining pool centralization (it is mainly small pools that suffer from high uncle rates, leaving them with lower revenues and unable to compete against larger mining pools with lower uncle rates). Thus, miners cannot naively raise the gas limit without sacrificing a diverse set of multiple competing mining pools.

The good news is that a client optimization has been recently discovered which is likely to enable a substantial increase to the block gas limit while maintaining a low uncle rate. The optimization is a fix to the way Parity relays blocks (discovered by [Alexey Akhunov of turbo-geth](https://medium.com/@akhounov/roadmap-for-turbo-geth-31cbfb1e72b7) fame). Currently Parity does full verification of block PoW and transaction processing, before relaying a block. The optimization is to only verify the PoW and then start relaying the block, while processing the transactions. This optimization might greatly reduce network uncle rates and could enable miners to raise the block gas limit substantially (note an alternative idea: rather than raising the block gas limit by 2x, computational opcodes could be repriced to 1/2).

How much can we raise the block gas limit with this optimization? We don’t know yet, and we don’t want to get excited prematurely. Core devs are hoping to study this question with network simulations and more data collection, but the answer depends on complex factors which have been understudied (network topology and propagation delays between full nodes). Aside from this one fix, there are further “low-hanging” optimizations to block relaying that could also be done.

Beyond low-hanging optimizations, more drastic changes for mainnet throughput increases are also being studied. One approach is parallel transaction processing, picking up where an [old EIP](https://github.com/ethereum/EIPs/issues/648) left off. Another approach to achieving a big scalability boost on the mainnet, mentioned long ago in the [Sharding FAQ](https://github.com/ethereum/wiki/wiki/Sharding-FAQs#what-about-approaches-that-do-not-try-to-shard-anything), is a change to the PoW protocol: “Bitcoin-NG’s design can … increase the scalability of transaction capacity by a constant factor of perhaps 5-50x… [the approach] is not mutually exclusive with sharding, and the two can certainly be implemented at the same time.”

So there are easy optimizations that might yield an immediate (totally wild guess, 2x-5x) throughput boost on the mainnet. And with more comprehensive protocol changes, maybe a 50x boost on the mainnet (not my number! its in the sharding FAQ) could be achieved.

But, a 2x-5x boost in throughput would make the current problems with mainnet 2x-5x worse. The biggest problem is growth in disk space, and if we’re going to boost the mainnet throughput then the disk space problem must be solved first.

### 2. Reducing the disk space for a sustainable network

A long-term solution for reducing disk space, i.e. storage rent, is the most controversial part of the 1.x plan. There is much debate and differing opinions on how necessary this is. On one end of the opinion spectrum, some 1.0 client maintainers believe that the state size is already growing too fast, and that even without any boost in throughput, a drastic change needs to be proposed and adopted. These core devs argue that at best, the current Ethereum mainnet can sustain growth for three more years. If some drastic breaking changes are not made before then to reduce the disk space burden, then Ethereum as we know it will not survive.

At the other end of the spectrum are researchers whose efforts are focused on scaling Ethereum by launching 2.0 as soon as possible. They argue that new hard drives can accomodate the current rate of state growth on the 1.0 mainnet, until 2.0 is launched and users migrate from 1.0 contracts to new contracts on 2.0. They also argue that introducing breaking changes on the mainnet would violate the behavioral expectations that users have about contracts deployed on 1.0, and that the 1.0 network would work just fine with a state size of 70 gigs in three years (the [current state size](http://didtheethereumblockchainreach1tbyet.5chdn.co/) is around 7 gigs, last I checked). Furthermore, introducing a rent mechanism on Ethereum 1.0 could be confusing to users, as it will likely be different from the rent mechanism introduced on 2.0.

An alternative to storage rent is [stateless clients](https://ethresear.ch/t/the-stateless-client-concept/172), but for stateless clients to be practical the state trie format would need to be changed to a format optimized for the stateless paradigm (i.e., clients would need to switch from the current hexary trie to a binary or sparse trie). Discussions among core devs lean toward the opinion that switching from stateful to stateless would be a huge change to 1.0 clients and much more complicated to implement. The simpler path, which can be achieved on a more aggressive timeline, is to keep the current stateful hexary patricia trie and add on storage rent.

The good news is that there are some easy, non-controversial changes that can be adopted immediately to reduce required disk space. These changes were proposed by Péter Szilágyi (of go-ethereum fame) as the first two of a three-point plan to reduce disk space (in brief: 1. delete past blocks  2. delete past logs 3. delete state, i.e. storage rent).  Currently a geth node sync’d to the chain downloads [over 100gb](https://etherscan.io/chart2/chaindatasizefast) of data, but most of that data is past blocks and past logs. The actual account state is only a fraction of that total data. To be clear, past blocks and past logs would of course continue to be stored somewhere and be widely available, but they would not be stored by common full nodes which dominate the network. Full nodes would instead only store some recent history of blocks and logs, perhaps several months or so of data.

The two easy changes (delete past blocks and delete past logs) would only break some dapps that expect a full node to index and query all past log events. These dapps would stop working with mere full nodes (instead they would require the user to run a more space-intensive archive style node, or to query a log indexing service). Sync’ing for the majority of users would become fast and painless (like in the early days, when the Ethereum mainnet was young and lightweight). But it would be a temporary fix, and sync’ing would gradually become slow and heavy again, as the account state grows and grows.

The solution to a growing account state is storage rent.

Among potential storage rent proposals, they differ in terms of friendliness to users, and implementation complexity (friendliness to core devs). The simplest implementations are not friendly to users. For instance, it is much simpler to implement a rent mechanism that simply deletes accounts which do not pay rent, and does not offer users any way to un-delete or “resurrect” their accounts. In contrast, a rent mechanism where users can later [resurrect accounts that didn’t pay rent](https://ethresear.ch/t/improving-ux-for-storage-rent/3994) is friendlier to users, but more complex to implement.

Another issue with rent is incentive issues around contracts with multiple users. For instance a token contract has many users who hold tokens, but a simple rent mechanism would require the contract to pay a rent fee. No single user is incentivized to pay rent for the contract, rather each token holder’s incentive is to let some other user pay the contract’s rent fee. Solving this incentive problem would require a major change to the ownership model around contract storage.

The storage rent proposal is the hardest part of the 1.x plan. It is politically controversial, as it will introduce breaking changes to the mainnet with new modes for user and developer experience. And it is technically complex to implement, especially to provide a user-friendly mechanism. The goal is to flesh out a detailed proposal that as many people as possible will be satisfied with (from core developers, to dapp developers, to dapp users).

### 3. Improved developer experience with VM upgrades

The third goal, upgrading the VM, is fairly independent of the first two. One proposal for upgrading the EVM is [EIP 615](https://eips.ethereum.org/EIPS/eip-615). This EIP is also known as “EVM 1.5” because it was proposed as a near-term improvement to the EVM, in between the longer-term move toward [Ewasm](https://github.com/ewasm/design) (aka “EVM 2.0”).

Ewasm was originally designed to be backwards-compatible with the EVM (i.e. so that Ewasm contracts could interoperate with EVM contracts), for adoption on the mainnet. Later, Casper-FFG was deprecated and the PoS roadmap pivoted to [Ethereum 2.0 phases](https://github.com/ethereum/wiki/wiki/Sharding-roadmap), with a beacon chain in Phase 0/1, and an execution engine based on Ewasm was proposed for Phase 2. But as the execution engine on 2.0 would be on a separate chain rather than 1.0 main chain, there is no need for the 2.0 Ewasm to be backwards-compatible with EVM. This means the “Ewasm 2.0” design is an open question, and could differ substantially from “Ewasm 1.0” (i.e. the current Ewasm design which is backwards-compatible with EVM).

The 1.x plan for Ewasm means pursuing the original goal: mainnet adoption of the backwards-compatible Ewasm version alongside EVM. A multi-step roadmap for introducing Ewasm on the mainnet will be detailed in proposals to come.

### Conclusion: No 1.x roadmap yet

The above plan for 1.x is a half-baked outline. At this time, the pertinent questions cannot be answered. Studies need to be performed to gather data on the potential degree of mainnet scalability improvements in the near-term. And the breaking changes required to make operation of full nodes sustainable in the mid and long-term need to be written up and published as detailed proposals for community consideration.

## Replies

**boris** (2018-11-24):

Fantastic! Thanks for posting. [@koeppelmann](/u/koeppelmann)’s tweet storm was also great, but not easy to link to.

There was a piece in the tweetstorm about eWASM as a precompile that made no sense to me, and I don’t see you mentioning.

https://twitter.com/koeppelmann/status/1066009676331053056?s=21

Pretty sure this is wrong and not possible.

Feels like LLVM to make other languages compiled to EVM today and focusing EWASM on Phase 2 might be a more effective path with results sooner.

Have any thoughts on this LLVM approach [@cdetrio](/u/cdetrio)?

I posted a diagram in this other thread:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png)
    [Thread to begin discussing "Ethereum 1.0" proposals](https://ethereum-magicians.org/t/thread-to-begin-discussing-ethereum-1-0-proposals/1768/8) [Ethereum 1.x Ring](/c/working-groups/ethereum-1-x-ring/33)



> Thanks for continuing to curate this, @jpitts. I also wonder where / how one gets involved with working groups. Would be good to list them and have a repo or channel or somewhere where people can knock on the door to find out more and get involved.
> I’ve started on drawing diagrams of the Ethereum system – decomposing the entire Ethereum client and some of its specifications.
> See https://docs.google.com/presentation/d/1UDW1KsNc5w8xaFLWaisn_ZFqWcflZHWs-_FUpDq_2kk/edit#slide=id.p
> Relevant for th…

---

**Brett** (2018-11-24):

Great breakdown - thank you Casey.

---

**AlexeyAkhunov** (2018-11-24):

Great write-up! Thank you for taking time (I am sure it took a lot of time) to do this, Casey

---

**ldct** (2018-11-24):

Nice!

> But, a 2x-5x boost in throughput would make the current problems with mainnet 2x-5x worse. The biggest problem is growth in disk space, and if we’re going to boost the mainnet throughput then the disk space problem must be solved first.

I am not very familiar with the constraints that go into setting the gas price of each opcode, but if the state size growth is the main problem, couldn’t we try to limit the state growth to roughly what it is currently while increasing throughput? i.e.,

1. Raise block gas limit by 2x
2. Increase the cost of SSTORE when a value is set to non-zero from zero to 40,000 gas

---

**sinamahmoodi** (2018-11-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ldct/48/381_2.png) ldct:

> Increase the cost of SSTORE when a value is set to non-zero from zero to 40,000 gas

I was also wondering if setting non-zero values to zero could be not only subsidized but rewarded, as a way to incentivize clearing unused storage. I saw there has been a [proposal](https://github.com/ethereum/EIPs/issues/142) along these lines by [@axic](/u/axic). Has there been more discussion on why this might not be viable?

---

**hershy** (2018-11-24):

[@cdetrio](/u/cdetrio) thank you for that summary. Information like this - even as a ‘personal perspective’ - is invaluable to those with their own forward roadmap/s on projects that are in or around the Ethereum network. One of the most powerful elements of operating with transparency, is that it allows for a community with the ability to prepare for any and all ‘adjustments’ needed to their operations/executions/processes.

I would also like to add that publishing a review like this immediately after the meeting - as well as including the fact that there is/was closed, private working groups assigned to tasks - would have gone a long to allaying many of the transparency concerns that have been raised over the past few days.

---

**gcolvin** (2018-11-24):

A half-baked technical idea on storage.  Can under-used storage be stored in fewer nodes, with a defined way for a node to find the pieces it is missing?  So the less often storage is used the less space it takes and the more expensive it is to load.

---

**virgil** (2018-11-25):

Strongly support us giving the users something to date then in the mean time.  Also don’t want to rush the research team to introduce something before it’s ready.  As for the specific proposals, it’s unclear to me which ones to prioritize.  But strongly support this direction.

---

**stobiewan** (2018-11-25):

How about keeping rent simple and maximally effective at the protocol level and completely deleting anything which runs out of funds. Leave it to user applications like mycrypto or mist manage safety and warn when sending to a deleted account to prevent replayed transactions, a service could exist to provide the accounts. When introducing rent give everything a year long buffer to make easy. It is reasonable to expect rent to be paid on anything which matters and for users not to reuse deleted accounts which have lost their nonce. Protocol shouldn’t be compromised to hold their hand, user apps can do it and eventually users will know anyway.

What’s friendly to users is actually getting it implemented ASAP and the simple method could give that, adding a suspended state and a good way to rehydrate them is very complex, creates room for dangerous bugs around something getting suspended multiple times and resumed at different points, and it’s likely UX will be entirely unfriendly around resuming suspended accounts anyway, I think it would actually almost never be used in reality.

Probability of achieving complex method of rent at a date sufficiently in advance of Serenity that it’s worth doing is very low. It also still leaves state growth to head towards infinity long term as nothing can be entirely deleted where as the simple method will actually work as desired.

---

**vbuterin** (2018-11-25):

> How about keeping rent simple and maximally effective at the protocol level and completely deleting anything which runs out of funds.

I think this is a bad idea. Users forget about some application they are involved in all the time. Even in ENS auctions which lasted a few days, I remember there were people who forgot to reveal their bids. From a usability point of view, a recovery path for an account that gets hibernated, even if an expensive one, is IMO essential.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ldct/48/381_2.png) ldct:

> I am not very familiar with the constraints that go into setting the gas price of each opcode, but if the state size growth is the main problem, couldn’t we try to limit the state growth to roughly what it is currently while increasing throughput? i.e.,
>
>
> Raise block gas limit by 2x
> Increase the cost of SSTORE when a value is set to non-zero from zero to 40,000 gas

I raised this exact possibility in the meeting, and it still seems reasonable to me. The way opcode prices were originally made is using [this spreadsheet](https://docs.google.com/spreadsheets/d/1m89CVujrQe5LAFJ8-YAUCcNK950dUzMQPMJBxRtGCqs/edit#gid=0) that basically just calculated the different costs of processing each opcode (microseconds, history bytes, state bytes…) and assigned a gas cost to each unit of each cost; we can just push up the cost we assign to storage bytes.

It definitely solves the largest first-order problem (storage is not costly enough in an absolute sense) minimally disruptively, and I’m not sure if the other inefficiencies of storage pricing today are bad enough to be worth uprooting the present-day storage model live to fix.

A third possibility that I have not yet seen discussed is to start off by raising the gas limit and increasing the SSTORE cost (possibly greatly increasing it, eg. 4-5x; also NOT increasing refunds to mitigate gastoken), and then start architecting a precompile that manages a cheaper class of temporary storage that follows some rent scheme.

---

**ldct** (2018-11-25):

A much cheaper class of temporary storage would be great. It seems to me that in many applications which require storage but not permanent storage, we know how long temporary storage should be allocated for (e.g. [EIPs/EIPS/eip-1153.md at master · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1153.md), and also many layer 2 designs), or at least a reasonable upper bound for it.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/f04885/48.png) sinamahmoodi:

> I was also wondering if setting non-zero values to zero could be not only subsidized but rewarded, as a way to incentivize clearing unused storage. I saw there has been a proposal  along these lines by @axic. Has there been more discussion on why this might not be viable?

IMO providing incentives for clearing storage in a way that doesn’t also incentivize gastoken is impossible

---

**kronosapiens** (2018-11-25):

I would also be cautious about introducing rent too quickly – it fundamentally changes the relationship between users and contracts (by making contracts shared resources instead of perpetual services) and could disrupt many projects’ business models. Increasing the SSTORE cost seems like the most reasonable backwards-compatible solution. Also:

- I like the idea of a RAM-style intermediate storage between the stack and storage proper; as a new feature, we can introduce new constraints without throwing a wrench in everyone’s works.
- IIRC from discussing with a colleague, the limit on refunds is there b/c there is no incentive to mine a tx which involves paying money to the caller.

---

**veox** (2018-11-25):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/f04885/48.png) sinamahmoodi:

> I was also wondering if setting non-zero values to zero could be not only subsidized but rewarded, as a way to incentivize clearing unused storage.

Although this has been answered, I ranted off [in a separate thread](https://ethereum-magicians.org/t/transient-programs-an-ancient-execution-paradigm-with-multi-send-example-and-incentives-for-storage-clean-up/2013).

**TL;DR:** The incentive mechanism, as it currently stands, seems mostly unusable. But there may be a way around it, if we change our wicked ways.

---

**sinamahmoodi** (2018-11-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ldct/48/381_2.png) ldct:

> IMO providing incentives for clearing storage in a way that doesn’t also incentivize gastoken is impossible

I didn’t know GasToken was something to be mitigated. This [thread](https://ethresear.ch/t/use-of-https-gastoken-io-positive-or-negative-for-the-network/2790) proved helpful in outlining its potential long-term implications.

---

**AdamDossa** (2018-12-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> A third possibility that I have not yet seen discussed is to start off by raising the gas limit and increasing the SSTORE cost (possibly greatly increasing it, eg. 4-5x; also NOT increasing refunds to mitigate gastoken), and then start architecting a precompile that manages a cheaper class of temporary storage that follows some rent scheme.

IMO any increases to SSTORE need to be done alongside corresponding increases to gas limits (e.g. 4x SSTORE increase => 4x gas limit increase) to avoid issues with some functions becoming uncallable due to gas limits and potentially locking funds etc…

---

**alberreman** (2018-12-11):

Hello out there! I’m a writer for ETHNews and I’m trying to understand the state rent conversation, but coming up short on a lot of fronts.

A few weeks back, Vlad Zamfir posted on Twitter about how, even after sharding, that state size will be an issue. Why? He was saying that we need to impose limits on state size or else the VM will be f-ed. Why?

I get the idea of state rent insofar as it makes sense to me that you’d want to compensate people for storing data, but that doesnt seem to be what people are talking about. You’re talking about the state being too big, period. Is this just because it takes forever to sync?

And then, in the 1x call, state rent and state reduction were discussed separately. Why? Wouldnt state rent cease to be an issue if the chain were sufficiently pruned? (Maybe not, if we actually get some users. Then I guess we’d need both.)

I can also be reached at [aberreman@ethnews.com](mailto:aberreman@ethnews.com) or [@alberreman](/u/alberreman) on telegram

---

**AlexeyAkhunov** (2018-12-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alberreman/48/984_2.png) alberreman:

> And then, in the 1x call, state rent and state reduction were discussed separately. Why? Wouldnt state rent cease to be an issue if the chain were sufficiently pruned? (Maybe not, if we actually get some users. Then I guess we’d need both.)

There were two separate discussions because state rent only applies to the active state (this comprises of all non-empty accounts and all contracts that have been created but not self-destructed, with their storage). What you call “state reduction” discussion was discussion about other bits of data that Ethereum clients are currently storing, sharing around, and providing to dApps

---

**Flash** (2019-01-06):

Great write up, thanks! I’m trying to catch up with the current 1.x and 2.0 situation and this is a huge help, it’s all very interesting.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Users forget about some application they are involved in all the time. Even in ENS auctions which lasted a few days, I remember there were people who forgot to reveal their bids. From a usability point of view, a recovery path for an account that gets hibernated, even if an expensive one, is IMO essential.

I 100% agree, punishing users with irreversible deletion of their permanent shit would not go over well.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cdetrio/48/482_2.png) cdetrio:

> To be clear, past blocks and past logs would of course continue to be stored somewhere and be widely available, but they would not be stored by common full nodes which dominate the network. Full nodes would instead only store some recent history of blocks and logs, perhaps several months or so of data.

Is there any more information on how and where this archival data will exist? I’d be interested to read the current consensus on it. I’m not a big fan of the idea that you’ll have to pull data stored in extravagantly large nodes that only a few people control.

---

**jpitts** (2019-01-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/flash/48/1356_2.png) Flash:

> Is there any more information on how and where this archival data will exist? I’d be interested to read the current consensus on it. I’m not a big fan of the idea that you’ll have to pull data stored in extravagantly large nodes that only a few people control.

There does seem to be a gap in the 1.x proposals regarding “the state that is stored somewhere”, and it does need to be clearly addressed. Perhaps nodes of this type could be called “evicted state archive”, and can be incentivized so that there can be more operators running them.

Myself, [@tjayrush](/u/tjayrush), [@5chdn](/u/5chdn), and many others participating in the “Data Ring” could take a look at this and begin a discussion about possible incentivized nodes of this type.

---

**Flash** (2019-01-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> Myself, @tjayrush, @5chdn, and many others participating in the “Data Ring” could take a look at this and begin a discussion about possible incentivized nodes of this type.

Brilliant, I’ll look out for it! Thanks for the reply.


*(3 more replies not shown)*

---
source: magicians
topic_id: 2682
title: "Data Ring Topic: Query Interface"
author: tjayrush
date: "2019-02-19"
category: Working Groups > Data Ring
tags: []
url: https://ethereum-magicians.org/t/data-ring-topic-query-interface/2682
views: 931
likes: 5
posts_count: 8
---

# Data Ring Topic: Query Interface

According to the [Denver notes](https://hackmd.io/s/Sy6g5I7B4#) there was converstation related to a standard way to query the node:

1. TheGraph is working to standardize data schemes
2. Support for “predicate language” is needed. (e.g. Give me X addresses who sent Y ETH to Z contract when the contract’s balance was below W wei).
3. JSON RPC Interface (e.g. Building graphQL into Go-Ethereum)

**Action item:** @Corey will begin an EIP and foster conversation on Eth Magicians.

## Replies

**tjayrush** (2019-02-19):

My own two cents here.

I think there are two, somewhat divergent, use cases. The first is reflected above. The above implies a large-scale, cross-chain capability for generic queries (all token transfers on any address between June and July). This type of query all but ensures that it won’t work on resource-constrained hardware such as a single end-user’s desktop without either a third-party or some sort of incentive mechanism.

I think a very important capability that we should preserve is what I call ‘permissionless auditing.’ In the best version of this, every user is able to fully audit any smart contract directly from their own running local node. A solution of the first type requires a large (and ever growing) database. I think it’s possible to give up arbitrary querability, minimize the size of the extracted data, and give direct access to specific data that the user needs.

The other thing that ‘permissionless auditing’ leans toward is a way to get information on a smart contract at near zero cost. If the system we design only allows one to get information on smart contracts by paying for it, and the price adjusts based on what people are willing to pay, nearly all of us will be priced out of the market pretty quickly. If that were the case, I think, this would be a death blow for the whole system.

So, to the above list of concerns as we build a standardized interface for querying I would add:

1. Preserve the ability to do ‘permissionless auditing.’

---

**wildmolasses** (2019-02-20):

Thanks for spurring the conversation, Jay.

I’d like to argue, parallel to you, that the query interface should be separate from any specific method of data retrieval.

Because there is no standard query interface, dApp developers have had to implement their own data strategies. Often they become the custodians of an RPC endpoint or black box API. At best they rely on the user’s rpc provider, which comes with its own frustrations (queries limited to rpc interface only). We want more than the rpc interface (e.g. tx per address), and the query interface discussion should examine that. But getting back to the argument, dApp developers should not be responsible for the retrieval of dApp data. They should merely be responsible for phrasing their data questions correctly: “How many ERC20 transfers has address 0x…f seen in the last month?” This question should then be kicked to you the user to figure out. The user’s machine should have opinions on how to answer this question, from pinging a centralized data service like etherscan to freshening a local cache against the local node. Along with this I’d argue for a new piece of metadata, “was-locally-verified,” that is returned for every query.

Separating the query interface from the means of retrieval makes sense for a few reasons.

1. does not depend on a certain retrieval method being optimal for all cases, users, time periods
2. frees developers from ad hoc data hacks
3. mediates between the current paradigm of depending on centralized services, and the ideal of these queries actually getting resolved in a verified trustworthy way.

---

**jpitts** (2019-02-21):

I agree that there should be separation between the query interface and the method of data retrieval. That they could be standardized is very helpful however, enabling vendors to come in and say they have this kind of query interface to their data.

The ability to verify the data, the ability to compose, and vendor neutrality are key principles here. Standards need to be defined to make sure these principles can be expressed, and also the emergence of some kind of open data service layer.

I do not think that significant improvements in data access will happen in Ethereum or any of the major smart contract blockchain protocols, which is actually a big opportunity.

---

**jpitts** (2019-02-21):

Additionally, I am interested in the Cypher graph query language as an alternative to GraphQL. It relates to SPARQL and is implemented in [redisgraph](https://oss.redislabs.com/redisgraph/).


      [en.wikipedia.org](https://en.wikipedia.org/wiki/Cypher_Query_Language)




###

Cypher is a declarative graph query language that allows for expressive and efficient querying and updating of a property graph. Cypher is a relatively simple but still very powerful language. Very complicated database queries can easily be expressed through Cypher. This allows users to focus on their domain instead of getting lost in database access.
 Cypher was largely an invention of Andrés Taylor while working for Neo4j, Inc.(formerly Neo Technology) in 2011. Cypher was originally intended to...

---

**tjayrush** (2019-02-21):

We should keep in mind that there are two very different users here. One is someone who wants “every token transfer on these X tokens between June and July”, another wants to figure out exactly what’s happening on a particular address and wants to do so 100% independently.

If that second type of user needs to rely on a third party they will either (a) have to pay, (b) have to relinquish their privacy, or © be at the mercy of the provider to not withhold the data. All three of those things is exactly opposite of what I thought we were trying to build.

There’s definitely a chance for providers of the data to make money from a usable solution, but I look at that as a problem, not an opportunity.

---

**jpitts** (2019-02-21):

Probably I should add the principle of privacy to my list. The principle of vendor neutrality speaks to the notion that the data would be available if the user has the computing resources and time to perform the indexing/querying, otherwise they’d pay the network and retrieve the output.

---

**tjayrush** (2019-02-21):

With true vendor neutrality on immutable data there would be little reason to pay for it. The community could agree on the contents of the historical indexes (they would have to in order to insure vendor neutrality), and if they did people would soon realize that the indexes never change and anyone could publish the indexes to IPFS (or some other content-addressable store) and share the hashes.

From there, it would be trivial to build a near zero-cost API that delivers not the results of the query on the index, but the IPFS hash of the portion of the index that contains those results. The querying process can then download that portion of the index directly from IPFS and pin it locally, thereby making it available to itself and others. The more people that use a system like that, the more readily available the data becomes on IPFS, and the faster it will be to retrieve. For files already pinned locally, the speed on the local machine would be near instantaneous. This has the added benefit that heavy users (people who query across many addresses or run a heavily used smart contract) would carry most of the pinned files. Small users would pin only a small part of the index (as they should). But, over time, the entire community would have the entire index available through IPFS (if they had the hashes).

Of course, this only handles the index. The end user’s local software would then have to query for the actual transaction/block data, but this is where running a local node comes in (i.e. dAppNode). But notice that having a local cached index would also lower the traffic to sites such as Infura, because the user would now be querying for very specific data (the transaction directly as opposed to range queries as it currently works).

I’m not saying this is the only way it should work, but we should very carefully consider methods that lean more towards distributing the data at minimal cost as opposed to centralizing it and having to pay for the data. Having to pay for the data will, in my opinion, challenge the long term success of the entire platform.

We’ve already paid for the data through block rewards and gas fees. Why should we have to pay for it again because of an inadequacy in the way the node provides the data?


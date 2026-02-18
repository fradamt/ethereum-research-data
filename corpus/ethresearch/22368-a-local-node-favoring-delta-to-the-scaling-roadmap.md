---
source: ethresearch
topic_id: 22368
title: A local-node-favoring delta to the scaling roadmap
author: vbuterin
date: "2025-05-19"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/a-local-node-favoring-delta-to-the-scaling-roadmap/22368
views: 5852
likes: 89
posts_count: 55
---

# A local-node-favoring delta to the scaling roadmap

*Special thanks to Micah Zoltu, Toni Wahrstätter, Justin Traglia and pcaversaccio for discussion*

The most common criticism of increasing the L1 gas limit, beyond concerns about network safety, is that it makes it harder to run a full node.

Especially in the context of a roadmap focused on [unbundling](https://ethresear.ch/t/decoupling-throughput-from-local-building/22004) the full node, addressing this requires an understanding of *what full nodes are for*.

Historically, the thinking has been that full nodes are for *validating the chain*; see [here](https://vitalik.eth.limo/general/2021/05/23/scaling.html#its-crucial-for-blockchain-decentralization-for-regular-users-to-be-able-to-run-a-node) for my own exposition of what could happen if regular users cannot verify. If this is the only issue, then L1 scaling is unlocked by ZK-EVMs: the only limit is keeping the block building and proving costs low enough that both can remain [1-of-n](https://vitalik.eth.limo/general/2020/08/20/trust.html) censorship-resistant and a competitive market.

However, in reality this is not actually the sole concern. The other major concern is: **it’s valuable to have a full node so that you can have a local RPC server that you can use to read the chain in a trustless, censorship-resistant and privacy-friendly way**. This document will discuss adjustments to the current L1 scaling roadmap that make this happen.

## Why not stop with trustlessness and privacy via ZK-EVM + PIR?

The [privacy roadmap I published last month](https://ethereum-magicians.org/t/a-maximally-simple-l1-privacy-roadmap/23459) focuses on TEEs + [ORAM](https://en.wikipedia.org/wiki/Oblivious_RAM) as a short-term patch plus [PIR](https://en.wikipedia.org/wiki/Private_information_retrieval) as a long-term solution. This, together with Helios and ZK-EVM verification, would allow any user to connect to external RPCs and be fully confident that (i) the chain they are getting is correct, and (ii) their data privacy is protected. So it is worth asking the question: why not stop here? Don’t these kinds of advanced cryptographic solutions make self-hosted nodes an outdated relic?

Here I can give a few replies:

- Fully trustless cryptographic solutions (ie. 1-server PIR) will be expensive. Currently the overhead is impractically high, and even after many efficiency improvements it is likely to stay expensive.
- Metadata privacy. The data of which IP address makes requests at what times, and the pattern of requests, is itself enough to reveal a lot of information about users.
- Censorship vulnerability: a market structure dominated by a few RPC providers is one that will face strong pressure to deplatform or censor users. Many RPC providers already exclude entire countries.

For these reasons, there is value in continuing to ensure greater ease of running a personal node.

## Short-term priorities

- Up-prioritize a full rollout of EIP-4444, all the way up to the final end state where each node stores data for only ~36 days. This greatly reduces disk space requirements, which are the primary issue preventing more people from running nodes. After this, the disk space requirements for a node will be (i) state size, (ii) state Merkle branches, (iii) 36 days of history.
- Build a distributed history storage solution, by which each node can store a small percentage of historical data older than the cutoff. Use erasure coding to maximize robustness. This ensures the property that “a blockchain is forever” without depending on centralized providers or putting heavy burdens on node operators
- Adjust gas pricing to make storage more expensive and execution less expensive. A particularly high priority is increasing the gas cost of creating new state: (i) SSTORE for new storage slots, (ii) contract code creation, (iii) sending ETH to accounts that do not yet have a balance or nonce.

## Medium-term priority: stateless verification

Once we enable stateless verification, it becomes possible to run an RPC-capable node (ie. one that stores the state) without storing state Merkle branches. This further decreases storage requirements by ~2x.

## A new type of node: partially stateless nodes

This is the new idea, and will be key for allowing personal node operation even in a context where the L1 gas limit grows by 10-100x.

We add a node type which verifies blocks statelessly, and verifies the whole chain (either through stateless validation or ZK-EVM) and keeps up-to-date a *portion* of the state. The node is capable of responding to RPC requests as long as the required data is within that subset of the state; other requests will fail (or have to fallback to an externally-hosted cryptographic solution; whether or not to do this should be the user’s choice).

[![partial_statelessness.drawio](https://ethresear.ch/uploads/default/optimized/3X/6/5/65e830fde9112642eb74f76377116aa9740129a6_2_690x303.png)partial_statelessness.drawio776×341 19.9 KB](https://ethresear.ch/uploads/default/65e830fde9112642eb74f76377116aa9740129a6)

The exact portion of the state to be held will depend on a config chosen by the user. Some examples might be:

- All state except for contracts that are known to be spam
- State associated with all EOAs and SCWs and all commonly used ERC20 and ERC721 tokens and applications
- State associated with all EOAs and SCWs that have been accessed in the last two years, some commonly used ERC20 tokens, plus a limited curated set of swap, defi and privacy applications

The config could be managed by an onchain contract: a user would run their node with `--save_state_by_config 0x12345...67890`, and the address would specify in some language a list of addresses, storage slots or otherwise filtered regions of the state that the node would save and keep up to date. Note that there is no need for the user to save Merkle branches; they only need to save the raw values.

This type of node would give the benefits of direct local access to the state that a user needs to care about, as well as maximal full privacy of access to that state.

## Replies

**GalRogozinski** (2025-05-19):

Interesting!

Excuse my silliness, but why do you offer to save the config onchain? Why not have a free and private config in a file?

---

**amadeobrands** (2025-05-19):

Makes sense.

The main goal should be to make L1 fast enough to enable on-chain price discovery for assets. L1 should serve as the global settlement layer, even for all L2 prices. Assets seeking hard settlement guarantees should originate on L1.

I believe this approach can achieve that state, but we need to recognize that many people, including myself, prefer to hold major assets on L1 rather than L2s.

---

**vbuterin** (2025-05-19):

it’s a convenience feature to allow a third-party actor (could be a DAO) to keep the config up to date.

---

**Vitomir2** (2025-05-19):

Pretty interesting read — **thanks for sharing!**

I’m curious about the longer-term history though. What if someone wants to verify transactions from, say, five years ago on Etherscan?

Would that still be possible after implementing a mechanism that retains history for only 36 months?

---

**bklnf** (2025-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This greatly reduces disk space requirements, which are the primary issue preventing more people from running nodes

Sorry, but 4tb nvme cost is 300-500usd.

Main blocker from running a node is the size of 32ETH deposit.

Running node with x10(at least) less deposit will onboard whole new wave of home node operators

---

**Noveleader** (2025-05-19):

It is 36 days.

The goal here is to ease out the local node running process. I think the global data would still be dependent on RPCs.

---

**Killari** (2025-05-19):

Cool ideas!

Rather than DAO or on-chain config managing on what state the node is keeping, I would give this power to the node operators. We could have an UI that would let user select and add what ever addresses to maintain state for. You could have a DAO managing address metadatas, eg uniswap pools = [0x23, 0x12], tornadoCash = [0x23…]. And the user could then check the checkboxes which state to manage.

A good example of this is IPFS desktop, that lets users to select which data to keep. The user should be able to select and deselect these addresses at any time and the node would start to adapt to users preferences (slowly, but eventually as retrieving new data from decentralized network takes time). IPFS has `wanted_list` system that manages this. You could also have some private RPC methods that allow you to manage on what data to keep and what not to keep.

---

**Killari** (2025-05-19):

You need 0 eth to run a node, there’s no 32 ETH deposit requirements. The 32 ETH is required to run a validator. This thread is about running nodes, not validators.

---

**GregTheGreek** (2025-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The most common criticism of increasing the L1 gas limit, beyond concerns about network safety, is that it makes it harder to run a full node.

If we’re on the topic of more *at home setups*, it should be noted we probably need to draw down ingress/egress. Depending on where you are the concept of *unlimited bandwidth* might not exist.

I’m aware there are efforts to potentially erasure code, and do more structure gossiping on the p2p level but would probably bake this in as a concern for this sub group of node operators.

---

**MicahZoltu** (2025-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/bklnf/48/19952_2.png) bklnf:

> Sorry, but 4tb nvme cost is 300-500usd.
> Main blocker from running a node is the size of 32ETH deposit.

You are talking about stakers.  This post is talking about end-users of Ethereum who need the ability to execute against state in a censorship resistant and privacy preserving way.  These people do *not* have 32 ETH, and most of them may not have $500 to spend.

---

**soispoke** (2025-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A new type of node: partially stateless nodes

This relates to some recent thoughts we had around Validity-Only Partial Statelessness ([VOPS](https://ethresear.ch/t/a-pragmatic-path-towards-validity-only-partial-statelessness-vops/22236/1)): nodes keeping just enough data to ensure they can maintain a healthy mempool to ensure we can scale while preserving CR. This would result in just storing the account data, and gives us **25x storage reduction**.

I really like the general approach of providing more flexibility in what partial-state nodes choose or need to store, depending on the use case:

- Nodes actively participating in protocol duties (e.g., attesters, FOCIL includers) could be required to store at least the state necessary to maintain the mempool (VOPS).
- However, there shouldn’t be strict requirements for nodes that simply want to read the chain in a trustless, CR-preserving, and privacy-friendly manner. They should just be able to keep as much state as they want depending on how often they would have to query state from elsewhere. But then the “elsewhere” part is still very important, and we’re trying to see if Portal could provide a good enough solution for random access lookups there.

---

**MicahZoltu** (2025-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> the address would specify in some language a list of addresses, storage slots or otherwise filtered regions of the state that the node would save and keep up to date

This could be a good use for something like [GitHub - Austin-Williams/cid-accumulator-monorepo: Trustless, decentralized CID accumulator for smart contracts —append, verify, and retrieve all your on-chain data via IPFS.](https://github.com/Austin-Williams/cid-accumulator-monorepo), so your on-chain updates would be on the order of 10,000s of gas with ~0 state growth, but it would perpetually link to a file that was maintained on the IPFS network by anonymous 3rd parties.

It is limited to append only, but you could split the files into 12 month epochs, and each file would contain a journal of additions and removals from which you can rebuild the final set for each epoch.  One could imagine some way to materialize the epochs into a different format via social layer so you have a base list + accumulator over the course of a year.

---

**CPerezz** (2025-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The node is capable of responding to RPC requests as long as the required data is within that subset of the state;

This I assume is opening the door for Wallets or Dapps to follow some sort of “Dapp storage support” where they store their part of the state and serve to their users while at the same time, they keep the nodes to assert correct root.

Then, they can serve RPC requests to their users (who can follow the chain with something like [VOPS](https://ethresear.ch/t/a-pragmatic-path-towards-validity-only-partial-statelessness-vops/22236).

So, in short, are wallets and Dapps the parties who we pretend to handle over the state storing and the RPC serving wrt their protocol-related data?

If so (and I think this makes sense) within stateless-consensus we’re carrying over a survey with Wallets and Dapps for stateless-related questions.

Would you be up for some feedback and proposing questions we should ask them or things/opinions/takes from their side?

One of our fears has always been that Dapps (specially good and useful ones) are a scarce resource. And putting more burden on them to build this partial RPC servers might be complex.

What’s your take?

---

**daniellehrner** (2025-05-19):

With Besu we already have an implementation of the flat state without the Merkle nodes and can confirm that it reduces the disk requirements drastically. For mainnet the full state only requires 80GB like that. Saving only part of the state would only be a small change.

The remaining challenge is adding proofs to verify the state.


      ![](https://ethresear.ch/uploads/default/original/3X/6/b/6b34e13fc4f9390761cfc8c248df9c6ed6e71160.png)

      [Consensys](https://consensys.io/blog/besu-fleet-the-future-of-rpc-scaling)



    ![](https://ethresear.ch/uploads/default/optimized/3X/8/6/8622e15b54d0a042986f2e5af65d7d24f49ddc77_2_690x361.jpeg)

###



This blog introduces Fleet for Besu, an LF Decentralized Trust project. This solution simplifies RPC service scaling while cutting costs and efficiency.

---

**MicahZoltu** (2025-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> This I assume is opening the door for Wallets or Dapps to follow some sort of “Dapp storage support” where they store their part of the state and serve to their users while at the same time, they keep the nodes to assert correct root.

This isn’t the future I personally want to see play out, though I recognize that it is a possibility (if I correctly understand what you are describing).  What I would like to see play out is end-users are able to run their own RPC servers that follow head and store *the vast majority* of all interesting state on Ethereum.  They would only drop things like spam/scam tokens, and state from apps that haven’t been touched in a decade (which combined I suspect is probably a very significant chunk of state usage on Ethereum if I had to take a wild guess).

With some proof related improvements, a trustless node like this could probably use less than 100GB without any state dropping, and maybe less than 50GB with state dropping.  This combined with UX improvements around node operations, and having these clients not execute blocks themselves (just validate proofs), and we can imagine a future where users just double click an installer and it runs in the background until the next hard fork (where they will have to update).

---

**vbuterin** (2025-05-19):

I think VOPS makes sense. One nuance that is worth keeping in mind is how these whole ideas would intersect with full AA (EIP-7701).

It feels like recently the way full AA thinking is trending is, keeping the protocol-level EIP itself minimal, and then encouraging the development of custom mempools that support custom sets of validity conditions targeting specific application categories (eg. wallets, privacy protocols, defi protocols [so you can safely make swaps with zero slippage tolerance and thereby protect yourself from sandwiching])

What this implies is that “which partial state you have to keep” itself becomes mempool specific, and so it’s a choice of each node implementation.

Which seems like it is compatible with the idea as a whole? Because there is no need for any global consensus on which state is kept and which state is not kept.

---

**juanfranblanco** (2025-05-19):

A couple of thoughts,

I believe that eventually enabling Dapps or users selecting the state they require will be ideal, not just a mini node level. User opens an application mobile / desktop / game / web (local storage or probably here a mini node to support it) and has the state they required synced, it might not be the whole 1 gig for the USDC Erc20 (tested that a year ago), but a fraction. A more complex data store like a game, or generic application, you store your data, validate and sync, when opening your app.

This types of applications could use “session / temporary delegated accounts”, like the ones in MUD, encouraging a more secure behaviour per account, and phishing attempts.

Distributed history could be complemented with other data, like transactions per account, which is left to indexers (although the current indexers, like etherscan, etc, could be the ones that create a new type of verification layer for this type of data), and ideally use that opportunity to store the transfer of Eth or “native tokens in L2s / L(x)s” without making any changes like Optimism tried before, to simplify the process.

Apps verify with proofs the data / simulate, etc… which could be done now if “eth_getProofs” like “helios” but I guess easier with verkle trees, when available.

---

**CPerezz** (2025-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> and store the vast majority of all interesting state on Ethereum.

This is exactly what state expiry will get us eventually.

I don’t think we disagree. I think the only problem we have here is that *vast majority of all interesting state* is something that will be HUGE if Ethereum becomes the ground for all economy-related activities in the future.

L2s will help there too ofc.

> Nevertheless, the amount of interesting state tends to infinity when time grows enough. And that is something that no measure (neither state expiry can solve).

Thus, the idea from Vitalik makes a lot of sense in combination with these types of nodes loke VOPS or Ress.

Users can follow the tip of the chain trustlessly, participate in consensus duties and keep healthy mempools for FOCIL or tx broadcasting.

On the other hand, Dapps and Wallets can keep the piece of protocol-related state only instead of a bunch of useless data they’ll never use for anything.

Then, these Wallets and Dapps can have a much easier time serving requests via RPC to their users specifically which can be verified against trustlessly-asserted roots.

Otherwise, we always need a `GOOD_SAMARITAN` who will serve this data to users that don’t want to store anything locally. Maybe not now. Maybe not in 10 years even.

But eventually, the fact that this happens means ethereum succeeded and became so big and important that we need to rely on these solutions.

The only caveat to all these discussions, is that this is only possible if the block producer **HAS ALL THE STATE**. Otherwise, `strong_statelessness`-like solutions will significantly harm UX unless a ton of effort is put. And won’t enable gas_scaling nor following the tip of the chain at such a low cost.

---

**soispoke** (2025-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I think VOPS makes sense. One nuance that is worth keeping in mind is how these whole ideas would intersect with full AA (EIP-7701).

Agreed, we had an **“AA-VOPS”** section in the post, where each node would only need to track the accounts it actively cares about (its own EOAs, those it interacts with, and frequently accessed contracts such as *TokenPaymaster* and *USDC*), maintaining a small local cache that is updated incrementally over time using `stateDiffs` from block producers.

But this comes at the cost of having to attach witnesses to transactions, leading to similar challenges as those found in strong statelessness proposals (higher P2P bandwidth, latency overhead, and the question of *who* should hold the full state then). Also unlike in your proposal, these nodes couldn’t really be queried in a general-purpose way, since they only hold state for the accounts they care about.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Which seems like it is compatible with the idea as a whole? Because there is no need for any global consensus on which state is kept and which state is not kept.

I think it is compatible with the general idea, but the nuance there is that we probably need global consensus on which state is kept for protocol participants that are responsible for preserving CR? Ideally we wouldn’t have to trade off CR for cool applications leveraging full AA, but not sure how to resolve that tension. If full AA at the protocol-level is minimal and close to what we have with 7702 (or at least only requires small, non-expensive checks for txn validity), then we could do something like:

- Attesters and includers are required to hold validity-only state to preserve strong CR and, optionally, any state needed to support a particular application/protocol making use of full AA (they would signal this somehow to make sure this state can be queried from them)
- Any dApp or wallet making use of full AA is responsible for holding the corresponding state and generate witnesses associated with user transactions, or broadcast the txns in a specific mempool
- Nodes staking 2048 ETH are required to store the full state
- Portal provides good guarantees about random state access

---

**MicahZoltu** (2025-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> This is exactly what state expiry will get us eventually.

I would *love* to see state expiry implemented!  I spent something like 6 months trying to solve it with some Ethereum researchers a while back but we were never able to come up with a solution that we thought would be satisfactory enough to actually get implemented.  If someone has figured out a solution I would love to hear it!


*(34 more replies not shown)*

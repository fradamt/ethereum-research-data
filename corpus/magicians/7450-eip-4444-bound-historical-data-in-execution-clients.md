---
source: magicians
topic_id: 7450
title: "EIP-4444: Bound Historical Data in Execution Clients"
author: matt
date: "2021-11-10"
category: EIPs > EIPs networking
tags: [state-expiry]
url: https://ethereum-magicians.org/t/eip-4444-bound-historical-data-in-execution-clients/7450
views: 9311
likes: 44
posts_count: 46
---

# EIP-4444: Bound Historical Data in Execution Clients

Discussion thread for [EIP-4444](https://eips.ethereum.org/EIPS/eip-4444).

## Replies

**yoavw** (2021-11-10):

A link to the EIP itself?  (I don’t see it in the github repo)

---

**matt** (2021-11-10):

Was hoping to get it merged quickly and update with `eips.ethereum.org` link, but it didn’t happen. I’ve updated it just now with the PR link.

---

**mkalinin** (2021-11-11):

It worth say when the specification of this EIP comes into effect. An important thing that this change depends on the Merge. This is because before the Merge historical block headers are essential for sync and bootstrapping process. Verifying the PoW seal of all blocks in the chain is the only way to prove the chain is valid. Network upgrade to PoS shifts this paradigm and makes historical data of EL chain not a requisite for node bootstrapping process.

I don’t think that this spec should be so prescriptive, i.e. saying MUST NOT wrt serving ancient data. The reason is that sync process of some clients may depend on the historic data and they will need a time to be prepared for such a big change. For instance, Erigon executes all blocks since genesis and doesn’t used any state downloading techniques to get in sync with the network; they will probably want to serve ancient blocks even if other clients stop doing it.

IMO, the purpose of this EIP in the context of the Merge is to send a clear signal to infra, users, and clients that they should consider that the invariant of storing the history is going to be broken in some future. If we don’t want this for the Merge then it could be prescriptive but it worth considering that it will take a lot of time for network participants to get prepared for such a change.

---

**djrtwo** (2021-11-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mkalinin/48/3343_2.png) mkalinin:

> I don’t think that this spec should be so prescriptive, i.e. saying MUST NOT wrt serving ancient data.

I disagree here. If we don’t make this prescriptive then we will have a gradual degradation in historic block and receipt sync while users/clients still rely on it, until it just becomes broken and a bunch of users are confused and upset.

Making this a **MUST NOT** serve makes this a harder EIP to implement because it will require preparing dapps (especially receipts) and users for this breaking change, but then it will be completed in a clean way. If instead it’s a **SHOULD NOT** or **MAY NOT**, we create a path for dapps to slowly become broken on some indefinite timeline (because many will just continue to rely on the functionality for as long as it seems to work).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mkalinin/48/3343_2.png) mkalinin:

> For instance, Erigon executes all blocks since genesis and doesn’t used any state downloading techniques to get in sync with the network; they will probably want to serve ancient blocks even if other clients stop doing it.

iiuc, Erigon has had a torrent block downloader in production for quite a while (it is *way* faster) and is expecting this breaking change at some point.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mkalinin/48/3343_2.png) mkalinin:

> IMO, the purpose of this EIP in the context of the Merge is to send a clear signal to infra, users, and clients that they should consider that the invariant of storing the history is going to be broken in some future

I agree with this, but to do so effectively, I think the strategy is to specify the EIP as it will be in it’s final form and begin communicating about it now rather than actually introducing the breaking change simultaneously with the Merge. Imo, this is going to take 12+ months to properly communicate and execute on the dapp/community side, but this EIP can use the Merge and weak subjectivity in it’s rationale to bound it to this shift to PoS even though it wont be fully implemented at the point of the shift.

---

**gcolvin** (2021-11-12):

> Preserving the history of Ethereum is fundamental

Yes.

> We suggest that a specialized “full sync” client is built. The client is a shim that pieces together different releases of execution engines and can import historical blocks to validate the entire Ethereum chain from genesis and generate all other historical data.

You don’t say who would build or maintain this client.  And it’s not clear to me how the shimming would work.  Existing clients go to some effort to efficiently manage the differences between releases, given most of the code hasn’t changed.

> There are censorship/availability risks if there is a lack of incentives to keep historical data.
> …
> there is a risk that more dapps will rely on centralized services for acquiring historical data.

Yes.  And I don’t think mitigating these risks is “out-of-scope for this proposal”.

---

**matt** (2021-11-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> it’s not clear to me how the shimming would work

Let’s say there are upgrades X, Y, and Z. During X, clients support X. During Y, clients support Y and so on. After each fork the code to run the fork is removed (save for the transition period of the fork). So if you want to validate the entire chain, you would start the client version that supports X and import all the X blocks. Then it would shutdown and you would run the client version that supports Y with the same data directory and again import all the blocks. Proceed with this and eventually you’ll be executing the tip of the chain with everything validated. The two caveats are i) after the merge, you’ll also need to get the beacon history and drive clients with that and ii) you may need to run glue code between client versions if there are breaking changes to the state / history storage.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> And I don’t think mitigating these risks is “out-of-scope for this proposal”.

I think there are pretty straightforward solutions to replicated storage of static data that we can tap into for this (e.g. IPFS, torrent, data mirrors, etc).

–

Copying from the PR thread:

> @djrtwo: Note, that discussions with @karalabe have pointed to making this a MUST because otherwise users will still rely on it while quality of this feature degrades until it is unusable. A MUST, instead, forces users and dapps to actually “upgrade” how they utilize this at the point of this shipping, forcing everyone’s hand so it doesn’t silently get worse and worse.

> @djrtwo: If we go that path, then this spec should specify that devp2p does return errors on requests outside of the specified range of epochs/time

I feel like `SHOULD` is adequate level of force for clients to do this? Geth continue to make up a large portion of the network and if they stop serving the data, it’s going to mostly be unavailable (and users will mostly be forced to adapt). That said, I don’t have a strong argument for one or the other. The one caveat is that most devp2p messages wouldn’t know how to distinguish requests for “non-existent data” and “expired data” because they are by hash. Only `GetBlockHeaders` is done via block number and could therefore return an error.

If we were to go with `SHOULD` and `GetBlockHeaders` returns an empty response instead of error, I think the main fail case will be clients that try to header sync the old way will be confused since they don’t get any headers back. This seems acceptable and avoids an new wire protocol version.

–

> @axic:  Actually back in April 2020 or so, within the Ipsilon team we thought about making a proposal to just hardcode given hashes for given blocks in an EIP. The idea would be to hardcode the hashes for past hard forks.

> However then regenesis was proposed, which in practice does the same, but programatically.

> Since regenesis as a concept is delayed ever so often, and given this EIP, would such a proposal make sense now?

In my mind, regenesis tackles a slightly different problem (and when I say regenesis, I generally mean [this version](https://notes.ethereum.org/@vbuterin/verkle_and_state_expiry_proposal)). This EIP is about removing the need to store *historical* data whereas regenesis is a mechanism primarily aimed at reducing the *state* data. Regenesis, as far as I understand it, does not prescribe that clients should discontinue holding historical headers / bodies / etc.

I am curious to understand better what you mean about hard coding past fork blocks. I think you’re referring to a type of weak subjectivity checkpoint?

–

Generally a question that keeps coming up is how to deal with the difference between non-existent and expired data. Geth has set the precedence in `v1.10.0` by turning the `txlookup` index to prune indexes older that 1 year by default. This means that if a user calls `eth_getTransactionByHash` with a valid tx hash from Byzantium, it will return an empty response.

Is the going to be acceptable behavior other data like blocks? And is acceptable over the wire? Seems like we’re leaning towards “yes”.

---

**MicahZoltu** (2021-11-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/djrtwo/48/859_2.png) djrtwo:

> I disagree here. If we don’t make this prescriptive then we will have a gradual degradation in historic block and receipt sync while users/clients still rely on it, until it just becomes broken and a bunch of users are confused and upset.
>
>
> Making this a MUST NOT serve makes this a harder EIP to implement because it will require preparing dapps (especially receipts) and users for this breaking change, but then it will be completed in a clean way. If instead it’s a SHOULD NOT or MAY NOT, we create a path for dapps to slowly become broken on some indefinite timeline (because many will just continue to rely on the functionality for as long as it seems to work).

My understanding of RFC 2119 is that what you are describing is exactly what **SHOULD** is used for.  **SHOULD** is a way for a specification to say “this behavior is what is best for the ecosystem/user, but it isn’t something that is strictly enforced and if you don’t follow it nothing is going to outright break”.

---

**gcolvin** (2021-11-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> So if you want to validate the entire chain, you would start the client version that supports X and import all the X blocks. Then it would shutdown and you would run the client version that supports Y with the same data directory and again import all the blocks. Proceed with this and eventually you’ll be executing the tip of the chain with everything validated

That’s what I feared ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12) It means all of these clients have to be maintained indefinitely.

---

**gcolvin** (2021-11-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> gcolvin:
>
>
> And I don’t think mitigating these risks is “out-of-scope for this proposal”.

I think there are pretty straightforward solutions to replicated storage of static data that we can tap into for this (e.g. IPFS, torrent, data mirrors, etc).

Then I’d like a bit more discussion of what the solutions and who is responsible for fixing what is going to get broken.

---

**MicahZoltu** (2021-11-13):

A. This is only necessary if one wants to validate the entire blockchain from genesis, which I argue is an uncommon operation at best, and I suspect eventually will simply be something that no one does.

B. The old clients don’t have to be maintained, they only need to continue to exist.  No updates need to be applied to them.

---

**jpitts** (2021-11-15):

> Preserving the history of Ethereum is fundamental and we believe there are various out-of-band ways to achieve this.

It should be stated what preserving the history of Ethereum is fundamental to, and how important state history preservation is relative to other properties of the protocol.

And if it is as fundamental as stated, why do the authors not propose an alternative, sustainable mechanism for it?

*Adding this:* Not that the current situation is indefinitely sustainable, but the current requirement sufficiently preserves and provides state history. The burden put on network users is heavy and growing, but there needs a realistic plan for how to maintain this widely-used aspect of the Ethereum network.

---

**gcolvin** (2021-11-15):

Yes.  The Ethereum blockchain is, fundamentally, an immutable record of transactions – value transfers and  valid computations. It seems to me that there should be *some* standard protocol for that, however the history is stored.

---

**mkalinin** (2021-11-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/djrtwo/48/859_2.png) djrtwo:

> Making this a MUST NOT serve makes this a harder EIP to implement because it will require preparing dapps (especially receipts) and users for this breaking change

Additionally, if we use **MUST NOT** then the peer that breaks this requirement **SHOULD** be disconnected and penalised.

---

**tjayrush** (2021-11-24):

I agree completely that “preserving this widely-used aspect of the Ethereum network” is of utmost importance. But why does it have to be a capability that the node maintains?

It seems to me that maintaining this ability in the node is exactly the problem. If the data is immutable, the entire state and the entire history of the chain can be written **once** to some content-addressable store (such as IPFS) and as long as someone preserves that data, anyone can get it. AN Ethereum node would not even have to be involved. All one would need is the hash of where the immutable data is stored.

Fresh data can be written as an ‘addendum’, so there would have to be some sort of published manifest of the original hash and the periodic ongoing hashes. I would argue that the hash of the manifest should be part of the chain, but, short of that, the community would have to maintain it (perhaps by publishing the hash to a smart contract).

My point is that because the data is immutable, and because we have content-address storage to store it in, there’s literally no need to continue to provide the ability to regenerate this data from genesis. The only outcome of regenerating from genesis would be to arrive at the same IPFS hash as you already have.

On top of that, there’s no reason the clients have to maintain this capability, and the entire purpose of this EIP is to remove that requirement. This might possibly open a whole new area of innovation related to providing access to this historical data – which I think would allow for amazingly more interesting dApps than we currently have (because of the need for a node to get to it).

Furthermore, if the historical data is chunked into manageable pieces, and it was properly indexed by chunk (with a bloom filter in front of each chunk) each individual user could easily download and pin only that portion of the database that they are interested in. Thereby distributing this historical data throughout the community as a natural by-product of using it. (See TrueBlocks).

---

**anett** (2021-12-01):

I agree that people are uploading lot of stuff on blockchain especially with the rise of NFTs but also not optimized token contracts which are causing state bloat. But did anyone think about other examples and use cases of blockchain? What if people uploaded their important documents like birth certificates on blockchain as the mission of blockchain is ledger which stores information on-chain forever. Suddenly those people won’t be able to access their documents because some devs thought it’s a good idea to delete blockchain state after some time… Another great example is NFTs especially NFTs that were made before ERC-721 ie 2017 and older like CryptoPunks. Those will be gone for ever.

From developer perspective, I’m sure that there are many data that are not important and doesn’t need to be stored.

Probably better idea would be to store data on full nodes and have light nodes or think about different ideas how to make infrastructure the most efficient without having to delete and loose data.

Don’t get me wrong, I’m just trying to think realistically from non-core-dev perspective and I’m against this EIP.

---

**MicahZoltu** (2021-12-02):

Ethereum was never designed to be a permanent data storage system.  Something like FileCoin is much better suited for long term data storage, and they have incentives built into the protocol to ensure that the cost of long term storage is paid for by those seeking it.

Also, this EIP removes *history* but not *state*.  State expiry is also an active area of research, but out of scope for this thread.

---

**niceblue** (2021-12-07):

I have been an Ethereum watcher and dapp developer for years, and have admired all the EIPs that have come through. However, this EIP is deeply troubling. I think this would be an extremely negative EIP to implement. Here’s why:

Ethereum was touted as the system to build “unstoppable” apps over the years, I loved it. With this EIP, these “unstoppable” apps will simply, well, stop (at least, their UXs/UIs will). It forces substantial and necessary adoption of some a.n.other (unknown and uncertain) protocol entirely outside of the Ethereum system. Pulling the “promise” of data persistence on old apps will be disastrous for the long term reputation of dapp development on Ethereum.

For those who say Ethereum was never meant to store data permanently, that is simply not true. It was! It’s *specced* that way and therefore *used* that way. And with this EIP, it will no longer. This is a truly fundamental change to (and destruction of) the Ethereum value proposition. Providing canonical transaction history tightly coupled with canonical transaction generation is CRITICAL to Ethereum’s value proposition. Offloading this entirely outside of Etheruem’s control gives away (and destroys) the future utility of Ether. Why? Because the whole point of canonical transaction generation is that you also have canonical transaction history.

**With EIP 4444, it is possible to lose entire chunks of past transaction history. Forever. As in gone. No one knows who sent (or did) what to who or when.**

There’s a reason why JP Morgan, HSBC, etc, any of these long storied banks are still around. It’s because you can rely on them having, somewhere inside their big walled offices, a transaction history going back over 100 years. This builds TRUST (yes, centralized trust). But that’s why (other) people come back to them (even if blockchain ppl don’t). The old history may be hand written in log books, sure not convenient, but it’s there.

Now imagine Ethereum was just such an organisation. You go to Ethereum in 12 years time and you ask (in code), what transaction happened on this account 10 years ago? The reply: oh go to Graph/Bittorrent/IPFS/a.n. other, we don’t keep that. You try numerous of these organisations, by some stroke of bad luck, they messed up on your particular EOA/contract (or their tech dies), and it’s gone. Would you trust the Ethereum system, simply because it moved to cool stateless consensus, and therefore decided they didn’t need to include anything as boring as past history anymore? I wouldn’t.

What this EIP fails to realise is that the value of canonical decentralised transactions in almost all *real world* use cases isn’t canonical decentralised  transactions, but *canonical history of* decentralised transactions. The blockchain that does this will win. Ethereum does both today, but with this EIP, it won’t any more. That’s what I would call the broken promise of Ethereum if this EIP happens, and without a simultaneous EIP that ensures canonical transaction history *at the Ethereum protocol level*. Perhaps some compromise can be made on time horizon. “Forever” is not enforceable, but say 20 years (for example) is, and good enough for most real world use cases (but even then not good enough for academic records, for example). Remember, the well known banks most of us also use can keep (centralised) canonical records for over a century, and universities can keep records for multiple centuries.

---

**Lilaaffe** (2021-12-07):

Arweave fixes your problem. Period.

---

**niceblue** (2021-12-07):

It is a.n.other protocol. canonical transaction history is *absolutely critical* to Ethereum. Why entrust that outside? If Arweave figures out Smartweave properly, let’s see where Ether ends up. More power to Arweave ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=10)

---

**aronchick** (2022-02-10):

Hi! I co-lead ResDev for Protocol Labs, we’re more than happy to help make available prove-ably immutable history of ETH forever on Filecoin & IPFS, and would not require any protocol changes. Please don’t hesitate to let me know if anyone would like help doing this!

Thanks!


*(25 more replies not shown)*

---
source: magicians
topic_id: 2352
title: Discussion about storage rent "eviction archive" nodes and incentives
author: jpitts
date: "2019-01-07"
category: Working Groups > Data Ring
tags: [storage-rent]
url: https://ethereum-magicians.org/t/discussion-about-storage-rent-eviction-archive-nodes-and-incentives/2352
views: 2265
likes: 7
posts_count: 7
---

# Discussion about storage rent "eviction archive" nodes and incentives

*Updated to remove the assumption that the state would be recoverable on Ethereum nodes.*

This is to begin a discussion about how state will be stored on behalf of ethereum accounts which have not paid their storage rent. While [the process of restoration has been proposed](https://ethereum-magicians.org/t/discussion-about-storage-rent-eviction-archive-nodes-and-incentives/2352/3?u=jpitts), there is a gap in how “the state that is stored somewhere” is actually stored.

In the current thinking around recoverable eviction, it is up to the user to have the removed state data, or perhaps up to a community-run service. How might reliable storage of this data be incentivized?

This discussion began with [comments in the Ethereum 1.x half baked roadmap thread](https://ethereum-magicians.org/t/ethereum-1-dot-x-a-half-baked-roadmap-for-mainnet-improvements/1995/20?u=jpitts):

Myself, [@tjayrush](/u/tjayrush), [@5chdn](/u/5chdn), and many others participating in the “Data Ring” could take a look at this and begin a discussion about possible incentivized nodes of this type.

[/quote]

---

**Beyond the discussion here in the Forum, I have also [proposed a Data Ring session](https://hackmd.io/s/SJDKo6lME#Data-Ring) to occur at the Magicians Gathering one day before EthDenver.**

## Replies

**jpitts** (2019-01-07):

For my two cents, I believe that all types of nodes which are essential to a healthy Ethereum mainnet network should be incentivized, whether light, full, archive, or this possible “eviction archive”.

An incentivization scheme for running nodes providing storage could feed information back to decision-makers or other processes in order to compute reasonable storage rent fees.

---

**jpitts** (2019-01-08):

Clarifying about the 1.x “recoverability”, I see that this has been defined in proposals dating back to November. I am getting more info on if any additional data beyond what is normally available on a full node is required to restore.

Felix Lange / fiji originally proposed a RESTORETO opcode in his [storage rent gist](https://gist.github.com/fjl/b495aa2154944263811eb1a73c6498cd#restoreto-addr-codeaddr):

A key description of the mechanism is from Page 56 of [@AlexeyAkhunov](/u/alexeyakhunov)’s [Ethereum state rent - rough proposal](https://github.com/ledgerwatch/eth_state/blob/58351eb8b70fa6031da1e23c1a77d982be677078/State_rent.pdf) dated Nov 26, 2018:

> New opcode PAYRENT is introduced to top up rentbalance by spending ETH, and RENTBALANCE (to read rentbalance). This can help keep existing contracts alive until they are migrated.
>
>
> When rent is not paid, contracts leave a “hash stump”, which can be used to restore the contract using opcode RESTORETO. This is different from semantics after Step 3, where linear cross-contract storage would be lost. At this step, linear cross-contract storage can also be recovered with RESTORETO.

[@holiman](/u/holiman)’s TLDR description:

> This scheme makes it possible to resurrect arbitrary size contracts, since you can spend infinite time on rebuilding the data-structure. Other types of resurrect, with proofs included in the transaction that does the restoration, has a practical limit on how much data you will be able to supply

---

**jpitts** (2019-01-08):

Further clarifying if any additional data beyond what is normally available on a full node is required to restore. The TLDR on that and implications:

- The restoring user must restore their state in a series of steps, calling the proposed RESTORETO opcode within a contract.
- RESTORETO accepts 1. addr of the hash stump left on eviction, and 2. addr of a contract from which code is taken.
- This user needs to have the evicted state data, or needs to get this data from some eviction archive service. This data is used in the contract.
- RESTORETO is not burdensome on any nodes, but is burdensome on the user depending on the size of state being restored.

From [questions asked on the all core devs gitter channel](https://discordapp.com/channels/420394352083337236/456572697892093962/532223660715409408) (edited for clarity):

> jpitts:
> Assuming the scenario described in the “rent-eip.md” gist, would the work done by RESTORETO be performed on full nodes? Clarifying that this would not require any kind of special storage outside of full nodes.
>
>
> An additional question regarding RESTORETO, how burdensome is this computation on the node? IMO, some of the misunderstanding about restoration may be rooted in misunderstanding that the entire state of the blockchain can be regenerated from a full node. even though it may not be immediately available.
>
>
> holiman:
> It would execute like any other opcode. Not sure I understand the Q. Whoever is rebuilding the state would need access to the full ‘preimage’ state at the point where it was removed, in order to put it back. The restoreto opcode is very simple
> The burden is on the user to restore data properly – but he can use a custom contract to do that incrementally
>
>
> jpitts:
> so in this contract, the user would have the data needed?
>
>
> holiman:
> The user needs to rebuild the same storage, identically, and then he can say ‘use this data, with that code, and restore that inactive contract over yonder’
> For an archived multisig, restore is a one-off. For restoring cryptokitties, it might take months
>
>
> jpitts:
> So basically the user either needs to have this data, or needs to get this data from some place which would hold it (perhaps at a cost). It takes more time because it has to be done in steps, only so much data can be restored in one txn.
> Or is it that RESTORETO on a large enough piece of state would take months to complete?
>
>
> AlexeyAkhunov:
> I think that noone will attempt to RESTORETO for very large contracts, it might be easier to start from scratch. It will probably be used to rescue some multisig wallets or something similar
>
>
> holiman:
> The RESTORETO in itself is trivial, the preceding build-up of data is the potentially heavy operation
> Well, “trivial”, hm, at least pretty simple
> I also think it wouldn’t be used to restore gigantic contracts, but it’s kind of important that it could if there was a need for it
>
>
> jpitts:
> This means that any necessary buildup operations could be performed by a community effort or service which could also store the evicted data.
>
>
> holiman:
> Hm, build-up is sensitive though, dunno if it can be done non-centralized. You wouldn’t want someone putting in bad data
> But yes, people could coordinate
> If you make a restore-bazonk contract where anyone can submit data, and you get some wrong value in, the RESTORETO will fail later on, when storage hash is wrong

---

**jvluso** (2019-01-09):

Not all incentives need to be monetary nor do they need to be tokenized. I think that there are 5 different incentives that can potentially be relied on initially:

### Holder Incentive

Anyone holding a token will lose it if the storage of their balance is forgotten by everyone. With a contract designed with rent in mind, they would only need to store their own personal balance to be able to recover it, and as long as the tools to make it simple exist it would take almost no disc space for an individual holder in their local wallet.

### Sender Incentive

Sending a token only transfers value if is successfully received. Therefore anyone sending tokens will have an incentive to keep track of the balances of the addresses they send tokens to. Much like the holder incentive, the costs will be minimal as long as the tools are available.

### Project Incentive

Anyone running a project with a token will have an incentive to keep track of the states of their contracts to make them more responsive globally to new users. The data will always be able to be recovered as long as one person stores it, but that doesn’t mean it will be able to be restored quickly. Healthy, active projects will distribute copies globally so anyone can have access more quickly, and these will also serve as backups if other methods fail.

### For-Profit Incentives

Several projects are running which profit from providing access to the full Ethereum blockchain, such as Etherscan, Infura, and many major search engines. These projects profit from adds and partnerships and have incentives to continue to run full archival nodes in order to continue profiting from providing these services.

### Non-Profit Incentives

The Ethereum Foundation, the Internet Archive, and potentially other non-profits run and are incentivized to continue running archival nodes in order to execute their mission. These shouldn’t be relied on, but they will ensure that there isn’t a single point of failure.

---

**tjayrush** (2019-01-09):

I really like thinking about the incentives this way. If you look at the first three groups, they each have the same aspect that the individual(s) interested in the use and meaning of the data are responsible to make sure it persists. The fourth one, I think, is the main way the current system works, and the fifth (non-profit) should be more prevalent, but you’re right we can’t really rely on them. To the extent that any solution to the problem increases the likelihood that types 1, 2 and 3 are take advantage of.

Perhaps there’s another group which is poorly described as ‘all the participants in the system because they benefit from the system itself.’  An example: why can’t every light client store some tiny portion of the data? Why can’t full nodes store a tiny (but larger) portion of the data? In other words, try to better capture the incentive everyone has for the whole system to work.

---

**jpitts** (2019-01-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> An example: why can’t every light client store some tiny portion of the data? Why can’t full nodes store a tiny (but larger) portion of the data? In other words, try to better capture the incentive everyone has for the whole system to work.

This reminds me of the [Mustekala project](https://github.com/musteka-la/mustekala/issues/4) from Metamask Labs:

> Features of the Content Routing System ( CRS )
>
>
> Divide the state into slices (avoiding the word shard ), which will be small, redundant, well spaced and useful to each peer.
> Each peer of kitsunet , which, by the way can be not only a browser peer, but a Hub , will maintain a number of these slices , consisting on an organized number of ethereum state and storage trie nodes, and will update their elements as the Block Header of the Canonical Chain goes changing.
> A peer will maintain, ideally, the slice containing relevant data to its operation, plus a couple of discrete slices to ensure redundancy and availability of the whole system.


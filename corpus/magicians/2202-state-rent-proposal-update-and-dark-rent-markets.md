---
source: magicians
topic_id: 2202
title: State Rent proposal update and Dark Rent markets
author: AlexeyAkhunov
date: "2018-12-12"
category: Working Groups > Ethereum 1.x Ring
tags: [storage-rent]
url: https://ethereum-magicians.org/t/state-rent-proposal-update-and-dark-rent-markets/2202
views: 4139
likes: 22
posts_count: 27
---

# State Rent proposal update and Dark Rent markets

First of all, let me summarise what happened in the State Rent working group since [first revision of the state rent proposal](https://ethereum-magicians.org/t/ethereum-state-rent-for-eth-1-x-pre-eip-document/2018) was published.

1. After considering Vitalik’s post on the common classes of contracts, it is very likely that Linear Cross-Contract Storage (LCCS) will be removed from the next revision, in favour of contractions based on CREATE2. An example of such construction for ERC20 tokens can be found here: https://github.com/ledgerwatch/eth_state/tree/master/erc20
2. ERC20 tokens have been identified as an important class of contracts, and now this has been quantified. Contracts that have ERC20 interface occupy around 53% of all contract storage. Their balances (how much each holder owns) occupy around third of all contract storage
3. Following the research of ERC20, the next most important (by footprint in the state) class of contracts will be identified and researched (so far the hunch is that is could either either on-chain order books or non-fungible token contracts). Solutions similar to ERC20 contract above will need to be researched.
4. It has been observed, that because evicted contracts would be recoverable, no eviction notification might be needed (it is present in the first revision of the proposal). For example, if an ERC20 token holder contract gets evicted, the token contract should not reduce the totalSupply, because the evicted holder can be reinstated, so technically, the tokens still exist.
5. Observation mentioned in the previous item weakens the case for the Eviction Priority Queue, described in the Step 2 of the first revision of the proposal. It is likely that the Eviction Priority Queue will be removed from the next revision, and eviction will instead happen when an account is “touched”. The regular updates to the rent balance will still only happen when an account is modified.
6. Adrian S. from PegaSys team is helping by creating Proof Of Concept implementation based on Pantheon.
7. First interesting observation made during the Proof Of Concept implementation, is that some kind of grace period is required to maintain a better user experience. Meaning that when you create a contract without an “endowment”, it should not get evicted at the same block. Current idea is to redirect part of the cost of contract or account creation (and potentially part of SSTORE charge) into the account’s rent balance.
8. Interesting consequence and complication of the point above is that because rent is charged in wei, but account creation and SSTORE is charged in gas, there might be conversation back from gas into wei. Also, if something gets created with a higher gas price, it will have a longer grace period.

Now, to the **Dark Rent markets**!

There were some counter-proposals to rent based on raising the cost of SSTORE a lot, so that it curbs further growth of the state. Some variants include putting up a deposit during any allocation in the state, which gets returned when the allocated space is reclaimed. That could also be viewed as an increased capital cost of allocation.

My argument, that I would like to share and discuss is this. Let’s say we drastically increase the cost of allocation, and this change in cost only applies to the allocations happening AFTER the hard fork (where the change is introduced). When such hard fork is announced, it is likely that the hoarding of the state will begin (get it while it is cheap!). Blocks will probably fill up with the state expanding transactions, and the gas prices will shoot up again. This situation might persist until the hard fork. And then, when the high costs are introduced, those who hoarded the space, will need to return their “investment” and will try to form what I call a **Dark Rent market**. I have not figured out the mechanism, but I think it is technically possible. The difference between this and the State Rent that is being proposed so far, is that the beneficiaries of the Dark rent are the hoarders, and the beneficiaries of the “Light” Rent are all ETH holders collectively (because rent gets burnt).

## Replies

**holiman** (2018-12-12):

I agree with you totally. Any fork where there’s a six month period in advance where users can hoard storage before it hits could be very dangerous.

Regarding grace period, I think that’s a temporary problem, it would be sufficient if something like this was automatically added to the contract constructor by the solc/vyper/whatever compiler; `PAYGAS(this, <reasonable_amount>)` where `reasonable_amount` is either a constructor argument, or a modifier, or a portion of the `balance`. And that it `throws` if there’s not sufficient value.

Anyway, I think it can be solved on layer 2, and is not *required*. I agree it might be nice, but not at the cost of too much extra complexity.

---

**AlexeyAkhunov** (2018-12-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> automatically added to the contract constructor by the solc/vyper/whatever compiler; PAYGAS(this, ) where reasonable_amount is either a constructor argument

You meant `PAYRENT` of course. And this would not extend to contracts created by sending a transaction from an Externally Owned Account to address zero, unless you also specify non-zero value. Because as far as I understand, `PAYRENT` would pay from the `balance` of the account executing the code, not from `tx.origin`. Or would you propose such change in semantics of `PAYRENT` ?

---

**samlavery** (2018-12-12):

Rent applies the ability to control access to space.  If we continue the rent allegory, you must consider the fact that the lock on the door only accepts the deed as a key, so you must give the deed to the alleged renter.  This is a lock that can’t be changed, and you just gave away the house.

So, unless there is a hidden market for a value-add entity that acts as a proxy to blockchain storage, state ownership won’t provide dividends, only a one time opportunity to buy something cheaply and maybe sell it for a higher price later.  I really don’t see this existential threat materializing, because at the end of the day blockchain state is supposed to be secure and it’s key responsibly managed.

**I’m not storing my super important data in some contract 50 other people have the key to.**

---

**AlexeyAkhunov** (2018-12-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samlavery/48/1269_2.png) samlavery:

> I’m not storing my super important data in some contract 50 other people have the key to.

Thanks! I expected this counter-argument!

So, when I said “I have not figured out the mechanics”, I meant that the EVM language is expressive enough to create a system where you would know that you will own the piece of state for certain amount of time, in exchange for certain payment. This could probably be achieved via some clever routing proxy based on `DELEGATECALL` with time-based access controls. I might code it up if there are enough people who do not believe this is possible.

---

**gcolvin** (2018-12-13):

I had suggested that not only could *storing* data get more expensive, but so could *loading* data.  I don’t see that loading creates a dark rent market.  I don’t know just how expensive loading would have to be to raise as much income as rent would.  (Note, I’m not concerned about “fairness” here, just the backwards-compatible operation of the system.)

---

**AlexeyAkhunov** (2018-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> I had suggested that not only could storing data get more expensive, but so could loading data. I don’t see that loading creates a dark rent market

This would only be true if loading the data becomes much more expensive *relative* to *allocating* the space (note that I do distinguish space allocation from storing, because simply changing already allocated values does not increase the size of the state normally). We can count how many `SLOAD` contracts today normally executed relative to how many allocating `SSTORE` (`SLOAD` costs 100x less than allocating `SSTORE` at present). I suspect that the dark rent would still form, unless the cost of allocating `SSTORE` becomes relatively small compared to usual `SLOAD`s. Need more thinking on this.

---

**holiman** (2018-12-13):

Yes, I meant `PAYRENT`. In the case of a EOA creating a contract*, the constructor/initcode would try to execute `PAYRENT`. If it failed – e.g due to no `value` having been provided in the call, there would be no deployment.

*nitpick: not by sending to address zero, which would just burn the money; but by sending *without* a recipient

---

**gcolvin** (2018-12-13):

I don’t see how SLOAD creates dark rent.

---

**gcolvin** (2018-12-13):

The numbers I wondered about on AllCoreDevs remain critical to whether the blockchain can survive.  We know that the blockchain is currently growing about twice as fast as storage is getting cheaper.  Assuming this continues, how much income do we need–from rent, store and load fees–to make up the difference?

---

**AlexeyAkhunov** (2018-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Assuming this continues, how much income do we need–from rent, store and load fees–to make up the difference?

The idea of rent (at least in my understanding) is not to provide income, but to restrict state growth. The limitation of growth becomes tied to the supply of ETH. As the state size approaches the desired maximum, the rent starts climbing sharply, pushing out more and more stuff out of the state. It would be very difficult to resist this process for a long time, because, since rent ETH gets burnt (removed from the supply), and therefore make resistance to rent more and more expensive. We are not targeting any specific income, but rather a certain state size.

EDIT: In other words, current proposal for State Rent, does not require figuring out how expensive the state access should be. It will adaptively become more expensive, as we approach the bounds

---

**gcolvin** (2018-12-13):

And could not the same idea be applied to storing and loading?

---

**gcolvin** (2018-12-13):

> @AlexeyAkhunov
> The idea of rent (at least in my understanding) is not to provide income, but to restrict state growth…  We are not targeting any specific income, but rather a certain state size.

Other than the desire to fit current RAM and SSD sizes, why limit state size?

Or (I’ve lost track) is evicted state available for seamless resurrection, so that it amounts to hierarchical storage?

---

**AlexeyAkhunov** (2018-12-13):

EDIT: inserted another answer here

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> And could not the same idea be applied to storing and loading?

Adaptive pricing of storing and loading? Interesting, let me think about that

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Other than the desire to fit current RAM and SSD sizes, why limit state size?

To keep sync time reasonable for the new nodes joining the network.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Or (I’ve lost track) is evicted state available for seamless resurrection, so that it amounts to hierarchical storage?

Seemless resurrection is only possible if we keep a “hash stump” in the place of evicted contracts. In some ways, yes, it is hierarchical storage.

Scheme based on “hash stump” is obviously prone to some a form of abuse - create lots of contract and leave their hashes in the state.

Therefore, from my point view (and this is Step 6 in the proposal), we might also need true eviction, which does not leave any stumps. To brings such contracts back, one would either need proofs of exclusion (pointers in the proposal), or graveyard tree, which is equivalent to moving the contract into the stateless realm.

---

**jpitts** (2018-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> The idea of rent (at least in my understanding) is not to provide income, but to restrict state growth. The limitation of growth becomes tied to the supply of ETH. As the state size approaches the desired maximum, the rent starts climbing sharply, pushing out more and more stuff out of the state. It would be very difficult to resist this process for a long time, because, since rent ETH gets burnt (removed from the supply), and therefore make resistance to rent more and more expensive. We are not targeting any specific income, but rather a certain state size.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Other than the desire to fit current RAM and SSD sizes, why limit state size?
>
>
> Or (I’ve lost track) is evicted state available for seamless resurrection, so that it amounts to hierarchical storage?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> To keep sync time reasonable for the new nodes joining the network.

This is a key area of discussion I think.

Are there any estimates about how much expansion of network use would create the scenario of reaching maximum state size / escalating rent?

If it does not allow a great amount of additional use, the goals of improving mainnet scalability will again be in contention with state size. Instead of targeting a maximum, is there a way to find a more reasonable economic equilibrium between storage needs and user needs?

State rent climbing sharply, or even the expectation that a limit could be reached, may cause problems for the dapp ecosystem and users who depend on the network daily.

As [@cdetrio](/u/cdetrio) described in the [half-baked 1.x roadmap](https://ethereum-magicians.org/t/ethereum-1-dot-x-a-half-baked-roadmap-for-mainnet-improvements/1995):

> The plan for 1.x encompasses three primary goals:
> (1) mainnet scalability boost by increasing the tx/s throughput, achieved with client optimizations that will enable raising the block gas limit substantially;
> (2) ensure that operating a full node will be sustainable by reducing and capping the disk space requirements with “storage rent”;
> (3) improved developer experience with VM upgrades including EVM 1.5 and Ewasm.

---

**AlexeyAkhunov** (2018-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> Are there any estimates about how much expansion of network use would create the scenario of reaching maximum state size / escalating rent?

No. And the reason is that Ethereum is not simply a monetary protocol. A lot of network uses (like transferring Ether or token to the existing accounts/holders), does not change the state size, and therefore, does not escalate the rent. Only expansive uses will cause the escalation. But there is a whole spectrum of possible uses from non-expansive to very expansive. And even more so, the prevalent uses do and will keep changing. How they have been changing so far needs to be researched and illustrated.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> If it does not allow a great amount of additional use, the goals of improving mainnet scalability will again be in contention with state size. Instead of targeting a maximum, is there a way to find a more reasonable economic equilibrium between storage needs and user needs?

Not necessarily. As I pointed out above, only expansive uses will be in contention with the state size. Also, the old unused state will be removed quicker the higher is the rent. Theoretically, the system is self-healing. And, we cannot cater for all user needs, because some of these needs require too much altruism from the maintainers of the network. One example of such a “need” is profiting from non-uniform gas prices (e.g. Gas Token). Other examples are spam-voting, or year-long ICOs.

Some contract developers make incorrect design choices, because the rent-free model encourages it. Examples - massive DEX contracts, using contract storage to record all trades and withdrawals that ever happened, in the ACTIVE state, MiniMe tokens, storing the entire history of token holding, in the ACTIVE state. Users will need to change their “needs”, I am afraid. They will need to optimise, because we are already optimising quite a lot.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> State rent climbing sharply, or even the expectation that a limit could be reached, may cause problems for the dapp ecosystem and users who depend on the network daily.

See my comment above. We (and I) are doing a lot of work currently to assess the impact of the State rent on the ecosystem, but it is unreasonable to expect that protocol developers will come along and save Ethereum, without dapp ecosystem needing to change their ways. It is everybody’s problem.

---

**gcolvin** (2018-12-13):

A lot of this is being driven by our state growing faster than storage is getting cheaper.  But is not the case for most anything else.  If we do settle down to a rate that is less that the cost rate these problems become much easier to deal with.

---

**jpitts** (2018-12-13):

Thank you for clarifying [@AlexeyAkhunov](/u/alexeyakhunov).

If I am interpreting this correctly in a very broad sense: *the introduction of costs will alter the way dapps make use of the network, while culling older state. It is not so much that there is a limit driven by sync times and node operator costs to worry about, but that this limit is avoided as the introduction of costs incentivizes changes in contract design and usage behavior.*

What concerns me is not that the network participants have to pay a cost, but that the new capacity to operate dapps created by 1.x will again get used up. Your pointing to “only expansive uses” as leading to this condition is reassuring!

Do you think that finding the right pricing of rent to maintain parity with the technical capacity to sync will be challenging?

Cost-based incentives targeting dapp developers (and by extension their users) is not the only lever available; node operators are available to do work.


      ![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 11 Dec 18](https://ethresear.ch/t/common-classes-of-contracts-and-how-they-would-handle-ongoing-storage-maintenance-fees-rent/4441/27?u=jpitts)



    ![image](https://ethereum-magicians.org/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_500x500.png)



###





          Economics






            storage-fee-rent







imho the root of the problem is that non-mining full nodes in ETH are not paid anything. That is why people are not able to buy enough storage and compute.  There are hundreds of millions of dollars per year paid to miners.  imho, one needs to...










Is it worth exploring a possible market mechanism between node operators and contract maintainers? [@tjayrush](/u/tjayrush) and the Data Ring have discussed node operator incentives before.

Or is it expected that an appropriate pricing scheme can be estimated / adjusted by the larger 1.x team.

---

**jpitts** (2018-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> it is unreasonable to expect that protocol developers will come along and save Ethereum

And yes, absolutely, each of us has to do the difficult work and make sacrifices in order to “save Ethereum”! Well, more like save it from being a shared smart phone from the late 1990s ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**AlexeyAkhunov** (2018-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> Do you think that finding the right pricing of rent to maintain parity with the technical capacity to sync will be challenging?

Yes, I think it will be. But I also think that we do not have to get it right from the first attempt. Firstly, the actual rent pricing is not introduced until Step 5 in the proposal (or Step 4 in the next revision). Secondly, it will be easy enough to tweak for pricing formulae once other mechanisms are in place. I am pretty sure we will not get it right on the first attempt, and we will have to observe how the first formulae behaves, and see where its defects are. And then we will do a hard-fork to correct it. That hard fork would be easy to prepare.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> Is it possible to create a market mechanism between node operators and rent charged to contracts so that an appropriate pricing of rent might be found?

Not at the moment. We do not have node operators modelled in any way in the protocol, like for example, miners (via Coinbase field in the blocks), or ETH holders (by their accounts and ether supply). One of my ideas is to launch a Plasma-like network for accounting between the node operators (not necessarily in Ether, but in some other token, and perhaps even allowing negative balances, so that new node operators do not need to have those tokens to start with). If we figure out how to distinguish a genuine accounting network like that from fake ones, we can use it to drive the pricing mechanism. But I do not know how to do that at the moment.

---

**vbuterin** (2018-12-15):

> When such hard fork is announced, it is likely that the hoarding of the state will begin (get it while it is cheap!). Blocks will probably fill up with the state expanding transactions, and the gas prices will shoot up again. This situation might persist until the hard fork. And then, when the high costs are introduced, those who hoarded the space, will need to return their “investment” and will try to form what I call a Dark Rent market . I have not figured out the mechanism, but I think it is technically possible. The difference between this and the State Rent that is being proposed so far, is that the beneficiaries of the Dark rent are the hoarders, and the beneficiaries of the “Light” Rent are all ETH holders collectively (because rent gets burnt).

It’s worth noting that there is a “keyhole solution” to this. For each storage key, store whether or not it has already been accessed after the fork. If the old new-storage-slot cost is `STORAGE_SLOT_OLD` and the new cost is `STORAGE_SLOT_NEW` (eg. 20000 and 60000), then if a storage slot is modified that has not yet been accessed after the fork, charge an additional `STORAGE_SLOT_NEW - STORAGE_SLOT_OLD` gas.

The flags also have a secondary function, which is that they can be used to calculate over time the number of nonempty storage slots in each contract, which is needed to properly charge rent to contracts if that ends up being implemented later.

Alternatively, if we decide that we have access to a “tell me how many storage slots this contract has now” method (this could be done safely for large contracts by storing values in the client’s database that start at zero or whatever the storage slot count is at fast-sync time, then updating them as blocks are processed), then we don’t need per-slot accounting; we can just store a variable “number of storage slots not updated”, and charge an additional `STORAGE_SLOT_NEW - STORAGE_SLOT_OLD` per write until this “debt” is paid off.


*(6 more replies not shown)*

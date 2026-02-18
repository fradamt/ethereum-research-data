---
source: ethresearch
topic_id: 6413
title: De-risking Execution environments by adding value-holding EEs
author: dankrad
date: "2019-11-05"
category: Sharding
tags: []
url: https://ethresear.ch/t/de-risking-execution-environments-by-adding-value-holding-ees/6413
views: 3408
likes: 7
posts_count: 3
---

# De-risking Execution environments by adding value-holding EEs

**TL;DR:** I suggest creating a store of value Execution Environment that is only tasked with ensuring balances of ETH and possibly ERC20/ERC721 tokens can be held on shards. This allows everyone to make their own choices on how to interact with other (potentially more experimental) Execution Environments and thus minimizes the damage they can do. This encourages innovation, as the barrier to trying out a new Execution Environments becomes lower.

# Rationale

[Execution Environments](https://notes.ethereum.org/w1Pn2iMmSTqCmVUTGV4T5A?view) are exciting because they allow upgrading the chain continuously, and potentially allow much more experimentation on top of a stable consensus layer, without requiring hard forks.

However, opening up “layer 1.5” poses some serious questions because it is possible to have low quality execution environments compromising the security of all their users and potentially even the whole chain (if enought value is at stake). The greatest risk comes from early execution environments that “feel” good enough, but later turn out to have significant bugs or drawbacks for the system, for example:

- An Execution Environment that’s a copy of the “official/standard” Execution Environment that does, however, not charge state rent. In the beginning, state storage will be easily available from centralized and decentralized sources, but of course it leads to the same long term problems as in Eth1
- An Execution Environment that seems fine, but turns out to have a subtle bug that lets people print money discovered after 5 years. Note even Bitcoin had an critical inflation bug as recently as 2018
- And of course any other kind of critical bug that an EE might have

Invariably, when such a bug happens, we will wonder if a hard fork could be done in order to fix the problem. It will be very difficult to draw the line which EEs would be rescued, as if we want to encourage experimentation there will be a scale of more and less trustworthy EEs.

However, to improve this and actually allow more innovation, we can add a value-holding EE (VHEE), that would be used to store value (ETH, ERC20 and ERC721). It provides all the functions of these standards it replaces and potentially more [If more token standards evolve in the future, a similar EE could be created for those].

The code for this VHEE would be sufficiently simple that it could be formally verified in its entirety, so that it will not be necessary to hard fork.

# Ownership

In order to be useful, the VHEE needs to have a very flexible notion of ownership. If it only provided value transfers, then it could not be the basis for a true Ethereum ecosystem. Instead, I think the best notion of ownership is something similar to the [“Pay to Script Hash” (P2SH)](https://en.bitcoin.it/wiki/Pay_to_script_hash) known in Bitcoin: An address in the VHEE would be the hash of a script that validates transactions from this address. The effective owner of the funds is thus whoever can create valid inputs for this scripts, which allows for many different kinds of ownership:

- Classical single-sig and multisig wallets
- Ownership by an address in another EE
- Ownership by multiples EE addresses, plus single-sig or multisig direct ownership
- Fallback constructions: An address in an EE that has a daily spending limit, with ultimate ownership by a private key that can revoke the addresses spending privileges at any time

The latter will require that we add a 32 byte state to each address, which can be used to store a state root to any required state by the validation script.

Any ownership by an EE ultimately fully relinquishes trust to that EE. The key is that we can create constructions where we don’t have to fully trust an EE for all our funds, and can thus interact with the EE and use its advantages without the danger of losing all funds.

For the function of some EEs, e.g. optimistic rollup, full control of the funds is central. They will therefore only accept funds that are on an address that is fully controlled by that EE. Using such an EE will always be associated with a higher risk. However, since secure cross-shard transactions will be possible with single-block latency in the new design, most users will probably want to keep most of their funds in their own control.

# Advantages for interaction between EEs

Without a separate VHEE, EEs can only interact (i.e. transfer value) with other EEs that they fully trust, because trusting, for example, an inflationary EE would be catastrophic to the EE accepting funds from this EE if they are not backed. However, creating the VHEE allows one EE to easily call (a contract in) another EE with funds backed by the value EE. So even if the receiving EE has no reason to trust the calling EE, it can still be assured that the funds are now safely in its control and act accordingly.

This also avoids the centralization issue that only EEs containing a large amount of value are interesting to users. Instead, the user might be able to chose the EE for every single transaction they want to execute, and different systems can use different EEs freely as they can still easily interact with most users.

# Eth1 transition

The one big exception to this is of course the Eth1 EE. Since it is not aware of the VHEE, at the start, it will naturally hold all the funds that are currently on the Eth1 chain. It is also likely not possible to make any kind of automated transition for ERC20s, as the contracts can have custom functionality that cannot simply be removed.

For the foreseeable future, we will likely have to accept that the Eth1 EE itself is also a legacy value-holding EE, likely restricted to one shard. To be more flexible with this, we can add a new kind of address to this Eth1 EE that works just like the P2SH-address in the VHEE. That would allow people to hold legacy e.g. ERC20 tokens but still be able to work with it in other Eth2 execution environments.

A more experimental idea would be to have special addresses in Eth1 that represent balances held by the VHEE, that could then also be transferred within shards. However, the problem with this is that special ERC20 contracts might allow decreasing of balances, and thus the VHEE might believe it holds a larger balance than it actually does, which would be catastrophic.

## Replies

**villanuevawill** (2019-11-08):

Previous discussions around this VHEE have labelled it as the “Generic Asset” EE. The discussion started in this response:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png)
    [One fee market EE to rule them all](https://ethresear.ch/t/one-fee-market-ee-to-rule-them-all/5608/7) [Sharded Execution](/c/sharded-execution/35)



> You’re correct that moving the balance of beacon eth between EEs on the beacon chain would not be a synchronous call and requires a crosslink to form and a receipt to absorb from a shard/EE that pegs to it. Even if we assume this proposed design pegs all fees to beacon eth, this would still simplify the proposal by just generating one account balance per EE/slot for the proposer vs. multiple receipts generated for each submitted transaction package on each EE. I also am on board with agreeing on…

[@matt](/u/matt) followed up with a simple example:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/matt/48/4560_2.png)
    [One fee market EE to rule them all](https://ethresear.ch/t/one-fee-market-ee-to-rule-them-all/5608/11) [Sharded Execution](/c/sharded-execution/35)



> There are a couple attributes of a generic asset EE that I think are desirable:
>
> The EE can be rigorously tested and formally verified, allowing anyone to deploy an asset with full confidence that the implementation is secure
> Allows for upgrades to all assets if need be
> Simplifies the transfer of value between EEs
> No need to for approve -> transferFrom as assets are first class
>
> I’m imagining this execution environment looking something like the following (just trying to get the broad strokes o…

In order for this approach to be optimal, there needs to be some concept of synchronous calls between EEs on the same shard. In the threads linked above, we advocated for this and had advocated for it previously on other forums. If there is pushback against synchronous calls between EEs, we may at the very least want to consider supporting synchronous calls for “utility” EEs such as for the Generic Asset or VHEE. An exercise to the reader of identifying other possible “utility” EEs (oracles, interpreters, etc.). Synchronous calls & generic asset EEs were also discussed here: [State Providers, Relayers - Bring Back the Mempool](https://ethresear.ch/t/state-providers-relayers-bring-back-the-mempool/5647)

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> In order to be useful, the VHEE needs to have a very flexible notion of ownership. If it only provided value transfers, then it could not be the basis for a true Ethereum ecosystem. Instead, I think the best notion of ownership is something similar to the “Pay to Script Hash” (P2SH)  known in Bitcoin: An address in the VHEE would be the hash of a script that validates transactions from this address. The effective owner of the funds is thus whoever can create valid inputs for this scripts, which allows for many different kinds of ownership:

Using a P2SH seems like a significant improvement over what we had originally envisioned. It avoids “fragmentation” between EEs. We originally considered a system where an account may have different balances across different EEs (as shown in the 2nd link). Some cons may be slightly increased execution and data for the submitted script. However, it decreases the amount of calls needed from the fragmented approach.

---

**dankrad** (2019-11-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> Previous discussions around this VHEE have labelled it as the “Generic Asset” EE. The discussion started in this response:

Thanks for linking up to this previous discussion, I had indeed missed that the same idea had already emerged there.

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> In order for this approach to be optimal, there needs to be some concept of synchronous calls between EEs on the same shard. In the threads linked above, we advocated for this and had advocated for it previously on other forums.

Yes, I agree with this and I am also strongly in favour of synchronous calls between EEs for this reason. Conversely, I think it can almost be said that without the VHEE, synchronous calls between EEs will be mostly useless: they can only be useful across a small number of EEs that trust each other. That does not seem to be a very good value proposition.

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> Some cons may be slightly increased execution and data for the submitted script. However, it decreases the amount of calls needed from the fragmented approach.

Yes. It would however also be easily possible to support two kinds of addresses, P2SH and direct EE control. A super-modular approach would be to only have direct EE control addresses in the VHEE, and then add a separate “Ownership EE” that implements other kinds of addresses like P2SH.


---
source: magicians
topic_id: 15982
title: "EIP-7251: Increase the MAX_EFFECTIVE_BALANCE"
author: mikeneuder
date: "2023-10-02"
category: EIPs
tags: [consensus-layer]
url: https://ethereum-magicians.org/t/eip-7251-increase-the-max-effective-balance/15982
views: 5238
likes: 36
posts_count: 19
---

# EIP-7251: Increase the MAX_EFFECTIVE_BALANCE

Discussion thread for [Add EIP: Increase the MAX_EFFECTIVE_BALANCE by michaelneuder · Pull Request #7251 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7251)

## Abstract

Increases the constant `MAX_EFFECTIVE_BALANCE`, while keeping the minimum staking balance `32 ETH`. This permits large node operators to consolidate into fewer validators while also allowing solo-stakers to earn compounding rewards and stake in more flexible increments.

## Motivation

As of October 3, 2023, there are currently over 830,000 validators participating in the consensus layer. The size of this set continues to grow due, in part, to the `MAX_EFFECTIVE_BALANCE`, which limits the stake of a single validator to `32 ETH`. This leads to large amounts of “redundant validators”, which are controlled by a single entity, possibly running on the same beacon node, but with distinct BLS signing keys. The limit on the `MAX_EFFECTIVE_BALANCE` is technical debt from the original sharding design, in which subcommittees (not the attesting committee but the committee calculated in `is_aggregator`) needed to be majority honest. As a result, keeping the weights of subcommittee members approximately equal reduced the risk of a single large validator containing too much influence. Under the current design, these subcommittees are only used for attestation aggregation, and thus only have a `1/N` honesty assumption.

With the security model of the protocol no longer dependent on a low value for `MAX_EFFECTIVE_BALANCE`, we propose raising this value while keeping the minimum validator threshold of `32 ETH`. This increase aims to reduce the validator set size, thereby reducing the number of P2P messages over the network, the number of BLS signatures that need to be aggregated each epoch, and the `BeaconState` memory footprint. This change adds value for both small and large validators. Large validators can consolidate to run fewer validators and thus fewer beacon nodes. Small validators now benefit from compounding rewards and the ability to stake in more flexible increments (e.g., the ability to stake `40 ETH` instead of needing to accumulate `64 ETH` to run two validators today).

**Related work** – [eip7251 related work · GitHub](https://gist.github.com/michaelneuder/cafabcfcfcccc45e44ab9d6b1c7b4e1d)

## Replies

**eawosika** (2024-01-12):

I published an in-depth explainer on EIP-7251 for those interested in learning more about the proposal to increase `MAX_EFFECTIVE_BALANCE` from 32 ETH to 2048 ETH and implement in-protocol validator consolidation as a solution to the problem of contracting the Beacon Chain’s validator set: [EIP-7251: Implications of Increasing MaxEB for Validators](https://research.2077.xyz/eip-7251-implications-of-increasing-maxeb-for-validators).

The article explains how EIP-7251 modifies aspects of the consensus protocol like validator activation, deposits, withdrawals, and slashing penalties to enable validator consolidation while preserving the Beacon Chain’s existing security properties. It also addresses regarding increased slashing risk for large validators and (potential) regulatory issues arising from implementing EIP-7251’s auto-compounding rewards feature. All comments/feedback are welcome.

---

**0xalpharush** (2024-01-30):

Is it not necessary to also modify the [ejection balance](https://eth2book.info/capella/part3/config/configuration/#ejection_balance)? If a validator consolidates their stake, they would lose substantially more from e.g. inactivity leak or lost keys before being ejected than retaining discrete, 32 ETH validators. Perhaps it should be proportional to the stake. Or am I missing something?

See also prior [discussions](https://github.com/ethereum/consensus-specs/issues/2883)

---

**dgusakov** (2024-03-22):

Dear authors of the proposal, given the latest news regarding including the EIP proposed into Pectra, I have several questions about the actual implementation.

- How the sweep threshold will be set?

Would it be a validator private key or WC to initiate this value?
- Would this value be changeable during validator operation?
- Can this value be reduced? (effectively acting as a trigger for the partial withdrawal)

The point about the cancelation of the initial slashing does not seem to be researched. When should one expect clarifications?
How will validators consolidation be performed?

Any information available is appreciated!

---

**0xalpharush** (2024-03-28):

I believe this [blog post](https://lighthouse-blog.sigmaprime.io/maxeb-inactivity-leak.html) answers my question

---

**eawosika** (2024-04-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dgusakov/48/11037_2.png) dgusakov:

> How will validators consolidation be performed?

Hi [@dgusakov](/u/dgusakov). I updated the [EIPs For Nerds: EIP-7251](https://ethereum2077.substack.com/p/eip-7251-increase-max-effective-balance) article with [information about the validator consolidation process](https://ethereum2077.substack.com/i/140556227/in-protocol-combination-of-validator-indices). I consulted [this article](https://notes.ethereum.org/@fradamt/maxeb-consolidation) from [@mikeneuder](/u/mikeneuder) and team, so you can check that for answers to some of the other questions you asked.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dgusakov/48/11037_2.png) dgusakov:

> The point about the cancelation of the initial slashing does not seem to be researched. When should one expect clarifications?

The [slashing penalty analysis](https://ethresear.ch/t/slashing-penalty-analysis-eip-7251/16509) has useful information on the cancelation of the initial slashing penalty. I haven’t seen anything concrete on the decision to remove the initial slashing penalty, but it’s part of the [EIP-7251 feature set](https://notes.ethereum.org/@mikeneuder/eip7251-features), so we should have more information about it soon enough. (I should update the EIP-7251 article once the info is available, too.)

---

**etan-status** (2024-04-29):

The proposal has the nice side effect of also increasing the average total value locked by the sync committee, making slashing approach for that more desirable in the future: [EIP-7657: Sync committee slashings](https://eips.ethereum.org/EIPS/eip-7657)

---

**etan-status** (2024-04-29):

Having these not in the CL `ExecutionPayload` makes local verification of EL `block_hash` complicated for the CL.

Generally, all of the new [EIP-7685](https://eips.ethereum.org/EIPS/eip-7685) “general purpose execution layer request” tend to share some of that, but the types 0 and 1 are at least somewhat mappable back to something of which the block hash can be computed by an optimistically syncing CL (while EL is undergoing maintenance, it cannot answer INVALID_BLOCK_HASH so the CL has to do it internally).

I’d advocate to try and replicate the three lists (deposit receipts / withdrawal requests / consolidation requests) into the EL block header as separate fields (instead of EIP-7685), and/or to create a EIP-6493 style StableContainer as their union, given their overlapping nature in common fields.

Currently the EIPs seem a bit… ad-hoc to me, which is alright for the initial devnet, but should be cleaned out later on.

Furthermore, all the extra BeaconState fields break trustminimized Merkle proof verifiers for decentralized staking pools such as RocketPool. It should be considered to combine this with [EIP-7688: Forward compatible consensus data structures](https://github.com/ethereum/EIPs/pull/8439/files).

Have put it on the ACDE agenda as well: [Execution Layer Meeting 187 · Issue #1029 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1029#issuecomment-2083588283)

---

**tkstanczak** (2024-06-26):

Have the following scenarios been taken into account:

1. initiating a validator exit with 32 ETH and then topping it up to 2048 ETH (would it allow me to go around the churn limits?)
2. initiating a validator exit with 32 ETH and then consolidating other validators to the exiting validator (would it allow me to go around the churn limits?)

---

a separate question:

- since on consolidation we are not really exiting the staked ETH, would it be possible to maintain a map of consolidated validators to their new indices for the period that would normally be driven by the churn limit without applying the actual churn limit delay? this would still allow us to slash the ETH (slash the target) while not delaying the consolidation of large operators

---

**etan-status** (2024-09-18):

Should there a be a sequential index on these (across all blocks), to help distinguish between multiple copies of the same exit data?

Deposit requests and withdrawals have a unique index as well.

---

**etan-status** (2024-09-19):

If the idea is for `MAX_CONSOLIDATION_REQUESTS_PER_PAYLOAD` to increase in the future, the Merkleization limit should be put to a theoretic limit (similar to how it is done for blobs). Otherwise, increasing the limit later breaks `hash_tree_root`.

---

**juliaaschmidt** (2024-10-03):

Two questions regarding the EIP-7251:

1. Custom Validator Ceilings:
 There are a lot of blog posts and resources mentioning validators being able to set custom validator ceilings, i.e., custom max EB, e.g., of 64 ETH, after which any excess amount would be automatically swept to the withdrawal credentials as currently done.
 In a breakout room discussion in April 2024 [Hack MD, Ethereum Breakout Room, Decision on Custom Ceilings], I read the feature of custom ceilings was removed from this EIP-7251 due to lack of demand. Is this correct?
 Thus, the incoming Pectra upgrade (EIP-7251) will not allow for custom validator ceilings to sweep from? If I ran a 0x02 validator and I wanted to sweep anything above 64 ETH, I could not and I would have to pay for a partial withdrawal transaction?
2. Initial slashing penalty reduction with EIP-7251:
 Given that the initial slashing penalty currently scales linearly, a validator with an EB of 2048 ETH would get slashed 64 ETH, because initial_slashing_penalty = 1/32 * EB = 1/32 * 2048 ETH = 64 ETH.
 To make consolidation more popular, I found two resources regarding lowering this penalty:

Initial slashing penalty set to a constant value of 1 ETH [Ethereum Notes, Mike Neuder, Slashing Penalty Analysis EIP-7251]
3. Initial slashing penalty still scaling with EB, but a lot smaller than before, 1/128 * EB, i.e., 1/128 * 2048 ETH = 16 ETH [Mike Neuder, Coinbase Webinar, April 2024].

**Which one reflects the latest decision? Are there any other decisions around the other slashing penalties you can update us on?**

Thank you. [@mikeneuder](/u/mikeneuder) [@dapplion](/u/dapplion)

---

**come-maiz** (2025-02-05):

I want to receive a commitment from the big stakers, lido and coinbase, confirming that they will consolidate their validators during the week after the pectra fork.

Are those teams testing the consolidation?

---

**Izzy** (2025-02-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/come-maiz/48/14376_2.png) come-maiz:

> confirming that they will consolidate their validators during the week after the pectra fork.

Tldr:

Lido contributors recognize that consolidations are a critical unlock for the Ethereum network going forward and are working on making them a reality, but it’s going to take a lot of time. For a protocol like Lido, supporting something like this is substantial development work that is ongoing, and decentralized protocols are at a heavy disadvantage to centralized solutions which can do all of this work offchain vs on-chain. Centralized staking providers and delegated stake operators have the easiest time to support consolidations; for them all/most of their complexity is offchain, so they can adapt more quickly. If you want to apply pressure to make consolidations happen more quickly, they’re the optimal target. In turn, their readiness when on-chain protocols have completed the coordinated efforts will mean that consolidation rollouts for on-chain solutions can happen faster. For protocols like Lido, Rocketpool, etc., the process is complex, intricate, and has a lot of moving pieces; please support these on-chain and decentralized solutions with your brainpower and help.

—

I’m a contributor to the Lido DAO. I’d like to bring some illumination to what the process of implementing this kind of stuff looks like, so that one might develop an appreciation for the complexity of requests like this, because I get the feeling things may seem very simple when they’re not.

**Centralized setups are exponentially faster at rolling out new Ethereum features that decentralized ones.**

For simple staking solutions, rolling out things like consolidations will be relatively easy; for others, it’s an immensely complex task.

Consider a spectrum of staking where the simplest staking solution (on the left) is a mono-operator mono-infra set up: it’s just 1 person, running X validators, all on the same machine or general set up of machines, and there’s zero extra complexity compared to vanilla staking from a contracts, oracles, off-chain tooling perspective. Consider that at the other end there is the most-decentralized version of a staking solution: everything (or as many things as possible has to be done on-chain or via oracles), there are a variety of node operators who all interact with the protocol in different ways, interaction with the protocol is some mix of permissioned or permissionless, the protocol has to account for a liquid representation of stake that is underlain by the relevant validators and stake. A solo node operator is on the left end, a small staking business is somewhere to the right of it, a centralized exchange with one operator is probably 1/3 of the way on the spectrum (and moves rightwards as it has to support an LST, or has multiple operators, etc.), and on-chain solutions are scattered between the middle to furthest right end of the spectrum.

Now let’s consider the relative complexity of designing and implementing upgrades to necessary code, tooling, processes, etc. The more centralized and simple the staking solution is, the simpler it is to adopt and implement the new functionality. The more complex and decentralized, the more complicated it becomes. Lido protocol upgrades are months of work, by various teams (contributors, node operators, the community, stakers, auditors, etc).

Just the amount of work required to ensure that protocol economics cannot break, creating new processes, removing technical debt based on previous assumptions etc, all of that is months of design and development. Then you need to test (withdrawals testing for the Lido protocol was 1.5 months of work with client teams, node operators, etc., this was *after* most code was finalized). Then you need to finalize, audit, and deploy.

**Work on consolidations has been ongoing for months, but is substantial and requires changing integral components of the Lido protocol**

If you consider that changes to implementations for 7251 and 7002 were still being made a few months ago, it basically means that most staking solutions haven’t begun directly working on Pectra things until ~Nov. Perhaps it could have started earlier, as the specs didn’t have a lot of substantial changes since after Aug or so, and devnet-3 was the first stable devnet in Sep. But, consider that development is planned ~9-12 months ahead, based on things that are known. At the time, the priorities for contributors working on Lido protocol were upgrading the Staking Router and deploying the Community Staking Module (CSM) to allow for permissionless entry to the protocol, which occurred in November (but were being worked on for the last 1.5 years). Since then, efforts are focused on Pectra (in two pieces: compatibility and support of new features) and CSMv2.

For a protocol like Lido, the work needed just to “patch” the protocol so that it is compatible (*without* adding new features) with a hardfork like Pectra is substantial (you can see details here: [LIP 27: Ensuring Compatibility with Ethereum’s Pectra Upgrade - Proposals - Lido Governance](https://research.lido.fi/t/lip-27-ensuring-compatibility-with-ethereum-s-pectra-upgrade/9444)). Given these kinds of timings and the amount of work required, it’s unfortunately unfeasible for a protocol like Lido to support consolidations in the kind of timeframe that you’ve outlined here.

In tandem with the work being done to “patch” the protocol, work has begun to also prepare for 7002 and 7251 (note that 7002 is much simpler functionality to add than 7251, as 7251 entails a significant overhaul of protocol accounting given assumptions about the effective balances of validators and the relationship between “keys” and “stake”).

For both features, contributors are working towards outlining (in the next few weeks) a proposed way forward to address key aspects of with respect to the Lido protocol, chiefly (this isn’t an exhaust list of considerations):

- Impact of consolidations (risk, rewards, operations) and TWs

A lot of work has already been done here but it needs to be updated (e.g EIP-7251: Effects on Rewards & Risks - Lido Governance)

Designing and implementing changes to on-chain and off-chain code
Analyzing and determining optimal consolidation parameters at the protocol level (what % of protocol should be consolidated, e.g. “how to deal with exits given that partial exits are very costly? Should a % of validators be kept at 32 ETH to allow for finer-grained control of withdrawal amounts? How to reason about bonds for permissionless “fat” validators, etc”)
Determining a timeline for implementation (when can consolidation support be deployed? How should consolidation happen after that?)
Should consolidations be utilized to support stake re-allocation into more robust validation infrastructure (e.g. DVT)?

---

**remyroy** (2025-02-06):

Hi,

I work on tooling, education and support around staking. While these changes are great from a technical point of view, I deplore the lack of strong and clear nomenclature to build on. Take the different kinds of withdrawal crendentials or validators for instance. We will now have type 0 with withdrawal credentials starting with `0x00`, type 1 (`0x01`) and type 2 (`0x02`). There is no clear convention on how we should refer to these validators. Refering to them by their number can be confusing. We came up with some names in our different documents but it hinders our ability to clearly communicate in the ecosystem.

I know there have been legal concerns are the *compounding* term but in the end, we still decided to call `0x02` validators **compounding**.

Here is what are came up with to differentiate them and try to build some conventions:

- Type 0 or 0x00: A regular validator without a withdrawal address. It can also be called a BLS or locked validator. Its balance continues to increase until it is converted to a type 1 validator.
- Type 1 or 0x01: A regular validator with a withdrawal address. Its balance is capped at 32 ETH, after which an automatic partial withdrawal sends any excess balance to the withdrawal address on a rolling window (typically every few days).
- Type 2 or 0x02: A compounding validator with a withdrawal address. Its balance is capped at 2048 ETH, after which an automatic partial withdrawal sends any excess balance to the withdrawal address on a rolling window. The rewards structure and slashing penalties are adjusted to be compounding and roughly equivalent to running multiple regular validators without the associated computational burden for the network or node operator.

Others are coming up with their own names and we muddle through and try to decypher people thoughts when they come asking for support.

---

**remyroy** (2025-02-14):

The official EIP-7251 document poorly defines the slashing penalty reduction.

> # Making the initial slashing penalty negligible
>
>
>
> To encourage consolidation, we could modify the slashing penalties. The biggest hit comes from the initial penalty of 1/32 of the validator’s effective balance. Since this scales linearly on the effective balance, the higher-stake validators directly incur higher risk. By changing the scaling properties, we could make consolidation more attractive.

I had to dig in the specs on [consensus-specs/specs/electra/beacon-chain.md at dev · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/blob/dev/specs/electra/beacon-chain.md#modified-slash_validator) to figure this out.

Were those changes rushed? Was the review process overlooked?

If an EIP changes the protocol, it should be clear about it and avoid using terms like *could*.

---

**come-maiz** (2025-02-19):

Thanks for all the details [@Izzy](/u/izzy). I understand.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/izzy/48/4672_2.png) Izzy:

> Determining a timeline for implementation (when can consolidation support be deployed? How should consolidation happen after that?)

If you prioritize consolidation after the hardfork day, when do you think all your operators can be ready?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/izzy/48/4672_2.png) Izzy:

> Centralized staking providers and delegated stake operators have the easiest time to support consolidations; for them all/most of their complexity is offchain, so they can adapt more quickly. If you want to apply pressure to make consolidations happen more quickly, they’re the optimal target.

Can you name them to call them into this thread and check how their testing is going?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/izzy/48/4672_2.png) Izzy:

> please support these on-chain and decentralized solutions with your brainpower and help.

I’m happy to help testing and reviewing ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) please let us know when there’s a place to start. I’ll read the two links you shared in the lido forum.

---

**come-maiz** (2025-02-19):

Does anybody know how Coinbase is doing their consolidation?

---

**come-maiz** (2025-02-19):

Can the EIP text still be changed?


---
source: magicians
topic_id: 9284
title: "EIP Draft: Multi-chain Governance"
author: Brendan
date: "2022-05-17"
category: EIPs
tags: [governance, chain-agnostic]
url: https://ethereum-magicians.org/t/eip-draft-multi-chain-governance/9284
views: 6622
likes: 40
posts_count: 28
---

# EIP Draft: Multi-chain Governance

# EIP Draft: Mult-chain Governance

This EIP aims to standardize a multi-chain governance system. The specification iterates on the original Compound Governor by separating proposal execution from consensus.

- EIP Draft is available here
- Reference implementation

# Background

Many projects in the space have benefitted from the excellent Compound governance system; whether by using the original contracts, forks, or the compatible OpenZeppelin Governor. Thanks to this inadvertent standardization, we’ve seen impressive projects like Tally that were able to build governance aggregators. Standardization allowed Tally to put their efforts into a deeper feature set rather than integration details.

The next step for many protocols is to go multi-chain.  At the moment this means having a multi-sig act in accordance with a Snapshot vote. While this works, there is no recourse if the multi-sig goes rogue or dormant. We need multi-chain token signalling.

By combining our efforts we can create a multi-chain governance standard that elevates the entire ecosystem, and allows us to leverage common infrastructure.

# Rationale

The above implementation is the best next step for PoolTogether. We have token holders on multiple chains, and we have contracts on multiple chains. We need:

- To allow voting on every chain we are deployed to
- To support state changes on every chain we are deployed to

Additionally, our existing governance system is a fork of the Compound Governor on Ethereum. Our solution must include a migration path for the legacy governance system.

I believe our best bet is to iterate on the Compound Governor to support multiple chains.

# Call to Action

My goal is to find others in the community with similar issues, and develop a standard that we can all move forward with. I’m sure that there are others that need multi-chain governance. Having a common effort will allow all of us to safely and rapidly expand to new chains.

I’ve written a draft EIP and implementation, but the specification is a community effort. I want to hear any and all feedback! In particular:

- Who else wants multi-chain governance?
- Is the spec unclear?
- How can the spec be improved?
- Is there more we should add? Less?

Have a read and let’s start the conversation!

## Replies

**auryn** (2022-05-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> Who else wants multi-chain governance?

Me me me!

We, Gnosis/GnosisGuild, have been working on several version of this for a while as part of [Zodiac](https://github.com/gnosis/zodiac). We see Multichain organizations as one of the really awesome things that Zodiac unlocks with the pattern of decoupling account and control logic. We have a few different iterations of this, solving for slightly different but related of problems in various ways. Starting with our [Reality module](https://github.com/gnosis/zodiac-module-reality) coupled with SafeSnap and  multichain strategies on Snapshot, followed by our [Bridge Module](https://github.com/gnosis/zodiac-module-bridge), and our as-of-yet-unannounced [Gnomad module](https://github.com/gnosis/zodiac-module-gnomad/).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> How can the spec be improved?

I see four distinct problems:

1. How to govern assets on multiple chains?
2. How to account for votes held on different chains?
3. How to make voting cost effective?
4. How to account for votes held in different systems (AMMs, vesting contracts, staking, etc)?

The spec and solution you describe solves nicely for 1-3, assuming there is an acceptable bridge between root an branch. But, as with the current implementations Governor (and, indeed, all on-chain voting that I’m aware of) it does not solve for 4. Meaning that, if vote weight is defined by a liquid token, there is always an opportunity cost for users to hold vote weight compared with using the token productively (often in ways that would be beneficial to the ecosystem, like providing liquidity to an AMM).

To solve for 4, GnosisDAO makes use of our [Reality module](https://github.com/gnosis/zodiac-module-reality) coupled with SafeSnap and multichain strategies on Snapshot, that leverage subgraphs to account for GNO held in many different places (GNO, LGNO, MGNO, SGNO, and GNO held in Uni V2 and V3, and Balancer V1 and V2 on mainnet and Gnosis Chain). Oracle-based-governance like this setup seems like the only viable way to account for this kind of ever-changing range of places that you might want to account for vote weight.

If accounting for votes in more places that just the voters’ wallets is a priority, then I’d suggest that the spec should leverage some oracle-based governance mechanism.

If not, then I think the current spec looks great.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> Is there more we should add? Less?

**IAvatar**

The spec states

> This system is can be easily adapted to support the original Compound Governor Timelock contract, which protocols to swap out the old Governor Alpha for this spec.

However I think it would be more flexible and composable if it were built to support [IAvatar](https://github.com/gnosis/zodiac/blob/master/contracts/interfaces/IAvatar.sol) from Zodiac. Essentially, replacing the timelock with a Gnosis Safe (or some other programmable account that exposes the same interface). You could achieve similar functionality to Timelock by leveraging the [Delay modifier](https://github.com/gnosis/zodiac-modifier-delay), without restricting the DAO’s future flexibility.

At the very least, I’d encourage DAO’s to use their timelocks to control a safe that holds their assets and controls their systems, rather than having the timelock do that directly.

---

**Brendan** (2022-05-18):

Hey Auryn! Appreciate your input here. You’ve raised some good points.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/auryn/48/1044_2.png) auryn:

> How to account for votes held in different systems (AMMs, vesting contracts, staking, etc)?

I 100% agree here. We have the same problem with our DAO, in that people stake their POOL tokens but lose the voting power. We’ve “solved” it by adding all of the derivatives that map 1:1 with POOL to the Snapshot vote. It’s pretty hacky, but the bandaid is holding for now. It’s just signalling to a multisig to vote accordingly with delegated voting power. We need to incorporate Zodiac here ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

Ideally, the spec is minimal enough to allow implementations to measure voting power in their own way. Rather than try to solve the problem of multiple voting tokens, as you described, we could instead make space for people to develop the right solution for them.

# More Modular Voting

Ideally, the spec is minimal enough to allow for different implementations to measure voting power in their own way. Voting can be measured in so many different ways:

- a staking contract that combines multiple token balances
- a veCurve-style lockup token
- COMP-like tokens that use block numbers

Among many others.

COMP-like tokens are particularly interesting: users for many projects on Ethereum have already delegated their voting power. We don’t want them to have to delegate again, so ideally the solution supports these tokens.

Really, the voting interface just answers the abstract question: *how much voting power does this user have for this proposal*. This question can be answered in many different ways. Right now the spec has the voting module use the `start epoch` to measure voting power.  However, to answer the above question properly the module needs the complete proposal info.

I’m thinking the Epoch Voter could be less prescriptive, and instead be abstracted as a mechanism that just returns a users voting power for a proposal:

Instead of:

```auto
interface EpochVoter {
    function votesAtEpoch(address _account, uint32 _epoch) external view returns (uint112);
}
```

We’d have:

```auto
interface Votes {
    function getVotes(address _account, bytes32 proposalHash, uint32 startEpoch, uint64 endTimestamp, bytes calldata branchData, bytes calldata rootData) external view returns (uint112);
}
```

The `branchData` blob and the `rootData` blob could be additional blobs of data that are “notarized” as part of the proposal hash. This would allow implementations to include additional data, such as block numbers, so that votes can be computed properly.

# Execution

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/auryn/48/1044_2.png) auryn:

> However I think it would be more flexible and composable if it were built to support IAvatar from Zodiac.

This is interesting; do you mean the Governor Branch would implement the IAvatar interface? Or that it would know how to speak to one?

Either way, I think implementations could tackle *execution* in different ways. Some may queue the list of calls in a Timelock, others may queue them in a Gnosis Safe. Ideally, the spec is minimal enough that users can tackle this in their own way.

Where the spec *does* need to support different implementation is in the `Call` struct.

Each proposal has an array of calls, each of which is:

```auto
struct Call {
    uint256 chainId;
    address caller;
    address target;
    uint256 value;
    bytes data;
}
```

The `chainId` and `caller` identify *who* should start the call, and the `target`, `value` and `data` identify who should be called.

Looking at the IAvator interface, it seems it additionally can have a “delegation” flag to denote whether to do a delegate call or a regular call. I wonder if we should add this to the Call struct so that it’s fully compatible with IAvator-style execution? Like a `delegateCall` flag or something.

What do you think?

---

**auryn** (2022-05-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> wonder if we should add this to the Call struct so that it’s fully compatible with IAvator-style execution? Like a delegateCall flag or something.
>
>
> What do you think?

Yeah, I think adding this flag would be useful.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> Or that it would know how to speak to one?

Ideally that it would know how to speak to IAvatar. Essentially, when it attempts to execute a transaction, it should call `execTransactionFromModule()` or `execTransactionFromModuleReturnData()`.

This might be to opinionated for the spec and something that is defined in specific implementations. However, the point of Zodiac is to standardize this interface so that we can make all for this rolling easily composable. So building this standard on top of Zodiac could certainly help encourage that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> We’ve “solved” it by adding all of the derivatives that map 1:1 with POOL to the Snapshot vote. It’s pretty hacky, but the bandaid is holding for now. It’s just signalling to a multisig to vote accordingly with delegated voting power. We need to incorporate Zodiac here

Yeah, this is why I tend to think that oracle-based governance is likely to win out. It’s just not viable to track all of these different places POOL might live in an on-chain voting contract. Especially when you factor in multiple chains.

I do think that on-chain governance is still well suited to situations where vote weight is illiquid, consumptive, or very strictly defined.

---

**Brendan** (2022-05-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/auryn/48/1044_2.png) auryn:

> Yeah, this is why I tend to think that oracle-based governance is likely to win out.

One of the reasons I’m excited about the root & branch approach is that it affords us the ability to integrate new voting strategies in the future. While the voting strategy may change, the need to coordinate state updates across chains will remain.

I see this current effort as being the next logical step for us. It won’t be the last, however. This EIP must allow for continued evolution!

---

**auryn** (2022-05-20):

Have you seen Usul, btw? cc [@nginnever](/u/nginnever)

Seems like there are a lot of similar design goals.

https://github.com/SekerDAO/Usul

---

**nginnever** (2022-05-20):

Thanks for tagging me [@auryn](/u/auryn)!!

[@Brendan](/u/brendan) great work, it’s cool to see such a similar protocol to the one I developed. Usul aims for the same targets. Rather than an “EpochVoter” connected to a “Root/Branch” we have “Strategies” connected to “Usul” (which acts as the connecting piece to the Safe and state machine for general proposal state). Strategies simply define the logic for tallying vote weight in whatever abstract way (even non-timeboxed methods like conviction voting). We also pass arbitrary data to the Strategy if Usul gets a valid proposal so that proposals can add unforeseen extra data.

Usul is audited with a Strat that works like Compound using [OpenZeppelin like governor](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/governance), one-member-one-vote, and NFT strats. [It has a working FE](https://sekerdao.com/) in beta that is bridging mainnet and Gnosis Chain, but we have ambitions to use Nomad mentioned by Auryn for access to more chains. Feel free to reach out to me anytime!

---

**Brendan** (2022-05-21):

Hey [@nginnever](/u/nginnever)! Thanks for chiming in.

I had a look at Usul; looks useful as a way to make voting modular. However, it doesn’t appear to capture any multi-chain logic.

I believe the multi-chain aspect of the EIP is distinct, in that it affords these two things:

**1. Token holders can agree on state changes across multiple chains

2. Token holders across multiple L2s and chains can vote on the proposals**

The first is enabled because the proposal hashes encode calls *along with the caller chain id and address*. It’s very similar to the [OZ Governor contract](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/b61faf8368f228a00f0b93e55a7e5ece916b431d/contracts/governance/Governor.sol#L295), but with the caller chain and address it makes the proposal hash cross-chain.

I’m curious to hear both of your takes on how to coordinate state updates across multiple chains, as this is the meat of the proposal.

As for the voting, I’d like to keep it on-chain and leverage blockchains for data availability. I don’t want Oracles to control our protocol, at least not yet. This is why each branch aggregates the votes and bridges them to the root.  There is a branch on each chain, and the root lives on Ethereum (or whichever is serving as the base chain).  That being said, if voting was modular (as in Usul) then each implementation can decide how it wants to Tally the votes.

The EIP might be a little hard to read; I wasn’t stoked on the format but perhaps it just needs more ancillary information. Here is the boiled-down version:

---

### Multi-Chain Governance in a Nutshell

#### 1. A new proposal is recorded in a Governor Root.

The proposal hash includes state change across the chains as an array of Call structs:

```auto
struct Call {
    uint callerChainId
    address caller
    address target
    bytes callData
}

proposalHash = keccak( Call[], ...other proposal data )
```

The above is simplified, of course there is more data.

#### 2. Users vote through Governor Branches

Users vote by presenting the proposal data, which is hashed to tally the users vote.

```auto
function vote(uint support, Call[], ...other proposal data)
```

This is cool, because the *Governor Root doesn’t need to signal the Governor Branch*. Users can discover proposals off-chain, then submit their vote along with the proposal contents. The contents is hashed to determine the proposal hash.

#### 3. Governor Branches submit their aggregate votes to the Governor Root

Once the proposal end time has elapsed, the Governor Branch can submit it’s total votes to the Governor Root:

**Governor Branch** → addVotes → **Governor Root**

```auto
addVotes(uint for, uint abstain, uint against, bytes32 proposalHash)
```

This is the first time that we need a bridge. The Governor Branch will send its votes over a bridge to the Governor Root.  Branches that have votes will send them over.

#### 4. Governor Root Queues Proposals that Pass

After the Governor Root receives all of the votes, the root can determine whether a proposal passes. If a proposal passes, then the Governor Root can queue the proposal hash in the Governor Branches:

**Governor Root** → queue → **Governor Branch**

```auto
queue(bytes32 proposalHash)
```

The `queue` message needs to be bridged, but *only to branches that require execution*. We may not need to bridge to all branches.

#### 5. Proposal is executed on Governor Branches

Once a proposal hash is queued on a branch, anyone can execute it by submitting the full proposal data:

```auto
execute(Call[], ...other proposal data)
```

The data will be hashed, and if the proposal has been queued it will be executed.

### Summary

In this way, we can easily coordinate state changes across multiple-chains with minimal bridging. Multi-chain proposals are efficiently encapsulated in hashes, and we minimize the number of bridged messages.  The only bridged messages are:

**Governor Branch** → addVotes → **Governor Root**

**Governor Root** → queueProposal → **Governor Branch**

---

I hope this illustrates the concept better; the EIP contains a lot of information and needs to be cleaned up. It might even need to be broken out into several pieces!

Does this make things clearer [@nginnever](/u/nginnever) and [@auryn](/u/auryn)? I do believe the multi-chain aspect is distinct. I’m curious to hear your thoughts on it as well as how you’d envision tackling it.

---

**nginnever** (2022-05-22):

Usul was built to be another tool in a set of composable tools. With the SekerDAO app we targeted only bridging two chains for scalability purposes (vote on the cheaper chain and bridge the execution to the more expensive one where you need state updates). We also only targeted the Gnosis Chain because there wasn’t a canonical solution for bridging every chain that would make it easy, which is were Nomad comes in.

…But composing Zodiac modules together I believe we can achieve the multichain governance you are suggesting.

I *think* it requires just adding one more module to our ecosystem (or voting strategy contract), something like a simple “aggregator” module that just waits for each chain to signal consensus that a FOR vote has passed. After collecting all of the chains approval it would then unlock a multisend transaction to various bridge contracts to engage the receiving endpoints with calldata to enact state changes for each chain.

1. Deploy Gnosis Safes on every chain that will participate in governance.
2. Deploy Usul modules on every chain that needs to vote. Give this module full control of the safe.
3. Deploy Bridge Module endpoints on every chain that needs to receive the outcome of a cross chain vote. Give this module full access to the safe. The bridge sender must be the aggregator module to avoid rogue proposals from injecting calls into the safes.
4. Proposals are submitted to each chain to send a bridge tx to one gnosis safe that simply says (yes, consensus was reached from the voters on this chain to signal a FOR vote for proposal hash 0x…).
5. These transactions hit the aggregator contract, and once all of the configured chains have signaled approval to the aggregator contract, it will then unlock the multisend transaction to bridge back to every chain that needs state updates.
6. The bridged data could just be a message stating that an aggregate proposal is passed in Usul, where each call can then be made, or the actual data just sent directly to the Safe.

I would need to spend a bit more time thinking if I missed anything (particularly with the trust assumptions introduced with multichain governance) or if this can be done without introducing an aggregator module (I’m pretty sure this can also be done with Usul voting strategy that acts as the aggregator actually, which would just be one simple contract that needs to be audited).

Some suggestions for your method…

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> #### 2. Users vote through Governor Branches
>
>
>
> Users vote by presenting the proposal data, which is hashed to tally the users vote.
>
>
>
> ```auto
> function vote(uint support, Call[], ...other proposal data)
> ```
>
>
>
> This is cool, because the Governor Root doesn’t need to signal the Governor Branch. Users can discover proposals off-chain, then submit their vote along with the proposal contents. The contents is hashed to determine the proposal hash.

This seems to require every voter to supply the proposal data for every vote, I wonder if there is a cost tradeoff of having every voter do the hashing calculation vs having one proposer store the data on-chain and create an identifier that everyone votes with.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> addVotes(uint for, uint abstain, uint against, bytes32 proposalHash)

Should be able to set the quorum correctly on each chain and simply send a “signal” to the Root by calling `chainPassedProposal()` and save some data. This might actually be necessary if you use OZ or Comp code directly since they read the totalSupply() from the token contract, which might be only the bridged token and not the actual totalSupply across all chains.

Thanks again for taking the time to think about how this can be done in multiple ways, ideally we could find a standard that doesn’t require using one implementation, which is one of the main motivations for Zodiac. You don’t need to use Usul as the governance module and could use any set of contracts that interface with an “Avatar”.

---

**Brendan** (2022-05-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nginnever/48/4143_2.png) nginnever:

> ideally we could find a standard that doesn’t require using one implementation,

I completely agree! The need for a standard is what is driving this proposal. A common spec will encourage an ecosystem of governance interfaces, analytics, aggregators, and whatever else people can dream up. [Tally](https://www.tally.xyz/) and other DAO aggregators will be able to scale with us into our multi-chain future. Let’s keep this conversation going.

Based on what you said, it sounds like the Gnosis Safe has a lot of modules that will make implementing the spec pretty straightforward.  Having many reusable parts allows developers to move much more quickly. However: what is the “whole” that these parts form? If we view it like a vehicle, then we see that Gnosis has a great engine and nice wheels but what is the driving experience? How are the engine and wheels controlled? This is what we need to determine. This is the “aggregator” module you mention.

# Finding the Abstraction

The specification needs to capture the right level of abstraction; it needs to be narrow in scope such that it is useful but also composable.

To me there are two important features to multi-chain governance:

**1. Proposals include state changes across multiple chains

2. Token holders across multiple L2s and chains can vote on the proposals**

Given that we don’t fully agree on how to tackle voting, let’s put voting to the side for the moment and focus on the first point: **how can we standardize multi-chain proposals**. This is where we have the most commonality right now. No matter how you vote, code needs to be agreed upon and executed on multiple chains.

# Multi-Chain Proposals

At a bare minimum we should have a common interface to introspect multi-chain state change proposals. A user of the spec must be able to:

1. Easily find proposals
2. View the state changes
3. Know whether a proposal has been executed

All signalling should be done through events and on-chain data (this is an EIP after all).

## Find Proposals

Proposal data should not be stored on-chain. There could be many state changes in a proposal, which would make storage prohibitively expensive. Instead, we can identify proposals using a content hash: the contents of the proposal is hashed to form a unique and verifiable identifier. Let’s call this identifier the `proposal hash`.

Depending on the implementation, proposal data includes state change data as well as consensus data. However, being a multi-chain system, execution and consensus may occur on different chains. We should separate that data. Let’s introduce another content hash for the state change data called the `state change hash`.

We now have:

```auto
stateChangeHash = hash( stateChangeData )
proposalHash = hash( stateChangeHash, consensusData )
```

To make this data available off-chain we’re going to need two events.

Let’s emit the first event from a contract we will call the `StateChangeOrigin`:

```solidity
interface StateChangeOrigin {
    event StateChangeCreated( stateChangeHash, ...stateChangeData );
}
```

This event includes the computed `stateChangeHash` as an indexed topic to make proposal discovery easier.

The second event captures the consensus data. By its nature, consensus must occur in a single place, so let’s call the second contract the `ConsensusRoot`

```solidity
interface ConsensusRoot {
    event ProposalCreated( proposalHash, stateChangeHash, ...consensusData);
}
```

The ProposalCreated event emits the proposal hash as an indexed topic as well.

By listening for events from a group of `StateChangeOrigin` and `ConsensusRoot` contracts a viewer will be able to put together the whole picture of the proposal. These contracts may or may not live on the same chain, or they could even be the same contract!

## View State Changes

Users must be able to see what the state changes are. We need to standardize the data format for multi-chain calls. What do we need to know for a call? At a minimum, we need to know:

- The chainId on which the call is occurring
- The caller who is the one doing the calling
- The target of the call
- The calldata for the call

We can define the “state change data” as being an array of structs of the above:

```solidity
struct Call {
    uint chainId;
    address caller;
    address target;
    bytes callData;
}

interface StateChangeOrigin {
    event StateChangeCreated( bytes32 indexed stateChangeHash, Call[] calls );
}
```

Now users can see what changes a proposal is going to make. For now, let’s hand-wave the details of `stateChangeHash = hash(calls)`.

## Know the Proposal State

Users need to know whether a proposal was successfully executed. This data should be available both on-chain and off-chain through events.

Given that a proposal can be executed on multiple chains, we’ll need to track execution per caller.

The `Caller` contract is the one that executes the proposal, so it must provide an event and on-chain accessor:

```solidity
interface Caller {
    event Executed(bytes32 indexed proposalHash);

    function wasExecuted(bytes32 proposalHash) external view returns (bool);
}
```

The `Executed` event must be emitted when the execution occurs.  The `wasExecuted` function allows on-chain contracts to determine if a proposal passed, and behave accordingly.

# Summary

Let’s bring the above all together:

```solidity
struct Call {
    uint chainId;
    address caller;
    address target;
    bytes callData;
}

interface StateChangeOrigin {
    event StateChangeCreated(
        bytes32 indexed stateChangeHash,
        Call[] calls
    );
}

interface ConsensusRoot {
    event ProposalCreated(
        bytes32 indexed proposalHash,
        bytes32 indexed stateChangeHash,
        bytes consensusData
    );
}

interface Caller {
    event Executed(bytes32 indexed proposalHash);

    function wasExecuted(bytes32 proposalHash) external view returns (bool);
}

```

These interfaces will allow a third party to:

- Find proposals (via indexing)
- View the state changes (by interpreting encoded event data)
- Know whether a proposal has been executed (by looking at multi-chain callers)

**Open Questions**

- Is this enough for a multi-chain proposal MVP? Does this spec need more? Is it too much?
- what details are missing?

Add value and delegateCall on the Call struct?
- Add bytes extraData on the event StateChangeOrigin for extensibility?

Is this spec flexible enough to support multiple voting EIPs?

### Note on Gas

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nginnever/48/4143_2.png) nginnever:

> I wonder if there is a cost tradeoff of having every voter do the hashing calculation vs having one proposer store the data on-chain and create an identifier that everyone votes with

You can ballpark the gas usage using [evm.codes](https://www.evm.codes/). The most expensive part will be the hashing of calldata, so let’s calculate the hashing costs:

- Estimate 6 words per Call struct
- Estimate 6 calls per Proposal
- Estimate each proposal has 4 words of consensus data

Total bytes per proposal: (6*6+4) * 32 = 1280

Plug that into the `SHA3` opcode and it costs 393 gas (worst-case). A cold SLOAD is 2100, so it’s cheaper than loading from storage.

# Summary

This pared-down version of the EIP keeps the proposal standard, but is flexible enough for implementations to tackle consensus their own way.

What do you all think of this? Is this more narrow scope a better starting point?

---

**mintcloud** (2022-05-24):

Thank you [@Brendan](/u/brendan) for kicking this off, and Auryn and Nathan for your contribution thus far.

Just wanted to signal our interest from 0x protocol on the topic. We have deployed the protocol on [7 different EVM-compatible blockchains](https://blog.0x.org/0x-ecosystem-update-18/) and are planning to setup an onchain binding “embassies+central government” governance system, controlled by ZRX holders.

We implemented a [community treasury with onchain binding voting on L1](https://www.0x.org/zrx/treasury), and that might evolve into ‘local treasuries’ too.

The `GovernorBranch`/ `GovernorRoot` pattern seems promising at a first glance. Intuitively, I tend to prefer leaving voting strategies and voting power calcs to each protocol/system, and land on standard for cross-chain state updates.

We’ll be watching this discussion closely! ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

---

**rafso** (2022-05-31):

Hi, Raf from Tally here. I’ve was talking about this spec with Brendan offline a few weeks ago. I’m finally catching up on this thread. I like the idea of splitting the two problems – cross-chain voting and cross-chain execution – into separate specs. Seems easier to agree on the path forward and to solve that way.

Lots of DAOs are looking at how to solve this problem. I’ve also been following [the discussions of how Uniswap DAO plans to solve it](https://gov.uniswap.org/t/proposed-template-for-future-cross-chain-deployment-proposals/16611).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> Proposal data should not be stored on-chain. There could be many state changes in a proposal, which would make storage prohibitively expensive. Instead, we can identify proposals using a content hash: the contents of the proposal is hashed to form a unique and verifiable identifier. Let’s call this identifier the proposal hash.

In our experience at Tally, storing stuff on-chain is expensive, but it’s a huge benefit for interoperability and UX. Maybe a happy medium would be to include optional fields for URI that point to the un-hashed data. The URLs can obviously become unavailable, but that at least makes UX easier when everyone is cooperating. It also makes it more obvious when someone isn’t cooperating by withholding data.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> The ProposalCreated event emits the proposal hash as an indexed topic as well.

Naming this event `ProposalCreated` causes a collision with the  [OZ Governor event of the same name](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/4942bd19e2da9e416e46da74356506d85950a491/contracts/governance/IGovernor.sol#L28-L38). Do we want to reuse the name? That makes it impossible to create a contract that implements both the OZ Governor interface and this cross-chain execution interface. I’d suggest using a different name.

Alternatively, we could overload the existing `ProposalCreated` event by putting the body of cross-chain event in the `description`. That’s a pretty ugly hack, but it would give us backwards compatibility without needing to upgrade all the existing contracts.

I’d also suggest including canonical start and end times for the voting period in this event. Otherwise, how will the off-chain votes know when to start and end the vote?  We should use wall clock times, not block heights, because we can’t assume that other chains know the block heights on the root chain.

Even if we do have start and end times, voters can still do timing attacks by moving tokens between chains because the vote won’t start at exactly the same time on all chains. I’m not sure how big of a deal that is. I’m ignoring it for now.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> The Executed event must be emitted when the execution occurs. The wasExecuted function allows on-chain contracts to determine if a proposal passed, and behave accordingly.

What’s the correct behavior for a proposal that passed, but whose execution reverts due to an error? We could only allow execution once, but the error may go away in the future. I would suggest letting anyone keep trying to execute the proposal, but only for X amount of time. I don’t think we need to change the interface to support that possible requirement. It’s internal to the execution logic on each chain.

Overall, I like the direction that this spec is going. I’ll post more thoughts as I come up with them.

---

**Brendan** (2022-06-01):

# Proposal Data URI

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rafso/48/6204_2.png) rafso:

> In our experience at Tally, storing stuff on-chain is expensive, but it’s a huge benefit for interoperability and UX. Maybe a happy medium would be to include optional fields for URI that point to the un-hashed data.

This is interesting to me! My assumption was that including the events would be enough, as the proposal data would be emitted. Do you feel that events are insufficient or impractical?

We’ve also found that events aren’t the most convenient, as they require an archive node to access. We’ve been using subgraphs for data, but the Graph network doesn’t support all chains.

If we added a `proposalDataUri` as you suggested, then the proposal data could be sourced from anywhere. For example, the data could be stored on:

- IPFS
- Web 2 host
- The Governor Branch contract itself (proposal origin)
- A separate chain used for data availability

To support all of the above, it makes me think:

- The spec will need to define a JSON schema (just like ERC721 metadata)
- We could additionally specify that the uri can be application/octet-stream with the standard ABI encoded data; that way contracts can store the data themselves (if gas is cheap  )
- Is it possible to use a separate chain for data availability? Can a URI point to a function on a chain?

I like the proposal data URI idea! Having a JSON schema and abi-encoded `application/octet-stream` would go a long way in terms of flexibility (and we can always still have the event).

# Timestamps

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rafso/48/6204_2.png) rafso:

> I’d also suggest including canonical start and end times for the voting period in this event. Otherwise, how will the off-chain votes know when to start and end the vote?

This is an interesting one…in the voting spec above I outline how “epochs” can prevent double voting (h/t to [@frangio](/u/frangio) for the idea!). The “start epoch” of the vote would be recorded; not the wall clock start time.

It seems to me that start and end times are actually a property of voting, so I hesitate them to include them in the proposal spec. However, perhaps we can broaden the meaning: the “start time” could instead the more abstract “created at” timestamp of the proposal. It would be useful for proposal display, regardless of voting. The ‘end time’ of a proposal may not be applicable to all implementations. Thoughts?

---

[@auryn](/u/auryn) I’ve heard that the Gnosis Chain is going to be used as a kind of “governance chain”. Is there substance to that? What do you think of the data availability aspect?

---

**anna-carroll** (2022-06-01):

Hey folks!! I’ve been following this conversation closely and have so much to chime in!!

For those who don’t know me, I’m the Protocol Lead at Nomad, and have been working closely with [@auryn](/u/auryn) and Nathan on the aforementioned Zodiac module.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> Who else wants multi-chain governance?

Me me me ![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=15)

## Execution vs. Voting

First things first: I strongly agree with the idea of separating concerns between proposal execution and voting. These are two different design spaces which both need to be solved for. I recommend we start with cross-chain proposal execution.

### Reasoning

1. For a cross-chain protocol, voting doesn’t necessarily need to be cross-chain, whereas proposal execution almost certainly does. A lot of large existing DAOs have well-working solutions for voting on a single chain (e.g. GovernorBravo), which they may not want to migrate from any time soon; many of these same DAOs have very broken experiences for cross-chain proposal execution, which is becoming more pressing to solve.
2. Multichain voting is a much larger design space, whereas cross-chain proposal execution is a tighter design space to start with. I have participated in a lot of discussions with teams about multichain voting already, and the needs can vary widely per-team. Over time I am definitely excited to participate in how this design space evolves!

## GovernanceRouter.sol

Next things next: I was glad to see some of the design conclusions [@Brendan](/u/brendan) came to in his post about Multi-Chain Proposals, as many of them tightly mirror the Nomad `GovernanceRouter.sol` [contract](https://github.com/nomad-xyz/monorepo/blob/main/packages/contracts-core/contracts/governance/GovernanceRouter.sol), a contract for cross-chain proposal execution which I designed nearly over a year ago!!  (Anyone who checks it out, feel free to provide feedback!)

### Similarities

**(1)** A struct of calls to be passed across chains:

```auto
    struct Call {
        bytes32 to;
        bytes data;
    }
```

Two questions about the proposed struct:

- address caller: why include this field? message passing protocols (that I know of) include the address of the caller on the origin chain so that it can be authenticated. in my mind it would be an attack vector for this to be configurable by end users, unless I misunderstand
- chainId: I felt it was best to batch an array of Calls on a per-chain basis. the array of Calls for each destination chain is hashed and sent to the destination chain, to be executed in one atomic batch. in that world, a chainId wouldn’t need to be part of individual Call struct, it’s associated with an array of Calls. I think that atomic execution of all of the Calls on one chain is quite desirable to maintain

---

**(2)** An event emitted when a state change is executed, mapping to `event Executed` above:

```auto
event BatchExecuted(bytes32 indexed batchHash);
```

---

**(3)** A queryable function `inboundCallBatches` which tells the caller the status of a batch, similar to the `function wasExecuted` above.

```auto
    // call hash -> call status
    mapping(bytes32 => BatchStatus) public inboundCallBatches;

    // The status of a batch of governance calls
   enum BatchStatus {
       Unknown,    // 0 - batch not yet delivered. may not exist.
       Pending,    // 1 - batch delivered, but not executed
       Complete    // 2 - batch executed
   }
```

**Note:** in my experience executing cross-chain proposals, returning the status **`enum`** - not a **`bool`** - to tell the status of a Batch has been *very* helpful in practice, such that off-chain actors know when it is possible to execute a batch. See this [script](https://github.com/nomad-xyz/monorepo/blob/b64a6c5abcc84a93b81d4d68698c3633763a36ed/packages/sdk-govern/scripts/executeRemoteDomains.ts#L37), which checks if a batch has been received, then executes it.

### Differences

**(1)** I opted not to emit a similar event to `StateChangeCreated`, because Nomad emits an event for every message sent, but I would be super open to revisit that decision

---

**(2)** Emits this event when the cross-chain containing the state change is delivered:

```auto
    event BatchReceived(bytes32 indexed batchHash);
```

Again, it’s helpful to know that additional intermediary step for a Batch, before the Batch is Executed.

---

**rafso** (2022-06-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> This is interesting to me! My assumption was that including the events would be enough, as the proposal data would be emitted. Do you feel that events are insufficient or impractical?

Ah good point, thanks for clarifying. I agree that event logs are sufficient. I didn’t realize that your proposed `StateChangeCreated` and `ProposalCreated` include plaintext data before hashing. That should be enough for anyone to reconstruct the proposal.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> It seems to me that start and end times are actually a property of voting, so I hesitate them to include them in the proposal spec. However, perhaps we can broaden the meaning: the “start time” could instead the more abstract “created at” timestamp of the proposal. It would be useful for proposal display, regardless of voting. The ‘end time’ of a proposal may not be applicable to all implementations.

Yes, I agree that we want to separate cross-chain execution from cross-chain voting. The cross-chain voting spec should have its own event with whatever metadata the branches need. We can figure out the right fields, such as `epoch` vs `created_at`, when we implement or create a spec for voting.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anna-carroll/48/6212_2.png) anna-carroll:

> Next things next: I was glad to see some of the design conclusions @Brendan came to in his post about Multi-Chain Proposals, as many of them tightly mirror the Nomad GovernanceRouter.sol

Awesome. Thanks for sharing! Seeing your working implementation helps me a lot to understand the details, especially around keeping track of branch execution with `BatchStatus` and `BatchReceived`. That bookkeeping state seems super-useful.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anna-carroll/48/6212_2.png) anna-carroll:

> (1) I opted not to emit a similar event to StateChangeCreated, because Nomad emits an event for every message sent, but I would be super open to revisit that decision

a `StateChangeCreated` state might be helpful to abstract away the bridge. Indexers might not want to have to keep track of events on bridges, and different bridges might not even emit the same events.

---

**anna-carroll** (2022-06-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rafso/48/6204_2.png) rafso:

> Seeing your working implementation helps me a lot to understand the details

I’m so glad to hear that!! This implementation has been putting in work, as Nomad executes cross-chain proposals with it regularly (most commonly to deploy & enroll a new chain).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rafso/48/6204_2.png) rafso:

> a StateChangeCreated state might be helpful to abstract away the bridge. Indexers might not want to have to keep track of events on bridges, and different bridges might not even emit the same events.

I totally agree it would be very nice to have an event indexers could pick up that indicates initiating cross-chain call execution ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Do you think that event should be emitted once for each destination chain, or once with a bundle of every destination chain? Personally, I’d say once per destination. Perhaps a higher-level Proposal event could include a bundle.

As a side note, I’d propose exploring some more general naming:

```auto
    event CrossChainCall(uint32 destination, bytes32 callHash, Call[] calls);
```

---

**Brendan** (2022-06-02):

Hey Anna! Nice to meet you. I did a deep-dive into Optics before Nomad emerged. I like the tech.

You’ve raised a lot of great points, in particular:

- Batch semantics. Group calls by caller
- Batch status: a function on the executor lets us know the status of the batch

Both of these make a ton of sense to me.

However, you mention that you don’t see a need for the `address caller`. After looking at the GovernanceRouter code, I think I see something very interesting!

# Imperative vs Declarative

Here is what I’m looking at in particular:

```solidity
function executeGovernanceActions(
    GovernanceMessage.Call[] calldata _localCalls,
    uint32[] calldata _domains,
    GovernanceMessage.Call[][] calldata _remoteCalls
) external onlyGovernorOrRecoveryManager;
```

While you haven’t explicitly declared the `caller` and the `chainId` for the array of calls, they are implicitly encoded in the ‘domains’ array and by who is listening on the other end. IIRC the `domain` is a xapp connection, so you are defining the receiver of each remote call batch. (afaik there is no multicasting yet?)

In a sense, Governance Router proposals are *imperative* in that the proposal is telling the router *how* to execute the proposal. A third party looking at the proposal would have to know the Nomad transport semantics to know who is calling who on what chain.

By including the `caller` and `chainId`, the cross-chain proposal becomes declarative; it doesn’t care how the bridging is accomplished, but it knows what the outcome will be. Contract X on chain Y will call function Z. If there are multiple batch executors on one chain, then each knows what it must do.

Is there a way we can marry these two? How can we keep the proposals transport-layer agnostic?

---

**anna-carroll** (2022-06-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> By including the caller and chainId, the cross-chain proposal becomes declarative; it doesn’t care how the bridging is accomplished, but it knows what the outcome will be. Contract X on chain Y will call function Z. If there are multiple batch executors on one chain, then each knows what it must do.
>
>
> Is there a way we can marry these two? How can we keep the proposals transport-layer agnostic?

Ahh I see what you mean now. `address caller` was meant to indicate the contract on the destination chain that will *receive the cross-chain message* which *contains* the calls, and then execute the calls. So, there is value in including the address of the `caller` on the event emitted, so an indexer can “know” where to look for these events - however, a couple things to note about the `caller` role.

## Specialized Caller

Regardless of the transport layer being used -  the `caller` must be a special contract, which implements a function to make it capable of receiving cross-chain messages from that transport layer. In Nomad, that function is called `handle`; in other transport layers, there are other names (there has been no cross-chain message passing standard, yet!)

The `caller` does the following:

1. handle incoming cross-chain messages from some transport layer
2. perform access validation on the message (e.g. check it’s coming from a permitted source)
3. decode the Calls within the message
4. execute the Calls

To perform this role to the fullest, the `caller` would be the contract in control of permissioned roles on a protocol. In most cases, those permissions tend to aggregate to a single contract. For example: `GovernorBravo` usually holds all the permissions for a given protocol, and often custodies treasury funds too.

## Multiple Callers?

I’d estimate that in the vast majority of cases, that, because

1. the caller must be a special contract
2. the caller holds privileged permissions on the protocol

This would mean that the vast majority of DAOs would opt for one `caller` contract per chain.

That being said, doesn’t really matter - we can emit the following event once per `(destination, caller)` tuple:

```auto
    event CrossChainCall(uint32 destination, address caller, bytes32 callHash, Call[] calls);
```

Knowing that, usually, there will be just one per chain.

(Incidentally - at Nomad, we think of the `(chainId, address)` tuple as an address’ “identifier” in the cross-chain world. Just an address is no longer sufficient.)

## Naming

Personally, to me the name `caller` is a bit confusing because there are so many potential `callers` in the process.

- the EOA that sends the transaction that initiates the cross-chain call on the sending chain
- the contract that actually calls the transport layer to initiate the cross-chain call on the sending chain
- the EOA that sends the transaction that executes the calls on the destination chain
- the contract that actually executes the calls on the destination chain

All of these could be fairly called a `caller`. What do y’all think?

---

**Brendan** (2022-06-03):

I agree that `caller` is too generic, and that it will need specialized logic in order to receive an authorized batch of calls. Being less abstract will make the spec much clearer. Call it Branch? Remote? Open to ideas.

It feels like the conversation is starting to gain focus- so I want to take a step back and reframe what we’re talking about.

# Recap

The proposal lifecycle can be boiled down into three steps:

1. Proposal is created
2. Proposal is voted on
3. If passed, proposal is executed

This thread has touched on all three of these steps, but we have the most common ground in the third: proposal execution. Most protocols will need to coordinate and execute state changes across multiple chains. That’s a given.

In fact, this is exactly what the Toby has written up in the [Uniswap Universal Governance Module](https://gov.uniswap.org/t/rfc-uniswap-universal-governance-module/16829). They want to remote control contracts.

The Uniswap RFC says that they are evaluating different vendors. In all likelihood these vendors have different interfaces: the resulting module will be proprietary.

It seems like we all agree that cross-chain execution is the biggest and most common pain point: so how about we start there? I would love to be able to swap different bridges: for example start with a native bridge then swap out for Nomad or another solution (or straight to Nomad ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=15) )

You used a word in the Governance Router that I thought captured it well: remote. We’re talking about “Remote Execution”.

# Standard for Remote Execution

It seems that we all want a standard for **Remote Execution**. This is really ground zero for multi-chain system: executing cross-chain calls. The standard should be comprehensive enough to be useful, but small enough to be easy to implement.

What should the goals of the standard be? Perhaps:

- Make it easy to trace protocol execution across multiple chains, regardless of transport layer.
- Make it easy to swap out transport layer

Tracing would be easy to do, as we really just need to standardize events, like we’ve been talking about.

Being able to swap out the remote execution puts more constraints on the implementation, but would be incredibly useful.

Using your language, imagine we had two contracts:

- Router: send execution batches to remotes
- Remote: receives batches and executes

The spec could define that:

- remotes are keyed on (chainid, address)
- events are emitted to help with tracing
- a Router function sends batches
- a Remote function checks batch status

Thoughts? I feel like we’re starting to gain some clarity here!

---

**TimDaub** (2022-06-04):

Hey, not sure if this has come up yet, but have you considered using ChainAgnostic’s standards track? [GitHub - ChainAgnostic/CAIPs: Chain Agnostic Improvement Proposals](https://github.com/ChainAgnostic/CAIPs)

---

**Brendan** (2022-06-05):

I didn’t know about CAIPs! But what we’re talking about it pretty EVM-specific; I think it fits well here.


*(7 more replies not shown)*

---
source: magicians
topic_id: 3035
title: Ethereum Object Capabilities
author: danfinlay
date: "2019-03-29"
category: Uncategorized
tags: [wallet, security]
url: https://ethereum-magicians.org/t/ethereum-object-capabilities/3035
views: 5785
likes: 12
posts_count: 7
---

# Ethereum Object Capabilities

Reposted from [here](https://hackmd.io/vlApCSi_QiOmArb9Wpkj3A?both).

As I just presented on the GitCoin live stream.

# Ethereum Object Capabilities

Here I will make the case that **Object Capabilities** (ocaps) represent a key atomic unit of composition, security, and versatile scalability (both computational and social) that is urgently missing from the Ethereum ecosystem, and merits a coordinated effort on behalf of Ethereum developers (and most blockchain developers).

---

## What are Ocaps?

From [Wikipedia](https://en.wikipedia.org/wiki/Object-capability_model), an Object Capability is:

- an unforgeable reference (in the sense of object references or protected pointers) that can be sent in messages.
- a message that specifies the operation to be performed.

Furthermore, objects *can only communicate by message sending*, and capabilities can only be obtained by either:

- initial conditions
- parenthood
- endowment
- introduction

i.e., all permissions are fully explicit and delegatable.

One way to think of an ocap is as a first-class object reference.

Another way is a signed message that grants the recipient the power to call a function, which itself can be signed and delegated.

---

## Ocaps as Power

Just think of an Ocap as a power.

It’s a power to do a given thing, given some constraints.

It could be the key to your house, or the right to enter a concert, or some tokens to buy pizza.

But this isn’t just a transferrable power like a physical object, it’s also sharable, or delegatable: Multiple people can wield the same finite power, and you can even delegate a power with new limitations, or “caveats”.

---

## Prior Ethereum Art That Resembles Ocaps

This pattern is already visible repeatedly throughout the ecosystem, although it is not generalized and in turn lacks many key features, but we can look at them now to establish their usefulness, and later we’ll revisit them to see how they could be improved by more deliberate ocap architecture.

---

### The Token Allowance Method

The original inter-contract permission allowed users on exchanges to trigger trades without locking their funds into an exchange contract.

---

### MetaTransactions

A MetaTransaction is a signed message that grants another account, or “relayer” the power to initiate a transaction on your behalf, usually in exchange for a fee.

---

### 0x Protocol Relayers

In the 0x Protocol, an “order” is a signed off-chain message that grants any holder the option to initiate a trade at a rate established in the message, in exchange for a fee to the relayer.

---

### Subscriptions

A subscription is a granted permission to another account to withdraw at a pre-defined rate.

---

### State Channels

Each state channel update can be defined as an off-chain capability for either member of the channel to settle the balance of that channel after a challenge period.

---

### Plasma Chains

Plasma chains imbue their participants with off-chain message that grant them the *capability* to trigger a withdraw function, again which has the caveat of a challenge period.

---

## Delegation and Attenuation

An Ocap can be thought of as a function reference in Java or JavaScript, and in fact JavaScript functions *nearly* resemble ocaps (except for that dangerous global scope).

If you have a function reference, you can call that function, but you can also pass it to someone else (like a smart contract), as *delegation*.

---

When delegating an ocap, you also have the opportunity to add arbitrary caveats, or *attenuations*.

For example, if I have permission to open my front door, I could rent out my house and give my kooky friend permission to open my front door *but only this weekend*.

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/a/ab968f59d6e26b354de4caa0222bcabfeb2fb1d8_2_690x112.png)691×113 29 KB](https://ethereum-magicians.org/uploads/default/ab968f59d6e26b354de4caa0222bcabfeb2fb1d8)

This series of permissions can be represented as a chain of signed messages off-chain, or it can be represented as a chain of permissioned contracts on-chain. There are probably countless possible constructions, so there is probably some value to establish baseline patterns that more sophisticated methods can be built on top of.

---

If we imagine each person and entity has a contract account capable of granting the permission to send transactions to new contracts. This is exactly how [the Gnosis SAFE module system](https://gnosis-safe.readthedocs.io/en/latest/contracts/architecture.html#modules) works, but the pattern should work with any contract capable of delegating sending permission.

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/7/79a8fc499a6a516065cd9f21d78c6b8883e32288_2_690x253.png)777×285 44.3 KB](https://ethereum-magicians.org/uploads/default/79a8fc499a6a516065cd9f21d78c6b8883e32288)

---

We can easily represent the same chain of decreasingly permitted contracts as a series of off-chain messages, in a similar pattern to [counterfactual state channels](https://medium.com/spankchain/a-state-channels-adventure-with-counterfactual-rick-part-1-ce68e16252ea).

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b4a9bb3432304b4eb724602aa124a3fff48e4aaa_2_690x249.png)737×266 43.5 KB](https://ethereum-magicians.org/uploads/default/b4a9bb3432304b4eb724602aa124a3fff48e4aaa)

These messages would only need to be submitted to the door at the time of redemption. A reference to a message would also need to be submitted in order to revoke it.

---

### Stateful Delegations

Some types of delegations can include state, and in those cases, each delegating message would need to result in a deterministically addressed on-chain entity, likely a good opportunity to use the [CREATE2](https://blog.cotten.io/ethereums-eip-1014-create-2-d17b1a184498) opcode.

For example, a delegated spending permission would always need to keep track of the amount withdrawn using it:

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/5/50c787bcce3a864a242929f1b363fbca75b0b848_2_690x142.png)798×165 41 KB](https://ethereum-magicians.org/uploads/default/50c787bcce3a864a242929f1b363fbca75b0b848)

This issue was discussed in the past when discussing [how tokens could be minted off-chain](https://ethresear.ch/t/off-chain-issuable-tokens/3331/2).

Note that as many have observed before, the blockchain is only needed for revoking and limiting permissions (“Blockchain as supreme court”). Extending permissions can happen entirely off-chain, and be consistently described in this pattern, establishing a path for blockchain-minimized development patterns.

---

## Revisiting Prior Art

If the earlier examples used ocaps instead of bespoke off-chain messages, what would be different? Here are a few ideas off the top of my head, there are surely many more benefits.

---

### The Token Allowance Method

If tokens included a transitive, off-chain allowance message, it would allow similar interactions as the current model, but making the setup transaction optional (less on-chain activity, transaction only mandatory on redemption), and also delegatable, which would almost inevitably provide some extensible usefulness.

---

### MetaTransactions

Sites promising to pay for transactions on a user’s behalf could grant gas limits to the user, without locking up funds on a user’s behalf.

Sites could also delegate explicit gas delegation limits to different sybil verification strategies, so that if one were exploited, it would not drain the entire pool.

Additionally, the ability to delegate the permission to pay gas is a great way for users to invite their friends and bypass the “first crypto acquisition” onboarding problem. This benefit is transitive, and so arbitrary graphs of friends could be invited to use the network from a common pool of Ether.

---

### 0x Protocol Relayers

If expressed as delegatable ocaps, 0x orders could be issued to multiple order books simultaneously, and could be delegated multiple hops of order pools, each receiving their own commissions.

---

### Subscriptions

Subscriptions could be created with an off-chain message, and only need to touch the blockchain at the time of a withdraw or redaction.

Additionally, subscriptions represented as ocaps would also be delegatable, and so a subscription service could itself subscribe to services with its own subscriptions. This eliminates capital lockup along a subscription supply chain, allowing more efficient allocation of future capital.

---

### State Channels

As long as the root account incorporates a challenge period before it can withdraw the related funds, a state channel could be created entirely counterfactually. This would mean new participants could be added dynamically, and even signing rights could be freely delegated to external services, even incorporating validation fees, all dynamically added to the live channel without checking into the blockchain.

---

### Plasma Chains

After the state channel example it should be clear that highly dynamic ocap accounts with a challenge period can already evolve into something resembling a Plasma chain. I think the ability for a validator to freely delegate their validation rights to another key or another combination of keys is already a pretty cool new feature.

Since funds in this case can also be sent to a counterfactually-instantiated account (one not published yet), funds on a plasma chain could be recursively deposited into a arbitrary sub-chains with their own withdraw periods, either state channels or tries of plasma chains.

More at [Minimum Viable Consensus with Object Capabilities](https://medium.com/capabul/minimum-viable-consensus-algorithms-with-object-capabilities-6059f926ab88).

---

## Weight on Chain

One concern is that redeeming long chains of delegated ocaps can be expensive to redeem on chain, but that is only true in the most rudimentary case.

This could be addressed *either* with a challenge period in the style of state channels (allowing incomplete proofs), or with more efficient cryptography like [zk-rollup](https://ethresear.ch/t/on-chain-scaling-to-potentially-500-tx-sec-through-mass-tx-validation/3477).

The key message I’d like to communicate here is that the underlying security model is one worth pursuing, not that a specific implementation is ideal.

---

## Data Availability

Many current layer-2 scaling strategies are plagued by data availability concerns. In an ocap architecture, the storage is always aligned with the agent who has value at stake. This means every piece of data has incentive equal to its value to store it, and in turn data availability becomes easier to address, since the actor incentivized to store the data can now choose from any solution available to them to keep their capabilities persistent.

---

## Relationship to the Actor Model

Since each permission is granted between discreet stateful entities that represent a atomic sets of permissions, the Object Capability model is well known to closely map to the Actor Model, a model of computation that is optimal for sharding and scalability.

Here’s a recent article by Brooklyn Zelenka on how the actor model could improve smart contract architecture for Ethereum:

https://medium.com/spadebuilders/actor-factor-2b0005fde786

[More on Wikipedia](https://en.wikipedia.org/wiki/Object-capability_model#Relationship_of_the_object-capability_model_and_the_Actor_model).

---

## The Role of The Wallet

The wallet will play a key role in allowing people to connect to the apps, services, and entites they want to while exposing the least possible risk, and issuing capabilities is an ideal composition pattern for this kind of log-in flow:

- Keeping as much off chain as possible.
- Granting as little permission as needed.
- Allowing the user to revoke permissions at ay time.
- Allowing the service to freely internally delegate its permissions however it needs to.

---

## Making ACLs Look Silly

A number of current Ethereum projects are starting to build complex security models on top of Access Control Lists (ACLs), which are essentially *The Alternative* to Object Capabilities, which are historically easier to invent, and so dominant, but less powerful.

---

For one thing, delegation doesn’t really work in the ACL model. Every time you want to grant a permission, you end up defining a new permission for granting a permission, but who grants the granting permission? And so many ACLs end up being silly lists of things like:

- User
- Moderator
- Admin
- SuperAdmin
- SuperDuperAdmin
- root
- rootroot

By embracing the natural law of transitive delegation, ocaps solve permission moderation in a pattern that naturally scales but is gracefully revocable by branch of broken trust at any time.

---

Also, ACLs are harder to code securely. Correctly writing ACL code requires code reviewers noticing *the absence of enforcement*, [like a missing onlyOwner modifier](https://medium.com/@DaveChappell_83345/detailed-analysis-of-the-300m-ethereum-wallet-breach-83d41fe36dd0), while ocaps invert the pattern, aligning authorization with access, so that access to a function becomes synonymous with permission to use it.

---

## Crowdfunding and DAOs

There is a lot of work being done on sophisticated models of voting and allocating funds using on-chain entities.

Allowing agents to designate spending limits to other agents, and the ability to transitively delegate those allowances is a highly liquid, versatile, and composable way to allow groups of people to pool their resources for common causes.

It may sound simple, but that doesn’t mean it isn’t incredibly powerful!

## Caveats, Expanded

Since caveats are the restrictions on calling a given method, the caveat format is worth deeply considering.

Ideally an account that is capable of issuing ocaps is also capable of interpreting a wide variety of caveats. Some of them may be efficient to express (few bytes), while others might be superior in their open ended nature.

---

For the sake of a minimum viable product, I would probably recommend a few efficiently encoded caveats as early ones:

- Restrict to method name
- Restrict to time period
- Restrict parameter to total sum (spending limit)
- Restrict parameter to amount over time (subscription)
- Restrict calling without challenge period (state channels)

---

Beyond these versatile cases, there should probably also be one open-ended but expensive tool, and this caveat would result in publishing its included bytecode as a new smart contract, which could enforce its own policies arbitrarily, potentially even relying on external state.

Note: Any stateful caveat would result in some state being published to the redeeming platform, and it is an exercise to the community whether multiple limits should reside within the same contract or multiple “actors”, although I think I know what Brooklyn would say!

---

## Challenges at the VM/Language Layer

The EVM 1.x is single-threaded and all calls are synchronous. A true ocap/actor-model architecture requires a message queue for async invocations, and so may be a valuable consideration for Ethereum 2.0.

This allows [avoiding reentrancy issues](https://medium.com/agoric/preventing-reentrancy-attacks-in-smart-contracts-3899bf837f23) the same way JavaScript handles async, with Promises:

```javascript
await sendToken(recipient, amount);
```

*Could JavaScript nearly be a better smart contract language than Solidity? [Some think so…](https://github.com/Agoric/Jessie)*

Fun fact: Promises were invented for the E-language, an ocap-centric language by Mark Miller.

---

## Modular Authentication

The most basic approach to this would involve signatures on every delegation, but to allow inter-contract communication, there is an opportunity to make message authentication more efficient by being modular.

Once authentication is abstracted out of the message itself, this same message-passing pattern could become even more gracefully composable with remote-system oracles, relays, and inter-chain networks.

Write your code once, interact with anything!

---

## Liquid Fundraising

Allows networks of accounts (people/programs) to dynamically allocate their resources to the other agents they trust, in proportion to that trust.

---

## Looking for Contributors!

If you’re interested in helping guide Ethereum towards this secure, extensible, and human centric model, get in touch!

Whether you’re looking for a job or just to do a couple bounty contributions, I’m hoping we can get all willing and able hands on deck for this cause.

---

## References:

- Reentrancy attacks could be eliminated with Object Capabilities
- A video intro to Ocaps
- Ocap-LD: A JSON based Ocap W3C proposal
- Cap’n Proto a highly efficient binary capability serialization format.
- A previous description of off-chain spending permissions
- Capabul: A blog full of my thoughts on the social implications of this pattern
- An example ocap-ld like object in the EIP-712 format
- Promises are Probably Older Than You (NG-conf talk)
- Actor Factor - The Actor Model in Blockchains.
- Liquid Liberal Radicalism - Ocaps applied to Liberal Radicalism.
- Minimum Viable Consensus with Object Capabilities

Mark Miller and his team at Agoric has been truly leading the charge towards ocaps for the last decade or two:

- Mark Miller Video Talks
- Mark Miller Papers
- Agoric Medium
- Agoric YouTube
- Dean Tribble “Trains, Hotels, & Async”
- The Jessie Language

## Replies

**boris** (2019-03-30):

Dan, this is great!

We also think that message queues can be deployed as re-usable smart contracts at the application layer today.

We meaning [@expede](/u/expede) of course, because I’m just the talk-y one ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

We can also improve the VM. Our current one or design future ones ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**jpitts** (2019-03-30):

This is an epic post, could it become an Informational EIP?

---

**danfinlay** (2019-03-30):

Looks like it fits the definition well, good idea!

---

**danfinlay** (2019-04-01):

I’d love to see an [@expede](/u/expede) proposal for generic message queues, and then it would be cool to see if there could be some syntactic sugar for integrating them into the language, maybe in a way that makes it easy to port the same contract code to a sharded/distributed platform.

---

**danfinlay** (2019-09-04):

I just wanted to note here that I think the wisp account type may serve as a good foundation for designing an implementation of this proposal: https://blog.ricmoo.com/wisps-the-magical-world-of-create2-5c2177027604

---

**danfinlay** (2019-11-21):

Some very pragmatic discussion in the general vicinity of this post is happening [over here](https://github.com/KamesCG/rapid-community/issues/1).


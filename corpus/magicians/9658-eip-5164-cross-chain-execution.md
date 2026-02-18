---
source: magicians
topic_id: 9658
title: "EIP-5164: Cross-Chain Execution"
author: Brendan
date: "2022-06-17"
category: EIPs
tags: [chain-agnostic]
url: https://ethereum-magicians.org/t/eip-5164-cross-chain-execution/9658
views: 11506
likes: 23
posts_count: 63
---

# EIP-5164: Cross-Chain Execution

This thread is for discussion pertaining to [EIP-5164](https://eips.ethereum.org/EIPS/eip-5164)

Many thanks to [@anna-carroll](/u/anna-carroll), [@Amxx](/u/amxx), [@mintcloud](/u/mintcloud), [@rafso](/u/rafso), [@auryn](/u/auryn), [@nginnever](/u/nginnever) for their contributions.

If anyone else would like to add their thoughts please speak up! Let’s get this finalized and moving forward. I’ll be reaching out to more bridges and other stakeholders in the meantime so that we can broaden the consensus.

[original pull request](https://github.com/ethereum/EIPs/pull/5164).

## Replies

**Karp** (2022-06-18):

Is this compatible with the merkle root approach that Nomad uses? I believe in Nomad calls are batched not as a list but as a merkle root.

---

**nambrot** (2022-06-18):

Great work everybody, happy to see you [@Brendan](/u/brendan) leading standardization here!

I’m curious and still wrapping my head around the spec, but why does the `CrossChainRelayer.relayCalls(Call[] calldata calls)` function specify no concept of the destination chain for a batch of calls? IIUC correctly the `Call` struct does not sufficiently encode enough information to determine the right `CrossChainReceiver`? I guess there will be an implicit mapping via the nonce in the respective events, but is that really enough for consumers of this abstraction?

In the Nomad taxonomy (as the one I’m familiar with), would `CrossChainRelayer` be the `GovernanceRouter` on the origin chain?

---

**Brendan** (2022-06-19):

Hey Karp, Nam!

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/k/d6d6ee/48.png) Karp:

> Is this compatible with the merkle root approach that Nomad uses? I believe in Nomad calls are batched not as a list but as a merkle root.

In Nomad, the Home contract hashes each message blob to incrementally build a merkle tree. We can put anything we want into that blob!

My understanding of Nomad is that you send messages through a Home contract. Each message sent to the Home contract includes a `domain` code, which determines the merkle root to which the message should be added. Replica contracts on other chains allow users to sign and attest merkle root updates for a particular domain. In this way, the Home contract has no idea who is replicating its state. ([@anna-carroll](/u/anna-carroll) correct me if I’m wrong :))

The Home contract’s lack of knowledge of the receiver address is why I went with the 1-to-n approach. The receivers are aware of the relayer, but not vice-versa.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nambrot/48/6366_2.png) nambrot:

> In the Nomad taxonomy (as the one I’m familiar with), would CrossChainRelayer be the GovernanceRouter on the origin chain?

Yes, they roughly similar. The Nomad `domains` were excluded because they’re specific to Nomad. The `CrossChainReceivers` are simply executing Calls that are passed into the `CrossChainRelayers`. In a way, the receivers are like an extension of the relayer.

One problem with this approach is that the Relayer contract can only determine the message destination based on either the sender address or some configuration in storage. We lost the ability to target a particular domain or target address. A Relayer contract can’t practically serve more than one message “channel”. We’d need to deploy a new Relayer if we changed the bridge.

Message handling is the big difference between Nomad and, for example, the Polygon bridge. Nomad has `domains` (broadcast 1-to-n), while Polygon has a target contract address (1-to-1 messages). Both of them require additional “magic values” (i.e. data from off-chain), whether it’s the Nomad `domain` or the `address` of a contract on another chain in the case of Polygon.

**Allowing Relayers to Send to More than One Receiver**

Perhaps it’s worth defining a `channel` argument that allows users to include implementation-specific data. Something like:

```auto
interface ICrossChainRelayer {
  function relay(bytes calldata channel, Call[] calldata calls) external;
}
```

The “channel” could be the target contract address or Nomad domain, it just depends on the type of bridge. Now a single Relayer contract can be used for multiple “channels”.

**Receiving Bridged Messages vs Executing**

The Receiver is also not ideal, because it both listens to the bridge and executes the calls. If we need to swap the bridge, then the contract executing the calls changes. We’d need to update any Ownables or other permissions.

To make the Receiver more swappable, we could separate the bridging code from execution. Imagine we had the developer supply an Executor contract:

```auto
interface ICrossChainExecutor {
  function execute(address from, Call[] calldata calls) onlyReceiver;
}
```

The developer would implement an executor and bind it to a particular receiver. To swap bridges they just change the receiver that the executor is bound to. The `from` is the original “from” address on the sending chain; I just added that.

Thoughts? It’s late but I wanted to get some ideas out there; hopefully this makes sense! There are lots of ways we can tackle this.

---

**nambrot** (2022-06-20):

> My understanding of Nomad is that you send messages through a Home contract. Each message sent to the Home contract includes a domain code, which determines the merkle root to which the message should be added.

~~I of course do not want to speak for Nomad, but I believe there is a separate home contract for each desired destination domain/chain.~~

EDIT: There is a single merkle root per home contract, messages of different destination domains are added to the same tree.

> Allowing Relayers to Send to More than One Receiver

Yeah I’d be very curious to hear from the consumers of this abstraction whether that is a requirement or not. I’m biased, but I would suspect so? I even wonder whether it is necessary to have this channel data more standardized so that underlying transport channels can be more easily swapped out. IIUC, if I’m Tally and I would like to use this EIP, in its current form, it would still need very transport channel specific logic? I would imagine that bridges like Nomad are more norm than the exception going forward.

> Receiving Bridged Messages vs Executing
>
>
> If we need to swap the bridge, then the contract executing the calls changes.

Is that necessarily true? I think swapping bridges is probably going to be very custom, but it still seems expressible to me? Isn’t that what the `RelayerSet` event is for?

---

**Amxx** (2022-06-20):

Hello,

Some feedback from just reading the draft:

---

I don’t like the

> When a user wishes to send cross-chain messages, they will create a CrossChainRelayer and a CrossChainReceiver.

This is an interpretation of how the ERC could be used, but is not a general truth. In particular, the ERC should not forbid reusing relayer/receiver, or sharing them.

---

`Call` currently does not include a gas amount. I believe this is needed. The execution outcome can obviously differ depending on the amount of gas allocated, and IMO the caller should specify the amount required by the call. Most bridge mechanisms currently include that.

---

I think

> The message receiver always authenticates the sender. This is the case whether contracts live on the same chain or across chains. That’s why the relayer is unaware of the receiver, but the receiver is aware of the relayer.

Is a bad design. Its overly restrictive. IMO, the ERC should discuss abstract relayer and receiver, and makes a little assumption about what is actually going to be checked internally. In particular, requiring the receiver to authenticate the sender, but not specifying this authentication method is not good. It creates a lot of ambiguity, which you don’t want in ERCs.

I see two big approaches to this ERC being used:

- in a “private” context, where an entity (for example a DAO) uses a relayer and receiver to propagate actions everywhere (the routing is missing from this ERC, so I assume it would be a broadcast). In that case, the emitter would be restricting call requests, and the receivers don’t case what the DAO’s address is, as long as the emitter is the right one. The emitter could even be the DAO itself …
I don’t really like this case because it assumes the “private” entity will have the knowledge to build this relaying system from the ground up, and will maintain them.
- in a “public” context, where anyone can send any message to anyone on the receiving end. This would IMO be the #1 use-case. Technically the ERC is enough because the “relaying on L2” mechanism is not in scope … but still, inside the scope of the relaying, having the address of the caller is essential (because it would have to be exposed to the callee). So we need the message sent between the relayer and the receiver to include that info.

To accommodate the second usecase, and also because I think the first usecase could use it, I would add

> ```auto
> interface CrossChainReceiver {
>    messageSender() returns (address)
> }
> ```
>
>
>
> If called during the execution of a cross-chain Call, MUST returns the address of the account that submitted the call on the relayer
> If called outside the execution of a cross-chain Call, MUST returns the default value 0x000000000000000000000000000000000000dEaD

---

I would argue that by default the relayer should not be re-configurable. Allowing that would cause  lot of governance issues. Some people may want a governed relayer, but I don’t think the `RelayerSet` event should be a default thing.

---

**Amxx** (2022-06-20):

Also, it goes without saying that I would add a `sender` or `caller` param to the events.

---

**drinkcoffee** (2022-06-23):

Have you considered using the same APIs as provided by the function call layer of the Crosschain Protocol Stack? In that way, any crosschain application can work with any crosschain function call approach, with any crosschain messaging layer. For example, Nomad could be the messaging layer, and GPACT or a non-atomic function call approach could be used.

For example, the API for calling a function on a different chain is here:



      [entethalliance.github.io](https://entethalliance.github.io/crosschain-interoperability/draft_crosschain_techspec_function.html#sec-CrosschainFunctionCallInterface)





###



This document, the Enterprise Ethereum Alliance Crosschain Interoperability Technical Specification, defines
the implementation requirements for Enterprise Ethereum clients that wish to do cross-blockchain communications.










Crosschain Protocol Stack: [Enterprise Ethereum Alliance Crosschain Interoperability Technical Specification Draft Version 1.0](https://entethalliance.github.io/crosschain-interoperability/draft_crosschain_techspec.html)

Function Call Layer: [Enterprise Ethereum Alliance Crosschain Interoperability Technical Specification Function Call Interface Draft Version 1.0](https://entethalliance.github.io/crosschain-interoperability/draft_crosschain_techspec_function.html)

Messaging Layer: [Enterprise Ethereum Alliance Crosschain Interoperability Technical Specification Messaging Interface Draft Version 1.0](https://entethalliance.github.io/crosschain-interoperability/draft_crosschain_techspec_messaging.html)

---

**drinkcoffee** (2022-06-23):

An important feature that in my quick read through didn’t see is crosschain authentication. You need the ability to do something similar to require(msg.sender == authenticated) for crosschain. Did the call come from an authorised contract on a certain blockchain.

---

**geogons** (2022-06-23):

Hi [@Brendan](/u/brendan), a question from the ChainBridge team:

What’s the rationale behind making CrossChainRelayer nonpayable?

How would it be possible for the bridge to charge fees on the source chain?

---

**Brendan** (2022-06-25):

Hey everybody, excuse the delay I was busy with some events.

# Public vs Private Bridge

[@Amxx](/u/amxx) articulated a very important design consideration: whether the ERC supports public or private bridges.

Public bridge: a bridge that anyone can use to send messages. It’s generalized, such that the receiver knows the caller on the origin chain. Many bridges are like this; Optimism, Polygon, and others.

Private bridge: a bridge is specific to a dapp. This is like Nomad’s home and replicas (i.e. relayer and receiver). Replicas need to be censorable by a dapp, so Nomad considers them dapp-specific.

The above EIP is essentially a private bridge; which means a user would need to deploy wrappers for some existing bridges. It’s compatible with Nomad, but precludes public bridges. Not ideal.

**By having the EIP support public bridges it will be compatible with both approaches**. A public design would still allow the user to deploy their own for a private bridge, but would support public bridges as well.

This is why I was thinking the spec should support bridge swaps [@nambrot](/u/nambrot), because in its current design the receiver executes the call, making it a privileged part of the protocol. To swap the bridge we’d need to update the receiver. Not ideal.

Btw [@nambrot](/u/nambrot), you asked why we would swap: for chains such as Optimism I’d prefer to use the native bridge for slow-moving pieces like governance. However, when tech like Nomad is more robust and has an incentivized censorship layer we’d be able to switch to it for faster bridging.

# Additional Fields

## Gas

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Call currently does not include a gas amount. I believe this is needed.

That’s smart- I like it. Should we have a special value? I.e. if `gas` is zero then it’s considered no-limit?

## Caller

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> I would add a sender or caller param to the events

100%. Going with a public approach would necessitate this.

## Payable

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/geogons/48/6415_2.png) geogons:

> [can] it be possible for the bridge to charge fees on the source chain?

That’s a cool idea! The send message function should be payable.

# Summary

- Update the EIP to be public, not private
- Make relayCalls payable
- Add gas limit and caller

Note: by making the bridge public the receiver contract will be verifying the caller as being their desired bridge. We won’t have to worry about authentication [@drinkcoffee](/u/drinkcoffee), as it’s dapp-specific (imagine a dapp that has a public function that can be called across a bridge).

**I’ve updated the EIP with the above changes**

[view the new version here](https://github.com/ethereum/EIPs/blob/a641fed8dd2d8ca3799bea19b2c77d9528728f64/EIPS/eip-5164.md).

Please review and comment so that we can continue iterating!

# Open Questions

Should we have a `relayData` call that relays a simple `bytes data` param? Or perhaps the Calls struct could be an extension? Would be curious to hear anyone’s thoughts.

---

**Amxx** (2022-07-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> Amxx:
>
>
> Call currently does not include a gas amount. I believe this is needed.

That’s smart- I like it. Should we have a special value? I.e. if `gas` is zero then it’s considered no-limit?

I’m not sure how detailed the ERC should be. I personally see an approach that would be similar to what GnosisSafe does for their multisig

- If the gas value is non zero, then the call must be performed with AT LEAST this value (we check that 1/64 of this value is remaining after the call).

If the call is a success, then all good (and it should not be replayed)
- If the call is a failure despite the gas requirement being met, then the call is non-retriable (we gave it a fair chance and it failed).

If the gas value is zero, then any amount provided is forwarded.

- If the call is a success, then all good (and it should not be replayed)
- If the call is a failure, then we create a “retriable ticket” that anyone can try to run. with any amount of gas. If the retry call fails, the ticket remains available. If the retry successed, we burn the ticket to prevent double execution.

---

**kladkogex** (2022-07-04):

Congrats on the EIP !

Please take a look at SKALE IMA bridge since it impements a generic messaging framework that resonates well with this EIP

https://docs.skale.network/ima/1.3.x/getting-started

It is currently running on SKL main net and allows to send a message from any SKL chain to any other SKL chain and to ETH main net

If there is an industry wide EIP we at SKALE are happy to make our messaging compliant.

The hardest feature is actually assigning and reimbursing gas costs correctly

---

**Brendan** (2022-07-06):

Hey [@kladkogex](/u/kladkogex) thanks for chiming in!  I poked through the docs but the setup didn’t jump out at me. Can you include a snippet? Or perhaps have a look at the EIP and see if we’re missing anything?

---

**Brendan** (2022-07-06):

[@Amxx](/u/amxx) Regarding the retry logic: it seems like that it implementation-specific, no? I hesitate to include that in the EIP.  As you said earlier, different bridges have different retry logic.

I do like your additional specification around the gas field. However, it feels like there are two elements to this: how much gas the CrossChainReceiver#receiveCalls fxn uses, and how much each of the calls in the batch should use.

Here’s a diagram of the EIP in its current form:

[![Screen Shot 2022-07-06 at 3.10.48 PM](https://ethereum-magicians.org/uploads/default/optimized/2X/a/aa5fb3e8cf37efd545929657872c3a18cffd5844_2_690x425.png)Screen Shot 2022-07-06 at 3.10.48 PM1990×1228 154 KB](https://ethereum-magicians.org/uploads/default/aa5fb3e8cf37efd545929657872c3a18cffd5844)

There are a couple of issues here:

- The CrossChainReceiver#receiveCalls() fxn is called by the bridge layer.  The bridge will only know the gas usage after the receiveCalls function is executed. This makes it hard to know costs up-front.
- Each Call struct currently has a gas value, but really it’s up to the user-implemented CrossChainReceiver to respect that value.  It’s not used directly by the ERC.

I noticed that in your [bridge code](https://github.com/Amxx/openzeppelin-labs/blob/3e843ccaa374a5147a92528ae2fbaa28bb70b797/crosschain-contracts/contracts/modules/CrossChainEnabledArbitrumL1.sol#L22) it defines the call along the lines:

`Bridge.crossChainCall(address target, bytes memory message, uint32 gasLimit)`

This ERC has essentially encoded a batch of calls in the message.  In your bridge, however, the gas limit essentially applies to the `CrossChainReceiver#receiveCalls` function.

This makes a lot more sense to me, as it is deeply functional for the bridge: the bridge now knows the expected gas limit for the `CrossChainReceiver#receiveCalls` function. This is made available on the sending chain as well, so the bridge could even take a payment on the sending side based on the required gas (a la the payable `relayCalls` fxn)

This makes me think we should follow the same logic as your bridge by adding a gas limit:

```auto
interface CrossChainRelayer {
    function relayCalls(CrossChainReceiver receiver, Call[] calldata calls, uint gasLimit);
}
```

We would then remove the `gas` field from the `Call` struct.

I don’t think the `CrossChainReceiver` needs to know the gas limit, because the limit is simply applied to the call by the bridge.

Thoughts?

---

**Amxx** (2022-08-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> @Amxx Regarding the retry logic: it seems like that it implementation-specific, no? I hesitate to include that in the EIP. As you said earlier, different bridges have different retry logic.

The thing is to have a retry logic that is NOT implementation specific, and that is standard to the bridge. It could technically be achieved in an extension ERC.

---

**Amxx** (2022-08-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> Here’s a diagram of the EIP in its current form:
>
>
> Screen Shot 2022-07-06 at 3.10.48 PM1990×1228 154 KB

I honestly don’t like this dependency on “receiveCalls”. It messes the ABI, and would be difficult to implement if the calls are arbitrary.

IMO the ERC-5164 CrossChainRelayer (on the sending chain) should call one dedicated contract on the receiving chain (we’ll need a name for that), which will in turn relay the call to the user contracts, just like the AMB and Optimism bridges do today.

I believe this will be cleaner. It would also put most of the logic on the receiving end in a contract that is reused, instead of requiering every user contract to ship it (in some cases this code can be really big)

---

**Amxx** (2022-08-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> I don’t think the CrossChainReceiver needs to know the gas limit, because the limit is simply applied to the call by the bridge.

As mentionned above, the cross chain signal should not go directly to the user contract. It should go to a bridge contract, which forwards the calls one by one (which a minimum amount of gas specified in the `Call` structure).

This bridge contract would be able to see if execution fails, and could (in the futur?) include retry mechanisms

---

**Amxx** (2022-08-12):

My vision was more something like this:

[![5164](https://ethereum-magicians.org/uploads/default/original/2X/a/ade0117a4ec5c8a982795f21d22a013acd15bb70.png)5164329×279 16 KB](https://ethereum-magicians.org/uploads/default/ade0117a4ec5c8a982795f21d22a013acd15bb70)

Again, i believe it would be way more versatile for the user contract on the receiving side not having to implement the calls going through a dedicated `receiveCalls`. This receiveCalls would be part of the red “implementation specific” interface between the two sides of the bridge.

To give some image, I’d like the bridge to be a bridge, with two sides, and that you can take in both direction. Not a catapult that sends you somewhere where a mattress is needs to catch you fall. Each side of the bridge would have an address, in a city, and would ideally know the address (and the city) of the other side.

Note: the user contract would still have to be “bridge aware” so that they recover the correct sender when msg.sender == bridge … but that is a very small piece of logic that could easily support multiple bridges (as long as they implement the same “user facing” interface).

---

**Brendan** (2022-08-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Not a catapult that sends you somewhere where a mattress is needs to catch you fall.

![:joy:](https://ethereum-magicians.org/images/emoji/twitter/joy.png?v=12) I like to of it as a one way street; when you combine two it becomes a two-way street. Although a catapult would be more fun to watch!

I agree with you in that I’d like the user space “receiver” to be as simple as possible. The trick is that we want the receiver to recognize both the bridge contract (to authorize the transport layer) and the caller on the other side (to authorize the action). Passing the caller explicitly seems like the simplest 80 IQ approach…but what else are you thinking? Perhaps the GSN-style extra calldata bytes for the sender?

You know what is interesting- the `CrossChainRelayer (receiver)` in your diagram is basically an implementation of the `CrossChainReceiver`. I quite like this as it specifically defines how the `Call[]` batch is handled, instead of leaving it up to a user-space implementation.

**Quick update for everyone else:** Pierrick from PoolTogether is starting work on ERC-5164 implementations for the native Optimism, Arbitrum, and Polygon message bridges. We’re going to collaborate with [@Amxx](/u/amxx) and use his [prototype work](https://github.com/Amxx/openzeppelin-labs/tree/devel/crosschain-contracts/contracts/libs). The implementations will help us refine the spec, then when we’re ready we’ll finalize the ERC and audit the bridges. Then we’ll have standardized bridges that everyone can use!

---

**Amxx** (2022-08-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brendan/48/6095_2.png) Brendan:

> Passing the caller explicitly seems like the simplest 80 IQ approach…but what else are you thinking?

You know what the meme says, sometimes the most stupid things are also the smartest ones.

I would love to see contracts do something like this:

```auto
interface ICrossChainReceiver {
    function foreignChainId() returns (uint256); // returns the chainId of the foreign chain
    function foreignSender() returns (address); // returns the address of the cross chain sender if during a crosschain call
}

contract BridgeAware {
    mapping(address => bool) isBridge;
    mapping(uint256 => mapping(address => bool) authorized;

    modifier onlyAuthorized() {
        bool isCrossChain = isBridge[msg.sender];
        address chain = isCrossChain ? IBridge(msg.sender).foreignChainId() : block.chainid;
        address sender = isCrossChain ? IBridge(msg.sender).foreignSender() : msg.sender;
        require(authorized[chain][sender], "Not authorized");
        _;
    }
}
```


*(42 more replies not shown)*

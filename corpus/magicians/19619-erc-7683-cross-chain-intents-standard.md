---
source: magicians
topic_id: 19619
title: "ERC-7683: Cross Chain Intents Standard"
author: marktoda
date: "2024-04-11"
category: ERCs
tags: [erc-20, interop, cross-chain, standards-adoption]
url: https://ethereum-magicians.org/t/erc-7683-cross-chain-intents-standard/19619
views: 11065
likes: 65
posts_count: 52
---

# ERC-7683: Cross Chain Intents Standard

The Cross Chain Intents Standard is meant to unify off-chain messages and on-chain settlement smart contracts to enable sharing of infrastructure, filler networks, and orders across cross-chain bridging and trading systems.

ERC:



      [github.com](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7683.md)





####



```md
---
eip: 7683
title: Cross Chain Intents
description: An interface for cross-chain trade execution systems.
author: Mark Toda (@marktoda), Matt Rice (@mrice32), Nick Pai (@nicholaspai)
discussions-to: https://ethereum-magicians.org/t/erc-cross-chain-intents-standard/19619
status: Draft
type: Standards Track
category: ERC
created: 2024-04-11
---

## Abstract

The following standard allows for the implementation of a standard API for cross-chain value-transfer systems. This standard provides generic order structs, as well as a standard set of settlement smart contract interfaces.

## Motivation

Intent-based systems have become the preeminent solution for end-user cross-chain interaction by abstracting away the complexity and time constraints of traditional bridges. One of the key difficulties for cross-chain intents systems is accessing sufficient liquidity and a network of active fillers across chains. This challenge may be exacerbated as the number of distinct chains increases over time. The end result of this is a poor experience for users including higher costs, longer wait times and higher failure rates than necessary.

```

  This file has been truncated. [show original](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7683.md)

## Replies

**xinbenlv** (2024-04-11):

Hi [@marktoda](/u/marktoda), cross-chain intents, this is an important space to solve on. Thanks for proposing it!

A few technical questions

1. settlement, swap etc seems assuming a specific token or token standard and a clearing / settling enivronment, have we think about making it something more general like a UserOps / general contact call?
2. on the other hand, assuming this standard just wanna solve crosschain token settlement, how does ResolvedCrossChainOrder include attestants from the settlement chain?

---

**nicholaspai** (2024-04-11):

hey [@xinbenlv](/u/xinbenlv) i’ll try to chime in here.

1. I think the  generalized message problem is very different from the token swap standard. I think smart contract systems that support this token standard (like Bridges and Cross Chain DEX’s) will be built on top of some sort of messaging network that uses a message standard in some way. The goal we had with proposing this token standard is to shrink the scope of the problem so that Bridges and DEX’s can use the standard today today while maintaining composability with existing messaging networks.
2. I think the idea of “attestants” is an opinionated feature that some intent settlement networks might use but others may not. I’m assuming you are defining an attestant as someone who claims “I saw an intent sent on X origin chain and I want to fulfill it” or perhaps someone who claims “I saw an intent sent on X origin chain and it was fulfilled by Alice on Y destination chain”. If an attestant is the former role, then I think they are a “filler” in the standard’s language, which is not included in the standard as it is not required for the intent principal to define when initiating an intent. However, some settlement systems might allow the intent to whitelist a specific filler for a specific intent. If an attestant is the latter role, then they are an intent settler or settlementContract in the standard. One of the goals of the standard is to allow intent settlement contracts to be opinionated about how they refund fulfilled intents while also committing to some shared language and feature-set. The standard allows fillers to define who they want to decide whether their fulfillment was valid or not, which helps them to give more accurate pricing to users who submit cross chain intent orders

---

**xinbenlv** (2024-04-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nicholaspai/48/7121_2.png) nicholaspai:

> I think the generalized message problem is very different from the token swap standard. I think smart contract systems that support this token standard (like Bridges and Cross Chain DEX’s) will be built on top of some sort of messaging network that uses a message standard in some way. The goal we had with proposing this token standard is to shrink the scope of the problem so that Bridges and DEX’s can use the standard today today while maintaining composability with existing messaging networks.

Agreed, in that case please update the title and summary to reflect this scope

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nicholaspai/48/7121_2.png) nicholaspai:

> I think the idea of “attestants” is an opinionated feature that some intent settlement networks might use but others may not. I’m assuming you are defining an attestant as someone who claims “I saw an intent sent on X origin chain and I want to fulfill it” or perhaps someone who claims “I saw an intent sent on X origin chain and it was fulfilled by Alice on Y destination chain”.

It’s less opinionated than you think: it’s more about future compatibility. If there is an attestation field predefined, anyone (future contract implementing your ERC) who doesn’t care about attestation can just leave it unfilled, contracts can ignore them: the behaves like a naive optimistism without challenging mechanism, pretty much centralized trust is the only way. yet anyone (future contract implementing your ERC) who cares about attestation can fill them with challengable optimistism commitments or zkproofs.

Opens up a lot of future compatibility for you.

That said, this is a great idea to work on. congrats on drafting it!

---

**heuer** (2024-04-12):

> have we think about making it something more general like a UserOps / general contact call

I think what you are proposing here is done by [Anoma](https://anoma.net/) (see also [Anoma: a unified architecture for full-stack decentralised applications](https://zenodo.org/records/8279842), or the recent [ethresear.ch](https://ethresear.ch/t/rfc-draft-anoma-as-the-universal-intent-machine-for-ethereum/19109) post).

---

**FakeZL** (2024-04-23):

Should we consider not only EVM chains but also NO-EVM chains?

0. orderData is a good design for support no-evm chain

1. in the difine ResolvedCrossChainOrder：input

```auto
/// @notice Tokens sent by the swapper as inputs to the order
struct Input {
	/// @dev The address of the ERC20 token on the origin chain
	address token;
	/// @dev The amount of the token to be sent
	uint256 amount;
}
```

adress token should not be type address

---

**xinbenlv** (2024-04-25):

Hi authors of ERC-7683, this is Victor, an EIP editor and current operator of AllERCDevs.

I like to invite you to our next AllERCDevs meeting (online) to present for 10min of your ERCs if you are interested!

AllERCDevs is a bi-weekly meeting for ERC authors, builders and editors to meet and help the drafting and adoption of an ERC. The next one is 2024-04-30 UTC 2300, let us know if this time works for you, I can put this ERC in the agenda, or you can add a response directly at [S2E4 AllERCDevs Agenda 2024-04-30 Tuesday UTC2300 (APEC friendly time) · Issue #22 · ercref/AllERCDevs · GitHub](https://github.com/ercref/AllERCDevs/issues/22)

---

**ss-sonic** (2024-05-21):

The value proposition of EIP-7683, which aims to standardize cross-chain trade execution, is indeed compelling. The potential to streamline cross-chain interactions by providing a unified interface is a significant step forward. However, there are several areas where this proposal could be further enhanced:

1. Title and Scope:

The title “Cross Chain Intents” is somewhat misleading. The term “intent” is highly generalized and can encompass a wide range of actions beyond just token trades. In the context of blockchain, intents can represent any programmable action, from complex financial transactions to staking and governance activities. A more precise title could help set accurate expectations.
2. Current Limitations:

As it stands, the proposal primarily facilitates cross-chain token trades using a Request for Quote (RFQ) mechanism. While this is useful, it does not significantly differentiate itself from existing primitives. The current demand in the ecosystem is for more generalized standards that can support a broader range of cross-chain activities. For instance, enabling users to purchase a token on one chain and automatically stake it in a protocol on another chain would provide greater utility.
3. Scalability and Security Considerations:

The proposal should address how it will scale for Rollups, considering their unique security and finality challenges. Rollups often have delayed transaction finality, and understanding how disputes and resolutions will be handled in the case of rollbacks is crucial. Clarifying these mechanisms will be vital for ensuring robustness and user trust.
4. Potential for Expansion:

There is a promising opportunity for this standard to evolve into something more sophisticated. Allowing users to express complex intents and having these intents executed by fillers (entities with the necessary funds and capabilities) can open up a myriad of possibilities. Fillers, essentially acting as service providers, could execute a wide range of instructions, from simple swaps to intricate financial operations, in exchange for fees and potential refunds.
5. Generalized Intent Execution:

The vision should expand towards enabling fillers to carry out a broader set of user-defined actions. This could involve complex transactions that span multiple protocols and chains, thereby significantly enhancing the user experience and the functional scope of cross-chain interactions.

We at Router Protocol are tirelessly trying to solve for chain-abstraction, which is our key area of focus. We are happy to ideate and collaborate to make web3 more simple and usable. In conclusion, while EIP-7683 lays a solid foundation for cross-chain trade execution, its true potential lies in broadening its scope to encompass a wider range of blockchain activities. Addressing scalability and security for Rollups and enabling more complex intent executions could transform this proposal into a cornerstone of cross-chain interoperability.

---

**frangio** (2024-05-23):

> Cross-chain execution systems implementing this standard SHOULD create a custom sub-type that can be parsed from the arbitrary orderData field.

If this struct is to be signed as EIP-712 data (the ERC doesn’t specify), the `orderData` will show up as uninterpreted bytes (i.e. a hex string) to the end-user, resulting in bad security (verifiability) and usability.

This kind of pattern is useful though, and it has come up before in the context of making EIP-1271 signatures account-bound and replay-protected. I believe an EIP-712 extension may be necessary to properly address this.

---

**frangio** (2024-05-23):

I’ve proposed an extension of EIP-712 that would enable better support for implementation-specific `orderData`:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png)
    [EIP: Box types for EIP-712 messages](https://ethereum-magicians.org/t/eip-box-types-for-eip-712-messages/20092) [EIPs](/c/eips/5)



> A special type box is defined for EIP-712 messages. A box value is a value of an arbitrary struct type whose underlying type is encapsulated from the containing struct, but transparent and type-checkable by the wallet, and thus able to be fully inspected by the user prior to signing. A verifying contract can be made agnostic to the underlying type of a box value, but this type is not erased and can be verified on-chain if necessary.

---

**nicholaspai** (2024-05-24):

> The current demand in the ecosystem is for more generalized standards that can support a broader range of cross-chain activities. For instance, enabling users to purchase a token on one chain and automatically stake it in a protocol on another chain would provide greater utility

We designed ERC7683 on the assumption that the majority of cross chain user intents are to (1) do some arbitrary action on the origin chain and then (2) swap into a token on the destination or vice versa. We therefore left room in the `bytes orderData` to encode arbitrary action. For example, the arbitrary data to execute (2) could be encoded like so into the `CrossChainOrder` struct:

```sol
// Bytes field from CrossChainOrder struct containing the ERC7683-compliant ResolvedCrossChainOrder data along with extra data.
bytes orderData = order.orderData;
struct DestinationAppData {
    address target; // contract I wish to call on the destination chain after my intent is fulfilled
    bytes targetData; // calldata I want to execute on target contract on destination chain
}
(DestinationAppData appData, ResolvedCrossChainOrder crossChainOrder) = abi.decode(order.orderData, (ImplementationData));
```

Now, I can support a user flow where my user submits an intent containing the above `target` and `targetData` in addition to the intent-specific parameters like `{input}/{output}{Token}/{Amount}`, `destinationChainId`, `originChainId`, `initiateDeadline`, `depositor`, etc. The user’s chosen intent settlement network would then need to ensure that when a solver fulfills the user’s intent, that the fulfillment triggers a call to `target` with `targetData` on behalf of the `depositor`.

In my opinion, enabling these generalized cross chain user flows is a feature that intent settlement networks can choose to offer or not, and there is room in ERC7683 to support this if the intent principal chooses a supporting `settlementContract`. The Across network [supports this](https://docs.across.to/integration-guides/across+-integration), for example.

> Allowing users to express complex intents and having these intents executed by fillers (entities with the necessary funds and capabilities) can open up a myriad of possibilities. Fillers, essentially acting as service providers, could execute a wide range of instructions, from simple swaps to intricate financial operations, in exchange for fees and potential refunds.

Now, this does not handle the case naturally where someone just wants to send a message, involving no token transfers, cross-chain. But you and I both seem to agree that all cross chain user intents will involve a token swap in some way

So, our long term vision is very much aligned with supporting generalized intent execution but we acknowledge that the biggest use case of intents will be to do (1) and (2) above. Therefore this ERC was written to contain the minimum set of parameters to support this cross-chain swaps plus arbitrary action without being too generalized as to be meaningless.

On the rollup security issue, I do not agree that rollup security is not addressed in the ERC parameters, though it is not obvious. By including the `settlementContract` in the `CrossChainOrder` struct, the user (or realistically, dApp) has freedom to decide which mechanism will settle their intent and therefore ensures that their intent is fulfilled. In my opinion it is the settlement contract’s responsibility to handle rollup liveness securely. By forcing users to specify the settlement contract, this ERC provides a foundation for a settlement marketplace where settlement protocols compete to abstract rollup security away from users. In my opinion the most successful settlement networks will be the ones who most efficiently remove finality risk while fulfilling user intents and also refund honest solvers.

---

**anna-carroll** (2024-06-04):

Hey y’all, small point of feedback - in the `resolve` function, why does the return type `ResolvedCrossChainOrder` repeat all of the fields on the parameter `CrossChainOrder`? is there ever a circumstance where the repeated fields would or should change between the input `CrossChainOrder` and the output `ResolvedCrossChainOrder`? in practice, copying these fields from the input type to the return type makes developing smart contracts that implement this standard unnecessarily uglier to write.

repeated fields:

```auto
    /// @dev The contract address that the order is meant to be settled by.
    /// Fillers send this order to this contract address on the origin chain
    address settlementContract;
    /// @dev The address of the user who is initiating the swap,
    /// whose input tokens will be taken and escrowed
    address swapper;
    /// @dev Nonce to be used as replay protection for the order
    uint256 nonce;
    /// @dev The chainId of the origin chain
    uint32 originChainId;
    /// @dev The timestamp by which the order must be initiated
    uint32 initiateDeadline;
    /// @dev The timestamp by which the order must be filled on the destination chain
    uint32 fillDeadline;
```

I would cut the repeated fields from `ResolvedCrossChainOrder` to change the type to something like `ResolvedOrderData`:

```auto
/// @title ResolvedOrderData type
/// @notice An implementation-generic representation of an order
/// @dev Defines all requirements for filling an order by unbundling the implementation-specific orderData.
/// @dev Intended to improve integration generalization by allowing fillers to compute the exact input and output information of any order
struct ResolvedOrderData {
    /// @dev The inputs to be taken from the swapper as part of order initiation
    Input[] swapperInputs;
    /// @dev The outputs to be given to the swapper as part of order fulfillment
    Output[] swapperOutputs;
    /// @dev The outputs to be given to the filler as part of order settlement
    Output[] fillerOutputs;
}

```

then

```auto
    /// @notice Resolves a specific CrossChainOrder into ResolvedOrderData
    /// @dev Intended to improve standardized integration of various order types and settlement contracts
    /// @param order The CrossChainOrder definition
    /// @param fillerData Any filler-defined data required by the settler
    /// @return ResolvedOrderData hydrated order data including the inputs and outputs of the order
    function resolve(CrossChainOrder order, bytes fillerData)
        external
        view
        returns (ResolvedOrderData);
```

of course, we still need to pass in the entire `CrossChainOrder` and `fillerData` as parameters (not just the raw `orderData` bytes) as `ResolvedOrderData` resolution may depend on additional fields

---

**nicholaspai** (2024-06-10):

Hey [@anna-carroll](/u/anna-carroll) thanks for taking a look at this, I think this is a very fair response. I think the idea behind `ResolvedCrossChainOrder` is that any user of a settlement protocol could glance at this struct in isolation to determine the shape of their intent order with respect to the settlement protocol. The expected user in this case would be a dApp developer or filler.

But I also think its expected that this same user would already know the shape of the `CrossChainOrder`, having just created/filled an intent order using it, and then would only want to know the additional new params in `ResolvedCrossChainOrder` that are relevant for the specific settlement contract.

---

**chainchampion** (2024-06-15):

Does this standard enforce / assume that the settlement contract has to live on the source chain of the intent?

What about a settlement model where the intent can be settled on the destination chain or maybe an arbitrary chain which acts as the source of truth for both intent order as well as settlement

---

**nambrot** (2024-06-24):

Thanks for pushing standardization on this very important topic! Here are some of my notes as part of conversations that I had with various folks over the last couple weeks about this topic:

- I agree that arbitrary post-fill actions with the tokens are a highly desired feature for cross-chain intents. What do you think about making it an explicit field on CrossChainOrder so that the intent has more standardized fields and requires less divergent tooling for parsing?
- While different intent generation and settlement systems could require vastly different orderData schema, I was wondering if there is opportunity for standardization without preventing experimentation. I was thinking of a mechanism like in EIP191 that has a version byte that allows the EIP to formalize orderData like a simple limit order, or an exact order.

Another benefit of pushing for more standardization on orderData is to have less variability in permit2 witnesses and type strings, and allow UIs/wallets to optimize the experience for the standard ones.

Probably doesn’t need to be in the EIP itself, but the high generality of the standard made it a bit hard to wrap your head around it for folks who are not in the weeds. Pseudo-code examples of `orderData` and `settlementContracts` I imagine would be helpful in conveying the power of this standard.
I’m curious if you thought about a standard function for filling? I.e. a `function fill(CrossChainOrder order, bytes fillerData)`. I suspect that there are systems where there is no need to change contract state to record the fill which is why it was omitted, but I’d imagine that standardizing this for the settlement systems that do would be still beneficial?

---

**mrice32** (2024-06-26):

Wouldn’t you still need some contract to process the intent on the origin chain since that’s where the user’s tokens reside? The standard only imposes that some contract exists on the origin to process the intent, not that that’s the only point of interaction or validation.

---

**mrice32** (2024-06-26):

> I agree that arbitrary post-fill actions with the tokens are a highly desired feature for cross-chain intents. What do you think about making it an explicit field on CrossChainOrder so that the intent has more standardized fields and requires less divergent tooling for parsing?
> While different intent generation and settlement systems could require vastly different orderData schema, I was wondering if there is opportunity for standardization without preventing experimentation. I was thinking of a mechanism like in EIP191 that has a version byte that allows the EIP to formalize orderData like a simple limit order, or an exact order.
>
> Another benefit of pushing for more standardization on orderData is to have less variability in permit2 witnesses and type strings, and allow UIs/wallets to optimize the experience for the standard ones.

The way the standard is currently designed, the explicit fields are only the ones that would apply to all implementing protocols. It is intentionally minimalist to ease the burden on implementing protocols and fillers. Adding post-fill actions would mean that some protocols might not implement part of the official standard and be forced to reject intents with that field, which might be confusing. Alternatively, if that field was required to be handled by all protocols implementing the standard, it would be limited to protocols that support it.

Jumping off your points, maybe the right path is to have an extension specification, where extensions that take advantage of orderData could be built and encoded in a specific way whereby each extension is, by default, not mutually exclusive with other extensions. For instance, maybe there’s an extension to encode a limit order and another extension to do post-fill actions. The former could be assigned identifier 0x01 and the latter assigned the identifier 0x02. If my protocol supports both, it could parse the order data to identify the data for each extension using the identifier. If my protocol doesn’t support one of them, it could fail during the parsing process. While something like this is doable, it is complex to specify and implement. Maybe it belongs in a separate ERC.

Thoughts? In my opinion minimalist ERCs often have the best chance of gaining adoption and being useful.

> Probably doesn’t need to be in the EIP itself, but the high generality of the standard made it a bit hard to wrap your head around it for folks who are not in the weeds. Pseudo-code examples of orderData and settlementContracts I imagine would be helpful in conveying the power of this standard.

Totally agree. More can and should be added there.

> I’m curious if you thought about a standard function for filling? I.e. a function fill(CrossChainOrder order, bytes fillerData). I suspect that there are systems where there is no need to change contract state to record the fill which is why it was omitted, but I’d imagine that standardizing this for the settlement systems that do would be still beneficial?

Definitely. It’s something I’m still wrestling with. The issues I see with a fill function:

- Most of the time, a filler does not need to pull in the entire Order/ResolvedOrder to do the fill. Only a fraction of that information is needed at fill time. However, because different protocols will need different pieces of the order (especially different pieces of the orderData), I can’t see how you could avoid requiring the entire order to be passed in and re-parsed. This would be very inefficient for implementing protocols.
- Some protocols or order types may depend on the state of the blockchain at the time of the initiation call to determine the exact parameters for the fill. For instance, imagine a dutch auction where the pricing of the order depends on the block.timestamp at initiation time. This would mean that you would need some mechanism by which the filler could a) get this information and b) communicate this information to the destination chain. You could just add an arbitrary bytes field and leave it up to the filler/protocol to figure all of this out, but then that means the standard isn’t really saving the filler/protocol much in that case, while imposing this bytes field on all the protocols that don’t need this contextual info. Note: fillerData isn’t this data, because fillerData in your example is presumably the same filler data submitted to initiate. The contextual info I’m referencing isn’t known until the initiate call is complete.

---

**qinyu** (2024-06-26):

Thanks for pushing a standard for cross-chain transaction, we (paywithglide.xyz) are looking to adopt this standard to work with our cross-chain execution system

Per the Input struct and signature based initiate function, it seems the standard assumes the input token is always ERC20? Curious if this standard can work with native token as swapper input token?

> /// @notice Tokens sent by the swapper as inputs to the order
> struct Input {
> /// @dev The address of the ERC20 token on the origin chain
> address token;
> /// @dev The amount of the token to be sent
> uint256 amount;
> }

---

**nambrot** (2024-06-30):

I definitely sympathize with the desire in keeping the EIP simple and understand that additional specificity, even if for optional extensions can be counter-productive. I admit that I generally bias towards the technical implementation considerations of standards, and less so the social aspects of them.

> Adding post-fill actions would mean that some protocols might not implement part of the official standard and be forced to reject intents with that field, which might be confusing.

Wouldn’t that already be the case if post-fill actions are specified in `orderData`, i.e. they have to reject the intent since they do not know about the `orderData` schema?

> maybe the right path is to have an extension specification

I do rather like the idea. To be honest, it doesn’t even have to be in the official specification, even a loose place for coordination I think would help implementors a lot to be compatible with each other. I do think it’s going to be hard to find a easily composable way of doing so. I.e. how do you express both an intent’s `orderData` implements both 0x01 and 0x02? You would probably have to then abi.encode both the identifiers and the data itself which can be a lot of data wrangling. We at Hyperlane had a somewhat similar problem when designing our `HookMetadata` which are also arbitrary bytes that different hooks can interpret differently, choosing the right trade-off between simplicity and expressiveness was definitely pretty hard.

> Only a fraction of that information is needed at fill time.

Thanks for the context on this one. Now seems obvious in hindsight ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

> You could just add an arbitrary bytes field and leave it up to the filler/protocol to figure all of this out but then that means the standard isn’t really saving the filler/protocol much in that case, while imposing this bytes field on all the protocols that don’t need this contextual info

That’s kind of the case already if this is not specified in the spec, right? The filler will need protocol/settlement contract specific context to know how to fill on the destination chain. This does seem very similar to the above `orderData` question. I think in this case, an empty `bytes` field seems maybe worth the cost for protocols that don’t need this info, but you are right that the benefit from slightly more structural prescription might still not be worth it.

I think for both cases, maybe enough standardization at the tooling level is sufficient, and does not need to reflect itself in the spec itself.

---

**ankitchiplunkar** (2024-07-15):

Why is the chainID not part of the Input struct (in ResolvedCrossChainOrder) and is a top level variable?

In a chain abstracted world user balances will be pulled parallely from several chains for the same order. So it makes sense have different chainIDs available for different inputs.

For context, ERC-5792 is also updating where they will specify chainID on a per-call basis and not use the same chainID for all the batches. [Quote from “Update EIP-5792: make atomicBatch chain-specific per-batch, not per-call (both in protocol messages and in normative prose) by bumblefudge · Pull Request #8626 · ethereum/EIPs”](https://arc.net/l/quote/ctyfkjqc)

---

**nicholaspai** (2024-07-24):

I’ve thought about how to respond to this a lot and I think ultimately I favor keeping `originChainId` at the top level of the Order struct.

The reason why is I think this standard is really designed to enable gasless cross chain intent orders and that means supporting AA frameworks with social momentum like Permit2 or 7702. I think using a single `originChainId` fits in best with these AA frameworks and is the easiest to support technically.

Also, I’m not sure in a vacuum how much I agree with this:

> In a chain abstracted world user balances will be pulled parallely from several chains for the same order.

I think supporting multiple input chain ids makes the filler’s job (i.e. of handling input chain finality, tracking input chain accounts, tracking input chain market prices, etc.) exponentially more difficult and my instinct is this won’t be a large enough use case. If 7683 gets widely adopted and it becomes very common for users to be able to declare intents gasless-ly, then wouldn’t they be *more* likely to consolidate all of their funds on to a single “home” chain and use it to fund actions on arbitrary destination chains?

Thoughts?


*(31 more replies not shown)*

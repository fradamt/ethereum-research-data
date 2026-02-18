---
source: magicians
topic_id: 8422
title: "Proposal: ERC20 bridge-mintable tokens"
author: frangio
date: "2022-02-24"
category: ERCs
tags: [token]
url: https://ethereum-magicians.org/t/proposal-erc20-bridge-mintable-tokens/8422
views: 2620
likes: 10
posts_count: 9
---

# Proposal: ERC20 bridge-mintable tokens

Standardizing bridges themselves and the end-to-end bridging process is a difficult and ambitious project. A [prior proposal](https://ethereum-magicians.org/t/outlining-a-standard-interface-for-cross-domain-erc20-transfers/6151) with this goal was not able to gain momentum.

The current proposal focuses more narrowly on standardizing the interface that a token has to implement in order to be used in a bridge system, which among other things requires the token to be mintable by the bridge.

**This is not yet an ERC. I’m looking to get input from the relevant parties and confirm willingness to implement this standard.** There are several discussion points listed below.

## Abstract

A standard interface for a bridge to interact with a destination ERC20 token. The scenario covered is that of a bridge where deposits on a source chain trigger minting on a destination chain.

## Motivation

Although bridges tend to have the ability to deploy an off-the-shelf ERC20 contract as the bridged counterpart of a particular token, a protocol may want its canonical bridged token to be a custom implementation or have a different set of features on top of the standard ones. In that case, if the protocol wants to make this canonical token available on multiple chains it will currently need to deploy a different version of the code to each chain, as bridges expect different interfaces of the token.

The goal of this proposal is to enable code portability for bridged ERC20 tokens, so that the same code can be deployed to different networks with zero changes.

## Specification

*As a strawman proposal, this is the interface currently used by Arbitrum.*

```auto
interface ERC20Bridged is ERC20 {
    function l1Address() external view returns (address);
    function bridgeMint(address account, uint256 amount) external;
    function bridgeBurn(address account, uint256 amount) external;
}
```

### l1Address

Returns the address of the L1 token that this one is a bridged version of.

This getter allows the bridge to verify that it is correct to mint the token for a deposit of a particular L1 token. It is needed because the address of the L2 token may be an input to the deposit operation, and not inferred from a one-to-one mapping.

### bridgeMint

Mints `amount` of the token and credits it to `account`.

### bridgeBurn

Burns `amount` of the token, deducted from the balance of `account`.

## Discussion

### Naming

#### l1Address

Optimism uses `l1Token`. The choice between “address” and “token” is minor, but I believe this standard should apply more broadly to protocols and bridges that are not strictly Layer 2s, so a different name would be more appropriate.

Additionally, even for a Layer 2 protocol, the name `l1Address` assumes assets are bridged from L1 to L2, and a standard interface should not assume this is the only possible bridging direction.

Some alternatives: `sourceToken`, `originToken`.

#### bridgeMint, bridgeBurn

Optimism uses `mint` and `burn`. What are the reasons each project went with their naming?

Polygon PoS Portal uses `deposit` and `withdraw`, which is different as it is meant to be called by the token holder themselves: `function withdraw(uint amount)`.

### Events

Arbitrum bridged tokens emit the standard ERC20 `Transfer` event. Optimism’s emit events `Mint` and `Burn` on top of `Transfer`. None of these events appear to be used as part of the bridge’s on-chain operation, though they may be used for off-chain monitoring.

Polygon’s PoS Portal uses standard `Transfer` events, and in fact relies on burn events to finalize withdrawals in Ethereum. This may be problematic as tokens could be burnable for reasons unrelated to withdrawals, so it may be advisable to instead rely on a special-purpose event.

An event for minting may also be useful for some bridge designs, so we might add two events:

```auto
event BridgeMinted(address indexed account, uint amount);
event BridgeBurned(address indexed account, uint amount);
```

### Generality

#### Multi-chain bridges

Could a bridge process deposits from multiple chains? If so, a bridged token may need to complement the address of the source token with the ID of the source chain.

```php
function sourceToken() view returns (address token, uint chainId)
```

#### Multi-bridge tokens

It’s not possible to force a token to be exclusively tied to a single bridge. Does this break any assumptions? Should a standard have an opinion about it?

Bridges that rely on burn events to prove withdrawals should consider this possibility. A burn should be somehow tied to a single bridge

#### Multi-source tokens

Could a token have multiple source tokens, possibly from multiple source chains? To support this scenario, instead of reporting a supported address as with `l1Address` the bridged token could offer a function to query whether a particular address is supported.

```php
function sourceToken(address token) view returns (bool);
function sourceToken(address token, uint chainId) view returns (bool);
```

### Mintable tokens

Is it ok if a bridged token is also mintable (on the destination chain) through other means?

## Backwards Compatibility

If we move forward with this proposal as an ERC, the resulting interface will likely be different from that implemented by bridges today. However, it seems all bridges are currently upgradeable, so there should be a backwards compatible upgrade path that bridge operators can agree to implement.

This appears simple enough by using ERC165 interfaces. Before executing a mint operation, the bridge can check using ERC165 if the standard interface is supported. If it is not supported, it can fall back to its legacy interface.

Similarly for withdrawals the bridge can support both interfaces.

If the withdrawal relies on the proof of an event, both the previous event as well as the standardized event could be supported. However, if the previously used event was a standard ERC20 `Transfer` event, both may be emitted at the same time and the bridge should make sure it only processes a withdrawal once.

## References

- Optimism L2StandardBridge
- Arbitrum L2ArbitrumGateway
- Polygon ChildChainManager

## Replies

**smartcontracts** (2022-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Optimism uses mint and burn. What are the reasons each project went with their naming?

Personally I like `bridgeMint` and `bridgeBurn` more simply because it makes clear that it’s a specific type of burn being performed by the bridge. Other ERC20 tokens may want `mint` and `burn` functions that have specific use-cases beyond the bridge (since these names are relatively common). So at least I’m on board for `bridgeMint` and `bridgeBurn`.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> An event for minting may also be useful for some bridge designs, so we might add two events:

If we’re going to have `bridgeMint` and `bridgeBurn` then I think separate mint and burn events (`BridgeMinted` and `BridgeBurned`) are appropriate.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> sourceToken

`sourceToken` is a great name, IMO.

---

**fredlacs** (2022-03-17):

> standardizing the interface that a token has to implement in order to be used in a bridge system

The standard is clear about encompassing tokens from bridges that leverage mints in the destination chain. But is the intention to mainly focus on tokens that are used in “protocol bridge” systems like Arbitrum and Optimism’s token bridges or is the intention for the scope to also cover tokens by other bridges (such as Hop and Nomad)? Some bridges like Connext’s nxtp don’t require a new destination token representation, but I believe Hop and Nomad both do (they mint a token then usually swap into the token representation that is minted by the “protocol bridges” ie the canonical representation).

> The goal of this proposal is to enable code portability for bridged ERC20 tokens

Imo the biggest win here is for tooling that integrates with the bridged tokens (ie offchain tooling / analytics / monitoring will be more portable). But agreed that easier portability for other devs wanting to integrate is also great.

> As a strawman proposal, this is the interface currently used by Arbitrum.

In terms of external interface this seems to work well, but more and more people have been relying on ERC20’s permit functionality ([ERC-2612: Permit Extension for EIP-20 Signed Approvals](https://eips.ethereum.org/EIPS/eip-2612)). I think it would be interesting to extend this standard to also include the permit function as part of the interface. We considered relying heavily on permits in our bridging flow (similarly to how most systems currently heavily rely on the approve/transferFrom flow).

Given the community sentiment towards adopting permit more and more (ie aave v3 has full permit support :D) I think it would be beneficial to also have this as part of the expected interface here.

> l1Address

We use this value mostly as an internal consistency check in the bridge. In my opinion, this is mostly a notion for the bridge itself - not the token. We also add it to the token as a consistency check, what would be the motivation for the standard to actually cover this? It could be more useful to instead expect the bridge to have something along the lines of `function getL1Address(address l2Token) external view returns (address)` or `function getSourceAddress(uint256 sourceChainID, address l2Token) external view returns (address)`. This approach might play along nicer with multichain bridges and the source token idea. Could be interesting if the proposal in general favored “source chain” language instead of L1 to play along better with multiple domains.

This also brings up a bigger question around division of concerns (what should live in the token or bridge). A relevant thing here is also the trust model around the data surfaced by either a token/gateway. For example, should you trust the name/symbol/l1Address a token tells you? Probably not. But if that information instead lives in the respective bridges, it might be easier to reason about (ie was this just randomly added in a constructor of the contract or actually sent over from L1 through a trustless bridge?).

> It’s not possible to force a token to be exclusively tied to a single bridge

That is true. In Arbitrum’s token bridging the invariant that is enforced is that a L1 token gets mapped deterministically into a single L2 token. It doesn’t make assumptions on if this L2 token understands or interoperates with multiple different bridges.

> Is it ok if a bridged token is also mintable (on the destination chain) through other means?

Users are already fundamentally trusting the token mechanics and implementation. In our bridging system we fully delegate all accounting to the token itself (we can do that since there is a 1 to 1 mapping from L1 to L2 token). The only assumption is that the L1 bridge will have enough collateral at the time of a user withdrawal.

What that means in practice is that it’s alright to have the token mintable by other destinations, as long as the mechanics of the overall system are consistent to ensure there is enough escrow to cover for L2 to L1 withdrawals when they happen.

An interesting question that shows up in the discussion of minting from multiple domains is the semantics of what “totalSupply” in a token actually means in each domain. If tokens can be minted in L1, L2 and some other domain it starts getting complicated to reason about.

> Events

To better accommodate for tokens with multiple domains/bridges it could be interesting to also include the address to which the token was minted.

Something along the lines of:

event BridgeMinted(address indexed bridge, address indexed account, uint amount);

Also worth noting that we would probably add this as a separate event in conjunction to the regular Transfer from zero to address on mint

> Backwards Compatibility

Sounds good, another caveat is the transition to the new expected events. They will only be available after block `x` (different x in each chain). It could be worth having a getter to specify the block from which each token started supporting this event to help offchain services that are attempting to consume this data. A pure getter could work here and would only affect the contract size limit (that I don’t think tokens are running into issues with currently).

H/T Chris, Harry Ng, and Daniel G for helping brainstorm through these ideas

---

**prestwich** (2022-03-17):

I’m afraid the cat is already out of the bag on this one. This standards process won’t be adopted by the bridges that already exist, and the decisions being proposed are generally poorly suited for them anyway.

Modeling off [this](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/):

**Some misconceptions engineers believe about bridges:**

- Bridges are between L1 and L2
- Bridges are 1:1 relationships between domains
- Domains use the EVM
- Domains have reliable ways to externalize information (“events”)
- Domains have a chainID
- ChainIDs are all unique
- Tokens are uniquely identified by a domain ID and an address
- Domains use addresses
- Addresses are 20-bytes
- Token & bridges devs know and care about EIP165
- Connext and Hop are bridges
- Tokens have exactly one canonical deployment (“source”)
- Canonical deployments don’t change over time
- Representational deployments don’t change over time
- ERC20 behavior is standardized
- Representational deployment behavior is standardized
- Relationships between representational and canonical deployments don’t change over time

---

**fredlacs** (2022-03-18):

I agree with many of the misconceptions raised here, but I believe that the proposed standard could still be quite useful with a narrow scope.

For example, targets ERC20 tokens with a particular focus on tooling compatibility and easy porting for devs integrating with token bridges from Ethereum to other EVM compatible chains.

The above probably still doesn’t tighten the scope enough but could be a good start.

---

**prestwich** (2022-03-18):

Well how much of the ecosystem do you want to exclude by tightening the scope? Something like 25-30% of bridge TVL is not Ethereum → EVM ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

---

**frangio** (2022-03-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fredlacs/48/5191_2.png) fredlacs:

> is the intention to mainly focus on tokens that are used in “protocol bridge” systems like Arbitrum and Optimism’s token bridges or is the intention for the scope to also cover tokens by other bridges (such as Hop and Nomad)?

My understanding is that there’s nothing special about a protocol’s official token bridge, so this standard should apply to any token bridge that uses minting. For Hop though, I see the tokens that it mints (“hTokens”) more like an internal representation, so I don’t think this standard would have to apply. Particularly because I don’t think projects would want or be able to deploy a custom implementation of the hToken interface.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fredlacs/48/5191_2.png) fredlacs:

> In my opinion, this is mostly a notion for the bridge itself - not the token. We also add it to the token as a consistency check, what would be the motivation for the standard to actually cover this?

This is a good point. I simply conceptualized this information as being the token’s, but it’s more a notion of the “contract” between the token and the bridge, and since this contract is implemented by the bridge it would also make sense to host the information there; the token is already trusting the bridge to follow the minting rules anyway. That said, the other reason I thought to put that information in the token is that it simplifies the deployment of the token: since the list of source-destination pairs should be permissionless, if it’s kept in the bridge it needs a function to register a pair and the destination token should be the one to invoke it, all of this is a more complicated protocol than just publishing a getter.

I had a better look at the Arbitrum bridge now and I see that this part works very different to Optimism’s.  On this point I like Optimism’s design better: it’s the destination token that decides what source token is accepted as “collateral”, and a one-to-many mapping is possible. In Arbitrum it seems the source token defines its one destination token, and it is a one-to-one mapping.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fredlacs/48/5191_2.png) fredlacs:

> An interesting question that shows up in the discussion of minting from multiple domains is the semantics of what “totalSupply” in a token actually means in each domain.

I think this standard should recommend that “totalSupply” be the circulating supply in the local chain only.

---

**frangio** (2022-03-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/prestwich/48/2870_2.png) prestwich:

> I’m afraid the cat is already out of the bag on this one.

Can you acknowledge/comment on the Backwards Compatibility section of the proposal? I’m arguing that bridges seem to still be upgradeable and that we’re still on time to define a standard and implement it. I imagine there are bridges that are not upgradeable, if you know any can you point those out so we can evaluate the impact on this standardization effort?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/prestwich/48/2870_2.png) prestwich:

> This standards process won’t be adopted by the bridges that already exist

What makes you think this? There are positive comments from Arbitrum and Optimism team members in this thread. I’m waiting for comment from the Polygon team. (I realize there are more bridges than these.) This standard could help adoption of bridges and new chains by reducing the development effort required to deploy on them, so there are incentives to adopt it.

---

**frangio** (2024-11-28):

This is now finally happening with [ERC-7802](https://ethereum-magicians.org/t/erc-7802-crosschain-token-interface/21508).


---
source: magicians
topic_id: 6151
title: Outlining a standard interface for cross-domain ERC20 Transfers
author: maurelian
date: "2021-05-04"
category: EIPs
tags: [layer-2, interfaces]
url: https://ethereum-magicians.org/t/outlining-a-standard-interface-for-cross-domain-erc20-transfers/6151
views: 4722
likes: 27
posts_count: 9
---

# Outlining a standard interface for cross-domain ERC20 Transfers

*Written in collaboration with [Ben Jones](http://github.com/ben-chain).*

The proliferation of L2s and sidechains means that assets must be represented and moved between different environments.  This post outlines how we at Optimism are defining interfaces for

1. looking up where to go, and
2. interacting with the contracts which will allow assets to be moved between chains.

This post outlines Optimism’s current work, and requests feedback from the community on how to correctly bridge L2 assets to L1.

**Terminology note:**

- we use the term cross-domain transfer to refer to the action of moving an asset between two asynchronous state spaces, such as L1 and Optimistic Ethereum.
- a gateway contract is one that receives and dispenses a token and facilitates the transfer to the cross-domain.

## Motivation

Multiple layer 2 solutions are currently being developed in parallel. There are also bridges to completely distinct layer 1 sidechains. Many projects currently operating on L1 will wish to operate on L2, or at least allow their token to be transacted on L2.

We are seeking to establish two simple standard interfaces for:

1. A pairing of gateway contracts (one on each domain) which will accept a “canonical” token address (e.g. the main L1 contract) on one domain, and express the L2 representation of the same token on the other domain.
2. A single registry, which maps a token address to the correct gateway contract that should be used for a cross-domain transfer.

The standard we are aiming for **does not need to satisfy all use cases**, nor include every possible feature. The simplicity and extensibility of EIP-20 itself should be used as a guiding reference.

Important properties we are aiming for include the *canonicality of token pairings*, and *cross-chain composability*.

### Canonicality of token pairings

Given a token on L1, there should be a clear way to define the source of truth about the address of the token on L2. By extension, the total supply of the token on L2 should be equivalent to the amount of the token deposited to the Gateway contract on L1.

We want to avoid situations where there is confusion about the correct address for the L2 counterpart to an L1 token.  However, we also want to avoid situations where a single contract handles deposits for all token types in the same way, as some tokens require custom L2 implementations which cannot be solved with any one bridge model.  Thus, we define a standard registry interface as opposed to a monolith contract.

### Composability

Projects and users are interested in more interesting actions than simply transferring funds between accounts. Proposals have included using a  `transferToAndCall` pattern, which would execute a call to the receiver’s address on the cross-domain (ie. `receiver.call(data)`) upon finalization of the transfer.

For simplicity and safety, we have elected for a more conservative approach.  Instead of having a contract on the receiving domain execute a call, we pass an `address from` and `bytes data` field through deposits.  Subsequently, the `data` and `from` fields of a deposit may be verified against the state of the recipient domain in a separate transaction.  We believe this affords the extensibility of having calldata to pass around, without the security risk of unexpected external calls.

## Specification

### Registry Interface

To define a standard way to list tokens and their corresponding gateways, without enshrining a single implementation of the bridge itself, we define a getter interface which can retrieve the address of the cross-domain gateway for a given ERC20 asset.

```jsx
contract Registry {
	/// returns the chain ID of the xDomain
	function crossDomainID() returns(uint256)

	/// returns the address of the token's counterpart on the xDomain
	function tokenToGateway(address token) external view returns (address)

	/// returns the address on this domain of an xDomain token
	function gatewayToToken(address counterpartToken) external view returns (address)

}
```

*Note: this interface has been expressed above in Solidity, but some community members have expressed that this might be better as an off-chain data source, similar to Uniswap’s TokenLists.  **We would especially love input on this from the community!***

### Gateway Interface

Gateways live on each domain, and together form a pair which communicate to each other across domains.  One gateway (e.g. an L1 deposit contract) will normally interact with the “real” token, locking and unlocking funds as they are transferred away and returned, respectively.  The other gateway (e.g. the L2 contract) holds special privilege over an L2 ERC20 address, minting and burning tokens as they are received and transferred.

Note that the terminology here is domain-agnostic, ie. it avoids terms like ‘deposit’ and ‘withdrawal’, so that we can use the same interface on L1 and L2 for transferring back and forth. We hope that this is more future proof, for a world where assets are transferred not only between L1 and L2, but between different L2s.

```jsx
interface TokenGateway {

    /**********
    * Events *
    **********/

    /**
    * @dev This emits when a token transfer to the cross-domain is initiated.
    * @param _from Address tokens are sent from on this domain.
    * @param _to Address that will receive the tokens on the cross-domain.
    * @param _amount Amount of the token to transfer.
    * @param _data Data provided to the cross-domain.
    */
    event OutboundTransferInitiated(
        address indexed _from,
        address indexed _to,
        uint256 _amount,
        bytes _data
    );

    /**
    * @dev This emits when a token transfer from the cross-domain is paid out on this domain.
    *    ie. in finalizeInboundTransfer().
    * @param _from Address tokens were sent from on the cross-domain.
    * @param _to Address that received the tokens on this domain.
    * @param _amount Amount of the token to transfer.
    * @param _data Data provided from the cross-domain.
    */
    event InboundTransferFinalized(
        address indexed _from,
        address indexed _to,
        uint256 _amount,
        bytes _data
    );

    /********************
    * Public Functions *
    ********************/

    /**
     * @returns The address the corresponding gateway on the xDomain
     */
    function counterpartGateway() returns(address);

    /**
     * @notice Transfers a token to the same address as msg.sender on the cross-domain.
     * emits an OutboundTransferInitiated event.
     * @param _amount Amount of the ERC20 to deposit.
     * @param _data Data provided to the cross-domain.
     */
    function outboundTransfer(
       uint _amount,
       bytes calldata _data
    )
      external;

    /**
     * @notice Transfers a token to another address on the cross-domain
     * emits a TransferredOver event
     * @param _to Address on cross domain to transfer to.
     * @param _amount Amount of the ERC20 to transfer.
     * @param _data Arbitrary data with additional information for use on the cross-domain.
     */
    function outboundTransferTo(
        address _to,
        uint _amount,
        bytes calldata _data
    )
        external;

   /*****************************
    * Cross-chain Functions *
    *****************************/
    /**
     * @notice Finalizes one or more transfers initiated on the cross-domain
     * emits a FinalizedReturn event.
     * @param _to Address to transfer the token to.
     * @param _amount Amount of the ERC20 to transfer.
     * @returns _from Address of the sender on the cross-domain.
     * @returns _data Data with additional information for use on the cross-domain.
     */
    function finalizeInboundTransfer(
        address _to,
        uint _amount
    )
      external
      returns
    (
        address _from,
        bytes memory _data
    )
}
```

A reference implementation of the current proposal can be found [here](https://github.com/ethereum-optimism/optimism/blob/refactor/622/gateway/packages/contracts/contracts/optimistic-ethereum/OVM/bridge/tokens/OVM_L2TokenGateway.sol).

## Community Request

We hope that this post can serve as a starting point for community discussion on token bridging interfaces and standards.  As more and more L2s appear, it is important that we get this right.  So, please tear it apart! ![:grinning_face_with_smiling_eyes:](https://ethereum-magicians.org/images/emoji/twitter/grinning_face_with_smiling_eyes.png?v=15)

## Replies

**TransmissionsDev** (2021-05-04):

Excited to see this stuff standardized!

Here are my unsolicited thoughts:

- I still believe a transferAndCall pattern is much more useful and a much better UX (requires some off chain logic otherwise along with adding additional parameters on functions to fetch the right data). The risk vector seems super mild (reentrancy) considering  you can just slap a nonReentrant modifier on it.
- The registry interface is great for users/devs, in terms of maintainers I’m not sure who would want to be maintaining those as it would probably be very expensive and whoever had admin control would be a serious target and hold a lot of power. Off-chain tokenlists are likely more scaleable and secure, however it would require user input which costs additional gas to ingest.

Only other thing I would comment on is standardizing the ‘semi-canonical’ bridges that a lot of rollups are considering? I know Arbitrum has a recommended/default tokenbridge and the ‘unibridge’ (david mihal) has been proposed and I believe accepted by the Optimism community. Ensuring those standards are aligned seems important.

---

**maurelian** (2021-05-05):

Good points thx!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/transmissionsdev/48/3876_2.png) TransmissionsDev:

> I still believe a transferAndCall pattern is much more useful and a much better UX (requires some off chain logic otherwise along with adding additional parameters on functions to fetch the right data). The risk vector seems super mild (reentrancy) considering you can just slap a nonReentrant modifier on it.

Noted ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/transmissionsdev/48/3876_2.png) TransmissionsDev:

> Only other thing I would comment on is standardizing the ‘semi-canonical’ bridges that a lot of rollups are considering?

Yes, there is a lot of demand for this. I think the standard could be adapted to that fairly simply by adding another `address` arg (or two in the case of an off-chain registry) to the transfer functions.

---

**maurelian** (2021-05-06):

I thought it might be to summarize what I see as two more or less orthogonal decisions:

### 1. Multiple gateway contracts vs a single one

In either case, tokens are escrowed on their ‘home domain’, and minted/burned on the destination domain.

With **multiple gateways**, each gateway contract can thus be managed/promoted by individual projects. The primary benefit here is control, in that gateways can be upgraded separately, or not be upgradable at all.

With a **single gateway**, projects have less overhead, and there is more clarity about the correct address of the gateway. Projects also have less control, and it’s more difficult to opt-out if they have special needs. This approach also has a somewhat higher risk of confusing people in the case that a project elects to use their own gateway.

This spectrum of control is what necessitates a choice in the next set of trade offs.

### 2. Registry vs token lists

Perfect summary:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/transmissionsdev/48/3876_2.png) TransmissionsDev:

> The registry interface is great for users/devs, in terms of maintainers I’m not sure who would want to be maintaining those as it would probably be very expensive and whoever had admin control would be a serious target and hold a lot of power. Off-chain tokenlists are likely more scaleable and secure, however it would require user input which costs additional gas to ingest.

---

**Dzack23** (2021-05-06):

*written in collab w/ [@fredlacs](/u/fredlacs)*

Thanks [@maurelian](/u/maurelian) and Ben for the write-up and the initiative!

First off, definitely in full support of increased efforts to coordinate standards like this across L2s. Moving to the domain-agnostic semantics (away from deposits/withdrawals) makes a lot of sense and is a refactor we’d be happy to do, and will esp. be nice when we get to cross-shard territory.

Some thoughts:

- R.e. the multiple vs. single Gateway question (i.e., single gateway contract on a given domain, vs. a gateway contract per token per domain): given that projects are handling this differently, I think the important practical thing is to just have the TokenGateway interface allow for both models; allowing for this is as simple as adding a tokenContractAddress param to the three transfer methods - this adds negligible overhead to gateways that support a single asset and you can require the expected tokenContractAddress to ensure correctness.
 To add some color to Arbitrum’s token bridging architecture: we have a single “TokenGateway” contract on L1. It has two modes of operation for bridging tokens: standard & custom.
The standard mode deploys a template “StandardArbERC20” on the L2 (OZ ERC20 with additional methods: transferAndCall for UX and mint/burn for cross domain transfers). The standard bridging deploys the L2 pair at a deterministically generated address (mechanism similar to the uni bridge proposal - H/T dmihal.
The custom mode allows for deploying the L2 side manually (with a bare minimum expected interface). This allows for tokens with special requirements to still use our “effectively canonical” bridge, and thus still opt-in to our on-chain address oracle (about which, see below!)
- When creating the equivalent of outBoundTranfers in Arbitrum we took a slightly different approach that would require two extra parameters added to the interface.
 If we assume the outBoundTranfers is targeting a chain which is resource constrained and uses a congestion auction mechanism (ie gas price / limit) it would be cool to also parametrise this in the call. For example, if you have a tx initiated by an L1 contract to an L2 contract, it still needs to participate in Arbitrum’s congestion auction. Specifying gas price / limit lets us fund and execute on the destination “automatically” or leave it as an open bid in an execution market.
 We could decode the gas values from the data field, but this would incur extra costs when tbh I expected most chains to have this notion or something similar. Would be good to compare notes on how Optimism / other L2s are thinking about this.
- We support the on-chain registry! To TransmissionsDev’s concerns, a registry doesn’t in principle have to allow for any admin control, or any manual updating; i.,e Arbitrum’s only assumes users already know/trust the L1 token contract address, and from there the mapping is fully deterministic. Other projects may prefer a system that involves some active maintenance, but we think the benefits to other dapps of having on-chain address oracles will be big and outweigh those inconveniences.
- Despite the general desire for “effectively canonical” TokenGateways/Registry, some projects (I think) will actually require their own, distinct bridging system, i.e., hop.exchange has already built their own L1/Arbitrum and L1/Optimism bridges, which in their case was (I think) necessary for them to achieve their desired more-aggressive finality time. Thus, maybe it’s worth adding some sort “bridgeName” to Registry to distinguish multiple bridges across the same domain pairings (tho tbh they obviously live at different addresses, so maybe that’s enough).
- Little thing, but we could use the additional bytes param in finalizeInboundTransfer as well

---

**luzius** (2021-05-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/transmissionsdev/48/3876_2.png) TransmissionsDev:

> I still believe a transferAndCall pattern is much more useful and a much better UX

+1 for transferAndCall

---

**akolotov** (2021-05-08):

Thanks for the proposal!

How about the destination L2/sidechains which support another address notations? Should be `_to` is bytes32 at least in this case assuming that in the worst case it contains `keccak256` of a recipient address located in `_data`?

I agree with [@Dzack23](/u/dzack23) that `finalizeInboundTransfer` must accept the additional bytes param. BTW may you also share more details (since the reference implementation you mentioned is not available by the link) what is `_from` and `_data` returned by this method, where did they come from?

Since you assume that pure ERC20 tokens can be locked on the gateway, I agree that the `transferAndCall` functionality cannot be utilized. So, probably it make sense to introduce a special method on the side which could be the tokens recipient like `onTokensBridged(address _tokenContract, bytes32 _from, uint256 _value, bytes _data)`, doesn’t it? This method will be called from the contract-recipient by the gateway after unlocking/minting the tokens.

Another suggestion could be to consider a method in the standard to support a batching transfer. It could be useful for the cases when several users delegate transfers of different tokens from L2/sidechain to a service to reduce impact of L1-L2/sidechain interactions specific (like timelocks, gas prices etc).

---

**maurelian** (2021-05-11):

Just dropping in here to say thanks to everyone for their feedback!

Especially [@dzack23](/u/dzack23) for the detailed write up, and [@akolotov](/u/akolotov) for some thoughtful points. I’ll be working on a revision based on the input here, and from other sources.

---

**frangio** (2021-12-17):

Hi all. I’d love to see this initiative resumed. However, standardizing the entire cross-domain transfer process looks like it will be really difficult, so I want to propose focusing on a small subset of it, and **only standardize the interface that is required by an ERC20 contract to be mintable by a bridge**. I think this can be a great start.

[Optimism](https://github.com/ethereum-optimism/optimism/blob/ff5a87fcc69f15656e8334c253b0a5ecba1dfa1d/packages/contracts/contracts/standards/IL2StandardERC20.sol) and [Arbitrum](https://github.com/OffchainLabs/arbitrum/blob/9db8f48b5a2701861dd9677bc43cfcf7478caea0/packages/arb-bridge-peripherals/contracts/tokenbridge/arbitrum/IArbToken.sol) are *so* close on this, and yet different:

```auto
// Optimism
interface IL2StandardERC20 {
    function l1Token() external returns (address);
    function mint(address _to, uint256 _amount) external;
    function burn(address _from, uint256 _amount) external;
}
```

```auto
// Arbitrum
interface IArbToken {
    function l1Address() external view returns (address);
    function bridgeMint(address account, uint256 amount) external;
    function bridgeBurn(address account, uint256 amount) external;
}
```

It would be amazing if we could settle on a common interface with common expectations of behavior, requirements, events, etc. The value that I see in this is that projects will be able to deploy the same code on multiple networks.

Is this feasible? Could Optimism, Arbitrum, and other networks adopt a standardized interface?


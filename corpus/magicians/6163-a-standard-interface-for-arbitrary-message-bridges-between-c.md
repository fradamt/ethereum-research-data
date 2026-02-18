---
source: magicians
topic_id: 6163
title: A standard interface for arbitrary message bridges between chains/layers
author: auryn
date: "2021-05-05"
category: EIPs
tags: [layer-2, interfaces]
url: https://ethereum-magicians.org/t/a-standard-interface-for-arbitrary-message-bridges-between-chains-layers/6163
views: 2834
likes: 10
posts_count: 10
---

# A standard interface for arbitrary message bridges between chains/layers

As the L2 and sidechain ecosystem grows, it will become increasingly useful for accounts to be able to pass messages between environments.

Recently, [@maurelian](/u/maurelian) suggested a [standard interface for cross-domain ERC20 transfers](https://ethereum-magicians.org/t/outlining-a-standard-interface-for-cross-domain-erc20-transfers/6151). In this post, I suggest that similar standardization for cross-domain messages would be useful.

There is some early discussion in this [Twitter thread](https://twitter.com/auryn_macmillan/status/1389594385604653060), but since no one has mentioned an existing standard yet, I figured I’d kick off a discussion here.

# Motivation

There are multiple layer 2 and sidechain solutions being developed in parallel or already in production. Several have already developed systems for passing messages between their network and others (for example: [xDai’s AMB](https://docs.tokenbridge.net/eth-xdai-amb-bridge/about-the-eth-xdai-amb), [Matic’s Data Tunnel](https://docs.matic.network/docs/develop/l1-l2-communication/data-tunnel/), and [Abitrum’s EthBridge](https://developer.offchainlabs.com/docs/l1_l2_messages)). However, their interface’s are inconsistent, which creates an unnecessarily complicated user/developer experience.

This proposal seeks to establish a standard interface to be used for passing messages between environments.

The proposal **does not** seek to standardize the method by which messages are validated, this should be at the discretion of the implementation.

# Specification

*Note: this is rough and will probably need to be revised*

```solidity
interface messageBridge {

    /**********
    * Events *
    **********/

    /*
    @dev Emits when a new message is created
    @param from Address that called passMessage() on source chain
    @param to The address that the message should be passed to on the destination chain
    @param chainId The ID of the destination chain
    @param data The message to be passed
    */
    event newMessage(
        address from,
        address to,
        uint256 chainId,
        bytes32 messageId,,
        bytes data
    );

    /*
    @dev Emits when a new proof is published
    @param messageId ID of the message the proof is for
    @param proof Proof that the message is valid, to be used as the _proof parameter for executeMessage()
    */
    event newProof(
        bytes32 messageId,
        bytes32 proof
    );

    /*
    @dev Emits when a message is executed
    @param from Address that called passMessage() on source chain
    @param to The address that the message was passed to on the destination chain
    @param chainId The ID of the source chain
    @param data The message that was passed
    */
    event messageExecuted(
        address from,
        address to,
        uint256 chainId,
        bytes32 messageId,
        bytes data
    );

    /********************
    * Public Functions *
    ********************/

    /*
    @dev Passes a message from source chain to destination chain and returns a unique message ID
    @param _to The address that the message should be passed to on the destination chain
    @param chainId The ID of the destination chain
    @param data The message to be passed
    @returns _messageId unique ID for this message
    */
    function passMessage(
        address _to,
        uint256 _destinationChainId,
        bytes memory _data
    )
        external
        returns (bytes32 _messageId);

    /*
    @dev asks the contract for proof that a given message is valid
    @param _messageId ID of the message to be validated
    @notice This may be called on the source or destination chain, depending on the implementation
    */
    function requestProof(
      bytes32 _messageId
    )
        external;

    /*
    @dev Returns proof that a given message is valid
    @param _messageId ID of the message to be validated
    @returns _proof Proof that the message is valid, to be used as the _proof parameter for executeMessage()
    @notice This may be called on the source or destination chain, depending on the implementation
    */
    function getProof(
        bytes32 _messageId
    )
        external
        returns (bytes32 _proof);

    /*
    @dev Executes a given message on destination chain, only if the given proof is valid
    @param _from The address that called passMessage() on the source chain
    @param _to The address that the message should be passed to on the destination chain
    @param _chainId The ID of the source chain
    @param _data The message that was passed
    @param _proof Proof that the message is valid
    */
    function executeMessage(
        address _from,
        address _to,
        uint256 _sourceChainId,
        bytes memory _data,
        bytes32 _proof
    )
        external;
}

```

# Request For Feedback

This proposal is early and quite rough. Constructive feedback would be very much appreciated. Have at it!

## Replies

**akolotov** (2021-05-05):

[@auryn](/u/auryn) thanks for proposal! May you extend the specification with actors like a cross-chain bridge contract, an originating contract, a terminating contract? Which contract should support the corresponding function or emit the corresponding message?

---

**auryn** (2021-05-05):

In the specification, I assumed that these bridges are multi-directional, so the contracts on each side should expose all of these functions.

Essentially, the same contract can be both origin and destination, depending on which direction the message is going.

---

**maurelian** (2021-05-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/auryn/48/1044_2.png) auryn:

> In the specification, I assumed that these bridges are multi-directional, so the contracts on each side should expose all of these functions.

This is the way! Symmetrical bridges mean we can reuse similar tooling and contracts to interact with them on either of the domains.

---

**akolotov** (2021-05-08):

Thanks! I completely support that the bridges are multi-directional. My question was about more details for the events and functions you proposed in standard.

For example, the method `passMessage` is called by the originating contract or EOA from the bridge contract, right? The method `executeMessage` is called also from the bridge contract by an oracle (EOA, a dedicated oracle or a flashbot) or by relaying contract (e.g. GSN), right?

But so far I don’t understand who and when should call `requestProof`.

I have few initial suggestions:

1. Consider to not extract from, to and chainId from the data field of the message. The originator (from) and the terminator (to) of the message could be in the chains/layers which have different address notation. Keeping 256 bits for the chain id is also overhead in most of cases, so, it makes sense to pass it in encoded form like 1 byte of chain id length + shortened chain id in big endian.
2. The message id must be part of the executeMessage call, it will allow making unique messages even if from, to, source chain id and data are the same.
3. It makes sense to emit the message id as part of newMessage or messageExecuted. It will simplify the tracking between messages requested to be passed and executed messages.
4. In some chains/layers the proof could be too big so do we really need to publish it in the newProof event? In some cases, the proof could be generated offchain (e.g. a threshold signature scheme or snark) so it will be overhead to register it on chain so it will be impossible to request it through the getProof method.
5. The standard also must specify the cases when executeMessage fails. For example, we can consider two options: executeMessage and safeExecuteMessage (or a special flag can be used to differentiate the outcome). In the case of executeMessage the transaction will not fail if the message reverted – it could be required for the cases when an automated oracle is responsible for delivering the messages to the destination chain, it must not stuck on attempts to execute the message again and again. At the same time, if the message is delivered by EOA it must have an ability to execute the message again if it failed by some reason (e.g. due to large slippage on AMM).
6. I would also introduce a method requestInfo:

```auto
function requestInfo(
    uint256 _destinationChainId,
    uint256 _callback,
    bytes memory _data
)
    external
    returns (bytes32 _messageId);
```

 The idea of this method is to get some information from the destination chain. The version 2 of ABI allows to encode JSON requests. So, this method could request both data from a specific contract and blockchain data like getLogs, getTransactionReceipt, getStorageAt, getTransactionByHash etc.

---

**auryn** (2021-05-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akolotov/48/3888_2.png) akolotov:

> For example, the method passMessage is called by the originating contract or EOA from the bridge contract, right?

Correct. The originating account calls `passMessage()` on the origin chain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akolotov/48/3888_2.png) akolotov:

> The method executeMessage is called also from the bridge contract by an oracle (EOA, a dedicated oracle or a flashbot) or by relaying contract (e.g. GSN), right?

`executeMessage()` should be a public function that any account can call.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akolotov/48/3888_2.png) akolotov:

> But so far I don’t understand who and when should call requestProof.

I think this really depends on the implementation.

The sequence that I predict is:

```auto
passMessage() --> requestProof() --> getProof() --> executeMessage()
  [origin]          [either]          [either]      [destination]
```

Depending on the implementation, request and get proof may be called on one, the other, or both origin and destination, or might be redundant.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akolotov/48/3888_2.png) akolotov:

> Consider to not extract from, to and chainId from the data field of the message. The originator (from) and the terminator (to) of the message could be in the chains/layers which have different address notation.

This is a really valid point that I hadn’t considered. I guess I was operating under the assumption that these bridges would only pass messages between EVM compatible chains/layers with the same address and chain format. I do still think it’s worthwhile extracting them from the data, as it will likely lower the barrier to entry for developers. But perhaps a more generic data type would be more suitable, `bytes32` for instance.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akolotov/48/3888_2.png) akolotov:

> Keeping 256 bits for the chain id is also overhead in most of cases , so, it makes sense to pass it in encoded form like 1 byte of chain id length + shortened chain id in big endian.

Also very valid. I do worry that this would increase the difficulty for developers to use the tool. Would a suitable compromise be to use a smaller namespace, `uint32` perhaps?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akolotov/48/3888_2.png) akolotov:

> The message id must be part of the executeMessage call, it will allow making unique messages even if from, to, source chain id and data are the same.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akolotov/48/3888_2.png) akolotov:

> It makes sense to emit the message id as part of newMessage or messageExecuted. It will simplify the tracking between messages requested to be passed and executed messages.

Great points! I’ll modify the OP to reflect these changes.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akolotov/48/3888_2.png) akolotov:

> In some chains/layers the proof could be too big so do we really need to publish it in the newProof event? In some cases, the proof could be generated offchain (e.g. a threshold signature scheme or snark) so it will be overhead to register it on chain so it will be impossible to request it through the getProof method.

Hhhmm. The I’m not suggesting that in cases like this the actual proof needs to be published on chain, `getProof()` simply needs to return some value that can be used as input to `executeMessage()` so it can validate that the message should be executed.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akolotov/48/3888_2.png) akolotov:

> The standard also must specify the cases when executeMessage fails. For example, we can consider two options: executeMessage and safeExecuteMessage

I’m not sure I agree that both options are needed. My assumption is that the `executeMessage()` operates as you described `safeExecuteMessage()`; it fails if reverted. In the case of an oracle, it should be up to the oracle to handle reverts.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/akolotov/48/3888_2.png) akolotov:

> I would also introduce a method requestInfo:

How would the method fetch the data? Perhaps with something like the [general-purpose bridge for Ethereum L2s](https://medium.com/the-ethereum-name-service/a-general-purpose-bridge-for-ethereum-layer-2s-e28810ec1d88) suggested by [@vbuterin](/u/vbuterin) and [@Arachnid](/u/arachnid) ?

Thinking about it more, perhaps [@Arachnid](/u/arachnid)’s design makes this whole exercise redundant? ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

---

**Arachnid** (2021-05-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/auryn/48/1044_2.png) auryn:

> Thinking about it more, perhaps @Arachnid’s design makes this whole exercise redundant?

If I understand what you’re working on here correctly, it’s a standard for the format of messages to be passed to contracts/etc at different layers? If so, I think it’s orthogonal to what we’re working on.

---

**auryn** (2021-05-18):

Yeah, I think you’re right. But if i understand what you’ve described, it could be used to build what I’ve described.

---

**drinkcoffee** (2021-07-14):

GPACT ([GitHub - ConsenSys/gpact: General Purpose Atomic Crosschain Transaction Protocol](https://github.com/ConsenSys/gpact) and [[2011.12783] General Purpose Atomic Crosschain Transactions](https://arxiv.org/abs/2011.12783)) is a protocol to allow function calls across blockchain / sidechains / rollups, where the updates are atomic: either being committed or discarded on all chains. As long as Ethereum Events can be proven to have been generated on one chain using threshold signing, threshold signing with slashing, some sort of zk scheme, something else, then the protocol can be used to bridge multiple chains all in the one crosschain function call.

I think GPACT is a competing technology to this proposal. It provides atomicity. However, this proposal is simpler. Is that your take [@auryn](/u/auryn) ?

---

**auryn** (2021-07-15):

I was not aware of GPACT, thanks for sharing!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/drinkcoffee/48/1850_2.png) drinkcoffee:

> I think GPACT is a competing technology to this proposal. It provides atomicity. However, this proposal is simpler. Is that your take @auryn ?

At first glance, it looks like a protocol implementation, rather than a standard. So I don’t think it competes with what I’m suggesting. However, since they have likely put a lot more thought into this than I have, it might be worth using their implementation as a reference for this standard.


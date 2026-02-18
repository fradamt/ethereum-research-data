---
source: ethresearch
topic_id: 21673
title: "ULTRA TX - Programmable blocks: One transaction is all you need for a unified and extendable Ethereum"
author: Brecht
date: "2025-02-05"
category: Layer 2
tags: []
url: https://ethresear.ch/t/ultra-tx-programmable-blocks-one-transaction-is-all-you-need-for-a-unified-and-extendable-ethereum/21673
views: 1295
likes: 19
posts_count: 12
---

# ULTRA TX - Programmable blocks: One transaction is all you need for a unified and extendable Ethereum

[![image](https://ethresear.ch/uploads/default/optimized/3X/5/5/5518bc25ab9f9220e9da5a3e79b13136483340d1_2_500x500.jpeg)image1024×1024 185 KB](https://ethresear.ch/uploads/default/5518bc25ab9f9220e9da5a3e79b13136483340d1)

# What

ULTRA TX is a way to achieve programmable L1 blocks, unlocking capabilities well beyond what is possible using standard L1 transactions in an L1 block. You could say ULTRA TX is to blocks what account abstraction is to EOAs.

This post will focus on what this means for L2s and the interoperability between L1 and L2s. Other possible use cases will not be explored here.

When you combine the L1 meta tx bundler and the (based) rollup block builders, you have an entity we’ll call the master builder. The master builder will build L1 blocks containing just a single extremely powerful and fat L1 transaction. This single transaction will henceforth be referred to as the ULTRA TX.

This setup makes it efficient and straightforward to do composability and aggregation for L2s and the L1.

For easy L1 composability, the ULTRA TX should be at the top of the L1 block so that the latest L1 state is directly available.

This approach requires no changes to L1.

# Why

- Enforcing things across transactions is a nightmare and often simply impossible.
- Doing L1 → L2 (like deposits) with EOA transactions is very inconvenient, especially for synchronous composability. See below why.
- All (or almost all) L1 transactions will be account abstraction transactions. EOA transactions are limited and should gradually go away. Not just for the UX improvements but also for efficiency. Having a smart contract based account with EIP-7702  is now also just a signature away, so easy for users to opt in.
- L2s want to propose/settle together (to share blobs and proof aggregation) and frequently (each L1 block ideally) for efficiency and UX.
- A more extendable L1 paves the way for better UX
- One account abstraction tx bundler on L1 is the most efficient.
- One block builder for all (based) rollups is the most powerful.

For these reasons I believe we are moving towards a future where almost everything will be done by a single L1 transaction. ULTRA TX can be adopted gradually, the rest of the block can be built in the traditional way.

Together with real time proving (in some reasonable capacity), this can achieve the ideal future where Ethereum truly feels like a single chain, where L1 and all L2s can call into each other, and every L2 can (but does not need to) settle in each L1 block, generally without loss in efficiency.

Going forward, [Gwyneth](https://x.com/gwyneth_taiko) will often be referenced to make things more concrete on how things could actually work. This is simply because it is the one I am most familiar with.

# Advantages

- Seamless and simple aggregation and interaction between L1 and L2s: L1 and L2 transactions can be used to build blocks in practically the same way with a shared mempool. This removes complexity and efficiency considerations of having to handle L1 transactions differently. See below how this can be achieved.
- Shared data compression and data aggregation into blobs: All rollup data can be shared and stored in blobs together.
- Atomicity: There can now be programmable logic to enforce things across transactions. All logic can be implemented using smart contracts.
- Provability: The whole ULTRA TX can easily be proven because all the inputs are directly available. Anything happening within that requires to be proven can depend on it being proven, or the whole ULTRA TX reverts. This is a major improvement compared to normal transactions where you cannot enforce something across transactions.
- Efficiency: Everything that needs to be proven, can be proven with just a single proof. There is no overhead for storing or sending messages. L1 → L2 calls that have a return value are the exception, but these can use relatively cheap transient storage.
- Access to the latest L1 state: The ULTRA TX being at the top of the block is important so that the latest L1 state is directly available in the block header of the previous block. This avoids the difficulties/inefficiencies of getting/ensuring the latest L1 state at some random point in the L1 block (e.g. no need for EIP-7814 to be able to reason across transaction boundaries). Delayed state root calculation like in EIP-7862 should not have much impact because the blocks can still be built immediately after a new L1 block comes in. However, to be able to prove the L1 state the prover will have to have the Merkle proofs against that state root for all used state.
- Preconfirmations: Only top of block L1 “inclusion” preconfs are required for e.g. gateways to be able to provide L1 and L2 execution preconfirmations. It’s possible to check onchain that a transaction is the 1st transaction in a block using a trick: Set the tx gas limit to the block gas limit and check: block.gaslimit - gasleft() - intrinsic_gas_cost
Finally the proof is verified showing that everything was done as expected.

This extra data is generated and provided by the master builder, not by the user. The user doesn’t have to sign any additional data or verify expensive proofs. The user can interact with smart contracts using extended functionality exactly the same way the user interacts with native functionality.

Developers using the extended functionality in their smart contracts also do not have to know what is actually happening behind the scenes.

Note that this exact approach only works because Gwyneth can “simulate” the execution of L1 transactions to glue everything together. L1 transactions are executed in the prover the same way as they will be on L1 when the ULTRA TX is proposed. This is important to make sure that the correct inputs are used to generate the output.

# (Synchronous) Composability

[![image](https://ethresear.ch/uploads/default/optimized/3X/4/6/466285b38d168edd1e90f303045a8af0769cbb80_2_690x374.png)image1352×733 15.3 KB](https://ethresear.ch/uploads/default/466285b38d168edd1e90f303045a8af0769cbb80)

I will again be using Gwyneth’s approach to synchronous composability as an example (you can read up on it quickly [here](https://x.com/Brechtpd/status/1885346586542428577), but also [here](https://capricious-firefly-0c5.notion.site/Gwyneth-Technical-Design-86a8d1a151954f559f8124301bed1d46), [here](https://ethresear.ch/t/booster-rollups-scaling-l1-directly/17125), and [here](https://ethresear.ch/t/booster-rollups-part-2-zk-evm-as-a-zk-coprocessor/17279)). In short, an additional precompile is added on L2 that allows switching chains for external calls. Gwyneth can also simulate all L1 transactions and afterwards just apply the state updates back to L1.

The assumption I’m going to make here is that each L1 account is a smart contract account and that all L2s are based (such nice assumptions!).

Building blocks can now easily be done as follows:

- We start with the post state for each chain (including for L1). There is no difference between L1 and L2 transactions (except that L1 transactions should be meta transactions, if not they are added to L1 block after the ULTRA TX).
- The L1/L2 transactions are executed in any order the builder wants.
- For L1 transactions, the EVM execution is modified so that the XCALLOPTIONS precompile works exactly the same as on L2 (i.e. it actually executes the call on the target L2) as described above in the Extending L1 section. This allows L1 transactions to call into L2 which is something we need to support for true synchronous composability.
- For any L1 → L2 call, we record the corresponding output of the call.
- Once all required transactions are executed locally by the builder, we can seal the blocks:

For the L2s, either the transactions or the state delta is put on L1 for data availability. This is done for each L2 independently so that they don’t have any interdependencies. The block hashes can be put onchain aggregated to save gas.
- For L1, we need to apply all state changes in the expected order onchain as they happened in the builder. For Gwyneth, this means applying the L1 transactions and the L1 state deltas (for L1 state changes done from L2) in the correct order.

The building process can be repeated as many times as needed to produce any number of blocks. This can be important to support execution preconfs for the transactions that are being included at faster than L1 block times. It is also important to parallelize the block building (see below).

Finally, a single proof is generated of the whole process (note that this may contain sub-proofs, see the section on parallelization below).

The ULTRA TX is then finally proposed onchain. All inputs to the transaction are used as the input to the proof and the proof is verified. If the proof is not valid, the whole transaction reverts.

Note that any additional requirements a builder has to support to be able to correctly include a transaction can be made part of the meta data of the transactions. This way builders can easily see if they are able to include the transaction without having to execute it. These rules can be enforced onchain. For example, for a cross chain transaction the meta tx would contain a list of chains that are allowed to be accessed. If this list is incomplete, the transaction is allowed to revert with the builder getting the transaction fee.

# Parallelization

The simplified process above is strictly sequential to allow all chains to interact with each other freely and synchronously in the easiest way. It is possible to build blocks for any set of chains in parallel as well if they do not require synchrony with each other. Multiple blocks can be submitted with practically the same efficiency. This allows breaking the sequential bottleneck and allows achieving greater throughput.

Even if, for example, a chain has an L1 state dependency, it is also still possible to build blocks in parallel. Only the subset of the state used in the block is important to be the actual latest values for the block to be valid.

There can be an additional layer on top of these blocks tracking the global state, while each block only depends directly on this sub state. Each block is proven individually, and then afterwards aggregated together with the additional state checks. The aggregation proof will track the global latest state across blocks and will check that the local state used in the block matches the current latest global state. The builder just has to ensure that these assumptions hold while building the blocks in parallel.

# Generalization

The generalization of how this (and more) can be used for all rollups (not just Gwyneth ones) will be coming in part 2. This framework will be called GLUE. A previous sketch was done [here](https://www.notion.so/132d07a3da30809aa801e26077a49b60?pvs=21). It will contain, in reasonable depth, the interfaces necessary both offchain and onchain to make it possible for all L1 extensions to make use of the proposed design.

# Code

Some code to make things more concrete and fun. Some details were omitted for brevity.

What the ULTRA TX would look like onchain:

```auto
function proposeBlock(BlockMetadata[] calldata blocks) external payable {
    for (uint i = 0; i  0) {
                (bool success, bytes memory result) = address(extensionOracle).call(abi.encode(call.returnData));
                require(success == true, "call to extension oracle failed");
            }
            // L1 account abstraction call
            _tx.addr.call{value: call.value}(call.data);
        }
        // Apply L1 state diff if necessary
        if (_tx.slots.length > 0) {
            GwynethContract(_tx.addr).applyStateDelta(_tx.slots);
        }
    }
}
```

How it looks for developers that want to take advantage of extended functionality:

```auto
using EVM for address;

function xTransfer(uint256 fromChain, uint256 toChain, address to, uint256 value) public returns (uint256) {
    return on(fromChain)._xTransfer(msg.sender, toChain, to, value);
}

function ChainAddress(uint256 chainId, xERC20 contractAddr) internal view returns (xERC20) {
    return xERC20(address(contractAddr).onChain(chainId));
}

function on(uint256 chainId) internal view returns (xERC20) {
    return ChainAddress(chainId, this);
}
```

How extensions can be exposed to developers:

```auto
library EVM {
    function xCallOptions(uint chainID) public view returns (bool)  {
        // Call the custom precompile
        bytes memory input = abi.encodePacked(version, chainID);
        (bool success, bytes memory result) = xCallOptionsAddress.staticcall(input);
        return success && bytes4(result) == xCallOptionsMagic;
    }

    function onChain(address addr, uint chainID) internal view returns (address) {
        bool xCallOptionsAvailable = xCallOptions(chainID, false);
        if (xCallOptionsAvailable) {
            return addr;
        } else {
            return extensionOracle;
        }
    }
}
```

What the Extension Oracle looks like:

```auto
contract ExtensionOracle {
    uint private transient returndataCounter;
    ReturnData[] private transient returndata;

    fallback() external payable {
        _returnData();
    }
    receive() external payable {
       _returnData();
    }

    function _returnData() internal {
        if (msg.sender == gwyneth) {
            returndata = abi.decode(msg.data, (GwynethData.ReturnData[]));
        } else {
            require(returndataCounter < returndata.length, "invalid call pattern");
            ReturnData memory returnData = returndata[returndataCounter++];
            bytes memory data = returnData.data;
            if (returnData.isRevert) {
                assembly {
                    revert(add(data, 32), mload(data))
                }
            } else {
                assembly {
                    return(add(data, 32), mload(data))
                }
            }
        }
    }
}
```

## Replies

**dionysuzx** (2025-02-06):

how concerned are you that ultra tx requires top of block? as in do u think builders will find this more profitable than a standard that doesn’t use this? because it reduces entropy in the block at least outside of the ultra tx.

compared to something that tries to stitch together synchronous composability across the block between TXs or has some type of flexibility in where the ultra tx is in the block.

this sounds very attractive design wise, i’m wondering if it’s also going to be the most efficient MEV side as well.

also this TX is enormous right? is there anything weird with inclusion lists like will it still be enforced inside the ultra tx or will be outside?

---

**thegaram33** (2025-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/brecht/48/4820_2.png) Brecht:

> What the ULTRA TX would look like onchain

I noticed that there are two ways to modify L1 state:

- Execute call. I believe this can either be an L2 → L1 call, or the return part of an L1 → L2 call.
- Apply state diff.

When do you use one or the other? Can you share some examples?

And can this approach support more complex patterns, e.g. L1 → L2 → L1 → L2 → L1? In this example this would be broken down into 3 L1 transactions, but the proof of the Ultra Tx guarantees atomicity.

---

**Brecht** (2025-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/dionysuzx/48/19065_2.png) dionysuzx:

> how concerned are you that ultra tx requires top of block? as in do u think builders will find this more profitable than a standard that doesn’t use this? because it reduces entropy in the block at least outside of the ultra tx.

I’m now not concerned anymore because the ULTRA TX can itself contain any L1 transaction as one of it’s transactions. The only requirement is that those transactions need to be L1 account abstraction transactions and not simple EOA transactions.

So if L1 transactions are done from account abstraction accounts, there is no downside of the ULTRA TX being at the top of the block. The block builder can still include them anywhere inside the ULTRA TX (as in, they will be top of the block inside the ULTRA TX). So there should be no downsides.

![](https://ethresear.ch/user_avatar/ethresear.ch/dionysuzx/48/19065_2.png) dionysuzx:

> compared to something that tries to stitch together synchronous composability across the block between TXs or has some type of flexibility in where the ultra tx is in the block.

If all L1 transactions are account abstraction transactions ULTRA TX offers exactly the same flexibility, but without requiring the difficulties of cross transaction logic (requiring something like [EIP-7814](https://github.com/ethereum/EIPs/blob/1676c9451a75fd0740c65e7d1d5f18296d68a9a0/EIPS/eip-7814.md) for L1 state calculation efficiency). Splitting up the work across multiple transactions would also require verifying a proof for each part, which would be very bad for efficiency as well.

![](https://ethresear.ch/user_avatar/ethresear.ch/dionysuzx/48/19065_2.png) dionysuzx:

> this sounds very attractive design wise, i’m wondering if it’s also going to be the most efficient MEV side as well.

Same as above, if all L1 transactions are account abstraction transactions then certainly no loss in flexibility. Flexibility to extract value only increases by being able to also directly tap into L2s (and composability between everything)!

![](https://ethresear.ch/user_avatar/ethresear.ch/dionysuzx/48/19065_2.png) dionysuzx:

> also this TX is enormous right? is there anything weird with inclusion lists like will it still be enforced inside the ultra tx or will be outside?

That’s a good question! I think inclusion lists would only work on real L1 transactions so any account abstraction transaction would not benefit from it but I could be wrong.

---

**Brecht** (2025-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> I noticed that there are two ways to modify L1 state:
>
>
> Execute call. I believe this can either be an L2 → L1 call, or the return part of an L1 → L2 call.
> Apply state diff.
>
>
> When do you use one or the other? Can you share some examples?

Executing calls would mostly be done to just execute L1 meta transactions. These would still have full L1 security, the reason they are part of the ULTRA TX is that:

- The L1 state can be calculated offchain as well and proven because all L1 transactions are also known. This way L2 transactions can have access the latest L1 state at all times, even when mixing L1 and L2 transactions.
- The top of block requirements doesn’t matter anymore: L1 transactions that need to be done before anything else are now just “top of block” inside the ULTRA TX
- They are also useful to do L1 → L2 calls, or also L1 “sub call” that are done from L2, that would also require full L1 security.

The state diff approach is to make L1 state updates done from L2 as cheap as possible. Only the absolute minimal work is done onchain to update the L1 state, and you get free batching when using this (all state updates done to L1 from L2 are automatically minimized to the smallest possible state change set). This would be useful to batch 100s of trades on L2 against the same pool on L1, the state delta that needs to be applied onchain would just be a couple of storage slots.

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> And can this approach support more complex patterns, e.g. L1 → L2 → L1 → L2 → L1? In this example this would be broken down into 3 L1 transactions, but the proof of the Ultra Tx guarantees atomicity.

Yes! The first L1 part will always have to be done completely on L1 (otherwise whoever creates the transaction should start the tx on L2). The other parts that execute on L1 will have an option: execute the call on L1 or “simulate” the call on L1 with Gwyneth generating the state diff. Depending on what the goal is (security/efficiency) one or the other can be chosen.

---

**stanleykhe** (2025-02-10):

Do you think it will become a problem in the future when there are 1000s of rollups and a single master builder is required to sequence them all? Is it possible to loose the master builder requirement and still have ultra tx?

---

**pixelcircuits** (2025-02-10):

Can calls to the “extension oracle” be reverted if the calling context eventually reverts?

---

**Brecht** (2025-02-11):

I call it the master builder because, in the end, this entity will be able to decide what gets in the blocks. But that doesn’t necessarily need to mean that this entity actually also builds all the blocks!

It’s similar to based rollups where the L1 validator can in theory build all the blocks, but of course it’s others that do the actual building.

You can read “master builder” as the master of builders. The king of kings.

---

**Brecht** (2025-02-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/pixelcircuits/48/13336_2.png) pixelcircuits:

> Can calls to the “extension oracle” be reverted if the calling context eventually reverts?

Reverts are fully supported. Reverts are nothing special really, just a slightly different way you have to return the result of a call. The call is executed normally offchain and so both successful and reverted calls can easily be supported by storing the result of that. If you look at the attached code for the `ExtensionOracle` you can see how that’s done for the onchain part.

Even ETH carrying calls (`msg.value > 0`) can be supported, because ETH sent to L2 is now sent to the `ExtensionOracle`. This ETH can be locked up on L1 and minted on L2 to bridge it to L2.

---

**thegaram33** (2025-02-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/brecht/48/4820_2.png) Brecht:

> I call it the master builder because, in the end, this entity will be able to decide what gets in the blocks. But that doesn’t necessarily need to mean that this entity actually also builds all the blocks!

With Gwyneth, I understood that the builder of the next “super block” (analogous to ultra tx) is free to just care about a subset of all rollups and ignore any tx touching any other rollup, that makes sense.

But how would outsourcing different rollup blocks to different builders work here? Let’s say builder `bA` builds for rollup `rA`, and builder `bB` builds for rollup `rB`. `bA` packs a tx originated in `rA`. This tx then calls into `rB`, updating its state. Concurrently `bB` is building a `rB` block. This block might now be invalidated, since `rB`’s state is updated by `bA`.

---

**Brecht** (2025-02-11):

Right, so a couple of options.

Obvious way is to split things up on the rollup level where builders each get a set of mutually exclusive rollups they can build for. All sync composability between those sets of rollups would not be possible so not great.

Another way is to just let builders build upon all the state optimistically. Then it’s up to the master builder to pack the most valuable blocks that can be combined without conflict in the ULTRA TX (similar to how L1 block builders pack transactions).

But there’s no reason things can’t be made more flexible and predictable as explained in the parallelization section.

Builders just have to be careful that they don’t both modify the exact same data and create a conflict. This is on the account/storage slot level. Easiest way to achieve this is again to have some hard ranges each builder is allowed to modify so no conflicts are possible.

But, builders can also work together to build these blocks. So builder A can let builder B know it wants to modify the state, and then B can allow/disallow that when possible. As long as everything is executed in the correct order, the data consistency checks will pass and all is good. Note that this working together does depend on trust. However, if you run the builder in a TEE you could make certain things enforceable making it mostly trustless.

---

**linoscope** (2025-06-30):

Nice post!

![](https://ethresear.ch/user_avatar/ethresear.ch/brecht/48/4820_2.png) Brecht:

> The state diff approach is to make L1 state updates done from L2 as cheap as possible. Only the absolute minimal work is done onchain to update the L1 state, and you get free batching when using this (all state updates done to L1 from L2 are automatically minimized to the smallest possible state change set). This would be useful to batch 100s of trades on L2 against the same pool on L1, the state delta that needs to be applied onchain would just be a couple of storage slots.

Is my understanding correct that this requires L1 contracts to explicitly opt-in to accept the state-diffs from L2 proofs? And if the L1 contract does *not* opt to accept state-diffs from L2, you can still fall back to the “execute call” route to handle L2->L1 interaction?


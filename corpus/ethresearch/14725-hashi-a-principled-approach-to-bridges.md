---
source: ethresearch
topic_id: 14725
title: Hashi - A principled approach to bridges
author: mkoeppelmann
date: "2023-01-31"
category: Architecture
tags: []
url: https://ethresear.ch/t/hashi-a-principled-approach-to-bridges/14725
views: 14003
likes: 13
posts_count: 9
---

# Hashi - A principled approach to bridges

**EDIT**: We have stared implementing this concept under the name Hashi at: [GitHub - gnosis/hashi: An EVM hash oracle aggregator](https://github.com/gnosis/hashi)

**Preface**

We see a range of approaches for bridges. The L2beat team gave a good [overview here](https://gov.l2beat.com/t/l2bridge-risk-framework/31).

The problem with the current approach is that the bridge landscape is very heterogeneous. For some chain combinations, there might be bridge solutions with lower trust requirements (e.g. a [zk based light client bridge](https://blog.succinct.xyz/post/2022/10/29/gnosis-bridge/) between Gnosis Chain and Ethereum - or this Berkely [paper on zk-birdges](http://zkbridge.org/) that has been the starting point for the [zk-collective](https://zkcollective.org/)). However - those bridges might only be available for a subset of chains and an application that needs to bridge to several chains might need to use a bridge solution that has worse security assumptions but can serve a greater number of chains (e.g. committee-based bridges like e.g. [wormhole](https://wormhole.com/))

(As a side note: Those security assumptions are about the system assuming it works as intended, they do not take into consideration the possibility of bugs. Historically many bridge hacks did not have their root cause in e.g. committees getting compromised but instead simply in smart contract bugs. Taking that into account it is maybe impossible to do an objective ranging of security of different bridges)

We see currently 2 issues:

1. As new bridge designs are being developed they often let applications pick new security tradeoffs but as discussed above they are rarely strictly better than what existed before
2. Standardization: currently, absolutely most bridges have their own message formats. For an application to switch from one bridge to another is a major engineering task. Early approaches to find standards for cross chain messages (kind of IBC for EVM) have not yet succeeded.

This approach tries to solve both:

1. Create “additive” security. New bridge approaches can ideally increase the security of existing bridges instead of offering new tradeoffs
2. Standardization at least on the lowest level (block header) - this allows standards to emerge above that are independent of the underlying bridge/trust mechanism

---

[![Screenshot 2023-01-31 at 16.49.32](https://ethresear.ch/uploads/default/optimized/2X/d/d2aa1320f3ac50c24dd6ade24e92ee5a12d5c493_2_690x388.png)Screenshot 2023-01-31 at 16.49.322738×1542 383 KB](https://ethresear.ch/uploads/default/d2aa1320f3ac50c24dd6ade24e92ee5a12d5c493)

**Block header based bridges**

At the center of this approach are “header storage contracts” - simple contracts that store ChainID->blocknumber->header

These header storage contracts need to get the headers from “header oracles” - they can be the different bridge we know today. Note, it is easily possible to convert any existing bridge that allows sending arbitrary messages into header oracles. If they do not support access to block headers directly, one can simply write a contract on the source chain that accesses a recent block header and sends it into the bridge.

We believe the block header abstraction layer is the best for standardization and aggregation. As block header oracles need governance, there might still be many per chain combination, but the role of governance can be quite minimized. After setting up a set of trusted bridge oracles, a minimized governance would only act as a conflict resolution mechanism. If all oracles report the same header for a block number, governance has no rights. Only in case oracles make conflicting reports governance would need to resolve it.

Once a reliable source for block headers from a foreign chain is established different tools can emerge on top.

a) Merkle proof for specific storage slots

b) Merkle proof for specific events being emitted

c) zk-based proof of (storage/ events/ previous headers/ …)

On top of these primitives, application specific contracts can emerge: Token bridges/ NFT bridges/ allowing smart contract wallets to [control assets cross chain](https://forum.gnosis-safe.io/t/how-can-a-safe-hold-asset-on-multiple-chains/2242)/…

As a side note: It might be even useful to have such a header oracle for your own chain. Currently within the EVM applications can only access the last 256 headers.

**Drawbacks**

The main drawback of this approach is higher gas costs and potentially slower bridging times. If n oracles are required for the header storage contract, the bridge time will be determined by the slowest. However - “liquidity protocols” like Hop or Connexed have emerged that can do much faster optimistic execution. They are expanding their scope to general messages. Those approaches still need a source of truth eventually which the described design can hopefully provide.

## Replies

**seunlanlege** (2023-01-31):

I actually really like this approach better, rather than en-forcing message formats, we can have standardized interfaces that bridge contracts can expose where they essentially act as block header oracles, rather than bundling a messaging protocol as well.

This can in turn allow applications develop their own custom messaging formats for special cases where the default messaging protocol doesn’t make sense.

I went ahead and sketched out a short API for what this `BlockHeaderOracle` might look like:

```auto
interface BlockHeaderOracle {
    // chainId can be the keccakHash of some readable version of the name
    // height of course refers to the block height, contracts should only query
    // for heights that were signalled in previous `NewHeader` events for obvious reasons.
    function blockHeader(bytes32 chainID, uint256 height) returns external public (bytes);

    // As new headers become available, the oracle should emit an even,
    // so offchain workers can notify on-chain contracts waiting on these headers.
    event NewHeader(bytes32 chainID, uint256 height);
}
```

---

**auryn** (2023-02-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> As block header oracles need governance, there might still be many per chain combination, but the role of governance can be quite minimized. After setting up a set of trusted bridge oracles, a minimized governance would only act as a conflict resolution mechanism. If all oracles report the same header for a block number, governance has no rights. Only in case oracles make conflicting reports governance would need to resolve it.

I actually think that governance can be completely eliminated in this system, which seems preferable. The core assumption that leads this to require governance is that this system must be able to decide what the canonical block header is for any past block on any given chain. But I think that is beyond the scope of what this contract needs to do.

Rather than having some governance mechanism mandated with curating oracles and conflict resolution, in order to decide the header for each historical block, all this system needs to do is aggregate the block headers reported by any number of header oracles. It should simply be a common interface for querying the block header reported by many disparate mechanisms.

I see no reason why anyone should not be able to add an adapter to any header oracle and it simply be up to the user (the person / contract / app consuming block headers) to decide what combination of oracles to trust and what the conflict resolution rules / mechanism should be.

Perhaps the contract should provide an optional conflict resolution mechanism, analogous to an M/N multisig, where the user would require M/N of their chosen headers to agree on the header for any given block in order to consider the reported header valid.

From the user’s perspective, here is an interface that feels sufficient.

```solidity
interface metaHeaderOracle {
  /// @dev Returns the block header reported by a given oracle for a given block.
  /// @param oracleAdapter Address of the oracle adapter to query.
  /// @param blockNumber Block number for which to return a header.
  /// @return blockHeader Block header reported by the given oracle adapter for the given block number.
  function getHeaderFromOracle(
    address oracleAdapter,
    uint256 blockNumber)
  public view returns(bytes32 blockHeader);

  /// @dev Returns the block headers for a given block reported by a given set of oracles.
  /// @param oracleAdapters Array of address for the oracle adapters to query, MUST be provided in numerical order from smallest to largest.
  /// @param blockNumber Block number for which to return headers.
  /// @return blockHeaders Array of block header reported by the given oracle adapters for the given block number.
  /// @notice This method MUST revert if the oracleAdapters array contains duplicates.
  function getHeadersFromOracles(
    address[] oracleAdapters,
    unint256 blockNumber)
  public view returns(bytes32[] blockHeaders);

  /// @dev Returns the blockheader agreed upon by a threshold of given header oracles.
  /// @param oracleAdapters Array of address for the oracle adapters to query, MUST be provided in numerical order from smallest to largest.
  /// @param blockNumber Block number for which to return headers.
  /// @param threshold Threshold of oracles that must report the same header for the given block. `threshold` MUST be ` oracleAdapters.length / 2`.
  /// @return blockHeader Block header reported by the required threshold of given oracle adapters for the given block number.
  /// @notice This method MUST revert if the oracleAdapters array contains duplicates.
  function getHeaderFromThreshold(
    address[] oracleAdapters,
    unint256 blockNumber,
    uint256 threshold)
  public view returns(bytes32 blockHeader);
}
```

---

**mkoeppelmann** (2023-02-15):

There is a debate to have whether the system should be push (oracles ping the header storage contract) or pull (head storage pings the oracles) and depending on this where headers are actually stored. In a pull approach, the header storage contract could actually be stateless. In a pull approach, the “getHeaderFromOracle” function would be redundant as one could query the oracle simply directly.

Anyhow, I am leaning towards a push approach to reduce the total number of interactions. Because the oracle needs to be “pushed” to in any case first before the header could do a pull. Going for a push approach (and storing the result after the first push) also makes sure that an oracle can not report differently about the same block which reduces complexity for edge cases in conflict resolution.

Another detail is, whether there should be one header storage contract per chain or should it all be in one contract, and thus functions would contain a chain ID.

```auto
contract metaHeaderOracle {
 /// chainID -> blocknumber -> oracle -> blockhash
 mapping (unit => mapping( unit => mapping( address => bytes32) header;

  function pushHeader(uint chainID, uint blockNumber, bytes32 hash) {
  header[chainID][blockNumber][msg.sender] = hash
  }

```

---

**auryn** (2023-02-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> There is a debate to have whether the system should be push (oracles ping the header storage contract) or pull (head storage pings the oracles)

My take on push/pull is that it’s probably up to the adapter contract for any given header oracle, and is likely determined by the constraints of each oracle mechanism. The MetaHeaderOracle can be agnostic to whether an adapter is push or pull.

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> makes sure that an oracle can not report differently about the same block which reduces complexity for edge cases in conflict resolution.

I really think this is an implement detail that adapters can have the freedom to choose. Some may allow the oracle to change its mind, others may not. Either option has consequences.

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> Another detail is, whether there should be one header storage contract per chain or should it all be in one contract, and thus functions would contain a chain ID.

I think the MetaHeaderRelay can both be one large contract and also not require chain IDs be passed in as parameters, so long as each adapter serves only one chain. It’s up to the user to make sure the set of adapters they query all correspond to the same chain. If not, there will surely be no consensus about the header returned.

---

**mkoeppelmann** (2023-03-04):

A quick update here: we got good feedback for this approach and various teams are interested in contributing. We started to implement it at: [GitHub - gnosis/hashi: An EVM header oracle aggregator](https://github.com/gnosis/hashi)

We already have some experimental “header oracles” for the Gnosis Chain AMB bridge and e.g the Wormhole bridge.

---

**sujithsomraaj** (2023-04-14):

"I really like the approach to expand the security of AMBs, especially since message bridges don’t seem interested in standardizing their interface layer (as discussed in this thread: [Standardisation of cross-chain messaging interface](https://ethresear.ch/t/standardisation-of-cross-chain-messaging-interface/13770)).

I do have a couple of concerns, however. Firstly, this approach removes the need for any validation mechanism by AMBs since the Hashi oracle network is extensive. If message bridges implement Hashi oracle aggregators, then there is no need for validation at the transport layer for AMBs since it would be unnecessary. They can simply act as relayers since the bulk of validation can be done by validating the payload delivered by AMBs against the proof delivered by the Hashi oracle aggregators.

Secondly, in such a case, if the oracle network of Hashi decides to work against a particular AMB (let’s say they collude with a competitor AMB), is there a way for an AMB to challenge the decision of the oracle network?"

Can’t we achieve the same by using a single oracle, and multiple relayers (to reduce the cost) and use a definite quorum approach.

For eg., use 1 oracle that just deliver the proof and the rest of them are relayers delivering multiple fragments of the message, then we reconstruct the message and prove it against the proof. (This will reduce the additive cost). just a thought !

---

**seungjulee** (2023-05-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> Block header based bridges
> …
>
>
> Once a reliable source for block headers from a foreign chain is established different tools can emerge on top.
>
>
> c) zk-based proof of (storage/ events/ previous headers/ …)
>
>
> …
>
>
> As a side note: It might be even useful to have such a header oracle for your own chain. Currently within the EVM applications can only access the last 256 headers.

For ZK Collective Hackathon, we created a proof of concept for this idea from [@mkoeppelmann](/u/mkoeppelmann).

‘**L1StateOracle** - A trustless and affordable framework for storing L1 historical states on L2 using zkp and block headers’

Given a reliable L1 block header hash for a certain block number with Hashi on L2, this PoC proves that you can store a L1 state value on L2 trustlessly by using block headers as a source of truth.

[![Screen Shot 2023-05-01 at 13.09.20](https://ethresear.ch/uploads/default/optimized/2X/3/3e71b9ad721ef3336bb9a9cfea30413b88519abb_2_690x384.jpeg)Screen Shot 2023-05-01 at 13.09.202000×1114 171 KB](https://ethresear.ch/uploads/default/3e71b9ad721ef3336bb9a9cfea30413b88519abb)

**How it works**

1. We used Axiom.xyz to create a ZK proof of a storage slot value associated with the block header at a desired block number.
2. On L2, we call AxiomStorageProof with the ZK storage proof that includes  (storageSlot, slotValue, blockNumber, associatedBlockHeaderHash).
3. On L2,  AxiomStorageProof calls Hashi to get the reliable block hash for L1 at a desired block number.
4. We compare the hash returned from Hashi and the one from the proof.
5. If same, AxiomStorageProof calls the prover contract to verify the proof. The prover verifies the storage value with the associated block header.
6. AxiomStorageProof  retrieves the state value associated with the block header. This retrieved state value can be stored, and be used for any other contracts on L2.

**Terminology**: For simplicity, we used L1 as a term for the source chain, and L2 as a term for the target chain. L1 and L2 here do not imply any association like rollup between the two. L1 and L2 can be any EVM compatible chain supported by Gnosis Hashi.

**Limitation**: This currently can only check the state value of a contract stored on a EVM storage slot, not the returned value from a contract method.

p.s. I’m looking for an engineering job in web3. Hire me! [resume.sjlee.me](http://resume.sjlee.me)

**More Info**



      [github.com/gnosis/hashi](https://github.com/gnosis/hashi/pull/11)














####


      `main` ← `seungjulee:main`




          opened 04:46AM - 22 Apr 23 UTC



          [![](https://ethresear.ch/uploads/default/original/2X/1/10a0ac36de7e85b6c13801f092d2485d77b75a71.png)
            mellowcroc](https://github.com/mellowcroc)



          [+806
            -0](https://github.com/gnosis/hashi/pull/11/files)







Hi, as part of the [ZKP Hackathon](https://zk-hacking.org/), we integrated Axiom[…](https://github.com/gnosis/hashi/pull/11) with Hashi.

Please refer to the following resources for detailed information:
https://hackmd.io/@mellowcroc/rJDwFTe7h
https://pitch.com/public/338a53ec-2b25-4ce8-a53c-2f963356326a

Note: We didn't get to copy over Axiom's verifier contract (https://github.com/axiom-crypto/axiom-eth/blob/main/data/storage/storage_ts.yul) in the current version, so we're using a fork of mainnet for testing. Since it conflicts with Hashi's existing Hardhat testing env, we commented out the testing code (in `hardhat.config.ts`). We are planning to update this very soon.

---

**kladkogex** (2023-05-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> At the center of this approach are “header storage contracts” - simple contracts that store ChainID->blocknumber->header
> These header storage contracts need to get the headers from “header oracles” - they can be the different bridge we know today.

If the blocks on the source chains are finalized using signing, then you do not need multiple oracle - the  destination chain can verify the signature, so anyone can submit the header.

Actually, there headers could be submitted by users in a crowdsourced way, as users submit transactions

Verification of many signatures they can be aggregated using ZK Protocols like Nova into a single ZK proof.


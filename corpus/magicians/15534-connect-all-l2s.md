---
source: magicians
topic_id: 15534
title: Connect all L2s
author: JXRow
date: "2023-08-24"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/connect-all-l2s/15534
views: 2701
likes: 7
posts_count: 17
---

# Connect all L2s

Nowadays, there is an increasing number of Layer 2 (L2) solutions, and official L2 implementations typically act as bridges to Layer 1 (L1). It appears as follows:

[![image](https://ethereum-magicians.org/uploads/default/original/2X/d/d583a5ee820863885a4d016aeacec16b6e962174.png)image639×302 9 KB](https://ethereum-magicians.org/uploads/default/d583a5ee820863885a4d016aeacec16b6e962174)

If we want to achieve full interoperability among all Layer 2 solutions, it would be as follows:

[![image](https://ethereum-magicians.org/uploads/default/original/2X/1/17c3337a3f2ce0f432a7527b1a7e7398a0a34091.png)image564×360 23.6 KB](https://ethereum-magicians.org/uploads/default/17c3337a3f2ce0f432a7527b1a7e7398a0a34091)

For each blockchain, it needs to establish cross-chain connections with five other blockchains. If there are n blockchains, then we would require n * (n-1) cross-chain bridges. (Note: What is commonly perceived as a single cross-chain bridge actually encompasses two separate bridges, one for A to B and another for B to A).

Cross-chain bridges essentially relay information from Chain A to Chain B. To optimize the cross-chain process, we propose a shift from a push mechanism to a pull mechanism. Each blockchain would consolidate data from the other five blockchains and write it as a single transaction on its own chain. This approach significantly reduces the number of required cross-chain bridges.

[![image](https://ethereum-magicians.org/uploads/default/original/2X/b/b0c4fbcf665ee2343179317ad3562e67bee354fb.png)image592×600 18.1 KB](https://ethereum-magicians.org/uploads/default/b0c4fbcf665ee2343179317ad3562e67bee354fb)

With n blockchains, only n cross-chain bridges are needed.

Suppose there are 6 blockchains, originally requiring 30 cross-chain bridges, but now only six are needed.

Suppose there are 10 blockchains, originally requiring 90 cross-chain bridges, but now only ten are needed.

There is no cross-chain bridge that can guarantee 100% security!

By dividing the cross-chain bridge into SendPort and Bridge layers, we can ensure that at least SendPort is 100% secure.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/d/dabe72e1db266604836062e9d942034f07b7e0aa_2_690x351.png)image800×408 53.7 KB](https://ethereum-magicians.org/uploads/default/dabe72e1db266604836062e9d942034f07b7e0aa)

SendPort, the smart contract acting as a data port, securely stores the data to be transferred across chains. As a decentralized and autonomous public infrastructure, it operates at the protocol level, ensuring a high level of security.

Bridge, on the other hand, represents the various cross-chain bridge projects. Each project retrieves data from the same SendPort and transfers it to their respective Bridge smart contracts. The data transfer methods employed may include fraud-proof mechanisms, multi-signature schemes, zero-knowledge proofs, and other secure techniques.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/a/aa3e91f8981cc87337e427c67fdc26ed332ca4a8_2_690x341.png)image800×396 51.8 KB](https://ethereum-magicians.org/uploads/default/aa3e91f8981cc87337e427c67fdc26ed332ca4a8)

As illustrated above, the three cross-chain bridge projects are all retrieving data from the same SendPort. Consequently, the data transported to their respective Bridge contracts should be identical. To enhance the security of cross-chain transfers, we can implement a “2 of 3” rule, even if 1 bridge be hacked, the cross-chain network still work, significantly improves the overall security of cross-chain operations.

For efficient data transfer, the recommended approach is to utilize a Hash Merkle Tree.

[![image](https://ethereum-magicians.org/uploads/default/original/2X/c/ceaf0b917aee9f61c0ca0d8cb453a1ca5032aeee.png)image800×399 28 KB](https://ethereum-magicians.org/uploads/default/ceaf0b917aee9f61c0ca0d8cb453a1ca5032aeee)

We send the hash of the data that needs to be cross-chain to the SendPort contract, which automatically generates the Merkle Tree. Only the Root Hash needs to be transported to verify the entire cross-chain data on the target chain. The Root Hash is very small, which is why we can consolidate cross-chain data from 100 chains into a single transaction for transportation to the target chain.

Hitchhiking becomes feasible. You can send the cross-chain information to the SendPort, which is free of charge, and then wait for the cross-chain bridge to transport it, without incurring any additional transportation costs. Finally, you can verify the cross-chain data on the target chain, which is also free of charge. In other words, you have hitched a ride.

By utilizing the aforementioned “2 of 3” rule, you can trust the cross-chain network, which is also free of charge.

I don’t know if there is a similar EIP, if no, can I propose this?

## Replies

**qizheng09** (2023-08-24):

Our current project is similar to this proposal, and it is set to launch on September 15th. It will enable trustless connection between any L1 and L2 solutions, which will greatly elevate the cross-chain capabilities within the entire industry. ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=12)

---

**xinbenlv** (2023-08-24):

Sounds pretty interesting. What does SendPort do?

---

**JXRow** (2023-08-24):

The SendPort is like a port, othert contracts and users send the cross-chain data to the port, it stores the pending data, waiting for sending to the destination chain, so it names SendPort.

---

**Mani-T** (2023-08-24):

Good idea. Replacing the push mechanism with a pull mechanism can streamline the cross-chain process, resulting in fewer necessary cross-chain bridges and enhancing efficiency and cost-effectiveness.

---

**xzhang** (2023-08-25):

Interesting idea! Quick question, who is responsible for moving the merkle data from the SendPort to the Bridge and how to guarantee the transfer of data is done correctly?

---

**JXRow** (2023-08-26):

Base on SendPort, it could have multiple Brige projects, each of them has its responsible for moving the merkle root, they work like Oracle, the more Oracles, the more correctly the data will be.

To achieve this, it needs each Oracle(Bridge) moving the same merkle root, that’s exactly the SendPort offering. Every chain has only one SendPort, so it works.

---

**brandonfrulla** (2023-08-28):

So in other words, we are almost enabling a `git fetch --all`-like structure for each chain in the L2 ecosystem.

I like the idea of removing so many bridges, since we all know they are one of the biggest risks to crypto natives for the foreseeable future (and continued “X bridge hacked for $Y” headlines will deter the masses from onboarding).

If we are standardizing this greatly simplified architecture, should the corresponding ‘refresh rate’ also be discussed [@JXRow](/u/jxrow)? With the reduced complexity, perhaps increased rate of refreshing could be supported as well, and increase UX along with it

---

**JXRow** (2023-08-28):

Refesh rate? I think it maybe 1 min, I’m trying to write codes to test it.

---

**BipBop** (2023-08-30):

Thank you for this insight about your project! There’s a great paper that designs a solution for interoperability between disparate systems; It uses a push mechanism so it may be a bit irrelevant here, but it’s still worth checking out as it shares similarities with your idea!

IPSME - Idempotent Publish/Subscribe Messaging Environment https://dl.acm.org/doi/10.1145/3458307.3460966

---

**JXRow** (2023-08-31):

I made it, *addMsgHash(bytes32 msgHash, uint toChainId)* is the function to store the message of cross, after a while, someone call the *addMsgHash()* and auto *pack()*, it dosen’t need owner or upgrade, it works decentralized.

This contract needs https://github.com/merkletreejs/merkletreejs to work with.

And, I built a Bridge contract to call the *addMsgHash()*, when it added 100 messages, it will auto pack, the pack() gas cost is 433649, not too much.

```auto
// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

import "./ISendPort.sol";
import "hardhat/console.sol";

contract SendPort is ISendPort {
    uint public constant PACK_INTERVAL = 6000;
    uint public constant MAX_PACKAGE_MESSAGES = 100;

    uint public pendingIndex = 0;

    mapping(uint => Package) public packages;

    constructor() {
        packages[0] = Package(0, bytes32(0), new bytes32[](0), new uint[](0), block.timestamp, 0);
    }

    function addMsgHash(bytes32 msgHash, uint toChainId) public {
        bytes32 leaf = keccak256(
            abi.encodePacked(msgHash, msg.sender)
        );
        Package storage pendingPackage = packages[pendingIndex];
        pendingPackage.leaves.push(leaf);
        pendingPackage.toChainIds.push(toChainId);

        emit MsgHashAdded(leaf, toChainId, msg.sender);

        if (pendingPackage.leaves.length >= MAX_PACKAGE_MESSAGES) {
            console.log("MAX_PACKAGE_MESSAGES", pendingPackage.leaves.length);
            _pack();
            return;
        }

        // console.log("block.timestamp", block.timestamp);
        if (pendingPackage.createTime + PACK_INTERVAL  1) {
            _leaves = _computeLeaves(_leaves);
        }
        pendingPackage.root = _leaves[0];
        pendingPackage.packedTime = block.timestamp;

        emit Packed(pendingPackage.index, pendingPackage.packedTime, pendingPackage.root);

        pendingIndex = pendingPackage.index + 1;
        packages[pendingIndex] = Package(pendingIndex, bytes32(0), new bytes32[](0), new uint[](0), pendingPackage.packedTime, 0);
    }

    function _computeLeaves(bytes32[] memory _leaves) pure internal returns (bytes32[] memory _nextLeaves) {
        if (_leaves.length % 2 == 0) {
            _nextLeaves = new bytes32[](_leaves.length / 2);
            bytes32 computedHash;
            for (uint i = 0; i + 1 < _leaves.length; i += 2) {
                computedHash = _hashPair(_leaves[i], _leaves[i + 1]);
                _nextLeaves[i / 2] = computedHash;
            }

        } else {
            bytes32 lastLeaf = _leaves[_leaves.length - 1];
            _nextLeaves = new bytes32[]((_leaves.length / 2 + 1));
            bytes32 computedHash;
            for (uint i = 0; i + 1 < _leaves.length; i += 2) {
                computedHash = _hashPair(_leaves[i], _leaves[i + 1]);
                _nextLeaves[i / 2] = computedHash;
            }
            _nextLeaves[_nextLeaves.length - 1] = lastLeaf;
        }
    }

    function _hashPair(bytes32 a, bytes32 b) private pure returns (bytes32) {
        return a < b ? _efficientHash(a, b) : _efficientHash(b, a);
    }

    function _efficientHash(bytes32 a, bytes32 b) private pure returns (bytes32 value) {
        /// @solidity memory-safe-assembly
        assembly {
            mstore(0x00, a)
            mstore(0x20, b)
            value := keccak256(0x00, 0x40)
        }
    }
}
```

---

**qizheng09** (2023-09-18):

[docs.google.com](https://docs.google.com/forms/d/1TY2xaz1SjNRtiTH-7_acibF4mZBts5dc25X02cKbssc/viewform?edit_requested=true)



    https://docs.google.com/forms/d/1TY2xaz1SjNRtiTH-7_acibF4mZBts5dc25X02cKbssc/viewform?edit_requested=true

###

Welcome to the Cycle Network Testnet!

Cycle Network is a trustless multi-chain asset settlement layer for cross-chain apps.
Cycle ultimate goal is to rescue developers from the tedious intricacies of layer deployment and users from the...










Hi everybody, we have launched our testnetV1, pls complete the form to apply for try.

---

**SKYBITDev3** (2023-09-18):

In June it was announced that

> Polygon 2.0 will be a network of zero-knowledge (ZK) layer 2 chains that will be able to communicate amongst themselves. The blog post also shared that on the user end, the network will feel like a single blockchain.

Source: https://www.coindesk.com/business/2023/06/12/polygon-takes-wraps-off-version-20

---

**JXRow** (2023-10-11):

I push it to EIP

https://github.com/ethereum/EIPs/pull/7833

---

**serejke** (2023-10-17):

That’s an interesting approach to use the pull mechanism. I have a couple of questions:

1. How DApps would pay the fees imposed by bridge? DApps are not aware of the bridges that will deliver their messages to the destination.
Since all messages are aggregated in a single SendPort contract, some DApps might have paid for the fee, but some have not. And the bridge will not be able to deliver only those who paid because the MerkleTree root would not match.
2. Normally, cross-chain DApps use the delivered message to call a contract on the destination chain. With the pull mechanics, the DApps would need to track the messages delivered and submit a “processing” transaction. It makes the cross-chain workflows a bit complicated engineering-wise.
Do you think there will be a best-practices pattern for the messages post-processing?

---

**JXRow** (2023-10-17):

1.Dapps dont need to pay the fees,  the bridge do the assets cross, and give Dapps hitchhike. It’s also good to the bridge itself, it donsn’t cost more, but take a better data view.

2.Yes, DApps need to track the messages delivered and submit a “verify” transaction. The good for this workflow is that it can run without servers, only front-end, totally decentralized, Dapps dont need to pay the gas(or fees), user will pay the gas.

---

**JXRow** (2023-12-08):

hey guys, the ERC is updated

https://github.com/ethereum/ERCs/pull/62


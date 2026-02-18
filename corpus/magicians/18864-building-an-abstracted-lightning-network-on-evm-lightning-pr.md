---
source: magicians
topic_id: 18864
title: "Building an Abstracted Lightning Network on EVM: Lightning Protocol"
author: JXRow
date: "2024-02-22"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/building-an-abstracted-lightning-network-on-evm-lightning-protocol/18864
views: 1226
likes: 1
posts_count: 3
---

# Building an Abstracted Lightning Network on EVM: Lightning Protocol

### Abstract

This article explores the possibility of abstracting the Bitcoin Lightning Network for application on EVM chains and designs a protocol layer for the wallet and payment sector: the Lightning Protocol. This protocol can significantly enhance the usability and security of wallets, accelerating the adoption of crypto payments.

### Rationale

A typical blockchain transfer involves the sender signing their transfer, and upon being added to the blockchain by nodes, the recipient confirms receipt. Adding to the blockchain requires block confirmation time, resulting in a delay in funds being received. If the sender gives the off-chain signature to the recipient, the recipient can take this signature to the blockchain at any time to collect the funds. The question arises: can the recipient confirm receipt without adding it to the blockchain, thus achieving instant transfer?

The answer is no, because the sender could sign the same funds over to multiple recipients, leading to a double-spending issue. The Bitcoin Lightning Network provides an excellent solution to this problem:

Funds are first locked in a Lightning Network node. When the sender transfers the money, they sign it over to the node, which then transfers it to the recipient. If the sender tries to double-spend the funds, the node can refuse the transaction, thus solving the double-spending problem and enabling instant transfers. Nodes can also bundle many transactions together before submitting them to the blockchain, significantly reducing transaction fees. (For ease of understanding, this explanation simplifies channels and various cryptographic terms.)

The key to this approach is that nodes can prevent double-spending. If all transactions sent from wallets must first go through a node, which then submits them to the blockchain, double-spending can be prevented, and instant transfers can be achieved.

Testing on the Ethereum Virtual Machine (EVM) has shown that this idea is feasible. If it were developed into a standard protocol, most public blockchains could implement instant transfers through this protocol. This protocol is an abstracted implementation of the Lightning Network, hence the name: Lightning Protocol. Compared to funds locked in the Lightning Network, which are off-chain, the funds in the Lightning Protocol remain on-chain, making it more suitable for larger sums.

### Source Code

The implementation of the smart contract consists of two components: the [SmartWallet.sol] and the [Node.sol]. Below is the core source code:

```solidity
/**
* Multiple operations in one sign, with atomic(all successed or all failed)
* owner to sign, bundler to call
*/
function atomSignCall(
    bytes calldata atomCallBytes,
    uint32 deadline,
    bytes calldata signature
) external onlyBundler {
    require(deadline >= block.timestamp, "atomSignCall: Expired");
    bytes32 msgHash = keccak256(
        bytes.concat(
            msg.data[:msg.data.length - signature.length - 32],
            bytes32(block.chainid),
            bytes20(address(this)),
            bytes4(valid)
        )
    );
    require(!usedMsgHashes[msgHash], "atomSignCall: Used msgHash");
    require(
        owner == msgHash.toEthSignedMessageHash().recover(signature),
        "atomSignCall: Invalid Signature"
    );

    _doAtomCall(atomCallBytes);

    usedMsgHashes[msgHash] = true;
}

function _doAtomCall(bytes calldata atomCallBytes) private {
    uint i;
    while (i < atomCallBytes.length) {
        address to = address(uint160(bytes20(atomCallBytes[i:i + 20])));
        uint value = uint(bytes32(atomCallBytes[i + 20:i + 52]));
        uint len = uint(bytes32(atomCallBytes[i + 52:i + 84]));

        (bool success, bytes memory result) = to.call{value: value}(
            atomCallBytes[i + 84:i + 84 + len]
        );
        if (!success) {
            assembly {
                revert(add(result, 32), mload(result))
            }
        }

        i += 84 + len;
    }
}
```

Using the smart contract as a wallet, all transactions exposed to the outside can only go through the `atomSignCall()` function. This function can only be called by the Node, and users themselves cannot invoke it. In naming, inspiration is drawn from ERC4337’s Bundler, namely Node. Users can sign a series of operations with their private key. These series of operations possess atomicity, meaning either all succeed or all roll back.

Below is the Node’s core source code:

```solidity
function executeOperation(
    address wallet,
    bytes calldata data
) public onlyBundlerManager {
    _callTo = wallet;
    _doSingleCall(_callTo, 0, data);
    _callTo = address(0);
}

function bundlerCallback(
    address to,
    uint value,
    bytes calldata data
) external onlyCallTo {
    _doSingleCall(to, value, data);
}

function _doSingleCall(address to, uint value, bytes calldata data) internal {
    (bool success, bytes memory result) = to.call{value: value}(data);
    if (!success) {
        assembly {
            revert(add(result, 32), mload(result))
        }
    }
}
```

The `_doSingleCall()` function enables the Node to initiate any arbitrary call, including invoking the `atomSignCall()` function of the user’s smart wallet.

The `bundlerCallback()` function represents a significant upgrade. It allows the Node, when calling the `atomSignCall()` function of the SmartWallet, to also trigger the `bundlerCallback()` function of the Node. This bidirectional communication ensures that a series of atomic operations proposed by the user can include tasks for the Node to execute. If the Node rejects these tasks, they can remain off-chain.

### Use case

In addition to facilitating real-time transfers, the Lightning Protocol serves as an intelligent agreement signed between SmartWallet and Node. This protocol specifies the actions required from users and Nodes, which are then signed by the user and submitted to the Node. If the Node proceeds to execute the transaction on-chain, the protocol includes the Node’s signature, and the execution on-chain enforces the terms of the protocol. If the Node chooses not to execute the transaction on-chain, the protocol remains inactive. The execution of the protocol is atomic: if one party fails to fulfill its obligations while the other has completed theirs, both parties roll back, rendering the protocol ineffective, and neither party suffers losses. Additionally, the protocol is enforceable: once one party has completed its obligations, the other party cannot retract, and completion is mandatory.

This feature is particularly useful in limit order trading, such as purchasing WBTC:

1. SmartWallet transfers USDT to Node.
2. Node exchanges USDT for WBTC and transfers it to SmartWallet.

The user signs both of these operations. If the Node finds the price acceptable, it can execute the transaction on-chain. Otherwise, it can treat it as a pending order, waiting for a suitable price before execution, with a deadline not exceeding the `deadline`. This feature enables decentralized limit orders: when the price is right, the system executes the trade for the user without touching the user’s funds. Previously, users either had to deposit funds into exchanges or authorize exchanges, leaving their funds vulnerable to hacking. However, with this method, even if the exchange is compromised, the hacker can only facilitate trades for users, without causing any loss.

To execute limit orders without requiring funds, the Node can adopt the following approach:

1. SmartWallet transfers USDT to Node.
2. Node exchanges USDT for WBTC on Uniswap and transfers it to SmartWallet.

In addition to these methods, the Node can obtain funds through flash loans, returning them after the trade is completed, thus incurring minimal borrowing costs. It can also source liquidity from multiple DEXs, making it suitable for large-volume trades.

Gas payment on behalf of users is also feasible:

1. SmartWallet performs regular transfers or interacts with DEFI.
2. SmartWallet transfers USDT to Node as gas.

The user signs both of these operations. After the Node executes the transaction on-chain, it receives USDT and covers the gas fees, and if the Node deems the gas fee insufficient, it can choose not to execute the transaction on-chain.

### Security

Because all operations must pass through the Node, it can also serve as a guardian for the SmartWallet. If it detects any unsafe operations, it can choose not to execute them on-chain, thereby preventing losses. Implementing 2FA on the Node side for sensitive operations provides an additional layer of security, requiring a second confirmation for unsafe operations.

It is evident that if the Node behaves maliciously, it can freeze the SmartWallet. To prevent such incidents, it is recommended that SmartWallets allow users to switch Nodes. Once switched, the original Node should not be able to prevent user operations, potentially leading to double-spending. It is advisable to introduce a transition period during Node switching, during which the original Node continues to provide services.

## Replies

**zhiqiangxu** (2024-03-03):

It seems there’s already such a project: [GitHub - raiden-network/raiden: Raiden Network](https://github.com/raiden-network/raiden)

---

**JXRow** (2024-03-11):

I know that, but it’s difference, the point is Abstracted, which builds by solidity, in smart contract


---
source: ethresearch
topic_id: 15947
title: New Paradigm Wallets and Tokens
author: wenzhenxiang
date: "2023-06-21"
category: Applications
tags: []
url: https://ethresear.ch/t/new-paradigm-wallets-and-tokens/15947
views: 3015
likes: 5
posts_count: 5
---

# New Paradigm Wallets and Tokens

# New Token Design

ERC20 tokens are Ethereum-based standard tokens that can be traded and transferred on the Ethereum network. But the essence of ERC20 is based on the EOA wallet design. EOA wallet has no state and code storage, and the smart contract wallet is different.

Almost all ERCs related to tokens are adding functions, our opinion is the opposite, we think the token contract should be simpler, more functions are taken care of by the smart contract wallet.

Our proposal is to design a simpler token asset based on the smart contract wallet,

It aims to achieve the following goals:

1. Keep the asset contract simple, only need to be responsible for the transaction function
2. approve and allowance functions are not managed by the token contract , approve and allowance should be configured at the user level instead of controlled by the asset contract, increasing the user’s more playability , while avoiding part of the ERC20 contract risk.
3. Remove the transferForm function, and a better way to call the other party’s token assets is to access the other party’s own contract instead of directly accessing the token asset contract.
4. Forward compatibility with ERC20 means that all fungible tokens can be compatible with this proposal.

**Examples**

The third party calls the user’s token transaction`(transferForm)`,

Judges whether the receiving address is safe `(safeTransferForm)`,

Permit extension for signed approvals `(ERC-2612,``permit)`

Authorizes the distribution of the user’s own assets`(approve, allowance)`,

Add the transfer hook function. `(ERC-777, hook)`

The above work should be handled by the user’s smart contract wallet, rather than the token contract itself.

# New Wallet Design

The smart contract wallet allows the user’s own account to have state and code, bringing programmability to the wallet. We think there are more directions to expand. For example, token asset management, functional expansion of token transactions, etc.

It aims to achieve the following goals:

1. Assets are allocated and managed by the wallet itself, such as approve and allowance, which are configured by the user’s contract wallet, rather than controlled by the token asset contract, to avoid some existing ERC-20 contract risks.
2. Add the transferFungibleToken function, the transaction initiated by the non-smart wallet itself or will verify the allowance amount
3. Users can choose batch approve and batch transfer. Batch approve can greatly reduce gas. The contract wallet itself manages the authorization status of all assets, and batch approve can be performed without calling multiple asset contracts.
4. Users can choose to add hook function before and after their transferFungibleToken to increase the user’s more playability
5. The user can choose to implement the receive hook

## Replies

**wenzhenxiang** (2023-06-30):

Use the sequence diagram to compare the difference between using this interface to transfer tokens.

**Alice calls the transfer herself**

The user call the transaction sequence diagram now(transfer).

[![image](https://ethresear.ch/uploads/default/optimized/2X/6/60398dc26d0d1062c88b0a742e53b776518bf2ea_2_690x262.png)image806×307 10.3 KB](https://ethresear.ch/uploads/default/60398dc26d0d1062c88b0a742e53b776518bf2ea)

The user use new paradigm to call the transaction sequence diagram, dotted lines are optional.

[![image](https://ethresear.ch/uploads/default/optimized/2X/b/b7a04051b84b2c81e9187c97225a179b1b1aba3b_2_690x478.png)image922×639 25.9 KB](https://ethresear.ch/uploads/default/b7a04051b84b2c81e9187c97225a179b1b1aba3b)

**Alice doesn’t call the transfer herself**

Sequence diagram of third party calling user transaction now(transferForm).

[![image](https://ethresear.ch/uploads/default/optimized/2X/9/9da66532c999b7452e0729144b6e874ae704793c_2_690x392.png)image899×511 20.7 KB](https://ethresear.ch/uploads/default/9da66532c999b7452e0729144b6e874ae704793c)

Sequence diagram of third party calling user transaction use new paradigm.(transferFungibleToken).

[![image](https://ethresear.ch/uploads/default/original/2X/a/ae8339abb37764a9963b9f3cd6f5bb560bde3ae0.png)image862×499 14 KB](https://ethresear.ch/uploads/default/ae8339abb37764a9963b9f3cd6f5bb560bde3ae0)

The third party uses new paradigm and is compatible with the old dapp protocol and EOA to call the user transaction sequence diagram(transferForm).

[![image](https://ethresear.ch/uploads/default/optimized/2X/1/19b185ca6eb832756b3c4561f36a8302cc028218_2_636x500.png)image733×576 22.8 KB](https://ethresear.ch/uploads/default/19b185ca6eb832756b3c4561f36a8302cc028218)

---

**Ebrahim** (2023-11-26):

Nice

did you use automated tool to generate the above diagrams or you did it manually?

---

**wenzhenxiang** (2023-12-04):

just write mermaid code, you can use AI generated mermaid code.

---

**wenzhenxiang** (2023-12-12):

ERC20 token is based on EOA design, and defi is based on ERC20 and EOA design.

There are many areas that can be improved. When contract wallets come out, there will be new ways of interacting with assets. As the article says.

When base assets change and support contract wallet, new dapp paradigms will be born, and compatible with all existing assets.


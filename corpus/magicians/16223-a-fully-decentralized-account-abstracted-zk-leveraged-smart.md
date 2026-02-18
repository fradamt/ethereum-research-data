---
source: magicians
topic_id: 16223
title: A fully decentralized account abstracted, zk leveraged smart contract wallet
author: sidharth231999
date: "2023-10-23"
category: Web > Wallets
tags: [wallet, zkp]
url: https://ethereum-magicians.org/t/a-fully-decentralized-account-abstracted-zk-leveraged-smart-contract-wallet/16223
views: 1156
likes: 2
posts_count: 2
---

# A fully decentralized account abstracted, zk leveraged smart contract wallet

**Introduction**

We all know that to operate ERC-4337, a few centralized components are typically required. I’m here with a new approach to create a fully decentralized, abstracted account wallet.

This wallet can be made and accessed using just a username and password. Fund spending transactions can be initiated from any Externally Owned Account (EOA) as long as the correct username and password are used.

You can use anyone’s EOA to spends funds from your sc wallet and whosoever initiated the transaction, gets the gas fees paid by them in the same txn. If you don’t have EOA setup on your device, you can make transactions from the wallet using the backend service without compromising security. This way spending funds only requires username, password and internet.

The security of this wallet, including password verification and user operation validity, is supported by zk-SNARKs. Additional features include paying gas fees from the smart contract wallet and non-native gas payments.

**1. Wallet creation**

- Users can create a wallet by providing a username and password. The password is hashed and then sent to the Factory smart contract along with the username. The hashed password is mapped to the username, and a Wallet contract is deployed with its address mapped with both the username and the hashed password. The Wallet contract is owned by the Factory and has only one function, multicall which can be accessed solely by the Factory contract.

**2. Spend Funds**

- Whenever a user wishes to spend funds from the wallet, they need to provide their username, a zk proof confirming knowledge of the actual password, and the userOps generated in the frontend.
- The zk proof generation requires three inputs: 1) password, 2) hashed password, and 3) userOps. The zk constraints check if the user knows the password(pre-image) corresponding to the hashed password. Additionally, the circuit verifies if the provided userOps match the user’s intentions, thereby eliminating the possibility of a front-running attack. After confirming these conditions, the zk proof is generated and can be verified on the chain.
- The zk proof is generated in the frontend when the user selects their username, password, and userOps (such as swap, transfer tokens, mint NFTs, etc.). Following the generation of the zk proof, the “callWallet” function in the Factory contract is triggered.
- This function verifies the zk proof, stores the hash of the proof to prevent reuse, and, upon successful verification, retrieves the address of the wallet contract associated with the hashed password. Subsequently, the “multicall” function of that wallet is executed, and the userOps are carried out.

One important aspect to consider is that the security of this wallet relies on the Poseidon Hash, which is used to create hash from the password and is snark-friendly. I would appreciate any feedback from the community and would welcome insights into the Poseidon Hash from community members.

## Replies

**rajpatil7322** (2023-11-03):

Hey I would like to work on this with you can you share a repo if you have created


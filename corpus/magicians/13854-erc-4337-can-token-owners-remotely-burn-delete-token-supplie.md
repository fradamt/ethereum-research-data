---
source: magicians
topic_id: 13854
title: "ERC-4337: Can token owners remotely burn/delete token supplies from abstract smart contract wallets without wallet owners' approval?"
author: howardleejh
date: "2023-04-17"
category: EIPs
tags: [wallet]
url: https://ethereum-magicians.org/t/erc-4337-can-token-owners-remotely-burn-delete-token-supplies-from-abstract-smart-contract-wallets-without-wallet-owners-approval/13854
views: 789
likes: 1
posts_count: 5
---

# ERC-4337: Can token owners remotely burn/delete token supplies from abstract smart contract wallets without wallet owners' approval?

Apologies for my noobness here, can I ask what happens when exploiters create an ERC20 Token contract and it has a `burn()` function included, and then sell their tokens, and upon completion of sale, decides to burn all the tokens that belong to abstract smart contract wallet owners? Am I right to say that because smart contracts do not require an `approve()` before making a `safeTransferFrom()` to a `0x00` address, essentially “burning the tokens” and affecting total supply on the ERC20 tokens, that this might be a possible exploit for ERC-4337 smart contract wallet owners, meaning if i used my abstract smart contract wallet to purchase 10ETH worth of those ERC20 tokens, I might lose all my ERC20 tokens and my 10ETH when token owner executes a `burn(address myAccount, uint256 _maxValue)`?

## Replies

**Perrin** (2023-04-17):

Hi, are you sure about that? " Am I right to say that because smart contracts do not require an `approve()` before making a `safeTransferFrom()` to a `0x00` address"

---

**howardleejh** (2023-04-17):

I did a very simple test here. I created a ERC20 token, minted some and transferred it to some smart contract. My next transaction i used my deployer account to execute a `burn()` function on the smart contract and burned its tokens. It worked. Transaction can be found here:

https://sepolia.etherscan.io/tx/0xc206c8488dc17bccc979ed0435292737438c965cd5e09fc176ec98cb4bd9c177

---

**tdergouzi** (2023-04-18):

Look at your transaction, function burn being restricted to onlyOwner is inherently insecure.

---

**howardleejh** (2023-04-18):

Yes I get that. The purpose was to understand how smart contracts react to receiving ERC20 tokens and how ERC20 token owners, regardless of multisig or access control could potentially manipulate token supply held by smart contracts, hence the over simplified test.


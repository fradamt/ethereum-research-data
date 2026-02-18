---
source: magicians
topic_id: 4907
title: "EIP-3091: Block Explorer API Routes"
author: pedrouid
date: "2020-11-03"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-3091-block-explorer-api-routes/4907
views: 3735
likes: 2
posts_count: 3
---

# EIP-3091: Block Explorer API Routes

Providing wallet with a `blockExporerUrl` could be valuable given that applications can permissionessly interface with each other given that standards are followed and become interoperable.

Hence I’ve explored existing block explorers and identified existing patterns where these endpoints are in consensus and could be specified under a standard which this EIP describes

### L1 Blockchain Explorers

#### Blocks

Blockscout (chainId=100) → [Gnosis chain blocks | Blockscout](https://blockscout.com/poa/xdai/blocks/)<BLOCK_HASH_OR_HEIGHT>

Etherscan (chainId=1) → https://etherscan.io/block/<BLOCK_HASH_OR_HEIGHT>

Etherchain (chainId=1) → https://etherchain.org/block/<BLOCK_HASH_OR_HEIGHT>

Ethplorer (chainId=1) → unsupported

Etherscan and Etherchain are in consensus for blocks endpoint but Blockscout uses `/blocks` endpoint instead and Ethplorer doesn’t have a page for blocks so returns 404 not found.

#### Transactions

Blockscout (chainId=100) → https://blockscout.com/poa/xdai/tx/<TX_HASH>

Etherscan (chainId=1) → https://etherscan.io/tx/<TX_HASH>

Etherchain (chainId=1) → https://etherchain.org/tx/<TX_HASH>

Ethplorer (chainId=1) → https://ethplorer.io/tx/<TX_HASH>

All block explorers are in consensus for transactions endpoint.

#### Accounts

Blockscout (chainId=100) → https://blockscout.com/poa/xdai/address/<ACCOUNT_ADDRESS>

Etherscan (chainId=1) → https://etherscan.io/address/<ACCOUNT_ADDRESS>

Etherchain (chainId=1) → https://etherchain.org/account/<ACCOUNT_ADDRESS>

Ethplorer (chainId=1) → https://ethplorer.io/address/<ACCOUNT_ADDRESS>

All block explorers are in consensus for accounts endpoint except Etherchain which uses `/account` endpoint instead

#### ERC-20 Tokens

Blockscout (chainId=100) → [Tokens list - Gnosis chain explorer | Blockscout](https://blockscout.com/poa/xdai/tokens/)<TOKEN_ADDRESS>

Etherscan (chainId=1) → [Token Tracker | Etherscan](https://etherscan.io/token/)<TOKEN_ADDRESS>

Etherchain (chainId=1) → https://etherchain.org/token/<TOKEN_ADDRESS>

Ethplorer (chainId=1) → https://ethplorer.io/address/<TOKEN_ADDRESS>

Etherscan and Etherchain are in consensus but Blockscout uses `/tokens` endpoint instead and Ethplorer doesn’t have a page for tokens so redirects to accounts page (`/address`).

### L2 Explorers

#### Blocks

Matic → https://explorer.matic.network/blocks/<BLOCK_HEIGHT_OR_HASH>

zkScan → [Explore zkSync Lite L2 Blockchain | zkSync Lite Block Explorer](https://zkscan.io/blocks/)<BLOCK_NUMBER>

Fuel → https://rinkeby.fuel.sh/block/<BLOCK_NUMBER>

#### Transactions

Matic → https://explorer.matic.network/tx/<TX_HASH>

zkScan → [Explore zkSync Lite L2 Blockchain | zkSync Lite Block Explorer](https://zkscan.io/transactions/)<TX_HASH>

Fuel → https://rinkeby.fuel.sh/tx/<TX_HASH>

#### Accounts

Matic → https://explorer.matic.network/address/<ACCOUNT_ADDRESS>

zkScan → [Explore zkSync Lite L2 Blockchain | zkSync Lite Block Explorer](https://zkscan.io/accounts/)<ACCOUNT_ADDRESS>

Fuel → https://rinkeby.fuel.sh/address/<ACCOUNT_ADDRESS>

#### ERC-20 Tokens

Matic → https://explorer.matic.network/tokens/<TOKEN_ADDRESS>

zkScan → unsupported (`/tokens` displays a list of tokens pointing to L1 explorer)

Fuel → unsupported

## EIP-3091

### Blocks

<BLOCK_EXPORER_URL>/block/<BLOCK_HASH_OR_HEIGHT>

### Transactions

<BLOCK_EXPORER_URL>/tx/<TX_HASH>

### Accounts

<BLOCK_EXPORER_URL>/address/<ACCOUNT_ADDRESS>

### ERC-20 Tokens

<BLOCK_EXPORER_URL>/token/<TOKEN_ADDRESS>



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/3091)














####


      `master` ← `pedrouid:patch-7`




          opened 07:36PM - 02 Nov 20 UTC



          [![](https://avatars.githubusercontent.com/u/10136079?v=4)
            pedrouid](https://github.com/pedrouid)



          [+45
            -0](https://github.com/ethereum/EIPs/pull/3091/files)







Providing wallet with a `blockExporerUrl` could be valuable given that applicati[…](https://github.com/ethereum/EIPs/pull/3091)ons can permissionessly interface with each other given that standards are followed and become interoperable.

Hence I've explored existing block explorers and identified existing patterns where these endpoints are in consensus and could be specified under a standard which this EIP describes

### L1 Blockchain Explorers

#### Blocks
Blockscout (chainId=100) -> https://blockscout.com/poa/xdai/blocks/<BLOCK_HASH_OR_HEIGHT>
Etherscan (chainId=1) -> https://etherscan.io/block/<BLOCK_HASH_OR_HEIGHT>
Etherchain (chainId=1) -> https://etherchain.org/block/<BLOCK_HASH_OR_HEIGHT>
Ethplorer (chainId=1) -> unsupported

Etherscan and Etherchain are in consensus for blocks endpoint but Blockscout uses `/blocks` endpoint instead and Ethplorer doesn't have a page for blocks so returns 404 not found.

#### Transactions
Blockscout (chainId=100) -> https://blockscout.com/poa/xdai/tx/<TX_HASH>
Etherscan (chainId=1) -> https://etherscan.io/tx/<TX_HASH>
Etherchain (chainId=1) -> https://etherchain.org/tx/<TX_HASH>
Ethplorer (chainId=1) -> https://ethplorer.io/tx/<TX_HASH>

All block explorers are in consensus for transactions endpoint.

#### Accounts
Blockscout (chainId=100) -> https://blockscout.com/poa/xdai/address/<ACCOUNT_ADDRESS>
Etherscan (chainId=1) -> https://etherscan.io/address/<ACCOUNT_ADDRESS>
Etherchain (chainId=1) -> https://etherchain.org/account/<ACCOUNT_ADDRESS>
Ethplorer (chainId=1) -> https://ethplorer.io/address/<ACCOUNT_ADDRESS>

All block explorers are in consensus for accounts endpoint except Etherchain which uses `/account` endpoint instead

#### ERC-20 Tokens
Blockscout (chainId=100) -> https://blockscout.com/poa/xdai/tokens/<TOKEN_ADDRESS>
Etherscan (chainId=1) -> https://etherscan.io/token/<TOKEN_ADDRESS>
Etherchain (chainId=1) -> https://etherchain.org/token/<TOKEN_ADDRESS>
Ethplorer (chainId=1) -> https://ethplorer.io/address/<TOKEN_ADDRESS>

Etherscan and Etherchain are in consensus but Blockscout uses `/tokens` endpoint instead and Ethplorer doesn't have a page for tokens so redirects to accounts page (`/address`).

### L2 Explorers

#### Blocks
Matic -> https://explorer.matic.network/blocks/<BLOCK_HEIGHT_OR_HASH>
zkScan -> https://zkscan.io/blocks/<BLOCK_NUMBER>
Fuel -> https://rinkeby.fuel.sh/block/<BLOCK_NUMBER>

#### Transactions
Matic -> https://explorer.matic.network/tx/<TX_HASH>
zkScan -> https://zkscan.io/transactions/<TX_HASH>
Fuel -> https://rinkeby.fuel.sh/tx/<TX_HASH>

#### Accounts
Matic -> https://explorer.matic.network/address/<ACCOUNT_ADDRESS>
zkScan -> https://zkscan.io/accounts/<ACCOUNT_ADDRESS>
Fuel -> https://rinkeby.fuel.sh/address/<ACCOUNT_ADDRESS>

#### ERC-20 Tokens
Matic -> https://explorer.matic.network/tokens/<TOKEN_ADDRESS>
zkScan -> unsupported (`/tokens` displays a list of tokens pointing to L1 explorer)
Fuel -> unsupported

## EIP-3091

### Blocks
<BLOCK_EXPORER_URL>/block/<BLOCK_HASH_OR_HEIGHT>

### Transactions
<BLOCK_EXPORER_URL>/tx/<TX_HASH>

### Accounts
<BLOCK_EXPORER_URL>/address/<ACCOUNT_ADDRESS>

### ERC-20 Tokens
<BLOCK_EXPORER_URL>/token/<TOKEN_ADDRESS>

## Replies

**chaals** (2020-11-10):

It would make more sense to use the standard approach of `/.well-known`, per [RFC 8615](https://tools.ietf.org/html/rfc8615) - and for that matter to define a standard query location, and then a very simple query language.

A parameter for what you want to see (`block`, `account`, `tx`, `token`), and one for where to find it…

The Eth way might be to encode the query in some hex format, with one byte for what you want an the rest for where to find it.

The “old web” way would be to defined a semi-readable parameter string like https://scanner.example.org/.well-known/EthExplorer?item:block;location:ace98769865cedfed or https://scanner.example.org/.well-known/EthExplorer?type:account;location:018fded5eedfed01812;chainid+networkid or something.

---

**ligi** (2023-02-10):

[@chaals](/u/chaals) I respectfully disagree - this EIP perfectly fulfilled it’s purpose of getting uniform routes for explorers - before the EIP it was a mess - this EIP created a shelling point and explorers converged to using the same routes. I fail to see the advantages of using well-known here - only disadvantages of less e.g. not having “This EIP was designed with existing API routes in mind to reduce disruption.” Wondering what advantages you see in using .well-known so it would make more sense?

That said: you could create another EIP to go the well-known way - I just think it will be an uphill battle to get explorers to adopt - but I think this EIP should not be changed.

PS: resurrecting this EIP here: [Polish & Resurrect EIP3091 by ligi · Pull Request #6491 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6491) - really hope we can move it to final soon

PPS: also currently creating a CAIP derived from this work: [Add BlockExplorer-routes CAIP by ligi · Pull Request #200 · ChainAgnostic/CAIPs · GitHub](https://github.com/ChainAgnostic/CAIPs/pull/200)


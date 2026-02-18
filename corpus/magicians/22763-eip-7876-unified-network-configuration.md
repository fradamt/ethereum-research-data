---
source: magicians
topic_id: 22763
title: "EIP-7876: Unified network configuration"
author: bogdan
date: "2025-02-04"
category: EIPs > EIPs Meta
tags: [json, configuration]
url: https://ethereum-magicians.org/t/eip-7876-unified-network-configuration/22763
views: 70
likes: 0
posts_count: 1
---

# EIP-7876: Unified network configuration

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9312)














####


      `ethereum:master` ← `bogdan:master`




          opened 09:01AM - 03 Feb 25 UTC



          [![bogdan](https://avatars.githubusercontent.com/u/122436?v=4)
            bogdan](https://github.com/bogdan)



          [+636
            -0](https://github.com/ethereum/EIPs/pull/9312/files)







This standard defines a universal format for specifying network configurations i[…](https://github.com/ethereum/EIPs/pull/9312)n decentralized applications (dApps). The configuration includes essential information about Ethereum networks, such as:

* available RPC URLs
* native currencies
* contract addresses
*  block explorers.

The goal of this standard is to simplify network configuration for dApp developers and enhance interoperability across Ethereum-compatible networks.

```json
{
  "version": "0.0.1",
  "timestamp": "2025-01-01T12:22:46.471Z",
  "summary": "NFT Artwork",
  "description": "Artwork published by independent artist. Carefully crafted with style in one of the creative studios of the world."
  "abiRoot": "https://nft-artwork.example.com/developer/abi"
  "networks": {
    "1": {
      "name": "Ethereum Mainnet",
      "testnet": false,
      "nativeCurrency": {
        "name": "Ether",
        "symbol": "ETH",
        "decimals": 18
      },
      "rpcs": {
        "main": {
          "url": "https://eth-rpc.example.com"
        },
        "backup": {
          "url": "https://eth-rpc.backup.example.com"
        }
      },
      "relations": {
        "mainnetChainId": null,
        "parentChainId": null
      },
      "explorers": {
        "megascan": {
          "root": "https://example.org",
          "block": "/block/:number",
          "address": "/address/:address",
          "tx": "/tx/:tx",
          "nft": "/nft/:address/:token"
        },
        "marketplace": {
          "root": "https://nft.marketplace/networks/eth",
          "block": null,
          "address": "/:address",
          "tx": null,
          "nft": "/:address/:token"
        }
      },
      "contracts": {
        "Registry": {
          "address": "0x57928ff7b0BBc3Ee4D84481e320DdB8B941f986A",
          "blockCreated": 1234567,
          "abiUrl": "./Registry.sol/Registry.json"
        },
        "OwnerWallet": {
          "address": "0xC12237E57B088e9191BD8054Df4f5B772646a4B6",
          "blockCreated": 1
        }
      }
    },
    "11155111": {
      "name": "Sepolia",
      "testnet": true,
      "nativeCurrency": {
        "name": "Sepolia Ether",
        "symbol": "ETH",
        "decimals": 18
      },
      "rpcs": {
        "main": {
          "url": "https://sepolia-rpc.example.com"
        },
        "backup": {
          "url": "https://sepolia-rpc.backup.example.com"
        }
      },
      "relations": {
        "mainnetChainId": 1,
        "parentChainId": null
      },
      "explorers": {
        "megascan": {
          "root": "https://sepolia.example.org",
          "block": "/block/:number",
          "address": "/address/:address",
          "tx": "/tx/:tx",
          "nft": "/nft/:address/:token"
        },
        "marketplace": {
          "root": "https://testnets.nft.marketplace/networks/sepolia",
          "block": null,
          "address": "/:address",
          "tx": null,
          "nft": "/:address/:token"
        }
      },
      "contracts": {
        "Registry": {
          "address": "0xE13471e6E5d11205AF290261f42108f89dCae72E",
          "blockCreated": 183882,
          "abiUrl": "./Registry.sol/Registry.json"
        },
        "OwnerWallet": {
          "address": "0xC12237E57B088e9191BD8054Df4f5B772646a4B6",
          "blockCreated": 1
        }
      }
    }
  }
}
```

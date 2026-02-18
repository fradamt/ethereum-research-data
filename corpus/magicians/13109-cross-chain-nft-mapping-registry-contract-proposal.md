---
source: magicians
topic_id: 13109
title: Cross-Chain NFT Mapping Registry Contract Proposal
author: hanbsd
date: "2023-03-01"
category: EIPs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/cross-chain-nft-mapping-registry-contract-proposal/13109
views: 791
likes: 7
posts_count: 6
---

# Cross-Chain NFT Mapping Registry Contract Proposal

---

## title: Cross-Chain NFT Mapping Registry Contract
description: A universal registry smart contract where an NFT contract owner can register its mapping contract for each secondary blockchain.
author: Zheng Han , Ming Jiang , Fan Yang
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2023-02-28
requires: EIP-173

## Abstract

This standard defines a registry where an NFT contract on Ethereum can register its mapping contract for each secondary blockchain, be it L1 or L2.

Through this way, developers are able to publish their NFTs on Ethereum while moving sophisticated application like IP licensing and derivative generation onto the secondary blockchain where it is more affordable and scalable.

Only the owner of an NFT contract on Ethereum can modify the mapping information for this contract in the registry. Anyone can query the registry to find out the deputy contract on each secondary blockchain for an Ethereum NFT contract.

## Motivation

This all started from the idea of implementing an IP licensing solution for NFTs. As we know, many NFT projects have generated derivative NFT collections on Ethereum, such as Mutant Ape Yachet Club derived from Bored Ape Yachet Club, and Space Doodles derived from Doodles. However, those collections are only called “derivative” but no actual derivative relations are ever recorded on-chain. We need to extend the NFT contract to add derivative relations as new metadata.

Furthermore, if we want to implement a full IP licensing solution, more licensing metadata along with the required enforcing logic will also be needed. For example, an NFT token holder may want to sell a derivative right to the public but doesn’t want the derivative token to be tradable; or the holder may want to rent out the token and charge by the use of it counted via oracle. The computation can be even more costly when we consider the fact that new tokens can be derived from multiple tokens and derivatives can have derivatives and so on.

Fortunately, many secondary blockchains, be it L1 or L2 to Ethereum, have emerged to be more affordable and scalable making the application logic we need feasible. Therefore, what we decide is to mirror the NFTs from Ethereum to the secondary blockchain and perform all the operations of derivative extension and licensing logic over there.

That leads to the idea of this design document, by standardizing a universal registry smart contract to record the mirroring relations. Copycats could appear on secondary blockchains, but the registry is there to tell which ones are the authentic deputy contracts endorsed by the original NFT project on Ethereum.

Once we implement the aforementioned IP licensing solution, it is also straightforward to verify whether any derivative NFT token generated on a secondary blockchain is officially licensed by tokens from some Ethereum NFT collections, by tracing along the derivative relations on the secondary blockchain to the root contracts and check them against the Ethereum NFT contracts in the registry.

## Specification

The following shows the complete code of the registry contract.

```solidity
pragma solidity ^0.8.0;

struct Chain {
    string network;
    uint256 id;
}

interface IOwner {
    function owner() external view returns (address owner);
}

contract TokenRegistry {

    mapping(address => mapping(string => mapping(uint256 => address))) private _secondaryTokenAddrRegistry;

    event SecondaryTokenAddressChanged(
        address indexed primaryAddr,
        Chain indexed secondaryChain,
        address indexed newSecondaryAddr
    );

    modifier validAddress(address addr) {
        require(addr != address(0), "Invalid address");
        _;
    }

    modifier onlyContractOwner(address addr) {
        require(msg.sender == IOwner(addr).owner());
        _;
    }

    function getSecondaryTokenAddress(
        address primaryAddr,
        Chain memory secondaryChain
    ) external view validAddress(primaryAddr) returns (address) {
        return _secondaryTokenAddrRegistry[primaryAddr][secondaryChain.network][secondaryChain.id];
    }

    function setSecondaryTokenAddress(
        address primaryAddr,
        Chain memory secondaryChain,
        address newSecondaryAddr
    ) external validAddress(primaryAddr) onlyContractOwner(primaryAddr) {
        _secondaryTokenAddrRegistry[primaryAddr][secondaryChain.network][secondaryChain.id] = newSecondaryAddr;
        emit SecondaryTokenAddressChanged(primaryAddr, secondaryChain, newSecondaryAddr);
    }

}
```

## Rationale

(TBD: Key points and short answers as follows)

1. Discuss about using type string for network in the structure of Chain instead of uint256. (Answer: Not all secondary blockchains have an integer ID for their network, but true for chain ID.)
2. Discuss about using owner() (defined in EIP-173) for access control instead of the NFT contract itself. (Answer: There is no way for existing deployed NFT contracts to register sending from the contract itself; in reality, contract owner is usually the operating team of the NFT.)
3. Discuss about whether we should check the address registered is indeed an NFT contract. (Answer: What is an NFT contract is not standardized, as we see ERC1155 and more to come out in addition to ERC721; it is also difficult to verify that for addresses in the secondary blockchain.)

## Backwards Compatibility

No backwards compatibility issues found.

## Test Cases

Test cases available in the repository: [comoco-labs/nft-registry](https://github.com/comoco-labs/nft-registry)

## Reference Implementation

Reference implementation available in the repository: [comoco-labs/nft-registry](https://github.com/comoco-labs/nft-registry)

## Security Considerations

No security considerations found.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**hanbsd** (2023-03-01):

Here are a few graphs showing how cross-chain mapping and licensing works:

1. NFT collections/tokens license to utilities(derivative NFT) on other chains
nft1440×810 60.5 KB
2. AI training dataset license to trained models (also a kind of derivative) based on the dataset
AI Dataset & Models1440×810 32.9 KB
3. Source code license to other code repo or generate an API (also a kind of derivative) based on the source code.
Code & API1440×810 33.8 KB

---

**coripple** (2023-03-19):

Sounds interesting. I’ve actually been looking into Layer 2 solution. Do you have any showcase for cross-chain NFT mapping?

---

**Dick** (2023-03-19):

(post deleted by author)

---

**minkyn** (2023-03-21):

The registry contract we proposed is much like what is proposed in EIP-1820 in terms of its singleton. Therefore, we recently updated the deployment script to adopt the keyless method, aka Nick’s method, just like EIP-1820 did.

The registry contract has been deployed to Goerli Testnet and can be found at:

https://goerli.etherscan.io/address/0x6c5713cc78bef0ff395f2216377eaf3dbda56400

---

**minkyn** (2023-03-22):

I’ll walk you through how we did the derivative NFT cross-chain.

Say we have two NFT contracts from Ethereum, which we created at Goerli Testnet:

```auto
const AVATAR_CONTRACT_GOERLI = "0x4E929f62B418516129814D1AcdB618Ef4eF05078";

const LOGO_CONTRACT_GOERLI = "0xf0bf6cba676516B8b62ec92c26be10644393960D";

```

Suppose we want to derive new NFTs from those two in Polygon. We would first create their mapping contracts. We use a self-developed contract `DerivativeToken` here, which is essentially ERC721 with extra metadata recording their derived parents. We have pre-created those contracts in Polygon Mumbai:

```auto
const AVATAR_CONTRACT_POLYGON = "0xd24264e0245e87e2965e6C4BedA7E77d85731475";

const avatarMappingContract = await ethers.getContractAt("DerivativeToken", AVATAR_CONTRACT_POLYGON);

const LOGO_CONTRACT_POLYGON = "0x2934066f8e279a59A4C5d1729a37eFe0D39Ff658";

const logoMappingContract = await ethers.getContractAt("DerivativeToken", LOGO_CONTRACT_POLYGON);

```

Now we need to register the mapping relationship in the proposed registry. For this showcase purpose, we created a sample registry contract at:

```auto
const REGISTRY_CONTRACT_GOERLI = "0x206a6fd631225f211a2d35f47af2d347c7b90801";

```

And here is how you would register at the contract:

```auto
const registry = await ethers.getContractAt("TokenRegistry", REGISTRY_CONTRACT_GOERLI);

await contract.setSecondaryTokenAddress(AVATAR_CONTRACT_GOERLI, { network: "polygon", id: 80001 }, AVATAR_CONTRACT_POLYGON);

await contract.setSecondaryTokenAddress(LOGO_CONTRACT_GOERLI, { network: "polygon", id: 80001 }, LOGO_CONTRACT_POLYGON);

```

Now that we have created the mapping contracts in Polygon, we could generate further contracts derived from them. First, we would deploy a `DerivativeToken` contract and mint a token deriving from `AVATAR_CONTRACT_POLYGON`.

```auto
const AVATAR_DNFT_CONTRACT = "0x98aEf158Ad18EAA720c394042562c878f45494d7";

const avatarDNFTContract = await ethers.getContractAt("DerivativeToken", AVATAR_DNFT_CONTRACT);

const parentTokens = [{ collection: avatarMappingContract.address, id: 0 }];

await avatarDNFTContract.mint(holder.address, 0 /* id */, parentTokens, RES_BASE_URL + "avatar_dnft/avatar_dnft_0.json");

```

Then we do the same for `LOGO_CONTRACT_POLYGON`.

```auto
const LOGO_DNFT_CONTRACT = "0x84e57e5fd46E54d39df64AD1e00f3D4A59fa5e35";

const logoDNFTContract = await ethers.getContractAt("DerivativeToken", LOGO_DNFT_CONTRACT);

const parentTokens = [{ collection: logoMappingContract.address, id: 0 }];

await logoDNFTContract.mint(holder.address, 0 /* id */, parentTokens, RES_BASE_URL + "logo_dnft/logo_dnft_0.json");

```

Last, we could even mint a token deriving from multiple parent tokens.

```auto
const AVATAR_LOGO_DNFT_CONTRACT = "0x44B0810153a3b5e7a3555645691e3bda936413e7";

const avatarLogoDNFTContract = await ethers.getContractAt("DerivativeToken", AVATAR_LOGO_DNFT_CONTRACT);

const parentTokens = [{ collection: avatarDNFTContract.address, id: 0 }, { collection: logoDNFTContract.address, id: 0 }];

await avatarLogoDNFTContract.mint(holder.address, 0 /* id */, parentTokens, RES_BASE_URL + "avatar_logo_dnft/avatar_logo_dnft.json");

```

At the end, we have a series of derivative tokens created in Polygon, whose root contracts are `AVATAR_CONTRACT_POLYGON` and `LOGO_CONTRACT_POLYGON` that are mapped from `AVATAR_CONTRACT_GOERLI` and `LOGO_CONTRACT_GOERLI`, and the mapping relationships are registered in the registry contract.


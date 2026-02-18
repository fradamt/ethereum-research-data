---
source: magicians
topic_id: 20503
title: "ERC-7738: Permissionless Script Registry"
author: JamesB
date: "2024-07-09"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7738-permissionless-script-registry/20503
views: 478
likes: 1
posts_count: 2
---

# ERC-7738: Permissionless Script Registry

Discussion topic for EIP-7738

This is the discussion on a draft EIP for an onchain script registry.

## Abstract

This EIP provides a means to create a standard registry for locating executable scripts associated with contracts.

## Motivation

[ERC-5169](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-5169.md) (`scriptURI`) provides a client script lookup method for contracts. This requires the contract to have implemented the ERC-5169 interface at the time of construction (or allow an upgrade path).

This proposal outlines a contract that can supply prototype and certified scripts. The contract would be a singleton instance multichain that would be deployed at identical addresses on supported chains.

### Overview

The registry contract will supply a set of URI links for a given contract address. These URI links point to script programs that can be fetched by a wallet, viewer or mini-dapp.

The pointers can be set using a setter in the registry contract.

The scripts provided could be authenticated in various ways:

1. The target contract which the setter specifies implements the Ownable interface. Once the script is fetched, the signature can be verified to match the Owner(). In the case of TokenScript this can be checked by a dapp or wallet using the TokenScript SDK, the TokenScript online verification service, or by extracting the signature from the XML, taking a keccak256 of the script and ecrecover the signing key address.
2. If the contract does not implement Ownable, further steps can be taken:
a. The hosting app/wallet can acertain the deployment key using 3rd party API or block explorer. The implementing wallet, dapp or viewer would then check the signature matches this deployment key.
b. Signing keys could be pre-authenticated by a hosting app, using an embedded keychain.
c. A governance token could allow a script council to authenticate requests to set and validate keys.

If these criteria are not met:

- For mainnet implementations the implementing wallet should be cautious about using the script - it would be at the app and/or user’s discretion.
- For testnets, it is acceptable to allow the script to function, at the discretion of the wallet provider.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY” and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

The contract MUST implement the IDecentralisedRegistry interface.

The contract MUST emit the ScriptUpdate event when the script is updated.

The contract SHOULD order the scriptURI returned so that the owner script is returned first (in the case of simple implementations the wallet will pick the first scriptURI returned).

```solidity
interface IDecentralisedRegistry {
    /// @dev This event emits when the scriptURI is updated,
    /// so wallets implementing this interface can update a cached script
    event ScriptUpdate(address indexed contractAddress, string[] newScriptURI);

    /// @notice Get the scriptURI for the contract
    /// @return The scriptURI
    function scriptURI(address contractAddress) external view returns (string[] memory);

    /// @notice Update the scriptURI
    /// emits event ScriptUpdate(address indexed contractAddress, scriptURI memory newScriptURI);
    function setScriptURI(address contractAddress, string[] memory scriptURIList) external;
}
```

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

## Rationale

This method allows contracts written without the ERC-5169 interface to associate scripts with themselves, and avoids the need for a centralised online server, with subsequent need for security and the requires an organisation to become a gatekeeper for the database.

## Reference Implementation

```solidity
import "@openzeppelin/contracts/access/Ownable.sol";

contract DecentralisedRegistry is IDecentralisedRegistry {
    struct ScriptEntry {
        mapping(address => string[]) scriptURIs;
        address[] addrList;
    }

    mapping(address => ScriptEntry) private _scriptURIs;

    function setScriptURI(
        address contractAddress,
        string[] memory scriptURIList
    ) public {
        require (scriptURIList.length > 0, "> 0 entries required in scriptURIList");
        bool isOwnerOrExistingEntry = Ownable(contractAddress).owner() == msg.sender
            || _scriptURIs[contractAddress].scriptURIs[msg.sender].length > 0;
        _scriptURIs[contractAddress].scriptURIs[msg.sender] = scriptURIList;
        if (!isOwnerOrExistingEntry) {
            _scriptURIs[contractAddress].addrList.push(msg.sender);
        }

        emit ScriptUpdate(contractAddress, msg.sender, scriptURIList);
    }

    // Return the list of scriptURI for this contract.
    // Order the return list so `Owner()` assigned scripts are first in the list
    function scriptURI(
        address contractAddress
    ) public view returns (string[] memory) {
        //build scriptURI return list, owner first
        address contractOwner = Ownable(contractAddress).owner();
        address[] memory addrList = _scriptURIs[contractAddress].addrList;
        uint256 i;

        //now calculate list length
        uint256 listLen = _scriptURIs[contractAddress].scriptURIs[contractOwner].length;
        for (i = 0; i  0) {
                    ownerScripts[scriptIndex++] = thisScriptURI;
                }
            }
        }

        //fill remainder of any removed strings
        for (i = scriptIndex; i < listLen; i++) {
            ownerScripts[scriptIndex++] = "";
        }

        return ownerScripts;
    }
}
```

## Replies

**zhangzhongnan928** (2024-07-16):

I believe, adding scripts to tokens can evolve the concept of tokens in Web3. Let’s explore this idea:

1. Tokens as Interactive Ownership Entities:

- Currently, tokens often represent static ownership, with DApps providing the interface and functionality.
- The vision is to make tokens themselves interactive, encapsulating both ownership and functionality.

1. Self-Contained User Experience:

- Imagine tokens that carry their own UI and logic, not just ownership data.
- Users could interact directly with the token, without needing a separate DApp interface.

1. Portable Functionality:

- An interactive token could be used across different platforms while maintaining its core functionality.
- For example, a concert ticket token could display event details, allow entry, and facilitate resale, regardless of which wallet or marketplace it’s viewed in.

1. Direct Interaction Points:

- Tokens could become primary interaction points, similar to websites or mobile apps.
- Users might “open” a token to access its features, rather than opening a separate DApp.

1. Enhanced Ownership Experience:

- Tokens could provide real-time updates, dynamic content, and interactive features directly.
- For instance, a property ownership token could show current value, allow for maintenance scheduling, or even control smart home features.

1. Reduced Platform Dependence:

- By encapsulating functionality within tokens, dependence on specific DApps or platforms could be reduced.
- This aligns with Web3’s goal of decentralization and user control.

1. Challenges to Address:

- Ensuring security when tokens carry executable code.
- Standardizing how different systems interact with these enhanced tokens.
- Creating intuitive user experiences for interacting directly with tokens.

1. Evolution of Web3 Interfaces:

- This could lead to a paradigm shift where users primarily interact with their owned tokens rather than platform-specific interfaces.
- Wallets might evolve into more general-purpose “token interaction environments”.

This concept of tokens as primary interaction points represents a significant evolution in how we think about digital ownership and interaction in Web3. It moves tokens from being passive representations of ownership to active, self-contained digital objects that users can directly engage with, potentially revolutionizing our interaction with digital assets and services.

This ERC-7738 further enables anyone to add any script to any token. Basically, developers can add different experiences to any existing/new tokens for users to use.


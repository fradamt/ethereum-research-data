---
source: magicians
topic_id: 26734
title: Social Media Dapp Algorithm Adjuster
author: VibeCoderLoveEth
date: "2025-11-27"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/social-media-dapp-algorithm-adjuster/26734
views: 33
likes: 0
posts_count: 1
---

# Social Media Dapp Algorithm Adjuster

Hi - interested in a social media Dapp that allows people to adjust there own algorithm. I’ve used vibe coding to make one in solidity (just algorithm adjuster). In my head it would just be a simple scroll through news articles you’d like to see. You could then share and like each others algorithms. Really not very good at this sort of thing though. I figured this could be a start. Is anyone doing something similar. I think I’d really struggle by myself. Code below.

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

/// @title AlgorithmRegistry
/// @author
/// @notice Registry and user-preference store for feed/algorithm implementations.
/// Algorithms are referenced by URI (IPFS/HTTP/ENS) and an owner (developer) can update them.
/// Users set which algorithm they prefer. Admin can deprecate harmful entries.
///
/// NOTE: This contract only stores references and preferences. Algorithm execution must be off-chain.

contract AlgorithmRegistry {
    // --- Simple Ownable (for governance/admin) ---
    address public owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() {
        owner = msg.sender;
        emit OwnershipTransferred(address(0), msg.sender);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Owner only");
        _;
    }

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Zero");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }

    // --- Algorithm storage ---
    struct Algorithm {
        address developer;    // who registered it
        string uri;           // pointer to implementation (IPFS CID, HTTPS, ENS)
        string metadata;      // JSON metadata or short description (e.g. JSON schema)
        bool active;          // deprecated = false
        uint256 createdAt;
        uint256 updatedAt;
    }

    Algorithm[] private algorithms; // algorithmId = index in this array

    // maps user -> chosen algorithmId (index). 0xFFFFFFFF... means none.
    mapping(address => uint256) public userAlgorithm;

    // optional: allow registry managers to set preference for other users (delegation)
    mapping(address => mapping(address => bool)) public delegates; // user => delegate => allowed

    // Events
    event AlgorithmRegistered(uint256 indexed id, address indexed developer, string uri, string metadata);
    event AlgorithmUpdated(uint256 indexed id, address indexed developer, string uri, string metadata);
    event AlgorithmDeprecated(uint256 indexed id, address indexed admin, bool active);
    event UserAlgorithmSet(address indexed user, uint256 indexed algorithmId);
    event DelegateSet(address indexed user, address indexed delegate, bool allowed);

    // sentinel value meaning "no selection"
    uint256 public constant NO_SELECTION = type(uint256).max;

    // --- Constructor continues: initialize empty list with no algorithms ---
    // (not necessary, but we can push a dummy so id 0 is real; here we just leave array empty)

    // --- Modifiers ---
    modifier validAlgorithmId(uint256 id) {
        require(id = algorithms.length) {
            return "";
        }
        Algorithm storage a = algorithms[id];
        if (!a.active) return "";
        return a.uri;
    }

    // --- Registration & updates ---

    /// @notice Register a new algorithm implementation (URI + metadata).
    /// @param uri pointer to implementation (IPFS CID, https, ENS)
    /// @param metadata short metadata string (JSON or description)
    /// @return id registered algorithm id
    function registerAlgorithm(string calldata uri, string calldata metadata) external returns (uint256 id) {
        require(bytes(uri).length > 0, "URI required");
        Algorithm memory a = Algorithm({
            developer: msg.sender,
            uri: uri,
            metadata: metadata,
            active: true,
            createdAt: block.timestamp,
            updatedAt: block.timestamp
        });
        algorithms.push(a);
        id = algorithms.length - 1;
        emit AlgorithmRegistered(id, msg.sender, uri, metadata);
    }

    /// @notice Update your algorithm's URI/metadata
    function updateAlgorithm(uint256 id, string calldata uri, string calldata metadata) external validAlgorithmId(id) onlyDeveloper(id) {
        require(bytes(uri).length > 0, "URI required");
        Algorithm storage a = algorithms[id];
        a.uri = uri;
        a.metadata = metadata;
        a.updatedAt = block.timestamp;
        emit AlgorithmUpdated(id, msg.sender, uri, metadata);
    }

    /// @notice Admin can deprecate/reactivate an algorithm (useful for abuse/time).
    function setAlgorithmActive(uint256 id, bool active) external validAlgorithmId(id) onlyOwner {
        algorithms[id].active = active;
        algorithms[id].updatedAt = block.timestamp;
        emit AlgorithmDeprecated(id, msg.sender, active);
    }

    // --- User preferences ---

    /// @notice User sets their own preferred algorithm id (or clear by passing NO_SELECTION)
    function setMyAlgorithm(uint256 id) external {
        if (id != NO_SELECTION) {
            require(id = n) return batch;
        uint256 end = start + count;
        if (end > n) end = n;
        uint256 len = end - start;
        batch = new Algorithm[](len);
        for (uint256 i = 0; i < len; ++i) {
            batch[i] = algorithms[start + i];
        }
    }
}
```

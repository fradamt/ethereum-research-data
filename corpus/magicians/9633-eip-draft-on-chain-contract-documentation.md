---
source: magicians
topic_id: 9633
title: "EIP Draft: On-Chain contract documentation"
author: MidnightLightning
date: "2022-06-15"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-draft-on-chain-contract-documentation/9633
views: 668
likes: 0
posts_count: 3
---

# EIP Draft: On-Chain contract documentation

This idea came about from the [ponderware](https://www.ponderware.com/) team as we decided on a structure for making as robust a means possible for [providing on-chain information about their MoonCatRescue project](https://mooncat.community/blog/onchain). For that implementation, a [MoonCatReference](https://etherscan.io/address/0x0B78C64bCE6d6d4447e58b09E53F3621f44A2a48#code) contract was devised to be a central documentation store. From my initial searches I don’t believe a standard like this has already been proposed? If on-chain links/documentation were done in a standard way, that could allow wallets and other end-user interfaces to automatically parse smart contracts and get additional information about the contracts for the user to decide if they wish to interact with them.

Starting to flesh out this idea into an EIP:

---

## Abstract

The bytecode data stored for smart contracts strives to be efficient for computation, but that makes it not human-friendly to read over. Solidity source code that generates the bytecode for the contract can include comments and specify variable names and function names to be clear to human readers, but that source code is not an on-chain record and could be more readily lost/destroyed than the smart contract itself. Having some means for a smart contract to present some human-friendly documentation would be helpful for future users looking to interact with the smart contracts, even if the original creator is no longer available or the original source code is lost.

## Motivation

Provide a consistent means for smart contract developers to communicate their intent to users on-chain. Many users find out about specific smart contracts through a project’s website. This can be an okay way to create a mental link between the documentation and information from a project team and the implementation on-chain, but it is susceptible to a user being tricked by a phishing website that looks like a popular project but points to a different contract. Having a consistent name and documentation link could allow wallet software to help bring it to user’s attention when things aren’t what they expect.

## Specification

For this standard, a Documentation Repository contract is defined, as well as an interface that contracts can implement.

### Documentation Repository

The Documentation Repository serves as a single point that saves data about many different contracts. The intent is that many Documentation Repositories would exist, each offering up their list of metadata, and users could pick and choose between them of which repositories they trust to give good information.

```auto
pragma solidity ^0.8.9;

/**
 * @title Documentation Repository
 * @dev Contract to store human-readable metadata about other smart contracts
 */
interface DocumentationRepository {
  /**
   * @notice Metadata about a specific smart contract
   * @dev Consistent data structure for on-chain information about a smart contract.
   */
  struct ContractMeta {
    uint256 chainId;
    address contractAddress;
    string name;
    string description;
    string URI;
  }

  /**
   * @notice Fetch information about a smart contract
   * @dev Throws if this repository has no information about `contractAddress`.
   * @param chainId The blockchain identifier the requested contract is on.
   * @param contractAddress The smart contract address being inquired about.
   * @return The metadata for the contract specified in the input parameters.
   */
  function getDocumentation (uint256 chainId, address contractAddress) external view returns (
    string name,
    string description,
    string URI
  );

  /**
   * @notice Fetch information about a smart contract
   * @dev Assumes that the chain being inquired about is the same chain this repository is deployed onto.
   *  Throws if this repository has no information about `contractAddress`.
   * @param contractAddress The smart contract address being inquired about.
   * @return The metadata for the contract specified in the input parameters.
   */
  function getDocumentation (address contractAddress) external view returns (
    string name,
    string description,
    string URI
  );

  /**
   * @notice Bulk query to fetch information about multiple smart contracts at once
   * @dev If the repository has no information about one of the input `contractAddresses`, that `contractAddress` is omitted from the return array.
   * @param chainIds The blockchain identifiers the requested contracts are on.
   * @param contractAddresses The smart contract addresses being inquired about.
   * @return The metadata for the contracts specified in the input parameters.
   */
  function getDocumentation (uint256[] chainIds, address[] contractAddresses) external view returns (ContractMeta[]);
}

/**
 * @title Documentation Repository, optional enumeration extension
 * @dev Provide the means to iterate through all records in the repository, without prior knowing which specific addresses it has stored.
 */
interface DocumentationRepositoryEnumerable {
  /**
   * @notice Count smart contracts tracked in this repository.
   * @return A count of valid documentation metadata objects tracked in this contract.
   */
  function totalContracts () external view returns (uint256);

  /**
   * @notice Enumerate valid metadata records in this repository.
   * @dev Throws if `index` >= `totalContracts()`
   * @param index A counter less than `totalContracts()`
   * @return The metadata for the `index`th metadata record.
   */
  function contractByIndex (uint256 index) external view returns (ContractMeta);

  /**
   * @notice Enumerate valid metadata records in this repository.
   * @dev If the repository has no information about one of the input `indexes` values, that `index` is omitted from the return array.
   * @param indexes An array of counters, each less than `totalContracts()`
   * @return The metadata for all the valid contracts requested
   */
  function getDocumentation (uint256[] indexes) external view returns (ContractMeta[]);
}
```

Each Documentation Repository instance is expected to have its own governance/ownership model on how they add and update information into the repository, which is separate from this standard and individual users can choose what level of curation/review they expect from the Documentation Repository owner(s) they opt in to.

The metadata about each smart contract includes the chain ID and address as identifiers, and then three bits of data that are subjective:

- name: A string that is a short label for the contract
- description: An optional string that is a longer phrase to describe the contract
- URI: A distinct Uniform Resource Identifier (URI) a user can go to find additional data about the contract

The `name` and `description` are both `string` values that don’t impose length maximums, so it’s up to the Repository instance to decide how long is appropriate. The longer these values are, the more costly to store on-chain, so Repository managers should provide at least enough information for end-users to decide if they want to learn more as a minimum, and may be more verbose in these values if desired.

The `URI` value should contain a way for a user to learn more about that contract. This could be a link to the project website for that smart contract, or a website run by the Documentation Repository managers to profile the project that smart contract belongs to, or a link to a JSON data object with additional structured data about the smart contract. The URI value must adhere to the [RFC3986](https://datatracker.ietf.org/doc/html/rfc3986) standard. Most commonly, Documentation Repositories should aim to use `https://`, `ipfs://` or `data://` schemes for the URI links for more information.

### Smart Contract self-documentation

```auto
pragma solidity ^0.8.9;

/**
 * @title Self-documenting smart contract
 * @dev Provide the means for a smart contract to identify which repository it trusts to give valid metadata about itself.
 */
interface DocumentedContract {
  function DocumentationRepository () external view returns (uint256 chainId, address contractAddress);

  function getDocumentation () external view returns (
    string name,
    string description,
    string URI
  );
}

```

## Rationale

Having multiple Documentation Repositories sets up a structure similar to the “token lists” concept that has become used in several Automated Market Maker (AMM) coin swap sites (different “authorities” can create their own lists of tokens that they’ve vetted, and each user can decide for themselves which authorities they trust to give good data, and pull those in as the references to use when picking tokens for a swap). Repositories could be curated by just an individual (could be a “personal” Documentation Repository for one person’s notes), a project team, a whole corporation, or larger consortium, each with their own goals of which sorts of contracts they want to focus on.

Bulk lookup functions provide options for a UI to reduce the number of network requests it needs to make to an Ethereum node for information about a suite of contracts it is interested in.

Separating the Enumeration properties into an optional extension (having `DocumentationRepository` and `DocumentationRepositoryEnumerable` rather than one combined one) follows the pattern of ERC721 and other token standards, which allows implementations to choose for themselves if the additional cost to store the enumeration indexes on-chain is worth the benefits they give.

Having repositories of documentation metadata be separate from the contracts themselves (rather than just having contracts implement a `getDocumentation` function that self-reports their metadata) allows end-users to know where to place their trust. With self-reporting, malicious contracts could return whatever lie they wanted (to try and impersonate a legitimate contract). With organized central repositories, a user can do the research into which repositories they want to trust rather than which individual contracts they want to trust, which should be less number of contracts for an end-user to review. Currently block explorers like Etherscan provide tagging/labeling options for users that are either from the team running the website (centralized) or custom-set by the individual user. But those bits of data are siloed in the individual block explorer sites (so could be more easily lost/censored than on-chain data).

Having the metadata for each smart contract includes a chain identifier to allow for the possibility of a Documentation Repository existing on a separate sidechain from the contracts it documents allows for Documentation Repository managers to set up on a different sidechain (which they may desire for gas-cost efficiencies), allows for multi-chain projects to all be documented in one Repository, and allows a Repository on one chain have an authoritative link to a Repository on another chain (if a group of managers curate Repositories on multiple chains, it allows users to trust the links between them). The downside to this method is for smart contract self-reporting, if the `DocumentationRepository()` for a contract is on another chain, the `getDocumentation()` result from that smart contract will not be able to just be a pass-through to the Repository, and will need to be some manual data (should be instructions how to connect to the Repository on the other chain).

## Reference Implementation

TODO

## Security Considerations

TODO

## Copyright

Copyright and related rights waived via [CC0](/LICENSE).

## Replies

**danfinlay** (2022-06-15):

[EIP 4430](https://eips.ethereum.org/EIPS/eip-4430) sounds similar/related. In its case, you have each contract responsible for reporting its own metadata.

For helping spread knowledge of metadata for contracts that don’t have this (backwards compat), I know [@Kames](/u/kames) is experimenting with making [a sort of web of trust registry like this](https://github.com/eth-experiments/eip-4430-sol) (in progress).

These approaches require a connection to the network, or struggle with backwards compat, or introduce a trusted third party for sourcing data, so I just wrote a new EIP aiming to address the same general problem here: [EIP: Rich Site-Proposed Contract Metadata](https://ethereum-magicians.org/t/eip-rich-site-proposed-contract-metadata/9635)

---

**MidnightLightning** (2022-06-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> EIP 4430 sounds similar/related. In its case, you have each contract responsible for reporting its own metadata.

This one seems to have the additional nuance of it goes down to the level of defining what a function does, not just what the contract does overall. Trusting the contract authors to be truthful seems to be a big caveat for that method, as if a user finds a report from an auditor saying “I audited contract address A and found it to be truthful”, and an attacker copies the contract with the `Describe` function, the user would have to notice it’s no longer “address A” (as the auditor’s sign-off on the contract is not on-chain for automatic parsing).

The “auditor” role in EIP4430 seems to play a critical role, and in the structure of this proposal I made, the parallel role I think is the Documentation Repository, where it’s “signing off” on different contracts by adding them to its data store?

> These approaches require a connection to the network, or struggle with backwards compat, or introduce a trusted third party for sourcing data

Yes, it involves a level of trust with a third-party, but with the intent that it could lead to a “web of trust” structure in the open, where different data sources could be compared readily. Moving the model be local to each user’s interaction with an Ethereum node I believe mostly cuts it off from seeing what others have done, so there’s still a risk when the user comes to a new contract from a new website they just found, it’s still just as hard to determine if it’s the real site, or a copycat scam site. With a web of trust possibility, upon first visit to a contract, a wallet could indicate “this contract is known/trusted by 3 friends/auditors you know” to bootstrap helping a user decide to trust this contract or not.


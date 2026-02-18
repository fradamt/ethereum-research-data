---
source: magicians
topic_id: 21865
title: "ERC-7827: JSON Smart Contract with Value Version Control"
author: bestape
date: "2024-11-26"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7827-json-smart-contract-with-value-version-control/21865
views: 537
likes: 5
posts_count: 5
---

# ERC-7827: JSON Smart Contract with Value Version Control

| Authors | Kyle Smith (@bestape) , Lex.Clinic (@lexclinic) |
| --- | --- |
| EIP Link | Github |
| Discussions | See MegaZu demo day , EIP Editing Office Hour 47 |
| Status | Draft |
| Type | Standards Track |
| Category | ERC |
| Created | 2024-11-07 |

## Abstract

This EIP defines a smart contract interface that allows for managing a JSON object within a smart contract, offering both real-time JSON output and a version-controlled history for each value.

The interface includes methods to retrieve the most recent JSON state as well as the version history of each key in the JSON object.

This approach supports REST developers familiar with JSON-based data interactions, thus improving accessibility for developers new to Web3 and Ethereum.

## Motivation

With an increasing number of developers from RESTful backgrounds joining the Ethereum ecosystem, there is a need for a contract interface that allows developers to easily interact with structured JSON data.

This EIP aims to create a universal standard that provides JSON data management and version control functionality in a straightforward and REST-like way, making Ethereum more accessible and developer-friendly.

## Specification

The contract interface includes the following methods:

### Read Methods

1. json()

Inputs: None.
2. Output: string (a JSON object as a string)
3. Description: Returns the JSON object in its latest state. The output uses the most recent value for each key in the JSON object, mimicking a REST JSON call.
4. Behavior: Each key in the JSON object reflects the latest “Last In, First Out” (LIFO) state of its value.
5. version(string key)

Inputs:

key (string): The JSON key whose version history is requested.
6. Output: string (a JSON array as a string)
7. Description: Returns an array of all versions of the specified key’s value in JSON format.
The array is ordered chronologically, with the earliest version at index 0 and the most recent version at the highest index.

### Write Method

1. write(string[] keys, string[] values, bool replace)

Inputs:

keys (string[]): Array of JSON key strings, where each key represents a path within the JSON object.
2. values (string[]): Array of JSON-compatible strings corresponding to each key. Can represent primitive types, arrays, or objects.
3. replace (bool): Determines whether to replace an existing key’s latest value.

If replace is true and the key exists, the existing value is updated in the json output.
4. However, the previous value persists in the version output, with the new value appended at the end of the version history array.
5. If replace is false and the key already exists, the transaction reverts.
6. Output: None.
7. Description: Writes new values to the JSON object, either adding a new key or updating an existing one, based on the replace parameter.

#### Additional Requirements

- Universal ABI: To support widespread adoption and ease of use, the ABI should be standardized for REST-like abstraction within popular Web3 libraries.
By making this contract accessible through Web3 abstractions, developers with REST experience can seamlessly interact with the contract.

## Rationale

1. REST-like Access via JSON Method
The json method enables developers to interact with the contract as if it were a RESTful API, improving accessibility for those familiar with traditional web development paradigms.
2. Version Management via Version Method
The version method provides a straightforward version control system for each key, offering a history of values that developers can reference without altering the main JSON structure.
This method maintains immutability for historical values while allowing updates to be appended.
3. Compatibility with Web3 Abstractions
Ensuring a simple and standardized ABI is essential for usability with Web3 libraries, thus enhancing developer experience and facilitating onboarding.

## Example Usage

Assume the following scenario with key-value management:

1. Initial Write:

```solidity
write(["name"], ["Alice"], false);
```

JSON Output after this call:

```json
{ "name": "Alice" }
```
2. Version History of name:

```json
["Alice"]
```
3. Updating Value with Replacement:

```solidity
write(["name"], ["Bob"], true);
```

JSON Output after this call:

```json
{ "name": "Bob" }
```
4. Version History of name:

```json
["Alice", "Bob"]
```
5. Attempting to Update without Replacement (Reverts if name exists):

```solidity
write(["name"], ["Charlie"], false);
```

This transaction would revert as name already exists, and replace is set to false.

## Backwards Compatibility

This EIP is a new standard and does not interfere with existing standards.

However, it introduces JSON object handling and version control, which may have specific considerations for gas optimization.

## Security Considerations

Care should be taken to handle large JSON objects efficiently to avoid excessive gas consumption.

---

# Further Reading

[![RPC calls should be as simple as rest calls](https://ethereum-magicians.org/uploads/default/optimized/2X/d/d984cc56d5917fe591aa8b016410cd6dfd818918_2_690x325.png)RPC calls should be as simple as rest calls991×468 85.4 KB](https://ethereum-magicians.org/uploads/default/d984cc56d5917fe591aa8b016410cd6dfd818918)

Deck [here](https://docs.google.com/presentation/d/1yH5FPRsIztEzV_HzHzxfMHiVoMz8essjxz7xAzKxreY/edit#slide=id.g3113ec1c8a7_0_52).

## Replies

**ryley-o** (2024-11-27):

Cool!

Wanted to call out an unaudited library that I helped publish at Art Blocks that could help with the design and implementation here!

A few notes about it:

- doesn’t have version control
- does allow for nesting/bool/number/string values
- efficiently concatenates per-layer (O(n) for n key/value pairs)
- supports optional base64 encoding to handle special characters

It’s available here: [artblocks-contracts/packages/contracts/contracts/libs/v0.8.x/JsonStatic.sol at main · ArtBlocks/artblocks-contracts · GitHub](https://github.com/ArtBlocks/artblocks-contracts/blob/main/packages/contracts/contracts/libs/v0.8.x/JsonStatic.sol)

---

**bestape** (2024-11-30):

Thank you very much! This is great.

Here’s my most recent deploy, but it’s a different pattern than the one suggested in this first ERC-7287 draft:

https://arbiscan.io/address/0x8dcbc12efe584e24592d07a81bd6f6450def1052

---

**bestape** (2025-08-30):

A lint-flixed version is up for review on Ethereum’s Github. Please take a look and give your opinion here. We still need the read methods within the EVM.

THANK YOU



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/734)














####


      `master` ← `lex-clinic:master`




          opened 02:40PM - 26 Nov 24 UTC



          [![](https://avatars.githubusercontent.com/u/173394432?v=4)
            lex-clinic](https://github.com/lex-clinic)



          [+114
            -0](https://github.com/ethereum/ERCs/pull/734/files)







From https://raw.githubusercontent.com/lexclinic/Templates/refs/heads/main/JSON%[…](https://github.com/ethereum/ERCs/pull/734)20Object%20Management%20with%20Version%20Control%20in%20Smart%20Contracts.md .

Draft created during MegaZu, given demo day feedback.

Following cat herder directions here https://discord.com/channels/916516304972824576/916725260664057916/1310976176013054043 . Please excuse my confusion. This is the first time I've gone through this process.

When opening a pull request to submit a new EIP, please use the suggested template: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

---

**bestape** (2025-09-04):

The permanent record here is the use of the proto-standard: https://snapshot.box/#/s:makerspace.eth/proposal/0x636bb82f90edc79563fe0b164a2eef3170617be175284226ab907a4e60663310


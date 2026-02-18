---
source: magicians
topic_id: 5446
title: EIP-3220 crosschain id specification
author: weijia31415
date: "2021-03-01"
category: EIPs
tags: [interop, eip-3220]
url: https://ethereum-magicians.org/t/eip-3220-crosschain-id-specification/5446
views: 4820
likes: 1
posts_count: 14
---

# EIP-3220 crosschain id specification

This is to create a discussion topic for EIP-3220.

---

## eip: 3220
title: Crosschain Identifier Specification
author: Weijia Zhang (), Peter Robinson ()
status: Draft
type: Standards Track
category: Core
created: 2020-10-21

## Simple Summary

Today chainid definition as specified in EIP-155 is an integer type.  This is not unique enough to identify all public and private blockchains.  A blockchain identifier (crosschain id) should be unique and satisfy the following requirements:

should provide identification, description, and discovery of blockchains.

should provide unique identification of each blockchain in the crosschain service ecosystem.

should provide descriptions for a blockchain identities such as chainId, name, type, consensus scheme etc.

should provide discovery mechanism for supported blockchains and also for new blockchains in the ecosystem.

should provide a mechanism for a joining blockchain to register to the ecosystem.

should provide a mechanism for a blockchain to edit properties or unregister from the crosschain ecosystem.

should provide a mechanism to get some critical information of the blockchain

should provide a mechanism to differentiate an original blockchain and a forked blockchain

should provide a mechanism to verify a chainid without external registration service

Hence we provide a specification for using a 32 byte identifier to represent any blockchain.  We call this identifier crosschain-id.

## Abstract

Crosschain operations include transfer of assets, data, message, events, and commands from one blockchain to another. In order to improve interoperability of crosschain operations, there is a need to uniquely identify source blockchain, target blockchains, and any relay chains that help facilite blockchain information transfer.  The identifier should follow a standard format so that all platforms and decentralize applications can use this identifier to represent a blockchain and also some information in the identifier to get some characteristis of the blockchain.  We name this blockchain identifier as crosschain-id and expect Ethereum community to use crosschain-id to represent any public or private blockchain.  The crosschain-id is a 32 byte hex string and with some bytes extracted from blockchain hash and some manually defined to characterize a blockchain.  We also propose a registration and lookup service to retrieve blockchain metadata from the crosschain-id.

## Motivation

EIP-155 was proposed by Vitalik to provide a unique identifier to a blockchain to provide simple relay attack protection.  This specification defines an integer for Chainid for a blockchain and sign the chainid into a transaction data and hence present attackers to send same transaction to different blockchains. This specification will require blockchains to define a chainid and register the chainid in a public repository.

The challenge of using an integer for chainid is that it is not broad enough to cover all blockchains and it does not prevent different blockchains using the same chainid.  Also, it does not address the issue for two forked blockchains having the same chainid.

Hence there is need for a more robust blockchain identifier that will overcome these drawbacks, especially for crosschain operations where multiple chains are involved.

## Specification

The section specifies a) The crosschain id definition b) the registration smart contract the defines metadata to be associated with a crosschain id; and c) the basic functions to parse and process a crosschain id.

### Definition of a 32 byte crosschain id

| Name | Size(bytes) | Description |
| --- | --- | --- |
| Truncated Block Hash | 16 | This is the block hash of the genesis block or the block hash of of the block immediate prior to the fork for a fork of a blockchain. The 16 bytes is the 16 least significant bytes, assuming network byte order. See table XYZA below for a list of existing blockchains. |
| Native Chain ID | 4 | This is the Chain Id value that should be used with the blockchain when signing transactions. For blockchains that do not have a concept of Chain Id, this value is zero. |
| Chain Type | 2 | See table XYZ below the current list of chain types. |
| Governance Identifier | 2 | For new blockchains, a governance_identifier can be specified to identify an original owner of a blockchain, to help settle forked / main chain disputes. For all existing blockchains and for blockchains that do not have the concept of an owner, this field is zero. |
| Reserved | 7 | Reserved for future use. Use 000000 for now. |
| Checksum | 1 | Used to verify the integrity of the identifier. This integrity check is targeted at detecting Crosschain Identifiers mis-typed by human users. The value is calculated as the truncated SHA256 message digest of the rest of the identifier, using the least significant byte, assuming network byte order. Note that this checksum byte only detects integrity with a probability of one in 256. This probability is adequate for the intended usage of detecting typographical errors by people manually entering the Crosschain Identifier. |

### Definition of crosschain id registration smart contract

The crosschain registration smart contract provides a registration service to crosschain id and its associated meta data.  The smart contract should support the following meta data.

| Metadata Name | Description | Examples |
| --- | --- | --- |
| Crosschain Id | 32 byte hex id | 0xabc. See the crosschain id section for details |
| Long Name | A long naname describing the blockchain.  Maximum length is 80 characters. | This long name could be Ethereum Mainnet, Bitcoin Cash, Wanchain Mainnet etc |
| Short Name | An abbreviated name for the blockchain. Maximum length is four characters. | For public blockchains, this will match the standard blockchain exchange name. For example, ETC, BTC. |
| Nickname | Nickname of the chain. Maximum length is 10 characters. | Names such as Rinkeby or Ropsten. |
| Chain Type | A meta data for the type of the blockchains such as public or private, permissioned or permissionless | Private:permissioned |
| Chain Category | A parameter to identify whether this is mainnet, or testnet | “mainnet”, “testnet” |
| Chain IP addresses and Service Provider Id | A set of IP addresses of static nodes that can be contacted to submit a crosschain transaction, and the associated name information for the company providing the service. | 125.125.125.125, 10.10.20.20 |
| Name Service Type | The contract naming service available on the blockchain. | The type of service, for instance ENS. |
| Name Service Address | The address of the name service contract on the blockchain. |  |

### Crosshchain Identifier Registration Contract

To register crosschian/blockchain id, there should be grace period for comments before it become official and verified.  The registration service should support the following functions

- RegisterBlockchainId
- ModifyName
- ModifyParameters
- VerifyBlockchainId
- QueryBlockChainId
- LookupBlockchainId
- QueryBlockchainOwner
- QueryBlockchainName(Blockchain-id, NameType)
- QueryParentBlockchainId

## Rationale

With the success of Bitcoin and Ethereum, various blockchains such as EOS, Ripple, Litecoin, Besu, Wanchain and the like have been developed and are growing at a fast pace.  There are also other private and consortium blockchains such as Hyperledger Fabric, Hyperledger Besu, Stellar, Corda, Quorum that only allow nodes with permitted identities to join the blockchain network.  The growth of public and private blockchains imposes

challenges for inter-chain interoperability, particularly when these chains are

heterogeneous and incompatible.

Enterprise Ethereum Alliance formed Crosschain Interoperability Task Force (CITF) to look into common crosschain problems and solutions. CITF team noticed that there is a lack of unique identifier to charaterise and describe a blockchain. Several proprosals were discussed in EEA Crosschain Interoperability Task Force meetings and discussions.  We have considered various alternative specifications such as using a random unique hex string to represent a blockchain.  The drawback of this method is that the random id can not be used to verify a blockchain’s intrinsic identity such as the blockhash of the genesis block.  A second alternative is simply using a genesis blockhash to represent a blockchain id for crosschain operations.  The drawback of this is that this id does not have information about the property of the blockchain and it has problem when a blockchain is forked into two blockchain.  After various discussion, we finally came up with hybrid crosschain identity specification that allows a blockchain to be identified and verified both manually and through computer programs.

## Backwards Compatibility

Crosschainid can be backward compatible with EIP-155.  The crosschain id contains a 4 byte segment to record the chainid based on EIP-155.

## Test Cases

The test cases should cover the generation of crosschain id, the parsing of an crosschain id to ensure the various segments of the crosschain id meets the specification.

For the crosschain registration smart contract, the test cases should cover the testing of all functions and also need to ensure that the security of each functions are properly implemented.

## Implementation

The implementation requires the following

- Generate the crosschain id based on the format defined in the specification.
- Parse the crosschain id based on the format defined in the spefication.
- For metadata associated with the crosschainid, the medadata needs to be registered with a smart contract.  The smart contract should implement the functions defined in the speficification.
- Once a smart contract is deployed, the owner of the smart contract can publish the smart contract address, ABI and also crosschain id specification version.
- Once a crosschain id is registered in the smart contract with extended metadata, there should be a waiting period for the community to review the registration and raise objection if there is inconsistency.

## Security Considerations

Collision of crosschain id:  Two blockchains can contain the same crosschain id and hence making the mistakenly transfer assets to a wrong blockchain.

This security concern is addressed by comparing the hash of the crosschain id with the hash of the genesis block.  If it matches, then the crosschain id is verified.  If not, the crosschain id can be compared with the forked blockhash.  If none of the blockhash match the crosschain id hash, then the crosschain id cannot be verified.

Preventing relay attack: Although crosschain id by itself is different from chainid and it is not signed into blockchain transaction, the crosschain id can still be used for presenting relay attack. An application that handles crosschain transaction can verified the crosschain id with its blockhash and decide whether the transaction is valid or not. Any transaction with a non-verifiable crosschain id should be rejected.

The crosschain-id are not required to be signed into blockchaid tx.

For blockchains that do not cryptographically sign crosschain id into the blocks, the crosschain id cannot be verified with the blocks itself and have to be verified with external smart contract address and offchain utilities implemented based on the crosschain id specification.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**gurleen3** (2021-04-04):

Hello! i was developing a generalised Cross Chain Protocol and was wondering if I can use CrosschainId identifier instead of ChainId that I am using. Since this EIP is in draft stage, Would incorporating CrosschainId to my smart contract work?

---

**weijia31415** (2021-04-04):

Yes, using crosschain id at the smart contract or Dapp layer should work as well. The original spec has a core spec and smart contract. EIP3220 only contains the core spec.  The smart contract spec will be submitted out soon.  The 32 byte definition in both core spec and smart contract spec are the same.

You care welcome to share your use case and we can see how the spec can best work in your case.

---

**John-Status** (2021-04-04):

[@weijia31415](/u/weijia31415)  I think it’s very important that any enhancement of Ethereum’s address format includes the ability to encode multiple chain IDs, not just a single chain ID that is possible with EIP-1191.  I’d like to experiment to see if it’s possible to devise a scheme that uses EIP-55 style case encoding to encode multiple Chain IDs into today’s Ethereum address format.  This would be incompatible with also encoding an EIP-55 checksum into an address, but as we move towards a multi-chain world the need to encode multiple chain IDs in addresses will become more pressing.

I go into more details about why encoding multiple chain IDs in addresses is important in this comment [Increasing address size from 20 to 32 bytes - #18 by greg7mdp](https://ethereum-magicians.org/t/increasing-address-size-from-20-to-32-bytes/5485/18)

Due to the limited space available when using EIP-55 style case encoding to encode additional data into an Ethereum address, we will need the absolutely most compact representation of Chain IDs possible to service this usecase of encoding Chain IDs into Ethereum addresses. To make Chain IDs sufficiently compact to fit more than one into Ethereum’s current address format, we will probable need to set a upper bound on the number of  Chain IDs that are available.

So regarding this proposal, perhaps it would also be useful to have a 2 byte representation of each chain ID which would give use 65536 possible Chain IDs to work with for when we encode Chain IDs into ethereum addresses?

Perhaps use 2 of the ‘Reserved’ 7 bytes (see the “Definition of a 32 byte crosschain id” table at the top of this thread) for this purpose?  So with this change there would be a 2 byte shorthand for every ChainID that could be encoded in ethereum addresses.

Or reducing “Native Chain ID” from 4 bytes to 2 bytes might be a better option?

Either way, in order to encode multiple Chain IDs into the current ethereum address format, we probably need each Chain ID to be no more than 2 bytes.

---

**weijia31415** (2021-04-05):

EIP-55 is not enforced in many applications.  We have seen supporting issues with people using addresses that have mismatched cases.  When encoding chainId into ethereum addresss, the representation should be both machine readable and human readable.

For crosschain id, the reserved 2 bytes are mostly for extensibility in the future.  The 16 bytes for the generic block hash is plenty and can have some extra bytes used for other purposes.  These bytes can be used for special cases as described in you post.  For example, the reserved byte can have 0x01 to enable the “two bytes address chainId”.  The “two byte address chainId” is byte 15 and 16 in the crosschain Id.  This will require changes proposed EIP-3220.

---

**gurleen3** (2021-04-06):

In my case, I would use the Crosschain Id identifier in smart contract. My protocol is for generalised cross-chain communication, that anyone from one heterogenous blockchain could communicate with another blockchain. So could you please elaborate more on how the smart contract spec works in my case?

---

**weijia31415** (2021-04-08):

At the smart contract layer, multiple functions are defined, including the following:

- RegisterBlockchainId
- ModifyName
- ModifyParameters
- VerifyBlockchainId
- QueryBlockChainId
- LookupBlockchainId
- QueryBlockchainOwner
- QueryBlockchainName(Blockchain-id, NameType)
- QueryParentBlockchainId

A smart contract can be deployed to provide these functions in a blockchain.  Dapps can interact with this smart contract to query crosschain id.

This was originally in EIP-3220 and was later separated to be a following up EIP.  We are working on the detailed spec.

---

**gurleen3** (2021-04-09):

Alright, Thanks for the help. Once done, please share more about the following up EIP you mentioned ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**weijia31415** (2021-12-10):

EIP-3220 automatic generation of crosschainId

EEA (Enterprise Ethereum Alliance) had a review of EIP-3220 and suggested that crosschain identifier should be generated unattended.  This means that the field of ChainType (2 bytes) and Governance identifier (2 bytes) should be replaced or removed.  This way, any blockchain crosschain id can be generated with genesis block header or forked block header in combination of current chainid.

---

**Probity** (2022-01-23):

If this cross chain ID provides a mechanism for connecting to Ethereum, I want to make a comment on rule based approaches for blanguage generation rulesets? I was looking at ICANN’s proposal for Zone Root Label and I though the superaltern logic for transitive sequences in language rulesets would be a great place to start

E.g. Korean into English

하 is Ha! - Consonant then a Vowel

(a/) (a) (a/) (b) (b/) (c)

So can be

(a/) (c)

Okay, so vowels and consonants can be identified between say Hangul and English concisely.

Consonant equals consonant a equals a and a equals b and b equals c so a equals c

Okay, nice chat. So

The superaltern logic to the transitive sequences in between  words in languages can be used for an equitable labeling improvement for an eventual international protocol for on-chain communication

---

**drinkcoffee** (2022-01-27):

I think the chain id needs to be 8 bytes long. Looking at ChainList: https://chainlist.org/ , multiple networks are using chain ids between 4 and 8 bytes long.

For example, Palm MainNet is using 11297108109, which is 0x2, A15C, 308D. That is, 5 bytes long.

---

**weijia31415** (2022-01-27):

Good point.  There are additional bytes in the crosschain id that can be used.  Allocating 8 bytes for the legacy chainid is no problem. There are several options to address really large chainids:

option 1: put chainid=0 for chainids that are larger than the allocated byte size ( >4294967295).  Use the legacyChainId in the crosschainId service smart contract to look up the legacy chainId.

Option 2: Use additional custom bytes in crosschainId for large chainds.  The reserved bytes would be 0xFFFFFFF (8 bytes).  The additional custom bytes can be set as:

Custom_bytes = chainId % 0xFFFFFFFF;

Thoughts?

---

**juanfranblanco** (2022-07-15):

[@weijia31415](/u/weijia31415)  My thoughts, and hence the idea of having a common registry. Native ChainIds should be enforced to be unique, to prevent replay attacks of transactions or even 712 signed messages. As per previous comments Native ChainIds, will probably require to be a BigInteger as there might be scenarios that have been used as such to be unique. [safe-contracts/GnosisSafe.sol at main · safe-global/safe-contracts · GitHub](https://github.com/safe-global/safe-contracts/blob/main/contracts/GnosisSafe.sol#L340)

---

**weijia31415** (2022-07-15):

Yes, the current native ChainId is too small in type to avoid collision in the future. If EIP-3220 is adopted, we have a crosschainId that is bundled with a significant block hash and will not only solve collision issue, but also avoid ambiguity with a chainId when a blockchain fork happens.


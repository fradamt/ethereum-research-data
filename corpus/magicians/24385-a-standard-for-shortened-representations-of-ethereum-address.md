---
source: magicians
topic_id: 24385
title: A standard for shortened representations of Ethereum addresses
author: rafaels
date: "2025-05-30"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/a-standard-for-shortened-representations-of-ethereum-addresses/24385
views: 141
likes: 2
posts_count: 1
---

# A standard for shortened representations of Ethereum addresses

## tl:dr

A simple standard is presented to shorten Ethereum addresses and make them easier to remember. The standard is based on references to the blockchain itself and can transform, for example, 20-byte addresses like [0xdAC17F958D2ee523a2206206994597C13D831ec7](https://etherscan.io/address/0xdac17f958d2ee523a2206206994597c13d831ec7) into short versions with 5 bytes plus the suffix **.ep** (Ethereum Pointer): `1.85.129.77.153.ep`.

The proposed standard also applies to contracts. For example, the address of the [USDC](https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48) token contract can be shortened to 4 bytes plus the **.ep** suffix: `92.207.161.22.ep`.

## Introduction

EOA (Externally Owned Account) and contract addresses on the Ethereum network are 20 bytes long and are represented by a 40-character hexadecimal string prefixed with **0x**. While long addresses contribute to the security of the system, they are not user-friendly because they are random, have no relation to entities, are difficult to memorize or recognize, and are prone to typing errors. The fact that these addresses are not human-friendly increases the risk of attacks such as [address poisoning](https://support.metamask.io/stay-safe/protect-yourself/wallet-and-hardware/address-poisoning-scams/) and [clipboard address hijacking](https://support.metamask.io/stay-safe/protect-yourself/wallet-and-hardware/clipboard-hacking/).

Two classes of solutions are available:

- Naming services – Systems like ENS (Ethereum Name Service), which are contract-based, distribute names based on a first-come, first-served model and pricing. Since these names have a cost and can vary in value on the secondary market, availability is competitive. ENS is highly efficient at storing various types of data, such as Ethereum wallet addresses, email addresses, social media profiles, and more. The main drawback is that name resolution requires access to a synchronized Ethereum node to be performed securely.
- Vanity mining – This approach is based on generating addresses that contain a specific pattern in their composition. These addresses can make it easier to recognize the entity that owns them, which helps mitigate attacks such as address poisoning and clipboard address hijacking. However, they do not shorten the addresses, so memorization remains difficult.

An alternative and simple standard is presented that creates short and relatively easy-to-remember addresses, although not in human-friendly format. Distribution follows a first-come, first-served basis: earlier addresses receive shorter versions, while more recent addresses are shortened to a lesser degree. Similar to the naming service solutions, resolving these addresses also requires access to an Ethereum node.

The inspiration comes from [dictionary-based](https://en.wikipedia.org/wiki/Dictionary_coder) compression methods. These methods take advantage of the fact that storing data consumes more memory than addressing it. They aim to store a single copy of each value (in a dictionary) and use pointers to reference it multiple times. Clearly, the Ethereum blockchain contains a significant amount of data redundancy. Addresses, for example, tend to appear repeatedly. If a copy of the blockchain is available, these addresses can be referenced using fewer than 20 bytes.

## The standard

A reference for a transaction on the Ethereum blockchain requires two values. The first value is an integer of `n` bytes representing the block number. `n` can be arbitrarily large since blocks quantity tend to grow indefinitely, however at the time of writing, the most recent block can be represented with 4 bytes. The second value used to reference a transaction is the transaction number within that block. This value can be stored in up to 2 bytes. Therefore, a transaction reference is composed of `<n bytes representing the block number><{1 or 2} bytes for the transaction number>.ep`, where both the block number and transaction number are encoded as a byte array using Big Endian.

EOA shortening consists of simply referencing, on the blockchain, the first transaction whose creator (i.e. signer) is the address. This reference takes the form `bbb.bbb.ttt.ep`, where the sequence `bbb.bbb` represents the block, the last byte `ttt` represents the transaction within the block, and the suffix **.ep** is appended. If the transaction number is greater than 255, the extended format `bbb.bbb.ttt:ttt.ep` can be used instead, where `ttt:ttt` represents the transaction number using two bytes (Big Endian encoding).

For contracts, the process is similar, but the reference points to the contract’s creation transaction. It’s possible for a block to have a contract creation transaction with an index greater than 255, in such cases, the extended format is used. Therefore, the general format for a shortened contract address is the same as for EOAs: `bbb.bbb.ttt:ttt.ep`.

Note that addresses whose first transaction was the creation of a contract cannot be shortened, since the shortening of that transaction refers to the contract that was created.

Both EOAs and contracts could technically be referenced by any transaction other than the first (for EOAs) or the creation transaction (for contracts), but by convention, the first transaction or the creation transaction is used to ensure uniqueness in the shortening scheme.

### Design choices

The main challenge lies in identifying the first transaction signed by an address, or the transaction that created a contract. This would require listing all transactions for a given address, which is not supported by Ethereum nodes. The possible solutions are:

- Index the blockchain manually.
- Use indexing APIs services such as Etherscan.
- Use any transaction instead of the first. This is a poor solution as it breaks the uniqueness of the shortened address and facilitates attacks such as address poisoning and clipboard address hijacking.

This indexing problem only arises during the shortening process, that is, when creating shortened addresses from original ones. Resolving the original address from a shortened one does not require any indexing and can be performed using any Ethereum node.

An alternative approach would be to use the first transaction in which the address receives funds, instead of the first one it sign. The following pros and cons have been considered:

|  | pros | cons |
| --- | --- | --- |
| first transaction it sign (from) | allows validators to shorten addresses | demands indexing to resolving |
| first transaction it receive (to) | allow cold wallets to have short version | demands indexing to shortening |

Was decided to use first transaction that it signs (`from`) to define short address.

## Examples

The first [Ethereum transaction](https://etherscan.io/tx/0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060) was sent by [thanateros.eth](https://app.ens.domains/thanateros.eth) and resulted in the shortest possible shortened address, consisting of just 3 bytes:

```sh
EOA Address:
0xA1E4380A3B1f749673E270229993eE55F35663b4
Etheureum pointer:
180.67.0.ep
```

Note: The Ethereum pointer `0.0.ep` does not exist due to the network’s stabilization phase and the gradual onboarding of users and developers.

A recent [address](https://etherscan.io/address/0x21ab46a5e3446ba0fdcc44d5d3db88b00807305b) example using 5 bytes:

```sh
EOA Address:
0x21aB46A5e3446ba0Fdcc44D5d3Db88b00807305B
Etheureum pointer:
1.85.129.77.153.ep
```

The [USDT](https://etherscan.io/address/0xdac17f958d2ee523a2206206994597c13d831ec7) token contract uses 4 bytes:

```sh
Contract Address:
0xdAC17F958D2ee523a2206206994597C13D831ec7
Etheureum pointer:
70.184.124.64.ep
```

The [earliest verified contract](https://etherscan.io/tx/0xb9926275fa948d65c5ac4b2896536bbf1b2a2a842567f724e9285ef0431b17dd), according to [Takens Theorem](https://medium.com/etherscan-blog/an-archeological-trip-across-early-ethereum-contracts-232b0de33f8), is shortened to 3 bytes:

```sh
Contract Address:
0xa3483b08C8A0F33eB07afF3A66fbcaf5C9018CDC
Etheureum pointer:
193.20.0.ep
```

## Implementation

A proof of concept is implemented at [GitHub - r4f4ss/ethshort: A converter between Ethereum address pointer and standard address](https://github.com/r4f4ss/ethshort).

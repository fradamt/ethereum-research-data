---
source: magicians
topic_id: 14158
title: Pretty good privacy (PGP / GPG) on-chain keyserver
author: SamWilsn
date: "2023-05-07"
category: Magicians > Primordial Soup
tags: [erc, cryptography]
url: https://ethereum-magicians.org/t/pretty-good-privacy-pgp-gpg-on-chain-keyserver/14158
views: 2432
likes: 22
posts_count: 17
---

# Pretty good privacy (PGP / GPG) on-chain keyserver

As I’ve [vaguely alluded](https://ethereum-magicians.org/t/eip-5630-encryption-and-decryption/10761/4) to in the past, I’ve wanted to investigate how a PGP keyserver backed by an on-chain contract might look. Now that I’ve had a few moments to think about it, here’s what I’ve come up with:

### Motivation

Why might we want PGP keys to be registered on chain? PGP has been around for eons, and is well supported in many programs: from [email clients](https://support.mozilla.org/en-US/kb/openpgp-thunderbird-howto-and-faq), to [source control](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work), to software distribution, and more.

Unfortunately, one of the downsides of PGP is key distribution/verification. How do you retrieve the other party’s encryption key before sending the first email? How do you know whether the signing key is the correct one for the software you downloaded?

Keyservers solve some of these problems by mapping from a user id (typically an email address) to a key bundle, or certificate. Keyservers are **trusted** and **centralized** parties. A keyserver can publish any certificate for an email, or could withhold revocations, or just disappear entirely.

I’d like to come up with a way to run a decentralized and trust-minimized keyserver on top of the Ethereum blockchain to solve these issues.

### A Solution

```solidity
type CertId is uint256;

interface KeyRegistry {
    //--------------------------------------------------------------------------
    // Events
    //--------------------------------------------------------------------------

    event Certify(
        address indexed certifier, bytes16 indexed kind, CertId indexed certId
    );

    event Revoke(
        address indexed certifier, bytes16 indexed kind, CertId indexed certId
    );

    //--------------------------------------------------------------------------
    // Key Management Functions
    //--------------------------------------------------------------------------

    /// @notice Link the given key with the sender's (certifier's) address.
    function certify(
        bytes16 kind,
        uint64 validBefore,
        bytes memory publicKey,
        bytes memory location
    ) external returns (CertId);

    /// @notice Mark the identified key as revoked.
    function revoke(CertId certId) external;

    //--------------------------------------------------------------------------
    // Getter Functions
    //--------------------------------------------------------------------------

    /// @notice Retrieve the revocation token for a certification.
    function idOf(address addr, bytes16 kind) external view returns (CertId);

    /// @notice Retrieve the public key of a certification.
    function keyOf(address addr, bytes16 kind)
        external
        view
        returns (bytes memory publicKey);

    /// @notice Retrieve the location of data associated with a certification.
    function locationOf(address addr, bytes16 kind)
        external
        view
        returns (bytes memory location);

    /// @notice Retrieve the first second where the certification is invalid.
    function validBeforeOf(address addr, bytes16 kind)
        external
        view
        returns (uint64 validBefore);

    //--------------------------------------------------------------------------
    // Permit-style Functions
    //--------------------------------------------------------------------------

    /// @notice Mark the identified key as revoked.
    function revoke(CertId certId, bytes calldata signature) external;

    /// @notice Link the key with the address recovered from the signature.
    function certify(
        bytes16 kind,
        uint64 validBefore,
        bytes calldata publicKey,
        bytes calldata location,
        bytes calldata signature
    ) external returns (CertId);

    //--------------------------------------------------------------------------
    // Multi-call Functions
    //--------------------------------------------------------------------------

    /// @dev See https://eips.ethereum.org/EIPS/eip-6357.
    function multicall(bytes[] calldata data)
        external
        returns (bytes[] memory);
}
```

#### Certification

A “certification” above is a statement from the owner of an Ethereum account (called the certifier) that a particular public key is a valid signer for that account. A certification SHALL be created after the successful execution of either of the `certify` methods above.

The location of a certification may be changed without triggering a revocation, or more formally:

- If certify is called for the same certifier-kind pair with an unchanged public key and an unchanged valid before time, the previous certification MAY be revoked.
- If certify is called for the same certifier-kind pair with a different public key, the previous certification MUST be revoked.
- If certify is called for the same certifier-kind pair with a different valid before time, the previous certification MUST be revoked.

A certification SHALL remain valid as long as it hasn’t expired and hasn’t been revoked.

Getter functions MUST revert if no matching valid certification exists.

When a certification is created or changed, a `Certify` event MUST be emitted.

If a certification is changed without being revoked, the returned certification identifier MUST remain the same.

##### Kind

This proposal standardizes the following `kind` values:

| Value | Public Key Algorithm | Location Interpretation |
| --- | --- | --- |
| 0x50475008132b8104000a000000000000 | ECDSA+secp256k1 (stored in uncompressed form with the 0x04 prefix) | IPFS CID in binary encoding pointing to a series of unarmoured OpenPGP packets |

Further proposals may define other non-conflicting values.

The value `0x50475008132b8104000a000000000000` is derived from `"PGP" (0x504750) || SHA256 (0x08) || ECDSA (0x13) || secp256k1 (0x2b8104000a)`, but the kind value is completely arbitrary. `0x01` would’ve been just as valid here.

##### Valid Before

The certification is valid while `block.timestamp < validBefore`. Implementations MAY interpret the value `2^64 - 1` as meaning the certification never expires.

##### Public Key

The public key material to associate with the certifier’s identity. The format of the public key is determined by the kind field.

Implementations MAY assume a maximum length of `0xFFFF` octets.

##### Location

A location, in a format determined by the kind field, of off-chain data associated with the certification.

Implementations MAY assume a maximum length of `0xFFFF` octets.

#### Revocation

A certification is said to be revoked if either of the `revoke` methods above are successfully executed with a matching identifier, or if a certification is replaced according to the rules above.

When a certification is revoked, a `Revoke` event MUST be emitted.

#### Notes on Compatibility

[gnupg](https://gnupg.org/) supports [ECDSA with the secp256k1 curve](https://wiki.gnupg.org/ECC) for signatures, which I believe is compatible with the `ecrecover` precompile (in a roundabout way.)

SHA-256 (not keccak256) hashes are supported both by [RFC 4880](https://www.rfc-editor.org/rfc/rfc4880.html#section-9.4) and by the `SHA256` precompile.

#### Notes on Permit-style Functions

The format of the signed messages will likely be [EIP-712](https://eips.ethereum.org/EIPS/eip-712), but the specifics are to be determined.

### Further Questions

- Can we standardize storing private key material on-chain, encrypted with a key derived from a mnemonic phrase?
- Should we allow, deny, or leave unspecified revoking and replacing expired keys?
- Is there a more efficient way to represent packets to avoid writing a PGP parser in Solidity?
- Can we execute the merge (with verification) off-chain and use a zk-proof to show it was done correctly for less gas than verifying on-chain?
- Storing certificates on-chain will be very expensive (napkin math says at least ~400k gas.) Can we do the work of merging/verifying and only store an IPFS hash? inspired by a twitter conversation with @LefterisJP

### Further Reading

- A decoded public key block
- RFC 4880: OpenPGP Message Format
- Hagrid Keyserver: Database trait

## Replies

**fubuloubu** (2023-05-07):

Could adding a PGP record to ENS make sense?

---

**SamWilsn** (2023-05-07):

My original idea was to add the PGP keys to ENS, but I chose not to because names expire, and the merging operation is more involved than just replacing the entire key.

To get PGP keys for an ENS name, I’d just resolve its address, then look that up in the PGP registry contract.

---

**SamWilsn** (2023-05-11):

Instead of sleeping, I’ve thrown together a prototype parser for the OpenPGP key format:



      [github.com](https://github.com/SamWilsn/Pgp.sol/blob/master/src/Pgp.sol)





####



```sol
// OpenPGP Implementation in Solidity
// Copyright (C) 2023 Sam Wilson
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see .

// SPDX-License-Identifier: AGPL-3.0-or-later

pragma solidity ^0.8.19;

```

  This file has been truncated. [show original](https://github.com/SamWilsn/Pgp.sol/blob/master/src/Pgp.sol)










It can handle the important bits of secp256k1 packets, though doesn’t yet perform any validation.

---

**xzhang** (2023-05-13):

I like the idea of setting up a PGP/GPG keyserver on-chain. In general, it may not be limited to PGP use cases. Basically what we need is a way to attach the real-world identity of an entity (a person or an organization) to some cryptographic identifiers, like PGP public keys or Ethereum address or other DID.

We have started doing similar things at [valid3.id](https://valid3.id) by combining Ethereum DID, attestation and verifiable credentials. We are in the process of designing the on-chain part. Would love to chat about it with you.

---

**SamWilsn** (2023-05-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xzhang/48/9466_2.png) xzhang:

> it may not be limited to PGP use cases

Yes, exactly. I’ve been convinced that the on-chain portion can be reduced to just a public key and a tiny bit of metadata (algorithm, expiry, etc.) Everything else can be done off-chain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xzhang/48/9466_2.png) xzhang:

> Would love to chat about it with you.

Sure! Feel free to shoot me a DM. I’m generally available after 10am ET.

---

**varunsrin** (2023-05-13):

Working on something related at Farcaster protocol that you might find interesting: [GitHub - farcasterxyz/contracts](https://github.com/farcasterxyz/contracts)

The primary use case is a stable mapping from a user’s identity to a keypair used to sign off-chain messages. But we’ve also used it to implemented encrypted messaging using double-ratched in one of the clients. (More details [here](https://www.youtube.com/watch?v=eMGtBmN7qKE&list=PL0eq1PLf6eUdm35v_840EGLXkVJDhxhcF&index=13))

---

**xzhang** (2023-05-14):

Hi Varunsrin, this is interesting. Do you perform some sort of checking to verify user identity before it is linked to the keypair?

---

**varunsrin** (2023-05-14):

The general idea is that you can map your keypair to a stable, but meaningless identifier (e.g. 12345) which gives you the ability to rotate the keypairs later without affecting your identifier. You can then separately map the identifier to meaningful identity constructs like your ENS or other verification systems. Finally, you can sign off-chain messages with your identifier which can be used by applications.

---

**SamWilsn** (2023-05-15):

Made some big changes to the specification in the initial post. Instead of processing PGP packets on-chain, we simply publish the public key itself with minimal metadata and a location of the full PGP bundle.

A PGP keyserver could be written to watch the chain, fetch the PGP bundles, and serve them up over the traditional protocol, while verifying the signature packets with the on-chain key.

---

**SamWilsn** (2023-05-18):

Got [in contact](https://twitter.com/_SamWilsn_/status/1658505428987150337) with some of the people at [Ethereum Attestation Service](https://attest.sh/) after a discussion with [@xzhang](/u/xzhang).

Looks like there is at least some potential to use EAS to build something similar to this.

My biggest concern with EAS is the added complexity of needing an external indexer to do key-by-address lookups. With the design as written in this post, you only need a regular Ethereum node.

---

**SamWilsn** (2023-06-10):

[@vbuterin](/u/vbuterin)’s “keystore contract” from [The Three Transitions](https://vitalik.eth.limo/general/2023/06/09/three_transitions.html) is pretty similar to what this thread turned into, and goes into some very interesting use cases that can be enabled with keystore contracts that I hadn’t considered, like registering signing keys on one chain (eg. mainnet) to spend funds on other chains (eg. optimism).

---

**SamWilsn** (2023-06-13):

If we want to support off-chain (or at least non-mainnet) proofs, we’ll need to standardize the storage layout as well as the contract interface. Anyone have experience optimizing storage layouts for succinct proofs? ![:rofl:](https://ethereum-magicians.org/images/emoji/twitter/rofl.png?v=12)

---

**nelsonhp** (2023-06-16):

I am confused by your comment but this may just be me missing the joke. I can be a bit dense at times, so forgive me if this is the case. Rather than trying to engineer an optimal layout for storage proof construction, why not allow the proof of a single storage slot to be sufficient? If you have all keys added to the system be appended to a Compact Sparse Merkle Tree (CSMT), and also maintain an append only revocation CSMT, you can then build a height two normal Merkle Tree of those two roots. In this way you can easily describe the state of the system by proving one hash and then providing proofs of inclusion/exclusion for the CSMTs. It is important to note that the revocation tree has nothing to do with expiry, or at least it shouldn’t since building it otherwise would create the problem of, “Who pays for the gas to add elements to the revocation CSMT on expiration?”. This is basically the idea behind Certificate Transparency Logs as described in [Google Trillian Verifiable Log Backed Map](https://github.com/google/trillian/blob/master/docs/papers/VerifiableDataStructures.pdf). See the Deposit Contract Formal Verification(See 1 below) for a description of how a CSMT can be built in chain. If you have not read [Peter Gutman’s, “Engineering Security”](https://www.cs.auckland.ac.nz/~pgut001/pubs/book.pdf), you may find it an interesting read.

1: Since this is a new account, I can only link 2 articles. Here is the url for the formal proof. github-DOT-com/runtimeverification/verified-smart-contracts/blob/master/deposit/formal-incremental-merkle-tree-algorithm.pdf

---

**SamWilsn** (2023-06-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nelsonhp/48/9783_2.png) nelsonhp:

> I am confused by your comment but this may just be me missing the joke. I can be a bit dense at times, so forgive me if this is the case.

The joke was that I didn’t expect anyone subscribed to this thread to be an expert on optimizing storage layouts. I’m quite glad you showed up!

I am about as far from an expert on cryptography as you can get while still working on Ethereum. I have happened to be around for enough EIPs to see the need for a key registry contract, but lack the expertise to design it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nelsonhp/48/9783_2.png) nelsonhp:

> Rather than trying to engineer an optimal layout for storage proof construction, why not allow the proof of a single storage slot to be sufficient?

That sounds like it answers the “does this address authorize this public key?” question quite well for off-chain purposes, but not as well for on-chain ones. Could store both if it’s important I guess?

Please correct me if I’m wrong, but without storing the actual key on-chain, we’d need an external mechanism for key discovery, right? So, for example, you’d have to ask `keys.example.com` for the certificate attached to `0xabc...def@ethereum` and confirm that with a proof to the storage slot.

---

**bitcoinbrisbane** (2023-08-08):

I would like to contribute to this EIP.  I was hoping this project would get off the ground [BlockPGP: A Blockchain-Based Framework for PGP Key Servers | IEEE Conference Publication | IEEE Xplore](https://ieeexplore.ieee.org/document/8590919) [BlockPGP: A new blockchain-based PGP management framework](https://techxplore.com/news/2020-02-blockpgp-blockchain-based-pgp-framework.html)

This will be like handshake protocol and domains names.  There is a .pgp HS domain too.

---

**bitcoinbrisbane** (2023-08-08):

Perhaps we could get a working group / forum / site up?  Id like to help.  We use PGP as the backbone of our id product idem.com.au


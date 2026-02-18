---
source: magicians
topic_id: 5121
title: About signature verification by smart contract wallets (1271, 1654, 2126)
author: Amxx
date: "2021-01-07"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/about-signature-verification-by-smart-contract-wallets-1271-1654-2126/5121
views: 2290
likes: 8
posts_count: 6
---

# About signature verification by smart contract wallets (1271, 1654, 2126)

The need for smart contract wallet to be able to recognise signature as been identified a long time ago. Verification of EOA’s signature using ecrecover is now very common, as is allows protocole to partially move offchain, reduce gas cost, and increase scalability.

Smart contract based wallet, like Argent and Gnosis can very rarely interact with such systems.

Many proposal, with various names, have been drafted. The ERC1271/1654 family proposed a `isValidSignature` function, with various arguments, that would allow a smart contract to recognise signature made by its owners. THe most common variants are

`isValidSignature(bytes data, bytes signature) returns (bytes4)`

`isValidSignature(bytes32 hash, bytes signature) returns (bytes4)`

With various assumption about how the hash or data should be processed

There function are expected to return their own selector has a “magic value”.

The second option is less generic, but IMO is a better fit considering the bytes32 format correspond to `ecrecover`'s supported format, and is standardised through ERC191 and ERC712

These 2 ERCs have been in draft for way to long!

More recently, [@pedrouid](/u/pedrouid) proposed ERC2126, which (while I did not agree with the overall design) had the benefit to try and have things moving again. Unforunatelly, the corresponding PR was close due to inactivity so the ERC never made it EIP repo.

Argent implements (bytes32, bytes), Gnosis implements a version of (bytes,bytes) where the data is expected to signed using an ERC712 structure. I do believe that it is high time we move a proposal to final call, as having the various proposal stuck in “draft” prevents adoption.

I’d love to have the community opinion on that subject. Particularly that of ERC1271 & 1654 authors, and that of Wallet developpers.

[@pedrouid](/u/pedrouid) [@PhABC](/u/phabc) [@frangio](/u/frangio) [@shrugs](/u/shrugs) [@abandeali1](/u/abandeali1) [@izqui](/u/izqui) [@catageek](/u/catageek) @pazams

## Replies

**PhABC** (2021-01-09):

Happy to make a PR to set ERC-1271 to final call again, with the `isValidSignature(bytes32 hash, bytes signature) returns (bytes4)` version. Need to look back as to why the last attempt never made it through.

---

**pedrouid** (2021-03-08):

the whole debate bytes32 vs bytes was an unfortunate event IMO to the specification of ERC-1271

there was a period of time that all smart contract wallets used bytes yet they all verified data differently

hence why bytes32 is the preferred interface since it guarantees that ecrecover behaves equally on all smart contracts

the second advantage was that using bytes 32 consolidate the differences of ERC-1654

therefore both standards now share the same validation and ERC-1654 is an extension of ERC-1271

given these developments I saw no benefit of pursuing ERC-2126 since the mine issue was solvable by using bytes32 for ERC-1271

---

**ligi** (2023-03-05):

Having one question about 1271 - it states:

> The specific return value is expected to be returned instead of a boolean in order to have stricter and simpler verification of a signature.

This is the reference implementation:

```auto
  /**
   * @notice Verifies that the signer is the owner of the signing contract.
   */
  function isValidSignature(
    bytes32 _hash,
    bytes calldata _signature
  ) external override view returns (bytes4) {
    // Validate signatures
    if (recoverSigner(_hash, _signature) == owner) {
      return 0x1626ba7e;
    } else {
      return 0xffffffff;
    }
  }
```

really having trouble understanding how this is simpler/stricter than

```auto
  /**
   * @notice Verifies that the signer is the owner of the signing contract.
   */
  function isValidSignature(
    bytes32 _hash,
    bytes calldata _signature
  ) external override view returns (boolean) {
    // Validate signatures
    if (recoverSigner(_hash, _signature) == owner) {
      return true;
    } else {
      return false;
    }
  }
```

really hope someone can enlighten me here.

Also think we need something like ERC2126 - otherwise IMHO 1271 is building on sand. Wondering what other approach [@Amxx](/u/amxx) had in mind when stating:

> More recently, @pedrouid proposed ERC2126, which (while I did not agree with the overall design) had the benefit to try and have things moving again.

---

**ligi** (2023-03-05):

digging into 1271 more another question arose (sorry to use this thread - but it is the last one about 1271 here and there is no discussions-to header in the EIP)

How should it work with multisigs where there is not only one owner? Here we would kinda need a list of signatures right? How would this work with the current 1271 design?

---

**luke** (2024-02-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> verification

Hello ligi, I was coming here with a query that might actually answer your question, or help you. Maybe.

I’m learning Ethereum and reading through lots of main EIPs making notes. Some are much higher quality writing than others. I’m at that wondeful stage where I don’t have the Curse of Knowledge, and this EIP is confusing.

The opening sentence gives the impression that the proposal I’m about to read will fix the “current” state of affairs so that contracts will be able to sign messages! But then goes on to say that it is merely proposing a way for any contract to check whether a signature “on behalf of a contract” is valid.

Strictly speaking, neither are true. The EIP is just defining a method which validates arbitrary data.

Because the EIP neglects to formalise or give an example of how the hash and signature are generated, it’s left open to interpretation as to what these values may contain, exactly. Thus the function is really asking, “Do you like this data?”

There are no uses of MUST or SHALL etc. other than a few in the coded spec.

Therefore, the signature bytes could potentially contain a custom layout of data to be decoded and checked, which could be a workaround for ligi.

Again, the EIP does not elaborate on how the method will be used in practice, nor how or what generates the hash and signature, so it is either:

a) left open intentionally

b) left open unintentionally, probably due to tacit (assumed) knowledge within the community of how this would work, or

c) is closed; the constraints are implied in the tacit knowledge that it’s simply not possible for public contract code to *securely* do anything much with this data other than to recover the signer public key and compare it to some other known address.

So I’m posting here to perhaps show ligi a way out, (or lead poor ligi astray), and to highlight that the EIP is not clear enough.

Thanks all,

Luke


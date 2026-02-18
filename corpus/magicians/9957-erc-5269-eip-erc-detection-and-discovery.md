---
source: magicians
topic_id: 9957
title: "ERC-5269: EIP/ERC Detection and Discovery"
author: xinbenlv
date: "2022-07-16"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-5269-eip-erc-detection-and-discovery/9957
views: 3685
likes: 17
posts_count: 23
---

# ERC-5269: EIP/ERC Detection and Discovery

Created a human interface detection. the high level idea is instead of returning machine standard ABI based EIP-165 standard interface. This can be a complement to EIP-165 and potentially easier to use for developers of destination smart contract or source smart contract or source dapp.

- EIP publication: ERC-5269: ERC Detection and Discovery
- Original: https://github.com/ethereum/EIPs/pull/5269
- Reference Implementation: ercref-contracts/ERCs/eip-5269 at main · ercref/ercref-contracts · GitHub
- Deployment (DRAFTv1): https://goerli.etherscan.io/address/0x33F735852619E3f99E1AF069cCf3b9232b2806bE#readContract

---


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5269)





###



An interface to identify if major behavior or optional behavior specified in an ERC is supported for a given caller.










## Abstract

An interface for better identification and detection of EIP/ERC by numbers.

It designates a field in which it’s called `majorEIPIdentifier` which is normally known or referred to as “EIP number”. For example, `ERC-721` aka EIP-721 has a `majorEIPIdentifier = 721`. This EIP has a `majorEIPIdentifier = 5269`.

Calling it a `majorEIPIdentifier` instead of `EIPNumber` makes it future-proof: anticipating there is a possibility where future EIP is not numbered or if we want to incorporate other types of standards.

It also proposes a new concept of `minorEIPIdentifier` which is left for authors of

individual EIP to define. For example, EIP-721’s author may define `ERC721Metadata`

interface as `minorEIPIdentifier= keccak256("ERC721Metadata")`.

It also proposes an event to allow smart contracts to optionally declare the EIPs they support.

## Motivation

This EIP is created as a competing standard for EIP-165.

Here are the major differences between this EIP and EIP-165.

1. EIP-165 uses the hash of a method’s signature which declares the existence of one method or multiple methods,
therefore it requires at least one method to exist in the first place. In some cases, some EIP/ERCs interface does not have a method, such as some EIPs related to data format and signature schemes or the “Soul-Bound-ness” aka SBT which could just revert a transfer call without needing any specific method.
2. EIP-165 doesn’t provide query ability based on the caller.
The compliant contract of this EIP will respond to whether it supports certain EIP based on a given caller.

Here is the motivation for this EIP given EIP-165 already exists:

1. Using EIP/ERC numbers improves human readability as well as make it easier to work with named contract such as ENS.
2. Instead of using an EIP-165 identifier, we have seen an increasing interest to use EIP/ERC numbers as the way to identify or specify an EIP/ERC. For example

- EIP-5267 specifies extensions to be a list of EIP numbers.
- EIP-600, and EIP-601 specify an EIP number in the m / purpose' / subpurpose' / EIP' / wallet' path.
- EIP-5568 specifies The instruction_id of an instruction defined by an EIP MUST be its EIP number unless there are exceptional circumstances (be reasonable)
- EIP-6120 specifies struct Token { uint eip; ..., } where uint eip is an EIP number to identify EIPs.
- EIP-867(Stagnant) proposes to create erpId: A string identifier for this ERP (likely the associated EIP number, e.g. “EIP-1234”).

1. Having an ERC/EIP number detection interface reduces the need for a lookup table in smart contract to
convert a function method or whole interface in any EIP/ERC in the bytes4 EIP-165 identifier into its respective EIP number and massively simplifies the way to specify EIP for behavior expansion.
2. We also recognize a smart contract might have different behavior given different caller accounts. One of the most notable use cases is that when using Transparent Upgradable Pattern, a proxy contract gives an Admin account and Non-Admin account different treatment when they call.

## Specification

In the following description, we use EIP and ERC inter-exchangeably. This was because while most of the time the description applies to an ERC category of the Standards Track of EIP, the ERC number space is a subspace of EIP number space and we might sometimes encounter EIPs that aren’t recognized as ERCs but has behavior that’s worthy of a query.

1. Any compliant smart contract MUST implement the following interface

```solidity
// DRAFTv1
pragma solidity ^0.8.9;

interface IERC5269 {
  event OnSupportEIP(
      address indexed caller, // when emitted with `address(0x0)` means all callers.
      uint256 indexed majorEIPIdentifier,
      bytes32 indexed minorEIPIdentifier, // 0 means the entire EIP
      bytes32 eipStatus,
      bytes extraData
  );

  /// @dev The core method of EIP/ERC Interface Detection
  /// @param caller, a `address` value of the address of a caller being queried whether the given EIP is supported.
  /// @param majorEIPIdentifier, a `uint256` value and SHOULD BE the EIP number being queried. Unless superseded by future EIP, such EIP number SHOULD BE less or equal to (0, 2^32-1]. For a function call to `supportEIP`, any value outside of this range is deemed unspecified and open to implementation's choice or for future EIPs to specify.
  /// @param minorEIPIdentifier, a `bytes32` value reserved for authors of individual EIP to specify. For example the author of [EIP-721](/EIPS/eip-721) MAY specify `keccak256("ERC721Metadata")` or `keccak256("ERC721Metadata.tokenURI")` as `minorEIPIdentifier` to be quired for support. Author could also use this minorEIPIdentifier to specify different versions, such as EIP-712 has its V1-V4 with different behavior.
  /// @param extraData, a `bytes` for [EIP-5750](/EIPS/eip-5750) for future extensions.
  /// @return eipStatus, a `bytes32` indicating the status of EIP the contract supports.
  ///                    - For FINAL EIPs, it MUST return `keccak256("FINAL")`.
  ///                    - For non-FINAL EIPs, it SHOULD return `keccak256("DRAFT")`.
  ///                      During EIP procedure, EIP authors are allowed to specify their own
  ///                      eipStatus other than `FINAL` or `DRAFT` at their discretion such as `keccak256("DRAFTv1")`
  ///                      or `keccak256("DRAFT-option1")`and such value of eipStatus MUST be documented in the EIP body
  function supportEIP(
    address caller,
    uint256 majorEIPIdentifier,
    bytes32 minorEIPIdentifier,
    bytes calldata extraData)
  external view returns (bytes32 eipStatus);
}
```

In the following description, `EIP_5269_STATUS` is set to be `keccak256("DRAFTv1")`.

In addition to the behavior specified in the comments of `IERC5269`:

1. Any minorEIPIdentifier=0 is reserved to be referring to the main behavior of the EIP being queried.
2. The Author of compliant EIP is RECOMMENDED to declare a list of minorEIPIdentifier for their optional interfaces, behaviors and value range for future extension.
3. When this EIP is FINAL, any compliant contract MUST return an EIP_5269_STATUS for the call of supportEIP((any caller), 5269, 0, [])

*Note*: at the current snapshot, the `supportEIP((any caller), 5269, 0, [])` MUST return `EIP_5269_STATUS`.

1. Any complying contract SHOULD emit an OnSupportEIP(address(0), 5269, 0, EIP_5269_STATUS, []) event upon construction or upgrade.
2. Any complying contract MAY declare for easy discovery any EIP main behavior or sub-behaviors by emitting an event of OnSupportEIP with relevant values and when the compliant contract changes whether the support an EIP or certain behavior for a certain caller or all callers.
3. For any EIP-XXX that is NOT in Final status, when querying the supportEIP((any caller), xxx, (any minor identifier), []), it MUST NOT return keccak256("FINAL"). It is RECOMMENDED to return 0 in this case but other values of eipStatus is allowed. Caller MUST treat any returned value other than keccak256("FINAL") as non-final, and MUST treat 0 as strictly “not supported”.
4. The function supportEIP MUST be mutability view, i.e. it MUST NOT mutate any global state of EVM.

## Rationale

1. When data type uint256 majorEIPIdentifier, there are other alternative options such as:

- (1) using a hashed version of the EIP number,
- (2) use a raw number, or
- (3) use an EIP-165 identifier.

The pros for (1) are that it automatically supports any evolvement of future EIP numbering/naming conventions.

But the cons are it’s not backward readable: seeing a `hash(EIP-number)` one usually can’t easily guess what their EIP number is.

We choose the (2) in the rationale laid out in motivation.

1. We have a bytes32 minorEIPIdentifier in our design decision. Alternatively, it could be (1) a number, forcing all EIP authors to define its numbering for sub-behaviors so we go with a bytes32 and ask the EIP authors to use a hash for a string name for their sub-behaviors which they are already doing by coming up with interface name or method name in their specification.
2. Alternatively, it’s possible we add extra data as a return value or an array of all EIP being supported but we are unsure how much value this complexity brings and whether the extra overhead is justified.
3. Compared to EIP-165, we also add an additional input of address caller, given the increasing popularity of proxy patterns such as those enabled by EIP-1967. One may ask: why not simply use msg.sender? This is because we want to allow query them without transaction or a proxy contract to query whether interface ERC-number will be available to that particular sender.
4. We reserve the input majorEIPIdentifier greater than or equals 2^32 in case we need to support other collections of standards which is not an ERC/EIP.

## Test Cases

```typescript
describe("ERC5269", function () {
  async function deployFixture() {
    // ...
  }

  describe("Deployment", function () {
    // ...
    it("Should emit proper OnSupportEIP events", async function () {
      let { txDeployErc721 } = await loadFixture(deployFixture);
      let events = txDeployErc721.events?.filter(event => event.event === 'OnSupportEIP');
      expect(events).to.have.lengthOf(4);

      let ev5269 = events!.filter(
        (event) => event.args!.majorEIPIdentifier.eq(5269));
      expect(ev5269).to.have.lengthOf(1);
      expect(ev5269[0].args!.caller).to.equal(BigNumber.from(0));
      expect(ev5269[0].args!.minorEIPIdentifier).to.equal(BigNumber.from(0));
      expect(ev5269[0].args!.eipStatus).to.equal(ethers.utils.id("DRAFTv1"));

      let ev721 = events!.filter(
        (event) => event.args!.majorEIPIdentifier.eq(721));
      expect(ev721).to.have.lengthOf(3);
      expect(ev721[0].args!.caller).to.equal(BigNumber.from(0));
      expect(ev721[0].args!.minorEIPIdentifier).to.equal(BigNumber.from(0));
      expect(ev721[0].args!.eipStatus).to.equal(ethers.utils.id("FINAL"));

      expect(ev721[1].args!.caller).to.equal(BigNumber.from(0));
      expect(ev721[1].args!.minorEIPIdentifier).to.equal(ethers.utils.id("ERC721Metadata"));
      expect(ev721[1].args!.eipStatus).to.equal(ethers.utils.id("FINAL"));

      // ...
    });

    it("Should return proper eipStatus value when called supportEIP() for declared supported EIP/features", async function () {
      let { erc721ForTesting, owner } = await loadFixture(deployFixture);
      expect(await erc721ForTesting.supportEIP(owner.address, 5269, ethers.utils.hexZeroPad("0x00", 32), [])).to.equal(ethers.utils.id("DRAFTv1"));
      expect(await erc721ForTesting.supportEIP(owner.address, 721, ethers.utils.hexZeroPad("0x00", 32), [])).to.equal(ethers.utils.id("FINAL"));
      expect(await erc721ForTesting.supportEIP(owner.address, 721, ethers.utils.id("ERC721Metadata"), [])).to.equal(ethers.utils.id("FINAL"));
      // ...

      expect(await erc721ForTesting.supportEIP(owner.address, 721, ethers.utils.id("WRONG FEATURE"), [])).to.equal(BigNumber.from(0));
      expect(await erc721ForTesting.supportEIP(owner.address, 9999, ethers.utils.hexZeroPad("0x00", 32), [])).to.equal(BigNumber.from(0));
    });

    it("Should return zero as eipStatus value when called supportEIP() for non declared EIP/features", async function () {
      let { erc721ForTesting, owner } = await loadFixture(deployFixture);
      expect(await erc721ForTesting.supportEIP(owner.address, 721, ethers.utils.id("WRONG FEATURE"), [])).to.equal(BigNumber.from(0));
      expect(await erc721ForTesting.supportEIP(owner.address, 9999, ethers.utils.hexZeroPad("0x00", 32), [])).to.equal(BigNumber.from(0));
    });
  });
});
```

See `TestERC5269.ts`.

## Reference Implementation

Here is a reference implementation for this EIP:

```solidity
contract ERC5269 is IERC5269 {
    bytes32 constant public EIP_STATUS = keccak256("DRAFTv1");
    constructor () {
        emit OnSupportEIP(address(0x0), 5269, bytes32(0), EIP_STATUS, "");
    }

    function _supportEIP(
        address /*caller*/,
        uint256 majorEIPIdentifier,
        bytes32 minorEIPIdentifier,
        bytes calldata /*extraData*/)
    internal virtual view returns (bytes32 eipStatus) {
        if (majorEIPIdentifier == 5269) {
            if (minorEIPIdentifier == bytes32(0)) {
                return EIP_STATUS;
            }
        }
        return bytes32(0);
    }

    function supportEIP(
        address caller,
        uint256 majorEIPIdentifier,
        bytes32 minorEIPIdentifier,
        bytes calldata extraData)
    external virtual view returns (bytes32 eipStatus) {
        return _supportEIP(caller, majorEIPIdentifier, minorEIPIdentifier, extraData);
    }
}
```

See `ERC5269.sol`.

Here is an example where a contract of EIP-721 also implement this EIP to make it easier

to detect and discover:

```solidity
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "../ERC5269.sol";
contract ERC721ForTesting is ERC721, ERC5269 {

    bytes32 constant public EIP_FINAL = keccak256("FINAL");
    constructor() ERC721("ERC721ForTesting", "E721FT") ERC5269() {
        _mint(msg.sender, 0);
        emit OnSupportEIP(address(0x0), 721, bytes32(0), EIP_FINAL, "");
        emit OnSupportEIP(address(0x0), 721, keccak256("ERC721Metadata"), EIP_FINAL, "");
        emit OnSupportEIP(address(0x0), 721, keccak256("ERC721Enumerable"), EIP_FINAL, "");
    }

  function supportEIP(
    address caller,
    uint256 majorEIPIdentifier,
    bytes32 minorEIPIdentifier,
    bytes calldata extraData)
  external
  override
  view
  returns (bytes32 eipStatus) {
    if (majorEIPIdentifier == 721) {
      if (minorEIPIdentifier == 0) {
        return keccak256("FINAL");
      } else if (minorEIPIdentifier == keccak256("ERC721Metadata")) {
        return keccak256("FINAL");
      } else if (minorEIPIdentifier == keccak256("ERC721Enumerable")) {
        return keccak256("FINAL");
      }
    }
    return super._supportEIP(caller, majorEIPIdentifier, minorEIPIdentifier, extraData);
  }
}

```

See `ERC721ForTesting.sol`.

## Security Considerations

Similar to EIP-165 callers of the interface MUST assume the smart contract

declaring they support such EIP interfaces doesn’t necessarily correctly support them.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**xinbenlv** (2023-01-10):

Done drafting, now moving to review. Feedback are greatly appreciated

---

**xinbenlv** (2023-01-10):

IIRC, [@Amxx](/u/amxx) you shared briefly an opinion that it seems no one was really using EIP-165 for identifying interface. I share the same feeling.

Therefore, I am proposing this EIP hopefully make it easier to detect and discover EIP behavors.

Your advice and feedback is greatly apprecitated!

---

**fulldecent** (2023-01-11):

A major concern with using ERC numbers to identify a specification is the draft process.

For many years ERC-20 meant one thing. Then it was finally published, and it meant something else. And then it was finalized and it meant some different further.

For more discussion on this topic, please see the standardization process of EIP-820/EIP-1820.

It is to easy to say “I’m ERC-XYZA compliant” (and people forget to say “ERC-XYZA **//DRAFT//**”) then later they are rugpulled because the definition of XYZA changes.

---

**xinbenlv** (2023-01-11):

That’s very good point. It doesn’t only happen to 820/1820, but also 721/821. It also happen to 712 for various version. See V1-V4 for domain separator.

Here are a few options to address the draft issue

- Option 1. For uint256 majorEIPIdentifer, in addition to the lowest 32bits reserved for EIP numbers, designate second lowest 32bits for “draft” and draft version. E.g. the 0 means Final. The 1, 2, 3, 4 are all Draft’ V1, V2, V3, V4.
hence the majorEIPIdentifer of draft v1 ERC20 will be uint192(0) || uint32(1) || uint32(20) = (2^32) + 20 = 4294967316 = 0x100000014
- Option 2. Use a specific minorEIPIdentifer for drafts. Such as keccack256(ERC721-DRAFTv1)
- Option 3. Instead of returning the normal MAGIC_WORD, return something like keccack256(DRAFT) in the return value when using draft.

Any preferences or other alternatives? [@fulldecent](/u/fulldecent)

---

**xinbenlv** (2023-01-11):

[@fulldecent](/u/fulldecent)

Per your suggestion, I updated ERC-5269 Draft with *Option 3* and shared a Reference Implementation on


      ![image](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/ercref/ercref-contracts/tree/main/ERCs/eip-5269)





###



[main/ERCs/eip-5269](https://github.com/ercref/ercref-contracts/tree/main/ERCs/eip-5269)



ERC Reference Implementations. Contribute to ercref/ercref-contracts development by creating an account on GitHub.










as well as



      [github.com](https://github.com/ercref/ercref-contracts/blob/main/contracts/drafts/ERC5269.sol)





####



```sol
// SPDX-License-Identifier: Apache-2.0
// Author: Zainan Victor Zhou
// Source repo: https://github.com/ercref/ercref-contracts
pragma solidity ^0.8.9;

import "./IERC5269.sol";

contract ERC5269 is IERC5269 {
    bytes32 constant public EIP_STATUS = keccak256("DRAFTv1");
    constructor () {
        emit OnSupportEIP(address(0x0), 5269, bytes32(0), EIP_STATUS, "");
    }

    function _supportEIP(
        address /*caller*/,
        uint256 majorEIPIdentifier,
        bytes32 minorEIPIdentifier,
        bytes calldata /*extraData*/)
    internal virtual view returns (bytes32 eipStatus) {
        if (majorEIPIdentifier == 5269) {
```

  This file has been truncated. [show original](https://github.com/ercref/ercref-contracts/blob/main/contracts/drafts/ERC5269.sol)










I also deployed one on goerli

Anyone could try read it on Etherscan: https://goerli.etherscan.io/address/0x33F735852619E3f99E1AF069cCf3b9232b2806bE#readContract

---

**xinbenlv** (2023-01-17):

This EIP is now moved to Review

---

**Arvolear** (2023-01-23):

Like the idea of EIP discovery, which might be useful for off-chain services or extendable dapps. I have several questions regarding the design. Would appreciate an educated reply.

1. The supportEIP function accepts both major and minor identifiers and returns some kind of minor identifier as well. Is there a particular case for that or may the bool flag be more appropriate to return?
2. Basically this function answers the question “Do you support that?”. Why not make it answer the “What do you support?” request instead?
3. I am a tiny bit concerned about the bytecode usage. In the ERC721 example, we are emitting many events and hardcoding some strings that eat bytecode. To be honest, the plain ERC721 contract is already quite large, adding this EIP would potentially make it unusable for applications that want to crank a lot of logic inside. (together with enumerability and royalties).
4. Is the support of EIP-5750 justified? Should the behavior of the supportEIP method be changeable somehow?

---

**xinbenlv** (2023-01-24):

Thanks for the feedback.

## Design Question: What data type and content to return?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arvolear/48/11091_2.png) Arvolear:

> The supportEIP function accepts both major and minor identifiers and returns some kind of minor identifier as well. Is there a particular case for that or may the bool flag be more appropriate to return?

We start-out with **Option (1)** a boolean `true / false` but since it’s only one bit there lacks prevention of **unintentional clash**. And that’s the main reason I believe why ERC721Receiver and the like choose to return a MAGIC_WORD instead.

We then go ahead use a MAGIC_WORD. **Option (2)** returns a single possibility e.g. `keccak256("ERC-5269")`. We get feedback from [@fulldecent](/u/fulldecent) to suggest handling the case when Draft was first written and being adopted by early adopter. Seeing. So we went on to explore **Option (3)**: Use a default value  `keccak256("FINAL")` and it also gives options to support things like `keccak256("DRAFT")` or `keccak256("DRAFTv1")` for early adopters without ambiguity and backwards conflicts.

## Design Question: How about return a list of all ERCs supported?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arvolear/48/11091_2.png) Arvolear:

> Basically this function answers the question “Do you support that?”. Why not make it answer the “What do you support?” request instead?

We have given it a thought, but what makes it hard for us is to make it both inheritable as well as gas efficient. Array operations could be expensive and when inheritance happens, one would need to add more interface supported into the return value. I haven’t figure out away to implement this in an gas efficient way and hence leaving this option out. If anyone knows some easy way to implement such flexible add and remove computation of identifiers, please advise us.

## Design Question: Should the behavior of the supportEIP method be changeable somehow?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arvolear/48/11091_2.png) Arvolear:

> Is the support of EIP-5750 justified? Should the behavior of the supportEIP method be changeable somehow?

Yes, I believe so. Given that `supportEIP` could change based on the `address caller`, we also want to make it future ready for other conditional behavior, such as:

- take timestamp as input, check at given time point whether some EIP is supported
- take some input and give different EIP status version as return value.

etc.

---

**DeFiFoFum** (2023-02-09):

I do appreciate the idea of **ERC-165** and also this proposal to map directly to ERC implementations, but my concern with these standards is that **it’s difficult to enforce that an external contract is being truthful** to the fact they are implementing the correct interface (knowingly or unknowingly), which could (or maybe “would eventually”) lead to unexpected reverts.

It could be cool to provide some sort of tooling, or even Solidity function (not in the specification per se, but as reference material) for a path to being able to verify that in fact an external contract is being truthful. It might require a mix of tools:

1. Single source of truth for ERC interfaces: I’m guessing the github directory of EIPs would be that place (Extra verification points: That information is hashed and that hash is stored on-chain or IPFS for extra proof)
2. Some tool which could find the function selectors of an ERC interface
3. Then verify that an external contract has all of the matching function selectors to prove it does in fact support the interface

Bonus: Ultra proof is to have an oracle network which has sets of whitelisted or blacklisted addresses of which contracts are meeting/not meeting certain standards.

That part really makes it difficult for me to be motivated to devote time to advancing these standards. I’m curious what your thoughts are?

---

**xinbenlv** (2023-04-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/defifofum/48/7006_2.png) DeFiFoFum:

> I do appreciate the idea of ERC-165 and also this proposal to map directly to ERC implementations, but my concern with these standards is that it’s difficult to enforce that an external contract is being truthful to the fact they are implementing the correct interface (knowingly or unknowingly), which could (or maybe “would eventually”) lead to unexpected reverts.

Appreciate the feedback from [@DeFiFoFum](/u/defifofum)

Let me address them individually

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/defifofum/48/7006_2.png) DeFiFoFum:

> my concern with these standards is that it’s difficult to enforce that an external contract is being truthful to the fact they are implementing the correct interface (knowingly or unknowingly), which could (or maybe “would eventually”) lead to unexpected reverts.

I agree with you! This is unfortunately out of the scope of ERC-165 or ERC-5269 but should be addressed in some other places.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/defifofum/48/7006_2.png) DeFiFoFum:

> Single source of truth for ERC interfaces: I’m guessing the github directory of EIPs would be that place (Extra verification points: That information is hashed and that hash is stored on-chain or IPFS for extra proof)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/defifofum/48/7006_2.png) DeFiFoFum:

> Bonus: Ultra proof is to have an oracle network which has sets of whitelisted or blacklisted addresses of which contracts are meeting/not meeting certain standards.

This will be great. Feel free to propose such Oracle.

But here is my two cents about having some Oracle check if some contract “fully comply with certain standard”: given the smart contract can have access control, they could present behavior to one caller under one circumstance but do not respond or revert in another circumstance. Therefore, behavior check would be a whitelisted approach and only have meaning at a given block number.

---

**mudgen** (2023-04-24):

Yes, this looks good to me.

---

**xinbenlv** (2023-04-24):

Thank you [@mudgen](/u/mudgen) . One particular technical decision is whether the `minorEIPIdentifier` to be format of `bytes32` or `string`.

- The bytes32 is native to EVM word-length and benefit for precision and machine compatibility.
- The string makes it more human-readable and potentially work with things like [ENSIP-10].

Any suggestion on this particular pending decision?

---

**sullof** (2023-06-14):

I really like this proposal. There is a necessity for a more adaptable alternative to ERC165. Innovation often leads us to deploy preliminary standard proposals in a production environment. These proposals might undergo changes later on, necessitating a mechanism to support such evolving versions. Thus said, I have a doubt.

The current mechanism in ERC-5269 requires the caller to be aware of all potential versions and statuses beforehand. The comments on the interface indicate that during the EIP procedure, authors can specify their own status aside from `FINAL` or `DRAFT`, such as `keccak256("DRAFTv1")` or `keccak256("DRAFT-option1")`, and such values must be documented in the EIP body.

This, however, creates a broad spectrum of possibilities that could lead to confusion. I propose that the standard should recommend a structured approach to versioning.

A `Major.Minor` versioning scheme, reminiscent of SemVer, could be a viable solution. Under this scheme, any draft would carry a version like `0.1`, `0.2`, and so forth, with the final version designated as `1.0`.

The `supportEIP` function could then return two values representing these versions, as such:

```auto
function supportEIP(
    address caller,
    uint256 majorEIPIdentifier,
    bytes32 minorEIPIdentifier,
    bytes calldata extraData)
  external view returns (uint, uint);
```

In this model, a return value of (0, 0) signifies non-support for the EIP. This approach would not only standardize versioning but also yield readable results, eliminating the need to decode the `keccak256` hash of the identifying string.

---

**sullof** (2023-06-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> One particular technical decision is whether the minorEIPIdentifier to be format of bytes32 or string.

From a readability and usability standpoint, employing a `string` format could be more advantageous.

However, when considering gas consumption, the `bytes32` format might be more suitable. If the function is frequently invoked by other contracts, using a `bytes32` can significantly reduce the gas cost. Strings can vary in length, require more complex operations for manipulation and comparison, and tend to consume more gas due to the extra computational work necessary.

---

**xinbenlv** (2023-06-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> such values must be documented in the EIP body

Sounds like a good idea. we could add a subsection for recommended pre-Status

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> A Major.Minor versioning scheme, reminiscent of SemVer, could be a viable solution. Under this scheme, any draft would carry a version like 0.1, 0.2, and so forth, with the final version designated as 1.0.

Just like to clarify, when I add Major Minor identifiers, the Minor was meant to apply for something like “ERC721Metadata” kind of interface, different from what minor version means in the SemVer scheme.

Now that you say it, maybe the wording of “Major” and “Minor” is confusing. Maybe it should be

- Major Identifier  → ERC Number
- Minor Identifier  → Behavior ID

How does that sound?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> using a bytes32 can significantly reduce the gas cost. Strings can vary in length

Good point. Agreed!

---

**sullof** (2023-06-15):

I’ve utilized the `Major.Minor` format as SemVer standard typically follows a `Major.Minor.Patch` scheme, which demands three uints returned. This seems overkill to me. Note, I’m not discussing subversions here - your strategy is sound for those.

What I’m focusing on are instances where provisional versions conflict with the final one. For example, while implementing ERC-6551 in Cruna Protocol, I’ve encountered an issue. The interface IERC6551Account requires the implementation of:

```auto
function owner() external view returns (address);
```

This should return the token-bound account owner. However, it conflicts with the `owner()` function needed by EIP-173 or EIP-5313 for contract ownership. A comprehensive discussion can be found starting from [this link](https://ethereum-magicians.org/t/erc-6551-non-fungible-token-bound-accounts/13030/125).

My suggestion is renaming the function to:

```auto
function accountOwner() external view returns (address);
```

This change resolves the conflict but breaks compatibility with existing implementations due to the interfaceId alteration. While ERC-165 can’t fix this, ERC-5269 may provide a solution.

Consider defining the current ERC-6551 version as 0.1. If the function is renamed causing a new interfaceId, we could call that version 0.2. Eventually, there will be a finalized version 1.0. With my proposal, the caller receives (0, 1) if the contract implemented the draft version, and (0, 2) or (1, 0), depending on contract deployment timing if the contract implemented latest version.

This approach eliminates ambiguity, making it easier for ERC-6551 proponents to modify their interface, even if it’s already in production.

---

**sullof** (2023-06-18):

Did you see my comment above?

---

**xinbenlv** (2023-06-18):

Just saw it! Will get back to you soon! Thanks for the detailed feedback!

---

**xinbenlv** (2023-11-15):

Feedback from today ERC@Devconnect

- @gnidan : consider include a structure in return value, will be useful for smart contract to call it.
- @amxx:

consider whether it’s necessary to have uint256 as the type for MajorIdentifier and  bytes32 as type for MinorIdentifier
- it seems a chicken and egg problem to have this ERC adopted

---

**xinbenlv** (2024-05-22):

A valuable feedback from [@Vectorized](/u/vectorized)

- ERC-165 is hard to work with when in diamond inheritance
- ERC-165 can’t represent any ERC without a method


*(2 more replies not shown)*

---
source: magicians
topic_id: 14056
title: "ERC-6956: Asset-Bound Non-Fungible Tokens"
author: tbergmueller
date: "2023-04-29"
category: ERCs
tags: [erc, nft, phygital]
url: https://ethereum-magicians.org/t/erc-6956-asset-bound-non-fungible-tokens/14056
views: 4195
likes: 8
posts_count: 10
---

# ERC-6956: Asset-Bound Non-Fungible Tokens

A standard interface, reference implementation and caveats on implementation of Asset-Bound NFTs. This was originally developed for the use with physical assets and goods (e.g. physical collectables, machine parts, …) and has been extended to be suitable for any digital (off-chain!) assets. Asset-Bound NFTs can even be used with abstract assets, such as e.g. club memberships as well.

# TLDR

Asset-bound Non-Fungible Tokens anchor a token 1:1 to a (physical or digital) asset and token transfers are authorized through attestation of control over the asset by an oracle

# Specification


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-6956)





###



Asset-bound NFTs anchor a token 1-1 to an asset and operations are authorized through oracle-attestation of control over the asset










TLDR, the proposed standard interface:

```solidity
// SPDX-License-Identifier: MIT OR CC0-1.0
pragma solidity ^0.8.18;

/**
 * @title IERC6956 Asset-Bound Non-Fungible Tokens
 * @notice Asset-bound Non-Fungible Tokens anchor a token 1:1 to a (physical or digital) asset and token transfers are authorized through attestation of control over the asset
 * @dev See https://eips.ethereum.org/EIPS/eip-6956
 *      Note: The ERC-165 identifier for this interface is 0xa9cf7635
 */
interface IERC6956 {

    /** @dev Authorization, typically mapped to authorizationMaps, where each bit indicates whether a particular ERC6956Role is authorized
     *      Typically used in constructor (hardcoded or params) to set burnAuthorization and approveAuthorization
     *      Also used in optional updateBurnAuthorization, updateApproveAuthorization, I
     */
    enum Authorization {
        NONE,               // = 0,      // None of the above
        OWNER,              // = (10) of the anchored token
     */
    event AnchorApproval(address indexed owner, address approved, bytes32 indexed anchor, uint256 tokenId);

    /**
     * @notice This emits when the ownership of any anchored NFT changes by any mechanism
     * @dev This emits together with tokenId-based ERC-721.Transfer and provides an anchor-perspective on transfers
     * @param from The previous owner, address(0) indicate there was none.
     * @param to The new owner, address(0) indicates the token is burned
     * @param anchor The anchor which is bound to tokenId
     * @param tokenId ID (>0) of the anchored token
     */
    event AnchorTransfer(address indexed from, address indexed to, bytes32 indexed anchor, uint256 tokenId);
    /**
     * @notice This emits when an attestation has been used indicating no second attestation with the same attestationHash will be accepted
     * @param to The to address specified in the attestation
     * @param anchor The anchor specificed in the attestation
     * @param attestationHash The hash of the attestation, see ERC-6956 for details
     * @param totalUsedAttestationsForAnchor The total number of attestations already used for the particular anchor
     */
    event AttestationUse(address indexed to, bytes32 indexed anchor, bytes32 indexed attestationHash, uint256 totalUsedAttestationsForAnchor);

    /**
     * @notice This emits when the trust-status of an oracle changes.
     * @dev Trusted oracles must explicitely be specified.
     *      If the last event for a particular oracle-address indicates it's trusted, attestations from this oracle are valid.
     * @param oracle Address of the oracle signing attestations
     * @param trusted indicating whether this address is trusted (true). Use (false) to no longer trust from an oracle.
     */
    event OracleUpdate(address indexed oracle, bool indexed trusted);

    /**
     * @notice Returns the 1:1 mapped anchor for a tokenId
     * @param tokenId ID (>0) of the anchored token
     * @return anchor The anchor bound to tokenId, 0x0 if tokenId does not represent an anchor
     */
    function anchorByToken(uint256 tokenId) external view returns (bytes32 anchor);
    /**
     * @notice Returns the ID of the 1:1 mapped token of an anchor.
     * @param anchor The anchor (>0x0)
     * @return tokenId ID of the anchored token, 0 if no anchored token exists
     */
    function tokenByAnchor(bytes32 anchor) external view returns (uint256 tokenId);

    /**
     * @notice The number of attestations already used to modify the state of an anchor or its bound tokens
     * @param anchor The anchor(>0)
     * @return attestationUses The number of attestation uses for a particular anchor, 0 if anchor is invalid.
     */
    function attestationsUsedByAnchor(bytes32 anchor) view external returns (uint256 attestationUses);
    /**
     * @notice Decodes and returns to-address, anchor and the attestation hash, if the attestation is valid
     * @dev MUST throw when
     *  - Attestation has already been used (an AttestationUse-Event with matching attestationHash was emitted)
     *  - Attestation is not signed by trusted oracle (the last OracleUpdate-Event for the signer-address does not indicate trust)
     *  - Attestation is not valid yet or expired
     *  - [if IERC6956AttestationLimited is implemented] attestationUsagesLeft(attestation.anchor) 0)
     * @return attestationHash The attestation hash computed on-chain as `keccak256(attestation)`
     */
    function decodeAttestationIfValid(bytes memory attestation, bytes memory data) external view returns (address to, bytes32 anchor, bytes32 attestationHash);

    /**
     * @notice Indicates whether any of ASSET, OWNER, ISSUER is authorized to burn
     */
    function burnAuthorization() external view returns(Authorization burnAuth);

    /**
     * @notice Indicates whether any of ASSET, OWNER, ISSUER is authorized to approve
     */
    function approveAuthorization() external view returns(Authorization approveAuth);

    /**
     * @notice Corresponds to transferAnchor(bytes,bytes) without additional data
     * @param attestation Attestation, refer ERC-6956 for details
     */
    function transferAnchor(bytes memory attestation) external;

    /**
     * @notice Changes the ownership of an NFT mapped to attestation.anchor to attestation.to address.
     * @dev Permissionless, i.e. anybody invoke and sign a transaction. The transfer is authorized through the oracle-signed attestation.
     *  - Uses decodeAttestationIfValid()
     *  - When using a centralized "gas-payer" recommended to implement IERC6956AttestationLimited.
     *  - Matches the behavior of ERC-721.safeTransferFrom(ownerOf[tokenByAnchor(attestation.anchor)], attestation.to, tokenByAnchor(attestation.anchor), ..) and mint an NFT if `tokenByAnchor(anchor)==0`.
     *  - Throws when attestation.to == ownerOf(tokenByAnchor(attestation.anchor))
     *  - Emits AnchorTransfer
     *
     * @param attestation Attestation, refer EIP-6956 for details
     * @param data Additional data, may be used for additional transfer-conditions, may be sent partly or in full in a call to safeTransferFrom
     *
     */
    function transferAnchor(bytes memory attestation, bytes memory data) external;

     /**
     * @notice Corresponds to approveAnchor(bytes,bytes) without additional data
     * @param attestation Attestation, refer ERC-6956 for details
     */
    function approveAnchor(bytes memory attestation) external;

     /**
     * @notice Approves attestation.to the token bound to attestation.anchor. .
     * @dev Permissionless, i.e. anybody invoke and sign a transaction. The transfer is authorized through the oracle-signed attestation.
     *  - Uses decodeAttestationIfValid()
     *  - When using a centralized "gas-payer" recommended to implement IERC6956AttestationLimited.
     *  - Matches the behavior of ERC-721.approve(attestation.to, tokenByAnchor(attestation.anchor)).
     *  - Throws when ASSET is not authorized to approve.
     *
     * @param attestation Attestation, refer EIP-6956 for details
     */
    function approveAnchor(bytes memory attestation, bytes memory data) external;

    /**
     * @notice Corresponds to burnAnchor(bytes,bytes) without additional data
     * @param attestation Attestation, refer ERC-6956 for details
     */
    function burnAnchor(bytes memory attestation) external;

    /**
     * @notice Burns the token mapped to attestation.anchor. Uses ERC-721._burn.
     * @dev Permissionless, i.e. anybody invoke and sign a transaction. The transfer is authorized through the oracle-signed attestation.
     *  - Uses decodeAttestationIfValid()
     *  - When using a centralized "gas-payer" recommended to implement IERC6956AttestationLimited.
     *  - Throws when ASSET is not authorized to burn
     *
     * @param attestation Attestation, refer EIP-6956 for details
     */
    function burnAnchor(bytes memory attestation, bytes memory data) external;
}
```

# Abstract

This standard allows to integrate physical and digital ASSETS without signing capabilities into dApps/web3 by extending ERC-721.

An ASSET, for example a physical object, is marked with a uniquely identifiable ANCHOR. The ANCHOR is bound in a secure and inseperable manner 1:1 to an NFT on-chain - over the complete life cylce of the ASSET.

Through an ATTESTATION, an ORACLE testifies that a particular ASSET associated with an ANCHOR has been CONTROLLED when defining the `to`-address for certain operations (mint, transfer, burn, approve, …). The ORACLE signs the ATTESTATION off-chain. The operations are authorized through verifying on-chain that ATTESTATION has been signed by a trusted ORACLE. Note that authorization is solely provided through the ATTESTATION, or in other words, through PROOF-OF-CONTROL over the ASSET. The controller of the ASSET is guaranteed to be the controller of the Asset-Bound NFT.

The proposed ATTESTATION-authorized operations such as `transferAnchor(attestation)` are permissionless, meaning neither the current owner (`from`-address) nor the receiver (`to`-address) need to sign.

Figure 1 shows the data flow of an ASSET-BOUND NFT transfer through a simplified example system employing the proposed standard. The system is utilizing a smartphone as user-device to interact with a physical ASSET and specify the `to`-address.

[![Figure 1: Sample system](https://ethereum-magicians.org/uploads/default/optimized/2X/4/47d22e7bfd7374e43beee279aa06c37cfb3f8786_2_690x254.jpeg)Figure 1: Sample system1920×709 62.9 KB](https://ethereum-magicians.org/uploads/default/47d22e7bfd7374e43beee279aa06c37cfb3f8786)

# Illustrative use-case

This corresponds to the  **Posession based digital twin** use case outlined in the EIP.

For illustration and as shown in [this video](https://youtu.be/bz-sgusrcVA), I decided to use a some artwork from my baby-girl, equip it with anchor-technology and hang that artwork in an NFT-Frame in the alpha-version of [HELIX Metaverse](https://helixmetaverse.com/)

[![helix_eip](https://ethereum-magicians.org/uploads/default/optimized/2X/4/4d3469c9f26a8c5ee3a03571313c1dd55bb0b8b7_2_690x389.jpeg)helix_eip1920×1085 131 KB](https://ethereum-magicians.org/uploads/default/4d3469c9f26a8c5ee3a03571313c1dd55bb0b8b7)

Left picture on the wall: Artwork from my daughter represented through Asset-Bound NFT

Right picture on the wall: Lighter from Lukas, the co-author, represented through Asset-Bound NFT

Video of the complete system in action: https://youtu.be/bz-sgusrcVA

# Rationale (Shortened!)

ERC-721 outlines that “NFTs can represent ownership over digital or physical assets”. ERC-721 excels in this task when used to represent ownership over digital, on-chain assets, i.e. when the asset is “holding a token of a specific contract” or the asset is an NFT’s metadata. However, we do see the inherent problem of non-enforcability, when ERC-721 is used without further adaptions to represent off-chain ASSETs, in particular physical objects or goods such as physical collectibles, cars, rental agreements involving physical goods etc.

When an off-chain ASSET’s ownership or posession changes, this shall be refleced on-chain through the corresponding NFT. Over an ASSET’s lifecycle, the ASSET’s ownership and posession state changes multiple, sometimes thousands, of times. Each of those state changes may result in shifting obligations and privileges for the involved parties. Therefore tokenization of an ASSET *without* enforcably anchoring the ASSET’s associated obligation and properties to the token is not complete. Nowadays, off-chain ASSETs are often “anchored” through adding an ASSET-identifier to a NFT’s metadata. Metadata is off-chain. The majority of implementations completely neglect that metadata can be changed off-chain. More serious implementations strive to preserve integrity by e.g. hashing metadata and storing the hash mapped to the tokenId on-chain. However, this approach does not allow for use-case, where metadata besides the asset-identifier, e.g. traits, “hours played”, … shall be mutable or evolvable.

In the proposed EIP we suggest to map an ASSET identifier (`ANCHOR`) on-chain to `tokenId`s.

Even if a (physical) ASSET is mass produced with fungible characteristics, each ASSET has an individual property graph and thus shall be represented in a non-fungible way. Hence this EIP follows the design decision that ASSET (represented via a unique asset identifier called ANCHOR) and token are always mapped 1-1 and not 1-N, so that a token represents the individual property graph of the ASSET.

In this EIP we propose a standard and two optional extensions that cover tokenization in ownership- and posession-based use cases. We will denote the standard and it’s extensions through their interface names, i.e. the standard is IERCxxxx, while the extensions are IERCxxxxAttestationLimited and IERCxxxFloatable.

# Current status

We have gathered a vast amount of use-case feedback for use with **physical assets**. Main interested industries (with some already implementations exist)

- Phygital Collectables [References still under NDA unfortunately]
- Representing physical or phygital objects in Metaverses and Gaming (aka Digital Twin)
- Wine & Spirits, e.g. some of our early customers Crypto Gin or especially nice use case with Dreissigacker wine, where you can digitally trade the NFT representing a bottle of wine, that’s still aging in the winery’s cellar for years.
- Logistics, especially for parts or spare-parts in automotive (warranty, liability, … )
- Players from DeFi have expressed great interested as it enables or improves use-cases where physical goods are used as collateral. We ensured the proposed EIP can be extended with Lock-/Lien-Mechanisms on assets, such as ERC-5058: Lockable Non-Fungible Tokens or ERC-5753: Lockable Extension for EIP-721. Also, ERC-5604: NFT Lien.

An earlier version of the Reference Implementation (using a transfer mechnism listed as “Alternatives considered” has already been security-reviewed successfully, the present EIP Draft will be reviewed later as well)

We are very much looking forward to your technical and use-case input. We are in particular looking for comments and discussion on

- Use-cases with digital off-chain assets, such as [Insert creative use-case here]
- Use-cases with abstract off-chain assets, such as memberships, …
- Implementation aspects
- Security concerns

## Replies

**tbergmueller** (2023-04-30):

[@TimDaub](/u/timdaub) I hope it’s ok mentioning you here;

Considering your [ERC-5192: Minimal Soulbound NFTs](https://eips.ethereum.org/EIPS/eip-5192) :

In our case, transfers can be authorized through owner, approved OR the novel attestation via transferAnchor(), where in a nutshall a trusted oracle is authorized to sign transfers off-chain.

Would it be fair to say `transferable(tokenId)` shall in our case only return true, if owner or approved can transfer?

Note via attestation a particular token can technically still be transferred, but neither the owner nor approved can initiate/sign a transfer for that particular token. So for market-places, the token is effectively non-transferable.

In case there is a clear answer to this question, it would be possible to extend our proposed EIP with the Lock / Unlock events, and we would implement ERC-5192 ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**tbergmueller** (2023-06-26):

Quick update on progress (outside ethereum-magicians);

A security review of the first projects using ERC-6956 reference implementation are currently done, ERC-6956 results will be shared here

We have a short session at Blockchance 2023 conference in Hamburg, Germany this Friday. Rather to present our product, but we chose ERC-6956 for the title as well, as it’s a key component. I will be there all three days as well, in case somebody wants to play around with it or discuss in person.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/c/cafe55fc3a31e3b6c4b97906497f6f890b81447f_2_690x181.png)image1138×299 31.7 KB](https://ethereum-magicians.org/uploads/default/cafe55fc3a31e3b6c4b97906497f6f890b81447f)

As soon as security review is done, we will incorporate eventual changes and then propose to move into the “IN REVIEW” status.

In the magicians-forum here we did receive some likes (also on related comments in different threads) but no dedicated feedback on the ERC yet. Feedback is still much appreciated, I cannot really believe the first draft is already perfect ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=15)

---

**tbergmueller** (2023-10-11):

As posted in  [Update EIP-6956: Fix typos by xiaolou86 · Pull Request #7834 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7834#issuecomment-1758258852)

Saftey advise in case you’re implementing:

We plan to simplify the EIP in the coming weeks/month significantly. In a nutshell

- the mapping ``anchor <> tokenID` will become optional, since in many use-cases it is not needed and a randomized tokenId (leveraging the full uint256) has the same level of security.
- This is expected to decrease gas significantly and simplifies interaction with the contract.
- this should be possible without breaking changes.
- (Events may only carry tokenId, some may become obsolete)

Also Details on Digital Assets will be added.

We will move this - on Pooja’s recommendation in Discord - to In Review prior to applying the changes in order to avoid the EIP becoming Stagnant

---

**tbergmueller** (2023-10-15):

Integration example of Asset-Bound NFTs: https://youtu.be/jwTNJywnCcY

(Voice-over is rather non-technical)

Physical Anchor-Technology and Oracle used:

[Meta Anchor](http://metaanchor.io/) (Random holographic fingerprint, counterfeit-proof)

Blockchain-Transactions of the transfers shown in video:

Bob to Alice: https://polygonscan.com/tx/0xaa2b1a6b2f4fa1cbe5447ade149cb56627ac066d3f61d28e69115dbc8af48829

Alice to Bob: https://polygonscan.com/tx/0x3c0bc69955016754a728f4583de4d87f176a4cdff2a6fdda58813589c0d97360

---

**sullof** (2023-10-15):

I believe that the proposal is generic enough to be used to manage identities without needing extra data.

Did you consider this specific use-case?

About the lock-unlock, I suggest you take a look to [ERC6982](https://eips.ethereum.org/EIPS/eip-6982) and [ERC6454](https://eips.ethereum.org/EIPS/eip-6454), their combination should address all your concerns.

---

**tbergmueller** (2023-10-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> I believe that the proposal is generic enough to be used to manage identities without needing extra data.
> Did you consider this specific use-case?

I’m not quite sure I follow this - could you please elaborate?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> About the lock-unlock, I suggest you take a look to ERC6982 and ERC6454, their combination should address all your concerns.

Yes, I did, and especially [ERC-6982: Efficient Default Lockable Tokens](https://eips.ethereum.org/EIPS/eip-6982) is suitable. Will also consider (and reference) this in the next iteration of the proposal

---

**sullof** (2023-10-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tbergmueller/48/9196_2.png) tbergmueller:

> I’m not quite sure I follow this - could you please elaborate?

I mean that your proposal is trying to create connections between physical assets and digital tokens, but it can be used to connect a physical status to a digital token as well. Let’s say that the ISSUER is the government and the issued asset is a passport. I am quite sure that your proposal would also cover that case. If so, its scope is much larger. What do you think?

---

**tbergmueller** (2023-10-22):

An interesting thought - and yes, I think it would work!

The proposal aims to implement an “asset first”-approach. (Oracle-attested) Possession of the ASSET authorizes transfers of the asset-bound NFT.

In the passport example, possessing the [physical] PASSPORT would mean I can transfer the passport-bound NFT to other wallets without needing to bother the ISSUER. This can be useful in case I want to switch my wallet, especially in the case when I lost access to the wallet, e.g. lost private key, seed phrase etc.

Also - as long as not floatable - the passport-bound NFT could not be stolen/drained from my wallet, so identity theft through digital scams can also be prevented.

---

**tbergmueller** (2024-02-05):

Note for readers;

Some related discussion concerning Adaption of ERC-6982 (Default Lockable) in this proposal is here: [ERC-6982: Default Lockable Proposal - #58 by tbergmueller](https://ethereum-magicians.org/t/erc-6982-default-lockable-proposal/13366/58)


---
source: magicians
topic_id: 15269
title: ERC-7439 Prevent ticket touting
author: sandy-sung-lb
date: "2023-07-28"
category: ERCs
tags: [nft, token, erc-721]
url: https://ethereum-magicians.org/t/erc-7439-prevent-ticket-touting/15269
views: 2166
likes: 6
posts_count: 7
---

# ERC-7439 Prevent ticket touting

---

## eip: 7439
title: Prevent ticket touting.
description: An interface for customers to resell their tickets via authorized ticket resellers and stop audiences being exploited in the ticket scalping.
author: Taien Wang(@taien-wang-lb), Mars Peng(@mars-peng-lb), Sandy Sung()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2023-07-28

## Abstract

This standard is an extension of EIP-721 and defines standard functions outlining a scope for ticketing agents or event organizers to take preventative actions to stop audiences being exploited in the ticket scalping market and allow customers to resell their tickets via authorized ticket resellers.

## Motivation

Industrial-scale ticket touting has been a longstanding issue, with its associated fraud and criminal problems leading to unfortunate incidents and waste of social resources. It is also hugely damaging to artists at all levels of their careers and to related businesses across the board. Although the governments of various countries have begun to legislate to restrict the behavior of scalpers, the effect is limited. They still sold tickets for events at which resale was banned or did not yet own then obtained substantial illegal profits from speculative selling. We consulted many opinions to provide a consumer-friendly resale interface, enabling buyers to resell or reallocate a ticket at the price they initially paid or less is the efficient way to rip off “secondary ticketing”.that enables ticketing agents to utilize

The typical ticket may be a “piece of paper” or even a voucher in your email inbox, making it easy to counterfeit or circulate. To restrict the transferability of these tickets, we have designed a mechanism that prohibits ticket transfers for all parties, including the ticket owner, except for specific accounts that are authorized to transfer tickets. The specific accounts may be ticketing agents, managers, promoters and authorized resale platforms. Therefore, the ticket touts are unable to transfer tickets as they wish. Furthermore, to enhance functionality, we have implemented a token info schema to each ticket,  allowing only authorized accounts(excluding the owner) to modify these records.

This standard defines a framework that enables ticketing agents to utilize ERC-721 tokens as event tickets and restricts token transferability to prevent ticket touting. By implementing this standard, we aim to protect customers from scams and fraudulent activities.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Interface

The interfaces and structure referenced here are as followed

- TokenInfo

signature: Recommend that the adapter self-defines what to sign using the user’s private key or agent’s private key to prove the token validity.
- status: Represent token current status.
- expireTime: Recommend set to the event due time.

TokenStatus

- Sold: When a token is sold, it MUST change to Sold. The token is valid in this status.
- Resell: When a token is in the secondary market, it MUST be changed to Resell. The token is valid in this status.
- Void: When the token owner engages in an illegal transaction, the token status MUST be set to Void, and the token is invalid in this status.
- Redeemed:  When the token is used, it is RECOMMENDED to change the token status to Redeemed.

```solidity
// SPDX-License-Identifier: CC0-1.0
pragma solidity 0.8.19;

/// @title IERC7439 Prevent Ticket Touting Interface
interface IERC7439 {

    /// @dev TokenStatus represent the token current status, only specific role can change status
    enum TokenStatus{
        Sold,        // 0
        Resell,      // 1
        Void,        // 2
        Redeemed     // 3
    }

    /// @param signature Data signed by user's private key or agent's private key
    /// @param status Token current status
    /// @param expireTime Event due time
    struct TokenInfo {
        bytes signature;
        TokenStatus status;
        uint256 expireTime;
    }
}
```

## Rationale

To support customer-oriented resale mechanism and customer-only ticket sale, while also increasing the speculative threshold for speculators to ensure fairness in the market.

TBD

## Backwards Compatibility

This proposal is fully backward compatible with EIP-721.

## Test Cases

```javascript
const { expectRevert } = require("@openzeppelin/test-helpers");
const { expect } = require("chai");
const ERCXXX = artifacts.require("ERCXXX");

contract("ERCXXX", (accounts) => {
  const [deployer, partner, userA, userB] = accounts;
  const expireTime = 19999999;
  const tokenId = 0;
  const signature = "0x993dab3dd91f5c6dc28e17439be475478f5635c92a56e17e82349d3fb2f166196f466c0b4e0c146f285204f0dcb13e5ae67bc33f4b888ec32dfe0a063e8f3f781b"
  const zeroHash = "0x";

  beforeEach(async () => {
    this.ercXXX = await ERCXXX.new({
      from: deployer,
    });
    await this.ercXXX.mint(userA, signature, { from: deployer });
  });

  it("Should mint a token", async () => {
    const tokenInfo = await this.ercXXX.tokenInfo(tokenId);

    expect(await this.ercXXX.ownerOf(tokenId)).to.equal(userA);
    expect(tokenInfo.signature).equal(signature);
    expect(tokenInfo.status).equal("0"); // Sold
    expect(tokenInfo.expireTime).equal(expireTime);
  });

  it("should ordinary users cannot transfer successfully", async () => {
    expectRevert(await this.ercXXX.transferFrom(userA, userB, tokenId, { from: userA }), "ERCXXX: You cannot transfer this NFT!");
  });

  it("should partner can transfer successfully and chage the token info to resell status", async () => {
    const tokenStatus = 1; // Resell

    await this.ercXXX.changeState(tokenId, zeroHash, tokenStatus, { from: partner });
    await this.ercXXX.transferFrom(userA, partner, tokenId, { from: partner });

    expect(tokenInfo.tokenHash).equal(zeroHash);
    expect(tokenInfo.status).equal(tokenStatus); // Resell
    expect(await this.ercXXX.ownerOf(tokenId)).to.equal(partner);
  });

  it("should partner can change the token status to void", async () => {
    const tokenStatus = 2; // Void

    await this.ercXXX.changeState(tokenId, zeroHash, tokenStatus, { from: partner });

    expect(tokenInfo.tokenHash).equal(zeroHash);
    expect(tokenInfo.status).equal(tokenStatus); // Void
  });

  it("should partner can change the token status to redeemed", async () => {
    const tokenStatus = 3; // Redeemed

    await this.ercXXX.changeState(tokenId, zeroHash, tokenStatus, { from: partner });

    expect(tokenInfo.tokenHash).equal(zeroHash);
    expect(tokenInfo.status).equal(tokenStatus); // Redeemed
  });

  it("should partner can resell the token and change status from resell to sold", async () => {
    let tokenStatus = 1; // Resell
    await this.ercXXX.changeState(tokenId, zeroHash, tokenStatus, { from: partner });
    await this.ercXXX.transferFrom(userA, partner, tokenId, { from: partner });

    expect(tokenInfo.status).equal(tokenStatus); // Resell
    expect(tokenInfo.tokenHash).equal(zeroHash);

    tokenStatus = 0; // Sold
    const newSignature = "0x113hqb3ff45f5c6ec28e17439be475478f5635c92a56e17e82349d3fb2f166196f466c0b4e0c146f285204f0dcb13e5ae67bc33f4b888ec32dfe0a063w7h2f742f";
    await this.ercXXX.changeState(tokenId, newSignature, tokenStatus, { from: partner });
    await this.ercXXX.transferFrom(partner, userB, tokenId, { from: partner });

    expect(tokenInfo.status).equal(tokenStatus); // Sold
    expect(tokenInfo.tokenHash).equal(newSignature);
  });
});

```

## Reference Implementation

```javascript
// SPDX-License-Identifier: CC0-1.0
pragma solidity 0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
// If you need additional metadata, you can import ERC721URIStorage
// import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "./IERCXXX.sol";

contract ERCXXX is ERC721, AccessControl, IERCXXX {
    using Counters for Counters.Counter;

    bytes32 public constant PARTNER_ROLE = keccak256("PARTNER_ROLE");
    Counters.Counter private _tokenIdCounter;

    uint256 public expireTime;

    mapping(uint256 => TokenInfo) public tokenInfo;

    constructor(uint256 _expireTime) ERC721("MyToken", "MTK") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(PARTNER_ROLE, msg.sender);
        expireTime = _expireTime;
    }

    function safeMint(address to, bytes memory signature) public {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
        tokenInfo[tokenId] = TokenInfo(signature, TokenStatus.Sold, expireTime);
    }

    function changeState(
        uint256 tokenId,
        bytes memory signature,
        TokenStatus tokenStatus,
        uint256 newExpireTime
    ) public onlyRole(PARTNER_ROLE) {
        tokenInfo[tokenId] = TokenInfo(signature, tokenStatus, newExpireTime);
    }

    function _burn(uint256 tokenId) internal virtual override(ERC721) {
        super._burn(tokenId);

        if (_exists(tokenId)) {
            delete tokenInfo[tokenId];
            // If you import ERC721URIStorage
            // delete _tokenURIs[tokenId];
        }
    }

    function supportsInterface(
        bytes4 interfaceId
    ) public view virtual override(AccessControl, ERC721) returns (bool) {
        return
            interfaceId == type(IERCXXX).interfaceId ||
            super.supportsInterface(interfaceId);
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal virtual override(ERC721) {
        if (!hasRole(PARTNER_ROLE, _msgSender())) {
            require(
                from == address(0) || to == address(0),
                "ERCXXX: You cannot transfer this NFT!"
            );
        }

        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }
}

```

## Security Considerations

There are no security considerations related directly to the implementation of this standard.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**Mani-T** (2023-07-29):

E-ticket often contain additional metadata about the event, such as event details, venue information, etc.  What about them?

---

**sandy-sung-lb** (2023-08-01):

Hi Mani-T,

Thanks for your question. You can add ERC721URIStorage to this EIP and store the additional event info, whether on-chain or off-chain.

I also draft the ERC721URIStorage import in **Reference Implementation** section.

Sandy

---

**0xTraub** (2023-08-01):

If anyone is curious the website https://cashortrade.org is probably the best closest web2 analogue. Tickets are listed and traded P2P and not allowed above face-value with CoT acting only as an intermediary on releasing funds (but we don’t need centralized intermediaries in this instance)

One potential idea for how to prevent scalpers is to mint the ticket and have some value attached to it representing “face value”. For example, if I mint it at 100 USDC then i should be able to query the value on the contract directly that tells me the face value, and then exchanges it is listed on or users can query this information to know they’re not being ripped off. This way you don’t need an authorized reseller you only need to know the price they originally paid for it.

I’ve proposed a potential EIP that can be used in conjunction with this.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xtraub/48/7553_2.png)
    [EIP Idea: Valuing Financial NFTs](https://ethereum-magicians.org/t/eip-idea-valuing-financial-nfts/15295) [EIPs](/c/eips/5)



> As DeFi continues to expand into new use-cases, the complexity of representing various financial positions can no longer be accomplished solely with fungible ERC-20 tokens. New financial NFTs (FNFTs) have no agreed upon standard for calculating their value on-chain. These financial positions tokenized as NFTs which cannot be valued cannot be used in DeFi. As a result a new standard is needed to be able to universally value these increasingly-complex financial instruments. Revest Finance proposes…

---

**sandy-sung-lb** (2023-08-02):

Hi 0xTraub,

Thanks for your reply. I agree with you that having a “face value” on the token for anyone to query, without the need for an authorized reseller, is beneficial from a value perspective. However, what I am more concerned about is the “source”. In reality, many people are willing to pay above the face value to ensure they can get tickets. You never know if they pay for the ticket besides the face value.

When this ticket is in high demand, it also means that many people are falling victim to fraud. For example, if there is no authorized reseller, sellers and buyers can agree on a specific amount beforehand outside of the face value. Once both parties confirm the agreement, the seller will then transfer the ticket to the buyer at its face value. However, in many cases, sellers receive the payment in advance but do not proceed with the next steps.

Media reports have estimated that the secondary ticket market is worth up to £1 billion a year in England. The value of the secondary ticket market is currently opaque. This opacity could result in unfair pricing, making it difficult for consumers to determine reasonable ticket prices. It may also hinder ticketing companies and event organizers from controlling the market and safeguarding fair ticket pricing and sales strategies. Such circumstances could impact market fairness and consumer rights. Therefore, enhancing transparency and legality is one of the crucial directions to improve the secondary ticket market.

The lack of legislation outlawing the unauthorized resale of tickets and the absence of regulation of the primary and secondary ticket market encourage unscrupulous practices, lack of transparency and fraud.

Sandy

---

**0xTraub** (2023-08-08):

While you make some fair points I think it would be pretty easy to get the support from the community to tell ticket resellers to get f****d for not being able to scalp people, but that’s a different argument. Given the ability to just look at the NFT contract representing the ticket origin it isn’t that difficult to verify that a ticket is legitimate because it comes from the legitimate contract. You don’t need to be an authorized reseller if you can prove the ticket is legitimate, in which case the value of the ticket itself should matter more than the seller.

---

**rayzhudev** (2023-12-12):

[@sandy-sung-lb](/u/sandy-sung-lb) I believe this EIP is the wrong approach to solving the problem. Tickets which are NFTs are very easy to tell whether they are authentic or not, by checking the contract address. If they are authentic, there is no problem with reselling them. Thus in order to provide a better secondary ticket marketplace, ticketing platforms should mint their tickets as NFTs. As long as tickets are traded on web2 platforms, scalpers will always exist. Creating an ERC standard for this doesn’t solve the problem since ticket resellers don’t need to use the blockchain.


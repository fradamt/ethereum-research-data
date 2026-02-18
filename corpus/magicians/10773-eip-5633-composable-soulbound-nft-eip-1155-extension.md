---
source: magicians
topic_id: 10773
title: "EIP-5633: Composable Soulbound NFT, EIP-1155 Extension"
author: HonorLabs
date: "2022-09-09"
category: EIPs
tags: [nft, eip165, eip-1155]
url: https://ethereum-magicians.org/t/eip-5633-composable-soulbound-nft-eip-1155-extension/10773
views: 4621
likes: 17
posts_count: 21
---

# EIP-5633: Composable Soulbound NFT, EIP-1155 Extension

---

## eip: 5633
title: Composable Soulbound NFT, EIP-1155 Extension
description: Add composable soulbound property to EIP-1155 tokens
author: HonorLabs (@honorworldio)
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2022-09-09
requires: 165, 1155

## Abstract

This standard is an extension of EIP-1155. It proposes a smart contract interface that can represent any number of soulbound and non-soulbound NFT types. Soulbound is the property of a token that prevents it from being transferred between accounts. This standard allows for each token ID to have its own soulbound property.

## Motivation

The soulbound NFTs similar to World of Warcraft’s soulbound items are attracting more and more attention in the Ethereum community. In a real world game like World of Warcraft, there are thousands of items, and each item has its own soulbound property. For example, the amulate Necklace of Calisea is of soulbound property, but another low level amulate is not. This proposal provides a standard way to represent soulbound NFTs that can coexist with non-soulbound ones. It is easy to design a composable NFTs for an entire collection in a single contract.

This standard outline a interface to EIP-1155 that allows wallet implementers and developers to check for soulbound property of token ID using EIP-165. the soulbound property can be checked in advance, and the transfer function can be called only when the token is not soulbound.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

A token type with a `uint256 id`  is soulbound if function `isSoulbound(uint256 id)` returning true. In this case, all EIP-1155 functions of the contract that transfer the token from one account to another MUST throw, except for mint and burn.

```auto
// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.0;

interface IERC5633 {
  /**
   * @dev Emitted when a token type `id` is set or cancel to soulbound, according to `bounded`.
   */
  event Soulbound(uint256 indexed id, bool bounded);

  /**
   * @dev Returns true if a token type `id` is soulbound.
   */
  function isSoulbound(uint256 id) external view returns (bool);
}
```

Smart contracts implementing this standard MUST implement the ERC-165 supportsInterface function and MUST return the constant value true if 0x911ec470 is passed through the interfaceID argument.

## Rationale

If all tokens in a contract are soulbound by default, `isSoulbound(uint256 id)` should return true by default during implementation.

## Backwards Compatibility

This standard is fully EIP-1155 compatible.

## Test Cases

Run in terminal:

```auto
npx hardhat test
```

### Test code

```auto
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("ERC5633Demo contract", function () {

  it("InterfaceId should equals 0x911ec470", async function () {
    const [owner, addr1, addr2] = await ethers.getSigners();

    const ERC5633Demo = await ethers.getContractFactory("ERC5633Demo");

    const demo = await ERC5633Demo.deploy();
    await demo.deployed();

    expect(await demo.getInterfaceId()).equals("0x911ec470");
  });

  it("Test soulbound", async function () {
    const [owner, addr1, addr2] = await ethers.getSigners();

    const ERC5633Demo = await ethers.getContractFactory("ERC5633Demo");

    const demo = await ERC5633Demo.deploy();
    await demo.deployed();

    await demo.setSoulbound(1, true);
    expect(await demo.isSoulbound(1)).to.equal(true);
    expect(await demo.isSoulbound(2)).to.equal(false);

    await demo.mint(addr1.address, 1, 2, "0x");
    await demo.mint(addr1.address, 2, 2, "0x");

    await expect(demo.connect(addr1).safeTransferFrom(addr1.address, addr2.address, 1, 1, "0x")).to.be.revertedWith(
        "ERC5633: Soulbound, Non-Transferable"
    );
    await expect(demo.connect(addr1).safeBatchTransferFrom(addr1.address, addr2.address, [1], [1], "0x")).to.be.revertedWith(
        "ERC5633: Soulbound, Non-Transferable"
    );
    await expect(demo.connect(addr1).safeBatchTransferFrom(addr1.address, addr2.address, [1,2], [1,1], "0x")).to.be.revertedWith(
        "ERC5633: Soulbound, Non-Transferable"
    );

    await demo.mint(addr1.address, 2, 1, "0x");
    demo.connect(addr1).safeTransferFrom(addr1.address, addr2.address, 2, 1, "0x");
    demo.connect(addr1).safeBatchTransferFrom(addr1.address, addr2.address, [2], [1], "0x");

    await demo.connect(addr1).burn(addr1.address, 1, 1);
    await demo.connect(addr1).burnBatch(addr1.address, [1], [1]);
    await demo.connect(addr2).burn(addr2.address, 2, 1);
    await demo.connect(addr2).burnBatch(addr2.address, [2], [1]);
  });
});

```

test contract:

```auto
// SPDX-License-Identifier: CC0-1.0

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

import "./ERC5633.sol";

contract ERC5633Demo is ERC1155, ERC1155Burnable, Ownable, ERC5633 {
    constructor() ERC1155("") ERC5633() {}

    function mint(address account, uint256 id, uint256 amount, bytes memory data)
        public
        onlyOwner
    {
        _mint(account, id, amount, data);
    }

    function mintBatch(address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
        public
        onlyOwner
    {
        _mintBatch(to, ids, amounts, data);
    }

    function setSoulbound(uint256 id, bool soulbound)
        public
        onlyOwner
    {
        _setSoulbound(id, soulbound);
    }

    // The following functions are overrides required by Solidity.
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC1155, ERC5633)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    function _beforeTokenTransfer(address operator, address from, address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
        internal
        override(ERC1155, ERC5633)
    {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);
    }

    function getInterfaceId() public view returns (bytes4) {
        return type(IERC5633).interfaceId;
    }
}
```

## Reference Implementation

```auto
// SPDX-License-Identifier: CC0-1.0

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "./IERC5633.sol";

/**
 * @dev Extension of ERC1155 that adds soulbound property per token id.
 *
 */
abstract contract ERC5633 is ERC1155, IERC5633 {
    mapping(uint256 => bool) private _soulbounds;

    /// @dev See {IERC165-supportsInterface}.
    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC1155) returns (bool) {
        return interfaceId == type(IERC5633).interfaceId || super.supportsInterface(interfaceId);
    }

    /**
     * @dev Returns true if a token type `id` is soulbound.
     */
    function isSoulbound(uint256 id) public view virtual returns (bool) {
        return _soulbounds[id];
    }

    function _setSoulbound(uint256 id, bool soulbound) internal {
        _soulbounds[id] = soulbound;
        emit Soulbound(id, soulbound);
    }

    /**
     * @dev See {ERC1155-_beforeTokenTransfer}.
     */
    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal virtual override {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);

        for (uint256 i = 0; i CC0.

## Replies

**castillo** (2022-09-25):

I’ve thought of a similar protocol before. In addition to games, there are many other application scenarios. For example, in crypto city, the property rights of citizens’ houses and vehicles are applicable to non-soulbound NFTs, while educational experience and citizen points can be used as soulbound NFTs.

---

**TimDaub** (2022-09-29):

[EIP-5192: Minimal Soulbound NFTs](https://eips.ethereum.org/EIPS/eip-5192) is now final. Maybe this interface can be adopted for EIP-1155 to solve your use case?

---

**HonorLabs** (2022-10-18):

Thanks! I think it’s a good idea, I’ll check out EIP-5192 and see if it’s possible.

---

**HonorLabs** (2022-10-18):

Thanks for reply. It’s a pretty good application scenario.

---

**CHANCE** (2022-10-27):

Contrary to EIP-5192, 5633 solves the problem with well-written and thought-out code. The solution proposed here in 5633 is much better and should and could stand alone.

I would prefer if every soul-bound interface is not itself soul-bound to an EIP that is a less-than-ideal developer, user, aggregate, and analyst experience.

For all soul-bound proposals that address the existing token specification of ERC1155s, 5633 is the best thought-out and most realistic.

Very big supporter of this implementation, thank you, [@HonorLabs](/u/honorlabs) and I look forward to seeing this EIP progress!

The act of this coming in an extension is a great choice. Yet, with 1155s, they carry one distinct nuance in that batch transfers are a default supported function which means now `batchTransferFrom` has 2 very costly for-loops to run.

Is there an existing reference implementation of adding this functionality directly into the transfer loop to illustrate that cost impact does not “*have to be*” high?

---

**TimDaub** (2022-10-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chance/48/7577_2.png) CHANCE:

> Contrary to EIP-5192, 5633 solves the problem with well-written and thought-out code.

kekw

```auto
 event Soulbound(uint256 indexed id, bool bounded);
```

the past form of “bind” is “bound”

---

**CHANCE** (2022-10-27):

The verbiage of an EIP can easily be updated ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

For verbosity, 5633 serves the problem better than 5192 by removing two specific events that create a long runway for usage and adoption issues.

Based on the fact that wording is your only note of resolve here, I presume you are also in support of 5633?

---

**TimDaub** (2022-10-27):

> In this case, all EIP-1155 functions of the contract that transfer the token from one account to another MUST throw, except for mint and burn.

Does this mean a soulbound token can always be burned?

The EIP-5633 implementation overrides `function _beforeTokenTransfer` of OZ but OZ uses this function in e.g. `burn`, so that’d mean the reference implementation and the specification are divergent: [openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol at master · OpenZeppelin/openzeppelin-contracts · GitHub](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC1155/ERC1155.sol#L344)

---

**CHANCE** (2022-11-01):

While antithetical to the idea of a psuedonym-bound token, constant forfeiture prevents tokens from becoming scarlet letters as well as absolves all need of token-breaking standards such a consensual minting.

Generally in EIPs, when something is not included in a must, that means it is a CAN such as:

> In this case, all EIP-1155 functions of the contract that transfer the token from one account to another MUST throw, except for mint and burn that CAN throw depending on implementation details.

---

**HonorLabs** (2022-11-20):

We are very glad you like this proposal, it’s an honor. Our intention is to propose a protocol that is more practical in the real world. Gas cost analysis and optimization is an important task in our next update.

---

**HonorLabs** (2022-11-20):

We implement Non-Transferable logic in the `function _beforeTokenTransfer`, because it’s a most suitable place, the function is called by the three main functional logic: `burn`, `transfer` and `mint`.

User CAN decide whether the token is burnable or not depends on the implementation.

---

**HonorLabs** (2022-11-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chance/48/7577_2.png) CHANCE:

> In this case, all EIP-1155 functions of the contract that transfer the token from one account to another MUST throw, except for mint and burn that CAN throw depending on implementation details.

Very precise description, thank you! ![:clap:](https://ethereum-magicians.org/images/emoji/twitter/clap.png?v=12) ![:clap:](https://ethereum-magicians.org/images/emoji/twitter/clap.png?v=12)

---

**tinom9** (2022-12-16):

What are your thoughts in explicitly making it EIP-721 compatible as well? I don’t love the idea of two separate standards for EIP-721 and EIP-1155 when it can serve both.

---

**yuki-js** (2022-12-17):

I think so too. I posted the proposal that is strongly inspired by EIP-5192 and have a similar interfaces. Please take a look.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yuki-js/48/8029_2.png)
    [EIP-6268: UNTransferability Indicator for EIP-1155](https://ethereum-magicians.org/t/sbt-implemented-in-erc1155/12182) [EIPs](/c/eips/5)



> I submitted an EIP, that is inspired by EIP-5172 and have a similar simple interface.
> This is something like EIP-5172 for EIP-1155.

---

**donnoh** (2022-12-20):

Since EIP5192 is already final it doesn’t make much sense to have both a `locked` and a `isSoulbound`  function that do the same thing.

---

**donnoh** (2022-12-21):

> If all tokens in a contract are soulbound by default, isSoulbound(uint256 id) should return true by default during implementation.

I think the function should throw if the `id` does not exist using the same pattern as other standards.

---

**sullof** (2023-01-11):

The problem with this proposal, as well as with EIP5192, is that they assume that the status of the token switches from transferable to non-transferable and vice versa following a transaction that emits an event. However, this may not always be the case. In the gaming industry, for example, an NFT’s status can change many times a day without any transactions, simply due to changes in context. As a result, the most reliable way to determine whether an NFT is transferable or not is to call a view function.

It is not feasible to implement an interface that requires an event in such scenarios.

So, I believe that events should be removed from this interface. Additionally, I think that the name of the function should be more direct, such as `isTransferable`, however I could survive to different name ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**TimDaub** (2023-01-11):

[@HonorLabs](/u/honorlabs) I’d be happy to adjust EIP-5633 to use the same nomenclature as EIP-5192 (`function locked` and `Locked` and `Unlocked` events and send a PR on GitHub. Is that interesting to you?

---

**stoicdev0** (2023-02-01):

I have the same problem as [@sullof](/u/sullof). Is removing the event an option for you?

---

**sullof** (2023-02-02):

It would make a lot of sense if EIP5633 extends EIP5192.


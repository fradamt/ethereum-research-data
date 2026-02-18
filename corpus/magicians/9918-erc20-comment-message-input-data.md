---
source: magicians
topic_id: 9918
title: ERC20 + Comment/Message/Input data
author: kleopartas
date: "2022-07-12"
category: EIPs
tags: [erc20]
url: https://ethereum-magicians.org/t/erc20-comment-message-input-data/9918
views: 1024
likes: 0
posts_count: 4
---

# ERC20 + Comment/Message/Input data

Hello,

Most banking apps have a comment text field when sending a payment.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8ee7f5a8de1f48ae7cdc0673e6c7c755ef9541ed_2_690x377.jpeg)image1242×680 117 KB](https://ethereum-magicians.org/uploads/default/8ee7f5a8de1f48ae7cdc0673e6c7c755ef9541ed)

Maybe I searched badly, but is there an ERC20 standard that has a comment field that will be in the event?

```auto
interface IERC20Comment {

    event Transfer(
        address indexed from,
        address indexed to,
        uint256 value,
        bytes indexed comment
    );

    function transfer(
        address to,
        uint256 amount,
        bytes comment
    ) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 amount,
        bytes comment
    ) external returns (bool);
}
```

Thanks to this comment field, payment identifiers can be stored there, which will be in the WEB2 database.

## Replies

**TimDaub** (2022-07-12):

Banking interface store this type of message usually where it’s either only accessible to you or you and the receiving party.

However, your suggestion implies that the message would be visible to anyone that has access to an Ethereum node. This violates the privacy context-integrity principle IMO.

The mockup you show with e.g. Metamask: That doesn’t need an adjusted in ERC20. Metamask could just implement and store the messages locally.

---

**kleopartas** (2022-07-12):

Thanks for your reply.

This message is not confidential. In this comment, I would like to store a hash of the transaction data.

My backend:

```auto
const secret = hash(itemIds, "aa1efcb7221a61");
const comment = hash(from, to, value, secret);
```

After the transaction, I check the Transfer event and make sure that the buyer has paid for the item.

```auto
if (comment === hash(event.from, event.to, event.value, secret)) {
    return "success";
}
```

Thanks to the comment, I can know exactly which set of goods the user paid for.

Without the comment, a user could have two sets of items for the same amount, and I wouldn’t be able to find out exactly what was paid for.

---

**kleopartas** (2022-07-12):

I think this extension would solve my problem.

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/utils/Context.sol";

abstract contract ERC20Comment is Context, ERC20 {
    /**
     * @dev Emitted by {transferWithComment} or {transferWithCommentFrom}.
     */
    event Comment(
        string indexed commment,
        address indexed from,
        address indexed to,
        uint256 value
    );

    /**
     * @dev See {IERC20-transfer}.
     *
     * - `commment` is additional field for custom message.
     */
    function transferWithComment(
        address to,
        uint256 amount,
        string memory commment
    ) public virtual returns (bool) {
        address owner = _msgSender();
        _transfer(owner, to, amount);
        emit Comment(commment, owner, to, amount);
        return true;
    }

    /**
     * @dev See {IERC20-transferFrom}.
     *
     * - `commment` is additional field for custom message.
     */
    function transferWithCommentFrom(
        address from,
        address to,
        uint256 amount,
        string memory commment
    ) public virtual returns (bool) {
        address spender = _msgSender();
        _spendAllowance(from, spender, amount);
        _transfer(from, to, amount);
        emit Comment(commment, from, to, amount);
        return true;
    }
}

```

Now any seller who has received a token can always determine which product was paid for.

It’s a pity that the custom field was not added initially (ERC20 standard), it would have pushed wallets (Metamask, etc.) to add a comment field at the time of their creation.


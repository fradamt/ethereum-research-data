---
source: magicians
topic_id: 931
title: MultiDimensional Tokenization
author: cre888
date: "2018-08-01"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/multidimensional-tokenization/931
views: 1088
likes: 1
posts_count: 8
---

# MultiDimensional Tokenization

hi magicians! just wondering if anyone has feedback on ERC-888: https://github.com/ethereum/EIPs/issues/888

troverman created this data structure to enable “multidimensional tokenization,” a singular protocol that objectively represents all possible happenings ~ for example, this utility contract defines balances of personal time “spent” doing context-specific actions (e.g. watching content): https://github.com/ExperienceNovo/bidio/blob/master/api/contracts/viewToken.sol

## Replies

**Ethernian** (2018-08-02):

Is it correct to see it as a token with with subaccounts?

Would you give more UseCases for MultiDimensionalToken as a standard?

---

**cre888** (2018-08-02):

thanks for the questions ~ your description is correct. by inheriting the 888 structure, [address][_id][_value], every dimensional identity could refer to potentially infinite “sub-accounts.” this purposeful design approach is generally useful for nested hierarchies with layers of information and functionality. Re: additional use cases ~ I’d say build whatever you imagine will be true and good for all people. we’re advocating super thin protocols that efficiently spread our intentional energy and its meaning, a.k.a. everyone’s collective interpretation.

---

**Ethernian** (2018-08-02):

> Would you give more UseCases for MultiDimensionalToken as a standard?

> I’d say build whatever you imagine will be true and good for all people.

IMHO, if anybody is free to build everything one can imagine, then we should not talk about *Standard*, we should talk about *DesignPattern*.

A *Standard* is something, that MUST be umplemented exact as described. For some reason.

For example, the ERC20 interface (and protocol) is a *Standard* because exchanges and wallets need an *unified and standard* interface to handle any ERC20 compliant token.

In contrast, the ERC20 implementation,  is a *Design Pattern*, because it can be changed without compatibility to existing Wallets and Exchanges.

It important to separate *Standards* from *Design Patterns* because we MUST agree only on *Standards*, but for *Design Patterns* a roughly consensus is enough.

Therefore, may I ask you, what kind of 3rd party players like exchanges, wallets and so on need the ERC888 as a *Standard*? What UseCase needs it?

unclear.

---

**cre888** (2018-08-03):

sorry I wasn’t clear. think about dimensional voting and other gestalt interactions within a multi-market. how else would a protocol designer achieve the same capabilities?

---

**Ethernian** (2018-08-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> what kind of 3rd party players like exchanges, wallets and so on need the ERC888 as a Standard ? What UseCase needs it?

I am unsure, but possibly communities, organised in hierarchical domains like [colony.io](https://colony.io) needs some kind of token, because every domain could be financially independent.

Have not thought in depth.

---

**cre888** (2018-08-07):

yes! not just any token ~ potentially infinite tokens, which are dimension-specific #pluralism

check this out (still a work in progress):


      [github.com](https://github.com/troverman/conexus/blob/master/api/contracts/DAO.sol)




####

```sol
pragma solidity ^0.4.21;
pragma experimental ABIEncoderV2;

contract ERC888{

    function balanceOf(address _owner, string _id) constant public returns (uint256 balance);
    function eskrowBalanceOf(address _owner, string _id) constant public returns (uint256 balance);
    function transfer(address _to, string _id, uint256 _value) public returns (bool success);
    function transferEskrow(address _address, string _id, uint256 _value, string _type) public returns (bool success);

}

contract Organization {

    struct Organization{
        string title;
        string content;
        address creator;
        address parent;
        address identifer;
```

  This file has been truncated. [show original](https://github.com/troverman/conexus/blob/master/api/contracts/DAO.sol)

---

**milonite** (2018-10-17):

Where I can find the EIP status of ERC-888


---
source: magicians
topic_id: 7554
title: safeTransferFrom can be called by Anyone once setApprovalForAll has been granted on one address
author: JosephF
date: "2021-11-24"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/safetransferfrom-can-be-called-by-anyone-once-setapprovalforall-has-been-granted-on-one-address/7554
views: 2412
likes: 3
posts_count: 3
---

# safeTransferFrom can be called by Anyone once setApprovalForAll has been granted on one address

The OpenZeppelin ERC721 Contract Library (I am using the Upgradeable version, but I assume that the behaviour should be the same in the “standard” non-apgradeable version) has the setApprovalForAll function, which enables an NFT owner to grant an operator to sell any of his Tokens on his behalf. I have used this function in one of my projects, whereby NFT owners grant (solely) my Smart Contract address, the ability to sell their Tokens on their behalf. I have noticed however, that once the setApprovalForAll function has been called by an owner, anyone could call the safeTransferFrom function and not only my Smart Contract or the Owner. This could constitute a major vulnerability in some existing smart contracts, in which the developer would expect that once the setApprovalForAll function has been called, that it would grant only the addresses found in the corresponding mapping to have the ability to call the safeTransferFrom function, but it actually grants anyone this ability.

To reproduce this vulnerability, I have implemented the following:

I have the following function in my ERC721 Smart Contract, which itself calls the safeTransferFrom function:

```auto
function tokTransfer(address payable from, address to, uint256 tokenId, uint256 price) external payable {
   require(msg.value >= price);
   this.safeTransferFrom(from, to, tokenId);
   ...
}
```

Token owners have called the setApprovalForAll on my Smart Contract, granting it authorisation to sell their tokens on their behalf. However, I am able to call this function directly in Truffle with the following statement (using the Purchaser account (i.e. accounts[2]) as the “from” parameter (i.e. _msgSender)):

```auto
instance.tokTransfer(accounts[1], accounts[2], 1001, '2500000000', {from: accounts[2], value: '2500000000'})
```

I can actually call my function, which itself calls the safeTransferFrom OpenZeppelin function, while the Sender (_msgSender) of the Transaction does not satisfy the require statement in the function below (found in the OpenZeppelin Library).

```auto
 function safeTransferFrom(
    address from,
    address to,
    uint256 tokenId,
    bytes memory _data
 ) public virtual override {
    require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: transfer caller is not owner nor approved");
    _safeTransfer(from, to, tokenId, _data);
 }
```

I have used the account (accounts[2]), which corresponds to the purchaser in the transaction above to make it clear and to emphasise on the vulnerability, but any account could be used for the “from” parameter. Also, please note that I am testing this using Ganache, just in case that this issue does not exist on the public Testnets or the Main Blockchain (I haven’t tested it on these yet), although I would expect it to behave the same.

Thank you.

Joseph F

## Replies

**rmeissner** (2021-11-24):

Probably more a question for the openzepplin forum or solidity forum.

I didn’t look into it in detail, but one thing to note: when you call a function of a the contract with `this.` it will trigger an internal transaction and therefore `msg.sender` in the called method will be the contract itself. Therefore it doesn’t matter what sender actually called your tok method.

Edit:

Tgis behavior is for example mentioned in this section of the solidity docs: [Contracts — Solidity 0.8.10 documentation](https://docs.soliditylang.org/en/v0.8.10/contracts.html#getter-functions)

---

**JosephF** (2021-11-24):

Thank you a millions times [@rmeissner](/u/rmeissner) You are absolutely right. The “this” keyword was messing up everything. After removing it, everything works as expected and unauthorised accounts are no longer able to call the transfer function. Regarding posting this post on this Forum, I had actually reported the issue on the OpenZeppeling Forum, but they were the ones who had actually suggested me to bring it up here (perhaps because of a potential vulnerability). Again, thank you very, very much and have a wonderful day!


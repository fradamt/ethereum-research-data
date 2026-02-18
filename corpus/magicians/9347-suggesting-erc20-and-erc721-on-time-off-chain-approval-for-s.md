---
source: magicians
topic_id: 9347
title: Suggesting ERC20 and ERC721 on-time off-chain approval for safer NFT trading
author: themez
date: "2022-05-23"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/suggesting-erc20-and-erc721-on-time-off-chain-approval-for-safer-nft-trading/9347
views: 965
likes: 0
posts_count: 2
---

# Suggesting ERC20 and ERC721 on-time off-chain approval for safer NFT trading

Currently, mainstream NFT trading markets utilize the approve function to take control of users’ assets for order matching.

To save gas, trading markets request users to approve the max amount of ERC20 tokens and all ERC721 tokens, so users don’t need to approve each trade repeatedly. But this leaves a tremendous potential security threat: if the market contract is compromised, all users’ assets could be stolen.

So I want to discuss a more secure way of trading, learning from main trading markets’ offline listing and bidding mechanisms. We could store users’ one-time approval off-chain and make them expirable.

### Extensions of token protocol

Add extension function to ERC20:

```solidity
transferFromWithAuthority(address from, address to, uint256 amount, uint256 nonce, uint256 expiration, bytes signature)
```

Add extension function to ERC721:

```solidity
function transferFromWithAuthority(address from, address to, uint256 tokenId, uint256 nonce, uint256 expiration, bytes signature)
```

### Process of listing ERC721 token

1. sign for approving ERC721 token

```typescript
signer._signTypedData(
    domain,
    {
      Approve: [
        { name: 'tokenId', type: 'uint256' },
        { name: 'operator', type: 'address' },
        { name: 'expiration', type: 'uint256' },
        { name: 'nonce', type: 'uint256' },
      ],
    },
    {
      tokenId: 1,
      operator: '0x0000000000000000000000000000000000000000',
      expiration: 1653868800,
      nonce: 1234567 // a random number, signature can only be used once
    }
  )

```

1. sign for the market order
2. order taker executing market contract

```solidity
function atomicMatch(Order order, bytes orderSignature, uint256 authorityNonce, uint256 authorityExpiration, bytes nftAuthoritySignature) public payable {
    require(validateOrder(order, orderSignature), 'Invalid order');
    require(msg.value == order.amount, 'No enough value');
    ERC721(order.itemAddress).transferFromWithAuthority(order.from, order.to, order.tokenId, authorityNonce, authorityExpiration, nftAuthoritySignature);
    payable(order.maker).transfer(order.amount);
}
```

The marketplace then needs to store two signatures off-chain,  one more comparing the mainstream market like the opensea. It seems there’s no way to sign only once for two contracts to operate.

### Process of biding using ERC20 token

1. sign for approving ERC20 token

```typescript
  signer._signTypedData(
    domain,
    {
      Approve: [
        { name: 'spender', type: 'address' },
        { name: 'amount', type: 'uint256' },
        { name: 'expiration', type: 'uint256' },
        { name: 'nonce', type: 'uint256'},
      ],
    },
    {
      spender: '0x0000000000000000000000000000000000000000',
      amount: 1000000000000000000,
      expiration: 1653868800,
      nonce: 1234567, // a random number, signature can only be used once
    }
  )
```

1. sign for the market order
2. owner takes the bidding

```solidity
function atomicMatch(
    Order order, bytes orderSignature,
    uint256 erc20AuthorityNonce, uint256 erc20AuthorityExpiration,  bytes erc20AuthoritySignature,
    uint256 erc721AuthorityNonce, uint256 erc721AuthorityExpiration, bytes erc721AuthoritySignature) {
    require(validateOrder(order, orderSignature), 'Invalid order');
    ERC20(order.paymentTokenAddress).transferFromWithAuthority(order.from, order.to, order.amount, erc20AuthorityNonce, erc20AuthorityExpiration, erc20AuthoritySignature);
    ERC721(order.itemAddress).transferFromWithAuthority(order.from, order.to, order.tokenId, erc721AuthorityNonce, erc721AuthorityExpiration, erc721AuthoritySignature);
}
```

## Replies

**xinbenlv** (2022-11-17):

Just to clarify, in the subject “on-time” do you mean “on*e*-time”?

For the context, there are a few approval related EIPs. I am also working on a general approval EIP called [EIP-5453 Endorsement](https://eips.ethereum.org/EIPS/eip-5453),

that solves general limited time approval problem. Feel free to join its discussion [here](https://ethereum-magicians.org/t/erc-5453-endorsement-standard/10355)


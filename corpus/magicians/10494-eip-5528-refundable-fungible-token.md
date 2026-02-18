---
source: magicians
topic_id: 10494
title: "EIP-5528: Refundable Fungible Token"
author: StartfundInc
date: "2022-08-23"
category: EIPs
tags: [token, refundable-tokens]
url: https://ethereum-magicians.org/t/eip-5528-refundable-fungible-token/10494
views: 7621
likes: 45
posts_count: 120
---

# EIP-5528: Refundable Fungible Token

pull request: https://github.com/ethereum/EIPs/pull/5528

## Abstract

This standard is an extension of EIP-20. This specification provides a type of escrow service in the blockchain ecosystem, which includes the following capabilities.

- The seller issues tokens.
- The seller creates an escrow smart contract with detailed escrow information. The information could include seller token contract address, buyer token contract address,  lock period, exchange rate, the maximum number of buyers, minimum balance of buyers, additional escrow success conditions, etc.
- The seller funds seller tokens to the escrow contract.
- Buyers fund buyer tokens which are pre-defined in the escrow contract.
- When the escrow status meets success, the seller can withdraw buyer tokens, and buyers can withdraw seller tokens based on exchange rates.
- Buyers can withdraw (or refund) their funded token if the escrow process is failed or is in the middle of the escrow process.

## Motivation

Due to the nature of cryptocurrencies that guarantee anonymity, there is no way to get it back to the cryptocurrency that has already been paid.

To solve this problem, the Escrow service exists in the real world. However, it is challenging to implement an escrow service coordinated by a third-party arbitrator in a decentralized cryptocurrency ecosystem. To solve this, a smart contract was designed that acts as an escrow and devised a function where each token is sent back to the original wallet if the escrow is not completed.

Escrow smart contract service should support refund EIP-20 tokens in the middle of the escrow process or when the operation fails.

## Specification

There are two types of contract for the escrow process:

- Payable Contract: The sellers and buyers use this token to fund the Escrow Contract.
- Escrow Contract: Defines the escrow policies and holds Payable Contract’s token for a certain period.

This standard proposes interfaces on top of the EIP-20 standard.

### Methods

#### constructor

The `Escrow Contract` may define the following policies:

- MUST include seller token contract address
- MUST include buyer token contract address
- Escrow period
- Maximum (or minimum) number of investors
- Maximum (or minimum) number of tokens to fund
- Exchange rates of seller/buyer token
- KYC verification of users

#### escrowFund

Funds `_value` amount of tokens to address `_to`.

In the case of `Escrow Contract`:

- _to MUST be the user address.
- msg.sender MUST be the payable contract address.
- MUST check policy validations.

In the case of `Payable Contract`:

- The address _to MUST be the escrow contract address.
- MUST call EIP-20’s _transfer likely function.
- Before calling _transfer function, MUST call the same function of the escrow contract interface. The parameter _to MUST be msg.sender to recognize the user address in the escrow contract.

```solidity
function escrowFund(address _to, uint256 _value) public returns (bool)
```

#### escrowRefund

Refunds `_value` amount of tokens from address `_from`.

In the case of `Escrow Contract`:

- _from MUST be the user address.
- msg.sender MUST be the payable contract address.
- MUST check policy validations.

In the case of `Payable Contract`:

- The address _from MUST be the escrow contract address.
- MUST call EIP-20’s _transfer likely function.
- Before calling _transfer function, MUST call the same function of the escrow contract interface. The parameter _from MUST be msg.sender to recognize the user address in the escrow contract.

```solidity
function escrowRefund(address _from, uint256 _value) public returns (bool)
```

#### escrowWithdraw

Withdraws funds from the escrow account.

In the case of `Escrow Contract`:

- MUST check the escrow process is completed.
- MUST send the remaining balance of seller and buyer tokens to msg.sender’s seller and buyer contract wallets.

In the case of `Payable Contract`, it is optional.

```solidity
function escrowWithdraw() public returns (bool)
```

### Example of interface

```solidity
pragma solidity ^0.4.20;

interface IERC5528 is ERC20 {

    function escrowFund(address _to, uint256 _value) public returns (bool);

    function escrowRefund(address to, uint256 amount) public returns (bool);

    function escrowWithdraw() public returns (bool);

}

```

## Rationale

The interfaces described in this EIP have been chosen to cover the refundable issue in the escrow operation.

The suggested 3 functions (`escrowFund`, `escrowRefund` and `escrowWithdraw`) are based on `transfer` function in EIP-20.

`escrowFund` send tokens to the escrow contract. The escrow contract can hold the contract in the escrow process or reject tokens if the policy does not meet.

`escrowRefund` can be invoked in the middle of the escrow process or when the escrow process is failed.

`escrowWithdraw` allows users (sellers and buyers) to transfer tokens from the escrow account. When the escrow process is completed, the seller can get the buyer’s token, and the buyers can get the seller’s token.

## Backwards Compatibility

This EIP is fully backward compatible with the EIP-20 specification.

## Security Considerations

Since the escrow contract controls seller and buyer rights, flaws within the escrow contract will directly lead to unexpected behavior and potential loss of funds.

## Replies

**AsianHub** (2022-08-30):

Unprecedented protocol, wow!

---

**AnnGrey** (2022-08-30):

As a young investor,students. I think the Escrow protocol is the best protection for my investment in Web3.

---

**bhuvi4u** (2022-08-30):

Wow…some useful token for nullifying our losses and for easy refunds

---

**UCLpower001** (2022-08-30):

EIP-5528 is the most fascinating innovation I have seen in my years of been in the Cryptocurrency space.Cybercriminals are now taking advantage of the ongoing craze around cryptocurrencies to trick potential victims and steal their digital money. In a recent report, research firm Chainalysis revealed that scammers steals over $7.7 billion ( Rs 58,698 crore approx.) worth of cryptocurrency from victims in 2021. you could see why the EIP-5528 is certainly what investor’s like me need inorder to actualize ROI and not be a victim.

Creativity is a free bird which cannot but to keep flying in the sky. Realtize Creativity is a common language and Ultimate joyful goal. Cheers to a better tommorow where investor’s  can invest their funds and be rest assured that there funds are safe.

---

**Hugo** (2022-08-30):

Good proposal!

Looking forward to seeing EIP5528 will be adopted by Ethereum official soon

---

**cryptoccc** (2022-08-30):

Really great I really like this

---

**vancepang** (2022-08-30):

Hey! Good proposal.

I am looking forward to seeing this proposal passed as soon as possible to protect web3 investors as soon as possible.

---

**ninjoy** (2022-08-30):

Wow!So great!I think I really need this!

---

**skyetang** (2022-08-30):

cool! to the moon ![:crescent_moon:](https://ethereum-magicians.org/images/emoji/twitter/crescent_moon.png?v=12)![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12)![:crescent_moon:](https://ethereum-magicians.org/images/emoji/twitter/crescent_moon.png?v=12)![:crescent_moon:](https://ethereum-magicians.org/images/emoji/twitter/crescent_moon.png?v=12)![:crescent_moon:](https://ethereum-magicians.org/images/emoji/twitter/crescent_moon.png?v=12)

#EIP-5528

---

**Hadeezah** (2022-08-30):

Wow! This really is a beauty. To see projects like this develop so fast on the blockchain. One can only imagine the security that will be enjoyed in the future.

---

**AnnGrey** (2022-09-01):

Should use in the crypto world as soon as possible

---

**bhuvi4u** (2022-09-01):

somuch security to our investmentments, with the help of this token losses are so low…this is Awesome ![:smiling_face_with_three_hearts:](https://ethereum-magicians.org/images/emoji/twitter/smiling_face_with_three_hearts.png?v=12)![:smiling_face_with_three_hearts:](https://ethereum-magicians.org/images/emoji/twitter/smiling_face_with_three_hearts.png?v=12)

---

**Ezedaniel** (2022-09-01):

An escrow system which essentially assures investors of safety irrespective of the future changes that may hit a project, is a most welcome idea. i am in full support.

We can push crypto mainstream further by properly marketing these innovative concept

---

**Francis8926** (2022-09-01):

Wow impressive…great development by management…kudos to teams​:+1:If i must confess am plsd to see ds happen…sky is d limit​:ok_hand:t4:![:hugs:](https://ethereum-magicians.org/images/emoji/twitter/hugs.png?v=12)

---

**UCLpower001** (2022-09-01):

As1.7 billion adults remain unbanked, digital currencies offer an opportunity for millions of people around the world to participate in the internet economy, especially for those who:

Their native countries’ weak or unfair financial policies have barred them from membership.

Due to their distrust of banks.

They lack the funds to open a bank account.

They reside in rural areas without access to financial services.

They lack the legal documentation necessary to open a bank account.

Thanks to Realtize EIP-5528 that is transforming the future of finance and global transactions with a cutting-edge wallet combined with a trusted Agent Network. that allows for quick payments, and on/off ramp solutions designed to enable financial.

---

**Sly10** (2022-09-01):

Everyday we see New innovations on the blockchain space. However, this Escrow system is definitely standing out to be among the best idea ever. Investors will be rest assured about their transactions. Nice one realtize.

---

**Deejay007** (2022-09-01):

For me the ERC5528 standard is definitely a revolutionary move by Realtize, considering the level at which super frauds are hiking up.This escrow system has definitely been long awaited, big ups to the team!!!

---

**Hadeezah** (2022-09-02):

Give it a couple more years, the blockchain might be run at par with traditional banking activities. If things like refunds can be incorporated, it shows learning on the blockchain. And technologies that learn do stick around.

---

**AnnGrey** (2022-09-06):

Securities fundraising in the digital space

---

**joudand** (2022-09-06):

こんな素晴らしいプロトコルがあっていいなぁ、早く見たいです


*(99 more replies not shown)*

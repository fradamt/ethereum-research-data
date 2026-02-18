---
source: magicians
topic_id: 8900
title: "EIP Idea: Token with Joint Accounts"
author: dg314
date: "2022-04-11"
category: EIPs
tags: [token]
url: https://ethereum-magicians.org/t/eip-idea-token-with-joint-accounts/8900
views: 577
likes: 0
posts_count: 3
---

# EIP Idea: Token with Joint Accounts

# EIP-xxxx: Token with Joint Accounts

Ethereum Improvement Proposal for an ERC-20 token with joint accounts.

## Motivation

Cryptocurrency has the potential to replace traditional payment methods, but ERC-20 tokens are still lacking a key feature offered by banks: **joint accounts**.

A joint bank account allows two or more people to deposit, withdraw, and transfer money from the same balance. Business partners and married couples alike rely on joint bank accounts to simultaneously access the same pool of money. An individual may even have access to multiple joint bank accounts at once.

Currently, a user must distribute their private key to share access to their ERC-20 balance without transferring it. Additionally, a single address cannot control distinct balances shared with different groups. ERC-xxxx extends the ERC-20 standard to implement a system of joint accounts that solves both of these problems.

## Overview

- ERC-xxxx is backward compatible with ERC-20.
- A user can share access to their address’s balance with any number of other addresses.
- A user can revoke access to their address’s balance from another address at any time.
- A user can have access to any positive number of balances.
- A user always has access to their own balance.
- A user can set their active balance holder to their own address or any address that they have balance access to.

A user’s active balance holder is their own address by default.

The balance and allowance of a user is displayed from the perspective of their active balance holder.

- This allows users to easily view balances and allowances of joint accounts in ERC-20 compatible platforms like MetaMask.

A group of users can create another address to serve as their joint account.

## Implementation

The following is a working version of the interface for an ERC-20 token with joint accounts.

```auto
/**
 * Interface for an ERC-20 token with joint accounts.
 */
interface IERC20JointAccounts is IERC20, IERC20Metadata {
    /**
     * @dev Emitted when `balanceHolder` shares balance access to `account`.
     */
    event BalanceAccessShared(address indexed balanceHolder, address indexed account);

    /**
     * @dev Emitted when `balanceHolder` revokes balance access from `account`.
     */
    event BalanceAccessRevoked(address indexed balanceHolder, address indexed account);

    /**
     * @dev Emitted when `account` updates its active balance holder to
     * `activeBalanceHolder`.
     */
    event ActiveBalanceHolderUpdated(address indexed account, address indexed activeBalanceHolder);

    /**
     * @dev Shares `account` access to caller's balance.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * Emits a {BalanceAccessShared} event.
     *
     * Requirements:
     *
     * - `account` must not be caller.
     * - `account` must not currently have access to callers's balance.
     */
    function shareBalanceAccess(address account) external returns (bool);

    /**
     * @dev Revokes `account`'s access to caller's balance.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * Emits a {BalanceAccessRevoked} event.
     * May emit an {ActiveBalanceHolderUpdated} event.
     *
     * Requirements:
     *
     * - `account` must not be caller.
     * - `account` must currently have access to callers's balance.
     */
    function revokeBalanceAccess(address account) external returns (bool);

    /**
     * @dev Returns a boolean value indicating whether `account` has
     * access to `balanceHolder`'s balance.
     */
    function hasBalanceAccess(address account, address balanceHolder) external view returns (bool);

    /**
     * @dev Returns the active balance holder of `account`.
     */
    function activeBalanceHolderOf(address account) external view returns (address);

    /**
     * @dev Sets the active balance holder of the sender to `account`.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * Emits an {ActiveBalanceHolderUpdated} event.
     *
     * Requirements:
     *
     * - Caller must currently have access to `account`'s balance.
     */
    function setActiveBalanceHolder(address account) external returns (bool);

    /**
     * @dev Balance of `account`. Directly uses addresses.
     */
    function addressBalanceOf(address account) external view returns (uint256);

    /**
     * @dev Allowance given to `spender` by `owner`. Directly uses addresses.
     */
    function addressAllowance(address owner, address spender) external view returns (uint256);
}
```

See https://github.com/dg314/eip-joint-accounts for a complete implementation.

## Feedback

Is this a valid EIP idea worth pursuing? Any feedback is greatly appreciated!

## Replies

**wjmelements** (2022-04-13):

I don’t see much value here. Can use ERC20 transfer to set primary owner, and ERC20 approve to enable balance access.

But even better: a smart contract with multiple owners can own your tokens. This can work without any change to existing tokens. The biggest problem with your idea here is that tokens would have to opt-in to using it. You cite Metamask, which has plugin support for categories of multisig contracts.

---

**davidc** (2022-04-18):

I agree with [@wjmelements](/u/wjmelements)

In addition, even if this EIP was implemented, I’d imagine people would start sharing their addresses with smart contract addresses rather than user addresses, and so now it is just unnecessarily more complicated than giving ownership of the token to a smart contract directly.

One may argue that it’s less risky to have this baked into the token directly rather than having to implement logic in a separate smart contract that would have to be able to give users the ability to take their tokens back from the contract. However, a standard interface and implementation could just as easily develop for such a smart contract instead. Also, different contracts with different use-cases can develop independently, without needing adoption from existing tokens. For example, such contracts may be able to work with multiple tokens at a time, or such contracts may have unique consensus mechanisms for moving funds.

Also, this would end up being similar to the approve function, but instead for an unlimited amount of tokens. It could start encouraging contracts to use this method instead of approve, which would be less secure.

It seems that this logic should not be the responsibility of the token contract, but rather of the holder of the token.


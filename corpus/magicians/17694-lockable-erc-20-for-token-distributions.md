---
source: magicians
topic_id: 17694
title: Lockable ERC-20 for token distributions?
author: sullof
date: "2023-12-27"
category: ERCs
tags: [token, erc20]
url: https://ethereum-magicians.org/t/lockable-erc-20-for-token-distributions/17694
views: 1936
likes: 5
posts_count: 10
---

# Lockable ERC-20 for token distributions?

**Introducing a Proposed ERC: Lockable ERC20 Token Management**

**Objective**: We aim to innovate the ERC20 token framework by integrating a feature that enables users to temporarily lock a portion of their token balance. This mechanism is designed to immobilize selected tokens for a set period, without necessitating their transfer to another entity. During this lock period, these tokens are rendered non-transferable and cannot be used in transactions.

**Use Cases**:

1. Reward Incentivization: Users can lock tokens to become eligible for rewards, adding a new dimension to token utility.
2. Vesting Mechanism: The system can be utilized to distribute tokens with vesting schedules, beneficial for investors, team members, and other stakeholders.

**Functionality**:

- Lock Mechanism: A trusted third-party service, upon user approval, can invoke a ‘lock’ function on the token contract. This function will specify the amount and duration of the lock.
- Contract Mapping: The contract will maintain a mapping to record these lock details, ensuring transparency and traceability.
- Balance Integrity: The total token balance of a user remains unchanged, but the locked amount becomes temporarily unusable.

**Transfers and Approvals**:

- Restricted Interactions: The contract, while processing transfers or approvals, will reference the lock mapping. It will disallow any interaction with the locked tokens, thereby safeguarding them.
- Unrestricted Access: Users retain complete freedom to transact with their remaining, unlocked balance.

**Benefits**:

1. Reward Schemes: This feature enables innovative reward schemes where users are incentivized to lock tokens without transferring custody.
2. Gas Efficiency: At the conclusion of the lock period, tokens are automatically unlocked, eliminating the need for manual ‘unstaking’ and thus reducing gas costs.

**Closing Thoughts**: This proposal aims to introduce a flexible yet secure way to manage token liquidity and utility. It could open new avenues for token usage while ensuring user control and reducing transactional overhead.

I’m eager to hear your thoughts and feedback on this initiative. Do you see potential in this approach? Any suggestions for improvement or concerns you might have?

**Notice that I rewrote the introduction to the thread because I realized that my first version was not very clear ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) You can see the previous version in the edit history**

## Replies

**xinbenlv** (2023-12-27):

Thanks [@sullof](/u/sullof), I think it would be useful, I am glad you are thinking of contributing a proposal on this use case.

That said, just FYI, there were many prior attempts in proposing lockables

Such as [ERC-1132: Extending ERC20 with token locking capability](https://eips.ethereum.org/EIPS/eip-1132)

Multiple competing Lockables of ERC-721

- ERC-5058: Lockable Non-Fungible Tokens
- ERC-5753: Lockable Extension for EIP-721
- ERC-7066: Lockable Extension for ERC-721

Maybe it’s a good time to think of how to consolidate the efforts and drive adoption?

I’d love to discuss it with you. Maybe in our next AllERCDevs

---

**sullof** (2023-12-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> That said, just FYI, there were many prior attempts in proposing lockables
>
>
> Such as ERC-1132: Extending ERC20 with token locking capability

Hey xinbenlv, thanks for pointing out ERC-1132. I hadn’t come across it before. Looks like it didn’t get much traction, probably because it’s too niche. I reckon standards should be straightforward and flexible enough for a bunch of different scenarios.

That said, ERC-1132 could be a solid starting point for something new. But we should chat about what we actually need in a standard like this and see if we can cook up something more general. Keen to hash this out more.

P.S. About ERC-721, there’s a whole mix of implementations out there. Some are official, others not so much, and they all seem to miss something. That’s why I’ve been working on ERC-6982, trying to create a common ground. I think the advanced ERCs should build on the simpler ones to make life easier for us devs.

---

**sullof** (2024-01-02):

I have an initial version of the interface I am implementing in a project. Does it sound general enough to make sense as a general standard?

```auto
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// @author Francesco Sullo

interface IERC20Lockable {
  /**
   * @dev Emitted when tokenId is locked
   */
  event Lock(address indexed account, uint256 amount, address indexed _locker, uint256 lockedUntil);

  /**
   * @dev Emitted when tokenId is unlocked, if the amount is unlocked before the expiration
   */
  event Unlock(address indexed account, uint256 amount, address indexed _locker);

  /**
   * @dev Lock the amount if msg.sender is owner or approved
   *   The locker MUST be owner of approved to lock the amount.
   *   If the locker has already locked some amount, the lockedUntil MUST be 0 and the amount added to the locked amount,
   *   without changing the existing lockedUntil. If, when adding to an existing lock the lockedUntil is not zero, it MUST revert.
   *
   *   To avoid forever locks, the contract should set a maximum lockedUntil, and the function MUST revert if the lockedUntil
   *   is greater than the maximum lockedUntil.
   */
  function lock(address locker, uint256 amount, uint256 lockedUntil) external;

  /**
   * @dev Unlocks the amount before the expiration. msg.sender MUST be a locker
   *   It MUST revert if the unlocking amount is not locked by the msg.sender.
   */
  function unlock(address account, uint256 amount, uint256 lockedUntil) external;

  /**
   * @dev Moves `amount` tokens from the caller's account to `to` and locks the amount
   *
   * Returns a boolean value indicating whether the operation succeeded.
   *
   * Emits a {Transfer} event.
   */
  function transferAndLock(address to, uint256 amount, uint256 lockedUntil) external;

  /**
   * @dev Moves `amount` tokens from `from` to `to` using the
   * allowance mechanism. `amount` is then deducted from the caller's
   * allowance. It also locks the amount.
   *
   * Returns a boolean value indicating whether the operation succeeded.
   *
   * Emits a {Transfer} event.
   */
  function transferFromAndLock(address from, address to, uint256 amount, uint256 lockedUntil) external;

  /**
   * @dev Unlocks `amount` and moves it from the caller's account to `to`
   *   msg.sender MUST be a locker.
   */
  function unlockAndTransfer(address to, uint256 amount, uint256 tokenUntil) external;

  /**
   * @dev It unlocks `amount` and moves it from `from` to `to` using the
   * allowance mechanism. `amount` is then deducted from the caller's
   * allowance.
   *
   *   msg.sender MUST be a locker.
   *
   * Returns a boolean value indicating whether the operation succeeded.
   *
   * Emits a {Transfer} event.
   */
  function unlockAndTransferFrom(address from, address to, uint256 amount, uint256 tokenUntil) external;

  /**
   * @dev Returns the available portion of the balance of account, i.e., the not-locked amount.
   */
  function availableBalanceOf(address account) external view returns (uint256);
}

```

---

**sullof** (2024-01-02):

Here is an implementation of that interface in an upgradeable contract:

```auto
// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

// @author Franncesco Sullo

import "@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

import "./IERC20Lockable.sol";

import {console} from "hardhat/console.sol";

contract ERC20Lockable is IERC20Lockable, Initializable, ERC20Upgradeable {
  error NotEnoughLockedAmount();
  error LockExpired();
  error LockNotFound();
  error TooManyLocks();
  error InsufficientAllowance();
  error LockTooLong();
  error MaxLockTimeCannotBeZero();

  struct LockedAmount {
    uint224 amount;
    uint32 lockedUntil;
  }

  struct Locker {
    address locker;
    uint32 locks;
  }

  mapping(address => mapping(address => LockedAmount[])) internal _locks;
  mapping(address => Locker[]) internal _lockers;
  uint256 public maxLockTime;

  function _beforeTokenTransfer(address from, address to, uint256 amount) internal virtual override {
    if (from == address(0)) return;
    if (_lockers[_msgSender()].length == 0) return;
    if (amount > _availableBalanceOfWhileCleaning(from)) revert InsufficientAllowance();
    super._beforeTokenTransfer(from, to, amount);
  }

  // solhint-disable-next-line
  function __ERC20Lockable_init(string memory name, string memory symbol, uint256 maxLockTime_) public initializer {
    __ERC20_init(name, symbol);
    _setMaxLockTime(maxLockTime_);
  }

  function _setMaxLockTime(uint256 maxLockTime_) internal {
    if (maxLockTime_ == 0) revert MaxLockTimeCannotBeZero();
    maxLockTime = maxLockTime_;
  }

  function lock(address account, uint256 amount, uint256 lockedUntil) public override {
    if (lockedUntil > block.timestamp + maxLockTime) revert LockTooLong();
    _spendAllowance(account, _msgSender(), amount);
    _lock(account, amount, _msgSender(), lockedUntil);
  }

  function _lock(address account, uint256 amount, address locker, uint256 lockedUntil) internal {
    if (_locks[locker][account].length > 10) {
      // to avoid gas issues during loops
      revert TooManyLocks();
    }
    _locks[locker][account].push(LockedAmount(uint224(amount), uint32(lockedUntil)));
    emit Lock(account, amount, locker, lockedUntil);
    for (uint256 i = 0; i  1) {
      _locks[locker][account][i] = _locks[locker][account][_locks[locker][account].length - 1];
      _locks[locker][account].pop();
    } else delete _locks[locker][account];
    _lockers[account][i] = _lockers[account][_lockers[account].length - 1];
    for (uint256 j = 0; j  1) _lockers[account][j].locks--;
        else {
          _lockers[account][j] = _lockers[account][_lockers[account].length - 1];
          _lockers[account].pop();
        }
        break;
      }
    }
  }

  function transferAndLock(address to, uint256 amount, uint256 lockedUntil) public override {
    transfer(to, amount);
    lock(to, amount, lockedUntil);
  }

  function transferFromAndLock(address from, address to, uint256 amount, uint256 lockedUntil) public override {
    transferFrom(from, to, amount);
    lock(to, amount, lockedUntil);
  }

  function unlockAndTransfer(address to, uint256 amount, uint256 tokenUntil) public override {
    unlock(_msgSender(), amount, tokenUntil);
    transfer(to, amount);
  }

  function unlockAndTransferFrom(address from, address to, uint256 amount, uint256 tokenUntil) public override {
    unlock(from, amount, tokenUntil);
    transferFrom(from, to, amount);
  }

  function availableBalanceOf(address account) public view override returns (uint256) {
    uint256 availableBalance = balanceOf(account);
    for (uint256 i = 0; i  block.timestamp) {
          availableBalance -= _locks[_lockers[account][i].locker][account][j].amount;
        }
      }
    }
    return availableBalance;
  }

  // Called before a transfer.
  // Reduces the gas consumption if any lock is expired
  function _availableBalanceOfWhileCleaning(address account) internal returns (uint256) {
    uint256 availableBalance = balanceOf(account);
    for (uint256 i = 0; i  block.timestamp) {
          availableBalance -= _locks[_lockers[account][i].locker][account][j].amount;
        } else {
          _deleteLock(account, _msgSender(), i);
        }
      }
    }
    return availableBalance;
  }

  uint256[50] private __gap;
}
```

Some of the operation are gas-intensive, but I am sure it is possible to find some better alternative to optimize the costs.

---

**sullof** (2024-01-05):

I have some concerns on my above Lockable ERC20 Implementation

The primary issue with it lies in its backward compatibility. Specifically, users who are unaware of the lockable feature might mistakenly rely on the `balanceOf` function to determine an account’s spendable balance. However, in our implementation, `balanceOf` reflects the total balance, which includes both locked and unlocked funds. This can be misleading as it doesn’t accurately represent the amount available for immediate transactions.

A potential solution could be to modify the `balanceOf` function so that it returns only the unlocked balance, ensuring that it reflects the spendable amount. Additionally, we could introduce a new function, `fullBalanceOf`, to report the total balance, combining both locked and unlocked funds.

However, this approach has a significant obstacle. In the OpenZeppelin ERC20 contracts, the `_balances` variable is private, meaning that any modification to accurately track and separate locked and unlocked balances would require a deep alteration of the OpenZeppelin codebase. This would involve either cloning and modifying the OpenZeppelin contract at a fundamental level or finding an alternative method to implement this feature.

We are left with two options:

1. An easy-to-implement interface with an availableBalanceOf function, which explicitly indicates the unlocked, spendable balance.
2. A more backward-compatible version with a fullBalanceOf function, providing a comprehensive view of an account’s total funds, both locked and unlocked.

We are evaluating these options to balance ease of implementation with backward compatibility and user clarity.

PS > In the second version, the added function may also be `lockedBalanceOf`, where the full balance is the sum of balanceOf(…) + lockedBalanceOf(…);

**Any insights or thoughts on the best path forward would be greatly appreciated.**

---

**hantosy** (2024-03-20):

Hello!

I get error :

> Blockquote
> ypeError: Function has override specified but does not override anything.
>  → ERC20Lockable.sol:36:92:
> |
> 36 |   function _beforeTokenTransfer(address from, address to, uint256 amount) internal virtual override {

> Blockquote
> I copy all your code. How should I fix it?
> Thanks you

---

**sullof** (2024-03-21):

I suspect you are using OpenZeppelin v5, which has replaces _beforeTokenTransfer with _update.

---

**lfsmoura** (2024-03-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sullof/48/3709_2.png) sullof:

> indexed amount

That’s a really interesting proposal and as [@xinbenlv](/u/xinbenlv) commented, it’s really relevant.

Why are you adding indexed to the amount parameter? wouldn’t that add extra gas cost? how that event would be used?

---

**sullof** (2024-03-25):

That is a mistake. Good catch.

Consider that the example above is a quick and dirty one, with no optimization, just to show how it may work.

I fixed it, thanks.


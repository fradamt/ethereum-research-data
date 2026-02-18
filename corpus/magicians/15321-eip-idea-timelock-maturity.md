---
source: magicians
topic_id: 15321
title: "EIP Idea: Timelock Maturity"
author: ekkila
date: "2023-08-01"
category: EIPs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/eip-idea-timelock-maturity/15321
views: 1869
likes: 3
posts_count: 5
---

# EIP Idea: Timelock Maturity

This EIP defines a standardized method to communicate the date on which a time-locked system will become unlocked. This allows for the determination of maturities for a wide variety of asset classes and increases the ease with which these assets may be valued.

Time-locks are ubiquitous, yet no standard on how to determine the date upon which they unlock exists. Time-locked assets experience theta-decay, where the time remaining until they become unlocked dictates their value. Providing a universal standard to view what date they mature on allows for improved on-chain valuations of the rights to these illiquid assets, particularly useful in cases where the rights to these illiquid assets may be passed between owners through semi-liquid assets such as ERC-721s or ERC-1155s.

```solidity
// SPDX-License-Identifier: CC0-1.0

pragma solidity ^0.8.0;

interface TimelockMaturity {
    /
     * @notice      This function returns the timestamp that the time lock specified by `id` unlocks at
     * @param       id The identifier which describes a specific time lock
     * @return      maturity The timestamp of the time lock when it unlocks
     */
    function getMaturity(bytes32 id)
        external
        view
        returns (uint256 maturity);

}
```

Locked Assets have become increasingly popular and used in different parts of defi, such as yield farming and vested escrow concept. This has increased the need to formalize and define an universal interface for all these timelocked assets.

Locked Assets cannot be valued normally since the value of these assets can be varied through time and many other different factors throughout the locking time. For instance, The Black-Scholes Model or Black-Scholes-Merton model is an example of a suitable model to estimate the theoritical value of asset with the consideration of impact of time and other potential risks. Time to maturity plays an important role in evaluating the price of timelocked assets, thus the demand to have a common interface for retrieving the data is inevitable.

### Reference Implementation

```solidity
// SPDX-License-Identifier: CC0-1.0

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract LockedERC20ExampleContract implements TimelockMaturity{
    ERC20 public immutable token;
    uint256 public totalLocked;

    //Timelock struct
    struct TimeLock {
        address owner;
        uint256 amount;
        uint256 maturity;
        bytes32 lockId;
    }

    //maps lockId to balance of the lock
    mapping(bytes32 => TimeLock) public idToLock;

    function constructor(
        address _token,
    ) public {
        token = ERC20(_token);
    }

    //Maturity is not appropriate
    error LockPeriodOngoing();
    error InvalidReceiver();
    error TransferFailed();

    /// @dev Deposit tokens to be locked in the requested locking period
    /// @param amount The amount of tokens to deposit
    /// @param lockingPeriod length of locking period for the tokens to be locked
    function deposit(uint256 amount, uint256 lockingPeriod) external returns (bytes32 lockId) {
        uint256 maturity = block.timestamp + lockingPeriod;
        lockId = keccack256(abi.encode(msg.sender, amount, maturity));

        require(idToLock[lockId].maturity == 0, "lock already exists");

        if (!token.transferFrom(msg.sender, address(this), amount)) {
            revert TransferFailed();
        }

        TimeLock memory newLock = TimeLock(msg.sender, amount, maturity, lockedId);

        totalLocked += amount;

        idToLock[lockId] = newLock;

    }

    /// @dev Withdraw tokens in the lock after the end of the locking period
    /// @param lockId id of the lock that user have deposited in
    function withdraw(bytes32 lockId) external {
        TimeLock memory lock = idToLock[lockId];

        if (msg.sender != lock.owner) {
            revert InvalidReceiver();
        }

        if (block.timestamp > lock.maturity) {
            revert LockPeriodOngoing();
        }

        totalLocked -= lock.amount;

        //State cleanup
        delete idToLock[lockId];

        if (!token.transfer(msg.sender, lock.amount)) {
            revert TransferFailed();
        }

    }

    function getMaturity(bytes32 id) external view returns (uint256 maturity) {
        return idToLock[id].maturity;
    }
}

```

## Replies

**Mani-T** (2023-08-07):

The concept of a standardized interface for time-locked assets holds promise in addressing valuation challenges and enhancing the efficiency and transparency of trading illiquid assets within the DeFi ecosystem. Careful attention to implementation details, security, and flexibility will be essential for its successful adoption and utilization.

---

**RobAnon** (2023-08-08):

Can hop in and say that future versions of Revest will implement this EIP.

---

**xhyumiracle** (2024-06-01):

Interesting. One question regarding this code snippet from the ref impl:

```solidity
        if (block.timestamp > lock.maturity) {
            revert LockPeriodOngoing();
        }
```

From my understanding, it seems should be `block.timestamp < lock.maturity`, rather than `>`.

Correct me if I misunderstood something.

---

**Web3Ling** (2024-06-03):

I believe a convenient time lock interface will be easier to use. It would also be beneficial to include a permission interface for upgrades, similar to upgradable contracts. Some dApps may need this feature, such as when a project updates the timelock following a DAO vote.


---
source: ethresearch
topic_id: 3106
title: EVM Compatible Transaction Fee(GAS) Delegated Execution Architecture for Plasma Chain
author: philosopher
date: "2018-08-27"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/evm-compatible-transaction-fee-gas-delegated-execution-architecture-for-plasma-chain/3106
views: 2839
likes: 6
posts_count: 5
---

# EVM Compatible Transaction Fee(GAS) Delegated Execution Architecture for Plasma Chain

# PoC1 : EVM Compatible Transaction Fee(GAS) Delegated Execution Architecture

Kevin Jeong([kevin.j@onther.io](mailto:kevin.j@onther.io), Onther Inc.)

Thomas Shin(Onther Inc.)

Jason Hwang(Onther Inc.)

Carl Park(Onther Inc.)

# Abstract

PoC1 is the transaction execution model which is competible with Ethereum Virtual Machine. The purpose of this project is to provide the transaction processing procedure, maintaining ethereum’s GAS system, delegates GAS from transactor to decentralized autonomous agent(smart contract) defined in blockchain.

In PoC1, we achieved an improvement from a simple structure, GAS and value(ETH) paid from only to transactor, to multiple structure the burden of fee is supported by “stamina contract” in a means of “Stamina”. Stamina is periodic-rechargable state variable and it’s comsumption is keep tracked and managed by blockchain rules.

As a result, users do not need to concern about the “keeping balance maintanance activities”. It also facilitates service provider to create a more user-friendly decentralized application(dApp). This will accelerate the emergence of killer apps, pushing to expand the decentralized ecosystem futher.

# 1. Introduction

## 1.1 Project Background and Purpose

Ethereum imposes fee on all computing operations to prevent unauthorized use of the network. This fee is calculated as a special unit called Gas and it is a [time-space cost](https://medium.com/onther-tech/plasma-mvp-audit-%EB%85%B9%EC%B7%A8%EB%A1%9D-script-166a2c5012b4)[2] on the Ethereum network.

The Ethereum blockchain avoids denial of service attacks through this commission model and solves the problem of distributing limited resource; ‘Right of state transitions in blockchain’. The important point is that the transactor always maintains a certain level of balance to generate the transaction paying the GAS Limit * GAS Price. Transactor sends a transaction “always” has to bear these costs. It extremely reduces the usability of DApps implemented on Ethereum blockchain.

In PoC1, we want to design an Execution Model which enhances the user experience. It is expected to provide a ground for user-friendly (accessibility / usability) application development environment.

## 1.2 Denotation and Grossary

The words defined in PoC1 are as follows(Some of denotations came from ETHEREUM: A SECURE DECENTRALISED GENERALISED TRANSACTION LEDGER[1]):

---

- ERC20: ERC20 is a smart contract technology standard for implementing tokens in the Ethereum blockchain.
- State balance: The balance recorded in the Ethereum State.
- Account: User identification unit in the Ethereum blockchain.
- NULL_ADDRESS: 0x00 or 0xFF...FF(2^160 - 1) with signature v = r = s = 0.
- Transactor: The account which sends transaction.
- Gas: Ethereum’s fee unit.
- Gas limit: the maximum gas consumption specified in transaction.
- Upfront cost: The cost to be charged before the EVM runs. It is calculated as value + gasLimit * gasPrice (Expenses that are charged before executing EVM.).
- Gas-upfront cost: Upfront cost - Value. Calculated as tx.gasLimit * tx.gasPrice.
- Value-upfront cost: Upfront cost - gas-upfront cost = value.
- Refunded gas: Gas Limit - the gas actually consumed by the EVM.
- Delegatee: An account that pays the transaction fee of another account in stamina contract.
- Delegator: An account that delegates the transaction fee to the delegatee in stamina contract.
- stamina pair: If delegatee designate delegator, they are pair. It is called .
- Stamina: State variable deposited to delegatee’s balance in stamina contract.
- Stamina Contract: A decentralized contract code containing procedures for handling delegated gas with stamina.
- Depositor account (depositor): An account who pours asset into the delegatee’s stamina bucket.
- Stamina deposit: An action of charging stamina to somebody’s account.
- Stamina withdraw: Removing charged stamina and filling other account balances accordingly.
- Stamina refund: Stamina refund is equals to refunded Gas in stamina contract.
- Stamina substract: An action of deducting delegatee’s stamina.
- Stamina recover: Refreshment of stamina.
- Stamina Epoch Length: It takes a certain period of time to recover stamina, which is called stamina epoch length.
- Epoch: Unit of stamina recovery cycle.

# 2. System Architecture

The system we design in this chapter is largely divided into two parts:

1. A contract dealing with the delegated gas costs
2. The procedure of transaction processing.

## 2.1 Delegated Gas Treatment

## 2.1.1 Stamina

The transaction fee of the delegator is purchased by the delegatee in the form of stamina, alleviating the delegator gas burden. A stamina can be obtained by depositing asset on a `stamina contract`, and an account that deposits the stamina of a delegatee is called a `depositor`.

The deduced stamina does not mean disappearing forever, but it will be recovered after a certain period of time. It is `stamina recover` in PoC1. The stamina requires a period of time to recover, and it is `recover epoch length`. Every epoch, stamina is newly charged as much as amount deposited.

The stamina balance expressed as follows:

[a]_{stm} \tag{1}

## 2.1.2 Stamina Pair

A delegator is denoted as D_{tor} and the delegatee as D_{tee}. The relationship between delegator and delegatee is defined as ST_{pair}F().

ST_{pair}F(D_{tor}) = D_{tee} \tag{2}

When the delegatee and the delegator satisfy the above equation, they become a `stamina pair`.

### 2.1.3 Stamina Contract

Stamina contract provides the following functions:

1. Designate delegator
2. Stamina Increase/Decrease
3. Stamina Refund/Substract/Recover

#### 2.1.3.1 Designate the Delegator

A delegatee can designate a delegator. Only a delegatee can designate, whereas a delegator can not. In addition, a delegatee can designate multiple delegators.

[![](https://ethresear.ch/uploads/default/original/2X/e/ef12be38e55e00eff1737fe653525ef684c96ab4.png)528×348 10.8 KB](https://ethresear.ch/uploads/default/ef12be38e55e00eff1737fe653525ef684c96ab4)

The delegatee calls stamina contract’s `setDelegator()` function to designate the delegator.

```solidity
function setDelegator(address delegator)
    external
    onlyInitialized
    returns (bool)
{
    address oldDelegatee = _delegatee[delegator];

    _delegatee[delegator] = msg.sender;

    emit DelegateeChanged(delegator, oldDelegatee, msg.sender);
    return true;
}
```

#### 2.1.3.2 Stamina Increase & Decrease

To increase the stamina, the depositor must call the `deposit()` function of the stamina contract.

For example, let’s assume account A, B exist. If account A calls `deposit()` function to add stamina of B, B’s stamina increased.

```solidity
function deposit(address delegatee)
    external
    payable
    onlyInitialized
    returns (bool)
  {
    require(msg.value >= MIN_DEPOSIT);

    uint totalDeposit = _total_deposit[delegatee];
    uint deposit = _deposit[msg.sender][delegatee];
    uint stamina = _stamina[delegatee];

    require(totalDeposit + msg.value > totalDeposit);
    require(deposit + msg.value > deposit);
    require(stamina + msg.value > stamina);

    _total_deposit[delegatee] = totalDeposit + msg.value;
    _deposit[msg.sender][delegatee] = deposit + msg.value;
    _stamina[delegatee] = stamina + msg.value;

    if (_last_recovery_block[delegatee] == 0) {
      _last_recovery_block[delegatee] = block.number;
    }

    emit Deposited(msg.sender, delegatee, msg.value);
    return true;
}
```

In contrast, stamina contract’s `requestWithdrawl()`, `withdraw()` function called to reduce the stamina of the delegatee. At this point stamina shrinks and depositor’s balance is increased as much as stamina reduced, accordingly.

In order for the depositor to withdraw, it goes through two steps:

1. Call the requestWithdrawl() function
: First, the depositor calls stamina contract’s requestWithdrawal() function. When it is called, the stamina of the delegatee is deducted by the requested amount, and this record remains in stamina contract.
2. Call the withdraw() function
: depositor can call the withdraw() function to withdraw the account balance as much as the stamina recorded in previous step.

```solidity
function requestWithdrawal(address delegatee, uint amount)
    external
    onlyInitialized
    returns (bool)
  {
    require(amount > 0);

    uint totalDeposit = _total_deposit[delegatee];
    uint deposit = _deposit[msg.sender][delegatee];
    uint stamina = _stamina[delegatee];

    require(deposit > 0);

    require(totalDeposit - amount  amount) {
      _stamina[delegatee] = stamina - amount;
    } else {
      _stamina[delegatee] = 0;
    }

    Withdrawal[] storage withdrawals = _withdrawal[msg.sender];

    uint withdrawalIndex = withdrawals.length;
    Withdrawal storage withdrawal = withdrawals[withdrawals.length++];

    withdrawal.amount = uint128(amount);
    withdrawal.requestBlockNumber = uint128(block.number);
    withdrawal.delegatee = delegatee;

    emit WithdrawalRequested(msg.sender, delegatee, amount, block.number, withdrawalIndex);
    return true;
}

function withdraw() external returns (bool) {
    Withdrawal[] storage withdrawals = _withdrawal[msg.sender];
    require(withdrawals.length > 0);

    uint lastWithdrawalIndex = _last_processed_withdrawal[msg.sender];
    uint withdrawalIndex;

    if (lastWithdrawalIndex == 0 && !withdrawals[0].processed) {
      withdrawalIndex = 0;
    } else if (lastWithdrawalIndex == 0) { // lastWithdrawalIndex == 0 && withdrawals[0].processed
      require(withdrawals.length >= 2);

      withdrawalIndex = 1;
    } else {
      withdrawalIndex = lastWithdrawalIndex + 1;
    }

    require(withdrawalIndex  stamina);
    uint targetBalance = stamina + amount;

    if (targetBalance > totalDeposit) _stamina[delegatee] = totalDeposit;
    else _stamina[delegatee] = targetBalance;

    return true;
}
```

The stamina of the delegatee will eventually be exhausted. But the depleted stamina can be recharged in the next epoch. It means the delegatee’s stamina is reusable.

Stamina recovery condition appears at the beginning of `addStamina()` function. If current epoch meets recovery condition, then total amount deposited will be regained.

```solidity
if (_last_recovery_block[delegatee] + RECOVER_EPOCH_LENGTH = value + gasLimit * gasPrice

    # 2. substract upfront cost(tx.value + tx.gasLimit * tx.gasPrice)
    substractBalance(from, balance - value - gasLimit * gasPrice)

    # 3. execute EVM
    executeVM(from, to, value, gasLimit, gasPrice, data)

    # 4. collect refunded gas
    addBalance(from, gasRemained * gasPrice)

def tx_delegated_execute(from, to, value, gasLimit, gasPrice, data) :
    # 0. check if (delegator, delegatee) pair exists. execute EVM.
    # getDelegatee() returns
    # or it returns
    delegatee = staminaContract.getDelegateeAddress(from)

    # 1. case where delegatee exist
    # Check, if `to` has delegatee check upfront cost(only gasLimit * gasPrice)
    if delegatee and staminaContract.balanceOf(delegatee) >= gasLimit * gasPrice:
        # 1-1. check if `from` can pay upfront cost(only value)
        assert getBalance(from) >= value

        # 1-2. subtract upfront cost(only gasLimit * gasPrice) from delegatee
        staminaContract.subtractBalance(delegatee, gasLimit * gasPrice)

        # 1-3. substract upfront cost(only value)
        substractBalance(from, value)

        # 1-4. execute EVM
        executeVM(from, to, value, gasLimit, gasPrice, data)

        # 1-5. collect refunded gas to delegatee
        staminaContract.addBalance(delegatee, gasRemained * gasPrice)

    # 2. case where delegatee does not exist
    else:
        # Execute tx tranditional way
        tx_traditional_execute(from, to, value, gasLimit, gasPrice, data)
```

### 2.2.5 Compare with Ethereum

|  | Traditional Ethereum | Delegated Model | Remarks |
| --- | --- | --- | --- |
| Account to buy upfront cost | transactor | transactor or delegatee |  |
| Account to buy gas-upfront | transactor | transactor or delegatee |  |
| Account to buy value-upfront | transactor | transactor |  |
| Minimum EVM Execution | 1 | 3 |  |

# 3. Implementation

## 3.1 Implement go-ethereum, py-evm

Link : [PoC1 : 구현(Implementation) - HackMD](https://hackmd.io/s/HJrS5IxIm) (Korean)

# 4. Conclusion

In PoC 1: EVM Compatible Gas In the Delegated Transaction Execution Model, we proposed an execution model to solve the usability problem, so that users do not have to worry about transaction fees. And this model also endures network attacks such as DoS.

The main feature of PoC1 is the delegation of transaction fees between stamina pair’s accounts. To delegate commission, PoC1 added a new concept “Stamina”. Once the stamina runs out, delegator can pay for the transaction fee on their own state balance. And it can still prevent any network attacks, because regardless of commission type, weather is stamina or balance, fees are charged for every transaction. Also, the delegatee can prevent the malicious delegator from consuming the stamina by releasing the pair designation when delegatee detects an abnormal behavior. If there is a dapp running on this model for a specific purpose, the service provider will have a number of delegatee and set the service users as delegator. Dapp’s initial users don’t have to worry about the transaction fee. This suggests that the proposed model of PoC1 is much more usable than the traditional execution model of Ethereum.

As we have seen in the `2.2.5 Comparison with the existing Ethereum execution model`, this model runs EVM at least three times per transaction, so if it is applied to mainnet, it becomes slower than before. Therefore, it is more suitable to use in private chain or sidechain. In order to solve this issue, we will discuss in [PoC2: Plasma EVM](https://hackmd.io/s/HyZ2ms8EX) on how to use the proposed architecture applied in sidechain.

# Reference

[1] [ETHEREUM: A SECURE DECENTRALISED GENERALISED TRANSACTION LEDGER BYZANTIUM VERSION e94ebda - 2018-06-05](https://ethereum.github.io/yellowpaper/paper.pdf)

[2] [Plasma MVP Audit Transacript (Script)](https://medium.com/onther-tech/plasma-mvp-audit-%EB%85%B9%EC%B7%A8%EB%A1%9D-script-166a2c5012b4)

## Replies

**MihailoBjelic** (2018-09-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/philosopher/48/2005_2.png) philosopher:

> 2.2.5 Compare with Ethereum

Can you please elaborate this section?

---

**philosopher** (2018-09-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/philosopher/48/2005_2.png) philosopher:

> 2.2.4 Pseudo-code

This section explains all.

The traditional execution model, execute VM only once.

But this model execute at least three times,

1. delegatee = staminaContract.getDelegateeAddress(from)
2. staminaContract.balanceOf(delegatee)
3. executeVM(from, to, value, gasLimit, gasPrice, data)

---

**MihailoBjelic** (2018-09-03):

Oh, I see. It’s not that the actual transaction is executed 3x, but you have 2 additional EVM operations (no. 1 and 2 in your explanation) besides the execution of the actual transaction (no. 3).

---

**philosopher** (2018-09-03):

Exactly. It delegates fee to another smart contracts’ state variable.


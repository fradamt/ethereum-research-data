---
source: magicians
topic_id: 11125
title: EIP for Smart Contract Wallet Standard
author: Eth
date: "2022-09-30"
category: EIPs
tags: [wallet, eip]
url: https://ethereum-magicians.org/t/eip-for-smart-contract-wallet-standard/11125
views: 1105
likes: 0
posts_count: 1
---

# EIP for Smart Contract Wallet Standard

# Abstract

The following describes standard functions a wallet contract can implement.

# Motivation

Those will allow dapps and wallets to handle tokens across multiple interfaces/dapps/eoa.

The most important here are, `transfer`, ‘transferOwnership’,`balanceOf` , `approve` and the `Transfer`event,the ‘approve’ event.

# Specification

## Wallet

### Methods

**NOTE**: An important point is that callers should handle `false` from `returns (bool success)`. Callers should not assume that `false` is never returned!

#### balanceOf

function balanceOf(address _token) constant returns (uint256 balance)

Get the account balance of token address `_token`

#### balanceOf

function balanceOf() constant returns (uint256 balance)

Get the account balance of ETH

#### transfer

function transfer(address _to, uint256 _value,address _token) returns (bool success)

Send `_value` amount of tokens to address `_to` with token address ‘_token’

#### transferFrom

function transferFrom(address _from, address _to, uint256 _value,address _token) returns (bool success)

Send `_value` amount of tokens from address `_from` to address `_to`

The `transferFrom` method is used for a withdraw workflow, allowing contracts to send tokens on your behalf, for example to “deposit” to a contract address and/or to charge fees in sub-currencies; the command should fail unless the `_from` account has deliberately authorized the sender of the message via some mechanism; we propose these standardized APIs for approval:

#### approve

function approve(address _spender, uint256 _value,address _token) returns (bool success)

Allow _spender to withdraw from your account, multiple times, up to the _value amount. If this function is called again it overwrites the current allowance with _value.

#### transferOwnership

function transferOwnership(address _owner) constant returns (bool success)

transfer wallet ownership,called by owner only normally,called by guardian when all guardians report wallet lost and owner can revoke it.

#### guardian

function guardian(address _guardian) constant returns (bool success)

set wallet guardian,called by owner only.

####lost

function lost() constant returns (bool success)

report wallet lost when owner disabled,called by guardian only.

### Events

#### Transfer

event Transfer(address indexed _from, address indexed _to, uint256 _value)

Triggered when token/eth are transferred.

#### Approval

event Approval(address indexed _owner, address indexed _spender, uint256 _value,address _token)

Triggered whenever `approve(address _spender, uint256 _value,address _token)` is called.

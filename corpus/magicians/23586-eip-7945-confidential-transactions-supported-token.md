---
source: magicians
topic_id: 23586
title: "EIP 7945: Confidential Transactions Supported Token"
author: andrewcheng
date: "2025-04-17"
category: ERCs
tags: [erc, token, privacy]
url: https://ethereum-magicians.org/t/eip-7945-confidential-transactions-supported-token/23586
views: 403
likes: 5
posts_count: 5
---

# EIP 7945: Confidential Transactions Supported Token

Proposed by Ant International: https://www.ant-intl.com/en/

[![antintl-logo](https://ethereum-magicians.org/uploads/default/optimized/2X/5/556b753a8c7cec1fcf67791c013aedd68f9aa6dc_2_690x284.png)antintl-logo1342×554 174 KB](https://ethereum-magicians.org/uploads/default/556b753a8c7cec1fcf67791c013aedd68f9aa6dc)

## Abstract

This proposal draws up a standard interface of confidential transaction supported token contracts, by providing basic funcationality without loss of generality. Contracts following the standard can provide confidentiality for users’ balances and token transfer value.

## Motivation

A standard interface allows confidential transactions of tokens on Ethereum (and/or other EVM-compatible blockchains) to be applied by certain parties which are sensitive to transfer amount, or by privacy-preserving applications.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Contract Interface

#### Methods

##### name

Returns the name of the token - e.g. `"MyConfidentialToken"` .

OPTIONAL - This method can be used to improve usability, but interfaces and other contracts MUST NOT expect these values to be present.

```auto
function name() public view returns (string)
```

##### symbol

Returns the symbol of the token. e.g. `"cHIX"` .

OPTIONAL - This method can be used to improve usability, but interfaces and other contracts MUST NOT expect these values to be present.

```auto
function symbol() public view returns (string)
```

##### decimals

Returns the number of decimals the token uses - e.g. `8` , means to divide the token amount by `100000000` to get its user representation.

OPTIONAL - This method can be used to improve usability, but interfaces and other contracts MUST NOT expect these values to be present.

```auto
function decimals() public view returns (uint8)
```

##### confidentialBalanceOf

Returns the account confidential balance of another account with address `owner` .

```auto
function confidentialBalanceOf(address owner)
public view returns (bytes memory confidentialBalance)
```

##### confidentialTransfer

Transfers `value` amount of tokens (behind `_confidentialTransferValue` ) to address `_to` , and MUST fire the `ConfidentialTransfer` event. The function SHOULD `throw` if the message caller’s `_proof` of this transfer fails to be verified.

Note:

- Callers MUST handle false from returns (bool success). Callers MUST NOT assume that false is never returned!
- Implementations can fully customize the proof system, (de)serialization strategies of bytes and/or the bussiness workflow. For example, when implementing “Zether” (see Zether: Towards Privacy in a Smart Contract World | Springer Nature Link (formerly SpringerLink) ) confidential token contracts, the _confidentialTransferValue and accounts’ confidential balances will be encrypted homomorphically under ElGamal public keys, and _proof will consist 3 parts to check:

_confidentialTransferValue is well encrypted under both caller’s public key and _to 's;
- The plaintext value behind _confidentialTransferValue is non-negative;
- The caller’s confidential balance is actually enough to pay the plaintext value behind _confidentialTransferValue .

```auto
function confidentialTransfer(
  address _to,
  bytes memory _confidentialTransferValue,
  bytes memory _proof
) public returns (bool success)
```

##### confidentialTransferFrom

Transfers `value` amount of tokens (behind `_confidentialTransferValue` ) from address `_from` to address `_to` , and MUST fire the `ConfidentialTransfer` event.

The `confidentialTransferFrom` method is used for a withdraw workflow, allowing contracts to transfer tokens on your behalf. This can be used for example to allow a contract to transfer tokens on your behalf and/or to charge fees in sub-currencies. The function SHOULD `throw` unless the `_from` account has deliberately authorized the sender of the message via some mechanism, and SHOULD `throw` if the message caller’s `_proof` of this transfer fails to be verified.

Note:

- Callers MUST handle false from returns (bool success). Callers MUST NOT assume that false is never returned!
- Implementations can fully customize the proof system, (de)serialization strategies of bytes and/or the bussiness workflow. For example, when implementing “Zether” confidential token contracts, the _confidentialTransferValue and accounts’ confidential balances will be encrypted homomorphically under ElGamal public keys, and _proof will consist 3 parts to check:

_confidentialTransferValue is well encrypted under public keys of _from 's, _to 's and caller’s;
- The plaintext value behind _confidentialTransferValue is non-negative;
- The caller’s confidential allowance is actually enough to pay the plaintext value behind _confidentialTransferValue .

```auto
function confidentialTransferFrom(
  address _from,
  address _to,
  bytes memory _confidentialTransferValue,
  bytes memory _proof
) public returns (bool success)

```

##### confidentialApprove

Allows `_spender` to withdraw from caller’s splitted part of balances multiple times, up to the the amount (allowance value) behind `_confidentialValue` to 0. This function SHOULD `throw` if the message caller’s `_proof` of this transfer fails to be verified.

Caution:

This function behaves much **different from** `approve(address,uint256)` in ERC20.

Calling `confidentialApprove` splits the confidential balance of caller’s account into *allowance part* and *the left part* .

The values behind two parts above after calling `confidentialApprove` , and the value behind the original confidential balance of caller’s account before calling `confidentialApprove` satisfy the equation:

[![截屏2025-04-17 15.09.21](https://ethereum-magicians.org/uploads/default/optimized/2X/a/ad66c011c6e3bfa2e43601f8f36e3b59ecda6933_2_517x20.png)截屏2025-04-17 15.09.213216×128 68.4 KB](https://ethereum-magicians.org/uploads/default/ad66c011c6e3bfa2e43601f8f36e3b59ecda6933)

- The allowance part of confidential balance allows _spender to withdraw multiple times through calling confidentialTransferFrom until _spender does not call it any more or the value behind this part is 0.

Every time the _spender calls confidentialTransferFrom , the value behind this part will be decreased by the value behind _confidentialTransferValue .

The left part remains as the new confidential balance of caller’s account.

If this function is called again it,

- merges existing allowance part into the confidential balance of caller’s account; and then
- overwrites the current allowance part with _confidentialValue .

Note:

- Callers MUST handle false from returns (bool success). Callers MUST NOT assume that false is never returned!
- Implementations can fully customize the proof system, (de)serialization strategies of bytes and/or the bussiness workflow. For example, when implementing “Zether” confidential token contracts, the _confidentialValue and accounts’ confidential balances will be encrypted homomorphically under ElGamal public keys, and _proof will consist 3 parts to check:

_confidentialValue is well encrypted under public keys of caller’s and _spender 's;
- The plaintext value behind _confidentialValue is non-negative;
- The caller’s confidential balance is actually enough to pay the plaintext value behind _confidentialValue .

```auto
function confidentialApprove(
  address _spender,
  bytes memory _confidentialValue,
  bytes memory _proof
) public returns (bool success)
```

##### confidentialAllowance

Returns the allowance part which `_spender` is still allowed to withdraw from `_owner` .

```auto
functinon confidentialAllowance(address _owner, address _spender)
public view returns (bytes memory _confidentialValue)
```

#### Events

##### ConfidentialTransfer

MUST trigger when tokens are transferred.

Specifically, if tokens are transffered through function `confidentialTransferFrom` , `_spender` address MUST be set to caller’s; otherwise, it SHOULD be set to `0x0` .

A confidential token contract,

- which creates new tokens SHOULD trigger a ConfidentialTransfer with the _from address set to 0x0 when tokens are minted;
- which destroys existent tokens SHOULD trigger a ConfidentialTransfer with the _to address set to 0x0 when tokens are burnt.

```auto
event ConfidentialTransfer(
  address indexed _spender,
  address indexed _from,
  address indexed _to,
  bytes _confidentialTransferValue
)
```

##### ConfidentialApproval

MUST trigger on any successful call to `confidentialApprove(address,bytes,bytes)` .

```auto
event ConfidentialApproval(
  address indexed _owner,
  address indexed _spender,
  bytes _currentAllowancePart,
  bytes _allowancePart
)
```

## Rationale

Confidential transactions have been implemented in many blockchains, either natively through blockchain protocols like Monero and Zcash, or through smart contracts like Zether (see [Zether: Towards Privacy in a Smart Contract World | Springer Nature Link (formerly SpringerLink)](https://doi.org/10.1007/978-3-030-51280-4_23) ) without modifying blockchain protocol.

However, when it comes to the latter way, actually no standards are proposed yet to illustrate such contracts. Users and applications cannot easily detect whether a token contract supports confidential transactions or not, and so hardly can they make transfers without revealing the actual amount.

Consequently, this proposal is to stardardize the confidential transaction supported token contracts, meanwhile without loss of generality, by only specifying core methods and events.

### Optional Accessor of “Confidential Total Supply”

Confidentiality of transfer amount makes it hard to support such field like `totalSupply()` in ERC20 (see [ERC-20: Token Standard](https://eips.ethereum.org/EIPS/eip-20) ). Because when it comes to the token “mint” or “burn”, if every user in this contract can access `totalSupply()` as well as decrypt it, these users will know the actual token value to be minted or burnt by comparing the `totalSupply()` before and after such operations, which means that confidentiality no longer exists.

Contract implementation can optionally support `confidentialTotalSupply()` by evaluating if anti-money laundrying (see next part) and audit are required. That would be much more plausible by making a small group of parties can know the plaintext total supply behind `confidentialTotalSupply()` .

```auto
function confidentialTotalSupply() public view returns (bytes memory)
```

### Anti-money Laundrying and Audit

To support audit of confidential transactions and total supply, especially such token issuers are banks or other financial institues supervised by governments or monetary authorities, confidential transactions can be implemented without changing `confidentialTransfer` method signature, by encoding more info into parameters.

For example in Zether-like implementation (see [PGC: Decentralized Confidential Payment System with Auditability | Springer Nature Link (formerly SpringerLink)](https://doi.org/10.1007/978-3-030-58951-6_29)), if token transfers are required to be audited, `confidentialTransfer` caller encrypts transfer `value` redundantly under public keys of caller’s, `to` ‘s, a group of auditors’, which makes it possible that related parties can exactly know the real `value` behind. So does `confidentialTotalSupply()` .

### Fat Token

Confidential transactions supported token can also implement ERC20 at the same time.

Token accounts in such tokens can hold 2 kinds of balances. Such token contracts can optionally provide methods to hind ERC20 plaintext balances into confidential balances, and vice versa, to reveal confidential balances back to ERC20 plaintext balances.

ERC20 interfaces will bring much more usability and utilities to confidential transaction supported tokens, realizing general confidentiality meantime.

## Backwards Compatibility

No backward compatibility issues found.

## Security Considerations

To realize full confidentiality, contracts implementing this presented interface SHOULD NOT creates (mints) or destroys (burns) tokens with plaintext value parameters. For implementation, following the same encryption strategies in `confidentialTransfer(address,bytes,bytes)` is RECOMMENDED.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**andrewcheng** (2025-05-14):

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1034)














####


      `master` ← `andrewcoder666:master`




          opened 09:42AM - 09 May 25 UTC



          [![](https://avatars.githubusercontent.com/u/22554065?v=4)
            andrewcoder666](https://github.com/andrewcoder666)



          [+250
            -0](https://github.com/ethereum/ERCs/pull/1034/files)







This PR proposal draws up a standard interface of confidential transaction suppo[…](https://github.com/ethereum/ERCs/pull/1034)rted token contracts, by providing basic functionality without loss of generality. Contracts following the standard can provide confidentiality for users’ balances and token transfer value.

---

**huyminh** (2025-10-13):

Hey everyone,

I’ve been looking into EIP-7945 and the whole idea of confidential transactions is super interesting.

To better understand the concept and contribute to the discussion, I have developed an initial implementation of the EIP using Zether and Circom. Here’s the link to what I have so far:



      [github.com](https://github.com/huyminh1115/eip7945-implementation)




  ![image](https://opengraph.githubassets.com/8908e674bd0757ff547571c09237eac2/huyminh1115/eip7945-implementation)



###



EIP-7945 confidential token with Zether protocol, BabyJub curve, and Circom ZK proofs










I would be very grateful for any feedback from the community. Specifically, I am interested in your thoughts on:

- The overall implementation strategy.
- Suggestions for improvement or optimization.
- Any areas where my interpretation may deviate from the EIP’s specification.

Thank you for your time and consideration. I look forward to the ongoing discussion around this proposal.

---

**SamWilsn** (2025-12-01):

> Transfers value amount of tokens (behind _confidentialTransferValue ) to address _to , and MUST fire the ConfidentialTransfer event. The function SHOULD throw if the message caller’s _proof of this transfer fails to be verified.

Are you sure you want to recommend throwing over reverting?

---

**SamWilsn** (2025-12-01):

Why keep the boolean return value from ERC-20? Is there a reason to keep it over just reverting on failure?


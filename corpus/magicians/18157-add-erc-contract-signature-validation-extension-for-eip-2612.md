---
source: magicians
topic_id: 18157
title: "Add ERC: Contract signature validation extension for EIP-2612 Permit"
author: yzhang1994
date: "2024-01-16"
category: ERCs
tags: [erc, account-abstraction]
url: https://ethereum-magicians.org/t/add-erc-contract-signature-validation-extension-for-eip-2612-permit/18157
views: 2297
likes: 5
posts_count: 7
---

# Add ERC: Contract signature validation extension for EIP-2612 Permit

## EIP: Contract signature validation extension for EIP-2612 Permit

### Included EIPs

- ERC-2612: Permit Extension for EIP-20 Signed Approvals
- ERC-1271: Standard Signature Validation Method for Contracts

### Abstract

This proposal aims to extend the functionality of the existing ERC-2612: Permit to support gasless ERC-20 approval operations initiated by smart contract wallets.

### Motivation

The current signature validation scheme in ERC-2612:, based on V, R, S parameters, restricts signature validation to EOA wallets.

With the growing popularity of smart contract wallets and increased adoption of ERC-1271, it is necessary to allow for flexible signature validation methods and the use of custom logic in each contract’s signature verification. By accepting unstructured signature bytes as input, custom algorithms and signature schemes can be utilized, enabling a wider range of wallet types.

### Specification

Compliant contracts must implement the `permit` using the following spec

```auto
function permit(address owner, address spender, uint value, uint deadline, bytes memory signature) external
```

as well as two other interfaces previously mandated by ERC-2612:

```auto
function nonces(address owner) external view returns (uint)
function DOMAIN_SEPARATOR() external view returns (bytes32)
```

A call to `permit(owner, spender, value, deadline, signature)` will set `allowance[owner][spender]` to value, increment `nonces[owner]` by 1, and emit a corresponding `Approval` event, if and only if the following conditions are met:

- The current blocktime is less than or equal to deadline.
- owner is not the zero address.
- nonces[owner] (before the state update) is equal to nonce.
- signature validation:

If owner is an EOA, signature is a valid secp256k1 signature in the form of abi.encodePacked(r, s, v).
- If owner is a contract, signature is validated by calling isValidSignature() on the owner contract.

If any of these conditions are not met, the permit call must revert.

### Rationale

By replacing the existing V, R, S signature validation scheme and introducing support for unstructured bytes input, contract developers can use a unified interface to validate signature from both EOAs and SC wallets. This allows for the utilization of different signature schemes and algorithms fitting the wallet type, paving the way for smart contract wallets and advanced wallet types to enhance their signature validation processes, promoting flexibility and innovation.

### Reference Implementation

Sample `permit` implemented with OZ’s SignatureChecker

```solidity
/**
 * @notice Update allowance with a signed permit
 * @dev Signature bytes can be used for both EOA wallets and contract wallets.
 * @param owner       Token owner's address (Authorizer)
 * @param spender     Spender's address
 * @param value       Amount of allowance
 * @param deadline    The time at which the signature expires (unix time)
 * @param signature   Unstructured bytes signature signed by an EOA wallet or a contract wallet
 */
function permit(
    address owner,
    address spender,
    uint256 value,
    uint256 deadline,
    bytes memory signature
) external {
    require(deadline >= now, "Permit is expired");
    require(owner != address(0), "ERC20: approve from the zero address");
    require(spender != address(0), "ERC20: approve to the zero address");

    bytes32 digest = keccak256(abi.encodePacked(
        hex"1901",
        DOMAIN_SEPARATOR,
        keccak256(abi.encode(
            keccak256("Permit(address owner,address spender,uint256 value,uint256 nonce,uint256 deadline)"),
            owner,
            spender,
            value,
            nonce,
            deadline
        ))
    ));

    require(
        // Check for both ECDSA signature and and ERC-1271 signature. A sample SignatureChecker is available at
        // https://github.com/OpenZeppelin/openzeppelin-contracts/blob/7bd2b2a/contracts/utils/cryptography/SignatureChecker.sol
        SignatureChecker.isValidSignatureNow(
            owner,
            typedDataHash,
            signature
        ),
        "Invalid signature"
    );

    allowed[owner][spender] = value;
    emit Approval(owner, spender, value);
}
```

### Backward Compatibility

This proposal is fully backward-compatible with the existing ERC-2612 standard. Contracts that currently rely on the V, R, S signature validation scheme will continue to function without any issues.

If both V, R, S signature validation and the new unstructured bytes signature validation need to be supported for backward compatibility reasons, developers can reduce duplicates by adapting the following code block as an example:

```auto
function permit(
    address owner,
    address spender,
    uint256 value,
    uint256 deadline,
    uint8 v,
    bytes32 r,
    bytes32 s
) external {
    _permit(owner, spender, value, deadline, abi.encodePacked(r, s, v));
}
```

### Security Considerations

- For contract wallets, the security of permit relies on isValidSignature() to ensure the signature bytes represent the desired execution from contract wallet owner(s). Contract wallet developers must exercise caution when implementing custom signature validation logic to ensure the security of their contracts.

## Replies

**smatthewenglish** (2024-01-29):

this is a smart idea, i also need this

---

**calvbore** (2024-01-29):

I support an update for 2612 to explicitly accept 1271 signatures.

---

**k06a** (2024-03-08):

Fully support this idea! Original Permit does not allow placing permit-based limit orders from multisig or smart accounts.

---

**radek** (2024-03-24):

awesome - seams to conclude the applicability discussion about 1271 for ERC20: [ERC-1271 : Standard Signature Validation Method for Contracts · Issue #1271 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/1271#issuecomment-1654816086)

Yet, Circle just extended 2612 implementation for 1271 - without extending interface: https://etherscan.io/address/0x43506849d7c04f9138d1a2050bbf3a0c054402dd#code#F19#L1

Which approach has the better adoption potential? USDC’s adjustement of 2612 or this ERC 7597?

---

**xshape** (2024-04-03):

I like the idea, I think this can be very useful.

---

**SamWilsn** (2024-05-13):

> If owner is an EOA […]

> If owner is a contract […]

How should the contract determine if `owner` is an EOA or contract? There is at least one proposal ([EIP-3540](https://eips.ethereum.org/EIPS/eip-3540#changes-to-execution-semantics)) that is trying to remove visibility into the code of external accounts. To be maximally forward compatible, I think you could define an algorithm for contracts to follow. Maybe a boolean for `ecrecover` vs. ERC-1271, or “try `ecrecover` first. If that fails, try ERC-1271.”


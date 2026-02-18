---
source: magicians
topic_id: 26706
title: "ERC-8087: Encrypted Hashed Arguments and Calls"
author: cfries
date: "2025-11-24"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-8087-encrypted-hashed-arguments-and-calls/26706
views: 69
likes: 0
posts_count: 2
---

# ERC-8087: Encrypted Hashed Arguments and Calls

We propose an ERC for executing function calls with encrypted arguments (and optionally encrypted  call descriptors) via a stateless decryption oracle. The goal is to support use-cases like  privacy-preserving order books or conditional DvP flows, while keeping the standard itself  as generic as possible.

The design is about *when* arguments and call descriptors become visible on-chain, not about  making calls or value flows permanently unlinkable. Once a request is fulfilled, anyone can  correlate the fulfilled call with the original requester via the standardized events.

## Simple Summary

This ERC standardizes how smart contracts can request a **function execution with encrypted arguments**,  optionally with an **encrypted call descriptor**, using a stateless decryption oracle (a *Call Decryption Oracle*).

It separates

1. a reusable, verifiable container for encrypted arguments, and
2. a call descriptor (what to call, and any validity constraints),

and defines how an off-chain oracle decrypts and executes such calls.

## Abstract

This ERC defines a data format and contract interface for executing smart contract calls where:

1. The arguments are encrypted and reusable (EncryptedHashedArguments), and
2. The call descriptor (target contract, selector, validity) is either

encrypted (EncryptedCallDescriptor), or
3. plain (CallDescriptor).

The encrypted arguments and the call descriptor are *not* directly bound on-chain. Instead, an on-chain  contract (the target or an orchestration contract) stores a hash commitment to the plaintext arguments and later verifies that the decrypted argument payload matches the stored commitment.

An on-chain *call decryption oracle* contract offers a request*/fulfill* pattern to request a call with encrypted arguments, which is fulfilled if admissible.

An off-chain *call decryption oracle* listens to standardized events, decrypts payloads, enforces any off-chain access-control policy, and calls back into the on-chain oracle to perform the requested call.

The ERC is compatible with existing decryption-oracle designs such as ERC-7573 and can be implemented as an extension of such oracles.

The contract receiving the decrypted arguments can pass these on to other contracts, which can, if necessary, validate the arguments against the previously stored **hash commitment**.

The decrypted arguments are transported as `(uint256 requestId, bytes argsPlain)` to allow correlating the call to the request. Here `argsPlain` is an ABI-encoding of a typed argument list (depending on the business logic).

## Motivation

Privacy- and conditionality-preserving protocols often need to:

- Keep arguments confidential until some condition is met (e.g. order books).
- Optionally keep the target address and function itself confidential.
- Allow reusable encrypted argument blobs that can be passed between contracts and stored on-chain.
- Allow the receiver of a call to verify that the decrypted arguments used in the call are exactly those that were committed to earlier.

Existing work like ERC-7573 focuses on a specific decryption-oracle use-case with fixed callbacks (e.g. DvP).

This ERC generalizes that pattern to a **generic function execution** mechanism, designed around:

- a clear separation of argument encryption and call encryption, and
- an explicit hash commitment enabling verification of the arguments by the receiving contract.

### Exemplary Use-Cases

#### Order Book Build Process avoiding Front Running

A possible use-case is the construction of an auction / order book preventing front-running, where the proposals can be made during a predefined phase. Here participants submit their proposals as encrypted hashed arguments, which are stored inside a smart contract. Once the order phase is closed, the smart contract calls the *call decryption oracle* (passing itself as the callback target) to receive the decrypted arguments in a call that will build the order book.

## Specification

### 1. Encrypted arguments

Encrypted arguments are independent of any particular call descriptor and can be reused.

Upon (off-chain) encryption (initialization) a hash of the (plain) arguments is generated accompanying the encrypted arguments to allow later verification.

```solidity
struct EncryptedHashedArguments {
    /**
     * Commitment to the plaintext argument payload.
     * The target contract should check keccak256(argsPlain) == argsHash.
     */
    bytes32 argsHash;

    /**
     * Identifier of the public key used for encryption (e.g. keccak256 of key material).
     */
    bytes32 publicKeyId;

    /**
     * Ciphertext of abi.encode(ArgsDescriptor), encrypted under publicKeyId.
     */
    bytes ciphertext;
}
```

#### Normative requirements (EncryptedHashedArguments)

For producers of `EncryptedHashedArguments`:

- The producer MUST compute

```solidity
  argsHash = keccak256(argsPlain);
```

where `argsPlain` is an `abi.encode(args...)` byte sequence and part of the `ArgsDescriptor` (see below).

- The producer MUST set ciphertext to the encryption of exactly

```solidity
abi.encode(argsDescriptor)
```

 under the key identified by publicKeyId, where argsDescriptor is an ArgsDescriptor as defined below.
- The producer MUST set argsHash to the value computed above.

A *call decryption oracle* implementation **MAY** provide a command line tool or endpoint to generate `EncryptedHashedArguments` from plaintext arguments.

This ERC does not standardize the encryption algorithm or key management; those are implementation-specific (similar to ERC-7573). Implementations **SHOULD** document how `publicKeyId` is derived from the underlying key material.

#### Argument Descriptor structure (normative for eligibility)

Prior to encryption, the arguments are bundled with an (optional) list of `eligibleCaller`s, to allow a *Call Decryption Oracle* to enforce eligibility of the requester in a consistent way. This prevents decryption by other contracts through observing encrypted arguments and requesting a call to the call decryption oracle.

This ERC standardizes the layout of the decrypted payload as:

```solidity
struct ArgsDescriptor {
    /**
     * List of addresses allowed to request decryption.
     * If empty, any requester is allowed. This is enforced off-chain by the oracle operator.
     */
    address[] eligibleCaller;

    /**
     * Plain argument payload, may be abi.encode(args...).
     */
    bytes argsPlain;
}
```

In this case, producers set

```solidity
bytes32 argsHash = keccak256(argsDescriptor.argsPlain);
bytes   ciphertext = ENC_publicKeyId(abi.encode(argsDescriptor));
```

The `eligibleCaller` list is not visible to on-chain contracts; it is only used off-chain by the oracle operator to decide whether to honor a decryption request.

### 2. Call descriptor

A **call descriptor** defines:

- which contract and function will be called, and
- any validity constraint (e.g. expiry block).

```solidity
struct CallDescriptor {
    /**
     * Contract that will be called by the oracle.
     */
    address targetContract;

    /**
     * Function that will be called by the oracle.
     * 4-byte function selector for the targetContract whose signature MUST be (uint256, bytes).
     */
    bytes4 selector;

    /**
     * Optional expiry (block number). 0 means "no explicit expiry".
     */
    uint256 validUntilBlock;
}
```

#### Plain vs. Encrypted Call Descriptors

A call descriptor can be:

- Plain: CallDescriptor is passed in clear on-chain.
- Encrypted: CallDescriptor is wrapped into:

```solidity
struct EncryptedCallDescriptor {
    /**
     * Identifier of the public key used for encryption.
     */
    bytes32 publicKeyId;

    /**
     * Ciphertext of abi.encode(CallDescriptor), encrypted under publicKeyId.
     */
    bytes ciphertext;
}
```

#### Normative requirements (CallDescriptor and EncryptedCallDescriptor)

- When using EncryptedCallDescriptor, the ciphertext MUST be the encryption of exactly abi.encode(CallDescriptor) under the key identified by publicKeyId.

### 3. Encryption/Decryption Method and optional Second Factor

The encryption/decryption method is an implementation detail of the call decryption oracle contract and bound to the contract address. Different instances may utilize different methods. The publicKeyId can serve as an indication in case the oracle performs a key rotation.

#### Second Factor

The oracle interface to request a call with encrypted arguments allows passing an optional `secondFactor`. The interpretation and encoding of the second factor is an implementation detail of a concrete oracle implementation. The second factor enables decryption schemes in which the owner/operator of the decryption oracle **cannot** decrypt the encrypted arguments before a request is made that provides this factor. This is useful in use-cases such as order books, where the oracle operator should not be able to inspect orders before a reveal / decryption phase. In such setups, trust in the oracle is primarily about **timely fulfilment**, not about keeping arguments secret forever.

The passed second factor may be an `abi.encode(...)` of a more complex structure, e.g. an encoded `bytes[]`, thus allowing for multiple factors to implement a k-out-of-n threshold decryption off-chain.

### 4. Oracle interface

The oracle exposes a **request/fulfill** pattern. Requests are cheap and do not require on-chain decryption; fulfillment is called by an off-chain operator after decryption.

```solidity
    function requestCall(
        CallDescriptor            calldata callDescriptor,
        EncryptedHashedArguments  calldata encArgs,
        bytes                     calldata secondFactor
    ) external payable returns (uint256 requestId);

    function requestEncryptedCall(
        EncryptedCallDescriptor   calldata encCall,
        EncryptedHashedArguments  calldata encArgs,
        bytes                     calldata secondFactor
    ) external payable returns (uint256 requestId);

    function fulfillEncryptedCall(
        uint256          requestId,
        CallDescriptor   calldata callDescriptor,
        bytes            calldata argsPlain
    ) external;

    function fulfillCall(
        uint256          requestId,
        bytes            calldata argsPlain
    ) external;

    function rejectCall(
        uint256 requestId,
        RejectionReason reason,
        bytes calldata details
    ) external;
}
```

> Note: This ERC does not standardize the exact storage layout of pending requests or the internal access control
> for fulfill* (e.g. onlyOracle). Implementations MUST ensure that only the intended oracle operator can call the
> fulfill* functions.

### 5. Target contract

A common pattern is that the target contract

1. In an initialization phase, receives and stores an encrypted argument encArg together with its hash argsHash, where argsHash is the hash of the plaintext argument payload.
2. In the execution phase, the caller issues a request to the call decryption oracle, obtains the requestId returned by requestCall / requestEncryptedCall, and passes this requestId along with argsHash to the call target (may be the same contract) in the same transaction. The call target then receives the decrypted argument payload argsPlain (under a callback selector) from the call decryption oracle, with the corresponding requestId and recomputes the hash and compares it to the stored value.
3. The call target can the procees with the business logic operating on the decrypted (and verified) arguments.

For example, the producer of `EncryptedHashedArguments` may choose

```solidity
bytes memory argsPlain = abi.encode(amount, beneficiary);
bytes32 argsHash = keccak256(argsPlain);
```

The target (or router) contract can then do:

```solidity
mapping(uint256 => bytes32) public argsHashByRequestId;

function registerArguments(uint256 requestId, bytes32 argsHash) external {
    // In the same transaction as the request, store the commitment for this requestId.
    argsHashByRequestId[requestId] = argsHash;
}

/**
 * @dev Target selector: Called by the Call Decryption Oracle with decrypted arguments.
 * The oracle calls this function with signature
 *    callback(uint256 requestId, bytes argsPlain)
 * where requestId is the technical correlation id assigned by the oracle.
 */
function executeWithVerification(
    uint256 requestId,
    bytes   calldata argsPlain
) external {
    // Lookup the pre-committed hash from the init phase.
    bytes32 stored = argsHashByRequestId[requestId];
    require(stored != bytes32(0), "Unknown requestId");

    // Recompute the hash from the received bytes.
    bytes32 computed = keccak256(argsPlain);
    require(computed == stored, "Encrypted args mismatch");

    /**
     * Optional: decode argsPlain to use it, e.g.
     *   (uint256 amount, address beneficiary) = abi.decode(argsPlain, (uint256, address));
     * and route to business logic.
     */
}
```

In this pattern:

- argsHash is the hash commit of argsPlain created upon off-chain argument construction.
- requestId is the technical identifier assigned by the Call Decryption Oracle when the request is issued. It is useful for correlation, logging and mapping inside routers, but is not required for the hash check.
- The argsPlain field passed to fulfill* is the exact byte payload used to compute argsHash. The callback (target or router) decodes argsPlain to recover the business arguments.
- A router/adapter contract can implement the executeWithVerification(uint256 requestId, bytes argsPlain) callback, perform the verification and decoding, and then call an already deployed target contract with its original typed function signature.

Implementations SHOULD register the `(requestId, argsHash)` mapping in the same transaction that issues the request to the oracle, to avoid any race where a very fast oracle operator could attempt to fulfill a request before the mapping is written on-chain. Even if the mapping is missing, the callback pattern above will cause the fulfillment to revert (due to `Unknown requestId`); however, registering in the same transaction provides deterministic behaviour.

## Rationale

- The two-stage design (arguments vs. call) allows encrypted arguments to be reusable and independent of any particular call descriptor.
- The explicit hash commitment (argsHash) binds arguments to a commitment stored by the receiving contract, while still allowing the arguments to be stored and passed separately as opaque bytes.
- The request/fulfill pattern reflects that decryption is off-chain. Requests are cheap; fulfill is initiated when decryption is ready.
- The use of abi.encodeWithSelector(selector, requestId, argsPlain) makes the on-chain oracle generic and able to support arbitrary function signatures while still providing a standard correlation identifier (requestId).
- Router/adapter pattern: when integrating with already deployed contracts whose function signatures cannot be changed, a small router contract can serve as the callback. The router implements a function like executeWithVerification(uint256 requestId, bytes argsPlain), verifies requestId and argsHash as above, decodes argsPlain into typed arguments, and then calls the pre-existing target contract with its original typed function. This preserves compatibility with existing deployments while still using the standard call decryption oracle.

## Backwards Compatibility

This ERC is designed to coexist with ERC-7573 decryption oracles. An existing ERC-7573 implementation can be extended to implement `ICallDecryptionOracle` without breaking existing interfaces.

## Reference Implementation

A non-normative reference implementation (Solidity) and a matching Java/off-chain implementation are provided separately. They illustrate:

- storage of pending requests,
- event emission for both encrypted and plain call descriptors,
- validation of hash bindings, and
- low-level call execution.

These implementations are work-in-progress and may evolve independently of the ERC text.

### Fees

Implementations MAY charge fees in ETH or ERC-20 tokens as part of their specific deployment.

## Security Considerations

### Oracle trust

The on-chain contract cannot verify correctness of decryption; it can only check that `keccak256(argsPlain) == argsHash`.  Parties must trust the oracle operator (or design an incentive/penalty mechanism) to decrypt correctly and call `fulfill*` faithfully.

### Replay

Implementations SHOULD mitigate replay by:

- using validUntilBlock in CallDescriptor, and/or
- including nonces or sequence numbers in higher-level protocols.

### Access control

Access control is an application-level concern. A common pattern is to embed an access-control list such as `address[] eligibleCaller` inside the encrypted payload (in `ArgsDescriptor`) and have the off-chain oracle operator enforce that the original requester is contained in that list (unless the list is empty, meaning “any requester”). The standard does not prescribe a particular access-control mechanism beyond this guidance.

### Traceability and non-mixing

This ERC is **not** intended to act as a mixer or general-purpose anonymization service for payments or calls.  Its purpose is to **defer** the disclosure of arguments (and optionally the call descriptor) until fulfillment.

Implementations SHOULD preserve the ability for off-chain indexers and observers to correlate `CallFulfilled` events with the corresponding `CallRequested` / `EncryptedCallRequested` events, for example by strictly adhering to the `requestId` linkage defined in this ERC.

Once a request is fulfilled, an observer can always reconstruct which `requester` initiated the request and which call and arguments were eventually used. Protocols that deliberately try to break this correlation or to hide value flows are out of scope of this ERC.

## Copyright

Copyright and related rights waived via CC0.

## Sequence Diagram

The following diagram illustrates the interaction between cient contract, decryption oracle contract and target contract.

[![encrypted-arguments-transparent-call-flow](https://ethereum-magicians.org/uploads/default/optimized/3X/3/2/32e2990c7317b6366cdd229bd7e92f10a9d287f7_2_690x484.png)encrypted-arguments-transparent-call-flow2043×1434 70.2 KB](https://ethereum-magicians.org/uploads/default/32e2990c7317b6366cdd229bd7e92f10a9d287f7)

## Replies

**cfries** (2025-11-30):

A **test deployment** of the **call decryption oracle** is available at the addresses below.

For a quick round-trip via Remix see the [Usage Page](https://finmath-decryption-oracle-3902fb.gitlab.io/finmath-decryption-oracle-encrypted-hashed-execution/usage/index.html) and the [Try It in Remix Page](https://finmath-decryption-oracle-3902fb.gitlab.io/finmath-decryption-oracle-encrypted-hashed-execution/try-it/index.html).

---

**Ethereum Mainnet**

```solidity
0x0a435F6f9E0933d5cfC6877209872b979414DD6e
```

**Polygon Mainnet**

```solidity
0x4f0c19951278667dDEBF31615b061160f2731F69
```

**Sepolia** (Ethereum Testnet)

```solidity
0x23447F00953C623351399C235A770cB3523c1A4f
```

**Amoy** (Polygon Testnet)

```solidity
0xfd42Dc58c152b688bb5A563052A682904e268dA4
```


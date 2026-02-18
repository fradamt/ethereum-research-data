---
source: magicians
topic_id: 24180
title: "EIP 7963: Oracle-Permissioned ERC-20 with ZK Proofs"
author: junmeng.t
date: "2025-05-15"
category: ERCs
tags: [erc, token, evm, zkp, merkle-proof]
url: https://ethereum-magicians.org/t/eip-7963-oracle-permissioned-erc-20-with-zk-proofs/24180
views: 433
likes: 6
posts_count: 5
---

# EIP 7963: Oracle-Permissioned ERC-20 with ZK Proofs

Proposed by Ant International: https://www.ant-intl.com/en/

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/7/7a9e49f26a9b9aaba0dd6f0fd361fc4357f067b2_2_690x284.jpeg)image1342×554 60.7 KB](https://ethereum-magicians.org/uploads/default/7a9e49f26a9b9aaba0dd6f0fd361fc4357f067b2)

# Simple Summary

This proposal extends ERC-20 tokens with oracle-permissioned transfers validated by zero-knowledge proofs. Token transfers are only valid when an external “Transfer Oracle” pre-approves them using off-chain payment instructions in a standardized JSON format, proven on-chain via ZK proofs.

## Abstract

The standard defines:

- ITransferOracle – a minimal interface that any ERC-20-compatible contract can consult to decide whether transfers should succeed
- approveTransfer flow – whereby an issuer deposits a one-time approval in the oracle with a ZK-proof attesting that the approval matches a canonicalized payment instruction message
- canTransfer query – whereby the token contract atomically consumes an approval when the holder initiates the transfer
- Generic data structures, events, and hooks that allow alternative permissioning logics (KYC lists, travel-rule attestations, CBDC quotas) to share the same plumbing

The scheme is issuer-agnostic, proof-system-agnostic, and network-agnostic (L1/L2). The payment instruction format is compatible with ISO 20022 pain.001 for interoperability with existing financial systems, but does not require implementers to access proprietary ISO specifications. Reference implementation uses RISC Zero as the proving system, but the standard admits any ZK-proof system.

## Motivation

Institutional tokenisation requires *both* ERC-20 fungibility **and** legally enforceable control over who may send value to whom and why.

Hard-coding rules in every token contract is brittle and non-standard. Centralising rules in a singleton oracle and proving off-chain documentation on-chain gives:

- Compliance traceability – every transfer links to a signed payment
order recognised by traditional finance systems.
- Issuer flexibility – any institution can swap out its oracle logic
without breaking ERC-20 compatibility.
- Composability – DeFi protocols can interact with permissioned tokens
using familiar ERC-20 flows, while downstream permission checks are
encapsulated in the oracle.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

### Interfaces

```solidity
/// @notice One-time ZK-backed approval for a single transfer.
struct TransferApproval {
    address  sender;
    address  recipient;
    uint256  minAmt;      // Minimum allowed transfer amount (inclusive)
    uint256  maxAmt;      // Maximum allowed transfer amount (inclusive)
    uint256  expiry;      // UNIX seconds; 0 == never expires
    bytes32  proofId;     // keccak256(root‖debtorHash‖creditorHash)
}

/// @title  External oracle consulted by permissioned tokens.
interface ITransferOracle {
    /// @dev   Verifies zk-proof and stores a one-time approval.
    /// @return proofId – unique handle for off-chain reconciliation
    function approveTransfer(
        TransferApproval calldata approval,
        bytes calldata proof,          // ZK proof bytes (system-specific)
        bytes calldata publicInputs    // ABI-encoded public outputs
    ) external returns (bytes32 proofId);

    /// @dev   Atomically consumes an approval that covers `amount`.
    ///        MUST revert if no such approval exists.
    function canTransfer(
        address token,
        address issuer,
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bytes32 proofId);
}
```

### ERC-20 Hook

A *Permissioned ERC-20* **MUST** replace the standard internal

`_update(address from, address to, uint256 amount)` logic with:

```solidity
bytes32 proofId = ORACLE.canTransfer(address(this), owner(), from, to, amount);
// MUST revert on failure
_super._update(from, to, amount);
emit TransferValidated(proofId);
```

`ORACLE` is an immutable constructor argument. (up to design)

### Validation Requirements

The oracle implementation **MUST** enforce the following validation rules when processing `approveTransfer`:

```solidity
require(minAmt  block.timestamp || expiry == 0, "Approval already expired");
```

### Approval Consumption Behavior

**Single-Use Policy**: Each approval is consumed entirely when a matching transfer occurs. Approvals **CANNOT** be partially consumed or reused for multiple transfers.

**Amount Matching**: A transfer with `amount` is valid if and only if `minAmt <= amount <= maxAmt` (both bounds inclusive).

**Best-Match Selection**: When multiple valid approvals exist for the same (issuer, sender, recipient) triplet, the oracle **SHOULD** consume the approval with the smallest amount range to preserve larger approvals for potentially larger transfers.

**Expiry Handling**: Expired approvals (where `block.timestamp >= expiry` and `expiry != 0`) **MUST** be ignored during transfer validation but **MAY** remain in storage for auditing purposes.

### Events

```solidity
event TransferApproved(
    address indexed issuer,
    address indexed sender,
    address indexed recipient,
    uint256 minAmt,
    uint256 maxAmt,
    uint256  expiry,
    bytes32 proofId
);

event ApprovalConsumed(
    address indexed issuer,
    address indexed sender,
    address indexed recipient,
    uint256 amount,
    bytes32 proofId
);

event TransferValidated(bytes32 indexed proofId);
```

### Payment Instruction Message Format

Payment instructions **MUST** be JSON objects with the following structure:

```json
{
  "messageId": "string",
  "creationDateTime": "ISO 8601 timestamp",
  "paymentInfo": {
    "debtor": {
      "name": "string",
      "identifier": "string",
      "identifierScheme": "string"
    },
    "creditor": {
      "name": "string",
      "identifier": "string",
      "identifierScheme": "string"
    },
    "amount": {
      "value": "string (in milli-units)",
      "currency": "string (ISO 4217 code)"
    },
    "executionDate": "ISO 8601 timestamp"
  }
}
```

**Field Definitions:**

- messageId: Unique identifier for this payment instruction
- creationDateTime: When the instruction was created (ISO 8601 format, UTC)
- debtor.identifier: Sender’s account identifier (Ethereum address, IBAN, BIC, etc.)
- debtor.identifierScheme: Type of identifier (e.g., “ethereum_address”, “iban”, “bic”, “swift”)
- creditor.identifier: Recipient’s account identifier
- creditor.identifierScheme: Type of identifier
- amount.value: Transfer amount in milli-units (integers only, no decimals)
- amount.currency: Three-letter currency code (e.g., “USD”, “EUR”, “GBP”)
- executionDate: When the transfer should execute (becomes approval expiry)

**Milli-unit Conversion**: All monetary amounts **MUST** be represented as integers in milli-units (10⁻³) to avoid floating-point precision issues:

- 1 milli-unit = 0.001 base currency units
- Example: 1.50 USD = “1500” milli-units
- Example: 0.001 BTC = “1” milli-unit

### Message Canonicalization

To ensure deterministic hashing, payment instructions **MUST** be canonicalized before Merkle tree construction:

1. JSON Canonicalization: Apply RFC 8785 (JCS)

Sort object keys lexicographically
2. Remove insignificant whitespace
3. Use minimal JSON encoding
4. Text Normalization: Apply UTF-8 NFC (Normalization Form C) to all string fields
5. Timestamp Format: All timestamps MUST use ISO 8601 format in UTC (e.g., “2025-01-03T10:30:00Z”)

**Example Canonicalization:**

Input:

```json
{ "amount": { "value": "1500", "currency": "USD" }, "debtor": { "name": "Alice" } }
```

Output (canonical):

```json
{"amount":{"currency":"USD","value":"1500"},"debtor":{"name":"Alice"}}
```

### Merkle-and-Proof Requirements

The merkle tree root is used to verify that the public inputs actually come from the original off-chain payment instruction. The ZK proof system validates that all fields belong to the same committed payment message through Merkle proof verification.

| Public Inputs | Purpose | Rationale |
| --- | --- | --- |
| root | Merkle root of payment instruction | Data-integrity and field binding |
| debtorHash | Hash of debtor (sender) data | Privacy-preserving sender identification |
| creditorHash | Hash of creditor (recipient) data | Privacy-preserving recipient identification |
| minAmountMilli/maxAmountMilli | Value bounds in milli-units | Anti-front-running protection |
| currencyHash | Hash of currency code | Currency validation |
| expiry | Execution date as timestamp | Prevents replay and ensures timeliness |

The ZK proof system **MUST** verify:

1. Hash Integrity: All provided hashes match computed hashes of the actual data
2. Amount Bounds: The transfer amount falls within the specified range
3. Merkle Proofs: All fields (debtor, creditor, amount, currency, expiry) belong to the same committed message
4. Expiry Validation: The execution date is consistent and not expired

*The oracle MAY accept additional public inputs, e.g., extended currency validation, jurisdiction codes, sanctions list epochs*

### Proof System Flexibility

This standard is **proof-system-agnostic**. The reference implementation uses RISC Zero for:

- Transparent Setup: No trusted ceremony required
- Developer Experience: Write verification logic in Rust
- Performance: Efficient proof generation and verification
- Auditability: Clear, readable verification code

However, implementations **MAY** use any ZK proof system (Groth16, PLONK, STARKs, etc.) as long as they:

1. Validate the required public inputs listed above
2. Ensure proper Merkle proof verification for field binding
3. Maintain the same security guarantees

### Upgradeability

- Token and Oracle MAY be behind EIP-1967 proxies.
- Verifier is stateless; safe to swap when a new proof system is adopted.
- Oracle logic can be upgraded independently of token contracts.

## Rationale

Keeping oracle logic out of the token contract preserves fungibility and lets one oracle serve hundreds of issuers. `TransferApproval` uses *amount ranges* so issuers can sign a single approval before the final FX quote is known. `canTransfer` returns the `proofId`, enabling downstream analytics and regulators to join on-chain transfers with off-chain payment system messages.

The Merkle proof requirement ensures that all approval data comes from the same authentic payment instruction, preventing field substitution attacks where an attacker might try to combine legitimate data from different transactions.

**Amount Range Design**: The `minAmt`/`maxAmt` bounds accommodate scenarios where the exact transfer amount is unknown at approval time (e.g., currency conversion with fluctuating exchange rates). The inclusive bounds (`minAmt <= amount <= maxAmt`) provide clear validation semantics, while the single-use consumption policy prevents approval reuse attacks.

**Best-Match Selection**: When multiple approvals overlap, selecting the approval with the smallest range optimizes for approval preservation, allowing issuers to create both broad approvals (e.g., 0-1000 tokens) and specific approvals (e.g., 100-110 tokens) without the specific approval being wastefully consumed by small transfers.

## Backwards Compatibility

Existing ERC-20 consumers remain unaffected; a failed `transfer` simply reverts. Wallets and exchanges **should** surface the oracle’s revert messages so users know they lack approval.

## Reference Implementation

A complete reference implementation is available in the assets directory.

The implementation includes:

- Solidity Contracts: Complete implementation with OpenZeppelin v5 compatibility

PermissionedERC20.sol - ERC-20 token with oracle-based transfer validation
- TransferOracle.sol - Manages one-time transfer approvals with ZK proof verification
- RiscZeroVerifier.sol - RISC Zero proof verification contract

**RISC Zero ZK Programs**: Rust-based guest program for payment instruction validation

- Guest program validates payment instruction messages
- Merkle proof verification for field integrity
- Zero-knowledge proof generation

**Testing Framework**: Comprehensive test suite

- 80 passing smart contract tests (Hardhat/TypeScript)
- 34 passing Rust unit tests
- 11 passing integration tests
- Gas profiling and optimization tests

**Development Tools**:

- CLI host program for proof generation and verification
- Test data generators and utilities
- Deployment scripts for various networks

The reference implementation demonstrates:

- Full payment instruction message validation
- Merkle proof verification for field integrity
- RISC Zero proof generation and verification
- Integration with standard ERC-20 workflows
- Comprehensive error handling and edge cases

**Setup Instructions**: See README.md in the assets directory for installation and usage.

## Security Considerations

- Replay Protection – approvals are one-time and keyed by proofId.
- Field Binding – Merkle proofs ensure all approval data comes from the same committed message.
- Oracle Risk – issuers SHOULD deploy dedicated oracles; a compromised oracle only endangers its own tokens.
- Proof System Security – the chosen ZK proof system must provide computational soundness and zero-knowledge properties.
- Hash Function Security – implementations should use cryptographically secure hash functions (e.g., Keccak256, SHA256).
- Amount Validation – strict bounds checking prevents amount manipulation attacks.

## Copyright

Copyright and related rights waived via [CC0].

## Replies

**Redoudou** (2025-05-18):

super interested was talking about this with TradeFi recently would love to chat more.

---

**junmeng.t** (2025-05-18):

Thanks for taking a look! Please don’t hesitate to ask any more questions you may have about the proposal.

---

**Redoudou** (2025-05-18):

This proposal is to extend the ERC-20 standard to require mandatory external oracle approvals linked to ISO 20022-compliant payment messages via zero-knowledge proofs.

While innovative, this mandatory approach fundamentally diverges from Ethereum’s core ethos of openness, permissionlessness, and composability.

The main reasons why the current proposal is problematic include:

- Permissioning Overreach: By mandating oracle-based approvals, the proposal restricts token transfers, undermining Ethereum’s fundamental value of decentralization and open access.
- Interoperability Challenges: This approach risks creating significant friction in the existing Ethereum ecosystem, potentially fragmenting liquidity and complicating integrations with decentralized finance (DeFi) protocols, wallets, and exchanges that currently operate seamlessly with standard ERC-20 tokens.
- Complexity and User Confusion: Introducing a mandatory compliance layer risks confusion among users and developers, complicating token interactions and slowing down innovation.

Recognizing the importance of institutional and regulated adoption, aligning Ethereum tokens with global financial compliance standards such as ISO 20022 remains valuable. However, I believe this does not require altering the core ERC-20 standard through an EIP.

Instead, I propose adopting design principles that preserve the core ERC-20 compatibility while enabling optional compliance checks for institutional use cases:

- ERC-20 Compatibility: Tokens remain fully ERC-20 compliant, maintaining current permissionless functionality and interoperability.
- Optional Compliance Features: Institutions could introduce compliance via separate optional entry points (e.g., a clearly distinguished function like transferWithISOApproval). These would require external oracle validation only when explicitly invoked.
- Clear Documentation and Distinction: Ensure explicit documentation to distinguish between standard (permissionless) token transfers and compliance-required (permissioned) transfers to minimize confusion and integration complexity.

Furthermore, the Enterprise Ethereum Alliance (EEA) could play a pivotal role by hosting workshops and developing standardized design principles in collaboration with Ant International and other institutional stakeholders. These workshops would aim to establish clear guidelines and best practices for compliant token implementations that respect Ethereum’s open ethos.

---

**junmeng.t** (2025-05-19):

Hi Redoudou, appreciate your comprehensive reply. Allow me to clarify some of the feedback received here.

1. This EIP does not force every ERC-20 token to integrate an oracle. It simply defines a standard interface that permissioned tokens can adopt. Unpermissioned tokens incur zero overhead.
2. Defi protocols, wallets and explorers continue to use the exact same ERC-20 abi. They only see a revert on transfer if the user has not obtained the required approval - no new function signatures or hooks to learn.
3. The proposal ships references circuits, SDKs and Solidity templates. For most devs/builders, spinning up a compliant oracle is a matter of configuration, not reinventing zk-proof mechanics from scratch.
4. Many tokens today already implement pausable, blacklistable, or mint capable extensions - and those are widely accepted. This EIP simplifies a standard pattern for compliance-driven permissioning, rather than each project inventing its own bespoke mechanism.
5. By centralising compliance logic in oracles, we actually reduce fragmentation - one comprehensively-audited oracle per regulator or service provider can potentially serve hundreds of tokens, rather than countless bespoke implementations hidden in individual token contracts.
6. Institutions can deploy parallel permissioned token contracts alongside fully permissionless ones. Users and builders choose whichever variant suits their needs which actually maintains the open-access ethos for the broader ecosystem.

In summary, the EIP actually introduces an opt-in, standardised and modular way to have legally enforceable compliance onto ERC-20 tokens without breaking any existing tooling or fragmenting liquidity for the permissionless majority - it’s simply for institutions who may require permissioning functionality. Please do share your thoughts on what I have explained and if there are any questions and clarifications you may require as well, happy to have an extended open discussion.


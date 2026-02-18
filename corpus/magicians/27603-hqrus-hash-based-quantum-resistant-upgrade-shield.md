---
source: magicians
topic_id: 27603
title: "HQRUS: Hash-Based Quantum-Resistant Upgrade Shield"
author: lightning-li
date: "2026-01-27"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/hqrus-hash-based-quantum-resistant-upgrade-shield/27603
views: 46
likes: 1
posts_count: 1
---

# HQRUS: Hash-Based Quantum-Resistant Upgrade Shield

## Abstract

This EIP proposes **Hash-Based Quantum-Resistant Upgrade Shield (HQRUS)**, a framework designed to establish a proactive security shield for Ethereum accounts before a specific quantum-resistant (QR) signature algorithm is finalized.

**HQRUS** introduces a **Commitment Aggregation Layer** that allows users to off-chain sign a commitment to a list of random secret hashes. This commitment is aggregated into a Merkle Root stored on L1. When the quantum threat becomes imminent, users utilize a **QRBindingTransaction** to upgrade their accounts. This transaction requires a STARK proof revealing knowledge of the pre-images of the committed hashes.

To ensure a smooth transition, the EIP defines a **Three-Phase Migration Schedule** culminating in a strict enforcement phase where legacy transactions are rejected. It also provides an **Emergency Recovery Path** for users who failed to participate in the commitment phase, utilizing either a Zero-Knowledge proof of address derivation or a time-delayed activation.

## Motivation

### The Pre-Quantum Security Gap

The Ethereum community is currently evaluating various NIST-approved Post-Quantum Cryptography (PQC) algorithms. However, selecting and standardizing a single algorithm is premature. Hard-coding a specific QR algorithm today risks obsolescence.

### The “Shield First, Upgrade Later” Strategy

**HQRUS** allows users to add a layer of hash-based security *now*, which acts as a gatekeeper for the future upgrade. Since CRQCs (Cryptographically Relevant Quantum Computers) threaten ECDSA but not SHA-256/Keccak, anchoring the upgrade right to the **pre-image of a hash** ensures that even if an ECDSA key is compromised, the attacker cannot hijack the upgrade process without breaking the hash function.

### Phased Migration & Safety Nets

A “flag day” upgrade is impractical for Ethereum’s scale. A phased approach allows for gradual adoption. Furthermore, a significant portion of users may miss the proactive commitment window. A strictly defined recovery path ensures these users are not permanently locked out, provided they can prove ownership through alternative means (derivation proofs) or endure a security delay.

## Specification

### Protocol Parameters

| Parameter | Description |
| --- | --- |
| MIGRATION_COMMITMENT_CONTRACT | Address of the L1 contract storing Merkle Roots. |
| MIGRATION_FORK_BEGIN | Phase 1 starts. Commitment Layer active. |
| MIGRATION_FORK_MIX | Phase 2 starts. QRBindingTransaction enabled. |
| MIGRATION_FORK_FINAL | Phase 3 starts. Legacy Txs disabled. Commitment contract frozen. |
| DORMANT_ACTIVATE_TIME | Mandatory wait period for Emergency Recovery (Time-lock path). |

### Migration Schedule

The transition occurs in three strict phases:

#### Phase 1: Setup & Commitment

- Period: MIGRATION_FORK_BEGIN to MIGRATION_FORK_MIX.
- Activity:

The MIGRATION_COMMITMENT_CONTRACT is deployed.
- Users sign MigrationIntent off-chain.
- Aggregators submit Merkle Roots to the contract.
- No on-chain upgrades are allowed yet. Legacy transactions function normally.

#### Phase 2: Voluntary Mix

- Period: MIGRATION_FORK_MIX to MIGRATION_FORK_FINAL.
- Activity:

QRBindingTransaction is enabled. Proactive users (e.g., Exchanges, Whales) can upgrade immediately.
- Legacy ECDSA transactions continue to function for non-upgraded accounts.
- The Commitment Layer remains open; users can still register or update commitments.

#### Phase 3: Final Enforcement

- Period: MIGRATION_FORK_FINAL onwards.
- Activity:

Commitment Freeze: The MIGRATION_COMMITMENT_CONTRACT enters a FROZEN state. No new commitments are accepted.
- Mandatory Upgrade: The network strictly enforces “Post-Quantum” rules.

Any transaction from an account that is NOT yet BOUND (upgraded) is rejected, unless it is a valid QRBindingTransaction or QRRecoveryTransaction.
- Users must successfully execute a binding transaction before they can send funds or interact with contracts.

### Commitment Aggregation Layer

This layer handles the users hash based shield registration.

#### Core Data Structure: Migration Intent and AccountInfo

**MigrationIntent**

```python
@dataclass
class MigrationIntent:
    chain_id: uint64
    nonce: uint64
    dest_chain_id: uint64
    random_secret_hashes: List[bytes32]
    threshold: uint8
    ecdsa_signature: bytes
```

**AccountInfo (L2 State)**

```python
@dataclass
class AccountInfo:
    nonce: uint64
    threshold: uint8
    random_secret_root: bytes32    # hash of random_secret_hashes
```

HQRUS allows users to provide multiple random values to enhance security and enables them to specify a threshold in their Intent—i.e., the minimum number of random values required to unlock subsequent QRBinding transactions. This empowers users to adopt diverse off-chain strategies for storing these random values, thereby maximizing security.

#### Aggregation logic

The commitment aggregation layer is a lightweight layer2 system to aggregate commitments of user’s  migration intent and verifiably public the commitments into the ethereum contract. The main workflow is as following:

- Users construct and sign MigrationIntent which represents their intent to add the hash based shield;
- Aggregator (Sequencer)

Upon receiving transactions from users, First checking transaction validity by verifying the classic ecdsa signature;
- Update the layer2 account tree root with the updated account information
- Construct blocks
- Regularly generate zk proof for batches of blocks
- Post public data in form of blobs on ethereum, and zk proof with public inputs(account tree root, blobs hash) into Quantum Key Commitment Registration Contract;

**Quantum Key Commitment Registration Contract**

- Verify the consistency between blobs and blobs hash in the public input;
- Verify the correctness of zk proof
- Store the latest account tree root

### Protocol-Level Account State Extension

The `Account` struct in the World State Trie is logically extended.

```python
@dataclass
class AccountStateHQRUS:
    # Legacy Fields
    nonce: uint64
    balance: uint256
    storage_root: bytes32
    code_hash: bytes32

    # New HQRUS Fields
    qr_pubkey_hash: bytes32
    qr_algorithm: uint8
    is_bound: uint8

```

After `MIGRATION_FORK_FINAL`, The account is in one of the following states:

- ERC-4337 accounts: The protocol considers accounts of this type to be in the BOUND state, meaning they have all already upgraded themselves to quantum-resistant contract code.
- EOA accounts/EIP-7702 accounts: （The code hash is empty, or the code corresponding to the code hash is of the form **0xef0100 || address**.）

UNBOUND_SAFE: nonce = 0 (Safe via Hash Collision).
- DORMANT: nonce > 0and is_bound = False and Not commit in Commitment Registration Contract
- COMMIT:nonce > 0and is_bound = False and Already commit in Commitment Registration Contract
- BOUND: is_bound = True

The following is a helper function to get account status:

```python
def get_account_status(account: AccountStateHQRUS, has_valid_stark_proof: bool) -> AccountStatus:
    # 1. account_type = EOA
    # 2. account_type = EIP7702
    # 3. account_type = CONTRACT
    account_type = parse_account_type(get_code(account.code_hash))

    if account.is_bound or account_type == "CONTRACT":
        return AccountStatus.BOUND

    if account.nonce == 0:
        return AccountStatus.UNBOUND_SAFE

    if has_valid_stark_proof:
        return AccountStatus.COMMIT
    else:
        return AccountStatus.DORMANT
```

### 4. Transaction Types

#### 4.1 QRBindingTransaction (The Standard Path)

Used to bind quantum-resistance keys or codes to accounts.

```python
@dataclass
class QRBindingTransaction:
    # ... Standard Fields ...

    # Payload
    qr_public_key: bytes      # Optional (Native Mode)
    qr_algorithm: uint8
    validation_code: bytes        # Optional (EIP-7702 Mode)

    # Proofs
    stark_proof_of_secrets: bytes # Proves knowledge of pre-images of committed hashes
    legacy_signature: bytes
```

The Execution logic:

```python
def process_qr_binding_tx(tx):
    sender = ecrecover(tx.hash_without_signatures(), tx.legacy_signature)
    public_input_hash = tx.hash_without_stark_proof()
    account = state.get(sender)
    commitment_root = COMMITMENT_CONTRACT.get_root()
    has_valid_proof = verify_bind_stark_proof(public_input_hash, commitment_root, sender, tx.stark_proof_of_secrets)

    account_status = get_account_status(account, has_valid_proof)

    # 2. Authorization Check (The "Gatekeeper")
    if account_status == BOUND:
        # Already bound, just check if keys match (rotation logic if supported)
        pass

    elif block.number  0:
        account.code_hash = keccak(tx.validation_code) # Set Code (AA)
    account.is_bound = True
    state.update(sender, account)
```

- stark_proof_of_secrets:
* Proves knowledge of pre-images of committed hashes and merkle proof to merkle root stored in the commitment registry contract
* To bind the stark_proof_of_secrets with QRBindingTransaction, the transaction hash needs to be a part of public inputs of stark proof

#### 4.2 QRRecoveryTransaction (The Emergency Path)

Used by Dormant account to upgrade to quantum-resistance keys or codes

```plaintext
@dataclass
class QRRecoveryTransaction:
    # ... Standard Fields ...

    # Payload
    qr_public_key: bytes
    qr_algorithm: uint8
    validation_code: bytes

    stark_proof_of_ownership: bytes
    legacy_signature: bytes
```

The execution logic

```python
def process_qr_recovery_transaction(tx: QRRecoveryTransaction):
    sender = ecrecover(tx.hash_without_signatures(), tx.legacy_signature)
    account = state.get(sender)
    public_input_hash = tx.hash_without_stark_proof()
    account_status = get_account_status(account, False)
    if account_status != DORMANT:
        raise Exception("Account must be in DORMANT state to activate QR")

    is_verified = False

    if not tx.stark_proof_of_ownership:
        time_elapsed = current_block_number() - MIGRATION_FORK_FINAL
        if time_elapsed > DORMANT_ACTIVATE_TIME:
            is_verified = True
        else:
            raise Exception("Dormancy period not yet reached")

    else:
        if builtin_stark_verifier(tx.stark_proof_of_ownership, sender, public_input_hash):
            is_verified = True
        else:
            raise Exception("Invalid STARK Proof")

    if is_verified:
        if tx.qr_public_key != "" and is_supported(tx.qr_algorithm):
            account.qr_pubkey_hash = keccak(tx.qr_public_key)
            account.qr_algorithm = tx.qr_algorithm

        if len(tx.validation_code) > 0:
            account.code_hash = keccak(tx.validation_code)

        account.is_bound = True
        state.update(sender, account)
```

- Path 1: Ownership stark proof (Instant)

User provides a stark_proof_of_ownership.
- Circuit Logic: Prove(Hash(Derive(Private_Input)) == Account_Address).
- This proves the user owns the Seed/Pre-image, not just the private key.
- To bind the stark_proof_of_ownership with QRRecoveryTransaction, the transaction hash needs to be a part of public inputs of stark proof
- If valid → Upgrade immediately.

**Path 2: Time Lock (Delayed)**

- Check block.number.
- Requirement: block.number > MIGRATION_FORK_FINAL + DORMANT_ACTIVATE_TIME.
- If valid → Upgrade allowed.
- Note: This path assumes that if an attacker stole the ECDSA key, the legitimate owner would have utilized the Commitment Layer or ownership Proof before the timeout expired.

#### 4.3 EIP 7702

For EIP-7702 accounts, control is exercised either by the EOA’s private key or by its delegated contract, and the EOA’s private key can replace the delegated contract. Therefore, upgrades to EIP-7702 accounts can fully follow the upgrades of the underlying EOA account.

#### 4.4 Account Abstraction (ERC 4337)

For Account Abstraction (AA), the account is fundamentally a contract account rather than an EOA, so its upgrade path cannot follow that of an EOA.

The most straightforward approach is for the AA account to directly upgrade itself to support a quantum-resistant signature algorithm. EntryPoint contract supports batch execute user operations, so the number of txs can be reduced a lot.

### 5. Security Analysis

#### The “Gap” Users (Exposed & No Commitment)

Users who fail to sign a commitment before Phase 3 face higher risks.

- Derivation Path: Secure if the user uses a standard wallet and can generate the proof. The attacker knows the Private Key but not the Seed (Pre-image).
- Time Lock Path: This is the “last resort”. It is risky because a quantum attacker with the Private Key can also wait for the timeout. However, it is included to prevent permanent fund lockup for users who lost their Seed but have their Private Key. We assume the DORMANT_ACTIVATE_TIME allows the ecosystem to potentially intervene or for the user to race (though racing a quantum attacker is difficult). Strong recommendation: Use the Commitment Aggregation Layer.

#### Unexposed Users (nonce=0)

These users are implicitly safe. They can skip the **Commitment Aggregation Layer** and simply send a `QRBindingTransaction` in Phase 3. For these users, a narrow window of vulnerability exists. When these users broadcast their first `QRBindingTransaction`, their ECDSA public key is revealed in the mempool.

A quantum-equipped adversary monitoring the mempool could theoretically derive the private key and broadcast a competing binding transaction with a higher gas fee in the same block (MEV front-running). We assume this risk is mitigated by the speed of block inclusion relative to the time required for quantum derivation, but it remains a non-zero risk factor.

So** it is highly recommended that unexposed users also register in the Commitment Aggregation Layer.** Doing so grants them immediate **Hash-Based Protection**.

## Rationale

### Why a Hash-Preimage “Shield” Instead of Choosing PQC Now?

Ethereum cannot safely hard-fork in a single “flag day” to one PQ signature without high coordination risk and potential cryptographic churn. HQRUS separates two decisions:

1. Authorization mechanism (now): require knowledge of hash preimages committed earlier to authorize an upgrade in the high-risk era.
2. Concrete PQ verification algorithm (later): allow the ecosystem to converge on a mature standard when threat timing is clearer.

This matches the “shield first, upgrade later” approach where the upgrade right is anchored in hash security assumptions rather than ECDSA

### Why a Commitment Aggregation Layer?

If every account committed on-chain directly, cost and UX would be prohibitive. An aggregation layer amortizes costs:

- off-chain collection of intents,
- periodic publication of roots,
- succinct verification via zk proofs posted to L1.

Importantly, the on-chain contract only needs to store a *root* and verify proofs of inclusion/consistency, rather than per-user data.

### Why Freeze Commitments at Phase 3?

Freezing the commitment contract:

- Creates a stable “liability boundary” for which accounts are protected by preimage commitments.
- Prevents adversaries with compromised ECDSA keys from registering new commitments after enforcement begins.
- Makes client behavior deterministic: after MIGRATION_FORK_FINAL, proofs are checked against a fixed commitment state.

### Why Two Recovery Paths?

HQRUS includes “safety nets” to prevent permanent fund loss:

- Proof of derivation (instant): proves ownership beyond the ECDSA key, by showing knowledge of the seed/preimage that derives the address.
- Time lock (delayed, last resort): allows recovery even for cases where derivation proof cannot be generated (non-standard wallets, brain wallets), at the cost of security assumptions and waiting.

This dual-path design explicitly trades off security and recoverability, and the EIP strongly recommends using the commitment layer when possible.

## Backwards Compatibility

- Phase 1 and Phase 2 preserve legacy ECDSA transaction validity for non-upgraded accounts.
- Phase 3 introduces strict rejection of legacy transactions for non-BOUND accounts, with explicit binding and recovery transaction types to transition safely

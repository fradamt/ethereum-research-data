---
source: ethresearch
topic_id: 22714
title: "Fluxe: A Universal Privacy Protocol for Cross-Chain Stablecoin Payments with Programmable Compliance"
author: rahulghangas
date: "2025-07-08"
category: Privacy
tags: [zk-roll-up]
url: https://ethresear.ch/t/fluxe-a-universal-privacy-protocol-for-cross-chain-stablecoin-payments-with-programmable-compliance/22714
views: 1293
likes: 27
posts_count: 20
---

# Fluxe: A Universal Privacy Protocol for Cross-Chain Stablecoin Payments with Programmable Compliance

# Fluxe: A Universal Privacy Protocol for Cross-Chain Stablecoin Payments with Programmable Compliance

## Abstract

We present Fluxe, a universal privacy protocol enabling private stablecoin transfers across multiple blockchain networks with regulatory compliance. The protocol combines hybrid proof architectures (client-side Groth16, server-side SP1), confidential UTXO models with indexed merkle trees, and zk-promises for asynchronous compliance callbacks. The system supports cross-chain private payments with automatic liquidity balancing and programmable payment rails.

## 1. Introduction

Current privacy protocols face the trilemma of privacy, compliance, and cross-chain interoperability. Fluxe solves this through zk-promises integration enabling asynchronous compliance determination without compromising transaction privacy.

## 2. Technical Architecture

### 2.1 Confidential UTXO Model

Each note N is defined as:

N = \{asset\_type, value, owner, \psi, chain\_hint, compliance\_data, lineage\_hash, pool\_id, callbacks\}

The note commitment is computed as:

cm = H(asset\_type \parallel value \parallel owner \parallel \psi \parallel chain\_hint \parallel compliance\_data \parallel lineage\_hash \parallel pool\_id \parallel H(callbacks))

The nullifier derivation prevents double-spending:

nf = H(auth\_secret \parallel \psi \parallel cm)

where auth\_secret is derived from the owner’s private key and \psi is per-note entropy.

### 2.2 Indexed Merkle Trees

Traditional sparse merkle trees require d = 256 hash operations for membership proofs. Fluxe uses indexed merkle trees with sorted linked-list structure reducing this to d = 64 operations.

Each leaf node stores:

leaf = \{value, next\_index, next\_value\}

**Non-membership Proof Implementation**:

Using indexed Merkle trees, non-membership is proven by finding the low nullifier (the sanctioned address with the largest value less than the target address):

\text{NonMembershipProof}(addr, root, proof) =

\begin{cases}
\text{MerkleProof}(low\_addr, root, path) \land \\
low\_addr.value < addr \land \\
(addr < low\_addr.next\_value \lor low\_addr.next\_value == 0)
\end{cases}

where low\_addr = \{value, next\_index, next\_value\} is the sanctioned address entry that the target address would fall after in the sorted list.

The proof consists of:

- Merkle path for node v_i (64 hashes)
- Verification that v_i.next\_value = v_{i+1}
- Range check: v_i ,
    public_inputs: Vec
) -> [u8; 32] {
    for (proof, inputs) in groth16_proofs.zip(public_inputs) {
        groth16::verify(proof, inputs);
    }

    let new_nullifiers = extract_nullifiers(public_inputs);
    indexed_merkle_tree::batch_insert(old_root, new_nullifiers)
}
```

### 2.4 Basic Client-Side Sanctions Screening

For basic compliance, the most fundamental requirement is proving that transaction addresses are not sanctioned. This is implemented through client-side zero-knowledge proofs against a commitment to flagged addresses.

**Sanctions List Commitment**:

The protocol maintains a Merkle tree commitment to sanctioned addresses:

sanctions\_root = \text{MerkleRoot}(\{addr_1, addr_2, ..., addr_n\})

where each addr_i is a sanctioned address hash.

**Basic Sanctions Screening Circuit**:

```auto
Public: sanctions_root, tx_valid
Private: sender_addr, recipient_addr, sanctions_proof_sender, sanctions_proof_recipient
Constraints:
  - NonMembershipProof(sender_addr, sanctions_root, sanctions_proof_sender)
  - NonMembershipProof(recipient_addr, sanctions_root, sanctions_proof_recipient)
  - tx_valid = (sender_proof_valid ∧ recipient_proof_valid)
```

> NOTE:  While basic sanctions screening happens client-side, the system’s true power lies in its ability to enforce compliance retroactively through callbacks. See Section 3.10 for how assets can be frozen post-transaction if compliance issues are discovered.

### 2.5 Cross-Chain Bridge Protocol

Bridge contracts maintain the invariant:

\sum_{i} deposits_i = \sum_{j} withdrawals_j + \sum_{k} liquidity\_k

For cross-chain operations, the protocol coordinates:

1. Source chain withdrawal: Burn note, emit event with proof
2. Message passing: CCTP (for USDC) or LayerZero (for others)
3. Destination chain deposit: Mint equivalent note after verification

The liquidity routing algorithm selects optimal paths based on:

cost(path) = gas\_cost + bridge\_fee + time\_penalty \cdot delay

This is done through external keepers that help pay gas and perform this actions on observed events, although the balancing functions are permissionless and can be called by anybody.

### 2.6 Integration with Twine Multi-Settlement Network

Fluxe operates as an application layer on top of Twine’s multi-settlement infrastructure, leveraging its light client architecture for cross-chain functionality:

- Light Client Verification: Twine maintains light clients for each supported chain to verify state transitions
- Cross-Chain Proofs: State updates are verified through light client proofs before acceptance on remote chains
- Asynchronous Settlement: Each chain processes Fluxe state updates upon light client verification
- Trust-Minimized Bridges: Asset transfers verified through light client state proofs

This architecture allows Fluxe to maintain privacy while achieving cross-chain interoperability through cryptographic verification rather than consensus.

```auto
┌────────────────────────────────────────────────────────┐
│                      TWINE                             │
│                                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │                   FLUXE                          │  │
│  │                                                  │  │
│  │  • Nullifier Tree (IMT)                          │  │
│  │  • Commitment Tree                               │  │
│  │  • Transfer Proofs (Groth16)                     │  │
│  │  • Compliance Callbacks                          │  │
│  │  • SP1 Verification                              │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↑                              │
│                    Light Clients                       │
└─────────────────────────┼──────────────────────────────┘
                     ↓
            ┌──────────┐    ┌──────────┐
            │ Ethereum │    │  Solana  │
            │  Bridge  │    │  Bridge  │
            └──────────┘    └──────────┘
            (Deposit/         (Deposit/
            Withdraw)         Withdraw)
```

## 3. zk-Promises Integration for Asynchronous Compliance

### 3.1 zk-Objects Foundation

Fluxe extends the zk-objects model where each user maintains a compliance object containing state and a unique nullifier for updates. The object structure:

obj = \{state, serial, cbList\}

where state contains compliance information, serial is a unique identifier preventing replay attacks, and cbList maintains pending callbacks.

The object commitment:

cm_{obj} = \text{Commit}(state \parallel serial \parallel H(cbList), r_{obj})

Object updates follow copy-on-write semantics: creating new commitments with fresh nullifiers while proving valid state transitions.

### 3.2 Dual Bulletin Board Architecture

The system maintains two global bulletin boards:

**Object Bulletin Board (bb_{obj})**: Stores object commitments using Merkle trees for membership proofs. The tree root rt_{obj} represents all valid object states.

**Callback Bulletin Board (bb_{cb})**: Stores callback invocations requiring both membership and non-membership proofs. Uses complement set approach partitioning unused ticket space into ranges.

Non-membership proofs implemented through signed range sets:

\text{NonMember}(ticket) \iff \exists (a,b) \in \text{RangeSet}: a < ticket < b

### 3.3 Callback Creation Protocol

Users create compliance callbacks during transaction execution through the \text{ExecMethodAndCreateCallback} algorithm:

**Step 1**: Generate rerandomized ticket from compliance provider’s public key:

ticket = pk_{compliance} \cdot r^{sk_{user}} \mod p

where r is cryptographically random and sk_{user} is the user’s signing key.

**Step 2**: Create callback entry with expiration and encryption:

cb_{entry} = \{ticket, exp\_time, enc\_key, method\_id\}

where enc\_key = \text{KDF}(user\_secret, ticket) for per-callback encryption.

**Step 3**: Update object with new callback list:

obj'.cbList = obj.cbList \parallel cb_{entry}

obj'.serial = \text{Fresh}()

**Step 4**: Generate ZK proof of valid transition:

```auto
Public: cm_old, cm_new, method_id
Private: obj_old, obj_new, r_old, r_new, cb_entry
Constraints:
  - cm_old = Commit(obj_old, r_old)
  - cm_new = Commit(obj_new, r_new)
  - obj_new.cbList = obj_old.cbList || cb_entry
  - obj_new.state = ValidTransition(obj_old.state, method_id)
```

### 3.4 Callback Invocation and Processing

Compliance providers invoke callbacks by posting to bb_{cb}:

invocation = \{ticket, \text{Enc}_{enc\_key}(args), timestamp, \sigma\}

where \sigma is a signature over (ticket, args, timestamp) using the ticket as public key.

Users process callbacks through \text{ScanOne} algorithm:

**Step 1**: Iterate through pending callbacks in cbList

**Step 2**: Check membership in bb_{cb}:

\exists invocation \in bb_{cb}: invocation.ticket = cb_{entry}.ticket

**Step 3**: If found and valid:

- Decrypt arguments: args = \text{Dec}_{enc\_key}(invocation.args)
- Execute method: state' = method(state, args)
- Remove from callback list: cbList' = cbList \setminus \{cb_{entry}\}

**Step 4**: Generate proof of correct processing:

```auto
Public: cm_old, cm_new, timestamp
Private: obj_old, obj_new, args, cb_entry
Constraints:
  - ValidDecryption(cb_entry.enc_key, invocation.args, args)
  - obj_new.state = ExecuteMethod(obj_old.state, args)
  - obj_new.cbList = obj_old.cbList \ {cb_entry}
  - timestamp  80:
    state.compliance_level = max(0, state.compliance_level - 1)
    state.transaction_limits.daily *= 0.5

  state.risk_score = risk_assessment
  return state
```

**Jurisdiction Compliance Method**:

```auto
method_jurisdiction(state, args):
  user_jurisdiction = args.jurisdiction
  allowed_operations = args.permitted_ops

  state.jurisdiction_flags |= (1 << user_jurisdiction)

  if "HIGH_VALUE_TX" not in allowed_operations:
    state.transaction_limits.daily = min(state.limits.daily, 10000)

  return state
```

### 3.8 Efficient Callback List Management

Callback lists use hash-chain representation for efficiency:

h_\ell := H(H(...H(H(\epsilon), cb_1), cb_2)...), cb_n)

**Append Operation** (O(1)):

h'_\ell = H(h_\ell, cb_{new})

**Removal Operation** during scanning:

State machine encoding enables amortized O(1) removal by rebuilding hash chain incrementally.

**Batch Processing**:

For k callbacks, proving complexity is O(k \log k) using recursive proof composition.

### 3.9 Privacy-Preserving Compliance Attestations

Users generate ZK proofs demonstrating compliance without revealing transaction details:

**Enhanced Sanctions Compliance Circuit**:

```auto
Public: attestation_hash, time_period
Private: tx_history, sanctions_root, compliance_callbacks
Constraints:
  - ∀ tx ∈ tx_history: tx.timestamp ∈ time_period
  - ∀ tx ∈ tx_history: CheckSanctions(tx.counterparty, sanctions_root) = CLEAR
  - ∀ cb ∈ compliance_callbacks: cb.result = "SANCTIONS_CLEAR"
  - attestation_hash = H(tx_history || compliance_callbacks)
```

**Multi-Jurisdiction AML Circuit**:

```auto
Public: jurisdictions[], thresholds[], attestation
Private: transactions, amounts, callback_results
Constraints:
  - ∀ j ∈ jurisdictions:
      Σ(amounts | tx.jurisdiction = j) ≤ thresholds[j]
  - ∀ result ∈ callback_results: result.aml_status = "COMPLIANT"
  - attestation = CommitToCompliance(transactions, callback_results)
```

**Source of Funds Verification**:

```auto
Public: legitimacy_threshold, source_categories
Private: fund_sources, verification_callbacks, lineage_proof
Constraints:
  - ∀ source ∈ fund_sources: source.category ∈ source_categories
  - ∀ verification ∈ verification_callbacks:
      verification.source_legitimacy ≥ legitimacy_threshold
  - ValidLineage(lineage_proof, fund_sources)
```

### 3.10 Post-Transaction Compliance Enforcement

A key innovation of the callback system is enabling retroactive compliance actions. Unlike traditional systems that must block transactions upfront, Fluxe allows transactions to proceed while maintaining the ability to freeze or recover assets if compliance issues are discovered later.

#### 3.10.1 Asset Freezing Mechanism

When a transaction is flagged post-facto, compliance callbacks can freeze the recipient’s assets:

```auto
method_freeze_assets(state, args):
    freeze_reason = args.reason  // "SANCTIONS_HIT", "AML_FLAG", etc.
    freeze_timestamp = args.timestamp // block number
    authority = args.compliance_authority
    if verify_authority(authority):
        state.frozen = true
        state.freeze_reason = freeze_reason
        state.freeze_time = freeze_timestamp
        state.compliance_level = 0
        // Prevent all outgoing transfers
        state.transaction_limits = {
            daily: 0,
            monthly: 0,
            yearly: 0
        }
    return state
```

#### 3.10.2 Advantages of Post-Transaction Enforcement

**1. Better User Experience**:

- Legitimate transactions aren’t delayed by compliance checks
- Users can transact immediately while compliance runs asynchronously
- Reduces false positives that block legitimate users

**2. More Comprehensive Screening**:

- Can use advanced ML models that take longer to run
- Cross-reference with multiple databases without blocking transactions
- Perform deep chain analysis that would be too slow for real-time

**3. Network Effects**:

- Bad actors can be identified through transaction patterns
- Entire clusters of related addresses can be frozen together
- Compliance improves over time as more data is collected

#### 3.10.3 Recovery and Unfreezing

Assets can be unfrozen if compliance checks clear:

```auto
method_unfreeze_assets(state, args):
    clearance_proof = args.proof
    reviewing_authority = args.authority
    if verify_clearance(clearance_proof, reviewing_authority):
        state.frozen = false
        state.compliance_level = determine_new_level(clearance_proof)
        state.transaction_limits = standard_limits(state.compliance_level)
    return state
```

#### 3.10.4 Time-Bounded Compliance

To balance compliance with usability, callbacks have expiration times:

- Initial Grace Period: 24-48 hours for basic compliance checks
- Extended Review: Up to 30 days for complex cases
- Auto-Release: If no callback invoked within expiry, transaction is considered cleared

This prevents indefinite asset freezing while giving compliance providers reasonable time to act.

## 4. Programmable Payment Rails

### 4.1 Recurring Payment Protocol

Recurring payments implemented through zk-promises scheduling:

RecurringPayment = \{recipient, amount, frequency, max\_payments, conditions\}

The payment schedule creates callbacks at intervals:

callback\_times = [start\_time + i \cdot frequency \mid i \in [0, max\_payments]]

Each callback verifies:

- Service conditions met: \text{VerifyConditions}(service\_state, conditions) = \text{true}
- Payment authorization valid: current\_time \leq start\_time + max\_payments \cdot frequency
- Sufficient balance: user\_balance \geq amount

### 4.2 Payment Streaming

Continuous payment streams with rate limiting:

Stream = \{recipient, rate, duration, start\_time\}

Available amount at time t:

available(t) = \min(rate \cdot (t - start\_time), total\_amount)

Withdrawal constraints:

\sum_{i} withdrawn_i \leq available(current\_time)

### 4.3 Conditional Payments

Multi-party escrow with programmable conditions:

ConditionalPayment = \{parties, conditions, timeout, resolution\_method\}

Release conditions encoded as circuit constraints:

```auto
Public: condition_hash, resolution
Private: condition_data, signatures
Constraints:
  - H(condition_data) = condition_hash
  - VerifyCondition(condition_data) = resolution
  - VerifySignatures(parties, signatures)
```

## 5. Security Analysis

### 5.1 Privacy Guarantees

**Unlinkability**: Given note commitments cm_1, cm_2, without knowledge of secrets, the probability of linking them is negligible:

\Pr[\text{Link}(cm_1, cm_2) = \text{true} \mid \text{no secrets}] \leq \text{negl}(\lambda)

**Amount Confidentiality**: Transaction amounts remain computationally hidden under the commitment scheme’s hiding property.

**Temporal Privacy**: Transaction timing unlinkable to user identity through batching with anonymity set size |A| \geq 2^k for security parameter k.

### 5.2 Compliance Integrity

**Callback Authenticity**: Signatures prevent forgery with security reduction to underlying signature scheme.

**Evasion Resistance**: Users cannot transact without processing callbacks due to state machine constraints.

**Audit Trail**: Complete compliance history maintained with selective disclosure through ZK proofs.

### 5.3 Cross-Chain Consistency via light clients

**Global State**: All chains maintain consistent view of global nullifier set N_{global} and note set C_{global} through Twine’s multi settlement.

**State Verification**:

```auto
Chain A → State proof → Verified by Light Client on Twine → Generate execution proof → Verify on Chain B → Update State
```

Since Fluxe operates entirely on Twine, state consistency is straightforward:

- Single State Tree: One global nullifier set and commitment tree
- Atomic Updates: All state transitions are atomic within Twine
- No Synchronization: No cross-chain state to synchronize
- Instant Finality: Transfers are final immediately on Twine

The only cross-chain interaction within Fluxe is verifying deposit/withdrawal events through Twine’s light clients.

## 6. Implementation Details

### 6.1 Circuit Constraints

The transfer circuit has constraint count:

- Merkle proof verification: 64 \times \text{hash_constraints}
- Nullifier computation: \text{hash_constraints}
- Value conservation: 1 constraint
- Range checks: 2 \times \log_2(\text{max_value}) constraints

### 6.2 Finality

Finality on settlement layer: Expected E[\text{finality}] = \max_i (E[\text{finality}_i] + E[\text{batch_posting}_i]) where i ranges over involved chains.

## 7. Comparison with Existing Protocols

| Protocol | Privacy | Compliance | Cross-Chain |
| --- | --- | --- | --- |
| Tornado Cash | ✓ | ✗ | ✗ |
| Aztec | ✓ | Partial | ✗ |
| Fluxe | ✓ | ✓ | ✓ |

## 8. Future Work

**Recursive SNARKs**: Transition to Halo2/Nova for transparent setup and better recursion.

**Sharded State**: Parallel processing with state sharding for higher throughput.

**Advanced Compliance**: ML-based risk assessment with privacy-preserving inference.

**Cross-Chain Messaging**: Integration with additional bridge protocols and interoperability standards.

## 9. Conclusion

Fluxe provides a comprehensive solution to the privacy-compliance-interoperability trilemma through novel integration of zk-promises with cross-chain infrastructure.

## References

1. Kattis, A. et al. (2024). “zk-Promises: Making Zero-Knowledge Objects Accountable”
2. Buterin, V. (2022). “Privacy Pools”
3. Succinct Labs (2024). “SP1: The Performant, Open-Source ZK Virtual Machine”
4. Moore, C. & Gandhi, S. (2024). “L2 Ethereum ZK Rollup for Private and Compliant Transactions”
5. Circle (2023). “Cross-Chain Transfer Protocol (CCTP) Documentation”
6. LayerZero (2023). “Omnichain Fungible Token (OFT) Standard”
7. Ioanna Tzialla, Abhiram Kothapalli, Bryan Parno, and Srinath Setty (2023). Transparency dictionaries with succinct proofs of correct operatio

## Replies

**MicahZoltu** (2025-07-09):

None of your LaTeX is rendering here.  I have seen others include LaTeX stuff so I assume it is possible, but you may need to change formatting to work with this forum.

---

**MicahZoltu** (2025-07-09):

It appears that asset movement needs to be approved by “Compliance Providers”.  Since those compliance providers essentially have a backdoor to the whole system, it seems that it would be much easier to just use a system closer to the TradFi model where you have a centralized database owned by the “Compliance Provider”.

Also, if someone has a backdoor then it isn’t a private system and I think it is incorrect to call it that.

Separately, it would be useful to include a sequence diagram showing how the information flows between user, “compliance provider”, and the blockchain.  Especially what information is revealed to each party.

---

**rahulghangas** (2025-07-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> None of your LaTeX is rendering here. I have seen others include LaTeX stuff so I assume it is possible, but you may need to change formatting to work with this forum.

I’ll look into correcting this

---

**rahulghangas** (2025-07-09):

Thanks for the feedback! There are some important misconceptions here that I’d like to clarify:

## 1. Compliance providers do NOT approve transactions

The system uses a “trust but verify” model - transactions proceed immediately without any approval. Compliance providers can only invoke callbacks *after* transactions complete, and only if issues are discovered. This is fundamentally different from TradFi where every transaction requires pre-approval.

## 2. There is no backdoor

Compliance providers cannot:

- See transaction details (amounts, recipients)
- Move or steal funds
- Block transactions from happening
- Access private keys or notes

They can only:

- Invoke callbacks that users must process
- Freeze assets if compliance violations are found
- Request attestations about transaction properties

The cryptography ensures they learn nothing beyond what users explicitly prove.

I would recommend reading [zk-promises](https://eprint.iacr.org/2024/1260.pdf) paper for a better understanding on how these callbacks work. So yes, this is still a private protocol because privacy is preserved for all relevant information

---

**MicahZoltu** (2025-07-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/rahulghangas/48/9738_2.png) rahulghangas:

> Compliance providers cannot:
>
>
> Block transactions from happening
>
>
> They can only:
>
>
> Freeze assets if compliance violations are found

These two things sound like they are in direct contradiction to each other.

---

**rahulghangas** (2025-07-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> These two things sound like they are in direct contradiction to each other.

Compliance callbacks are basically proofs that clients need to create on request ex post facto (ie, after the transaction is done). The new (recipient) note is freezed from being spent

---

**MicahZoltu** (2025-07-09):

What happens if Alice deposits X, then transfers to Bob, Bob then transfers to Carol, and then the compliance provider flags Alice’s deposit as blocked?  Is Carol’s money frozen?

---

**rahulghangas** (2025-07-12):

You’re right. Under the current model, if the callback gets triggered and posted to the bulletin after the funds are transferred to C, then funds get frozen for C. There’s ways to get around it, for eg. enforcing on the sequencer level (since the sequencer is centralized) that checks need to be satisfied asynchronously before the next transfer is done, which can be done quite quickly without affecting user experience. This approach obviously sacrifices censorship resistance.

There’s various other approaches that we are considering with varied levels of decentralization, at the cost of increasing complexity of the protocol.

---

**MicahZoltu** (2025-07-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/rahulghangas/48/9738_2.png) rahulghangas:

> This approach obviously sacrifices censorship resistance.

The system you are describing is not censorship resistant at all, it is explicitly designed to censor.  It seems that since this design has already thrown out censorship resistance, you might as well at least make it so the censorship occurs against the correct person.

---

**rahulghangas** (2025-07-13):

Again, that was just an example if you read my comment again. You’re selectively quoting text and taking it out of context.

> There’s various other approaches that we are considering with varied levels of decentralization, at the cost of increasing complexity of the protocol.

Did you read the above by any chance?

> you might as well at least make it so the censorship occurs against the correct person.

This is exactly how banks work with modern protocols for instant settlement. Not all checks can be done proactively so often funds are frozen after transfer. It’s not possible to do these checks upfront in our protocol because we’ll have to ask the user to create proofs for all arbitrary checks, which becomes very expensive from a time and resource perspective.

Also, re your first comment

> It appears that asset movement needs to be approved by “Compliance Providers”. Since those compliance providers essentially have a backdoor to the whole system, it seems that it would be much easier to just use a system closer to the TradFi model where you have a centralized database owned by the “Compliance Provider”.
> Also, if someone has a backdoor then it isn’t a private system and I think it is incorrect to call it that.
> Separately, it would be useful to include a sequence diagram showing how the information flows between user, “compliance provider”, and the blockchain. Especially what information is revealed to each party.

Would also be great if you could acknowledge that your comments were premature and uninformed, and the system actually implements privacy. It’s great if you’re asking questions, but at least acknowledge my answers before a follow up

---

**MicahZoltu** (2025-07-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/rahulghangas/48/9738_2.png) rahulghangas:

> This is exactly how banks work with modern protocols for instant settlement.

The way banks work (censoring, seizing, and freezing people’s money) is exactly the thing that many of us think needs to end.  There are people all around the world trying to put a stop to this behavior via legal and legislative approaches, and those of us building cryptocurrencies are trying to put a stop to it by providing an alternative where that cannot happen.

If your goal is to build something modeled off of the way banks work that is fine, but it *is* censorship if some third party can decide who is or isn’t allowed to transfer money to who, or can seize or freeze funds of anyone.

---

**rahulghangas** (2025-07-14):

Can you define compliance for me?

---

**rahulghangas** (2025-07-14):

And yes, we are trying to build a compliant system here while adding privacy guarantees, which is strictly better than banks. Adoption comes through integration, not through rebellion

---

**boris-kolar** (2025-07-23):

This is useless shit. The key point of crypto is PERMISSIONLESS nature of transactions.

---

**rahulghangas** (2025-07-23):

Stablecoins aren’t permissionless. Circle, Tether and others can censor addresses at will, so I don’t think your argument applies here.

Also, would prefer if you can comment in a civil tone, else feel free to move off this discussion

---

**boris-kolar** (2025-07-23):

There are some permissionless stablecoins (DAI, for example). Shitcoins like USDC/USDT should not be called cryptocurrency (they have more in common with CBDC than a cryptocurrency).

---

**MicahZoltu** (2025-07-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/rahulghangas/48/9738_2.png) rahulghangas:

> Stablecoins aren’t permissionless. Circle, Tether and others can censor addresses at will, so I don’t think your argument applies here.
>
>
> Also, would prefer if you can comment in a civil tone, else feel free to move off this discussion

I agree with you on the tone, we should keep things civil.  I disagree that we should be looking at circle, tether, etc. as targets of what we want to build.  Those things exist because we have a permissionless system and we cannot stop them from existing.  Their existence does not imply endorsement.

---

**rahulghangas** (2025-07-23):

Fair point, was probably a strawman to compare permissiveness of stablecoins with a protocol. However, if historical and current events have taught us something, governments can arbitrarily call a protocol a money transmitter regardless of whether it’s a permissionless protocol or not. Fluxe is a permissionless protocol in most aspects, the only thing the compliance operator can impose is the requirement to prove certain assertions without revealing anything else about the transaction. This is no different from a smart contract enforcing a list of bad actors from not being able to interact with it.

I personally am of the opinion that this is a good tradeoff to have while still enjoying most of the properties that blockchains give you and regulatory arbitrage that crypto allows, while adding privacy on top of it.

---

**MicahZoltu** (2025-07-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/rahulghangas/48/9738_2.png) rahulghangas:

> I personally am of the opinion that this is a good tradeoff to have while still enjoying most of the properties that blockchains give you and regulatory arbitrage that crypto allows, while adding privacy on top of it.

I suspect you will find a lot of disagreement from the cryptocurrency community on this tradeoff, especially the people who have been involved for a while.  The original point cryptocurrencies tried to solve is exactly the problem of oppressive governments freezing and seizing people’s assets.  Blockchains gave us a way to have online currency that was resistant to any form of participation censorship.

Any system that implements censorship features on a blockchain (including USDC, USDT, etc.) will get a lot of pushback, as it goes against the core ethos that underlies the entire purpose of blockchains (censorship resistance).


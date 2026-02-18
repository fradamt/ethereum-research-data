---
source: magicians
topic_id: 27408
title: "Toward Comparable PQ Signature Benchmarks on EVM: Surface Taxonomy + Shared XOF/Test Vector Suite"
author: pipavlo82
date: "2026-01-09"
category: EIPs > EIPs interfaces
tags: [erc, evm, wallet]
url: https://ethereum-magicians.org/t/toward-comparable-pq-signature-benchmarks-on-evm-surface-taxonomy-shared-xof-test-vector-suite/27408
views: 119
likes: 20
posts_count: 22
---

# Toward Comparable PQ Signature Benchmarks on EVM: Surface Taxonomy + Shared XOF/Test Vector Suite

I think the PQ-on-EVM discussion is currently missing one “boring but decisive” piece: a way to make benchmarks comparable across projects (Falcon vs ML-DSA vs Dilithium) without accidentally measuring different assumptions.

Why this matters

We often compare “gas per verify” while silently mixing:

different security levels (128/192/256-bit targets),

different verification surfaces (pure verify vs ERC-1271 vs AA validateUserOp vs end-to-end handleOps),

different hash/XOF wiring (FIPS SHAKE vs Keccak-CTR / Keccak-PRNG conventions).

This makes results non-comparable and can mislead design decisions.

Proposal (algorithm-agnostic)

(1) Surface taxonomy: define what is being measured

Benchmarks should be tagged by surface, e.g.:

sig::app_verify (pure in-EVM verification)

sig::app_erc7913_adapter (ERC-7913 surface for wallets/AA/L2)

sig::aa_validateUserOp / sig::aa_handleOps (end-to-end AA surfaces)

sig::protocol_precompile_assumption (protocol-facing path; e.g., EIP-7932-style)

This prevents mixing “app-facing” and “protocol-facing” costs in the same discussion.

(2) Shared XOF/hashing wiring vector suite

Given the modular seam approach (keep both versions), I suggest two explicit lanes:

FIPS lane: SHAKE{128,256}-style wiring (NIST-aligned)

EVM lane: Keccak-CTR / Keccak-PRNG wiring (gas-driven pure-EVM path)

The key is to make wiring explicit so projects don’t benchmark different conventions by accident.

Concrete ask

Would contributors be open to:

agreeing on a minimal JSON schema for XOF (and where applicable hash-to-point) test vectors, with a lane identifier (fips vs evm), and

tagging benchmark results by surface so we stop mixing incompatible measurement scopes?

If there is interest, I can post a starter schema + small vector set + a minimal runner/provenance format.

## Replies

**Madeindreams** (2026-01-10):

This is a really good framing. I agree the discussion is currently mixing *measurement surfaces* and *assumptions*, which makes comparisons noisy at best and misleading at worst.

One additional angle that may be worth making explicit if we go down this path is **key storage realism**.

If we’re defining benchmark surfaces and wiring lanes, I’d love to see **key material constraints** acknowledged as well — specifically whether a scheme can realistically be backed by **TPM-resident private keys**.

From a deployment and security standpoint, this matters because:

- Some curves / schemes can be generated, stored, and used entirely inside a TPM (or similar secure enclave).
- Others require exporting private key material into software memory, which fundamentally changes the threat model — regardless of gas cost.

So alongside:

- surface taxonomy (app vs AA vs protocol), and
- wiring lanes (FIPS vs EVM),

it may be useful to tag whether a benchmark assumes:

- TPM / HSM–compatible private key storage, or
- software-resident keys.

This doesn’t need to be prescriptive, but making the assumption explicit would help avoid optimizing for schemes that look great in gas benchmarks but can’t be deployed with strong hardware-backed key isolation.

In other words: comparability isn’t just about gas and hashes — it’s also about whether the security model survives contact with real-world key management.

If there’s interest, I think this fits naturally as an additional annotation rather than a new axis, similar to how you’re proposing surface tagging.

Happy to elaborate if useful.

---

**pipavlo82** (2026-01-10):

Thanks — this is a great point, and I agree it should be captured explicitly.

I like the framing “key storage realism” as an annotation (not a new axis), because it affects deployability / threat model but doesn’t change the on-chain verifier cost directly.

Concretely, I think we can add a small, explicit tag to each benchmark row, e.g. key_storage_assumption with a minimal vocabulary:

resident_hsm_tpm: private key never leaves a TPM/HSM/SE; signing via device API

sealed_exportable: key is at-rest protected (enclave-backed / keystore), but can be exposed to software memory during signing

software_exportable: key material is managed in software (file/memory), no hardware isolation assumption

Two notes to keep it honest:

This tag is orthogonal to the “verification surface” (pure verify vs ERC-1271 vs AA validateUserOp vs end-to-end handleOps). It’s simply making the off-chain key management assumption explicit so we don’t accidentally optimize for a deployment model that won’t be used in practice.

We don’t need to decide which schemes “support TPM” in the benchmark spec itself — the dataset can record the declared assumption and (optionally) a short notes field with the signing setup used.

If you’re willing: do you have a preferred taxonomy here (TPM vs HSM vs Secure Enclave vs passkey/WebAuthn-style APIs), or examples where this mismatch caused misleading comparisons? I’d love to incorporate that into the “assumptions” section so the benchmark stays rigorous.

---

**Madeindreams** (2026-01-10):

Happy to elaborate — this question comes directly from deployment experience rather than theory.

In our case, the core constraint was exactly what you’re pointing at: **the TPM does not natively support the Ethereum curve**, so true TPM-resident secp256k1 signing wasn’t available.

The approach we ended up with is:

- A symmetric encryption key is generated and sealed inside the TPM (PCR-bound).
- The Ethereum private key exists only in encrypted form at rest, encrypted under that TPM-sealed key.
- For signing, the key is decrypted ephemerally in process memory, used, and the memory is explicitly cleared immediately afterward.
- The sealing key itself never leaves the TPM, and the private key is never exportable in plaintext at rest.

Architecturally, this allowed us to operate a wallet that supports:

- a standard EOA path,
- a TPM-sealed encrypted key path, and
- an account-abstraction (AA) layer on top.

In practice, this gives users **maximum flexibility** (EOA compatibility, AA features when desired) while still achieving **meaningful hardware-backed protection** against key exfiltration and offline attacks.

From a taxonomy standpoint, I’d describe this as something like:

`key_storage_assumption = tpm_sealed_software_signing`

It’s not equivalent to native TPM signing, but it’s materially stronger than a purely software-managed key, and often the *best achievable* security posture given curve and API constraints today.

This is why I think making key-storage assumptions explicit is valuable: some schemes benchmark extremely well but implicitly assume key handling models that don’t survive contact with real-world deployment.

If useful, I’m happy to help refine the vocabulary further — especially to distinguish:

- TPM-resident signing (where available),
- TPM-sealed keys with ephemeral in-memory use,
- and fully software-exportable keys.

That distinction doesn’t change on-chain verifier cost, but it absolutely changes the security and deployability story.

---

**pipavlo82** (2026-01-10):

This is excellent — thank you. I agree this should be an annotation, not a new measurement surface: it doesn’t change on-chain verifier gas, but it does change deployability + threat model realism.

I’ll add a key_storage_assumption field alongside surface (app / AA / protocol) and wiring_lane (FIPS SHAKE vs EVM Keccak-style). Proposed enum (v0):

tpm_resident_signing

tpm_sealed_ephemeral_use (TPM-sealed at rest, ephemeral decrypt in-process, explicit zeroization)

software_exportable_key

If you (or others) have a better vocabulary split (e.g., HSM vs TPM vs TEE), I’m happy to iterate — the goal is comparability without prescribing a single operational model.

---

**Madeindreams** (2026-01-10):

This looks spot on to me — the enum maps cleanly to how these systems are actually deployed.

`tpm_sealed_ephemeral_use` in particular matches the model we use in practice today (TPM-sealed at rest, ephemeral in-process decrypt for signing, explicit zeroization), driven by the lack of native secp256k1 support in TPMs.

We’ve found this enables a flexible wallet architecture (EOA compatibility + AA layering) while still providing meaningful hardware-backed protection against offline key exfiltration.

I agree this belongs as an annotation, not a new surface. Your proposed split feels right for v0; finer distinctions (TPM vs HSM vs TEE) can live in notes if needed later.

If helpful, I’m also happy to help implement or validate this — we’re already working with this model in an OSS wallet project and could use it as a concrete reference or demo.

---

**pipavlo82** (2026-01-10):

Thanks — this is very actionable.

I’ll land key_storage_assumption as a first-class annotation (not a new surface) with the v0 enum we discussed (tpm_resident_signing, tpm_sealed_ephemeral_use, software_exportable) and keep finer TPM/HSM/TEE nuances in notes for now.

If you’re comfortable sharing the OSS wallet reference (repo/docs), I’d love to add it under a small “reference implementations” section and include one example dataset row tagged tpm_sealed_ephemeral_use (TPM-sealed at rest + ephemeral in-process decrypt + explicit zeroization), so people don’t compare threat models implicitly.

Happy to iterate on the vocabulary with you to keep it descriptive rather than prescriptive.

---

**pipavlo82** (2026-01-10):

Quick follow-up: I wired `key_storage_assumption` end-to-end (spec + parser + dataset).

It’s now an **optional annotation axis** (orthogonal to on-chain gas) so benchmark rows can be tagged as `tpm_resident_signing` / `tpm_sealed_ephemeral_use` / `software_exportable` (default `unknown`).

This should help prevent apples-to-oranges comparisons where “software exportable keys” get compared to “TPM-sealed ephemeral use” under the same threat model label.

If you can point me to a concrete OSS reference implementation, I’ll add it under “reference implementations” and start tagging rows accordingly.

---

**Madeindreams** (2026-01-10):

This is great work — and honestly very aligned with where I was already planning to go.

I’m happy to share my work and adapt it to this direction. Post-quantum authorization on EVM has been on my roadmap for a while; I just wasn’t ready yet to push PQ verification all the way into an AA validation path. Since you’re actively building toward comparable benchmark surfaces, this is something I can now adapt quite naturally.

A bit of context on my side:

QuantumAuth already uses **post-quantum signatures in its ZK-based authentication flow**, but today those signatures terminate off-chain. The next logical step is exactly what you’re describing: moving PQ (or hybrid PQ + secp256k1) verification into an **AA contract policy / validation surface** so it can be measured, compared, and eventually standardized.

Importantly, QuantumAuth is **not just a wallet**. It’s a full identity + authorization infrastructure:

- QA Client (develop branch)
Local wallet / identity agent, hardware-rooted (TPM today). Keys are never exportable; signing uses sealed keys with ephemeral in-memory material only.
- QA Bridge (browser extension)
What users perceive as the “wallet” (MetaMask-like UX), but it holds zero keys. It only bridges dapps ↔ connectors ↔ the local QA client.
- QA Privacy Connector
A privacy-first connector that avoids wallet fingerprinting and metadata leakage (no passive domain correlation, no silent identity reuse).
- QA Backend
Stores public device keys only, enabling a user identity to be reused safely across multiple domains without central custody.
- QA SDK
Low-friction developer tooling to integrate QA for authentication and authorization without rewriting app logic.

Most of this is publicly described here:

https://quantumauth.io

(docs are still WIP, but the architecture and threat model are already laid out)

I’d be very happy to:

- Adapt my current AA contract + policy layer to validate PQ (or hybrid) signatures
- Tag and benchmark it using the same surface taxonomy you’re proposing (ERC-1271 / validateUserOp, etc.)
- Explicitly declare key storage assumptions (TPM sealed + ephemeral use), which QuantumAuth already follows in practice

Beta is planned for **next week** (Linux & Windows). Android is likely next, followed by Secure Enclave support for macOS / iOS.

I think aligning real-world infra (hardware-rooted keys, privacy-preserving connectors) with a shared PQ benchmarking methodology is exactly what this space needs. Happy to collaborate and contribute concrete data instead of hypothetical numbers.

Looking forward to comparing notes.

---

**pipavlo82** (2026-01-10):

Thanks — this is extremely helpful, and I agree the enum you suggested maps cleanly to real deployments.

I’ll keep `key_storage_assumption` as an annotation (not a new surface) for v0, with the coarse split:

`tpm_resident_signing` / `tpm_sealed_ephemeral_use` / `software_exportable`, and finer TPM/HSM/TEE details in notes.

Your offer of a concrete OSS reference would be very valuable. If you’re open to it, could you point me to the specific repo(s)/branch where the AA contract + policy/validation layer lives?

Next step on my side: I can add a “Reference implementations” section and a vendor runner entry so we can tag benchmark rows with `key_storage_assumption` and a pinned provenance (repo + commit + surface, e.g. ERC-1271 vs `validateUserOp`).

If you have a preferred minimal benchmark harness (one or two representative surfaces), I’m happy to align so results are comparable and reproducible.

---

**Madeindreams** (2026-01-10):

That sounds perfect — the coarse enum + notes approach maps very well to how this is deployed in practice.

I’m happy to share concrete OSS references. The pieces you’re asking about live in the following repos/paths:

**AA contract + validation / policy layer**

- QuantumAuth smart account (current AA implementation):
https://github.com/quantumauth-io/quantum-auth-contracts/blob/main/contracts/account/QuantumAuthAccount.sol

This is where I plan to adapt the validation logic to support PQ (or hybrid) signatures at the AA surface (`validateUserOp`), while keeping compatibility with existing flows.

**TPM / hardware-rooted key utilities**

- TPM device utilities (key sealing, curves in use today, ephemeral signing model):
https://github.com/quantumauth-io/quantum-go-utils/blob/main/tpmdevice/tpmdevice.go

This follows the *tpm_sealed_ephemeral_use* model you described: keys are sealed to hardware, decrypted ephemerally for signing, and never exportable.

**AA transaction submission path**

- Where the client assembles and submits transactions to the AA contract:
https://github.com/quantumauth-io/quantum-auth-client/blob/develop/internal/http/handlers.go#L461

This is the integration point where PQ-backed authorization can be cleanly wired into the AA flow.

For a **minimal benchmark harness**, I’d suggest starting with:

1. validateUserOp (AA-native surface)
2. optionally an ERC-1271 adapter for dapp-facing compatibility

I’m happy to align the contract layout, hashing/wiring lane, and surface definitions so results are directly comparable and reproducible. Once the PQ validation path is in place, I can pin commits and help tag benchmark rows with `key_storage_assumption=tpm_sealed_ephemeral_use`.

Looking forward to collaborating on this — having real-world infra + reproducible benchmarks in the same frame is exactly what this space needs.

---

**pipavlo82** (2026-01-11):

Hey — thank you for taking the time to point to concrete OSS anchors. This is exactly what I was hoping for.

No need for me to clone anything right now; I can reference these repos/paths directly. When you have a moment, could you share pinned refs (commit hashes or tags) for each link (or GitHub permalinks pinned to a commit), so the provenance stays stable as the code evolves?

On my side, I’ll add a small “Reference implementations” section and use your TPM utility as the canonical example for:

- key_storage_assumption = tpm_sealed_ephemeral_use
…and I’ll tag dataset rows with:
- key_storage_ref = repo@commit + path
- key_storage_notes = short deployment caveats (PCR/policy, zeroization expectations, etc., only at the notes level)

For the benchmark harness, I’m fully aligned:

- v0 baseline: validateUserOp (AA-native surface)
- optional: an ERC-1271 adapter for dapp-facing compatibility

Once your PQ (or hybrid) validation logic lands in the account contract, I’d love to vendor-pin a commit and add it as a reproducible benchmark row in the dataset (so people can compare apples-to-apples across schemes and surfaces). If you already have a preferred minimal Foundry harness entry point or naming convention for gas logs/snapshots, send it over and I’ll align my runner/extractor to match.

Really looking forward to collaborating — tying real deployment constraints (TPM-sealed key handling) to reproducible EVM benchmarks is exactly the missing bridge in this space.

---

**Madeindreams** (2026-01-11):

Thanks — I really appreciate this conversation and the level of rigor you’re bringing to it. This is exactly the kind of alignment I was hoping for.

I do have some work currently in the pipeline to get the **QuantumAuth beta** out (client + AA flow + browser extension). The core pieces are ready, but there may be some unavoidable latency on the extension side due to browser store approvals (especially Chrome). Once the beta is publicly released, I’ll come back to this thread with **pinned commits / permalinks** for all the relevant components so the benchmark provenance stays stable.

On the contract side, I’m planning to leave deliberate room for:

- multiple PQ algorithms
- hybrid modes
- flexible key representations

so the AA validation logic remains backward-compatible as we transition QuantumAuth toward on-chain PQ (or hybrid) signature validation. That should make it easier to add new schemes later without breaking existing deployments or benchmark continuity.

Once the PQ (or hybrid) validation path lands in the account contract, I’d be very happy to vendor-pin a commit and collaborate on adding it as a **reproducible benchmark row** under `validateUserOp`, with `key_storage_assumption = tpm_sealed_ephemeral_use`.

Really looking forward to collaborating on this — bridging real deployment constraints with clean, comparable EVM benchmarks feels like the right next step for the ecosystem.

---

**pipavlo82** (2026-01-11):

Thanks — makes sense on the beta timing (especially the Chrome/store side). Whenever you’re ready, pinned permalinks/commits will be perfect for keeping provenance stable.

I like the contract posture: keeping room for multiple PQ schemes, hybrid modes, and flexible key encodings while staying backward-compatible is exactly what we need for long-lived, comparable benchmarks.

I’ve added `key_storage_assumption` as an annotation axis and I’m ready to add a reproducible `validateUserOp` row tagged `tpm_sealed_ephemeral_use` once your on-chain PQ/hybrid validation path is in place.

Two quick alignment points so I can match your setup cleanly:

1. What Foundry harness/test naming do you prefer for gas snapshots/logs?
2. Is there a canonical signing “wiring lane” (hashing/message format) you want to standardize for the AA validation path?

Excited to line this up — this is exactly the kind of “real deployment ↔ reproducible benchmarks” connection the ecosystem is missing.

---

**Madeindreams** (2026-01-11):

That all makes sense, and thanks for the alignment questions — they’re helpful in clarifying what’s explicit vs implicit today.

At the moment, **we haven’t established a formal gas benchmark harness**. Gas measurements so far have been used purely for **UX estimation** (user-facing cost previews), not as reproducible benchmark data. The implementation has stayed entirely within **AA-native hashing and flow**, so there was no need yet to isolate or label a dedicated benchmark lane.

Concretely, the current model is:

- standard AA validateUserOp flow
- native EntryPoint getUserOpHash
- signatures applied directly over the UserOpHash
- support for multiple signatures in the userOp.signature field, with policy logic deciding how they’re interpreted

Because of that, the effective (but implicit) wiring lane today is:

- EVM / Keccak-based
- AA-native message format
- no custom hashing, XOF, or non-standard message encoding on-chain

That said, now that there’s a clear path and shared vocabulary, I fully agree it’s time to **make this explicit**:

- define a canonical wiring lane (likely an “EVM lane v0” staying compatible with AA hashing)
- introduce a minimal Foundry harness with named gas snapshots/logs for validateUserOp
- extend the validation logic to support PQ and hybrid signatures without breaking backward compatibility

Once the full PQ (or hybrid) signature validation path is landed in the account contract, the model will be much clearer and I’ll be happy to:

- pin commits / permalinks
- freeze a wiring lane definition
- align on gas snapshot naming so results are directly reproducible

In short: today we deliberately stayed inside the AA-native model; once PQ validation is fully wired into `validateUserOp`, we’ll formalize the lane and the benchmark surface properly. Looking forward to lining that up with your dataset once the beta is out.

---

**pipavlo82** (2026-01-11):

Thanks for spelling out the current implicit lane — that baseline is exactly what we need for v0 comparability: `EntryPoint.getUserOpHash` + signatures over `UserOpHash`, Keccak/EVM, no custom XOF/encoding.

Once PQ/hybrid verification is wired into `validateUserOp`, I can vendor-pin a commit and add a reproducible dataset row aligned to that lane:

- surface = aa::validateUserOp
- key_storage_assumption = tpm_sealed_ephemeral_use
- key_storage_ref = repo@commit + path

Two concrete alignment points so I can match your setup cleanly:

1. Which EntryPoint version / repo are you targeting for getUserOpHash semantics (and any packing quirks)?
2. When you add the Foundry harness, do you have a preferred snapshot/test naming convention (e.g., test_gas_validateUserOp_*)?

Happy to follow your naming so gas snapshots/logs remain directly reproducible as you add multiple PQ algorithms and hybrid modes.

---

**Madeindreams** (2026-01-11):

That sounds great — we’re fully aligned on the v0 baseline.

EntryPoint version

At the time the QuantumAuth account contract was implemented, it targeted the Account Abstraction contracts v0.8.0 semantics (i.e., EntryPoint.getUserOpHash as defined there). I’m aware that v0.9.0 is expected to land imminently (if not already), and part of the upcoming work will be to rebase and verify compatibility once that release is finalized. For the initial benchmark row, v0.8.0 semantics should be the correct reference point; I’ll explicitly pin the EntryPoint repo + commit when I publish the benchmark-ready commits.

Gas snapshot / test naming

I don’t have a strong preference on naming, as long as the intent is explicit. I do think it’s important to clearly distinguish PQ vs non-PQ paths, especially once hybrid modes are introduced, so something along the lines of:

test_gas_validateUserOp_pq

test_gas_validateUserOp_hybrid

(and eventually per-algorithm variants)

would make sense to keep datasets readable as additional schemes are added.

Happy to follow your conventions on the runner/extractor side so snapshots and logs remain directly reproducible across surfaces and algorithms.

Looking forward to pinning everything once the PQ/hybrid validation path is in place — this is shaping up very nicely.

---

**pipavlo82** (2026-01-11):

Sounds good — v0.8.0 `EntryPoint.getUserOpHash` semantics as the baseline reference point is perfect for v0 comparability. Once you publish the benchmark-ready commits, I’ll pin the EntryPoint repo+commit alongside your account contract in the dataset provenance.

On naming: I’m aligned with keeping intent explicit. I’ll mirror your convention on the runner/extractor side and map snapshots into distinct rows, e.g.:

- test_gas_validateUserOp_pq → surface=aa::validateUserOp, validation_mode=pq
- test_gas_validateUserOp_hybrid → surface=aa::validateUserOp, validation_mode=hybrid

(then extend with per-algorithm variants as you add schemes), while keeping `key_storage_assumption=tpm_sealed_ephemeral_use` + `key_storage_ref=repo@commit:path`.

Whenever you’re ready, just drop:

1. the pinned permalinks (or commit hashes) for the account / TPM utils / client path, and
2. the EntryPoint repo+commit you want treated as the canonical v0.8.0 reference.

I’ll wire it into the dataset and reports so the rows stay reproducible across surfaces and algorithms.

---

**Madeindreams** (2026-01-13):

Hey [@pipavlo82](/u/pipavlo82)

I did some deeper research on this, and unfortunately **direct PQ signature verification on Ethereum L1 isn’t a viable path**.

Verifying something like **ML-DSA-65 directly in Solidity would almost certainly exceed practical gas limits**. Even an optimized implementation would be prohibitively expensive and fragile. For PQ signatures to be gas-efficient, **verification really needs to be integrated at the chain level** (e.g. a precompile or system contract).

That leaves two realistic options today:

1. Ethereum mainnet
The only enforceable option is to verify a ZK proof derived from the PQ signature, not the signature itself.
This is deployable today, but the benchmark would essentially be “cost of proof verification + calldata”, not native PQ verification.
2. Layer 2 / Appchain
A Layer 2 (or custom rollup) that implements PQ verification as a native primitive is the clean solution. In that environment, PQ signatures can be verified directly and efficiently, and benchmarks are actually meaningful.

So at best on mainnet we could benchmark **ZK proof validation**, but it’s not worth attempting to validate an actual PQ signature directly on-chain. That path just doesn’t make sense given current EVM constraints.

This is why we’re increasingly looking at a **PQ-aware Layer 2 (“quantum chain”)** as the right place for real enforcement.

---

**pipavlo82** (2026-01-13):

Thanks — that matches my current read as well.

I’m treating “native PQ verify in Solidity on Ethereum L1” as a worst-case stress test / upper bound, not a recommended production path. The benchmark value is still there, but only if we scope it to realistic enforcement surfaces:

Mainnet today: measure (ZK proof verification + calldata) for “PQ attestation,” not PQ verification itself.

L2 / appchain: measure native PQ verification as a first-class primitive (precompile/system-contract equivalent), where the results are actually meaningful for deployed AA flows.

Protocol-facing (future): keep a placeholder surface for an EIP-7932-style precompile assumption so we can drop in real numbers once an ABI + implementation direction stabilizes.

Two practical follow-ups I’d love your take on:

For the mainnet ZK path, what proof system / verifier shape do you consider the most “representative” to benchmark (Groth16 vs PLONK vs Halo2-style, etc.)?

For the L2/appchain path, is the right “minimal contract surface” essentially an ERC-7913/AA-compatible verifier ABI, or do you think we should target a different interface?

If you’re open to it, I can add a dedicated dataset lane for “ZK-from-PQ” vs “native PQ” so we don’t accidentally compare apples to oranges.

Small clarification: we actually measured this path. A full ML-DSA-65 verify() POC in Solidity is currently ~68,901,612 gas (Foundry snapshot), and an optimized inner primitive (PreA compute_w_fromPacked_A_ntt) is ~1,499,354 gas. These are recorded with provenance in the public gas-per-secure-bit dataset. I agree this likely isn’t mainnet-production viable today, but that’s exactly why these baselines are useful: they quantify what a precompile/system-contract or L2-native integration would save.

---

**pipavlo82** (2026-01-13):

On the **mainnet ZK-from-PQ** lane: my default “representative today” would be **Groth16 on BN254** (widely deployed verifier shape on Ethereum L1), and optionally a second point for a **PLONK/Halo2-style** verifier if you think that’s the direction we should anchor for future-proofing. If you had to pick *one* to benchmark first, which would you choose?

On the **L2/appchain / system-contract** lane: I’m currently treating the minimal surface as **ERC-7913-style verifier ABI**, plus AA-facing **validateUserOp** (EntryPoint-bound) and ERC-1271 as adapters — with explicit message lanes to prevent replay-by-interpretation across surfaces. Do you think ERC-7913 is the right “lowest common denominator” ABI for this lane, or is there a better canonical interface you’d prefer?

(For context: I’ve now tagged the dataset rows with `lane_assumption` + `wiring_lane` so ZK-from-PQ vs native-PQ vs legacy don’t get mixed.)


*(1 more replies not shown)*

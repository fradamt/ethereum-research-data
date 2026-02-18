---
source: magicians
topic_id: 25763
title: "[ERC-7999] CrediNet Verifiable Credit SBT —— verifiable snapshot, revoke/replace, expiry, DID/VC hooks"
author: Born2Win
date: "2025-10-13"
category: ERCs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/erc-7999-credinet-verifiable-credit-sbt-verifiable-snapshot-revoke-replace-expiry-did-vc-hooks/25763
views: 41
likes: 1
posts_count: 1
---

# [ERC-7999] CrediNet Verifiable Credit SBT —— verifiable snapshot, revoke/replace, expiry, DID/VC hooks

Summary

We propose an ERC-721–compatible, non-transferable credit credential standard for decentralized credit systems. It binds a verifiable credit snapshot (hash/Merkle root of scoring JSON incl. version & data-source consent) to a soulbound token (SBT), and defines lifecycle semantics: revoke, replace (atomic old→new), and expiry. It also provides DID/VC hooks via hashed references, enabling off-chain privacy with on-chain verifiability.

Motivation

Existing SBT/NTT proposals cover non-transferability (EIP-5192) and burn authorization/governance (EIP-5484), or account-bound issuance (EIP-4973), and NFT-attached badges (ERC-5114). But credit needs more:

– verifiable snapshot anchoring (score version, consented data sources),

– structured revoke/replace/expiry semantics,

– optional selective disclosure / ZK hooks,

– DID/VC interoperability.

Design Overview

Schema + Snapshot. A schemaId identifies a credit model/version (e.g., CrediNet.Score.v1). A snapshot records the hash/root of a scoring JSON (incl. version, dimensions, issuedAt, consentsHash, optional vcHash, optional evidenceURI) and optional expiry.

Uniqueness. Each (holder, schemaId) has ≤ 1 Active token.

Lifecycle.

mintCredit(to, schemaId, snap, burnAuth, tokenURI) → Active.

replaceCredit(to, schemaId, snap, tokenURI, reasonCode, evidenceURI) → atomic revoke old + mint new.

revoke(tokenId, reasonCode, evidenceURI) → Revoked (per burnAuth).

expire(tokenId) (permissionless when time reached) → Expired.

Non-transferability. All transfer*/approve* MUST revert. Optional EIP-5192 locked() returns true to help wallets avoid transfer UX.

Interoperability. ERC-721 events on mint/burn; optional burnAuth() for EIP-5484 code compatibility; optional isSnapshotProven(tokenId, proof) hook to plug ZK verifiers.

Minimal Interface (excerpt)

```auto
interface IERC7xxx /* is IERC165, IERC721 */ {
struct CreditSnapshot {
bytes32 snapshotHash;
bytes32 consentsHash;
bytes32 vcHash; // optional
uint64 issuedAt;
uint64 expiry; // 0 => no expiry
}
event CreditMinted(address indexed to, uint256 indexed tokenId, uint32 indexed schemaId,
bytes32 snapshotHash, bytes32 consentsHash, bytes32 vcHash,
uint64 issuedAt, uint64 expiry);
event CreditReplaced(uint256 indexed oldTokenId, uint256 indexed newTokenId,
uint16 reasonCode, string evidenceURI);
event CreditRevoked(uint256 indexed tokenId, uint16 reasonCode, string evidenceURI);
event CreditExpired(uint256 indexed tokenId);
function mintCredit(address to, uint32 schemaId, CreditSnapshot calldata snap,
uint8 burnAuth, string calldata tokenURI) external returns (uint256);
function replaceCredit(address to, uint32 schemaId, CreditSnapshot calldata snap,
string calldata tokenURI, uint16 reasonCode, string calldata evidenceURI)
external returns (uint256);
function revoke(uint256 tokenId, uint16 reasonCode, string calldata evidenceURI) external;
function expire(uint256 tokenId) external;
function creditOf(address holder, uint32 schemaId) external view returns (uint256);
function getSnapshot(uint256 tokenId) external view returns (CreditSnapshot memory);
function burnAuth(uint256 tokenId) external view returns (uint8); // optional (EIP-5484)
function statusOf(uint256 tokenId) external view returns (uint8); // 0=Active,1=Revoked,2=Expired
function locked(uint256 tokenId) external view returns (bool); // optional (EIP-5192)
}
```

Questions for the community

Default burnAuth mode for credit (issuer-only vs both)?

Minimal reasonCode registry and recommended ranges?

Snapshot JSON mandatory fields (dimensions vs free-form)?

isSnapshotProven — standardize proof targets (e.g., “score ≥ t & source∈whitelist”)?

Whether to include a SchemaRegistry (on-chain) in the base spec?

References

– Minimal locked signaling (EIP-5192), burn authorization (EIP-5484), account-bound (EIP-4973), badge to NFT (ERC-5114).

We welcome feedback, implementations, and wallet/explorer UX inputs. Testnets & reference code will follow in the PR.

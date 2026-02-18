---
source: magicians
topic_id: 22922
title: Proposal for an on-chain Smart Profiles Standard
author: hurricane247
date: "2025-02-20"
category: Web
tags: [wallet, sbt, user-data, smart-profile, profile]
url: https://ethereum-magicians.org/t/proposal-for-an-on-chain-smart-profiles-standard/22922
views: 185
likes: 11
posts_count: 10
---

# Proposal for an on-chain Smart Profiles Standard

### Summary

We propose a new on-chain standard for Smart Profiles, enabling user-centric identity management on Ethereum. This standard allows for decentralized profile schemas, profile minting, IPFS storage of profile data, and cryptographic attestation mechanisms.

### Motivation

Current Web3 identity solutions lack composability and flexibility. By introducing a standardized approach to creating and managing user profiles on-chain, we can enable:

- Decentralized, permissionless profile schema publication
- User-owned profile minting with cryptographic attestations of verified data and claims
- Interoperability across dApps while maintaining user privacy

### Specification

1. On-chain Profile Schemas

Profile schemas can be defined and deployed as smart contracts.
2. The schema registration mechanism is inspired by Ethereum Attestation Service (EAS).
3. Anyone can publish a profile schema, allowing flexibility for different applications.
4. Profile Minting

Users can mint profiles adhering to any of the published schemas.
5. Minted profiles exist as SBTs on user wallets which contain on-chain references to IPFS-hosted profile documents.
6. The on-chain profile includes an IPFS CID, similar to how NFTs store metadata.
7. IPFS-Based Profile Storage

Profile documents stored on IPFS consist of two parts:

Public Data: Readable by anyone, useful for public credentials or reputation systems.
8. Private Data: Encrypted using client-controlled keys.
9. Clients can use MetaMask Snaps or Lit Protocol for encryption and access control.
10. Attestation Mechanism

Profile data can be attested by the profile issuing party using EAS, allowing:

On-chain attestations for key profile attributes.
11. Off-chain attestations for private or large datasets.
12. This enables verifiable claims and proofs for both public and private data.

### Benefits

- Decentralization: No central authority controls the schema or profiles.
- Interoperability: Profiles can be used across different dApps and ecosystems.
- Privacy-Preserving: Users control access to their private data with encryption.
- Verifiable Identity: Attestations allow for provable identity claims (on-chain and off-chain).

### Current State of the art

We have already created the whole profiles framework in ceramic network. You can find the schemas and various profiles built with it here:

https://docs.plurality.network/the-core-protocol/structure-of-a-smart-profile

We have also recently launched an MVP of a smart profiles wallet where we are using these ceramic network based smart profiles in production:



      [x.com](https://x.com/PluralityWeb3/status/1890381880102396315)





####

[@](https://x.com/PluralityWeb3/status/1890381880102396315)



  https://x.com/PluralityWeb3/status/1890381880102396315










We have an open-source repo that acts as SDK to manage smart profiles.

https://github.com/Web3-Plurality/plurality-smart-profile-utils

### Next Steps

We invite feedback from the Ethereum community on:

- Enhancements to the schema publication mechanism.
- Best practices for encryption and key management.
- Integration with existing identity and reputation systems.

Smart profiles are meant to be a public good like ENS/EAS. We imagine infinite use cases which will open up the Ethereum ecosystem to endless possibilities not limited to mostly finance.

Would love to hear thoughts from the community! Let’s collaborate on refining this idea into a robust standard for on-chain user profiles.

### Team:

- Hira Siddiqui (https://x.com/identityonchain)
- Mujtaba Idrees (https://x.com/mujtabaidrees94)

## Replies

**bumblefudge** (2025-02-20):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/h/d9b06d/48.png) hurricane247:

> Profile documents stored on IPFS

Who’s pinning? How fetched?

---

**hurricane247** (2025-02-20):

1. IPFS nodes are pinning. There should be an incentivization model built around it for pinning.
2. They are fetched through Smart Profiles SDK (linked in the post).

---

**mujtaba.idrees** (2025-02-20):

Actually even if we consider simple ipfs we still need to pin the docs, you’re right. In the end, we need an incentivization model to pin those documents or the user can pin it themselves to keep the profiles available.

---

**bumblefudge** (2025-02-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mujtaba.idrees/48/9076_2.png) mujtaba.idrees:

> In the end, we need an incentivization model to pin those documents or the user can pin it themselves to keep the profiles available.

I’m not sure you’re responsible for business models or tokenomics, per se, but it might be nice to keep going since you’ve got this much momentum specifying all the interfaces and data models.  In other words, if the goal here is to have an e2e standard for all the moving parts, I would suggest also including some concrete details (if not full interfaces and data models) for what happens at that “aggregation layer” of “Identity Providers” that enroll and pin the profiles of end-users, and ideally some kind of migration standard for how one moves to another if the pinner/host/hub that enrolled you goes broke or winds down. Even if, in what you’ve built so far, there is only one provider (or you are the only provider), this would at least enable a theoretical “second implementation” (perhaps Ceramic-free and classic-IPFS-based, or swapping out other core elements) to come along more easily and deliver “credible exit” for anyone who sets up these profiles and wants them to outlive the registrar that original pinned them.

---

**bumblefudge** (2025-02-20):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/h/d9b06d/48.png) hurricane247:

> They are fetched through Smart Profiles SDK (linked in the post).

I meant are they being pulled from a public gateway or one from a service-provider like Pinata or one provided by Plurality, but it seems like the answer is the first, if this how smart profiles get pulled out of the IPFS DHT:



      [github.com](https://github.com/Web3-Plurality/plurality-eth-online/blob/d5ebb2b303e49a6a8bd83df316b33de26d2ea3b4/packages/api/src/controllers/PermawebUploadController.ts#L99)





####



```ts


1. },
2. {
3. headers: {
4. pinata_api_key: process.env.PINATA_API_KEY,
5. pinata_secret_api_key: process.env.PINATA_API_SECRET,
6. },
7. }
8. );
9. console.log(resp.data.IpfsHash);
10. //const pinataobj = resp.data.IpfsHash;
11. res.status(200).send({ url: `https://ipfs.io/ipfs/${resp.data.IpfsHash}` }).json();
12.
13. } catch (e) {
14. //console.log(e);
15. res.status(500).send(e);
16. }
17. });*/


```

---

**mujtaba.idrees** (2025-02-21):

You are correct in pointing out that we might need

> A Ceramic-free, classic-IPFS-based second implementation to provide a “credible exit” and ensure profiles outlive the registrar.

Since this post focuses on profile standards as a data format, we deliberately omitted protocol-level details.

The concern about outliving the registrar is entirely valid. If we develop a smart contract-based profile system, we will need a reliable pinning or indexing service backed by a decentralized protocol.

### Possible Approach:

- Indexing nodes could pin and index IPFS documents, helping maintain data availability.
- A decentralized indexing protocol could allow efficient retrieval of profile data.
- Reward mechanisms might be needed to incentivize node operators, but any model that introduces fees for simple profile queries would need careful evaluation.

---

**mujtaba.idrees** (2025-02-21):

(post deleted by author)

---

**mujtaba.idrees** (2025-02-21):

(post deleted by author)

---

**hurricane247** (2025-02-21):

You raise an important point about the need for a:

> Ceramic-free, classic-IPFS-based alternative to ensure profiles remain accessible beyond the lifespan of any single registrar.

Since this discussion is centered on profile standards as a data format, protocol-level implementation details were intentionally left out.

One reason we initially adopted a system like Ceramic was its ability to link IPFS documents with blockchain addresses without requiring an on-chain registry. This approach simplified key management but also introduced limitations when considering long-term persistence beyond any single protocol. A key challenge is ensuring profiles remain available in a decentralized and verifiable manner.

To address this, a more generic and flexible protocol could be designed—one that provides reliable pinning and indexing of profiles without relying on a single provider.

**Possible Approach:**

1. Indexing nodes could pin and index IPFS documents, helping maintain data availability.
2. A decentralized indexing protocol could allow efficient retrieval of profile data.
3. Reward mechanisms might be needed to incentivize node operators, but any model that introduces fees for simple profile queries would need careful evaluation.


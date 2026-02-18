---
source: magicians
topic_id: 15862
title: "EIP-7522: OIDC ZK Verifier for AA Account"
author: dongshu2013
date: "2023-09-20"
category: EIPs
tags: [erc, wallet, account-abstraction, zkp]
url: https://ethereum-magicians.org/t/eip-7522-oidc-zk-verifier-for-aa-account/15862
views: 5019
likes: 10
posts_count: 10
---

# EIP-7522: OIDC ZK Verifier for AA Account

Discussion for [Add EIP: Account Recovery by OIDC by dongshu2013 · Pull Request #7743 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7743)

The purpose of the EIP is to standardize the interface for a new model which use OpenID ZK Verification as the recovery mechanism for AA account.

## Replies

**orbmis** (2023-10-02):

This is a very interesting proposal, and I think it could be a very powerful primitive.  It’s great to see it being published as an EIP.

If I have one question, it’s whether there are known requirements for creating a proof of a HWT, e.g. what cryptographic schemes need to be supported etc.  Is there reference documentation for this?  For example, is there an implicit dependency on a zk implementation of say the OIDC spec?

---

**yyd106** (2023-10-10):

[@orbmis](/u/orbmis) The implementation is open to all the ZK algorithms. Right now we mainly focuses on the Nova implementation: [GitHub - OpenID3/zk-jwt: the library to generate zk proof for JWT](https://github.com/OpenID3/zk-jwt)

---

**ajhodges** (2023-10-20):

This is really interesting. I’m curious about the vision for the guardians.

> One may set multiple OIDC identities(e.g. Google Account, Facebook Account) as guardians to minimize the centralization risk introduced by the identity provider.

Does this imply the ability to roll up multiple JWT proofs into a single proof? For example, if I had a wallet where I wanted to set up 3 guardians and require a 2/3 threshold of valid JWTs as a precondition for recovery, is that feasible with this approach? It seems critical to enforce a minimum of 2 JWT signatures for this to effectively minimize centralization risk, but I’m not sure if this is one of your design goals.

---

**dongshu2013** (2023-10-20):

Supporting the mode with multiple OpenID to recover one account is one of our goals, not only to ensure the recovery is decentralized enough but also to provide better security. The way to achieve this is quite flexible though. We can either aggregate the proof off-chain or we can simply implement the multi-sig logic on-chain and do verification for each proof separately.

---

**alinush** (2024-03-18):

Very glad to see [this EIP](https://eips.ethereum.org/EIPS/eip-7522) on Ethereum! However, this proposal is not sufficiently descriptive… Are there more updates expected?

Two questions:

1. How is the address associated with an OpenID account derived? e.g., AFAICT, to prevent phishing, the address needs to be associated both with the user (by anchoring to, say, the sub field) and the OAuth application (by anchoring to the aud field)
2. The EIP talks about privacy, but the TXN signature seems to include the JWT signature which, when verified against the JWT header & payload would leak the identity of the user.
3. The EIP mentions “Privacy will be guaranteed as the connection between Web2 identity and the Web3 account will be hidden.” But the details are missing: i.e., what is the ZK relation? (e.g., see an example here)

---

**yyd106** (2024-07-09):

[@alinush](/u/alinush)

1. The client side could put the hash of user’s address (operator account) into the OAuth request. Once user passed the authentication, it will be included by the JWT which signed by identity provider, say, google.
2. The EIP defines an ZKP based on the JWT. The ZK declaration could include: 1. the user’s OAuth ID hash, and the operator (address) is included in same id_token; 2. the signature of the JWT is true.
3. Once the proof from step 2 has been verified by account contract, user’s operator will be set as the controller on user’s contract account while user’s JWT is keeping private.

---

**kjhman21** (2025-11-10):

[@yyd106](/u/yyd106) [@dongshu2013](/u/dongshu2013)

I really like this and I am also building similar one. But it seems like the discussion stopped on Jul 24. Any progress??

---

**yyd106** (2025-11-11):

The rollout of this scheme hinges on the efficiency of ZK technology. At present, the cost is still prohibitively high.

Do you have the latest numbers on your solution’s efficiency? If the performance and cost look good, we can push ahead.

---

**Ankita.eth** (2025-11-11):

**[@yyd106](/u/yyd106) [@kjhman21](/u/kjhman21) [@dongshu2013](/u/dongshu2013)**

EIP-7522 is shaping up to be the **privacy-native recovery layer** AA has been missing. Leveraging ZK-attested OIDC JWTs to rotate keys *without exposing Web2 identity* is a masterstroke — effectively turning centralized logins into **sovereign recovery factors**. The modular design (guardian registry + verifier + off-chain prover) is elegant and future-proof.

With 2025-era folding optimizations (Nova + Sangria), the numbers now look strong:

- <1.5s proof gen (laptop)
- <20 KB proof size
- ~450K gas verification (post-Dencun)

Multi-guardian thresholds are now *realistically deployable*: aggregate 3 JWT proofs off-chain into one succinct Nova instance, or verify them individually with an on-chain 2/3 threshold logic.

### Key Technical Alignment

Formalize the **binding hash** inside the circuit:

```solidity
guardianHash = keccak256(sub ‖ aud ‖ operatorNonce)
```

- operatorNonce: wallet-generated per recovery
- Mitigates replay and phishing risks
- Should be a required field in the spec

Also consider enforcing **JWT expiry checks** (`iat`, `exp`) and a **guardian revocation mechanism** (tombstone flag or Merkle root update).

---

### Recommendation

Update the EIP with:

1. Clear ZK relation (public inputs + witness layout)
2. keccak256(sub‖aud‖nonce) binding rule
3. Dual recovery options (aggregated vs multi-verify)
4. EIP-4844 blob fallback
5. EIP-4337 / 7702 compatibility snippets
6. Current benchmark table (Nova + zk-jwt)

This proposal is already **ERC-ready** — it just needs final alignment and spec clarity.


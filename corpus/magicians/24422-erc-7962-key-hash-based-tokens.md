---
source: magicians
topic_id: 24422
title: "ERC-7962: Key Hash Based Tokens"
author: dugubuyan
date: "2025-06-03"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7962-key-hash-based-tokens/24422
views: 923
likes: 19
posts_count: 57
---

# ERC-7962: Key Hash Based Tokens

[ERC] [Add ERC: Key Hash Based Tokens by dugubuyan · Pull Request #1061 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1061)

The proposal, ERC-KeyHashToken: Key Hash-Based Token Standard (EIP-TBD), introduces two token standards: ERC-KeyHash721 for non-fungible tokens (NFTs) and ERC-KeyHash20 for fungible tokens (akin to ERC-20). Unlike traditional standards, it employs a keyHash (computed as keccak256(hashKey)) to represent ownership instead of Ethereum addresses, with operations (e.g., transfer, destroy) verified via ECDSA signatures. The core innovations include enhanced privacy, separation of ownership and transaction initiation, and robust security through EIP-712 signatures and nonce mechanisms.

- Need for Privacy Protection
- Current State: In ERC-20 and ERC-721, ownership is tied to Ethereum addresses, which are publicly visible on the blockchain. Through on-chain analysis, these addresses can be linked to real-world identities, particularly in high-value transactions or NFT markets, compromising user privacy.
- Proposal Advantage:

Replaces addresses with keyHash, allowing users to prove ownership without revealing their actual addresses. The hashKey (kept confidential) is only provided during signature operations, with only the keyHash recorded on-chain, reducing identity linkage risks.
- Users can generate unique hashKeys for each token or balance, further minimizing linkability between on-chain activities, aligning with privacy trends like EIP-5564 (Stealth Addresses).

**Necessity**: As regulatory scrutiny increases (e.g., GDPR) and user demand for privacy grows (e.g., decentralized identity needs), privacy protection is a critical requirement for blockchain applications. ERC-KeyHashToken provides a standardized solution for privacy-sensitive scenarios.
**Demand for Transaction Flexibility and User Experience Optimization**
**Current State**: Traditional token standards require owners to pay gas fees and initiate transactions from their addresses, increasing costs and complexity in high-gas or batch transaction scenarios.
**Proposal Advantage**:

- Separates ownership from transaction initiation, allowing anyone with a valid signature to initiate transactions and pay gas fees. This enables third parties (e.g., service providers, enterprises) to cover gas costs, similar to EIP-2612’s permit mechanism.
- Supports batch transactions, such as transferring multiple NFTs in one transaction, optimizing gas usage.

**Necessity**: With fluctuating Ethereum gas fees, reducing transaction costs is vital. The proposal’s support for gas sponsorship and batch processing is particularly valuable for large-scale applications, enhancing user experience.
Detailed Application Scenarios

1. Anonymous Collectibles (NFT Use Case)

- Scenario Description: In digital art or collectibles markets, NFT owners want to hide their identities to avoid on-chain tracking. For example, a high-net-worth individual purchasing an art NFT wishes to remain anonymous.
- Application:

With ERC-KeyHash721, NFT ownership is tied to a keyHash rather than a public address. Owners transfer NFTs via signatures without exposing their addresses.
- Users can generate unique hashKeys for each NFT, reducing activity correlation.

**Advantages**: Enhances user privacy, attracting privacy-conscious collectors and boosting market competitiveness.
**Real-World Example**: NFT projects like Azuki or CryptoPunks could adopt this standard to offer greater privacy, appealing to high-end users.

1. Private Financial Transactions

- Scenario Description: In DeFi or institutional finance, users want to transfer tokens without exposing addresses, such as high-net-worth individuals moving large ERC-20 token amounts.
- Application:

With ERC-KeyHash20, token balances are tied to keyHash, and users execute transfers via signatures.
- Third parties can cover gas fees, simplifying operations.

**Advantages**: Protects transaction privacy, reduces on-chain tracking risks, and supports flexible gas payment, ideal for enterprise applications.
**Real-World Example**: Stablecoins like MakerDAO’s DAI could adopt this standard for privacy-preserving private transactions.

1. Batch Transactions and Gas Sponsorship

- Scenario Description: NFT marketplaces or gaming platforms need to transfer tokens in bulk for users who prefer not to pay high gas fees. For example, Axie Infinity wants to distribute reward tokens to new players.
- Application:

Using ERC-KeyHash721 or ERC-20, platforms collect user signatures, initiate batch transactions, and cover gas fees.
- Mimics Bitcoin’s UTXO model for optimized balance transfers (e.g., leftKeyHash).

**Advantages**: Reduces user costs, simplifies operations, and suits large-scale distribution scenarios.
**Real-World Example**: Platforms like OpenSea or Axie Infinity could use gas sponsorship to improve user retention.

#### Comparison with Existing Standards

| Feature | ERC-20/ERC-721 | ERC-KeyHashToken |
| --- | --- | --- |
| Ownership Identifier | Ethereum Address | keyHash (keccak256(hashKey)) |
| Privacy Protection | Public, No Privacy | Anonymous, Signature-Based |
| Gas Payment | Owner Pays | Third-Party Can Pay |
| Security | Basic Signatures | EIP-712, Nonce, Deadline |
| Use Cases | General Tokens | Privacy, Batch Transactions, DID |

#### Potential Challenges and Solutions

- Privacy Limitation: hashKey must be transmitted during transfers, risking exposure.

Solution: Recommend hardware wallets for hashKey storage and encrypted channels for transmission.

**Gas Costs**: Signature verification and EIP-712 hashing increase gas consumption.

- Solution: Use gas sponsorship and optimize implementations (e.g., batch operations) to offset costs.

**User Education**: Managing hashKey adds complexity.

- Solution: Develop user-friendly wallet tools to simplify signature and key management.

## Replies

**dugubuyan** (2025-12-04):

### 【EIP-7962 Update】Major Updates to Key Hash Based Tokens (Dec 2025)

Since the initial discussion draft was posted in May 2025, we’ve received valuable community feedback and gone through several rounds of iteration. Below are the **major changes and improvements** made to ERC-KeyHash721 and ERC-KeyHash20. The updated EIP is now officially numbered **EIP-7962**.

#### 1. Official EIP Number: 7962

- The proposal is now formally submitted as EIP-7962 (previously discussed under the working title “Key-Based Tokens”).

#### 2. Terminology Clarified & Unified

- Unified and clearly defined:

key: 65-byte uncompressed secp256k1 public key (0x04 || X || Y)
- keyHash: keccak256(key) – the on-chain ownership identifier

Signer address is derived as `address(uint160(uint256(keccak256(key[1:])))))` (standard Ethereum address derivation from the 64-byte XY coordinates).

#### 3. Major Redesign of ERC-KeyHash20 Transfer (UTXO-like Model)

- Abandoned the traditional ERC-20 “balance subtraction” approach.
- Now requires an input-output-change model on every transfer:

```solidity
transfer(
    bytes32 fromKeyHash,
    bytes32 toKeyHash,
    uint256 amount,
    ...,
    bytes32 leftKeyHash   // change output; strictly required to be ≠ fromKeyHash && ≠ toKeyHash
)
```
- Benefits:

Forces key rotation on every spend → dramatically improves privacy
- Prevents partial spends from leaving identifiable remainder balances
- Aligns perfectly with Bitcoin UTXO privacy model and the spirit of EIP-5564

#### 4. Security Significantly Strengthened

- All state-changing operations (transfer, destroy) now use full EIP-712 structured data signing (all critical parameters included).
- Per-keyHash nonce tracking (mapping(bytes32 => uint256) _keyNonces).
- Cross-contract replay protection via EIP-712 domain separator (chainId + verifyingContract).
- Mandatory deadline parameter for signature expiration.
- Explicit rejection of malleable signatures (recommend OpenZeppelin ECDSA library).

#### 5. Explicit Removal of approve / allowance

- Because the full public key is revealed in calldata during any operation, keys are treated as one-time-use.
- No approve or allowance functions are provided.
- After any transfer/destroy, users are expected to immediately migrate remaining assets to a fresh keyHash.
- Implementations MAY block reuse of any keyHash whose key has ever been revealed.

#### 6. Full Reference Implementations Added

- Complete, compilable OpenZeppelin-style implementations for both ERC-KeyHash721 and ERC-KeyHash20 are now included.
- Covers EIP-712 domain, nonce management, signature verification, _addressFromUncompressedKey, etc.

#### 7. Security Considerations Section Greatly Expanded

New/emphasized risks & best practices:

- Public key exposure in calldata → always use fresh key pairs
- Secure private-key / public-key storage recommendations (hardware wallets encouraged)
- Detailed analysis of replay protection, deadlines, nonce design, gas costs, etc.

#### 8. Other Adjustments

- ownerOf(tokenId) → returns bytes32 (keyHash), not address
- balanceOf(bytes32 keyHash)
- mint access control remains implementation-defined (owner-only, open mint, etc.)
- Unified events: KeyHashTransfer721 / KeyHashTransfer20; burn emits transfer to 0 + optional KeyHashBurn721

### Current Status

- EIP-7962 markdown has been fully updated with all the above changes.
- PR to ethereum/EIPs will be opened in the next few days.
- We especially welcome feedback on:

Should ERC-KeyHash20 offer an optional “non-strict” mode that allows leftKeyHash == fromKeyHash for compatibility?
- Do we need batch transfer interfaces (multi-input/multi-output)?
- Community sentiment toward the strict one-time-key model?

Huge thanks to everyone who provided feedback earlier — most of these improvements came directly from those discussions!

Looking forward to moving this toward Last Call.

[@dugubuyan](/u/dugubuyan) @nake13 @stbrahms @LiYingxuan

---

**SamWilsn** (2025-12-04):

Regarding the `mint` & `destroy` functions, if they are intended to be restricted to the contract owner/creator, you probably shouldn’t specify them in the required interface. You’ll note that none of the popular token standards (ERC-20, ERC-721, ERC-1155) directly define either of these functions.

These functions are often omitted from the token interface because token interfaces exist to facilitate compatibility between otherwise uncoordinated pieces of software, like a wallet and the token contract, but the `mint` & `destroy` functions are intended to be called by the contract creator/owner. The contract creator/owner can be reasonably expected to know how to interact with their own contract, so no standard interface is required. Requiring these functions overly constrains implementations. For example, imagine a fixed-supply token where no minting/burning is permitted after construction. Now that token’s contract is forever burdened with `mint`/`destroy` functions that always revert.

---

**dugubuyan** (2025-12-05):

Yes, you are right. As interfaces, these two functions should not be required

---

**benhaben** (2025-12-18):

I really appreciate the design direction of ERC-7962: Key Hash Based Tokens.

The core innovation—decoupling authorization from execution by shifting from address-driven to signature-driven interactions—is extremely valuable. Specifically, the ability for any address to initiate transfers, third parties to sponsor gas, and native support for batch operations opens up a wide range of practical use cases that are difficult or inefficient under traditional ERC-20/721 models.

This approach significantly lowers user onboarding friction (e.g., users don’t need ETH to transact), enables privacy-conscious applications through keyHash-based ownership, and empowers platforms to deliver Web2-like experiences on Ethereum—such as bulk reward distributions, anonymous collectibles, or gasless transactions—without relying on zero-knowledge proofs or complex infrastructure.

While not a full privacy solution, it strikes an excellent balance between usability, security, and lightweight anonymity. I believe this standard could become a foundational building block for next-generation tokenized applications.

Great work, and looking forward to seeing it evolve!

---

**mickwif** (2025-12-18):

I see **ERC-KeyHashToken** as a very advanced proposal that addresses privacy issues at the standard level and solves several real-world problems in a more reasonable and cost-efficient way for specific scenarios.

However, the migration cost for the existing ecosystem is extremely high. Address-based ownership is deeply embedded in wallets, tooling, and user expectations, so this proposal is unlikely to replace ERC-20 or ERC-721.

Instead, ERC-KeyHashToken is better positioned as a **complementary standard** for privacy-sensitive, gas-sponsored, or enterprise use cases, rather than a general-purpose replacement.

---

**mashima** (2025-12-18):

This solution provides a new approach to enhancing the scalability and security of tokens. The complexity of its implementation and the level of industry acceptance remain to be further tested.

---

**dugubuyan** (2025-12-18):

Correct. This solution serves as a supplement to ERC20 and ERC721, and is unlikely to replace them. Additionally, the design of this solution prioritizes privacy-focused scenarios, such as membership identity verification. Similar to what DDC(https://github.com/DataDanceChain/DDC-Market-Contracts.) does, it enables verification and transactions of membership identities across multiple merchants without exposing any address information.

---

**hiwanz** (2025-12-18):

Strictly speaking, this analogy isn’t entirely accurate. However, this solution does aim to minimize the risk of privacy exposure at the business level. Combining this with one-time address logic on the wallet side could further enhance privacy features.

Ultimately, however, it all comes down to the fundamental business considerations: how significant are the business needs and application scenarios?

---

**dugubuyan** (2025-12-19):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/df705f/48.png) mashima:

> This solution provides a new approach to enhancing the scalability and security of tokens. The complexity of its implementation and the level of industry acceptance remain to be further tested.

Yes, considering complex business implementations, it’s common to add custom business logic in practical applications—this is an “addition” approach. However, a “subtraction” approach can also be adopted based on this solution, as demonstrated in the reference implementation: [GitHub - DataDanceChain/DDC-Market-Contracts](https://github.com/DataDanceChain/DDC-Market-Contracts).

In this implementation, `_addressFromUncompressedKey(key)` and address validation are omitted during transfers. The simplification is possible because a contract owner is introduced, and all transactions are initiated by the contract owner. While this sacrifices some decentralization, it aligns with the business requirements of transparency and immutability.

---

**dugubuyan** (2025-12-19):

Yes, that’s exactly my motivation for designing this ERC. There are essential privacy protections to be fulfilled, but standard ERC20 and ERC721 cannot meet these requirements.

---

**erain9** (2025-12-19):

I am very supportive of this ERC. The mechanism introduced is lightweight yet practical for introducing Privacy for onchain token activities.

---

**RichardBelsum** (2025-12-22):

I really appreciate this privacy-focused design. When can we expect more application scenarios to go live? Please keep us posted with more updates.

---

**chenzhitong** (2025-12-22):

Let’s first consider when an address and keyHash derived from a public key can be linked together.

Obviously, this linkage becomes possible only when the public key is revealed. Here there are two main ways this can happen:

(1) through the transfer transaction itself, or

(2) through a signature.

Whenever an Ethereum address actively initiates a transaction, its public key can be reconstructed from the transaction signature.

In other words, whenever a private key produces a signature — whether the signature is included on-chain as part of a transaction or is published off-chain as a signed message — the corresponding public key can be recovered from it.

Therefore, unlinkability for a specific ownership entity is broken once there exists a signature or a revealed public key associated with that keyHash (or its corresponding address).

This situation is expected to be quite common in practice.

If we enforce a one-time-use policy for keyHash to mitigate this, then in principle

transfer(bytes32 fromKeyHash, bytes32 toKeyHash, …, bytes32 leftKeyHash)

and

transfer(address from, address to, …, address left)

would behave similarly, since addresses could also be restricted to one-time use.

Essentially, both address and keyHash are different one-way encodings of the same underlying public key, and the public key itself is the only true unique identifier.

This ERC introduces a new additional encoding and ownership abstraction to mitigate the systemic linkability that arises from using addresses as the only universal ownership identifier.

This might be one possible approach, though there could be others. After all, you can’t have your cake and eat it too.

---

**dugubuyan** (2025-12-22):

You have thought this through very carefully. In this proposal, compared to directly using one-time public keys, there are additional considerations:

**1. Different on-chain storage content: hash is irreversible, addresses can be reversely derived**

**Current design (keyHash = keccak256(entire 65-byte key)):**

What is permanently stored on-chain is a completely irreversible 32-byte hash. Before a transfer, anyone seeing the `keyHash` returned by `ownerOf` cannot recover the public key or derive any address information from it. There is absolutely no information leakage.

**If changed to directly store the “public key address” (lower 160 bits of keccak256(key[1:])):**

This address is essentially a “fingerprint” of the public key, but it is in the standard Ethereum address format. Once the full public key (`key` ) is revealed during transfer, an observer can immediately calculate this address and permanently associate it: “The historical owner of this token was this address.” In the on-chain history, this address would be forever visible; even if the token is later transferred to a new address, the old one remains exposed.

Although the protocol encourages one-time public keys (discarding the old key after transfer), the irreversibility of `keyHash` provides an extra layer of protection: even if someone sees the public key during transfer, they cannot link the historically stored `keyHash` on-chain to this public key/address (because the hash is one-way).

**2. Preventing on-chain “address labeling” and long-term linking**

In the Ethereum ecosystem, addresses are easily labeled (e.g., by on-chain analysis firms like Chainalysis or Nansen). Once a “public key address” is labeled as belonging to a person/project, all subsequent token history using this address can be permanently linked.

**Using `keyHash` (a random-looking bytes32) as the identifier:**

It does not resemble an address, making labeling extremely difficult.

Even if the public key and derived address are exposed during transfer, this address only appears in the calldata of that transaction and is not permanently stored in the contract’s ownership mapping.

Historical records only contain a series of unrelated bytes32 values, making long-term linking extremely challenging.

**3. Alignment with privacy primitives like ERC-5564 (Stealth Addresses)**

The stealth address mechanism in ERC-5564 also first publishes a public key hash (or similar commitment), and the spending public key is only revealed when the recipient spends.

The broader Ethereum privacy ecosystem (including various privacy token proposals under discussion) tends to use commitments/hashes rather than direct addresses/public keys to identify ownership, precisely to minimize linkable information on-chain.

Using `keyHash` makes this ERC natively compatible with future stealth meta-address schemes (a stealth address can generate countless one-time keyHashes).

**Conclusion: The value of this additional hash layer**

**Primary value: Provides “forward privacy” and “historical unlinkability.”** Even if the current public key must be exposed during transfer, the on-chain historical records remain completely anonymous hashes, with no mathematical link to the exposed public key/address.

**If directly using public key-derived addresses:** Exposure of the public key during transfer → Address is calculated → On-chain historical ownership directly points to this address → Historical ownership can be permanently tracked and labeled, significantly reducing privacy strength.

The current `keyHash` design adds a commitment layer on top of the “one-time public key” model, ensuring that the identifier stored on-chain can never be linked to any actually exposed public key.

Thus, while it might seem like an extra step, this additional `keccak256(entire key)` layer is precisely the fundamental reason why this protocol offers stronger privacy than a “simple one-time address model.”

---

**lutianzhou001** (2025-12-29):

Great ideas, BTW, could we add some functions for requiring complex fund movements (e.g., exchanges, payment processors) since single-input-single-output transactions are inefficient.

I suggest we add a batch interface similar to Bitcoin’s transaction model, just like

function batchTransfer(

bytes32 calldata fromKeyHashes,

bytes32 calldata toKeyHashes,

uint256 calldata amounts,

bytes calldata signatures,

bytes32 changeKeyHash,

uint256 deadline

) external;

This consolidates can multiple inputs/outputs into a single transaction, reducing gas costs and improving atomicity.

---

**yanz** (2025-12-31):

Storing an irreversible keyHash on-chain instead of address-like fingerprints gives strictly better forward privacy and makes historical linkage and labeling much harder, which lines up well with ERC‑5564 and other commitment-based schemes. But I don’t see this realistically replacing ERC‑20 or ERC‑721 given current ecosystem inertia, but as a complementary standard for membership, B2B, and some privacy scenarios, it looks very compelling.

---

**dugubuyan** (2026-01-04):

You’ve raised an excellent suggestion. Batch transfers can significantly reduce gas costs and greatly improve the user experience, making them particularly suitable for use cases like gaming and airdrops.

While ERC-7962 itself does not define a batch transfer interface, its authorization and execution model makes **“batch transfers fully feasible at the implementation layer and architecturally more natural than traditional ERC-20/ERC-721.”**

ERC-7962’s `transfer` has a crucial feature: **“Authorization happens off-chain (via signatures), execution happens on-chain (by any address).”** This means that multiple transfers can be collected off-chain and submitted together by an executor (relayer/aggregator)—something that is either impossible or awkward in traditional ERC models.

The specification explicitly defines that:

1. transfer does not depend on msg.sender.
2. Authorization depends solely on the signature and keyHash.

Therefore, implementing batch transfers based on ERC-7962 can be done at the application layer. Below is a reference implementation approach I propose, with the following workflow:

1. The user signs multiple transfers individually.
2. A relayer collects the signatures.
3. The relayer sequentially submits the multiple transfers within a single block.

---

**Max2557** (2026-01-18):

This post was flagged by the community and is temporarily hidden.

---

**huahua** (2026-01-18):

Thanks for sharing ERC-7962 — I really like the direction here. Moving from **address-based ownership** to **keyHash-based ownership** feels like a clean “primitive-level” shift that unlocks a few things we usually bolt on with extra infrastructure:

- Authorization vs execution separation (any relayer can submit tx + sponsor gas)
- Lightweight privacy / unlinkability (at least compared to fully address-tied balances)
- A more “UTXO-flavored” transfer model for fungible tokens (the leftKeyHash change output)

That said, I have a few questions / concerns that I think are worth discussing before broader adoption:

### 1) Privacy model clarity: what exactly is protected?

Even though `ownerOf()` and `balanceOf()` are `bytes32 keyHash`, the **public key is revealed in calldata during transfer**, and the signer address can be derived from that pubkey. So privacy seems to rely heavily on **one-time keys + strict key rotation**.

- Do you see ERC-7962 as primarily “reducing casual tracking” rather than providing strong privacy guarantees?
- Should the spec explicitly recommend/require wallet-side key pools (like stealth-address style workflows) to make the privacy benefits real in practice?

### 2) Recipient UX: how do people get toKeyHash safely?

To send tokens, I need the recipient’s `toKeyHash`. That’s fine for power users, but for normal users it raises practical questions:

- How should wallets/apps exchange keyHash values? QR code? out-of-band messaging? registry?
- Is the recommended flow “recipient generates a fresh key pair per receive” (like stealth addresses), and only shares the hash?

This part will heavily determine whether the standard is usable beyond niche applications.

### 3) Composability with existing DeFi / app infrastructure

The absence of `approve/allowance` makes sense if keys are one-time, but it also means **most existing DeFi patterns won’t work directly** (DEX routers, lending protocols, staking contracts, etc.).

- Do you envision “adapter / wrapper” contracts as the main integration path (wrap KeyHash20 into ERC-20, unwrap on exit)?
- If yes, do you think it’s worth standardizing a canonical adapter pattern so the ecosystem doesn’t fragment?

### 4) ERC-KeyHash20 strict mode tradeoffs (full spend + change)

The strict `leftKeyHash != fromKeyHash && != toKeyHash` is a strong privacy move and aligns with UTXO thinking. But it also changes how balances behave and increases wallet complexity:

- Every spend becomes an input-output-change flow, which is powerful but unfamiliar for ERC-20 users.
- It may also increase state writes (two outputs each time).

I’m curious if you’ve benchmarked gas costs vs a more “account-like” model, and whether you expect wallets to abstract this away completely.

### 5) Signature formats / account types

Right now the model is tightly coupled to **secp256k1 ECDSA** (`ecrecover`-style verification). That’s okay, but it means:

- It won’t natively support contract-based signature schemes (e.g., EIP-1271),
- and won’t directly align with passkey/P-256 style signing without an additional layer.

Do you see a future extension where the “keyHash” could represent a broader class of verifiers (pubkeys, contract verifiers, threshold keys), or is the intention to keep this minimal and ECDSA-only?

### 6) Indexing & wallet discovery

Since assets are tied to `keyHash`, wallet UX may depend on tracking generated keys locally.

- Are there recommended event indexing patterns (best practices for wallets to discover balances/NFTs)?
- Any concern about users losing track of key pools and “orphaning” assets?

---

Overall, I think ERC-7962 is a strong proposal **as a complementary standard**, especially for:

- gas-sponsored flows,
- privacy-sensitive memberships/credentials,
- and “Web2-like UX” distribution systems.

If the wallet UX story (key management + recipient discovery) is clearly documented and standardized, this could become a very practical building block.

Looking forward to the next iteration — especially around batch interfaces (multi-in/multi-out would be very interesting here).

---

**yoona** (2026-01-18):

As a senior undergraduate with roughly three years of hands-on blockchain development experience, I interpret ERC-7962 as a meaningful shift in the token ownership primitive: instead of binding balances and ownership to publicly linkable Ethereum addresses, it binds them to a cryptographic key hash (keyHash = keccak256(key)) and authorizes critical actions (notably transfers) via EIP-712 typed signatures with nonce and deadline-based replay protection, allowing any caller (e.g., a relayer) to submit the transaction without inheriting control—thereby enabling gas sponsorship and operational separation between “who controls the asset” and “who pays/executes.”

In my view, the proposal is technically coherent and security-conscious in its explicit verification and anti-replay design, and it can materially reduce address-centric linkability when combined with disciplined key rotation and relayer hygiene; however, it is not a drop-in replacement for ERC-20/ERC-721 because the ecosystem is fundamentally address-indexed, so real adoption will likely concentrate first in relayer-native verticals (consumer apps, games, privacy-sensitive collectibles, and certain institutional flows) and depend heavily on wallet UX, key lifecycle management, and adapter patterns that restore interoperability with existing tooling and DeFi composability.


*(36 more replies not shown)*

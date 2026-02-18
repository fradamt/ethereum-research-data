---
source: magicians
topic_id: 23262
title: "ERC-7913: Key Verifiers"
author: Amxx
date: "2025-03-25"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7913-key-verifiers/23262
views: 238
likes: 7
posts_count: 7
---

# ERC-7913: Key Verifiers

### Update Log

- 2025-03-21: initial draft Add ERC: Signature Verifiers by Amxx · Pull Request #986 · ethereum/ERCs · GitHub

## Replies

**xinbenlv** (2025-04-06):

Hi [@amxx](/u/amxx) glad to see this ERC which generalize the signature verifications.

> A signer is a bytes object that is the concatenation of an address and optionally a key: verifier || key. A signer is at least 20 bytes long.

Question, was it intentional that byte packing rules was left out in `verifier || key` as out of scope in this ERC?

---

**Amxx** (2025-04-07):

There have been internal discussion with the other authors has to was is in scope and what is not.

IMO the encoding (`verifier || key`) and the verification process that is documented in the “Reference Implementation” section should be standard. It was decided otherwise so that this ERC is not depending on 1271. Currently, only the verifier interface is in scope.

Do you think signer encoding should be more formally standardized?

---

**xinbenlv** (2025-04-07):

IMHO in scope or out of scope, it’s fine either way. Just need to clarify in spec. So if you choose to leave it out of scope, please consider mentioning in Spec section too.

---

**ernestognw** (2025-05-30):

Since its publication, we’ve been working on ERC-7913 developments that enabled very expressive and standard use cases for smart accounts.

**Account Signers**

- SignerERC7913
- MultiSignerERC7913
- MultisignerERC7913Weighted

**Account Modules (ERC-7579)**

- ERC7579Multisig module
- ERC7579MultisigWeighted module
- ERC7579Confirmation module

**Utilities**

- ERC7913Utils

**Verifiers**

- ERC7913P256Verifier
- ERC7913RSAVerifier
- ERC7913ZKEmailVerifier

---

**ernestognw** (2025-08-21):

Hi all!

I’ve been thinking about ERC-7913 in the context of frontend UIs and wallets. So far the ERC enables arbitrary signature verification so the UI doesn’t really need to know the signature algorithm as long as the user provides it with a valid one. However, there’s no standard way to request ERC-7913 signatures.

As opposed to EOAs that use regular wallets (e.g. Metamask) or smart contracts that may have their own UI, a frontend would need to know information about the verifier so it can ask the user for the signature. For example, if a verifier is a Groth16Verifier for ZKEmail proofs, then the frontend must be able to show a dialog waiting for an email to be sent and proved.

I was thinking the ERC could benefit from something like suggesting the following getters:

```solidity
interface IERC7913SignatureVerifier {
  // Existing
  function verify(bytes calldata key, bytes32 hash, bytes calldata signature) external view returns (bytes4);

  // OPTIONAL/RECOMMENDED
  function algorithm() external view returns (string memory);
  function version() external view returns (string memory);
}
```

Thoughts?

---

**Amxx** (2025-08-22):

Overall, I see two types of entities to interract with ERC-7913 verifiers:

- signers that support ONE algorithm, and know the address a verifier they trust to correctly verify the signature they produced. When these signers are asked what their “identity” is, they will provide the ERC-7913 formated identity (verifier+key)
- signature consumers, that given any identity and any signature are able to check if the signature is valid for that identity.

The first one knows what verifier to use. I don’t see them needing to do “feature discovery”. The second one doesn’t need to know how the signature is verified, so they also don’t need to do “feature discovery”.

---

To address you question about “there’s no standard way to request ERC-7913 signatures”. I don’t think there needs to be.

Right now, app application just “requests a signature”, and the wallet will provide a signature. That signature would be ECDSA. It could also be a ERC-1271 signature, which the wallet can build however it wants. In the case of multisig wallets, that “building the signature” may include multiple signer getting notifications, doing individual signatures, and the wallet gattering that into one big multisignature.

IMO wallets/signers that use 7913 would do just the same, in the sens that the app would request a signature for a given identity they support.

IMO, If there is something to standardise here its the “asking the signer what its identity is, getting a ERC-7913 identity back (>20bytes), and supporting that”. That would be a Wallet/Signer interface ERC.

---

As I mentioneed, I see ERC-7913 as an “extension” of ERC-1271. In both cases I believe its (only) about signature verification and not about signature generation. In the case of ERC-1271, there isn’t any function similar to the `algorithm` or `version` that you propose, and as we saw, this is just fine. Wallets know what account they are signing for, and generate the signature accordingly. IMO the same applied to ERC-7913.

That doesn’t mean that if someone wants to add `algorithm()` or `version()` they shouldn’t do it. But I don’t think we need to standardize these function in ERC-7913. I also believe these function would create more questions:

- What are the strings returned? Do we standardize them? If yes, in ERC-7913?
- Who is going to consume the strings? It feels to me like this is mostly (only?) going to be used by offchain components like wallets/signers. They will likelly have to maintain a algorithm()/version() database to interpret what these functions return… so at that point its just as easy to have an verifier address database.


---
source: magicians
topic_id: 15712
title: "Proposal for a New EIP: Batch EIP-712 Signing"
author: nathanglb
date: "2023-09-08"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/proposal-for-a-new-eip-batch-eip-712-signing/15712
views: 823
likes: 3
posts_count: 4
---

# Proposal for a New EIP: Batch EIP-712 Signing

EIP-712 enabled the signing of typed data, which is great for gasless approvals.  To name a couple common use cases, EIP-2612 Permits for ERC20 tokens and gasless off-chain NFT listings and offers.  Prior to EIP-712, users signed an incomprehensible array of bytes (dangerous).  With EIP-712 Web3 wallets now have a formalized way to present human readable information for signature (less dangerous).

Currently though, `eth_signTypedData` in a JSON RPC and web3 wallets only support the signing of a single signature at a time.

Motivation:

Consider the example of an NFT marketplace where a user wants to approve a batch of similar approvals.  Listing many NFTs for sale with one signature.  To create individual signed approvals for 25 items, a user would have to list their NFTs one at a time - a tedious task with a bad UX.  An improved UX would be to allow a user to select 25 of their NFTs to list in a single atomic action.

Some marketplaces solve for this by using Merkle Proofs - in effect, users sign a Merkle Root where the leaves in the merkle tree contain the individual orders that can be verified by supply the user’s merkle root and the proofs of the items being purchased.  This is a highly over-engineered solution with a couple of problems.

1. Signing a merkle root (bytes32) is an opaque blind signature - a false merkle root could be presented by a malicious application to trick a user into signing off on listings to their own detriment.
2. If an entire tree structure is signed, the data is technically readable, but verbose enough with so many levels that a user may not fully read it.  Furthermore, to ecrecover the full signature, all the data must be available to reconstruct the structured data and recover the signer address.  This can potentially bloat calldata.
3. The use of merkle proofs can add additional gas overhead that wouldn’t be present if an array of simpler signed approvals could be provided instead of merkle root and proofs.

Proposal:

An update to web3 wallets. To support generation of multiple EIP-712 signatures with a single click to “sign”.

Currently users are presented with human readable typed data for each EIP-712 signature.  Update the UI of wallets to include “pages”, where each “page” provides the details of one of the signatures in the batch.  Make navigation between pages streamlined and simple.  Disable the sign button until all pages have been viewed.

For security, each EIP-712 signature requested in a batch MUST be for the same domain separate and message type (no mixing of approval types, only allow batches of the same type).

After review of all signature data pages is complete, enable the “Sign” button of the wallet.  The wallet MUST then use the unlocked account private key to generate and return an array of individual signatures for each requested typed data message.

Recommendation is to create a new RPC and new library functions rather than edit existing functionality.  Possibly:

- eth_signTypedDataBatch
- personal_signTypedDataBatch
- web3.eth.signTypedDataBatch
- web3.eth.personal.signTypedDataBatch

## Replies

**0xth0mas** (2023-09-08):

Having discussed this briefly with Nathan prior to posting, I am in favor of a method for passing batch signing requests to wallets as it would greatly improve user experience in dapps where a user is performing multiple actions with EIP712 signatures.

The actual wallet UX should be up to the wallet provider in how they implement the batch signing whether it’s a summary that can be drilled down into or requiring paging through.

Limiting batch signatures to a common domain and primary type would mitigate the security issue of a malicious website injecting an unexpected signature request with other signatures. This would also make the request JSON a simple modification from the existing EIP712 signature specification with the message object being replaced with a messages array that the wallet iterates over with a common set of domain and type parameters. Similarly the response JSON can replace result value with a results array with each signature in the array corresponding to the same index message in the messages array.

If we are going to move forward with an EIP that will gain adoption with wallet providers to refresh the message signing UX, I would like to use the opportunity to also include a method for taking signatures from “human readable” to human readable. Function calls are simple for wallet providers to determine what is taking place and provide warnings to users (i.e. “you are about to grant approval for this address to transfer X tokens”) but EIP712 signature structure can vary widely from contract to contract with different meanings.

To accomplish that we could explore a markdown format supplied via a URI that is included in the domain type hash that allows for actual human readable interpretations of the typed data being signed. Being part of the domain type hash would prevent malicious parties from replacing the interpretation markdown with false descriptions that do not align with what the contract developer intended.

---

**ashhanai** (2024-04-01):

Thank you, [@nathanglb](/u/nathanglb), for kicking off this conversation. I like the idea of batch signatures and would like to dust off the discussion again. Are there any updates?

Restricting batch signatures to the same domain makes a lot of sense, and I agree with [@0xth0mas](/u/0xth0mas) that the UX should be left to wallet providers with some recommendations in this discussion but not in the EIP itself.

Even though I understand the motivation to make signatures more human-readable, it isn’t a good idea to introduce a URL to the domain in this EIP as it would be inconsistent with the current EIP-712. Another EIP can be introduced that will extend the EIP-712 domain with an optional descriptor URL.

---

**nathanglb** (2024-04-02):

It would be great to see this kick off again.  I haven’t seen any enthusiasm for this from wallet providers.  This is unfortunate, because it forces protocols to do more complex merkle-based logic specific to their individual protocols, which is tricky to get right.


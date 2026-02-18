---
source: magicians
topic_id: 25201
title: "ERC-8010: Pre-delegated Signature Verification"
author: jxom
date: "2025-08-21"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8010-pre-delegated-signature-verification/25201
views: 253
likes: 6
posts_count: 8
---

# ERC-8010: Pre-delegated Signature Verification

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1186)














####


      `master` ← `jxom:jxom/signature-verification-predelegation`




          opened 07:22PM - 21 Aug 25 UTC



          [![](https://avatars.githubusercontent.com/u/7336481?v=4)
            jxom](https://github.com/jxom)



          [+141
            -0](https://github.com/ethereum/ERCs/pull/1186/files)













This ERC defines a signature verification procedure that enables signature validation for accounts that intend to delegate via [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) before onchain delegation occurs. The standard introduces a detectable signature wrapper containing an [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) authorization and initialization data, allowing verifiers to simulate the delegation and validate signatures through [ERC-1271](https://eips.ethereum.org/EIPS/eip-1271) in a single atomic operation.

## Replies

**frangio** (2025-08-21):

ERC-6492 places the marker at the end of the signature, could this be done with this ERC as well? It would allow the verification procedure to check for markers in a single place.

It looks like this scheme only enables off-chain verification, right?

If the user delegated to a contract in the past and then redelegated to another contract, signatures for the first delegation should probably be invalidated. I don’t think Step 2 correctly handles this. What would handle it is to check the account nonce.

---

**jxom** (2025-08-22):

> ERC-6492 places the marker at the end of the signature, could this be done with this ERC as well? It would allow the verification procedure to check for markers in a single place.

Yes, fair. I updated the spec accordingly.

> It looks like this scheme only enables off-chain verification, right?

For now, yes. Unfortunately, it is not very trivial (or possible?) to do this onchain right now.

> If the user delegated to a contract in the past and then redelegated to another contract, signatures for the first delegation should probably be invalidated. I don’t think Step 2 correctly handles this. What would handle it is to check the account nonce.

Will amend!

---

**Ivshti** (2025-08-27):

I propose that we find a way to develop this ERC into a **replacement** / **successor** of ERC-6492.

here’s why

- 6492 defines the verification order, which is important for correctly verifying signatures
- 6492 defines an easy way to verify all types of signatures
- the flow and principle of operation is almost the same

The first two traits make life significantly easier for devs.

You could argue that having this implemented correctly in viem is sufficient and dev ergonomics shouldn’t be that important, but this is not the case

- a majority of the ecosystem still uses ethers which is notoriously behind on signature verification (still oblivious to 1271 Add support for EIP-1271 signature verification in the utils package by Ivshti · Pull Request #3904 · ethers-io/ethers.js · GitHub)
- a majority of the ecosystem has their own signature verification flow that they cannot easily replace

Additionally, I could argue that introducing a third EIP into this mix will just make many good-intentioned devs who are trying to keep up with the AA ecosystem just rage quit on signature verification. In other words, mixing 6492 and 8010 verification will be at best slightly annoying, at worst quite the mess (I know in theory you just have to check magics, in practice you branch off code that might already be very branch-y).

A very concrete example of this confusion: when reading 8010, there’s some ambiguity of when 6492 need to be performed: part of the ERC states clearly that it should be done if MAGIC is not found, but there’s no explicit instruction/consensus of which ERC should apply it’s logic first, furthermore in most practical cases you might be tempted to identify the type of the account first, which is a can of worms in itself. Two ERCs simply adds way too much ambiguity to order.

Already in touch with [@jxom](/u/jxom) about this

Sidenote: I was originally doubting the value of 7702 counterfactual verification altogether, before I remembered about PREP, which introduces a very valid reason for this to exist.

---

**Ivshti** (2025-08-28):

On second thought, I think the best approach is to reference the 6492 algorithm in this ERC for all signatures that are NOT 7702 counterfactual signatures

This way, the flow is very clear, and we don’t have the same information across multiple ERCs

---

**jxom** (2025-08-31):

Amended the ERC to your recommendations!

---

**ogunsakin** (2025-10-03):

thanks for proposing

similar concern about about stale nonce but not sure I see a way around it currently.

[@jxom](/u/jxom) can we validate `chain_id` to prevent cross-chain replay

---

**jxom** (2025-10-09):

The node would validate `chain_id` on the `eth_call` authlist, no?


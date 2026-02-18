---
source: magicians
topic_id: 11059
title: ERC-5719 - Signature replacing for smart contract wallets
author: Agusx1211
date: "2022-09-26"
category: EIPs
tags: [wallet, signatures]
url: https://ethereum-magicians.org/t/erc-5719-signature-replacing-for-smart-contract-wallets/11059
views: 2404
likes: 3
posts_count: 8
---

# ERC-5719 - Signature replacing for smart contract wallets

This is an extension proposal to EIP-1271, it addresses the issue of smart contract wallet signatures becoming invalidated and breaking certain dapps.

For example:

Assume a multisig smart contract wallet with signers X and Y, you use signer X to list some assets on opensea, 2 weeks later you replace signer X for a new signer, Z. Without any additional measures, the listing becomes invalidated.

Using this EIP the wallet can use signer Z to re-sign the message, and the dapp can non-interactively fetch the signature as a replacement.

https://github.com/ethereum/EIPs/pull/5719

## Replies

**PhABC** (2022-09-29):

It would be helpful if the rationale section included why a fully on-chain solution was not chosen. It’s stated that URI can be used with both centralized and decentralized systems, but not *why* URI is a better choice over a fully on-chain system.

---

**SamWilsn** (2022-10-04):

This solution won’t work for contracts that forward the signature. For example, you could have an approve-transfer batch contract (using something like Dai’s `permit`.) The off-chain application might have no idea a signature is being used in a subcall, and so won’t know that it needs to retry.

---

**Agusx1211** (2022-10-04):

The top-level caller should still be able to detect the signature is stale and do the replacing. Maybe the EIP should specify that all signatures should first be validated using EIP-1271 (and replacing if needed), even if that signature is going to be used for something other than direct validation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> The off-chain application might have no idea a signature is being used in a subcall, and so won’t know that it needs to retry.

Is this a common thing? if a signature is used internally then it’s most likely an input of the top-level caller, a contract that *stores* signatures could lead to the scenario, but I haven’t seen that pattern out there.

This scenario is hard to cover because the smart contract wallet doesn’t have that information on-chain (otherwise it could just accept the digest and ignore the signature), but at least the edge case reverts back to the status-quo (the stale signature fails).

---

**SamWilsn** (2022-11-25):

I just noticed that you don’t define which algorithm to use for `_digest`. Probably should do that.

---

Have you considered using an [EIP-1155](https://eips.ethereum.org/EIPS/eip-1155#metadata) style URI format, where the client is expected to substitute `{digest}` in the returned string with the digest value? If there’s some technical reason why that wouldn’t work, might be good content for the Rationale section.

---

**Agusx1211** (2022-11-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I just noticed that you don’t define which algorithm to use for _digest. Probably should do that.

My bad, `digest` is meant to be the `hash` as defined by EIP-1271. That can be a little bit confusing, I will update the EIP so it uses the same nomenclature.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Have you considered using an EIP-1155 style URI format, where the client is expected to substitute {digest} in the returned string with the digest value?

This is an interesting idea, the biggest benefit is that a client wouldn’t need to call the contract to fetch every replacement URL. I think this makes more sense on metadata (because you usually need to fetch N tokens), Signature replacement is only triggered when a signature is found to be invalid, so a 1 by 1 basis.

---

**SamWilsn** (2022-11-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/agusx1211/48/2305_2.png) Agusx1211:

> the biggest benefit is that a client wouldn’t need to call the contract to fetch every replacement URL

I was thinking that it would save code space in the contract wallet, instead of having to convert a `bytes32` to hex.

---

**SamWilsn** (2022-11-25):

We’re trying a new process where we get a volunteer peer reviewer to read through your proposal and post any feedback here. Your peer reviewer is [@abhinavmir](/u/abhinavmir)!

If any of this EIP’s authors would like to participate in the volunteer peer review process, [shoot me a message](https://ethereum-magicians.org/new-message?username=SamWilsn&title=Peer+Review+Volunteer)!

---

[@abhinavmir](/u/abhinavmir) please take a look through [EIP-5719](https://eips.ethereum.org/EIPS/eip-5719) and comment here with any feedback or questions. Thanks!


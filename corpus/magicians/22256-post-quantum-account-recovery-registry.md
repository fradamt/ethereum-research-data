---
source: magicians
topic_id: 22256
title: Post-quantum account recovery registry
author: iAmMichaelConnor
date: "2024-12-17"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/post-quantum-account-recovery-registry/22256
views: 128
likes: 3
posts_count: 1
---

# Post-quantum account recovery registry

> The ERCs repo README says “Before you write an ERC, ideas MUST be thoroughly discussed on Ethereum Magicians or Ethereum Research”
>
>
> So here I am
>
>
> If this gets sufficient traction, I’ll draft and open an ERC for the registry contract.

Vitalik sets the scene nicely in his related post [How to hard-fork to save most users' funds in a quantum emergency - Execution Layer Research - Ethereum Research](https://ethresear.ch/t/how-to-hard-fork-to-save-most-users-funds-in-a-quantum-emergency/18901). There, he explains that *“most users’ private keys are themselves the result of a bunch of [quantum resistant] hash calculations”*, and that for these users, we have a neat way to enable them to migrate their accounts in the event that quantum computers start stealing funds.

This post seeks to enable the remaining users – those whose private key was not derived via some quantum-resistant hashing of a seed – to migrate. (It’s worth noting that it’s not just applicable to those users; it’s widely applicable to any Ethereum account).

## The proposal

The proposal is for a basic registry smart contract to be designed, deployed, and universally recognised.

## Overview

A new “Post-quantum account recovery registry” contract (the “Registry”) is deployed. Preferably, a single registry is universally agreed-upon and recognised, to make a future migration of accounts as smooth as possible.

User flow:

- A user derives some secret of type bytes.
- They commit to the secret with some quantum-resistant hash, such as sha256:

commitment = sha256(secret).

They submit this `commitment` to the Registry.
The Registry stores the `commitment` against the user’s `address` in a mapping.

Should quantum computers then appear powerful enough, the process for migrating would look much like Vitalik described in the above-linked post. Quoting here, but with bold text highlighting a modification that serves this proposal:

"

*1. Revert all blocks after the first block where it’s clear that large-scale theft is happening

2. Traditional EOA-based transactions are disabled

3. A new transaction type is added to allow transactions from smart contract wallets (eg. part of [RIP-7560](https://ethereum-magicians.org/t/rip-7560-native-account-abstraction/16664)), if this is not available already

4. A new transaction type or opcode is added by which you can provide a STARK proof which proves knowledge of **`secret` for a given (`address`, `commitment`) tuple in the Registry**. The STARK also accepts as a public input the hash of a new piece of validation code for that account. If the proof passes, your account’s code is switched over to the new validation code, and you will be able to use it as a smart contract wallet from that point forward.*

"

The transaction mentioned in step 4 could either:

- make a view call to the Registry to validate the (address, commitment) tuple.
- include a storage proof to the Registry’s storage slots.

## Interface

To be refined. My Solidity is rusty and I’m going off memory; forgive me. Let’s call it pseudocode, to protect me.

```js
contract PostQuantumAccountRecoveryRegistry {
  // This mapping has an implicit getter (right?)
  public mapping(address => bytes32) commitments;

  external function submit_commitment(bytes32 commitment) {

      // See section below for whether we should allow users
      // to overwrite their commitment. Here, I disallow it.

      assert(commitments[msg.sender] == 0);

      commitments[msg.sender] = commitment;
  }
}
```

## Discussion

### Is it useful?

The scheme requires users to actively recognise the future threat of quantum computers and submit a transaction to the Registry. For users who can prove derivation of their Ethereum private key via a quantum-resistant hash, the above-linked proposal by Vitalik might be preferred, since it is non-interactive until quantum computers arrive.

Even for users not captured by Vitalik’s proposal, they *could* manually migrate their assets to an account whose private key *does* satisfy Vitalik’s proposal. That said, such a manual migration might not be desirable: it’s arguably inconvenient; there might be defi positions that the user is unwilling to unwind; the user’s tokens might be locked, or subject to withdrawal delays; the cost in fees of migration might be too great; the risk of exposing a cold wallet for multiple transactions might be considered too high; the user might accidentally send to the wrong address.

This proposal at least offers this class of users an alternative option, through a single, inexpensive transaction to the Registry.

### Do we need all of the migration details?

An interesting observation is that the details for *how* exactly we (the community) would handle a big post-quantum migration doesn’t necessarily need to block the progress of this proposal: all it proposes is the existence of a Registry that stores commitments. People can even begin submitting commitments before we’ve worked out the rest of this. Once the commitments are there, we would then have time to decide how to prove their preimages and migrate accounts.

Having said that, the `secret` *does* likely need to be provided as a witness to a STARK at the time of migration, and so the `secret` needs to be generated with that in mind. If the `secret` lives on a hardware wallet, and we can’t extract that `secret`, and that hardware wallet won’t ever support STARKs, the `secret` might be useless. I guess Vitalik’s above-linked post has this same problem?

### Is this secret less secure than the user’s private key?

`sha256` is available on hardware wallets, so solutions exist to avoid the `secret` ever entering a “hot” device. Having said that, the previous section suggests that the `secret` will eventually need to be accessible to be used in a STARK witness. (It’s a shame we’re not allowed to use elliptic curves, or we could use Schnorr!!)

### Can a user overwrite their commitment?

There’s a tricky problem that if someone gains possession of a powerful quantum computer, they could technically impersonate all users and overwrite all of the commitments in the Registry, rendering the Registry useless. For that reason, I’m erring on the side of disallowing overwrites. After all, if a user loses or leaks their `secret`, that’s akin to losing or leaking their private key.

One could perhaps add a 6-month delay to overwrite requests. That way, if the mysterious, powerful quantum computer does successfully manage to inconspicuously overwrite users’ commitments, we can make the assumption that wouldn’t be able to restrain themselves from doing *something* wildly *con*-spicuous within the first 6 months of having this super power. If we see something fishy (like the transferring of Satoshi’s bitcoin), we can disregard all overwrite requests that took place within the 6 months prior to that incident.

## Next steps

Criticise this. Suggest improvements.

If it gets traction, we can open an ERC.

Then we can design, build, audit, and deploy the Registry.

Question: Since the above “migration” steps of this would require an *EIP* (not an ERC), does that technically make this an EIP?

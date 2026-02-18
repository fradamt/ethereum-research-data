---
source: ethresearch
topic_id: 14930
title: A simple persistent pseudonym scheme
author: lsankar4033
date: "2023-03-01"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/a-simple-persistent-pseudonym-scheme/14930
views: 2832
likes: 14
posts_count: 7
---

# A simple persistent pseudonym scheme

*co-authored with [@0DanielTehrani](/u/0danieltehrani)*

*EDIT: added signature check on `contentData` on recommendation from [@enricobottazzi](/u/enricobottazzi)*

In this post, we present a simple scheme for persistent (pseudo)nyms based on Eth set membership.

## Why?

Use of Ethereum naturally places one in a number of important, identity-defining ‘sets’. Sets like:

- all holders of NFT X
- voters in DAO Y
- liquidity providers to protocol Z at time T

We believe one’s existence within such a set is an identifier of growing importance in the crypto+internet economy. And we believe that being able to do so while maintaining privacy is a fundamental human right.

So why pseudonyms? We’ve observed (i.e. in [heyanoun](https://heyanoun.xyz/) and [heyanon](https://www.heyanon.xyz/)) that while Ethereum users have things to say pseudonymously, without a persistent name to which they can accrue reputation, the flavor of interactions is quite simplistic.

This document lays out an extremely simple SNARK-based mechanism for persistent pseudonyms that allow reputation accrual.

## Properties

There are a few properties we designed this scheme around:

### nyms are ‘single-signer’

A given pseudonym must be attributable to no more than one Ethereum signer. Stated differently, a human viewing a given pseudonym’s usage anywhere on the internet must know that it’s being used by one Ethereum pub/privkey pair.

### linkage to Eth-based set membership

This one’s obvious, but worth restating. We want our pseudonyms to mean something relative to sets on Ethereum. As such, our proof mechanism must allow a pseudonym-holder to associate Eth-based sets they’re into pseudonyms they control.

### web3 wallet compatible

It’s crucial that our mechanism work with the ecosystem of tools/infrastructure that exists today. We have ideas for improvements that require heavier-weight changes to web3 wallets ([An ECDSA Nullifier Scheme for Unique Pseudonymity within Zero Knowledge Proofs](https://eprint.iacr.org/2022/1255)), but testing applications with these improvements would require many entities in industry (wallets) to make a uniform change to their infra.

### non-interactive, stateless

At this stage, we’re most interested in the simplest, easiest to use mechanisms. Too many layers of interaction could make something unusable and complicated economics could get in the way of agile experimentation.

Thus, we designed our mechanism to be stateless (i.e. no chain state management) and require minimal interaction from a user.

### (semi-)human choosable and (semi-)human recognizable

We want humans to:

1. be able to express themselves with their nym
2. be able to recognize/remember nyms they see online

2 is crucial for reputation accrual. We want our nyms to make sense to human minds.

1 allows nyms to be open to human creativity.

Because we’re requiring statelessness at this point, we need to combine the ‘human-grokkable’ part of a nym with a collision-resistant ID, to avoid name collisions.

The result is nyms of the format {human-readable-segment}-{UUID}, i.e. ‘alice-2443212411’

One way in which state might be added to nym ownership in the future is via an ENS-like registry of ‘vanity’ nyms, but we consider this outside of the scope of this note.

## Proof scheme

We utilize the following circuit pseudocode to associate nyms with activity:

```auto
circuit ProveNymOwnership {
  // hash is machine-readable UUID, code is human-readable segment
  pub input nymHash
  pub input nymCode

  // ECDSASign(nymCode)
  priv input signedCode

  // i.e. merkle root/proof
  pub input ethSetAccumulator
  priv input ethSetProof
  priv input ethPubkey

  // content that user is producing from their nym
  pub input contentData
  priv input signedContentData

  // check 1
  signedCode === ECDSASignVerify(ethPubkey, nymCode)
  nymHash === Hash(signedCode)

  // check 2
  verifySetMembership(ethSetProof, ethSetAccumulator, ethPubkey)

  // check 3
  signedContentData === ECDSASignVerify(ethPubkey, contentData)
}
```

check 1 ensure that the human readable and unique/UUID pieces of the pseudonym are related by a private signature. because the signature is private, the user’s identity is concealed and because the UUID piece of the pseudonym is derived from the signature, we can be assured that only a single ETH signer can produce a given `nymHash`

check 2 is the same set membership check we’ve used in previous applications.

check 3 assures that the content is ‘labeled’ with this pseudonym, similar to use in previous applications.

The combination of checks here ensures that:

1. a given pseudonym is known to be associated with 1 or more Eth sets
2. only a single Ethereum signer can produce a given pseudonym
3. 2 signers are extremely unlikely to collide on nymHash even if they choose the same (human-identifiable)nymCode

The nyms as shared on the internet (i.e. human-readable venues) can be of the form:`${nymCode}-${nymHash}`, i.e. ‘alice-2443212411’ as mentioned before.

`nymHash` can be be used in any venue where machine-readability is all that matters (i.e. interpretability in the EVM/smart contracts).

Finally, we use 1 or more unconstrained public inputs to pin this proof to the ‘content’ the user is attaching the proof to.

At first, this may simply be threaded messages (as in heyanoun v2), but we’re keeping the core mechanism general enough for this content to be anything from a social media post to an Ethereum transaction. We believe this scheme can be used to label almost any piece of information on the internet with an Eth-based pseudonym.

## UX

To use a nym = `${nymCode}-${nymHash}`, a user creates a proof for the desired combination and the set they’re claiming membership in. He/she also associates the proof to the piece of content he/she is creating via the unconstrained input `contentData`

Note that a user can’t ‘spoof’ a known `nymHash`; they can only produce `nymHash`-s corresponding to ECDSA signers they control.

Users choose how to associate {nym, proof, anonymity set, content} online.

One slight hitch is that a user must keep track of `nymCodes` they correspond to. Given that humans already remember social media handles, this doesn’t seem like too much trouble.

However, even if he/she doesn’t, as long as he/she has access to some content/nyms he/she *might* have used in the past, the nyms can be tested by re-signing and seeing which `nymHash`es correspond to his/her signer.

## Extensions

There are a number of extensions on this model that we’re excited to flesh out and experiment with.

(briefly) 2 ideas:

1. use ‘previous proof hash’ in contentMetadata as a way to create ‘discussion threading’
2. ‘nym/reputation’ merging by generating a proof showing that one can create 2 or more nymHashes

For brevity’s sake, we’ll save fleshing these (and other ideas) out for a future post!

## Replies

**enricobottazzi** (2023-03-01):

Hi [@lsankar4033](/u/lsankar4033) [@0DanielTehrani](/u/0danieltehrani).

Very intriguing idea, as always! I have a few questions:

1. How would you ensure that the content identifier by contentData is actually produced by the signer? In applications such as Semaphore or Heyanon the signal needs to be signed and this is added as a constraint inside the circuit
2. Is the Nym persistent across different membership sets? If so, does it pose any risk of breaking the privacy of the pseudonym? For example, if my address belongs to two different membership sets (and it is the only one that belongs to both sets), as soon as I publish

content using my pseudonym together with a membership proof of group A
3. content using my pseudonym together with a membership proof of group B

It would be trivial to retrieve the identity behind the pseudonym

---

**lsankar4033** (2023-03-01):

intriguing questions, as always ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

> How would you ensure that the content identifier by contentData is actually produced by the signer? In applications such as Semaphore or Heyanon the signal needs to be signed and this is added as a constraint inside the circuit

good point. the original thought here was that the proof only binds the pseudonym. of course, this means that the `contentData` isn’t itself ‘labeled’, and also a single piece of `contentData` can be claimed by multiple pseudonyms.

I believe a simple alleviation is to add an optional signature check on the `contentData`. i.e. `signedData === ECDSASign(contentData, ethPubkey)`. fortunately, this doesn’t add much prover overhead thanks to spartan-ecdsa!

> Is the Nym persistent across different membership sets? If so, does it pose any risk of breaking the privacy of the pseudonym? For example, if my address belongs to two different membership sets (and it is the only one that belongs to both sets), as soon as I publish
>
>
> content using my pseudonym together with a membership proof of group A
> content using my pseudonym together with a membership proof of group B

anonymity set reductions b/c of set intersection is absolutely a concern here.

It seems inevitable that such reductions happen if we allow pseudonyms to exist across many different contexts (which I think is desirable). Personally believe that solutions should happen at the ‘UX/wallet’ layer instead of hte ‘protocol’ layer. Future identity wallets should flag when a user is constraining an anonymity set a certain amount and provide visibility/analytics into the anonymity of existing nyms.

One of the nice things in this scheme is that a user is always given the choice between adding to an old pseudonym or spinning up a new one (if adding to the old would reduce anonymity set too much).

---

**enricobottazzi** (2023-03-02):

> I believe a simple alleviation is to add an optional signature check on the contentData. i.e. signedData === ECDSASign(contentData, ethPubkey). fortunately, this doesn’t add much prover overhead thanks to spartan-ecdsa!

I think that is a necessary add-on. Do you see any use case where this extra signature check wouldn’t be required?

Also, I haven’t checked out spartan-ecdsa yet, but how does it fit with the standard zk dev tooling? Taking heyanon as example, how would it be compatible with the existing circuit built with circom-snarkjs-groth16 prover?

---

**lsankar4033** (2023-03-02):

> I think that is a necessary add-on. Do you see any use case where this extra signature check wouldn’t be required?

yep, have already added it as an edit to the main post!

> Also, I haven’t checked out spartan-ecdsa yet, but how does it fit with the standard zk dev tooling? Taking heyanon as example, how would it be compatible with the existing circuit built with circom-snarkjs-groth16 prover?

yep. spartan operates on r1cs, so circom can be used (utilizing [@nibnalin](/u/nibnalin) 's nova-scotia compiler to properly format intermediates). some sample circuits here: [spartan-ecdsa/packages/circuits at main · personaelabs/spartan-ecdsa · GitHub](https://github.com/personaelabs/spartan-ecdsa/tree/main/packages/circuits)

---

**enricobottazzi** (2023-05-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/lsankar4033/48/10215_2.png) lsankar4033:

> We have ideas for improvements that require heavier-weight changes to web3 wallets (An ECDSA Nullifier Scheme for Unique Pseudonymity within Zero Knowledge Proofs ), but testing applications with these improvements would require many entities in industry (wallets) to make a uniform change to their infra

Hey [@lsankar4033](/u/lsankar4033), I was coming back to the post (: I’m wondering how would you even benefit from a deterministic ECDSA nullifier for such an application. A deterministic nullifier is needed for those types of applications where you want to avoid “double-spending”, that would be a required feature in the case you require the same address within a membership set to not be able to generate multiple nyms. But this doesn’t seem the case to me.

---

**lsankar4033** (2023-05-30):

sorry for the slow response!

in some sense, this scheme is designed to not require deterministic nullifiers. It feels like we’ll eventually need them though though; I believe we’ll eventually need to make something ‘not-reusable’ in the naming stack.

The goals with this scheme are mostly around providing a minimal framework from which we can test user behavior!


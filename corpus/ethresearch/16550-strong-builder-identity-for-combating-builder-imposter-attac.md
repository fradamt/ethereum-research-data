---
source: ethresearch
topic_id: 16550
title: Strong Builder Identity for Combating Builder Imposter Attacks
author: MaxResnick
date: "2023-09-05"
category: Cryptography
tags: [mev]
url: https://ethresear.ch/t/strong-builder-identity-for-combating-builder-imposter-attacks/16550
views: 2654
likes: 18
posts_count: 4
---

# Strong Builder Identity for Combating Builder Imposter Attacks

# Strong Builder Identity

co authored with [@kobigurk](/u/kobigurk) from Geometry and [@mmp](/u/mmp) from SMG

Thanks to [@akinovak](/u/akinovak) for comments.

5 Hours ago, [Titan Builder announced on twitter](https://twitter.com/titanbuilderxyz/status/1699057370197049533?s=20) that they had evidence of a builder impersonating them. In the post Titan described how an imposter has been using Titan’s extradata, “Titan (titanbuilder.xyz)”, in blocks produced by the imposter. The imposter also set Titan’s address as the block recipeint (titanbuilder.eth). The only identifying information that the attacker couldn’t spoof was the proposer payment transaction which it sends from [(titanpayload.eth)](https://etherscan.io/name-lookup-search?id=titanpayload.eth).

You can see a recent [example imposter block here.](https://etherscan.io/block/18072350)

What the imposter is trying to acomplish is unclear at this stage. That said, as of the time of writing, [Titan estimates](https://twitter.com/titanbuilderxyz/status/1699057372277432340?s=20) they have spent over 17 eth and an attacker rarely does this without a plan for making it back.

There are also possibly connected reports of a [flashbots imposter](https://twitter.com/nero_eth/status/1699125497014145080?s=20).

Motivated by this, we suggest a stronger builder identity system. Rather than rely on plaintext extradata to identify builders, which is easy to spoof, the extradata should be used for a builder signature.

The main design constraint we have is that the system must integrate into the current block structure.

## Components

### BN254 BLS signatures

BN254 is a pairing-friendly curve commonly used for SNARKs, and has cryptographic operations precompiled on Ethereum since EIPs 196 and 197.

BLS signatures are a pairing-based signature scheme, where the signature is a single group element. For BN254, this means we can encode a signature in 32 bytes.

Additionally, it’s possible to (somewhat) [efficiently verify BLS signatures on Ethereum](https://ethresear.ch/t/bls-signatures-in-solidity/7919).

### Registry

The registry smart contract would accept the following from builders:

- Builder info:

Name
- BN254 public key
- .eth address and a signature from it (or some other identifiying mechanism)

BN254 signature on the builder info hash

The registry would verify the signature before approving the builder.

The builder info would be stored in an append-only list, and the builder would keep their index in this list, denoting it **builder index**.

### Graffiti

The builder has the ability to set the *extra data* field in a block, which is 32 bytes long. The builder would put a BLS signature on the block hash in the extra data.

Proposers may verify the signatures before proposing, but they don’t have to.

### Gas limit watermarking

The builder also has to tell the signature verifiers which builder they are, and they don’t have enough space in the extra data anymore.

Note that the builder can at least control the last 3 digits in the gas limit arbitrarily, allowing them to use it for their builder index.

### Verifiers

Verifiers would then get the corresponding name and public key from the smart contract.

Explorers can use this data to verifiably display builder identities in blocks.

### Limitations

Note that with current relay design, the relay can change the gas limit unilaterally, which may be a concern. However, a malicious relay can already do a lot worse things than this in the present design, so we are comfortable assuming a trusted relay.

### Other design possibilities

- Use longer but cheaper signatures and encode them in the proposer payment transfer transaction. The problem is that the proposer payment transfer txn does not always exist
- Encode the builder index in the same place. Same problem

## Replies

**sui414** (2023-09-06):

Adding some data investigation here on the imposter behavior (as time of Sep 5 evening PT):

There are multiple builder pubkey appeared as imposters: 1 for flashbots, 10 for Titan (not including 0xabf1ad5e in titan’s list active June-Aug is team’s testing instance - confirmed by their team)

[![image](https://ethresear.ch/uploads/default/optimized/2X/5/5f165c5f78c1d87770a6fb87d46c8fc57c127128_2_690x215.png)image2968×926 328 KB](https://ethresear.ch/uploads/default/5f165c5f78c1d87770a6fb87d46c8fc57c127128)

1 builder pubkey appeared in both cases that is not known/controlled by the team - is the default pubkey lots of new builder instances accidentally use - which shall be ruled out from the imposter concern: **0xaa1488eae4b06a1fff840a2b6db167afc520758dc2c8af0dfb57037954df3431b747e2f900fe8805f05d635e9a29717b**.

(split reply into multiple because of new user embedding media limits > <)

---

**sui414** (2023-09-06):

[![image](https://ethresear.ch/uploads/default/optimized/2X/3/3f021f2d314261105fbfa46d737dd61440540d7d_2_690x331.jpeg)image1920×922 150 KB](https://ethresear.ch/uploads/default/3f021f2d314261105fbfa46d737dd61440540d7d)

All of them have same activation timeframe around past few days - started the imposter behavior since Sep2 w/ flashbots’ ExtraData, then stopped w/ flashbots and started Titan on Sep5; this seems to be an indicator that the imposters behind the 2 cases are likely same entity.

UPDATE: as of Sep6 most of the pubkey stopped, with only 1 `0x82790923` still going with blocks

---

**sui414** (2023-09-06):

(updated changes / corrected after discussion with & info from Toni W, Max R)

Tracking ALL the historical blocks those builder pubkeys produced, all of them are new (i.e. no historical blocks in other timeframe) except the default pubkey - which reasonably has a history of produced blocks with ALL kinds of builder extraData signature in the past.

Based on above, summary of current understanding:

- there likely is an imposter team, started with Flashbots’ extraData and then switch to Titan (unclear if there are more builders affected);
- they spun up instances with default pubkey (and is still producing blocks with it); but also then spun up a bunch other new pubkey, who never been used and now is still pasting Titan’s extraData in their block;
- they’ve been subsidizing their blocks heavily, but unclear what’s the intention/action next; unsure if they have an endpoint to receive bundle/attract flow neither.


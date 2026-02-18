---
source: ethresearch
topic_id: 23685
title: Universal Enshrined Encrypted Mempool EIP
author: jannikluhn
date: "2025-12-17"
category: Proof-of-Stake
tags: [mev]
url: https://ethresear.ch/t/universal-enshrined-encrypted-mempool-eip/23685
views: 1089
likes: 39
posts_count: 18
---

# Universal Enshrined Encrypted Mempool EIP

This thread is for discussing the [EIP](https://github.com/ethereum/EIPs/pull/10943) to add a scheme agnostic encrypted mempool to Ethereum (number pending). Here’s the full text:

## Abstract

This EIP proposes to enshrine an encrypted mempool into the protocol. It enables users to encrypt their transactions until they have been included in a block, protecting them from front running and sandwiching attacks as well as increasing censorship resistance guarantees. The design is encryption technology agnostic by supporting arbitrary decryption key providers, which can for instance be based on threshold encryption, MPC committees, TEEs, delay encryption, or FHE schemes. Traditional plaintext transactions are still supported and progression of the chain is guaranteed even if decryption key providers fail.

## Motivation

The goal of this EIP is to prevent users from malicious transaction reordering attacks as well as increase real time (“weak”) censorship resistance of the protocol. It also aims to reduce regulatory risks of block builders and other protocol participants by temporarily blinding them. The goal is not to improve user privacy (e.g., transaction confidentiality) as transactions are publicly revealed eventually.

This proposal builds on prior work such as the [Shutterized Beacon Chain](https://ethresear.ch/t/shutterized-beacon-chain/12249) and a live, out-of-protocol implementation of the encrypted mempool already deployed on [Gnosis Chain](https://www.gnosis.io/blog/shutterized-gnosis-chain-is-live). It addresses a long-standing issue with front running and has the potential to mitigate harmful second-order effects of MEV, such as builder centralization. The design also fits naturally with enshrined proposer-builder separation (ePBS), making it a logical extension of Ethereum’s roadmap.

## Specification

In the execution layer, a contract called the key provider registry is deployed. It allows any account to register a key provider and assigns them a unique ID. Registration requires specifying a contract with a decryption and a key validation function, each of which accept a key ID and a key message as byte strings. Additionally, key providers may designate other providers as directly trusted, thereby forming a directed trust graph. We define a key provider A to trust another key provider B if and only if a directed path from A to B exists in this graph. The beacon chain replicates the key provider registry in its state, analogously to the mechanism that handles beacon chain deposits.

Encrypted transactions are added as a new transaction type. They consist of an envelope and the encrypted payload. The envelope specifies the envelope nonce, gas amount, gas price parameters, key provider ID, key ID, and the envelope signature. The encrypted payload contains the payload nonce, value, calldata, and payload signature.

In a valid block, any transaction encrypted with a key from key provider A may only be preceded by

- Plaintext transactions
- Transactions encrypted with keys from key provider A
- Transactions encrypted with keys from key providers that A trusts

In each slot, when a key provider observes the execution payload published by the builder, they collect the key IDs referenced in the envelopes of all encrypted transactions addressed with their key provider ID. For each of those, they must publish either the corresponding decryption key or a key withhold notice. The corresponding message references the beacon block hash to prevent replays in a future slot. They may do so either immediately upon observing the execution payload or delay publication to a later point in the slot.

Members of the Payload Timeliness Committee (PTC) must listen for the decryption keys referenced by all encrypted transactions, as identified by the key provider ID and key ID fields. They must validate these keys using the validation function specified in the registry contract, using a hardcoded small gas limit per key. Finally, they must attest to the presence or absence of a valid key for each encrypted transaction in the payload attestation message, which is extended for this purpose with a dedicated bitfield.

During execution payload processing, after all plaintext transactions, the envelopes of the encrypted transactions are executed as a batch. This updates the nonces of the envelope signers and pays fees from the envelope accounts. The fee covers the cost of block space used by the envelope, decrypted payload, and decryption key, as well as the computation used during decryption and key validation. Subsequently, the encrypted payloads are decrypted with the key specified by the key provider ID and key ID on the envelope using the decryption function from the key provider registry. If decryption succeeds, the resulting payload transactions are executed subject to the gas limit specified on the envelopes as well as the block gas limit. If decryption or execution fails, including if the decryption key is attested as missing by the PTC, the transaction is skipped without reverting the envelope.

## Rationale

### Key Provider Registration

Registration is encryption technology agnostic to ensure neutrality of the protocol, to minimize barriers to entry for new key providers, and to empower users to choose the optimal scheme for their purposes. An execution layer contract was chosen as a canonical way of specifying arbitrary execution logic. Registration purely on the CL is a reasonable alternative.

Many encryption schemes are inefficient to express in the EVM and therefore would require dedicated precompiles. Adding those is, however, out of scope of this EIP.

### Key Provider Trust Graph

A user who sends an encrypted transaction must not only trust their own key provider, but also any key provider used for earlier transactions in a block (see Security Considerations). While the protocol should respect the users’ trust preferences, if each user only trusts their own key provider, builders would only be able to include transactions encrypted with keys from a single key provider in each block. This is undesirable because it makes it difficult for key providers with a small market share to compete, risking to create a key provider monopoly.

On the other hand, requiring users to explicitly state which third-party providers they trust would add a transaction size overhead and make block building more difficult due to the potentially large number of competing user preferences that need to be fulfilled. As a compromise, this proposal requires key providers to make this choice. Users implicitly agree by using the key provider’s keys.

With this solution, even if a quasi-monopoly consisting of a single dominating key provider emerges and this key provider does not specify any other key providers as trusted, builders can still include transactions that use other small key providers without opportunity costs, as long as the small key providers trust the major one (and potentially each other).

### Transaction Order

The proposal effectively splits blocks into a plaintext and an encrypted transaction section. Plaintext transactions are put first, enabling builders to fully simulate the execution in this section and apply existing block building techniques and MEV extraction strategies. Builders can thus append encrypted transactions to the end of the block without opportunity costs. If the order were reversed, fees for encrypted transactions would have to be considerably higher in order for blocks that include them to be competitive in PBS auctions compared to blocks with only plaintext transactions.

### Transaction Execution

The protocol as well as builders must be protected from including encrypted transactions that end up unable to pay for gas. To ensure this is the case irrespective of the content of any encrypted payload in a block, the fee payment is part of the plaintext envelope and all envelopes in a block are executed before any encrypted payload. Gas refunds are not paid out to guarantee the fee amount the builder and the protocol will receive at block building time.

For simplicity, the encrypted payload contains a signature. A less private but more efficient alternative is to consider the envelope signer as sender.

### Decryption Key Withholding

The protocol explicitly allows decryption key providers to withhold decryption keys under conditions of their choosing. This enables them to safely implement rules to restrict which users are allowed to use which keys, e.g., based on prior payments and to prevent key ID front running attacks (see Security Considerations). On the other hand, keys that have been withheld unjustifiably may be used in custom slashing mechanisms and reliability metrics (note that the protocol records which keys are present and which ones have been present and which ones have not).

### Lack of In-Protocol Key Provider Incentives

This proposal does not enshrine a fee mechanism for key providers, nor punishments for misbehavior. This allows for a variety of incentive models to be implemented off-chain. For instance, key providers could make agreements with builders, be paid on a per-transaction basis by users, or operate as public goods. They may also subject themselves to slashing conditions for unwarranted withholding of keys to make their service more appealing to users.

### Execution Payload Encryption

A future EIP may propose to let builders use the keys from the key providers to encrypt the execution payload. This enables them to publish the execution payload immediately after constructing it, compared to publishing it only at the 50% slot mark. This would increase p2p efficiency and protect builders from missed slots due to crashes. Additionally, if the builder attaches a zero knowledge proof about which keys have been used in a block, the key revelation time window could start earlier and therefore be longer. This feature is not included in this EIP to minimize complexity.

## Backwards Compatibility

The proposal makes backwards incompatible changes to the protocol to the execution and consensus layer.

## Security Considerations

### Trusted Key Providers

Users necessarily need to trust the key providers they use to encrypt their transactions to

- not release the decryption keys early which would allow front running and sandwiching attacks
- not release the decryption keys late which would prevent execution of the transaction while the envelope fee still has to be paid.

Key providers may earn this trust by cryptographic mechanisms (e.g., threshold encryption, hardware encryption), economic mechanisms (e.g., slashing for misbehavior), governance mechanisms (e.g., voting to select socially reputable entities), or a combination of these.

To a lesser degree, users need to trust all key providers used for encrypted transactions preceding theirs in a block. This is because key providers have the option to publish or to withhold decryption keys which they can take after observing decryption keys for following transactions. This option gives them one bit of influence over the pre-state of later transactions. Maliciously chosen “decryption” schemes may make this attack much stronger by allowing directly modifying specific parts of the decryption results using crafted decryption keys or setting it outright. This effectively enables front running.

Users do not have to trust any key provider used for transactions included after theirs because the pre-state of the user’s transaction payload is not affected by later transactions’ payloads (only their envelopes, but those are chosen before any decryption keys are published). Similarly, users of plaintext transactions do not have to trust any key provider (but they continue to have to trust builders).

### Reorgs

Decryption keys are published before the corresponding encrypted transactions are finalized. Thus, in the event of a chain reorg, a transaction may become public even though it is not necessarily included in the chain. However, since the decryption key message includes the block hash, it can be invalidated by the key validation function. This does not prevent inclusion of the envelope transaction, but does prevent execution and, hence, front running of the payload.

### Key ID Front Running

When a user encrypts a transaction with a particular key ID, another user could observe this transaction in flight and create another encrypted transaction that specifies the same key provider and key ID. If the second transaction is included in an earlier block than the original one, a naive key provider would reveal the key and thus the original transaction, even though it is not included yet.

Key providers can protect their users from this attack. One possible strategy to do so is “namespacing” key IDs: Providers only release keys for key IDs that are prefixed with the envelope signer’s address and withhold all others. As we can reasonably assume that the attacker does not have access to the envelope signer account, an attacker would be unable to produce a transaction with correctly namespaced key ID.

### Key Provider-Child Builder Collusion

To build a new block, builders need to know the post-state of the previous block and thus all decryption keys used in a block and which of them are withheld. This information is publicly known once the PTC attests. However, malicious key providers could collude with a block builder and give them an earlier heads up. This would give the builders a competitive advantage as they can start the block building process earlier.

The impact of the attack is deemed low because the time between publishing of the payload attestations and the end of the slot is still long enough for block building. Furthermore, the start of the block building period is much less critical than the end (since only then the full set of includable transactions is known), which is not affected by the attack. Also, delaying the release of decryption keys bears the risk of them not being attested to by the PTC, negating the competitive advantage of the attacker. And finally, if the number of encrypted transactions that use the malicious key provider is small, their impact on the tree state is likely small as well. This means optimistic block building strategies that don’t rely on full knowledge of the state tree could be viable, countering the attack.

## Replies

**vbuterin** (2025-12-18):

Interesting, so this is essentially a kind of “encryption abstraction” that lets each user choose who they trust.

My first instinct here is: would the “your key provider must trust the previous key providers” rule not lead to extreme network effects, and thus naturally collapse into everyone trusting the same key provider? And if that happens, would this not just turn into a universal shared key (eg. threshold encryption to the round’s attesters) with extra steps? Though maybe that’s acceptable, if the goal is to put the mechanism outside consensus so that it can be modified without changing the mempool or hard forking.

---

**jannikluhn** (2025-12-19):

Good question! The goal of the trust graph is actually to *reduce* the network effects: Say, there’s a big key provider with 90% encrypted transaction volume and a small key provider with only 10%. If neither trusts the other, builders can only pick one of them for each block, so they’re gonna pick the big one 90% of the time. Users of the small one will have to wait 10x as long for their transaction to be included. With the trust graph, the small provider can communicate to builders that they’re ok with being included behind the big one. So they get a less secure spot, but faster.

I guess the question is if anyone would ever use the small key provider if they implicitly have to trust the big one anyway. I think they might because the levels of trust are very different: The direct key provider can decrypt immediately when the transaction is published, before it has been included in a block. This can be used for sandwiching attacks, censorship, etc, all the bad stuff. The indirectly trusted key providers are much more limited: They can only wait for the direct key provider to release the key and then based on that decide to release or withhold their own keys. At this point though, the block is already built, so they cannot censor and sandwiching is much more difficult and inefficient (they have to guess in advance what the encrypted transaction might do, place the frontrunning transaction accordingly, and then turn it on or off by releasing/withholding their key depending if their guess was correct or not). So I could see users not trusting some key provider enough to use them directly, but deeming the implicit trust assumption acceptable.

---

**koyahness** (2025-12-19):

An interesting approach!

This is what i could tease apart with AI based analysis.

This proposal aims to integrate (enshrine) an encrypted mempool directly into the Ethereum protocol to combat malicious MEV and improve censorship resistance.

Below is a summary of the core concepts, motivations, and technical design outlined in the proposal:

1. Core Objective

The primary goal is to protect users from front-running and sandwich attacks. By encrypting transactions until they are committed to a specific order in a block, the contents (value, destination, and data) remain hidden from block builders and proposers. This prevents them from selectively reordering or inserting their own transactions to profit at the user’s expense.

2. Key Features

* Encryption Agnostic: The design is built to support various decryption technologies. This includes Threshold Encryption (e.g., Shutter), MPC committees, Trusted Execution Environments (TEEs), Delay Encryption, or even future FHE (Fully Homomorphic Encryption) schemes.

* Enshrinement: Unlike “out-of-protocol” solutions (like current private RPCs), this would be part of the Ethereum consensus layer. This ensures the highest level of security and “weak” censorship resistance, as builders cannot see what they are censoring until it is too late.

* Hybrid Support: The proposal allows for a “hybrid” model where both plaintext (traditional) and encrypted transactions coexist.

* Liveness Guarantees: A critical design point is ensuring the chain continues to progress even if the “decryption key providers” (the entities responsible for releasing the keys) fail or go offline.

3. Transaction Lifecycle

* Encryption: A user encrypts their transaction using a public key provided by the network’s decryption providers.

* Inclusion: An encrypted transaction is included in a block by a builder/proposer. At this stage, the builder knows the transaction’s size and gas limit but not its contents.

* Decryption: Once the block is finalized or the order is “locked,” the decryption keys are revealed.

* Execution: The transactions are decrypted and executed in the order they were committed. If a transaction is found to be invalid after decryption (e.g., insufficient balance), it is simply skipped.

4. Why “Universal”?

The “Universal” aspect refers to the proposal’s attempt to create a standard interface that can work across different Ethereum Roadmap milestones, such as ePBS (Enshrined Proposer-Builder Separation). It aims to be a flexible framework rather than a rigid implementation of a single cryptographic technique.

5. Motivation & Context

This proposal builds on years of research into “Shutterized” beacon chains and the real-world performance of encrypted mempools on the Gnosis Chain. It is seen as a way to “blind” builders, reducing their power and helping to mitigate the centralization risks associated with high-MEV extraction.

Status: It would require a significant Ethereum hard fork and broad community consensus to be implemented.

---

**jannikluhn** (2025-12-19):

The summary is mostly accurate, except for point 4: Universal refers to the fact that it supports arbitrary crypto schemes and key providers. Should have made this more clear in the EIP.

---

**Julian** (2026-01-07):

Thanks for the proposal! My main concern is the optional decryption.

The encrypted transactions are put at the bottom of the block and only revealed if the key provider reveals the keys. That means there could be encrypted transactions at the bottom of the block that e.g. make a swap to buy ETH. The transaction is only decrypted if the swap turns out to be valuable at the last moment the keys must be released, otherwise, the transaction remains encrypted. Note that this is later than when the block must be committed to. This is akin to the [free option problem in ePBS](https://collective.flashbots.net/t/the-free-option-problem-in-epbs/5115) where the builder may decide whether or not to reveal its payload based on its ex-post trading performance. Key providers could do the same thing. This is undesirable because space on-chain is wasted in providing these options and it further complicates block building. Note that this option is less costly to exercise because instead of losing the entire block, only the encrypted transaction value is lost but even the fees from the transactions are paid. In the extreme, the builder could become a key provider and only include its own encrypted transactions that aim to extract MEV.

---

**b-wagn** (2026-01-08):

Thanks for this great post! I like the idea of having one universal design that allows multiple cryptographic solutions.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> a contract with a decryption and a key validation function, each of which accept a key ID and a key message as byte strings.

Can you give a bit more details on the syntax / interface of these two functions? Especially, I think having that spelled out would help to verify if the proposal is really decryption-mechanism agnostic, i.e., supports threshold enc, delay encryption, [sealed transactions](https://ethresear.ch/t/sealed-transactions/21859) (?).

Also, I was wondering if you have thought about which security notions (at least informally) the used decryption mechanisms should satisfy (e.g., for threshold enc, there are tons of notions to choose from).

---

**jannikluhn** (2026-01-09):

Thanks for the interesting feedback! I agree that the free option exists and that it can be used to extract MEV. It seems difficult to avoid without abandoning the goal of supporting arbitrary key providers. I’m not sure though how big the negative impact would actually be. To me, it seems the main issue with the free option in ePBS is that it could lead to empty slots with cancelled transactions, which is very bad in terms of UX. In our case, there’s no direct user impact, the only downside is slightly less efficient MEV extraction.

I say only slightly less because key extractors can use an artificual decryption function that looks like this: `decrypt(message, key) = key`. That way, they not only have one bit of influence (reveal/not reveal), but they can execute arbitrary code by crafting the key accordingly (subject to the preset gas limit). That way they have almost full power and can extract MEV with close to maximal efficiency. So I think the only efficiency loss comes from having two MEV “equilibration” transactions in short order one after another (one end-of-block in the encrypted part, one top-of-block in the next one).

---

**jannikluhn** (2026-01-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/b-wagn/48/17510_2.png) b-wagn:

> Can you give a bit more details on the syntax / interface of these two functions? Especially, I think having that spelled out would help to verify if the proposal is really decryption-mechanism agnostic, i.e., supports threshold enc, delay encryption, sealed transactions (?).

I think it should be maximally simple and general, something like:

```auto
verify(bytes key_provider_id, bytes key_id, bytes key) -> boolean
decrypt(bytes key_provider_id, bytes key_id, bytes key, bytes message) -> bytes
```

Do you see any decryption scheme that would not be supported by this? The odd one out seems to be sealed transactions which seems we can support like this:

```auto
verify(_, key_id, key) -> hash(key) == key_id
decrypt(_, key) -> key
```

(i.e. `key_id` is the hash of the transaction and `key` is the transaction itself)

What I’m unsure about is if the functions should get access to context information such as current block number, EVM state, or sender of the transaction to decrypt. I’m leaning towards no for safety and simplicity, but I could see it being useful in some cases, e.g. to restrict who’s allowed to use a key.

![](https://ethresear.ch/user_avatar/ethresear.ch/b-wagn/48/17510_2.png) b-wagn:

> Also, I was wondering if you have thought about which security notions (at least informally) the used decryption mechanisms should satisfy (e.g., for threshold enc, there are tons of notions to choose from).

First of all, I think it’s important to make sure the chain stays secure even if there’s a malicious key provider with malicious decryption scheme. Only users who use it explicitly should be affected as well as users who trust it indirectly through the trust graph. But for something reasonable that users would want to use, I don’t have anything formal, but would start with:

- no decryption before encryption payload is released, but early enough for PTC to attest to them
- Commitment, i.e., there’s only one valid decrypted message for a particular encrypted message
- Non-malleability
- CCA security

It would be great to get feedback on this from other potential future key providers.

---

**b-wagn** (2026-01-12):

Thanks for the response! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> I think it should be maximally simple and general, something like:
>
>
>
> ```auto
> verify(bytes key_provider_id, bytes key_id, bytes key) -> boolean
> decrypt(bytes key_provider_id, bytes key_id, bytes key, bytes message) -> bytes
> ```

Is `key` the public key that is registered or is it the private key that is used to decrypt ciphertexts? Related to that, I am a bit confused about your syntax of `decrypt`.

Usually, a decryption function (for PKE, FHE, …) would take as input a *ciphertext* and not a message, i.e., something like `decrypt(secret_key, ciphertext) = message`

---

**jannikluhn** (2026-01-12):

Sorry, should have been more clear. `message` is meant to be the ciphertext (or more concretely, the encrypted payload). `key` is meant to be the decryption key. Depending on the crypto scheme used, it might also contain additional data to verify/authenticate it’s correctness, like a signature of the key provider.

The system does not really have a notion of public keys (because it only encrypts, it doesn’t decrypt). I guess `key_id` comes close, it’s meant to specify to the key provider which decryption key to release. This could be a public key or it could be an identity value in an identity-based encryption scheme like Shutter.

---

**b-wagn** (2026-01-12):

Thanks! Makes sense.

That leads me to my next question:

If `key` is the decryption key, then it may depend on the ciphertext whether it is valid or not, right? For instance, if you use threshold ElGamal or threshold Boneh-Franklin or something alike. So should the syntax of `verify` also include the ciphertext as input?

And then I assume the correctness property that you want from this algorithm is something like: “if `verify` outputs 1, then `decrypt` will output the original message”.

---

**jannikluhn** (2026-01-13):

Makes sense, will update the proposal to pass the ciphertext to the verification function. I don’t see any downside in that. Thank you for the feedback!

---

**Marchhill** (2026-01-20):

Interesting proposal!

Could you give some more details on how timing of the slot would change? Specifically how will the key release and decryption line up with other events in the slot, and whether it is compatible with different slot lengths?

---

**jannikluhn** (2026-01-25):

Key providers publish their keys between the time the builder publishes the execution payload and the time the PTC attests. According to the ePBS specs, the latter is at the latest at [75% or 9s](https://github.com/ethereum/consensus-specs/blob/9e2dc0bcf9aa17b549e1df4712b16a5709d74119/specs/_features/eip7732/validator.md#payload-timeliness-attestation) into a slot. The former is, as far as I can tell, [largely up to the builder](https://github.com/ethereum/consensus-specs/blob/9e2dc0bcf9aa17b549e1df4712b16a5709d74119/specs/_features/eip7732/builder.md#constructing-the-execution-payload-envelope), but sometime between the beacon block proposal time and the PTC attestation deadline. Realistically, builders will likely want to publish as soon as possible to reduce the risk of their block not receiving sufficient timeliness attestations, but only after the beacon block has received sufficient regular attestations. It will be interesting to get real world data on this once ePBS goes live, but for now I think a good estimate is the 25% / 4s mark (the attestation deadline).

All in all, this gives key providers a 50%/6s window between 25%/3s to 75%/9s window to generate, publish, and broadcast decryption keys. I’m optimistic that this is long enough for most key provision mechanisms, but it would of course be better to get data from different real world implementations. With 6s slot times and all other things equal, the window would go down to 3s. To me, this sounds too short unfortunately.

I don’t think it’s relevant for the discussion, but for completeness: Some key providers may be able to publish decryption keys already on observing the beacon block only. This works if their decryption keys are not transaction, but block specific, and if they are not worried about builders withholding their blocks on observing the keys.

Regarding decryption, that’s carried out as part of block execution. In pure ePBS, nodes can execute blocks as soon as they receive the execution payload. With this EIP, strictly speaking, they have to wait for the payload timeliness attestations from the PTC in order to know which keys to consider, so execution is delayed to the 75% mark. That said, the attestations are only relevant for the encrypted section of a block. The leading plaintext transactions can be executed with only the execution payload, so there’s no latency impact for those.

---

**Julian** (2026-01-26):

Thanks for your earlier reply on MEV extraction!

I was curious about how this encrypted mempool approach compares to the private mempools we have today on Ethereum.

When using a private mempool a user needs to trust the mempool provider / builder not to sandwich which is similar to trusting the key provider. In [BuilderNet](https://buildernet.org/) or [Relay Block Merging](https://ethresear.ch/t/relay-block-merging-boosting-value-censorship-resistance/22592), multiple private mempools can be merged if the private mempool providers trust each other which sounds similar to the Key Provider Trust Graph.

A key benefit to me of encrypted mempools is that it could improve the builder market as it could potentially reduce the ability of builders to acquire private order flow since users do not need to use private order flow. I’m curious if that advantage holds in this design as well since the key providers are in some ways similar to private mempools.

---

**0w3n-d** (2026-01-26):

So the changes these transactions make to account / storage state when executed is not included in the state root for that block? No one will be able to know prior to the transaction being included on chain what it does or what state is changed by it?

---

**remosm** (2026-01-26):

Interesting proposal! To piggyback on [@Julian](/u/julian)’s comment, [Relay Block Merging](https://ethresear.ch/t/relay-block-merging-boosting-value-censorship-resistance/22592) could be extended to support a less universal version of such an encrypted mempool. This maintains protection against builder frontrunning, at the cost of limiting the set of key share holders to builders and relays.

Specifically, builders and relays could hold key shares and lazily pass forward decryption shares with the payload. In this way, no ~significant additional latency would be introduced.

At the relay merging stage, the decryption shares provided by the builder and relay could be combined to append the decrypted transactions to the block. This prevents builders from frontrunning and only maintains trust in relays, which is an improvement over the status quo.

A more advanced setup could allow k-of-n shares to be combined, where the set of relays holds enough shares to reach the threshold. In this way, the transactions can be decrypted without the builder’s share, addressing the free option problem. A simple way to implement this is to use the channel used for [relay constraints sharing](https://ethresear.ch/t/block-constraints-sharing-multi-relay-inclusion-lists-beyond/22752).

Overall, the main advantages of such an out-of-protocol setup are that it addresses frontrunning risk, and is doable today. The big downside versus a native implementation is that we maintain the relay as a trusted party.


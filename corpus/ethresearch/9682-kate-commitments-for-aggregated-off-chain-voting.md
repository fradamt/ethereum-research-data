---
source: ethresearch
topic_id: 9682
title: Kate Commitments for aggregated off-chain voting
author: nikeshnazareth
date: "2021-05-31"
category: Cryptography
tags: []
url: https://ethresear.ch/t/kate-commitments-for-aggregated-off-chain-voting/9682
views: 3113
likes: 10
posts_count: 11
---

# Kate Commitments for aggregated off-chain voting

I had an idea for aggregating votes off-chain and validating them on-chain with Kate commitments and BLS signatures. There is at least one loophole to be closed and potentially lots of ways to make it more elegant, but this should be enough detail to explain the idea in a way that someone with more experience can critique it. Feedback is most welcome!

https://nikeshnazareth.github.io/vote-aggregation/

## Replies

**rsolari** (2021-06-03):

Thanks for sharing this idea! I am excited about projects to make on-chain voting cheaper and more accessible.

I particularly like this idea if there’s a good way to do signature verification on a rollup. Is there a well-trod path to checking BLS signatures on a rollup? Ideally, we’d use ZK rollup, because the economic security and long dispute windows of an optimistic rollup don’t help when there is a potentially extremely valuable on-chain vote that closes after just a few days.

---

**nikeshnazareth** (2021-06-07):

Thanks for the feedback!

It’s not entirely clear in my head but I’m not sure rollups help here. I think this is conceptually like a use-case specific zkrollup optimization (particularly, if we’re talking about PLONK).

The way I see it is:

- In ZK Rollup, you send all the transactions on chain for data availability reasons.
- Then you map your aggregation problem into a circuit diagram
- Then you take that circuit and (in the PLONK case), convert it into a polynomial equation. There’s a generic way to do this but it produces a relatively complicated equation
- Then given that polynomial equation, you produce the final result and prove that it matches the data

This scheme is using the same primitives, but I’m skipping over the first 3 steps and handcrafting a polynomial equation that applies to the standard voting use case. Since it’s a custom equation, I imagine it would be more efficient than what you’d get out of a ZK rollup. There’s no gate logic or copy constraints or anything.  Of course, in both cases, the final step is just a handful of on-chain pairings, so they’d be the same in that regard.

I think leaving the signatures outside of the polynomial equation is actually an advantage because:

- Ethereum will have BLS precompiles so verification will be very efficient: EIP-2537: Precompile for BLS12-381 curve operations
- Since we’re validating signatures on the fly, we don’t need to save any of the individual votes on chain

Does that make sense? Although I’m no expert on this stuff so I could be mistaken.

---

**bgits** (2021-06-07):

This is a nice idea. Regarding the commitment of balances, will it require a trusted party to submit a commitment of balances for the vote?

I see there is a process for minting, but if every voter needs to do an onchain transaction to commit their balance doesn’t that defeat the purpose?

---

**nikeshnazareth** (2021-06-07):

The design is for the contract to always have an up-to-date Balance commitment. Nobody submits it directly - it gets updated on every mint / burn / transfer operation. Because of the linearity, it can be updated just with “augment commitments” that only affect the balances that needs to change.

The contract doesn’t need to store the actual balances, but users will need to be able to retrieve them somehow. Either they’ll have to reconstruct it from the events or the contract could keep it in storage for convenience.

When it comes time to vote, nobody needs to submit actual balances because the contract is using the Balance commitment and the Vote commitment to validate the final tally. Of course, whoever calculate the tally offline does need to know the balances so they can use them to calculate the tally.

---

**bgits** (2021-06-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/nikeshnazareth/48/6353_2.png) nikeshnazareth:

> The design is for the contract to always have an up-to-date Balance commitment. Nobody submits it directly - it gets updated on every mint / burn / transfer operation. Because of the linearity, it can be updated just with “augment commitments” that only affect the balances that needs to change.

Is there a proof of concept contract demonstrating this in solidity?

---

**nikeshnazareth** (2021-06-10):

> Is there a proof of concept contract demonstrating this in solidity?

No code yet.

> I see there is a process for minting, but if every voter needs to do an onchain transaction to commit their balance doesn’t that defeat the purpose?

I see the misunderstanding now, though. I was thinking of this as a standalone contract with its own internal logic. It has the same functionality as normal ERC20 tokens but it’s not actually an ERC20. The most important difference is that users need BLS signatures for identities, not ETH addresses. So either that will require wallets to support BLS, or we need a chain with account abstraction (eg Optimism or ETH 2.0). Or hopefully someone can figure out a cool mathematical trick to sign an ECDSA message and translate that into a BLS signature, but I’m not holding my breath on that one.

But if you want to use this on live projects (of course you do! Why wasn’t that obvious to me in the first place ![:man_facepalming:](https://ethresear.ch/images/emoji/facebook_messenger/man_facepalming.png?v=12)??) then we need a way of associating the user ERC20 token balances with these new EfficientVotingToken balances. And if users had to exchange them before every vote, that would be really lame.

Maybe it’d be okay to get users to do a one-time upgrade to a new token that kept the token balance commitment up to date (but was still an ERC20). Or tokens with upgradeability patterns could do that directly. Or without user /project intervention, we could have a function on a separate voting contract that allows anyone to copy balances over atomically. But we’d still need to get users to pick a BLS key and associate it with their ETH address. I’m not sure if there’s a good way to do that without individual users registering their BLS keys.

---

**bgits** (2021-06-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/nikeshnazareth/48/6353_2.png) nikeshnazareth:

> The most important difference is that users need BLS signatures for identities, not ETH addresses. So either that will require wallets to support BLS, or we need a chain with account abstraction (eg Optimism or ETH 2.0). Or hopefully someone can figure out a cool mathematical trick to sign an ECDSA message and translate that into a BLS signature, but I’m not holding my breath on that one.

BLS verification can already be done: [BLS Signatures in Solidity](https://ethresear.ch/t/bls-signatures-in-solidity/7919)

Even if not done in solidity it would be helpful to see how this would work in any language. Like a minimal viable polynomial commitment scheme.

---

**rsolari** (2021-06-10):

Awesome, thanks for explaining this stuff. Makes sense to me.

Couple questions about how the BLS commitment might work:

- Anytime a token owner deposits/withdraws/transfers, they have to sign something to update the BLS commitment, right? Current voting systems take a snapshot of the balances, but the wouldn’t work here without all the signed commitments, right?
- Is there a way for another smart contract to have a balance on a BLS token contract? I don’t see how, but maybe there’s some clever trick that I am missing. That would be useful for voting from e.g. multi sig contracts, autonomous proposals, and on-chain treasuries.

---

**nikeshnazareth** (2021-06-12):

> BLS verification can already be done: BLS Signatures in Solidity

I was more concerned about BLS signatures in wallets, but then again maybe we can add this to the list of reasons for wallets to support BLS ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)

> Even if not done in solidity it would be helpful to see how this would work in any language. Like a minimal viable polynomial commitment scheme.

Yes, absolutely. I may have some time next week to put something together.

---

**nikeshnazareth** (2021-06-12):

> Couple questions about how the BLS commitment might work…

Thanks for the questions! I’m not sure I understand the first one but I think it’s based on a misunderstanding. So let me just say a bunch of things that I think are true in order to build each piece systematically, and hopefully that clarifies.

I think I wasn’t too clear about what Polynomial commitments *require* you to do vs *allow* you to do.

There is no inherent relationship between Polynomial commitments and BLS signatures. PCs are just a way to fingerprint large amounts of arbitrary data. I’m using BLS signatures for the same reason normal contracts use ECDSA signatures: to convince the contract that you’re authorised to mint/burn/transfer. But the contract can rearrange balances arbitrarily with no user intervention, provided it has access to the underlying data that generated the commitments. You could keep that data in storage, just like a normal ERC20. And in that case, you could do snapshots the way ERC20s currently do them.

So you could imagine taking a normal ERC20, and modifying it (or copying the balances to a new contract) so that it redundantly keeps tracks of a BALANCE polynomial commitment, and keeps it up to date with every balance transfer. This could be entirely transparent to the user. The slight complication is that you’d need to map user addresses to positions in the polynomial for that to make sense (at least, if you’re using the encoding that I suggest). With such a token, users could still vote using their normal ETH address in order to create a VOTE polynomial commitment, and then the same trick of doing a dot product between the BALANCE and VOTE commitments to calculate the tally offline and convince the contract in constant time that it’s right. Although this works, it doesn’t achieve much because if users are going to individually update their value in the VOTE commitment, they might as well just update the tally directly.

Enter BLS keys. Imagine introducing a new rule that said some users, if they want to, can assign their balance to a BLS key (or you could let them keep both, where either one works depending on what they’re trying to do). They’d need to register that key and the contract would then track a BLS_KEYS commitment as well. With that change, any subset of users that have opted in to using BLS keys would be able to update the VOTE commitment with all of their votes in a single step. So the voting procedure gets more efficient as more voters choose to use BLS keys.

Normal contracts would still keep balances against their address and transfer / vote with them as before. I think you’re right that a contract can’t do a BLS signature for the same reason they can’t do an ECDSA signature - they can’t keep the key private. But by the nature of the contract, you’re not going to be able to coordinate with them in an off-chain aggregate mechanism anyway, so they would have always been a bottleneck (unless you’re doing something cool with SNARKs).

As an aside, if we’re talking about an N-of-N multisig, BLS signatures actually let you achieve the functionality directly without a smart contract: you just save the balance under the aggregate public key. If we’re talking about an N-of-M multisig, I have some vague thoughts about how you might be able to do that too, but I haven’t thought it through properly.

Then the last trick that I mentioned is that if you’re storing commitments, you don’t actually need to store the data (but you can if you want to). Ignoring all the voting stuff for a second, you could imagine taking a standard ERC20 and creating a BALANCES commitment with it. At that point, you could delete all the actual balances, provided users were able to reconstruct them (from events or by querying a data provider that’s watching the contract). Whenever the contract needs to know a particular value (eg. if they’re doing a transfer, they need to know the sender has sufficient funds), whoever is doing the action would need to construct a proof (in linear time) to convince the contract (in constant time) that the claimed balance matches their commitment. You could even do a mixed version, where users can opt in to this scheme and so their contract can delete their balance. Slight caveat: this opt-in strategy only works if users who haven’t opted in never need to know the balances of users who have, which I think is fine as long as we’re not worried about positive overflows from transferring tokens to somebody without knowing their existing balance. Note that this trick has nothing to do with BLS signatures or voting. It’s just noticing that a contract with a commitment doesn’t need to know the underlying data as long as someone gives it to them (and proves it) when required.

And to your point about snapshots, it’s actually easier if the contract is treating the commitment as the canonical balance, because copying a commitment is basically equivalent to taking a snapshot. But if the contract is also storing some of that data, it would need to track how that data changes across the snapshot as well, just like existing contracts.

Hopefully that clears it up. Let me know if you want any other clarifications!


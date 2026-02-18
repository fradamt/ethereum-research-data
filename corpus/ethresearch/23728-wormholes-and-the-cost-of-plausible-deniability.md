---
source: ethresearch
topic_id: 23728
title: Wormholes and the cost of plausible deniability
author: Pierre
date: "2025-12-23"
category: Privacy
tags: []
url: https://ethresear.ch/t/wormholes-and-the-cost-of-plausible-deniability/23728
views: 548
likes: 17
posts_count: 10
---

# Wormholes and the cost of plausible deniability

by [@mmjahanara](/u/mmjahanara), [@pierre](/u/pierre)

Thanks to [@b-wagn](/u/b-wagn), [@soispoke](/u/soispoke), [@winderica](/u/winderica) and [@levs57](/u/levs57) for the helpful discussions and comments which led to this writeup.

*TLDR; We go over why wormholes’ plausible deniability property doesn’t seem compatible with Ethereum’s 160 bits addresses. Also, we shed light on EIP-7503’s claimed anonymity set, which is much lower than expected in practice. While the latter issue should be solvable, we believe the first might require to rethink the overall wormhole setup. We conclude the post with a potential, briefly described, follow-up design using beacon chain deposits*

### On Wormholes

Ethereum privacy solutions have historically relied on application-specific anonymity sets. In protocols like [Tornado Cash](https://github.com/tornadocash), the act of depositing funds is an explicit interaction with a specific smart contract. This creates a fundamental flaw: while the *link* between depositor and withdrawer is broken, the *participation* in the privacy protocol is public. These designs allow chain observers to label and potentially censor all depositors to the anonymity set.

[EIP-7503 (zero-knowledge wormholes)](https://eips.ethereum.org/EIPS/eip-7503) proposes a different paradigm, relying on plausible deniability.

The mechanism is simple: users “burn” funds by sending them to a cryptographically determined unspendable address. Later, they provide a (non-interactive) zero-knowledge proof (NIZK) that they know the pre-image of that address to re-mint the funds in a fresh account. Crucially, the “deposit” (or “burn”) is indistinguishable from a standard ETH transfer to a fresh address.

However, we believe there might be a fundamental tradeoff between plausible deniability and security, which may hinder the enshrinement of wormholes within the L1 today. In addition to this, we also shed a light on an issue with respect to EIP-7503’s effective anonymity set, which might be lower than expected.

## Notation and Assumptions

We will use:

- \mathsf{H}(\cdot) for a generic 256-bit hash function (e.g., SHA3, SHA-256, …).
- \operatorname{trunc}_{160}(x) for truncation of a 256-bit value x to a 160-bit Ethereum address.
- Domain-separated hashes as \mathsf{H}(\text{“TAG”} \parallel \cdots), where \text{“TAG”} is a fixed ASCII prefix (e.g. \text{“worm”}, \text{“null”}).

### EIP-7503

In the original EIP-7503 specification, a burn address is derived from a single secret s:

Addr_{burn}(s) = \operatorname{trunc}_{160}(\mathsf{H}(\text{“worm”} || s)).

In the first step, the user *burns* its funds by picking a random s and sending them to Addr_{burn}(s). Later, the user can *mint* funds by providing to a smart contract a *nullifier* \nu = \mathsf{H}(\text{“null”} \parallel s) and a NIZK proof that \nu is consistent with some existing transaction A\to B (i.e., uses s s.t. B = Addr_{burn}(s)). The contract  verifies the proof and checks that \nu has not been submitted before. If these checks pass, the funds are minted.

The security properties of such a burn-mint mechanism aren’t explicit, so let us informally define them.

#### Correctness / Completeness

If a user behaves honestly, then it can mint after burning.

#### Privacy

1. Unlinkability

Intuitively, *privacy* here means that no one (except the user itself) can link the burn transaction to the minting process, i.e., the mint transaction submitted to the mint contract. To be a bit more precise, we consider the user being honest in this case, and want that no observer of the chain can tell which transaction was the burn transaction that corresponds to the mint transaction.

1. Plausible deniability

The second privacy property that we want is that the burn transaction should look like a “regular” transaction. In particular, the burn address B should look like a random address. Plausible deniability is nice and is one of the major difference with tornado-cash like protocols requiring explicit contract interactions. With wormholes, *participation* in the burn protocol remains private - note that withdrawing remains public.

#### Non-Inflation

This is the idea that we don’t want ETH created out of thin air and means that one can only mint if one burned before: our map from any successful mint transaction to a burn transaction should be injective. At a first glance, this would mean preventing an adversary from producing two different nullifiers for the same burn transaction. Indeed, if an adversary can produce such two different nullifiers for the same burn transaction, we would end up with an inflation bug.

Since \mathsf{H}(\cdot) is hiding, wouldn’t that be straightforward? Well, as noticed early on [by the Scroll team](https://www.notion.so/scrollzkp/WIP-Wormhole-RIP-2817792d22af80029818ee83cb1c54ba), this is where things get tough.

### The birthday paradox

The [birthday paradox](https://en.wikipedia.org/wiki/Birthday_problem) implies that finding *any* two secrets s_1, s_2 such that the 160-bit addresses collide

Addr_{burn}(s_1) = \operatorname{trunc}_{160}(\mathsf{H}(s_1)) = \operatorname{trunc}_{160}(\mathsf{H}(s_2)) = Addr_{burn}(s_2)

takes approximately 2^{80} operations. Although large, such a number remains within the reach of nation-states or massive mining pools. When an attacker finds such a collision, the protocol breaks:

1. Deposit 100 ETH to the colliding address once.
2. Mint with nullifier \nu_1=\mathsf{H}(\text{"null"} \parallel s_1) and \nu_2=\mathsf{H}(\text{"null"} \parallel s_2). These are two distinct nullifiers, so 100 ETH are minted twice.
3. Withdraw 200 ETH.

Since the verifier only checks that each nullifier is used once, it cannot tell that these two withdrawals are backed by the *same* on-chain deposit. This is an infinite inflation bug: 160-bit address collisions at the 2^{80} birthday bound translate directly into double-mints.

However, note that a chain with a larger address space will not have to face this security shortcoming: the security of scheme would be satisfying with full-size 320-bit addresses. Ethereum’s 160-bit truncation is an optimization that it could, in theory, move away from.

### Tentative solution: remove collisions search and make the scheme hard to break with dlog instead?

Let us propose an idea: could we work around the birthday paradox and instead of requiring from the attacker to find collisions to ask him to instead break dlog?

Say that we work with the following NIZK on the statement (\mathcal{R}_{root}, \nu) and witness (sk,s_{worm},tx = (A,B,pk),\text{salt},\pi_{merkle}) along the following constraints:

(1) \pi_{merkle} authenticates tx in \mathcal{R}_{root};

(2) pk == \mathsf{SkToPk}(sk), i.e., pk = sk \cdot G for ECDSA keys;

(4) B == \operatorname{trunc}_{160}\!\big(\mathsf{H}(\text{"worm"} \parallel sk \parallel \text{salt})\big);

(5) \nu == \mathsf{H}(\text{"null"} \parallel sk \parallel tx).

That setting would be pretty nice: a user could even re-use its burn address when using the same \text{salt} value for two different burn transactions!

The security argument should also be straightforward: double-minting now requires breaking the NIZK, ECDSA, or the hash used for \nu, rather than exploiting a 2^{80}-cost address collision. Indeed, for a fixed burn transaction (and thus fixed A, pk, B), there is only one valid sk, or you would otherwise be able to find two different secret keys mapping to the same pubkey that initiated the transaction. Thus, all colliding witnesses map to the same nullifier.

### Is it the fix?

Not really, because preventing nullifier collisions isn’t the only issue!

Wormholes should also prevent burn addresses from being spendable. As noted by the original EIP-7503, an attacker could find a pair of secrets (s_1, s_2) such that `create2_address(..., s1) == sha256("wormhole" || s2)`. In that setup, an attacker could burn funds to `sha256("wormhole" || s2)` and  withdraw them subsequently from `create2_address(..., s1)`. Although that means the attacker could extract their ether twice (only), that still should be considered failure.

But are we really concerned given our above updated circuit? Since our design requires an attacker to break dlog, can’t we simply require [for EXTCODESIZE to not be 0](https://eips.ethereum.org/EIPS/eip-3607) when burning funds? That would prevent an attacker from withdrawing funds burned to `create2_address(..., s1)`.

The thing is that it is a mistake to think in the first place that the above scheme requires an adversary to break dlog. The game for an attacker to control the burn address remains, in fact, pretty much the same as the one involving the `CREATE2` opcode, regardless of the proof of knowledge on the private key.

In our setup, for a burn address to be spendable, the game is the following: if the attacker is able to find two secrets (s_1, s_2) such that trunc160(H(\text{“worm”} || s_1)) == trunc160(H(skToPk(s_2))), he wins. Indeed, when that’s the case, the attacker ends up with a spendable burn address, since finding such a pair lets the attacker initiate a transaction from trunc160(H(skToPk(s_1))) to trunc160(H(\text{“worm”} || s1)), an address controlled with s_2!

We are back to square one: this is the same collision search problem with only 80 bits in complexity.

### Today’s plausibly deniable wormholes require to work with collision resistance

Ignoring detection heuristics, wormholes’ plausible deniability requirement entails that no one observing the L1 is able to distinguish wormhole transactions from regular ones. This property naturally requires the burn address computation to remain private to the user initiating the burn. But, because of the collision resistance game, there is no way for users to prove with more than 80 bits of security that the secret they used to generate the private 160 bits burn address does not as well control it.

A way out could be to enshrine the burn address within the protocol itself (say sending funds to trunc160(H(\text{“worm”})), turning the problem into a pre-image search task. But that setting would make us lose the plausible deniability property that we are looking for. We end up stuck in having to choose between a weakly secure but plausibly deniable design and another one pretty much equivalent to tornado-cash like setups.

We list here three questions that we think are valuable for improving the state of wormholes:

1. Are there any other primitives we could leverage to enshrine  plausibly deniable wormholes in the L1? We think the answer is yes and are initiating follow-up work on leveraging beacon deposits instead. We briefly detail the idea in the below add-on.
2. Would there be a way to build wormholes from a pre-image search problem with plausible deniability? We aren’t sure of this, it seems quite hard to work with a deterministic but private burn address.
3. Are there any low-hanging L1 changes that would let us answer one of the above two questions positively?

### Add-ons

#### EIP-7503 effective anonymity set

There is a practical issue for which we aren’t sure this has been discussed properly. In doubt, we are writing things here to make it clear.

EIP-7503 exposes the `beacon_block_root` as a public input of the mint proof. But this decision shrinks the claimed anonymity set ([all of the Ethereum accounts with zero outgoing transactions](https://eips.ethereum.org/EIPS/eip-7503)) to transactions which occurred in that block, since the corresponding burn transaction must be in the referenced block. If wormhole protocols decide to use transaction receipt roots as input to users’ mint proof, keeping a large enough anonymity set will require access to an accumulator providing the ability to obtain authentication paths to all previous transactions.

While this should work in theory, since every block root hash is a commitment to all transactions prior to that block, this proof would either require an efficient client-side recursive snark or a particular L1 setup - say replacing keccak with an arithmetization friendly hash or extending block headers with a field committing to a merklized block root containing all previous blocks hashes.

#### Follow-up work: Wormholes meet beacon deposits

The [beacon deposit contract](https://etherscan.io/address/0x00000000219ab540356cbb839cbe05303d7705fa#code) is a one-way bridge from the execution layer to the beacon chain. As deployed today, each validator is publicly linkable to its deposit and withdrawal destination: the contract exposes a single `deposit` function that accepts a deposit together with the validator `pubkey` and withdrawal credentials (`withdrawal_credentials`).

There might be a way to design a private version of the contract, which would replace `pubkey` and `withdrawal_credentials` with a corresponding hiding commitment. Deposits would then be claimed on the beacon chain by providing a zk proof-of-knowledge. In this construction the validator is added to the activation queue only after the deposit has been claimed on the beacon chain. Note that unclaimed deposits can still be added to the withdrawal queue like any regular validator.

This would require some protocol re-architecture, but it could materially improve validator privacy while also acting as an in-protocol, wormhole-like mechanism with plausible deniability. Moreover, with roughly one-third of ETH staked and on the order of tens of millions of dollars in daily withdrawals (or more), the resulting anonymity set could be meaningfully large.

## Replies

**seresistvanandras** (2025-12-23):

Great work! Congrats! A few comments and food for thought below. In a nutshell, I’m not in favor of enshrining a non-general purpose and likely a temporary privacy solution on the L1. Additionally, in terms of practical privacy/plausible deniability point of view it is a very minimal (if at all) improvement over Tornado Cash-style shielded pools.

- Post-quantum security Looking ahead, one of the many reasons why EIP-7503 seems to be temporary is the lack of post-quanutm security. For wormhole to be future-proof, at least there should be a clear path towards transitioning into a post-quantum world. This perhaps should already apply to any L1 protocol upgrade.
- Plausible deniability People seem to underestimate the power of side-channels and metadata analyses on blockchains. In particular, even though the raison d’être of Wormhole would be plausible deniability, I believe, in practice it would essentially provide negligible plausible deniability. There are numerous papers analyzing the time passed between (heuristically) linked deposit and withdraw transaction in Tornado Cash. They consistently find that it follows a distribution with low means (2-3 days) and exponentially decaying tails in the distribution.  See for instance, Figures 8. and 9. here or Figure 17. here. Thus, in practice, the anonymity set of a Wormhole withdraw transaction will be only a few (hundred) thousand transactions in the last few days. The situation will be dramatically worse, when one considers the particular amount correlations. (Most users will just withdraw Wormhole deposits all at once because of convenience and moderate withdraw gas costs) One could say as it was suggested by the Scroll Team to apply “a fixed denominated list of deposit amounts for simpler UX”. But such a design would essentially collapse the entire system back to a Tornado Cash shielded-pool in terms of detectability. We are back at square one.
- Non-general purpose privacy In my view, EIP-7503 would be at the level of a potential L1-enshrinement if it could provide general-purpose, programmable privacy. The current design is essentially a Tornado Cash-style privacy-enhancing technology from late 2019. In the long run, we would need a Wormhole-like privacy tool that lets us not only deposit and withdraw ether/erc20 tokens, but also allows transfers (this is already enabled by Wormhole), swaps, and ideally anything DeFi. Real anonymity set would stem from programmability. If people could use their money “inside Wormhole” then they would not be motivated to exit the system. Wormhole as an “undetectable Railgun” would be really cool. Enhanced usability and more functionalities (i.e., transfers, swaps, DeFi) will also increase adoption and the maturity of the proposal.

---

**MicahZoltu** (2025-12-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/seresistvanandras/48/10229_2.png) seresistvanandras:

> See for instance, Figures 8. and 9. here or Figure 17. here.

The heuristics referenced in those figures are the subset of users who made critical OpSec/usage mistakes.  Thus, the time correlations in those figures suffer from very significant sample bias.

---

**seresistvanandras** (2025-12-24):

You’re right, agreed. There may be sample biase, for sure. But the underlying assumption in my argument is that the average user will behave as those 10% (in both linked papers the authors manage to link at least 10% of withdraws) that are linked heuristically. I think this is a reasonable assumption, especially w.r.t. to the time that users tend to leave their assets in a shielded pool. One may want to look up empirical measurements for Zcash, or Litecoin’s MimbleWimble Extension Block (MWEB) to have a better sense of user behaviour in shielded pools. That would give a more informed sense about the possible plausible deniability of Wormhole.

(btw I would not blame so much users for these “critical” OpSec/usage mistakes. These are not necessarily their faults and it is super easy to screw up. 1) we gotta educate users 2) wallets could/should help making these decisions on the user’s behalf.)

My hunch is that people leave much more willingly their assets in a shielded pool if they can do “stuff” with it, i.e., transfer, swaps, DeFi. Partially, that’s the reason of Railgun’s success IMHO. General-purpose Wormhole would attract *much more users* who additionally would *leave their assets much longer* in the system. I believe that such a general-purpose undetectable privacy-layer would make much more sense to enshrine.

---

**MicahZoltu** (2025-12-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/seresistvanandras/48/10229_2.png) seresistvanandras:

> My hunch is that people leave much more willingly their assets in a shielded pool if they can do “stuff” with it, i.e., transfer, swaps, DeFi.

It depends on the user you are trying to attract: degens or people who use crypto as a store of value/medium of exchange?

The primary reason I don’t store all of my assets in a shielded pool is because I cannot have time-delayed recovery systems setup, and securing money against both theft and loss at the same time is *extremely* hard (in the real world) without time based recovery options.  Secondarily, I would like to be able to transact directly from the shielded pool, but I don’t need to be able to do degen stuff direct.  If I can just pay my bills from shielded that is sufficient.

![](https://ethresear.ch/user_avatar/ethresear.ch/seresistvanandras/48/10229_2.png) seresistvanandras:

> (btw I would not blame so much users for these “critical” OpSec/usage mistakes. These are not necessarily their faults and it is super easy to screw up. 1) we gotta educate users 2) wallets could/should help making these decisions on the user’s behalf.)

The only way we will get regular users to have good OpSec is if the tools they use force good OpSec on them.  The tooling should not allow deposit followed by an immediate withdraw, it should have a randomized delay built-in to it for initial deposits.

---

**CPerezz** (2026-01-01):

That was a really nice article! Thanks a lot for sharing! So refreshing to read and with a really interesting idea involving the Beacon at the end.

Have you looked further into it? Are there any plans to actually work on a PoC for that?

Also, isn’t there any other trick to play here? ie. What if you limit the amount of ETH/wormhole tx to be <1ETH.

One legit user can make as many txs as they want and pass all the ETH needed in multiple txs (just paying 21k ([soon less]()) extra per each tx. But, for an adversary, the cost is massive. As for each tx, it actually needs to mine an address with at least 80bits target each time. So the attack gets insanely delayed and doesn’t seem that worth it.

This is just an idea I’ve had after 10 mins of looking at the roof and thinking so it might be dumb. It’s not bulletproof but unsure if there’s anything that we can discuss in these lines. cc: [@MicahZoltu](/u/micahzoltu)

But seems a simple and easy compromise between attack_cost vs. reward?

---

**MicahZoltu** (2026-01-02):

Also keep in mind that since ETH is not designed for long term stability against goods & services that people care about, any threshold we set may end up being too high or too low to have any effect in the future.

---

**Pierre** (2026-01-02):

[@seresistvanandras](/u/seresistvanandras) thanks for the feedback!

Regarding pq security, I guess that working with a larger address space for burn transactions would do the trick? Also, there are already several pq ready zksnarks and wormholes are signature schemes agnostic; so the broad idea should still work?

I agree that plausible deniability can be discussed when instantiated in practice and can cause quite a few troubles. But this issue isn’t tied to wormholes per se. My hunch is also to think that   tomorrow’s average user won’t behave as today’s, especially in the context of the education initiatives and wallet infra changes that you suggest (which I agree with)!

I suppose that enshrining non-general purpose privacy would entail much larger L1 changes. It is indeed limiting for wormholes to not feature a programmable shielded pool, but their simplicity is also what makes them attractive in the first place.

[@CPerezz](/u/cperezz) thanks for the kind words, always appreciated! Yes, we are taking a look at it, we hope to come back with some results soon.

Indeed, limiting wormhole deposits to some fixed amount could be an idea. As [@micahzoltu](/u/micahzoltu) mentioned, it’s hard to know what 1 ETH will be able to buy in the next few years. I also presume an attacker demonstrating an ability to generate double-mints could recoup most of the attack cost (if not profit) with shorting ETH? I’m no expert though!

---

**Phillip-Kemper** (2026-01-05):

A larger anonymity set is possible if the mint proof is instead a *state/balance proof*: prove that *at some later block* the (secret-derived) burn address exists in the execution state with balance ≥ amount (and e.g. nonce=0 / no code, etc.). This lets you choose any beacon root after the deposit as the “snapshot” you prove against, as long as the balance is still there, so the anonymity set is no longer “events in one block”, it’s “all accounts satisfying the predicate at that snapshot”

---

**NicoSerranoP** (2026-01-26):

Thank you! This is a great in-depth explanation of the 160-bit security problem of zkWormholes. I was a bit lost between why 160 bit addresses are a problem in the zkWormholes setting and not in the actual Ethereum setting. Here is an explanation that help me clear the confusion (please correct me if there is something wrong):

## Ethereum setting:

To generate a Ethereum address you need to perform the following steps:

1. have a secret private key s
2. compute a public key pk = s ·G (for ECDSA)
3. hash the public key hash_{pk} = H(pk)
4. truncate it to 160 bits to get your Ethereum address Addr_{pk} = trunc_{160}(hash_{pk})

To move your funds you need to sign a transaction using s, send it to the network and the protocol will validate your signature before allowing you to move funds. Even though the Ethereum address length is 160 bits, the attacker would not be able to brute force your signature.

## zkWormholes setting

To generate a zkWormhole address you need to perform the following steps:

1. have a secret s_{zk}
2. hash the secret concatenated to some constant value hash_{s_{zk}} = H("worm" || s_{zk})
3. truncate it to 160 bits to get a Ethereum address Addr_{s_{zk}} = trunc_{160}(hash_{s_{zk}})

The address Addr_{s_{zk}} cannot move funds because there is no valid public key generated from s_{zk}. To move funds in the zkWormholes setting we generate a NIZK proof that we know a s_{zk} that generates Addr_{s_{zk}} and send it to a smart contract to mint new tokens.

In this case, because of the 160 bit addresses and the birthday paradox, a powerful attacker can brute force two different secrets s_{i} that would both generate Addr_{s_{i}} following a valid NIZK proof. This situation would allow an attacker to double mint tokens from a single zkWormholes transactions.

PS: I am feel plausible deniability is an powerful feature. We should keep researching ways of achieving it (with zkWormholes or with any other technology).


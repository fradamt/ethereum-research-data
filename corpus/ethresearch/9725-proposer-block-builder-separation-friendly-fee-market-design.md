---
source: ethresearch
topic_id: 9725
title: Proposer/block builder separation-friendly fee market designs
author: vbuterin
date: "2021-06-04"
category: Economics
tags: []
url: https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs/9725
views: 48353
likes: 86
posts_count: 40
---

# Proposer/block builder separation-friendly fee market designs

*Special thanks to Justin Drake and the Flashbots team for feedback and discussion.*

A major risk threatening the ongoing decentralization of consensus networks is the economics around miner extractable value (MEV), sophisticated tricks to extract profit from the ability to choose the contents of the next block. A simple example of MEV is arbitraging all on-chain decentralized exchanges against price movements that have happened since the previous block. While normal PoS rewards are reasonably egalitarian, as single validators earn the same rate of return as powerful pools, there are significant economies of scale in finding sophisticated MEV extraction opportunities. A pool that is 10x bigger will have 10x more opportunities to extract MEV but it will also be able to spend much more effort on making proprietary optimizations to extract more out of each opportunity. In addition to this problem, MEV also complicates decentralized pooling, as in a decentralized pool there would still need to be one entity packaging and proposing the block, and they can easily secretly extract MEV without sharding that revenue with the pool itself.

The best-known solution is **proposer/block-builder separation**. Instead of the block **proposer** trying to produce a revenue-maximizing block by themselves, they rely on a market where outside actors that we call **block-builders** produce **bundles** consisting of complete block contents and a fee for the proposer, and the proposer chooses the bundle with the highest fee. The proposer’s choice is reduced to picking the highest-fee bundle, an algorithm so simple that in a decentralized pool it can even be done inside an MPC to prevent cheating.

This post proposes some designs for how this could be done.

*See also, ideas from 2018 that closely inspire the ideas here: [Optimised proposal commitment scheme](https://ethresear.ch/t/optimised-proposal-commitment-scheme/1314)*

## Desired properties for a proposer/builder separated block proposal design

We will focus on five major desired properties:

- Untrusted proposer friendliness: there’s minimal or no risk that a proposer will screw over a block builder, so block builders have no incentive to prefer proposers that have some off-chain reputation or personal connection to the builder (as that would favor large pools).
- Untrusted builder friendliness: there’s minimal or no risk that a block builder will screw over a proposer, so proposers have no incentive to favor builders that have some off-chain reputation or personal connection to the proposer (as that would make it harder for new builders to enter the market). If deposits are needed to accomplish this, they should be maximally low.
- Weak proposer friendliness: the mechanism should not require proposers to have either (i) high bandwidth or other computational resources or (ii) high technical sophistication
- Bundle un-stealability: proposers should not be able to take bundles proposed by block builders and extract transactions from them to make their own bundles, preventing the block builder from earning a profit (and possibly harming them even further)
- Consensus-layer simplicity and safety: the mechanism should continue to be safe and ideally be covered by the same analysis as the existing block proposal mechanism from a consensus-layer perspective

## Idea 1

1. Block builders make bundles and publish the headers of the bundles that they create. A bundle header contains a commitment to the bundle body (the intended block contents), the payment to the proposer, and a signature from the builder.
2. The proposer chooses the bundle header offering the highest payment (considering only bundles where the builder has enough balance to actually make that payment). They sign and publish a proposal containing that bundle header.
3. Upon seeing the signed proposal, the block builder that offered the included bundle header publishes the full bundle.

At this point, the fork choice rule has the ability to make one of three judgements (instead of the usual two, block present vs block absent):

- Block proposal absent
- Block proposal present but bundle body absent
- Block proposal present and bundle body present

Note that in the second case, the proposal still becomes part of the chain and, crucially, the block builder’s payment to the proposer still processes (but the block builder does not get any fees or MEV themselves).

### Analysis

Three of the five properties are fairly simple to show:

- The proposer receives the promised payment unconditionally, so bundles can’t screw over proposers
- All three steps are very automated and low-bandwidth, so this satisfies weak-proposer-friendliness
- The proposer cannot see the contents of the bundles that they are signing, so this satisfies bundle un-stealability

Consensus-layer properties, and untrusted proposer friendliness, are more tricky. This design does change how the fork choice works, increasing it to 3 options instead of 2, and it also means that the proposer is no longer the last actor in the game. Theoretically, one can reason that if fork choices are capable of making decisions, then this should be fine, but it’s still a significant change with potential unknown-unknowns.

The proposer does not see bundle contents and cannot screw over block-builders by bundle-stealing, but they can use a much more subtle attack to grief block builders. They can publish their proposal near the end of a slot, ensuring that attesters (probably) see the proposal on time, but not giving the block-builder enough time to publish the *body*, so there would be a significant chance that the attesters do not see the body on time. This imposes a risk on block-builders, and gives them an incentive to favor trusted proposers. Additionally, it creates an opportunity by which a malicious majority can heavily penalize block-builders that it dislikes.

I see two families of approaches to mitigating this problem:

- Attesters have a 2s delay between the maximum time at which they accept a proposal and the maximum time at which they accept a body. This mostly solves the issue if you trust the attesters, though the fundamental issue that block builders have a risk of losing funds still remains. Additionally, it’s not clear that it’s incentive-compatible for attesters to vote in this way (though one could conceivably force them to wait by requiring them to attest to a 2-second-long VDF solution to the proposal)
- If a body does not get included, the proposer only gets half the payment (and the block builder only pays half). This makes griefing by the proposer costly, but it still ensures that griefing by the block builder continues to be costly (in both cases costly enough that you can generally trust even anonymous actors to not want to do it). For example, if a bundle has proposer fee 1 and block builder profit 1.05:

Honest behavior would lead to a (builder, proposer) payoff of (0.05, 1)
- Proposer or attester publishing to late, leading to a header-only block being accepted, would lead to a payoff of (-0.5, 0.5)

## Idea 2

1. Block builders make bundles and publish the headers of the bundles that they create. A bundle header contains a commitment to the contents, the payment to the proposer, and a signature from the builder.
2. The proposer chooses and signs a statement consisting of the list of bundle headers that they’ve seen.
3. Upon seeing that statement, the selected block builders publish their corresponding bodies.
4. The proposer chooses one of the bundle headers from the list they’ve pre-committed to, and publishes a proposal with it.

There is a new slashing condition that would eject and penalize any proposer who publishes a proposal that is not part of the list that they committed to in the same slot.

Note also that the list of bundle headers submitted by the proposer in step (2) could also instead be a list of encrypted hashes of bundle headers with each hash encrypted to the public key of the builder of that bundle, so that only the builder knows if they were accepted. This reduces DoS risks.

### Analysis

Once again, three of the five properties are fairly simple to show:

- Proposers cannot steal bundles because they only see any bundle bodies when they’ve already restricted themselves to a finite set of existing bundle headers.
- There’s no possibility of the builder-to-proposer payment happening without the full body being included, so proposers cannot cheat builders economically either.
- Consensus properties are the same as before, because the system is still a proposer-moves-last game and there’s no change in what the consensus rules are deciding on

The two harder properties to ensure in this case are weak-proposer-friendliness and untrusted-block-builder-friendliness. The concern is that a malicious block builder can attack proposers by making a large number of proposals that all offer a very high fee, but never publish the body of any of them. If the proposer has a cap on how many bundles they accept, then this attack can price out *all* of the legitimate bundles, and leave the proposer with no bundles that they can legally include in their block. If there is no cap on how many bundles the proposer can accept, then this risks an unbounded number of full bundle bodies (think: 500 kB each) being sent to the proposer, an overwhelming amount of bandwidth requirement.

One solution to this conundrum is to rate-limit bundle header submission in some way that is not a hard limit.

- A fee for submitting bundles, which is adjusted through some EIP-1559-like mechanism to target some rate (eg. 8 bundles per slot)
- A deposit requirement for being a block builder (necessary anyway to ensure proposers get paid), together with a rule that if you publish a bundle that does not get included when a lower-priced bundle did get included, you cannot submit bundles for the next N slots

The fee itself could also be charged only in the case where your bundle does not get included but a lower-priced bundle does, as that’s the specific situation in which you may have acted maliciously (or the proposer was malicious or the network was bad at the time).

There is some precedent for this; [ENS auctions](https://medium.com/the-ethereum-name-service/a-beginners-guide-to-buying-an-ens-domain-3ccac2bdc770) have a 0.5% loser fee to discourage people from making bids when they are clearly not going to win just to force up the amount that the winner has to pay.

However, these techniques risk introducing a trust requirement on the proposer, so they need to be done carefully and the penalty for failing to get a bundle included cannot be too high.

An alternative solution is to allow free and unlimited bundle body publication, but limit body propagation at network layer. One simple algorithm is:

- Add a slight delay for the minimum time at which bundle bodies can be propagated: 0s for the highest-paying bundle, 0.2s for the second-highest-paying bundle, 0.38s for the third-highest-paying bundle, and generally 2 * (1 - 0.9^{k-1}) seconds for the k’th highest paying bundle.
- Add a rule that a node does not propagate a bundle body if it has already propagated a higher-paying bundle body.

These two techniques can be combined together: you could have a slight fee to reduce the expected number of bundles to eg. 50 per slot, and then use network-layer mechanisms like this to reduce bandwidth requirements further.

## Conclusions

So far I don’t have a clear logical reason to believe that the above two approaches are the *only* families of solutions to the problem; there could be others. Out of these two approaches, idea (1) is conceptually simpler but it introduces risk to the block builder as well as more complex fork choice rule requirements. Idea (2) is simpler from the fork choice and consensus perspective, but it has challenges dealing with malicious block builder DoS and any solutions to this problem risk creating other problems as well, though this could conceivably be minimized. As of yet I’m still not sure which one is better.

## Replies

**nazariyv** (2021-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The best-known solution is proposer/block-builder separation

can we assume that:

1. block-builders will produce more profitable blocks than proposers would otherwise?
2. the separation would prevent proposers from being / having/financing their own block-builders, especially if assumption (1) is violated.

---

**vbuterin** (2021-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/nazariyv/48/6415_2.png) nazariyv:

> block-builders will produce more profitable blocks than proposers would otherwise?

We can’t assume that this is always true, but I definitely expect professional block builders to often be able to produce more profitable blocks than average proposers.

![](https://ethresear.ch/user_avatar/ethresear.ch/nazariyv/48/6415_2.png) nazariyv:

> the separation would prevent proposers from being / having/financing their own block-builders, especially if assumption (1) is violated.

Proposers are totally able to be their own block-builders, and there is nothing wrong with this. The goal is simply that they should not have to be.

---

**Shymaa-Arafat** (2021-06-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The proposer’s choice is reduced to picking the highest-fee bundle,

with EIP-1559 will it be the highest fee or the highest tip bundle?

I mean if fee is burned,  naturally the miner/proposer will care about the max tip.

.

-Also, with 2-level solution I kind of worry about one more possible level of malicious collide one should worry about. I think it is similar to “solvers” in the Gnosis protocol if I remember the name right… now we have to protect from a malicious builder trying to deceive the miner, malicious miner trying to front-run a victim user, malicious couple of builder-proposer having more power to victimize users or hurt the system.

3-Allow me to express a fear/worry after reading a lot of papers about MEV, front-running, sandwich attacks,…etc. I kind of feel with all these MEV suggestions that u r like trying to reconcile with miners after the fee burning policy by giving them a piece of MEV from users, which “may” (I’m no expert) hurt the overall Ethereum market in the long run

.

Sorry if my Qs were conceptual & trivial, since I haven’t done real Ethereum development

.

»»» I must add that if u r going to use some of the Gnosis Protocol ideas, u have to take enough precautions of all their previous exploits, although I don’t find an isomorphic to disregarded utility in ur solution; just added the term incase someone else notice something I missed

---

**jannikluhn** (2021-06-05):

To me idea 2 sounds much more favorable because it doesn’t require any consensus changes.

One way to fix the DoS issue is to use a threshold encryption committee:

1. The committee provides an encryption key for each slot.
2. Block builders encrypt their bundles with this key and send them (with plaintext headers) to the proposer.
3. The proposer publishes a commitment to one of the bundles (selected based on the fee in the header).
4. Upon seeing the commitment, the threshold committee publishes the decryption key.
5. The proposer decrypts the bundle and creates the block.

This doesn’t have the same DoS problem as headers are at all times attached to their (encrypted) bodies, so there are no unavailable proposals. Invalid ones or ones that are unlikely to be accepted can be filtered early at the network level.

It does rely on an honest-majority committee, but since it’s not at the consensus layer and fully opt-in I don’t think many proposers or builders would mind. Also, different proposers could use different committees if they don’t trust the same ones, as long as block builders trust them too.

---

**yoavw** (2021-06-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> ## Idea 1
>
>
>
> …
>
>
> If a body does not get included, the proposer only gets half the payment (and the block builder only pays half). This makes griefing by the proposer costly, but it still ensures that griefing by the block builder continues to be costly (in both cases costly enough that you can generally trust even anonymous actors to not want to do it). For example, if a bundle has proposer fee 1 and block builder profit 1.05:
>
> Honest behavior would lead to a (builder, proposer) payoff of (0.05, 1)
> Proposer or attester publishing to late, leading to a header-only block being accepted, would lead to a payoff of (-0.5, 0.5)

Even if the block builder ends up paying 0.5 of the proposer fee, an attack may still be profitable.  Suppose we have proposer1 and proposer2, but proposer2 also runs a malicious builder1 and a colluding builder2.  Builder1 sends proposer1 blocks, paying 0.5 fee and never publishes the body.  Proposer1 is unable to complete any block and always gets just 0.5 (paid by builder1).  Proposer2 always gets 1 fee, and its colluding builder2 earns block builder profit.  The colluders (proposer2+builder1+builder2) always earn 0.5+profit (0.55 in the example above), while proposer1 always gets 0.5.  It makes collusion more profitable than the default behavior, which might lead to centralization.

Would it work better if we make the 0.5 fee case asymmetric?  If the body is not published, the proposer gets 0.5 fee but the builder pays 1 fee - half of which is burned.  This would shift the scales and hopefully makes collusion unprofitable.  Proposer1 gets 0.5 but the colluders lose 1 so they end up with 0+profit (0.05 in the example above).  As long as profit < 0.5 fee, collusion seems unprofitable.

In reality this attack seems unlikely because the colluders make 0.55 (and the attacked proposer 0.5) but a honest pair (proposer3,builder3) make 1.05.  However, the possibility of this attack means that proposers will prefer to work with trusted builders (be a part of a honest pair) to avoid getting into the 0.5 situation, and that violates **Untrusted builder friendliness**.

Another concern around the symmetric 0.5-fee is that it makes stalling the chain cheaper than advancing it. A malicious block builder can always bids the highest fee, knowing that it will never publish the body so it will end up paying 0.5 of its bid while triggering the default “zero-proposal” for the slot.

Honest block builders attempting to advance the chain must outbid the malicious one, and they end up paying the full fee.

Hence, advancing the chain costs twice as much as stalling it.

Making the 0.5 fee asymmetric as I suggested above (builder pays 1 fee, proposer gets 0.5, and 0.5 fee gets burned) seems to even the costs.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> ## Idea 2

Doesn’t has the same drawback because a proposer is not limited to a single block header.

However, it gives the proposer more power to choose between blocks after they’re already known.  I don’t see a DoS/griefing opportunity but a proposer colluding with a group of builders could always select the block that makes most sense based on off-chain events.  E.g. an oracle is going to publish a piece of real world information in the next block, not known when the current block is built, but known by the time it is proposed.  Two builders send conflicting blocks before the information is known, one assuming that the oracle will return 0 and the other assumes 1, and then their colluding proposer chooses the “winning” one 2 seconds later.

A proposer could have done the same by itself before this proposal - proposing only when the oracle information is known, but now that we separate builders from proposers, we don’t want collusion to be profitable.  Collusion between builders and proposers becomes the winning strategy due to new information becoming available during the period between building and proposing.

It seems like a corner case that won’t happen too often, but it still makes collusion the more profitable strategy, leading to potential centralization.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A fee for submitting bundles, which is adjusted through some EIP-1559-like mechanism to target some rate (eg. 8 bundles per slot)

It doesn’t mitigate the collusion above, because the fee is paid from the builder to the proposer, which are actually the same entity.  That is, unless the fee is burned like in EIP 1559.  If the fee is burned then it should mitigate this collusion, just as long as the profit from the collusion around the oracle result is lower than the burned fee.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A deposit requirement for being a block builder (necessary anyway to ensure proposers get paid), together with a rule that if you publish a bundle that does not get included when a lower-priced bundle did get included, you cannot submit bundles for the next N slots

N-slots exclusion penalty could work better since the combined entity actually takes a loss.  Obviously, if the gains from choosing the winning block and not publishing the losing one (based on oracle information) is sufficiently high, no mitigation would work.  We could add some sort of slashing for not publishing the body, but that may be too harsh because unreliable connectivity could also lead to that.  N-slots exclusion seems to strike the balance.

If we go with the N-slots exclusion, the block builder deposit needs a withdrawal delay, i.e. the deposit must remain locked for at least N slots after submitting a block.  Otherwise it wouldn’t be Sybil resistance and will just lead to high churn rate of block builders.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The fee itself could also be charged only in the case where your bundle does not get included but a lower-priced bundle does, as that’s the specific situation in which you may have acted maliciously (or the proposer was malicious or the network was bad at the time).

This condition seems necessary if we add such a fee.  Otherwise a fee reduces the incentive to run a builder (separately from the proposer- if fee is not burned, or at all - if fee is burned).  If the submission fee becomes too high it could increase centralization by reducing the number of builders or encouraging them to collude with a proposer.

The combined approach, with fee based delay and not propagating lower-fee bodies after a high fee body was propagated, seems to solve most problems.

On a more general note, both issues I highlighted are centered around the profitability of collusion between builders and proposers.

Would it make sense to add a sixth desired property, “Collusion doesn’t increase profitability”?  The 5th rule (**Consensus-layer simplicity and safety**) implicitly includes it, since the consensus layer already has that property, but there’s a subtle difference because we’re adding another component and want to prevent collusion with it as well, so it might make sense to make it explicit.

---

**JustinDrake** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> miner extractable value (MEV)

I believe the modern take (and the one relevant for Ethereum post-merge) is “Maximal Extractable Value” ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> idea 2 sounds much more favorable because it doesn’t require any consensus changes

Realistically both ideas require consensus changes. For example in idea 2 the slashing condition is best done in consensus for capital efficiency, to bypass gas complications, and for general simplicity.

As I see it idea 1 is clearly preferably to idea 2:

1. bandwidth—Idea 1 requires the proposer to receive many bodies from builders. This is almost a non-starter for weak proposers and presents a DoS vector.
2. latency—Idea 1 has three half-rounds of latency (builders publish headers, proposer publishes header, builder publishes body) whereas idea 2 has four half-rounds of latency (builders publish headers, proposer publishes commitment, builder publishes body, proposer publishes header and body).
3. simplicity—Idea 1 avoids unnecessary complications such as the slashing condition in idea 2.
4. builder-friendliness—Idea 2 allows the proposer to profitably steal from the builder when MEV is greater than the slashing penalty. Note that MEV has a significant spiky component (e.g. flash crash liquidations, contract hacks, token launch front-running).
5. proposer MPC-friendliness—As noted idea 1 has a trivial blackbox (i.e. without seeing bodies) MPC-friendly header selection algorithm whereas idea 2 opens the door for more sophisticated (and less MPC-friendly) non-blackbox selection algorithms that analyse the content of bodies.
6. proposer power minimisation—As a general rule of thumb we want to minimise the discretionary power of proposers. Idea 1 is preferable in this regard because header selection is blackbox, without seeing bodies.

---

**vbuterin** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> Even if the block builder ends up paying 0.5 of the proposer fee, an attack may still be profitable. Suppose we have proposer1 and proposer2, but proposer2 also runs a malicious builder1 and a colluding builder2. Builder1 sends proposer1 blocks, paying 0.5 fee and never publishes the body. Proposer1 is unable to complete any block and always gets just 0.5 (paid by builder1). Proposer2 always gets 1 fee, and its colluding builder2 earns block builder profit. The colluders (proposer2+builder1+builder2) always earn 0.5+profit (0.55 in the example above), while proposer1 always gets 0.5. It makes collusion more profitable than the default behavior, which might lead to centralization.

Isn’t this just saying that the colluding attacker makes a 0.55 profit instead of a 1.05 profit from being honest (so they sacrifice 0.5 from the attack) and they make the honest proposer lose 0.5 in the process? So this is a griefing attack; it’s not actually in the colluding attacker’s (direct) interest to do this, and so one should expect that it should not happen often. Or am I misunderstanding something?

> Would it make sense to add a sixth desired property, “Collusion doesn’t increase profitability”?

I was covering that under weak proposer friendliness: the mechanism should not favor proposers that are engaging in spooky advanced strategies that require ongoing effort to figure out, which collusion definitely is.

---

**yoavw** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Isn’t this just saying that the colluding attacker makes a 0.55 profit instead of a 1.05 profit from being honest (so they sacrifice 0.5 from the attack) and they make the honest proposer lose 0.5 in the process? So this is a griefing attack; it’s not actually in the colluding attacker’s (direct) interest to do this, and so one should expect that it should not happen often. Or am I misunderstanding something?

If profit was consistently 0.05 then yes, but once MEV profits surpass 0.5 fee this behavior becomes profitable, e.g. when there’s a highly profitable frontrunning opportunity.  MEV profits will fluctuate, and often stay below this threshold.  The problem is, once players start engaging in this behavior (at a time when it makes sense because MEV > 0.5) all the proposers will want to defend themselves after getting 0.5 a couple of times.  The simplest defense will be to work with a trusted pool of block builders.  At that point even if MEV profits drop back to 0.05 and the collusion attack stops, the proposers already centralized the builders into trusted pools.

In other words, as soon as MEV profits cross the 0.5 threshold once, the network switches to a more centralized state and there’s no trigger to ever switch it back.

Am I missing something that would stop this from happening?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I was covering that under weak proposer friendliness: the mechanism should not favor proposers that are engaging in spooky advanced strategies that require ongoing effort to figure out, which collusion definitely is.

Right.  No additional property is needed.

---

**lekssays** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Isn’t this just saying that the colluding attacker makes a 0.55 profit instead of a 1.05 profit from being honest (so they sacrifice 0.5 from the attack) and they make the honest proposer lose 0.5 in the process? So this is a griefing attack; it’s not actually in the colluding attacker’s (direct) interest to do this, and so one should expect that it should not happen often. Or am I misunderstanding something?

In the long run, if we consider the colluding players to have the option of being honest and earn 1.05 or malicious and earn 0.55 but making honest proposer loose 0.5, I think that it could be a profitable strategy nonetheless because the honest proposers will have two options: either quit (in case the effort is less than the profit) or stay (in case the whole operation is somewhat (i.e., not earning the full 1.05) profitable. Both options will lead to centralization is some sense. For the first option, it will leave the floor to malicious players (and I think this is a risk that might need a little bit of thinking if I am not mistaken. For the second option as [@yoavw](/u/yoavw) mentioned, the honest proposers will choose to work only with the builders that they trust which is a profitable and safe strategy for them where I don’t personally see an incentive for them to quit their trusted area and work with unknown builders.

So, as I see it (and of course I might be highly mistaken), there will be groups of proposers that work only with the builders in their whitelist) which makes the whole process not fully decentralized.

On the top of my head, I think if we could see it (or adapt it) to a non-zero sum game (where the malicious proposers do not really affect the honest ones) by proposing some punishment mechanism (that I don’t have any idea now of how to integrate it) would fix many issues.

---

**yoavw** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/lekssays/48/5743_2.png) lekssays:

> On the top of my head, I think if we could see it (or adapt it) to a non-zero sum game (where the malicious proposers do not really affect the honest ones) by proposing some punishment mechanism (that I don’t have any idea now of how to integrate it) would fix many issues.

Good idea.  Make it so that proposers are never affected by the attack, but increase the cost of collusion.  Maybe something like this:

Proposer always gets 1 fee, regardless of whether the slot is successful or bad.  Builder pays fee*X (X>=1).  Upon a successful slot, builder is refunded (X-1)*fee.  On a bad slot, (X-1)*fee is burned without refund.

X>=1 is a decaying function of the number recent bad slots, such as 1+K*moving_bad_slots_ratio.

When no one attacks the network, X is close to 1.  When someone starts implementing the collusion strategy, X keeps increasing until the attack becomes unprofitable and subsides.  This way the attack becomes increasingly more expensive but proposers remain unaffected so they don’t centralize.  The only victim would be a honest builder who had the misfortune of losing connectivity in mid proposal during an ongoing collusion attack.  That seems rare enough for the  network to live with.

The downside of not letting the attack affect proposers is that it opens up a vector for malicious proposers to slow down the network by always publishing slots with the zero proposal, claiming that the body was not published.  As long as it’s a minority it doesn’t matter, but we need to think whether they could have an incentive to do so collectively.  Hopefully it won’t be an issue since the proposer still has more to gain by publishing a successful block.

---

**vbuterin** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> If profit was consistently 0.05 then yes, but once MEV profits surpass 0.5 fee this behavior becomes profitable

Why would it be profitable? Is it because the MEV from the first block carries over into the next block, which *is* controlled by a friendly proposer? If so then ok that makes sense.

---

**lekssays** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> Proposer always gets 1 fee, regardless of whether the slot is successful or bad. Builder pays fee*X (X>=1). Upon a successful slot, builder is refunded (X-1)*fee. On a bad slot, (X-1)*fee is burned without refund.
>
>
> X>=1 is a decaying function of the number recent bad slots, such as 1+K*moving_bad_slots_ratio.

I agree with this part. I think that decoupling the profits of both malicious and honest players would solve the issue. Another point, even the profit itself should be dynamic and not consistent (e,g,. 0.05 as [@vbuterin](/u/vbuterin) suggested). It can be calculated depending of the “moving_bad_slots_ratio” (or another metric) as well.

Another idea that would be hard (it will put an overhead in the network), we can borrow the idea of staking here, so before any operation proposers should stake an amount Y where Y > profit. This staking will be valid for the duration of the operation (e.g., till publishing the body of the block). Then, everyone gets paid and Y + profit gets returned to the proposer. I don’t see any incentive for proposers to act maliciously, but I am not sure on the feasibility part (so it would still need some analysis in this regard).

---

**vbuterin** (2021-06-07):

> Another point, even the profit itself should be dynamic and not consistent

One quick clarification: the 0.05 is not a hardcoded number, it was simply an example. In reality, the profit rate for block builders would be set by the market; I expect it to be low in a competitive environment.

---

**yoavw** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Why would it be profitable? Is it because the MEV from the first block carries over into the next block, which is controlled by a friendly proposer? If so then ok that makes sense.

If MEV carries over to the next block and it’s controlled by a honest proposer then the protocol achieved its goal despite the delay.  But if the colluders that performed the 0.5 fee attack are also a large pool of potential proposers (think coinbase-sized staking farms), they have a relatively high chance to control the next slot.  Their strategy in this case would be to stall slots by spending 0.5 until one of their proposers is selected.

This attack wouldn’t have been possible with the pre-separation protocol because even a large staking farm can’t stall the chain effectively.  With this change a stalling attack might become a viable strategy during high MEV circumstances.

It seems that any design that enables stalling attacks would violate **Weak proposer friendliness** by favoring large pools.  Does it make sense or am I totally off the mark here?

The only way I see to mitigate this attack in the context of **idea 1** is to increase stalling cost exponentially with each bad slot:

1. builder offers fee but sends conditional_fee = fee*2^num_of_consecutive_bad_slots
2. proposer receives fee in any case
3. burn conditional_fee - fee if slot is bad
4. refund conditional_fee - fee to builder if not burned

---

**vbuterin** (2021-06-07):

I think the fee for a stalling attack might end up being quadratic naturally. The reason is that as more blocks come up, the attacker would need to keep outbidding legitimate block builders, and legitimate block builders would be making higher and higher bids as the number of unclaimed transactions piles up. So the *per-block* cost to the builder would be increasing in time (linear in time if demand is constant and either (i) there was no block size cap or (ii) elasticity = 1), and so the *total* cost would be something close to quadratic.

---

**yoavw** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/lekssays/48/5743_2.png) lekssays:

> profit itself should be dynamic and not consistent

The protocol doesn’t control the profit and can’t even calculate it.  This is MEV profit and may only become apparent in hindsight when the block builder’s MEV strategy is analyzed.  For well known strategies the profit will be low due to a race to the bottom, with block builders competing by offering a high fee for their block to be included.  Basically a MEV auction.  For new strategies or ones that can’t be replicated easily (e.g. requiring large holdings of an illiquid governance token), profit can be very high for a short time.

---

**yoavw** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I think the fee for a stalling attack might end up being quadratic naturally.

Yes.  I was just thinking about that too.  Fees will keep increasing linearly but the attacker has to pay 0.5 * the sum of fees for the stalled slots.  It’ll only make sense in rare opportunities of knowledge-asymmetry such as when implementing a new MEV strategy that others haven’t identified yet, to prevent frontrunning its first shot.

But any reason not to make it exponentially expensive based on the length of the stall? Under normal conditions a stall of more than 1-2 slots seems unlikely, so the exponential cost will only kick in during an attack.

---

**vbuterin** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/yoavw/48/6142_2.png) yoavw:

> But any reason not to make it exponentially expensive based on the length of the stall? Under normal conditions a stall of more than 1-2 slots seems unlikely, so the exponential cost will only kick in during an attack.

I would say the main reasons to consider staying away from that are:

1. Just plain old protocol simplicity (increasing complexity introduces greater risk from unknown-unknowns)
2. Relying too much on lose-lose games (where there are penalties that do not correspond to rewards) is risky because it creates an incentive to circumvent the protocol (eg. imagine a few rounds of stalling happened, and there’s a risk a block will not get included due to network latency; proposer+builders would benefit from moving over to some layer-2 super-protocol)

---

**lekssays** (2021-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Relying too much on lose-lose games (where there are penalties that do not correspond to rewards) is risky because it creates an incentive to circumvent the protocol (eg. imagine a few rounds of stalling happened, and there’s a risk a block will not get included due to network latency; proposer+builders would benefit from moving over to some layer-2 super-protocol)

I think (correct me if I am wrong) that the incentive to move to a layer-2 super-protocol would be a strategy in any case, so it doesn’t need a special event (e.g., few rounds of stalling) to happen.

If we separated the rewards from penalties, it would be a very rare case to have few rounds of stalling because its cost would be very high (quadratic or exponential as you explained).

Thus, attacking the protocol is a loosing strategy (unless the malicious player does not care about incentives but it only cares about taking down the protocol).

I think that the attack on the protocol and making builders quit because of unprofitable auctions have the same overall effect. However, the latter has a more probability of happening. So, we need a tradeoff between the two.

---

**yoavw** (2021-06-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Just plain old protocol simplicity (increasing complexity introduces greater risk from unknown-unknowns)

Agreed. We should go with the simplest protocol that satisfies the five properties.  I hope the market/fee based mitigation can achieve it.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Relying too much on lose-lose games (where there are penalties that do not correspond to rewards) is risky because it creates an incentive to circumvent the protocol (eg. imagine a few rounds of stalling happened, and there’s a risk a block will not get included due to network latency; proposer+builders would benefit from moving over to some layer-2 super-protocol)

I don’t know if it would come to that, since each proposer would probably run its own local builder to handle cases where it gets selected and no one else submits a block.  Whether it creates a sub-optimal block or just proposes an empty (but valid) block doesn’t matter.  Either way it breaks the stall chain and resets the conditional_fee.  Long stall-chains will be too rare to justify developing a layer-2-super-protocol when it’s easy to just break the chain with a local builder.

But you’re right - keep it as simple as possible as long as it satisfies the requirements.


*(19 more replies not shown)*

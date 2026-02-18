---
source: magicians
topic_id: 26392
title: I think it's ok to allow stage 1 rollups shorter withdrawal windows (1-2 days), but we should be more conservative on stage 2
author: vbuterin
date: "2025-11-02"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/i-think-its-ok-to-allow-stage-1-rollups-shorter-withdrawal-windows-1-2-days-but-we-should-be-more-conservative-on-stage-2/26392
views: 3133
likes: 36
posts_count: 18
---

# I think it's ok to allow stage 1 rollups shorter withdrawal windows (1-2 days), but we should be more conservative on stage 2

## 1. Where did the current “7 days” number come from?

See [this post](https://ethresear.ch/t/optimistic-rollups-the-challenge-period-and-strong-censorship-attacks/21721):

> For simplicity, let’s assume that censorship is sustained, i.e. it is performed with no breaks. Moreover, we assume L1 rollbacks and L1 rollup-specific invalid state transitions to be a highly controversial and not desirable social response that should be avoided where possible.
>
>
> We sketch the following timeline:
>
>
> (0h → 24h): a 51% strong censorship attack is detected.
> (24h → 6d): a hard fork is coordinated, implemented and activated to slash censoring validators.
> 1d: the time left on the honest players’ clock to play the game.

Historically, it took us 6 days to implement the fastest emergency fork we’ve done from start to finish ( [EIP-608: Hardfork Meta: Tangerine Whistle](https://eips.ethereum.org/EIPS/eip-608) in 2016), so if we use that as a benchmark, then 7 days seems reasonable for “how long does it take Ethereum to fork?”

There is one misconception in this post, which is that you need a *hard fork* to take out censoring validators. This is not true: the protocol has been deliberately designed so that a minority soft fork that counter-censors the censors is sufficient. And a soft fork can be done more quickly. But on the other hand, in a 51% censorship attack, you would expect an attack on the social layer, so things could get chaotic, and that’s an argument in the opposite direction. Hence, on the whole, “an onchain civil war started by a 51% censorship attack will take the chain out for 6 days” seems like a reasonable assumption.

## 2. What are the downsides of 7 day withdrawal windows?

To withdraw through the canonical bridge, you have to wait 7 days before you get your assets. This is a long time. Almost all users instead deposit and withdraw through liquidity providers, intermediaries which give you the coins immediately from their balance sheet, and then deposit and withdraw through the canonical bridge on their own, charging a fee to the user to account for the costs of rebalancing.

The need for liquidity providers to wait is a key thing that is preventing liquidity provider-based bridging from being cheap, unless it goes through trust-based third party bridges. As a result, (i) today bridging has costs that are low, but still significant, and (ii) a lot of it happens through the USDC and other bridges, making the Ethereum ecosystem de-facto more trust-dependent than it otherwise would be.

If we want actually-decentralized defi to thrive, we need faster withdrawals. In the medium term, this is why I support [fast withdrawals](https://x.com/VitalikButerin/status/1953131251436818684) through ZK proofs, or a hybrid 2-of-3 OP+ZK+TEE or OP+ZK+ZK scheme. This will bring withdrawal times down to 10-60 min, a 168-1000x cut to liquidity providers’ costs. In the short term, before such technologies are ready, allowing faster withdrawals from optimistic rollups could cut liquidity providers’ costs by 3-7x, which is still a helpful win.

## 3. What does a 1-2 day withdrawal window give us in terms of security?

The longest-lasting failure that the Ethereum blockchain has had was [the consensus failure in 2016](https://www.reddit.com/r/ethereum/comments/5eoaaw/consensus_flaw_in_geth_we_have_identified_the/). This created a fork that split the chain in half, and within **12 hours**, almost everyone was able to rejoin the correct fork. *This wasn’t really “downtime”*, because a sophisticated actor could easily have sent a transaction that would have gotten included on both chains. But the 12 hour duration is a reasonable precedent for an upper bound, especially if we want fraud proof posting to be available to less sophisticated actors. During the [2016 Shanghai DoS wars](https://www.youtube.com/watch?v=nhr5nlMNvRQ), individual clients were unusable for periods that lasted nearly as long.

Additionally, speaking of less sophisticated actors, **8 hours** is a standard human sleep duration.

**A 1-day withdrawal window is enough to ensure that you can send in a fraud proof transaction** even if the fraud happens contemporaneously with any of the above issues (or even a combination: fraud proof 1h after you go to sleep, consensus failure right after you wake up → 8 + 12 hours lost, still less than 24 hours, and that assumes you’re the only fraud prover and you can’t send in fraud proof txs during the consensus failure!)

However, note that 1 day is *not* enough for a new fraud proving node operator to spin up, and due-diligence the software enough to feel comfortable [putting down a 3600 ETH deposit](https://docs.arbitrum.io/launch-arbitrum-chain/faq-troubleshooting/troubleshooting-building-arbitrum-chain). Additionally, it’s not enough time for a 6-of-8 security council to respond to a bug.

To solve both of these problems, **I would highly recommend a mechanism where any security council member can flip a switch to extend the delay to 7 days or even longer**. This ensures 1-2 day withdrawals in the normal case, but gives enough time to resolve issues when they do arise. For the same reasons as above, 1-2 days *is* enough time for the fastest member of a security council to be able to flip that switch, even if an exceptional situation happens.

Because of the above, I would argue **1-2 days is enough to deal with any problem other than a 51% censorship attack on Ethereum**.

## 4. My tentative conclusion: 1-2 days ok for stage 1, 7 days for stage 2

A **stage 1 rollup** can already be hacked if 75% of the security council get hacked. A 51% censorship attack on Ethereum is already an extreme situation, similarly extreme to 75% of a security council being hacked. Hence, for rollups that already accept stage 1 assumptions, the somewhat weaker properties of a **1-2 day window seem fine**.

For a **stage 2 rollup**, the goal is to achieve true Ethereum-equivalent security. Hence, we *do* want to be 51% attack resistant, because Ethereum itself is 51% attack resistant (in the sense that if you hold ETH on L1, you keep that ETH even if a 51% attack happens; an attacker cannot make invalid state transitions happen). So **we want the 7 day delay on any optimistic components**.

Note that **this does NOT mean that when rollups upgrade to stage 2, we will see a degradation of UX or liquidity costs**. The reason is that I expect stage 2 to come from a [2-of-3 scheme](https://ethereum-magicians.org/t/a-simple-l2-security-and-finalization-roadmap/23309), where an optimistic prover is only one of the three. **In the normal case, instant proving systems (either ZK + TEE, or ZK + ZK) will ensure near-instant withdrawals**. Hence, liquidity costs will be far lower than even 1-day-withdrawal optimistic rollups. The 7 day window will only come into play in the exceptional case, when an instant proof system breaks and the optimistic system needs to come in to serve as the tiebreaker.

## Replies

**donnoh** (2025-11-03):

Is the fact that reducing the challenge period adds several billions now and potentially more in the future to the bounty to perform a a strong censorship attack a concern? I really want to avoid making `rug-op-boost` appealing to validators

---

**rami** (2025-11-03):

[@donnoh](/u/donnoh) Why is the length of the dispute period related to how much bounty there is for the L1 to eat the L2s?

---

**hal2001** (2025-11-04):

Hart from Across (the intents protocol) here. I’m personally been pushing for shorter L2 withdrawal times because it vastly improves intents (aka fast bridging) from L2s. Some very quick thoughts that I can elaborate on if others are curious:

When thinking about the cost of the 7 day bridge to (intents) solvers, there are two factors to consider: (1) is the obvious cost of capital (aka 7 days is 7x cheaper than 1 day). The other factor is harder to model: it’s the “I’m not sure if my capital will get locked for 7 days or not”.

The harder to model factor has a sort of impossible-to-price uncertainty. For some actors, the risk of a 7 day lock on funds is simply unacceptable and there’s no (reasonable) price they will be ok with (they simply can’t risk being captial constrained for 7 days). I think 1 day removes most of that risk, but it’s not entirely obvious. (I think that risk is completely gone at 1hr or 2hr).

Concrete example where 7 days to 1 day would make a huge difference. Occasionally solvers see one-way flows off of an L2. Say, for example, there is a $10m of net outflows from an L2 (and this definitely happens). From my experience, a solver is unwilling to lock up $10m for 7 days at almost any price. It’s sort of like that solver goes “out of business” for a full week—and it’s hard for them to predict how much money they could make that week if they did have the $10m available. So again, it’s sort of a weird hard-to-model cost. To cover this uncertainty, solvers start charging crazy high rates to lock money for 7 days (like 200bps, aka 2%… or more). This essentially acts to “shut off” the fast bridging off that chain—there is just no liquidity. A 1 day bridge would reduce this uncertainty an awful lot, and probably cap rates at something more reasonable (like 25bps, or 0.25%). A 1 hour bridge would cap this at like 2bps… so that’s where we want to get to.

But even without a 1hr bridge, 1 day vs 7 days helps a huge amount. No solver wants to be locked out of their money for a full week; 1 day is both economically and psychologically much more tractable than the current status quo.

---

**vbuterin** (2025-11-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rami/48/16382_2.png) rami:

> @donnoh Why is the length of the dispute period related to how much bounty there is for the L1 to eat the L2s?

The argument is that if the dispute period is lower, then there is a larger risk that a 51% censorship + theft attack will actually succeed, because the community is unable to coordinate to fork away the chain in time.

Though I’d argue that even at the 1 day level, the cost of a censorship attack (serious risk of millions of ETH being slashed) is lower than the reward (I don’t think the L2 TVL is as high), so it’s ok at the current stage, though eventually we do want stage 2 + ZK.

---

**rami** (2025-11-04):

[@vbuterin](/u/vbuterin) I spoke with [@donnoh](/u/donnoh) out of band and got some similar clarification, but still in my view the bounty is always the TVL/TVS, and the probability of success with 51% is always 100% regardless of how long it takes. I say this because “the social response” is not something that’s clearly planned out and proven to “stop” the attack. For example, would this response be triggered if just some $20M TVL rollup is at stake? To me, the social response is like a nuclear deterrent, but you can short ETH before you push for its activation and end up winning even if you get slashed significantly.

---

**Zodomo** (2025-11-04):

Shorter windows are likely worthwhile. I think the pricing difficulties raised by [@hal2001](/u/hal2001) has more to do with L2’s remaining Stage 1. Solvers already price intents with this 7 day window in mind. This change would make it cheaper for solvers already okay with these optimistic designs. Anyone refraining from solving due to the longer optimistic period may be unswayed by a reduction in best case times, and the only way to cater to them is by L2’s reaching Stage 2 properly. This would improve operations for those running solvers today, reduce costs for users today (even if only a little due to incalculable likelihood of increased delays), and gives the community even more ammo to nudge L2’s towards Stage 2.

I’m totally in favor of reducing these windows today, with a 1-of-N assumption that it can be temporarily reverted to 7 days in the event of an emergency. Especially as it brings many user-facing benefits.

---

**ellie** (2025-11-04):

I do not have a strong opinion either way, but here’s some thoughts fwiw:

- 2/3 proving systems are very close to ready today.  Reducing the fraud window is not at odds with accelerating 2/3 proving systems, but I hope we can see some L2s with 2/3 proof systems extremely soon.
- 2/3 proof systems will likely remain more expensive than fraud proof systems alone since the ZK proofs are currently expensive, and provers need to be incentivized (or subsidized by the L2 itself) to account for these costs.  In natively ZK rollups the ZK proving cost is already part of the economic model.  ZK proving cost is not part of the economic model of current optimistic L2s.  This could potentially create friction for stage 1 rollups wanting to upgrade to stage 2.  They now need to extend their fraud window to 7 days, meaning they have UX regression, or they need to find a way to pay for ZK proofs to support the 2/3 proof system.  Realistically, many stage 0 and 1 rollups today are frugal with their onchain costs, and this may prevent them from upgrading to stage 2.  Proof aggregation layers can help here, as well as cheaper ZK proving.  Both will come with time.  This isn’t an unsolvable problem–it’s just something to consider.
- This thesis seems completely reasonable, but before officially changing any stage definitions in L2 Beat we should have concrete data analysis to confirm the claims.  For example, can we compare liquidity bridge fees between optimistic and ZK rollups today?  Is there a meaningful fee difference when we control for other factors?  Can we confirm this fee difference is due to the canonical bridge delay?  Or is it due to other factors?  I’d love to have more input from solvers themselves (like Hart!).  We should also confirm whether this really will make more users use the canonical bridge / liquidity bridges.  If users already are used to using trusted bridges that still offer much better UX, they will likely continue that behavior despite this change.

---

**tim-clancy.eth** (2025-11-04):

Code is law, a 51% strong censorship means we already failed, there shall be no bailouts for optimistic rollups. Sorry! That’s simply the cost of doing business in a non-validity-proof regime.

Therefore it’s fine to have less than seven days for a fraud proof to play out. I like the security council “add additional delay” switch.

---

**gluk64** (2025-11-04):

This would legitimize PoA nature of today’s optimistic rollups (who rely in practice on security councils instead of fraud proofs).

What’s worse: this would create an insurmontable anti-incentive barrier for any of them to ever reach Stage 2.

It means that the security mechanism of fraud proofs won’t ever be subject to the same rigor as we do for ZK proofs, rendering hybrid proof mechanisms pointless.

Why don’t we just leap straight into the future with multi-proof ZK?

---

**nambrot** (2025-11-05):

I mostly agree with the commentary (especially from [@hal2001](/u/hal2001)) that this has significant benefits for overall interop that that alone makes this likely worth it. Maybe my 2c I would love to have reflected in the broader discussion is a recognition that there are a lot of levers to be played with.

For example, I really like the proposal to have security council members being able to extend the withdrawal window to the full 7 day. What if a 2/2 or 3/3 multi-proof system can override a malicious security council member. This would give us the benefit of immediate withdrawal reduction windows with limited censorship ability from the security council member.

Another thing I would love to explore is whether rate limits can make sense here. i.e. I would imagine that for many chains, withdrawal windows only matter for a super small subset of the value locked. What if we only allow 1% of TVL to be withdrawable in that 1 day window, and after that, you do need to await the full 7 days. You could again pair this with instant proving systems where larger withdrawals just have to go through the ZK+TEE path.

Reckon me biased, but I feel like we have the expressiveness of the L1 here to help us encode more granularly than just (1 vs. 7 days)

---

**rudolf** (2025-11-05):

From [@haydenadams](/u/haydenadams):

> 7 day withdrawals are the single thing most holding L2 adoption back - figuring out how to safely and quickly lower is probably the highest leverage thing the EF can do to accelerate Ethereum adoption. I’ve spoken to top market makers in the space and they’ve cited long withdrawal times as by far the biggest blocker to holding increased amounts of capital on L2s

> Generally 7days is a life time for market makers. 1 second would be ideal but a day is much better than a week. lets say you were willing to subsidize $10m of fast withdrawals - this is the diff of $70m/week and $10m/week

---

**greg** (2025-11-05):

[@rudolf](/u/rudolf) & [@ellie](/u/ellie) thanks for bringing this to my attention.

Greg from Sprinter/ChainSafe/Lodestar I’m speaking from the point of view of solvers, market makers & core developers.

[@hal2001](/u/hal2001) covered a lot of the topics very well.

As Hart mentioned it is 7x cheaper from 7 days → 1 day, while in reality its hard to actually compute that cost efficiency but its probably much closer to a 50x-100x cheaper, as we count in minutes, not days. For every minute of capital I can efficiently rebalance I can re-compete in the next auction to make more money. In most intent systems, we have two options 1) deal with rebalancing ourselves, or 2) pay an LP (like in across) to front me the funds early. Depending on the route and asset the total revenue generated can be anywhere from 0.5bps - 10bps (typically on the lower side), which is then split between the solver, and the LP. When dealing with rebalancing ourselves, we either default to a CEX for fast exits, or use a separate bridge/clearing mechanism such as Everclear. Another note is that its not often in our best interest to rebalance immediately, waiting for some transactions to settle, and clear after 30-60 minutes is *ok* in most cases, i mean there is a reason even VISA waits 1-3 days…lol

Reducing the L2 exit window CAN impact the solver and market maker community but only if its done in a significantly more dramatic way, I’d argue down to a few hours. The name of the game  really comes down to how efficient you can be with as minimal capital as possible. Naively you can illustrate this with a simple formula:

`capital_required = (daily_volume_rebalanced * settlement_delay)/rebalance_frequency * buffer`

It becomes a difficult question of incentives if the wait time is longer than 3 hours, and usually custom deals need to be made to satisfy the delay. So instead what we do is:

1. Pay LPs (eg across)
2. Use a different bridge
3. Use CEX

Frankly, these all work just fine, i have no qualms. My gut instinct say that if we go from 7->1 day we might see the LP fee go down by a marginal amount, say 20-30%, simply because the cost of locking up is still relatively high, and margins are already so low they need to compete with other protocols offering 5-6%. CEX is actually a great option too, depending on the chain a full rebalance might only take around 20 minutes and with enough volume the discount applied is actually good and can often be under the cost of the LP payment.

Now, from the POV (not necessarily myself) of decentralization maximalist, or just a protocol developer. I want to eliminate the centralized entities as fast as possible. If a CEX is the most efficient way to rebalance (cost + time) we aren’t doing enough. Simple as that. We should strive to reduce as far down as we can safely go, there is no reason to be putting funds at risk.

TLDR: Think in terms of hours, not days. Every hour illiquid capital, increases the overall capital requirement. Reducing the window more aggressively to hours is unquantifiable, but probably in the magnitude of >100x improvement to what we have today. IFF decentralization is the primary goal, benchmark off of the cost of using a CEX, and eliminate them as an option.

EDIT-1: grammar

---

**greg** (2025-11-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nambrot/48/6366_2.png) nambrot:

> Another thing I would love to explore is whether rate limits can make sense here.

I don’t think this is a good idea, its all or nothing IMO. Too many edge cases would open up around how to handle double spends (released early, but then we have halt/rollback, it gets ugly).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> A 1-day withdrawal window is enough to ensure that you can send in a fraud proof transaction

I disagree with this statement, no one is manually rolling a fraud proof transaction. IIRC Optimism has randomly automated fraud proof challenges on mainnet as part of their QA/smoke testing. I would expect all this to be automated down to the block, and frankly if they’re not thats a huge probelm with the L2 security teams. If a chain needs to be challenged this should just happen naturally.

Based on the events more recently regarding Balancer, I think as a community even if a multisig needed to make some soft-changes etc they should be able to react fast enough. To the previous point, if a challenge comes in, the bridge should automatically be falling back to a delayed settlement iirc, and if it doesn’t thats a good lever to pull on.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> However, note that 1 day is not enough for a new fraud proving node operator to spin up, and due-diligence the software enough to feel comfortable putting down a 3600 ETH deposit. Additionally, it’s not enough time for a 6-of-8 security council to respond to a bug.

Honestly, the L2’s or the EF should seriously consider running a fallback, relying and random firms or DAOs to run faud proofs sounds like an absolute disster waiting to happen.

---

**haydenadams** (2025-11-05):

Came here to say all this but Josh got there first

Huge fan of this proposal and think its a great step forward

The debate between faster stage 1 withdrawals vs faster push to stage 2 is kind of reminiscent of the debate between focusing on L1 scaling or L2 scaling, which I think most people now agree the answer to is “both”

---

**ptrwtts** (2025-11-06):

How about TEE Prover + 1 Day for Stage 1?

---

**ryanberckmans** (2025-11-11):

As Mark from OP [said](https://x.com/tyneslol/status/1988205944107659762) on twitter, we are “managing by committee” on this issue. However I don’t think Mark’s quote appropriately acknowledges the true high risk here and thus rationale for a base-layer-style decentralized governance process.

If we reduce the withdrawal window to 1 day, the downside risk seems almost immeasurably high because a successful attacker is not just stealing locked funds on an L2 but also greatly harming the reputation of Ethereum’s L1+L2 model. Perhaps irreparably so.

Given the path-dependent nature of the L1 competitive landscape, the last thing we need is a major reduction in the public’s belief in the L1+L2 model at the time when it’s really starting to thrive.

Others have said that the rigorous economic analysis seems to be lacking here to justify a reduction to 1 day. I remember the Roughgarden paper for EIP-1559. Where’s that high level of science here?

As Alex G said, “why don’t we just leap straight into the future with multi-proof ZK? Why risk reducing the ORU fraud dispute window at all?”

If we must reduce to 1 day, why not 2 days instead? 2 days is 2x the capital cost of 1 day, but a sustained censorship attack gets exponentially less likely to succeed with 2 days vs 1 day (because the attacker has to win every single slot, right?), and a 5-day reduction (from 7 days to 2 days) delivers most of the benefit compared to a 6-day reduction (7 days to 1 day).

Overall, I’m a layperson on this, but the proposed reduction to 1 day seems suspicious and risky to me.

---

**potuz** (2025-11-11):

Adding something here cause I haven’t seen this in the thread. The separation of strong vs weak censorship is not that important here. Strong censorship by a 51% attack can be detected on-chain by oracles on missed slots and thus the contract itself can increase the withdrawal window to 7 days in a trustless manner (yes, this leads to false positives and grieving attacks but won’t get there).

The only type of attack that matters IMO is the economic attack of weak censorship for a single transaction. It is not as simple as:

- Censoring just one transaction since as soon as the 1st transaction lands the protocol can automatically extend the window to 7d: the attacker’s budget can be spent either in the 1st transaction or later in censoring the remaining challenge transactions during the 7 day period.
- The expected budget is the rollup TVL: the attacker can leverage shorts offchain or would simply profit from driving the rollup out of business.
- FOCIL solves this: not really, besides the 51% attack on FOCIL, the attacker can spend the budget in only bribing the proposer or the builder (instead of the 16 includers) into not producing a block when the proposer is not from his controlling stake. The proper analysis is not that trivial as if it were “multiple proposers”.


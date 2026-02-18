---
source: ethresearch
topic_id: 5225
title: Penalties and conserved quantities in state channels
author: technocrypto
date: "2019-03-28"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/penalties-and-conserved-quantities-in-state-channels/5225
views: 2811
likes: 8
posts_count: 18
---

# Penalties and conserved quantities in state channels

There are two different ways of doing penalties and fee-splitting (where multiple parties share the costs of on-chain transactions) in channels.

In one approach, specific funds or assets are set aside as “deposits”.  These “security deposits” can be thought of as belonging to a certain “state channel game” which conserves total asset quantities, and uses as inputs or “moves” the different signed messages passed back and forth amongst “players” in the channel, and/or various states of the blockchain.  When one player makes a certain “move” in this game by, for example, publishing an out of date state to the chain, another player may be able to respond on their “move” by providing evidence of this fact (such as a later state which has been signed by the first player), and then the game would allow them to claim the other player’s deposit, or be refunded a tx fee, or whichever penalty/fee the protocol demands

In the second approach, particular funds/assets are not necessarily set aside as deposits. Instead, the assets within a channel may be fully allocated to the set of open “channel games”. Penalty logic also exists, but is not restricted to act on assets of a separate “deposit”. Instead, penalties take “priority” over other channel applications, allowing them to use the value of the assets which may be owned partway through a chess game as part of the penalty structure, for example.  This also permits penalties such as “loss of all assets/state” to be enacted, analogous to the Lightning Network’s approach.

On the face of it, the second approach appears to be strictly more flexible, and also more capital efficient for certain penalty structures, than the first.  But a natural question exists: can we encode the second approach within the style of the first approach?  And yes, it appears that we can.

To do this, we can modify every single application run within the state channel to entail the entire penalty process as part of its own state transition logic.  Now, assets can still be allocated fully to individual channels, but all assets are also part of the penalty scheme, since the penalty scheme is contained within every application.  In addition, we must have some sort of “default rule” for the base layer channel mechanism which allocates all assets to an instance of the penalty game unless otherwise allocated to another application. This prevents penalties from being temporarily “paused” when an individual application, such as a chess game, is finished.

Obviously, this naive approach has a lot of drawbacks.  Depending on the architecture, it may rely on every single game developer correctly implementing the penalty scheme.  It may require the closing and re-opening of all applications when the penalty policy needs upgrading. It may require multiple penalty policies and complex logic to be applied beyond individual state channels as part of state channel networks, where the counterparty to the metachannel/virtual channel is not the direct counterparty, and one needs to differentiate between the loss of the assets locked to a metachannel locally, and the *net* loss of that asset movement across the entire chain of interactions (a.k.a. misbehavior by the adjacent connection vs misbehaviour by the remote party to the metachannel).  If long-running metachannels are “left open in the background” as part of various mechanism design use cases, the cross-application upgrade to a fee policy may be impractical. etc.

For these, as well as many other reasons, I have always steered away from trying to enforce the notion of asset conservation at an *architectural* level in state channel designs (as opposed to enforcing it within a subset of the overall channel’s structure, which is obviously quite useful for many purposes).

Last Thursday the excellent Tom Close gave a presentation on his Nitro paper (from February) in the state channel researcher’s call.  In the paper, and the call, he claims that the paradigm of “total asset conservation per channel” which the paper proposes is capable of supporting “arbitrary” state channel techniques, which I have expressed skepticism of, both privately before the paper’s release, and again on the call. He asked me to document specific cases where I thought the approach might fail or have serious drawbacks, which is what prompted this post.

Security penalties and fees are not directly treated by the Nitro paper, but the general scheme used would seem to imply that the first of these two approaches I describe in this post is the only one compatible with his approach, and since security penalties are a crucial element of state channel design I thought this was a good place to start.  There are a very large number of scenarios that I am skeptical can be handled effectively by the Nitro protocol, which I view as being useful primarily for its clear formalism that targets a specifically identified subset of use cases, rather than as a technique that should be used for arbitrary applications.  In particular I am a highly outspoken critic of the tendency for people to view generalized state channels as “just asset transfer with arbitrarily complex conditions”, as I have mentioned many times before in analyzing various other proposals for state channel architecture.  But since considering each of those scenarios in relation to Nitro protocol specifically would take quite a bit of time for both of us, I hope this post can at least kick off the conversation in a more concrete way, while also exploring topics that the Ethereum research community more broadly can find useful along the way.

**Questions for Tom:**

First, (assuming my take on Nitro is correct) is there a better way than my “naive” version to implement security penalties within your approach?  (The following questions assume that there is, but I don’t want to propose one on your behalf).

Within such a proposed technique, how would an upgrade of penalty/fee policy for a “ledger channel” counterparty’s misbehaviour look? How about an upgrade of penalty/fee policy for a remote “virtual channel” counterparty’s misbehavior? And in the example, does either have to be aware of the process for the other?

Also, in the proposed technique, does the base channel object have to be directly aware of and implement the penalty/fee policy as well? This appears to be required in my naive approach, but I’m curious to see how this would work in your preferred take.

## Replies

**tomclose** (2019-03-28):

Just to confirm I understand the question: penalties apply when one participant, p, does something provably bad. The classic example of this is p challenging with a stale state, defined to be a state other than the last one that p signed. Another participant can prove that this was bad by providing a later state signed by p.

You describe two different approaches. Also to check my understanding, here is an example of each:

*Approach 1:*

A and B open a state channel, X. They each contribute 5 coins into X and 1 coin into SD[X], a security deposit for X. Inside the channel they play two games simultaneously: (i) a game of rock-paper-scissors (RPS) where they each wager 2 coins and (ii) a game of chess (CHS) each wagering 3 coins.

A is losing at RPS, so decides to try and cheat by registering a stale state on-chain. B proves that A challenged with a stale state and is therefore able to claim the entirety of SD[X] (assuming that’s what the penalty rules say). None of this affects CHS.

*Approach 2:*

A and B open a state channel, X. They each contribute 5 coins into X (but don’t need to deposit anything into SD[X]). They play RPS and CHS, as before.

Again A tries to cheat, and B proves that the state they challenge with was stale. This time, B is able to receive all 10 coins from X (assuming this is what the penalty rules say). By cheating at RPS, B has also forfeited CHS.

Assuming that the understanding above is correct, I’ll continue with the questions…

We haven’t yet specified how penalties will work in Nitro but we would probably proceed with a slightly different approach:

*Approach 3:*

A and B open a state channel, X. They each contribute 5 coins into X (but don’t need to deposit anything into SD[X]). They play RPS and CHS, as before.

Again A tries to cheat by lodging a stale challenge. At the time they register the challenge they have to put 3 coins (say) into SD[X]. If B proves that A is cheating, then B claims those 3 coins. If not, those 3 coins are returned to A when B responds (in the case where A wasn’t cheating) or the challenge expires.

I believe this has slightly better properties than Approach 1, as the coins in SD[X] are only locked for the duration of the challenge, if a challenge takes place at all.

This applies for all channels - if you challenge in a ledger channel, L, or a guarantor channel, G, you would have to deposit into SD[L] or SD[G] accordingly.

I am unconvinced about Approach 2 in general: (a) it makes it harder to estimate the penalty, as the amount A is penalised by depends on the state of the game CHS - if A happened to be losing RPS and CHS, it’s possible that the penalty is actually 0; (b) it makes it harder for the players of CHS to reason about whether the game is still valid. Point (b) becomes especially nasty if the game CHS wasn’t chess but actually supporting a virtual channel between other participants - if all funding is suddenly yanked across to one player, all and every game in the virtual channel tree is affected too. In designing Nitro, we purposefully ruled out this type of interaction.

---

**technocrypto** (2019-03-28):

Your descriptions of 1 and 2 are correct examples of the approach. Regarding approach 3, I assume that at the time A submits their stale state to chain the blockchain cannot immediately distinguish between a “challenge” and just an attempt to withdraw because B has gone offline and is unavailable.

Are you saying that in the latter case you would require an additional deposit from outside of the channel to permit any attempted non-unanimous closing of the channel? This would certainly be useful in *some* circumstances, but what does a person do if all their funds are in the channel? The nature of state channels means that they can’t convince any third party the deposit is safe to make on their behalf. I hope you will agree with me that, even if we require parties to always have such funds available, your proposed approach is significantly raising the capital cost should we want to be able to levy nontrivial penalties, especially in the case that these funds are already owned by A within the channel, and also will limit any penalty size to the amount which can be deposited, meaning that you *cannot* leverage as high of a penalty as Approach 2 would be able to enact against someone who does have at least some balance in the channel.

In terms of virtual/metachannels, it is perfectly possible to “yank the funding” of just one *link* in the metachannel, with the remaining links being left intact. In fact, this is the correct behaviour when a ledger channel intermediary along the path has misbehaved, since it would leave any parties not directly in that ledger channel unaffected, with their channels all continuing to run fine, and the metachannel could be even be dynamically rerouted to another available path where the game would continue and permit even the initially wronged player to add their game winnings to the amount they received in penalty (at least that’s how it’s intended to work in our approach, I would consider any other behavior to be an error). I’d encourage you to work the example through. The key thing to notice is that capital is locked on *both* sides of any intermediary, and the condition of keeping the outcomes the same is what makes the “routing” not reduce the intermediary’s own balance. When they misbehave they sacrifice that symmetry, so that their own balance *is* affected, and that’s where the “extra” capital comes from for the penalty without anyone else being affected.

Backing out of the specifics here, it is definitely the case that LN currently uses Approach 2. Regardless of whether you prefer another approach (I personally think the incentives of LN should be tweaked slightly myself, for that matter), this means it is certainly an example of something someone might want to try. Is there a better way than my “naive method” for them to do that within Nitro protocol? Or will all methods of enacting “total penalties” have unacceptable drawbacks within that design?

---

**tomclose** (2019-03-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> Are you saying that in the latter case you would require an additional deposit from outside of the channel to permit any attempted non-unanimous closing of the channel? … what does a person do if all their funds are in the channel?

Yes. If all their funds are in a channel they can’t submit a challenge. I agree this raises the capital cost. The point is that even with all of this it is still strictly better than Approach 1 that you suggested, as in Approach 1 all these things are also true but the capital is locked for the duration of the channel where as in Approach 3 it is only locked for the duration of the challenge (if there is a challenge at all). It also means that the penalty scales with the amount of provably bad behaviour - if a participant repeatedly launches stale challenges, they will be punished multiple times.

It’s worth saying that the size of the penalty deposit can be set on a per-channel basis by adding a property to the state. This allows participants to make their own decisions about the deposit based on the funds stored in the channel, their funds on hand and their security requirements.

I believe I’m already on the same page as to how the yanking would work with virtual channels. Would you agree with the following statement? “In cheating at RPS with Bob, Alice forfeits CHS with Bob and her game of GO with Charlie and the payment she received for brunch from Danielle”. My previous comment stands: because the penalty is dependent on the state of unrelated channels it is very difficult to make any guarantee over the size of the penalty. You can put an upper bound on it (the total stored in all channels) but it seems like the only lower bound you can put on it is zero. It is also changes over time. It seems like it would be difficult to make any deductions about the incentives in the system when you can say so little about the penalty for bad behaviour at any given time. How do you see this working in practice?

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> Is there a better way than my “naive method” for them to do that within Nitro protocol?

I don’t believe there is - and that’s by design. We want to rule out the situation where a mistake* that Alice makes with Bob affects the payments she is receiving from Danielle. We want the state in our channels to be as self-contained and isolated from the occurrences in other channels as possible.

Just to confirm, is Approach 2 the approach to penalties that you’re taking in Counterfactual?

* Worth noting here that while challenging with old state is “provably bad” it could happen by mistake e.g. if Alice lost some states when her system crashed or similar.

---

**technocrypto** (2019-03-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/tomclose/48/3252_2.png) tomclose:

> in Approach 1 all these things are also true but the capital is locked for the duration of the channel where as in Approach 3 it is only locked for the duration of the challenge

This seems confused. In Approach 1 the amount in the “security deposit” channel can be dynamically adjusted, so the capital costs can be matched to Approach 3 (pretty much exactly like how your second paragraph works) except that the extra funds can be kept in the channel rather than left on chain, which seems strictly better. Not that it matters, because in my “naive” re-take on Approach 1 there is less capital costs than both, and I’m not advocating for Approach 1 anyways.  Counterfactual is in the “Approach 2” category, roughly speaking, because we would permit decisions about whether or not to conserve total quantities in penalty games (though we can support all of your Approach 3 stuff easily as a subset of this).

For your virtual channel example, things only look like that because in one very weird sub-case where Alice doesn’t have any “beneficial prospects” in any of her open virtual channels so she intentionally abandons them all as worthless. It’s also not the example I referred to, where Ingrid is the cheater and Alic keeps all of her channels with Bob, Charlie, and Danielle just fine.

As far as penalty schemas the design space is very wide, but it is obviously trivial to enforce a lower bound by only agreeing to channel combinations that still leave your counterparty with at least some balance. You’re just moving the upper bound from the strictly lower limit in the competing schemes (such as yours) all the way up to total assets in the channel PLUS whatever else is introduced in a challenge. It allows strictly stronger penalties.

For the last comment, the thing you’re trying to rule out isn’t an issue in our design. I don’t think you quite understand my metachannels example yet.

*I don’t think it’s ever worth continuing even if it is an error. If your counterparty’s software is malfunctioning you should “rescue” all of the state and you can manually give it back to them when their software is fixed. Otherwise you could end up destroying state needlessly.

---

**tomclose** (2019-03-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> This seems confused. In Approach 1 the amount in the “security deposit” channel can be dynamically adjusted, so the capital costs can be matched to Approach 3 (pretty much exactly like how your second paragraph works) except that the extra funds can be kept in the channel rather than left on chain, which seems strictly better.

Is it? A penalty deposit locked in a state channel is still funds locked that can’t be used elsewhere. The chain has no visibility into what’s locked in a channel, so it doesn’t seem like you can make the ability to launch a challenge dependent on how much is locked in the penalty deposit channel, which makes it impossible to do “just-in-time-for-challenge locking”. It seems, therefore, that the only way the participants get the security guarantee is to keep the penalty deposit locked for the duration of the channel.

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> As far as penalty schemas the design space is very wide, but it is obviously trivial to enforce a lower bound by only agreeing to channel combinations that still leave your counterparty with at least some balance.

The challenge here is not agreeing to channel combinations upfront but ensuring that the combinations of these channels maintains value as the state of those channels changes. In order to maintain a minimum penalty deposit, a wallet would presumably need to do keep a minimum total conserved across those channels. “Just lost chess? Well, you can’t make a payment in your payment channel (even though it looks like there are enough funds) until you sign an update that adds another channel to the penalty groupings.” That seems nasty because your channel updates are then coupled in non-obvious ways.

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> It’s also not the example I referred to, where Ingrid is the cheater and Alic keeps all of her channels with Bob, Charlie, and Danielle just fine.

If all these are supported by the channel with Ingrid, and all Ingrid’s money has been forfeited to Alice, it’s a bit like Alice has just won all these games. That’s not a problem for Alice. And it’s also not a problem for her opponents, as (because the funds aren’t conserved) it isn’t true that by Alice winning, they’ve lost. In this situation, it doesn’t seem like there’s an incentive for Alice to keep playing, as she has already won the maximum amount, so she should probably just resign and let her opponent win. This seems like a slightly counter-intuitive situation to communicate to a user.

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> You’re just moving the upper bound from the strictly lower limit in the competing schemes (such as yours) all the way up to total assets in the channel PLUS whatever else is introduced in a challenge. It allows strictly stronger penalties.

If you’re falling back on penalties locked up at the time of challenge to provide your lower bound, why bother with the other approach at all? I don’t believe it’s correct to describe the penalties as *strictly* stronger as the additional penalties could be zero. You can say that they’re strictly not weaker.

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> For the last comment, the thing you’re trying to rule out isn’t an issue in our design.

The things I’m trying to rule out seem to be inevitable consequences of an “Approach 2” system.

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> I don’t think you quite understand my metachannels example yet.

Could you identify the part you don’t think I understand and give a further example or something? You might well be right but I’m going to need help if I’m going to understand it better. ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)

---

**technocrypto** (2019-03-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/tomclose/48/3252_2.png) tomclose:

> it doesn’t seem like you can make the ability to launch a challenge dependent on how much is locked in the penalty deposit channel, which makes it impossible to do “just-in-time-for-challenge locking”

You can collect the deposit counterfactually, and make the request to close retroactively invalid if it is eventually shown that the deposit didn’t exist. This is financially equivalent, since in your scheme the deposit is refunded if the counterparty doesn’t respond (and pretty much has to be for safety).

![](https://ethresear.ch/user_avatar/ethresear.ch/tomclose/48/3252_2.png) tomclose:

> a wallet would presumably need to do keep a minimum total conserved across those channels

Of course you can implement this strategy in our framework if you *want* to, but there are far simpler strategies. For example, having a small, dynamically resized “security deposit” within the channel to guarantee the floor, and then just pushing the ceiling up to “all” or “almost all” would strictly increase penalties for protocol breaking without introducing any additional accounting requirements. I have a rough idea of what the “ideal” model looks like here btw but it’s basically a whole paper’s worth of analysis so I don’t want to try and fit it in an ethresearch post (and it gives different answers for different types of users). The root idea is just that everything comes down to the incentive gradient at all points in the landscape of choices, which is the fundamental rule of mechanism design.

![](https://ethresear.ch/user_avatar/ethresear.ch/tomclose/48/3252_2.png) tomclose:

> In this situation, it doesn’t seem like there’s an incentive for Alice to keep playing, as she has already won the maximum amount, so she should probably just resign and let her opponent win. This seems like a slightly counter-intuitive situation to communicate to a user.

That’s where you’re wrong.  Everyone is *safe* in terms of total capital impact in that situation, but if we program their wallets to *maximize* their gains in this situation Alice’s software will instantly propose an atomic transition to a different route, while the old route is cashed out in the manner which maximizes the cost assigned to Ingrid.  Remember, Alice has already won all of Ingrid’s money on *her* side of the link, but unless Alice was completely tapped out in all channels she had open Ingrid still has some money on the *other* side of that link, and Ingrid’s balance there depends on how the channel is closed. So Alice and all her metachannel counterparties can close that route with Alice “losing” everything from those games as far as Ingrid is concerned, while atomically opening up a new route where she’s been given almost all of that difference back (because we need a tiny incentive for the others to cooperate). The net result is that Alice keeps *all* of the assets she had in the ledger channel with Alice, and also gets, say, 95% of the assets on the other side credited to her along in a metachannel along a brand new route. Meanwhile her counterparty who agreed to re-route has kept all of *their* assets from the old metachannel in the new metachannel, plus gained 5% of what Alice had in the metachannel.  Both are very happy, because the difference has come from Ingrid the cheater.  Or to put it another way, the only significant net impact of Ingrid treating Alice incorrectly is that Ingrid pays Alice a large security penalty, which is exactly what we want here. We don’t *want* Ingrid to be able to get larger gains at the same risk just because Alice has a bunch of metachannels open and routed across Ingrid’s node.

![](https://ethresear.ch/user_avatar/ethresear.ch/tomclose/48/3252_2.png) tomclose:

> If you’re falling back on penalties locked up at the time of challenge to provide your lower bound, why bother with the other approach at all?

I don’t actually think this is going to be very useful in most cases because of the additional friction it introduces to user experience, but I was merely pointing out that you *could* still do this if you want. The whole point of our approach is to leave open the possibility of literally any channel construction, after all. The reason I say “strictly” is that I’m assuming a “channel user” has at least *some* channel open with at least *some* assets in it, otherwise I wouldn’t consider them a channel user. I can apply those assets to the penalty, while in your scheme you cannot, which is the strict advantage. I also haven’t detailed this, but there is a fully incentive compatible way to do the “paying your last assets away” step in a channel, which maintains good incentive gradient throughout (just as an aside in case you’re wondering).

![](https://ethresear.ch/user_avatar/ethresear.ch/tomclose/48/3252_2.png) tomclose:

> The things I’m trying to rule out seem to be inevitable consequences of an “Approach 2” system.

If you’re talking about “mistakes” then there is no way to make it so that a software error is unable to affect all open channels handled by that software. But beyond this I think that once you understand the metachannels example above you’ll see that you’re currently optimising the wrong side of the interaction. You **want** to bring the hammer down as hard as possible on provable protocol violations, that’s the whole point of the state channel strategy. What you should be asking is not, “what makes this easier on accidental protocol violators” but rather “what maximizes safety for people running software that correctly follows the protocol”. Because the latter is how you actually *incentivize* software to be strict about following the protocol. If someone’s software is malfunctioning, you *should* take all of the state away from them. You can always give it back later if you decide it wasn’t their fault, but you shouldn’t be trusting provably buggy software which may or may not have been intentionally modified with further assets. That’s just clearly the wrong incentive structure for the “do I run the exact protocol as specified” side of the game. It’s like saying, “I’ll only cancel *part* of the block reward for an invalid header that still has a valid PoW attached, because I don’t want to be too mean”. That’s just not the way to incentivize correctly behaving software to be run, and will actively generate plausible deniability for actual attacks to be conducted under.

Re your last comment the metachannel example in this post is my current angle I’m trying to use to explain this. I’m trying to show how the incentives actually work in my proposed tactic, and why they’re preferred to your deposit-at-attempted-close plus limit-penalties-to-particular-designated-funds approach. You don’t actually *want* weaker incentives against protocol violation. You really don’t.  I do think that Nitro protocol is a useful thing to run within a state channel. I just don’t think it encompasses *all* the useful things we want to do (and security deposits are really only one of many, many examples).  It’s a matter of scope.

---

**tomclose** (2019-03-28):

When you say things like “once you understand the metachannels example above you’ll see that you’re currently optimising the wrong side …” it makes me feel hurt because I want my arguments and opinions to be treated with respect, even if you believe them to be merely the product of a misunderstanding. If you feel like I have misunderstood something, please feel point out specifically where and how. You might be right that I will subsequently change my opinions but that’s the only way you can know for sure. ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)

It seems like we’re going round in circles a bit. The following quote summarizes things for me:

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> I don’t actually think this is going to be very useful in most cases because of the additional friction it introduces to user experience, but I was merely pointing out that you could still do this if you want.

Overall, you are pointing out that Approach 2 isn’t possible in Nitro. I agree with that - it isn’t. I’m arguing that it has some undesirable properties, which means it isn’t completely obvious whether you’d want to use this approach anyhow. You seem to agree with that - but that the point stands that you *could* implement this in Counterfactual but you *couldn’t* implement it on top of Nitro. This is correct.

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> You want to bring the hammer down as hard as possible on provable protocol violations, that’s the whole point of the state channel strategy. … If someone’s software is malfunctioning, you  should  take all of the state away from them.

As discussed in the state channel researchers call, I’m not sure everyone would share these opinions. My take would be that you want to punish protocol violations sufficiently to discourage them, but this doesn’t necessarily mean you should always punish them maximally. I get that malfunctioning software is a protocol violation but I’m not sure I (personally) would want to be a user of a framework which adheres to your stated philosophy.

---

**liam** (2019-03-30):

Just read this; some thoughts:

**On maximizing penalties**. Jeff is defending maximally penalizing a user for malicious behaviour. From a game theoretic point of view this is the optimal strategy. However it assumes correctly implemented software. From a *practical* point of view it is likely people like myself, Tom, or others writing the software will make a mistake. So, it is wise to have a buffer to handle the case of the software behaving incorrectly and unintentionally submit old state or something like that.

This isn’t really a useful argument in my opinion. There is no clearly “right” side of the argument. I would argue the best thing to do is ensure the architecture of the software can eventually support maximal penalties once we have enough confidence in the implementation, but perhaps don’t maximally penalize literally as of today March 30th.

**On mistakes**. A key argument Jeff is making is that software errors can lead to you losing all of your money, anyway. So, if we’re intending on writing correct software, why not shift some extra work to manage more complicated scenarios onto the software too. One thing that Tom had brought up was that Approach 2 “makes it harder to estimate the penalty”. I would argue this isn’t really true because software does this assesment for you and it is deterministic.

**On approach 2**. A bunch of the work we’ve done has also been to mitigate the worst-case scenarios of someone attacking you with stale state. Say, for example, that you open and close 1000 channels inside a ledger channel. It is possible for someone to submit 1000 concurrent challenges against you. It would be nice to refute all 1000 challenges with a single transaction. This is possible in our current approach somewhat because of some properties of Approach 2; specifically the ability for the outcome of a channel to be dependant on some external value (e.g., the outcome of another channel or on-chain property / a `view` property).

**On research vs engineering**. We should work to separate out the actual optimal research decisions such as maximal penalties and the practical engineering decisions that go into short-term releases of software. This seems to be the bulk of this discussion.

**Side-note**: Just to disambiguate something here, “Counterfactual” is being used interchangeably to represent the  [software](https://github.com/counterfactual/monorepo) and [the paper](https://l4.ventures/papers/statechannels.pdf) in this discussion. Our approach to the software is to build the most simple and usable framework *now* but designed with the kinds of optimizations discussed in this thread such that they are easy to transition to in the future. For example, a state machine based application is an example type of application in the framework which all APIs are designed around, but it not the only way the framework can be used. Another example; although Approach 2 & 3 are separated in this discussion, we’ll probably start with Approach 3 for the initial approach of the software because it is easy to implement. Seems to me like over time (assuming people use channels more) Approach 2 will become strictly better (because more funds will be in channels), but this depends on usage.

---

**technocrypto** (2019-04-03):

Sorry for the delay in responding here, guys, I was sick for a few days there. The first thing I want to say is that it is definitely not my intention to make anyone feel treated with disrespect. I go hard on technical rigour, as Liam can definitely attest, but this is certainly not out of any personal animus or lack of appreciation for people’s work. “Security mindset” can definitely be mistaken for rudeness, since it involves an intentional search for mistakes, limitations, and edge cases in systems that people have genuinely put a lot of effort and attention into. Ideally such criticisms can be seen as positive contributions toward the overall work of providing end users with secure, hardened, and functional tools; rather than as disrespectful or demeaning.  That is certainly the mindset I am coming from: we are all on the same team of trying to make blockchain software secure, usable, and featureful for actual users in the world.

On the penalties side I think neither of you (Tom or Liam) are understanding my core point here. I’m not just making a subjective argument that I like larger penalties because I want to be mean to people who break the protocol or some totally social consideration like that. Incentive compatibility (and ideally, a protocol-compliant Nash equilibrium as well) are formal properties of a protocol spec combined with a payoff table of some sort. Whether or not people *like* incentive compatible protocols in practice is a totally different question, though I realise I have mixed in arguments about why incentive compatibility is desirable in the first place with my comments about which penalty schemes *are* incentive compatible (that’s my bad). There are two properties of the payoff table here which I don’t think you guys are taking into account.

First, I think we can all agree that the successfully publishing out of date state can result in a benefit *A* to the successful publisher of (value of best past state) - (value of current state). Similarly we can note that other parties to the channel will incur costs *B₁,B₂, etc*, respectively of (value of current state) - (value of published state). Note that the sum of *B₁,B₂, etc* need not equal *A* if some value is destroyed or created in the process of publishing stale state, or if the parties value the state differently, etc. Given a penalty amount *P* and a real world chance of publishing old state successfully *S*, an incentive compatible state channel protocol which wants protocol-compliant software not to publish old state can *only* permit values of *A* for which *S* * *A* < *P* . This is a hard bound. For any fixed values of *P* and *S* there is a specific *A* which caps the amount of “bi+directionality” a channel can permit (that is, the difference between any channel participant’s “best” past state and any new current state entered into). Making *P* larger strictly expands the “risk bandwidth” *A* which a channel can permit while remaining incentive compatible. I’ve omitted fees here, but they only have an effect on incentive compatibility when fees exceed one of *B₁,B₂, etc* and even then it depends on your agent model and a bunch of decision theory stuff. *P* is the dominant factor.  So adding more to *P* from any source (especially from within the channel if assets already exist there, since they will be cheapest in terms of capital cost) allows strictly more incentive compatible channel states. I do separately argue that incentive compatibility is *desirable* for a state channel design, and certainly this is the dominant position right now among blockchain researchers who I respect.  Even if users are willing to follow protocols at their own personal expense this isn’t a property one generally wishes to *rely* upon for safety of a mechanism. I would deeply question any contemporary blockchain mechanism which isn’t aiming for some reasonable approximation of incentive compatibility.

As relevant as this first property of the payoff table is though, the second property really blows it out of the water: the existence of a *hidden payoff table*.  No matter how well our software is able to track the value of the assets in a state channel (and this is already quite hard in general), there can always be other incentives, outside of the protocol entirely, which play into parties’ decisions for whether or not to run protocol-adherent software. These can include bribes, knock-on effects of being successful at publishing old states, conflicts (in which losses *B₁,B₂, etc* are valued *positively* by some other party), etc.  We can model these out-of-protocol incentives as a hidden payoff table which adds directly onto values *A,B₁,B₂, etc* above.  This is where maximising P *really* gets critical, because theoretically *any* permitted difference between a past and current channel state could result in **arbitrarily** high values of *A*, and any protocol (even Nitro) has to build in some *real world* estimate of how this hidden payoff table looks to maintain the property of incentive compatibility. In practice I think “attacking multiple channels to exploit chain congestion” and “conflicts with small to medium budgets” are the most important real life sources of hidden payoffs (these are why our paper talks about minimizing the costs of responding to stale state attacks, and about bounding griefing factor in channels).  But regardless of *what* you believe about the real-world values for this hidden payoff table, it’s clear that *P* becomes even more critical when we take them into account, because they suggest that *A* can be higher in practice than just what we directly see inside the channel.  You really do want to maximize *P* here. It’s not just my opinion, it’s a requirement for incentive compatibility over a wide range of thoroughly realistic and highly useful protocol states (c.f. bidirectional payment channels). Or else you’re throwing incentive compatibility away.

There are several other points that I think are very relevant here, but these are two of the most important ones, and I hope you both can agree that they aren’t primarily anything to do with subjective opinions. It’s a different thing to argue that you don’t *like* incentive compatibility than to argue that maximising *P* isn’t the way to get it.  It definitely is. That’s just how the math works out.

For Liam’s other points I just want to clarify that I think you’ve mislabeled our initial “MVP” target for Counterfactual as Approach 3. Approach 3 (as Tom described it) relied purely on fixed external deposits at challenge time. That’s not really our plan as I currently understand it, but we can clarify that offline. I just don’t want readers of this thread to be confused about your statement. The “MVP” approach we’ve discussed so far has fixed penalties *within* the channel, not deposited separately at challenge time. But that’s a minor quibble.

---

**tomclose** (2019-04-04):

I think it’s fair to summarize your argument as follows: to be “incentive compatible” we need to ensure that the expected payout from a successfully publishing bad state is less than the penalty P; but due to the existence of a “hidden payoff table” we can’t know what the expected payout is; therefore the only option is to maximize P.

I believe the following thought experiment shows there is something amiss with this conclusion. We’ve already established that one possible component of P is a deposit, d, that is provided at the time the challenge is launched (as in Approach 3). How large should d be? Regardless of any other components of the penalty, increasing d always increases P. Any penalty scheme that maximizes P should therefore (a) have a non-zero d that (b) is as large as possible. But, as you pointed out earlier, setting d to be large is undesirable as it “is significantly raising the capital cost should we want to be able to levy nontrivial penalties”. This contradiction shows that you already accept that it isn’t as simple as just maximizing P - there are other factors that need to come into play when designing protocols.

As I’ve said before, I believe that the important thing here is to punish protocol violations sufficiently to discourage them - and to be clear about the level of protection the penalties provide. No protocol can tolerate arbitrarily high hidden payoffs, but a well designed protocol can identify a set of economic bounds within which “incentive compatibility” will hold. Using Approach 3 on Nitro makes it possible to do this with a minimal amount of complexity.

---

**technocrypto** (2019-04-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/tomclose/48/3252_2.png) tomclose:

> I think it’s fair to summarize your argument as follows: to be “incentive compatible” we need to ensure that the expected payout from a successfully publishing bad state is less than the penalty P; but due to the existence of a “hidden payoff table” we can’t know what the expected payout is; therefore the only option is to maximize P.

I only agree with this argument up until the first semicolon. Not only do we have partial knowledge about the hidden payoff table, the argument for maximising P is not derived from our lack of knowledge about these payoffs. Rather, the argument is that for any specific model of the (visible+hidden) payoffs, increasing P increases the “risk bandwidth” of the channel. Therefore given a certain amount of total committed capital in a channel, we maximize the *efficiency* of P by permitting as much of this capital as possible to be added to P. I’m not pretending that P can be increased arbitrarily at no cost. I’m saying that *efficient* channel design takes advantage of *cheap* and *realistic* opportunities to increase P. If your user model for a specific situation (say, a commercial user with access to large amounts of capital on reasonable timescales) shows that they will be able to make large deposits d, then definitely you should take advantage of that capability to increase the “risk bandwidth” their channel can support, so that you can enter into requested protocol states if they attempt to do so, perhaps with an additional notice to the user at the point which shows the size of the deposit d which will be required when entering into the new domain.  Note however that changing d may, depending on your design, require an on-chain transaction, so this is a tradeoff against cost, delay, etc.  The space of channel designs is very large and very user model dependent, which is why a general framework like ours doesn’t want to have opinions about sticking to just one exact point in this tradeoff space.  But even aside from all of these tradeoffs, if a user has capital in a channel, then it doesn’t increase capital costs at all to be able to add that in to P, and doing so strictly increases the “risk bandwidth” of that channel.  I don’t see any positive argument for removing the ability to use this capital at an architectural level.

As a side note, in determining the *optimal* balance between in-channel and out-of-channel deposits for a given channel, note that out-of-channel deposits must be made at a point when the blockchain doesn’t know the most recent state of the channel, while *penalties* are applied at a point where the blockchain *does* know the most recent state of the channel. Thus it is easy to dynamically adjust penalties from the portion of the penalty that lies in the channel, while adjusting the deposit portion of the penalty requires either an on-chain transaction or a complicated system of continually-timing-out deposit settings which will increase availability requirements and force a go-to-chain by specific deadlines if one party is not available to renew for the next period. So broadly speaking it seems like in-channel penalties are better for casual users who don’t have a lot of access to extra capital and don’t want to have strict availability requirements, while more commercial users who expect to be available very consistently, have lots of access to extra capital, and have a need for higher amounts of risk bandwidth, can benefit from bumping up the deposit size to increase P. Either type of user will benefit from being able to apply extra capital within the channel towards P, however.

Backing off towards the big picture, I don’t think it’s unreasonable for a channel type targeting a specific set of users and design criteria, like Nitro, to just choose particular points in this huge tradeoff space.  My main point in raising all of this is just to show why so much flexibility is genuinely needed in a framework which would aim to be used for channels *in general*. The design space of channels is very wide, and techniques which are optimal for one kind of user are not optimal for another.  I can certainly see that being able to have “Nitro Channels” supported within Counterfactual allows for the particular use cases it addresses to be easily hardened, given the relative simplicity of the design. But since I really do see us as all working on the same team here, I think it’s an incredible amount of wasted effort for you to build out an *entirely separate stack* just to enable that, and to have the two stacks existing out there but only compatble in one way (Counterfactual users being able to use Nitro applications but Nitro users not being able to use Counterfactual applications, since Counterfactual can just write an adapter to support Nitro channels).  Wallets which integrate a state channels framework have to build out a lot of stuff that doesn’t depend on the specific design commitments you’re making:  blockchain monitoring components, secret storage methods for channel state, messaging layers, etc.  All of this effort could end being duplicated between us, or you could just build Nitro on top of Counterfactual, and let all *those* parts be built **once** in a shared open source project, while you focus on the parts of the stack which are actually uniquely Nitro.  That’s all I’m saying here.  Having the *capabilities* of Nitro is useful.  Being restricted to *only* the capabilities of Nitro is what I’m arguing is insufficient to cover the whole space of useful state channel designs.

---

**zakalwe** (2019-04-04):

Hi

(This is Jeremy BTW)

Just to throw in my quick (and totally penalisable) $0.02 - I’ve always gone with the mantra that P cannot be anything less than what a participant could gain by being malicious.  And, in general, that’s the entire value of the channel - if you are able to successfully close a channel with a stale state.  In fact, the only person that might be able to prove that P should be less is the other participant, who has no interest in doing so.

There are some edge-cases - that I considered and then discarded - where you can submit an incorrect, but signed, state transition from the counterparty.  In this case P could definitely be a lot less (and this might work as you can close a channel with penalty immediately); however we just treat these as failing to follow the protocol and ignore the attempted state transition, which turns out to be a lot cleaner in code.

I don’t know enough about how either of you implement multiple games in one channel, or virtual channels on top of “real” ones - but if you can limit the penalty to the value in either the individual game, or the virtual channel, doesn’t this make things easier?

---

**technocrypto** (2019-04-04):

I definitely think just discarding invalid state transitions is the right move. We’re not *trying* to penalise people very much for malfunctioning software.  We ideally want to apply as much penalty as possible to actual bad actors, and as little as possible to real users.

In terms of limiting the penalty to the value of some particular application or virtual/metachannel, to me penalties are about actors, not about applications.  The important thing is that the *party* who misbehaved is penalised.  The particular app they were using at the time is less important.  So any given protocol violation exists at one particular link in the graph, regardless of how long the metachannel is, and penalties need to be applied there.  As I tried to illustrate in my example above, this may or may not affect the metachannel itself, because if the protocol violator was merely an intermediary, the metachannel should be able to continue unaffected.

---

**tomclose** (2019-04-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> All of this effort could end being duplicated between us, or you could just build Nitro on top of Counterfactual, and let all those parts be built once in a shared open source project, while you focus on the parts of the stack which are actually uniquely Nitro. That’s all I’m saying here.

It seems like you might be unaware of the fact that Liam and I spent a considerable amount of time last year figuring out whether we could embed ForceMove into Counterfactual before we created Nitro. We eventually gave up, concluding that the update mechanics (in particular the round-robin nature of ForceMove where the state transitions with a single signature) made it too difficult to build a wallet to support both styles upfront.

This said, the key design goal of Nitro is simplicity. Our guiding design principle is to create something that’s easy to reason about and prove the correctness of.  Embedding it into Counterfactual at this point would lose that property.

Finally, I get that your reasons are noble for wanting everyone to build on top of Counterfactual. All the same, I feel like a should make the point that being the framework that everyone builds on top of is not a position that can be claimed - it must be earned. I just don’t see Counterfactual as having done that just yet.

Anyhow, I feel like this conversation has run its course for me. I should probably go and waste my efforts more effectively … ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)

---

**technocrypto** (2019-04-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/tomclose/48/3252_2.png) tomclose:

> It seems like you might be unaware of the fact that Liam and I spent a considerable amount of time last year figuring out whether we could embed ForceMove into Counterfactual before we created Nitro. We eventually gave up, concluding that the update mechanics (in particular the round-robin nature of ForceMove where the state transitions with a single signature) made it too difficult to build a wallet to support both styles upfront.

I’ll let Liam respond to this, but I don’t think he would characterize his conclusions the same way.

In terms of earning the role I fully agree this is needed. So far quite a lot of projects have made the call that we *have* earned that role, and I expect our continuing efforts to prove this. I would advise you to at least keep in mind some particular standard of what “earning that role” looks like, so that if we meet it you can pivot to reduce the duplication of effort.  Everyone has to make that call for themselves.  But given the fact that wallets need to do a huge amount of integration work to support frameworks, I really do think that tighter collaboration around an encompassing standard is a signficant benefit to everyone.

---

**liam** (2019-04-04):

Yeah I’d disagree with that; I don’t think we spent a considerable amount of time on it at all. The large majority of forces preventing an integration are and have always been social as far as I can tell. The Force Move API (validTransition) can be easily remapped to the CounterfactualApp API which we’ve discussed a bunch. However in our setup the PreFundSetup and other intermediary steps don’t need to be a part of the scheme at all so my recommendation was to skip that entirely. But, we never exhaustively wrote this stuff down.

This is probably a topic for a different thread though. However it still remains true that it Force Move with or without Nitro could exist on top of the technology stack we’ve written today and I’d love to see that happen ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**marckr** (2019-04-06):

Just chiming in, certainly not wasted. I have thought about state channels and counterfactual having read the paper around when it came out. Was studying MPC and VPSS at the time, going to have to reread the Counterfactual paper. Thanks for rounding out the conversation.


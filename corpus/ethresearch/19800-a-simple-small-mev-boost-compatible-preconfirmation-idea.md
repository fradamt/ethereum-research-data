---
source: ethresearch
topic_id: 19800
title: A simple, small, mev-boost compatible preconfirmation idea
author: FabrizioRomanoGenove
date: "2024-06-13"
category: Layer 2
tags: [mev, preconfirmations]
url: https://ethresear.ch/t/a-simple-small-mev-boost-compatible-preconfirmation-idea/19800
views: 5296
likes: 22
posts_count: 12
---

# A simple, small, mev-boost compatible preconfirmation idea

**Disclaimer**: This post will not contain any nice images, because I am artistically inept.

The reasons why I’m writing this are the following:

1. Preconfs are a very hot topic right now and many people are working on them;
2. As usual, some of the proposed solutions advocate for punching changes all the way into the main Ethereum protocol. I’m personally not a fan of this, since life is already full of oh my God, what have I done?™ moments and more drama™ is the least thing everyone probably needs.
3. MEV-boost is probably the only thing this community has really almost universally agreed upon since MEV has been a thing. So I’d very much try to preserve backwards-compatibility with MEV-boost and generalize on this than coming up with more innovative ways to balkanize our ecosystem even further.

## A primer on MEV-boost

This section exists just so that everyone is on the same page. Feel free to skip it or to insult me if you think I summarised things stupidly.

In layman terms, MEV-boost works like this:

1. Proposer polls the relayer(s) for their best blocks;
2. Relayer(s) send their best block headers to proposer;
3. Proposer picks the best block by comparing the block headers received and the block built in-house.
4. For an in-house block, proposer just signs and broadcasts. For a mev-boost block, proposer signs the header. Relay will broadcast the complete block revealing the payload.

This mechanism is nice because the only party that builders have to trust is relayer: Proposer cannot unbundle blocks and scam builders.

## The actual idea

The idea I have in mind works towards extending mev-boost by allowing for preconfs (and most likely for a lot of other stuff if one wants to). Notably, it does not change points 2,3,4 in the previous section, but only point 1.

Suppose proposer has a stash of preconfed txs on the side. The only thing the idea assumes is the following:

> By the time Proposer starts polling, it needs to have a finalized lists of preconfed txs to include.

The reason for this will become clear shortly. Having this list at hand, proposer sends a signed JSON object to the relayer when it polls, containing the preconfed txs. This object could look, for instance, like this:

```JSON
{
    proposer: address,
    slotNumber: int,
    gasUsed: int,
    blobsUsed: int.
    mergingPolicy: int,
    mustBeginWith: txBundle,
    mustContain: txBundle,
    mustOmit: txBundle,
    mustEndWith: txBundle,
    otherStuff: JSON,
    signature : signature
}
```

**This design is just an idea. It is by no means fixed yet and most likely can be improved upon both in conceptual and performance terms, so take it with a grain of salt.**

The fields `proposer` and `slotNumber` are obvious. The fields `mergingPolicy`, `mustBeginWith`, `mustContain`, `mustOmit`, `mustEndWith` can all be empty: They contain bundles of transactions that must (or must not) be included in the block. These fields are, effectively, the ones that proposer can use to signal relayer that 'hey, I need the block to respect these requirements, because of previous agreement I made with other parties."

How the proposer comes to define this json object is not our concern, and is outside of the scope of this idea. Just for the sake of clarity though, let’s consider some examples: For instance, [XGA](https://docs.xga.com), one of the projects `20[ ]` is contributing to, provides preconfs as tokenized bottom-of-block space. As such, XGA-style preconfs will produce objects where only `mustEndWith` is not empty.

The fields `gasUsed` and `blobsUsed` tell the relay how much gas and blobs the ‘preconf space’ already claimed. `otherStuff` exists to be able to extend this standard in the future without *more drama™*.

### Merging policies

The `mergingPolicy` fields instructs the relay about how to deal with all this information. This is fundamental because, in the end, the relay will still run a traditional mev-boost auction for the remaining blockspace. As soon as a block is built by more than one party there’s a risk that different parties may step up on each other’s toes. As such, `mergingPolicy` serves as a well-defined conflict resolution policy. If you need a mental reference, think about git conflicts and automated ways to solve them if you so like.

How to define merging policies is up for debate. The community could agree on a common repository where merging policies are defined, voted and agreed upon, and where merging algos are explicitly provided. So, for instance, one merging policy could be:

> If the payload coming from the builder contains a transaction that also appears in the preconf bundle, deal with it in the following way:

As said above, XGA sells BOB as preconfs, and leaves TOB open for traditional mev-boost auctions. As such, it has already defined and implemented a merging policy for its bottom of the block case, which will hopefully be open sourced soon.

### What does the relay do?

This is probably already kinda clear at this point, but to make it explicit: The relay receives this signed JSON object when the proposer polls. What should it do with it? First of all, it should make some of these fields public to the builders, such as `mergingPolicy`, `gasUsed`, `blobsUsed` and `mustOmit`. This way builders will know what they can build.

When a block from a builder is received, the relayer will **unbundle** the block and apply the merging policy to merge it with the preconfed txs. The **relay** will sign the block header, and send it to the proposer.

From the POV of a builder, everything is kinda the same. They create their block using the info provided by the relay (in the simplest case this just means using slightly less gas than limit), and submit it as their bid.

From this point on, everything works as in traditional MEV-boost.

## Analysis

Ok, so let’s run a rapid analysis of this thing.

### Pros

1. Changes to MEV-boost proper are really minimal. We just need to define an API that MEV-boost must listen to to build the polling payload, and redefine the polling logic.
2. Very little work from Proposer’s side. More work may be needed depending on the preconf system a given proposer wants to use, but then again this is out of the scope of this idea.
3. Very little work from builder’s side unless people go overly crazy with merging policies. I do not think this is necessarily a problem tho as an overly deranged merging policy would result in builders not submitting anything, and most likely in relayers not taking bets in the first place. So I’d bet that this could pretty much evolve as a ‘let the markets decide’ thing.
4. This idea is straightforwardly backwads-compatible with traditional MEV-boost: If the polling payload is empty, we collapse to a traditional MEV-boost auction with no other requisites.
5. This idea allows for gradual phasing out of MEV-boost if the community so decides. For instance, proposers may agree to produce bundles where usedGas is a very low parameter in the beginning (it won’t exceed 5M for XGA, for instance), meaning that the majority of blockspace would come from traditional building, with only a tiny part being preconfs or more generally ‘other stuff’. This parameter may then be increasingly crancked up or varied with time if the community so decides, effectively phasing out traditional block building in favor of ‘something else’. In this respect yes, I know I’m being vague here but when it comes to how this thing could be adopted I can only speculate.
6. This system can be extended in many ways, and it is flexible. Merging policies could be defined democratically, and the polling info could be extended effectively implementing something akin to PEPSI, for instance. Another possible extension/evolution can be using otherStuff to define Jito-style auctions. I mean, there’s really a plethora of ways to go from here.
7. The polling payload is signed by the proposer, and the block header is signed by the relayer. This keeps both parties in check as we accumulate evidence for slashing both. For instance:

Imagine I get some preconf guarantee from proposer and that I have evidence of this. Again how this happens is outside of the scope of this post, as this mechanism is agnostic wrt how preconfs are negotiated.
8. Now suppose furthermore than my preconfed tx does not land in the block.
9. I can use the chain of signed objects to challenge both relayer and proposer. If my tx wasn’t in the polling info signed by proposer, that’s proposer’s fault. On the other hand, if it was, but it wasn’t in the block, then it’s relayer’s fault. I think this is enough to build a slashing mechanism of sorts, which could for instance leverage some already available restaking solution.
10. Ethereum protocol doesn’t see any of this. So if it fucks up, we just call it a day and retire in good order without having caused the apocalypse: Relays will only accept empty payloads, proposers will only send empty payloads, and we’ll essentially revert to mev-boost without anyone having to downgrade their infra. I think this is the main selling point of this idea: The amount of ways to make stuff explode in mev-related infraland are countless, so this whole idea was built with a ‘it has to be failsafe’ idea in mind.

### Cons

1. Relayer must unbundle builder blocks to do the merging. I do not think this creates a huge trust issue as relayer can already do this as of now: In general, a relayer that scams builders is a relayer that won’t be used again, and will go out of business quickly.
2. Relayer must do computational work. This is probably the major pain point. This idea entails slightly more latency, as an incoming bid cannot be relayed instantly because mergingPolicy has to be applied. The computational penalty is furthermore heavily dependent on how deranged the merging policy is. As a silver lining, this computational work is provable as both the merging info and the resulting block are signed. The result is that we have provable evidence to remunerate a relay for its work if we want to, possibly solving a major pain point for relayers in traditional mev-boost.
3. Relayer is slashable if it screws up. Again, how this should be implemented is outside of the scope of this idea as this mechanism only accounts for the needed trail of evidence to implement slashing, but does not deal with the slashing per sé. Anyway, it is still worth reasoning on the possible consequences of this: If slashing policies are implemented, Relayers will most likely need to provide some collateral or implement some form of captive insurance. Again, this may signify more complexity on one hand but also opportunity on the other, as relayers may for instance decide to tokenize said collateral and develop mechanisms to make money out of these newly created financial instruments. As relayers are private enterprises I’ll leave these considerations to the interested parties.
4. Polling info must stay fixed. This is related to point 3 above and point 6 of the Pros subsection: If the polling info changes all the time, this means huge computational stress for the relayer, and it furthermore allows for malicious behavior from the proposer: For instance, a proposer could send two different polling payloads, and include a given preconfed tx only in one of them. How to resolve these inconsistencies is an open question. In my opinion, the wisest and simplest thing to do would be requiring the polling info to be fixed, meaning that if proposer signs conflicting payloads for the same slot this should be considered akin to equivocation, and thus a slashable offence.
 By the way, the consequence of this is that the idea proposed here necessarily excludes some preconf use cases. This is related to my comment here and I think it is unavoidable if we want to keep MEV-boost around. As the majority  of revenue from MEV comes precisely from the bids of very refined, high-time frame searchers, and as I am quite sure that validators don’t want to give this money up at least for now, ‘leaving these players be’ by ruling out such preconf use-cases is in my opinion the most practical option, and exactly the rationale motivating this idea.

## Closing remarks

That’s it. If the idea is interesting enough let me know, I’ll be happy to start a discussion around it.  The `20[ ]` team will also be around at EthCC if you want to discuss this in person.

## Replies

**terence** (2024-06-13):

How much latency do we think this add to the overall block release pipeline? The additional steps are:

- The relayer sends the requirement list to the builder.
- The builder sends the block to the relayer.
- The relayer verifies the block (not necessary if it’s an optimistic relayer).
- The relayer responds with the header back to the proposer.

Alternatively, we could assume the relayer can unbundle the block and fill in the requirement list itself without having to go through the builder.

---

**FabrizioRomanoGenove** (2024-06-13):

Yeah sorry, I wasn’t being clear. We need to absolutely assume that “the relayer can unbundle the block and fill in the requirement list itself without having to go through the builder.” if we don’t want builders to MEV the sh*t out of the preconfs, lol.

So to answer you more extensively:

### The relayer sends the requirement list to the builder.

This is only needed depending on the merging policy. For instance, for a ‘BOB, low priority’ kind of preconf there is very little we need to do. Basically the only thing builder has to know is what the merging policy is. For instance, to make everything simpler for builders XGA uses things such as:

> If builder submits a tx which also appears as a preconf tx in BOB, strip it out of BOB.

This means that for builders nothing really changes, they have priority over preconfed txs. In theory a competitive builder may fear that a competitor could use preconf to backrun their block, but given that preconfs have to be ready before the auction starts, I think this is a minimal concern. In general, we’re talking about two very different markets here.

As I said in the main post, the more deranged the merging policy is, the more complicated and terrible the mechanism becomes. Luckily for us the market is often very swift in punishing this kind of inefficiencies, and a very deranged policy would probably fall out of fashion rather quickly!

### The builder sends the block to the relayer.

Nothing new under the sun! Again, builders may need to do extra work if the merging policy requires it, which is why they have to be picked wisely.

### The relayer verifies the block (not necessary if it’s an optimistic relayer).

This is the pain point I was talking about before. Verifying the block is basically necessary, as the relayer is the party doing the merging. So it cannot blindly trust the builder. For instance, as hinted above, if the same tx (the literal same tx, same nonce, same everything) is submitted both by builder and as a preconf, the relayer will have to actively avoid that the tx shows up as duplicated in the block. This extra computational work is the main source of added latency. The more the merging policy is complicated, the worse it gets.

### The relayer responds with the header back to the proposer.

Nothing new under the sun here. The main difference is that the relayer signs it, accruing the chain of evidence that can be used to implement slashing.

---

**matt783** (2024-06-13):

If I understand correctly, the idea is to allocate a pre-confirmed portion of block space for proposers to include transactions.

Proposers can receive open market payments through MEV-boost relays, ensuring fairness by prioritizing these transactions top-of-block (TOB).

This approach increases metered block space for both the open market and preferred routes (pre-confirmation agents), balancing the negative externalities of frontrunning using the pre-confirmation feature.

From a proposer’s standpoint, they benefit from participating in a dual market scheme while maintaining the flexibility to optimize their proposer payments.

This enables optionality to the existing block space market without requiring any breaking changes.

---

**FabrizioRomanoGenove** (2024-06-13):

> If I understand correctly, the idea is to allocate a pre-confirmed portion of block space for proposers to include transactions.

Correct.

> Proposers can receive open market payments through MEV-boost relays, ensuring fairness by prioritizing these transactions top-of-block (TOB).

This depends. If you use the `mustBeginWith` field in the payload, and use a `mergingPolicy` which privileges preconfs over traditional MEV-boost, this may not be true anymore, as preconfs would get TOB. It really depends on how one runs the system but yes, I agree with you that what you wrote is probably the most obvious and wisest way to run it, lol.

> From a proposer’s standpoint, they benefit from participating in a dual market scheme while maintaining the flexibility to optimize their proposer payments.
> This enables optionality to the existing block space market without requiring any breaking changes.

Yes. This is the main point of the idea. Also, this results in very little changes to be implemented from the proposer’s POV. Ironically, Vitalik is giving a talk today called ‘Don’t overload the proposer’, I guess at least my timing was right ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=12)

---

**yooyobby** (2024-06-14):

as far as my understanding goes, builder will build a block as usual, relayer will unbundle the block and put the preconfed tx in it and send it to proposer, and proposer would propose the mev-boosted block.

thus almost no changes to other roles but for relayer?

forgive me for my lack of knowledge, but i have 2 rly basic questions

i) if preconfed txs conflict with already-in txs in the builder’s block, wouldn’t that harm the builder’s profitability?

ii) if the builder’s block arrives full, then wouldn’t there be times when relayer cannot add more txs to the block?

---

**dpl0a** (2024-06-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/yooyobby/48/15664_2.png) yooyobby:

> i) if preconfed txs conflict with already-in txs in the builder’s block, wouldn’t that harm the builder’s profitability?

See Fabrizio’s answer above:

![](https://ethresear.ch/user_avatar/ethresear.ch/fabrizioromanogenove/48/16390_2.png) FabrizioRomanoGenove:

> Basically the only thing builder has to know is what the merging policy is. For instance, to make everything simpler for builders XGA uses things such as:
>
>
>
> If builder submits a tx which also appears as a preconf tx in BOB, strip it out of BOB.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/yooyobby/48/15664_2.png) yooyobby:

> ii) if the builder’s block arrives full, then wouldn’t there be times when relayer cannot add more txs to the block?

There is a reserved space in the block for this. If a builder block arrives full there’s no problem since they’re occupying space that doesn’t intersect with the space occupied by the preconf bundles.

---

**FabrizioRomanoGenove** (2024-06-14):

Adding to [@dpl0a](/u/dpl0a) answer:

i) It really depends on the merging policy. Merging policy, as I stated in the original post, can be pretty much everything, including a mechanism that completely destroys the builder’s profit. For instance, it could be:

> Disregard builder transactions altogether.

Clearly, this is not wise nor profitable. In general, clever merging policies should ensure builders’ profitability, lest proposer sees its revenue declining.

ii) This is why I suggested to have `gasUsed` and `blobsUsed` in the polling objects. These items should be propagated by relayer to builders to instruct them about what to build. Again, I’d expect that the wise thing here is converging on some agreed-upon values. For instance, XGA at the moment caps `gasUsed` at 5M. In this case a builder submitting a block using more than 25M is automatically disqualified from the auction.

One important thing I probably did not stress enough in the main post is this: I’m assuming preconfs and MEV-boost building to be, at least for now, completely different markets. In my intuition, the main preconfs users are probably rollups, with sequencers that want to give inclusion guarantees ASAP. This is a completely separated usecase from competitive building (arbitrages etc.) so I wouldn’t expect much conflict from these two markets at the merging phase. I’m ready to be proved wrong though!

---

**CeciliaZ030** (2024-07-26):

Maybe we should not take mev-boost for granted and give up other principles to maximize mev-boost compatibility? By saying principles, I mean:

1. PBS is a temporary solution with trusted relays before ePBS → we should work towards a trustless set of infrastructure that levitates relay dependency.
2. PBS is designed with clean specialization & modularization → builder should build blocks, relays should just relay, validator should just validate. Having relays a merging significant body of the block implies block-building, plus validation, which seems counterintuitive to what it’s set out for.
3. Communication overhead should be minimized → also counterintuitive to me why are proposers throwing Txs to relays just to do something that they can do themselves. If MEV extraction in preconf Txs is not desired, proposers should just do a Arbitrum-style first-come-first-serve “merge policy”, as you described. Maybe this is adding communication & computation & infrastructure overhead for not much benefits?

---

**FabrizioRomanoGenove** (2024-07-26):

I agree with you, but it is important to understand where one comes from.

PBS is a two sided market: One needs to convince proposers AND builders AND basically whoever works in this ecosystem to onboard whatever alternative to MEV-boost is proposed. If bootstrapping a two-sided market is hard, changing the status quo in a two-sided market is exponentially harder. This is important because it places ideas in context and not in a vacuum, and this brings me to the next, most important point. Speaking of context, the reality of things is that:

1. Ethereum is a very political ecosystem atm. Having a good proposal is at least as important as to whom proposed the proposal, and the context of vested economic interests the proposal is going to touch.
2. MEV-boost is pretty much the only thing this space has agreed upon since MEV became a mainstream concept. Call it temporary as you want but it’s the only thing that has stood the test of time for years at the moment.

Point 1. here is really important. I consider myself a no-one. I am not part of the EF and most importantly I have no political power to really enforce any meaningful change on this ecosystem, and I do not like doing armchair-research. Proposing ‘radical’ alternatives to MEV-boost hence, no matter how good they look on paper, is not my job. Better said, proposing ‘radical’ alternatives to MEV-boost is literally not within my reach. The best I can do is proposing an alternative that, while not being perfect, has the biggest chance of making an impact by being adopted, and this  happens by avoiding any change that entails going to every single proposer and builder and asking them to change the client they run, especially given that MEV-boost has made them good money until now, whereas the ‘alternative’ is probably not battle-tested yet by the market.

Maybe someone else (a very influential individual, a huge project, or a huge VC) can try this move. I hope they do, and I wish them the best of luck. I for sure stand no chance, hence I work with what I have within reach: Making the least possible changes to MEV boost, in a way that ensures any proposer that they can roll-back to usual MEV-boost if they want to.

To conclude: I am sorry if my reply sounds overly pessimistic. I just take into account the reality I am immersed in while I think.

---

**CeciliaZ030** (2024-07-26):

Thanks for the reply!

![](https://ethresear.ch/user_avatar/ethresear.ch/fabrizioromanogenove/48/16390_2.png) FabrizioRomanoGenove:

> MEV-boost is pretty much the only thing this space has agreed upon since MEV became a mainstream concept.

True, mev-boost is the only thing that’s widely used but not enshrined which gives ppl space to make modifications. Lots of ideas for ePBS involve modifications of mev-boost anyways, and preconf should definitely take advantage of that as long as it’s backward compatible.

![](https://ethresear.ch/user_avatar/ethresear.ch/fabrizioromanogenove/48/16390_2.png) FabrizioRomanoGenove:

> Proposing ‘radical’ alternatives to MEV-boost hence, no matter how good they look on paper, is not my job. Better said, proposing ‘radical’ alternatives to MEV-boost is literally not within my reach.

Is a “radical” alternative to the existing centralized relay a better idea? Does it set us to the right path thinking long term?

---

**FabrizioRomanoGenove** (2024-07-26):

‘Radical’ is not with respect to good or bad. There are a billion ideas that are better than MEV boost. Radical is with respect to the possibility of actually bringing it to fruition.

We’re seeing this with preconfs, that challenge the status quo, are supported by a lot of influential people from the community, and yet they’re seeing a lot of hate and backlash by an equally influential part of the community? Will they win the market? I don’t know. What I know is that if I were the one to propose something like that it wouldn’t have gone anywhere, which is why I abstain from proposing stuff like that in the first place ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)


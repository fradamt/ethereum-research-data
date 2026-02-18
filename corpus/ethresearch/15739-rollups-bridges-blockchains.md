---
source: ethresearch
topic_id: 15739
title: Rollups = Bridges + Blockchains
author: bruno_f
date: "2023-05-28"
category: Layer 2
tags: []
url: https://ethresear.ch/t/rollups-bridges-blockchains/15739
views: 5750
likes: 9
posts_count: 6
---

# Rollups = Bridges + Blockchains

This started as an email to Jon Charbonneau after I read his great blog post “[Rollups Are L1s (& L2s) a.k.a. How Rollups Actually Actually Actually Work](https://dba.mirror.xyz/LYUb_Y2huJhNUw_z8ltqui2d6KY8Fc3t_cnSE9rDL_o)”. By the end it turned out to be waaay to long for an email and I thought it might be interesting for other people too. So I decided to instead post it here.

---

TLDR: My name is Bruno França, I’m the consensus lead at Matter Labs and I just wanted to share my *opinions* with you on what is and is not a rollup.

With that out of the way, I’ve been following your posts for a few months. Sometimes I don’t agree with your conclusions (for example, on shared sequencers), but your posts always have high-quality research and are quite unbiased so I normally learn something new. Your last post on what rollups are was no exception, the difference here is that it actually forced me to think for a while on what is a rollup and I think my ramblings might be useful for you.

To start, I’ll say on what I agree with you. I do agree that:

1. There are two different concepts here. I’ll call them the “rollup bridge” and the “rollup blockchain” temporarily.
2. That a rollup bridge and a rollup chain are separate and can “fork” away from each other.
3. That L1 and L2 are relative terms and depend on where a given asset was issued / is native to.

Let’s start with a thought experiment. Imagine we have two separate existing blockchains, let’s say Ethereum and Near. Can we build a trustless bi-directional bridge between them without modifying their protocols? Yes, we can! First, imagine we develop zk validity proofs for Near’s VM and consensus (all my examples are going to be about zk rollups, it’s just simpler for me). This clearly doesn’t require any change to Near’s protocol, we simply find a way of proving that a given block is a valid state transition inside a SNARK/STARK. Now, we also create on Ethereum a smart contract to verify those proofs and we’re done.

Now anyone can submit Near blocks (or state deltas) to Ethereum together with validity proofs and that smart contract will know the state of Near’s blockchain without any trust assumptions. And then it’s trivial to send messages from Near to Ethereum, you just need to submit Merkle proofs of Near’s state to the smart contract in Ethereum, that way you can prove any part of Near’s state. That’s the first realization. We are not sending coins or data from one blockchain to another blockchain, there’s no movement of anything, these are all still independent databases. We are just proving the state of one blockchain in another blockchain. Moving coins across blockchains is just a convenient abstraction.

But so far this is uni-directional, we only prove Near’s state on Ethereum. How do we do the reverse? Simple, we develop validity proofs for Ethereum, create a verifier contract on Near and send Ethereum blocks and validity proofs to Near. Now we can prove Ethereum’s state in Near. With two uni-directional trustless bridges we get a bi-directional one. This however ponders the question, why do we need two bridges? Rollups don’t have two bridges, Arbitrum and zkSync don’t have Ethereum bridges in their states, what’s happening here? Well, they have, but it’s a different type of bridge. We force zkSync full nodes to also be Ethereum full nodes, the same happens with Arbitrum full nodes. That’s the second realization, all rollups actually have two uni-directional bridges. It’s just that on the zkSync → Ethereum direction we use validity proofs + state deltas while on the Ethereum → zkSync direction we just use a full node bridge. Evidently a possible solution to connect Ethereum and Near would be to require each Ethereum full node to also be a Near full node and vice-versa. This would in fact achieve the same thing, it’s just a little dumb because it doesn’t scale well.

But now we have two bridges with validity proofs between Ethereum and Near. We can prove one blockchain state on the other blockchain and use that to “move assets” and “send messages”. What I want to point out is that we didn’t change any protocol, we didn’t require any extra functionality from Ethereum’s or Near’s full nodes, each blockchain might not even be aware of these bridges. A completely foreign third-party like Matter Labs or Coinbase could maintain (and eventually fail to maintain) these bridges. So, are Ethereum and Near now rollups? Is Near more secure now because its blocks are posted on Ethereum? Will either blockchain’s security decrease if the bridges stop working? I think that you would agree that no, nothing changed on either blockchain. It’s just that now there’s a smart contract on each blockchain that can access the state on the other blockchain. Note that these bridges are also independent, if one of them fails, the other is completely unaffected.

Now we can talk about different types bridges then. Patrick McCorry has a [brilliant post](https://stonecoldpat.substack.com/p/mental-models-for-l1-and-l2) on rollups being validating bridges. I can say that I’m generally on Patrick’s camp, but I think there’s actually more types of bridges:

- The first type is obviously “full node bridges”. These are simply when the full nodes of one blockchain are also full nodes of another blockchain. This is the highest level of security for a bridge, this is what a trustless bridge actually is. The bridge has no extra security assumptions. It is also completely unworkable at scale. In the Ethereum + Near thought experiment, if we require all full nodes to be full nodes of both blockchains, then there’s no point in having two different blockchains. It can make sense in one direction though, if the node requirements for one blockchain are much smaller than for the other blockchain. That’s exactly what happens in rollups like zkSync, Arbitrum, Optimism, etc.
- The second type are “validity bridges”. This is a bridge that uses zk proofs to prove the validity of a given state transition (i.e. zk rollups). We have extra trust assumptions related to the proof system used for those validity proofs.
- The third type are “optimistic bridges”. The type of bridge used in optimistic rollups. The extra trust assumptions here are related to game theory and to the existence of at least one honest full node of the optimistic rollup.

Both validity bridges and optimistic bridges aim to approximate the security of full node bridges without requiring the same level of resources. In effect, a validity or optimistic bridge pretty much acts like a full node of another blockchain, but it’s just a smart contract.

Then of course you have light-client bridges (like Near’s Rainbow bridge), multisig bridges and so on. Now we can actually use this model to classify different rollup projects. For example, zkSync Era is a centralized (i.e. single validator) blockchain with a full node bridge *from* Ethereum and a validity bridge *to* Ethereum. And that’s what most rollups today are: blockchains with a full node bridge from the base chain and a validity or optimistic bridge to that same base chain. Note that this creates a kind of hierarchy between the chains, Ethereum full nodes won’t become full nodes of whatever rollup decides to bridge to it, but the rollup full nodes are pretty much forced to also be Ethereum full nodes. So there is maybe some value in the L1 and L2 terminology, even though I agree that for a given asset L1 and L2 are relative (we probably need better naming for these concepts).

Finally note that the rollup blockchain doesn’t inherit the technical security of the parent chain. In other words, posting the data (and proofs) from some blockchain to Ethereum will not increase that blockchain’s security. *The usage of Ethereum’s data availability is solely for the benefit of the rollup bridge, not of the rollup blockchain.* That implies then that the rollup bridge includes the smart contract and the data availability on Ethereum, and that the rollup blockchain is, well, just a blockchain.

This model, as neat as it seems right now, doesn’t explain validiums and sovereign rollups. Are validiums bridges or blockchains? How is it different from validity bridges? How about sovereign rollups? They don’t even have bridges! Let’s start with sovereign rollups since they are simpler to analyze.

The way sovereign rollups are normally described is as a rollups without a bridge. They essentially use another blockchain’s data availability and consensus as their own and so inherit that blockchain’s security. They do so by posting all their data to a base chain and the sovereign rollup full nodes are just full nodes of the base chain that have extra rules to interpret that data.

So is this a rollup? No, it’s not. It might sound like a rollup at first, but a lot of other things also meet this definition. Things that we certainly don’t classify as rollups, for example, Ordinals in Bitcoin. All the data for the Ordinals blockchain is on the Bitcoin blockchain. And for you to be a full node of the Ordinals blockchain you just need a Bitcoin full node and to know the Ordinals rules. It also has exactly the same security as Bitcoin. The same can be said about many other protocols on top of Bitcoin like Omni, Counterparty, Mastercoin, etc. Are all these protocols sovereign rollups?

I could probably find more examples, but the main point is that a blockchain piggybacking on another blockchain’s consensus and/or data availability is nothing new. As far as I know there’s no common term for these constructions, so I’ll try the name “dependent blockchains”. The innovation with rollups was creating a way for two blockchains to communicate in a trust-minimized and efficient way. Sovereign rollups lack that and so shouldn’t be called rollups, they are simply dependent blockchains.

This now fits nicely into our overall model. Blockchains are independent if they have their own consensus and data availability, and dependent if they rely on another chain’s consensus or data availability. Separately, they might or not have bridges to and/or from another blockchain. A sovereign rollup then is just a dependent blockchain without any bridges *to* the base chain. But sovereign rollups, by definition, do have a full node bridge *from* the base chain, since full nodes of a dependent blockchain need to be full nodes of the base chain.

Finally, we get to validiums. Just like rollups, they are blockchains with a full node bridge *from* the base chain and *some* bridge *to* the base chain. That new type of bridge is basically a validity bridge where we don’t post the blockchain data (either inputs or state deltas) to the base chain, we only post the zk proofs. For lack of a better name let’s call them partial validity bridges. But how is this different from a normal rollup? To find that out we need to understand what happens when blockchains fail and bridges fork.

Let’s go back to our thought experiment on bridging Ethereum and Near. In this situation, what happens if the Near blockchain halts (let’s not worry about how that happens, just imagine that Near completely stopped producing blocks)? Evidently, the bridge from Near to Ethereum will stop being updated. If there are coins on that bridge, they are stuck until the Near chain resumes. Evidently, the assets on that bridge don’t seem to have the same security as the Ethereum blockchain. That goes against what is normally claimed about the security of rollups, so what’s happening here? Remember that both validity and optimistic bridges act similarly to full nodes, and full nodes can fork a blockchain. Most rollups have some “escape hatch” mechanism planned, which really is just an automated fork mechanism. In our example, if the Near blockchain fails, the bridge could change into a [based rollup](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016), allowing anyone to update the state of the bridge, as long as it comes accompanied by a validity proof. If the Near blockchain then comes back online, it would have a different state from the bridge, thus reinforcing the idea that the bridge has indeed forked away from Near. This bridge would effectively have the same security as Ethereum, but it is crucial that there is some forking mechanism planned into the bridge. Imagine other situation where both Ethereum and Near blockchain are working but only Coinbase is allowed to update the state of the bridge (because that’s how the bridge was designed). If Coinbase fails for some reason and there is no forking mechanism in the bridge, then the bridge will just halt and all the assets will become stuck, even though the Near blockchain is still live. By now it should be pretty clear that bridges and blockchains really are different entities and that the security of one doesn’t influence the security of the other.

Now we can easily see the difference between validity bridges and partial validity bridges (i.e. validiums). Validity bridges are always guaranteed to have the state data (which is of course necessary to create a fork) because they post all state updates to the base chain. Partial validity bridges might not have that state data, it instead requires a honest minority of the validators in the validium blockchain to guarantee the availability of that data.

To summarize this very long post, it is *blockchains and bridges all the way down*. There’s many different types of bridges, but the ones that are more interesting for the L2 space are: full node bridges, optimistic bridges, validity bridges and partial validity bridges. We can also classify blockchains into two different types, dependent or independent, depending if they use another blockchain’s consensus and data availability as their own. These are separate concepts though and we can pair any type of blockchain with pretty much any number and type of bridges.

## Replies

**cryptskii** (2023-06-10):

I’d be interested in having you look at my paper which involves a solution to having a validity rollup on bitcoin coin utilizing consensus not just data availability.Please let me know if this interests you. I’d like one or two experts to review it before I over share the information. Thank you

---

**JonCharbonneau** (2023-06-12):

Sorry missed this when it was first posted, this is a great post thank you! Was admittedly slightly afraid when I saw the title ![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12). A few responses below:

> Finally note that the rollup blockchain doesn’t inherit the technical security of the parent chain. In other words, posting the data (and proofs) from some blockchain to Ethereum will not increase that blockchain’s security. The usage of Ethereum’s data availability is solely for the benefit of the rollup bridge, not of the rollup blockchain. That implies then that the rollup bridge includes the smart contract and the data availability on Ethereum, and that the rollup blockchain is, well, just a blockchain.

Could you elaborate here? I don’t think I would agree with this if I’m understanding your argument correctly. As described in the post, a “sovereign” rollup (i.e., no bridge) can still inherit the technical security of its base layer, so it’s not only for the benefit of the bridge. Also as described in [this great thread](https://twitter.com/sreeramkannan/status/1632622108822962178?s=20) by [@sreeramkannan](/u/sreeramkannan).

> But sovereign rollups, by definition, do have a full node bridge from the base chain, since full nodes of a dependent blockchain need to be full nodes of the base chain.

I don’t believe this is true? You either need to embed a base layer full node within the rollup full node *or* have the ability to run a trust-minimized light client (eg, with DAS). If you were to launch a sovereign rollup on Ethereum today, you *would* then need to embed an Ethereum full node in the rollup full node. However, that’s due to current base layer implementation, not fundamental to sovereign rollups (and can change in the future for Ethereum).

> Most rollups have some “escape hatch” mechanism planned, which really is just an automated fork mechanism. In our example, if the Near blockchain fails, the bridge could change into a based rollup , allowing anyone to update the state of the bridge, as long as it comes accompanied by a validity proof

This is a very interesting area! Actually reminds me quite a bit of what Anatoly had [tweeted about recently as described here](https://twitter.com/aeyakovenko/status/1643838814564286465?s=20). Also an idea for a “trust-minimized” bridge between two chains without being a “rollup” necessarily, where the bridge could again fork away. Still need to think more about this/potential issues.

> Sometimes I don’t agree with your conclusions (for example, on shared sequencers)

Just curious what you disagree on, always fun to chat on ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)

This is a great post and really enjoyed reading it, thanks again for the thoughtful response!

---

**bruno_f** (2023-06-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/joncharbonneau/48/13786_2.png) JonCharbonneau:

> Was admittedly slightly afraid when I saw the title .

The title is a tad click-baity, I agree. ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/joncharbonneau/48/13786_2.png) JonCharbonneau:

> Could you elaborate here? I don’t think I would agree with this if I’m understanding your argument correctly. As described in the post, a “sovereign” rollup (i.e., no bridge) can still inherit the technical security of its base layer, so it’s not only for the benefit of the bridge. Also as described in this great thread by @sreeramkannan.

Sovereign rollups do indeed inherit the security of the base chain. In that paragraph I’m excluding them, and my point is that I don’t consider sovereign rollups to be rollups at all. Looking at all different constructions that are talked about, it seems like there are two independent properties: 1) having a trust-minimized bridge, 2) piggybacking/depending/co-opting the base chain’s consensus.

We can imagine a 2-by-2 table with these properties:

- Has a bridge + co-opts consensus: This would be Based Rollups, for example, and other constructions like it.
- Has a bridge + independent consensus: Basically every rollup that exists today, having a centralized server is basically a separate chain. Also in this category, rollups that plan to decentralize by implementing their own PoS chain. The example I gave of Ethereum and Near connecting through a trust minimized bridge would also fit in here.
- No bridge + co-opts consensus: Sovereign “rollups” fit in here.
- No bridge + independent consensus: These are simply two separate blockchains/L1s. Nothing special here.

For me, it seems weird to consider everything that isn’t separate L1s as rollups. Going back to the example I gave of connecting Ethereum and Near through trust-minimized bridges, if we consider that construction a rollup (and I think we should), then it’s somewhat jarring to also consider sovereign rollups as rollups.

![](https://ethresear.ch/user_avatar/ethresear.ch/joncharbonneau/48/13786_2.png) JonCharbonneau:

> I don’t believe this is true? You either need to embed a base layer full node within the rollup full node or have the ability to run a trust-minimized light client (eg, with DAS). If you were to launch a sovereign rollup on Ethereum today, you would then need to embed an Ethereum full node in the rollup full node. However, that’s due to current base layer implementation, not fundamental to sovereign rollups (and can change in the future for Ethereum).

That’s interesting actually, I haven’t thought of that. Although, if every rollup full node just has a light-client to the base chain, then they would need to be continually asking base chain full nodes for relevant transactions. Not very practical but probably works. But fair enough, it is another type of bridge then, light client bridge, and sovereign “rollups” could indeed work with it. With DAS and validity proofs it could be a very interesting light client bridge. ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/joncharbonneau/48/13786_2.png) JonCharbonneau:

> This is a very interesting area! Actually reminds me quite a bit of what Anatoly had tweeted about recently as described here. Also an idea for a “trust-minimized” bridge between two chains without being a “rollup” necessarily, where the bridge could again fork away. Still need to think more about this/potential issues.

What Anatoly describes is basically an “escape hatch” mechanism. It’s not that different from what most rollups are implementing currently. But I would say that if you have a trust-minimized bridge between two chains then it is a rollup.

![](https://ethresear.ch/user_avatar/ethresear.ch/joncharbonneau/48/13786_2.png) JonCharbonneau:

> Just curious what you disagree on, always fun to chat on

I’m not sure I want to derail this topic that much! ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12) It’s probably already going to be a long discussion as it is. But you can DM me if you like and I’ll be happy to share my opinions on shared sequencers too.

![](https://ethresear.ch/user_avatar/ethresear.ch/joncharbonneau/48/13786_2.png) JonCharbonneau:

> This is a great post and really enjoyed reading it, thanks again for the thoughtful response!

Thanks! I like reading your posts too, so it’s nice to be able to contribute back.

---

**JonCharbonneau** (2023-06-12):

> The title is a tad click-baity, I agree.

I’m not one to complain about click-baity titles here hahahah just funny it’s great

> Sovereign rollups do indeed inherit the security of the base chain. In that paragraph I’m excluding them, and my point is that I don’t consider sovereign rollups to be rollups at all. Looking at all different constructions that are talked about, it seems like there are two independent properties: 1) having a trust-minimized bridge, 2) piggybacking/depending/co-opting the base chain’s consensus.
> We can imagine a 2-by-2 table with these properties:
>
>
> Has a bridge + co-opts consensus: This would be Based Rollups, for example, and other constructions like it.
> Has a bridge + independent consensus: Basically every rollup that exists today, having a centralized server is basically a separate chain. Also in this category, rollups that plan to decentralize by implementing their own PoS chain. The example I gave of Ethereum and Near connecting through a trust minimized bridge would also fit in here.
> No bridge + co-opts consensus: Sovereign “rollups” fit in here.
> No bridge + independent consensus: These are simply two separate blockchains/L1s. Nothing special here.
>
>
> For me, it seems weird to consider everything that isn’t separate L1s as rollups. Going back to the example I gave of connecting Ethereum and Near through trust-minimized bridges, if we consider that construction a rollup (and I think we should), then it’s somewhat jarring to also consider sovereign rollups as rollups.

To clarify, I’m not considering everything that isn’t a separate L1 as a rollup. The way I used it was "Rollups are blockchains that post their blocks to another blockchain, and inherit the consensus and data availability (DA) of that blockchain.”

So the Near example here *wouldn’t* fit that description, although it would have a very interesting bridge in this case.

I would of course call current rollups with a bridge “rollups” (and would *still* consider them to be rollups even if they implement a PoS set prior to Ethereum consensus). I’d also consider the idea (obviously none are live) of sovereign rollups to be rollups (i.e., those without the bridge). Both constructs post their data to another chain (whether full data or state diffs, enough to reconstruct the full state), and they inherit its consensus and DA.

This works because I’d say that *all* rollups co-opt the base chain’s consensus, regardless of sequencer implementation. Even if you implement a centralized sequencer or rollup consensus, these are just an *additional* “pre-consensus” for temporary guarantees, then they eventually defer to the base layer’s consensus. E.g., even with a rollup validator set reaching consensus, this is of course only for pre-confirmations. They’re not finalized until the base layer has also reached consensus and accepted it.

So the base layer consensus is the final arbiter in either case, and of course these “pre-consensus” options for pre-confirmations are equally available to sovereign (i.e., no bridge) and classic smart contract rollups. Either can equally have a centralized sequencer, pre-consensus set, L1-sequenced (based), etc.

(Also open to any definitions hahah, just I think that’s how these would fit in here based on this description which seems helpful to me.)

> That’s interesting actually, I haven’t thought of that. Although, if every rollup full node just has a light-client to the base chain, then they would need to be continually asking base chain full nodes for relevant transactions. Not very practical but probably works. But fair enough, it is another type of bridge then, light client bridge, and sovereign “rollups” could indeed work with it. With DAS and validity proofs it could be a very interesting light client bridge.

Yea if you want the two-way bridge without a base layer full node, you’d also want L1 validity (or fault) proofs. Though you can also just not have the bridge (i.e., sovereign), in which case you don’t need to keep checking on relevant transactions, you just want to follow the tip of the chain and know that your data is available (and with DAS implemented, you’d know your data is available even if there’s a malicious majority base layer consensus/chain fork, etc.). So it’s not an option to launch a sovereign rollup on Ethereum today like this (as there are no minimized light clients/no DAS yet), in which case you’d definitely need the full node even if you didn’t care about the bridge.

> What Anatoly describes is basically an “escape hatch” mechanism. It’s not that different from what most rollups are implementing currently. But I would say that if you have a trust-minimized bridge between two chains then it is a rollup.

So I guess this is the core of it. Based on how I used the term “rollup”:

- “Sovereign rollups” would indeed be rollups
- The Near construct wouldn’t be

And based on your description:

- “Sovereign rollups” aren’t rollups, they’re some other term
- But this Near construct would be a rollup

So you’re using the rollup definition in a similar manner (possibly the same actually) as how I used “L1” and “L2” definitions. I.e., it’s primarily a description of the security relationship when operating between chains.

I had thought about this a while and ended up going with the description of “rollups” I used because this type of bridging-security relationship felt properly addressed by L1 and L2 already. So it seemed redundant to use rollups in this bridge-centric manner, leaving us without a term to describe the other important relationship (posting data to another chain to inherit its consensus and DA, bridge aside).

Though it seems reasonable to use the terms in the opposite manner, i.e.:

- If you use rollups as the “bridge-centric” description, as you use it
- Then it’s probably reasonable to use L1 and L2 to cover the relationship I’m describing with rollups (i.e., you could call sovereign rollups L2s instead, regardless of whether they bridge to the base layer)

I favored the direction I used them, because I think it’s helpful to think of “L1” and “L2” as relative terms, which you seemingly agree with: “That L1 and L2 are relative terms and depend on where a given asset was issued / is native to.”

> I’m not sure I want to derail this topic that much!  It’s probably already going to be a long discussion as it is. But you can DM me if you like and I’ll be happy to share my opinions on shared sequencers too.

Will do!

---

**markodayan** (2024-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/bruno_f/48/8809_2.png) bruno_f:

> The usage of Ethereum’s data availability is solely for the benefit of the rollup bridge, not of the rollup blockchain.

Had to come back to this to contest this. It is primarily for providing the info for rollup nodes to stream into a derivation pipeline to build the chain – this is the foundational rollup definition.

If the DA helps facilitate trust-minimized rollup->L1 messaging – rollup is extended from the foundational class to “classic” (cause its implementing a validating bridge with whatever enforcement mechanism used to prove integrity of execution to the L1)


---
source: magicians
topic_id: 2573
title: Experiments we should be running
author: lrettig
date: "2019-02-02"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/experiments-we-should-be-running/2573
views: 2401
likes: 18
posts_count: 20
---

# Experiments we should be running

I have a fear, which has been increasingly recently, that Ethereum is not innovating fast enough. As [@Ethernian](/u/ethernian) pointed out in [this thread](https://ethereum-magicians.org/t/thought-experiment-ethereum-has-failed-in-5-years-why-did-it-fail-how-we-can-prevent-it/2568), it’s critical that Ethereum continue to innovate rapidly as that is one of its core differentiators.

The fact that it’s taken 16 months from Byzantium to Constantinople (still not in production), despite the fact that Constantinople is relatively noncontroversial and doesn’t actually change very much, is one reason I feel this way. The fact that, according to the [best estimates](https://www.reddit.com/r/ethereum/comments/ajc9ip/ama_we_are_the_eth_20_research_team/), we won’t have a functional (from the perspective of most layer two developers) Eth2 until 2021 (phase 2) at the earliest, is another. (Note that this is not intended in any way as a criticism of Eth2 research. It’s a hard problem and, all things considered, the roadmap sounds reasonable to me. It’s more a question of how incremental our innovation should be–more on this in a moment.) Our inability to make decisions on controversial questions such as progpow is a third reason.

Some may have a vision for an Ethereum that’s more stable today, with few or no breaking changes. That’s not my vision. My vision is of an Ethereum that continues to innovate until we’ve achieved maturity along four dimensions, at which point the base layer should become stable, and innovation should occur at layer two and above, with two exceptions: fixing bugs/critical issues and public good issues which must be tackled at layer one. Those four dimensions are 1. scalability, 2. usability, 3. governance, and 4. adoption. In general I’m making the same case that [@vbuterin](/u/vbuterin) made [in this blog post](https://vitalik.ca/general/2018/08/26/layer_1.html).

To be clear, as we explored in depth in [EIP-1283 reentrancy bug](https://ethereum-magicians.org/t/remediations-for-eip-1283-reentrancy-bug/2434), we have a tacit social contract with smart contract developers today but it’s unclear what that contract is and what is considered invariant by both parties. Seeking to better understand that social contract and being more explicit about what should and should not be considered invariant would be a good start.

But I also feel strongly that, at this stage in Ethereum’s evolution, we must not shy away from innovation, even on the Eth1 chain. As I suggested elsewhere:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png)[The roadmap and dev-led vs. research-led projects](https://ethereum-magicians.org/t/the-roadmap-and-dev-led-vs-research-led-projects/2554/1)

> Eth1x should be considered the canonical roadmap until Eth2 has proven viable

The two workstreams should continue to collaborate closely to ensure that, as much as possible, innovation flowing into Eth1x can be used as-is for Eth2, and that the upgrade can be performed as smoothly as possible. But the key point is: **Eth1x innovation should not slow while we wait for Eth2.**

With all that being said, here’s a list of experiments that we should consider attempting in the near term:

- Changing the PoW algorithm (to, e.g., progpow)
- PoS on Eth1
- Various governance strategies, including dipping our toes into on-chain governance
- Funding core R&D in-protocol via fees, inflation, and/or “rent,” i.e., experimenting with different forms of taxation.
- Finding a sustainable storage model via e.g. storage “rent” or “maintenance fees”
- Different virtual machines, e.g., Ewasm
- The various scaling technologies I outlined here

(I could keep going, and I urge others to add to this list.)

We don’t know if any of these ideas will work, and many of them may in fact be terrible, but the point is, we will never know if we don’t experiment. To me, one of the things that makes Ethereum the best blockchain is its general-purpose nature and the fact that we’re not afraid to experiment. Of course, this must be balanced against the social contract and the need for stability.

We need to find ways to run more experiments. I suggested several ways we might attempt this:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png)[Thought experiment: Ethereum has failed in 5 years. Why did it fail? How we can prevent it?](https://ethereum-magicians.org/t/thought-experiment-ethereum-has-failed-in-5-years-why-did-it-fail-how-we-can-prevent-it/2568/3)

> An idea I’ve been toying around with, which is obviously not fully formed, is, can we somehow spin up more “Etherea” i.e. chains with some value today for experimentation? The xDai chain is a great example of this. They could be sidechains, Plasma chains, “hard spoon” chains, new chains (e.g.a “Litethereum” chain with a clean ledger, which pushes the envelope on experimentation and research, a bit like a Litecoin to Ethereum’s Bitcoin), or Polkadot parachains.

## Replies

**Ethernian** (2019-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> here’s a list of experiments that we should consider attempting in the near term:

- better N2N (node to node) secure messaging between heterogeneous subnets.
I feel, that it is even more important that moving crypto assets around, because will connect all the ethereum parts together into one network.
- we need better standards for non-updating data queries. Current access layer is a pain and creates a needs of supporting servers for dapps.

---

**Ethernian** (2019-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Our inability to make decisions on controversial questions such as progpow is a third reason.

Our inability to make a decision is a symptom. Our problems are deeper and still unknown. May be it is  missing roles and incentives, may be missing procedures. I don’t know.

I am a little bit concerned about ideas proposing (semi-) centralized governance over different CoreDev groups. They are expected to understand fully what are they doing. If they ready to delegate their decision power, it will just obscure their lack of understanding, arguments or clarity. It will create powerful, but wrong decisions.

I would make a survey and ask CoreDevs single question: why does it take so long from from upgrade to upgrade and ask for real-live examples. Most probably the “Why” question needs to be repeated recursively some times before we will find a root cause we can target.

I am sure results will be quite unexpected.

---

**fubuloubu** (2019-02-03):

Definitely agree on more innovation on Layer 1 in the short- to medium-term (e.g. 1x proposals). Competition is definitely here, and we need to be proactive. More of that needs to be coordinated in parallel.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Changing the PoW algorithm (to, e.g., progpow)

I really enjoyed [@AlexeyAkhunov](/u/alexeyakhunov)’s latest article on ProgPoW, and I in general agree with his assessments.  ([Here](https://link.medium.com/Mn11cF5y0T) for those who haven’t seen it yet)

We should look at security holistically, and not be scared by words like “ASIC”, instead asking the bigger questions like “What are the trends here?” and “How does this affect security?”

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> PoS on Eth1

Instead of ProgPoW, I really REALLY believe we should seek to integrate the PoS experiment into the main chain via the Hybrid approach in the medium-term. That is a core innovation I haven’t seen yet in another project. We already know that PoW works (and when it doesn’t) and we will soon have validation our particular approach to PoS will work. PoS is complimentary and can solve problems PoW can’t (namely finality). Why not combine the two to increase security?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Various governance strategies, including dipping our toes into on-chain governance

This is one of the core things I believe still separates us from other attempts like Polkadot, Tezos, etc. I do *not* believe explicit, on-chain governance is the way to go, at least as baked in to the protocol. We can perhaps begin to talk about using a “governance by DAOs” approach with voting and the whole nine in the long run, but I believe our social scalability is only in a middle point between tight social consensus in small groups, and a larger formalized structure. We can begin to self-organize in more efficient subgroups, and form a heirarchy of different perspectives on the proposals we have. This will increase effectiveness by reducing noise and coordination costs among core contributors to the system.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Funding core R&D in-protocol via fees, inflation, and/or “rent,” i.e., experimenting with different forms of taxation

Likely to be very controversial to the point of being a waste of time? Let’s see how experiments like Moloch work out, we already have some successes like Gitcoin grants and Aragon Nest that I think warrant deeper investment. I’m not sure taxation through inflation is a socially tenable position in our ecosystem. Let’s grow through collective action and shared prosperity from intelligently applied investments of what we already have.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Finding a sustainable storage model via e.g. storage “rent” or “maintenance fees”

I really disagree with core protocol fees, instead storage maintenance and pruning should correspond with an extra-protocol fee market or just more people running their own full nodes. We should look into sharded state/state pruning that removes requirements from full nodes to have an all-or-nothing approach to storage.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Different virtual machines, e.g., Ewasm

If this doesn’t happen in the medium-term for 1x, we should abandon it. Too much upgrade cost and time losses while the EVM tooling continues to grow. Time to act is now!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> The various scaling technologies I outlined here

A lot of great proposals for short- to medium-term improvements. Investing in small experiments with proof of concepts is a great use of resources.

---

**fubuloubu** (2019-02-03):

I also think the hybrid approach gives us a chance to gradually validate our approach to PoS in real-world terms. We can show that coordinating two chains together will work (PoW pulls data from PoS block attestations). We could allow access to the randomness generated by PoS and see how bias-able it is in more low-stakes scenarios like betting games (who will inevitably use this as an API). We need to start integrating the two together eventually, do it in a low-stakes way.

---

**lrettig** (2019-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> I really REALLY believe we should seek to integrate the PoS experiment into the main chain via the Hybrid approach in the medium-term.

This would not be easy but it would be a *fascinating* experiment, especially in parallel to Eth2. In a sense it’s sort of like a fall-back plan if Eth2 were to be delayed further or run into unforeseen obstacles.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> I do not believe explicit, on-chain governance is the way to go, at least as baked in to the protocol.

It’s not black or white, that’s the point I’m trying to make. For instance, the way miners vote to increase or decrease the block size today in-protocol. I think there are all sorts of other low-key experiments we could run here. I’m not suggesting that Ethereum become Tezos overnight, but if we don’t explore the tradeoff space we’ll never know how optimal it is today.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> I really disagree with core protocol fees, instead storage maintenance and pruning should correspond with an extra-protocol fee market or just more people running their own full nodes.

For the record, following on [@AlexeyAkhunov](/u/alexeyakhunov)’s latest work and the meetings at Stanford, we appear to be moving pretty rapidly in the direction of introducing in-protocol storage maintenance fees. I don’t think we’ll achieve sustainability without this. If you feel strongly otherwise, now would be a good time to voice that!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> If this doesn’t happen in the medium-term for 1x, we should abandon it. Too much upgrade cost and time losses while the EVM tooling continues to grow.

I disagree. Let’s not confuse VM with language and tooling, for one thing. Solidity continues to mature but it can be made to work with Ewasm or any other VM. And I don’t think the upgrade cost is a big deal, especially with new chains and shards. I think we should continue to explore new options and not be afraid to add new ones later or have multiple VMs.

Thanks for the great ideas and feedback!

---

**fubuloubu** (2019-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> I think we should continue to explore new options and not be afraid to add new ones later or have multiple VMs.

I broadly agree, but I really don’t think we should discount the shear amount of effort that has gone into the current tooling. Formalizing the K semantics for the EVM took a very long time, and WASM is more complicated than that. Not to say it’s impossible, but it is not to be underestimated how much momentum EVM has at this point.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> For the record, following on @AlexeyAkhunov’s latest work and the meetings at Stanford, we appear to be moving pretty rapidly in the direction of introducing in-protocol storage maintenance fees. I don’t think we’ll achieve sustainability without this. If you feel strongly otherwise, now would be a good time to voice that!

I’ve voiced this a few times, but it seems like most broadly disagree. I think it’s broadly better to create *space* for a fee market to exist than to try and shoehorn one into the protocol, hoping to get the economics close enough that it doesn’t all just crumble in practice. I also think that in giving that space (through a formalization of how data storage proofs work) we give the user *choice* of how they handle it: micro-payments for data access from full/archive nodes, store it themselves, build a dapp-specific storage structure (a la Graph Protocol) for both reads *and* writes, etc. Solid engineering here can help unlock the economics in a multitude of ways, being based on simpler assumptions of how it works technically.

I don’t think I have the time or energy to do more than voice my concerns here though. I just think there’s a better way down that path.

---

**fubuloubu** (2019-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> hoping to get the economics close enough that it doesn’t all just crumble in practice.

And remember, we can test engineering solutions on testnets, but we cannot *truly* test economics without real things at stake. From a risk standpoint, rent fees in the protocol is asking for a lot to go right.

---

**AlexeyAkhunov** (2019-02-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> lrettig:
>
>
>
> For the record, following on @AlexeyAkhunov’s latest work and the meetings at Stanford, we appear to be moving pretty rapidly in the direction of introducing in-protocol storage maintenance fees. I don’t think we’ll achieve sustainability without this. If you feel strongly otherwise, now would be a good time to voice that!

I’ve voiced this a few times, but it seems like most broadly disagree. I think it’s broadly better to create *space* for a fee market to exist than to try and shoehorn one into the protocol, hoping to get the economics close enough that it doesn’t all just crumble in practice. I also think that in giving that space (through a formalization of how data storage proofs work) we give the user *choice* of how they handle it: micro-payments for data access from full/archive nodes, store it themselves, build a dapp-specific storage structure (a la Graph Protocol) for both reads *and* writes, etc. Solid engineering here can help unlock the economics in a multitude of ways, being based on simpler assumptions of how it works technically.

Great to hear different kind voices! I just wanted to say that we are not “married” to the idea of introducing the State fees (formerly known as State rent) into the protocol. We are, however, researching the best way to do it if it has to be done. But apart from that, we are also actively working on producing the evidence of whether or not state size restrictions will be necessary, and on mitigations (and this will hopefully start coming through very soon) to see how far they can get us.

---

**lrettig** (2019-02-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> we can test engineering solutions on testnets, but we cannot truly test economics without real things at stake. From a risk standpoint, rent fees in the protocol is asking for a lot to go right.

This is exactly the reason we need to be running more experiments on alternate chains with value, as I argued above:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> An idea I’ve been toying around with, which is obviously not fully formed, is, can we somehow spin up more “Etherea” i.e. chains with some value today for experimentation? The xDai chain is a great example of this. They could be sidechains, Plasma chains, “hard spoon” chains, new chains (e.g.a “Litethereum” chain with a clean ledger, which pushes the envelope on experimentation and research, a bit like a Litecoin to Ethereum’s Bitcoin), or Polkadot parachains.

[@fredhr](/u/fredhr) called this “the thesis of Polkadot” which may be true, but from my perspective (and based on my limited understanding of Polkadot) it’s a bit less about scalability and app-specific chains and a bit more about experimentation, economic parameterization, and, ideally, a form of futarchy in which the market sorts things out.

---

**lrettig** (2019-02-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> I’ve voiced this a few times, but it seems like most broadly disagree. I think it’s broadly better to create space for a fee market to exist than to try and shoehorn one into the protocol, hoping to get the economics close enough that it doesn’t all just crumble in practice. I also think that in giving that space (through a formalization of how data storage proofs work) we give the user choice of how they handle it: micro-payments for data access from full/archive nodes, store it themselves, build a dapp-specific storage structure (a la Graph Protocol) for both reads and writes, etc. Solid engineering here can help unlock the economics in a multitude of ways, being based on simpler assumptions of how it works technically.

This is an interesting idea. It sort of strikes me as the difference between baking a single signing/verification algorithm into the protocol, as Ethereum has, versus the “account abstraction” idea that we’ve explored where each accountholder can choose how they want to secure their account (allowing them to e.g. choose a quantum-resistant algorithm now if they prefer).

I’ve yet to see a comprehensive proposal for how we’d accomplish “storage abstraction” in Ethereum, aside from the “pure stateless client” idea which, last I checked, was deemed unworkable due to issues with deleting accounts, reclaiming dead parts of the trie, etc.

---

**fubuloubu** (2019-02-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> issues with deleting accounts

What happens if you forget to pay your rent? Does your account get deleted permanently? If it’s not permanent, they’re basically the same thing in practice.

---

**Ethernian** (2019-02-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> If it’s not permanent, they’re basically the same thing in practice.

My understanding, it is not the same because it gets really deleted (space freed), but you can actually re-create it later providing the proof that the state is the same as it was deleted. It is your obligation to get the state from somewhere.

BTW, it needs incremental storage updates (for states bigger than blocklimit). But it is anyway useful for deploying bigger contracts too.

Pls, correct me if I am wrong.

---

**fubuloubu** (2019-02-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> it gets really deleted (space freed), but you can actually re-create it later providing the proof that the state is the same as it was deleted

If that’s the case… Then it is the same! Because it’s not permanent if I can restore it. That will create a secondary market for long-term storage of state, or clients will implement features to account for this (“cold storage” of storage), or both!

Full node operators can offer this as a service, and now their efforts are sustainable.

---

So now, figure out how to limit the growth of the state by choosing a particular depth, and then try and figure out the spamming problem (i.e. transaction gas costs get multiplied by a factor determined by the time since a transaction was last performed). That probably ends up looking something like state rent, but at least the UX is a little better in practice.

---

**lrettig** (2019-02-06):

In [Alexey’s latest proposal](https://ethereum-magicians.org/t/state-rent-proposal-version-2-rushed/2494), accounts and contracts are handled differently:

- accounts are totally removed - but can be recreated trivially by sending some ETH. Note that replay protection becomes an issue here.
- contracts are never totally removed - a “hash stub” remains which allows the contract to be recreated later if someone can rebuild the state.

We should probably move this conversation to a thread about that proposal!

---

**Ethernian** (2019-02-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Funding core R&D in-protocol via fees, inflation, and/or “rent,” i.e., experimenting with different forms of taxation.

**TL;DR** : I am against pure taxation/inflation/rent etc form of R&D funding. It should be mixed with investments per Quadratic Voting. I would suggest to create investable token for experimentation we are approaching with the rewards payout on merging into main ethereum trunk. Exact investment rules are to be invented  yet.

**Long Read:**

I am deeply convinced, that we need to revise economic and incentives basement of experiments we are approaching. We are all talking “we should do this and that” but there is no governance body in ethereum community. Who will implement our decisions?

As I stated in [2nd part of my post](https://ethereum-magicians.org/t/thought-experiment-ethereum-has-failed-in-5-years-why-did-it-fail-how-we-can-prevent-it/2568/2), current economic structure of grants or long term EF support does not create correct set of incentives long term. Redesign of the investment and economic structure could help.

In particular I would revise the the premise “don’t introduce a token in the core project”. IMHO, It was introduced to keep capital flow in the ETH and keep ecosystem as simple as possible. Nevertheless the an experimental core project should have own token as an investing vehicle to attract critical investors and merge it with ETH after project becomes part of the main ethereum. Exact rules are to be invented yet.

Community investors would invest into core projects if there is a reasonable investment scheme.

---

**lrettig** (2019-02-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> Community investors would invest into core projects if there is a reasonable investment scheme

But most core projects aren’t and never will be profitable, nor even have a business model - for instance, the teams implementing the eth2 spec.

---

**Ethernian** (2019-02-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> But most core projects aren’t and never will be profitable…

It is true, but I firmly believe there are other sources to create investor’s rewards. Not only from project’s profit. A successful project will increase ethereum evaluation after it become merged into

main trunk (otherwise it is just useless). It should be possible to create an investor’s reward from the part of the increased evaluation of the whole ethereum project.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> … nor even have a business model - for instance, the teams implementing the eth2 spec.

It could be important research: why teams are working on eth2? Who pays for it?

---

**cdetrio** (2019-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> fubuloubu:
>
>
> I’ve voiced this a few times, but it seems like most broadly disagree. I think it’s broadly better to create space for a fee market to exist than to try and shoehorn one into the protocol, hoping to get the economics close enough that it doesn’t all just crumble in practice. I also think that in giving that space (through a formalization of how data storage proofs work) we give the user choice of how they handle it: micro-payments for data access from full/archive nodes, store it themselves, build a dapp-specific storage structure (a la Graph Protocol) for both reads and writes, etc. Solid engineering here can help unlock the economics in a multitude of ways, being based on simpler assumptions of how it works technically.

This is an interesting idea. It sort of strikes me as the difference between baking a single signing/verification algorithm into the protocol, as Ethereum has, versus the “account abstraction” idea that we’ve explored where each accountholder can choose how they want to secure their account (allowing them to e.g. choose a quantum-resistant algorithm now if they prefer).

I’ve yet to see a comprehensive proposal for how we’d accomplish “storage abstraction” in Ethereum, aside from the “pure stateless client” idea which, last I checked, was deemed unworkable due to issues with deleting accounts, reclaiming dead parts of the trie, etc.

Stateless clients are basically what [@fubuloubu](/u/fubuloubu) was hinting at (“a formalization of how data storage proofs work”). Nobody has deemed stateless clients as unworkable, afaik. The issues to solve for stateless clients are mostly a question of optimizing the proof sizes, imo.

Issues with deleting hash stubs and resurrection after deletion are around rent mechanisms that propose to delete contract accounts from the state (as opposed to leaving the hash stub there). In the stateless paradigm nobody ever deletes accounts or parts of the trie, so these are not issues. (You could imagine a hybrid version of stateless that also has a deletion mechanism to constrain the size of the trie, with the benefit that everyone’s proof sizes would be slightly reduced in the very long run. But the benefit would be so marginal its probably not worth it.)

The primary critique against stateless is that it leaves unanswered the question of who will generate your proofs, if you don’t want to do it yourself. I make the same critique that rent only answers the question for people who can afford to pay the rent continually, and leaves it unanswered for everyone else (who might deploy contracts that are put to “sleep” and then later must be [awakened by providing a bunch of proof data](https://ethresear.ch/t/improving-the-ux-of-rent-with-a-sleeping-waking-mechanism/1480)).

---

Back to the topic of the thread, I don’t think anyone is against trying out experiments somewhere, whether on forks/chains with value or testnets. Its just that it takes a lot of work to run a worthwhile experiment (its called an experiment because its something new which is untried, usually because it hasn’t been built yet). Even if it might be easy to spin up new chains (using a PoA testnet or plasma/polkadot/etc, with value or without), it is hard to spin up new chains with new features. New features must be implemented by someone (not to mention tested for correctness by someone, to prevent experiments from going wrong like The DAO did), and that takes work. Its not that people are shying away from innovation. Its simply that there is too much work to do and not enough hours in a day, imo.

The points on governance strategies and funding core R&D are intertwined because regardless of whether contribution to the R&D fund is mandatory or voluntary, the overarching question is how the funds are governed. A couple of experiments which seem to be happening along these lines include DAOs (like suggested in the [State of Ethereum 2.0 report](https://ethereum-magicians.org/t/the-state-of-ethereum-2-0-report-from-kyokan-and-ameen-soleimani/2596/2)) and the [EthSignals ring](https://github.com/ethereum-magicians/scrolls/wiki/EthSignals-Ring) (or is it called [Tennagraph](https://ethsignals.gitbook.io/wiki/)?). Are these efforts minimally sufficient to learn from? Or is there a specific governance experiment the community ought to try in the near term, but which nobody is currently working towards?

Don’t forget that can also try to learn from the governance experiments happening outside of the ethereum ecosystem (“the wise man learns from the mistakes of others”).

On the key point “Eth1x innovation should not slow while we wait for Eth2”, the question is whether Eth1x will be integrated into Eth2 (as some 2.0 researchers hope), or whether Eth1x will persist as a separate chain indefinitely (as [some 2.0 researchers expect](https://www.reddit.com/r/ethereum/comments/ajc9ip/ama_we_are_the_eth_20_research_team/eeub32p)). There is no canonical roadmap of Eth1x or Eth2 that answers this question.

If Eth1x will be integrated, then (as you said) we as core devs should focus on innovations with benefits that will carry over to Eth2 and/or speed up integration. But if Eth1x persists as a separate chain indefinitely, then we can either innovate on Eth1x, or we slow down our contributions to Eth1x and instead choose to work on speeding up delivery of Eth2. Assuming there are only 24 hours in a day and that we are limited in number, this is a fundamental conflict.

---

**fubuloubu** (2019-02-08):

Fantastic response.

I think the consensus is that 1x should all be forwards compatible with what 2.0 is. The way I would phrase it, 1x solves issues we know about with the existing chain to make it stronger and sustainable in the long run. It mostly has to do with the data and execution layers, so I don’t think there’s a huge conflict with 2.0 designs IMO.

2.0 is focused on the consensus layer changes, and the overall architecture. This includes the execution layer (WASM vs. EVM, cross-shard sync, etc.) There are definitely some things that probably conflict, and you are right in that we should resolve them so that 1x work and 2.0 work is compatible.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cdetrio/48/482_2.png) cdetrio:

> If Eth1x will be integrated, then (as you said) we as core devs should focus on innovations with benefits that will carry over to Eth2 and/or speed up integration. But if Eth1x persists as a separate chain indefinitely, then we can either innovate on Eth1x, or we slow down our contributions to Eth1x and instead choose to work on speeding up delivery of Eth2. Assuming there are only 24 hours in a day and that we are limited in number, this is a fundamental conflict.

One final point about separate chains: I think this is a technicality, but I don’t believe it is advisible or even possible to have 1x become a part of 2.0 directly. I think it has to exist as a separate chain as 2.0 designs are being validated in practice. The 2.0 chain should be attractive enough for devs to port over their applications over time, according to their comfort level with the new tech. I don’t think we can avoid this, so we should embrace it and plan ahead for what that transition might look like.

Luckily, 1x will make that as minimal as possible, with the hardest part being the planning ahead of migrating over application state (which is hard).

---

Potentially an interesting approach is that state rent/stateless account updates in 1x could make it easier to “init” contracts on the new chain? It’ll sort of be like a restore, or maybe we make a special, one-way upgrade mechanism for accounts that directly maps the state root for an account.

![:man_shrugging:](https://ethereum-magicians.org/images/emoji/twitter/man_shrugging.png?v=12) Random ideas


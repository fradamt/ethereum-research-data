---
source: magicians
topic_id: 2568
title: "Thought experiment: Ethereum has failed in 5 years. Why did it fail? How we can prevent it?"
author: Ethernian
date: "2019-02-01"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/thought-experiment-ethereum-has-failed-in-5-years-why-did-it-fail-how-we-can-prevent-it/2568
views: 2407
likes: 14
posts_count: 19
---

# Thought experiment: Ethereum has failed in 5 years. Why did it fail? How we can prevent it?

Here is one of many discussion threads to the topic started by [@lrettig](/u/lrettig) I would discuss in details…

Please find my detailed explanations below…



      [twitter.com](https://twitter.com/lrettig/status/1090086660690374656)



    ![image](https://pbs.twimg.com/profile_images/1606906717446746112/ITAZkLjx_200x200.jpg)

####

[@lrettig](https://twitter.com/lrettig/status/1090086660690374656)

  Thought experiment: fast-forward five years and the Ethereum experiment has failed. Why did it fail? Extra points for providing plausible detail.

Hint: I don't think it would be because of the tech

  https://twitter.com/lrettig/status/1090086660690374656










https://twitter.com/Ethernian/status/1090523967130124288

https://twitter.com/lrettig/status/1090537375837708289

https://twitter.com/Ethernian/status/1090724617864560654

https://twitter.com/Ethernian/status/1090726225818124288

https://twitter.com/lrettig/status/1090936028733599744

## Replies

**Ethernian** (2019-02-02):

# 1. Detailed explanations: Experimental Shards

1. Ethereum creates much a lot of innovations in research. Nevertheless we have difficulties in adoption: very few of improvements get implemented and the process is very slow. More centralized competitors improve their products faster.
2. It is a real problem, because there is only two promises can win on the market:
“the most stable” or “the fastest innovation”. Everything in between, that does not held promise “immutable like bitcoin” and is not “the fastest innovator” will fail.
Ethereum has promised to be innovative, thats why it MUST be the fastest innovator among of his kind to survive.
3. Usually people suggest to introduce Ethereum-wide (semi-centralized?) governance in the hope to make decision making faster. The downside will be the greatly decreased inclusivity and the lowed decisions quality because centralized actor get biased much easier. Lack of inclusivity and biased centralized governance will force innovators to split off from Ethereum and continue as separate projects.
Ethereum will speed up first but then break apart.
4. I think, the lack of governance is not the reason why we can not make decisions fast enough.
The problem is: decisions to be made are too complex for big amount of decision makers. Someone can make one complex decision, many people can agree on simple decision, but making complex decision by many parties will fail.
5. Our EIP process now: all CoreDevs must agree on EIP implementation in CoreDev calls. Looks like usual EIP decision is not simple enough and there are too many decision makers.
Solution: Let’s allow EIP implementation by few ethereum clients first and let others to join the implementation later. Few clients (or even only one) will agree on EIP faster. If the EIP gets implemented by some clients, it will be easier to adopt it for others.
6. Implementation idea was proposed by @vbuterin  in Cancun: shards with different state of “maturity”. An “experimental” shard may implement “new experimental features” supported by only one or few ethereum clients. If it works well, other implementations will follow and the EIP gets “matured”.
7. The idea of “experimental shards” or “experimental sidechains” raises a new interesting question: what is ethereum? What sidechain or shard is still ethereum what is a new separate project? Is it an ETH coin? is it technology? Is it consensus mechanism? Which invariants are ethereum-wide?
Is Tendermint or Quorum an ethereum “sidechain”?
Anyway the more ethereum is able to “unite” different sub-networks, the more strong it will be. It will be great if anyone could start his own “ethereum clone” and still stay in ethereum network whatever it will be.

## 2. Detailed explanations: Core Projects funding: EF vs Community.

1. Inclusiveness boosts competition of implementations and ideas. Nevertheless some Core Projects were preselected “in advance” in early ages and promoted as part of Ethereum regardless if they will succeed or not. Swarm and Whisper are good examples.
2. The “early pre-selection” of the project creates risks:

it creates incentives to prefer EF as an employer over project’s future users.
3. lower incentives for project to deliver, more incentives to become endless story.
4. project can’t be replaced or abandoned easily because it will mean “Ethereum failure”.
5. potential competitors are get “officially pre-excluded” from Ethereum Core Tect because of “officially pre-selected” one. Think about IPFS, PSS, Filecoin as competitors of Swarm and Whisper.
6. Al in all: We should check whether any “early pre-selected” Core projects are retarding the Ethereum project in general. This “pre-selection” of particular projects may had valid reasons three years ago, but now we should re-think their special status. It doesn’t means we (or EF) should stop them or cut off grants, but it means their competitors should become the same chance to become part of Ethereum Core.
7. How some projects became “pre-selected” by EF? I think they were not. It is just a public perception of the long-term mutual commitment of the EF to fund the project and of the project team to work on it. “Funded by EF” is a strong endorsement, which becomes “pre-selection” over the years with all negative consequences mentioned above.
8. What can we do? I would prefer to see Core Projects funded by community in some kind of honest ICO or may be by special purpose Prediction Market. It will create enough pressure on projects to perform and it will create incentives to shareholder to review critically what the projects are doing. ICO craze has shown how strong public funding can be. But we have unsolved challenge there:
9. Challenge: It is officially discouraged for Core and Infrastructure Ethereum projects to create own utility coin if it is possible to operate with ETH. If there is no utility coin, what is the investment vehicle and where are rewards for successful investors are coming from?
10. Solution idea: if some meaningful Core project gets merged into ethereum main, it will raise ethereum evaluation. This is where investor rewards may come from. The exact mechanism need to be developed yet.
11. If we succeed to create a mechanism for market evaluation of ethereum core projects, we will speed up ethereum, IMHO.

---

**lrettig** (2019-02-02):

Thanks for bringing this up. This (the pace of change and innovation) is one of the very most important topics in Ethereum right now. I love the idea of “heterogeneous shards” and I’ve been advocating for this since I first heard about sharding. I remain strongly in favor of this, but agree that it raises some very interesting questions. Here are a few, off the top of my head:

- Is any of this possible with Eth1 or must we wait until Eth2? An idea I’ve been toying around with, which is obviously not fully formed, is, can we somehow spin up more “Etherea” i.e. chains with some value today for experimentation? The xDai chain is a great example of this. They could be sidechains, Plasma chains, “hard spoon” chains, new chains (e.g.a “Litethereum” chain with a clean ledger, which pushes the envelope on experimentation and research, a bit like a Litecoin to Ethereum’s Bitcoin), or Polkadot parachains.
- What is the minimum degree of consensus needed to achieve this or similar experimentation? Does it require a hard fork? How much can be done without a hard fork? Setting up a bridge a la xDai, for instance, does not require a fork.
- Most importantly, seconding the question you asked, it begs the question, “What is Ethereum?” The canonical “Eth2” roadmap as it stands is for “many homogenous shards.” How much can be changed without breaking protocol-level homogeneity? The shards will, for instance, potentially have differing fee markets. Could they have different governance policies? Different EIPs as you suggest? It sounds more and more like Polkadot, with a set of heterogeneous “shard” chains.

---

**Ethernian** (2019-02-02):

Added [Detailed explanations: Core Projects funding: EF vs Community](https://ethereum-magicians.org/t/thought-experiment-ethereum-has-failed-in-5-years-why-did-it-fail-how-we-can-prevent-it/2568/2)

---

**Ethernian** (2019-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> An idea I’ve been toying around with, which is obviously not fully formed, is, can we somehow spin up more “Etherea” i.e. chains with some value today for experimentation?

The challenge here is the economy and business incentives.

There is a reason for developers of some particular client to implement EIPs unilaterally: *they* get paid by *their* customers running private chains based on *their* client. It is a B2B business.

But what is the reason for *two* different clients to implement some EIP and run a *private* chain together? I don’t see any. If the customer does not demand two different clients to support some EIP in *his private* chain (and I think no one customer will do it), then nobody will push developers of other clients to implement this EIP. Because nobody will give up *his own* USP (unique selling preposition) and share *his* customers. It means private “experimental” side chains creates no incentives to be adopted by many clients, even one by one.

Public chain is another business: For an ethereum client it is a public show case for its reliability. This public show case needs millions of users in billions of wealth stored in it, in order to create a strong evidence of reliability.

Even if it technically possible, a public “experimental” shard or side chains need strong incentives for client developers to step in. It means it should be connected enough to the public stable main chain in order to create the same strong evidence of battle-tested reliability as the main chain. In other words, it should be well connected to main ethereum in order to be part of it.

This premise defines minimum requirements for the side-chain (or shard). For example:

1. It should be possible to exchange secure messages between an experimental shard and the stable shard.
2. It should be possible to send and receive ETHs between an experimental shard and the stable shard.
3. … may be more?

I would ask your technical questions in [ethresear.ch](http://ethresear.ch).

---

**Ethernian** (2019-02-04):

[@lrettig](/u/lrettig),

I am collecting few topics for Ethereum Magicians Council in Paris.

It would be great to have a discussion “Why we are too slow in adopting innovations we are creating”?

This should be “5 Whys” Retrospective.

I need few supporters to list this topic in Agenda. Would you appreciate it?

Guys, please ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=9) to signal your support.

---

**Ethernian** (2019-02-05):

Submitted the topic to agenda.

[@lrettig](/u/lrettig),

I feel we’ll do well to invite some CoreDevs and other implementors into discussion.

---

**lrettig** (2019-02-06):

I hope we get more participation from core devs and researchers than we did in Prague

---

**Ethernian** (2019-02-10):

I have listed the [Topic “5 Whys" retrospective” in the Council’s Agenda](https://hackmd.io/DaJhrasLQteUk3IwX5bQAg?view#17-%E2%80%9C5-Whys-retrospective-Why-we-are-too-slow-in-adopting-innovations-we-are-creating%E2%80%9D)

please add yourself to participant’s list.

---

**gcolvin** (2019-02-11):

[@Ethernian](/u/ethernian)  I’m one core dev who plans to be there.  I’ve got personal concerns as Brooke and I seek funding for our plans to develop a formally verified EVM 1.5 VM.  And I’ve become concerned for Ethereum that the Foundation is the primary source of funding, and one that cannot process a grant application in a reasonable, promised amount of time, or make technical decisions in an open process.  But it’s hard to fund work outside of the Foundation, as it’s difficult to make any profit off Layer 1 work.  But it’s also difficult to do sustained R&D while relying on short-term grants, contracts, and personal savings for sustenance.  And it takes sustained R&D to maintain steady innovation.

Part of the problem seems to be the intention and belief that everything Ethereum 1.0 is going to be completely replaced “very soon”.  So why invest resources in the old VM and old PoW chain?  I was telling Casey just a few hours ago that–after 44 years of programming, 37 years in the industry, and 7 years on a world-class VM team–this goes against so much of what I’ve learned about the importance of backwards compatibility, iterative development, integrated R&D, and more that I sometimes want to pull my hair out.  Instead I’m just abrasive on the Gitter channels.

So in my opinion Ethereum failing in five years isn’t a thought experiment.  It’s a reality if we don’t prevent it.

---

**boris** (2019-02-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> I hope we get more participation from core devs and researchers than we did in Prague

Unlikely unless we very specifically reach out, invite people, and plan what would be discussed.

I’d love to run ETH1x + Istanbul planning sessions, either directly at EthMagicians or at a dedicated time post ETHCC – I’ve been keeping March 8th & 9th open. For now, have added myself as facilitator for EIPs & Standards so we can perhaps push that along a bit.

Alexey, who is really leading the charge on state management, won’t be in Paris.

Perhaps we should dedicate time for a longer EthRoadmap session again, maybe even within ETHCC? Talking both ETH1x and ETH2 would be useful, in context. Alexey’s state management talks 27 months, which seems like a length of time we should dig into. [@lrettig](/u/lrettig) if you’re going to be in Paris, would you volunteer to facilitate another roadmap session, fish bowl style?

I’m also turning my attention to when we can next reasonably get everyone together ahead of various Istanbul roadmap deadlines – mid April.

---

**lrettig** (2019-02-11):

Happy to spearhead, schedule permitting - I intend to be at the council of Paris and all of EthCC but may not be able to stick around after EthCC.

---

**boris** (2019-02-11):

Great. I was going to email [@jdetychey](/u/jdetychey) tomorrow and ask him if he wants EthRoadmap inside ETHCC or if we should make room for it at council. Once we nail that down, we can start inviting.

I’m thinking making it part of Council means that we have a bit more flexibility and that it’s a separate audience that makes the choice to get involved in ecosystem stuff. What do you think [@lrettig](/u/lrettig)?

---

**fulldecent** (2019-02-11):

I think this is a realistic view of the issues, good to hear the candor.

One solution is to have two entirely competing projects, a 1.0 team and a 2.0 team and start actively funding them as separate projects. Might as well, because when the fork happens “any day now” we can be confident that some interests will work to keep 1.0 running. Even if Nvidia sponsors it.

I have worked through, and won, research proposals with NASA, the US Army, and other US DoD agencies (“SBIR” program). I’ve also been in the running for a DARPA contract. Their process is long, but it is clear. And it runs fairly and exactly as you expect. You /can/ do this in an open organization but it requires strong leadership. If such a leader is here and you want to hear my experiences with large research grant processes, you’re welcome to call.

---

**gcolvin** (2019-02-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> One solution is to have two entirely competing projects, a 1.0 team and a 2.0 team and start actively funding them as separate projects.

I actually think that having separate organizations in the first place was a mistake, both for the developers and the technology.

For the 2.0 developers it seems to have turned into a university as much as a startup.  That may be unfair, tbut delivery has slipped a year or more every year I’ve been here. I do think they have gotten better at R&D, as they work with client teams to keep them up to date, and plan to more realistic schedules.

And technologically the beacon chain spec still depends on there being a mainchain. There is no design yet known that does without one, so the mainchain will need to keep running on PoW indefinitely. (Not even some ASIC makers seem to know this.)  And without backwards compatibility it is just another alternative blockchain hanging off of the Ethereum mainchain that happens to have rights to that trademark.  If somebody else provides a scalable EVM-compatible solution on a tighter schedule the trademark might not matter, and that might even be a good thing for the community.

---

**gcolvin** (2019-02-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> I have worked through, and won, research proposals with …

I worked through and lost at the SBIR process once.  The professor helping me with the grant warned me, “*Never* count on grants for your basic sustenance.”  Still, I’d love to talk to you about it.

---

**fulldecent** (2019-02-11):

Oh really, cool. Great, please drop me a line at [entriken@phor.net](mailto:entriken@phor.net) I’m on Philadelphia time zone, let’s find a time to talk.

---

**lrettig** (2019-02-11):

I can see benefits to either. No strong preference here. There was a “workshop” format at EthCC last year that was conducive to this sort of dialog.

---

**gcolvin** (2019-02-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> Solution: Let’s allow EIP implementation by few ethereum clients first and let others to join the implementation later. Few clients (or even only one) will agree on EIP faster. If the EIP gets implemented by some clients, it will be easier to adopt it for others.

EIP-1 already encourages at least one implementation.  But getting other clients to implement an EIP that hasn’t been accepted can be a big ask.


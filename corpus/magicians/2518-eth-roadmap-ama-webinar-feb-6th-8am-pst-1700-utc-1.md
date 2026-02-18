---
source: magicians
topic_id: 2518
title: ETH Roadmap AMA - Webinar Feb 6th, 8AM PST / 1700 UTC+1
author: boris
date: "2019-01-24"
category: Working Groups > Ethereum 1.x Ring
tags: [eth1x, storage-rent, community-call, ethcatherders, ama]
url: https://ethereum-magicians.org/t/eth-roadmap-ama-webinar-feb-6th-8am-pst-1700-utc-1/2518
views: 4838
likes: 19
posts_count: 12
---

# ETH Roadmap AMA - Webinar Feb 6th, 8AM PST / 1700 UTC+1

I reached out to [@AlexeyAkhunov](/u/alexeyakhunov) to assist him in hosting an **ETH 1.x / ETH Roadmap AMA** session. The CoreDevs meetup is coming up this weekend in Stanford, so we figured a little while after that event would be a good time to collect notes, share them, and then answer questions / get feedback from the community.

Zoom link: https://zoom.us/j/767339240

Some of the topics include:

- Ethereum 1x vision and objectives
- State rent and other methods of managing the state in Ethereum
- eWASM on Ethereum 1.0
- Making Ethereum clients small by pruning history, block and events

See the HackMD file for presenters and topics, and to add any questions you have https://hackmd.io/MnyKo1unT5Wb52tpDTi4rA

Please register on Zoom to take part in the webinar https://zoom.us/meeting/register/4b0c73835fdc47b0dc2040ba88984b7b

Depending on volume of attendees and questions, it may be helpful to run a Reddit thread on questions in [/r/ethereum](https://www.reddit.com/r/ethereum) – I’m not good at Reddit, so perhaps someone could volunteer to help out with this if it’s a good idea.

---

Note: Zoom registration is not required, but it’s a quick easy way to get a reminder / updates about the event. We’ll be sharing the public Zoom link shortly before the event.

## Replies

**boris** (2019-02-06):

[![alexey-potential-timeline-hardforks](https://ethereum-magicians.org/uploads/default/optimized/2X/8/81b915fc5315a8ae19c3ff9e4c91d0b2e470e174_2_690x381.jpeg)alexey-potential-timeline-hardforks1820×1005 326 KB](https://ethereum-magicians.org/uploads/default/81b915fc5315a8ae19c3ff9e4c91d0b2e470e174)

Thank you to [@AlexeyAkhunov](/u/alexeyakhunov) [@holiman](/u/holiman) Paul [@axic](/u/axic) [@lrettig](/u/lrettig) for answering questions / providing an overview. From my point of view, incredibly valuable and very helpful.

Thank you to [@timbeiko](/u/timbeiko) for early note taking and everyone for their participation and listening.

The notes are in the same [HackMD link](https://hackmd.io/MnyKo1unT5Wb52tpDTi4rA?both), but I have pasted them below to keep all content together.

The two action items I’ve pulled up top here, plus added (3).

### (1) ETH1x Alternate Chain

Use Cosmos and/or Polkadot for zone / parachain that has solved problem around bi-directional transfers. dapps can deploy and be sure that the alternate chain and features will remain, and helps test things that will be valuable on main-net Ethereum.

- Boris (will post thread on EthMagicians)

### (2) Alexey HF Planning Diagrams

Get these posted as Google Slides for re-use / adoption by others.

Excellent format for communicating multi-hard fork meta features as well as point features. Suggest that this become a strongly suggested part of any larger proposals.

### (3) Tracking Roadmap Discussions

I ([@boris](/u/boris)) have been updating / maintaining the [Roadmap page on the Ethereum wiki](https://en.ethereum.wiki/roadmap) as a useful persistent single URL to put information. It is world-editable, likely something for [ethcatherders](/tag/ethcatherders)  to potentially make use of,

cc [@lrettig](/u/lrettig) [@5chdn](/u/5chdn)

---

## Video

https://images.spade.builders/video/2019-02-06-eth1x-roadmap-ama.mp4

## Questions

### How much will Peter’s EEP work inform process?

[EEP-5: Ethereum Hardfork Process · Issue #5 · karalabe/eee · GitHub](https://github.com/karalabe/eee/issues/5), Afri’s comments [Ethereum Core Devs Meeting 52 Agenda · Issue #66 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/66#issuecomment-450840440)

Alexey: schedule every 9 months. Already working within this framework.

Goal of Stanford was changes for each group by May.

Changes will go in October

### Which EIPs are under consideration for Istanbul?

Alexy: don’t really know, not proposed as part of process yet.

See https://en.ethereum.wiki/roadmap/istanbul

EIP 1679 tracks this [EIP-1679: Hardfork Meta: Istanbul](https://eips.ethereum.org/EIPS/eip-1679)

### Are there any 1.x features that may be considered as EIPs for Istabul? If so, which ones?

Alexey: 2 working groups changes will be proposed

- State Fees

Seems like we will propose replay protection and accounting of the account states.

eWASM

- Overarching vision: introduce complete eWASM feature set in Ethereum. If we can do it in 1.0, great! If not, it may happen in 2.0.
- In past couple months, idea of introducing precompiles (subset of full eWASM) came up. Challenges for precompiles: need to implement in every client, and need benchmark. We can assume there will be more and more clients, which complicates the process. Ewasm helps in reducing that to a single implementation.

Note: for PegaSys, Java makes precompiles harder than other languages.

Need to look at engines that are capable of executing eWASM without a lot of loss compared to native execution.
Don’t have all the answers for pre-compiles or other options of introducing Ewasm, but have some answers that we plan to communicate.
May & October deadlines put stress on what can be achieved. A lot can be specified by May, but it would be challenging to have everything implementing in each of the clients by October.

Will hear from eWASM later too

Boris: anyone can propose EIPs. Needs to follow CoreDev / EIP process. See EIP-1679 and roadmap link above to track. ETH Cat Herders may be helpful in surfacing this more.

### Are there any ways to test 1.x proposals in a production environment without a hard fork to the main chain? Could we have a “state rent testnet”, for example? If so, is the development effort worth it?

Alexey:

New chain? bi-directional Ether needs to be figured out.

Research problem since Bitcoin introduced sidechains

Might be able to do it with Polkadot or Cosmos, ETH1x zone? Parachain? Try and organize bi-directional Ether.

Testnet as early as possible

My question (Tim)

Way to get more data, not just theoretical. This is controversial vs other things. HOw do we get “Real” data on this?

Alexey:

Ethermint is zones in Cosmos

These other projects may work better than sidechains, because they have infrastructure. Been working on bi-directional transfers. Quite some time. Some things will hit mainnet that is prep work, that won’t affect anything.

Martin: will have testnets, how long is the time? For developers to try. Lot of steps before we get to final, flip the switch

Boris: [Question, missed the first part]… Afri suggestion: could a group run a “chain” that has incentives built in, that will stick around, and [   ]. Would let the ETH ecosystem build + learn at a quicker rate. Goerli may be a better infrastructure to help with this. I am willing and able to do this. We need to figure out research, technology and an incentive model for smart contract and dapp developers to deploy on an alternate chain.

Martin: The problem is not to launch a new testnet, that’s trival. The problem is to implement everything in a client and solve all the issues.

Boris: Right, that’s the problem I’m pointing out: client developers don’t really have an incentive to build “a random testnet” and try it out.

Martin: Yes, but the big problem is we still need to figure out the implementation details for these changes.

Boris: Been spending times with dapp developers. One big question: how do we get Cryptokitties, MakerDAO, 0x to deploy on this?

Alexey: This is why I was thinking about Cosmos/Ethermint.

Boris: Let’s put this on hold, happy to do some cat hearding to help with this.

Alex: Martin is saying the challenge is specifying the changes in detail vs. implementing the testnet.

Alexey: After the state rent proposal, Adrian from PegaSys implemented state rent. Biggest challenge was recovery of contract. Don’t want people to waste their time on sidechains. PoW sidechains don’t work.

Alex: Q to Alexey and Martin; Have you considered forking Ropsten/Rinkeby? They have dapps deployed (Raiden, Gnosis, Maker(?)). Forking that could be a good test base.

Marten: Good idea. Can definitely fork a testnet “in a minority” so that we don’t mess with people who want to use these testnets for other purposes.

Alex: Is it possible to clone the state and change the chain id so that it’s a new network that starts with the same data?

Alexey: Would say yes, but not sure.

### Vlad’s #CryptoLaw blog: “love it” or “absolutely love it”—?

Joke question from our friends at CleanApp

### Want to know more about roadmap of ETH1.x and role / relationship with Ethereum Cat Herders.

Lane:

Born out of EthMagicians

One thing that came out of that, a series of questions, starting with ETHMagicians Council of Berlin – what is the Ethereum roadmap?

Something that has been lacking in Ethereum is project management – lots of smart technical minds

Lane made a call at Council of Prague, from the stage (ETH2 AMA) – ask people to contribute, to do project management. A dozen people reached out.

Hudson and I, and Afri, interviewed people, in pure Ethereum organic fashion, this group emerged.

Not tied to any organization. Open Community, modeled after EthMagicians. People with deep PM experience. Increasing communication. More regular hard fork schedule.

Still looking

https://gitter.im/ethereum-cat-herders/community

Martin: FEM is for discussion. Is this for execution?

Greg: not about discussion, high quality EIPs

Boris: I think about it as a long-form blog anyone can participate in. Great thing that Cat Herders can “pick up” FEM threads.

See https://medium.com/ethereum-cat-herders/decentralizing-ethereum-project-management-ffff4c09d0ea for a bit more info; a longer-form blog post introducing the Herders is forthcoming.

### What resources (people+funding) are required to get all of 1.x into Istanbul? How can we make this happen in the next 6-9 months? Who are the decision makers? What is the process? (Rajeev)

Alexey: 1.x upgrades can’t come in one Hard Fork. Probably more like 3 (shows state rent upgrade picture).

![Uploading file..._sb0hc19oe]()

Alexey: Upgrades are every ~9 months. 3 upgrades ~= 27 months.

Alexey: “Anyone” is a decision maker. Anyone can submit a proposal. But, there is a risk of 1.x “monopolizing” ETH changes.

Lane: Are you saying this because of bandwith for developers or mutual exclusivity?

Alexey: Had a retro about bandwith with Frederik, Vitalik and Hudson. Comments were that implementation isn’t very long once features are specified. What takes more time getting things looked at, discussion of changes, etc. Prior to 1.x, not much motivation to put a lot of changes in before 2.0. With 1.x, we may surprise ourselves re: bandwith! Monopoly assumption came from the bandwith constraints.

Greg: I think this would cause a lot of backlash by the community, as others also have EIPs that are ready for work to be told that their work is put on hold because of 1.x

Joke: rebrand all EIP proposals as ETH1.x !

> Who said it was a joke??? [name=Boris Mann]

Alexey: Monopoly assumption came out of the fact that we had limited bandwith. Problems discussed for 1.x were:

- Four things… missed them

Alexey: Working on figuring out how much time we have to fix these problems. For example, how long do we have to bound the state? Urgency of 1.x work depends on these answers. If the state growth will cause the chain to die in 1 year, then we need to fix this before.

Alex: Can you explain why State rent has to be split into 3 hard forks? Is there a minimum time delay between them?

Alexey: Illustration is very arbitrary. Don’t take it as “approved”. Was just to illustrate a way the changes could be split. Could probably be acheived in 2 (and not 3) hard forks, but would require a *lot* of changes in one of the HFs. After each HF, there will be a PoC for the next steps.

Boris: This doesn’t feel arbitrary. It’s good to see how the EIPs depend on each other, how many hard forks are needed, and how long the changes will take to be fully deployed. This is a good diagram and other large efforts should try to produce something similar.

> Specifically, it sets an expectation for other teams to do similar work – e.g. I want to see the eWASM plan in a similar way. Also mentioned that this is sort of like “Swim Lanes” [name=Boris Mann]

Greg: Agreed, I was critical of the “monopoly” issue. Need to consider the critical page, to not overwhealm the client delveopers. Sounds like a job for Cat Herders to lay out all of these.

Alexey: In this diagram, you can see how certain changes (ex: C & D) can be collapsed into a single hard fork, or into a soft fork (ex: B). This will continue to evolve.

Alex: Why does this have to be separated into different forks? Is it because they have to be activated on different block numbers? Or because it is a complexity/bandwidth issue?

Marten: For the replay protections, you need to separate it. At first, you introduce an optional `time to live` (`TTL`) for transactions, and you need to give time to developers to implement it. After, in another fork, you make `TTL` required.

Alexey: going through non-fork options – some more coordination

e.g. JSON-RPC calls for size of contract, can test on main net before consensus errors

Advanced Sync Protocols, most important change in Ethereum clients, must be done now to avoid slowdown. Group on Gitter to track this. Peter at Geth, ideas at Parity, Alexey/Andrei, Trinity is interested (can’t sync even though they implement everything)

Pretty hopeful that we can delay the doom quite significantly.

---

Boris: re: decision makers, see above for Roadmap link, and EIP-1679.

### I want to contribute in project management.

Yes (Rajeev)

# Notes

## Intros

- ETH 1.x grew from the TurboGeth work, showed at DevCon
- ETH1.x event: Success, but not a lot of people, should maybe have another
- Not super clear what the state of State Rent proposal is, want to use this call for updates
- eWASM vision: have eWASM contracts replace the EVM
- Figuring out the best way to introduce eWASM (precompile vs. deploy full contracts)

---

(next Lane talked cat herders, then Alexey went through questions, lots of discussion in between)

## Post Questions

Alex: replay protection question? _A TTL field. *missed something*

Marten: Previous proposal was from Nick Johnson. Not enough motivation? Easier to clean out transactions. Nicer for user, right now it gets lots, don’t know if it will ever be included. Or if you try and enter some ICO or whatever, and you know there is a deadline, would be a nice to set TTL.

Dust clearing thing makes it very nice.

Alex: even before Nick Johnson, VB proposed it in 2016 with new transaction format, which would be extensible.

Did mention that second part of replay could be soft fork. Wonder if it would make sense to accept both formats. Don’t want to go too deep.

Marten: problem if we accept both, then people who made transactions 2 years ago, they kind of will be replayed. Would put people at risk.

---

Alex: another side comment. One about process and EIPs, came up multiple times. Only point where developers are certain that change is worth implementing, is when it gets scheduled into a hard fork. This particular proposal, change the behaviour by finalizing the EIP earlier, launching on testnet, strong commitment to be in HF.

Boris: explanation of people doing PRs. (MORE HERE)

Marten: high quality PRs is great. getting something in Geth is not that difficult. Test coverage needed. If changes to consensus, transaction tests. Lots of other work that needs to be done.

Alexey: proof of work – i.e. you’ve done some stuff. EIP needs to have proof of concept, tests, etc. All the TBDs need to be done.

Boris: if testing, less TBDs needed – we need to be clear on what people

Lane: perceived legitimacy. This isn’t a side project. Rallying the troops, having them understand. Until the point where ETH2 is ready to go, the canonical roadmap is ETH1x, and therefore we should get more buy in.

Alexey: yes, have some ideas on buy in.

Greg: don’t throw ideas, throw work at us. Proposals for core, Magicians is a good spot to work on Core ideas, but core proposal needs to be well specified, at least a prototype, can’t expect it in all clients, before CoreDevs consider it.

Lane: I think everyone agrees with that. Need to communicate. How to create a good EIP, etc.

Greg: different point, from IfDefElse, miners, etc. People out there mining have ideas that PoS is coming soon, and making decisions on buying hardware. My guess would be at least 5 years. No plan for ETH1 to ever go away.

Lane: to me, looks a lot like that from the roadmap. Not quote and unquote official.

Boris: 27 months from just Alexey’s roadmap

---

Alexey: go over buy in. Description of the problems. What is going to happen, what is going to blow up?

One way is to do emulation.

But let’s understand the problems well first.

(Alexey Blog Post)

> Lots of good explanation, best to watch the video where Alexey walks through everything [name=Boris Mann]

---

## eWASM

Hand to Paul:

Looking at the problem with precompiles, who does the work.

No new precompiles for a while. Start eWASM with solving a

One final precompile, call it eWASM.

Just an idea. Not set in stone.

EVM has its own problems. eWASM is a solid foundation. Identified undefined behaviour. Solid engine. Contract writers might still make mistakes.

Engine might have some sort of bugs in it.

Our blocker now is guarantees from engines. Nice if that engine was audited. For precompiles, would be nice to have fast engines.

Would need compiled eWASM code.

Another interesting problem is metering. How are we going to meter eWASM contracts? have some ideas with Runtime Verification. Doing current block metering. Can do an optimization over EVM where each opcode doesn’t need to be metered.

Metering that doesn’t depend on Web Assembly contract.

Metering that is separate from contracts. Could implement precompiles natively.

Lot of good engineering problems.

Greg: the EVM is defined in the YP, no undefined behaviour. Has been formalized in K and Lem. No lack of firm foundation. Pavel has written a compiler for it. Lots of other problems.

Alex: K also formalized WASM as part of K-WASM.

Greg: just wanted to raise this. Code for EVM has already been written.

Brooke: EVM should be improved in the mean time. Want to second that the EVM isn’t defective in those ways. This is a discussion we need to have.

Alexey: why is eWASM part of ETH1x? What is the common thing between state fees and eWASM. Answer to this, if we want to go into meta features, rather than point features (eg. precompiles for RSA). So the meta-feature is support for multiple languages.

Brooke: LLVM to EVM is also possible. eWASM isn’t going to immediately going to get us these things. Still extra work. And EVM, if we put the effort into, can do similar things without having to drop current contracts.

Alex: I don’t think dropping contracts is part of this.

Brooke: what are we doing with the existing contracts?

Alex: multiple ways to go, they stay as they are.

Boris: what executes them?

Alex: in the short term, same engines are used – same EVM interpreter – no reason to drop them. In the long term, have multiple options. Outside ETH1.0, then the landspace changes.

(sounds like run current EVM and eWASM both in clients)

Alex: in ETH2, maybe no EVM, so no migration path needed. Nothing set in stone.

Marten: adding eWASM engine, have precompiles running eWASM. THen launch new precompiles in eWASM code. Is this the first step?

Alex: actually wrote down summary of different options we are looking at, going through those could explain a lot better.

We have multiple problems, Paul has explained. Precompiles are needed to intro features that aren’t currently possible on the EVM because of block gas limits / processing time. Because of that

Over 2 past years precompiles were proposed. A subset was intro’d with Byzantium end of 2017. No others deployed since then.

Computationally expensive features intro’d to Ethereum. Another issue is the contracts themselves. More about language support and tooling. This has improved in the last year. Still only two major languages, Solidity and Vyper.

One benefit is a different instruction set inside a larger ecosystem. Not just languages, but also security tooling. It did improve over the years. That’s a big thing where a new instruction set could help. Where all these tools already exist.

Brooke mentioned that LLVM to EVM bytecode could be possible. It must be mentioned, it’s not just LLVM to EVM translation. THere are high level features that need to be exposed if this translation is effective.

We are looking at Yul, an IR. Multiple ways to implement. Ways to implement with complete isolation - results are not as expected. Tighter integration provides better results, but increases complexity.

In that case a lot of code would be duplicated and translated. One easy approach in LLVM, not exposing anything, this means you just need to write an LLVM to EVM compiler. I would argue that likely that the performance would not be what you expect. I don’t only mean computation, but also data size. Has a huge effect on the cost.

If you want to expose platform details, that means changing the languages, and the work becomes much bigger.

Going back to eWASM, the two problems / needs, are precompiles and more tools and languages to Ethereum. It seems that, according to eWASM team, could solve both issues.

We have multiple different options and paths. Main goal is to have entire eWASM design on the network. Usable for both user contracts and pre-compiles. Multiple ways to do that. Wanted to clarify three terms, four terms that came up in different discussions.

Contracts, user contracts, that’s clear.

User-defined pre-compiles. They are the subset of eWASM used for pre-compiles, but can be submitted to the network, through something other than a hard fork. Compared to that, pre-compiles can only be done via hard fork. This protects the network. That’s a benefit of pre-compiles in this way.

As a HF, we can audit them. Outside of HF, won’t be audited.

Pre-compiles themselves can be split in two brackets. Interpreted pre-compiles which can be executed with an interpreter. Have looked at 6 pre-compiles proposals. Certain number of those can be interpreted.

The other category are those that cannot be run through an interpreter. eg. Elliptic Curve Pairings – too heavy computation, can’t run through interpreters. Have looked at AOT engines – we mean, virtual machine, or engine, takes WASM blob, translates / compiles, and executes it natively. Couple of different options – translation done each time? Cached? Only HF precompiles? Can we cache the native version in the client?

Very last case is what we call “blueprints”. No WASM engine needed. What blueprint means, it ties into AOTs. Precompiles are defined as WASM blob, and that’s what is accepted into consensus, and also native code becomes part of consensus. Another option is eWASM blueprints, means to calculate gas formula. Currently replaces benchmarking, and do metering formula of realistic gas usage. Clients can take the feature and do it natively, and expect that the formula matches the algorithm.

Implement precompile with a certain algorithm. Client can implement natively. Can be certaing that formula matches it. But, different algo could be faster. Up to the client.

Greg: with these options, where do things fit into stages of the roadmap?

Alex: exact questions we are heavily working on. Clear that some options won’t fit into timeline. Some options will. Have to come up with a proposal, likely having multiple options, with estimated timelines. Certain that, without pointing at any of these options, we know some of them are possible.

Boris: EVM and eWASM in parallel for some time?

Alex: agree that under 1.0, no one is considering removing EVM, there to stay. May as well receive improvements.

Alexey: totally agree with that. Parallelizable transactions

Alexey: second strategy for community buy in (first is statement of problem). Second is impact on large contracts. Something that came up, will need to split up multiple workstreams, done by different people. Read their contract, propose re-write for them, bring them back together. Communicate with large dapp developers. Thinking about Gitcoin Bounties.

Boris: talk to dapps?

Alexey: figure out for them what the problems. Can’t have dapp devs on critical path. Have to analysis first. Do the work as a proposal, as Gitcoin bounties. If you come to meeting with info about how it will work.

---

**holiman** (2019-02-07):

Thanks for taking notes. Some corrections

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Marten: Previous proposal was from Nick Johnson. Not enough motivation? Easier to clean out transactions. Nicer for user, right now it gets lots, don’t know if it will ever be included. Or if you try and enter some ICO or whatever, and you know there is a deadline, would be a nice to set TTL.
>
>
> Dust clearing thing makes it very nice.

Martin: Previous proposal was from Nick Johnson. IIRC, it was not included since it’s a rather big change, and there was not enough motivation to make it at that time.

The main motivation then was,

- Making it easier to clean out transactions from the pools, instead of them sloshing around in the network.
- Nicer for user: if a transaction is ‘lost’, you won’t know if it will ever be included, and you will need to ‘burn’ that nonce to ensure that it never get’s executed.
- Nicer for user 2: If you try and enter some ICO or whatever, when there’s a lot of transactions and hard to get transaction sin, and you also know that there is a deadline where the ICO closes in 6 hours, it would be a nice to set TTL. Right now, your high-priced (but insufficiently-for-this-ico-priced) transaction might get included a day after the deadline.

However, the dust-clearing aspect makes makes this a hard prerequisite, and not only a nice-to-have.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Marten: problem if we accept both, then people who made transactions 2 years ago, they kind of will be replayed. Would put people at risk.

Martin: The problem is if if we accept both types, then old transactions from years ago will be replayable again. So if your account now is empty, and you refill it, then it might suddenly replay the first transaction you ever did with that account. So that would definitely put funds at risk, and basically invalidate the entire reason to implement (temporal) replay protection.

---

**boris** (2019-02-07):

Thanks for corrections / expanded answers [@holiman](/u/holiman)!

(and note - some of those are [@timbeiko](/u/timbeiko) notes, some are mine)

---

**boris** (2019-02-07):

[@AlexeyAkhunov](/u/alexeyakhunov) is working on updated versions of his slides for State Management.

For planning purposes, to close item (2), I’ve extracted his pictures of multi-hardfork planning and put them into a new slide deck. I’m going to adopt this format for future presentations as well. Please use “File > Make a copy…” if you would like to use.


      [docs.google.com](https://docs.google.com/presentation/d/1pk7smp2k65CWCpXrEiZ9BURr8VzNqWdPyRk2mLZ7Jpo/edit)


    https://docs.google.com/presentation/d/1pk7smp2k65CWCpXrEiZ9BURr8VzNqWdPyRk2mLZ7Jpo/edit

###

Fork Roadmap Planning Diagrams to assist in visualizing changes across hardforks








This is a super valuable format to look across dependencies and figure out how many hardforks it will take to get something fully deployed.

The “soft fork” type of deployments probably need more explanation on what is and isn’t possible as well.

---

**5chdn** (2019-02-12):

A roadmap AMA session! I want to join!

---

**AlexeyAkhunov** (2019-02-12):

It was my bad. I was in such a hectic mode, I forgot to invite everyone I should have, of course, including you. I just assumed that people could invite themselves. And many did

---

**AlexeyAkhunov** (2019-02-12):

Yes, please do. I only personally invited couple of people assuming that everyone else would just come and join, sorry it was not clear. It was not an “invitation-only” event

---

**boris** (2019-02-13):

Ideally we will run one in Paris and/or do some more online ones. I spent two weeks tweeting and posting and sending updates and I’m frankly surprised there wasn’t more interest.

[@AlexeyAkhunov](/u/alexeyakhunov) not your fault at all – being decentralized, we have trouble doing communications in a very broad way. I don’t really know how to solve this other than having everyone spread the word.

And Afri wants me to just drop links to events he should be at in his personal Matrix channel ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=9)

---

**rajeevgopalakrishna** (2019-02-13):

Is there one dedicated place/channel which only lists upcoming meetings/events for all FEM rings/topics? Otherwise, these meeting calls get lost in all the other messages. Something similar to “Fellowship Gatherings” perhaps?

---

**boris** (2019-02-13):

I always use the tag [#community-call](https://ethereum-magicians.org/tags/community-call) for all of these I’ve done. It doesn’t make sense to use just one Category – since then the people in a particular ring won’t see it.

I’d suggest continuing to promote [#community-call](https://ethereum-magicians.org/tags/community-call) for all the online stuff.

---

**AlexeyAkhunov** (2019-02-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> @AlexeyAkhunov not your fault at all – being decentralized, we have trouble doing communications in a very broad way. I don’t really know how to solve this other than having everyone spread the word.

I know it is not all my fault. I just wanted to highlight that I did not really pay attention to how this AMA was named. I thought of it as Ethereum1x workshop AMA (and that is why I only personally invited 2 people myself), but it is was also ETH Roadmap AMA, as announced here. Next time I might forget to invite some people again. So I would like to tell everyone - do not wait to be invited. Invite yourself if you want to participate.


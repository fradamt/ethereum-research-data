---
source: magicians
topic_id: 20084
title: Should the EVM transition to a cross-industry open-source foundation and evolve as a cross-chain project?
author: Neurone
date: "2024-05-22"
category: Magicians > Primordial Soup
tags: [evm, governance, community, open-source]
url: https://ethereum-magicians.org/t/should-the-evm-transition-to-a-cross-industry-open-source-foundation-and-evolve-as-a-cross-chain-project/20084
views: 1047
likes: 6
posts_count: 11
---

# Should the EVM transition to a cross-industry open-source foundation and evolve as a cross-chain project?

The Ethereum Virtual Machine is now a de facto public good and not just one of the Ethereum Blockchain core components anymore.

As the EVM’s influence spans multiple blockchain platforms, the entire blockchain ecosystem can benefit from evolving the project’s governance into a cross-industry open-source organization, such as the Linux Foundation, and separating the Ethereum Improvement Proposals from the EVM Improvement Proposals.

The goal is to ensure the EVM’s governance and evolution align with the blockchain space’s interconnected and collaborative nature, reimagining it as a platform-agnostic infrastructure that can seamlessly interact with and support various blockchain networks.

What are your thoughts about this?

**Rationales**

While initially designed for Ethereum Blockhain’s purposes, the EVM has extended its significance beyond that, becoming a fundamental building block for various other blockchain projects, L2s, and chains.

The spreading of the EVM across multiple—even competing—chains and projects consolidated it as a standard, fostering the creation of countless tools and services for developers, companies, and final users.

However, the widespread adoption of the EVM now also raises challenges for its governance and evolution: any changes or updates to the specs have far-reaching implications for all these interconnected chains and projects.

Some blockchains are already unable to be 100% fully EVM compatible, and things will get worse in the future as more EVM specs are upgraded to satisfy Ethereum Blockchain’s needs only.

The concrete risk is a future split in the ecosystem, with increasing difficulty in developing cross-chain compatible tools and services and consequent fragmentation of the developers’ and users’ communities.

Currently, changes to the EVM are proposed and implemented through Ethereum Improvement Proposals (EIPs). While this process effectively addresses the needs of the Ethereum Mainnet chain, it hardly considers the broader implications for the entire interconnected ecosystem of chains and projects utilizing the EVM.

Shifting the paradigm and separating the EVM governance and lifecycle from the Ethereum Blockchain could enable a more comprehensive approach to its evolution, considering the interconnected nature of the EVM’s usage and ensuring that changes or updates are implemented with the broader ecosystem in mind.

## Replies

**matt** (2024-05-22):

Ultimately, the EVM is the Ethereum VM. I think we should make it easy for other chains to develop on top and extend the EVM, but I don’t think it’s possible to have a governing body outside ACD dictate what the L1 EVM looks like.

---

**shemnon** (2024-05-24):

I don’t know about an org whose role is to govern the evolution of the EVM, but an independent org that certifies conformance of EVMs against standards produced by other bodies (such as the EIP and RIP processes) I think would be very useful.

---

**MrSilly** (2024-05-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neurone/48/315_2.png) Neurone:

> As the EVM’s influence spans multiple blockchain platforms, the entire blockchain ecosystem can benefit from evolving the project’s governance into a cross-industry open-source organization, such as the Linux Foundation, and separating the Ethereum Improvement Proposals from the EVM Improvement Proposals

I think you may be misunderstanding what the EIP process is for. Why doesn’t Linux have a Linux Improvement Proposal process?  I’d argue it is because Linux kernels don’t need to agree with each other as much as Ethereum clients do. There are in fact many forks of the Linux kernel that all happily co-exist. The fork maintainers (usually companies) have an incentive to minimize how much their fork diverges from the most canonical development trunk which creates a trend towards convergence over time via contributions to the mainline repo maintained by Linus and friends.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> I don’t think it’s possible to have a governing body outside ACD dictate what the L1 EVM looks like.

This is true regarding governance, especially to the degree that there is only one canonical EVM standard, as the OP suggests.

However a variance of this strategy that could make sense would be to collaborate at the level of modular standards / codebases. The subset of the Linux kernel you need for running a supercomputer is different than the subset you need for running on an Raspberry Pi, but they’re still mostly building on the same codebase.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neurone/48/315_2.png) Neurone:

> Shifting the paradigm and separating the EVM governance and lifecycle from the Ethereum Blockchain could enable a more comprehensive approach to its evolution, considering the interconnected nature of the EVM’s usage and ensuring that changes or updates are implemented with the broader ecosystem in mind.

First, if ChatGPT didn’t write the above you’re doing a great job imitating its default style. Anyhow, for something like this to make sense a few things would have to happen:

1. Non Ethereum projects would have to band up together to maintain forks of EVM implementations in different languages. Ethereum client developers do not have the incentive to do any extra work and some of them seem ideologically opposed to other projects benefiting from their code. Sadly, the positive-sum ethos of open source conflicts with the zero-sum ethos of financial networks.
2. The implementations would have to be modular. Different networks  make different trade offs. It will be hard enough for them to agree on engineering questions, let alone agree on one canonical version when their interests collide.
3. They shouldn’t expect to collaborate with Ethereum client developers until the effort has more to offer them than vice versa. This will realistically take some time.

---

**Neurone** (2024-05-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) MrSilly:

> I think you may be misunderstanding what the EIP process is for.

I know why the EIP process was created and what it is currently used for, which is why I suggest spinning off the EVM Improvement Proposal, keeping the EIP for the Ethereum Blockchain, and having a different *EVMIP* for the EVM.

Currently, those EIPs are only considering their implications for the Ethereum Blockchain.

Developers working on those EIPs are not aware of, don’t recognize, or simply don’t care about the reality that the EVM project has become bigger than the Ethereum Blockchain project.

I was one of those developers, back in 2020 when I proposed my first EIP or when commenting about other EIPs right now, but I think the scenario has changed, and we should envision a different future for this process.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) MrSilly:

> Why doesn’t Linux have a Linux Improvement Proposal process? I’d argue it is because Linux kernels don’t need to agree with each other as much as Ethereum clients do. There are in fact many forks of the Linux kernel that all happily co-exist. The fork maintainers (usually companies) have an incentive to minimize how much their fork diverges from the most canonical development trunk which creates a trend towards convergence over time via contributions to the mainline repo maintained by Linus and friends.

I love Linux, but that does not mean I like *Linus and friends’* governance. Not because I don’t like Linus, but because I would prefer not to live just in the hope that a single man will not go mad or be thrown under the bus for the evolution of core software.

I mentioned the Linux Foundation as an example because I think they can be considered *super partes* (impartial?) and well recognized and estimated in the open source ecosystem. They also own the Hyperledger Foundation, proving that the interest in the space has been there for years.

I was not referring to the Linux Kernel project; I don’t think a parallel with that is a good fit, especially when it comes to governing the project’s evolution.

But as software, the Linux OS based on the Linux Kernel still must be able to talk with Windows and Mac, right? So, when you want to make changes to shared standards (TCP/IP, UDP, DNS, HTTP, HTML, etc.), the best approach is to have a shared ground.

IEEE or W3C are better examples when discussing Internet Protocols, but they are just examples.

To me, an existing organization is better than a new one, but that attains to the *how-to-do-it* phase; I think we are still in the *does-it-makes-sense* or *do-we-want-to-do-it* phase.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) MrSilly:

> First, if ChatGPT didn’t write the above you’re doing a great job imitating its default style.

Am I imitating a ChatBot? ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12) I don’t know; I’m probably still stuck in the moment when ChatBots imitate humans, not the opposite.

I’m trying to convey ideas and get feedback about a complex topic, summarizing it as much as possible to get to the point. I’m not an English native, but I’m trying my best to do it correctly ([deepl.com](http://deepl.com) is my best friend). I hope this does not invalidate the discussion.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) MrSilly:

> Anyhow, for something like this to make sense a few things would have to happen:
>
>
> Non Ethereum projects would have to band up together to maintain forks of EVM implementations in different languages. Ethereum client developers do not have the incentive to do any extra work and some of them seem ideologically opposed to other projects benefiting from their code. Sadly, the positive-sum ethos of open source conflicts with the zero-sum ethos of financial networks.

Isn’t that already the case? We have dozens of implementations of the EVM in different languages. Implementing something is not the problem if the specs are clear, but especially if the specs are not linked to external dependencies. Any chain/project will implement its software, sustaining the costs of doing that as it happens now.

The point is to agree on the specs. When we evolve the EVM specs, we must consider all the implications, not just a single blockchain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) MrSilly:

> The implementations would have to be modular. Different networks make different trade offs. It will be hard enough for them to agree on engineering questions, let alone agree on one canonical version when their interests collide.

Isn’t modularity a good trait to have in any case? By the way, it’s definitely a crucial point, but it relates to the development of the specific EVM implementation more than the specs definition the EVM must comply with.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) MrSilly:

> They shouldn’t expect to collaborate with Ethereum client developers until the effort has more to offer them than vice versa. This will realistically take some time.

Timing is also important, but we will never get there if we never start.

It’s not easy, but we have people here who created a multibillion-dollar public network from scratch in less than ten years, so the problem of achieving this is secondary and it can be figuring out if there’s the willingness to do this.

But is there the willingness to do it or to imagine a different - better? - ideal goal to tend to, where the EVM is not just an Ethereum core component but an independent and shared OSS?

Do we agree multiple chains depend on the EVM to allow inter-ledger integrations, and if we don’t take any actions, sooner or later, the EVM will introduce something that can work only with the Ethereum network, essentially suddenly breaking its compatibility with all the cross-chain projects out there?

Do we recognize this as an issue for the Ethereum ecosystem we should worry about?

---

**MrSilly** (2024-05-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neurone/48/315_2.png) Neurone:

> I know why the EIP process was created and what it is currently used for, which is why I suggest spinning off the EVM Improvement Proposal, keeping the EIP for the Ethereum Blockchain, and having a different EVMIP for the EVM.

What I meant was that it goes back to incentives. It wouldn’t make sense for the current stakeholders in the EIP process to do that because they’re committed to it as a way of making Ethereum better. They’re not necessarily aligned with the success of most other projects that are using the EVM. it would add extra friction when the amount of friction to contribute is already considered by many to be too high.

Making the EVM a good platform for multiple projects is just a harder problem to solve than making it good for Ethereum.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neurone/48/315_2.png) Neurone:

> Currently, those EIPs are only considering their implications for the Ethereum Blockchain.

Correct, and it would be kind of weird for Ethereum Improvement Proposals to have a wider scope than improving Ethereum.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neurone/48/315_2.png) Neurone:

> Developers working on those EIPs are not aware of, don’t recognize, or simply don’t care about the reality that the EVM project has become bigger than the Ethereum Blockchain project.

Simply don’t care. And in some cases even resentful that others are using the stuff they developed for Ethereum. There are different classes of people involved in the EIP process and they often they can’t even see eye to eye with each other. There’s a constant tension between Ethereum researchers and client devs for example. So getting them to see eye to eye with non-Ethereum projects? At this stag, forget about it. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

I agree that it would be a good thing if we could put our tribalism aside and work together in the spirit of open source / science but if we’re going to start making progress we have to recognize where we are right now. We’re not there yet.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neurone/48/315_2.png) Neurone:

> I love Linux, but that does not mean I like Linus and friends’ governance

Well, at the risk of getting a bit philosophical, I think it is always helpful to pin down definitions before having a discussion, especially when there’s a risk people talk past each other because they’re using the same words to mean different things. Unfortunately, this seems to be the default when it comes to governance. When the governance is over a singleton it is governed by either force or opt-out consensus (your choice is fight or flight). When it’s not a singleton, governance is opt-in. You choose to follow something, or maybe you just choose to follow what everyone else is following.

So governance, in the context of an open source project like Linux means something very different from in the context of a country or a company. The reason for that is there is only one instance of a country and there can be many forks of an open source project all competing for status. If you don’t like how Linus and friends govern their copy of the Linux kernel you’re free to maintain your own and do it some other way. The penalty you face for disagreeing with them is that others who accept Linus’s authority may just ignore the work you’re doing and choose to continue building on Linus’s version. Worse case scenario you’ll be left all alone to maintain your other way of doing things, and the larger the delta between your version and the more popular branches, the more work you have to do. At some point you stop being able to share code with others and just branch off into your own separate thing.

Interestingly, Ethereum kind of has both types of governance. There’s only one instance of the rules of consensus for whatever counts as the canonical Ethereum network, because it’s not a stable equilibrium for the name Ethereum to refer to different networks. So there’s a fight over that. But beneath the fight, nobody is forcing anyone to do anything. If you can get enough people to take you seriously you can get your version of the network called Ethereum. Or, as a second best, create a new network that enough people like better to be viable on its own.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neurone/48/315_2.png) Neurone:

> But as software, the Linux OS based on the Linux Kernel still must be able to talk with Windows and Mac, right? So, when you want to make changes to shared standards (TCP/IP, UDP, DNS, HTTP, HTML, etc.), the best approach is to have a shared ground. IEEE or W3C are better examples when discussing Internet Protocols

Yes agreed that:

1. We should separate standards from implementations.
2. Open standards are very important. Without open standards nothing can talk to anything else. The Internet’s success was built on open standards, and many of the problems we have with it now are due to a lack of them. We only need one email client because that was standardized, but we need to have 5 different instant messaging apps because that came later and all the players believe it’s more profitable to have their own proprietary walled garden.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neurone/48/315_2.png) Neurone:

> Am I imitating a ChatBot?  I don’t know; I’m probably still stuck in the moment when ChatBots imitate humans, not the opposite. I’m not an English native, but I’m trying my best to do it correctly (deepl.com is my best friend). I hope this does not invalidate the discussion.

Sorry, that could have come off as unnecessarily rude. I’m not a native English speaker either. Maybe sounding like a bot is what happens now when the translation services use LLMs. The other day I was thinking maybe I should consider passing all my writing through ChatGPT and ask it to make me sound friendly. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

FWIW, I think it’s the ideas that matter, not the style. I have nothing against these tools it’s just that ChatGPT’s default style adds many unnecessary words to make things sound legit. If you use them without editing, you end end up sounding like a politically correct committee.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) MrSilly:

> Non Ethereum projects would have to band up together to maintain forks of EVM implementations in different languages.
>
>
>
>
>  Neurone:
>
>
> Isn’t that already the case? We have dozens of implementations of the EVM in different languages.

To the best of my knowledge they’re not banding together yet so every implementation lives in its own little universe walled off from the others. The closest thing to what you suggest is actually the Rollup Improvement Process (RIP), which isn’t an easy sell even when you’re trying to coordinate rollups that all use Ethereum. Extending that beyond Ethereum rollups could be a great idea, just harder. If it happens it’ll be because someone stepped up to lead the effort and manages to herd all these cats together.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neurone/48/315_2.png) Neurone:

> Do we agree multiple chains depend on the EVM to allow inter-ledger integrations, and if we don’t take any actions, sooner or later, the EVM will introduce something that can work only with the Ethereum network, essentially suddenly breaking its compatibility with all the cross-chain projects out there?

Re cross-chain, the devil is in the details and smarter people than myself have made compelling arguments that:

1. cross-chain compatibility is a pipe dream
2. cross-rollup compatibility is probable achievable, but still hard
3. The design space of rollups should allow any tradeoff you want while still leveraging the security of Ethereum, so why would you want to dilute your attention to support other layer 1s if you’re already committed to Ethereum?

I believe if someone did want to step up to lead the effort they should start by helping the other L1s become rollups instead and use their token for governance instead. Then they can join the RIP process.

---

**mratsim** (2024-06-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neurone/48/315_2.png) Neurone:

> As the EVM’s influence spans multiple blockchain platforms, the entire blockchain ecosystem can benefit from evolving the project’s governance into a cross-industry open-source organization, such as the Linux Foundation, and separating the Ethereum Improvement Proposals from the EVM Improvement Proposals.
>
>
> The goal is to ensure the EVM’s governance and evolution align with the blockchain space’s interconnected and collaborative nature, reimagining it as a platform-agnostic infrastructure that can seamlessly interact with and support various blockchain networks.

This sounds like architecture astronauting.

There is no benefit from separating the EVM from EIP process except increasing friction and governance cost.

Other blockchains choose to use the EVM, they didn’t have to. They ride on Ethereum coattails but they don’t contribute back.

For Linux, companies contribute back maintenance, dev time and tooling. Until that happens, what would Ethereum get from spending valuable time and coordination resources (yet another call per week at minimum) from divesting the EVM from EIP?

Even worse, many criticized the EVM and tout not using the EVM as a marketing tool. Even Vitalik himself publicly mentioned several times that the EVM had significant flaws:

- 2021: x.com
- 2024: Vitalik: If time could go back, I would rebuild Ethereum like this

and the EF certainly worked on completely changing the EVM from the ground up with eWASM: [design/rationale.md at master · ewasm/design · GitHub](https://github.com/ewasm/design/blob/master/rationale.md)

In fact, what blockchains are you thinking of that would contribute besides Ethereum? As mentioned in this blog post [Ewasm: Where We Are and Where We Are Going | by Daniejjimenez | Medium](https://daniejjimenez.medium.com/ewasm-where-we-are-and-where-we-are-going-c5b0d80a0e5e), many are using WASM, why would they change?

---

Replying to further comments

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neurone/48/315_2.png) Neurone:

> The point is to agree on the specs. When we evolve the EVM specs, we must consider all the implications, not just a single blockchain.

The implication for Ethereum is extra friction, extra governance, extra time for core devs that are already busy. The gains are zilch, not even goodwill as criticizing Ethereum or the EVM is used as a differentiator.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/neurone/48/315_2.png) Neurone:

> Do we agree multiple chains depend on the EVM to allow inter-ledger integrations, and if we don’t take any actions, sooner or later, the EVM will introduce something that can work only with the Ethereum network, essentially suddenly breaking its compatibility with all the cross-chain projects out there?

Forking is an architecture decision, they bear the cost of that decision, and there is a simple solution to avoid breaking changes, use versioning.

Or they can start from a stable base like Ethereum Classic VM (see [GitHub - ETCDEVTeam/sputnikvm: A Blockchain Virtual Machine](https://github.com/ETCDEVTeam/sputnikvm) ) which explicitly mention targeting EVM-based blockchains.

Expecting Ethereum to maintain the EVM, then EVM clients and then to maintain cross-chain projects is very one-sided.

Regarding cross-chain transactions you don’t need VM equivalence, there are Ethereum L2 that use the SVM instead of the EVM.

> Do we recognize this as an issue for the Ethereum ecosystem we should worry about?

No. There are only downsides for Ethereum.

---

**mratsim** (2024-06-04):

Now, I’m sorry for “personal” attack towards the project you seem to work for, Hedera Hashgraph, but they have been engaging in the past into questionable tactics to undermine Ethereum and did not build goodwill among Ethereum core devs.

For instance this article ranked Ethereum Consensus last in terms of energy efficiency and Hedera first:

- https://web.archive.org/web/20210908231937/https://finance.yahoo.com/news/proof-stake-ethereum-2-0-153221744.html

They mention a research article from University College London which is available here:

- https://arxiv.org/pdf/2109.03667
- https://web.archive.org/web/20210908121907/http://blockchain.cs.ucl.ac.uk/wp-content/uploads/2021/09/UCL_CBT_DPS_Q32021_updated.pdf

It states

> Conflict of Interest
> M.P. declares that he is bound by a confidentiality agreement
> that prevents him from disclosing his competing interests in
> this work.

And curiously the version on Hedera website does not state anything: [Wayback Machine](https://web.archive.org/web/20210908120438/https://hedera.com/UCL_Env_Impact_Report.pdf)

And University College London is a sponsor of Hedera ([Pioneering Best-In-Class Governance | Hedera Council](https://hedera.com/council)):

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/9/94e9975e047e160335f66296170236884a98e4a7_2_690x137.png)image1400×279 28.1 KB](https://ethereum-magicians.org/uploads/default/94e9975e047e160335f66296170236884a98e4a7)

I can only surmise that Hedera under the guise of a reputable university has been engaging into research with very questionable bias and trying to hide it.

This is further demonstrated from the methodology of the research itself.

> Nevertheless, existing models can be combined with additional data arising from the scientific literature, reports, and public ledger information to form a baseline that can be used to avoid time-consuming experimental validation.

I think this is enough to show that Hedera does not engage in goodwill collaboration and is not legitimate to ask anything out of Ethereum core devs.

---

**shemnon** (2024-06-04):

Who is this directed at?

---

**mratsim** (2024-06-06):

[@Neurone](/u/neurone), see his Github [Neurone (Giuseppe Bertone) · GitHub](https://github.com/neurone)

---

**Neurone** (2024-06-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mratsim/48/2872_2.png) mratsim:

> Now, I’m sorry for “personal” attack towards the project you seem to work for, Hedera Hashgraph, but they have been engaging in the past into questionable tactics to undermine Ethereum and did not build goodwill among Ethereum core devs.
>
>
> […]
>
>
> I think this is enough to show that Hedera does not engage in goodwill collaboration and is not legitimate to ask anything out of Ethereum core devs.

I appreciate your taking the time to read and answer this thread and your previous message on the topic, regardless of whether I agree with your opinions.

I consider this a serious topic: **taking (or not taking) action about it has practical and real implications for multiple projects**.

And yes, I think developers currently working with EVM-compatible networks should definitely contribute to the discussions and share their opinions, ideas, and experiences.

I don’t see the need to drive the conversation to other topics. Hedera isn’t asking anything out of to Ethereum core devs, and I think people here do not care about Hedera or my career in the Web3 ecosystem, so **I’m skipping replying in details to all those statements** even though I totally disagree with them ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)


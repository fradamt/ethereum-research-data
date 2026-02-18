---
source: magicians
topic_id: 139
title: "EIP-867: Standardized Ethereum Recovery Proposals (ERPs)"
author: phiferd
date: "2018-04-16"
category: EIPs
tags: [fund-recovery]
url: https://ethereum-magicians.org/t/eip-867-standardized-ethereum-recovery-proposals-erps/139
views: 10305
likes: 37
posts_count: 39
---

# EIP-867: Standardized Ethereum Recovery Proposals (ERPs)

Creating this thread as a place to continue any discussion around EIP-867 once the PR is merged as a draft.

## Replies

**sfultong** (2018-04-17):

Thanks for creating this thread, [@phiferd](/u/phiferd)

I’m against 867 because accepting/rejecting ERPs is a governance issue, and I don’t think devs should be burdened with making those decisions.

---

**SylTi** (2018-04-17):

I agree with sfultong, I think the DAO recovery was a mistake that opened a can of worms. We need to definitely close it; not open it wider.

---

**postables** (2018-04-20):

This kind of issue should not even be considered as it’s something that can harm the integrity of everyone’s network for the monetary benefit of a very small portion of the user base.  The error that resulted in this catastrophic loss of money wasn’t the fault of the protocol or the network rather it was the fault of the developer of the code, but more importantly the fault of everyone who lost money because they didn’t do their own due diligence. Why you wouldn’t when entrusting hundreds of millions of dollars is beyond me but to each their own. Since this is a human element which is the sole source of troubles why not settle it in court the way the rest of the world does when they lose money? The fact that you continuously submit this pull request goes to show just how powerful this technology is. It seems like this same pull request comes through every 2-3 months. Maybe if we make this into a meme you’ll stop?

https://ethereum-magicians.org/uploads/default/original/1X/73320ef06c0da46582c2cdb9fc71b96dcd764c1b.jpg (content updated by [@jpitts](/u/jpitts) to only link to the meme)

---

**postables** (2018-04-20):

And the second meme for now

https://ethereum-magicians.org/uploads/default/original/1X/288edc1ec17be104ac17c8f27d0bae3643026e3c.jpg (content updated by [@jpitts](/u/jpitts) to only link to the meme)

---

**tenthirtyone** (2018-04-20):

The memes are toxic and we can do without them. Reposting my comments from the github thread as they are still relevant.

**TLDR: If you don’t like network history you fork, not the entire network.**

I think forking is easier, better and preferable to a bureaucratic process.

As you point out, this proposal is just the Tyranny of the Majority

“this would require massive coordination among people running clients to succeed, essentially like any other kind of 51% attack.”

I can misunderstand too. But I see forking as the solution to immutable history if you disagree with the history.

Furthermore, I think this fundamentally misunderstands the point of cryptocurrency. A major appeal, for me, is the push vs pull type of transaction. This breaks that. Because now the network has a pull transaction that can take money from anyone - just like banking. Then I don’t technically own my coins. The people who can vote to take them do.

I don’t think I support this on any grounds but I can be educated if I am completely missing the point.

---

**postables** (2018-04-20):

Very valid, if we don’t own our own coins then we might as well just stick with the banking system we have now which clearly demonstrates what happens when you give a very small number of people contrpl over large amounts of financial assets. About the meme(s), I would counter that submitting this same pull request over and over again despite it being pretty clear  what eveetone thinks, Is infinitely more toxic but I do see what you’re saying. If there are problems with it then I would be happy to remove them.

---

**bwheeler96** (2018-04-21):

I still strongly oppose this EIP. The blockchain is not designed to have a history that can be rewritten.

---

**jamesray1** (2018-04-21):

Extending on others comments which I generally agree with, accepting this EIP or any other fund recovery EIP such as EIP-999 would set a precedent that may encourage people to be less cautious about thoroughly auditing their code. It discourages due diligence on the part of investors, and investing in teams and using products that do not have open source code.

---

**MicahZoltu** (2018-04-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tenthirtyone/48/112_2.png) tenthirtyone:

> I think forking is easier, better and preferable to a bureaucratic process.

The ERP process is a forking process.  It is just a recommendation on how people can formalize their requests for a hard fork when it pertains to recovery of lost (not stolen) funds.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tenthirtyone/48/112_2.png) tenthirtyone:

> now the network has a pull transaction that can take money from anyone - just like banking

Note: The ERP process is pretty clear on never being used to take money away from one owner and assigning it to another.  It is designed/worded such that it can only take money that is *inaccessible by anyone* and assign it to the person that *should* have access to it.  This happens in situations where people typo an address, or end up with funds stuck in a smart contract due to a bug.  The ERP process is expressly *not* for something like TheDAO recovery where funds were *taken* from one party and given to another.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/postables/48/114_2.png) postables:

> pretty clear  what eveetone thinks

Just because a handful of people brigaded a GitHub issue doesn’t mean that *everyone* believes a thing.  There are something like 36,000 Ethereum nodes in operation, and likely some number of orders of magnitude more Ethereum users.  I guarantee you that we haven’t heard from the *vast* majority of economic participants on the issue.  This is one of the many problems with any kind of voting or “majority rule” system of governance.  Those who make the most noise are not necessarily the same set of people who should be listened to (sometimes the sets overlap, sometimes they don’t).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bwheeler96/48/78_2.png) bwheeler96:

> The blockchain is not designed to have a history that can be rewritten

Note: While possibly just a technicality, this process does not propose rewriting history.  It proposes changing the rules of how history is written in the future.  *All* hard forks are just “changing the rules by which future history is written”, this one is proposing formalizing a *process* by which certain classes of rule changes can be discussed and easily implemented rather than handling this whole class as a series of unrelated changes.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamesray1/48/1548_2.png) jamesray1:

> would set a precedent that may encourage people to be less cautious about thoroughly auditing their code. It discourages due diligence on the part of investors, and investing in teams and using products that do not have open source code.

Unfortunately, no matter how much care and due diligence you put into writing software, it will (almost) always have bugs.  OpenSSL Heartbleed is a great recent example of something that has gone through probably the most stringent of security audits over two decades and *still* had a critical security flaw in it.  As long as humans are the ones writing software, there *will* be bugs.  We certainly want to encourage people to write good software and do their due diligence, but at the same time I think it is unreasonable to assert that anyone who authors software with a bug deserves to be severely punished (on the order of hundreds of millions of dollars).

Personally, I think even with a streamlined ERP process, the cost of recovery is still very high, along with forced capital lockup time while you wait for the next hard fork.  IMO, this is “punishment enough” to encourage people to write good code, while still allowing for fixing of honest mistakes.

Also, keep in mind that the ERP process cannot be used to recover funds that are in possession of anyone.  This means that TheDAO hack, fraud, theft, etc. *cannot* be rolled back with this process.  Thus, there is still *significant* incentive to write good code since the bug you ultimately run into may not be a “lost funds” bug but instead a “stolen funds” bug which this process will not help you with.

---

**jamesray1** (2018-04-21):

Thanks for the insightful comments Micah!

There’s still a concern that the process adds more burden on core developers. (EIP editors shouldn’t have much burden, they just read an EIP and merge it as a draft if is technically sound and the author has finished editing it and is happy to merge it.) Who is going to bear the cost of the extra hours invested by core developers into recovering lost funds? We should have layer 2 markets for decentralized insurance. Until they are implemented we *could* allow recovery of lost funds, and then after they are implemented we could only allow recovery of lost funds proportional to the amount insured.

---

**phiferd** (2018-04-21):

If there’s a moderator on this thread, please remove the memes (at the very least, the one with a picture of James). Regardless of where you stand, don’t tolerate that nonsense here, please.

As I said the same at the first Ethereum Magicians meeting – it’s all of our responsibility to ensure that the conversation is respectful and productive.

---

**bwheeler96** (2018-04-21):

[@MicahZoltu](/u/micahzoltu)

> While possibly just a technicality, this process does not propose rewriting history. It proposes changing the rules of how history is written in the future.

A hard fork to recover funds is exactly rewriting history. It seems parity likes to use the term “state transition” where during a hardfork the state of the blockchain is modified by the hardfork. That is what funds recovery almost necessarily implies. So…

If a bug is caused by an EVM issue, and the funds are recoverable by the EVM issue, then sure lets hardfork to patch the issue, and then the affected parties can make recoveries.

If a bug is not caused by an EVM issue, or simply patching the EVM will not enable users to access lost funds, there should not be a hard fork to recover the issue.

> Unfortunately, no matter how much care and due diligence you put into writing software, it will (almost) always have bugs.

The EVM is a special case. Programs are generally so simple that writing bug free code is in fact expected.

**IF DEVELOPERS EXPECT TO RELEASE BUGS, THEY CAN CREATE THEIR OWN UPGRADE SCHEMA THEMSELVES.**

Arguing hardforks for fund recovery are OK because developers will inevitably release bugs is essentially saying that everyone who develops on Ethereum and everyone who uses all those applications needs to trust the core dev team to keep their funds safe, when they should be relying solely on open source smart contracts.

Hard forks for the sake of funds recovery could be the death of Ethereum.

---

**tenthirtyone** (2018-04-21):

We’ve represented most of the high-level ideas from the old thread here very well. Though I easily miss things. I welcome any correction and the extra value it would bring to the thread.

First, thank you [@MicahZoltu](/u/micahzoltu) for addressing each point. It’s going to be crucial that all voices are heard for us to solve this problem. Second, thanks to [@jpitts](/u/jpitts)  for giving us a place for civil discourse.

I’m hearing things in your feedback ([@MicahZoltu](/u/micahzoltu) ). I could use your help checking my understanding.

You expressed a market need quite well that many of us tend to miss. There are users who wish to take part in this wonderful experiment. But they are discouraged by the high price of failure.

We should show compassion to these customers. The responsibility of being your own bank is brutal. Each of us likely still remembers the fears of our own early transactions still to this day.

As we grow up together in this technology the time for vanguards will pass. We will need a way to onboard these users or we give other projects an advantage.

However, we cannot deny that there are also users who value immutability. Therefore non-recoverability of funds is of higher value to them than the actual recovery of their funds.

We have to respect and show compassion to these customers as well.

I propose we look to the features and innovations of this new technology to solve this problem. Let’s move forward together with new ideas.

Finally, we must bulwark against the slippery slope. Introducing a moral justification for lost fund recovery could lead to a moral justification for other appeals for on-chain authority. Something we must avoid.

My short-sightedness did prevent me from seeing the value here. And I am ready to agree. There is something we can do.

EIP-867’s original proposal was:

1. Standards that will need to be met by any follow-on ERP in order to be considered for approval.
2. Recommendations for a common format for ERPs to use to specify a set of corrective actions that can be interpreted by clients.
3. Guidelines for client teams to implement code that can read, interpret, and apply the corrective actions at a specific block.  The set of possible corrective actions is intentionally limited to minimize risk associated with any ERP.

I propose a new beginning and solicit the review of peers here, and elsewhere…

Requirements:

1. The Ethereum Recovery Proposal respects the fundamental features of cryptocurrency - property rights, immutable history and the resulting digital scarcity.
2. The Ethereum Recovery Proposal will provide a ‘Sandbox Environment’ for projects wishing to explore the Ethereum production network with their project.
3. The Ethereum Recovery Proposal recognizes the customers right to informed consent before making their financial and technological decision.

Implementation

1. Going forward, projects wishing to engage in the Ethereum Recovery Proposal will include an boolean identifier on their smart contracts
isEIP867 = true
2. Each EIP867 contract that receives user funds will lock them via smart contract. The contract will implement the following features

- Create a new Token - Recovery Eth (Reth)
- 1:1 with user Eth

It will implement the following functions

- abort - Contract Owner function. Return user funds and selfdestruct project contracts
- convert - DAO vote by Reth holders to convert the project from Reth to Eth. “Go Live” functionality provided to users
- escape - Reth holder function. Return user funds, destroy user Reth.

All contract operations will use the Reth token.

Each project may implement its own degree of fiat within its Reth environment.

The market may decide on the price of each project’s Reth.

Each project’s Reth price is protected by the 1:1 backing of Eth.

Merchants may accept Reth at a 1:1 Eth value as they may instantly convert back to Eth upon receipt of the token.

The customer has the comfort of experimenting without the fear of crooked developers, zero day exploits or unknown bugs that may affect the project.

The Ethereum Network does not have to change a thing. It provides these features out of the box already. This change is entirely reliant on developers putting aside their own hubris and/or customers demanding it of project developers.

The cost of these additional features is amortized to each project. The ‘inevitability of mistakes’ problem mentioned by [@MicahZoltu](/u/micahzoltu) is now properly mitigated to the developer rather than subsidized by the entire network.

I think this is a reasonable start. Apologies for the wall of text. I welcome feedback to this proposal whose spirit is to preserve the entire underlying technology that originally brought us to the project while showing compassion to new users.

Edit: To clarify. My message is If Fiat is to exist here it will do so under our umbrella of voluntary property rights. As our system is so superior that it is permissive even to those systems which disagree with it. They may freely operate so long as they do so peacefully.

Fundamentally, our property rights cannot exist under their system. Even if we operate peacefully. That is why I see this as the only possible compromise - As I acknowledge I can be wrong.

---

**MicahZoltu** (2018-04-23):

[@tenthirtyone](/u/tenthirtyone) The problem with layer 2 solutions (contract solutions) as you have proposed is that there could just as well be a bug in the Recovery ETH layer as there is in the next layer contract.  Also, contracts that want to interact with other contracts (like a multisig wallet) can’t really implement this as a layer 2 solution.  The Parity bug, for example, would have still been a problem even if they implemented a layer 2 solution.

Similarly, most of the recovery proposals that have been discussed couldn’t have been avoided with layer 2 solutions.  For example, many of them are just people accidentally entering an address with a typo, or forgetting to include a destination in their send, or using an Ethereum API incorrectly.  Many of these people aren’t interacting with contracts at all, they are interacting directly with the blockchain.

Re: Slippery slope.  One of the reasons I like the ERP process is because it puts well defined boundaries on what is “acceptable”.  The alternative is to handle each case as a one-off which is more susceptible to slippery slopes (though I’m still not convinced it is really that slippery).

---

You bring up some useful terminology in your comment [@tenthirtyone](/u/tenthirtyone), which is the difference between “property rights” and “immutability”.  The ERP process is an attempt to enforce property rights, while people who argue for immutability are really arguing *against* property rights.

I’m curious, those of you arguing against property rights, why is it that you don’t like the idea of property rights?  What is it about immutability that makes you value it over property rights?

---

**sfultong** (2018-04-23):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Note: The ERP process is pretty clear on never being used to take money away from one owner and assigning it to another.  It is designed/worded such that it can only take money that is inaccessible by anyone and assign it to the person that should have access to it.  This happens in situations where people typo an address, or end up with funds stuck in a smart contract due to a bug.  The ERP process is expressly not for something like TheDAO recovery where funds were taken from one party and given to another.

This is not my interpretation.

I assume you’re referring to the Justification section, which says

“A concise description of why this action is both reasonable (cannot be accomplished without an irregular state change) and unlikely to be challenged by a *directly* affected party.”

What does “directly” affected mean?

If anyone claims that they are directly affected by an ERP, and they object to that ERP, does it mean the ERP should automatically be rejected?

What if a directly affected party is in jail? In that case they will be unlikely to challenge any ERP.

---

**MicahZoltu** (2018-04-23):

This is the bit that, in my opinion, makes it so that any funds currently controlled by an individual (e.g., TheDAO hacker) would not qualify for going through the ERP process (emphasis mine):

> This EIP describes a common format to be used for a subclass of EIPs […] that propose an irregular state change required to address a fund recovery scenario that cannot be addressed using the standard protocol.

If there exists a private key known by someone (or possibly known by someone) that has access to the assets in question, then it is *possible* to handle the recovery via the standard protocol (e.g., via an ETH transfer transaction).

[@phiferd](/u/phiferd), there may be value in making this a bit more plain/obvious/clear.  While I do think the above quote technically creates that requirement, to the average reader it is not obvious on first glance.

---

**phiferd** (2018-04-23):

[@MicahZoltu](/u/micahzoltu) is correct in his interpretation. I’m certainly open to rewording if there’s a better way to phrase it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sfultong/48/71_2.png) sfultong:

> What does “directly” affected mean?

For directly affected, let’s start with a simple example.

A → B*, where A is a regular account and B* is a off-by-one typo of address B, which is also a regular account (i.e. not a contract).

In this case, there are clearly two “directly affected” parties: A and B. The owner of address C doesn’t have any provable involvement in the transaction. If we agree that private property exists on the blockchain (I don’t think everyone here does), then A and B are the only two people that really have anything to say about what the “right” solution is. The ERP process (explicitly) only applies in cases where A and B *agree* on the solution.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sfultong/48/71_2.png) sfultong:

> If anyone claims that they are directly affected by an ERP, and they object to that ERP, does it mean the ERP should automatically be rejected?

No. In the example above, C cannot just arbitrarily claim to be affected.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sfultong/48/71_2.png) sfultong:

> What if a directly affected party is in jail? In that case they will be unlikely to challenge any ERP.

If B is in jail and A claims that funds in B* should be sent to A, then the agreement requirement cannot be met. In that case, a B would likely challenge. However, if A agrees that the funds in B* should go to B, then B’s permission probably isn’t required (after all, A can send funds to B anytime he wants without B’s permission).

Can it be more complicated?  Of course. However, the ERP process was not meant to handle all cases.  Rather than saying “here are 50 scenarios we *can’t* solve” we tried to carve out a boundary around cases that we can solve.

---

**tenthirtyone** (2018-04-23):

Thanks [@MicahZoltu](/u/micahzoltu), I want to address your points and possibly clear up any misunderstandings you have regarding property rights.

Layer 2 is just as susceptible as Layer 1. Yes, I never disagreed here. The bonus is that your project may now implement whatever degree of fiat that it needs. **Which is the spirit of the ERP - To what degree will Ethereum users allow for Fiat in their network**? It should be sandboxed as far away from the chain as possible. Preferably left to the legacy banking system

As Fiat would represent a backwards incompatible and breaking feature for the current user base the only compromise is for projects wishing to include Fiat-as-a-Feature (FaaF) to do so moving forward, in their own projects. Not as a network solution to a problem specific to a single project.

I love your point about multisig and interacting with other contracts. I will update the ERP spec - Projects that implement the Ethereum Recovery Proposal should only interact with other Projects that implement the Ethereum Recovery Proposal. Thank you.

This will protect other teams from projects that require they test their beta product in production.

Now then, let’s talk about property rights…

If you own a bar of gold and throw it in the Marianas Trench, I agree you can make a case that you still own that gold. This would be tantamount to a user miss-typing the receiving address of a transaction.

But to me, that’s a valid transaction. Code is Law the same way we will not rewrite the laws of physics to reclaim the bar of gold.

The argument for an ERP that changes the fundamentals of the protocols binding Ethereum together is frustrating because it relies on sliding the goal post - The Slippery Slope. Its already happening right now. Code is Law so you pose “Let’s move where the line is for the Code.” While that is clever, it shows a belligerent misunderstanding of the environment and its users.

Even the definitions of property rights are subject in this upside down argument. For if we were to apply your airy and nebulous standard to current users the network would break. I could just as easily claim every tx ever sent by me was a mistake and force this very human process to decide who owns what funds - no different from a banking system.

The user was the only person able to send those funds down a black hole. They did. **Part of the responsibility of owning property is that you can make mistakes. It is a fundamental failure of property rights to grant one group some exclusive privilege**. In this case, the ability to reverse their transaction.

Furthermore, there are many more perfectly legitimate use cases where a user would burn a coin - sending to address(0) for instance. Since your proposal relies on a human fiat process to determine if funds were sent incorrectly the only option you have is a layer 2 solution.

As this entire proposal is nothing more than a single project (Parity) masquerading their required change as a required change to the core fundamentals that govern the Ethereum network is ultimately elitist favoritism toward a tiny group I think we should put an end to the masquerade and call this exactly what it is:

The Parity team has shown they are incapable of production code without putting their user funds at risk. To date, they have put more effort into changing the Ethereum network to suit their project than toward building a beneficial product that is a boon to the ecosystem. Maybe Ethereum just isn’t the blockchain for the Partiy team? Maybe they should fork and start a chain that provides the FaaF they need?

Let’s not forget, the entire premise is the most recent Parity debacle is assuming the user ‘accidentally’ triggered the selfDestruct. The Developers left that feature in the code. The developers are responsible. Regardless, I would be willing to go on record (although it is not true) claiming to be the person who called selfDestruct and I would claim that title saying I did it intentionally. That would defeat the entire foundation of the original EIP. At least, for Parity users.

---

**phiferd** (2018-04-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tenthirtyone/48/112_2.png) tenthirtyone:

> Regardless, I would be willing to go on record (although it is not true) claiming to be the person who called selfDestruct and I would claim that title saying I did it intentionally. That would defeat the entire foundation of the original EIP. At least, for Parity users.

I suggest you rethink this approach; to claim that you’re willing to lie to get what you want really doesn’t help your argument.

---

**MicahZoltu** (2018-04-24):

ETH Recovery has been a desired thing since before the Parity multisig issue.  While the Parity multisig issue is the biggest single loss, there are a large number of other smaller losses that effect a large number of users.  I like blockchains because they prevent institutionalized theft (e.g., [Civil Forfeiture](https://en.wikipedia.org/wiki/Civil_forfeiture_in_the_United_States) and [Chargebacks](https://en.wikipedia.org/wiki/Chargeback), not because they enable me to shoot myself in the foot.  What I am proposing is that we protect people from shooting themselves in the foot where we can, while continuing to defend against institutionalized theft.  I *almost* left for ETC because I saw it as an instance of institutionalized theft (effectively a chargeback), and in the end my reasons for sticking with ETH had nothing to do with the to-recover or not-to-recover question.  Should institutional theft become a pattern, I would likely leave Ethereum.

For me personally, I have a [Shelling Fence](https://www.lesswrong.com/posts/Kbm6QnJv9dgWsPHQP/schelling-fences-on-slippery-slopes) that prevents this from being a slippery slope.  It certainly feels like the disagreement is around whether or not a Shelling Fence exists.


*(18 more replies not shown)*

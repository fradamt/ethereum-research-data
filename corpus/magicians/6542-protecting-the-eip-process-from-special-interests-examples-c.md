---
source: magicians
topic_id: 6542
title: Protecting the EIP process from special interests + examples & case study
author: defectivealtruist
date: "2021-06-24"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/protecting-the-eip-process-from-special-interests-examples-case-study/6542
views: 5669
likes: 63
posts_count: 50
---

# Protecting the EIP process from special interests + examples & case study

## Motivation

Can we better protect the EIP process from special interests while improving the incentives for those working for the public good?

The purpose of this post is to get the ball rolling on a discussion we hope will eventually result in the equivalent of a meta EIP that  structurally improves the EIP process.

## The problem: high reward for colluders, low reward for honest people

Without improvements to the current EIP process there is a danger that protocol lobbyists getting paid to serve special interests will outnumber unpaid altruistic volunteers serving the public good, leading to a tragedy of the commons.

We believe this is already a problem and that it is getting worse. We’ll start by providing some general examples, and examine in more detail a recent EIP as a case study.

We can break the problem of perverse incentives down into two related sub-problems:

1. High reward for getting bad EIPs in: special interests have a high incentive to lobby governance for changes that benefit them, even at the expense of the public good or other stakeholders. This can be a high stakes adversarial game, where success depends on obfuscation, collusion and misdirection. Successful protocol lobbyists could be highly motivated and well coordinated.
2. Low reward for promoting the public good: either by protecting from bad EIPs or by doing all the work to get good EIPs in. Both require significant talent, time and energy.  Only some of this work is intrinsically rewarding. The current process relies heavily on altruism and prestige, and it is unclear whether this will scale in proportion to the scaling rewards for successfully attacking the process.

The imbalance is a natural consequence of **public choice theory** (see David Friedman’s [excellent original writings on the subject](http://www.daviddfriedman.com/Academic/Price_Theory/PThy_Chapter_19/PThy_Chap_19.html)). The core idea is that **concentrated special interests win out over diffuse public interests**, sometimes even when the diffuse public interest is larger in absolute terms. A somewhat naive calculation for illustration:

- $100 million gain divided by 100 colluders = $1M gain per colluder
- $1 billion loss distributed across 100,000,000 million public victims= $10 loss per victim

Coordinating the defense is hard because it’s a large group, and each individual member of the group internalizes only a very small portion of the benefits of a successful defense. Special interests, on the other hand, are a *concentrated interest*, which each participant expecting to see a large portion of the gains from getting their proposals implemented. Hence, the attackers will be highly motivated, while the defenders suffer from a tragedy of the commons.

### Testimonial: what it’s like now for honest people

*"To prevent a bad proposal that someone is really motivated to push in, I have to write posts, prove my point beyond doubt, talk to people to make sure the issues get enough exposure, and I’ll probably need to stay on it, defend my research on the ACD, etc.  And I have no real incentive to do this, other than defending the ecosystem I care about.  The people on the other side are strongly motivated. They are paid to fight for their EIP, and have a lot to gain from it. How many EIPs will pass because no one is willing to put the resources to shoot them down, while the proposer is motivated to push it through?*

*And the same goes in the other direction. I’m often reluctant to propose EIPs that I think are good for everyone because I’m afraid  the process of pushing it past the objections at ACDs and getting it accepted would exhaust me.*

*And so EIPs that don’t personally benefit someone are less likely to be accepted, while EIPs proposed by companies that stand to gain are more likely."*

## General examples of EIPs that may benefit special interests in subtle ways

Sunlight is a good disinfectant, but whether it’s enough depends on how deeply it penetrates.

The more attention and domain expertise is required to understand how value or risk is transferred, the less resistance can be expected, and the easier it will be to get the critical mass of community sentiment required to persuade the core devs to include a change.

A blatant EIP that says “give X ETH per block to our cabal” will quickly get rejected (and, indeed, even EIP-2025, a not-obviously-malicious proposal of that type was quickly thrown out). But there are far more subtle protocol changes that can benefit some constituencies at the expense of others.

Some examples include:

- Precompiles

Concentrated interest in favor: specific use case that wants a precompile
- Diffuse interest against: large increase in consensus complexity, dependence on external libraries, development time delaying high-priority items (e.g., the merge)

**Coin rescues or other state-intervention forks**

- Concentrated interest in favor: single group that wants their coins saved
- Diffuse interest against: risk of chaotic split, precedent, long-term higher governance burden and controversial-fork risk due to emboldened future requests

**Highly specialized in-EVM/state data structures (e.g., sorted storage slots, heaps)**

- Concentrated interest in favor: specific use cases (e.g., on-chain order books) that benefit from these structures
- Diffuse interest against: greater consensus complexity, lower flexibility to make future changes (e.g., sorted storage slots would have prevented Vitalik’s recent Verkle tree proposal)

This is not to say that all proposals of the above categories are bad; sometimes a more concentrated gain really is on the whole greater than the widely distributed cost of a proposal. But *as a general rule*, we should expect the concentrated pro- side to be systematically over-represented, and the diffuse anti- side to be systematically under-represented.

The open and inclusive nature of the EIP process is currently our main defense against bad proposals. However, given that proposals may be complex and subtle in their effects it may be unsafe to rely on proposals being self evidently good or bad. An open process where everyone has access to various public forums may not in practice provide sufficient protection to balance out the perverse incentives.

## Starting to explore the solution space

We’re going to try and start the conversation by proposing some principles and ideas. This list will be incomplete as the intention is to **get the ball rolling, not say the final word**.

We believe it’s important to recognize that **making bad things harder has to be balanced with making good things easier** so that we don’t end up throwing out the baby with the bathwater. We wouldn’t want to “protect” the EIP process by shutting it down.

### Principles of defense we can learn from the city of Troy

Let’s use the famous trojan horse that brought down the ancient city of Troy as a metaphor.

Thanks to the open nature of the process, everyone who is paying attention can see what is trying to get through our metaphorical gates. This means an attack has to sneak past the public’s guardians in plain sight.

How do we raise the bar and make it harder to disguise attacks (e.g., the infiltrating force that opens the gates to the city) as “gifts” (e.g., a beautiful statue of a horse to decorate our city)?

For example, this may involve a combination of improvements to our processes that help us:

1. Better understand who is offering us gifts and what is their motivation. Who are they working for? What’s their track record? Are they friend or foe? How aligned are they with our values? Do they have conflicts of interests?
2. Make sure we have enough highly trained guards that are well paid and stay alert. Volunteers are great, but there’s only so much glory to be had and standing guard gets old fast.
3. Make it harder for attackers to lull us to sleep by hijacking our trusted institutions.
4. Make sure our guards can sound the alarm and draw attention to an attack that might overwhelm them. We can’t defend ourselves against attacks we don’t realize are happening.
5. Investigate close calls so we can iterate intelligently on our defense mechanisms while carefully balancing trade offs and avoiding knee-jerk overreactions.
6. Keep score to increase public awareness of who is doing a good job helping us, and who has been trying to harm us. Since our attention and resources will always be limited, we should allocate it intelligently. Leveraging reputation could be part of the solution.
7. Reward and honor what we want more of - benefactors and guardians of the public good, while penalizing and shaming what we want less of, those who attack us in the service of special interest.

## Example ideas for making lobbying for bad proposals harder

### Open bounties to incentivize permission-less research

*“Given enough eyeballs, all bugs are shallow” - Linus’s law*

The last line of defense before including any EIP in a network upgrade could be an open bug bounty that will pay anyone who discovers significant flaws that blocks the EIP’s inclusion as is. The reward should be at least enough to pay for an independent audit at current market rates. It should be open for long enough to give independent researchers time to find flaws.

The benefit of a bounty as a supplement to a contracted audit is that it is minimally opinionated regarding who will succeed. It’s not who you know, it’s what you know. Anyone with skill can try to claim a bounty and get compensated for success with economic and reputational rewards.

The bounty process should not only reward finding flaws in existing proposals but also alternative proposals that achieve similar benefits with a better risk/reward profile.

### Post-mortem on failures and close calls

*“Fool me once, shame on you. Fool me twice, shame on me”*

When a bad proposal almost gets in, maximize the learning from that by funding a bounty that rewards the  best understanding of what process improvements would have maximized our margin of safety against bad proposals while minimizing the friction for good proposals.

### Fund “meta audits” that watch the watchers

Reward those who watch the watchers and help the community hold auditors accountable.

One way to do this would be to post open bounties for the best “audits of auditors”. These would reward those that take a close look at what past audits missed and help the community reassess how much to trust their brands.

Consider using these “meta audits” to update a public hall of fame & shame that makes it easier to notice when auditors miss critical issues. The effect should be that when a critical issue is missed the community can reduce the “credit score” of that auditor.

Auditors have skin in the game to the degree that they are held accountable for endorsing bad proposals (e.g., explicitly or implicitly). For an efficient auditing market to form around Ethereum the reputation of auditors and the amount of business they get should be based on their performance.

Pushing auditors with low standards out creates a market opportunity for auditors with higher standards.

Achieving this is a public good and will help improve an industry otherwise prone to market failures, though it’s worth thinking carefully about how to do this to avoid introducing perverse incentives that adversely affect e.g. what EIPs auditors are willing to audit.

### More transparency

*“Sunlight is the best disinfectant”*

1. Require disclosing conflicts of interests: all proposers and their supporters must disclose conflicts between their private interests and the interests of the public, or the interests of other stakeholders in the ecosystem.
2. Require disclosing motivation: all proposers and their supporters must disclose their motivation for participating. This means what they stand to gain if the proposal is accepted.
3. Require disclosing means: all proposers and their supporters should disclose who they are working for.
4. Whistleblowing: encourage people to provide evidence in those cases where important information is being withheld.
5. Accountability tracking: if evidence establishes beyond reasonable doubt (e.g., thanks to a whistleblower) that proposers and their supporters withheld information on their motivation, means or conflicts of interests, their reputation should suffer and their ability to influence the EIP process should be diminished. Similarly, exceptional positive contributors should see their reputation benefit. Some form of public tracking (e.g., badges) can be used to formalize this.

### Transparency and accountability for Ethereum Foundation signalling

1. Make signalling explicit: In order to prevent the hijacking of the EF’s brand, the EF should publicly disclose its intention in funding work related to an EIP.
 For example, it should be clear whether an EF employee authorized funding an audit in support of what they believe to be a good EIP proposal or out of concern that it may be flawed in a way they can’t put their finger on.
 This will be more clear if the EF explicitly signals the former when it has the intention to support something, and the latter when it does not.
2. Increase personal skin in game by disentangling organizational and personal reputations: the EF is not a hive mind like “The Borg”. It is a collection of individuals with varying degrees of domain expertise. The domain experts the EF relies on to authorize signalling on the EF’s behalf should have skin in the game. The community should be able to see their faces. Their personal reputation should increase by supporting good things, and diminish from supporting bad things.

## Example ideas for making more good things happen

In addition to making it more difficult for EIPs promoted by special interests to pass through unchallenged, it is also important to make it easier for truly important EIPs to make it through, even if they don’t have any special interest constituencies supporting them (e.g., EIP-2929 gas price changes) to improve anti-DoS safety that were talked about for over a year without progress before they started to be implemented).

## Retroactive grants for EIPs

How much more top talent could we attract to serve the public good if it was at least (or more) economically rewarding to work on that than in the service of special intersts?

Retroactive grant models make it possible for those interested in allocating resources to the public good to solve the easier problem of evaluating impacts post-hoc instead of the harder problem of anticipating future impacts.

There’s more than one way to do this but here’s a simple approach. Each EIP could designate a *proposer* that will be responsible for getting the EIP all the way through to a network upgrade and distributing any retroactive grant amongst collaborators afterwards. The proposer would also track which individuals and teams made the most important contributions to that EIP, and make an allocation table representing what they consider to be a fair distribution of rewards.

Any tips (from the public, or the EF, or other grantees, or potentially revenue from selling an NFT of the EIP) would be split among the contributors according to the allocation table. If desired, the allocation table could even be tokenized, allowing an independent team to raise funds to pay for fiat or ETH-denominated expenses if they can convince the market that their EIP will succeed and be deemed valuable.

## EIP 3074 as a case study

We expect this to be the most controversial part of this post, but we feel it is instructive to examine a live specimen of protocol lobbying currently in progress in the service of a powerful and highly motivated special interest - Consensys. We are watching the situation unfold with growing concern, but have so far avoided getting directly involved in this discussion on the public forums under any name.

### On the precipice

Consensys’s proposal was deceptively simple and was purported to solve the important problem of gas abstraction, by creating a new type of transaction that delegates control over an EOA to a contract. This appears more powerful and dangerous than what is needed for gas abstraction. Why do it this way? From EIP 3074:

*“A good analogy for the benefit this EIP provides is that it’s similar to allowing any EOA to become a smart contract wallet without deploying a contract.”*

This is both insightful and potentially misleading. As Vitalik points out, rather than accomplishing account abstraction, [EIP 3074 enshrines EOAs instead of helping us get beyond them](https://ethereum-magicians.org/t/we-should-be-moving-beyond-eoas-not-enshrining-them-even-further-eip-3074-related/6538).

It now seems dangerously close to getting into the next network upgrade, despite:

1. Critical security issues that were not discovered by two EF-commissioned audits
2. Being designed to benefit Consensys’s proprietary Metamask wallet at the expense of open source smart contract wallets
3. Centralization risks

### The security flaws that almost went undiscovered

Up until a last minute intervention by the unpaid volunteer who posted *“A simpler alternative to EIP 3074”* on this forum, the process not only failed to catch the security problems but also failed to come up with alternatives that had potentially better risk/reward profiles and could get the purported upsides with fewer downsides.

### The candid discussion that didn’t happen

At no point in the process did we have a public discussion on why promoting EIP 3074 was in Consensys’s strategic interests, or how it risked benefiting Consensys at the expense of other stakeholders like Gnosis and Argent.

We also didn’t discuss whether it was interests of the Ethereum community to tilt the playing field in Metamask’s favor, especially given that after establishing high market share they rug pulled on open source licensing, a core Ethereum value.

### How did we get so close to EIP 3074 being seriously considered for inclusion in the next network upgrade?

Consensys made all the right moves. The proposal is deceptively simple on its surface. They made it easy for the core devs by implementing the client change. They lobbied for it behind the scenes, starting with their natural allies and gradually networking out to expand their circle of support.

Consensys also cleverly lobbied to position their proposal as something that EF was supporting. Consensys could have easily funded the audits by themselves, but they probably realized it would legitimize the proposal more if they could get the EF to participate, and thus leverage the EF’s trusted brand.

In various internal community calls promoting this proposal the impression conveyed was that it was endorsed by the EF and was practically a done deal. Who wants to criticize a proposal backed with the prestige of the EF?

A piece of the puzzle that is still missing is what role Consensys played in selecting the auditors, given that Least Authority ended up endorsing EIP 3074 after missing critical issues. From their report:

*“We conclude that under the right conditions - wallets and invokers being implemented correctly - that this proposal is safe for use”*

Promoting a false sense of security can have negative value.

### How could things have played out differently?

Imagine that a year ago we had this discussion on protecting the EIP process from special interests and improved the EIP process with some of the ideas presented in this post. How could things have played out differently?

#### We wouldn’t rely on unpaid volunteers to catch critical security issues

If we had been routinely auditing the auditors by comparing their audit reports to what was later discovered we may have noticed Least Authority’s poor track record  and adjusted their reputation appropriately.

Ideally, the pain of visibly losing reputation in our metaphorical hall of shame would incentivize Least Authority to be more diligent with their audits. They might catch more critical issues, or at least be more cautious in providing endorsements that could come back to haunt them.

With bug bounties as the last line of defense, the situation would tend to be more self correcting as critical issues that auditors miss would be an opportunity for new auditors to make a name for themselves.

Auditors that keep missing critical issues would cease to command a premium as a source of trust and may have to switch to a different business model such as competing for bug bounties that only pay out on success.

#### Consensys wouldn’t have been able to hijack the EF brand

1. Explicit signalling: most likely EF would have clarified that it was funding the audits out of concern rather than with the intention of signalling support.
2. Accountable domain experts: if Consensys tried pursuading a domain expert at the EF to explicitly signal support for EIP 3074, that person would have to consider whether they were confident enough to stake their personal reputation on doing that.

#### Understanding motivation

First, we would have started by encouraging a candid discussion about Consensys’s motivations in promoting EIP 3074 so aggressively.

If the proposers didn’t provide full disclosure regarding their ties to Consensys we might regard them personally with suspicion. If they were honest about their affiliations but were simply not in a position to disclose Consensys’s strategic interests due to an honest lack of insight we could regard not them but their employer with suspicion and invite community members to try and fill in the gaps.

We could invite speculation on Consensys’s business interests and the goals of senior management while still believing that most of the technical people working for Consensys are good and well intentioned community members.

#### Better late than never

As an exercise, let’s try to take a stab at understanding Consensys’s motivation. Suppose the future belongs to smart contract wallets and we expect EOAs to be gradually phased in favor of account abstraction. This is not good for Metamask, the dominant EOA wallet owned by Consensys.

#### Why exactly is EIP 3074 so important to Consensys?

EIP 3074 is strategic for Consensys because it changes the rules of the games to make it possible for the proprietary Metamask wallet to leverage its position as a dominant EOA wallet to compete and possibly displace trusted open source smart contract solutions like Gnosis and Argent.

This would potentially further centralize Ethereum around Metamask.

#### Understanding Metamask’s strategic positioning with/without EIP 3074

How does EIP 3074 transform the red ocean of smart contract wallets into a blue ocean for Metamask?

Without EIP 3074, if Metamask wants to compete in the smart contract wallet space it has to develop a new smart contract wallet offering and then try to convince users to choose that over other more mature smart contract solutions that have empirically stood the test of time and have billions in assets under management. That’s a hard sell.

With EIP 3074, Metamask can seamlessly convert their userbase in place to a new kind of smart contract wallet (they coined “Synthetic EOA”) by having users sign a special type of transaction that delegates control to an all capable invoker contract. They control the UX, so it should be not be hard for them to do that.

#### One contract to rule them all

An EIP 3074 invoker contract will be as extremely security sensitive as any smart wallet contract. Assuming Consensys don’t make a catastrophic mistake, their invoker contract could gain enough Assets Under Management to provide empirical validation that it is trustworthy.

Given the sensitivity of this contract, users that are using Metamask’s invoker will be reluctant to switch to other invokers. Metamask can leverage their trusted invoker to provide their users with similar benefits to smart contract wallets without the pain or risk of migration. This way Metamask gets to lock-in users that would have eventually “graduated” to open source smart contract wallets.

To the degree that competition in the market resembles a winner take all tournament competition will be limited and we could end up centralizing Ethereum around a proprietary wallet with a natural de-facto monopoly.

From EIP 3074:

*“Choosing an invoker is similar to choosing a smart contract wallet implementation. It’s important to choose one that has been thoroughly reviewed, tested, and accepted by the community as secure. We expect a few invoker designs to be utilized by most major transaction relay providers, with a few outliers that offer more novel mechanisms.”*

### The process that Consensys is exploiting is more of a problem than Consensys

Amongst our friends are technical people at Consensys that we like and respect. The above case study is not meant to attack anyone involved in EIP3074 personally. Good people can be misguided. They are not the problem.

Consensys itself is also not the problem. It’s a rational corporate actor trying to maximize its special interests. In that sense it is not fully aligned with Ethereum’s values, but it is not unique in this regard.

The problem is if we don’t do a better job protecting the EIP process from the special interests, EIP3074 will not be the last bad proposal that is on the verge of getting in. If our defenses don’t hold, successful attacks would embolden future attacks. In the worst case scenario, this could incentivize the creation of a well funded lobbying industry that gradually captures the EIP process.

## Replies

**timbeiko** (2021-06-25):

[@defectivealtruist](/u/defectivealtruist) thanks for your post! Lots to unpack. I’ll share some thoughts below.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> Precompiles

I think we’ve moved to rejecting more and more precompiles based on the “diffuse interests against”, see EIP-2537 as a recent example, along with the desire to potentially do EVM384 instead. This seems to me like a clear case where there were several private interests pushing for precompiles, but it did not lead to inclusion.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> Coin rescues or other state-intervention forks

The only occurrence of this is TheDAO fork, which I have no desire in re-hashing, but needless to say a large enough % of the community’s funds were involved that the line between private and public interests was blurred, and those who disagreed with this particular intervention got the opportunity to “exit” to ETC.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> Highly specialized in-EVM/state data structures (e.g., sorted storage slots, heaps)

Are there any examples of EIPs for this you can share?

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> The last line of defense before including any EIP in a network upgrade could be an open bug bounty that will pay anyone who discovers significant flaws that blocks the EIP’s inclusion as is.

This already exists: https://bounty.ethereum.org/ In the past, we’ve doubled it when mainnet upgrades were happening, too. It does not fit all your criteria, but is at least a start.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> The bounty process should not only reward finding flaws in existing proposals but also alternative proposals that achieve similar benefits with a better risk/reward profile.

This is interesting! I think the tradeoff here is that we risk grinding the process to a halt because some EIPs, especially more complex ones, will never be perfect. For example, we already tabled a few tweaks to EIP-1559 for a “v2” someday in order to ship what had been implemented/tested/audited. Not saying I’m against the idea, but we need to weigh the pros/cons.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> When a bad proposal almost gets in, maximize the learning from that by funding a bounty that rewards the best understanding of what process improvements would have maximized our margin of safety against bad proposals while minimizing the friction for good proposals.

Agreed we should do this, and I think we’ve somehow gotten worse at them. We’ve done a few in the past, but I agree we should do more, have them be of higher quality, and publicize them more broadly. Relying on volunteers/already overworked people is probably the main blocking factor here, and likely one that can be addressed.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> ### Fund “meta audits” that watch the watchers

I’m concerned this has more cons than pros. The first is that if our audits currently rely on volunteers or “altruistic” participants, putting a target on their back is likely to make them less eager to participate. IMO we need to move towards having consistent high quality audits set up before trying to go for “meta audits”.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> Require disclosing conflicts of interests

Questions: where do you think this should be done? Some people have done it on AllCoreDevs, for example, but it doesn’t get written in the EIP. Also worth noting that the EIP process is currently open to anonymous submitters, so it may not always be possible. It is worth noting the tradeoff there.

Also curious what you think is the “bar” for conflict?

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> Require disclosing motivation

I think this tends to happen naturally, but people can still conceal bits of it. (1) and (3) probably cover what doesn’t get disclosed.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> Require disclosing means

I can see some people not being comfortable doing that, but in general this already happens. For example, the BLAKE2b precompile was clearly stated as being pushed by people who wanted better interoperability with ZCash (even though it ultimately didn’t accomplish that…!).

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> Whistleblowing: encourage people to provide evidence in those cases where important information is being withheld.

Strongly against this. When it is important enough, it happens naturally. The EIP process is already quite taxing to participate in, and having people feel like they have a target on their back throughout will likely prevent people from contributing.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> ### Transparency and accountability for Ethereum Foundation signalling

This is a big can of worms which in practice doesn’t seem like the core problem to me (in the spirit of your post: I am a contractor with the EF). Open to change the process based on the community’s requests, but that’s the extent of my comments.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> ## Retroactive grants for EIPs

Strongly agree with this! I am working on something like this at the moment and, interestingly enough, the biggest pushback I’ve gotten is that it can lead to more capture of the EIP process, or at least the perception of “special interests funding changes”. I still think on net it is a good thing, but it is worth mentioning that this can easily go “against” a lot of the principles that you list.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> ## EIP 3074 as a case study

(Disclosure: ex-ConsenSys employee) One meta-error in your analysis here is overestimating the amount of coordination within ConsenSys (specifically the two different orgs which the 3074 champions and MetaMask belong to). Won’t dwell on it because it could very well be that individuals are closely coordinated and future orgs may be more aligned, but worth mentioning.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> It now seems dangerously close to getting into the next network upgrade, despite:

This is false. It has been discussed as potentially being included, but there were never formal conversations about inclusion.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> Critical security issues that were not discovered by two EF-commissioned audits

I think we have a pretty good track record of taking EIPs out if there are security concerns, even if they are brought up late in the process. See Istanbul/St-Peterburg for example, or more recently EIP-2537 being removed from Berlin.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> EIP 3074 was in Consensys’s strategic interests, or how it risked benefiting Consensys at the expense of other stakeholders like Gnosis and Argent.

This is a bit harder. That “scope” of discussion is not really a part of the EIP process. Perhaps we could include it more explicitly, and obviously Gnosis or Argent would be free to share their thoughts about the EIP in the current process. There is just not really a concept of “strategic analysis” for EIPs.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/d/7ab992/48.png) defectivealtruist:

> The problem is if we don’t do a better job protecting the EIP process from the special interests, EIP3074 will not be the last bad proposal that is on the verge of getting in. If our defenses don’t hold, successful attacks would embolden future attacks. In the worst case scenario, this could incentivize the creation of a well funded lobbying industry that gradually captures the EIP process.

I agree that this is likely to get worse, but one counterbalancing force I see is that as the community grows, getting consensus on *any* change becomes harder, which naturally leads to protocol ossification. There are several proposals that could have been possible 4-5 years ago that likely are not today, and I suspect the same will be true in the future. I think this is a feature and not a bug.

Again, thank you for sharing all of this. I’d be happy to support and help anyone who wants to propose specific changes to the process and get them adopted. If you want to do this, I would encourage you to also review past changes to the EIP process and their success or failure. My #1 bit of advice would be to try and do things iteratively vs. proposing a “complete overhaul”. If you can find the 1-2 things you think will be most impactful, it is easier to get buy in for those, see them work, and add 1-2 more, vs. trying to do 3-5 changes at once.

---

**CryptoBlockchainTech** (2021-06-25):

I agree 1000% with moving away from a system that is easily exploited by the few and powerful as this was needed a long time ago to prevent the proliferation of ASICs on the network and preventing Consensys from installing their own people into the 1559 implementation process to ensure smooth implementation…ahem, ex Consensys employees.

Good luck to you but moving to POS will be 100x more difficult to stop special interests from corrupting the process as this is the very nature of POS. POS ensures those with the most skin in the game have the loudest voices, which if you look at who some of the the biggest stakers are…exchanges.

It is only going to get more difficult going forward to ensure Ethereum remains a truly decentralized entity. This is a much needed start to a problem that has been around for a long time and is only now coming to the forefront where it is easier to see.

---

**vbuterin** (2021-07-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> defectivealtruist:
>
>
> Highly specialized in-EVM/state data structures (e.g., sorted storage slots, heaps)

Are there any examples of EIPs for this you can share?

I think the OP’s intent was to list classes of potential “good for concentrated interest, bad for public interest” ideas in general, including things that haven’t been proposed yet but might conceivably be in the future. That said, from the early days of Ethereum I do remember multiple instances of things in that category being proposed. Particuarly:

- There were discussions in 2014 about adding “next empty storage slot” and “prev empty storage slot” opcodes, which would have allowed Ethereum contracts to maintain and operate over sorted data structures without the tree-on-top-of-a-tree hacks that are required today. The idea was eventually scrapped because developers intuitively realized that something with the interface of a hashmap can be implemented far more easily than something with the interface of a search tree.
- Early on we were considering looking into adding priority queue data structures to the EVM so we could efficiently implement on-chain order books (Bitshares had on-chain order books and there was a desire to have an equivalent), but this was scrapped due to complexity
- Proposals for enshrined ERC20 tokens (this was shot down quickly, because of the “if you can do it without enshrined protocol features, you should do it without enshrined protocol features” principle)

None of this made it to EIP stage, because it was the 2014-15 era and the community was small enough to keep track of proposals informally. But it is a good example of things that were successfully averted by a pro-simplicity/minimalism norm!

---

**SamWilsn** (2021-07-03):

We’ve held two community calls (though I can only find the [recording](https://www.youtube.com/watch?v=pUJlZMXrVEI) for one at the moment) to discuss with groups outside of ConsenSys, and the feedback has generally been positive. I’d hardly call them “internal.” Maybe it’s time to hold a third?

This is perhaps off-the-main-topic of this post, but I’d be really interested in discussing (and possibly co-authoring a post on) the specifics of centralization risks and how EIP-3074 benefits ConsenSys/MetaMask over other wallets. My Telegram & Discord handles are the same as this account here, or we can figure out some other method of communication if need be!

---

**pedrouid** (2021-07-04):

As author of WalletConnect protocol, one of the alternative wallet providers to Metamask, I could not be happier to see EIP-3074 being included in the next hard fork

Sponsored Transactions are going to completely change wallet UX for Ethereum positively in so many ways.

I can’t wrap my head around how the OP found this EIP to put Metamask in advantage over any other wallet.

Meta-transactions have been researched and developed for years and even current Smart Contract Wallets would benefit from EIP-3074.

I’m not interested in who sponsored or funded the research and development of EIP-3074. The spec speaks for itself and it will be IMO the most impactful EIP to mainstream adoption

---

**cmagan** (2021-07-08):

Isn’t it all about the subjective definition of “good” and “bad” EIPs?

I think it is generally positive that there are many stakeholders each with his own self interests.

Sometimes, someone can try to promote an EIP that benefits himself more that it benefits others (or even hurts others).

Then it is the responsibility of others to point it out - but they might be many “little guys” that don’t understand or have enough economic interest in the matter.

So my takeaway is that **transparency** and **accessibility** are the most important and hard to corrupt mechanisms that might help more people to get involved and keep the process aligned with their interests.

How should we make reliable and transparent information about EIPs as available and accessible to many people?

How those people would be able to express their preference in a sibyl resistant way?

---

**fulldecent** (2022-04-13):

Sufficiently advanced lobbying is indistinguishable from grassroots initiatives.

---

**dtedesco1** (2022-04-13):

Yet is either necessarily good or bad? Ay, there’s the rub.

---

**gcolvin** (2022-05-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pedrouid/48/16715_2.png) pedrouid:

> The spec speaks for itself…

Exactly.  We are evaluating technical specifications, not their provenance.

---

**MrSilly** (2024-04-12):

Without a fight, the decentralized censorship-resistant vision of Ethereum has little chance of winning against the work of deep pockets on a pragmatic core dev community that doesn’t seem that hard to infiltrate or persuade to go against those values. A few things that might still make a difference:

1. Being more explicit about Ethereum’s values of decentralization, censorship-resistance, open source and open standards and campaigning in their support.
2. A critical examination of the implicit governance that has filled the vacuum from the absence of any formal process. Is it right to just count votes by core devs? If so, who counts as a core dev and how do we prevent special interests from stuffing ACD with their people?
3. Amending the EIP process to invite more criticism by adding sections such as conflicts of interest, winners & losers.

---

**MrSilly** (2024-04-12):

# How do defend Ethereum from the threat of retroactive bribes?

Airdrops can be used for retroactive bribes. Building on the OP’s example, imagine a de facto natural monopoly is created around Metamask’s invoker contract post EIP 3074 getting in. This could logically follow from the circumstances without any nefarious intentions: invoker contracts are extremely security sensitive, so it would make sense for Metamask and other wallets to whitelist them with extreme prejudice, to avoid users being tricked into delegating their wallets to a malicious invoker. As the largest EOA wallet Metamask’s invoker is likely going to get the most traction. It will have the largest AUM. The larger its AUM the more trusted the contract is going to be, because the AUM serves as a natural bounty. The larger the bounty, the more confidence we can have the contract is safe, because the incentive to compromise has not materialized.

It would be safest for this contract to be immutable, and I’m hoping this turns out to be true for the first versions of it, given the security implications. But let’s consider what happens if down the road, after enough confidence has been built up, an upgradeable version of the invoker contract is launched. Naturally, you couldn’t have the upgrade capability controlled by a centralized multi-sig. That would be unsafe. So we could end up with a governance token. One that controls one of the most important contracts in the ecosystem, with the largest AUM other than the beacon chain. It might be worth a lot. Maybe billions. We’ll have airdrops, possibly  rewarding everyone who supported the consensus changes required for all of this to happen. They would be celebrated as retroactive grants for public goods instead of a reward for promoting a special interest. Nobody has to even promise anything in advance or act in bad faith. The incentives around this are similar to the revolving doors between government regulators and private industry.  The expectation of a lucrative high paying job after your public service ends can be enough to align those working in the public sector with the private sector. No bribe needs to be offered or accepted. No laws broken.

The possibility of using airdrops this way makes it harder to protect governance against special interests. I am a little reluctant to point this out but probably this is something those working to promote special interests are smart enough to figure out for themselves. I’ve come around to thinking it is better to talk about this openly so we can think about possible mitigations and have the motivation to implement them.

A conflicts of interest section in the EIP might help somewhat. They’re standard in the academic world. In the meantime, until we make that improvement to the EIP process, perhaps asking openly anyone who is campaigning for an EIP whether they have any upside (eg equity) or expectation of receiving upside (eg informal promise) to the example outcome?

Exposure or expectation of upside wouldn’t necessarily be a dealbreaker that makes your arguments in favor of an EIP invalid, but the extra information gives the other participants in the discussion the ability to account for the possibility of some motivated reasoning being in play. We’ve done this implicitly for things like EIP-999 but it isn’t always going to be that obvious.

---

**MrSilly** (2024-04-12):

>

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> I think we have a pretty good track record of taking EIPs out if there are security concerns, even if they are brought up late in the process. See Istanbul/St-Peterburg for example, or more recently EIP-2537 being removed from Berlin.

Tim, didn’t ACD just vote to include EIP 3074 despite it opening up a denial of service attack by breaking the DoS protection we have for EIP-4844 BLOBs? Can the existing governance process claim to be pretty good at addressing security concerns when instead of relying on a careful auditing process you end up bringing it to a vote after discussing security concerns on the call itself? How can we expect anyone to have the ability to understand a complex issue on the fly like that?

It seems somewhat unsafe to rely on the ability and willingness of individual contributors like Yoav to highlight issues with a proposal while also relying on the ability of others on that call to evaluate those arguments right before its brought to a vote. It’s unserious to do things that way. Security vulnerabilities are not mitigated by having more of whomever counts as a core dev vote in favor of them. Doing things this way not only risks letting in a proposal that exposes the network to attack but also risks delegitimizing ACD as a governance venue that can be taken seriously by the community.

As an alternative, perhaps we should consider for contentious proposals a more formal and rigorous evaluation process that includes auditing and a request for comments from the community on all aspects?

---

**SamWilsn** (2024-04-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) Liraz Siri:

> evaluation process that includes auditing and a request for comments

That’s a great idea! We can have a body of editors that ensure the quality of documents, a forum for discussing the proposals, and a comment period to make sure the community has a chance to contribute. Since it’s a process for making suggestions to make the blockchain better, let’s call it the Ethereum Improvement Proposal process, or EIPs for short!

---

**MrSilly** (2024-04-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) Liraz Siri:

> evaluation process that includes auditing and a request for comments

Perhaps not carefully worded enough. How about  “security evaluation process that includes auditing and a request for comments by the auditors on potential security problems”.

Is that more clear now?

---

**MrSilly** (2024-04-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> We are evaluating technical specifications, not their provenance.

If “we” were perfectly trustworthy and “evaluating” was straightforward then yes provenance wouldn’t matter.

In the real world, both “we” and “evaluating” will be impacted by special interests.

“Evaluating” correctly requires domain expertise and attention, neither of which is equally distributed. Expert opinions can also be bought and if you don’t dive deep enough it can be hard to tell a trustworthy authority from one that isn’t. How safe is it to give an equal vote to people who are not equally informed and equally attentive? How would making governance decisions this way not devolve into “you scratch my back I scratch yours” politics?

Regarding “we” what measures do we currently have in place to prevent special interests from influencing who is on the de facto committee of core devs that is asked yay or nay on a CFI?

To believe this is not worthy of a serious discussion supposes that the controls around who gets a vote are either perfect or imperfect but good enough to resist pressures from special interests with deep pockets. I don’t think we have good reason to believe either. If you’re a big corporation that stands to gain billions from a change to consensus is it really that hard to hire core devs? Or perhaps send your protocol lobbyists to infiltrate client teams and influence them from the inside? If the other devs are not too opinionated about the consensus change that is being lobbied for the lobbyist might end up representing that team. If it’s a prestigious team, the lobbyist could end up with the power to essentially veto consensus changes that don’t align with the lobbyists agenda, because for example, they solve problems the lobbyist claims to care about in ways that don’t benefit his sponsors. In the background the lobbyist would be coordinating behind the scenes to form alliances with other players so ACD calls are basically done deals. In the foreground there would be a meme factory that would out-campaign everyone else to manufacture consent or at least its appearance. Campaigns would play on the prejudices of the community, claiming its all about giving power to the people rather than promoting tirelessly in the service of special interests. They’d play to the fears of other core devs (eg “core devs don’t care about users!”).

My point is as soon as there is enough money at stake from capturing governance provenance matters because it ties back to incentives. We may no longer be in the environment where naive social conventions work best and everyone can be assumed to be acting in good faith. If someone is a protocol lobbyists it could help to know who they’re working for. Again, this doesn’t mean the proposal is bad. A scientist working for a corporation can still produce good science and have integrity, but as soon as they start responding to criticism with memes on X and politics, they’re no longer doing science and we can’t pretend they’re not motivated by something other than truth.

---

**SamWilsn** (2024-04-13):

The foremost experts on Ethereum security are likely the same people working on the client software, who are the same people deciding which proposals to accept. Auditors who can do better are rare and presumably expensive. Requiring these external audits as part of the process would be extremely unfair to EIP authors without deep pockets.

---

On a more personal note, I want to express my apologies for the sarcasm. This is a touchy thread for me.

---

**MrSilly** (2024-04-13):

No need to apologize. I understand this subject has been contentious for quite some time so bound to surface some difficult emotions. Still appreciated though.

1. For sure some of the people who understand the protocol best are working for the client teams, but the skillset required for implementing and maintaining a high quality client does not necessarily intersect perfectly with the skills for excelling in protocol design and security. It would be a happy coincidence if it does, but we shouldn’t rely on that. I think that’s why we have a research team. If we didn’t need them it would be more efficient for the client teams to just sort out implementation details between themselves.
2. It’s now standard in this space to have separate people audit and develop contracts. We can expect contract developers to also have a very deep intimate understanding of the security concerns for their contracts, but we find it still essential to bring in auditors to take a fresh look because a security focused team that specializes in auditing  can still add value. They’ve seen many more examples of how mistakes happen. Also, it can be easy to overlook subtle issues in something you’ve been working on for a while. What you intend the code to do can easily be confused with what the code actually does and developers are holding these intentions in their mind more strongly than external auditors.
3. I agree that it would be onerous to expect EIP authors to fund the auditing for protocol amendments. It’s hard to even source the talent, let alone pay for it. My expectation would be that the auditing would be funded by the same sources that fund client teams. We also don’t expect EIP authors to fund the implementations of their protocol amendments to all clients, though we’re happy when they submit patches. If auditing is a best practice for contract amendments that effect only one project, why shouldn’t it be the best practice for protocol amendments that risk effecting the whole network?

---

**potuz** (2024-04-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mrsilly/48/12254_2.png) Liraz Siri:

> It seems somewhat unsafe to rely on the ability and willingness of individual contributors like Yoav to highlight issues with a proposal while also relying on the ability of others on that call to evaluate those arguments right before its brought to a vote.

This does resonate with me. It seemed weird that this discussion wasn’t really closed **before** the call. Specially given that Yoav had already highlighted this issue in the previous ACDE, and this issue was discussed minimally on Discord after that ACDE 2 weeks ago. I am far from being an expert or even knowledgeable on the topic, but from the little I saw in the discussions in Discord I didn’t see an actual reply to the DOS of blob transaction invalidation being cheap to carry with 3074.

---

**MrSilly** (2024-04-15):

It’s just what you would expect if the ACDE is a formality and the meat of the discussion happens elsewhere between the client teams in private, without other stakeholders or pesky critics around. The way we’re doing things now, they’re the only stakeholder that has a vote anyway. I think this has to change.

---

**MrSilly** (2024-04-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Questions: where do you think this should be done? Some people have done it on AllCoreDevs, for example, but it doesn’t get written in the EIP. Also worth noting that the EIP process is currently open to anonymous submitters, so it may not always be possible. It is worth noting the tradeoff there.
>
>
> Also curious what you think is the “bar” for conflict?

Wouldn’t it be a good idea to have a conflicts of interest section in the EIP itself? I’d also have a winners and losers section discussing second order effects of the proposal on different players in the ecosystem.

IMHO, bar for conflict of interest would be is the company you work for stands to win more than other network participants. If it is on the winning side of this, the community should take that into account


*(29 more replies not shown)*

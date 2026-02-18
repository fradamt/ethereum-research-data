---
source: magicians
topic_id: 26433
title: Ethereum Fund Recovery Protocol (EFRP)
author: Cova
date: "2025-11-05"
category: Uncategorized
tags: [governance]
url: https://ethereum-magicians.org/t/ethereum-fund-recovery-protocol-efrp/26433
views: 1411
likes: 101
posts_count: 26
---

# Ethereum Fund Recovery Protocol (EFRP)

My apologies for the long post, I’ve hidden part of the post beneath a spoiler tag in the middle. Additionally this text is available in a word format which is considerably easier to read. You can find the document and read it online here: [EFRP](https://drive.proton.me/urls/RWK33JBCS8#VbB0frZ4mzPN)

Also you’l find an Executive summary right after the introduction. The full proposal text starts a little over halfway under the large header **Ethereum Fund Recovery Protocol**

##### Introduction

Self-custody and the complete control it offers users is one of crypto’s greatest strengths. However it also comes at great risk to the individual. One must practice strict crypto due diligence in order to avoid losing funds. Users must keep their private keys safe and secure, preventing both loss and theft, having solid cyber security/awareness is paramount. Additionally users need to be very meticulous when transferring funds, a failed copy paste, typo or even deliberate scam can cause funds to be sent to the wrong address which usually means they are lost forever.

When dealing with smart contracts on the Ethereum network additional smart contract risk comes into play. When a smart contract unexpectedly malfunctions due to an unforeseen interaction/programming error it is the user who risks losing their funds. Since it cannot be expected from users to read/inspect the code of any smart contract it is up to developers to adhere to the highest standards when coding smart contracts. However since developers are only humans mistakes have been and will be made again.

Currently when a catastrophic error does inevitably occur there is no recourse to salvage lost funds and it is the individuals interacting with the smart contract who pay the price.

This additional risk increases the barrier for adoption of smart contract ecosystems like Ethereum and often results in great personal loss. Our aim is to develop an Ethereum Fund Recovery Protocol (EFRP) to mitigate these risks and lower the barriers to adoption of the Ethereum blockchain for regular people and institutions. A single major incident with an institutional user might prevent any further adoption of Ethereum and open the field for other blockchains to fill the gap, which such an incident would create.

The EFRP aims to create a decentralized mechanism by which users who have lost/might lose funds to smart contract malfunction/bugs can regain access to their funds without interfering or sacrificing the immutability of the Ethereum blockchain.

##### Executive Summary

**Ethereum Fund Recovery Protocol (EFRP)** proposes a fair, transparent, and decentralized mechanism to assist users who have lost access to their ETH due to smart contract bugs or accidental contract inaccessibility—without resorting to contentious hard forks or centralized decision-making.

Across the Ethereum ecosystem, hundreds of thousands of ETH remain permanently compromised due to unforeseen technical failures, including smart contract vulnerabilities, misuse of the SELFDESTRUCT opcode, and poorly designed upgrade patterns. These issues have impacted a wide array of users—from individuals to DAOs to ICO projects—revealing systemic gaps in safety.

We hope this proposal can redress mechanisms within Ethereum’s current framework reassuring users (retail and institutional) by diminishing smart contract malfunction risk.

**Key Features of the EFRP:**

**sETH Token Mechanism:** Eligible users receive a 1:1 token (sETH) that represents their inaccessible ETH. Over time, sETH is redeemed for real ETH via redirected base fees (from EIP-1559), while the corresponding locked ETH is permanently burned and remains inaccessible.

**Strict Eligibility Criteria:** Incidents caused by verifiable smart contract bugs are eligible. Proof of ownership through private key signatures is mandatory.

**Governance via a Technical DAO (The Council):** A decentralized 15-member council of Ethereum experts reviews each case in private, ensuring consistent and unbiased application of rules. Cases require cryptographic verification and full transparency.

**No Hard Forks or Protocol Changes Required:** The system maintains Ethereum’s core principle of immutability. The recovery mechanism operates independently of Ethereum protocol changes and consensus rules. It functions entirely through smart contracts and community governance without altering the core Ethereum protocol.

**Transparent, Publicly Auditable Operations:** All Council decisions, compensation, and sETH distributions are recorded on-chain for full community scrutiny.

**Fully respects immutability of the ETH blockchain:** The EFRP does not require any past transactions to be undone or altering any contract that exists on the blockchain thereby fully respecting immutability.

**Benefits:**

Lowers barriers of adoption for ETH based smart contracts by diminishing smart contract malfunction risk for individual and institutional users.

Respects immutability by burning inaccessible ETH

Provides relief to users affected by smart contract flaws, not user error

Prevents ad-hoc recovery attempts that fragment community consensus

Establishes a precedent for responsible governance of smart contract risk

Ethereum Fund Recovery Protocol is a decentralized, rule-based system of accountability and fairness. It preserves economic neutrality while extending Ethereum’s resilience. This proposal seeks community feedback and support to shape a future where contract safety and immutability can coexist.

# Ethereum Fund Recovery Protocol Context

Disclaimer: We are small group of individual early ETH adopters, that helped grow the protocol at its inception who are united by a common personal tragedy in the “Parity wallet bug” that occurred on November 6th 2017. We are not affiliated with Parity in any shape or form nor have we been in direct contact with them. We are however all stakeholders in this event that has resulted in us losing access to our ETH for over 7 years.

We are undertaking this endeavor not to demand or claim anything from either Parity, ETH developers or the ETH community at large. It is our hope that we can have a public discussion about possible solutions for our situation, not just for ourselves but also for others who have found themselves in a similar unfortunate situation and for possible future situations that may occur.

We do not want a contentious EIP, we do not want to create drama or divisiveness within the ETH community, we do not want a simple bailout just for ourselves. What we do want is to have a public discourse after all these years about our situation and others like it to assess if there is a way we as a community can come together and create a possible solution to strengthen the ETH protocol. Should there be an agreed way forward then we view this as strengthening the ETH protocol as a whole and providing an opportunity to end the discussion if such a mechanism should exist. Additionally we believe that such a mechanism could greatly assist adoption of the ETH blockchain by significantly lowering smart contract risk to individual and institutional users.

## The context and controversy

The topic of fund recovery and hard forking is incredibly sensitive within the ETH community and for good reason. The nature of fund recovery, especially when performed via a hard fork, but also to a lesser degree a soft fork, infringes on one of the most important fundamental aspects of the blockchain itself, immutability. Ethereum went through its most existential crisis to date over the DAO Hack and subsequent hard-fork that occurred on June 17, 2016.

*I’ve hidden more context beneath this spoiler tag.*

**
Historical Context**

## The DAO hack

In April 2016 in Ethereum’s early days an ambitious project was launched simply named the DAO. The project was a first of its kind and saw a massive influx of ETH holders invest their ETH into this exciting new project, within 28 days the crowd sale raised around 11.5 million ETH. Nearly 14% of all ETH tokens issued at the time. Unfortunately despite several security concerns raised in May a hacker exploited vulnerabilities in the DAO smart contract. On June 17th the DAO contract was drained of 3.6 million ETH to a sub contract controlled by the hacker where they couldn’t be moved from for 34 days. After this holding period the attacker could have withdrawn the ETH completely.

In the weeks that followed Ethereum went through an existential crisis over how to handle the situation at hand. Eventually Ethereum hard forked to move the DAO funds to a recovery address where DAO investors could swap their DAO tokens back to ETH. The controversy cannot be understated, to this day there are news articles about what happened and both proponents and opponents still have discussions about whether the right call was made.

A minority of ETH users continued to support the original non forked chain which spawned the birth of Ethereum Classic (ETC). To this day ETC exists and while only valued at about 1% of the current ETH network it shows how contentious this hard fork was and still is.

The solution to the DAO hack was EIP-779 and this was implemented as an Ethereum hard fork. This was decided at a period before any formal Ethereum governance structure existed early in Ethereum’s development. The system used was community debate and carbonvoting. Carbonvoting required Ethereum to be sent to a specific address to express their stance on the proposal (pro fork or anti fork). Whilst there was strong support for the fork (87% in favor) there was discussion surrounding the limitations of the vote including limited participation and wealth-based influence. Nonetheless the split acted as a catalyst for governance innovation on the Ethereum network leading to future developments like on-chain governance and Decentralised Autonomous Organisations with more secure frameworks.

Having been a part of the ETH community at the time and living through it ourselves we are also still conflicted about the situation. We do feel some of the controversy was made worse by certain blockchain communities being hostile towards Ethereum and fanning the flames so to speak, while jumping on the bandwagon to damage Ethereum. On the other hand, not acting would have led to an enormous amount of people within the ETH community losing their investment and an unknown black hat hacker gaining a significant stake in the ETH network. Intervention was maybe the lesser of two evils, and undoubtedly resulted in improved governance frameworks on the network, the trauma however of this contentious hard fork still lives on.

## The Parity wallet hack and freeze

Roughly one year later Ethereum had its second largest high profile hack/bug. On July 19, 2017 a user accidently triggered a vulnerability that was found in the Parity Wallet 1.5 which was released on January 19, 2017. The vulnerability was only in Parity’s “enhanced” multi-sig contract.

An unknown hacker moved quickly and used the vulnerability to hack 3 multisig wallets for about 153,000 ETH belonging to three ETH based projects. Affected were Swarm City (44,055 ETH), Edgeless (26,793 ETH) and Æternity (82,189 ETH). Luckily due to these projects quickly sounding the alarm a group of White Hat hackers from the ETH development community managed to exploit the same vulnerability and drain all other vulnerable multi-sig wallets. This swift action resulted in them saving about 377,000 ETH which were returned by the group to their rightful owners.

Parity was also made aware and put out an emergency message the night of July 19th. They urged everyone who still had funds in the parity multi-sig wallet 1.5 or higher to immediately move their funds to a secure address. The following day the 20th of July Parity released an update to their wallet software. Quote: *“UPDATE (20/07/17, 00:26 CEST): Multi-sig wallets created in Parity Wallet after 19/07/17 23:14:56 CEST are secure.”*

Unfortunately we know what happened after this. Three months after the Parity hack and emergency contract re-deployment another incident occurred. An anonymous user found an uninitialized wallet related to Parity and initialized it thereby making themselves the sole owner. They then executed the kill function (Opcode: SELFDESTRUCT) and deleted the wallet from existence. This wallet was the library upon which all parity multi-sig wallets created since 20th of July 2017 relied upon to function. The result, all these wallets lost their functionality thereby effectively freezing the ETH stored within them. A total of 513,774 ETH was frozen and remains inaccessible.

## Parity

Understandably Parity has received a ton of criticism, animosity and even hate from the community since the multi-sig wallet hack and subsequent bug/freeze. Seeing as the coding mistakes were obvious in hindsight this is understandable but everything is always easy in hindsight. We also feel that the way they subsequently handled the situation after it occurred was terrible. They should have come forward to the community straight away in an open transparent manner to have a public discourse about the most appropriate way to handle the situation. Rather than forcefully proposing EIPs and seemingly attempting to push them through without community consensus, they should have engaged in open discourse with the broader community, respecting all voices and opinions.

However, despite being direct victims of the wallet freeze we do want to break a lance for Parity.

Parity was founded by Gavin Wood who was one of the co-founders of Ethereum. At the time he willingly split off from the foundation he helped to create in order to reduce the foundations burn rate and found Parity. The aim to establish Parity was to keep supporting/building Ethereum and they have done so since the beginning.

Any developer who has worked with Ethereum for a long time will note Parity’s early contributions as significant and critical, tech stack substrate, ewasm smart contracts, light client etc. The Parity Ethereum code base had been running for more than 2 years to support the Ethereum network all free of charge and all open source.

Most notably the Parity client single handedly kept the Ethereum network up and running during the DoS spam attacks that occurred during DevCon 2 in Shanghai. It’s importance cannot be understated and in general the Parity client was loved and used by many in the Ethereum community.

While being a relatively small group with limited funds developing free, open-source software for Ethereum, Parity has, despite their best efforts, made unfortunate and costly mistakes that have resulted in significant losses of ETH for others.

## The victims

We think it’s really important to get a very common misconception out of the way here. There seem to be a lot of people who think that Parity themselves were the biggest victim of the wallet freeze. Subsequently a lot of people feel it is the price they pay for their own coding mistakes.

Parity the company nor the individuals working for Parity did not lose a single ETH themselves.

Any solution to this problem would not bail out Parity or any individual who worked at Parity. We are talking about 598 wallets which are impacted. Of these wallets 16 belong to ICO’s most notably Polkadot (306,276 ETH) and ICONOMI (114,939) for a total of 474,830 ETH and an additional 38,944 ETH belonging to individual wallets.

Now many will say that Parity = Polkadot but that is definitely incorrect. Yes, while some people are involved with both Parity and Polkadot they are distinctly not the same entity. The funds that were lost were not funds from the company Parity who invested in Polkadot, instead they were funds from individual ETH investors that choose to invest in a new blockchain.

It is these individual investors who are the real victims; it was ultimately their ETH that was compromised. It is the same case for ICONOMI and the other ICO’s. Due to the freeze, their investments lost significant value as they missed a large portion of ICO-funded treasuries. Even worse, some ICOs lost all their funds and collapsed, leaving investors completely deprived of their investments.

Ultimately neither Parity nor the individuals behind Parity lost anything. It was individual ICO investors or unlucky individuals that used the Parity multi sig wallet that lost their ETH and paid the price for Parity’s coding mistake.

## Crypto due diligence

Another frequently repeated criticism concerns crypto due diligence. Many argue that using the Parity wallet reflected poor due diligence, especially since the multi-signature wallet had already been hacked a few months earlier. Therefore, some believe the victims have no one but themselves to blame. But is that really the case?

First of all it assumes that there were plenty of other wallet storage options, however there were in fact only a handful of clients at the time, with the 2 biggest by far being Geth and Parity.

At the time the parity wallet accounted for approximately 1/4 to 1/3 of all Ethereum storage wallets being used, being the second most used wallet after Geth. If this bug also affected the regular Parity wallet instead of only the multi-sig would all those additional victims also have deserved it too due to lack of due diligence? The irony here is that multi-sig wallets are considered one of the safest options, especially for shared custody or institutional use.

By 2017, Parity Technologies had a reputation as a leader in Ethereum infrastructure, thanks to its high-performance client written in Rust—a language valued for its memory safety and efficiency. For years, Parity’s client had been battle-tested under real-world conditions, earning widespread adoption among enterprises and developers. Its stability and scalability stood in stark contrast to Geth, Ethereum’s dominant client at the time, which struggled with memory leaks and outages during network stress tests like DoS/spam attacks. Parity’s reliability was no accident: it was a mature, purpose-built system that had evolved over years of rigorous optimization, not an experimental project.

However, this reputation masked a critical vulnerability elsewhere in Parity’s ecosystem: its smart contracts. While the core client code was robust, the multi-signature wallet contracts Parity offered as optional tools lacked the same rigor. At the time, Ethereum’s ecosystem was still maturing, and practices like comprehensive audits and formal verification—now industry standards—were inconsistently applied. This gap proved catastrophic when flaws in Parity’s contract code led to two high-profile incidents in 2017, freezing and draining millions of dollars in ETH. The disconnect between the client’s reliability and the contracts’ fragility underscored a broader lesson: even proven infrastructure providers are not immune to risks in adjacent systems, especially in a rapidly evolving technological landscape.

The question of Crypto due diligence is in fact a challenging one. Let’s be clear it should certainly entail keeping your private keys secured, not sending funds to the wrong address, verifying what crypto to invest in, diligent internet safety to avoid getting hacked/fished. However, how much responsibility should fall on users vs. developers/ecosystems in a trust-minimized but highly technical environment? Individual users cannot realistically be expected to audit the code of major clients like Parity (or even smart contracts they interact with) as even experts struggle with this.

The logical conclusion is that the ETH lost to Parity’s bugs wasn’t purely “bad luck” it was a failure of processes in an immature system.

A lack of industry-wide safety standards.

Overreliance on reputational heuristics (“Parity = Gavin Wood = safe”).

Poorly designed contract architecture (e.g., shared libraries with no recovery mechanisms).

Today, such a failure would still be possible, but much less likely. The ecosystem now prioritizes audits, formal verification, and defensive coding patterns (e.g., OpenZeppelin standards).

Blaming users for not auditing Parity’s code is unreasonable. Blaming *only* Parity oversimplifies the problem. The losses were a symptom of a young ecosystem learning through catastrophic failures which is a pattern seen in many emerging technologies. It is highly likely if today’s OpenZepplin’s standards had been used the Parity freeze would not have occurred. It is also true that these standards evolved due to incidents just like the Parity wallet freeze.

However such incidents contribute to the barrier of adoption facing a new and emerging ecosystem like Ethereum. If there is no recourse for individual users when developers make such critical mistakes how can we expect them to adopt smart contracts and increase adoption? Since it is clearly impossible for individual users to verify smart contract code themselves and obviously we don’t want to hold developers financially responsible for unexpected smart contract malfunctions (who in their right mind would keep developing if the risk was that high?) a recovery mechanism is needed.

## Moral obligation

Currently within the Ethereum ecosystem there essentially only exists governance by majority decision. While this creates an environment of strong cooperation between high level participants who help program and design the ecosystem it can drown out individual voices. Although the DAO hack was an outlier due to its sheer size of affected users, in general users affected by smart contract bugs/malfunctions are essentially always a small affected minority. There is no constitution or court that this minority can appeal to in case their legitimate ownership of ETH is compromised.

An decentralized recovery mechanism could help protect the rights of individual users and institutions that have been affected by unfortunate smart contract malfunctions. In the case of the Parity wallet freeze it is a small group of early adopters whose contribution helped grow Ethereum in its early days who now depend on the late unaffected minority to help them regain access to their funds. Do we not have a moral obligation to ensure everyone’s legitimate ownership of their own ETH is safeguarded without having to rely on a large unaffected majority to decide on the fate of the small affected minority?

The reality is that if 60% of ETH users were affected by the wallet freeze an intervention would have happened a long time ago. Yet due to the affected users being a small minority they are left to dry and have lost access to their legitimate funds for over 7 years. This is a form of two-tier justice that is highly undesirable

There is a bittersweet irony here where one of the core fundamentals of blockchain is complete ownership over your own funds. No central authority can take your funds away from you, freeze them or prevent you from sending them anywhere. Yet they can be compromised when interacting with a legitimate smart contract causing you to lose complete control and the only recourse is to appeal to a large unaffected majority for help.

## Considerations

From previous discussions it is very clear that any solution should be a solution for all ETH compromised not just those in the Parity wallet freeze. We strongly agree with this sentiment, so the aim is to establish a general Ethereum Fund Recovery Protocol (EFRP) that is open to anyone no matter how big or how small, no matter how well or ill connected they are.

One of the problems with trying to establish a technical solution, for example, a protocol upgrade (let’s say a general protocol smart contract revival EIP to restore Parity wallet functionality), is the potential for a whole slew of unintended side effects on other contracts that had not been taken into consideration. On top of that, such a solution would still only resolve lost ETH due to those specific circumstances (in the case of Parity, a killed contract) and does not solve the situation of ETH compromised in different ways. So, a general protocol upgrade (like the ability to revive killed contracts) seems out of the question as it is too risky, too specific and is generally unwanted. Protocol upgrades should be driven by systemic improvements and rigorously evaluated through Ethereum’s established EIP framework, rather than tailored to retroactively address isolated failures like compromised funds due to smart contract malfunctions.

Although specific cases like the Parity wallet freeze might trigger discussions about certain parts of the ETH protocol (like the Pragmatic destruction of SELFDESTRUCT, quote: “The only opcode that breaks the code immutability invariant and indeed, was responsible for the demise of the Parity multisig is… SELFDESTRUCT.”) and eventually lead to protocol upgrades. Discussions regarding protocol upgrades should be held on their own, not in light of ETH recovery. Protocol upgrades should not be mixed or burdened by the discussion regarding specific ETH recoveries. Rather ETH recovery should be discussed entirely on its own in isolation of protocol upgrades.

## Potential Solution

To safeguard Ethereum’s future, solutions must prioritize *proactive resilience* over reactive fixes. This means embedding safeguards into the protocol’s design while rigorously upholding immutability and decentralization.

If protocol upgrades are not possible to release individually compromised ETH incidents, where the issue is related to smart contract code error rather than at the Ethereum protocol level, how can they be recovered? The most obvious answer is also highly contentious, and this is a hard fork through a form of governance. However, there seems to be a very strong opposition to any hard forks to help release ETH in lost contracts. The concern is centered around the breach of immutability of the chain and that it will set a dangerous precedent that will lead to endless hardforks. Also there is fear this will lead to more centralization and pressure from outside of the ETH community to hard fork based on the whims of the powers that be. The opposition seems not necessarily against helping those with ETH that becomes compromised but against using hard forks to do so. Clearly there are good arguments against using hard forks. So how can we still help those with compromised ETH without using hard forks or protocol upgrades to regain lost ETH?

An alternative could be to create and distribute a new “Saved ETH” recovery token, let’s call it sETH, to those affected. This token is a 1 : 1 relation to the compromised ETH. When successfully calling upon the Ethereum Fund Recovery Protocol (abbreviated EFRP) those calling for help accept sETH instead of their compromised ETH and their original ETH is to be forever burned afterwards.

The point of the sETH token is that it will slowly be burned and replaced with actual ETH, we propose to use the ETH base fee that is currently being burned since EIP 1559 for this purpose. So over time those holding sETH will slowly see their sETH burned and replaced with actual ETH thereby making them whole again. If no sETH exists the base fee will completely be burned exactly as is currently the case.

Once sETH is accepted the original ETH that is currently compromised is forever burned so despite the base fee being temporarily distributed to sETH holders an equivalent amount of compromised ETH will be burned in advance. There is a degree of economic logic to this, in that compromised ETH will be permanently burnt completely removing it from the ecosystem therefore the actual ETH burn rate will not be affected and there will be 0 inflation because of the EFRP.

We believe that such a recovery protocol could see thousands of users ultimately regain access to their compromised ETH without hard forking for every instance of recovery. The core principle of the protocol is ownership over accessibility.

Normally holding the private key demonstrates both ownership and accessibility on the blockchain. The protocol is designed for those fringe cases where users still hold the private key and thereby can definitively prove ownership but somehow have lost accessibility to the funds in question.

Immutability is often heralded as the main reason any form of ETH fund recovery cannot be done through a hard fork as this would infringe upon this basic principle of the Ethereum blockchain. So our proposal is a way to move forward to still help out the thousands of users who currently have ETH tokens stuck in limbo and those in the future who may face similar issues without relying on hard forks to do so. This protocol would be open to anyone no matter how large or small or how well connected.

We believe that the EFRP would lower the smart contract malfunction risk for individual users thereby significantly lowering the barrier to adoption of the Ethereum ecosystem. Additionally, having an adequate decentralized resilient recovery mechanism in case the inevitable happens will strengthen institutional confidence to pick the Ethereum ecosystem over more centralized competitors. The EFRP would be a big step towards solving the question of dealing with unintended smart contract interactions without resorting to rollbacks or centralized code interventions that damage immutability.

# Economic logic

Currently a significant amount of ETH exists which is compromised, the locked Parity multi sig is a prime example but there are others. These ETH exist on the blockchain like any other ETH, they are not burned but inaccessible. Our proposal would allow the owners of these ETH to self-burn these ETH forever and accept sETH as compensation through the EFRP.

The economic result of this action will be a temporary increase in ETH burn rate, before sETH is distributed the original stuck ETH is burned up front. Over time the sETH will be burned while it is replaced with the base fee currently burned since EIP 1559. When all sETH is burned the base fee will be burned exactly as is done currently. The net effect on Ethereum inflation will be 0 as sETH is only generated by burning an equal amount of ETH in advance through the EFRP.

[![Flowchart sETH burn](https://ethereum-magicians.org/uploads/default/optimized/3X/1/6/1651f6879fdfa9a4f48f503a838e5fcf09ad7027_2_690x71.png)Flowchart sETH burn3080×320 48.3 KB](https://ethereum-magicians.org/uploads/default/1651f6879fdfa9a4f48f503a838e5fcf09ad7027)

***Since the text was to long the actual proposal follows in the first post.***

## Replies

**Cova** (2025-11-05):

# Ethereum Fund Recovery Protocol

The protocol consists of an exact set of principles/conditions/tests, these define in which specific cases a recovery is valid and saved ETH (sETH) can be distributed. These principles/conditions apply to all cases equally and are to ensure immutably, decentralization, transparency, accessibility and anonymity.

The protocol consists of 3 phases each with its own exact set of principles/conditions/tests.

1. Application
2. Assessment
3. Resolution

[![Flowchart EFRP](https://ethereum-magicians.org/uploads/default/optimized/3X/9/5/959823487c4e98a6fbf0a51363947afcc1b3a293_2_217x500.png)Flowchart EFRP979×2251 105 KB](https://ethereum-magicians.org/uploads/default/959823487c4e98a6fbf0a51363947afcc1b3a293)

## Phase one Application

The application phase sets out how to apply for the Ethereum Fund Recovery Protocol.

Firstly in order to request recovery stakeholders should post a public post on the Ethereum Magicians or a similar public message board requesting recovery. They can do so through anonymous accounts but they should link a cryptographically verifiable signed message with their public key related to the wallet which has funds stuck.

The message they should sign with their private key should be something along the lines of “requesting ETH recovery for funds stuck in contract XXXXX”. The purpose is for affected users to register their claims by providing cryptographic proof of ownership for compromised funds.

Ideally but not a requirement the stakeholder(s) posting the request already post what happened and which funds are stuck. Members of the Council DAO will regularly check the forum for new requests. If the cryptographically signed message requesting recovery is verified correctly on the blockchain by one of the Council members the request is deemed valid and the recovery protocol will move to phase two. Every case will be assigned a case number that has a chronological numeric order to them. Cases will be dealt with chronologically.

Any fund recovery can only be requested by signing a public cryptographically verifiable message with the corresponding private key for the wallet in question. So if the private key is lost no recovery is ever possible.

## Phase two Assessment

In this stage the case will be reviewed based on 4 core principles/conditions.

**Ownership over accessibility**

In any request to help restore compromised funds it should be absolutely clear without a shadow of a doubt which wallet owns which funds that are stuck. In cases where this is not 100% clear recovery cannot be done. This has to be cryptographically verifiable on chain for everyone to see.

**Funds are stuck through unintended/unforeseen smart contract interaction, coding mistake or bug**

Upon examination it should be crystal clear that the funds are stuck due to some unforeseen incident which was not the original intention of the contract. For example funds that were intended to be burned disqualify.

**Recovery only possible through hard fork**

Funds only qualify for the EFRP which cannot be saved by any other means than a hard fork. If any other means are possible those should be pursued instead.

**2 year minimum time limit**

Funds requesting recovery have to be stuck for a minimum of 2 years before they can apply for recovery. This means the compromised funds have not been moved for at least 2 years. Likewise if a former request to restore has been done but was rejected a new 2 year time limit applies from the date of rejection before a reapplication to recover can be done.

#### “The council” DAO

In order to ensure the principles/conditions are applied correctly and equally to all we suggest an independent DAO is formed called “the Council”. This council tests the cases brought before it and if a case is deemed valid it can distribute sETH to those affected. It is Important that every step of this protocol and every action of the DAO are public, transparent and verifiable on the blockchain for everyone to see on top of that decentralization is important.

The council should consist of 15 persons, these are public positions for a maximum of 5 years, after someone steps down from their position or their 5 year tenure is up they cannot reapply for a minimum of 5 years.

We envision anyone can publicly apply to be in the council but preference should be given to those that hold a decent amount of knowledge about Ethereum smart contract programming. The people on the council should have enough technical know-how that they can accurately assess whether a case presented to them qualifies correctly on the principles/conditions outlined in the protocol. The original council should be formed through public applications and by public discourse. After the council is formed whenever new council members are needed they can publicly apply, if there are no major objections from the public the council itself will vote whether the application is accepted or not. The council can also vote to remove council members, any council member can propose a vote to remove another council member. If a large majority of 10 out of 15 councilors are in favor the vote passes and the council member in question is removed.

##### Council compensation

We do not expect councilors to work for free and they should be able to bill the hours they work for the council according to industry standards. In order to fund the council anyone on the Ethereum blockchain can donate to the public council compensation address. Councilors can then receive compensation for the hours they put in by billing the contract which also acts as a multisig. If there are no funds in the contract any work done by the council is suspended until the council wallet is funded again. The council is seen as a public good and it is up to all of us participants of the Ethereum blockchain to fund it if we feel this public good is worth funding. The compensation for hours put into council work will be set by the council internally based on industry standards. They are free to regulate this amongst themselves.

##### Voting

The council smart contract will be created in which there is a token for every councilor. When a case is presented to the council 5 of them will be chosen randomly from the 15 total councilors through the smart contract. Which councilor was chosen remains hidden for the public and other councilors. Every chosen councilor then tests the presented case against the principles/conditions on their own and in private. After they are finished they can give one of 3 signals; positive, negative and neutral. A positive signal means the councilor deems the case at hand qualifies on all aforementioned principles/conditions. A negative signal means a case does not qualify on 1 or multiple aforementioned principles/conditions. A neutral signal means a councilor is unsure about 1 or multiple principles/conditions.

##### Outcome

After all 5 signals have been cast they are publicized through the smart contract and which councilors gave which signals are revealed. Councilors can give additional reasoning for their signals but are not required to do so.

If there are 3 or more positive signals a case qualifies for recovery according to the council and their advice is to enact recovery and distribute sETH. If there are 3 or more negative signals a case does not qualify according to the council and their advice is to not enact recovery. If no positive or negative majority is achieved due to neutral votes the case will be presented again to the council leading to once more 5 councilors being randomly assigned by the smart contract. If this second round also leads to no positive or negative majority the case is treated as if there is a negative majority.

If a negative majority is the outcome the advice is to enact no recovery and the 2 year timer to apply for the recovery protocol resets. Stakeholders are free to discuss why the advice was negative but cannot reapply for recovery for another 2 years.

## Phase three resolution

When a positive signal is given the council will distribute sETH to those who have requested it. The wallets in question will sign another signed message with their private key specifying a new ETH wallet address where they would like to receive the sETH. They will then burn their original ETH before receiving the sETH.

##### Burning the original eth

Burning the original ETH is tricky since the funds are currently inaccessible. We propose 3 different ideas on how to ensure they will be burned forever.

1. Transferring ownership to the Council DAO

The first idea is to have the applicant transfer ownership aka the private key over to the Council DAO. If the ETH ever becomes accessible due to some unforeseen update to the ETH chain in the future the Council DAO will use the private key to access the unlocked funds and send them to the burn address. It is very unlikely that this will ever be needed but safeguards the funds being burned forever.

1. Pre-signed transaction

Similarly to proposal one but perhaps more difficult due to the complex and diverse nature of the contracts in which the funds are stuck would be to have the applicant sign 1 or multiple pre-signed transactions transferring the funds to the burn address. In case the ETH ever becomes available again due to some future hard fork the Council or anyone else for that matter could broadcast the pre-signed transactions sending the funds to the burn address thereby ensuring the funds are burned forever.

1. Creating a new OPCODE

Alternatively creating a new OPCODE that allows one to self-destruct a private key could be created. This could be a possible replacement for the OPCODE SELFDESTRUCT by allowing wallet owners to self-destruct their own private key without deleting contract data from the blockchain. After destroying the private key all funds associated with the wallet in question are forever burned even if they somehow become accessible again in the future, without a working private key they will never be able to be moved thus burning the funds forever.

##### seth distribution

After the funds have been burned the Council will distribute sETH to the newly designed wallet address. In order to distribute sETH a large majority of 10 out of the 15 council members need to sign the transaction to distribute it. This is an additional safeguard to prevent a small number of council members who have gone rogue to distribute sETH without just reason. Of course all of this is completely transparent and verifiable for anyone on the blockchain to see.

Wallets that did not request recovery but are stakeholders in a contract that has already successfully applied for recovery by other stakeholders can always do so at a later date. In such a situation their case will be handled with priority over other pending cases since resolution should be fast.

When sETH tokens are in existence the base fee that is currently burned will instead be collected in the council contract. The first of the month or every X number of blocks the collected ETH will be automatically distributed to all the addresses holding sETH. ETH will be distributed pro rato so if 100 ETH is distributed and there are currently 1000 sETH tokens in existence every holder will receive 10% of their sETH in ETH.

The amount of ETH received automatically burns an equivalent sETH amount on a 1:1 basis. Slowly but surely all sETH in existence should thus be burned. When no sETH exists all ETH remaining in the contract will be burned. When no sETH exists the base fee will be burned exactly as is currently the case.

##### Disclaimer

Just to reiterate our proposal will never revert or undo transactions already made on the blockchain. Also no ETH funds will ever be forcibly transferred from one address to another. The EFRP does not infringe upon the immutability of the ETH blockchain in any way.

Fund recovery through this protocol will only ever result in currently compromised funds being burned forever and their respective owners being compensated with ETH that is currently burned as base fee.

This is not reversing or undoing past transactions but a new mechanism to recover ETH that is currently compromised without using hard forks to do so. As any sETH distributed burns an equivalent amount of ETH that is currently compromised the actual burn rate is not affected. Yet it allows us to recover compromised ETH without using hard forks.

We hope this can be a way for all of us to move forward together without leaving individual holders behind as unfortunate collateral damage from smart contract bugs either now, in the past or in the future. Bugs and coding mistakes even from some of the most experienced in the industry like Parity are inevitable in a new, young, and upcoming technology. We believe the EFRP can significantly lower the barrier to Ethereum adoption by diminishing the smart contract malfunction risk for individual users.

We truly hope to hear your opinion about our idea whether positive or negative. At the end of the day we feel an Ethereum recovery mechanism could benefit the entire ecosystem both individual and institutional users.

Please share your opinion.

---

**gcolvin** (2025-11-06):

There was an older proposal to handle some of what your proposal covers that I think foundered on the need for irregular state transitions.  You seem to have solved that problem.

---

**Cova** (2025-11-06):

Analyzing everything that has been said before it is clear that using hard forks to regain access is unwanted. This would lead to endless hard forks burdening the chain&developers, might cause unanticipated side effects and alter the chain state thereby damaging Ethereum’s immutability.

Instead we propose burning the compromised ETH forever and compensating victims by redirecting the base fees from EIP 1559 that are currently being burned.

---

**alibum** (2025-11-07):

Thanks for this. I was affected by the “Parity wallet bug”. This approach to a solution is the first which fully covers all previously mentioned concerns raised by the community. Thanks to the author. Hopefully we can find common ground to move forward here.

---

**aptyp1985-creator** (2025-11-07):

As someone affected and part of the group that supported this proposal, I believe the EFRP proposal finally presents a constructive and fair way to address the problem of frozen ETH caused by contract bugs. The idea of introducing a token as transparent compensation, based on a fully decentralized and verifiable process, aligns both with the spirit of Ethereum and the legitimate interests of the affected community. The fact that this approach works without hard forks or central interventions shows real respect for the principles of blockchain and finally gives those affected new hope. It is time for the community to seriously consider this proposal and stop ignoring our cause.

Great article [@Cova](/u/cova)

Disclaimer ![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=12):

My reply is translated from German to Englisch

---

**Azzuro** (2025-11-10):

The problem seems to be the concept of a council introduces a subjective factor while the overall expectation is to have a network based on objective and auditable rules.

The other issue is how to burn the ETH in question is case it has been transferred further or even moved to CEX or DEX etc. meanwhile (which is often the case if malicious actors using compromised smart contracts are involved).

---

**Cova** (2025-11-10):

Ideally in the future council work would be automated however currently I don’t see a way in which that is possible. So there is a degree of subjectivity however due to every case being reviewed by 5 councilors, based on objective public rules and the whole process being public & transparent the outcome should be as objective as possible.

Additionally applicants can apply again after 2 years if there is a negative outcome. This insures if there is an unfavorable degree of subjectivity in an assessment there is a chance to have a new assessment (likely with different councilors) in the future.

In general the EFRP is not applicable to stolen funds. The EFRP is only applicable to funds still in possession of the legitimate owners, they need to prove ownership when they apply for the EFRP by use of the private key.

---

**Azzuro** (2025-11-11):

Yes, I understand the idea. It is certainly better than the previous clawback concepts.

---

**Cova** (2025-11-11):

I’m happy to hear it and I agree with you that full automation would be the best possible solution. Arguably this could be done at a protocol level.

I imagine something along the lines of calling a function that automatically verifies how much ETH your address holds even if it’s inside a smart contract. If you agree that the verified amount is correct you can execute a follow up transaction. In said transaction the ETH amount is burned and you get a replacement sETH token instead. Slowly sETH is replaced by actual ETH from the base fees from EIP 1559.

Technically this seems feasible to me, I do however worry that it might cause unintended side effects. For example what if said ETH was used as collateral for a DeFi loan, suddenly the collateral would be burned and the loan would not be covered anymore. This is one of the reasons why I think currently we still need some form of human assessment to prevent outcomes like this.

---

**Azzuro** (2025-11-12):

Right, I did not even mention the option of fully automating the process since it leads to additional challenges as you’ve pointed out.

---

**kdenhartog** (2025-11-12):

I think the problem is necessary to be addressed, so by no means am I opposed. However, what is being proposed here is effectively a judicial process for Ethereum so I’d like to better understand the scope and governance of this process. Here’s a few questions I’ve got.

1. Is the scope of this intentionally only around contract bugs or would hacks also be in scope?
2. Do you expect the scope to change over time to address the problems we can’t predict today or is this intended to only solve previous issues and then be removed?
3. How do you expect the council is elected, changed, removed or what the voting and governance process is for this? For example, is it a simple majority, super majority, or unanimous decision made that allows for the reversal?
4. How do you plan to prevent prediction markets economically incentivizing the outcome of the council’s decisions?

---

**Cova** (2025-11-12):

1. The EFRP is only intended for funds that are still in possession of their respective owner but are somehow compromised and inaccessible unfortunately stolen funds do not qualify. A prerequisite is the funds have to be publicly cryptographically verifiable on chain that the funds are tied to the owner requesting recovery. So you still need to be in possession of your private key and the funds need to be tied to that private key.

As someone who’s also been the victim of a crypto theft long ago I do sincerely feel for everyone that’s gotten funds stolen however I don’t see how we could address those cases without compromising Ethereum’s immutability. From a blockchain perspective (notably not from a legal stance!) once the funds are transferred to the thief the thief is the legitimate owner. Somehow intervening and returning funds to their original owner (while a morally logical intervention) would mean you’d essentially lose immutability. This would open the door to far bigger issues. However when funds are stolen you can and in my opinion should go to the police, crypto theft is most definitely covered by real life law.

1. This is intended to address all such cases both in the past, present and future. We do not envision the EFRP changing or growing in scope. It’s intended as a small singular DAO overseeing the EFRP protocol. It’s singular and narrowly defined in it’s scope of operations and not intended to eventually scale to other subjects. The intent is for it to be a permanent small decentralized governance tool.
2. We’ve set up an outline for how this might work, however all these parameters can be changed of course. I imagine there is far more knowledge within the Ethereum community of what the best parameters are than within our small group of affected users. In the protocol we have outlined the following:
 “The original council should be formed through public applications and by public discourse. After the council is formed whenever new council members are needed they can publicly apply, if there are no major objections from the public the council itself will vote whether the application is accepted or not. The council can also vote to remove council members, any council member can propose a vote to remove another council member. If a large majority of 10 out of 15 councilors are in favor the vote passes and the council member in question is removed. “
 For every case 5 out of the 15 councilors are chosen at random, they then make their assement alone and in private. You would need a 3+ vote outcome either positive or negative to have a positive or negative outcome.

Also I would like to stress it’s not a reversal, clawback, rollback or anything of the sorts. When a positive outcome is achieved no past transactions are undone or reversed, nor is any new code inserted through a hardfork. A positive outcome leads to a new transaction done by the applicant to burn the compromised ETH. In return they get a new recovery token sETH, over time the sETH will be burned by replacing it with actual ETH that is redirected from the base fees (EIP 1559).

So the mechanism is to burn the compromised ETH and compensate victims by redirecting the base fees to make them whole again. Since they burn their original compromised ETH up front the actual burn rate is not affected and 0 inflation occurs because of the EFRP.

1. Interesting question, I don’t think it’s possible to stop prediction markets. However most cases should be fairly obvious for most people to judge whether they qualify for the EFRP or not since all information regarding them and how cases are judged is fully public. A single council member only knows their own judgment before all votes are cast so the edge they have is 20% of the actual outcome but 80% (the other council members) are also unknown to them.
 During the process the council members also do not know which other council members are assigned to a specific case so in the event of multiple corrupt council members it would be hard to exploit this advantage further. It would be possible to increase the amount of council members per case making the edge they hold even smaller. However I do not expect the EFRP to become a popular prediction market most cases will be to predictable for everyone to make it interesting to bet on.

---

**kdenhartog** (2025-11-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cova/48/16433_2.png) Cova:

> The EFRP is only intended for funds that are still in possession of their respective owner but are somehow compromised and inaccessible unfortunately stolen funds do not qualify.

Ok, while I suspect it won’t stay this way forever defining this scope as such now makes sense to keep it quite practical. If it becomes an effective measure of judicial reviews, I suspect it will either be replicated for other such options or extended. Maybe it makes sense to define a process for how the process can be extended too?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cova/48/16433_2.png) Cova:

> “The original council should be formed through public applications and by public discourse. After the council is formed whenever new council members are needed they can publicly apply, if there are no major objections from the public the council itself will vote whether the application is accepted or not. The council can also vote to remove council members, any council member can propose a vote to remove another council member. If a large majority of 10 out of 15 councilors are in favor the vote passes and the council member in question is removed. “

I think you’ll want to shift this to a 75% majority for removal. This will prevent dilution of a vote if the council adds new members. E.g. if they add a 16th, but only 10 are still needed that would make it a 62.5% majority vote for removal with one additional council member. Also, it’s not ideal to have a governance of “we reviewed ourselves and deemed we’re fine” approach. I’d suggest adding some sort of checks and balance here.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cova/48/16433_2.png) Cova:

> Also I would like to stress it’s not a reversal, clawback, rollback or anything of the sorts. When a positive outcome is achieved no past transactions are undone or reversed, nor is any new code inserted through a hardfork. A positive outcome leads to a new transaction done by the applicant to burn the compromised ETH. In return they get a new recovery token sETH, over time the sETH will be burned by replacing it with actual ETH that is redirected from the base fees (EIP 1559).

Would it be simpler to just keep an index of funds that are caught (and as such can’t be moved anyways) and then just mark them as issued against? In this way, the DAO would just keep a record of the new sETH it issues and which 1:1 backing they come from so that the original funds don’t need to be moved. Instead they’re recognized as frozen based on the audit. Then if said funds move later, some portion of sETH can be bought back from the market and burned.

In this way too, the value of the governance by the council directly sets the value of sETH. If the council does good, the value is expected to remain pegged 1:1. Otherwise, it’s diluted and in this way the market gets to act as a checks and balance against the governance council’s choices.

I think the prediction market aspect remains dull right now, but I expect it will introduce side effects into the future that are unpredictable. Especially because their choices have a direct impact on the value of sETH and indirectly on ETH and could be contentious in the future just as the DAO hardfork hack was contentious.

It’s likely something that needs to be thought through further, but unfortunately I don’t have much to contribute in the way of a solution for this.

---

**Cova** (2025-11-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> Ok, while I suspect it won’t stay this way forever defining this scope as such now makes sense to keep it quite practical. If it becomes an effective measure of judicial reviews, I suspect it will either be replicated for other such options or extended. Maybe it makes sense to define a process for how the process can be extended too?

I would say that is definitely beyond the scope of our proposal. The EFRP is intended as a limited well defined decentralized governance tool for dealing with a specific issue. The issue being ETH that has gotten stuck/compromised/frozen inside smart contracts due to a variety of reasons.

Maybe it could become an example of how to have some form of mild governance in a decentralized manner that respects Ethereum’s decentralized and immutable nature.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> think you’ll want to shift this to a 75% majority for removal. This will prevent dilution of a vote if the council adds new members. E.g. if they add a 16th, but only 10 are still needed that would make it a 62.5% majority vote for removal with one additional council member. Also, it’s not ideal to have a governance of “we reviewed ourselves and deemed we’re fine” approach. I’d suggest adding some sort of checks and balance here.

We intended to have a predetermined maximum number (the number of course is up for debate) of council members. However a percentage like 75% might be better then X out of Y to always guarantee a sufficient majority is needed.

The idea is that applicants are public and known figures from within the community (they can be anonymous similar to for example the Silviculture Society but have a public persona) and are only suitable for the role if there are no objections from anyone.

But I certainly welcome this discussion our proposal should be viewed as a first set up of how things could be done not a definitive vote yes or no proposal. I think the most important step is every step (case application criteria, council selection, assessment, outcomes, etcetc) are completely transparent and open for anyone to view and monitor. Corruption is very hard to pull of in an environment that is completely transparent and auditable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> Would it be simpler to just keep an index of funds that are caught (and as such can’t be moved anyways) and then just mark them as issued against? In this way, the DAO would just keep a record of the new sETH it issues and which 1:1 backing they come from so that the original funds don’t need to be moved. Instead they’re recognized as frozen based on the audit. Then if said funds move later, some portion of sETH can be bought back from the market and burned.
>
>
> In this way too, the value of the governance by the council directly sets the value of sETH. If the council does good, the value is expected to remain pegged 1:1. Otherwise, it’s diluted and in this way the market gets to act as a checks and balance against the governance council’s choices.
>
>
> I think the prediction market aspect remains dull right now, but I expect it will introduce side effects into the future that are unpredictable. Especially because their choices have a direct impact on the value of sETH and indirectly on ETH and could be contentious in the future just as the DAO hardfork hack was contentious.
>
>
> It’s likely something that needs to be thought through further, but unfortunately I don’t have much to contribute in the way of a solution for this.

I understand your reasoning and it would technically be a lot easier to pull off. But I do strongly prefer to actually burn the compromised funds. I think it makes for a cleaner better organized solution.

Do you think it would be very hard to implant a technical solution to actually burn the compromised funds? While the funds themselves are currently inaccessible and a regular burn by sending them to the burn address wouldn’t be possible an alternative might be. The funds are still tied to the private key so if we somehow would essentially “burn” the private key the funds are effectively burned even if due to some unforeseen protocol update in the future they’d become accessible again.

It’s important however that the burn happens from an action by the user not the Council DAO. We should never want to give anyone the power to burn funds from others so it should be an action done by the applicant to the EFRP protocol.

---

**kdenhartog** (2025-11-13):

The only thing I was thinking about for the burn was that a person may still have active assets tied to the account so private key reveal forces the user to migrate accounts first. Similarly, it’s possible a smart account just has some authorization logic in it that’s not private key based (e.g. I authorize spends with a ZkLogin credential like what Sui does [Sui Features | zkLogin](https://sui.io/zklogin)) in which case I wouldn’t have a key to burn.

---

**Cova** (2025-11-13):

Good point, some cases might have to be excluded like ZkLogin if we can’t guarantee that the compromised funds are burned.

In your opinion would such a burn feature (based around the private key rather than the actual funds) be possible from a technical perspective?

---

**Psylar** (2025-11-19):

This article is good summary of the events and EFRP  - I Accidentally Killed It: Why $17 Billion Worth of ETH is Frozen — And How Holders Are Trying to Get It Back’ [“I accidentally killed it” – Why $1.7 Billion worth of ETH is Frozen and How Holders Are Trying to Get It Back | CoinCodex](https://coincodex.com/article/76302/i-accidentally-killed-it-why-17-billion-worth-of-eth-is-frozen-and-how-holders-are-trying-to-get-it-back/)

---

**Psylar** (2025-11-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> about for the burn was that a person may still have active assets tied to the account so private key reveal forces the user to migrate accounts first. Similarly, it’s possible a smart account just has some

Ok it seems there are cases that would require a different approach if a burn is felt to be appropriate

---

**Psylar** (2025-11-19):

Thanks for posting this Cova. I was also affected by the Parity bug. This seems to be an excellent start to a possible solution.

---

**Psylar** (2025-11-21):

While fully objective systems are the ideal, the reality is that some parts of decentralised governance just can’t operate that way yet. Ethereum itself is a good example: core development decisions and Ethereum Foundation stewardship ultimately rely on a subjective, socially coordinated, “council-like” process. Decisions are shaped by discussion, expert opinion and rough consensus rather than a strict algorithm or purely on-chain mechanism. So introducing a structured council in this protocol wouldn’t be adding something unusual or foreign to the ecosystem, it would simply formalise a pattern that already exists.

It seems that what’s being proposed is a transparent, criteria-driven council intended to address a long-standing issue within the Ethereum network. If we accept that this problem exists—and if we genuinely care about the network’s long-term resilience, competitiveness, and ability to evolve—then it’s something that ultimately needs to be resolved. In an ultra-competitive environment, leaving structural weaknesses unaddressed isn’t a neutral choice; it’s a risk to the network’s future. This proposal offers a structured way to confront that problem rather than continuing to ignore it.


*(5 more replies not shown)*

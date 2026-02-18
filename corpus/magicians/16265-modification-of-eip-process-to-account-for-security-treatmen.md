---
source: magicians
topic_id: 16265
title: Modification of EIP process to account for security treatments
author: Dexaran
date: "2023-10-25"
category: Magicians > Process Improvement
tags: [erc]
url: https://ethereum-magicians.org/t/modification-of-eip-process-to-account-for-security-treatments/16265
views: 3571
likes: 21
posts_count: 26
---

# Modification of EIP process to account for security treatments

The current EIP process assumes that once an EIP reaches “final” state its text can not be modified. EIPs have a special “Security Considerations” section that is supposed to be written by the EIP author at the time EIP is submitted. Security Considerations section can not be modified after the EIP reached its “final” state which is inadequate because a security flaw can be discovered in any program/specification at any time. It is a common case where a security flaw is discovered in a software that is being in use for years.

Security Considerations section must not reach it’s ‘final’ state ever or a specific process must be designed around EIP procedure in order to enable security disclosures in any EIPs.

I would like to propose a change to the EIP process that I would recommend and get comments on the subject before submitting an EIPIP.

**1. Change the “Final EIPs are immutable” paradigm to “Abstract, Motivation, Specification and Rationale sections of final EIPs are immutable, while Security Considerations section can be updated anytime after EIP finalization”.**

Rationale: Security Considerations section sould reflect relevant info about the EIP, not only what was known to the author at the moment of writing the EIP text. If a new security flaw / consideration is worth adding to the EIP - it must be added to warn the readers.  The goal here is to keep EIP readers aware of ANY security problems associated with the EIP, not only those that the author of the EIP wanted to mention when the EIP was submitted.

**2. Write an Ethereum Security Guideline - a set of rules that an application-level standard/program must adhere to. Violation of any of the Ethereum Security Guideline principles must be considered a red flag and indicated in the Security Considerations section of the proposal upon disclosure.**

Rationale: EIP editors are not security experts, and it is unrealistic to require each EIP to be reviewed by a dedicated security expert (even though it is desirable). If we can compile a list of basic security “principles” and agree on it once - it will eliminate the need of evaluating each proposal separately by enabling EIP editors to benchmark any proposal against the Security Guideline. The Security Guideline can also be used to help the developers to make their smart-contracts more fault-tolerant. The Security Guideline should be submitted as an EIP. The Security Guideline can be superseded by a newer one should a better one be written.

**3. Update EIP-1.**

Rationale: EIP-1 must include a reference to Security Guideline and re-define the “final” status of EIPs to allow Security Considerations updates.

Any Security Consideration that wasn’t included in the original EIP text but is discovered afterwards can be proposed and added to the Security Considerations section.

Any violation of Security Guideline principles must be described once discovered and added to the Security Considerations section. It can be helpful to indicate that an EIP violates Security Guideline principles in the most visible form in order to raise the awareness of the potential implementers.

## Replies

**bumblefudge** (2023-11-01):

This would actually moving more towards the Security Review structure of W3C, but I think the workforce of W3C is substantially larger, and the people that do that review are committed about 10hrs/wk to the process yearround, i.e. their employers “pledge” 1/4 of their FTEs to this glamorous position, so I wonder about the labor footprint of this kind of formalization.

I can’t speak for the editors but I think much of the reservation here is from editors not wanting to have to be experts, and I feel like the judgment about what violates those principles (#2) is a lot of work, whether it comes from the editors or from outsiders who have to be somehow motivated/incentivized/rewarded to put in that time researching and thinkingly deeply.  Maybe this PR would get more traction if you had an auditing company behind it willing to champion it *and do it* for the first year? ![:laughing:](https://ethereum-magicians.org/images/emoji/twitter/laughing.png?v=12)

In all seriousness, I think the lightest-weight version of a solution to this problem, that did NOT put additional demands on the editors, would be to Make Informationals Great Again, and to offer some kind of link from final PR to update/addendum/“if i had it to do over again” document that comes later.  The lightest-weight version of this idea that I can imagine would be an optional frontmatter key whose value can ONLY be a single link to another EIP/ERC, no editorial text.  Maybe it could be an array or maybe you could add up to X words, like, “for updated security considerations, see ERC-XXXX”.  Thoughts welcome on a version of this you would support (particularly if you are an EIP editor), glad to open an alternate PR IFF anyone wants it

---

**Dexaran** (2023-11-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bumblefudge/48/7449_2.png) bumblefudge:

> Maybe this PR would get more traction if you had an auditing company behind it willing to champion it and do it for the first year?

Luckily I own an auditing company https://www.zoominfo.com/c/callisto/547151294

https://audits.callisto.network/audited-projects

So if it is the requirement to get it accepted - we can discuss ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**frangio** (2023-11-06):

This is not addressed in the post but I think all changes to an EIP should require approval by one of the original EIP authors.

An alternative to this proposal would be a completely separate “area” in the website for security information about EIPs, instead of keeping the current structure and simply making Security Considerations mutable. I think this would make a lot more sense for many reasons: different governance, different semantics (normative specification versus guidelines), and because over time the volume of relevant security content can become a lot more than an EIP’s own content.

---

**Mani-T** (2023-11-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> An alternative to this proposal would be a completely separate “area” in the website for security information about EIPs, instead of keeping the current structure and simply making Security Considerations mutable. I think this would make a lot more sense for many reasons: different governance, different semantics (normative specification versus guidelines), and because over time the volume of relevant security content can become a lot more than an EIP’s own content.

I agree with you. Over time, the volume of security content may grow significantly, potentially overshadowing the core EIP content.  Keeping them separate allows for better organization and scalability.

---

**Dexaran** (2023-11-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> This is not addressed in the post but I think all changes to an EIP should require approval by one of the original EIP authors.

I think it’s a terrible idea because:

1. What if an author of the EIP doesn’t maintain it or even doesn’t exist anymore? We can get EIPs that will be permanently frozen in an immutable status just because the author left them.
2. There will be conflicts of interests. An author of an EIP can refuse to approve a security disclosure in their EIP for the sake of a promotional push.

“We found a critical bug in your software.”

Author: “No.”

“Ok, we pretend its secure. Author said No”

---

**Dexaran** (2023-11-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mani-t/48/10103_2.png) Mani-T:

> Over time, the volume of security content may grow significantly, potentially overshadowing the core EIP content. Keeping them separate allows for better organization and scalability.

Whats the point of having Security Considerations section in the EIP at all then?

---

**SamWilsn** (2023-11-07):

I’ve said all of this before in other threads, so please forgive me for repeating myself.

I object to including security considerations surfaced after a proposal becomes final within the body of the proposal itself. To be clear, I *do* believe that these security considerations should be published somewhere, just not within the EIP.

My objection stems from the question of who has the authority to determine if a security disclosure is worthy of publishing. Within the EIP framework that exists today, there are two choices: authors and EIP Editors.

EIP Editors are not expected to have any technical knowledge about the proposals they oversee. Given the wide range of topics we see, it would be basically impossible to maintain any meaningful depth of expertise. Further, it’s important that the EIP process maintain credible neutrality. We don’t want to be put in a position where we could appear to make a decision for ulterior purposes, like personal gain. Choosing to (not) publish a vulnerability puts us in that position.

Authors, on the other hand, should be technical experts on their proposal, but should they be the ultimate authority on what is/isn’t a vulnerability? Once a proposal goes to final, I like to think of it as belonging to the community (where before final, it belongs to the author(s).) A contrived example here is with [ERC-223](https://eips.ethereum.org/EIPS/eip-223): the proposal as written cannot differentiate between an EOA or a counterfactual contract (i.e. `CREATE2`) that hasn’t been deployed yet; one might argue that this should be mentioned in the Security Considerations section, since it can lead to loss of tokens. While that example is relatively harmless, I can certainly envision a scenario where an author is incentivized to prevent publishing of a vulnerability to protect their financial interests.

So if authors and EIP Editors are poor choices, what can we do? I see two options:

- Publish every security disclosure without vetting, or
- Publish no security disclosures.

Personally, I prefer the latter option.

---

**Dexaran** (2023-11-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> So if authors and EIP Editors are poor choices, what can we do? I see two options:
>
>
> Publish every security disclosure without vetting, or
> Publish no security disclosures.
>
>
> Personally, I prefer the latter option.

I completely understand your point and to address this I have pt.2 in my proposal:

**2. Write an Ethereum Security Guideline - a set of rules that an application-level standard/program must adhere to. Violation of any of the Ethereum Security Guideline principles must be considered a red flag and indicated in the Security Considerations section of the proposal upon disclosure.**

So, the EIP editors will not have to decide whether to publish a vulnerability or not. Instead EIP editors will review “appeals to indicate a violation of the security guideline in a EIP” and judge whether it’s valid or not - and its a much simplier task.

This is how a vulnerability disclosure will be done:

There is a security guideline that has a set of rules.

```auto
EIP-X: Security Guideline
Every secure software must do:

1. XXX
2. YYY
3. ZZZ
```

Someone pretends that EIP-123123 violates rule 1. He builds a contract, deploys it on testnet, simulates a scenario under which we expect the contract to do XXX but it is visible in the transaction history that the contract is doing something else. If someone can assemble such a precident artificially to demonstrate how EIP-123123 violates a rule of the security guideline - then we can add it to the security considerations section.

So basically its not the EIP editors who decide whether something is a vulnerability or not, its the rules in the security guideline EIP. If we can agree on this set of rules once - we can use it afterwards. And dedicated security experts can work on the development of the security guideline EIP. This is what I propose.

---

**Dexaran** (2023-11-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> To be clear, I do believe that these security considerations should be published somewhere, just not within the EIP.

This raises the question of “what is the goal?”. We should keep in mind that we are dealing with **financial software** here. The cost of a mistake can be huge. It’s not like you get errors in your browser console and you can simply ignore most of them and be fine. **If someone makes a single mistake in our area then it means someone else will lose funds.**

There is a good illustration to what we are discussing here, a script that calculates the amount of “lost” ERC-20 tokens: [ERC-20 Losses Calculator](https://dexaran.github.io/erc20-losses/)

In 2017 there were $16K lost due to known security issue in ERC-20 standard.

In 2018 there were $1,000,000

In 2023 there are more than $90,000,000 and the amount is growing exponentially because nobody cares and we keep our users losing money

So I would say that **security must be a priority.** I don’t see any problems with having Security Considerations section in the EIP list all the security disclosures just because they all need to be placed right in front of the implementers eyes. If it helps to prevent the exploitation of **known-to-be-insecure** implementations and **save our users from losing $90,000,000** then its a reasonable decision.

---

**SamWilsn** (2023-11-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> Write an Ethereum Security Guideline

I maintain that there is no way to write a list of guidelines that can be evaluated objectively. If there was, we would’ve automated it and solved computer security once and for all.

---

**Dexaran** (2023-11-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I maintain that there is no way to write a list of guidelines that can be evaluated objectively. If there was, we would’ve automated it and solved computer security once and for all.

It’s not possible to write a “formal specification for every possible issue in computer software” I agree. But it is totally possible to write a guideline that describes 10 main principles of secure software development that if violated will inevitably result in the lost funds for the end user.

I’m not saying “we can solve all security problems with this proposal”.

I’m saying “we can prevent the most obvious issues with this proposal and save a lot of end users funds”.

---

**Dexaran** (2023-11-07):

Software security is not something new and revolutionary. It’s a well-developed area with few common well-known “standards” of what to do and what to avoid.

Software security is also not something abstract and inconsistent, like predicting the next market move. It has some strict basic rules that can be described.

If you google “Secure software development principles” and review few pages you will find out that they describe the same things.

---

**shemnon** (2023-11-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Publish every security disclosure without vetting, or
> Publish no security disclosures.

Option 2.1: let CVEs do the security disclosures.

---

**joeysantoro** (2023-11-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Option 2.1: let CVEs do the security disclosures.

Could this be done as a new ERC type called “Security” which can then be potentially backlinked to other EIPs on the website?

---

**SamWilsn** (2023-11-13):

This is similar to the approach [@Dexaran](/u/dexaran) has taken with [ethereum/EIPs#7915](https://github.com/ethereum/EIPs/pull/7915).

Publishing a new EIP listing a proposal’s flaws is more compatible with our process, for sure, but still runs afoul of my core objection: I don’t want Editors deciding whether or not to publish a security vulnerability.

So far, the best options to me are:

- We make a wiki, or
- We defer to CVEs.

---

**Dexaran** (2023-11-13):

I’m more concerned about what we should do with ERCs upon vulnerability disclosures. Right now I’m talking about application-level standards.

There can be only two viable options **if we want to prevent financial damage to Ethereum users**:

- Mark a standard as “insecure” without modifying the specification/reference implementation. Recommend using other standards in production.
- Fix the discovered vulnerability in the original ERC.

If we decide to outsource vulnerability disclosures somewhere and declare “we don’t have to deal with vulnerabilities ourselves, let vulnerable ERCs stay unchanged” then it will inevitably result in financial damage to the end users due to **KNOWN vulnerabilities**. This is not a goal to pursue in my opinion.

---

**frangio** (2023-11-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> We make a wiki

I think this is a great direction, but a pure wiki editable by anyone seems very risky for security purposes.

Something like [Discourse Post Voting](https://meta.discourse.org/t/discourse-post-voting/227808) could be a good option. Create a new category in this forum called Security Disclosures, in that category there should be a topic for every ERC, and all topics should have voting enabled. Each post can contain a security disclosure following a specific format. CVEs can be optionally linked in each post.

It should also be possible to retract an ERC if it’s found to be inherently or irreparably insecure. For this we could have a new Retracted EIP status, or the Withdrawn status could be reused. Alternatively, only the reference implementation of an ERC may be retracted.

---

**SamWilsn** (2023-11-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> It should also be possible to retract an ERC if it’s found to be inherently or irreparably insecure. For this we could have a new Retracted EIP status, or the Withdrawn status could be reused. Alternatively, only the reference implementation of an ERC may be retracted.

This still runs into my primary objection: who decides if a proposal is inherently or irreparably insecure?

---

**bumblefudge** (2023-12-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Option 2.1: let CVEs do the security disclosures.

I don’t know the degree to which you’re joking here, but a buddy of mine has been working on a cool [prototype that integrates ActivityPub into CVE reporting](https://github.com/ietf-scitt/use-cases/blob/3f10017af4cebb7d07e541c299ef277d43fb9c0d/openssf_metrics.md#activitypub-extensions-for-securitymdtxt-contact-uris) for the IETF SCITT group.  In this guy’s proposed model, CVE reporting pipelines would create “posts” (events) in the fediverse for all that follow the appropriate accounts per codebase to be notified about and interact with/comment on.  Imagine if we were having this conversation in the comments thread of an automated CVE post, hehe.

---

**shemnon** (2023-12-26):

Not joking at all.  And this workflow if it ships makes my argument a bit stronger.

I am a bit concerned about the low barrier to post a CVE, which is mostly busywork if not done through tooling like github.  But that would be a signal that someone posting the security notification thinks its worth the effort of following the CVE process.  And I am assuming there is interest and desire in the CVE community to keep it high signal so it doesn’t devolve into NNTP levels of spam.

That is what I am hoping for by offloading the decision of “what is a security issue” to another team, it is a team that has vested interest in making their signal of “this is a security threat” high.  (and then the ordinals CVE hit…)


*(5 more replies not shown)*

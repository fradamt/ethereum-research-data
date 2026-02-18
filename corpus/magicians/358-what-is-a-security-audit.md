---
source: magicians
topic_id: 358
title: What is a security audit?
author: maurelian
date: "2018-05-15"
category: Working Groups
tags: []
url: https://ethereum-magicians.org/t/what-is-a-security-audit/358
views: 2004
likes: 19
posts_count: 20
---

# What is a security audit?

The ethereum community has kind of recreated the security process, with (until recently) very little input from the pre-existing information security community. We’ve made up a lot of things up from scratch, which has resulted in a tremendous variation in the definition of an “audit”, and in what it means to audit a smart contract system.

Some questions I’d like to hear from people about:

ring an auditor to make sure there are no bugs or vulnerabilities?

- Is it an auditor’s job to pronounce a system “secure or insecure”?
- How can auditors collaborate with development teams earlier in the design and development process?
- How can the we improve on the existing incentives* in developer/auditor relationship?

ie. Audits are expensive and time consuming, so developers are incentivized to include as many features as possible in a “major release”.

---

If you’re interested in further discussion IRL follow this topic:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maurelian/48/43_2.png)
    [Proposed gathering of the Security community](https://ethereum-magicians.org/t/proposed-gathering-of-the-security-community/356) [Working Groups](/c/working-groups/11)



> I’m concerned that the need for security and correctness in smart contract engineering is being outweighed by the pressure to deliver highly complex systems to anxious ICO investors.
> Following conversations at EdCon in Toronto, there’s a clear need for a gathering specifically focused on smart contract security. Here is my best attempt at outlining what I think this event would look like, as well as my open questions.
> Goals
> To share knowledge to prevent and mitigate security risks facing smart…

## Replies

**fubuloubu** (2018-05-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maurelian/48/43_2.png) maurelian:

> Can we do better than the current “security last” approach of developing a system then hiring an auditor to make sure there are no bugs or vulnerabilities?

Yes. In my previous field (aerospace flight software) we would always have a Preliminary Design Review (PDR) and Critical Design Review (CDR).

PDR would typically be at the stage where you are planning how you would like to attack the project, with some breakdown of your goals into high level requirements, which would get reviewed in a day-long presentation showing various customers and stakeholders (FAA or other certification org). This way you can get expert feedback on your approach before you commit too many resources towards implementing it. Including security auditors at this stage would allow them to review your architecture for high-level holes (reducing the time you need to identify and change approaches) as well as getting them familiar with your project for later stages.

CDR would typically occur after a design was deemed feature-complete. This review ensures that a large panel of people (customers, QA, certification board) agree with the total approach including testing and flight demo plans before final sign off to begin the validation cycle. Security auditors are entirely fulfiing this role right now (they are expected to provide final GO/NO-GO status on the code), so I think this process should be more formalized into what the expectations are since there are many other groups of people that should understand what is happening here.

---

**fubuloubu** (2018-05-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maurelian/48/43_2.png) maurelian:

> Is it an auditor’s job to pronounce a system “secure or insecure”?

They can only provide positive confirmation that a system is NOT “insecure”. They should not be expected to prove it “secure”

---

**fubuloubu** (2018-05-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maurelian/48/43_2.png) maurelian:

> How can the we improve on the existing incentives* in developer/auditor relationship?

More modularity? Getting modules audited piecemeal?

---

**maurelian** (2018-05-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> They can only provide positive confirmation that a system is NOT “insecure”. They should not be expected to prove it “secure”

How would you describe the difference between NOT insecure and secure?

---

**fubuloubu** (2018-05-15):

I think to a security auditor “secure” means “to the best of our knowledge and the quality of our toolsets, there is nothing that is a known bug or insecure practice that we have found in the limited time we have to audit”, which is the correct definition.

To many developers, “secure” means “pretty much no bugs”.

The difference between them is that the auditor understands there are limitations to the toolsets, and how to combine them together to acheive maximum coverage of the codebase to the set of scenarios presented in the specification(s), whereas the developer thinks it is possible to formally prove that what they built is exactly what the specification said, if only they had the knowledge to be able to do so.

There is always something that you don’t know is a problem until it is, and it takes multiple tools run by multiple parties with multiple different perspectives on what the goals are in the specification to have enough layers on it to ensure it’s as robust as possible. At the end of the day, the strongest indicator of “security” is being in a malicious, open environment for an extended period of time, with a strong incentivize to attack it.

Having robust procedures around how the code is handled and ensuring you are properly pushing the envelope of the application only as far as you are willing to lose it is when next steps are involved.

---

**redsquirrel** (2018-05-16):

In my experience as an auditor, I have sometimes been involved more iteratively, rather than a big bang at the end. You need to be careful of “going native”, though. The outside perspective that an auditor brings is important, and the closer you get to the engineering process, the less “outside” you become. I think best case is to “drop in” for a couple brief sessions of feedback before the final audit.

---

**fubuloubu** (2018-05-16):

At some point you become their QA person, and you should ask for a raise!

But seriously, I think “iterative involvement” is definitely key to success. [@maurelian](/u/maurelian) keeps bringing this up, and I think setting more formal checkpoints for (serious) developers will create a stronger relationship and a deeper understanding with the auditor, which ultimately increases quality and security.

---

**drgoldberg** (2018-05-17):

Hey all, my co-founder and I wrote this blog post about our philosophy of a smart contract security audit. Hope you enjoy. Welcome any feedback. https://medium.com/@bloctrax/philosophy-of-a-smart-contract-security-audit-1e111efd28cb

---

**paulhauner** (2018-05-20):

We’re lucky to have a director who’s last job was as a manager (before that, pen tester) in the cyber-sec division of one of the big-four audit firms. His input has really shaped my understanding of the language we should use. He reviews all reports and generally manages to pick me up on something. Here’s how we work, with regards to the “secure or insecure” topic:

Generally, our wording is along the lines of “no vulnerabilities were detected”. This clearly communicates that we did not find any issues, however it leaves open the possibility that some flew under the radar. We also try and avoid the term “audit” as it tends to infer some form of official inspection abiding to some predefined set of rules, which does not exist in this space. We prefer to use “security review”.

We absolutely do not declare a system to be “secure”, “safe”, “vulnerability-free” or anything of the like. Firstly, such terms are absolute and in order to use them accurately you would need to arduously define the scope of the statement (e.g., does it extend to the management of the “owner” keys, does it include the security of a hash function, etc). Secondly, using such terms do not leave room for error on the reviewers behalf.

Of course, you could use some catch-all “best-effort” statement at the end of the document to cover a “secure” statement, but to me it does not seem very concise to declare a system to be absolutely *something*, then waive that absolute term later on. Sometimes you can’t avoid doing this (we do include and rely upon that waiver statement), but when it comes down to a final declaration of the system I think it should be as concise as possible.

Interestingly, I was pulled up on the statement “no known vulnerabilities are present”, as it could be interpreted that “known” includes all vulnerabilities known to humanity, meaning the contract is impossible to exploit at this point in time. Avoiding such ambiguity is important to us, so I would definitely say that calling something “not insecure” is either directly calling it “secure” or simply too ambiguous to be used in any official statement (using our methodology).

---

**holiman** (2018-05-22):

I worked as an infosec consultant for about 7 years, so here are some thoughts…

- Whenever we wrote a report, we were always very careful to outline the exact scope (what did we look at, what did we look for), and very precise about all that was excluded. You need to think hard about what you have excluded, since it’s harder to narrow it down than what you actually did do. Things like: “did not audit the test-coverage”, or “did not audit the multisig wallet that will be used to operate the contract”, or “did not include the web-parts of the user interface”. Also thread-model-wise: does the audit assume that the operators are trusted?. In scope, always include what you mean by security: security of the users? of the owners?
- The report summary always ended with a rating. Typically "we consider this app/thing to have a low risk […of being hacked…} ", if it was good. We never ever wrote anything more positive than “low risk”.
- All reports contained a list of observations made. Each observation had one-paragraph summary: non-technical who can achive what impact . E.g: “A flaw in input handling made it possible for an authenticated attacker to alter database entries”. After that follows a technical description. After that recommendation(s) to fix the flaw.

A notable difference I’ve seen in this space, compared to infosec, is that customers tend to want to use the audit as a sales-tool. I have had to explain basically “I’ll give you the report, you’re free to do what you want with it. If you publish it in incomplete form, I reserve the right to publish it in it’s entirety. The report will focus on the things you did wrong, not the things you did right”.

Oh, and after delivering a report, we *always* made a follow-up report when they had fixed the issues. That second check should be quick, and not cover anything other than verifying the fixes in the first report.

I agree about iterative mode being good – but at some point you’re not an auditor any more, but instead the security-guy for the team. And in that case, maybe someone else should do an audit. If a company have X dollars to spend on security, the ‘iterative-security-guy’ approach may be better to spend it on than a pure audit-approach, imo.

---

**maurelian** (2018-05-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> customers tend to want to use the audit as a sales-tool.

Agree that this feels awkward, but I’m not sure it’s a bad thing. End users should genuinely care about security here. Reports should still be written for the project team, but a knowledgeable end user should be able to read the report.

---

**trigun0x2** (2018-05-22):

Risk auditing often deliver probability instead of a boolean for things like this.

I’m in favor of a probability of risk of each major section of code instead of one answer for the entire codebase.

---

**trigun0x2** (2018-05-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maurelian/48/43_2.png) maurelian:

> How can auditors collaborate with development teams earlier in the design and development process?
> How can the we improve on the existing incentives* in developer/auditor relationship?

I think one big issue here is that most teams come from a web development background and they’re not in the mindset of working with a security team from the start.

We often hear from teams 1-3 weeks before their official launch (for small - medium size projects).

I have found that the overall atmosphere is changing and people are starting to care about security as a core component thanks to efforts like this.

---

**fubuloubu** (2018-05-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/trigun0x2/48/330_2.png) trigun0x2:

> I think one big issue here is that most teams come from a web development background and they’re not in the mindset of working with a security team from the start.

100% this. There is no common resource that explains “why” they need to be more careful, only this general threat that you do, or else learn it the hard way.

Explaining what risk is and how to think about it is a critical skill not many have who are entering the space.

---

**fubuloubu** (2018-05-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> A notable difference I’ve seen in this space, compared to infosec, is that customers tend to want to use the audit as a sales-tool.

I think a big part of this is because it’s such a new process for most people, they see it as a value-add instead of a requirement. There’s a lot of education to be done…

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> I agree about iterative mode being good – but at some point you’re not an auditor any more, but instead the security-guy for the team.

I think there’s a difference between an audit relationship that’s semi-frequent and “the security guy”. If it’s at defined checkpoints where major changes are taking place, then that’s a value-add because they have better intuition of what the product should do without being too deep in the day-to-day. I would say any contact more frequent than 2-4 weeks and you start to errode the objectivity of the auditor because of familiarity.

---

**RexShinka** (2018-05-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maurelian/48/43_2.png) maurelian:

> Is it an auditor’s job to pronounce a system “secure or insecure”?

In aerospace, the final auditor is the government (the FAA or equivalent).  All they say is that a piece of software was developed according to a strict process (at the software level).  They never say anything about bugs and security.  At the system level (flight test) they say the system worked properly when a strict agreed test set was executed.

If there was an agreed process, then the auditors responsibility becomes smaller.  An agreed set of code and compile review tools is an example.  The auditor can just run the tools to check the box.  Constantly improving the process is crucial here.

Complex blockchain security aspects (re-entry, inheritance, etc) may be very difficult to check via a process, so the individual auditor may still be vital for some time.

The process also pushes the work onto the development team, not the auditor.  The auditor spots check that the process was done correctly.  I just realized that with everything in the public github (as it will be for many projects) then anyone can audit the process.  That could be interesting.

---

**fubuloubu** (2018-05-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rexshinka/48/225_2.png) RexShinka:

> I just realized that with everything in the public github (as it will be for many projects) then anyone can audit the process.  That could be interesting.

That’s a great point. Very interesting indeed!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rexshinka/48/225_2.png) RexShinka:

> The process also pushes the work onto the development team, not the auditor.  The auditor spots check that the process was done correctly

I definitely think we need to explore more of what the developer team’s responsibilities should be. There should be some predefined metrics for success in terms of security, basically what is acceptable and what is not acceptable, as different projects may have different guarantees. Setting expectations is important for a successful audit, as it is for users to understand exactly the level of detail that was applied.

Heck, even a short disclaimer saying “this code is unaudited as it is intended for testing or entertainment purposes only” would be a step up from the level of ambiguity we have now.

---

We both harp on aerospace because that is what we know, but it does have a solution for this problem: Design Assurance Levels (DAL). It’s a simple letter score that sets clear high level guidelines of what the expectations are for a system: Level A means “flight critical”, which means the system is designed to withstand multiple faults as the functionality is critical for safe operation of the aircraft. Level C means “mission critical”, which means degradation of the system is marginally hazardous as it increases pilot workload, which could lead to mission abort, and other more dangerous scenarios. Level E basically means “not hazardous at all” which means it does not affect flight safety, and you can do whatever you want to test it as nothing is required.

This simple grading schemes allows system integration engineers (like I was in my old career) to take systems other people have designed (like sensors and actuation equipment) and build a larger system out of them. Understanding the DAL as well as the failure modes of that system is what allowed us to do this successfully, it gives us the framework necessary to make well-reasoned assessments without having to be experts in those systems.

Perhaps something similar can work here, I know I am figuring out how we can apply it.

---

**Ethernian** (2018-06-23):

BACKGROUND:

My code was audited by two independent auditors and deployed one year ago.

Two cosmetic bugs came in to sight till now but no major bugs appeared.

Our Auditors were great guys! I am very thankful to them!

EXPERIENCE:

1. Auditors have audited me, but I have tryied to audit the auditors too.
I have silently implanted some bugs into the code and tried to estimate a quality of the audit by ratio bugs_found / bugs_known.
Unfortunately non of auditors have found all my “fake” bugs, so the ratio was <100%.
(but they have found other show stopping bugs!)
IMHO, this kind of measurement must be part of any professional audit.
2. Audit must be provided face-to-face and in pair-programming mode. Some bugs may be in the gap between specification and implementation. So you will need to explain not only the code written, but the environment around it.
A pair-auditing is very exhausting job. More 4 hours a day is not reasonable. You will spend days if not weeks on it.

---

**fubuloubu** (2018-06-24):

Pair-auditing is a very interesting suggestion.

I’m not sure if pair-programming itself is warranted here, that’s more a of a design practice and I think the auditor needs to stay sufficiently out of the design to be objective.

But I definitely think pair-auditing – running through the list of issues found alongside the developer – should absolutely be best practice for reviewing audit revision suggestions.

Face-to-face is the best way to do this, but not always possible. Tools that help with this will be very handy.

Wemux is cool! https://github.com/zolrath/wemux


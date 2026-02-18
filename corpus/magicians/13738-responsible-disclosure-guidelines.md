---
source: magicians
topic_id: 13738
title: Responsible Disclosure Guidelines
author: PatrickAlphaC
date: "2023-04-09"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/responsible-disclosure-guidelines/13738
views: 1714
likes: 24
posts_count: 20
---

# Responsible Disclosure Guidelines

For a long time, we as a community have not settled on a responsible disclosure process, leading to white hats being unsure of what to do when a vulnerability is hacked.

This has caused funds to be lost, whitehats to be ridiculed (scaring other white hats from trying to white hat), and a air of unease in what is already a very stressful situation.

This has happened many times with mixed approaches and success.

- instance A
- instance B
- instance C
- Instance D

The dilemma is as such:

# 1. Reach out to team, and hopefully you don’t speak to someone with ill-intentions

Pros:

- You can work with the team and make sure they get their funds

Cons:

- The clock is ticking. If you found the exploit, it’s only a matter of time before someone else does
- We want to encourage White hats to do the right thing, but some feel all their work will be for free
- Smart contracts are permissionless agreements, and some have no governance. Who is responsible for a smart contract that has no owner? Who do you report to?

# 2. You rescue the funds yourself

Pros:

- You can be assured that you have saved the funds, and no one else will exploit it

Cons:

- You can mess up the rescue and potentially make it worse
- You can scare or piss off the project
- Potential legality issues?
- Some white hats become grey hats, holding funds unless they are promised they can take a percentage of the recovered funds

# We need a community guideline

EDIT: I don’t think this needs to be an EIP?

I propose that at DeFi summit we have a panel that is a few hours long where we have a discussion where we can nail down a responsible disclosure process.

EDIT: Orrrr… we just discuss it here.

I’d want someone from Immunefi there, since it seems like an easy step 1 would be to “check if they have a bug bounty.”

I’m happy to moderate this panel, although I don’t have much experience running town halls like this.

We iterate on the guidelines as people follow them to mixed results.

Seems like an initial outline would be:

1. Check if they have a bug bounty program. If yes, follow those steps.
2. Try to reach out to the team, and give them X amount of time (finding X seems important)
3. In the event X is passed, attempt rescue
4. During the rescue, follow Y steps:

Y steps might be:

Before sending any transactions, consider:

- If its possible for this to be MEV’d? If unsure, reach out to Z.
- Who else this might effect

Anyways, looking forward to suggestions on this

## Replies

**PatrickAlphaC** (2023-04-09):

Questions like such should be addressed:

- How to make sure reporter is compensated (or how do we foster a community where white hats are encouraged to help protocols)?
- What if protocol devs are incompetent?
- Who is responsible for decentralized code?
- How long do you wait for report to be answered?

---

**Romeo369887** (2023-04-09):

Here’s my suggestion:

1. Investors should demand a fair bug bounty program for every crypto project.
2. There should be a standardized verification procedure that every white hat should go through where they prove themselves competent enough to spot potential issues in a project. As a result, whenever one such white hat approaches the project custodians they will take the issue seriously or else be held responsible for oversight.
3. The bounty program should be confidential and the white hat should be legally/contractually required to shut up for the next 48-72 hours (or any other appropriate timeframe) while they take care of the issue. In violation, the white hat would lose their special privilege.

Vice versa, if the project doesn’t come up with a satisfactory justification to ignore the white hat’s warnings and do nothing, they will be a) penalized for oversight and b) pay a fee to the white hat regardless.

---

**McNatureCrystal** (2023-04-09):

*summon Web3 High Council of Chains*

*No such council known*

Think an IT General, global, public, trusted, transparent “Dev-Reddit” where any IT development knowledge (publicly accessible) can be found.  One that’s advertised publicly via mainstream sources, such as Billboards to Tv to Facebook.

Imagine if all these various YouTube channels and developer forums and docs all had one location, the collective amount of global collaboration would be positively obnoxious.

It would also be a perfect use case scenario for this whole hullabaloo that’s been occurring.

Plus non IT individuals would have a place to report sketchy offbeat fraud, scams and cryptocurrencies for the whole technology community to see.

I am by no means an expert but I can most certainly state that it’s growing increasingly hard for beginner devs to continue/start a reliable, unbiased path of learning.

---

**MarkusEicher** (2023-04-09):

Hi Patrick. As a newcomer to this domain, I’m pretty concerned about what I have just read. The 4 examples you mentioned in your post above are not giving a good feeling about the way the industry or the community handles bugs, flaws and vulnerabilities. I personally find the case D specially concerning. I consider the implementation of the Uniswap contract as weak. If you follow the POC, then it seems that it would be possible to harden it in favor of the users. If I did understand it correctly, it would be possible to handle ETH transactions better than standard ERC20 Token transactions. Well, however. Cases B and C read like stuff for a Hollywood movie. Unbelievable efforts from white hat people without any guarantee to get compensated. These Dark Forest stories should be out in the wild to read for everyone being in this scene, especially for people new to this. I will for sure do my research to keep up with this security topic. I hope you will find good company from competent people with influence to come to a good solution and more awareness for this. Thanks for doing good work for the community and good luck for all who contribute to this.

---

**port** (2023-04-09):

The following steps can be one of the ways to handle such a situation.

1. Upon discovering a bug that has the potential to cause significant loss of funds, the white hat hacker should report the vulnerability to the affected project team as soon as possible.
2. If the team fails to respond within a specified time frame (e.g., 4, 6, 8, or 12 hours - to be determined through community discussion), the white hat hacker may proceed to take necessary actions to secure the funds by exploiting the vulnerability in a responsible and ethical manner.
3. In the event that the team responds within the specified time frame, the white hat hacker should collaborate with the team to determine the appropriate course of action to address the vulnerability.

Feel free to suggest any improvements.

---

**Maka** (2023-04-09):

There are so many factors, for one there are no protections for rescuers. Have been involved with some successful rescues and a couple failures. Both failures saw the attempting white hat’s accused of stealing.

If the wrong person gets the wrong idea could be a big issue.

Getting front run or copy catted seems to be most common first fail and you would hope someone learns that with a smaller sum, at the same time the person attempting a rescue has to act responsibly and within their own limits.

If there are massive sums on the line and they are remotely unsure about any aspect, then should probably lean towards submitting a proof of concept to the relevant security team via some encrypted method.

We are also in an era where it increasingly takes less knowledge of how things work, to have a tool find (and exploit) a bug for you, than it does to file a report on it in some cases.

Have had people say they are researchers with bugs to report, while not knowing how to encrypt a message with a pgp key.

Would love to see best practices pushed in relation to rescues and reporting.

---

**edamigod** (2023-04-09):

So, after reviewing the replies so far to this thread it seems formatting of a proper solution is the main issue. I appreciate the intent put behind the original post because it gives a clear idea as to what’s needed.

White-hats are already incentivized to cooperate to a degree, but the “10%” bounty default when a program isn’t in place is an unspoken agreement that many incompetent or incorrigible development teams might not acquiesce to. Protocols must have bug bounty programs to be considered investable, period. This is not something that is enforceable on a protocol level, obviously. Due-diligence is on the user’s end, but novel tools in this space spur adoption before proper vetting as part of their bullcase. This isn’t a sustainable way to protect users, especially in the face of incompetence.

If the protocol does not have a bug bounty program, official means of safety should be established within the community so that there is no legal liability for both parties.

(This is where room for an EIP actually makes sense.)

In order for a white-hat to consider that a notification period was sufficient to execute an exploit, one must consider that the time-period be mathematically derived instead of static for all protocols. Something to the tune of: Time-since-launch / TVL of protocol with another parameter for time-integer reasonability. This alleviates fears of incompetence causing users to lose funds to a potential black-hat as long lasting protocols with significant TVL usually have some form of incident management in place if a bug bounty program isn’t present (which usually isn’t the case).

In the case that the protocol doesn’t not respond within this mathematically-derived time period, the white-hat may disclose the exploit through whatever channels they deem necessary and/or exploit it themselves while taking a default 10% bounty & holding funds securely for return post-mortem.

This “default” bug bounty program would prevent protocols from gross negligence while incentivizing white-hats to continue being benevolent. Forcing protocols to adopt this standard if they refuse to adopt a bug bounty program is a great step forward in prevent gross loss of funds for most users trying to interact with novel & established dApps.

This also would also help address the many cases where protocols do not recognize the severity of a potential exploit even though a clear vector for fund loss has been established. Preventing legal disputes necessitates this being an EIP or some other decentralized but enforceable standard…

---

**McNatureCrystal** (2023-04-09):

This. People don’t take into account that we have neighbors, roommates, staff with ISP, local, state, federal government’s.

All these are layers of trust that CONSTANTLY change.

Everytime you discover a trust line is hiding something, the line gets damaged.

---

**kamikazebr** (2023-04-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/maka/48/9131_2.png) Maka:

> encrypt a message with a pgp key.

That its good point. We could create a protocol with that kind of tools, where Devs of Projects (DoP) and Bugs Reporters (BR) could met in secure way for both side.

Of DoP could assure upfront the bug bounty for the protocol give the available timeframe of response. BRs could file a report on the issue and even decide if need go to Rescue. That File need be in secure way encrypted, so after the Rescue (if necessary) or Attempt that could be proven later on, after the timeframe past using some kind of Commit-Real or even ZKProof.

In cases where DoP dont register your projects we could have that colllected from contracts deployed based in the previous projects related and have big Index. So we could have Researchers to get in touch with DoP to incentivize they verify and register the project.

I’m just dreaming here, but who knows that could be some solution to help both parties collaborate and have some protections.

---

**Maka** (2023-04-10):

A lot of great suggestions I’d love to see standardized.

At very least can raise awareness of best practices, that aim to protect researchers and users while being respectful of a target protocols position.

Researchers can adequately hash proof of concepts and paste publicly for verification at a later date, before disclosing.

Researchers should probably avoid public mem pool where possible, and learn how to send encrypted email.

But if protocols don’t pay for what is a verifiable crit they should be publicly shamed.

And if someone whitehats then keeps <= 10%, it should not be up for discussion.

There are though a lot of grey areas, as to what constitutes “incompetent”, on the side of protocol or researcher.

It can be hard to relay a threat to someone else, when it is technical, where context is limited, or if there is a language barrier. Some engineers are arrogant, but reports can also be akin to badly written spam from a chancer.

So a team might need time to test and verify information they are only just receiving, and it’s tough to put a hard number on that duration.

If you are convinced you can rescue funds and that someone else is likley to blackhat before you can get the protocol to listen then you should do what they think is right, while understanding people will point fingers if anything goes wrong.

Not sure if there is one size fits all solution, as it so dependant on parties involved, level of assumed risk etc.

But if there were to become a standardized, broadly accepted formula for reward that accounts for age of protocol and TVL, it could help reduce some whitehats urge to rush a rescue as a means of being assured a fair reward.

---

**h4l** (2023-04-10):

Maybe this is tangential, but I came across a vulnerability in a draft EIP today, and couldn’t find a disclosure procedure for EIPs/ERCs. In this instance I’ve contacted the authors directly, but it would be useful to have some guidance for this.

---

**Tudmotu** (2023-04-10):

This is an important topic, especially seeing as one of the most profitable trading strategies in crypto today is exploiting protocols.

Your post raises a fundamental conflict for white hats in the crypto space:

Once an exploit in a contract is discovered, *there is not much to do other than try and rescue the funds*. Even if you notify “the team”, they have nothing to do about it other than to ask users to withdraw their funds, which will alert malicious actors to the possibility of an exploit.

*Is there even a way to solve this fundamental issue?*

I’m not sure, but I think the first step is to start talking about something we’ve been avoiding for some time:

Immutability.

Smart-contract immutability, while trust-minimizing, is also security-minimizing.

In the “TradTech” world, immutability is not only rare — it’s “considered harmful”:

- Libraries are kept up-to-date to include latest security patches, which are even backported into LTS releases
- Exploits are fixed covertly, without affecting users
- Agile/Lean/etc taught us that rapid releases lead to fewer bugs

In TradTech, *there is no such fundamental conflict*, because we can update software without affecting users. When a white hat discovers a vulnerability in a Web2 product, they don’t need to consider whether to exploit it themselves or not, because they know the centralized entity that controls that product can simply update the code and make the issue go away.

As I said, I am not sure what the solution here is. But I strongly believe we should start talking more about immutability and whether its benefits outweigh its costs.

---

**PatrickAlphaC** (2023-04-10):

1. Agreed. Bug bounties are important.

I think the meta right now is 10% with a cap at like $5 Million.

1. I don’t think this will work. We’d make an authoritative group responsible for giving white hat certs which is antithetical to what we are doing in web3.

I don’t think this is enough. It doesn’t address if a project:

- Doesn’t have a bounty
- Doesn’t have a dev team (ie: ungoverned)

It’s a good start though.

---

**PatrickAlphaC** (2023-04-10):

1. Yes. Good step 1.
2. Agreed. What should we set that time frame to be?
3. Agreed.

What if there is no dev team?

We probably need rescue guidelines too.

---

**PatrickAlphaC** (2023-04-10):

I like the math approach for deriving at an acceptable response time.

One thing to note, I think 10% + a cap is a better reward default.

For example, a $100B protocol shouldn’t have to give $10B back. Remember, that’s $10B of pension plans, retirement funds, etc.

---

**port** (2023-04-11):

Honestly, I think 6-8 hours could work given that everything happens so fast in this space.

If there is no team, yeah we need rescue guidelines.

Maybe a smart contract that uses a commit-reveal scheme could work here. So that the white hat can prove that he could rescue the funds

---

**Angler** (2023-04-11):

Hey [@PatrickAlphaC](/u/patrickalphac) thanks for bringing this topic up. We are actually building a protocol called Hats Finance to precisely battle these issues. Here are the two most urgent issues in our opinion:

For projects spam and low-effort reports is probably the biggest issue.

It is currently very viable to submit the same “non-issue” to 100 projects. Most will dismiss it but if one or two projects pay $100 out of courtesy then it was worth it for the submitter (basically an economic attack on bug bounties).

This is a very big issue for the projects since they have to block resources for reviewing a great number of submissions with most of them being no/low value and it buries important information.

A real critical submission could be left unread because it’s expected to be another spam report or simply be stuck in the queue to be triaged.

We think an on-chain submission that acts as a spam filter is one of the cleanest solutions. The security researcher has to either pay a small fee (transaction cost + variable fee) or stake a small amount (gets slashed in case of spam) to submit a report.

This makes it unviable to send the same low-effort report to 100 projects but doesn’t affect a real submission worth potentially multiple $10k.

For Security Researchers / Hackers the biggest issue is uncertainty around payments

The security researcher has to disclose all information regarding the vulnerability before the negotiations for the reward starts. At this time the project has no incentive anymore to pay a high reward since it’s already in possession of all required information and the white hat often gets lowballed or even ghosted. There are multiple ways to solve this issue our mid-term solution is to host the bounties in an on-chain vault that a neutral Arbitration Service can freeze in case of a dispute.

The long-term solution is to automize payouts with an information escrow. The hacker creates a “ZK Proof of Hack” and hands over the PoC to an Escrow. The reward itself is in escrow before the team gets the information on the vulnerability. If the issue gets exploited before the team can fix the vulnerability the hacker loses his reward.

There are many more issues:

- How to size a bug bounty to be effective
- How to ensure encrypted communication between the hacker and the team
- How to allow hackers to participate that can’t KYC (we still want them to disclose instead of becoming black hats)

---

**Kinetex** (2023-04-26):

Establish clear policies: Protocols can establish clear policies outlining the process for reporting vulnerabilities and the rewards for doing so. These policies should be easily accessible and communicated to the community.

---

**PatrickAlphaC** (2023-09-11):

Thanks for the comments all. I dropped the ball a little on this conversation. Picking it up back now.

[@Angler](/u/angler) love the post. Wondering if you have a solid proposal?

[@port](/u/port) wondering if you can take a look at this.

# What do you do if you find a live issue?

1. Check for a bug bounty

- If yes → Submit, and you’re done
- If no → Continue

1. Reach out for help

- Seal 911 (Or other emergency web3 paths)
- Connect with the team
- Come up with a plan to fix

If they want to fix → hooray! Do that. ← ISSUE: How do we make sure they get paid for their work?

If they ignore it… You have a few options:

1. If they ignore you

- Give them 45 - 90 days to fix it, and say you will publicly disclose the information if they do not fix it
- Attempt a rescue yourself (Ideally, you never reach here)

The reason I brought this up in the first place, and am bringing it up again, is I want to give a clear path in new educational materials so we can avoid whitehats hurting themselves and others.


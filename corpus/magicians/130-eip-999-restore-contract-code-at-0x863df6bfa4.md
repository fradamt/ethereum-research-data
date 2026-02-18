---
source: magicians
topic_id: 130
title: "EIP-999: Restore Contract Code at 0x863DF6BFa4"
author: 5chdn
date: "2018-04-15"
category: EIPs
tags: [fund-recovery]
url: https://ethereum-magicians.org/t/eip-999-restore-contract-code-at-0x863df6bfa4/130
views: 25880
likes: 199
posts_count: 120
---

# EIP-999: Restore Contract Code at 0x863DF6BFa4

I have published EIP-999 this morning: This proposes to restore the code of the `WalletLibrary` contract at `0x863DF6BFa4469f3ead0bE8f9F2AAE51c91A907b4` with a patched version that can not be claimed or killed.

Link to [read the proposal document](http://eips.ethereum.org/EIPS/eip-999). Any comments welcome! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

Edit: Apparently, a lot of the discussion is taking place outside this thread. I’ll try to document this here:

- https://reddit.com/r/ethereum/comments/8cdqi8/restore_contract_code_at/
- Proposal to restore a destroyed Ethereum contract | Hacker News
- https://github.com/ethereum/EIPs/pull/999

For the sake of completeness, there is an ongoing coin vote, however, I do not endorse this.

- https://www.etherchain.org/coinvote/poll/35

## Replies

**sfultong** (2018-04-15):

How is there no discussion here?

Apparently people prefer to voice their disagreement on github.

Between this, The DAO fork, and EIP 867, I think this is the least evil, personally.

---

**fubuloubu** (2018-04-15):

EIPs like this are sort of like court cases: they set precedent.

Therefore a specific request to restore a change to a point where it would be set straight (or at least firmly crooked) sets precedent on how this sort of thing might occur in the future. In my opinion, 867 was not a good precedent to set, and that’s why it failed. I believe this is marginally closer, because hard forks have a signaling process that corresponds loosely to general consensus instead of a review board and public hearing like 867 proposed.

I think this is at the core of good governance of our platform, and the fact that a resolution to this issue keeps getting proposed I think shows that we need something in place. It needs to set the correct precedent moving forward such that it is as robust and fair as possible, and this is a much larger conversation we need to be having as a community. The decisions being made here affect far more than the money that was lost.

---

**fubuloubu** (2018-04-15):

I know parts of my specific solutions to these problems:

1. Higher level software engineering guidelines to prevent this sort of bug in the future, minimizing occurances as much as possible.
2. On-chain recovery vehicles like insurance, where losses are covered partially and uncontroversially, at least until a larger decision is made.
3. A community-centric process for identifying and creating consensus for responses to issues like these, that ensure the broadest possible response where users can signal their support and adoption is managed in the fairest possible way. This process mighy take months to years to resolve, and I think that should be on purpose.

---

**x-ETHeREAL-x** (2018-04-15):

This is a specific request to restore a single self-destructed contract? How many people have made mistakes that cost them ETH? Allowing case-by-case proposals for mistake reversals is a terrible idea and opens up all kinds of concerns about picking winners and losers (and who gets to pick).  When any person or group is able to pick winners and losers, you inevitably get corruption, bribery, etc.  This would set a terrible and dangerous precedent.  Parity/Polkadot has a lot to gain from this being accepted – how much would they rationally be incentived to offer in direct bribes and/or indirect social media manipulation to help get this passed?  Maybe they wouldn’t do this and are good actors, but it cannot be assume others would be. This needs to be condemned as a class of proposals that open the door to massive corruption, not merely as an individual proposal.

---

**supRNurse** (2018-04-15):

While I applaud the effort to return the trapped ETH to the Parity clients, let me ask what about the remaining multitudes of people with ETH trapped in un-spendable accounts. Why push a method that only rescues Parities funds.  Many of us have stranded funds and have waited a lot longer for a solution.

---

**MicahZoltu** (2018-04-16):

That is why I personally prefer the previously proposed ERP process.  It gives everyone equal opportunity to get their funds restored, without having to come up with novel solutions for each.

---

**supRNurse** (2018-04-16):

I agree completely. One method arguably improves the chain… the other just returns ETH which was lost by important people.

---

**5chdn** (2018-04-16):

EIP-999 can be perfectly converted into an ERP as specified in EIP-867 but apparently it does not look like anyone wants to implement it. Interesting observation from the two previous discussions:

- EIP-867: “we don’t want a process for that”, “recoveries should be rare, exceptional precedents”
- EIP-999: “we don’t want elitist proposals”, “everyone should be able to recover lost funds”

I openly support EIP-867, but I don’t want to wait for it to happen. And if any other case wants recovery, i.e., the EIP-156 cases, I would advise them to also write proposals. This might create a strong case for proceeding with ERP.

---

**MicahZoltu** (2018-04-16):

I fully agree [@5chdn](/u/5chdn).  I would *love* for someone to champion writing up ERPs for the well known cases of lost ETH, including the Parity multisig, 156, off by 1, etc.

---

**fulldecent** (2018-04-16):

![:-1:](https://ethereum-magicians.org/images/emoji/twitter/-1.png?v=9)

12345678901234567890

---

**dekz** (2018-04-16):

I personally had to do a double take at the speed in which this EIP was reviewed (and approved within 40 minutes) and merged. Being all too familiar with the EIP process, I have to note this was extremely quick. It should also be noted that counter-point EIPs exist such as [EIP#894](https://github.com/ethereum/EIPs/pull/894) which meet the criteria to be merged (having responded to feedback) which have not been.

This issue, as you aptly point out is quite contentious. I understand that a merged EIP does not mean the EIP is accepted and will be implemented. I am afraid that the greater community **does not**.

I currently have not yet made a decision, on a personal level, of where I stand on this issue. The spotlight is now shining on the EIP reviewers, the core dev team and the community on how this will be handled. I implore you all to remain impartial if your position in the community asks this of you, if not let your opinions be heard and known to the public.

Thus we as a community are thrown into the world of public perception. Ethereum’s immutability will be questioned. Motives, impropriety and cronyism will all be brought up in the public sphere.

Let the result of this be advantageous for the community and not for a single actor.

> Asking the Ethereum community first if an idea is original helps prevent too much time being spent on something that is guaranteed to be rejected based on prior discussions (searching the Internet does not always do the trick). It also helps to make sure the idea is applicable to the entire community and not just the author. Just because an idea sounds good to the author does not mean it will work for most people in most areas where Ethereum is used.

We will no doubt spend many hours if not days discussing this and issues like this in the future, I quote EIP1 above and I hope we all think through this in-depth. *Does this benefit the entire community and not just the author.*

---

**MicahZoltu** (2018-04-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dekz/48/75_2.png) dekz:

> counter-point EIPs exist such as EIP#894  which meet the criteria to be merged (having responded to feedback) which have not been.

That EIP doesn’t meet the bar for editorial requirements (IMO), as has been discussed pretty thoroughly in the EIP comments.  The editors have tried to give feedback to the author on how it can be changed to be more grammatically/technically sound, but the author insists on using particular language, I believe because the purpose of the EIP is meant to be evocative.

I believe some of the EIP editors *are* against recovery, but they are generally all able to remain objective in their editing role, which is to ensure that EIPs that get merged as a draft are effectively written so as to effectively communicate what they are proposing.  You can even see in the discussion of 894 that people in favor of the EIP don’t even agree on what it means because the wording is so unclear and vague.

---

**Mushoz** (2018-04-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5chdn/48/1242_2.png) 5chdn:

> EIP-999 can be perfectly converted into an ERP as specified in EIP-867 but apparently it does not look like anyone wants to implement it. Interesting observation from the two previous discussions:
>
>
> EIP-867: “we don’t want a process for that”, “recoveries should be rare, exceptional precedents”
> EIP-999: “we don’t want elitist proposals”, “everyone should be able to recover lost funds”
>
>
> I openly support EIP-867, but I don’t want to wait for it to happen. And if any other case wants recovery, i.e., the EIP-156 cases, I would advise them to also write proposals. This might create a strong case for proceeding with ERP.

Of course, this is completely normal. There will be 4 different groups:

1. The group that values immutability above all, and wants neither proposal to succeed.
2. A group that wants a general solution, but not a cherry picked solution for the Parity hack and hence would support EIP-867 but would oppose EIP-999
3. A group that doesn’t want a general solution, but would accept this one-time only decision. Hence this group would agree to EIP-999, but not to EIP-867.
4. A group that thinks either solution is a good solution and would support both EIPs.

Personally, I firmly belong to group 1. Both EIPs require an offchain decision and hence is vulnerable to bribery and extortion. Parity has a huge financial incentive to make these EIPs pass and hence have a huge financial incentive to bribe people, the media, etc. Parity might be a good actor, and not employ these tactics, however, this sets a hugely important precedent. What is to stop another actor that manages to lose a good chunk of money not to employ these kind of dirty tactics?

Also, many many funds have been lost in the past. Why should we even discuss this particular case, but not all the others? If either EIP is allowed to pass, who is going to decide which other parties will have their funds restored? This whole idea is incredibly dangerous and will set a very bad slippery slope that we should avoid at all costs.

In my opinion, the Ethereum blockchain loses much of its value if it loses the immutability property and hence I strongly oppose this EIP. A lessened form of decentralization and immutability should only be allowed to be used on sidechains. Immutability is THE most important property of the base layer and should be protected at all costs.

A blockchain based system that is vulnerable to bribery and extortion is no more valuable than legacy systems and will soon meet the same corruption that plagues legacy financial systems and politics. No thank you.

Lastly, while I do feel incredibly sorry for the people who lost money in this, this ultimately was employing extremely sloppy practices on Parity’s part. No formal third party audit after the code was changed that is handling hundreds of millions of dollars is just a sad state of affairs. A bailout here would simply give out the message it is okay to not follow best practices, because a bailout is around the corner should mistakes be made.

---

**cooganb** (2018-04-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/53a042/48.png) supRNurse:

> While I applaud the effort to return the trapped ETH to the Parity clients, let me ask what about the remaining multitudes of people with ETH trapped in un-spendable accounts. Why push a method that only rescues Parities funds.  Many of us have stranded funds and have waited a lot longer for a solution.

Agree!!

I absolutely agree with this sentiment!

---

**sfultong** (2018-04-16):

It seems like the All Core Devs meetings is where the final decisions on governance are made.

I think EIP-867 is the worst idea, as it makes core devs responsible for evaluating every ERP. How many ERPs do its proponents think will be drafted? I can easily picture a situation where every All Core Devs meeting involves going through 100s-1000s of ERPs, the vast majority without merit. How could the process not be abused? Bitcoin maximalist trolls could fill out tons of ERPs for very little effort.

I’m less hostile to EIP-999, but I do think that the community needs some objective criteria on what sort of smart contract screw-ups should be fixed through ad hoc hard forks. Until we can come up with that criteria and have the majority of the community agree with it, I’m against EIP-999

Unfortunately, even measuring what the majority of the community agrees with is contentious.

---

**MicahZoltu** (2018-04-16):

Trolls can already spam the EIP GitHub repo, the ERP system won’t change that.  The first step is getting to draft which means getting past the editors which make sure that the proposal is at least sound/grammatically correct/technically complete, so the only things that will make it to the core devs meeting are ERPs like similar to EIP-999 where someone has a complete solution drafted up and it is well described and implementable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sfultong/48/71_2.png) sfultong:

> It seems like the All Core Devs meetings is where the final decisions on governance are made.

This is incorrect.  The All Core Devs meeting is where the various client dev teams discuss what each client team is going to implement.  Ultimately the individual clients can choose what to implement but they generally *prefer* to all implement the same things to avoid a fork.  Ultimately the final governance decision is what economic participants decide to run.  Even if all of the clients implement a thing, if no one upgrades their client to accept the changes then it doesn’t matter.

---

**prestonvanloon** (2018-04-16):

I think this EIP would set dangerous precedents if accepted.  This EIP outlines the recovery of a contract that was used in an unintended way where the contract contained no underlying flaw, rather it was simply misused.

Personally, I have issues with this EIP. It outlines a specific contract recovery rather than generic recovery (EIP-867). This would set precedent to create another EIP when some subjectively non-trival amount of ETH is lost by misuse of a valid contract. If I set the wrong owner on my multisig contract and lost all of my ETH, am I entitled to my funds to be recovered? The amount lost is not significant to the network and poses no risk to others, but it was my entire stash.

I agree with the quote below…

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/8491ac/48.png) Mushoz:

> In my opinion, the Ethereum blockchain loses much of its value if it loses the immutability property and hence I strongly oppose this EIP. A lessened form of decentralization and immutability should only be allowed to be used on sidechains. Immutability is THE most important property of the base layer and should be protected at all costs.
>
>
> A blockchain based system that is vulnerable to bribery and extortion is no more valuable than legacy systems and will soon meet the same corruption that plagues legacy financial systems and politics. No thank you.
>
>
> Lastly, while I do feel incredibly sorry for the people who lost money in this, this ultimately was employing extremely sloppy practices on Parity’s part. No formal third party audit after the code was changed that is handling hundreds of millions of dollars is just a sad state of affairs. A bailout here would simply give out the message it is okay to not follow best practices, because a bailout is around the corner should mistakes be made.

/vote no on EIP-999

---

**sfultong** (2018-04-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Ultimately the final governance decision is what economic participants decide to run.

The decision to leave the network that is called Ethereum is a very final form of “governance”, but it’s not useful to bring it up in the context of deciding on the future of Ethereum.

The definition of what the network called Ethereum is, is decided by All Core Dev meetings. This is why we don’t call Ethereum Classic the “real” Ethereum.

I’m fine with this centralized governance, but I think the value of Ethereum will be greater if the community can agree ahead of time that certain things about the protocol should not be altered.

---

**fubuloubu** (2018-04-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sfultong/48/71_2.png) sfultong:

> The decision to leave the network that is called Ethereum is a very final form of “governance”

I think the process needs to look much closer to something like this, as that is basically a final signal that entire network sees nothing wrong with the proposal. Getting a measurement of support/no-support from the entire community would be required to vote effectively on outcomes like this proposal.

---

**maurelian** (2018-04-16):

I avoid this debate, because I don’t really have any novel points to make, but I guess it’s at the stage where decisions are made by a vague sense of how loud the shouting is.

So here are my grumbling reasons for opposition:

1. Moral hazard. We’re not paying attention to the less influential voices who have lost a much less money, so we’re implicitly endorsing a “too big to fail” incentive model.
2. Future distraction. Ethereum’s competitive advantage is in a large, friendly community of contributors, working hard on scalability and usability improvements.

Making this change will ensure that we continue to revisit requests like this on a regular basis. That will **continue** to distract us from efforts to improve the technology for everyone. Becoming a project which constantly debates fund restoration EIPs will make Ethereum a “not much fun” open source project to contribute to, thus deterring new contributors.


*(99 more replies not shown)*

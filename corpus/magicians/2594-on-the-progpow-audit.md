---
source: magicians
topic_id: 2594
title: On the progpow audit
author: lrettig
date: "2019-02-05"
category: Protocol Calls & happenings > Announcements
tags: [progpow, ethcatherders, audit]
url: https://ethereum-magicians.org/t/on-the-progpow-audit/2594
views: 5984
likes: 39
posts_count: 31
---

# On the progpow audit

Opening this thread as a general purpose place for the community to discuss the upcoming progpow audit being handled by the Ethereum Cat Herders at the request of the All Core Devs. Please post questions or comments and we’ll do our best to make sure that all parties weigh in.

## Replies

**sneg55** (2019-02-07):

Could you clarify little bit what’s the purpose of this audit?

---

**sneg55** (2019-02-19):

I’ve another question, I was wondering why EF struggling with funding ProgPow audit.  Is it really necessary to fund **security audit** with bounties?

---

**lrettig** (2019-02-25):

I don’t think it’s a lack of funds, I think it has more to do with political sensitivity: trying to remain neutral and not favor one side or the other, concerns around sending signals, etc. EF is hypersensitive to this sort of thing.

---

**sneg55** (2019-02-26):

It’ll be great if you could mention it on upcoming Progpow audit bounty page, since it’s not 100% clear for everyone.

---

**lrettig** (2019-02-26):

I don’t think I can, that’s not my bounty

---

**lookfirst** (2019-02-27):

There are now two bounties:

[Fund WhiteBlock Analysis](https://explorer.bounties.network/bounty/2424)

[Fund Andrea and teams past and future development](https://gitcoin.co/grants/54/progpow-full-stack-integration)

Both are extremely important to get funded in order to get ProgPoW to mainnet.

At this point, development has stopped as Andrea has run out of his own personal funds to continue.

Without 3rd party analysis, nobody can recommend to the CoreDevs that this is a safe solution.

If WhiteBlock finds any issues, then those will need to get resolved and the Andrea funding is also to help with that.

---

**lookfirst** (2019-02-27):

The whole argument that the EF cannot get involved in funding ProgPoW is weak sauce.

If ethereum is ever 51% attacked, the EF is going to have a huge mess on their hands.

---

**fubuloubu** (2019-02-27):

I’m not sure the audit is a *security* audit? ([@souptacular](/u/souptacular) can maybe clarify)

From what I remember from the council of Denver, the audit was to ensure the claims of ASIC resistance had a solid underpinning, and to obtain an independent review of the code for the hardware claims being made.

We don’t know the right people to contact for that who are sufficiently “neutral” on this issue.

---

**lookfirst** (2019-02-27):

My expectation is that WB will do all of the above.

Is WhiteBlock not neutral enough? I can’t think of a single motivation they would have to produce results that favored ProgPoW such that they would have any benefit. In fact, it would be a risk to their entire business model to ‘approve’ ProgPoW.

For the sake of the security of Ethereum, I deeply hope they find issues and they get resolved as quickly as possible. Thirdening is coming literally tomorrow, which reduces profitability even further and we have Linzhi coming out with claimed 7x ASIC’s in June/July… who’s going to be left to secure the network?

---

**lookfirst** (2019-02-27):

Saying that there is nobody “neutral” enough to evaluate and ensure the security of a ~$14b (today) network, is a grand failure of the EF.

A [fund should be created](https://gitcoin.co/grants/15/whiteblock-testing-2) just to make sure that this doesn’t happen again and the EF should be the #1 contributor.

---

**fubuloubu** (2019-02-27):

I would say Whiteblock *is* neutral enough actually. I think they have the expertise to evaluate, so I am happy they got this effort started.

This happened *after* the council though, so the sentiments have probably changed since the council.

---

**fubuloubu** (2019-02-27):

We’re all on the same side. I was working on a post to try to call out all my potential issues with ProgPoW to shake out the last of the skeptics and move this forward.

This is a highly contentious and political upgrade, it’s been very difficult to find all the facts amidst all the noise and outrage.

---

**lookfirst** (2019-02-27):

Maybe your visibility into the matter is new. I just need to point out that this has been discussed at many levels (private and public), for months now. I’m just glad it is moving forward.

Agreed on the noise, which is why the idea came about to get WB involved. This will allow us to get past the contention and personal drama and focus on the technology. If it is sound, all the better. If it has issues, let’s get them fixed.

Next step is to get the word out to fund it all.

---

**fubuloubu** (2019-02-27):

I am like most people who have had familiarity with the proposal for months. From the outside looking in, there is a mess of different incentives at play, it is very difficult from a macro level to determine if it is a “necessary” change to make, even after you dig through the tough technical points of whether it is sound (and it appears sound to me from my limited knowledge in hardware engineering).

My points as a skeptic were much broader and more philosophical about whether it was a distraction, but I am with you now that this has a marginal enough boost to network security that it is worth the funding to move forward and protect the diversification of the mining ecosystem.

Every time someone calls a skeptic like myself “uninformed”, “stupid”, or claims that the proposal is “obvious”, it trips alarm bells in my head that lead me further away from the path to understanding why it is necessary, especially as someone who admittedly has very little hardware design experience to evaluate the proposal.

What we need now is more facts and less “professional opinions”. I think that’s what gets this across the finish line.

---

I’m sorry if that is terse or rude, but it has been my experience that people who are for the proposal are getting exasperated instead of being patient and guiding people through it.

I think many people involved are underestimating the political-ness of this proposal. It is a hard battle to fight!

---

**lookfirst** (2019-02-27):

Seems weird to call anyone names or make assumptions. I don’t know how to respond to that, but I’d say it takes thick skin to be here. Just discounting something because you’ve been called a name doesn’t seem like a good solution either. Maybe people are yelling because they feel strongly about the security of the network and care about their investment in this technology. They see the train rolling down the tracks towards the bridge that has explosives on it.

Agreed that it is hard to evaluate. My first reaction to it all was: “We need to make sure it is 110% necessary” and “Why is Kristy such a drama queen?”

Once I got past that and decided to focus on the tech, it became clear that due to the focus on PoS and [a distaste for PoW](https://twitter.com/VitalikButerin/status/1077548790272405504), a ball had been dropped.

That ball is the understanding of the importance of PoW on the current network. Ethash has served well for so long that all the people supporting it are gone now. The deep understanding of the importance of mining and securing the network against 51% attacks, is gone. Miners have been relegated to a necessary evil, which is really the wrong way to look at the people who are securing the network today.

At the same time, this has given ASIC manufacturers a chance to catch up with their solutions. The threat of losing the original mission statement of being GPU centric is real, especially now with the crypto winter and thirdening. Profitability is gone and GPU’s are being turned off. Look at the difficulty levels (subtract out the time bomb increase), we are back at 2018 levels… a whole years worth of added compute power has been shut off.

Everyone has had their eye on the PoS ball… even with the assumption that it’ll just replace PoW. But, fact is that PoW isn’t going away anytime soon. It will be around for years more. It will overlap with PoS for years after that is first released. PoW is not a distraction, a 51% attack is a distraction.

It turns out that whatever personal motivations Kristy (or whomever) had to originally work on ProgPoW are not relevant now. The thirdening, crypto winter and Linzhi hastened things to the point of making these the relevant issues.

Agreed. More facts. Less opinions. Let’s get WB funded and working ASAP. I’d argue that the EF should reverse their decision and fund these grants. It is embarrassing to effectively have to beg the community to fund this stuff.

---

**fubuloubu** (2019-02-27):

Calling people names is a tactic to attempt to force someone into making a decision a certain way. It usually has the opposite effect on me, hence why my initial reaction to ProgPoW was to move against it, because it raised those types of flags. I agree that there seems to be the best alignment to move forward with it, but only after a personal accounting with my larger concerns that lead to this being a marginal enough benefit to be valuable (instead of an overwhelmingly obvious result).

---

“ASIC resistance” as a concept is disputable, but we don’t have the luxury of disputing it anymore because we can’t guarantee a robust and fair marketplace for development of machines against an “ASIC friendly algo”.

We also have to be sure we are the top GPU mining coin, and that the value of other GPU coins is not comparable to our own so we remain untouchable by mercenary hash power.

There are tons of macro level analysis that trades whether it is worth it to move forward with now, the eventual move to PoS is also something to consider as even though the Phase 3 (final) network is years away, the Phase 0 chain should hopefully launch within the year and we can use it to help secure the chain if we are smart!

We have to evaluate all options here to ensure security, not just ones we know about.

---

**lookfirst** (2019-02-27):

Agreed 100% with everything you said.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> We have to evaluate all options here to ensure security, not just ones we know about.

The issue is that there is no funding, or motivation, to do that evaluation. =( Hence this discussion. =)

---

**shemnon** (2019-02-27):

At the council of Denver I thought that the audit needed to cover 3 areas:

- performance benchmarking
- a professional opinion as to the claim that there will only be 1.1x/1.2x/1.5x theoretical asic advantage (based on tech)
- a professional opinion that the algorithm is cryptographically sound, i.e. there are no known calculation shortcuts and the crypto primitives (like keccak-f800) are used correctly or at least are used in a way that will provide what we want it to do.

The benchmarking will provide insight as to wether the 0.9.2 version of the spec or 0.9.3 version provides a not-too-unbalanced amd/nvidia performance difference, and also help us plan for what to expect on a block transition when the hashes/sec goes down 2x-3x.  (how long to get back to 15s blocks and how much sooner will the ice age be felt).

What I want and likely won’t get is some validation that this design will provide the desired limited upside to ASIC implementation.  As someone not trained in hardware the explanation sounds legit, but a corroborating opinion from a qualified neutral party would be better.  It sounds like all the qualified experts will all have conflicts of interest and won’t be considered neutral, or are otherwise unavailable to comment.  I hope I’m wrong on that mark.

---

**Anlan** (2019-02-27):

I agree with all positions expressed above. Nevertheless let me point out some facts.

1. The whole point of ProgPoW on Eth is to slow down incoming wave of ASICs and to prepare a more levelled field for any mining device;
2. All this delays only give room to ASIC manufactures to organize a counteroffensive move and prepare for a contentious hf;
3. ProgPoW specs are publicly available since a year now
4. Heavy lifting has already been done implementing both verification on major nodes (geth and parity) and an open-source miner;
5. If anyone is thinking that audit/testnet/implementations can go ahead without proper funding … then better we dismiss the whole project.

---

**fubuloubu** (2019-02-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/anlan/48/1434_2.png) Anlan:

> ProgPoW specs are publicly available since a year now

This is probably the biggest risk. “ASIC resistance” ultimately relies on information asymmetry, which inherently gives any solution a shelf life. Ask the Monero folks, the community can’t move as fast as a well-organized hardware company.


*(10 more replies not shown)*

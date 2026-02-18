---
source: magicians
topic_id: 805
title: CoinDesk article about "stuck ether", and efforts to unstuck the process
author: jpitts
date: "2018-07-19"
category: Magicians > Process Improvement
tags: [fund-recovery]
url: https://ethereum-magicians.org/t/coindesk-article-about-stuck-ether-and-efforts-to-unstuck-the-process/805
views: 3428
likes: 21
posts_count: 28
---

# CoinDesk article about "stuck ether", and efforts to unstuck the process

**Ethereum’s Most Heated Tech Debate Is Proving It’s Far From Over**

https://www.coindesk.com/ethereums-most-heated-tech-debate-is-proving-its-far-from-over/

Even though she quoted a few extreme/trollish statements, overall [@rachel-rose](/u/rachel-rose) does a decent job covering the many facets of this issue, and helpfully integrates comments made in this forum, in social media, in GitHub, and in deliberations at the 2018 Council of Berlin.

> “I think that people feel unstuck in the sense of, ‘Hey, EIP 867 needs to get turned into an actual process.’”

I’m also really glad the article emphasized another key statement made by [@boris](/u/boris) on Saturday at the Council of Berlin:

> “There is no finality in the room here,” Boris Mann, co-organizer of the event, reminded everyone. “We know that humans meeting face-to-face is a good way to get a job done, but finality in any decisions will be made in a much more open and accessible forum than this discussion.”

But unfortunately the extreme aspect came early-on in the article, perhaps dissuading many readers from reading on:

> “Ethereum is completely centralized.”

It seems that the loudest and most quotable voices too often get included in articles. Could the spirit of this be conveyed without encouraging flat-earth views? Still, we remember that concerns about opaque governance processes are real, and should be thoughtfully addressed.

This is part of why we are organizing the Magicians and its Circles!

## Replies

**boris** (2018-07-19):

Centralized in the same way that Bitcoin has an open source process and BIP process too? I just don’t understand that statement.

Thanks for capturing and quoting this all out, [@jpitts](/u/jpitts)

---

**boris** (2018-07-19):

Comments on the article:

Shouldn’t [@5chdn](/u/5chdn) be listed as “Communications Manager, Parity and Ethereum Core Dev” or similar?

notgrubles [being quoted](https://twitter.com/notgrubles/status/1018503412940529664) without the context of him not understanding the EIP process at all really sucks. I responded in that thread.

(OK, I was going to pick apart a bunch more lines but just too hard when the info is pulled in from everywhere)

Here’s my tweet thread about the article that I just posted:



      [twitter.com](https://twitter.com/bmann/status/1019961665696223232)



    ![image](https://pbs.twimg.com/profile_images/1854187880522121216/a6WsfLBz_200x200.jpg)

####

[@bmann](https://twitter.com/bmann/status/1019961665696223232)

  I appreciate @_lunar_mining attending #ethmagicians & sitting in on many sessions. From speaking to her, I understand the challenge of putting together a fair & understandable article.

I'm quoted several times: https://t.co/jjzit9i977

  https://twitter.com/bmann/status/1019961665696223232










The thread started by [@CryptoHokie](/u/cryptohokie) [Slight process improvement ideas: Deferred Proposals and Community Support - #16 by boris](https://ethereum-magicians.org/t/slight-process-improvement-ideas-deferred-proposals-and-community-support/744/16) is where some quotes attributed to me came from? Or maybe from gitter governance? That’s the other tough part – chasing down where those quotes came from without direct links means the article further obscures context.

I feel like I’m getting drawn into this fight without enough context of my own. I think still on my plate is an attempt to make a diagram, and more discussion on Core Devs role. Without more Core Devs in the room, it was easier to just say “your guys’ problem”.

[@cdetrio](/u/cdetrio) did a great job of beating me up (in a good way) by pointing out that the “we” that have to work on this is everyone who cares about this stuff.

Back to notes and next steps!

---

**AtLeastSignificant** (2018-07-19):

I’ve been having numerous arguments, mostly on the /r/ethereum subreddit, involving the centralization issue.  It’s far too easy to assume that there are financial, power, and other ulterior motives behind the actions of core devs and the EIP process.  This is not to say that there are any that pose significant threat, but nothing is being done to prevent this speculation.  In fact, the direct opposite is being done.

---

**boris** (2018-07-19):

Can you explain what the centralization issue is?

Ethereum node clients are developed by multiple groups across multiple repos.

The EIP process is run inside a repo owned by the Ethereum Foundation.

The process, this forum, Core Devs represent individuals.

I’d love to better understand what the issue is.

---

**AtLeastSignificant** (2018-07-19):

To somebody working within the development sphere, there probably is no apparent centralization issue.  The problem arises once EIPs have been approved and core developers have agree to implement some change.

Miners and non-technical community members (or technical ones who are not directly involved with core dev activities) have absolutely no say in what is done before or after EIPs are accepted.  By definition, they are not participants in what happens pre-approval, and once core devs have decided to implement some change there is essentially no viable recourse for these parties.

It may be by design that non-technical people are not participating in the EIP process.  That would be a mess and bog down the whole thing.

It may also be by design that miners don’t really have any say in things if they plan on taking the most financially viable options.

I don’t personally have any issues with the level of centralization, but the way it is handled is extremely opaque and makes it trivial to speculate about all kinds of things.  There is both history and current actions that are troubling, and very little has ever been done to prove that the suspicion is unwarranted.

---

**AtLeastSignificant** (2018-07-19):

I’m not sure that the Bitcoin process is comparable to Ethereum at this point.  Node signalling is still the governance mechanism, and it’s an opt-in for change approach.  This is the opposite for Ethereum that takes an opt-out approach, and since the vast majority will simply follow what they think the rest of the majority will do (adopt the change), they also adopt it because it’s financially safe.

I will also suggest that most miners are participating in pools and/or do not actually know or care about the changes to the protocol.  They only care that it is profitable to mine.  Just how much of the network is like this is impossible to know, but I would say it’s the majority.

---

**boris** (2018-07-19):

Hence the work on signaling.

---

**AtLeastSignificant** (2018-07-19):

Can you point me in the right direction to inform myself on this work?  I actually just posted: https://www.reddit.com/r/ethereum/comments/907g5m/feasibility_of_adding_a_signalling_mechanism_to/

---

**boris** (2018-07-19):

Thanks - appreciate the expanded context.

If by centralization you mean — a group of Code Devs where anyone can get involved who is building a client?

The short form of EthMagicians inclusion statements is “all are welcome”. There were lots of non-technical people (including myself, although I do have tech experience) participating.

What came out is that everyone is fairly comfortable with technical feedback process.

Now there is an undefined process of how Core Devs accept & schedule items for inclusion (those really are two steps, especially since HF inclusion opportunities might be years apart).

Even then, users can run whatever client they feel like.

So that’s where we’re at. There is an undefined process and potentially some assistance from signaling. And a bunch of stuff about chain IDs per EIP that went over my head in the Gitter chat.

No ill will, no closed groups, nobody in charge. Just a willingness to work on the issues.

---

**boris** (2018-07-19):

There is a Signaling ring in the process of forming. There is a Riot channel #ethsignaling

See also this thread [Lightning Talks: Signaling: Technical challenges with measuring sentiment](https://ethereum-magicians.org/t/lightning-talks-signaling-technical-challenges-with-measuring-sentiment/728) — which includes a link to video of the presentation.

---

**AtLeastSignificant** (2018-07-19):

> a group of Code Devs where anyone can get involved who is building a client?

That’s not entirely true.  There are many who have opinions but who are not equipped or interested in being equipped to “get involved” in a meaningful way.  This is why I think the level of ~~centeralization~~ filtering is both by design and beneficial.  It would be *more* beneficial to make what code/core devs do more transparent so that these individuals (who are economic participants) are not perpetuating some sort of controversy that doesn’t need to exist.

> What came out is that everyone is fairly comfortable with technical feedback process.

From within the EthMagicians circle, I assume.  I know that the reddit community has many people who are far from comfortable with things.

> Even then, users can run whatever client they feel like.

This is the statement I have the biggest problem with. It’s patently false.  Miners cannot support whatever fork they want if they are acting as rational economically driven entities. They can *only* support what is financially viable, and what is financially viable is *only* what core devs decide to implement.

This is somewhat concerning on its own because it leaves out those who are not involved in development, but I personally have no problem with that.  I have a problem with people who represent Ethereum claiming that this is not the case though, and the real problem is that “what core devs decide to implement” is not a transparent process and is far too easy to speculate about.

I find this to be self evident by the fact that I’m here discussing it in a thread about a CoinDesk article also talking about it.  The root of the problem seems to be ignorance, not shady practices (although many who would support my position so far would not agree with this point).  I don’t think you can educate those who wish to remain ignorant, so I think the far simpler solution and one that is most honest is to be clear that Ethereum governance and development is *not* something everybody can participate in.  It is reserved for those who have high ability, time, money, and desire.

---

**boris** (2018-07-19):

Yes, from one weekend with a small group of people. None of whom “represent Ethereum” because that’s not possible. We are a volunteer group that wants to work together to improve the technical underpinnings of the network.

And what also came out is exactly what you are saying — that more work needs to be done on Core Dev process and signaling.

I don’t know how else to cover your thoughts on “not everyone can be involved in the Core Dev process”. Every other open source community I have been involved in functions the same way. The barriers are time & effort to learn code bases and participate. Do you have suggestions on this point?

It’s being discussed here because people care about giving feedback and context.

I’ll bow out on miner comments altogether since I don’t know enough about it.

Hope that helps.

---

**AtLeastSignificant** (2018-07-19):

> None of whom “represent Ethereum” because that’s not possible.

Again, this is patently false.  To say Vitalik doesn’t represent Ethereum, Vlad, Nick Johnson, etc. don’t represent Ethereum is borderline delusional.  You don’t have to have unilateral control over the entirety of the network to be a figurehead.  In fact, it’s not even up to Vitalik & others to decide whether or not they represent Ethereum, it’s entirely the choice of the community.

> Do you have suggestions on this point?

My suggestion is that those who represent Ethereum stop suggesting that the development process is the epitome of decentralization, because it’s not.  It doesn’t account for miner sentiment nor economic participants opinion.  If that is intentional, which I think it is, then they need to be clear about it and not pretend that anybody anywhere can play a meaningful role.

Again, my personal problem with the current situation is that it’s far too easy to create false narratives that harm the ecosystem as a whole, and current actions are only increasing this problem, not working to squash it.

---

**jpitts** (2018-07-19):

[@AtLeastSignificant](/u/atleastsignificant) you make some very important points in this discussion. However, I would ask you to refrain from language which, in an ad-hominem manner, paints another person as being disconnected from reality.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atleastsignificant/48/219_2.png) AtLeastSignificant:

> Again, this is patently false.  To say Vitalik doesn’t represent Ethereum, Vlad, Nick Johnson, etc. don’t represent Ethereum is borderline delusional.

---

**AtLeastSignificant** (2018-07-19):

Agree, and my apologies.

---

**jpitts** (2018-07-19):

Thanks, [@AtLeastSignificant](/u/atleastsignificant)!

---

Regarding this point:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atleastsignificant/48/219_2.png) AtLeastSignificant:

> You don’t have to have unilateral control over the entirety of the network to be a figurehead.  In fact, it’s not even up to Vitalik & others to decide whether or not they represent Ethereum, it’s entirely the choice of the community.

I would not call these individuals figureheads, perhaps I will just refer to them as “prominent voices”.

There is a certain social weight of individuals that can be outsized, and this has to be acknowledged. They may not represent Ethereum in any structural sense, but their communications do create and reinforce power structures IMO.

The weight of their voices is often deserved, as their contributions and expertise are immense. They may also understand or implicitly represent certain important stakeholder concerns.

However, some of the social weight has been packed on by the media attention or likes on Twitter, etc. In other cases, it is packed on by having a record in other areas, but perhaps not the area in question. This can lead to distortion in the decision-making because of a possible inaccurate assumption of domain competence.

By understanding these power structures and potential distortions, we can create decision-making mechanisms which mitigate the social problems and enable the best decisions possible.

Avoiding biases in decision-making is partly why we have defined certain principles for the Fellowship, among them:

- open process, all are invited to participate, all notes are public
- representing yourself in decisions, and not your stakeholder group (that can be done in the rings or other emerging stakeholder groups)
- technically competent input

---

**AtLeastSignificant** (2018-07-19):

I agree that there is no centralization issue at the individual level.  As Vitalik said, devs are a pretty fungible lot.

From my understanding, the primary point of centralization lies within the current EIP process - something I am under the impression is being actively worked on.

I would like to see the EIP process be purely technical, and a separate *fully transparent* process for deciding which EIPs are going to be supported by core devs.  The latter can happen before the former, meaning EIPs can be rejected by core devs before being fully fleshed out in every technical detail - to avoid worthless work.

When I say “fully transparent”, I do not mean “anybody can write in, just like the FCC comments”. I mean I would like to see core devs who head important and contentious issue provide a full-disclosure about their bias, motives, etc.  This would go a long way in dispelling a lot of the unknown and speculation about bad actors and whatnot.  Video format would be ideal for this IMO, just because the demographic who benefit most from understanding what the changes are and why the are being supported are not those who are already reading about them on Github/here.

I really believe it’s a PR issue, not that core devs are full of bad actors and intentionally doing suspicious things.  There is a centralization concern, but it’s a necessary and beneficial level of centralization for Ethereum, just not transparent enough to quell what seems to be an increasing level of suspicion and (probably) intentional/organized misinformation campaigns.

---

**boris** (2018-07-19):

Amusingly, I am going to have a [BLOG OFF with Nick, where I argue in favour of “anyone can submit EIPs”](https://ethereum-magicians.org/t/eip-standards-process-2-30pm-saturday-july-18/766/2) – the group of people who review them is much broader than just Core Devs, especially as we boot up Rings. So, if it’s Wallet related, the people working on Wallet Ring can provide their expertise. More broadly, anyone can make a technical comment / objection to any EIPs.

Since it is fully open, lots of people end up making political or non-technical arguments, which is not helpful.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atleastsignificant/48/219_2.png) AtLeastSignificant:

> I would like to see the EIP process be purely technical, and a separate fully transparent process for deciding which EIPs are going to be supported by core devs.

As I’ve stated several times, what you’re apparently asking for here is *exactly the conclusion we came to*. Please do get involved and help out.

PR issue: honestly, “we” are going to continue operating in the open with full transparency.

---

**AtLeastSignificant** (2018-07-19):

This is really encouraging thing to see.  I think my ignorance to much of what’s been said here is a bit indicative of the problem others are also experiencing though.  I moderate two fairly relevant Ethereum subreddits, as well as a handful of smaller ones, and consider myself more active than the “average user” - whatever that is.  I also have a strong engineering and security background - yet I’m largely in the dark about a lot of this stuff because I simply don’t have the time between a 60 hour a week job and other projects/responsibilities.

It requires a certain level of time and effort to keep up with all of this stuff, and I don’t think the larger community on Twitter/Reddit have that.  These really are the primary platforms where most of the confusion and dissent are taking place, and I wonder if it’s not something that can be worked on (or if it’s even worth working on from your perspective).

---

**boris** (2018-07-19):

If you will excuse me for being blunt for a moment, *work* does not get done on those platforms.

Broadly speaking, I have seen this coming for a couple of years as interest has gone exponential. The average business person buying crypto on an exchange has no idea about the collaborative process by which open source gets built. Never mind the extra layer of running an open source blockchain network.

I am *brand new* to being this involved in the Ethereum community – basically you can see me writing up some notes and suggests at the end of May, and then I volunteered to organize the Berlin event – which was the second ever, and really the first of its kind. Now we have Magicians, Rings, and [Scrolls](https://github.com/ethereum-magicians/scrolls/wiki) and will be more organized.

But, I do have a 15 year history in open source, so this all seems very normal. The community is storming / forming / norming around base processes. What is harder, is there is no central authority to appeal to.

I even found that Ethereum projects (that are dapps or otherwise not building node client software) that I reached out to had in many cases not being focused on how to move the core code along. The ERC standard setting (as opposed to EIPs on core protocol) are a vast space where dapps *can* collaborate. But we have to get those projects to have people within their organization that spend time keeping up, that are welcomed in, and that work together on useful standards.

And of course, because a lot of us deeply care about the principles of decentralization, standing up and shouting about “this is the way it works and I’m in charge” would directly go against that. So we hope people will collaborate around best practices – because ideally no one can force anything.

The larger community are going to have to decide to either get involved directly (which, yes, has a certain time commitment!) or to find voices / people / sources they “trust”. This has always been the case for open source.

I appreciate the effort *you* have made in the discussion here. I think we ended up in violent agreement ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=9) This got long again, and it is late! Cheers!


*(7 more replies not shown)*

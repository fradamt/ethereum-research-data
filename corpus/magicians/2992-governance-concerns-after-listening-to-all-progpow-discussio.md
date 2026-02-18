---
source: magicians
topic_id: 2992
title: Governance concerns after listening to ~all ProgPow discussions on Core Dev calls
author: elliot_olds
date: "2019-03-26"
category: Magicians > Process Improvement
tags: [progpow]
url: https://ethereum-magicians.org/t/governance-concerns-after-listening-to-all-progpow-discussions-on-core-dev-calls/2992
views: 4683
likes: 38
posts_count: 58
---

# Governance concerns after listening to ~all ProgPow discussions on Core Dev calls

I recently went back and listened to all the Core Dev calls that I could find in which ProgPow was discussed (call 38, and every call between 45-57 – let me know if I missed any) to understand the process by which we got to this point. These are the governance-related issues that I found most concerning:

**1. There was an assumption from the beginning that it was appropriate for the Core Devs to horse trade with the GPU miners**

Core devs talked about giving miners ProgPow in exchange for them accepting the issuance reduction from 3 to 2. It seems far from obvious that this sort of thing is appropriate. I’d guess that many in the community believe that GPU miners should not receive compensation from the network to ‘offset’ harms, but that we should instead only offer such compensation when it benefits the network as a whole. At the very least, if the network is to give out compensation like this it’s something that more than just the Core Devs should decide. It’s not a technical issue.

**2. There is an assumption that’s almost never stated explicitly that ASIC resistance is a worthy goal to pursue**

There is research and theoretical arguments suggesting that ASIC resistance makes the network less secure (see https://youtu.be/N6eDuEEb0Oc?t=458 for instance). Never at any point in my review of the dev calls did I see the Core Devs engage in how this change impacts the cost to attack Ethereum, which IMO is the most important consideration. It is true that the whitepaper is anti-ASIC and ethash was designed to be anti-ASIC, but our understanding of crypto network security has improved since then. Hudson did ask at least once if anyone had any opinions about whether ASICs were really a problem: https://www.youtube.com/watch?v=TafZui-DnV0&feature=youtu.be&t=3387, but his question was met with 18 seconds of silence.

**3. To make such an impactful change we probably want to get feedback from more than miners**

Here’s a very condensed timeline of how the initial tentative consensus was reached, based on my notes. I may have missed some things, and am not aware of anything that might have happened outside of the Core Dev calls:

On call 38 the IfDefElse team joins the call the present ProgPow to the Core Devs.

On call 45 there were several miners giving their opinions on ProgPow in the context of issuance reduction discussions.

On call 47 Hudson says that there’s renewed interest in getting ProgPow into a future hard fork, but it’s not clear from listening to the call where the interest is coming from. I’m guessing miners? Hudson later says that he’s been talking to video card manufacturers about it.

Calls 48, 49, and 50 have technical updates and implementation progress. On call 51 the devs confirm that ProgPow has not been decided yet.

Miss If and Mr. Else (creators of ProgPow) are on call 52, where Hudson makes clear that in the call they’ll talk about “if” they should ship ProgPow, not when. Most devs who speak seem in favor of shipping it, one has concerns about the amount of work required. They discuss for about 45 minutes in total. At the end of this call, Hudson says that they’ll tentatively go ahead with ProgPow unless there’s some major problem found.

I believe it was after call 52 where the first big pushback occurred. It looked like the Core Devs made the decision after after consulting with miners and the IfDefElse team, but I didn’t see much evidence that anyone reached out to the broader community. As noted above, all I listened to were the calls so I may be missing attempts to rope in others.

It’s seems hard for the community to discover such things organically, because discussions about ProgPow were sandwiched between discussion of technical issues that legitimately only required the consensus of the Core Devs, making it hard for non-Core-Devs to find the relevant discussions. Even if the community was following the Core Dev calls and had listened to call 51, there was no indication that the Core Devs were going to make the tentative go-ahead decision by the end of call 52.

**4. There doesn’t seem to be enough awareness of conflicts of interest.**

As in the Afri situation, conflicts of interest exist and are relevant regardless of whether the parties in question are doing anything wrong.

Given that the situation we’re in now seems to be the result of miners initially pushing for it, it would have been nice to see more skepticism and attempts to reach out to the broader community. There seems to be an assumption in the dev calls that what miners want should be given significant weight. IMO this is pretty controversial and not something for the Core Devs to decide.

## Replies

**lookfirst** (2019-03-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> It is true that the whitepaper is anti-ASIC and ethash was designed to be anti-ASIC, but our understanding of crypto network security has improved since then.

I’d love to know what the improved understanding has to do with the anti-ASIC stance.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> 4. There doesn’t seem to be enough awareness of conflicts of interest.

For those of us following ProgPoW for a long time now, the conflict of interest issues are a dead horse. It is a technical argument now. Does it do what it is claimed and does it pass analysis?

[Least Authority’s original ethash analysis predicted the state we are in now…](https://github.com/LeastAuthority/ethereum-analyses/blob/master/PoW.md#9-month-overhaul)

---

**boris** (2019-03-26):

Thanks for posting this here!

How do you think Core Devs can “test” the contentious-ness of something?

Core Devs have already said they don’t want to take on the responsibility of reaching out to the community. Do you have any suggestions on who should do this and how?

For reference, related threads (which puts pings on those other threads):



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jcyr/48/133_2.png)
    [My technical take on ProgPow's weakest link](https://ethereum-magicians.org/t/my-technical-take-on-progpows-weakest-link/2983) [EIPs](/c/eips/5)



> First let me say that I’ve worked extensively with the algorithm, and as far as I’m concerned it is sound and meets its objective of evening the mining playing field. As proposed ProgPow creates a new pseudo random sequence of OpenCL or CUDA code every 10 blocks or so. In order to run on the GPUs this code is just-in-time recompiled at run-time with each new ProgPow period. In an ideal world that would be fine, but compilers (specially optimizing compilers) are incredibly complex beasts and are …



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png)
    [On the progpow audit](https://ethereum-magicians.org/t/on-the-progpow-audit/2594) [Announcements](/c/announcements/8)



> Opening this thread as a general purpose place for the community to discuss the upcoming progpow audit being handled by the Ethereum Cat Herders at the request of the All Core Devs. Please post questions or comments and we’ll do our best to make sure that all parties weigh in.

And the [progpow](/tag/progpow) tag should capture everything related to this.

---

**elliot_olds** (2019-03-26):

> I’d love to know what the improved understanding has to do with the anti-ASIC stance.

The video I linked to above is a good start, and I’d be happy to elaborate more but I’d like this thread to focus on the governance issues. Is there another thread existing thread you’d recommend taking this discussion to?

> For those of us following ProgPoW for a long time now, the conflict of interest issues are a dead horse. It is a technical argument now. Does it do what it is claimed and does it pass analysis?

Regardless of what has happened since then, on call 52 the Core Devs made a decision to tentatively go ahead with ProgPow after seemingly only talking to miners and the IfDefElse team about it. They may have talked to others too but I’m only going by what’s reported on the calls. The issue is not “have the conflicts of interest for ProgPow been addressed in the ensuing discussion?” but “what policies should we have to detect/deal with changes pushed by those with conflicts of interest in the future?”

---

**elliot_olds** (2019-03-26):

> How do you think Core Devs can “test” the contentious-ness of something?

I think in this particular case intuition should have caught it. Changing the proof of work function of a coin has long been considered a pretty major event.

For the general case it seems useful to have a high signal to noise channel announcing when a change is starting to be seriously evaluated by the Core Devs, and when a decision has been made. A Twitter account would probably work well as updates will naturally be retweeted based on community interest.

It need not be an existing Core Dev who does this. Have we tried explicitly soliciting a volunteer from a pool of technical Ethereum enthusiasts for something like this before?

---

**lookfirst** (2019-03-26):

Ok, then let’s get back to governance…

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> 2. There is an assumption that’s almost never stated explicitly that ASIC resistance is a worthy goal to pursue

It is explicitly stated all over the place. Including the Yellow Paper. Are you trying to say it isn’t repeated in every CoreDev discussion and therefore a governance issue?

---

**boris** (2019-03-26):

Thanks. It sounds like “more communication” and “a place to go look / monitor” is what’s wanted.

There is a new [#eips:core-eips](/c/eips/core-eips/35) forum here, and the hardfork process 233 update will have a single page to monitor for updates.

---

**elliot_olds** (2019-03-26):

Yes – the white and yellow papers are both anti-ASIC. They are also both very old and I think the reasoning in the yellow paper is flawed.

I’m registering your point as “ASIC resistance is so clearly established as good that it’s fine that it was never discussed on the Core Dev calls.” I disagree but this doesn’t seem like the place to have that discussion. Curious whether other people here share your view though.

---

**lrettig** (2019-03-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> I think the reasoning in the yellow paper is flawed.

The reasoning in the white paper is sort of flawed too. It talks about resisting ASICs by requiring miners to process lots of arbitrary transactions, an idea that was debunked ages ago and never worked. In other words, it says ASIC resistance is a goal but doesn’t propose a workable solution.

---

**lookfirst** (2019-03-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> I’m registering your point as “ASIC resistance is so clearly established as good that it’s fine that it was never discussed on the Core Dev calls.” I disagree but this doesn’t seem like the place to have that discussion. Curious whether other people here share your view though.

I am specifically responding to your points and asking the hard questions, yet you keep telling me that this isn’t the place. ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12) Hmmm…

I am saying two things:

1. The original mission of ETH is defined as being ASIC-resistant.
2. The conversation to change that definition is separate from ProgPoW.

---

**lookfirst** (2019-03-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> In other words, it says ASIC resistance is a goal but doesn’t propose a workable solution.

Ethash has provided enough ASIC resistance for the last 4 years (which is a whole lifetime in crypto) that there isn’t currently a single manufacturer out there producing one publicly for sale. I’d say that goal has been achieved pretty well.

For better or worse, ETH is the top GPU hashrate coin. If that changes, there are actual and theoretical risks to the security of the network at the current time and in the future during the switch to PoS.

The decision to change from GPUs to ASICs is a far bigger question than to go ProgPoW or not. I cover this in 5,6,7… https://medium.com/altcoin-magazine/13-questions-about-ethereums-movement-to-progpow-e17e0a6d88b8

If Linzhi releases an ethash ASIC, they will be the ***only*** manufacturer producing something that is 7x more hash rate than anything else on the market. Another one might come along, but you can’t guarantee that. Bitmain is in huge financial trouble at this point and even their IPO is delayed. Inno is having financial issues as well.

---

**sneg55** (2019-03-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> How do you think Core Devs can “test” the contentious-ness of something?

I’ve seen a very a nice chart from EIP0 recently: [![image](https://ethereum-magicians.org/uploads/default/optimized/2X/e/ef5de9681c2258e820818edcf4bcdcc7392be8cc_2_591x500.jpeg)image1200×1014 108 KB](https://ethereum-magicians.org/uploads/default/ef5de9681c2258e820818edcf4bcdcc7392be8cc)

---

**boris** (2019-03-27):

Yes, by [@danfinlay](/u/danfinlay).

What people are asking for is to find out about Discussions and register it as contentious there.

Which is totally doable — but would require paying attention to published Core EIPs.

So the onus is on people to pay attention.

Going forward, perhaps the [#eips:core-eips](/c/eips/core-eips/35) category is good enough.

---

**elliot_olds** (2019-03-27):

> The original mission of ETH is defined as being ASIC-resistant.

ASIC resistance is a means to an end. It was desired because it was believed that it lead to decentralization in mining, which lead to better censorship resistance. If we have information that suggests ASIC-resistance is worse for censorship resistance, then I believe the community should abandon ASIC-resistance. Don’t you? Do you think the goal is something other than censorship resistance?

> The conversation to change that definition is separate from ProgPoW.

The impact of any change to Ethereum’s censorship resistance is always relevant to the ship decision if that impact may be significant.

---

**sneg55** (2019-03-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> If we have information that suggests ASIC-resistance is worse for censorship resistance, then I believe the community should abandon ASIC-resistance.

Any credible proofs on that?

---

**lookfirst** (2019-03-27):

What [@sneg55](/u/sneg55) said.

Also… why are you going off on censorship resistance? PoW isn’t about censorship, it is about the ability to not trust a third party for transaction confirmations. That is all. Per the Bitcoin whitepaper: Trustless.

The war is over hash rate and who controls it. Putting hash rate into the hands of a few small companies (the ASIC manufacturers, who are well known bad actors), is the most censorship driven thing you could possibly do.

---

**lightuponlight** (2019-03-27):

I can only agree with all the points raised by Elliot here.

The governance considerations here are enormous. This is an EIP designed to give economic benefits of one group at the expense of another, and so whether this is something Ethereum should be doing needs to be discussed at length with the entire community and unless the community comes to consensus about this, it should not go forward.

---

**tvanepps** (2019-03-27):

first, thank you for taking the time to pore over previous All Core Dev calls to map out a coherent timeline. this was clearly missing, and even Hudson lost the plot at one point, and he facilitates them. It’s been a long process and fluid players serve to add confusion at some points.

---

**sneg55** (2019-03-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lightuponlight/48/1779_2.png) lightuponlight:

> This is an EIP designed to give economic benefits of one group at the expense of another

EIP-1789 is also designed with same approach to give benefits of one group at the expense of miners.

---

**elliot_olds** (2019-03-27):

> why are you going off on censorship resistance? PoW isn’t about censorship, it is about the ability to not trust a third party for transaction confirmations

Trust a third party **to do what**? Bitcoin and ETH were designed so that you don’t have to trust a third party not to censor your funds, or confiscate them. The cryptographic aspects of Ethereum provide most of the resistance against theft (if someone doesn’t have your private keys, they can’t move your funds). The PoW mechanism allows double spending to be solved in a decentralized way, and the purpose of that decentralization is censorship resistance.

> Putting hash rate into the hands of a few small companies (the ASIC manufacturers, who are well known bad actors), is the most censorship driven thing you could possibly do.

It’s unclear whether ASIC manufacturers pose much risk.

I’ve decided to create a thread just about the object-level discussion regarding whether ASICs are good or bad for Ethereum, to ensure that this thread stays focused on governance:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png)
    [Is ASIC-resistance good for Ethereum?](https://ethereum-magicians.org/t/is-asic-resistance-good-for-ethereum/3018)



> There has been some discussion in this thread and in the ProgPow-review gitter channel about whether ASIC-resistance is a goal that Ethereum should be striving for.
> I thought it might be good to have a more permanent record of these discussions, in a thread that was exclusively devoted to them.
> The main arguments in favor of ASICs are:
> (1) GPU mined coins are cheaper to attack with rented hashpower
> It’s easier to rent a large amount of GPU power than it is to rent a large amount of ASIC powe…

---

**lrettig** (2019-03-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sneg55/48/1524_2.png) sneg55:

> EIP-1789 is also designed with same approach to give benefits of one group at the expense of miners

This isn’t true. EIP-1789 still isn’t finalized but it will include zero rewards to start so no one benefits at anyone else’s expense. There will be a separate EIP to turn on the rewards, and we don’t know yet whether they will come out of mining rewards.


*(37 more replies not shown)*

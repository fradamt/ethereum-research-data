---
source: magicians
topic_id: 3191
title: Process of getting EIPs getting accepted into a hardfork
author: boris
date: "2019-04-25"
category: Magicians > Process Improvement
tags: [eip, hardfork]
url: https://ethereum-magicians.org/t/process-of-getting-eips-getting-accepted-into-a-hardfork/3191
views: 1359
likes: 3
posts_count: 11
---

# Process of getting EIPs getting accepted into a hardfork

[@fubuloubu](/u/fubuloubu) is the first to use the upgraded 233 process to have his EIP as proposed in the Istanbul hard fork meta [EIP-1679: Hardfork Meta: Istanbul](http://eips.ethereum.org/EIPS/eip-1679)

> It was discussed on Ethereum Core Devs Meeting 59 Agenda · Issue #93 · ethereum/pm · GitHub already, but I am unsure if that met the requirements of discussion for consideration into Istanbul. In any case, I don’t think it’s very clear when ACD discussion is required, or if something is successful coming out of the discussion. I would appreciate your guidance here.
>
>
> For implementation, I have a branch for py-evm/trinity implemented here. Do I need to create implementations for geth/parity? Do I need to create a test case in the GitHub - ethereum/tests: Common tests for all Ethereum implementations repo? What are the requirements for acceptance into the hard fork EIP? EIP-233 only says that “[o]nce the EIP has been accepted by Core Devs, the EIP should be moved to the Accepted EIPs section”, which isn’t terribly descriptive.

In the past, Core Devs accepting it (going on ACD, discussing it, and seeing if there was consensus for acceptance) was about it.

We’ve talked about yes, tests would be good.

Yes, implementations would be good. But - client devs have said to me they actually enjoy implementing new features if they are accepted. I think a best practice would be to create tracking issues in the client repos as a first step.

So at this point, do all of these things which helps get it ready for deployment, and schedule an ACD review too.

Do we need to tighten this up? What other guidance can we give to help people succeed in proposing and having high quality EIPs accepted?

## Replies

**fubuloubu** (2019-04-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> I think a best practice would be to create tracking issues in the client repos as a first step.

So, I don’t think writing issues about including the given EIP should be a necessary condition to seek acceptance of a given EIP into a Hardfork. It also seems like an EIP doesn’t necessarily need to be in Accepted or Last Call status, nor does it strictly need test cases or an implementation as requirement. It seems like the lowest common denominator here is that the EIP simply exists and has had *enough* prior discussion so as to seem well-formed to ACDs (who will reject out of hand if it *hasn’t* had enough prior discussion). I would argue *well-formedness* means the proposal is sufficient and complete, so as to describe the concept, and has the Rationale behind it clearly identified so as to discuss the pros and cons of such an approach (including Security considerations, in a perfect world).

An implementation in at least one client is clearly a recommendation for all EIPs, which makes sense to me. This ensures you know what you’re talking about with the proposal if the author is not *well-known* to the community, but making it a requirement is difficult because it may either be too complex to actually implement in practice, or simple enough as to seem obvious. If the issue is complex, I would suggest at least a proof-of-concept be developed to aid the ACD discussions of fork inclusion (and also the EIP standardization process more generally).

Test cases seem to be suggested in only more complex proposals. This ensures implementation is de-risked a bit, as complex proposals may not be correctly implemented without an independently-developed test cases for the proposal. Eventually of course *all* EIPs scheduled for fork inclusion *must* have test cases, but I don’t think this is a necessary condition in the discussion of whether to include into a fork. Work can begin after the decision is made for inclusion, as this is the most efficient use of developer time, but it is always welcome prior to this point.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> But - client devs have said to me they actually enjoy implementing new features if they are accepted.

This is interesting. Client developers spend a lot of time on maintenance, and may enjoy the challenge of implementing a proposal. They also may prefer to implement within the team as they may have their own quality process that they trust more. Finally, they may welcome the help, as client development is a time-intensive and largely thankless job. Would be interesting to get more opinions on the matter. I would expect each team to have different opinions here.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> In the past, Core Devs accepting it (going on ACD, discussing it, and seeing if there was consensus for acceptance) was about it.

One weird thing I noticed was that my proposal I had already talked about in an ACD. I thought this was a part of the EIP process, but I was mistaken. It makes sense for ACDs to come to consensus only on hardfork EIPs, because really at the end of the day this is the decision point for what matters. This should be made more clear that Accepted isn’t necessary for proposal or even the decision for inclusion in a hard fork, but *is* a requirement prior to the decision point of GO/NO-GO of the hard fork (activation height scheduled).

It is kind of hard to wrap your head around the process, unless you think of things in terms of deliverables and schedules around a particular hard fork.

My 2 wei.

---

**wighawag** (2019-04-25):

I am new to all the process so bear with me if I am misunderstanding something.

ACD I guess means All Core Dev meeting, right ?

I am a bit concerned about what seems to be the current flow that decide what will be included in the next hardfork. I thought core dev wanted to remove some responsibility from their shoulder (a feeling shared by the community too).

From what you are saying it seems we all submit proposal and they get decided via ACD. While core devs would indeed be able to review the consensus about each EIP, I wonder where they will be looking though to decide whether there is consensus among the community or not.

Indeed, where is the place for the community to voice concern (and answer them) about inclusion of each particular proposal ?

From my experience, when I have concern about a particular EIP being included and I brought it up on the EIP’s discussion thread, we reply to me that it does not matter if you disagree about inclusion at this stage since an EIP is only about technical soundness. And I actually think it make sense, this way it is possible for multiple competing EIP  to be specified before the community decide which one should be included. But then again, where can we, as a community voice our concern (or answer them) about inclusion of particular EIP?

Is that in the comment of EIP-1679 ?

Should we not have an EIP for each proposal inclusion instead?

This would allow a more focused conversation. It would also be compatible with a different hardfork procedure where hardfork can happen more frequently on EIP per EIP basis. Basically as soon as we reach consensus on the inclusion of a particular EIP, we could start the hardfork process for that one.

---

**fubuloubu** (2019-04-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> I thought core dev wanted to remove some responsibility from their shoulder (a feeling shared by the community too).

At the end of the day, client developers decide what goes into clients. Yes, there is not a good process for capturing community sentiment, but they do alright.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> Indeed, where is the place for the community to voice concern (and answer them) about inclusion of each particular proposal ?

`discussions-to` in EIP. I would say to discuss the possible issues and mitigations with a proposal inside the specific EIP, and then maybe compare/contrast different proposals inside the meta/hardfork EIP?

So, `discussions-to` of EIP-1679 for Istanbul (which is missing!)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> It would also be compatible with a different hardfork procedure where hardfork can happen more frequently on EIP per EIP basis.

I think this has largely been denied as a possible outcome. There is far too much coordination effort required for there to be more than 1-2 a year.

---

**fubuloubu** (2019-04-25):

consciousEntity:

> the comments on this thread indicate there is a move to push any non-technical decision making beyond the ACD call and to adoption. I’d be curious to hear people’s perspectives on this approach, especially as it hasn’t previously been used.

I don’t think the comments on this thread are suggesting that, but I’ll bite and say it’s not a bad idea. The UASF and SegWit2x upgrades on Bitcoin were two very interesting upgrades that occurred and were pretty interesting for Bitcoin. I think a mechanism that takes a little power out of the hands of ACDs and puts it more into the community’s hands through running nodes is very interesting as it promotes community engagement. Critics will always day that this gives entities like Infura too much power because “no one runs Ethereum nodes” but the reality is they’ll just follow community sentiment as well.

The real problem is making this mechanism, which (ironically) could be through chain ID if chain ID were set via the hash of the genesis block and all active EIPs. We could do something like signal to peers what the node *wants* to activate and make a change at 95%

---

**boris** (2019-04-25):

consciousEntity:

> In my experience, this leads to discussion groups that emphasize promoters and developers of that EIP, at the expense of those who have broader issues with it.

I think the EthMagicians hosted discussions have had constructive criticism and pushback.

The discussions-fo is not meant to be a working group (that should be a repo or other venue) but rather an open forum for feedback.

---

**boris** (2019-04-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wighawag/48/257_2.png) wighawag:

> From my experience, when I have concern about a particular EIP being included and I brought it up on the EIP’s discussion thread, we reply to me that it does not matter if you disagree about inclusion at this stage since an EIP is only about technical soundness. And I actually think it make sense, this way it is possible for multiple competing EIP to be specified before the community decide which one should be included. But then again, where can we, as a community voice our concern (or answer them) about inclusion of particular EIP?

Not quite. Accepting an EIP as Draft or Last Call is about the technical correctness.

Including it in a hardfork is where both ACD - who more broadly steward the “health of the network” - and the community can discuss.

Without ACD giving it a thumbs up, it doesn’t get in.

If there is community contentious it doesn’t get in.

We have acknowledged we don’t know where or how the community should voice concerns. I have heard that discussions here are too technical.

Previously, without the hardfork meta, it was really hard to tell what was being proposed. For Constantinople, the majority of EIPs were all in Draft form still! So, by having [1679](https://eips.ethereum.org/EIPS/eip-1679), anyone can track all the proposals in one spot.

There already is an EIP for each EIP, so I would suggest using that discussion link to voice support or dissent for inclusion. Of course, as soon as an EIP has a number assigned - even during technical review - dissent can be registered for inclusion. Tennagraph being one way to do that.

---

**wighawag** (2019-04-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Not quite. Accepting an EIP as Draft or Last Call is about the technical correctness.

That’s what I meant

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Without ACD giving it a thumbs up, it doesn’t get in.

Make sense as they will obviously be the one implementing it.

But obviously core devs will want to follow the community sentiment and my question was really: how do we make sure the community is aware of the available choice before ACD happen ? so that the community sentiment can be established and as a result ACD decision become simplified

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> If there is community contentious it doesn’t get in.

Unless it becomes clear that 2 community differs in their vision. In that ACD could decide to implement both and make a switch in their client for the community to decide which node they’ll run, like what happen at the DAO.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Previously, without the hardfork meta, it was really hard to tell what was being proposed. For Constantinople, the majority of EIPs were all in Draft form still! So, by having 1679, anyone can track all the proposals in one spot.

I am actually very pleased to see 1679 for that. I just want to know how we can then proceed now.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> So,  discussions-to  of EIP-1679 for Istanbul

Make sense! If there are contention on several EIP we could always break that into different topics.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> There already is an EIP for each EIP, so I would suggest using that discussion link to voice support or dissent for inclusion. Of course, as soon as an EIP has a number assigned - even during technical review - dissent can be registered for inclusion. Tennagraph being one way to do that.

Yes but as mentioned EIP are about technical correctness. So usually concern about inclusion, are not welcomed there. It also less visible for those that are interested in the hardfork per se and might not see that there were alternative EIP proposed.

---

**fubuloubu** (2019-05-03):

consciousEntity:

> The group of ACDs and the client developers are largely the same, and as such have a defacto monopoly on implementation.

This is definitely what I was getting at. They do have a defacto monopoly, but they have that monopoly because they have the unique position of being the only ones who build and release client software at the end of the day.

There are multiple clients though. If a client refuses to implement a change that the community has deemed necessary, or implements a change the community disagrees with, then the community can ultimately decide not to run the client. If enough make this decision, that particular client may lose enough of the share of nodes that it may no longer be relevant, and another one can take it’s place. In that way, the community does hold ultimate authority, as this software is open source so forking the codebases is just as possible as forking the chain.

Therefore, the client developers seek to reduce the potential for this happening, so they can continue being relevant. They do this by making decisions consistent with “the community”, which often leads them to be more conservative than people expect when making changes they deem controversial.

---

**boris** (2019-05-03):

I know. That’s why I said what I did. It’s a clear example of discussion-to being pointed at the wrong thing.

Of course, I certainly would not have wanted to try and moderate that in a thread here, either – who knows how that would have turned out.

---

**abdelhamidbakhta** (2019-06-17):

What do you think about using a decentralized release management system for major Ethereum clients ? I think it could be useful for integrity checks of Ethereum clients releases and also in the future to assess specific features are present in a given version of a specific software (through a vetting process). In general i think we should use our own tech, blockchain features are great for governance use cases. I have started to implement a PoC including smart contracts, SDK and also a web dApp. We could start by using something on the mainnet.


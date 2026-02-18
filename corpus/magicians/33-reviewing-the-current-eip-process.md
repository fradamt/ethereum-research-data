---
source: magicians
topic_id: 33
title: Reviewing the current EIP process
author: jpitts
date: "2018-02-20"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/reviewing-the-current-eip-process/33
views: 5373
likes: 31
posts_count: 22
---

# Reviewing the current EIP process

Let’s get to know the current EIP process (as documented in EIP-1):

**[EIP-1: Purpose and guidelines for Ethereum Improvement Proposals](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1.md)**

**EIP Rational**

We intend EIPs to be the primary mechanisms for proposing new features, for collecting community input on an issue, and for documenting the design decisions that have gone into Ethereum.

**Three types of EIP**

1. Standard Track EIP

- Core
- Networking
- Interface
- ERC - application-level standards and conventions

1. Informational EIP - design issue, or provides general guidelines or information to the Ethereum community
2. Meta EIP - procedures, guidelines, changes to the decision-making process, and changes to the tools

**EIP Work Flow**

*The EIP process begins with a new idea for Ethereum.*

- Each EIP must have a champion
- A draft EIP should be presented as a pull request

Standards Track EIPs consist of three parts, a design document, implementation, and finally if warranted an update to the formal specification.

- It must be a clear and complete description of the proposed enhancement.
- The enhancement must represent a net improvement.
- The proposed implementation, if applicable, must be solid and must not complicate the protocol unduly.

Once an EIP has been accepted, the implementations must be completed. When the implementation is complete and accepted by the community, the status will be changed to “Final”.

**What belongs in a successful EIP?**

- Preamble
- Simple Summary
- Abstract
- Motivation
- Specification
- Rationale
- Backwards Compatibility
- Test Cases
- Implementations
- Copyright Waiver

**EIP Editor Responsibilities and Workflow**

For each new EIP that comes in

- Read the EIP to check if it is ready: sound and complete.
- Edit the EIP for language

Once ready for the repository:

- Assign an EIP number
- Accept the corresponding pull request
- List the EIP in README.md

The editors don’t pass judgment on EIPs. We merely do the administrative & editorial part.

## Replies

**AlexeyAkhunov** (2018-02-21):

Nick Johnson has been tweeting about IETF process, maybe something can be taken from there: https://www.rfc-editor.org/rfc/rfc7282.txt

---

**jpitts** (2018-02-21):

I think a lot can be learned from the IETF in terms of process, particularly from the notion of “rough consensus”. [On Consensus and Humming in the IETF](https://www.rfc-editor.org/rfc/rfc7282.txt) by Pete Resnick (which you have referenced) shows how seriously they take effective decision-making.

Also, this is Nick’s tweet thread on reaching consensus: https://twitter.com/nicksdjohnson/status/966381359051796485.

Greg has been championing the idea of learning from the IETF and other standards bodies for a long time now, and we should. Definitely point to any other organizations (even corporate as in Zappos) that we can learn from.

---

**jpitts** (2018-02-25):

Nick Johnson [@Arachnid](/u/arachnid) recently posted a [comment on EIP-898](https://github.com/ethereum/EIPs/issues/898#issuecomment-367942142) that describes current operating process really well. His description illustrates how the de-facto process is different from the process outlined in [EIP-1](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1.md)).

> Here’s my understanding of the current process, based on EIP 1 and experience:
>
>
> Someone submits a draft EIP as a pull request
> Interested participants debate the proposal until consensus on the contents of the draft have been reached.
> An EIP editor merges the PR as a draft
> Someone submits a PR to update the draft; repeat from step 2.
> Once the EIP is ‘mature’, if it modifies the protocol it’s discussed at an All Core Devs meeting. If the participants agree it’s a good idea, they implement it in their specific clients, and the EIP moves to ‘accepted’.
> Once implemented, if the EIP modifies consensus, it’s added to a scheduled hard fork.
> The hard fork and its contents are announced, and users have the opportunity to determine if they accept the hard fork or reject it.
> The hard fork block is reached, and people upgrade, or don’t.

---

**tjayrush** (2018-03-02):

I’ll start. Each item in the above list (with the exception of item 2) has a pretty clear group of participants: (1) someone…, (3) an EIP editor, (4) someone…, (5) core devs, (6) core devs (implicit), (7) miners, (8) miners. Item (2) has ‘interested participants’ which is ill-defined.

The primary concern, if I may try to voice it, is that the portion of the ‘interested participants’ that are not ‘core devs’ and who disagree with the decisions made by the ‘core devs’ (or even disagree that ‘consensus’ has been reached) have a lesser say in what happens.

I’m not suggesting any solutions, only pointing to the crux of issue. The other steps seem pretty clear to me.

---

**Arachnid** (2018-03-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> I’ll start. Each item in the above list (with the exception of item 2) has a pretty clear group of participants: (1) someone…, (3) an EIP editor, (4) someone…, (5) core devs, (6) core devs (implicit), (7) miners, (8) miners. Item (2) has ‘interested participants’ which is ill-defined.

7 and 8 are not ‘miners’, they are ‘economic participants’. Miners don’t decide which hard fork gets adopted, they follow the money. They can mine whatever fork they want, but since reorgs don’t happen across hard forks, that has no impact on which side gets accepted by the community.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/919ad9/48.png) CryptoHokie:

> Also #5 “if the participants agree…” this implies that after consensus has been reached and the EIP matured, the Core devs still have a layer of approval for go/no go.

Ultimately, this will always be the case: you cannot force the implementers of a piece of software to write or merge changes they do not agree with. If you want to force a change against the wishes of the maintainers, you will have to fork the code and do it yourself.

---

**Arachnid** (2018-03-02):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/919ad9/48.png) CryptoHokie:

> Yes, but that is meant to be debated in #2, not number five.

Disagree. Engineers who work on clients can comment during #2, but just because there’s technical consensus on the contents of an EIP doesn’t mean that they are happy to implement it in their clients. There’s a number of reasons they might object to implementing the EIP even if the specification is stable.

In my mind, the role of EIP editors should be as straightforward as possible, which means assessing as objectively as possible whether a standard is stable; this doesn’t imply assessing an EIP’s viability.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/919ad9/48.png) CryptoHokie:

> Actually I’m wondering if the open debate / initial social consensus guage should be occurring before an EIP is even submitted.

It’s very difficult to debate the merits of something that isn’t sufficiently specified.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/919ad9/48.png) CryptoHokie:

> Or some sort of agreement on what classes of changes are even allowable for EIP submission (thin line here since that requires a definition for classes of changes which itself would require consensus).

Again, trying to build in restrictions on what can be standardised misses the point. There’s nothing that says that hard fork changes have to come from EIPs; if we make the EIP process harder to navigate, people will just go elsewhere. EIPs are an *input* to the hard fork process, not part of the process itself.

---

**Arachnid** (2018-03-02):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/919ad9/48.png) CryptoHokie:

> So why not do away with any sort of social debate if the developers are ultimately the gate keepers anyway?

Because devs won’t implement something if they’re sure nobody wants it - and they’ll be more inclined to implement something if there’s clear signs it’ll be useful to people. Feedback is good.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/919ad9/48.png) CryptoHokie:

> I also don’t get what you’re saying up top about there being technical consensus but clients not wanting to implement. If it reaches the defined consensus point for acceptance, and they disagree with it, they’re free to fork. We can’t let EIPs just die because one client or one subset of interest groups disagrees, that defeats the entire point of consensus, no?

Suppose there’s consensus on an EIP that would slow down a client implementation by a factor of 10 if implemented. Clearly, client implementers would reject this.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/c/919ad9/48.png) CryptoHokie:

> At the end of the day the devs need to either honor the consensus or we abandon the thought of a greater community inclusive consensus, because devs will ultimately be acting as gatekeepers anyway, which in my opinion, defeats the purpose of trying to make any sort of decentralized governance process work.

I think you’re being ambiguous about what you mean by ‘consensus’.

In the EIP writing process, it’s agreement on what the standard should contain.

When it comes to the chain, ‘consensus’ is what clients preserve.

When it comes to adopting or not adopting changes, ‘consensus’ is something the community agrees on.

Ultimately, there’s no way to force client implementers to implement something that they don’t think is a good idea. No amount of legislating can get around that.

---

**MicahZoltu** (2018-03-02):

Really the way the governance process works is a series of vetos.  None of the vetos stop the process from moving forward, but a group exercising their veto power makes it significantly harder for the process to move forward for others.

1. First veto is the EIP editors, who can choose to not merge an EIP into draft.
2. Second veto is the Core Devs group, who can choose to recommend against a change.
3. Third veto is the client dev teams, who can choose not to implement a change.
4. Fourth veto are economic participants, who can choose not to use a client that implements a change.

The process can be skipped/bypassed by anyone.  As a user, I can fork a client, author a change, and then run a node containing that change  I will have successfully hard forked with the change I desire, but it is unlikely that anyone would join me on my chain in this case.  Thus, the veto powers at each step are weak at best.

The system has inertia as well.  If something makes it all the way to implemented in clients, it has a lot of inertia and it is actually reasonably difficult to get the community to not move forward with that change.  Similarly, if the Core Devs call results in agreement on a change, it would be hard for a single client to exercise their veto power (but they can certainly try).

---

I’m personally a fan of this mechanism for client development and protocol improvements.  I think democracy and voting in general is a terrible process because the vast majority of voters are largely uninformed and vote with their heart, not their head (I have personally done this in the past as well, it is human nature).  This process allows people who have spent a lot of time thinking about an issue the least amount of inertia pushing against them and those who have spent less time more inertia to fight against.

---

**Arachnid** (2018-03-03):

This is an excellent description of the process. I agree.

Does anyone else think we need an “I’m only an EIP” infographic/comic/animation to explain the whole process? ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**jamesray1** (2018-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> Once an EIP has been accepted, the implementations must be completed. When the implementation is complete and accepted by the community, the status will be changed to “Final”.

I disagree, client developers can choose. So I suggest that you say, “Once an EIP has been accepted, client developers choose whether to adopt them or not. If the EIP is adopted in implementations, then the community has to choose whether or not to upgrade their clients. Once the majority have updated their clients then the EIP can be considered to be adopted by the community, and the status can be changed to final.” However, an issue with this last point is that you would need to somehow track the percentage of upgrades to the latest implementation.

---

**jamesray1** (2018-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> What belongs in a successful EIP?
>
>
> Preamble
> Simple Summary
> Abstract
> Motivation
> Specification
> Rationale
> Backwards Compatibility
> Test Cases
> Implementations
> Copyright Waiver

Note that not all of these are always applicable, e.g. Backwards Compatibility, Test Cases, and Implementations. I have wrote a few EIPs and I have just left the template for these sections or commented them out.

---

**jamesray1** (2018-03-04):

https://www.rfc-editor.org/rfc/rfc7282.txt is worth reading. It raises an interesting governance process that could be applied beyond technical systems: eliminating objections or discarding a proposal if the objection can’t be technically fixed. However you would still need some kind of signalling/voting to replace humming (which starts the process of consensus), because humming can’t be done at scale and needs most stakeholders/participants to be involved in person, but like rough consensus, this signalling would be the beginning of the process. When I first heard about rough consensus I was skeptical, but this article gives a reasonable exposition of why it is useful, and better than just voting.

---

**fulldecent** (2018-03-10):

Hello, I’m Will Entriken. I wrote/championed the latest two EIP drafts that got merged, and have been involved a little in the Solidity project.

How can I help here? And what will a win look like for the Magicians project?

FYI, I am here representing myself, not part of any organization and I haven’t found any funding yet.

---

**fulldecent** (2018-03-12):

I will be attending and presenting at Exploring 721 in Dallas next weekend (discussing ERC-721). One of the topics is reviewing the standards process.

Maybe I am not the most qualified to speak on this panel, but I will do my best to inspire the next round of EIP contributors.

I hope this thread can be active in the next week so that I may learn more and be useful at the event. Of course you are all welcome to attend.

---

**jpitts** (2018-03-12):

Thanks [@fulldecent](/u/fulldecent), this is a great opportunity to educate people in the community about the process and then to get them involved.

---

**fulldecent** (2018-03-12):

Here’s all my open questions, and others I’ve heard about the current EIP-1:

1. Who assigns the editors?
2. Are the term limits or any other qualifications or restrictions on editor participation?
3. How does the champion summon an editor to initiate review?
4. What is the “Ethereum philosophy”?
5. How do you get from draft to final?
6. How do you “win” as an EIP author?

Here is every problem I see with the current process:

1. There is a strong incentive for anybody who has an interface in their program to go and standardize that interface. This results in a heaping pile of ERCs for use cases that are imagined at best. Personally I have a much higher threshold for use cases and consensus.
2. Because of the noise, it is difficult for interested and useful people to find EIPs that have a reasonable chance of passing.
3. The needs of the deciding stakeholders (“the community”? Ethereum Foundation? people with commit access to ethereum/EIPs?) are not well documented. Personally for any open source project I work with, it is nice to know you are working on a welcome problem before sending a pull request.
4. The identity of the stakeholder is unclear. If [ the Ethereum Foundation will decide on EIPs during the Project Management/All Core Devs meetings and if that meeting sets the direction of go-ethereum/Parity and if those projects are critical for Ethereum ] then effectively only the people that can vote there matter. It should be more clear whether this is the case.
5. The process to amend EIP-1 is not defined.

---

**gcolvin** (2018-03-27):

One issue is that the notion of a “mature” draft is ill-defined.  There should probably be a status called Ready which means that the Editors have approved it so far as meeting editorial standards, and the author believes it is ready for consideration by the core developers.

- Authors will likely not move a proposal forward absent consensus by the Fellowship, but (again) the Fellowship has no power here, it is the author’s proposal and the author’s choice.
- Alternatively, the Editors can choose not to move a proposal to Ready status absent Fellowship consensus.  Though again, anyone is free to submit proposals to the core devs independently.

---

**Arachnid** (2018-03-28):

I’ve written up an EIP draft proposing a revision to the EIP process [here](https://github.com/ethereum/EIPs/pull/956/files). Feedback appreciated.

---

**jpitts** (2018-05-02):

Useful “flow chart for how changes are currently made to the Ethereum platform”, tweeted by Dan Finlay:


      [twitter.com](https://twitter.com/danfinlay/status/991521043939504129)


    ![image](https://pbs.twimg.com/media/DcKW-GlXUAAMsR0.jpg:large)

####

 Here's a flow chart for how changes are currently made to the Ethereum platform. #EIP0

  [8:33 PM - 1 May 2018](https://twitter.com/danfinlay/status/991521043939504129)




       281





       92

---

**tjayrush** (2018-07-18):

Has there been any suggestion about an EIP status called ‘Withdrawn’?

There’s been discussion about ‘closing’ EIPs if they never enter Final Call or if the do enter Final Call but get rejected, but there doesn’t seem to be a way to remove an EIP from active consideration.

The reason this matters to me is, if one thinks about new entrants to the space, whose best way to learn about what’s going on in a deeply technical way is to read every comment on every EIP, it would be helpful if they could easily identify EIPs that have little or no chance of ever becoming part of the spec (to the extent that there is a spec).

If there was a status called ‘Withdrawn’ the author could, much like moving an EIP to ‘Final Call’ simply move the EIP to ‘Withdrawn.’  The Core Devs then have a bit of an easier path. If they simply ignore the EIP, or speak about it briefly and don’t suggest that the author moves it forward, then hopefully, the author will get the idea that it’s best to move the EIP to withdrawn.

The header of withdrawn EIPs could be colored pink or something to make them obvious.

Thoughts?


*(1 more replies not shown)*

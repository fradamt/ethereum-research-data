---
source: magicians
topic_id: 3627
title: Case discussion on the EIP process, based on EIP-1900 & EIP-1
author: loredanacirstea
date: "2019-09-05"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/case-discussion-on-the-eip-process-based-on-eip-1900-eip-1/3627
views: 3301
likes: 1
posts_count: 28
---

# Case discussion on the EIP process, based on EIP-1900 & EIP-1

Threads that started this discussion:

https://twitter.com/danfinlay/status/1168187079089508352



      [twitter.com](https://twitter.com/lorecirstea/status/1168204570390147072)



    ![image](https://pbs.twimg.com/profile_images/1419943375936135169/qqAS_x5l_200x200.png)

####

[@lorecirstea](https://twitter.com/lorecirstea/status/1168204570390147072)

  Timeline thread 👇

  https://twitter.com/lorecirstea/status/1168204570390147072










I am also posting my timeline here:

1. ERC-1900: Decentralized Type System for EVM · Issue #1882 · ethereum/EIPs · GitHub opened on March 28th, EIP-1900 Decentralized Type System for EVM by loredanacirstea · Pull Request #1900 · ethereum/EIPs · GitHub opened on April 2nd.
2. Pinged an editor on April 6th for EIP number - no response
3. Wrote 3 articles about dType parts: Medium
4. Made 3 video demos: https://www.youtube.com/playlist?list=PL323JufuD9JC46yClCf5fdaEX17kocem7
5. All shared on Twitter & Reddit, EIPs on EIP Gitter chat
6. https://twitter.com/jemenger/status/1143655108896362497

The article mentions the Draft PR, exactly where the opcode section was (NJ now says he did not see it). NJ was interested. I also gave him the issue link to discuss.First EIP editor interested!

1. 1- NJ comments were useful - I said as much. But, up to a point, when he wanted to close the discussion because I wouldn’t do as he proposed. And kept asking for more and more content, even after I limited the EIP scope.
2 - My PR was unmerged, the only editor looking was stopping collaboration, while he was promoting fast Draft merging without technical soundness check - after the whole EIP999. So, I did not understand why he would not merge it after spending so much time on it.
2. July 2nd: ERC-1900: Decentralized Type System for EVM · Issue #1882 · ethereum/EIPs · GitHub I say: “Therefore, I do not see a reason to deny merging of this ERC Draft to master”. NJ still did not review/merge the PR.
3. July 2-4: I made proposals for EIP editors: Pull requests · ethereum/EIPs · GitHub
4. EIP1900 merged July 7th - not by NJ though.

[@danfinlay](/u/danfinlay)

, if you still think there are lapses in logic & I was overreacting, I can spend 30-60 min to go through the EIP discussion with you (not on Twitter, but on ETHMagicians, Gitter, etc.) & hear what I could have done better at each point.

## Replies

**loredanacirstea** (2019-09-05):

Regarding:

https://twitter.com/danfinlay/status/1169688792527065093

I can’t know if he acted will malice. That is not under contention. What I said was that he abused my EIP and me personally (on Twitter, even when his person was not involved in the discussion).

But we are not here to discuss him, I hope we are here to discuss my fault: how did I miscommunicate?

---

**danfinlay** (2019-09-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/loredanacirstea/48/2202_2.png) loredanacirstea:

> But we are not here to discuss him, I hope we are here to discuss my fault: how did I miscommunicate?

So first of all, the EIP process is slow, and it’s run by volunteers, and that sucks. I think he needed to be clear when he was communicating as an editor and when not, and I think he even agrees about that.

I didn’t see instances of him being specifically abusive. Some of the worst things you claimed out were things like pinging EIP editors, and getting no response, and I confirmed you waited like 3 months for EIP 1900 to be merged, but [you had only pinged nick savers](https://github.com/ethereum/EIPs/pull/1900#issuecomment-480512721). Maybe you meant to ping Nick Johnson there, and maybe this is why you thought he was being abusive?

I think the EIP process seems overwhelmed right now, I also have submissions that are not being actively interacted with, but I just assume people are busy, I don’t assume it’s malice.

From your timeline, I didn’t see any instance of Nick being directly abusive to you on Github nor Twitter (maybe you could still link to examples, but they weren’t there), but [you did act fairly cruel](https://twitter.com/lorecirstea/status/1168085577503313920) once you had decided Nick was acting against you.

I feel like a lot of this is frustration that there hasn’t been wider community embrace of your proposals, and I mostly side with my earlier thought, that most people are just busy and distracted. I tend to agree with the saying “Genius is 1 percent inspiration and 99 percent perspiration.” The ideas you’ve shared may be great, and inevitable, and maybe they [make ENS obsolete](https://medium.com/@loredana.cirstea/flexible-alias-or-why-ens-is-obsolete-a1353030f445), but I just don’t think it’s productive to get defeated when sharing an idea doesn’t make it take off in a 3 day window.

I think tools like dType and pipeline are useful even one user at a time, and maybe you don’t want to do it, but maybe you need a teammate who is willing to go talking to developers one at a time, and showing them how it works, why it saves them time, how it makes their contracts more composable. The first ~6 months of MetaMask was a big education effort. Most dapps built wallets into the site by default, and storing keys in an extension was not at all an intuitive next step. It can take a while to educate people into new paradigms.

I’m a huge fan of your work, and I first started following you because I was also interested in graph-based smart contract authoring, but MetaMask keeps me so busy, I can’t read every proposal by anyone, even my favorite thinkers. Things fall through the cracks. Helping people allocate their attention to the highest-impact things is one thing I’d love to see come out of blockchain, but until we have that, we have to be sympathetic to the fact that our listeners are mortal, they have limited attention and energy and time in the day, and no matter how good our ideas are, most of the value will always come from the labor of implementation, not from the idea itself.

A few times you expressed irritation at people who you perceived as being dense, or not attentive enough. I think this attitude is sometimes getting directly in the way of people who might otherwise want to learn more about the systems you’re proposing.

Infrastructure like type systems may not get viral buzz like a hot ICO, but I wish that wasn’t as demotivating to you.

Anyways, I wish good ideas always won, but ideas transmit by communication, and sometimes that communication can be tedious, and repetitive, but that’s communication, and it’s all we’ve got. I hope you find a way to rally the support you deserve without feeling slighted.

---

**loredanacirstea** (2019-09-05):

If we want to get a clear answer on a problem, we should stick with the problem.

I am going to avoid answering to anything else than the issue at hand: “It looks like a bit of miscommunication to me.”

I can answer to your other points after we clarify this one. So, how did I miscommunicate when trying to get EIP-1900 merged?

Please tell me one instance of miscommunication. We clarify that, and then we move to the next instance.

---

**danfinlay** (2019-09-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/loredanacirstea/48/2202_2.png) loredanacirstea:

> So, how did I miscommunicate when trying to get EIP-1900 merged?

For one thing, you said you had tried to ping EIP editors, but [had only pinged Nick Savers](https://github.com/ethereum/EIPs/pull/1900#issuecomment-480512721). Did you mean to ping Nick Johnson? Is it possible you were mad at him for not replying to a message that was never sent to him?

---

**loredanacirstea** (2019-09-05):

I pinged Nick Savers because I saw he was reviewing EIPs at that time. There was no other active reviewer at that specific time.

I also posted in https://gitter.im/ethereum/EIPs?at=5c9ce69caee5b449f3aafdcb

> Just opened an issue for an EIP that I want to propose, to gather feedback: Decentralized Type System ethereum/EIPs#1882. There are links to the current in work implementation & a demo video. Comments, suggestions are really appreciated and I think we need this if we want better interoperability.

No, I did not confuse Nick Johnson with Nick Savers.

Is this an instance of miscommunication from my part?

---

**loredanacirstea** (2019-09-06):

[@danfinlay](/u/danfinlay), it has been 18h hours and you have not answered. If anyone else wants to answer how this constitutes miscommunication from my part, I am open to hear it.

Otherwise, unless another instance of alleged miscommunication is produced in the next 12h, I will consider that I have not miscommunicated during the EIP-1900 process. And we can move to the next point.

---

**danfinlay** (2019-09-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/loredanacirstea/48/2202_2.png) loredanacirstea:

> @danfinlay, it has been 18h hours and you have not answered. If anyone else wants to answer how this constitutes miscommunication from my part, I am open to hear it.

Sorry, there are a lot of things that have been demanding my attention lately. I’m fine conceding miscommunication was not your problem. Instead, it was maybe getting angry when no malice was intended.

If you’re going to take one point at a time, I’m not sure I’ll be able to maintain the discussion. I might suggest a forum like kialo that allows many nested points to be addressed very specifically at once, if you require this kind of granularity to the discussion.

---

**loredanacirstea** (2019-09-06):

> Sorry, there are a lot of things that have been demanding my attention lately.

You opened the discussion in the first place.

And the only reasons for which I am willing to put time into this myself are:

- I valued your opinion and wanted to see the exact points on which we agree and disagree
- I started this as a discussion on the EIP process, to see if I could have done anything better when proposing EIP-1900 (others might be interested in this too)

> I’m fine conceding miscommunication was not your problem

Ok. But I hope it is not because of the medium or lack of time.

> Instead, it was maybe getting angry when no malice was intended.

Then this will be the next point.

> If you’re going to take one point at a time, I’m not sure I’ll be able to maintain the discussion

I think there is no other way to clarify a situation.

> I might suggest a forum like kialo

You offered me the option to choose the medium and I thought the EIP process discussion could be useful here. We can use kialo (which seems great) for the other, unrelated topics.

---

**loredanacirstea** (2019-09-06):

> Instead, it was maybe getting angry when no malice was intended.

> https://twitter.com/danfinlay/status/1168192376294105088
> but I think some of that un-clarity was met with overly quick hostility

I already said: “I can’t know if he acted will malice. That is not under contention.”

What was the first occurrence from [issue #1882](https://github.com/ethereum/EIPs/issues/1882) that you consider as “overly quick hostility” or “getting angry”?

---

**loredanacirstea** (2019-09-07):

I take this personally because: [The Ethereum Unicorn](https://medium.com/@loredana.cirstea/the-ethereum-unicorn-f7674b84dc69).

If I see a problem, I want to fix it. If I am not the only one, then where are they and why are they not doing the same as I am? I am using this case discussion to exactly determine the problems. I am willing to fight for others and find solutions - see my [EIP-1 process proposals](https://github.com/ethereum/EIPs/pulls?q=is%3Apr+is%3Aopen+editors+author%3Aloredanacirstea).

---

**loredanacirstea** (2019-09-07):

[@danfinlay](/u/danfinlay), I do not want us to forget the state in which this discussion is, so I am pressing ahead. Since you seem to not have time, I will make an assumption and answer the question for you.

So, I will assume the first instance is in: [ERC-1900: Decentralized Type System for EVM · Issue #1882 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/1882#issuecomment-507619192)

> I suggest you pay attention to how clearly you phrase your questions before being unsatisfied with the answer.

The sequence of interactions that resulted in my above phrase is:

> One interface can have many implementations, but there doesn’t seem to be any distinction made between the two here. comment

> LC: Are you referring to the dType registry interface and implementation or to the type library? comment

> No, I’m talking about the distinction between a type definition and an implementation. For example, the ERC20 standard defines some types, which are implemented by a large number of different contracts. Capturing the ability for a type to have many implementations seems like a pretty basic feature to support. comment

If the word `types` has the exact same meaning in both `ERC20 standard defines some types` and in `ability for a type to have many implementations`, then:

- The ERC20 standard defines functions types and devs can indeed implement the functions as they please.
- ERC20 function types can be defined & registered as types in dType. Devs can still implement them as they please.

But, I assumed that the problem was with non-function types. And from this perspective, the ERC20 example is a bad example (I was confused because of it).

- Solidity is statically typed → building a type system on top of it is restrictive → the best solution that we found is one based on structs.
- when you describe a custom struct with dType, you can generate its implementation → devs are not free to change the implementation, which is an automation feature; but devs are those who propose the type description in the first place.

Therefore, my answer:

> LC: Devs have the freedom to implement type helper functions, as long as the required ones are implemented (to be discussed). As for the definition, I am open to other proposals that not necessarily based on structs. I am actually trying to have optional subtypes, that can be stored with map. dType registry will be extended with an additional optionals field in the dType struct & a standardized way to define optionals in the Type Library, but this is not ready yet. Other than this, what can I do more to give more freedom to the implementation comment

> I still think you’re not understanding the difference between an interface and an implementation. An interface describes an API for other code to interact with, but not how it’s implemented. What you’re proposing here seems to be more along the lines of a directory of library code.
> […] [the spec] doesn’t make a clear distinction between interfaces and implementations. I wish you luck, but I don’t plan to offer further technical feedback.
> comment

At this point I was expecting references to the lines of code that were the culprit (one big reason why we use GitHub & PR reviews) and some pointers as to what can I do to fix them. But here, the assumption was that I do not know the general difference between an interface and an implementation.

I still do not know what the exact problem was. If someone knows exactly, please explain.

> LC: I asked you before: “Are you referring to the dType registry interface and implementation or to the type library?”, to which you answered with “No, I’m talking about the distinction between a type definition and an implementation”. I suggest you pay attention to how clearly you phrase your questions before being unsatisfied with the answer.
> I thought it was clear that this ERC aims to both:
>
>
> standardize type libraries
> propose a unique type registry to be implemented (anyone can make their own registry, and the interface is defined here: EIPs/EIPS/eip-1900.md at 8d46acbaaead36b2063dc31fbfbf4fca1e34e621 · ethereum/EIPs · GitHub, but it is beneficial to have a unique registry and I explained why already)
> comment

So, regarding this interface-implementation criticism, the status was:

- comparison with ERC20, which is a different type of standard
- no reference to any lines of code/spec
- no code/spec examples
- this criticism was used as one of the reasons for stopping any further technical feedback

Considering the above, do you consider my phrase: **“I suggest you pay attention to how clearly you phrase your questions before being unsatisfied with the answer.”** as being untrue? Did I not point out the exact problem that I was facing?

If I become aware of a problem, I will voice it - it is the only way to help the communication advance. Overlooking makes me feel like a hypocrite and it does not help any discussion party understand or improve.

[@danfinlay](/u/danfinlay), if you think my comment is coming off as unwarranted hostility, please help me rephrase it.

[@Arachnid](/u/arachnid), if you think I misunderstood your quoted words from above or if you have any material that I overlooked, let me know.

---

**Arachnid** (2019-09-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/loredanacirstea/48/2202_2.png) loredanacirstea:

> if you think I misunderstood your quoted words from above or if you have any material that I overlooked, let me know.

How would you represent ERC20 or another standard, where the standard defines an interface that can have multiple independent implementations, in DType?

ERC20 and others define an interface in the form of an ABI, and specify some constraints on their behaviour, but do not prescribe an implementation. Many different contract instances can be accessed using this interface, without the caller having to care about how it is implemented.

DType, in contrast, seems to assume each type will have exactly one implementation.

---

**loredanacirstea** (2019-09-07):

[@Arachnid](/u/arachnid), thank you for coming into the conversation.

I already said:

> The ERC20 standard defines functions types and devs can indeed implement the functions as they please.
> ERC20 function types can be defined & registered as types in dType. Devs can still implement them as they please.
>
>
> non-function types:
>
>
> Solidity is statically typed → building a type system on top of it is restrictive → the best solution that we found is one based on structs.
> when you describe a custom struct with dType, you can generate its implementation → devs are not free to change the implementation, which is an automation feature; but devs are those who propose the type description in the first place.

> As for the definition, I am open to other proposals that not necessarily based on structs.

So:

- functions are described with dType by registering their ABI → implementation is left to the dev (not all types have exactly one implementation)
- non-function types indeed have a deterministic implementation

We never said this is an interface system, but a type system. However, the registry itself has an interface and could be implemented differently by others.

Types intended to be used in the EVM need to have a deterministic implementation - types are not interfaces and devs + machines need to know what to expect:

- a type definition library
- a type definition struct
- standardized names + ABI structure for additional type checking library functions (implementation is left to the dev)
- a set of standard functions for type manipulation (implementation is left to the dev)

Also, this is an example of how one can build types visually: [Visual dType](https://pipeos-one.github.io/visual-dtype). The main output is a JSON that will be stored in the registry. From this JSON you could also build & deploy the type automatically if you do not know how to code & want the easy way.

Note: Devs can create their own types (up to `2^256-1`), with another name, if they are unhappy with an already registered type.

---

**Arachnid** (2019-09-07):

Can you give an example, then, of how you would define a DType type with, say, the ERC20 transfer method, and how multiple developers would implement this? I still don’t see how that’s possible in DType, so an end-to-end example would really help.

---

**loredanacirstea** (2019-09-08):

I have responded to this question in the [EIP-1921 discussion thread](https://github.com/ethereum/EIPs/issues/1921#issuecomment-529191345), because I would like to keep the current thread on point.

---

**loredanacirstea** (2019-09-09):

EIP-1900 only describes a data type system. EIP-1921 only describes the function type extension.

For standards like ERC20, you need an extension to interfaces and that will come in future EIPs.

This discussion was only about EIP-1900, and possibly EIP-1921.

[@Arachnid](/u/arachnid) demonstrated that he does not understand dType as described in these two standards, because he demands that an interface heavy standard should be described with these tools. A simpler demo of what dType does (only EIP-1900), is made available in this video: https://youtu.be/GZg4L2o0Nyw

[@danfinlay](/u/danfinlay), therefore, [@Arachnid](/u/arachnid) could not have “refined” the specs, beyond the first (indeed useful) comments on the spec structure & clarity

> but Nick here got into the proposal, and seemed to be trying to help refine the spec source

---

**Arachnid** (2019-09-10):

All I am asking for is a practical end to end example of how someone would use DType - how you define a type, implement it, and consume it. I used ERC20 as an example because it’s a commonly used interface everyone understands, but I’d be happy to see any end to end example.

If someone like myself who is heavily involved in the ethereum smart contract field has difficulty understanding the scope and intent of DType, you may want to consider the possibility that there is an issue with the ease of understanding your specification, rather than with my ability to consume it.

---

**loredanacirstea** (2019-09-10):

[@Arachnid](/u/arachnid), fair point, but I did not understand that the purpose of EIP-1900 was not clear to you when we had the discussion on #1882. Only now I understand because you were clear about it.

I answered your above question here: https://github.com/ethereum/EIPs/issues/1882#issuecomment-529840460

---

**loredanacirstea** (2019-09-10):

A. I see no interest for:

- a detailed analysis on the conclusions and opinions put forth by @danfinlay, @Arachnid and myself
- a detailed analysis of the EIP process in this case discussion

B. I see:

- @danfinlay expressing opinions without being prepared to give the other party (myself) time for rebuttal
- people quickly being sensitive around the word “obsolete”, referring to a tech, while not giving a damn about gatekeeping and actual ad hominem (1, 2). Yes, DNS should be made obsolete; if ENS started as a decentralized copy of DNS and does not plan to change, then you are promoting tech that stifles innovation and a truly machine-readable world)
- readers passively reading & waiting for a conclusion, instead of actively participating

When I will see interest in A, I will continue this analysis.

And any time someone will bring any of these topics into a discussion on another topic, I will ping them here, since they have time to discuss it and force me to have time to discuss it.

[@danfinlay](/u/danfinlay), you should at least post a clarification to https://twitter.com/danfinlay/status/1168187079089508352, saying that I did not miscommunicate, as you conceded in [this comment](https://ethereum-magicians.org/t/case-discussion-on-the-eip-process-based-on-eip-1900-eip-1/3627/8).

---

**danfinlay** (2019-09-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/loredanacirstea/48/2202_2.png) loredanacirstea:

> @danfinlay expressing opinions without being prepared to give the other party (myself) time for rebuttal

Sorry, like I’ve said repeatedly, I don’t have a lot of time to spare, and I already gave a lot of time to my initial feedback, which you are free to take and leave as you like. It seems you’ve had a lot of time to respond, and I’m willing to respond as I’m able, I’m sorry it’s not synchronous, there are many important things competing for my attention right now.

I will try to get back to this, but if you’re going to read slow delays as unacceptable disinterest or even “not giving you time for rebuttal”, then I will just leave it alone, as it seems like I may be doing more harm than good.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/loredanacirstea/48/2202_2.png) loredanacirstea:

> @danfinlay, you should at least post a clarification to https://twitter.com/danfinlay/status/1168187079089508352 , saying that I did not miscommunicate, as you conceded in this comment.

Thanks for highlighting the most important thing for me to reply on.

From what I can tell, the hostility began around [June 2](https://github.com/ethereum/EIPs/issues/1882#issuecomment-507619192). Phrases like:

- I suggest you pay attention to how clearly you phrase your questions before being unsatisfied with the answer.
- So aside from your destructive (as opposed to constructive) and your inexact criticism, what can I do?

I totally get that this was frustration at not getting merged, but I would also point out that at no point during this issue discussion do you link to the pull request that you’re referring to, so I could imagine that Nick didn’t even realize there was a PR that you were suggesting, and didn’t see himself as blocking at all.

There were also lots of instances of hostility in [the more recent twitter thread](https://twitter.com/lorecirstea/status/1168085577503313920).

Anyways, I’m not judging, I really do understand the frustration with the EIP process, I have EIPs that also do not get merges or comments. I’m just answering your question so you can hopefully understand why from my perspective, this just looks like a misunderstanding that got escalated.

I’ll try to review the other comments soon, sorry for the regular absence, it is not meant in bad spirit.


*(7 more replies not shown)*
